/**
 * Task creation request
 */
export interface TaskCreate {
	task: string;
	messageId?: string;
	deadline?: string;
	userId: string;
}

/**
 * Task update request
 */
export interface TaskUpdate {
	task?: string;
	deadline?: string;
}

/**
 * Task response
 */
export interface TaskResponse {
	task_id: string;
	task: string;
	deadline?: string;
	priority: 'high' | 'medium' | 'low';
	relevance_score?: number;
	utility_score?: number;
	cost_score?: number;
	messageId?: string;
	userId: string;
	classification?: string;
	createdAt: string;
	updatedAt: string;
}
