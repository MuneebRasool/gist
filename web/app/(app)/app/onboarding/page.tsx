'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { AgentService } from '@/services/agent.service';
import { QuestionWithOptions } from '@/types/agent';
import { useOnboardingStore } from '@/store/onboarding.store';
import { toast } from 'sonner';
import { motion, AnimatePresence } from 'framer-motion';
import { OnboardingService, OnboardingFormData, SimplifiedEmail } from '@/services/agent/onboarding.service';

// Import extracted components
import { OnboardingAssistant } from '@/components/app/onboarding/OnboardingAssistant';
import { QuestionCard } from '@/components/app/onboarding/QuestionCard';
import { SummaryView } from '@/components/app/onboarding/SummaryView';
import { LoadingScreen } from '@/components/app/onboarding/LoadingScreen';
import { NavigationButtons } from '@/components/app/onboarding/NavigationButtons';
import { ProgressBar } from '@/components/app/onboarding/ProgressBar';

const loadingMessages = [
	"Creating your personalized dashboard...",
	"Analyzing your email preferences...",
	"Setting up task extraction...",
	"Finalizing your profile...",
	"Almost ready to show your dashboard..."
];

const OnboardingPage = () => {
	const router = useRouter();
	const searchParams = useSearchParams();
	const email = searchParams.get('email') || localStorage.getItem('userEmail') || '';
	const domain = searchParams.get('domain') || localStorage.getItem('domain') || '';

	const {
		questions,
		summary,
		answers,
		isLoading,
		isCompleted,
		setQuestions,
		setSummary,
		setAnswer,
		setIsLoading,
		setIsCompleted,
	} = useOnboardingStore();

	const [isSubmitting, setIsSubmitting] = useState(false);
	const [loadingMessageIndex, setLoadingMessageIndex] = useState(0);
	const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
	const [showSummary, setShowSummary] = useState(false);
	const [assistantMessage, setAssistantMessage] = useState("I'll help you set up your profile. Let's start with a few questions.");

	useEffect(() => {
		const fetchDomainInference = async () => {
			if (!email) {
				toast.error('Email not found. Please try connecting your email again.');
				router.push('/app/dashboard/settings');
				return;
			}
	
			setIsLoading(true);
	
			try {
				// Ensure localStorage is only accessed in the client
				if (typeof window === 'undefined') return;
	
				// Get rated emails and ratings from localStorage
				let storedEmails: SimplifiedEmail[] = [];
				let storedRatings: Record<string, number> = {};
	
				try {
					const emailsJson = localStorage.getItem('ratedEmails');
					const ratingsJson = localStorage.getItem('emailRatings');
	
					storedEmails = emailsJson ? JSON.parse(emailsJson) : [];
					storedRatings = ratingsJson ? JSON.parse(ratingsJson) : {};
				} catch (parseError) {
					console.error('Error parsing stored emails or ratings:', parseError);
				}
	
				// Call domain inference API
				const response = await AgentService.inferDomain(email, storedEmails, storedRatings);
				console.log('Domain inference response:', response);
	
				if (response.error) {
					console.error('Domain inference error:', response.error);
					toast.error('Failed to load onboarding questions. Please try again.');
					router.push('/app/dashboard');
					return;
				}
	
				if (response.data) {
					console.log('Domain inference data:', response.data);
	
					// Set questions
					setQuestions(response.data.questions || []);
	
					//Set summary based on response data
					const generatedSummary =
						response.data.summary ||
						(response.data.domain
							? `Based on your email, we've personalized some questions for your ${response.data.domain} context.`
							: 'Please answer these questions to help us personalize your experience.');
	
					setSummary(generatedSummary);
				}
			} catch (error) {
				console.error('Error fetching domain inference:', error);
				toast.error('Failed to load onboarding questions. Please try again.');
				router.push('/app');
			} finally {
				setIsLoading(false);
			}
		};
	
		// Run only on client side
		if (typeof window !== 'undefined') {
			fetchDomainInference();
		}
	}, [email, router, setIsLoading, setQuestions, setSummary]);
	
	// Add effect to cycle through loading messages when isSubmitting is true
	useEffect(() => {
		let interval: NodeJS.Timeout;
		
		if (isSubmitting) {
			// Set up interval to cycle through loading messages every 4 seconds
			interval = setInterval(() => {
				setLoadingMessageIndex(prev => (prev + 1) % loadingMessages.length);
			}, 4000);
		}
		
		// Clean up interval when component unmounts or when isSubmitting changes
		return () => {
			if (interval) clearInterval(interval);
		};
	}, [isSubmitting]);

	// Update assistant message based on current question
	useEffect(() => {
		if (questions.length > 0 && currentQuestionIndex < questions.length) {
			const messages = [
				"This helps me understand your preferences better.",
				"Great question! Your answer will help personalize your experience.",
				"I'm learning more about how you work with each answer.",
				"This information helps me tailor the experience to your needs."
			];
			setAssistantMessage(messages[currentQuestionIndex % messages.length]);
		} else if (showSummary) {
			setAssistantMessage("Here's a summary of your choices. Look good?");
		}
	}, [currentQuestionIndex, questions.length, showSummary]);

	const handleOptionSelect = (question: string, option: string) => {
		setAnswer(question, option);
	};

	const goToNextQuestion = () => {
		if (currentQuestionIndex < questions.length - 1) {
			setCurrentQuestionIndex(prev => prev + 1);
		} else {
			setShowSummary(true);
		}
	};

	const goToPreviousQuestion = () => {
		if (currentQuestionIndex > 0) {
			setCurrentQuestionIndex(prev => prev - 1);
		}
	};

	const handleSubmit = async () => {
		try {
			setIsSubmitting(true);
			setLoadingMessageIndex(0); // Start with the first message

			// Check if all questions are answered
			const areAllQuestionsAnswered = questions.every((q) => answers[q.question]);

			if (!areAllQuestionsAnswered) {
				toast.error('Please answer all questions before submitting');
				setIsSubmitting(false);
				return;
			}

			// Save answers and other onboarding data to localStorage
			const emailRatings = JSON.parse(localStorage.getItem('emailRatings') || '{}');
			const ratedEmails = JSON.parse(localStorage.getItem('ratedEmails') || '[]');
			// Prepare the onboarding data to send to the backend
			const onboardingData: OnboardingFormData = {
				questions: questions,
				answers: answers,
				domain: domain,
				emailRatings: emailRatings,
				ratedEmails: ratedEmails
			};

			console.log('Submitting onboarding data to backend:', {
				questions: questions.length,
				answers: Object.keys(answers).length,
				domain,
				emailRatings: Object.keys(emailRatings).length,
				ratedEmails: ratedEmails.length
			});
			const response = await OnboardingService.submitOnboardingData(onboardingData);

			console.log('Onboarding submission response:', response);
			
			if (response.error) {
				const errorMessage = typeof response.error === 'string' 
					? response.error 
					: response.error.message || 'Failed to save preferences';
				console.error('Onboarding submission error:', errorMessage);
				toast.error(errorMessage);
				setIsSubmitting(false);
				return;
			}

			setIsCompleted(true);
			toast.success('Profile information saved successfully!');

			// Show loading UI for 20 seconds before redirecting
			// The loading messages will cycle automatically due to the useEffect
			setTimeout(() => {
				router.push('/app/dashboard');
			}, 20000);
		} catch (error) {
			console.error('Error submitting onboarding answers:', error);
			toast.error('Failed to save information. Please try again.');
			setIsSubmitting(false);
		}
	};

	if (isLoading || isSubmitting) {
		return (
			<LoadingScreen 
				message={isSubmitting ? loadingMessages[loadingMessageIndex] : "Loading your questions..."} 
				isSubmitting={isSubmitting}
			/>
		);
	}

	return (
		<div className='flex min-h-screen items-center justify-center p-4 bg-gradient-to-r from-[#e6dcda] via-[#cfc6cb] to-[#ced4d8]'>
			<motion.div
				initial={{ opacity: 0, y: 20 }}
				animate={{ opacity: 1, y: 0 }}
				transition={{ duration: 0.5, ease: 'easeOut' }}
				className='w-full max-w-xl'
			>
				<div className='overflow-hidden rounded-3xl bg-white/40 shadow-sm backdrop-blur-sm'>
					<div className='border-b border-gray-100 px-8 py-6 flex justify-between items-center'>
						<h2 className='text-2xl font-semibold text-gray-800'>You are,</h2>
						<ProgressBar 
							currentQuestionIndex={currentQuestionIndex}
							totalQuestions={questions.length}
							showSummary={showSummary}
						/>
					</div>

					<div className='p-8'>
						<div className='space-y-8'>
							{/* Assistant component */}
							<OnboardingAssistant 
								message={assistantMessage}
								currentQuestionIndex={currentQuestionIndex}
								totalQuestions={questions.length}
								isShowingSummary={showSummary}
							/>

							{/* Questions or Summary */}
							<AnimatePresence mode="wait">
								{!showSummary && questions.length > 0 && (
									<QuestionCard
										key={`question-${currentQuestionIndex}`}
										question={questions[currentQuestionIndex]}
										selectedAnswer={answers[questions[currentQuestionIndex]?.question]}
										onSelectOption={handleOptionSelect}
									/>
								)}

								{showSummary && (
									<SummaryView 
										questions={questions} 
										answers={answers} 
									/>
								)}
							</AnimatePresence>

							{/* Navigation Buttons */}
							<NavigationButtons 
								currentQuestionIndex={currentQuestionIndex}
								totalQuestions={questions.length}
								showSummary={showSummary}
								isSubmitting={isSubmitting}
								hasCurrentAnswer={!!answers[questions[currentQuestionIndex]?.question]}
								onPrevious={goToPreviousQuestion}
								onNext={goToNextQuestion}
								onSubmit={handleSubmit}
								onEditAnswers={() => setShowSummary(false)}
							/>
						</div>
					</div>
				</div>
			</motion.div>
		</div>
	);
};

export default OnboardingPage;
