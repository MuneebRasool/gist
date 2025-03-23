'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { useOnboardingStore } from '@/store/onboarding.store';
import { EmailRatingStep } from '@/components/app/onboarding/EmailRatingStep';
import { QuestionsStep } from '@/components/app/onboarding/QuestionsStep';
import { LoadingScreen } from '@/components/app/onboarding/LoadingScreen';
import { ReviewPersonalityStep } from '@/components/app/onboarding/ReviewPersonalityStep';
import CompletedStep from '@/components/app/onboarding/CompletedStep';

export default function OnboardingPage() {
	const searchParams = useSearchParams();
	const { currentStep, setUserEmail } = useOnboardingStore();
	const [isLoading, setIsLoading] = useState(true);

	// Handle URL params
	useEffect(() => {
		const emailFromParams = searchParams.get('email');
		if (emailFromParams) {
			setUserEmail(emailFromParams);
		}
		setIsLoading(false);
	}, [searchParams, setUserEmail]);

	if (isLoading) {
		return <LoadingScreen message='Loading...' />;
	}

	// Render appropriate step based on current step in store
	if (currentStep === 'email-rating') {
		return <EmailRatingStep />;
	}

	if (currentStep === 'questions') {
		return <QuestionsStep />;
	}

	if (currentStep === 'reviewPersonality' || 'task_generation') {
		return <ReviewPersonalityStep />;
	}

	if (currentStep === 'completed') {
		return <CompletedStep />;
	}

	return null;
}
