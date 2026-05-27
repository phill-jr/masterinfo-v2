<?php
/**
 * MasterInfo - Admin Config API (PROTEGIDO)
 * GET  → retorna config.json (requer sessao admin)
 * POST → salva config.json (requer sessao admin + CSRF)
 */

require_once __DIR__ . '/../auth/session.php';
require_once __DIR__ . '/../auth/csrf.php';

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-CSRF-Token');
header('Access-Control-Allow-Credentials: true');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

// ─── Exigir autenticacao ───
requireAdminSession();

$configFile = __DIR__ . '/../config.json';

// ─── GET: ler config ───
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if (!file_exists($configFile)) {
        http_response_code(404);
        echo json_encode(['error' => 'config.json nao encontrado']);
        exit;
    }
    echo file_get_contents($configFile);
    exit;
}

// ─── POST: salvar config ───
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Validar CSRF
    $csrfToken = $_SERVER['HTTP_X_CSRF_TOKEN'] ?? '';
    if (!validateCsrfToken($csrfToken)) {
        http_response_code(403);
        echo json_encode(['error' => 'Token CSRF invalido. Recarregue a pagina.']);
        exit;
    }

    $input = file_get_contents('php://input');
    $data = json_decode($input, true);

    if ($data === null) {
        http_response_code(400);
        echo json_encode(['error' => 'JSON invalido']);
        exit;
    }

    // Validacao basica de estrutura (todas as secoes gerenciadas pelo admin)
    $required = ['empresa', 'checkout', 'hero', 'stats', 'diferenciais', 'bairros', 'depoimentos', 'faq', 'planos', 'addons'];
    $missing = [];
    foreach ($required as $key) {
        if (!isset($data[$key])) $missing[] = $key;
    }
    if (!empty($missing)) {
        http_response_code(400);
        echo json_encode(['error' => 'Estrutura invalida. Secoes faltando: ' . implode(', ', $missing)]);
        exit;
    }

    // Backup antes de salvar (dentro de secrets/ para nao ser acessivel via web)
    if (file_exists($configFile)) {
        $backupDir = __DIR__ . '/../secrets';
        if (!is_dir($backupDir)) mkdir($backupDir, 0755, true);
        copy($configFile, $backupDir . '/config.json.bak');
    }

    // Salvar com formatacao legivel
    $result = file_put_contents($configFile, json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE), LOCK_EX);

    if ($result === false) {
        http_response_code(500);
        echo json_encode(['error' => 'Erro ao salvar arquivo']);
        exit;
    }

    echo json_encode(['ok' => true, 'message' => 'Configuracao salva com sucesso']);
}
