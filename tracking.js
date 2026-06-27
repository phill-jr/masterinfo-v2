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
  var miUserData = null;   // dados do cliente p/ Correspondência Avançada (Advanced Matching)

  // ── POLÍTICA DE CONSENTIMENTO DOS PIXELS (LGPD) ──────────────────────────────
  // Fica AQUI (tracking.js é versionado e vai pro deploy direto). NÃO no config.json:
  // o deploy.sh (passo 0.5) PUXA o config.json da produção e sobrescreveria qualquer
  // flag posto no repo. Por isso o controle mora no código.
  //   false = pixels (Meta/Google Ads) DISPARAM NO LOAD; o banner de cookies continua
  //           aparecendo, mas só como AVISO (clicar não muda o disparo).
  //   true  = pixels só disparam APÓS o aceite de marketing no banner (LGPD estrito).
  // config.tracking.requireConsent, SE existir, tem prioridade sobre este padrão.
  // ⚠️ Decisão do dono do site; disparar marketing antes do aceite é cinza na ANPD.
  var REQUIRE_CONSENT_DEFAULT = false;

  // ═══════════════════════════════════════════════
  //  JORNADA DO CLIENTE (1st-party → comentário do lead no Bitrix)
  //  Origem/UTM e páginas são captadas SEMPRE (mesmo com pixels off);
  //  a trilha de cliques (plano/CTA) usa os eventos do miTrack.
  // ═══════════════════════════════════════════════
  var JRN_KEY = 'mi_jrn', SRC_KEY = 'mi_src', VIS_KEY = 'mi_visits';

  function jrnGet() { try { return JSON.parse(sessionStorage.getItem(JRN_KEY)) || []; } catch (e) { return []; } }
  function jrnPush(code, label) {
    try {
      var a = jrnGet();
      label = (label == null ? '' : String(label)).substring(0, 60);
      var last = a[a.length - 1];
      if (last && last.e === code && last.d === label) return; // colapsa repetição
      a.push({ t: Date.now(), e: code, d: label });
      if (a.length > 40) a = a.slice(-40);
      sessionStorage.setItem(JRN_KEY, JSON.stringify(a));
    } catch (e) {}
  }

  function curPageName() {
    var page = location.pathname.replace(/\/$/, '') || '/';
    return ({
      '/index.html': 'Home', '/index': 'Home', '/index-light.html': 'Home', '/index-light': 'Home',
      '/checkout.html': 'Checkout', '/checkout': 'Checkout', '/admin.html': 'Admin', '/': 'Home',
      '/familia': 'Família', '/home-office': 'Home Office', '/gamer': 'Gamer', '/tv-streaming': 'TV e Streaming',
      '/com-1-roteador': 'Com 1 Roteador', '/com-2-roteadores': 'Com 2 Roteadores', '/contato': 'Contato', '/copa': 'Copa'
    }[page]) || page;
  }

  function recordSource() {
    try {
      var visits = parseInt(localStorage.getItem(VIS_KEY) || '0', 10) || 0;
      if (sessionStorage.getItem(SRC_KEY)) return;          // 1x por sessão
      visits += 1; try { localStorage.setItem(VIS_KEY, String(visits)); } catch (e) {}
      var q = new URLSearchParams(location.search);
      var ref = document.referrer || '';
      var sameHost = ref && ref.indexOf(location.host) !== -1;
      sessionStorage.setItem(SRC_KEY, JSON.stringify({
        utm_source: q.get('utm_source') || '', utm_medium: q.get('utm_medium') || '',
        utm_campaign: q.get('utm_campaign') || '', utm_content: q.get('utm_content') || '',
        utm_term: q.get('utm_term') || '', gclid: q.get('gclid') || '', fbclid: q.get('fbclid') || '',
        referrer: sameHost ? '' : ref, landing: location.pathname, firstSeen: Date.now(), visits: visits
      }));
    } catch (e) {}
  }

  // Monta o resumo legível pro comentário do lead. '' se não houver nada.
  window.miJourneyText = function () {
    try {
      var src = {}; try { src = JSON.parse(sessionStorage.getItem(SRC_KEY)) || {}; } catch (e) {}
      var jrn = jrnGet(), L = [];
      var uniq = function (arr) { return arr.filter(function (v, i) { return v && arr.indexOf(v) === i; }); };
      var of = function (code) { return jrn.filter(function (x) { return x.e === code; }).map(function (x) { return x.d; }); };

      var origem = [];
      if (src.utm_source) origem.push(src.utm_source + (src.utm_medium ? '/' + src.utm_medium : ''));
      if (src.utm_campaign) origem.push('camp: ' + src.utm_campaign);
      if (src.gclid) origem.push('Google Ads (gclid)');
      if (src.fbclid) origem.push('Facebook (fbclid)');
      if (!origem.length && src.referrer) origem.push('ref: ' + src.referrer);
      if (!origem.length) origem.push('direto/orgânico');
      L.push('Origem: ' + origem.join(' · '));
      if (src.landing) L.push('Entrada: ' + src.landing + (src.utm_content ? ' (' + src.utm_content + ')' : ''));

      var planos = uniq(of('plan')); if (planos.length) L.push('Planos vistos: ' + planos.join(', '));
      var cep = of('cep').pop(); if (cep) L.push('CEP: ' + cep);
      var pgs = of('pg').filter(function (v, i, a) { return !i || a[i - 1] !== v; }); if (pgs.length) L.push('Páginas: ' + pgs.join(' → '));
      var cliques = uniq(of('cta')); if (cliques.length) L.push('Cliques: ' + cliques.slice(0, 6).join(', '));

      var eng = [];
      if (src.firstSeen) { var s = Math.round((Date.now() - src.firstSeen) / 1000); eng.push('tempo ' + (s >= 60 ? Math.floor(s / 60) + 'min' + (s % 60) + 's' : s + 's')); }
      var scrolls = of('scroll').map(function (d) { return parseInt(d, 10) || 0; }); if (scrolls.length) eng.push('scroll ' + Math.max.apply(null, scrolls) + '%');
      if (src.visits) eng.push(src.visits + 'ª visita');
      if (eng.length) L.push('Engajamento: ' + eng.join(' · '));

      return L.length ? ('— Jornada no site —\n' + L.join('\n')) : '';
    } catch (e) { return ''; }
  };

  // Captura origem + página de entrada SEMPRE (independe do enableTracking)
  recordSource();
  jrnPush('pg', curPageName());

  // Inicializa SÓ as tags permitidas pelo consentimento (LGPD/ANPD).
  //   Análise  -> GTM + GA4
  //   Marketing-> Google Ads + Facebook Pixel
  // Idempotente: cada tag entra uma única vez. Reexecuta quando o consentimento muda.
  var _inited = { gtm: false, ga4: false, ads: false, fb: false };
  function initAllowed() {
    if (!cfg || !cfg.enableTracking) return;
    var c = window.miConsent || { analytics: false, marketing: false };
    if ((c.analytics || c.marketing) && !_inited.gtm) { _inited.gtm = true; initGTM(cfg.gtmId); }
    if (c.analytics && !_inited.ga4) { _inited.ga4 = true; initGA4(cfg.ga4Id); }
    if (c.marketing && !_inited.ads) { _inited.ads = true; initGoogleAds(cfg.googleAdsId); }
    if (c.marketing && !_inited.fb) { _inited.fb = true; initFacebookPixel(cfg.facebookPixelId); }
  }

  // SEM gate de consentimento: dispara TODOS os pixels configurados já no load.
  // Usado quando cfg.requireConsent === false — o banner (cookie-consent.js) segue
  // aparecendo só como AVISO, mas o pixel não espera o aceite.
  function initAll() {
    if (!cfg || !cfg.enableTracking) return;
    if (!_inited.gtm) { _inited.gtm = true; initGTM(cfg.gtmId); }
    if (!_inited.ga4) { _inited.ga4 = true; initGA4(cfg.ga4Id); }
    if (!_inited.ads) { _inited.ads = true; initGoogleAds(cfg.googleAdsId); }
    if (!_inited.fb)  { _inited.fb  = true; initFacebookPixel(cfg.facebookPixelId); }
  }

  // ─── Carregamento ADIADO dos pixels (perf: ↓TBT/INP/LCP) ───
  // Inicializa GTM/GA4/Ads/FB FORA da janela crítica de load: no 1º gesto do usuário
  // (pointerdown/keydown/touchstart/scroll) OU em idle após o load — o que vier antes.
  // Conversão NÃO se perde: ela exige clique, e no 1º gesto os stubs fbq/gtag já existem
  // (o evento do clique fica enfileirado e é enviado quando o script async carrega).
  // A jornada 1st-party (gclid/fbclid→Bitrix) e os links wa.me NÃO dependem disto e
  // continuam IMEDIATOS mais abaixo. requestIdleCallback c/ timeout garante o disparo
  // (page_view/remarketing) mesmo sem interação, ~3s após o load.
  function oncePixelsReady(cb) {
    var done = false;
    var evs = ['pointerdown', 'keydown', 'touchstart', 'scroll'];
    var opts = { passive: true, capture: true };
    function go() {
      if (done) return; done = true;
      for (var i = 0; i < evs.length; i++) window.removeEventListener(evs[i], go, opts);
      cb();
    }
    for (var j = 0; j < evs.length; j++) window.addEventListener(evs[j], go, opts);
    var idle = function () {
      if ('requestIdleCallback' in window) window.requestIdleCallback(go, { timeout: 3000 });
      else setTimeout(go, 2500);
    };
    if (document.readyState === 'complete') idle();
    else window.addEventListener('load', idle, { once: true });
  }

  // ─── Bootstrap: carrega config e inicializa tudo ───
  (window.miCfg ? window.miCfg() : fetch('/config.json?v=' + Date.now()).then(function (r) { return r.json(); }))
    .then(function (data) {
      cfg = data.tracking || {};
      // Pixels (GTM/GA4/Ads/FB) só com enableTracking ligado + IDs configurados,
      // ADIADOS pra fora do load (oncePixelsReady) e respeitando o consentimento (LGPD).
      if (cfg.enableTracking) {
        // config tem prioridade; sem o campo, usa o padrão do código (REQUIRE_CONSENT_DEFAULT)
        var needConsent = (cfg.requireConsent === undefined || cfg.requireConsent === null)
          ? REQUIRE_CONSENT_DEFAULT : !!cfg.requireConsent;
        oncePixelsReady(function () {
          if (!needConsent) {
            // Sem gate de consentimento: dispara os pixels (banner segue como AVISO).
            console.info('[Tracking] consentimento dispensado → pixels no 1º gesto/idle (banner é só aviso).');
            initAll();
          } else if (typeof window.miOnConsent === 'function') {
            window.miOnConsent(initAllowed);            // dispara agora se já decidido; e a cada mudança
          } else {
            // cookie-consent.js ausente: sem consentimento explícito, NÃO dispara pixels.
            console.info('[Tracking] cookie-consent.js ausente; pixels aguardam consentimento.');
            window.addEventListener('mi:consent', initAllowed);
          }
          trackPageView();             // page_view (pixels) após o init — vai pro dataLayer/gtag/fbq
        });
      } else {
        console.info('[Tracking] Pixels desabilitados; jornada 1st-party (p/ lead no Bitrix) continua ativa.');
        trackPageView();               // sem pixels: registra só a jornada 1st-party
      }
      // Handlers SEMPRE imediatos: alimentam a jornada do lead + atribuição WhatsApp (gclid).
      // Dentro do miTrack, os pixels só disparam se a tag já foi inicializada.
      trackWhatsAppClicks();
      tagAllWaLinks();                 // marca os links wa.me já presentes na página
      setTimeout(tagAllWaLinks, 1500); // e os injetados depois (widget Marina, rodapé, modais)
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
    // Carrega o gtag.js do PROPRIO ID do Google Ads, checando o ID ESPECIFICO (nao "qualquer
    // gtag.js"). Quando ha um GA4 configurado (ga4Id), o initGA4 ja carregou gtag.js?id=<GA4>;
    // o guard antigo ("existe algum gtag.js?") fazia o initGoogleAds PULAR, e o tag do Ads
    // ficava so como config secundario -> NAO ativa se o AW nao estiver linkado como destino do
    // GA4, e a conversao do form era chamada mas NUNCA transmitida (FORMULARIO 01 = 0). Carregar
    // o gtag.js?id=<AW> garante o tag do Ads ativo (multi-tag e suportado: cada gtag/js?id=X
    // registra o destino X). Sem GA4 (ga4Id vazio) continua igual ao comportamento anterior.
    // Bug diagnosticado 27/06/2026 (form chamava a conversao, mas o Ads nao transmitia).
    if (!document.querySelector('script[src*="gtag/js?id=' + id + '"]')) {
      var s = document.createElement('script');
      s.async = true;
      s.src = 'https://www.googletagmanager.com/gtag/js?id=' + id;
      document.head.appendChild(s);
    }
    if (!window.gtag) {
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag('js', new Date());
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
    // 2º arg = Correspondência Avançada (e-mail/telefone/nome/CPF). Se já identificado, vai junto;
    // o fbevents.js faz o hash SHA-256 no navegador. Eleva a qualidade de correspondência (EMQ).
    window.fbq('init', id, miUserData || undefined);
    window.fbq('track', 'PageView');
  }

  // ═══════════════════════════════════════════════
  //  CORRESPONDÊNCIA AVANÇADA (Advanced Matching) + ATRIBUIÇÃO
  // ═══════════════════════════════════════════════

  // Normaliza dados do cliente p/ Advanced Matching (lowercase/trim/dígitos).
  // O fbevents.js faz o hash SHA-256 no navegador antes de enviar.
  function buildAdvancedMatching(u) {
    var am = {};
    if (!u) return am;
    if (u.email) am.em = String(u.email).trim().toLowerCase();
    if (u.phone) { var d = String(u.phone).replace(/\D/g, ''); if (d) am.ph = (d.length <= 11 ? '55' + d : d); }
    if (u.nome) {
      var parts = String(u.nome).trim().toLowerCase().split(/\s+/);
      if (parts[0]) am.fn = parts[0];
      if (parts.length > 1) am.ln = parts[parts.length - 1];
    }
    if (u.cpf) am.external_id = String(u.cpf).replace(/\D/g, '');
    if (u.cidade) am.ct = String(u.cidade).trim().toLowerCase().replace(/\s+/g, '');
    if (u.uf) am.st = String(u.uf).trim().toLowerCase();
    if (u.cep) am.zp = String(u.cep).replace(/\D/g, '');
    return am;
  }

  // Identifica o cliente (Advanced Matching). Pode ser chamada a qualquer momento do checkout;
  // se o pixel ainda não inicializou (sem consentimento), guarda p/ usar no init.
  window.miIdentify = function (user) {
    try {
      var am = buildAdvancedMatching(user);
      if (!am || !Object.keys(am).length) return;
      miUserData = Object.assign(miUserData || {}, am);
      if (typeof window.fbq === 'function' && cfg && cfg.facebookPixelId && _inited.fb) {
        window.fbq('init', cfg.facebookPixelId, miUserData); // re-init adiciona AM aos próximos eventos
      }
    } catch (e) {}
  };

  // Identificadores de atribuição p/ enviar ao Bitrix (→ o CAPI do Sync Hub usa como fbc/fbp).
  window.miAttribution = function () {
    var src = {}; try { src = JSON.parse(sessionStorage.getItem(SRC_KEY)) || {}; } catch (e) {}
    var fbp = (document.cookie.match(/_fbp=([^;]+)/) || [])[1] || '';
    var fbc = (document.cookie.match(/_fbc=([^;]+)/) || [])[1] || '';
    if (!fbc && src.fbclid) fbc = 'fb.1.' + Date.now() + '.' + src.fbclid; // monta o fbc a partir do fbclid
    return { fbclid: src.fbclid || '', fbp: fbp, fbc: fbc, gclid: src.gclid || '' };
  };

  // ═══════════════════════════════════════════════
  //  EVENTO CENTRAL: miTrack()
  // ═══════════════════════════════════════════════

  window.miTrack = function (eventName, params) {
    params = params || {};

    // ── Jornada (antes do gate: registra mesmo com pixels desligados) ──
    try {
      if (eventName === 'plan_click') { if (params.plan) jrnPush('plan', params.plan + (params.value ? ' (R$ ' + Number(params.value).toFixed(2).replace('.', ',') + ')' : '')); }
      else if (eventName === 'cta_click') jrnPush('cta', params.label || '');
      else if (eventName === 'cep_check') jrnPush('cep', (params.cep || '') + (params.viable ? ' (com cobertura)' : ''));
      else if (eventName === 'whatsapp_click') jrnPush('cta', 'WhatsApp (' + (params.context || '') + ')');
      else if (eventName === 'page_view') jrnPush('pg', params.page_name || curPageName());
      else if (eventName === 'scroll_depth') jrnPush('scroll', params.percent);
      else if (eventName === 'modal_open') jrnPush('cta', 'Abriu modal' + (params.plan ? ' — ' + params.plan : ''));
      else if (eventName === 'begin_checkout') jrnPush('cta', 'Iniciou checkout' + (params.plan ? ' — ' + params.plan : ''));
      else if (eventName === 'waitlist_signup') jrnPush('cep', (params.cep || '') + ' (sem cobertura)');
    } catch (e) {}

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
        // 'purchase' = conclusão do checkout NO SITE (signup, não pagamento) → CompleteRegistration.
        // O Purchase REAL (contrato assinado) sai só pelo CAPI server-side, no mesmo pixel → evita contar 2x.
        'purchase': function () { window.fbq('track', 'CompleteRegistration', { content_name: params.plan || '', content_category: 'Internet Fibra', value: params.value || 0, currency: 'BRL' }); },
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
    var pageName = curPageName();

    window.miTrack('page_view', {
      page_title: document.title,
      page_location: location.href,
      page_path: page,
      page_name: pageName
    });
  }

  // ─── Atribuição no WhatsApp: injeta #mi_gc=/#mi_fbc= no texto pré-preenchido do wa.me ───
  //   Quando o visitante chegou de anúncio (gclid/fbclid na URL → mi_src), o Sync Hub
  //   (WaFbclidCapture) lê esse marcador na 1ª mensagem do cliente e atribui a venda do
  //   contrato à campanha (Google Ads / Meta). Espelha o snippet do WordPress. No-op sem gclid/fbclid.
  function waAttributionMarker() {
    var src = {}; try { src = JSON.parse(sessionStorage.getItem(SRC_KEY)) || {}; } catch (e) {}
    var g = String(src.gclid || '').replace(/[^A-Za-z0-9_\-.]/g, '');
    var f = String(src.fbclid || '').replace(/[^A-Za-z0-9_\-.]/g, '');
    var m = '';
    if (g) m += ' #mi_gc=' + g;
    if (f) m += ' #mi_fbc=' + f;
    return m;
  }
  function tagWaLink(link) {
    try {
      if (!link || !link.href) return;
      var m = waAttributionMarker();
      if (!m) return;
      var u = new URL(link.href, location.href);
      var t = u.searchParams.get('text') || '';
      if (t.indexOf('#mi_gc=') !== -1 || t.indexOf('#mi_fbc=') !== -1) return; // já marcado (texto decodificado — evita duplicar)
      u.searchParams.set('text', t + m);
      link.href = u.toString();
    } catch (e) {}
  }
  function tagAllWaLinks() {
    if (!waAttributionMarker()) return;
    var links = document.querySelectorAll('a[href*="wa.me"], a[href*="api.whatsapp.com"]');
    for (var i = 0; i < links.length; i++) tagWaLink(links[i]);
  }

  // ─── WhatsApp: interceptar todos os cliques ───
  function trackWhatsAppClicks() {
    document.addEventListener('click', function (e) {
      var link = e.target.closest('a[href*="wa.me"], a[href*="api.whatsapp.com"]');
      if (!link) return;
      tagWaLink(link); // injeta o marcador de atribuição (#mi_gc=/#mi_fbc=) antes de abrir o WhatsApp

      var context = 'unknown';
      if (link.closest('.hero')) context = 'hero';
      else if (link.closest('.final-cta, .cta-banner')) context = 'cta_final';
      else if (link.closest('.footer')) context = 'footer';
      else if (link.closest('.whatsapp-float, .boleto-float')) context = 'float_button';
      else if (link.closest('.mi-modal-card')) context = 'modal_success';
      else if (link.id === 'ckWhatsappLink' || link.id === 'checkoutWhatsapp' || link.closest('.checkout, .checkout-main, .checkout-content, .checkout-layout')) context = 'checkout_success';

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
      else if (btn.closest('.final-cta, .cta-banner')) section = 'cta_final';
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

      // Sem .plan-name no markup: deriva da velocidade, ou do ?plano= do link.
      var name = planName ? planName.textContent.trim() : '';
      if (!name && planSpeed) name = (planSpeed.textContent.trim() + ' ' + (planUnit ? planUnit.textContent.trim() : '')).trim();
      if (!name && btn.href) { var pm = btn.href.match(/plano=([^&]+)/); if (pm) name = decodeURIComponent(pm[1]); }

      window.miTrack('plan_click', {
        plan: name,
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
