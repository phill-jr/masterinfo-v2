<?php
/**
 * MasterInfo - Security Headers Centralizados
 *
 * Aplicado em todo endpoint PHP (api/*.php, auth/*.php) que faz include
 * deste arquivo. NOTA: paginas HTML estaticas (index.html, admin.html,
 * subpaginas) NAO recebem estes headers via PHP - usar o snippet
 * `deploy/nginx-security.conf.example` no nginx pra cobrir HTML estatico.
 */

function sendSecurityHeaders(): void {
    header('X-Content-Type-Options: nosniff');
    header('X-Frame-Options: SAMEORIGIN');
    // X-XSS-Protection removido — descontinuado pelos browsers modernos
    // (Chrome/Edge ja nao implementam, e em algumas versoes habilitar pode
    //  introduzir XSS). Confiar em CSP abaixo.
    header('Referrer-Policy: strict-origin-when-cross-origin');
    header('Permissions-Policy: geolocation=(self), camera=(), microphone=(), payment=(), usb=(), magnetometer=(), gyroscope=()');

    // Content-Security-Policy - mitiga XSS, supply-chain e clickjacking
    // OBS: 'unsafe-inline' temporario porque ha onclick=/style= inline no
    // codigo. Plano: extrair pra arquivos e remover essa permissao.
    $csp = "default-src 'self'; "
        . "script-src 'self' 'unsafe-inline' https://unpkg.com https://www.googletagmanager.com https://www.google-analytics.com https://connect.facebook.net; "
        . "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://unpkg.com; "
        . "img-src 'self' data: blob: https:; "
        . "font-src 'self' https://fonts.gstatic.com data:; "
        . "connect-src 'self' https://viacep.com.br https://nominatim.openstreetmap.org https://www.google-analytics.com https://www.googletagmanager.com https://*.facebook.com; "
        . "media-src 'self'; "
        . "object-src 'none'; "
        . "frame-ancestors 'self'; "
        . "base-uri 'self'; "
        . "form-action 'self'";
    header('Content-Security-Policy: ' . $csp);

    // HSTS - HTTPS direto ou atras de proxy reverso com X-Forwarded-Proto
    $isHttps = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
        || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https')
        || ((int)($_SERVER['SERVER_PORT'] ?? 80) === 443);
    if ($isHttps) {
        header('Strict-Transport-Security: max-age=63072000; includeSubDomains; preload');
    }
}
