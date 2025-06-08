from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# بارگذاری فایل .env و گرفتن توکن
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# هندلر دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من ربات شما هستم 🤖")

# اجرای ربات
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("✅ ربات با موفقیت راه‌اندازی شد...")
    app.run_polling()
