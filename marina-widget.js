/**
 * Marina — widget de chat flutuante (boletos / 2a via).
 *
 * Abre o MESMO atendimento da Marina que existe em /ajuda/boletos, porem num
 * popup ancorado no botao .boleto-float — sem trocar de pagina.
 * Backend: /api/marina.php (proxy PHP que guarda o token e fala com a Marina/Sync).
 *
 * Progressive enhancement: se este JS nao rodar, o .boleto-float continua sendo
 * um link normal para /ajuda/boletos (que tem o chat completo).
 *
 * Para usar em qualquer pagina: ter um elemento .boleto-float e incluir este script.
 */
(function () {
  'use strict';

  var PROXY_URL = '/api/marina.php';
  var launcher = document.querySelector('.boleto-float');
  if (!launcher) return;

  // ───────────────────────── estilos ─────────────────────────
  var style = document.createElement('style');
  style.textContent = [
    '.marina-pop{position:fixed;bottom:28px;right:28px;width:374px;max-width:calc(100vw - 32px);height:560px;max-height:calc(100vh - 56px);background:#fff;border-radius:18px;box-shadow:0 24px 60px rgba(0,0,0,0.28),0 4px 16px rgba(0,0,0,0.12);display:flex;flex-direction:column;overflow:hidden;z-index:1000;opacity:0;transform:translateY(16px) scale(0.98);transition:opacity .22s ease,transform .22s ease;}',
    '.marina-pop.is-open{opacity:1;transform:translateY(0) scale(1);}',
    '.marina-pop[hidden]{display:none;}',
    '.marina-pop-head{display:flex;align-items:center;gap:12px;padding:14px 16px;background:linear-gradient(135deg,#ff7a05,#ff5a1f);color:#fff;}',
    '.marina-pop-avatar{width:42px;height:42px;border-radius:50%;background:rgba(255,255,255,0.22);display:flex;align-items:center;justify-content:center;font-size:1.3rem;flex-shrink:0;}',
    '.marina-pop-id{flex:1;line-height:1.2;min-width:0;}',
    '.marina-pop-id strong{display:block;font-size:0.98rem;}',
    '.marina-pop-status{font-size:0.74rem;display:flex;align-items:center;gap:5px;opacity:0.95;}',
    '.marina-pop-dot{width:8px;height:8px;border-radius:50%;background:#7CFFB2;display:inline-block;box-shadow:0 0 0 3px rgba(124,255,178,0.25);}',
    '.marina-pop-close{width:32px;height:32px;border:none;background:rgba(255,255,255,0.18);color:#fff;border-radius:9px;cursor:pointer;font-size:1.05rem;display:flex;align-items:center;justify-content:center;flex-shrink:0;}',
    '.marina-pop-close:hover{background:rgba(255,255,255,0.30);}',
    '.marina-pop-reset{display:none;align-items:center;gap:5px;border:none;background:rgba(255,255,255,0.18);color:#fff;border-radius:9px;cursor:pointer;font-size:0.7rem;font-weight:700;padding:0 10px;height:32px;white-space:nowrap;flex-shrink:0;font-family:inherit;}',
    '.marina-pop-reset.is-visible{display:inline-flex;}',
    '.marina-pop-reset:hover{background:rgba(255,255,255,0.30);}',
    '.marina-pop-reset i{font-size:0.95rem;}',
    '.marina-pop-cpf{padding:20px 16px;}',
    '.marina-pop-intro{margin:0 0 14px;padding:12px 14px;background:#fff4ea;border:1px solid #ffe2c7;border-radius:14px;border-top-left-radius:4px;font-size:0.9rem;line-height:1.5;color:#5a4636;}',
    '.marina-pop-intro strong{color:#d35400;}',
    '.marina-pop-intro.is-typing::after{content:"";display:inline-block;width:2px;height:1em;background:#d35400;margin-left:2px;vertical-align:-2px;animation:marinaCaret 0.7s steps(1) infinite;}',
    '@keyframes marinaCaret{50%{opacity:0;}}',
    '.marina-pop-cpf label{display:block;font-size:0.9rem;color:#3a3a44;margin-bottom:10px;font-weight:600;}',
    '.marina-pop-cpf-row{display:flex;gap:8px;flex-wrap:wrap;}',
    '.marina-pop-cpf-row input{flex:1;min-width:150px;padding:12px 14px;border-radius:10px;border:1px solid #d9d9e0;background:#fff;color:#1a1a2e;font-size:1rem;font-family:inherit;}',
    '.marina-cpf-err{border-color:#e63946 !important;}',
    '.marina-pop-cpf-row button,.marina-pop-input button{border:none;cursor:pointer;font-family:inherit;}',
    '.marina-pop-cpf-row button{padding:12px 16px;border-radius:10px;background:linear-gradient(135deg,#ff7a05,#ff5a1f);color:#fff;font-weight:700;display:inline-flex;align-items:center;gap:6px;white-space:nowrap;}',
    '.marina-pop-note{font-size:0.76rem;color:#8a8a93;margin-top:10px;}',
    '.marina-pop-note a{color:#ff7a05;}',
    '.marina-pop-body{flex:1;padding:16px;overflow-y:auto;display:flex;flex-direction:column;gap:10px;background:#f6f6f9;}',
    '.marina-bubble{max-width:84%;padding:10px 14px;border-radius:14px;font-size:0.9rem;line-height:1.45;word-wrap:break-word;}',
    '.marina-bubble-bot{align-self:flex-start;background:#fff;color:#2a2a34;border:1px solid #ececf1;border-bottom-left-radius:4px;}',
    '.marina-bubble-user{align-self:flex-end;background:linear-gradient(135deg,#ff7a05,#ff5a1f);color:#fff;border-bottom-right-radius:4px;}',
    '.marina-md-table{border-collapse:collapse;margin:8px 0;font-size:0.8rem;width:100%;}',
    '.marina-md-table th,.marina-md-table td{border:1px solid #e0e0e6;padding:5px 9px;text-align:left;}',
    '.marina-md-table th{background:#f0f0f4;font-weight:700;}',
    '.marina-typing{display:flex;gap:4px;align-items:center;}',
    '.marina-typing span{width:7px;height:7px;border-radius:50%;background:#bbb;animation:marinaBlink 1.2s infinite both;}',
    '.marina-typing span:nth-child(2){animation-delay:.2s;}',
    '.marina-typing span:nth-child(3){animation-delay:.4s;}',
    '@keyframes marinaBlink{0%,80%,100%{opacity:.25}40%{opacity:1}}',
    '.marina-boleto{align-self:stretch;background:#fff;color:#1a1a2e;border:1px solid #ececf1;border-radius:14px;padding:14px;}',
    '.marina-boleto-top{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:8px;}',
    '.marina-boleto-status{font-size:0.7rem;text-transform:uppercase;background:rgba(255,122,5,0.15);color:#c2410c;padding:3px 8px;border-radius:8px;font-weight:700;white-space:nowrap;}',
    '.marina-boleto-meta{display:flex;justify-content:space-between;align-items:center;font-size:0.85rem;color:#555;margin-bottom:10px;gap:8px;}',
    '.marina-boleto-val{font-size:1.2rem;font-weight:800;color:#1a1a2e;}',
    '.marina-boleto-qr{display:block;width:150px;height:150px;margin:0 auto 12px;border-radius:8px;background:#fff;}',
    '.marina-boleto-actions{display:flex;flex-direction:column;gap:8px;}',
    '.marina-boleto-btn{display:inline-flex;align-items:center;justify-content:center;gap:7px;padding:11px 14px;border-radius:10px;border:1px solid rgba(0,0,0,0.12);background:#f4f4f6;color:#1a1a2e;font-weight:600;font-size:0.85rem;text-decoration:none;cursor:pointer;}',
    '.marina-boleto-btn:hover{background:#fff3e8;border-color:#ffbe8a;}',
    '.marina-pop-input{display:flex;gap:8px;padding:12px 14px;border-top:1px solid #ececf1;background:#fff;}',
    '.marina-pop-input input{flex:1;padding:11px 14px;border-radius:10px;border:1px solid #d9d9e0;background:#fff;color:#1a1a2e;font-size:0.95rem;font-family:inherit;}',
    '.marina-pop-input button{width:46px;border-radius:10px;background:linear-gradient(135deg,#ff7a05,#ff5a1f);color:#fff;font-size:1.1rem;flex-shrink:0;}',
    '@media (max-width:480px){.marina-pop{bottom:0;right:0;left:0;width:100%;max-width:100%;height:100dvh;max-height:100dvh;border-radius:0;}}'
  ].join('');
  document.head.appendChild(style);

  // ───────────────────────── DOM do painel ─────────────────────────
  var pop = document.createElement('div');
  pop.className = 'marina-pop';
  pop.setAttribute('hidden', '');
  pop.setAttribute('role', 'dialog');
  pop.setAttribute('aria-label', 'Atendimento de boletos com a Marina');
  pop.innerHTML =
    '<div class="marina-pop-head">' +
      '<span class="marina-pop-avatar"><i class="ph-fill ph-headset"></i></span>' +
      '<div class="marina-pop-id"><strong>Marina</strong>' +
        '<span class="marina-pop-status"><span class="marina-pop-dot"></span> Atendimento online</span></div>' +
      '<button type="button" class="marina-pop-reset" aria-label="Nova consulta (trocar CPF)" title="Nova consulta — trocar CPF"><i class="ph ph-arrow-counter-clockwise"></i> Nova consulta</button>' +
      '<button type="button" class="marina-pop-close" aria-label="Fechar"><i class="ph ph-x"></i></button>' +
    '</div>' +
    '<div class="marina-pop-cpf">' +
      '<p class="marina-pop-intro">Oi! 👋 Sou a <strong>Marina</strong>. Precisa da <strong>2ª via do seu boleto</strong>? Eu pego aqui mesmo, na hora — código de barras, Pix ou PDF.</p>' +
      '<label>Pra começar, é só me passar seu CPF:</label>' +
      '<div class="marina-pop-cpf-row">' +
        '<input type="tel" inputmode="numeric" placeholder="000.000.000-00" maxlength="14" autocomplete="off" class="marina-cpf-input">' +
        '<button type="button" class="marina-cpf-btn">Continuar <i class="ph ph-arrow-right"></i></button>' +
      '</div>' +
      '<p class="marina-pop-note">Usamos seu CPF so pra localizar suas faturas. <a href="https://wa.me/5547989212991" target="_blank">Prefere o WhatsApp?</a></p>' +
    '</div>' +
    '<div class="marina-pop-body" hidden></div>' +
    '<div class="marina-pop-input" hidden>' +
      '<input type="text" placeholder="Escreva sua mensagem..." autocomplete="off" class="marina-msg-input">' +
      '<button type="button" class="marina-send-btn" aria-label="Enviar"><i class="ph-fill ph-paper-plane-right"></i></button>' +
    '</div>';
  document.body.appendChild(pop);

  var elClose    = pop.querySelector('.marina-pop-close');
  var elReset    = pop.querySelector('.marina-pop-reset');
  var elCpfStep  = pop.querySelector('.marina-pop-cpf');
  var elCpfInput = pop.querySelector('.marina-cpf-input');
  var elCpfBtn   = pop.querySelector('.marina-cpf-btn');
  var elBody     = pop.querySelector('.marina-pop-body');
  var elInputRow = pop.querySelector('.marina-pop-input');
  var elMsg      = pop.querySelector('.marina-msg-input');
  var elSend     = pop.querySelector('.marina-send-btn');
  var whatsapp   = document.querySelector('.whatsapp-float');

  var sid = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : ('s' + Date.now() + Math.floor(Math.random() * 1e6));
  var cpf = '', busy = false, started = false, opened = false, gen = 0;

  // Atendimento ligado/desligado no admin: se desabilitado, esconde o botao.
  fetch(PROXY_URL, { method: 'GET' })
    .then(function (r) { return r.json(); })
    .then(function (s) { if (s && s.enabled === false) launcher.style.display = 'none'; })
    .catch(function () {});

  // ───────────────────────── abrir / fechar ─────────────────────────
  function openPop() {
    pop.hidden = false;
    void pop.offsetWidth; // força reflow p/ a transicao rodar
    pop.classList.add('is-open');
    opened = true;
    launcher.style.display = 'none';
    if (whatsapp) whatsapp.style.display = 'none';
    setTimeout(function () { (started ? elMsg : elCpfInput).focus(); }, 60);
    if (!started) setTimeout(typeIntro, 280);
  }
  function closePop() {
    pop.classList.remove('is-open');
    opened = false;
    launcher.style.display = '';
    if (whatsapp) whatsapp.style.display = '';
    setTimeout(function () { if (!opened) pop.hidden = true; }, 240);
  }
  launcher.addEventListener('click', function (e) { e.preventDefault(); openPop(); });
  elClose.addEventListener('click', closePop);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && opened) closePop(); });

  // Nova consulta: zera sessao + chat + CPF (UX p/ consultar varios CPFs).
  // gen++ invalida qualquer resposta em voo, pra nao misturar conversa antiga.
  function resetConversation() {
    gen++;
    sid = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : ('s' + Date.now() + Math.floor(Math.random() * 1e6));
    cpf = ''; busy = false; started = false;
    elBody.innerHTML = ''; elBody.hidden = true;
    elInputRow.hidden = true;
    elReset.classList.remove('is-visible');
    elCpfStep.hidden = false;
    elCpfInput.value = ''; elCpfInput.classList.remove('marina-cpf-err');
    elSend.disabled = false;
    elCpfInput.focus();
  }
  elReset.addEventListener('click', resetConversation);

  // Digita a saudacao da Marina como se ela estivesse escrevendo (uma vez por carregamento).
  // Deriva os segmentos do proprio HTML do balao, entao mantem os <strong> e o fallback estatico.
  var introDone = false;
  function typeIntro() {
    if (introDone) return;
    var el = pop.querySelector('.marina-pop-intro');
    if (!el) return;
    introDone = true;
    if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var chars = [];
    [].forEach.call(el.childNodes, function (n) {
      var bold = (n.nodeType === 1 && n.tagName === 'STRONG') ? 1 : 0;
      Array.from(n.textContent || '').forEach(function (c) { chars.push([c, bold]); });
    });
    el.textContent = '';
    el.classList.add('is-typing');
    var i = 0, html = '', openB = false;
    function esc2(c) { return c.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
    var t = setInterval(function () {
      if (i >= chars.length) {
        if (openB) html += '</strong>';
        el.innerHTML = html;
        el.classList.remove('is-typing');
        clearInterval(t);
        return;
      }
      var ch = chars[i][0], bold = chars[i][1];
      if (bold && !openB) { html += '<strong>'; openB = true; }
      else if (!bold && openB) { html += '</strong>'; openB = false; }
      html += esc2(ch);
      el.innerHTML = html + (openB ? '</strong>' : '');
      i++;
    }, 22);
  }

  // ───────────────────────── chat (mesma logica da pagina /ajuda/boletos) ─────────────────────────
  function maskCpf(v) {
    v = v.replace(/\D/g, '').slice(0, 11);
    if (v.length > 9) return v.replace(/(\d{3})(\d{3})(\d{3})(\d{1,2})/, '$1.$2.$3-$4');
    if (v.length > 6) return v.replace(/(\d{3})(\d{3})(\d{1,3})/, '$1.$2.$3');
    if (v.length > 3) return v.replace(/(\d{3})(\d{1,3})/, '$1.$2');
    return v;
  }
  elCpfInput.addEventListener('input', function () { elCpfInput.classList.remove('marina-cpf-err'); elCpfInput.value = maskCpf(elCpfInput.value); });

  function esc(s) { var d = document.createElement('div'); d.textContent = (s == null ? '' : String(s)); return d.innerHTML; }
  // Markdown leve (a Marina responde com **negrito** e tabelas | | |). Escapa antes (XSS-safe).
  function mdRender(raw) {
    var lines = String(raw == null ? '' : raw).split('\n'), html = '', i = 0;
    function inl(s) {
      s = esc(s).replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
      // [texto](url) -> link; depois URLs cruas. So http/https (evita javascript: etc).
      s = s.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, function (m, t, u) { return '<a href="' + u + '" target="_blank" rel="noopener noreferrer">' + t + '</a>'; });
      s = s.replace(/(^|\s)(https?:\/\/[^\s<]+)/g, function (m, pre, u) { return pre + '<a href="' + u + '" target="_blank" rel="noopener noreferrer">' + u + '</a>'; });
      return s;
    }
    function cells(l) { return l.trim().replace(/^\||\|$/g, '').split('|').map(function (c) { return c.trim(); }); }
    while (i < lines.length) {
      if (/^\s*\|.*\|\s*$/.test(lines[i]) && i + 1 < lines.length && /^\s*\|[\s:|-]+\|\s*$/.test(lines[i + 1])) {
        var head = cells(lines[i]); i += 2; var rows = '';
        while (i < lines.length && /^\s*\|.*\|\s*$/.test(lines[i])) { var r = cells(lines[i]); rows += '<tr>' + r.map(function (c) { return '<td>' + inl(c) + '</td>'; }).join('') + '</tr>'; i++; }
        html += '<table class="marina-md-table"><thead><tr>' + head.map(function (h) { return '<th>' + inl(h) + '</th>'; }).join('') + '</tr></thead><tbody>' + rows + '</tbody></table>';
      } else { html += inl(lines[i]) + '<br>'; i++; }
    }
    return html.replace(/(<br>\s*)+$/, '');
  }
  function scrollDown() { elBody.scrollTop = elBody.scrollHeight; }
  function addBubble(text, who) {
    var b = document.createElement('div');
    b.className = 'marina-bubble marina-bubble-' + who;
    b.innerHTML = mdRender(text);
    elBody.appendChild(b); scrollDown(); return b;
  }
  function addTyping() {
    var t = document.createElement('div');
    t.className = 'marina-bubble marina-bubble-bot marina-typing';
    t.innerHTML = '<span></span><span></span><span></span>';
    elBody.appendChild(t); scrollDown(); return t;
  }
  function fmtDate(d) { var m = /^(\d{4})-(\d{2})-(\d{2})/.exec(d || ''); return m ? (m[3] + '/' + m[2] + '/' + m[1]) : (d || ''); }
  function fmtMoney(v) {
    if (v == null || v === '') return '';
    var n = Number(String(v).replace(',', '.'));
    return isNaN(n) ? esc(v) : ('R$ ' + n.toFixed(2).replace('.', ','));
  }
  function copyBtn(label, text) { return text ? '<button type="button" class="marina-boleto-btn" data-copy="' + esc(text) + '">' + label + '</button>' : ''; }
  function renderBoleto(b) {
    if (!b) return;
    var card = document.createElement('div');
    card.className = 'marina-boleto';
    var linha = b.linha_digitavel || b.codigo_barras || '';
    var html = '<div class="marina-boleto-top"><strong>' + esc(b.descricao || 'Fatura') + '</strong>' + (b.status ? '<span class="marina-boleto-status">' + esc(b.status) + '</span>' : '') + '</div>';
    html += '<div class="marina-boleto-meta">';
    if (b.vencimento) html += '<span><i class="ph ph-calendar-blank"></i> Vence ' + esc(fmtDate(b.vencimento)) + '</span>';
    if (b.valor != null && b.valor !== '') html += '<span class="marina-boleto-val">' + fmtMoney(b.valor) + '</span>';
    html += '</div>';
    if (b.pix_qrcode_png_base64) html += '<img class="marina-boleto-qr" alt="QR Code PIX" src="data:image/png;base64,' + esc(b.pix_qrcode_png_base64) + '">';
    html += '<div class="marina-boleto-actions">';
    html += copyBtn('<i class="ph ph-barcode"></i> Copiar linha digitavel', linha);
    html += copyBtn('<i class="ph ph-qr-code"></i> Copiar codigo PIX', b.pix_copia_cola);
    if (b.url_pdf) html += '<a class="marina-boleto-btn" href="' + esc(b.url_pdf) + '" target="_blank"><i class="ph ph-file-pdf"></i> Baixar PDF</a>';
    html += '</div>';
    card.innerHTML = html;
    elBody.appendChild(card); scrollDown();
  }
  elBody.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-copy]');
    if (!btn) return;
    navigator.clipboard.writeText(btn.getAttribute('data-copy')).then(function () {
      var old = btn.innerHTML; btn.innerHTML = '<i class="ph ph-check"></i> Copiado!';
      setTimeout(function () { btn.innerHTML = old; }, 1800);
    }).catch(function () {});
  });

  function send(text) {
    if (busy) return;
    busy = true; elSend.disabled = true;
    var myGen = gen;
    addBubble(text, 'user');
    var typing = addTyping();
    fetch(PROXY_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ cpf: cpf, message: text, session_id: sid })
    })
      .then(function (r) { return r.json().catch(function () { return { reply: 'Recebi uma resposta inesperada. Tenta de novo ou chama no WhatsApp.' }; }); })
      .then(function (d) {
        if (myGen !== gen) return;       // resetou no meio: descarta resposta antiga
        typing.remove();
        if (d && d.session_id) sid = d.session_id;
        addBubble((d && d.reply) ? d.reply : 'Nao recebi resposta. Tenta de novo ou chama no WhatsApp.', 'bot');
        if (d && Array.isArray(d.boletos)) d.boletos.forEach(renderBoleto);
      })
      .catch(function () {
        if (myGen !== gen) return;
        typing.remove();
        addBubble('Falha de conexao. Tenta de novo ou fala com a gente no WhatsApp.', 'bot');
      })
      .finally(function () { if (myGen === gen) { busy = false; elSend.disabled = false; elMsg.focus(); } });
  }

  function start() {
    var digits = elCpfInput.value.replace(/\D/g, '');
    if (digits.length !== 11) { elCpfInput.classList.add('marina-cpf-err'); elCpfInput.focus(); return; }
    cpf = digits; started = true;
    elReset.classList.add('is-visible');
    elCpfStep.hidden = true; elBody.hidden = false; elInputRow.hidden = false;
    addBubble('Perfeito! Já tô localizando suas faturas pelo seu CPF... 🔎', 'bot');
    send('quero meu boleto');
  }
  elCpfBtn.addEventListener('click', start);
  elCpfInput.addEventListener('keydown', function (e) { if (e.key === 'Enter') start(); });
  elSend.addEventListener('click', function () { var t = elMsg.value.trim(); if (t) { elMsg.value = ''; send(t); } });
  elMsg.addEventListener('keydown', function (e) { if (e.key === 'Enter') { var t = elMsg.value.trim(); if (t) { elMsg.value = ''; send(t); } } });
})();
