<?php
/**
 * MasterInfo - Credenciais do Admin (TEMPLATE)
 *
 * 1. Copie este arquivo para `auth/credentials.php` (mesma pasta, sem o .example).
 * 2. Gere o hash da sua senha:
 *      php -r "echo password_hash('SUASENHAFORTE', PASSWORD_BCRYPT) . PHP_EOL;"
 * 3. Cole o resultado em ADMIN_PASS_HASH abaixo.
 *
 * `auth/credentials.php` esta no .gitignore - nao versionar.
 */

define('ADMIN_USER', 'admin');

// Substituir pelo hash gerado com password_hash() em producao.
define('ADMIN_PASS_HASH', 'COLE_AQUI_O_HASH_BCRYPT');
