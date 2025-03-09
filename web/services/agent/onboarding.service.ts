import { ApiClient } from '@/lib/api-client';
import { EmailMessage } from '@/services/nylas/email.service';

// Define a simplified email type to avoid serialization issues
export interface SimplifiedEmail {
  id: string;
  subject: string;
  // IMPORTANT: This needs to match the expected format on the server
  // The server expects 'from', but will convert it to 'from_' with the alias
  from: Array<{
    name: string;
    email: string;
  }>;
  snippet?: string;
  date?: number;
}

export interface OnboardingFormData {
  // Step 1: Domain-specific questions and answers
  questions: {
    question: string;
    options: string[];
  }[];
  answers: Record<string, string>;
  domain?: string;
  
  // Step 2: Email ratings
  emailRatings: Record<string, number>;
  ratedEmails: SimplifiedEmail[];
}

export interface PersonalitySummaryResponse {
  success: boolean;
  message: string;
  personalitySummary?: string;
}

/**
 * Service for handling user onboarding data
 */
export class OnboardingService {
  /**
   * Submit onboarding data to generate and save user personality
   * @param data Onboarding form data and email ratings
   * @returns Personality summary
   */
  static async submitOnboardingData(data: OnboardingFormData) {
    console.log('🟡 ONBOARDING SERVICE: Submitting data to API');
    
    // Deep clone and log exactly what we're sending
    const clonedData = JSON.parse(JSON.stringify(data));
    console.log('🟡 ONBOARDING SERVICE: Full request payload:', clonedData);
    
    try {
      const response = await ApiClient.post<PersonalitySummaryResponse>('/api/agent/submit-onboarding', data);
      console.log('🟡 ONBOARDING SERVICE: Response received:', response);
      return response;
    } catch (error) {
      console.error('🟡 ONBOARDING SERVICE: Error during API call:', error);
      // Log additional axios error details if available
      if (error && (error as any).response) {
        const axiosError = error as any;
        console.error('🟡 ONBOARDING SERVICE: Response status:', axiosError.response.status);
        console.error('🟡 ONBOARDING SERVICE: Response data:', axiosError.response.data);
        
        // For 422 errors, log the validation errors in detail
        if (axiosError.response.status === 422 && axiosError.response.data?.detail) {
          console.error('🟡 VALIDATION ERRORS:');
          axiosError.response.data.detail.forEach((err: any, index: number) => {
            console.error(`Error ${index + 1}:`, {
              location: err.loc,
              type: err.type,
              message: err.msg
            });
          });
        }
      }
      throw error;
    }
  }
} 