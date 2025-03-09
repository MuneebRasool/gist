'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { AgentService } from '@/services/agent.service';
import { QuestionWithOptions } from '@/types/agent';
import { useOnboardingStore } from '@/store/onboarding.store';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Label } from '@/components/ui/label';
import { Loader2 } from 'lucide-react';
import { toast } from 'sonner';

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
          // Set questions from response
          setQuestions(response.data.questions || []);
          
          // Handle case where summary is missing
          if (response.data.summary) {
            setSummary(response.data.summary);
          } else if (response.data.domain) {
            // If there's a domain field but no summary, create a simple summary from the domain
            setSummary(`Based on your email, we've personalized some questions for your ${response.data.domain} context.`);
          } else {
            // Default summary if neither exists
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
      
      // For now, using the onboarding submit API endpoint
      // This can be updated when the backend endpoint is decided
      const response = await fetch('/api/onboarding/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ answers }),
      });
      
      if (!response.ok) {
        toast.error('Failed to submit onboarding information. Please try again.');
        return;
      }
      
      setIsCompleted(true);
      toast.success('Onboarding completed successfully!');
      
      // Redirect to main app after successful submission
      setTimeout(() => {
        router.push('/app');
      }, 1500);
    } catch (error) {
      console.error('Error submitting onboarding answers:', error);
      toast.error('Failed to submit onboarding information. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };
  
  if (isLoading) {
    return (
      <div className="flex h-[calc(100vh-80px)] w-full flex-col items-center justify-center">
        <Loader2 size={40} className="animate-spin text-primary" />
        <p className="mt-4 text-lg font-medium">Loading your personalized onboarding...</p>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto py-8">
      <Card className="max-w-3xl mx-auto">
        <CardHeader>
          <CardTitle className="text-2xl font-bold">Welcome to GIST</CardTitle>
          <CardDescription>
            Please answer a few questions to help us personalize your experience
          </CardDescription>
        </CardHeader>
        <CardContent>
          {questions.length > 0 ? (
            <div className="space-y-8">
              {summary && (
                <div className="mb-6 rounded-lg bg-muted p-4">
                  <p className="text-sm text-muted-foreground">{summary}</p>
                </div>
              )}
              
              {questions.map((question: QuestionWithOptions, index: number) => (
                <div key={index} className="space-y-4">
                  <h3 className="text-lg font-medium">{question.question}</h3>
                  <RadioGroup
                    value={answers[question.question] || ''}
                    onValueChange={(value) => handleOptionSelect(question.question, value)}
                    className="space-y-2"
                  >
                    {question.options.map((option: string, optIndex: number) => (
                      <div key={optIndex} className="flex items-center space-x-2">
                        <RadioGroupItem id={`q${index}-opt${optIndex}`} value={option} />
                        <Label htmlFor={`q${index}-opt${optIndex}`}>{option}</Label>
                      </div>
                    ))}
                  </RadioGroup>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-center text-muted-foreground">No questions available. Please try again later.</p>
          )}
        </CardContent>
        <CardFooter>
          <Button 
            onClick={handleSubmit} 
            disabled={isSubmitting || questions.length === 0} 
            className="w-full"
          >
            {isSubmitting ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" /> 
                Submitting...
              </>
            ) : (
              'Complete Onboarding'
            )}
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
};

export default OnboardingPage; 