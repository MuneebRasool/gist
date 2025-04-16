import { ApiClient } from '@/lib/api-client';

interface ApiError {
	message: string;
	status: number;
}

interface ApiResponse<T> {
	data: T | null;
	error: ApiError | null;
}

interface TaskReorderRequest {
	task_id: string;
	direction: 'up' | 'down';
	positions: number;
	task_above_id?: string;
	task_below_id?: string;
	classification: string;
}

interface TaskReorderResponse {
	task_id: string;
	relevance_score?: number;
	utility_score?: number;
	cost_score?: number;
	success: boolean;
	message: string;
}

export class FeedbackService {
	/**
	 * Send task reordering feedback to the server
	 */
	static async reorderTask(
		taskId: string,
		direction: 'up' | 'down',
		positions: number,
		taskAboveId?: string,
		taskBelowId?: string,
		classification?: string
	): Promise<ApiResponse<TaskReorderResponse>> {
		try {
			const payload: TaskReorderRequest = {
				task_id: taskId,
				direction,
				positions,
				task_above_id: taskAboveId,
				task_below_id: taskBelowId,
				classification: classification || '',
			};
			const response = await ApiClient.post<TaskReorderResponse>('/api/feedback/re-order', payload);

			return {
				data: response.data || null, // Ensure data is null if undefined
				error: null,
			};
		} catch (error: any) {
			console.error('Error reordering task:', error);
			return {
				data: null,
				error: {
					message: error.response?.data?.detail || 'Failed to reorder task',
					status: error.response?.status || 500,
				},
			};
		}
	}
}
