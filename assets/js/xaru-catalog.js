/* XARU HOME — renderizador del catálogo demostrativo (Biblia Visual V3 §8, §17)
 *
 * Lee data/properties/*.json y construye las tarjetas con el MISMO marcado que
 * la plantilla (cs_card cs_style_1), de modo que el diseño, los efectos y las
 * animaciones existentes siguen aplicándose sin tocarse.
 *
 * Aporta sobre la plantilla:
 *   - <picture> con AVIF / WebP / JPEG y srcset en 480/768/1280/1920/2560
 *   - carga diferida real (loading=lazy, decoding=async)
 *   - filtros por tipología propios del catálogo, no los genéricos de la plantilla
 *   - i18n por atributo lang del documento (en / es / ar / zh)
 *
 * Todo activo lleva demo:true. No se presenta como inventario real.
 */
(function () {
  "use strict";

  var WIDTHS = [480, 768, 1280, 1920, 2560];
  var SIZES =
    "(max-width: 575px) 92vw, (max-width: 767px) 46vw, (max-width: 991px) 44vw, "
    + "(max-width: 1399px) 31vw, 300px";   // medido: la tarjeta ocupa ~291 px en escritorio

  /* ---------- utilidades ---------- */

  function lang() {
    var l = (document.documentElement.getAttribute("lang") || "en").toLowerCase();
    l = l.split("-")[0];
    return ["en", "es", "ar", "zh"].indexOf(l) >= 0 ? l : "en";
  }

  // Prefijo para subir desde la página actual hasta la raíz del sitio.
  function root() {
    var p = location.pathname.replace(/\/[^\/]*$/, "/");
    var depth = p.split("/").filter(Boolean).length;
    // /es/, /ar/, /zh/ cuentan como un nivel; los subdirectorios suman.
    return depth ? new Array(depth + 1).join("../") : "";
  }

  function t(field, l) {
    if (field == null) return "";
    if (typeof field === "string") return field;
    return field[l] || field.en || "";
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function price(usd, l) {
    if (!usd) return "";
    var v, u;
    if (usd >= 1e9) { v = usd / 1e9; u = "B"; }
    else if (usd >= 1e6) { v = usd / 1e6; u = "M"; }
    else { v = usd / 1e3; u = "K"; }
    var n = v >= 100 ? Math.round(v) : Math.round(v * 10) / 10;
    return "$" + n + u;
  }

  function num(n, l) {
    if (n == null) return "";
    try { return Number(n).toLocaleString(l === "zh" ? "zh-CN" : l); }
    catch (e) { return String(n); }
  }

  /* ---------- imagen responsive ---------- */

  // hero_image llega como assets/img/xaru/catalog/<id>.jpg
  // las derivadas viven en assets/img/xaru/catalog/r/<id>-<w>.<ext>
  function srcset(rel, ext, R) {
    var m = rel.match(/([^\/]+)\.jpg$/);
    if (!m) return null;
    var base = R + "assets/img/xaru/catalog/r/" + m[1];
    return WIDTHS.map(function (w) {
      return base + "-" + w + "." + ext + " " + w + "w";
    }).join(", ");
  }

  function picture(rel, alt, cls, R) {
    var avif = srcset(rel, "avif", R);
    var webp = srcset(rel, "webp", R);
    var jpg = srcset(rel, "jpg", R);
    var fallback = R + rel;
    if (!avif) {
      return '<img src="' + esc(fallback) + '" class="' + cls +
        '" loading="lazy" decoding="async" alt="' + esc(alt) + '">';
    }
    return (
      "<picture>" +
      '<source type="image/avif" srcset="' + esc(avif) + '" sizes="' + SIZES + '">' +
      '<source type="image/webp" srcset="' + esc(webp) + '" sizes="' + SIZES + '">' +
      '<img src="' + esc(fallback) + '" srcset="' + esc(jpg) + '" sizes="' + SIZES +
      '" class="' + cls + '" loading="lazy" decoding="async" alt="' + esc(alt) + '">' +
      "</picture>"
    );
  }

  /* ---------- tarjeta ---------- */

  function metric(label, value) {
    if (!value) return "";
    return '<li><span class="cs_primary_color"></span>' +
      esc(value) + " " + esc(label) + "</li>";
  }

  function card(item, ui, l, R) {
    var title = t(item.title, l);
    var loc = [t(item.city, l), t(item.country, l)].filter(Boolean).join(", ");
    var cat = t(item.language_content && item.language_content.category, l);
    var variant = t(item.language_content && item.language_content.variant, l);
    var status = t(item.language_content && item.language_content.status, l);
    var alt = title + " — " + cat + (loc ? ", " + loc : "");

    var feats = [
      metric(t(ui.beds, l), item.bedrooms),
      metric(t(ui.baths, l), item.bathrooms),
      item.built_area_m2 ? metric("m² " + t(ui.built, l), num(item.built_area_m2, l)) : "",
      item.hotel_keys ? metric(t(ui.keys, l), item.hotel_keys) : "",
      item.berths ? metric(t(ui.berths, l), item.berths) : "",
      item.hectares && !item.bedrooms ? metric(t(ui.hectares, l), num(item.hectares, l)) : ""
    ].filter(Boolean).join("");

    var detail = R + "property-details.html?id=" + encodeURIComponent(item.id);

    return (
      '<div class="col-md-6 col-xl-4 xr_cat_item" ' +
      'data-subcategory="' + esc(item.subcategory) + '" ' +
      'data-variant="' + esc(item.variant) + '" ' +
      'data-price="' + Number(item.price_usd || 0) + '" ' +
      'data-beds="' + Number(item.bedrooms || 0) + '" ' +
      'data-baths="' + Number(item.bathrooms || 0) + '">' +
        '<div class="cs_card cs_style_1">' +
          '<a href="' + esc(detail) + '" aria-label="' + esc(title) +
          '" class="cs_card_thumbnail cs_radius_20 cs_mb_17 position-relative">' +
            picture(item.hero_image, alt, "cs_card_img_front", R) +
            '<span class="cs_property_price cs_primary_bg cs_fs_20 cs_white_color ' +
            'cs_semibold cs_primary_font cs_radius_10 position-absolute">' +
            esc(price(item.price_usd, l)) + "</span>" +
            '<span class="xr_demo_flag">' + esc(status) + "</span>" +
          "</a>" +
          '<div class="cs_card_content">' +
            (feats ? '<ul class="cs_property_features cs_mb_23 list-unstyled">' + feats + "</ul>" : "") +
            '<h3 class="cs_fs_20 cs_semibold cs_mb_5">' +
            '<a href="' + esc(detail) + '">' + esc(title) + "</a></h3>" +
            '<p class="cs_heading_color cs_mb_5">' + esc(loc) + "</p>" +
            '<p class="xr_cat_kind">' + esc(cat) + (variant ? " · " + esc(variant) : "") + "</p>" +
          "</div>" +
        "</div>" +
      "</div>"
    );
  }

  /* ---------- filtros por tipología ---------- */

  function filters(items, l, mount) {
    var seen = {}, order = [];
    items.forEach(function (it) {
      var k = it.subcategory;
      if (!seen[k]) {
        seen[k] = t(it.language_content && it.language_content.category, l) || k;
        order.push(k);
      }
    });
    var all = { en: "All", es: "Todos", ar: "الكل", zh: "全部" }[l];
    var html = '<button type="button" class="xr_cat_filter is-active" data-f="*">' +
      esc(all) + "</button>";
    order.forEach(function (k) {
      html += '<button type="button" class="xr_cat_filter" data-f="' + esc(k) + '">' +
        esc(seen[k]) + "</button>";
    });
    mount.innerHTML = html;

    mount.addEventListener("click", function (e) {
      var b = e.target.closest(".xr_cat_filter");
      if (!b) return;
      var f = b.getAttribute("data-f");
      mount.querySelectorAll(".xr_cat_filter").forEach(function (x) {
        x.classList.toggle("is-active", x === b);
      });
      STATE.typology = f;
      applyFilters();
    });
  }

  /* ---------- barra lateral heredada de la plantilla ----------
   * La plantilla trae filtros de dormitorios, baños y precio. Al pasar el
   * listado a datos, esos controles quedarían decorativos: se conectan aquí
   * para que hagan lo que dicen que hacen. Si la página no los trae, no pasa
   * nada — todo es opcional.                                               */

  var STATE = { typology: "*", beds: [], baths: [], min: 0, max: Infinity };

  function applyFilters() {
    document.querySelectorAll(".xr_cat_item").forEach(function (el) {
      var beds = +el.getAttribute("data-beds");
      var baths = +el.getAttribute("data-baths");
      var p = +el.getAttribute("data-price");
      var ok =
        (STATE.typology === "*" || el.getAttribute("data-subcategory") === STATE.typology) &&
        (!STATE.beds.length || STATE.beds.some(function (n) { return n === 5 ? beds > 4 : beds === n; })) &&
        (!STATE.baths.length || STATE.baths.some(function (n) { return n === 5 ? baths > 4 : baths === n; })) &&
        p >= STATE.min && p <= STATE.max;
      el.hidden = !ok;
    });
    var vis = document.querySelectorAll(".xr_cat_item:not([hidden])").length;
    var out = document.querySelector("[data-catalog-count]");
    if (out) out.textContent = vis;
  }

  function checkedNums(labels) {
    var out = [];
    labels.forEach(function (lb) {
      var box = lb.querySelector('input[type="checkbox"]');
      if (!box || !box.checked) return;
      var txt = (lb.textContent || "").trim();
      out.push(/more|más|mas|أكثر|以上/i.test(txt) ? 5 : parseInt(txt, 10));
    });
    return out.filter(function (n) { return !isNaN(n); });
  }

  function bindSidebar() {
    // Agrupa los checkboxes por el encabezado de su bloque.
    var groups = { beds: [], baths: [] };
    document.querySelectorAll("h2, h3, h4, .cs_widget_title").forEach(function (h) {
      var txt = (h.textContent || "").toLowerCase();
      var key = /bedroom|dormitor|غرف النوم|卧室/.test(txt) ? "beds"
              : /bathroom|baño|bano|الحمامات|浴室/.test(txt) ? "baths" : null;
      if (!key) return;
      var box = h.parentElement;
      if (box) groups[key] = Array.prototype.slice.call(box.querySelectorAll("li, label"));
    });

    // Valores que realmente existen en el catálogo. La plantilla ofrece
    // 1/2/3 dormitorios, que en una cartera de este rango no se dan nunca:
    // dejar esas casillas sería ofrecer un filtro que no puede devolver nada.
    var present = { beds: {}, baths: {} };
    document.querySelectorAll(".xr_cat_item").forEach(function (el) {
      var b = +el.getAttribute("data-beds"), t2 = +el.getAttribute("data-baths");
      if (b) present.beds[b > 4 ? 5 : b] = 1;
      if (t2) present.baths[t2 > 4 ? 5 : t2] = 1;
    });

    Object.keys(groups).forEach(function (k) {
      groups[k].forEach(function (lb) {
        var input = lb.querySelector('input[type="checkbox"]');
        if (!input) return;
        var n = checkedNums([lb].map(function (x) {
          var c = x.cloneNode(true);
          var cb = c.querySelector('input[type="checkbox"]');
          if (cb) cb.checked = true;
          return c;
        }))[0];
        if (n && !present[k][n]) { lb.hidden = true; return; }
        input.addEventListener("change", function () {
          STATE[k] = checkedNums(groups[k]);
          applyFilters();
        });
      });
    });

    var priceInputs = Array.prototype.slice.call(
      document.querySelectorAll('input[placeholder^="$"]'));
    if (priceInputs.length >= 2) {
      // La plantilla trae rangos de vivienda corriente; el catálogo arranca
      // por encima del millón. Se reetiquetan para no mentir sobre el rango.
      priceInputs[0].placeholder = "$1,000,000";
      priceInputs[1].placeholder = "$500,000,000";
      priceInputs.slice(0, 2).forEach(function (inp, i) {
        inp.addEventListener("input", function () {
          var v = parseFloat((inp.value || "").replace(/[^0-9.]/g, ""));
          if (i === 0) STATE.min = isNaN(v) ? 0 : v;
          else STATE.max = isNaN(v) ? Infinity : v;
          applyFilters();
        });
      });
    }
  }

  /* ---------- arranque ---------- */

  function render(host) {
    var l = lang();
    var R = root();
    var files = (host.getAttribute("data-catalog") || "private-real-estate")
      .split(",").map(function (s) { return s.trim(); }).filter(Boolean);

    Promise.all(files.map(function (f) {
      return fetch(R + "data/properties/" + f + ".json").then(function (r) {
        if (!r.ok) throw new Error(f + ": " + r.status);
        return r.json();
      });
    })).then(function (packs) {
      var items = [], ui = packs[0].ui || {};
      packs.forEach(function (p) { items = items.concat(p.items || []); });

      var limit = parseInt(host.getAttribute("data-limit") || "0", 10);
      if (limit > 0) items = items.slice(0, limit);

      host.innerHTML = items.map(function (it) { return card(it, ui, l, R); }).join("");

      var fmount = document.querySelector("[data-catalog-filters]");
      if (fmount) filters(items, l, fmount);

      bindSidebar();
      applyFilters();

      var note = document.querySelector("[data-catalog-note]");
      if (note) note.textContent = t(packs[0].demo_note, l);

      host.dispatchEvent(new CustomEvent("xaru:catalog-ready", {
        bubbles: true, detail: { count: items.length }
      }));
    }).catch(function (err) {
      // Sin datos no se deja un hueco: se retira el contenedor en silencio.
      if (window.console) console.warn("[xaru-catalog]", err);
      host.removeAttribute("data-catalog");
    });
  }

  function init() {
    document.querySelectorAll("[data-catalog]").forEach(render);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
