/*
 * XARU HOME — panel del comprador (Biblia §5.7)
 * =============================================================
 * Guardados con carpetas, búsquedas guardadas, alertas, historial de vistos y
 * comparador. Cinco pestañas sobre un mismo estado.
 *
 * MODO SIMULACIÓN
 * ---------------
 * No hay cuenta ni servidor todavía, así que todo esto vive en el navegador a
 * través de `Store`, un adaptador con la firma que tendrá el Engagement
 * Service: `list`, `add`, `remove`, `move`. El día que exista, cambian cuatro
 * métodos y el resto del fichero se queda igual. Lo que se guarda aquí no sale
 * del dispositivo, y la página lo dice.
 *
 * El historial de vistos lo escribe la ficha del activo; aquí solo se lee.
 *
 * Montaje: <div data-account></div>
 */
(function () {
  "use strict";

  var HOST = document.querySelector("[data-account]");
  if (!HOST) return;

  var R = "/";
  var API = R + "data/api/v1/";

  function lang() {
    var l = (document.documentElement.getAttribute("lang") || "en").slice(0, 2);
    return ["en", "es", "ar", "zh"].indexOf(l) >= 0 ? l : "en";
  }
  var L = lang();
  var PR = R + (L === "en" ? "" : L + "/");

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
    if (v == null) return t("poa");
    try {
      return new Intl.NumberFormat(loc4(),
        { style: "currency", currency: cur || "USD", maximumFractionDigits: 0 }).format(v);
    } catch (e) { return (cur || "USD") + " " + nf(v); }
  }
  function when(iso) {
    if (!iso) return "";
    try {
      return new Intl.DateTimeFormat(loc4(),
        { year: "numeric", month: "short", day: "numeric" }).format(new Date(iso));
    } catch (e) { return String(iso).slice(0, 10); }
  }

  var T = {
    title:      {en:"Your saved work",es:"Su trabajo guardado",
                 ar:"ما حفظته",zh:"您的收藏"},
    saved:      {en:"Saved assets",es:"Activos guardados",ar:"الأصول المحفوظة",zh:"收藏的资产"},
    searches:   {en:"Saved searches",es:"Búsquedas guardadas",ar:"عمليات البحث المحفوظة",zh:"保存的搜索"},
    alerts:     {en:"Alerts",es:"Alertas",ar:"التنبيهات",zh:"提醒"},
    viewed:     {en:"Recently viewed",es:"Vistos recientemente",ar:"شوهدت مؤخراً",zh:"最近浏览"},
    compare:    {en:"Compare",es:"Comparar",ar:"مقارنة",zh:"对比"},
    folders:    {en:"Folders",es:"Carpetas",ar:"المجلدات",zh:"文件夹"},
    allFolder:  {en:"All",es:"Todas",ar:"الكل",zh:"全部"},
    newFolder:  {en:"New folder",es:"Nueva carpeta",ar:"مجلد جديد",zh:"新建文件夹"},
    folderName: {en:"Folder name",es:"Nombre de la carpeta",ar:"اسم المجلد",zh:"文件夹名称"},
    moveTo:     {en:"Move to",es:"Mover a",ar:"نقل إلى",zh:"移动至"},
    remove:     {en:"Remove",es:"Quitar",ar:"إزالة",zh:"移除"},
    open:       {en:"Open",es:"Abrir",ar:"فتح",zh:"打开"},
    rerun:      {en:"Run this search",es:"Ejecutar esta búsqueda",
                 ar:"تشغيل هذا البحث",zh:"运行此搜索"},
    createAlert:{en:"Alert me",es:"Avisarme",ar:"نبّهني",zh:"提醒我"},
    alertOn:    {en:"Alert on",es:"Alerta activa",ar:"التنبيه مفعّل",zh:"提醒已开"},
    daily:      {en:"Daily",es:"Diaria",ar:"يومي",zh:"每日"},
    weekly:     {en:"Weekly",es:"Semanal",ar:"أسبوعي",zh:"每周"},
    instant:    {en:"Instant",es:"Inmediata",ar:"فوري",zh:"即时"},
    frequency:  {en:"Frequency",es:"Frecuencia",ar:"التكرار",zh:"频率"},
    clearAll:   {en:"Clear",es:"Vaciar",ar:"مسح",zh:"清空"},
    addCompare: {en:"Add to compare",es:"Añadir al comparador",
                 ar:"أضف للمقارنة",zh:"加入对比"},
    emptySaved: {en:"You have not saved any asset yet.",
                 es:"Todavía no ha guardado ningún activo.",
                 ar:"لم تحفظ أي أصل بعد.",zh:"您尚未收藏任何资产。"},
    emptySear:  {en:"No saved searches yet. Save one from any result page.",
                 es:"No hay búsquedas guardadas. Guarde una desde cualquier página de resultados.",
                 ar:"لا عمليات بحث محفوظة بعد. احفظ واحدة من أي صفحة نتائج.",
                 zh:"尚无保存的搜索。可在任意结果页保存。"},
    emptyView:  {en:"Nothing viewed yet.",es:"Nada visto todavía.",
                 ar:"لم تُعرض أي عناصر بعد.",zh:"暂无浏览记录。"},
    emptyComp:  {en:"Add up to four assets to compare them side by side.",
                 es:"Añada hasta cuatro activos para compararlos lado a lado.",
                 ar:"أضف حتى أربعة أصول لمقارنتها جنباً إلى جنب.",zh:"最多可添加四项资产进行并排对比。"},
    browse:     {en:"Browse the inventory",es:"Explorar el inventario",
                 ar:"تصفّح المعروض",zh:"浏览资产库"},
    poa:        {en:"Price upon application",es:"Precio a consulta",
                 ar:"السعر عند الطلب",zh:"价格面议"},
    beds:       {en:"Bedrooms",es:"Dormitorios",ar:"غرف النوم",zh:"卧室"},
    baths:      {en:"Bathrooms",es:"Baños",ar:"الحمامات",zh:"浴室"},
    area:       {en:"Built area",es:"Superficie",ar:"المساحة",zh:"建筑面积"},
    price:      {en:"Price",es:"Precio",ar:"السعر",zh:"价格"},
    ppsqm:      {en:"Price per m²",es:"Precio por m²",ar:"السعر لكل م²",zh:"每平米单价"},
    type:       {en:"Type",es:"Tipología",ar:"النوع",zh:"物业类型"},
    location:   {en:"Location",es:"Ubicación",ar:"الموقع",zh:"位置"},
    verifiedL:  {en:"Verified",es:"Verificado",ar:"موثّق",zh:"已核验"},
    yes:        {en:"Yes",es:"Sí",ar:"نعم",zh:"是"},
    no:         {en:"No",es:"No",ar:"لا",zh:"否"},
    localNote:  {en:"Saved on this device. Sign-in to carry your saved assets and alerts between devices is coming with the client portal.",
                 es:"Guardado en este dispositivo. El acceso con cuenta, para llevar sus activos y alertas entre dispositivos, llega con el portal de cliente.",
                 ar:"محفوظ على هذا الجهاز. وتسجيل الدخول لنقل أصولك وتنبيهاتك بين الأجهزة يأتي مع بوابة العملاء.",
                 zh:"保存在本设备。可在多设备间同步收藏与提醒的账户登录，将随客户门户一同推出。"},
    loading:    {en:"Loading…",es:"Cargando…",ar:"جارٍ التحميل…",zh:"加载中…"},
    results:    {en:"results now",es:"resultados ahora",ar:"نتيجة الآن",zh:"当前结果"}
  };
  function t(k) { return (T[k] && (T[k][L] || T[k].en)) || k; }

  /* ------------------------------------------------- adaptador de persistencia
     Firma del futuro Engagement Service. Hoy: navegador. */
  var Store = {
    _r: function (k, d) {
      try { return JSON.parse(localStorage.getItem(k) || d); } catch (e) { return JSON.parse(d); }
    },
    _w: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} },
    favorites:   function () { return this._r("xaru_favorites", "[]"); },
    setFavorites:function (v) { this._w("xaru_favorites", v); },
    folders:     function () { return this._r("xaru_folders", '{"__names":[]}'); },
    setFolders:  function (v) { this._w("xaru_folders", v); },
    searches:    function () { return this._r("xaru_saved_searches", "[]"); },
    setSearches: function (v) { this._w("xaru_saved_searches", v); },
    viewed:      function () { return this._r("xaru_viewed", "[]"); },
    compare:     function () { return this._r("xaru_compare", "[]"); },
    setCompare:  function (v) { this._w("xaru_compare", v); }
  };

  var IDX = [], BY_ID = {};

  var WIDTHS_BY_DIR = {
    "assets/img/xaru/catalog/": [480, 768, 1280, 1920, 2560],
    "assets/img/xaru/gen2/":    [768, 1280, 1920]
  };
  function picture(rel, alt) {
    rel = String(rel || "").replace(/^\//, "");
    var m = /^(.*\/)([^\/]+)\.jpg$/.exec(rel);
    if (!m || !WIDTHS_BY_DIR[m[1]]) {
      return '<img src="' + esc(R + rel) + '" alt="' + esc(alt) + '" loading="lazy">';
    }
    var dir = m[1] + "r/", base = m[2], w = WIDTHS_BY_DIR[m[1]];
    function set(ext) {
      return w.map(function (x) { return R + dir + base + "-" + x + "." + ext + " " + x + "w"; }).join(", ");
    }
    var sizes = "(max-width:767px) 92vw, 300px";
    return "<picture>" +
      '<source type="image/avif" srcset="' + esc(set("avif")) + '" sizes="' + sizes + '">' +
      '<source type="image/webp" srcset="' + esc(set("webp")) + '" sizes="' + sizes + '">' +
      '<img src="' + esc(R + dir + base + "-768.jpg") + '" alt="' + esc(alt) +
      '" loading="lazy" decoding="async"></picture>';
  }

  function titleOf(x) { return (x.t && (x.t[L] || x.t.en)) || x.id; }
  function priceOf(x) {
    return (x.poa || x.p == null) ? t("poa") : money(x.p, x.cur);
  }

  var TAB = "saved", FOLDER = "";

  function shell() {
    var tabs = [["saved", t("saved")], ["searches", t("searches")],
                ["alerts", t("alerts")], ["viewed", t("viewed")], ["compare", t("compare")]];
    return '<div class="xr_ac_tabs" role="tablist">' +
      tabs.map(function (x) {
        return '<button type="button" role="tab" data-tab="' + x[0] + '"' +
          (x[0] === TAB ? ' class="is-on" aria-selected="true"' : ' aria-selected="false"') +
          "><span>" + esc(x[1]) + '</span><b class="xr_ac_n" data-n="' + x[0] + '"></b></button>';
      }).join("") + "</div>" +
      '<div class="xr_ac_body"></div>' +
      '<p class="xr_ac_local">' + esc(t("localNote")) + "</p>";
  }

  function counts() {
    var f = Store.favorites(), s = Store.searches(), v = Store.viewed(), c = Store.compare();
    var n = { saved: f.length, searches: s.length,
              alerts: s.filter(function (x) { return x.alert; }).length,
              viewed: v.length, compare: c.length };
    HOST.querySelectorAll(".xr_ac_n").forEach(function (el) {
      var k = el.getAttribute("data-n");
      el.textContent = n[k] ? nf(n[k]) : "";
    });
  }

  /* ---------------------------------------------------------------- guardados */
  function tile(x, folder) {
    var names = Store.folders().__names || [];
    var href = PR + "property-details.html?id=" + encodeURIComponent(x.id);
    return '<article class="xr_ac_tile" data-id="' + esc(x.id) + '">' +
      '<a class="xr_ac_img" href="' + esc(href) + '">' + picture(x.img, titleOf(x)) + "</a>" +
      '<div class="xr_ac_txt">' +
        '<h4><a href="' + esc(href) + '">' + esc(titleOf(x)) + "</a></h4>" +
        "<p>" + esc([x.city, x.cc].filter(Boolean).join(", ")) + "</p>" +
        "<b>" + esc(priceOf(x)) + "</b>" +
      "</div>" +
      '<div class="xr_ac_ops">' +
        '<select data-move="' + esc(x.id) + '" aria-label="' + esc(t("moveTo")) + '">' +
          '<option value="">' + esc(t("moveTo")) + "…</option>" +
          '<option value="">' + esc(t("allFolder")) + "</option>" +
          names.map(function (n) {
            return '<option value="' + esc(n) + '"' + (n === folder ? " selected" : "") +
              ">" + esc(n) + "</option>";
          }).join("") +
        "</select>" +
        '<button type="button" data-cmp="' + esc(x.id) + '">' + esc(t("addCompare")) + "</button>" +
        '<button type="button" class="is-danger" data-unfav="' + esc(x.id) + '">' +
          esc(t("remove")) + "</button>" +
      "</div>" +
    "</article>";
  }

  function viewSaved() {
    var favs = Store.favorites();
    var fold = Store.folders();
    var names = fold.__names || [];
    var items = favs.map(function (id) { return BY_ID[id]; }).filter(Boolean);
    if (FOLDER) {
      items = items.filter(function (x) { return fold[x.id] === FOLDER; });
    }
    return '<div class="xr_ac_folders">' +
        '<button type="button" class="xr_ac_folder' + (FOLDER ? "" : " is-on") +
          '" data-folder="">' + esc(t("allFolder")) + "</button>" +
        names.map(function (n) {
          return '<button type="button" class="xr_ac_folder' + (FOLDER === n ? " is-on" : "") +
            '" data-folder="' + esc(n) + '">' + esc(n) + "</button>";
        }).join("") +
        '<button type="button" class="xr_ac_newfolder">+ ' + esc(t("newFolder")) + "</button>" +
      "</div>" +
      (items.length
        ? '<div class="xr_ac_grid">' + items.map(function (x) {
            return tile(x, fold[x.id] || "");
          }).join("") + "</div>"
        : '<div class="xr_ac_empty"><p>' + esc(t("emptySaved")) + '</p>' +
          '<a class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_10" href="' +
          PR + 'real-estate/search/"><span>' + esc(t("browse")) + "</span></a></div>");
  }

  /* --------------------------------------------------------- búsquedas y alertas */
  function searchRows(onlyAlerts) {
    var list = Store.searches().filter(function (s) { return onlyAlerts ? s.alert : true; });
    if (!list.length) {
      return '<div class="xr_ac_empty"><p>' + esc(t("emptySear")) + '</p>' +
        '<a class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_10" href="' +
        PR + 'real-estate/search/"><span>' + esc(t("browse")) + "</span></a></div>";
    }
    return '<ul class="xr_ac_list">' + list.map(function (s, i) {
      var n = countFor(s.qs, s.base);
      return '<li class="xr_ac_row">' +
        '<div class="xr_ac_row_main">' +
          "<strong>" + esc(s.name || s.qs) + "</strong>" +
          '<span class="xr_ac_row_meta">' + esc(readable(s.qs)) + " · " +
            nf(n) + " " + esc(t("results")) + " · " + esc(when(s.at)) + "</span>" +
        "</div>" +
        '<div class="xr_ac_row_ops">' +
          '<a class="xr_ac_btn" href="' + esc((s.path || (PR + "real-estate/search/")) + (s.qs || "")) + '">' +
            esc(t("rerun")) + "</a>" +
          '<select data-freq="' + i + '" aria-label="' + esc(t("frequency")) + '">' +
            ["instant", "daily", "weekly"].map(function (f) {
              return '<option value="' + f + '"' + (s.freq === f ? " selected" : "") +
                ">" + esc(t(f)) + "</option>";
            }).join("") +
          "</select>" +
          '<button type="button" class="xr_ac_btn' + (s.alert ? " is-on" : "") +
            '" data-alert="' + i + '">' + esc(s.alert ? t("alertOn") : t("createAlert")) + "</button>" +
          '<button type="button" class="xr_ac_btn is-danger" data-delsearch="' + i + '">' +
            esc(t("remove")) + "</button>" +
        "</div>" +
      "</li>";
    }).join("") + "</ul>";
  }

  /* Cuenta cuántos activos devuelve hoy una búsqueda guardada. El valor de una
     alerta es justamente ese: saber que el número se ha movido. */
  function countFor(qs, base) {
    var p = new URLSearchParams(String(qs || "").replace(/^\?/, ""));
    var get = function (k) { return (p.get(k) || "").split(",").filter(Boolean); };
    var num = function (k) { var v = parseFloat(p.get(k)); return isNaN(v) ? null : v; };
    var cc = get("cc"), city = get("city"), type = get("type"), am = get("am");
    base = base || {};
    var off = p.get("offering") || base.offering;
    var cat = p.get("category") || base.category;
    var pmin = num("priceMin"), pmax = num("priceMax"), bmin = num("bedsMin");
    var q = (p.get("q") || "").toLowerCase();
    return IDX.filter(function (x) {
      if (off && x.off !== off) return false;
      if (cat && x.cat !== cat) return false;
      if (cc.length && cc.indexOf(x.cc) < 0) return false;
      if (city.length && city.indexOf(x.city) < 0) return false;
      if (type.length && type.indexOf(x.type) < 0) return false;
      if (am.length && !am.every(function (a) { return (x.am || []).indexOf(a) >= 0; })) return false;
      if (pmin != null && !(x.p != null && x.p >= pmin)) return false;
      if (pmax != null && !(x.p != null && x.p <= pmax)) return false;
      if (bmin != null && !(x.bd >= bmin)) return false;
      if (q && String(titleOf(x)).toLowerCase().indexOf(q) < 0 &&
          String(x.city || "").toLowerCase().indexOf(q) < 0) return false;
      return true;
    }).length;
  }

  function readable(qs) {
    var p = new URLSearchParams(String(qs || "").replace(/^\?/, ""));
    var out = [];
    p.forEach(function (v, k) { if (k !== "page") out.push(k + "=" + v); });
    return out.length ? out.join(" · ") : t("allFolder");
  }

  /* ---------------------------------------------------------------- vistos */
  function viewViewed() {
    var v = Store.viewed().map(function (e) {
      return { x: BY_ID[e.id], at: e.at };
    }).filter(function (e) { return e.x; });
    if (!v.length) return '<div class="xr_ac_empty"><p>' + esc(t("emptyView")) + "</p></div>";
    return '<div class="xr_ac_grid">' + v.map(function (e) {
      var href = PR + "property-details.html?id=" + encodeURIComponent(e.x.id);
      return '<article class="xr_ac_tile">' +
        '<a class="xr_ac_img" href="' + esc(href) + '">' + picture(e.x.img, titleOf(e.x)) + "</a>" +
        '<div class="xr_ac_txt">' +
          '<h4><a href="' + esc(href) + '">' + esc(titleOf(e.x)) + "</a></h4>" +
          "<p>" + esc(when(e.at)) + "</p><b>" + esc(priceOf(e.x)) + "</b>" +
        "</div>" +
        '<div class="xr_ac_ops">' +
          '<button type="button" data-cmp="' + esc(e.x.id) + '">' + esc(t("addCompare")) + "</button>" +
        "</div></article>";
    }).join("") + "</div>" +
      '<button type="button" class="xr_ac_btn is-danger xr_ac_clearviewed">' +
      esc(t("clearAll")) + "</button>";
  }

  /* ---------------------------------------------------------------- comparador */
  function viewCompare() {
    var ids = Store.compare().slice(0, 4);
    var items = ids.map(function (id) { return BY_ID[id]; }).filter(Boolean);
    if (!items.length) return '<div class="xr_ac_empty"><p>' + esc(t("emptyComp")) + '</p>' +
      '<a class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_10" href="' +
      PR + 'real-estate/search/"><span>' + esc(t("browse")) + "</span></a></div>";

    var rows = [
      [t("price"), function (x) { return priceOf(x); }],
      [t("type"), function (x) { return (x.typeName && (x.typeName[L] || x.typeName.en)) || x.type; }],
      [t("location"), function (x) { return [x.city, x.cc].filter(Boolean).join(", "); }],
      [t("beds"), function (x) { return x.bd ? nf(x.bd) : "—"; }],
      [t("baths"), function (x) { return x.ba ? nf(x.ba) : "—"; }],
      [t("area"), function (x) { return x.area ? nf(x.area) + " m²" : (x.ha ? nf(x.ha) + " ha" : "—"); }],
      [t("ppsqm"), function (x) { return x.ppa ? money(x.ppa, x.cur) : "—"; }],
      [t("verifiedL"), function (x) { return x.ver ? t("yes") : t("no"); }]
    ];

    return '<div class="xr_ac_cmpwrap"><table class="xr_ac_cmp"><thead><tr><th></th>' +
      items.map(function (x) {
        var href = PR + "property-details.html?id=" + encodeURIComponent(x.id);
        return '<th><a class="xr_ac_cmp_img" href="' + esc(href) + '">' +
          picture(x.img, titleOf(x)) + "</a>" +
          '<a class="xr_ac_cmp_t" href="' + esc(href) + '">' + esc(titleOf(x)) + "</a>" +
          '<button type="button" class="xr_ac_btn is-danger" data-uncmp="' + esc(x.id) + '">' +
          esc(t("remove")) + "</button></th>";
      }).join("") + "</tr></thead><tbody>" +
      rows.map(function (r) {
        return "<tr><th>" + esc(r[0]) + "</th>" +
          items.map(function (x) { return "<td><bdi>" + esc(r[1](x)) + "</bdi></td>"; }).join("") +
        "</tr>";
      }).join("") + "</tbody></table></div>";
  }

  /* ---------------------------------------------------------------- pintado */
  function paint() {
    var body = HOST.querySelector(".xr_ac_body");
    body.innerHTML =
      TAB === "saved" ? viewSaved()
      : TAB === "searches" ? searchRows(false)
      : TAB === "alerts" ? searchRows(true)
      : TAB === "viewed" ? viewViewed()
      : viewCompare();
    HOST.querySelectorAll("[data-tab]").forEach(function (b) {
      var on = b.getAttribute("data-tab") === TAB;
      b.classList.toggle("is-on", on);
      b.setAttribute("aria-selected", on ? "true" : "false");
    });
    counts();
    try {
      var u = new URL(location.href);
      u.hash = TAB;
      history.replaceState({}, "", u.toString());
    } catch (e) {}
  }

  function bind() {
    HOST.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (!b) return;

      if (b.hasAttribute("data-tab")) { TAB = b.getAttribute("data-tab"); return paint(); }
      if (b.hasAttribute("data-folder")) { FOLDER = b.getAttribute("data-folder"); return paint(); }

      if (b.classList.contains("xr_ac_newfolder")) {
        var name = window.prompt(t("folderName"));
        if (!name) return;
        var f = Store.folders();
        f.__names = f.__names || [];
        if (f.__names.indexOf(name) < 0) f.__names.push(name);
        Store.setFolders(f);
        FOLDER = name;
        return paint();
      }
      if (b.hasAttribute("data-unfav")) {
        var id = b.getAttribute("data-unfav");
        Store.setFavorites(Store.favorites().filter(function (x) { return x !== id; }));
        var f2 = Store.folders(); delete f2[id]; Store.setFolders(f2);
        return paint();
      }
      if (b.hasAttribute("data-cmp")) {
        var c = Store.compare(), cid = b.getAttribute("data-cmp");
        if (c.indexOf(cid) < 0 && c.length < 4) c.push(cid);
        Store.setCompare(c);
        TAB = "compare";
        return paint();
      }
      if (b.hasAttribute("data-uncmp")) {
        var uid = b.getAttribute("data-uncmp");
        Store.setCompare(Store.compare().filter(function (x) { return x !== uid; }));
        return paint();
      }
      if (b.hasAttribute("data-alert")) {
        var s = Store.searches(), i = parseInt(b.getAttribute("data-alert"), 10);
        if (s[i]) { s[i].alert = !s[i].alert; s[i].freq = s[i].freq || "daily"; Store.setSearches(s); }
        return paint();
      }
      if (b.hasAttribute("data-delsearch")) {
        var s2 = Store.searches(); s2.splice(parseInt(b.getAttribute("data-delsearch"), 10), 1);
        Store.setSearches(s2);
        return paint();
      }
      if (b.classList.contains("xr_ac_clearviewed")) {
        try { localStorage.removeItem("xaru_viewed"); } catch (er) {}
        return paint();
      }
    });

    HOST.addEventListener("change", function (e) {
      var el = e.target;
      if (el.hasAttribute("data-move")) {
        var f = Store.folders();
        var id = el.getAttribute("data-move");
        if (el.value) f[id] = el.value; else delete f[id];
        Store.setFolders(f);
        return paint();
      }
      if (el.hasAttribute("data-freq")) {
        var s = Store.searches(), i = parseInt(el.getAttribute("data-freq"), 10);
        if (s[i]) { s[i].freq = el.value; Store.setSearches(s); }
      }
    });

    window.addEventListener("hashchange", function () {
      var h = location.hash.replace("#", "");
      if (["saved", "searches", "alerts", "viewed", "compare"].indexOf(h) >= 0) {
        TAB = h; paint();
      }
    });
  }

  HOST.innerHTML = '<p class="xr_dir_loading">' + esc(t("loading")) + "</p>";
  fetch(API + "search-index.json")
    .then(function (r) { return r.ok ? r.json() : { items: [] }; })
    .catch(function () { return { items: [] }; })
    .then(function (d) {
      IDX = d.items || [];
      IDX.forEach(function (x) { BY_ID[x.id] = x; });
      var h = location.hash.replace("#", "");
      if (["saved", "searches", "alerts", "viewed", "compare"].indexOf(h) >= 0) TAB = h;
      HOST.innerHTML = shell();
      bind();
      paint();
    });
})();
