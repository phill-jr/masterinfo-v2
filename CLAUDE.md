# MasterInfo v2 — PROJETO ATIVO do site MasterInfo ✅

Você está na pasta **certa**. Esta é a versão ATIVA / produção do site MasterInfo (redesign v2, landing page).

- Pasta: `C:\Users\Philipe Alves\masterinfo-v2` · remote `github.com/phill-jr/masterinfo-v2`.
- ⚠️ A pasta sibling `C:\Users\Philipe Alves\Masterinfo` (remote `sitemaster`) é o site **ANTIGO** — não mexer lá.
- Dev: `python -m http.server 8091` rodando nesta pasta. Admin: `http://localhost:8091/admin.html` · site: `http://localhost:8091/index-light.html`. Ver `COMO-EDITAR.md`.

## Arquitetura (o essencial pra não errar)
- **Conteúdo é config-driven.** `admin.html` (CMS — abas Empresa, Cobertura, FAQ, Planos, Extras, Tracking, SEO, Menus, Bitrix, Marina) edita o `config.json`, salvo via `api/admin-config.php` (PHP + CSRF, backup em `secrets/config.json.bak`).
- **`site-loader.js`** faz `fetch('config.json')` e injeta o conteúdo no site **em-lugar** (textContent/href/meta) por **id** — ex.: `#footerCnpj`, `#footerEmail`, `#footerWhatsapp`. ⚠️ **Regra de ouro: se o elemento no HTML não tiver o id que o `site-loader` espera, o valor do admin NÃO aparece no site** (foi exatamente o bug do CNPJ no rodapé do `index-light.html`, corrigido em 02/06/2026).
- `index.html` = tema escuro (tem todos os ids de rodapé). `index-light.html` = variante light, em uso ativo — estava SEM os ids do rodapé; só o `#footerCnpj` foi religado. Os demais (`footerWhatsapp/Email/Instagram/Facebook/Desc`) ainda estão chumbados ali.
- Subpáginas (familia, gamer, home-office, tv-streaming, aplicativos/*) são geradas por `gerar_subpaginas.py` — **texto chumbado no Python, NÃO lê o config**.
- `copa/`, `api/form-submit.php`, `api/admin/bitrix-*.php`, `secrets/bitrix-mapping.json` = captação de lead (Bitrix24), fora do conteúdo do admin.

Histórico e detalhes mais finos ficam na memória do projeto (`repos-masterinfo`, `v2-arquitetura`).
