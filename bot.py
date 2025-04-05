from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
import os

# Читаем токен
with open("token.txt") as f:
    TOKEN = f.read().strip()

async def reply_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет!")

app = ApplicationBuilder().token(TOKEN).build()

# Регистрируем обработчик всех сообщений
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_hello))

print("Бот запущен...")
app.run_polling()
