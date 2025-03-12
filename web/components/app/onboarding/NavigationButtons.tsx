import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { ArrowLeft, ArrowRight, CheckCircle, Loader2 } from 'lucide-react';

interface NavigationButtonsProps {
  currentQuestionIndex: number;
  totalQuestions: number;
  showSummary: boolean;
  isSubmitting: boolean;
  hasCurrentAnswer: boolean;
  onPrevious: () => void;
  onNext: () => void;
  onSubmit: () => void;
  onEditAnswers: () => void;
}

export const NavigationButtons = ({
  currentQuestionIndex,
  totalQuestions,
  showSummary,
  isSubmitting,
  hasCurrentAnswer,
  onPrevious,
  onNext,
  onSubmit,
  onEditAnswers,
}: NavigationButtonsProps) => {
  return (
    <div className='mt-10 flex items-center justify-between pt-4 gap-4'>
      {!showSummary && (
        <motion.div
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className={`${currentQuestionIndex === 0 ? 'invisible' : 'visible'}`}
        >
          <Button
            onClick={onPrevious}
            variant="outline"
            className="h-12 rounded-xl text-base font-medium transition-all duration-300 border-gray-200"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back
          </Button>
        </motion.div>
      )}

      {!showSummary ? (
        <motion.div
          whileHover={hasCurrentAnswer ? { scale: 1.02 } : {}}
          whileTap={hasCurrentAnswer ? { scale: 0.98 } : {}}
          className='flex-1'
        >
          <Button
            onClick={onNext}
            disabled={!hasCurrentAnswer}
            className={`h-12 w-full rounded-xl text-base font-medium transition-all duration-300 ${
              !hasCurrentAnswer
                ? 'bg-gray-100 text-gray-400'
                : 'bg-gray-900 text-white hover:bg-gray-800'
            }`}
          >
            {currentQuestionIndex === totalQuestions - 1 ? 'Review Answers' : 'Continue'}
            <ArrowRight className="h-4 w-4 ml-2" />
          </Button>
        </motion.div>
      ) : (
        <>
          <motion.div
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <Button
              onClick={onEditAnswers}
              variant="outline"
              className="h-12 rounded-xl text-base font-medium transition-all duration-300 border-gray-200"
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Edit Answers
            </Button>
          </motion.div>
          <motion.div
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className='flex-1'
          >
            <Button
              onClick={onSubmit}
              disabled={isSubmitting}
              className="h-12 w-full rounded-xl text-base font-medium transition-all duration-300 bg-gray-900 text-white hover:bg-gray-800"
            >
              {isSubmitting ? (
                <div className='flex items-center gap-2'>
                  <Loader2 className='h-4 w-4 animate-spin' />
                  <span>Saving...</span>
                </div>
              ) : (
                <>
                  Complete Setup
                  <CheckCircle className="h-4 w-4 ml-2" />
                </>
              )}
            </Button>
          </motion.div>
        </>
      )}
    </div>
  );
};

export default NavigationButtons; 