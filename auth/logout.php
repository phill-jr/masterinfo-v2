<?php
/**
 * MasterInfo - Logout
 */

if (session_status() === PHP_SESSION_NONE) session_start();
session_unset();
session_destroy();

// Limpar cookie de sessao
if (ini_get('session.use_cookies')) {
    $params = session_get_cookie_params();
    setcookie(session_name(), '', time() - 42000,
        $params['path'], $params['domain'],
        $params['secure'], $params['httponly']
    );
}

header('Location: ../admin-login.html');
exit;
