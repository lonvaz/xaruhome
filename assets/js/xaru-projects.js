/*
 * XARU HOME — proyectos off-plan (Biblia §5.5)
 * =============================================================
 * Listado y ficha de proyecto. Lo que distingue a un off-plan de un activo
 * terminado no es la fotografía: es la entrega comprometida, el avance de obra
 * declarado y el plan de pago. Eso es lo que manda la ficha.
 *
 * Montaje:
 *   <div data-projects></div>                    listado
 *   <div data-project data-slug="…"></div>       ficha
 *
 * Origen: /data/api/v1/projects.json — la proyección de las tablas projects,
 * unit_types, payment_plans y payment_plan_milestones.
 */
(function () {
  "use strict";

  var LIST = document.querySelector("[data-projects]");
  var ONE = document.querySelector("[data-project]");
  var HOST = LIST || ONE;
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
    if (v == null) return "—";
    try {
      return new Intl.NumberFormat(loc4(),
        { style: "currency", currency: cur || "USD", maximumFractionDigits: 0 }).format(v);
    } catch (e) { return (cur || "USD") + " " + nf(v); }
  }

  var T = {
    handover:   {en:"Handover",es:"Entrega",ar:"التسليم",zh:"交付"},
    progress:   {en:"Construction progress",es:"Avance de obra",
                 ar:"نسبة الإنجاز",zh:"施工进度"},
    source:     {en:"Source",es:"Fuente",ar:"المصدر",zh:"来源"},
    developer:  {en:"Developer",es:"Promotora",ar:"المطوّر",zh:"开发商"},
    from:       {en:"From",es:"Desde",ar:"ابتداءً من",zh:"起价"},
    to:         {en:"to",es:"a",ar:"إلى",zh:"至"},
    units:      {en:"units",es:"unidades",ar:"وحدة",zh:"套"},
    available:  {en:"available",es:"disponibles",ar:"متاحة",zh:"可售"},
    unitTypes:  {en:"Unit types",es:"Tipos de unidad",ar:"أنواع الوحدات",zh:"户型"},
    unitName:   {en:"Type",es:"Tipo",ar:"النوع",zh:"户型"},
    beds:       {en:"Bedrooms",es:"Dormitorios",ar:"غرف النوم",zh:"卧室"},
    area:       {en:"Area",es:"Superficie",ar:"المساحة",zh:"面积"},
    priceFrom:  {en:"From",es:"Desde",ar:"من",zh:"起价"},
    plan:       {en:"Payment plan",es:"Plan de pago",ar:"خطة السداد",zh:"付款计划"},
    milestone:  {en:"Milestone",es:"Hito",ar:"المرحلة",zh:"节点"},
    percent:    {en:"Share",es:"Porcentaje",ar:"النسبة",zh:"比例"},
    trigger:    {en:"Triggered by",es:"Se activa con",ar:"يستحق عند",zh:"触发条件"},
    booking:    {en:"On reservation",es:"En la reserva",ar:"عند الحجز",zh:"预订时"},
    milestones: {en:"On construction milestones",es:"Contra hitos de obra",
                 ar:"وفق مراحل الإنجاز",zh:"按施工节点"},
    handoverT:  {en:"On handover",es:"En la entrega",ar:"عند التسليم",zh:"交付时"},
    post:       {en:"After handover",es:"Tras la entrega",ar:"بعد التسليم",zh:"交付后"},
    enquire:    {en:"Private enquiry",es:"Consulta reservada",ar:"استفسار خاص",zh:"私人咨询"},
    all:        {en:"All projects",es:"Todos los proyectos",ar:"كل المشاريع",zh:"全部项目"},
    anyDev:     {en:"Any developer",es:"Cualquier promotora",ar:"أي مطوّر",zh:"所有开发商"},
    projects:   {en:"projects",es:"proyectos",ar:"مشروع",zh:"个项目"},
    empty:      {en:"No projects match.",es:"Ningún proyecto coincide.",
                 ar:"لا مشاريع مطابقة.",zh:"没有符合条件的项目。"},
    loading:    {en:"Loading…",es:"Cargando…",ar:"جارٍ التحميل…",zh:"加载中…"},
    notFound:   {en:"This project is not available.",es:"Este proyecto no está disponible.",
                 ar:"هذا المشروع غير متاح.",zh:"该项目不可用。"},
    demoNote:   {en:"Sample project. Figures are illustrative until the developer file is loaded.",
                 es:"Proyecto de muestra. Las cifras son ilustrativas hasta que se cargue el expediente de la promotora.",
                 ar:"مشروع تجريبي. الأرقام إيضاحية إلى أن يُحمَّل ملف المطوّر.",
                 zh:"样例项目。在开发商档案载入前，各项数字仅供示意。"},
    escrowNote: {en:"Off-plan figures are those declared by the developer. Payment terms, escrow arrangements and delivery obligations are confirmed in the reservation documentation, not here.",
                 es:"Las cifras de off-plan son las declaradas por la promotora. Las condiciones de pago, el depósito en garantía y las obligaciones de entrega se confirman en la documentación de reserva, no aquí.",
                 ar:"أرقام البيع على المخطط هي ما يعلنه المطوّر. وتُثبَّت شروط السداد وحساب الضمان والتزامات التسليم في مستندات الحجز، لا هنا.",
                 zh:"期房数据均为开发商申报值。付款条件、监管账户安排与交付义务以预订文件为准，而非本页。"}
  };
  function t(k) { return (T[k] && (T[k][L] || T[k].en)) || k; }

  var TRIG = { booking: "booking", milestones: "milestones",
               handover: "handoverT", post_handover: "post" };

  var DATA = [];

  function card(p) {
    var href = PR + "real-estate/project/" + encodeURIComponent(p.slug) + "/";
    return '<a class="xr_prj_card" href="' + esc(href) + '">' +
      '<span class="xr_prj_top">' +
        "<strong>" + esc(p.name) + "</strong>" +
        "<em>" + esc(p.developer) + "</em>" +
      "</span>" +
      '<span class="xr_prj_bar" role="img" aria-label="' + esc(t("progress")) + " " +
        nf(p.progress) + '%"><i style="width:' + Math.max(2, Math.min(100, p.progress)) + '%"></i></span>' +
      '<span class="xr_prj_meta">' +
        "<b>" + esc(t("progress")) + " " + nf(p.progress) + "%</b>" +
        "<b>" + esc(t("handover")) + " Q" + p.handover.quarter + " " + p.handover.year + "</b>" +
      "</span>" +
      '<span class="xr_prj_price">' + esc(t("from")) + " " +
        esc(money(p.priceFrom, p.currency)) + " · " + nf(p.unitsAvailable) + "/" +
        nf(p.unitsTotal) + " " + esc(t("units")) + "</span>" +
    "</a>";
  }

  function list() {
    var devs = DATA.map(function (p) { return p.developer; })
      .filter(function (d, i, a) { return d && a.indexOf(d) === i; });
    HOST.innerHTML =
      '<div class="xr_dir_bar">' +
        '<select class="xr_prj_sel"><option value="">' + esc(t("anyDev")) + "</option>" +
        devs.map(function (d) {
          return '<option value="' + esc(d) + '">' + esc(d) + "</option>";
        }).join("") + "</select>" +
        '<span class="xr_dir_count"></span>' +
      "</div>" +
      '<div class="xr_prj_grid"></div>';

    function paint() {
      var sel = HOST.querySelector(".xr_prj_sel").value;
      var out = DATA.filter(function (p) { return !sel || p.developer === sel; })
        .sort(function (a, b) {
          return (a.handover.year - b.handover.year) || (a.handover.quarter - b.handover.quarter);
        });
      HOST.querySelector(".xr_dir_count").textContent = nf(out.length) + " " + t("projects");
      HOST.querySelector(".xr_prj_grid").innerHTML = out.length
        ? out.map(card).join("")
        : '<p class="xr_dir_empty">' + esc(t("empty")) + "</p>";
    }
    HOST.addEventListener("change", paint);
    paint();
  }

  function detail(slug) {
    var p = DATA.filter(function (x) { return x.slug === slug; })[0];
    if (!p) {
      HOST.innerHTML = '<p class="xr_dir_empty">' + esc(t("notFound")) + "</p>";
      return;
    }
    var devHref = PR + "real-estate/developer/" + encodeURIComponent(p.developerSlug) + "/";
    var units = (p.unitTypes || []).map(function (u) {
      var un = (u.nameI18n && (u.nameI18n[L] || u.nameI18n.en)) || u.name;
      return "<tr><td>" + esc(un) + "</td>" +
        "<td><bdi>" + (u.bedrooms ? nf(u.bedrooms) : "—") + "</bdi></td>" +
        "<td><bdi>" + nf(u.areaMin) + "–" + nf(u.areaMax) +
          (L === "ar" ? " م²" : " m²") + "</bdi></td>" +
        "<td><bdi>" + esc(money(u.priceFrom, p.currency)) + "</bdi></td></tr>";
    }).join("");

    var pl = p.paymentPlan || {};
    var miles = (pl.milestones || []).map(function (m) {
      var tk = TRIG[m.trigger_event] || m.trigger_event;
      return '<li class="xr_prj_mile">' +
        '<span class="xr_prj_mile_pct"><b>' + nf(m.percent) + "%</b>" +
          '<i style="width:' + Math.max(3, Math.min(100, m.percent)) + '%"></i></span>' +
        '<span class="xr_prj_mile_txt"><strong>' +
          esc((m.labelI18n && (m.labelI18n[L] || m.labelI18n.en)) || m.label) + "</strong>" +
          "<em>" + esc(t(tk)) + "</em></span></li>";
    }).join("");

    HOST.innerHTML =
      '<div class="xr_pf_head is-org">' +
        '<div class="xr_pf_id">' +
          '<p class="xr_pf_name">' + esc(p.name) + "</p>" +
          "<p>" + esc(t("developer")) + ': <a href="' + esc(devHref) + '">' +
            esc(p.developer) + "</a></p>" +
        "</div>" +
        '<div class="xr_pf_cta">' +
          '<a class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_10" href="' +
            PR + 'private-enquiry/"><span>' + esc(t("enquire")) + "</span></a>" +
        "</div>" +
      "</div>" +
      '<div class="xr_pf_stats">' +
        "<div><b>Q" + p.handover.quarter + " " + p.handover.year + "</b><span>" +
          esc(t("handover")) + "</span></div>" +
        "<div><b>" + nf(p.progress) + "%</b><span>" + esc(t("progress")) + "</span></div>" +
        "<div><b>" + esc(money(p.priceFrom, p.currency)) + "</b><span>" +
          esc(t("from")) + "</span></div>" +
        "<div><b>" + nf(p.unitsAvailable) + " / " + nf(p.unitsTotal) + "</b><span>" +
          esc(t("units")) + " " + esc(t("available")) + "</span></div>" +
      "</div>" +
      '<div class="xr_prj_progress">' +
        '<span class="xr_prj_bar"><i style="width:' +
          Math.max(2, Math.min(100, p.progress)) + '%"></i></span>' +
        '<p class="xr_prj_src">' + esc(t("source")) + ": " + esc(p.progressSource || "—") + "</p>" +
      "</div>" +
      (units ? '<h3 class="xr_pf_h">' + esc(t("unitTypes")) + "</h3>" +
        '<div class="xr_prj_tablewrap"><table class="xr_prj_table"><thead><tr>' +
          "<th>" + esc(t("unitName")) + "</th><th>" + esc(t("beds")) + "</th>" +
          "<th>" + esc(t("area")) + "</th><th>" + esc(t("priceFrom")) + "</th>" +
        "</tr></thead><tbody>" + units + "</tbody></table></div>" : "") +
      (miles ? '<h3 class="xr_pf_h">' + esc(t("plan")) +
        (pl.name ? ' <span class="xr_prj_planname">' + esc(pl.name) + "</span>" : "") + "</h3>" +
        '<ul class="xr_prj_miles">' + miles + "</ul>" : "") +
      '<p class="xr_prj_note">' + esc(t("escrowNote")) + "</p>" +
      (p.demo ? '<p class="xr_pf_demo">' + esc(t("demoNote")) + "</p>" : "");
  }

  HOST.innerHTML = '<p class="xr_dir_loading">' + esc(t("loading")) + "</p>";
  fetch(API + "projects.json")
    .then(function (r) { if (!r.ok) throw 0; return r.json(); })
    .then(function (d) {
      DATA = d.items || [];
      if (LIST) return list();
      detail(ONE.getAttribute("data-slug"));
    })
    .catch(function (err) {
      if (window.console) console.warn("[xaru-projects]", err);
      HOST.innerHTML = '<p class="xr_dir_empty">' + esc(t("notFound")) + "</p>";
    });
})();
