import os
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)
import threading

TOKEN = os.environ["TOKEN"]
GROUP_CHAT_ID = -1002848835602

# اضافه کردن ایموجی شیشه‌ای کنار هر زبان برای حس بهتر
LANGUAGES = {
    "🔲 فارسی": "fa",
    "🔲 English": "en",
    "🔲 العربية": "ar",
    "🔲 简体中文": "zh",
    "🔲 Türkçe": "tr",
    "🔲 한국어": "ko",
    "🔲 Srpski": "sr",
    "🔲 Español": "es"
}

RESUMES = {
    "fa": "سلام! من دانیال فتح‌اللهی هستم، برنامه‌نویس و بازی‌ساز...",
    "en": "Hello! I'm Danial Fathollahi, programmer and game developer...",
    "ar": "مرحباً! أنا دانيال فتح اللهي، مبرمج ومطور ألعاب...",
    "zh": "你好！我是丹尼尔·法塔拉希，程序员和游戏开发者...",
    "tr": "Merhaba! Ben Danial Fathollahi, programcı ve oyun geliştiriciyim...",
    "ko": "안녕하세요! 저는 다니엘 파톨라히입니다, 프로그래머이자 게임 개발자...",
    "sr": "Zdravo! Ja sam Danijal Fatolahiji, programer i developer igara...",
    "es": "¡Hola! Soy Danial Fathollahi, programador y desarrollador de juegos..."
}

user_languages = {}

app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'pong'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_languages[user.id] = None

    info = (
        f"کاربر جدید!\n"
        f"👤 نام: {user.first_name} {user.last_name or ''}\n"
        f"🆔 آیدی عددی: {user.id}\n"
        f"🔗 یوزرنیم: @{user.username}" if user.username else "🔗 بدون یوزرنیم"
    )
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=info)

    keyboard = [[KeyboardButton(lang)] for lang in LANGUAGES.keys()]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        "لطفاً زبان خود را انتخاب کنید:",
        reply_markup=reply_markup
    )

async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    if text not in LANGUAGES:
        await update.message.reply_text("لطفاً یکی از زبان‌ها را انتخاب کنید.")
        return
    lang_code = LANGUAGES[text]
    user_languages[user.id] = lang_code

    welcome_texts = {
        "fa": "زبان شما ثبت شد. همه رزومه‌ها را برایتان ارسال می‌کنم.",
        "en": "Language set. Sending all resumes now.",
        "ar": "تم تعيين اللغة. سأرسل جميع السير الذاتية الآن.",
        "zh": "语言已设置。现在发送所有简历。",
        "tr": "Dil ayarlandı. Tüm özgeçmişleri gönderiyorum.",
        "ko": "언어가 설정되었습니다. 모든 이력서를 보내드립니다.",
        "sr": "Jezik je postavljen. Šaljem sve biografije sada.",
        "es": "Idioma establecido. Enviando todos los currículums ahora."
    }
    await update.message.reply_text(welcome_texts[lang_code])

    # ارسال همه رزومه ها در یک پیام یا چند پیام جدا (اینجا یک پیام طولانی)
    all_resumes_text = "\n\n".join(
        f"--- {k} ---\n{v}" for k, v in RESUMES.items()
    )
    await update.message.reply_text(all_resumes_text)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text.lower()
    lang = user_languages.get(user.id)

    if lang is None:
        await update.message.reply_text("لطفاً ابتدا زبان خود را انتخاب کنید.")
        return

    about_keywords = {
        "fa": ["درباره من", "همکاری با من"],
        "en": ["about me", "collaboration"],
        "ar": ["عني", "تعاون"],
        "zh": ["关于我", "合作"],
        "tr": ["hakkımda", "iş birliği"],
        "ko": ["내 소개", "협력"],
        "sr": ["o meni", "saradnja"],
        "es": ["sobre mí", "colaboración"]
    }

    if any(keyword in text for keyword in about_keywords.get(lang, [])):
        await update.message.reply_text(RESUMES[lang])
    else:
        default_responses = {
            "fa": "لطفاً سوالتان را واضح‌تر بپرسید یا «درباره من» یا «همکاری با من» را تایپ کنید.",
            "en": "Please ask clearly or type 'about me' or 'collaboration'.",
            "ar": "يرجى طرح السؤال بوضوح أو كتابة 'عني' أو 'تعاون'.",
            "zh": "请清楚提问，或输入“关于我”或“合作”。",
            "tr": "Lütfen net sorun veya 'hakkımda' ya da 'iş birliği' yazın.",
            "ko": "명확하게 질문하거나 '내 소개' 또는 '협력'을 입력하세요.",
            "sr": "Molimo pitajte jasno ili napišite 'o meni' ili 'saradnja'.",
            "es": "Por favor, pregunta claramente o escribe 'sobre mí' o 'colaboración'."
        }
        await update.message.reply_text(default_responses.get(lang, "Please ask clearly."))

def run_bot():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, language_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("ربات در حال اجراست...")
    application.run_polling()

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8000)).start()
    run_bot()
