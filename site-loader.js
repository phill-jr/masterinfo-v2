/**
 * MasterInfo v2 - Site Loader
 * Carrega config.json e injeta o conteudo dinamico na home (index.html).
 *
 * IMPORTANTE: atualiza os elementos EM-LUGAR (textContent / href / meta),
 * sem regenerar grids inteiros, para NAO quebrar os scripts inline da pagina
 * (carrossel do hero, copa popup, promo bar, mapa Leaflet, mega-menu).
 * Cada secao e adicionada aqui conforme recebe ganchos (ids) no index.html.
 */
(function () {
  'use strict';

  fetch('config.json?v=' + Date.now())
    .then(function (r) { return r.json(); })
    .then(function (cfg) {
      // Expor config para outros scripts (checkout, modal, tracking)
      window._siteConfig = cfg;

      run('seo', function () { loadSeo(cfg.seo, cfg.empresa, cfg.planos); });
      run('footer', function () { loadFooter(cfg.empresa); });
      run('faq', function () { loadFaq(cfg.faq); });
      run('faqSchema', function () { loadFaqSchema(cfg.faq); });
      run('planos', function () { loadPlanos(cfg.planos); });
      run('bairros', function () { loadBairros(cfg.bairros); });
      run('footerMenus', function () { loadFooterMenus(cfg.menus && cfg.menus.footer); });
      run('secoesOrdem', function () { loadSecoesOrdem(cfg.secoesOrdem); });
      run('menuHeader', function () { loadMenuHeader(cfg.menuHeader); });
    })
    .catch(function (e) {
      console.warn('[SiteLoader] config.json nao carregado, usando HTML estatico:', e);
    });

  // Executa cada secao isolada — um erro numa secao nao derruba as outras
  function run(nome, fn) {
    try { fn(); } catch (e) { console.warn('[SiteLoader] falha na secao "' + nome + '":', e); }
  }

  // ─── SEO + Schema.org (metas por atributo + JSON-LD regenerado) ───
  function loadSeo(seo, emp, planos) {
    if (!seo) return;
    emp = emp || {};

    if (seo.title) document.title = seo.title;
    setMeta('meta[name="description"]', seo.description);
    setMeta('meta[property="og:title"]', seo.ogTitle);
    setMeta('meta[property="og:description"]', seo.ogDescription);
    setMeta('meta[property="og:url"]', seo.ogUrl);
    setMeta('meta[property="og:image"]', seo.ogImage);
    setMeta('meta[property="og:site_name"]', seo.ogSiteName);
    setMeta('meta[name="twitter:title"]', seo.twitterTitle);
    setMeta('meta[name="twitter:description"]', seo.twitterDescription);

    // Regenera o JSON-LD a partir de empresa + planos + seo (evita dados chumbados)
    var ld = document.getElementById('schema-org') || document.querySelector('script[type="application/ld+json"]');
    if (ld) {
      try {
        ld.textContent = JSON.stringify(buildSchema(seo, emp, planos || []), null, 2);
      } catch (e) {
        console.warn('[SiteLoader] falha ao gerar JSON-LD:', e);
      }
    }
  }

  function buildSchema(seo, emp, planos) {
    var url = seo.ogUrl || 'https://masterinfointernet.com';
    var cidadeParts = (emp.cidade || '').split(',');
    var locality = (cidadeParts[0] || '').trim();
    var region = (cidadeParts[1] || '').trim();

    var schema = {
      '@context': 'https://schema.org',
      '@type': 'InternetServiceProvider',
      'name': seo.ogSiteName || 'MasterInfo Internet',
      'description': seo.schemaDescription || seo.description || '',
      'url': url,
      'telephone': emp.telefone ? '+55' + emp.telefone.replace(/\D/g, '') : '',
      'email': emp.email || '',
      'address': {
        '@type': 'PostalAddress',
        'streetAddress': emp.endereco || '',
        'addressLocality': locality,
        'addressRegion': region,
        'postalCode': emp.cep || '',
        'addressCountry': 'BR'
      },
      'areaServed': { '@type': 'City', 'name': locality },
      'priceRange': seo.priceRange || '',
      'sameAs': [emp.instagram, emp.facebook].filter(Boolean)
    };

    if (seo.ratingValue) {
      schema.aggregateRating = {
        '@type': 'AggregateRating',
        'ratingValue': String(seo.ratingValue),
        'bestRating': '5',
        'ratingCount': String(seo.ratingCount || '')
      };
    }

    if (planos && planos.length) {
      schema.hasOfferCatalog = {
        '@type': 'OfferCatalog',
        'name': 'Planos de Internet Fibra',
        'itemListElement': planos.map(function (p) {
          var preco = (p.precoPontual != null ? p.precoPontual : p.preco);
          return {
            '@type': 'Offer',
            'name': p.nome + ' ' + p.velocidade + ' ' + p.unidade,
            'price': Number(preco || 0).toFixed(2),
            'priceCurrency': 'BRL',
            'url': url + '/checkout.html?plano=' + p.id
          };
        })
      };
    }
    return schema;
  }

  // ─── Rodape (descricao, redes sociais, e-mail, CNPJ, logo) ───
  function loadFooter(emp) {
    if (!emp) return;
    setText('#footerDesc', 'Internet fibra optica de verdade em ' + (emp.cidade || 'Joinville') + '. Mais de 6 anos conectando familias e empresas.');
    setHref('#footerInstagram', emp.instagram);
    setHref('#footerFacebook', emp.facebook);
    if (emp.whatsapp) setHref('#footerWhatsapp', 'https://wa.me/' + emp.whatsapp);
    if (emp.email) setHref('#footerEmail', 'mailto:' + emp.email);
    if (emp.cnpj) setText('#footerCnpj', '© 2026 MasterInfo Internet. Todos os direitos reservados. CNPJ: ' + emp.cnpj);
    if (emp.logo) {
      document.querySelectorAll('.logo img').forEach(function (img) { img.src = emp.logo; });
    }
  }

  // ─── FAQ (atualiza em-lugar; se a contagem mudar, regenera + religa o accordion) ───
  function loadFaq(faqs) {
    if (!faqs || !faqs.length) return;
    var list = document.querySelector('.faq .faq-list');
    if (!list) return;
    var items = list.querySelectorAll('.faq-item');

    if (items.length === faqs.length) {
      faqs.forEach(function (f, i) {
        var q = items[i].querySelector('.faq-question span');
        var a = items[i].querySelector('.faq-answer p');
        if (q && f.pergunta != null) q.textContent = f.pergunta;
        if (a && f.resposta != null) a.innerHTML = f.resposta;
      });
      return;
    }

    list.innerHTML = faqs.map(function (f) {
      return '<div class="faq-item">' +
        '<button class="faq-question"><span>' + esc(f.pergunta) + '</span><i class="ph ph-caret-down"></i></button>' +
        '<div class="faq-answer"><p>' + (f.resposta || '') + '</p></div>' +
        '</div>';
    }).join('');
    bindFaqAccordion(list);
  }

  function bindFaqAccordion(list) {
    var items = list.querySelectorAll('.faq-item');
    items.forEach(function (item) {
      var btn = item.querySelector('.faq-question');
      if (!btn) return;
      btn.addEventListener('click', function () {
        var active = item.classList.contains('active');
        items.forEach(function (el) { el.classList.remove('active'); });
        if (!active) item.classList.add('active');
      });
    });
  }

  // ─── FAQ Schema (JSON-LD FAQPage sincronizado com o config, p/ SEO + GEO) ───
  function loadFaqSchema(faqs) {
    var faqLd = document.getElementById('schema-faq');
    if (!faqLd || !faqs || !faqs.length) return;
    faqLd.textContent = JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'FAQPage',
      'mainEntity': faqs.map(function (f) {
        return {
          '@type': 'Question',
          'name': stripTags(f.pergunta),
          'acceptedAnswer': { '@type': 'Answer', 'text': stripTags(f.resposta) }
        };
      })
    }, null, 2);
  }

  // ─── Planos: sincroniza os PRECOS dos cards da home a partir do config ───
  // (layout, apps inclusos e features sao bespoke do redesign — nao mexemos)
  function loadPlanos(planos) {
    if (!planos || !planos.length) return;
    // alias do link de checkout -> id nominal do config (mesmo mapa do checkout.js)
    var ALIAS = { '600': 'lite-casa', '800': 'lite-familia', '1000': 'lite-home-office', 'ultra-800': 'ultra-familia', 'ultra-1000': 'ultra-home-office' };
    var byId = {};
    planos.forEach(function (p) { byId[p.id] = p; });

    document.querySelectorAll('.plans .plan-card').forEach(function (card) {
      var link = card.querySelector('a.btn-plan[href*="checkout.html?plano="]');
      if (!link) return;
      var m = link.getAttribute('href').match(/plano=([^&]+)/);
      if (!m) return;
      var id = ALIAS[m[1]] || m[1];
      var p = byId[id];
      if (!p) return;

      var pontual = (p.precoPontual != null ? p.precoPontual : p.preco);
      if (pontual != null) {
        var intPart = Math.floor(pontual);
        var cents = Math.round((pontual - intPart) * 100);
        var valEl = card.querySelector('.plan-value');
        var centsEl = card.querySelector('.plan-cents');
        if (valEl) valEl.textContent = String(intPart);
        if (centsEl) centsEl.textContent = ',' + ('0' + cents).slice(-2);
      }
      if (p.precoCheio != null) {
        var origEl = card.querySelector('.plan-price-original');
        if (origEl) origEl.innerHTML = 'de <s>R$ ' + formatBRL(p.precoCheio) + '</s> por apenas';
      }
    });
  }

  function formatBRL(n) {
    return Number(n).toFixed(2).replace('.', ',');
  }

  // ─── Bairros (atualiza os nomes das tags em-lugar; preserva handlers do mapa inline) ───
  // Coords dos pins continuam no script do mapa (bespoke). So sincroniza nome/dataBairro
  // quando a contagem bate, pra nao quebrar o clique tag->zoom do Leaflet.
  function loadBairros(bairros) {
    if (!bairros || !bairros.length) return;
    window._cfgBairros = bairros; // exposto pro script do mapa (uso futuro)
    var tags = document.querySelectorAll('#cobertura .neighborhood-tag[data-bairro]');
    if (tags.length === bairros.length) {
      bairros.forEach(function (b, i) {
        if (b.nome != null) tags[i].textContent = b.nome;
        if (b.dataBairro != null) tags[i].setAttribute('data-bairro', b.dataBairro);
      });
    }
  }

  // ─── Menu do topo / header (reordena, oculta, edita e regenera os dropdowns) ───
  function loadMenuHeader(mh) {
    if (!mh || !mh.itens || !mh.itens.length) return;
    var nav = document.getElementById('nav'); if (!nav) return;
    var sales = nav.querySelector('.nav-list-sales');
    var client = nav.querySelector('.nav-list-client');
    if (!sales || !client) return;

    function findByHref(h) { var a = nav.querySelector('.nav-list a.nav-link[href="' + h + '"]'); return a ? a.closest('.nav-item') : null; }
    function findDrop(txt) {
      var lis = nav.querySelectorAll('.nav-item.has-mega');
      for (var i = 0; i < lis.length; i++) {
        var t = lis[i].querySelector('.nav-trigger');
        if (t && t.textContent.replace(/\s+/g, ' ').trim().indexOf(txt) === 0) return lis[i];
      }
      return null;
    }
    var FIND = {
      internet: function () { return findDrop('Internet'); },
      tv: function () { return findByHref('/tv-streaming'); },
      cobertura: function () { return findByHref('#cobertura'); },
      historia: function () { return findByHref('#nossa-historia'); },
      contato: function () { return findByHref('#contato'); },
      aplicativos: function () { return findDrop('Aplicativos'); },
      ajuda: function () { return findDrop('Ajuda'); }
    };

    mh.itens.forEach(function (it) {
      var find = FIND[it.key]; if (!find) return;
      var li = find(); if (!li) return;
      li.style.display = (it.on === false) ? 'none' : '';
      if (it.tipo === 'link') {
        var a = li.querySelector('a.nav-link');
        if (a) {
          if (it.label != null) a.textContent = it.label;
          if (it.href) a.setAttribute('href', it.href);
          if (it.target) a.setAttribute('target', it.target);
        }
      } else {
        var trig = li.querySelector('.nav-trigger');
        if (trig && it.label != null) trig.innerHTML = esc(it.label) + ' <i class="ph ph-caret-down nav-trigger-caret"></i>';
        var dl = li.querySelector('.dropdown-list');
        if (dl && it.children) {
          dl.innerHTML = it.children.map(function (c) {
            var logo = c.logo ? '<img class="dropdown-logo dropdown-logo-real" src="' + esc(c.logo) + '" alt="' + esc(c.label) + '" loading="lazy">' : '';
            var tgt = c.target ? ' target="' + esc(c.target) + '"' : '';
            return '<li><a href="' + esc(c.href) + '"' + tgt + ' class="dropdown-link">' + logo + esc(c.label) + '</a></li>';
          }).join('');
        }
      }
      var ul = (it.lado === 'dir') ? client : sales;
      ul.appendChild(li);
    });

    if (mh.clientButton) {
      var btn = nav.querySelector('.header-client-btn');
      if (btn) {
        if (mh.clientButton.href) btn.setAttribute('href', mh.clientButton.href);
        var sp = btn.querySelector('span');
        if (sp && mh.clientButton.label != null) sp.textContent = mh.clientButton.label;
      }
    }

    rebindMega();
  }

  // Re-liga o mega-menu (hover desktop + click) apos o nav ser reorganizado.
  // Guard _megaBound evita listeners duplicados.
  var _megaDocBound = false;
  function rebindMega() {
    var navItems = document.querySelectorAll('#nav .nav-item.has-mega');
    var backdrop = document.getElementById('megaBackdrop');
    function closeAll() {
      navItems.forEach(function (it) { it.classList.remove('is-open'); });
      if (backdrop) backdrop.classList.remove('is-visible');
    }
    navItems.forEach(function (item) {
      if (item._megaBound) return;
      item._megaBound = true;
      var trigger = item.querySelector('.nav-trigger');
      var hoverTimer;
      item.addEventListener('mouseenter', function () {
        if (window.innerWidth < 1024) return;
        clearTimeout(hoverTimer);
        navItems.forEach(function (it) { if (it !== item) it.classList.remove('is-open'); });
        item.classList.add('is-open');
        if (backdrop) backdrop.classList.add('is-visible');
      });
      item.addEventListener('mouseleave', function () {
        if (window.innerWidth < 1024) return;
        hoverTimer = setTimeout(function () {
          item.classList.remove('is-open');
          if (backdrop) backdrop.classList.remove('is-visible');
        }, 120);
      });
      if (trigger) {
        trigger.addEventListener('click', function (e) {
          e.preventDefault();
          var wasOpen = item.classList.contains('is-open');
          closeAll();
          if (!wasOpen) {
            item.classList.add('is-open');
            if (backdrop && window.innerWidth >= 1024) backdrop.classList.add('is-visible');
          }
        });
      }
    });
    if (!_megaDocBound) {
      _megaDocBound = true;
      document.addEventListener('click', function (e) {
        if (!e.target.closest('.nav-item.has-mega') && !e.target.closest('.mega-menu')) closeAll();
      });
    }
  }

  // ─── Ordem & visibilidade das secoes da home (move os blocos <section>) ───
  function loadSecoesOrdem(arr) {
    if (!arr || !arr.length) return;
    var MAP = { hero: '.hero', planos1: '#planos', planos2: '.plans-light', historia: '#nossa-historia', cobertura: '#cobertura', depoimentos: '#depoimentos', cta: '.cta-banner', faq: '#faq' };
    var nodes = [];
    arr.forEach(function (it) {
      var sel = MAP[it.key]; if (!sel) return;
      var el = document.querySelector(sel);
      if (el && el.tagName === 'SECTION') {
        el.style.display = (it.on === false) ? 'none' : '';
        nodes.push(el);
      }
    });
    if (nodes.length < 2) return;
    var parent = nodes[0].parentNode;
    var lastDom = nodes[0];
    nodes.forEach(function (n) {
      if (lastDom.compareDocumentPosition(n) & Node.DOCUMENT_POSITION_FOLLOWING) lastDom = n;
    });
    var anchor = lastDom.nextSibling;
    nodes.forEach(function (n) { parent.insertBefore(n, anchor); });
  }

  // ─── Menus do rodape (regenera as 3 colunas a partir do config) ───
  function loadFooterMenus(cols) {
    if (!cols || !cols.length) return;
    var grid = document.querySelector('.footer .footer-grid');
    if (!grid) return;
    grid.querySelectorAll('.footer-col').forEach(function (c) { c.remove(); });
    var html = cols.map(function (col) {
      var links = (col.links || []).map(function (l) {
        var icon = l.icone ? '<i class="' + esc(l.icone) + '"></i> ' : '';
        var tgt = l.target ? ' target="' + esc(l.target) + '"' : '';
        return '<a href="' + esc(l.href) + '"' + tgt + '>' + icon + esc(l.label) + '</a>';
      }).join('');
      return '<div class="footer-col"><h4>' + esc(col.titulo) + '</h4>' + links + '</div>';
    }).join('');
    grid.insertAdjacentHTML('beforeend', html);
  }

  // ─── Helpers ───
  function setText(sel, val) {
    var el = document.querySelector(sel);
    if (el && val != null && val !== '') el.textContent = val;
  }
  function setHTML(sel, val) {
    var el = document.querySelector(sel);
    if (el && val != null && val !== '') el.innerHTML = val;
  }
  function setHref(sel, val) {
    var el = document.querySelector(sel);
    if (el && val) el.setAttribute('href', val);
  }
  function setMeta(sel, val, attr) {
    var el = document.querySelector(sel);
    if (el && val != null && val !== '') el.setAttribute(attr || 'content', val);
  }
  function esc(str) {
    if (str == null) return '';
    var d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
  }
  function stripTags(html) {
    if (html == null) return '';
    var d = document.createElement('div');
    d.innerHTML = html;
    return (d.textContent || d.innerText || '').replace(/\s+/g, ' ').trim();
  }
})();
