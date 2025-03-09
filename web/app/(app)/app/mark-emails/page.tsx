'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import EmailService, { EmailMessage } from '@/services/nylas/email.service';
import { OnboardingService, OnboardingFormData } from '@/services/agent/onboarding.service';
import { useOnboardingStore } from '@/store/onboarding.store';
import { Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import { AnimatePresence, motion } from 'framer-motion';
import EmailCard from '@/components/app/onboarding/EmailCard';
import QuestionPrompt from '@/components/app/onboarding/QuestionPrompt';
import ProgressIndicator from '@/components/app/onboarding/ProgressIndicator';
import { Email } from '@/types/nylasEmail';

export default function OnboardingEmailRatingPage() {
  const router = useRouter();
  const [emails, setEmails] = useState<EmailMessage[]>([]);
  const [currentEmailIndex, setCurrentEmailIndex] = useState(0);
  const [emailRatings, setEmailRatings] = useState<Record<string, number>>({});
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    const fetchEmails = async () => {
      try {
        setIsLoading(true);
        const response = await EmailService.getEmails({ limit: 10 });
        
        if (response.error) {
          toast.error('Failed to load emails. Please try again.');
          return;
        }
        
        if (response.data?.data) {
          // Transform the date to number if it's a string
          const transformedEmails = response.data.data.map((email: Email) => ({
            ...email,
            date: typeof email.date === 'string' ? new Date(email.date).getTime() / 1000 : Number(email.date)
          })) as EmailMessage[];
          
          setEmails(transformedEmails);
          
          // Initialize ratings with default value (5)
          const initialRatings: Record<string, number> = {};
          transformedEmails.forEach(email => {
            initialRatings[email.id] = 5;
          });
          setEmailRatings(initialRatings);
        }
      } catch (error) {
        console.error('Error fetching emails:', error);
        toast.error('Failed to load emails. Please try again.');
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchEmails();
  }, []);

  const handleEmailRate = (rating: number) => {
    const currentEmail = emails[currentEmailIndex];
    
    setEmailRatings(prev => ({
      ...prev,
      [currentEmail.id]: rating
    }));
  };
  
  const handleNextEmail = async () => {
    if (currentEmailIndex < emails.length - 1) {
      setCurrentEmailIndex(prev => prev + 1);
    } else {
      await handleSubmit();
    }
  };

  const handleSubmit = async () => {
    try {
      setIsSubmitting(true);
      
      // Get data from localStorage
      const storedQuestions = localStorage.getItem('onboardingQuestions');
      const storedAnswers = localStorage.getItem('onboardingAnswers');
      const domain = localStorage.getItem('domain') || undefined;
      
      const onboardingData: OnboardingFormData = {
        questions: storedQuestions ? JSON.parse(storedQuestions) : [],
        answers: storedAnswers ? JSON.parse(storedAnswers) : {},
        domain,
        emailRatings,
        ratedEmails: emails.map(email => ({
          id: email.id,
          subject: email.subject || '',
          from: Array.isArray(email.from) ? email.from : [],
          snippet: email.snippet || '',
          date: email.date || 0
        }))
      };
      
      const response = await OnboardingService.submitOnboardingData(onboardingData);
      
      if (response.error) {
        const errorMessage = typeof response.error === 'string' 
          ? response.error 
          : response.error.message || 'Failed to save preferences';
        toast.error(errorMessage);
        return;
      }
      
      toast.success('Onboarding completed successfully!');
      
      // Clear localStorage
      localStorage.removeItem('onboardingQuestions');
      localStorage.removeItem('onboardingAnswers');
      localStorage.removeItem('domain');
      
      router.push('/app');
    } catch (error) {
      console.error('Error submitting onboarding data:', error);
      toast.error('Failed to save your preferences. Please try again.');
      router.push('/app');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex min-h-[calc(100vh-80px)] items-center justify-center">
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex flex-col items-center gap-6"
        >
          <div className="relative h-16 w-16">
            <motion.div
              animate={{ 
                rotate: 360,
                transition: { duration: 1.5, repeat: Infinity, ease: "linear" }
              }}
              className="absolute inset-0 rounded-full border-2 border-indigo-200 border-t-indigo-500"
            />
          </div>
          <p className="text-lg font-medium text-gray-700">Loading your emails...</p>
        </motion.div>
      </div>
    );
  }

  if (emails.length === 0) {
    return (
      <div className="flex min-h-[calc(100vh-80px)] items-center justify-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-2xl bg-white p-8 text-center shadow-lg"
        >
          <h3 className="text-xl font-medium text-gray-800">No Emails Found</h3>
          <p className="mt-4 text-gray-600">
            We couldn&apos;t find any emails to rate. Let&apos;s continue with your onboarding.
          </p>
          <motion.button
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => router.push('/app')}
            className="mt-6 rounded-lg bg-indigo-600 px-6 py-3 text-white transition-all hover:bg-indigo-700"
          >
            Continue to Dashboard
          </motion.button>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="flex min-h-[calc(100vh-80px)] flex-col items-center justify-center px-4 py-8">
      <QuestionPrompt />
      
      <AnimatePresence mode="wait">
        <EmailCard
          key={emails[currentEmailIndex].id}
          email={emails[currentEmailIndex]}
          currentRating={emailRatings[emails[currentEmailIndex].id]}
          onRate={handleEmailRate}
          onNext={handleNextEmail}
          isLastEmail={currentEmailIndex === emails.length - 1}
        />
      </AnimatePresence>
      
      <ProgressIndicator
        currentIndex={currentEmailIndex}
        totalEmails={emails.length}
      />
    </div>
  );
} 