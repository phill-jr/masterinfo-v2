<?php
/**
 * MasterInfo - API de Checkout
 * Recebe pedido completo e envia para Bitrix24 CRM
 * POST JSON → crm.contact.add + crm.deal.add
 */

// secrets/config.php define ALLOWED_ORIGIN — precisa carregar ANTES dos headers.
require_once __DIR__ . '/../secrets/config.php';
require_once __DIR__ . '/../security-headers.php';
require_once __DIR__ . '/rate-limit.php';

sendSecurityHeaders();

header('Content-Type: application/json; charset=utf-8');
// CORS fail-closed: se ALLOWED_ORIGIN nao foi definido (config faltando ou typo),
// emite 'null' em vez de '*'. Antes era wildcard fallback → spam de leads cross-origin.
if (defined('ALLOWED_ORIGIN')) {
    header('Access-Control-Allow-Origin: ' . ALLOWED_ORIGIN);
} else {
    header('Access-Control-Allow-Origin: null');
}
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

// Helpers compartilhados do Bitrix (request, dedup, contato/deal, timeline, normalização).
if (!defined('MASTERINFO_INTERNAL')) define('MASTERINFO_INTERNAL', true);
require_once __DIR__ . '/admin/_bitrix-helper.php';
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
        http_response_code(400);
        echo json_encode(['success' => false, 'mensagem' => "Campo obrigatório ausente: $field"]);
        exit;
    }
}

// Validar CPF (mod11)
$cpf = preg_replace('/\D/', '', $input['cpf']);
if (strlen($cpf) !== 11 || !validaCPF($cpf)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'mensagem' => 'CPF inválido.']);
    exit;
}

// Validar email
if (!filter_var($input['email'], FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'mensagem' => 'E-mail inválido.']);
    exit;
}

// ─── Gerar número do pedido ───
$pedido = 'MI-' . date('Y') . '-' . str_pad(random_int(1, 99999), 5, '0', STR_PAD_LEFT);

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
        // 1. Contato (dedup por telefone normalizado + email) → cria se não existir
        $contact_id = bx_find_contact($phoneE164, $email);
        if (!$contact_id) {
            $contact_id = bx_create_contact($nome, $phoneE164, $email, $endereco);
        }

        // 2. Negócio vinculado ao contato
        if ($contact_id) {
            $deal_title = "Checkout Site - {$input['plano_nome']} - $nome";
            $deal_id = bx_create_deal($deal_title, $contact_id, $input['total_mensal'] ?? 0, $comments, BITRIX_CATEGORY, BITRIX_STAGE);
        }

        // 3. Jornada → comentário de timeline NO NEGÓCIO recém-criado (sanitizada).
        //    NÃO faz journey_save: o deal já existe aqui; a automação de "Negócio criado"
        //    pegaria do store e duplicaria o comentário.
        $jornada = mb_substr(strip_tags(trim((string) ($input['jornada'] ?? ''))), 0, 2000);
        if ($jornada !== '' && $deal_id) {
            bx_timeline_comment((int) $deal_id, 'deal', $jornada);
        }

        // 4. fbclid / _fbp / gclid → campos do Negócio (p/ o CAPI do Sync Hub mandar fbc/fbp no Purchase
        //    e atribuição do Google Ads).
        //    gclid: ATIVO POR PADRÃO — o campo UF_CRM_GCLID já existe no Bitrix (criado pelo Sync Hub,
        //    userfield id 3608), então a atribuição do Google Ads NÃO depende de config na produção.
        //    secrets/config.php pode sobrescrever o nome do campo se necessário. fbclid/_fbp continuam
        //    OPT-IN (nomes de campo do Meta não são estáveis): defina BITRIX_UF_FBCLID / BITRIX_UF_FBP
        //    em secrets/config.php (ex.: define('BITRIX_UF_FBCLID', 'UF_CRM_1700000000');) para ligá-los.
        if (!defined('BITRIX_UF_GCLID'))  define('BITRIX_UF_GCLID', 'UF_CRM_GCLID');
        if (!defined('BITRIX_UF_FBCLID')) define('BITRIX_UF_FBCLID', 'UF_CRM_FBCLID');
        if (!defined('BITRIX_UF_FBP'))    define('BITRIX_UF_FBP', 'UF_CRM_FBP');
        if ($deal_id && (defined('BITRIX_UF_FBCLID') || defined('BITRIX_UF_FBP') || defined('BITRIX_UF_GCLID'))) {
            $ufFields = [];
            if (defined('BITRIX_UF_FBCLID') && !empty($input['fbclid'])) $ufFields[BITRIX_UF_FBCLID] = bx_sanitize_text((string) $input['fbclid'], 255);
            if (defined('BITRIX_UF_FBP') && !empty($input['fbp']))       $ufFields[BITRIX_UF_FBP]    = bx_sanitize_text((string) $input['fbp'], 255);
            if (defined('BITRIX_UF_GCLID') && !empty($input['gclid']))   $ufFields[BITRIX_UF_GCLID]  = bx_sanitize_text((string) $input['gclid'], 512);
            if ($ufFields) bx_request('crm.deal.update.json', ['id' => $deal_id, 'fields' => $ufFields]);
        }
    } catch (\Throwable $e) {
        error_log('[MasterInfo Checkout] Bitrix24 error: ' . get_class($e) . ': ' . $e->getMessage() . ' @ ' . $e->getFile() . ':' . $e->getLine());
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

// bitrixRequest/findBitrixContact/createBitrixContact/createBitrixDeal foram movidas pro
// api/admin/_bitrix-helper.php → bx_request / bx_find_contact / bx_create_contact / bx_create_deal.

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
