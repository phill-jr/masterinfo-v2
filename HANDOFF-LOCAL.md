# Dossiê — Projeto Site MasterInfo (handoff p/ outra sessão Claude)

> Documento de orientação local. Aponte qualquer nova sessão do Claude pra ler este arquivo
> antes de mexer no site — ele resume pasta certa, como rodar, deploy, arquitetura e integrações.

---

## ⚠️ Regra nº 1 — tem DUAS pastas, use a certa

| | Pasta | Remote | Status |
|---|---|---|---|
| ❌ **NÃO use** | `C:\Users\Philipe Alves\Masterinfo` | `github.com/phill-jr/sitemaster` | **ANTIGO / legado** |
| ✅ **USE esta** | `C:\Users\Philipe Alves\masterinfo-v2` | `github.com/phill-jr/masterinfo-v2` | **ATIVO / produção** |

Antes de editar qualquer arquivo do site, confirme: `git remote -v` tem que mostrar **`masterinfo-v2`**.
Se mostrar `sitemaster`, você está no lugar errado. (Já se perdeu ~30 min editando a pasta errada — por isso a regra.)

Branch ativa: `main`. Últimos commits relevantes da v2: `c088b22` (fonte Archivo), `6a95891` (pass anti-IA),
`1226c7e` (6 planos novos 2026 — commit do **Eike**, colaborador), `aa70fec` (escala + Central Assinante).

---

## 🏃 Como rodar local (GOTCHA crítico)

- **Use PHP, NÃO python:**
  `php -S localhost:8091 -t "C:\Users\Philipe Alves\masterinfo-v2"` (PHP 8.4 instalado no Windows).
- `python -m http.server 8091` serve `.php` como **TEXTO** → admin não salva, cobertura/IXC, boletos da Marina,
  formulários→Bitrix e republish das subpáginas **não funcionam**. Sintoma clássico
  ("as integrações pararam / tokens zeraram") = na real é o python.
- Prova rápida de que o PHP está executando: `GET /api/marina.php` → `{"enabled":true,"configured":true}`.
- Admin: `admin.html` (exige login via `admin-login.html` → `auth/login.php`, sessão PHP + CSRF).
  Sem login → POST volta **401** e não grava.

### URLs locais
- Site (home clara, a ativa): http://localhost:8091/index-light.html
- Home dark: http://localhost:8091/index.html
- Admin (CMS): http://localhost:8091/admin.html
- Checkout: http://localhost:8091/checkout.html

---

## 🚀 Deploy (3 fatos que confundem)

1. `git push origin main` → GitHub Actions → **GitHub Pages em SUBPATH** `https://phill-jr.github.io/masterinfo-v2/`.
   Caminhos root-absolute (`/termos/`, `/tracking.js`) **quebram** nesse subpath → é só espelho secundário.
2. **Produção real `masterinfointernet.com` é WordPress** (tema Bridge, WPBakery 5.5.2, Wordfence) — **NÃO é o repo v2**.
   O push não atualiza a produção. Todo o hardening/admin do v2 **não protege o site público hoje**.
3. **Credencial de push (resolvida):** helper git local aponta pro `gh` logado como `phill-jr`.
   `git push` simples já funciona nesta pasta. Antes de qualquer rsync/deploy:
   `git pull --rebase --autostash` (o Eike commita direto).

---

## 🧱 Arquitetura (config-driven)

- **Fonte única = `config.json`**, editado pelo `admin.html` (13 abas) e salvo por `api/admin-config.php` (CSRF).
- **2 homes HTML separadas, SEM auto-sync:** `index.html` (dark) e `index-light.html` (claro, **a ATIVA**).
  Mudança de **conteúdo/section/link/copy** num precisa ser **replicada no outro**.
  CSS/JS/config são compartilhados (não replicar).
- **21 subpáginas estáticas** geradas por `python gerar_subpaginas.py`
  (default `--menus` = sync cirúrgico de header+rodapé; `--full` regenera corpo e **reverte** melhorias —
  usar só intencionalmente). O `admin-config.php` roda o gerador automaticamente após salvar.
- **Home renderiza em runtime** via `site-loader.js` (menus, rodapé, FAQ, schema SEO, popup Copa, escala do site).
- **Links de checkout = convenção `data-plano="<id>"`** (regra única) ou `href="checkout.html?plano=<id>"`.
  IDs canônicos: `lite-casa` / `lite-familia` / `lite-home-office` / `ultra-familia` / `ultra-home-office`.
  **Nunca** usar `#` num CTA de checkout.
- **Secrets** (`secrets/config.php`, `secrets/ixc.php`, `secrets/bitrix-mapping.json`) são **gitignored** →
  recriar no admin de produção. Nunca commitar.

---

## 🔌 Integrações / sistemas vizinhos

- **Cobertura (CEP):** `api/viabilidade.php` → ViaCEP → Nominatim → IXC (`rad_caixa_ftth`).
  Configurável no admin (aba Cobertura, store `secrets/ixc.php`).
- **Boletos / 2ª via = chat da "Marina"** (agente do **Sync Hub**, acesso IXC). Site só fala com `/api/marina.php` (proxy).
  Front existe em 2 lugares: `marina-widget.js` (float global) + `ajuda/boletos/index.html` (inline) — manter em sincronia.
- **Bitrix24 = captação de lead:** `api/form-submit.php`, `api/checkout.php`, dedup por telefone E.164, jornada via timeline.
  Slugs no `bitrix-mapping.json` (gitignored).
- **FazUP (indicações/gamificação)** = `games.masterinfointernet.com/indicar/cliente` — destino da seção "Indique e Ganhe".
- **Central do Assinante IXC** = `sistema1.masterinfointernet.com/central_assinante_web` (Vue2).
  Login com captcha + cookie cross-domain → **sem SSO de fora**; Área do Cliente própria teria que usar webservice v1 IXC.
- **Tracking 1st-party** (`tracking.js`) em todas as páginas; pixels GTM/GA4/Ads/FB gated por
  `config.enableTracking` (hoje **false**) + LGPD (`cookie-consent.js`, Consent Mode v2).
- **2 WhatsApps:** Principal `554734341734` (atendimento) e Comercial `5547989212991`
  (vendas, é o número único no resto do site).

---

## 🧠 Onde está a memória persistente deste projeto

```
C:\Users\Philipe Alves\.claude\projects\C--Users-Philipe-Alves-Masterinfo\memory\
├── MEMORY.md              ← índice (carregado toda sessão)
├── repos-masterinfo.md    ← as 2 pastas
├── v2-arquitetura.md      ← config-driven, site-loader, gerador
├── v2-admin-local.md      ← admin + php -S vs python
├── v2-deploy.md           ← Pages subpath / produção WP / credencial
├── producao-wordpress.md  ← produção é WordPress, não o repo
├── v2-dual-home-sync.md   ← regra das 2 homes
├── cobertura-ixc.md / marina-boletos.md / contato-page.md
├── paginas-legais.md / central-assinante-mapa.md
├── indique-ganhe.md / escala-site.md / home-refresh-antiia.md
```

> Esse caminho de memória é atrelado à pasta **antiga** (`...-Masterinfo`). Se você abrir a sessão direto na v2,
> a memória fica noutro diretório de projeto e **não carrega automaticamente** — vale apontar o outro Claude pra ler estes arquivos.

**Regra global do Philipe** (vale em toda sessão): `C:\Users\Philipe Alves\.claude\CLAUDE.md` —
stack PHP 8 / IXC / VPS `45.168.7.5:1822`, deploy via WSL+SCP, padrões de DB idempotente, etc.
