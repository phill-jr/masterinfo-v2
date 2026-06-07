<?php
/**
 * MasterInfo - Upload de imagens (PROTEGIDO)
 *
 * POST /api/admin-upload.php
 *   multipart/form-data:
 *     - imagem: file (jpg/png/webp/gif, ≤5MB)
 *     - destino: opcional ("slide" por enquanto; reservado pra outros usos)
 *
 * Resposta JSON:
 *   { ok: true, path: "imgs/hero/slide-20260605-141520-a1b2c3.png", size, mime }
 *
 * Requer sessao admin + CSRF (mesmo padrao do admin-config.php).
 * MIME e detectado por finfo (NAO confia no que o cliente envia).
 */

require_once __DIR__ . '/../auth/session.php';
require_once __DIR__ . '/../auth/csrf.php';

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-CSRF-Token');
header('Access-Control-Allow-Credentials: true');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

requireAdminSession();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Metodo nao permitido']);
    exit;
}

$csrfToken = $_SERVER['HTTP_X_CSRF_TOKEN'] ?? '';
if (!validateCsrfToken($csrfToken)) {
    http_response_code(403);
    echo json_encode(['error' => 'Token CSRF invalido. Recarregue a pagina.']);
    exit;
}

// ─── Validar campo do form ───
if (!isset($_FILES['imagem'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Nenhuma imagem enviada (campo "imagem" ausente).']);
    exit;
}

$file = $_FILES['imagem'];

$uploadErrorMessages = [
    UPLOAD_ERR_INI_SIZE   => 'Arquivo maior que o permitido pelo servidor (upload_max_filesize).',
    UPLOAD_ERR_FORM_SIZE  => 'Arquivo maior que o permitido pelo formulario.',
    UPLOAD_ERR_PARTIAL    => 'Upload incompleto. Tente de novo.',
    UPLOAD_ERR_NO_FILE    => 'Nenhum arquivo enviado.',
    UPLOAD_ERR_NO_TMP_DIR => 'Servidor sem diretorio temporario.',
    UPLOAD_ERR_CANT_WRITE => 'Servidor nao conseguiu salvar (permissoes?).',
    UPLOAD_ERR_EXTENSION  => 'Upload bloqueado por extensao PHP.',
];

if ($file['error'] !== UPLOAD_ERR_OK) {
    http_response_code(400);
    echo json_encode(['error' => $uploadErrorMessages[$file['error']] ?? ('Erro no upload (codigo ' . $file['error'] . ').')]);
    exit;
}

// ─── Tamanho maximo: 5MB ───
$maxBytes = 5 * 1024 * 1024;
if ($file['size'] > $maxBytes) {
    http_response_code(400);
    echo json_encode(['error' => 'Imagem maior que 5MB.']);
    exit;
}

// ─── Detectar MIME REAL (nao confia em $_FILES[...]['type']) ───
if (!class_exists('finfo')) {
    http_response_code(500);
    echo json_encode(['error' => 'Servidor sem extensao fileinfo (PHP).']);
    exit;
}

$finfo = new finfo(FILEINFO_MIME_TYPE);
$mime = $finfo->file($file['tmp_name']);

// SVG NAO entra na lista por seguranca (pode carregar script).
$allowedMimes = [
    'image/jpeg' => 'jpg',
    'image/png'  => 'png',
    'image/webp' => 'webp',
    'image/gif'  => 'gif',
];

if (!isset($allowedMimes[$mime])) {
    http_response_code(400);
    echo json_encode(['error' => 'Tipo de arquivo nao permitido (' . htmlspecialchars($mime, ENT_QUOTES) . '). Use JPG, PNG, WebP ou GIF.']);
    exit;
}

$ext = $allowedMimes[$mime];

// ─── Pasta de destino ───
$relDir = 'imgs/hero';
$absDir = realpath(__DIR__ . '/..') . DIRECTORY_SEPARATOR . str_replace('/', DIRECTORY_SEPARATOR, $relDir);

if (!is_dir($absDir)) {
    if (!@mkdir($absDir, 0755, true) && !is_dir($absDir)) {
        http_response_code(500);
        echo json_encode(['error' => 'Nao foi possivel criar a pasta ' . $relDir . '.']);
        exit;
    }
}

// ─── Nome unico ───
// Formato: slide-YYYYMMDD-HHMMSS-{6 hex}.ext  (sortavel cronologicamente)
$rand = bin2hex(random_bytes(3));
$filename = 'slide-' . date('Ymd-His') . '-' . $rand . '.' . $ext;
$target = $absDir . DIRECTORY_SEPARATOR . $filename;

if (!move_uploaded_file($file['tmp_name'], $target)) {
    http_response_code(500);
    echo json_encode(['error' => 'Falha ao salvar o arquivo no servidor.']);
    exit;
}

// ─── Resposta ───
echo json_encode([
    'ok'   => true,
    'path' => $relDir . '/' . $filename,
    'size' => $file['size'],
    'mime' => $mime,
]);
