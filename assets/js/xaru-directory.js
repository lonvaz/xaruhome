/*
 * XARU HOME — directorios y perfiles
 * =============================================================
 * Biblia §5.6. Un mismo fichero cubre las dos caras porque son la misma
 * consulta vista a dos distancias: el directorio lista entidades, el perfil
 * abre una y muestra su cartera.
 *
 * Montaje:
 *   <div data-directory="agents|agencies|developers"></div>
 *   <div data-profile="agents|agencies|developers" data-slug="…"></div>
 *
 * Origen: /data/api/v1/agents.json, agencies.json, projects.json y
 * search-index.json — la proyección de la base de datos. El día que exista el
 * Directory Service, `load()` pasa a ser la llamada de red.
 */
(function () {
  "use strict";

  var DIR = document.querySelector("[data-directory]");
  var PRO = document.querySelector("[data-profile]");
  var HOST = DIR || PRO;
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
  function norm(s) {
    s = String(s || "").toLowerCase();
    try { s = s.normalize("NFD").replace(/[̀-ͯ]/g, ""); } catch (e) {}
    return s.trim();
  }

  var T = {
    agents:      {en:"Advisers",es:"Asesores",ar:"المستشارون",zh:"顾问"},
    agencies:    {en:"Offices",es:"Oficinas",ar:"المكاتب",zh:"分支机构"},
    developers:  {en:"Developers",es:"Promotoras",ar:"المطوّرون",zh:"开发商"},
    searchName:  {en:"Search by name",es:"Buscar por nombre",ar:"ابحث بالاسم",zh:"按名称搜索"},
    anyOffice:   {en:"Any office",es:"Cualquier oficina",ar:"أي مكتب",zh:"所有分支"},
    anyCountry:  {en:"Any country",es:"Cualquier país",ar:"أي دولة",zh:"所有国家"},
    listings:    {en:"assets",es:"activos",ar:"أصل",zh:"项资产"},
    verified:    {en:"Verified",es:"Verificado",ar:"موثّق",zh:"已核验"},
    licence:     {en:"Licence",es:"Licencia",ar:"الترخيص",zh:"执照"},
    languages:   {en:"Languages",es:"Idiomas",ar:"اللغات",zh:"语言"},
    specialities:{en:"Specialities",es:"Especialidades",ar:"التخصصات",zh:"专长"},
    areas:       {en:"Markets covered",es:"Plazas que cubre",ar:"الأسواق المغطاة",zh:"覆盖市场"},
    responds:    {en:"Typically responds in",es:"Responde normalmente en",
                  ar:"يستجيب عادةً خلال",zh:"通常回复时间"},
    minutes:     {en:"min",es:"min",ar:"دقيقة",zh:"分钟"},
    rating:      {en:"Rating",es:"Valoración",ar:"التقييم",zh:"评分"},
    reviews:     {en:"reviews",es:"valoraciones",ar:"تقييم",zh:"条评价"},
    portfolio:   {en:"Portfolio",es:"Cartera",ar:"المحفظة",zh:"资产组合"},
    seeAll:      {en:"See the full portfolio",es:"Ver la cartera completa",
                  ar:"عرض المحفظة كاملة",zh:"查看全部资产"},
    contact:     {en:"Private enquiry",es:"Consulta reservada",ar:"استفسار خاص",zh:"私人咨询"},
    team:        {en:"Advisers in this office",es:"Asesores de esta oficina",
                  ar:"مستشارو هذا المكتب",zh:"该分支的顾问"},
    projects:    {en:"Projects",es:"Proyectos",ar:"المشاريع",zh:"项目"},
    website:     {en:"Website",es:"Sitio web",ar:"الموقع",zh:"网站"},
    hq:          {en:"Head office",es:"Sede",ar:"المقر",zh:"总部"},
    poa:         {en:"Price upon application",es:"Precio a consulta",
                  ar:"السعر عند الطلب",zh:"价格面议"},
    empty:       {en:"Nothing matches this search.",es:"Nada coincide con esta búsqueda.",
                  ar:"لا شيء يطابق هذا البحث.",zh:"没有符合条件的结果。"},
    loading:     {en:"Loading…",es:"Cargando…",ar:"جارٍ التحميل…",zh:"加载中…"},
    error:       {en:"Could not be loaded.",es:"No se pudo cargar.",
                  ar:"تعذّر التحميل.",zh:"无法加载。"},
    notFound:    {en:"This profile is not available.",es:"Este perfil no está disponible.",
                  ar:"هذا الملف غير متاح.",zh:"该主页不可用。"},
    demoNote:    {en:"Platform demonstration record — the structure and workflow are the production ones; the entity is not.",
                  es:"Registro de demostración de la plataforma — la estructura y el flujo son los de producción; la entidad no.",
                  ar:"سجل تجريبي للمنصة — البنية وسير العمل هي الإنتاجية، أما الكيان فلا.",
                  zh:"平台演示记录——架构与流程均为正式环境，主体本身则非真实。"},
    handover:    {en:"Handover",es:"Entrega",ar:"التسليم",zh:"交付"},
    units:       {en:"units",es:"unidades",ar:"وحدة",zh:"套"},
    from:        {en:"From",es:"Desde",ar:"ابتداءً من",zh:"起价"}
  };
  function t(k) { return (T[k] && (T[k][L] || T[k].en)) || k; }

  /* Nombres legibles a partir de lo que ya publica la API. */
  var TYN = {}, CCN = {};
  function typeLabel(slug) { return TYN[slug] || slug; }
  function ccLabel(cc) { return CCN[cc] || cc; }

  var WIDTHS_BY_DIR = {
    "assets/img/xaru/catalog/": [480, 768, 1280, 1920, 2560],
    "assets/img/xaru/gen2/":    [768, 1280, 1920]
  };
  function picture(rel, alt, sizes) {
    rel = String(rel || "").replace(/^\//, "");
    var m = /^(.*\/)([^\/]+)\.jpg$/.exec(rel);
    if (!m || !WIDTHS_BY_DIR[m[1]]) {
      return '<img src="' + esc(R + rel) + '" alt="' + esc(alt) + '" loading="lazy">';
    }
    var dir = m[1] + "r/", base = m[2], w = WIDTHS_BY_DIR[m[1]];
    function set(ext) {
      return w.map(function (x) { return R + dir + base + "-" + x + "." + ext + " " + x + "w"; }).join(", ");
    }
    return "<picture>" +
      '<source type="image/avif" srcset="' + esc(set("avif")) + '" sizes="' + sizes + '">' +
      '<source type="image/webp" srcset="' + esc(set("webp")) + '" sizes="' + sizes + '">' +
      '<img src="' + esc(R + dir + base + "-768.jpg") + '" alt="' + esc(alt) +
      '" loading="lazy" decoding="async"></picture>';
  }

  /* Iniciales: no hay retrato de cada asesor y una silueta genérica repetida
     veintidós veces se ve peor que un monograma. */
  function monogram(name) {
    var p = String(name || "").replace(/[^\p{L}\s.]/gu, "").split(/[\s.]+/).filter(Boolean);
    var s = (p[0] || "").charAt(0) + (p.length > 1 ? p[p.length - 1].charAt(0) : "");
    return esc(s.toUpperCase());
  }

  var DATA = { agents: [], orgs: [], projects: [], index: [] };

  /* ---------------------------------------------------------------- tarjetas */
  function agentCard(a) {
    var href = PR + "real-estate/agent/" + encodeURIComponent(a.slug) + "/";
    return '<a class="xr_dir_card is-agent" href="' + esc(href) + '">' +
      '<span class="xr_dir_avatar">' + monogram(a.name) + "</span>" +
      '<span class="xr_dir_body">' +
        '<strong>' + esc(a.name) + (a.verified ?
          ' <i class="fa-solid fa-circle-check" aria-hidden="true"></i>' : "") + "</strong>" +
        "<em>" + esc(a.agency || "") + "</em>" +
        '<b>' + nf(a.listings) + " " + esc(t("listings")) + "</b>" +
      "</span></a>";
  }
  function orgCard(o) {
    var kind = o.kind === "developer" ? "developer" : "agency";
    var href = PR + "real-estate/" + (kind === "developer" ? "developer" : "agency") +
      "/" + encodeURIComponent(o.slug) + "/";
    var place = [o.city, ccLabel(o.country)].filter(Boolean).join(", ");
    return '<a class="xr_dir_card is-org" href="' + esc(href) + '">' +
      '<span class="xr_dir_body">' +
        "<strong>" + esc(o.name) + (o.verified ?
          ' <i class="fa-solid fa-circle-check" aria-hidden="true"></i>' : "") + "</strong>" +
        "<em>" + esc(place) + "</em>" +
        "<b>" + nf(o.listings) + " " + esc(t("listings")) + "</b>" +
      "</span></a>";
  }

  /* ---------------------------------------------------------------- directorio */
  function directory(kind) {
    var items = kind === "agents" ? DATA.agents
      : DATA.orgs.filter(function (o) {
          return kind === "developers" ? o.kind === "developer" : o.kind === "agency";
        });

    HOST.innerHTML =
      '<div class="xr_dir_bar">' +
        '<input type="search" class="xr_dir_q" placeholder="' + esc(t("searchName")) + '" ' +
          'aria-label="' + esc(t("searchName")) + '">' +
        (kind === "agents"
          ? '<select class="xr_dir_sel"><option value="">' + esc(t("anyOffice")) + "</option>" +
            DATA.orgs.filter(function (o) { return o.kind === "agency"; })
              .map(function (o) {
                return '<option value="' + esc(o.slug) + '">' + esc(o.name) + "</option>";
              }).join("") + "</select>"
          : '<select class="xr_dir_sel"><option value="">' + esc(t("anyCountry")) + "</option>" +
            items.map(function (o) { return o.country; })
              .filter(function (c, i, a) { return c && a.indexOf(c) === i; })
              .map(function (c) {
                return '<option value="' + esc(c) + '">' + esc(ccLabel(c)) + "</option>";
              }).join("") + "</select>") +
        '<span class="xr_dir_count"></span>' +
      "</div>" +
      '<div class="xr_dir_grid"></div>';

    function paint() {
      var q = norm(HOST.querySelector(".xr_dir_q").value);
      var sel = HOST.querySelector(".xr_dir_sel").value;
      var out = items.filter(function (x) {
        if (q && norm(x.name).indexOf(q) < 0) return false;
        if (sel) {
          if (kind === "agents" && x.agencySlug !== sel) return false;
          if (kind !== "agents" && x.country !== sel) return false;
        }
        return true;
      }).sort(function (a, b) { return b.listings - a.listings; });

      HOST.querySelector(".xr_dir_count").textContent =
        nf(out.length) + " " + t(kind).toLowerCase();
      HOST.querySelector(".xr_dir_grid").innerHTML = out.length
        ? out.map(kind === "agents" ? agentCard : orgCard).join("")
        : '<p class="xr_dir_empty">' + esc(t("empty")) + "</p>";
    }
    HOST.addEventListener("input", paint);
    HOST.addEventListener("change", paint);
    paint();
  }

  /* ---------------------------------------------------------------- perfil */
  function listingStrip(items, moreHref) {
    if (!items.length) return "";
    return '<h3 class="xr_pf_h">' + esc(t("portfolio")) + "</h3>" +
      '<div class="xr_pf_grid">' +
      items.slice(0, 6).map(function (x) {
        var title = x.t[L] || x.t.en;
        var href = PR + "property-details.html?id=" + encodeURIComponent(x.id);
        return '<a class="xr_pf_card" href="' + esc(href) + '">' +
          '<span class="xr_pf_img">' +
            picture(x.img, title, "(max-width:767px) 92vw, 320px") + "</span>" +
          "<strong>" + esc(title) + "</strong>" +
          "<em>" + esc([x.city, ccLabel(x.cc)].filter(Boolean).join(", ")) + "</em>" +
          "<b>" + esc(x.poa || x.p == null ? t("poa") : money(x.p, x.cur)) + "</b></a>";
      }).join("") + "</div>" +
      (items.length > 6
        ? '<a class="xr_link xr_pf_more" href="' + esc(moreHref) + '">' +
          esc(t("seeAll")) + '<i class="fa-solid fa-angle-right"></i></a>'
        : "");
  }

  function chipList(label, values, mapFn) {
    if (!values || !values.length) return "";
    return '<div class="xr_pf_row"><span>' + esc(label) + "</span><p>" +
      values.map(function (v) {
        return '<span class="xr_pf_chip">' + esc(mapFn ? mapFn(v) : v) + "</span>";
      }).join("") + "</p></div>";
  }

  function agentProfile(slug) {
    var a = DATA.agents.filter(function (x) { return x.slug === slug; })[0];
    if (!a) return null;
    var mine = DATA.index.filter(function (x) { return x.ag === slug; });
    var more = PR + "real-estate/search/?ag=" + encodeURIComponent(slug);
    return '<div class="xr_pf_head">' +
        '<span class="xr_pf_avatar">' + monogram(a.name) + "</span>" +
        '<div class="xr_pf_id">' +
          '<p class="xr_pf_name">' + esc(a.name) + (a.verified ?
            ' <i class="fa-solid fa-circle-check" title="' + esc(t("verified")) + '"></i>' : "") + "</p>" +
          "<p>" + esc(a.title || "") +
            (a.agency ? " · " + '<a href="' + PR + "real-estate/agency/" +
              encodeURIComponent(a.agencySlug) + '/">' + esc(a.agency) + "</a>" : "") + "</p>" +
          '<p class="xr_pf_lic">' + esc(t("licence")) + " " + esc(a.licence || "") + "</p>" +
        "</div>" +
        '<div class="xr_pf_cta">' +
          '<a class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_10" href="' +
            PR + 'private-enquiry/"><span>' + esc(t("contact")) + "</span></a>" +
        "</div>" +
      "</div>" +
      '<div class="xr_pf_stats">' +
        '<div><b>' + nf(a.listings) + "</b><span>" + esc(t("listings")) + "</span></div>" +
        (a.rating ? '<div><b>' + nf(a.rating) + "</b><span>" + esc(t("rating")) +
          " · " + nf(a.ratingCount) + " " + esc(t("reviews")) + "</span></div>" : "") +
        (a.responseMinutes ? '<div><b>' + nf(a.responseMinutes) + " " + esc(t("minutes")) +
          "</b><span>" + esc(t("responds")) + "</span></div>" : "") +
      "</div>" +
      '<div class="xr_pf_facts">' +
        chipList(t("languages"), a.languages, function (v) { return v.toUpperCase(); }) +
        chipList(t("specialities"), a.specialities, typeLabel) +
        chipList(t("areas"), a.serviceAreas, ccLabel) +
      "</div>" +
      (a.demo ? '<p class="xr_pf_demo">' + esc(t("demoNote")) + "</p>" : "") +
      listingStrip(mine, more);
  }

  function orgProfile(slug, kind) {
    var o = DATA.orgs.filter(function (x) { return x.slug === slug; })[0];
    if (!o) return null;
    var mine = DATA.index.filter(function (x) { return x.og === slug; });
    var more = PR + "real-estate/search/?og=" + encodeURIComponent(slug);
    var team = DATA.agents.filter(function (x) { return x.agencySlug === slug; });
    var projs = DATA.projects.filter(function (p) { return p.developerSlug === slug; });
    var place = [o.city, ccLabel(o.country)].filter(Boolean).join(", ");

    return '<div class="xr_pf_head is-org">' +
        '<div class="xr_pf_id">' +
          '<p class="xr_pf_name">' + esc(o.name) + (o.verified ?
            ' <i class="fa-solid fa-circle-check" title="' + esc(t("verified")) + '"></i>' : "") + "</p>" +
          "<p>" + esc(o.legalName || "") + "</p>" +
          '<p class="xr_pf_lic">' + esc(t("licence")) + " " + esc(o.licence || "") + "</p>" +
        "</div>" +
        '<div class="xr_pf_cta">' +
          '<a class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_10" href="' +
            PR + 'private-enquiry/"><span>' + esc(t("contact")) + "</span></a>" +
        "</div>" +
      "</div>" +
      (o.description ? '<p class="xr_pf_bio">' + esc(o.description) + "</p>" : "") +
      '<div class="xr_pf_stats">' +
        '<div><b>' + nf(o.listings) + "</b><span>" + esc(t("listings")) + "</span></div>" +
        (place ? '<div><b>' + esc(place) + "</b><span>" + esc(t("hq")) + "</span></div>" : "") +
        (team.length ? '<div><b>' + nf(team.length) + "</b><span>" +
          esc(t("agents")) + "</span></div>" : "") +
        (projs.length ? '<div><b>' + nf(projs.length) + "</b><span>" +
          esc(t("projects")) + "</span></div>" : "") +
      "</div>" +
      (o.demo ? '<p class="xr_pf_demo">' + esc(t("demoNote")) + "</p>" : "") +
      (projs.length ? '<h3 class="xr_pf_h">' + esc(t("projects")) + "</h3>" +
        '<div class="xr_pf_projects">' + projs.map(function (p) {
          return '<a class="xr_pf_proj" href="' + PR + "real-estate/project/" +
            encodeURIComponent(p.slug) + '/">' +
            "<strong>" + esc(p.name) + "</strong>" +
            "<em>" + esc(t("handover")) + " Q" + p.handover.quarter + " " + p.handover.year + "</em>" +
            "<b>" + esc(t("from")) + " " + esc(money(p.priceFrom, p.currency)) + " · " +
            nf(p.unitsAvailable) + "/" + nf(p.unitsTotal) + " " + esc(t("units")) + "</b></a>";
        }).join("") + "</div>" : "") +
      listingStrip(mine, more) +
      (team.length ? '<h3 class="xr_pf_h">' + esc(t("team")) + "</h3>" +
        '<div class="xr_dir_grid">' + team.map(agentCard).join("") + "</div>" : "");
  }

  /* ---------------------------------------------------------------- carga */
  HOST.innerHTML = '<p class="xr_dir_loading">' + esc(t("loading")) + "</p>";

  Promise.all([
    fetch(API + "agents.json").then(function (r) { return r.ok ? r.json() : { items: [] }; }),
    fetch(API + "agencies.json").then(function (r) { return r.ok ? r.json() : { items: [] }; }),
    fetch(API + "projects.json").then(function (r) { return r.ok ? r.json() : { items: [] }; }),
    fetch(API + "search-index.json").then(function (r) { return r.ok ? r.json() : { items: [] }; }),
    fetch(API + "locations.json").then(function (r) { return r.ok ? r.json() : { countries: [] }; })
  ]).then(function (o) {
    DATA.agents = o[0].items || [];
    DATA.orgs = o[1].items || [];
    DATA.projects = o[2].items || [];
    DATA.index = o[3].items || [];
    (o[4].countries || []).forEach(function (c) { CCN[c.code] = c.name[L] || c.name.en; });
    DATA.index.forEach(function (x) {
      if (x.typeName) TYN[x.type] = x.typeName[L] || x.typeName.en;
    });

    if (DIR) return directory(DIR.getAttribute("data-directory"));

    var kind = PRO.getAttribute("data-profile");
    var slug = PRO.getAttribute("data-slug");
    var html = kind === "agents" ? agentProfile(slug) : orgProfile(slug, kind);
    if (!html) {
      HOST.innerHTML = '<p class="xr_dir_empty">' + esc(t("notFound")) + "</p>";
      return;
    }
    HOST.innerHTML = html;
  }).catch(function (err) {
    if (window.console) console.warn("[xaru-directory]", err);
    HOST.innerHTML = '<p class="xr_dir_empty">' + esc(t("error")) + "</p>";
  });
})();
