/* legal.js — comportamento compartilhado das páginas legais
   (nav mega-menu + mobile, sumário com scroll-spy, sumário recolhível no mobile) */
(function () {
  'use strict';

  // ── Mega-menu + mobile (mesmo comportamento das subpáginas) ──
  var navItems = document.querySelectorAll('.nav-item.has-mega');
  navItems.forEach(function (item) {
    var trigger = item.querySelector('.nav-trigger');
    if (!trigger) return;
    trigger.addEventListener('click', function (e) {
      e.preventDefault();
      var wasOpen = item.classList.contains('is-open');
      navItems.forEach(function (it) { it.classList.remove('is-open'); });
      if (!wasOpen) item.classList.add('is-open');
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.nav-item.has-mega') && !e.target.closest('.mega-menu')) {
      navItems.forEach(function (it) { it.classList.remove('is-open'); });
    }
  });
  var mt = document.getElementById('mobileToggle');
  var nv = document.getElementById('nav');
  if (mt && nv) mt.addEventListener('click', function () {
    mt.classList.toggle('active'); nv.classList.toggle('open');
  });

  // ── Sumário recolhível no mobile ──
  var toc = document.querySelector('.lg-toc');
  var tocTitle = toc && toc.querySelector('.lg-toc-title');
  if (toc && tocTitle) {
    toc.classList.add('lg-toc-collapsible');
    tocTitle.addEventListener('click', function () {
      // só alterna quando o título está clicável (mobile, via CSS)
      if (window.matchMedia('(max-width: 900px)').matches) {
        toc.classList.toggle('is-open');
      }
    });
  }

  // ── Smooth scroll nos links do sumário (fecha o sumário mobile ao clicar) ──
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll('.lg-toc a[href^="#"]'));
  tocLinks.forEach(function (link) {
    link.addEventListener('click', function (e) {
      var id = link.getAttribute('href').slice(1);
      var target = document.getElementById(id);
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      history.replaceState(null, '', '#' + id);
      if (toc && window.matchMedia('(max-width: 900px)').matches) toc.classList.remove('is-open');
    });
  });

  // ── Scroll-spy: destaca a seção visível no sumário ──
  var sections = Array.prototype.slice.call(document.querySelectorAll('.lg-content section[id]'));
  if (sections.length && tocLinks.length && 'IntersectionObserver' in window) {
    var byId = {};
    tocLinks.forEach(function (l) { byId[l.getAttribute('href').slice(1)] = l; });
    var visible = {};
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { visible[en.target.id] = en.isIntersecting ? en.intersectionRatio : 0; });
      var bestId = null, bestRatio = 0;
      sections.forEach(function (s) {
        var r = visible[s.id] || 0;
        if (r > bestRatio) { bestRatio = r; bestId = s.id; }
      });
      if (bestId && byId[bestId]) {
        tocLinks.forEach(function (l) { l.classList.remove('is-active'); });
        byId[bestId].classList.add('is-active');
      }
    }, { rootMargin: '-88px 0px -55% 0px', threshold: [0, 0.25, 0.5, 1] });
    sections.forEach(function (s) { spy.observe(s); });
  }
})();
