<?php
/**
 * MasterInfo - Credenciais do Admin (TEMPLATE, multi-usuario)
 *
 * 1. Copie este arquivo para `auth/credentials.php` (mesma pasta, sem o .example).
 * 2. Gere o hash de cada senha:
 *      php -r "echo password_hash('SUASENHAFORTE', PASSWORD_BCRYPT, ['cost'=>12]) . PHP_EOL;"
 * 3. Cole cada usuario/hash no array ADMIN_USERS abaixo.
 *
 * `auth/credentials.php` esta no .gitignore - nao versionar.
 */

define('ADMIN_USERS', [
    'admin' => 'COLE_AQUI_O_HASH_BCRYPT',
    // 'outrousuario' => 'OUTRO_HASH_BCRYPT',
]);
