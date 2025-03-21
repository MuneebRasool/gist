import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { MessageCircle } from 'lucide-react';
import { Avatar } from '@/components/ui/avatar';

interface OnboardingAssistantProps {
	message: string;
	currentQuestionIndex: number;
	totalQuestions: number;
	isShowingSummary: boolean;
}

export const OnboardingAssistant = ({
	message,
	currentQuestionIndex,
	totalQuestions,
	isShowingSummary,
}: OnboardingAssistantProps) => {
	const [assistantAnimation, setAssistantAnimation] = useState(false);

	// Trigger assistant animation periodically
	useEffect(() => {
		const animationInterval = setInterval(() => {
			setAssistantAnimation(true);
			setTimeout(() => setAssistantAnimation(false), 1000);
		}, 5000);

		return () => clearInterval(animationInterval);
	}, []);

	return (
		<motion.div
			initial={{ opacity: 0, y: 5 }}
			animate={{ opacity: 1, y: 0 }}
			key={message}
			className='mb-8 w-full rounded-xl bg-blue-50 p-3 text-gray-700'
		>
			{message}
		</motion.div>
	);
};

export default OnboardingAssistant;
