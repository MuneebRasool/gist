'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import EmailService, { EmailMessage } from '@/services/nylas/email.service';
// import { OnboardingService, OnboardingFormData, QuestionWithOptions } from '@/services/agent/onboarding.service';
import { useOnboardingStore } from '@/store/onboarding.store';
import { Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import { AnimatePresence, motion } from 'framer-motion';
import EmailCard from '@/components/app/onboarding/EmailCard';
import QuestionPrompt from '@/components/app/onboarding/QuestionPrompt';
import ProgressIndicator from '@/components/app/onboarding/ProgressIndicator';
import { Email } from '@/types/nylasEmail';
import { AgentService } from '@/services/agent.service';

export default function OnboardingEmailRatingPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [emails, setEmails] = useState<EmailMessage[]>([]);
  const [currentEmailIndex, setCurrentEmailIndex] = useState(0);
  const [emailRatings, setEmailRatings] = useState<Record<string, number>>({});
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [loadingMessageIndex, setLoadingMessageIndex] = useState(0);

  const loadingMessages = [
    "Creating your personality profile...",
    "Fetching your recent emails...",
    "Extracting tasks from your emails..."
  ];

  useEffect(() => {
    const emailFromParams = searchParams.get('email');
    if (emailFromParams) {
      localStorage.setItem('userEmail', emailFromParams);
      console.log('Email saved to localStorage:', emailFromParams);
    }
  }, [searchParams]);

  useEffect(() => {
    const fetchEmails = async () => {
      try {
        setIsLoading(true);
        const response = await EmailService.getOnboardingEmails({ limit: 15 });
        
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

  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    if (isLoading && isSubmitting) {
      interval = setInterval(() => {
        setLoadingMessageIndex(prev => (prev + 1) % loadingMessages.length);
      }, 3000);
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isLoading, isSubmitting, loadingMessages.length]);

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
      
      // Get domain and email from localStorage
      const domain = localStorage.getItem('domain') || undefined;
      const email = searchParams.get('email') || localStorage.getItem('userEmail') || undefined;
      
      // Map the emails to the simplified format
      const simplifiedEmails = emails.map(email => ({
        id: email.id,
        subject: email.subject || '',
        from: Array.isArray(email.from) ? email.from : [],
        snippet: email.snippet || '',
        date: email.date || 0
      }));
      
      try {
        
        const emailsJson = JSON.stringify(simplifiedEmails);
        const ratingsJson = JSON.stringify(emailRatings);
        
        localStorage.setItem('ratedEmails', emailsJson);
        localStorage.setItem('emailRatings', ratingsJson);
        
        // Ensure email is saved to localStorage
        if (email) {
          localStorage.setItem('userEmail', email);
        }
        
        // Verify the data was saved correctly
        const savedEmails = localStorage.getItem('ratedEmails');
        const savedRatings = localStorage.getItem('emailRatings');
        const savedEmail = localStorage.getItem('userEmail');
        
        if (!savedEmails || !savedRatings) {
          console.error('Failed to save emails or ratings to localStorage');
        } else {
          console.log('Successfully saved emails and ratings to localStorage');
          if (savedEmail) {
            console.log('Successfully saved user email to localStorage:', savedEmail);
          }
        }
      } catch (error) {
        console.error('Error saving data to localStorage:', error);
      }
      
      toast.success('Email ratings saved successfully!');
      
      // Show loading sequence before redirecting
      setIsLoading(true);
      setIsSubmitting(true);
      setLoadingMessageIndex(0);
      
      // Include email in redirect URL if available
      const emailParam = email ? `&email=${email}` : '';
      const redirectPath = domain ? `/app/onboarding?domain=${domain}${emailParam}` : `/app/onboarding${emailParam ? `?${emailParam.substring(1)}` : ''}`;
      
      // Add a small delay to show the success message
      setTimeout(() => {
        router.push(redirectPath);
      }, 1500);
    } catch (error) {
      console.error('Error submitting email ratings:', error);
      toast.error('Failed to complete onboarding. Please try again.');
      setIsSubmitting(false);
    }
  };


  if (isLoading) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-gradient-to-r from-[#e6dcda] via-[#cfc6cb] to-[#ced4d8]">
        <div className="flex flex-col items-center justify-center space-y-8">
          <div className="relative">
            <div className="h-12 w-12 animate-spin rounded-full border-4 border-[#A5B7C8]/30 border-t-[#A5B7C8]" />
          </div>
          <p className="text-lg font-medium text-gray-600">
            {isSubmitting ? loadingMessages[loadingMessageIndex] : "Loading your emails..."}
          </p>
        </div>
      </div>
    );
  }

  if (emails.length === 0) {
    return (
      <div className="flex min-h-[calc(100vh-80px)] items-center justify-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-2xl bg-white/40 p-8 text-center shadow-lg backdrop-blur-sm"
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
        {emails.length > 0 && (
          <div key={emails[currentEmailIndex].id} className="bg-white shadow-lg rounded-2xl">
            <EmailCard
              email={emails[currentEmailIndex]}
              currentRating={emailRatings[emails[currentEmailIndex].id]}
              onRate={handleEmailRate}
              onNext={handleNextEmail}
              isLastEmail={currentEmailIndex === emails.length - 1}
            />
          </div>
        )}
      </AnimatePresence>
      
      <ProgressIndicator
        currentIndex={currentEmailIndex}
        totalEmails={emails.length}
      />
    </div>
  );
} 