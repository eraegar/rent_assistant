import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface Manager {
  id: number;
  name: string;
  email: string;
  department: string;
}

interface ManagerStore {
  manager: Manager | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (phone: string, password: string) => Promise<boolean>;
  logout: () => void;
  refreshProfile: () => Promise<Manager | null>;
}

// API base URL
const API_BASE_URL = 'https://api.rent-assistant.ru';

export const useManagerStore = create<ManagerStore>()(
  persist(
    (set, get) => ({
      manager: null,
      token: null,
      isAuthenticated: false,
      loading: false,

      login: async (phone: string, password: string): Promise<boolean> => {
        set({ loading: true });
        try {
          const response = await fetch(`${API_BASE_URL}/api/v1/management/auth/login`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ phone, password }),
          });

          if (response.ok) {
            const data = await response.json();
            const token = data.access_token;
            
            // Сохраняем токен в localStorage перед обновлением профиля
            localStorage.setItem('manager_token', token);
            set({ token }); // Устанавливаем токен в состояние
            
            // Обновляем профиль и получаем данные менеджера
            const manager = await get().refreshProfile();
            
            set({ manager, isAuthenticated: true, loading: false });
            return true;
          } else {
            set({ loading: false });
            return false;
          }
        } catch (error) {
          console.error('Login error:', error);
          set({ loading: false });
          return false;
        }
      },

      logout: () => {
        localStorage.removeItem('manager_token');
        set({ 
          manager: null, 
          token: null, 
          isAuthenticated: false 
        });
      },

      refreshProfile: async (): Promise<Manager | null> => {
        const token = get().token || localStorage.getItem('manager_token');
        if (!token) return null;

        try {
          const response = await fetch(`${API_BASE_URL}/api/v1/management/profile`, {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          });

          if (response.ok) {
            const manager = await response.json();
            set({ manager, isAuthenticated: true, token });
            return manager;
          } else {
            // Token invalid
            get().logout();
            return null;
          }
        } catch (error) {
          console.error('Profile refresh error:', error);
          get().logout();
          return null;
        }
      },
    }),
    {
      name: 'manager-storage',
      partialize: (state) => ({
        token: state.token,
        manager: state.manager,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
); 