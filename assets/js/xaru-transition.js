/*
 * XARU HOME — cortina de transición entre páginas
 * =============================================================
 * QUÉ HACE Y DÓNDE
 * ----------------
 * La cortina es un recurso editorial: acompaña el paso de una puerta a otra
 * dentro del relato del sitio. Dentro del marketplace no pinta nada, porque
 * ahí la navegación es de trabajo —abrir una ficha, volver, abrir otra— y
 * cualquier retardo se lee como lentitud, no como cuidado.
 *
 * POR QUÉ SE REESCRIBIÓ
 * ---------------------
 * La versión anterior se activaba solo con enlaces terminados en `.html`. En
 * un sitio de carpetas eso significaba que la cortina saltaba exactamente en
 * un sitio: al pulsar una propiedad. Es decir, la acción más repetida del
 * portal era la única que tardaba 1,3 s, y el resto iban instantáneas. Esa
 * incoherencia se lee como un fallo, y lo era.
 *
 * Ahora la regla es al revés y es explícita: la cortina acompaña la navegación
 * editorial —menú, puertas, artículos— y NUNCA la del inventario. Y dura menos
 * de medio segundo, que es lo que aguanta una transición antes de convertirse
 * en una espera.
 */
(function () {
  "use strict";

  var overlay = document.querySelector(".xr_transition_overlay");
  if (!overlay) return;

  var MS = 480;

  /* Superficies del marketplace: dentro de ellas, nunca hay cortina. */
  var PORTAL = [
    "[data-marketplace]", "[data-mp-home]", "[data-directory]", "[data-profile]",
    "[data-projects]", "[data-project]", "[data-account]", "[data-console]",
    ".cs_property_details", ".xr_pdp_dock", ".xr_pdp_nav", ".xr_mp_nav"
  ].join(",");

  /* Destinos que son inventario: tampoco, se venga de donde se venga. */
  function isInventory(path) {
    return /property-details\.html/i.test(path) ||
      /\/real-estate\/(buy|rent|land|map|search|commercial|account|office|administration|agent|agency|developer|project|agents|agencies|developers|new-projects)(\/|$)/i.test(path);
  }

  function clear() { overlay.classList.remove("active"); }
  window.addEventListener("pageshow", clear);
  window.addEventListener("popstate", clear);

  document.addEventListener("click", function (e) {
    if (e.defaultPrevented) return;
    if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;

    var link = e.target.closest ? e.target.closest("a[href]") : null;
    if (!link) return;

    var href = link.getAttribute("href");
    if (!href) return;

    /* Nada que no sea una navegación real a otra página de este sitio. */
    if (href.charAt(0) === "#") return;
    if (/^(javascript:|mailto:|tel:|sms:|whatsapp:)/i.test(href)) return;
    if (link.target && link.target !== "_self") return;
    if (link.hasAttribute("download")) return;

    var url;
    try { url = new URL(link.href, location.href); } catch (err) { return; }
    if (url.origin !== location.origin) return;
    /* Mismo documento con ancla distinta: lo resuelve el navegador. */
    if (url.pathname === location.pathname && url.hash) return;

    /* Componentes de la plantilla que usan <a> como disparador. */
    if (link.classList.contains("cs_open_modal") ||
        link.classList.contains("cs_video_open") ||
        link.classList.contains("cs_close_modal") ||
        link.getAttribute("data-bs-toggle") ||
        link.getAttribute("role") === "tab" ||
        link.closest(".cs_tabs") ||
        link.closest(".cs_lightgallery")) return;

    /* Las dos reglas nuevas: ni dentro del portal, ni hacia el inventario. */
    if (link.closest(PORTAL)) return;
    if (isInventory(url.pathname)) return;

    e.preventDefault();
    overlay.classList.add("active");
    /* Red a prueba de fallos: si la navegación no llega a ocurrir, la cortina
       se retira sola en lugar de dejar la pantalla en negro. */
    var done = false;
    setTimeout(function () {
      if (done) return;
      done = true;
      window.location.href = link.href;
    }, MS);
    setTimeout(clear, MS + 4000);
  }, false);
})();
