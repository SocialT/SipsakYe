/* Render'dan önce çalışır (defer YOK).
   1. html.js sınıfı: scroll animasyonu yalnızca JS varsa içeriği gizler.
   2. Kayıtlı tema tercihi: sayfa boyanmadan uygulanır, yanıp sönme olmaz. */
(function () {
  var r = document.documentElement;
  r.classList.add("js");
  try {
    var t = localStorage.getItem("sy-theme");
    if (t === "dark" || t === "light") r.setAttribute("data-theme", t);
  } catch (e) {}
})();
