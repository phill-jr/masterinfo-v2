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

/**
 * Sanitiza texto livre do visitante antes de mandar pro Bitrix24.
 *
 * O Bitrix renderiza COMMENTS/TITLE (e vários UF_CRM) como HTML em telas do
 * operador → input cru = XSS ARMAZENADO no painel. Também neutraliza injeção de
 * tags/control-chars no log. APLICAR em todo valor de texto livre, não só na jornada.
 *
 * - strip_tags: remove qualquer marcação HTML/JS
 * - remove control chars perigosos (preserva \t \n \r p/ comentários multilinha)
 * - mb_substr: limita o tamanho (anti-abuso de campo / payload gigante)
 * Preserva acentuação UTF-8.
 */
function bx_sanitize_text(string $value, int $maxLen = 2000): string {
    $clean = strip_tags($value);
    // Remove NUL e demais control chars (mantém tab 0x09, LF 0x0A, CR 0x0D).
    // Sem flag /u de propósito: esses bytes nunca compõem char UTF-8 multibyte,
    // então não corrompem acentuação — e evita o null de PCRE em UTF-8 inválido.
    $stripped = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/', '', $clean);
    if ($stripped !== null) $clean = $stripped;
    return mb_substr($clean, 0, $maxLen, 'UTF-8');
}

/**
 * Normaliza um telefone brasileiro pro formato E.164 (+55DDDNUMERO).
 * Necessário pra casar com o número que o conector de WhatsApp do Bitrix grava
 * e a deduplicação por telefone funcionar — o Bitrix NÃO trata
 * "+5547999990000" e "47999990000" como o mesmo número.
 */
function bx_normalize_phone_br(string $raw): string {
    $d = preg_replace('/\D+/', '', $raw);
    if ($d === '') return '';
    // Já vem com DDI 55 (12 díg = 55+fixo, 13 díg = 55+móvel)
    if ((strlen($d) === 12 || strlen($d) === 13) && strpos($d, '55') === 0) {
        return '+' . $d;
    }
    // Número nacional: 10 díg (DDD+fixo) ou 11 díg (DDD+móvel)
    if (strlen($d) === 10 || strlen($d) === 11) {
        return '+55' . $d;
    }
    // Outros casos: best-effort, devolve com '+' (não inventa DDI)
    return '+' . $d;
}

/**
 * Procura um contato existente por telefone e/ou email (deduplicação).
 * @return int|null  ID do contato, ou null se não achar.
 */
function bx_find_contact(string $phone = '', string $email = ''): ?int {
    foreach ([['PHONE', $phone], ['EMAIL', $email]] as $pair) {
        [$type, $val] = $pair;
        if ($val === '') continue;
        try {
            $r = bx_request('crm.duplicate.findbycomm.json', [
                'type' => $type, 'values' => [$val], 'entity_type' => 'CONTACT',
            ]);
            if (!empty($r['result']['CONTACT'][0])) return (int) $r['result']['CONTACT'][0];
        } catch (\Throwable $e) {
            error_log('[bx_find_contact] ' . get_class($e) . ': ' . $e->getMessage() . ' @ ' . $e->getFile() . ':' . $e->getLine());
        }
    }
    return null;
}

/**
 * Cria um contato (faz split do nome em NAME + LAST_NAME). Telefone/email viram multifield.
 * @return int|null  ID do contato criado, ou null.
 */
function bx_create_contact(string $nome, string $phone = '', string $email = '', string $endereco = '', string $sourceId = 'WEB'): ?int {
    // Texto livre do visitante → sanitiza antes de qualquer uso (XSS no painel Bitrix).
    $nome     = bx_sanitize_text($nome, 150);
    $endereco = bx_sanitize_text($endereco, 500);
    $parts = preg_split('/\s+/', trim($nome), 2);
    $fields = [
        'NAME'      => $parts[0] ?? $nome,
        'LAST_NAME' => $parts[1] ?? '',
        'SOURCE_ID' => $sourceId,
        'OPENED'    => 'Y',
    ];
    if ($phone !== '')    $fields['PHONE']   = [['VALUE' => $phone, 'VALUE_TYPE' => 'MOBILE']];
    if ($email !== '')    $fields['EMAIL']   = [['VALUE' => $email, 'VALUE_TYPE' => 'WORK']];
    if ($endereco !== '') $fields['ADDRESS'] = $endereco;
    $r = bx_request('crm.contact.add.json', ['fields' => $fields]);
    return isset($r['result']) ? (int) $r['result'] : null;
}

/**
 * Cria um negócio (deal) vinculado a um contato.
 * @return int|null  ID do negócio criado, ou null.
 */
function bx_create_deal(string $title, ?int $contactId, $opportunity = 0, string $comments = '', $categoryId = 0, string $stageId = 'NEW', string $sourceId = 'WEB'): ?int {
    // Texto livre do visitante → sanitiza (TITLE e COMMENTS são renderizados como HTML no Bitrix).
    $title    = bx_sanitize_text($title, 250);
    $comments = $comments !== '' ? bx_sanitize_text($comments, 20000) : '';
    $fields = [
        'TITLE'       => $title,
        'CATEGORY_ID' => $categoryId,
        'STAGE_ID'    => $stageId,
        'SOURCE_ID'   => $sourceId,
        'CURRENCY_ID' => 'BRL',
        'OPENED'      => 'Y',
    ];
    if ($contactId)                                     $fields['CONTACT_ID']  = $contactId;
    if ($opportunity !== null && $opportunity !== '')   $fields['OPPORTUNITY'] = $opportunity;
    if ($comments !== '')                               $fields['COMMENTS']    = $comments;
    $r = bx_request('crm.deal.add.json', ['fields' => $fields, 'params' => ['REGISTER_SONET_EVENT' => 'Y']]);
    return isset($r['result']) ? (int) $r['result'] : null;
}

/**
 * Decide o SOURCE_ID (Origem nativa do Bitrix) pela fonte de trafego capturada.
 * Precedencia: gclid (Google Ads) > fbclid (Meta Ads) > origem do form > default das regras > WEBFORM.
 * As origens sao EDITAVEIS no admin (bitrix-mapping.json -> source_rules). Usa STATUS_ID, nunca o nome.
 * So usa fbclid (NAO fbp/fbc — esses existem em trafego organico e classificariam tudo como Meta).
 */
function bx_determine_source_id(array $data, array $cfg): string {
    $rules = bx_load_mapping()['source_rules'] ?? [];
    if (!empty($data['gclid'])  && !empty($rules['gclid']))  return bx_sanitize_text((string) $rules['gclid'], 80);
    if (!empty($data['fbclid']) && !empty($rules['fbclid'])) return bx_sanitize_text((string) $rules['fbclid'], 80);
    $fallback = $cfg['source_id'] ?? '';
    if ($fallback === '' || $fallback === 'WEB') $fallback = $rules['default'] ?? 'WEBFORM'; // 'WEB' nao existe nesse portal
    return bx_sanitize_text((string) $fallback, 80);
}

/** Posta um comentário de timeline numa entidade ('lead'|'deal'|...). Best-effort (loga, não lança). */
function bx_timeline_comment(int $entityId, string $entityType, string $comment): bool {
    // Texto livre do visitante → sanitiza (comentário de timeline renderiza HTML no Bitrix).
    $comment = bx_sanitize_text($comment, 20000);
    if ($entityId <= 0 || $comment === '') return false;
    try {
        bx_request('crm.timeline.comment.add.json', ['fields' => [
            'ENTITY_ID' => $entityId, 'ENTITY_TYPE' => $entityType, 'COMMENT' => $comment,
        ]]);
        return true;
    } catch (\Throwable $e) {
        error_log('[bx_timeline_comment] ' . get_class($e) . ': ' . $e->getMessage() . ' @ ' . $e->getFile() . ':' . $e->getLine());
        return false;
    }
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
        // Origem por fonte de trafego (SOURCE_ID dinamico) — editavel no admin (STATUS_ID, nao o nome).
        'source_rules' => [
            'gclid'   => '',          // ex.: UC_BPJ8RQ (Google Ads)
            'fbclid'  => '',          // ex.: 10|BITRIX_WHATCRM_NET_70680444 (Meta Ads)
            'default' => 'WEBFORM',   // Site (fallback organico/direto)
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
