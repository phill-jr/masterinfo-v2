<?php
/**
 * MasterInfo - Verificar sessao admin
 * Retorna { ok: true, csrf_token: "..." } se autenticado
 * Retorna 401 se nao autenticado
 */

require_once __DIR__ . '/session.php';
require_once __DIR__ . '/csrf.php';

header('Content-Type: application/json; charset=utf-8');

requireAdminSession();

echo json_encode([
    'ok' => true,
    'user' => $_SESSION['admin_user'] ?? 'admin',
    'csrf_token' => generateCsrfToken(),
]);
