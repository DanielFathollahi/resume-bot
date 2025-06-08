from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler

import os

TOKEN = os.environ["TOKEN"]
bot = Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0)

PDF_PATH = "resume.pdf"
ADMIN_CHAT_ID = 6441736006

# Route /ping برای نگه داشتن سرویس فعال
@app.route('/ping')
def ping():
    return 'pong'

# Route webhook برای تلگرام
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'OK'

# تعریف handler ها مشابه کد قبلی
async def start(update, context):
    user = update.message.from_user
    info = (
        f"کاربر جدید!\n"
        f"👤 نام: {user.first_name} {user.last_name or ''}\n"
        f"🆔 آیدی عددی: {user.id}\n"
        f"🔗 یوزرنیم: @{user.username}" if user.username else "🔗 بدون یوزرنیم"
    )
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=info)

    keyboard = [
        [InlineKeyboardButton("رزومه", callback_data="send_resume"),
         InlineKeyboardButton("پروژه", callback_data="send_project")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("سلام! یکی از گزینه‌ها را انتخاب کنید:", reply_markup=reply_markup)

async def button_handler(update, context):
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

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(button_handler))

if __name__ == "__main__":
    # این پورت رو Render خودش تعیین می‌کنه
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
