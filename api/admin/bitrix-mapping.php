<?php
/**
 * GET  /api/admin/bitrix-mapping.php → retorna o JSON de mapeamento
 * POST /api/admin/bitrix-mapping.php → salva (body JSON, requer CSRF)
 *
 * Requer sessão admin.
 */
define('MASTERINFO_INTERNAL', true);
require_once __DIR__ . '/../../auth/session.php';
require_once __DIR__ . '/../../auth/csrf.php';
require_once __DIR__ . '/../../security-headers.php';
require_once __DIR__ . '/../rate-limit.php';
require_once __DIR__ . '/_bitrix-helper.php';

sendSecurityHeaders();
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-CSRF-Token');
header('Access-Control-Allow-Credentials: true');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }

requireAdminSession();

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    checkRateLimit('bitrix-map-get', 120, 60);
    echo json_encode(['ok' => true, 'mapping' => bx_load_mapping()]);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkRateLimit('bitrix-map-post', 30, 60);

    $csrf = $_SERVER['HTTP_X_CSRF_TOKEN'] ?? '';
    if (!validateCsrfToken($csrf)) {
        http_response_code(403);
        echo json_encode(['ok' => false, 'error' => 'CSRF inválido. Recarregue a página.']);
        exit;
    }

    $raw = file_get_contents('php://input');
    $data = json_decode($raw, true);
    if (!is_array($data)) {
        http_response_code(400);
        echo json_encode(['ok' => false, 'error' => 'JSON inválido']);
        exit;
    }

    // Sanitização básica
    $clean = [
        'field_labels' => [],
        'forms'        => [],
        'source_rules' => [],
    ];

    // Origem por fonte de trafego (gclid/fbclid -> SOURCE_ID). STATUS_ID ate 80 chars.
    // Preserva o existente se o POST nao enviar (defesa contra wipe — o admin sempre manda).
    if (!isset($data['source_rules'])) {
        $existing = bx_load_mapping();
        if (!empty($existing['source_rules']) && is_array($existing['source_rules'])) {
            $clean['source_rules'] = $existing['source_rules'];
        }
    } elseif (is_array($data['source_rules'])) {
        foreach (['gclid', 'fbclid', 'default'] as $sk) {
            $sv = $data['source_rules'][$sk] ?? '';
            if (is_string($sv)) $clean['source_rules'][$sk] = substr(trim($sv), 0, 80);
        }
    }

    if (isset($data['field_labels']) && is_array($data['field_labels'])) {
        foreach ($data['field_labels'] as $k => $v) {
            if (is_string($k) && is_string($v) && $v !== '') {
                $clean['field_labels'][substr($k, 0, 80)] = substr(trim($v), 0, 120);
            }
        }
    }

    if (isset($data['forms']) && is_array($data['forms'])) {
        foreach ($data['forms'] as $slug => $cfg) {
            if (!is_string($slug) || !is_array($cfg)) continue;
            $slugClean = preg_replace('/[^a-z0-9-_]/i', '', substr($slug, 0, 60));
            $clean['forms'][$slugClean] = [
                'label'        => substr((string) ($cfg['label'] ?? $slugClean), 0, 120),
                'entity'       => in_array($cfg['entity'] ?? '', ['lead', 'contact', 'deal']) ? $cfg['entity'] : 'deal',
                'category_id'  => (int) ($cfg['category_id'] ?? 0),
                'stage_id'     => substr((string) ($cfg['stage_id'] ?? 'NEW'), 0, 60),
                'source_id'    => substr((string) ($cfg['source_id'] ?? 'WEB'), 0, 30),
                'dedupe_by'    => array_values(array_intersect((array) ($cfg['dedupe_by'] ?? []), ['phone', 'email'])),
                'mappings'     => [],
                'deal_title_template' => substr((string) ($cfg['deal_title_template'] ?? ''), 0, 200),
            ];
            if (is_array($cfg['mappings'] ?? null)) {
                foreach ($cfg['mappings'] as $from => $to) {
                    if (is_string($from) && is_string($to)) {
                        $clean['forms'][$slugClean]['mappings'][substr($from, 0, 60)] = substr($to, 0, 80);
                    }
                }
            }
        }
    }

    if (bx_save_mapping($clean)) {
        echo json_encode(['ok' => true, 'saved_at' => date('c')]);
    } else {
        http_response_code(500);
        echo json_encode(['ok' => false, 'error' => 'Falha ao salvar arquivo']);
    }
    exit;
}

http_response_code(405);
echo json_encode(['ok' => false, 'error' => 'Método não permitido']);
