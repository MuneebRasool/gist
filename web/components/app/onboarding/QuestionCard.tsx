import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { CheckCircle } from 'lucide-react';
import { QuestionWithOptions } from '@/types/agent';

interface QuestionCardProps {
  question: QuestionWithOptions;
  selectedAnswer: string | undefined;
  onSelectOption: (question: string, option: string) => void;
}

export const QuestionCard = ({
  question,
  selectedAnswer,
  onSelectOption,
}: QuestionCardProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      transition={{ duration: 0.3 }}
      className='space-y-6'
    >
      <h3 className='text-lg font-medium text-gray-700'>{question.question}</h3>
      <div className='grid grid-cols-1 sm:grid-cols-2 gap-4'>
        {question.options.map((option: string, optIndex: number) => (
          <motion.div 
            key={optIndex} 
            whileHover={{ scale: 1.03 }} 
            whileTap={{ scale: 0.97 }}
            transition={{ type: "spring", stiffness: 400, damping: 17 }}
          >
            <Button
              variant='outline'
              className={`h-14 w-full rounded-xl border text-base font-medium transition-all duration-200 ${
                selectedAnswer === option
                  ? 'border-gray-400 bg-gray-50 text-gray-900 shadow-sm'
                  : 'border-gray-200 bg-white text-gray-600 hover:border-gray-300 hover:bg-gray-50/50'
              }`}
              onClick={() => onSelectOption(question.question, option)}
            >
              <span className='block truncate px-2' title={option}>
                {option}
              </span>
              {selectedAnswer === option && (
                <CheckCircle className="h-4 w-4 ml-2 text-green-500" />
              )}
            </Button>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
};

export default QuestionCard; 