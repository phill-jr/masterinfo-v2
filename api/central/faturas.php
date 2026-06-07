<?php
/**
 * GET /api/central/faturas.php  — requer sessão do cliente.
 * Lista as faturas em aberto do cliente logado.
 */
define('MASTERINFO_INTERNAL', true);
require_once __DIR__ . '/_central.php';

central_headers();
$sess = central_require_session();

try {
    $faturas = central_faturas_abertas($sess['id']);
    central_json(200, [
        'ok'      => true,
        'cliente' => ['nome' => $sess['nome']],
        'faturas' => $faturas,
        'total'   => count($faturas),
    ]);
} catch (\Throwable $e) {
    error_log('[central/faturas] ' . get_class($e) . ': ' . $e->getMessage() . ' @ ' . $e->getFile() . ':' . $e->getLine());
    central_json(500, ['ok' => false, 'error' => 'internal', 'message' => 'Não consegui carregar suas faturas.']);
}
