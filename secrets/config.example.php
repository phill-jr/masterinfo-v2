<?php
/**
 * MasterInfo — Config de segredos (EXEMPLO)
 *
 * COMO USAR:
 *   1. Copie este arquivo para "config.php" na mesma pasta (secrets/)
 *   2. Substitua os valores abaixo pelos reais
 *   3. NÃO commite o config.php (já está no .gitignore)
 */

// ─── Bitrix24 ───
// Webhook de ENTRADA gerado em: Aplicativos > Desenvolvedores > Webhook de entrada
// Precisa ter permissão CRM marcada.
define('BITRIX_WEBHOOK', 'https://SEU.bitrix24.com.br/rest/USER_ID/TOKEN_AQUI/');

// Segredo que protege o endpoint api/bitrix-dedupe.php (chamado pela regra de
// automação "Webhook" do Bitrix no evento "Lead criado"). Gere com: bin2hex(random_bytes(16)).
define('BITRIX_DEDUPE_SECRET', 'TROCAR_POR_RANDOM_HEX');

// Origem permitida (CORS) — domínio público do site
define('ALLOWED_ORIGIN', 'https://www.masterinfointernet.com');

// ─── Segurança ───
// Token forte aleatório (gere com: bin2hex(random_bytes(32)) )
define('SESSION_SECRET', 'TROCAR_POR_RANDOM_32_BYTES_HEX');

// ─── Marina (Sync Hub) — chat de boletos ───
// Endpoint do agente Marina (Sync) e token da integração.
define('MARINA_URL', 'https://sync.masterinfointernet.com/api/marina/boletos');
// site_boletos_token gerado no painel do Sync (Integrações → "Marina Boletos").
// Alternativa: variável de ambiente MARINA_TOKEN (tem prioridade sobre esta constante).
define('MARINA_TOKEN', 'COLE_O_TOKEN_DO_SYNC_AQUI');

// ─── IXC — Verificação de cobertura/viabilidade ───
// RECOMENDADO: configure pelo PAINEL ADMIN (aba Cobertura → "Integração IXC").
// O admin grava em secrets/ixc.php (fora do git, token só no servidor).
// As constantes abaixo são OPCIONAIS — só servem de fallback se o store não existir.
// Prioridade: variável de ambiente > secrets/ixc.php (admin) > estas constantes.
// define('IXC_URL', 'https://SEU-IXC.com.br/webservice/v1');
// define('IXC_TOKEN', 'ID:TOKEN');          // formato usuario:token (Basic Auth do IXC)
// define('VIABILIDADE_RAIO_METROS', 300);   // raio (m) de busca da caixa FTTH mais próxima
