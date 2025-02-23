import { ApiClient } from '@/lib/api-client';

type getEmailOptions = {
	limit?: number;
	offset?: string;
	unread?: boolean;
	starred?: boolean;
	in_folder?: string;
	subject?: string;
};

export class EmailService {
	static async getEmails(options: getEmailOptions) {
		return await ApiClient.get('/api/nylas/email/messages', {
			...options,
		});
	}
}
