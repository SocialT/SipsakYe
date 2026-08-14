/* Şipşak Ye — tanıtım sitesi. Bağımlılık yok, ~2KB. */
(function () {
  "use strict";

  /* --- Tema değiştirme (kayıtlı tercih head.js'te uygulanır) --- */
  var root = document.documentElement;

  document.addEventListener("click", function (ev) {
    var toggle = ev.target.closest(".theme-toggle");
    if (!toggle) return;
    var current = root.getAttribute("data-theme");
    if (!current) {
      current = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    }
    var next = current === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("sy-theme", next); } catch (e) {}
  });

  /* --- Mobil menü --- */
  var navToggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".nav");
  if (navToggle && nav) {
    navToggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(open));
    });
    nav.addEventListener("click", function (ev) {
      if (ev.target.closest("a")) {
        nav.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* --- Sözleşmeler/Legal açılır menüsü: dışarı tıklayınca veya Esc ile kapat.
     Menünün kendisi <details>/<summary> ile çalışır, bu sadece ek incelik. --- */
  document.addEventListener("click", function (ev) {
    document.querySelectorAll(".nav-dropdown[open]").forEach(function (dd) {
      if (!dd.contains(ev.target)) dd.removeAttribute("open");
    });
  });
  document.addEventListener("keydown", function (ev) {
    if (ev.key !== "Escape") return;
    document.querySelectorAll(".nav-dropdown[open]").forEach(function (dd) {
      dd.removeAttribute("open");
    });
  });

  /* --- Header gölgesi --- */
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-stuck", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* --- Görünüme girince yumuşak geçiş --- */
  var revealables = document.querySelectorAll(".reveal");
  if (revealables.length) {
    var revealAll = function () {
      revealables.forEach(function (el) { el.classList.add("is-in"); });
    };

    if (!("IntersectionObserver" in window)) {
      revealAll();
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            io.unobserve(entry.target);
          }
        });
      }, { rootMargin: "0px 0px -5% 0px", threshold: 0 });
      revealables.forEach(function (el) { io.observe(el); });

      // Güvenlik ağı: hızlı kaydırma, çapa bağlantısıyla atlama veya
      // sayfa içinde arama gibi durumlarda gözlemci tetiklenmeyebilir.
      // Hiçbir bölüm görünmez kalmasın — boş sayfa mağaza reddi demek.
      setTimeout(revealAll, 2500);
    }
  }

  /* --- Yıl --- */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
