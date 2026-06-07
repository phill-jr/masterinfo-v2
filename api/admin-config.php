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
    $required = ['empresa', 'checkout', 'heroSlides', 'stats', 'diferenciais', 'bairros', 'depoimentos', 'faq', 'planos', 'addons'];
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

    // ─── Republicar as subpaginas estaticas ───
    // O gerador le o config recem-salvo e reescreve header+rodape das 21 paginas
    // (modo --menus, cirurgico). Nao-fatal: se python/exec nao estiver disponivel,
    // o save segue OK e o motivo volta em 'publish' pra mostrar no admin.
    $publish = republishSubpages(__DIR__ . '/../gerar_subpaginas.py');

    echo json_encode(['ok' => true, 'message' => 'Configuracao salva com sucesso', 'publish' => $publish]);
}

/**
 * Propaga o menu pras subpaginas rodando `python gerar_subpaginas.py --menus`.
 * O comando e 100% estatico (nome do python + caminho do script + flag fixa),
 * sem nenhum dado do usuario — sem risco de injecao de shell.
 */
function republishSubpages($scriptPath)
{
    $script = realpath($scriptPath);
    if (!$script || !is_file($script)) {
        return ['ran' => false, 'reason' => 'gerador nao encontrado'];
    }
    if (!function_exists('exec')) {
        return ['ran' => false, 'reason' => 'exec indisponivel'];
    }
    $disabled = array_map('trim', explode(',', (string) ini_get('disable_functions')));
    if (in_array('exec', $disabled, true)) {
        return ['ran' => false, 'reason' => 'exec desabilitado no PHP'];
    }

    $isWin = stripos(PHP_OS, 'WIN') === 0;
    $cands = $isWin ? ['py', 'python', 'python3'] : ['python3', 'python'];
    $py = null;
    foreach ($cands as $c) {
        $probe = ($isWin ? 'where ' : 'command -v ') . escapeshellarg($c);
        $found = trim((string) @shell_exec($probe . ' 2>&1'));
        if ($found !== '' && stripos($found, 'not found') === false && stripos($found, 'could not find') === false) {
            $py = $c;
            break;
        }
    }
    if (!$py) {
        return ['ran' => false, 'reason' => 'python nao encontrado no host'];
    }

    $cmd = escapeshellarg($py) . ' ' . escapeshellarg($script) . ' --menus 2>&1';
    $out = [];
    $rc = 1;
    @exec($cmd, $out, $rc);

    return [
        'ran'  => true,
        'ok'   => ($rc === 0),
        'code' => $rc,
        'tail' => implode(' | ', array_slice($out, -2)),
    ];
}
