<?php
/**
 * Landing page de campanha — GET /promo/<slug>/  (rewrite no .htaccess → /promo/index.php?c=<slug>)
 *
 * O conteúdo vem de secrets/bitrix-mapping.json → forms[<slug>].landing, editável no
 * admin (aba Bitrix). O lead vai pro Bitrix via api/form-submit.php usando o MESMO slug.
 *
 * POR QUE PHP (e não HTML + fetch): o og:title/og:image é o preview do link no
 * Instagram/WhatsApp, e o crawler dessas plataformas NÃO roda JS. Renderizado no
 * servidor, o preview sai certo e o link publica na hora que salva no admin.
 *
 * Molde visual copiado de copa/index.html (auto-contido: CSS inline, só tracking.js
 * + cookie-consent.js). Difere da copa de propósito em 3 pontos:
 *   - sem envio ao Google Sheets (só Bitrix) → sem o setTimeout de 2,5s que segura o redirect
 *   - com honeypot _hp (o form-submit.php já trata, a copa não manda)
 *   - com miTrack('generate_lead') (a copa não reporta conversão nenhuma aos pixels)
 */
define('MASTERINFO_INTERNAL', true);
require_once __DIR__ . '/../security-headers.php';
require_once __DIR__ . '/../api/admin/_bitrix-helper.php'; // já carrega secrets/config.php

sendSecurityHeaders();

// Mesmo filtro de slug do form-submit.php:56 — o que passa aqui tem que passar lá.
$slug = preg_replace('/[^a-z0-9-_]/i', '', (string) ($_GET['c'] ?? ''));
$form = $slug !== '' ? (bx_load_mapping()['forms'][$slug] ?? null) : null;
$L    = is_array($form['landing'] ?? null) ? $form['landing'] : null;

// Slug inexistente, formulário sem landing, ou campanha despublicada → 404 do site.
if (!$L || empty($L['ativa'])) {
    http_response_code(404);
    header('Cache-Control: no-store');
    $notFound = __DIR__ . '/../404.html';
    if (is_readable($notFound)) readfile($notFound);
    exit;
}

// Oferta muda no meio da campanha; 5 min evita servir preço velho por muito tempo.
header('Cache-Control: public, max-age=300');

/** Todo texto abaixo é editável no admin → nunca sai cru no HTML. */
function promo_e($s): string { return htmlspecialchars((string) $s, ENT_QUOTES, 'UTF-8'); }
/** Valor pra dentro de <script>: json_encode fecha </script> e aspas. */
function promo_js($v): string {
    return json_encode($v, JSON_UNESCAPED_UNICODE | JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT);
}
function promo_val(array $L, string $k, string $fallback = ''): string {
    $v = trim((string) ($L[$k] ?? ''));
    return $v !== '' ? $v : $fallback;
}

$titulo    = promo_val($L, 'titulo', (string) ($form['label'] ?? 'Oferta MasterInfo'));
$badge     = promo_val($L, 'badge');
$subtitulo = promo_val($L, 'subtitulo');
$velocidade= promo_val($L, 'velocidade');
$preco     = promo_val($L, 'preco');
$precoDet  = promo_val($L, 'precoDetalhe');
$cta       = promo_val($L, 'cta', 'Quero contratar');
$letraMiuda= promo_val($L, 'letraMiuda');
$planoNome = promo_val($L, 'planoNome', $titulo);
$ogTitulo  = promo_val($L, 'ogTitulo', $titulo);
$ogDesc    = promo_val($L, 'ogDescricao', $subtitulo);
$ogImagem  = promo_val($L, 'ogImagem');
$waMsg     = promo_val($L, 'whatsappMsg', 'Olá! Quero a oferta: ' . $planoNome);

// R$ 89,90 → "89" grande + "90" sobrescrito (mesmo tratamento visual da copa).
$precoNum = $preco;
$precoCents = '';
if (strpos($preco, ',') !== false) [$precoNum, $precoCents] = explode(',', $preco, 2);
$precoValor = (float) str_replace(',', '.', preg_replace('/[^\d,.]/', '', $preco)); // p/ o pixel

// URL absoluta pro og:url/og:image/canonical — é o que o crawler do Instagram/WhatsApp
// busca, então precisa ser o domínio público, sempre.
//   - NÃO usa HTTP_HOST cru: o cliente controla esse header (og:image apontando pra fora).
//   - NÃO usa ALLOWED_ORIGIN: aquilo é config de CORS e em PRODUÇÃO está valendo
//     'http://localhost:8091' (constatado 16/07/2026) — o preview sairia apontando pro
//     localhost de quem abrisse o link. Host canônico fica fixo aqui.
// non-www porque o site canoniza assim (.htaccess:37-41); og:image em www tomaria 301
// e há scraper de preview que não segue redirect de imagem.
define('PROMO_HOST_CANONICO', 'https://masterinfointernet.com');
$host    = (string) ($_SERVER['HTTP_HOST'] ?? '');
$ehLocal = (bool) preg_match('/^(localhost|127\.0\.0\.1|\[::1\])(:\d+)?$/i', $host);
$base    = $ehLocal ? 'http://' . $host : PROMO_HOST_CANONICO; // dev vê preview local
$pageUrl = $base . '/promo/' . $slug . '/';

// WhatsApp comercial (vendas) — do config.json, não chumbado como na copa.
$whatsapp = '5547989212991';
$cfgPath  = __DIR__ . '/../config.json';
if (is_readable($cfgPath)) {
    $j = json_decode((string) file_get_contents($cfgPath), true);
    $n = preg_replace('/\D+/', '', (string) ($j['empresa']['whatsapp'] ?? ''));
    if ($n !== '') $whatsapp = $n;
}
?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script>window.miCfg=window.miCfg||function(){return window.__miCfgP||(window.__miCfgP=fetch('/config.json?v='+Date.now()).then(function(r){return r.json();}));};</script>
  <title><?= promo_e($titulo) ?> | MasterInfo Internet</title>
  <meta name="description" content="<?= promo_e($ogDesc) ?>">
  <link rel="canonical" href="<?= promo_e($pageUrl) ?>">
  <!-- Campanha paga: não queremos a LP competindo com o site no orgânico. -->
  <meta name="robots" content="noindex, follow">

  <!-- Preview do link no Instagram/WhatsApp — precisa estar no HTML (crawler não roda JS). -->
  <meta property="og:title" content="<?= promo_e($ogTitulo) ?>">
  <meta property="og:description" content="<?= promo_e($ogDesc) ?>">
  <meta property="og:url" content="<?= promo_e($pageUrl) ?>">
  <meta property="og:type" content="website">
<?php if ($ogImagem !== ''): ?>
  <meta property="og:image" content="<?= promo_e($base . $ogImagem) ?>">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="<?= promo_e($base . $ogImagem) ?>">
<?php endif; ?>
  <meta name="twitter:title" content="<?= promo_e($ogTitulo) ?>">
  <meta name="twitter:description" content="<?= promo_e($ogDesc) ?>">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
  <noscript><link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet"></noscript>
  <link rel="stylesheet" href="/vendor/phosphor/phosphor.css?v=20260619" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="/vendor/phosphor/phosphor.css?v=20260619"></noscript>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

  <style>
    :root {
      --orange: #ff7a05;
      --yellow: #fcc305;
      --red: #e63946;
      --dark: #0f0f14;
      --fire: linear-gradient(135deg, #ff7a05, #fcc305);
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      font-family: 'Outfit', sans-serif;
      background: var(--dark);
      color: #fff;
      line-height: 1.5;
      overflow-x: hidden;
    }
    .wrap { max-width: 560px; margin: 0 auto; padding: 0 20px; }
    .page {
      position: relative;
      min-height: 100vh;
      isolation: isolate;
      padding: 32px 0 60px;
    }
    .page::before {
      content: '';
      position: absolute;
      inset: 0;
      background:
        radial-gradient(circle at 50% 0%, rgba(255,122,5,0.35) 0%, transparent 55%),
        radial-gradient(circle at 80% 90%, rgba(230,57,70,0.25) 0%, transparent 50%),
        linear-gradient(180deg, #1a0d05 0%, #0f0f14 100%);
      z-index: -1;
    }
    .topo { text-align: center; margin-bottom: 26px; }
    .topo img { height: 38px; width: auto; }
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 18px;
      background: rgba(255,122,5,0.15);
      border: 1px solid rgba(255,122,5,0.5);
      border-radius: 999px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.12em;
      color: #ff9a3c;
      text-transform: uppercase;
    }
    .badge i { font-size: 0.9rem; }
    .center { text-align: center; }
    h1 {
      font-size: clamp(1.9rem, 7vw, 2.7rem);
      font-weight: 900;
      letter-spacing: -0.03em;
      line-height: 1.08;
      margin: 18px 0 14px;
    }
    .lead {
      font-size: 1.05rem;
      color: rgba(255,255,255,0.78);
      margin-bottom: 28px;
    }
    .preco-card {
      background: linear-gradient(160deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
      border: 1px solid rgba(255,122,5,0.35);
      border-radius: 22px;
      padding: 28px 24px;
      text-align: center;
      margin-bottom: 28px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.4);
    }
    .preco-card .speed {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.85rem;
      letter-spacing: 0.1em;
      color: var(--yellow);
      font-weight: 700;
      text-transform: uppercase;
    }
    .preco-main {
      display: flex;
      align-items: baseline;
      justify-content: center;
      gap: 4px;
      margin: 8px 0 2px;
    }
    .preco-cur { font-size: 1.4rem; font-weight: 700; color: #fff; }
    .preco-num {
      font-size: clamp(3.4rem, 16vw, 4.6rem);
      font-weight: 900;
      letter-spacing: -0.04em;
      background: var(--fire);
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
      line-height: 1;
    }
    .preco-cents { font-size: 1.4rem; font-weight: 800; color: #fff; align-self: flex-start; margin-top: 8px; }
    .preco-cond {
      font-size: 0.95rem;
      color: rgba(255,255,255,0.8);
      font-weight: 600;
    }
    .form-card {
      background: #fff;
      color: #1a1a1a;
      border-radius: 22px;
      padding: 28px 24px;
      box-shadow: 0 24px 60px rgba(0,0,0,0.5);
    }
    .form-card h2 {
      font-size: 1.35rem;
      font-weight: 900;
      letter-spacing: -0.02em;
      margin-bottom: 4px;
    }
    .form-card .sub {
      font-size: 0.92rem;
      color: #666;
      margin-bottom: 22px;
    }
    .field { margin-bottom: 16px; }
    .field label {
      display: block;
      font-size: 0.82rem;
      font-weight: 700;
      color: #444;
      margin-bottom: 6px;
    }
    .field input {
      width: 100%;
      padding: 14px 16px;
      font-size: 1rem;
      font-family: inherit;
      border: 2px solid #e5e1d8;
      border-radius: 12px;
      background: #faf8f4;
      transition: border-color 0.2s, background 0.2s;
    }
    .field input:focus { outline: none; border-color: var(--orange); background: #fff; }
    .field input::placeholder { color: #aaa; }
    /* Honeypot: invisível pro humano, preenchido por bot. Fora da viewport (não display:none,
       que alguns bots detectam). O form-submit.php descarta o envio se vier preenchido. */
    .hp { position: absolute; left: -9999px; width: 1px; height: 1px; overflow: hidden; }
    .submit-btn {
      width: 100%;
      padding: 17px;
      font-size: 1.08rem;
      font-weight: 800;
      font-family: inherit;
      color: #fff;
      background: var(--fire);
      border: none;
      border-radius: 999px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 12px 28px rgba(255,122,5,0.4);
      transition: transform 0.15s, box-shadow 0.15s;
      margin-top: 6px;
    }
    .submit-btn:hover { transform: translateY(-2px); box-shadow: 0 16px 34px rgba(255,122,5,0.5); }
    .submit-btn:active { transform: translateY(0); }
    .submit-btn:disabled { opacity: 0.7; cursor: default; transform: none; }
    .form-trust {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      margin-top: 14px;
      font-size: 0.78rem;
      color: #888;
    }
    .form-trust i { color: #25d366; font-size: 1rem; }
    .fine {
      text-align: center;
      font-size: 0.72rem;
      color: rgba(255,255,255,0.45);
      margin-top: 20px;
      font-style: italic;
      line-height: 1.5;
    }
    .proof {
      display: flex;
      justify-content: center;
      gap: 22px;
      margin: 30px 0 0;
      flex-wrap: wrap;
    }
    .proof-item { text-align: center; font-size: 0.8rem; color: rgba(255,255,255,0.7); }
    .proof-item strong { display: block; font-size: 1.1rem; color: #fff; font-weight: 800; }
    .proof-item i { color: var(--yellow); }
  </style>
</head>
<body>
  <div class="page">
    <div class="wrap">

      <div class="topo">
        <a href="/"><img src="/imgs/logo-masterinfo.png" alt="MasterInfo Internet" width="140" height="38"></a>
      </div>

      <div class="center">
<?php if ($badge !== ''): ?>
        <span class="badge"><i class="ph-fill ph-fire"></i> <?= promo_e($badge) ?></span>
<?php endif; ?>
        <h1><?= promo_e($titulo) ?></h1>
<?php if ($subtitulo !== ''): ?>
        <p class="lead"><?= promo_e($subtitulo) ?></p>
<?php endif; ?>
      </div>

<?php if ($preco !== ''): ?>
      <div class="preco-card">
<?php if ($velocidade !== ''): ?>
        <div class="speed"><?= promo_e($velocidade) ?></div>
<?php endif; ?>
        <div class="preco-main">
          <span class="preco-cur">R$</span>
          <span class="preco-num"><?= promo_e($precoNum) ?></span>
<?php if ($precoCents !== ''): ?>
          <span class="preco-cents"><?= promo_e($precoCents) ?></span>
<?php endif; ?>
        </div>
<?php if ($precoDet !== ''): ?>
        <div class="preco-cond"><?= promo_e($precoDet) ?></div>
<?php endif; ?>
      </div>
<?php endif; ?>

      <form class="form-card" id="leadForm">
        <h2>Garanta sua vaga</h2>
        <p class="sub">Preencha e fale com a gente no WhatsApp pra fechar.</p>

        <div class="field">
          <label for="nome">Seu nome</label>
          <input type="text" id="nome" name="nome" placeholder="Nome completo" required autocomplete="name">
        </div>
        <div class="field">
          <label for="bairro">Seu bairro</label>
          <input type="text" id="bairro" name="bairro" placeholder="Ex: Comasa, Boa Vista, Aventureiro..." required>
        </div>
        <div class="field">
          <label for="telefone">Seu WhatsApp</label>
          <input type="tel" id="telefone" name="telefone" placeholder="(47) 9____-____" required inputmode="numeric" autocomplete="tel">
        </div>

        <div class="hp" aria-hidden="true">
          <label for="_hp">Não preencha este campo</label>
          <input type="text" id="_hp" name="_hp" tabindex="-1" autocomplete="off">
        </div>

        <button type="submit" class="submit-btn">
          <?= promo_e($cta) ?> <i class="ph-bold ph-arrow-right"></i>
        </button>

        <div class="form-trust">
          <i class="ph-fill ph-whatsapp-logo"></i> Você vai falar direto com nosso time
        </div>
      </form>

      <div class="proof">
        <div class="proof-item"><strong><i class="ph-fill ph-star"></i> 4,8</strong> 2.450 avaliações</div>
        <div class="proof-item"><strong>100%</strong> Fibra Óptica</div>
        <div class="proof-item"><strong>100%</strong> Joinville</div>
      </div>

<?php if ($letraMiuda !== ''): ?>
      <p class="fine"><?= promo_e($letraMiuda) ?></p>
<?php endif; ?>

    </div>
  </div>

  <script>
  (function() {
    var SLUG     = <?= promo_js($slug) ?>;
    var PLANO    = <?= promo_js($planoNome) ?>;
    var VALOR    = <?= promo_js($precoValor) ?>;
    var WA       = <?= promo_js($whatsapp) ?>;
    var WA_MSG   = <?= promo_js($waMsg) ?>;

    var form = document.getElementById('leadForm');
    var tel  = document.getElementById('telefone');
    var hp   = document.getElementById('_hp');
    var btn  = form.querySelector('.submit-btn');

    // Máscara (47) 9XXXX-XXXX
    tel.addEventListener('input', function() {
      var v = tel.value.replace(/\D/g, '').slice(0, 11);
      var out = '';
      if (v.length > 0) out = '(' + v.slice(0, 2);
      if (v.length >= 2) out += ') ' + v.slice(2, 7);
      if (v.length >= 7) out += '-' + v.slice(7, 11);
      tel.value = out;
    });

    function irParaWhatsApp(nome, bairro, telefone) {
      var msg = WA_MSG + '\n\n' +
        'Nome: ' + nome + '\n' +
        'Bairro: ' + bairro + '\n' +
        'WhatsApp: ' + telefone;
      window.location.href = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(msg);
    }

    form.addEventListener('submit', function(e) {
      e.preventDefault();
      var nome = document.getElementById('nome').value.trim();
      var bairro = document.getElementById('bairro').value.trim();
      var telefone = tel.value.trim();
      if (!nome || !bairro || !telefone) return;

      btn.disabled = true;
      btn.innerHTML = 'Enviando... <i class="ph-bold ph-spinner"></i>';

      var att = (typeof window.miAttribution === 'function') ? window.miAttribution() : {};
      var dados = {
        nome: nome,
        bairro: bairro,
        telefone: telefone,
        plano: PLANO,
        origem: SLUG,
        _hp: hp ? hp.value : '',
        jornada: (typeof window.miJourneyText === 'function' ? window.miJourneyText() : ''),
        gclid: att.gclid || '', fbclid: att.fbclid || '', fbp: att.fbp || '', fbc: att.fbc || ''
      };

      // Conversão pros pixels (GA4/Ads/Meta) ANTES do redirect — a página é abandonada
      // logo em seguida. A /copa/ não faz isso e por isso não reporta lead nenhum.
      try {
        if (typeof window.miTrack === 'function') window.miTrack('generate_lead', { plan: PLANO, value: VALOR });
      } catch (err) {}

      // Grava no Bitrix e só então manda pro WhatsApp — sem o lead o resto não serve.
      // keepalive: a requisição sobrevive ao unload do redirect.
      var seguiu = false;
      function seguir() {
        if (seguiu) return;
        seguiu = true;
        irParaWhatsApp(nome, bairro, telefone);
      }

      try {
        fetch('/api/form-submit.php', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          keepalive: true,
          body: JSON.stringify({ form: SLUG, data: dados })
        }).then(seguir).catch(seguir);
      } catch (err) { seguir(); }

      // Rede lenta/offline: não prende o visitante no formulário.
      setTimeout(seguir, 4000);
    });
  })();
  </script>
  <script src="/tracking.js?v=20260627a" defer></script>
  <script src="/cookie-consent.js?v=20260603-cc"></script>
</body>
</html>
