import { ApiClient } from '@/lib/api-client';
import { Email, EmailResponse, GetEmailOptions } from '@/types/nylasEmail';

export default class EmailService {
	static async getEmails(options: GetEmailOptions) {
		return await ApiClient.get<EmailResponse>('/api/nylas/email/messages', {
			...options,
		});
	}
	static async getEmailById(messageId: string) {
		return await ApiClient.get<Email>(`/api/nylas/email/messages/${messageId}`);
	}
}
