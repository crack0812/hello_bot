import os
from dotenv import load_dotenv
from openai import OpenAI
from telegram.ext import (
    ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
)
from telegram import Update

# Загружаем .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# 🔐 Разрешённые пользователи (вставь сюда свои user_id)
ALLOWED_USERS = [
    7805692305, 792501309, 5965928738
]

# 🧠 Память чатов
chat_history = {}

# ✅ Команда /reset — очистка диалога
async def reset_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("⛔ У вас нет доступа к этому боту.")
        return

    chat_history[user_id] = []
    await update.message.reply_text("🧠 История диалога очищена!")

# 💬 Обработка сообщений
async def chat_with_openai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text

    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("⛔ У вас нет доступа к этому боту.")
        return

    if user_id not in chat_history:
        chat_history[user_id] = []

    chat_history[user_id].append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_history[user_id]
        )
        reply = response.choices[0].message.content.strip()
        chat_history[user_id].append({"role": "assistant", "content": reply})

    except Exception as e:
        reply = f"❌ Ошибка при обращении к OpenAI: {e}"

    await update.message.reply_text(reply)

# 🚀 Запуск Telegram бота
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("reset", reset_history))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_openai))

print("�� Бот с контекстом, /reset и ограничением по пользователям запущен!")
app.run_polling()

