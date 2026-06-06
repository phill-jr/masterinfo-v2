<?php
/**
 * Store das configurações da integração IXC (verificação de cobertura/viabilidade).
 *
 * Persistido em secrets/ixc.php — arquivo .php (executa, NUNCA é servido como texto)
 * e a pasta secrets/ é bloqueada no .htaccess. O token vive só aqui, no servidor.
 *
 * Usado por:
 *   - api/viabilidade.php   (consulta pública de cobertura — lê tudo)
 *   - api/admin/ixc.php     (painel admin — lê status, salva e testa)
 */
if (!defined('MASTERINFO_INTERNAL')) { define('MASTERINFO_INTERNAL', true); }

function ixc_store_path(): string {
    return __DIR__ . '/../secrets/ixc.php';
}

/**
 * Retorna as configurações resolvidas.
 * Prioridade p/ url e token: variável de ambiente > store > constante (secrets/config.php).
 */
function ixc_settings(): array {
    $f = ixc_store_path();
    $d = is_file($f) ? @include $f : null;
    if (!is_array($d)) { $d = []; }

    $url = getenv('IXC_URL') ?: (string) ($d['url'] ?? '');
    if ($url === '' && defined('IXC_URL')) { $url = IXC_URL; }

    $token = getenv('IXC_TOKEN') ?: (string) ($d['token'] ?? '');
    if ($token === '' && defined('IXC_TOKEN')) { $token = IXC_TOKEN; }

    $raio = (int) ($d['raio_metros'] ?? 0);
    if ($raio <= 0 && defined('VIABILIDADE_RAIO_METROS')) { $raio = (int) VIABILIDADE_RAIO_METROS; }
    if ($raio <= 0) { $raio = 300; }

    $cidade = trim((string) ($d['id_cidade'] ?? ''));
    if ($cidade === '') { $cidade = '4446'; } // Joinville (default histórico do código)

    return [
        'enabled'     => (bool) ($d['enabled'] ?? false),
        'url'         => rtrim((string) $url, '/'),
        'token'       => (string) $token,
        'raio_metros' => $raio,
        'id_cidade'   => $cidade,
    ];
}

/** Persiste as configurações (escreve um .php que devolve o array). */
function ixc_save(array $s): bool {
    $arr = [
        'enabled'     => (bool) ($s['enabled'] ?? false),
        'url'         => rtrim(trim((string) ($s['url'] ?? '')), '/'),
        'token'       => (string) ($s['token'] ?? ''),
        'raio_metros' => max(1, (int) ($s['raio_metros'] ?? 300)),
        'id_cidade'   => trim((string) ($s['id_cidade'] ?? '')),
    ];
    $php = "<?php\n// Gerado pelo painel admin (Integração IXC). NAO commitar — contém token.\nreturn "
         . var_export($arr, true) . ";\n";
    $dir = dirname(ixc_store_path());
    if (!is_dir($dir)) { @mkdir($dir, 0755, true); }
    return file_put_contents(ixc_store_path(), $php, LOCK_EX) !== false;
}

/**
 * Faz uma requisição "listar" na API do IXC.
 *
 * @param string     $endpoint  ex: 'rad_caixa_ftth'
 * @param array      $params    corpo da consulta IXC (qtype/query/oper/page/rp/...)
 * @param array|null $override  ['url'=>, 'token'=>] p/ testar credenciais ainda não salvas
 * @return array|null  resposta decodificada, ou null em erro (sempre logado)
 */
function ixc_request(string $endpoint, array $params = [], ?array $override = null): ?array {
    $cfg   = ixc_settings();
    $url   = rtrim((string) ($override['url']   ?? $cfg['url']), '/');
    $token = (string) ($override['token'] ?? $cfg['token']);

    if ($url === '' || $token === '') {
        error_log('[ixc] requisição abortada: url ou token vazios');
        return null;
    }

    $ch = curl_init($url . '/' . $endpoint);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_USERPWD        => $token,
        CURLOPT_HTTPHEADER     => ['Content-Type: application/json', 'ixcsoft: listar'],
        CURLOPT_CUSTOMREQUEST  => 'GET',
        CURLOPT_POSTFIELDS     => json_encode($params),
        // SSL verify ON — se IXC tiver cert self-signed, instalar CA no servidor
        // em vez de desabilitar. (Antes: VERIFYPEER/VERIFYHOST = false → MITM podia
        // ler/modificar token + dados de cliente.)
        CURLOPT_SSL_VERIFYPEER => true,
        CURLOPT_SSL_VERIFYHOST => 2,
        CURLOPT_TIMEOUT        => 10,
    ]);

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curlErr  = curl_error($ch);
    curl_close($ch);

    if ($curlErr !== '') {
        error_log("[ixc] cURL erro em {$endpoint}: {$curlErr}");
        return null;
    }
    if ($httpCode !== 200 || !$response) {
        error_log("[ixc] HTTP {$httpCode} em {$endpoint}");
        return null;
    }

    $data = json_decode($response, true);
    return is_array($data) ? $data : null;
}
