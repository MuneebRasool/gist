import { ApiClient } from '@/lib/api-client';
import { TaskCreate, TaskUpdate, TaskResponse, TaskEmailResponse } from '@/types/tasks';

/**
 * Tasks service for managing tasks
 */
export class TasksService {
	/**
	 * Create a new task
	 * @param data Task creation data
	 */
	static async createTask(data: TaskCreate) {
		return await ApiClient.post<TaskResponse>('/api/tasks/', data);
	}

	/**
	 * Get a task by task ID
	 * @param taskId Task ID
	 */
	static async getTask(taskId: string) {
		return await ApiClient.get<TaskResponse>(`/api/tasks/id/${taskId}`);
	}

	/**
	 * Get a task by message ID
	 * @param messageId Message ID
	 */
	static async getTaskByMessageId(messageId: string) {
		return await ApiClient.get<TaskResponse>(`/api/tasks/message/${messageId}`);
	}

	/**
	 * Get all tasks for a specific user
	 * @param userId User ID
	 */
	static async getUserTasks(userId: string) {
		return await ApiClient.get<TaskResponse[]>(`/api/tasks/user/${userId}`);
	}
	/**
	 * Get all tasks for a specific user in the library
	 * @param userId User ID
	 */
	static async getUserLibraryTasks(userId: string) {
		return await ApiClient.get<TaskEmailResponse[]>(`/api/tasks/${userId}/emails/library`);
	}
	/**
	 * Get all tasks for a specific user in the drawer
	 * @param userId User ID
	 */
	static async getUserDrawerTasks(userId: string) {
		return await ApiClient.get<TaskEmailResponse[]>(`/api/tasks/${userId}/emails/drawer`);
	}

	/**
	 * Update a task
	 * @param taskId Task ID
	 * @param data Update data
	 */
	static async updateTask(taskId: string, data: TaskUpdate) {
		return await ApiClient.patch<TaskResponse>(`/api/tasks/${taskId}`, data);
	}

	/**
	 * Delete a task
	 * @param taskId Task ID
	 */
	static async deleteTask(taskId: string) {
		return await ApiClient.delete(`/api/tasks/${taskId}`);
	}
}
