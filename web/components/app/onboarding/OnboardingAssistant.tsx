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
    <div className="flex items-start gap-4 mb-8">
      <motion.div
        animate={assistantAnimation ? { scale: 1.05 } : { scale: 1 }}
        transition={{ duration: 0.3 }}
      >
        <Avatar className="h-12 w-12 bg-blue-100">
          <MessageCircle className="h-6 w-6 text-blue-500" />
        </Avatar>
      </motion.div>
      <motion.div 
        initial={{ opacity: 0, y: 5 }}
        animate={{ opacity: 1, y: 0 }}
        key={message}
        className="bg-blue-50 p-3 rounded-xl text-gray-700 max-w-[80%]"
      >
        {message}
      </motion.div>
    </div>
  );
};

export default OnboardingAssistant; 