from dotenv import load_dotenv
import os
import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")


def start(update, context):
    user = update.effective_user
    welcome_text = (
        f"👋 Привет, {user.first_name}!\n\n"
        "🤖 Добро пожаловать в Assistant-for-Rent!\n\n"
        "🚀 Я ваш персональный помощник для управления задачами.\n\n"
        "📱 **Возможности:**\n"
        "• 📋 Посмотреть мои задачи\n"
        "• 📊 Статистика\n"
        "• 💰 Тарифы\n"
        "• ❓ Помощь\n\n"
        "💰 **Наши тарифы:**\n"
        "• Базовый: 15 000₽/мес (2 часа/день)\n"
        "• Стандарт: 30 000₽/мес (5 часов/день)\n"
        "• Премиум: 50 000₽/мес (8 часов/день)\n\n"
        "👇 Выберите действие:"
    )

    keyboard = [
        [
            telegram.InlineKeyboardButton("📋 Мои задачи", callback_data='my_tasks'),
            telegram.InlineKeyboardButton("📊 Статистика", callback_data='stats')
        ],
        [
            telegram.InlineKeyboardButton("💰 Тарифы", callback_data='pricing'),
            telegram.InlineKeyboardButton("❓ Помощь", callback_data='help')
        ],
        [
            telegram.InlineKeyboardButton("✍️ Создать задачу", callback_data='create_task'),
            telegram.InlineKeyboardButton("📞 Поддержка", callback_data='support')
        ]
    ]
    markup = telegram.InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(welcome_text, reply_markup=markup, parse_mode='Markdown')


def handle_callback(update, context):
    query = update.callback_query
    query.answer()
    user = update.effective_user

    if query.data == 'my_tasks':
        tasks_text = (
            f"📋 **Ваши задачи:**\n\n"
            f"📊 Всего: 5\n"
            f"✅ Выполнено: 3\n"
            f"⏳ В процессе: 2\n\n"
            f"**Последние задачи:**\n"
            f"✅ Расшифровка аудио\n"
            f"⏳ Поиск информации\n"
            f"⏳ Организация встречи\n\n"
            f"💡 Чтобы создать новую задачу, просто отправьте мне текст!"
        )
        
        keyboard = [
            [telegram.InlineKeyboardButton("✍️ Создать задачу", callback_data='create_task')],
            [telegram.InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
        ]
        markup = telegram.InlineKeyboardMarkup(keyboard)
        query.edit_message_text(tasks_text, reply_markup=markup, parse_mode='Markdown')

    elif query.data == 'stats':
        stats_text = (
            "📊 **Ваша статистика:**\n\n"
            "📈 За этот месяц:\n"
            "• Создано задач: 12\n"
            "• Выполнено: 8\n"
            "• Время сэкономлено: ~24 часа\n\n"
            "💰 Эффективность:\n"
            "• Средний рейтинг: 4.8/5\n"
            "• Скорость выполнения: 95%\n\n"
            "🚀 Откройте приложение для подробной аналитики!"
        )
        
        keyboard = [
            [telegram.InlineKeyboardButton("📋 Мои задачи", callback_data='my_tasks')],
            [telegram.InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
        ]
        markup = telegram.InlineKeyboardMarkup(keyboard)
        query.edit_message_text(stats_text, reply_markup=markup, parse_mode='Markdown')

    elif query.data == 'pricing':
        pricing_text = (
            "💰 **Тарифные планы:**\n\n"
            "🥉 **Базовый** - 15,000₽/мес\n"
            "• 2 часа работы в день\n"
            "• 1 задача в день\n"
            "• Базовая аналитика\n\n"
            "🥈 **Стандарт** - 30,000₽/мес\n"
            "• 5 часов работы в день\n"
            "• 3 задачи в день\n"
            "• Приоритетная поддержка\n\n"
            "🥇 **Премиум** - 50,000₽/мес\n"
            "• 8 часов работы в день\n"
            "• Неограниченно задач\n"
            "• VIP поддержка 24/7\n\n"
            "🚀 Выберите план в приложении!"
        )
        
        keyboard = [
            [telegram.InlineKeyboardButton("📞 Связаться с поддержкой", callback_data='support')],
            [telegram.InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
        ]
        markup = telegram.InlineKeyboardMarkup(keyboard)
        query.edit_message_text(pricing_text, reply_markup=markup, parse_mode='Markdown')

    elif query.data == 'create_task':
        create_text = (
            "✍️ **Создание задачи:**\n\n"
            "📝 Просто отправьте мне сообщение с описанием задачи!\n\n"
            "**Примеры:**\n"
            "• 'Найди информацию о компании XYZ'\n"
            "• 'Расшифруй аудиозапись' (+ прикрепи файл)\n"
            "• 'Организуй встречу с клиентом на завтра'\n"
            "• 'Переведи документ на английский'\n\n"
            "⚡ Укажите приоритет:\n"
            "• 'срочно' - выполним за 2-4 часа (+100%)\n"
            "• 'быстро' - выполним за 12 часов (+50%)\n"
            "• без пометки - выполним за 24 часа\n\n"
            "💬 Жду ваше сообщение!"
        )
        
        keyboard = [
            [telegram.InlineKeyboardButton("📋 Мои задачи", callback_data='my_tasks')],
            [telegram.InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
        ]
        markup = telegram.InlineKeyboardMarkup(keyboard)
        query.edit_message_text(create_text, reply_markup=markup, parse_mode='Markdown')

    elif query.data == 'help':
        help_text = (
            "❓ **Помощь и инструкции:**\n\n"
            "🚀 **Как начать:**\n"
            "1. Откройте приложение\n"
            "2. Зарегистрируйтесь или войдите\n"
            "3. Создайте первую задачу\n\n"
            "📋 **Типы задач:**\n"
            "• Исследовательские\n"
            "• Административные\n" 
            "• Творческие\n"
            "• Технические\n\n"
            "⚡ **Приоритеты:**\n"
            "• Обычная (24 часа)\n"
            "• Быстрая (12 часов) +50%\n"
            "• Срочная (2-4 часа) +100%\n\n"
            "💬 Есть вопросы? Обращайтесь в поддержку!"
        )
        
        keyboard = [
            [telegram.InlineKeyboardButton("✍️ Создать задачу", callback_data='create_task')],
            [telegram.InlineKeyboardButton("📞 Поддержка", callback_data='support')],
            [telegram.InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
        ]
        markup = telegram.InlineKeyboardMarkup(keyboard)
        query.edit_message_text(help_text, reply_markup=markup, parse_mode='Markdown')

    elif query.data == 'support':
        support_text = (
            "📞 **Служба поддержки:**\n\n"
            "🕐 **Время работы:**\n"
            "Пн-Пт: 9:00 - 21:00 MSK\n"
            "Сб-Вс: 10:00 - 18:00 MSK\n\n"
            "📧 **Контакты:**\n"
            "• Email: support@assistant-for-rent.com\n"
            "• Телефон: +7 (800) 555-35-35\n"
            "• Telegram: @assistant_support\n\n"
            "⚡ **Быстрая помощь:**\n"
            "Опишите вашу проблему, и мы ответим в течение 30 минут!"
        )
        
        keyboard = [
            [telegram.InlineKeyboardButton("💬 Написать в поддержку", url="https://t.me/assistant_support")],
            [telegram.InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
        ]
        markup = telegram.InlineKeyboardMarkup(keyboard)
        query.edit_message_text(support_text, reply_markup=markup, parse_mode='Markdown')

    elif query.data == 'back_to_main':
        # Возвращаемся к главному меню
        start_message = context.user_data.get('start_message', 'Добро пожаловать!')
        keyboard = [
            [
                telegram.InlineKeyboardButton("📋 Мои задачи", callback_data='my_tasks'),
                telegram.InlineKeyboardButton("📊 Статистика", callback_data='stats')
            ],
            [
                telegram.InlineKeyboardButton("💰 Тарифы", callback_data='pricing'),
                telegram.InlineKeyboardButton("❓ Помощь", callback_data='help')
            ],
            [
                telegram.InlineKeyboardButton("✍️ Создать задачу", callback_data='create_task'),
                telegram.InlineKeyboardButton("📞 Поддержка", callback_data='support')
            ]
        ]
        markup = telegram.InlineKeyboardMarkup(keyboard)
        
        welcome_text = (
            f"👋 Привет, {user.first_name}!\n\n"
            "🤖 Добро пожаловать в Assistant-for-Rent!\n\n"
            "👇 Выберите действие:"
        )
        query.edit_message_text(welcome_text, reply_markup=markup)


def handle_message(update, context):
    """Обработка текстовых сообщений - создание задач"""
    user_message = update.message.text
    user = update.effective_user
    
    # Определяем приоритет из текста
    priority = "обычная"
    priority_emoji = "📝"
    
    if "срочно" in user_message.lower() or "urgent" in user_message.lower():
        priority = "срочная (+100%)"
        priority_emoji = "🔥"
    elif "быстро" in user_message.lower() or "fast" in user_message.lower():
        priority = "быстрая (+50%)"
        priority_emoji = "⚡"
    
    # Создаем подтверждение задачи
    response_text = (
        f"✅ **Задача создана!**\n\n"
        f"👤 **Клиент:** {user.first_name}\n"
        f"{priority_emoji} **Приоритет:** {priority}\n"
        f"📝 **Описание:**\n_{user_message}_\n\n"
        f"🕐 **Статус:** Передана ассистенту\n"
        f"📱 **ID задачи:** #{hash(user_message) % 10000}\n\n"
        f"🚀 Ваша задача принята в работу!\n"
        f"Уведомим вас, когда будет готова."
    )
    
    keyboard = [
        [
            telegram.InlineKeyboardButton("📋 Мои задачи", callback_data='my_tasks'),
            telegram.InlineKeyboardButton("✍️ Ещё задачу", callback_data='create_task')
        ],
        [telegram.InlineKeyboardButton("📊 Статистика", callback_data='stats')]
    ]
    markup = telegram.InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(response_text, reply_markup=markup, parse_mode='Markdown')


def main():
    if TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Ошибка: Не установлен токен бота!")
        print("📝 Создайте файл .env с вашим токеном:")
        print("   BOT_TOKEN=ваш_токен_от_botfather")
        return
    
    print(f"🤖 Starting Assistant-for-Rent Bot...")
    print(f"🔑 Token: {TOKEN[:10]}...")
    
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Регистрация обработчиков
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_callback))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("🚀 Bot is running...")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
