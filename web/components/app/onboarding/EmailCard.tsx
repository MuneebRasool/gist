import { EmailMessage } from '@/services/nylas/email.service';
import { motion } from 'framer-motion';
import { ChevronRight } from 'lucide-react';
import { useState } from 'react';

interface EmailCardProps {
  email: EmailMessage;
  currentRating: number;
  onRate: (rating: number) => void;
  onNext: () => void;
  isLastEmail: boolean;
}

export default function EmailCard({ 
  email, 
  currentRating = 5, 
  onRate, 
  onNext,
  isLastEmail 
}: EmailCardProps) {
  const ratingOptions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  const [isExiting, setIsExiting] = useState(false);
  
  const getRatingLabel = (rating: number) => {
    if (rating <= 2) return 'Irrelevant';
    if (rating <= 4) return 'Low Priority';
    if (rating <= 6) return 'Somewhat Important';
    if (rating <= 8) return 'Important';
    return 'Critical';
  };

  const cardVariants = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, x: -300, transition: { duration: 0.3, ease: "easeInOut" } }
  };

  const handleNextClick = () => {
    setIsExiting(true);
    // Add a small delay before calling onNext to allow the animation to play
    setTimeout(() => {
      onNext();
      setIsExiting(false);
    }, 300);
  };

  return (
    <motion.div
      variants={cardVariants}
      initial="initial"
      animate="animate"
      exit="exit"
      className="w-full max-w-2xl overflow-hidden rounded-2xl bg-white/40 p-0 shadow-lg backdrop-blur-sm"
    >
      <div className="border-b border-gray-100 bg-white/30 p-6">
        <div className="space-y-4">
          <div className="space-y-1">
            <div className="text-xs font-medium uppercase tracking-wider text-gray-500">Recipient</div>
            <div className="text-sm text-gray-600">{email.to?.[0]?.email || 'Unknown Recipient'}</div>
          </div>
          
          <div className="space-y-1">
            <div className="text-xs font-medium uppercase tracking-wider text-gray-500">Subject</div>
            <div className="text-lg font-medium text-gray-900">{email.subject || '(No Subject)'}</div>
          </div>
        </div>
      </div>
      
      <div className="p-6">
        <div className="space-y-1">
          <div className="text-xs font-medium uppercase tracking-wider text-gray-500">Message</div>
          <div className="min-h-[100px] text-base leading-relaxed text-gray-800">{email.snippet}</div>
        </div>
      </div>
      
      <div className="space-y-6 bg-white/30 p-6">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-500">Not Important</span>
            <span className="text-sm font-medium text-gray-500">Very Important</span>
          </div>
          
          <div className="relative">
            {/* Background gradient bar */}
            <div className="absolute inset-x-0 top-1/2 h-1 -translate-y-1/2 rounded-full bg-gradient-to-r from-gray-200 via-rose-200 to-gray-900"></div>
            
            {/* Rating buttons */}
            <div className="relative flex justify-between">
              {ratingOptions.map((rating) => (
                <motion.button
                  key={rating}
                  onClick={() => onRate(rating)}
                  whileHover={{ y: -4 }}
                  whileTap={{ scale: 0.95 }}
                  className={`relative z-10 flex h-10 w-10 items-center justify-center rounded-full border-2 transition-all duration-200 ${
                    currentRating === rating
                      ? 'border-gray-900 bg-gray-900 text-white shadow-md shadow-gray-200'
                      : 'border-gray-200 bg-white text-gray-700 hover:border-gray-300'
                  }`}
                >
                  {rating}
                </motion.button>
              ))}
            </div>
          </div>
          
          {/* Rating label */}
          <div className="text-center">
            <motion.span
              key={currentRating}
              initial={{ opacity: 0, y: 5 }}
              animate={{ opacity: 1, y: 0 }}
              className="inline-block rounded-full bg-gray-100 px-3 py-1 text-sm font-medium text-gray-700"
            >
              {getRatingLabel(currentRating)}
            </motion.span>
          </div>
        </div>
        
        <div className="flex justify-end">
          <motion.button
            whileHover={{ x: 4 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleNextClick}
            disabled={isExiting}
            className="flex items-center gap-2 rounded-lg bg-black px-5 py-3 text-sm font-medium text-white transition-all hover:bg-black/90 disabled:opacity-70"
          >
            {isLastEmail ? 'Complete' : 'Next Email'}
            <ChevronRight className="h-4 w-4" />
          </motion.button>
        </div>
      </div>
    </motion.div>
  );
} 