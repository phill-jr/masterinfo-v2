# MAPEAMENTO — Campos do site × Painel admin (masterinfo-v2)

> Mapa de quais campos do site refletem as edições do painel `admin.html`.
> **Formulários Bitrix ficam de fora** (captação de lead — outra função).
> Atualizado em 01/06/2026.

## Arquitetura

- **Produção:** `index.html` (tema escuro). `index-light.html` é variante órfã.
- **Fluxo:** `admin.html` (abas) → grava `config.json` via `api/admin-config.php` (PHP + CSRF) → **`site-loader.js`** injeta na home (atualiza em-lugar; não regenera grids, pra não quebrar carrossel/copa/promo/mapa). Também leem `config.json`: `checkout.js` (planos/addons/tema) e `tracking.js`.
- **Antes deste trabalho:** `site-loader.js` não era carregado em lugar nenhum → a home era 100% chumbada e o admin era "fantasma". Agora o loader está wirado na `index.html`.

## O que REFLETE as edições do admin

| Seção do site | `config.json` | Aba do admin | Reflete? | Onde |
|---|---|---|---|---|
| SEO — title, description, OG, Twitter | `seo.*` | **SEO** (nova) | ✅ | `loadSeo` |
| Schema.org JSON-LD (nome, tel, endereço, **preços dos planos**) | derivado de `empresa`+`planos`+`seo` | SEO/Empresa/Planos | ✅ | `loadSeo`/`buildSchema` (regenerado) |
| Rodapé — CNPJ, descrição, Instagram, Facebook, WhatsApp, e-mail | `empresa.*` | Empresa | ✅ | `loadFooter` |
| FAQ — perguntas e respostas | `faq[]` | Social | ✅ | `loadFaq` |
| **Planos — preços** (à vista + cheio) das 2 seções da home | `planos[].precoPontual` / `precoCheio` | Planos | ✅ | `loadPlanos` (sync em-lugar) |
| Cobertura — nomes das tags de bairro | `bairros[].nome`/`dataBairro` | Cobertura | ✅ | `loadBairros` |
| Checkout — modo, tema, whatsapp, planos, addons | `checkout.*`, `planos[]`, `addons[]` | Empresa/Planos/Extras | ✅ | `checkout.js` |
| Tracking — GTM/GA4/Ads/Pixel | `tracking.*` | Tracking | ✅ | `tracking.js` |

## Chumbado por DECISÃO (o redesign do v2 divergiu do config)

Estas seções foram redesenhadas além do que o `config.json` descreve; **deixadas como estão** a pedido:

| Seção | Por quê |
|---|---|
| **Hero** | é um carrossel de banners (imagens), não usa `hero.*` (texto) |
| **Depoimentos** | marquee com nomes diferentes dos de `config.depoimentos` |
| **Números sociais** (`4.9 / 2382 / 97% / 6+`) | `data-sp-target` chumbados, diferentes de `config.stats` |
| Copa popup, Promo bar, Mega-menus, Títulos de seção | conteúdo bespoke, não há campo no config |
| Diferenciais ("Atendimento Local"…) | a seção do config **não existe** na home v2 |

## Limitações conhecidas

- **Planos:** só os **preços** sincronizam. Velocidade exibida (ex.: "1000 Mega" vs config "1 Giga"), apps inclusos (SKY/Deezer/Disney) e features ("Instalação 3 dias"…) são **bespoke** do redesign — não vêm do config.
- **Bairros:** só os **nomes** das tags. As coordenadas dos pins do mapa Leaflet seguem no script inline da `index.html` (bespoke).
- **Subpáginas** (`familia/`, `gamer/`, `aplicativos/*`…): geradas pelo `gerar_subpaginas.py` (texto chumbado no Python). **Não** são config-driven — editar exige rodar o gerador.
- **Salvar no admin** exige o host **PHP** (`api/admin-config.php`). Em servidor estático (preview), o admin carrega via fallback `config.json` mas não persiste o save.

## Bug corrigido (pré-existente)

`renderAddons` fazia `a.incluidoEm.indexOf(...)`, mas os addons do v2 não têm `incluidoEm` → lançava `TypeError` e abortava `renderAll` **antes** de `renderTracking` e do novo SEO. As abas **Extras** e **Tracking** estavam silenciosamente quebradas. Corrigido com guarda `(a.incluidoEm || [])` + init em `toggleAddonPlan` + fallback `a.instalacao || 0`.

## Arquivos alterados

- `site-loader.js` — reescrito para o v2 (loadSeo, loadFooter, loadFaq, loadPlanos, loadBairros; atualização em-lugar).
- `index.html` — `<script src="site-loader.js">` + ids no rodapé (`footerDesc/Instagram/Facebook/Whatsapp/Email/Cnpj`).
- `config.json` — nova chave `seo`.
- `admin.html` — aba **SEO** (render/update) + fix do `renderAddons`.

## Como verificar (end-to-end)

1. Servir com PHP: `php -S localhost:8091` (ou o host de produção). Estático (`python -m http.server`) serve o site mas não salva no admin.
2. No `admin.html`, mudar um **preço** na aba Planos → Salvar → abrir `index.html` → o card e o JSON-LD refletem (provado: 99,90 → 88,80 propagou pro card e pro Schema).
3. Mudar `seo.title` / rodapé / FAQ e conferir na home.
