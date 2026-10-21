/* Scroll reveal dengan IntersectionObserver (bukan listener scroll). Bertahap per induk agar terasa bergelombang. */
(function () {
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0.06, rootMargin: '0px 0px -5% 0px' });
  var seen = new WeakMap();
  document.querySelectorAll('.hv main .card, .hv main h2, .hv main .callout, .hv main .step, .hv main details').forEach(function (el) {
    if (el.closest('.card') && el.closest('.card') !== el) return; // elemen di dalam kartu ikut kartunya
    var p = el.parentNode, n = seen.get(p) || 0; seen.set(p, n + 1);
    el.classList.add('rv'); el.style.transitionDelay = Math.min(n, 5) * 70 + 'ms'; io.observe(el);
  });
})();
