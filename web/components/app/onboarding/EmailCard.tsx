import { EmailMessage } from '@/services/nylas/email.service';
import { motion } from 'framer-motion';
import { ChevronRight } from 'lucide-react';
import { useState, useEffect } from 'react';
import { Slider } from '@/components/ui/slider';

interface EmailCardProps {
	email: EmailMessage;
	currentRating: number;
	onRate: (rating: number) => void;
	onNext: () => void;
	isLastEmail: boolean;
}

export default function EmailCard({ email, currentRating = 5, onRate, onNext, isLastEmail }: EmailCardProps) {
	const [isExiting, setIsExiting] = useState(false);
	const [sliderValue, setSliderValue] = useState(currentRating);

	useEffect(() => {
		setSliderValue(currentRating);
	}, [currentRating]);

	const getRatingLabel = (rating: number) => {
		if (rating <= 1) return 'Spam';
		if (rating <= 2) return 'Low Relevance';
		if (rating <= 3) return 'For Later / Keep on File';
		if (rating <= 4) return 'Important';
		return 'Priority';
	};

	const getRatingDescription = (rating: number) => {
		if (rating <= 1) return 'Unwanted, irrelevant, or outright junk';
		if (rating <= 2) return 'Not immediately useful but also not junk';
		if (rating <= 3) return 'Important but not requiring action';
		if (rating <= 4) return 'Needs attention but not urgent';
		return 'Urgent and actionable';
	};

	const handleSliderChange = (value: number[]) => {
		setSliderValue(value[0]);
		onRate(value[0]);
	};

	const cardVariants = {
		initial: { opacity: 0, y: 20 },
		animate: { opacity: 1, y: 0 },
		exit: { opacity: 0, x: -300, transition: { duration: 0.3, ease: 'easeInOut' } },
	};

	const handleNextClick = () => {
		setIsExiting(true);
		setTimeout(() => {
			onNext();
			setIsExiting(false);
		}, 300);
	};

	return (
		<motion.div
			variants={cardVariants}
			initial='initial'
			animate='animate'
			exit='exit'
			className='w-full max-w-3xl rounded-2xl bg-background/80'
		>
			<div className='space-y-6 border-b p-6'>
				<div className='flex'>
					<div className='w-32'>
						<span className='text-base font-bold text-gray-900'>Recipient:</span>
					</div>
					<div className='flex-1'>
						<span className='text-base text-gray-900'>{email.to?.[0]?.email || 'Unknown Recipient'}</span>
					</div>
				</div>

				<div className='flex'>
					<div className='w-32'>
						<span className='text-base font-bold text-gray-900'>Subject:</span>
					</div>
					<div className='flex-1'>
						<span className='text-base text-gray-900'>{email.subject || '(No Subject)'}</span>
					</div>
				</div>

				<div className='flex'>
					<div className='w-32'>
						<span className='text-base font-bold text-gray-900'>Text:</span>
					</div>
					<div className='flex-1'>
						<div className='max-h-[180px] overflow-y-auto text-base leading-relaxed text-gray-900'>{email.body}</div>
					</div>
				</div>
			</div>

			<div className='space-y-5 border-t border-gray-50 p-4'>
				<div className='space-y-3'>
					<div className='text-center'>
						<div className='text-base font-medium text-gray-900'>{getRatingLabel(sliderValue)}</div>
						<div className='mt-1 text-sm text-gray-600'>{getRatingDescription(sliderValue)}</div>
					</div>
					<div>
						<Slider
							value={[sliderValue]}
							onValueChange={handleSliderChange}
							min={1}
							max={5}
							step={1}
							className='w-full'
						/>
						<div className='mt-3 flex justify-between px-0.5'>
							<span className='text-sm text-gray-500'>Spam</span>
							<span className='text-sm text-gray-500'>Priority</span>
						</div>
					</div>
				</div>

				<div className='flex justify-end'>
					<motion.button
						whileHover={{ x: 4 }}
						whileTap={{ scale: 0.95 }}
						onClick={handleNextClick}
						disabled={isExiting}
						className='flex items-center gap-2 rounded-lg bg-foreground px-5 py-2.5 text-sm font-medium text-background transition-all hover:bg-foreground/90 disabled:opacity-70'
					>
						{isLastEmail ? 'Complete' : 'Next Email'}
						<ChevronRight className='h-4 w-4' />
					</motion.button>
				</div>
			</div>
		</motion.div>
	);
}
