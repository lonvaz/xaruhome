# -*- coding: utf-8 -*-
"""XARU HOME — Phase 2 copy & data (single source of truth for the property core).
Real pillar copy (Real Estate · Commercial & Hospitality · Land & Master
Developments), homepage 12-block copy, catalog filter labels and ficha field
labels — all in EN/ES/AR/ZH. Consumed by gen_i18n.py. No design tokens here.
Brand names (XARU, ASHIMA, NEXARU GLOBAL) never translated. "Price upon
application". Western figures. [PHASE 0] marks data pending from Josep (§12)."""

def T(en, es, ar, zh):
    return {"en": en, "es": es, "ar": ar, "zh": zh}

# El rotulo se veia tal cual en la web publica: "[PHASE 0]" no le dice nada
# a quien visita el sitio, solo suena a obra sin terminar. Se mantiene la
# honestidad del dato pendiente, se retira la jerga interna.
PHASE0 = T("To be confirmed", "Pendiente de confirmación",
           "قيد التأكيد", "待确认")

# ================================================================ shared UI labels
UI = {
 "enquire":       T("Enquire", "Consultar", "استفسار", "咨询"),
 "view_details":  T("View details", "Ver ficha", "عرض التفاصيل", "查看详情"),
 "request_access":T("Request access", "Solicitar acceso", "طلب وصول", "申请访问"),
 "explore_assets":T("Explore assets", "Explorar activos", "استكشف الأصول", "浏览资产"),
 "present_opp":   T("Present an opportunity", "Presentar una oportunidad", "قدّم فرصة", "提交机会"),
 "view_catalog":  T("View the full catalogue", "Ver el catálogo completo", "عرض الكتالوج الكامل", "查看完整目录"),
 "view_division": T("View division", "Ver división", "عرض القسم", "查看板块"),
 "back_catalog":  T("Back to catalogue", "Volver al catálogo", "العودة إلى الكتالوج", "返回目录"),
 "status":        T("Status", "Estado", "الحالة", "状态"),
 "filters":       T("Filter opportunities", "Filtrar oportunidades", "تصفية الفرص", "筛选机会"),
 "all":           T("All", "Todos", "الكل", "全部"),
 "reset":         T("Reset", "Restablecer", "إعادة ضبط", "重置"),
 "showing":       T("Showing", "Mostrando", "عرض", "显示"),
 "of":            T("of", "de", "من", "共"),
 "results":       T("opportunities", "oportunidades", "فرص", "个机会"),
 "no_results":    T("No opportunities match these filters.", "Ninguna oportunidad coincide con estos filtros.",
                    "لا توجد فرص مطابقة لهذه المرشّحات.", "没有符合这些筛选条件的机会。"),
 "poa":           T("Price upon application", "Precio a consultar", "السعر عند الطلب", "价格面议"),
 "enquire_priv":  T("Enquire privately", "Consultar en privado", "استفسار خاص", "私下咨询"),
 "key_facts":     T("Key facts", "Datos clave", "الحقائق الأساسية", "关键信息"),
 "overview":      T("Overview", "Descripción", "نظرة عامة", "概览"),
 "nda_line":      T("Information available under NDA", "Información disponible bajo NDA",
                    "المعلومات متاحة بموجب اتفاقية سرية", "信息在保密协议下提供"),
 "deal_room":     T("Private Deal Room process", "Proceso de la Sala de Operaciones Privada",
                    "مسار غرفة الصفقات الخاصة", "私人交易室流程"),
 "verified_mandate": T("Verified mandate", "Mandato verificado", "تفويض موثّق", "已核实委托"),
}

# ================================================================ ficha field labels
FICHA = {
 "location":     T("Location", "Ubicación", "الموقع", "位置"),
 "price":        T("Price", "Precio", "السعر", "价格"),
 "bedrooms":     T("Bedrooms", "Habitaciones", "غرف النوم", "卧室"),
 "bathrooms":    T("Bathrooms", "Baños", "الحمّامات", "浴室"),
 "built":        T("Built area", "Superficie construida", "المساحة المبنية", "建筑面积"),
 "plot":         T("Plot area", "Superficie de parcela", "مساحة القطعة", "地块面积"),
 "style":        T("Style", "Estilo", "الطراز", "风格"),
 "operating":    T("Operating state", "Estado operativo", "الحالة التشغيلية", "运营状态"),
 "keys":         T("Keys", "Llaves", "المفاتيح", "客房数"),
 "occupancy":    T("Occupancy (teaser)", "Ocupación (avance)", "الإشغال (موجز)", "入住率（简报）"),
 "noi":          T("NOI (teaser)", "NOI (avance)", "صافي الدخل التشغيلي (موجز)", "净营业收入（简报）"),
 "operator":     T("Operator", "Operador", "المشغّل", "运营商"),
 "structure":    T("Structure", "Estructura", "الهيكل", "结构"),
 "ticket":       T("Indicative ticket", "Ticket indicativo", "القيمة الاسترشادية", "指示性额度"),
 "area":         T("Area", "Superficie", "المساحة", "面积"),
 "tenure":       T("Tenure", "Tenencia", "الحيازة", "权属"),
 "current_use":  T("Current use", "Uso actual", "الاستخدام الحالي", "现状用途"),
 "projected_use":T("Projected use", "Uso proyectado", "الاستخدام المتوقّع", "规划用途"),
 "access":       T("Access", "Acceso", "الوصول", "交通"),
 "water":        T("Water", "Agua", "المياه", "水资源"),
 "environmental":T("Environmental", "Ambiental", "البيئية", "环境"),
 "planning":     T("Planning", "Urbanístico", "التخطيط", "规划"),
 "permits":      T("Permits", "Permisos", "التصاريح", "许可"),
 "phase":        T("Phase", "Fase", "المرحلة", "阶段"),
 "counterparty": T("Counterparty sought", "Contraparte buscada", "الطرف المقابل المطلوب", "所寻对手方"),
 "capital_req":  T("Capital required", "Capital requerido", "رأس المال المطلوب", "所需资本"),
 "region":       T("Region", "Región", "المنطقة", "地区"),
 "category":     T("Category", "Categoría", "الفئة", "类别"),
 "scale":        T("Scale", "Escala", "النطاق", "规模"),
 "opp_type":     T("Opportunity type", "Tipo de oportunidad", "نوع الفرصة", "机会类型"),
}

COUNTERPARTY = {
 "developer": T("Developer", "Desarrollador", "مطوّر", "开发商"),
 "capital":   T("Capital", "Capital", "رأس مال", "资本"),
 "operator":  T("Operator", "Operador", "مشغّل", "运营商"),
 "buyer":     T("Buyer", "Comprador", "مشترٍ", "买家"),
}

# ================================================================ catalog headers + facets
CATALOG = {
 "private-properties": {
   "eyebrow": T("Real Estate", "Inmobiliario", "العقارات", "房地产"),
   "title": T("Private Properties", "Propiedades Privadas", "العقارات الخاصة", "私人房产"),
   "lead": T("Villas, mansions, estates, castles, private islands and branded residences — curated worldwide and held to a single standard.",
            "Villas, mansiones, fincas, castillos, islas privadas y residencias de marca — seleccionadas en todo el mundo bajo un solo estándar.",
            "فيلات وقصور وحوزات وقلاع وجزر خاصة ومساكن ذات علامات — منتقاة حول العالم وفق معيار واحد.",
            "别墅、豪宅、庄园、城堡、私人岛屿与品牌住宅——甄选全球，恪守统一标准。"),
   "facets": ["location", "lifestyle", "bedrooms"],
 },
 "commercial-hospitality": {
   "eyebrow": T("Real Estate", "Inmobiliario", "العقارات", "房地产"),
   "title": T("Commercial & Hospitality", "Comercial y Hostelería", "التجاري والضيافة", "商业与酒店"),
   "lead": T("Operating hotels, resorts and income-producing assets — presented with their operating state, never as static listings.",
            "Hoteles en operación, resorts y activos de renta — presentados con su estado operativo, nunca como fichas estáticas.",
            "فنادق تشغيلية ومنتجعات وأصول مدرّة للدخل — تُعرض بحالتها التشغيلية، لا كقوائم جامدة.",
            "运营中的酒店、度假村与收益型资产——以其运营状态呈现，而非静态清单。"),
   "facets": ["region", "operating", "structure"],
 },
 "land-projects": {
   "eyebrow": T("Developments", "Desarrollos", "التطوير", "开发项目"),
   "title": T("Land, Projects & Opportunities", "Suelo, Proyectos y Oportunidades", "الأراضي والمشاريع والفرص", "土地、项目与机会"),
   "lead": T("Territorial land, master plans, halted projects and capital opportunities — measured in kilometres, phases and mandates, not meters.",
            "Suelo territorial, master plans, proyectos detenidos y oportunidades de capital — medidos en kilómetros, fases y mandatos, no en metros.",
            "أراضٍ إقليمية ومخططات عامة ومشاريع متوقفة وفرص رأسمالية — تُقاس بالكيلومترات والمراحل والتفويضات، لا بالأمتار.",
            "区域性土地、总体规划、停滞项目与资本机会——以公里、阶段与委托衡量，而非平米。"),
   "facets": ["region", "phase", "opp_type"],
 },
}

FACET_LABEL = {
 "location": FICHA["location"], "region": FICHA["region"], "lifestyle": T("Lifestyle","Estilo de vida","نمط الحياة","生活方式"),
 "bedrooms": FICHA["bedrooms"], "operating": FICHA["operating"], "structure": FICHA["structure"],
 "phase": FICHA["phase"], "opp_type": FICHA["opp_type"],
}

# ================================================================ homepage — 12 blocks
HOME = {
 "hero_eyebrow": "GLOBAL REAL ESTATE  ·  DEVELOPMENT  ·  CAPITAL  ·  BUSINESS INFRASTRUCTURE",

 # Block 2 — journey selector
 "journey_eyebrow": T("Your route", "Su recorrido", "مسارك", "您的路径"),
 "journey_title": T("What brings you to XARU?", "¿Qué le trae a XARU?", "ما الذي أتى بك إلى XARU؟", "您为何来到 XARU？"),
 "journey": [
   (T("I'm looking for a property", "Busco una propiedad", "أبحث عن عقار", "我在寻找房产"), "real-estate/private-properties/"),
   (T("I want to sell an asset", "Quiero vender un activo", "أريد بيع أصل", "我想出售资产"), "opportunities/submit/"),
   (T("I have a project", "Tengo un proyecto", "لديّ مشروع", "我有一个项目"), "developments/project-structuring/"),
   (T("I'm seeking capital or partners", "Busco capital o socios", "أبحث عن رأس مال أو شركاء", "我在寻求资本或合作伙伴"), "capital/strategic-partnerships/"),
   (T("I want to invest", "Quiero invertir", "أريد الاستثمار", "我想投资"), "opportunities/"),
   (T("I need to establish internationally", "Necesito establecerme internacionalmente", "أحتاج إلى التأسيس دولياً", "我需要国际化落地"), "business-infrastructure/corporate-services/"),
   # Anadidos 1-ago-2026: los seis caminos originales solo abrian puertas
   # inmobiliarias y de capital. Hosteleria, suelo, materias primas y la sala
   # de operaciones no tenian entrada, y son casa igual que el ladrillo.
   (T("I operate a hotel or resort", "Opero un hotel o un resort", "أدير فندقاً أو منتجعاً", "我经营酒店或度假村"), "real-estate/commercial-hospitality/"),
   (T("I hold land or a master plan", "Tengo suelo o un plan maestro", "لديّ أرض أو مخطط عام", "我持有土地或总体规划"), "developments/land-master-developments/"),
   (T("I trade commodities", "Comercializo materias primas", "أتاجر في السلع", "我从事大宗商品贸易"), "business-infrastructure/trade-financial/"),
   (T("I want access to the deal room", "Quiero acceso a la sala de operaciones", "أريد الدخول إلى غرفة الصفقات", "我想进入交易室"), "capital/deal-room/"),
 ],

 # Block 3 — the six operating divisions
 # Decia "Tres mercados inmobiliarios": reducia toda la casa al ladrillo y
 # dejaba fuera comercio, capital, infraestructura y establecimiento.
 "markets_eyebrow": T("Six operating divisions", "Seis divisiones operativas", "ست وحدات تشغيلية", "六大业务板块"),
 "markets_title": T("Where would you like to begin?", "¿Por dónde desea empezar?", "من أين تودّ أن تبدأ؟", "您想从何处开始？"),
 "markets": [
   (T("Private Real Estate", "Inmobiliario Privado", "العقارات الخاصة", "私人房产"),
    T("Villas, estates, castles, private islands and branded residences.",
      "Villas, fincas, castillos, islas privadas y residencias de marca.",
      "فيلات وحوزات وقلاع وجزر خاصة ومساكن ذات علامات.",
      "别墅、庄园、城堡、私人岛屿与品牌住宅。"),
    "real-estate/private-properties/", "07_villa_dubai.jpg"),
   (T("Commercial & Hospitality", "Comercial y Hostelería", "التجاري والضيافة", "商业与酒店"),
    T("Operating hotels, resorts and income assets — presented with their P&L state.",
      "Hoteles en operación, resorts y activos de renta — presentados con su estado de P&L.",
      "فنادق تشغيلية ومنتجعات وأصول دخل — تُعرض بحالة الأرباح والخسائر.",
      "运营中的酒店、度假村与收益资产——附带其损益状态。"),
    "real-estate/commercial-hospitality/", "05_hotel_project.jpg"),
   (T("Land & Master Developments", "Suelo y Desarrollos Maestros", "الأراضي والتطويرات الكبرى", "土地与总体开发"),
    T("Territorial land, master plans and signature destinations at scale.",
      "Suelo territorial, master plans y destinos emblemáticos a escala.",
      "أراضٍ إقليمية ومخططات عامة ووجهات مميّزة على نطاق واسع.",
      "区域性土地、总体规划与大规模标志性目的地。"),
    "developments/land-master-developments/", "06_masterplan_ashima.jpg"),
   (T("Capital & Transactions", "Capital y Transacciones", "رأس المال والمعاملات", "资本与交易"),
    T("Capital, strategic partners and a private deal room for verified mandates.",
      "Capital, socios estratégicos y una sala de operaciones reservada para mandatos verificados.",
      "رأس مال وشركاء استراتيجيون وغرفة صفقات خاصة للتفويضات الموثّقة.",
      "资本、战略伙伴，以及面向已核验委托的私人交易室。"),
    "capital/strategic-partnerships/", "24_capital_district.jpg"),
   (T("Trade & Financial Infrastructure", "Comercio e Infraestructura Financiera", "التجارة والبنية المالية", "贸易与金融基础设施"),
    T("Commodities, mining and quarries, offtake and placement, payment rails and financial platforms.",
      "Commodities, minería y canteras, offtake y colocación, infraestructura de pagos y plataformas financieras.",
      "السلع والتعدين والمحاجر، الشراء والتصريف، بنية المدفوعات والمنصات المالية.",
      "大宗商品、矿业与采石、承购与配售、支付通道与金融平台。"),
    "business-infrastructure/trade-financial/", "25_trade_port.jpg"),
   (T("Corporate Services & Relocation", "Servicios Corporativos y Relocalización", "الخدمات المؤسسية والانتقال", "企业服务与迁移"),
    T("Entities, compliance, banking, residence — the structure behind an operating presence.",
      "Entidades, cumplimiento, banca, residencia — la estructura detrás de una presencia operativa.",
      "الكيانات والامتثال والخدمات المصرفية والإقامة — البنية خلف الحضور التشغيلي.",
      "实体、合规、银行、居留——运营存在背后的架构。"),
    "business-infrastructure/corporate-services/", "26_corporate_services.jpg"),
 ],

 # Block 4 — featured opportunities (tabs render from opportunities.json)
 "featured_eyebrow": T("Live mandates", "Mandatos activos", "تفويضات نشطة", "在册委托"),
 "featured_title": T("Featured Opportunities", "Oportunidades Destacadas", "الفرص المميّزة", "精选机会"),
 "tabs": [
   ("private",  T("Private", "Privado", "خاص", "私人")),
   ("commercial", T("Commercial", "Comercial", "تجاري", "商业")),
   ("land",     T("Land", "Suelo", "أراضٍ", "土地")),
   ("projects", T("Projects", "Proyectos", "مشاريع", "项目")),
   ("private-market", T("Private Market", "Mercado Privado", "السوق الخاص", "私人市场")),
 ],

 # Block 5 — beyond intermediation
 "cap_eyebrow": T("Beyond intermediation", "Más allá de la intermediación", "أبعد من الوساطة", "超越中介"),
 "cap_title": T("One structure, end to end", "Una sola estructura, de principio a fin", "بنية واحدة، من البداية إلى النهاية", "单一架构，贯穿始终"),
 "capability": [
   (T("Acquire", "Adquirir", "الاقتناء", "收购"), T("Sourcing and acquisition under mandate.", "Búsqueda y adquisición por mandato.", "التوريد والاقتناء بالتفويض.", "受托寻源与收购。")),
   (T("Structure", "Estructurar", "الهيكلة", "架构"), T("Legal, fiduciary and SPV structuring.", "Estructuración jurídica, fiduciaria y de SPV.", "الهيكلة القانونية والائتمانية وSPV.", "法律、信托与SPV架构。")),
   (T("Finance", "Financiar", "التمويل", "融资"), T("Capital matched through regulated channels.", "Capital conectado por canales regulados.", "رأس مال عبر قنوات منظّمة.", "通过受监管渠道对接资本。")),
   (T("Develop", "Desarrollar", "التطوير", "开发"), T("Master plan to delivery.", "Del master plan a la entrega.", "من المخطط العام إلى التسليم.", "从总体规划到交付。")),
   (T("Operate", "Operar", "التشغيل", "运营"), T("Operator selection and asset management.", "Selección de operador y gestión de activos.", "اختيار المشغّل وإدارة الأصول.", "运营商遴选与资产管理。")),
   (T("Expand", "Expandir", "التوسّع", "拓展"), T("Corporate infrastructure and relocation.", "Infraestructura corporativa y relocalización.", "البنية المؤسسية والانتقال.", "企业基础设施与迁居。")),
 ],

 # Block 6 — projects & capital dual-track
 "dual_eyebrow": T("Projects & capital", "Proyectos y capital", "المشاريع ورأس المال", "项目与资本"),
 "dual_title": T("A two-way structure", "Una estructura de doble vía", "بنية ثنائية الاتجاه", "双向架构"),
 "dual_lead": T("XARU acts as principal on both sides of the table — matching projects that seek capital with capital that seeks projects, under its own diligence.",
               "XARU actúa como principal en ambos lados de la mesa — uniendo proyectos que buscan capital con capital que busca proyectos, bajo su propia diligencia.",
               "تعمل XARU كطرف أصيل على جانبَي الطاولة — تربط المشاريع الباحثة عن رأس المال برأس المال الباحث عن مشاريع، وفق عنايتها الخاصة.",
               "XARU 以本人身份立于交易两端——以自身尽调，将寻求资本的项目与寻求项目的资本对接。"),
 "dual_a": (T("Present a project", "Presentar un proyecto", "قدّم مشروعاً", "提交项目"), "opportunities/submit/"),
 "dual_b": (T("Deploy capital", "Desplegar capital", "استثمار رأس المال", "配置资本"), "capital/strategic-partnerships/"),

 # Block 7 — ASHIMA facets (added strip; existing visual section kept)
 "ashima_eyebrow": T("Signature case", "Caso emblemático", "الحالة المميّزة", "标志案例"),
 "ashima_title": T("ASHIMA — a territory becoming a destination", "ASHIMA — un territorio que se vuelve destino",
                   "ASHIMA — أرضٌ تتحوّل إلى وجهة", "ASHIMA——从疆域到目的地"),
 "ashima_facets": [
   (T("Vision", "Visión", "الرؤية", "愿景"), T("Health, culture, eco, innovation, sustainability.", "Salud, cultura, eco, innovación, sostenibilidad.", "الصحة والثقافة والبيئة والابتكار والاستدامة.", "健康、文化、生态、创新、可持续。")),
   (T("Scale", "Escala", "النطاق", "规模"), T("A master development measured in millions of m².", "Un desarrollo maestro medido en millones de m².", "تطوير رئيسي يُقاس بملايين الأمتار المربّعة.", "以数百万平方米衡量的总体开发。")),
   (T("Territorial model", "Modelo territorial", "النموذج الإقليمي", "territorial模型"), T("Land held and planned as a single thesis.", "Suelo mantenido y planificado como una sola tesis.", "أرض محفوظة ومخططة كأطروحة واحدة.", "作为单一论点持有与规划的土地。")),
   (T("Governance", "Gobernanza", "الحوكمة", "治理"), T("Standards and oversight from the outset.", "Estándares y supervisión desde el inicio.", "معايير ورقابة منذ البداية.", "自始即设标准与监督。")),
   (T("Structuring", "Estructuración", "الهيكلة", "架构"), T("Vehicles, feasibility and capital design.", "Vehículos, viabilidad y diseño de capital.", "الكيانات والجدوى وتصميم رأس المال.", "载体、可行性与资本设计。")),
   (T("Phasing", "Fases", "المراحل", "分期"), T("Sequenced delivery, phase by phase.", "Entrega secuenciada, fase a fase.", "تسليم متسلسل، مرحلة تلو الأخرى.", "分期有序交付。")),
   (T("Execution", "Ejecución", "التنفيذ", "执行"), T("Development management to operation.", "Gestión de desarrollo hasta la operación.", "إدارة التطوير حتى التشغيل.", "从开发管理到运营。")),
 ],

 # Block 8 — business infrastructure (max 4 cards)
 "infra_eyebrow": T("Business infrastructure", "Infraestructura empresarial", "البنية المؤسسية", "企业基础设施"),
 "infra_title": T("The infrastructure behind ownership", "La infraestructura detrás de la propiedad", "البنية التي تسند التملّك", "支撑持有的基础设施"),
 "infra": [
   (T("Corporate Services", "Servicios Corporativos", "الخدمات المؤسسية", "企业服务"),
    T("Company formation, governance and ongoing administration.", "Constitución, gobierno y administración continua.", "التأسيس والحوكمة والإدارة المستمرة.", "公司设立、治理与持续行政。"),
    "business-infrastructure/corporate-services/"),
   (T("Compliance & Governance", "Cumplimiento y Gobernanza", "الامتثال والحوكمة", "合规与治理"),
    T("AML, due diligence and corporate standards through regulated channels.", "AML, due diligence y estándares corporativos por canales regulados.", "مكافحة الغسل والعناية الواجبة والمعايير عبر قنوات منظّمة.", "反洗钱、尽调与合规——通过受监管渠道。"),
    "business-infrastructure/corporate-services/"),
   (T("Financial Infrastructure", "Infraestructura Financiera", "البنية المالية", "金融基础设施"),
    T("Payments and platforms designed with authorised entities and partners.", "Pagos y plataformas diseñados con entidades y partners autorizados.", "مدفوعات ومنصّات تُصمَّم مع كيانات وشركاء مرخّصين.", "与获授权实体及伙伴共建的支付与平台。"),
    "business-infrastructure/trade-financial/"),
   (T("Trade & Relocation", "Comercio y Relocalización", "التجارة والانتقال", "贸易与迁居"),
    T("Commodities, distribution, migration and family relocation.", "Commodities, distribución, migración y relocalización familiar.", "السلع والتوزيع والهجرة وانتقال العائلة.", "大宗商品、分销、移民与家庭迁居。"),
    "business-infrastructure/trade-financial/"),
 ],

 # Block 9 — real presence
 "presence_eyebrow": T("Real presence", "Presencia real", "حضور حقيقي", "真实存在"),
 "presence_title": T("Capability, demonstrated — not declared", "Capacidad demostrada, no declarada", "قدرة تُبرهَن لا تُعلَن", "以行动证明能力，而非声称"),
 "presence_lead": T("XARU HOME operates as a NEXARU GLOBAL brand, licensed in the United Arab Emirates, with capabilities delivered directly or through authorised entities and partners.",
                    "XARU HOME opera como marca de NEXARU GLOBAL, con licencia en los Emiratos Árabes Unidos, con capacidades prestadas directamente o a través de entidades y partners autorizados.",
                    "تعمل XARU HOME كعلامة من NEXARU GLOBAL، مرخّصة في الإمارات العربية المتحدة، بقدرات تُقدَّم مباشرةً أو عبر كيانات وشركاء مرخّصين.",
                    "XARU HOME 作为 NEXARU GLOBAL 旗下品牌运营，持有阿联酋牌照，能力由自身或获授权实体与合作伙伴交付。"),
 "presence_items": [
   (T("Offices", "Oficinas", "المكاتب", "办公网络"), T("Confirmed markets published on the Company page.", "Mercados confirmados publicados en la página de Compañía.", "أسواق مؤكّدة تُنشر في صفحة الشركة.", "已确认市场发布于公司页面。")),
   (T("Entities & scope", "Entidades y alcance", "الكيانات والنطاق", "实体与范围"), T("Licensed brand under NEXARU GLOBAL.", "Marca con licencia bajo NEXARU GLOBAL.", "علامة مرخّصة تحت NEXARU GLOBAL.", "NEXARU GLOBAL 旗下持牌品牌。")),
   (T("Active markets", "Mercados activos", "الأسواق النشطة", "活跃市场"), T("Europe, the Americas, the Gulf and Asia.", "Europa, las Américas, el Golfo y Asia.", "أوروبا والأمريكتان والخليج وآسيا.", "欧洲、美洲、海湾地区与亚洲。")),
   (T("Team & network", "Equipo y red", "الفريق والشبكة", "团队与网络"), T("Roles and international network — figures published once verified.", "Roles y red internacional — cifras publicadas una vez verificadas.", "الأدوار والشبكة الدولية — تُنشر الأرقام بعد التحقق.", "岗位与国际网络——数字经核实后公布。")),
 ],

 # Block 10 — governance & trust
 "gov_eyebrow": T("Governance & trust", "Gobierno y confianza", "الحوكمة والثقة", "治理与信任"),
 "gov_title": T("Power is demonstrated, not declared", "El poder se demuestra, no se declara", "القوة تُبرهَن لا تُعلَن", "实力以行动证明，而非声称"),
 "gov_items": [
   T("Confidentiality and information protection", "Confidencialidad y protección de la información", "السرّية وحماية المعلومات", "保密与信息保护"),
   T("Due diligence and verified mandates", "Due diligence y mandatos verificados", "العناية الواجبة والتفويضات الموثّقة", "尽职调查与已核实委托"),
   T("AML / compliance through regulated channels", "AML / cumplimiento por canales regulados", "مكافحة الغسل / الامتثال عبر قنوات منظّمة", "反洗钱／通过受监管渠道合规"),
   T("Legal and tax coordination", "Coordinación legal y fiscal", "التنسيق القانوني والضريبي", "法律与税务协调"),
 ],

 # Block 11 — insights
 "ins_eyebrow": T("Insights", "Análisis", "رؤى", "洞察"),
 "ins_title": T("Perspective, by sector", "Perspectiva, por sector", "رؤى بحسب القطاع", "分门别类的洞见"),

 # Block 12 — private desk
 "desk_eyebrow": T("Private Desk", "Mesa Privada", "المكتب الخاص", "私人服务台"),
 "desk_title": T("One conversation. One structure. Total confidentiality.",
                 "Una conversación. Una estructura. Total confidencialidad.",
                 "محادثة واحدة. بنية واحدة. سرّية تامّة.", "一次对话。单一架构。全然保密。"),
 "desk_cta": T("Speak with the Private Desk", "Hablar con la Mesa Privada", "تحدّث مع المكتب الخاص", "联系私人服务台"),
}

# ================================================================ pillar copy (3 pillars)
# Section keys map to ARCH.PILLAR_SECTIONS (01..12). 12 is the generic CTA.
def _P(**k): return k

PILLARS = {
 # ---------------------------------------------------------------- Real Estate (door)
 "real-estate": {
  "01": _P(p=[T(
    "XARU HOME is an international real-estate structure. Under a single responsibility it advises on, brokers and structures exceptional private property and operating hospitality assets — from the search itself to acquisition, structuring and, where required, development and operation.",
    "XARU HOME es una estructura inmobiliaria internacional. Bajo una sola responsabilidad asesora, intermedia y estructura propiedades privadas excepcionales y activos hoteleros en operación — desde la búsqueda hasta la adquisición, la estructuración y, cuando procede, el desarrollo y la operación.",
    "XARU HOME بنية عقارية دولية. تحت مسؤولية واحدة تقدّم المشورة والوساطة والهيكلة لعقارات خاصة استثنائية وأصول ضيافة تشغيلية — من البحث ذاته إلى الاقتناء والهيكلة، وعند اللزوم التطوير والتشغيل.",
    "XARU HOME 是一个国际房地产架构。在单一责任下，为卓越的私人房产与运营中的酒店资产提供咨询、中介与架构——从寻源本身到收购、架构，并在需要时进行开发与运营。")]),
  "02": _P(p=[T("XARU serves those for whom property is both a home and a position.",
                "XARU sirve a quienes la propiedad es a la vez un hogar y una posición.",
                "تخدم XARU من تكون العقارات لديهم مسكناً وموقعاً في آنٍ واحد.",
                "XARU 服务于视房产既为家园亦为资产配置的客户。")],
           list=[T("Private clients and families", "Clientes privados y familias", "العملاء الخاصّون والعائلات", "私人客户与家族"),
                 T("Owners seeking a discreet sale", "Propietarios que buscan una venta discreta", "ملّاك يبحثون عن بيع متحفّظ", "寻求低调出售的业主"),
                 T("Investors and family offices", "Inversionistas y family offices", "المستثمرون والمكاتب العائلية", "投资者与家族办公室"),
                 T("Companies establishing a footprint", "Compañías que establecen presencia", "شركات تؤسّس حضوراً", "拓展布局的企业")]),
  "03": _P(p=[T("Assets and needs handled across the private market.", "Activos y necesidades atendidos en el mercado privado.", "أصول واحتياجات نتناولها عبر السوق الخاص.", "涵盖私人市场的资产与需求。")],
           list=[T("Villas, mansions and estates", "Villas, mansiones y fincas", "الفيلات والقصور والحوزات", "别墅、豪宅与庄园"),
                 T("Castles, haciendas and historic properties", "Castillos, haciendas y propiedades históricas", "القلاع والضياع والعقارات التاريخية", "城堡、庄园与历史建筑"),
                 T("Private islands and one-of-one trophies", "Islas privadas y trofeos one-of-one", "الجزر الخاصة والأصول الفريدة", "私人岛屿与独一无二的珍稀资产"),
                 T("Branded residences and new residential", "Residencias de marca y residencial nuevo", "المساكن ذات العلامات والسكني الجديد", "品牌住宅与全新住宅"),
                 T("Private search by mandate", "Búsqueda privada por mandato", "بحث خاص بالتفويض", "受托私人寻购")]),
  "04": _P(p=[T("XARU sources, verifies, structures and closes — coordinating every specialist the transaction requires under one point of responsibility.",
                "XARU busca, verifica, estructura y cierra — coordinando a cada especialista que la operación requiere bajo un solo punto de responsabilidad.",
                "تبحث XARU وتتحقّق وتُهيكل وتُنجز — بتنسيق كل مختص تتطلبه الصفقة تحت نقطة مسؤولية واحدة.",
                "XARU 寻源、核实、架构并成交——在单一责任点下协调交易所需的每一位专家。")]),
  "05": _P(p=[T("What XARU does not do.", "Qué NO hace XARU.", "ما لا تقوم به XARU.", "XARU 不做的事。")],
           list=[T("Publish as “available” what is still being validated", "Publicar como «disponible» lo que aún se valida", "نشر ما يزال قيد التحقّق بوصفه «متاحاً»", "把仍在验证中的资产标为“可售”"),
                 T("Disclose owners, coordinates or sensitive price without mandate", "Revelar propietarios, coordenadas o precio sensible sin mandato", "الكشف عن الملّاك أو الإحداثيات أو السعر الحسّاس دون تفويض", "未经委托披露业主、坐标或敏感价格"),
                 T("Make regulatory claims it cannot substantiate", "Hacer afirmaciones regulatorias que no puede respaldar", "تقديم ادعاءات تنظيمية لا يمكن إثباتها", "作出无法证实的监管主张")]),
  "06": _P(steps=[T("Private brief and mandate", "Brief privado y mandato", "موجز خاص وتفويض", "私密简报与委托"),
                  T("Sourcing and verification", "Búsqueda y verificación", "التوريد والتحقّق", "寻源与核实"),
                  T("Structuring and due diligence", "Estructuración y due diligence", "الهيكلة والعناية الواجبة", "架构与尽职调查"),
                  T("Negotiation and closing", "Negociación y cierre", "التفاوض والإنجاز", "谈判与成交"),
                  T("Post-completion and continuity", "Post-cierre y continuidad", "ما بعد الإنجاز والاستمرارية", "成交后与延续")]),
  "07": _P(p=[T("XARU works on a curated basis; admission protects both sides.", "XARU trabaja de forma seleccionada; la admisión protege a ambas partes.", "تعمل XARU على أساس منتقى؛ القبول يحمي الطرفين.", "XARU 以甄选方式合作；准入保护双方。")],
           list=[T("Verified ownership or verified purchasing capacity", "Titularidad verificada o capacidad de compra verificada", "ملكية موثّقة أو قدرة شرائية موثّقة", "已核实的所有权或购买能力"),
                 T("A clear mandate and realistic expectations", "Un mandato claro y expectativas realistas", "تفويض واضح وتوقعات واقعية", "明确委托与合理预期"),
                 T("Willingness to complete KYC where required", "Disposición a completar KYC cuando corresponda", "الاستعداد لاستكمال اعرف عميلك عند اللزوم", "在需要时愿意完成 KYC")]),
  "08": _P(p=[T("Internal capability, extended by an authorised network.", "Capacidad interna, ampliada por una red autorizada.", "قدرة داخلية تمتدّ عبر شبكة مرخّصة.", "内部能力，辅以获授权网络。")],
           list=[T("In-house sourcing, structuring and transaction management", "Búsqueda, estructuración y gestión de operaciones propias", "توريد وهيكلة وإدارة صفقات داخلية", "自有寻源、架构与交易管理"),
                 T("Legal, fiduciary and tax coordination", "Coordinación legal, fiduciaria y fiscal", "التنسيق القانوني والائتماني والضريبي", "法律、信托与税务协调"),
                 T("Banking, compliance and relocation partners", "Partners de banca, cumplimiento y relocalización", "شركاء مصرفيون وامتثال وانتقال", "银行、合规与迁居合作伙伴")]),
  "09": _P(p=[T("A family acquires a lakefront estate off-market: XARU verifies title, structures the holding vehicle, coordinates tax and banking, and manages the closing — one team, one line of responsibility.",
                "Una familia adquiere una finca junto al lago fuera de mercado: XARU verifica el título, estructura el vehículo de tenencia, coordina fiscalidad y banca, y gestiona el cierre — un solo equipo, una sola línea de responsabilidad.",
                "تقتني عائلة حوزة على البحيرة خارج السوق: تتحقّق XARU من السند، وتُهيكل كيان التملّك، وتنسّق الضرائب والبنوك، وتدير الإنجاز — فريق واحد وخط مسؤولية واحد.",
                "一个家族在场外收购一处湖畔庄园：XARU 核实产权、搭建持有载体、协调税务与银行并管理成交——一个团队，一条责任线。")]),
  "10": _P(p=[T("Every mandate is governed by confidentiality, due diligence and defined scope.", "Cada mandato se rige por confidencialidad, due diligence y un alcance definido.", "يخضع كل تفويض للسرّية والعناية الواجبة ونطاق محدّد.", "每项委托均受保密、尽调与既定范围约束。")]),
  "11": _P(faq=[
    (T("Do you publish prices?", "¿Publican precios?", "هل تنشرون الأسعار؟", "你们公布价格吗？"),
     T("Where discretion applies, price is available upon application.", "Cuando aplica la discreción, el precio se facilita a consulta.", "حيث تنطبق السرّية، يُتاح السعر عند الطلب.", "在需要保密时，价格面议。")),
    (T("Can a sale stay off-market?", "¿Una venta puede permanecer off-market?", "هل يمكن أن يبقى البيع خارج السوق؟", "出售可以保持非公开吗？"),
     T("Yes. Off-market and confidential mandates are a core part of our work.", "Sí. Los mandatos off-market y confidenciales son parte central de nuestro trabajo.", "نعم. التفويضات خارج السوق والسرّية جزء أساسي من عملنا.", "可以。非公开与保密委托是我们工作的核心。")),
   ]),
 },

 # ---------------------------------------------------------------- Commercial & Hospitality (division)
 "real-estate/commercial-hospitality": {
  "01": _P(p=[T(
    "XARU HOME structures and transacts operating hospitality and income-producing commercial real estate. We present assets by their operating reality — occupancy, structure and state — not as static listings, and we can act across the full lifecycle of an asset.",
    "XARU HOME estructura y transacciona hostelería en operación e inmobiliario comercial de renta. Presentamos los activos por su realidad operativa — ocupación, estructura y estado — no como fichas estáticas, y podemos actuar en todo el ciclo de vida del activo.",
    "تُهيكل XARU HOME وتتداول أصول الضيافة التشغيلية والعقارات التجارية المدرّة للدخل. نعرض الأصول بواقعها التشغيلي — الإشغال والهيكل والحالة — لا كقوائم جامدة، ويمكننا العمل عبر كامل دورة حياة الأصل.",
    "XARU HOME 架构并交易运营中的酒店业与收益型商业地产。我们以资产的运营实况——入住率、结构与状态——呈现，而非静态清单，并可覆盖资产的完整生命周期。")]),
  "02": _P(p=[T("Owners, operators, investors and lenders of operating assets.", "Propietarios, operadores, inversionistas y financiadores de activos en operación.", "ملّاك ومشغّلون ومستثمرون ومموّلون لأصول تشغيلية.", "运营资产的业主、运营商、投资者与出借方。")],
           list=[T("Owners of operating or repositioning hotels", "Propietarios de hoteles en operación o reposicionamiento", "ملّاك فنادق تشغيلية أو قيد إعادة التموضع", "运营中或重新定位酒店的业主"),
                 T("Investors seeking income and value-add", "Inversionistas que buscan renta y value-add", "مستثمرون يبحثون عن دخل وقيمة مضافة", "寻求收益与增值的投资者"),
                 T("Operators seeking assets and mandates", "Operadores que buscan activos y mandatos", "مشغّلون يبحثون عن أصول وتفويضات", "寻求资产与委托的运营商"),
                 T("Sponsors recapitalising halted projects", "Sponsors que recapitalizan proyectos detenidos", "رعاة يعيدون رسملة مشاريع متوقفة", "为停滞项目再融资的发起方")]),
  "03": _P(p=[T("Operating and development-stage assets across hospitality and income commercial.", "Activos en operación y en desarrollo en hostelería y comercial de renta.", "أصول تشغيلية وقيد التطوير عبر الضيافة والتجاري المدرّ للدخل.", "涵盖酒店与收益型商业的运营与开发阶段资产。")],
           list=[T("Operating hotels and resorts (P&L, occupancy)", "Hoteles y resorts en operación (P&L, ocupación)", "فنادق ومنتجعات تشغيلية (الأرباح والإشغال)", "运营中的酒店与度假村（损益、入住率）"),
                 T("Repositioning and value-add", "Reposicionamiento y value-add", "إعادة التموضع والقيمة المضافة", "重新定位与增值"),
                 T("Serviced residences and aparthotels", "Aparthoteles y serviced residences", "المساكن المخدومة والشقق الفندقية", "服务式公寓与公寓酒店"),
                 T("Income commercial and leisure assets", "Comercial de renta y activos de ocio", "التجاري المدرّ للدخل وأصول الترفيه", "收益型商业与休闲资产"),
                 T("Halted / incomplete projects seeking capital", "Proyectos detenidos / incompletos que buscan capital", "مشاريع متوقفة / غير مكتملة تبحث عن رأس مال", "寻求资本的停滞／未完工项目")]),
  "04": _P(p=[T("XARU prepares teasers, runs structured processes, coordinates operator selection and manages the transaction — protecting sensitive financials throughout.",
                "XARU prepara teasers, conduce procesos estructurados, coordina la selección de operador y gestiona la transacción — protegiendo los datos financieros sensibles en todo momento.",
                "تُعدّ XARU الموجزات وتدير عمليات منظّمة وتنسّق اختيار المشغّل وتدير الصفقة — مع حماية البيانات المالية الحسّاسة طوال المسار.",
                "XARU 准备招商摘要、开展结构化流程、协调运营商遴选并管理交易——全程保护敏感财务数据。")]),
  "05": _P(p=[T("What XARU does not do.", "Qué NO hace XARU.", "ما لا تقوم به XARU.", "XARU 不做的事。")],
           list=[T("Publish full P&L, occupancy or licences openly", "Publicar P&L, ocupación o licencias completas de forma abierta", "نشر كامل الأرباح أو الإشغال أو التراخيص علناً", "公开完整损益、入住率或牌照"),
                 T("Present halted projects as operational", "Presentar proyectos detenidos como operativos", "عرض مشاريع متوقفة على أنها تشغيلية", "把停滞项目呈现为运营中"),
                 T("Guarantee returns", "Garantizar rendimientos", "ضمان العوائد", "保证回报")]),
  "06": _P(steps=[T("Asset review and operating read", "Revisión del activo y lectura operativa", "مراجعة الأصل والقراءة التشغيلية", "资产审阅与运营解读"),
                  T("Teaser and confidential information memorandum", "Teaser y memorándum de información confidencial", "موجز ومذكرة معلومات سرّية", "招商摘要与保密信息备忘录"),
                  T("Structured process and NDA data room", "Proceso estructurado y data room bajo NDA", "عملية منظّمة وغرفة بيانات بموجب اتفاقية سرية", "结构化流程与保密数据室"),
                  T("Operator selection where required", "Selección de operador cuando procede", "اختيار المشغّل عند اللزوم", "在需要时遴选运营商"),
                  T("Transaction management to completion", "Gestión de la transacción hasta el cierre", "إدارة الصفقة حتى الإنجاز", "交易管理直至完成")]),
  "07": _P(p=[T("Admission protects sensitive operating information.", "La admisión protege la información operativa sensible.", "القبول يحمي المعلومات التشغيلية الحسّاسة.", "准入保护敏感运营信息。")],
           list=[T("Verified ownership, sponsorship or capital capacity", "Titularidad, patrocinio o capacidad de capital verificados", "ملكية أو رعاية أو قدرة رأسمالية موثّقة", "已核实的所有权、发起方或资本能力"),
                 T("Realistic pricing and process expectations", "Precio y expectativas de proceso realistas", "تسعير وتوقعات عملية واقعية", "合理的定价与流程预期"),
                 T("NDA and KYC where applicable", "NDA y KYC cuando aplique", "اتفاقية سرية واعرف عميلك عند الاقتضاء", "适用时签署保密协议与 KYC")]),
  "08": _P(p=[T("Transaction capability, operating expertise and capital access.", "Capacidad transaccional, expertise operativo y acceso a capital.", "قدرة على الصفقات وخبرة تشغيلية ووصول إلى رأس المال.", "交易能力、运营专长与资本渠道。")],
           list=[T("In-house process and transaction management", "Proceso y gestión de transacciones propios", "عملية وإدارة صفقات داخلية", "自有流程与交易管理"),
                 T("Operator and brand relationships", "Relaciones con operadores y marcas", "علاقات مع المشغّلين والعلامات", "运营商与品牌关系"),
                 T("Capital partners for recapitalisation and JV", "Partners de capital para recapitalización y JV", "شركاء رأس مال لإعادة الرسملة والمشاريع المشتركة", "再融资与合资的资本伙伴")]),
  "09": _P(p=[T("A 210-key hotel is halted pre-opening. XARU prepares a confidential teaser, runs a capital process under NDA, selects an operator and structures a recapitalisation JV — occupancy and NOI disclosed only inside the data room.",
                "Un hotel de 210 llaves queda detenido antes de abrir. XARU prepara un teaser confidencial, conduce un proceso de capital bajo NDA, selecciona operador y estructura una JV de recapitalización — ocupación y NOI revelados solo dentro del data room.",
                "يتوقّف فندق بـ210 مفاتيح قبل الافتتاح. تُعدّ XARU موجزاً سرّياً وتدير عملية رأسمالية بموجب اتفاقية سرية وتختار مشغّلاً وتُهيكل مشروعاً مشتركاً لإعادة الرسملة — لا يُكشف الإشغال وصافي الدخل إلا داخل غرفة البيانات.",
                "一家210间客房的酒店在开业前停滞。XARU 制作保密摘要、在保密协议下开展资本流程、遴选运营商并架构再融资合资——入住率与净营业收入仅在数据室内披露。")]),
  "10": _P(p=[T("Sensitive financials are released only through a controlled, NDA-governed process.", "Los datos financieros sensibles se liberan solo mediante un proceso controlado y regido por NDA.", "لا تُتاح البيانات المالية الحسّاسة إلا عبر عملية مضبوطة تحكمها اتفاقية سرية.", "敏感财务仅通过受控、受保密协议约束的流程释放。")]),
  "11": _P(faq=[
    (T("Will you show occupancy and NOI?", "¿Mostrarán ocupación y NOI?", "هل ستعرضون الإشغال وصافي الدخل؟", "会展示入住率与净营业收入吗？"),
     T("As teasers publicly; full figures are released under NDA.", "Como avances públicamente; las cifras completas se liberan bajo NDA.", "كموجز علناً؛ وتُتاح الأرقام الكاملة بموجب اتفاقية سرية.", "公开仅作简报；完整数字在保密协议下提供。")),
    (T("Do you handle halted projects?", "¿Gestionan proyectos detenidos?", "هل تديرون المشاريع المتوقفة؟", "你们处理停滞项目吗？"),
     T("Yes — recapitalisation and repositioning are a core specialty.", "Sí — recapitalización y reposicionamiento son una especialidad central.", "نعم — إعادة الرسملة والتموضع تخصّص أساسي.", "是的——再融资与重新定位是核心专长。")),
   ]),
 },

 # ---------------------------------------------------------------- Land & Master Developments (division)
 "developments/land-master-developments": {
  "01": _P(p=[T(
    "XARU HOME originates, structures and delivers land and master developments — territory measured in kilometres, held as a single thesis. From large land and coastal holdings to signature destinations such as ASHIMA, we carry a site from land to legacy.",
    "XARU HOME origina, estructura y entrega suelo y desarrollos maestros — territorio medido en kilómetros, sostenido como una sola tesis. Desde grandes extensiones y suelo costero hasta destinos emblemáticos como ASHIMA, llevamos un emplazamiento del suelo al legado.",
    "تنشئ XARU HOME وتُهيكل وتُسلّم الأراضي والتطويرات الكبرى — أرضٌ تُقاس بالكيلومترات وتُحمَل كأطروحة واحدة. من الأراضي الواسعة والساحلية إلى وجهات مميّزة مثل ASHIMA، ننقل الموقع من الأرض إلى الإرث.",
    "XARU HOME 发起、架构并交付土地与总体开发——以公里衡量、作为单一论点持有的疆域。从大宗土地与滨海地块到 ASHIMA 等标志性目的地，我们让一处土地从疆域走向传世之作。")]),
  "02": _P(p=[T("Landowners, developers, capital and institutions building at destination scale.", "Propietarios de suelo, desarrolladores, capital e instituciones que construyen a escala de destino.", "ملّاك الأراضي والمطوّرون ورأس المال والمؤسسات الذين يبنون على نطاق الوجهات.", "以目的地规模建设的地主、开发商、资本与机构。")],
           list=[T("Landowners seeking a developer or capital", "Propietarios de suelo que buscan desarrollador o capital", "ملّاك أراضٍ يبحثون عن مطوّر أو رأس مال", "寻求开发商或资本的地主"),
                 T("Developers seeking land or master plans", "Desarrolladores que buscan suelo o master plans", "مطوّرون يبحثون عن أراضٍ أو مخططات عامة", "寻求土地或总体规划的开发商"),
                 T("Capital and family offices for large projects", "Capital y family offices para grandes proyectos", "رأس مال ومكاتب عائلية للمشاريع الكبرى", "投资大型项目的资本与家族办公室"),
                 T("Operators for experiential destinations", "Operadores para destinos experienciales", "مشغّلون للوجهات التجريبية", "体验式目的地的运营商")]),
  "03": _P(p=[T("Land and project positions across their full spectrum.", "Posiciones de suelo y proyecto en todo su espectro.", "مراكز أراضٍ ومشاريع عبر طيفها الكامل.", "覆盖全谱系的土地与项目头寸。")],
           list=[T("Large land and coastal holdings", "Grandes extensiones y suelo costero", "أراضٍ واسعة وحيازات ساحلية", "大宗土地与滨海地块"),
                 T("Resort land and mixed-use", "Suelo para resorts y uso mixto", "أراضي المنتجعات والاستخدام المختلط", "度假村用地与混合用途"),
                 T("Planned communities and experiential destinations", "Comunidades planificadas y destinos experienciales", "مجتمعات مخططة ووجهات تجريبية", "规划社区与体验式目的地"),
                 T("Permitted land and land in regularization", "Suelo con permisos y suelo en regularización", "أراضٍ مرخّصة وأراضٍ قيد التسوية", "已获许可土地与权属规整中土地"),
                 T("Signature master developments (ASHIMA)", "Desarrollos maestros emblemáticos (ASHIMA)", "تطويرات رئيسية مميّزة (ASHIMA)", "标志性总体开发（ASHIMA）")]),
  "04": _P(p=[T("Depending on the project, jurisdiction, feasibility and mandate, XARU may act as adviser, structurer, integrator, sponsor, manager or participant — coordinating land, structuring, capital, permits, operator and delivery.",
                "Según el proyecto, la jurisdicción, la viabilidad y el mandato, XARU puede actuar como asesor, estructurador, integrador, sponsor, gestor o participante — coordinando suelo, estructuración, capital, permisos, operador y entrega.",
                "بحسب المشروع والولاية القضائية والجدوى والتفويض، قد تعمل XARU كمستشار أو مُهيكل أو مُدمج أو راعٍ أو مدير أو مشارك — بتنسيق الأرض والهيكلة ورأس المال والتصاريح والمشغّل والتسليم.",
                "视项目、司法管辖区、可行性与授权而定，XARU 可担任顾问、架构方、整合方、发起方、管理方或参与方——协调土地、架构、资本、许可、运营商与交付。")]),
  "05": _P(p=[T("What XARU does not do.", "Qué NO hace XARU.", "ما لا تقوم به XARU.", "XARU 不做的事。")],
           list=[T("Claim it “always develops” every asset", "Afirmar que «siempre desarrolla» todo activo", "الادعاء بأنها «تطوّر دائماً» كل أصل", "声称对每处资产“总是开发”"),
                 T("Present concept-stage land as permitted", "Presentar suelo en fase de concepto como permitido", "عرض أرض في مرحلة المفهوم على أنها مرخّصة", "把概念阶段土地呈现为已获许可"),
                 T("Overstate tenure, water or environmental status", "Sobreafirmar la tenencia, el agua o el estado ambiental", "المبالغة في الحيازة أو المياه أو الوضع البيئي", "夸大权属、水资源或环境状态")]),
  "06": _P(steps=[T("Land verification and thesis", "Verificación del suelo y tesis", "التحقّق من الأرض والأطروحة", "土地核实与论点"),
                  T("Feasibility and master plan", "Viabilidad y master plan", "الجدوى والمخطط العام", "可行性与总体规划"),
                  T("Legal, fiduciary and SPV structuring", "Estructuración jurídica, fiduciaria y de SPV", "الهيكلة القانونية والائتمانية وSPV", "法律、信托与SPV架构"),
                  T("Permits, capital and operator", "Permisos, capital y operador", "التصاريح ورأس المال والمشغّل", "许可、资本与运营商"),
                  T("Development management and delivery", "Gestión de desarrollo y entrega", "إدارة التطوير والتسليم", "开发管理与交付")]),
  "07": _P(p=[T("Large developments require aligned counterparties.", "Los grandes desarrollos requieren contrapartes alineadas.", "تتطلب التطويرات الكبرى أطرافاً متوائمة.", "大型开发需要目标一致的对手方。")],
           list=[T("Verified land control or a credible thesis", "Control de suelo verificado o una tesis creíble", "سيطرة موثّقة على الأرض أو أطروحة موثوقة", "已核实的土地控制或可信论点"),
                 T("Capital or development capacity", "Capacidad de capital o de desarrollo", "قدرة رأسمالية أو تطويرية", "资本或开发能力"),
                 T("Long-horizon, phased expectations", "Expectativas de horizonte largo y por fases", "توقعات طويلة الأمد وعلى مراحل", "长周期、分期的预期")]),
  "08": _P(p=[T("Development capability across the value chain.", "Capacidad de desarrollo en toda la cadena de valor.", "قدرة تطويرية عبر سلسلة القيمة.", "覆盖价值链的开发能力。")],
           list=[T("In-house structuring and development management", "Estructuración y gestión de desarrollo propias", "هيكلة وإدارة تطوير داخلية", "自有架构与开发管理"),
                 T("Planning, environmental and legal partners", "Partners de urbanismo, medio ambiente y legales", "شركاء تخطيط وبيئة وقانون", "规划、环境与法律合作伙伴"),
                 T("Capital, operator and JV partners", "Partners de capital, operador y JV", "شركاء رأس مال ومشغّلون ومشاريع مشتركة", "资本、运营商与合资伙伴")]),
  "09": _P(p=[T("An 11,000,000+ m² coastal holding is verified and master-planned. XARU structures the vehicle, phases the plan, and brings a developer and capital into a joint venture — the land moving from thesis to development-ready.",
                "Una reserva costera de 11.000.000+ m² se verifica y se planifica. XARU estructura el vehículo, fasea el plan e integra a un desarrollador y capital en una joint venture — el suelo pasando de tesis a listo para desarrollo.",
                "تُتحقّق حيازة ساحلية تتجاوز 11.000.000 م² وتُخطَّط. تُهيكل XARU الكيان وتقسّم الخطة إلى مراحل وتُدخل مطوّراً ورأس مال في مشروع مشترك — لتنتقل الأرض من الأطروحة إلى الجاهزية للتطوير.",
                "一处逾 11,000,000 平方米的滨海地块经核实并完成总体规划。XARU 搭建载体、分期规划，并引入开发商与资本组成合资——土地从论点走向开发就绪。")]),
  "10": _P(p=[T("Tenure, permits and environmental status are represented only as verified under mandate.", "La tenencia, los permisos y el estado ambiental solo se representan como verificados bajo mandato.", "لا تُمثَّل الحيازة والتصاريح والوضع البيئي إلا كموثّقة بموجب تفويض.", "权属、许可与环境状态仅以受托核实的方式呈现。")]),
  "11": _P(faq=[
    (T("Is the land permitted?", "¿El suelo tiene permisos?", "هل الأرض مرخّصة؟", "土地已获许可吗？"),
     T("Each opportunity states its permit and phase status explicitly.", "Cada oportunidad indica su estado de permisos y fase de forma explícita.", "تبيّن كل فرصة حالة تصاريحها ومرحلتها صراحةً.", "每个机会均明确说明其许可与阶段状态。")),
    (T("Does XARU co-invest?", "¿XARU coinvierte?", "هل تشارك XARU في الاستثمار؟", "XARU 会共同投资吗？"),
     T("Depending on the mandate, XARU may act as sponsor or participant.", "Según el mandato, XARU puede actuar como sponsor o participante.", "بحسب التفويض، قد تعمل XARU كراعٍ أو مشارك.", "视授权而定，XARU 可担任发起方或参与方。")),
   ]),
 },
}
