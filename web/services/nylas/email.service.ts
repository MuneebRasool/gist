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
	static async getMessages(limit: number = 10, offset?: string, params?: Record<string, any>) {
		const queryParams = new URLSearchParams();
		
		// Add limit and offset
		queryParams.append('limit', limit.toString());
		if (offset) {
			queryParams.append('offset', offset);
		}
		
		// Add any additional params
		if (params) {
			Object.entries(params).forEach(([key, value]) => {
				if (value !== undefined && value !== null) {
					queryParams.append(key, value.toString());
				}
			});
		}
		
		const query = queryParams.toString();
		return await ApiClient.get<EmailMessageList>(`/api/nylas/messages${query ? `?${query}` : ''}`);
	}

	static async getEmails(options: GetEmailOptions) {
		return await ApiClient.get<EmailResponse>('/api/nylas/email/messages', {
			...options,
		});
	}
	static async getEmailById(messageId: string) {
		return await ApiClient.get<Email>(`/api/nylas/email/messages/${messageId}`);
	}
}
