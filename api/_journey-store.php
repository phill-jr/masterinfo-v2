<?php
/**
 * Store da "jornada do cliente" por telefone — ponte entre o cadastro (que cria
 * Contato+Lead) e o Negócio (criado depois pelo WhatsApp/conversão). Permite postar
 * o MESMO comentário de timeline no Negócio quando ele nascer.
 *
 * Persistido em secrets/journeys.json (gitignored por secrets/*). Chave = telefone E.164.
 * Usado por: api/form-submit.php (salva) e api/bitrix-deal-journey.php (lê/remove).
 */
if (!defined('MASTERINFO_INTERNAL')) { define('MASTERINFO_INTERNAL', true); }

function journey_store_path(): string {
    return __DIR__ . '/../secrets/journeys.json';
}

function journey_load(): array {
    $f = journey_store_path();
    if (!is_file($f)) return [];
    $d = json_decode((string) @file_get_contents($f), true);
    return is_array($d) ? $d : [];
}

function journey_write(array $d): bool {
    $f = journey_store_path();
    $dir = dirname($f);
    if (!is_dir($dir)) { @mkdir($dir, 0755, true); }
    return file_put_contents($f, json_encode($d, JSON_UNESCAPED_UNICODE), LOCK_EX) !== false;
}

/** Salva a jornada por telefone (normalizado). Faz prune (>30 dias) e cap (500). */
function journey_save(string $phone, string $text): bool {
    $phone = trim($phone);
    if ($phone === '' || $text === '') return false;
    $d = journey_load();
    $now = time();
    foreach ($d as $k => $v) {
        if (!isset($v['ts']) || ($now - (int) $v['ts']) > 2592000) unset($d[$k]);
    }
    if (count($d) >= 500) {
        uasort($d, function ($a, $b) { return ((int) ($a['ts'] ?? 0)) <=> ((int) ($b['ts'] ?? 0)); });
        $d = array_slice($d, -499, null, true);
    }
    $d[$phone] = ['text' => $text, 'ts' => $now];
    return journey_write($d);
}

function journey_get(string $phone): string {
    $d = journey_load();
    return (string) ($d[trim($phone)]['text'] ?? '');
}

function journey_del(string $phone): void {
    $d = journey_load();
    $phone = trim($phone);
    if (isset($d[$phone])) { unset($d[$phone]); journey_write($d); }
}
