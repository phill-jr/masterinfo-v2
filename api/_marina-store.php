<?php
/**
 * Store das configurações do atendimento Marina (chat de boletos).
 *
 * Persistido em secrets/marina.php — arquivo .php (executa, NUNCA é servido como texto)
 * e a pasta secrets/ é bloqueada no .htaccess. O token vive só aqui, no servidor.
 *
 * Usado por:
 *   - api/marina.php          (proxy público — lê enabled/endpoint/token)
 *   - api/admin/marina.php    (painel admin — lê status e salva)
 */
if (!defined('MASTERINFO_INTERNAL')) { define('MASTERINFO_INTERNAL', true); }

function marina_store_path(): string {
    return __DIR__ . '/../secrets/marina.php';
}

/**
 * Retorna as configurações resolvidas.
 * Prioridade p/ endpoint e token: variável de ambiente > store > constante (secrets/config.php).
 */
function marina_settings(): array {
    $f = marina_store_path();
    $d = is_file($f) ? @include $f : null;
    if (!is_array($d)) { $d = []; }

    $endpoint = getenv('MARINA_URL') ?: (string) ($d['endpoint'] ?? '');
    if ($endpoint === '' && defined('MARINA_URL')) { $endpoint = MARINA_URL; }

    $token = getenv('MARINA_TOKEN') ?: (string) ($d['token'] ?? '');
    if ($token === '' && defined('MARINA_TOKEN')) { $token = MARINA_TOKEN; }

    return [
        'enabled'  => (bool) ($d['enabled'] ?? false),
        'endpoint' => (string) $endpoint,
        'token'    => (string) $token,
    ];
}

/** Persiste as configurações (escreve um .php que devolve o array). */
function marina_save(array $s): bool {
    $arr = [
        'enabled'  => (bool) ($s['enabled'] ?? false),
        'endpoint' => trim((string) ($s['endpoint'] ?? '')),
        'token'    => (string) ($s['token'] ?? ''),
    ];
    $php = "<?php\n// Gerado pelo painel admin (Atendimento Marina). NAO commitar — contém token.\nreturn "
         . var_export($arr, true) . ";\n";
    $dir = dirname(marina_store_path());
    if (!is_dir($dir)) { @mkdir($dir, 0755, true); }
    return file_put_contents(marina_store_path(), $php, LOCK_EX) !== false;
}
