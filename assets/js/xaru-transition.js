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

  /* LA REGLA
     --------
     La cortina marca el paso de un pilar a otro: las seis puertas de primer
     nivel y la portada. Nada más. Cualquier botón interno —dentro de Real
     Estate o de cualquier otra puerta— navega sin cortina, porque ahí no se
     está cambiando de sección, se está trabajando dentro de una.

     Es una lista blanca, no una lista de exclusiones. La versión anterior
     excluía casos uno a uno y siempre se escapaba alguno: /real-estate/sold/,
     /real-estate/private-properties/ y /real-estate/commercial-hospitality/
     seguían disparándola porque no estaban en la lista de excepciones. Con una
     lista blanca, lo que no está declarado sencillamente no la activa. */
  var DOORS = [
    "", "real-estate", "developments", "capital",
    "business-infrastructure", "company", "insights"
  ];

  function isDoor(pathname) {
    var parts = pathname.split("/").filter(Boolean);
    /* Se descarta el prefijo de idioma: /es/capital/ es la misma puerta. */
    if (parts.length && ["es", "ar", "zh"].indexOf(parts[0]) >= 0) parts.shift();
    /* Una puerta es exactamente un segmento, o ninguno (la portada). */
    if (parts.length > 1) return false;
    return DOORS.indexOf(parts[0] || "") >= 0;
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

    /* La regla: solo de pilar a pilar. Si el destino no es una puerta, no hay
       cortina; y si se sale de la puerta en la que ya se está, tampoco, porque
       eso es moverse dentro de la misma sección. */
    if (!isDoor(url.pathname)) return;
    if (url.pathname === location.pathname) return;

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
