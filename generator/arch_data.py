# -*- coding: utf-8 -*-
"""XARU HOME — Phase 1 architecture data (single source of truth).
Nav tree (4 doors + Company + Insights) and shell-page registry, in EN/ES/AR/ZH.
Consumed by gen_i18n.py to (a) inject the mega-menu into every generated page and
(b) build the navigable shell pages. No design tokens are defined here."""

LANGS = ("en", "es", "ar", "zh")

def T(en, es, ar, zh):
    return {"en": en, "es": es, "ar": ar, "zh": zh}

# ------------------------------------------------------------------ buttons / chrome
BTN_ENQUIRY = T("Private Enquiry", "Consulta Privada", "استفسار خاص", "私人咨询")
BTN_SUBMIT  = T("Submit an Opportunity", "Presentar una oportunidad", "تقديم فرصة", "提交机会")
CRUMB_HOME  = T("Home", "Inicio", "الرئيسية", "首页")
SELECT_LANG = T("Select language", "Seleccionar idioma", "اختر اللغة", "选择语言")
EXPAND      = T("Expand section", "Desplegar sección", "توسيع القسم", "展开栏目")
PH          = T("[ PENDING — PHASE 2 COPY ]", "[ PENDIENTE — TEXTO FASE 2 ]",
                "[ قيد الإعداد — محتوى المرحلة 2 ]", "[ 待定 — 第二阶段文案 ]")
VIEW_DIV    = T("View division", "Ver división", "عرض القسم", "查看板块")

# ------------------------------------------------------------------ the nav tree
# door = {slug,label,intro,intro_sub,cols[]}; col = {slug,title,wide,items[label]}
NAV = [
 {"slug": "real-estate",
  "label": T("Real Estate", "Inmobiliario", "العقارات", "房地产"),
  "intro": T("Exceptional properties, held to a single standard.",
             "Propiedades excepcionales, bajo un solo estándar.",
             "عقارات استثنائية، وفق معيار واحد.", "卓越房产，恪守统一标准。"),
  "intro_sub": T("Private residences and operating hospitality assets, curated worldwide.",
                 "Residencias privadas y activos hoteleros en operación, seleccionados en todo el mundo.",
                 "مساكن خاصة وأصول ضيافة تشغيلية، منتقاة حول العالم.", "甄选全球的私人住宅与运营中的酒店资产。"),
  "cols": [
   {"slug": "real-estate/private-properties",
    "title": T("Private Properties", "Propiedades Privadas", "العقارات الخاصة", "私人房产"),
    "items": [
     T("Villas & mansions", "Villas y mansiones", "الفيلات والقصور", "别墅与豪宅"),
     T("Castles, haciendas & estates", "Castillos, haciendas y fincas", "القلاع والضياع والحوزات", "城堡、庄园与地产"),
     T("Private islands", "Islas privadas", "الجزر الخاصة", "私人岛屿"),
     T("Branded residences", "Residencias de marca", "المساكن ذات العلامات", "品牌住宅"),
     T("New residential", "Residencial nuevo", "سكني جديد", "全新住宅"),
     T("Private search by mandate", "Búsqueda privada por mandato", "بحث خاص بالتفويض", "受托私人寻购"),
     T("Sell your property", "Venda su propiedad", "بيع عقارك", "出售您的房产")]},
   {"slug": "real-estate/commercial-hospitality", "wide": True,
    "title": T("Commercial & Hospitality", "Comercial y Hostelería", "التجاري والضيافة", "商业与酒店"),
    "items": [
     T("Operational hotels", "Hoteles en operación", "فنادق تشغيلية", "运营中酒店"),
     T("Repositioning", "Reposicionamiento", "إعادة التموضع", "重新定位"),
     T("Resorts", "Resorts", "المنتجعات", "度假村"),
     T("Serviced residences", "Aparthoteles", "المساكن المخدومة", "服务式公寓"),
     T("Theme parks & destinations", "Parques temáticos y destinos", "المدن الترفيهية والوجهات", "主题公园与目的地"),
     T("Marinas, clubs & leisure", "Marinas, clubes y ocio", "المراسي والنوادي والترفيه", "码头、俱乐部与休闲"),
     T("Income commercial", "Comercial de renta", "التجاري المدرّ للدخل", "收益型商业"),
     T("Halted / incomplete projects", "Proyectos detenidos / incompletos", "مشاريع متوقفة / غير مكتملة", "停滞 / 未完成项目"),
     T("Confidential portfolio", "Portafolio confidencial", "محفظة سرّية", "保密资产组合")]},
  ]},

 {"slug": "developments",
  "label": T("Developments", "Desarrollos", "التطوير", "开发项目"),
  "intro": T("Land and master developments, from vision to delivery.",
             "Suelo y desarrollos maestros, de la visión a la entrega.",
             "الأراضي والتطويرات الكبرى، من الرؤية إلى التسليم.", "从愿景到交付的土地与总体开发。"),
  "intro_sub": T("Territory, structuring and execution under one responsibility.",
                 "Territorio, estructuración y ejecución bajo una sola responsabilidad.",
                 "الأرض والهيكلة والتنفيذ تحت مسؤولية واحدة.", "土地、架构与执行，统一担责。"),
  "cols": [
   {"slug": "developments/land-master-developments", "wide": True,
    "title": T("Land & Master Developments", "Suelo y Desarrollos Maestros", "الأراضي والتطويرات الكبرى", "土地与总体开发"),
    "items": [
     T("Large land", "Grandes extensiones", "أراضٍ واسعة", "大宗土地"),
     T("Coastal land", "Suelo costero", "أراضٍ ساحلية", "滨海土地"),
     T("Resort land", "Suelo para resorts", "أراضي المنتجعات", "度假村用地"),
     T("Mixed-use", "Uso mixto", "الاستخدام المختلط", "混合用途"),
     T("Planned communities", "Comunidades planificadas", "مجتمعات مخططة", "规划社区"),
     T("Experiential destinations", "Destinos experienciales", "وجهات تجريبية", "体验式目的地"),
     T("Permitted land", "Suelo con permisos", "أراضٍ مرخّصة", "已获许可土地"),
     T("Land in regularization", "Suelo en regularización", "أراضٍ قيد التسوية", "权属规整中土地"),
     T("Signature projects / ASHIMA", "Proyectos emblemáticos / ASHIMA", "مشاريع مميّزة / ASHIMA", "标志性项目 / ASHIMA")]},
   {"slug": "developments/project-structuring", "wide": True,
    "title": T("Project Structuring & Development", "Estructuración y Desarrollo de Proyectos", "هيكلة وتطوير المشاريع", "项目架构与开发"),
    "items": [
     T("Feasibility", "Viabilidad", "الجدوى", "可行性"),
     T("Legal & fiduciary structuring", "Estructuración jurídica y fiduciaria", "الهيكلة القانونية والائتمانية", "法律与信托架构"),
     T("SPV / vehicles", "Vehículos / SPV", "الكيانات / SPV", "特殊目的载体 / SPV"),
     T("Master plan & business model", "Master plan y modelo de negocio", "المخطط العام ونموذج العمل", "总体规划与商业模式"),
     T("Licensing & permits", "Licencias y permisos", "التراخيص والتصاريح", "牌照与许可"),
     T("Operator selection", "Selección de operador", "اختيار المشغّل", "运营商遴选"),
     T("Development management", "Gestión de desarrollo", "إدارة التطوير", "开发管理"),
     T("Commercialization", "Comercialización", "التسويق التجاري", "商业化"),
     T("XARU as integrator / co-developer", "XARU como integrador / codesarrollador", "XARU كمُدمج / مطوّر شريك", "XARU 作为整合者 / 联合开发者")]},
  ]},

 {"slug": "capital",
  "label": T("Capital & Transactions", "Capital y Transacciones", "رأس المال والصفقات", "资本与交易"),
  "intro": T("Capital and projects, matched with discipline.",
             "Capital y proyectos, unidos con disciplina.",
             "رأس المال والمشاريع، مقرونان بانضباط.", "资本与项目，审慎对接。"),
  "intro_sub": T("A two-way structure — capital seeking projects, projects seeking capital.",
                 "Una estructura de doble vía — capital que busca proyectos, proyectos que buscan capital.",
                 "بنية ثنائية الاتجاه — رأس مال يبحث عن مشاريع، ومشاريع تبحث عن رأس مال.", "双向架构——资本寻项目，项目寻资本。"),
  "cols": [
   {"slug": "capital/strategic-partnerships", "wide": True,
    "title": T("Capital & Strategic Partnerships", "Capital y Alianzas Estratégicas", "رأس المال والشراكات الاستراتيجية", "资本与战略合作"),
    "items": [
     T("Projects seeking capital", "Proyectos que buscan capital", "مشاريع تبحث عن رأس مال", "寻求资本的项目"),
     T("Capital seeking projects", "Capital que busca proyectos", "رأس مال يبحث عن مشاريع", "寻求项目的资本"),
     T("Developers seeking land", "Desarrolladores que buscan suelo", "مطورون يبحثون عن أراضٍ", "寻求土地的开发商"),
     T("Owners seeking developer", "Propietarios que buscan desarrollador", "ملاك يبحثون عن مطوّر", "寻求开发商的业主"),
     T("Operators seeking assets", "Operadores que buscan activos", "مشغّلون يبحثون عن أصول", "寻求资产的运营商"),
     T("Joint ventures", "Joint ventures", "المشاريع المشتركة", "合资企业"),
     T("Funds & family offices", "Fondos y family offices", "الصناديق والمكاتب العائلية", "基金与家族办公室"),
     T("Due diligence", "Due diligence", "العناية الواجبة", "尽职调查"),
     T("Deal origination", "Originación de operaciones", "نشأة الصفقات", "交易发起"),
     T("Transaction management", "Gestión de transacciones", "إدارة الصفقات", "交易管理")]},
   {"slug": "capital/deal-room",
    "title": T("Private Deal Room", "Sala de Operaciones Privada", "غرفة الصفقات الخاصة", "私人交易室"),
    "items": [
     T("Request private access", "Solicitar acceso privado", "طلب وصول خاص", "申请私人访问")]},
  ]},

 {"slug": "business-infrastructure",
  "label": T("Business Infrastructure", "Infraestructura Empresarial", "البنية المؤسسية", "企业基础设施"),
  "intro": T("The infrastructure behind ownership and operation.",
             "La infraestructura detrás de la propiedad y la operación.",
             "البنية التي تسند التملّك والتشغيل.", "支撑持有与运营的基础设施。"),
  "intro_sub": T("Trade, financial infrastructure, corporate services and relocation.",
                 "Comercio, infraestructura financiera, servicios corporativos y relocalización.",
                 "التجارة والبنية المالية والخدمات المؤسسية والانتقال.", "贸易、金融基础设施、企业服务与迁居。"),
  "cols": [
   {"slug": "business-infrastructure/trade-financial", "wide": True,
    "title": T("Trade & Financial Infrastructure", "Comercio e Infraestructura Financiera", "التجارة والبنية المالية", "贸易与金融基础设施"),
    "items": [
     T("Commodities, mining & quarry licenses", "Commodities, minería y canteras", "السلع والتعدين ورخص المحاجر", "大宗商品、矿业与采石许可"),
     T("Agricultural & productive", "Agrícolas y productivos", "الزراعية والإنتاجية", "农业与生产性资产"),
     T("Operating assets", "Activos operativos", "الأصول التشغيلية", "运营资产"),
     T("Commodities commercialization", "Comercialización de commodities", "تسويق السلع", "大宗商品商业化"),
     T("Offtake & placement", "Offtake y colocación", "الشراء المسبق والتصريف", "承购与配售"),
     T("International distribution", "Distribución internacional", "التوزيع الدولي", "国际分销"),
     T("Payments infrastructure", "Infraestructura de pagos", "بنية المدفوعات", "支付基础设施"),
     T("Orchestration & reconciliation", "Orquestación y conciliación", "التنسيق والتسوية", "编排与对账"),
     T("Custom financial platforms", "Plataformas financieras a medida", "منصّات مالية مخصّصة", "定制金融平台"),
     T("Integrations & APIs", "Integraciones y APIs", "التكاملات وواجهات API", "集成与 API")]},
   {"slug": "business-infrastructure/corporate-services", "wide": True,
    "title": T("Corporate Services & Relocation", "Servicios Corporativos y Relocalización", "الخدمات المؤسسية والانتقال", "企业服务与迁居"),
    "items": [
     T("Company formation", "Constitución de empresas", "تأسيس الشركات", "公司设立"),
     T("Corporate governance", "Gobierno corporativo", "الحوكمة المؤسسية", "公司治理"),
     T("Legal coordination", "Coordinación legal", "التنسيق القانوني", "法律协调"),
     T("Tax & accounting", "Fiscalidad y contabilidad", "الضرائب والمحاسبة", "税务与会计"),
     T("AML / compliance / DD", "AML / cumplimiento / DD", "مكافحة الغسل / الامتثال / العناية", "反洗钱 / 合规 / 尽调"),
     T("Banking & operational readiness", "Banca y preparación operativa", "الخدمات المصرفية والجاهزية التشغيلية", "银行与运营准备"),
     T("Migration & residency", "Migración y residencia", "الهجرة والإقامة", "移民与居留"),
     T("Family relocation", "Relocalización familiar", "انتقال العائلة", "家庭迁居"),
     T("Business installation", "Instalación empresarial", "التأسيس التشغيلي للأعمال", "企业落地"),
     T("Ongoing corporate admin", "Administración corporativa continua", "الإدارة المؤسسية المستمرة", "持续企业行政")]},
  ]},

 {"slug": "company", "single": True,
  "label": T("Company", "Compañía", "الشركة", "公司"),
  "intro": T("One structure. Verifiable capability.", "Una estructura. Capacidad verificable.",
             "بنية واحدة. قدرة قابلة للتحقّق.", "单一架构。可验证的能力。"),
  "intro_sub": T("Who we are, how we operate, and where.", "Quiénes somos, cómo operamos y dónde.",
                 "من نحن، وكيف نعمل، وأين.", "我们是谁、如何运作、身在何处。"),
  "cols": [
   {"slug": "company", "wide": True,
    "title": T("The Company", "La Compañía", "الشركة", "公司"),
    # per-item targets (Phase 5): real sections of /company/ + the Insights hub
    "hrefs": ["company/#who-we-are", "company/#operating-model", "company/#offices",
              "company/#team", "company/#entities", "company/#governance",
              "company/#projects", "company/#network", "insights/", "company/#contact"],
    "items": [
     T("Who we are", "Quiénes somos", "من نحن", "关于我们"),
     T("Operating model", "Modelo operativo", "نموذج التشغيل", "运营模式"),
     T("Offices", "Oficinas", "المكاتب", "办公网络"),
     T("Team", "Equipo", "الفريق", "团队"),
     T("Entities & scope", "Entidades y alcance", "الكيانات والنطاق", "实体与范围"),
     T("Governance & standards", "Gobernanza y estándares", "الحوكمة والمعايير", "治理与标准"),
     T("Projects & cases", "Proyectos y casos", "المشاريع والحالات", "项目与案例"),
     T("International network", "Red internacional", "الشبكة الدولية", "国际网络"),
     T("Insights", "Análisis", "رؤى", "洞察"),
     T("Contact", "Contacto", "اتصل بنا", "联系我们")]},
  ]},

 {"slug": "insights", "single": True,
  "label": T("Insights", "Análisis", "رؤى", "洞察"),
  "intro": T("Perspective, by sector.", "Perspectiva, por sector.", "رؤى بحسب القطاع.", "分门别类的洞见。"),
  "intro_sub": T("Research and commentary across our markets.",
                 "Investigación y análisis en nuestros mercados.",
                 "أبحاث وتحليلات عبر أسواقنا.", "覆盖各市场的研究与评论。"),
  "cols": [
   {"slug": "insights", "wide": True,
    "title": T("Insights", "Análisis", "رؤى", "洞察"),
    # per-item targets (Phase 5): the hub's category anchors
    "hrefs": ["insights/#luxury-residential", "insights/#hospitality", "insights/#land",
              "insights/#capital", "insights/#development", "insights/#commodities",
              "insights/#international-establishment"],
    "items": [
     T("Luxury residential", "Residencial de lujo", "السكني الفاخر", "奢华住宅"),
     T("Hospitality", "Hostelería", "الضيافة", "酒店业"),
     T("Land", "Suelo", "الأراضي", "土地"),
     T("Capital", "Capital", "رأس المال", "资本"),
     T("Development", "Desarrollo", "التطوير", "开发"),
     T("Commodities", "Commodities", "السلع", "大宗商品"),
     T("International establishment", "Establecimiento internacional", "التأسيس الدولي", "国际落地")]},
  ]},
]

# ------------------------------------------------------------------ 12-section pillar formula
PILLAR_SECTIONS = [
 ("01", T("Capability Statement", "Declaración de capacidad", "بيان القدرة", "能力声明")),
 ("02", T("Who We Serve", "A quién servimos", "لمن نقدّم خدماتنا", "服务对象")),
 ("03", T("Assets & Needs", "Activos y necesidades", "الأصول والاحتياجات", "资产与需求")),
 ("04", T("What XARU Does", "Qué hace XARU", "ما تقوم به XARU", "XARU 的职责")),
 ("05", T("What XARU Does Not Do", "Qué NO hace XARU", "ما لا تقوم به XARU", "XARU 不做什么")),
 ("06", T("How We Work", "Cómo trabajamos", "كيف نعمل", "工作流程")),
 ("07", T("Admission Criteria", "Criterios de admisión", "معايير القبول", "准入标准")),
 ("08", T("Internal & External Capabilities", "Capacidades internas y externas", "القدرات الداخلية والخارجية", "内部与外部能力")),
 ("09", T("Illustrative Scenario", "Escenario ilustrativo", "سيناريو توضيحي", "示例情景")),
 ("10", T("Governance & Compliance", "Gobernanza y cumplimiento", "الحوكمة والامتثال", "治理与合规")),
 ("11", T("Frequently Asked Questions", "Preguntas frecuentes", "الأسئلة الشائعة", "常见问题")),
 ("12", T("Speak With XARU", "Hable con XARU", "تحدّث مع XARU", "联系 XARU")),
]

# Permitted capability language (§6) — safe to show in the governance section.
CAPABILITY_NOTE = T(
 "Depending on the project, jurisdiction, feasibility and mandate, XARU may act as adviser, structurer, integrator, sponsor, manager or participant. XARU designs, integrates and coordinates financial and technological infrastructure through authorised entities and partners where the activity requires it.",
 "Según el proyecto, la jurisdicción, la viabilidad y el mandato, XARU puede actuar como asesor, estructurador, integrador, sponsor, gestor o participante. XARU diseña, integra y coordina infraestructura financiera y tecnológica a través de entidades y partners autorizados cuando la actividad lo requiere.",
 "بحسب المشروع والولاية القضائية والجدوى والتفويض، قد تعمل XARU كمستشار أو مُهيكل أو مُدمج أو راعٍ أو مدير أو مشارك. تصمّم XARU وتُدمج وتنسّق البنية المالية والتقنية عبر كيانات وشركاء مرخّصين عندما يستلزم النشاط ذلك.",
 "视项目、司法管辖区、可行性与授权而定，XARU 可担任顾问、架构方、整合方、发起方、管理方或参与方。当业务需要时，XARU 通过获授权的实体与合作伙伴设计、整合并协调金融与技术基础设施。")

SECTION_LEAD = T("This section will be authored in Phase 2 following the common XARU pillar formula.",
                 "Esta sección se redactará en la Fase 2 siguiendo la fórmula común de página pilar de XARU.",
                 "سيُكتب هذا القسم في المرحلة 2 وفق الصيغة الموحّدة لصفحة الركيزة لدى XARU.",
                 "本栏目将在第二阶段依照 XARU 支柱页统一范式撰写。")

# ------------------------------------------------------------------ hero images per shell slug
HERO_IMG = {
 "real-estate": "07_villa_dubai.jpg",
 "real-estate/private-properties": "09_villa_como.jpg",
 "real-estate/commercial-hospitality": "05_hotel_project.jpg",
 "developments": "03_land_mega.jpg",
 "developments/land-master-developments": "22_land_parcels.jpg",
 "developments/project-structuring": "19_resort_complex.jpg",
 "capital": "13_investment_bg.jpg",
 "capital/strategic-partnerships": "15_difc_gate.jpg",
 "capital/deal-room": "23_dubai_gold_night.jpg",
 "business-infrastructure": "18_business_district.jpg",
 "business-infrastructure/trade-financial": "25_trade_port.jpg",
 "business-infrastructure/corporate-services": "26_corporate_services.jpg",
 # El hook de portada es la unica imagen generada que se conserva.
 # La cabecera de Compania pasa a fotografia real.
 "company": "30_company.jpg",
 "insights": "17_ocean_cliff.jpg",
 "opportunities/submit": "16_atlantic_aerial.jpg",
 "private-enquiry": "21_concrete_lattice.jpg",
}

# ------------------------------------------------------------------ eyebrow per door (for shell hero)
DOOR_EYEBROW = {
 "real-estate": T("Real Estate", "Inmobiliario", "العقارات", "房地产"),
 "developments": T("Developments", "Desarrollos", "التطوير", "开发项目"),
 "capital": T("Capital & Transactions", "Capital y Transacciones", "رأس المال والصفقات", "资本与交易"),
 "business-infrastructure": T("Business Infrastructure", "Infraestructura Empresarial", "البنية المؤسسية", "企业基础设施"),
 "company": T("The Company", "La Compañía", "الشركة", "公司"),
 "insights": T("Insights", "Análisis", "رؤى", "洞察"),
}

# ------------------------------------------------------------------ form pages copy
FORM_SUBMIT = {
 "title": BTN_SUBMIT,
 "eyebrow": T("Two-way intake", "Ingreso de doble vía", "استقبال ثنائي الاتجاه", "双向登记"),
 "lead": T("XARU works as a principal on both sides of the table. Tell us which side you are on.",
           "XARU actúa como principal en ambos lados de la mesa. Indíquenos en qué lado se encuentra.",
           "تعمل XARU كطرف أصيل على جانبَي الطاولة. أخبرنا في أي جانب أنت.",
           "XARU 以本人身份立于交易两端。请告知您位于哪一侧。"),
 "sideA": T("I have an asset or project and I am seeking…",
            "Tengo un activo o proyecto y busco…",
            "لديّ أصل أو مشروع وأبحث عن…", "我有资产或项目，正在寻求……"),
 "sideB": T("I have capital or capability and I am seeking…",
            "Tengo capital o capacidad y busco…",
            "لديّ رأس مال أو قدرة وأبحث عن…", "我有资本或能力，正在寻求……"),
 "seekingA": [T("Capital", "Capital", "رأس مال", "资本"),
              T("A developer", "Un desarrollador", "مطوّر", "开发商"),
              T("An operator", "Un operador", "مشغّل", "运营商"),
              T("A buyer", "Un comprador", "مشتري", "买家"),
              T("A joint-venture partner", "Un socio de joint venture", "شريك مشروع مشترك", "合资伙伴")],
 "seekingB": [T("A project to fund", "Un proyecto que financiar", "مشروع للتمويل", "可投资的项目"),
              T("Land to develop", "Suelo que desarrollar", "أرض للتطوير", "可开发的土地"),
              T("An asset to operate", "Un activo que operar", "أصل للتشغيل", "可运营的资产"),
              T("An asset to acquire", "Un activo que adquirir", "أصل للاقتناء", "可收购的资产"),
              T("A co-investment", "Una coinversión", "استثمار مشترك", "共同投资")],
 "f_name": T("Full name", "Nombre completo", "الاسم الكامل", "全名"),
 "f_email": T("Email", "Correo electrónico", "البريد الإلكتروني", "电子邮箱"),
 "f_phone": T("Phone", "Teléfono", "الهاتف", "电话"),
 "f_org": T("Company / family office", "Empresa / family office", "الشركة / المكتب العائلي", "公司 / 家族办公室"),
 "f_country": T("Country / market", "País / mercado", "الدولة / السوق", "国家 / 市场"),
 "f_ticket": T("Indicative size or ticket", "Tamaño o ticket indicativo", "الحجم أو القيمة الاسترشادية", "指示性规模或额度"),
 "f_detail": T("Describe the asset, project or capacity", "Describa el activo, proyecto o capacidad",
               "صف الأصل أو المشروع أو القدرة", "描述资产、项目或能力"),
 "f_conf": T("This enquiry is confidential", "Esta consulta es confidencial", "هذا الاستفسار سرّي", "此咨询属保密"),
 "submit": T("Submit privately", "Enviar de forma privada", "إرسال بسرّية", "保密提交"),
 "note": T("Backend integration is scheduled for Phase 6. No data is transmitted from this shell form.",
           "La integración de backend está prevista para la Fase 6. Este formulario preliminar no transmite datos.",
           "تكامل الخادم مقرّر للمرحلة 6. لا تُرسَل أي بيانات من هذا النموذج التمهيدي.",
           "后端集成计划于第六阶段完成。此初始表单不传输任何数据。"),
}

FORM_ENQUIRY = {
 "title": BTN_ENQUIRY,
 "eyebrow": T("Private desk", "Mesa privada", "المكتب الخاص", "私人服务台"),
 "lead": T("One conversation. One structure. Total confidentiality.",
           "Una conversación. Una estructura. Total confidencialidad.",
           "محادثة واحدة. بنية واحدة. سرّية تامّة.", "一次对话。单一架构。全然保密。"),
 "f_name": FORM_SUBMIT["f_name"], "f_email": FORM_SUBMIT["f_email"],
 "f_phone": FORM_SUBMIT["f_phone"], "f_country": FORM_SUBMIT["f_country"],
 "f_interest": T("Area of interest", "Área de interés", "مجال الاهتمام", "关注领域"),
 "f_message": T("How can we help?", "¿Cómo podemos ayudarle?", "كيف يمكننا مساعدتك؟", "我们能如何协助？"),
 "submit": T("Send private enquiry", "Enviar consulta privada", "إرسال استفسار خاص", "发送私人咨询"),
 "note": FORM_SUBMIT["note"],
}

# ------------------------------------------------------------------ shell registry
# Each shell: slug, label, breadcrumb parents [(label,slug)], phase tag.
def _door(slug): return next(d for d in NAV if d["slug"] == slug)

SHELLS = []
for _d in NAV:
    SHELLS.append({"slug": _d["slug"], "label": _d["label"], "intro": _d["intro"],
                   "intro_sub": _d["intro_sub"], "parents": [], "door": _d["slug"],
                   "kind": "single" if _d.get("single") else "door"})
    if not _d.get("single"):
        for _c in _d["cols"]:
            SHELLS.append({"slug": _c["slug"], "label": _c["title"], "intro": _d["intro"],
                           "intro_sub": _d["intro_sub"],
                           "parents": [(_d["label"], _d["slug"])], "door": _d["slug"],
                           "kind": "division"})

# --------------------------------------------------------- media provenance (visual bible)
# Stock may represent a CATEGORY, never a SPECIFIC asset. Rendered under every image that
# accompanies a named/priced opportunity, and under the ASHIMA block.
MEDIA_REF_NOTE = T(
 "Category reference image. Licensed stock photography \u2014 it does not depict this specific asset.",
 "Imagen de referencia de categor\u00eda. Fotograf\u00eda de stock con licencia \u2014 no corresponde a este activo concreto.",
 "\u0635\u0648\u0631\u0629 \u0645\u0631\u062c\u0639\u064a\u0629 \u0644\u0644\u0641\u0626\u0629. \u0635\u0648\u0631\u0629 \u0645\u0631\u062e\u0635\u0629 \u0645\u0646 \u0623\u0631\u0634\u064a\u0641 \u0645\u0635\u0648\u0651\u0631 \u2014 \u0644\u0627 \u062a\u0645\u062b\u0644 \u0647\u0630\u0627 \u0627\u0644\u0623\u0635\u0644 \u0628\u0639\u064a\u0646\u0647.",
 "\u7c7b\u522b\u53c2\u8003\u56fe\u7247\u3002\u5df2\u6388\u6743\u56fe\u5e93\u6444\u5f71\u4f5c\u54c1\uff0c\u5e76\u975e\u8be5\u5177\u4f53\u8d44\u4ea7\u7684\u5b9e\u62cd\u3002")

MEDIA_GEO_NOTE = T(
 "Illustrative image \u2014 geographic and environmental reference of the region. It does not depict the project as built.",
 "Imagen ilustrativa \u2014 referencia geogr\u00e1fica y ambiental de la regi\u00f3n. No representa el proyecto construido.",
 "\u0635\u0648\u0631\u0629 \u062a\u0648\u0636\u064a\u062d\u064a\u0629 \u2014 \u0645\u0631\u062c\u0639 \u062c\u063a\u0631\u0627\u0641\u064a \u0648\u0628\u064a\u0626\u064a \u0644\u0644\u0645\u0646\u0637\u0642\u0629. \u0644\u0627 \u062a\u0645\u062b\u0644 \u0627\u0644\u0645\u0634\u0631\u0648\u0639 \u0645\u064f\u0646\u0641\u0651\u0630\u064b\u0627.",
 "\u793a\u610f\u56fe\u7247 \u2014 \u8be5\u533a\u57df\u7684\u5730\u7406\u4e0e\u73af\u5883\u53c2\u8003\uff0c\u4e0d\u4ee3\u8868\u9879\u76ee\u5efa\u6210\u540e\u7684\u5b9e\u666f\u3002")
