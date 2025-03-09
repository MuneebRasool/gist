import { motion } from 'framer-motion';

export default function QuestionPrompt() {
  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-10 max-w-2xl text-center"
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.2 }}
        className="mb-4 inline-block rounded-full bg-indigo-50 px-4 py-1 text-sm font-medium text-indigo-700"
      >
        Email Importance Rating
      </motion.div>
      
      <h2 className="text-2xl font-semibold leading-tight text-gray-800 md:text-3xl">
        A few emails in your inbox and send box caught my attention.
      </h2>
      
      <p className="mt-4 text-lg text-gray-600">
        Can you help me better understand how important they are to what you&apos;re currently trying to achieve?
      </p>
    </motion.div>
  );
} 