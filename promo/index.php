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
$ofertaLbl = promo_val($L, 'ofertaLabel');
$ofertaVal = promo_val($L, 'ofertaValor');
$cta       = promo_val($L, 'cta', 'Quero contratar');
$letraMiuda= promo_val($L, 'letraMiuda');
$planoNome = promo_val($L, 'planoNome', $titulo);
$ogTitulo  = promo_val($L, 'ogTitulo', $titulo);
$ogDesc    = promo_val($L, 'ogDescricao', $subtitulo);
$ogImagem  = promo_val($L, 'ogImagem');
$appLogo   = promo_val($L, 'appLogo');
$appTexto  = promo_val($L, 'appTexto');
$tema      = promo_val($L, 'tema');
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
      /* Curvas fortes: as nativas do CSS são fracas demais e a animação some. */
      --ease-out: cubic-bezier(0.23, 1, 0.32, 1);
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
    /* Cor sólida, não gradiente com background-clip:text. Aquilo exige
       color:transparent — se o clip falhar em algum browser, o número mais
       importante da campanha simplesmente some da tela. Não vale o efeito. */
    .preco-num {
      font-size: clamp(3.4rem, 16vw, 4.6rem);
      font-weight: 900;
      letter-spacing: -0.04em;
      color: var(--yellow);
      line-height: 1;
    }
    .preco-cents { font-size: 1.4rem; font-weight: 800; color: #fff; align-self: flex-start; margin-top: 8px; }
    /* Pílula da oferta (2ª mensalidade etc.): é o gancho da promoção, então ganha
       destaque próprio — mas SEMPRE abaixo do preço cheio. O 159,90 continua sendo
       o número-herói de propósito: inverter viraria propaganda enganosa (o valor
       promocional vale só uma fatura). */
    .preco-oferta {
      display: inline-flex;
      align-items: baseline;
      gap: 8px;
      margin: 12px auto 4px;
      padding: 8px 20px;
      background: rgba(252,195,5,0.1);
      border: 1px solid rgba(252,195,5,0.5);
      border-radius: 999px;
    }
    .preco-oferta .lbl {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--yellow);
    }
    .preco-oferta .val {
      font-size: 1.45rem;
      font-weight: 900;
      letter-spacing: -0.02em;
      color: #fff;
      line-height: 1;
    }
    .preco-cond {
      font-size: 0.95rem;
      color: rgba(255,255,255,0.8);
      font-weight: 600;
    }
    /* Faixa do app incluso (Disney+ etc.): o logo faz o benefício ser reconhecido
       antes de ser lido — ninguém "lê" a Disney, a pessoa VÊ. */
    .preco-app {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      margin-top: 16px;
      padding-top: 16px;
      border-top: 1px solid rgba(255,255,255,0.1);
      font-size: 0.9rem;
      font-weight: 600;
      color: rgba(255,255,255,0.85);
    }
    .preco-app img {
      width: 34px;
      height: 34px;
      border-radius: 8px;
      flex-shrink: 0;
      background: #fff;
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
      transition: border-color 200ms ease, background 200ms ease;
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
      transition: transform 160ms var(--ease-out), box-shadow 160ms var(--ease-out);
      margin-top: 6px;
    }
    /* Hover só onde existe ponteiro de verdade: no touch o tap dispara :hover e o
       botão FICA preso no estado elevado depois do toque — e essa página é quase
       toda tráfego de celular vindo do Instagram. */
    @media (hover: hover) and (pointer: fine) {
      .submit-btn:hover { transform: translateY(-2px); box-shadow: 0 16px 34px rgba(255,122,5,0.5); }
    }
    /* Feedback de aperto: confirma que a interface ouviu o toque. */
    .submit-btn:active { transform: scale(0.97); }
    .submit-btn:disabled { opacity: 0.7; cursor: default; transform: none; }
    /* O Phosphor não gira sozinho. Sem isto o "Enviando…" mostra um ícone PARADO
       bem no momento em que o lead está sendo gravado — parece travado.
       Rápido (0.6s) de propósito: spinner veloz faz o envio parecer mais rápido. */
    @keyframes promo-spin { to { transform: rotate(360deg); } }
    .submit-btn .ph-spinner { display: inline-block; animation: promo-spin 0.6s linear infinite; }
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

    /* ── Desktop: duas colunas ──
       Empilhado, o desktop herdava o problema do celular só que pior: hero alto +
       card de 327px e o formulário caía fora da tela, com metade da largura vazia
       dos lados. Com o espaço horizontal que existe, a oferta fica à esquerda e o
       formulário à direita — os dois na primeira tela, sem rolagem e sem barra
       flutuante. Mobile continua no fluxo natural (a grade só liga em ≥900px). */
    @media (min-width: 900px) {
      .wrap { max-width: 1080px; }
      .page { padding: 40px 0 64px; }
      /* stretch, não start: as duas colunas assumem a altura da linha — é isso que
         dá o "chão" comum onde as bases dos dois cards se encontram. */
      .grade {
        display: grid;
        grid-template-columns: minmax(0, 1fr) 400px;
        gap: 56px;
        align-items: stretch;
      }
      .col-oferta, .col-acao { display: flex; flex-direction: column; }
      /* Centralizado é gesto de celular; em duas colunas o texto ancora à esquerda. */
      .center { text-align: left; margin-bottom: 28px; }
      h1 { font-size: clamp(2.1rem, 3.2vw, 3rem); margin-top: 20px; }
      .lead { margin-bottom: 0; }
      /* ── Bases dos dois cards alinhadas ──
         O card de preço DESCE até o fim da coluna (margin-top:auto — desloca, não
         deforma) e o formulário ESTICA até o mesmo fim (flex:1). Antes as bases
         eram acidente do conteúdo: em 1280 o card parava 46px ACIMA do form; em
         1920 o h1 quebra em 3 linhas (font-size tem 3.2vw), empurrava o card e ele
         passava 21px ABAIXO. Como o título é editável no admin, cada campanha caía
         num lugar — não existia valor de margem que resolvesse. */
      .preco-card { margin-top: auto; margin-bottom: 0; }
      .form-card { flex: 1; }
      .proof { justify-content: flex-start; }
      .fine { text-align: left; }
      /* (sticky removido do .col-acao: com as colunas em stretch o item já ocupa a
         linha inteira e não sobra folga pra deslizar — a regra não fazia nada.) */
      body { padding-bottom: 0; }
      /* (a barra fixa é desligada mais abaixo, depois da regra que a define —
         media query não muda especificidade, então ordem é o que decide) */
    }

    /* ── Barra de ação fixa (mobile) ──
       Medido em 390x844: o botão do formulário nasce em 1004px, 216px ABAIXO da
       dobra — e no celular real a barra do navegador come mais ~100px. O visitante
       via a oferta e não via como contratar. A barra põe o CTA sempre ao alcance
       do polegar; some sozinha quando o botão de verdade entra em cena, pra não
       existirem dois CTAs na mesma tela. */
    .cta-fixo {
      position: fixed;
      left: 0; right: 0; bottom: 0;
      /* Acompanha a coluna do conteúdo (560px) em vez de esticar na tela toda:
         no desktop uma barra full-width sob uma página estreita fica deslocada. */
      max-width: 560px;
      margin: 0 auto;
      z-index: 50;
      display: flex;
      align-items: center;
      gap: 14px;
      padding: 12px 16px calc(12px + env(safe-area-inset-bottom, 0px));
      background: rgba(10,12,22,0.82);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border-top: 1px solid rgba(255,255,255,0.1);
      transform: translateY(110%);
      transition: transform 220ms var(--ease-out);
    }
    .cta-fixo[data-visivel] { transform: translateY(0); }
    /* O preço só entra na barra quando o card de preço saiu de vista. Com o card
       na tela, repetir "R$ 159,90 · 2ª mensalidade R$ 79,95" logo abaixo dele é
       eco, não reforço: a barra existe pra dar o CTA que sumiu, não o preço que
       já está lá. Sem o preço, o botão toma a barra inteira. */
    .cta-fixo-preco {
      line-height: 1.15;
      flex-shrink: 0;
      overflow: hidden;
      max-width: 160px;
      opacity: 1;
      transition: max-width 220ms var(--ease-out), opacity 160ms var(--ease-out), margin 220ms var(--ease-out);
    }
    .cta-fixo[data-preco-oculto] .cta-fixo-preco {
      max-width: 0;
      opacity: 0;
      margin-left: -14px; /* absorve o gap do flex */
    }
    .cta-fixo-preco strong { display: block; font-size: 1.15rem; font-weight: 900; color: #fff; }
    .cta-fixo-preco strong span { font-size: 0.8rem; font-weight: 700; }
    .cta-fixo-preco small { font-size: 0.68rem; color: rgba(255,255,255,0.6); }
    .cta-fixo-btn {
      flex: 1;
      padding: 14px 18px;
      font-family: inherit;
      font-size: 0.98rem;
      font-weight: 800;
      color: #fff;
      background: var(--fire);
      border: none;
      border-radius: 999px;
      cursor: pointer;
      box-shadow: 0 8px 22px rgba(255,122,5,0.4);
      transition: transform 160ms var(--ease-out);
    }
    .cta-fixo-btn:active { transform: scale(0.97); }
    /* Reserva o espaço da barra: sem isto ela cobre a letra miúda no fim da página. */
    body { padding-bottom: 84px; }
    /* Desliga a barra no desktop. Precisa vir DEPOIS da regra acima: media query não
       altera especificidade, então quem estiver por último na cascata ganha — foi
       exatamente por isso que a barra apareceu flutuando no meio da tela grande.
       Critério é largura, não (pointer: fine): ponteiro cortaria laptop touch e
       deixaria o comportamento impossível de testar em navegador emulando celular. */
    @media (min-width: 900px) {
      .cta-fixo { display: none; }
    }

    /* Movimento reduzido = menos movimento, não nenhum: tira o deslocamento
       decorativo e mantém o spinner (é ele que diz que o envio está rolando). */
    @media (prefers-reduced-motion: reduce) {
      .cta-fixo { transition: none; }
      html { scroll-behavior: auto; }
      .submit-btn { transition: box-shadow 160ms ease; }
      .submit-btn:hover, .submit-btn:active { transform: none; }
      .submit-btn .ph-spinner { animation-duration: 1.2s; }
    }
  </style>
<?php if ($tema === 'disney'): ?>
  <style>
    /* ── Tema "noite Disney" (campo tema=disney no admin) ──
       Cores AMOSTRADAS da arte oficial Disney+ (Canva DAHPmr0pTHI), não
       inventadas: o gradiente da peça é diagonal 225deg com ciano #00bcc7 no
       canto superior direito caindo até petróleo #001530 no inferior esquerdo;
       fundo da peça #011622; texto-destaque #caecff.
       Antes o tema usava azul-royal (#0a1633/#0063e5/#5cd4ff) — família de cor
       errada: a arte é TEAL/petróleo, não azul.
       Só o ambiente muda: o CTA continua laranja MasterInfo de propósito —
       laranja sobre teal-noite é o contraste máximo (é o botão que converte) e
       mantém a marca da casa na página. */
    body { background: #001530; }
    .page::before {
      background:
        /* 'to bottom left', NÃO um ângulo fixo: na arte os cantos sup-esq
           (#003e4f) e inf-dir (#003547) têm quase a mesma cor — assinatura de
           gradiente canto-a-canto, onde esses dois caem no meio da linha. Com
           225deg fixo o canto inf-dir saía #005161 (claro demais). A keyword
           também se adapta sozinha a qualquer proporção de tela.
           Stops intermediários porque o gradiente da arte NÃO é interpolação
           linear entre as pontas: medido ponto a ponto, o ciano só abre nos
           ~20% finais (o meio da diagonal é #003e4f, não o #00687b que uma
           interpolação de 2 stops produziria). */
        linear-gradient(to bottom left,
          #00bcc7 0%,
          #0095a9 10%,
          #006070 25%,
          #003e4f 50%,
          #00243a 75%,
          #001530 100%);
    }
    /* Céu estrelado: pontinhos via radial-gradient, piscando devagar. Uma camada
       só (opacity num pseudo-elemento) — custa quase nada de GPU. */
    .page::after {
      content: '';
      position: absolute;
      inset: 0;
      z-index: -1;
      pointer-events: none;
      background-image:
        radial-gradient(1.5px 1.5px at 12% 18%, rgba(255,255,255,0.9), transparent 50%),
        radial-gradient(1px 1px at 73% 9%, rgba(255,255,255,0.7), transparent 50%),
        radial-gradient(1.5px 1.5px at 52% 6%, rgba(255,255,255,0.8), transparent 50%),
        radial-gradient(1px 1px at 31% 42%, rgba(255,255,255,0.5), transparent 50%),
        radial-gradient(1px 1px at 89% 33%, rgba(255,255,255,0.6), transparent 50%),
        radial-gradient(1.5px 1.5px at 7% 61%, rgba(255,255,255,0.45), transparent 50%),
        radial-gradient(1px 1px at 64% 74%, rgba(255,255,255,0.4), transparent 50%),
        radial-gradient(1px 1px at 43% 27%, rgba(255,255,255,0.65), transparent 50%),
        radial-gradient(1px 1px at 22% 84%, rgba(255,255,255,0.35), transparent 50%);
      animation: promo-twinkle 6s ease-in-out infinite alternate;
    }
    @keyframes promo-twinkle { from { opacity: 0.5; } to { opacity: 1; } }
    /* Hierarquia igual à da arte: o CIANO (#00bcc7) é ambiente — fundo, bordas,
       rótulos; quem precisa SALTAR usa o gelo #caecff (a mesma cor que a peça
       usa no "TODO ESSE UNIVERSO"). Com o fundo agora teal, preço e badge em
       ciano caíam na família do próprio fundo e perdiam força — o gelo resolve
       sem sair da paleta oficial. */
    .badge { background: rgba(0,188,199,0.18); border-color: rgba(0,188,199,0.55); color: #caecff; }
    .preco-card { border-color: rgba(0,188,199,0.35); }
    .preco-card .speed { color: #2fd3dd; }
    .preco-num { color: #caecff; } /* sólido, mesmo motivo do tema padrão */
    .preco-oferta { background: rgba(0,188,199,0.1); border-color: rgba(0,188,199,0.5); }
    .preco-oferta .lbl { color: #2fd3dd; }
    .proof-item i { color: #2fd3dd; }
    /* Barra fixa do mobile no petróleo do tema (era azul-royal do tema antigo). */
    .cta-fixo { background: rgba(0,21,48,0.85); border-top-color: rgba(0,188,199,0.22); }
    @media (prefers-reduced-motion: reduce) { .page::after { animation: none; } }
  </style>
<?php endif; ?>
</head>
<body>
  <div class="page">
    <div class="wrap">

      <div class="topo">
        <a href="/"><img src="/imgs/logo-masterinfo.png" alt="MasterInfo Internet" width="140" height="38"></a>
      </div>

      <div class="grade">
      <div class="col-oferta">
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
<?php if ($ofertaVal !== ''): ?>
        <div class="preco-oferta">
<?php if ($ofertaLbl !== ''): ?>
          <span class="lbl"><?= promo_e($ofertaLbl) ?></span>
<?php endif; ?>
          <span class="val"><?= promo_e($ofertaVal) ?></span>
        </div>
<?php endif; ?>
<?php if ($precoDet !== ''): ?>
        <div class="preco-cond"><?= promo_e($precoDet) ?></div>
<?php endif; ?>
<?php if ($appTexto !== '' || $appLogo !== ''): ?>
        <div class="preco-app">
<?php if ($appLogo !== ''): ?>
<?php /* eager: o card de preço cai dentro da 1ª dobra no celular — lazy aqui só atrasaria
         uma imagem que o visitante já está vendo. width/height fixos p/ não causar CLS. */ ?>
          <img src="<?= promo_e($appLogo) ?>" alt="" width="34" height="34" decoding="async">
<?php endif; ?>
<?php if ($appTexto !== ''): ?>
          <span><?= promo_e($appTexto) ?></span>
<?php endif; ?>
        </div>
<?php endif; ?>
      </div>
<?php endif; ?>
      </div><!-- /col-oferta -->

      <div class="col-acao">
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
      </div><!-- /col-acao -->
      </div><!-- /grade -->

      <!-- Selos e letra miúda ficam FORA da grade de propósito: dentro da coluna do
           formulário eles entravam na conta da altura da coluna, e aí a base do form
           media junto com eles — nunca casava com a do card de preço. No celular a
           ordem na tela não muda (a grade só existe em ≥900px; aqui é fluxo normal). -->
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

<?php if ($preco !== ''): ?>
  <div class="cta-fixo" id="ctaFixo" aria-hidden="true">
    <div class="cta-fixo-preco">
      <strong>R$ <?= promo_e($precoNum) ?><?php if ($precoCents !== ''): ?><span>,<?= promo_e($precoCents) ?></span><?php endif; ?></strong>
<?php if ($ofertaVal !== ''): ?>
      <small><?= promo_e($ofertaLbl !== '' ? $ofertaLbl : 'depois') ?> <?= promo_e($ofertaVal) ?></small>
<?php endif; ?>
    </div>
    <button type="button" class="cta-fixo-btn" id="ctaFixoBtn">Quero contratar</button>
  </div>
<?php endif; ?>

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

    // ── Barra de ação fixa ──
    // Aparece enquanto o botão real está fora de vista e some quando ele entra:
    // dois CTAs iguais na mesma tela confundem em vez de ajudar.
    var barra = document.getElementById('ctaFixo');
    if (barra) {
      window.promoAtualizarBarra = function(botaoNaTela) {
        if (botaoNaTela) {
          barra.removeAttribute('data-visivel');
          barra.setAttribute('aria-hidden', 'true');
        } else {
          barra.setAttribute('data-visivel', '');
          barra.setAttribute('aria-hidden', 'false');
        }
      };
      function botaoEstaNaTela() {
        var b = btn.getBoundingClientRect();
        return b.top < window.innerHeight && b.bottom > 0;
      }
      // Estado no 1º frame, sem esperar callback: o IntersectionObserver pode
      // atrasar a 1ª entrega (aba em background/prerender) e a barra ficaria
      // escondida justo em quem abre o link e não rola.
      window.promoAtualizarBarra(botaoEstaNaTela());

      // O preço da barra só entra quando o card de preço sai de vista (anti-eco).
      var card = document.querySelector('.preco-card');
      window.promoAtualizarPreco = function(cardNaTela) {
        if (cardNaTela) barra.setAttribute('data-preco-oculto', '');
        else barra.removeAttribute('data-preco-oculto');
      };
      function cardEstaNaTela() {
        if (!card) return false;
        var c = card.getBoundingClientRect();
        return c.top < window.innerHeight && c.bottom > 0;
      }
      window.promoAtualizarPreco(cardEstaNaTela());

      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function(entradas) {
          window.promoAtualizarBarra(entradas[0].isIntersecting);
        }, { threshold: 0.6 }).observe(btn);
        if (card) {
          new IntersectionObserver(function(entradas) {
            window.promoAtualizarPreco(entradas[0].isIntersecting);
          }, { threshold: 0.25 }).observe(card);
        }
      } else {
        // Sem IO (browser velho): scroll passivo é suficiente e não trava a rolagem.
        window.addEventListener('scroll', function() {
          window.promoAtualizarBarra(botaoEstaNaTela());
          window.promoAtualizarPreco(cardEstaNaTela());
        }, { passive: true });
      }

      document.getElementById('ctaFixoBtn').addEventListener('click', function() {
        if (typeof window.miTrack === 'function') { try { window.miTrack('cta_click', { label: 'barra fixa promo' }); } catch (e) {} }
        form.scrollIntoView({ behavior: 'smooth', block: 'center' });
        // Foca depois da rolagem: focar antes cancela o scroll suave e o browser
        // dá um salto seco até o campo. preventScroll pelo mesmo motivo.
        setTimeout(function() {
          try { document.getElementById('nome').focus({ preventScroll: true }); } catch (e) {}
        }, 450);
      });
    }

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
