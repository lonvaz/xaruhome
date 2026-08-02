/*
 * XARU HOME — acceso a guardados desde la cabecera
 * =============================================================
 * Un corazón con su contador en la cabecera de todas las páginas, que lleva al
 * panel del comprador. Sin él, guardar un activo era una acción sin destino:
 * el usuario pulsaba el corazón y no volvía a encontrar lo guardado.
 *
 * Se inyecta desde JavaScript en lugar de escribirse en la plantilla porque la
 * cabecera la generan cinco constructores distintos y algunas páginas
 * heredadas no pasan por ninguno. Un solo fichero cubre las 400 páginas.
 *
 * El contador se recalcula al volver a la pestaña y cuando otra pestaña
 * modifica el almacenamiento, así que dos ventanas abiertas no se contradicen.
 */
(function () {
  "use strict";

  function lang() {
    var l = (document.documentElement.getAttribute("lang") || "en").slice(0, 2);
    return ["en", "es", "ar", "zh"].indexOf(l) >= 0 ? l : "en";
  }
  var L = lang();
  var PR = "/" + (L === "en" ? "" : L + "/");

  var LBL = {
    en: "Saved assets", es: "Activos guardados",
    ar: "الأصول المحفوظة", zh: "收藏的资产"
  };
  var label = LBL[L] || LBL.en;

  function count() {
    try {
      var f = JSON.parse(localStorage.getItem("xaru_favorites") || "[]");
      return Array.isArray(f) ? f.length : 0;
    } catch (e) { return 0; }
  }

  function mount() {
    var list = document.querySelector(".cs_right_nav_list");
    if (!list || document.querySelector(".xr_saved_link")) return null;
    var li = document.createElement("li");
    li.className = "xr_saved_li";
    li.innerHTML =
      '<a class="xr_saved_link" href="' + PR + 'real-estate/account/" aria-label="' +
      label + '" title="' + label + '">' +
      '<i class="fa-regular fa-heart" aria-hidden="true"></i>' +
      '<b class="xr_saved_n" hidden></b></a>';
    // Antes de los dos botones de llamada a la acción: es un acceso, no una CTA.
    list.insertBefore(li, list.firstChild);
    return li;
  }

  function paint() {
    var b = document.querySelector(".xr_saved_n");
    if (!b) return;
    var n = count();
    b.textContent = n > 99 ? "99+" : String(n);
    b.hidden = !n;
    var a = b.closest("a");
    if (a) a.classList.toggle("is-on", !!n);
    var i = a && a.querySelector("i");
    if (i) i.className = (n ? "fa-solid" : "fa-regular") + " fa-heart";
  }

  function start() {
    if (!mount()) {
      if (!document.querySelector(".xr_saved_link")) return;
    }
    paint();
    window.addEventListener("storage", function (e) {
      if (!e.key || e.key === "xaru_favorites") paint();
    });
    document.addEventListener("visibilitychange", function () {
      if (!document.hidden) paint();
    });
    // El corazón de cada tarjeta escribe en el mismo sitio; el contador se
    // actualiza en el mismo gesto en lugar de esperar a recargar.
    document.addEventListener("click", function (e) {
      if (e.target.closest("[data-fav]")) setTimeout(paint, 0);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
