(function ($) {
  "use strict";

  /*
  |=====================================================================
  | Template Name: Xproperty
  | Author: Laralink
  | Version: 1.0.0
  |=====================================================================
  |=====================================================================
  | TABLE OF CONTENTS:
  |=====================================================================
  |
  | 01. Preloader
  | 02. Mobile Menu
  | 03. Sticky Header
  | 04. Dynamic Background
  | 05. Slick Slider
  | 06. Language Select
  | 07. Search Modal Toggle
  | 08. Smooth Page Scroll (Lenis)
  | 09. Counter Animation
  | 10. Modal Video
  | 11. Review
  | 12. Tabs
  | 13. Accordian
  | 14. heart toggle
  | 15. Date And Time Picker
  | 16. Apartment Finding Function
  | 17. Pricing value Toggle
  | 18. Light Gallery
  | 19. Load More Portfolio Items
  | 20. Data Table
  | 21. Scroll Up
  | 22. Dynamic contact form
  | 23. AOS Animation
  |
  */

  /*====================================================================
    Scripts initialization
  ======================================================================*/
  $.exists = function (selector) {
    return $(selector).length > 0;
  };

  $(window).on("load", function () {
    preloader();
  });
  $(window).on("scroll", function () {
    stickyHeader();
    showScrollUp();
  });

  $(function () {
    mainNav();
    stickyHeader();
    dynamicBackground();
    slickInit();
    quantityInit();
    modalToggle();
    smoothScroll();
    counterInit();
    modalVideo();
    review();
    tabs();
    accordian();
    elementToggle();
    dateTimePicker();
    apartmentShow();
    pricingToggle();
    lightGallery();
    loadMore();
    dataTable();
    scrollUp();
    aosInit();
    $(".tom_select").each(function () {
      new TomSelect(this, {
        create: false,
        onDropdownOpen: function (dropdown) {
          dropdown.classList.add("active");
        },
        onDropdownClose: function (dropdown) {
          dropdown.classList.remove("active");
        },
      });
    });
    if ($.exists(".cs_getting_year")) {
      const date = new Date();
      $(".cs_getting_year").text(date.getFullYear());
    }
  });
  /*======================================================================
   Run on window resize
  =======================================================================*/
  $(window).on("resize", function () {
    const mobileWidth = 1199;
    if ($(window).width() >= mobileWidth) {
    }
  });

  /*======================================================================
    01. Preloader
  ========================================================================*/
  function preloader() {
    // XARU: Hompark-style double-curtain exit — CSS driven via body.page-loaded
    // (class is added by xaru-effects.js; fallback here for safety)
    $("body").addClass("page-loaded");
  }

  /*======================================================================
    02. Mobile Menu
  ========================================================================*/
  function mainNav() {
    $(".cs_nav").append('<span class="cs_menu_toggle"><span></span></span>');
    $(".menu-item-has-children").append(
      '<span class="cs_menu_dropdown_toggle"><span></span></span>'
    );
    $(".cs_menu_toggle").on("click", function () {
      $(this)
        .toggleClass("active")
        .siblings(".cs_nav_list_wrap")
        .toggleClass("active")
        .children(".cs_close_nav")
        .toggleClass("active");
    });
    $(".cs_close_nav").on("click", function () {
      $(this)
        .toggleClass("active")
        .parent(".cs_nav_list_wrap")
        .toggleClass("active")
        .siblings(".cs_menu_toggle")
        .toggleClass("active");
    });
    $(".cs_menu_dropdown_toggle").on("click", function () {
      $(this).toggleClass("active").siblings("ul").slideToggle();
      $(this).parent().toggleClass("active");
    });
  }

  /*======================================================================
    03. Sticky Header
  ========================================================================*/
  function stickyHeader() {
    var scroll = $(window).scrollTop();
    if (scroll >= 10) {
      $(".cs_sticky_header").addClass("cs_sticky_active");
    } else {
      $(".cs_sticky_header").removeClass("cs_sticky_active");
    }
  }

  /*======================================================================
    04. Dynamic Background
  ========================================================================*/
  function dynamicBackground() {
    $("[data-src]").each(function () {
      var src = $(this).attr("data-src");
      $(this).css({
        "background-image": "url(" + src + ")",
      });
    });
  }

  /*======================================================================
    05. Slick Slider
  ========================================================================*/
  function slickInit() {
    if ($.exists(".cs_slider")) {
      $(".cs_slider").each(function () {
        // Slick Variable
        var $ts = $(this).find(".cs_slider_container");
        var $slickActive = $(this).find(".cs_slider_wrapper");
        var $status = $(this).find(".cs_slider_number");

        // Auto Play
        var autoPlayVar = parseInt($ts.attr("data-autoplay"), 10);
        // Auto Play Time Out
        var autoplaySpdVar = 3000;
        if (autoPlayVar > 1) {
          autoplaySpdVar = autoPlayVar;
          autoPlayVar = 1;
        }
        // Slide Change Speed
        var speedVar = parseInt($ts.attr("data-speed"), 10);
        // Slider Loop
        var loopVar = Boolean(parseInt($ts.attr("data-loop"), 10));
        // Slider Center
        var centerVar = Boolean(parseInt($ts.attr("data-center"), 10));
        // Variable Width
        var variableWidthVar = Boolean(
          parseInt($ts.attr("data-variable-width"), 10)
        );
        // Pagination
        var paginaiton = $(this)
          .find(".cs_pagination")
          .hasClass("cs_pagination");
        // Slide Per View
        var slidesPerView = $ts.attr("data-slides-per-view");
        if (slidesPerView == 1) {
          slidesPerView = 1;
        }
        if (slidesPerView == "responsive") {
          var slidesPerView = parseInt($ts.attr("data-add-slides"), 10);
          var lgPoint = parseInt($ts.attr("data-lg-slides"), 10);
          var mdPoint = parseInt($ts.attr("data-md-slides"), 10);
          var smPoint = parseInt($ts.attr("data-sm-slides"), 10);
          var xsPoing = parseInt($ts.attr("data-xs-slides"), 10);
        }
        // Fade Slider
        var fadeVar = parseInt($($ts).attr("data-fade-slide"));
        fadeVar === 1 ? (fadeVar = true) : (fadeVar = false);

        /* Start Count Slide Number */
        $slickActive.on(
          "init reInit afterChange",
          function (event, slick, currentSlide, nextSlide) {
            var i = (currentSlide ? currentSlide : 0) + 1;
            $status.html(
              `<span class="cs_current_number">${i}</span> <span class="cs_slider_number_seperator"></span> <span class="cs_total_numbers">${slick.slideCount}</span>`
            );
          }
        );
        /* End Count Slide Number */

        // Slick Active Code
        $slickActive.slick({
          rtl: $("html").attr("dir") === "rtl",
          autoplay: autoPlayVar,
          dots: paginaiton,
          centerPadding: "28%",
          speed: speedVar,
          infinite: loopVar,
          autoplaySpeed: autoplaySpdVar,
          centerMode: centerVar,
          fade: fadeVar,
          prevArrow: $(this).find(".cs_left_arrow"),
          nextArrow: $(this).find(".cs_right_arrow"),
          appendDots: $(this).find(".cs_pagination"),
          slidesToShow: slidesPerView,
          variableWidth: variableWidthVar,
          swipeToSlide: true,
          responsive: [
            {
              breakpoint: 1400,
              settings: {
                slidesToShow: lgPoint,
              },
            },
            {
              breakpoint: 1200,
              settings: {
                slidesToShow: mdPoint,
              },
            },
            {
              breakpoint: 992,
              settings: {
                slidesToShow: smPoint,
              },
            },
            {
              breakpoint: 768,
              settings: {
                slidesToShow: xsPoing,
              },
            },
          ],
        });
      });
    }
  }
  /*======================================================================
    06. Language Select
  ========================================================================*/
  function quantityInit() {
    // Language switcher: open/close the dropdown. The items are now real
    // <a> links to the per-language folder index (see /es/, /ar/), so no
    // decorative flag-swap is performed — navigation handles the change.
    $(".cs_language_switcher").on("click", function (e) {
      e.stopPropagation();
      $(".cs_language_dropdown").slideToggle(250);
    });
    // Close the dropdown when clicking outside of it.
    $(document).on("click", function (e) {
      if (!$(e.target).closest(".cs_language_select").length) {
        $(".cs_language_dropdown").slideUp(200);
      }
    });
    // Persist the manual choice so the auto-detector never overrides it.
    // Desktop dropdown + mobile-menu language row share this handler; the
    // href navigation is left intact (we only write localStorage first).
    $(document).on(
      "click",
      ".cs_language_dropdown a, .cs_mobile_lang a",
      function () {
        var lang = ($(this).attr("data-lang") || "").toLowerCase();
        if (lang) {
          try {
            localStorage.setItem("xaru_lang", lang);
          } catch (e) {}
        }
      }
    );
  }
  /*======================================================================
    07. Search Modal Toggle
  ========================================================================*/
  function modalToggle() {
    $(".cs_open_modal").on("click", function () {
      $(".cs_advanced_search_modal").addClass("active");
      $("body").addClass("scroll_off");
    });
    $(".cs_close_modal").on("click", function () {
      $(".cs_advanced_search_modal").removeClass("active");
      $("body").removeClass("scroll_off");
    });
  }
  /*======================================================================
    08. Smooth Page Scroll
  ========================================================================*/
  function smoothScroll() {
    const lenis = new Lenis({
      duration: 1.5,
      smooth: true,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    });

    function raf(time) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }

    requestAnimationFrame(raf);
  }
  /*=====================================================================
    09. Counter Animation
  =======================================================================*/
  function counterInit() {
    if ($.exists(".odometer")) {
      $(window).on("scroll", function () {
        function winScrollPosition() {
          var scrollPos = $(window).scrollTop(),
            winHeight = $(window).height();
          var scrollPosition = Math.round(scrollPos + winHeight / 1.2);
          return scrollPosition;
        }

        $(".odometer").each(function () {
          var elemOffset = $(this).offset().top;
          if (elemOffset < winScrollPosition()) {
            $(this).html($(this).data("count-to"));
          }
        });
      });
    }
  }
  /*=====================================================================
    10. Modal Video
  =======================================================================*/
  function modalVideo() {
    if ($.exists(".cs_video_open")) {
      $("body").append(`
        <div class="cs_video_popup">
          <div class="cs_video_popup-overlay"></div>
          <div class="cs_video_popup-content">
            <div class="cs_video_popup-layer"></div>
            <div class="cs_video_popup_container">
              <div class="cs_video_popup-align">
                <div class="embed-responsive embed-responsive-16by9">
                  <iframe class="embed-responsive-item" src="about:blank"></iframe>
                </div>
              </div>
              <div class="cs_video_popup_close"></div>
            </div>
          </div>
        </div>
      `);
      $(document).on("click", ".cs_video_open", function (e) {
        e.preventDefault();
        var video = $(this).attr("href");

        $(".cs_video_popup_container iframe").attr("src", `${video}`);

        $(".cs_video_popup").addClass("active");
      });
      $(".cs_video_popup_close, .cs_video_popup-layer").on(
        "click",
        function (e) {
          $(".cs_video_popup").removeClass("active");
          $("html").removeClass("overflow-hidden");
          $(".cs_video_popup_container iframe").attr("src", "about:blank");
          e.preventDefault();
        }
      );
    }
  }
  /*=====================================================================
    11. Review
  =======================================================================*/
  function review() {
    $(".cs_rating").each(function () {
      var review = $(this).data("rating");
      var reviewVal = review * 20 + "%";
      $(this).find(".cs_rating_percentage").css("width", reviewVal);
    });
  }
  /*====================================================================
    12. Tabs
  =====================================================================*/
  function tabs() {
    $(".cs_tab_links a").on("click", function (e) {
      var currentAttrValue = $(this).attr("href");
      //Tab and slider both activation code
      $(".cs_tabs " + currentAttrValue)
        .addClass("active")
        .siblings()
        .removeClass("active");
      $(this).parents("li").addClass("active").siblings().removeClass("active");
      e.preventDefault();
    });
  }
  /*====================================================================
    13. Accordian
  ======================================================================*/
  function accordian() {
    $(".cs_accordian").children(".cs_accordian_body").hide();
    $(".cs_accordian.active").children(".cs_accordian_body").show();
    $(".cs_accordian_head").on("click", function () {
      $(this)
        .parent(".cs_accordian")
        .siblings()
        .children(".cs_accordian_body")
        .slideUp(250);
      $(this).siblings().slideDown(250);
      $(this)
        .parent()
        .parent()
        .siblings()
        .find(".cs_accordian_body")
        .slideUp(250);
      /* Accordian Active Class */
      $(this).parents(".cs_accordian").addClass("active");
      $(this).parent(".cs_accordian").siblings().removeClass("active");
    });
  }
  /*=====================================================================
    14. heart toggle
  =======================================================================*/
  function elementToggle() {
    $(".cs_heart_toggler i").on("click", function () {
      $(this).toggleClass("fa-solid");
    });
    // Category Widget Toggle
    $(".cs_sidebar_widget_title").on("click", function () {
      $(this)
        .toggleClass("active")
        .siblings(".cs_sidebar_widget_content")
        .slideToggle()
        .parent(".cs_sidebar_widget")
        .toggleClass("active");
    });
    $(".cs_dashboard_nav li").on("click", function () {
      $(this).addClass("active").removeClass("active");
    });
  }
  /*=====================================================================
    15.Date And Time Picker
  =======================================================================*/
  function dateTimePicker() {
    flatpickr("#timePicker", {
      enableTime: true,
      allowInput: true,
      noCalendar: true,
      dateFormat: "G:i: K", // Only time in 24-hour format
    });
    flatpickr("#datePicker", {
      enableTime: false,
      allowInput: true,
      dateFormat: "d-F-Y", // 12-hour with AM/PM
    });
  }
  /*=====================================================================
    16.Apartment Finding Function
  =======================================================================*/
  function apartmentShow() {
    const apartmentShowBtn = $(".cs_apartment_btn");
    apartmentShowBtn.on("click", function () {
      $(this)
        .parent(".cs_apartment_item")
        .addClass("active")
        .siblings(".cs_apartment_item")
        .removeClass("active");
    });
  }
  /*===================================================================
    17. Pricing value Toggle
   ===================================================================*/
  function pricingToggle() {
    let currentAttrValue = "monthly";
    $(".cs_pricing_control a").on("click", function (e) {
      $(this).parents("li").addClass("active").siblings().removeClass("active");
      e.preventDefault();
      currentAttrValue = $(this).attr("href");
      if (currentAttrValue !== "yearly") {
        $(".yearlyPrice,.yearlyText").hide();
        $(".monthlyPrice,.monthlyText").show();
      } else {
        $(".yearlyPrice,.yearlyText").show();
        $(".monthlyPrice,.monthlyText").hide();
      }
    });
  }
  /*=================================================================
   18. Light Gallery
 ====================================================================*/
  function lightGallery() {
    $(".cs_gallery_list").each(function () {
      $(this).lightGallery({
        selector: ".cs_gallery_item",
        subHtmlSelectorRelative: false,
        thumbnail: false,
        mousewheel: true,
      });
    });
  }
  /*=================================================================
   19. Load More Portfolio Items
  ===================================================================*/
  function loadMore() {
    $(".cs_property_item").slice(0, 6).show();
    $("#loadMoreProperty").on("click", function (e) {
      e.preventDefault();
      $(".cs_property_item:hidden").slice(0, 3).slideDown(250);
      if ($(".cs_property_item:hidden").length <= 1) {
        $("#loadMoreProperty span")
          .text("No More to show")
          .css("cursor", "not-allowed");
      }
    });
  }
  /*=================================================================
   20. Data Table
  ===================================================================*/
  function dataTable() {
    $("#clientsListTable").DataTable({
      responsive: true,
    });
  }
  /*==================================================================
    21. Scroll Up
  ====================================================================*/
  function scrollUp() {
    $(".cs_scrollup_btn").on("click", function (e) {
      e.preventDefault();
      $("html,body").animate(
        {
          scrollTop: 0,
        },
        0
      );
    });
  }
  /* For Scroll Up */
  function showScrollUp() {
    let scroll = $(window).scrollTop();
    if (scroll >= 350) {
      $(".cs_scrollup_btn").addClass("show");
    } else {
      $(".cs_scrollup_btn").removeClass("show");
    }
  }
  /*=====================================================================
    22. Dynamic contact form
  =======================================================================*/
  if ($.exists("#cs_form")) {
    const form = document.getElementById("cs_form");
    const result = document.getElementById("cs_result");

    form.addEventListener("submit", function (e) {
      const formData = new FormData(form);
      e.preventDefault();
      var object = {};
      formData.forEach((value, key) => {
        object[key] = value;
      });
      var json = JSON.stringify(object);
      // XARU HOME: form backend not connected yet (placeholder, no third-party keys)
      result.innerHTML = "Thank you — our team will contact you shortly.";
      form.reset();
      setTimeout(() => {
        result.style.display = "none";
      }, 5000);
    });
  }
  /*============================================================
    23. AOS Animation
  ==============================================================*/
  function aosInit() {
    AOS.init({
      offset: 100,
      duration: 1000,
      easing: "ease",
      once: true,
      mirror: false,
    });
  }
})(jQuery); // End of use strict
