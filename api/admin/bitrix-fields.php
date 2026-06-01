<?php
/**
 * GET /api/admin/bitrix-fields.php?entity=deal
 * Lista campos do Bitrix (padrão + UF_CRM customizados) + apelidos amigáveis salvos.
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
checkRateLimit('bitrix-fields', 60, 60);

$entity = $_GET['entity'] ?? 'deal';
$method = match ($entity) {
    'lead'    => 'crm.lead.fields.json',
    'contact' => 'crm.contact.fields.json',
    default   => 'crm.deal.fields.json',
};

try {
    $r = bx_request($method);
    $fields = $r['result'] ?? [];

    $mapping = bx_load_mapping();
    $labels  = $mapping['field_labels'] ?? [];

    $out = [];
    foreach ($fields as $key => $meta) {
        $isCustom = strpos($key, 'UF_CRM_') === 0;
        $title    = $meta['title'] ?? '';
        // Se vier vazio ou igual ao próprio ID, considera "sem título"
        if ($title === '' || $title === $key) $title = null;

        $out[] = [
            'id'        => $key,
            'title'     => $title,
            'alias'     => $labels[$key] ?? null, // apelido amigável salvo no painel
            'type'      => $meta['type'] ?? 'string',
            'required'  => (bool) ($meta['isRequired'] ?? false),
            'readonly'  => (bool) ($meta['isReadOnly'] ?? false),
            'multiple'  => (bool) ($meta['isMultiple'] ?? false),
            'is_custom' => $isCustom,
        ];
    }

    // Ordena: customizados sem alias por último, com alias em cima
    usort($out, function ($a, $b) {
        $sa = ($a['alias'] ? 0 : 2) + ($a['is_custom'] ? 1 : 0);
        $sb = ($b['alias'] ? 0 : 2) + ($b['is_custom'] ? 1 : 0);
        if ($sa !== $sb) return $sa <=> $sb;
        return strcasecmp($a['alias'] ?? $a['title'] ?? $a['id'], $b['alias'] ?? $b['title'] ?? $b['id']);
    });

    echo json_encode([
        'ok'     => true,
        'entity' => $entity,
        'count'  => count($out),
        'fields' => $out,
    ]);
} catch (Exception $e) {
    http_response_code(502);
    echo json_encode(['ok' => false, 'error' => $e->getMessage()]);
}
