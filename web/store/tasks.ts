import { TaskResponse } from '@/types/tasks';
import { create } from 'zustand';
import { TasksService } from '@/services/tasks.service';


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
}));