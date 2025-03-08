import { ApiClient } from '@/lib/api-client';
import { ProcessEmailsRequest, SpamClassificationResponse, ExtractTaskBatchResponse, ContentClassificationResponse, ContentClassificationRequest } from '@/types/agent';

/**
 * Agent service for email processing and task extraction
 */
export class AgentService {
	/**
	 * Extract tasks from a batch of emails
	 * @param data Process emails request data
	 */
	static async extractTaskBatch(data: ProcessEmailsRequest) {
		return await ApiClient.post<ExtractTaskBatchResponse>('/api/agent/extract-task-batch', data);
	}

	/**
	 * Classify spam emails from a batch of emails
	 * @param data Process emails request data
	 */
	static async classifySpams(data: ProcessEmailsRequest) {
		return await ApiClient.post<SpamClassificationResponse>('/api/agent/classify-spams', data);
	}

	/**
	 * Classify content by type and usefulness
	 * @param content Text content to classify
	 */
	static async classifyContent(content: string) {
		const request: ContentClassificationRequest = { content };
		return await ApiClient.post<ContentClassificationResponse>('/api/agent/classify-content', request);
	}
}
