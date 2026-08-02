# -*- coding: utf-8 -*-
"""Siembra la base de datos de la plataforma XARU HOME.

Construye `platform/xaru.db` a partir del esquema canónico y la llena con:

  · el árbol geográfico completo (130 países, 293 ciudades)
  · taxonomías: tipologías residenciales, comerciales y de suelo, y amenidades
  · organizaciones de prueba: agencias, promotoras y la propia plataforma
  · agentes de prueba y compradores de prueba
  · inventario: los activos que ya existían + una cartera amplia por país,
    incluyendo suelo minero, terreno de escala urbana, islas y castillos
  · demanda: leads, favoritos, búsquedas guardadas y alertas
  · operación: casos de moderación, ledger de créditos y promociones

TODO el inventario sembrado aquí lleva `is_demo = 1` y una etiqueta visible.
No se borra nunca: cuando entre inventario real convivirán, y el filtro por
`is_demo` decide qué se publica. Esa es la vía para pasar de muestra a real
sin rehacer nada.

Uso:
    python3 platform/seed.py            # reconstruye xaru.db desde cero
"""
import json, os, random, sqlite3, sys, unicodedata
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from geo_world import WORLD  # noqa: E402
from geo_terrain import allowed as terrain_allows  # noqa: E402
from describe import describe  # noqa: E402

DB = os.path.join(HERE, "xaru.db")
SCHEMA = os.path.join(HERE, "schema.sql")
NOW = "2026-08-02T00:00:00Z"
RNG = random.Random(20260802)          # determinista: dos siembras iguales

DEMO_LABEL = "PLATFORM DEMO"



# Bandas coherentes por tipologia residencial: (dorm_min, dorm_max, m2_min, m2_max).
# Sin esto el sembrador producia aticos de un dormitorio a treinta millones y
# compounds de dos, que es exactamente lo que descalifica a un portal.
BEDROOM_BAND = {
    "apartment":         (1, 4, 65, 320),
    "duplex":            (2, 5, 130, 480),
    "penthouse":         (3, 6, 220, 900),
    "townhouse":         (3, 5, 150, 420),
    "bungalow":          (2, 4, 110, 300),
    "villa":             (4, 8, 320, 1600),
    "mansion":           (6, 12, 800, 3600),
    "compound":          (8, 20, 1200, 6000),
    "castle":            (10, 30, 1500, 8000),
    "estate":            (6, 14, 700, 4200),
    "hacienda":          (5, 12, 600, 3200),
    "equestrian":        (5, 10, 500, 2400),
    "branded-residence": (2, 5, 140, 620),
    "chalet":            (3, 7, 200, 900),
    "waterfront-home":   (3, 7, 250, 1100),
    "whole-floor":       (3, 8, 300, 1400),
    "half-floor":        (2, 5, 180, 700),
    "whole-building":    (10, 40, 1200, 9000),
}


# Tipologia de cada oportunidad. Su fichero de origen trae `model: residential`,
# que no distingue una isla de un atico: se declara aqui, activo por activo,
# porque son trece y porque son los que el cliente ya conoce por su nombre.
OPP_TYPE = {
    "pp-samana-island":          "private-island",
    "pp-villa-dubai":            "villa",
    "pp-penthouse-london":       "penthouse",
    "pp-villa-como":             "estate",
    "pp-casa-tulum":             "waterfront-home",
    "pp-villa-marbella":         "villa",
    "ch-hotel-operational":      "hotel",
    "ch-hotel-halted":           "halted-project",
    "ch-resort-development":     "resort",
    "lp-land-11m":               "masterplan-land",
    "lp-ashima-masterplan":      "masterplan-land",
    "cf-confidential-portfolio": "mixed-use",
    "pa-quarry-license":         "quarry",
}

# ---------------------------------------------------------------- utilidades
def uid(prefix, n):
    return "%s_%012d" % (prefix, n)


# Letras que la descomposicion Unicode no separa en base + acento: no llevan
# marca combinante, son caracteres propios. Sin esta tabla, "Sorensen" salia
# como "g-sorensen" en unos sitios y "g-s%C3%B8rensen" en otros, y el enlace
# se rompia.
_FOLD = {
    "\u00f8": "o", "\u00e6": "ae", "\u00df": "ss", "\u00f0": "d", "\u00fe": "th",
    "\u0142": "l", "\u0111": "d", "\u0127": "h", "\u0131": "i", "\u0153": "oe",
    "\u00e5": "a", "\u0119": "e", "\u0105": "a", "\u017c": "z", "\u017a": "z",
}

def slugify(s):
    s = "".join(_FOLD.get(c, c) for c in str(s).lower())
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    out = []
    for c in s:
        out.append(c if (c.isalnum() and c.isascii()) else "-")
    return "-".join(x for x in "".join(out).split("-") if x)


def pid(n, width=8):
    """public_id no secuencial: base36 de un hash estable."""
    h = (n * 2654435761) % (36 ** width)
    d = "0123456789abcdefghijklmnopqrstuvwxyz"
    out = ""
    while h:
        out = d[h % 36] + out
        h //= 36
    return out.rjust(width, "0")


def iso(days_ago):
    return (datetime(2026, 8, 2) - timedelta(days=days_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- taxonomías
RESIDENTIAL_TYPES = [
    ("apartment", "Apartment", "Apartamento", "شقة", "公寓"),
    ("villa", "Villa", "Villa", "فيلا", "别墅"),
    ("townhouse", "Townhouse", "Casa adosada", "تاون هاوس", "联排别墅"),
    ("penthouse", "Penthouse", "Penthouse", "بنتهاوس", "顶层公寓"),
    ("duplex", "Duplex", "Dúplex", "دوبلكس", "复式住宅"),
    ("compound", "Compound", "Complejo residencial", "مجمّع", "住宅园区"),
    ("whole-floor", "Whole floor", "Planta completa", "طابق كامل", "整层"),
    ("half-floor", "Half floor", "Media planta", "نصف طابق", "半层"),
    ("whole-building", "Whole building", "Edificio completo", "مبنى كامل", "整栋"),
    ("bungalow", "Bungalow", "Bungaló", "بنغل", "平层别墅"),
    ("mansion", "Mansion", "Mansión", "قصر", "豪宅"),
    ("castle", "Castle / Château", "Castillo / Château", "قلعة", "城堡"),
    ("estate", "Estate", "Finca", "حوزة", "庄园"),
    ("private-island", "Private island", "Isla privada", "جزيرة خاصة", "私人岛屿"),
    ("branded-residence", "Branded residence", "Residencia de marca", "مسكن بعلامة", "品牌住宅"),
    ("chalet", "Chalet", "Chalet", "شاليه", "雪山木屋"),
    ("waterfront-home", "Waterfront home", "Casa frente al agua", "منزل على الواجهة المائية", "滨水住宅"),
    ("equestrian", "Equestrian estate", "Finca ecuestre", "حوزة للخيول", "马术庄园"),
    ("hacienda", "Hacienda", "Hacienda", "هاسيندا", "庄园宅邸"),
]

COMMERCIAL_TYPES = [
    ("office", "Office", "Oficina", "مكتب", "写字楼"),
    ("retail", "Retail / Shop", "Local comercial", "متجر", "商铺"),
    ("showroom", "Showroom", "Showroom", "صالة عرض", "展厅"),
    ("warehouse", "Warehouse", "Almacén", "مستودع", "仓库"),
    ("factory", "Factory", "Fábrica", "مصنع", "厂房"),
    ("business-centre", "Business centre", "Centro de negocios", "مركز أعمال", "商务中心"),
    ("coworking", "Coworking", "Coworking", "عمل مشترك", "联合办公"),
    ("staff-accommodation", "Staff accommodation", "Alojamiento de personal", "سكن موظفين", "员工宿舍"),
    ("labour-camp", "Labour camp", "Campamento laboral", "سكن عمال", "劳工营地"),
    ("hotel", "Hotel / Aparthotel", "Hotel / Apartahotel", "فندق", "酒店"),
    ("resort", "Resort", "Resort", "منتجع", "度假村"),
    ("marina", "Marina & beach club", "Marina y club de playa", "مرسى", "码头"),
    ("mixed-use", "Mixed-use development", "Desarrollo de uso mixto", "تطوير متعدد الاستخدامات", "综合体"),
    ("entertainment", "Park & entertainment", "Parque y ocio", "ترفيه", "娱乐设施"),
    ("serviced-residence", "Serviced residence", "Aparthotel y residencia", "مسكن مخدوم", "服务式公寓"),
    ("halted-project", "Halted project", "Proyecto detenido", "مشروع متوقف", "停滞项目"),
]

LAND_TYPES = [
    ("residential-plot", "Residential plot", "Parcela residencial", "قطعة سكنية", "住宅地块"),
    ("commercial-plot", "Commercial plot", "Parcela comercial", "قطعة تجارية", "商业地块"),
    ("coastal-land", "Coastal land", "Suelo costero", "أرض ساحلية", "海岸土地"),
    ("island-territory", "Island territory", "Territorio insular", "إقليم جزري", "岛屿领地"),
    ("masterplan-land", "Master-plan land", "Suelo de plan maestro", "أرض مخطط عام", "总体规划用地"),
    ("agricultural-land", "Agricultural estate land", "Suelo agrícola", "أرض زراعية", "农业用地"),
    ("hotel-resort-land", "Hotel & resort land", "Suelo hotelero", "أرض فندقية", "酒店度假用地"),
    ("urban-mixed-land", "Urban mixed-use land", "Suelo urbano mixto", "أرض حضرية مختلطة", "城市综合用地"),
    ("mining-concession", "Mining concession", "Concesión minera", "امتياز تعديني", "采矿特许"),
    ("quarry", "Quarry & aggregates", "Cantera y áridos", "محجر", "采石场"),
    ("forestry-land", "Forestry land", "Suelo forestal", "أرض حرجية", "林地"),
    ("energy-land", "Energy & solar land", "Suelo energético", "أرض للطاقة", "能源用地"),
    ("city-scale-land", "City-scale territory", "Territorio de escala urbana", "إقليم بحجم مدينة", "城市级土地"),
]

AMENITIES = [
    ("central-ac", "climate", "Central air conditioning", "Aire acondicionado central", "تكييف مركزي", "中央空调"),
    ("maid-room", "space", "Maid's room", "Habitación de servicio", "غرفة خادمة", "佣人房"),
    ("balcony", "outdoor", "Balcony / terrace", "Balcón / terraza", "شرفة", "阳台露台"),
    ("shared-pool", "leisure", "Shared pool", "Piscina compartida", "مسبح مشترك", "共享泳池"),
    ("private-pool", "leisure", "Private pool", "Piscina privada", "مسبح خاص", "私人泳池"),
    ("shared-spa", "leisure", "Shared spa", "Spa compartido", "سبا مشترك", "共享水疗"),
    ("shared-gym", "leisure", "Shared gym", "Gimnasio compartido", "صالة رياضية مشتركة", "共享健身房"),
    ("private-gym", "leisure", "Private gym", "Gimnasio privado", "صالة رياضية خاصة", "私人健身房"),
    ("concierge", "service", "Concierge / reception", "Conserjería", "خدمة الاستقبال", "礼宾服务"),
    ("covered-parking", "parking", "Covered parking", "Estacionamiento cubierto", "موقف مغطى", "地下车位"),
    ("water-view", "view", "Water view", "Vista al agua", "إطلالة مائية", "水景"),
    ("skyline-view", "view", "Skyline view", "Vista al skyline", "إطلالة على الأفق", "天际线景观"),
    ("golf-view", "view", "Golf view / access", "Vista o acceso a golf", "إطلالة على الغولف", "高尔夫景观"),
    ("pets-allowed", "policy", "Pets allowed", "Mascotas permitidas", "يُسمح بالحيوانات", "允许养宠"),
    ("study", "space", "Study", "Estudio", "غرفة مكتب", "书房"),
    ("private-garden", "outdoor", "Private garden", "Jardín privado", "حديقة خاصة", "私人花园"),
    ("jacuzzi", "leisure", "Private jacuzzi", "Jacuzzi privado", "جاكوزي خاص", "私人按摩浴缸"),
    ("built-in-wardrobes", "space", "Built-in wardrobes", "Armarios empotrados", "خزائن مدمجة", "嵌入式衣柜"),
    ("walk-in-closet", "space", "Walk-in closet", "Vestidor", "غرفة ملابس", "步入式衣帽间"),
    ("built-in-appliances", "kitchen", "Built-in appliances", "Electrodomésticos empotrados", "أجهزة مدمجة", "嵌入式家电"),
    ("children-area", "family", "Children's play area", "Zona infantil", "منطقة أطفال", "儿童游乐区"),
    ("children-pool", "family", "Children's pool", "Piscina infantil", "مسبح أطفال", "儿童泳池"),
    ("bbq-area", "outdoor", "Barbecue area", "Zona de barbacoa", "منطقة شواء", "烧烤区"),
    ("security-24-7", "service", "24/7 security", "Seguridad 24/7", "أمن على مدار الساعة", "24小时安保"),
    ("lobby", "service", "Lobby", "Lobby", "بهو", "大堂"),
    ("elevator", "access", "Elevator", "Ascensor", "مصعد", "电梯"),
    ("accessible", "access", "Step-free access", "Accesibilidad sin escalones", "وصول ميسّر", "无障碍通行"),
    ("smart-home", "tech", "Smart home", "Domótica", "منزل ذكي", "智能家居"),
    ("beach-access", "location", "Beach access", "Acceso a playa", "وصول إلى الشاطئ", "海滩通道"),
    ("marina-access", "location", "Marina access", "Acceso a marina", "وصول إلى المرسى", "码头通道"),
    ("rooftop", "outdoor", "Rooftop", "Azotea", "سطح", "屋顶平台"),
    ("sauna", "leisure", "Sauna / steam room", "Sauna / baño de vapor", "ساونا", "桑拿蒸汽房"),
    ("business-lounge", "service", "Business lounge", "Sala de negocios", "صالة أعمال", "商务休息室"),
    ("ev-charging", "tech", "EV charging", "Carga de vehículo eléctrico", "شحن السيارات الكهربائية", "电动车充电"),
    ("storage", "space", "Storage", "Trastero", "مخزن", "储藏室"),
    ("laundry", "space", "Laundry area", "Zona de lavandería", "منطقة غسيل", "洗衣区"),
    ("generator", "utility", "Backup power", "Respaldo energético", "مولّد احتياطي", "备用电源"),
    ("community-park", "outdoor", "Community park", "Parque comunitario", "حديقة عامة", "社区公园"),
    ("sports-court", "leisure", "Sports court", "Cancha deportiva", "ملعب رياضي", "运动场"),
    ("metro-nearby", "location", "Transport nearby", "Transporte cercano", "مواصلات قريبة", "临近交通"),
    ("helipad", "service", "Helipad", "Helipuerto", "مهبط مروحيات", "直升机坪"),
    ("private-dock", "location", "Private dock", "Muelle privado", "رصيف خاص", "私人码头"),
    ("staff-quarters", "space", "Staff quarters", "Dependencias de servicio", "سكن العاملين", "佣人房区"),
    ("vineyard", "land", "Vineyard", "Viñedo", "كرم عنب", "葡萄园"),
    ("water-rights", "land", "Water rights", "Derechos de agua", "حقوق المياه", "水权"),
    ("road-access", "land", "Road access", "Acceso rodado", "وصول بالطريق", "道路通达"),
    ("grid-connection", "land", "Grid connection", "Conexión a red", "اتصال بالشبكة", "电网接入"),
    ("mineral-rights", "land", "Mineral rights", "Derechos mineros", "حقوق التعدين", "矿权"),
]

# Nivel de precio por país: multiplicador sobre la base de la tipología.
TIER = {
    "MC": 4.0, "CH": 3.0, "SG": 2.8, "HK": 2.8, "GB": 2.4, "US": 2.3, "AE": 2.2,
    "FR": 2.1, "IT": 1.9, "ES": 1.6, "PT": 1.5, "AU": 1.9, "JP": 1.9, "CA": 1.8,
    "DE": 1.8, "NL": 1.8, "IE": 1.7, "AT": 1.7, "BS": 2.4, "KY": 2.6, "BL": 3.2,
    "TC": 2.2, "VG": 2.2, "MV": 2.6, "PF": 2.2, "SC": 2.0, "MU": 1.4, "GR": 1.4,
    "HR": 1.3, "ME": 1.1, "TR": 1.0, "MX": 1.2, "CR": 1.2, "PA": 1.1, "DO": 1.1,
    "BR": 1.1, "AR": 0.9, "CL": 1.1, "UY": 1.2, "CO": 0.9, "PE": 0.8, "ZA": 0.9,
    "MA": 0.9, "TH": 1.1, "ID": 1.0, "MY": 0.9, "PH": 0.8, "VN": 0.8, "IN": 0.9,
    "CN": 1.7, "KR": 1.6, "QA": 1.9, "SA": 1.6, "OM": 1.2, "BH": 1.3, "KW": 1.5,
}

# Base de precio en USD por tipología (mediana antes del multiplicador de país)
BASE_PRICE = {
    "apartment": 1_400_000, "villa": 3_800_000, "townhouse": 1_900_000,
    "penthouse": 6_500_000, "duplex": 2_600_000, "compound": 9_500_000,
    "whole-floor": 7_500_000, "half-floor": 4_200_000, "whole-building": 22_000_000,
    "bungalow": 1_600_000, "mansion": 12_000_000, "castle": 18_000_000,
    "estate": 9_000_000, "private-island": 48_000_000, "branded-residence": 3_200_000,
    "chalet": 5_500_000, "waterfront-home": 6_800_000, "equestrian": 8_500_000,
    "hacienda": 5_200_000,
    "office": 4_500_000, "retail": 2_800_000, "showroom": 3_100_000,
    "warehouse": 5_400_000, "factory": 8_200_000, "business-centre": 16_000_000,
    "coworking": 6_100_000, "staff-accommodation": 7_300_000, "labour-camp": 5_900_000,
    "hotel": 52_000_000, "resort": 118_000_000, "marina": 64_000_000,
    "mixed-use": 145_000_000, "entertainment": 96_000_000, "serviced-residence": 41_000_000,
    "halted-project": 38_000_000,
    "residential-plot": 2_400_000, "commercial-plot": 5_600_000, "coastal-land": 34_000_000,
    "island-territory": 42_000_000, "masterplan-land": 96_000_000,
    "agricultural-land": 18_000_000, "hotel-resort-land": 46_000_000,
    "urban-mixed-land": 72_000_000, "mining-concession": 128_000_000,
    "quarry": 54_000_000, "forestry-land": 26_000_000, "energy-land": 38_000_000,
    "city-scale-land": 410_000_000,
}

# Familia de fotos por tipología: se reutiliza el banco ya licenciado.
PHOTO_FAMILY = {
    "apartment": ["pr-city-apartments", "pr-branded-residences"],
    "villa": ["pr-villas", "pr-contemporary-houses"],
    "townhouse": ["pr-contemporary-houses", "pr-city-apartments"],
    "penthouse": ["pr-penthouses"],
    "duplex": ["pr-branded-residences", "pr-penthouses"],
    "compound": ["pr-mansions", "pr-estates"],
    "whole-floor": ["pr-penthouses", "pr-city-apartments"],
    "half-floor": ["pr-city-apartments"],
    "whole-building": ["ch-mixed-use", "ch-serviced-residences"],
    "bungalow": ["pr-contemporary-houses", "pr-waterfront"],
    "mansion": ["pr-mansions"],
    "castle": ["pr-castles-chateaux"],
    "estate": ["pr-estates", "pr-haciendas"],
    "private-island": ["pr-private-islands", "ld-island-territories"],
    "branded-residence": ["pr-branded-residences"],
    "chalet": ["pr-villas-mountain", "pr-contemporary-houses-mountain"],
    "waterfront-home": ["pr-waterfront"],
    "equestrian": ["pr-equestrian"],
    "hacienda": ["pr-haciendas"],
    "office": ["ch-mixed-use", "ch-serviced-residences"],
    "retail": ["ch-mixed-use"],
    "showroom": ["ch-mixed-use"],
    "warehouse": ["ld-masterplan", "ch-mixed-use"],
    "factory": ["ld-masterplan", "ch-mixed-use"],
    "business-centre": ["ch-mixed-use"],
    "coworking": ["ch-mixed-use"],
    "staff-accommodation": ["ch-serviced-residences"],
    "labour-camp": ["ch-serviced-residences"],
    "hotel": ["ch-operating-hotels", "ch-boutique-hotels"],
    "resort": ["ch-resorts"],
    "marina": ["ch-marinas-beach-clubs"],
    "mixed-use": ["ch-mixed-use"],
    "entertainment": ["ch-parks-entertainment"],
    "serviced-residence": ["ch-serviced-residences"],
    "halted-project": ["ch-halted-projects"],
    "residential-plot": ["ld-urban-mixed-land", "ld-coastal-land"],
    "commercial-plot": ["ld-urban-mixed-land"],
    "coastal-land": ["ld-coastal-land"],
    "island-territory": ["ld-island-territories"],
    "masterplan-land": ["ld-masterplan-land"],
    "agricultural-land": ["ld-agricultural-estate-land"],
    "hotel-resort-land": ["ld-hotel-resort-land"],
    "urban-mixed-land": ["ld-urban-mixed-land"],
    "mining-concession": ["ld-masterplan-land", "ld-agricultural-estate-land"],
    "quarry": ["ld-hotel-resort-land", "ld-masterplan-land"],
    "forestry-land": ["ld-agricultural-estate-land"],
    "energy-land": ["ld-masterplan-land"],
    "city-scale-land": ["ld-masterplan-land", "ld-urban-mixed-land"],
}

AGENCIES = [
    ("XARU Select", "AE", "Dubai", "select"),
    ("XARU Mediterranean", "ES", "Marbella", "mediterranean"),
    ("XARU Americas", "US", "Miami", "americas"),
    ("XARU Asia Pacific", "SG", "Singapore", "asia-pacific"),
    ("XARU Land & Resources", "PA", "Panama City", "land-resources"),
    ("XARU Hospitality Partners", "GR", "Athens", "hospitality-partners"),
]

DEVELOPERS = [
    ("Ashima Development Group", "MX", 2011),
    ("Meridian Coastal Developments", "AE", 2006),
    ("Northlight Urban", "GB", 1998),
    ("Terra Andina Desarrollos", "CL", 2014),
    ("Sable Bay Resorts", "MU", 2009),
]

AGENT_NAMES = [
    "A. Reyes", "M. Haddad", "L. Ferrer", "J. Okonkwo", "S. Lindqvist", "R. Mehta",
    "C. Duarte", "N. Yamamoto", "P. Novak", "T. Alves", "K. Brennan", "D. Moreau",
    "F. Castellanos", "H. Al-Mansouri", "I. Petrova", "O. Adeyemi", "V. Rossi",
    "B. Chen", "G. Sørensen", "E. Marchetti", "Y. Kaya", "Z. Nkosi",
]

BUYER_NAMES = [
    "Comprador de prueba 01", "Comprador de prueba 02", "Comprador de prueba 03",
    "Comprador de prueba 04", "Comprador de prueba 05", "Comprador de prueba 06",
    "Comprador de prueba 07", "Comprador de prueba 08", "Comprador de prueba 09",
    "Comprador de prueba 10", "Comprador de prueba 11", "Comprador de prueba 12",
]


# ---------------------------------------------------------------- banco de fotos
def photo_pool():
    """Agrupa las fotos ya licenciadas por prefijo de subcategoría."""
    d = os.path.join(ROOT, "assets", "img", "xaru", "catalog")
    pool = {}
    for f in sorted(os.listdir(d)):
        if not f.endswith(".jpg"):
            continue
        base = f[:-4]
        pool.setdefault(base, []).append("assets/img/xaru/catalog/" + f)
    return pool


def pick_photo(pool, families, n):
    return pick_gallery(pool, families, n, 1)[0]


def pick_gallery(pool, families, n, k):
    """k fotos distintas de la misma familia, empezando en un punto estable.

    Una ficha con una sola foto no es una ficha: el comprador quiere recorrer
    la casa. Todas salen del mismo banco licenciado y de la misma familia
    tipologica, asi que la galeria es coherente con lo que anuncia el titulo.
    """
    cands = []
    for fam in families:
        cands += [v[0] for key, v in pool.items() if key.startswith(fam)]
    if not cands:
        cands = [v[0] for v in pool.values()]
    k = max(1, min(k, len(cands)))
    start = n % len(cands)
    return [cands[(start + i) % len(cands)] for i in range(k)]


# ---------------------------------------------------------------- inventario heredado
def import_existing(cur, loc_of_city, org_ids, agent_ids, media_id_for, listings,
                    pool_ref=None):
    """Importa lo que ya existía en el sitio: los 156 activos del catálogo y las
    13 oportunidades. Nada se pierde. Los seis activos `pp-` vuelven a estar
    publicados como inventario de muestra de la plataforma — que es lo que son —
    en lugar de retirados.
    """
    n = 0
    packs = ["private-real-estate", "commercial-hospitality", "land-developments"]
    fam = {"private-real-estate": "residential", "commercial-hospitality": "commercial",
           "land-developments": "land"}
    pool_ref = pool_ref or [photo_pool()]
    subtype_pt = {}
    for row in cur.execute("SELECT id, slug FROM property_types").fetchall():
        subtype_pt[row[1]] = row[0]
    # Nombre de la tipologia en los cuatro idiomas, indexado por id, para poder
    # componer la descripcion de lo que se importa.
    type_names = {r[0]: {"en": r[1], "es": r[2], "ar": r[3], "zh": r[4]} for r in cur.execute(
        "SELECT id, name_en, name_es, name_ar, name_zh FROM property_types")}

    def type_for(group, sub):
        guess = {
            "villas": "villa", "mansions": "mansion", "castles-chateaux": "castle",
            "estates": "estate", "penthouses": "penthouse", "city-apartments": "apartment",
            "branded-residences": "branded-residence", "private-islands": "private-island",
            "waterfront": "waterfront-home", "contemporary-houses": "villa",
            "equestrian": "equestrian", "haciendas": "hacienda",
            "operating-hotels": "hotel", "boutique-hotels": "hotel", "resorts": "resort",
            "marinas-beach-clubs": "marina", "mixed-use": "mixed-use",
            "parks-entertainment": "entertainment", "serviced-residences": "serviced-residence",
            "halted-projects": "halted-project",
            "coastal-land": "coastal-land", "island-territories": "island-territory",
            "masterplan-land": "masterplan-land", "agricultural-estate-land": "agricultural-land",
            "hotel-resort-land": "hotel-resort-land", "urban-mixed-land": "urban-mixed-land",
        }.get(sub)
        if guess and ("pt_" + guess) in subtype_pt.values():
            return "pt_" + guess
        return "pt_" + ("villa" if group == "residential" else
                        "mixed-use" if group == "commercial" else "masterplan-land")

    for pack in packs:
        path = os.path.join(ROOT, "data", "properties", pack + ".json")
        if not os.path.exists(path):
            continue
        d = json.load(open(path, encoding="utf-8"))
        group = fam[pack]
        for a in d["items"]:
            n += 1
            cc = None
            for code, meta in WORLD.items():
                if meta[0] == a.get("country"):
                    cc = code
                    break
            city = a.get("city") or "—"
            key = (cc, city)
            if key not in loc_of_city:
                # la ciudad del activo heredado no estaba en el árbol: se añade
                if cc is None:
                    cc = "AE"
                parent = "loc_" + cc.lower()
                cid = "loc_" + cc.lower() + "_" + slugify(city)
                try:
                    cur.execute("INSERT INTO locations VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                (cid, parent, "city", slugify(city), city, city, city, city,
                                 cc, None, None, slugify(WORLD[cc][0]) + "/" + slugify(city), 0))
                except sqlite3.IntegrityError:
                    pass
                loc_of_city[key] = (cid, WORLD[cc][5][0][1], WORLD[cc][5][0][2], WORLD[cc][4])
            lid_city, clat, clon, _ = loc_of_city[key]
            lid = "lst_legacy_" + a["id"]
            mid = media_id_for(a["hero_image"])
            price = a.get("price_usd") or 0
            built = a.get("built_area_sqm")
            lc = a.get("language_content") or {}
            cur.execute("""INSERT INTO listings (id, public_id, tenant_id, org_id, agent_id,
                external_reference, source_system, business_category, offering_type,
                inventory_type, property_type_id, subtype, location_id, country_code,
                city, latitude, longitude, location_precision, public_display_address,
                bedrooms, bathrooms, built_area_sqm, plot_area_sqm, hectares, hotel_keys,
                berths, currency, price_minor, price_on_application, price_per_sqm_minor,
                furnishing, completion_status, ownership_type, verification_status,
                lifecycle_status, moderation_status, quality_score, promotion_tier,
                hero_media_id, published_at, updated_at, is_demo, demo_label, created_at)
                VALUES (%s)""" % ",".join(["?"] * 44),
                (lid, pid(90000 + n), "tn_xaru", org_ids[n % len(org_ids)],
                 agent_ids[n % len(agent_ids)], a["id"], "migration", group, "sale",
                 "ready", type_for(group, a.get("subcategory", "")), a.get("subcategory"),
                 lid_city, cc, city, clat, clon, "community",
                 ", ".join(x for x in (a.get("city"), a.get("country")) if x),
                 a.get("bedrooms"), a.get("bathrooms"), built, a.get("land_area_m2"),
                 a.get("hectares"), a.get("hotel_keys"), a.get("berths"),
                 "USD", price * 100 if price else None, 0 if price else 1,
                 int(price * 100 / built) if (price and built) else None,
                 "unknown", "ready", "freehold", "verified",
                 "PUBLISHED", "approved", 84, "none", mid, NOW, NOW, 1, DEMO_LABEL, NOW))
            gal = [g for g in (a.get("gallery") or []) if isinstance(g, str)]
            if len(gal) < 4:
                # La galeria venia vacia en el catalogo heredado. Se completa con
                # fotos de la misma subcategoria, que es de donde salio la de
                # portada, manteniendo esa como primera.
                # `fam` ya nombra el mapa pack->grupo en esta funcion.
                fams = [a["id"].rsplit("-", 1)[0], a.get("subcategory") or ""]
                extra = pick_gallery(pool_ref[0], [f for f in fams if f], n, 8)
                gal = [a["hero_image"]] + [g for g in extra if g != a["hero_image"]]
            gal = gal[:9]
            for gi, gp in enumerate(gal[:9]):
                cur.execute("INSERT OR IGNORE INTO listing_media VALUES (?,?,?,?)",
                            (lid, media_id_for(gp), gi, 1 if gi == 0 else 0))
            for loc in ("en", "es", "ar", "zh"):
                ttl = a.get("title") or a["id"]
                cur.execute("INSERT INTO listing_translations VALUES (?,?,?,?,?,?,?)",
                            (lid, loc, ttl, (a.get("long_description") or {}).get(loc), None,
                             slugify(ttl) + "-" + pid(90000 + n)[:6], "human"))
            listings.append(lid)
            cur.execute("UPDATE locations SET listing_count = listing_count + 1 WHERE id IN (?,?)",
                        (lid_city, "loc_" + cc.lower()))

    # ---- las 13 oportunidades, incluidos los seis pp-* que se habían retirado
    opp_path = os.path.join(ROOT, "data", "opportunities.json")
    if os.path.exists(opp_path):
        od = json.load(open(opp_path, encoding="utf-8"))
        for o in od["opportunities"]:
            n += 1
            cc = None
            country = (o.get("location") or {}).get("country")
            for code, meta in WORLD.items():
                if meta[0] == country:
                    cc = code
                    break
            cc = cc or "AE"
            city = (o.get("location") or {}).get("city") or WORLD[cc][5][0][0]
            key = (cc, city)
            if key not in loc_of_city:
                cid = "loc_" + cc.lower() + "_" + slugify(city)
                try:
                    cur.execute("INSERT INTO locations VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                (cid, "loc_" + cc.lower(), "city", slugify(city), city, city,
                                 city, city, cc, None, None,
                                 slugify(WORLD[cc][0]) + "/" + slugify(city), 0))
                except sqlite3.IntegrityError:
                    pass
                loc_of_city[key] = (cid, WORLD[cc][5][0][1], WORLD[cc][5][0][2], WORLD[cc][4])
            lid_city, clat, clon, _ = loc_of_city[key]
            lid = "lst_opp_" + o["id"]
            mid = media_id_for(o["images"][0])
            sp = o.get("specs") or {}
            group = {"private-properties": "residential",
                     "commercial-hospitality": "commercial"}.get(o["catalog"], "land")
            opp_slug = OPP_TYPE.get(o["id"])
            opp_pt = subtype_pt.get(opp_slug) or type_for(group, "")
            if opp_pt and not str(opp_pt).startswith("pt_"):
                opp_pt = "pt_" + opp_slug
            cur.execute("""INSERT INTO listings (id, public_id, tenant_id, org_id, agent_id,
                external_reference, source_system, business_category, offering_type,
                inventory_type, property_type_id, subtype, location_id, country_code, city,
                latitude, longitude, location_precision, public_display_address, bedrooms,
                bathrooms, built_area_sqm, plot_area_sqm, currency, price_minor,
                price_on_application, verification_status, lifecycle_status,
                moderation_status, quality_score, promotion_tier, hero_media_id,
                published_at, updated_at, is_demo, demo_label, created_at)
                VALUES (%s)""" % ",".join(["?"] * 37),
                (lid, pid(95000 + n), "tn_xaru", org_ids[n % len(org_ids)],
                 agent_ids[n % len(agent_ids)], o["id"], "migration", group, "sale", "ready",
                 opp_pt, opp_slug, lid_city, cc, city, clat, clon,
                 "community", ", ".join(x for x in (city, country) if x),
                 sp.get("bedrooms"), sp.get("bathrooms"), sp.get("builtAreaSqm"),
                 sp.get("plotAreaSqm"), ((o.get("price") or {}).get("currency") or "USD"),
                 None, 1, "verified", "PUBLISHED", "approved", 88, "featured", mid,
                 NOW, NOW, 1, DEMO_LABEL, NOW))
            # Las trece oportunidades traen una sola imagen. Son las primeras
            # que ve cualquiera que entre por "comprar", asi que su galeria se
            # completa con fotos de su misma tipologia, igual que el resto.
            ogal = [g for g in (o.get("images") or []) if isinstance(g, str)]
            if len(ogal) < 4 and ogal:
                fams_o = PHOTO_FAMILY.get(opp_slug) or [o["catalog"]]
                oextra = pick_gallery(pool_ref[0], fams_o, n, 8)
                ogal = [ogal[0]] + [g for g in oextra if g not in ogal]
            for gi, gp in enumerate(ogal[:8]):
                cur.execute("INSERT OR IGNORE INTO listing_media VALUES (?,?,?,?)",
                            (lid, media_id_for(gp), gi, 1 if gi == 0 else 0))
            if n % 3 == 0:
                cur.execute("INSERT OR IGNORE INTO listing_media VALUES (?,?,?,?)",
                            (lid, media_id_for(ogal[0], kind="floorplan"), 90, 0))
            # Las oportunidades no traen texto largo en su fichero de origen.
            # Se compone con los mismos datos de la fila, igual que el resto del
            # inventario: nada inventado, ninguna ficha sin descripcion.
            tnames = type_names.get(opp_pt, {})
            for loc in ("en", "es", "ar", "zh"):
                ttl = (o.get("title") or {}).get(loc) or (o.get("title") or {}).get("en") or o["id"]
                body = describe(
                    loc, type_name=tnames.get(loc) or o.get("model") or "",
                    city=city, country=(WORLD[cc][{"en": 0, "es": 1, "ar": 2, "zh": 3}[loc]]),
                    bedrooms=sp.get("bedrooms"), bathrooms=sp.get("bathrooms"),
                    built=sp.get("builtAreaSqm"), plot=sp.get("plotAreaSqm"),
                    hectares=sp.get("hectares"), keys=sp.get("hotelKeys"),
                    completion="ready", verified=True, is_demo=True)
                cur.execute("INSERT INTO listing_translations VALUES (?,?,?,?,?,?,?)",
                            (lid, loc, ttl, body, None,
                             slugify(ttl) + "-" + pid(95000 + n)[:6], "human"))
            listings.append(lid)
            cur.execute("UPDATE locations SET listing_count = listing_count + 1 WHERE id IN (?,?)",
                        (lid_city, "loc_" + cc.lower()))
    return n


# ---------------------------------------------------------------- construcción
def main():
    if os.path.exists(DB):
        os.remove(DB)
    con = sqlite3.connect(DB)
    con.executescript(open(SCHEMA, encoding="utf-8").read())
    cur = con.cursor()

    # ---- tenant y plataforma
    cur.execute("INSERT INTO tenants VALUES (?,?,?,?,?)",
                ("tn_xaru", "XARU HOME", "AE", "eu", NOW))

    # ---- taxonomías
    order = 0
    for group, rows in (("residential", RESIDENTIAL_TYPES),
                        ("commercial", COMMERCIAL_TYPES),
                        ("land", LAND_TYPES)):
        for slug, en, es, ar, zh in rows:
            order += 1
            cur.execute("INSERT INTO property_types VALUES (?,?,?,?,?,?,?,?,?)",
                        ("pt_" + slug, group, slug, en, es, ar, zh, order, 1))
    for i, (slug, cat, en, es, ar, zh) in enumerate(AMENITIES):
        cur.execute("INSERT INTO amenities VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    ("am_" + slug, slug, cat, en, es, ar, zh, slug, "residential,commercial,land", i, 1))

    # ---- geografía
    loc_of_city = {}
    n = 0
    for cc, (en, es, ar, zh, region, cities) in WORLD.items():
        n += 1
        country_id = "loc_" + cc.lower()
        cur.execute("INSERT INTO locations VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (country_id, None, "country", slugify(en), en, es, ar, zh, cc,
                     None, None, slugify(en), 0))
        for city, lat, lon in cities:
            n += 1
            cid = "loc_" + cc.lower() + "_" + slugify(city)
            cur.execute("INSERT INTO locations VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (cid, country_id, "city", slugify(city), city, city, city, city,
                         cc, lat, lon, slugify(en) + "/" + slugify(city), 0))
            loc_of_city[(cc, city)] = (cid, lat, lon, region)

    # ---- organizaciones, agentes y compradores
    org_ids = []
    for i, (name, cc, city, slug) in enumerate(AGENCIES):
        oid = uid("org", i + 1)
        org_ids.append(oid)
        cur.execute("""INSERT INTO organizations (id,tenant_id,public_id,kind,legal_name,
                       trade_name,slug,logo_media_id,description,country_code,city,website,
                       phone,email,licence_number,licence_expires_at,verification_status,
                       plan_code,listing_quota,is_demo,created_at)
                          VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (oid, "tn_xaru", pid(i + 1), "agency", name + " FZ-LLC", name, slug, None,
                     "Demo agency of the XARU HOME platform. Test record, not a trading entity.",
                     cc, city, "https://xaruhome.com", None, "partners@xaruhome.com",
                     "DEMO-LIC-%04d" % (i + 1), "2027-12-31", "verified", "professional",
                     500, 1, NOW))
        cur.execute("INSERT INTO branches VALUES (?,?,?,?,?,?,?)",
                    (uid("br", i + 1), "tn_xaru", oid, name + " — HQ", city, cc, 1))

    dev_ids = []
    for i, (name, cc, year) in enumerate(DEVELOPERS):
        oid = uid("org", 100 + i)
        cur.execute("""INSERT INTO organizations (id,tenant_id,public_id,kind,legal_name,
                       trade_name,slug,logo_media_id,description,country_code,city,website,
                       phone,email,licence_number,licence_expires_at,verification_status,
                       plan_code,listing_quota,is_demo,created_at)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (oid, "tn_xaru", pid(100 + i), "developer", name + " S.A.", name,
                     slugify(name), None, "Demo developer record of the XARU HOME platform.",
                     cc, None, None, None, None, "DEMO-DEV-%04d" % i, "2028-06-30",
                     "verified", "developer", 200, 1, NOW))
        did = uid("dev", i + 1)
        dev_ids.append(did)
        cur.execute("""INSERT INTO developers (id,org_id,public_id,slug,name,country_code,
                       founded_year,description,logo_media_id,verification_status,is_demo)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                    (did, oid, pid(200 + i), slugify(name), name, cc, year,
                     "Demo developer. Projects shown are platform test inventory.", None,
                     "verified", 1))

    agent_ids = []
    for i, nm in enumerate(AGENT_NAMES):
        uidx = uid("usr", i + 1)
        oid = org_ids[i % len(org_ids)]
        cur.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (uidx, pid(300 + i), "agent%02d@demo.xaruhome.com" % (i + 1), nm,
                     ["en", "es", "ar", "zh"][i % 4], None, "agent", "tn_xaru", oid, 1, 1, NOW, NOW))
        aid = uid("agt", i + 1)
        agent_ids.append(aid)
        cur.execute("""INSERT INTO agents (id,tenant_id,user_id,org_id,branch_id,public_id,slug,
                       display_name,job_title,bio,photo_media_id,languages,specialities,
                       service_areas,licence_number,licence_expires_at,verification_status,
                       phone,whatsapp,email,response_minutes_p50,rating_avg,rating_count,
                       status,is_demo,created_at)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (aid, "tn_xaru", uidx, oid, uid("br", (i % len(AGENCIES)) + 1),
                     pid(400 + i), slugify(nm) + "-" + pid(400 + i)[:4], nm,
                     "Advisor", "Demo agent profile of the XARU HOME platform.", None,
                     ",".join(["en", "es", "ar", "zh"][: 2 + (i % 3)]),
                     "", "", "DEMO-AG-%04d" % i, "2027-06-30", "verified",
                     None, None, "advisor%02d@demo.xaruhome.com" % (i + 1),
                     None, None, 0, "active", 1, NOW))

    buyer_ids = []
    for i, nm in enumerate(BUYER_NAMES):
        bid = uid("usr", 900 + i)
        buyer_ids.append(bid)
        cur.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (bid, pid(900 + i), "buyer%02d@demo.xaruhome.com" % (i + 1), nm,
                     ["es", "en", "ar", "zh"][i % 4], None, "buyer", None, None, 0, 1, NOW, NOW))

    # ---- inventario
    pool = photo_pool()
    media_seen = {}

    def media_id_for(path, kind="photo"):
        """Un id de medio por (fichero, tipo). El plano y el recorrido apuntan
        al mismo archivo que la foto: lo que se declara es que el activo tiene
        plano y tour, no un render distinto que no existe."""
        key = (path, kind)
        if key not in media_seen:
            mid = uid("med", len(media_seen) + 1)
            media_seen[key] = mid
            cur.execute("INSERT INTO media VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                        (mid, "tn_xaru", kind, path, None, None, None, None,
                         "licensed_stock", "approved", NOW))
        return media_seen[key]

    all_types = ([("residential", t) for t in RESIDENTIAL_TYPES]
                 + [("commercial", t) for t in COMMERCIAL_TYPES]
                 + [("land", t) for t in LAND_TYPES])

    counter = 0
    listings = []
    for cc, (en, es, ar, zh, region, cities) in WORLD.items():
        tier = TIER.get(cc, 0.85)
        # Mercados grandes reciben más inventario; ninguno se queda vacío.
        per_city = 4 if tier >= 2.0 else (3 if tier >= 1.3 else 2)
        for city, lat, lon in cities:
            lid_city, clat, clon, creg = loc_of_city[(cc, city)]
            for k in range(per_city):
                counter += 1
                # La tipologia tiene que ser posible en esta plaza. Se avanza
                # por la lista hasta dar con una que el territorio admita: una
                # isla privada solo cae en costa, un chalet solo en montaña, y
                # una planta entera de oficinas solo en una plaza con peso.
                idx = (counter * 7) % len(all_types)
                for _step in range(len(all_types)):
                    group, ty = all_types[(idx + _step) % len(all_types)]
                    if terrain_allows(cc, city, ty[0], tier, region):
                        break
                (tslug, ten, tes, tar, tzh) = ty
                offering = "rent" if (counter % 9 == 0) else "sale"
                if group == "land":
                    offering = "sale"
                base = BASE_PRICE[tslug] * tier
                jitter = 0.55 + ((counter * 37) % 90) / 100.0
                price = int(base * jitter)
                if offering == "rent":
                    price = max(24_000, int(price * 0.045))
                poa = 1 if (counter % 23 == 0) else 0
                beds = baths = None
                built = plot = hect = keys = berths = None
                if group == "residential":
                    # Dormitorios, banos y superficie coherentes con la
                    # tipologia. Una isla privada no se describe por
                    # dormitorios, y una mansion de 27 millones no tiene dos.
                    if tslug == "private-island":
                        built = None
                        hect = round(4 + (counter * 11) % 900, 1)
                    else:
                        lo, hi, amin, amax = BEDROOM_BAND.get(tslug, (2, 5, 110, 480))
                        # El contador avanza con paso fijo por tipologia, asi
                        # que un modulo directo daba el mismo valor a todos los
                        # activos del mismo tipo. Se mezcla antes de repartir.
                        h = (counter * 2654435761) % (1 << 32)
                        beds = lo + (h >> 7) % max(1, hi - lo + 1)
                        baths = max(1, min(beds, (beds + 1) - ((h >> 3) % 2)))
                        built = amin + (h >> 11) % max(1, amax - amin)
                        if tslug in ("villa", "mansion", "estate", "castle",
                                     "hacienda", "equestrian", "compound"):
                            plot = built * (4 + counter % 12)
                elif group == "commercial":
                    built = 400 + (counter * 91) % 24000
                    if tslug in ("hotel", "resort", "serviced-residence"):
                        keys = 40 + (counter * 13) % 380
                    if tslug == "marina":
                        berths = 60 + (counter * 7) % 300
                else:
                    hect = round(5 + (counter * 17) % 4800, 1)
                    if tslug == "city-scale-land":
                        hect = round(1200 + (counter * 29) % 9000, 1)
                    if tslug in ("mining-concession", "quarry"):
                        hect = round(80 + (counter * 23) % 2600, 1)

                lid = uid("lst", counter)
                photo = pick_photo(pool, PHOTO_FAMILY[tslug], counter)
                mid = media_id_for(photo)
                title_en = "%s in %s" % (ten, city)
                price_per = None
                if price and built:
                    price_per = int(price * 100 / built)

                cur.execute("""INSERT INTO listings (
                    id, public_id, tenant_id, org_id, branch_id, agent_id, project_id, unit_type_id,
                    external_reference, source_system, version, business_category, offering_type,
                    inventory_type, property_type_id, subtype, location_id, country_code,
                    admin_area_1, city, district, community, building_name, unit_number_private,
                    street_address_private, latitude, longitude, location_precision,
                    public_display_address, bedrooms, bedroom_label, bathrooms, maid_rooms,
                    study_rooms, parking_spaces, floor_number, total_building_floors,
                    built_area_sqm, plot_area_sqm, hectares, hotel_keys, berths,
                    currency, price_minor, price_on_application, rent_frequency,
                    service_charge_minor, price_per_sqm_minor, negotiable, financing_available,
                    available_from, occupancy_status, furnishing, condition, completion_status,
                    handover_quarter, handover_year, ownership_type, regulatory_jurisdiction,
                    permit_number, verification_status, verification_expires_at,
                    lifecycle_status, moderation_status, quality_score, promotion_tier,
                    hero_media_id, published_at, updated_at, expires_at, sold_at, rented_at,
                    archived_at, created_by, updated_by, suspension_reason_code,
                    is_demo, demo_label, created_at)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (lid, pid(1000 + counter), "tn_xaru", org_ids[counter % len(org_ids)],
                     uid("br", (counter % len(AGENCIES)) + 1), agent_ids[counter % len(agent_ids)],
                     None, None, "XH-%06d" % counter, "migration", 1,
                     group, offering,
                     "off_plan_first_sale" if counter % 11 == 0 else "ready",
                     "pt_" + tslug, tslug, lid_city, cc,
                     None, city, None, None, None, None, None,
                     round(clat + ((counter % 17) - 8) * 0.004, 6),
                     round(clon + ((counter % 13) - 6) * 0.004, 6),
                     "community", "%s, %s" % (city, en),
                     beds, None, baths, None, None,
                     (counter % 4) if group == "residential" else None,
                     None, None, built, plot, hect, keys, berths,
                     "USD", None if poa else price * 100, poa,
                     "yearly" if offering == "rent" else None,
                     None, price_per, counter % 5 == 0, counter % 7 == 0,
                     None, "vacant",
                     ["furnished", "unfurnished", "partly_furnished"][
                         ((counter * 2654435761) % (1 << 32) >> 9) % 3],
                     "excellent",
                     "off_plan" if counter % 11 == 0 else "ready",
                     (counter % 4) + 1 if counter % 11 == 0 else None,
                     2027 + (counter % 3) if counter % 11 == 0 else None,
                     "freehold", cc, "DEMO-PRM-%06d" % counter,
                     "verified" if counter % 3 else "unverified", "2027-12-31",
                     "PUBLISHED", "approved", 62 + (counter * 13) % 38,
                     "featured" if counter % 19 == 0 else ("premium" if counter % 37 == 0 else "none"),
                     mid, iso(counter % 240), iso(counter % 60), None, None, None, None,
                     "seed", "seed", None, 1, DEMO_LABEL, NOW))

                # Galeria: entre cuatro y nueve fotos por activo. Y en una parte
                # del inventario, plano de planta y recorrido 360: son dos de las
                # senales que mas pesan cuando alguien compara dos anuncios.
                gal = pick_gallery(pool, PHOTO_FAMILY[tslug], counter, 4 + counter % 6)
                for gi, gp in enumerate(gal):
                    cur.execute("INSERT OR IGNORE INTO listing_media VALUES (?,?,?,?)",
                                (lid, media_id_for(gp), gi, 1 if gi == 0 else 0))
                hm = (counter * 2654435761) % (1 << 32)
                if (hm >> 5) % 100 < 27:
                    cur.execute("INSERT OR IGNORE INTO listing_media VALUES (?,?,?,?)",
                                (lid, media_id_for(gal[0], kind="floorplan"), 90, 0))
                if (hm >> 13) % 100 < 16:
                    cur.execute("INSERT OR IGNORE INTO listing_media VALUES (?,?,?,?)",
                                (lid, media_id_for(gal[-1], kind="tour360"), 91, 0))

                # Historial de precio: una parte del inventario lleva una bajada
                # real registrada. Es lo que permite decir "ha bajado un 8%" sin
                # inventarlo en el momento de pintar.
                if price and not poa and ((counter * 2654435761) % (1 << 32) >> 19) % 100 < 12:
                    was = int(price * (1.06 + (counter % 9) / 100.0))
                    cur.execute("INSERT INTO listing_price_history VALUES (?,?,?,?,?,?)",
                                (uid("pph", counter), lid, "USD", was * 100,
                                 iso(30 + counter % 90), "agent"))
                    cur.execute("INSERT INTO listing_price_history VALUES (?,?,?,?,?,?)",
                                (uid("ppn", counter), lid, "USD", price * 100,
                                 iso(counter % 25), "agent"))

                # Amenidades primero: la descripción las menciona por familia.
                am_slugs, am_cats = [], []
                for a in range(3 + counter % 5):
                    row = AMENITIES[(counter * (a + 3)) % len(AMENITIES)]
                    if row[0] in am_slugs:
                        continue
                    am_slugs.append(row[0])
                    if row[1] not in am_cats:
                        am_cats.append(row[1])
                    cur.execute("INSERT OR IGNORE INTO listing_amenities VALUES (?,?)",
                                (lid, "am_" + row[0]))

                is_off = counter % 11 == 0
                name_by_loc = {"en": (ten, en, title_en),
                               "es": (tes, es, "%s en %s" % (tes, city)),
                               "ar": (tar, ar, "%s في %s" % (tar, city)),
                               "zh": (tzh, zh, "%s · %s" % (tzh, city))}
                for loc in ("en", "es", "ar", "zh"):
                    tname, cname, ttl = name_by_loc[loc]
                    body = describe(
                        loc, type_name=tname, city=city, country=cname,
                        bedrooms=beds, bathrooms=baths, built=built, plot=plot,
                        hectares=hect, keys=keys, berths=berths,
                        completion="off_plan" if is_off else "ready",
                        handover_q=((counter % 4) + 1) if is_off else None,
                        handover_y=(2027 + (counter % 3)) if is_off else None,
                        ownership="freehold", cc=cname,
                        amenity_categories=am_cats,
                        verified=bool(counter % 3), is_demo=True)
                    cur.execute("INSERT INTO listing_translations VALUES (?,?,?,?,?,?,?)",
                                (lid, loc, ttl, body, None,
                                 slugify(ttl) + "-" + pid(1000 + counter)[:6], "human"))
                cur.execute("INSERT INTO listing_transitions VALUES (?,?,?,?,?,?,?,?,?)",
                            (uid("trn", counter), lid, "APPROVED", "PUBLISHED", "seed",
                             "SEED_PUBLISH", "Inventario de muestra de la plataforma",
                             iso(counter % 240), uid("cor", counter)))
                cur.execute("INSERT INTO outbox_events VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                            (uid("evt", counter), "listing.published.v1", lid, "listing", 1,
                             "tn_xaru", iso(counter % 240), "listings-service",
                             uid("cor", counter), None, 1,
                             json.dumps({"publicId": pid(1000 + counter), "isDemo": True}), None))
                listings.append(lid)
                cur.execute("UPDATE locations SET listing_count = listing_count + 1 WHERE id IN (?,?)",
                            (lid_city, "loc_" + cc.lower()))

    # ---- inventario que ya existía en el sitio: no se pierde nada
    legacy = import_existing(cur, loc_of_city, org_ids, agent_ids, media_id_for, listings,
                             pool_ref=[pool])

    # ---- proyectos off-plan
    for i, did in enumerate(dev_ids):
        cc = DEVELOPERS[i][1]
        city = WORLD[cc][5][0][0]
        lid_city = loc_of_city[(cc, city)][0]
        prj = uid("prj", i + 1)
        cur.execute("""INSERT INTO projects (id,tenant_id,developer_id,public_id,slug,name,
                       location_id,status,launch_date,handover_quarter,handover_year,
                       construction_progress_percent,progress_source,progress_updated_at,
                       price_min_minor,price_max_minor,currency,units_total,units_available,
                       description,hero_media_id,is_demo,created_at)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (prj, "tn_xaru", did, pid(700 + i), slugify(DEVELOPERS[i][0]) + "-phase-1",
                     DEVELOPERS[i][0] + " — Phase 1", lid_city, "off_plan", "2026-03-01",
                     (i % 4) + 1, 2028 + (i % 2), 18 + i * 9, "Developer report", NOW,
                     850_000_00, 6_400_000_00, "USD", 180 + i * 40, 96 + i * 12,
                     "Demo off-plan project of the XARU HOME platform.", None, 1, NOW))
        plan = uid("pln", i + 1)
        cur.execute("INSERT INTO payment_plans VALUES (?,?,?,?)", (plan, prj, "60/40", 1))
        for j, (lbl, pct, trg) in enumerate((("Reservation", 10, "booking"),
                                             ("During construction", 50, "milestones"),
                                             ("On handover", 40, "handover"))):
            cur.execute("INSERT INTO payment_plan_milestones VALUES (?,?,?,?,?,?)",
                        (uid("mil", i * 10 + j), plan, lbl, pct, trg, j))
        for j in range(3):
            cur.execute("INSERT INTO unit_types VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                        (uid("unt", i * 10 + j), prj, "%d bedroom" % (j + 1), j + 1, j + 1,
                         62 + j * 40, 96 + j * 55, (850_000 + j * 900_000) * 100,
                         (1_400_000 + j * 1_500_000) * 100, "USD", 24 + j * 8))

    # ---- demanda de prueba
    for i in range(140):
        lid = listings[(i * 37) % len(listings)]
        aid = agent_ids[i % len(agent_ids)]
        stage = ["new", "contacted", "qualified", "viewing", "negotiation", "won", "lost"][i % 7]
        cur.execute("""INSERT INTO leads (id, public_id, tenant_id, listing_id, project_id,
                       agent_id, org_id, user_id, channel, contact_name, contact_email,
                       contact_phone, message, consent_given, consent_basis, utm_source,
                       utm_medium, utm_campaign, referer, stage, priority, spam_score,
                       budget_min_minor, budget_max_minor, budget_currency, dedupe_key,
                       sla_due_at, first_response_at, lost_reason, is_demo, created_at, updated_at)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (uid("led", i + 1), pid(5000 + i), "tn_xaru", lid, None, aid,
                     org_ids[i % len(org_ids)], buyer_ids[i % len(buyer_ids)],
                     ["form", "whatsapp", "call", "email"][i % 4],
                     BUYER_NAMES[i % len(BUYER_NAMES)],
                     "buyer%02d@demo.xaruhome.com" % ((i % 12) + 1), None,
                     "Consulta de prueba generada por la siembra de la plataforma.", 1,
                     "consent", "demo", "seed", "platform-demo", None, stage, "normal", 0.0,
                     500_000_00, 4_000_000_00, "USD", None, iso(i % 30), None, None, 1,
                     iso(i % 90), iso(i % 30)))
        cur.execute("INSERT INTO lead_activities VALUES (?,?,?,?,?,?)",
                    (uid("act", i + 1), uid("led", i + 1), "note",
                     "Lead de muestra creado por la siembra.", "seed", iso(i % 90)))

    for i, bid in enumerate(buyer_ids):
        for j in range(4):
            cur.execute("INSERT OR IGNORE INTO favorites VALUES (?,?,?,?,?)",
                        (bid, listings[(i * 53 + j * 11) % len(listings)], "default", None, NOW))
        ss = uid("sav", i + 1)
        q = {"offeringType": "sale", "countryCode": list(WORLD)[i % len(WORLD)],
             "price": {"currency": "USD", "max": "5000000"}}
        cur.execute("INSERT INTO saved_searches VALUES (?,?,?,?,?,?)",
                    (ss, bid, "Búsqueda de prueba %02d" % (i + 1), json.dumps(q),
                     "/real-estate/search/?offeringType=sale", NOW))
        cur.execute("INSERT INTO alert_subscriptions VALUES (?,?,?,?,?,?,?,?)",
                    (uid("alr", i + 1), ss, bid, ["instant", "daily", "weekly"][i % 3],
                     "email", None, 1, NOW))

    # ---- inventario en tramitacion --------------------------------------
    # Una cola de moderacion en la que todo esta aprobado no es una cola. Estos
    # registros NO tocan lo publicado: se anaden aparte, en los estados previos
    # a la publicacion, para que el ciclo de vida y el panel de administracion
    # tengan trabajo real que enseñar. La vista publica no los muestra, asi que
    # el inventario visible no cambia ni en uno.
    # Los diecisiete estados del ciclo de vida estan en el CHECK del esquema;
    # aqui se usan los seis que preceden o suceden a la publicacion.
    PENDING_STATES = [
        ("DRAFT", "pending", None),
        ("HUMAN_REVIEW", "pending", "photo_quality"),
        ("AUTOMATED_REVIEW", "pending", "duplicate_check,price_outlier"),
        ("REJECTED", "rejected", "permit_missing"),
        ("EXPIRED", "approved", None),
        ("PAUSED", "approved", None),
    ]
    pending_ids = []
    src = cur.execute("SELECT * FROM listings WHERE lifecycle_status='PUBLISHED' "
                      "ORDER BY public_id LIMIT 200").fetchall()
    cols = [d[0] for d in cur.description]
    for i in range(60):
        base = dict(zip(cols, src[(i * 7) % len(src)]))
        state, mod, rules = PENDING_STATES[i % len(PENDING_STATES)]
        nid = uid("lstq", i + 1)
        base["id"] = nid
        base["public_id"] = pid(700000 + i)
        base["external_reference"] = "XH-Q%05d" % i
        base["lifecycle_status"] = state
        base["moderation_status"] = mod
        base["quality_score"] = 34 + (i * 7) % 45
        base["published_at"] = (None if state in ("DRAFT", "HUMAN_REVIEW", "AUTOMATED_REVIEW")
                                else base["published_at"])
        base["created_at"] = iso(i % 21)
        base["updated_at"] = iso(i % 9)
        cur.execute("INSERT INTO listings (%s) VALUES (%s)"
                    % (",".join(cols), ",".join(["?"] * len(cols))),
                    tuple(base[c] for c in cols))
        cur.execute("INSERT INTO listing_media VALUES (?,?,?,?)",
                    (nid, base["hero_media_id"], 0, 1))
        for loc in ("en", "es", "ar", "zh"):
            row = cur.execute("SELECT title, description FROM listing_translations "
                              "WHERE listing_id=? AND locale=?",
                              (dict(zip(cols, src[(i * 7) % len(src)]))["id"], loc)).fetchone()
            cur.execute("INSERT INTO listing_translations VALUES (?,?,?,?,?,?,?)",
                        (nid, loc, (row[0] if row else "Draft listing"),
                         (row[1] if row else None), None,
                         slugify(row[0] if row else "draft") + "-q" + str(i), "machine"))
        pending_ids.append((nid, state, rules))

    # ---- operación
    # La cola se arma sobre lo que de verdad espera decisión, no sobre activos
    # ya publicados: 42 casos con su regla incumplida y su SLA.
    # La cola se ordena por vencimiento, asi que si todos los casos comparten
    # SLA la primera pantalla sale monotona: treinta filas identicas. Se
    # reparten el plazo, la regla y la prioridad, y un tercio va vencido, que
    # es lo que hace util una cola.
    RULE_MIX = ["photo_quality", "duplicate_check", "price_outlier",
                "permit_missing", "photo_quality,duplicate_check",
                "price_outlier,permit_missing"]
    ci = 0
    for (nid, state, rules) in pending_ids:
        if state not in ("HUMAN_REVIEW", "AUTOMATED_REVIEW", "REJECTED"):
            continue
        ci += 1
        # dias hasta el vencimiento: negativo = vencido
        due = [-2, -1, 0, 1, 1, 2, 3, 5][ci % 8]
        cur.execute("INSERT INTO moderation_cases VALUES (?,?,?,?,?,?,?,?,?)",
                    (uid("mod", ci), nid, iso(2 + ci % 12),
                     ["urgent", "high", "normal", "normal", "high"][ci % 5],
                     iso(-due),
                     "decided" if state == "REJECTED" else
                     ("in_review" if ci % 4 == 0 else "open"),
                     round(0.06 + 0.09 * (ci % 10), 2),
                     rules if (ci % 3 == 0 and rules) else RULE_MIX[ci % len(RULE_MIX)],
                     ("moderator%02d" % (ci % 4)) if ci % 3 == 0 else None))
    for i in range(12):
        ci += 1
        cur.execute("INSERT INTO moderation_cases VALUES (?,?,?,?,?,?,?,?,?)",
                    (uid("mod", ci), listings[(i * 97) % len(listings)], iso(i % 14),
                     ["normal", "high", "urgent"][i % 3], iso(-1),
                     "decided", round(0.12 * (i % 6), 2),
                     "photo_quality,duplicate_check", "moderator01"))
    cur.execute("INSERT INTO plans VALUES (?,?,?,?,?,?,?,?)",
                ("professional", "Professional", "USD", 49900, "month", 500, 25, "featured,api,crm"))
    cur.execute("INSERT INTO plans VALUES (?,?,?,?,?,?,?,?)",
                ("developer", "Developer", "USD", 149900, "month", 2000, 60, "projects,api,crm,promotions"))
    for i, oid in enumerate(org_ids):
        cur.execute("INSERT INTO subscriptions VALUES (?,?,?,?,?,?,?)",
                    (uid("sub", i + 1), oid, "professional", "active", NOW, "2026-09-02", 12))
        cur.execute("INSERT INTO credit_ledger VALUES (?,?,?,?,?,?,?)",
                    (uid("cl", i * 2 + 1), oid, "purchase", 5000, "seed", "seed-buy-%d" % i, NOW))
        cur.execute("INSERT INTO credit_ledger VALUES (?,?,?,?,?,?,?)",
                    (uid("cl", i * 2 + 2), oid, "consumption", -1200, "seed", "seed-use-%d" % i, NOW))

    # ---- perfil del agente derivado de su cartera --------------------------
    # Especialidades, zonas y tiempo de respuesta no se inventan: salen de lo
    # que cada asesor lleva realmente. Un perfil vacio en un directorio es peor
    # que no tener directorio.
    for aid in agent_ids:
        specs = [r[0] for r in cur.execute(
            "SELECT subtype, COUNT(*) c FROM listings WHERE agent_id=? AND subtype IS NOT NULL "
            "GROUP BY subtype ORDER BY c DESC LIMIT 4", (aid,))]
        areas = [r[0] for r in cur.execute(
            "SELECT country_code, COUNT(*) c FROM listings WHERE agent_id=? "
            "GROUP BY country_code ORDER BY c DESC LIMIT 5", (aid,))]
        n = cur.execute("SELECT COUNT(*) FROM listings WHERE agent_id=?", (aid,)).fetchone()[0]
        h = sum(ord(ch) for ch in aid)
        cur.execute("""UPDATE agents SET specialities=?, service_areas=?,
                       response_minutes_p50=?, rating_avg=?, rating_count=?,
                       phone=?, whatsapp=?
                       WHERE id=?""",
                    (",".join(specs), ",".join(areas),
                     18 + (h % 5) * 12,
                     round(4.2 + (h % 8) / 10.0, 1),
                     max(3, n // 3),
                     "+971 4 000 %04d" % (h % 10000),
                     "+971 50 000 %04d" % (h % 10000),
                     aid))

    con.commit()

    stats = {}
    for t in ("locations", "property_types", "amenities", "organizations", "agents", "users",
              "listings", "listing_translations", "listing_amenities", "projects", "leads",
              "favorites", "saved_searches", "alert_subscriptions", "moderation_cases",
              "outbox_events", "listing_transitions", "credit_ledger", "media"):
        stats[t] = cur.execute("SELECT COUNT(*) FROM %s" % t).fetchone()[0]
    con.close()

    print("Base de datos: %s" % DB)
    for k, v in stats.items():
        print("  %-24s %6d" % (k, v))


if __name__ == "__main__":
    main()
