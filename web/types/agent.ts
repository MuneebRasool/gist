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
