import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from linkedin_agent import generate_ice_breakers


load_dotenv()


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    await update.message.reply_text(
        "👋 Привет! Я бот для генерации персонализированных сообщений LinkedIn.\n\n"
        "📝 Отправь мне текст био профиля LinkedIn, и я создам 3 варианта "
        "персонализированных сообщений для знакомства.\n\n"
        "💡 Пример: 'Иван, основатель стартапа в сфере FinTech...'"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    await update.message.reply_text(
        "ℹ️ Как пользоваться:\n\n"
        "1. Скопируй текст био из LinkedIn профиля\n"
        "2. Отправь его мне в сообщении\n"
        "3. Получи 3 варианта персонализированных сообщений\n\n"
        "📌 Команды:\n"
        "/start - Начать работу\n"
        "/help - Показать эту справку\n"
        "/example - Показать пример"
    )


async def example_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /example"""
    example_text = """Пример био профиля:

'Ахат, основатель ТОО в Казахстане. Занимаюсь оценкой, консалтингом и логистикой. 
Сейчас внедряю ИИ-агентов в свои бизнес-процессы, чтобы автоматизировать холодные продажи 
в LinkedIn и обработку заказов в WhatsApp. Ищу в команду быстрых разработчиков.'

Просто отправь мне такой текст, и я сгенерирую персонализированные сообщения! 🚀"""
    
    await update.message.reply_text(example_text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений"""
    user_text = update.message.text
    
    
    if len(user_text) < 20:
        await update.message.reply_text(
            "⚠️ Текст профиля слишком короткий. Пожалуйста, отправь более подробное описание."
        )
        return
    
    
    processing_msg = await update.message.reply_text(
        "⏳ Анализирую профиль и генерирую персонализированные сообщения..."
    )
    
    try:
        ice_breakers = generate_ice_breakers(user_text, api_provider="openai")
        response = "✅ Вот 3 варианта персонализированных сообщений:\n\n"
        
        for i, message in enumerate(ice_breakers, 1):
            response += f"━━━━━━━━━━━━━━━\n"
            response += f"📨 Вариант {i} ({len(message)} символов):\n"
            response += f"{message}\n\n"
        
        response += "━━━━━━━━━━━━━━━\n"
        response += "💡 Выбери наиболее подходящий вариант или используй как основу!"
        
        
        await processing_msg.delete()
        
        
        await update.message.reply_text(response)
        
    except Exception as e:
        logger.error(f"Ошибка при генерации: {e}")
        await processing_msg.delete()
        await update.message.reply_text(
            f"❌ Произошла ошибка: {str(e)}\n\n"
            "Проверь настройки API ключа в .env файле."
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error(f"Update {update} caused error {context.error}")


def main():
    """Запуск бота"""
    
    
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN не найден в переменных окружения")
    
    
    application = Application.builder().token(token).build()
    
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("example", example_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    
    application.add_error_handler(error_handler)
    
    
    logger.info("Бот запущен и готов к работе!")
    print("🤖 Telegram-бот запущен успешно!")
    print("📱 Найди своего бота в Telegram и начни отправлять био профили")
    print("🛑 Для остановки нажми Ctrl+C")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
