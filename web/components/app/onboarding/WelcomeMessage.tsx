'use client';
import { motion, AnimatePresence } from 'framer-motion';
import { useState, useEffect } from 'react';
import AcknowledgeForm from './AcknowledgeForm';

export default function WelcomeMessage() {
	const [isAnimatingToCorner, setIsAnimatingToCorner] = useState(false);
	const [showForm, setShowForm] = useState(false);

	useEffect(() => {
		const timer = setTimeout(() => {
			setIsAnimatingToCorner(true);
			setTimeout(() => {
				setShowForm(true);
			}, 500);
		}, 1500);

		return () => clearTimeout(timer);
	}, []);

	return (
		<div className='fixed inset-0 flex items-center justify-center'>
			<motion.div
				initial={isAnimatingToCorner ? false : { opacity: 0, y: 20 }}
				animate={
					isAnimatingToCorner
						? {
								opacity: 1,
								y: 0,
								x: 0,
								scale: 0.6,
								top: '2rem',
								left: '2rem',
								flexDirection: 'row',
							}
						: {
								opacity: 1,
								y: 0,
								x: 0,
								scale: 1,
								flexDirection: 'column',
							}
				}
				transition={{ duration: 1, ease: 'easeInOut' }}
				className={`absolute z-50 flex items-center gap-4 ${
					isAnimatingToCorner ? '' : 'left-1/2 top-1/2 !-translate-x-1/2 !-translate-y-1/2 gap-8'
				}`}
			>
				<motion.div
					animate={{
						width: isAnimatingToCorner ? 48 : 160,
						height: isAnimatingToCorner ? 48 : 160,
					}}
					transition={{
						duration: 1,
					}}
					className='size-40 rounded-full bg-primary'
				/>
				<h1 className='text-4xl font-semibold text-gray-700'>Hi, I&apos;m Gist!</h1>
			</motion.div>

			<AnimatePresence>{showForm && <AcknowledgeForm />}</AnimatePresence>
		</div>
	);
}
