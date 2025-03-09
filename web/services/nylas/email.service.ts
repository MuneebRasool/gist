import { ApiClient } from '@/lib/api-client';
import { Email, EmailResponse, GetEmailOptions } from '@/types/nylasEmail';

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
	static async getEmailById(messageId: string) {
		return await ApiClient.get<Email>(`/api/nylas/email/messages/${messageId}`);
	}
}
