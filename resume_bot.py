from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

LANG, MAIN_MENU = range(2)

# تعریف زبان‌ها و پرچم‌ها
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

# متون به زبان‌ها (نمونه کامل‌تر متن "درباره من" رو جایگذاری کردم)
TEXTS = {
    'fa': {
        'welcome': 'لطفاً زبان خود را انتخاب کنید:',
        'menu': 'لطفاً یکی از گزینه‌ها را انتخاب کنید:',
        'chat_ai': '💬 چت با هوش مصنوعی',
        'about_me': '🤝 همکاری با من',
        'resume': """سلام! 👋  
من **دانیال فتح‌اللهی** هستم؛ یک فرد خلاق، پرتلاش و عاشق تکنولوژی! 💡  
🔧 برنامه‌نویس، 🎮 توسعه‌دهنده بازی و 🎨 طراح گرافیک با تجربه واقعی پروژه.

💻 زبان‌های برنامه‌نویسی:
• Python 🐍  
• C / C# 💻  
• HTML & CSS 🌐  

🕹️ توسعه بازی:
• ساخت بازی با Unity  
• انتشار بازی در Myket: «آشوب کلمات» ⚔️🧩  

🌍 توسعه وب:
• طراحی سایت با WordPress  
• مدیریت و پشتیبانی سایت‌های محتوایی  

🎬 طراحی و تدوین گرافیک و ویدیو:
• Photoshop 🖌️  
• Premiere 🎞️  
• After Effects 🌟  
• DaVinci Resolve 🎥  

📊 نرم‌افزارهای بهره‌وری:
• Microsoft Office (ورد، اکسل، پاورپوینت) 📄📈  

📚 مدارک:
• CS50x – علوم کامپیوتر (دانشگاه هاروارد)  
• CS50s – هوش مصنوعی (دانشگاه هاروارد) 🤖

🏅 عضو تیم ملی واترپلو ایران 🏊‍♂️  
📚 علاقه‌مند به مطالعه، ورزش و یادگیری مادام‌العمر  
🎯 هدف: ساخت محصولات نوآورانه و تاثیرگذار فناوری

📍 یزد – ایران  
📧 daniel.fathollahi.4@gmail.com  
📱 0933-835-8107
""",
    },
    'ar': {
        'welcome': 'يرجى اختيار لغتك:',
        'menu': 'يرجى اختيار أحد الخيارات:',
        'chat_ai': '💬 الدردشة مع الذكاء الاصطناعي',
        'about_me': '🤝 التعاون معي',
        'resume': """مرحباً! 👋  
أنا **دانيال فتح اللهي**، شخص مبدع، مجتهد ومحب للتكنولوجيا! 💡  
🔧 مبرمج، 🎮 مطور ألعاب، و 🎨 مصمم جرافيك ذو خبرة حقيقية.

💻 لغات البرمجة:
• Python 🐍  
• C / C# 💻  
• HTML & CSS 🌐  

🕹️ تطوير الألعاب:
• صناعة ألعاب باستخدام Unity  
• نشر لعبة على Myket: "فوضى الكلمات" ⚔️🧩  

🌍 تطوير المواقع:
• تصميم مواقع بواسطة WordPress  
• إدارة ودعم المواقع المحتوية  

🎬 تصميم وتحرير الفيديو والجرافيك:
• Photoshop 🖌️  
• Premiere 🎞️  
• After Effects 🌟  
• DaVinci Resolve 🎥  

📊 برامج الإنتاجية:
• Microsoft Office (Word، Excel، PowerPoint) 📄📈  

📚 الشهادات:
• CS50x – علوم الحاسوب (جامعة هارفارد)  
• CS50s – الذكاء الاصطناعي (جامعة هارفارد) 🤖

🏅 عضو المنتخب الوطني الإيراني للواتر بولو 🏊‍♂️  
📚 مهتم بالقراءة، الرياضة، والتعلم المستمر  
🎯 الهدف: إنشاء منتجات تقنية مبتكرة وفعالة

📍 يزد – إيران  
📧 daniel.fathollahi.4@gmail.com  
📱 0933-835-8107
"""
    },
    'zh': {
        'welcome': '请选择您的语言：',
        'menu': '请选择以下选项之一：',
        'chat_ai': '💬 与人工智能聊天',
        'about_me': '🤝 与我合作',
        'resume': """你好！👋  
我是**丹尼尔·法塔拉希**，一个有创造力、勤奋且热爱科技的人！💡  
🔧 程序员，🎮 游戏开发者，🎨 平面设计师，拥有真实项目经验。

💻 编程语言：
• Python 🐍  
• C / C# 💻  
• HTML & CSS 🌐  

🕹️ 游戏开发：
• 使用Unity制作游戏  
• 在Myket发布了游戏：“混乱之词” ⚔️🧩  

🌍 网站开发：
• 使用WordPress设计网站  
• 内容网站管理和支持  

🎬 图形和视频编辑：
• Photoshop 🖌️  
• Premiere 🎞️  
• After Effects 🌟  
• DaVinci Resolve 🎥  

📊 办公软件：
• Microsoft Office (Word, Excel, PowerPoint) 📄📈  

📚 认证：
• CS50x – 计算机科学 (哈佛大学)  
• CS50s – 人工智能 (哈佛大学) 🤖

🏅 伊朗国家水球队成员 🏊‍♂️  
📚 喜欢阅读、运动和终身学习  
🎯 目标：创造创新且有影响力的科技产品

📍 位置：伊朗 亚兹德  
📧 daniel.fathollahi.4@gmail.com  
📱 0933-835-8107
"""
    },
    'tr': {
        'welcome': 'Lütfen dilinizi seçiniz:',
        'menu': 'Lütfen seçeneklerden birini seçiniz:',
        'chat_ai': '💬 Yapay zeka ile sohbet',
        'about_me': '🤝 Benimle çalış',
        'resume': """Merhaba! 👋  
Ben **Danial Fathollahi**; yaratıcı, çalışkan ve teknoloji meraklısıyım! 💡  
🔧 Yazılımcı, 🎮 Oyun Geliştirici ve 🎨 Grafik Tasarımcıyım, gerçek proje deneyimim var.

💻 Programlama Dilleri:
• Python 🐍  
• C / C# 💻  
• HTML & CSS 🌐  

🕹️ Oyun Geliştirme:
• Unity ile oyun geliştirme  
• Myket’te yayınlanan oyun: “Kelimelerin Kaosu” ⚔️🧩  

🌍 Web Geliştirme:
• WordPress ile web sitesi tasarımı  
• İçerik sitesi yönetimi ve destek  

🎬 Grafik ve Video Düzenleme:
• Photoshop 🖌️  
• Premiere 🎞️  
• After Effects 🌟  
• DaVinci Resolve 🎥  

📊 Üretkenlik Yazılımları:
• Microsoft Office (Word, Excel, PowerPoint) 📄📈  

📚 Sertifikalar:
• CS50x – Bilgisayar Bilimleri (Harvard Üniversitesi)  
• CS50s – Yapay Zeka (Harvard Üniversitesi) 🤖

🏅 İran Su Topu Milli Takımı Üyesi 🏊‍♂️  
📚 Okumaya, spora ve sürekli öğrenmeye ilgiliyim  
🎯 Amaç: Yenilikçi ve etkileyici teknoloji ürünleri geliştirmek

📍 Konum: Yezd – İran  
📧 daniel.fathollahi.4@gmail.com  
📱 0933-835-8107
"""
    },
    'ko': {
        'welcome': '언어를 선택하세요:',
        'menu': '옵션 중 하나를 선택하세요:',
        'chat_ai': '💬 인공지능과 대화하기',
        'about_me': '🤝 나와 협력하기',
        'resume': """안녕하세요! 👋  
저는 **다니엘 파톨라히**입니다. 창의적이고, 성실하며, 기술을 사랑하는 사람입니다! 💡  
🔧 프로그래머, 🎮 게임 개발자, 🎨 그래픽 디자이너이며 실제 프로젝트 경험이 있습니다.

💻 프로그래밍 언어:
• Python 🐍  
• C / C# 💻  
• HTML & CSS 🌐  

🕹️ 게임 개발:
• Unity로 게임 제작  
• Myket에 “단어의 혼돈” 게임 출시 ⚔️🧩  

🌍 웹 개발:
• WordPress로 웹사이트 디자인  
• 콘텐츠 사이트 관리 및 지원  

🎬 그래픽 및 비디오 편집:
• Photoshop 🖌️  
• Premiere 🎞️  
• After Effects 🌟  
• DaVinci Resolve 🎥  

📊 생산성 소프트웨어:
• Microsoft Office (Word, Excel, PowerPoint) 📄📈  

📚 자격증:
• CS50x – 컴퓨터 과학 (하버드 대학교)  
• CS50s – 인공지능 (하버드 대학교) 🤖

🏅 이란 국가 수구팀 멤버 🏊‍♂️  
📚 독서, 스포츠, 평생 학습에 관심 많음  
🎯 목표: 혁신적이고 영향력 있는 기술 제품 만들기

📍 위치: 이란 야즈드  
📧 daniel.fathollahi.4@gmail.com  
📱 0933-835-8107
"""
    },
    'sr': {
        'welcome': 'Izaberite jezik:',
        'menu': 'Izaberite jednu od opcija:',
        'chat_ai': '💬 Čat sa veštačkom inteligencijom',
        'about_me': '🤝 Saradnja sa mnom',
        'resume': """Zdravo! 👋  
Ja sam **Danijal Fatolahiji**, kreativan, vredan i zaljubljenik u tehnologiju! 💡  
🔧 Programer, 🎮 Razvijač igara i 🎨 Grafički dizajner sa stvarnim iskustvom.

💻 Programski jezici:
• Python 🐍  
• C / C# 💻  
• HTML & CSS 🌐  

🕹️ Razvoj igara:
• Izrada igara pomoću Unity  
• Objavljena igra na Myket: “Haos reči” ⚔️🧩  

🌍 Web razvoj:
• Dizajn sajtova pomoću WordPress  
• Upravljanje i podrška sajtovima  

🎬 Grafička i video obrada:
• Photoshop 🖌️  
• Premiere 🎞️  
• After Effects 🌟  
• DaVinci Resolve 🎥  

📊 Produktivni softver:
• Microsoft Office (Word, Excel, PowerPoint) 📄📈  

📚 Sertifikati:
• CS50x – Računarske nauke (Harvard Univerzitet)  
• CS50s – Veštačka inteligencija (Harvard Univerzitet) 🤖

🏅 Član iranske reprezentacije u vaterpolu 🏊‍♂️  
📚 Zainteresovan za čitanje, sport i kontinuirano učenje  
🎯 Cilj: Kreiranje inovativnih i uticajnih tehnoloških proizvoda

📍 Lokacija: Jazd – Iran  
📧 daniel.fathollahi.4@gmail.com  
📱 0933-835-8107
"""
    },
    'es': {
        'welcome': 'Por favor seleccione su idioma:',
        'menu': 'Por favor seleccione una opción:',
        'chat_ai': '💬 Chat con inteligencia artificial',
        'about_me': '🤝 Colaborar conmigo',
        'resume': """¡Hola! 👋  
Soy **Danial Fathollahi**, una persona creativa, trabajadora y apasionada por la tecnología! 💡  
🔧 Programador, 🎮 Desarrollador de juegos y 🎨 Diseñador gráfico con experiencia real.

💻 Lenguajes de programación:
• Python 🐍  
• C / C# 💻  
• HTML & CSS 🌐  

🕹️ Desarrollo de juegos:
• Creación de juegos con Unity  
• Juego publicado en Myket: “Caos de Palabras” ⚔️🧩  

🌍 Desarrollo web:
• Diseño web con WordPress  
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

🏅 Miembro del equipo nacional de waterpolo de Irán 🏊‍♂️  
📚 Apasionado por la lectura, el deporte y el aprendizaje continuo  
🎯 Objetivo: Crear productos tecnológicos innovadores e impactantes

📍 Ubicación: Yazd – Irán  
📧 daniel.fathollahi.4@gmail.com  
📱 0933-835-8107
"""
    },
    'en': {
        'welcome': 'Please select your language:',
        'menu': 'Please choose an option:',
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
📧 daniel.fathollahi.4@gmail.com  
📱 0933-835-8107
"""
    }
}

user_langs = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[
        KeyboardButton(f"{data['flag']} {data['name']}") for code, data in LANGUAGES.items()
    ]]
    await update.message.reply_text(
        "لطفاً زبان خود را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return LANG

async def lang_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    user_id = update.effective_user.id

    # تشخیص زبان انتخاب شده با پرچم یا نام
    chosen_lang = None
    for code, data in LANGUAGES.items():
        if data['flag'] in text or data['name'] in text:
            chosen_lang = code
            break

    if not chosen_lang:
        await update.message.reply_text("زبان معتبر انتخاب نشده، لطفا دوباره انتخاب کنید.")
        return LANG

    user_langs[user_id] = chosen_lang
    lang_texts = TEXTS[chosen_lang]

    keyboard = [[
        KeyboardButton(lang_texts['chat_ai']),
        KeyboardButton(lang_texts['about_me'])
    ]]

    await update.message.reply_text(
        f"{lang_texts['menu']} {LANGUAGES[chosen_lang]['flag']}",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return MAIN_MENU

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    chosen_lang = user_langs.get(user_id, 'en')
    lang_texts = TEXTS[chosen_lang]

    text = update.message.text
    if text == lang_texts['about_me']:
        # ارسال رزومه به زبان انتخاب شده
        await update.message.reply_text(f"{LANGUAGES[chosen_lang]['flag']} {lang_texts['resume']}", parse_mode='Markdown')
    elif text == lang_texts['chat_ai']:
        # پیام خوش‌آمدگویی به چت هوش مصنوعی (قابل توسعه)
        await update.message.reply_text(f"{LANGUAGES[chosen_lang]['flag']} خوش آمدید به بخش چت هوش مصنوعی! این بخش در حال توسعه است.")
    else:
        await update.message.reply_text(lang_texts['menu'])

    return MAIN_MENU

def main():
    app = Application.builder().token("YOUR_TELEGRAM_BOT_TOKEN").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANG: [MessageHandler(filters.TEXT & ~filters.COMMAND, lang_choice)],
            MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu)],
        },
        fallbacks=[]
    )

    app.add_handler(conv_handler)

    print("Bot started...")
    app.run_polling()

if __name__ == '__main__':
    main()
