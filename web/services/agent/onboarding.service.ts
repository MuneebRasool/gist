import { ApiClient } from '@/lib/api-client';
import { EmailMessage } from '@/services/nylas/email.service';

// Define a simplified email type to avoid serialization issues
export interface SimplifiedEmail {
  id: string;
  subject: string;
  from: Array<{ name: string; email: string }>;
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
    return await ApiClient.post<PersonalitySummaryResponse>('/api/agent/submit-onboarding', data);
  }
} 