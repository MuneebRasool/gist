'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { useOnboardingStore } from '@/store/onboarding.store';
import { EmailRatingStep } from '@/components/app/onboarding/EmailRatingStep';
import { QuestionsStep } from '@/components/app/onboarding/QuestionsStep';
import { LoadingScreen } from '@/components/app/onboarding/LoadingScreen';
import { ReviewPersonalityStep } from '@/components/app/onboarding/ReviewPersonalityStep';
import CompletedStep from '@/components/app/onboarding/CompletedStep';
import EmailService from '@/services/nylas/email.service';
import { AgentService } from '@/services/agent.service';
import { OnboardingService } from '@/services/agent/onboarding.service';
import { toast } from 'sonner';
import { useRouter } from 'next/navigation';

export default function OnboardingPage() {
	const searchParams = useSearchParams();
	const router = useRouter();
	const {
		currentStep,
		setUserEmail,
		topEmails,
		setTopEmails,
		questions,
		setQuestions,
		summary,
		setSummary,
		emailRatings,
		ratedEmails,
		userEmail,
		setEmailRatings,
		answers,
		domain,
	} = useOnboardingStore();
	const [isLoading, setIsLoading] = useState(true);
	const [fetchError, setFetchError] = useState<string | null>(null);

	// Set email from params
	useEffect(() => {
		const emailFromParams = searchParams.get('email');
		if (emailFromParams) {
			setUserEmail(emailFromParams);
		}
	}, [searchParams, setUserEmail]);

	// Handle data fetching based on current step
	useEffect(() => {
		const fetchData = async () => {
			setIsLoading(true);
			setFetchError(null);

			try {
				if (currentStep === 'email-rating' && topEmails.length === 0) {
					console.log('Fetching emails for onboarding');
					const response = await EmailService.getOnboardingEmails({ limit: 5, in_folder: 'INBOX' });

					if (response.error) {
						setFetchError('Failed to load emails. Please try again.');
						toast.error('Failed to load emails. Please try again.');
						return;
					}

					if (response.data?.data) {
						const transformedEmails = response.data.data.map((email) => ({
							...email,
							date: typeof email.date === 'string' ? new Date(email.date).getTime() / 1000 : Number(email.date),
						}));

						setTopEmails(transformedEmails);

						// Initialize ratings
						const initialRatings: Record<string, number> = {};
						transformedEmails.forEach((email) => {
							initialRatings[email.id] = 3;
						});
						setEmailRatings(initialRatings);
					}
				}

				// Questions step data
				else if (currentStep === 'questions' && questions.length === 0) {
					console.log('Fetching domain inference for onboarding');
					if (!userEmail) {
						setFetchError('User email is missing. Please try again.');
						toast.error('User email is missing. Please try again.');
						return;
					}

					const response = await AgentService.inferDomain(userEmail, ratedEmails, emailRatings);

					if (response.error) {
						console.error('Domain inference error:', response.error);
						setFetchError('Failed to load onboarding questions. Please try again.');
						toast.error('Failed to load onboarding questions. Please try again.');
						router.push('/app/dashboard');
						return;
					}

					if (response.data) {
						setQuestions(response.data.questions || []);
					}
				}

				// Personality data
				else if (currentStep === 'reviewPersonality' && !summary) {
					console.log('Fetching personality data for onboarding');
					const onboardingData = {
						questions,
						answers,
						domain: domain || '',
						emailRatings,
						ratedEmails: ratedEmails || [],
					};

					const response = await OnboardingService.submitOnboardingData(onboardingData);

					if (response.error) {
						setFetchError('Failed to load personality data. Please try again.');
						toast.error('Failed to load personality data. Please try again.');
						return;
					}

					if (response.data) {
						setSummary(response.data.personalitySummary ?? 'Personality Summary');
					}
				}
			} catch (error) {
				console.error('Error fetching onboarding data:', error);
				if (error instanceof Error) {
					console.error('Error details:', error.message);
				}
				if (error instanceof Response) {
					console.error('Response status:', error.status, 'Response text:', await error.text());
				}
				setFetchError('An error occurred while loading data. Please try again.');
				toast.error('An error occurred while loading data. Please try again.');
			} finally {
				setIsLoading(false);
			}
		};

		fetchData();
	}, [
		currentStep,
		topEmails.length,
		questions.length,
		summary,
		emailRatings,
		ratedEmails,
		userEmail,
		answers,
		domain,
		router,
		setEmailRatings,
		setQuestions,
		setTopEmails,
		setSummary,
		questions,
	]);

	if (isLoading) {
		let message = 'Loading...';
		if (currentStep === 'email-rating') message = 'Loading your emails...';
		if (currentStep === 'questions') message = 'Creating your personalized dashboard...';
		if (currentStep === 'reviewPersonality') message = 'Fetching personality data...';
		if (currentStep === 'task_generation') message = 'Extracting Tasks...';

		return <LoadingScreen message={message} />;
	}

	if (fetchError) {
		// Handle error state - could be more sophisticated in a real app
		return (
			<div className='flex min-h-screen flex-col items-center justify-center p-4'>
				<div className='relative rounded border border-red-300 bg-red-50 px-4 py-3 text-red-700' role='alert'>
					<strong className='font-bold'>Error: </strong>
					<span className='block sm:inline'>{fetchError}</span>
				</div>
			</div>
		);
	}

	if (currentStep === 'email-rating') {
		return <EmailRatingStep emails={topEmails} />;
	}

	if (currentStep === 'questions') {
		return <QuestionsStep questions={questions} />;
	}

	// Fixed the condition that was causing issues
	if (currentStep === 'reviewPersonality' || currentStep === 'task_generation') {
		return <ReviewPersonalityStep personalitySummary={summary} />;
	}

	if (currentStep === 'completed') {
		return <CompletedStep />;
	}

	return null;
}
