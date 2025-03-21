import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useOnboardingStore } from '@/store/onboarding.store';
import { AgentService } from '@/services/agent.service';
import { toast } from 'sonner';
import { useRouter } from 'next/navigation';
import { QuestionCard } from './QuestionCard';
import { SummaryView } from './SummaryView';
import { NavigationButtons } from './NavigationButtons';
import { ProgressBar } from './ProgressBar';
import { LoadingScreen } from './LoadingScreen';

export const QuestionsStep = () => {
	const router = useRouter();
	const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
	const [showSummary, setShowSummary] = useState(false);
	const [isLoading, setIsLoading] = useState(true);

	const {
		questions,
		answers,
		emailRatings,
		userEmail,
		setQuestions,
		currentStep,
		ratedEmails,
		setAnswer,
		setCurrentStep,
	} = useOnboardingStore();

	const fetchDomainInference = useCallback(async () => {
		console.log('fetchDomainInference', questions.length);
		if (!userEmail || questions.length > 0 || currentStep !== 'questions') {
			setIsLoading(false);
			return;
		}
		setIsLoading(true);
		try {
			const response = await AgentService.inferDomain(userEmail, ratedEmails, emailRatings);

			if (response.error) {
				console.error('Domain inference error:', response.error);
				toast.error('Failed to load onboarding questions. Please try again.');
				router.push('/app/dashboard');
				return;
			}

			if (response.data) {
				setQuestions(response.data.questions || []);
			}
		} catch (error) {
			console.error('Error fetching domain inference:', error);
			toast.error('Failed to load onboarding questions. Please try again.');
			router.push('/app');
		} finally {
			setIsLoading(false);
		}
	}, [currentStep, emailRatings, ratedEmails, router, setQuestions, userEmail]);

	useEffect(() => {
		fetchDomainInference();
	}, [fetchDomainInference]);

	const handleOptionSelect = (question: string, option: string) => {
		setAnswer(question, option);
	};

	const goToNextQuestion = () => {
		if (currentQuestionIndex < questions.length - 1) {
			setCurrentQuestionIndex((prev) => prev + 1);
		} else {
			setShowSummary(true);
		}
	};

	const goToPreviousQuestion = () => {
		if (currentQuestionIndex > 0) {
			setCurrentQuestionIndex((prev) => prev - 1);
		}
	};

	const handleComplete = async () => {
		try {
			const areAllQuestionsAnswered = questions.every((q) => answers[q.question]);
			if (!areAllQuestionsAnswered) {
				toast.error('Please answer all questions before submitting');
				return;
			}
			setCurrentStep('reviewPersonality');
		} catch (error) {
			console.error('Error submitting onboarding answers:', error);
			toast.error('Failed to save information. Please try again.');
		}
	};

	if (isLoading) {
		return <LoadingScreen message={'Creating your personalized dashboard...'} />;
	}

	return (
		<div className='flex min-h-screen items-center justify-center p-3'>
			<motion.div
				initial={{ opacity: 0, y: 20 }}
				animate={{ opacity: 1, y: 0 }}
				transition={{ duration: 0.5, ease: 'easeOut' }}
				className='w-full max-w-xl'
			>
				<div className='rounded-3xl bg-background/80 shadow-sm backdrop-blur-sm'>
					<div className='flex items-center justify-between border-b px-8 py-6'>
						<h2 className='text-lg font-semibold sm:text-2xl'>You are ,</h2>
						<ProgressBar
							currentQuestionIndex={currentQuestionIndex}
							totalQuestions={questions.length}
							showSummary={showSummary}
						/>
					</div>

					<div className='p-4 sm:p-6'>
						<div className='space-y-8'>
							<AnimatePresence mode='wait'>
								{!showSummary && questions.length > 0 && (
									<QuestionCard
										key={`question-${currentQuestionIndex}`}
										question={questions[currentQuestionIndex]}
										selectedAnswer={answers[questions[currentQuestionIndex]?.question]}
										onSelectOption={handleOptionSelect}
									/>
								)}

								{showSummary && <SummaryView questions={questions} answers={answers} />}
							</AnimatePresence>

							<NavigationButtons
								currentQuestionIndex={currentQuestionIndex}
								totalQuestions={questions.length}
								showSummary={showSummary}
								hasCurrentAnswer={!!answers[questions[currentQuestionIndex]?.question]}
								onPrevious={goToPreviousQuestion}
								onNext={goToNextQuestion}
								onSubmit={handleComplete}
								onEditAnswers={() => setShowSummary(false)}
							/>
						</div>
					</div>
				</div>
			</motion.div>
		</div>
	);
};
