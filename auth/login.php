<?php
/**
 * MasterInfo - Endpoint de Login
 * POST: { usuario: "...", senha: "..." } → { ok: true } ou { error: "..." }
 */

require_once __DIR__ . '/session.php';
require_once __DIR__ . '/credentials.php';

header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Metodo nao permitido']);
    exit;
}

// ─── Rate limiting: 5 tentativas / 15 min por IP ───
$ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$rateFile = sys_get_temp_dir() . '/mi_login_' . md5($ip);
$rateData = file_exists($rateFile)
    ? json_decode(file_get_contents($rateFile), true)
    : ['count' => 0, 'reset' => time() + 900];

if (time() > ($rateData['reset'] ?? 0)) {
    $rateData = ['count' => 0, 'reset' => time() + 900];
}

if ($rateData['count'] >= 5) {
    $wait = max(1, ($rateData['reset'] ?? time()) - time());
    http_response_code(429);
    echo json_encode(['error' => "Muitas tentativas. Aguarde {$wait} segundos."]);
    exit;
}

// ─── Validar credenciais ───
$input = json_decode(file_get_contents('php://input'), true);
$user = trim($input['usuario'] ?? '');
$pass = $input['senha'] ?? '';

// Hash do usuario informado (null se nao existir). Usamos um hash dummy quando
// nao existe para que password_verify rode sempre e o tempo de resposta nao
// vaze quais usuarios sao validos (mitiga user enumeration por timing).
$storedHash = ADMIN_USERS[$user] ?? null;
$verifyHash = $storedHash ?? '$2y$12$0000000000000000000000000000000000000000000000000000u';

if ($storedHash === null || !password_verify($pass, $verifyHash)) {
    $rateData['count']++;
    file_put_contents($rateFile, json_encode($rateData), LOCK_EX);

    // Delay para dificultar brute force
    sleep(1);

    http_response_code(401);
    echo json_encode(['error' => 'Usuario ou senha invalidos']);
    exit;
}

// ─── Sucesso: iniciar sessao ───
file_put_contents($rateFile, json_encode(['count' => 0, 'reset' => time() + 900]), LOCK_EX);

if (session_status() === PHP_SESSION_NONE) session_start();
session_regenerate_id(true);

$_SESSION['admin_authenticated'] = true;
$_SESSION['admin_ip'] = $ip;
$_SESSION['admin_user'] = $user;
$_SESSION['last_regeneration'] = time();
$_SESSION['last_activity'] = time();
$_SESSION['csrf_token'] = bin2hex(random_bytes(32));

echo json_encode(['ok' => true]);
