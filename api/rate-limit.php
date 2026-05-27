<?php
/**
 * MasterInfo - Rate Limiting Centralizado
 * Baseado em arquivo, por IP + endpoint.
 */

/**
 * Verifica rate limit. Encerra com 429 se excedido.
 *
 * @param string $endpoint  Nome do endpoint (ex: 'viabilidade', 'checkout')
 * @param int    $maxReqs   Maximo de requisicoes permitidas na janela
 * @param int    $windowSec Duracao da janela em segundos
 */
function checkRateLimit(string $endpoint, int $maxReqs, int $windowSec): void {
    $ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    $key = md5($endpoint . ':' . $ip);
    $file = sys_get_temp_dir() . '/mi_rate_' . $key;

    $data = file_exists($file)
        ? json_decode(file_get_contents($file), true)
        : ['count' => 0, 'reset' => time() + $windowSec];

    // Resetar janela se expirou
    if (time() > ($data['reset'] ?? 0)) {
        $data = ['count' => 0, 'reset' => time() + $windowSec];
    }

    $data['count']++;
    file_put_contents($file, json_encode($data), LOCK_EX);

    if ($data['count'] > $maxReqs) {
        $retry = max(1, ($data['reset'] ?? time()) - time());
        header('Content-Type: application/json; charset=utf-8');
        header('Retry-After: ' . $retry);
        http_response_code(429);
        echo json_encode(['error' => "Muitas requisicoes. Tente novamente em {$retry} segundos."]);
        exit;
    }
}
