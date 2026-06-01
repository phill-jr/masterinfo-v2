<?php
/**
 * GET /api/admin/bitrix-test.php
 * Testa a conexão com o Bitrix24 (chama profile.json).
 * Requer sessão admin.
 */
define('MASTERINFO_INTERNAL', true);
require_once __DIR__ . '/../../auth/session.php';
require_once __DIR__ . '/../../security-headers.php';
require_once __DIR__ . '/../rate-limit.php';
require_once __DIR__ . '/_bitrix-helper.php';

sendSecurityHeaders();
header('Content-Type: application/json; charset=utf-8');
requireAdminSession();
checkRateLimit('bitrix-test', 30, 60);

try {
    $r = bx_request('profile.json');
    $u = $r['result'] ?? [];
    echo json_encode([
        'ok'    => true,
        'user'  => trim(($u['NAME'] ?? '') . ' ' . ($u['LAST_NAME'] ?? '')),
        'id'    => $u['ID'] ?? null,
        'admin' => $u['ADMIN'] ?? false,
    ]);
} catch (Exception $e) {
    http_response_code(502);
    echo json_encode(['ok' => false, 'error' => $e->getMessage()]);
}
