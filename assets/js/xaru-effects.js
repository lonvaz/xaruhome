/*
 * XARU HOME — Hompark effects layer (vanilla, no new deps except Swiper)
 * 01. Text rotator (port of Hompark text-rotater.js — 1200ms/word, 500ms fade)
 * 02. Entrance choreography (double-curtain preloader exit + header/hero cascade)
 * 03. Stellar-like continuous parallax (rAF, Lenis-compatible)
 * 04. Hero Swiper (fraction 1/3, rotated PREV/NEXT, bg parallax 1.15)
 * 05. Smooth anchor scroll, 1300ms (Hompark timing)
 * 06. Floating form labels (.label-up)
 */
(function () {
  "use strict";

  /* ============ 01. Text rotator ============ */
  function initRotators() {
    var els = document.querySelectorAll(".xr_text_rotater[data-text]");
    els.forEach(function (el) {
      var words = el
        .getAttribute("data-text")
        .split("|")
        .map(function (w) {
          return w.trim();
        })
        .filter(Boolean);
      if (words.length < 2) return;
      var i = 0;
      el.style.transition = "opacity 500ms ease-in-out";
      el.textContent = words[0];
      setInterval(function () {
        el.style.opacity = "0";
        setTimeout(function () {
          i = (i + 1) % words.length;
          el.textContent = words[i];
          el.style.opacity = "1";
        }, 500);
      }, 1200);
    });
  }

  /* ============ 02. Entrance choreography ============ */
  var loaded = false;
  function pageLoaded() {
    if (loaded) return;
    loaded = true;
    document.body.classList.add("page-loaded");
    var pre = document.querySelector(".cs_preloader");
    if (pre) {
      setTimeout(function () {
        pre.style.display = "none";
      }, 2600);
    }
  }
  window.addEventListener("load", pageLoaded);
  /* Safety: never trap the user behind the curtain */
  setTimeout(pageLoaded, 4000);

  /* ============ 03. Stellar-like parallax ============ */
  var pxItems = [];
  function collectParallax() {
    pxItems = [];
    document.querySelectorAll("[data-xr-parallax]").forEach(function (el) {
      var ratio = parseFloat(el.getAttribute("data-xr-parallax"));
      if (!ratio || ratio === 1) return;
      var anchor = el.closest("[data-xr-parallax-anchor]") || el.parentElement;
      pxItems.push({ el: el, ratio: ratio, anchor: anchor });
    });
  }
  function runParallax() {
    if (!pxItems.length) return;
    var vh = window.innerHeight;
    if (window.innerWidth < 992) {
      /* keep mobile calm + avoid overflow issues */
      pxItems.forEach(function (it) {
        it.el.style.transform = "";
      });
      return;
    }
    pxItems.forEach(function (it) {
      var r = it.anchor.getBoundingClientRect();
      if (r.bottom < -vh || r.top > vh * 2) return;
      var offset = r.top + r.height / 2 - vh / 2;
      var y = offset * (1 - it.ratio);
      var max = r.height * 0.12;
      if (y > max) y = max;
      if (y < -max) y = -max;
      it.el.style.transform = "translate3d(0," + y.toFixed(1) + "px,0)";
    });
  }
  function rafLoop() {
    runParallax();
    requestAnimationFrame(rafLoop);
  }

  /* ============ 04. Hero Swiper ============ */
  function initHeroSlider() {
    var sliderEl = document.querySelector(".xr_hero_slider");
    if (!sliderEl || typeof Swiper === "undefined") return;
    /* data-background → background-image on the parallax bg layer */
    sliderEl.querySelectorAll(".xr_slide_bg[data-background]").forEach(function (bg) {
      bg.style.backgroundImage = "url(" + bg.getAttribute("data-background") + ")";
    });
    new Swiper(sliderEl, {
      loop: true,
      speed: 600,
      allowTouchMove: false,
      autoplay: { delay: 4500, disableOnInteraction: false },
      pagination: { el: ".xr_hero_fraction", type: "fraction" },
      navigation: { nextEl: ".xr_hero_next", prevEl: ".xr_hero_prev" },
    });
  }

  /* ============ 05. Smooth anchor scroll (1300ms, Hompark) ============ */
  function initAnchorScroll() {
    document.addEventListener("click", function (e) {
      var link = e.target.closest ? e.target.closest('a[href^="#"]') : null;
      if (!link) return;
      var id = link.getAttribute("href");
      if (id.length < 2) return;
      var target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      var start = window.pageYOffset;
      var end = target.getBoundingClientRect().top + start - 90;
      var t0 = null;
      var dur = 1300;
      function ease(t) {
        /* cubic-bezier(.86,0,.07,1) approximation — easeInOutQuint */
        return t < 0.5 ? 16 * t * t * t * t * t : 1 - Math.pow(-2 * t + 2, 5) / 2;
      }
      function step(ts) {
        if (!t0) t0 = ts;
        var p = Math.min(1, (ts - t0) / dur);
        window.scrollTo(0, start + (end - start) * ease(p));
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }

  /* ============ 06. Floating labels ============ */
  function initFloatingLabels() {
    document
      .querySelectorAll(".xr_float_form .cs_form_field")
      .forEach(function (field) {
        var ph = field.getAttribute("placeholder");
        if (!ph) return;
        field.removeAttribute("placeholder");
        var wrap = document.createElement("div");
        wrap.className = "xr_float_field";
        field.parentNode.insertBefore(wrap, field);
        wrap.appendChild(field);
        var label = document.createElement("span");
        label.className = "xr_float_label";
        label.textContent = ph;
        wrap.appendChild(label);
        function check() {
          if (field.value !== "" || document.activeElement === field) {
            label.classList.add("label-up");
          } else {
            label.classList.remove("label-up");
          }
        }
        field.addEventListener("focus", check);
        field.addEventListener("blur", check);
        field.addEventListener("input", check);
        check();
      });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initRotators();
    initHeroSlider();
    initAnchorScroll();
    initFloatingLabels();
    collectParallax();
    requestAnimationFrame(rafLoop);
  });
})();
