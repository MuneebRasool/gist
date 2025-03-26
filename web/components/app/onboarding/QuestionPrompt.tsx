import { motion } from 'framer-motion';

export default function QuestionPrompt() {
	return (
		<motion.div
			initial={{ opacity: 0, y: -20 }}
			animate={{ opacity: 1, y: 0 }}
			className='my-10 max-w-3xl rounded-xl bg-background p-3 text-center'
		>
			A few emails in your inbox and send box caught my attention. Can you help me better understand how important they
			are to what you’re currently trying to achieve?
		</motion.div>
	);
}
