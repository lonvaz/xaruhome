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
    demo:      {en:"Platform demo",es:"Muestra de plataforma",ar:"عرض تجريبي",zh:"平台演示"},
    verifiedB: {en:"Verified",es:"Verificado",ar:"موثّق",zh:"已核验"},
    fav:       {en:"Save",es:"Guardar",ar:"حفظ",zh:"收藏"},
    share:     {en:"Share",es:"Compartir",ar:"مشاركة",zh:"分享"},
    call:      {en:"Call",es:"Llamar",ar:"اتصال",zh:"致电"},
    email:     {en:"Email",es:"Email",ar:"بريد",zh:"邮件"},
    whatsapp:  {en:"WhatsApp",es:"WhatsApp",ar:"واتساب",zh:"WhatsApp"},
    page:      {en:"Page",es:"Página",ar:"صفحة",zh:"第"},
    prev:      {en:"Previous",es:"Anterior",ar:"السابق",zh:"上一页"},
    next:      {en:"Next",es:"Siguiente",ar:"التالي",zh:"下一页"},
    simNote:   {en:"Simulation mode — inventory is platform demo data and actions are stored on this device.",
                es:"Modo simulación — el inventario es de muestra y las acciones se guardan en este dispositivo.",
                ar:"وضع المحاكاة — المعروض بيانات تجريبية وتُحفظ الإجراءات على هذا الجهاز.",
                zh:"模拟模式——资产为平台演示数据，操作保存在本设备。"},
    searchHere:{en:"Search this area",es:"Buscar en esta zona",ar:"ابحث في هذه المنطقة",zh:"搜索此区域"},
    qPlace:    {en:"City, country, typology or reference",
                es:"Ciudad, país, tipología o referencia",
                ar:"مدينة أو دولة أو نوع أو مرجع",
                zh:"城市、国家、类型或编号"},
    keysL:     {en:"keys",es:"llaves",ar:"مفتاح",zh:"客房"},
    haL:       {en:"ha",es:"ha",ar:"هكتار",zh:"公顷"},
    sqmL:      {en:"m²",es:"m²",ar:"م²",zh:"㎡"}
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
    saveSearch: function (name, qs) {
      var s = this.savedSearches();
      if (s.some(function (x) { return x.qs === qs; })) return false;
      s.push({ name: name, qs: qs, at: new Date().toISOString() });
      this._write("xaru_saved_searches", s);
      return true;
    }
  };

  /* ---------------------------------------------------------------- estado */
  var DATA = null, META = null, LOCS = null;
  var STATE = {};

  var LIST_KEYS = ["type", "cc", "city", "am"];
  var NUM_KEYS = ["bedsMin", "bedsMax", "bathsMin", "priceMin", "priceMax", "areaMin", "areaMax", "page"];

  function readURL() {
    var p = new URLSearchParams(location.search);
    var s = {
      q: p.get("q") || "",
      offering: p.get("offering") || HOST.getAttribute("data-offering") || "",
      category: p.get("category") || HOST.getAttribute("data-category") || "",
      sort: p.get("sort") || "recommended",
      view: p.get("view") || HOST.getAttribute("data-view") || "list",
      verified: p.get("verified") === "1",
      completion: p.get("completion") || ""
    };
    LIST_KEYS.forEach(function (k) {
      s[k] = (p.get(k) || "").split(",").filter(Boolean);
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
      if (state.verified && !x.ver) return false;
      if (state.completion && x.comp !== state.completion) return false;
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
  var WIDTHS_BY_DIR = {
    "assets/img/xaru/catalog/": [480, 768, 1280, 1920, 2560],
    "assets/img/xaru/gen2/":    [768, 1280, 1920]
  };
  var SIZES = "(max-width:575px) 92vw, (max-width:991px) 46vw, (max-width:1399px) 31vw, 380px";
  function picture(rel, alt) {
    var m = /^(.*\/)([^\/]+)\.jpg$/.exec(rel || "");
    if (!m) return '<img src="' + esc(R + (rel || "")) + '" alt="' + esc(alt) + '" loading="lazy">';
    var dir = m[1], w = WIDTHS_BY_DIR[dir];
    if (!w) return '<img src="' + esc(R + rel) + '" alt="' + esc(alt) + '" loading="lazy">';
    function set(ext) {
      return w.map(function (x) { return R + dir + "r/" + m[2] + "-" + x + "." + ext + " " + x + "w"; }).join(", ");
    }
    return "<picture>" +
      '<source type="image/avif" srcset="' + esc(set("avif")) + '" sizes="' + SIZES + '">' +
      '<source type="image/webp" srcset="' + esc(set("webp")) + '" sizes="' + SIZES + '">' +
      '<img src="' + esc(R + dir + "r/" + m[2] + "-768.jpg") + '" alt="' + esc(alt) +
      '" loading="lazy" decoding="async"></picture>';
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
    var badges = "";
    if (x.promo && x.promo !== "none")
      badges += '<span class="xr_promo_badge is-' + esc(x.promo) + '">' + esc(x.promo) + "</span>";
    if (x.ver) badges += '<span class="xr_verified_badge">' + esc(t("verifiedB")) + "</span>";
    if (x.demo) badges += '<span class="xr_demo_badge">' + esc(t("demo")) + "</span>";

    return '<article class="xr_mp_card" data-id="' + esc(x.id) + '">' +
      '<a class="xr_mp_media" href="' + esc(href) + '" aria-label="' + esc(title) + '">' +
        picture(x.img, title) +
        '<span class="xr_mp_price">' + esc(price) + "</span>" +
        '<span class="xr_card_badges">' + badges + "</span>" +
      "</a>" +
      '<div class="xr_mp_body">' +
        '<p class="xr_mp_type">' + esc(typeName) + "</p>" +
        '<h3 class="xr_mp_title"><a href="' + esc(href) + '">' + esc(title) + "</a></h3>" +
        '<p class="xr_mp_loc">' + esc([x.city, x.cc].filter(Boolean).join(", ")) + "</p>" +
        (specs.length ? '<ul class="xr_mp_specs">' +
          specs.map(function (s) { return "<li><bdi>" + esc(s) + "</bdi></li>"; }).join("") + "</ul>" : "") +
        '<div class="xr_mp_foot">' +
          '<span class="xr_mp_agent">' + esc(x.ogName || "") + "</span>" +
          '<button type="button" class="xr_mp_fav' + (fav ? " is-on" : "") +
          '" data-fav="' + esc(x.id) + '" aria-pressed="' + (fav ? "true" : "false") +
          '" aria-label="' + esc(t("fav")) + '"><i class="fa-solid fa-heart"></i></button>' +
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
          '<button type="button" class="xr_mp_more">' + esc(t("filters")) + "</button>" +
        "</div>" +
        '<div class="xr_mp_bar_right">' +
          '<div class="xr_mp_seg" data-seg="view">' +
            '<button type="button" data-v="list">' + esc(t("list")) + "</button>" +
            '<button type="button" data-v="split">' + esc(t("split")) + "</button>" +
            '<button type="button" data-v="map">' + esc(t("map")) + "</button>" +
          "</div>" +
        "</div>" +
      "</div>" +
      '<div class="xr_mp_panel" hidden>' +
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
          '<label class="xr_mp_check"><input type="checkbox" data-k="verified"> ' + esc(t("verified")) + "</label>" +
        "</div>" +
        '<div class="xr_mp_amen"></div>' +
        '<div class="xr_mp_panel_foot">' +
          '<button type="button" class="xr_mp_reset">' + esc(t("reset")) + "</button>" +
        "</div>" +
      "</div>" +
      '<div class="xr_mp_head">' +
        '<p class="xr_mp_count"></p>' +
        '<div class="xr_mp_head_right">' +
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
    STATE.cc.forEach(function (c) { chip(c, function () { STATE.cc = STATE.cc.filter(function (x) { return x !== c; }); }); });
    STATE.type.forEach(function (c) { chip(c, function () { STATE.type = STATE.type.filter(function (x) { return x !== c; }); }); });
    STATE.am.forEach(function (c) { chip(c, function () { STATE.am = STATE.am.filter(function (x) { return x !== c; }); }); });
    if (STATE.priceMin != null) chip(t("price") + " ≥ " + nf(STATE.priceMin), function () { STATE.priceMin = null; });
    if (STATE.priceMax != null) chip(t("price") + " ≤ " + nf(STATE.priceMax), function () { STATE.priceMax = null; });
    if (STATE.bedsMin != null) chip(t("beds") + " ≥ " + STATE.bedsMin, function () { STATE.bedsMin = null; });
    if (STATE.verified) chip(t("verified"), function () { STATE.verified = false; });
    if (STATE.completion) chip(STATE.completion, function () { STATE.completion = ""; });
    HOST.querySelector(".xr_mp_chips").innerHTML = out.join("");
  }
  var CHIPS = {};

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

    chips();
    syncControls();
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
        var p = HOST.querySelector(".xr_mp_panel");
        p.hidden = !p.hidden; return;
      }
      if (b.classList.contains("xr_mp_reset")) {
        STATE = readURL();
        LIST_KEYS.forEach(function (k) { STATE[k] = []; });
        NUM_KEYS.forEach(function (k) { STATE[k] = null; });
        STATE.q = ""; STATE.verified = false; STATE.completion = ""; STATE.page = 1;
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
        var ok = Store.saveSearch(document.title, location.search || "?");
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
      if (k2 === "verified") { STATE.verified = el.checked; STATE.page = 1; return apply(true); }
      if (k2 === "completion") { STATE.completion = el.value; STATE.page = 1; return apply(true); }
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
