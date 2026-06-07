<?php
/**
 * POST /api/central/auth-verify.php  — body { challenge, code }
 * Valida o OTP e abre a sessão do cliente.
 */
define('MASTERINFO_INTERNAL', true);
require_once __DIR__ . '/_central.php';

central_headers();
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    central_json(405, ['ok' => false, 'error' => 'method', 'message' => 'Método não permitido.']);
}

checkRateLimit('central-auth-verify', 20, 600);

$in        = central_input();
$challenge = (string) ($in['challenge'] ?? '');
$code      = central_digits((string) ($in['code'] ?? ''));

if (strlen($code) !== 6) {
    central_json(422, ['ok' => false, 'error' => 'INVALID_CODE', 'message' => 'Digite o código de 6 dígitos.']);
}

try {
    $r = central_otp_verify($challenge, $code);
    if (!$r['ok']) {
        $map = [
            'expired'  => ['Código expirado. Peça um novo.', 410],
            'too_many' => ['Muitas tentativas. Peça um novo código.', 429],
            'wrong'    => ['Código incorreto.', 401],
            'invalid'  => ['Requisição inválida.', 400],
        ];
        [$msg, $http] = $map[$r['error']] ?? ['Código inválido.', 401];
        central_json($http, ['ok' => false, 'error' => $r['error'],
            'attempts_left' => $r['attempts_left'] ?? null, 'message' => $msg]);
    }

    central_login_session($r['cliente']);
    central_json(200, ['ok' => true, 'cliente' => ['nome' => $r['cliente']['nome']], 'message' => 'Acesso liberado!']);
} catch (\Throwable $e) {
    error_log('[central/auth-verify] ' . get_class($e) . ': ' . $e->getMessage() . ' @ ' . $e->getFile() . ':' . $e->getLine());
    central_json(500, ['ok' => false, 'error' => 'internal', 'message' => 'Erro interno.']);
}
