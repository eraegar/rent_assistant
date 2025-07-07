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
  refreshProfile: () => Promise<void>;
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
            
            set({ token, isAuthenticated: true });
            localStorage.setItem('manager_token', token);
            
            // Get profile
            await get().refreshProfile();
            set({ loading: false });
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

      refreshProfile: async () => {
        const token = get().token || localStorage.getItem('manager_token');
        if (!token) return;

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
          } else {
            // Token invalid
            get().logout();
          }
        } catch (error) {
          console.error('Profile refresh error:', error);
          get().logout();
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