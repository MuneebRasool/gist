import { Progress } from '@/components/ui/progress';

interface ProgressBarProps {
	currentQuestionIndex: number;
	totalQuestions: number;
	showSummary: boolean;
}

export const ProgressBar = ({ currentQuestionIndex, totalQuestions, showSummary }: ProgressBarProps) => {
	const progressPercentage =
		totalQuestions > 0 ? (showSummary ? 100 : ((currentQuestionIndex + 1) / totalQuestions) * 100) : 0;

	return (
		<div className='flex items-center gap-2'>
			<Progress value={progressPercentage} className='h-2 w-24' />
			<span className='text-sm text-gray-500'>
				{showSummary ? 'Review' : `${currentQuestionIndex + 1}/${totalQuestions}`}
			</span>
		</div>
	);
};

export default ProgressBar;
