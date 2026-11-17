"""
Placeholder structure for a fresh install. Nothing here is a fact about the
company: no clients, projects, figures, people or certifications. Every
publishable row is created as `pending`, so none of it reaches the live site
until a person approves it, and descriptive text starts with "Placeholder".
"""

P = "Placeholder — "
P_AR = "نص مؤقت — "

SETTINGS = {
    "tagline": "Project management services",
    "tagline_ar": "خدمات إدارة المشاريع",
    "company_name_ar": "ثري بيلارز لخدمات إدارة المشاريع",
    "short_name_ar": "ثري بيلارز",
    "hero_eyebrow": "Project Management Services",
    "hero_eyebrow_ar": "خدمات إدارة المشاريع",
    "hero_headline": "Every project, on three strong pillars",
    "hero_headline_ar": "كل مشروع على ثلاث ركائز متينة",
    "hero_subline": "Placeholder sentence — replace with the approved one-line positioning statement.",
    "hero_subline_ar": "جملة مؤقتة — تُستبدل بعبارة التعريف المعتمدة.",
    "hero_primary_label_ar": "اطلب عرضاً",
    "hero_secondary_label_ar": "مشاريعنا",
    "seo_title": "3 Pillars Project Management Services",
    "seo_title_ar": "ثري بيلارز لخدمات إدارة المشاريع",
    "cookie_notice": "We use essential cookies to run this site and, with your consent, analytics to improve it.",
    "cookie_notice_ar": "نستخدم ملفات تعريف الارتباط الضرورية لتشغيل الموقع، وبموافقتك أدوات تحليل لتحسينه.",
}

HOME_SECTIONS = [
    ("hero", "", "", "", ""),
    ("trust", "Trusted by", "موضع ثقة", "", ""),
    ("pillars", "Our foundation", "أساسنا", "The three pillars", "الركائز الثلاث"),
    ("services", "What we do", "ما نقدمه", "Services built around delivery", "خدمات مبنية حول التنفيذ"),
    ("kpis", "In numbers", "بالأرقام", "", ""),
    ("projects", "Selected work", "أعمال مختارة", "Featured projects", "مشاريع مميزة"),
    ("approach", "How we work", "كيف نعمل", "From initiation to closeout", "من البدء حتى الإغلاق"),
    ("sectors", "Where we work", "أين نعمل", "Sectors we serve", "القطاعات التي نخدمها"),
    ("testimonial", "", "", "", ""),
    ("insights", "Insights", "رؤى", "Latest thinking", "أحدث المقالات"),
    ("cta", "Start a conversation", "لنبدأ الحوار", "Have a project? Let’s talk.", "لديك مشروع؟ لنتحدث."),
]

PILLARS = [
    ("green", "Governance", "الحوكمة", "Layers", "Clear decisions, roles and controls from day one.",
     "قرارات وأدوار وضوابط واضحة منذ اليوم الأول."),
    ("blue", "Delivery", "التنفيذ", "Route", "Plans that hold under pressure, and teams that follow them.",
     "خطط تصمد تحت الضغط وفرق تلتزم بها."),
    ("grey", "Assurance", "الضمان", "ShieldCheck", "Cost, time and quality measured honestly and reported early.",
     "قياس صادق للتكلفة والوقت والجودة وإبلاغ مبكر."),
]

SECTORS = [
    ("Infrastructure", "البنية التحتية", "Route", "Roads, bridges, water and utilities.", "الطرق والجسور والمياه والمرافق."),
    ("Buildings", "المباني", "Building", "Commercial, residential and public buildings.", "المباني التجارية والسكنية والعامة."),
    ("Energy", "الطاقة", "Zap", "Power generation, transmission and renewables.", "توليد الطاقة ونقلها والطاقة المتجددة."),
    ("Industrial", "الصناعة", "Factory", "Plants, logistics hubs and industrial facilities.", "المصانع ومراكز الخدمات اللوجستية والمنشآت الصناعية."),
    ("Government", "القطاع الحكومي", "Landmark", "Public programmes and institutional projects.", "البرامج العامة والمشاريع المؤسسية."),
]

SERVICES = [
    ("Project Management Consultancy", "استشارات إدارة المشاريع", "ClipboardCheck", True,
     "End-to-end management of a project on the client’s behalf.", "إدارة متكاملة للمشروع نيابةً عن العميل."),
    ("Project Controls", "ضبط المشاريع", "ChartGantt", False,
     "Planning, scheduling and cost control that show where a project really stands.",
     "التخطيط والجدولة وضبط التكاليف لمعرفة وضع المشروع الحقيقي."),
    ("Cost Management & Quantity Surveying", "إدارة التكاليف وحساب الكميات", "Calculator", False,
     "Estimates, budgets, valuations and final accounts.", "التقديرات والموازنات والتقييمات والحسابات الختامية."),
    ("Contract Administration & Claims", "إدارة العقود والمطالبات", "Signature", False,
     "Contract strategy, administration and dispute avoidance.", "استراتيجية العقود وإدارتها وتجنب النزاعات."),
    ("Design Management", "إدارة التصميم", "PencilRuler", False,
     "Coordinating design teams so drawings arrive complete and on time.",
     "تنسيق فرق التصميم لتصل المخططات مكتملة وفي موعدها."),
    ("Construction Supervision", "الإشراف على التنفيذ", "HardHat", False,
     "On-site supervision of quality, safety and progress.", "الإشراف الميداني على الجودة والسلامة والتقدم."),
    ("PMO Setup", "تأسيس مكاتب إدارة المشاريع", "Network", False,
     "Standing up a project management office: methods, tools and people.",
     "تأسيس مكتب لإدارة المشاريع: المنهجيات والأدوات والكوادر."),
    ("Feasibility & Tender Management", "دراسات الجدوى وإدارة المناقصات", "Scale", False,
     "Testing the case for a project and running a fair, competitive tender.",
     "اختبار جدوى المشروع وإدارة مناقصة عادلة وتنافسية."),
]

PMC_STEPS = [
    ("Understand", "الفهم", "Agree objectives, constraints and success measures with the client.",
     "الاتفاق مع العميل على الأهداف والقيود ومقاييس النجاح."),
    ("Plan", "التخطيط", "Build the governance, schedule, budget and risk register.",
     "بناء الحوكمة والجدول الزمني والموازنة وسجل المخاطر."),
    ("Deliver", "التنفيذ", "Manage designers, contractors and suppliers against the plan.",
     "إدارة المصممين والمقاولين والموردين وفق الخطة."),
    ("Hand over", "التسليم", "Close out contracts, documents and lessons learned.",
     "إغلاق العقود والوثائق والدروس المستفادة."),
]

PMC_DELIVERABLES = [
    ("Project execution plan", "خطة تنفيذ المشروع"),
    ("Integrated master schedule", "الجدول الزمني الرئيسي المتكامل"),
    ("Cost plan and cash-flow forecast", "خطة التكاليف وتوقعات التدفق النقدي"),
    ("Risk and issue registers", "سجلات المخاطر والقضايا"),
    ("Monthly progress reports", "تقارير التقدم الشهرية"),
]

LIFECYCLE = [
    ("Initiation", "البدء", "Flag", "Define the business case, objectives and governance.",
     "تحديد دراسة الجدوى والأهداف والحوكمة.", "Project charter\nStakeholder register",
     "ميثاق المشروع\nسجل أصحاب المصلحة"),
    ("Planning", "التخطيط", "Map", "Turn objectives into scope, schedule, budget and a plan for risk.",
     "تحويل الأهداف إلى نطاق وجدول وموازنة وخطة للمخاطر.", "Scope baseline\nSchedule\nBudget",
     "خط أساس النطاق\nالجدول الزمني\nالموازنة"),
    ("Execution", "التنفيذ", "Hammer", "Mobilise teams and contractors and deliver the work.",
     "تعبئة الفرق والمقاولين وتنفيذ الأعمال.", "Contracts awarded\nWork packages", "ترسية العقود\nحزم العمل"),
    ("Monitoring & Control", "المتابعة والضبط", "Activity", "Measure progress against the baseline and act early.",
     "قياس التقدم مقارنةً بخط الأساس والتصرف مبكراً.", "Progress reports\nChange log", "تقارير التقدم\nسجل التغييرات"),
    ("Closeout", "الإغلاق", "FlagTriangleRight", "Hand over, settle accounts and capture lessons.",
     "التسليم وتسوية الحسابات وتوثيق الدروس.", "Handover documents\nFinal account\nLessons learned",
     "وثائق التسليم\nالحساب الختامي\nالدروس المستفادة"),
]

PAGES = [
    ("about", "About us", "من نحن", "Who we are", "من نحن"),
    ("approach", "Our approach", "منهجيتنا", "How we work", "كيف نعمل"),
    ("careers", "Careers", "الوظائف", "Join us", "انضم إلينا"),
    ("services", "Services", "الخدمات", "What we do", "ما نقدمه"),
    ("sectors", "Sectors", "القطاعات", "Where we work", "أين نعمل"),
    ("projects", "Projects", "المشاريع", "Selected work", "أعمال مختارة"),
    ("insights", "Insights", "رؤى", "Thinking", "أفكار"),
    ("contact", "Contact us", "اتصل بنا", "Get in touch", "تواصل معنا"),
    ("request-a-proposal", "Request a proposal", "اطلب عرضاً", "Work with us", "اعمل معنا"),
    ("capability-statement", "Capability statement", "ملف القدرات", "Download", "تحميل"),
    ("privacy", "Privacy notice", "إشعار الخصوصية", "Legal", "قانوني"),
    ("terms", "Terms of use", "شروط الاستخدام", "Legal", "قانوني"),
    ("cookies", "Cookie policy", "سياسة ملفات تعريف الارتباط", "Legal", "قانوني"),
]

HEADER_NAV = [
    ("Services", "الخدمات", "/services", "services"),
    ("Sectors", "القطاعات", "/sectors", "sectors"),
    ("Projects", "المشاريع", "/projects", ""),
    ("Approach", "منهجيتنا", "/approach", ""),
    ("Insights", "رؤى", "/insights", ""),
    ("About", "من نحن", "/about", ""),
    ("Careers", "الوظائف", "/careers", ""),
    ("Contact", "اتصل بنا", "/contact", ""),
]

FOOTER = [
    ("Company", "الشركة", [("About", "من نحن", "/about"), ("Approach", "منهجيتنا", "/approach"),
                           ("Careers", "الوظائف", "/careers"), ("Insights", "رؤى", "/insights")]),
    ("Work with us", "اعمل معنا", [("Request a proposal", "اطلب عرضاً", "/request-a-proposal"),
                                    ("Capability statement", "ملف القدرات", "/capability-statement"),
                                    ("Contact", "اتصل بنا", "/contact")]),
]

LEGAL = [("Privacy", "الخصوصية", "/privacy"), ("Terms", "الشروط", "/terms"), ("Cookies", "ملفات تعريف الارتباط", "/cookies")]

INSIGHT_CATEGORIES = [("News", "أخبار", "news"), ("Articles", "مقالات", "articles")]
