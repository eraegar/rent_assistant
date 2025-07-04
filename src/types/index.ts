export interface User {
  id: string;
  name: string;
  email: string;
  phone: string;
  telegram_username?: string;
  subscription?: Subscription;
  created_at: string;
}

export interface Subscription {
  id: string;
  client_id: string;
  plan: SubscriptionPlan;
  status: SubscriptionStatus;
  started_at: string;
  expires_at: string;
  auto_renew: boolean;
}

export enum SubscriptionPlan {
  PERSONAL_2H = 'personal_2h',
  PERSONAL_5H = 'personal_5h', 
  PERSONAL_8H = 'personal_8h',
  BUSINESS_2H = 'business_2h',
  BUSINESS_5H = 'business_5h',
  BUSINESS_8H = 'business_8h',
  COMBO_2H = 'combo_2h',
  COMBO_5H = 'combo_5h',
  COMBO_8H = 'combo_8h',
  NONE = 'none',
  PERSONAL_ONLY = 'personal_only',
  BUSINESS = 'business',
  FULL = 'full'
}

export enum SubscriptionStatus {
  ACTIVE = 'active',
  CANCELLED = 'cancelled', 
  EXPIRED = 'expired',
  PENDING_PAYMENT = 'pending_payment'
}

export interface Task {
  id: string;
  title: string;
  description: string;
  type: TaskType;
  task_type: string;
  status: TaskStatus;
  created_at: string;
  updated_at?: string;
  deadline?: string;
  result?: string;
  assigned_assistant?: string;
  assistant_notes?: string;
  ai_suggestion?: string;
  attachments: string[];
}

export enum TaskType {
  PERSONAL = 'personal',
  BUSINESS = 'business',
  URGENT = 'urgent',
  RESEARCH = 'research',
  CREATIVE = 'creative'
}

export enum TaskStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  WAITING_CLIENT = 'waiting_client',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled'
}

export enum UserStatus {
  UNAUTHENTICATED = 'unauthenticated',
  AUTHENTICATED = 'authenticated',
  NEEDS_SUBSCRIPTION = 'needsSubscription',
  HAS_ACTIVE_SUBSCRIPTION = 'hasActiveSubscription'
}

export interface AuthState {
  user: User | null;
  userStatus: UserStatus;
  isLoading: boolean;
  token: string | null;
}

export interface TaskState {
  tasks: Task[];
  isLoading: boolean;
}

export interface PlanDetails {
  name: string;
  price: string;
  description: string;
  features: string[];
  isPopular: boolean;
  assistantType: AssistantType;
  hoursPerDay: number;
}

export enum AssistantType {
  PERSONAL = 'personal',
  BUSINESS = 'business',
  COMBO = 'combo'
}

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
} 