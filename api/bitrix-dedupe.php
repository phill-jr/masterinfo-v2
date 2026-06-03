<?php
/**
 * POST /api/bitrix-dedupe.php?secret=XXX[&dryrun=1]
 *
 * Chamado por uma regra de automação do Bitrix (ação "Webhook") no evento
 * "Lead criado". Procura leads com o MESMO telefone (normalizado +55) e mescla
 * os duplicados, mantendo o lead MAIS ANTIGO (menor ID) como master.
 *
 * Corpo aceito (configure o webhook do Bitrix pra mandar o ID do lead):
 *   - JSON  { "lead_id": 123 }   (ou { "ID": 123 })
 *   - form  data[FIELDS][ID]=123 (formato do evento ONCRMLEADADD)
 *   - query ?lead_id=123
 *
 * ?dryrun=1 → só LOGA o que mesclaria, NÃO mescla (use no rollout/teste).
 *
 * ⚠️ Merge é IRREVERSÍVEL. Conservador: só match exato de telefone, master = mais antigo.
 */
define('MASTERINFO_INTERNAL', true);
require_once __DIR__ . '/../security-headers.php';
require_once __DIR__ . '/rate-limit.php';
require_once __DIR__ . '/admin/_bitrix-helper.php'; // bx_request + bx_normalize_phone_br + secrets/config.php

sendSecurityHeaders();
header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'Método não permitido']);
    exit;
}

// ─── Auth por segredo compartilhado (comparação em tempo constante) ───
$secret = (string) ($_GET['secret'] ?? $_POST['secret'] ?? '');
if (!defined('BITRIX_DEDUPE_SECRET') || BITRIX_DEDUPE_SECRET === '' || !hash_equals(BITRIX_DEDUPE_SECRET, $secret)) {
    http_response_code(403);
    echo json_encode(['ok' => false, 'error' => 'Segredo inválido']);
    exit;
}

// Rate limit: 120 chamadas/min por IP (o robô do Bitrix pode disparar em rajada)
checkRateLimit('bitrix-dedupe', 120, 60);

$dryrun = !empty($_GET['dryrun']);

// ─── Descobrir o ID do lead recém-criado ───
$body = json_decode(file_get_contents('php://input'), true);
$leadId = 0;
if (is_array($body)) {
    $leadId = (int) ($body['lead_id'] ?? $body['ID'] ?? ($body['data']['FIELDS']['ID'] ?? 0));
}
if (!$leadId && isset($_POST['data']['FIELDS']['ID'])) {
    $leadId = (int) $_POST['data']['FIELDS']['ID'];
}
if (!$leadId && isset($_GET['lead_id'])) {
    $leadId = (int) $_GET['lead_id'];
}
if ($leadId <= 0) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'lead_id ausente no payload']);
    exit;
}

try {
    // ─── Telefone do lead novo → normalizado ───
    $lead = bx_request('crm.lead.get.json', ['id' => $leadId]);
    $rawPhone = $lead['result']['PHONE'][0]['VALUE'] ?? '';
    $fone = $rawPhone !== '' ? bx_normalize_phone_br((string) $rawPhone) : '';
    if ($fone === '') {
        echo json_encode(['ok' => true, 'skipped' => 'lead sem telefone', 'lead_id' => $leadId]);
        exit;
    }

    // ─── Leads com o MESMO telefone ───
    $dup = bx_request('crm.duplicate.findbycomm.json', [
        'type'        => 'PHONE',
        'values'      => [$fone],
        'entity_type' => 'LEAD',
    ]);
    $ids = array_values(array_unique(array_filter(array_map('intval', $dup['result']['LEAD'] ?? []))));
    sort($ids); // menor ID = mais antigo = master (precisa ser o 1º do entityIds)

    if (count($ids) < 2) {
        echo json_encode(['ok' => true, 'phone' => $fone, 'found' => count($ids), 'merged' => []]);
        exit;
    }

    $master = $ids[0];
    $merged = array_slice($ids, 1);

    if ($dryrun) {
        error_log("[bitrix-dedupe][DRYRUN] phone={$fone} master={$master} merge=" . implode(',', $merged));
        echo json_encode(['ok' => true, 'dryrun' => true, 'phone' => $fone, 'master' => $master, 'would_merge' => $merged]);
        exit;
    }

    // ─── Mescla (entityTypeId 1 = Lead). Master = primeiro ID do array. ───
    $resp   = bx_request('crm.entity.mergeBatch.json', [
        'params' => ['entityTypeId' => 1, 'entityIds' => $ids],
    ]);
    $status = $resp['result']['STATUS'] ?? 'UNKNOWN';
    error_log("[bitrix-dedupe] phone={$fone} master={$master} merged=" . implode(',', $merged) . " status={$status}");
    echo json_encode([
        'ok'     => true,
        'phone'  => $fone,
        'master' => $master,
        'merged' => $merged,
        'status' => $status,
    ]);
} catch (\Throwable $e) {
    error_log('[bitrix-dedupe] ' . get_class($e) . ': ' . $e->getMessage() . ' @ ' . $e->getFile() . ':' . $e->getLine());
    http_response_code(502);
    echo json_encode(['ok' => false, 'error' => $e->getMessage()]);
}
