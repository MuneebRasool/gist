import { create } from 'zustand';
import { TaskEmailResponse } from '@/types/tasks';
import { TasksService } from '@/services/tasks.service';

interface LibraryTasksState {
	tasks: TaskEmailResponse[];
	isLoading: boolean;
	fetchTasks: (userId: string) => Promise<void>;
	setTasks: (tasks: TaskEmailResponse[]) => void;
	setLoading: (loading: boolean) => void;
	addTask: (task: TaskEmailResponse) => void;
	removeTask: (messageId: string) => void;
	updateTask: (messageId: string, updatedTask: Partial<TaskEmailResponse>) => void;
}

export const useLibraryTasksStore = create<LibraryTasksState>((set) => ({
	tasks: [],
	isLoading: false,

	setTasks: (tasks) => set({ tasks }),

	setLoading: (loading) => set({ isLoading: loading }),

	fetchTasks: async (userId) => {
		set({ isLoading: true });
		try {
			const response = await TasksService.getUserLibraryTasks(userId);
			if (response.data) {
				set({ tasks: response.data });
			}
		} catch (error) {
			console.error('Error fetching library tasks:', error);
		} finally {
			set({ isLoading: false });
		}
	},

	addTask: (task) => set((state) => ({ tasks: [...state.tasks, task] })),

	removeTask: (messageId) =>
		set((state) => ({
			tasks: state.tasks.filter((task) => task.messageId !== messageId),
		})),

	updateTask: (messageId, updatedTask) =>
		set((state) => ({
			tasks: state.tasks.map((task) => (task.messageId === messageId ? { ...task, ...updatedTask } : task)),
		})),
}));
