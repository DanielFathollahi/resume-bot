import os
import threading
from flask import Flask
from telegram import (
    Update, KeyboardButton, ReplyKeyboardMarkup,
    InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler,
    ConversationHandler, ContextTypes, filters
)

TOKEN = os.getenv("TOKEN")
GROUP_CHAT_ID = -1002542201765

app = Flask(__name__)

@app.route('/')
def ping():
    return 'pong'

ASK_LANGUAGE, ASK_NAME, ASK_JOB, ASK_PHONE, ASK_EMAIL = range(5)

# مسیر فایل‌های صوتی معرفی رزومه
voice_files = {
    'fa': 'رزومه به فارسی.ogg',
    'en': 'Resume in English.ogg',
    'ar': 'السيرة الذاتية بالعربية.ogg',
    'zh': '简历中文.ogg'
}

translations = {
    'fa': {
        'intro': """
من دانیال فتح‌اللهی هستم؛ برنامه‌نویس، طراح و بازی‌ساز با تجربه در یونیتی، وب، و نرم‌افزارهای گرافیکی. علاقه‌مند به تکنولوژی، ورزش، و نوآوری هستم.
        
تحصیلات:
- فارغ‌التحصیل رشته کامپیوتر، هنرستان نعیم‌آباد
- دو مدرک از دانشگاه هاروارد: CS50x و CS50AI

مهارت‌ها:
Python، C، C#، HTML & CSS، Unity، WordPress، Photoshop، Premiere، After Effects، DaVinci Resolve، Office
        
سازنده بازی آشوب کلمات در مایکت
عضو تیم ملی واترپلو ایران
""",
        'ask_name': "لطفاً نام و نام خانوادگی خود را وارد کنید ✍️",
        'ask_job': "لطفاً اطلاعات شغلی خود را بنویسید ✍️",
        'ask_phone': "لطفاً شماره تلفن خود را ارسال کنید 📱",
        'ask_email': "لطفاً ایمیل خود را وارد کنید 📧",
        'thanks': "✅ اطلاعات شما ثبت شد. ممنون 🙏",
        'cancel': "لغو شد."
    },
    'en': {
        'intro': """
I am Daniel Fathollahi; a programmer, designer, and game developer experienced in Unity, web, and graphic software. Passionate about technology, sports, and innovation.

Education:
- Computer Science graduate, Naeem-Abad Technical School
- Two certificates from Harvard University: CS50x and CS50AI

Skills:
Python, C, C#, HTML & CSS, Unity, WordPress, Photoshop, Premiere, After Effects, DaVinci Resolve, Office

Developer of the mobile game "Chaos of Words" on Myket
Member of Iran's national water polo team
""",
        'ask_name': "Please enter your full name ✍️",
        'ask_job': "Please describe your job or business ✍️",
        'ask_phone': "Please send your phone number 📱",
        'ask_email': "Please enter your email address 📧",
        'thanks': "✅ Your information has been recorded. Thank you 🙏",
        'cancel': "Cancelled."
    },
    'ar': {
        'intro': """
أنا دانيال فتح‌اللهي؛ مبرمج، مصمم ومطور ألعاب ذو خبرة في Unity والويب وبرامج التصميم. شغوف بالتكنولوجيا والرياضة والابتكار.

التعليم:
- خريج تخصص الحاسوب من مدرسة نعيم آباد التقنية
- شهادتان من جامعة هارفارد: CS50x و CS50AI

المهارات:
Python، C، C#، HTML & CSS، Unity، WordPress، Photoshop، Premiere، After Effects، DaVinci Resolve، Office

مطور لعبة "فوضى الكلمات" على Myket
عضو في الفريق الوطني الإيراني لكرة الماء
""",
        'ask_name': "يرجى إدخال الاسم الكامل ✍️",
        'ask_job': "يرجى وصف عملك أو مهنتك ✍️",
        'ask_phone': "يرجى إرسال رقم الهاتف 📱",
        'ask_email': "يرجى إدخال البريد الإلكتروني 📧",
        'thanks': "✅ تم تسجيل معلوماتك. شكرًا 🙏",
        'cancel': "تم الإلغاء."
    },
    'zh': {
        'intro': """
我是丹尼尔·法托拉希；一名程序员、设计师和游戏开发者，擅长Unity、网页开发和图形软件。热爱技术、运动和创新。

教育背景：
- 纳伊姆阿巴德技术学校计算机专业毕业
- 哈佛大学CS50x和CS50AI证书

技能：
Python、C、C#、HTML & CSS、Unity、WordPress、Photoshop、Premiere、After Effects、DaVinci Resolve、Office

《混乱之词》手机游戏开发者（Myket平台）
伊朗国家水球队队员
""",
        'ask_name': "请输入您的全名 ✍️",
        'ask_job': "请输入您的职业信息 ✍️",
        'ask_phone': "请发送您的电话号码 📱",
        'ask_email': "请输入您的电子邮件地址 📧",
        'thanks': "✅ 您的信息已记录。谢谢 🙏",
        'cancel': "已取消。"
    }
}
# ادامه کد مثل ساختار بالا...
