import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ["TOKEN"]  # از محیط دریافت می‌کنیم

# وقتی کاربر /start بزند
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! رزومه‌ی من برای شما ارسال می‌شود. لطفاً چند لحظه صبر کنید.")

    # مسیر فایل PDF رزومه
    pdf_path = "resume.pdf"

    # ارسال فایل
    with open(pdf_path, "rb") as pdf_file:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=pdf_file)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # ثبت دستور start
    app.add_handler(CommandHandler("start", start))

    # اجرا
    app.run_polling()
