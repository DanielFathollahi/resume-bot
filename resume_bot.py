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
        resume_text = """شناگر حرفه‌ای و بازیکن حرفه‌ای واترپلو

برنامه‌نویسی و توسعه اپلیکیشن‌های اندروید

آشنایی با نرم‌افزار Unity و توسعه بازی‌های موبایل

طراحی و برنامه‌نویسی بازی‌های کلمات و پازل

توانایی کار با نرم‌افزارهای آفیس (Word, Excel, PowerPoint)

علاقه‌مند به یادگیری مباحث هوش مصنوعی و توسعه نرم‌افزار

آشنایی با اصول و تکنیک‌های تحلیل و ساخت بازی‌های کامپیوتری

توانایی مدیریت پروژه‌های کوچک برنامه‌نویسی و طراحی بازی

مسلط به زبان فارسی و دارای توانایی پایه در زبان انگلیسی

تجربه‌ها:

ساخت بازی کلمه‌ای در Unity

برنامه‌نویسی اپلیکیشن‌های اندروید و انتشار آن‌ها در گوگل پلی

شرکت در مسابقات شنای حرفه‌ای و واترپلو

همکاری در پروژه‌های کوچک نرم‌افزاری و طراحی بازی

اهداف و علاقه‌مندی‌ها:

توسعه مهارت‌های برنامه‌نویسی و طراحی بازی

تبدیل شدن به یک میلیاردر و موفق در زمینه تجارت و فناوری

ادامه تحصیل در رشته علوم کامپیوتر یا مهندسی نرم‌افزار
"""
        await query.edit_message_text(resume_text)
    elif data == 'projects':
        await query.edit_message_text("🔹 این پروژه‌هام هستن: ...")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_click))
app.run_polling()
