/**
 * MasterInfo - Tracking Hub
 * Gerencia GTM, GA4, Google Ads, Facebook Pixel.
 * Carrega IDs do config.json (editaveis pelo admin).
 *
 * Eventos padronizados:
 *   miTrack('page_view')
 *   miTrack('generate_lead', { plan, value })
 *   miTrack('begin_checkout', { plan, value })
 *   miTrack('purchase', { plan, value, orderId })
 *   miTrack('whatsapp_click', { context })
 *   miTrack('cep_check', { cep, viable })
 *   miTrack('waitlist_signup', { cep })
 *   miTrack('plan_click', { plan, value })
 *   miTrack('cta_click', { label })
 */
(function () {
  'use strict';

  var cfg = null;

  // ─── Bootstrap: carrega config e inicializa tudo ───
  fetch('config.json?v=' + Date.now())
    .then(function (r) { return r.json(); })
    .then(function (data) {
      cfg = data.tracking || {};
      if (!cfg.enableTracking) {
        console.info('[Tracking] Tracking desabilitado no config.json');
        return;
      }
      initGTM(cfg.gtmId);
      initGA4(cfg.ga4Id);
      initGoogleAds(cfg.googleAdsId);
      initFacebookPixel(cfg.facebookPixelId);
      trackPageView();
      trackWhatsAppClicks();
      trackCTAClicks();
      trackPlanClicks();
      trackScrollDepth();
    })
    .catch(function (e) {
      console.warn('[Tracking] config.json nao carregado:', e);
    });

  // ═══════════════════════════════════════════════
  //  INICIALIZADORES
  // ═══════════════════════════════════════════════

  // ─── Google Tag Manager ───
  function initGTM(id) {
    if (!id) return;
    // Head script
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtm.js?id=' + id;
    document.head.appendChild(s);

    // dataLayer init
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      'gtm.start': new Date().getTime(),
      event: 'gtm.js'
    });

    // noscript iframe (fallback)
    var ns = document.createElement('noscript');
    var iframe = document.createElement('iframe');
    iframe.src = 'https://www.googletagmanager.com/ns.html?id=' + id;
    iframe.height = '0';
    iframe.width = '0';
    iframe.style.cssText = 'display:none;visibility:hidden';
    ns.appendChild(iframe);
    document.body.insertBefore(ns, document.body.firstChild);
  }

  // ─── Google Analytics 4 (gtag.js) ───
  function initGA4(id) {
    if (!id) return;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + id;
    document.head.appendChild(s);

    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', id, {
      send_page_view: false, // controlamos manualmente
      cookie_flags: 'SameSite=None;Secure'
    });
  }

  // ─── Google Ads (remarketing + conversoes) ───
  function initGoogleAds(id) {
    if (!id) return;
    if (!window.gtag) {
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
    }
    window.gtag('config', id);
  }

  // ─── Facebook Pixel ───
  function initFacebookPixel(id) {
    if (!id) return;
    /* jshint ignore:start */
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
    n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}
    (window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    /* jshint ignore:end */
    window.fbq('init', id);
    window.fbq('track', 'PageView');
  }

  // ═══════════════════════════════════════════════
  //  EVENTO CENTRAL: miTrack()
  // ═══════════════════════════════════════════════

  window.miTrack = function (eventName, params) {
    params = params || {};
    if (!cfg || !cfg.enableTracking) return;

    // ── dataLayer (GTM) ──
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(Object.assign({ event: eventName }, params));

    // ── GA4 (gtag) ──
    if (window.gtag) {
      window.gtag('event', eventName, params);
    }

    // ── Google Ads Conversions ──
    if (window.gtag && cfg.googleAdsId) {
      var convLabels = cfg.googleAdsConversions || {};

      if (eventName === 'generate_lead' && convLabels.lead) {
        window.gtag('event', 'conversion', {
          send_to: cfg.googleAdsId + '/' + convLabels.lead,
          value: params.value || 0,
          currency: 'BRL'
        });
      }

      if (eventName === 'purchase' && convLabels.purchase) {
        window.gtag('event', 'conversion', {
          send_to: cfg.googleAdsId + '/' + convLabels.purchase,
          value: params.value || 0,
          currency: 'BRL',
          transaction_id: params.orderId || ''
        });
      }

      if (eventName === 'whatsapp_click' && convLabels.whatsappClick) {
        window.gtag('event', 'conversion', {
          send_to: cfg.googleAdsId + '/' + convLabels.whatsappClick
        });
      }
    }

    // ── Facebook Pixel ──
    if (typeof window.fbq === 'function') {
      var fbMap = {
        'generate_lead': function () { window.fbq('track', 'Lead', { content_name: params.plan || 'Site MasterInfo', content_category: 'Internet Fibra', value: params.value || 0, currency: 'BRL' }); },
        'purchase': function () { window.fbq('track', 'Purchase', { content_name: params.plan || '', content_category: 'Internet Fibra', value: params.value || 0, currency: 'BRL' }); },
        'begin_checkout': function () { window.fbq('track', 'InitiateCheckout', { content_name: params.plan || '', value: params.value || 0, currency: 'BRL' }); },
        'cep_check': function () { window.fbq('trackCustom', 'CEPCheck', { cep: params.cep, viable: params.viable }); },
        'whatsapp_click': function () { window.fbq('trackCustom', 'WhatsAppClick', { context: params.context }); },
        'plan_click': function () { window.fbq('track', 'ViewContent', { content_name: params.plan, value: params.value || 0, currency: 'BRL' }); }
      };
      if (fbMap[eventName]) fbMap[eventName]();
    }

    // Debug log (remover em producao via GTM)
    console.debug('[Tracking]', eventName, params);
  };

  // ═══════════════════════════════════════════════
  //  AUTO-TRACKING: eventos automaticos
  // ═══════════════════════════════════════════════

  function trackPageView() {
    var page = location.pathname.replace(/\/$/, '') || '/';
    var pageName = {
      '/index-light.html': 'Home',
      '/index-light': 'Home',
      '/checkout.html': 'Checkout',
      '/checkout': 'Checkout',
      '/admin.html': 'Admin',
      '/': 'Home'
    }[page] || page;

    window.miTrack('page_view', {
      page_title: document.title,
      page_location: location.href,
      page_path: page,
      page_name: pageName
    });
  }

  // ─── WhatsApp: interceptar todos os cliques ───
  function trackWhatsAppClicks() {
    document.addEventListener('click', function (e) {
      var link = e.target.closest('a[href*="wa.me"]');
      if (!link) return;

      var context = 'unknown';
      if (link.closest('.hero')) context = 'hero';
      else if (link.closest('.final-cta')) context = 'cta_final';
      else if (link.closest('.footer')) context = 'footer';
      else if (link.closest('.whatsapp-float')) context = 'float_button';
      else if (link.closest('.mi-modal-card')) context = 'modal_success';
      else if (link.id === 'checkoutWhatsapp' || link.closest('.checkout')) context = 'checkout_success';

      window.miTrack('whatsapp_click', { context: context, url: link.href });
    });
  }

  // ─── CTAs: botoes de acao ───
  function trackCTAClicks() {
    document.addEventListener('click', function (e) {
      var btn = e.target.closest('.btn-primary, .btn-plan, .btn-outline');
      if (!btn) return;
      // Pular links WhatsApp (ja rastreados acima)
      if (btn.href && btn.href.indexOf('wa.me') !== -1) return;
      // Pular planos (rastreados separadamente)
      if (btn.classList.contains('btn-plan')) return;

      var label = btn.textContent.trim().substring(0, 50);
      var section = 'unknown';
      if (btn.closest('.hero')) section = 'hero';
      else if (btn.closest('.final-cta')) section = 'cta_final';
      else if (btn.closest('.coverage')) section = 'cobertura';
      else if (btn.closest('header')) section = 'header';

      window.miTrack('cta_click', { label: label, section: section });
    });
  }

  // ─── Planos: clique em "Contratar" ───
  function trackPlanClicks() {
    document.addEventListener('click', function (e) {
      var btn = e.target.closest('.btn-plan');
      if (!btn) return;

      var card = btn.closest('.plan-card');
      if (!card) return;

      var planName = card.querySelector('.plan-name');
      var planValue = card.querySelector('.plan-value');
      var planSpeed = card.querySelector('.plan-speed-num');
      var planUnit = card.querySelector('.plan-speed-unit');

      window.miTrack('plan_click', {
        plan: planName ? planName.textContent : '',
        speed: (planSpeed ? planSpeed.textContent : '') + ' ' + (planUnit ? planUnit.textContent : ''),
        value: planValue ? parseFloat(planValue.textContent) : 0,
        currency: 'BRL'
      });
    });
  }

  // ─── Scroll depth (25%, 50%, 75%, 100%) ───
  function trackScrollDepth() {
    var milestones = { 25: false, 50: false, 75: false, 100: false };

    function checkScroll() {
      var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      var docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      if (docHeight <= 0) return;
      var pct = Math.round((scrollTop / docHeight) * 100);

      [25, 50, 75, 100].forEach(function (m) {
        if (pct >= m && !milestones[m]) {
          milestones[m] = true;
          window.miTrack('scroll_depth', { percent: m, page: location.pathname });
        }
      });
    }

    var throttle = null;
    window.addEventListener('scroll', function () {
      if (throttle) return;
      throttle = setTimeout(function () { throttle = null; checkScroll(); }, 300);
    }, { passive: true });
  }

})();
