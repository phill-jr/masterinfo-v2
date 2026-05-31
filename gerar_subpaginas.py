# -*- coding: utf-8 -*-
"""Gera 12 subpaginas (Internet + Aplicativos) com layout consistente."""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
        "slug": "com-2-roteadores",
        "tag": "INTERNET · WI-FI EM TODA A CASA",
        "title": "Wi-Fi em toda a casa, sem ponto cego",
        "subtitle": "Com 2 roteadores em rede mesh, você navega forte da cozinha ao quintal. Mesma velocidade em qualquer cômodo.",
        "ico": "ph-broadcast",
        "gradient": "linear-gradient(135deg, #8b0a17 0%, #e63946 50%, #ff7a05 100%)",
        "highlights": [
            ("📶", "Cobertura total", "Dois roteadores cobrem casas grandes, sobrados e quintal."),
            ("🔄", "Roaming inteligente", "Seu celular troca de roteador sozinho, sem cair conexão."),
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
  <link rel="stylesheet" href="{base}styles.css?v=20260531-d">
  <link rel="stylesheet" href="{base}modal.css?v=20260531-d">
</head>
<body>'''


def header(depth):
    base = "../" * depth
    return f'''
  <!-- HEADER -->
  <header class="header" id="header">
    <div class="container header-inner">
      <a href="{base}" class="logo">
        <img src="{base}imgs/logo-masterinfo.png" alt="MasterInfo Internet" class="logo-img">
      </a>
      <nav class="nav" id="nav">
        <ul class="nav-list nav-list-sales">
          <li class="nav-item has-mega">
            <button class="nav-trigger" type="button">Internet <i class="ph ph-caret-down nav-trigger-caret"></i></button>
            <div class="mega-menu mega-menu-simple">
              <div class="mega-menu-inner">
                <ul class="dropdown-list">
                  <li><a href="{base}home-office/" class="dropdown-link">Home Office</a></li>
                  <li><a href="{base}gamer/" class="dropdown-link">Gamer</a></li>
                  <li><a href="{base}com-2-roteadores/" class="dropdown-link">Com 2 Roteadores</a></li>
                  <li><a href="{base}com-1-roteador/" class="dropdown-link">Com 1 Roteador</a></li>
                </ul>
              </div>
            </div>
          </li>
          <li class="nav-item"><a href="{base}#planos" class="nav-link">TV e Streaming</a></li>
          <li class="nav-item"><a href="{base}#cobertura" class="nav-link">Cobertura</a></li>
          <li class="nav-item"><a href="{base}#nossa-historia" class="nav-link">Nossa História</a></li>
          <li class="nav-item"><a href="{base}#contato" class="nav-link">Contato</a></li>
        </ul>

        <span class="nav-divider" aria-hidden="true"></span>

        <ul class="nav-list nav-list-client">
          <li class="nav-item has-mega">
            <button class="nav-trigger" type="button">Aplicativos <i class="ph ph-caret-down nav-trigger-caret"></i></button>
            <div class="mega-menu mega-menu-simple">
              <div class="mega-menu-inner">
                <ul class="dropdown-list">
                  <li><a href="{base}aplicativos/sky-light/" class="dropdown-link">
                    <img class="dropdown-logo dropdown-logo-real" src="{base}imgs/sky.jpg" alt="">SKY+ Light</a></li>
                  <li><a href="{base}aplicativos/deezer/" class="dropdown-link">
                    <img class="dropdown-logo dropdown-logo-real" src="{base}imgs/deezer.webp" alt="">Deezer</a></li>
                  <li><a href="{base}aplicativos/globoplay/" class="dropdown-link">
                    <img class="dropdown-logo dropdown-logo-real" src="{base}imgs/globoplay.png" alt="">Globoplay</a></li>
                  <li><a href="{base}aplicativos/disney-plus/" class="dropdown-link">
                    <img class="dropdown-logo dropdown-logo-real" src="{base}imgs/disney-plus.png" alt="">Disney+</a></li>
                  <li><a href="{base}aplicativos/hbo-max/" class="dropdown-link">
                    <img class="dropdown-logo dropdown-logo-real" src="{base}imgs/hbo-max.jpg" alt="">HBO Max</a></li>
                  <li><a href="{base}aplicativos/prime-video/" class="dropdown-link">
                    <img class="dropdown-logo dropdown-logo-real" src="{base}imgs/prime-video.png" alt="">Prime Video</a></li>
                  <li><a href="{base}aplicativos/exitlag/" class="dropdown-link">
                    <img class="dropdown-logo dropdown-logo-real" src="{base}imgs/exitlag.png" alt="">Exitlag</a></li>
                  <li><a href="{base}aplicativos/kaspersky/" class="dropdown-link">
                    <img class="dropdown-logo dropdown-logo-real" src="{base}imgs/kaspersky.webp" alt="">Kaspersky</a></li>
                </ul>
              </div>
            </div>
          </li>
          <li class="nav-item has-mega">
            <button class="nav-trigger" type="button">Ajuda <i class="ph ph-caret-down nav-trigger-caret"></i></button>
            <div class="mega-menu mega-menu-simple">
              <div class="mega-menu-inner">
                <ul class="dropdown-list">
                  <li><a href="https://wa.me/5547989212991" target="_blank" class="dropdown-link">Suporte WhatsApp</a></li>
                  <li><a href="https://www.speedtest.net" target="_blank" class="dropdown-link">Speedtest</a></li>
                  <li><a href="{base}ajuda/wifi" class="dropdown-link">Configurar Wi-Fi</a></li>
                  <li><a href="{base}#faq" class="dropdown-link">Perguntas frequentes</a></li>
                  <li><a href="{base}ajuda/reportar" class="dropdown-link">Reportar problema</a></li>
                  <li><a href="{base}ajuda/boletos" class="dropdown-link">Boletos e faturas</a></li>
                </ul>
              </div>
            </div>
          </li>
        </ul>

        <a href="https://sistema1.masterinfointernet.com/central_assinante_web/login" target="_blank" class="header-client-btn">
          <i class="ph-fill ph-user-circle"></i><span>Área do Cliente</span>
        </a>
      </nav>
      <button class="mobile-toggle" id="mobileToggle" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
    <div class="mega-backdrop" id="megaBackdrop"></div>
  </header>'''


def footer(depth):
    base = "../" * depth
    return f'''
  <!-- FOOTER -->
  <footer class="footer" id="contato">
    <div class="footer-trust">
      <div class="container footer-trust-inner">
        <div class="footer-trust-item"><i class="ph-fill ph-star"></i><div><strong>4,9 / 5</strong><span>2.382 avaliações no Google</span></div></div>
        <div class="footer-trust-item"><i class="ph-fill ph-lightning"></i><div><strong>100% Fibra Óptica</strong><span>Sem rádio, sem cabo compartilhado</span></div></div>
        <div class="footer-trust-item"><i class="ph-fill ph-map-pin"></i><div><strong>100% Joinville</strong><span>Atendimento local, equipe da região</span></div></div>
        <div class="footer-trust-item"><i class="ph-fill ph-handshake"></i><div><strong>Sem fidelidade</strong><span>Cancela quando quiser, sem multa</span></div></div>
      </div>
    </div>
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a href="{base}" class="logo"><img src="{base}imgs/logo-masterinfo.png" alt="MasterInfo Internet" class="logo-img"></a>
          <p>Internet fibra óptica de verdade. Mais de 6 anos conectando famílias e empresas.</p>
          <div class="footer-social">
            <a href="https://www.instagram.com/masterinfointernet" target="_blank"><i class="ph ph-instagram-logo"></i></a>
            <a href="https://www.facebook.com/masterinfointernet" target="_blank"><i class="ph ph-facebook-logo"></i></a>
            <a href="https://wa.me/5547989212991" target="_blank"><i class="ph ph-whatsapp-logo"></i></a>
          </div>
        </div>
        <div class="footer-col">
          <h4>Internet</h4>
          <a href="{base}home-office/">Home Office</a>
          <a href="{base}gamer/">Gamer</a>
          <a href="{base}com-2-roteadores/">Com 2 Roteadores</a>
          <a href="{base}com-1-roteador/">Com 1 Roteador</a>
        </div>
        <div class="footer-col">
          <h4>Institucional</h4>
          <a href="{base}#cobertura">Cobertura</a>
          <a href="{base}#depoimentos">Depoimentos</a>
          <a href="{base}#nossa-historia">Nossa História</a>
          <a href="{base}#faq">Dúvidas</a>
        </div>
        <div class="footer-col">
          <h4>Fale com a gente</h4>
          <a href="https://wa.me/5547989212991" target="_blank"><i class="ph-fill ph-whatsapp-logo"></i> WhatsApp</a>
          <a href="mailto:masterinfo@masterinfointernet.com"><i class="ph ph-envelope"></i> E-mail</a>
          <a href="https://www.instagram.com/masterinfointernet" target="_blank"><i class="ph ph-instagram-logo"></i> Instagram</a>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 MasterInfo Internet. Todos os direitos reservados.</p>
        <div class="footer-legal">
          <a href="#">Termos de Uso</a><span>·</span>
          <a href="#">Política de Privacidade</a><span>·</span>
          <a href="#">LGPD</a>
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
  }})();
  </script>
</body>
</html>'''


# ─── TEMPLATES DAS PÁGINAS ────────────────────────────────────────────

# Imagens de fundo do hero das subpáginas Internet.
# Aceita extensões: jpg, png, webp (ordem de preferência).
IMG_BG = {
    "home-office":      "home-office",
    "gamer":            "gamer",
    "com-2-roteadores": "2-roteadores",
    "com-1-roteador":   "1-roteador",
}

def find_img(slug, base_path):
    """Encontra arquivo imgs/hero/sub/{slug}.{ext} no disco."""
    for ext in ("jpg", "jpeg", "png", "webp"):
        rel = f"imgs/hero/sub/{slug}.{ext}"
        if os.path.exists(os.path.join(base_path, rel)):
            return rel
    return None


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
        <a href="../#planos" class="sub-plan-card">
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

    img_rel = find_img(IMG_BG.get(p["slug"], ""), BASE_DIR)
    img_style = f"background-image: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.4)), url('../{img_rel}'); background-size: cover; background-position: center;" if img_rel else f"background: {p['gradient']};"

    return f'''{head(p["title"], depth)}
{header(depth)}

  <!-- HERO da subpágina (imagem de fundo) -->
  <section class="sub-hero" style="{img_style}">
    <div class="container sub-hero-inner">
      <span class="sub-hero-tag">{p["tag"]}</span>
      <h1 class="sub-hero-title">{p["title"]}</h1>
      <p class="sub-hero-subtitle">{p["subtitle"]}</p>
      <a href="../#planos" class="sub-hero-cta">{p["cta"]} <i class="ph ph-arrow-right"></i></a>
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


# ─── GERAR ARQUIVOS ───────────────────────────────────────────────────

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  + {os.path.relpath(path, BASE_DIR)}")


print("Internet (4 páginas)…")
for p in INTERNET:
    write_file(os.path.join(BASE_DIR, p["slug"], "index.html"), page_internet(p, depth=1))

print("\nAplicativos (8 páginas)…")
for a in APLICATIVOS:
    write_file(os.path.join(BASE_DIR, "aplicativos", a["slug"], "index.html"), page_app(a, depth=2))

print("\n✓ 12 subpáginas geradas.")
