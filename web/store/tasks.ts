import { TaskResponse } from '@/types/tasks';
import { create } from 'zustand';
import { TasksService } from '@/services/tasks.service';

interface TasksStore {
	tasks: TaskResponse[];
	isLoading: boolean;
	setTasks: (tasks: TaskResponse[]) => void;
	addTask: (task: TaskResponse) => void;
	removeTask: (taskId: string) => void;
	setLoading: (loading: boolean) => void;
	fetchTasks: (userId: string) => Promise<void>;
}

export const useTasksStore = create<TasksStore>((set) => ({
	tasks: [],
	isLoading: false,
	setTasks: (tasks) => set({ tasks }),
	addTask: (task) => set((state) => ({ tasks: [...state.tasks, task] })),
	removeTask: (taskId) =>
		set((state) => ({
			tasks: state.tasks.filter((task) => task.task_id !== taskId),
		})),
	setLoading: (loading) => set({ isLoading: loading }),
	fetchTasks: async (userId: string) => {
		try {
			set({ isLoading: true });
			const response = await TasksService.getUserTasks(userId);
			console.log('Tasks fetched:', response.data);
			set({ tasks: response.data ?? [] });
		} catch (error) {
			console.error('Failed to fetch tasks:', error);
		} finally {
			set({ isLoading: false });
		}
	},
}));
