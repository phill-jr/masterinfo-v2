/**
 * PlayHub — renderiza:
 *  1. Vitrine de logos no card de cada plano (substitui o "App Master X")
 *  2. Seção PlayHub na home (4 cards de categoria + modal "todos os apps")
 *
 * Tudo data-driven do config.json (chaves: planos[].categorias, playhub[])
 * Renderiza DEPOIS que o site-loader.js já injetou os dados.
 */
(function () {
  'use strict';

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function initial(str) {
    var t = (str || '').trim();
    return (t.charAt(0) || '?').toUpperCase();
  }

  // Mini-vitrine no card (até 4 logos + "+X" + categoria + link)
  function renderVitrine(plano, catsById) {
    var cats = plano.categorias || [];
    if (!cats.length) {
      return '<div class="plan-apps-vitrine vitrine-empty">Sem app de TV nesse plano</div>';
    }

    // Pega TODOS os apps das categorias do plano (deduplicado por nome)
    var seen = {};
    var apps = [];
    cats.forEach(function (catId) {
      var cat = catsById[catId];
      if (!cat) return;
      (cat.apps || []).forEach(function (a) {
        if (!seen[a.nome]) {
          seen[a.nome] = true;
          apps.push(a);
        }
      });
    });

    // Cor da primeira categoria (visual coerente)
    var firstCat = catsById[cats[0]] || {};
    var corCat = firstCat.cor || '#6b7280';
    var catLabel = cats.map(function (c) {
      return (catsById[c] && catsById[c].nome) || c;
    }).join(' + ');

    var totalApps = apps.length;
    var visible = apps.slice(0, 4);
    var rest = totalApps - visible.length;

    var logosHtml = visible.map(function (a) {
      if (a.logo) {
        return '<img class="vitrine-logo" src="' + escapeHtml(a.logo) + '" alt="' + escapeHtml(a.nome) + '" loading="lazy" onerror="this.outerHTML=\'<span class=&quot;vitrine-fallback&quot;>' + escapeHtml(initial(a.nome)) + '</span>\'">';
      }
      return '<span class="vitrine-fallback">' + escapeHtml(initial(a.nome)) + '</span>';
    }).join('');

    var moreHtml = rest > 0 ? '<span class="vitrine-more">+' + rest + '</span>' : '';

    return (
      '<div class="plan-apps-vitrine" style="--cat-color:' + corCat + '">' +
      '<span class="vitrine-cat"><span class="vitrine-cat-dot"></span>' + escapeHtml(catLabel) + '</span>' +
      '<div class="vitrine-logos">' + logosHtml + moreHtml + '</div>' +
      '<a href="#playhub" class="vitrine-link">Ver os ' + totalApps + ' apps disponíveis <i class="ph ph-arrow-down"></i></a>' +
      '</div>'
    );
  }

  // Card preto/branco: hero (logo em moldura branca + preço destaque) + body (tag, headline, desc, CTA)
  function renderPlayHubCard(cat) {
    var apps = cat.apps || [];
    // Pega o primeiro app COM logo pra ser o "destaque" do hero
    var destaque = null;
    for (var i = 0; i < apps.length; i++) {
      if (apps[i].logo) { destaque = apps[i]; break; }
    }

    var logoInner = destaque
      ? '<img class="ph-card-hero-logo" src="' + escapeHtml(destaque.logo) + '" alt="' + escapeHtml(destaque.nome) + '" loading="lazy" onerror="this.outerHTML=\'<span class=&quot;ph-card-hero-fallback&quot;>' + escapeHtml((cat.nome || '?').charAt(0)) + '</span>\'">'
      : '<span class="ph-card-hero-fallback">' + escapeHtml((cat.nome || '?').charAt(0)) + '</span>';

    var precoFmt = Number(cat.preco || 0).toFixed(2).replace('.', ',');

    return (
      '<div class="playhub-card" data-cat="' + escapeHtml(cat.id) + '">' +
        '<div class="ph-card-hero">' +
          '<div class="ph-card-hero-frame">' + logoInner + '</div>' +
          '<div class="ph-card-hero-preco">' +
            '<strong>R$ ' + precoFmt + '</strong>' +
            '<small>por mês avulso</small>' +
          '</div>' +
        '</div>' +
        '<div class="ph-card-body">' +
          '<span class="ph-card-tag">' + escapeHtml(cat.nome) + '</span>' +
          '<h3 class="ph-card-headline">' + escapeHtml(cat.descricao || '') + '</h3>' +
          '<p class="ph-card-desc">' + apps.length + ' apps na categoria · escolha 1 por mês</p>' +
          '<span class="ph-card-cta">Ver todos os ' + apps.length + ' apps <i class="ph ph-arrow-right"></i></span>' +
        '</div>' +
      '</div>'
    );
  }

  // Modal: TODOS os apps + planos que dão acesso
  function renderModal(cat, planosByCat) {
    var planos = planosByCat[cat.id] || [];
    var apps = cat.apps || [];

    var appsHtml = apps.map(function (a) {
      var inner = a.logo
        ? '<img src="' + escapeHtml(a.logo) + '" alt="' + escapeHtml(a.nome) + '" loading="lazy" onerror="this.outerHTML=\'<span class=&quot;playhub-app-fallback&quot;>' + escapeHtml(initial(a.nome)) + '</span>\'">'
        : '<span class="playhub-app-fallback">' + escapeHtml(initial(a.nome)) + '</span>';
      return (
        '<div class="playhub-modal-app">' +
        inner +
        '<span class="nome">' + escapeHtml(a.nome) + '</span>' +
        '</div>'
      );
    }).join('');

    var planosHtml = planos.length
      ? '<div class="playhub-modal-planos">' +
        '<h4>Planos que incluem ' + escapeHtml(cat.nome) + '</h4>' +
        '<ul>' +
        planos.map(function (p) {
          return '<li>✓ <a href="#planos">' + escapeHtml(p.nome) + '</a> — ' + p.velocidade + ' ' + p.unidade + ' por R$ ' + Number(p.precoPontual).toFixed(2).replace('.', ',') + '/mês</li>';
        }).join('') +
        '</ul></div>'
      : '<p style="color:#888;font-size:0.9rem">Esta categoria é vendida apenas como add-on avulso.</p>';

    return (
      '<div class="playhub-modal-card" style="--cat-color:' + (cat.cor || '#6b7280') + '">' +
      '<button class="playhub-modal-close" aria-label="Fechar" data-close>×</button>' +
      '<div class="playhub-modal-head">' +
      '<h3 class="playhub-modal-title">' + escapeHtml(cat.nome) + '</h3>' +
      '<p class="playhub-modal-sub">' + escapeHtml(cat.descricao || '') + ' · 1 app por mês · R$ ' + Number(cat.preco || 0).toFixed(2).replace('.', ',') + ' avulso</p>' +
      '</div>' +
      '<div class="playhub-modal-grid">' + appsHtml + '</div>' +
      planosHtml +
      '</div>'
    );
  }

  function openModal(catId, playhub, planosByCat) {
    var cat = playhub.filter(function (c) { return c.id === catId; })[0];
    if (!cat) return;

    var overlay = document.getElementById('playhubModal');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.id = 'playhubModal';
      overlay.className = 'playhub-modal';
      overlay.addEventListener('click', function (e) {
        if (e.target === overlay || e.target.matches('[data-close], [data-close] *')) closeModal();
      });
      document.body.appendChild(overlay);
    }
    overlay.innerHTML = renderModal(cat, planosByCat);
    requestAnimationFrame(function () { overlay.classList.add('is-open'); });
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    var overlay = document.getElementById('playhubModal');
    if (overlay) overlay.classList.remove('is-open');
    document.body.style.overflow = '';
  }

  // ─── Bootstrap ───
  function start(cfg) {
    var playhub = (cfg && cfg.playhub) || [];
    var planos = (cfg && cfg.planos) || [];
    if (!playhub.length) return;

    // Mapas auxiliares
    var catsById = {};
    playhub.forEach(function (c) { catsById[c.id] = c; });
    var planosByCat = {};
    planos.forEach(function (p) {
      (p.categorias || []).forEach(function (catId) {
        (planosByCat[catId] = planosByCat[catId] || []).push(p);
      });
    });

    // 1) Substitui o div .plan-apps original em cada card
    document.querySelectorAll('.plan-card').forEach(function (card) {
      var ctaLink = card.querySelector('a.btn-plan[data-plano]');
      var planoId = ctaLink && ctaLink.dataset.plano;
      if (!planoId) return;
      var plano = planos.filter(function (p) { return p.id === planoId; })[0];
      if (!plano) return;

      var apps = card.querySelector('.plan-apps');
      if (!apps) return;

      // Substitui a "vitrine" antiga (lista de app único) pela nova
      var list = apps.querySelector('.plan-apps-list');
      if (list) {
        var temp = document.createElement('div');
        temp.innerHTML = renderVitrine(plano, catsById);
        list.replaceWith(temp.firstChild);
      }
    });

    // 2) Renderiza seção PlayHub
    var sec = document.getElementById('playhub-grid');
    if (sec) {
      sec.innerHTML = playhub.map(function (c) { return renderPlayHubCard(c, planosByCat); }).join('');
      sec.addEventListener('click', function (e) {
        var card = e.target.closest('.playhub-card');
        if (card) openModal(card.dataset.cat, playhub, planosByCat);
      });
    }

    // ESC fecha modal
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeModal();
    });
  }

  // Descobre o caminho até a raiz a partir da própria <script> tag.
  // Funciona em qualquer profundidade: /, /tv-streaming/, /aplicativos/deezer/, etc.
  function configUrl() {
    try {
      var scripts = document.getElementsByTagName('script');
      for (var i = scripts.length - 1; i >= 0; i--) {
        var s = scripts[i].getAttribute('src') || '';
        var idx = s.indexOf('playhub.js');
        if (idx >= 0) {
          return s.slice(0, idx) + 'config.json?v=' + Date.now();
        }
      }
    } catch (_) {}
    return 'config.json?v=' + Date.now();
  }

  // Quando o config carrega via site-loader
  function getConfig(cb) {
    if (window.__masterConfig) { cb(window.__masterConfig); return; }
    fetch(configUrl())
      .then(function (r) { return r.json(); })
      .then(function (c) { window.__masterConfig = c; cb(c); })
      .catch(function () { });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { getConfig(start); });
  } else {
    getConfig(start);
  }
})();
