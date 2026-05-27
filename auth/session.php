<?php
/**
 * MasterInfo - Gerenciamento de Sessao Segura
 */

// Configuracao segura ANTES de session_start
ini_set('session.cookie_httponly', 1);
ini_set('session.cookie_samesite', 'Strict');
ini_set('session.use_strict_mode', 1);
ini_set('session.gc_maxlifetime', 7200); // 2 horas

/**
 * Exige sessao admin valida. Retorna 401 JSON se nao autenticado.
 */
function requireAdminSession() {
    if (session_status() === PHP_SESSION_NONE) session_start();

    if (
        empty($_SESSION['admin_authenticated']) ||
        empty($_SESSION['admin_ip']) ||
        $_SESSION['admin_ip'] !== ($_SERVER['REMOTE_ADDR'] ?? '')
    ) {
        http_response_code(401);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['error' => 'Nao autenticado', 'redirect' => 'admin-login.html']);
        exit;
    }

    // Expirar sessao apos 2 horas de inatividade
    if (isset($_SESSION['last_activity']) && (time() - $_SESSION['last_activity'] > 7200)) {
        session_unset();
        session_destroy();
        http_response_code(401);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['error' => 'Sessao expirada', 'redirect' => 'admin-login.html']);
        exit;
    }
    $_SESSION['last_activity'] = time();

    // Regenerar ID a cada 30 min para prevenir session fixation
    if (time() - ($_SESSION['last_regeneration'] ?? 0) > 1800) {
        session_regenerate_id(true);
        $_SESSION['last_regeneration'] = time();
    }
}

/**
 * Verifica se ha sessao admin ativa (sem bloquear).
 */
function hasAdminSession(): bool {
    if (session_status() === PHP_SESSION_NONE) session_start();
    return !empty($_SESSION['admin_authenticated']) &&
           !empty($_SESSION['admin_ip']) &&
           $_SESSION['admin_ip'] === ($_SERVER['REMOTE_ADDR'] ?? '');
}
