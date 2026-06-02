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
      run('planos', function () { loadPlanos(cfg.planos); });
      run('bairros', function () { loadBairros(cfg.bairros); });
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
    var ld = document.querySelector('script[type="application/ld+json"]');
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
})();
