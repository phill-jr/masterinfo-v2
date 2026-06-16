<?php
/**
 * GET /api/admin/bitrix-sources.php
 * Lista as origens (SOURCE_ID) cadastradas no Bitrix24 — alimenta o select
 * "Origem do lead" de cada formulário no painel admin (aba Bitrix).
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
checkRateLimit('bitrix-sources', 60, 60);

try {
    // No Bitrix, as origens de lead/negócio ficam no crm.status com ENTITY_ID = SOURCE.
    $r = bx_request('crm.status.list.json', [
        'filter' => ['ENTITY_ID' => 'SOURCE'],
        'order'  => ['SORT' => 'ASC'],
    ]);

    $sources = array_map(fn($s) => [
        'status_id' => $s['STATUS_ID'],
        'name'      => $s['NAME'],
        'sort'      => (int) ($s['SORT'] ?? 0),
    ], $r['result'] ?? []);

    echo json_encode(['ok' => true, 'sources' => $sources]);
} catch (Exception $e) {
    http_response_code(502);
    echo json_encode(['ok' => false, 'error' => $e->getMessage()]);
}
