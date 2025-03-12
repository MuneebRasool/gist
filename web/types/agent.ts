import { EmailParticipant } from './nylasEmail';

/**
 * Email data structure
 */
export interface ExtractedEmailData {
	id: string;
	subject: string;
	from_: EmailParticipant[];
	body: string;
}

/**
 * Process emails request
 */
export interface ProcessEmailsRequest {
	emails: ExtractedEmailData[];
}

/**
 * Extract task batch response
 */
export interface ExtractTaskBatchResponse {
	success: boolean;
	message: string;
}

/**
 * Spam classification response
 */
export interface SpamClassificationResponse {
	spam: ExtractedEmailData[];
	non_spam: ExtractedEmailData[];
}

/**
 * Content classification request
 */
export interface ContentClassificationRequest {
	content: string;
}

/**
 * Content classification response
 */
export interface ContentClassificationResponse {
	success: boolean;
	message: string;
	type: string;
}

/**
 * Domain inference request
 */
export interface DomainInferenceRequest {
	email: string;
	ratedEmails?: Array<{
		id: string;
		subject: string;
		from: Array<{
			name: string;
			email: string;
		}>;
		snippet?: string;
		date?: number;
	}>;
	ratings?: Record<string, number>;
}

/**
 * Question with options structure
 */
export interface QuestionWithOptions {
	question: string;
	options: string[];
}

/**
 * Domain inference response
 */
export interface DomainInferenceResponse {
	success: boolean;
	message: string;
	questions: QuestionWithOptions[];
	summary?: string;
	domain?: string;
}
