import { ApiClient } from '@/lib/api-client';
import { EmailMessage } from '@/services/nylas/email.service';

// Define a simplified email type to avoid serialization issues
export interface SimplifiedEmail {
	id: string;
	subject: string;
	body: string;
	from: Array<{
		name: string;
		email: string;
	}>;
	snippet?: string;
	date?: number;
}

export interface QuestionWithOptions {
	question: string;
	options: string[];
}

export interface DomainInferenceResponse {
	success: boolean;
	message: string;
	questions: QuestionWithOptions[];
	summary: string;
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
		try {
			const response = await ApiClient.post<PersonalitySummaryResponse>('/api/agent/submit-onboarding', data);
			return response;
		} catch (error) {
			// Log additional axios error details if available
			if (error && (error as any).response) {
				const axiosError = error as any;

				// For 422 errors, log the validation errors in detail
				if (axiosError.response.status === 422 && axiosError.response.data?.detail) {
					axiosError.response.data.detail.forEach((err: any, index: number) => {
						console.error(`Error ${index + 1}:`, {
							location: err.loc,
							type: err.type,
							message: err.msg,
						});
					});
				}
			}
			throw error;
		}
	}

	/**
	 * Update domain inference with rated emails
	 * @param email User's email address
	 * @param ratedEmails List of emails rated by the user
	 * @returns Domain inference results with questions
	 */
	static async updateDomainInference(email: string, ratedEmails: SimplifiedEmail[]) {
		const payload = {
			email,
			ratedEmails,
		};
		return await ApiClient.post<DomainInferenceResponse>('/api/agent/infer-domain', payload);
	}

	static async startOnboarding() {
		return ApiClient.post<OnboardingFormData>('/api/agent/start-onboarding');
	}
}
