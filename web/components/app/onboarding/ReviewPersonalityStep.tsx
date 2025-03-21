'use client';

import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { OnboardingService } from '@/services/agent/onboarding.service';
import { useOnboardingStore } from '@/store/onboarding.store';
import { useCallback, useEffect, useState } from 'react';
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
	const [isLoading, setIsLoading] = useState(false);
	const [newSummary, setNewSummary] = useState(summary);
	const [isSubmitting, setIsSubmitting] = useState(false);
	const router = useRouter();

	const fetchData = useCallback(async () => {
		if (currentStep !== 'reviewPersonality' || summary) {
			return;
		}
		setIsLoading(true);
		const onboardingData = {
			questions,
			answers,
			domain: domain || '',
			emailRatings,
			ratedEmails: ratedEmails || [],
		};

		const response = await OnboardingService.submitOnboardingData(onboardingData);
		console.log(response);
		if (response.data) {
			setSummary(response.data.personalitySummary ?? 'Personality Summary');
			setNewSummary(response.data.personalitySummary ?? 'Personality Summary');
		}
		setIsLoading(false);
	}, [answers, currentStep, domain, emailRatings, questions, ratedEmails, setSummary, summary]);

	const onComplete = useCallback(async () => {
		setIsSubmitting(true);
		if (newSummary !== summary) {
			setSummary(newSummary);
			const response = await UserService.updateUserPersonality([newSummary]);
		}
		const res = await OnboardingService.startOnboarding();
		if (res.data) {
			update({ onboarding: true });
			resetState();
			router.push('/app/dashboard');
			setCurrentStep('completed');
		} else {
			toast.error('Failed to start onboarding. Please try again.');
		}
		setIsSubmitting(false);
	}, [newSummary, summary, setSummary, update, resetState, router, setCurrentStep]);

	useEffect(() => {
		fetchData();
	}, [fetchData]);

	if (isLoading) {
		return <LoadingScreen message='Loading...' />;
	}
	if (isSubmitting) {
		return <LoadingScreen message='Extracting Tasks...' />;
	}

	return (
		<div className='flex h-full flex-col items-center justify-center'>
			<div className='flex max-w-2xl flex-col items-center justify-center gap-6 rounded-xl bg-white/80 p-4 backdrop-blur-sm sm:p-8'>
				<h2 className='text-center text-2xl font-bold'>Review Your Personality Summary</h2>
				<p className='text-center text-muted-foreground'>Please review and edit your personality summary if needed</p>

				<Textarea
					value={newSummary}
					onChange={(e) => setNewSummary(e.target.value)}
					className='min-h-[200px] w-full'
					placeholder='Your personality summary will appear here...'
				/>

				<Button className='w-full max-w-md' onClick={onComplete}>
					All Looks Good 👍
				</Button>
			</div>
		</div>
	);
}
