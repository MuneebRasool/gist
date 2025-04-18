import { useEffect, useState } from 'react';
import { toast } from 'sonner';
import { AnimatePresence } from 'framer-motion';
import { Email } from '@/types/nylasEmail';
import { useOnboardingStore } from '@/store/onboarding.store';
import EmailCard from './EmailCard';
import QuestionPrompt from './QuestionPrompt';
import ProgressIndicator from './ProgressIndicator';
import { LoadingScreen } from './LoadingScreen';
import NoEmail from './EmailTriage/NoEmail';
import { EmailMessage } from '@/services/nylas/email.service';

interface EmailRatingStepProps {
	emails: EmailMessage[];
}

export const EmailRatingStep = ({ emails }: EmailRatingStepProps) => {
	const [currentEmailIndex, setCurrentEmailIndex] = useState(0);
	const { emailRatings, setEmailRatings, setRatedEmails, setCurrentStep } = useOnboardingStore();

	// Initialize email ratings if needed
	useEffect(() => {
		if (emails.length > 0 && Object.keys(emailRatings).length === 0) {
			const initialRatings: Record<string, number> = {};
			emails.forEach((email) => {
				initialRatings[email.id] = 3;
			});
			setEmailRatings(initialRatings);
		}
	}, [emails, emailRatings, setEmailRatings]);

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
		}
	};

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
