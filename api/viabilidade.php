<?php
/**
 * MasterInfo - API de Viabilidade
 * Recebe CEP, consulta coordenadas via ViaCEP + Nominatim,
 * busca CTOs próximas no IXC e verifica portas disponíveis.
 *
 * POST /api/viabilidade.php
 * Body: { "cep": "89228130" }
 * Response: { "viavel": true, "endereco": {...}, "cto": {...} }
 */

require_once __DIR__ . '/../security-headers.php';
require_once __DIR__ . '/rate-limit.php';

sendSecurityHeaders();

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: ' . (defined('ALLOWED_ORIGIN') ? ALLOWED_ORIGIN : '*'));
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    responder(false, 'Método não permitido', 405);
}

require_once __DIR__ . '/../secrets/config.php';

// Rate limiting: 20 consultas/hora por IP
checkRateLimit('viabilidade', 20, 3600);

// Receber CEP
$input = json_decode(file_get_contents('php://input'), true);
$cep = preg_replace('/\D/', '', $input['cep'] ?? '');

if (strlen($cep) !== 8) {
    responder(false, 'CEP inválido. Informe 8 dígitos.');
}

// ─── Step 1: Consultar ViaCEP ───
$viaCep = consultarViaCep($cep);
if (!$viaCep) {
    responder(false, 'CEP não encontrado. Verifique e tente novamente.');
}

// ─── Step 2: Obter coordenadas via Nominatim ───
$coords = obterCoordenadas($viaCep);
if (!$coords) {
    // Fallback: buscar CTOs por bairro no IXC
    $cto = buscarCtoPorBairro($viaCep['bairro'] ?? '');
    if ($cto) {
        responder(true, 'Cobertura disponível no seu bairro!', 200, [
            'endereco' => $viaCep,
            'cto' => [
                'nome' => $cto['descricao'],
                'bairro' => $cto['bairro'],
                'portas_disponiveis' => $cto['portas_disponiveis'],
            ],
        ]);
    }
    responder(false, 'Não foi possível verificar a cobertura para este endereço. Entre em contato pelo WhatsApp.');
}

// ─── Step 3: Buscar CTOs próximas no IXC ───
$cto = buscarCtoProxima($coords['lat'], $coords['lon']);
if (!$cto) {
    responder(false, 'Ainda não temos cobertura no seu endereço. Estamos expandindo! Deixe seus dados e avisamos quando chegar.', 200, [
        'endereco' => $viaCep,
        'sem_cobertura' => true,
    ]);
}

// ─── Step 4: Verificar portas disponíveis ───
$portasOcupadas = contarPortasOcupadas($cto['id']);
$portasDisponiveis = max(0, (int)$cto['capacidade'] - $portasOcupadas);

if ($portasDisponiveis <= 0) {
    responder(false, 'Temos fibra no seu endereço, mas a caixa mais próxima está lotada. Deixe seus dados e entraremos em contato quando houver vaga.', 200, [
        'endereco' => $viaCep,
        'sem_porta' => true,
    ]);
}

responder(true, 'Cobertura disponível!', 200, [
    'endereco' => $viaCep,
    'cto' => [
        'nome' => $cto['descricao'],
        'bairro' => $cto['bairro'],
        'portas_disponiveis' => $portasDisponiveis,
        'distancia_metros' => $cto['distancia'] ?? null,
    ],
]);

// ══════════════════════════════════════════════
// FUNÇÕES
// ══════════════════════════════════════════════

function responder($viavel, $mensagem, $httpCode = 200, $dados = []) {
    http_response_code($httpCode);
    echo json_encode(array_merge([
        'viavel' => $viavel,
        'mensagem' => $mensagem,
    ], $dados), JSON_UNESCAPED_UNICODE);
    exit;
}

function consultarViaCep($cep) {
    $url = "https://viacep.com.br/ws/{$cep}/json/";
    $response = file_get_contents($url);
    if (!$response) return null;

    $data = json_decode($response, true);
    if (isset($data['erro']) && $data['erro']) return null;

    return [
        'cep' => $data['cep'] ?? '',
        'logradouro' => $data['logradouro'] ?? '',
        'bairro' => $data['bairro'] ?? '',
        'cidade' => $data['localidade'] ?? '',
        'uf' => $data['uf'] ?? '',
    ];
}

function obterCoordenadas($viaCep) {
    $query = urlencode("{$viaCep['logradouro']}, {$viaCep['bairro']}, {$viaCep['cidade']}, {$viaCep['uf']}, Brasil");
    $url = "https://nominatim.openstreetmap.org/search?format=json&q={$query}&limit=1&countrycodes=br";

    $ctx = stream_context_create(['http' => [
        'header' => "User-Agent: MasterInfoViabilidade/1.0\r\n",
        'timeout' => 5,
    ]]);

    $response = @file_get_contents($url, false, $ctx);
    if (!$response) return null;

    $data = json_decode($response, true);
    if (empty($data[0])) return null;

    return [
        'lat' => (float)$data[0]['lat'],
        'lon' => (float)$data[0]['lon'],
    ];
}

function ixcRequest($endpoint, $params = []) {
    $url = IXC_URL . '/' . $endpoint;

    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_USERPWD => IXC_TOKEN,
        CURLOPT_HTTPHEADER => [
            'Content-Type: application/json',
            'ixcsoft: listar',
        ],
        CURLOPT_CUSTOMREQUEST => 'GET',
        CURLOPT_POSTFIELDS => json_encode($params),
        CURLOPT_SSL_VERIFYPEER => false,
        CURLOPT_SSL_VERIFYHOST => false,
        CURLOPT_TIMEOUT => 10,
    ]);

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode !== 200 || !$response) return null;

    return json_decode($response, true);
}

function buscarCtoProxima($lat, $lon) {
    // Buscar CTOs ativas com coordenadas preenchidas
    // O IXC não suporta busca por raio, então buscamos todas da cidade
    // e calculamos distância no PHP
    $data = ixcRequest('rad_caixa_ftth', [
        'qtype' => 'rad_caixa_ftth.status',
        'query' => 'A',
        'oper' => '=',
        'page' => '1',
        'rp' => '200000',
        'sortname' => 'rad_caixa_ftth.id',
        'sortorder' => 'desc',
        'grid_param' => json_encode([
            ['TB' => 'rad_caixa_ftth.id_cidade', 'OP' => '=', 'P' => '4446'], // Joinville
        ]),
    ]);

    if (!$data || empty($data['registros'])) return null;

    $raioMax = VIABILIDADE_RAIO_METROS;
    $melhorCto = null;
    $menorDistancia = PHP_FLOAT_MAX;

    foreach ($data['registros'] as $cto) {
        $ctoLat = (float)($cto['latitude'] ?? 0);
        $ctoLon = (float)($cto['longitude'] ?? 0);

        if ($ctoLat == 0 || $ctoLon == 0) continue;

        $distancia = calcularDistancia($lat, $lon, $ctoLat, $ctoLon);

        if ($distancia < $menorDistancia && $distancia <= $raioMax) {
            $menorDistancia = $distancia;
            $melhorCto = $cto;
            $melhorCto['distancia'] = round($distancia);
        }
    }

    return $melhorCto;
}

function buscarCtoPorBairro($bairro) {
    if (empty($bairro)) return null;

    $data = ixcRequest('rad_caixa_ftth', [
        'qtype' => 'rad_caixa_ftth.bairro',
        'query' => $bairro,
        'oper' => 'L',
        'page' => '1',
        'rp' => '1',
        'sortname' => 'rad_caixa_ftth.id',
        'sortorder' => 'desc',
        'grid_param' => json_encode([
            ['TB' => 'rad_caixa_ftth.status', 'OP' => '=', 'P' => 'A'],
        ]),
    ]);

    if (!$data || empty($data['registros'])) return null;

    $cto = $data['registros'][0];
    $portasOcupadas = contarPortasOcupadas($cto['id']);
    $cto['portas_disponiveis'] = max(0, (int)$cto['capacidade'] - $portasOcupadas);

    return $cto;
}

function contarPortasOcupadas($ctoId) {
    $data = ixcRequest('radpop_radio_cliente_fibra', [
        'qtype' => 'radpop_radio_cliente_fibra.id_caixa_ftth',
        'query' => (string)$ctoId,
        'oper' => '=',
        'page' => '1',
        'rp' => '1',
        'sortname' => 'radpop_radio_cliente_fibra.id',
        'sortorder' => 'desc',
    ]);

    return (int)($data['total'] ?? 0);
}

/**
 * Calcula distância entre dois pontos (Haversine) em metros
 */
function calcularDistancia($lat1, $lon1, $lat2, $lon2) {
    $R = 6371000; // Raio da Terra em metros
    $dLat = deg2rad($lat2 - $lat1);
    $dLon = deg2rad($lon2 - $lon1);

    $a = sin($dLat / 2) * sin($dLat / 2) +
         cos(deg2rad($lat1)) * cos(deg2rad($lat2)) *
         sin($dLon / 2) * sin($dLon / 2);

    $c = 2 * atan2(sqrt($a), sqrt(1 - $a));
    return $R * $c;
}
