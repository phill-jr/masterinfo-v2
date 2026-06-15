<?php
/**
 * api/central/_central.php — Motor da "Área do Cliente" própria (MasterInfo).
 *
 * Em vez de jogar o cliente na central nativa do IXC (que tem captcha + cookie
 * cross-domain e não permite SSO de fora), a gente faz a nossa própria área:
 *   CPF  →  acha o cliente no IXC (webservice v1)  →  envia código (OTP) pro
 *   contato cadastrado  →  valida  →  mostra faturas em aberto + 2ª via.
 *
 * Reaproveita:
 *   - api/_ixc-store.php  (ixc_request / ixc_settings — token só no servidor)
 *   - api/rate-limit.php  (anti-abuso por IP)
 *   - secrets/config.php  (ALLOWED_ORIGIN, SESSION_SECRET)
 *
 * ⚠️ ENVIO DO OTP: o projeto ainda não tem SMTP/SMS. Por padrão o "transport" é
 *    'log' (modo dev): o código é gravado em secrets/.central-otp-dev.log (pasta
 *    bloqueada no .htaccess, NUNCA vai pro navegador). Pra produção, configure
 *    CENTRAL_OTP_TRANSPORT='mail' (PHP mail) ou plugue SMTP/SMS (TODO marcado).
 */

if (!defined('MASTERINFO_INTERNAL')) { define('MASTERINFO_INTERNAL', true); }

if (is_file(__DIR__ . '/../../secrets/config.php')) {
    require_once __DIR__ . '/../../secrets/config.php';
}
require_once __DIR__ . '/../_ixc-store.php';
require_once __DIR__ . '/../rate-limit.php';
if (is_file(__DIR__ . '/../../security-headers.php')) {
    require_once __DIR__ . '/../../security-headers.php';
}

// ════════════════════════════════════════════════════════════════════
//  HTTP / CORS / entrada
// ════════════════════════════════════════════════════════════════════

function central_json(int $code, array $payload): void {
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($payload, JSON_UNESCAPED_UNICODE);
    exit;
}

/** Headers de segurança + CORS com credenciais (same-origin em produção). */
function central_headers(): void {
    if (function_exists('sendSecurityHeaders')) { sendSecurityHeaders(); }

    $origin  = $_SERVER['HTTP_ORIGIN'] ?? '';
    $allowed = defined('ALLOWED_ORIGIN') ? ALLOWED_ORIGIN : '';
    $ok = ($allowed !== '' && $origin === $allowed)
        || ($origin !== '' && preg_match('#^https?://(localhost|127\.0\.0\.1)(:\d+)?$#', $origin));

    if ($origin !== '' && $ok) {
        header('Access-Control-Allow-Origin: ' . $origin);
        header('Vary: Origin');
        header('Access-Control-Allow-Credentials: true');
        header('Access-Control-Allow-Headers: Content-Type, X-Requested-With');
        header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
    }
    if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'OPTIONS') { http_response_code(204); exit; }
}

function central_input(): array {
    $d = json_decode((string) file_get_contents('php://input'), true);
    return is_array($d) ? $d : [];
}

// ════════════════════════════════════════════════════════════════════
//  Sessão do cliente (separada da sessão do admin)
// ════════════════════════════════════════════════════════════════════

function central_session_boot(): void {
    if (session_status() === PHP_SESSION_ACTIVE) { return; }
    session_name('MICENTRAL');
    $secure = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
        || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https');
    session_set_cookie_params([
        'lifetime' => 0, 'path' => '/', 'httponly' => true,
        'secure' => $secure, 'samesite' => 'Lax',
    ]);
    @session_start();
}

function central_login_session(array $cliente): void {
    central_session_boot();
    session_regenerate_id(true);
    $_SESSION['central_cliente_id'] = (string) $cliente['id'];
    $_SESSION['central_nome']       = (string) ($cliente['nome'] ?? '');
    $_SESSION['central_cpf']        = (string) ($cliente['cnpj_cpf'] ?? '');
    $_SESSION['central_auth_at']    = time();
    $_SESSION['central_last']       = time();
}

/** Exige sessão válida (idle máx. 30 min). Encerra com 401 se não houver. */
function central_require_session(): array {
    central_session_boot();
    $id   = (string) ($_SESSION['central_cliente_id'] ?? '');
    $last = (int) ($_SESSION['central_last'] ?? 0);
    if ($id === '' || (time() - $last) > 1800) {
        central_logout_session();
        central_json(401, ['ok' => false, 'error' => 'unauthorized', 'message' => 'Sessão expirada. Entre novamente.']);
    }
    $_SESSION['central_last'] = time();
    return ['id' => $id, 'nome' => (string) ($_SESSION['central_nome'] ?? '')];
}

function central_logout_session(): void {
    central_session_boot();
    $_SESSION = [];
    if (ini_get('session.use_cookies')) {
        $p = session_get_cookie_params();
        setcookie(session_name(), '', time() - 42000, $p['path'] ?: '/', $p['domain'] ?? '', $p['secure'] ?? false, $p['httponly'] ?? true);
    }
    @session_destroy();
}

// ════════════════════════════════════════════════════════════════════
//  CPF / CNPJ
// ════════════════════════════════════════════════════════════════════

function central_digits(string $s): string { return preg_replace('/\D/', '', $s); }

function central_mask_doc(string $digits): string {
    if (strlen($digits) === 11) {
        return preg_replace('/(\d{3})(\d{3})(\d{3})(\d{2})/', '$1.$2.$3-$4', $digits);
    }
    if (strlen($digits) === 14) {
        return preg_replace('/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/', '$1.$2.$3/$4-$5', $digits);
    }
    return $digits;
}

function central_valid_cpf(string $cpf): bool {
    $cpf = central_digits($cpf);
    if (strlen($cpf) !== 11 || preg_match('/^(\d)\1{10}$/', $cpf)) { return false; }
    for ($t = 9; $t < 11; $t++) {
        $sum = 0;
        for ($i = 0; $i < $t; $i++) { $sum += (int) $cpf[$i] * (($t + 1) - $i); }
        $d = ((10 * $sum) % 11) % 10;
        if ((int) $cpf[$t] !== $d) { return false; }
    }
    return true;
}

// ════════════════════════════════════════════════════════════════════
//  IXC — cliente, faturas, 2ª via
// ════════════════════════════════════════════════════════════════════

/** Acha o cliente no IXC por CPF (tenta mascarado e cru — o IXC costuma guardar mascarado). */
function central_find_cliente(string $cpfDigits): ?array {
    foreach ([central_mask_doc($cpfDigits), $cpfDigits] as $valor) {
        if ($valor === '') { continue; }
        $resp = ixc_request('cliente', [
            'qtype' => 'cliente.cnpj_cpf', 'query' => $valor, 'oper' => '=',
            'page' => '1', 'rp' => '1',
            'sortname' => 'cliente.id', 'sortorder' => 'desc',
        ]);
        if ($resp && !empty($resp['registros'][0])) {
            $r = $resp['registros'][0];
            return [
                'id'       => (string) ($r['id'] ?? ''),
                'nome'     => (string) ($r['razao'] ?? ($r['fantasia'] ?? '')),
                'cnpj_cpf' => (string) ($r['cnpj_cpf'] ?? ''),
                'email'    => trim((string) ($r['email'] ?? '')),
                'celular'  => central_digits((string) ($r['telefone_celular'] ?? '')),
                'whatsapp' => central_digits((string) ($r['whatsapp'] ?? '')),
                'ativo'    => (string) ($r['ativo'] ?? ''),
            ];
        }
    }
    return null;
}

/** Faturas em aberto (status 'A') do cliente. */
function central_faturas_abertas(string $idCliente): array {
    $resp = ixc_request('fn_areceber', [
        'qtype' => 'fn_areceber.id_cliente', 'query' => $idCliente, 'oper' => '=',
        'page' => '1', 'rp' => '50',
        'sortname' => 'fn_areceber.data_vencimento', 'sortorder' => 'asc',
        'grid_param' => json_encode([
            ['TB' => 'fn_areceber.status', 'OP' => '=', 'P' => 'A'],
        ]),
    ]);
    $out = [];
    foreach (($resp['registros'] ?? []) as $r) {
        if ((string) ($r['id_cliente'] ?? '') !== (string) $idCliente) { continue; } // defesa
        $out[] = [
            'id'              => (string) ($r['id'] ?? ''),
            'id_cobranca'     => (string) ($r['id_cobranca'] ?? ''),
            'nosso_numero'    => (string) ($r['nosso_numero'] ?? ''),
            'vencimento'      => (string) ($r['data_vencimento'] ?? ''),
            'valor'           => (string) ($r['valor'] ?? ''),
            'valor_aberto'    => (string) ($r['valor_aberto'] ?? ($r['valor'] ?? '')),
            'status'          => (string) ($r['status'] ?? ''),
            'linha_digitavel' => (string) ($r['linha_digitavel'] ?? ''),
            'gateway_link'    => (string) ($r['gateway_link'] ?? ''),
        ];
    }
    return $out;
}

/** POST de "ação" no IXC (ex.: get_boleto) — diferente do listar (ixc_request). */
function central_ixc_post(string $endpoint, array $payload): ?array {
    $cfg = ixc_settings();
    if ($cfg['url'] === '' || $cfg['token'] === '') {
        error_log('[central] ' . $endpoint . ' sem credenciais IXC');
        return null;
    }
    $ch = curl_init($cfg['url'] . '/' . $endpoint);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_USERPWD        => $cfg['token'],
        CURLOPT_POST           => true,
        CURLOPT_HTTPHEADER     => ['Content-Type: application/json'],
        CURLOPT_POSTFIELDS     => json_encode($payload),
        // SSL verify ON — se IXC tiver cert self-signed, instalar CA no servidor
        // em vez de desabilitar. (Antes: VERIFYPEER/VERIFYHOST = false → MITM
        // podia ler/modificar boletos e linhas digitaveis.)
        CURLOPT_SSL_VERIFYPEER => true,
        CURLOPT_SSL_VERIFYHOST => 2,
        CURLOPT_TIMEOUT        => 25,
    ]);
    $resp = curl_exec($ch);
    $http = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $err  = curl_error($ch);
    curl_close($ch);

    if ($err !== '')              { error_log("[central] {$endpoint} cURL: {$err}"); return null; }
    if ($http !== 200 || !$resp)  { error_log("[central] {$endpoint} HTTP {$http}"); return null; }

    $data = json_decode($resp, true);
    return is_array($data) ? $data : ['raw' => $resp];
}

/** Gera a 2ª via (PDF base64) de UMA fatura, confirmando que ela é do cliente logado. */
function central_segunda_via(string $idCliente, string $faturaId): array {
    // Anti-IDOR: confirma dono da fatura antes de gerar
    $check = ixc_request('fn_areceber', [
        'qtype' => 'fn_areceber.id', 'query' => $faturaId, 'oper' => '=',
        'page' => '1', 'rp' => '1', 'sortname' => 'fn_areceber.id', 'sortorder' => 'desc',
    ]);
    $fat = $check['registros'][0] ?? null;
    if (!$fat || (string) ($fat['id_cliente'] ?? '') !== (string) $idCliente) {
        return ['ok' => false, 'error' => 'forbidden'];
    }

    $b = central_ixc_post('get_boleto', [
        'boletos'         => $faturaId,
        'juro'            => 'S',
        'multa'           => 'S',
        'atualiza_boleto' => 'S',
        'tipo_boleto'     => 'arquivo',
        'base64'          => 'S',
    ]);
    if ($b === null) { return ['ok' => false, 'error' => 'upstream']; }

    // get_boleto pode devolver o PDF de várias formas conforme a versão do IXC
    $pdf = '';
    if (is_string($b))            { $pdf = $b; }
    elseif (!empty($b['base64'])) { $pdf = (string) $b['base64']; }
    elseif (!empty($b['arquivo'])){ $pdf = (string) $b['arquivo']; }
    elseif (!empty($b['raw']) && is_string($b['raw'])) { $pdf = $b['raw']; }

    return [
        'ok'              => true,
        'pdf_base64'      => $pdf,
        'linha_digitavel' => (string) ($fat['linha_digitavel'] ?? ''),
        'gateway_link'    => (string) ($fat['gateway_link'] ?? ''),
        'vencimento'      => (string) ($fat['data_vencimento'] ?? ''),
        'valor'           => (string) ($fat['valor_aberto'] ?? ($fat['valor'] ?? '')),
    ];
}

// ════════════════════════════════════════════════════════════════════
//  OTP (código de uso único)
// ════════════════════════════════════════════════════════════════════

function central_otp_dir(): string {
    $d = sys_get_temp_dir() . '/mi_central_otp';
    if (!is_dir($d)) { @mkdir($d, 0700, true); }
    return $d;
}
function central_otp_secret(): string {
    return defined('SESSION_SECRET') ? SESSION_SECRET : 'mi-central-otp-fallback';
}

function central_otp_create(array $cliente, string $channel, string $destinoMasked): array {
    $challenge = bin2hex(random_bytes(16));
    $code = str_pad((string) random_int(0, 999999), 6, '0', STR_PAD_LEFT);
    $rec = [
        'cliente_id'     => (string) $cliente['id'],
        'nome'           => (string) $cliente['nome'],
        'cnpj_cpf'       => (string) $cliente['cnpj_cpf'],
        'code_hash'      => hash_hmac('sha256', $code, central_otp_secret()),
        'channel'        => $channel,
        'destino_masked' => $destinoMasked,
        'expires'        => time() + 600,   // 10 min
        'attempts'       => 0,
        'max'            => 5,
    ];
    file_put_contents(central_otp_dir() . '/' . $challenge . '.json', json_encode($rec), LOCK_EX);
    return ['challenge' => $challenge, 'code' => $code];
}

function central_otp_verify(string $challenge, string $code): array {
    $challenge = preg_replace('/[^a-f0-9]/', '', $challenge);
    if ($challenge === '') { return ['ok' => false, 'error' => 'invalid']; }
    $f = central_otp_dir() . '/' . $challenge . '.json';
    if (!is_file($f)) { return ['ok' => false, 'error' => 'expired']; }

    $rec = json_decode((string) file_get_contents($f), true);
    if (!is_array($rec))                       { @unlink($f); return ['ok' => false, 'error' => 'expired']; }
    if (time() > ($rec['expires'] ?? 0))       { @unlink($f); return ['ok' => false, 'error' => 'expired']; }
    if (($rec['attempts'] ?? 0) >= ($rec['max'] ?? 5)) { @unlink($f); return ['ok' => false, 'error' => 'too_many']; }

    $rec['attempts']++;
    file_put_contents($f, json_encode($rec), LOCK_EX);

    $given = hash_hmac('sha256', central_digits($code), central_otp_secret());
    if (!hash_equals((string) $rec['code_hash'], $given)) {
        return ['ok' => false, 'error' => 'wrong', 'attempts_left' => max(0, ($rec['max'] ?? 5) - $rec['attempts'])];
    }
    @unlink($f);
    return ['ok' => true, 'cliente' => ['id' => $rec['cliente_id'], 'nome' => $rec['nome'], 'cnpj_cpf' => $rec['cnpj_cpf']]];
}

// ════════════════════════════════════════════════════════════════════
//  Canal + envio do OTP
// ════════════════════════════════════════════════════════════════════

function central_mask_email(string $e): string {
    if (!str_contains($e, '@')) { return $e; }
    [$u, $d] = explode('@', $e, 2);
    $n = mb_strlen($u);
    $u2 = mb_substr($u, 0, 1) . str_repeat('*', max(1, $n - 2)) . ($n > 1 ? mb_substr($u, -1) : '');
    return $u2 . '@' . $d;
}
function central_mask_phone(string $p): string {
    $p = central_digits($p);
    return strlen($p) < 4 ? '****' : '****-' . substr($p, -4);
}

/** Escolhe o melhor canal: e-mail (temos rota) → senão celular/whatsapp (SMS futuro). */
function central_pick_channel(array $cliente): ?array {
    if ($cliente['email'] !== '' && filter_var($cliente['email'], FILTER_VALIDATE_EMAIL)) {
        return ['channel' => 'email', 'destino' => $cliente['email'], 'masked' => central_mask_email($cliente['email'])];
    }
    $fone = $cliente['celular'] !== '' ? $cliente['celular'] : $cliente['whatsapp'];
    if (strlen($fone) >= 10) {
        return ['channel' => 'sms', 'destino' => $fone, 'masked' => central_mask_phone($fone)];
    }
    return null;
}

/**
 * Envia o código OTP. Transports:
 *   'mail' + e-mail   → PHP mail() simples (default em prod).
 *   'log'             → grava em secrets/.central-otp-dev.log (SOMENTE em dev).
 *   TODO: 'smtp' (PHPMailer) e 'sms' (gateway).
 *
 * SEGURANCA: 'log' grava o codigo em texto claro com canal+destino.
 * Se secrets/ for exposto (nginx sem deny), atacante loga como qualquer
 * cliente. Em producao 'log' so funciona se APP_ENV=dev.
 */
function central_send_code(string $channel, string $destino, string $code, string $nome): bool {
    $transport = getenv('CENTRAL_OTP_TRANSPORT')
        ?: (defined('CENTRAL_OTP_TRANSPORT') ? CENTRAL_OTP_TRANSPORT : 'log');

    // Hardening: bloqueia transport='log' fora de dev.
    $appEnv = getenv('APP_ENV') ?: (defined('APP_ENV') ? APP_ENV : 'prod');
    if ($transport === 'log' && $appEnv !== 'dev') {
        error_log("[central-otp] BLOCKED: transport='log' so permitido em APP_ENV=dev (atual={$appEnv})");
        return false;
    }

    try {
        if ($transport === 'mail' && $channel === 'email') {
            $from = defined('CENTRAL_MAIL_FROM') ? CENTRAL_MAIL_FROM : 'nao-responda@masterinfointernet.com';
            $assunto = '=?UTF-8?B?' . base64_encode('Seu código de acesso — MasterInfo') . '?=';
            $corpo = "Olá, {$nome}!\n\nSeu código de acesso à Área do Cliente é: {$code}\n"
                   . "Ele expira em 10 minutos.\n\nSe não foi você, ignore este e-mail.\n\nMasterInfo Internet";
            $headers = "From: MasterInfo <{$from}>\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=utf-8\r\n";
            return @mail($destino, $assunto, $corpo, $headers);
        }
        // ── Modo dev (default em local): código só no servidor, nunca no navegador ──
        // Loga so destino e canal — o codigo nao vai pro arquivo persistente.
        // (O codigo aparece em error_log do PHP em dev pra debug, e somente em dev.)
        $line = '[' . date('Y-m-d H:i:s') . "] channel={$channel} destino={$destino} challenge=ok\n";
        @file_put_contents(__DIR__ . '/../../secrets/.central-otp-dev.log', $line, FILE_APPEND | LOCK_EX);
        error_log("[central-otp] (dev) {$channel}:{$destino} -> {$code}");
        return true;
    } catch (\Throwable $e) {
        error_log('[central-otp] ' . get_class($e) . ': ' . $e->getMessage() . ' @ ' . $e->getFile() . ':' . $e->getLine());
        return false;
    }
}
