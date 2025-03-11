'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { AgentService } from '@/services/agent.service';
import { QuestionWithOptions } from '@/types/agent';
import { useOnboardingStore } from '@/store/onboarding.store';
import { Button } from '@/components/ui/button';
import { Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import { motion, AnimatePresence } from 'framer-motion';
import { OnboardingService, OnboardingFormData, SimplifiedEmail } from '@/services/agent/onboarding.service';

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
	
					// Set summary based on response data
					let generatedSummary =
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
	}, [isSubmitting, loadingMessages.length]);

	const handleOptionSelect = (question: string, option: string) => {
		setAnswer(question, option);
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
		  <div className="fixed inset-0 z-50 flex items-center justify-center bg-gradient-to-r from-[#e6dcda] via-[#cfc6cb] to-[#ced4d8]">
			<div className="flex flex-col items-center justify-center space-y-8">
			  <div className="relative">
				<div className="h-12 w-12 animate-spin rounded-full border-4 border-[#A5B7C8]/30 border-t-[#A5B7C8]" />
			  </div>
			  <p className="text-lg font-medium text-gray-600">
				{isSubmitting ? loadingMessages[loadingMessageIndex] : "Loading your questions..."}
			  </p>
			</div>
		  </div>
		);
	}
	

	return (
		<div className='flex min-h-screen items-center justify-center p-4'>
			<motion.div
				initial={{ opacity: 0, y: 20 }}
				animate={{ opacity: 1, y: 0 }}
				transition={{ duration: 0.5, ease: 'easeOut' }}
				className='w-full max-w-xl'
			>
				<div className='overflow-hidden rounded-3xl bg-white/40 shadow-sm backdrop-blur-sm'>
					<div className='border-b border-gray-100 px-8 py-6'>
						<h2 className='text-2xl font-semibold text-gray-800'>You are,</h2>
					</div>

					<div className='p-8'>
						<div className='space-y-8'>
							<AnimatePresence>
								{questions.map((question: QuestionWithOptions, index: number) => (
									<motion.div
										key={index}
										initial={{ opacity: 0, y: 15 }}
										animate={{ opacity: 1, y: 0 }}
										transition={{ delay: 0.1 * (index + 1) }}
										className='space-y-4'
									>
										<h3 className='text-base font-medium text-gray-700'>{question.question}</h3>
										<div className='grid grid-cols-2 gap-4'>
											{question.options.map((option: string, optIndex: number) => (
												<motion.div key={optIndex} whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
													<Button
														variant='outline'
														className={`h-14 w-full rounded-xl border text-base font-medium transition-all duration-200 ${
															answers[question.question] === option
																? 'border-gray-400 bg-gray-50 text-gray-900'
																: 'border-gray-200 bg-white text-gray-600 hover:border-gray-300 hover:bg-gray-50/50'
														}`}
														onClick={() => handleOptionSelect(question.question, option)}
													>
														<span className='block truncate px-2' title={option}>
															{option}
														</span>
													</Button>
												</motion.div>
											))}
										</div>
									</motion.div>
								))}
							</AnimatePresence>

							<div className='mt-10 flex items-center justify-between pt-4'>
								<motion.div
									whileHover={!isSubmitting && questions.every((q) => answers[q.question]) ? { scale: 1.02 } : {}}
									whileTap={!isSubmitting && questions.every((q) => answers[q.question]) ? { scale: 0.98 } : {}}
									className='w-full'
								>
									<Button
										onClick={handleSubmit}
										disabled={isSubmitting || questions.length === 0 || !questions.every((q) => answers[q.question])}
										className={`h-12 w-full rounded-xl text-base font-medium transition-all duration-300 ${
											isSubmitting || questions.length === 0 || !questions.every((q) => answers[q.question])
												? 'bg-gray-100 text-gray-400'
												: 'bg-gray-900 text-white hover:bg-gray-800'
										}`}
									>
										{isSubmitting ? (
											<div className='flex items-center gap-2'>
												<Loader2 className='h-4 w-4 animate-spin' />
												<span>Saving...</span>
											</div>
										) : (
											'Continue'
										)}
									</Button>
								</motion.div>
							</div>
						</div>
					</div>
				</div>
			</motion.div>
		</div>
	);
};

export default OnboardingPage;
