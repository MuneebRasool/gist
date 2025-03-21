import { motion } from 'framer-motion';
import { QuestionWithOptions } from '@/types/agent';

interface SummaryViewProps {
	questions: QuestionWithOptions[];
	answers: Record<string, string>;
}

export const SummaryView = ({ questions, answers }: SummaryViewProps) => {
	return (
		<motion.div
			key='summary'
			initial={{ opacity: 0, y: 20 }}
			animate={{ opacity: 1, y: 0 }}
			exit={{ opacity: 0, y: -20 }}
			className='space-y-6'
		>
			<h3 className='text-lg font-medium'>Your Profile Summary</h3>
			<div className='space-y-4 rounded-xl'>
				{questions.map((question, index) => (
					<div key={index} className='flex items-center justify-between gap-4 border-b pb-2 last:border-0 last:pb-0'>
						<p className='text-sm text-muted-foreground'>{question.question}</p>
						<p className='text-sm font-medium'>{answers[question.question]}</p>
					</div>
				))}
			</div>
		</motion.div>
	);
};

export default SummaryView;
