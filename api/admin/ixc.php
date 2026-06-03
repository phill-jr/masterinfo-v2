<?php
/**
 * GET  /api/admin/ixc.php → status { enabled, url, raio_metros, id_cidade, has_token }  (NUNCA devolve o token)
 * POST /api/admin/ixc.php → salva { enabled, url, token, raio_metros, id_cidade }        (requer sessão admin + CSRF)
 * POST {action:'test', url?, token?} → testa a conexão com o IXC SEM salvar.
 *
 * Token vai pro store server-side (secrets/ixc.php). Token vazio no POST = MANTÉM o atual
 * (assim o admin edita o resto sem redigitar o token).
 */
define('MASTERINFO_INTERNAL', true);
require_once __DIR__ . '/../../auth/session.php';
require_once __DIR__ . '/../../auth/csrf.php';
require_once __DIR__ . '/../../security-headers.php';
require_once __DIR__ . '/../rate-limit.php';
require_once __DIR__ . '/../_ixc-store.php';

sendSecurityHeaders();
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-CSRF-Token');
header('Access-Control-Allow-Credentials: true');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }

requireAdminSession();

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    checkRateLimit('ixc-admin-get', 120, 60);
    $s = ixc_settings();
    echo json_encode([
        'ok'          => true,
        'enabled'     => $s['enabled'],
        'url'         => $s['url'],
        'raio_metros' => $s['raio_metros'],
        'id_cidade'   => $s['id_cidade'],
        'has_token'   => $s['token'] !== '',
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkRateLimit('ixc-admin-post', 30, 60);

    $csrf = $_SERVER['HTTP_X_CSRF_TOKEN'] ?? '';
    if (!validateCsrfToken($csrf)) {
        http_response_code(403);
        echo json_encode(['ok' => false, 'error' => 'CSRF inválido. Recarregue a página.']);
        exit;
    }

    $data = json_decode(file_get_contents('php://input'), true);
    if (!is_array($data)) {
        http_response_code(400);
        echo json_encode(['ok' => false, 'error' => 'JSON inválido']);
        exit;
    }

    $current = ixc_settings();

    // Token: vazio = mantém o atual; preenchido = substitui.
    $postedToken = isset($data['token']) ? trim((string) $data['token']) : '';
    $token = $postedToken !== '' ? $postedToken : $current['token'];

    $url = isset($data['url']) ? trim((string) $data['url']) : $current['url'];
    if ($url !== '' && !preg_match('#^https?://#i', $url)) {
        http_response_code(400);
        echo json_encode(['ok' => false, 'error' => 'A URL do IXC deve começar com http:// ou https://']);
        exit;
    }

    $idCidade = isset($data['id_cidade']) ? trim((string) $data['id_cidade']) : $current['id_cidade'];

    // ─── Ação: testar conexão (não salva) ───
    if (($data['action'] ?? '') === 'test') {
        if ($url === '' || $token === '') {
            http_response_code(422);
            echo json_encode(['ok' => false, 'error' => 'Informe a URL e o token pra testar (ou salve um token antes).']);
            exit;
        }
        $resp = ixc_request('rad_caixa_ftth', [
            'qtype' => 'rad_caixa_ftth.id', 'query' => '0', 'oper' => '>',
            'page'  => '1', 'rp' => '1',
        ], ['url' => $url, 'token' => $token]);
        if ($resp === null) {
            echo json_encode(['ok' => false, 'error' => 'Não conectou no IXC. Verifique a URL, o token e se o IP do servidor está liberado no IXC.']);
            exit;
        }
        echo json_encode([
            'ok'           => true,
            'test'         => true,
            'total_caixas' => (int) ($resp['total'] ?? 0),
            'message'      => 'Conexão OK! O IXC respondeu.',
        ], JSON_UNESCAPED_UNICODE);
        exit;
    }

    $raio = (int) ($data['raio_metros'] ?? $current['raio_metros']);
    if ($raio < 50 || $raio > 5000) {
        http_response_code(422);
        echo json_encode(['ok' => false, 'error' => 'O raio de busca deve ficar entre 50 e 5000 metros.']);
        exit;
    }

    $enabled = !empty($data['enabled']);

    // Não deixa ativar sem url + token + cidade (evita checagem quebrada no ar).
    if ($enabled && ($url === '' || $token === '' || $idCidade === '')) {
        http_response_code(422);
        echo json_encode(['ok' => false, 'error' => 'Pra ativar a verificação, informe a URL, o token e o ID da cidade.']);
        exit;
    }

    if (!ixc_save([
        'enabled'     => $enabled,
        'url'         => $url,
        'token'       => $token,
        'raio_metros' => $raio,
        'id_cidade'   => $idCidade,
    ])) {
        http_response_code(500);
        echo json_encode(['ok' => false, 'error' => 'Falha ao salvar a configuração.']);
        exit;
    }

    echo json_encode([
        'ok'          => true,
        'enabled'     => $enabled,
        'url'         => $url,
        'raio_metros' => $raio,
        'id_cidade'   => $idCidade,
        'has_token'   => $token !== '',
        'saved_at'    => date('c'),
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

http_response_code(405);
echo json_encode(['ok' => false, 'error' => 'Método não permitido']);
