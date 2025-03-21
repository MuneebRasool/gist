import React from 'react';
import { motion } from 'framer-motion';
import { useOnboardingStore } from '@/store';

const NoEmail = () => {
	const { setCurrentStep } = useOnboardingStore();
	return (
		<div className='flex h-full items-center justify-center'>
			<motion.div
				initial={{ opacity: 0, y: 20 }}
				animate={{ opacity: 1, y: 0 }}
				className='rounded-2xl bg-background/80 p-8 text-center shadow-lg backdrop-blur-sm'
			>
				<h3 className='text-xl font-medium'>No Emails Found</h3>
				<p className='mt-4 text-gray-600'>
					We couldn&apos;t find any emails to rate. Let&apos;s continue with your onboarding.
				</p>
				<motion.button
					whileHover={{ scale: 1.03 }}
					whileTap={{ scale: 0.98 }}
					onClick={() => setCurrentStep('questions')}
					className='mt-6 rounded-lg bg-primary px-6 py-3 text-primary-foreground transition-all hover:bg-primary/80'
				>
					Continue to Questions
				</motion.button>
			</motion.div>
		</div>
	);
};

export default NoEmail;
