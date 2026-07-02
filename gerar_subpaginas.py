# -*- coding: utf-8 -*-
"""Gera as 16 subpaginas (Internet + Aplicativos + Ajuda) com layout consistente.

O rodape (colunas de menu) e montado a partir de config.json -> menus.footer,
a MESMA fonte que o site-loader.js usa na home. Assim, editar o "Menu do rodape"
no admin e rerodar este script propaga a mudanca pra TODAS as paginas do site
(home via runtime + subpaginas/estaticas via este gerador)."""

import os
import re
import sys
import json

# Conteúdo (páginas-pilar + blog), fonte única do texto dessas páginas. Ver conteudo_blog.py.
from conteudo_blog import AUTHORS, PUBLISHER, PILARES, BLOG, DATE_DEFAULT, PERSONAS_CONTENT, BLOG_DEEP, BAIRROS_DEEP

# Console do Windows e cp1252 por padrao e quebra em '✓'/acentos. Forca UTF-8.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Rodape: fonte unica de verdade = config.json -> menus.footer (a mesma da home).
with open(os.path.join(BASE_DIR, "config.json"), encoding="utf-8") as _cfg_f:
    CONFIG = json.load(_cfg_f)
FOOTER_MENUS = CONFIG.get("menus", {}).get("footer", [])

# Escala do site (admin -> config.layout.siteScale, em %). Na home o site-loader.js
# seta a CSS var em runtime; as subpaginas sao estaticas, entao a gente "assa" o
# valor num <style> no <head>. Default 100 = 1 (sem mudanca; cai no default do CSS).
SITE_SCALE = round((CONFIG.get("layout", {}).get("siteScale", 100) or 100) / 100, 3)

# Planos do config.json indexados por id, fonte unica dos campos de texto dos
# cards das subpaginas (nome/velocidade/unidade/precos/features). A faixa de apps
# inclusos continua curada no PLANS_MAP. Em runtime o <script data-mi-plans>
# (PLANS_SYNC_SCRIPT) refaz a mesma sincronizacao, entao editar no admin reflete
# sem precisar re-gerar.
CFG_PLANS_BY_ID = {p.get("id"): p for p in CONFIG.get("planos", [])}


def fmt_brl(n):
    """Numero do config (99.99) -> string BR '99,99'. None -> '' (cai no fallback)."""
    if n is None:
        return ""
    return f"{float(n):.2f}".replace(".", ",")

# ─── DADOS DAS PÁGINAS ────────────────────────────────────────────────

INTERNET = [
    {
        "slug": "home-office",
        "tag": "INTERNET · TRABALHO",
        "title": "Internet pra trabalhar de casa",
        "subtitle": "Estabilidade pra reunião não cair, upload turbinado pra mandar arquivos pesados e ping baixo pra responder rápido.",
        "ico": "ph-briefcase",
        "gradient": "linear-gradient(135deg, #c1121f 0%, #ff7a05 50%, #fcc305 100%)",
        "highlights": [
            ("📞", "Reunião sem queda", "Conexão estável pra Zoom, Teams, Meet, chovendo ou fazendo sol."),
            ("☁️", "Upload turbinado", "Mandar arquivo grande, fazer backup em nuvem, sem espera."),
            ("⚡", "Latência baixa", "Resposta rápida em ferramentas em tempo real."),
        ],
        "plans": ["lite-premium", "ultra-home-office"],
        "cta": "Quero internet pra home office",
    },
    {
        "slug": "gamer",
        "tag": "INTERNET · GAMER",
        "title": "Internet de gamer, de verdade",
        "subtitle": "Ping baixo, jitter controlado e zero perda de pacote. Pra você não perder ranked por causa da net.",
        "ico": "ph-game-controller",
        "gradient": "linear-gradient(135deg, #2d0407 0%, #8b0a17 40%, #e63946 100%)",
        "highlights": [
            ("🎮", "Ping até 8ms", "Conexão direta com São Paulo, ideal pra Valorant, CS, LoL."),
            ("🔥", "Zero perda de pacote", "Não vai mais cair partida ranqueada no meio."),
            ("📡", "Fibra dedicada", "Sem cabo compartilhado com vizinho fazendo download."),
        ],
        "plans": ["ultra-gamer", "lite-basic"],
        "cta": "Quero internet de gamer",
    },
    {
        "slug": "familia",
        "tag": "INTERNET · PRA FAMÍLIA",
        "title": "Internet pra família toda usar ao mesmo tempo",
        "subtitle": "Vários celulares, TV no streaming, criança no tablet, jogo do filho online, tudo junto, sem travar. Wi-Fi com força pra casa cheia.",
        "ico": "ph-users-three",
        "gradient": "linear-gradient(135deg, #c1121f 0%, #ff7a05 50%, #fcc305 100%)",
        "highlights": [
            ("👨‍👩‍👧‍👦", "Tudo rodando junto", "Mãe na novela, pai no jogo, filhos no TikTok, tudo ao mesmo tempo, sem trava."),
            ("📺", "Streaming em 4K", "Netflix, Disney+, Globoplay e SKY+ rodando em qualquer TV da casa."),
            ("🛡️", "Wi-Fi seguro pra criança", "Suporte pra controle parental e antivírus Kaspersky opcional."),
        ],
        "plans": ["lite-premium", "ultra-familia"],
        "cta": "Quero internet pra família",
    },
    {
        "slug": "com-2-roteadores",
        "tag": "INTERNET · WI-FI EM TODA A CASA",
        "title": "Wi-Fi em toda a casa, sem ponto cego",
        "subtitle": "Com 2 roteadores em rede mesh, você navega forte da cozinha ao quintal. Mesma velocidade em qualquer cômodo.",
        "ico": "ph-broadcast",
        "gradient": "linear-gradient(135deg, #8b0a17 0%, #e63946 50%, #ff7a05 100%)",
        "highlights": [
            ("📶", "Cobertura total", "Dois roteadores cobrem casas grandes, sobrados e quintal."),
            ("🔄", "Rede inteligente", "Seu celular troca de roteador sozinho, sem cair conexão."),
            ("🚀", "Wi-Fi 6", "Velocidade máxima nos dispositivos modernos."),
        ],
        "plans": ["ultra-familia", "ultra-home-office", "ultra-gamer"],
        "cta": "Quero Wi-Fi em toda a casa",
    },
    {
        "slug": "com-1-roteador",
        "tag": "INTERNET · ENTRADA",
        "title": "Internet boa pra apartamento e casa pequena",
        "subtitle": "Plano essencial com Wi-Fi cobrindo bem o ambiente. Pra quem quer fibra de verdade sem pagar caro.",
        "ico": "ph-wifi-high",
        "gradient": "linear-gradient(135deg, #6b3d00 0%, #c19000 50%, #fcc305 100%)",
        "highlights": [
            ("🏠", "Ideal pra apartamento", "Cobertura Wi-Fi suficiente em até 80m²."),
            ("💸", "Preço justo", "A partir de R$ 99,99/mês, sem letra miúda."),
            ("⚡", "Fibra óptica real", "Mesmo plano de entrada, mesma fibra dos planos premium."),
        ],
        "plans": ["lite-casa", "lite-premium", "lite-basic"],
        "cta": "Quero plano com 1 roteador",
    },
]

# Mescla o conteúdo aprofundado (corpo editorial + FAQ) revisado nas personas correspondentes.
for _it in INTERNET:
    _pc = PERSONAS_CONTENT.get(_it["slug"])
    if _pc:
        _it["body"] = _pc["body"]
        _it["faq"] = [(x["q"], x["a"]) for x in _pc["faq"]]

# Mescla os corpos aprofundados dos posts do blog (BLOG_DEEP).
for _b in BLOG:
    _bd = BLOG_DEEP.get(_b["slug"])
    if _bd:
        _b["body"] = _bd["body"]
        _b["faq"] = [(x["q"], x["a"]) for x in _bd["faq"]]

# Insere a seção "Sobre o bairro" (BAIRROS_DEEP, fatos pesquisados/verificados) nas páginas de bairro,
# antes de "Internet para cada necessidade", preservando o resto (mapa etc.) + amplia a FAQ.
for _p in PILARES:
    _sd = BAIRROS_DEEP.get(_p["slug"])
    if _sd:
        _anchor = '<h2>Internet para cada necessidade</h2>'
        if _anchor in _p["body"]:
            _p["body"] = _p["body"].replace(_anchor, _sd["section"] + '\n\n    ' + _anchor, 1)
        else:
            _p["body"] = _p["body"] + '\n\n    ' + _sd["section"]
        _p["faq"] = list(_p.get("faq", [])) + [(x["q"], x["a"]) for x in _sd["faq_extra"]]

APLICATIVOS = [
    # cats: em quais categorias do PlayHub esse app aparece (cruzado em compute_escolher_em)
    {"slug": "sky-light", "name": "SKY+ Light", "tag": "TV ao vivo",
     "desc": "Canais de TV no celular, smart TV ou computador. Esportes, jornalismo, novelas, onde você estiver.",
     "logo": "sky.jpg",
     "highlights": ["50+ canais ao vivo", "App pra smart TV, celular e PC", "Sem antena, sem parabólica"],
     "cats": ["standard", "advanced", "top"]},  # SKY+ Light (std), c/ Globo (adv), SKY+ (top)
    {"slug": "deezer", "name": "Deezer", "tag": "Música sem anúncios",
     "desc": "Mais de 90 milhões de músicas em alta qualidade. Sem propaganda, modo offline, playlists personalizadas.",
     "logo": "deezer.webp",
     "highlights": ["90M+ músicas em HD", "Modo offline (baixe e ouça sem net)", "Sem nenhum anúncio"],
     "cats": ["advanced"]},
    {"slug": "globoplay", "name": "Globoplay", "tag": "Novelas e esportes",
     "desc": "Novelas inéditas, séries originais, futebol ao vivo e tudo da Globo on demand.",
     "logo": "globoplay.png",
     "highlights": ["Novelas e séries Globo", "Futebol ao vivo (Brasileirão, Libertadores)", "Filmes Telecine inclusos"],
     "cats": ["top", "premium"]},
    {"slug": "disney-plus", "name": "Disney+", "tag": "Disney, Pixar, Marvel",
     "desc": "Disney, Pixar, Marvel, Star Wars e National Geographic. Tudo em um único app.",
     "logo": "disney-plus.png",
     "highlights": ["Tudo da Disney, Pixar, Marvel", "Star Wars e Nat Geo", "4K, Dolby Atmos"],
     "cats": ["top", "premium"]},  # TOP (Ads) + Premium (sem ads)
    {"slug": "hbo-max", "name": "HBO Max", "tag": "Séries premium e Warner",
     "desc": "Séries originais da HBO, filmes Warner, DC, Cartoon Network. As maiores produções num só lugar.",
     "logo": "hbo-max.jpg",
     "highlights": ["Game of Thrones, House of the Dragon, The Last of Us", "Filmes Warner em estreia", "DC Universe completo"],
     "cats": ["top", "premium"]},  # TOP (Ads) + Premium (sem ads)
    {"slug": "prime-video", "name": "Prime Video", "tag": "Amazon Originals",
     "desc": "Séries originais Amazon (The Boys, Reacher, Rings of Power), filmes em estreia e clássicos.",
     "logo": "prime-video.png",
     "highlights": ["The Boys, Reacher, Fallout", "Filmes em estreia", "Combo com SKY+ Light disponível"],
     "cats": ["top"]},
    {"slug": "exitlag", "name": "Exitlag", "tag": "Otimizador pra gamers",
     "desc": "Reduz seu ping até 70% em jogos online: Valorant, CS, LoL, Fortnite. Conexão otimizada por servidores dedicados.",
     "logo": "exitlag.png",
     "highlights": ["Ping até 70% menor", "Suporta 1.000+ jogos", "Servidores dedicados pra gamers"],
     "cats": ["standard"]},
    {"slug": "kaspersky", "name": "Kaspersky", "tag": "Antivírus premium",
     "desc": "Proteção completa pra até 5 dispositivos. Antivírus, VPN, gerenciador de senhas e proteção pra crianças.",
     "logo": "kaspersky.webp",
     "highlights": ["Protege seu PC, celular e da família", "VPN ilimitada inclusa", "Controle parental e antivírus"],
     "cats": ["standard", "advanced", "premium"]},  # 1 Lic (std), 3 Lic (adv), 5 Lic (prem)
]


def compute_escolher_em(app_cats):
    """Cruza as categorias PlayHub do app com os planos do config.json e
    retorna lista [(nome_plano, categoria_nome)...] dos planos que liberam
    pelo menos uma das categorias do app. Ex.: app SKY+ Light tem cats=[standard,
    advanced, top] -> retorna [(Lite Casa, Standard), (Lite Premium, Advanced),
    (Ultra Home Office, Standard), (Ultra Gamer, TOP)] etc."""
    planos = CONFIG.get("planos") or []
    playhub = CONFIG.get("playhub") or []
    cat_nome = {c["id"]: c.get("nome", c["id"]) for c in playhub}
    out = []
    for p in planos:
        p_cats = p.get("categorias") or []
        # Pega a PRIMEIRA cat do plano que casa com as do app (evita duplicar plano)
        match_cat = next((c for c in p_cats if c in app_cats), None)
        if match_cat:
            out.append((p.get("nome", p.get("id", "?")), cat_nome.get(match_cat, match_cat)))
    return out

AJUDA = [
    {
        "slug": "wifi",
        "tag": "AJUDA · WI-FI",
        "title": "Como configurar seu Wi-Fi",
        "subtitle": "Trocar o nome da rede, mudar a senha e deixar o sinal forte em toda a casa, passo a passo, sem complicação.",
        "gradient": "linear-gradient(135deg, #6b3d00 0%, #c19000 50%, #fcc305 100%)",
        "steps": [
            ("🔑", "Trocar a senha do Wi-Fi", "Acesse o painel do roteador (geralmente 192.168.0.1 ou 192.168.1.1) com o login do aparelho e altere o campo de senha da rede."),
            ("📶", "Deixar o sinal mais forte", "Posicione o roteador num ponto central e alto, longe de paredes grossas, micro-ondas e espelhos. Casa grande pede o plano com 2 roteadores (mesh)."),
            ("🔄", "Reiniciar quando travar", "Tire o roteador da tomada por 30 segundos e ligue de novo, resolve a maioria das lentidões momentâneas."),
        ],
        "cta_label": "Falar com o suporte no WhatsApp",
        "cta_href": "https://wa.me/554734341734?text=Ol%C3%A1!%20Preciso%20de%20ajuda%20para%20configurar%20meu%20Wi-Fi.",
    },
    {
        "slug": "reportar",
        "tag": "AJUDA · SUPORTE",
        "title": "Reportar um problema",
        "subtitle": "Sem internet, conexão lenta ou caindo? Nossa equipe local resolve rápido. Conte o que está acontecendo.",
        "gradient": "linear-gradient(135deg, #8b0a17 0%, #e63946 50%, #ff7a05 100%)",
        "steps": [
            ("🚫", "Sem conexão", "Confira se as luzes do roteador estão acesas e tente reiniciá-lo. Se continuar sem internet, fale com a gente."),
            ("🐢", "Internet lenta", "Faça um teste de velocidade pelo Speedtest conectado por cabo, anote o resultado e mande pra gente avaliar."),
            ("📡", "Quedas constantes", "Anote os horários em que cai, isso ajuda nossa equipe a identificar a causa mais rápido."),
        ],
        "cta_label": "Abrir chamado no WhatsApp",
        "cta_href": "https://wa.me/554734341734?text=Ol%C3%A1!%20Quero%20reportar%20um%20problema%20na%20minha%20internet.",
    },
    {
        "slug": "boletos",
        "tag": "AJUDA · FINANCEIRO",
        "title": "Boletos e faturas",
        "subtitle": "Segunda via, vencimento e formas de pagamento, tudo na Central do Assinante, quando você quiser.",
        "gradient": "linear-gradient(135deg, #06402b 0%, #0a7d4f 50%, #18b368 100%)",
        "steps": [
            ("🧾", "Segunda via do boleto", "Acesse a Central do Assinante com seu login para baixar a 2ª via e copiar o código de barras na hora."),
            ("📅", "Vencimento e histórico", "Consulte faturas anteriores, datas de vencimento e os pagamentos já realizados."),
            ("💳", "Formas de pagamento", "Boleto, Pix e cartão. Pagando em dia você garante o desconto do seu plano."),
        ],
        "cta_label": "Acessar a Central do Assinante",
        "cta_href": "https://sistema1.masterinfointernet.com/central_assinante_web/login",
        "chat": True,
    },
]

PLANS_MAP = {
    # ─── LINHA LITE, 1 Roteador Wi-Fi 6 ───
    "lite-casa": {
        "nome": "Lite Casa", "linha": "LITE",
        "speed": "600", "unit": "Mega",
        "preco": "99,99", "preco_cheio": "109,99",
        "apps": [{"logo": "sky.jpg", "nome": "App Master Standard"}],
        "features": [
            "Wi-Fi 6 em 1 ambiente",
            "1 app de TV / mês (categoria Standard)",
            "Suporte Sábado e Domingo",
        ],
    },
    "lite-premium": {
        "nome": "Lite Premium", "linha": "LITE",
        "speed": "800", "unit": "Mega",
        "preco": "119,90", "preco_cheio": "129,90",
        "apps": [{"logo": "sky.jpg", "nome": "App Master Advanced"}],
        "features": [
            "Wi-Fi 6 em 1 ambiente",
            "1 app de TV / mês (categoria Advanced)",
            "Velocidade pra família",
        ],
    },
    "lite-basic": {
        "nome": "Lite Basic", "linha": "LITE",
        "speed": "1", "unit": "Giga",
        "preco": "129,00", "preco_cheio": "139,00",
        "apps": [],
        "features": [
            "Wi-Fi 6 em 1 ambiente",
            "Sem app de TV (velocidade pura)",
            "1 Giga pra trabalho remoto",
        ],
    },
    # ─── LINHA ULTRA, Mesh Wi-Fi 6 ───
    "ultra-familia": {
        "nome": "Ultra Família", "linha": "ULTRA",
        "speed": "1", "unit": "Giga",
        "preco": "149,90", "preco_cheio": "159,90",
        "apps": [{"logo": "disney-plus.png", "nome": "App Master Premium"}],
        "features": [
            "Mesh Wi-Fi 6 (cobertura total)",
            "1 app de TV / mês (categoria Premium)",
            "Streaming sem trava em qualquer canto",
        ],
    },
    "ultra-home-office": {
        "nome": "Ultra Home Office", "linha": "ULTRA",
        "speed": "1", "unit": "Giga",
        "preco": "179,90", "preco_cheio": "189,90",
        "apps": [
            {"logo": "globoplay.png", "nome": "App Master TOP"},
            {"logo": "sky.jpg", "nome": "App Master Advanced"},
            {"logo": "kaspersky.webp", "nome": "Kaspersky"},
        ],
        "apps_sep": "+",
        "features": [
            "Mesh Wi-Fi 6 (cobertura total)",
            "3 apps de TV / mês (TOP + Advanced + Standard)",
            "Kaspersky pra segurança dos dados",
        ],
    },
    "ultra-gamer": {
        "nome": "Ultra Gamer", "linha": "ULTRA",
        "speed": "1", "unit": "Giga",
        "preco": "189,90", "preco_cheio": "199,90",
        "apps": [
            {"logo": "exitlag.png", "nome": "ExitLag"},
            {"logo": "globoplay.png", "nome": "App Master TOP"},
        ],
        "apps_sep": "+",
        "features": [
            "Mesh Wi-Fi 6 (cobertura total)",
            "2 apps de TV / mês (TOP + Premium)",
            "ExitLag, ping mínimo no online",
        ],
    },
}

# ─── HEADER + FOOTER COMUNS ──────────────────────────────────────────

# config.json compartilhado (1 fetch/página em vez de N). Plain string (sem f) p/ as chaves
# JS serem literais; inserido no <head> via {CFG_SHIM} no f-string do head().
CFG_SHIM = "<script>window.miCfg=window.miCfg||function(){return window.__miCfgP||(window.__miCfgP=fetch('/config.json?v='+Date.now()).then(function(r){return r.json();}));};</script>"


def head(title, depth, extra_head=""):
    base = "../" * depth
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {CFG_SHIM}
  <title>{title} | MasterInfo Internet</title>
  <meta name="description" content="MasterInfo Internet, fibra óptica 100% em Joinville.">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
  <noscript><link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet"></noscript>
  <link rel="stylesheet" href="/vendor/phosphor/phosphor.css?v=20260619" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="/vendor/phosphor/phosphor.css?v=20260619"></noscript>
  <link rel="icon" type="image/svg+xml" href="{base}favicon.svg">
  <link rel="icon" type="image/png" sizes="96x96" href="{base}favicon-96x96.png">
  <link rel="icon" href="{base}favicon.ico" sizes="any">
  <link rel="apple-touch-icon" sizes="180x180" href="{base}apple-touch-icon.png">
  <link rel="stylesheet" href="{base}styles.css?v=20260531-e">
  <link rel="stylesheet" href="{base}modal.css?v=20260531-e">
  {extra_head}
  <style>:root{{--site-scale:{SITE_SCALE}}}</style>
</head>
<body>'''


def build_header(depth):
    """Monta o <header> a partir de config.menuHeader, o MESMO resultado que o
    site-loader.loadMenuHeader produz na home: UMA lista (.nav-list-sales) na
    ordem do config, itens com on=False OMITIDOS (ex.: TV e Streaming), dropdowns
    (com logos/filhos) e botao do cliente do config. hrefs traduzidos por
    profundidade. Sem o divisor / a lista da direita (menu vira uma linha unica)."""
    base = "../" * depth
    mh = CONFIG.get("menuHeader") or {}
    lis = []
    for it in (mh.get("itens") or []):
        if it.get("on") is False:            # respeita o liga/desliga do admin
            continue
        if it.get("tipo") == "drop":
            kids = []
            for c in (it.get("children") or []):
                tgt = f' target="{c["target"]}" rel="noopener"' if c.get("target") else ''
                logo = (f'<img class="dropdown-logo dropdown-logo-real" src="{footer_href(c["logo"], base)}" alt="{c.get("label", "")}" loading="lazy">'
                        if c.get("logo") else '')
                kids.append(f'                  <li><a href="{footer_href(c.get("href", "#"), base)}"{tgt} class="dropdown-link">{logo}{c.get("label", "")}</a></li>')
            lis.append("\n".join([
                '          <li class="nav-item has-mega">',
                f'            <button class="nav-trigger" type="button">{it.get("label", "")} <i class="ph ph-caret-down nav-trigger-caret"></i></button>',
                '            <div class="mega-menu mega-menu-simple">',
                '              <div class="mega-menu-inner">',
                '                <ul class="dropdown-list">',
                *kids,
                '                </ul>',
                '              </div>',
                '            </div>',
                '          </li>',
            ]))
        else:                                 # tipo "link"
            tgt = f' target="{it["target"]}" rel="noopener"' if it.get("target") else ''
            lis.append(f'          <li class="nav-item"><a href="{footer_href(it.get("href", "#"), base)}"{tgt} class="nav-link">{it.get("label", "")}</a></li>')

    cb = mh.get("clientButton") or {}
    return "\n".join([
        '<header class="header" id="header">',
        '    <div class="container header-inner">',
        f'      <a href="{base}" class="logo">',
        f'        <img src="{base}imgs/logo-masterinfo.png" alt="MasterInfo Internet" class="logo-img">',
        '      </a>',
        '      <nav class="nav" id="nav">',
        '        <ul class="nav-list nav-list-sales">',
        *lis,
        '        </ul>',
        f'        <a href="{cb.get("href", "#")}" target="{cb.get("target", "_blank")}" rel="noopener" class="header-client-btn">',
        f'          <i class="ph-fill ph-user-circle"></i><span>{cb.get("label", "Área do Cliente")}</span>',
        '        </a>',
        '      </nav>',
        '      <button class="mobile-toggle" id="mobileToggle" aria-label="Menu"><span></span><span></span><span></span></button>',
        '    </div>',
        '    <div class="mega-backdrop" id="megaBackdrop"></div>',
        '  </header>',
    ])


def header(depth):
    # O <header> sai do config.menuHeader (build_header), igual à home.
    return f'''
  <!-- HEADER -->
  {build_header(depth)}'''


def footer_href(href, base):
    """Traduz um href do config (relativo a home) pro contexto de uma subpagina.

    O config guarda os caminhos como na home: "/familia" (root-absolute) e
    "#cobertura" (ancora de secao da home). Numa subpagina em profundidade
    `depth`, base = "../"*depth. Links externos (http/mailto/tel) passam intactos.
    """
    if href.startswith(("http://", "https://", "mailto:", "tel:")):
        return href
    if href.startswith("#"):              # ancora de secao -> sobe pra home + ancora
        return f"{base}{href}"
    if href.startswith("/"):              # root-absolute -> relativo a esta pagina
        path = href[1:]
        last = path.split("/")[-1]
        if path and "." not in last and "#" not in path and not path.endswith("/"):
            path += "/"                   # diretorio -> barra final (evita redirect 301)
        return f"{base}{path}"
    return f"{base}{href}"                 # ja relativo


def render_footer_cols(base):
    """Monta as 3 colunas <div class="footer-col"> a partir de config.menus.footer.

    Indentacao de 8 espacos pra casar com o template e as paginas estaticas.
    Adiciona rel="noopener" em todo link target="_blank" (boa pratica)."""
    blocks = []
    for col in FOOTER_MENUS:
        lines = ['        <div class="footer-col">',
                 f'          <h4>{col.get("titulo", "")}</h4>']
        for l in col.get("links", []):
            icon = f'<i class="{l["icone"]}"></i> ' if l.get("icone") else ''
            tgt = f' target="{l["target"]}" rel="noopener"' if l.get("target") else ''
            href = footer_href(l.get("href", "#"), base)
            lines.append(f'          <a href="{href}"{tgt}>{icon}{l.get("label", "")}</a>')
        lines.append('        </div>')
        blocks.append("\n".join(lines))
    return "\n".join(blocks)


def footer(depth, boleto=True, extra_scripts=""):
    base = "../" * depth
    boleto_html = (f'''
  <!-- ========== BOLETO / 2ª VIA FLOAT ========== -->
  <a href="/ajuda/boletos/" class="boleto-float" aria-label="Boletos e 2ª via de fatura">
    <span class="boleto-tooltip">
      <span class="boleto-tooltip-text">2ª via de boleto</span>
      <span class="boleto-tooltip-sub">Chat na hora com a Marina</span>
    </span>
    <i class="ph-fill ph-barcode"></i>
    <span class="boleto-pulse"></span>
  </a>
  <script src="{base}marina-widget.js?v=20260617-a" defer></script>''') if boleto else ""
    return f'''
  <!-- FOOTER -->
  <footer class="footer" id="contato">
    <div class="footer-trust">
      <div class="container footer-trust-inner">
        <div class="footer-trust-item"><i class="ph-fill ph-star"></i><div><strong>4,8 / 5</strong><span>2.450 avaliações no Google</span></div></div>
        <div class="footer-trust-item"><i class="ph-fill ph-lightning"></i><div><strong>100% Fibra Óptica</strong><span>Sem rádio, sem cabo compartilhado</span></div></div>
        <div class="footer-trust-item"><i class="ph-fill ph-map-pin"></i><div><strong>100% Joinville</strong><span>Atendimento local, equipe da região</span></div></div>
        <div class="footer-trust-item"><i class="ph-fill ph-handshake"></i><div><strong>Suporte que resolve</strong><span>Fala com gente de verdade</span></div></div>
      </div>
    </div>
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a href="{base}" class="logo"><img src="{base}imgs/logo-masterinfo.png" alt="MasterInfo Internet" class="logo-img"></a>
          <p>Internet fibra óptica de verdade. Mais de 6 anos conectando famílias e empresas.</p>
          <div class="footer-social">
            <a href="https://www.instagram.com/masterinfo.internet" target="_blank" rel="noopener"><i class="ph ph-instagram-logo"></i></a>
            <a href="https://www.facebook.com/masterinfointernet" target="_blank" rel="noopener"><i class="ph ph-facebook-logo"></i></a>
            <a href="https://wa.me/554734341734" target="_blank" rel="noopener"><i class="ph ph-whatsapp-logo"></i></a>
          </div>
        </div>
{render_footer_cols(base)}
      </div>
      <div class="footer-payment">
        <span class="footer-payment-label">Formas de pagamento</span>
        <div class="footer-payment-icons">
          <span class="payment-icon"><i class="ph-fill ph-currency-circle-dollar"></i> PIX</span>
          <span class="payment-icon"><i class="ph-fill ph-barcode"></i> Boleto</span>
          <span class="payment-icon"><i class="ph-fill ph-credit-card"></i> Cartão</span>
        </div>
      </div>
      <div class="footer-bottom">
        <p id="footerCnpj">&copy; 2026 MasterInfo Internet. Todos os direitos reservados. CNPJ: 08.990.505/0001-52</p>
        <div class="footer-legal">
          <a href="/termos/">Termos de Uso</a><span>·</span>
          <a href="/privacidade/">Política de Privacidade</a><span>·</span>
          <a href="/lgpd/">LGPD</a>
        </div>
      </div>
    </div>
  </footer>

  <a href="https://wa.me/5547989212991" class="whatsapp-float" target="_blank" rel="noopener">
    <span class="whatsapp-tooltip">
      <span class="whatsapp-tooltip-online"><span class="whatsapp-online-dot"></span> Online agora</span>
      <span class="whatsapp-tooltip-text">Fala com a gente!</span>
    </span>
    <i class="ph-fill ph-whatsapp-logo"></i>
    <span class="whatsapp-pulse"></span>
  </a>

  <script>
  (function() {{
    var navItems = document.querySelectorAll('.nav-item.has-mega');
    navItems.forEach(function(item) {{
      var trigger = item.querySelector('.nav-trigger');
      if (trigger) {{
        trigger.addEventListener('click', function(e) {{
          e.preventDefault();
          var wasOpen = item.classList.contains('is-open');
          navItems.forEach(function(it) {{ it.classList.remove('is-open'); }});
          if (!wasOpen) item.classList.add('is-open');
        }});
      }}
    }});
    document.addEventListener('click', function(e) {{
      if (!e.target.closest('.nav-item.has-mega') && !e.target.closest('.mega-menu')) {{
        navItems.forEach(function(it) {{ it.classList.remove('is-open'); }});
      }}
    }});
    var mt = document.getElementById('mobileToggle');
    var nv = document.getElementById('nav');
    if (mt && nv) mt.addEventListener('click', function() {{
      mt.classList.toggle('active'); nv.classList.toggle('open');
    }});

    // Slideshow do hero (rotaciona slides com fade)
    var slideshow = document.querySelector('.sub-hero-slideshow');
    if (slideshow) {{
      var slides = slideshow.querySelectorAll('.sub-hero-slide');
      var interval = parseInt(slideshow.getAttribute('data-interval'), 10) || 5000;
      if (slides.length > 1) {{
        var current = 0;
        setInterval(function() {{
          slides[current].classList.remove('is-active');
          current = (current + 1) % slides.length;
          slides[current].classList.add('is-active');
        }}, interval);
      }}
    }}
  }})();
  </script>
{boleto_html}
{extra_scripts}
  <script src="/tracking.js?v=20260627a" defer></script>
  <script src="/cookie-consent.js?v=20260603-cc"></script>
</body>
</html>'''


# ─── TEMPLATES DAS PÁGINAS ────────────────────────────────────────────

# Imagens de fundo do hero das subpáginas Internet.
# Aceita extensões: jpg, png, webp (ordem de preferência).
IMG_BG = {
    "home-office":      "home-office",
    "gamer":            "gamer",
    "familia":          "familia",
    "com-2-roteadores": "2-roteadores",
    "com-1-roteador":   "1-roteador",
}

def find_img(slug, base_path):
    """Encontra arquivo imgs/hero/sub/{slug}.{ext} (single) no disco."""
    for ext in ("jpg", "jpeg", "png", "webp"):
        rel = f"imgs/hero/sub/{slug}.{ext}"
        if os.path.exists(os.path.join(base_path, rel)):
            return rel
    return None


def find_imgs(slug, base_path):
    """Encontra todas imagens imgs/hero/sub/{slug}-N.{ext} (slideshow). Fallback: single."""
    imgs = []
    for i in range(1, 21):  # até 20 slides
        for ext in ("jpg", "jpeg", "png", "webp"):
            rel = f"imgs/hero/sub/{slug}-{i}.{ext}"
            if os.path.exists(os.path.join(base_path, rel)):
                imgs.append(rel)
                break
    if imgs:
        return imgs
    # fallback: imagem única
    single = find_img(slug, base_path)
    return [single] if single else []


# Patcher de runtime das subpaginas: le config.json e atualiza os .sub-plan-card
# (nome/velocidade/unidade/precos/features) ao vivo, mesma ideia do data-mi-widgets.
# Assim, editar um plano no admin reflete nas subpaginas sem precisar re-gerar. A
# faixa de apps inclusos (curada) nao e tocada.
PLANS_SYNC_SCRIPT = """<script data-mi-plans>(function(){function brl(n){return Number(n).toFixed(2).replace('.',',');}function esc(s){var d=document.createElement('div');d.textContent=(s==null?'':s);return d.innerHTML;}var A={'600':'lite-casa','800':'lite-familia','1000':'lite-home-office','ultra-800':'ultra-familia','ultra-1000':'ultra-home-office'};try{(window.miCfg?window.miCfg():fetch('/config.json?v='+Date.now()).then(function(r){return r.json();})).then(function(c){var b={};(c.planos||[]).forEach(function(p){b[p.id]=p;});document.querySelectorAll('a.sub-plan-card[href*="checkout.html?plano="]').forEach(function(card){var m=card.getAttribute('href').match(/plano=([^&]+)/);if(!m)return;var p=b[A[m[1]]||m[1]];if(!p)return;var sp=card.querySelector('.sub-plan-speed');if(sp&&p.velocidade!=null)sp.innerHTML=esc(p.velocidade)+'<small> '+esc(p.unidade||'Mega')+'</small>';var nm=card.querySelector('.sub-plan-name');if(nm&&p.nome!=null)nm.textContent=p.nome;var po=card.querySelector('.sub-plan-price-original');if(po&&p.precoCheio!=null)po.innerHTML='de <s>R$ '+brl(p.precoCheio)+'</s> por';var pr=card.querySelector('.sub-plan-price');var pt=(p.precoPontual!=null?p.precoPontual:p.precoCheio);if(pr&&pt!=null)pr.innerHTML='R$ '+brl(pt)+' <em>/mês</em>';var ul=card.querySelector('.sub-plan-features');if(ul&&p.features&&p.features.length)ul.innerHTML=p.features.map(function(f){return '<li><i class="ph-fill ph-check-circle"></i> '+esc(f)+'</li>';}).join('');});}).catch(function(){});}catch(e){}})();</script>"""


def page_internet(p, depth=1):
    plan_cards = ""
    for plan_id in p["plans"]:
        plan = PLANS_MAP[plan_id]
        cfg = CFG_PLANS_BY_ID.get(plan_id, {})

        # Campos de texto: config.json e a fonte unica; PLANS_MAP e so fallback.
        nome = cfg.get("nome") or plan["nome"]
        speed = cfg.get("velocidade") or plan["speed"]
        unit = cfg.get("unidade") or plan.get("unit", "Mega")
        preco = fmt_brl(cfg.get("precoPontual")) or plan["preco"]
        preco_cheio = fmt_brl(cfg.get("precoCheio")) or plan["preco_cheio"]
        features = cfg.get("features") or plan["features"]

        # Faixa de apps (curada no PLANS_MAP, fica como esta)
        apps_html = ""
        sep = plan.get("apps_sep")
        for i, app in enumerate(plan["apps"]):
            if i > 0 and sep:
                apps_html += f'<span class="sub-plan-app-sep">{sep}</span>'
            apps_html += f'''
            <div class="sub-plan-app">
              <img src="../imgs/{app["logo"]}" alt="{app["nome"]}" class="sub-plan-app-logo">
              <span class="sub-plan-app-name">{app["nome"]}</span>
            </div>'''

        # Features
        features_html = "".join(
            f'<li><i class="ph-fill ph-check-circle"></i> {f}</li>'
            for f in features
        )

        plan_cards += f'''
        <a href="../checkout.html?plano={plan_id}" class="sub-plan-card">
          <div class="sub-plan-head">
            <span class="sub-plan-speed">{speed}<small> {unit}</small></span>
            <span class="sub-plan-name">{nome}</span>
          </div>
          <div class="sub-plan-price-wrap">
            <span class="sub-plan-price-original">de <s>R$ {preco_cheio}</s> por</span>
            <span class="sub-plan-price">R$ {preco} <em>/mês</em></span>
            <span class="sub-plan-discount"><i class="ph-fill ph-tag"></i> R$ 10+ OFF pagando em dia</span>
          </div>
          <div class="sub-plan-apps">
            <span class="sub-plan-apps-label">INCLUSO</span>
            <div class="sub-plan-apps-list">{apps_html}
            </div>
          </div>
          <ul class="sub-plan-features">{features_html}
          </ul>
          <span class="sub-plan-cta">Ver detalhes <i class="ph ph-arrow-right"></i></span>
        </a>'''

    highlights_html = ""
    for emoji, title, desc in p["highlights"]:
        highlights_html += f'''
        <div class="sub-highlight">
          <div class="sub-highlight-emoji">{emoji}</div>
          <h3>{title}</h3>
          <p>{desc}</p>
        </div>'''

    imgs = find_imgs(IMG_BG.get(p["slug"], ""), BASE_DIR)
    if len(imgs) >= 2:
        slides_html = "\n      ".join(
            f'<div class="sub-hero-slide{" is-active" if i == 0 else ""}" style="background-image: url(\'../{img}\');"></div>'
            for i, img in enumerate(imgs)
        )
        hero_open = f'<section class="sub-hero sub-hero-slideshow" data-interval="5000" style="background: {p["gradient"]};">\n      {slides_html}\n      <div class="sub-hero-overlay"></div>'
    elif len(imgs) == 1:
        style = f"background-image: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.4)), url('../{imgs[0]}'); background-size: cover; background-position: center;"
        hero_open = f'<section class="sub-hero" style="{style}">'
    else:
        hero_open = f'<section class="sub-hero" style="background: {p["gradient"]};">'

    # Conteúdo editorial aprofundado + FAQ (opcionais; mesma estrutura/estilo das pilares).
    extra = f'<link rel="stylesheet" href="/blog.css?v={BLOGCSS_VER}">' if (p.get("body") or p.get("faq")) else ""
    article = f'\n  <div class="article-band">\n    <div class="article">{p["body"]}\n    </div>\n  </div>' if p.get("body") else ""
    faq_html, faq_jsonld = render_faq(p.get("faq", []))
    return f'''{head(p["title"], depth, extra)}
{header(depth)}

  <!-- HERO da subpágina -->
  {hero_open}
    <div class="container sub-hero-inner">
      <span class="sub-hero-tag">{p["tag"]}</span>
      <h1 class="sub-hero-title">{p["title"]}</h1>
      <p class="sub-hero-subtitle">{p["subtitle"]}</p>
      <a href="../checkout.html?plano={p["plans"][0]}" class="sub-hero-cta">{p["cta"]} <i class="ph ph-arrow-right"></i></a>
    </div>
  </section>

  <!-- Por que esse plano -->
  <section class="sub-section sub-section-light">
    <div class="container">
      <div class="section-header section-header-tight">
        <h2 class="section-title">Por que escolher esse plano</h2>
      </div>
      <div class="sub-highlights">{highlights_html}
      </div>
    </div>
  </section>

  <!-- Planos disponíveis -->
  <section class="sub-section sub-section-dark">
    <div class="container">
      <div class="section-header section-header-tight">
        <h2 class="section-title">Planos disponíveis</h2>
      </div>
      <div class="sub-plans-grid">{plan_cards}
      </div>
    </div>
  </section>
{article}{faq_html}
{PLANS_SYNC_SCRIPT}
{faq_jsonld}{footer(depth)}'''


def page_app(a, depth=2):
    highlights_html = ""
    for h in a["highlights"]:
        highlights_html += f'<li><i class="ph-fill ph-check-circle"></i> {h}</li>'

    # Cruza categorias do app com os planos do config.json (validado).
    escolher = compute_escolher_em(a.get("cats") or [])
    if escolher:
        items = "".join(
            f'<li><i class="ph-fill ph-check"></i> <strong>{nome_p}</strong> <span class="sub-app-cat">categoria {cat_nome}</span></li>'
            for nome_p, cat_nome in escolher)
        escolher_html = f'''
      <div class="sub-app-escolher">
        <h3>Onde você pode escolher esse app</h3>
        <p class="sub-app-escolher-sub">Cada plano libera uma categoria PlayHub e você escolhe 1 app por mês dentro dela.</p>
        <ul class="sub-app-escolher-list">{items}</ul>
      </div>'''
    else:
        escolher_html = '''
      <div class="sub-app-escolher sub-app-escolher-empty">
        <p>Esse app é vendido como add-on avulso. Fala com a gente pelo WhatsApp pra contratar.</p>
      </div>'''

    base = "../" * depth
    extra_head = f'<link rel="stylesheet" href="{base}playhub.css?v=20260617-playhub2">'
    extra_scripts = f'  <script src="{base}playhub.js?v=20260617-playhub-b" defer></script>'

    return f'''{head(a["name"], depth, extra_head=extra_head)}
{header(depth)}

  <!-- HERO da subpágina (app) -->
  <section class="sub-hero sub-hero-app">
    <div class="container sub-hero-inner sub-hero-app-inner">
      <div class="sub-app-logo-wrap">
        <img src="../../imgs/{a["logo"]}" alt="{a["name"]}" class="sub-app-logo-big">
      </div>
      <div class="sub-app-content">
        <span class="sub-hero-tag">APLICATIVO · {a["tag"]}</span>
        <h1 class="sub-hero-title">{a["name"]}</h1>
        <p class="sub-hero-subtitle">{a["desc"]}</p>
        <a href="../../#planos" class="sub-hero-cta">Ver planos com {a["name"]} <i class="ph ph-arrow-right"></i></a>
      </div>
    </div>
  </section>

  <!-- O que tem + onde escolher -->
  <section class="sub-section sub-section-light">
    <div class="container sub-section-narrow">
      <div class="section-header section-header-tight">
        <h2 class="section-title">O que vem incluso</h2>
      </div>
      <ul class="sub-app-features">{highlights_html}
      </ul>
{escolher_html}
    </div>
  </section>

  <!-- ========== PLAYHUB · APPS POR CATEGORIA ========== -->
  <section class="playhub-section" id="playhub">
    <div class="container">
      <div class="ph-head">
        <div class="ph-head-text">
          <span class="ph-eyebrow">PlayHub</span>
          <h2 class="ph-title">Aproveite com a <span class="title-fire">MasterInfo</span></h2>
          <p class="ph-subtitle">Em qualquer plano com app de TV, você escolhe 1 app por mês dentro da sua categoria. Mais de 30 opções entre streaming, segurança, educação e mais.</p>
        </div>
        <a href="#playhub-howto" class="ph-aux-btn">Como funciona <i class="ph ph-info"></i></a>
      </div>

      <div id="playhub-grid" class="playhub-grid">
        <!-- preenchido pelo playhub.js -->
      </div>

      <div class="playhub-howto" id="playhub-howto">
        <i class="ph-fill ph-info"></i>
        <span>Cada plano tem uma categoria liberada. Os planos Ultra Home Office e Ultra Gamer dão acesso a mais de uma categoria, com 1 escolha por mês em cada.</span>
      </div>
    </div>
  </section>

{footer(depth, extra_scripts=extra_scripts)}'''


# Widget de chat de boletos (Marina). String comum (NÃO f-string) p/ não conflitar
# com as chaves de CSS/JS. Inserida no page_ajuda quando o item tem "chat": True.
# Fala só com /api/marina.php (proxy server-to-server que guarda o token).
CHAT_BOLETOS_HTML = r'''
  <!-- Chat de boletos (Marina) -->
  <section class="sub-section sub-section-dark" id="chat-boletos">
    <div class="container sub-section-narrow">
      <div class="section-header section-header-tight">
        <h2 class="section-title">Pegar minha 2ª via agora</h2>
      </div>
      <div class="mi-chat">
        <div class="mi-chat-head">
          <span class="mi-chat-avatar"><i class="ph-fill ph-headset"></i></span>
          <div>
            <strong>Marina</strong>
            <span class="mi-chat-status"><span class="mi-chat-dot"></span> Atendimento online</span>
          </div>
        </div>
        <div class="mi-chat-cpf" id="miChatCpf">
          <label for="miCpf">Pra começar, informe seu CPF</label>
          <div class="mi-chat-cpf-row">
            <input type="tel" id="miCpf" inputmode="numeric" placeholder="000.000.000-00" maxlength="14" autocomplete="off">
            <button type="button" id="miCpfBtn">Continuar <i class="ph ph-arrow-right"></i></button>
          </div>
          <p class="mi-chat-note">Usamos seu CPF só pra localizar suas faturas. <a href="https://wa.me/554734341734" target="_blank" rel="noopener">Prefere o WhatsApp?</a></p>
        </div>
        <div class="mi-chat-body" id="miChatBody" hidden></div>
        <div class="mi-chat-input" id="miChatInput" hidden>
          <input type="text" id="miMsg" placeholder="Escreva sua mensagem..." autocomplete="off">
          <button type="button" id="miSend" aria-label="Enviar"><i class="ph-fill ph-paper-plane-right"></i></button>
        </div>
      </div>
    </div>
  </section>

  <style>
    #chat-boletos .mi-chat{max-width:560px;margin:0 auto;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.10);border-radius:18px;overflow:hidden;}
    #chat-boletos .mi-chat-head{display:flex;align-items:center;gap:12px;padding:14px 18px;background:rgba(255,122,5,0.12);border-bottom:1px solid rgba(255,255,255,0.08);}
    #chat-boletos .mi-chat-avatar{width:42px;height:42px;border-radius:50%;background:linear-gradient(135deg,#ff7a05,#fcc305);display:flex;align-items:center;justify-content:center;color:#fff;font-size:1.3rem;flex-shrink:0;}
    #chat-boletos .mi-chat-head strong{display:block;color:#fff;font-size:0.95rem;}
    #chat-boletos .mi-chat-status{font-size:0.75rem;color:#9fe0b0;display:flex;align-items:center;gap:5px;}
    #chat-boletos .mi-chat-dot{width:8px;height:8px;border-radius:50%;background:#22c55e;display:inline-block;box-shadow:0 0 0 3px rgba(34,197,94,0.2);}
    #chat-boletos .mi-chat-cpf{padding:22px 18px;}
    #chat-boletos .mi-chat-cpf label{display:block;font-size:0.9rem;color:#cfcfd6;margin-bottom:10px;}
    #chat-boletos .mi-chat-cpf-row{display:flex;gap:8px;flex-wrap:wrap;}
    #chat-boletos .mi-chat-cpf-row input{flex:1;min-width:160px;padding:12px 14px;border-radius:10px;border:1px solid rgba(255,255,255,0.16);background:rgba(0,0,0,0.25);color:#fff;font-size:1rem;}
    #chat-boletos .mi-cpf-err{border-color:#e63946 !important;}
    #chat-boletos .mi-chat-cpf-row button,#chat-boletos .mi-chat-input button{border:none;cursor:pointer;}
    #chat-boletos .mi-chat-cpf-row button{padding:12px 18px;border-radius:10px;background:linear-gradient(135deg,#ff7a05,#fcc305);color:#fff;font-weight:700;display:inline-flex;align-items:center;gap:6px;}
    #chat-boletos .mi-chat-note{font-size:0.78rem;color:#8a8a93;margin-top:10px;}
    #chat-boletos .mi-chat-note a{color:#fcc305;}
    #chat-boletos .mi-chat-body{padding:16px;height:340px;overflow-y:auto;display:flex;flex-direction:column;gap:10px;}
    #chat-boletos .mi-bubble{max-width:84%;padding:10px 14px;border-radius:14px;font-size:0.9rem;line-height:1.45;word-wrap:break-word;}
    #chat-boletos .mi-bubble-bot{align-self:flex-start;background:rgba(255,255,255,0.08);color:#e8e8ef;border-bottom-left-radius:4px;}
    #chat-boletos .mi-bubble-user{align-self:flex-end;background:linear-gradient(135deg,#ff7a05,#fcc305);color:#fff;border-bottom-right-radius:4px;}
    #chat-boletos .mi-md-table{border-collapse:collapse;margin:8px 0;font-size:0.8rem;width:100%;}
    #chat-boletos .mi-md-table th,#chat-boletos .mi-md-table td{border:1px solid rgba(255,255,255,0.18);padding:5px 9px;text-align:left;}
    #chat-boletos .mi-md-table th{background:rgba(255,255,255,0.08);font-weight:700;}
    #chat-boletos .mi-typing{display:flex;gap:4px;align-items:center;}
    #chat-boletos .mi-typing span{width:7px;height:7px;border-radius:50%;background:#aaa;animation:miblink 1.2s infinite both;}
    #chat-boletos .mi-typing span:nth-child(2){animation-delay:.2s;}
    #chat-boletos .mi-typing span:nth-child(3){animation-delay:.4s;}
    @keyframes miblink{0%,80%,100%{opacity:.25}40%{opacity:1}}
    #chat-boletos .mi-boleto{align-self:stretch;background:#fff;color:#1a1a2e;border-radius:14px;padding:14px;}
    #chat-boletos .mi-boleto-top{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:8px;}
    #chat-boletos .mi-boleto-status{font-size:0.7rem;text-transform:uppercase;background:rgba(255,122,5,0.15);color:#c2410c;padding:3px 8px;border-radius:8px;font-weight:700;white-space:nowrap;}
    #chat-boletos .mi-boleto-meta{display:flex;justify-content:space-between;align-items:center;font-size:0.85rem;color:#555;margin-bottom:10px;gap:8px;}
    #chat-boletos .mi-boleto-val{font-size:1.2rem;font-weight:800;color:#1a1a2e;}
    #chat-boletos .mi-boleto-qr{display:block;width:150px;height:150px;margin:0 auto 12px;border-radius:8px;background:#fff;}
    #chat-boletos .mi-boleto-actions{display:flex;flex-direction:column;gap:8px;}
    #chat-boletos .mi-boleto-btn{display:inline-flex;align-items:center;justify-content:center;gap:7px;padding:11px 14px;border-radius:10px;border:1px solid rgba(0,0,0,0.12);background:#f4f4f6;color:#1a1a2e;font-weight:600;font-size:0.85rem;text-decoration:none;cursor:pointer;}
    #chat-boletos .mi-boleto-btn:hover{background:#fff3e8;border-color:#ffbe8a;}
    #chat-boletos .mi-chat-input{display:flex;gap:8px;padding:12px 16px;border-top:1px solid rgba(255,255,255,0.08);}
    #chat-boletos .mi-chat-input input{flex:1;padding:11px 14px;border-radius:10px;border:1px solid rgba(255,255,255,0.16);background:rgba(0,0,0,0.25);color:#fff;font-size:0.95rem;}
    #chat-boletos .mi-chat-input button{width:46px;border-radius:10px;background:linear-gradient(135deg,#ff7a05,#fcc305);color:#fff;font-size:1.1rem;flex-shrink:0;}
  </style>

  <script>
  (function(){
    var PROXY_URL = '/api/marina.php';
    var sid = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : ('s' + Date.now() + Math.floor(Math.random()*1e6));
    var cpf = '', busy = false;
    var elCpfStep = document.getElementById('miChatCpf');
    var elCpfInput = document.getElementById('miCpf');
    var elCpfBtn = document.getElementById('miCpfBtn');
    var elBody = document.getElementById('miChatBody');
    var elInputRow = document.getElementById('miChatInput');
    var elMsg = document.getElementById('miMsg');
    var elSend = document.getElementById('miSend');
    if (!elCpfStep) return;

    // Atendimento ligado/desligado no painel admin: se desabilitado, esconde a seção.
    fetch(PROXY_URL, { method: 'GET' })
      .then(function(r){ return r.json(); })
      .then(function(s){ if (s && s.enabled === false){ var sec = document.getElementById('chat-boletos'); if (sec) sec.style.display = 'none'; } })
      .catch(function(){});

    function maskCpf(v){
      v = v.replace(/\D/g,'').slice(0,11);
      if (v.length > 9) return v.replace(/(\d{3})(\d{3})(\d{3})(\d{1,2})/, '$1.$2.$3-$4');
      if (v.length > 6) return v.replace(/(\d{3})(\d{3})(\d{1,3})/, '$1.$2.$3');
      if (v.length > 3) return v.replace(/(\d{3})(\d{1,3})/, '$1.$2');
      return v;
    }
    elCpfInput.addEventListener('input', function(){ elCpfInput.classList.remove('mi-cpf-err'); elCpfInput.value = maskCpf(elCpfInput.value); });

    function esc(s){ var d = document.createElement('div'); d.textContent = (s==null?'':String(s)); return d.innerHTML; }
    // Markdown leve (a Marina responde com **negrito** e tabelas | | |). Escapa antes (XSS-safe).
    function mdRender(raw){
      var lines = String(raw==null?'':raw).split('\n'), html='', i=0;
      function inl(s){ return esc(s).replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>'); }
      function cells(l){ return l.trim().replace(/^\||\|$/g,'').split('|').map(function(c){ return c.trim(); }); }
      while (i < lines.length){
        if (/^\s*\|.*\|\s*$/.test(lines[i]) && i+1 < lines.length && /^\s*\|[\s:|-]+\|\s*$/.test(lines[i+1])){
          var head = cells(lines[i]); i += 2; var rows = '';
          while (i < lines.length && /^\s*\|.*\|\s*$/.test(lines[i])){ var r = cells(lines[i]); rows += '<tr>'+r.map(function(c){ return '<td>'+inl(c)+'</td>'; }).join('')+'</tr>'; i++; }
          html += '<table class="mi-md-table"><thead><tr>'+head.map(function(h){ return '<th>'+inl(h)+'</th>'; }).join('')+'</tr></thead><tbody>'+rows+'</tbody></table>';
        } else { html += inl(lines[i]) + '<br>'; i++; }
      }
      return html.replace(/(<br>\s*)+$/,'');
    }
    function scrollDown(){ elBody.scrollTop = elBody.scrollHeight; }
    function addBubble(text, who){
      var b = document.createElement('div');
      b.className = 'mi-bubble mi-bubble-' + who;
      b.innerHTML = mdRender(text);
      elBody.appendChild(b); scrollDown(); return b;
    }
    function addTyping(){
      var t = document.createElement('div');
      t.className = 'mi-bubble mi-bubble-bot mi-typing';
      t.innerHTML = '<span></span><span></span><span></span>';
      elBody.appendChild(t); scrollDown(); return t;
    }
    function fmtDate(d){ var m = /^(\d{4})-(\d{2})-(\d{2})/.exec(d||''); return m ? (m[3]+'/'+m[2]+'/'+m[1]) : (d||''); }
    function fmtMoney(v){
      if (v==null || v==='') return '';
      var n = Number(String(v).replace(',','.'));
      return isNaN(n) ? esc(v) : ('R$ ' + n.toFixed(2).replace('.',','));
    }
    function copyBtn(label, text){
      return text ? '<button type="button" class="mi-boleto-btn" data-copy="'+esc(text)+'">'+label+'</button>' : '';
    }
    function renderBoleto(b){
      if (!b) return;
      var card = document.createElement('div');
      card.className = 'mi-boleto';
      var linha = b.linha_digitavel || b.codigo_barras || '';
      var html = '<div class="mi-boleto-top"><strong>'+esc(b.descricao||'Fatura')+'</strong>'+(b.status?'<span class="mi-boleto-status">'+esc(b.status)+'</span>':'')+'</div>';
      html += '<div class="mi-boleto-meta">';
      if (b.vencimento) html += '<span><i class="ph ph-calendar-blank"></i> Vence '+esc(fmtDate(b.vencimento))+'</span>';
      if (b.valor!=null && b.valor!=='') html += '<span class="mi-boleto-val">'+fmtMoney(b.valor)+'</span>';
      html += '</div>';
      if (b.pix_qrcode_png_base64) html += '<img class="mi-boleto-qr" alt="QR Code PIX" src="data:image/png;base64,'+esc(b.pix_qrcode_png_base64)+'">';
      html += '<div class="mi-boleto-actions">';
      html += copyBtn('<i class="ph ph-barcode"></i> Copiar linha digitável', linha);
      html += copyBtn('<i class="ph ph-qr-code"></i> Copiar código PIX', b.pix_copia_cola);
      if (b.url_pdf) html += '<a class="mi-boleto-btn" href="'+esc(b.url_pdf)+'" target="_blank" rel="noopener"><i class="ph ph-file-pdf"></i> Baixar PDF</a>';
      html += '</div>';
      card.innerHTML = html;
      elBody.appendChild(card); scrollDown();
    }
    elBody.addEventListener('click', function(e){
      var btn = e.target.closest('[data-copy]');
      if (!btn) return;
      navigator.clipboard.writeText(btn.getAttribute('data-copy')).then(function(){
        var old = btn.innerHTML; btn.innerHTML = '<i class="ph ph-check"></i> Copiado!';
        setTimeout(function(){ btn.innerHTML = old; }, 1800);
      }).catch(function(){});
    });

    function send(text){
      if (busy) return;
      busy = true; elSend.disabled = true;
      addBubble(text, 'user');
      var typing = addTyping();
      fetch(PROXY_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cpf: cpf, message: text, session_id: sid })
      })
      .then(function(r){ return r.json().catch(function(){ return { reply: 'Recebi uma resposta inesperada. Tenta de novo ou chama no WhatsApp.' }; }); })
      .then(function(d){
        typing.remove();
        if (d && d.session_id) sid = d.session_id;
        addBubble((d && d.reply) ? d.reply : 'Não recebi resposta. Tenta de novo ou chama no WhatsApp.', 'bot');
        if (d && Array.isArray(d.boletos)) d.boletos.forEach(renderBoleto);
      })
      .catch(function(){
        typing.remove();
        addBubble('Falha de conexão. Tenta de novo ou fala com a gente no WhatsApp.', 'bot');
      })
      .finally(function(){ busy = false; elSend.disabled = false; elMsg.focus(); });
    }

    function start(){
      var digits = elCpfInput.value.replace(/\D/g,'');
      if (digits.length !== 11){ elCpfInput.classList.add('mi-cpf-err'); elCpfInput.focus(); return; }
      cpf = digits;
      elCpfStep.hidden = true; elBody.hidden = false; elInputRow.hidden = false;
      addBubble('Oi! Sou a Marina 👋 Deixa eu buscar suas faturas pelo seu CPF...', 'bot');
      send('quero meu boleto');
    }
    elCpfBtn.addEventListener('click', start);
    elCpfInput.addEventListener('keydown', function(e){ if (e.key === 'Enter') start(); });
    elSend.addEventListener('click', function(){ var t = elMsg.value.trim(); if (t){ elMsg.value=''; send(t); } });
    elMsg.addEventListener('keydown', function(e){ if (e.key === 'Enter'){ var t = elMsg.value.trim(); if (t){ elMsg.value=''; send(t); } } });
  })();
  </script>'''


def page_ajuda(a, depth=2):
    steps_html = ""
    for emoji, title, desc in a["steps"]:
        steps_html += f'''
        <div class="sub-highlight">
          <div class="sub-highlight-emoji">{emoji}</div>
          <h3>{title}</h3>
          <p>{desc}</p>
        </div>'''

    chat_html = CHAT_BOLETOS_HTML if a.get("chat") else ""

    return f'''{head(a["title"], depth)}
{header(depth)}

  <!-- HERO da subpágina (ajuda) -->
  <section class="sub-hero" style="background: {a["gradient"]};">
    <div class="container sub-hero-inner">
      <span class="sub-hero-tag">{a["tag"]}</span>
      <h1 class="sub-hero-title">{a["title"]}</h1>
      <p class="sub-hero-subtitle">{a["subtitle"]}</p>
      <a href="{a["cta_href"]}" target="_blank" class="sub-hero-cta" rel="noopener">{a["cta_label"]} <i class="ph ph-arrow-right"></i></a>
    </div>
  </section>

  <!-- Passo a passo -->
  <section class="sub-section sub-section-light">
    <div class="container">
      <div class="section-header section-header-tight">
        <h2 class="section-title">Passo a passo</h2>
      </div>
      <div class="sub-highlights">{steps_html}
      </div>
    </div>
  </section>
{chat_html}
{footer(depth, boleto=not a.get("chat"))}'''


# ─── GERAR ARQUIVOS ───────────────────────────────────────────────────

# TODAS as paginas (menos a home) que carregam header+rodape padrao, com sua
# profundidade (base = "../"*depth). As 16 geradas saem das listas de dados; as 5
# estaticas (nao geradas por template) entram explicitas. A home NAO entra: ela
# monta header+rodape em runtime via site-loader.js (mesma fonte = o config).
def page_playhub(depth=1):
    """Página dedicada do PlayHub (/playhub/): hero + como funciona + as 4 categorias
    (cards renderizados pelo playhub.js; clicar abre o modal do nível). depth=1."""
    base = "../" * depth
    extra_head = f'<link rel="stylesheet" href="{base}playhub.css?v=20260617-playhub2">'
    extra_scripts = f'  <script src="{base}playhub.js?v=20260617-playhub-b" defer></script>'

    passos = [
        ("📺", "Escolha seu plano", "Todo plano com app de TV já vem com uma categoria PlayHub liberada, sem custo extra."),
        ("🎯", "Escolha 1 app por mês", "Dentro da sua categoria você troca de app quando quiser: 1 por mês, na hora que preferir."),
        ("✨", "Aproveite tudo", "Streaming, música, leitura, educação e segurança, direto no seu plano de internet."),
    ]
    passos_html = ""
    for emoji, titulo, desc in passos:
        passos_html += f'''
        <div class="sub-highlight">
          <div class="sub-highlight-emoji">{emoji}</div>
          <h3>{titulo}</h3>
          <p>{desc}</p>
        </div>'''

    return f'''{head("PlayHub, Catálogo de apps incluso no seu plano", depth, extra_head=extra_head)}
{header(depth)}

  <!-- HERO PlayHub -->
  <section class="sub-hero" style="background: linear-gradient(135deg, #1a1a1a 0%, #3a1e05 100%);">
    <div class="container sub-hero-inner">
      <span class="sub-hero-tag">PLAYHUB · CATÁLOGO DE APPS</span>
      <h1 class="sub-hero-title">Os melhores apps, inclusos no seu plano</h1>
      <p class="sub-hero-subtitle">Em qualquer plano com app de TV você escolhe 1 app por mês dentro da sua categoria. Mais de 30 opções entre streaming, música, leitura, educação e segurança.</p>
      <a href="{base}#planos" class="sub-hero-cta">Ver planos <i class="ph ph-arrow-right"></i></a>
    </div>
  </section>

  <!-- Como funciona -->
  <section class="sub-section sub-section-light">
    <div class="container">
      <div class="section-header section-header-tight">
        <h2 class="section-title">Como funciona</h2>
      </div>
      <div class="sub-highlights">{passos_html}
      </div>
    </div>
  </section>

  <!-- ========== PLAYHUB · CATEGORIAS ========== -->
  <section class="playhub-section" id="playhub">
    <div class="container">
      <div class="ph-head">
        <div class="ph-head-text">
          <span class="ph-eyebrow">Catálogos</span>
          <h2 class="ph-title">Escolha o seu <span class="title-fire">catálogo</span></h2>
          <p class="ph-subtitle">Cada plano libera uma categoria. Clique pra ver tudo que tem em cada uma, Standard, Advanced, TOP e Premium.</p>
        </div>
        <a href="#playhub-howto" class="ph-aux-btn">Como funciona <i class="ph ph-info"></i></a>
      </div>

      <div id="playhub-grid" class="playhub-grid">
        <!-- preenchido pelo playhub.js -->
      </div>

      <div class="playhub-howto" id="playhub-howto">
        <i class="ph-fill ph-info"></i>
        <span>Cada plano tem uma categoria liberada. Os planos Ultra Home Office e Ultra Gamer dão acesso a mais de uma categoria, com 1 escolha por mês em cada.</span>
      </div>
    </div>
  </section>

{footer(depth, extra_scripts=extra_scripts)}'''


# ─── PÁGINAS-PILAR + BLOG (camada de conteúdo SEO/GEO) ────────────────────
# Geradas por funções (usam head()/header()/footer() → nascem compatíveis com os
# syncs cirúrgicos) e registradas em MENU_PAGES + SEO_META. Flag: --content / --blog.
BLOGCSS_VER = "20260618-b"
BLOG_BY_REL = {f'blog/{_p["slug"]}/index.html': _p for _p in BLOG}
# og:image por página (preview social correto): imagem do próprio pilar/post (rel; SITE_URL no sync_og).
OG_IMG_BY_REL = {}
for _op in PILARES:
    if _op.get("hero_img"):
        OG_IMG_BY_REL[f'{_op["slug"]}/index.html'] = _op["hero_img"]
for _op in BLOG:
    if _op.get("image"):
        OG_IMG_BY_REL[f'blog/{_op["slug"]}/index.html'] = _op["image"]
_MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def format_date_br(iso):
    try:
        y, m, d = iso.split("-")
        return f"{int(d)} {_MESES[int(m) - 1]} {y}"
    except Exception:
        return iso


def reading_min(html):
    """Estima minutos de leitura a partir do HTML do corpo (~200 palavras/min)."""
    text = re.sub(r"<[^>]+>", " ", html or "")
    return max(1, round(len(text.split()) / 200))


def render_plan_cards(plan_ids):
    """Monta os <a class="sub-plan-card"> (href root-absolute p/ checkout). Texto vem do
    config.json (CFG_PLANS_BY_ID), fallback PLANS_MAP; apps curados no PLANS_MAP. Casa com
    o PLANS_SYNC_SCRIPT (que sincroniza pelo href checkout.html?plano=)."""
    cards = ""
    for plan_id in plan_ids:
        plan = PLANS_MAP.get(plan_id, {})
        cfg = CFG_PLANS_BY_ID.get(plan_id, {})
        nome = cfg.get("nome") or plan.get("nome", plan_id)
        speed = cfg.get("velocidade") or plan.get("speed", "")
        unit = cfg.get("unidade") or plan.get("unit", "Mega")
        preco = fmt_brl(cfg.get("precoPontual")) or plan.get("preco", "")
        preco_cheio = fmt_brl(cfg.get("precoCheio")) or plan.get("preco_cheio", "")
        features = cfg.get("features") or plan.get("features", [])
        apps_html = ""
        for app in plan.get("apps", []):
            apps_html += (f'\n              <div class="sub-plan-app">'
                          f'<img src="/imgs/{app["logo"]}" alt="{app["nome"]}" class="sub-plan-app-logo">'
                          f'<span class="sub-plan-app-name">{app["nome"]}</span></div>')
        features_html = "".join(f'<li><i class="ph-fill ph-check-circle"></i> {f}</li>' for f in features)
        cards += (
            f'\n        <a href="/checkout.html?plano={plan_id}" class="sub-plan-card">'
            f'\n          <div class="sub-plan-head">'
            f'\n            <span class="sub-plan-speed">{speed}<small> {unit}</small></span>'
            f'\n            <span class="sub-plan-name">{nome}</span>'
            f'\n          </div>'
            f'\n          <div class="sub-plan-price-wrap">'
            f'\n            <span class="sub-plan-price-original">de <s>R$ {preco_cheio}</s> por</span>'
            f'\n            <span class="sub-plan-price">R$ {preco} <em>/mês</em></span>'
            f'\n            <span class="sub-plan-discount"><i class="ph-fill ph-tag"></i> R$ 10+ OFF pagando em dia</span>'
            f'\n          </div>'
            f'\n          <div class="sub-plan-apps"><span class="sub-plan-apps-label">INCLUSO</span>'
            f'<div class="sub-plan-apps-list">{apps_html}\n            </div></div>'
            f'\n          <ul class="sub-plan-features">{features_html}</ul>'
            f'\n          <span class="sub-plan-cta">Ver detalhes <i class="ph ph-arrow-right"></i></span>'
            f'\n        </a>')
    return cards


def build_plans_inline(plan_ids):
    return f'<div class="sub-plans-grid article-plans">{render_plan_cards(plan_ids)}\n      </div>'


def build_plans_section(plan_ids):
    return (f'\n  <section class="sub-section sub-section-dark" id="planos">'
            f'\n    <div class="container">'
            f'\n      <div class="section-header section-header-tight"><h2 class="section-title">Planos disponíveis</h2></div>'
            f'\n      <div class="sub-plans-grid">{render_plan_cards(plan_ids)}\n      </div>'
            f'\n    </div>\n  </section>')


def render_faq(faqs):
    """(html_section, jsonld_script) para [(pergunta, resposta)...]. Usa <details>/<summary>
    (funciona sem JS, pois as subpáginas não carregam o site-loader) + JSON-LD FAQPage."""
    if not faqs:
        return "", ""
    items = ""
    for q, a in faqs:
        items += (f'\n        <details class="faq-q"><summary>{q}</summary>'
                  f'<div class="faq-a"><p>{a}</p></div></details>')
    html = (f'\n  <section class="sub-section sub-section-light">'
            f'\n    <div class="container article-narrow">'
            f'\n      <div class="section-header section-header-tight"><h2 class="section-title">Perguntas frequentes</h2></div>'
            f'\n      <div class="faq-block">{items}\n      </div>'
            f'\n    </div>\n  </section>')
    nodes = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": nodes}
    script = '\n  <script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n  </script>'
    return html, script


def build_schema_data(rel, name, desc, url):
    """JSON-LD por tipo de página: BlogPosting (posts), Blog (índice), WebPage (resto)."""
    if rel in BLOG_BY_REL:
        post = BLOG_BY_REL[rel]
        a = AUTHORS.get(post.get("author"), AUTHORS["equipe"])
        author_node = {"@type": a["type"], "name": a["name"]}
        au = a.get("url", "")
        if au:
            author_node["url"] = (SITE_URL + au) if au.startswith("/") else au
            if au == "/sobre/philipe/":
                author_node["@id"] = SITE_URL + au + "#person"
        img = post.get("image", "")
        img_abs = (SITE_URL + img) if img.startswith("/") else img
        return {"@context": "https://schema.org", "@graph": [
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE_URL + "/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE_URL + "/blog/"},
                {"@type": "ListItem", "position": 3, "name": name, "item": url},
            ]},
            {"@type": "BlogPosting", "headline": post.get("h1", name), "description": desc,
             "url": url, "datePublished": post.get("date", DATE_DEFAULT),
             "dateModified": post.get("date", DATE_DEFAULT), "image": img_abs, "inLanguage": "pt-BR",
             "author": author_node,
             "publisher": {"@type": "Organization", "name": PUBLISHER["name"],
                           "logo": {"@type": "ImageObject", "url": SITE_URL + PUBLISHER["logo"]}},
             "mainEntityOfPage": {"@type": "WebPage", "@id": url},
             "isPartOf": {"@type": "Blog", "name": "Blog MasterInfo", "url": SITE_URL + "/blog/"}},
        ]}
    if rel == "blog/index.html":
        return {"@context": "https://schema.org", "@graph": [
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE_URL + "/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": url},
            ]},
            {"@type": "Blog", "name": "Blog MasterInfo", "description": desc, "url": url, "inLanguage": "pt-BR",
             "publisher": {"@type": "Organization", "name": PUBLISHER["name"],
                           "logo": {"@type": "ImageObject", "url": SITE_URL + PUBLISHER["logo"]}},
             "blogPost": [{"@type": "BlogPosting", "headline": _p.get("h1"),
                           "url": SITE_URL + "/blog/" + _p["slug"] + "/",
                           "datePublished": _p.get("date", DATE_DEFAULT)} for _p in BLOG]},
        ]}
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": url},
        ]},
        {"@type": "WebPage", "name": name, "description": desc, "url": url, "inLanguage": "pt-BR",
         "isPartOf": {"@type": "WebSite", "name": "MasterInfo Internet", "url": SITE_URL + "/"},
         "about": {"@type": "Organization", "name": "MasterInfo Internet", "url": SITE_URL + "/"}},
    ]}


# Páginas de bairro → schema LocalBusiness/ISP próprio (areaServed do bairro). Espelha os
# dados canônicos do provedor da home; @id por página p/ não colidir com o #provedor da home.
BAIRRO_AREA = {
    "internet-comasa-joinville": "Comasa",
    "internet-boa-vista-joinville": "Boa Vista",
    "internet-iririu-joinville": "Iririú",
    "internet-espinheiros-joinville": "Espinheiros",
    "internet-aventureiro-joinville": "Aventureiro",
    "internet-itinga-joinville": "Itinga",
    "internet-jardim-paraiso-joinville": "Jardim Paraíso",
    "internet-jardim-sofia-joinville": "Jardim Sofia",
    "internet-cubatao-joinville": "Cubatão",
    "internet-nova-brasilia-joinville": "Nova Brasília",
    "internet-rio-bonito-joinville": "Rio Bonito",
    "internet-estrada-timbe-joinville": "Estrada Timbé",
    "internet-paranaguamirim-joinville": "Paranaguamirim",
}

def local_business_jsonld(bairro_nome, page_url):
    data = {
        "@context": "https://schema.org",
        "@type": ["InternetServiceProvider", "LocalBusiness"],
        "@id": page_url + "#provedor",
        "name": "MasterInfo Internet",
        "image": SITE_URL + "/og-image.jpg",
        "logo": {"@type": "ImageObject", "url": SITE_URL + "/logo-masterinfo.png"},
        "description": f"Provedor de internet fibra óptica que atende o bairro {bairro_nome}, em Joinville, SC.",
        "url": page_url,
        "telephone": "+554734341734",
        "email": "masterinfo@masterinfointernet.com",
        "address": {"@type": "PostalAddress", "streetAddress": "Rua Prefeito Baltazar Buschle, 628",
                    "addressLocality": "Joinville", "addressRegion": "SC", "postalCode": "89228-000", "addressCountry": "BR"},
        "geo": {"@type": "GeoCoordinates", "latitude": -26.2798, "longitude": -48.8016},
        "areaServed": {"@type": "Place", "name": f"{bairro_nome}, Joinville, SC"},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "08:00", "closes": "12:00"}],
        "priceRange": "R$ 99,99 - R$ 189,90",
        "hasMap": "https://www.google.com/maps?cid=10673247961179135046",
        "sameAs": ["https://www.instagram.com/masterinfo.internet",
                   "https://www.facebook.com/masterinfointernet",
                   "https://www.google.com/maps?cid=10673247961179135046"],
    }
    return '\n  <script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n  </script>'


# Interlink spoke-to-spoke entre as paginas de bairro (hub-and-spoke). Cada bairro linka
# pros outros 12, fechando o internal linking (antes os bairros so linkavam pro hub).
def bairros_vizinhos_section(current_slug):
    outros = [(s, n) for s, n in BAIRRO_AREA.items() if s != current_slug]
    chips = "".join(f'<a href="/{s}/" class="bv-link">Internet {n}</a>' for s, n in outros)
    css = ('<style>.bairros-vizinhos{padding:52px 0;background:rgba(255,122,5,0.04)}'
           '.bairros-vizinhos h2{font-size:clamp(1.3rem,3vw,1.75rem);font-weight:800;color:var(--text-primary);margin-bottom:8px}'
           '.bairros-vizinhos p{color:var(--text-muted);margin-bottom:22px}'
           '.bv-grid{display:flex;flex-wrap:wrap;gap:10px}'
           '.bv-link{display:inline-flex;align-items:center;padding:8px 16px;font-size:0.9rem;font-weight:600;color:var(--orange-dark);'
           'background:rgba(255,122,5,0.07);border:1px solid rgba(255,122,5,0.22);border-radius:999px;'
           'transition:transform .16s cubic-bezier(.23,1,.32,1),background-color .16s ease,border-color .16s ease}'
           '.bv-link:active{transform:scale(.96)}'
           '@media(hover:hover) and (pointer:fine){.bv-link:hover{background:rgba(255,122,5,.14);border-color:rgba(255,122,5,.5)}}</style>')
    return ('\n  ' + css +
            '\n  <section class="bairros-vizinhos">\n    <div class="container">'
            '\n      <h2>Internet fibra óptica em outros bairros de Joinville</h2>'
            '\n      <p>A MasterInfo também leva fibra óptica de verdade para:</p>'
            f'\n      <div class="bv-grid">{chips}</div>'
            '\n    </div>\n  </section>')


def page_pilar(p, depth=1):
    extra = f'<link rel="stylesheet" href="/blog.css?v={BLOGCSS_VER}">'
    short_title = p["title"].split(" | ")[0]
    if p.get("cta_whatsapp"):
        cta_href = "https://wa.me/" + p["cta_whatsapp"]
    else:
        cta_href = "/checkout.html?plano=" + p.get("cta_plano", "")
    hero_style = (f"background-image: linear-gradient(rgba(0,0,0,0.58), rgba(0,0,0,0.42)), "
                  f"url('{p['hero_img']}'); background-size:cover; background-position:center;")
    hero = (f'\n  <section class="sub-hero" style="{hero_style}">'
            f'\n    <div class="container sub-hero-inner">'
            f'\n      <span class="sub-hero-tag">{p["tag"]}</span>'
            f'\n      <h1 class="sub-hero-title">{p["h1"]}</h1>'
            f'\n      <p class="sub-hero-subtitle">{p["lead"]}</p>'
            f'\n      <a href="{cta_href}" class="sub-hero-cta">{p["cta"]} <i class="ph ph-arrow-right"></i></a>'
            f'\n    </div>\n  </section>')
    body = p["body"]
    plans_after = ""
    if p.get("plans"):
        if "<!--PLANS_GRID-->" in body:
            body = body.replace("<!--PLANS_GRID-->", build_plans_inline(p["plans"]))
        else:
            plans_after = build_plans_section(p["plans"])
    else:
        body = body.replace("<!--PLANS_GRID-->", "")
    article = f'\n  <div class="article-band">\n    <div class="article">{body}\n    </div>\n  </div>'
    faq_html, faq_jsonld = render_faq(p.get("faq", []))
    if p.get("cta_whatsapp"):
        band = ("Vamos montar a internet ideal pra sua empresa?",
                "Fale com nosso time comercial e receba uma proposta sob medida para o seu endereço em Joinville.",
                "Pedir proposta no WhatsApp", cta_href)
    else:
        band = ("Pronto pra ter fibra de verdade?",
                "Consulte a cobertura no seu endereço e contrate em minutos, com suporte de gente da região.",
                p["cta"], cta_href)
    cta_band = (f'\n  <section class="cta-band">\n    <div class="container">'
                f'\n      <h2>{band[0]}</h2>\n      <p>{band[1]}</p>'
                f'\n      <a href="{band[3]}" class="cta-band-btn">{band[2]} <i class="ph ph-arrow-right"></i></a>'
                f'\n    </div>\n  </section>')
    plans_script = ("\n" + PLANS_SYNC_SCRIPT) if p.get("plans") else ""
    lb = local_business_jsonld(BAIRRO_AREA[p["slug"]], SITE_URL + "/" + p["slug"] + "/") if p["slug"] in BAIRRO_AREA else ""
    vizinhos = bairros_vizinhos_section(p["slug"]) if p["slug"] in BAIRRO_AREA else ""
    return (head(short_title, depth, extra) + header(depth) + hero + article
            + plans_after + faq_html + vizinhos + cta_band + faq_jsonld + lb + plans_script + footer(depth))


def page_blog_index(depth=1):
    extra = f'<link rel="stylesheet" href="/blog.css?v={BLOGCSS_VER}">'
    cards = ""
    for p in BLOG:
        a = AUTHORS.get(p.get("author"), AUTHORS["equipe"])
        tag0 = p["tags"][0] if p.get("tags") else "Blog"
        cards += (f'\n        <a href="/blog/{p["slug"]}/" class="blog-card">'
                  f'\n          <div class="blog-card-img" style="background-image:url(\'{p["image"]}\');"></div>'
                  f'\n          <div class="blog-card-body">'
                  f'\n            <span class="blog-card-tag">{tag0}</span>'
                  f'\n            <h2 class="blog-card-title">{p["h1"]}</h2>'
                  f'\n            <p class="blog-card-excerpt">{p["lead"]}</p>'
                  f'\n            <span class="blog-card-meta">{a["name"]} · {format_date_br(p.get("date", DATE_DEFAULT))}</span>'
                  f'\n          </div>\n        </a>')
    hero = ('\n  <section class="blog-hero" style="background-image: linear-gradient(rgba(16,17,28.82), rgba(46,30,14.66)), url(\'/imgs/blog/blog-banner.jpg\'); background-size:cover; background-position:center;">\n    <div class="container">'
            '\n      <span class="blog-hero-eyebrow">BLOG MASTERINFO</span>'
            '\n      <h1>Dicas de internet pra aproveitar melhor sua conexão</h1>'
            '\n      <p>Guias diretos sobre fibra, Wi-Fi, velocidade e cobertura, feitos pela equipe da MasterInfo em Joinville.</p>'
            '\n    </div>\n  </section>')
    grid = (f'\n  <section class="article-band">\n    <div class="container">'
            f'\n      <div class="blog-grid">{cards}\n      </div>\n    </div>\n  </section>')
    return head("Blog", depth, extra) + header(depth) + hero + grid + footer(depth)


def build_related(post):
    others = [q for q in BLOG if q["slug"] != post["slug"]][:3]
    items = "".join(f'\n        <li><a href="/blog/{q["slug"]}/">{q["h1"]}</a></li>' for q in others)
    return (f'\n  <section class="article-band">\n    <div class="article">'
            f'\n      <h2 class="related-title">Leia também</h2>'
            f'\n      <ul class="related-list">{items}\n      </ul>'
            f'\n      <div class="post-cta">'
            f'\n        <div class="post-cta-text"><strong>Quer fibra de verdade em Joinville?</strong><p>Veja os planos e a cobertura no seu endereço.</p></div>'
            f'\n        <a href="/internet-joinville/" class="cta-band-btn">Ver internet em Joinville <i class="ph ph-arrow-right"></i></a>'
            f'\n      </div>\n    </div>\n  </section>')


def page_blog_post(post, depth=2):
    extra = f'<link rel="stylesheet" href="/blog.css?v={BLOGCSS_VER}">'
    a = AUTHORS.get(post.get("author"), AUTHORS["equipe"])
    short_title = post["title"].split(" | ")[0]
    img = post.get("image", "")
    if img and not img.endswith(".svg"):
        hero_style = (f"background-image: linear-gradient(rgba(12,12,24.62), rgba(12,12,24.62)), "
                      f"url('{img}'); background-size:cover; background-position:center;")
    else:
        hero_style = "background:linear-gradient(135deg,#0a1f44 0%,#14366b 55%,#1f5fa8 100%);"
    tag0 = post["tags"][0] if post.get("tags") else "Artigo"
    hero = (f'\n  <section class="blog-post-hero" style="{hero_style}">\n    <div class="container">'
            f'\n      <nav class="blog-breadcrumb"><a href="/">Início</a> <span>/</span> <a href="/blog/">Blog</a> <span>/</span> <span>{tag0}</span></nav>'
            f'\n      <span class="blog-post-tag">{tag0}</span>'
            f'\n      <h1>{post["h1"]}</h1>'
            f'\n      <p class="blog-post-lead">{post["lead"]}</p>'
            f'\n    </div>\n  </section>')
    rt = reading_min(post.get("body", ""))
    a_url = (a.get("url") or "/#nossa-historia")
    byline = (f'\n      <div class="byline">'
              f'<img src="{a["img"]}" alt="{a["name"]}" class="byline-avatar" loading="lazy">'
              f'<div class="byline-info"><span class="byline-name"><a href="{a_url}">{a["name"]}</a></span>'
              f'<span class="byline-role">{a["role"]} · {format_date_br(post.get("date", DATE_DEFAULT))} · {rt} min de leitura</span></div></div>')
    article = (f'\n  <main class="blog-main">\n    <div class="article-band">'
               f'\n      <article class="article">{byline}{post["body"]}\n      </article>'
               f'\n    </div>')
    faq_html, faq_jsonld = render_faq(post.get("faq", []))
    related = build_related(post)
    return (head(short_title, depth, extra) + header(depth) + hero + article
            + faq_html + related + "\n  </main>" + faq_jsonld + footer(depth))


def page_autor(depth=1):
    """Página de autor (E-E-A-T): bio + lista de artigos + schema ProfilePage/Person."""
    extra = f'<link rel="stylesheet" href="/blog.css?v={BLOGCSS_VER}">'
    a = AUTHORS["philipe"]
    posts = "".join(f'\n        <li><a href="/blog/{p["slug"]}/">{p["h1"]}</a></li>' for p in BLOG)
    hero = ('\n  <section class="blog-post-hero" style="background:linear-gradient(135deg,#16111c 0%,#2e1e0e 70%,#7a3205 100%);">'
            '\n    <div class="container">'
            '\n      <nav class="blog-breadcrumb"><a href="/">Início</a> <span>/</span> <span>Autor</span></nav>'
            '\n      <span class="blog-post-tag">Autor</span>'
            f'\n      <h1>{a["name"]}</h1>'
            f'\n      <p class="blog-post-lead">{a["role"]}</p>'
            '\n    </div>\n  </section>')
    body = ('\n  <main class="blog-main">\n    <div class="article-band">\n      <article class="article">'
            f'\n      <div class="byline"><img src="{a["img"]}" alt="{a["name"]}" class="byline-avatar"><div class="byline-info"><span class="byline-name">{a["name"]}</span><span class="byline-role">{a["role"]}</span></div></div>'
            '\n      <p>Philipe Alves Medeiros começou na informática aos 16 anos, na época da gravação de CDs. Passou pela manutenção das escolas de informática RTI, formou-se em <strong>Sistemas de Informação</strong> e atuou por anos como <strong>arquiteto de redes</strong> em diversas empresas, experiência que hoje está por trás da operação de fibra da MasterInfo.</p>'
            '\n      <p>É essa bagagem, de quem projeta e mantém rede de verdade, que sustenta a MasterInfo Internet: <strong>fibra óptica até a casa do cliente (FTTH)</strong> com engenharia e suporte feitos por gente da própria região.</p>'
            '\n      <p>Joinvilense, é casado com <strong>Tatiane Lemos</strong> cofundadora da MasterInfo, e pai de três filhos. Escreve aqui sobre fibra, Wi-Fi, velocidade e cobertura com a visão de quem constrói e opera a rede todos os dias.</p>'
            f'\n      <h2>Artigos por {a["name"]}</h2>'
            f'\n      <ul class="related-list">{posts}\n      </ul>'
            '\n      </article>\n    </div>\n  </main>')
    person = {"@context": "https://schema.org", "@type": "ProfilePage",
              "@id": SITE_URL + "/sobre/philipe/",
              "mainEntity": {"@type": "Person", "@id": SITE_URL + "/sobre/philipe/#person",
                             "name": a["name"], "jobTitle": a["role"],
                             "description": "Fundador da MasterInfo Internet. Formado em Sistemas de Informação e arquiteto de redes, atua com fibra óptica (FTTH) em Joinville há mais de 6 anos.",
                             "knowsAbout": ["Redes de computadores", "Fibra óptica", "FTTH", "Wi-Fi", "Provedores de internet"],
                             "worksFor": {"@type": "Organization", "@id": SITE_URL + "/#org", "name": "MasterInfo Internet", "url": SITE_URL + "/"},
                             "url": SITE_URL + "/sobre/philipe/", "image": SITE_URL + a["img"]}}
    schema = '\n  <script type="application/ld+json">\n' + json.dumps(person, ensure_ascii=False, indent=2) + '\n  </script>'
    return head(a["name"], depth, extra) + header(depth) + hero + body + schema + footer(depth)


def gerar_pilares():
    print("Páginas-pilar (landing comercial)…")
    for p in PILARES:
        write_file(os.path.join(BASE_DIR, p["slug"], "index.html"), page_pilar(p, depth=1))


def gerar_blog():
    print("\nBlog (índice + posts)…")
    write_file(os.path.join(BASE_DIR, "blog", "index.html"), page_blog_index(depth=1))
    for p in BLOG:
        write_file(os.path.join(BASE_DIR, "blog", p["slug"], "index.html"), page_blog_post(p, depth=2))
    write_file(os.path.join(BASE_DIR, "sobre", "philipe", "index.html"), page_autor(depth=2))


MENU_PAGES = (
    [(f'{p["slug"]}/index.html', 1) for p in INTERNET]
    + [(f'{s}/index.html', 1) for s in
       ("contato", "tv-streaming", "termos", "privacidade", "lgpd", "playhub")]
    + [(f'aplicativos/{a["slug"]}/index.html', 2) for a in APLICATIVOS]
    + [(f'ajuda/{a["slug"]}/index.html', 2) for a in AJUDA]
    + [(f'{p["slug"]}/index.html', 1) for p in PILARES]              # páginas-pilar
    + [('blog/index.html', 1)]                                       # índice do blog
    + [(f'blog/{p["slug"]}/index.html', 2) for p in BLOG]            # posts
    + [('sobre/philipe/index.html', 2)]                              # página de autor (sobre/philipe/ = profundidade 2)
)

# Bloco <header>...</header> inteiro (nao aninha, entao non-greedy basta).
_HEADER_RE = re.compile(r'<header class="header" id="header">.*?</header>', re.DOTALL)

# Bloco das 3 colunas .footer-col, ate (sem incluir) o .footer-payment. Greedy +
# lookahead: da 1a <div class="footer-col"> ate a ultima </div> antes do payment.
_FOOTER_COLS_RE = re.compile(
    r'[ \t]*<div class="footer-col">.*</div>\s*(?=</div>\s*<div class="footer-payment">)',
    re.DOTALL,
)

# <style> que carrega a escala do site nas subpaginas (a home usa site-loader.js).
_SITE_SCALE_RE = re.compile(r'<style>:root\{--site-scale:[^}]*\}</style>')

# URL canonica do site (sem barra final), base do <link rel="canonical"> self-referente.
SITE_URL = "https://masterinfointernet.com"
_CANONICAL_RE = re.compile(r'[ \t]*<link rel="canonical"[^>]*>')


# Phosphor: troca o <script> do unpkg (CDN externo lento + carrega 6 pesos + JS) por CSS
# LOCAL com só regular+fill+bold (os 3 usados). Grande ganho de LCP/INP. Cobre subpáginas
# (MENU_PAGES) + homes + checkout + copa.
_PHOSPHOR_RE = re.compile(r'[ \t]*<script src="https://unpkg\.com/@phosphor-icons/web@2\.0\.3"></script>')
_PHOSPHOR_LINK = '<link rel="stylesheet" href="/vendor/phosphor/phosphor.css?v=20260619">'
PHOSPHOR_PAGES = [rel for rel, _ in MENU_PAGES] + [
    "index.html", "index-light.html", "checkout.html", "copa/index.html",
]


def sync_phosphor():
    """Substitui o <script> do Phosphor (unpkg) por <link> pro CSS local. Cirúrgico,
    idempotente, CRLF-safe. Inclui as homes/checkout/copa (que os outros syncs não tocam)."""
    changed = same = skipped = 0
    for rel in PHOSPHOR_PAGES:
        path = os.path.join(BASE_DIR, *rel.split("/"))
        if not os.path.exists(path):
            skipped += 1
            continue
        with open(path, encoding="utf-8", newline="") as f:
            orig = f.read()
        if _PHOSPHOR_RE.search(orig):
            html = _PHOSPHOR_RE.sub(lambda m: "  " + _PHOSPHOR_LINK, orig)
        else:
            same += 1  # já trocado (ou sem o script)
            continue
        if html != orig:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(html)
            print(f"  ~ phosphor local: {rel}")
            changed += 1
        else:
            same += 1
    print(f"\n  Phosphor (CSS local) : {changed} trocada(s), {same} já em dia/sem script, {skipped} pulada(s).")


_IMG_TAG_RE = re.compile(r'<img\b[^>]*?>', re.S)


def sync_img_dims():
    """Adiciona width/height (medidos via Pillow) nas <img> sem dimensões → reduz CLS.
    Idempotente, CRLF-safe. Resolve src relativo (../) à pasta da página e root-absolute (/).
    Se Pillow ausente (ex.: servidor de produção), PULA sem erro (não quebra o admin)."""
    try:
        from PIL import Image
    except Exception:
        print("\n  Img dims: Pillow ausente, pulado (HTML já versionado mantém as dimensões).")
        return
    cache = {}

    def measure(page_path, src):
        s = src.split('?')[0]
        if not s or s.startswith('data:') or s.lower().endswith('.svg'):
            return None
        if s.startswith('/'):
            fp = os.path.join(BASE_DIR, *s.lstrip('/').split('/'))
        else:
            fp = os.path.normpath(os.path.join(os.path.dirname(page_path), *s.split('/')))
        if fp in cache:
            return cache[fp]
        d = None
        if os.path.exists(fp):
            try:
                with Image.open(fp) as im:
                    d = im.size
            except Exception:
                d = None
        cache[fp] = d
        return d

    changed = total = 0
    for rel in PHOSPHOR_PAGES:
        path = os.path.join(BASE_DIR, *rel.split("/"))
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8", newline="") as f:
            orig = f.read()
        cnt = [0]

        def repl(m):
            tag = m.group(0)
            if re.search(r'\bwidth\s*=', tag) or re.search(r'\bheight\s*=', tag):
                return tag
            sm = re.search(r'\bsrc="([^"]+)"', tag)
            if not sm:
                return tag
            d = measure(path, sm.group(1))
            if not d:
                return tag
            cnt[0] += 1
            return tag[:-1].rstrip() + ' width="%d" height="%d">' % (d[0], d[1])

        new = _IMG_TAG_RE.sub(repl, orig)
        if new != orig:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new)
            changed += 1
            total += cnt[0]
    print(f"\n  Img dims (width/height) : {total} img em {changed} página(s).")


def sync_configshim():
    """Injeta o shim window.miCfg() no <head> (após o viewport) p/ os consumidores
    compartilharem 1 fetch do config.json. Idempotente (pula se já tem), CRLF-safe.
    Cobre subpáginas + homes/checkout/copa (PHOSPHOR_PAGES)."""
    vp = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    changed = same = skipped = 0
    for rel in PHOSPHOR_PAGES:
        path = os.path.join(BASE_DIR, *rel.split("/"))
        if not os.path.exists(path):
            skipped += 1
            continue
        with open(path, encoding="utf-8", newline="") as f:
            orig = f.read()
        if "window.miCfg" in orig:
            same += 1
            continue
        if vp not in orig:
            skipped += 1
            continue
        nl = "\r\n" if "\r\n" in orig else "\n"
        html = orig.replace(vp, vp + nl + "  " + CFG_SHIM, 1)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(html)
        print(f"  ~ config-shim: {rel}")
        changed += 1
    print(f"\n  Config shim (miCfg) : {changed} injetada(s), {same} já em dia, {skipped} sem viewport.")


def sync_canonical():
    """Injeta/atualiza o <link rel="canonical"> SELF-REFERENTE no <head> de TODAS as
    subpaginas (MENU_PAGES). URL = SITE_URL + dir/ (ex.: familia/index.html ->
    https://masterinfointernet.com/familia/). Cirurgico (so a tag canonical),
    idempotente, CRLF-safe: atualiza se ja existir, insere antes do </head> se faltar.
    A home NAO entra: index.html/index-light.html tem canonical estatico apontando p/ a raiz."""
    changed = same = skipped = 0
    for rel, depth in MENU_PAGES:
        path = os.path.join(BASE_DIR, *rel.split("/"))
        if not os.path.exists(path):
            skipped += 1
            continue
        url_path = rel.rsplit("/index.html", 1)[0]
        canonical_url = f"{SITE_URL}/{url_path}/"
        link_line = f'<link rel="canonical" href="{canonical_url}">'
        with open(path, encoding="utf-8", newline="") as f:
            orig = f.read()
        nl = "\r\n" if "\r\n" in orig else "\n"
        if _CANONICAL_RE.search(orig):
            html = _CANONICAL_RE.sub(lambda m: "  " + link_line, orig)
        elif "</head>" in orig:
            html = orig.replace("</head>", "  " + link_line + nl + "</head>", 1)
        else:
            print(f"  ! pulado (sem </head>): {rel}")
            skipped += 1
            continue
        if html != orig:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(html)
            print(f"  ~ canonical: {rel} -> {canonical_url}")
            changed += 1
        else:
            same += 1
    print(f"\n  Canonical (self-referente): {changed} aplicada(s), {same} já em dia, {skipped} pulada(s).")


# SEO por página: <title> e <meta description> ÚNICOS e otimizados (keywords reais do
# GSC + "Joinville"). Mata o duplicate-meta (head() dava a mesma desc genérica p/ todas)
# e melhora o CTR. Title <=60 chars, desc ~150-160. Sem em-dash (pass anti-IA).
SEO_META = {
    "home-office/index.html": ("Internet para Home Office em Joinville | MasterInfo",
        "Internet fibra para trabalhar de casa em Joinville: conexão estável para reuniões, upload rápido e Wi-Fi 6. Planos home office com instalação rápida."),
    "gamer/index.html": ("Internet para Gamer em Joinville, Baixa Latência | MasterInfo",
        "Internet fibra para jogar online em Joinville: baixa latência, ping estável, 1 Giga e Exitlag. Plano gamer com Wi-Fi 6. Confira a cobertura."),
    "familia/index.html": ("Internet Fibra para Família em Joinville | MasterInfo",
        "Internet fibra óptica para a família toda em Joinville: 800 Mega a 1 Giga, Wi-Fi 6 e vários aparelhos ao mesmo tempo. Instalação rápida. Veja os planos."),
    "com-2-roteadores/index.html": ("Wi-Fi em Toda a Casa em Joinville (2 Roteadores) | MasterInfo",
        "Wi-Fi sem ponto cego em Joinville: kit com 2 roteadores Wi-Fi 6 para sinal forte em todos os cômodos. Cobertura total da casa. Veja os planos."),
    "com-1-roteador/index.html": ("Internet Fibra para Apartamento em Joinville | MasterInfo",
        "Internet fibra óptica para apartamento e casa pequena em Joinville, com roteador Wi-Fi 6. Planos a partir de 600 Mega. Confira a cobertura."),
    "contato/index.html": ("Fale com a MasterInfo, Contato em Joinville | MasterInfo",
        "Entre em contato com a MasterInfo Internet em Joinville: WhatsApp, telefone e atendimento local. Tire dúvidas sobre planos, cobertura e suporte."),
    "tv-streaming/index.html": ("Internet com TV e Streaming em Joinville | MasterInfo",
        "Internet fibra com TV ao vivo e apps de streaming inclusos em Joinville: SKY+ Light, Globoplay e mais. Planos com entretenimento. Confira."),
    "termos/index.html": ("Termos de Uso | MasterInfo Internet",
        "Termos de uso dos serviços de internet fibra óptica da MasterInfo em Joinville. Conheça as condições de contratação e uso dos planos."),
    "privacidade/index.html": ("Política de Privacidade | MasterInfo Internet",
        "Política de privacidade da MasterInfo Internet: como coletamos, usamos e protegemos seus dados pessoais conforme a LGPD."),
    "lgpd/index.html": ("LGPD e Proteção de Dados | MasterInfo Internet",
        "Como a MasterInfo trata seus dados conforme a Lei Geral de Proteção de Dados (LGPD). Seus direitos e nossos compromissos de privacidade."),
    "playhub/index.html": ("PlayHub: Apps e Streaming Inclusos | MasterInfo Internet",
        "PlayHub da MasterInfo: SKY+ Light, Deezer, Globoplay e mais apps de streaming inclusos no seu plano de internet fibra em Joinville. Conheça."),
    "aplicativos/sky-light/index.html": ("SKY+ Light na Internet Fibra MasterInfo | TV ao Vivo Inclusa",
        "SKY+ Light incluso no seu plano de internet fibra MasterInfo em Joinville: TV ao vivo nos canais que você ama, direto na conexão, sem antena. Veja como."),
    "aplicativos/deezer/index.html": ("Deezer Incluso na Internet Fibra | MasterInfo Joinville",
        "Música sem anúncios com Deezer incluso no seu plano de internet fibra MasterInfo em Joinville. Ouça onde quiser, sem interrupção."),
    "aplicativos/globoplay/index.html": ("Globoplay Incluso na Internet Fibra | MasterInfo Joinville",
        "Novelas, esportes e séries com Globoplay incluso no seu plano de internet fibra MasterInfo em Joinville. Assista quando e onde quiser."),
    "aplicativos/disney-plus/index.html": ("Disney+ Incluso na Internet Fibra | MasterInfo Joinville",
        "Disney, Pixar, Marvel e Star Wars com Disney+ incluso no seu plano de internet fibra MasterInfo em Joinville. Maratone os clássicos."),
    "aplicativos/hbo-max/index.html": ("HBO Max Incluso na Internet Fibra | MasterInfo Joinville",
        "Séries premium e filmes da Warner com HBO Max incluso no seu plano de internet fibra MasterInfo em Joinville. Assista em alta qualidade."),
    "aplicativos/prime-video/index.html": ("Prime Video Incluso na Internet Fibra | MasterInfo Joinville",
        "Amazon Originals, filmes e séries com Prime Video incluso no seu plano de internet fibra MasterInfo em Joinville. Entretenimento sem limite."),
    "aplicativos/exitlag/index.html": ("Exitlag Incluso, Internet Gamer | MasterInfo Joinville",
        "Reduza o ping e jogue sem lag com Exitlag incluso no seu plano de internet fibra MasterInfo em Joinville. Otimizador ideal para gamers."),
    "aplicativos/kaspersky/index.html": ("Kaspersky Incluso na Internet Fibra | MasterInfo Joinville",
        "Proteja seus dispositivos com o antivírus Kaspersky premium incluso no seu plano de internet fibra MasterInfo em Joinville. Navegue seguro."),
    "ajuda/wifi/index.html": ("Como Configurar seu Wi-Fi | Ajuda MasterInfo",
        "Passo a passo para configurar e melhorar seu Wi-Fi MasterInfo: posição do roteador, senha, canais e dicas para sinal forte em toda a casa."),
    "ajuda/reportar/index.html": ("Reportar um Problema na Internet | MasterInfo",
        "Está com a internet lenta ou fora do ar em Joinville? Veja como reportar um problema à MasterInfo e acionar o suporte técnico rápido."),
    "ajuda/boletos/index.html": ("2a Via de Boleto e Faturas | MasterInfo",
        "Acesse a 2a via do seu boleto MasterInfo, consulte faturas e formas de pagamento. Resolva sua fatura de internet em Joinville pelo chat da Marina."),
}

# Pilares + blog: title/desc únicos vindos do conteudo_blog. Mantém o SEO_META como
# fonte única dos syncs (title/meta/og/schema) para TODAS as páginas geradas.
for _pil in PILARES:
    SEO_META[f'{_pil["slug"]}/index.html'] = (_pil["title"], _pil["desc"])
SEO_META["blog/index.html"] = (
    "Blog MasterInfo: Dicas de Internet em Joinville",
    "Dicas e guias sobre internet fibra, Wi-Fi, velocidade e cobertura. Conteúdo da MasterInfo para você aproveitar melhor sua conexão em Joinville.")
for _post in BLOG:
    SEO_META[f'blog/{_post["slug"]}/index.html'] = (_post["title"], _post["desc"])
SEO_META["sobre/philipe/index.html"] = (
    "Philipe Alves Medeiros, Fundador da MasterInfo Internet",
    "Conheça Philipe Alves Medeiros, fundador da MasterInfo Internet em Joinville. Artigos sobre fibra óptica, Wi-Fi, velocidade e cobertura.")

_TITLE_RE = re.compile(r'<title>.*?</title>', re.DOTALL)
_DESC_RE = re.compile(r'<meta name="description" content="[^"]*">')


def sync_seo_meta():
    """Aplica <title> e <meta description> ÚNICOS (SEO_META) em cada subpágina.
    Cirúrgico (só title+desc), idempotente, CRLF-safe. Mata o duplicate-meta."""
    changed = same = skipped = 0
    for rel, depth in MENU_PAGES:
        if rel not in SEO_META:
            skipped += 1
            continue
        title, desc = SEO_META[rel]
        path = os.path.join(BASE_DIR, *rel.split("/"))
        if not os.path.exists(path):
            skipped += 1
            continue
        with open(path, encoding="utf-8", newline="") as f:
            orig = f.read()
        html = _TITLE_RE.sub(lambda m: '<title>' + title + '</title>', orig, count=1)
        html = _DESC_RE.sub(lambda m: '<meta name="description" content="' + desc + '">', html, count=1)
        if html != orig:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(html)
            print(f"  ~ seo-meta: {rel}")
            changed += 1
        else:
            same += 1
    print(f"\n  SEO meta (title + description): {changed} atualizada(s), {same} já em dia, {skipped} sem mapa.")


_OG_RE = re.compile(r'[ \t]*<!-- og:auto -->.*?<!-- /og:auto -->\r?\n?', re.DOTALL)
_SCHEMA_RE = re.compile(r'[ \t]*<!-- schema:auto -->.*?<!-- /schema:auto -->\r?\n?', re.DOTALL)


def sync_schema():
    """Injeta JSON-LD (BreadcrumbList + WebPage ligada ao Organization) no <head> de
    cada subpágina, elas não tinham schema nenhum (só a home tinha). Nome do breadcrumb
    derivado do SEO_META title (antes do ' | '). Bloco marcado, idempotente, CRLF-safe."""
    changed = same = skipped = 0
    for rel, depth in MENU_PAGES:
        if rel not in SEO_META:
            skipped += 1
            continue
        title, desc = SEO_META[rel]
        name = title.split(" | ")[0].strip()
        url = SITE_URL + "/" + rel.rsplit("/index.html", 1)[0] + "/"
        # BlogPosting (posts) / Blog (índice) / WebPage (pilares e demais).
        data = build_schema_data(rel, name, desc, url)
        path = os.path.join(BASE_DIR, *rel.split("/"))
        if not os.path.exists(path):
            skipped += 1
            continue
        with open(path, encoding="utf-8", newline="") as f:
            orig = f.read()
        nl = "\r\n" if "\r\n" in orig else "\n"
        json_str = json.dumps(data, ensure_ascii=False, indent=2).replace("\n", nl)
        block = nl.join([
            '  <!-- schema:auto -->',
            '  <script type="application/ld+json">',
            json_str,
            '  </script>',
            '  <!-- /schema:auto -->',
            '',
        ])
        if _SCHEMA_RE.search(orig):
            html = _SCHEMA_RE.sub(lambda m: block, orig, count=1)
        elif "</head>" in orig:
            html = orig.replace("</head>", block + "</head>", 1)
        else:
            print(f"  ! pulado (sem </head>): {rel}")
            skipped += 1
            continue
        if html != orig:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(html)
            print(f"  ~ schema: {rel}")
            changed += 1
        else:
            same += 1
    print(f"\n  JSON-LD (Breadcrumb + WebPage): {changed} atualizada(s), {same} já em dia, {skipped} sem mapa/head.")


def sync_og():
    """Injeta Open Graph + Twitter Card no <head> de cada subpágina (head() do gerador
    NÃO emite OG → links no WhatsApp/Facebook ficavam sem preview). Usa SEO_META p/
    title/desc + URL canônica + og-image.jpg (1200x630). Bloco marcado <!-- og:auto -->idempotente, CRLF-safe."""
    img = SITE_URL + "/og-image.jpg"
    changed = same = skipped = 0
    for rel, depth in MENU_PAGES:
        if rel not in SEO_META:
            skipped += 1
            continue
        title, desc = SEO_META[rel]
        url = SITE_URL + "/" + rel.rsplit("/index.html", 1)[0] + "/"
        img = (SITE_URL + OG_IMG_BY_REL[rel]) if rel in OG_IMG_BY_REL else (SITE_URL + "/og-image.jpg")
        path = os.path.join(BASE_DIR, *rel.split("/"))
        if not os.path.exists(path):
            skipped += 1
            continue
        with open(path, encoding="utf-8", newline="") as f:
            orig = f.read()
        nl = "\r\n" if "\r\n" in orig else "\n"
        # og:title/twitter:title sempre terminam com "| MasterInfo" (sem dobrar nos que ja tem).
        og_title = title if "MasterInfo" in title else title + " | MasterInfo"
        block = nl.join([
            '  <!-- og:auto -->',
            '  <meta property="og:type" content="website">',
            '  <meta property="og:site_name" content="MasterInfo Internet">',
            '  <meta property="og:title" content="' + og_title + '">',
            '  <meta property="og:description" content="' + desc + '">',
            '  <meta property="og:url" content="' + url + '">',
            '  <meta property="og:image" content="' + img + '">',
            '  <meta name="twitter:card" content="summary_large_image">',
            '  <meta name="twitter:title" content="' + og_title + '">',
            '  <meta name="twitter:description" content="' + desc + '">',
            '  <meta name="twitter:image" content="' + img + '">',
            '  <!-- /og:auto -->',
            '',
        ])
        if _OG_RE.search(orig):
            html = _OG_RE.sub(lambda m: block, orig, count=1)
        elif "</head>" in orig:
            html = orig.replace("</head>", block + "</head>", 1)
        else:
            print(f"  ! pulado (sem </head>): {rel}")
            skipped += 1
            continue
        if html != orig:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(html)
            print(f"  ~ og: {rel}")
            changed += 1
        else:
            same += 1
    print(f"\n  Open Graph + Twitter: {changed} atualizada(s), {same} já em dia, {skipped} sem mapa/head.")


def sync_menus():
    """Sincroniza HEADER (bloco <header>) e RODAPE (colunas .footer-col) de TODAS
    as paginas (menos a home) com config.menuHeader / config.menus.footer.

    Cirurgico (mexe so nesses 2 blocos), idempotente e CRLF-safe: preserva corpo,
    brand, chat e o resto de cada pagina. E o que se roda depois de editar os menus
    no admin. A home nao entra: monta tudo em runtime via site-loader.js.

    So grava o arquivo se header E rodape baterem 1x cada (senao pula e avisa, pra
    nunca corromper uma pagina com estrutura inesperada)."""
    changed = same = skipped = 0
    for rel, depth in MENU_PAGES:
        path = os.path.join(BASE_DIR, *rel.split("/"))
        if not os.path.exists(path):
            print(f"  ! pulado (nao existe): {rel}")
            skipped += 1
            continue
        with open(path, encoding="utf-8", newline="") as f:
            orig = f.read()
        nl = "\r\n" if "\r\n" in orig else "\n"
        header_html = build_header(depth)
        cols = render_footer_cols("../" * depth)
        if nl != "\n":
            header_html = header_html.replace("\n", nl)
            cols = cols.replace("\n", nl)
        html, nh = _HEADER_RE.subn(lambda m: header_html, orig)
        html, nf = _FOOTER_COLS_RE.subn(lambda m: cols + nl + "      ", html)
        if nh != 1 or nf != 1:
            print(f"  ! pulado (header x{nh}, rodape x{nf}; esperava 1 de cada): {rel}")
            skipped += 1
            continue
        if html != orig:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(html)
            print(f"  ~ menus sincronizados: {rel}")
            changed += 1
        else:
            same += 1
    print(f"\n  Menus (header + rodapé): {changed} atualizada(s), {same} já em dia, {skipped} pulada(s).")


def sync_site_scale():
    """Injeta/atualiza o <style>:root{--site-scale:X}</style> no <head> de TODAS as
    subpaginas (X = SITE_SCALE = config.layout.siteScale/100). Cirurgico (so o
    <style>), idempotente, CRLF-safe. Insere antes do </head> se ausente; atualiza
    o valor se ja existir. A home NAO entra: o site-loader.js seta a var em runtime."""
    style_line = f'<style>:root{{--site-scale:{SITE_SCALE}}}</style>'
    changed = same = skipped = 0
    for rel, depth in MENU_PAGES:
        path = os.path.join(BASE_DIR, *rel.split("/"))
        if not os.path.exists(path):
            skipped += 1
            continue
        with open(path, encoding="utf-8", newline="") as f:
            orig = f.read()
        nl = "\r\n" if "\r\n" in orig else "\n"
        if _SITE_SCALE_RE.search(orig):
            html = _SITE_SCALE_RE.sub(style_line, orig)
        elif "</head>" in orig:
            html = orig.replace("</head>", "  " + style_line + nl + "</head>", 1)
        else:
            print(f"  ! pulado (sem </head>): {rel}")
            skipped += 1
            continue
        if html != orig:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(html)
            print(f"  ~ escala aplicada: {rel}")
            changed += 1
        else:
            same += 1
    print(f"\n  Escala do site (--site-scale:{SITE_SCALE}): {changed} atualizada(s), {same} já em dia, {skipped} pulada(s).")


# Widgets flutuantes: script inline (marcado) injetado antes do </body> das subpaginas.
# Le config.json -> widgets em RUNTIME e esconde os FABs desligados no admin. Imune a
# adblock (sem nome 'tracking'); como le o config ao vivo, NAO precisa regenerar a cada
# toggle, basta existir uma vez nas paginas.
_WIDGETS_RE = re.compile(r'[ \t]*<script data-mi-widgets>.*?</script>', re.DOTALL)
_WIDGETS_SCRIPT = "<script data-mi-widgets>(function(){try{(window.miCfg?window.miCfg():fetch('/config.json?v='+Date.now()).then(function(r){return r.json();})).then(function(c){var w=(c&&c.widgets)||{},m={indicacao:'.indicar-float',boleto:'.boleto-float',whatsapp:'.whatsapp-float'};Object.keys(m).forEach(function(k){if(w[k]===false){var e=document.querySelector(m[k]);if(e)e.style.display='none';}});}).catch(function(){});}catch(e){}})();</script>"


def sync_widget_floats():
    """Injeta/atualiza o <script data-mi-widgets> antes do </body> de TODAS as
    subpaginas. Em runtime le config.json -> widgets e esconde .indicar-float/
    .boleto-float/.whatsapp-float marcados como false no admin. Cirurgico,
    idempotente, CRLF-safe. A home NAO entra (site-loader.js faz via loadWidgets)."""
    changed = same = skipped = 0
    for rel, depth in MENU_PAGES:
        path = os.path.join(BASE_DIR, *rel.split("/"))
        if not os.path.exists(path):
            skipped += 1
            continue
        with open(path, encoding="utf-8", newline="") as f:
            orig = f.read()
        nl = "\r\n" if "\r\n" in orig else "\n"
        if _WIDGETS_RE.search(orig):
            html = _WIDGETS_RE.sub(lambda m: "  " + _WIDGETS_SCRIPT, orig)
        elif "</body>" in orig:
            html = orig.replace("</body>", "  " + _WIDGETS_SCRIPT + nl + "</body>", 1)
        else:
            print(f"  ! pulado (sem </body>): {rel}")
            skipped += 1
            continue
        if html != orig:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(html)
            print(f"  ~ widgets script: {rel}")
            changed += 1
        else:
            same += 1
    print(f"\n  Widgets flutuantes (config.widgets): {changed} atualizada(s), {same} já em dia, {skipped} pulada(s).")


# Formas de pagamento em runtime: <script data-mi-payment> injetado antes do </body>
# das subpaginas. Le config.json -> formasPagamento e reconstroi .footer-payment-icons
# (default: PIX/Boleto/Cartao ON, Debito automatico OFF). Como le o config ao vivo, NAO
# precisa regenerar a cada toggle no admin. A home faz via site-loader.loadFormasPagamento.
_PAYMENT_RE = re.compile(r'[ \t]*<script data-mi-payment>.*?</script>', re.DOTALL)
_PAYMENT_SCRIPT = "<script data-mi-payment>(function(){try{var M=[['pix','PIX','ph-currency-circle-dollar'],['boleto','Boleto','ph-barcode'],['cartao','Cartão','ph-credit-card'],['debitoAutomatico','Débito automático','ph-bank']];var D={pix:true,boleto:true,cartao:true,debitoAutomatico:false};(window.miCfg?window.miCfg():fetch('/config.json?v='+Date.now()).then(function(r){return r.json();})).then(function(c){var fp=(c&&c.formasPagamento)||{},box=document.querySelector('.footer-payment-icons');if(!box)return;box.innerHTML=M.filter(function(m){var v=(m[0] in fp)?fp[m[0]]:D[m[0]];return v!==false;}).map(function(m){return '<span class=\"payment-icon\"><i class=\"ph-fill '+m[2]+'\"></i> '+m[1]+'</span>';}).join('');}).catch(function(){});}catch(e){}})();</script>"
# Linha estatica do "Debito automatico" no rodape (removida das subpaginas; default OFF).
_DEBITO_STATIC_RE = re.compile(r'[ \t]*<span class="payment-icon"><i class="ph-fill ph-bank"></i> Débito automático</span>\r?\n')


def sync_payment():
    """Remove a forma estatica 'Debito automatico' do rodape e injeta/atualiza o
    <script data-mi-payment> antes do </body> de TODAS as subpaginas. A home NAO entra
    (site-loader.js faz via loadFormasPagamento). Cirurgico, idempotente, CRLF-safe."""
    changed = same = skipped = 0
    for rel, depth in MENU_PAGES:
        path = os.path.join(BASE_DIR, *rel.split("/"))
        if not os.path.exists(path):
            skipped += 1
            continue
        with open(path, encoding="utf-8", newline="") as f:
            orig = f.read()
        nl = "\r\n" if "\r\n" in orig else "\n"
        html = _DEBITO_STATIC_RE.sub("", orig)
        if _PAYMENT_RE.search(html):
            html = _PAYMENT_RE.sub(lambda m: "  " + _PAYMENT_SCRIPT, html)
        elif "</body>" in html:
            html = html.replace("</body>", "  " + _PAYMENT_SCRIPT + nl + "</body>", 1)
        else:
            print(f"  ! pulado (sem </body>): {rel}")
            skipped += 1
            continue
        if html != orig:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(html)
            print(f"  ~ formas de pagamento: {rel}")
            changed += 1
        else:
            same += 1
    print(f"\n  Formas de pagamento (config.formasPagamento): {changed} atualizada(s), {same} já em dia, {skipped} pulada(s).")


# Planos em runtime: o PLANS_SYNC_SCRIPT (definido junto do page_internet) injetado
# antes do </body> das subpaginas que tem tabela de plano (.sub-plan-card). Le
# config.json -> planos ao vivo e sincroniza nome/velocidade/unidade/precos/features
# dos cards. Como le o config ao vivo, NAO precisa regenerar a cada edicao no admin.
_PLANS_RE = re.compile(r'[ \t]*<script data-mi-plans>.*?</script>', re.DOTALL)


def sync_plans_runtime():
    """Injeta/atualiza o <script data-mi-plans> antes do </body> das subpaginas que
    tem .sub-plan-card (as 5 paginas de Internet). Em runtime le config.json ->
    planos e sincroniza os cards com o admin (mesma fonte que o site-loader.loadPlanos
    usa na home). Cirurgico, idempotente, CRLF-safe. A home NAO entra."""
    changed = same = skipped = 0
    for rel, depth in MENU_PAGES:
        path = os.path.join(BASE_DIR, *rel.split("/"))
        if not os.path.exists(path):
            skipped += 1
            continue
        with open(path, encoding="utf-8", newline="") as f:
            orig = f.read()
        # So mexe nas paginas que tem tabela de plano.
        if "sub-plan-card" not in orig:
            continue
        nl = "\r\n" if "\r\n" in orig else "\n"
        if _PLANS_RE.search(orig):
            html = _PLANS_RE.sub(lambda m: "  " + PLANS_SYNC_SCRIPT, orig)
        elif "</body>" in orig:
            html = orig.replace("</body>", "  " + PLANS_SYNC_SCRIPT + nl + "</body>", 1)
        else:
            print(f"  ! pulado (sem </body>): {rel}")
            skipped += 1
            continue
        if html != orig:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(html)
            print(f"  ~ planos runtime: {rel}")
            changed += 1
        else:
            same += 1
    print(f"\n  Planos em runtime (data-mi-plans): {changed} atualizada(s), {same} já em dia, {skipped} pulada(s).")


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  + {os.path.relpath(path, BASE_DIR)}")


def sync_subpage_ctas():
    """Aponta os CTAs das paginas Internet (hero + cada card de plano) DIRETO pro
    checkout com o plano (hero = plano principal; cada card = o seu plano, na ordem
    de p["plans"]). CIRURGICO: troca SO os hrefs dos CTAs, nao toca corpo/footer, por isso NAO reverte o DRIFT dos templates de corpo. Idempotente."""
    changed = 0
    for p in INTERNET:
        path = os.path.join(BASE_DIR, p["slug"], "index.html")
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8", newline="") as f:
            html = f.read()
        orig = html
        plans = p.get("plans") or []
        primary = plans[0] if plans else None
        if primary:
            html = html.replace(
                '<a href="../#planos" class="sub-hero-cta">',
                '<a href="../checkout.html?plano=' + primary + '" class="sub-hero-cta">')
        counter = {"i": 0}
        def repl_card(m):
            i = counter["i"]; counter["i"] += 1
            plano = plans[i] if i < len(plans) else (primary or "")
            return '<a href="../checkout.html?plano=' + plano + '" class="sub-plan-card">'
        html = re.sub(r'<a href="\.\./#planos" class="sub-plan-card">', repl_card, html)
        if html != orig:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(html)
            print(f"  ~ CTAs -> checkout: {p['slug']} (hero={primary}, cards={plans})")
            changed += 1
    print(f"  CTAs das subpaginas Internet: {changed} atualizada(s).")


def gerar_bodies():
    """Regenera o CORPO completo (hero/planos/destaques/chat) das 16 subpaginas
    a partir dos dados deste arquivo.

    ATENCAO: os templates de corpo aqui estao DEFASADOS em relacao ao HTML
    versionado (brand/social/chat foram editados direto no HTML e nao retro-
    portados pro template). Use --full so quando for INTENCIONALMENTE regenerar
    conteudo, senao ele reverte essas melhorias."""
    print("Internet (5 páginas)…")
    for p in INTERNET:
        write_file(os.path.join(BASE_DIR, p["slug"], "index.html"), page_internet(p, depth=1))
    print("\nAplicativos (8 páginas)…")
    for a in APLICATIVOS:
        write_file(os.path.join(BASE_DIR, "aplicativos", a["slug"], "index.html"), page_app(a, depth=2))
    print("\nAjuda (3 páginas)…")
    for a in AJUDA:
        write_file(os.path.join(BASE_DIR, "ajuda", a["slug"], "index.html"), page_ajuda(a, depth=2))
    print("\nPlayHub (1 página)…")
    write_file(os.path.join(BASE_DIR, "playhub", "index.html"), page_playhub(depth=1))


def gerar_internet_hero():
    """Gera internet-hero.json: 1 entrada por pagina de Internet (slug, title, tag,
    1a imagem do slideshow da pagina, href). A home (site-loader.loadHeroPaginas) le
    esse arquivo quando config.homeHero.usarPaginas = true e mostra 1 slide por pagina
    com o titulo por cima. Paths ROOT-relative (a home esta na raiz, sem ../)."""
    out = []
    for p in INTERNET:
        imgs = find_imgs(IMG_BG.get(p["slug"], ""), BASE_DIR)
        if not imgs:
            print(f"  ! '{p['slug']}' sem imagem em imgs/hero/sub, pulando")
            continue
        out.append({
            "slug": p["slug"],
            "title": p["title"],
            "tag": p["tag"],
            "img": imgs[0],
            "plano": (p["plans"][0] if p.get("plans") else None),  # plano primário → checkout
            "cta": p.get("cta") or "Quero esse plano",
            "href": "#planos",  # fallback se o plano não existir
        })
    path = os.path.join(BASE_DIR, "internet-hero.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"  internet-hero.json: {len(out)} pagina(s).")


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "--menus"
    if modo in ("--full", "--tudo", "--bodies"):
        print(">> Modo FULL: regenera corpos + sincroniza menus (header + rodapé).")
        print("   (templates de corpo podem estar defasados, ver docstring de gerar_bodies)\n")
        gerar_bodies()
        print("\nSincronizando header + rodapé com o config.json…")
        sync_menus()
    elif modo in ("--content", "--blog", "--paginas"):
        print(">> Modo CONTENT: gera páginas-pilar + blog, depois sincroniza tudo.\n")
        gerar_pilares()
        gerar_blog()
        print("\nSincronizando header + rodapé com o config.json…")
        sync_menus()
    else:  # --menus (padrão): SÓ header + rodapé, cirúrgico e seguro de rodar sempre
        print(">> Sincronizando os menus (header + rodapé): config.json → todas as páginas…\n")
        sync_menus()
    print("\nEscala do site (--site-scale) → subpáginas…")
    sync_site_scale()
    print("\nCanonical (self-referente) → subpáginas…")
    sync_canonical()
    print("\nPhosphor (CSS local, sem unpkg) → páginas…")
    sync_phosphor()
    print("\nConfig shim (1 fetch do config.json) → páginas…")
    sync_configshim()
    print("\nImg dims (width/height p/ CLS) → páginas…")
    sync_img_dims()
    print("\nSEO meta (title + description únicos) → subpáginas…")
    sync_seo_meta()
    print("\nOpen Graph + Twitter Card → subpáginas…")
    sync_og()
    print("\nJSON-LD (Breadcrumb + WebPage) → subpáginas…")
    sync_schema()
    print("\nWidgets flutuantes (config.widgets) → subpáginas…")
    sync_widget_floats()
    print("\nFormas de pagamento (config.formasPagamento) → subpáginas…")
    sync_payment()
    print("\nPlanos em runtime (config.planos) → subpáginas…")
    sync_plans_runtime()
    print("\nCTAs das subpáginas Internet → checkout…")
    sync_subpage_ctas()
    print("\nHero da home por páginas (internet-hero.json)…")
    gerar_internet_hero()
    print("\n✓ Concluído.")
