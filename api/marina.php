<?php
/**
 * /api/marina.php  — ponte entre o chat de boletos do site e o agente Marina (Sync Hub).
 *
 *   GET  → status público { enabled, configured }   (o chat usa pra aparecer/sumir)
 *   POST → repassa a conversa pra Marina (guarda o token; rate-limit; valida CPF)
 *
 * Config (enabled / endpoint / token) vem do store server-side (secrets/marina.php),
 * gerenciado pelo painel admin. Token NUNCA é exposto ao navegador.
 */
define('MASTERINFO_INTERNAL', true);

if (file_exists(__DIR__ . '/../secrets/config.php')) {
    require_once __DIR__ . '/../secrets/config.php';
}
require_once __DIR__ . '/rate-limit.php';
require_once __DIR__ . '/_marina-store.php';
if (file_exists(__DIR__ . '/../security-headers.php')) {
    require_once __DIR__ . '/../security-headers.php';
    if (function_exists('sendSecurityHeaders')) { sendSecurityHeaders(); }
}

header('Content-Type: application/json; charset=utf-8');

$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
if ($method === 'OPTIONS') { http_response_code(204); exit; }

$cfg = marina_settings();

// ─── GET: status (sem segredo) — o chat decide se aparece ───
if ($method === 'GET') {
    echo json_encode([
        'enabled'    => $cfg['enabled'],
        'configured' => ($cfg['endpoint'] !== '' && $cfg['token'] !== ''),
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

if ($method !== 'POST') {
    http_response_code(405);
    echo json_encode(['reply' => 'Método não permitido.', 'error' => 'method']);
    exit;
}

// ─── Habilitado? (defesa em profundidade — o chat já se esconde no front) ───
if (!$cfg['enabled']) {
    http_response_code(403);
    echo json_encode([
        'reply' => 'O atendimento de boletos está temporariamente indisponível. Fale com a gente no WhatsApp 👉',
        'error' => 'disabled',
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

if ($cfg['endpoint'] === '' || $cfg['token'] === '') {
    error_log('[marina] endpoint/token não configurados (painel admin → Atendimento Marina).');
    http_response_code(503);
    echo json_encode([
        'reply' => 'O atendimento de boletos está sendo configurado. Por enquanto, fale com a gente no WhatsApp 👉',
        'error' => 'not_configured',
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

// ─── Anti-abuso: 25 mensagens / 10 min por IP ───
checkRateLimit('marina-boletos', 25, 600);

$input = json_decode(file_get_contents('php://input'), true);
if (!is_array($input)) {
    http_response_code(400);
    echo json_encode(['reply' => 'Requisição inválida.', 'error' => 'bad_request']);
    exit;
}

$cpf       = preg_replace('/\D/', '', (string) ($input['cpf'] ?? ''));
$message   = trim((string) ($input['message'] ?? ''));
$sessionId = preg_replace('/[^A-Za-z0-9\-]/', '', (string) ($input['session_id'] ?? ''));
if ($sessionId === '') { $sessionId = bin2hex(random_bytes(8)); }

// Valida só o FORMATO do CPF (11 dígitos). Quem valida dono/existência é a Marina (IXC).
if (strlen($cpf) !== 11) {
    http_response_code(422);
    echo json_encode([
        'reply'      => 'Pra localizar seu boleto, me informe um CPF válido (11 dígitos), por favor.',
        'error'      => 'INVALID_CPF',
        'session_id' => $sessionId,
    ], JSON_UNESCAPED_UNICODE);
    exit;
}
if ($message === '') { $message = 'quero meu boleto'; }
if (mb_strlen($message) > 1000) { $message = mb_substr($message, 0, 1000); }

$payload = json_encode([
    'cpf'        => $cpf,
    'message'    => $message,
    'session_id' => $sessionId,
    'channel'    => 'site-boletos',
], JSON_UNESCAPED_UNICODE);

try {
    // Marina às vezes responde 5xx transitório — tentamos até 2x antes de desistir.
    $body = false; $httpCode = 0; $curlErr = '';
    for ($attempt = 1; $attempt <= 2; $attempt++) {
        $ch = curl_init($cfg['endpoint']);
        curl_setopt_array($ch, [
            CURLOPT_POST           => true,
            CURLOPT_POSTFIELDS     => $payload,
            CURLOPT_HTTPHEADER     => [
                'Content-Type: application/json',
                'Authorization: Bearer ' . $cfg['token'],
            ],
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT        => 60,
            CURLOPT_CONNECTTIMEOUT => 10,
        ]);
        $body     = curl_exec($ch);
        $httpCode = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curlErr  = curl_error($ch);
        curl_close($ch);

        // Loga só ERROS da Marina (5xx / falha de conexão). Não loga sucesso = não vaza dado do cliente.
        if ($httpCode >= 500 || $curlErr !== '') {
            error_log('[marina] upstream erro: attempt=' . $attempt . ' http=' . $httpCode . ' err=' . $curlErr . ' body=' . substr((string) $body, 0, 300));
        }

        // Para no sucesso ou em erro <500 (4xx é definitivo). Só re-tenta em 5xx / falha de conexão.
        if ($body !== false && $curlErr === '' && $httpCode > 0 && $httpCode < 500) { break; }
        if ($attempt < 2) { usleep(900000); } // 0,9s antes de re-tentar
    }

    if ($body === false || $curlErr !== '') {
        error_log('[marina] cURL falhou: ' . $curlErr);
        http_response_code(502);
        echo json_encode([
            'reply'      => 'Não consegui falar com o atendimento agora. Tenta de novo em instantes ou chama no WhatsApp 👉',
            'error'      => 'upstream',
            'session_id' => $sessionId,
        ], JSON_UNESCAPED_UNICODE);
        exit;
    }

    $decoded = json_decode($body, true);
    if (!is_array($decoded)) {
        error_log('[marina] resposta nao-JSON da Marina (HTTP ' . $httpCode . '): ' . substr((string) $body, 0, 300));
        http_response_code(502);
        echo json_encode([
            'reply'      => 'Recebi uma resposta inesperada do atendimento. Tenta de novo ou chama no WhatsApp 👉',
            'error'      => 'bad_upstream',
            'session_id' => $sessionId,
        ], JSON_UNESCAPED_UNICODE);
        exit;
    }

    if (empty($decoded['session_id'])) { $decoded['session_id'] = $sessionId; }
    // Se a Marina respondeu erro (>=400) sem um 'reply' utilizável, garante uma mensagem amigável
    // (evita o "Não recebi resposta" sem contexto no chat).
    if ($httpCode >= 400 && empty($decoded['reply'])) {
        $decoded['reply'] = 'O atendimento teve um erro momentâneo. Tenta de novo em instantes ou chama no WhatsApp 👉';
    }
    http_response_code($httpCode ?: 200);
    echo json_encode($decoded, JSON_UNESCAPED_UNICODE);
} catch (\Throwable $e) {
    error_log('[marina] ' . get_class($e) . ': ' . $e->getMessage() . ' @ ' . $e->getFile() . ':' . $e->getLine());
    http_response_code(500);
    echo json_encode([
        'reply'      => 'Tive um erro interno aqui. Pode tentar pelo WhatsApp, por favor? 👉',
        'error'      => 'internal',
        'session_id' => $sessionId,
    ], JSON_UNESCAPED_UNICODE);
}
