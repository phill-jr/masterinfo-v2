<?php
/**
 * GET /api/admin/bitrix-stages.php?category_id=0&entity=deal
 * Lista etapas (status) de um funil.
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
checkRateLimit('bitrix-stages', 60, 60);

$categoryId = isset($_GET['category_id']) ? (int) $_GET['category_id'] : 0;
$entity     = $_GET['entity'] ?? 'deal';

try {
    // No Bitrix, entityId p/ DEAL_STAGE = "DEAL_STAGE_{categoryId}" (exceto categoria 0 que é "DEAL_STAGE")
    $entityId = $entity === 'lead'
        ? 'STATUS'
        : ($categoryId === 0 ? 'DEAL_STAGE' : "DEAL_STAGE_$categoryId");

    $r = bx_request('crm.status.list.json', [
        'filter' => ['ENTITY_ID' => $entityId],
        'order'  => ['SORT' => 'ASC'],
    ]);

    $stages = array_map(fn($s) => [
        'status_id' => $s['STATUS_ID'],
        'name'      => $s['NAME'],
        'sort'      => (int) ($s['SORT'] ?? 0),
    ], $r['result'] ?? []);

    echo json_encode(['ok' => true, 'category_id' => $categoryId, 'stages' => $stages]);
} catch (Exception $e) {
    http_response_code(502);
    echo json_encode(['ok' => false, 'error' => $e->getMessage()]);
}
