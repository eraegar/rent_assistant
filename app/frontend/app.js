// Application State
let currentUser = null;
let tasks = [];
let currentTaskId = null;

console.log('App.js loaded');
console.log('AuthAPI available:', typeof AuthAPI !== 'undefined');
console.log('TasksAPI available:', typeof TasksAPI !== 'undefined');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing app...');
    initializeApp();
});

async function initializeApp() {
    setupEventListeners();
    updateAuthUI();
    
    // Check if user is already logged in
    if (AuthManager.isAuthenticated()) {
        try {
            currentUser = await AuthAPI.getCurrentUser();
            showDashboard();
            await loadUserData();
        } catch (error) {
            console.error('Failed to load user data:', error);
            AuthManager.removeToken();
            updateAuthUI();
            showWelcome();
        }
    } else {
        showWelcome();
    }
}

function setupEventListeners() {
    console.log('Setting up event listeners...');
    
    // Auth modal listeners
    const authBtn = document.getElementById('authBtn');
    console.log('authBtn found:', !!authBtn);
    
    authBtn?.addEventListener('click', () => {
        console.log('Auth button clicked!');
        document.getElementById('authModal').classList.remove('hidden');
    });
    document.getElementById('closeAuthModalBtn')?.addEventListener('click', () => {
        document.getElementById('authModal').classList.add('hidden');
    });
    
    // Profile modal listeners
    document.getElementById('profileBtn')?.addEventListener('click', showProfileModal);
    document.getElementById('closeProfileModalBtn')?.addEventListener('click', hideProfileModal);
    document.getElementById('logoutBtn')?.addEventListener('click', handleLogout);
    document.getElementById('editProfileBtn')?.addEventListener('click', () => {
        alert('Редактирование профиля будет добавлено в следующей версии');
    });
    document.getElementById('settingsBtn')?.addEventListener('click', () => {
        alert('Настройки будут добавлены в следующей версии');
    });
    
    // Auth tab listeners
    document.getElementById('loginTab')?.addEventListener('click', showLoginForm);
    document.getElementById('registerTab')?.addEventListener('click', showRegisterForm);
    
    // Auth form listeners
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    document.getElementById('registerForm').addEventListener('submit', handleRegister);
    
    // Task form listeners
    document.getElementById('taskForm')?.addEventListener('submit', handleTaskSubmit);
    
    // Navigation listeners
    document.getElementById('dashboardBtn')?.addEventListener('click', () => showSection('dashboard'));
    document.getElementById('analyticsBtn')?.addEventListener('click', () => showSection('analytics'));
    
    // Modal listeners
    document.getElementById('newTaskBtn')?.addEventListener('click', showNewTaskModal);
    document.getElementById('closeModal')?.addEventListener('click', hideNewTaskModal);
    document.getElementById('closeTaskDetail')?.addEventListener('click', hideTaskDetailModal);
    
    // Task action listeners
    document.getElementById('acceptTaskBtn')?.addEventListener('click', () => {
        if (currentTaskId) updateTaskStatus(currentTaskId, 'completed');
    });
    document.getElementById('revisionTaskBtn')?.addEventListener('click', () => {
        if (currentTaskId) updateTaskStatus(currentTaskId, 'revision');
    });
    
    // Example task listeners
    document.querySelectorAll('.example-task').forEach(task => {
        task.addEventListener('click', function() {
            const taskText = this.getAttribute('data-task');
            document.getElementById('taskTitle').value = taskText;
            showNewTaskModal();
        });
    });
    
    // Setup phone number formatting
    setupPhoneFormatting();
}

// UI helper functions
function showLoginForm() {
    document.getElementById('loginTab').classList.add('border-b-2', 'border-blue-500', 'text-blue-500', 'font-medium');
    document.getElementById('loginTab').classList.remove('text-gray-500', 'hover:text-gray-700');
    document.getElementById('registerTab').classList.remove('border-b-2', 'border-blue-500', 'text-blue-500', 'font-medium');
    document.getElementById('registerTab').classList.add('text-gray-500', 'hover:text-gray-700');
    document.getElementById('loginForm').classList.remove('hidden');
    document.getElementById('registerForm').classList.add('hidden');
}

function showRegisterForm() {
    document.getElementById('registerTab').classList.add('border-b-2', 'border-blue-500', 'text-blue-500', 'font-medium');
    document.getElementById('registerTab').classList.remove('text-gray-500', 'hover:text-gray-700');
    document.getElementById('loginTab').classList.remove('border-b-2', 'border-blue-500', 'text-blue-500', 'font-medium');
    document.getElementById('loginTab').classList.add('text-gray-500', 'hover:text-gray-700');
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('registerForm').classList.remove('hidden');
}

// Authentication handlers
async function handleLogin(e) {
    e.preventDefault();
    
    const phone = document.getElementById('phoneLoginInput').value.replace(/\D/g, ''); // Только цифры
    const formattedPhone = '+' + phone; // Добавляем + для отправки на сервер
    const password = document.getElementById('passwordInput').value;
    
    try {
        await AuthAPI.login(formattedPhone, password);
        currentUser = await AuthAPI.getCurrentUser();
        document.getElementById('authModal').classList.add('hidden');
        updateAuthUI();
        showDashboard();
        await loadUserData();
        alert('Добро пожаловать!');
    } catch (error) {
        alert(error.message);
    }
}

async function handleRegister(e) {
    e.preventDefault();
    
    const name = document.getElementById('nameInput').value;
    const phone = document.getElementById('regPhoneInput').value.replace(/\D/g, ''); // Только цифры
    const formattedPhone = '+' + phone; // Добавляем + для отправки на сервер
    const password = document.getElementById('regPasswordInput').value;
    const confirmPassword = document.getElementById('confirmPasswordInput').value;
    
    if (password !== confirmPassword) {
        alert('Пароли не совпадают');
        return;
    }
    
    try {
        await AuthAPI.register(name, formattedPhone, password);
        alert('Регистрация успешна! Теперь войдите в систему.');
        
        // Switch to login tab
        showLoginForm();
        
        // Fill login form with formatted phone
        document.getElementById('phoneLoginInput').value = formatPhoneNumber(phone);
        document.getElementById('passwordInput').value = password;
        
    } catch (error) {
        alert(error.message);
    }
}

// Task handlers
async function handleTaskSubmit(e) {
    e.preventDefault();
    
    const title = document.getElementById('taskTitle').value;
    const description = document.getElementById('taskDescription').value;
    const type = document.getElementById('taskType').value;
    const priority = document.getElementById('taskPriority').value;
    const speed = document.getElementById('taskSpeed').value;
    
    try {
        const newTask = await TasksAPI.createTask({
            title,
            description,
            type,
            priority,
            speed
        });
        
        tasks.unshift(newTask);
        await updateTaskStats();
        renderTaskList();
        hideNewTaskModal();
        
        // Clear form
        document.getElementById('taskForm').reset();
        
        alert('Задача успешно создана!');
    } catch (error) {
        alert('Ошибка при создании задачи: ' + error.message);
    }
}

async function updateTaskStatus(taskId, newStatus) {
    try {
        const updatedTask = await TasksAPI.updateTask(taskId, { status: newStatus });
        
        // Update task in local array
        const taskIndex = tasks.findIndex(t => t.id === taskId);
        if (taskIndex !== -1) {
            tasks[taskIndex] = updatedTask;
        }
        
        await updateTaskStats();
        renderTaskList();
        hideTaskDetailModal();
        
        const message = newStatus === 'completed' ? 'Задача принята!' : 'Задача отправлена на доработку.';
        alert(message);
    } catch (error) {
        alert('Ошибка при обновлении задачи: ' + error.message);
    }
}

// Data loading functions
async function loadUserData() {
    try {
        // Load tasks
        tasks = await TasksAPI.getTasks();
        
        // Update UI
        await updateTaskStats();
        renderTaskList();
        
        // Load analytics if on analytics page
        if (!document.getElementById('analyticsSection').classList.contains('hidden')) {
            await loadAnalytics();
        }
    } catch (error) {
        console.error('Failed to load user data:', error);
        alert('Ошибка при загрузке данных');
    }
}

async function updateTaskStats() {
    try {
        const stats = await TasksAPI.getTaskStats();
        
        document.getElementById('totalTasks').textContent = stats.total_tasks;
        document.getElementById('completedTasks').textContent = stats.completed_tasks;
        document.getElementById('pendingTasks').textContent = stats.pending_tasks;
        document.getElementById('revisionTasks').textContent = stats.revision_tasks;
        
        // Mock earned amount for now
        document.getElementById('earnedAmount').textContent = stats.completed_tasks * 500 + ' ₽';
    } catch (error) {
        console.error('Failed to update stats:', error);
    }
}

async function loadAnalytics() {
    try {
        const [monthlyData, typeData] = await Promise.all([
            TasksAPI.getMonthlyAnalytics(),
            TasksAPI.getTypeAnalytics()
        ]);
        
        renderCharts(monthlyData, typeData);
    } catch (error) {
        console.error('Failed to load analytics:', error);
    }
}

// UI Functions
function showWelcome() {
    document.getElementById('welcomeSection').classList.remove('hidden');
    document.getElementById('dashboardSection').classList.add('hidden');
    document.getElementById('analyticsSection').classList.add('hidden');
}

function showDashboard() {
    document.getElementById('welcomeSection').classList.add('hidden');
    document.getElementById('dashboardSection').classList.remove('hidden');
    document.getElementById('analyticsSection').classList.add('hidden');
}

function showSection(section) {
    if (section === 'analytics') {
        document.getElementById('welcomeSection').classList.add('hidden');
        document.getElementById('dashboardSection').classList.add('hidden');
        document.getElementById('analyticsSection').classList.remove('hidden');
        loadAnalytics();
    } else {
        showDashboard();
    }
}

function showNewTaskModal() {
    document.getElementById('newTaskModal').classList.remove('hidden');
}

function hideNewTaskModal() {
    document.getElementById('newTaskModal').classList.add('hidden');
}

function showTaskDetailModal(taskId) {
    currentTaskId = taskId;
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;
    
    // Populate modal with task details
    document.getElementById('taskDetailModal').classList.remove('hidden');
    // You'll need to implement the task detail modal content
}

function hideTaskDetailModal() {
    document.getElementById('taskDetailModal').classList.add('hidden');
    currentTaskId = null;
}

function renderTaskList() {
    const container = document.getElementById('taskList');
    
    if (tasks.length === 0) {
        container.innerHTML = `
            <div class="text-center py-8">
                <i class="fas fa-tasks text-4xl text-gray-300 mb-4"></i>
                <p class="text-gray-500">У вас пока нет задач</p>
                <button class="mt-4 bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600" onclick="showNewTaskModal()">
                    Создать первую задачу
                </button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = tasks.map(task => `
        <div class="task-card ${getTaskCardClass(task.status)} bg-white rounded-lg shadow-md p-4 cursor-pointer hover:shadow-lg transition-shadow" onclick="showTaskDetailModal(${task.id})">
            <div class="flex justify-between items-start mb-2">
                <h3 class="font-semibold text-gray-800">${task.title}</h3>
                <span class="px-2 py-1 text-xs rounded ${getStatusClass(task.status)}">
                    ${getStatusText(task.status)}
                </span>
            </div>
            <p class="text-gray-600 text-sm mb-3">${(task.description || '').substring(0, 100)}${task.description && task.description.length > 100 ? '...' : ''}</p>
            <div class="flex justify-between items-center text-sm text-gray-500">
                <div class="flex items-center space-x-4">
                    <span class="px-2 py-1 rounded ${task.type === 'business' ? 'bg-blue-100 text-blue-800' : 'bg-purple-100 text-purple-800'}">
                        ${task.type === 'business' ? 'Бизнес' : 'Личная'}
                    </span>
                    <span class="px-2 py-1 rounded ${getPriorityClass(task.priority)}">
                        ${getPriorityText(task.priority)}
                    </span>
                </div>
                <div class="flex items-center">
                    <i class="fas fa-user-circle mr-1"></i>
                    ${task.assistant || 'Не назначен'}
                </div>
            </div>
        </div>
    `).join('');
}

function renderCharts(monthlyData, typeData) {
    // Monthly chart
    const monthlyCtx = document.getElementById('monthlyChart').getContext('2d');
    new Chart(monthlyCtx, {
        type: 'line',
        data: {
            labels: monthlyData.labels,
            datasets: [{
                label: 'Выполненные задачи',
                data: monthlyData.data,
                borderColor: '#3B82F6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    
    // Task type chart
    const taskTypeCtx = document.getElementById('taskTypeChart').getContext('2d');
    new Chart(taskTypeCtx, {
        type: 'doughnut',
        data: {
            labels: typeData.labels,
            datasets: [{
                data: typeData.data,
                backgroundColor: ['#3B82F6', '#8B5CF6']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

// Helper functions
function getTaskCardClass(status) {
    switch(status) {
        case 'completed': return 'completed-task';
        case 'pending': return 'pending-task';
        case 'revision': return 'revision-task';
        default: return '';
    }
}

function getStatusClass(status) {
    switch(status) {
        case 'completed': return 'bg-green-100 text-green-800';
        case 'pending': return 'bg-yellow-100 text-yellow-800';
        case 'revision': return 'bg-red-100 text-red-800';
        default: return 'bg-gray-100 text-gray-800';
    }
}

function getStatusText(status) {
    switch(status) {
        case 'completed': return 'Выполнено';
        case 'pending': return 'В работе';
        case 'revision': return 'На доработке';
        default: return 'Неизвестно';
    }
}

function getPriorityClass(priority) {
    switch(priority) {
        case 'high': return 'bg-red-100 text-red-800';
        case 'medium': return 'bg-yellow-100 text-yellow-800';
        case 'low': return 'bg-green-100 text-green-800';
        default: return 'bg-gray-100 text-gray-800';
    }
}

function getPriorityText(priority) {
    switch(priority) {
        case 'high': return 'Высокая';
        case 'medium': return 'Средняя';
        case 'low': return 'Обычная';
        default: return 'Неизвестно';
    }
}

// Phone formatting functions
function formatPhoneNumber(value) {
    // Удаляем все символы кроме цифр
    const cleaned = value.replace(/\D/g, '');
    
    // Начинаем с +7
    if (cleaned.length === 0) return '';
    
    let formatted = '+7';
    
    if (cleaned.length > 1) {
        // Добавляем код города в скобках
        const areaCode = cleaned.slice(1, 4);
        if (areaCode.length > 0) {
            formatted += ` (${areaCode}`;
            if (areaCode.length === 3) {
                formatted += ')';
            }
        }
    }
    
    if (cleaned.length > 4) {
        // Добавляем первую часть номера
        const firstPart = cleaned.slice(4, 7);
        formatted += ` ${firstPart}`;
    }
    
    if (cleaned.length > 7) {
        // Добавляем вторую часть номера
        const secondPart = cleaned.slice(7, 9);
        formatted += `-${secondPart}`;
    }
    
    if (cleaned.length > 9) {
        // Добавляем третью часть номера
        const thirdPart = cleaned.slice(9, 11);
        formatted += `-${thirdPart}`;
    }
    
    return formatted;
}

function handlePhoneInput(event) {
    const input = event.target;
    const cursorPosition = input.selectionStart;
    const oldValue = input.value;
    const oldLength = oldValue.length;
    
    // Форматируем значение
    const newValue = formatPhoneNumber(input.value);
    input.value = newValue;
    
    // Восстанавливаем позицию курсора
    const newLength = newValue.length;
    const lengthDiff = newLength - oldLength;
    const newCursorPosition = cursorPosition + lengthDiff;
    
    // Устанавливаем курсор в правильную позицию
    setTimeout(() => {
        input.setSelectionRange(newCursorPosition, newCursorPosition);
    }, 0);
}

function setupPhoneFormatting() {
    // Находим все поля телефона и добавляем форматирование
    const phoneInputs = [
        document.getElementById('phoneLoginInput'),
        document.getElementById('regPhoneInput')
    ];
    
    phoneInputs.forEach(input => {
        if (input) {
            // Добавляем обработчики событий
            input.addEventListener('input', handlePhoneInput);
            input.addEventListener('keydown', (e) => {
                // Разрешаем стандартные клавиши навигации
                const allowedKeys = [
                    'Backspace', 'Delete', 'Tab', 'Escape', 'Enter',
                    'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown',
                    'Home', 'End'
                ];
                
                if (allowedKeys.includes(e.key) || 
                    (e.key >= '0' && e.key <= '9') ||
                    e.ctrlKey || e.metaKey) {
                    return; // Разрешаем ввод
                }
                
                e.preventDefault(); // Блокируем остальные символы
            });
            
            // Устанавливаем начальное значение
            if (!input.value) {
                input.value = '+7 (';
            }
            
            // Предотвращаем удаление +7 (
            input.addEventListener('keydown', (e) => {
                if ((e.key === 'Backspace' || e.key === 'Delete') && 
                    input.selectionStart <= 4) {
                    e.preventDefault();
                }
            });
        }
    });
}

// Profile management functions
function updateAuthUI() {
    const authBtn = document.getElementById('authBtn');
    const profileBtn = document.getElementById('profileBtn');
    
    if (AuthManager.isAuthenticated()) {
        // User is logged in - show profile button, hide auth button
        authBtn.classList.add('hidden');
        profileBtn.classList.remove('hidden');
    } else {
        // User is not logged in - show auth button, hide profile button  
        authBtn.classList.remove('hidden');
        profileBtn.classList.add('hidden');
    }
}

async function showProfileModal() {
    try {
        // Load current user data
        const user = await AuthAPI.getCurrentUser();
        const stats = await TasksAPI.getTaskStats();
        
        // Update profile modal content
        document.getElementById('profileName').textContent = user.name;
        document.getElementById('profilePhone').textContent = user.phone;
        document.getElementById('profileTotalTasks').textContent = stats.total_tasks;
        document.getElementById('profileCompletedTasks').textContent = stats.completed_tasks;
        
        // Show modal
        document.getElementById('profileModal').classList.remove('hidden');
    } catch (error) {
        console.error('Failed to load profile data:', error);
        alert('Ошибка при загрузке профиля');
    }
}

function hideProfileModal() {
    document.getElementById('profileModal').classList.add('hidden');
}

function handleLogout() {
    if (confirm('Вы уверены, что хотите выйти из аккаунта?')) {
        AuthAPI.logout();
        hideProfileModal();
        updateAuthUI();
        showWelcome();
        currentUser = null;
        tasks = [];
        alert('Вы успешно вышли из аккаунта');
    }
} 