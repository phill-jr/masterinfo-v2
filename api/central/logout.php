<?php
/** POST /api/central/logout.php — encerra a sessão do cliente. */
define('MASTERINFO_INTERNAL', true);
require_once __DIR__ . '/_central.php';

central_headers();
central_logout_session();
central_json(200, ['ok' => true]);
