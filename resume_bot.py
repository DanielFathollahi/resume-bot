import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

TOKEN = "7403835902:AAG-6KAhT3fP1XNlUjHQs_TVGSl3EPwu_1g"

# پیام شروع بات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📄 رزومه", callback_data='resume')],
        [InlineKeyboardButton("🛠 پروژه‌ها", callback_data='projects')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("یکی از گزینه‌های زیر را انتخاب کن:", reply_markup=reply_markup)

# کنترل دکمه‌ها
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == 'resume':
        resume_text = """✅ رزومه من:

🏊‍♂️ شناگر حرفه‌ای و بازیکن حرفه‌ای واترپلو  
📱 توسعه‌دهنده اپلیکیشن‌های اندروید  
🎮 توسعه‌دهنده بازی با Unity  
🧩 ساخت بازی‌های کلمه‌ای  
💼 آشنا با Word, Excel, PowerPoint  
🤖 علاقه‌مند به هوش مصنوعی و برنامه‌نویسی  
🎯 هدف: میلیاردر شدن در زمینه فناوری و تجارت
"""
        await query.edit_message_text(resume_text)
    elif data == 'projects':
        await query.edit_message_text("🔹 این پروژه‌هام هستن:\n1. بازی Amirza-like\n2. اپلیکیشن پرداخت 'صندوق'\n3. ربات تلگرام رزومه\n4. بازی Wall Ball در Unity")

# ساخت اپ و فعال‌سازی وب‌هوک
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_click))

# اجرا به صورت webhook برای Render
app.run_webhook(
    listen="0.0.0.0",
    port=int(os.environ.get('PORT', 5000)),
    webhook_url="https://resume-bot-1w9j.onrender.com"
)
