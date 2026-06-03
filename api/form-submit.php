<?php
/**
 * POST /api/form-submit.php
 * Endpoint PÚBLICO que recebe formulários do site e envia pro Bitrix24
 * usando o mapeamento configurado no painel admin.
 *
 * Body JSON:
 *   {
 *     "form": "pre-venda-copa",      // slug do form (configurado no admin)
 *     "data": {
 *        "nome": "...",
 *        "bairro": "...",
 *        "telefone": "...",
 *        ...
 *     }
 *   }
 *
 * Resposta:
 *   { "ok": true, "deal_id": 123 } | { "ok": false, "error": "..." }
 */
define('MASTERINFO_INTERNAL', true);
require_once __DIR__ . '/../security-headers.php';
require_once __DIR__ . '/rate-limit.php';
require_once __DIR__ . '/admin/_bitrix-helper.php';

sendSecurityHeaders();
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: ' . (defined('ALLOWED_ORIGIN') ? ALLOWED_ORIGIN : '*'));
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'Método não permitido']);
    exit;
}

// Rate limit: 20 envios/hora por IP (anti-spam)
checkRateLimit('form-submit', 20, 3600);

$input = json_decode(file_get_contents('php://input'), true);
if (!is_array($input) || empty($input['form']) || !is_array($input['data'] ?? null)) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'Payload inválido']);
    exit;
}

$slug = preg_replace('/[^a-z0-9-_]/i', '', $input['form']);
$data = $input['data'];

// Honeypot anti-bot opcional: campo "_hp" deve vir vazio
if (!empty($data['_hp'])) {
    echo json_encode(['ok' => true, 'spam' => true]);
    exit;
}

$mapping = bx_load_mapping();
$cfg = $mapping['forms'][$slug] ?? null;
if (!$cfg) {
    http_response_code(404);
    echo json_encode(['ok' => false, 'error' => "Formulário '$slug' não configurado no painel admin"]);
    exit;
}

try {
    // ─── Aplica mapeamento ───
    // Cada destino é "ENTIDADE.CAMPO" (ex: CONTACT.NAME, DEAL.TITLE, DEAL.UF_CRM_xxx)
    $contactFields = [];
    $dealFields    = [];
    $leadFields    = [];

    foreach ($cfg['mappings'] as $formField => $target) {
        if (!array_key_exists($formField, $data)) continue;
        $value = $data[$formField];
        [$dest, $field] = explode('.', $target, 2) + [null, null];
        if (!$field) continue;

        // (nao da pra retornar referencia de um match arm em PHP -> usa if/elseif)
        unset($bucket);
        if ($dest === 'CONTACT')   { $bucket = &$contactFields; }
        elseif ($dest === 'DEAL')  { $bucket = &$dealFields; }
        elseif ($dest === 'LEAD')  { $bucket = &$leadFields; }
        else { continue; }

        // PHONE/EMAIL precisam vir como array de objetos
        if ($field === 'PHONE') {
            // Normaliza p/ +55 (E.164) — sem isso a deduplicação do Bitrix não casa
            // com o número que o WhatsApp grava (ver _bitrix-helper.php).
            $bucket['PHONE'] = [['VALUE' => bx_normalize_phone_br((string) $value), 'VALUE_TYPE' => 'MOBILE']];
        } elseif ($field === 'EMAIL') {
            $bucket['EMAIL'] = [['VALUE' => $value, 'VALUE_TYPE' => 'WORK']];
        } else {
            // Concatena se mesmo campo recebe vários (ex: COMMENTS)
            if (isset($bucket[$field])) {
                $bucket[$field] .= "\n" . $value;
            } else {
                $bucket[$field] = $value;
            }
        }
    }

    // ─── Cria contato (com deduplicação) ───
    $contactId = null;
    if (!empty($cfg['dedupe_by'])) {
        if (in_array('phone', $cfg['dedupe_by']) && !empty($contactFields['PHONE'][0]['VALUE'])) {
            $r = bx_request('crm.duplicate.findbycomm.json', [
                'type'        => 'PHONE',
                'values'      => [$contactFields['PHONE'][0]['VALUE']],
                'entity_type' => 'CONTACT',
            ]);
            if (!empty($r['result']['CONTACT'])) $contactId = (int) $r['result']['CONTACT'][0];
        }
        if (!$contactId && in_array('email', $cfg['dedupe_by']) && !empty($contactFields['EMAIL'][0]['VALUE'])) {
            $r = bx_request('crm.duplicate.findbycomm.json', [
                'type'        => 'EMAIL',
                'values'      => [$contactFields['EMAIL'][0]['VALUE']],
                'entity_type' => 'CONTACT',
            ]);
            if (!empty($r['result']['CONTACT'])) $contactId = (int) $r['result']['CONTACT'][0];
        }
    }

    if (!$contactId && !empty($contactFields)) {
        // Split NAME -> NAME + LAST_NAME se vier completo
        if (!empty($contactFields['NAME']) && empty($contactFields['LAST_NAME'])) {
            $parts = preg_split('/\s+/', trim($contactFields['NAME']), 2);
            $contactFields['NAME']      = $parts[0];
            $contactFields['LAST_NAME'] = $parts[1] ?? '';
        }
        $contactFields['SOURCE_ID'] = $cfg['source_id'] ?? 'WEB';
        $contactFields['OPENED']    = 'Y';
        $r = bx_request('crm.contact.add.json', ['fields' => $contactFields]);
        $contactId = $r['result'] ?? null;
    }

    // ─── Cria deal/lead ───
    $entityId = null;
    if ($cfg['entity'] === 'deal') {
        // Título do deal (template opcional)
        if (!empty($cfg['deal_title_template'])) {
            $title = $cfg['deal_title_template'];
            foreach ($data as $k => $v) $title = str_replace('{' . $k . '}', (string) $v, $title);
            $dealFields['TITLE'] = $title;
        }
        if (empty($dealFields['TITLE'])) $dealFields['TITLE'] = $cfg['label'];
        $dealFields['CATEGORY_ID'] = $cfg['category_id'];
        $dealFields['STAGE_ID']    = $cfg['stage_id'];
        $dealFields['SOURCE_ID']   = $cfg['source_id'] ?? 'WEB';
        $dealFields['CURRENCY_ID'] = 'BRL';
        $dealFields['OPENED']      = 'Y';
        if ($contactId) $dealFields['CONTACT_ID'] = $contactId;
        $r = bx_request('crm.deal.add.json', [
            'fields' => $dealFields,
            'params' => ['REGISTER_SONET_EVENT' => 'Y'],
        ]);
        $entityId = $r['result'] ?? null;
    } elseif ($cfg['entity'] === 'lead') {
        $leadFields['TITLE']       = $cfg['label'];
        $leadFields['STATUS_ID']   = $cfg['stage_id'];
        $leadFields['SOURCE_ID']   = $cfg['source_id'] ?? 'WEB';
        $leadFields['OPENED']      = 'Y';
        if ($contactId) $leadFields['CONTACT_ID'] = $contactId; // vincula o lead ao contato criado/encontrado
        $r = bx_request('crm.lead.add.json', ['fields' => $leadFields]);
        $entityId = $r['result'] ?? null;
    }

    // ─── Jornada do cliente → comentário de timeline + store p/ propagar ao Negócio ───
    $jornada = isset($data['jornada']) ? trim((string) $data['jornada']) : '';
    if ($jornada !== '') {
        // 1) comentário na timeline da entidade recém-criada (lead/deal)
        if ($entityId && in_array($cfg['entity'], ['lead', 'deal'], true)) {
            try {
                bx_request('crm.timeline.comment.add.json', ['fields' => [
                    'ENTITY_ID'   => (int) $entityId,
                    'ENTITY_TYPE' => $cfg['entity'],
                    'COMMENT'     => $jornada,
                ]]);
            } catch (\Throwable $e) { error_log('[form-submit] timeline: ' . get_class($e) . ' ' . $e->getMessage()); }
        }
        // 2) guarda por telefone (E.164) p/ a automação postar no Negócio quando ele nascer
        $jphone = $contactFields['PHONE'][0]['VALUE'] ?? '';
        if ($jphone !== '') {
            try { require_once __DIR__ . '/_journey-store.php'; journey_save($jphone, $jornada); }
            catch (\Throwable $e) { error_log('[form-submit] journey_save: ' . $e->getMessage()); }
        }
    }

    echo json_encode([
        'ok'         => true,
        'contact_id' => $contactId,
        'entity_id'  => $entityId,
        'entity'     => $cfg['entity'],
    ]);
} catch (Exception $e) {
    error_log('[form-submit] ' . $e->getMessage());
    http_response_code(502);
    echo json_encode(['ok' => false, 'error' => $e->getMessage()]);
}
