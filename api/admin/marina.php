<?php
/**
 * GET  /api/admin/marina.php → status { enabled, endpoint, has_token }  (NUNCA devolve o token)
 * POST /api/admin/marina.php → salva { enabled, endpoint, token }       (requer sessão admin + CSRF)
 *
 * Token vai pro store server-side (secrets/marina.php). Se o campo token vier vazio no POST,
 * o token atual é MANTIDO (não apaga) — assim o admin pode editar o resto sem redigitar o token.
 */
define('MASTERINFO_INTERNAL', true);
require_once __DIR__ . '/../../auth/session.php';
require_once __DIR__ . '/../../auth/csrf.php';
require_once __DIR__ . '/../../security-headers.php';
require_once __DIR__ . '/../rate-limit.php';
require_once __DIR__ . '/../_marina-store.php';

sendSecurityHeaders();
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-CSRF-Token');
header('Access-Control-Allow-Credentials: true');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }

requireAdminSession();

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    checkRateLimit('marina-admin-get', 120, 60);
    $s = marina_settings();
    echo json_encode([
        'ok'        => true,
        'enabled'   => $s['enabled'],
        'endpoint'  => $s['endpoint'],
        'has_token' => $s['token'] !== '',
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkRateLimit('marina-admin-post', 30, 60);

    $csrf = $_SERVER['HTTP_X_CSRF_TOKEN'] ?? '';
    if (!validateCsrfToken($csrf)) {
        http_response_code(403);
        echo json_encode(['ok' => false, 'error' => 'CSRF inválido. Recarregue a página.']);
        exit;
    }

    $data = json_decode(file_get_contents('php://input'), true);
    if (!is_array($data)) {
        http_response_code(400);
        echo json_encode(['ok' => false, 'error' => 'JSON inválido']);
        exit;
    }

    $current = marina_settings();

    // Token: vazio = mantém o atual; preenchido = substitui.
    $postedToken = isset($data['token']) ? trim((string) $data['token']) : '';
    $token = $postedToken !== '' ? $postedToken : $current['token'];

    $endpoint = isset($data['endpoint']) ? trim((string) $data['endpoint']) : $current['endpoint'];
    if ($endpoint !== '' && !preg_match('#^https?://#i', $endpoint)) {
        http_response_code(400);
        echo json_encode(['ok' => false, 'error' => 'O endpoint deve começar com http:// ou https://']);
        exit;
    }

    $enabled = !empty($data['enabled']);

    // Não deixa habilitar sem token + endpoint (evita chat quebrado no ar).
    if ($enabled && ($token === '' || $endpoint === '')) {
        http_response_code(422);
        echo json_encode(['ok' => false, 'error' => 'Pra habilitar o atendimento, informe o endpoint e o token.']);
        exit;
    }

    if (!marina_save(['enabled' => $enabled, 'endpoint' => $endpoint, 'token' => $token])) {
        http_response_code(500);
        echo json_encode(['ok' => false, 'error' => 'Falha ao salvar a configuração.']);
        exit;
    }

    echo json_encode([
        'ok'        => true,
        'enabled'   => $enabled,
        'endpoint'  => $endpoint,
        'has_token' => $token !== '',
        'saved_at'  => date('c'),
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

http_response_code(405);
echo json_encode(['ok' => false, 'error' => 'Método não permitido']);
