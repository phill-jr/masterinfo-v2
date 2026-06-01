<?php
/**
 * MasterInfo — Helpers internos pra chamadas Bitrix24
 * Usado pelos endpoints admin/bitrix-*.php e form-submit.php
 *
 * NÃO chamar este arquivo direto pelo navegador.
 */

if (!defined('MASTERINFO_INTERNAL')) {
    http_response_code(403);
    exit('Forbidden');
}

require_once __DIR__ . '/../../secrets/config.php';

/**
 * Chama a API REST do Bitrix24.
 * @throws Exception em erros HTTP, cURL ou retorno com 'error'
 */
function bx_request(string $method, array $data = []): array {
    if (!defined('BITRIX_WEBHOOK') || empty(BITRIX_WEBHOOK)) {
        throw new Exception('BITRIX_WEBHOOK não configurado em secrets/config.php');
    }

    $url = rtrim(BITRIX_WEBHOOK, '/') . '/' . ltrim($method, '/');

    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_POST           => true,
        CURLOPT_POSTFIELDS     => json_encode($data, JSON_UNESCAPED_UNICODE),
        CURLOPT_HTTPHEADER     => ['Content-Type: application/json'],
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT        => 25,
        CURLOPT_CONNECTTIMEOUT => 10,
        CURLOPT_SSL_VERIFYPEER => true,
    ]);

    $response = curl_exec($ch);
    $http     = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $cerr     = curl_error($ch);
    curl_close($ch);

    if ($cerr) {
        throw new Exception("Conexão Bitrix falhou: $cerr");
    }

    $body = json_decode($response, true);
    if ($body === null) {
        throw new Exception("Resposta Bitrix não é JSON válido (HTTP $http)");
    }

    if (isset($body['error'])) {
        $msg = $body['error_description'] ?? $body['error'];
        throw new Exception("Bitrix: $msg");
    }

    if ($http >= 400) {
        throw new Exception("Bitrix HTTP $http");
    }

    return $body;
}

/** Caminho do JSON de mapeamento. */
function bx_mapping_path(): string {
    return __DIR__ . '/../../secrets/bitrix-mapping.json';
}

function bx_load_mapping(): array {
    $path = bx_mapping_path();
    if (!file_exists($path)) {
        return bx_default_mapping();
    }
    $data = json_decode(file_get_contents($path), true);
    return is_array($data) ? $data : bx_default_mapping();
}

function bx_save_mapping(array $data): bool {
    $path = bx_mapping_path();
    $dir = dirname($path);
    if (!is_dir($dir)) mkdir($dir, 0700, true);
    return (bool) file_put_contents(
        $path,
        json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE)
    );
}

/** Estrutura default — fica como base no painel admin. */
function bx_default_mapping(): array {
    return [
        // Apelidos amigáveis pros 248 UF_CRM (preenchidos no painel)
        'field_labels' => [
            // 'UF_CRM_1676591723362' => 'Bairro',
            // 'UF_CRM_1676772668897' => 'Plano',
        ],
        // Configuração POR FORMULÁRIO do site
        'forms' => [
            'pre-venda-copa' => [
                'label'        => 'Pré-venda Copa 2026',
                'entity'       => 'deal',         // lead | contact | deal
                'category_id'  => 0,              // funil (Comercial = 0)
                'stage_id'     => 'NEW',          // etapa inicial
                'source_id'    => 'WEB',          // origem
                'dedupe_by'    => ['phone'],      // evita duplicar contato
                // Mapeamento form → Bitrix
                'mappings' => [
                    'nome'     => 'CONTACT.NAME',
                    'bairro'   => 'DEAL.COMMENTS',
                    'telefone' => 'CONTACT.PHONE',
                    'plano'    => 'DEAL.TITLE',
                    'origem'   => 'DEAL.SOURCE_DESCRIPTION',
                ],
                'deal_title_template' => 'Pré-venda Copa — {nome} ({bairro})',
            ],
        ],
    ];
}
