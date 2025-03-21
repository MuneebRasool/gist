import { motion } from 'framer-motion';

interface ProgressIndicatorProps {
	currentIndex: number;
	totalEmails: number;
}

export default function ProgressIndicator({ currentIndex, totalEmails }: ProgressIndicatorProps) {
	return (
		<div className='mt-5 flex max-w-lg justify-center text-sm font-medium text-muted-foreground'>
			Email {currentIndex + 1} of {totalEmails}
		</div>
	);
}
