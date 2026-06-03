<?php
/**
 * MasterInfo - API de Checkout
 * Recebe pedido completo e envia para Bitrix24 CRM
 * POST JSON → crm.contact.add + crm.deal.add
 */

require_once __DIR__ . '/../security-headers.php';
require_once __DIR__ . '/rate-limit.php';

sendSecurityHeaders();

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: ' . (defined('ALLOWED_ORIGIN') ? ALLOWED_ORIGIN : '*'));
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'mensagem' => 'Método não permitido.']);
    exit;
}

// Rate limiting: 10 pedidos/hora por IP
checkRateLimit('checkout', 10, 3600);

require_once __DIR__ . '/../secrets/config.php';

// Helpers compartilhados: normalização de telefone (+55 E.164) e store da jornada.
if (!defined('MASTERINFO_INTERNAL')) define('MASTERINFO_INTERNAL', true);
require_once __DIR__ . '/admin/_bitrix-helper.php';
require_once __DIR__ . '/_journey-store.php';
if (!defined('BITRIX_CATEGORY')) define('BITRIX_CATEGORY', 0);     // funil Comercial (default)
if (!defined('BITRIX_STAGE')) define('BITRIX_STAGE', 'NEW');       // etapa inicial (default)

// ─── Receber dados ───
$input = json_decode(file_get_contents('php://input'), true);

if (!$input) {
    http_response_code(400);
    echo json_encode(['success' => false, 'mensagem' => 'Dados inválidos.']);
    exit;
}

// ─── Validação ───
$required = ['nome', 'cpf', 'whatsapp', 'email', 'plano_nome', 'plano_valor', 'cep', 'numero'];
foreach ($required as $field) {
    if (empty($input[$field])) {
        echo json_encode(['success' => false, 'mensagem' => "Campo obrigatório ausente: $field"]);
        exit;
    }
}

// Validar CPF (mod11)
$cpf = preg_replace('/\D/', '', $input['cpf']);
if (strlen($cpf) !== 11 || !validaCPF($cpf)) {
    echo json_encode(['success' => false, 'mensagem' => 'CPF inválido.']);
    exit;
}

// Validar email
if (!filter_var($input['email'], FILTER_VALIDATE_EMAIL)) {
    echo json_encode(['success' => false, 'mensagem' => 'E-mail inválido.']);
    exit;
}

// ─── Gerar número do pedido ───
$pedido = 'MI-' . date('Y') . '-' . str_pad(mt_rand(1, 99999), 5, '0', STR_PAD_LEFT);

// ─── Montar dados formatados ───
$nome = trim($input['nome']);
$phone = preg_replace('/\D/', '', $input['whatsapp']);
$phoneE164 = bx_normalize_phone_br($phone); // +55 (E.164) p/ casar a dedup com o número do WhatsApp
$email = trim($input['email']);

// Endereço completo
$endereco = trim(($input['logradouro'] ?? '') . ', ' . ($input['numero'] ?? ''));
if (!empty($input['complemento'])) $endereco .= ' - ' . $input['complemento'];
$endereco .= ' - ' . ($input['bairro'] ?? '') . ', ' . ($input['cidade'] ?? '') . '/' . ($input['uf'] ?? '');
$endereco .= ' - CEP: ' . ($input['cep'] ?? '');

// Addons formatados
$addons_text = '';
$addons = $input['addons'] ?? [];
if (!empty($addons)) {
    $addon_lines = [];
    foreach ($addons as $addon) {
        $line = '• ' . $addon['nome'] . ': R$ ' . number_format($addon['valor'], 2, ',', '.');
        if (!empty($addon['instalacao']) && $addon['instalacao'] > 0) {
            $line .= ' + R$ ' . number_format($addon['instalacao'], 2, ',', '.') . ' instalação';
        }
        $addon_lines[] = $line;
    }
    $addons_text = implode("\n", $addon_lines);
}

// Comentários do deal
$comments = "CHECKOUT SITE MASTERINFO\n";
$comments .= "========================\n\n";
$comments .= "📋 Pedido: $pedido\n";
$comments .= "📅 Data: " . date('d/m/Y H:i') . "\n\n";
$comments .= "── PLANO ──\n";
$comments .= $input['plano_nome'] . "\n";
$comments .= "Mensal: R$ " . number_format($input['plano_valor'], 2, ',', '.') . "\n\n";

if ($addons_text) {
    $comments .= "── EXTRAS ──\n$addons_text\n\n";
}

$comments .= "── TOTAIS ──\n";
$comments .= "Total mensal: R$ " . number_format($input['total_mensal'] ?? 0, 2, ',', '.') . "\n";
if (!empty($input['total_instalacao']) && $input['total_instalacao'] > 0) {
    $comments .= "Instalação: R$ " . number_format($input['total_instalacao'], 2, ',', '.') . "\n";
}
$comments .= "\n";

$comments .= "── CLIENTE ──\n";
$comments .= "Nome: $nome\n";
$comments .= "CPF: " . formatCPF($cpf) . "\n";
$comments .= "Nascimento: " . ($input['nascimento'] ?? '') . "\n";
if (!empty($input['rg'])) $comments .= "RG: " . $input['rg'] . "\n";
$comments .= "WhatsApp: " . formatPhone($phone) . "\n";
$comments .= "E-mail: $email\n\n";

$comments .= "── ENDEREÇO ──\n";
$comments .= "$endereco\n";
if (!empty($input['referencia'])) $comments .= "Referência: " . $input['referencia'] . "\n";
if (!empty($input['cto_nome'])) $comments .= "\n── CTO ──\n" . $input['cto_nome'] . "\n";

// ─── Enviar para Bitrix24 ───
$deal_id = null;

if (!empty(BITRIX_WEBHOOK)) {
    try {
        // 1. Buscar contato existente (telefone normalizado p/ casar com o WhatsApp)
        $contact_id = findBitrixContact($phoneE164, $email);

        // 2. Criar contato se não existir
        if (!$contact_id) {
            $contact_id = createBitrixContact($nome, $phoneE164, $email, $endereco);
        }

        // 3. Criar deal
        if ($contact_id) {
            $deal_title = "Checkout Site - {$input['plano_nome']} - $nome";
            $deal_id = createBitrixDeal($deal_title, $contact_id, $input['total_mensal'] ?? 0, $comments);
        }

        // 4. Jornada do cliente → comentário de timeline no Negócio + store por telefone
        $jornada = trim((string) ($input['jornada'] ?? ''));
        if ($jornada !== '') {
            if ($deal_id) {
                try {
                    bitrixRequest('crm.timeline.comment.add.json', ['fields' => [
                        'ENTITY_ID' => (int) $deal_id, 'ENTITY_TYPE' => 'deal', 'COMMENT' => $jornada,
                    ]]);
                } catch (\Throwable $e) { error_log('[MasterInfo Checkout] timeline: ' . $e->getMessage()); }
            }
            try { journey_save($phoneE164, $jornada); } catch (\Throwable $e) {}
        }
    } catch (\Throwable $e) {
        error_log('[MasterInfo Checkout] Bitrix24 error: ' . $e->getMessage());
        // Não falha o checkout por erro do CRM
    }
}

// ─── Log do pedido ───
error_log("[MasterInfo Checkout] Pedido $pedido criado. Deal ID: " . ($deal_id ?: 'N/A'));

// ─── Resposta ───
echo json_encode([
    'success' => true,
    'pedido' => $pedido,
    'deal_id' => $deal_id,
    'mensagem' => 'Pedido registrado com sucesso!',
]);

// ═══════════════════════════════════════════
// Funções auxiliares
// ═══════════════════════════════════════════

function bitrixRequest($method, $data = []) {
    $url = rtrim(BITRIX_WEBHOOK, '/') . '/' . $method;

    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => json_encode($data),
        CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 30,
        CURLOPT_SSL_VERIFYPEER => true,
    ]);

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);

    if ($error) {
        throw new Exception("Curl error: $error");
    }

    $body = json_decode($response, true);

    if ($httpCode !== 200 || isset($body['error'])) {
        $msg = $body['error_description'] ?? $body['error'] ?? 'Unknown error';
        throw new Exception("Bitrix24: $msg");
    }

    return $body;
}

function findBitrixContact($phone, $email) {
    // Busca por telefone
    try {
        $res = bitrixRequest('crm.duplicate.findbycomm.json', [
            'type' => 'PHONE',
            'values' => [$phone],
            'entity_type' => 'CONTACT',
        ]);
        if (!empty($res['result']['CONTACT'])) {
            return (int) $res['result']['CONTACT'][0];
        }
    } catch (Exception $e) {
        // ignora e tenta por email
    }

    // Busca por email
    try {
        $res = bitrixRequest('crm.duplicate.findbycomm.json', [
            'type' => 'EMAIL',
            'values' => [$email],
            'entity_type' => 'CONTACT',
        ]);
        if (!empty($res['result']['CONTACT'])) {
            return (int) $res['result']['CONTACT'][0];
        }
    } catch (Exception $e) {
        // ignora
    }

    return null;
}

function createBitrixContact($nome, $phone, $email, $endereco) {
    $parts = explode(' ', trim($nome));
    $firstName = $parts[0];
    $lastName = count($parts) > 1 ? implode(' ', array_slice($parts, 1)) : '';

    $res = bitrixRequest('crm.contact.add.json', [
        'fields' => [
            'NAME' => $firstName,
            'LAST_NAME' => $lastName,
            'PHONE' => [['VALUE' => $phone, 'VALUE_TYPE' => 'MOBILE']],
            'EMAIL' => [['VALUE' => $email, 'VALUE_TYPE' => 'WORK']],
            'ADDRESS' => $endereco,
            'SOURCE_ID' => 'WEB',
            'OPENED' => 'Y',
        ],
    ]);

    return $res['result'] ?? null;
}

function createBitrixDeal($title, $contactId, $opportunity, $comments) {
    $res = bitrixRequest('crm.deal.add.json', [
        'fields' => [
            'TITLE' => $title,
            'CATEGORY_ID' => BITRIX_CATEGORY,
            'STAGE_ID' => BITRIX_STAGE,
            'CONTACT_ID' => $contactId,
            'SOURCE_ID' => 'WEB',
            'OPPORTUNITY' => $opportunity,
            'CURRENCY_ID' => 'BRL',
            'COMMENTS' => $comments,
            'OPENED' => 'Y',
        ],
        'params' => [
            'REGISTER_SONET_EVENT' => 'Y',
        ],
    ]);

    return $res['result'] ?? null;
}

function validaCPF($cpf) {
    if (preg_match('/^(\d)\1{10}$/', $cpf)) return false;

    $soma = 0;
    for ($i = 0; $i < 9; $i++) $soma += (int)$cpf[$i] * (10 - $i);
    $resto = 11 - ($soma % 11);
    $d1 = $resto >= 10 ? 0 : $resto;
    if ((int)$cpf[9] !== $d1) return false;

    $soma = 0;
    for ($i = 0; $i < 10; $i++) $soma += (int)$cpf[$i] * (11 - $i);
    $resto = 11 - ($soma % 11);
    $d2 = $resto >= 10 ? 0 : $resto;
    return (int)$cpf[10] === $d2;
}

function formatCPF($cpf) {
    return substr($cpf, 0, 3) . '.' . substr($cpf, 3, 3) . '.' . substr($cpf, 6, 3) . '-' . substr($cpf, 9);
}

function formatPhone($phone) {
    if (strlen($phone) === 11) {
        return '(' . substr($phone, 0, 2) . ') ' . substr($phone, 2, 5) . '-' . substr($phone, 7);
    }
    return '(' . substr($phone, 0, 2) . ') ' . substr($phone, 2, 4) . '-' . substr($phone, 6);
}
