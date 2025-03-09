'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import EmailService, { EmailMessage } from '@/services/nylas/email.service';
import { OnboardingService, OnboardingFormData, SimplifiedEmail } from '@/services/agent/onboarding.service';
import { useOnboardingStore } from '@/store/onboarding.store';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Slider } from '@/components/ui/slider';
import { Loader2, Mail } from 'lucide-react';
import { toast } from 'sonner';
import { format } from 'date-fns';
import { Email } from '@/types/nylasEmail';
import { QuestionWithOptions } from '@/types/agent';

const OnboardingEmailRatingPage = () => {
  const router = useRouter();
  const [emails, setEmails] = useState<EmailMessage[]>([]);
  const [emailRatings, setEmailRatings] = useState<Record<string, number>>({});
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  // Get onboarding data from the store
  const { questions, answers } = useOnboardingStore();

  useEffect(() => {
    const fetchEmails = async () => {
      try {
        setIsLoading(true);
        // Use the existing getEmails method instead of getMessages
        const response = await EmailService.getEmails({
          limit: 10,
          // Add other parameters if needed
        });
        
        if (response.error) {
          toast.error('Failed to load emails. Please try again.');
          return;
        }
        
        if (response.data?.data) {
          // Adapt to the EmailResponse structure
          const emailMessages = response.data.data.map((email: Email) => ({
            id: email.id,
            subject: email.subject || '',
            from: email.from || [],
            to: email.to || [],
            cc: email.cc || [],
            bcc: email.bcc || [],
            date: typeof email.date === 'string' 
              ? new Date(email.date).getTime() / 1000 // Convert string date to unix timestamp
              : 0,
            snippet: email.snippet || '',
            body: email.body || '',
            unread: email.unread || false,
            starred: email.starred || false
          }));
          
          setEmails(emailMessages);
          
          // Initialize ratings with default values (5)
          const initialRatings: Record<string, number> = {};
          emailMessages.forEach((email: EmailMessage) => {
            initialRatings[email.id] = 5;
          });
          setEmailRatings(initialRatings);
        } else {
          setEmails([]);
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
  
  const handleRatingChange = (emailId: string, rating: number[]) => {
    setEmailRatings(prev => ({
      ...prev,
      [emailId]: rating[0]
    }));
  };
  
  const handleSubmit = async () => {
    console.log('🔵 Starting onboarding submission process...');
    try {
      setIsSubmitting(true);
      
      // Try to get data from first onboarding step
      let storedQuestions: QuestionWithOptions[] = [];
      let storedAnswers: Record<string, string> = {};
      let domain: string | undefined;
      
      try {
        console.log('🔵 Retrieving data from localStorage...');
        // Get stored questions and answers from localStorage
        const questionsStr = localStorage.getItem('onboardingQuestions');
        const answersStr = localStorage.getItem('onboardingAnswers');
        const domainStr = localStorage.getItem('domain');
        
        if (questionsStr) {
          storedQuestions = JSON.parse(questionsStr);
          console.log(`🔵 Found ${storedQuestions.length} questions in localStorage`);
        }
        if (answersStr) {
          storedAnswers = JSON.parse(answersStr);
          console.log(`🔵 Found ${Object.keys(storedAnswers).length} answers in localStorage`);
        }
        if (domainStr) {
          domain = domainStr;
          console.log(`🔵 Found domain in localStorage: ${domain}`);
        }
      } catch (error) {
        console.error('❌ Error retrieving data from localStorage:', error);
      }
      
      console.log(`🔵 Preparing email data (${emails.length} emails)...`);
      // Prepare simplified email data to avoid serialization issues
      const simplifiedEmails: SimplifiedEmail[] = emails.map(email => ({
        id: email.id,
        subject: email.subject,
        from: email.from && email.from.length > 0 ? [email.from[0]] : [],
        snippet: email.snippet,
        date: email.date
      }));
      console.log('🔵 Simplified email data prepared');
      
      // Prepare onboarding data from both steps
      const onboardingData: OnboardingFormData = {
        // Use data from store first, fall back to localStorage
        questions: questions.length > 0 ? questions : storedQuestions,
        answers: Object.keys(answers).length > 0 ? answers : storedAnswers,
        domain,
        emailRatings,
        ratedEmails: simplifiedEmails
      };
      
      console.log('🔵 Final onboarding data:', {
        questionCount: onboardingData.questions.length,
        answerCount: Object.keys(onboardingData.answers).length,
        domain: onboardingData.domain,
        ratingCount: Object.keys(onboardingData.emailRatings).length,
        emailCount: onboardingData.ratedEmails.length
      });
      
      try {
        console.log('🔵 Sending data to server...');
        // Submit data to backend
        const response = await OnboardingService.submitOnboardingData(onboardingData);
        console.log('🔵 Response received from server:', response);
        
        if (response.error) {
          console.error('❌ Error from server:', response.error);
          toast.error('Failed to save your preferences. We\'ll ask again later.');
          // Still redirect to app even if saving fails - don't block the user
          router.push('/app');
          return;
        }
        
        console.log('✅ Onboarding data submitted successfully');
        if (response.data?.personalitySummary) {
          console.log('✅ Personality summary:', response.data.personalitySummary);
        }
        
        toast.success('Onboarding completed successfully!');
        
        // Clear localStorage onboarding data since it's now saved on the server
        try {
          console.log('🔵 Clearing localStorage...');
          localStorage.removeItem('onboardingQuestions');
          localStorage.removeItem('onboardingAnswers');
          localStorage.removeItem('domain');
          localStorage.removeItem('emailRatings');
          localStorage.removeItem('emailSubjects');
          console.log('✅ localStorage cleared');
        } catch (error) {
          console.error('❌ Error clearing localStorage:', error);
        }
        
        // Redirect to main app
        console.log('🔵 Redirecting to main app...');
        setTimeout(() => {
          router.push('/app');
        }, 1500);
      } catch (apiError) {
        console.error('❌ API call error:', apiError);
        // Try to extract and log response details if available
        if (apiError instanceof Error) {
          console.error('❌ Error message:', apiError.message);
          // @ts-ignore
          if (apiError.response) {
            // @ts-ignore
            console.error('❌ Response status:', apiError.response.status);
            // @ts-ignore
            console.error('❌ Response data:', apiError.response.data);
          }
        }
        throw apiError; // Rethrow to be caught by outer catch
      }
    } catch (error) {
      console.error('❌ Error in handleSubmit:', error);
      toast.error('Something went wrong. You\'ll be redirected to the main app.');
      // Still redirect to app even if error occurs
      setTimeout(() => {
        router.push('/app');
      }, 1500);
    } finally {
      setIsSubmitting(false);
      console.log('🔵 Submission process completed');
    }
  };
  
  if (isLoading) {
    return (
      <div className="flex h-[calc(100vh-80px)] w-full flex-col items-center justify-center">
        <Loader2 size={40} className="animate-spin text-primary" />
        <p className="mt-4 text-lg font-medium">Loading your emails...</p>
      </div>
    );
  }
  
  if (emails.length === 0) {
    return (
      <div className="container mx-auto py-8">
        <Card className="max-w-3xl mx-auto">
          <CardHeader>
            <CardTitle className="text-2xl font-bold">No Emails Found</CardTitle>
            <CardDescription>
              We couldn't find any emails to rate. This could happen if you've just connected your account.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              Let's continue with your onboarding without this step.
            </p>
          </CardContent>
          <CardFooter>
            <Button onClick={() => router.push('/app')}>
              Continue to Dashboard
            </Button>
          </CardFooter>
        </Card>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto py-8">
      <Card className="max-w-4xl mx-auto">
        <CardHeader>
          <CardTitle className="text-2xl font-bold">Rate Your Emails</CardTitle>
          <CardDescription>
            Please rate how important these emails are to you on a scale from 1 to 10. 
            This helps us understand your preferences.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {emails.map((email) => (
              <div key={email.id} className="border rounded-lg p-4">
                <div className="flex items-start gap-3 mb-4">
                  <Mail className="h-5 w-5 text-muted-foreground mt-1" />
                  <div className="flex-1">
                    <h3 className="font-medium text-lg">{email.subject || '(No Subject)'}</h3>
                    <div className="flex flex-wrap gap-2 text-sm text-muted-foreground mb-2">
                      <span>
                        From: {email.from?.[0]?.name || email.from?.[0]?.email || 'Unknown'}
                      </span>
                      <span className="ml-auto">
                        {format(new Date(email.date * 1000), 'MMM d, yyyy')}
                      </span>
                    </div>
                    <p className="text-sm text-muted-foreground line-clamp-2">{email.snippet}</p>
                  </div>
                </div>
                <div className="mt-4">
                  <div className="flex justify-between mb-2 text-sm">
                    <span>Not Important (1)</span>
                    <span>Very Important (10)</span>
                  </div>
                  <div className="flex items-center gap-4">
                    <Slider
                      value={[emailRatings[email.id] || 5]}
                      min={1}
                      max={10}
                      step={1}
                      onValueChange={(value) => handleRatingChange(email.id, value)}
                      className="flex-1"
                    />
                    <span className="text-lg font-medium w-8 text-center">
                      {emailRatings[email.id] || 5}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
        <CardFooter className="flex items-center justify-between">
          <div className="text-sm text-muted-foreground">
            Step 2 of 2: Email Preferences
          </div>
          <Button 
            onClick={handleSubmit} 
            disabled={isSubmitting || emails.length === 0}
          >
            {isSubmitting ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" /> 
                Saving...
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

export default OnboardingEmailRatingPage; 