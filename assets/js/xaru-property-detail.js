/*
 * XARU HOME — ficha de propiedad (property-details.html?id=…)
 *
 * POR QUE EXISTE
 * --------------
 * La plantilla traia una ficha de ejemplo: "Evergreen Estates", 70.000 dolares,
 * "217 Horizon Heights Road, NY 10022", una descripcion de una casa alquilada
 * en Filadelfia con inquilinos y ayudas para primer comprador, una calculadora
 * de hipoteca y un listado de colegios cercanos. Las 156 tarjetas del catalogo
 * apuntaban todas ahi, asi que cualquiera que pinchase una propiedad de treinta
 * millones aterrizaba en una vivienda de setenta mil dolares que no existe.
 *
 * Este fichero lee el ?id= de la URL, lo busca en los mismos tres paquetes JSON
 * que alimentan el catalogo y reconstruye la ficha con los datos reales:
 * titulo, ubicacion, precio, fotografia, superficies, descripcion y estado. Las
 * secciones que no aplican a esta cartera — hipoteca, colegios, plano de
 * planta, "amenities" de vivienda corriente — se retiran en lugar de dejarse
 * con datos inventados.
 *
 * Si no hay ?id= o el id no existe, la pagina se queda como esta y se avisa por
 * consola: mejor no tocar nada que dejar una ficha a medias.
 */
(function () {
  "use strict";

  /* El .cs_property_details de la plantilla cierra antes de tiempo: la
     descripcion, la calculadora de hipoteca y el formulario "Schedule A Tour"
     son hermanos suyos dentro del mismo .container. Se reescribe el contenedor
     entero, no solo el primer bloque, o la ficha real quedaria con la ficha
     inventada pegada debajo. */
  var ANCHOR = document.querySelector(".cs_property_details");
  if (!ANCHOR) return;
  var HOST = ANCHOR.parentElement || ANCHOR;

  var PACKS = ["private-real-estate", "commercial-hospitality", "land-developments"];

  function lang() {
    var l = (document.documentElement.getAttribute("lang") || "en").slice(0, 2);
    return ["en", "es", "ar", "zh"].indexOf(l) >= 0 ? l : "en";
  }
  function root() {
    var p = location.pathname.split("/").filter(Boolean);
    return (p[0] === "es" || p[0] === "ar" || p[0] === "zh") ? "../" : "./";
  }
  function t(o, l) {
    if (!o) return "";
    return typeof o === "string" ? o : (o[l] || o.en || "");
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function num(n, l) {
    try { return Number(n).toLocaleString(l === "zh" ? "zh-CN" : l === "ar" ? "ar" : l === "es" ? "es-ES" : "en-US"); }
    catch (e) { return String(n); }
  }
  function price(v, l) {
    if (!v) return UI.on_application[l];
    return "$" + num(v, l);
  }

  var UI = {
    on_application: { en: "Price upon application", es: "Precio a consulta",
                      ar: "السعر عند الطلب", zh: "价格面议" },
    overview:   { en: "Overview", es: "Resumen", ar: "نظرة عامة", zh: "概览" },
    details:    { en: "Asset details", es: "Datos del activo", ar: "بيانات الأصل", zh: "资产明细" },
    features:   { en: "Highlights", es: "Destacados", ar: "أبرز الملامح", zh: "亮点" },
    beds:       { en: "Bedrooms", es: "Dormitorios", ar: "غرف النوم", zh: "卧室" },
    baths:      { en: "Bathrooms", es: "Baños", ar: "الحمامات", zh: "浴室" },
    built:      { en: "Built area", es: "Superficie construida", ar: "المساحة المبنية", zh: "建筑面积" },
    land:       { en: "Plot", es: "Parcela", ar: "قطعة الأرض", zh: "地块" },
    hectares:   { en: "Land", es: "Suelo", ar: "الأرض", zh: "土地" },
    keys:       { en: "Keys", es: "Llaves", ar: "المفاتيح", zh: "客房" },
    berths:     { en: "Berths", es: "Amarres", ar: "المراسي", zh: "泊位" },
    category:   { en: "Category", es: "Categoría", ar: "الفئة", zh: "类别" },
    variant:    { en: "Type", es: "Variante", ar: "النوع", zh: "型别" },
    location:   { en: "Location", es: "Ubicación", ar: "الموقع", zh: "位置" },
    status:     { en: "Status", es: "Estado", ar: "الحالة", zh: "状态" },
    enquire:    { en: "Private enquiry", es: "Consulta reservada",
                  ar: "استفسار خاص", zh: "私人咨询" },
    back:       { en: "Back to the portfolio", es: "Volver al portafolio",
                  ar: "العودة إلى المحفظة", zh: "返回资产组合" },
    related:    { en: "Similar assets", es: "Activos similares",
                  ar: "أصول مشابهة", zh: "同类资产" }
  };

  /* La fotografia se sirve por derivadas, igual que en las tarjetas. */
  var WIDTHS = [480, 768, 1280, 1920, 2560];
  function picture(src, alt, R) {
    if (!src) return "";
    var m = /^(.*\/)([^\/]+)\.jpg$/.exec(src.replace(/^\//, ""));
    if (!m) return '<img src="' + esc(R + src.replace(/^\//, "")) + '" alt="' + esc(alt) + '" class="w-100">';
    var dir = m[1] + "r/", base = m[2];
    function set(ext) {
      return WIDTHS.map(function (w) {
        return R + dir + base + "-" + w + "." + ext + " " + w + "w";
      }).join(", ");
    }
    return (
      "<picture>" +
        '<source type="image/avif" srcset="' + esc(set("avif")) + '" sizes="(max-width: 991px) 94vw, 1140px">' +
        '<source type="image/webp" srcset="' + esc(set("webp")) + '" sizes="(max-width: 991px) 94vw, 1140px">' +
        '<img src="' + esc(R + dir + base + "-1280.jpg") + '" alt="' + esc(alt) +
        '" class="w-100" loading="eager" decoding="async">' +
      "</picture>"
    );
  }

  function row(label, value) {
    if (value === "" || value == null) return "";
    return '<li><span class="cs_semibold">' + esc(label) + ':</span><span>' + esc(value) + "</span></li>";
  }

  function build(it, ui, l, R, siblings) {
    var lc = it.language_content || {};
    var title = t(lc.title, l) || it.title;
    var place = [it.city, it.region, it.country].filter(Boolean).join(", ");
    var cat = t(lc.category, l) || it.subcategory;
    var vr = t(lc.variant, l) || it.variant;
    var status = t(lc.status, l) || it.status;
    var alt = title + " — " + cat + ", " + place;

    var feats = (it.features || []).map(function (f) { return t(f, l) || f; }).filter(Boolean);

    var strip = [];
    if (it.bedrooms)      strip.push([it.bedrooms, UI.beds[l]]);
    if (it.bathrooms)     strip.push([it.bathrooms, UI.baths[l]]);
    if (it.built_area_m2) strip.push([num(it.built_area_m2, l) + " m²", UI.built[l]]);
    if (it.land_area_m2)  strip.push([num(it.land_area_m2, l) + " m²", UI.land[l]]);
    else if (it.hectares) strip.push([num(it.hectares, l) + " ha", UI.hectares[l]]);
    if (it.hotel_keys)    strip.push([it.hotel_keys, UI.keys[l]]);
    if (it.berths)        strip.push([it.berths, UI.berths[l]]);

    var related = siblings.slice(0, 3).map(function (s) {
      var st = t((s.language_content || {}).title, l) || s.title;
      return (
        '<div class="col-md-4"><a class="xr_rel_card" href="property-details.html?id=' +
        encodeURIComponent(s.id) + '">' +
          '<span class="xr_rel_img">' + picture(s.hero_image, st, R) + "</span>" +
          '<span class="xr_rel_body"><strong>' + esc(st) + "</strong>" +
          "<em>" + esc([s.city, s.country].filter(Boolean).join(", ")) + "</em>" +
          "<b>" + esc(price(s.price_usd, l)) + "</b></span>" +
        "</a></div>"
      );
    }).join("");

    return (
      '<div class="cs_property_header cs_mb_40">' +
        '<div class="cs_property_header_left">' +
          '<h1 class="cs_fs_49 cs_mb_3">' + esc(title) + "</h1>" +
          '<div class="cs_property_location_text"><span class="mb-0">' + esc(place) + "</span></div>" +
        "</div>" +
        '<div class="cs_property_header_right">' +
          '<h3 class="cs_property_price cs_fs_39 cs_mb_8">' + esc(price(it.price_usd, l)) + "</h3>" +
          '<p class="cs_fs_20 cs_semibold mb-0">' + esc(cat) + " · " + esc(vr) + "</p>" +
        "</div>" +
      "</div>" +
      '<div class="cs_property_banner cs_radius_20 position-relative cs_mb_40">' +
        picture(it.hero_image, alt, R) +
        '<span class="cs_property_badge cs_primary_bg cs_fs_14 cs_white_color cs_medium cs_radius_20 position-absolute">' +
        esc(status) + "</span>" +
      "</div>" +
      '<ul class="cs_property_features_list cs_mp_0">' +
        strip.map(function (s) {
          return '<li><div class="cs_center_column text-center">' +
                 '<h2 class="cs_fs_20 cs_semibold mb-0">' + esc(s[0]) + "</h2>" +
                 '<span class="cs_fs_14">' + esc(s[1]) + "</span></div></li>";
        }).join("") +
      "</ul>" +
      '<div class="cs_height_50 cs_height_lg_40"></div>' +
      '<div class="row cs_gap_y_40">' +
        '<div class="col-lg-8"><div class="cs_single_property_content cs_radius_20">' +
          '<div class="cs_property_desc">' +
            '<h3 class="cs_fs_25 cs_semibold cs_mb_15">' + esc(UI.overview[l]) + "</h3>" +
            "<p>" + esc(t(it.long_description, l) || t(it.short_description, l)) + "</p>" +
          "</div>" +
          (feats.length
            ? '<div class="cs_property_amenties"><h3 class="cs_fs_25 cs_semibold cs_mb_15">' +
              esc(UI.features[l]) + "</h3>" +
              '<ul class="cs_property_amenties_list cs_mp_0">' +
              feats.map(function (f) { return "<li>" + esc(f) + "</li>"; }).join("") +
              "</ul></div>"
            : "") +
          '<div class="cs_property_info"><h3 class="cs_fs_25 cs_semibold cs_mb_15">' +
            esc(UI.details[l]) + "</h3>" +
            '<ul class="cs_property_info_list cs_mp_0">' +
              row(UI.category[l], cat) +
              row(UI.variant[l], vr) +
              row(UI.location[l], place) +
              row(UI.beds[l], it.bedrooms || "") +
              row(UI.baths[l], it.bathrooms || "") +
              row(UI.built[l], it.built_area_m2 ? num(it.built_area_m2, l) + " m²" : "") +
              row(UI.land[l], it.land_area_m2 ? num(it.land_area_m2, l) + " m²" : "") +
              row(UI.hectares[l], (!it.land_area_m2 && it.hectares) ? num(it.hectares, l) + " ha" : "") +
              row(UI.keys[l], it.hotel_keys || "") +
              row(UI.berths[l], it.berths || "") +
              row(UI.status[l], status) +
            "</ul>" +
          "</div>" +
        "</div></div>" +
        '<div class="col-lg-4"><aside class="cs_sidebar cs_style_1 cs_gray3_bg cs_radius_20">' +
          '<div class="cs_sidebar_widget">' +
            '<h3 class="cs_sidebar_widget_title cs_fs_20 cs_semibold cs_mb_16"><span>' +
            esc(UI.enquire[l]) + "</span></h3>" +
            '<p class="cs_secondary_color">' + esc(t(ui.demo_note, l)) + "</p>" +
            '<a href="' + R + 'private-enquiry/" class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_10">' +
            "<span>" + esc(UI.enquire[l]) + "</span></a>" +
            '<div class="cs_height_20"></div>' +
            '<a href="' + R + 'property-listing-search.html" class="xr_link">' + esc(UI.back[l]) + "</a>" +
          "</div>" +
        "</aside></div>" +
      "</div>" +
      (related
        ? '<div class="cs_height_70 cs_height_lg_50"></div>' +
          '<h3 class="cs_fs_25 cs_semibold cs_mb_15">' + esc(UI.related[l]) + "</h3>" +
          '<div class="row cs_gap_y_30 xr_rel_grid">' + related + "</div>"
        : "")
    );
  }

  var id = new URLSearchParams(location.search).get("id");
  var l = lang(), R = root();

  Promise.all(PACKS.map(function (f) {
    return fetch(R + "data/properties/" + f + ".json").then(function (r) {
      if (!r.ok) throw new Error(f + ": " + r.status);
      return r.json();
    });
  })).then(function (packs) {
    var all = [], ui = packs[0].ui || {};
    ui.demo_note = ui.demo_note || packs[0].demo_note;
    packs.forEach(function (p) { all = all.concat(p.items || []); });

    var it = id ? all.filter(function (x) { return x.id === id; })[0] : null;
    if (!it) {
      /* Sin ?id= o con un id que no existe, la plantilla enseñaba su ficha de
         ejemplo de setenta mil dolares. Se manda al buscador del portafolio,
         que es lo que la persona venia a ver. */
      location.replace(R + "property-listing-search.html");
      return;
    }
    var siblings = all.filter(function (x) {
      return x.subcategory === it.subcategory && x.id !== it.id;
    });

    /* Se conserva el envoltorio .cs_property_details: toda la hoja de estilos
       de la plantilla cuelga de esa clase (cabecera a dos columnas, tira de
       caracteristicas, posicion del distintivo). Sin ella la ficha se
       desmontaba en una columna y el distintivo se salia del ancho. */
    HOST.innerHTML = '<div class="cs_property_details">' +
                     build(it, ui, l, R, siblings) + "</div>";

    var title = t((it.language_content || {}).title, l) || it.title;
    document.title = title + " | XARU HOME";

    /* Las secciones de la plantilla que no aplican a esta cartera: hipoteca,
       colegios cercanos, plano de planta, "propiedades relacionadas" de
       ejemplo. Se retiran en vez de dejarse con cifras inventadas. */
    [".cs_property_mortgage", ".cs_property_nearby", ".cs_property_floor",
     ".cs_property_surroundings", ".cs_property_financial_info"].forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (el) { el.remove(); });
    });
    var rel = document.querySelector("section.cs_slider.cs_style_1.cs_slider_gap_24");
    if (rel) rel.remove();
  }).catch(function (err) {
    if (window.console) console.warn("[xaru-detail]", err);
  });
})();
