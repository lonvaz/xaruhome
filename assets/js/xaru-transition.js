/*
 * XARU HOME — page transition module (ported from Hompark)
 * Isolated: intercepts ONLY plain same-origin links to .html pages.
 * Never touches: hashes/anchors, tabs, modals, cs_* component triggers,
 * new-tab links, downloads, or javascript: links.
 */
(function () {
  "use strict";

  var overlay = document.querySelector(".xr_transition_overlay");
  if (!overlay) return;

  // Reset overlay when arriving on the page (also on bfcache restore)
  window.addEventListener("pageshow", function () {
    overlay.classList.remove("active");
  });

  document.addEventListener(
    "click",
    function (e) {
      if (e.defaultPrevented) return;
      if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;

      var link = e.target.closest ? e.target.closest("a[href]") : null;
      if (!link) return;

      var href = link.getAttribute("href");
      if (!href) return;

      // Exclusions: anchors, protocols, new tabs, downloads, component triggers
      if (href.indexOf("#") === 0) return;
      if (/^(javascript:|mailto:|tel:|https?:\/\/)/i.test(href) && link.host !== window.location.host) return;
      if (href.indexOf("javascript:") === 0 || href.indexOf("mailto:") === 0 || href.indexOf("tel:") === 0) return;
      if (link.target && link.target !== "_self") return;
      if (link.hasAttribute("download")) return;
      if (href.indexOf("#") !== -1) return; // page.html#anchor — let native/lenis handle it
      if (!/\.html(\?.*)?$/i.test(href)) return;

      // Skip anything wired to Xproperty JS components (modals, video, tabs, gallery)
      if (
        link.classList.contains("cs_open_modal") ||
        link.classList.contains("cs_video_open") ||
        link.classList.contains("cs_close_modal") ||
        link.closest(".cs_tabs") ||
        link.closest(".cs_lightgallery") ||
        link.getAttribute("data-bs-toggle") ||
        link.getAttribute("role") === "tab"
      ) {
        return;
      }

      e.preventDefault();
      overlay.classList.add("active");
      setTimeout(function () {
        window.location.href = href;
      }, 1300);
    },
    false
  );
})();
