import { ApiClient } from '@/lib/api-client';
import { Email, EmailResponse, GetEmailOptions } from '@/types/nylasEmail';

export interface EmailParticipant {
	name: string;
	email: string;
}

export interface EmailMessage {
	id: string;
	subject: string;
	from: EmailParticipant[];
	to: EmailParticipant[];
	cc: EmailParticipant[];
	bcc: EmailParticipant[];
	date: number;
	snippet: string;
	body: string;
	unread: boolean;
	starred: boolean;
}

export interface EmailMessageList {
	messages: EmailMessage[];
	next_cursor: string | null;
}

/**
 * Service class for handling Nylas email operations
 */
export default class EmailService {
	/**
	 * Fetches emails from Nylas
	 * @param limit Number of emails to fetch (max 100)
	 * @param offset Pagination cursor
	 * @param params Additional query parameters
	 * @returns List of email messages
	 */

	static async getEmails(options: GetEmailOptions) {
		return await ApiClient.get<EmailResponse>('/api/nylas/email/messages', {
			...options,
		});
	}

	static async getOnboardingEmails(options: GetEmailOptions) {
		return await ApiClient.get<EmailResponse>('/api/nylas/email/onboarding/message', {
			...options,
		});
	}

	static async getEmailById(messageId: string) {
		return await ApiClient.get<Email>(`/api/nylas/email/messages/${messageId}`);
	}
}
