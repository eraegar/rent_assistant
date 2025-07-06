import { create } from 'zustand';
import { Task, TaskType, TaskStatus, TaskState } from '../types';
import { apiService } from '../services/api';

interface TaskStore extends TaskState {
  loadTasks: () => Promise<void>;
  fetchTasks: () => Promise<void>;
  createTask: (title: string, description: string, type: TaskType) => Promise<boolean>;
  updateTask: (taskId: string, updates: Partial<Task>) => Promise<boolean>;
  updateTaskStatus: (taskId: string, status: TaskStatus, result?: string) => Promise<boolean>;
  setLoading: (loading: boolean) => void;
  completedTasks: Task[];
  pendingTasks: Task[];
  waitingTasks: Task[];
}

export const useTaskStore = create<TaskStore>((set, get) => ({
  tasks: [],
  isLoading: false,

  get completedTasks() {
    return get().tasks.filter(task => task.status === TaskStatus.COMPLETED);
  },

  get pendingTasks() {
    return get().tasks.filter(task => 
      task.status === TaskStatus.PENDING || task.status === TaskStatus.IN_PROGRESS
    );
  },

  get waitingTasks() {
    return get().tasks.filter(task => task.status === TaskStatus.WAITING_CLIENT);
  },

  setLoading: (loading: boolean) => {
    set({ isLoading: loading });
  },

  loadTasks: async () => {
    set({ isLoading: true });
    try {
      const response = await apiService.getTasks();
      if (response.success && response.data) {
        set({ tasks: response.data, isLoading: false });
      } else {
        set({ isLoading: false });
      }
    } catch (error) {
      console.error('Load tasks error:', error);
      set({ isLoading: false });
    }
  },

  fetchTasks: async () => {
    set({ isLoading: true });
    try {
      const response = await apiService.getTasks();
      if (response.success && response.data) {
        set({ tasks: response.data, isLoading: false });
      } else {
        set({ isLoading: false });
      }
    } catch (error) {
      console.error('Fetch tasks error:', error);
      set({ isLoading: false });
    }
  },

  updateTask: async (taskId: string, updates: Partial<Task>): Promise<boolean> => {
    try {
      // For now, we'll update the local state only since the API method doesn't exist yet
      const { tasks } = get();
      const updatedTasks = tasks.map(task => 
        task.id === taskId ? { ...task, ...updates } : task
      );
      set({ tasks: updatedTasks });
      return true;
    } catch (error) {
      console.error('Update task error:', error);
      return false;
    }
  },

  createTask: async (title: string, description: string, type: TaskType): Promise<boolean> => {
    set({ isLoading: true });
    try {
      console.log('Creating task:', { title, description, type });
      const response = await apiService.createTask(title, description, type);
      console.log('Task creation response:', response);
      
      if (response.success && response.data) {
        const { tasks } = get();
        set({ 
          tasks: [response.data, ...tasks],
          isLoading: false 
        });
        console.log('Task created successfully:', response.data);
        return true;
      } else {
        console.error('Task creation failed:', response.message);
        set({ isLoading: false });
        return false;
      }
    } catch (error) {
      console.error('Create task error:', error);
      set({ isLoading: false });
      return false;
    }
  },

  updateTaskStatus: async (taskId: string, status: TaskStatus, result?: string): Promise<boolean> => {
    try {
      const response = await apiService.updateTaskStatus(taskId, status, result);
      if (response.success) {
        const { tasks } = get();
        const updatedTasks = tasks.map(task => 
          task.id === taskId 
            ? { ...task, status, result, updated_at: new Date().toISOString() }
            : task
        );
        set({ tasks: updatedTasks });
        return true;
      }
      return false;
    } catch (error) {
      console.error('Update task status error:', error);
      return false;
    }
  }
})); 