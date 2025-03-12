import { Loader2 } from 'lucide-react';

interface LoadingScreenProps {
  message: string;
  isSubmitting?: boolean;
}

export const LoadingScreen = ({ message, isSubmitting = false }: LoadingScreenProps) => {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-gradient-to-r from-[#e6dcda] via-[#cfc6cb] to-[#ced4d8]">
      <div className="flex flex-col items-center justify-center space-y-8">
        <div className="relative">
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-[#A5B7C8]/30 border-t-[#A5B7C8]" />
          {isSubmitting && (
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="h-6 w-6 rounded-full bg-white" />
            </div>
          )}
        </div>
        <p className="text-lg font-medium text-gray-600 text-center max-w-md px-4">
          {message}
        </p>
      </div>
    </div>
  );
};

export default LoadingScreen; 