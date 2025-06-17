// Telegram WebApp Integration
class TelegramWebApp {
    constructor() {
        this.tg = window.Telegram?.WebApp;
        this.isInTelegram = !!this.tg;
        this.init();
    }

    init() {
        if (!this.isInTelegram) {
            console.log('Not running in Telegram WebApp');
            return;
        }

        console.log('🚀 Telegram WebApp initialized');
        
        // Настройка WebApp
        this.tg.ready();
        this.tg.expand();
        
        // Настройка темы
        this.setupTheme();
        
        // Настройка кнопок
        this.setupButtons();
        
        // Обработка событий
        this.setupEventHandlers();
        
        // Получение данных пользователя
        this.handleUserData();
        
        // Обработка параметров запуска
        this.handleStartParams();
    }

    setupTheme() {
        if (!this.tg) return;
        
        // Применяем тему Telegram
        const themeParams = this.tg.themeParams;
        
        document.documentElement.style.setProperty('--tg-theme-bg-color', themeParams.bg_color || '#ffffff');
        document.documentElement.style.setProperty('--tg-theme-text-color', themeParams.text_color || '#000000');
        document.documentElement.style.setProperty('--tg-theme-hint-color', themeParams.hint_color || '#999999');
        document.documentElement.style.setProperty('--tg-theme-link-color', themeParams.link_color || '#0088cc');
        document.documentElement.style.setProperty('--tg-theme-button-color', themeParams.button_color || '#0088cc');
        document.documentElement.style.setProperty('--tg-theme-button-text-color', themeParams.button_text_color || '#ffffff');
        
        // Обновляем цвет header bar
        this.tg.setHeaderColor(themeParams.bg_color || '#667eea');
    }

    setupButtons() {
        if (!this.tg) return;
        
        // Главная кнопка
        this.tg.MainButton.text = "Создать задачу";
        this.tg.MainButton.color = "#0088cc";
        this.tg.MainButton.textColor = "#ffffff";
        
        // Кнопка назад
        this.tg.BackButton.onClick(() => {
            this.handleBackButton();
        });
    }

    setupEventHandlers() {
        if (!this.tg) return;
        
        // Главная кнопка
        this.tg.MainButton.onClick(() => {
            this.handleMainButton();
        });
        
        // Закрытие приложения
        this.tg.onEvent('viewportChanged', () => {
            console.log('Viewport changed:', this.tg.viewportHeight);
        });
        
        // Обработка haptic feedback
        this.setupHapticFeedback();
    }

    setupHapticFeedback() {
        if (!this.tg?.HapticFeedback) return;
        
        // Добавляем haptic feedback к кнопкам
        document.addEventListener('click', (e) => {
            if (e.target.matches('button, .btn, [role="button"]')) {
                this.tg.HapticFeedback.impactOccurred('medium');
            }
        });
    }

    handleUserData() {
        if (!this.tg?.initDataUnsafe?.user) return;
        
        const user = this.tg.initDataUnsafe.user;
        console.log('Telegram User:', user);
        
        // Сохраняем данные пользователя
        this.telegramUser = {
            id: user.id,
            first_name: user.first_name,
            last_name: user.last_name,
            username: user.username,
            language_code: user.language_code,
            is_premium: user.is_premium
        };
        
        // Автоматическая авторизация через Telegram
        this.autoAuthWithTelegram();
    }

    async autoAuthWithTelegram() {
        if (!this.telegramUser) return;
        
        try {
            // Проверяем, есть ли уже токен
            if (AuthManager.isAuthenticated()) {
                console.log('User already authenticated');
                return;
            }
            
            // Попытка авторизации через Telegram ID
            const response = await fetch('/auth/telegram-login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    telegram_id: this.telegramUser.id,
                    first_name: this.telegramUser.first_name,
                    last_name: this.telegramUser.last_name,
                    username: this.telegramUser.username
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                AuthManager.setToken(data.access_token);
                console.log('✅ Auto-authenticated via Telegram');
                
                // Обновляем UI
                if (window.updateAuthUI) {
                    window.updateAuthUI();
                }
                
                // Показываем уведомление
                this.showNotification(`Добро пожаловать, ${this.telegramUser.first_name}!`);
            }
        } catch (error) {
            console.error('Telegram auth failed:', error);
        }
    }

    handleStartParams() {
        if (!this.tg?.initDataUnsafe?.start_param) return;
        
        const startParam = this.tg.initDataUnsafe.start_param;
        console.log('Start param:', startParam);
        
        // Обрабатываем различные параметры запуска
        if (startParam.startsWith('task_')) {
            const taskText = decodeURIComponent(startParam.replace('task_', ''));
            this.prefillTaskForm(taskText);
        }
    }

    handleMainButton() {
        console.log('Main button clicked');
        
        // Определяем текущую страницу и действие
        const currentSection = this.getCurrentSection();
        
        switch (currentSection) {
            case 'welcome':
                this.showNewTaskModal();
                break;
            case 'dashboard':
                this.showNewTaskModal();
                break;
            case 'analytics':
                this.exportAnalytics();
                break;
            default:
                this.showNewTaskModal();
        }
    }

    handleBackButton() {
        console.log('Back button clicked');
        
        // Проверяем, какие модальные окна открыты
        const modals = ['authModal', 'profileModal', 'newTaskModal'];
        
        for (const modalId of modals) {
            const modal = document.getElementById(modalId);
            if (modal && !modal.classList.contains('hidden')) {
                modal.classList.add('hidden');
                this.tg.BackButton.hide();
                return;
            }
        }
        
        // Если модалов нет, возвращаемся к главной странице
        if (window.showWelcome) {
            window.showWelcome();
        }
    }

    getCurrentSection() {
        if (!document.getElementById('welcomeSection').classList.contains('hidden')) {
            return 'welcome';
        }
        if (!document.getElementById('dashboardSection').classList.contains('hidden')) {
            return 'dashboard';
        }
        if (!document.getElementById('analyticsSection').classList.contains('hidden')) {
            return 'analytics';
        }
        return 'unknown';
    }

    showNewTaskModal() {
        if (window.showNewTaskModal) {
            window.showNewTaskModal();
            this.tg.MainButton.hide();
            this.tg.BackButton.show();
        }
    }

    prefillTaskForm(taskText) {
        const taskTitleInput = document.getElementById('taskTitle');
        if (taskTitleInput) {
            taskTitleInput.value = taskText;
            this.showNewTaskModal();
        }
    }

    showNotification(message) {
        if (this.tg?.showAlert) {
            this.tg.showAlert(message);
        } else {
            alert(message);
        }
    }

    showConfirm(message, callback) {
        if (this.tg?.showConfirm) {
            this.tg.showConfirm(message, callback);
        } else {
            const result = confirm(message);
            callback(result);
        }
    }

    // Обновление состояния кнопок в зависимости от контекста
    updateButtons(context) {
        if (!this.tg) return;
        
        switch (context) {
            case 'welcome':
                this.tg.MainButton.text = "Создать задачу";
                this.tg.MainButton.show();
                this.tg.BackButton.hide();
                break;
                
            case 'dashboard':
                this.tg.MainButton.text = "Новая задача";
                this.tg.MainButton.show();
                this.tg.BackButton.hide();
                break;
                
            case 'analytics':
                this.tg.MainButton.text = "Экспорт данных";
                this.tg.MainButton.show();
                this.tg.BackButton.hide();
                break;
                
            case 'modal':
                this.tg.MainButton.hide();
                this.tg.BackButton.show();
                break;
                
            default:
                this.tg.MainButton.hide();
                this.tg.BackButton.hide();
        }
    }

    // Отправка данных обратно в Telegram бот
    sendDataToBot(data) {
        if (this.tg?.sendData) {
            this.tg.sendData(JSON.stringify(data));
        }
    }

    // Закрытие WebApp
    close() {
        if (this.tg?.close) {
            this.tg.close();
        }
    }
}

// Инициализация при загрузке страницы
window.telegramWebApp = new TelegramWebApp();

// Экспорт для использования в других скриптах
window.TelegramWebApp = TelegramWebApp; 