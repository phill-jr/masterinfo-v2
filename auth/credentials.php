<?php
/**
 * MasterInfo - Credenciais do Admin
 *
 * IMPORTANTE: Este arquivo NAO deve ir para o git!
 *
 * Para gerar um novo hash de senha:
 *   php -r "echo password_hash('suasenha', PASSWORD_BCRYPT) . PHP_EOL;"
 *
 * Cole o resultado no ADMIN_PASS_HASH abaixo.
 */

define('ADMIN_USER', 'admin');

// Senha padrao: master@2026 (TROCAR em producao!)
define('ADMIN_PASS_HASH', '$2y$12$4LWbS5HCXfbAAenvH1wJ7.hLgVlExqI6UNM6rxDBeCX2pBDr5zlse');

// Para trocar a senha, gere um novo hash:
// php -r "echo password_hash('novaSenha', PASSWORD_BCRYPT) . PHP_EOL;"
