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
require_once __DIR__ . '/_webhook-auth.php';

sendSecurityHeaders();
header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'Método não permitido']);
    exit;
}

// Auth (segredo via body/header/query) + rate-limit + ID do negócio — compartilhado.
$dealId = webhook_auth_and_parse('bitrix-deal-journey', 'deal_id');
$dryrun = !empty($_GET['dryrun']);

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

    if (bx_timeline_comment($dealId, 'deal', $jornada)) {
        journey_del($phone);
        error_log("[deal-journey] comentário postado no negócio {$dealId} (phone {$phone})");
    }
    echo json_encode(['ok' => true, 'deal_id' => $dealId, 'phone' => $phone]);
} catch (\Throwable $e) {
    error_log('[deal-journey] ' . get_class($e) . ': ' . $e->getMessage() . ' @ ' . $e->getFile() . ':' . $e->getLine());
    http_response_code(502);
    echo json_encode(['ok' => false, 'error' => $e->getMessage()]);
}
