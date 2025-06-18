from dotenv import load_dotenv
import os
import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://7963-194-164-216-167.ngrok-free.app")


def start(update, context):
    welcome_text = (
        "👋 Добро пожаловать в Assistant-for-Rent!\n\n"
        "🤖 Я ваш персональный помощник, который поможет организовать работу с личным или бизнес-ассистентом.\n\n"
        "📱 Наше мобильное приложение позволяет:\n"
        "• Размещать задачи\n"
        "• Общаться с ассистентом\n"
        "• Получать ежемесячные отчеты\n"
        "• Управлять тарифами\n\n"
        "💼 Наши тарифы:\n"
        "• Личный ассистент: от 15 000₽/мес\n"
        "• Бизнес ассистент: от 30 000₽/мес\n"
        "• Комбинированный: от 40 000₽/мес\n\n"
        "Выберите действие в меню ниже 👇"
    )

    keyboard = [
        [telegram.InlineKeyboardButton("📱 Открыть приложение", web_app=telegram.WebAppInfo(WEBAPP_URL))],
        [telegram.InlineKeyboardButton("📋 Примеры задач", callback_data='examples')],
        [telegram.InlineKeyboardButton("💰 Тарифы", callback_data='pricing')],
        [telegram.InlineKeyboardButton("📄 Документы", callback_data='documents')],
        [telegram.InlineKeyboardButton("📞 Связаться с нами", callback_data='contact')]
    ]
    markup = telegram.InlineKeyboardMarkup(keyboard)
    update.message.reply_text(welcome_text, reply_markup=markup)


def handle_callback(update, context):
    query = update.callback_query
    query.answer()

    if query.data == 'examples':
        examples_text = (
            "📋 Примеры задач, которые может выполнить ваш ассистент:\n\n"
            "• Расшифровка аудио/видео записей\n"
            "• Поиск и анализ информации\n"
            "• Организация встреч и звонков\n"
            "• Работа с документами\n"
            "• Заказ товаров и услуг\n"
            "• И многое другое!\n\n"
            "Задайте любую задачу, и мы поможем её решить!"
        )
        query.edit_message_text(examples_text)

    elif query.data == 'pricing':
        pricing_text = (
            "💰 Наши тарифы:\n\n"
            "👤 Личный ассистент:\n"
            "• 15 000₽/мес - 2 часа в день\n"
            "• 30 000₽/мес - 5 часов в день\n"
            "• 50 000₽/мес - 8 часов в день\n\n"
            "💼 Бизнес ассистент:\n"
            "• 30 000₽/мес - 2 часа в день\n"
            "• 60 000₽/мес - 5 часов в день\n"
            "• 80 000₽/мес - 8 часов в день\n\n"
            "🌟 Комбинированный:\n"
            "• 40 000₽/мес - 2 часа в день\n"
            "• 80 000₽/мес - 5 часов в день\n"
            "• 100 000₽/мес - 8 часов в день"
        )
        query.edit_message_text(pricing_text)

    elif query.data == 'documents':
        documents_text = (
            "📄 Наши документы:\n\n"
            "• Договор-оферта: [ссылка]\n"
            "• Политика конфиденциальности: [ссылка]\n"
            "• Пользовательское соглашение: [ссылка]"
        )
        query.edit_message_text(documents_text)

    elif query.data == 'contact':
        contact_text = (
            "📞 Связаться с нами:\n\n"
            "• Email: support@assistant-for-rent.com\n"
            "• Телефон: +7 (XXX) XXX-XX-XX\n"
            "• Telegram: @support_assistant"
        )
        query.edit_message_text(contact_text)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Регистрация обработчиков
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_callback))

    print("Bot polling...")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
