/*
 * XARU HOME — consolas de operación (Biblia §5.8 y §5.9)
 * =============================================================
 * Dos paneles sobre la misma proyección: el de oficina (B2B) y el de
 * administración. Un solo fichero porque comparten la tabla, las pestañas y el
 * mismo criterio: enseñar la operación tal como será, sin fingir que se
 * ejecuta.
 *
 * QUÉ HACE Y QUÉ NO
 * -----------------
 * Muestra inventario por estado, cartera de leads con su SLA, consumo de
 * créditos, cuota del plan, cola de moderación con su regla incumplida y las
 * transiciones del ciclo de vida. Lo que NO hace es decidir: aprobar, rechazar
 * o suspender exige identidad y traza de auditoría, y una decisión sin traza
 * no se simula. Los botones de decisión aparecen desactivados con el motivo a
 * la vista, que es más honesto que ocultarlos.
 *
 * El asistente de alta (§8) recorre sus diez pasos y valida en cada uno, pero
 * termina en un resumen del registro que se crearía, no en un alta: escribir
 * en el inventario sin servidor sería escribir en el navegador de quien mire.
 *
 * Montaje: <div data-console="b2b"></div> · <div data-console="admin"></div>
 */
(function () {
  "use strict";

  var HOST = document.querySelector("[data-console]");
  if (!HOST) return;
  var MODE = HOST.getAttribute("data-console");

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
  function when(iso) {
    if (!iso) return "—";
    try {
      return new Intl.DateTimeFormat(loc4(),
        { year: "numeric", month: "short", day: "numeric" }).format(new Date(iso));
    } catch (e) { return String(iso).slice(0, 10); }
  }
  function overdue(iso) {
    if (!iso) return false;
    try { return new Date(iso).getTime() < Date.now(); } catch (e) { return false; }
  }

  var T = {
    /* comunes */
    office:     {en:"Office",es:"Oficina",ar:"المكتب",zh:"分支机构"},
    inventory:  {en:"Inventory",es:"Inventario",ar:"المعروض",zh:"资产"},
    pipeline:   {en:"Pipeline",es:"Pipeline",ar:"مسار الصفقات",zh:"销售漏斗"},
    billing:    {en:"Plan & credits",es:"Plan y créditos",ar:"الخطة والأرصدة",zh:"套餐与额度"},
    newListing: {en:"New listing",es:"Alta de activo",ar:"إدراج جديد",zh:"新建房源"},
    queue:      {en:"Moderation queue",es:"Cola de moderación",ar:"قائمة المراجعة",zh:"审核队列"},
    lifecycle:  {en:"Lifecycle",es:"Ciclo de vida",ar:"دورة الحياة",zh:"生命周期"},
    taxonomy:   {en:"Taxonomies",es:"Taxonomías",ar:"التصنيفات",zh:"分类体系"},
    activity:   {en:"Activity",es:"Actividad",ar:"النشاط",zh:"活动记录"},
    total:      {en:"Total",es:"Total",ar:"الإجمالي",zh:"总计"},
    state:      {en:"State",es:"Estado",ar:"الحالة",zh:"状态"},
    count:      {en:"Records",es:"Registros",ar:"سجلات",zh:"记录数"},
    quota:      {en:"Quota",es:"Cuota",ar:"الحصة",zh:"配额"},
    used:       {en:"used",es:"usada",ar:"مستخدَم",zh:"已用"},
    stage:      {en:"Stage",es:"Etapa",ar:"المرحلة",zh:"阶段"},
    contact:    {en:"Contact",es:"Contacto",ar:"جهة الاتصال",zh:"联系人"},
    channel:    {en:"Channel",es:"Canal",ar:"القناة",zh:"渠道"},
    budget:     {en:"Budget",es:"Presupuesto",ar:"الميزانية",zh:"预算"},
    sla:        {en:"SLA",es:"SLA",ar:"مهلة الاستجابة",zh:"响应时限"},
    overdueL:   {en:"Overdue",es:"Vencido",ar:"متأخر",zh:"已逾期"},
    created:    {en:"Created",es:"Creado",ar:"تاريخ الإنشاء",zh:"创建时间"},
    plan:       {en:"Plan",es:"Plan",ar:"الخطة",zh:"套餐"},
    renews:     {en:"Renews",es:"Renueva",ar:"يتجدد",zh:"续订"},
    seats:      {en:"Seats",es:"Puestos",ar:"المقاعد",zh:"席位"},
    features:   {en:"Includes",es:"Incluye",ar:"يشمل",zh:"包含"},
    balance:    {en:"Credit balance",es:"Saldo de créditos",ar:"رصيد الأرصدة",zh:"额度余额"},
    ledger:     {en:"Ledger",es:"Movimientos",ar:"سجل الحركات",zh:"流水"},
    entry:      {en:"Entry",es:"Concepto",ar:"البند",zh:"项目"},
    credits:    {en:"Credits",es:"Créditos",ar:"الأرصدة",zh:"额度"},
    listing:    {en:"Listing",es:"Activo",ar:"العرض",zh:"房源"},
    risk:       {en:"Risk",es:"Riesgo",ar:"المخاطر",zh:"风险"},
    rules:      {en:"Failed rules",es:"Reglas incumplidas",ar:"القواعد المخالفة",zh:"未通过规则"},
    assignee:   {en:"Assignee",es:"Asignado a",ar:"المُسنَد إليه",zh:"负责人"},
    unassigned: {en:"Unassigned",es:"Sin asignar",ar:"غير مُسنَد",zh:"未分配"},
    approve:    {en:"Approve",es:"Aprobar",ar:"اعتماد",zh:"通过"},
    reject:     {en:"Reject",es:"Rechazar",ar:"رفض",zh:"驳回"},
    from:       {en:"From",es:"De",ar:"من",zh:"由"},
    to:         {en:"To",es:"A",ar:"إلى",zh:"至"},
    actor:      {en:"Actor",es:"Actor",ar:"المنفّذ",zh:"操作者"},
    at:         {en:"When",es:"Cuándo",ar:"متى",zh:"时间"},
    types:      {en:"Property types",es:"Tipologías",ar:"أنواع العقارات",zh:"物业类型"},
    amenities:  {en:"Amenities",es:"Amenidades",ar:"المرافق",zh:"设施"},
    countries:  {en:"Countries",es:"Países",ar:"الدول",zh:"国家"},
    cities:     {en:"Cities",es:"Ciudades",ar:"المدن",zh:"城市"},
    all:        {en:"All",es:"Todos",ar:"الكل",zh:"全部"},
    filterSt:   {en:"Any status",es:"Cualquier estado",ar:"أي حالة",zh:"所有状态"},
    loading:    {en:"Loading…",es:"Cargando…",ar:"جارٍ التحميل…",zh:"加载中…"},
    empty:      {en:"Nothing here.",es:"Nada aquí.",ar:"لا شيء هنا.",zh:"暂无内容。"},
    readOnly:   {en:"Read-only in simulation. Approving, rejecting or suspending requires an authenticated identity and an audit trail; a decision without a trail is not something to simulate.",
                 es:"Solo lectura en simulación. Aprobar, rechazar o suspender exige identidad autenticada y traza de auditoría; una decisión sin traza no es algo que se deba simular.",
                 ar:"للقراءة فقط في وضع المحاكاة. الاعتماد أو الرفض أو التعليق يتطلب هوية موثّقة وأثر تدقيق؛ والقرار دون أثر ليس مما يُحاكى.",
                 zh:"模拟模式下为只读。通过、驳回或暂停均需经认证的身份与审计轨迹；无轨迹的决定不应被模拟。"},
    maskNote:   {en:"Contact details are masked in this projection, exactly as they will be in the production panel for anyone without the lead assigned.",
                 es:"Los datos de contacto van enmascarados en esta proyección, igual que estarán en el panel de producción para quien no tenga el lead asignado.",
                 ar:"بيانات الاتصال مُقنَّعة في هذه الإسقاطة، تماماً كما ستكون في لوحة الإنتاج لمن ليس العميل المحتمل مُسنَداً إليه.",
                 zh:"本投影中联系方式已脱敏，与正式面板中未获分配该线索者所见完全一致。"},
    /* asistente §8 */
    wizard:     {en:"Listing wizard",es:"Asistente de alta",ar:"معالج الإدراج",zh:"房源发布向导"},
    step:       {en:"Step",es:"Paso",ar:"الخطوة",zh:"步骤"},
    of:         {en:"of",es:"de",ar:"من",zh:"/"},
    next:       {en:"Next",es:"Siguiente",ar:"التالي",zh:"下一步"},
    back:       {en:"Back",es:"Atrás",ar:"السابق",zh:"上一步"},
    finish:     {en:"Review summary",es:"Ver el resumen",ar:"عرض الملخّص",zh:"查看摘要"},
    required:   {en:"This step needs an answer before you can continue.",
                 es:"Este paso necesita una respuesta antes de continuar.",
                 ar:"تحتاج هذه الخطوة إلى إجابة قبل المتابعة.",
                 zh:"需先填写本步骤才能继续。"},
    summary:    {en:"What would be created",es:"Lo que se crearía",
                 ar:"ما سيتم إنشاؤه",zh:"将创建的记录"},
    wizardNote: {en:"The wizard validates every step and ends in the record that would be created. It stops there: writing to the inventory without a server would only write into the browser of whoever is looking.",
                 es:"El asistente valida cada paso y termina en el registro que se crearía. Ahí se detiene: escribir en el inventario sin servidor sería escribir solo en el navegador de quien mire.",
                 ar:"يتحقّق المعالج من كل خطوة وينتهي إلى السجل الذي سيُنشأ. ويتوقف هناك: الكتابة في المعروض دون خادم لن تتعدى متصفح من ينظر.",
                 zh:"向导会逐步校验，并以将要创建的记录收尾。到此为止：没有服务端，写入资产库只会写进当下浏览者的浏览器。"},
    restart:    {en:"Start again",es:"Empezar de nuevo",ar:"البدء من جديد",zh:"重新开始"}
  };
  function t(k) { return (T[k] && (T[k][L] || T[k].en)) || k; }

  var STATE_L = {
    DRAFT:            {en:"Draft",es:"Borrador",ar:"مسودة",zh:"草稿"},
    INCOMPLETE:       {en:"Incomplete",es:"Incompleto",ar:"غير مكتمل",zh:"未完成"},
    SUBMITTED:        {en:"Submitted",es:"Enviado",ar:"مُرسَل",zh:"已提交"},
    AUTOMATED_REVIEW: {en:"Automated review",es:"Revisión automática",
                       ar:"مراجعة آلية",zh:"自动审核"},
    HUMAN_REVIEW:     {en:"Human review",es:"Revisión humana",ar:"مراجعة بشرية",zh:"人工审核"},
    CHANGES_REQUESTED:{en:"Changes requested",es:"Cambios solicitados",
                       ar:"مطلوب تعديلات",zh:"待修改"},
    APPROVED:         {en:"Approved",es:"Aprobado",ar:"معتمد",zh:"已通过"},
    SCHEDULED:        {en:"Scheduled",es:"Programado",ar:"مجدول",zh:"已排期"},
    PUBLISHED:        {en:"Published",es:"Publicado",ar:"منشور",zh:"已发布"},
    PAUSED:           {en:"Paused",es:"Pausado",ar:"موقوف مؤقتاً",zh:"已暂停"},
    UNDER_OFFER:      {en:"Under offer",es:"En negociación",ar:"قيد التفاوض",zh:"洽谈中"},
    REJECTED:         {en:"Rejected",es:"Rechazado",ar:"مرفوض",zh:"已驳回"},
    SUSPENDED:        {en:"Suspended",es:"Suspendido",ar:"معلَّق",zh:"已停用"},
    EXPIRED:          {en:"Expired",es:"Caducado",ar:"منتهي",zh:"已过期"},
    SOLD:             {en:"Sold",es:"Vendido",ar:"مُباع",zh:"已售"},
    RENTED:           {en:"Rented",es:"Alquilado",ar:"مؤجَّر",zh:"已租"},
    ARCHIVED:         {en:"Archived",es:"Archivado",ar:"مؤرشف",zh:"已归档"}
  };
  function stateL(k) { return (STATE_L[k] && (STATE_L[k][L] || STATE_L[k].en)) || k; }

  var STAGE_L = {
    new:       {en:"New",es:"Nuevo",ar:"جديد",zh:"新线索"},
    contacted: {en:"Contacted",es:"Contactado",ar:"تم التواصل",zh:"已联系"},
    qualified: {en:"Qualified",es:"Cualificado",ar:"مؤهَّل",zh:"已确认意向"},
    viewing:   {en:"Viewing",es:"Visita",ar:"معاينة",zh:"看房"},
    offer:     {en:"Offer",es:"Oferta",ar:"عرض",zh:"报价"},
    won:       {en:"Won",es:"Ganado",ar:"مكسوب",zh:"成交"},
    lost:      {en:"Lost",es:"Perdido",ar:"مفقود",zh:"流失"}
  };
  function stageL(k) { return (STAGE_L[k] && (STAGE_L[k][L] || STAGE_L[k].en)) || k; }

  var RULE_L = {
    photo_quality:  {en:"Photo quality",es:"Calidad de foto",ar:"جودة الصور",zh:"图片质量"},
    duplicate_check:{en:"Duplicate",es:"Duplicado",ar:"تكرار",zh:"重复房源"},
    price_outlier:  {en:"Price outlier",es:"Precio atípico",ar:"سعر شاذ",zh:"价格异常"},
    permit_missing: {en:"Permit missing",es:"Falta permiso",ar:"تصريح ناقص",zh:"缺少许可"}
  };
  function ruleL(k) { return (RULE_L[k] && (RULE_L[k][L] || RULE_L[k].en)) || k; }

  var B2B = null, ADMIN = null, ORG = 0, TAB = "";

  function tabs(list) {
    return '<div class="xr_cs_tabs" role="tablist">' + list.map(function (x) {
      return '<button type="button" role="tab" data-tab="' + x[0] + '"' +
        (x[0] === TAB ? ' class="is-on" aria-selected="true"' : ' aria-selected="false"') +
        ">" + esc(x[1]) + "</button>";
    }).join("") + "</div>";
  }
  function table(head, rows) {
    if (!rows.length) return '<p class="xr_cs_empty">' + esc(t("empty")) + "</p>";
    return '<div class="xr_cs_tablewrap"><table class="xr_cs_table"><thead><tr>' +
      head.map(function (h) { return "<th>" + esc(h) + "</th>"; }).join("") +
      "</tr></thead><tbody>" + rows.join("") + "</tbody></table></div>";
  }
  function pill(cls, txt) { return '<span class="xr_cs_pill is-' + cls + '">' + esc(txt) + "</span>"; }

  /* ================================================================ B2B */
  function b2bInventory(o) {
    var order = ["PUBLISHED", "HUMAN_REVIEW", "AUTOMATED_REVIEW", "DRAFT",
                 "PAUSED", "REJECTED", "EXPIRED"];
    var keys = Object.keys(o.inventoryByState).sort(function (a, b) {
      var ia = order.indexOf(a), ib = order.indexOf(b);
      return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib);
    });
    var used = o.inventoryTotal, quota = o.quota || 0;
    var pct = quota ? Math.min(100, Math.round(used * 100 / quota)) : 0;
    return '<div class="xr_cs_kpis">' +
        "<div><b>" + nf(used) + "</b><span>" + esc(t("inventory")) + "</span></div>" +
        "<div><b>" + nf(quota) + "</b><span>" + esc(t("quota")) + "</span></div>" +
        "<div><b>" + nf(pct) + "%</b><span>" + esc(t("used")) + "</span></div>" +
      "</div>" +
      '<div class="xr_cs_meter"><i style="width:' + pct + '%"></i></div>' +
      table([t("state"), t("count")], keys.map(function (k) {
        return "<tr><td>" + pill(k.toLowerCase().replace(/_/g, "-"), stateL(k)) +
          "</td><td><bdi>" + nf(o.inventoryByState[k]) + "</bdi></td></tr>";
      }));
  }

  function b2bPipeline(o) {
    var stages = (B2B && B2B.stages) || [];
    var cols = stages.map(function (st) {
      var n = o.leadsByStage[st] || 0;
      return '<div class="xr_cs_stage"><b>' + nf(n) + "</b><span>" + esc(stageL(st)) + "</span></div>";
    }).join("");
    var rows = o.leads.map(function (l) {
      var od = overdue(l.slaDueAt) && !l.firstResponseAt;
      return "<tr>" +
        "<td>" + esc(l.name || "—") + '<span class="xr_cs_sub">' + esc(l.email) +
          " · " + esc(l.phone) + "</span></td>" +
        "<td>" + pill("stage", stageL(l.stage)) + "</td>" +
        "<td>" + esc(l.channel || "—") + "</td>" +
        "<td><bdi>" + (l.budgetMin ? money(l.budgetMin, l.currency) + " – " +
          money(l.budgetMax, l.currency) : "—") + "</bdi></td>" +
        "<td>" + (od ? pill("late", t("overdueL")) : esc(when(l.slaDueAt))) + "</td>" +
        "<td>" + esc(when(l.createdAt)) + "</td>" +
      "</tr>";
    });
    return '<div class="xr_cs_pipeline">' + cols + "</div>" +
      table([t("contact"), t("stage"), t("channel"), t("budget"), t("sla"), t("created")], rows) +
      '<p class="xr_cs_note">' + esc(t("maskNote")) + "</p>";
  }

  function b2bBilling(o) {
    var p = o.plan || {};
    return '<div class="xr_cs_kpis">' +
        "<div><b>" + esc(p.name || "—") + "</b><span>" + esc(t("plan")) + "</span></div>" +
        "<div><b>" + esc(money(p.priceMonthly, p.currency)) + "</b><span>" +
          esc(t("plan")) + "</span></div>" +
        "<div><b>" + nf(o.creditBalance) + "</b><span>" + esc(t("balance")) + "</span></div>" +
        "<div><b>" + esc(when(p.renewsAt)) + "</b><span>" + esc(t("renews")) + "</span></div>" +
        "<div><b>" + nf(p.seats || 0) + "</b><span>" + esc(t("seats")) + "</span></div>" +
      "</div>" +
      ((p.features || []).length
        ? '<div class="xr_pf_row"><span>' + esc(t("features")) + "</span><p>" +
          p.features.map(function (f) {
            return '<span class="xr_pf_chip">' + esc(f) + "</span>";
          }).join("") + "</p></div>"
        : "") +
      '<h4 class="xr_cs_h">' + esc(t("ledger")) + "</h4>" +
      table([t("entry"), t("credits"), t("at")], (o.credits || []).map(function (c) {
        return "<tr><td>" + esc(c.type) + "</td><td><bdi>" +
          (c.credits > 0 ? "+" : "") + nf(c.credits) + "</bdi></td><td>" +
          esc(when(c.at)) + "</td></tr>";
      }));
  }

  /* --------------------------------------------------- asistente de alta §8 */
  var WSTEPS = [
    { k: "offering", q: {en:"Operation",es:"Operación",ar:"نوع العملية",zh:"交易方式"},
      opts: [["sale", {en:"For sale",es:"Venta",ar:"للبيع",zh:"出售"}],
             ["rent", {en:"To rent",es:"Alquiler",ar:"للإيجار",zh:"租赁"}]] },
    { k: "category", q: {en:"Category",es:"Categoría",ar:"الفئة",zh:"类别"},
      opts: [["residential", {en:"Residential",es:"Residencial",ar:"سكني",zh:"住宅"}],
             ["commercial", {en:"Commercial",es:"Comercial",ar:"تجاري",zh:"商业"}],
             ["land", {en:"Land",es:"Suelo",ar:"أرض",zh:"土地"}]] },
    { k: "type", q: {en:"Property type",es:"Tipología",ar:"نوع العقار",zh:"物业类型"}, dyn: "type" },
    { k: "country", q: {en:"Country",es:"País",ar:"الدولة",zh:"国家"}, dyn: "country" },
    { k: "city", q: {en:"City",es:"Ciudad",ar:"المدينة",zh:"城市"}, dyn: "city" },
    { k: "spaces", q: {en:"Bedrooms and built area",es:"Dormitorios y superficie",
                       ar:"غرف النوم والمساحة",zh:"卧室与建筑面积"}, num: ["bedrooms", "sqm"] },
    { k: "price", q: {en:"Asking price",es:"Precio de salida",ar:"السعر المطلوب",zh:"要价"},
      num: ["amount"] },
    { k: "media", q: {en:"Photography",es:"Fotografía",ar:"التصوير",zh:"图片"},
      opts: [["ready", {en:"Professional set ready",es:"Reportaje profesional listo",
                        ar:"جلسة تصوير احترافية جاهزة",zh:"已有专业图片"}],
             ["needed", {en:"Shoot to be commissioned",es:"Reportaje por encargar",
                         ar:"يلزم طلب جلسة تصوير",zh:"需安排拍摄"}]] },
    { k: "permit", q: {en:"Permit or mandate reference",es:"Referencia de permiso o mandato",
                       ar:"مرجع التصريح أو التفويض",zh:"许可或委托编号"}, text: true },
    { k: "review", q: {en:"Submit for review",es:"Enviar a revisión",
                       ar:"إرسال للمراجعة",zh:"提交审核"},
      opts: [["now", {en:"Submit now",es:"Enviar ahora",ar:"إرسال الآن",zh:"立即提交"}],
             ["draft", {en:"Keep as draft",es:"Guardar como borrador",
                        ar:"حفظ كمسودة",zh:"存为草稿"}]] }
  ];
  var W = { i: 0, v: {}, err: "" };

  function wizardOpts(step) {
    if (step.dyn === "type") {
      var cat = W.v.category;
      var seen = {}, out = [];
      (window.__XARU_TYPES__ || []).forEach(function (x) {
        if (cat && x.cat !== cat) return;
        if (seen[x.type]) return;
        seen[x.type] = 1;
        out.push([x.type, x.typeName || { en: x.type }]);
      });
      return out.slice(0, 24);
    }
    if (step.dyn === "country") {
      return (window.__XARU_CC__ || []).slice(0, 60).map(function (c) {
        return [c.code, c.name];
      });
    }
    if (step.dyn === "city") {
      var cc = (window.__XARU_CC__ || []).filter(function (c) { return c.code === W.v.country; })[0];
      return ((cc && cc.cities) || []).map(function (t2) {
        return [t2.name, { en: t2.name, es: t2.name, ar: t2.name, zh: t2.name }];
      });
    }
    return step.opts || [];
  }

  function wizard() {
    var step = WSTEPS[W.i];
    var body;
    if (W.i >= WSTEPS.length) {
      body = '<div class="xr_cs_summary"><h4>' + esc(t("summary")) + "</h4>" +
        table([t("entry"), t("state")], WSTEPS.map(function (s) {
          var v = W.v[s.k];
          if (s.num) v = s.num.map(function (n) { return W.v[s.k + "_" + n] || "—"; }).join(" · ");
          return "<tr><td>" + esc(s.q[L] || s.q.en) + "</td><td><bdi>" +
            esc(v == null || v === "" ? "—" : v) + "</bdi></td></tr>";
        })) +
        '<p class="xr_cs_note">' + esc(t("wizardNote")) + "</p>" +
        '<button type="button" class="xr_ac_btn xr_wz_restart">' + esc(t("restart")) + "</button>" +
      "</div>";
    } else if (step.num) {
      body = '<div class="xr_wz_fields">' + step.num.map(function (n) {
        return '<label>' + esc(n) + '<input type="number" min="0" data-wznum="' + esc(n) +
          '" value="' + esc(W.v[step.k + "_" + n] || "") + '"></label>';
      }).join("") + "</div>";
    } else if (step.text) {
      body = '<div class="xr_wz_fields"><label><input type="text" data-wztext value="' +
        esc(W.v[step.k] || "") + '"></label></div>';
    } else {
      var opts = wizardOpts(step);
      body = '<div class="xr_wz_opts">' + opts.map(function (o) {
        var label = typeof o[1] === "string" ? o[1] : (o[1][L] || o[1].en);
        return '<button type="button" class="xr_wz_opt' +
          (W.v[step.k] === o[0] ? " is-on" : "") + '" data-wzopt="' + esc(o[0]) + '">' +
          esc(label) + "</button>";
      }).join("") + "</div>";
      if (!opts.length) {
        body = '<p class="xr_cs_empty">' + esc(t("empty")) + "</p>";
      }
    }

    var n = Math.min(W.i + 1, WSTEPS.length);
    return '<div class="xr_wz">' +
      '<div class="xr_wz_head">' +
        "<span>" + esc(t("step")) + " " + nf(n) + " " + esc(t("of")) + " " +
          nf(WSTEPS.length) + "</span>" +
        '<div class="xr_wz_bar"><i style="width:' +
          Math.round(n * 100 / WSTEPS.length) + '%"></i></div>' +
      "</div>" +
      (W.i < WSTEPS.length ? "<h4>" + esc(step.q[L] || step.q.en) + "</h4>" : "") +
      body +
      (W.err ? '<p class="xr_wz_err">' + esc(W.err) + "</p>" : "") +
      (W.i < WSTEPS.length
        ? '<div class="xr_wz_nav">' +
            '<button type="button" class="xr_ac_btn xr_wz_back"' +
              (W.i === 0 ? " disabled" : "") + ">" + esc(t("back")) + "</button>" +
            '<button type="button" class="xr_ac_btn is-on xr_wz_next">' +
              esc(W.i === WSTEPS.length - 1 ? t("finish") : t("next")) + "</button>" +
          "</div>"
        : "") +
    "</div>";
  }

  /* ================================================================ admin */
  function adminQueue() {
    var rows = (ADMIN.queue || []).map(function (c) {
      var od = overdue(c.slaDueAt) && c.status !== "decided";
      return "<tr>" +
        '<td><a href="' + PR + "property-details.html?id=" + encodeURIComponent(c.listing) +
          '">' + esc(c.title || c.listing) + "</a>" +
          '<span class="xr_cs_sub">' + esc([c.city, c.country].filter(Boolean).join(", ")) +
          " · " + esc(c.org || "") + "</span></td>" +
        "<td>" + pill(String(c.state || "").toLowerCase().replace(/_/g, "-"), stateL(c.state)) + "</td>" +
        "<td>" + pill(c.priority, c.priority) + "</td>" +
        "<td><bdi>" + nf(Math.round((c.risk || 0) * 100)) + "%</bdi></td>" +
        "<td>" + (c.failedRules || []).map(function (r) {
            return '<span class="xr_pf_chip">' + esc(ruleL(r)) + "</span>";
          }).join(" ") + "</td>" +
        "<td>" + (od ? pill("late", t("overdueL")) : esc(when(c.slaDueAt))) + "</td>" +
        "<td>" + esc(c.assignee || t("unassigned")) + "</td>" +
        '<td class="xr_cs_actions">' +
          '<button type="button" class="xr_ac_btn" disabled title="' + esc(t("readOnly")) + '">' +
            esc(t("approve")) + "</button>" +
          '<button type="button" class="xr_ac_btn is-danger" disabled title="' +
            esc(t("readOnly")) + '">' + esc(t("reject")) + "</button>" +
        "</td>" +
      "</tr>";
    });
    var late = (ADMIN.queue || []).filter(function (c) {
      return overdue(c.slaDueAt) && c.status !== "decided";
    }).length;
    var open = (ADMIN.queue || []).filter(function (c) { return c.status !== "decided"; }).length;
    return '<div class="xr_cs_kpis">' +
        "<div><b>" + nf(ADMIN.queueCount) + "</b><span>" + esc(t("queue")) + "</span></div>" +
        "<div><b>" + nf(open) + "</b><span>" + esc(t("state")) + "</span></div>" +
        '<div><b class="' + (late ? "is-late" : "") + '">' + nf(late) + "</b><span>" +
          esc(t("overdueL")) + "</span></div>" +
      "</div>" +
      '<p class="xr_cs_note">' + esc(t("readOnly")) + "</p>" +
      table([t("listing"), t("state"), "SLA", t("risk"), t("rules"),
             t("sla"), t("assignee"), ""], rows);
  }

  function adminLifecycle() {
    var st = ADMIN.lifecycleStates || {};
    var keys = Object.keys(st).sort(function (a, b) { return st[b] - st[a]; });
    var max = Math.max.apply(null, keys.map(function (k) { return st[k]; }).concat([1]));
    return '<div class="xr_cs_bars">' + keys.map(function (k) {
      return '<div class="xr_cs_barrow">' +
        '<span class="xr_cs_barlbl">' + esc(stateL(k)) + "</span>" +
        '<span class="xr_cs_bartrack"><i style="width:' +
          Math.max(1, Math.round(st[k] * 100 / max)) + '%"></i></span>' +
        '<b class="xr_cs_barval">' + nf(st[k]) + "</b></div>";
    }).join("") + "</div>" +
      '<h4 class="xr_cs_h">' + esc(t("activity")) + "</h4>" +
      table([t("listing"), t("from"), t("to"), t("actor"), t("at")],
        (ADMIN.transitions || []).slice(0, 25).map(function (x) {
          return "<tr><td><bdi>" + esc(x.listing) + "</bdi></td><td>" +
            esc(stateL(x.from)) + "</td><td>" + pill(
              String(x.to || "").toLowerCase().replace(/_/g, "-"), stateL(x.to)) +
            "</td><td>" + esc(x.actor || "—") + "</td><td>" + esc(when(x.at)) + "</td></tr>";
        }));
  }

  function adminTaxonomy() {
    var tx = ADMIN.taxonomies || {};
    return '<div class="xr_cs_kpis">' +
      [["types", tx.propertyTypes], ["amenities", tx.amenities],
       ["countries", tx.countries], ["cities", tx.cities]].map(function (p) {
        return "<div><b>" + nf(p[1] || 0) + "</b><span>" + esc(t(p[0])) + "</span></div>";
      }).join("") + "</div>" +
      '<p class="xr_cs_note">' + esc(t("readOnly")) + "</p>";
  }

  /* ---------------------------------------------------------------- pintado */
  function paint() {
    if (MODE === "b2b") {
      var o = B2B.items[ORG];
      HOST.innerHTML =
        '<div class="xr_cs_bar">' +
          '<select class="xr_cs_org" aria-label="' + esc(t("office")) + '">' +
          B2B.items.map(function (x, i) {
            return '<option value="' + i + '"' + (i === ORG ? " selected" : "") + ">" +
              esc(x.name) + "</option>";
          }).join("") + "</select>" +
        "</div>" +
        tabs([["inventory", t("inventory")], ["pipeline", t("pipeline")],
              ["billing", t("billing")], ["wizard", t("wizard")]]) +
        '<div class="xr_cs_body">' +
          (TAB === "pipeline" ? b2bPipeline(o)
            : TAB === "billing" ? b2bBilling(o)
            : TAB === "wizard" ? wizard()
            : b2bInventory(o)) +
        "</div>";
    } else {
      HOST.innerHTML =
        tabs([["queue", t("queue")], ["lifecycle", t("lifecycle")], ["taxonomy", t("taxonomy")]]) +
        '<div class="xr_cs_body">' +
          (TAB === "lifecycle" ? adminLifecycle()
            : TAB === "taxonomy" ? adminTaxonomy()
            : adminQueue()) +
        "</div>";
    }
  }

  function bind() {
    HOST.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (!b || b.disabled) return;
      if (b.hasAttribute("data-tab")) { TAB = b.getAttribute("data-tab"); return paint(); }
      if (b.hasAttribute("data-wzopt")) {
        W.v[WSTEPS[W.i].k] = b.getAttribute("data-wzopt");
        W.err = "";
        // Cambiar de categoria invalida la tipologia elegida; cambiar de pais,
        // la ciudad. Arrastrar un valor incoherente es peor que perderlo.
        if (WSTEPS[W.i].k === "category") delete W.v.type;
        if (WSTEPS[W.i].k === "country") delete W.v.city;
        return paint();
      }
      if (b.classList.contains("xr_wz_back")) { W.i = Math.max(0, W.i - 1); W.err = ""; return paint(); }
      if (b.classList.contains("xr_wz_next")) {
        var s = WSTEPS[W.i], ok;
        if (s.num) ok = s.num.every(function (n) { return W.v[s.k + "_" + n]; });
        else if (s.text) ok = !!W.v[s.k];
        else ok = !!W.v[s.k];
        if (!ok) { W.err = t("required"); return paint(); }
        W.err = ""; W.i += 1; return paint();
      }
      if (b.classList.contains("xr_wz_restart")) { W = { i: 0, v: {}, err: "" }; return paint(); }
    });
    HOST.addEventListener("change", function (e) {
      if (e.target.classList.contains("xr_cs_org")) {
        ORG = parseInt(e.target.value, 10) || 0;
        return paint();
      }
    });
    HOST.addEventListener("input", function (e) {
      var el = e.target, s = WSTEPS[W.i];
      if (!s) return;
      if (el.hasAttribute("data-wznum")) W.v[s.k + "_" + el.getAttribute("data-wznum")] = el.value;
      if (el.hasAttribute("data-wztext")) W.v[s.k] = el.value;
    });
  }

  HOST.innerHTML = '<p class="xr_dir_loading">' + esc(t("loading")) + "</p>";
  Promise.all([
    fetch(API + (MODE === "b2b" ? "b2b.json" : "admin.json"))
      .then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }),
    MODE === "b2b" ? fetch(API + "search-index.json")
      .then(function (r) { return r.ok ? r.json() : { items: [] }; })
      .catch(function () { return { items: [] }; }) : Promise.resolve(null),
    MODE === "b2b" ? fetch(API + "locations.json")
      .then(function (r) { return r.ok ? r.json() : { countries: [] }; })
      .catch(function () { return { countries: [] }; }) : Promise.resolve(null)
  ]).then(function (o) {
    if (!o[0]) throw new Error("no data");
    if (MODE === "b2b") {
      B2B = o[0]; TAB = "inventory";
      window.__XARU_TYPES__ = (o[1].items || []).map(function (x) {
        return { type: x.type, typeName: x.typeName, cat: x.cat };
      });
      window.__XARU_CC__ = o[2].countries || [];
    } else {
      ADMIN = o[0]; TAB = "queue";
    }
    paint();
    bind();
  }).catch(function (err) {
    if (window.console) console.warn("[xaru-console]", err);
    HOST.innerHTML = '<p class="xr_cs_empty">' + esc(t("empty")) + "</p>";
  });
})();
