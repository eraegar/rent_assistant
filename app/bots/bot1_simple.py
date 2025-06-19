from dotenv import load_dotenv
import os
import telegram
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Загружаем .env из папки bots и из корня проекта
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
load_dotenv()  # Загружаем также корневой .env как fallback

TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")


async def start(update, context):
    print(f"🔍 DEBUG: START command received from user {update.effective_user.first_name}")
    user = update.effective_user
    welcome_text = (
        f"👋 Привет, {user.first_name}!\n\n"
        "🤖 Добро пожаловать в Assistant-for-Rent!\n\n"
        "🚀 Я ваш персональный помощник для управления задачами.\n\n"
        "📱 Используйте приложение для полного функционала или выберите действие в меню:\n\n"
        "👇 Выберите действие:"
    )

    # Получаем WebApp URL из .env файла
    webapp_url = os.getenv("WEBAPP_URL", "https://4257-194-164-216-167.ngrok-free.app")
    
    keyboard = [
        [
            telegram.InlineKeyboardButton("🚀 Открыть приложение", url=webapp_url)
        ],
        [
            telegram.InlineKeyboardButton("💡 Примеры задач", callback_data='task_examples'),
            telegram.InlineKeyboardButton("💰 Тарифы", callback_data='pricing')
        ],
        [
            telegram.InlineKeyboardButton("📄 Документы", callback_data='documents'),
            telegram.InlineKeyboardButton("📞 Поддержка", callback_data='support')
        ]
    ]
    markup = telegram.InlineKeyboardMarkup(keyboard)
    
    print(f"🔍 DEBUG: Sending start message with {len(keyboard)} rows of buttons")
    await update.message.reply_text(welcome_text, reply_markup=markup)
    print(f"✅ DEBUG: Start message sent successfully")


async def handle_callback(update, context):
    print(f"🔍 DEBUG: ========== CALLBACK RECEIVED ==========")
    print(f"🔍 DEBUG: Update type: {type(update)}")
    print(f"🔍 DEBUG: Has callback_query: {hasattr(update, 'callback_query')}")
    
    if not update.callback_query:
        print("❌ DEBUG: No callback_query in update!")
        return
        
    try:
        query = update.callback_query
        print(f"🔍 DEBUG: Callback data: '{query.data}'")
        print(f"🔍 DEBUG: User: {query.from_user.first_name}")
        print(f"🔍 DEBUG: Message ID: {query.message.message_id}")
        
        # Обязательно отвечаем на callback
        await query.answer()
        print(f"✅ DEBUG: Callback answered")
        
        user = update.effective_user
        
        print(f"🔍 DEBUG: Processing callback: {query.data}")

        if query.data == 'pricing':
            print("DEBUG: Processing pricing callback")
            pricing_text = (
                "💰 Тарифные планы:\n\n"
                "⭐ Базовый - 15,000₽/мес\n"
                "• 2 часа работы в день\n"
                "• 1 задача в день\n"
                "• Персональный ассистент\n"
                "• Базовая аналитика\n\n"
                "🌟 Стандартный - 25,000₽/мес\n"
                "• 5 часов работы в день\n"
                "• До 4 задач в день\n"
                "• Персональный ассистент\n"
                "• Расширенная аналитика\n\n"
                "👑 Премиум - 35,000₽/мес\n"
                "• 8 часов работы в день\n"
                "• Неограниченные задачи\n"
                "• Персональный ассистент\n"
                "• Полная аналитика\n\n"
                "🚀 Выберите план в приложении!"
            )
            
            keyboard = [
                [telegram.InlineKeyboardButton("📞 Связаться с поддержкой", callback_data='support')],
                [telegram.InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
            ]
            markup = telegram.InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(pricing_text, reply_markup=markup)

        elif query.data == 'task_examples':
            print("DEBUG: Processing task_examples callback")
            examples_text = (
                "💡 Примеры задач для ассистента:\n\n"
                "🏠 Личные задачи:\n"
                "• Заказать пиццу другу, который болеет\n"
                "• Найти и забронировать семейный тур на выходные\n"
                "• Выбрать подарок маме на день рождения в бюджете 5000₽\n"
                "• Организовать сюрприз для жены - букет и доставку\n\n"
                "💼 Бизнес-задачи:\n"
                "• Расшифровать запись Zoom-встречи в текстовый формат\n"
                "• Найти контакты 10 потенциальных клиентов в сфере IT\n"
                "• Составить еженедельный отчет по продажам\n"
                "• Запланировать встречи с клиентами на следующую неделю"
            )
            
            webapp_url = os.getenv("WEBAPP_URL", "https://4257-194-164-216-167.ngrok-free.app")
            keyboard = [
                [telegram.InlineKeyboardButton("🚀 Создать задачу в приложении", url=webapp_url)],
                [telegram.InlineKeyboardButton("✍️ Написать задачу в чат", callback_data='create_task')],
                [telegram.InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
            ]
            markup = telegram.InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(examples_text, reply_markup=markup)

        elif query.data == 'documents':
            print("DEBUG: Processing documents callback")
            documents_text = (
                "📄 Соглашение об обработке персональных данных\n\n"
                "🔒 Политика конфиденциальности\n"
                "Мы обязуемся защищать ваши персональные данные в соответствии с российским законодательством.\n\n"
                "📋 Собираемые данные:\n"
                "• Имя и контактная информация\n"
                "• Текст заданий и сообщений\n"
                "• Данные об использовании сервиса\n"
                "• Техническая информация (IP, устройство)\n\n"
                "🛡️ Меры защиты:\n"
                "• SSL-шифрование при передаче\n"
                "• Ограниченный доступ к данным\n"
                "• Регулярная очистка устаревших данных\n"
                "• Соответствие требованиям ФЗ-152\n\n"
                "⚖️ Ваши права:\n"
                "• Доступ к своим данным\n"
                "• Исправление неточностей\n"
                "• Удаление данных по запросу\n"
                "• Отзыв согласия в любое время"
            )
            
            keyboard = [
                [telegram.InlineKeyboardButton("📄 Скачать полное соглашение", url="https://assistant-for-rent.com/docs/privacy.pdf")],
                [telegram.InlineKeyboardButton("📄 Пользовательское соглашение", url="https://assistant-for-rent.com/docs/terms.pdf")],
                [telegram.InlineKeyboardButton("📞 Связаться по вопросам данных", callback_data='support')],
                [telegram.InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
            ]
            markup = telegram.InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(documents_text, reply_markup=markup)

        elif query.data == 'support':
            print("DEBUG: Processing support callback")
            support_text = (
                "📞 Служба поддержки:\n\n"
                "🕐 Время работы:\n"
                "Пн-Пт: 9:00 - 21:00 MSK\n"
                "Сб-Вс: 10:00 - 18:00 MSK\n\n"
                "📧 Контакты:\n"
                "• Email: support@assistant-for-rent.com\n"
                "• Телефон: +7 (999) 999-99-99\n"
                "• Telegram: @assistant-for-rent-support\n\n"
                "⚡ Быстрая помощь:\n"
                "Опишите вашу проблему, и мы ответим в течение 30 минут!"
            )
            
            keyboard = [
                [telegram.InlineKeyboardButton("💬 Написать в поддержку", url="https://t.me/assistant-for-rent-support")],
                [telegram.InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
            ]
            markup = telegram.InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(support_text, reply_markup=markup)

        elif query.data == 'create_task':
            print("DEBUG: Processing create_task callback")
            create_text = (
                "✍️ Создание задачи:\n\n"
                "📝 Просто отправьте мне сообщение с описанием задачи!\n\n"
                "Примеры:\n"
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
            
            webapp_url = os.getenv("WEBAPP_URL", "https://4257-194-164-216-167.ngrok-free.app")
            keyboard = [
                [telegram.InlineKeyboardButton("🚀 Открыть приложение", url=webapp_url)],
                [telegram.InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
            ]
            markup = telegram.InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(create_text, reply_markup=markup)

        elif query.data == 'back_to_main':
            print("DEBUG: Processing back_to_main callback")
            # Возвращаемся к главному меню
            webapp_url = os.getenv("WEBAPP_URL", "https://4257-194-164-216-167.ngrok-free.app")
            keyboard = [
                [
                    telegram.InlineKeyboardButton("🚀 Открыть приложение", url=webapp_url)
                ],
                [
                    telegram.InlineKeyboardButton("💡 Примеры задач", callback_data='task_examples'),
                    telegram.InlineKeyboardButton("💰 Тарифы", callback_data='pricing')
                ],
                [
                    telegram.InlineKeyboardButton("📄 Документы", callback_data='documents'),
                    telegram.InlineKeyboardButton("📞 Поддержка", callback_data='support')
                ]
            ]
            markup = telegram.InlineKeyboardMarkup(keyboard)
            
            welcome_text = (
                f"👋 Привет, {user.first_name}!\n\n"
                "🤖 Добро пожаловать в Assistant-for-Rent!\n\n"
                "👇 Выберите действие:"
            )
            await query.edit_message_text(welcome_text, reply_markup=markup)
        else:
            print(f"DEBUG: Unknown callback data: {query.data}")
            
    except Exception as e:
        print(f"ERROR in handle_callback: {e}")
        import traceback
        traceback.print_exc()
        
        # Попытаемся ответить пользователю об ошибке
        try:
            await query.edit_message_text("❌ Произошла ошибка. Попробуйте еще раз или обратитесь в поддержку.")
        except:
            pass


async def handle_message(update, context):
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
            telegram.InlineKeyboardButton("💡 Примеры задач", callback_data='task_examples'),
            telegram.InlineKeyboardButton("✍️ Ещё задачу", callback_data='create_task')
        ],
        [telegram.InlineKeyboardButton("💰 Тарифы", callback_data='pricing')]
    ]
    markup = telegram.InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(response_text, reply_markup=markup)


def main():
    print(f"🔍 DEBUG: Checking TOKEN...")
    print(f"🔍 DEBUG: BOT_TOKEN env var: {os.getenv('BOT_TOKEN', 'NOT_SET')[:10]}...")
    
    if TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Ошибка: Не установлен токен бота!")
        print("📝 Создайте файл .env с вашим токеном:")
        print("   BOT_TOKEN=ваш_токен_от_botfather")
        return
    
    print(f"🤖 Starting Assistant-for-Rent Bot...")
    print(f"🔑 Token: {TOKEN[:10]}...")
    
    try:
        application = Application.builder().token(TOKEN).build()
        print(f"✅ DEBUG: Application created successfully")

        # Регистрация обработчиков
        start_handler = CommandHandler("start", start)
        callback_handler = CallbackQueryHandler(handle_callback)
        message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
        
        application.add_handler(start_handler)
        print(f"✅ DEBUG: Start handler registered")
        
        application.add_handler(callback_handler)
        print(f"✅ DEBUG: Callback handler registered")
        
        application.add_handler(message_handler)
        print(f"✅ DEBUG: Message handler registered")

        print("🚀 Bot is running...")
        print("✅ All handlers registered successfully")
        print("🔍 DEBUG: Starting polling...")
        application.run_polling()
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 