import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ["TOKEN"]
PDF_PATH = "resume.pdf"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

        try:
            with open(PDF_PATH, "rb") as pdf_file:
                await context.bot.send_document(chat_id=query.message.chat.id, document=pdf_file)
        except Exception as e:
            await query.edit_message_text(f"خطا در ارسال فایل: {e}")

    elif query.data == "send_project":
        await query.message.reply_text("این پروژه‌های من است: https://example.com/projects")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("ربات در حال اجراست...")
    app.run_polling()
