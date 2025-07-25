import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes, ConversationHandler
)

TOKEN = os.environ.get("TOKEN")
ADMIN_CHAT_ID = -1002848835602  # آیدی عددی شما

app = Flask(__name__)

LANG_SELECT, MAIN_MENU = range(2)

# زبان‌ها و پرچم‌ها
LANGUAGES = {
    'fa': {'name': 'فارسی', 'flag': '🇮🇷'},
    'ar': {'name': 'العربية', 'flag': '🇸🇦'},
    'zh': {'name': '中文', 'flag': '🇨🇳'},
    'tr': {'name': 'Türkçe', 'flag': '🇹🇷'},
    'ko': {'name': '한국어', 'flag': '🇰🇷'},
    'sr': {'name': 'Srpski', 'flag': '🇷🇸'},
    'es': {'name': 'Español', 'flag': '🇪🇸'},
    'en': {'name': 'English', 'flag': '🇬🇧'},
}

# متن‌های چندزبانه
TEXTS = {
    'fa': {
        'choose_lang': 'لطفاً زبان خود را انتخاب کنید:',
        'menu_text': 'لطفاً یکی از گزینه‌ها را انتخاب کنید:',
        'chat_ai': '💬 چت با هوش مصنوعی',
        'about_me': '🤝 همکاری با من',
        'resume': """سلام! 👋  
من **دانیال فتح‌اللهی** هستم؛ یه آدم خلاق، پرتلاش و عاشق تکنولوژی! 💡  
🔧 برنامه‌نویس، 🎮 بازی‌ساز و 🎨 طراح گرافیک با تجربه در ساخت پروژه‌های واقعی.

💻 زبان‌های برنامه‌نویسی:
• Python 🐍  
• C / C# 💻  
• HTML & CSS 🌐  

🕹️ بازی‌سازی:
• ساخت بازی با Unity  
• انتشار بازی در مایکت: «آشوب کلمات» ⚔️🧩  

🌍 توسعه وب:
• طراحی سایت با WordPress  
• مدیریت و پشتیبانی سایت‌های محتوایی  

🎬 طراحی و ویرایش گرافیک و ویدیو:
• Photoshop 🖌️  
• Premiere 🎞️  
• After Effects 🌟  
• DaVinci Resolve 🎥  

📊 نرم‌افزارهای کاربردی:
• Microsoft Office (ورد، اکسل، پاورپوینت) 📄📈  

📚 دوره‌ها و مدارک بین‌المللی:
• CS50x – مبانی علوم کامپیوتر (Harvard University)  
• CS50s – هوش مصنوعی (Harvard University) 🤖

🏅 عضو تیم ملی واترپلو ایران 🏊‍♂️  
📚 علاقه‌مند به مطالعه، ورزش و یادگیری مداوم  
🎯 هدفم: ساخت محصولات تکنولوژیک تأثیرگذار و خلاقانه

📞 راه‌های ارتباطی:
📍 موقعیت: یزد – ایران  
📧 ایمیل: daniel.fathollahi.4@gmail.com  
📱 شماره تماس: 0933-835-8107
""",
    },
    'ar': {
        'choose_lang': 'يرجى اختيار لغتك:',
        'menu_text': 'يرجى اختيار أحد الخيارات:',
        'chat_ai': '💬 دردشة مع الذكاء الاصطناعي',
        'about_me': '🤝 التعاون معي',
        'resume': """مرحباً! 👋  
أنا **دانيال فتح اللهي**، شخص مبدع ومجتهد ومحب للتكنولوجيا! 💡  
🔧 مبرمج، 🎮 مطور ألعاب، و🎨 مصمم جرافيك ذو خبرة في المشاريع الواقعية.

💻 لغات البرمجة:
• Python 🐍  
• C / C# 💻  
• HTML & CSS 🌐  

🕹️ تطوير الألعاب:
• تطوير الألعاب باستخدام Unity  
• نشر لعبة على Myket: "فوضى الكلمات" ⚔️🧩  

🌍 تطوير المواقع:
• تصميم المواقع باستخدام WordPress  
• إدارة ودعم المواقع المحتوية  

🎬 تصميم وتحرير الجرافيك والفيديو:
• Photoshop 🖌️  
• Premiere 🎞️  
• After Effects 🌟  
• DaVinci Resolve 🎥  

📊 برامج الإنتاجية:
• Microsoft Office (Word، Excel، PowerPoint) 📄📈  

📚 الشهادات:
• CS50x – علوم الحاسوب (جامعة هارفارد)  
• CS50s – الذكاء الاصطناعي (جامعة هارفارد) 🤖

🏅 عضو في المنتخب الوطني الإيراني للواتر بولو 🏊‍♂️  
📚 مهتم بالقراءة والرياضة والتعلم المستمر  
🎯 الهدف: إنشاء منتجات تقنية مبتكرة وذات تأثير

📍 الموقع: يزد – إيران  
📧 البريد الإلكتروني: daniel.fathollahi.4@gmail.com  
📱 رقم الهاتف: 0933-835-8107
"""
    },
    'zh': {
        'choose_lang': '请选择您的语言：',
        'menu_text': '请选择一个选项：',
        'chat_ai': '💬 与人工智能聊天',
        'about_me': '🤝 与我合作',
        'resume': """你好！👋  
我是**丹尼尔·法塔拉希**，一个有创造力、努力工作并热爱科技的人！💡  
🔧 程序员、🎮 游戏开发者 和 🎨 平面设计师，拥有实际项目经验。

💻 编程语言:
• Python 🐍  
• C / C# 💻  
• HTML 和 CSS 🌐  

🕹️ 游戏开发:
• 使用 Unity 开发游戏  
• 已在 Myket 上发布游戏《混乱之词》⚔️🧩  

🌍 网站开发:
• 使用 WordPress 设计网站  
• 内容网站的管理和支持  

🎬 平面与视频编辑:
• Photoshop 🖌️  
• Premiere 🎞️  
• After Effects 🌟  
• DaVinci Resolve 🎥  

📊 办公软件:
• Microsoft Office (Word, Excel, PowerPoint) 📄📈  

📚 认证:
• CS50x – 计算机科学 (哈佛大学)  
• CS50s – 人工智能 (哈佛大学) 🤖

🏅 伊朗国家水球队成员 🏊‍♂️  
📚 热爱阅读、运动和持续学习  
🎯 目标：打造创新且有影响力的科技产品

📍 地点：伊朗–亚兹德  
📧 邮箱：daniel.fathollahi.4@gmail.com  
📱 电话：0933-835-8107
"""
    },
    'tr': {
        'choose_lang': 'Lütfen dilinizi seçin:',
        'menu_text': 'Lütfen bir seçenek seçin:',
        'chat_ai': '💬 Yapay Zeka ile Sohbet',
        'about_me': '🤝 Benimle İş Birliği',
        'resume': """Merhaba! 👋  
Ben **Danial Fathollahi**; yaratıcı, çalışkan ve teknoloji tutkunu biriyim! 💡  
🔧 Yazılımcı, 🎮 Oyun Geliştirici ve 🎨 Grafik Tasarımcı olarak gerçek projelerde deneyim sahibiyim.

💻 Programlama Dilleri:
• Python 🐍  
• C / C# 💻  
• HTML & CSS 🌐  

🕹️ Oyun Geliştirme:
• Unity ile oyun geliştirme  
• Myket'te yayınlanan oyun: “Kelimelerin Kaosu” ⚔️🧩  

🌍 Web Geliştirme:
• WordPress ile web tasarımı  
• İçerik sitelerinin yönetimi ve desteği  

🎬 Grafik ve Video Düzenleme:
• Photoshop 🖌️  
• Premiere 🎞️  
• After Effects 🌟  
• DaVinci Resolve 🎥  

📊 Üretkenlik Yazılımları:
• Microsoft Office (Word, Excel, PowerPoint) 📄📈  

📚 Sertifikalar:
• CS50x – Bilgisayar Bilimi (Harvard Üniversitesi)  
• CS50s – Yapay Zeka (Harvard Üniversitesi) 🤖

🏅 İran Su Topu Milli Takımı üyesi 🏊‍♂️  
📚 Okuma, spor ve sürekli öğrenmeye ilgi duyuyorum  
🎯 Amacım: Yenilikçi ve etkileyici teknoloji ürünleri geliştirmek

📍 Konum: Yezd – İran  
📧 E-posta: daniel.fathollahi.4@gmail.com  
📱 Telefon: 0933-835-8107
"""
    },
    'ko': {
        'choose_lang': '언어를 선택하세요:',
        'menu_text': '옵션을 선택하세요:',
        'chat_ai': '💬 AI와 채팅하기',
        'about_me': '🤝 저와 협력하기',
        'resume': """안녕하세요! 👋  
저는 **다니엘 파톨라히**입니다. 창의적이고 성실하며 기술을 사랑하는 사람입니다! 💡  
🔧 프로그래머, 🎮 게임 개발자, 🎨 그래픽 디자이너로 실제 프로젝트 경험이 있습니다.

💻 프로그래밍 언어:
• Python 🐍  
• C / C# 💻  
• HTML & CSS 🌐  

🕹️ 게임 개발:
• Unity를 사용한 게임 제작  
• Myket에 게임 출시: "단어의 혼돈" ⚔️🧩  

🌍 웹 개발:
• WordPress를 이용한 웹사이트 디자인  
• 콘텐츠 사이트 관리 및 지원  

🎬 그래픽 및 영상 편집:
• Photoshop 🖌️  
• Premiere 🎞️  
• After Effects 🌟  
• DaVinci Resolve 🎥  

📊 오피스 소프트웨어:
• Microsoft Office (Word, Excel, PowerPoint) 📄📈  

📚 자격증:
• CS50x – 컴퓨터 과학 (하버드 대학교)  
• CS50s – 인공지능 (하버드 대학교) 🤖

🏅 이란 국가 수구팀 멤버 🏊‍♂️  
📚 독서, 운동, 평생 학습에 관심이 많습니다  
🎯 목표: 혁신적이고 영향력 있는 기술 제품을 만드는 것

📍 위치: 이란 – 야즈드  
📧 이메일: daniel.fathollahi.4@gmail.com  
📱 전화번호: 0933-835-8107
"""
    },
    'sr': {
        'choose_lang': 'Izaberite svoj jezik:',
        'menu_text': 'Izaberite opciju:',
        'chat_ai': '💬 Razgovor sa AI',
        'about_me': '🤝 Saradnja sa mnom',
        'resume': """Zdravo! 👋  
Ja sam **Danijal Fatolahiji**, kreativan, vredan i zaljubljenik u tehnologiju! 💡  
🔧 Programer, 🎮 programer igara i 🎨 grafički dizajner sa iskustvom u stvarnim projektima.

💻 Programski jezici:
• Python 🐍  
• C / C# 💻  
• HTML & CSS 🌐  

🕹️ Razvoj igara:
• Izrada igara pomoću Unity  
• Objavljena igra na Myket: “Haos reči” ⚔️🧩  

🌍 Web razvoj:
• Dizajniranje sajtova pomoću WordPress  
• Upravljanje i podrška za sajtove sa sadržajem  

🎬 Grafička i video obrada:
• Photoshop 🖌️  
• Premiere 🎞️  
• After Effects 🌟  
• DaVinci Resolve 🎥  

📊 Produktivni softver:
• Microsoft Office (Word, Excel, PowerPoint) 📄📈  

📚 Sertifikati:
• CS50x – Računarske nauke (Univerzitet Harvard)  
• CS50s – Veštačka inteligencija (Univerzitet Harvard) 🤖

🏅 Član reprezentacije Irana u vaterpolu 🏊‍♂️  
📚 Zainteresovan za čitanje, sport i kontinuirano učenje  
🎯 Cilj: Kreiranje inovativnih i uticajnih tehnoloških proizvoda

📍 Lokacija: Jazd – Iran  
📧 Email: daniel.fathollahi.4@gmail.com  
📱 Telefon: 0933-835-8107
"""
    },
    'es': {
        'choose_lang': 'Por favor, selecciona tu idioma:',
        'menu_text': 'Por favor, elige una opción:',
        'chat_ai': '💬 Chat con IA',
        'about_me': '🤝 Colaborar conmigo',
        'resume': """¡Hola! 👋  
Soy **Danial Fathollahi**, una persona creativa, trabajadora y apasionada por la tecnología. 💡  
🔧 Programador, 🎮 desarrollador de videojuegos y 🎨 diseñador gráfico con experiencia real en proyectos.

💻 Lenguajes de programación:
• Python 🐍  
• C / C# 💻  
• HTML & CSS 🌐  

🕹️ Desarrollo de videojuegos:
• Creación de juegos con Unity  
• Juego publicado en Myket: “Caos de Palabras” ⚔️🧩  

🌍 Desarrollo web:
• Diseño de sitios web con WordPress  
• Gestión y soporte de sitios de contenido  

🎬 Diseño gráfico y edición de video:
• Photoshop 🖌️  
• Premiere 🎞️  
• After Effects 🌟  
• DaVinci Resolve 🎥  

📊 Software de productividad:
• Microsoft Office (Word, Excel, PowerPoint) 📄📈  

📚 Certificaciones:
• CS50x – Ciencias de la Computación (Universidad de Harvard)  
• CS50s – Inteligencia Artificial (Universidad de Harvard) 🤖

🏅 Miembro del equipo nacional iraní de waterpolo 🏊‍♂️  
📚 Apasionado por la lectura, el deporte y el aprendizaje continuo  
🎯 Objetivo: Crear productos tecnológicos innovadores e impactantes

📍 Ubicación: Yazd – Irán  
📧 Correo: daniel.fathollahi.4@gmail.com  
📱 Teléfono: 0933-835-8107
"""
    },
    'en': {
        'choose_lang': 'Please select your language:',
        'menu_text': 'Please choose an option:',
        'chat_ai': '💬 Chat with AI',
        'about_me': '🤝 Collaborate with me',
        'resume': """Hello! 👋  
I'm **Danial Fathollahi**, a creative, hardworking, and tech-loving individual! 💡  
🔧 Programmer, 🎮 Game Developer, and 🎨 Graphic Designer with real project experience.

💻 Programming Languages:
• Python 🐍  
• C / C# 💻  
• HTML & CSS 🌐  

🕹️ Game Development:
• Game creation with Unity  
• Published a game on Myket: “Chaos of Words” ⚔️🧩  

🌍 Web Development:
• Website design with WordPress  
• Content site management and support  

🎬 Graphic and Video Editing:
• Photoshop 🖌️  
• Premiere 🎞️  
• After Effects 🌟  
• DaVinci Resolve 🎥  

📊 Productivity Software:
• Microsoft Office (Word, Excel, PowerPoint) 📄📈  

📚 Certifications:
• CS50x – Computer Science (Harvard University)  
• CS50s – Artificial Intelligence (Harvard University) 🤖

🏅 Member of Iran National Water Polo Team 🏊‍♂️  
📚 Interested in reading, sports, and lifelong learning  
🎯 Goal: Creating innovative and impactful tech products

📍 Location: Yazd – Iran  
📧 Email: daniel.fathollahi.4@gmail.com  
📱 Phone: 0933-835-8107
"""
    },
}

user_langs = {}

@app.route('/ping')
def ping():
    return 'pong'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    info = (
        f"New user!\n"
        f"👤 Name: {user.first_name} {user.last_name or ''}\n"
        f"🆔 ID: {user.id}\n"
        f"🔗 Username: @{user.username}" if user.username else "🔗 No username"
    )
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=info)

    keyboard = [
        [InlineKeyboardButton(f"{v['flag']} {v['name']}", callback_data=f"lang_{code}")]
        for code, v in LANGUAGES.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please select your language / لطفاً زبان خود را انتخاب کنید:", reply_markup=reply_markup)
    return LANG_SELECT

async def lang_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    lang_code = query.data.split('_')[1]

    if lang_code not in LANGUAGES:
        await query.edit_message_text("Invalid language selected.")
        return ConversationHandler.END

    user_langs[user_id] = lang_code
    texts = TEXTS[lang_code]

    keyboard = [
        [
            InlineKeyboardButton(texts['chat_ai'], callback_data='chat_ai'),
            InlineKeyboardButton(texts['about_me'], callback_data='about_me'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(f"{LANGUAGES[lang_code]['flag']} {texts['menu_text']}", reply_markup=reply_markup)
    return MAIN_MENU

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    lang_code = user_langs.get(user_id, 'en')
    texts = TEXTS[lang_code]

    if query.data == 'about_me':
        await query.edit_message_text(f"{LANGUAGES[lang_code]['flag']} {texts['resume']}")
    elif query.data == 'chat_ai':
        # این قسمت را به دلخواه می‌توانید به چت هوش مصنوعی متصل کنید
        await query.edit_message_text(f"{LANGUAGES[lang_code]['flag']} بخش چت هوش مصنوعی در حال توسعه است.")
    else:
        await query.edit_message_text(f"{LANGUAGES[lang_code]['flag']} {texts['menu_text']}")

    return MAIN_MENU

def run_bot():
    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANG_SELECT: [CallbackQueryHandler(lang_handler, pattern=r'^lang_')],
            MAIN_MENU: [CallbackQueryHandler(main_menu_handler, pattern=r'^(about_me|chat_ai)$')],
        },
        fallbacks=[],
        allow_reentry=True,
    )

    application.add_handler(conv_handler)

    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8000)).start()
    run_bot()
