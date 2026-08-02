/*
 * XARU HOME — ficha del activo (property-details.html?id=…)
 * =============================================================
 * POR QUE EXISTE
 * --------------
 * La plantilla traia una ficha de ejemplo: "Evergreen Estates", 70.000 dolares,
 * una direccion de Nueva York, una calculadora de hipoteca y un listado de
 * colegios cercanos. Todas las tarjetas del catalogo apuntaban ahi, asi que
 * quien pinchaba una propiedad de treinta millones aterrizaba en una vivienda
 * de setenta mil que no existe.
 *
 * DE DONDE SALEN LOS DATOS
 * ------------------------
 * De `/data/api/v1/listings/{publicId}.json`, la proyeccion que publica
 * `platform/export_api.py` desde la base de datos, con la forma que tendra la
 * respuesta de `GET /api/v1/listings/{id}`. El dia que exista el Listing
 * Service, `fetchListing()` pasa a ser esa llamada y no cambia nada mas.
 *
 * Para los identificadores heredados del catalogo antiguo se conserva la via
 * de los tres paquetes JSON: nada de lo que ya funcionaba deja de funcionar.
 *
 * LO QUE NO SE INVENTA
 * --------------------
 * Hipoteca, colegios cercanos, plano de planta y agenda de visitas se retiran
 * en lugar de rellenarse con cifras falsas. Una ficha con datos inventados es
 * peor que una ficha corta.
 */
(function () {
  "use strict";

  var ANCHOR = document.querySelector(".cs_property_details");
  if (!ANCHOR) return;
  var HOST = ANCHOR.parentElement || ANCHOR;

  var R = "/";
  var API = R + "data/api/v1/";
  var PACKS = ["private-real-estate", "commercial-hospitality", "land-developments"];

  function lang() {
    var l = (document.documentElement.getAttribute("lang") || "en").slice(0, 2);
    return ["en", "es", "ar", "zh"].indexOf(l) >= 0 ? l : "en";
  }
  var L = lang();
  var PR = R + (L === "en" ? "" : L + "/");

  function tv(o) {
    if (!o) return "";
    return typeof o === "string" ? o : (o[L] || o.en || "");
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function loc4() {
    return L === "zh" ? "zh-CN" : L === "ar" ? "ar-AE" : L === "es" ? "es-ES" : "en-US";
  }
  function nf(v) {
    try { return new Intl.NumberFormat(loc4()).format(v); } catch (e) { return String(v); }
  }
  function money(v, cur) {
    if (v == null) return U("poa");
    try {
      return new Intl.NumberFormat(loc4(),
        { style: "currency", currency: cur || "USD", maximumFractionDigits: 0 }).format(v);
    } catch (e) { return (cur || "USD") + " " + nf(v); }
  }
  function when(iso) {
    if (!iso) return "";
    try {
      return new Intl.DateTimeFormat(loc4(), { year: "numeric", month: "long", day: "numeric" })
        .format(new Date(iso));
    } catch (e) { return String(iso).slice(0, 10); }
  }

  /* ---------------------------------------------------------------- i18n */
  var T = {
    poa:        {en:"Price upon application",es:"Precio a consulta",ar:"السعر عند الطلب",zh:"价格面议"},
    perYear:    {en:"per year",es:"al año",ar:"سنوياً",zh:"每年"},
    perSqm:     {en:"per m²",es:"por m²",ar:"لكل م²",zh:"每平米"},
    overview:   {en:"Overview",es:"Resumen",ar:"نظرة عامة",zh:"概览"},
    details:    {en:"Asset details",es:"Datos del activo",ar:"بيانات الأصل",zh:"资产明细"},
    amenities:  {en:"Amenities and provision",es:"Amenidades y dotación",ar:"المرافق والتجهيزات",zh:"设施与配套"},
    beds:       {en:"Bedrooms",es:"Dormitorios",ar:"غرف النوم",zh:"卧室"},
    baths:      {en:"Bathrooms",es:"Baños",ar:"الحمامات",zh:"浴室"},
    parking:    {en:"Parking",es:"Aparcamiento",ar:"مواقف",zh:"车位"},
    built:      {en:"Built area",es:"Superficie construida",ar:"المساحة المبنية",zh:"建筑面积"},
    plot:       {en:"Plot",es:"Parcela",ar:"قطعة الأرض",zh:"地块"},
    hectares:   {en:"Land",es:"Suelo",ar:"الأرض",zh:"土地"},
    keys:       {en:"Keys",es:"Llaves",ar:"المفاتيح",zh:"客房"},
    berths:     {en:"Berths",es:"Amarres",ar:"المراسي",zh:"泊位"},
    reference:  {en:"Reference",es:"Referencia",ar:"المرجع",zh:"编号"},
    category:   {en:"Category",es:"Categoría",ar:"الفئة",zh:"类别"},
    type:       {en:"Type",es:"Tipología",ar:"النوع",zh:"物业类型"},
    offering:   {en:"Offering",es:"Régimen",ar:"نوع العرض",zh:"交易方式"},
    sale:       {en:"For sale",es:"En venta",ar:"للبيع",zh:"出售"},
    rent:       {en:"To rent",es:"En alquiler",ar:"للإيجار",zh:"租赁"},
    location:   {en:"Location",es:"Ubicación",ar:"الموقع",zh:"位置"},
    completion: {en:"Completion",es:"Estado de obra",ar:"حالة الإنجاز",zh:"交付状态"},
    ready:      {en:"Ready",es:"Listo",ar:"جاهز",zh:"现房"},
    off_plan:   {en:"Off-plan",es:"Off-plan",ar:"على المخطط",zh:"期房"},
    handover:   {en:"Handover",es:"Entrega",ar:"التسليم",zh:"交付"},
    furnishing: {en:"Furnishing",es:"Amueblado",ar:"التأثيث",zh:"家具配置"},
    furnished:  {en:"Furnished",es:"Amueblado",ar:"مفروش",zh:"带家具"},
    unfurnished:{en:"Unfurnished",es:"Sin amueblar",ar:"غير مفروش",zh:"无家具"},
    partly_furnished:{en:"Partly furnished",es:"Parcialmente amueblado",ar:"مفروش جزئياً",zh:"部分家具"},
    ownership:  {en:"Ownership",es:"Titularidad",ar:"نوع الملكية",zh:"产权"},
    freehold:   {en:"Freehold",es:"Pleno dominio",ar:"تملّك حر",zh:"永久产权"},
    leasehold:  {en:"Leasehold",es:"Derecho de superficie",ar:"حق انتفاع",zh:"租赁产权"},
    published:  {en:"Published",es:"Publicado",ar:"تاريخ النشر",zh:"发布时间"},
    updated:    {en:"Last updated",es:"Última actualización",ar:"آخر تحديث",zh:"最近更新"},
    trust:      {en:"Verification",es:"Verificación",ar:"التوثيق",zh:"核验"},
    verified:   {en:"Verified listing",es:"Activo verificado",ar:"عرض موثّق",zh:"已核验房源"},
    unverified: {en:"Verification in progress",es:"Verificación en curso",ar:"التوثيق قيد الإنجاز",zh:"核验进行中"},
    quality:    {en:"Listing quality",es:"Calidad de la ficha",ar:"جودة العرض",zh:"房源完整度"},
    agent:      {en:"Your adviser",es:"Su asesor",ar:"مستشارك",zh:"您的顾问"},
    licence:    {en:"Licence",es:"Licencia",ar:"الترخيص",zh:"执照"},
    enquire:    {en:"Private enquiry",es:"Consulta reservada",ar:"استفسار خاص",zh:"私人咨询"},
    save:       {en:"Save this asset",es:"Guardar este activo",ar:"حفظ هذا الأصل",zh:"收藏此资产"},
    saved:      {en:"Saved",es:"Guardado",ar:"محفوظ",zh:"已收藏"},
    share:      {en:"Copy link",es:"Copiar enlace",ar:"نسخ الرابط",zh:"复制链接"},
    copied:     {en:"Link copied",es:"Enlace copiado",ar:"تم نسخ الرابط",zh:"链接已复制"},
    back:       {en:"Back to the inventory",es:"Volver al inventario",ar:"العودة إلى المعروض",zh:"返回资产库"},
    similar:    {en:"Similar assets",es:"Activos similares",ar:"أصول مشابهة",zh:"同类资产"},
    onMap:      {en:"On the map",es:"Sobre el mapa",ar:"على الخريطة",zh:"地图位置"},
    precision:  {en:"Approximate position. The exact address is disclosed to qualified enquirers.",
                 es:"Posición aproximada. La dirección exacta se facilita a interesados cualificados.",
                 ar:"موقع تقريبي. يُفصح عن العنوان الدقيق للمستفسرين المؤهّلين.",
                 zh:"位置为大致范围。确切地址仅向经审核的意向方披露。"},
    demoNote:   {en:"Sample record. Particulars are illustrative until the live mandate is loaded.",
                 es:"Registro de muestra. Los datos son ilustrativos hasta que se cargue el mandato real.",
                 ar:"سجل تجريبي. البيانات إيضاحية إلى أن يُحمَّل التفويض الفعلي.",
                 zh:"样例记录。在正式委托载入前，各项数据仅供示意。"},
    featured:   {en:"Featured",es:"Destacado",ar:"مميّز",zh:"精选"},
    premium:    {en:"Premium",es:"Premium",ar:"بريميوم",zh:"尊享"},
    spotlight:  {en:"Spotlight",es:"En foco",ar:"تحت الضوء",zh:"聚焦"},
    notFound:   {en:"This asset is not available.",es:"Este activo no está disponible.",
                 ar:"هذا الأصل غير متاح.",zh:"该资产不可用。"}
  };
  function U(k) { return (T[k] && (T[k][L] || T[k].en)) || k; }

  /* ---------------------------------------------------------------- imagen */
  var WIDTHS_BY_DIR = {
    "assets/img/xaru/catalog/": [480, 768, 1280, 1920, 2560],
    "assets/img/xaru/gen2/":    [768, 1280, 1920]
  };
  function picture(rel, alt, sizes, eager) {
    rel = String(rel || "").replace(/^\//, "");
    var m = /^(.*\/)([^\/]+)\.jpg$/.exec(rel);
    var attrs = ' alt="' + esc(alt) + '" class="w-100"' +
      (eager ? ' loading="eager" fetchpriority="high"' : ' loading="lazy"') + ' decoding="async"';
    if (!m || !WIDTHS_BY_DIR[m[1]]) return '<img src="' + esc(R + rel) + '"' + attrs + ">";
    var dir = m[1] + "r/", base = m[2], w = WIDTHS_BY_DIR[m[1]];
    function set(ext) {
      return w.map(function (x) { return R + dir + base + "-" + x + "." + ext + " " + x + "w"; }).join(", ");
    }
    return "<picture>" +
      '<source type="image/avif" srcset="' + esc(set("avif")) + '" sizes="' + sizes + '">' +
      '<source type="image/webp" srcset="' + esc(set("webp")) + '" sizes="' + sizes + '">' +
      '<img src="' + esc(R + dir + base + "-1280.jpg") + '"' + attrs + "></picture>";
  }

  /* --------------------------------------------------- persistencia (favoritos)
     Mismo adaptador que usa el marketplace: hoy navegador, mañana el
     Engagement Service. */
  var Store = {
    favorites: function () {
      try { return JSON.parse(localStorage.getItem("xaru_favorites") || "[]"); } catch (e) { return []; }
    },
    toggle: function (id) {
      var f = this.favorites(), i = f.indexOf(id);
      if (i >= 0) f.splice(i, 1); else f.push(id);
      try { localStorage.setItem("xaru_favorites", JSON.stringify(f)); } catch (e) {}
      return i < 0;
    }
  };

  /* ---------------------------------------------------------------- bloques */
  function fact(v, label) {
    return '<li><div class="cs_center_column text-center">' +
      '<h2 class="cs_fs_20 cs_semibold mb-0"><bdi>' + esc(v) + "</bdi></h2>" +
      '<span class="cs_fs_14">' + esc(label) + "</span></div></li>";
  }
  function row(label, value) {
    if (value === "" || value == null) return "";
    return '<li><span class="cs_semibold">' + esc(label) + ":</span><span><bdi>" +
      esc(value) + "</bdi></span></li>";
  }
  function sqm(v) { return v == null ? "" : nf(v) + (L === "ar" ? " م²" : " m²"); }

  function render(d, meta, similar) {
    var title = tv(d.title);
    var typeName = tv(d.propertyType && d.propertyType.name) || (d.propertyType || {}).slug || "";
    // El toponimo no se traduce; el pais si. Se compone aqui en vez de usar
    // `displayAddress`, que viene en un solo idioma desde la base.
    var country = tv(d.location.country) || d.location.countryCode;
    var place = [d.location.city, country].filter(Boolean).join(", ") ||
                d.location.displayAddress || "";
    var sp = d.spaces || {}, pr = d.price || {}, cond = d.condition || {}, tr = d.trust || {};
    var hero = (d.media && d.media[0] && d.media[0].url) || "";
    var priceTxt = (pr.onApplication || pr.amount == null)
      ? U("poa")
      : money(pr.amount, pr.currency) + (d.offeringType === "rent" ? " " + U("perYear") : "");

    /* --- distintivos ------------------------------------------------- */
    var badges = "";
    if (tr.promotion && tr.promotion !== "none")
      badges += '<span class="xr_promo_badge is-' + esc(tr.promotion) + '">' +
        esc(U(tr.promotion)) + "</span>";
    if (tr.verified) badges += '<span class="xr_verified_badge">' + esc(U("verified")) + "</span>";
    if (d.demo) badges += '<span class="xr_demo_badge">' + esc(d.demoLabel || "DEMO") + "</span>";

    /* --- tira de datos ----------------------------------------------- */
    var strip = "";
    if (sp.bedrooms)  strip += fact(nf(sp.bedrooms), U("beds"));
    if (sp.bathrooms) strip += fact(nf(sp.bathrooms), U("baths"));
    if (sp.builtAreaSqm) strip += fact(sqm(sp.builtAreaSqm), U("built"));
    if (sp.plotAreaSqm)  strip += fact(sqm(sp.plotAreaSqm), U("plot"));
    if (sp.hectares)  strip += fact(nf(sp.hectares) + (L === "ar" ? " هكتار" : " ha"), U("hectares"));
    if (sp.hotelKeys) strip += fact(nf(sp.hotelKeys), U("keys"));
    if (sp.berths)    strip += fact(nf(sp.berths), U("berths"));
    if (sp.parking)   strip += fact(nf(sp.parking), U("parking"));
    if (pr.perSqm)    strip += fact(money(pr.perSqm, pr.currency), U("perSqm"));

    /* --- amenidades, agrupadas por familia ---------------------------- */
    var amenHtml = "";
    if (d.amenities && d.amenities.length) {
      var nameOf = {};
      ((meta && meta.amenities) || []).forEach(function (a) {
        nameOf[a.slug] = a["name_" + L] || a.name_en;
      });
      amenHtml = '<div class="cs_property_amenties"><h3 class="cs_fs_25 cs_semibold cs_mb_15">' +
        esc(U("amenities")) + '</h3><ul class="cs_property_amenties_list cs_mp_0">' +
        d.amenities.map(function (s) {
          return "<li>" + esc(nameOf[s] || s) + "</li>";
        }).join("") + "</ul></div>";
    }

    /* --- tabla de datos ----------------------------------------------- */
    var handover = (cond.handover && cond.handover.year)
      ? "Q" + cond.handover.quarter + " " + cond.handover.year : "";
    var table =
      row(U("reference"), d.publicId) +
      row(U("type"), typeName) +
      row(U("offering"), U(d.offeringType === "rent" ? "rent" : "sale")) +
      row(U("location"), place) +
      row(U("beds"), sp.bedrooms ? nf(sp.bedrooms) : "") +
      row(U("baths"), sp.bathrooms ? nf(sp.bathrooms) : "") +
      row(U("built"), sqm(sp.builtAreaSqm)) +
      row(U("plot"), sqm(sp.plotAreaSqm)) +
      row(U("hectares"), sp.hectares ? nf(sp.hectares) + " ha" : "") +
      row(U("completion"), cond.completion ? U(cond.completion) : "") +
      row(U("handover"), handover) +
      row(U("furnishing"), (cond.furnishing && cond.furnishing !== "unknown") ? U(cond.furnishing) : "") +
      row(U("ownership"), (cond.ownership && cond.ownership !== "unknown") ? U(cond.ownership) : "") +
      row(U("published"), when(d.publishedAt)) +
      row(U("updated"), when(d.updatedAt));

    /* --- mapa ---------------------------------------------------------- */
    var mapHtml = "";
    if (d.location.lat && d.location.lon) {
      mapHtml = '<div class="xr_pdp_block"><h3 class="cs_fs_25 cs_semibold cs_mb_15">' +
        esc(U("onMap")) + '</h3><div class="xr_pdp_map" data-lat="' + d.location.lat +
        '" data-lon="' + d.location.lon + '"></div>' +
        '<p class="xr_pdp_note">' + esc(U("precision")) + "</p></div>";
    }

    /* --- similares ------------------------------------------------------ */
    var simHtml = similar.slice(0, 3).map(function (s) {
      var st = tv(s.t);
      return '<div class="col-md-4"><a class="xr_rel_card" href="' + PR +
        "property-details.html?id=" + encodeURIComponent(s.id) + '">' +
        '<span class="xr_rel_img">' + picture(s.img, st, "(max-width:767px) 92vw, 360px") + "</span>" +
        '<span class="xr_rel_body"><strong>' + esc(st) + "</strong>" +
        "<em>" + esc([s.city, s.cc].filter(Boolean).join(", ")) + "</em>" +
        "<b>" + esc((s.poa || s.p == null) ? U("poa") : money(s.p, s.cur)) + "</b></span></a></div>";
    }).join("");

    var ag = d.agent || {}, og = d.agency || {};
    var fav = Store.favorites().indexOf(d.publicId) >= 0;

    return (
      '<div class="cs_property_header cs_mb_40">' +
        '<div class="cs_property_header_left">' +
          '<p class="xr_pdp_eyebrow">' + esc(typeName) + " · " +
            esc(U(d.offeringType === "rent" ? "rent" : "sale")) + "</p>" +
          '<h1 class="cs_fs_49 cs_mb_3">' + esc(title) + "</h1>" +
          '<div class="cs_property_location_text"><span class="mb-0">' + esc(place) + "</span></div>" +
        "</div>" +
        '<div class="cs_property_header_right">' +
          '<h3 class="cs_property_price cs_fs_39 cs_mb_8"><bdi>' + esc(priceTxt) + "</bdi></h3>" +
          '<div class="xr_pdp_actions">' +
            '<button type="button" class="xr_pdp_fav' + (fav ? " is-on" : "") +
              '" data-fav aria-pressed="' + (fav ? "true" : "false") + '">' +
              '<i class="fa-solid fa-heart"></i> <span>' + esc(U(fav ? "saved" : "save")) + "</span></button>" +
            '<button type="button" class="xr_pdp_share" data-share>' +
              '<i class="fa-solid fa-link"></i> <span>' + esc(U("share")) + "</span></button>" +
          "</div>" +
        "</div>" +
      "</div>" +
      '<div class="cs_property_banner cs_radius_20 position-relative cs_mb_40">' +
        picture(hero, title + " — " + typeName + ", " + place, "(max-width:991px) 94vw, 1140px", true) +
        '<span class="xr_card_badges">' + badges + "</span>" +
      "</div>" +
      (strip ? '<ul class="cs_property_features_list cs_mp_0">' + strip + "</ul>" : "") +
      '<div class="cs_height_50 cs_height_lg_40"></div>' +
      '<div class="row cs_gap_y_40">' +
        '<div class="col-lg-8"><div class="cs_single_property_content cs_radius_20">' +
          '<div class="cs_property_desc">' +
            '<h3 class="cs_fs_25 cs_semibold cs_mb_15">' + esc(U("overview")) + "</h3>" +
            "<p>" + esc(tv(d.description)) + "</p>" +
          "</div>" +
          amenHtml +
          '<div class="cs_property_info"><h3 class="cs_fs_25 cs_semibold cs_mb_15">' +
            esc(U("details")) + '</h3><ul class="cs_property_info_list cs_mp_0">' + table + "</ul></div>" +
          mapHtml +
        "</div></div>" +
        '<div class="col-lg-4"><aside class="cs_sidebar cs_style_1 cs_gray3_bg cs_radius_20">' +
          '<div class="cs_sidebar_widget xr_pdp_agent">' +
            '<h3 class="cs_sidebar_widget_title cs_fs_20 cs_semibold cs_mb_16"><span>' +
              esc(U("agent")) + "</span></h3>" +
            (ag.name ? '<p class="xr_pdp_agent_name">' + esc(ag.name) +
              (ag.verified ? ' <i class="fa-solid fa-circle-check" aria-hidden="true"></i>' : "") + "</p>" : "") +
            (og.name ? '<p class="xr_pdp_agent_org">' + esc(og.name) + "</p>" : "") +
            (ag.licence ? '<p class="xr_pdp_agent_lic">' + esc(U("licence")) + " " + esc(ag.licence) + "</p>" : "") +
            '<a href="' + PR + 'private-enquiry/" class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_10">' +
              "<span>" + esc(U("enquire")) + "</span></a>" +
          "</div>" +
          '<div class="cs_sidebar_widget xr_pdp_trust">' +
            '<h3 class="cs_sidebar_widget_title cs_fs_20 cs_semibold cs_mb_16"><span>' +
              esc(U("trust")) + "</span></h3>" +
            '<p class="xr_pdp_trust_state is-' + (tr.verified ? "on" : "off") + '">' +
              '<i class="fa-solid fa-' + (tr.verified ? "shield-halved" : "hourglass-half") + '"></i> ' +
              esc(U(tr.verified ? "verified" : "unverified")) + "</p>" +
            (tr.qualityScore ? '<p class="xr_pdp_quality"><span>' + esc(U("quality")) +
              "</span><b>" + nf(tr.qualityScore) + "/100</b></p>" : "") +
            (d.demo ? '<p class="xr_pdp_demo">' + esc(U("demoNote")) + "</p>" : "") +
            '<a href="' + PR + 'real-estate/search/" class="xr_link">' + esc(U("back")) + "</a>" +
          "</div>" +
        "</aside></div>" +
      "</div>" +
      (simHtml
        ? '<div class="cs_height_70 cs_height_lg_50"></div>' +
          '<h3 class="cs_fs_25 cs_semibold cs_mb_15">' + esc(U("similar")) + "</h3>" +
          '<div class="row cs_gap_y_30 xr_rel_grid">' + simHtml + "</div>"
        : "")
    );
  }

  /* ---------------------------------------------------------------- mapa */
  function mountMap() {
    var el = document.querySelector(".xr_pdp_map");
    if (!el) return;
    var lat = parseFloat(el.getAttribute("data-lat")), lon = parseFloat(el.getAttribute("data-lon"));
    function draw() {
      var map = window.L.map(el, { scrollWheelZoom: false }).setView([lat, lon], 11);
      window.L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        { maxZoom: 18, attribution: "© OpenStreetMap" }).addTo(map);
      // Circulo, no chincheta: la posicion es de comunidad, no de portal.
      window.L.circle([lat, lon], { radius: 1600, color: "#8B6E45", weight: 1,
        fillColor: "#C9A876", fillOpacity: 0.22 }).addTo(map);
      setTimeout(function () { map.invalidateSize(); }, 80);
    }
    if (window.L && window.L.map) return draw();
    var css = document.createElement("link");
    css.rel = "stylesheet"; css.href = R + "assets/vendor/leaflet/leaflet.css";
    document.head.appendChild(css);
    var s = document.createElement("script");
    s.src = R + "assets/vendor/leaflet/leaflet.js";
    s.onload = function () {
      if (window.L && window.L.Icon && window.L.Icon.Default)
        window.L.Icon.Default.imagePath = R + "assets/vendor/leaflet/images/";
      draw();
    };
    document.head.appendChild(s);
  }

  /* ---------------------------------------------------------------- eventos */
  function bind(id) {
    HOST.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (!b) return;
      if (b.hasAttribute("data-fav")) {
        var on = Store.toggle(id);
        b.classList.toggle("is-on", on);
        b.setAttribute("aria-pressed", on ? "true" : "false");
        var s1 = b.querySelector("span"); if (s1) s1.textContent = U(on ? "saved" : "save");
        return;
      }
      if (b.hasAttribute("data-share")) {
        var done = function () {
          var s2 = b.querySelector("span"); if (s2) s2.textContent = U("copied");
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(location.href).then(done, done);
        } else { done(); }
      }
    });
  }

  /* Historial de vistos: lo escribe la ficha, lo lee el panel del comprador.
     Veinte entradas, sin duplicados, la mas reciente primero. */
  function remember(id) {
    try {
      var v = JSON.parse(localStorage.getItem("xaru_viewed") || "[]");
      v = v.filter(function (e) { return e && e.id !== id; });
      v.unshift({ id: id, at: new Date().toISOString() });
      localStorage.setItem("xaru_viewed", JSON.stringify(v.slice(0, 20)));
    } catch (e) {}
  }

  /* ---------------------------------------------------------------- carga */
  function legacy(id) {
    return Promise.all(PACKS.map(function (f) {
      return fetch(R + "data/properties/" + f + ".json").then(function (r) {
        return r.ok ? r.json() : { items: [] };
      }).catch(function () { return { items: [] }; });
    })).then(function (packs) {
      var all = [];
      packs.forEach(function (p) { all = all.concat(p.items || []); });
      var it = all.filter(function (x) { return x.id === id; })[0];
      if (!it) return null;
      // El registro heredado se traduce a la forma de la API: un solo camino
      // de render, dos origenes.
      var lc = it.language_content || {};
      return {
        publicId: it.id, demo: false,
        title: lc.title || it.title,
        description: it.long_description || it.short_description || {},
        businessCategory: it.subcategory, offeringType: "sale",
        propertyType: { slug: it.variant, name: lc.variant || it.variant },
        location: { countryCode: it.country, city: it.city,
                    displayAddress: [it.city, it.region, it.country].filter(Boolean).join(", "),
                    precision: "community", lat: it.lat, lon: it.lon },
        spaces: { bedrooms: it.bedrooms, bathrooms: it.bathrooms,
                  builtAreaSqm: it.built_area_m2, plotAreaSqm: it.land_area_m2,
                  hectares: it.hectares, hotelKeys: it.hotel_keys, berths: it.berths },
        price: { currency: "USD", amount: it.price_usd, onApplication: !it.price_usd },
        condition: {}, amenities: [],
        media: [{ kind: "photo", url: it.hero_image }],
        trust: { verified: true, promotion: "none" },
        agent: {}, agency: {}, publishedAt: null, updatedAt: null
      };
    });
  }

  function fetchListing(id) {
    return fetch(API + "listings/" + encodeURIComponent(id) + ".json")
      .then(function (r) { if (!r.ok) throw 0; return r.json(); })
      .catch(function () { return legacy(id); });
  }

  var id = new URLSearchParams(location.search).get("id");
  if (!id) { location.replace(PR + "real-estate/search/"); return; }

  Promise.all([
    fetchListing(id),
    fetch(API + "meta.json").then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; }),
    fetch(API + "search-index.json").then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; })
  ]).then(function (out) {
    var d = out[0], meta = out[1], idx = out[2];
    if (!d) { location.replace(PR + "real-estate/search/"); return; }

    var similar = [];
    if (idx && idx.items) {
      var slug = (d.propertyType || {}).slug;
      similar = idx.items.filter(function (x) {
        return x.id !== d.publicId && x.type === slug && x.cc === d.location.countryCode;
      });
      if (similar.length < 3) {
        idx.items.forEach(function (x) {
          if (similar.length >= 3) return;
          if (x.id !== d.publicId && x.type === slug && similar.indexOf(x) < 0) similar.push(x);
        });
      }
    }

    HOST.innerHTML = '<div class="cs_property_details">' + render(d, meta, similar) + "</div>";
    document.title = tv(d.title) + " | XARU HOME";
    var md = document.querySelector('meta[name="description"]');
    if (md) md.setAttribute("content", String(tv(d.description) || tv(d.title)).slice(0, 300));

    bind(d.publicId);
    mountMap();
    remember(d.publicId);

    /* Las secciones de la plantilla que no aplican a esta cartera: hipoteca,
       colegios cercanos, plano de planta, agenda de visita. Se retiran en vez
       de dejarse con cifras inventadas. */
    [".cs_property_mortgage", ".cs_property_nearby", ".cs_property_floor",
     ".cs_property_surroundings", ".cs_property_financial_info"].forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (el) { el.remove(); });
    });
    var rel = document.querySelector("section.cs_slider.cs_style_1.cs_slider_gap_24");
    if (rel) rel.remove();
  }).catch(function (err) {
    if (window.console) console.warn("[xaru-detail]", err);
    HOST.innerHTML = '<div class="cs_property_details"><p class="xr_mp_empty">' +
      esc(U("notFound")) + "</p></div>";
  });
})();
