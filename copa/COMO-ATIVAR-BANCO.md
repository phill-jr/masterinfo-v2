# Como ativar o banco de dados dos leads (5 minutos)

Os leads da pré-venda vão cair numa **planilha do Google** (de graça, sem limite).
Faça uma vez só:

## 1. Criar a planilha
1. Abra **sheets.google.com** → **Em branco** (planilha nova).
2. Dê um nome, ex: `Leads Pré-venda Copa`.

## 2. Colar o código do banco
1. Na planilha, menu **Extensões → Apps Script**.
2. Apague o que estiver lá e cole TODO o conteúdo do arquivo **`leads-apps-script.gs`**.
3. Clique no disquete (Salvar).

## 3. Publicar como aplicativo web
1. Botão **Implantar → Nova implantação**.
2. Em "Selecionar tipo" (engrenagem) → **App da Web**.
3. Configure:
   - **Executar como:** Eu (seu e-mail)
   - **Quem pode acessar:** **Qualquer pessoa**
4. Clique **Implantar** → autorize o acesso (faz login na sua conta).
5. **Copie a URL** que aparece (termina em `/exec`).

## 4. Colar a URL no site
1. Abra o arquivo **`copa/index.html`**.
2. Procure a linha:
   ```js
   var SHEETS_ENDPOINT = '';
   ```
3. Cole a URL entre as aspas:
   ```js
   var SHEETS_ENDPOINT = 'https://script.google.com/macros/s/AAAA.../exec';
   ```
4. Salve, depois no terminal:
   ```
   git add -A
   git commit -m "ativa banco de leads da copa"
   git push
   ```

## Pronto!
Cada pessoa que preencher o formulário vira uma linha na sua planilha
(Data, Nome, Bairro, WhatsApp, Plano) **e** abre o WhatsApp com o time.

> Pra testar: abra a página `/copa/`, preencha e envie. Confira se apareceu na planilha.
> Se mudar o código `.gs` depois, refaça o passo 3 com **Implantar → Gerenciar implantações → Editar → Nova versão**.
