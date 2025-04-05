import os
from dotenv import load_dotenv
from openai import OpenAI
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update

# Загружаем .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Инициализируем OpenAI клиент
client = OpenAI(api_key=OPENAI_API_KEY)

# Обработчик Telegram-сообщений
async def chat_with_openai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message.content.strip()

    except Exception as e:
        reply = f"Ошибка при обращении к OpenAI: {e}"

    await update.message.reply_text(reply)

# Настройка Telegram бота
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_openai))

print("Бот запущен с OpenAI 1.0+")
app.run_polling()


