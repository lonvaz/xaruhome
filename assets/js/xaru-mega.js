/* XARU HOME — mega-menu controller (Phase 1 architecture)
   Desktop (>=1200px): CSS :hover opens each 4-door panel; this file adds
   keyboard + click support and closes panels on outside-click / Esc.
   Mobile (<=1199px): the mega nav becomes an accordion inside the hamburger
   slide-out. Each door's caret toggle expands its panel in place. The existing
   language selector row (.cs_mobile_lang) is left untouched. RTL-safe. */
(function () {
  "use strict";
  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }
  ready(function () {
    var items = Array.prototype.slice.call(
      document.querySelectorAll(".xr_mega_item")
    );
    if (!items.length) return;

    function closeAll(except) {
      items.forEach(function (li) {
        if (li !== except) li.classList.remove("is-open");
      });
    }

    items.forEach(function (li) {
      var toggle = li.querySelector(".xr_mega_toggle");
      var link = li.querySelector(".xr_mega_link");

      // Caret toggle (visible on mobile) — expand/collapse the panel in place.
      if (toggle) {
        toggle.addEventListener("click", function (e) {
          e.preventDefault();
          e.stopPropagation();
          var open = li.classList.contains("is-open");
          closeAll(open ? null : li);
          li.classList.toggle("is-open", !open);
          toggle.setAttribute("aria-expanded", String(!open));
        });
      }

      // Desktop keyboard access: Enter/Space on the door link opens the panel
      // (without blocking navigation on a normal click).
      if (link) {
        link.addEventListener("keydown", function (e) {
          if (e.key === " " || e.key === "Spacebar") {
            e.preventDefault();
            var open = li.classList.contains("is-open");
            closeAll(open ? null : li);
            li.classList.toggle("is-open", !open);
          }
        });
      }
    });

    // Outside click closes any open desktop panel.
    document.addEventListener("click", function (e) {
      if (!e.target.closest(".xr_mega_item")) closeAll(null);
    });
    // Esc closes everything.
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeAll(null);
    });
  });
})();
