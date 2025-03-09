import { motion } from 'framer-motion';

interface ProgressIndicatorProps {
  currentIndex: number;
  totalEmails: number;
}

export default function ProgressIndicator({ currentIndex, totalEmails }: ProgressIndicatorProps) {
  const progress = ((currentIndex + 1) / totalEmails) * 100;
  
  return (
    <div className="mt-8 flex flex-col items-center gap-2">
      <div className="flex w-full max-w-md items-center justify-between px-1">
        <span className="text-sm font-medium text-gray-500">
          Email {currentIndex + 1} of {totalEmails}
        </span>
        <span className="text-sm font-medium text-gray-700">
          {progress.toFixed(0)}% Complete
        </span>
      </div>
      
      <div className="h-2 w-full max-w-md overflow-hidden rounded-full bg-gray-100">
        <motion.div 
          className="h-full bg-gradient-to-r from-rose-200 to-gray-900"
          initial={{ width: 0 }}
          animate={{ 
            width: `${progress}%`,
            transition: { duration: 0.5, ease: "easeOut" }
          }}
        />
      </div>
    </div>
  );
} 