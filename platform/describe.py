# -*- coding: utf-8 -*-
"""Descripción del activo compuesta a partir de sus propios datos.

Una ficha sin descripción no es una ficha. Pero inventar prosa comercial para
un inventario de muestra sería peor: cada frase afirmaría algo que no está en
ninguna columna, y el día que entre inventario real nadie sabría distinguir lo
descrito de lo imaginado.

Aquí no se inventa nada. Cada oración se arma con campos que ya existen en la
fila —tipología, ciudad, país, superficies, dormitorios, baños, estado de obra,
régimen de propiedad, amenidades, verificación— y si un campo falta, la oración
que dependía de él sencillamente no se escribe. El resultado se lee como una
descripción redactada porque el orden y las conjunciones están cuidados, no
porque se haya añadido nada.

Cuatro idiomas, misma composición. Los topónimos no se traducen nunca: el
nombre de la plaza es el mismo en las cuatro versiones, que es la regla de la
casa.
"""

# Grupos de amenidades: se mencionan por familia, no una a una, porque una
# enumeración de veinte comas no la lee nadie.
AMENITY_GROUP = {
    "climate":    {"en": "climate control", "es": "climatización",
                   "ar": "تحكّم بالمناخ", "zh": "温控系统"},
    "wellness":   {"en": "wellness facilities", "es": "instalaciones de bienestar",
                   "ar": "مرافق العافية", "zh": "康养设施"},
    "leisure":    {"en": "leisure amenities", "es": "amenidades de ocio",
                   "ar": "مرافق ترفيهية", "zh": "休闲配套"},
    "security":   {"en": "security provision", "es": "seguridad",
                   "ar": "منظومة أمنية", "zh": "安防配置"},
    "outdoor":    {"en": "outdoor space", "es": "espacio exterior",
                   "ar": "مساحات خارجية", "zh": "户外空间"},
    "services":   {"en": "building services", "es": "servicios del edificio",
                   "ar": "خدمات المبنى", "zh": "楼宇服务"},
    "technology": {"en": "building technology", "es": "tecnología del edificio",
                   "ar": "تقنيات المبنى", "zh": "楼宇科技"},
    "parking":    {"en": "parking", "es": "aparcamiento", "ar": "مواقف", "zh": "停车位"},
    "views":      {"en": "open views", "es": "vistas abiertas",
                   "ar": "إطلالات مفتوحة", "zh": "开阔视野"},
    "access":     {"en": "private access", "es": "acceso privado",
                   "ar": "وصول خاص", "zh": "私密通道"},
}

COMPLETION = {
    "ready":    {"en": "ready to occupy", "es": "listo para ocupar",
                 "ar": "جاهز للإشغال", "zh": "可即时入住"},
    "off_plan": {"en": "off-plan, with handover scheduled",
                 "es": "off-plan, con entrega prevista",
                 "ar": "على المخطط، مع تسليم مقرّر", "zh": "期房，交付时间已定"},
}

OWNERSHIP = {
    "freehold": {"en": "freehold", "es": "en pleno dominio",
                 "ar": "تملّك حر", "zh": "永久产权"},
    "leasehold": {"en": "leasehold", "es": "en derecho de superficie",
                  "ar": "حق انتفاع", "zh": "租赁产权"},
}

# Plantillas. Cada una recibe solo los datos que existen.
S = {
 "open_res": {
   "en": "%(type)s in %(city)s, %(country)s.",
   "es": "%(type)s en %(city)s, %(country)s.",
   "ar": "%(type)s في %(city)s، %(country)s.",
   "zh": "位于%(country)s%(city)s的%(type)s。"},
 "beds": {
   "en": " The residence is laid out over %(built)s and comprises %(bd)d bedrooms and %(ba)d bathrooms.",
   "es": " La residencia se distribuye en %(built)s y cuenta con %(bd)d dormitorios y %(ba)d baños.",
   "ar": " تمتد المساحة على %(built)s وتضم %(bd)d غرف نوم و%(ba)d حمامات.",
   "zh": "住宅建筑面积%(built)s，设%(bd)d间卧室与%(ba)d间浴室。"},
 "beds_noarea": {
   "en": " It comprises %(bd)d bedrooms and %(ba)d bathrooms.",
   "es": " Cuenta con %(bd)d dormitorios y %(ba)d baños.",
   "ar": " يضم %(bd)d غرف نوم و%(ba)d حمامات.",
   "zh": "设%(bd)d间卧室与%(ba)d间浴室。"},
 "plot": {
   "en": " The plot extends to %(plot)s.",
   "es": " La parcela alcanza %(plot)s.",
   "ar": " تبلغ مساحة القطعة %(plot)s.",
   "zh": "地块面积%(plot)s。"},
 "hect": {
   "en": " The holding extends to %(ha)s hectares.",
   "es": " La superficie alcanza %(ha)s hectáreas.",
   "ar": " تمتد الحيازة على %(ha)s هكتار.",
   "zh": "占地%(ha)s公顷。"},
 "area_only": {
   "en": " The asset occupies %(built)s.",
   "es": " El activo ocupa %(built)s.",
   "ar": " يشغل الأصل %(built)s.",
   "zh": "资产建筑面积%(built)s。"},
 "keys": {
   "en": " It operates with %(keys)d keys.",
   "es": " Opera con %(keys)d llaves.",
   "ar": " يعمل بـ%(keys)d مفتاحاً.",
   "zh": "现有客房%(keys)d间。"},
 "berths": {
   "en": " The marina holds %(berths)d berths.",
   "es": " La marina dispone de %(berths)d amarres.",
   "ar": " يضم المرسى %(berths)d مرسى.",
   "zh": "码头设%(berths)d个泊位。"},
 "completion": {
   "en": " The asset is %(comp)s.",
   "es": " El activo está %(comp)s.",
   "ar": " الأصل %(comp)s.",
   "zh": "该资产%(comp)s。"},
 "handover": {
   "en": " Handover is scheduled for Q%(q)d %(y)d.",
   "es": " La entrega está prevista para el %(q)dT de %(y)d.",
   "ar": " التسليم مقرّر في الربع %(q)d من %(y)d.",
   "zh": "预计%(y)d年第%(q)d季度交付。"},
 "ownership": {
   "en": " Title is held %(own)s under %(cc)s law.",
   "es": " La titularidad se ostenta %(own)s bajo la legislación de %(cc)s.",
   "ar": " الملكية %(own)s وفق قانون %(cc)s.",
   "zh": "产权为%(own)s，适用%(cc)s法律。"},
 "amen": {
   "en": " Provision includes %(list)s.",
   "es": " La dotación incluye %(list)s.",
   "ar": " تشمل التجهيزات %(list)s.",
   "zh": "配套包括%(list)s。"},
 "verified": {
   "en": " The listing has been verified by the XARU HOME desk and its documentation reviewed.",
   "es": " El activo ha sido verificado por la mesa de XARU HOME y su documentación revisada.",
   "ar": " تم توثيق العرض من قبل مكتب XARU HOME ومراجعة مستنداته.",
   "zh": "该房源已由 XARU HOME 团队核验，相关文件亦经审阅。"},
 "unverified": {
   "en": " Verification of this listing is in progress; particulars are provided by the holder of the mandate.",
   "es": " La verificación de este activo está en curso; los datos los aporta el titular del mandato.",
   "ar": " توثيق هذا العرض قيد الإنجاز؛ والبيانات مقدَّمة من صاحب التفويض.",
   "zh": "该房源核验进行中；资料由委托持有方提供。"},
 "demo": {
   "en": " This record is platform demonstration inventory: the structure, the workflow and the data model are the production ones, the asset is not.",
   "es": " Este registro es inventario de demostración de la plataforma: la estructura, el flujo y el modelo de datos son los de producción; el activo no.",
   "ar": " هذا السجل ضمن المعروض التجريبي للمنصة: البنية وسير العمل ونموذج البيانات هي نفسها الإنتاجية، أما الأصل فلا.",
   "zh": "本条为平台演示资产：架构、流程与数据模型均与正式环境一致，资产本身则非真实。"},
}


def _n(v, loc):
    """Miles con el separador del idioma."""
    try:
        v = int(round(float(v)))
    except (TypeError, ValueError):
        return None
    s = "{:,}".format(v)
    if loc == "es":
        s = s.replace(",", ".")
    return s


def _area(v, loc):
    n = _n(v, loc)
    return None if n is None else ("%s م²" % n if loc == "ar" else "%s m²" % n)


def _join(items, loc):
    items = [x for x in items if x]
    if not items:
        return None
    if loc == "zh":
        return "、".join(items)
    if len(items) == 1:
        return items[0]
    tail = {"en": " and ", "es": " y ", "ar": " و"}[loc]
    return ", ".join(items[:-1]) + tail + items[-1]


def describe(loc, *, type_name, city, country, bedrooms=None, bathrooms=None,
             built=None, plot=None, hectares=None, keys=None, berths=None,
             completion=None, handover_q=None, handover_y=None,
             ownership=None, cc=None, amenity_categories=(), verified=False,
             is_demo=False):
    """Compone la descripción. Cada oración que no tiene dato, no se escribe."""
    out = [S["open_res"][loc] % {"type": type_name, "city": city, "country": country}]

    b = _area(built, loc)
    if bedrooms and bathrooms:
        key = "beds" if b else "beds_noarea"
        out.append(S[key][loc] % {"built": b, "bd": int(bedrooms), "ba": int(bathrooms)})
    elif b:
        out.append(S["area_only"][loc] % {"built": b})

    p = _area(plot, loc)
    if p:
        out.append(S["plot"][loc] % {"plot": p})
    h = _n(hectares, loc)
    if h:
        out.append(S["hect"][loc] % {"ha": h})
    if keys:
        out.append(S["keys"][loc] % {"keys": int(keys)})
    if berths:
        out.append(S["berths"][loc] % {"berths": int(berths)})

    if completion in COMPLETION:
        out.append(S["completion"][loc] % {"comp": COMPLETION[completion][loc]})
    if handover_q and handover_y:
        out.append(S["handover"][loc] % {"q": int(handover_q), "y": int(handover_y)})
    if ownership in OWNERSHIP and cc:
        out.append(S["ownership"][loc] % {"own": OWNERSHIP[ownership][loc], "cc": cc})

    groups = []
    for c in amenity_categories:
        g = AMENITY_GROUP.get(c)
        if g and g[loc] not in groups:
            groups.append(g[loc])
    lst = _join(groups[:4], loc)
    if lst:
        out.append(S["amen"][loc] % {"list": lst})

    out.append(S["verified" if verified else "unverified"][loc])
    if is_demo:
        out.append(S["demo"][loc])
    return "".join(out).strip()
