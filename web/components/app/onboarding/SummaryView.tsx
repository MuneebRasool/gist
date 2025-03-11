import { motion } from 'framer-motion';
import { QuestionWithOptions } from '@/types/agent';

interface SummaryViewProps {
  questions: QuestionWithOptions[];
  answers: Record<string, string>;
}

export const SummaryView = ({ questions, answers }: SummaryViewProps) => {
  return (
    <motion.div
      key="summary"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className='space-y-6'
    >
      <h3 className='text-lg font-medium text-gray-700'>Your Profile Summary</h3>
      <div className='space-y-4 bg-gray-50/70 p-4 rounded-xl'>
        {questions.map((question, index) => (
          <div 
            key={index} 
            className="flex justify-between items-center border-b border-gray-100 pb-2 last:border-0 last:pb-0"
          >
            <p className="text-sm text-gray-600">{question.question}</p>
            <p className="text-sm font-medium text-gray-800">{answers[question.question]}</p>
          </div>
        ))}
      </div>
    </motion.div>
  );
};

export default SummaryView; 