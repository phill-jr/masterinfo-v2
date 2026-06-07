<?php
/**
 * POST /api/central/auth-start.php  — body { cpf }
 * Acha o cliente no IXC e dispara o código (OTP) pro contato cadastrado.
 * Resposta: { ok, challenge, channel, destino_masked, expires_in, message }
 */
define('MASTERINFO_INTERNAL', true);
require_once __DIR__ . '/_central.php';

central_headers();
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    central_json(405, ['ok' => false, 'error' => 'method', 'message' => 'Método não permitido.']);
}

// Anti-abuso: 8 pedidos de código / 10 min por IP
checkRateLimit('central-auth-start', 8, 600);

$in  = central_input();
$cpf = central_digits((string) ($in['cpf'] ?? ''));

if (!central_valid_cpf($cpf)) {
    central_json(422, ['ok' => false, 'error' => 'INVALID_CPF', 'message' => 'Informe um CPF válido (11 dígitos).']);
}

$cfg = ixc_settings();
if ($cfg['url'] === '' || $cfg['token'] === '') {
    error_log('[central/auth-start] IXC não configurado (secrets/ixc.php / IXC_URL / IXC_TOKEN).');
    central_json(503, ['ok' => false, 'error' => 'not_configured',
        'message' => 'A Área do Cliente está em configuração. Por enquanto, fale com a gente no WhatsApp.']);
}

// Resposta generica usada quando o cliente nao existe OU nao tem contato cadastrado.
// Quebra a enumeracao de CPF (antes: 404 vs 200 vs 409 vazavam o estado do cadastro).
// Operadores podem investigar pelos error_logs server-side abaixo.
$genericOk = [
    'ok'             => true,
    'challenge'      => null,           // sem challenge real - o validate-code vai negar
    'channel'        => null,
    'destino_masked' => null,
    'expires_in'     => 600,
    'message'        => 'Se houver um cadastro com esse CPF, enviamos um código de 6 dígitos para o e-mail ou celular cadastrado. Não recebeu? Fale com a gente no WhatsApp.',
];

try {
    $cli = central_find_cliente($cpf);
    if (!$cli) {
        error_log("[central/auth-start] CPF sem cadastro no IXC (mascarado em resposta): " . substr($cpf, 0, 3) . '***');
        central_json(200, $genericOk);
    }

    $ch = central_pick_channel($cli);
    if (!$ch) {
        error_log("[central/auth-start] Cliente sem e-mail/celular (id_cliente=" . ($cli['id'] ?? '?') . ")");
        central_json(200, $genericOk);
    }

    $otp  = central_otp_create($cli, $ch['channel'], $ch['masked']);
    $sent = central_send_code($ch['channel'], $ch['destino'], $otp['code'], $cli['nome']);
    if (!$sent) {
        // Aqui e erro REAL (mail/sms falhou) — sinaliza pro cliente que pode tentar de novo.
        central_json(502, ['ok' => false, 'error' => 'send_failed',
            'message' => 'Não consegui enviar o código agora. Tente de novo em instantes.']);
    }

    central_json(200, [
        'ok'             => true,
        'challenge'      => $otp['challenge'],
        'channel'        => $ch['channel'],
        'destino_masked' => $ch['masked'],
        'expires_in'     => 600,
        'message'        => 'Enviamos um código de 6 dígitos para ' .
            ($ch['channel'] === 'email' ? 'o e-mail ' : 'o celular ') . $ch['masked'] . '.',
    ]);
} catch (\Throwable $e) {
    error_log('[central/auth-start] ' . get_class($e) . ': ' . $e->getMessage() . ' @ ' . $e->getFile() . ':' . $e->getLine());
    central_json(500, ['ok' => false, 'error' => 'internal', 'message' => 'Erro interno. Tente novamente.']);
}
