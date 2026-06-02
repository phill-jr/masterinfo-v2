# ✅ HANDOFF — Integração Bitrix24 (COMPLETA)

> Última atualização: 01/06/2026 · Quem deixou: Philipe + Claude
> **Status: 3 de 3 fases concluídas — integração funcionando ponta a ponta.**

## 📋 Status atual

| Fase | O que é | Status |
|---|---|---|
| **B1 — Backend PHP** | 6 endpoints de admin + 1 endpoint público que recebe forms e manda pro Bitrix | ✅ **Pronto** + 🐛 corrigido bug de sintaxe no `form-submit.php` (`match` não pode retornar referência → trocado por `if/elseif`; antes dava 500 sempre) |
| **B2 — Painel Admin UI** | Aba "Bitrix" no `admin.html`: testar conexão + configurar formulários (tipo, funil, etapa, mapeamento por dropdown dos campos do Bitrix, testar com dados fake) | ✅ **Pronto** |
| **B3 — Migrar form da Copa** | `copa/index.html` envia pro `/api/form-submit.php` em paralelo ao Google Sheets (redundância) | ✅ **Pronto** |

> **Nota de UI (B2):** o card de "apelidos UF_CRM" foi descartado — em vez de apelidar 248 campos, o mapeamento do formulário usa um **dropdown** que lista os campos de Contato + Negócio direto do Bitrix (nome amigável + código), agrupados. Mais simples e direto.

## ✅ O que JÁ tá pronto e funcionando (B1)

**Arquivos novos no repo:**
```
api/admin/_bitrix-helper.php       ← helpers (chamada REST, load/save mapping)
api/admin/bitrix-test.php          ← GET: testa o webhook
api/admin/bitrix-categories.php    ← GET: lista funis (7 cadastrados)
api/admin/bitrix-stages.php        ← GET: lista etapas de um funil
api/admin/bitrix-fields.php        ← GET: 297 campos do Deal (248 UF_CRM)
api/admin/bitrix-mapping.php       ← GET/POST: salva/lê config (CSRF)
api/form-submit.php                ← POST público: recebe form do site
secrets/config.example.php         ← modelo do config (não commitar o real)
```

**O default já mapeia a pré-venda da Copa:** funil **Comercial** (id 0), etapa **Negociação** (NEW), entidade **Deal**, campos `nome → CONTACT.NAME`, `telefone → CONTACT.PHONE`, `bairro → DEAL.COMMENTS`.

## 🔧 Pra ATIVAR no servidor PHP (5 min)

1. Subir o conteúdo do repo pro servidor PHP (a hospedagem que o Philipe vai indicar).
2. Criar manualmente o arquivo `secrets/config.php` lá no servidor (NÃO commitar — está no `.gitignore`):
   ```php
   <?php
   define('BITRIX_WEBHOOK', 'https://masterinfointernet.bitrix24.com.br/rest/1/orycdrdahxtib8g3/');
   define('ALLOWED_ORIGIN', 'https://www.masterinfointernet.com');
   define('SESSION_SECRET', '<gerar com: php -r "echo bin2hex(random_bytes(32));">');
   ```
3. Garantir que a pasta `secrets/` é gravável pelo PHP (vai criar `secrets/bitrix-mapping.json` ao salvar mapeamentos).
4. Testar logado como admin:
   - `GET /api/admin/bitrix-test.php` → deve retornar `{"ok":true,"user":"Philipe Alves"}`
   - `GET /api/admin/bitrix-categories.php` → 7 funis
   - `GET /api/admin/bitrix-fields.php?entity=deal` → 297 campos

## 🛠️ O que FALTA fazer (B2 + B3)

### Fase B2 — Painel Admin UI
Adicionar uma aba nova **"Integração Bitrix"** no `admin.html` (que já existe). A aba precisa ter 3 cards:

**Card 1 — Conexão**
- Mostra status do webhook (chama `bitrix-test.php`)
- Botão "Testar conexão" → mostra ✅/❌ com nome do usuário

**Card 2 — Apelidos dos campos UF_CRM**
- Chama `bitrix-fields.php?entity=deal`
- Tabela com 248 campos UF_CRM (id + input pra dar nome amigável)
- Busca/filtro (são 248, tem que ter como achar)
- Botão "Salvar apelidos" → POST `bitrix-mapping.php` (campo `field_labels`)
- Os apelidos salvos viram dropdown amigável no Card 3

**Card 3 — Formulários do site**
Lista expansível dos forms configurados (hoje só `pre-venda-copa`). Cada um:
- Tipo de entidade: radio **Lead / Deal / Contact**
- Funil: `<select>` populado pelo `bitrix-categories.php`
- Etapa inicial: `<select>` populado pelo `bitrix-stages.php` (atualiza quando muda o funil)
- Mapeamento dos campos: tabela `campo do form → campo do Bitrix` (usando os apelidos do Card 2)
- Template do título do deal (ex: `Pré-venda Copa — {nome} ({bairro})`)
- Botão "Salvar form" → POST `bitrix-mapping.php` (campo `forms[slug]`)
- Botão "Testar com dados fake" → cria um deal de teste no Bitrix

**Padrão de UI:** seguir o estilo dos cards já existentes no `admin.html` (mesma paleta, mesmo padrão de input, mesmo botão laranja).

**CSRF:** usar o token que já é gerado pelo `auth/csrf.php` (ver como o `admin-config.php` faz hoje).

### Fase B3 — Migrar form da Copa
No arquivo `copa/index.html`, trocar o método de envio.

**Hoje (Google Sheets via form+iframe):**
```js
var SHEETS_ENDPOINT = 'https://script.google.com/macros/s/.../exec';
// ... cria iframe + form HTML
```

**Depois (PHP/Bitrix):**
```js
fetch('/api/form-submit.php', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    form: 'pre-venda-copa',
    data: { nome, bairro, telefone }
  })
}).then(function(){
  // abre WhatsApp em seguida (mesma lógica de hoje)
});
```

**Sugestão:** manter o Sheets em paralelo no começo (redundância de segurança). Só remover quando confirmar que o Bitrix está caindo certinho.

## 🐛 Pontos de atenção / gotchas

- **O site hoje está no GitHub Pages** (que NÃO roda PHP). Antes de testar qualquer coisa, precisa subir num host com PHP 8+.
- **248 UF_CRM estão sem título no Bitrix** — todos retornam o próprio ID como `title`. Por isso a tela de apelidos do Card 2 é essencial. Sem ela, o usuário do admin não vai saber o que cada campo significa.
- **PHP 8.0+** é necessário (uso de `match` expression no helper).
- **CORS:** o `ALLOWED_ORIGIN` no `secrets/config.php` precisa bater com o domínio onde o site fica hospedado (senão o form-submit.php bloqueia).
- **Rate limit:** form-submit tem 20 envios/hora por IP (anti-spam). Pra eventos de alto volume, ajustar em `api/rate-limit.php`.

## 🧪 Como testar B1 antes de mexer no UI

Com o servidor PHP rodando e logado no admin do site:

```bash
# 1. Sanity check
curl --cookie-jar c.txt https://SITE/auth/login.php -d 'user=admin&pass=...'
curl --cookie c.txt https://SITE/api/admin/bitrix-test.php
# Esperado: {"ok":true,"user":"Philipe Alves","id":"1","admin":true}

# 2. Funis
curl --cookie c.txt https://SITE/api/admin/bitrix-categories.php
# Esperado: 7 funis (Comercial, CS - Relacionamento, ...)

# 3. Disparar lead fake (publico)
curl https://SITE/api/form-submit.php \
  -H 'Content-Type: application/json' \
  -d '{"form":"pre-venda-copa","data":{"nome":"Teste B1","bairro":"Comasa","telefone":"(47) 99999-0000"}}'
# Esperado: {"ok":true,"contact_id":N,"entity_id":N,"entity":"deal"}
# E aparece o deal no Bitrix > Funil Comercial > Negociação
```

## 📞 Contatos

- **Webhook do Bitrix** (já configurado): `https://masterinfointernet.bitrix24.com.br/rest/1/orycdrdahxtib8g3/`
- **Webhook ID** no Bitrix: `30` (Aplicativos → Desenvolvedores → Webhooks)
- **Permissão atribuída:** CRM
- **Funil padrão da Copa:** Comercial (id 0)
- **Etapa inicial padrão:** Negociação (`NEW`)

## 📁 Onde está cada coisa

- Site em produção: GitHub Pages (`phill-jr.github.io/masterinfo-v2/`) — **não roda PHP**
- Repo: `github.com/phill-jr/masterinfo-v2`
- Backup atual da Copa: Google Sheets via Apps Script (em `copa/leads-apps-script.gs`)
- Pasta de leads local: `Desktop/03 - Masterinfo Internet/Lançamento - Master/`

---

**Status final:** integração completa e validada localmente (conexão, listagem de funis/etapas/campos, salvar mapeamento, criar deal de teste ponta a ponta). Próximo passo é só **ativar em produção** (host PHP): subir o repo, criar o `secrets/config.php` real e migrar o DNS/hospedagem do GitHub Pages (que não roda PHP) pra um servidor com PHP 8+.

> ⚠️ Deals de teste criados durante a validação (apagar no Bitrix): `394256`, `394294`, `394296` + contato `79986`.
