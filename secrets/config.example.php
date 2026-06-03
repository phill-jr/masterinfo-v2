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
