/**
 * MasterInfo - Site Loader
 * Carrega config.json e injeta conteudo dinamico no site.
 * Todas as secoes do site sao renderizadas a partir dos dados do admin.
 */
(function () {
  'use strict';

  fetch('config.json?v=' + Date.now())
    .then(function (r) { return r.json(); })
    .then(function (cfg) {
      // Expor config globalmente para outros scripts (checkout, modal)
      window._siteConfig = cfg;

      loadEmpresa(cfg.empresa);
      loadHero(cfg.hero);
      loadPlanos(cfg.planos);
      loadStats(cfg.stats);
      loadDiferenciais(cfg.diferenciais);
      loadBairros(cfg.bairros);
      loadDepoimentos(cfg.depoimentos);
      loadFaq(cfg.faq);
      loadFooter(cfg.empresa);
    })
    .catch(function (e) {
      console.warn('[SiteLoader] config.json nao carregado, usando HTML estatico:', e);
    });

  // ─── Empresa (topbar, whatsapp links, telefone) ───
  function loadEmpresa(emp) {
    if (!emp) return;

    // Telefone no topbar
    setText('#topbarPhone', emp.telefone);
    setHref('#topbarPhoneLink', 'tel:' + emp.telefone.replace(/\D/g, ''));

    // Cidade no topbar
    if (emp.cidade) {
      setHTML('#topbarCity', '<i class="ph ph-map-pin"></i> ' + emp.cidade);
    }

    // Todos os links WhatsApp
    var waLinks = document.querySelectorAll('a[href*="wa.me"]');
    waLinks.forEach(function (a) {
      var baseUrl = 'https://wa.me/' + emp.whatsapp;
      var text = a.href.split('?text=')[1] || '';
      a.href = baseUrl + (text ? '?text=' + text : '');
    });

    // Telefone nos CTAs (pula o topbar que ja foi tratado acima)
    var telLinks = document.querySelectorAll('a[href^="tel:"]:not(#topbarPhoneLink)');
    telLinks.forEach(function (a) {
      a.href = 'tel:' + emp.telefone.replace(/\D/g, '');
      // Atualizar texto visivel se contem icone + texto
      if (a.querySelector('i') && a.childNodes.length > 1) {
        var iconHTML = a.querySelector('i').outerHTML;
        a.innerHTML = iconHTML + ' ' + emp.telefone;
      }
    });
  }

  // ─── Hero ───
  function loadHero(hero) {
    if (!hero) return;
    setHTML('#heroBadge', hero.badge);
    setHTML('#heroTitulo', hero.titulo + '<br><span class="hero-highlight">' + hero.tituloDestaque + '</span><br>' + hero.tituloFim);
    setHTML('#heroSubtitulo', hero.subtitulo);

    var trustContainer = document.getElementById('heroTrust');
    if (trustContainer && hero.confianca) {
      var icons = ['ph-fill ph-clock', 'ph-fill ph-handshake', 'ph-fill ph-star'];
      var html = '';
      hero.confianca.forEach(function (item, i) {
        html += '<div class="hero-trust-item">' +
          '<i class="' + (icons[i] || 'ph-fill ph-check') + '"></i>' +
          '<span>' + item + '</span>' +
          '</div>';
      });
      trustContainer.innerHTML = html;
    }
  }

  // ─── Planos (cards de planos) ───
  function loadPlanos(planos) {
    if (!planos || !planos.length) return;
    var container = document.getElementById('plansGrid');
    if (!container) return;

    var html = '';
    planos.forEach(function (p, i) {
      var isFeatured = !!p.badge;
      var delay = i * 100;

      html += '<div class="plan-card' + (isFeatured ? ' plan-featured' : '') + '" data-aos="fade-up"' +
        (delay ? ' data-aos-delay="' + delay + '"' : '') + '>';

      if (p.badge) {
        html += '<div class="plan-badge">' + esc(p.badge) + '</div>';
      }

      html += '<div class="plan-header">' +
        '<span class="plan-name">' + esc(p.nome) + '</span>' +
        '<div class="plan-speed">' +
          '<span class="plan-speed-num">' + esc(p.velocidade) + '</span>' +
          '<span class="plan-speed-unit">' + esc(p.unidade) + '</span>' +
        '</div>' +
      '</div>' +
      '<div class="plan-body">' +
        '<div class="plan-price">' +
          '<span class="plan-currency">R$</span>' +
          '<span class="plan-value">' + Math.round(p.preco) + '</span>' +
          '<span class="plan-period">/m\u00eas</span>' +
        '</div>' +
        '<ul class="plan-features">';

      if (p.features) {
        p.features.forEach(function (f) {
          html += '<li><i class="ph-fill ph-check-circle"></i> ' + esc(f) + '</li>';
        });
      }

      html += '</ul>' +
        '<a href="checkout.html?plano=' + esc(p.id) + '" class="btn ' + (isFeatured ? 'btn-primary ' : '') + 'btn-plan">' +
          'Contratar <i class="ph ph-arrow-right"></i>' +
        '</a>' +
      '</div></div>';
    });

    container.innerHTML = html;
  }

  // ─── Stats ───
  function loadStats(stats) {
    if (!stats) return;
    var container = document.getElementById('statsGrid');
    if (!container) return;

    var html = '';
    stats.forEach(function (s, i) {
      if (i > 0) html += '<div class="stat-divider"></div>';
      html += '<div class="stat-item">' +
        '<div class="stat-number" data-target="' + s.valor + '"' +
        (s.sufixo ? ' data-suffix="' + s.sufixo + '"' : '') +
        (s.prefixo ? ' data-prefix="' + s.prefixo + '"' : '') +
        (s.decimal ? ' data-decimal="true"' : '') +
        '>0</div>' +
        '<div class="stat-label">' + s.label + '</div>' +
        '</div>';
    });
    container.innerHTML = html;

    // Re-attach stats animation observer
    initStatsAnimation();
  }

  function initStatsAnimation() {
    var statNumbers = document.querySelectorAll('.stat-number[data-target]');
    var animated = false;

    function animateStats() {
      if (animated) return;
      animated = true;
      statNumbers.forEach(function (el) {
        var target = parseFloat(el.getAttribute('data-target'));
        var suffix = el.getAttribute('data-suffix') || '';
        var prefix = el.getAttribute('data-prefix') || '';
        var isDecimal = el.getAttribute('data-decimal') === 'true';
        var duration = 2000;
        var start = performance.now();

        function update(now) {
          var elapsed = now - start;
          var progress = Math.min(elapsed / duration, 1);
          var ease = 1 - Math.pow(1 - progress, 3);
          var value = ease * target;
          if (isDecimal) {
            el.textContent = prefix + value.toFixed(1) + suffix;
          } else {
            el.textContent = prefix + Math.round(value).toLocaleString('pt-BR') + suffix;
          }
          if (progress < 1) requestAnimationFrame(update);
        }
        requestAnimationFrame(update);
      });
    }

    var statsSection = document.querySelector('.stats');
    if (statsSection) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) animateStats();
        });
      }, { threshold: 0.3 });
      observer.observe(statsSection);
    }
  }

  // ─── Diferenciais (Why section) ───
  function loadDiferenciais(difs) {
    if (!difs) return;
    var container = document.getElementById('whyGrid');
    if (!container) return;

    var html = '';
    difs.forEach(function (d) {
      html += '<div class="why-card">' +
        '<div class="why-icon"><i class="' + d.icone + '"></i></div>' +
        '<h3>' + d.titulo + '</h3>' +
        '<p>' + d.descricao + '</p>' +
        '</div>';
    });
    container.innerHTML = html;
  }

  // ─── Bairros ───
  function loadBairros(bairros) {
    if (!bairros) return;

    // Expose bairros for map script FIRST (before DOM update)
    window._cfgBairros = bairros;

    var container = document.getElementById('bairrosTags');
    if (!container) return;

    var html = '';
    bairros.forEach(function (b) {
      html += '<span class="neighborhood-tag" data-bairro="' + b.dataBairro + '">' + b.nome + '</span>';
    });
    html += '<span class="neighborhood-tag neighborhood-new">+ Novos bairros em breve</span>';
    container.innerHTML = html;

    // Re-attach tag click handlers
    container.querySelectorAll('.neighborhood-tag[data-bairro]').forEach(function (tag) {
      tag.addEventListener('click', function () {
        var bairroName = tag.getAttribute('data-bairro');
        var match = bairros.find(function (b) { return b.dataBairro === bairroName; });
        if (match && window._covMap) {
          window._covMap.flyTo([match.lat, match.lng], 15, { duration: 1 });
          container.querySelectorAll('.neighborhood-tag').forEach(function (t) { t.classList.remove('tag-active'); });
          tag.classList.add('tag-active');
        }
      });
    });
  }

  // ─── Depoimentos ───
  function loadDepoimentos(deps) {
    if (!deps) return;
    var container = document.getElementById('testimonialsGrid');
    if (!container) return;

    var html = '';
    deps.forEach(function (d) {
      var stars = '';
      for (var i = 0; i < (d.estrelas || 5); i++) {
        stars += '<i class="ph-fill ph-star"></i>';
      }
      var initial = d.nome.charAt(0).toUpperCase();
      html += '<div class="testimonial-card">' +
        '<div class="testimonial-stars">' + stars + '</div>' +
        '<p>"' + d.texto + '"</p>' +
        '<div class="testimonial-author">' +
          '<div class="testimonial-avatar">' + initial + '</div>' +
          '<div><strong>' + d.nome + '</strong><span>' + d.local + '</span></div>' +
        '</div>' +
        '</div>';
    });
    container.innerHTML = html;
  }

  // ─── FAQ ───
  function loadFaq(faqs) {
    if (!faqs) return;
    var container = document.getElementById('faqList');
    if (!container) return;

    var html = '';
    faqs.forEach(function (f) {
      html += '<div class="faq-item">' +
        '<button class="faq-question">' +
          '<span>' + f.pergunta + '</span>' +
          '<i class="ph ph-caret-down"></i>' +
        '</button>' +
        '<div class="faq-answer"><p>' + f.resposta + '</p></div>' +
        '</div>';
    });
    container.innerHTML = html;

    // Re-attach FAQ toggle
    container.querySelectorAll('.faq-question').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var item = btn.parentElement;
        var isOpen = item.classList.contains('active');
        container.querySelectorAll('.faq-item').forEach(function (el) { el.classList.remove('active'); });
        if (!isOpen) item.classList.add('active');
      });
    });
  }

  // ─── Footer ───
  function loadFooter(emp) {
    if (!emp) return;
    setHTML('#footerEndereco', '<i class="ph ph-map-pin"></i> ' + emp.endereco + '<br>' + emp.bairroEndereco + ' \u2013 ' + emp.cidade + '<br>CEP: ' + emp.cep);
    setHTML('#footerTelefone', '<i class="ph ph-phone"></i> ' + emp.telefone);
    setHTML('#footerWhatsapp', '<i class="ph ph-whatsapp-logo"></i> ' + emp.whatsappFormatado);
    setHTML('#footerEmail', '<i class="ph ph-envelope"></i> ' + emp.email);
    setHTML('#footerCnpj', '\u00a9 2026 MasterInfo Internet. Todos os direitos reservados. CNPJ: ' + emp.cnpj);

    // Social links
    setHref('#footerInstagram', emp.instagram);
    setHref('#footerFacebook', emp.facebook);

    // Footer brand text
    setText('#footerDesc', 'Internet fibra optica 100% em ' + emp.cidade + '. Mais de 6 anos conectando familias e empresas da regiao.');
  }

  // ─── Helpers ───
  function setText(sel, val) {
    var el = document.querySelector(sel);
    if (el && val) el.textContent = val;
  }

  function setHTML(sel, val) {
    var el = document.querySelector(sel);
    if (el && val) el.innerHTML = val;
  }

  function setHref(sel, val) {
    var el = document.querySelector(sel);
    if (el && val) el.href = val;
  }

  function esc(str) {
    if (!str) return '';
    var d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
  }
})();
