# Auditoria SEO/GEO — masterinfo-v2 (18/06/2026, nível hard)

Auditoria linha-a-linha de TODO o site. Foco em **achados NOVOS** além do já corrigido
(canonical, 19 redirects + www→non-www, title/meta únicos, OG+JSON-LD subpáginas, og-image, rating removido).

---

## ✅ O que já está SÓLIDO (confirmado nesta auditoria)

| Item | Status | Evidência |
|---|---|---|
| Canonical self-referente | ✅ todas as páginas | curl |
| http → https | ✅ 301 | `http://` → `https://` |
| www → non-www | ✅ 301 | corrigido 18/06 |
| robots.txt (libera bots de IA: GPTBot, ClaudeBot, PerplexityBot, Google-Extended…) | ✅ | `robots.txt` |
| **llms.txt** | ✅ **EXCELENTE** (planos, FAQ, cobertura, contato, diferenciais) | `llms.txt` |
| Sitemap (20-21 URLs, sem checkout) | ✅ | `sitemap.xml` |
| 404 retorna 404 | ✅ | curl |
| Hierarquia de headings (1 `<h1>` por página indexável) | ✅ | 25/25 págs = 1 h1 |
| Title + meta description únicos (subpáginas) | ✅ | `sync_seo_meta` |
| Open Graph + Twitter Card (subpáginas) | ✅ | `sync_og` |
| JSON-LD Breadcrumb+WebPage (subpáginas) | ✅ | `sync_schema` |

---

## 🔴 CRÍTICO — Performance / Core Web Vitals (categoria NOVA, alto impacto no ranking)

### C1. Imagem de hero gigante — `banner-aplicativos.png` = **1.172 KB (1,1 MB)**, 1920×1080
- **Evidência:** `imgs/hero/banner-aplicativos.png` 1,1 MB; `banner-copa.png` 241 KB (slide 0, eager = LCP).
- **Impacto:** LCP ruim + desperdício de banda. PNG é o pior formato pra foto.
- **Fix:** converter os banners pra **WebP** (qualidade 80 → ~80-150 KB), atualizar `src`. Manter PNG como fallback se quiser (`<picture>`).

### C2. Leaflet (mapa) carregado SÍNCRONO no `<head>`
- **Evidência:** `index-light.html:38-39` (e `index.html`): `<link ...leaflet.css>` + `<script ...leaflet.js>` no head, **bloqueando render**. ~150 KB para um recurso usado **só no modal de cobertura** (sob clique).
- **Impacto:** atrasa First Paint/LCP de TODAS as visitas por uma feature que a maioria não usa.
- **Fix:** carregar Leaflet **on-demand** (injetar CSS/JS quando o usuário abre o modal de cobertura). Tira ~150 KB do caminho crítico.

### C3. `site-loader.js` + `playhub.js` via `document.write(... ?v='+Date.now())`
- **Evidência:** `index-light.html:1477-1478`: `document.write('<script src="site-loader.js?v=' + Date.now() + ...')`.
- **Impacto duplo:** (a) `document.write` **trava o parser** (anti-pattern penalizado pelo Chrome); (b) `?v=Date.now()` muda a URL **a cada page view** → o navegador **NUNCA cacheia** esses 2 scripts → re-download em toda visita/navegação.
- **Fix:** trocar por `<script defer src="site-loader.js?v=20260618">` com **versão fixa** (bumpar só quando editar). ⚠️ site-loader é crítico — testar ordem de execução em `localhost:8091` antes (ele injeta conteúdo do config; precisa rodar após o DOM).

---

## 🟡 ALTO

### A1. Phosphor Icons script síncrono no `<head>` (de `unpkg.com`)
- **Evidência:** `index-light.html:35` `<script src="https://unpkg.com/@phosphor-icons/web@2.0.3"></script>`.
- **Fix:** `defer` no script, ou self-host só o subset de ícones usados.

### A2. Dependências de terceiro (`unpkg.com`) no caminho crítico
- **Evidência:** Phosphor + Leaflet vêm de `unpkg.com` (CDN externo).
- **Impacto:** latência de DNS/conexão extra + risco (se unpkg cair, quebra). 
- **Fix:** self-hostar (servir do próprio domínio) → menos conexões, mais controle, melhor cache.

### A3. Quase nenhuma imagem em WebP/AVIF
- **Evidência:** só **2** imagens webp/avif em todo `imgs/`. O resto é PNG/JPG.
- **Fix:** pipeline de conversão pra WebP nas imagens pesadas (heros, logos de plano).

### A4. Schema do provedor incompleto (LocalBusiness/ISP)
- **Evidência:** `index.html` JSON-LD `InternetServiceProvider` tem address/areaServed/telephone/offers, mas **falta `geo` (coordenadas), `openingHours`, `image`, `@id`**.
- **Impacto:** enfraquece elegibilidade a painel de conhecimento local + Google Maps/local pack.
- **Fix:** adicionar `geo: {latitude, longitude}` (da Rua Baltazar Buschler 628), `openingHours`, `image` (logo/og-image). Reaproveitar no `buildSchema` do site-loader.

---

## 🟢 MÉDIO / Refinamento

### M1. `alt=""` em imagens
- **Evidência:** `tv-streaming/index.html` 8 logos de app com `alt=""` (ex.: `imgs/sky.jpg alt=""`); home hero 2 (slideshow). 
- **Nota:** baixa prioridade — os logos têm o NOME do app em texto ao lado (decorativo). Hero é slideshow com aria-label no link.
- **Fix:** `alt="SKY+ Light"` etc. nos logos da matriz; hero pode manter `alt=""` (decorativo) se o link tiver aria-label.

### M2. FAQ schema só na home (injetado em runtime pelo site-loader)
- **Evidência:** subpáginas têm Breadcrumb+WebPage, mas **não** FAQPage. A home tem FAQ via `loadFaqSchema`.
- **Fix:** as páginas Internet (familia/gamer/home-office) têm conteúdo de FAQ implícito → adicionar `FAQPage` schema (a skill aponta FAQ como maior probabilidade de citação em IA/GEO).

### M3. Sitemap `lastmod` desatualizado
- **Evidência:** `sitemap.xml` lastmod = 2026-06-17, mas houve mudanças em 06-18 (meta, OG, schema, redirects).
- **Fix:** bumpar lastmod das páginas tocadas pra 2026-06-18.

### M4. Sem `Service`/`Product` schema nas páginas de plano
- **Fix:** cada página Internet poderia ter `Service` (provider = MasterInfo, areaServed Joinville, offers) — reforça relevância.

### M5. GEO — answer-first nas subpáginas
- As subpáginas Internet têm h1 + conteúdo, mas sem parágrafo "answer-first" (TL;DR) no topo (como adicionamos na home). Ajuda citação em IA.

---

## 📋 Plano de ação priorizado (impacto × esforço)

| # | Ação | Impacto | Esforço |
|---|---|---|---|
| 1 | Converter heros + logos pesados pra **WebP** (C1, A3) | 🔴 alto (LCP) | médio |
| 2 | **Leaflet on-demand** (C2) | 🔴 alto (render) | médio |
| 3 | Trocar `document.write`+`Date.now()` por `defer`+versão fixa (C3) | 🔴 alto (cache+parser) | médio (testar) |
| 4 | `defer`/self-host Phosphor + Leaflet (A1, A2) | 🟡 | baixo-médio |
| 5 | Enriquecer ISP schema: geo+openingHours+image (A4) | 🟡 (local SEO) | baixo |
| 6 | FAQPage schema nas páginas Internet (M2) | 🟢 (GEO) | médio |
| 7 | Corrigir `alt` dos logos + sitemap lastmod (M1, M3) | 🟢 | baixo |

**Veredito:** o **crawl/indexação/on-page/GEO está sólido**. O território **não explorado e de maior retorno agora é PERFORMANCE/Core Web Vitals** (itens C1-C3) — é fator de ranking do Google e estava intocado. Depois, enriquecimento de structured data (A4, M2, M4) pra local SEO + GEO.
