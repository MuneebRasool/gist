'use client';

import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { OnboardingService, OnboardingStatusEvent } from '@/services/agent/onboarding.service';
import { useOnboardingStore } from '@/store/onboarding.store';
import { useCallback, useEffect, useState, useRef } from 'react';
import { LoadingScreen } from './LoadingScreen';
import { UserService } from '@/services/user.service';
import { useRouter } from 'next/navigation';
import { useSession } from 'next-auth/react';
import { toast } from 'sonner';

export function ReviewPersonalityStep() {
	const {
		summary,
		setSummary,
		currentStep,
		resetState,
		setCurrentStep,
		questions,
		answers,
		domain,
		emailRatings,
		ratedEmails,
	} = useOnboardingStore();
	const { update } = useSession();
	const [isLoading, setIsLoading] = useState(true);
	const [newSummary, setNewSummary] = useState(summary);
	const [isSubmitting, setIsSubmitting] = useState(false);
	const [loadingMessage, setLoadingMessage] = useState('Checking onboarding status...');
	const [isProcessing, setIsProcessing] = useState(false);
	const [connectionError, setConnectionError] = useState<string | null>(null);
	const eventSourceRef = useRef<EventSource | null>(null);
	const isCheckingRef = useRef<boolean>(false);
	const isComponentMounted = useRef<boolean>(true);
	const router = useRouter();

	const redirectToDashboard = useCallback(() => {
		update({ onboarding: true });
		resetState();
		router.push('/app/dashboard');
		setCurrentStep('completed');
	}, [update, resetState, router, setCurrentStep]);

	const fetchPersonalityData = useCallback(async () => {
		if (currentStep !== 'reviewPersonality' || summary) {
			if (isComponentMounted.current) {
				setIsLoading(false);
			}
			return;
		}
		
		try {
			setLoadingMessage('Fetching personality data...');
			const onboardingData = {
				questions,
				answers,
				domain: domain || '',
				emailRatings,
				ratedEmails: ratedEmails || [],
			};

			const response = await OnboardingService.submitOnboardingData(onboardingData);
			if (response.data && isComponentMounted.current) {
				setSummary(response.data.personalitySummary ?? 'Personality Summary');
				setNewSummary(response.data.personalitySummary ?? 'Personality Summary');
			}
		} catch (error) {
			console.error('Error fetching personality data:', error);
			toast.error('Failed to load personality data');
		} finally {
			if (isComponentMounted.current) {
				setIsLoading(false);
			}
		}
	}, [answers, currentStep, domain, emailRatings, questions, ratedEmails, setSummary, summary]);

	const handleStatusUpdate = useCallback((data: OnboardingStatusEvent) => {
		if (!isComponentMounted.current) return;

		console.log('Received status update:', data);
		setConnectionError(null);

		switch (data.status) {
			case 'completed':
				if (eventSourceRef.current) {
					eventSourceRef.current.close();
					eventSourceRef.current = null;
				}
				setCurrentStep('completed');
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
	}, [redirectToDashboard, setCurrentStep]);

	const startStatusStream = useCallback(async () => {
		if (!isComponentMounted.current) return;

		// Close existing connection if any
		if (eventSourceRef.current) {
			eventSourceRef.current.close();
			eventSourceRef.current = null;
		}

		try {
			const eventSource = await OnboardingService.createStatusStream(
				handleStatusUpdate,
				(error) => {
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
				}
			);

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

	const checkOnboardingStatus = useCallback(async () => {
		if (!isComponentMounted.current || isCheckingRef.current) return;

		try {
			isCheckingRef.current = true;
			setLoadingMessage('Checking onboarding status...');
			
			const result = await OnboardingService.checkOnboardingStatus();

			if (result.data?.success && isComponentMounted.current) {
				// If onboarding is complete, redirect to dashboard
				if (result.data.onboarding && !result.data.task_gen) {
					redirectToDashboard();
					return;
				}
				
				// If we're in task_generation step or tasks are being generated, show the loading screen
				if (currentStep === 'task_generation' || result.data.in_progress) {
					setIsProcessing(true);
					setLoadingMessage('Extracting Tasks...');
					
					// Only start a new SSE stream if one doesn't already exist
					if (!eventSourceRef.current) {
						await startStatusStream();
					}
					return;
				}
				
				// Otherwise, fetch personality data if needed
				await fetchPersonalityData();
			}
		} catch (error) {
			console.error('Error checking onboarding status:', error);
			if (isComponentMounted.current) {
				toast.error('Failed to check onboarding status');
				setIsLoading(false);
			}
		} finally {
			isCheckingRef.current = false;
		}
	}, [redirectToDashboard, startStatusStream, fetchPersonalityData, currentStep]);

	const onComplete = useCallback(async () => {
		if (!isComponentMounted.current) return;

		setIsSubmitting(true);
		setLoadingMessage('Starting onboarding process...');
		setConnectionError(null);

		try {
			// First update the personality if needed
			if (newSummary !== summary) {
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
	}, [newSummary, summary, setSummary, startStatusStream, setCurrentStep]);

	// Initialize component - check onboarding status on mount
	useEffect(() => {
		isComponentMounted.current = true;
		
		// Initial load - always check onboarding status first
		checkOnboardingStatus();

		return () => {
			isComponentMounted.current = false;
			if (eventSourceRef.current) {
				eventSourceRef.current.close();
				eventSourceRef.current = null;
			}
		};
	}, [checkOnboardingStatus]);

	if (isLoading || isSubmitting || isProcessing) {
		return <LoadingScreen message={loadingMessage} />;
	}

	if (connectionError) {
		return (
			<div className='flex h-full flex-col items-center justify-center'>
				<div className='flex max-w-3xl w-full flex-col items-center justify-center gap-6 rounded-xl bg-white/80 p-4 backdrop-blur-sm sm:p-8'>
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
			<div className='flex max-w-3xl w-full flex-col items-center justify-center gap-6 rounded-xl bg-white/80 p-4 backdrop-blur-sm sm:p-8'>
				<h2 className='text-center text-2xl font-bold'>Review Your Personality Summary</h2>
				<p className='text-center text-muted-foreground'>Please review and edit your personality summary if needed</p>

				<Textarea
					value={newSummary}
					onChange={(e) => setNewSummary(e.target.value)}
					className='min-h-[400px] w-full text-base p-4'
					placeholder='Your personality summary will appear here...'
				/>

				<Button className='w-full max-w-md' onClick={onComplete}>
					All Looks Good 👍
				</Button>
			</div>
		</div>
	);
}
