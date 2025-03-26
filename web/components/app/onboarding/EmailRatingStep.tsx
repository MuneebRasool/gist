import { useCallback, useEffect, useState } from 'react';
import { toast } from 'sonner';
import { AnimatePresence } from 'framer-motion';
import EmailService from '@/services/nylas/email.service';
import { Email } from '@/types/nylasEmail';
import { useOnboardingStore } from '@/store/onboarding.store';
import EmailCard from './EmailCard';
import QuestionPrompt from './QuestionPrompt';
import ProgressIndicator from './ProgressIndicator';
import { LoadingScreen } from './LoadingScreen';
import NoEmail from './EmailTriage/NoEmail';

export const EmailRatingStep = () => {
	const [currentEmailIndex, setCurrentEmailIndex] = useState(0);
	const [isLoading, setIsLoading] = useState(true);
	const {
		emailRatings,
		setTopEmails,
		currentStep,
		topEmails: emails,
		setEmailRatings,
		setRatedEmails,
		setCurrentStep,
	} = useOnboardingStore();

	const fetchEmails = useCallback(async () => {
		console.log('fetchEmails', emails.length, currentStep);
		if (emails.length > 0 || currentStep !== 'email-rating') {
			setIsLoading(false);
			return;
		}
		try {
			setIsLoading(true);
			const response = await EmailService.getOnboardingEmails({ limit: 5, in_folder: 'INBOX' });

			if (response.error) {
				toast.error('Failed to load emails. Please try again.');
				return;
			}

			if (response.data?.data) {
				const transformedEmails = response.data.data.map((email: Email) => ({
					...email,
					date: typeof email.date === 'string' ? new Date(email.date).getTime() / 1000 : Number(email.date),
				}));
				console.log('transformedEmails', transformedEmails);
				setTopEmails(transformedEmails);
				const initialRatings: Record<string, number> = {};
				transformedEmails.forEach((email) => {
					initialRatings[email.id] = 3;
				});
				setEmailRatings(initialRatings);
			}
		} catch (error) {
			console.error('Error fetching emails:', error);
			toast.error('Failed to load emails. Please try again.');
		} finally {
			setIsLoading(false);
		}
	}, [currentStep, setEmailRatings, setTopEmails]);

	// Fetch emails
	useEffect(() => {
		fetchEmails();
	}, [fetchEmails]);

	const handleEmailRate = (rating: number) => {
		const currentEmail = emails[currentEmailIndex];
		setEmailRatings({
			...emailRatings,
			[currentEmail.id]: rating,
		});
	};

	const handleNextEmail = async () => {
		if (currentEmailIndex < emails.length - 1) {
			setCurrentEmailIndex((prev) => prev + 1);
		} else {
			await handleComplete();
		}
	};

	const handleComplete = async () => {
		try {
			setIsLoading(true);
			const simplifiedEmails = emails.map((email) => ({
				id: email.id,
				subject: email.subject || '',
				from: Array.isArray(email.from) ? email.from : [],
				snippet: email.snippet || '',
				date: email.date || 0,
				body: email.body || '',
			}));

			setRatedEmails(simplifiedEmails);
			setCurrentStep('questions');
		} catch (error) {
			console.error('Error completing email rating:', error);
			toast.error('Failed to complete email rating. Please try again.');
			setIsLoading(false);
		}
	};

	if (isLoading) {
		return <LoadingScreen message={'Loading your emails...'} />;
	}

	if (emails.length === 0) {
		return <NoEmail />;
	}

	return (
		<div className='flex flex-col items-center justify-center px-4 py-8'>
			<QuestionPrompt />

			<AnimatePresence mode='wait'>
				{emails.length > 0 && (
					<div key={emails[currentEmailIndex].id} className='rounded-2xl bg-background/80'>
						<EmailCard
							email={emails[currentEmailIndex]}
							currentRating={emailRatings[emails[currentEmailIndex].id]}
							onRate={handleEmailRate}
							onNext={handleNextEmail}
							isLastEmail={currentEmailIndex === emails.length - 1}
						/>
					</div>
				)}
			</AnimatePresence>

			<ProgressIndicator currentIndex={currentEmailIndex} totalEmails={emails.length} />
		</div>
	);
};
