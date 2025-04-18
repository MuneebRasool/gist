'use client';

import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { OnboardingService, OnboardingStatusEvent } from '@/services/agent/onboarding.service';
import { useOnboardingStore } from '@/store/onboarding.store';
import { useState, useRef, useCallback, useEffect } from 'react';
import { LoadingScreen } from './LoadingScreen';
import { UserService } from '@/services/user.service';
import { useRouter } from 'next/navigation';
import { useSession } from 'next-auth/react';
import { toast } from 'sonner';

interface ReviewPersonalityStepProps {
	personalitySummary: string;
}

export function ReviewPersonalityStep({ personalitySummary }: ReviewPersonalityStepProps) {
	const { setSummary, currentStep, setCurrentStep, questions, answers, domain, emailRatings, ratedEmails } =
		useOnboardingStore();
	const { update } = useSession();
	const [isLoading, setIsLoading] = useState(false); // Start with not loading since we get summary from props
	const [newSummary, setNewSummary] = useState(personalitySummary);
	const [isSubmitting, setIsSubmitting] = useState(false);
	const [loadingMessage, setLoadingMessage] = useState('');
	const [isProcessing, setIsProcessing] = useState(false);
	const [connectionError, setConnectionError] = useState<string | null>(null);
	const eventSourceRef = useRef<EventSource | null>(null);
	const isComponentMounted = useRef<boolean>(true);
	const router = useRouter();

	const redirectToDashboard = useCallback(() => {
		update({ onboarding: true });
		setCurrentStep('completed');
		localStorage.removeItem('onboarding-storage');

		router.push('/app/dashboard');
	}, [update, setCurrentStep, router]);

	const handleStatusUpdate = useCallback(
		(data: OnboardingStatusEvent) => {
			if (!isComponentMounted.current) return;

			console.log('Received status update:', data);
			setConnectionError(null);

			switch (data.status) {
				case 'completed':
					if (eventSourceRef.current) {
						eventSourceRef.current.close();
						eventSourceRef.current = null;
					}
					redirectToDashboard();
					setIsProcessing(false);
					break;
				case 'processing':
					setIsProcessing(true);
					setLoadingMessage('Extracting Tasks...');
					break;
				case 'error':
					setConnectionError(data.message || 'Connection error occurred');
					toast.error(data.message || 'Connection error occurred');
					if (isComponentMounted.current) {
						setIsLoading(false);
						setIsProcessing(false);
					}
					break;
			}
		},
		[redirectToDashboard]
	);

	const startStatusStream = useCallback(async () => {
		if (!isComponentMounted.current) return;

		// Close existing connection if any
		if (eventSourceRef.current) {
			OnboardingService.closeStatusStream(eventSourceRef.current);
			eventSourceRef.current = null;
		}

		try {
			const eventSource = await OnboardingService.createStatusStream(handleStatusUpdate, (error) => {
				console.error('SSE Error:', error);
				if (isComponentMounted.current) {
					// When an SSE error occurs, first check if onboarding is already complete
					// before showing the connection error
					OnboardingService.checkOnboardingStatus()
						.then((result) => {
							if (result.data?.success) {
								if (result.data.onboarding && !result.data.task_gen) {
									// Onboarding is actually complete, just redirect
									redirectToDashboard();
									return;
								}
							}
							// If we get here, onboarding is not complete, so show the error
							setConnectionError('Connection error. Please try refreshing the page.');
							toast.error('Connection error. Please try refreshing the page.');
							setIsLoading(false);
							setIsProcessing(false);
						})
						.catch(() => {
							// If status check also fails, then show the connection error
							setConnectionError('Connection error. Please try refreshing the page.');
							toast.error('Connection error. Please try refreshing the page.');
							setIsLoading(false);
							setIsProcessing(false);
						});
				}
			});

			eventSourceRef.current = eventSource;
			return eventSource;
		} catch (error) {
			console.error('Failed to create status stream:', error);
			if (isComponentMounted.current) {
				// When we fail to create the SSE stream, check if onboarding is already complete
				try {
					const result = await OnboardingService.checkOnboardingStatus();
					if (result.data?.success && result.data.onboarding && !result.data.task_gen) {
						// Onboarding is actually complete, just redirect
						redirectToDashboard();
						return null;
					}
				} catch {
					// Ignore error from status check and continue with connection error
				}

				setConnectionError('Failed to connect to server. Please try refreshing the page.');
				toast.error('Failed to connect to server. Please try refreshing the page.');
				setIsLoading(false);
				setIsProcessing(false);
			}
			return null;
		}
	}, [handleStatusUpdate, redirectToDashboard]);

	// Check status on initial load if we're in task_generation step
	useEffect(() => {
		isComponentMounted.current = true;

		// If we're already in task_generation step, start the status stream
		if (currentStep === 'task_generation') {
			setIsProcessing(true);
			setLoadingMessage('Extracting Tasks...');
			startStatusStream();
		}

		return () => {
			isComponentMounted.current = false;
			if (eventSourceRef.current) {
				eventSourceRef.current.close();
				eventSourceRef.current = null;
			}
		};
	}, [currentStep, startStatusStream]);

	const onComplete = useCallback(async () => {
		if (!isComponentMounted.current) return;

		setIsSubmitting(true);
		setLoadingMessage('Starting onboarding process...');
		setConnectionError(null);

		try {
			// First update the personality if needed
			if (newSummary !== personalitySummary) {
				setSummary(newSummary);
				await UserService.updateUserPersonality([newSummary]);
			}

			// Check if onboarding is already in progress before starting it again
			const statusCheck = await OnboardingService.checkOnboardingStatus();

			// Set the current step to task_generation
			setCurrentStep('task_generation');

			// Only start onboarding if it's not already in progress
			if (!statusCheck.data?.in_progress) {
				const res = await OnboardingService.startOnboarding();
				if (!res.data) {
					throw new Error('Failed to start onboarding');
				}
			}

			// In either case, start the status stream to monitor progress
			if (isComponentMounted.current) {
				setIsProcessing(true);
				startStatusStream();
				setLoadingMessage('Extracting Tasks...');
			}
		} catch (error) {
			console.error('Error starting onboarding:', error);
			if (isComponentMounted.current) {
				toast.error('Failed to start onboarding. Please try again.');
				setIsSubmitting(false);
				// Set the step back if there was an error
				setCurrentStep('reviewPersonality');
			}
		}
	}, [newSummary, personalitySummary, setSummary, startStatusStream, setCurrentStep]);

	if (isLoading || isSubmitting || isProcessing) {
		return <LoadingScreen message={loadingMessage} />;
	}

	if (connectionError) {
		return (
			<div className='flex h-full flex-col items-center justify-center'>
				<div className='flex w-full max-w-3xl flex-col items-center justify-center gap-6 rounded-xl bg-background/80 p-4 backdrop-blur-sm sm:p-8'>
					<h2 className='text-center text-2xl font-bold text-red-500'>Connection Error</h2>
					<p className='text-center text-muted-foreground'>{connectionError}</p>
					<Button className='w-full max-w-md' onClick={() => window.location.reload()}>
						Retry
					</Button>
				</div>
			</div>
		);
	}

	return (
		<div className='flex h-full flex-col items-center justify-center'>
			<div className='flex w-full max-w-3xl flex-col items-center justify-center gap-6 rounded-xl bg-background/80 p-4 backdrop-blur-sm sm:p-8'>
				<h2 className='text-center text-2xl font-bold'>Review Your Personality Summary</h2>
				<p className='text-center text-muted-foreground'>Please review and edit your personality summary if needed</p>

				<Textarea
					value={newSummary}
					onChange={(e) => setNewSummary(e.target.value)}
					className='min-h-[400px] w-full p-4 text-base'
					placeholder='Your personality summary will appear here...'
				/>

				<Button className='w-full max-w-md' onClick={onComplete}>
					All Looks Good 👍
				</Button>
			</div>
		</div>
	);
}
