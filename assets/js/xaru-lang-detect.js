/* XARU HOME — client-side language auto-detection.
 * SEO-safe: no cloaking, no bot-specific behaviour, no change to
 * hreflang/canonical. Pure client redirect, at most once per session,
 * never against an explicit user choice. Runs synchronously in <head>
 * so the decision is taken before heavy content paints (no FOUC).
 */
(function () {
  "use strict";

  // Only these 12 pages exist in all four languages. Anything else
  // (login, register, error, dashboards…) must never be auto-redirected.
  var TRANSLATABLE = {
    "index.html": 1,
    "property-listing-buy.html": 1,
    "property-listing-rent.html": 1,
    "property-listing-search.html": 1,
    "single-property-v1.html": 1,
    "property-details.html": 1,
    "agents-list.html": 1,
    "about-us.html": 1,
    "blog.html": 1,
    "blog-details.html": 1,
    "contact.html": 1,
    "faq.html": 1
  };

  // navigator language tag -> supported site language (es/ar/zh, else en).
  function mapLang(tag) {
    if (!tag) return null;
    tag = String(tag).toLowerCase();
    if (tag.indexOf("es") === 0) return "es";
    if (tag.indexOf("ar") === 0) return "ar";
    if (tag.indexOf("zh") === 0) return "zh";
    if (tag.indexOf("en") === 0) return "en";
    return null;
  }

  function detectDeviceLang() {
    var list = (navigator.languages && navigator.languages.length)
      ? navigator.languages
      : [navigator.language || navigator.userLanguage];
    for (var i = 0; i < list.length; i++) {
      var m = mapLang(list[i]);
      if (m) return m;      // first tag that maps to a supported language
    }
    return "en";            // anything unsupported -> English (root)
  }

  // Language of the current page, derived from its path (/es/… /ar/… /zh/…).
  function currentLang(segs) {
    if (segs.length && (segs[0] === "es" || segs[0] === "ar" || segs[0] === "zh")) {
      return segs[0];
    }
    return "en";
  }

  try {
    // (a) User already chose a language manually — respect it forever.
    if (localStorage.getItem("xaru_lang")) return;
  } catch (e) { /* storage blocked: fall through, still guarded by session flag */ }

  try {
    // (b) Already auto-redirected once this session — never loop.
    if (sessionStorage.getItem("xaru_autoredir")) return;
  } catch (e) { return; } // no sessionStorage -> can't guard loops, so do nothing

  var path = location.pathname;
  var rawSegs = path.split("/");
  var file = rawSegs[rawSegs.length - 1];
  var isDir = !file;                              // trailing slash -> clean directory URL
  var segs = rawSegs.filter(function (s) { return s.length; });

  var cur = currentLang(segs);
  var want = detectDeviceLang();

  // (b/c) Device language already matches the page, or unsupported -> stop.
  if (want === cur) return;

  var target;
  if (isDir) {
    // Clean directory URLs (doors, divisions, company, insights, fichas…) are
    // generated in all four languages with the SAME path under /es/ /ar/ /zh/.
    var rest = segs.slice(cur === "en" ? 0 : 1);  // path without the lang prefix
    target = (want === "en" ? "/" : "/" + want + "/") + rest.join("/")
           + (rest.length ? "/" : "") + location.search + location.hash;
  } else {
    // (c) Only redirect the 12 fully-translated legacy .html pages.
    if (!TRANSLATABLE[file]) return;
    target = (want === "en" ? "/" + file : "/" + want + "/" + file)
           + location.search + location.hash;
  }

  // Mark the session and redirect once (replace: no history entry, no back-loop).
  try { sessionStorage.setItem("xaru_autoredir", "1"); } catch (e) { return; }
  location.replace(target);
})();
