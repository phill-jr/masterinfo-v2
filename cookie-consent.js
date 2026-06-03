/**
 * MasterInfo — Consentimento de Cookies (LGPD / Guia ANPD de Cookies)
 * Banner granular: Necessários (sempre on) · Análise (opt-in) · Marketing (opt-in).
 *
 * - Seta Google Consent Mode v2 = DENIED antes de qualquer tag (default).
 * - Atualiza para GRANTED conforme a escolha do usuário.
 * - Expõe:
 *     window.miConsent              -> { necessary, analytics, marketing, decided }
 *     window.miOnConsent(cb)        -> registra callback (chamado quando há/muda decisão)
 *     window.miCookiePrefs()        -> reabre o painel de preferências
 *     evento 'mi:consent' (window)  -> detail = window.miConsent
 *
 * tracking.js consome isso para só inicializar GA4/GTM/Ads/Pixel após o aceite.
 * Autossuficiente: injeta o próprio CSS. Não roda no /admin.
 */
(function () {
  'use strict';

  // Não exibir em páginas internas (admin/login).
  var path = (location.pathname || '').toLowerCase();
  if (path.indexOf('admin') !== -1) return;

  var STORE_KEY = 'mi_cookie_consent';
  var VERSION = 1; // incrementar para re-solicitar consentimento se a política mudar
  var POLICY_URL = '/privacidade/#cookies';

  // ─── Consent Mode v2: padrão NEGADO, antes de qualquer tag do Google ───
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  if (typeof window.gtag !== 'function') window.gtag = gtag;
  window.gtag('consent', 'default', {
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: 'denied',
    functionality_storage: 'granted',
    security_storage: 'granted',
    wait_for_update: 500
  });

  // ─── Estado / persistência ───
  function read() {
    try {
      var o = JSON.parse(localStorage.getItem(STORE_KEY));
      if (o && o.v === VERSION) return o;
    } catch (e) {}
    return null;
  }
  var listeners = [];
  window.miConsent = { necessary: true, analytics: false, marketing: false, decided: false };
  window.miOnConsent = function (cb) {
    if (typeof cb !== 'function') return;
    listeners.push(cb);
    if (window.miConsent.decided) { try { cb(window.miConsent); } catch (e) {} }
  };

  function apply(o) {
    window.miConsent = { necessary: true, analytics: !!o.analytics, marketing: !!o.marketing, decided: true };
    window.gtag('consent', 'update', {
      analytics_storage: o.analytics ? 'granted' : 'denied',
      ad_storage: o.marketing ? 'granted' : 'denied',
      ad_user_data: o.marketing ? 'granted' : 'denied',
      ad_personalization: o.marketing ? 'granted' : 'denied'
    });
    listeners.forEach(function (cb) { try { cb(window.miConsent); } catch (e) {} });
    try { window.dispatchEvent(new CustomEvent('mi:consent', { detail: window.miConsent })); } catch (e) {}
  }

  function persist(analytics, marketing) {
    var o = { v: VERSION, necessary: true, analytics: !!analytics, marketing: !!marketing, ts: Date.now() };
    try { localStorage.setItem(STORE_KEY, JSON.stringify(o)); } catch (e) {}
    apply(o);
  }

  var existing = read();
  if (existing) apply(existing); // já decidiu antes → aplica sem mostrar banner

  // ─── CSS injetado ───
  function injectCSS() {
    if (document.getElementById('mi-cc-style')) return;
    var css = '' +
    '.mi-cc-banner,.mi-cc-modal,.mi-cc-modal *{box-sizing:border-box;font-family:"Outfit",system-ui,-apple-system,Segoe UI,Roboto,sans-serif}' +
    '.mi-cc-banner{position:fixed;left:16px;right:16px;bottom:16px;z-index:2147483600;max-width:940px;margin:0 auto;' +
      'background:#fff;color:#1b1b22;border:1.5px solid #ececf2;border-radius:18px;box-shadow:0 20px 60px rgba(20,20,30,.28);' +
      'padding:20px 22px;display:flex;gap:18px;align-items:center;flex-wrap:wrap;' +
      'opacity:0;transform:translateY(20px);transition:opacity .35s ease,transform .35s ease}' +
    '.mi-cc-banner.mi-cc-in{opacity:1;transform:none}' +
    '.mi-cc-ico{flex-shrink:0;width:46px;height:46px;border-radius:13px;display:grid;place-items:center;font-size:1.5rem;color:#fff;' +
      'background:linear-gradient(135deg,#e63946,#ff7a05,#fcc305);box-shadow:0 8px 18px rgba(255,122,5,.3)}' +
    '.mi-cc-text{flex:1 1 320px;min-width:240px;font-size:.95rem;line-height:1.55;color:#41414d}' +
    '.mi-cc-text strong{color:#16161c;font-weight:800;display:block;margin-bottom:2px;font-size:1.02rem}' +
    '.mi-cc-text a{color:#e06800;font-weight:700;text-decoration:none}.mi-cc-text a:hover{text-decoration:underline}' +
    '.mi-cc-actions{display:flex;gap:10px;flex-wrap:wrap;align-items:center}' +
    '.mi-cc-btn{cursor:pointer;border:none;font-family:inherit;font-weight:800;font-size:.92rem;padding:12px 18px;border-radius:999px;' +
      'transition:transform .15s ease,box-shadow .15s ease,background .15s ease,border-color .15s ease;white-space:nowrap}' +
    '.mi-cc-btn:hover{transform:translateY(-2px)}' +
    '.mi-cc-btn-primary{color:#fff;background:linear-gradient(135deg,#e63946,#ff7a05,#fcc305);box-shadow:0 12px 28px rgba(255,122,5,.34)}' +
    '.mi-cc-btn-ghost{background:#f4f4f7;color:#3a3a45}' +
    '.mi-cc-btn-ghost:hover{background:#ececf2}' +
    '.mi-cc-btn-link{background:none;color:#5a5a66;padding:12px 10px;text-decoration:underline;font-weight:700}' +
    '.mi-cc-btn-link:hover{color:#16161c;transform:none}' +
    /* modal */
    '.mi-cc-modal{position:fixed;inset:0;z-index:2147483601;display:none;align-items:center;justify-content:center;padding:18px;' +
      'background:rgba(15,15,22,.55);backdrop-filter:blur(3px);-webkit-backdrop-filter:blur(3px)}' +
    '.mi-cc-modal.mi-cc-open{display:flex}' +
    '.mi-cc-card{background:#fff;width:100%;max-width:560px;max-height:90vh;overflow-y:auto;border-radius:22px;' +
      'box-shadow:0 30px 80px rgba(0,0,0,.4);padding:28px;transform:translateY(16px) scale(.98);opacity:0;transition:transform .3s ease,opacity .3s ease}' +
    '.mi-cc-modal.mi-cc-open .mi-cc-card{transform:none;opacity:1}' +
    '.mi-cc-card h2{font-size:1.4rem;font-weight:900;letter-spacing:-.02em;color:#14141a;margin:0 0 6px}' +
    '.mi-cc-card .mi-cc-sub{color:#5a5a66;font-size:.95rem;line-height:1.55;margin:0 0 20px}' +
    '.mi-cc-card .mi-cc-sub a{color:#e06800;font-weight:700;text-decoration:none}.mi-cc-card .mi-cc-sub a:hover{text-decoration:underline}' +
    '.mi-cc-row{display:flex;gap:14px;align-items:flex-start;padding:16px 0;border-top:1px solid #ececf2}' +
    '.mi-cc-row-body{flex:1}' +
    '.mi-cc-row h3{font-size:1rem;font-weight:800;color:#16161c;margin:0 0 3px}' +
    '.mi-cc-row p{font-size:.88rem;line-height:1.5;color:#5a5a66;margin:0}' +
    '.mi-cc-switch{position:relative;flex-shrink:0;width:46px;height:26px;margin-top:2px}' +
    '.mi-cc-switch input{position:absolute;opacity:0;width:100%;height:100%;margin:0;cursor:pointer}' +
    '.mi-cc-track{position:absolute;inset:0;border-radius:999px;background:#d4d4dd;transition:background .2s ease}' +
    '.mi-cc-track::before{content:"";position:absolute;top:3px;left:3px;width:20px;height:20px;border-radius:50%;background:#fff;box-shadow:0 2px 5px rgba(0,0,0,.25);transition:transform .2s ease}' +
    '.mi-cc-switch input:checked+.mi-cc-track{background:linear-gradient(135deg,#e63946,#ff7a05)}' +
    '.mi-cc-switch input:checked+.mi-cc-track::before{transform:translateX(20px)}' +
    '.mi-cc-switch input:disabled+.mi-cc-track{background:linear-gradient(135deg,#9aa0aa,#b9bec6);cursor:not-allowed}' +
    '.mi-cc-switch input:disabled+.mi-cc-track::before{transform:translateX(20px)}' +
    '.mi-cc-locked{font-size:.7rem;font-weight:700;color:#16a34a;text-transform:uppercase;letter-spacing:.05em;display:inline-flex;align-items:center;gap:4px;margin-top:4px}' +
    '.mi-cc-card-actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}' +
    '.mi-cc-card-actions .mi-cc-btn{flex:1 1 auto}' +
    '@media (max-width:620px){.mi-cc-banner{padding:18px;gap:14px}.mi-cc-actions{width:100%}.mi-cc-actions .mi-cc-btn{flex:1 1 auto;text-align:center}.mi-cc-btn-link{flex-basis:100%}}' +
    '@media (prefers-reduced-motion:reduce){.mi-cc-banner,.mi-cc-card,.mi-cc-btn{transition:none}}';
    var st = document.createElement('style');
    st.id = 'mi-cc-style';
    st.textContent = css;
    document.head.appendChild(st);
  }

  // ─── Banner ───
  var bannerEl = null, modalEl = null;

  function buildBanner() {
    if (bannerEl) return;
    bannerEl = document.createElement('div');
    bannerEl.className = 'mi-cc-banner';
    bannerEl.setAttribute('role', 'region');
    bannerEl.setAttribute('aria-label', 'Aviso de cookies');
    bannerEl.innerHTML =
      '<span class="mi-cc-ico" aria-hidden="true"><i class="ph-fill ph-cookie"></i></span>' +
      '<div class="mi-cc-text"><strong>A gente usa cookies 🍪</strong>' +
      'Usamos cookies necessários para o site funcionar e, com a sua autorização, cookies de análise e marketing ' +
      'para melhorar sua experiência. Veja a <a href="' + POLICY_URL + '">Política de Privacidade</a>.</div>' +
      '<div class="mi-cc-actions">' +
        '<button type="button" class="mi-cc-btn mi-cc-btn-link" data-cc="custom">Personalizar</button>' +
        '<button type="button" class="mi-cc-btn mi-cc-btn-ghost" data-cc="reject">Só os necessários</button>' +
        '<button type="button" class="mi-cc-btn mi-cc-btn-primary" data-cc="accept">Aceitar todos</button>' +
      '</div>';
    document.body.appendChild(bannerEl);
    bannerEl.addEventListener('click', function (e) {
      var b = e.target.closest('[data-cc]'); if (!b) return;
      var a = b.getAttribute('data-cc');
      if (a === 'accept') { persist(true, true); hideBanner(); }
      else if (a === 'reject') { persist(false, false); hideBanner(); }
      else if (a === 'custom') { openModal(); }
    });
    // reveal com setTimeout (rAF não dispara em aba em 2º plano / headless)
    setTimeout(function () { if (bannerEl) bannerEl.classList.add('mi-cc-in'); }, 30);
  }
  function hideBanner() {
    if (!bannerEl) return;
    bannerEl.classList.remove('mi-cc-in');
    setTimeout(function () { if (bannerEl && bannerEl.parentNode) bannerEl.parentNode.removeChild(bannerEl); bannerEl = null; }, 360);
  }

  // ─── Modal de preferências ───
  function buildModal() {
    if (modalEl) return;
    modalEl = document.createElement('div');
    modalEl.className = 'mi-cc-modal';
    modalEl.setAttribute('role', 'dialog');
    modalEl.setAttribute('aria-modal', 'true');
    modalEl.setAttribute('aria-labelledby', 'mi-cc-title');
    modalEl.innerHTML =
      '<div class="mi-cc-card">' +
        '<h2 id="mi-cc-title">Preferências de cookies</h2>' +
        '<p class="mi-cc-sub">Escolha quais cookies pode usar. Você pode mudar isso quando quiser. ' +
          'Detalhes na <a href="' + POLICY_URL + '">Política de Privacidade</a>.</p>' +
        '<div class="mi-cc-row">' +
          '<div class="mi-cc-row-body"><h3>Necessários</h3><p>Essenciais para o site funcionar (segurança e navegação). Não podem ser desativados.</p>' +
            '<span class="mi-cc-locked"><i class="ph-fill ph-lock-simple"></i> Sempre ativos</span></div>' +
          '<label class="mi-cc-switch"><input type="checkbox" checked disabled aria-label="Necessários (sempre ativos)"><span class="mi-cc-track"></span></label>' +
        '</div>' +
        '<div class="mi-cc-row">' +
          '<div class="mi-cc-row-body"><h3>Análise</h3><p>Ajudam a entender como o site é usado (ex.: Google Analytics), para melhorarmos a experiência.</p></div>' +
          '<label class="mi-cc-switch"><input type="checkbox" id="mi-cc-analytics" aria-label="Cookies de análise"><span class="mi-cc-track"></span></label>' +
        '</div>' +
        '<div class="mi-cc-row">' +
          '<div class="mi-cc-row-body"><h3>Marketing</h3><p>Permitem medir campanhas e mostrar ofertas relevantes (ex.: Google Ads, Meta Pixel).</p></div>' +
          '<label class="mi-cc-switch"><input type="checkbox" id="mi-cc-marketing" aria-label="Cookies de marketing"><span class="mi-cc-track"></span></label>' +
        '</div>' +
        '<div class="mi-cc-card-actions">' +
          '<button type="button" class="mi-cc-btn mi-cc-btn-ghost" data-cc="save">Salvar preferências</button>' +
          '<button type="button" class="mi-cc-btn mi-cc-btn-primary" data-cc="accept-all">Aceitar todos</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(modalEl);
    modalEl.addEventListener('click', function (e) {
      if (e.target === modalEl) { closeModal(); return; } // clique no backdrop
      var b = e.target.closest('[data-cc]'); if (!b) return;
      var a = b.getAttribute('data-cc');
      if (a === 'save') {
        persist(!!modalEl.querySelector('#mi-cc-analytics').checked, !!modalEl.querySelector('#mi-cc-marketing').checked);
        closeModal(); hideBanner();
      } else if (a === 'accept-all') {
        persist(true, true); closeModal(); hideBanner();
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modalEl && modalEl.classList.contains('mi-cc-open')) closeModal();
    });
  }
  function openModal() {
    buildModal();
    var c = window.miConsent || {};
    modalEl.querySelector('#mi-cc-analytics').checked = !!c.analytics;
    modalEl.querySelector('#mi-cc-marketing').checked = !!c.marketing;
    modalEl.classList.add('mi-cc-open');
    var first = modalEl.querySelector('#mi-cc-analytics'); if (first) setTimeout(function () { first.focus(); }, 50);
  }
  function closeModal() { if (modalEl) modalEl.classList.remove('mi-cc-open'); }

  // Reabrir preferências (usado pelo link do rodapé)
  window.miCookiePrefs = function () { injectCSS(); openModal(); };

  // ─── Link "Preferências de cookies" no rodapé (.footer-legal) ───
  function injectFooterLink() {
    var legal = document.querySelector('.footer-legal');
    if (!legal || legal.querySelector('[data-cc-prefs]')) return;
    var sep = document.createElement('span'); sep.textContent = '·';
    var a = document.createElement('a');
    a.href = '#'; a.setAttribute('data-cc-prefs', '1'); a.textContent = 'Preferências de cookies';
    a.addEventListener('click', function (e) { e.preventDefault(); window.miCookiePrefs(); });
    legal.appendChild(sep); legal.appendChild(a);
  }

  // ─── Boot ───
  function boot() {
    injectCSS();
    injectFooterLink();
    if (!existing) buildBanner(); // só mostra se ainda não decidiu
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
  // Rede de segurança: se o rodapé for (re)construído por outro script, garante o link.
  window.addEventListener('load', injectFooterLink);
})();
