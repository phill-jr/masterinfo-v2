# HANDOFF — SEO MasterInfo: de ~72 para 90

> Documento autossuficiente para uma NOVA sessão do Claude Code continuar a evolução de SEO do
> site **masterinfointernet.com** (projeto `masterinfo-v2`). Você NÃO tem a memória da conversa
> anterior — tudo que precisa está aqui. Data-base: 2026-06-22.

---

## 0. Contexto em 30 segundos

- Site institucional/landing da **MasterInfo Internet** (provedor de fibra em Joinville/SC), config-driven (HTML + PHP + JS vanilla).
- Passou por uma grande otimização de SEO/GEO. **Nota composta atual ≈ 72/100** (re-auditoria ao vivo com subagentes). **Meta = 90.**
- O **teto do que dá pra ganhar editando o repositório já foi atingido (~72-74)**. Os ~18 pontos restantes estão em **servidor (nginx) + autoridade off-site + tempo de reindexação** — ver tarefas abaixo.
- Já feito (no ar): on-page (titles/desc/canonical/H1), 13 páginas de bairro (7 com fatos reais pesquisados), 9 posts de blog, bio do fundador (E-E-A-T), schema amplo (Org/WebSite/LocalBusiness/ISP/FAQPage/BlogPosting/Person), **0 travessões de IA**, LocalBusiness nos bairros, autor dos posts = Person, preço crawlável, tabela comparativa no post PlayHub.

**Antes de começar:** rode a skill **`/sync-site-masterinfo`** (carrega acesso/deploy/arquitetura) e leia a memória do projeto em
`C:\Users\Philipe Alves\.claude\projects\C--Users-Philipe-Alves-Masterinfo\memory\` (em especial `seo-audit-2026-06-22.md`, `v2-deploy`, `v2-arquitetura`).

---

## 1. Regras inegociáveis (NÃO quebrar)

1. **Responder SEMPRE em português (pt-BR)** com o Philipe.
2. **PROIBIDO travessão (— ou –)** em qualquer conteúdo novo — é tell de IA e o site foi 100% limpo. Use vírgula/ponto/parênteses. Em prompts de geração de conteúdo, proíba explicitamente.
3. **Gerador é durável** — `python gerar_subpaginas.py --content` (pilares/blog/bairros/autor) e `--full` (personas/apps/ajuda) regeneram a partir das fontes (`conteudo_blog.py`, `gerar_subpaginas.py`). NÃO editar HTML gerado à mão (é revertido na regen) — editar a FONTE. `--menus` (default) só sincroniza header/rodapé/CTA.
4. **Conteúdo é config-driven.** A fonte da verdade de planos/empresa/FAQ/menus é o **admin de PRODUÇÃO** (`admin.html`), salvo em `config.json`. **Editar `config.json` no repo NÃO adianta** — o `deploy.sh` (passo 0.5) puxa o config de produção e sobrescreve. Mudanças de config = pelo admin.
5. **Duas homes separadas:** `index.html` (dark) e `index-light.html` (claro, a ATIVA). Mudança de conteúdo/markup em uma precisa ser replicada na outra (CSS/JS/config são compartilhados).
6. **Schema da home é runtime:** `site-loader.js > buildSchema()` reescreve `#schema-org` (ISP/LocalBusiness) ao carregar; o bloco estático `@graph` (Organization + WebSite) NÃO é sobrescrito. Para mudar o ISP da home, edite `buildSchema`.
7. **Git:** usar **Git Bash / git.exe** (NUNCA o git do WSL — quebra CRLF). `git pull --rebase --autostash` antes de deploy (o colaborador Eike commita direto).
8. **Deploy:** `wsl bash "temporarios/deploy.sh"` (1 comando; rsync + smoke test). **Outward-facing → confirmar com o usuário antes.**
9. **Verificar SEMPRE no ar** após deploy (curl + parse), não confiar só no local.

---

## 2. Acesso

| Item | Valor |
|------|-------|
| Repo | `github.com/phill-jr/masterinfo-v2` (branch `main`, conta gh `phill-jr`) |
| Pasta local | `C:\Users\Philipe Alves\Masterinfo\masterinfo-v2` |
| Produção | `https://masterinfointernet.com` → Cloudflare DNS-only → **DirectAdmin 45.168.4.18** |
| SSH (deploy) | `philipe@45.168.4.18` porta **9152**, chave `C:\Users\Philipe Alves\.ssh\id_ed25519_masterinfo` |
| Docroot | `/home/masterin/domains/masterinfointernet.com/public_html` (PHP 8.2) |
| Deploy | `wsl bash "temporarios/deploy.sh"` |
| GSC | MCP `awesome-gsc` (propriedade `sc-domain:masterinfointernet.com`, conta `philipeamads@gmail.com`) |

---

## 3. Tarefas priorizadas (P0 = maior impacto)

### P0 — Headers de segurança + cache no nginx (DESTRAVA Técnico e Performance) ✅ FEITO 2026-06-22
**✅ RESOLVIDO E NO AR (2026-06-22):** 5/5 security headers (X-Frame, X-Content-Type, Referrer, Permissions-Policy, HSTS) agora chegam no GET de TODO HTML estático (home, subpáginas, blog, bairros, checkout). Verificado por curl em 13 páginas + smoke test verde. **Mecanismo:** bloco `add_header ... always` condicional `|*if DOMAIN="masterinfointernet.com"|` no template custom do DA `/usr/local/directadmin/data/templates/custom/nginx_server_secure.conf` (antes do `|CUSTOM4|`, nível server), valores alinhados ao `security-headers.php` do app. Detalhes/rollback na memória `p0-security-headers-nginx`. **Causa-raiz** (diferente da hipótese abaixo): DA é reverse-proxy e serve estático via **X-Accel**, que DESCARTA os headers do Apache/.htaccess no GET; os `*.cust_nginx*.conf` da sessão anterior nunca eram incluídos. **Falta (deferido, não-bloqueante):** CSP nas estáticas (Report-Only primeiro; snippet pronto em `deploy/nginx-security.conf.example`) e Cache-Control no HTML (menor).

**Problema (histórico, já resolvido acima):** nas respostas **GET** dos HTML (200) NÃO chegavam `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, `Cache-Control`; o `Strict-Transport-Security` só aparecia nas 404. O `.htaccess` já tem regras, mas o **nginx (reverse proxy do DirectAdmin) não as repassa no GET**.

**Verificar (mostra o problema):**
```bash
curl -sS -o /dev/null -D - https://masterinfointernet.com/        # GET: faltam os headers
curl -sS -o /dev/null -D - -I https://masterinfointernet.com/     # HEAD: alguns aparecem
```

**Corrigir (no DirectAdmin — precisa de acesso ao servidor/host):** adicionar no nginx do domínio um bloco que injeta os headers nos estáticos. No DA, o caminho usual é um custom config do nginx para o domínio (ex.: `/usr/local/directadmin/data/users/masterin/nginx_php.conf` ou via "Custom HTTPD Configurations" do painel). Diretivas:
```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
# Cache: HTML curto, assets longos
location ~* \.html$ { add_header Cache-Control "public, max-age=600, stale-while-revalidate=86400" always; }
location ~* \.(css|js|png|jpg|jpeg|webp|svg|woff2|ico)$ { add_header Cache-Control "public, max-age=2592000, immutable" always; }
```
> CSP é o mais delicado (pode quebrar scripts inline/gtag/Bitrix). Comece SEM CSP (ou com `Content-Security-Policy-Report-Only`) e só endureça depois de validar GTM/GA4/Ads/Bitrix/marina-widget. Depois de aplicar, reverificar com o `curl` acima e rodar o agente `seo-technical`.
> ⚠️ Mexer no host toca SÓ o docroot do masterinfointernet.com — NÃO o `games.masterinfointernet.com` (FazUP, mesmo IP).

### P1 — Core Web Vitals de campo 🟠
- Precisa de **chave da Google API** (PageSpeed Insights / CrUX) — pedir ao Philipe ou configurar.
- Sem chave, só dá lab. Já feitos: hero WebP, lazy-load, defer de pixels, Phosphor self-host, async-CSS, hero `<picture>` no index-light.
- Faltam: WebP no resto do site (nginx transparente OU `gen_webp.py` + `<picture>` nas subpáginas/logo) e o `Cache-Control` (vem com a P0).
- Depois das correções, **revalidação do Google leva ~28 dias**. Medir com `seo-performance` / PSI.

### P2 — Autoridade off-site (MAIOR teto restante p/ IA e ranking) 🟠
Externo, leva semanas, mas é o que mais move a agulha:
- **Reclame Aqui** (presença verificada), **canal YouTube** (2-3 vídeos com a marca no título — maior correlação única com citação por IA), citações/backlinks locais (imobiliárias, listas de provedores de Joinville).
- Adicionar os perfis criados ao `sameAs` (schema `buildSchema` + bloco Org estático das 2 homes) e ao `llms.txt`.
- A sessão pode **rascunhar** roteiros de vídeo / textos de perfil, mas a criação de contas/posts é manual do Philipe.

### P3 — Itens do Philipe (rápidos, no admin de produção)
- **LinkedIn do Philipe** → adicionar em `sameAs` do schema `Person` em `/sobre/philipe/` (fonte: `gerar_subpaginas.py > page_autor`, dict `AUTHORS["philipe"]` em `conteudo_blog.py`) + link visível na página.
- `config.json` no admin: trocar os ~10 **travessões** (popup Copa "Copa do Mundo 2026 —", "ExitLag — ping mínimo", 2 diferenciais "...sua casa —", "...você paga —") por vírgula; corrigir `empresa.endereco` "Buschler" → "Prefeito Baltazar Buschle".

### P4 — Código menor (retorno modesto, dá pra fazer)
- **Estrada Timbé 301 (opcional):** `/internet-estrada-timbe-joinville/` na verdade é uma VIA dentro do Jardim Paraíso. Decidiu-se MANTER (capta a busca). Se o Philipe preferir consolidar: 301 no `.htaccess` → `/internet-jardim-paraiso-joinville/` + remover do `sitemap.xml` + ajustar links internos.
- **IndexNow:** usar a skill `/seo-bing` (cria a key + submete URLs ao Bing/Yandex). Só criar o arquivo da key NÃO basta.
- **`aggregateRating`:** o GMB tem 4,8★/2.447 avaliações, mas **NÃO** colocar rating auto-atribuído em Organization/ISP (o Google penaliza — já foi removido em 17/06). Só com fonte de reviews de terceiros válida.
- **FAQ mais citável:** as respostas da FAQ da home são curtas (~25 palavras; ideal 130-160 p/ IA). A FAQ da home é **config-driven** (admin). As FAQ de bairro/blog são do gerador (`render_faq`) — dá pra expandir com fatos, sem inventar.

### P5 — Medir e iterar
- **Re-rodar a auditoria** pra cravar a nota: skill `/seo-audit www.masterinfointernet.com` (ou disparar os subagentes `seo-technical`, `seo-content`, `seo-schema`, `seo-performance`, `seo-geo` em paralelo sobre o site AO VIVO). ⚠️ Os agentes pedem para VERIFICAR via curl antes de dizer que "falta schema" (já deram falso-positivo).
- **GSC** (MCP `awesome-gsc`): acompanhar indexação das páginas novas + cliques/impressões. Reindexação completa leva ~4-8 semanas.

---

## 4. Pesos do score (pra priorizar)
Técnico 22% · Conteúdo 23% · On-Page 20% · Schema 10% · Performance 10% · IA 10% · Imagens 5%.
A **P0 (nginx)** sozinha levanta Técnico (22%) e parte de Performance (10%) — é o maior salto de nota por esforço.

---

## 5. Definição de pronto
- P0 aplicada e confirmada (headers no GET via curl) + `seo-technical` reavaliando Técnico ≥ 85.
- Nota composta re-auditada ≥ 85 (90 depende também do off-site + reindexação).
- Nada quebrado: smoke test do deploy verde (`/`, `/index-light.html`, `/contato/`, `/checkout.html`, `/api/marina.php` → 200) + sem regressão visual.
