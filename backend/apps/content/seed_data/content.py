"""
The website content, transcribed from docs/content/3pillars-content.md.

English is copied verbatim from the document; `manage.py check_copy` fails if
any English string here stops matching it. Arabic is a draft translation that
follows docs/content/glossary-en-ar.md and is seeded with ar_reviewed = False.

Fields the document does not provide are left empty rather than written here.
"""

POSITIONING = (
    "3 Pillars helps public and private sector clients manage complex projects and develop business opportunities "
    "across the built environment, infrastructure, urban development, and research-led sectors."
)
POSITIONING_AR = (
    "تساعد ثري بيلارز عملاء القطاعين العام والخاص على إدارة المشاريع المعقدة وتطوير فرص الأعمال في قطاعات البيئة "
    "العمرانية والبنية التحتية والتنمية العمرانية والقطاعات القائمة على البحث."
)

CONSULTATION = "/contact/request-a-consultation/"

# ── Site settings (home hero and home SEO) ───────────────────────────────

SITE = {
    "tagline": POSITIONING,
    "tagline_ar": POSITIONING_AR,
    "home_h1": "Project Management and Business Development for Complex Projects",
    "home_h1_ar": "إدارة المشاريع وتطوير الأعمال للمشاريع المعقدة",
    "hero_headline": "Turning Projects into Progress. Turning Opportunities into Growth.",
    "hero_headline_ar": "نحوّل المشاريع إلى تقدّم، والفرص إلى نمو.",
    "hero_primary_label": "Explore Our Services",
    "hero_primary_label_ar": "اكتشف خدماتنا",
    "hero_primary_link": "/services/",
    "hero_secondary_label": "Discuss Your Project",
    "hero_secondary_label_ar": "ناقش مشروعك معنا",
    "hero_secondary_link": CONSULTATION,
    "home_seo_title": "3 Pillars | Project Management & Business Development",
    "home_seo_title_ar": "ثري بيلارز | إدارة المشاريع وتطوير الأعمال",
    "home_meta_description": (
        "3 Pillars supports project delivery and business growth through project management, business development, "
        "and strategic insight across infrastructure and the built environment."
    ),
    "home_meta_description_ar": (
        "تدعم ثري بيلارز تنفيذ المشاريع ونمو الأعمال من خلال إدارة المشاريع وتطوير الأعمال والرؤية الاستراتيجية في "
        "البنية التحتية والبيئة العمرانية."
    ),
    "home_primary_keyword": "project management and business development",
    "home_supporting_keywords": (
        "programme management, project controls, infrastructure project management, business development consulting, "
        "market entry strategy"
    ),
}

#: Cleared on purpose. The SEO defaults give way to the positioning statement. The hero keeps
#: only its heading, headline and buttons (decision 26 Nov 2026: brief hero text); the document's
#: eyebrow and supporting copy stay editable in Site settings → Hero, and the supporting copy's
#: message is carried by the introduction section directly below.
SITE_CLEARED = ("seo_title", "seo_title_ar", "seo_description", "seo_description_ar",
                "hero_eyebrow", "hero_eyebrow_ar", "hero_subline", "hero_subline_ar")

# ── Home sections, in page order ─────────────────────────────────────────

HOME_SECTIONS = [
    {"kind": "hero"},
    {
        "kind": "intro",
        "title": "A focused approach to project delivery and business growth",
        "title_ar": "نهج مركّز لتنفيذ المشاريع ونمو الأعمال",
        "intro": (
            "Successful projects require more than technical expertise. They need clear governance, realistic plans, "
            "disciplined cost and schedule control, effective stakeholder coordination, and the ability to recognise "
            "opportunities as markets evolve. 3 Pillars brings these disciplines together to help clients move from "
            "ambition to informed action."
        ),
        "intro_ar": (
            "لا يكفي التميز الفني وحده لنجاح المشاريع؛ فهي تحتاج إلى حوكمة واضحة، وخطط واقعية، وضبط منضبط للتكاليف "
            "والجداول الزمنية، وتنسيق فعّال مع أصحاب المصلحة، وقدرة على اقتناص الفرص مع تطور الأسواق. وتجمع ثري "
            "بيلارز هذه التخصصات معاً لتساعد عملاءها على الانتقال من الطموح إلى العمل المدروس."
        ),
    },
    {"kind": "pillars", "title": "Services overview", "title_ar": "نظرة عامة على الخدمات"},
    {
        "kind": "sectors",
        "intro": "Our work is relevant across the sectors that shape cities, economies, and essential services:",
        "intro_ar": "يمتد عملنا إلى القطاعات التي تشكّل المدن والاقتصادات والخدمات الأساسية:",
    },
    {"kind": "value", "title": "How we create value", "title_ar": "كيف نصنع القيمة"},
    {
        "kind": "cta",
        "title": "Let’s move your next project or opportunity forward.",
        "title_ar": "لنمضِ معاً بمشروعك أو فرصتك القادمة إلى الأمام.",
        "intro": (
            "Whether you are planning a major project, strengthening delivery oversight, entering a new market, or "
            "assessing a strategic opportunity, 3 Pillars is ready to start the conversation."
        ),
        "intro_ar": (
            "سواء كنت تخطط لمشروع كبير، أو تعزز الإشراف على التنفيذ، أو تدخل سوقاً جديدة، أو تقيّم فرصة استراتيجية، "
            "فإن ثري بيلارز مستعدة لبدء الحوار."
        ),
        "cta_label": "Contact 3 Pillars",
        "cta_label_ar": "تواصل مع ثري بيلارز",
        "cta_link": "/contact/",
    },
    {"kind": "trust", "visible": False},
    {"kind": "kpis", "visible": False},
    {"kind": "projects", "visible": False},
    {"kind": "testimonial", "visible": False},
    {"kind": "insights", "visible": False},
]

VALUE_POINTS = [
    {"title": "Clarity", "title_ar": "الوضوح",
     "body": "We clarify objectives, priorities, opportunities, and routes to action.",
     "body_ar": "نوضّح الأهداف والأولويات والفرص ومسارات العمل."},
    {"title": "Control", "title_ar": "الضبط",
     "body": "We strengthen governance, programme visibility, coordination, and performance oversight.",
     "body_ar": "نعزز الحوكمة ووضوح الرؤية على البرامج والتنسيق والإشراف على الأداء."},
    {"title": "Growth", "title_ar": "النمو",
     "body": "We connect market insight, strategic relationships, and business development activity.",
     "body_ar": "نربط بين المعلومات السوقية والعلاقات الاستراتيجية وأنشطة تطوير الأعمال."},
]

# ── The three pillars ────────────────────────────────────────────────────

PILLARS = [
    {
        "number": 1, "color": "green", "role_on_site": "lead", "is_proposed": False,
        "service": "project-programme-management",
        "name": "Project & Programme Management",
        "name_ar": "إدارة المشاريع والبرامج",
        "core_value": "Plans, governs, monitors, and coordinates projects to support controlled delivery.",
        "core_value_ar": "تخطيط المشاريع وحوكمتها ومتابعتها وتنسيقها لدعم تنفيذ منضبط.",
        "summary": (
            "We support project owners and organisations with structured planning, governance, controls, risk "
            "oversight, reporting, and coordination throughout the project lifecycle. Our focus is to improve "
            "visibility, strengthen decision-making, and keep delivery aligned with agreed objectives."
        ),
        "summary_ar": (
            "ندعم ملّاك المشاريع والمؤسسات بالتخطيط المنظم والحوكمة والضبط والإشراف على المخاطر وإعداد التقارير "
            "والتنسيق على امتداد دورة حياة المشروع. ونركز على تحسين وضوح الرؤية، وتعزيز اتخاذ القرار، والحفاظ على "
            "توافق التنفيذ مع الأهداف المتفق عليها."
        ),
        "detail": (
            "We help clients establish the structures, plans, controls, and coordination required to manage projects "
            "and programmes with greater confidence. This pillar focuses on scope, schedule, cost, risk, governance, "
            "reporting, and stakeholder alignment."
        ),
        "detail_ar": (
            "نساعد عملاءنا على إرساء الهياكل والخطط والضوابط والتنسيق اللازمة لإدارة المشاريع والبرامج بثقة أكبر. "
            "وتركز هذه الركيزة على النطاق والجدول الزمني والتكلفة والمخاطر والحوكمة وإعداد التقارير وتوافق أصحاب "
            "المصلحة."
        ),
        "core_outcomes": (
            "Clear accountability, improved project visibility, coordinated delivery, early issue identification, and "
            "better-informed management decisions."
        ),
        "core_outcomes_ar": (
            "مساءلة واضحة، ورؤية أوضح للمشروع، وتنفيذ منسّق، واكتشاف مبكر للمشكلات، وقرارات إدارية أكثر استنارة."
        ),
        "covers": (
            "Project planning, programme coordination, governance, PMO support, project controls, cost and schedule "
            "monitoring, risk and change management, reporting, and closeout."
        ),
        "covers_ar": (
            "تخطيط المشاريع، وتنسيق البرامج، والحوكمة، ودعم مكتب إدارة المشاريع، وضبط المشاريع، ومتابعة التكاليف "
            "والجداول الزمنية، وإدارة المخاطر والتغيير، وإعداد التقارير، وإغلاق المشروع."
        ),
    },
    {
        "number": 2, "color": "blue", "role_on_site": "lead", "is_proposed": False,
        "service": "business-development",
        "name": "Business Development & Market Expansion",
        "name_ar": "تطوير الأعمال والتوسع في الأسواق",
        "core_value": "Identifies opportunities, supports market entry, builds partnerships, and strengthens bids.",
        "core_value_ar": "تحديد الفرص، ودعم دخول الأسواق، وبناء الشراكات، وتعزيز العطاءات.",
        "summary": (
            "We help organisations understand markets, assess opportunities, develop strategic relationships, prepare "
            "for tenders, and build a structured route to sustainable growth. Our approach connects market "
            "intelligence with practical commercial action."
        ),
        "summary_ar": (
            "نساعد المؤسسات على فهم الأسواق، وتقييم الفرص، وتطوير العلاقات الاستراتيجية، والاستعداد للمناقصات، وبناء "
            "مسار منظم نحو نمو مستدام. ويربط نهجنا بين المعلومات السوقية والعمل التجاري العملي."
        ),
        "detail": (
            "We help organisations identify where to compete and how to pursue the right opportunities. This pillar "
            "connects market research with opportunity screening, positioning, partner development, tender strategy, "
            "and market entry planning."
        ),
        "detail_ar": (
            "نساعد المؤسسات على تحديد أين تنافس وكيف تسعى إلى الفرص المناسبة. وتربط هذه الركيزة أبحاث السوق بفرز "
            "الفرص، والتموضع، وتطوير الشركاء، واستراتيجية المناقصات، والتخطيط لدخول الأسواق."
        ),
        "core_outcomes": (
            "A clearer view of target markets, qualified opportunities, stronger commercial positioning, and more "
            "structured business development activity."
        ),
        "core_outcomes_ar": (
            "رؤية أوضح للأسواق المستهدفة، وفرص مؤهلة، وتموضع تجاري أقوى، وأنشطة تطوير أعمال أكثر تنظيماً."
        ),
        "covers": (
            "Market research, opportunity identification, market entry, growth strategy, partnerships, tender and "
            "proposal support, and commercial positioning."
        ),
        "covers_ar": (
            "أبحاث السوق، وتحديد الفرص، ودخول الأسواق، واستراتيجية النمو، والشراكات، ودعم المناقصات والعروض، "
            "والتموضع التجاري."
        ),
    },
    {
        "number": 3, "color": "grey", "role_on_site": "enabling", "is_proposed": True,
        "service": "strategic-advisory-market-intelligence",
        "name": "Strategic Advisory & Market Intelligence",
        "name_ar": "الاستشارات الاستراتيجية والمعلومات السوقية",
        "core_value": "Turns market, sector, and project intelligence into better-informed decisions.",
        "core_value_ar": "تحويل المعلومات السوقية والقطاعية ومعلومات المشاريع إلى قرارات أكثر استنارة.",
        "summary": (
            "We bring together sector research, market assessment, opportunity analysis, and strategic "
            "recommendations to help clients evaluate where to compete, how to position, and which opportunities "
            "merit further attention."
        ),
        "summary_ar": (
            "نجمع بين البحوث القطاعية وتقييم الأسواق وتحليل الفرص والتوصيات الاستراتيجية لمساعدة عملائنا على تقييم "
            "أين ينافسون، وكيف يتموضعون، وأي الفرص تستحق مزيداً من الاهتمام."
        ),
        "detail": (
            "We provide the research and analytical layer that supports both project decisions and business growth. "
            "This includes country and sector assessments, demand and competitor analysis, opportunity evaluation, "
            "feasibility inputs, and strategic recommendations, subject to the company’s approved scope and "
            "capabilities."
        ),
        "detail_ar": (
            "نقدم الطبقة البحثية والتحليلية التي تدعم قرارات المشاريع ونمو الأعمال على حد سواء. ويشمل ذلك تقييمات "
            "الدول والقطاعات، وتحليل الطلب والمنافسين، وتقييم الفرص، ومدخلات دراسات الجدوى، والتوصيات الاستراتيجية، "
            "وذلك في حدود النطاق والقدرات المعتمدة للشركة."
        ),
        "core_outcomes": (
            "Evidence-led priorities, improved understanding of market conditions, and more disciplined decisions on "
            "projects and growth opportunities."
        ),
        "core_outcomes_ar": (
            "أولويات قائمة على الأدلة، وفهم أعمق لظروف السوق، وقرارات أكثر انضباطاً بشأن المشاريع وفرص النمو."
        ),
        "covers": (
            "Country and sector studies, market and competitor analysis, opportunity assessment, feasibility inputs, "
            "and strategic recommendations."
        ),
        "covers_ar": (
            "دراسات الدول والقطاعات، وتحليل الأسواق والمنافسين، وتقييم الفرص، ومدخلات دراسات الجدوى، والتوصيات "
            "الاستراتيجية."
        ),
        "note": (
            "This third pillar is a proposed positioning framework, not a confirmed statement of the company’s "
            "approved service portfolio. Management should validate it before publication.\n\n"
            "(Confirm approved scope.)"
        ),
    },
]

# ── Services ─────────────────────────────────────────────────────────────

SERVICES = [
    {
        "slug": "project-programme-management", "pillar": 1, "icon": "ClipboardList",
        "name": "Project & Programme Management",
        "name_ar": "إدارة المشاريع والبرامج",
        "seo_title": "Project & Programme Management | 3 Pillars",
        "seo_title_ar": "إدارة المشاريع والبرامج | ثري بيلارز",
        "meta_description": (
            "3 Pillars supports project owners with project and programme planning, governance, coordination, "
            "performance controls, risk oversight, and delivery reporting."
        ),
        "meta_description_ar": (
            "تدعم ثري بيلارز ملّاك المشاريع في تخطيط المشاريع والبرامج وحوكمتها وتنسيقها وضبط أدائها والإشراف على "
            "مخاطرها وإعداد تقارير تنفيذها."
        ),
        "h1": "Project & Programme Management",
        "h1_ar": "إدارة المشاريع والبرامج",
        "primary_keyword": "project and programme management",
        "supporting_keywords": (
            "construction project management, infrastructure project management, programme governance, project "
            "delivery management"
        ),
        "intro": [
            "Complex projects require a clear management structure, realistic plans, reliable information, and timely "
            "decisions. 3 Pillars supports clients in establishing and maintaining the management disciplines needed "
            "to coordinate people, activities, budgets, schedules, risks, and stakeholders across the project "
            "lifecycle.",
            "Our approach is tailored to the project environment and the client’s governance model. We focus on "
            "visibility, accountability, and early action so that project leaders can understand performance and "
            "respond to issues before they escalate.",
        ],
        "intro_ar": [
            "تتطلب المشاريع المعقدة هيكلاً إدارياً واضحاً، وخططاً واقعية، ومعلومات موثوقة، وقرارات في وقتها. وتدعم "
            "ثري بيلارز عملاءها في إرساء الانضباط الإداري والحفاظ عليه لتنسيق الأفراد والأنشطة والموازنات والجداول "
            "الزمنية والمخاطر وأصحاب المصلحة على امتداد دورة حياة المشروع.",
            "ونكيّف نهجنا وفق بيئة المشروع ونموذج الحوكمة لدى العميل. ونركز على وضوح الرؤية والمساءلة والتحرك المبكر "
            "لكي يتمكن قادة المشاريع من فهم الأداء ومعالجة المشكلات قبل تفاقمها.",
        ],
        "capabilities_title": "Our project management capabilities",
        "capabilities_title_ar": "قدراتنا في إدارة المشاريع",
        "capabilities": [
            ("Project Initiation & Planning", "بدء المشروع وتخطيطه",
             "Clarifying objectives, scope, deliverables, assumptions, interfaces, responsibilities, and delivery "
             "priorities.",
             "توضيح الأهداف والنطاق والمخرجات والافتراضات والواجهات البينية والمسؤوليات وأولويات التنفيذ."),
            ("Programme & Project Governance", "حوكمة البرامج والمشاريع",
             "Defining governance structures, decision rights, reporting lines, review cycles, and escalation routes.",
             "تحديد هياكل الحوكمة وصلاحيات القرار وخطوط التقارير ودورات المراجعة ومسارات التصعيد."),
            ("Project Planning & Scheduling", "تخطيط المشاريع وجدولتها",
             "Developing and reviewing integrated schedules, milestones, dependencies, critical activities, and "
             "progress updates.",
             "إعداد الجداول الزمنية المتكاملة ومراجعتها، والمراحل الرئيسية، والترابطات، والأنشطة الحرجة، وتحديثات "
             "التقدم."),
            ("Project Controls & Performance Monitoring", "ضبط المشاريع ومتابعة الأداء",
             "Establishing practical controls for scope, schedule, cost, progress, risks, changes, and performance "
             "reporting.",
             "إرساء ضوابط عملية للنطاق والجدول الزمني والتكلفة والتقدم والمخاطر والتغييرات وتقارير الأداء."),
            ("Cost & Commercial Monitoring", "متابعة التكاليف والجوانب التجارية",
             "Supporting budget baselines, cost tracking, forecast reviews, commitments, and commercial visibility.",
             "دعم خطوط الأساس للموازنة، وتتبع التكاليف، ومراجعة التوقعات، والالتزامات، ووضوح الرؤية التجارية."),
            ("Risk & Change Management", "إدارة المخاطر والتغيير",
             "Identifying, assessing, assigning, monitoring, and reporting risks, issues, assumptions, and change "
             "requests.",
             "تحديد المخاطر والمشكلات والافتراضات وطلبات التغيير وتقييمها وإسنادها ومتابعتها والإبلاغ عنها."),
            ("Stakeholder & Interface Coordination", "التنسيق مع أصحاب المصلحة والواجهات البينية",
             "Supporting communication, coordination, action tracking, and management of interfaces across project "
             "parties.",
             "دعم التواصل والتنسيق وتتبع الإجراءات وإدارة الواجهات البينية بين أطراف المشروع."),
            ("Reporting & Management Dashboards", "التقارير ولوحات المتابعة الإدارية",
             "Providing structured reports and dashboards that help project leaders understand status, trends, "
             "decisions, and required actions.",
             "تقديم تقارير منظمة ولوحات متابعة تساعد قادة المشاريع على فهم الوضع والاتجاهات والقرارات والإجراءات "
             "المطلوبة."),
            ("Project Closeout & Handover", "إغلاق المشروع وتسليمه",
             "Coordinating completion requirements, documentation, outstanding actions, lessons learned, and handover "
             "planning.",
             "تنسيق متطلبات الإنجاز والتوثيق والإجراءات المتبقية والدروس المستفادة وتخطيط التسليم."),
        ],
        "who_we_support": (
            "Project owners, developers, public sector entities, investors, programme sponsors, engineering and "
            "construction organisations, and delivery partners seeking structured management support."
        ),
        "who_we_support_ar": (
            "ملّاك المشاريع، والمطورون، وجهات القطاع العام، والمستثمرون، ورعاة البرامج، ومؤسسات الهندسة والإنشاءات، "
            "وشركاء التنفيذ الباحثون عن دعم إداري منظم."
        ),
        "cta_headline": "Bring greater control and clarity to your project.",
        "cta_headline_ar": "امنح مشروعك مزيداً من الضبط والوضوح.",
        "cta_label": "Discuss Project Management Support",
        "cta_label_ar": "ناقش دعم إدارة المشاريع",
    },
    {
        "slug": "pmo-project-controls", "pillar": 1, "icon": "ChartGantt",
        "name": "PMO & Project Controls",
        "name_ar": "مكتب إدارة المشاريع وضبط المشاريع",
        "seo_title": "PMO & Project Controls Services | 3 Pillars",
        "seo_title_ar": "خدمات مكتب إدارة المشاريع وضبط المشاريع | ثري بيلارز",
        "meta_description": (
            "Build stronger project governance with PMO setup, project controls, schedule and cost monitoring, "
            "performance reporting, and management dashboards."
        ),
        "meta_description_ar": (
            "عزّز حوكمة مشاريعك بتأسيس مكتب إدارة المشاريع، وضبط المشاريع، ومتابعة الجداول الزمنية والتكاليف، "
            "وتقارير الأداء، ولوحات المتابعة الإدارية."
        ),
        "h1": "PMO & Project Controls",
        "h1_ar": "مكتب إدارة المشاريع وضبط المشاريع",
        "primary_keyword": "PMO and project controls services",
        "supporting_keywords": (
            "project management office, project controls consultancy, project reporting, schedule control, cost control"
        ),
        "intro": [
            "A Project Management Office (PMO) gives organisations a consistent way to govern projects, monitor "
            "performance, manage information, and support decisions. 3 Pillars can help establish or strengthen PMO "
            "processes that reflect the scale, complexity, and reporting needs of each organisation.",
        ],
        "intro_ar": [
            "يمنح مكتب إدارة المشاريع (PMO) المؤسسات طريقة متسقة لحوكمة المشاريع ومتابعة الأداء وإدارة المعلومات "
            "ودعم القرارات. ويمكن لثري بيلارز المساعدة في تأسيس إجراءات مكتب إدارة المشاريع أو تعزيزها بما يتناسب مع "
            "حجم كل مؤسسة ودرجة تعقيدها واحتياجاتها من التقارير.",
        ],
        "bullets_title": "What we can support",
        "bullets_title_ar": "ما يمكننا دعمه",
        "bullets": [
            ("PMO design, mobilisation, and operating procedures",
             "تصميم مكتب إدارة المشاريع وتفعيله وإجراءات تشغيله"),
            ("Project governance frameworks, roles, and accountability matrices",
             "أطر حوكمة المشاريع والأدوار ومصفوفات المساءلة"),
            ("Integrated master schedules and milestone tracking",
             "الجداول الزمنية الرئيسية المتكاملة وتتبع المراحل الرئيسية"),
            ("Cost, budget, commitments, and forecast monitoring",
             "متابعة التكاليف والموازنات والالتزامات والتوقعات"),
            ("Progress measurement and performance indicators", "قياس التقدم ومؤشرات الأداء"),
            ("Risk, issue, change, and decision registers", "سجلات المخاطر والمشكلات والتغييرات والقرارات"),
            ("Executive dashboards and periodic project reports",
             "لوحات المتابعة التنفيذية والتقارير الدورية للمشاريع"),
            ("Portfolio-level visibility and project prioritisation support",
             "وضوح الرؤية على مستوى المحفظة ودعم ترتيب أولويات المشاريع"),
            ("Process reviews and continuous improvement", "مراجعة الإجراءات والتحسين المستمر"),
        ],
        "context_title": "Why a structured PMO matters",
        "context_title_ar": "لماذا يهم مكتب إدارة مشاريع منظم",
        "context_body": (
            "A well-designed PMO helps management see where projects stand, compare performance consistently, "
            "identify issues earlier, and direct attention to the decisions that matter. The objective is not to add "
            "administration; it is to make project information useful, timely, and actionable."
        ),
        "context_body_ar": (
            "يساعد مكتب إدارة المشاريع المصمم جيداً الإدارةَ على معرفة موقف المشاريع، ومقارنة الأداء بصورة متسقة، "
            "واكتشاف المشكلات مبكراً، وتوجيه الاهتمام إلى القرارات المهمة. والهدف ليس إضافة أعباء إدارية، بل جعل "
            "معلومات المشاريع مفيدة وفي وقتها وقابلة للتنفيذ."
        ),
        "cta_label": "Strengthen Your Project Controls",
        "cta_label_ar": "عزّز ضبط مشاريعك",
    },
    {
        "slug": "business-development", "pillar": 2, "icon": "TrendingUp",
        "name": "Business Development & Market Expansion",
        "name_ar": "تطوير الأعمال والتوسع في الأسواق",
        "seo_title": "Business Development & Market Expansion | 3 Pillars",
        "seo_title_ar": "تطوير الأعمال والتوسع في الأسواق | ثري بيلارز",
        "meta_description": (
            "3 Pillars helps organisations assess markets, identify opportunities, build strategic partnerships, "
            "develop market entry plans, and strengthen tender positioning."
        ),
        "meta_description_ar": (
            "تساعد ثري بيلارز المؤسسات على تقييم الأسواق وتحديد الفرص وبناء الشراكات الاستراتيجية ووضع خطط دخول "
            "الأسواق وتعزيز تموضعها في المناقصات."
        ),
        "h1": "Business Development & Market Expansion",
        "h1_ar": "تطوير الأعمال والتوسع في الأسواق",
        "primary_keyword": "business development consulting",
        "supporting_keywords": (
            "business growth strategy, market expansion strategy, opportunity identification, market entry consulting, "
            "strategic partnerships"
        ),
        "intro": [
            "Sustainable growth requires more than finding new leads. It requires a clear understanding of markets, a "
            "disciplined approach to opportunity selection, strong relationships, and the ability to translate "
            "strategic priorities into commercial action. 3 Pillars supports organisations seeking to expand their "
            "presence, develop partnerships, and pursue opportunities across infrastructure, the built environment, "
            "urban development, and related sectors.",
        ],
        "intro_ar": [
            "لا يتحقق النمو المستدام بمجرد إيجاد عملاء محتملين جدد؛ بل يتطلب فهماً واضحاً للأسواق، ونهجاً منضبطاً في "
            "اختيار الفرص، وعلاقات قوية، وقدرة على ترجمة الأولويات الاستراتيجية إلى عمل تجاري. وتدعم ثري بيلارز "
            "المؤسسات الساعية إلى توسيع حضورها وتطوير شراكاتها والسعي إلى الفرص في البنية التحتية والبيئة العمرانية "
            "والتنمية العمرانية والقطاعات المرتبطة بها.",
        ],
        "capabilities_title": "Our business development capabilities",
        "capabilities_title_ar": "قدراتنا في تطوير الأعمال",
        "capabilities": [
            ("Market Research & Intelligence", "أبحاث السوق والمعلومات السوقية",
             "Assessing country and sector conditions, market demand, competitor activity, procurement environments, "
             "and potential clients.",
             "تقييم أوضاع الدول والقطاعات، والطلب في السوق، ونشاط المنافسين، وبيئات المشتريات، والعملاء المحتملين."),
            ("Opportunity Identification & Screening", "تحديد الفرص وفرزها",
             "Identifying relevant projects and business opportunities, then assessing strategic fit, scale, timing, "
             "requirements, and pursuit priorities.",
             "تحديد المشاريع وفرص الأعمال ذات الصلة، ثم تقييم ملاءمتها الاستراتيجية وحجمها وتوقيتها ومتطلباتها "
             "وأولويات السعي إليها."),
            ("Market Entry & Expansion Strategy", "استراتيجية دخول الأسواق والتوسع",
             "Supporting the assessment of target markets, entry options, local requirements, partner needs, and "
             "practical market development roadmaps.",
             "دعم تقييم الأسواق المستهدفة، وخيارات الدخول، والمتطلبات المحلية، واحتياجات الشركاء، وخرائط طريق عملية "
             "لتطوير الأسواق."),
            ("Business Growth Strategy", "استراتيجية نمو الأعمال",
             "Helping define target segments, priority services, commercial objectives, positioning, and measurable "
             "business development plans.",
             "المساعدة في تحديد الشرائح المستهدفة، والخدمات ذات الأولوية، والأهداف التجارية، والتموضع، وخطط تطوير "
             "أعمال قابلة للقياس."),
            ("Strategic Partnerships & Consortium Development", "الشراكات الاستراتيجية وتكوين الائتلافات",
             "Supporting the identification and assessment of potential partners, consortium structures, and "
             "collaboration opportunities.",
             "دعم تحديد الشركاء المحتملين وتقييمهم، وهياكل الائتلافات، وفرص التعاون."),
            ("Tender & Proposal Strategy", "استراتيجية المناقصات والعروض",
             "Supporting bid/no-bid assessments, opportunity reviews, tender planning, compliance coordination, "
             "proposal positioning, and submission readiness.",
             "دعم تقييم قرار المشاركة في المناقصة، ومراجعة الفرص، وتخطيط المناقصات، وتنسيق الامتثال، وتموضع العروض، "
             "والجاهزية للتقديم."),
            ("Client & Stakeholder Engagement", "التواصل مع العملاء وأصحاب المصلحة",
             "Mapping relevant stakeholders and supporting structured engagement plans aligned with the "
             "organisation’s commercial priorities.",
             "تحديد أصحاب المصلحة المعنيين ودعم خطط تواصل منظمة تتوافق مع الأولويات التجارية للمؤسسة."),
            ("Business Development Planning & Reporting", "تخطيط تطوير الأعمال وإعداد تقاريره",
             "Establishing opportunity registers, pursuit stages, action plans, review routines, and management "
             "reporting.",
             "إعداد سجلات الفرص، ومراحل السعي إليها، وخطط العمل، ودورات المراجعة، والتقارير الإدارية."),
        ],
        "steps_title": "Our business development process",
        "steps_title_ar": "منهجيتنا في تطوير الأعمال",
        "steps": [
            ("Understand the organisation’s capabilities, objectives, and target sectors.",
             "فهم قدرات المؤسسة وأهدافها والقطاعات التي تستهدفها."),
            ("Assess markets and identify relevant opportunities.", "تقييم الأسواق وتحديد الفرص ذات الصلة."),
            ("Prioritise opportunities against strategic fit, capability, risk, and resources.",
             "ترتيب أولويات الفرص وفق الملاءمة الاستراتيجية والقدرات والمخاطر والموارد."),
            ("Define the pursuit approach, partners, stakeholders, and required actions.",
             "تحديد نهج السعي إلى الفرصة والشركاء وأصحاب المصلحة والإجراءات المطلوبة."),
            ("Track progress, review outcomes, and refine the market development plan.",
             "متابعة التقدم ومراجعة النتائج وتحسين خطة تطوير السوق."),
        ],
        "cta_headline": "Build a more focused path to your next market opportunity.",
        "cta_headline_ar": "ابنِ مساراً أكثر تركيزاً نحو فرصتك السوقية القادمة.",
        "cta_label": "Discuss Business Development",
        "cta_label_ar": "ناقش تطوير الأعمال",
    },
    {
        "slug": "strategic-advisory-market-intelligence", "pillar": 3, "icon": "ChartColumn",
        "name": "Strategic Advisory & Market Intelligence",
        "name_ar": "الاستشارات الاستراتيجية والمعلومات السوقية",
        "seo_title": "Strategic Advisory & Market Intelligence | 3 Pillars",
        "seo_title_ar": "الاستشارات الاستراتيجية والمعلومات السوقية | ثري بيلارز",
        "meta_description": (
            "Make informed project and growth decisions through market intelligence, sector research, opportunity "
            "assessment, and practical strategic recommendations."
        ),
        "meta_description_ar": (
            "اتخذ قرارات مدروسة بشأن المشاريع والنمو من خلال المعلومات السوقية والبحوث القطاعية وتقييم الفرص "
            "والتوصيات الاستراتيجية العملية."
        ),
        "h1": "Strategic Advisory & Market Intelligence",
        "h1_ar": "الاستشارات الاستراتيجية والمعلومات السوقية",
        "primary_keyword": "strategic advisory and market intelligence",
        "supporting_keywords": (
            "market intelligence services, sector research, country market study, opportunity assessment, feasibility "
            "study support"
        ),
        "intro": [
            "Sound decisions depend on a clear understanding of the environment in which an organisation operates. "
            "3 Pillars brings together structured research and practical analysis to help clients assess markets, "
            "understand sector dynamics, evaluate opportunities, and make informed choices about projects and growth "
            "priorities.",
        ],
        "intro_ar": [
            "تعتمد القرارات السليمة على فهم واضح للبيئة التي تعمل فيها المؤسسة. وتجمع ثري بيلارز بين البحث المنظم "
            "والتحليل العملي لمساعدة عملائها على تقييم الأسواق، وفهم ديناميكيات القطاعات، وتقييم الفرص، واتخاذ "
            "خيارات مدروسة بشأن المشاريع وأولويات النمو.",
        ],
        "bullets_title": "Potential areas of support",
        "bullets_title_ar": "مجالات الدعم المحتملة",
        "bullets": [
            ("Country and sector market assessments", "تقييمات أسواق الدول والقطاعات"),
            ("Market size, demand, and trend analysis", "تحليل حجم السوق والطلب والاتجاهات"),
            ("Competitor and stakeholder mapping", "رسم خرائط المنافسين وأصحاب المصلحة"),
            ("Opportunity screening and prioritisation", "فرز الفرص وترتيب أولوياتها"),
            ("Commercial and strategic risk assessment", "تقييم المخاطر التجارية والاستراتيجية"),
            ("Initial feasibility and investment screening inputs", "مدخلات أولية لدراسات الجدوى وفرز الاستثمارات"),
            ("Market entry options and development scenarios", "خيارات دخول الأسواق وسيناريوهات التطوير"),
            ("Management briefings and decision-support reports", "إحاطات للإدارة وتقارير لدعم القرار"),
        ],
        "scope_caveat": (
            "The precise scope of research, feasibility, environmental, socio-economic, technical, or financial "
            "studies must be aligned with 3 Pillars’ approved capabilities and the specialist resources engaged for "
            "each assignment."
        ),
        "scope_caveat_ar": (
            "يجب أن يتوافق النطاق الدقيق للدراسات البحثية أو دراسات الجدوى أو الدراسات البيئية أو الاجتماعية "
            "والاقتصادية أو الفنية أو المالية مع القدرات المعتمدة لثري بيلارز والموارد المتخصصة المكلّفة بكل مهمة."
        ),
        "positioning_note": (
            "Present this page as the analytical support behind the two core service lines. Avoid promising "
            "specialist technical studies, certification, or regulated advisory unless those services are confirmed "
            "and appropriately resourced."
        ),
    },
]

# ── Sectors ──────────────────────────────────────────────────────────────

SECTORS = [
    {
        "slug": "built-environment", "icon": "Building2",
        "name": "Built Environment",
        "name_ar": "البيئة العمرانية",
        "focus_summary": (
            "Project and programme management, development coordination, project controls, commercial planning, and "
            "opportunity development for building-related projects."
        ),
        "focus_summary_ar": (
            "إدارة المشاريع والبرامج، وتنسيق التطوير، وضبط المشاريع، والتخطيط التجاري، وتطوير الفرص للمشاريع "
            "المرتبطة بالمباني."
        ),
        "seo_title": "Built Environment Project Management | 3 Pillars",
        "seo_title_ar": "إدارة مشاريع البيئة العمرانية | ثري بيلارز",
        "meta_description": (
            "3 Pillars supports building and built environment projects through project management, programme "
            "coordination, project controls, and business development."
        ),
        "meta_description_ar": (
            "تدعم ثري بيلارز مشاريع المباني والبيئة العمرانية من خلال إدارة المشاريع وتنسيق البرامج وضبط المشاريع "
            "وتطوير الأعمال."
        ),
        "h1": "Project Management for the Built Environment",
        "h1_ar": "إدارة المشاريع في البيئة العمرانية",
        "primary_keyword": "built environment project management",
        "supporting_keywords": (
            "building project management, real estate development management, construction programme management, "
            "project controls"
        ),
        "intro": [
            "The built environment brings together buildings, public spaces, assets, and the systems that support the "
            "way people live and work. Delivering successful built environment projects requires clear objectives, "
            "coordinated teams, effective controls, and a strong understanding of commercial and stakeholder "
            "requirements.",
            "3 Pillars supports clients involved in built environment projects with project and programme management, "
            "PMO support, cost and schedule monitoring, risk and change coordination, and business development "
            "services. We help organisations strengthen oversight and pursue opportunities across the building and "
            "development landscape.",
        ],
        "intro_ar": [
            "تجمع البيئة العمرانية بين المباني والفضاءات العامة والأصول والأنظمة التي تدعم طريقة عيش الناس وعملهم. "
            "ويتطلب نجاح مشاريع البيئة العمرانية أهدافاً واضحة، وفرقاً منسقة، وضوابط فعّالة، وفهماً عميقاً للمتطلبات "
            "التجارية ومتطلبات أصحاب المصلحة.",
            "وتدعم ثري بيلارز عملاءها العاملين في مشاريع البيئة العمرانية بإدارة المشاريع والبرامج، ودعم مكتب إدارة "
            "المشاريع، ومتابعة التكاليف والجداول الزمنية، وتنسيق المخاطر والتغيير، وخدمات تطوير الأعمال. ونساعد "
            "المؤسسات على تعزيز الإشراف والسعي إلى الفرص في مجال المباني والتطوير.",
        ],
        "list_title": "Areas of focus",
        "list_title_ar": "مجالات التركيز",
        "list_items": [
            ("Residential, commercial, and mixed-use developments", "المشاريع السكنية والتجارية ومتعددة الاستخدامات"),
            ("Public and institutional buildings", "المباني العامة والمؤسسية"),
            ("Industrial and specialised facilities", "المنشآت الصناعية والمتخصصة"),
            ("Development programmes and multi-site initiatives", "برامج التطوير والمبادرات متعددة المواقع"),
            ("Project governance, controls, and stakeholder coordination",
             "حوكمة المشاريع وضبطها والتنسيق مع أصحاب المصلحة"),
        ],
        "related_services": [
            "project-programme-management", "pmo-project-controls", "business-development",
            "strategic-advisory-market-intelligence",
        ],
    },
    {
        "slug": "infrastructure", "icon": "Route",
        "name": "Infrastructure",
        "name_ar": "البنية التحتية",
        "focus_summary": (
            "Management and business development support for transport, roads, water, wastewater, marine, ports, "
            "airports, power, and other essential infrastructure."
        ),
        "focus_summary_ar": (
            "دعم الإدارة وتطوير الأعمال في النقل والطرق والمياه والصرف الصحي والأعمال البحرية والموانئ والمطارات "
            "والطاقة وغيرها من البنى التحتية الأساسية."
        ),
        "seo_title": "Infrastructure Project Management & Business Development | 3 Pillars",
        "seo_title_ar": "إدارة مشاريع البنية التحتية وتطوير الأعمال | ثري بيلارز",
        "meta_description": (
            "Support for infrastructure project delivery and business growth across transport, water, roads, marine, "
            "ports, airports, and power-related sectors."
        ),
        "meta_description_ar": (
            "دعم تنفيذ مشاريع البنية التحتية ونمو الأعمال في قطاعات النقل والمياه والطرق والأعمال البحرية والموانئ "
            "والمطارات والطاقة."
        ),
        "h1": "Infrastructure Project Management and Business Development",
        "h1_ar": "إدارة مشاريع البنية التحتية وتطوير الأعمال",
        "primary_keyword": "infrastructure project management",
        "supporting_keywords": (
            "infrastructure programme management, transport project management, water infrastructure, roads and "
            "highways, port project management"
        ),
        "intro": [
            "Infrastructure projects are essential to economic activity and community development. They often involve "
            "multiple authorities, funding arrangements, technical disciplines, contractors, suppliers, and local "
            "stakeholders. Effective management depends on strong governance, coordinated planning, transparent "
            "reporting, and informed commercial decisions.",
            "3 Pillars supports organisations involved in infrastructure development through project and programme "
            "management, PMO and project controls, opportunity assessment, market development, and strategic "
            "partnership support.",
        ],
        "intro_ar": [
            "تُعد مشاريع البنية التحتية أساسية للنشاط الاقتصادي وتنمية المجتمعات، وكثيراً ما تشمل جهات حكومية متعددة، "
            "وترتيبات تمويل، وتخصصات فنية، ومقاولين، وموردين، وأصحاب مصلحة محليين. وتعتمد الإدارة الفعّالة على حوكمة "
            "قوية، وتخطيط منسق، وتقارير شفافة، وقرارات تجارية مدروسة.",
            "وتدعم ثري بيلارز المؤسسات العاملة في تطوير البنية التحتية من خلال إدارة المشاريع والبرامج، ومكتب إدارة "
            "المشاريع وضبط المشاريع، وتقييم الفرص، وتطوير الأسواق، ودعم الشراكات الاستراتيجية.",
        ],
        "list_title": "Infrastructure subsectors",
        "list_title_ar": "قطاعات البنية التحتية الفرعية",
        "list_items": [
            ("Roads and highways", "الطرق والطرق السريعة"),
            ("Transport and mobility", "النقل والتنقل"),
            ("Water supply and wastewater systems", "أنظمة إمدادات المياه والصرف الصحي"),
            ("Marine works, ports, and coastal infrastructure", "الأعمال البحرية والموانئ والبنية التحتية الساحلية"),
            ("Airports and aviation-related infrastructure", "المطارات والبنية التحتية المرتبطة بالطيران"),
            ("Power and energy-related infrastructure", "البنية التحتية للكهرباء والطاقة"),
        ],
        "our_focus": (
            "We connect delivery oversight with market and opportunity insight, helping clients manage project "
            "complexity while building a clearer view of future business opportunities."
        ),
        "our_focus_ar": (
            "نربط الإشراف على التنفيذ بالمعلومات السوقية ورؤية الفرص، لنساعد عملاءنا على إدارة تعقيد المشاريع وبناء "
            "رؤية أوضح لفرص الأعمال المستقبلية."
        ),
        "related_services": ["project-programme-management", "pmo-project-controls", "business-development"],
    },
    {
        "slug": "urban-development-planning", "icon": "Map",
        "name": "Urban Development & Planning",
        "name_ar": "التنمية والتخطيط العمراني",
        "focus_summary": (
            "Programme coordination, development strategy, market and stakeholder assessment, phasing, and management "
            "support for urban and master-planning initiatives."
        ),
        "focus_summary_ar": (
            "تنسيق البرامج، واستراتيجية التطوير، وتقييم الأسواق وأصحاب المصلحة، والتنفيذ المرحلي، والدعم الإداري "
            "لمبادرات التخطيط العمراني والمخططات الشاملة."
        ),
        "seo_title": "Urban Development & Planning | 3 Pillars",
        "seo_title_ar": "التنمية والتخطيط العمراني | ثري بيلارز",
        "meta_description": (
            "3 Pillars supports urban development and planning initiatives through programme management, stakeholder "
            "coordination, strategic assessment, and business development."
        ),
        "meta_description_ar": (
            "تدعم ثري بيلارز مبادرات التنمية والتخطيط العمراني من خلال إدارة البرامج والتنسيق مع أصحاب المصلحة "
            "والتقييم الاستراتيجي وتطوير الأعمال."
        ),
        "h1": "Managing Urban Development and Planning Programmes",
        "h1_ar": "إدارة برامج التنمية والتخطيط العمراني",
        "primary_keyword": "urban development project management",
        "supporting_keywords": (
            "master plan programme management, urban development strategy, city development projects, stakeholder "
            "coordination"
        ),
        "intro": [
            "Urban development and planning initiatives require a long-term view, coordinated stakeholders, phased "
            "implementation, and a clear understanding of economic, social, spatial, and infrastructure priorities. "
            "3 Pillars supports the management and strategic development aspects of these initiatives, helping "
            "clients connect planning objectives with delivery structures and market realities.",
        ],
        "intro_ar": [
            "تتطلب مبادرات التنمية والتخطيط العمراني رؤية بعيدة المدى، وتنسيقاً بين أصحاب المصلحة، وتنفيذاً مرحلياً، "
            "وفهماً واضحاً للأولويات الاقتصادية والاجتماعية والمكانية وأولويات البنية التحتية. وتدعم ثري بيلارز "
            "الجوانب الإدارية والتطويرية الاستراتيجية لهذه المبادرات، لتساعد عملاءها على ربط أهداف التخطيط بهياكل "
            "التنفيذ وواقع الأسواق.",
        ],
        "list_title": "Areas of support",
        "list_title_ar": "مجالات الدعم",
        "list_items": [
            ("Programme and project coordination for urban development initiatives",
             "تنسيق البرامج والمشاريع لمبادرات التنمية العمرانية"),
            ("Implementation planning and development phasing", "تخطيط التنفيذ وتحديد مراحل التطوير"),
            ("Stakeholder mapping and engagement coordination", "تحديد أصحاب المصلحة وتنسيق التواصل معهم"),
            ("Market and socio-economic context assessment", "تقييم السياق السوقي والاجتماعي والاقتصادي"),
            ("Opportunity and partnership identification", "تحديد الفرص والشراكات"),
            ("Performance reporting and programme governance", "تقارير الأداء وحوكمة البرامج"),
        ],
        "related_services": [
            "project-programme-management", "business-development", "strategic-advisory-market-intelligence",
        ],
    },
    {
        "slug": "research-studies", "icon": "BookOpen",
        "name": "Research & Studies",
        "name_ar": "البحوث والدراسات",
        "focus_summary": (
            "Market intelligence, feasibility inputs, socio-economic and sector analysis, and evidence-based decision "
            "support, subject to approved scope."
        ),
        "focus_summary_ar": (
            "المعلومات السوقية، ومدخلات دراسات الجدوى، والتحليل الاجتماعي والاقتصادي والقطاعي، ودعم القرار القائم "
            "على الأدلة، في حدود النطاق المعتمد."
        ),
        "seo_title": "Research, Studies & Market Intelligence | 3 Pillars",
        "seo_title_ar": "البحوث والدراسات والمعلومات السوقية | ثري بيلارز",
        "meta_description": (
            "Research and market intelligence to support project planning, opportunity assessment, business "
            "development, and strategic decisions."
        ),
        "meta_description_ar": (
            "بحوث ومعلومات سوقية لدعم تخطيط المشاريع وتقييم الفرص وتطوير الأعمال والقرارات الاستراتيجية."
        ),
        "h1": "Research, Studies & Market Intelligence",
        "h1_ar": "البحوث والدراسات والمعلومات السوقية",
        "primary_keyword": "market research and feasibility studies",
        "supporting_keywords": (
            "sector studies, country market research, opportunity assessment, feasibility analysis, socio-economic "
            "research"
        ),
        "intro": [
            "Reliable research helps organisations understand context, test assumptions, and make decisions with "
            "greater confidence. 3 Pillars uses market and sector intelligence to inform project priorities, business "
            "development plans, and opportunity assessment.",
        ],
        "intro_ar": [
            "تساعد البحوث الموثوقة المؤسسات على فهم السياق واختبار الافتراضات واتخاذ القرارات بثقة أكبر. وتستخدم ثري "
            "بيلارز المعلومات السوقية والقطاعية لتوجيه أولويات المشاريع وخطط تطوير الأعمال وتقييم الفرص.",
        ],
        "list_title": "Research themes",
        "list_title_ar": "محاور البحث",
        "list_items": [
            ("Country and sector market studies", "دراسات أسواق الدول والقطاعات"),
            ("Demand and market trend assessment", "تقييم الطلب واتجاهات السوق"),
            ("Competitor and stakeholder analysis", "تحليل المنافسين وأصحاب المصلحة"),
            ("Socio-economic context and development indicators", "السياق الاجتماعي والاقتصادي ومؤشرات التنمية"),
            ("Opportunity screening and prioritisation", "فرز الفرص وترتيب أولوياتها"),
            ("Feasibility inputs and strategic decision-support reports",
             "مدخلات دراسات الجدوى وتقارير دعم القرار الاستراتيجي"),
        ],
        "positioning_note": (
            "Where assignments require specialised technical, environmental, geotechnical, traffic, GIS, or other "
            "regulated studies, the website should only list these capabilities where delivery responsibility, "
            "qualified resources, and formal scope are confirmed."
        ),
        "related_services": ["strategic-advisory-market-intelligence"],
    },
]

# ── About: values and approach ───────────────────────────────────────────

COMPANY_VALUES = [
    ("Integrity", "النزاهة",
     "We communicate clearly, act responsibly, and maintain professional standards.",
     "نتواصل بوضوح، ونتصرف بمسؤولية، ونحافظ على المعايير المهنية."),
    ("Accountability", "المساءلة",
     "We define responsibilities, track actions, and make performance visible.",
     "نحدد المسؤوليات، ونتابع الإجراءات، ونجعل الأداء واضحاً للجميع."),
    ("Insight", "الرؤية",
     "We use evidence, analysis, and sector understanding to inform decisions.",
     "نستند إلى الأدلة والتحليل وفهم القطاعات في توجيه القرارات."),
    ("Collaboration", "التعاون",
     "We coordinate with clients, delivery teams, partners, and stakeholders.",
     "ننسق مع العملاء وفرق التنفيذ والشركاء وأصحاب المصلحة."),
    ("Practicality", "الواقعية العملية",
     "We favour actionable recommendations and workable management systems.",
     "نفضّل التوصيات القابلة للتنفيذ والأنظمة الإدارية العملية."),
    ("Long-term value", "القيمة طويلة الأمد",
     "We consider sustainability, resilience, and lasting outcomes in our work.",
     "نراعي في عملنا الاستدامة والمرونة والنتائج الدائمة."),
]

#: "Name: summary" in the document; split at the colon so the name can be set in bold.
APPROACH_STEPS = [
    ("Understand the context", "فهم السياق",
     "objectives, stakeholders, constraints, markets, and risks.",
     "الأهداف وأصحاب المصلحة والقيود والأسواق والمخاطر."),
    ("Define the route", "تحديد المسار",
     "scope, priorities, responsibilities, delivery approach, and success measures.",
     "النطاق والأولويات والمسؤوليات ونهج التنفيذ ومقاييس النجاح."),
    ("Coordinate action", "تنسيق العمل",
     "align teams, information, decisions, and dependencies.",
     "مواءمة الفرق والمعلومات والقرارات والترابطات."),
    ("Monitor performance", "متابعة الأداء",
     "track progress, cost, schedule, risks, and emerging opportunities.",
     "متابعة التقدم والتكلفة والجدول الزمني والمخاطر والفرص الناشئة."),
    ("Learn and improve", "التعلم والتحسين",
     "capture lessons, strengthen processes, and support the next stage.",
     "توثيق الدروس، وتعزيز الإجراءات، ودعم المرحلة التالية."),
]

# ── Pages ────────────────────────────────────────────────────────────────

ABOUT_US = {
    "slug": "about-us",
    "title": "About Us", "title_ar": "من نحن",
    "seo_title": "About 3 Pillars | Project Delivery & Business Growth",
    "seo_title_ar": "عن ثري بيلارز | تنفيذ المشاريع ونمو الأعمال",
    "meta_description": (
        "Learn about 3 Pillars, a focused company supporting project management, business development, and strategic "
        "decision-making across key development sectors."
    ),
    "meta_description_ar": (
        "تعرّف على ثري بيلارز، الشركة المتخصصة في دعم إدارة المشاريع وتطوير الأعمال واتخاذ القرار الاستراتيجي في "
        "قطاعات التنمية الرئيسية."
    ),
    "h1": "About 3 Pillars", "h1_ar": "عن ثري بيلارز",
    "primary_keyword": "project management and business development company",
    "supporting_keywords": (
        "project management consultancy, business growth advisory, infrastructure management, strategic advisory"
    ),
    "blocks": [
        {
            "kind": "rich_text", "title": "Who We Are", "title_ar": "من نحن",
            "body": [
                "3 Pillars is a project management and business development company focused on helping organisations "
                "deliver complex projects and pursue meaningful growth opportunities. We work across the built "
                "environment, infrastructure, urban development, and research-led sectors, combining structured "
                "management practices with commercial awareness and market insight.",
                "Our role is to help clients bring greater clarity to project objectives, improve coordination and "
                "performance oversight, and make better-informed business decisions. From project planning and "
                "programme controls to market assessment and opportunity development, we focus on the disciplines that "
                "turn plans into measurable progress.",
            ],
            "body_ar": [
                "ثري بيلارز شركة متخصصة في إدارة المشاريع وتطوير الأعمال، تركز على مساعدة المؤسسات في تنفيذ المشاريع "
                "المعقدة والسعي إلى فرص نمو ذات أثر. ونعمل في قطاعات البيئة العمرانية والبنية التحتية والتنمية العمرانية "
                "والقطاعات القائمة على البحث، جامعين بين الممارسات الإدارية المنظمة والوعي التجاري والمعلومات السوقية.",
                "ويتمثل دورنا في مساعدة العملاء على إضفاء مزيد من الوضوح على أهداف مشاريعهم، وتحسين التنسيق والإشراف "
                "على الأداء، واتخاذ قرارات أعمال أكثر استنارة. فمن تخطيط المشاريع وضبط البرامج إلى تقييم الأسواق "
                "وتطوير الفرص، نركز على التخصصات التي تحوّل الخطط إلى تقدم قابل للقياس.",
            ],
        },
        {
            "kind": "rich_text", "title": "Our Vision", "title_ar": "رؤيتنا",
            "body": [
                "To be a trusted management and business development organisation, recognised for strengthening "
                "project delivery and helping clients identify and pursue sustainable opportunities across the sectors "
                "we serve.",
            ],
            "body_ar": [
                "أن نكون مؤسسة موثوقة في الإدارة وتطوير الأعمال، معروفة بتعزيز تنفيذ المشاريع ومساعدة العملاء على "
                "تحديد الفرص المستدامة والسعي إليها في القطاعات التي نخدمها.",
            ],
        },
        {
            "kind": "rich_text", "title": "Our Mission", "title_ar": "رسالتنا",
            "body": [
                "To provide practical project management, business development, and strategic advisory support that "
                "improves decision-making, supports disciplined execution, and creates a clear path from opportunity to "
                "delivery.",
            ],
            "body_ar": [
                "تقديم دعم عملي في إدارة المشاريع وتطوير الأعمال والاستشارات الاستراتيجية يحسّن اتخاذ القرار، ويدعم "
                "التنفيذ المنضبط، ويرسم مساراً واضحاً من الفرصة إلى التنفيذ.",
            ],
        },
        {"kind": "values", "title": "Our Values", "title_ar": "قيمنا"},
        {
            "kind": "approach_steps", "title": "Our Approach", "title_ar": "منهجيتنا",
            "body": [
                "We start by understanding the client’s objectives, operating context, constraints, and desired "
                "outcomes. We then define the right level of support, establish clear responsibilities and management "
                "processes, and maintain a practical focus on progress, risks, decisions, and results.",
            ],
            "body_ar": [
                "نبدأ بفهم أهداف العميل وسياق عمله والقيود التي يواجهها والنتائج التي يتطلع إليها. ثم نحدد المستوى "
                "المناسب من الدعم، ونرسي مسؤوليات وإجراءات إدارية واضحة، ونحافظ على تركيز عملي على التقدم والمخاطر "
                "والقرارات والنتائج.",
            ],
        },
        {
            "kind": "affiliation", "visible": False,
            "note": (
                "Affiliation wording – approval required\n\nIf 3 Pillars is formally part of HS Group, add a short "
                "approved statement explaining the relationship. Do not imply that 3 Pillars has the same legal "
                "identity, history, offices, or credentials as HS Group unless the corporate structure and wording "
                "have been confirmed."
            ),
        },
    ],
}

OUR_APPROACH = {
    "slug": "our-approach",
    "title": "Our Approach", "title_ar": "منهجيتنا",
    "seo_title": "Our Approach | The 3 Pillars Framework",
    "seo_title_ar": "منهجيتنا | إطار الركائز الثلاث",
    "meta_description": (
        "Discover how 3 Pillars connects project and programme management, business development, and strategic market "
        "intelligence to support better decisions and delivery."
    ),
    "meta_description_ar": (
        "اكتشف كيف تربط ثري بيلارز بين إدارة المشاريع والبرامج وتطوير الأعمال والمعلومات السوقية الاستراتيجية لدعم "
        "قرارات وتنفيذ أفضل."
    ),
    "h1": "Three Connected Pillars for Delivery and Growth",
    "h1_ar": "ثلاث ركائز مترابطة للتنفيذ والنمو",
    "primary_keyword": "integrated project management and business development",
    "supporting_keywords": "project delivery strategy, market intelligence, programme governance, business growth strategy",
    "blocks": [
        {
            "kind": "rich_text", "title": "How the pillars work together", "title_ar": "كيف تعمل الركائز معاً",
            "body": [
                "Market intelligence informs which opportunities to pursue. Business development turns selected "
                "opportunities into relationships and commercial pathways. Project and programme management supports "
                "disciplined planning, governance, and delivery once an opportunity becomes a project.",
            ],
            "body_ar": [
                "توجّه المعلومات السوقية اختيار الفرص التي يُسعى إليها، ويحوّل تطوير الأعمال الفرص المختارة إلى علاقات "
                "ومسارات تجارية، وتدعم إدارة المشاريع والبرامج التخطيط المنضبط والحوكمة والتنفيذ حين تتحول الفرصة إلى "
                "مشروع.",
            ],
        },
    ],
}

PAGES = [
    ABOUT_US,
    OUR_APPROACH,
    {
        "slug": "leadership-team", "path": "/about-us/leadership-team/",
        "title": "Leadership & Team", "title_ar": "القيادة والفريق",
    },
    {
        "slug": "hs-group", "path": "/about-us/hs-group/",
        "title": "Our Relationship with HS Group", "title_ar": "علاقتنا بمجموعة HS",
        "note": (
            "Legal and brand-approved description of whether 3 Pillars is part of HS Group, affiliated, or "
            "independently operated."
        ),
    },
    {
        "slug": "services",
        "title": "Services", "title_ar": "الخدمات",
        "seo_title": "3 Pillars Services | Project Management & Business Development",
        "seo_title_ar": "خدمات ثري بيلارز | إدارة المشاريع وتطوير الأعمال",
        "meta_description": (
            "Explore 3 Pillars services in project and programme management, PMO and project controls, business "
            "development, market expansion, and strategic advisory."
        ),
        "meta_description_ar": (
            "استكشف خدمات ثري بيلارز في إدارة المشاريع والبرامج، ومكتب إدارة المشاريع وضبط المشاريع، وتطوير الأعمال، "
            "والتوسع في الأسواق، والاستشارات الاستراتيجية."
        ),
        "h1": "Our Services", "h1_ar": "خدماتنا",
        "primary_keyword": "project management and business development services",
        "supporting_keywords": (
            "project and programme management, PMO services, project controls, tender management, market entry advisory"
        ),
        "intro": (
            "3 Pillars provides management and business development services designed to support organisations at "
            "different stages of the project and business lifecycle. We can support a defined assignment, a critical "
            "project phase, or an ongoing management and growth programme, depending on the client’s needs and agreed "
            "scope."
        ),
        "intro_ar": (
            "تقدم ثري بيلارز خدمات في الإدارة وتطوير الأعمال مصممة لدعم المؤسسات في مختلف مراحل دورة حياة المشروع "
            "والأعمال. ويمكننا دعم مهمة محددة، أو مرحلة حرجة من المشروع، أو برنامج مستمر للإدارة والنمو، وفقاً "
            "لاحتياجات العميل والنطاق المتفق عليه."
        ),
        "note": (
            "Each service page should link to the sectors where the service is relevant, and each sector page should "
            "link back to the most relevant service pages."
        ),
    },
    {
        "slug": "sectors",
        "title": "Sectors", "title_ar": "القطاعات",
        "seo_title": "Sectors We Serve | 3 Pillars",
        "seo_title_ar": "القطاعات التي نخدمها | ثري بيلارز",
        "meta_description": (
            "3 Pillars supports project management and business development across the built environment, "
            "infrastructure, urban development and planning, and research-led sectors."
        ),
        "meta_description_ar": (
            "تدعم ثري بيلارز إدارة المشاريع وتطوير الأعمال في البيئة العمرانية والبنية التحتية والتنمية والتخطيط "
            "العمراني والقطاعات القائمة على البحث."
        ),
        "h1": "Sectors We Serve", "h1_ar": "القطاعات التي نخدمها",
        "primary_keyword": "project management across infrastructure and built environment",
        "supporting_keywords": (
            "built environment project management, infrastructure programme management, urban development, research and "
            "studies"
        ),
        "intro": (
            "The sectors we serve are connected by complex programmes, multiple stakeholders, long delivery horizons, "
            "and significant investment decisions. 3 Pillars applies project management, business development, and "
            "strategic insight to help clients navigate these demands."
        ),
        "intro_ar": (
            "تجمع القطاعات التي نخدمها برامجُ معقدة، وأصحابُ مصلحة متعددون، وآفاقُ تنفيذ طويلة، وقراراتُ استثمار "
            "كبيرة. وتوظّف ثري بيلارز إدارة المشاريع وتطوير الأعمال والرؤية الاستراتيجية لمساعدة عملائها على التعامل "
            "مع هذه المتطلبات."
        ),
    },
    {
        "slug": "projects",
        "title": "Projects", "title_ar": "المشاريع",
        "seo_title": "Projects & Case Studies | 3 Pillars",
        "seo_title_ar": "المشاريع ودراسات الحالة | ثري بيلارز",
        "meta_description": (
            "Explore selected projects and case studies demonstrating project management, programme coordination, "
            "project controls, and business development support."
        ),
        "meta_description_ar": (
            "استكشف مشاريع مختارة ودراسات حالة توضح دعمنا في إدارة المشاريع وتنسيق البرامج وضبط المشاريع وتطوير "
            "الأعمال."
        ),
        "h1": "Selected Projects and Case Studies", "h1_ar": "مشاريع مختارة ودراسات حالة",
        "primary_keyword": "project management projects",
        "supporting_keywords": (
            "infrastructure project management case studies, construction programme management, development project "
            "case studies"
        ),
        "note": (
            "Our project experience should be presented through clear, evidence-based case studies. Each case study "
            "must explain the project context, the client’s challenge, the scope of 3 Pillars’ involvement, and the "
            "value delivered. The objective is to show what the company was specifically responsible for, not simply "
            "to display project names or photographs.\n\nCredit the delivery entity and 3 Pillars’ "
            "precise role accurately. Do not attribute HS Group, affiliate, or joint-venture project work to 3 Pillars "
            "without evidence and approval."
        ),
    },
    {
        "slug": "insights",
        "title": "Insights", "title_ar": "رؤى",
        "seo_title": "Insights | Project Management & Business Development",
        "seo_title_ar": "رؤى | إدارة المشاريع وتطوير الأعمال",
        "meta_description": (
            "Read 3 Pillars insights on project management, infrastructure markets, business development, project "
            "controls, and strategic growth."
        ),
        "meta_description_ar": (
            "اقرأ رؤى ثري بيلارز حول إدارة المشاريع وأسواق البنية التحتية وتطوير الأعمال وضبط المشاريع والنمو "
            "الاستراتيجي."
        ),
        "h1": "Insights and Market Perspectives", "h1_ar": "رؤى ووجهات نظر سوقية",
        "primary_keyword": "project management and infrastructure insights",
        "supporting_keywords": (
            "project management best practices, infrastructure market trends, business development insights, "
            "programme controls"
        ),
        "intro": (
            "Explore practical perspectives on managing complex projects, understanding market developments, and "
            "building effective business strategies across the sectors we serve."
        ),
        "intro_ar": (
            "استكشف وجهات نظر عملية حول إدارة المشاريع المعقدة، وفهم تطورات الأسواق، وبناء استراتيجيات أعمال فعّالة في "
            "القطاعات التي نخدمها."
        ),
        "note": (
            "Use the News section for verified corporate announcements, appointments, partnerships, market entries, "
            "project milestones, event participation, and official updates. Every item should include a publication "
            "date, a concise summary, and a factual description of 3 Pillars’ role."
        ),
    },
    {
        "slug": "careers",
        "title": "Careers", "title_ar": "الوظائف",
        "seo_title": "Careers at 3 Pillars | Join Our Team",
        "seo_title_ar": "الوظائف في ثري بيلارز | انضم إلى فريقنا",
        "meta_description": (
            "Explore career opportunities at 3 Pillars for professionals in project management, project controls, "
            "business development, research, and strategic advisory."
        ),
        "meta_description_ar": (
            "استكشف الفرص الوظيفية في ثري بيلارز للمهنيين في إدارة المشاريع وضبط المشاريع وتطوير الأعمال والبحوث "
            "والاستشارات الاستراتيجية."
        ),
        "h1": "Build Your Career with 3 Pillars", "h1_ar": "ابنِ مسيرتك المهنية مع ثري بيلارز",
        "primary_keyword": "project management careers",
        "supporting_keywords": (
            "project manager jobs, programme management careers, business development careers, PMO careers"
        ),
        "intro": (
            "We are interested in professionals who bring strong technical understanding, commercial awareness, "
            "analytical thinking, and a collaborative approach. Explore current opportunities and learn how you can "
            "contribute to projects and business development across our sectors."
        ),
        "intro_ar": (
            "نهتم بالمهنيين الذين يجمعون بين الفهم الفني المتين والوعي التجاري والتفكير التحليلي وروح التعاون. استكشف "
            "الفرص المتاحة حالياً وتعرّف على كيفية إسهامك في المشاريع وتطوير الأعمال في قطاعاتنا."
        ),
        "cta_label": "View Opportunities", "cta_label_ar": "استعرض الفرص الوظيفية",
    },
    {
        "slug": "contact",
        "title": "Contact Us", "title_ar": "تواصل معنا",
        "seo_title": "Contact 3 Pillars | Project & Business Enquiries",
        "seo_title_ar": "تواصل مع ثري بيلارز | استفسارات المشاريع والأعمال",
        "meta_description": (
            "Contact 3 Pillars to discuss project management, programme controls, business development, market "
            "expansion, or strategic advisory requirements."
        ),
        "meta_description_ar": (
            "تواصل مع ثري بيلارز لمناقشة احتياجاتك في إدارة المشاريع أو ضبط البرامج أو تطوير الأعمال أو التوسع في "
            "الأسواق أو الاستشارات الاستراتيجية."
        ),
        "h1": "Let’s Discuss Your Project or Business Opportunity",
        "h1_ar": "لنناقش مشروعك أو فرصة أعمالك",
        "primary_keyword": "contact project management consultancy",
        "supporting_keywords": (
            "project management enquiry, business development consultation, infrastructure project support"
        ),
        "intro": (
            "Tell us about your project, business priorities, or target market. Our team will review your enquiry and "
            "direct it to the appropriate contact."
        ),
        "intro_ar": (
            "أخبرنا عن مشروعك أو أولويات أعمالك أو السوق التي تستهدفها، وسيراجع فريقنا استفسارك ويحيله إلى الجهة "
            "المختصة."
        ),
        "cta_label": "Submit Enquiry", "cta_label_ar": "أرسل الاستفسار",
        "note": (
            "Publish only verified corporate details: office address, official email, telephone number, business "
            "hours, and the social media channels managed by 3 Pillars. If the company uses HS Group offices or shared "
            "contact channels, explain the relationship and obtain approval before displaying them."
        ),
    },
    {
        "slug": "request-a-consultation", "path": CONSULTATION,
        "title": "Request a Consultation", "title_ar": "اطلب استشارة",
    },
]

#: Old pages this content replaces; their addresses now 404 (decision D2).
RETIRED_PAGES = ("about", "approach", "request-a-proposal")

# ── Navigation ───────────────────────────────────────────────────────────

HEADER_NAV = [
    {"label": "Home", "label_ar": "الرئيسية", "link": "/"},
    {"label": "About Us", "label_ar": "من نحن", "link": "/about-us/", "children": [
        {"label": "Who We Are", "label_ar": "من نحن", "link": "/about-us/"},
        {"label": "Our Approach", "label_ar": "منهجيتنا", "link": "/our-approach/"},
        {"label": "Leadership & Team", "label_ar": "القيادة والفريق", "link": "/about-us/leadership-team/"},
        {"label": "Our Relationship with HS Group", "label_ar": "علاقتنا بمجموعة HS", "link": "/about-us/hs-group/",
         "visible": False},
    ]},
    {"label": "Services", "label_ar": "الخدمات", "link": "/services/", "mega_menu": "services", "children": [
        {"label": "Project & Programme Management", "label_ar": "إدارة المشاريع والبرامج",
         "link": "/services/project-programme-management/"},
        {"label": "PMO & Project Controls", "label_ar": "مكتب إدارة المشاريع وضبط المشاريع",
         "link": "/services/pmo-project-controls/"},
        {"label": "Business Development", "label_ar": "تطوير الأعمال", "link": "/services/business-development/"},
        {"label": "Strategic Advisory & Market Intelligence", "label_ar": "الاستشارات الاستراتيجية والمعلومات السوقية",
         "link": "/services/strategic-advisory-market-intelligence/"},
    ]},
    {"label": "Sectors", "label_ar": "القطاعات", "link": "/sectors/", "mega_menu": "sectors", "children": [
        {"label": "Built Environment", "label_ar": "البيئة العمرانية", "link": "/sectors/built-environment/"},
        {"label": "Infrastructure", "label_ar": "البنية التحتية", "link": "/sectors/infrastructure/"},
        {"label": "Urban Development & Planning", "label_ar": "التنمية والتخطيط العمراني",
         "link": "/sectors/urban-development-planning/"},
        {"label": "Research & Studies", "label_ar": "البحوث والدراسات", "link": "/sectors/research-studies/"},
    ]},
    {"label": "Projects", "label_ar": "المشاريع", "link": "/projects/", "children": [
        {"label": "Selected Projects", "label_ar": "مشاريع مختارة", "link": "/projects/?type=selected"},
        {"label": "Case Studies", "label_ar": "دراسات الحالة", "link": "/projects/?type=case-study"},
    ]},
    {"label": "Insights", "label_ar": "رؤى", "link": "/insights/", "children": [
        {"label": "Articles", "label_ar": "مقالات", "link": "/insights/?kind=article"},
        {"label": "Market Perspectives", "label_ar": "وجهات نظر سوقية", "link": "/insights/?kind=perspective"},
        {"label": "Project Delivery Insights", "label_ar": "رؤى في تنفيذ المشاريع", "link": "/insights/?kind=delivery"},
        {"label": "News", "label_ar": "الأخبار", "link": "/insights/?kind=news"},
    ]},
    {"label": "Careers", "label_ar": "الوظائف", "link": "/careers/"},
    {"label": "Contact", "label_ar": "تواصل", "link": "/contact/", "children": [
        {"label": "Contact Us", "label_ar": "تواصل معنا", "link": "/contact/"},
        {"label": "Request a Consultation", "label_ar": "اطلب استشارة", "link": CONSULTATION, "is_cta": True},
    ]},
]

#: The document gives no footer; columns keep their existing titles and link to the pages above.
FOOTER = [
    ("Company", "الشركة", [
        ("About Us", "من نحن", "/about-us/"),
        ("Our Approach", "منهجيتنا", "/our-approach/"),
        ("Insights", "رؤى", "/insights/"),
        ("Careers", "الوظائف", "/careers/"),
    ]),
    ("Work with us", "اعمل معنا", [
        ("Request a Consultation", "اطلب استشارة", CONSULTATION),
        ("Contact Us", "تواصل معنا", "/contact/"),
        ("Capability statement", "ملف القدرات", "/capability-statement/"),
    ]),
]

LEGAL_LINKS = {"/privacy": "/privacy/", "/terms": "/terms/", "/cookies": "/cookies/"}

# ── Insights ─────────────────────────────────────────────────────────────

INSIGHT_CATEGORIES = [
    ("project-programme-management", "Project & Programme Management", "إدارة المشاريع والبرامج"),
    ("pmo-planning-project-controls", "PMO, Planning & Project Controls",
     "مكتب إدارة المشاريع والتخطيط وضبط المشاريع"),
    ("infrastructure-built-environment-markets", "Infrastructure and Built Environment Markets",
     "أسواق البنية التحتية والبيئة العمرانية"),
    ("business-development-market-expansion", "Business Development & Market Expansion",
     "تطوير الأعمال والتوسع في الأسواق"),
    ("strategic-partnerships-tenders", "Strategic Partnerships and Tenders", "الشراكات الاستراتيجية والمناقصات"),
    ("research-feasibility-opportunity-assessment", "Research, Feasibility & Opportunity Assessment",
     "البحوث ودراسات الجدوى وتقييم الفرص"),
]

DRAFT_TOPICS = [
    ("What Does Effective Project Governance Look Like in Large Infrastructure Projects?",
     "كيف تبدو حوكمة المشاريع الفعّالة في مشاريع البنية التحتية الكبرى؟"),
    ("Project Management vs. Programme Management: Understanding the Difference",
     "إدارة المشاريع وإدارة البرامج: فهم الفرق بينهما"),
    ("Why Project Controls Matter for Cost and Schedule Performance",
     "لماذا يهم ضبط المشاريع لأداء التكاليف والجداول الزمنية"),
    ("How to Evaluate Infrastructure Opportunities in Emerging Markets",
     "كيف تُقيَّم فرص البنية التحتية في الأسواق الناشئة"),
    ("A Practical Framework for Market Entry in the Infrastructure Sector",
     "إطار عملي لدخول الأسواق في قطاع البنية التحتية"),
    ("From Opportunity Identification to Bid Strategy: Building a Disciplined Pursuit Process",
     "من تحديد الفرص إلى استراتيجية العطاءات: بناء عملية منضبطة للسعي إلى الفرص"),
    ("The Role of Market Intelligence in Better Investment and Development Decisions",
     "دور المعلومات السوقية في تحسين قرارات الاستثمار والتطوير"),
    ("How a Project Management Office Improves Portfolio Visibility",
     "كيف يحسّن مكتب إدارة المشاريع وضوح الرؤية على المحفظة"),
]

# ── Launch readiness (document section 19) ───────────────────────────────

CLAIMS_TO_VERIFY = [
    ("Corporate relationship", "Legal and brand-approved description of whether 3 Pillars is part of HS Group, "
                               "affiliated, or independently operated."),
    ("Company history", "Approved establishment date and whether any HS Group history can be attributed to 3 Pillars."),
    ("Project experience", "Exact entity that delivered each project and the exact 3 Pillars role, if any."),
    ("Numbers and statistics", "Project counts, locations, staff numbers, years of experience, and measurable outcomes "
                               "supported by records."),
    ("Services", "Approved service list, delivery capability, licences, professional registrations, and geographic "
                 "limitations."),
    ("Leadership and team", "Names, titles, biographies, photographs, and approval to publish."),
    ("Clients and partners", "Permission to use names, logos, quotations, project images, or case study information."),
    ("Contact information", "Official business email, telephone numbers, addresses, and social media URLs."),
]

PRE_LAUNCH_CHECKLIST = [
    "Approve the positioning statement and confirm the three-pillar framework.",
    "Confirm the corporate relationship statement and permitted use of HS Group credentials.",
    "Confirm the final service list and ensure each service has an accountable delivery owner.",
    "Approve sector naming and ensure it matches actual operating priorities.",
    "Complete all SEO titles, meta descriptions, H1s, URLs, and internal links.",
    "Prepare genuine project case studies with accurate role attribution and approved images.",
    "Add privacy policy, cookie notice, terms of use, and any required legal disclosures.",
    "Test all forms, email routing, calls to action, mobile layouts, and accessibility basics.",
    "Check page speed, structured data, sitemap, robots.txt, redirects, and analytics.",
    "Proofread all content and remove every placeholder before publication.",
]
