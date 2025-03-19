import React from 'react';
import { Button } from '@/components/ui/button';
import { Library, Inbox } from 'lucide-react';

interface FloatingButtonsProps {
  onLibraryClick?: () => void;
  onDrawerClick?: () => void;
}

const FloatingButtons: React.FC<FloatingButtonsProps> = ({
  onLibraryClick,
  onDrawerClick,
}) => {
  return (
    <div className="w-full max-w-7xl h-full">
      <div className="flex gap-4 w-full">
        <Button
          onClick={onLibraryClick}
          className="flex-1 h-14 bg-white/40 hover:bg-white/50 backdrop-blur-md text-gray-800 rounded-2xl shadow-lg transition-all duration-200 flex items-center justify-center gap-2 text-lg font-medium"
          variant="ghost"
        >
          <Library className="h-5 w-5" />
          Library
        </Button>
        <Button
          onClick={onDrawerClick}
          className="flex-1 h-14 bg-white/40 hover:bg-white/50 backdrop-blur-md text-gray-800 rounded-2xl shadow-lg transition-all duration-200 flex items-center justify-center gap-2 text-lg font-medium"
          variant="ghost"
        >
          <Inbox className="h-5 w-5" />
          Drawer
        </Button>
      </div>
    </div>
  );
};

export default FloatingButtons; 