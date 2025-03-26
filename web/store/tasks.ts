import { TaskResponse } from '@/types/tasks';
import { create } from 'zustand';
import { TasksService } from '@/services/tasks.service';
import { FeedbackService } from '@/services/feedback.service';
import { toast } from 'sonner';

const CACHE_DURATION = 60 * 1000;

interface CachedTasks {
	tasks: TaskResponse[];
	expiry: number;
}

/**
 * Get cached tasks for a specific user
 */
const getCachedTasks = (userId: string): TaskResponse[] | null => {
	try {
		const cachedData = localStorage.getItem(`tasks_${userId}`);
		if (!cachedData) return null;

		const { tasks, expiry }: CachedTasks = JSON.parse(cachedData);
		if (Date.now() > expiry) {
			localStorage.removeItem(`tasks_${userId}`);
			return null;
		}

		return tasks;
	} catch (error) {
		console.error('Error retrieving cached tasks:', error);
		return null;
	}
};

/**
 * Cache tasks for a specific user
 */
const setCachedTasks = (userId: string, tasks: TaskResponse[]) => {
	try {
		const cachedData: CachedTasks = {
			tasks,
			expiry: Date.now() + CACHE_DURATION,
		};
		localStorage.setItem(`tasks_${userId}`, JSON.stringify(cachedData));
	} catch (error) {
		console.error('Error caching tasks:', error);
	}
};

interface TasksStore {
	tasks: TaskResponse[];
	isLoading: boolean;
	currentUserId: string | null;
	setUserId: (userId: string) => void;
	setTasks: (tasks: TaskResponse[]) => void;
	addTask: (task: TaskResponse) => void;
	removeTask: (taskId: string) => void;
	setLoading: (loading: boolean) => void;
	fetchTasks: (userId: string, forceRefresh?: boolean) => Promise<void>;
	updateTaskOrder: (taskIds: string[]) => void;
	reorderTask: (
		taskId: string,
		oldIndex: number,
		newIndex: number,
		classification: string,
		reorderedTasks: TaskResponse[]
	) => Promise<void>;
}

export const useTasksStore = create<TasksStore>((set, get) => ({
	tasks: [],
	isLoading: false,
	currentUserId: null,

	setUserId: (userId) => set({ currentUserId: userId }),

	setTasks: (tasks) => {
		const { currentUserId } = get();
		set({ tasks });
		if (currentUserId) {
			setCachedTasks(currentUserId, tasks);
		}
	},

	addTask: (task) =>
		set((state) => {
			const { currentUserId } = get();
			const updatedTasks = [...state.tasks, task];
			if (currentUserId) {
				setCachedTasks(currentUserId, updatedTasks);
			}
			return { tasks: updatedTasks };
		}),

	removeTask: (taskId) =>
		set((state) => {
			const { currentUserId } = get();
			const updatedTasks = state.tasks.filter((task) => task.task_id !== taskId);
			if (currentUserId) {
				setCachedTasks(currentUserId, updatedTasks);
			}
			return { tasks: updatedTasks };
		}),

	setLoading: (loading) => set({ isLoading: loading }),

	fetchTasks: async (userId: string, forceRefresh = false) => {
		// Set current user ID
		set({ currentUserId: userId });

		// Check cache first (unless forced refresh is requested)
		if (!forceRefresh) {
			const cachedTasks = getCachedTasks(userId);
			if (cachedTasks) {
				set({ tasks: cachedTasks });
				return;
			}
		}
		// Fetch from API
		try {
			set({ isLoading: true });
			const response = await TasksService.getUserTasks(userId);
			const tasks = response.data ?? [];
			set({ tasks });
			setCachedTasks(userId, tasks);
		} catch (error) {
			console.error('Failed to fetch tasks:', error);
		} finally {
			set({ isLoading: false });
		}
	},

	/**
	 * Update the order of tasks based on an array of task IDs
	 * This is used for drag-and-drop reordering
	 */
	updateTaskOrder: (taskIds) => {
		set((state) => {
			const { currentUserId } = get();

			// Create a map for quick lookup of tasks by ID
			const taskMap = new Map(state.tasks.map((task) => [task.task_id, task]));

			// Create a new array of tasks in the specified order
			// For any task IDs that don't exist in the current tasks, they are ignored
			const orderedTasks = taskIds
				.map((id) => taskMap.get(id))
				.filter((task): task is TaskResponse => task !== undefined);

			// Add any tasks that weren't in the taskIds array (maintain their original order)
			const remainingTasks = state.tasks.filter((task) => !taskIds.includes(task.task_id));
			const updatedTasks = [...orderedTasks, ...remainingTasks];

			// Update cache if we have a user ID
			if (currentUserId) {
				setCachedTasks(currentUserId, updatedTasks);
			}

			return { tasks: updatedTasks };
		});
	},

	/**
	 * Reorder a task and send feedback to the backend
	 * @param taskId - ID of the task being reordered
	 * @param oldIndex - Original index of the task
	 * @param newIndex - New index of the task
	 * @param classification - Classification of the task (Main Focus-View, Drawer, Library)
	 * @param reorderedTasks - The array of tasks after reordering
	 */
	reorderTask: async (taskId, oldIndex, newIndex, classification, reorderedTasks) => {
		const { tasks, setTasks } = get();

		// Calculate direction and positions moved
		const direction = newIndex < oldIndex ? 'up' : 'down';
		const positions = Math.abs(newIndex - oldIndex);

		// Find the tasks above and below the reordered task in the new order
		// These must have the same classification
		const taskIndex = reorderedTasks.findIndex((task) => task.task_id === taskId);

		// Find task above (if any) with the same classification
		let taskAboveId: string | undefined;
		for (let i = taskIndex - 1; i >= 0; i--) {
			if (reorderedTasks[i].classification === classification) {
				taskAboveId = reorderedTasks[i].task_id;
				break;
			}
		}

		// Find task below (if any) with the same classification
		let taskBelowId: string | undefined;
		for (let i = taskIndex + 1; i < reorderedTasks.length; i++) {
			if (reorderedTasks[i].classification === classification) {
				taskBelowId = reorderedTasks[i].task_id;
				break;
			}
		}

		try {
			// Call the API to update the task's relevance score
			const response = await FeedbackService.reorderTask(
				taskId,
				direction,
				positions,
				taskAboveId,
				taskBelowId,
				classification
			);

			if (response.error) {
				toast.error(`Failed to update task order: ${response.error.message}`);
				return;
			}

			if (response.data) {
				// Update the task in the store with the new scores
				const updatedTasks = tasks.map((task) => {
					if (task.task_id === taskId) {
						return {
							...task,
							relevance_score: response.data?.relevance_score ?? task.relevance_score,
							utility_score: response.data?.utility_score ?? task.utility_score,
							cost_score: response.data?.cost_score ?? task.cost_score,
						};
					}
					return task;
				});

				setTasks(updatedTasks);
				toast.success('Task order updated');
			}
		} catch (error) {
			console.error('Error reordering task:', error);
			toast.error('Failed to update task order');
		}
	},
}));
