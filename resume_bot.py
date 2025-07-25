import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ["TOKEN"]
ADMIN_CHAT_ID = 6441736006  # آیدی عددی شما
PDF_PATH = "resume.pdf"

app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'pong'

voice_files = {
    'fa': 'رزومه به فارسی.ogg',
    'en': 'Resume in English.ogg',
    'ar': 'السيرة الذاتية بالعربية.ogg',
    'zh': '简历中文.ogg'
}

translations = {
    'fa': "من دانیال فتح‌اللهی هستم؛ برنامه‌نویس، طراح و بازی‌ساز با تجربه در یونیتی، وب، و نرم‌افزارهای گرافیکی. علاقه‌مند به تکنولوژی، ورزش، و نوآوری هستم.\n\nتحصیلات:\n- فارغ‌التحصیل رشته کامپیوتر، هنرستان نعیم‌آباد\n- دو مدرک از دانشگاه هاروارد: CS50x و CS50AI\n\nمهارت‌ها:\nPython، C، C#، HTML & CSS، Unity، WordPress، Photoshop، Premiere، After Effects، DaVinci Resolve، Office\n\nسازنده بازی آشوب کلمات در مایکت\nعضو تیم ملی واترپلو ایران",
    'en': "I am Daniel Fathollahi; a programmer, designer, and game developer experienced in Unity, web, and graphic software. Passionate about technology, sports, and innovation.\n\nEducation:\n- Computer Science graduate, Naeem-Abad Technical School\n- Two certificates from Harvard University: CS50x and CS50AI\n\nSkills:\nPython, C, C#, HTML & CSS, Unity, WordPress, Photoshop, Premiere, After Effects, DaVinci Resolve, Office\n\nDeveloper of the mobile game \"Chaos of Words\" on Myket\nMember of Iran's national water polo team",
    'ar': "أنا دانيال فتح‌اللهي؛ مبرمج، مصمم ومطور ألعاب ذو خبرة في Unity والويب وبرامج التصميم. شغوف بالتكنولوجيا والرياضة والابتكار.\n\nالتعليم:\n- خريج تخصص الحاسوب من مدرسة نعيم آباد التقنية\n- شهادتان من جامعة هارفارد: CS50x و CS50AI\n\nالمهارات:\nPython، C، C#، HTML & CSS، Unity، WordPress، Photoshop، Premiere، After Effects، DaVinci Resolve، Office\n\nمطور لعبة \"فوضى الكلمات\" على Myket\nعضو في الفريق الوطني الإيراني لكرة الماء",
    'zh': "我是丹尼尔·法托拉希；一名程序员、设计师和游戏开发者，擅长Unity、网页开发和图形软件。热爱技术、运动和创新。\n\n教育背景：\n- 纳伊姆阿巴德技术学校计算机专业毕业\n- 哈佛大学CS50x和CS50AI证书\n\n技能：\nPython、C、C#、HTML & CSS、Unity、WordPress、Photoshop、Premiere、After Effects、DaVinci Resolve、Office\n\n《混乱之词》手机游戏开发者（Myket平台）\n伊朗国家水球队队员"
}

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
            InlineKeyboardButton("رزومه به فارسی 🇮🇷", callback_data="resume_fa"),
            InlineKeyboardButton("Resume in English 🇬🇧", callback_data="resume_en")
        ],
        [
            InlineKeyboardButton("السيرة الذاتية 🇸🇦", callback_data="resume_ar"),
            InlineKeyboardButton("简历 🇨🇳", callback_data="resume_zh")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "سلام! زبان مورد نظر برای دریافت رزومه را انتخاب کنید:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang_key = query.data.replace("resume_", "")

    if lang_key in translations:
        # ارسال متن رزومه
        await query.message.reply_text(translations[lang_key])
        # ارسال فایل صوتی اگر موجود باشد
        voice_path = voice_files.get(lang_key)
        if voice_path and os.path.exists(voice_path):
            with open(voice_path, "rb") as voice:
                await context.bot.send_voice(chat_id=query.message.chat.id, voice=voice)
    else:
        await query.message.reply_text("رزومه مورد نظر یافت نشد.")

    # ارسال فایل PDF کلی (اختیاری)
    if os.path.exists(PDF_PATH):
        with open(PDF_PATH, "rb") as pdf_file:
            await context.bot.send_document(chat_id=query.message.chat.id, document=pdf_file)

def run_bot():
    app_telegram = ApplicationBuilder().token(TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(CallbackQueryHandler(button_handler))
    print("ربات در حال اجراست...")
    app_telegram.run_polling()

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8000)).start()
    run_bot()
