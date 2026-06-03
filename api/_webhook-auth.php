<?php
/**
 * Auth + parse compartilhado dos webhooks de automação do Bitrix
 * (api/bitrix-dedupe.php, api/bitrix-deal-journey.php).
 *
 * Valida o segredo, rate-limita e extrai o ID da entidade. Encerra a request em falha.
 * Segredo aceito por: corpo JSON `secret` (RECOMENDADO) > header `X-Webhook-Secret` >
 * `?secret=` (fallback — vaza em logs de acesso do nginx/Cloudflare; evite).
 */
if (!defined('MASTERINFO_INTERNAL')) { http_response_code(403); exit('Forbidden'); }

function webhook_auth_and_parse(string $rateKey, string $idField): int {
    $body = json_decode(file_get_contents('php://input'), true);
    if (!is_array($body)) $body = [];

    $secret = '';
    if (isset($body['secret']) && $body['secret'] !== '') $secret = (string) $body['secret'];
    elseif (!empty($_SERVER['HTTP_X_WEBHOOK_SECRET']))     $secret = (string) $_SERVER['HTTP_X_WEBHOOK_SECRET'];
    elseif (isset($_GET['secret']))                        $secret = (string) $_GET['secret'];

    if (!defined('BITRIX_DEDUPE_SECRET') || BITRIX_DEDUPE_SECRET === '' || !hash_equals(BITRIX_DEDUPE_SECRET, $secret)) {
        http_response_code(403);
        echo json_encode(['ok' => false, 'error' => 'Segredo inválido']);
        exit;
    }

    if (function_exists('checkRateLimit')) checkRateLimit($rateKey, 120, 60);

    $id = (int) ($body[$idField] ?? $body['ID'] ?? ($body['data']['FIELDS']['ID'] ?? 0));
    if (!$id && isset($_POST['data']['FIELDS']['ID'])) $id = (int) $_POST['data']['FIELDS']['ID'];
    if (!$id && isset($_GET[$idField]))                $id = (int) $_GET[$idField];
    if ($id <= 0) {
        http_response_code(400);
        echo json_encode(['ok' => false, 'error' => "$idField ausente no payload"]);
        exit;
    }
    return $id;
}
