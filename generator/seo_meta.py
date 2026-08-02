# -*- coding: utf-8 -*-
"""XARU HOME — SEO/AEO metadata & JSON-LD (Phase 6).

Single source of truth for:
  * SEO_META  — unique <title> + <meta description> per page, per language
                (EN values from SEO_AUDIT.md §3; ES/AR/ZH = patrimonial-quality,
                keyword-localised translations, brands untranslated).
  * FAQ_QA    — the 6 real Q&A (SCHEMA_ADD.md block c) in 4 languages; the visible
                accordion and the FAQPage JSON-LD are BOTH derived from this dict,
                so they can never drift.
  * JSON-LD   — enriched Organization/RealEstateAgent + 5 Service blocks (index),
                WebSite + SearchAction (every page, shared chrome), FAQPage (faq),
                BreadcrumbList (inner pages). Built as Python dicts and json.dumps'd
                so every emitted block is valid JSON by construction.

Imported by gen_i18n.py.
"""
import json, re

# ---------------------------------------------------------------- helpers
def esc(s):
    """Minimal HTML escaping for text placed in <title>/attribute values."""
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

LANGS = ("en", "es", "ar", "zh")
BASE  = {"en": "https://xaruhome.com/", "es": "https://xaruhome.com/es/",
         "ar": "https://xaruhome.com/ar/", "zh": "https://xaruhome.com/zh/"}
INLANG = {"en": "en", "es": "es", "ar": "ar", "zh": "zh-CN"}

def page_url(lang, fname):
    # Home pages use CLEAN URLs (no index.html); inner pages keep their .html.
    if fname == "index.html":
        return BASE[lang]
    return BASE[lang] + fname

# ======================================================================
# 1) TITLES + DESCRIPTIONS  (title <=60 EN; desc 146-156 EN; natural elsewhere)
# ======================================================================
SEO_META = {
 "index.html": {
  "en": ("XARU HOME | Assets, Projects, Capital and International Expansion",
         "Real estate is the starting point. XARU HOME is the operational home for assets, projects, capital and international expansion."),
  "es": ("XARU HOME | Activos, proyectos, capital y expansión internacional",
         "Real estate es el punto de partida. XARU HOME es el hogar operativo de activos, proyectos, capital y expansión internacional."),
  "ar": ("XARU HOME | الأصول والمشاريع ورأس المال والتوسّع الدولي",
         "العقارات هي نقطة الانطلاق. XARU HOME هي المقرّ التشغيلي للأصول والمشاريع ورأس المال والتوسّع الدولي."),
  # El chino era fiel pero corto: 37 caracteres. Como en CJK cada caracter ocupa
  # el doble de ancho que uno latino, no llegaba a llenar el espacio que Google
  # muestra. Se amplia nombrando las divisiones, sin inflar con palabras clave.
  "zh": ("XARU HOME | 资产、项目、资本与国际拓展",
         "房地产是起点。XARU HOME 是资产、项目、资本与国际拓展的运营中枢，涵盖私人住宅、商业与酒店资产、土地与总体开发、项目架构及资本合作。"),
 },
 "property-listing-buy.html": {
  "en": ("Private Islands & Luxury Property for Sale | XARU HOME",
         "Buy private islands, beachfront land, hotels and luxury villas worldwide with XARU HOME. Curated ultra-prime listings, discreet global advisory from Dubai."),
  "es": ("Islas privadas y propiedades de lujo en venta | XARU HOME",
         "Compre islas privadas, suelo frente al mar, hoteles y villas de lujo en todo el mundo con XARU HOME. Listados ultra-prime seleccionados y asesoría global discreta desde Dubái."),
  "ar": ("جزر خاصة وعقارات فاخرة للبيع | XARU HOME",
         "اشترِ جزراً خاصة وأراضيَ على الواجهة البحرية وفنادق وفللاً فاخرة حول العالم مع XARU HOME. قوائم فائقة التميّز منتقاة واستشارة عالمية حصيفة من دبي."),
  "zh": ("私人岛屿与奢华房产在售 | XARU HOME",
         "通过 XARU HOME 购置遍及全球的私人岛屿、海滨地块、酒店与奢华别墅。精选顶级房源，源自迪拜的审慎全球顾问服务。"),
 },
 "property-listing-rent.html": {
  "en": ("Luxury Villas & Estates for Rent Worldwide | XARU HOME",
         "Rent exceptional luxury villas, estates and residences worldwide with XARU HOME. Private, senior advisory from the global structure of NEXARU GLOBAL."),
  "es": ("Villas y fincas de lujo en alquiler en el mundo | XARU HOME",
         "Alquile villas, fincas y residencias de lujo excepcionales en todo el mundo con XARU HOME. Asesoría privada y sénior de la estructura global de NEXARU GLOBAL."),
  "ar": ("فلل وعزب فاخرة للإيجار حول العالم | XARU HOME",
         "استأجر فللاً وعزباً ومساكن فاخرة استثنائية حول العالم مع XARU HOME. استشارة خاصة ورفيعة المستوى من الكيان العالمي لـ NEXARU GLOBAL."),
  "zh": ("全球奢华别墅与庄园租赁 | XARU HOME",
         "通过 XARU HOME 租赁遍及全球的卓越奢华别墅、庄园与宅邸。源自 NEXARU GLOBAL 全球架构的私人资深顾问服务。"),
 },
 "property-listing-search.html": {
  "en": ("Search Global Luxury Real Estate | XARU HOME",
         "Search XARU HOME's global portfolio of private islands, luxury villas, land and resorts by location, type and scale. Ultra-prime real estate, worldwide."),
  "es": ("Buscar inmobiliaria de lujo global | XARU HOME",
         "Busque en el portafolio global de XARU HOME —islas privadas, villas de lujo, suelo y resorts— por ubicación, tipo y escala. Inmobiliaria ultra-prime, en todo el mundo."),
  "ar": ("ابحث في العقارات الفاخرة عالمياً | XARU HOME",
         "ابحث في محفظة XARU HOME العالمية من الجزر الخاصة والفلل الفاخرة والأراضي والمنتجعات حسب الموقع والنوع والحجم. عقارات فائقة التميّز حول العالم."),
  "zh": ("搜索全球奢华房产 | XARU HOME",
         "按位置、类型与规模搜索 XARU HOME 的全球房产组合——私人岛屿、奢华别墅、土地与度假村。遍及全球的顶级房产。"),
 },
 "single-property-v1.html": {
  "en": ("Exceptional Luxury Property | XARU HOME",
         "Explore an exceptional luxury property with XARU HOME — ultra-prime real estate, private advisory and discreet acquisition worldwide, including with crypto."),
  "es": ("Propiedad de lujo excepcional | XARU HOME",
         "Explore una propiedad de lujo excepcional con XARU HOME: inmobiliaria ultra-prime, asesoría privada y adquisición discreta en todo el mundo, también con cripto."),
  "ar": ("عقار فاخر استثنائي | XARU HOME",
         "استكشف عقاراً فاخراً استثنائياً مع XARU HOME: عقارات فائقة التميّز واستشارة خاصة واقتناء حصيف حول العالم، بما في ذلك بالعملات الرقمية."),
  "zh": ("卓越奢华房产 | XARU HOME",
         "与 XARU HOME 一同探索一处卓越奢华房产——遍及全球的顶级房产、私人顾问与审慎收购，亦可使用加密资产。"),
 },
 "property-details.html": {
  "en": ("Private Island & Estate Details | XARU HOME",
         "View full details of this ultra-prime XARU HOME listing — private islands and luxury estates worldwide, with discreet acquisition and digital-asset options."),
  "es": ("Detalles de isla privada y finca | XARU HOME",
         "Consulte todos los detalles de este listado ultra-prime de XARU HOME: islas privadas y fincas de lujo en todo el mundo, con adquisición discreta y opciones en activos digitales."),
  "ar": ("تفاصيل جزيرة خاصة وعزبة | XARU HOME",
         "اطّلع على كامل تفاصيل هذا العرض الفائق التميّز من XARU HOME: جزر خاصة وعزب فاخرة حول العالم، مع اقتناء حصيف وخيارات بالأصول الرقمية."),
  "zh": ("私人岛屿与庄园详情 | XARU HOME",
         "查看 XARU HOME 这处顶级房源的完整详情——遍及全球的私人岛屿与奢华庄园，提供审慎收购及数字资产付款选项。"),
 },
 "about-us.html": {
  "en": ("About XARU HOME | Global Luxury Real Estate Group",
         "XARU HOME is the luxury real estate structure of NEXARU GLOBAL: 20+ years advising private clients on acquisition, investment, development and relocation."),
  "es": ("Acerca de XARU HOME | Grupo inmobiliario de lujo global",
         "XARU HOME es la estructura inmobiliaria de lujo de NEXARU GLOBAL: más de 20 años asesorando a clientes privados en adquisición, inversión, desarrollo y relocalización."),
  "ar": ("عن XARU HOME | مجموعة عقارات فاخرة عالمية",
         "XARU HOME هي الكيان العقاري الفاخر لـ NEXARU GLOBAL: أكثر من 20 عاماً في إرشاد العملاء من الأفراد في الاقتناء والاستثمار والتطوير والانتقال."),
  "zh": ("关于 XARU HOME | 全球奢华房产集团",
         "XARU HOME 是 NEXARU GLOBAL 旗下的奢华房产架构：逾 20 年为私人客户提供收购、投资、开发与移居方面的咨询。"),
 },
 "contact.html": {
  "en": ("Contact XARU HOME | Private Luxury Real Estate Enquiry",
         "Contact XARU HOME for a confidential luxury real estate enquiry. Dubai-based, UAE-licensed advisory for private islands, investment and global relocation."),
  "es": ("Contacto XARU HOME | Consulta privada de inmobiliaria de lujo",
         "Contacte con XARU HOME para una consulta inmobiliaria de lujo confidencial. Asesoría con base en Dubái y licencia en los EAU: islas privadas, inversión y relocalización global."),
  "ar": ("اتصل بـ XARU HOME | استفسار خاص عن العقارات الفاخرة",
         "تواصل مع XARU HOME لاستفسار عقاري فاخر وسرّي. استشارة مقرّها دبي ومرخّصة في الإمارات: جزر خاصة واستثمار وانتقال عالمي."),
  "zh": ("联系 XARU HOME | 奢华房产私人咨询",
         "就保密的奢华房产事宜联系 XARU HOME。总部位于迪拜、持阿联酋牌照的顾问服务：私人岛屿、投资与全球移居。"),
 },
 "agents-list.html": {
  "en": ("Advisors | XARU HOME Luxury Real Estate",
         "Meet the senior advisors behind XARU HOME — a discreet luxury real estate team guiding private clients and institutions across borders, worldwide."),
  "es": ("Asesores | Inmobiliaria de lujo XARU HOME",
         "Conozca a los asesores sénior de XARU HOME: un equipo inmobiliario de lujo y discreto que guía a clientes privados e instituciones más allá de las fronteras."),
  "ar": ("المستشارون | عقارات XARU HOME الفاخرة",
         "تعرّف على كبار مستشاري XARU HOME: فريق عقاري فاخر وحصيف يرشد العملاء من الأفراد والمؤسسات عبر الحدود حول العالم."),
  "zh": ("顾问团队 | XARU HOME 奢华房产",
         "认识 XARU HOME 背后的资深顾问——一支审慎的奢华房产团队，为跨境的私人客户与机构提供指引。"),
 },
 "blog.html": {
  "en": ("Luxury Real Estate Insights & News | XARU HOME",
         "Insights on luxury real estate, private islands, investment and buying property with crypto — from XARU HOME, the global structure of NEXARU GLOBAL."),
  "es": ("Perspectivas y noticias de inmobiliaria de lujo | XARU HOME",
         "Perspectivas sobre inmobiliaria de lujo, islas privadas, inversión y compra de propiedades con cripto, de XARU HOME, la estructura global de NEXARU GLOBAL."),
  "ar": ("رؤى وأخبار العقارات الفاخرة | XARU HOME",
         "رؤى حول العقارات الفاخرة والجزر الخاصة والاستثمار وشراء العقارات بالعملات الرقمية، من XARU HOME، الكيان العالمي لـ NEXARU GLOBAL."),
  "zh": ("奢华房产洞见与资讯 | XARU HOME",
         "关于奢华房产、私人岛屿、投资及以加密资产购置房产的洞见——来自 NEXARU GLOBAL 全球架构 XARU HOME。"),
 },
 "blog-details.html": {
  "en": ("Luxury Real Estate Insight | XARU HOME",
         "Read the latest XARU HOME insight on luxury real estate, private islands, investment and relocation — expert perspective for private clients worldwide."),
  "es": ("Análisis de inmobiliaria de lujo | XARU HOME",
         "Lea el último análisis de XARU HOME sobre inmobiliaria de lujo, islas privadas, inversión y relocalización: perspectiva experta para clientes privados en todo el mundo."),
  "ar": ("تحليل العقارات الفاخرة | XARU HOME",
         "اقرأ أحدث تحليل من XARU HOME حول العقارات الفاخرة والجزر الخاصة والاستثمار والانتقال: رؤية خبيرة للعملاء من الأفراد حول العالم."),
  "zh": ("奢华房产洞察 | XARU HOME",
         "阅读 XARU HOME 关于奢华房产、私人岛屿、投资与移居的最新洞察——为全球私人客户提供的专家视角。"),
 },
 "faq.html": {
  "en": ("Luxury Real Estate FAQ | XARU HOME",
         "Answers on XARU HOME's luxury real estate services: acquisition, investment, relocation and buying property with digital assets through regulated channels."),
  "es": ("Preguntas frecuentes de inmobiliaria de lujo | XARU HOME",
         "Respuestas sobre los servicios inmobiliarios de lujo de XARU HOME: adquisición, inversión, relocalización y compra de propiedades con activos digitales por canales regulados."),
  "ar": ("الأسئلة الشائعة للعقارات الفاخرة | XARU HOME",
         "إجابات حول خدمات XARU HOME العقارية الفاخرة: الاقتناء والاستثمار والانتقال وشراء العقارات بالأصول الرقمية عبر قنوات مُنظَّمة."),
  "zh": ("奢华房产常见问题 | XARU HOME",
         "关于 XARU HOME 奢华房产服务的解答：收购、投资、移居，以及通过受监管渠道以数字资产购置房产。"),
 },
}

# ---------------------------------------------------------------- head rewriter
def set_head(h, lang, fname):
    """Rewrite <title>, meta description, og/twitter title+description and og:url
    in `h` for (lang, fname). Idempotent — matches by tag, not by prior content."""
    title, desc = SEO_META[fname][lang]
    t, d = esc(title), esc(desc)
    url = page_url(lang, fname)
    h = re.sub(r'<title>.*?</title>', lambda m: '<title>%s</title>' % t, h, count=1, flags=re.S)
    h = re.sub(r'<meta\s+name="description"[^>]*?content="[^"]*"\s*/?>',
               lambda m: '<meta name="description" content="%s" />' % d, h, count=1, flags=re.S)
    h = re.sub(r'<meta property="og:title" content="[^"]*"\s*/?>',
               lambda m: '<meta property="og:title" content="%s">' % t, h, count=1)
    h = re.sub(r'<meta property="og:description" content="[^"]*"\s*/?>',
               lambda m: '<meta property="og:description" content="%s">' % d, h, count=1)
    h = re.sub(r'<meta name="twitter:title" content="[^"]*"\s*/?>',
               lambda m: '<meta name="twitter:title" content="%s">' % t, h, count=1)
    h = re.sub(r'<meta name="twitter:description" content="[^"]*"\s*/?>',
               lambda m: '<meta name="twitter:description" content="%s">' % d, h, count=1)
    h = re.sub(r'<meta property="og:url" content="[^"]*"\s*/?>',
               lambda m: '<meta property="og:url" content="%s">' % url, h, count=1)
    return h

# ======================================================================
# 2) FAQ — 6 real Q&A (SCHEMA_ADD block c), 4 languages.
#    Visible accordion (EN written into faq.html) + translations + FAQPage
#    JSON-LD all derive from here, so text and schema always coincide.
# ======================================================================
FAQ_QA = {
 "en": [
  ("What types of property does XARU HOME handle?",
   "XARU HOME brokers ultra-prime real estate worldwide: private islands, large-scale development land, hotels and resorts, and luxury villas and estates, alongside investment, development and relocation services."),
  ("Can I buy property with cryptocurrency or digital assets?",
   "For qualifying clients, XARU HOME facilitates property acquisition using digital assets such as USDC, USDT and BTC, exclusively through regulated channels, with full KYC/AML verification and legal counsel in every jurisdiction."),
  ("Which countries does XARU HOME operate in?",
   "Our network spans the United Arab Emirates and the wider Middle East, China, India, Pakistan, Europe, the United States and Latin America, including Mexico, Colombia, Ecuador, Peru, Panama, the Dominican Republic, El Salvador and Nicaragua."),
  ("Does XARU HOME help with golden visa or residency by investment?",
   "Yes. Through our investment and relocation teams we guide qualified clients on residency and citizenship-by-investment routes, including UAE golden visa real estate, as part of a complete relocation and corporate-services offering."),
  ("Is there a fee for a property consultation?",
   "Initial private consultations are by appointment and confidential. Fees depend on the mandate and are agreed in writing before any engagement; contact us to discuss your requirements."),
  ("Who is behind XARU HOME?",
   "XARU HOME is the luxury real estate structure of NEXARU GLOBAL, a UAE-licensed group based in Dubai whose senior team has advised private clients, families and institutions for more than 20 years."),
 ],
 "es": [
  ("¿Qué tipos de propiedad gestiona XARU HOME?",
   "XARU HOME intermedia bienes raíces ultra-prime en todo el mundo: islas privadas, suelo para desarrollos a gran escala, hoteles y resorts, y villas y fincas de lujo, junto con servicios de inversión, desarrollo y relocalización."),
  ("¿Puedo comprar una propiedad con criptomonedas o activos digitales?",
   "Para clientes que cumplen los requisitos, XARU HOME facilita la adquisición de propiedades mediante activos digitales como USDC, USDT y BTC, exclusivamente a través de canales regulados, con verificación KYC/AML completa y asesoría legal en cada jurisdicción."),
  ("¿En qué países opera XARU HOME?",
   "Nuestra red abarca los Emiratos Árabes Unidos y el conjunto de Oriente Medio, China, India, Pakistán, Europa, Estados Unidos y América Latina, incluidos México, Colombia, Ecuador, Perú, Panamá, República Dominicana, El Salvador y Nicaragua."),
  ("¿Ayuda XARU HOME con la golden visa o la residencia por inversión?",
   "Sí. A través de nuestros equipos de inversión y relocalización, orientamos a clientes cualificados en las vías de residencia y ciudadanía por inversión, incluida la golden visa inmobiliaria de los EAU, como parte de una oferta integral de relocalización y servicios corporativos."),
  ("¿Tiene coste una consulta sobre una propiedad?",
   "Las consultas privadas iniciales son con cita previa y confidenciales. Los honorarios dependen del mandato y se acuerdan por escrito antes de cualquier encargo; contáctenos para tratar sus necesidades."),
  ("¿Quién está detrás de XARU HOME?",
   "XARU HOME es la estructura inmobiliaria de lujo de NEXARU GLOBAL, un grupo con licencia en los EAU y sede en Dubái, cuyo equipo sénior ha asesorado a clientes privados, familias e instituciones durante más de 20 años."),
 ],
 "ar": [
  ("ما أنواع العقارات التي تتعامل معها XARU HOME؟",
   "تُدير XARU HOME صفقات عقارات فائقة التميّز حول العالم: جزر خاصة، وأراضي تطوير كبرى، وفنادق ومنتجعات، وفلل وعزب فاخرة، إلى جانب خدمات الاستثمار والتطوير والانتقال."),
  ("هل يمكنني شراء عقار بالعملات المشفّرة أو الأصول الرقمية؟",
   "للعملاء المؤهّلين، تُيسّر XARU HOME شراء العقارات باستخدام الأصول الرقمية مثل USDC وUSDT وBTC، حصراً عبر قنوات مُنظَّمة، مع التحقّق الكامل وفق معايير «اعرف عميلك» ومكافحة غسل الأموال (KYC/AML)، واستشارة قانونية في كل ولاية قضائية."),
  ("في أي دول تعمل XARU HOME؟",
   "تمتدّ شبكتنا عبر الإمارات العربية المتحدة والشرق الأوسط عموماً، والصين والهند وباكستان وأوروبا والولايات المتحدة وأمريكا اللاتينية، بما في ذلك المكسيك وكولومبيا والإكوادور وبيرو وبنما وجمهورية الدومينيكان والسلفادور ونيكاراغوا."),
  ("هل تساعد XARU HOME في الفيزا الذهبية أو الإقامة عبر الاستثمار؟",
   "نعم. من خلال فريقَي الاستثمار والانتقال لدينا، نرشد العملاء المؤهّلين في مسارات الإقامة والجنسية عبر الاستثمار، بما في ذلك عقارات الفيزا الذهبية في الإمارات، كجزء من عرض متكامل للانتقال والخدمات المؤسسية."),
  ("هل هناك رسوم على استشارة بشأن عقار؟",
   "الاستشارات الخاصة الأولية تكون بموعد مسبق وسرّية. تعتمد الأتعاب على التفويض ويُتّفق عليها كتابةً قبل أي ارتباط؛ تواصل معنا لمناقشة متطلباتك."),
  ("مَن يقف وراء XARU HOME؟",
   "XARU HOME هي الكيان العقاري الفاخر لـ NEXARU GLOBAL، وهي مجموعة مرخّصة في الإمارات ومقرّها دبي، وقد قدّم فريقها الكبير المشورة لعملاء من الأفراد والعائلات والمؤسسات لأكثر من 20 عاماً."),
 ],
 "zh": [
  ("XARU HOME 经手哪些类型的房产？",
   "XARU HOME 在全球代理顶级房产：私人岛屿、大型开发用地、酒店与度假村，以及奢华别墅与庄园，并提供投资、开发与移居服务。"),
  ("我可以用加密货币或数字资产购买房产吗？",
   "对于符合资格的客户，XARU HOME 协助以 USDC、USDT、BTC 等数字资产完成房产收购，且仅通过受监管渠道进行，并在每一司法管辖区实施完整的 KYC/AML 核查并提供法律顾问。"),
  ("XARU HOME 在哪些国家开展业务？",
   "我们的网络遍及阿拉伯联合酋长国及更广泛的中东地区、中国、印度、巴基斯坦、欧洲、美国与拉丁美洲，包括墨西哥、哥伦比亚、厄瓜多尔、秘鲁、巴拿马、多米尼加共和国、萨尔瓦多与尼加拉瓜。"),
  ("XARU HOME 是否协助黄金签证或投资移民居留？",
   "是的。通过我们的投资与移居团队，我们为符合条件的客户提供居留与投资入籍路径的指导，包括阿联酋黄金签证房产，作为完整移居与企业服务方案的一部分。"),
  ("房产咨询是否收费？",
   "初次私人咨询需预约并严格保密。费用视委托而定，并在任何委托开始前以书面形式约定；欢迎联系我们商讨您的需求。"),
  ("XARU HOME 的背后是谁？",
   "XARU HOME 是 NEXARU GLOBAL 旗下的奢华房产架构，一家持有阿联酋牌照、总部位于迪拜的集团，其资深团队为私人客户、家族与机构提供咨询已逾 20 年。"),
 ],
}

def get_faq_pairs(lang):
    """(english, translation) pairs for the visible accordion — questions + answers."""
    pairs = []
    for (eq, ea), (tq, ta) in zip(FAQ_QA["en"], FAQ_QA[lang]):
        pairs.append((eq, tq))
        pairs.append((ea, ta))
    return pairs

# ======================================================================
# 3) JSON-LD
# ======================================================================
ORG_ID     = "https://xaruhome.com/#organization"
WEBSITE_ID = "https://xaruhome.com/#website"
LOGO       = "https://xaruhome.com/assets/img/xaru/monogram_gold_160.png"
COVER      = "https://xaruhome.com/assets/img/xaru/og-cover.jpg"

ORG_DESC = {
 "en": "XARU HOME is the global luxury real estate structure of NEXARU GLOBAL: acquisition and sale of private islands, large-scale land, hotels, resorts and luxury villas; investment and fund structuring; developer capital; relocation and corporate services; and property acquisition with digital assets through regulated channels.",
 "es": "XARU HOME es la estructura inmobiliaria de lujo global de NEXARU GLOBAL: adquisición y venta de islas privadas, suelo a gran escala, hoteles, resorts y villas de lujo; inversión y estructuración de fondos; capital para promotores; relocalización y servicios corporativos; y adquisición de propiedades con activos digitales a través de canales regulados.",
 "ar": "XARU HOME هي الكيان العقاري الفاخر العالمي لـ NEXARU GLOBAL: اقتناء وبيع الجزر الخاصة والأراضي الكبرى والفنادق والمنتجعات والفلل الفاخرة؛ والاستثمار وهيكلة الصناديق؛ ورأس المال للمطوّرين؛ والانتقال والخدمات المؤسسية؛ واقتناء العقارات بالأصول الرقمية عبر قنوات مُنظَّمة.",
 "zh": "XARU HOME 是 NEXARU GLOBAL 旗下的全球奢华房产架构：私人岛屿、大型地块、酒店、度假村与奢华别墅的收购与销售；投资与基金架构；开发商资本；移居与企业服务；以及通过受监管渠道以数字资产收购房产。",
}

AREA = ["United Arab Emirates", "China", "India", "Pakistan", "Europe",
        "United States", "Mexico", "Colombia", "Ecuador", "Peru", "Panama",
        "Dominican Republic", "El Salvador", "Nicaragua"]

OFFERS = [
 "Luxury property acquisition and sale",
 "Private islands and large-scale land brokerage",
 "Hotels and resorts advisory",
 "Real estate investment and fund structuring",
 "Developer capital",
 "Relocation and corporate services",
 "Property acquisition with digital assets via regulated channels",
]

def organization(lang):
    return {
     "@context": "https://schema.org",
     "@type": "RealEstateAgent",
     "@id": ORG_ID,
     "name": "XARU HOME",
     "legalName": "XARU HOME (a NEXARU GLOBAL brand)",
     "url": BASE[lang],
     "logo": LOGO,
     "image": COVER,
     "description": ORG_DESC[lang],
     "inLanguage": INLANG[lang],
     "brand": {"@type": "Brand", "name": "NEXARU GLOBAL"},
     "parentOrganization": {"@type": "Organization", "name": "NEXARU GLOBAL"},
     "foundingDate": "2005",
     "slogan": "One structure, worldwide.",
     "email": "contact@xaruhome.com",
     "knowsLanguage": ["en", "es", "ar", "zh"],
     "address": {"@type": "PostalAddress", "addressLocality": "Dubai", "addressCountry": "AE"},
     "areaServed": [{"@type": "Country", "name": c} for c in AREA],
     "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}} for n in OFFERS],
     "sameAs": [],
    }

def website(lang):
    return {
     "@context": "https://schema.org",
     "@type": "WebSite",
     "@id": WEBSITE_ID,
     "name": "XARU HOME",
     "url": BASE[lang],
     "inLanguage": INLANG[lang],
     "publisher": {"@type": "Organization", "name": "NEXARU GLOBAL"},
     "potentialAction": {
       "@type": "SearchAction",
       "target": {"@type": "EntryPoint",
                  "urlTemplate": BASE[lang] + "property-listing-search.html?q={search_term_string}"},
       "query-input": "required name=search_term_string",
     },
    }

_SERVICES = [
 ("Luxury property acquisition and sale", "Luxury real estate brokerage",
  "Acquisition and sale of exceptional properties — private islands, large-scale land, hotels, resorts and luxury villas — for private clients, families and institutions.",
  "property-listing-buy.html"),
 ("Real estate investment and fund structuring", "Real estate investment advisory",
  "Investment opportunities, fund structuring and residency-by-investment guidance, including UAE golden visa real estate, for qualified investors.",
  "index.html#investment"),
 ("Developer capital", "Development finance and structuring",
  "Capital and structuring for developers of master-planned and large-scale projects, from land to legacy.",
  "index.html#developers"),
 ("Relocation and corporate services", "Relocation and corporate services provider",
  "Complete relocation, corporate structuring and company-services-provider (CSP) support across jurisdictions.",
  "index.html#relocation"),
 ("Property acquisition with digital assets", "Regulated digital-asset property settlement",
  "Property acquisition using digital assets (USDC, USDT, BTC) for qualifying clients, exclusively through regulated channels with full KYC/AML verification and legal counsel in every jurisdiction.",
  "index.html"),
]

def services(lang):
    out = []
    for name, stype, desc, path in _SERVICES:
        # Home-page service URLs use the CLEAN root (no index.html); the
        # inner-page service URL (property-listing-buy.html) keeps its .html.
        url = ("https://xaruhome.com/" + path).replace("/index.html", "/")
        out.append({
         "@context": "https://schema.org",
         "@type": "Service",
         "name": name,
         "serviceType": stype,
         "provider": {"@id": ORG_ID},
         "areaServed": "Worldwide",
         "description": desc,
         "url": url,
        })
    return out

def faqpage(lang):
    return {
     "@context": "https://schema.org",
     "@type": "FAQPage",
     "inLanguage": INLANG[lang],
     "mainEntity": [
       {"@type": "Question", "name": q,
        "acceptedAnswer": {"@type": "Answer", "text": a}}
       for q, a in FAQ_QA[lang]
     ],
    }

# ---- BreadcrumbList ----------------------------------------------------
_L = {
 "home":   {"en": "Home", "es": "Inicio", "ar": "الرئيسية", "zh": "首页"},
 "props":  {"en": "Properties", "es": "Propiedades", "ar": "العقارات", "zh": "房产"},
 "buy":    {"en": "Properties for Sale", "es": "Propiedades en venta", "ar": "عقارات للبيع", "zh": "在售房产"},
 "rent":   {"en": "Properties for Rent", "es": "Propiedades en alquiler", "ar": "عقارات للإيجار", "zh": "租赁房产"},
 "search": {"en": "Search", "es": "Buscar", "ar": "بحث", "zh": "搜索"},
 "single": {"en": "Luxury Property", "es": "Propiedad de lujo", "ar": "عقار فاخر", "zh": "奢华房产"},
 "details":{"en": "Evergreen Estates", "es": "Fincas Evergreen", "ar": "عقارات إيفرغرين", "zh": "常青庄园"},
 "about":  {"en": "About", "es": "Nosotros", "ar": "من نحن", "zh": "关于我们"},
 "contact":{"en": "Contact", "es": "Contacto", "ar": "اتصل بنا", "zh": "联系我们"},
 "agents": {"en": "Advisors", "es": "Asesores", "ar": "المستشارون", "zh": "顾问团队"},
 "blog":   {"en": "Insights", "es": "Perspectivas", "ar": "الرؤى", "zh": "洞见"},
 "post":   {"en": "How to Choose the Perfect Neighborhood for Your Family",
            "es": "Cómo elegir el barrio perfecto para su familia",
            "ar": "كيف تختار الحي المثالي لعائلتك",
            "zh": "如何为家人选择理想社区"},
 "faq":    {"en": "FAQ", "es": "Preguntas frecuentes", "ar": "الأسئلة الشائعة", "zh": "常见问题"},
}

# each trail: list of (label_key, target_fname). Home is prepended automatically.
_TRAILS = {
 "property-listing-buy.html":    [("buy", "property-listing-buy.html")],
 "property-listing-rent.html":   [("rent", "property-listing-rent.html")],
 "property-listing-search.html": [("search", "property-listing-search.html")],
 "single-property-v1.html":      [("props", "property-listing-buy.html"), ("single", "single-property-v1.html")],
 "property-details.html":        [("props", "property-listing-buy.html"), ("details", "property-details.html")],
 "about-us.html":                [("about", "about-us.html")],
 "contact.html":                 [("contact", "contact.html")],
 "agents-list.html":             [("agents", "agents-list.html")],
 "blog.html":                    [("blog", "blog.html")],
 "blog-details.html":            [("blog", "blog.html"), ("post", "blog-details.html")],
 "faq.html":                     [("faq", "faq.html")],
}
BREADCRUMBS = set(_TRAILS)

def breadcrumb(lang, fname):
    trail = [("home", "index.html")] + _TRAILS[fname]
    items = []
    for i, (key, tgt) in enumerate(trail, start=1):
        items.append({"@type": "ListItem", "position": i,
                      "name": _L[key][lang], "item": page_url(lang, tgt)})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "inLanguage": INLANG[lang], "itemListElement": items}

# ---- assembly ----------------------------------------------------------
def _script(d):
    body = json.dumps(d, ensure_ascii=False, indent=2)
    json.loads(body)  # validate every block before it is written
    return '<script type="application/ld+json">\n' + body + '\n</script>'

def jsonld_for(lang, fname):
    """Full comment-wrapped JSON-LD payload for (lang, fname)."""
    blocks = []
    if fname == "index.html":
        blocks.append(organization(lang))
    blocks.append(website(lang))
    if fname == "index.html":
        blocks.extend(services(lang))
    if fname == "faq.html":
        blocks.append(faqpage(lang))
    if fname in BREADCRUMBS:
        blocks.append(breadcrumb(lang, fname))
    parts = "\n".join("    " + _script(b).replace("\n", "\n    ") for b in blocks)
    return "    <!-- XARU JSON-LD -->\n" + parts + "\n    <!-- /XARU JSON-LD -->\n"

def block_count(fname):
    n = 1  # website
    if fname == "index.html":
        n += 1 + len(_SERVICES)
    if fname == "faq.html":
        n += 1
    if fname in BREADCRUMBS:
        n += 1
    return n

# ======================================================================
# 4) PHASE 6 — SEO for the new architecture (folder-URL pages)
#    34 slugs x 4 languages: unique keyword-bearing <title> (<=60 EN),
#    persuasive 150-160 char descriptions, og/twitter, and JSON-LD
#    (BreadcrumbList + Service + ItemList + Article).
#    Consumed by gen_i18n._shell_head / _write_shell.
# ======================================================================

def shell_url(lang, slug):
    """Clean folder URL for a Phase 1-5 page: https://xaruhome.com/es/real-estate/"""
    return BASE[lang] + slug + "/"

OG_LOCALE = {"en": "en_US", "es": "es_ES", "ar": "ar_AE", "zh": "zh_CN"}

_G2 = "https://xaruhome.com/assets/img/xaru/gen2/"

# ---------------------------------------------------------------- short labels (breadcrumbs / schema names)
SLUG_LABEL = {
 "business-infrastructure":                     {"en": "Business Infrastructure", "es": "Infraestructura Empresarial",
                                                 "ar": "البنية المؤسسية", "zh": "企业基础设施"},
 "business-infrastructure/corporate-services":  {"en": "Corporate Services & Relocation", "es": "Servicios Corporativos y Relocalización",
                                                 "ar": "الخدمات المؤسسية والانتقال", "zh": "企业服务与迁居"},
 "business-infrastructure/trade-financial":     {"en": "Trade & Financial Infrastructure", "es": "Comercio e Infraestructura Financiera",
                                                 "ar": "التجارة والبنية المالية", "zh": "贸易与金融基础设施"},
 "capital":                                     {"en": "Capital & Transactions", "es": "Capital y Transacciones",
                                                 "ar": "رأس المال والصفقات", "zh": "资本与交易"},
 "capital/deal-room":                           {"en": "Private Deal Room", "es": "Sala de Operaciones Privada",
                                                 "ar": "غرفة الصفقات الخاصة", "zh": "私人交易室"},
 "capital/strategic-partnerships":              {"en": "Capital & Strategic Partnerships", "es": "Capital y Alianzas Estratégicas",
                                                 "ar": "رأس المال والشراكات الاستراتيجية", "zh": "资本与战略合作"},
 "company":                                     {"en": "Company", "es": "Compañía",
                                                 "ar": "الشركة", "zh": "公司"},
 "developments":                                {"en": "Developments", "es": "Desarrollos",
                                                 "ar": "التطوير", "zh": "开发项目"},
 "developments/land-master-developments":       {"en": "Land & Master Developments", "es": "Suelo y Desarrollos Maestros",
                                                 "ar": "الأراضي والتطويرات الكبرى", "zh": "土地与总体开发"},
 "developments/project-structuring":            {"en": "Project Structuring & Development", "es": "Estructuración y Desarrollo de Proyectos",
                                                 "ar": "هيكلة وتطوير المشاريع", "zh": "项目架构与开发"},
 "insights":                                    {"en": "Insights", "es": "Análisis",
                                                 "ar": "رؤى", "zh": "洞察"},
 "insights/capital-halted-projects":            {"en": "Private capital and halted projects", "es": "Capital privado y proyectos detenidos",
                                                 "ar": "رأس المال الخاص والمشاريع المتوقفة", "zh": "私人资本与停滞项目"},
 "insights/international-establishment":        {"en": "Establishing internationally", "es": "Establecerse internacionalmente",
                                                 "ar": "التأسيس الدولي", "zh": "国际落地"},
 "insights/operational-hospitality":            {"en": "Operational hospitality", "es": "Hospitality operativo",
                                                 "ar": "الضيافة التشغيلية", "zh": "运营型酒店资产"},
 "insights/territorial-land":                   {"en": "Territorial land", "es": "Suelo territorial",
                                                 "ar": "الأرض الإقليمية", "zh": "疆域级土地"},
 "opportunities":                               {"en": "Land, Projects & Opportunities", "es": "Suelo, Proyectos y Oportunidades",
                                                 "ar": "الأراضي والمشاريع والفرص", "zh": "土地、项目与机会"},
 "opportunities/cf-confidential-portfolio":     {"en": "Confidential Portfolio", "es": "Portafolio confidencial",
                                                 "ar": "محفظة سرّية", "zh": "保密资产组合"},
 "opportunities/lp-ashima-masterplan":          {"en": "ASHIMA Master Development", "es": "ASHIMA — Desarrollo maestro",
                                                 "ar": "ASHIMA — تطوير رئيسي", "zh": "ASHIMA 总体开发"},
 "opportunities/lp-land-11m":                   {"en": "Territorial Land Holding", "es": "Reserva territorial",
                                                 "ar": "حيازة أرضية إقليمية", "zh": "区域性土地储备"},
 "opportunities/pa-quarry-license":             {"en": "Quarry Licence & Aggregates", "es": "Licencia de cantera y áridos",
                                                 "ar": "رخصة محجر وركام", "zh": "采石许可与骨料"},
 "opportunities/submit":                        {"en": "Submit an Opportunity", "es": "Presentar una oportunidad",
                                                 "ar": "تقديم فرصة", "zh": "提交机会"},
 "private-enquiry":                             {"en": "Private Enquiry", "es": "Consulta Privada",
                                                 "ar": "استفسار خاص", "zh": "私人咨询"},
 "real-estate":                                 {"en": "Real Estate", "es": "Inmobiliario",
                                                 "ar": "العقارات", "zh": "房地产"},
 "real-estate/sold":                            {"en": "Past Operations", "es": "Operaciones anteriores",
                                                 "ar": "عمليات سابقة", "zh": "过往交易"},
 # ---- rutas del marketplace (Biblia §5.1) -----------------------------
 "real-estate/search":                          {"en": "Search the Inventory", "es": "Buscar en el inventario",
                                                 "ar": "ابحث في المعروض", "zh": "检索资产库"},
 "real-estate/agents":                          {"en": "Advisers", "es": "Asesores",
                                                 "ar": "المستشارون", "zh": "顾问团队"},
 "real-estate/agencies":                        {"en": "Offices", "es": "Oficinas",
                                                 "ar": "المكاتب", "zh": "分支机构"},
 "real-estate/developers":                      {"en": "Developers", "es": "Promotoras",
                                                 "ar": "المطوّرون", "zh": "开发商"},
 "real-estate/new-projects":                    {"en": "New Projects", "es": "Proyectos nuevos",
                                                 "ar": "المشاريع الجديدة", "zh": "新项目"},
 "real-estate/account":                         {"en": "Your Account", "es": "Su cuenta",
                                                 "ar": "حسابك", "zh": "您的账户"},
 "real-estate/office":                          {"en": "Office Operation", "es": "Operación de la oficina",
                                                 "ar": "تشغيل المكتب", "zh": "分支机构运营"},
 "real-estate/administration":                  {"en": "Moderation & Lifecycle", "es": "Moderación y ciclo de vida",
                                                 "ar": "المراجعة ودورة الحياة", "zh": "审核与生命周期"},
 "real-estate/buy":                             {"en": "Residential for Sale", "es": "Residencial en venta",
                                                 "ar": "سكني للبيع", "zh": "住宅出售"},
 "real-estate/rent":                            {"en": "Residential to Rent", "es": "Residencial en alquiler",
                                                 "ar": "سكني للإيجار", "zh": "住宅租赁"},
 "real-estate/commercial/buy":                  {"en": "Commercial for Sale", "es": "Comercial en venta",
                                                 "ar": "تجاري للبيع", "zh": "商业出售"},
 "real-estate/commercial/rent":                 {"en": "Commercial to Lease", "es": "Comercial en alquiler",
                                                 "ar": "تجاري للإيجار", "zh": "商业租赁"},
 "real-estate/land":                            {"en": "Land & Large-Scale Sites", "es": "Suelo y grandes superficies",
                                                 "ar": "الأراضي والمواقع الكبرى", "zh": "土地与大型地块"},
 "real-estate/map":                             {"en": "Inventory Map", "es": "Mapa del inventario",
                                                 "ar": "خريطة المعروض", "zh": "资产地图"},
 "real-estate/commercial-hospitality":          {"en": "Commercial & Hospitality", "es": "Comercial y Hostelería",
                                                 "ar": "التجاري والضيافة", "zh": "商业与酒店"},
 "real-estate/commercial-hospitality/ch-hotel-halted":      {"en": "Halted Hotel Project", "es": "Proyecto hotelero detenido",
                                                 "ar": "مشروع فندقي متوقف", "zh": "停滞酒店项目"},
 "real-estate/commercial-hospitality/ch-hotel-operational": {"en": "Operating Boutique Hotel", "es": "Hotel boutique en operación",
                                                 "ar": "فندق بوتيك تشغيلي", "zh": "运营中精品酒店"},
 "real-estate/commercial-hospitality/ch-resort-development":{"en": "Beach Resort, Development Stage", "es": "Resort de playa, en desarrollo",
                                                 "ar": "منتجع شاطئي، مرحلة التطوير", "zh": "海滨度假村，开发阶段"},
 "real-estate/private-properties":              {"en": "Private Properties", "es": "Propiedades Privadas",
                                                 "ar": "العقارات الخاصة", "zh": "私人房产"},
 "real-estate/private-properties/pp-casa-tulum":      {"en": "Beachfront Residence, Tulum", "es": "Residencia frente al mar, Tulum",
                                                 "ar": "مسكن على الشاطئ، تولوم", "zh": "图卢姆海滨住宅"},
 "real-estate/private-properties/pp-penthouse-london":{"en": "Penthouse, Central London", "es": "Ático, Londres centro",
                                                 "ar": "بنتهاوس، وسط لندن", "zh": "伦敦中心顶层公寓"},
 "real-estate/private-properties/pp-samana-island":   {"en": "Private Island, Samaná Bay", "es": "Isla privada, Bahía de Samaná",
                                                 "ar": "جزيرة خاصة، خليج سامانا", "zh": "萨马纳湾私人岛屿"},
 "real-estate/private-properties/pp-villa-como":      {"en": "Lakefront Estate, Lake Como", "es": "Finca junto al lago, Lago de Como",
                                                 "ar": "حوزة على البحيرة، بحيرة كومو", "zh": "科莫湖畔庄园"},
 "real-estate/private-properties/pp-villa-dubai":     {"en": "Signature Villa, Dubai", "es": "Villa de autor, Dubái",
                                                 "ar": "فيلا مميّزة، دبي", "zh": "迪拜臻品别墅"},
 "real-estate/private-properties/pp-villa-marbella":  {"en": "Villa, Marbella Golden Mile", "es": "Villa, Milla de Oro de Marbella",
                                                 "ar": "فيلا، الميل الذهبي بماربيا", "zh": "马贝拉黄金一英里别墅"},
}

# ---------------------------------------------------------------- title + description, 34 slugs x 4 languages
SHELL_SEO = {

 # ---- paneles (Biblia de Real Estate §5.7-§5.9) -----------------------
 "real-estate/account": {
  "en": ("Saved Properties, Searches & Alerts | XARU HOME",
         "Saved assets in folders, the searches you run again, alerts on them, recently viewed and up to four assets compared side by side. Stored on your device."),
  "es": ("Propiedades, búsquedas y alertas guardadas | XARU HOME",
         "Activos guardados en carpetas, las búsquedas que repite, alertas sobre ellas, vistos recientemente y hasta cuatro activos comparados. Se guarda en su dispositivo."),
  "ar": ("العقارات وعمليات البحث والتنبيهات المحفوظة | XARU HOME",
         "أصول محفوظة في مجلدات، وعمليات البحث التي تكرّرها، والتنبيهات عليها، وما شوهد مؤخراً، وحتى أربعة أصول للمقارنة. يُحفظ على جهازك."),
  "zh": ("收藏的房源、搜索与提醒 | XARU HOME",
         "分文件夹整理的收藏资产、反复运行的搜索、其上的提醒、最近浏览记录，以及最多四项资产的并排对比。全部存于您的设备。"),
 },
 "real-estate/office": {
  "en": ("Partner Console — Inventory, Leads & Credits | XARU HOME",
         "Inventory by lifecycle state against the plan quota, the lead pipeline with response deadlines, credit consumption and the ten-step listing wizard."),
  "es": ("Consola del socio — Inventario, leads y créditos | XARU HOME",
         "Inventario por estado del ciclo de vida contra la cuota del plan, pipeline de leads con plazos de respuesta, consumo de créditos y asistente de alta en diez pasos."),
  "ar": ("لوحة الشريك — المعروض والعملاء والأرصدة | XARU HOME",
         "المعروض حسب حالة دورة الحياة في مقابل حصة الخطة، ومسار العملاء بمواعيد الاستجابة، واستهلاك الأرصدة، ومعالج الإدراج بعشر خطوات."),
  "zh": ("合作方控制台 — 资产、线索与额度 | XARU HOME",
         "按生命周期状态统计的资产及套餐配额、附响应时限的线索漏斗、额度消耗，以及十步发布向导。"),
 },
 "real-estate/administration": {
  "en": ("Moderation Queue & Listing Lifecycle | XARU HOME",
         "The moderation queue with failed rules and deadlines, the inventory across seventeen lifecycle states, live transitions and the taxonomies underneath."),
  "es": ("Cola de moderación y ciclo de vida | XARU HOME",
         "La cola de moderación con reglas incumplidas y plazos, el inventario entre diecisiete estados del ciclo de vida, transiciones en vivo y las taxonomías."),
  "ar": ("قائمة المراجعة ودورة حياة العروض | XARU HOME",
         "قائمة المراجعة مع القواعد المخالفة والمُهل، والمعروض عبر سبع عشرة حالة لدورة الحياة، والانتقالات الحيّة والتصنيفات."),
  "zh": ("审核队列与房源生命周期 | XARU HOME",
         "附未通过规则与时限的审核队列、横跨十七个生命周期状态的资产分布、实时状态迁移及底层分类体系。"),
 },

 # ---- off-plan (Biblia de Real Estate §5.5) ---------------------------
 "real-estate/new-projects": {
  "en": ("Off-Plan Projects & Payment Plans | XARU HOME",
         "Off-plan projects with the developer who committed, the handover date, the construction stage actually reached and how the payment is staged against it."),
  "es": ("Proyectos off-plan y planes de pago | XARU HOME",
         "Proyectos off-plan con la promotora que se ha comprometido, la fecha de entrega, el punto real de la obra y cómo se escalona el pago contra ella."),
  "ar": ("مشاريع على المخطط وخطط السداد | XARU HOME",
         "مشاريع على المخطط مع المطوّر الملتزِم وموعد التسليم ومرحلة الإنشاء المبلوغة فعلاً وكيفية جدولة السداد في مقابلها."),
  "zh": ("期房项目与付款计划 | XARU HOME",
         "期房项目，附作出承诺的开发商、交付日期、工程实际进展阶段，以及付款如何与之对应分期。"),
 },

 # ---- directorios (Biblia de Real Estate §5.6) ------------------------
 "real-estate/agents": {
  "en": ("Property Advisers Worldwide | XARU HOME",
         "The XARU HOME advisers: the office that holds each mandate, the licence on file and the markets each adviser actually covers. No anonymous inbox."),
  "es": ("Asesores inmobiliarios en el mundo | XARU HOME",
         "Los asesores de XARU HOME: la oficina que lleva cada mandato, la licencia registrada y las plazas que cada asesor cubre de verdad. Ningún buzón anónimo."),
  "ar": ("مستشارو العقارات حول العالم | XARU HOME",
         "مستشارو XARU HOME: المكتب صاحب كل تفويض، والترخيص المسجّل، والأسواق التي يغطيها كل مستشار فعلاً. ولا بريد مجهول."),
  "zh": ("全球房地产顾问 | XARU HOME",
         "XARU HOME 的顾问团队：持有各项委托的分支机构、备案执照，以及每位顾问真正覆盖的市场。绝无匿名信箱。"),
 },
 "real-estate/agencies": {
  "en": ("Our Offices & Licensed Entities | XARU HOME",
         "The offices that hold the mandates, each with its legal entity, its licence and the inventory registered under it — what makes a mandate enforceable."),
  "es": ("Nuestras oficinas y entidades licenciadas | XARU HOME",
         "Las oficinas que llevan los mandatos, cada una con su entidad legal, su licencia y el inventario registrado a su nombre — lo que hace exigible un mandato."),
  "ar": ("مكاتبنا وكياناتنا المرخّصة | XARU HOME",
         "المكاتب التي تحمل التفويضات، لكلٍّ كيانه القانوني وترخيصه والمعروض المسجّل باسمه — وهو ما يجعل التفويض واجب النفاذ."),
  "zh": ("我们的分支机构与持牌主体 | XARU HOME",
         "持有委托的各分支机构，均附其法律主体、执照及名下登记的资产——这正是委托具备可执行力的依据。"),
 },
 "real-estate/developers": {
  "en": ("Property Developers & Off-Plan Projects | XARU HOME",
         "The developers behind the off-plan projects on the platform, with registered projects, committed handover and the payment plan on offer."),
  "es": ("Promotoras y proyectos off-plan | XARU HOME",
         "Las promotoras detrás de los proyectos off-plan de la plataforma, con proyectos registrados, entrega comprometida y el plan de pago que ofrecen."),
  "ar": ("المطوّرون ومشاريع البيع على المخطط | XARU HOME",
         "المطوّرون وراء مشاريع «على المخطط» في المنصة، مع المشاريع المسجّلة وموعد التسليم الملتزَم به وخطة السداد المعروضة."),
  "zh": ("开发商与期房项目 | XARU HOME",
         "平台上期房项目背后的开发商，附已登记项目、承诺交付时间与提供的付款计划。"),
 },

 # ---- rutas del marketplace (Biblia de Real Estate §5.1) --------------
 "real-estate/search": {
  "en": ("Search Luxury Property Worldwide | XARU HOME",
         "Search the full XARU HOME inventory: residential, commercial, hospitality and land in the markets where the firm operates. Filter by country, city, typology, price and surface."),
  "es": ("Buscar propiedades de lujo en el mundo | XARU HOME",
         "Busque en todo el inventario de XARU HOME: residencial, comercial, hostelería y suelo en los mercados donde opera la firma. Filtre por país, ciudad, tipología, precio y superficie."),
  "ar": ("ابحث عن عقارات فاخرة حول العالم | XARU HOME",
         "ابحث في كامل معروض XARU HOME: سكني وتجاري وضيافة وأراضٍ في الأسواق التي تعمل بها الشركة. رشّح حسب الدولة والمدينة والنوع والسعر والمساحة."),
  "zh": ("全球奢华房产检索 | XARU HOME",
         "检索 XARU HOME 全部资产：住宅、商业、酒店与土地，覆盖本公司经营的各个市场。可按国家、城市、类型、价格与面积筛选。"),
 },
 "real-estate/buy": {
  "en": ("Luxury Homes for Sale Worldwide | XARU HOME",
         "Villas, penthouses, estates, private islands and heritage houses for sale worldwide. Every record carries its verification status, typology and the office holding the mandate."),
  "es": ("Viviendas de lujo en venta en el mundo | XARU HOME",
         "Villas, áticos, fincas, islas privadas y casas históricas en venta en todo el mundo. Cada registro lleva su estado de verificación, tipología y la oficina que tiene el mandato."),
  "ar": ("منازل فاخرة للبيع حول العالم | XARU HOME",
         "فلل وبنتهاوس وحوزات وجزر خاصة وبيوت تراثية للبيع حول العالم. يحمل كل سجل حالة التوثيق والنوع والمكتب صاحب التفويض."),
  "zh": ("全球奢华住宅在售 | XARU HOME",
         "全球在售的别墅、顶层公寓、庄园、私人岛屿与历史宅邸。每条记录均标注核验状态、物业类型及持有委托的分支机构。"),
 },
 "real-estate/rent": {
  "en": ("Luxury Homes to Rent Worldwide | XARU HOME",
         "Long-let and seasonal residences quoted per year. Relocation cases are handled by the same desk that manages the corporate structuring behind the move."),
  "es": ("Viviendas de lujo en alquiler en el mundo | XARU HOME",
         "Residencias de larga duración y de temporada, cotizadas por año. Los casos de relocalización los lleva la misma mesa que gestiona la estructuración corporativa."),
  "ar": ("منازل فاخرة للإيجار حول العالم | XARU HOME",
         "مساكن للإيجار الطويل والموسمي مُسعَّرة سنوياً. تتولى حالات الانتقال المكتب نفسه الذي يدير الهيكلة المؤسسية وراء الانتقال."),
  "zh": ("全球奢华住宅租赁 | XARU HOME",
         "长租与季节性住宅，按年报价。搬迁安置由负责相应公司架构的同一团队处理。"),
 },
 "real-estate/commercial/buy": {
  "en": ("Hotels, Offices & Commercial Assets for Sale | XARU HOME",
         "Operating hotels, resorts, offices, retail, logistics and industrial plant for sale. Where the asset trades as a business, the record states keys, operator and completion."),
  "es": ("Hoteles, oficinas y activos comerciales en venta | XARU HOME",
         "Hoteles en explotación, resorts, oficinas, retail, logística e industria en venta. Cuando el activo se transmite como negocio, el registro indica llaves, operador y estado de obra."),
  "ar": ("فنادق ومكاتب وأصول تجارية للبيع | XARU HOME",
         "فنادق عاملة ومنتجعات ومكاتب وتجزئة ولوجستيات ومنشآت صناعية للبيع. وحين يُتداول الأصل كنشاط تشغيلي، يوضّح السجل المفاتيح والمشغّل وحالة الإنجاز."),
  "zh": ("酒店、写字楼与商业资产在售 | XARU HOME",
         "在营酒店、度假村、写字楼、零售、物流与工业设施在售。当资产以经营性业务交易时，记录会列明客房数、运营方与交付状态。"),
 },
 "real-estate/commercial/rent": {
  "en": ("Offices, Retail & Warehouse Space to Lease | XARU HOME",
         "Offices, retail units, warehouses and light industrial space quoted per year. Fit-out, licensing and the corporate vehicle behind the tenancy sit in the same file."),
  "es": ("Oficinas, locales y naves en alquiler | XARU HOME",
         "Oficinas, locales, naves y espacio industrial ligero cotizados por año. Implantación, licencias y el vehículo societario del arrendamiento van en el mismo expediente."),
  "ar": ("مكاتب ومحال ومستودعات للإيجار | XARU HOME",
         "مكاتب ومحال ومستودعات ومساحات صناعية خفيفة مُسعَّرة سنوياً. ويُدار التجهيز والتراخيص والكيان المؤسسي المستأجر ضمن الملف نفسه."),
  "zh": ("写字楼、商铺与仓储空间租赁 | XARU HOME",
         "写字楼、商铺、仓库与轻工业空间，按年报价。装修、执照及承租主体的公司架构在同一档案内处理。"),
 },
 "real-estate/land": {
  "en": ("Development Land, Islands & Mining Concessions | XARU HOME",
         "Development land, coastal and island holdings, agricultural and forestry estates, mining concessions, quarries, energy sites and parcels sized for entire new towns."),
  "es": ("Suelo, islas y concesiones mineras | XARU HOME",
         "Suelo finalista, fincas costeras e insulares, explotaciones agrícolas y forestales, concesiones mineras, canteras, suelo energético y parcelas para ciudades enteras."),
  "ar": ("أراضي التطوير والجزر وامتيازات التعدين | XARU HOME",
         "أراضٍ للتطوير وممتلكات ساحلية وجزرية وضياع زراعية وحرجية وامتيازات تعدين ومحاجر ومواقع طاقة وقطع بحجم مدن كاملة."),
  "zh": ("开发用地、岛屿与采矿权 | XARU HOME",
         "开发用地、海岸与岛屿地产、农林庄园、采矿权与采石场、能源用地，以及可容纳整座新城的地块。"),
 },
 "real-estate/map": {
  "en": ("Property Map — Search by Location | XARU HOME",
         "The XARU HOME inventory read geographically. Pan and zoom to work a market, and switch between map, split and list without losing the filters already set."),
  "es": ("Mapa de propiedades — Buscar por ubicación | XARU HOME",
         "El inventario de XARU HOME leído geográficamente. Desplace y acerque para trabajar un mercado, y cambie entre mapa, vista dividida y lista sin perder los filtros."),
  "ar": ("خريطة العقارات — البحث حسب الموقع | XARU HOME",
         "معروض XARU HOME مقروءاً جغرافياً. حرّك الخريطة وقرّبها لتعمل على سوق بعينه، وبدّل بين الخريطة والعرض المقسّم والقائمة دون فقدان المرشحات."),
  "zh": ("房产地图 — 按位置检索 | XARU HOME",
         "XARU HOME 资产库的地理视图。平移与缩放以聚焦某一市场，并可在地图、分屏与列表之间切换而不丢失已设定的筛选条件。"),
 },

 # ---- inventario historico (Biblia de Real Estate §1.2, §20.5) ---------
 "real-estate/sold": {
  "en": ("Past Operations — Track Record | XARU HOME",
         "Assets that have completed their cycle with XARU HOME. Kept out of the active portfolio and published as a record, not as an offer."),
  "es": ("Operaciones anteriores — Trayectoria | XARU HOME",
         "Activos que han completado su ciclo con XARU HOME. Fuera del portafolio activo, publicados como historial, no como oferta."),
  "ar": ("عمليات سابقة — السجل | XARU HOME",
         "أصول أتمّت دورتها مع XARU HOME. تبقى خارج المحفظة النشطة وتُنشر كسجل، لا كعرض."),
  "zh": ("过往交易 — 业绩记录 | XARU HOME",
         "已与 XARU HOME 完成周期的资产。不计入在售资产组合，作为记录公布而非报价。"),
 },

 # ---- doors & divisions ------------------------------------------------
 "real-estate": {
  "en": ("Luxury Real Estate & Private Islands for Sale | XARU HOME",
         "Private islands, villas, estates and operational hotels for sale worldwide. XARU HOME curates ultra-prime real estate under one structure, from Dubai."),
  "es": ("Inmobiliaria de lujo e islas privadas en venta | XARU HOME",
         "Islas privadas, villas, fincas y hoteles en operación en venta en todo el mundo. XARU HOME reúne inmobiliaria ultra-prime bajo una sola estructura, desde Dubái."),
  "ar": ("عقارات فاخرة وجزر خاصة للبيع | XARU HOME",
         "جزر خاصة وفلل وحوزات وفنادق تشغيلية للبيع حول العالم. تنتقي XARU HOME عقارات فائقة التميّز ضمن بنية واحدة وبمعيار واحد، انطلاقاً من دبي وبسرّية تامّة."),
  "zh": ("奢华房产与私人岛屿在售 | XARU HOME",
         "全球在售的私人岛屿、别墅、庄园与运营中酒店。XARU HOME 以单一架构甄选顶级房产，源自迪拜，全程审慎保密的私人顾问服务。"),
 },
 "real-estate/private-properties": {
  "en": ("Private Islands & Luxury Villas for Sale | XARU HOME",
         "Private islands, villas, castles, estates and branded residences for sale worldwide, curated by XARU HOME and held to a single patrimonial standard."),
  "es": ("Islas privadas y villas de lujo en venta | XARU HOME",
         "Islas privadas, villas, castillos, fincas y residencias de marca en venta en todo el mundo, seleccionadas por XARU HOME bajo un solo estándar patrimonial."),
  "ar": ("جزر خاصة وفلل فاخرة للبيع | XARU HOME",
         "جزر خاصة وفلل وقلاع وحوزات ومساكن ذات علامات للبيع حول العالم، تنتقيها XARU HOME وفق معيار ثرويّ واحد وبسرّية تامّة في كل مرحلة من مراحل الصفقة."),
  "zh": ("私人岛屿与奢华别墅在售 | XARU HOME",
         "全球在售的私人岛屿、别墅、城堡、庄园与品牌住宅，由 XARU HOME 甄选，恪守统一的传承标准，交易全程审慎保密。"),
 },
 "real-estate/commercial-hospitality": {
  "en": ("Operational Hotels & Resorts for Sale | XARU HOME",
         "Operational hotels for sale, resorts, halted projects and income assets worldwide, presented with their true operating state and never as static listings."),
  "es": ("Hoteles en operación y resorts en venta | XARU HOME",
         "Hoteles en operación en venta, resorts, proyectos detenidos y activos de renta en el mundo, presentados con su estado operativo, nunca como fichas estáticas."),
  "ar": ("فنادق تشغيلية ومنتجعات للبيع | XARU HOME",
         "فنادق تشغيلية للبيع ومنتجعات ومشاريع متوقفة وأصول مدرّة للدخل حول العالم، تُعرض بحالتها التشغيلية الحقيقية لا كقوائم جامدة، وبيانات التشغيل بموجب اتفاقية سرّية."),
  "zh": ("运营中酒店与度假村在售 | XARU HOME",
         "全球在售的运营中酒店、度假村、停滞项目与收益型资产，均以真实运营状态呈现，而非静态房源清单；经营数据在保密协议下披露。"),
 },
 "developments": {
  "en": ("Land & Master Development Projects | XARU HOME",
         "Development land for sale and master developments worldwide: territory, real estate project structuring and execution under one responsibility, end to end."),
  "es": ("Suelo y desarrollos maestros a gran escala | XARU HOME",
         "Suelo para desarrollo en venta y desarrollos maestros en el mundo: territorio, estructuración de proyectos inmobiliarios y ejecución bajo una responsabilidad."),
  "ar": ("الأراضي والتطويرات الكبرى | XARU HOME",
         "أراضي تطوير للبيع وتطويرات كبرى حول العالم: الأرض وهيكلة المشاريع العقارية والتنفيذ تحت مسؤولية واحدة، من الرؤية الأولى وحتى التسليم النهائي."),
  "zh": ("土地与总体开发项目 | XARU HOME",
         "全球在售开发用地与总体开发项目：土地、房地产项目架构与执行，统一担责，从最初愿景一路贯穿至最终交付。"),
 },
 "developments/land-master-developments": {
  "en": ("Development Land for Sale & Master Plans | XARU HOME",
         "Development land for sale at territorial scale: coastal, resort and permitted land, master plans and signature destinations, measured in kilometres not metres."),
  "es": ("Suelo para desarrollo en venta y master plans | XARU HOME",
         "Suelo para desarrollo en venta a escala territorial: suelo costero, para resorts y con permisos, master plans y destinos emblemáticos medidos en kilómetros."),
  "ar": ("أراضي تطوير للبيع ومخططات عامة | XARU HOME",
         "أراضي تطوير للبيع على نطاق إقليمي: أراضٍ ساحلية وأراضي منتجعات وأراضٍ مرخّصة ومخططات عامة ووجهات مميّزة تُقاس بالكيلومترات لا بالأمتار المربعة."),
  "zh": ("开发用地在售与总体规划 | XARU HOME",
         "疆域尺度的开发用地在售：滨海用地、度假村用地与已获许可土地，以及总体规划与标志性目的地，以公里而非平米衡量。"),
 },
 "developments/project-structuring": {
  "en": ("Real Estate Project Structuring | XARU HOME",
         "Real estate project structuring end to end: feasibility, legal and fiduciary structuring, SPVs, licensing, operator selection, development and delivery."),
  "es": ("Estructuración de proyectos inmobiliarios | XARU HOME",
         "Estructuración de proyectos inmobiliarios de principio a fin: viabilidad, estructuración jurídica y fiduciaria, SPV, licencias, operador, desarrollo y entrega."),
  "ar": ("هيكلة المشاريع العقارية | XARU HOME",
         "هيكلة المشاريع العقارية من البداية إلى النهاية: الجدوى، والهيكلة القانونية والائتمانية، وكيانات SPV، والتراخيص، واختيار المشغّل، وإدارة التطوير والتسليم."),
  "zh": ("房地产项目架构与开发 | XARU HOME",
         "房地产项目全流程架构：可行性研究、法律与信托架构、SPV 载体、牌照许可、运营商遴选、开发管理，直至最终交付。"),
 },
 "capital": {
  "en": ("Capital for Real Estate Projects | XARU HOME",
         "Capital for real estate projects and projects for capital: a two-way structure with intake, verification, diligence and managed negotiation to closing."),
  "es": ("Capital para proyectos inmobiliarios | XARU HOME",
         "Capital para proyectos inmobiliarios y proyectos para el capital: una estructura de doble vía con admisión, verificación, due diligence y negociación al cierre."),
  "ar": ("رأس مال للمشاريع العقارية | XARU HOME",
         "رأس مال للمشاريع العقارية ومشاريع لرأس المال: بنية ثنائية الاتجاه تقوم على الاستقبال والتحقّق والعناية الواجبة والتفاوض المُدار حتى إغلاق الصفقة."),
  "zh": ("房地产项目资本对接 | XARU HOME",
         "为房地产项目寻资本，为资本寻项目：双向架构，涵盖登记、核验、尽职调查，以及全程管理的谈判直至交割完成。"),
 },
 "capital/strategic-partnerships": {
  "en": ("Real Estate Joint Ventures & Capital | XARU HOME",
         "Joint ventures, co-investment and capital for real estate projects: developers, operators, funds and family offices matched under verified mandate."),
  "es": ("Joint ventures y capital inmobiliario | XARU HOME",
         "Joint ventures, coinversión y capital para proyectos inmobiliarios: desarrolladores, operadores, fondos y family offices unidos bajo mandato verificado."),
  "ar": ("المشاريع المشتركة ورأس المال العقاري | XARU HOME",
         "مشاريع مشتركة واستثمار مشترك ورأس مال للمشاريع العقارية: مطوّرون ومشغّلون وصناديق ومكاتب عائلية يُقرَنون بتفويض موثّق وعناية واجبة كاملة."),
  "zh": ("房地产合资与资本合作 | XARU HOME",
         "合资、共同投资与房地产项目资本：开发商、运营商、基金与家族办公室，在经核实的委托与尽调之下审慎对接。"),
 },
 "capital/deal-room": {
  "en": ("Off-Market Real Estate Opportunities | XARU HOME",
         "Off-market real estate opportunities in a private deal room: public teasers only, then a nine-step route of verification, NDA, KYC and data room access."),
  "es": ("Oportunidades inmobiliarias off-market | XARU HOME",
         "Oportunidades inmobiliarias off-market en una sala de operaciones privada: solo teasers públicos y una ruta de nueve pasos con verificación, NDA, KYC y data room."),
  "ar": ("فرص عقارية خارج السوق | XARU HOME",
         "فرص عقارية خارج السوق في غرفة صفقات خاصة: موجزات علنية فقط، ثم مسار من تسع خطوات يشمل التحقّق واتفاقية السرّية وإجراءات KYC وغرفة البيانات."),
  "zh": ("非公开房产机会 | XARU HOME",
         "私人交易室中的非公开房产机会：对外仅有简报，其后须经九步流程——核验、保密协议、KYC 与数据室授权，依序推进。"),
 },
 "business-infrastructure": {
  "en": ("Business Infrastructure & Company Setup | XARU HOME",
         "Company formation UAE, international relocation, commodities offtake and placement: the corporate infrastructure that continues after the transaction closes."),
  "es": ("Infraestructura empresarial y societaria | XARU HOME",
         "Constitución de sociedades en los EAU, relocalización internacional, offtake y colocación de commodities: la infraestructura que continúa tras la transacción."),
  "ar": ("البنية المؤسسية وتأسيس الشركات | XARU HOME",
         "تأسيس الشركات في الإمارات، والانتقال الدولي، وشراء السلع وتصريفها: البنية المؤسسية التي تستمر بعد إتمام الصفقة، تحت حوكمة واحدة ومعيار واحد."),
  "zh": ("企业基础设施与公司设立 | XARU HOME",
         "阿联酋公司注册、国际迁居、大宗商品包销与分销——交易完成之后仍在延续的企业基础设施，统一治理，同一标准。"),
 },
 "business-infrastructure/trade-financial": {
  "en": ("Commodities Offtake & Placement | XARU HOME",
         "Commodities offtake and placement with productive assets, verified counterparties and financial infrastructure coordinated through authorised partners."),
  "es": ("Offtake y colocación de commodities | XARU HOME",
         "Offtake y colocación de commodities con activos productivos, contrapartes verificadas e infraestructura financiera coordinada mediante partners autorizados."),
  "ar": ("شراء السلع وتصريفها | XARU HOME",
         "اتفاقيات شراء السلع وتصريفها مع أصول إنتاجية وأطراف مقابلة موثّقة وبنية مالية تُنسَّق عبر شركاء وكيانات مرخّصة في كل ولاية قضائية معنيّة."),
  "zh": ("大宗商品包销与分销 | XARU HOME",
         "大宗商品包销与分销，依托生产性资产、经核验的对手方，以及通过获授权伙伴与实体协调的金融基础设施。"),
 },
 "business-infrastructure/corporate-services": {
  "en": ("Company Formation UAE & Relocation | XARU HOME",
         "Company formation UAE and international relocation: entities, banking introductions, licensing, residency and family establishment across jurisdictions."),
  "es": ("Constitución de sociedades EAU y relocalización | XARU HOME",
         "Constitución de sociedades en los EAU y relocalización internacional: entidades, banca, licencias, residencia y establecimiento familiar entre jurisdicciones."),
  "ar": ("تأسيس الشركات في الإمارات والانتقال | XARU HOME",
         "تأسيس الشركات في الإمارات والانتقال الدولي: الكيانات، والتعريف المصرفي، والتراخيص، والإقامة، وتوطين العائلة عبر ولايات قضائية متعدّدة وبتنسيق واحد."),
  "zh": ("阿联酋公司注册与国际迁居 | XARU HOME",
         "阿联酋公司注册与国际迁居：实体设立、银行引荐、牌照许可、居留身份与家庭安置，跨司法管辖区一体推进。"),
 },

 # ---- company & insights hub ------------------------------------------
 "company": {
  "en": ("About XARU HOME | The Company & Its Structure",
         "About XARU HOME: three levels, seven autonomous divisions, the entities it operates under, its governance, its offices and the standard behind every mandate."),
  "es": ("Acerca de XARU HOME | La compañía y su estructura",
         "Acerca de XARU HOME: tres niveles, siete divisiones autónomas, las entidades bajo las que opera, su gobernanza, sus oficinas y el estándar de cada mandato."),
  "ar": ("عن XARU HOME | الشركة وبنيتها",
         "عن XARU HOME: ثلاثة مستويات وسبعة أقسام مستقلّة، والكيانات التي تعمل تحتها، وحوكمتها ومكاتبها والمعايير التي تحكم كل تفويض تقبله المجموعة."),
  "zh": ("关于 XARU HOME | 公司与架构",
         "关于 XARU HOME：三个层级、七个自主板块，其运营所依托的实体、治理机制与办公网络，以及贯穿每一项委托的执业标准。"),
 },
 "insights": {
  "en": ("Real Estate & Capital Insights | XARU HOME",
         "Research from XARU HOME on luxury real estate, territorial land, operational hospitality, private capital and international establishment: seven sectors."),
  "es": ("Análisis de inmobiliaria y capital | XARU HOME",
         "Análisis de XARU HOME sobre inmobiliaria de lujo, suelo territorial, hospitality operativo, capital privado y establecimiento internacional: siete sectores."),
  "ar": ("رؤى العقارات ورأس المال | XARU HOME",
         "أبحاث XARU HOME في العقارات الفاخرة والأرض الإقليمية والضيافة التشغيلية ورأس المال الخاص والتأسيس الدولي — سبعة قطاعات وانضباط تحليلي واحد."),
  "zh": ("房地产与资本洞察 | XARU HOME",
         "XARU HOME 关于奢华房产、疆域级土地、运营型酒店资产、私人资本与国际落地的研究——七个板块，同一分析纪律。"),
 },

 # ---- catalogue & forms ------------------------------------------------
 "opportunities": {
  "en": ("Development Land & Project Opportunities | XARU HOME",
         "Development land for sale, master plans, halted projects and capital opportunities under live mandate, measured in kilometres, phases and mandates."),
  "es": ("Suelo, proyectos y oportunidades de inversión | XARU HOME",
         "Suelo para desarrollo en venta, master plans, proyectos detenidos y oportunidades de capital bajo mandato activo, medidos en kilómetros, fases y mandatos."),
  "ar": ("الأراضي والمشاريع وفرص الاستثمار | XARU HOME",
         "أراضي تطوير للبيع ومخططات عامة ومشاريع متوقفة وفرص رأسمالية بتفويض نشط — تُقاس بالكيلومترات والمراحل والتفويضات، لا بالأمتار المربعة."),
  "zh": ("土地、项目与投资机会 | XARU HOME",
         "在册委托下的开发用地在售、总体规划、停滞项目与资本机会——以公里、阶段与委托衡量，而非以平方米衡量。"),
 },
 "opportunities/submit": {
  "en": ("Submit a Property or Project Opportunity | XARU HOME",
         "Submit an opportunity to XARU HOME: an asset, a project or capital. Two confidential routes, one standard of verification, reviewed against live mandates."),
  "es": ("Presentar una propiedad o un proyecto | XARU HOME",
         "Presente una oportunidad a XARU HOME: un activo, un proyecto o capital. Dos rutas confidenciales, un solo estándar de verificación y revisión por mandato."),
  "ar": ("تقديم عقار أو مشروع | XARU HOME",
         "قدّم فرصة إلى XARU HOME: أصلاً أو مشروعاً أو رأس مال. مساران سرّيان ومعيار تحقّق واحد، وتُراجَع كل فرصة مقابل التفويضات النشطة لدى المجموعة."),
  "zh": ("提交房产或项目机会 | XARU HOME",
         "向 XARU HOME 提交机会：资产、项目或资本。两条保密路径，同一核验标准，并对照在册委托逐一审阅。"),
 },
 "private-enquiry": {
  "en": ("Private Enquiry | XARU HOME Advisory Desk",
         "One conversation, one structure, total confidentiality. Open a private enquiry with the XARU HOME desk on property, capital, development or relocation."),
  "es": ("Consulta privada | Mesa de asesoría XARU HOME",
         "Una conversación, una estructura, confidencialidad total. Abra una consulta privada con la mesa de XARU HOME: propiedad, capital, desarrollo o relocalización."),
  "ar": ("استفسار خاص | مكتب XARU HOME للاستشارة",
         "محادثة واحدة وبنية واحدة وسرّية تامّة. افتح استفساراً خاصاً مع مكتب XARU HOME حول العقار أو رأس المال أو التطوير أو الانتقال الدولي."),
  "zh": ("私人咨询 | XARU HOME 顾问服务台",
         "一次对话、单一架构、全然保密。就房产、资本、开发或迁居事宜，向 XARU HOME 私人服务台发起保密咨询。"),
 },

 # ---- insights articles ------------------------------------------------
 "insights/operational-hospitality": {
  "en": ("Operational Hotels: The Asset That Earns | XARU HOME",
         "Operational hotels for sale are priced on their P&L, not their postcard. XARU HOME Research on hospitality as an asset class, repositioning and discretion."),
  "es": ("Hoteles en operación: el activo que renta | XARU HOME",
         "Los hoteles en operación se valoran por su P&L, no por su postal. Análisis de XARU HOME Research sobre hospitality como clase de activo y reposicionamiento."),
  "ar": ("الضيافة التشغيلية: الأصل الذي يُدرّ | XARU HOME",
         "الفنادق التشغيلية تُقيَّم بقائمة أرباحها لا بصورتها البريدية. تحليل من XARU HOME Research حول الضيافة كفئة أصول وإعادة التموضع والوساطة المنضبطة."),
  "zh": ("运营型酒店：先创收的资产 | XARU HOME",
         "运营中酒店以损益表定价，而非以风景定价。XARU HOME Research 解析酒店作为资产类别、重新定位与有纪律的中介之道。"),
 },
 "insights/territorial-land": {
  "en": ("Territorial Land: When Scale Is the Thesis | XARU HOME",
         "When development land for sale becomes a territory, the question changes from what can be built to what can be founded. XARU HOME Research on land at scale."),
  "es": ("Suelo territorial: cuando la escala es la tesis | XARU HOME",
         "Cuando el suelo en venta se vuelve territorio, la pregunta cambia: de qué se puede construir a qué se puede fundar. Análisis de XARU HOME Research sobre escala."),
  "ar": ("الأرض الإقليمية: حين يكون الحجم أطروحة | XARU HOME",
         "حين تتحوّل أرض التطوير المعروضة إلى إقليم، يتغيّر السؤال من ماذا يمكن بناؤه إلى ماذا يمكن تأسيسه. تحليل من XARU HOME Research حول الأرض بالحجم الكبير."),
  "zh": ("疆域级土地：规模即命题 | XARU HOME",
         "当在售开发用地成为一片疆域，问题便从「能建什么」转为「能开创什么」。XARU HOME Research 解析大尺度土地的价值逻辑。"),
 },
 "insights/capital-halted-projects": {
  "en": ("Private Capital for Halted Projects | XARU HOME",
         "A halted project is rarely a bad project, usually a broken structure. XARU HOME Research on private capital, restructuring and the discipline of re-entry."),
  "es": ("Capital privado y proyectos detenidos | XARU HOME",
         "Un proyecto detenido rara vez es un mal proyecto: suele ser una estructura rota. Análisis de XARU HOME Research sobre capital privado y reestructuración."),
  "ar": ("رأس المال الخاص والمشاريع المتوقفة | XARU HOME",
         "المشروع المتوقف نادراً ما يكون مشروعاً سيئاً — بل بنية معطوبة في الغالب. تحليل من XARU HOME Research حول رأس المال الخاص وإعادة الهيكلة والدخول المنضبط."),
  "zh": ("私人资本与停滞项目 | XARU HOME",
         "停滞的项目很少是坏项目，多半是架构失灵。XARU HOME Research 解析私人资本、重组路径与重新进场的纪律。"),
 },
 "insights/international-establishment": {
  "en": ("International Establishment & Residency | XARU HOME",
         "Company formation UAE, entities, banking and residency: international relocation works when the entity, the family and the operation are structured as one."),
  "es": ("Establecimiento internacional y residencia | XARU HOME",
         "Constitución de sociedades en los EAU, entidades, banca y residencia: la relocalización funciona cuando entidad, familia y operación se estructuran a la vez."),
  "ar": ("التأسيس الدولي والإقامة | XARU HOME",
         "تأسيس الشركات في الإمارات والكيانات والخدمات المصرفية والإقامة: ينجح الانتقال الدولي حين تُهيكَل الكيان والعائلة والتشغيل معاً كوحدة واحدة متماسكة."),
  "zh": ("国际落地与居留身份 | XARU HOME",
         "阿联酋公司注册、实体、银行与居留：唯有将实体、家庭与运营一并架构，国际迁居才真正落地生根。"),
 },

 # ---- asset records (fichas) ------------------------------------------
 "real-estate/private-properties/pp-samana-island": {
  "en": ("Private Island for Sale, Samaná Bay | XARU HOME",
         "A private island for sale in Samaná Bay, Dominican Republic. Full particulars and price upon application through the XARU HOME private desk, in confidence."),
  "es": ("Isla privada en venta, Bahía de Samaná | XARU HOME",
         "Isla privada en venta en la Bahía de Samaná, República Dominicana. Detalles completos y precio a consultar a través de la mesa privada de XARU HOME."),
  "ar": ("جزيرة خاصة للبيع، خليج سامانا | XARU HOME",
         "جزيرة خاصة للبيع في خليج سامانا بجمهورية الدومينيكان. التفاصيل الكاملة والسعر عند الطلب عبر المكتب الخاص لـ XARU HOME، وبسرّية تامّة."),
  "zh": ("萨马纳湾私人岛屿在售 | XARU HOME",
         "多米尼加共和国萨马纳湾一处私人岛屿在售。完整资料与价格面议，经由 XARU HOME 私人服务台保密提供。"),
 },
 "real-estate/private-properties/pp-villa-dubai": {
  "en": ("Signature Villa for Sale in Dubai | XARU HOME",
         "A signature luxury villa for sale in Dubai, United Arab Emirates. Key facts, private viewing and price upon application through the XARU HOME private desk."),
  "es": ("Villa de autor en venta en Dubái | XARU HOME",
         "Villa de lujo de autor en venta en Dubái, Emiratos Árabes Unidos. Datos clave, visita privada y precio a consultar en la mesa privada de XARU HOME."),
  "ar": ("فيلا مميّزة للبيع في دبي | XARU HOME",
         "فيلا فاخرة مميّزة للبيع في دبي بالإمارات العربية المتحدة. الحقائق الأساسية ومعاينة خاصة والسعر عند الطلب عبر المكتب الخاص لـ XARU HOME."),
  "zh": ("迪拜臻品别墅在售 | XARU HOME",
         "阿联酋迪拜一处臻品奢华别墅在售。关键信息、私人看房与价格面议，均由 XARU HOME 私人服务台安排。"),
 },
 "real-estate/private-properties/pp-penthouse-london": {
  "en": ("Penthouse for Sale, Central London | XARU HOME",
         "A penthouse for sale in central London. Key facts, discreet viewing and price upon application through the XARU HOME private desk, with worldwide advisory."),
  "es": ("Ático en venta, centro de Londres | XARU HOME",
         "Ático en venta en el centro de Londres. Datos clave, visita discreta y precio a consultar a través de la mesa privada de XARU HOME, con asesoría global."),
  "ar": ("بنتهاوس للبيع، وسط لندن | XARU HOME",
         "بنتهاوس للبيع في وسط لندن. الحقائق الأساسية ومعاينة حصيفة والسعر عند الطلب عبر المكتب الخاص لـ XARU HOME، مع استشارة عالمية شاملة."),
  "zh": ("伦敦中心顶层公寓在售 | XARU HOME",
         "伦敦市中心一处顶层公寓在售。关键信息、审慎看房与价格面议，由 XARU HOME 私人服务台提供全球顾问支持。"),
 },
 "real-estate/private-properties/pp-villa-como": {
  "en": ("Lakefront Estate for Sale, Lake Como | XARU HOME",
         "A lakefront estate for sale on Lake Como, Lombardy, Italy. Key facts, private viewing and price upon application through the XARU HOME private desk."),
  "es": ("Finca junto al lago en venta, Lago de Como | XARU HOME",
         "Finca junto al lago en venta en el Lago de Como, Lombardía, Italia. Datos clave, visita privada y precio a consultar en la mesa privada de XARU HOME."),
  "ar": ("حوزة على البحيرة للبيع، بحيرة كومو | XARU HOME",
         "حوزة على ضفاف بحيرة كومو للبيع في لومبارديا بإيطاليا. الحقائق الأساسية ومعاينة خاصة والسعر عند الطلب عبر المكتب الخاص لـ XARU HOME."),
  "zh": ("科莫湖畔庄园在售 | XARU HOME",
         "意大利伦巴第大区科莫湖畔一处庄园在售。关键信息、私人看房与价格面议，经由 XARU HOME 私人服务台安排。"),
 },
 "real-estate/private-properties/pp-casa-tulum": {
  "en": ("Beachfront Residence for Sale, Tulum | XARU HOME",
         "A beachfront residence for sale in Tulum, Quintana Roo, Mexico. Key facts, private viewing and price upon application through the XARU HOME private desk."),
  "es": ("Residencia frente al mar en venta, Tulum | XARU HOME",
         "Residencia frente al mar en venta en Tulum, Quintana Roo, México. Datos clave, visita privada y precio a consultar en la mesa privada de XARU HOME."),
  "ar": ("مسكن على الشاطئ للبيع، تولوم | XARU HOME",
         "مسكن على الشاطئ للبيع في تولوم بولاية كينتانا رو، المكسيك. الحقائق الأساسية ومعاينة خاصة والسعر عند الطلب عبر المكتب الخاص لـ XARU HOME."),
  "zh": ("图卢姆海滨住宅在售 | XARU HOME",
         "墨西哥金塔纳罗奥州图卢姆一处海滨住宅在售。关键信息、私人看房与价格面议，经由 XARU HOME 私人服务台安排。"),
 },
 "real-estate/private-properties/pp-villa-marbella": {
  "en": ("Villa for Sale, Marbella Golden Mile | XARU HOME",
         "A villa for sale on the Marbella Golden Mile, Andalusia, Spain. Key facts, private viewing and price upon application through the XARU HOME private desk."),
  "es": ("Villa en venta, Milla de Oro de Marbella | XARU HOME",
         "Villa en venta en la Milla de Oro de Marbella, Andalucía, España. Datos clave, visita privada y precio a consultar en la mesa privada de XARU HOME."),
  "ar": ("فيلا للبيع، الميل الذهبي بماربيا | XARU HOME",
         "فيلا للبيع في الميل الذهبي بماربيا، الأندلس، إسبانيا. الحقائق الأساسية ومعاينة خاصة والسعر عند الطلب عبر المكتب الخاص لـ XARU HOME."),
  "zh": ("马贝拉黄金一英里别墅在售 | XARU HOME",
         "西班牙安达卢西亚马贝拉黄金一英里一处别墅在售。关键信息、私人看房与价格面议，经由 XARU HOME 私人服务台安排。"),
 },
 "real-estate/commercial-hospitality/ch-hotel-operational": {
  "en": ("Operational Hotel for Sale, Riviera Maya | XARU HOME",
         "An operational boutique hotel for sale in the Riviera Maya, Mexico. Region, category and status are public; the operating statement is released only under NDA."),
  "es": ("Hotel en operación en venta, Riviera Maya | XARU HOME",
         "Hotel boutique en operación en venta en la Riviera Maya, México. Región, categoría y estado públicos; la cuenta de explotación se libera solo bajo NDA."),
  "ar": ("فندق تشغيلي للبيع، ريفييرا مايا | XARU HOME",
         "فندق بوتيك تشغيلي للبيع في ريفييرا مايا بالمكسيك. المنطقة والفئة والحالة علنية؛ ولا تُسلَّم بيانات التشغيل إلا بموجب اتفاقية سرّية موقّعة."),
  "zh": ("运营中酒店在售，玛雅海岸 | XARU HOME",
         "墨西哥玛雅海岸一家运营中精品酒店在售。地区、类别与状态公开；经营报表仅在签署保密协议之后披露。"),
 },
 "real-estate/commercial-hospitality/ch-hotel-halted": {
  "en": ("Halted Hotel Project, Panama City | XARU HOME",
         "A halted hotel project in Panama City seeking capital or a developer. Treated honestly as a restructuring situation, with its own diligence and capital route."),
  "es": ("Proyecto hotelero detenido, Ciudad de Panamá | XARU HOME",
         "Proyecto hotelero detenido en Ciudad de Panamá en busca de capital o desarrollador. Tratado como situación de reestructuración, con su propia ruta de capital."),
  "ar": ("مشروع فندقي متوقف، مدينة بنما | XARU HOME",
         "مشروع فندقي متوقف في مدينة بنما يبحث عن رأس مال أو مطوّر. يُعامَل بصدق كحالة إعادة هيكلة، بعنايته الواجبة الخاصة ومسار رأس المال الخاص به."),
  "zh": ("停滞酒店项目，巴拿马城 | XARU HOME",
         "巴拿马城一处停滞酒店项目，寻求资本或开发商。如实按重组事项对待，配以独立尽调与独立的资本路径。"),
 },
 "real-estate/commercial-hospitality/ch-resort-development": {
  "en": ("Beach Resort Development, Punta Cana | XARU HOME",
         "A beach resort at development stage in Punta Cana, Dominican Republic. Phase, structure and counterparty sought disclosed; particulars under mandate only."),
  "es": ("Resort de playa en desarrollo, Punta Cana | XARU HOME",
         "Resort de playa en fase de desarrollo en Punta Cana, República Dominicana. Fase, estructura y contraparte buscada; los detalles, bajo mandato y en privado."),
  "ar": ("منتجع شاطئي قيد التطوير، بونتا كانا | XARU HOME",
         "منتجع شاطئي في مرحلة التطوير ببونتا كانا، جمهورية الدومينيكان. المرحلة والهيكل والطرف المقابل المطلوب معلنة؛ والتفاصيل بموجب تفويض وبسرّية."),
  "zh": ("海滨度假村开发项目，蓬塔卡纳 | XARU HOME",
         "多米尼加共和国蓬塔卡纳一处开发阶段的海滨度假村。阶段、结构与所寻对手方公开；详细资料在委托之下保密提供。"),
 },
 "opportunities/lp-land-11m": {
  "en": ("Development Land for Sale, Oaxaca Coast | XARU HOME",
         "Territorial development land for sale on the Oaxaca coast, Mexico: over 11 million m² held in one title. Tenure, access and planning released under mandate."),
  "es": ("Suelo para desarrollo en venta, costa de Oaxaca | XARU HOME",
         "Reserva territorial en venta en la costa de Oaxaca, México: más de 11 millones de m² en un solo título. Tenencia, acceso y urbanismo, bajo mandato privado."),
  "ar": ("أرض تطوير للبيع، ساحل واهاكا | XARU HOME",
         "أرض تطوير إقليمية للبيع على ساحل واهاكا بالمكسيك — أكثر من 11 مليون متر مربع بسند واحد. الحيازة والوصول والتخطيط تُفصح بموجب تفويض."),
  "zh": ("开发用地在售，瓦哈卡海岸 | XARU HOME",
         "墨西哥瓦哈卡海岸一宗疆域级开发用地在售——逾 1100 万平方米，单一权属。权属、交通与规划资料在委托之下提供。"),
 },
 "opportunities/lp-ashima-masterplan": {
  "en": ("ASHIMA Master Development, Oaxaca | XARU HOME",
         "ASHIMA, a signature master development in Oaxaca, Mexico: a territory becoming a destination, structured around health, culture, ecology and innovation."),
  "es": ("ASHIMA, desarrollo maestro en Oaxaca | XARU HOME",
         "ASHIMA: desarrollo maestro emblemático en Oaxaca, México. Un territorio que se vuelve destino, estructurado en salud, cultura, ecología e innovación."),
  "ar": ("ASHIMA، تطوير رئيسي في واهاكا | XARU HOME",
         "ASHIMA — تطوير رئيسي مميّز في واهاكا بالمكسيك: أرضٌ تتحوّل إلى وجهة، مُهيكَلة حول الصحة والثقافة والبيئة والابتكار والتنمية المستدامة."),
  "zh": ("ASHIMA 标志性总体开发，瓦哈卡 | XARU HOME",
         "ASHIMA——墨西哥瓦哈卡的标志性总体开发：一片从疆域走向目的地的土地，以健康、文化、生态与创新为架构。"),
 },
 "opportunities/cf-confidential-portfolio": {
  "en": ("Confidential Off-Market Portfolio | XARU HOME",
         "A confidential portfolio of off-market real estate opportunities. Public teaser only; identities, financials and price travel the private deal room route."),
  "es": ("Portafolio confidencial off-market | XARU HOME",
         "Portafolio confidencial de oportunidades inmobiliarias off-market. Solo teaser público; identidades, cifras y precio viajan por la sala de operaciones privada."),
  "ar": ("محفظة سرّية خارج السوق | XARU HOME",
         "محفظة سرّية من الفرص العقارية خارج السوق. موجز علني فقط؛ أما الهويات والأرقام والسعر فتسلك مسار غرفة الصفقات الخاصة بخطواته التسع كاملة."),
  "zh": ("保密非公开资产组合 | XARU HOME",
         "一组非公开房产机会的保密资产组合。对外仅有简报；身份、财务与价格须经私人交易室路径逐步披露。"),
 },
 "opportunities/pa-quarry-license": {
  "en": ("Quarry Licence & Aggregates Asset | XARU HOME",
         "A licensed quarry and aggregates production asset in the Caribbean, Dominican Republic. A productive asset with offtake and placement managed under mandate."),
  "es": ("Licencia de cantera y producción de áridos | XARU HOME",
         "Cantera con licencia y producción de áridos en el Caribe, República Dominicana. Activo productivo con offtake y colocación gestionados bajo mandato."),
  "ar": ("رخصة محجر وإنتاج ركام | XARU HOME",
         "محجر مرخّص وأصل لإنتاج الركام في منطقة الكاريبي بجمهورية الدومينيكان. أصل إنتاجي مع اتفاقيات شراء وتصريف تُدار بموجب تفويض واضح."),
  "zh": ("采石许可与骨料资产 | XARU HOME",
         "位于多米尼加共和国加勒比地区的持牌采石场与骨料生产资产。生产性资产，包销与分销在委托之下统一管理。"),
 },
}

# ---------------------------------------------------------------- og:image per slug
SHELL_OG_IMG = {
 "real-estate": "07_villa_dubai.jpg",
 "real-estate/private-properties": "09_villa_como.jpg",
 "real-estate/commercial-hospitality": "05_hotel_project.jpg",
 "developments": "03_land_mega.jpg",
 "developments/land-master-developments": "06_masterplan_ashima.jpg",
 "developments/project-structuring": "04_resort_dev.jpg",
 "capital": "13_investment_bg.jpg",
 "capital/strategic-partnerships": "13_investment_bg.jpg",
 "capital/deal-room": "08_penthouse_london.jpg",
 "business-infrastructure": "05_hotel_project.jpg",
 "business-infrastructure/trade-financial": "14_cta_bg.jpg",
 "business-infrastructure/corporate-services": "26_corporate_services.jpg",
 "company": "30_company.jpg",
 "insights": "10_casa_tulum.jpg",
 "opportunities": "03_land_mega.jpg",
 "opportunities/submit": "14_cta_bg.jpg",
 "private-enquiry": "13_investment_bg.jpg",
 "insights/operational-hospitality": "05_hotel_project.jpg",
 "insights/territorial-land": "03_land_mega.jpg",
 "insights/capital-halted-projects": "13_investment_bg.jpg",
 "insights/international-establishment": "14_cta_bg.jpg",
 "real-estate/private-properties/pp-samana-island": "02_island_rd.jpg",
 "real-estate/private-properties/pp-villa-dubai": "07_villa_dubai.jpg",
 "real-estate/private-properties/pp-penthouse-london": "08_penthouse_london.jpg",
 "real-estate/private-properties/pp-villa-como": "09_villa_como.jpg",
 "real-estate/private-properties/pp-casa-tulum": "10_casa_tulum.jpg",
 "real-estate/private-properties/pp-villa-marbella": "11_villa_marbella.jpg",
 "real-estate/commercial-hospitality/ch-hotel-operational": "05_hotel_project.jpg",
 "real-estate/commercial-hospitality/ch-hotel-halted": "05_hotel_project.jpg",
 "real-estate/commercial-hospitality/ch-resort-development": "04_resort_dev.jpg",
 "opportunities/lp-land-11m": "03_land_mega.jpg",
 "opportunities/lp-ashima-masterplan": "06_masterplan_ashima.jpg",
 "opportunities/cf-confidential-portfolio": "13_investment_bg.jpg",
 "opportunities/pa-quarry-license": "03_land_mega.jpg",
}

def shell_meta(lang, slug, fallback_title=None, fallback_desc=None):
    """(title, description) for a Phase 1-5 folder page. Falls back to the
    generator-supplied strings when a slug has no curated entry yet."""
    e = SHELL_SEO.get(slug)
    if not e:
        return fallback_title, fallback_desc
    return e[lang]

def shell_social(lang, slug, title, desc):
    """og: + twitter: block for a folder page (already-escaped values)."""
    t, d = esc(title), esc(desc)
    url = shell_url(lang, slug)
    img = _G2 + SHELL_OG_IMG[slug] if slug in SHELL_OG_IMG else COVER
    kind = "article" if slug.startswith("insights/") else "website"
    return "\n    ".join([
      '<meta property="og:type" content="%s">' % kind,
      '<meta property="og:site_name" content="XARU HOME">',
      '<meta property="og:locale" content="%s">' % OG_LOCALE[lang],
      '<meta property="og:title" content="%s">' % t,
      '<meta property="og:description" content="%s">' % d,
      '<meta property="og:url" content="%s">' % url,
      '<meta property="og:image" content="%s">' % img,
      '<meta property="og:image:width" content="1200">',
      '<meta property="og:image:height" content="630">',
      '<meta name="twitter:card" content="summary_large_image">',
      '<meta name="twitter:title" content="%s">' % t,
      '<meta name="twitter:description" content="%s">' % d,
      '<meta name="twitter:image" content="%s">' % img,
    ])

# ---------------------------------------------------------------- JSON-LD for the new pages
def shell_breadcrumb(lang, slug):
    """Home > ...ancestors... > page, built from the slug path itself."""
    items = [{"@type": "ListItem", "position": 1,
              "name": _L["home"][lang], "item": BASE[lang]}]
    parts = slug.split("/")
    for i in range(1, len(parts) + 1):
        s = "/".join(parts[:i])
        if s not in SLUG_LABEL:
            continue
        items.append({"@type": "ListItem", "position": len(items) + 1,
                      "name": SLUG_LABEL[s][lang], "item": shell_url(lang, s)})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "inLanguage": INLANG[lang], "itemListElement": items}

# division / door pillars that carry a Service block, with their English serviceType
SHELL_SERVICE = {
 "real-estate":                                "Luxury real estate brokerage",
 "real-estate/private-properties":             "Private islands and luxury residential brokerage",
 "real-estate/commercial-hospitality":         "Hotel, resort and hospitality asset brokerage",
 "developments":                               "Land and master development advisory",
 "developments/land-master-developments":      "Development land brokerage and master planning",
 "developments/project-structuring":           "Real estate project structuring and fiduciary structuring",
 "capital":                                    "Capital for real estate projects",
 "capital/strategic-partnerships":             "Joint ventures and real estate capital placement",
 "capital/deal-room":                          "Off-market real estate opportunities",
 "business-infrastructure":                    "Corporate infrastructure and international establishment",
 "business-infrastructure/trade-financial":    "Commodities offtake and placement",
 "business-infrastructure/corporate-services": "Company formation UAE and international relocation",
}

def shell_service(lang, slug):
    title, desc = SHELL_SEO[slug][lang]
    return {
     "@context": "https://schema.org",
     "@type": "Service",
     "name": SLUG_LABEL[slug][lang],
     "serviceType": SHELL_SERVICE[slug],
     "provider": {"@id": ORG_ID},
     "areaServed": "Worldwide",
     "description": desc,
     "inLanguage": INLANG[lang],
     "url": shell_url(lang, slug),
    }

# the 3 catalogues and the asset records they list
SHELL_ITEMLIST = {
 "real-estate/private-properties": [
   "real-estate/private-properties/pp-samana-island",
   "real-estate/private-properties/pp-villa-dubai",
   "real-estate/private-properties/pp-penthouse-london",
   "real-estate/private-properties/pp-villa-como",
   "real-estate/private-properties/pp-casa-tulum",
   "real-estate/private-properties/pp-villa-marbella"],
 "real-estate/commercial-hospitality": [
   "real-estate/commercial-hospitality/ch-hotel-operational",
   "real-estate/commercial-hospitality/ch-hotel-halted",
   "real-estate/commercial-hospitality/ch-resort-development"],
 "opportunities": [
   "opportunities/lp-land-11m",
   "opportunities/lp-ashima-masterplan",
   "opportunities/cf-confidential-portfolio",
   "opportunities/pa-quarry-license"],
}

def shell_itemlist(lang, slug):
    items = []
    for i, child in enumerate(SHELL_ITEMLIST[slug], start=1):
        items.append({"@type": "ListItem", "position": i,
                      "name": SLUG_LABEL[child][lang],
                      "url": shell_url(lang, child)})
    return {"@context": "https://schema.org", "@type": "ItemList",
            "name": SLUG_LABEL[slug][lang],
            "inLanguage": INLANG[lang],
            "numberOfItems": len(items),
            "itemListOrder": "https://schema.org/ItemListUnordered",
            "itemListElement": items}

# the four foundational Insights analyses
ARTICLE_META = {
 "insights/operational-hospitality":     ("2026-02-10", "Hospitality"),
 "insights/territorial-land":            ("2026-03-18", "Land"),
 "insights/capital-halted-projects":     ("2026-04-22", "Capital"),
 "insights/international-establishment": ("2026-05-27", "International establishment"),
}
ARTICLE_MODIFIED = "2026-07-31"
RESEARCH_AUTHOR = "XARU HOME Research"

def shell_article(lang, slug):
    published, section = ARTICLE_META[slug]
    title, desc = SHELL_SEO[slug][lang]
    headline = SHELL_SEO[slug][lang][0].split(" | ")[0]
    return {
     "@context": "https://schema.org",
     "@type": "Article",
     "headline": headline,
     "description": desc,
     "inLanguage": INLANG[lang],
     "datePublished": published,
     "dateModified": ARTICLE_MODIFIED,
     "articleSection": section,
     "author": {"@type": "Organization", "name": RESEARCH_AUTHOR,
                "url": BASE[lang] + "insights/"},
     "publisher": {"@type": "Organization", "name": "XARU HOME",
                   "logo": {"@type": "ImageObject", "url": LOGO}},
     "image": _G2 + SHELL_OG_IMG[slug],
     "isPartOf": {"@type": "Blog", "name": SLUG_LABEL["insights"][lang],
                  "url": shell_url(lang, "insights")},
     "mainEntityOfPage": {"@type": "WebPage", "@id": shell_url(lang, slug)},
     "url": shell_url(lang, slug),
    }

def shell_jsonld(lang, slug):
    """Comment-wrapped JSON-LD payload for a Phase 1-5 folder page.
    Every block is json.dumps'd and re-parsed by _script() before emission."""
    blocks = [website(lang)]
    if slug in SLUG_LABEL:
        blocks.append(shell_breadcrumb(lang, slug))
    if slug in SHELL_SERVICE:
        blocks.append(shell_service(lang, slug))
    if slug in SHELL_ITEMLIST:
        blocks.append(shell_itemlist(lang, slug))
    if slug in ARTICLE_META:
        blocks.append(shell_article(lang, slug))
    parts = "\n".join("    " + _script(b).replace("\n", "\n    ") for b in blocks)
    return "    <!-- XARU JSON-LD -->\n" + parts + "\n    <!-- /XARU JSON-LD -->"

# ---------------------------------------------------------------- sitemap inventory
# Live .html pages (old core) — blog.html / blog-details.html excluded: they
# now redirect to /insights/.
SITEMAP_HTML = [
 ("index.html", "1.0"),
 ("property-listing-buy.html", "0.9"),
 ("property-listing-rent.html", "0.7"),
 ("property-listing-search.html", "0.7"),
 ("property-details.html", "0.6"),
 ("contact.html", "0.7"),
 ("faq.html", "0.6"),
]

SITEMAP_PRIORITY = {
 "real-estate": "0.9", "developments": "0.9", "capital": "0.9",
 "business-infrastructure": "0.9", "company": "0.8", "insights": "0.8",
 "opportunities": "0.9", "private-enquiry": "0.7", "opportunities/submit": "0.7",
 # rutas de resultados: son la puerta de entrada real al inventario
 "real-estate/search": "0.9", "real-estate/buy": "0.9", "real-estate/rent": "0.8",
 "real-estate/commercial/buy": "0.8", "real-estate/commercial/rent": "0.7",
 "real-estate/land": "0.8", "real-estate/map": "0.7",
 "real-estate/agents": "0.7", "real-estate/agencies": "0.7", "real-estate/developers": "0.7",
 "real-estate/new-projects": "0.8",
 "real-estate/account": "0.4", "real-estate/office": "0.4",
 "real-estate/administration": "0.3",
}

def sitemap_entries():
    """[(path_without_language_prefix, priority)] for every live URL, in order.
    Home + folder pages use clean URLs; legacy core pages keep their .html."""
    out = []
    for fname, pr in SITEMAP_HTML:
        out.append(("" if fname == "index.html" else fname, pr))
    for slug in sorted(SHELL_SEO):
        depth = slug.count("/")
        pr = SITEMAP_PRIORITY.get(slug, "0.8" if depth == 1 else "0.6")
        out.append((slug + "/", pr))
    return out

# ---------------------------------------------------------------- utility / account pages
# Legacy template pages that are not part of the public architecture: they get a
# unique title + description (no duplicate titles sitewide) and are kept out of
# the index with robots noindex, follow. English root only.
UTILITY_META = {
 "login.html": ("Client Login | XARU HOME Private Portal",
                "Sign in to the XARU HOME private client portal to review saved properties, mandates and documents shared by your advisor."),
 "register.html": ("Create an Account | XARU HOME Private Portal",
                   "Create a XARU HOME private portal account to save properties, follow mandates and receive confidential updates from your advisor."),
 "forgot-password.html": ("Reset Your Password | XARU HOME Portal",
                          "Reset the password of your XARU HOME private portal account. A secure reset link is sent to the email address on file."),
 "change-password.html": ("Change Your Password | XARU HOME Portal",
                          "Change the password of your XARU HOME private portal account and keep access to your mandates and documents secure."),
 "profile.html": ("Your Profile | XARU HOME Private Portal",
                  "Your XARU HOME private portal profile: contact details, preferences and the mandates your advisor has shared with you."),
 "profile-settings.html": ("Profile Settings | XARU HOME Private Portal",
                           "Manage the settings of your XARU HOME private portal profile: contact details, notification preferences and privacy options."),
 "my-property.html": ("Your Properties | XARU HOME Private Portal",
                      "The properties registered under your XARU HOME private portal account, with their current status and advisor notes."),
 "favourite-property.html": ("Saved Properties | XARU HOME Private Portal",
                             "The properties you have saved in the XARU HOME private portal, ready to review or share with your advisor."),
 "add-property.html": ("Add a Property | XARU HOME Private Portal",
                       "Register a property in the XARU HOME private portal so your advisor can review it and open the corresponding mandate."),
 "edit-property.html": ("Edit a Property | XARU HOME Private Portal",
                        "Update the particulars of a property registered in the XARU HOME private portal before it is reviewed by your advisor."),
 "client-list.html": ("Client Directory | XARU HOME Private Portal",
                      "The client directory of the XARU HOME private portal, reserved for advisors operating under an active XARU HOME mandate."),
 "error.html": ("Page Not Available | XARU HOME",
                "This XARU HOME page is not available. Return to the homepage or contact the private desk and we will point you to the right place."),
}

def set_utility_head(h, fname):
    """Unique title/description + noindex for a legacy utility page."""
    title, desc = UTILITY_META[fname]
    t, d = esc(title), esc(desc)
    h = re.sub(r'<title>.*?</title>', lambda m: '<title>%s</title>' % t, h, count=1, flags=re.S)
    if re.search(r'<meta\s+name="description"', h):
        h = re.sub(r'<meta\s+name="description"[^>]*?content="[^"]*"\s*/?>',
                   lambda m: '<meta name="description" content="%s" />' % d, h, count=1, flags=re.S)
    else:
        h = h.replace('<title>', '<meta name="description" content="%s" />\n    <title>' % d, 1)
    if re.search(r'<meta\s+name="robots"', h):
        h = re.sub(r'<meta\s+name="robots"[^>]*?content="[^"]*"\s*/?>',
                   '<meta name="robots" content="noindex, follow" />', h, count=1, flags=re.S)
    else:
        h = h.replace('<title>', '<meta name="robots" content="noindex, follow" />\n    <title>', 1)
    for tag, val in (('property="og:title"', t), ('property="og:description"', d),
                     ('name="twitter:title"', t), ('name="twitter:description"', d)):
        h = re.sub(r'<meta %s content="[^"]*"\s*/?>' % tag,
                   lambda m, v=val, g=tag: '<meta %s content="%s">' % (g, v), h, count=1)
    return h
