import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { CheckCircle } from 'lucide-react';
import { QuestionWithOptions } from '@/types/agent';

interface QuestionCardProps {
	question: QuestionWithOptions;
	selectedAnswer: string | undefined;
	onSelectOption: (question: string, option: string) => void;
}

export const QuestionCard = ({ question, selectedAnswer, onSelectOption }: QuestionCardProps) => {
	return (
		<motion.div
			initial={{ opacity: 0, x: 20 }}
			animate={{ opacity: 1, x: 0 }}
			exit={{ opacity: 0, x: -20 }}
			transition={{ duration: 0.3 }}
			className='space-y-6'
		>
			<h3 className='font-medium sm:text-lg'>{question.question}</h3>
			<div className='grid grid-cols-1 gap-4 sm:grid-cols-2'>
				{question.options.map((option: string, optIndex: number) => (
					<motion.div
						key={optIndex}
						whileHover={{ scale: 1.03 }}
						whileTap={{ scale: 0.97 }}
						transition={{ type: 'spring', stiffness: 400, damping: 17 }}
					>
						<Button
							variant='outline'
							className={`h-14 w-full rounded-xl border text-base font-medium ${
								selectedAnswer === option ? 'border-foreground' : ''
							}`}
							onClick={() => onSelectOption(question.question, option)}
						>
							<span className='block truncate px-2' title={option}>
								{option}
							</span>
						</Button>
					</motion.div>
				))}
			</div>
		</motion.div>
	);
};

export default QuestionCard;
