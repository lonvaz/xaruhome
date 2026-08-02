/*
 * XARU HOME — entrada al marketplace
 * =============================================================
 * El buscador que abre el inventario desde la página de Real Estate: selector
 * de operación, autocompletado jerárquico país → ciudad, filtros rápidos y las
 * plazas con más stock.
 *
 * No filtra nada por su cuenta. Compone la URL canónica de la ruta de
 * resultados —/real-estate/buy/?cc=ES&city=Marbella— y navega. Esa URL es la
 * misma que se comparte, se guarda y se indexa, así que la entrada y el
 * resultado no pueden desincronizarse.
 *
 * Se alimenta de /data/api/v1/locations.json y stats.json, la proyección de la
 * base de datos. La sección editorial de la página no se toca: esto se monta
 * encima, no en su lugar.
 */
(function () {
  "use strict";

  var HOST = document.querySelector("[data-mp-home]");
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
  function nf(v) {
    try {
      return new Intl.NumberFormat(L === "zh" ? "zh-CN" : L === "ar" ? "ar-AE"
        : L === "es" ? "es-ES" : "en-US").format(v);
    } catch (e) { return String(v); }
  }
  function norm(s) {
    s = String(s || "").toLowerCase();
    try { s = s.normalize("NFD").replace(/[̀-ͯ]/g, ""); } catch (e) {}
    return s.trim();
  }

  var T = {
    buy:        {en:"Buy",es:"Comprar",ar:"شراء",zh:"购买"},
    rent:       {en:"Rent",es:"Alquilar",ar:"إيجار",zh:"租赁"},
    commercial: {en:"Commercial",es:"Comercial",ar:"تجاري",zh:"商业"},
    land:       {en:"Land",es:"Suelo",ar:"أراضٍ",zh:"土地"},
    placeholder:{en:"Country, city or asset type",
                 es:"País, ciudad o tipo de activo",
                 ar:"دولة أو مدينة أو نوع الأصل",
                 zh:"国家、城市或资产类型"},
    search:     {en:"Search",es:"Buscar",ar:"بحث",zh:"搜索"},
    onMap:      {en:"Search on the map",es:"Buscar sobre el mapa",
                 ar:"البحث على الخريطة",zh:"地图检索"},
    quick:      {en:"Straight to",es:"Directo a",ar:"مباشرة إلى",zh:"快速进入"},
    islands:    {en:"Private islands",es:"Islas privadas",ar:"جزر خاصة",zh:"私人岛屿"},
    castles:    {en:"Castles & estates",es:"Castillos y fincas",ar:"قلاع وحوزات",zh:"城堡与庄园"},
    hotels:     {en:"Operating hotels",es:"Hoteles en operación",ar:"فنادق تشغيلية",zh:"在营酒店"},
    mining:     {en:"Mining & quarries",es:"Minería y canteras",ar:"تعدين ومحاجر",zh:"矿业与采石"},
    citysized:  {en:"City-scale land",es:"Suelo de escala urbana",ar:"أراضٍ بحجم مدينة",zh:"城市级土地"},
    offplan:    {en:"Off-plan projects",es:"Proyectos off-plan",ar:"مشاريع على المخطط",zh:"期房项目"},
    markets:    {en:"Markets with the most stock",es:"Plazas con más inventario",
                 ar:"الأسواق الأكثر معروضاً",zh:"库存最多的市场"},
    assets:     {en:"assets",es:"activos",ar:"أصل",zh:"项资产"},
    countries:  {en:"countries",es:"países",ar:"دولة",zh:"个国家"},
    cities:     {en:"cities",es:"ciudades",ar:"مدينة",zh:"座城市"},
    advisers:   {en:"advisers",es:"asesores",ar:"مستشار",zh:"位顾问"},
    noMatch:    {en:"No match",es:"Sin coincidencias",ar:"لا نتائج",zh:"无匹配"},
    allIn:      {en:"Everything in",es:"Todo en",ar:"كل ما في",zh:"全部位于"},
    simNote:    {en:"Simulation mode — the inventory below is platform demo data.",
                 es:"Modo simulación — el inventario de abajo es de muestra de la plataforma.",
                 ar:"وضع المحاكاة — المعروض أدناه بيانات تجريبية للمنصة.",
                 zh:"模拟模式——以下资产为平台演示数据。"}
  };
  function t(k) { return (T[k] && (T[k][L] || T[k].en)) || k; }

  /* Cada operación es una ruta distinta, no un parámetro: son las URL que se
     indexan y las que el cliente comparte. */
  var OPS = [
    { k: "buy",        route: "real-estate/buy/" },
    { k: "rent",       route: "real-estate/rent/" },
    { k: "commercial", route: "real-estate/commercial/buy/" },
    { k: "land",       route: "real-estate/land/" }
  ];
  var QUICK = [
    { k: "islands",   route: "real-estate/buy/?type=private-island" },
    { k: "castles",   route: "real-estate/buy/?type=castle,estate,hacienda" },
    { k: "hotels",    route: "real-estate/commercial/buy/?type=hotel,resort" },
    { k: "mining",    route: "real-estate/land/?type=mining-concession,quarry" },
    { k: "citysized", route: "real-estate/land/?type=city-scale-land,masterplan-land" },
    { k: "offplan",   route: "real-estate/buy/?completion=off_plan" }
  ];

  var LOCS = null, STATS = null, OP = "buy", PICK = null;

  function shell() {
    return '' +
      '<div class="xr_mph_card">' +
        '<div class="xr_mph_ops" role="tablist">' +
          OPS.map(function (o, i) {
            return '<button type="button" role="tab" data-op="' + esc(o.k) + '"' +
              (i === 0 ? ' class="is-on" aria-selected="true"' : ' aria-selected="false"') +
              ">" + esc(t(o.k)) + "</button>";
          }).join("") +
        "</div>" +
        '<div class="xr_mph_row">' +
          '<div class="xr_mph_field">' +
            '<input type="search" class="xr_mph_q" autocomplete="off" ' +
              'placeholder="' + esc(t("placeholder")) + '" ' +
              'aria-label="' + esc(t("placeholder")) + '" role="combobox" ' +
              'aria-expanded="false" aria-controls="xr_mph_list">' +
            '<ul class="xr_mph_list" id="xr_mph_list" role="listbox" hidden></ul>' +
          "</div>" +
          '<button type="button" class="xr_mph_go">' + esc(t("search")) + "</button>" +
        "</div>" +
        '<div class="xr_mph_foot">' +
          '<a class="xr_mph_maplink" href="' + PR + 'real-estate/map/">' +
            '<i class="fa-solid fa-location-dot"></i> ' + esc(t("onMap")) + "</a>" +
        "</div>" +
      "</div>" +
      '<div class="xr_mph_quick"><span>' + esc(t("quick")) + "</span>" +
        QUICK.map(function (q) {
          return '<a href="' + PR + q.route + '">' + esc(t(q.k)) + "</a>";
        }).join("") +
      "</div>" +
      '<div class="xr_mph_stats"></div>' +
      '<div class="xr_mph_markets"></div>';
  }

  /* ------------------------------------------------- autocompletado jerárquico
     País primero, sus ciudades indentadas debajo. Es la jerarquía real del
     árbol geográfico, no una lista plana de cadenas. */
  function suggest(qs) {
    var q = norm(qs), out = [];
    var cs = (LOCS && LOCS.countries) || [];
    if (!q) {
      cs.slice()
        .sort(function (a, b) { return b.count - a.count; })
        .slice(0, 8)
        .forEach(function (c) { out.push({ kind: "country", c: c }); });
      return out;
    }
    cs.forEach(function (c) {
      var cn = c.name[L] || c.name.en;
      var hitC = norm(cn).indexOf(q) === 0 || norm(c.name.en).indexOf(q) === 0 ||
                 norm(c.code) === q;
      var cities = (c.cities || []).filter(function (t2) { return norm(t2.name).indexOf(q) >= 0; });
      if (hitC) {
        out.push({ kind: "country", c: c });
        (c.cities || []).slice(0, 4).forEach(function (t2) {
          out.push({ kind: "city", c: c, t: t2 });
        });
      } else if (cities.length) {
        out.push({ kind: "country", c: c, dim: true });
        cities.slice(0, 5).forEach(function (t2) { out.push({ kind: "city", c: c, t: t2 }); });
      }
    });
    return out.slice(0, 12);
  }

  function paintList(items) {
    var ul = HOST.querySelector(".xr_mph_list");
    if (!items.length) {
      ul.innerHTML = '<li class="xr_mph_none">' + esc(t("noMatch")) + "</li>";
    } else {
      ul.innerHTML = items.map(function (it, i) {
        var cn = it.c.name[L] || it.c.name.en;
        if (it.kind === "country") {
          return '<li role="option" data-i="' + i + '" class="xr_mph_opt is-country' +
            (it.dim ? " is-dim" : "") + '">' +
            '<span class="xr_mph_opt_name">' + esc(cn) + "</span>" +
            '<span class="xr_mph_opt_n">' + nf(it.c.count) + "</span></li>";
        }
        return '<li role="option" data-i="' + i + '" class="xr_mph_opt is-city">' +
          '<span class="xr_mph_opt_name">' + esc(it.t.name) + "</span>" +
          '<span class="xr_mph_opt_sub">' + esc(cn) + "</span>" +
          '<span class="xr_mph_opt_n">' + nf(it.t.count) + "</span></li>";
      }).join("");
    }
    ul.hidden = false;
    HOST.querySelector(".xr_mph_q").setAttribute("aria-expanded", "true");
    ul._items = items;
  }

  function closeList() {
    var ul = HOST.querySelector(".xr_mph_list");
    ul.hidden = true;
    HOST.querySelector(".xr_mph_q").setAttribute("aria-expanded", "false");
  }

  /* Si lo tecleado nombra exactamente un pais o una ciudad, se filtra por
     ellos en vez de buscar el texto: "Mexico" debe abrir Mexico, no una
     busqueda por la palabra. */
  function resolve(txt) {
    var q = norm(txt);
    if (!q) return null;
    var cs = (LOCS && LOCS.countries) || [], hit = null;
    cs.forEach(function (c) {
      if (hit) return;
      if (norm(c.name[L] || "") === q || norm(c.name.en) === q || norm(c.code) === q) {
        hit = { cc: c.code, city: null };
      }
    });
    if (hit) return hit;
    cs.forEach(function (c) {
      if (hit) return;
      (c.cities || []).forEach(function (t2) {
        if (!hit && norm(t2.name) === q) hit = { cc: c.code, city: t2.name };
      });
    });
    return hit;
  }

  function go() {
    var op = OPS.filter(function (o) { return o.k === OP; })[0] || OPS[0];
    var qs = [];
    if (PICK) {
      qs.push("cc=" + encodeURIComponent(PICK.cc));
      if (PICK.city) qs.push("city=" + encodeURIComponent(PICK.city));
    } else {
      var free = HOST.querySelector(".xr_mph_q").value.trim();
      var hit = resolve(free);
      if (hit) {
        qs.push("cc=" + encodeURIComponent(hit.cc));
        if (hit.city) qs.push("city=" + encodeURIComponent(hit.city));
      } else if (free) {
        qs.push("q=" + encodeURIComponent(free));
      }
    }
    location.href = PR + op.route + (qs.length ? "?" + qs.join("&") : "");
  }

  function paintStats() {
    if (!STATS) return;
    var pairs = [[STATS.listings, "assets"], [STATS.countries, "countries"],
                 [STATS.cities, "cities"], [STATS.agents, "advisers"]];
    HOST.querySelector(".xr_mph_stats").innerHTML =
      pairs.map(function (p) {
        return '<div class="xr_mph_stat"><b>' + nf(p[0]) + "</b><span>" +
          esc(t(p[1])) + "</span></div>";
      }).join("") +
      '<p class="xr_mph_sim">' + esc(t("simNote")) + "</p>";
  }

  function paintMarkets() {
    // Una plaza por pais. Ordenar las 372 ciudades por stock devolvia doce
    // ciudades del mismo pais —el que mas inventario tiene— y la casa parecia
    // operar en un solo mercado. Se toma la primera de cada pais y se ordena
    // entre ellas: doce paises distintos, que es lo que hay.
    var cities = [];
    ((LOCS && LOCS.countries) || []).forEach(function (c) {
      var best = null;
      (c.cities || []).forEach(function (t2) {
        if (t2.count && (!best || t2.count > best.count)) best = t2;
      });
      if (best) cities.push({ c: c, t: best });
    });
    cities.sort(function (a, b) {
      return (b.c.count - a.c.count) || (b.t.count - a.t.count);
    });
    HOST.querySelector(".xr_mph_markets").innerHTML =
      '<h3 class="xr_mph_h">' + esc(t("markets")) + "</h3>" +
      '<div class="xr_mph_mgrid">' +
      cities.slice(0, 12).map(function (x) {
        var cn = x.c.name[L] || x.c.name.en;
        return '<a class="xr_mph_market" href="' + PR + "real-estate/search/?cc=" +
          encodeURIComponent(x.c.code) + "&city=" + encodeURIComponent(x.t.name) + '">' +
          '<strong>' + esc(x.t.name) + "</strong>" +
          "<em>" + esc(cn) + "</em>" +
          "<b>" + nf(x.t.count) + " " + esc(t("assets")) + "</b></a>";
      }).join("") + "</div>";
  }

  function bind() {
    var q = HOST.querySelector(".xr_mph_q");

    HOST.addEventListener("click", function (e) {
      var op = e.target.closest("[data-op]");
      if (op) {
        OP = op.getAttribute("data-op");
        HOST.querySelectorAll("[data-op]").forEach(function (b) {
          var on = b.getAttribute("data-op") === OP;
          b.classList.toggle("is-on", on);
          b.setAttribute("aria-selected", on ? "true" : "false");
        });
        return;
      }
      if (e.target.closest(".xr_mph_go")) { go(); return; }
      var opt = e.target.closest(".xr_mph_opt");
      if (opt) {
        var items = HOST.querySelector(".xr_mph_list")._items || [];
        var it = items[parseInt(opt.getAttribute("data-i"), 10)];
        if (!it) return;
        var cn = it.c.name[L] || it.c.name.en;
        PICK = { cc: it.c.code, city: it.kind === "city" ? it.t.name : null };
        q.value = it.kind === "city" ? it.t.name + ", " + cn : cn;
        closeList();
        go();
      }
    });

    var timer = null;
    q.addEventListener("input", function () {
      PICK = null;
      clearTimeout(timer);
      timer = setTimeout(function () { paintList(suggest(q.value)); }, 140);
    });
    q.addEventListener("focus", function () { paintList(suggest(q.value)); });
    q.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { e.preventDefault(); go(); }
      if (e.key === "Escape") closeList();
    });
    document.addEventListener("click", function (e) {
      if (!HOST.contains(e.target)) closeList();
    });
  }

  Promise.all([
    fetch(API + "locations.json").then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; }),
    fetch(API + "stats.json").then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; })
  ]).then(function (out) {
    LOCS = out[0]; STATS = out[1];
    HOST.innerHTML = shell();
    bind();
    paintStats();
    paintMarkets();
  }).catch(function (err) {
    if (window.console) console.warn("[xaru-mp-home]", err);
  });
})();
