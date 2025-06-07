from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

TOKEN = "7403835902:AAG-6KAhT3fP1XNlUjHQs_TVGSl3EPwu_1g"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📄 رزومه", callback_data='resume')],
        [InlineKeyboardButton("🛠 پروژه‌ها", callback_data='projects')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("یکی از گزینه‌های زیر را انتخاب کن:", reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == 'resume':
        await query.edit_message_text("🔹 این رزومه‌ی منه: ...")
    elif data == 'projects':
        await query.edit_message_text("🔹 این پروژه‌هام هستن: ...")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_click))
app.run_polling()
