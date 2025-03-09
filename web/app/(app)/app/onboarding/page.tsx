'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { AgentService } from '@/services/agent.service';
import { QuestionWithOptions } from '@/types/agent';
import { useOnboardingStore } from '@/store/onboarding.store';
import { Button } from '@/components/ui/button';
import { Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import { motion, AnimatePresence } from 'framer-motion';

const OnboardingPage = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const email = searchParams.get('email');
  
  const { 
    questions, 
    summary, 
    answers, 
    isLoading, 
    isCompleted,
    setQuestions, 
    setSummary, 
    setAnswer, 
    setIsLoading,
    setIsCompleted
  } = useOnboardingStore();
  
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    const fetchDomainInference = async () => {
      if (!email) {
        toast.error('Email not found. Please try connecting your email again.');
        router.push('/app/settings');
        return;
      }
      
      try {
        setIsLoading(true);
        const response = await AgentService.inferDomain(email);
        
        if (response.error) {
          toast.error('Failed to load onboarding questions. Please try again.');
          router.push('/app');
          return;
        }
        
        if (response.data) {
          setQuestions(response.data.questions || []);
          
          if (response.data.summary) {
            setSummary(response.data.summary);
          } else if (response.data.domain) {
            setSummary(`Based on your email, we've personalized some questions for your ${response.data.domain} context.`);
          } else {
            setSummary('Please answer these questions to help us personalize your experience.');
          }
        }
      } catch (error) {
        console.error('Error fetching domain inference:', error);
        toast.error('Failed to load onboarding questions. Please try again.');
        router.push('/app');
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchDomainInference();
  }, [email, router, setIsLoading, setQuestions, setSummary]);

  const handleOptionSelect = (question: string, option: string) => {
    setAnswer(question, option);
  };

  const handleSubmit = async () => {
    try {
      setIsSubmitting(true);
      
      // Check if all questions are answered
      const areAllQuestionsAnswered = questions.every(q => answers[q.question]);
      
      if (!areAllQuestionsAnswered) {
        toast.error('Please answer all questions before submitting');
        return;
      }
      
      // Save answers and other onboarding data to localStorage
      try {
        localStorage.setItem('onboardingAnswers', JSON.stringify(answers));
        localStorage.setItem('onboardingQuestions', JSON.stringify(questions));
        localStorage.setItem('onboardingSummary', summary);
        
        if (email) {
          localStorage.setItem('userEmail', email);
        }
        
        // Store domain if available from response data
        const response = await AgentService.inferDomain(email || '');
        if (response.data?.domain) {
          localStorage.setItem('domain', response.data.domain);
        }
      } catch (error) {
        console.error('Error saving to localStorage:', error);
      }
      
      setIsCompleted(true);
      toast.success('Profile information saved successfully!');
      
      router.push('/app/onboarding2');
    } catch (error) {
      console.error('Error submitting onboarding answers:', error);
      toast.error('Failed to save information. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
        <motion.div 
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="flex flex-col items-center gap-5 rounded-2xl bg-white/80 p-8 shadow-lg backdrop-blur-sm"
        >
          <Loader2 size={48} className="animate-spin text-indigo-500" />
          <p className="text-lg font-medium text-gray-700">Loading your personalized experience...</p>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
        className="w-full max-w-xl"
      >
        <div className="overflow-hidden rounded-3xl bg-white/90 shadow-xl backdrop-blur-sm">
          <div className="border-b border-gray-100 bg-gradient-to-r from-indigo-50 to-blue-50 px-8 py-6">
            <h2 className="text-2xl font-semibold text-gray-800">Welcome to GIST</h2>
            <p className="mt-1 text-sm text-gray-600">Please answer a few questions to help us personalize your experience</p>
          </div>
          
          <div className="p-8">
            {summary && (
              <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="mb-8 rounded-xl bg-blue-50/50 p-4 text-sm leading-relaxed text-gray-700"
              >
                {summary}
              </motion.div>
            )}
            
            <div className="space-y-8">
              <AnimatePresence>
                {questions.map((question: QuestionWithOptions, index: number) => (
                  <motion.div 
                    key={index}
                    initial={{ opacity: 0, y: 15 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 * (index + 1) }}
                    className="space-y-4"
                  >
                    <h3 className="text-base font-medium text-gray-700">{question.question}</h3>
                    <div className="grid grid-cols-2 gap-4">
                      {question.options.map((option: string, optIndex: number) => (
                        <motion.div
                          key={optIndex}
                          whileHover={{ scale: 1.02 }}
                          whileTap={{ scale: 0.98 }}
                        >
                          <Button
                            variant="outline"
                            className={`h-14 w-full rounded-xl border-2 text-base font-medium transition-all duration-200 ${
                              answers[question.question] === option 
                                ? 'border-indigo-300 bg-gradient-to-r from-indigo-50 to-blue-50 text-indigo-700 shadow-sm' 
                                : 'border-gray-200 bg-white text-gray-600 hover:border-indigo-200 hover:bg-indigo-50/30 hover:text-indigo-600'
                            }`}
                            onClick={() => handleOptionSelect(question.question, option)}
                          >
                            <span className="block truncate px-2" title={option}>
                              {option}
                            </span>
                          </Button>
                        </motion.div>
                      ))}
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>

              <div className="mt-10 flex items-center justify-between pt-4">
                <div className="text-sm font-medium text-indigo-500">
                  Step 1 of 2: Profile Information
                </div>
                <motion.div
                  whileHover={!isSubmitting && questions.every(q => answers[q.question]) ? { scale: 1.03 } : {}}
                  whileTap={!isSubmitting && questions.every(q => answers[q.question]) ? { scale: 0.97 } : {}}
                >
                  <Button
                    onClick={handleSubmit}
                    disabled={isSubmitting || questions.length === 0 || !questions.every(q => answers[q.question])}
                    className={`h-12 rounded-xl px-8 text-base font-medium transition-all duration-300 ${
                      isSubmitting || questions.length === 0 || !questions.every(q => answers[q.question])
                        ? 'bg-gradient-to-r from-gray-100 to-gray-200 text-gray-400'
                        : 'bg-gradient-to-r from-indigo-500 to-blue-500 text-white hover:from-indigo-600 hover:to-blue-600'
                    }`}
                  >
                    {isSubmitting ? (
                      <div className="flex items-center gap-2">
                        <Loader2 className="h-4 w-4 animate-spin" />
                        <span>Saving...</span>
                      </div>
                    ) : (
                      'Continue to Next Step'
                    )}
                  </Button>
                </motion.div>
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default OnboardingPage; 