import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useOnboardingStore } from '@/store/onboarding.store';
import { toast } from 'sonner';
import { QuestionCard } from './QuestionCard';
import { NavigationButtons } from './NavigationButtons';
import { ProgressBar } from './ProgressBar';
import { QuestionWithOptions } from '@/types/agent';

interface QuestionsStepProps {
	questions: QuestionWithOptions[];
}

export const QuestionsStep = ({ questions }: QuestionsStepProps) => {
	const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
	const { answers, setAnswer, setCurrentStep } = useOnboardingStore();

	const handleOptionSelect = (question: string, option: string) => {
		setAnswer(question, option);
	};

	const goToNextQuestion = () => {
		const currentQuestion = questions[currentQuestionIndex];
		if (!answers[currentQuestion?.question]) {
			toast.error('Please answer the current question before proceeding');
			return;
		}

		if (currentQuestionIndex < questions.length - 1) {
			setCurrentQuestionIndex((prev) => prev + 1);
		} else {
			handleComplete();
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

	if (questions.length === 0) {
		return (
			<div className='flex min-h-screen items-center justify-center'>
				<div className='rounded-xl bg-background/80 p-6 shadow-sm backdrop-blur-sm'>
					<p className='text-center text-lg text-muted-foreground'>No questions available.</p>
				</div>
			</div>
		);
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
						<ProgressBar
							currentQuestionIndex={currentQuestionIndex}
							totalQuestions={questions.length}
							showSummary={false}
						/>
					</div>

					<div className='p-4 sm:p-6'>
						<div className='space-y-8'>
							<AnimatePresence mode='wait'>
								{questions.length > 0 && (
									<QuestionCard
										key={`question-${currentQuestionIndex}`}
										question={questions[currentQuestionIndex]}
										selectedAnswer={answers[questions[currentQuestionIndex]?.question]}
										onSelectOption={handleOptionSelect}
									/>
								)}
							</AnimatePresence>

							<NavigationButtons
								currentQuestionIndex={currentQuestionIndex}
								totalQuestions={questions.length}
								showSummary={false}
								hasCurrentAnswer={!!answers[questions[currentQuestionIndex]?.question]}
								onPrevious={goToPreviousQuestion}
								onNext={goToNextQuestion}
								onSubmit={handleComplete}
								onEditAnswers={() => {}}
							/>
						</div>
					</div>
				</div>
			</motion.div>
		</div>
	);
};
