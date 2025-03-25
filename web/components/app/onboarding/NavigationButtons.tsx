import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { ArrowLeft, ArrowRight, CheckCircle, Loader2 } from 'lucide-react';

interface NavigationButtonsProps {
	currentQuestionIndex: number;
	totalQuestions: number;
	showSummary: boolean;
	hasCurrentAnswer: boolean;
	onPrevious: () => void;
	onNext: () => void;
	onSubmit: () => void;
	onEditAnswers: () => void;
}

export const NavigationButtons = ({
	currentQuestionIndex,
	totalQuestions,
	showSummary,
	hasCurrentAnswer,
	onPrevious,
	onNext,
	onSubmit,
	onEditAnswers,
}: NavigationButtonsProps) => {
	return (
		<div className='flex items-center gap-4 pt-4'>
			{!showSummary && (
				<motion.div
					whileHover={{ scale: 1.02 }}
					whileTap={{ scale: 0.98 }}
					className={`${currentQuestionIndex === 0 ? 'hidden' : ''}`}
				>
					<Button
						onClick={onPrevious}
						variant='outline'
						className='h-12 items-center gap-2 rounded-xl font-medium transition-all duration-300'
					>
						<ArrowLeft size={18} />
						Back
					</Button>
				</motion.div>
			)}

			{!showSummary ? (
				<motion.div
					whileHover={hasCurrentAnswer ? { scale: 1.02 } : {}}
					whileTap={hasCurrentAnswer ? { scale: 0.98 } : {}}
					className='flex-1'
				>
					<Button
						onClick={onNext}
						disabled={!hasCurrentAnswer}
						className={`h-12 w-full flex-1 items-center gap-2 rounded-xl text-base font-medium transition-all duration-300`}
					>
						{currentQuestionIndex === totalQuestions - 1 ? 'Next Step' : 'Continue'}
						<ArrowRight size={18} />
					</Button>
				</motion.div>
			) : (
				<>
					<motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
						<Button
							onClick={onEditAnswers}
							variant='outline'
							className='h-12 items-center gap-2 rounded-xl text-base font-medium transition-all duration-300'
						>
							<ArrowLeft size={18} />
							Edit Answers
						</Button>
					</motion.div>
					<motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} className='flex-1'>
						<Button
							onClick={onSubmit}
							className='h-12 w-full items-center gap-2 rounded-xl text-base font-medium transition-all duration-300'
						>
							Complete Setup
							<CheckCircle size={18} className='text-green-500' />
						</Button>
					</motion.div>
				</>
			)}
		</div>
	);
};

export default NavigationButtons;
