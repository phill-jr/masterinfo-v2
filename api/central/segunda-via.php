<?php
/**
 * POST /api/central/segunda-via.php  — body { fatura_id }  — requer sessão.
 * Gera a 2ª via (PDF base64) da fatura, confirmando que ela é do cliente logado.
 */
define('MASTERINFO_INTERNAL', true);
require_once __DIR__ . '/_central.php';

central_headers();
$sess = central_require_session();

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    central_json(405, ['ok' => false, 'error' => 'method', 'message' => 'Método não permitido.']);
}

$in       = central_input();
$faturaId = central_digits((string) ($in['fatura_id'] ?? ''));
if ($faturaId === '') {
    central_json(422, ['ok' => false, 'error' => 'INVALID', 'message' => 'Fatura inválida.']);
}

try {
    $r = central_segunda_via($sess['id'], $faturaId);
    if (!$r['ok']) {
        $http = $r['error'] === 'forbidden' ? 403 : 502;
        central_json($http, ['ok' => false, 'error' => $r['error'],
            'message' => 'Não consegui gerar a 2ª via dessa fatura.']);
    }
    central_json(200, $r);
} catch (\Throwable $e) {
    error_log('[central/segunda-via] ' . get_class($e) . ': ' . $e->getMessage() . ' @ ' . $e->getFile() . ':' . $e->getLine());
    central_json(500, ['ok' => false, 'error' => 'internal', 'message' => 'Erro ao gerar a 2ª via.']);
}
