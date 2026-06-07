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
            ("📞", "Reunião sem queda", "Conexão estável pra Zoom, Teams, Meet — chovendo ou fazendo sol."),
            ("☁️", "Upload turbinado", "Mandar arquivo grande, fazer backup em nuvem, sem espera."),
            ("⚡", "Latência baixa", "Resposta rápida em ferramentas em tempo real."),
        ],
        "plans": ["lite-home-office", "ultra-home-office"],
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
        "plans": ["lite-home-office", "ultra-home-office"],
        "cta": "Quero internet de gamer",
    },
    {
        "slug": "familia",
        "tag": "INTERNET · PRA FAMÍLIA",
        "title": "Internet pra família toda usar ao mesmo tempo",
        "subtitle": "Vários celulares, TV no streaming, criança no tablet, jogo do filho online — tudo junto, sem travar. Wi-Fi com força pra casa cheia.",
        "ico": "ph-users-three",
        "gradient": "linear-gradient(135deg, #c1121f 0%, #ff7a05 50%, #fcc305 100%)",
        "highlights": [
            ("👨‍👩‍👧‍👦", "Tudo rodando junto", "Mãe na novela, pai no jogo, filhos no TikTok — tudo ao mesmo tempo, sem trava."),
            ("📺", "Streaming em 4K", "Netflix, Disney+, Globoplay e SKY+ rodando em qualquer TV da casa."),
            ("🛡️", "Wi-Fi seguro pra criança", "Suporte pra controle parental e antivírus Kaspersky opcional."),
        ],
        "plans": ["lite-familia", "ultra-familia"],
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
        "plans": ["ultra-familia", "ultra-home-office"],
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
            ("💸", "Preço justo", "A partir de R$ 79,90/mês — sem letra miúda."),
            ("⚡", "Fibra óptica real", "Mesmo plano de entrada, mesma fibra dos planos premium."),
        ],
        "plans": ["lite-casa", "lite-familia", "lite-home-office"],
        "cta": "Quero plano com 1 roteador",
    },
]

APLICATIVOS = [
    {"slug": "sky-light", "name": "SKY+ Light", "tag": "TV ao vivo",
     "desc": "Canais de TV no celular, smart TV ou computador. Esportes, jornalismo, novelas — onde você estiver.",
     "logo": "sky.jpg",
     "highlights": ["50+ canais ao vivo", "App pra smart TV, celular e PC", "Sem antena, sem parabólica"],
     "incluso_em": "Lite Casa, Família, Home Office e toda linha Ultra"},
    {"slug": "deezer", "name": "Deezer", "tag": "Música sem anúncios",
     "desc": "Mais de 90 milhões de músicas em alta qualidade. Sem propaganda, modo offline, playlists personalizadas.",
     "logo": "deezer.webp",
     "highlights": ["90M+ músicas em HD", "Modo offline (baixe e ouça sem net)", "Sem nenhum anúncio"],
     "incluso_em": "Lite Home Office (à escolha entre SKY+ Light ou Deezer)"},
    {"slug": "globoplay", "name": "Globoplay", "tag": "Novelas e esportes",
     "desc": "Novelas inéditas, séries originais, futebol ao vivo e tudo da Globo on demand.",
     "logo": "globoplay.png",
     "highlights": ["Novelas e séries Globo", "Futebol ao vivo (Brasileirão, Libertadores)", "Filmes Telecine inclusos"],
     "incluso_em": "Ultra Família"},
    {"slug": "disney-plus", "name": "Disney+", "tag": "Disney, Pixar, Marvel",
     "desc": "Disney, Pixar, Marvel, Star Wars e National Geographic — tudo em um único app, sem anúncios.",
     "logo": "disney-plus.png",
     "highlights": ["Tudo da Disney, Pixar, Marvel", "Star Wars e Nat Geo", "4K, Dolby Atmos, sem ads"],
     "incluso_em": "Ultra Home Office"},
    {"slug": "hbo-max", "name": "HBO Max", "tag": "Séries premium e Warner",
     "desc": "Séries originais da HBO, filmes Warner, DC, Cartoon Network. As maiores produções num só lugar.",
     "logo": "hbo-max.jpg",
     "highlights": ["Game of Thrones, House of the Dragon, The Last of Us", "Filmes Warner em estreia", "DC Universe completo"],
     "incluso_em": "Add-on disponível em todos os planos"},
    {"slug": "prime-video", "name": "Prime Video", "tag": "Amazon Originals",
     "desc": "Séries originais Amazon (The Boys, Reacher, Rings of Power), filmes em estreia e clássicos.",
     "logo": "prime-video.png",
     "highlights": ["The Boys, Reacher, Fallout", "Filmes em estreia", "Combo com SKY+ Light disponível"],
     "incluso_em": "Add-on combo SKY+ Light + Amazon"},
    {"slug": "exitlag", "name": "Exitlag", "tag": "Otimizador pra gamers",
     "desc": "Reduz seu ping até 70% em jogos online — Valorant, CS, LoL, Fortnite. Conexão otimizada por servidores dedicados.",
     "logo": "exitlag.png",
     "highlights": ["Ping até 70% menor", "Suporta 1.000+ jogos", "Servidores dedicados pra gamers"],
     "incluso_em": "Add-on disponível em todos os planos"},
    {"slug": "kaspersky", "name": "Kaspersky", "tag": "Antivírus premium",
     "desc": "Proteção completa pra 3 dispositivos. Antivírus, VPN, gerenciador de senhas e proteção pra crianças.",
     "logo": "kaspersky.webp",
     "highlights": ["Protege até 3 dispositivos", "VPN ilimitada inclusa", "Controle parental e antivírus"],
     "incluso_em": "Add-on disponível em todos os planos"},
]

AJUDA = [
    {
        "slug": "wifi",
        "tag": "AJUDA · WI-FI",
        "title": "Como configurar seu Wi-Fi",
        "subtitle": "Trocar o nome da rede, mudar a senha e deixar o sinal forte em toda a casa — passo a passo, sem complicação.",
        "gradient": "linear-gradient(135deg, #6b3d00 0%, #c19000 50%, #fcc305 100%)",
        "steps": [
            ("🔑", "Trocar a senha do Wi-Fi", "Acesse o painel do roteador (geralmente 192.168.0.1 ou 192.168.1.1) com o login do aparelho e altere o campo de senha da rede."),
            ("📶", "Deixar o sinal mais forte", "Posicione o roteador num ponto central e alto, longe de paredes grossas, micro-ondas e espelhos. Casa grande pede o plano com 2 roteadores (mesh)."),
            ("🔄", "Reiniciar quando travar", "Tire o roteador da tomada por 30 segundos e ligue de novo — resolve a maioria das lentidões momentâneas."),
        ],
        "cta_label": "Falar com o suporte no WhatsApp",
        "cta_href": "https://wa.me/5547989212991?text=Ol%C3%A1!%20Preciso%20de%20ajuda%20para%20configurar%20meu%20Wi-Fi.",
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
            ("📡", "Quedas constantes", "Anote os horários em que cai — isso ajuda nossa equipe a identificar a causa mais rápido."),
        ],
        "cta_label": "Abrir chamado no WhatsApp",
        "cta_href": "https://wa.me/5547989212991?text=Ol%C3%A1!%20Quero%20reportar%20um%20problema%20na%20minha%20internet.",
    },
    {
        "slug": "boletos",
        "tag": "AJUDA · FINANCEIRO",
        "title": "Boletos e faturas",
        "subtitle": "Segunda via, vencimento e formas de pagamento — tudo na Central do Assinante, quando você quiser.",
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
    "lite-casa": {
        "nome": "1 Roteador", "speed": "600", "preco": "99,90", "preco_cheio": "109,90",
        "apps": [{"logo": "sky.jpg", "nome": "SKY Light"}],
        "features": [
            "Wi-Fi em 1 ambiente",
            "SKY+ Light grátis",
            "Suporte Sábado e Domingo",
        ],
    },
    "lite-familia": {
        "nome": "1 Roteador", "speed": "800", "preco": "109,00", "preco_cheio": "119,00",
        "apps": [{"logo": "sky.jpg", "nome": "SKY Light"}],
        "features": [
            "Wi-Fi em 1 ambiente",
            "SKY+ Light grátis",
            "Velocidade pra família",
        ],
    },
    "lite-home-office": {
        "nome": "1 Roteador", "speed": "1000", "preco": "119,90", "preco_cheio": "129,90",
        "apps": [
            {"logo": "sky.jpg", "nome": "SKY Light"},
            {"logo": "deezer.webp", "nome": "Deezer"},
        ],
        "apps_sep": "ou",
        "features": [
            "Wi-Fi em 1 ambiente",
            "Escolha entre SKY+ Light ou Deezer",
            "1 Giga para trabalho remoto",
        ],
    },
    "ultra-familia": {
        "nome": "2 Roteadores", "speed": "800", "preco": "139,90", "preco_cheio": "159,90",
        "apps": [{"logo": "globoplay.png", "nome": "Globoplay"}],
        "features": [
            "Wi-Fi em toda a casa (Mesh)",
            "Globoplay incluso",
            "Cobertura sem ponto cego",
        ],
    },
    "ultra-home-office": {
        "nome": "2 Roteadores", "speed": "1000", "preco": "218,60", "preco_cheio": "228,60",
        "apps": [
            {"logo": "sky.jpg", "nome": "SKY Light"},
            {"logo": "disney-plus.png", "nome": "Disney+"},
        ],
        "apps_sep": "+",
        "features": [
            "Wi-Fi em toda a casa (Mesh)",
            "SKY+ Light + Disney+ inclusos",
            "Suporte prioritário",
        ],
    },
}

# ─── HEADER + FOOTER COMUNS ──────────────────────────────────────────

def head(title, depth):
    base = "../" * depth
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | MasterInfo Internet</title>
  <meta name="description" content="MasterInfo Internet — fibra óptica 100% em Joinville.">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/@phosphor-icons/web@2.0.3"></script>
  <link rel="icon" type="image/svg+xml" href="{base}favicon.svg">
  <link rel="stylesheet" href="{base}styles.css?v=20260531-e">
  <link rel="stylesheet" href="{base}modal.css?v=20260531-e">
  <style>:root{{--site-scale:{SITE_SCALE}}}</style>
</head>
<body>'''


def build_header(depth):
    """Monta o <header> a partir de config.menuHeader — o MESMO resultado que o
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
                tgt = f' target="{c["target"]}"' if c.get("target") else ''
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
            tgt = f' target="{it["target"]}"' if it.get("target") else ''
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
        f'        <a href="{cb.get("href", "#")}" target="{cb.get("target", "_blank")}" class="header-client-btn">',
        f'          <i class="ph-fill ph-user-circle"></i><span>{cb.get("label", "Área do Cliente")}</span>',
        '        </a>',
        '      </nav>',
        '      <button class="mobile-toggle" id="mobileToggle" aria-label="Menu"><span></span><span></span><span></span></button>',
        '    </div>',
        '    <div class="mega-backdrop" id="megaBackdrop"></div>',
        '  </header>',
    ])


def header(depth):
    # O <header> sai do config.menuHeader (build_header) — igual à home.
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


def footer(depth, boleto=True):
    base = "../" * depth
    boleto_html = (f'''
  <!-- ========== BOLETO / 2ª VIA FLOAT ========== -->
  <a href="/ajuda/boletos" class="boleto-float" aria-label="Boletos e 2ª via de fatura">
    <span class="boleto-tooltip">
      <span class="boleto-tooltip-text">2ª via de boleto</span>
      <span class="boleto-tooltip-sub">Chat na hora com a Marina</span>
    </span>
    <i class="ph-fill ph-barcode"></i>
    <span class="boleto-pulse"></span>
  </a>
  <script src="{base}marina-widget.js?v=20260602-a" defer></script>''') if boleto else ""
    return f'''
  <!-- FOOTER -->
  <footer class="footer" id="contato">
    <div class="footer-trust">
      <div class="container footer-trust-inner">
        <div class="footer-trust-item"><i class="ph-fill ph-star"></i><div><strong>4,9 / 5</strong><span>2.382 avaliações no Google</span></div></div>
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
            <a href="https://www.instagram.com/masterinfo.internet" target="_blank"><i class="ph ph-instagram-logo"></i></a>
            <a href="https://www.facebook.com/masterinfointernet" target="_blank"><i class="ph ph-facebook-logo"></i></a>
            <a href="https://wa.me/554734341734" target="_blank"><i class="ph ph-whatsapp-logo"></i></a>
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
          <span class="payment-icon"><i class="ph-fill ph-bank"></i> Débito automático</span>
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

  <a href="https://wa.me/5547989212991" class="whatsapp-float" target="_blank">
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
  <script src="/tracking.js?v=20260603a" defer></script>
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


def page_internet(p, depth=1):
    plan_cards = ""
    for plan_id in p["plans"]:
        plan = PLANS_MAP[plan_id]

        # Faixa de apps
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
            for f in plan["features"]
        )

        plan_cards += f'''
        <a href="../checkout.html?plano={plan_id}" class="sub-plan-card">
          <div class="sub-plan-head">
            <span class="sub-plan-speed">{plan["speed"]}<small> Mega</small></span>
            <span class="sub-plan-name">{plan["nome"]}</span>
          </div>
          <div class="sub-plan-price-wrap">
            <span class="sub-plan-price-original">de <s>R$ {plan["preco_cheio"]}</s> por</span>
            <span class="sub-plan-price">R$ {plan["preco"]} <em>/mês</em></span>
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

    return f'''{head(p["title"], depth)}
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

{footer(depth)}'''


def page_app(a, depth=2):
    highlights_html = ""
    for h in a["highlights"]:
        highlights_html += f'<li><i class="ph-fill ph-check-circle"></i> {h}</li>'

    return f'''{head(a["name"], depth)}
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

  <!-- O que tem -->
  <section class="sub-section sub-section-light">
    <div class="container sub-section-narrow">
      <div class="section-header section-header-tight">
        <h2 class="section-title">O que vem incluso</h2>
      </div>
      <ul class="sub-app-features">{highlights_html}
      </ul>
      <p class="sub-app-incluso">
        <strong>Disponível em:</strong> {a["incluso_em"]}
      </p>
    </div>
  </section>

{footer(depth)}'''


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
          <p class="mi-chat-note">Usamos seu CPF só pra localizar suas faturas. <a href="https://wa.me/5547989212991" target="_blank">Prefere o WhatsApp?</a></p>
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
      if (b.url_pdf) html += '<a class="mi-boleto-btn" href="'+esc(b.url_pdf)+'" target="_blank"><i class="ph ph-file-pdf"></i> Baixar PDF</a>';
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
      <a href="{a["cta_href"]}" target="_blank" class="sub-hero-cta">{a["cta_label"]} <i class="ph ph-arrow-right"></i></a>
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
MENU_PAGES = (
    [(f'{p["slug"]}/index.html', 1) for p in INTERNET]
    + [(f'{s}/index.html', 1) for s in
       ("contato", "tv-streaming", "termos", "privacidade", "lgpd")]
    + [(f'aplicativos/{a["slug"]}/index.html', 2) for a in APLICATIVOS]
    + [(f'ajuda/{a["slug"]}/index.html', 2) for a in AJUDA]
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


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  + {os.path.relpath(path, BASE_DIR)}")


def sync_subpage_ctas():
    """Aponta os CTAs das paginas Internet (hero + cada card de plano) DIRETO pro
    checkout com o plano (hero = plano principal; cada card = o seu plano, na ordem
    de p["plans"]). CIRURGICO: troca SO os hrefs dos CTAs, nao toca corpo/footer —
    por isso NAO reverte o DRIFT dos templates de corpo. Idempotente."""
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
    conteudo — senao ele reverte essas melhorias."""
    print("Internet (5 páginas)…")
    for p in INTERNET:
        write_file(os.path.join(BASE_DIR, p["slug"], "index.html"), page_internet(p, depth=1))
    print("\nAplicativos (8 páginas)…")
    for a in APLICATIVOS:
        write_file(os.path.join(BASE_DIR, "aplicativos", a["slug"], "index.html"), page_app(a, depth=2))
    print("\nAjuda (3 páginas)…")
    for a in AJUDA:
        write_file(os.path.join(BASE_DIR, "ajuda", a["slug"], "index.html"), page_ajuda(a, depth=2))


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "--menus"
    if modo in ("--full", "--tudo", "--bodies"):
        print(">> Modo FULL: regenera corpos + sincroniza menus (header + rodapé).")
        print("   (templates de corpo podem estar defasados — ver docstring de gerar_bodies)\n")
        gerar_bodies()
        print("\nSincronizando header + rodapé com o config.json…")
        sync_menus()
    else:  # --menus (padrão): SÓ header + rodapé, cirúrgico e seguro de rodar sempre
        print(">> Sincronizando os menus (header + rodapé): config.json → todas as páginas…\n")
        sync_menus()
    print("\nEscala do site (--site-scale) → subpáginas…")
    sync_site_scale()
    print("\nCTAs das subpáginas Internet → checkout…")
    sync_subpage_ctas()
    print("\n✓ Concluído.")
