<?php
/**
 * POST /api/bitrix-deal-journey.php?secret=XXX[&dryrun=1]
 *
 * Chamado por uma regra de automação do Bitrix (ação "Webhook") no evento
 * "Negócio criado". Pega o telefone do contato do negócio, busca a jornada
 * guardada no cadastro (por telefone) e posta como comentário de timeline NO
 * NEGÓCIO. Remove do store depois (1 vez só).
 *
 * Corpo: { "deal_id": 123 } | { "ID": 123 } | data[FIELDS][ID] | ?deal_id=123
 * ?dryrun=1 → só LOGA o que postaria, sem postar.
 */
define('MASTERINFO_INTERNAL', true);
require_once __DIR__ . '/../security-headers.php';
require_once __DIR__ . '/rate-limit.php';
require_once __DIR__ . '/admin/_bitrix-helper.php'; // bx_request + bx_normalize_phone_br + secrets/config.php
require_once __DIR__ . '/_journey-store.php';

sendSecurityHeaders();
header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'Método não permitido']);
    exit;
}

// ─── Auth por segredo compartilhado (mesmo da automação de dedup) ───
$secret = (string) ($_GET['secret'] ?? $_POST['secret'] ?? '');
if (!defined('BITRIX_DEDUPE_SECRET') || BITRIX_DEDUPE_SECRET === '' || !hash_equals(BITRIX_DEDUPE_SECRET, $secret)) {
    http_response_code(403);
    echo json_encode(['ok' => false, 'error' => 'Segredo inválido']);
    exit;
}

checkRateLimit('bitrix-deal-journey', 120, 60);
$dryrun = !empty($_GET['dryrun']);

// ─── ID do negócio recém-criado ───
$body = json_decode(file_get_contents('php://input'), true);
$dealId = 0;
if (is_array($body)) {
    $dealId = (int) ($body['deal_id'] ?? $body['ID'] ?? ($body['data']['FIELDS']['ID'] ?? 0));
}
if (!$dealId && isset($_POST['data']['FIELDS']['ID'])) $dealId = (int) $_POST['data']['FIELDS']['ID'];
if (!$dealId && isset($_GET['deal_id'])) $dealId = (int) $_GET['deal_id'];
if ($dealId <= 0) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'deal_id ausente no payload']);
    exit;
}

try {
    // ─── Telefone do contato do negócio → normalizado ───
    $deal = bx_request('crm.deal.get.json', ['id' => $dealId]);
    $contactId = (int) ($deal['result']['CONTACT_ID'] ?? 0);
    $phone = '';
    if ($contactId) {
        $c = bx_request('crm.contact.get.json', ['id' => $contactId]);
        $raw = $c['result']['PHONE'][0]['VALUE'] ?? '';
        if ($raw !== '') $phone = bx_normalize_phone_br((string) $raw);
    }
    if ($phone === '') {
        echo json_encode(['ok' => true, 'skipped' => 'negócio sem telefone de contato', 'deal_id' => $dealId]);
        exit;
    }

    $jornada = journey_get($phone);
    if ($jornada === '') {
        echo json_encode(['ok' => true, 'skipped' => 'sem jornada guardada p/ esse telefone', 'phone' => $phone]);
        exit;
    }

    if ($dryrun) {
        error_log("[deal-journey][DRYRUN] deal={$dealId} phone={$phone}");
        echo json_encode(['ok' => true, 'dryrun' => true, 'deal_id' => $dealId, 'phone' => $phone, 'preview' => $jornada]);
        exit;
    }

    bx_request('crm.timeline.comment.add.json', ['fields' => [
        'ENTITY_ID'   => $dealId,
        'ENTITY_TYPE' => 'deal',
        'COMMENT'     => $jornada,
    ]]);
    journey_del($phone);
    error_log("[deal-journey] comentário postado no negócio {$dealId} (phone {$phone})");
    echo json_encode(['ok' => true, 'deal_id' => $dealId, 'phone' => $phone]);
} catch (\Throwable $e) {
    error_log('[deal-journey] ' . get_class($e) . ': ' . $e->getMessage() . ' @ ' . $e->getFile() . ':' . $e->getLine());
    http_response_code(502);
    echo json_encode(['ok' => false, 'error' => $e->getMessage()]);
}
