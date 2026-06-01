<?php
/**
 * GET /api/admin/bitrix-categories.php?entity=deal
 * Lista funis (categorias) do Bitrix pra entidade (deal por padrão).
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
checkRateLimit('bitrix-cats', 60, 60);

$entity = $_GET['entity'] ?? 'deal';
$entityTypeId = $entity === 'lead' ? 1 : 2; // 1=Lead, 2=Deal

try {
    $r = bx_request('crm.category.list.json', ['entityTypeId' => $entityTypeId]);
    $cats = $r['result']['categories'] ?? [];
    $out = array_map(fn($c) => [
        'id'        => (int) $c['id'],
        'name'      => $c['name'],
        'isDefault' => ($c['isDefault'] ?? 'N') === 'Y',
        'sort'      => (int) ($c['sort'] ?? 0),
    ], $cats);
    usort($out, fn($a, $b) => $a['sort'] <=> $b['sort']);
    echo json_encode(['ok' => true, 'categories' => $out]);
} catch (Exception $e) {
    http_response_code(502);
    echo json_encode(['ok' => false, 'error' => $e->getMessage()]);
}
