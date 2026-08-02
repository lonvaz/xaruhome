/*
 * XARU HOME — Marketplace (PLP)
 * =============================================================
 * Página de resultados con paridad funcional de un portal inmobiliario de
 * gran escala: lista, mapa y vista dividida; filtros combinables sincronizados
 * con la URL; orden; paginación; facetas con conteo; favoritos, búsqueda
 * guardada y alerta.
 *
 * MODO SIMULACIÓN
 * ---------------
 * No hay servidor todavía. El inventario llega de `/data/api/v1/search-index
 * .json`, que es la proyección que publica `platform/export_api.py` desde la
 * base de datos real, con la forma que tendrá la respuesta de
 * `GET /api/v1/search/listings`. El filtrado y las facetas se resuelven aquí;
 * el día que exista el Search Service, `query()` pasa a ser una llamada de red
 * y todo lo demás — URL, estado, render, mapa — se queda igual.
 *
 * Lo que persiste (favoritos, búsquedas guardadas, alertas) se guarda hoy en
 * el almacenamiento del navegador a través de `Store`, un adaptador con la
 * misma firma que tendrá el Engagement Service. Cambiar de uno a otro es
 * cambiar la implementación de tres métodos.
 */
(function () {
  "use strict";

  var HOST = document.querySelector("[data-marketplace]");
  /* data-preview="6" convierte el montaje en escaparate: seis fichas y un
     enlace a la busqueda completa, sin barra ni paginacion. */
  var PREVIEW = HOST ? (parseInt(HOST.getAttribute("data-preview") || "0", 10) || 0) : 0;
  if (!HOST) return;

  var API = "data/api/v1/";
  var PAGE_SIZE = 24;

  /* ---------------------------------------------------------------- i18n */
  function lang() {
    var l = (document.documentElement.getAttribute("lang") || "en").slice(0, 2);
    return ["en", "es", "ar", "zh"].indexOf(l) >= 0 ? l : "en";
  }
  var L = lang();
  /* Rutas absolutas desde la raiz del dominio, igual que el resto del sitio
     (el generador ya emite /assets/... en el head). R apunta a la raiz —de ahi
     cuelgan los datos y las imagenes, que son unicos para los cuatro idiomas—
     y PR al arbol del idioma, de donde cuelgan las paginas. */
  var R = "/";
  var PR = "/" + (L === "en" ? "" : L + "/");

  var T = {
    results:   {en:"assets",es:"activos",ar:"أصل",zh:"项资产"},
    seeAll:    {en:"See all {n} assets",es:"Ver los {n} activos",
                ar:"عرض كل الأصول ({n})",zh:"查看全部 {n} 项资产"},
    prevEmpty: {en:"No live inventory in this category right now.",
                es:"Ahora mismo no hay inventario activo en esta categoría.",
                ar:"لا يوجد معروض نشط في هذه الفئة حالياً.",
                zh:"该类别目前没有在售资产。"},
    of:        {en:"of",es:"de",ar:"من",zh:"共"},
    showing:   {en:"Showing",es:"Mostrando",ar:"عرض",zh:"显示"},
    sort:      {en:"Sort",es:"Ordenar",ar:"ترتيب",zh:"排序"},
    recommended:{en:"Recommended",es:"Recomendados",ar:"موصى به",zh:"推荐"},
    newest:    {en:"Newest",es:"Más recientes",ar:"الأحدث",zh:"最新"},
    priceAsc:  {en:"Price: low to high",es:"Precio: menor a mayor",ar:"السعر: تصاعدي",zh:"价格：从低到高"},
    priceDesc: {en:"Price: high to low",es:"Precio: mayor a menor",ar:"السعر: تنازلي",zh:"价格：从高到低"},
    areaDesc:  {en:"Largest area",es:"Mayor superficie",ar:"الأكبر مساحة",zh:"面积最大"},
    ppaAsc:    {en:"Price per m²",es:"Precio por m²",ar:"السعر لكل م²",zh:"每平米价格"},
    list:      {en:"List",es:"Lista",ar:"قائمة",zh:"列表"},
    map:       {en:"Map",es:"Mapa",ar:"خريطة",zh:"地图"},
    split:     {en:"Split",es:"Dividida",ar:"مقسّم",zh:"分屏"},
    filters:   {en:"Filters",es:"Filtros",ar:"عوامل التصفية",zh:"筛选"},
    reset:     {en:"Clear all",es:"Limpiar todo",ar:"مسح الكل",zh:"清除全部"},
    apply:     {en:"Apply",es:"Aplicar",ar:"تطبيق",zh:"应用"},
    save:      {en:"Save this search",es:"Guardar esta búsqueda",ar:"حفظ هذا البحث",zh:"保存此搜索"},
    saved:     {en:"Search saved",es:"Búsqueda guardada",ar:"تم حفظ البحث",zh:"已保存搜索"},
    alert:     {en:"Create alert",es:"Crear alerta",ar:"إنشاء تنبيه",zh:"创建提醒"},
    empty:     {en:"No assets match these filters.",es:"Ningún activo coincide con estos filtros.",
                ar:"لا توجد أصول تطابق هذه المعايير.",zh:"没有资产符合这些筛选条件。"},
    emptyHint: {en:"Try widening the price range or removing a filter.",
                es:"Pruebe a ampliar el rango de precio o a quitar un filtro.",
                ar:"جرّب توسيع نطاق السعر أو إزالة أحد المرشحات.",
                zh:"请尝试放宽价格区间或移除一个筛选条件。"},
    loading:   {en:"Loading inventory…",es:"Cargando inventario…",ar:"جارٍ تحميل المعروض…",zh:"正在加载资产…"},
    error:     {en:"Inventory could not be loaded.",es:"No se pudo cargar el inventario.",
                ar:"تعذّر تحميل المعروض.",zh:"无法加载资产。"},
    retry:     {en:"Retry",es:"Reintentar",ar:"إعادة المحاولة",zh:"重试"},
    anyLoc:    {en:"Any location",es:"Cualquier ubicación",ar:"أي موقع",zh:"任意地点"},
    anyType:   {en:"Any type",es:"Cualquier tipo",ar:"أي نوع",zh:"任意类型"},
    beds:      {en:"Bedrooms",es:"Dormitorios",ar:"غرف النوم",zh:"卧室"},
    baths:     {en:"Bathrooms",es:"Baños",ar:"الحمامات",zh:"浴室"},
    price:     {en:"Price",es:"Precio",ar:"السعر",zh:"价格"},
    area:      {en:"Area (m²)",es:"Superficie (m²)",ar:"المساحة (م²)",zh:"面积（㎡）"},
    amenities: {en:"Amenities",es:"Amenidades",ar:"المرافق",zh:"设施"},
    verified:  {en:"Verified only",es:"Solo verificados",ar:"الموثّقة فقط",zh:"仅已核验"},
    completion:{en:"Completion",es:"Estado de obra",ar:"حالة الإنجاز",zh:"交付状态"},
    ready:     {en:"Ready",es:"Listo",ar:"جاهز",zh:"现房"},
    offplan:   {en:"Off-plan",es:"Off-plan",ar:"على المخطط",zh:"期房"},
    min:       {en:"Min",es:"Mín",ar:"الأدنى",zh:"最低"},
    max:       {en:"Max",es:"Máx",ar:"الأعلى",zh:"最高"},
    sale:      {en:"Buy",es:"Comprar",ar:"شراء",zh:"购买"},
    rent:      {en:"Rent",es:"Alquilar",ar:"إيجار",zh:"租赁"},
    poa:       {en:"Price upon application",es:"Precio a consulta",ar:"السعر عند الطلب",zh:"价格面议"},
    perYear:   {en:"/ year",es:"/ año",ar:"/ سنة",zh:"/ 年"},
    demo:      {en:"Sample",es:"Muestra",ar:"عيّنة",zh:"样例"},
    verifiedB: {en:"Verified",es:"Verificado",ar:"موثّق",zh:"已核验"},
    fav:       {en:"Save",es:"Guardar",ar:"حفظ",zh:"收藏"},
    share:     {en:"Share",es:"Compartir",ar:"مشاركة",zh:"分享"},
    call:      {en:"Call",es:"Llamar",ar:"اتصال",zh:"致电"},
    email:     {en:"Email",es:"Email",ar:"بريد",zh:"邮件"},
    whatsapp:  {en:"WhatsApp",es:"WhatsApp",ar:"واتساب",zh:"WhatsApp"},
    page:      {en:"Page",es:"Página",ar:"صفحة",zh:"第"},
    prev:      {en:"Previous",es:"Anterior",ar:"السابق",zh:"上一页"},
    next:      {en:"Next",es:"Siguiente",ar:"التالي",zh:"下一页"},
    simNote:   {en:"Sample inventory shown while the live portfolio is being loaded. Saved items are kept on this device.",
                es:"Inventario de muestra mientras se carga el portafolio real. Lo que guarde queda en este dispositivo.",
                ar:"معروض تجريبي ريثما تُحمَّل المحفظة الفعلية. وما تحفظه يبقى على هذا الجهاز.",
                zh:"正式资产组合载入期间显示样例资产。您的收藏保存在本设备。"},
    searchHere:{en:"Search this area",es:"Buscar en esta zona",ar:"ابحث في هذه المنطقة",zh:"搜索此区域"},
    qPlace:    {en:"City, country, typology or reference",
                es:"Ciudad, país, tipología o referencia",
                ar:"مدينة أو دولة أو نوع أو مرجع",
                zh:"城市、国家、类型或编号"},
    keysL:     {en:"keys",es:"llaves",ar:"مفتاح",zh:"客房"},
    featured:  {en:"Featured",es:"Destacado",ar:"مميّز",zh:"精选"},
    premium:   {en:"Premium",es:"Premium",ar:"بريميوم",zh:"尊享"},
    spotlight: {en:"Spotlight",es:"En foco",ar:"تحت الضوء",zh:"聚焦"},
    haL:       {en:"ha",es:"ha",ar:"هكتار",zh:"公顷"},
    sqmL:      {en:"m²",es:"m²",ar:"م²",zh:"㎡"},
    photos:    {en:"photos",es:"fotos",ar:"صورة",zh:"张"},
    planL:     {en:"Floor plan",es:"Plano",ar:"مخطط",zh:"户型图"},
    tourL:     {en:"360° tour",es:"Tour 360°",ar:"جولة 360°",zh:"360°看房"},
    dropL:     {en:"price drop",es:"de bajada",ar:"انخفاض",zh:"降价"},
    listedToday:{en:"Listed today",es:"Publicado hoy",ar:"نُشر اليوم",zh:"今日发布"},
    listedD:   {en:"Listed %d days ago",es:"Publicado hace %d días",
                ar:"نُشر قبل %d يوماً",zh:"%d 天前发布"},
    listedM:   {en:"Listed %d months ago",es:"Publicado hace %d meses",
                ar:"نُشر قبل %d أشهر",zh:"%d 个月前发布"},
    saveA:     {en:"Save",es:"Guardar",ar:"حفظ",zh:"收藏"},
    allTypes:  {en:"All",es:"Todas",ar:"الكل",zh:"全部"},
    createAlert:{en:"Create alert",es:"Crear alerta",ar:"إنشاء تنبيه",zh:"创建提醒"},
    alertOn:   {en:"Alert created",es:"Alerta creada",ar:"تم إنشاء التنبيه",zh:"提醒已创建"},
    closeF:    {en:"Close filters",es:"Cerrar filtros",ar:"إغلاق المرشحات",zh:"关闭筛选"},
    exploreT:  {en:"Continue exploring",es:"Seguir explorando",
                ar:"واصل الاستكشاف",zh:"继续探索"},
    exploreByCity:{en:"By market",es:"Por plaza",ar:"حسب السوق",zh:"按市场"},
    exploreByType:{en:"By typology",es:"Por tipología",ar:"حسب النوع",zh:"按类型"},
    exploreByCountry:{en:"By country",es:"Por país",ar:"حسب الدولة",zh:"按国家"},
    furnish:   {en:"Furnishing",es:"Amueblado",ar:"التأثيث",zh:"家具配置"},
    anyFurn:   {en:"Any",es:"Cualquiera",ar:"الكل",zh:"不限"},
    furnished: {en:"Furnished",es:"Amueblado",ar:"مفروش",zh:"带家具"},
    unfurnished:{en:"Unfurnished",es:"Sin amueblar",ar:"غير مفروش",zh:"无家具"},
    partly_furnished:{en:"Partly furnished",es:"Parcialmente amueblado",
                      ar:"مفروش جزئياً",zh:"部分家具"},
    ppsqm:     {en:"Price per m²",es:"Precio por m²",ar:"السعر لكل م²",zh:"每平米单价"},
    kw:        {en:"Keywords",es:"Palabras clave",ar:"كلمات مفتاحية",zh:"关键词"},
    kwPlace:   {en:"e.g. beachfront, private pool",es:"p. ej. frente al mar, piscina privada",
                ar:"مثل: على الشاطئ، مسبح خاص",zh:"例如：海滨、私人泳池"},
    extras:    {en:"Listing includes",es:"El anuncio incluye",
                ar:"يتضمن العرض",zh:"房源包含"},
    hasPlan:   {en:"Floor plan",es:"Plano de planta",ar:"مخطط الطابق",zh:"户型图"},
    hasTour:   {en:"360° tour",es:"Recorrido 360°",ar:"جولة 360°",zh:"360°看房"},
    hasDrop:   {en:"Price reduced",es:"Precio rebajado",ar:"سعر مخفَّض",zh:"已降价"},
    anyState:  {en:"Any status",es:"Cualquier estado",ar:"أي حالة",zh:"不限状态"},
    showN:     {en:"Show %s assets",es:"Mostrar %s activos",
                ar:"عرض %s أصل",zh:"显示 %s 项资产"},
    showNone:  {en:"No matches",es:"Sin coincidencias",ar:"لا نتائج",zh:"无匹配"}
  };
  function t(k) { return (T[k] && (T[k][L] || T[k].en)) || k; }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function nf(v) {
    try { return new Intl.NumberFormat(L === "zh" ? "zh-CN" : L === "ar" ? "ar-AE"
      : L === "es" ? "es-ES" : "en-US").format(v); } catch (e) { return String(v); }
  }
  function money(v, cur) {
    try { return new Intl.NumberFormat(L === "zh" ? "zh-CN" : L === "ar" ? "ar-AE"
      : L === "es" ? "es-ES" : "en-US",
      { style: "currency", currency: cur || "USD", maximumFractionDigits: 0 }).format(v); }
    catch (e) { return (cur || "USD") + " " + nf(v); }
  }
  function norm(s) {
    s = String(s || "").toLowerCase();
    try { s = s.normalize("NFD").replace(/[̀-ͯ]/g, ""); } catch (e) {}
    return s.replace(/\s+/g, " ").trim();
  }

  /* ------------------------------------------------- adaptador de persistencia
     Misma firma que tendrá el Engagement Service. Hoy escribe en el navegador;
     mañana serán PUT /api/v1/me/favorites y POST /api/v1/me/saved-searches. */
  var Store = {
    _read: function (k) { try { return JSON.parse(localStorage.getItem(k) || "[]"); } catch (e) { return []; } },
    _write: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} },
    favorites: function () { return this._read("xaru_favorites"); },
    toggleFavorite: function (id) {
      var f = this.favorites(), i = f.indexOf(id);
      if (i >= 0) f.splice(i, 1); else f.push(id);
      this._write("xaru_favorites", f);
      return i < 0;
    },
    savedSearches: function () { return this._read("xaru_saved_searches"); },
    saveSearch: function (name, qs, path, base, alert) {
      var s = this.savedSearches();
      var hit = null;
      s.forEach(function (x) { if (x.qs === qs && x.path === path) hit = x; });
      if (hit) {
        if (alert && !hit.alert) { hit.alert = true; hit.freq = hit.freq || "daily"; }
        else { return false; }
      } else {
        s.push({ name: name, qs: qs, path: path, base: base || {},
                 alert: !!alert, freq: alert ? "daily" : null,
                 at: new Date().toISOString() });
      }
      this._write("xaru_saved_searches", s);
      return true;
    }
  };

  /* ---------------------------------------------------------------- estado */
  var DATA = null, META = null, LOCS = null;
  var STATE = {};

  var LIST_KEYS = ["type", "cc", "city", "am"];
  var NUM_KEYS = ["bedsMin", "bedsMax", "bathsMin", "priceMin", "priceMax",
                  "areaMin", "areaMax", "ppsqmMin", "ppsqmMax", "page"];

  function readURL() {
    var p = new URLSearchParams(location.search);
    var s = {
      q: p.get("q") || "",
      offering: p.get("offering") || HOST.getAttribute("data-offering") || "",
      category: p.get("category") || HOST.getAttribute("data-category") || "",
      sort: p.get("sort") || "recommended",
      ag: p.get("ag") || "",
      og: p.get("og") || "",
      view: p.get("view") || HOST.getAttribute("data-view") || "list",
      verified: p.get("verified") === "1",
      completion: p.get("completion") || "",
      furn: p.get("furn") || "",
      kw: p.get("kw") || "",
      plan: p.get("plan") === "1",
      tour: p.get("tour") === "1",
      drop: p.get("drop") === "1"
    };
    /* Los filtros de lista pueden venir fijados por el propio montaje, igual
       que offering y category: asi una pagina de pilar declara su tipologia en
       el HTML y no hace falta una segunda logica de consulta para ella. */
    LIST_KEYS.forEach(function (k) {
      s[k] = (p.get(k) || HOST.getAttribute("data-" + k) || "").split(",").filter(Boolean);
    });
    NUM_KEYS.forEach(function (k) {
      var v = parseFloat(p.get(k));
      s[k] = isNaN(v) ? null : v;
    });
    s.page = s.page || 1;
    return s;
  }

  function writeURL(replace) {
    var p = new URLSearchParams();
    if (STATE.q) p.set("q", STATE.q);
    if (STATE.offering && !HOST.getAttribute("data-offering")) p.set("offering", STATE.offering);
    if (STATE.category && !HOST.getAttribute("data-category")) p.set("category", STATE.category);
    LIST_KEYS.forEach(function (k) { if (STATE[k].length) p.set(k, STATE[k].join(",")); });
    NUM_KEYS.forEach(function (k) {
      if (k === "page") { if (STATE.page > 1) p.set("page", STATE.page); return; }
      if (STATE[k] != null) p.set(k, STATE[k]);
    });
    if (STATE.verified) p.set("verified", "1");
    if (STATE.completion) p.set("completion", STATE.completion);
    if (STATE.furn) p.set("furn", STATE.furn);
    if (STATE.kw) p.set("kw", STATE.kw);
    if (STATE.plan) p.set("plan", "1");
    if (STATE.tour) p.set("tour", "1");
    if (STATE.drop) p.set("drop", "1");
    if (STATE.ag) p.set("ag", STATE.ag);
    if (STATE.og) p.set("og", STATE.og);
    if (STATE.sort !== "recommended") p.set("sort", STATE.sort);
    if (STATE.view !== "list") p.set("view", STATE.view);
    var url = location.pathname + (p.toString() ? "?" + p.toString() : "");
    history[replace ? "replaceState" : "pushState"]({}, "", url);
  }

  /* ---------------------------------------------------------------- consulta
     Esta es la única función que cambia el día que exista el Search Service:
     pasará a ser `fetch(API + "search/listings", {method:"POST", body:…})`. */
  function query(state, items) {
    var terms = norm(state.q).split(" ").filter(Boolean);
    return items.filter(function (x) {
      if (state.offering && x.off !== state.offering) return false;
      if (state.category && x.cat !== state.category) return false;
      if (state.type.length && state.type.indexOf(x.type) < 0) return false;
      if (state.cc.length && state.cc.indexOf(x.cc) < 0) return false;
      if (state.city.length && state.city.indexOf(x.city) < 0) return false;
      if (state.ag && x.ag !== state.ag) return false;
      if (state.og && x.og !== state.og) return false;
      if (state.verified && !x.ver) return false;
      if (state.completion && x.comp !== state.completion) return false;
      if (state.furn && x.furn !== state.furn) return false;
      if (state.plan && !x.plan) return false;
      if (state.tour && !x.tour) return false;
      if (state.drop && !x.drop) return false;
      if (state.ppsqmMin != null && !(x.ppa != null && x.ppa >= state.ppsqmMin)) return false;
      if (state.ppsqmMax != null && !(x.ppa != null && x.ppa <= state.ppsqmMax)) return false;
      if (state.kw) {
        // Las palabras clave buscan en la descripcion larga y en las
        // amenidades, no solo en el titulo: quien escribe "piscina privada"
        // busca la amenidad, no el nombre del activo.
        var kws = norm(state.kw).split(/[\s,]+/).filter(Boolean);
        var bag = norm([x.t[L] || x.t.en, x.city,
                        (x.typeName && (x.typeName[L] || x.typeName.en)),
                        (x.am || []).join(" ")].filter(Boolean).join(" "));
        if (!kws.every(function (w) { return bag.indexOf(w) >= 0; })) return false;
      }
      if (state.bedsMin != null && !(x.bd >= state.bedsMin)) return false;
      if (state.bedsMax != null && !(x.bd && x.bd <= state.bedsMax)) return false;
      if (state.bathsMin != null && !(x.ba >= state.bathsMin)) return false;
      if (state.priceMin != null && !(x.p != null && x.p >= state.priceMin)) return false;
      if (state.priceMax != null && !(x.p != null && x.p <= state.priceMax)) return false;
      if (state.areaMin != null && !(x.area && x.area >= state.areaMin)) return false;
      if (state.areaMax != null && !(x.area && x.area <= state.areaMax)) return false;
      if (state.am.length && !state.am.every(function (a) { return (x.am || []).indexOf(a) >= 0; })) return false;
      if (terms.length) {
        var hay = norm([x.t[L] || x.t.en, x.city, x.cc,
                        (x.typeName && (x.typeName[L] || x.typeName.en)),
                        x.agName, x.ogName].filter(Boolean).join(" "));
        if (!terms.every(function (w) { return hay.indexOf(w) >= 0; })) return false;
      }
      return true;
    });
  }

  function sortItems(list, sort) {
    var c = list.slice();
    if (sort === "newest") c.sort(function (a, b) { return (b.pub || "").localeCompare(a.pub || ""); });
    else if (sort === "price-asc") c.sort(function (a, b) { return (a.p == null) - (b.p == null) || a.p - b.p; });
    else if (sort === "price-desc") c.sort(function (a, b) { return (a.p == null) - (b.p == null) || b.p - a.p; });
    else if (sort === "area-desc") c.sort(function (a, b) { return (b.area || 0) - (a.area || 0); });
    else if (sort === "ppa-asc") c.sort(function (a, b) { return (a.ppa || 1e12) - (b.ppa || 1e12); });
    else c.sort(function (a, b) {
      var r = (b.promo === "featured") - (a.promo === "featured");
      return r || (b.q || 0) - (a.q || 0);
    });
    return c;
  }

  /* ---------------------------------------------------------------- imagen */
  /* Escalera de reserva. Son los anchos que existen para TODA imagen del
     directorio; se usa solo si meta.json no trajera la lista real. Nunca debe
     prometer mas de lo seguro: un candidato de srcset que no existe se ve como
     una foto rota, no como una foto peor. */
  var WIDTHS_BY_DIR = {
    "assets/img/xaru/catalog/": [480, 768, 1280],
    "assets/img/xaru/gen2/":    [768, 1280, 1920]
  };
  /* Anchos reales por imagen, publicados por la API tras leer el disco. Antes
     se anunciaban 1920 y 2560 para todo el catalogo, pero 144 de los 156
     masters miden 1600 y esas derivadas nunca se generaron —con razon: no se
     inventa resolucion—. En pantalla grande o retina el navegador pedia el
     candidato grande, recibia un 404 y la propiedad aparecia sin foto. */
  function widthsFor(dir, base) {
    var t = META && META.imageWidths && META.imageWidths[base];
    return (t && t.length) ? t : WIDTHS_BY_DIR[dir];
  }
  /* Ancho de reserva: el primero que llegue a 768, y si ninguno llega, el mayor
     que haya. Siempre un fichero que existe. */
  function fallbackW(w) {
    for (var i = 0; i < w.length; i++) { if (w[i] >= 768) return w[i]; }
    return w[w.length - 1];
  }
  var SIZES = "(max-width:575px) 92vw, (max-width:991px) 46vw, (max-width:1399px) 31vw, 380px";
  function picture(rel, alt) {
    var m = /^(.*\/)([^\/]+)\.jpg$/.exec(rel || "");
    if (!m) return '<img src="' + esc(R + (rel || "")) + '" alt="' + esc(alt) + '" loading="lazy">';
    var dir = m[1], w = widthsFor(dir, m[2]);
    if (!w) return '<img src="' + esc(R + rel) + '" alt="' + esc(alt) + '" loading="lazy">';
    function set(ext) {
      return w.map(function (x) { return R + dir + "r/" + m[2] + "-" + x + "." + ext + " " + x + "w"; }).join(", ");
    }
    return "<picture>" +
      '<source type="image/avif" srcset="' + esc(set("avif")) + '" sizes="' + SIZES + '">' +
      '<source type="image/webp" srcset="' + esc(set("webp")) + '" sizes="' + SIZES + '">' +
      /* El <img> de reserva se toma de la propia escalera, no de un 768 fijo:
         si algun master no llegara a ese ancho, el fijo seria otro 404. */
      '<img src="' + esc(R + dir + "r/" + m[2] + "-" + fallbackW(w) + ".jpg") + '" alt="' + esc(alt) +
      '" loading="lazy" decoding="async"></picture>';
  }

  /* Nombre del asesor y de la oficina a partir del propio indice: los enlaces
     "ver la cartera completa" de los perfiles llegan con ?ag= u ?og=. */
  function agLabel(slug) {
    var m = (DATA && DATA.items || []).filter(function (x) { return x.ag === slug; })[0];
    return (m && m.agName) || slug;
  }
  function ogLabel(slug) {
    var m = (DATA && DATA.items || []).filter(function (x) { return x.og === slug; })[0];
    return (m && m.ogName) || slug;
  }

  /* Antiguedad del anuncio: "publicado hace 12 dias" dice mas del mercado que
     una fecha. Por encima de sesenta dias se cuenta en meses. */
  function listedAgo(iso) {
    if (!iso) return "";
    var d = Math.floor((Date.now() - new Date(iso).getTime()) / 86400000);
    if (isNaN(d) || d < 0) return "";
    if (d === 0) return t("listedToday");
    if (d < 60) return t("listedD").replace("%d", nf(d));
    return t("listedM").replace("%d", nf(Math.round(d / 30)));
  }

  /* Nombre legible de la tipologia; el chip mostraba el slug en crudo. */
  var TYN = null;
  function typeLabel(slug) {
    if (!TYN) {
      TYN = {};
      ((DATA && DATA.items) || []).forEach(function (x) {
        if (x.typeName) TYN[x.type] = x.typeName[L] || x.typeName.en;
      });
    }
    return TYN[slug] || slug;
  }

  /* Nombre del pais en el idioma de la pagina. El de la ciudad no se traduce. */
  var CCN = null;
  function ccName(cc) {
    if (!CCN) {
      CCN = {};
      ((LOCS && LOCS.countries) || []).forEach(function (c) {
        CCN[c.code] = c.name[L] || c.name.en;
      });
    }
    return CCN[cc] || cc;
  }

  /* ---------------------------------------------------------------- tarjeta */
  function card(x) {
    var title = x.t[L] || x.t.en;
    var typeName = (x.typeName && (x.typeName[L] || x.typeName.en)) || x.type;
    var price = x.poa ? t("poa")
      : money(x.p, x.cur) + (x.off === "rent" ? " " + t("perYear") : "");
    var specs = [];
    if (x.bd) specs.push(nf(x.bd) + " " + t("beds"));
    if (x.ba) specs.push(nf(x.ba) + " " + t("baths"));
    if (x.area) specs.push(nf(x.area) + " " + t("sqmL"));
    else if (x.ha) specs.push(nf(x.ha) + " " + t("haL"));
    if (x.keys) specs.push(nf(x.keys) + " " + t("keysL"));
    var fav = Store.favorites().indexOf(x.id) >= 0;
    var href = PR + "property-details.html?id=" + encodeURIComponent(x.id);

    /* Distintivos de confianza arriba a la izquierda; el corazon, arriba a la
       derecha y sobre la foto, que es donde la mano lo busca. */
    var flags = "";
    if (x.ver) flags += '<span class="xr_verified_badge">' +
      '<i class="fa-solid fa-circle-check" aria-hidden="true"></i> ' + esc(t("verifiedB")) + "</span>";
    if (x.promo && x.promo !== "none")
      flags += '<span class="xr_promo_badge is-' + esc(x.promo) + '">' + esc(t(x.promo)) + "</span>";
    if (x.drop) flags += '<span class="xr_drop_badge"><i class="fa-solid fa-arrow-down" ' +
      'aria-hidden="true"></i> ' + nf(x.drop) + "% " + esc(t("dropL")) + "</span>";

    /* Lo que trae el anuncio, abajo sobre la foto: numero de fotos, plano y
       recorrido. Son las tres senales que deciden entre dos anuncios iguales. */
    var kit = '<span class="xr_kit_item"><i class="fa-solid fa-camera" aria-hidden="true"></i> ' +
      nf(x.nph || 1) + "</span>";
    if (x.plan) kit += '<span class="xr_kit_item" title="' + esc(t("planL")) +
      '"><i class="fa-solid fa-ruler-combined" aria-hidden="true"></i></span>';
    if (x.tour) kit += '<span class="xr_kit_item" title="' + esc(t("tourL")) +
      '"><i class="fa-solid fa-street-view" aria-hidden="true"></i></span>';

    var tel = x.tel ? '<a class="xr_mp_contact" href="tel:' +
      esc(String(x.tel).replace(/[^+\d]/g, "")) + '" rel="nofollow">' +
      '<i class="fa-solid fa-phone" aria-hidden="true"></i> ' + esc(t("call")) + "</a>" : "";
    var wa = x.wa ? '<a class="xr_mp_contact is-wa" target="_blank" rel="noopener nofollow" ' +
      'href="https://wa.me/' + esc(String(x.wa).replace(/[^\d]/g, "")) +
      "?text=" + encodeURIComponent(title + " — " + location.origin + href) + '">' +
      '<i class="fa-brands fa-whatsapp" aria-hidden="true"></i> WhatsApp</a>' : "";

    var ago = listedAgo(x.pub);

    return '<article class="xr_mp_card" data-id="' + esc(x.id) + '">' +
      '<div class="xr_mp_media">' +
        '<a href="' + esc(href) + '" aria-label="' + esc(title) + '">' +
          picture(x.img, title) + "</a>" +
        '<span class="xr_mp_price">' + esc(price) + "</span>" +
        '<span class="xr_card_badges">' + flags + "</span>" +
        '<span class="xr_mp_kit">' + kit + "</span>" +
        '<button type="button" class="xr_mp_fav' + (fav ? " is-on" : "") +
          '" data-fav="' + esc(x.id) + '" aria-pressed="' + (fav ? "true" : "false") +
          '" aria-label="' + esc(t("saveA")) + '"><i class="fa-solid fa-heart"></i></button>' +
        (x.demo ? '<span class="xr_demo_tag">' + esc(t("demo")) + "</span>" : "") +
      "</div>" +
      '<div class="xr_mp_body">' +
        '<p class="xr_mp_type">' + esc(typeName) + "</p>" +
        '<h3 class="xr_mp_title"><a href="' + esc(href) + '">' + esc(title) + "</a></h3>" +
        '<p class="xr_mp_loc">' + esc([x.city, ccName(x.cc)].filter(Boolean).join(", ")) + "</p>" +
        (specs.length ? '<ul class="xr_mp_specs">' +
          specs.map(function (v) { return "<li><bdi>" + esc(v) + "</bdi></li>"; }).join("") + "</ul>" : "") +
        '<div class="xr_mp_foot">' +
          '<span class="xr_mp_agent">' + esc(x.ogName || "") +
            (ago ? '<em>' + esc(ago) + "</em>" : "") + "</span>" +
          (tel || wa ? '<span class="xr_mp_contacts">' + tel + wa + "</span>" : "") +
        "</div>" +
      "</div>" +
    "</article>";
  }

  /* ---------------------------------------------------------------- facetas */
  function facets(list) {
    var byType = {}, byCC = {}, byCity = {};
    list.forEach(function (x) {
      byType[x.type] = (byType[x.type] || 0) + 1;
      byCC[x.cc] = (byCC[x.cc] || 0) + 1;
      if (x.city) byCity[x.city] = (byCity[x.city] || 0) + 1;
    });
    return { type: byType, cc: byCC, city: byCity };
  }

  /* ---------------------------------------------------------------- mapa
     Puerto MapProvider: la lógica no depende del SDK. Hoy Leaflet + OSM; el
     adaptador de Mapbox o Google entra sin tocar nada de lo de arriba. */
  var MapProvider = (function () {
    var map = null, layer = null, ready = false;
    /* Leaflet va servido desde el propio dominio: el mapa no depende de que
       una CDN de terceros este disponible, y el sitio sigue teniendo una sola
       superficie de red. Se carga solo cuando se pide una vista con mapa. */
    var loading = false, waiters = [];
    function load(cb) {
      if (window.L && window.L.map) return cb();
      waiters.push(cb);
      if (loading) return;
      loading = true;
      var css = document.createElement("link");
      css.rel = "stylesheet";
      css.href = R + "assets/vendor/leaflet/leaflet.css";
      document.head.appendChild(css);
      var s = document.createElement("script");
      s.src = R + "assets/vendor/leaflet/leaflet.js";
      s.onload = function () {
        if (window.L && window.L.Icon && window.L.Icon.Default) {
          window.L.Icon.Default.imagePath = R + "assets/vendor/leaflet/images/";
        }
        var w = waiters; waiters = []; w.forEach(function (f) { f(); });
      };
      s.onerror = function () {
        var w = waiters; waiters = [];
        w.forEach(function (f) { f(new Error("map provider unavailable")); });
      };
      document.head.appendChild(s);
    }
    return {
      render: function (el, items, onMove) {
        load(function (err) {
          if (err || !window.L) {
            el.innerHTML = '<div class="xr_mp_map_fallback">' + esc(t("error")) + "</div>";
            return;
          }
          if (!map) {
            map = window.L.map(el, { scrollWheelZoom: false }).setView([20, 10], 2);
            window.L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
              { maxZoom: 18, attribution: "© OpenStreetMap" }).addTo(map);
            map.on("moveend", function () { if (onMove) onMove(map.getBounds()); });
            ready = true;
          }
          if (layer) map.removeLayer(layer);
          layer = window.L.layerGroup().addTo(map);
          var pts = [];
          items.forEach(function (x) {
            if (!x.lat || !x.lon) return;
            pts.push([x.lat, x.lon]);
            var price = x.poa ? t("poa") : money(x.p, x.cur);
            var mk = window.L.marker([x.lat, x.lon]).addTo(layer);
            mk.bindPopup('<a href="' + esc(PR + "property-details.html?id=" + encodeURIComponent(x.id)) +
              '"><strong>' + esc(x.t[L] || x.t.en) + "</strong></a><br>" + esc(price));
          });
          if (pts.length) {
            try { map.fitBounds(pts, { padding: [30, 30], maxZoom: 12 }); } catch (e) {}
          }
          setTimeout(function () { if (map) map.invalidateSize(); }, 60);
        });
      },
      isReady: function () { return ready; }
    };
  })();

  /* ---------------------------------------------------------------- render */
  function shell() {
    return '' +
      '<div class="xr_mp_bar">' +
        '<div class="xr_mp_bar_left">' +
          '<div class="xr_mp_seg" data-seg="offering">' +
            '<button type="button" data-v="sale">' + esc(t("sale")) + "</button>" +
            '<button type="button" data-v="rent">' + esc(t("rent")) + "</button>" +
          "</div>" +
          '<input type="search" class="xr_mp_q" name="q" placeholder="' + esc(t("qPlace")) + '">' +
          '<select class="xr_mp_sel" data-k="cc"></select>' +
          '<select class="xr_mp_sel" data-k="type"></select>' +
          '<div class="xr_mp_seg" data-seg="completion">' +
            '<button type="button" data-c="">' + esc(t("anyState")) + "</button>" +
            '<button type="button" data-c="ready">' + esc(t("ready")) + "</button>" +
            '<button type="button" data-c="off_plan">' + esc(t("offplan")) + "</button>" +
          "</div>" +
          '<button type="button" class="xr_mp_more">' + esc(t("filters")) +
            '<b class="xr_mp_more_n"></b></button>' +
        "</div>" +
        '<div class="xr_mp_bar_right">' +
          '<div class="xr_mp_seg" data-seg="view">' +
            '<button type="button" data-v="list">' + esc(t("list")) + "</button>" +
            '<button type="button" data-v="split">' + esc(t("split")) + "</button>" +
            '<button type="button" data-v="map">' + esc(t("map")) + "</button>" +
          "</div>" +
        "</div>" +
      "</div>" +
      '<div class="xr_mp_types" role="group"></div>' +
      '<div class="xr_mp_panel" hidden data-lenis-prevent>' +
        '<div class="xr_mp_panel_head">' +
          '<h4>' + esc(t("filters")) + "</h4>" +
          '<button type="button" class="xr_mp_close" aria-label="' + esc(t("closeF")) +
            '">&times;</button>' +
        "</div>" +
        '<div class="xr_mp_panel_grid">' +
          '<label>' + esc(t("beds")) + '<span class="xr_mp_range">' +
            '<input type="number" min="0" max="20" data-k="bedsMin" placeholder="' + esc(t("min")) + '">' +
            '<input type="number" min="0" max="20" data-k="bedsMax" placeholder="' + esc(t("max")) + '"></span></label>' +
          '<label>' + esc(t("baths")) + '<span class="xr_mp_range">' +
            '<input type="number" min="0" max="20" data-k="bathsMin" placeholder="' + esc(t("min")) + '"></span></label>' +
          '<label>' + esc(t("price")) + '<span class="xr_mp_range">' +
            '<input type="number" min="0" step="100000" data-k="priceMin" placeholder="' + esc(t("min")) + '">' +
            '<input type="number" min="0" step="100000" data-k="priceMax" placeholder="' + esc(t("max")) + '"></span></label>' +
          '<label>' + esc(t("area")) + '<span class="xr_mp_range">' +
            '<input type="number" min="0" data-k="areaMin" placeholder="' + esc(t("min")) + '">' +
            '<input type="number" min="0" data-k="areaMax" placeholder="' + esc(t("max")) + '"></span></label>' +
          '<label>' + esc(t("completion")) +
            '<select data-k="completion"><option value="">—</option>' +
            '<option value="ready">' + esc(t("ready")) + "</option>" +
            '<option value="off_plan">' + esc(t("offplan")) + "</option></select></label>" +
          '<label>' + esc(t("ppsqm")) + '<span class="xr_mp_range">' +
            '<input type="number" min="0" step="500" data-k="ppsqmMin" placeholder="' + esc(t("min")) + '">' +
            '<input type="number" min="0" step="500" data-k="ppsqmMax" placeholder="' + esc(t("max")) + '"></span></label>' +
          '<label>' + esc(t("furnish")) +
            '<select data-k="furn"><option value="">' + esc(t("anyFurn")) + "</option>" +
            '<option value="furnished">' + esc(t("furnished")) + "</option>" +
            '<option value="unfurnished">' + esc(t("unfurnished")) + "</option>" +
            '<option value="partly_furnished">' + esc(t("partly_furnished")) + "</option></select></label>" +
          '<label>' + esc(t("kw")) +
            '<input type="text" data-k="kw" placeholder="' + esc(t("kwPlace")) + '"></label>' +
          '<label class="xr_mp_check"><input type="checkbox" data-k="verified"> ' + esc(t("verified")) + "</label>" +
        "</div>" +
        '<div class="xr_mp_extras"><p>' + esc(t("extras")) + "</p>" +
          '<label class="xr_mp_amchip"><input type="checkbox" data-k="plan"> ' + esc(t("hasPlan")) + "</label>" +
          '<label class="xr_mp_amchip"><input type="checkbox" data-k="tour"> ' + esc(t("hasTour")) + "</label>" +
          '<label class="xr_mp_amchip"><input type="checkbox" data-k="drop"> ' + esc(t("hasDrop")) + "</label>" +
        "</div>" +
        '<div class="xr_mp_amen"></div>' +
        '<div class="xr_mp_panel_foot">' +
          '<button type="button" class="xr_mp_reset">' + esc(t("reset")) + "</button>" +
          '<button type="button" class="xr_mp_apply"></button>' +
        "</div>" +
      "</div>" +
      '<div class="xr_mp_head">' +
        '<p class="xr_mp_count"></p>' +
        '<div class="xr_mp_head_right">' +
          '<button type="button" class="xr_mp_alert" aria-label="' + esc(t("createAlert")) +
            '" title="' + esc(t("createAlert")) + '"><i class="fa-regular fa-bell"></i></button>' +
          '<button type="button" class="xr_mp_save">' + esc(t("save")) + "</button>" +
          '<select class="xr_mp_sort">' +
            '<option value="recommended">' + esc(t("recommended")) + "</option>" +
            '<option value="newest">' + esc(t("newest")) + "</option>" +
            '<option value="price-asc">' + esc(t("priceAsc")) + "</option>" +
            '<option value="price-desc">' + esc(t("priceDesc")) + "</option>" +
            '<option value="area-desc">' + esc(t("areaDesc")) + "</option>" +
            '<option value="ppa-asc">' + esc(t("ppaAsc")) + "</option>" +
          "</select>" +
        "</div>" +
      "</div>" +
      '<p class="xr_mp_chips"></p>' +
      '<div class="xr_mp_stage">' +
        '<div class="xr_mp_list"></div>' +
        '<div class="xr_mp_map" hidden></div>' +
      "</div>" +
      '<nav class="xr_mp_pager" aria-label="pagination"></nav>' +
      '<div class="xr_mp_explore"></div>' +
      '<p class="xr_mp_sim">' + esc(t("simNote")) + "</p>";
  }

  function fillSelects(all) {
    var f = facets(all);
    var ccSel = HOST.querySelector('.xr_mp_sel[data-k="cc"]');
    var tySel = HOST.querySelector('.xr_mp_sel[data-k="type"]');
    var ccs = Object.keys(f.cc).sort(function (a, b) { return f.cc[b] - f.cc[a]; });
    var name = {};
    (LOCS && LOCS.countries || []).forEach(function (c) { name[c.code] = c.name[L] || c.name.en; });
    ccSel.innerHTML = '<option value="">' + esc(t("anyLoc")) + "</option>" +
      ccs.map(function (c) {
        return '<option value="' + esc(c) + '">' + esc(name[c] || c) + " (" + f.cc[c] + ")</option>";
      }).join("");
    var tn = {};
    all.forEach(function (x) { tn[x.type] = (x.typeName && (x.typeName[L] || x.typeName.en)) || x.type; });
    var tys = Object.keys(f.type).sort(function (a, b) { return (tn[a] || "").localeCompare(tn[b] || ""); });
    tySel.innerHTML = '<option value="">' + esc(t("anyType")) + "</option>" +
      tys.map(function (k) {
        return '<option value="' + esc(k) + '">' + esc(tn[k]) + " (" + f.type[k] + ")</option>";
      }).join("");
    var amBox = HOST.querySelector(".xr_mp_amen");
    if (META && META.amenities) {
      amBox.innerHTML = "<p>" + esc(t("amenities")) + "</p>" + META.amenities.slice(0, 24).map(function (a) {
        return '<label class="xr_mp_amchip"><input type="checkbox" data-am="' + esc(a.slug) + '"> ' +
          esc(a["name_" + L] || a.name_en) + "</label>";
      }).join("");
    }
  }

  function syncControls() {
    HOST.querySelectorAll('[data-seg="offering"] button').forEach(function (b) {
      b.classList.toggle("is-on", b.getAttribute("data-v") === STATE.offering);
    });
    HOST.querySelectorAll('[data-seg="view"] button').forEach(function (b) {
      b.classList.toggle("is-on", b.getAttribute("data-v") === STATE.view);
    });
    HOST.querySelector(".xr_mp_q").value = STATE.q;
    HOST.querySelector(".xr_mp_sort").value = STATE.sort;
    var cc = HOST.querySelector('.xr_mp_sel[data-k="cc"]');
    if (cc) cc.value = STATE.cc[0] || "";
    var ty = HOST.querySelector('.xr_mp_sel[data-k="type"]');
    if (ty) ty.value = STATE.type[0] || "";
    NUM_KEYS.forEach(function (k) {
      var el = HOST.querySelector('[data-k="' + k + '"]');
      if (el) el.value = STATE[k] == null ? "" : STATE[k];
    });
    var comp = HOST.querySelector('[data-k="completion"]');
    if (comp) comp.value = STATE.completion || "";
    var ver = HOST.querySelector('[data-k="verified"]');
    if (ver) ver.checked = !!STATE.verified;
    ["furn", "kw"].forEach(function (k) {
      var el = HOST.querySelector('[data-k="' + k + '"]');
      if (el) el.value = STATE[k] || "";
    });
    ["plan", "tour", "drop"].forEach(function (k) {
      var el = HOST.querySelector('[data-k="' + k + '"]');
      if (el) el.checked = !!STATE[k];
    });
    HOST.querySelectorAll('[data-seg="completion"] button').forEach(function (b) {
      b.classList.toggle("is-on", (b.getAttribute("data-c") || "") === (STATE.completion || ""));
    });
    HOST.querySelectorAll("[data-am]").forEach(function (el) {
      el.checked = STATE.am.indexOf(el.getAttribute("data-am")) >= 0;
    });
  }

  function chips() {
    var out = [];
    function chip(label, fn) {
      out.push('<button type="button" class="xr_mp_chip" data-chip="' + esc(label) + '">' +
        esc(label) + " ✕</button>");
      CHIPS[label] = fn;
    }
    CHIPS = {};
    if (STATE.q) chip('"' + STATE.q + '"', function () { STATE.q = ""; });
    STATE.cc.forEach(function (c) { chip(ccName(c), function () { STATE.cc = STATE.cc.filter(function (x) { return x !== c; }); }); });
    STATE.city.forEach(function (c) { chip(c, function () { STATE.city = STATE.city.filter(function (x) { return x !== c; }); }); });
    STATE.type.forEach(function (c) { chip(typeLabel(c), function () { STATE.type = STATE.type.filter(function (x) { return x !== c; }); }); });
    STATE.am.forEach(function (c) { chip(c, function () { STATE.am = STATE.am.filter(function (x) { return x !== c; }); }); });
    if (STATE.priceMin != null) chip(t("price") + " ≥ " + nf(STATE.priceMin), function () { STATE.priceMin = null; });
    if (STATE.priceMax != null) chip(t("price") + " ≤ " + nf(STATE.priceMax), function () { STATE.priceMax = null; });
    if (STATE.bedsMin != null) chip(t("beds") + " ≥ " + STATE.bedsMin, function () { STATE.bedsMin = null; });
    if (STATE.ag) chip(agLabel(STATE.ag), function () { STATE.ag = ""; });
    if (STATE.og) chip(ogLabel(STATE.og), function () { STATE.og = ""; });
    if (STATE.verified) chip(t("verified"), function () { STATE.verified = false; });
    if (STATE.completion) chip(t(STATE.completion === "off_plan" ? "offplan" : "ready"),
                              function () { STATE.completion = ""; });
    if (STATE.furn) chip(t(STATE.furn), function () { STATE.furn = ""; });
    if (STATE.kw) chip(t("kw") + ": " + STATE.kw, function () { STATE.kw = ""; });
    if (STATE.plan) chip(t("hasPlan"), function () { STATE.plan = false; });
    if (STATE.tour) chip(t("hasTour"), function () { STATE.tour = false; });
    if (STATE.drop) chip(t("hasDrop"), function () { STATE.drop = false; });
    if (STATE.ppsqmMin != null) chip(t("ppsqm") + " ≥ " + nf(STATE.ppsqmMin),
                                     function () { STATE.ppsqmMin = null; });
    if (STATE.ppsqmMax != null) chip(t("ppsqm") + " ≤ " + nf(STATE.ppsqmMax),
                                     function () { STATE.ppsqmMax = null; });
    HOST.querySelector(".xr_mp_chips").innerHTML = out.join("");
  }
  var CHIPS = {};

  /* MODO ESCAPARATE
     -----------------------------------------------------------------
     Una pagina de pilar no necesita la aplicacion entera: necesita enseñar que
     hay obra y llevar al buscador. Antes no enseñaba nada —la portada de
     Propiedades Privadas decia "0 de 0" y no pintaba una sola ficha mientras el
     inventario tenia treinta villas, veintidos mansiones y once castillos— y
     los enlaces del menu recargaban esa misma pagina vacia.

     Esto no es un segundo buscador: usa el mismo query(), el mismo orden y la
     misma ficha que el marketplace. Solo cambia cuanto enseña y que en vez de
     paginar, remata con un enlace a la busqueda completa. Una sola logica. */
  function paintPreview() {
    var res = sortItems(query(STATE, DATA.items), STATE.sort);
    var href = HOST.getAttribute("data-href") || "";
    if (!res.length) {
      HOST.innerHTML = '<div class="xr_mp_empty"><p>' + esc(t("prevEmpty")) + "</p></div>";
      return;
    }
    HOST.innerHTML =
      '<div class="xr_mp_list xr_mp_preview">' +
        res.slice(0, PREVIEW).map(card).join("") +
      "</div>" +
      (href ? '<p class="xr_mp_preview_more"><a class="xr_link" href="' + esc(href) + '">' +
                esc(t("seeAll").replace("{n}", nf(res.length))) +
                '<i class="fa-solid fa-angle-right"></i></a></p>' : "");
  }

  function paint() {
    var all = DATA.items;
    var res = sortItems(query(STATE, all), STATE.sort);
    var pages = Math.max(1, Math.ceil(res.length / PAGE_SIZE));
    if (STATE.page > pages) STATE.page = pages;
    var slice = res.slice((STATE.page - 1) * PAGE_SIZE, STATE.page * PAGE_SIZE);

    HOST.querySelector(".xr_mp_count").innerHTML =
      "<strong>" + nf(res.length) + "</strong> " + esc(t("results"));

    var list = HOST.querySelector(".xr_mp_list");
    if (!res.length) {
      list.innerHTML = '<div class="xr_mp_empty"><p>' + esc(t("empty")) + "</p><p>" +
        esc(t("emptyHint")) + '</p><button type="button" class="xr_mp_reset">' +
        esc(t("reset")) + "</button></div>";
    } else {
      list.innerHTML = slice.map(card).join("");
    }

    var pager = HOST.querySelector(".xr_mp_pager");
    if (pages > 1) {
      var btns = '<button type="button" data-page="' + (STATE.page - 1) + '"' +
        (STATE.page === 1 ? " disabled" : "") + ">" + esc(t("prev")) + "</button>";
      var from = Math.max(1, STATE.page - 2), to = Math.min(pages, from + 4);
      for (var i = from; i <= to; i++) {
        btns += '<button type="button" data-page="' + i + '"' +
          (i === STATE.page ? ' class="is-on"' : "") + ">" + i + "</button>";
      }
      btns += '<button type="button" data-page="' + (STATE.page + 1) + '"' +
        (STATE.page === pages ? " disabled" : "") + ">" + esc(t("next")) + "</button>";
      pager.innerHTML = btns;
    } else pager.innerHTML = "";

    var stage = HOST.querySelector(".xr_mp_stage");
    var mapEl = HOST.querySelector(".xr_mp_map");
    stage.setAttribute("data-view", STATE.view);
    mapEl.hidden = STATE.view === "list";
    list.hidden = STATE.view === "map";
    if (STATE.view !== "list") MapProvider.render(mapEl, res.slice(0, 300));

    paintTypes(all);
    paintExplore(all);
    chips();
    syncControls();
    paintApply(res.length);
    var moreN = HOST.querySelector(".xr_mp_more_n");
    if (moreN) {
      var n = activeFilters();
      moreN.textContent = n ? nf(n) : "";
    }
  }

  /* Fila de tipologias con su recuento, como la de un portal: se ve de un
     vistazo donde esta el inventario y se filtra con un solo gesto. Los
     recuentos respetan todo lo demas que haya puesto menos la propia
     tipologia, que es como debe comportarse una faceta. */
  function paintTypes(all) {
    var box = HOST.querySelector(".xr_mp_types");
    if (!box) return;
    var sinType = {};
    Object.keys(STATE).forEach(function (k) { sinType[k] = STATE[k]; });
    sinType.type = [];
    var base = query(sinType, all);
    var n = {}, nm = {};
    base.forEach(function (x) {
      n[x.type] = (n[x.type] || 0) + 1;
      nm[x.type] = (x.typeName && (x.typeName[L] || x.typeName.en)) || x.type;
    });
    var keys = Object.keys(n).sort(function (a, b) { return n[b] - n[a]; }).slice(0, 12);
    box.innerHTML =
      '<button type="button" class="xr_mp_type' + (STATE.type.length ? "" : " is-on") +
        '" data-type="">' + esc(t("allTypes")) +
        '<b>' + nf(base.length) + "</b></button>" +
      keys.map(function (k) {
        return '<button type="button" class="xr_mp_type' +
          (STATE.type.indexOf(k) >= 0 ? " is-on" : "") + '" data-type="' + esc(k) + '">' +
          esc(nm[k]) + "<b>" + nf(n[k]) + "</b></button>";
      }).join("");
  }

  /* Enlaces de continuación bajo los resultados. No son relleno: son las
     únicas rutas de este buscador que un indexador puede seguir sin ejecutar
     JavaScript, y son las que un visitante usa cuando su búsqueda no cuajó. */
  function paintExplore(all) {
    var box = HOST.querySelector(".xr_mp_explore");
    if (!box) return;
    var route = location.pathname;
    function group(title, items) {
      if (!items.length) return "";
      return '<div class="xr_mp_exgroup"><h4>' + esc(title) + "</h4><p>" +
        items.map(function (x) {
          return '<a href="' + esc(x.href) + '">' + esc(x.label) +
            "<span>" + nf(x.n) + "</span></a>";
        }).join("") + "</p></div>";
    }
    function top(keyf, labelf, hreff, k) {
      var n = {}, lb = {}, hr = {};
      all.forEach(function (x) {
        var key = keyf(x);
        if (!key) return;
        n[key] = (n[key] || 0) + 1;
        lb[key] = labelf(x);
        hr[key] = hreff(x);
      });
      return Object.keys(n).sort(function (a, b) { return n[b] - n[a]; })
        .slice(0, k).map(function (key) {
          return { label: lb[key], href: hr[key], n: n[key] };
        });
    }
    box.innerHTML = '<h3 class="xr_mp_exh">' + esc(t("exploreT")) + "</h3>" +
      '<div class="xr_mp_exgrid">' +
      group(t("exploreByCity"), top(
        function (x) { return x.city && x.cc ? x.cc + "|" + x.city : null; },
        function (x) { return x.city; },
        function (x) { return route + "?cc=" + encodeURIComponent(x.cc) +
                              "&city=" + encodeURIComponent(x.city); }, 8)) +
      group(t("exploreByCountry"), top(
        function (x) { return x.cc; },
        function (x) { return ccName(x.cc); },
        function (x) { return route + "?cc=" + encodeURIComponent(x.cc); }, 8)) +
      group(t("exploreByType"), top(
        function (x) { return x.type; },
        function (x) { return (x.typeName && (x.typeName[L] || x.typeName.en)) || x.type; },
        function (x) { return route + "?type=" + encodeURIComponent(x.type); }, 8)) +
      "</div>";
  }

  /* Cuantos filtros hay puestos: el boton "Filtros" lo lleva encima, para que
     se vea que hay algo activo sin tener que abrir el panel. */
  function activeFilters() {
    var n = 0;
    LIST_KEYS.forEach(function (k) { if (STATE[k].length) n++; });
    NUM_KEYS.forEach(function (k) { if (k !== "page" && STATE[k] != null) n++; });
    ["furn", "kw", "completion"].forEach(function (k) { if (STATE[k]) n++; });
    ["verified", "plan", "tour", "drop"].forEach(function (k) { if (STATE[k]) n++; });
    return n;
  }

  /* El boton del panel lleva el recuento en vivo: se sabe cuantos activos
     quedan antes de cerrar, que es justo la duda que hace abrir y cerrar tres
     veces seguidas. */
  function paintApply(n) {
    var b = HOST.querySelector(".xr_mp_apply");
    if (!b) return;
    b.textContent = n ? t("showN").replace("%s", nf(n)) : t("showNone");
    b.disabled = !n;
  }

  /* Nombre legible de la busqueda guardada: la ruta y los filtros puestos,
     no el <title> de la pagina, que es siempre el mismo. */
  function niceName() {
    var bits = [];
    if (STATE.offering) bits.push(t(STATE.offering));
    if (STATE.category) bits.push(STATE.category);
    STATE.cc.forEach(function (c) { bits.push(ccName(c)); });
    STATE.city.forEach(function (c) { bits.push(c); });
    STATE.type.forEach(function (c) { bits.push(typeLabel(c)); });
    if (STATE.priceMin != null) bits.push("≥ " + nf(STATE.priceMin));
    if (STATE.priceMax != null) bits.push("≤ " + nf(STATE.priceMax));
    if (STATE.q) bits.push('"' + STATE.q + '"');
    return bits.length ? bits.join(" · ") : t("results");
  }

  /* El panel se abre como cajón lateral. Se bloquea el desplazamiento del
     fondo —si no, mover la rueda dentro del cajón arrastra la página de
     detrás— y se pone un velo que cierra al pulsarlo. */
  var SCRIM = null;
  function lenisStop() {
    try { if (window.__xaruLenis) window.__xaruLenis.stop(); } catch (e) {}
  }
  function lenisStart() {
    try { if (window.__xaruLenis) window.__xaruLenis.start(); } catch (e) {}
  }

  function openPanel() {
    var pn = HOST.querySelector(".xr_mp_panel");
    pn.hidden = false;
    document.body.classList.add("xr_drawer_open");
    lenisStop();
    if (!SCRIM) {
      SCRIM = document.createElement("div");
      SCRIM.className = "xr_mp_scrim";
      SCRIM.addEventListener("click", closePanel);
      document.body.appendChild(SCRIM);
    }
    SCRIM.classList.add("is-on");
    var f = pn.querySelector("input, select, button");
    if (f) { try { f.focus({ preventScroll: true }); } catch (e) {} }
  }
  function closePanel() {
    var pn = HOST.querySelector(".xr_mp_panel");
    if (pn) pn.hidden = true;
    document.body.classList.remove("xr_drawer_open");
    lenisStart();
    if (SCRIM) SCRIM.classList.remove("is-on");
    var m = HOST.querySelector(".xr_mp_more");
    if (m) { try { m.focus({ preventScroll: true }); } catch (e) {} }
  }

  function apply(push) {
    STATE.page = STATE.page || 1;
    writeURL(!push);
    paint();
  }

  /* ---------------------------------------------------------------- eventos */
  function bind() {
    HOST.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (!b) return;
      if (b.hasAttribute("data-v")) {
        var seg = b.closest("[data-seg]").getAttribute("data-seg");
        var v = b.getAttribute("data-v");
        if (seg === "offering") STATE.offering = STATE.offering === v ? "" : v;
        else STATE.view = v;
        STATE.page = 1; apply(true); return;
      }
      if (b.classList.contains("xr_mp_more")) {
        var pn = HOST.querySelector(".xr_mp_panel");
        if (pn.hidden) openPanel(); else closePanel();
        return;
      }
      if (b.classList.contains("xr_mp_apply")) {
        closePanel();
        HOST.querySelector(".xr_mp_head").scrollIntoView({ behavior: "smooth", block: "start" });
        return;
      }
      if (b.hasAttribute("data-type")) {
        var ty = b.getAttribute("data-type");
        STATE.type = ty ? [ty] : [];
        STATE.page = 1; apply(true); return;
      }
      if (b.classList.contains("xr_mp_close")) {
        closePanel(); return;
      }
      if (b.classList.contains("xr_mp_alert")) {
        // Una alerta es una busqueda guardada que ademas avisa. Se crea sobre
        // la busqueda actual y se gestiona desde el panel del comprador.
        Store.saveSearch(niceName(), location.search || "", location.pathname,
                         { offering: STATE.offering, category: STATE.category }, true);
        b.classList.add("is-on");
        b.setAttribute("title", t("alertOn"));
        b.innerHTML = '<i class="fa-solid fa-bell"></i>';
        return;
      }
      if (b.hasAttribute("data-c")) {
        STATE.completion = b.getAttribute("data-c") || "";
        STATE.page = 1; apply(true); return;
      }
      if (b.classList.contains("xr_mp_reset")) {
        STATE = readURL();
        LIST_KEYS.forEach(function (k) { STATE[k] = []; });
        NUM_KEYS.forEach(function (k) { STATE[k] = null; });
        STATE.q = ""; STATE.verified = false; STATE.completion = "";
        STATE.furn = ""; STATE.kw = "";
        STATE.plan = false; STATE.tour = false; STATE.drop = false;
        STATE.page = 1;
        apply(true); return;
      }
      if (b.hasAttribute("data-page")) {
        STATE.page = parseInt(b.getAttribute("data-page"), 10) || 1;
        apply(true);
        HOST.scrollIntoView({ behavior: "smooth", block: "start" });
        return;
      }
      if (b.hasAttribute("data-chip")) {
        var fn = CHIPS[b.getAttribute("data-chip")];
        if (fn) { fn(); STATE.page = 1; apply(true); }
        return;
      }
      if (b.hasAttribute("data-fav")) {
        var on = Store.toggleFavorite(b.getAttribute("data-fav"));
        b.classList.toggle("is-on", on);
        b.setAttribute("aria-pressed", on ? "true" : "false");
        return;
      }
      if (b.classList.contains("xr_mp_save")) {
        var ok = Store.saveSearch(niceName(), location.search || "",
                                  location.pathname,
                                  { offering: STATE.offering, category: STATE.category });
        b.textContent = ok ? t("saved") : t("saved");
        b.disabled = true;
        return;
      }
    });

    HOST.addEventListener("change", function (e) {
      var el = e.target;
      if (el.classList.contains("xr_mp_sort")) { STATE.sort = el.value; STATE.page = 1; return apply(true); }
      if (el.classList.contains("xr_mp_sel")) {
        var k = el.getAttribute("data-k");
        STATE[k] = el.value ? [el.value] : [];
        STATE.page = 1; return apply(true);
      }
      if (el.hasAttribute("data-am")) {
        var a = el.getAttribute("data-am");
        if (el.checked) STATE.am.push(a);
        else STATE.am = STATE.am.filter(function (x) { return x !== a; });
        STATE.page = 1; return apply(true);
      }
      var k2 = el.getAttribute("data-k");
      if (k2 === "verified" || k2 === "plan" || k2 === "tour" || k2 === "drop") {
        STATE[k2] = el.checked; STATE.page = 1; return apply(true);
      }
      if (k2 === "completion" || k2 === "furn") {
        STATE[k2] = el.value; STATE.page = 1; return apply(true);
      }
      if (k2 === "kw") { STATE.kw = el.value; STATE.page = 1; return apply(true); }
      if (k2 && NUM_KEYS.indexOf(k2) >= 0) {
        var v = parseFloat(el.value);
        STATE[k2] = isNaN(v) ? null : v;
        STATE.page = 1; return apply(true);
      }
    });

    var numTimer = null;
    HOST.addEventListener("input", function (e) {
      var el = e.target;
      var k = el.getAttribute && el.getAttribute("data-k");
      if (k === "kw") {
        clearTimeout(numTimer);
        numTimer = setTimeout(function () {
          if (STATE.kw === el.value) return;
          STATE.kw = el.value; STATE.page = 1; apply(false);
        }, 420);
        return;
      }
      if (!k || NUM_KEYS.indexOf(k) < 0) return;
      clearTimeout(numTimer);
      numTimer = setTimeout(function () {
        var v = parseFloat(el.value);
        var nv = isNaN(v) ? null : v;
        if (STATE[k] === nv) return;
        STATE[k] = nv; STATE.page = 1; apply(false);
      }, 420);
    });

    var qbox = HOST.querySelector(".xr_mp_q");
    var timer = null;
    qbox.addEventListener("input", function () {
      clearTimeout(timer);
      timer = setTimeout(function () { STATE.q = qbox.value; STATE.page = 1; apply(false); }, 260);
    });

    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape") return;
      var pn = HOST.querySelector(".xr_mp_panel");
      if (pn && !pn.hidden) closePanel();
    });

    window.addEventListener("popstate", function () { STATE = readURL(); paint(); });
  }

  /* ---------------------------------------------------------------- arranque */
  HOST.innerHTML = '<p class="xr_mp_loading">' + esc(t("loading")) + "</p>";

  Promise.all([
    fetch(R + API + "search-index.json").then(function (r) { if (!r.ok) throw 0; return r.json(); }),
    fetch(R + API + "meta.json").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }),
    fetch(R + API + "locations.json").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; })
  ]).then(function (out) {
    DATA = out[0]; META = out[1]; LOCS = out[2];
    if (PREVIEW) { STATE = readURL(); paintPreview(); return; }
    HOST.innerHTML = shell();
    STATE = readURL();
    fillSelects(DATA.items);
    bind();
    paint();
  }).catch(function (err) {
    if (window.console) console.warn("[xaru-marketplace]", err);
    HOST.innerHTML = '<div class="xr_mp_empty"><p>' + esc(t("error")) +
      '</p><button type="button" onclick="location.reload()">' + esc(t("retry")) + "</button></div>";
  });
})();
