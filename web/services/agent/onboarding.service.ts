import { ApiClient } from '@/lib/api-client';
import { EmailMessage } from '@/services/nylas/email.service';
import { envConfig } from '@/config';
import { EventSource } from 'eventsource';
import { getServerSession } from 'next-auth';
import { getSession } from 'next-auth/react';
import { authOptions } from '@/lib/auth';


// Extend EventSourceInit to include headers
interface ExtendedEventSourceInit extends EventSourceInit {
	headers?: Record<string, string>;
}

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

export interface OnboardingStatusEvent {
	status: 'connected' | 'processing' | 'completed' | 'error';
	message?: string;
	timestamp: string;
}

const SSE_CONFIG = {
	RETRY_INTERVAL: 3000, // 3 seconds
	MAX_RETRIES: 3,
	TIMEOUT: 120000, // 30 seconds
};

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

	/**
	 * Check if onboarding has been completed
	 * @returns Onboarding status
	 */
	static async checkOnboardingStatus() {
		return ApiClient.get<{ onboarding: boolean; task_gen : boolean; in_progress: boolean; success: boolean }>('/api/agent/onboarding-check');
	}

	/**
	 * Create an SSE connection to listen for onboarding status updates
	 * @param onStatusUpdate Callback function for status updates
	 * @param onError Callback function for errors
	 * @returns EventSource connection that should be closed when no longer needed
	 */
	static async createStatusStream(
		onStatusUpdate: (data: OnboardingStatusEvent) => void,
		onError?: (error: Event) => void
	): Promise<EventSource> {
		let retryCount = 0;
		const baseUrl = envConfig.API_URL;
		
		// Get session using the same method as ApiClient
		const session = await getSession();
		if (!session?.user?.token) {
			throw new Error('No authentication token available');
		}
		
		// Use the token as a URL parameter
		const url = new URL(`${baseUrl}/api/agent/onboarding-status`);
		url.searchParams.append('token', session.user.token);
		
		// Create EventSource with proper headers
		// Note: Headers may not work in all browsers with EventSource
		// but we include them anyway as a fallback
		const eventSource = new EventSource(url.toString(), {
			headers: {
				Authorization: `Bearer ${session.user.token}`
			}
		} as ExtendedEventSourceInit);

		let connectionTimeout: NodeJS.Timeout;

		const resetTimeout = () => {
			if (connectionTimeout) clearTimeout(connectionTimeout);
			connectionTimeout = setTimeout(() => {
				console.error('SSE connection timeout');
				eventSource.close();
				onStatusUpdate({
					status: 'error',
					message: 'Connection timeout',
					timestamp: new Date().toISOString(),
				});
			}, SSE_CONFIG.TIMEOUT);
		};

		eventSource.onopen = () => {
			console.log('SSE connection opened');
			retryCount = 0;
			resetTimeout();
		};

		eventSource.onmessage = (event: MessageEvent) => {
			try {
				resetTimeout();
				const data = JSON.parse(event.data) as OnboardingStatusEvent;
				onStatusUpdate(data);
				
				if (data.status === 'completed') {
					if (connectionTimeout) clearTimeout(connectionTimeout);
					eventSource.close();
				}
			} catch (error) {
				console.error('Failed to parse SSE message:', error);
				onStatusUpdate({
					status: 'error',
					message: 'Failed to parse server message',
					timestamp: new Date().toISOString(),
				});
			}
		};

		eventSource.onerror = (error: Event) => {
			console.error('SSE connection error:', error);
			if (connectionTimeout) clearTimeout(connectionTimeout);

			if (retryCount < SSE_CONFIG.MAX_RETRIES) {
				retryCount++;
				console.log(`Retrying connection (${retryCount}/${SSE_CONFIG.MAX_RETRIES})`);
				setTimeout(() => {
					// Attempt to reconnect
					if (eventSource.readyState === EventSource.CLOSED) {
						onStatusUpdate({
							status: 'error',
							message: 'Attempting to reconnect...',
							timestamp: new Date().toISOString(),
						});
					}
				}, SSE_CONFIG.RETRY_INTERVAL);
			} else {
				eventSource.close();
				onStatusUpdate({
					status: 'error',
					message: 'Connection failed after multiple retries',
					timestamp: new Date().toISOString(),
				});
			}

			if (onError) onError(error);
		};

		return eventSource;
	}

	/**
	 * Safely close an SSE connection
	 * This method should be called when redirecting or when the component unmounts
	 * @param eventSource The EventSource connection to close
	 */
	static closeStatusStream(eventSource: any): void {
		if (eventSource) {
			console.log('Safely closing SSE connection');
			eventSource.close();
		}
	}
}
