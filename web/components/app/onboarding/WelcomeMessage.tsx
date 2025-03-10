'use client';
import { motion, AnimatePresence } from 'framer-motion';
import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Mail, Calendar } from 'lucide-react';
import { useSession } from 'next-auth/react';
import { NylasAuthService } from '@/services/nylas/auth.service';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';

export default function WelcomeMessage() {
  const [showInitialMessage, setShowInitialMessage] = useState(true);
  const [showPermissions, setShowPermissions] = useState(false);
  const [isAnimatingToCorner, setIsAnimatingToCorner] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { data: session } = useSession();
  const router = useRouter();

  const userName = session?.user?.name?.split(' ')[0] || 'there';

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsAnimatingToCorner(true);
      setTimeout(() => {
        setShowInitialMessage(false);
        setShowPermissions(true);
      }, 500);
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  const handleAcknowledge = async () => {
    try {
      setIsLoading(true);
      const res = await NylasAuthService.getAuthUrl();
      if (res.error) {
        toast.error(res.error.message);
      } else {
        router.push(res.data?.url ?? '');
      }
    } catch (error) {
      console.error('Failed to get auth URL:', error);
      toast.error('Failed to connect email. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-gradient-to-r from-[#e6dcda] to-[#cfc6cb]">
      <AnimatePresence>
        {showInitialMessage && (
          <>
            <motion.div
              initial={isAnimatingToCorner ? false : { opacity: 0, y: 20 }}
              animate={
                isAnimatingToCorner
                  ? {
                      opacity: 1,
                      y: 0,
                      x: 0,
                      scale: 0.6,
                      top: '2rem',
                      left: '2rem',
                    }
                  : {
                      opacity: 1,
                      y: 0,
                      x: 0,
                      scale: 1,
                    }
              }
              exit={{ opacity: 0 }}
              transition={{ duration: 0.5, ease: 'easeInOut' }}
              className={`absolute ${isAnimatingToCorner ? '' : 'left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2'} text-center`}
            >
              <h1 className="text-4xl font-semibold text-gray-700">Hi, I&apos;m Gist!</h1>
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={isAnimatingToCorner ? { opacity: 0 } : { opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="absolute left-1/2 top-1/2 -translate-x-1/2 translate-y-24"
            >
              <div className="h-32 w-32 rounded-full bg-[#e6dcda]/70 backdrop-blur-sm" />
              <motion.div
                animate={{ 
                  scale: [1, 1.1, 1],
                  rotate: [0, 5, -5, 0]
                }}
                transition={{ 
                  duration: 3,
                  repeat: Infinity,
                  repeatDelay: 2
                }}
                className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2"
              >
                <div className="h-24 w-24 rounded-full bg-[#cfc6cb]" />
              </motion.div>
            </motion.div>
          </>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {!showInitialMessage && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="w-full max-w-xl px-4"
          >
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="rounded-3xl bg-white/40 p-8 shadow-lg backdrop-blur-sm"
            >
              <div className="mb-6 flex items-center gap-3">
                <div className="h-10 w-10 rounded-full bg-[#cfc6cb]/70">
                  <motion.div
                    animate={{ 
                      scale: [1, 1.2, 1],
                      rotate: [0, 10, -10, 0]
                    }}
                    transition={{ 
                      duration: 2,
                      repeat: Infinity,
                      repeatDelay: 3
                    }}
                    className="flex h-full items-center justify-center"
                  >
                    👋
                  </motion.div>
                </div>
                <h2 className="text-xl font-semibold text-gray-700">Hi {userName},</h2>
              </div>
              
              <p className="mb-4 text-gray-600">It&apos;s so nice to meet you.</p>
              <p className="mb-6 text-gray-600">
                I&apos;d love for me to get to know you a little bit so I can better assist you.
                To help me with that, here are some access I need.
              </p>

              <div className="space-y-4">
                <div className="rounded-xl bg-white/30 p-4 backdrop-blur-sm">
                  <div className="flex items-center gap-3">
                    <Mail className="h-6 w-6 text-gray-600" />
                    <p className="text-sm text-gray-600">
                      Grant Gist access to your email to better understand your tasks and help with to-do lists and planning.
                    </p>
                  </div>
                </div>

                <div className="rounded-xl bg-white/30 p-4 backdrop-blur-sm">
                  <div className="flex items-center gap-3">
                    <Calendar className="h-6 w-6 text-gray-600" />
                    <p className="text-sm text-gray-600">
                      Allow Gist to access your calendar to view your schedule and help you plan meetings.
                    </p>
                  </div>
                </div>

                <Button 
                  onClick={handleAcknowledge}
                  disabled={isLoading}
                  className="mt-4 h-12 w-full bg-black text-base font-medium text-white hover:bg-black/90"
                >
                  {isLoading ? (
                    <div className="flex items-center gap-2">
                      <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                      Connecting...
                    </div>
                  ) : (
                    'Acknowledge & Agree'
                  )}
                </Button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
} 