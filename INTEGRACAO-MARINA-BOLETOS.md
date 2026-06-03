# Integração Marina (Sync) ↔ Site MasterInfo — Página de Boletos

> **Para:** time/agente do projeto **Sync** (dono do agente **Marina**).
> **De:** site institucional **MasterInfo** (`masterinfo-v2`, PHP sem framework).
> **Objetivo:** colocar a Marina atendendo na página **`/ajuda/boletos`** do site, pra o cliente pegar a 2ª via / boleto conversando com ela.

---

## 1. O que queremos

Na página de boletos do site vai ter um **chat**. O cliente informa o **CPF** + mensagem, e a **Marina** (que vocês já têm, com acesso ao IXC) **valida o CPF e devolve o(s) boleto(s)**.

O site **não** acessa o IXC nem o proxy de LLM. O site só conversa com **um endpoint HTTP da Marina**. Toda a inteligência e o acesso ao IXC continuam do lado de vocês (Sync).

**Resumindo: preciso que a Marina seja exposta como uma API HTTP** que recebe `{cpf, mensagem, sessão}` e responde `{texto, boletos[]}`. O resto eu faço do lado do site.

---

## 2. Arquitetura

```
Navegador do cliente
   │  (só vê o chat; nunca vê token nem IXC)
   ▼
[ Site MasterInfo ]  api/marina.php  (proxy PHP — guarda o token, faz rate-limit)
   │  POST server-to-server, com Authorization
   ▼
[ Sync ]  ENDPOINT DA MARINA   ← É ISSO QUE PRECISO DE VOCÊS
   │
   ├─ valida CPF no IXC
   ├─ acha o cliente / contrato
   ├─ pega faturas em aberto (fn_areceber)
   └─ devolve texto + boleto (linha digitável / PIX / PDF)
```

- Chamada é **servidor→servidor** (PHP do site → endpoint da Marina). **Não é o navegador** que chama. Logo **não precisa de CORS**.
- O site manda um **token** em header (vocês definem).

---

## 3. O que o SITE já faz (deste lado, não precisam fazer nada)

- Renderiza o chat na página de boletos.
- Valida o **formato** do CPF (11 dígitos) antes de enviar.
- Mantém um **`session_id`** por conversa (pra vocês terem histórico, se usarem).
- Faz **rate-limit / anti-abuso** (limita chamadas por IP/sessão) — pra não estourar o proxy de LLM.
- Mostra a resposta da Marina e renderiza o boleto (botão de PDF, copiar linha digitável / PIX).

---

## 4. O que eu preciso de vocês (resumo)

1. **URL** do endpoint da Marina (a que o site vai chamar).
2. **Como autenticar** (nome do header + token). Ex.: `Authorization: Bearer xxx` ou `x-api-key: xxx`.
3. **Formato do request** que a Marina aceita (campos).
4. **Formato da response** (onde vem o texto e onde vem o boleto/linha digitável/PDF).
5. Confirmar como a Marina trata **CPF inválido / não encontrado / sem fatura em aberto**.
6. (Se houver) **limite de requisições** / concorrência do lado de vocês.

> 👉 **O ideal:** se conseguirem expor **exatamente** o contrato da seção 5, eu ligo "plug-and-play". Se a Marina **já tem** um endpoint com formato diferente, **me mandem o formato real** (1 exemplo de request + 1 de response que funcionam) que eu adapto o site pra ele.

---

## 5. Contrato proposto (o ideal pro site)

### 5.1 Request — site → Marina

```http
POST {URL_DA_MARINA}
Content-Type: application/json
Authorization: Bearer {TOKEN}
```
```json
{
  "cpf": "12345678900",
  "message": "Quero a 2ª via do meu boleto",
  "session_id": "a1b2c3d4-...",
  "channel": "site-boletos"
}
```

| Campo | Tipo | Descrição |
|---|---|---|
| `cpf` | string | Só dígitos (11). O site já limpa máscara. |
| `message` | string | Texto que o cliente digitou. |
| `session_id` | string | UUID por conversa — pra Marina manter contexto/histórico (se usar). |
| `channel` | string | Fixo `"site-boletos"` — pra vocês saberem a origem. |

### 5.2 Response — Marina → site (HTTP 200)

```json
{
  "reply": "Achei sua fatura, Philipe! Vence dia 10/01. Segue a 2ª via 👇",
  "session_id": "a1b2c3d4-...",
  "boletos": [
    {
      "descricao": "Mensalidade Jan/2026",
      "vencimento": "2026-01-10",
      "valor": "99.90",
      "status": "aberto",
      "linha_digitavel": "34191.79001 01043.510047 91020.150008 1 99990000009990",
      "pix_copia_cola": "00020126...br.gov.bcb.pix...",
      "url_pdf": "https://.../boleto/abc123.pdf"
    }
  ],
  "done": false
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `reply` | **sim** | Texto da Marina pra mostrar no chat. |
| `session_id` | sim | Ecoa o recebido (ou cria, se vier vazio). |
| `boletos` | não | Lista; **só quando** a Marina gerar/encontrar. Vazio/ausente quando ainda está conversando. |
| `boletos[].url_pdf` | desejável | Link da 2ª via / PDF (o site vira um botão "Baixar boleto"). |
| `boletos[].linha_digitavel` | desejável | Pro botão "copiar". |
| `boletos[].pix_copia_cola` | opcional | Se tiverem PIX, melhor ainda. |
| `done` | opcional | `true` quando o atendimento encerrou. |

> Pode mandar **só `reply`** nas mensagens de conversa e incluir `boletos[]` só na hora que gerar. O site lida com os dois casos.

### 5.3 Erros (HTTP 4xx/5xx)

```json
{ "error": "CPF não encontrado na base", "code": "CPF_NOT_FOUND" }
```
Códigos que ajudam o site a tratar: `INVALID_CPF`, `CPF_NOT_FOUND`, `NO_OPEN_INVOICE`, `RATE_LIMITED`, `INTERNAL`.
(Se preferirem devolver tudo em HTTP 200 com `reply` explicando o erro, também funciona — só me digam qual abordagem.)

### 5.4 Sessão / histórico

- A Marina mantém o histórico por `session_id`, ou é **stateless** (cada request é independente)?
- Se for stateless e precisarem do histórico, o site pode mandar as últimas N mensagens junto — **me digam** se querem isso e em que campo.

---

## 6. Segurança (importante — por favor leiam)

1. **A validação de quem é o dono do CPF fica com a Marina.** O site confia que a Marina só devolve boleto **do CPF informado**. Garantam que não dá pra puxar boleto de terceiros.
2. **⚠️ CPF sozinho é um identificador fraco** (não é segredo). Como vocês vão devolver dado pessoal/financeiro (nome, valor, vencimento) a partir de um CPF, recomendo fortemente **uma** destas proteções:
   - **Mandar o boleto pro contato cadastrado** (e-mail/WhatsApp do cliente no IXC) em vez de exibir tudo na tela; ou
   - pedir um **2º dado** (data de nascimento ou nº do contrato) antes de liberar.
   - Se vocês decidirem liberar só com CPF, tudo bem — mas que seja **decisão consciente de vocês** (é o lado que tem o dado). O site vai aplicar rate-limit e log, mas isso não substitui a validação.
3. **Token:** definam um token só pra essa integração (não reusar o do proxy LLM). O site guarda server-side.
4. **Allowlist (opcional):** se quiserem, restrinjam o endpoint ao **IP do servidor do site** — me digam e eu confirmo o IP de saída.

---

## 7. Teste de aceite

Quando o endpoint estiver pronto, este `curl` tem que funcionar (rodando do servidor do site):

```bash
curl -s -X POST "{URL_DA_MARINA}" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {TOKEN}" \
  -d '{"cpf":"<CPF_DE_TESTE>","message":"quero meu boleto","session_id":"teste-123","channel":"site-boletos"}' \
  --max-time 60
```
Esperado: HTTP 200 com `reply` (e, se o CPF de teste tiver fatura, `boletos[]` com `url_pdf` ou `linha_digitavel`).

---

## 8. Checklist — me devolvam isto

- [ ] **URL** do endpoint da Marina: `_______________________`
- [ ] **Header de auth + token**: `_______________________`
- [ ] Aceita os campos `cpf`, `message`, `session_id`, `channel`? (ou me digam os nomes reais)
- [ ] A response traz `reply` + `boletos[]` com `url_pdf` / `linha_digitavel`? (ou me mandem 1 exemplo real de response)
- [ ] Marina é **stateful** (guarda histórico por `session_id`) ou **stateless**?
- [ ] Como trata **CPF inválido / não encontrado / sem fatura**?
- [ ] Tem **limite de requisições** que eu deva respeitar?
- [ ] Decisão de segurança sobre **CPF-only** (item 6.2): liberar na tela, mandar pro contato cadastrado, ou pedir 2º dado?
- [ ] Querem **allowlist** do IP do site? (se sim, te passo o IP)

---

> Com a URL + token + o formato (ou um exemplo real de request/response), eu finalizo o `api/marina.php` e o chat na página de boletos do lado do site. Qualquer formato que a Marina já use, eu adapto — só preciso ver o que ela espera e o que ela devolve.
