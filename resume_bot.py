import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import threading

TOKEN = os.environ["TOKEN"]
PDF_PATH = "resume.pdf"
ADMIN_CHAT_ID = 6441736006  # آیدی عددی شما

app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'pong'

# کد ربات تلگرام
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    info = (
        f"کاربر جدید!\n"
        f"👤 نام: {user.first_name} {user.last_name or ''}\n"
        f"🆔 آیدی عددی: {user.id}\n"
        f"🔗 یوزرنیم: @{user.username}" if user.username else "🔗 بدون یوزرنیم"
    )
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=info)

    keyboard = [
        [
            InlineKeyboardButton("رزومه", callback_data="send_resume"),
            InlineKeyboardButton("پروژه", callback_data="send_project"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "سلام! یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "send_resume":
        if not os.path.exists(PDF_PATH):
            await query.edit_message_text("فایل رزومه پیدا نشد.")
            return

        with open(PDF_PATH, "rb") as pdf_file:
            await context.bot.send_document(chat_id=query.message.chat.id, document=pdf_file)

    elif query.data == "send_project":
        await query.message.reply_text("این پروژه‌های من است: https://example.com/projects")

def run_bot():
    app_telegram = ApplicationBuilder().token(TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(CallbackQueryHandler(button_handler))
    print("ربات در حال اجراست...")
    app_telegram.run_polling()

if __name__ == "__main__":
    # اجرای وب‌سرور Flask در Thread جدا
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8000)).start()
    # اجرای ربات تلگرام
    run_bot()
