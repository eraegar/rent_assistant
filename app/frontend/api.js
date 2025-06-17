// API Configuration
const API_BASE_URL = window.location.origin;
const API_ENDPOINTS = {
    login: '/auth/login',
    register: '/auth/register',
    me: '/auth/me',
    tasks: '/tasks',
    taskStats: '/tasks/stats/overview',
    monthlyAnalytics: '/tasks/analytics/monthly',
    typeAnalytics: '/tasks/analytics/types'
};

// Auth token management
class AuthManager {
    static getToken() {
        return localStorage.getItem('auth_token');
    }

    static setToken(token) {
        localStorage.setItem('auth_token', token);
    }

    static removeToken() {
        localStorage.removeItem('auth_token');
    }

    static getAuthHeaders() {
        const token = this.getToken();
        return token ? { 'Authorization': `Bearer ${token}` } : {};
    }

    static isAuthenticated() {
        return !!this.getToken();
    }
}

// API Client
class ApiClient {
    static async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...AuthManager.getAuthHeaders(),
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            
            if (response.status === 401) {
                AuthManager.removeToken();
                window.location.reload();
                return;
            }

            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.detail || `HTTP error! status: ${response.status}`);
            }

            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            }
            return response;
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    static async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    static async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    static async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    static async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}

// Auth API
class AuthAPI {
    static async login(phone, password) {
        try {
            const response = await ApiClient.post(API_ENDPOINTS.login, {
                phone,
                password
            });
            
            if (response.access_token) {
                AuthManager.setToken(response.access_token);
            }
            
            return response;
        } catch (error) {
            throw new Error('Неверный номер телефона или пароль');
        }
    }

    static async register(name, phone, password) {
        const data = { name, phone, password };
        console.log('🚀 Sending registration data:', data);
        
        try {
            const response = await ApiClient.post(API_ENDPOINTS.register, data);
            console.log('✅ Registration successful:', response);
            return response;
        } catch (error) {
            console.error('❌ Registration failed:', error);
            console.error('❌ Error details:', error.message);
            throw new Error('Ошибка регистрации. Возможно, этот номер уже зарегистрирован.');
        }
    }

    static async getCurrentUser() {
        return ApiClient.get(API_ENDPOINTS.me);
    }

    static logout() {
        AuthManager.removeToken();
        window.location.reload();
    }
}

// Tasks API
class TasksAPI {
    static async getTasks(filters = {}) {
        const params = new URLSearchParams();
        Object.keys(filters).forEach(key => {
            if (filters[key] !== null && filters[key] !== undefined) {
                params.append(key, filters[key]);
            }
        });
        
        const endpoint = params.toString() ? 
            `${API_ENDPOINTS.tasks}?${params.toString()}` : 
            API_ENDPOINTS.tasks;
            
        return ApiClient.get(endpoint);
    }

    static async createTask(taskData) {
        return ApiClient.post(API_ENDPOINTS.tasks, taskData);
    }

    static async getTask(taskId) {
        return ApiClient.get(`${API_ENDPOINTS.tasks}/${taskId}`);
    }

    static async updateTask(taskId, updateData) {
        return ApiClient.put(`${API_ENDPOINTS.tasks}/${taskId}`, updateData);
    }

    static async deleteTask(taskId) {
        return ApiClient.delete(`${API_ENDPOINTS.tasks}/${taskId}`);
    }

    static async getTaskStats() {
        return ApiClient.get(API_ENDPOINTS.taskStats);
    }

    static async getMonthlyAnalytics() {
        return ApiClient.get(API_ENDPOINTS.monthlyAnalytics);
    }

    static async getTypeAnalytics() {
        return ApiClient.get(API_ENDPOINTS.typeAnalytics);
    }
}

// Export for use in other scripts
window.AuthManager = AuthManager;
window.ApiClient = ApiClient;
window.AuthAPI = AuthAPI;
window.TasksAPI = TasksAPI; 