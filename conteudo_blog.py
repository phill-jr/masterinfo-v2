# -*- coding: utf-8 -*-
"""Conteúdo (dados + corpo HTML) das páginas-pilar e do blog da MasterInfo.

Separado do gerar_subpaginas.py pra manter o gerador enxuto. É a FONTE ÚNICA do
texto dessas páginas: editar aqui e rodar `python gerar_subpaginas.py --content`
regenera os corpos. Os syncs cirúrgicos (header/rodapé/canonical/og/seo/schema)
continuam rodando no `--menus` padrão.

⚠️ Strings comuns (NÃO f-strings) → chaves {} literais são seguras aqui.
Links internos são ROOT-ABSOLUTE (/familia/, /checkout.html?plano=...), válidos em
produção (domínio na raiz) e no `php -S localhost:8091`.
"""

# ─── AUTORES (E-E-A-T real; NUNCA autor fake) ─────────────────────────────
AUTHORS = {
    "philipe": {
        "type": "Person", "name": "Philipe Alves Medeiros", "role": "Fundador da MasterInfo",
        "img": "/imgs/historia/fundador-philipe.jpg", "url": "/sobre/philipe/",
        "bio": "Fundador da MasterInfo Internet. Há mais de 6 anos levando fibra óptica de verdade pra Joinville, com equipe e suporte da região.",
    },
    "tatiane": {
        "type": "Person", "name": "Tatiane Lemos", "role": "Fundadora da MasterInfo",
        "img": "/imgs/historia/fundadora-tatiane.jpg", "url": "/#nossa-historia",
        "bio": "Cofundadora da MasterInfo Internet, à frente do atendimento e da experiência do cliente em Joinville.",
    },
    # Autor dos posts técnicos. Definido pelo usuário (2026-06-18): Philipe Alves
    # Medeiros (fundador). Se for outra pessoa, trocar nome/cargo/foto aqui.
    "tecnica": {
        "type": "Person", "name": "Philipe Alves Medeiros",
        "role": "Fundador da MasterInfo",
        "img": "/imgs/historia/fundador-philipe.jpg", "url": "/sobre/philipe/",
        "bio": "Fundador da MasterInfo Internet, à frente da rede de fibra óptica em Joinville há mais de 6 anos.",
    },
    "equipe": {
        "type": "Organization", "name": "Equipe MasterInfo", "role": "MasterInfo Internet",
        "img": "/imgs/logo-masterinfo.png", "url": "/#nossa-historia",
        "bio": "MasterInfo Internet: provedor de fibra óptica 100% em Joinville, há mais de 6 anos.",
    },
}

PUBLISHER = {"name": "MasterInfo Internet", "logo": "/imgs/logo-masterinfo.png"}
DATE_DEFAULT = "2026-06-18"

# ─── PÁGINAS-PILAR (landing comercial) ────────────────────────────────────
# slug → /slug/ (depth 1). hero_img = imagem de fundo (root-absolute). plans =
# ids de plano pra renderizar o grid (.sub-plan-card, sincronizado por data-mi-plans).
# body = HTML entre o hero e o bloco de planos/FAQ. faq = [(pergunta, resposta)...].

PILARES = [
    {
        "slug": "internet-joinville",
        "title": "Internet Fibra em Joinville | Planos e Cobertura",
        "desc": "Internet fibra óptica em Joinville: planos de 600 Mega a 1 Giga, Wi-Fi 6, instalação rápida e suporte local. Veja a cobertura no seu bairro.",
        "tag": "INTERNET · JOINVILLE",
        "h1": "Internet fibra em Joinville, com suporte de gente da região",
        "lead": "Fibra óptica de verdade na sua casa, do Centro ao Vila Nova, passando por Bom Retiro, América, Glória e Boa Vista. Planos de 600 Mega a 1 Giga, Wi-Fi 6 e atendimento local que resolve.",
        "hero_img": "/imgs/hero/sub/familia-1.jpg",
        "gradient": "linear-gradient(135deg, #c1121f 0%, #ff7a05 50%, #fcc305 100%)",
        "cta": "Ver planos e cobertura",
        "cta_plano": "lite-premium",
        "plans": ["lite-casa", "lite-premium", "ultra-familia"],
        "body": """
    <div class="tldr">
      <strong>Resumo rápido:</strong> a MasterInfo é um provedor de <strong>internet 100% fibra óptica em Joinville</strong>com planos a partir de 600 Mega, Wi-Fi 6 incluso e instalação rápida. O diferencial é o <strong>suporte local</strong>: equipe da região, sem call center distante. Consulte a cobertura no seu endereço e contrate em minutos.
    </div>

    <h2>Por que escolher uma internet fibra em Joinville</h2>
    <p>Joinville é a maior cidade de Santa Catarina e cresce rápido, com bairros novos e demanda cada vez maior por internet estável para trabalho remoto, estudo e streaming. A fibra óptica é, hoje, a melhor tecnologia disponível na cidade: ela leva o sinal por luz dentro de um cabo de vidro, sem a interferência e a instabilidade da internet via rádio ou dos cabos antigos.</p>
    <p>Na prática, isso significa <strong>mesma velocidade de dia e de noite</strong>navegação que não cai quando chove e latência baixa para chamadas de vídeo e jogos. Para entender as diferenças entre as tecnologias, leia <a href="/blog/fibra-vs-radio-vs-cabo/">fibra óptica vs rádio vs cabo</a>.</p>

    <h2>Planos de internet em Joinville</h2>
    <p>Nossos planos vão de 600 Mega (ideal para apartamento e casa pequena) até 1 Giga (para casa cheia, com muita gente conectada ao mesmo tempo). Todos incluem <strong>roteador Wi-Fi 6</strong> e pelo menos 1 app de TV ou streaming por mês. Veja as opções abaixo e escolha pela sua realidade:</p>

    <!--PLANS_GRID-->

    <h2>Cobertura: tem fibra no seu bairro?</h2>
    <p>Atendemos grande parte de Joinville com rede própria de fibra. A forma mais rápida de saber se já chegamos no seu endereço é <strong>consultar a cobertura pelo CEP</strong> aqui no site, em poucos segundos. Se preferir o passo a passo, leia <a href="/blog/cobertura-fibra-cep-joinville/">como saber se tem fibra no seu endereço</a>.</p>
    <p>Já atendemos regiões como Centro, América, Glória, Bom Retiro, Boa Vista, Vila Nova, Costa e Silva, Iririú e muitos outros bairros, com expansão constante para novas áreas.</p>
    <p>Páginas dedicadas por bairro: <a href="/internet-comasa-joinville/">Comasa</a><a href="/internet-boa-vista-joinville/">Boa Vista</a><a href="/internet-iririu-joinville/">Iririú</a><a href="/internet-espinheiros-joinville/">Espinheiros</a><a href="/internet-aventureiro-joinville/">Aventureiro</a><a href="/internet-itinga-joinville/">Itinga</a><a href="/internet-jardim-paraiso-joinville/">Jardim Paraíso</a><a href="/internet-jardim-sofia-joinville/">Jardim Sofia</a><a href="/internet-cubatao-joinville/">Cubatão</a><a href="/internet-nova-brasilia-joinville/">Nova Brasília</a><a href="/internet-rio-bonito-joinville/">Rio Bonito</a><a href="/internet-estrada-timbe-joinville/">Estrada Timbé</a> e <a href="/internet-paranaguamirim-joinville/">Paranaguamirim</a>.</p>

    <h2>Internet para cada necessidade</h2>
    <p>Cada casa usa a internet de um jeito. Por isso, além do plano certo, vale escolher a página que combina com o seu perfil:</p>
    <ul>
      <li><a href="/familia/">Internet para a família</a>: vários aparelhos ligados ao mesmo tempo, sem travar.</li>
      <li><a href="/home-office/">Internet para home office</a>: estabilidade para reuniões e upload rápido.</li>
      <li><a href="/gamer/">Internet para gamer</a>: baixa latência e zero perda de pacote.</li>
      <li><a href="/com-2-roteadores/">Wi-Fi em toda a casa</a>: dois roteadores em mesh, sem ponto cego.</li>
    </ul>
    <p>Não sabe quantos Mega contratar? O guia <a href="/blog/quantos-mega-de-internet-voce-precisa/">quantos Mega você precisa</a> ajuda a decidir em 2 minutos.</p>

    <h2>O diferencial: suporte local em Joinville</h2>
    <p>Tem provedor grande que atende metade do Brasil de um call center distante. A MasterInfo é diferente: somos <strong>de Joinville, para Joinville</strong>há mais de 6 anos. Quando você fala com a gente, fala com alguém da região, que conhece a cidade e resolve rápido. É o motivo de termos <strong>4,8 de 5 estrelas</strong> com milhares de avaliações no Google.</p>
""",
        "faq": [
            ("A MasterInfo é de Joinville mesmo?", "Sim. Somos um provedor local, nascido e sediado em Joinville, há mais de 6 anos. Nossa equipe técnica e o suporte são todos da região."),
            ("Quais bairros de Joinville têm cobertura?", "Atendemos boa parte da cidade com fibra própria, incluindo Centro, América, Glória, Bom Retiro, Boa Vista, Vila Nova, Costa e Silva e Iririú, entre outros. A maneira mais rápida de confirmar é consultar a cobertura pelo seu CEP aqui no site."),
            ("Qual a velocidade dos planos?", "Os planos vão de 600 Mega a 1 Giga, todos em fibra óptica com Wi-Fi 6 incluso. A escolha ideal depende de quantas pessoas e aparelhos usam a internet ao mesmo tempo."),
            ("Quanto tempo leva para instalar?", "Após a confirmação de cobertura e contratação, a instalação costuma ser agendada para os próximos dias úteis, feita pela nossa equipe técnica local."),
        ],
    },
    {
        "slug": "internet-empresarial",
        "title": "Internet Empresarial em Joinville (Link Dedicado)",
        "desc": "Internet empresarial em Joinville: link dedicado em fibra óptica, banda garantida, IP fixo, SLA e suporte local prioritário. Peça uma proposta.",
        "tag": "INTERNET · EMPRESAS",
        "h1": "Internet empresarial em Joinville, com banda garantida",
        "lead": "Link dedicado em fibra óptica para a sua empresa em Joinville: velocidade garantida em download e upload, IP fixo, SLA e suporte prioritário de uma equipe que fica na cidade.",
        "hero_img": "/imgs/hero/sub/empresarial-1.jpg",
        "gradient": "linear-gradient(135deg, #0a1f44 0%, #14366b 50%, #1f5fa8 100%)",
        "cta": "Pedir proposta empresarial",
        "cta_whatsapp": "5547989212991",
        "plans": [],
        "body": """
    <div class="tldr">
      <strong>Resumo rápido:</strong> a internet empresarial da MasterInfo é um <strong>link dedicado em fibra óptica</strong> em Joinville: a banda contratada é só sua (não dividida com vizinhos), com a <strong>mesma velocidade de download e upload</strong>IP fixo, SLA de disponibilidade e suporte prioritário local. Ideal para empresas que dependem de internet estável o tempo todo. <a href="https://wa.me/5547989212991">Peça uma proposta no WhatsApp</a>.
    </div>

    <h2>O que é internet empresarial (link dedicado)</h2>
    <p>Internet empresarial não é a mesma coisa que o plano residencial. Em um <strong>link dedicado</strong>a banda contratada é exclusiva da sua empresa: ninguém mais compartilha aquela capacidade. O resultado é uma conexão estável e previsível, com <strong>velocidade simétrica</strong> (download e upload iguais) e garantia de entrega, mesmo nos horários de pico.</p>

    <h2>Vantagens para a sua empresa</h2>
    <ul>
      <li><strong>Banda garantida:</strong> a velocidade contratada é entregue de ponta a ponta, sem cair quando o bairro inteiro está usando a internet.</li>
      <li><strong>Upload tão rápido quanto o download:</strong> essencial para backup em nuvem, videoconferência, sistemas ERP e envio de arquivos pesados.</li>
      <li><strong>IP fixo:</strong> para servidores, câmeras, VPN, ponto eletrônico e acesso remoto.</li>
      <li><strong>SLA e disponibilidade:</strong> acordo de nível de serviço com compromisso de tempo de resposta.</li>
      <li><strong>Suporte prioritário e local:</strong> quando algo acontece, você fala com a equipe da MasterInfo em Joinville, não com um call center distante.</li>
    </ul>

    <h2>Link dedicado x banda larga compartilhada</h2>
    <p>A banda larga residencial é compartilhada: ótima para casa, mas pode oscilar nos horários de maior uso. O link dedicado entrega capacidade exclusiva e garantida. Veja a diferença:</p>
    <table class="article-table">
      <thead><tr><th>Característica</th><th>Banda larga (residencial)</th><th>Link dedicado (empresarial)</th></tr></thead>
      <tbody>
        <tr><td>Banda</td><td>Compartilhada</td><td>Exclusiva e garantida</td></tr>
        <tr><td>Download x Upload</td><td>Assimétrico</td><td>Simétrico (iguais)</td></tr>
        <tr><td>IP fixo</td><td>Geralmente não</td><td>Sim</td></tr>
        <tr><td>SLA</td><td>Não</td><td>Sim</td></tr>
        <tr><td>Prioridade no suporte</td><td>Padrão</td><td>Prioritária</td></tr>
      </tbody>
    </table>

    <h2>Para quais empresas é indicado</h2>
    <p>O link dedicado faz diferença em escritórios, clínicas e consultórios, comércios com muitos pagamentos e sistemas online, indústrias, contabilidades, e qualquer empresa que use sistemas em nuvem, videoconferência constante, câmeras de segurança ou atendimento que não pode parar.</p>

    <h2>Como contratar a internet empresarial da MasterInfo</h2>
    <p>Cada empresa tem uma necessidade diferente de banda e estrutura, por isso o plano empresarial é montado sob medida. Fale com nosso time comercial pelo <a href="https://wa.me/5547989212991">WhatsApp (47) 98921-2991</a> ou pela página de <a href="/contato/">contato</a> e receba uma proposta para o seu endereço em Joinville.</p>
""",
        "faq": [
            ("Qual a diferença entre link dedicado e internet residencial?", "No link dedicado a banda é exclusiva da sua empresa e garantida, com velocidade simétrica (download e upload iguais), IP fixo e SLA. A internet residencial é compartilhada e assimétrica, ótima para casa mas sem garantia de banda nos horários de pico."),
            ("A internet empresarial tem IP fixo?", "Sim. O link dedicado empresarial inclui IP fixo, necessário para servidores, VPN, câmeras, ponto eletrônico e acesso remoto."),
            ("Vocês atendem empresas em toda Joinville?", "Atendemos a maior parte de Joinville com fibra própria e avaliamos a viabilidade técnica para o endereço da sua empresa. Fale com o comercial para confirmar a cobertura."),
            ("Como peço uma proposta?", "Pelo WhatsApp comercial (47) 98921-2991 ou pela página de contato. Montamos uma proposta sob medida conforme a banda e a estrutura que a sua empresa precisa."),
        ],
    },
    {
        "slug": "melhor-internet-joinville",
        "title": "Qual a Melhor Internet de Joinville? Critérios para Escolher",
        "desc": "Como escolher a melhor internet de Joinville: estabilidade, fibra dedicada, suporte local e avaliações reais. Veja os critérios e os planos da MasterInfo.",
        "tag": "GUIA · MELHOR INTERNET",
        "h1": "Qual a melhor internet de Joinville? Os critérios que importam",
        "lead": "Não existe uma resposta única, mas existem critérios objetivos para escolher bem: tecnologia, estabilidade real, suporte local e reputação. Veja como avaliar e onde a MasterInfo se encaixa.",
        "hero_img": "/imgs/hero/sub/home-office-2.jpg",
        "gradient": "linear-gradient(135deg, #c1121f 0%, #ff7a05 50%, #fcc305 100%)",
        "cta": "Ver planos da MasterInfo",
        "cta_plano": "ultra-familia",
        "plans": ["lite-premium", "ultra-familia", "ultra-home-office"],
        "body": """
    <div class="tldr">
      <strong>Resumo rápido:</strong> a melhor internet de Joinville é a que combina <strong>fibra óptica</strong><strong>estabilidade real</strong> (não só velocidade no papel), <strong>suporte local que resolve</strong> e <strong>boa reputação</strong>. Provedores regionais costumam ganhar no atendimento. A MasterInfo atende esses critérios com 4,8/5 no Google e equipe 100% de Joinville.
    </div>

    <p class="article-note">Transparência: a MasterInfo é um provedor de Joinville, então esta página tem o nosso ponto de vista. Em vez de um ranking "neutro" de concorrentes, listamos os <strong>critérios objetivos</strong> que você deve usar para decidir, seja qual for o provedor.</p>

    <h2>1. Tecnologia: fibra óptica até a sua casa</h2>
    <p>O primeiro filtro é a tecnologia. Fibra óptica (FTTH, fibra até a casa) é mais estável e rápida que internet via rádio ou cabo antigo, e não sofre com chuva ou interferência. Se o provedor não leva fibra até o seu imóvel, dificilmente será a melhor opção. Entenda melhor em <a href="/blog/fibra-vs-radio-vs-cabo/">fibra vs rádio vs cabo</a>.</p>

    <h2>2. Estabilidade real, não só velocidade no papel</h2>
    <p>Velocidade alta no contrato não significa nada se a conexão cai à noite ou trava quando todo mundo está usando. O que importa é a <strong>estabilidade no dia a dia</strong>: a mesma velocidade de manhã e às 21h, latência baixa para chamadas e jogos, e zero quedas. Pergunte a vizinhos e olhe avaliações que falem de estabilidade, não só de preço.</p>

    <h2>3. Suporte local que resolve</h2>
    <p>Esse é o critério que mais separa um bom provedor de um provedor qualquer. Quando a internet cai, você quer falar com alguém que entende e resolve, não esperar horas num call center. Provedores regionais como a MasterInfo têm <strong>equipe na cidade</strong>técnicos que conhecem os bairros e tempo de resposta menor.</p>

    <h2>4. Reputação e avaliações reais</h2>
    <p>Avaliações no Google e indicações de quem já é cliente valem mais que qualquer propaganda. A MasterInfo tem <strong>4,8 de 5 estrelas</strong> com milhares de avaliações, reflexo de mais de 6 anos conectando famílias e empresas em Joinville.</p>

    <h2>5. Preço justo e sem letra miúda</h2>
    <p>O mais barato nem sempre é o melhor, e o mais caro também não. Procure um plano com <strong>preço claro</strong>sem surpresas na fatura, com o que está incluso bem explicado (roteador, apps, suporte). Veja os planos da MasterInfo abaixo, com preço transparente e desconto por pagamento em dia.</p>

    <!--PLANS_GRID-->

    <h2>Cobertura por bairro: onde a MasterInfo tem fibra em Joinville</h2>
    <p>A "melhor internet" também depende do <strong>bairro</strong>: o que vale é ter fibra óptica (FTTH) chegando até o seu endereço. A MasterInfo tem <strong>rede própria de fibra em 13 bairros de Joinville</strong> e amplia a cobertura toda semana. Bairros atendidos hoje:</p>
    <ul>
      <li><strong>Comasa</strong>bairro-sede da MasterInfo</li>
      <li><strong>Boa Vista</strong></li>
      <li><strong>Espinheiros</strong></li>
      <li><strong>Aventureiro</strong></li>
      <li><strong>Jardim Paraíso</strong></li>
      <li><strong>Jardim Sofia</strong></li>
      <li><strong>Cubatão</strong></li>
      <li><strong>Itinga</strong></li>
      <li><strong>Nova Brasília</strong></li>
      <li><strong>Rio Bonito</strong></li>
      <li><strong>Estrada Timbé</strong></li>
      <li><strong>Paranaguamirim</strong></li>
      <li><strong>Iririú</strong></li>
    </ul>
    <p>Não achou seu bairro na lista? A rede cresce toda semana, <a href="/#cobertura">consulte a cobertura pelo seu CEP</a> e confirme a disponibilidade no seu endereço em segundos. Veja também o <a href="/internet-joinville/">guia de internet em Joinville</a> por perfil de uso.</p>

    <h2>Como aplicar tudo isso na prática</h2>
    <p>Resumindo: priorize fibra óptica, confirme a estabilidade com quem mora perto, valorize o suporte local e cheque as avaliações. Se quiser ir direto ao ponto, veja o <a href="/internet-joinville/">guia de internet em Joinville</a> ou descubra <a href="/blog/quantos-mega-de-internet-voce-precisa/">quantos Mega você precisa</a>.</p>

    <h2>Internet fibra por bairro em Joinville</h2>
    <p>Veja a página do seu bairro: <a href="/internet-comasa-joinville/">Comasa</a><a href="/internet-boa-vista-joinville/">Boa Vista</a><a href="/internet-iririu-joinville/">Iririú</a><a href="/internet-espinheiros-joinville/">Espinheiros</a><a href="/internet-aventureiro-joinville/">Aventureiro</a><a href="/internet-itinga-joinville/">Itinga</a><a href="/internet-jardim-paraiso-joinville/">Jardim Paraíso</a><a href="/internet-jardim-sofia-joinville/">Jardim Sofia</a><a href="/internet-cubatao-joinville/">Cubatão</a><a href="/internet-nova-brasilia-joinville/">Nova Brasília</a><a href="/internet-rio-bonito-joinville/">Rio Bonito</a><a href="/internet-estrada-timbe-joinville/">Estrada Timbé</a> e <a href="/internet-paranaguamirim-joinville/">Paranaguamirim</a>.</p>

    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": ["InternetServiceProvider", "LocalBusiness"],
      "@id": "https://masterinfointernet.com/#provedor",
      "name": "MasterInfo Internet",
      "url": "https://masterinfointernet.com/",
      "telephone": "+554734341734",
      "image": "https://masterinfointernet.com/og-image.jpg",
      "address": { "@type": "PostalAddress", "streetAddress": "Rua Prefeito Baltazar Buschle, 628", "addressLocality": "Joinville", "addressRegion": "SC", "postalCode": "89228-000", "addressCountry": "BR" },
      "geo": { "@type": "GeoCoordinates", "latitude": -26.2798, "longitude": -48.8016 },
      "areaServed": [
        { "@type": "City", "name": "Joinville" },
        { "@type": "Place", "name": "Comasa, Joinville" },
        { "@type": "Place", "name": "Boa Vista, Joinville" },
        { "@type": "Place", "name": "Espinheiros, Joinville" },
        { "@type": "Place", "name": "Aventureiro, Joinville" },
        { "@type": "Place", "name": "Jardim Paraíso, Joinville" },
        { "@type": "Place", "name": "Jardim Sofia, Joinville" },
        { "@type": "Place", "name": "Cubatão, Joinville" },
        { "@type": "Place", "name": "Itinga, Joinville" },
        { "@type": "Place", "name": "Nova Brasília, Joinville" },
        { "@type": "Place", "name": "Rio Bonito, Joinville" },
        { "@type": "Place", "name": "Estrada Timbé, Joinville" },
        { "@type": "Place", "name": "Paranaguamirim, Joinville" },
        { "@type": "Place", "name": "Iririú, Joinville" }
      ]
    }
    </script>
""",
        "faq": [
            ("Qual é a melhor internet de Joinville?", "Não há uma resposta única para todos, mas a melhor internet é a que reúne fibra óptica até a sua casa, estabilidade real no dia a dia, suporte local que resolve e boa reputação. A MasterInfo atende esses critérios com nota 4,8/5 no Google e equipe 100% de Joinville."),
            ("Provedor local é melhor que operadora grande?", "Em atendimento, quase sempre sim. Provedores regionais têm equipe na cidade, conhecem os bairros e respondem mais rápido. Em fibra óptica, a qualidade do sinal de um bom provedor local costuma igualar ou superar a das grandes."),
            ("Como confirmar a estabilidade antes de contratar?", "Pergunte a vizinhos que já usam o provedor, leia avaliações que falem de quedas e velocidade à noite (não só de preço) e confirme se a tecnologia é fibra óptica até o imóvel."),
            ("A MasterInfo atende meu bairro?", "A MasterInfo atende 13 bairros de Joinville com fibra óptica própria: Comasa, Boa Vista, Espinheiros, Aventureiro, Jardim Paraíso, Jardim Sofia, Cubatão, Itinga, Nova Brasília, Rio Bonito, Estrada Timbé, Paranaguamirim e Iririú, e a cobertura cresce toda semana. Consulte pelo seu CEP aqui no site para confirmar em segundos."),
        ],
    },
    {
        "slug": "internet-comasa-joinville",
        "title": "Internet Fibra no Comasa, Joinville | MasterInfo",
        "desc": "Internet fibra óptica no Comasa (Joinville): provedor com sede no próprio bairro, planos de 600 Mega a 1 Giga, Wi-Fi 6 e instalação rápida. Veja a cobertura pelo seu CEP.",
        "tag": "INTERNET · COMASA",
        "h1": "Internet fibra no Comasa: o provedor que fica no seu bairro",
        "lead": "A MasterInfo tem sede no Comasa, em Joinville, fibra óptica de verdade (FTTH) até a sua casa, Wi-Fi 6 e suporte de gente da região. Consulte a cobertura no seu endereço e contrate em minutos.",
        "hero_img": "/imgs/hero/sub/familia-1.jpg",
        "gradient": "linear-gradient(135deg, #c1121f 0%, #ff7a05 50%, #fcc305 100%)",
        "cta": "Ver planos e cobertura",
        "cta_plano": "lite-premium",
        "plans": ["lite-casa", "lite-premium", "ultra-familia"],
        "body": """
    <div class="tldr">
      <strong>Resumo rápido:</strong> a MasterInfo é um provedor de <strong>internet 100% fibra óptica</strong> com <strong>sede no próprio Comasa</strong>em Joinville (Rua Prefeito Baltazar Buschle, 628). Planos de 600 Mega a 1 Giga, Wi-Fi 6 incluso e suporte local de verdade. Consulte a cobertura no seu endereço e contrate em minutos.
    </div>

    <h2>Internet fibra no Comasa, em Joinville</h2>
    <p>O Comasa é um dos bairros que a MasterInfo conhece melhor, afinal, é onde fica a nossa sede. Isso significa <strong>fibra óptica até a sua casa (FTTH)</strong>com sinal estável de dia e de noite, sem a instabilidade do rádio ou dos cabos antigos. Para entender as diferenças entre as tecnologias, leia <a href="/blog/fibra-vs-radio-vs-cabo/">fibra óptica vs rádio vs cabo</a>.</p>
    <p>Por estarmos no bairro, o atendimento é próximo e rápido: quando precisar, você fala com quem é da região e conhece o Comasa de perto.</p>

    <h2>Planos de internet para o Comasa</h2>
    <p>Os planos vão de 600 Mega (ideal para apartamento e casa pequena) até 1 Giga (para casa cheia, com muita gente conectada ao mesmo tempo). Todos incluem <strong>roteador Wi-Fi 6</strong> e pelo menos 1 app de TV ou streaming por mês:</p>

    <!--PLANS_GRID-->

    <h2>Cobertura de fibra no Comasa</h2>
    <p>Atendemos o Comasa com rede própria de fibra óptica. Como a expansão é constante e a disponibilidade varia de rua para rua, a forma mais rápida e segura de confirmar se já chegamos no seu endereço é <strong>consultar a cobertura pelo CEP</strong> aqui no site, em poucos segundos. Se preferir o passo a passo, veja <a href="/blog/cobertura-fibra-cep-joinville/">como saber se tem fibra no seu endereço</a>.</p>

    <div style="margin:24px 0;border-radius:14px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.12);line-height:0;">
      <iframe src="https://www.google.com/maps?q=Comasa%2C%20Joinville%20-%20SC&output=embed" width="100%" height="360" style="border:0;display:block;" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa do bairro Comasa, em Joinville, área de cobertura da MasterInfo"></iframe>
    </div>

    <h2>Internet para cada necessidade</h2>
    <p>Cada casa usa a internet de um jeito. Além do plano certo, vale escolher a página que combina com o seu perfil:</p>
    <ul>
      <li><a href="/familia/">Internet para a família</a>: vários aparelhos ligados ao mesmo tempo, sem travar.</li>
      <li><a href="/home-office/">Internet para home office</a>: estabilidade para reuniões e upload rápido.</li>
      <li><a href="/gamer/">Internet para gamer</a>: baixa latência e zero perda de pacote.</li>
      <li><a href="/com-2-roteadores/">Wi-Fi em toda a casa</a>: dois roteadores em mesh, sem ponto cego.</li>
    </ul>
    <p>Quer ver a cidade toda? Veja também <a href="/internet-joinville/">internet fibra em Joinville</a>.</p>

    <h2>O diferencial: um provedor que é do Comasa</h2>
    <p>Tem provedor grande que atende metade do Brasil de um call center distante. A MasterInfo é diferente: somos <strong>de Joinville, com sede no Comasa</strong>há mais de 6 anos. Quando você fala com a gente, fala com alguém da região, que resolve rápido. É o motivo de termos <strong>4,8 de 5 estrelas</strong> com milhares de avaliações no Google.</p>
""",
        "faq": [
            ("A MasterInfo atende o Comasa?", "Sim. Nossa sede fica no próprio Comasa (Rua Prefeito Baltazar Buschle, 628) e atendemos o bairro com fibra óptica até a sua casa (FTTH). Como a cobertura varia de rua para rua, confirme no seu endereço pelo CEP aqui no site."),
            ("Quais as velocidades dos planos no Comasa?", "Os planos vão de 600 Mega a 1 Giga, todos em fibra óptica com Wi-Fi 6 incluso. A escolha ideal depende de quantas pessoas e aparelhos usam a internet ao mesmo tempo."),
            ("Quanto tempo leva para instalar no Comasa?", "Após confirmar a cobertura e contratar, a instalação costuma ser agendada para os próximos dias úteis, feita pela nossa equipe técnica local."),
            ("Por que escolher um provedor com sede no bairro?", "Porque o suporte é de quem é da região e está por perto: atendimento mais rápido, sem call center distante. Por isso temos 4,8 de 5 estrelas no Google."),
        ],
    },
    {
        "slug": "internet-boa-vista-joinville",
        "title": "Internet Fibra na Boa Vista, Joinville | MasterInfo",
        "desc": "Internet fibra óptica na Boa Vista (Joinville): planos de 600 Mega a 1 Giga, Wi-Fi 6, instalação rápida e suporte local. Veja a cobertura pelo seu CEP.",
        "tag": "INTERNET · BOA VISTA",
        "h1": "Internet fibra na Boa Vista, em Joinville",
        "lead": "Fibra óptica de verdade (FTTH) na Boa Vista, um dos bairros mais movimentados de Joinville. Wi-Fi 6, instalação rápida e suporte de gente da região. Consulte a cobertura no seu endereço e contrate em minutos.",
        "hero_img": "/imgs/hero/sub/familia-1.jpg",
        "gradient": "linear-gradient(135deg, #c1121f 0%, #ff7a05 50%, #fcc305 100%)",
        "cta": "Ver planos e cobertura",
        "cta_plano": "lite-premium",
        "plans": ["lite-casa", "lite-premium", "ultra-familia"],
        "body": """
    <div class="tldr">
      <strong>Resumo rápido:</strong> a MasterInfo leva <strong>internet 100% fibra óptica (FTTH)</strong> para a Boa Vista, em Joinville, com planos de 600 Mega a 1 Giga, Wi-Fi 6 incluso e suporte local de verdade. Consulte a cobertura no seu endereço e contrate em minutos.
    </div>

    <h2>Internet fibra na Boa Vista, em Joinville</h2>
    <p>A Boa Vista é um dos bairros mais populosos e movimentados de Joinville, muita gente, muitos dispositivos e uso intenso o dia todo. Para isso, a <strong>fibra óptica até a sua casa (FTTH)</strong> é a melhor opção: sinal estável de dia e de noite, sem a instabilidade do rádio ou dos cabos antigos. Entenda as diferenças em <a href="/blog/fibra-vs-radio-vs-cabo/">fibra óptica vs rádio vs cabo</a>.</p>

    <h2>Planos de internet para a Boa Vista</h2>
    <p>Os planos vão de 600 Mega (casa pequena) até 1 Giga (casa cheia, com muita gente conectada ao mesmo tempo). Todos incluem <strong>roteador Wi-Fi 6</strong> e pelo menos 1 app de TV ou streaming por mês:</p>

    <!--PLANS_GRID-->

    <h2>Cobertura de fibra na Boa Vista</h2>
    <p>Atendemos a Boa Vista com rede própria de fibra óptica. Como a disponibilidade varia de rua para rua, a forma mais rápida de confirmar se já chegamos no seu endereço é <strong>consultar a cobertura pelo CEP</strong> aqui no site. Se preferir, veja <a href="/blog/cobertura-fibra-cep-joinville/">como saber se tem fibra no seu endereço</a>.</p>

    <div style="margin:24px 0;border-radius:14px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.12);line-height:0;">
      <iframe src="https://www.google.com/maps?q=Boa%20Vista%2C%20Joinville%20-%20SC&output=embed" width="100%" height="360" style="border:0;display:block;" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa do bairro Boa Vista, em Joinville, área de cobertura da MasterInfo"></iframe>
    </div>

    <h2>Internet para cada necessidade</h2>
    <p>Cada casa usa a internet de um jeito. Escolha a página que combina com o seu perfil:</p>
    <ul>
      <li><a href="/familia/">Internet para a família</a>: vários aparelhos ao mesmo tempo, sem travar.</li>
      <li><a href="/home-office/">Internet para home office</a>: estabilidade para reuniões e upload rápido.</li>
      <li><a href="/gamer/">Internet para gamer</a>: baixa latência e zero perda de pacote.</li>
      <li><a href="/com-2-roteadores/">Wi-Fi em toda a casa</a>: dois roteadores em mesh, sem ponto cego.</li>
    </ul>
    <p>Veja também <a href="/internet-joinville/">internet fibra em Joinville</a>.</p>

    <h2>O diferencial: suporte local</h2>
    <p>Somos <strong>de Joinville, para Joinville</strong>há mais de 6 anos. Quando você fala com a gente, fala com alguém da região, que resolve rápido, por isso temos <strong>4,8 de 5 estrelas</strong> com milhares de avaliações no Google.</p>
""",
        "faq": [
            ("A MasterInfo atende a Boa Vista?", "Sim. A Boa Vista está na nossa área de cobertura de fibra óptica em Joinville. Como a disponibilidade varia de rua para rua, confirme no seu endereço pelo CEP aqui no site."),
            ("Quais as velocidades dos planos na Boa Vista?", "Os planos vão de 600 Mega a 1 Giga, todos em fibra óptica com Wi-Fi 6 incluso. A escolha ideal depende de quantas pessoas e aparelhos usam a internet ao mesmo tempo."),
            ("Quanto tempo leva para instalar na Boa Vista?", "Após confirmar a cobertura e contratar, a instalação costuma ser agendada para os próximos dias úteis, feita pela nossa equipe técnica local."),
            ("A internet aguenta uma casa com muita gente usando?", "Sim. Os planos de 1 Giga com Mesh Wi-Fi 6 foram pensados justamente para casas cheias, com vários aparelhos conectados ao mesmo tempo sem travar."),
        ],
    },
    {
        "slug": "internet-iririu-joinville",
        "title": "Internet Fibra no Iririú, Joinville | MasterInfo",
        "desc": "Internet fibra óptica no Iririú (Joinville): planos de 600 Mega a 1 Giga, Wi-Fi 6, instalação rápida e suporte local. Veja a cobertura pelo seu CEP.",
        "tag": "INTERNET · IRIRIÚ",
        "h1": "Internet fibra no Iririú, em Joinville",
        "lead": "Fibra óptica de verdade (FTTH) no Iririú, um grande bairro residencial de Joinville. Wi-Fi 6 para a casa toda, instalação rápida e suporte de gente da região. Consulte a cobertura no seu endereço.",
        "hero_img": "/imgs/hero/sub/familia-1.jpg",
        "gradient": "linear-gradient(135deg, #c1121f 0%, #ff7a05 50%, #fcc305 100%)",
        "cta": "Ver planos e cobertura",
        "cta_plano": "lite-premium",
        "plans": ["lite-casa", "lite-premium", "ultra-familia"],
        "body": """
    <div class="tldr">
      <strong>Resumo rápido:</strong> a MasterInfo leva <strong>internet 100% fibra óptica (FTTH)</strong> para o Iririú, em Joinville, com planos de 600 Mega a 1 Giga, Wi-Fi 6 incluso e suporte local de verdade. Consulte a cobertura no seu endereço e contrate em minutos.
    </div>

    <h2>Internet fibra no Iririú, em Joinville</h2>
    <p>O Iririú é um grande bairro residencial de Joinville, de famílias e casas, perfil em que a internet precisa cobrir bem todos os cômodos e aguentar vários aparelhos ao mesmo tempo. A <strong>fibra óptica até a casa (FTTH)</strong> entrega isso com sinal estável e Wi-Fi forte. Veja as diferenças em <a href="/blog/fibra-vs-radio-vs-cabo/">fibra óptica vs rádio vs cabo</a>.</p>

    <h2>Planos de internet para o Iririú</h2>
    <p>Os planos vão de 600 Mega (casa pequena) até 1 Giga (casa cheia). Todos incluem <strong>roteador Wi-Fi 6</strong> e pelo menos 1 app de TV ou streaming por mês:</p>

    <!--PLANS_GRID-->

    <h2>Cobertura de fibra no Iririú</h2>
    <p>Atendemos o Iririú com rede própria de fibra óptica. Como a disponibilidade varia de rua para rua, a forma mais rápida de confirmar se já chegamos no seu endereço é <strong>consultar a cobertura pelo CEP</strong> aqui no site. Se preferir, veja <a href="/blog/cobertura-fibra-cep-joinville/">como saber se tem fibra no seu endereço</a>.</p>

    <div style="margin:24px 0;border-radius:14px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.12);line-height:0;">
      <iframe src="https://www.google.com/maps?q=Iririu%2C%20Joinville%20-%20SC&output=embed" width="100%" height="360" style="border:0;display:block;" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa do bairro Iririú, em Joinville, área de cobertura da MasterInfo"></iframe>
    </div>

    <h2>Internet para cada necessidade</h2>
    <p>Cada casa usa a internet de um jeito. Escolha a página que combina com o seu perfil:</p>
    <ul>
      <li><a href="/familia/">Internet para a família</a>: vários aparelhos ao mesmo tempo, sem travar.</li>
      <li><a href="/home-office/">Internet para home office</a>: estabilidade para reuniões e upload rápido.</li>
      <li><a href="/gamer/">Internet para gamer</a>: baixa latência e zero perda de pacote.</li>
      <li><a href="/com-2-roteadores/">Wi-Fi em toda a casa</a>: dois roteadores em mesh, sem ponto cego.</li>
    </ul>
    <p>Veja também <a href="/internet-joinville/">internet fibra em Joinville</a>.</p>

    <h2>O diferencial: suporte local</h2>
    <p>Somos <strong>de Joinville, para Joinville</strong>há mais de 6 anos. Quando você fala com a gente, fala com alguém da região, que resolve rápido, por isso temos <strong>4,8 de 5 estrelas</strong> com milhares de avaliações no Google.</p>
""",
        "faq": [
            ("A MasterInfo atende o Iririú?", "Sim. O Iririú está na nossa área de cobertura de fibra óptica em Joinville. Como a disponibilidade varia de rua para rua, confirme no seu endereço pelo CEP aqui no site."),
            ("Quais as velocidades dos planos no Iririú?", "Os planos vão de 600 Mega a 1 Giga, todos em fibra óptica com Wi-Fi 6 incluso. A escolha ideal depende de quantas pessoas e aparelhos usam a internet ao mesmo tempo."),
            ("Quanto tempo leva para instalar no Iririú?", "Após confirmar a cobertura e contratar, a instalação costuma ser agendada para os próximos dias úteis, feita pela nossa equipe técnica local."),
            ("O Wi-Fi cobre a casa toda no Iririú?", "Sim. Os planos com Mesh Wi-Fi 6 usam dois roteadores em rede mesh para cobrir todos os cômodos, sem ponto cego, ideal para casas maiores."),
        ],
    },
    {
        "slug": "internet-espinheiros-joinville",
        "title": "Internet Fibra no Espinheiros, Joinville | MasterInfo",
        "desc": "Internet fibra óptica no Espinheiros (Joinville): planos de 600 Mega a 1 Giga, Wi-Fi 6, instalação rápida e suporte local. Veja a cobertura pelo seu CEP.",
        "tag": "INTERNET · ESPINHEIROS",
        "h1": "Internet fibra no Espinheiros, em Joinville",
        "lead": "Fibra óptica de verdade (FTTH) no Espinheiros, na região norte de Joinville, Wi-Fi 6, instalação rápida e suporte de gente da região. Consulte a cobertura no seu endereço e contrate em minutos.",
        "hero_img": "/imgs/hero/sub/familia-1.jpg",
        "gradient": "linear-gradient(135deg, #c1121f 0%, #ff7a05 50%, #fcc305 100%)",
        "cta": "Ver planos e cobertura",
        "cta_plano": "lite-premium",
        "plans": ["lite-casa", "lite-premium", "ultra-familia"],
        "body": """
    <div class="tldr">
      <strong>Resumo rápido:</strong> a MasterInfo leva <strong>internet 100% fibra óptica (FTTH)</strong> para o Espinheiros, na região norte de Joinville, vizinho do Comasa, onde fica a nossa sede. Planos de 600 Mega a 1 Giga, Wi-Fi 6 e suporte local. Consulte a cobertura no seu endereço.
    </div>

    <h2>Internet fibra no Espinheiros, em Joinville</h2>
    <p>O Espinheiros fica na região norte de Joinville, ao lado do Comasa, bairro que a MasterInfo conhece de perto, já que é onde fica a nossa sede. Com <strong>fibra óptica até a sua casa (FTTH)</strong>você tem sinal estável de dia e de noite, sem a instabilidade do rádio ou dos cabos antigos. Veja as diferenças em <a href="/blog/fibra-vs-radio-vs-cabo/">fibra óptica vs rádio vs cabo</a>.</p>

    <h2>Planos de internet para o Espinheiros</h2>
    <p>Os planos vão de 600 Mega (casa pequena) até 1 Giga (casa cheia). Todos incluem <strong>roteador Wi-Fi 6</strong> e pelo menos 1 app de TV ou streaming por mês:</p>

    <!--PLANS_GRID-->

    <h2>Cobertura de fibra no Espinheiros</h2>
    <p>Atendemos o Espinheiros com rede própria de fibra óptica. Como a disponibilidade varia de rua para rua, confirme se já chegamos no seu endereço <strong>consultando a cobertura pelo CEP</strong> aqui no site. Veja também <a href="/blog/cobertura-fibra-cep-joinville/">como saber se tem fibra no seu endereço</a>.</p>

    <div style="margin:24px 0;border-radius:14px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.12);line-height:0;">
      <iframe src="https://www.google.com/maps?q=Espinheiros%2C%20Joinville%20-%20SC&output=embed" width="100%" height="360" style="border:0;display:block;" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa do bairro Espinheiros, em Joinville, área de cobertura da MasterInfo"></iframe>
    </div>

    <h2>Internet para cada necessidade</h2>
    <p>Escolha a página que combina com o seu perfil: <a href="/familia/">família</a><a href="/home-office/">home office</a><a href="/gamer/">gamer</a> ou <a href="/com-2-roteadores/">Wi-Fi em toda a casa</a>. Veja também <a href="/internet-joinville/">internet fibra em Joinville</a>.</p>

    <h2>O diferencial: suporte local</h2>
    <p>Somos <strong>de Joinville, para Joinville</strong>há mais de 6 anos, com sede no Comasa, bem ao lado do Espinheiros. Atendimento próximo, de quem é da região, com <strong>4,8 de 5 estrelas</strong> no Google.</p>
""",
        "faq": [
            ("A MasterInfo atende o Espinheiros?", "Sim. O Espinheiros está na nossa área de cobertura de fibra óptica em Joinville e fica ao lado do Comasa, onde fica a nossa sede. Como a disponibilidade varia de rua para rua, confirme no seu endereço pelo CEP."),
            ("Quais as velocidades dos planos no Espinheiros?", "Os planos vão de 600 Mega a 1 Giga, todos em fibra óptica com Wi-Fi 6 incluso. A escolha ideal depende de quantas pessoas e aparelhos usam a internet ao mesmo tempo."),
            ("Quanto tempo leva para instalar no Espinheiros?", "Após confirmar a cobertura e contratar, a instalação costuma ser agendada para os próximos dias úteis, feita pela nossa equipe técnica local."),
        ],
    },
    {
        "slug": "internet-aventureiro-joinville",
        "title": "Internet Fibra no Aventureiro, Joinville | MasterInfo",
        "desc": "Internet fibra óptica no Aventureiro (Joinville): planos de 600 Mega a 1 Giga, Wi-Fi 6, instalação rápida e suporte local. Veja a cobertura pelo seu CEP.",
        "tag": "INTERNET · AVENTUREIRO",
        "h1": "Internet fibra no Aventureiro, em Joinville",
        "lead": "Fibra óptica de verdade (FTTH) no Aventureiro, um dos bairros mais populosos de Joinville, Wi-Fi 6, instalação rápida e suporte de gente da região. Consulte a cobertura no seu endereço.",
        "hero_img": "/imgs/hero/sub/familia-1.jpg",
        "gradient": "linear-gradient(135deg, #c1121f 0%, #ff7a05 50%, #fcc305 100%)",
        "cta": "Ver planos e cobertura",
        "cta_plano": "lite-premium",
        "plans": ["lite-casa", "lite-premium", "ultra-familia"],
        "body": """
    <div class="tldr">
      <strong>Resumo rápido:</strong> a MasterInfo leva <strong>internet 100% fibra óptica (FTTH)</strong> para o Aventureiro, um dos bairros mais populosos de Joinville. Planos de 600 Mega a 1 Giga, Wi-Fi 6 e suporte local. Consulte a cobertura no seu endereço.
    </div>

    <h2>Internet fibra no Aventureiro, em Joinville</h2>
    <p>O Aventureiro é um dos bairros mais populosos de Joinville, muita gente e muitos aparelhos conectados ao mesmo tempo. A <strong>fibra óptica até a casa (FTTH)</strong> dá conta desse uso intenso, com sinal estável e Wi-Fi forte. Entenda as diferenças em <a href="/blog/fibra-vs-radio-vs-cabo/">fibra óptica vs rádio vs cabo</a>.</p>

    <h2>Planos de internet para o Aventureiro</h2>
    <p>Os planos vão de 600 Mega (casa pequena) até 1 Giga (casa cheia). Todos incluem <strong>roteador Wi-Fi 6</strong> e pelo menos 1 app de TV ou streaming por mês:</p>

    <!--PLANS_GRID-->

    <h2>Cobertura de fibra no Aventureiro</h2>
    <p>Atendemos o Aventureiro com rede própria de fibra óptica. Como a disponibilidade varia de rua para rua, confirme se já chegamos no seu endereço <strong>consultando a cobertura pelo CEP</strong> aqui no site. Veja também <a href="/blog/cobertura-fibra-cep-joinville/">como saber se tem fibra no seu endereço</a>.</p>

    <div style="margin:24px 0;border-radius:14px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.12);line-height:0;">
      <iframe src="https://www.google.com/maps?q=Aventureiro%2C%20Joinville%20-%20SC&output=embed" width="100%" height="360" style="border:0;display:block;" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa do bairro Aventureiro, em Joinville, área de cobertura da MasterInfo"></iframe>
    </div>

    <h2>Internet para cada necessidade</h2>
    <p>Escolha a página que combina com o seu perfil: <a href="/familia/">família</a><a href="/home-office/">home office</a><a href="/gamer/">gamer</a> ou <a href="/com-2-roteadores/">Wi-Fi em toda a casa</a>. Veja também <a href="/internet-joinville/">internet fibra em Joinville</a>.</p>

    <h2>O diferencial: suporte local</h2>
    <p>Somos <strong>de Joinville, para Joinville</strong>há mais de 6 anos. Atendimento próximo, de quem é da região, com <strong>4,8 de 5 estrelas</strong> e milhares de avaliações no Google.</p>
""",
        "faq": [
            ("A MasterInfo atende o Aventureiro?", "Sim. O Aventureiro está na nossa área de cobertura de fibra óptica em Joinville. Como a disponibilidade varia de rua para rua, confirme no seu endereço pelo CEP aqui no site."),
            ("Quais as velocidades dos planos no Aventureiro?", "Os planos vão de 600 Mega a 1 Giga, todos em fibra óptica com Wi-Fi 6 incluso. A escolha ideal depende de quantas pessoas e aparelhos usam a internet ao mesmo tempo."),
            ("A internet aguenta uma casa com muita gente usando?", "Sim. Os planos de 1 Giga com Mesh Wi-Fi 6 foram pensados para casas cheias, com vários aparelhos conectados ao mesmo tempo sem travar."),
        ],
    },
    {
        "slug": "internet-itinga-joinville",
        "title": "Internet Fibra na Itinga, Joinville | MasterInfo",
        "desc": "Internet fibra óptica na Itinga (Joinville): planos de 600 Mega a 1 Giga, Wi-Fi 6, instalação rápida e suporte local. Veja a cobertura pelo seu CEP.",
        "tag": "INTERNET · ITINGA",
        "h1": "Internet fibra na Itinga, em Joinville",
        "lead": "Fibra óptica de verdade (FTTH) na Itinga, um grande bairro da região sul de Joinville, Wi-Fi 6 para a casa toda, instalação rápida e suporte de gente da região. Consulte a cobertura no seu endereço.",
        "hero_img": "/imgs/hero/sub/familia-1.jpg",
        "gradient": "linear-gradient(135deg, #c1121f 0%, #ff7a05 50%, #fcc305 100%)",
        "cta": "Ver planos e cobertura",
        "cta_plano": "lite-premium",
        "plans": ["lite-casa", "lite-premium", "ultra-familia"],
        "body": """
    <div class="tldr">
      <strong>Resumo rápido:</strong> a MasterInfo leva <strong>internet 100% fibra óptica (FTTH)</strong> para a Itinga, um grande bairro da região sul de Joinville. Planos de 600 Mega a 1 Giga, Wi-Fi 6 e suporte local. Consulte a cobertura no seu endereço.
    </div>

    <h2>Internet fibra na Itinga, em Joinville</h2>
    <p>A Itinga é um grande bairro da região sul de Joinville, com muitas famílias e casas. É um perfil em que a internet precisa cobrir bem todos os cômodos, e a <strong>fibra óptica até a casa (FTTH)</strong> entrega isso com Wi-Fi forte e estável. Veja as diferenças em <a href="/blog/fibra-vs-radio-vs-cabo/">fibra óptica vs rádio vs cabo</a>.</p>

    <h2>Planos de internet para a Itinga</h2>
    <p>Os planos vão de 600 Mega (casa pequena) até 1 Giga (casa cheia). Todos incluem <strong>roteador Wi-Fi 6</strong> e pelo menos 1 app de TV ou streaming por mês:</p>

    <!--PLANS_GRID-->

    <h2>Cobertura de fibra na Itinga</h2>
    <p>Atendemos a Itinga com rede própria de fibra óptica. Como a disponibilidade varia de rua para rua, confirme se já chegamos no seu endereço <strong>consultando a cobertura pelo CEP</strong> aqui no site. Veja também <a href="/blog/cobertura-fibra-cep-joinville/">como saber se tem fibra no seu endereço</a>.</p>

    <div style="margin:24px 0;border-radius:14px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.12);line-height:0;">
      <iframe src="https://www.google.com/maps?q=Itinga%2C%20Joinville%20-%20SC&output=embed" width="100%" height="360" style="border:0;display:block;" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa do bairro Itinga, em Joinville, área de cobertura da MasterInfo"></iframe>
    </div>

    <h2>Internet para cada necessidade</h2>
    <p>Escolha a página que combina com o seu perfil: <a href="/familia/">família</a><a href="/home-office/">home office</a><a href="/gamer/">gamer</a> ou <a href="/com-2-roteadores/">Wi-Fi em toda a casa</a>. Veja também <a href="/internet-joinville/">internet fibra em Joinville</a>.</p>

    <h2>O diferencial: suporte local</h2>
    <p>Somos <strong>de Joinville, para Joinville</strong>há mais de 6 anos. Atendimento próximo, de quem é da região, com <strong>4,8 de 5 estrelas</strong> e milhares de avaliações no Google.</p>
""",
        "faq": [
            ("A MasterInfo atende a Itinga?", "Sim. A Itinga está na nossa área de cobertura de fibra óptica em Joinville. Como a disponibilidade varia de rua para rua, confirme no seu endereço pelo CEP aqui no site."),
            ("Quais as velocidades dos planos na Itinga?", "Os planos vão de 600 Mega a 1 Giga, todos em fibra óptica com Wi-Fi 6 incluso. A escolha ideal depende de quantas pessoas e aparelhos usam a internet ao mesmo tempo."),
            ("O Wi-Fi cobre a casa toda na Itinga?", "Sim. Os planos com Mesh Wi-Fi 6 usam dois roteadores em rede mesh para cobrir todos os cômodos, sem ponto cego, ideal para casas maiores."),
        ],
    },
    {
        "slug": "internet-jardim-paraiso-joinville",
        "title": "Internet Fibra no Jardim Paraíso, Joinville | MasterInfo",
        "desc": "Internet fibra óptica no Jardim Paraíso (Joinville): planos de 600 Mega a 1 Giga, Wi-Fi 6, instalação rápida e suporte local. Veja a cobertura pelo seu CEP.",
        "tag": "INTERNET · JARDIM PARAÍSO",
        "h1": "Internet fibra no Jardim Paraíso, em Joinville",
        "lead": "Fibra óptica de verdade (FTTH) no Jardim Paraíso, em Joinville, Wi-Fi 6 para a casa toda, instalação rápida e suporte de gente da região. Consulte a cobertura no seu endereço.",
        "hero_img": "/imgs/hero/sub/familia-1.jpg",
        "gradient": "linear-gradient(135deg, #c1121f 0%, #ff7a05 50%, #fcc305 100%)",
        "cta": "Ver planos e cobertura",
        "cta_plano": "lite-premium",
        "plans": ["lite-casa", "lite-premium", "ultra-familia"],
        "body": """
    <div class="tldr">
      <strong>Resumo rápido:</strong> a MasterInfo leva <strong>internet 100% fibra óptica (FTTH)</strong> para o Jardim Paraíso, em Joinville, com planos de 600 Mega a 1 Giga, Wi-Fi 6 incluso e suporte local. Consulte a cobertura no seu endereço.
    </div>

    <h2>Internet fibra no Jardim Paraíso, em Joinville</h2>
    <p>No Jardim Paraíso, a <strong>fibra óptica até a sua casa (FTTH)</strong> garante sinal estável de dia e de noite, com Wi-Fi forte para a família toda, sem a instabilidade do rádio ou dos cabos antigos. Veja as diferenças em <a href="/blog/fibra-vs-radio-vs-cabo/">fibra óptica vs rádio vs cabo</a>.</p>

    <h2>Planos de internet para o Jardim Paraíso</h2>
    <p>Os planos vão de 600 Mega (casa pequena) até 1 Giga (casa cheia). Todos incluem <strong>roteador Wi-Fi 6</strong> e pelo menos 1 app de TV ou streaming por mês:</p>

    <!--PLANS_GRID-->

    <h2>Cobertura de fibra no Jardim Paraíso</h2>
    <p>Atendemos o Jardim Paraíso com rede própria de fibra óptica. Como a disponibilidade varia de rua para rua, confirme se já chegamos no seu endereço <strong>consultando a cobertura pelo CEP</strong> aqui no site. Veja também <a href="/blog/cobertura-fibra-cep-joinville/">como saber se tem fibra no seu endereço</a>.</p>

    <div style="margin:24px 0;border-radius:14px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.12);line-height:0;">
      <iframe src="https://www.google.com/maps?q=Jardim%20Paraiso%2C%20Joinville%20-%20SC&output=embed" width="100%" height="360" style="border:0;display:block;" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa do bairro Jardim Paraíso, em Joinville, área de cobertura da MasterInfo"></iframe>
    </div>

    <h2>Internet para cada necessidade</h2>
    <p>Escolha a página que combina com o seu perfil: <a href="/familia/">família</a><a href="/home-office/">home office</a><a href="/gamer/">gamer</a> ou <a href="/com-2-roteadores/">Wi-Fi em toda a casa</a>. Veja também <a href="/internet-joinville/">internet fibra em Joinville</a>.</p>

    <h2>O diferencial: suporte local</h2>
    <p>Somos <strong>de Joinville, para Joinville</strong>há mais de 6 anos. Atendimento próximo, de quem é da região, com <strong>4,8 de 5 estrelas</strong> no Google.</p>
""",
        "faq": [
            ("A MasterInfo atende o Jardim Paraíso?", "Sim. O Jardim Paraíso está na nossa área de cobertura de fibra óptica em Joinville. Como a disponibilidade varia de rua para rua, confirme no seu endereço pelo CEP aqui no site."),
            ("Quais as velocidades dos planos no Jardim Paraíso?", "Os planos vão de 600 Mega a 1 Giga, todos em fibra óptica com Wi-Fi 6 incluso. A escolha ideal depende de quantas pessoas e aparelhos usam a internet ao mesmo tempo."),
            ("Quanto tempo leva para instalar no Jardim Paraíso?", "Após confirmar a cobertura e contratar, a instalação costuma ser agendada para os próximos dias úteis, feita pela nossa equipe técnica local."),
        ],
    },
    {
        "slug": "internet-jardim-sofia-joinville",
        "title": "Internet Fibra no Jardim Sofia, Joinville | MasterInfo",
        "desc": "Internet fibra óptica no Jardim Sofia (Joinville): planos de 600 Mega a 1 Giga, Wi-Fi 6, instalação rápida e suporte local. Veja a cobertura pelo seu CEP.",
        "tag": "INTERNET · JARDIM SOFIA",
        "h1": "Internet fibra no Jardim Sofia, em Joinville",
        "lead": "Fibra óptica de verdade (FTTH) no Jardim Sofia, em Joinville, estabilidade para trabalho remoto, Wi-Fi 6 e suporte de gente da região. Consulte a cobertura no seu endereço.",
        "hero_img": "/imgs/hero/sub/familia-1.jpg",
        "gradient": "linear-gradient(135deg, #c1121f 0%, #ff7a05 50%, #fcc305 100%)",
        "cta": "Ver planos e cobertura",
        "cta_plano": "lite-premium",
        "plans": ["lite-casa", "lite-premium", "ultra-familia"],
        "body": """
    <div class="tldr">
      <strong>Resumo rápido:</strong> a MasterInfo leva <strong>internet 100% fibra óptica (FTTH)</strong> para o Jardim Sofia, em Joinville, com planos de 600 Mega a 1 Giga, Wi-Fi 6 incluso e suporte local. Consulte a cobertura no seu endereço.
    </div>

    <h2>Internet fibra no Jardim Sofia, em Joinville</h2>
    <p>Para quem trabalha ou estuda de casa no Jardim Sofia, estabilidade é tudo. A <strong>fibra óptica até a casa (FTTH)</strong> entrega conexão constante para reuniões em vídeo e upload rápido, sem quedas. Entenda as diferenças em <a href="/blog/fibra-vs-radio-vs-cabo/">fibra óptica vs rádio vs cabo</a>.</p>

    <h2>Planos de internet para o Jardim Sofia</h2>
    <p>Os planos vão de 600 Mega (casa pequena) até 1 Giga (casa cheia). Todos incluem <strong>roteador Wi-Fi 6</strong> e pelo menos 1 app de TV ou streaming por mês:</p>

    <!--PLANS_GRID-->

    <h2>Cobertura de fibra no Jardim Sofia</h2>
    <p>Atendemos o Jardim Sofia com rede própria de fibra óptica. Como a disponibilidade varia de rua para rua, confirme se já chegamos no seu endereço <strong>consultando a cobertura pelo CEP</strong> aqui no site. Veja também <a href="/blog/cobertura-fibra-cep-joinville/">como saber se tem fibra no seu endereço</a>.</p>

    <div style="margin:24px 0;border-radius:14px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.12);line-height:0;">
      <iframe src="https://www.google.com/maps?q=Jardim%20Sofia%2C%20Joinville%20-%20SC&output=embed" width="100%" height="360" style="border:0;display:block;" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa do bairro Jardim Sofia, em Joinville, área de cobertura da MasterInfo"></iframe>
    </div>

    <h2>Internet para cada necessidade</h2>
    <p>Escolha a página que combina com o seu perfil: <a href="/familia/">família</a><a href="/home-office/">home office</a><a href="/gamer/">gamer</a> ou <a href="/com-2-roteadores/">Wi-Fi em toda a casa</a>. Veja também <a href="/internet-joinville/">internet fibra em Joinville</a>.</p>

    <h2>O diferencial: suporte local</h2>
    <p>Somos <strong>de Joinville, para Joinville</strong>há mais de 6 anos. Atendimento próximo, de quem é da região, com <strong>4,8 de 5 estrelas</strong> no Google.</p>
""",
        "faq": [
            ("A MasterInfo atende o Jardim Sofia?", "Sim. O Jardim Sofia está na nossa área de cobertura de fibra óptica em Joinville. Como a disponibilidade varia de rua para rua, confirme no seu endereço pelo CEP aqui no site."),
            ("A internet é boa para trabalhar de casa no Jardim Sofia?", "Sim. A fibra óptica oferece estabilidade e upload rápido, ideais para reuniões em vídeo e home office. Os planos de 1 Giga com Wi-Fi 6 dão folga até com a casa toda conectada."),
            ("Quanto tempo leva para instalar no Jardim Sofia?", "Após confirmar a cobertura e contratar, a instalação costuma ser agendada para os próximos dias úteis, feita pela nossa equipe técnica local."),
        ],
    },
    {
        "slug": "internet-cubatao-joinville",
        "title": "Internet Fibra no Cubatão, Joinville | MasterInfo",
        "desc": "Internet fibra óptica no Cubatão (Joinville): planos de 600 Mega a 1 Giga, Wi-Fi 6, instalação rápida e suporte local. Veja a cobertura pelo seu CEP.",
        "tag": "INTERNET · CUBATÃO",
        "h1": "Internet fibra no Cubatão, em Joinville",
        "lead": "Fibra óptica de verdade (FTTH) no Cubatão, em Joinville, Wi-Fi 6, instalação rápida e suporte de gente da região. Consulte a cobertura no seu endereço e contrate em minutos.",
        "hero_img": "/imgs/hero/sub/familia-1.jpg",
        "gradient": "linear-gradient(135deg, #c1121f 0%, #ff7a05 50%, #fcc305 100%)",
        "cta": "Ver planos e cobertura",
        "cta_plano": "lite-premium",
        "plans": ["lite-casa", "lite-premium", "ultra-familia"],
        "body": """
    <div class="tldr">
      <strong>Resumo rápido:</strong> a MasterInfo leva <strong>internet 100% fibra óptica (FTTH)</strong> para o Cubatão, em Joinville, com planos de 600 Mega a 1 Giga, Wi-Fi 6 incluso e suporte local. Consulte a cobertura no seu endereço.
    </div>

    <h2>Internet fibra no Cubatão, em Joinville</h2>
    <p>No Cubatão, a <strong>fibra óptica até a casa (FTTH)</strong> entrega sinal estável e Wi-Fi forte para streaming, estudo e trabalho, a mesma velocidade chova ou faça sol. Veja as diferenças em <a href="/blog/fibra-vs-radio-vs-cabo/">fibra óptica vs rádio vs cabo</a>.</p>

    <h2>Planos de internet para o Cubatão</h2>
    <p>Os planos vão de 600 Mega (casa pequena) até 1 Giga (casa cheia). Todos incluem <strong>roteador Wi-Fi 6</strong> e pelo menos 1 app de TV ou streaming por mês:</p>

    <!--PLANS_GRID-->

    <h2>Cobertura de fibra no Cubatão</h2>
    <p>Atendemos o Cubatão com rede própria de fibra óptica. Como a disponibilidade varia de rua para rua, confirme se já chegamos no seu endereço <strong>consultando a cobertura pelo CEP</strong> aqui no site. Veja também <a href="/blog/cobertura-fibra-cep-joinville/">como saber se tem fibra no seu endereço</a>.</p>

    <div style="margin:24px 0;border-radius:14px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.12);line-height:0;">
      <iframe src="https://www.google.com/maps?q=Cubatao%2C%20Joinville%20-%20SC&output=embed" width="100%" height="360" style="border:0;display:block;" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa do bairro Cubatão, em Joinville, área de cobertura da MasterInfo"></iframe>
    </div>

    <h2>Internet para cada necessidade</h2>
    <p>Escolha a página que combina com o seu perfil: <a href="/familia/">família</a><a href="/home-office/">home office</a><a href="/gamer/">gamer</a> ou <a href="/com-2-roteadores/">Wi-Fi em toda a casa</a>. Veja também <a href="/internet-joinville/">internet fibra em Joinville</a>.</p>

    <h2>O diferencial: suporte local</h2>
    <p>Somos <strong>de Joinville, para Joinville</strong>há mais de 6 anos. Atendimento próximo, de quem é da região, com <strong>4,8 de 5 estrelas</strong> no Google.</p>
""",
        "faq": [
            ("A MasterInfo atende o Cubatão?", "Sim. O Cubatão está na nossa área de cobertura de fibra óptica em Joinville. Como a disponibilidade varia de rua para rua, confirme no seu endereço pelo CEP aqui no site."),
            ("Quais as velocidades dos planos no Cubatão?", "Os planos vão de 600 Mega a 1 Giga, todos em fibra óptica com Wi-Fi 6 incluso. A escolha ideal depende de quantas pessoas e aparelhos usam a internet ao mesmo tempo."),
            ("Quanto tempo leva para instalar no Cubatão?", "Após confirmar a cobertura e contratar, a instalação costuma ser agendada para os próximos dias úteis, feita pela nossa equipe técnica local."),
        ],
    },
    {
        "slug": "internet-nova-brasilia-joinville",
        "title": "Internet Fibra na Nova Brasília, Joinville | MasterInfo",
        "desc": "Internet fibra óptica na Nova Brasília (Joinville): planos de 600 Mega a 1 Giga, Wi-Fi 6, instalação rápida e suporte local. Veja a cobertura pelo seu CEP.",
        "tag": "INTERNET · NOVA BRASÍLIA",
        "h1": "Internet fibra na Nova Brasília, em Joinville",
        "lead": "Fibra óptica de verdade (FTTH) na Nova Brasília, em Joinville, Wi-Fi 6 para a casa toda, instalação rápida e suporte de gente da região. Consulte a cobertura no seu endereço.",
        "hero_img": "/imgs/hero/sub/familia-1.jpg",
        "gradient": "linear-gradient(135deg, #c1121f 0%, #ff7a05 50%, #fcc305 100%)",
        "cta": "Ver planos e cobertura",
        "cta_plano": "lite-premium",
        "plans": ["lite-casa", "lite-premium", "ultra-familia"],
        "body": """
    <div class="tldr">
      <strong>Resumo rápido:</strong> a MasterInfo leva <strong>internet 100% fibra óptica (FTTH)</strong> para a Nova Brasília, em Joinville, com planos de 600 Mega a 1 Giga, Wi-Fi 6 incluso e suporte local. Consulte a cobertura no seu endereço.
    </div>

    <h2>Internet fibra na Nova Brasília, em Joinville</h2>
    <p>Na Nova Brasília, a <strong>fibra óptica até a casa (FTTH)</strong> garante Wi-Fi forte em todos os cômodos e sinal estável para a família toda usar ao mesmo tempo. Veja as diferenças em <a href="/blog/fibra-vs-radio-vs-cabo/">fibra óptica vs rádio vs cabo</a>.</p>

    <h2>Planos de internet para a Nova Brasília</h2>
    <p>Os planos vão de 600 Mega (casa pequena) até 1 Giga (casa cheia). Todos incluem <strong>roteador Wi-Fi 6</strong> e pelo menos 1 app de TV ou streaming por mês:</p>

    <!--PLANS_GRID-->

    <h2>Cobertura de fibra na Nova Brasília</h2>
    <p>Atendemos a Nova Brasília com rede própria de fibra óptica. Como a disponibilidade varia de rua para rua, confirme se já chegamos no seu endereço <strong>consultando a cobertura pelo CEP</strong> aqui no site. Veja também <a href="/blog/cobertura-fibra-cep-joinville/">como saber se tem fibra no seu endereço</a>.</p>

    <div style="margin:24px 0;border-radius:14px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.12);line-height:0;">
      <iframe src="https://www.google.com/maps?q=Nova%20Brasilia%2C%20Joinville%20-%20SC&output=embed" width="100%" height="360" style="border:0;display:block;" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa do bairro Nova Brasília, em Joinville, área de cobertura da MasterInfo"></iframe>
    </div>

    <h2>Internet para cada necessidade</h2>
    <p>Escolha a página que combina com o seu perfil: <a href="/familia/">família</a><a href="/home-office/">home office</a><a href="/gamer/">gamer</a> ou <a href="/com-2-roteadores/">Wi-Fi em toda a casa</a>. Veja também <a href="/internet-joinville/">internet fibra em Joinville</a>.</p>

    <h2>O diferencial: suporte local</h2>
    <p>Somos <strong>de Joinville, para Joinville</strong>há mais de 6 anos. Atendimento próximo, de quem é da região, com <strong>4,8 de 5 estrelas</strong> no Google.</p>
""",
        "faq": [
            ("A MasterInfo atende a Nova Brasília?", "Sim. A Nova Brasília está na nossa área de cobertura de fibra óptica em Joinville. Como a disponibilidade varia de rua para rua, confirme no seu endereço pelo CEP aqui no site."),
            ("Quais as velocidades dos planos na Nova Brasília?", "Os planos vão de 600 Mega a 1 Giga, todos em fibra óptica com Wi-Fi 6 incluso. A escolha ideal depende de quantas pessoas e aparelhos usam a internet ao mesmo tempo."),
            ("Quanto tempo leva para instalar na Nova Brasília?", "Após confirmar a cobertura e contratar, a instalação costuma ser agendada para os próximos dias úteis, feita pela nossa equipe técnica local."),
        ],
    },
    {
        "slug": "internet-rio-bonito-joinville",
        "title": "Internet Fibra no Rio Bonito, Joinville | MasterInfo",
        "desc": "Internet fibra óptica no Rio Bonito (Joinville): planos de 600 Mega a 1 Giga, Wi-Fi 6, instalação rápida e suporte local. Veja a cobertura pelo seu CEP.",
        "tag": "INTERNET · RIO BONITO",
        "h1": "Internet fibra no Rio Bonito, em Joinville",
        "lead": "Fibra óptica de verdade (FTTH) no Rio Bonito, em Joinville, fibra de verdade até a sua casa, Wi-Fi 6 e suporte de gente da região. Consulte a cobertura no seu endereço.",
        "hero_img": "/imgs/hero/sub/familia-1.jpg",
        "gradient": "linear-gradient(135deg, #c1121f 0%, #ff7a05 50%, #fcc305 100%)",
        "cta": "Ver planos e cobertura",
        "cta_plano": "lite-premium",
        "plans": ["lite-casa", "lite-premium", "ultra-familia"],
        "body": """
    <div class="tldr">
      <strong>Resumo rápido:</strong> a MasterInfo leva <strong>internet 100% fibra óptica (FTTH)</strong> para o Rio Bonito, em Joinville, com planos de 600 Mega a 1 Giga, Wi-Fi 6 incluso e suporte local. Consulte a cobertura no seu endereço.
    </div>

    <h2>Internet fibra no Rio Bonito, em Joinville</h2>
    <p>No Rio Bonito, a <strong>fibra óptica até a casa (FTTH)</strong> faz diferença: leva conexão estável e Wi-Fi forte, com a mesma velocidade de dia e de noite, sem a instabilidade do rádio. Veja as diferenças em <a href="/blog/fibra-vs-radio-vs-cabo/">fibra óptica vs rádio vs cabo</a>.</p>

    <h2>Planos de internet para o Rio Bonito</h2>
    <p>Os planos vão de 600 Mega (casa pequena) até 1 Giga (casa cheia). Todos incluem <strong>roteador Wi-Fi 6</strong> e pelo menos 1 app de TV ou streaming por mês:</p>

    <!--PLANS_GRID-->

    <h2>Cobertura de fibra no Rio Bonito</h2>
    <p>Atendemos o Rio Bonito com rede própria de fibra óptica. Como a disponibilidade varia de rua para rua, confirme se já chegamos no seu endereço <strong>consultando a cobertura pelo CEP</strong> aqui no site. Veja também <a href="/blog/cobertura-fibra-cep-joinville/">como saber se tem fibra no seu endereço</a>.</p>

    <div style="margin:24px 0;border-radius:14px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.12);line-height:0;">
      <iframe src="https://www.google.com/maps?q=Rio%20Bonito%2C%20Joinville%20-%20SC&output=embed" width="100%" height="360" style="border:0;display:block;" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa da região do Rio Bonito, em Joinville, área de cobertura da MasterInfo"></iframe>
    </div>

    <h2>Internet para cada necessidade</h2>
    <p>Escolha a página que combina com o seu perfil: <a href="/familia/">família</a><a href="/home-office/">home office</a><a href="/gamer/">gamer</a> ou <a href="/com-2-roteadores/">Wi-Fi em toda a casa</a>. Veja também <a href="/internet-joinville/">internet fibra em Joinville</a>.</p>

    <h2>O diferencial: suporte local</h2>
    <p>Somos <strong>de Joinville, para Joinville</strong>há mais de 6 anos. Atendimento próximo, de quem é da região, com <strong>4,8 de 5 estrelas</strong> no Google.</p>
""",
        "faq": [
            ("A MasterInfo atende o Rio Bonito?", "Sim. O Rio Bonito está na nossa área de cobertura de fibra óptica em Joinville. Como a disponibilidade varia de rua para rua, confirme no seu endereço pelo CEP aqui no site."),
            ("Quais as velocidades dos planos no Rio Bonito?", "Os planos vão de 600 Mega a 1 Giga, todos em fibra óptica com Wi-Fi 6 incluso. A escolha ideal depende de quantas pessoas e aparelhos usam a internet ao mesmo tempo."),
            ("Quanto tempo leva para instalar no Rio Bonito?", "Após confirmar a cobertura e contratar, a instalação costuma ser agendada para os próximos dias úteis, feita pela nossa equipe técnica local."),
        ],
    },
    {
        "slug": "internet-estrada-timbe-joinville",
        "title": "Internet Fibra na Estrada Timbé, Joinville | MasterInfo",
        "desc": "Internet fibra óptica na Estrada Timbé (Joinville): planos de 600 Mega a 1 Giga, Wi-Fi 6, instalação rápida e suporte local. Veja a cobertura pelo seu CEP.",
        "tag": "INTERNET · ESTRADA TIMBÉ",
        "h1": "Internet fibra na Estrada Timbé, em Joinville",
        "lead": "Fibra óptica de verdade (FTTH) na região da Estrada Timbé, em Joinville, fibra de verdade até a sua casa, Wi-Fi 6 e suporte de gente da região. Consulte a cobertura no seu endereço.",
        "hero_img": "/imgs/hero/sub/familia-1.jpg",
        "gradient": "linear-gradient(135deg, #c1121f 0%, #ff7a05 50%, #fcc305 100%)",
        "cta": "Ver planos e cobertura",
        "cta_plano": "lite-premium",
        "plans": ["lite-casa", "lite-premium", "ultra-familia"],
        "body": """
    <div class="tldr">
      <strong>Resumo rápido:</strong> a MasterInfo leva <strong>internet 100% fibra óptica (FTTH)</strong> para a região da Estrada Timbé, em Joinville, com planos de 600 Mega a 1 Giga, Wi-Fi 6 incluso e suporte local. Consulte a cobertura no seu endereço.
    </div>

    <h2>Internet fibra na Estrada Timbé, em Joinville</h2>
    <p>Na região da Estrada Timbé, ter <strong>fibra óptica de verdade até a casa (FTTH)</strong> faz toda a diferença frente às alternativas instáveis: sinal constante e Wi-Fi forte, chova ou faça sol. Veja as diferenças em <a href="/blog/fibra-vs-radio-vs-cabo/">fibra óptica vs rádio vs cabo</a>.</p>

    <h2>Planos de internet para a Estrada Timbé</h2>
    <p>Os planos vão de 600 Mega (casa pequena) até 1 Giga (casa cheia). Todos incluem <strong>roteador Wi-Fi 6</strong> e pelo menos 1 app de TV ou streaming por mês:</p>

    <!--PLANS_GRID-->

    <h2>Cobertura de fibra na Estrada Timbé</h2>
    <p>Atendemos a região da Estrada Timbé com rede própria de fibra óptica. Como a disponibilidade varia de trecho para trecho, confirme se já chegamos no seu endereço <strong>consultando a cobertura pelo CEP</strong> aqui no site. Veja também <a href="/blog/cobertura-fibra-cep-joinville/">como saber se tem fibra no seu endereço</a>.</p>

    <div style="margin:24px 0;border-radius:14px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.12);line-height:0;">
      <iframe src="https://www.google.com/maps?q=Estrada%20Timbe%2C%20Joinville%20-%20SC&output=embed" width="100%" height="360" style="border:0;display:block;" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa da região da Estrada Timbé, em Joinville, área de cobertura da MasterInfo"></iframe>
    </div>

    <h2>Internet para cada necessidade</h2>
    <p>Escolha a página que combina com o seu perfil: <a href="/familia/">família</a><a href="/home-office/">home office</a><a href="/gamer/">gamer</a> ou <a href="/com-2-roteadores/">Wi-Fi em toda a casa</a>. Veja também <a href="/internet-joinville/">internet fibra em Joinville</a>.</p>

    <h2>O diferencial: suporte local</h2>
    <p>Somos <strong>de Joinville, para Joinville</strong>há mais de 6 anos. Atendimento próximo, de quem é da região, com <strong>4,8 de 5 estrelas</strong> no Google.</p>
""",
        "faq": [
            ("A MasterInfo atende a Estrada Timbé?", "Sim. A região da Estrada Timbé está na nossa área de cobertura de fibra óptica em Joinville. Como a disponibilidade varia de trecho para trecho, confirme no seu endereço pelo CEP aqui no site."),
            ("Quais as velocidades dos planos na Estrada Timbé?", "Os planos vão de 600 Mega a 1 Giga, todos em fibra óptica com Wi-Fi 6 incluso. A escolha ideal depende de quantas pessoas e aparelhos usam a internet ao mesmo tempo."),
            ("Quanto tempo leva para instalar na Estrada Timbé?", "Após confirmar a cobertura e contratar, a instalação costuma ser agendada para os próximos dias úteis, feita pela nossa equipe técnica local."),
        ],
    },
    {
        "slug": "internet-paranaguamirim-joinville",
        "title": "Internet Fibra no Paranaguamirim, Joinville | MasterInfo",
        "desc": "Internet fibra óptica no Paranaguamirim (Joinville): planos de 600 Mega a 1 Giga, Wi-Fi 6, instalação rápida e suporte local. Veja a cobertura pelo seu CEP.",
        "tag": "INTERNET · PARANAGUAMIRIM",
        "h1": "Internet fibra no Paranaguamirim, em Joinville",
        "lead": "Fibra óptica de verdade (FTTH) no Paranaguamirim, um grande bairro da região sul de Joinville, Wi-Fi 6, instalação rápida e suporte de gente da região. Consulte a cobertura no seu endereço.",
        "hero_img": "/imgs/hero/sub/familia-1.jpg",
        "gradient": "linear-gradient(135deg, #c1121f 0%, #ff7a05 50%, #fcc305 100%)",
        "cta": "Ver planos e cobertura",
        "cta_plano": "lite-premium",
        "plans": ["lite-casa", "lite-premium", "ultra-familia"],
        "body": """
    <div class="tldr">
      <strong>Resumo rápido:</strong> a MasterInfo leva <strong>internet 100% fibra óptica (FTTH)</strong> para o Paranaguamirim, um grande bairro da região sul de Joinville, com planos de 600 Mega a 1 Giga, Wi-Fi 6 incluso e suporte local. Consulte a cobertura no seu endereço.
    </div>

    <h2>Internet fibra no Paranaguamirim, em Joinville</h2>
    <p>O Paranaguamirim é um grande bairro da região sul de Joinville, com muitas famílias. A <strong>fibra óptica até a casa (FTTH)</strong> entrega Wi-Fi forte para todos os cômodos e aguenta vários aparelhos ao mesmo tempo. Veja as diferenças em <a href="/blog/fibra-vs-radio-vs-cabo/">fibra óptica vs rádio vs cabo</a>.</p>

    <h2>Planos de internet para o Paranaguamirim</h2>
    <p>Os planos vão de 600 Mega (casa pequena) até 1 Giga (casa cheia). Todos incluem <strong>roteador Wi-Fi 6</strong> e pelo menos 1 app de TV ou streaming por mês:</p>

    <!--PLANS_GRID-->

    <h2>Cobertura de fibra no Paranaguamirim</h2>
    <p>Atendemos o Paranaguamirim com rede própria de fibra óptica. Como a disponibilidade varia de rua para rua, confirme se já chegamos no seu endereço <strong>consultando a cobertura pelo CEP</strong> aqui no site. Veja também <a href="/blog/cobertura-fibra-cep-joinville/">como saber se tem fibra no seu endereço</a>.</p>

    <div style="margin:24px 0;border-radius:14px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.12);line-height:0;">
      <iframe src="https://www.google.com/maps?q=Paranaguamirim%2C%20Joinville%20-%20SC&output=embed" width="100%" height="360" style="border:0;display:block;" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa do bairro Paranaguamirim, em Joinville, área de cobertura da MasterInfo"></iframe>
    </div>

    <h2>Internet para cada necessidade</h2>
    <p>Escolha a página que combina com o seu perfil: <a href="/familia/">família</a><a href="/home-office/">home office</a><a href="/gamer/">gamer</a> ou <a href="/com-2-roteadores/">Wi-Fi em toda a casa</a>. Veja também <a href="/internet-joinville/">internet fibra em Joinville</a>.</p>

    <h2>O diferencial: suporte local</h2>
    <p>Somos <strong>de Joinville, para Joinville</strong>há mais de 6 anos. Atendimento próximo, de quem é da região, com <strong>4,8 de 5 estrelas</strong> e milhares de avaliações no Google.</p>
""",
        "faq": [
            ("A MasterInfo atende o Paranaguamirim?", "Sim. O Paranaguamirim está na nossa área de cobertura de fibra óptica em Joinville. Como a disponibilidade varia de rua para rua, confirme no seu endereço pelo CEP aqui no site."),
            ("A internet aguenta uma casa com muita gente no Paranaguamirim?", "Sim. Os planos de 1 Giga com Mesh Wi-Fi 6 foram pensados para casas cheias, com vários aparelhos conectados ao mesmo tempo sem travar."),
            ("Quanto tempo leva para instalar no Paranaguamirim?", "Após confirmar a cobertura e contratar, a instalação costuma ser agendada para os próximos dias úteis, feita pela nossa equipe técnica local."),
        ],
    },
]

# ─── BLOG (posts informacionais) ──────────────────────────────────────────
# slug → /blog/slug/ (depth 2). author = chave em AUTHORS. image = destaque (og).
BLOG = [
    {
        "slug": "quantos-mega-de-internet-voce-precisa",
        "title": "Quantos Mega de Internet Você Precisa? Guia por Perfil",
        "desc": "Quantos Mega de internet contratar? Guia por perfil de uso (sozinho, casal, família, home office, gamer) com tabela por atividade e recomendação prática.",
        "h1": "Quantos Mega de internet você precisa? Guia por perfil",
        "lead": "Antes de contratar, descubra a velocidade ideal pra sua casa sem pagar a mais nem ficar travando. A conta é simples e depende de quantas pessoas e aparelhos usam a internet ao mesmo tempo.",
        "author": "tecnica",
        "date": DATE_DEFAULT,
        "image": "/imgs/hero/sub/familia-1.jpg",
        "tags": ["Planos", "Velocidade", "Dicas"],
        "body": """
    <div class="tldr">
      <strong>Resposta rápida:</strong> para 1 a 2 pessoas com uso comum, <strong>300 a 500 Mega</strong> resolvem. Família com vários aparelhos e streaming em 4K: <strong>600 a 800 Mega</strong>. Casa cheia, home office e jogos ao mesmo tempo: <strong>1 Giga</strong>. O que mais pesa não é o tipo de atividade, e sim <strong>quantos aparelhos usam a internet juntos</strong>.
    </div>

    <h2>O que define a velocidade ideal</h2>
    <p>Muita gente acha que precisa de um plano gigante por causa de uma atividade específica (jogar, por exemplo). Na verdade, o que mais consome banda é a <strong>soma de tudo acontecendo ao mesmo tempo</strong>: a TV em streaming, dois celulares no TikTok, alguém em chamada de vídeo e o videogame baixando uma atualização. Quanto mais aparelhos simultâneos, mais Mega você precisa.</p>

    <h2>Quanto cada atividade consome</h2>
    <p>Para você ter uma referência, veja o consumo aproximado de cada atividade sozinha:</p>
    <table class="article-table">
      <thead><tr><th>Atividade</th><th>Velocidade recomendada</th></tr></thead>
      <tbody>
        <tr><td>Redes sociais e navegação</td><td>5 a 10 Mega</td></tr>
        <tr><td>Streaming de vídeo em HD</td><td>10 a 15 Mega</td></tr>
        <tr><td>Streaming em 4K</td><td>25 Mega por tela</td></tr>
        <tr><td>Chamada de vídeo (trabalho)</td><td>10 a 20 Mega</td></tr>
        <tr><td>Jogos online</td><td>20 a 50 Mega (e ping baixo)</td></tr>
        <tr><td>Download de jogos e arquivos grandes</td><td>quanto mais, melhor</td></tr>
      </tbody>
    </table>
    <p>Repare: nenhuma atividade sozinha exige 1 Giga. A conta muda quando tudo roda junto, em vários aparelhos.</p>

    <h2>Recomendação por perfil</h2>
    <h3>Mora sozinho ou em casal</h3>
    <p>Uso comum (redes, streaming, uma chamada de vez em quando): <strong>300 a 500 Mega</strong> sobram. Boa pedida é a <a href="/com-1-roteador/">internet para apartamento e casa pequena</a>.</p>
    <h3>Família com vários aparelhos</h3>
    <p>Streaming em 4K, criança no tablet, todo mundo conectado: <strong>600 a 800 Mega</strong> garantem tudo rodando sem travar. Veja a <a href="/familia/">internet para a família</a>.</p>
    <h3>Home office</h3>
    <p>Reunião que não pode cair e upload de arquivos pesados pedem estabilidade e bom upload: a partir de <strong>500 a 800 Mega</strong>. Detalhes na <a href="/home-office/">internet para home office</a>.</p>
    <h3>Gamer</h3>
    <p>Para jogo online, o ping (latência) importa mais que o número de Mega. Ainda assim, <strong>500 Mega a 1 Giga</strong> garantem baixar updates rápido e jogar enquanto outros usam a casa. Veja a <a href="/gamer/">internet para gamer</a>.</p>
    <h3>Casa grande ou cheia</h3>
    <p>Muita gente, muitos cômodos: além de <strong>800 Mega a 1 Giga</strong>considere <a href="/com-2-roteadores/">Wi-Fi com 2 roteadores</a> para não ter ponto cego.</p>

    <h2>Wi-Fi também importa</h2>
    <p>De nada adianta contratar 1 Giga e ter Wi-Fi fraco. O roteador e o posicionamento dele fazem muita diferença. Se o sinal não chega bem em algum cômodo, leia <a href="/blog/como-melhorar-wifi-em-casa/">como melhorar o Wi-Fi em casa</a>.</p>
""",
        "faq": [
            ("Quantos Mega preciso para uma família?", "Para uma família com vários aparelhos, streaming em 4K e uso simultâneo, 600 a 800 Mega costumam ser o ideal. Casas muito cheias ou com home office podem se beneficiar de 1 Giga."),
            ("Quantos Mega preciso para jogar online?", "Para jogos, o ping (latência) importa mais que a velocidade. Uma conexão de 300 a 500 Mega em fibra com baixa latência já joga bem; mais Mega ajudam a baixar atualizações rápido e a dividir a casa."),
            ("Mais Mega deixa a internet mais rápida?", "Mais Mega ajudam quando há muitos aparelhos usando ao mesmo tempo ou downloads grandes. Para uma única atividade, a partir de certo ponto você não percebe diferença: o Wi-Fi e a estabilidade passam a importar mais."),
            ("Como sei se estou recebendo a velocidade contratada?", "Faça um teste de velocidade conectado por cabo ou perto do roteador. Em fibra, você deve receber perto da velocidade contratada; perdas grandes podem indicar Wi-Fi fraco ou problema a resolver com o suporte."),
        ],
    },
    {
        "slug": "fibra-vs-radio-vs-cabo",
        "title": "Fibra Óptica vs Rádio vs Cabo: Qual a Melhor Internet?",
        "desc": "Fibra óptica, internet via rádio ou cabo: entenda as diferenças de velocidade, estabilidade e cobertura, e descubra qual é a melhor internet pra você.",
        "h1": "Fibra óptica vs rádio vs cabo: qual a melhor internet?",
        "lead": "Os três tipos de conexão mais comuns no Brasil têm diferenças grandes de estabilidade e velocidade. Entenda cada um em linguagem simples e veja por que a fibra virou o padrão.",
        "author": "tecnica",
        "date": DATE_DEFAULT,
        "image": "/imgs/blog/fibra-optica.jpg",
        "tags": ["Tecnologia", "Fibra óptica"],
        "body": """
    <div class="tldr">
      <strong>Resposta rápida:</strong> a <strong>fibra óptica</strong> é a melhor tecnologia de internet disponível hoje: mais rápida, mais estável e imune a chuva e interferência. A internet <strong>via rádio</strong> serve para áreas rurais sem cabeamento, mas oscila e divide banda. O <strong>cabo</strong> (par metálico) é antigo e perde para a fibra em quase tudo. Se há fibra no seu endereço, ela é a escolha certa.
    </div>

    <h2>O que é cada tecnologia</h2>
    <p><strong>Fibra óptica:</strong> os dados viajam como luz dentro de um cabo de vidro finíssimo. É a tecnologia mais moderna, com altíssima capacidade e pouquíssima perda de sinal por distância.</p>
    <p><strong>Internet via rádio:</strong> o sinal chega por ondas de rádio, de uma antena/torre até um receptor no seu telhado. Não precisa de cabo até a casa, o que ajuda em áreas remotas.</p>
    <p><strong>Cabo (par metálico/coaxial):</strong> usa fios de cobre para transmitir sinal elétrico. Foi muito comum no passado, mas tem capacidade e estabilidade menores que a fibra.</p>

    <h2>Comparativo direto</h2>
    <table class="article-table">
      <thead><tr><th>Critério</th><th>Fibra óptica</th><th>Via rádio</th><th>Cabo metálico</th></tr></thead>
      <tbody>
        <tr><td>Velocidade</td><td>Muito alta (até 1 Giga+)</td><td>Baixa a média</td><td>Média</td></tr>
        <tr><td>Estabilidade</td><td>Excelente</td><td>Oscila (clima, obstáculos)</td><td>Boa, mas inferior à fibra</td></tr>
        <tr><td>Afeta com chuva?</td><td>Não</td><td>Sim</td><td>Pouco</td></tr>
        <tr><td>Banda compartilhada</td><td>Dedicada por casa (FTTH)</td><td>Compartilhada na torre</td><td>Compartilhada</td></tr>
        <tr><td>Melhor para</td><td>Casa e empresa na cidade</td><td>Zona rural sem fibra</td><td>Legado</td></tr>
      </tbody>
    </table>

    <h2>Por que a fibra virou o padrão</h2>
    <p>A fibra não sofre interferência eletromagnética, não perde sinal com a chuva e mantém a mesma velocidade independentemente da distância (dentro do projeto da rede). Para quem mora na cidade, como em <a href="/internet-joinville/">Joinville</a>é disparado a melhor opção: estável de dia e de noite, com latência baixa para chamadas e jogos.</p>

    <h2>E a internet via rádio, quando faz sentido?</h2>
    <p>A internet via rádio tem o seu lugar: em áreas rurais ou afastadas, onde ainda não chegou cabeamento de fibra, ela conecta onde nada mais conecta. A desvantagem é depender de linha de visada com a torre e sofrer com clima e congestionamento quando muita gente usa a mesma antena.</p>

    <h2>Como saber qual você tem (ou pode ter)</h2>
    <p>Se o provedor instala um equipamento ligado a um cabo de fibra que entra na sua casa, é FTTH (fibra até a casa), o ideal. Para descobrir se já existe fibra no seu endereço, veja <a href="/blog/cobertura-fibra-cep-joinville/">como consultar a cobertura pelo CEP</a> ou compare as opções no guia <a href="/melhor-internet-joinville/">qual a melhor internet de Joinville</a>.</p>
""",
        "faq": [
            ("Fibra óptica é melhor que internet via rádio?", "Na cidade, sim. A fibra é mais rápida, mais estável e não sofre com chuva nem interferência. A internet via rádio é uma boa alternativa em áreas rurais onde ainda não há cabeamento de fibra."),
            ("A fibra óptica cai com chuva?", "Não. Como os dados viajam por luz dentro de um cabo de vidro, a fibra não é afetada por chuva nem por interferência eletromagnética, ao contrário da internet via rádio."),
            ("Qual a diferença de fibra para cabo?", "A fibra usa luz em cabo de vidro, com altíssima capacidade e estabilidade. O cabo metálico (cobre) usa sinal elétrico, com capacidade e estabilidade menores. A fibra supera o cabo em praticamente tudo."),
            ("Como sei se tenho fibra até minha casa?", "Se a conexão chega por um cabo de fibra ligado a um equipamento (ONU/ONT) dentro do imóvel, é FTTH (fibra até a casa). Consulte a cobertura pelo CEP para confirmar a disponibilidade no seu endereço."),
        ],
    },
    {
        "slug": "cobertura-fibra-cep-joinville",
        "title": "Como Saber se Tem Fibra no Seu Endereço em Joinville",
        "desc": "Veja como descobrir se tem internet fibra no seu endereço em Joinville: consulta de cobertura por CEP, passo a passo e o que fazer se ainda não chegou.",
        "h1": "Como saber se tem fibra no seu endereço em Joinville",
        "lead": "Antes de contratar, vale confirmar se a fibra já chegou na sua rua. Dá pra checar em segundos pelo CEP, sem precisar ligar pra ninguém. Veja o passo a passo.",
        "author": "tecnica",
        "date": DATE_DEFAULT,
        "image": "/imgs/blog/cobertura-joinville.jpg",
        "tags": ["Cobertura", "Joinville", "Instalação"],
        "body": """
    <div class="tldr">
      <strong>Resposta rápida:</strong> a forma mais rápida de saber se tem fibra no seu endereço em Joinville é <strong>consultar a cobertura pelo CEP</strong> aqui no site. Você informa o CEP e o número, e o sistema confirma na hora se a rede já atende o local. Se ainda não chegou, dá pra registrar interesse para ser avisado quando a fibra expandir para a sua região.
    </div>

    <h2>Por que confirmar a cobertura primeiro</h2>
    <p>Internet fibra (FTTH) depende de a rede de fibra já passar pela sua rua. Mesmo em uma cidade bem atendida como Joinville, a expansão é por etapas, bairro a bairro. Confirmar a cobertura antes evita frustração e já adianta a contratação se estiver tudo certo.</p>

    <h2>Passo a passo para consultar pelo CEP</h2>
    <ol>
      <li><strong>Tenha o CEP e o número</strong> do imóvel em mãos. Não sabe o CEP? Dá pra buscar pelo nome da rua nos Correios.</li>
      <li><strong>Abra a consulta de cobertura</strong> da MasterInfo aqui no site (botão de cobertura/consulta de CEP).</li>
      <li><strong>Informe o CEP e o número</strong> e confirme. O sistema verifica a viabilidade técnica na hora.</li>
      <li><strong>Veja o resultado:</strong> se houver cobertura, você já escolhe o plano e segue para a contratação. Se não houver, registre seu contato para ser avisado quando a fibra chegar.</li>
    </ol>

    <h2>Tem cobertura: e agora?</h2>
    <p>Com a viabilidade confirmada, é só escolher o plano pelo seu perfil de uso. Se estiver em dúvida, o guia <a href="/blog/quantos-mega-de-internet-voce-precisa/">quantos Mega você precisa</a> ajuda a decidir. Depois é só contratar; a instalação é agendada e feita pela nossa equipe técnica local.</p>

    <h2>Ainda não tem fibra na minha rua</h2>
    <p>A rede da MasterInfo cresce constantemente em Joinville. Se o seu endereço ainda não estiver coberto, vale registrar seu interesse: assim você é avisado assim que a fibra expandir para a sua região. Enquanto isso, fale com a gente pelo <a href="/contato/">contato</a> para entender a previsão para o seu bairro.</p>

    <h2>Bairros atendidos</h2>
    <p>Já levamos fibra para boa parte da cidade, incluindo Centro, América, Glória, Bom Retiro, Boa Vista, Vila Nova, Costa e Silva e Iririú, entre outros. Veja todas as opções no guia de <a href="/internet-joinville/">internet em Joinville</a>.</p>
""",
        "faq": [
            ("Como sei se tem fibra no meu endereço?", "Consulte a cobertura pelo CEP aqui no site: informe o CEP e o número do imóvel e o sistema confirma na hora se a rede de fibra já atende o local."),
            ("Preciso pagar para consultar a cobertura?", "Não. A consulta de cobertura por CEP é gratuita e leva poucos segundos."),
            ("E se ainda não tiver fibra na minha rua?", "Você pode registrar seu interesse para ser avisado quando a fibra expandir para a sua região. A rede da MasterInfo cresce constantemente em Joinville."),
            ("Quanto tempo leva a instalação depois de confirmar a cobertura?", "Após confirmar a viabilidade e contratar, a instalação é agendada para os próximos dias úteis e feita pela equipe técnica local da MasterInfo."),
        ],
    },
    {
        "slug": "como-melhorar-wifi-em-casa",
        "title": "Wi-Fi Lento ou Caindo? Como Melhorar o Sinal em Casa",
        "desc": "Wi-Fi lento, travando ou com ponto cego? Veja dicas práticas para melhorar o sinal em casa: posição do roteador, canais, senha e quando usar mesh.",
        "h1": "Wi-Fi lento ou caindo? Como melhorar o sinal em casa",
        "lead": "Às vezes a internet é boa, mas o Wi-Fi não chega direito em todo canto da casa. A maioria dos problemas se resolve com ajustes simples. Veja o que fazer antes de chamar o suporte.",
        "author": "tecnica",
        "date": DATE_DEFAULT,
        "image": "/imgs/hero/sub/2-roteadores-2.jpg",
        "tags": ["Wi-Fi", "Dicas", "Suporte"],
        "body": """
    <div class="tldr">
      <strong>Resposta rápida:</strong> a maioria dos problemas de Wi-Fi vem de <strong>posição ruim do roteador</strong>. Coloque-o num ponto <strong>central e alto</strong>longe de paredes grossas, micro-ondas e espelhos. Reinicie quando travar, mantenha a senha protegida e, em casas grandes, use <strong>2 roteadores em mesh</strong>. Se nada resolver, fale com o suporte.
    </div>

    <h2>1. Posicione bem o roteador</h2>
    <p>É a dica que mais resolve. O roteador deve ficar num lugar <strong>central</strong> da casa e <strong>elevado</strong> (em cima de um móvel, não no chão nem dentro do armário). Evite deixá-lo atrás da TV, perto do micro-ondas ou colado em paredes grossas e espelhos, que bloqueiam o sinal.</p>

    <h2>2. Reinicie quando travar</h2>
    <p>Se a internet ficou lenta do nada, tire o roteador da tomada por 30 segundos e ligue de novo. Isso resolve a maioria das lentidões momentâneas, é o famoso "desliga e liga".</p>

    <h2>3. Use a rede de 5 GHz para o que importa</h2>
    <p>Roteadores modernos têm duas redes: <strong>2,4 GHz</strong> (alcança mais longe, porém mais lenta) e <strong>5 GHz</strong> (mais rápida, alcance menor). Conecte os aparelhos que precisam de velocidade (TV, PC, celular principal) no 5 GHz quando estiver perto do roteador.</p>

    <h2>4. Proteja sua senha</h2>
    <p>Wi-Fi aberto ou com senha fraca pode estar sendo usado por vizinhos, o que deixa tudo lento. Use uma senha forte e troque periodicamente. O passo a passo está na página <a href="/ajuda/wifi/">como configurar seu Wi-Fi</a>.</p>

    <h2>5. Casa grande? Pense em mesh (2 roteadores)</h2>
    <p>Um único roteador não cobre bem sobrados, casas grandes e quintais. A solução é a rede <strong>mesh</strong>: dois roteadores trabalhando juntos, com o celular trocando de um para o outro sem cair. Veja a <a href="/com-2-roteadores/">internet com 2 roteadores</a>.</p>

    <h2>6. Confirme se o problema é o Wi-Fi ou o plano</h2>
    <p>Faça um teste de velocidade <strong>conectado por cabo</strong> ou bem perto do roteador. Se a velocidade vier boa por cabo mas ruim no Wi-Fi distante, o problema é cobertura do Wi-Fi (resolve com posição/mesh). Se vier ruim em tudo, pode ser o plano ou algo a verificar; nesse caso, veja <a href="/blog/quantos-mega-de-internet-voce-precisa/">quantos Mega você precisa</a> ou fale com o suporte.</p>

    <h2>Quando chamar o suporte</h2>
    <p>Se você já ajustou a posição, reiniciou e testou por cabo, e mesmo assim a internet cai ou vem lenta, é hora de acionar a gente. Abra um chamado em <a href="/ajuda/reportar/">reportar um problema</a> ou fale no WhatsApp. Nossa equipe local resolve rápido.</p>
""",
        "faq": [
            ("Por que meu Wi-Fi é lento em alguns cômodos?", "Geralmente por causa da posição do roteador e de obstáculos como paredes grossas, espelhos e o micro-ondas. Colocar o roteador num ponto central e alto resolve boa parte dos casos; casas grandes pedem 2 roteadores em mesh."),
            ("Reiniciar o roteador ajuda?", "Sim. Tirar o roteador da tomada por 30 segundos e religar resolve a maioria das lentidões momentâneas. É a primeira coisa a tentar."),
            ("Qual a diferença entre as redes 2,4 GHz e 5 GHz?", "A 2,4 GHz alcança mais longe, mas é mais lenta; a 5 GHz é mais rápida, com alcance menor. Use a 5 GHz nos aparelhos que precisam de velocidade e estão perto do roteador."),
            ("Testei e a internet está lenta até por cabo, o que faço?", "Se a velocidade vem ruim até conectado por cabo, pode não ser o Wi-Fi. Verifique se o plano atende seu uso e, se persistir, fale com o suporte da MasterInfo para avaliarmos a conexão."),
        ],
    },
    # ─── ONDA 2 ───
    {
        "slug": "internet-caiu-o-que-fazer",
        "title": "A Internet Caiu? Passo a Passo para Voltar a Conectar",
        "desc": "Internet caiu ou sem conexão? Veja um passo a passo simples para resolver: checar luzes do roteador, reiniciar, testar por cabo e quando chamar o suporte.",
        "h1": "A internet caiu? Passo a passo para voltar a conectar",
        "lead": "Antes de achar que é problema grande, a maioria das quedas se resolve em minutos com alguns passos simples. Veja o que fazer na ordem certa e quando acionar o suporte.",
        "author": "tecnica",
        "date": DATE_DEFAULT,
        "image": "/imgs/hero/sub/2-roteadores-3.jpg",
        "tags": ["Suporte", "Wi-Fi"],
        "body": """
    <div class="tldr">
      <strong>Resposta rápida:</strong> 1) confira as <strong>luzes do roteador</strong> (a de internet/PON precisa estar acesa e fixa); 2) <strong>reinicie</strong> o roteador (tire da tomada 30 segundos e religue); 3) teste <strong>por cabo</strong> e em outro aparelho; 4) se as luzes estiverem anormais ou nada resolver, <strong>fale com o suporte</strong>. Em Joinville, nossa equipe é local e resolve rápido.
    </div>

    <h2>1. Olhe as luzes do roteador</h2>
    <p>O roteador conta muita coisa pelas luzes. A luz de <strong>Power</strong> deve estar acesa; a de <strong>internet/PON/LOS</strong> (fibra) precisa estar acesa e estável. Se a luz LOS estiver <strong>vermelha ou piscando</strong>costuma indicar problema no sinal da fibra, algo que o suporte precisa verificar. Se tudo está apagado, confira se o aparelho está na tomada e ligado.</p>

    <h2>2. Reinicie o roteador (resolve a maioria)</h2>
    <p>Parece clichê, mas funciona: <strong>tire o roteador da tomada, espere 30 segundos e ligue de novo</strong>. Aguarde 1 a 2 minutos até as luzes estabilizarem. Esse "desliga e liga" resolve boa parte das quedas e lentidões momentâneas.</p>

    <h2>3. Teste por cabo e em outro aparelho</h2>
    <p>Para saber se o problema é a internet ou só o Wi-Fi, conecte um computador <strong>por cabo</strong> ao roteador. Se funcionar por cabo mas não no Wi-Fi, o problema é a rede sem fio (veja <a href="/blog/como-melhorar-wifi-em-casa/">como melhorar o Wi-Fi em casa</a>). Teste também em outro celular: se só um aparelho está sem internet, o problema pode ser nele.</p>

    <h2>4. Verifique se é só na sua casa</h2>
    <p>Às vezes a queda é momentânea e regional. Se possível, pergunte a um vizinho que também é cliente. Isso ajuda a equipe a identificar mais rápido se é algo pontual no seu imóvel ou na rede.</p>

    <h2>5. Ainda sem internet? Fale com a gente</h2>
    <p>Se as luzes estão anormais (LOS vermelha) ou nada resolveu, é hora de acionar o suporte. Abra um chamado em <a href="/ajuda/reportar/">reportar um problema</a> ou chame no WhatsApp. Tenha em mãos o que você já testou e os horários em que cai, isso acelera muito o atendimento. Por sermos um provedor <a href="/internet-joinville/">local de Joinville</a>o suporte é com gente da região.</p>
""",
        "faq": [
            ("Por que minha internet cai sozinha?", "As causas mais comuns são roteador precisando reiniciar, Wi-Fi com interferência, ou oscilação no sinal da fibra. Comece reiniciando o roteador e testando por cabo; se persistir ou a luz LOS ficar vermelha, fale com o suporte."),
            ("O que significa a luz vermelha (LOS) no roteador?", "A luz LOS vermelha ou piscando geralmente indica que o sinal da fibra não está chegando corretamente ao aparelho. Reinicie uma vez; se continuar vermelha, acione o suporte para verificar."),
            ("Reiniciar o roteador resolve mesmo?", "Sim, na maioria dos casos. Tire da tomada por 30 segundos e religue, aguardando as luzes estabilizarem. Resolve boa parte das quedas e lentidões momentâneas."),
            ("Como falo com o suporte da MasterInfo?", "Pelo WhatsApp ou pela página de reportar um problema. Informe o que já testou e os horários das quedas; nossa equipe local de Joinville resolve rápido."),
        ],
    },
    {
        "slug": "como-funciona-instalacao-da-fibra",
        "title": "Como Funciona a Instalação da Fibra (e Quanto Tempo Leva)",
        "desc": "Vai contratar fibra? Veja como funciona a instalação passo a passo, quanto tempo leva, o que o técnico faz e como deixar tudo pronto para o dia.",
        "h1": "Como funciona a instalação da fibra (e quanto tempo leva)",
        "lead": "Contratou e ficou na dúvida sobre o dia da instalação? Veja o que acontece, quanto tempo costuma levar e como deixar tudo pronto para a equipe.",
        "author": "tecnica",
        "date": DATE_DEFAULT,
        "image": "/imgs/historia/momento-time-tecnico.jpg",
        "tags": ["Instalação", "Cobertura"],
        "body": """
    <div class="tldr">
      <strong>Resposta rápida:</strong> depois de confirmar a <strong>cobertura</strong> e contratar, a instalação é <strong>agendada</strong> e feita pela equipe técnica local. No dia, o técnico passa o <strong>cabo de fibra</strong> até o imóvel, instala o equipamento (ONU/roteador), configura o Wi-Fi e testa a velocidade. Costuma levar <strong>de 1 a 2 horas</strong>.
    </div>

    <h2>Antes da instalação: confirme a cobertura</h2>
    <p>O primeiro passo é confirmar que a fibra já atende o seu endereço. Dá para checar em segundos pelo CEP (veja <a href="/blog/cobertura-fibra-cep-joinville/">como saber se tem fibra no seu endereço</a>). Com a viabilidade confirmada e o plano escolhido, a instalação é agendada para os próximos dias úteis.</p>

    <h2>O que o técnico faz no dia</h2>
    <ol>
      <li><strong>Passa o cabo de fibra</strong> da rede até a sua casa ou apartamento.</li>
      <li><strong>Instala o equipamento</strong> (a ONU/roteador) num ponto adequado do imóvel.</li>
      <li><strong>Configura o Wi-Fi</strong> (nome da rede e senha) e orienta sobre o uso.</li>
      <li><strong>Testa a velocidade</strong> para garantir que está tudo entregando como contratado.</li>
    </ol>

    <h2>Quanto tempo leva</h2>
    <p>A instalação costuma levar <strong>de 1 a 2 horas</strong>dependendo do imóvel e do trajeto do cabo. Apartamentos com infraestrutura pronta tendem a ser mais rápidos; casas grandes ou trajetos mais longos podem levar um pouco mais.</p>

    <h2>Como se preparar</h2>
    <ul>
      <li>Tenha em mente <strong>onde quer o roteador</strong> (de preferência num ponto central e alto, para o Wi-Fi pegar bem; veja <a href="/blog/como-melhorar-wifi-em-casa/">dicas de Wi-Fi</a>).</li>
      <li>Garanta que haja <strong>uma tomada</strong> perto desse ponto.</li>
      <li>Deixe o acesso livre para o técnico passar o cabo.</li>
    </ul>

    <h2>Depois de instalado</h2>
    <p>Com tudo pronto, é só conectar seus aparelhos. Se quiser tirar o máximo do plano, vale escolher o pacote certo para o seu uso, veja <a href="/blog/quantos-mega-de-internet-voce-precisa/">quantos Mega você precisa</a> ou conheça os planos em <a href="/internet-joinville/">internet em Joinville</a>.</p>
""",
        "faq": [
            ("Quanto tempo leva a instalação da fibra?", "Normalmente de 1 a 2 horas, dependendo do imóvel e do trajeto do cabo. Apartamentos com infraestrutura pronta costumam ser mais rápidos."),
            ("Preciso estar em casa na instalação?", "Sim, é necessário que um responsável esteja no local para liberar o acesso, indicar onde instalar o roteador e receber as orientações."),
            ("A instalação tem custo?", "Depende do plano e da promoção vigente. Confirme as condições ao contratar; muitas vezes há instalação facilitada. Fale com a gente para os detalhes do seu caso."),
            ("Em quanto tempo consigo agendar?", "Após confirmar a cobertura e contratar, a instalação costuma ser agendada para os próximos dias úteis, conforme a disponibilidade da equipe."),
        ],
    },
    {
        "slug": "internet-para-empresas-o-que-considerar",
        "title": "Internet para Empresas: o que Considerar Antes de Contratar",
        "desc": "Vai contratar internet para a sua empresa? Veja os pontos que importam: banda garantida, upload, IP fixo, SLA e suporte, e como escolher entre link dedicado e banda larga.",
        "h1": "Internet para empresas: o que considerar antes de contratar",
        "lead": "Internet de empresa não é igual à de casa. Antes de fechar, veja os critérios que evitam dor de cabeça e mantêm seu negócio sempre online.",
        "author": "philipe",
        "date": DATE_DEFAULT,
        "image": "/imgs/hero/sub/empresarial-1.jpg",
        "tags": ["Empresas"],
        "body": """
    <div class="tldr">
      <strong>Resposta rápida:</strong> para empresa, priorize <strong>banda garantida</strong><strong>upload alto (simétrico)</strong><strong>IP fixo</strong><strong>SLA</strong> e <strong>suporte prioritário</strong>. Para operações que não podem parar, o <strong>link dedicado</strong> supera a banda larga comum. Veja a <a href="/internet-empresarial/">internet empresarial da MasterInfo</a> em Joinville.
    </div>

    <h2>1. Banda garantida x compartilhada</h2>
    <p>A internet residencial é compartilhada e pode oscilar nos horários de pico. Para empresa, o ideal é <strong>banda garantida</strong> (link dedicado): a capacidade contratada é sua, de ponta a ponta, sem cair quando o bairro inteiro está usando.</p>

    <h2>2. Upload tão importante quanto download</h2>
    <p>Empresas mandam tanto quanto recebem: backup em nuvem, videoconferência, sistemas ERP, envio de arquivos. Por isso o <strong>upload simétrico</strong> (igual ao download) faz muita diferença, algo que a banda larga comum raramente entrega.</p>

    <h2>3. IP fixo</h2>
    <p>Se a empresa usa servidores, câmeras, VPN, ponto eletrônico ou acesso remoto, vai precisar de <strong>IP fixo</strong>. É um item que a maioria dos planos residenciais não oferece.</p>

    <h2>4. SLA e suporte prioritário</h2>
    <p>O <strong>SLA</strong> (acordo de nível de serviço) define o compromisso de disponibilidade e tempo de resposta. Junto com um <strong>suporte prioritário e local</strong>é o que garante que, se algo acontecer, sua empresa volte rápido. Provedor regional ajuda aqui: equipe na cidade resolve mais rápido que um call center distante.</p>

    <h2>5. Escalabilidade</h2>
    <p>Sua empresa vai crescer. Vale escolher um provedor que permita <strong>aumentar a banda</strong> conforme a demanda, sem precisar trocar tudo.</p>

    <h2>Link dedicado ou banda larga?</h2>
    <p>Se a internet é crítica para o seu negócio (atendimento online, sistemas em nuvem, muitos pagamentos), o <strong>link dedicado</strong> compensa. Para uso mais leve, uma banda larga empresarial pode bastar. Na dúvida, fale com nosso time comercial pelo <a href="https://wa.me/5547989212991">WhatsApp (47) 98921-2991</a> ou conheça a <a href="/internet-empresarial/">internet empresarial</a>.</p>
""",
        "faq": [
            ("Qual a diferença entre internet de empresa e residencial?", "A de empresa prioriza banda garantida, upload simétrico, IP fixo, SLA e suporte prioritário. A residencial é compartilhada e assimétrica, ótima para casa, mas sem garantia de banda nos horários de pico."),
            ("Minha empresa precisa de link dedicado?", "Se a internet é crítica (sistemas em nuvem, videoconferência constante, muitos pagamentos, câmeras), sim. Para uso mais leve, uma banda larga empresarial pode ser suficiente."),
            ("Internet empresarial tem IP fixo?", "Sim, o link dedicado empresarial inclui IP fixo, necessário para servidores, VPN, câmeras e acesso remoto."),
            ("Como peço uma proposta para minha empresa?", "Pelo WhatsApp comercial (47) 98921-2991 ou pela página de internet empresarial. Montamos a proposta conforme a banda e a estrutura que sua empresa precisa em Joinville."),
        ],
    },
    {
        "slug": "sky-light-playhub-como-funciona",
        "title": "SKY+ Light e os Apps Inclusos: Como Funciona o PlayHub",
        "desc": "Entenda o PlayHub da MasterInfo: como funciona o SKY+ Light e os apps de TV e streaming inclusos no seu plano de internet fibra em Joinville.",
        "h1": "SKY+ Light e os apps inclusos: como funciona o PlayHub",
        "lead": "Seu plano de fibra pode vir com TV ao vivo e apps de streaming inclusos. Entenda como o PlayHub funciona e como escolher o seu app todo mês.",
        "author": "equipe",
        "date": DATE_DEFAULT,
        "image": "/imgs/hero/banner-aplicativos.png",
        "tags": ["Apps", "TV e Streaming"],
        "body": """
    <div class="tldr">
      <strong>Resposta rápida:</strong> o <strong>PlayHub</strong> é o catálogo de apps de TV e streaming inclusos nos planos da MasterInfo. Cada plano libera uma <strong>categoria</strong> (Standard, Advanced, TOP ou Premium) e você <strong>escolhe 1 app por mês</strong> dentro dela, como o <a href="/aplicativos/sky-light/">SKY+ Light</a> (TV ao vivo). Veja tudo em <a href="/playhub/">PlayHub</a>.
    </div>

    <h2>O que é o SKY+ Light</h2>
    <p>O <strong>SKY+ Light</strong> é TV ao vivo no celular, na smart TV ou no computador, sem antena e sem parabólica. Canais de esporte, jornalismo, novelas e mais, onde você estiver. É um dos apps que vêm inclusos no seu plano de fibra.</p>

    <h2>Como funciona o PlayHub</h2>
    <p>Em vez de um pacote fixo, a MasterInfo trabalha com o <strong>PlayHub</strong>: um conjunto de apps organizados em categorias. O seu plano libera uma categoria, e <strong>todo mês você escolhe 1 app</strong> dentro dela. Quer assistir TV ao vivo num mês e trocar por outro app no mês seguinte? Pode.</p>

    <h2>As categorias</h2>
    <ul>
      <li><strong>Standard</strong>: apps de entrada (ex.: SKY+ Light).</li>
      <li><strong>Advanced</strong>: catálogo maior, com mais opções.</li>
      <li><strong>TOP</strong> e <strong>Premium</strong>: os pacotes mais completos, com os principais apps de streaming.</li>
    </ul>
    <p>Quanto mais alto o plano, mais completa a categoria liberada. Veja quais apps estão em cada uma na página do <a href="/playhub/">PlayHub</a>.</p>

    <h2>Como escolher seu app</h2>
    <p>Depois de contratar, você ativa o app da sua categoria pelos canais da MasterInfo. A troca mensal dá flexibilidade para acompanhar o que você mais quer assistir em cada época.</p>

    <h2>Qual plano combina com você</h2>
    <p>Se a casa consome muito streaming, vale um plano com categoria mais alta. Em dúvida sobre velocidade, veja <a href="/blog/quantos-mega-de-internet-voce-precisa/">quantos Mega você precisa</a> ou conheça os planos em <a href="/internet-joinville/">internet em Joinville</a>.</p>
""",
        "faq": [
            ("O que é o PlayHub da MasterInfo?", "É o catálogo de apps de TV e streaming inclusos nos planos. Cada plano libera uma categoria (Standard, Advanced, TOP ou Premium) e você escolhe 1 app por mês dentro dela."),
            ("O SKY+ Light está incluso no plano?", "Sim, o SKY+ Light faz parte do PlayHub. Dependendo da categoria do seu plano, ele é uma das opções que você pode escolher."),
            ("Posso trocar de app todo mês?", "Sim. O PlayHub permite escolher 1 app por mês dentro da categoria do seu plano, dando flexibilidade para variar conforme o que você quer assistir."),
            ("Preciso de antena para o SKY+ Light?", "Não. O SKY+ Light é TV ao vivo pela internet, no celular, smart TV ou computador, sem antena e sem parabólica."),
        ],
    },
    {
        "slug": "segunda-via-de-boleto-masterinfo",
        "title": "2ª Via de Boleto da MasterInfo: Como Emitir e Pagar",
        "desc": "Precisa da 2ª via do boleto da MasterInfo? Veja como emitir a segunda via, consultar faturas e pagar por boleto, Pix ou cartão pela Central do Assinante.",
        "h1": "2ª via de boleto da MasterInfo: como emitir e pagar",
        "lead": "Perdeu o boleto ou quer adiantar o pagamento? Veja como acessar a 2ª via, consultar suas faturas e pagar do jeito que preferir.",
        "author": "equipe",
        "date": DATE_DEFAULT,
        "image": "/imgs/historia/momento-atendimento.jpg",
        "tags": ["Financeiro", "Suporte"],
        "body": """
    <div class="tldr">
      <strong>Resposta rápida:</strong> a 2ª via do boleto é emitida na <strong>Central do Assinante</strong> com o seu login: você baixa o boleto, copia o código de barras e paga por <strong>boleto, Pix ou cartão</strong>. Precisa de ajuda na hora? Use o chat de boletos da <a href="/ajuda/boletos/">página de boletos</a>.
    </div>

    <h2>Como emitir a 2ª via</h2>
    <ol>
      <li>Acesse a <strong>Central do Assinante</strong> com o seu login.</li>
      <li>Vá em <strong>faturas/boletos</strong> e localize a fatura em aberto.</li>
      <li><strong>Baixe a 2ª via</strong> ou copie o <strong>código de barras / Pix</strong> para pagar na hora.</li>
    </ol>
    <p>Se preferir, o chat de boletos na <a href="/ajuda/boletos/">página de boletos</a> ajuda você a localizar a fatura rapidamente.</p>

    <h2>Formas de pagamento</h2>
    <p>Você paga como for melhor: <strong>boleto</strong><strong>Pix</strong> (na hora, sem espera de compensação) ou <strong>cartão</strong>. Pagando em dia, você garante o desconto do seu plano.</p>

    <h2>Consultar faturas e vencimento</h2>
    <p>Na Central do Assinante dá para ver faturas anteriores, datas de vencimento e os pagamentos já feitos, tudo num lugar só, quando você quiser.</p>

    <h2>Dúvidas sobre a fatura</h2>
    <p>Se algo não bater ou você tiver dúvida sobre uma cobrança, fale com a gente. Por sermos um provedor local de <a href="/internet-joinville/">Joinville</a>o atendimento é com gente da região e resolve rápido.</p>
""",
        "faq": [
            ("Como tiro a 2ª via do boleto da MasterInfo?", "Acesse a Central do Assinante com seu login, vá em faturas/boletos e baixe a 2ª via ou copie o código de barras/Pix. O chat de boletos no site também ajuda a localizar a fatura."),
            ("Posso pagar por Pix?", "Sim. Você pode pagar por boleto, Pix ou cartão. O Pix cai na hora, sem espera de compensação."),
            ("Onde consulto faturas anteriores?", "Na Central do Assinante, onde ficam as faturas, datas de vencimento e o histórico de pagamentos."),
            ("Tenho desconto pagando em dia?", "Sim. Pagando em dia você garante o desconto do seu plano. Os valores aparecem na sua fatura."),
        ],
    },
]


# Conteúdo aprofundado das personas (corpo editorial + FAQ), gerado por workflow e revisado (adversarial) em 2026-06-22.
PERSONAS_CONTENT = {
 "gamer": {
  "lead": "Fibra dedicada, ping estável e suporte local: o que um gamer em Joinville precisa saber antes de escolher o plano certo.",
  "body": "<h2>Por que a conexão faz diferença no jogo, e onde a maioria erra</h2>\n<p>Velocidade alta não é o mesmo que conexão boa para jogos. Um plano de 200 Mega via rádio ou cabo coaxial compartilhado pode funcionar bem para streaming, mas travar num raid ou te dar kill-lag em partida ranqueada. O que importa para quem joga online é outra lista: <strong>ping baixo, jitter estável e zero perda de pacote</strong>. Esses três dependem muito mais do tipo de infraestrutura do que do número de Mega no contrato.</p>\n<p>A Masterinfo usa fibra óptica FTTH, a fibra chega até dentro da sua casa, sem trecho de rádio no meio do caminho e sem compartilhar cabo coaxial com o quarteirão. Isso reduz a variação de latência que aparece especialmente nos horários de pico, quando vizinhos estão assistindo séries ao mesmo tempo que você está numa partida decisiva.</p>\n<p>Se quiser entender a diferença técnica entre os tipos de conexão disponíveis em Joinville, o artigo <a href=\"/blog/fibra-vs-radio-vs-cabo/\">fibra vs rádio vs cabo</a> detalha cada um sem enrolação.</p>\n\n<h2>O que um gamer precisa checar na hora de contratar</h2>\n<p>Antes de fechar qualquer plano, vale revisar quatro pontos:</p>\n<ul>\n  <li><strong>Tipo de fibra:</strong> confirme que é FTTH (fibra até a casa), não FTTB (fibra até o prédio e cabo até o apartamento) nem rádio no último trecho.</li>\n  <li><strong>Roteador compatível:</strong> Wi-Fi 5 (802.11ac) já entrega velocidade, mas Wi-Fi 6 (802.11ax) reduz latência por ar em ambientes com vários dispositivos conectados ao mesmo tempo. O plano <a href=\"/gamer/\">Ultra Gamer</a> já inclui mesh Wi-Fi 6 com cobertura total.</li>\n  <li><strong>Cobertura dentro de casa:</strong> paredes de concreto e distância do roteador aumentam latência via Wi-Fi. Para casa maior ou sobrado, uma solução <a href=\"/com-2-roteadores/\">com 2 roteadores em mesh</a> garante sinal consistente em todos os cômodos.</li>\n  <li><strong>Suporte quando cai:</strong> jogo cancelado por queda de conexão é diferente de série pausada. Equipe local responde mais rápido que central 0800 de outra cidade. A Masterinfo atende por WhatsApp com equipe em Joinville.</li>\n</ul>\n\n<h2>ExitLag e otimizadores de rota: o que a Masterinfo faz e o que é por conta do jogador</h2>\n<p>O ExitLag é um software que redireciona o tráfego do seu jogo por rotas mais rápidas até os servidores da game company, independente da operadora. Ele funciona em cima da sua conexão, não substitui a qualidade dela. Com uma fibra ruim, o ExitLag melhora, mas não resolve. Com uma fibra estável como FTTH, você começa de um ponto mais sólido e o ExitLag entrega mais resultado.</p>\n<p>O plano <a href=\"/gamer/\">Ultra Gamer</a> já inclui o ExitLag entre os recursos, e a Masterinfo não bloqueia VPN ou otimizadores de rota. O tráfego chega até o seu roteador sem restrição de protocolo.</p>\n\n<h2>Gamer também faz live, assiste e divide a conexão</h2>\n<p>Se você transmite partidas na Twitch ou YouTube, a velocidade de upload importa tanto quanto o download. Com 1 Giga de fibra dedicada, há banda de sobra para transmitir sem comprometer a partida em outra tela, mas o upload exato varia por infraestrutura local, então vale confirmar no momento do cadastro.</p>\n<p>E se a família divide o plano, alguém assistindo streaming em 4K, outro numa call de trabalho, você numa ranked, 1 Giga de fibra dedicada distribui sem degradar a qualidade de cada um. Veja como funciona para <a href=\"/familia/\">famílias com múltiplos usuários</a>.</p>\n<p>Para quem joga e trabalha em home office no mesmo dia, o <a href=\"/home-office/\">plano Home Office</a> também é uma opção a avaliar dependendo do perfil de uso.</p>\n<p>Se quer a melhor estrutura disponível para jogar online em Joinville, mesh Wi-Fi 6, ExitLag incluso, instalação em até 3 dias e suporte local por WhatsApp, o plano é este: <a href=\"/checkout.html?plano=ultra-gamer\"><strong>contratar o Ultra Gamer</strong></a>.</p>",
  "faq": [
   {
    "q": "Qual o ping que posso esperar com a Masterinfo em Joinville?",
    "a": "O ping depende principalmente de onde ficam os servidores do jogo. Servidores brasileiros, como os da AWS São Paulo usados por Riot e Epic, costumam marcar entre 10 ms e 30 ms em fibra FTTH; é uma estimativa típica de mercado, não uma garantia contratual. Ping para servidores nos EUA fica em torno de 100 ms ou mais, o que é limitação de distância física, não da operadora. O que a fibra FTTH contribui de verdade é estabilidade: menos variação entre uma medição e outra, sem picos repentinos nos horários de pico."
   },
   {
    "q": "O ExitLag funciona normalmente com a conexão da Masterinfo?",
    "a": "Sim. O ExitLag já vem incluso no plano Ultra Gamer, e a Masterinfo não bloqueia VPN, otimizadores de rota ou softwares similares como Mudfish ou WTFast. O tráfego sai do seu dispositivo sem restrição de protocolo. O ExitLag funciona sobre qualquer conexão, fibra FTTH oferece a base mais estável para que o software entregue o máximo de resultado."
   },
   {
    "q": "É melhor jogar via cabo (Ethernet) ou Wi-Fi 6 com a Masterinfo?",
    "a": "Cabo Ethernet sempre entrega latência ligeiramente menor e zero interferência por ar, é o ideal para PC de mesa em ranked competitivo. Wi-Fi 6 é uma boa alternativa para quem joga no notebook, console ou não quer passar cabo, especialmente em ambientes sem muitas paredes ou com poucos dispositivos concorrendo pelo canal. Para casa grande, a solução com 2 roteadores em mesh Wi-Fi 6 é melhor do que um único ponto com sinal fraco no quarto."
   },
   {
    "q": "Quanto tempo demora a instalação da Masterinfo?",
    "a": "A instalação é feita em até 3 dias úteis após a contratação, com equipe própria de Joinville. Por ser FTTH, o técnico passa o cabo de fibra óptica até dentro da sua casa, não tem instalação remota nem roteador sem configuração. Se tiver algum problema após a ativação, o suporte é por WhatsApp com a mesma equipe local."
   }
  ]
 },
 "familia": {
  "lead": "Fibra óptica que aguenta tablet de criança, streaming na TV, home office e jogo online, tudo ao mesmo tempo, sem ninguém reclamar de lentidão.",
  "body": "<h2>Quantos aparelhos a sua casa usa de verdade?</h2>\n<p>Pense num fim de tarde normal: as crianças no tablet assistindo YouTube ou Disney+, a TV da sala com GloboPlay no ar, você em uma videochamada do trabalho e o adolescente no quarto em algum jogo online. São facilmente cinco a oito aparelhos ativos ao mesmo tempo, e todos precisando de conexão boa, agora.</p>\n<p>É exatamente nessa hora que a qualidade da internet aparece. Com fibra óptica até a casa (FTTH), o sinal não é compartilhado com outros vizinhos da rua, não depende de clima e tende a variar menos no horário de pico. A conexão que você contrata é a que chega até o seu roteador, sem divisão com a rua.</p>\n<p>Se quiser entender melhor quantos Mega a sua família realmente precisa, temos um guia prático: <a href=\"/blog/quantos-mega-de-internet-voce-precisa/\">Quantos Mega de internet você precisa?</a></p>\n\n<h2>Wi-Fi forte na casa toda, não só perto do roteador</h2>\n<p>Velocidade alta na contratação não resolve se o sinal não chega no quarto do fundo ou no quintal. É um problema comum em casas maiores, de dois andares ou com paredes grossas.</p>\n<p>Os planos da MasterInfo já incluem <strong>Wi-Fi 6</strong>padrão com melhor gerenciamento de múltiplos aparelhos conectados ao mesmo tempo do que as gerações anteriores. Para casas onde um único roteador não cobre tudo, o plano <strong>com 2 roteadores</strong> forma uma rede Mesh: os dois aparelhos trabalham juntos e criam uma cobertura única, sem ponto cego.</p>\n<ul>\n  <li>Criança no quarto mais distante: sinal cheio, sem buffering.</li>\n  <li>TV na sala com streaming em alta definição: sem tela de carregamento no meio do episódio.</li>\n  <li>Notebook no escritório: videochamada estável durante o expediente.</li>\n  <li>Celular no quintal: conexão mantida sem cair para dados móveis.</li>\n</ul>\n<p>Veja como funciona a opção de <a href=\"/com-2-roteadores/\">internet com 2 roteadores</a> para cobertura Mesh na casa toda.</p>\n\n<h2>O que muda na prática com fibra dedicada</h2>\n<p>Muitos provedores entregam fibra até um ponto da rua e, depois, distribuem por cabo coaxial ou rádio entre os clientes do bairro. Isso divide a banda disponível entre vizinhos e é por isso que a internet fica mais lenta quando todo mundo chega em casa ao mesmo tempo.</p>\n<p>A MasterInfo usa <strong>fibra óptica direto até a casa</strong> (FTTH puro), sem cabo coaxial compartilhado nem rádio. Cada cliente tem o seu próprio trajeto de fibra. Se quiser entender a diferença técnica de forma simples, o post <a href=\"/blog/fibra-vs-radio-vs-cabo/\">Fibra vs Rádio vs Cabo</a> explica o que muda no dia a dia.</p>\n<p>Para a família, isso significa que a velocidade contratada fica disponível mesmo quando o bairro está com alta demanda, como num feriado ou fim de semana chuvoso.</p>\n\n<h2>Qual plano faz sentido para a sua família?</h2>\n<p>Para famílias com vários aparelhos ativos e consumo intenso de streaming, o <strong>Plano Ultra Família</strong> é o mais indicado: velocidade para todos ao mesmo tempo, Wi-Fi 6 incluso e possibilidade de expandir para dois roteadores Mesh sem trocar o plano. O suporte é feito por uma equipe aqui em Joinville, via WhatsApp, sem fila de 0800.</p>\n<p>Se a casa tem menos aparelhos simultâneos ou o uso é mais casual, o <strong>Plano Lite Premium</strong> cobre streaming em HD, tablets e navegação no dia a dia sem apertar.</p>\n<p>Instalação em até 3 dias úteis após a confirmação de cobertura no seu endereço.</p>\n<p><a href=\"/checkout.html?plano=ultra-familia\"><strong>Ver o Plano Ultra Família e contratar</strong></a></p>",
  "faq": [
   {
    "q": "Quantos aparelhos conseguem ficar conectados ao mesmo tempo sem travar?",
    "a": "Depende do plano e do roteador. Com Wi-Fi 6 e o Plano Ultra Família, a rede gerencia múltiplos dispositivos simultaneamente com melhor distribuição de banda do que os padrões anteriores. Tablets, TVs em streaming, notebooks e celulares podem estar ativos ao mesmo tempo sem que um aparelho penalize o outro."
   },
   {
    "q": "A internet trava quando todo mundo chega em casa no final do dia?",
    "a": "Com fibra óptica até a casa (FTTH), o sinal não é compartilhado com outros clientes da rua. Isso reduz a variação de velocidade no horário de pico, porque a conexão é dedicada ao seu endereço e não dividida com os vizinhos."
   },
   {
    "q": "Preciso de dois roteadores, ou um já resolve?",
    "a": "Depende da planta e do tamanho da casa. Em ambientes mais abertos e compactos, um roteador Wi-Fi 6 costuma cobrir bem. Em casas maiores, de dois andares ou com muitas paredes, dois roteadores formando rede Mesh garantem sinal forte em todos os cômodos. A MasterInfo oferece as duas opções de instalação."
   },
   {
    "q": "A MasterInfo tem cobertura no meu bairro em Joinville?",
    "a": "A rede cobre boa parte de Joinville, mas o jeito mais rápido de confirmar é verificar a disponibilidade pelo seu endereço direto no site. Após a confirmação, a instalação é agendada em até 3 dias úteis."
   }
  ]
 },
 "home-office": {
  "lead": "Quem trabalha em casa sabe: uma reunião caindo no meio da apresentação custa mais do que a mensalidade de qualquer plano de internet.",
  "body": "<h2>O que derruba uma reunião não é a velocidade, é a instabilidade</h2>\n<p>Planos de rádio ou cabo coaxial aparecem bem no papel, mas dividem a banda com dezenas de vizinhos. Nas horas de pico, das 8h às 10h e das 18h às 21h, essa concorrência se traduz em travamentos no Google Meet, tela congelada no Zoom e upload de arquivos que demora o dobro.</p>\n<p>A MasterInfo usa fibra óptica dedicada até a porta da sua casa (FTTH), em Joinville. O sinal não passa por cabo coaxial compartilhado nem por rádio sujeito a interferência de chuva ou obstáculos. A banda contratada é sua, nas horas em que você mais precisa dela.</p>\n<p>Para entender a diferença entre as tecnologias disponíveis na cidade, vale ler <a href=\"/blog/fibra-vs-radio-vs-cabo/\">fibra vs rádio vs cabo, qual tecnologia escolher</a>.</p>\n\n<h2>Upload importa tanto quanto download para quem trabalha remoto</h2>\n<p>A maioria das pessoas olha só para o download. Mas home office exige upload constante: enviar arquivos para o cliente, compartilhar tela, fazer backup em nuvem, transmitir vídeo na chamada. Com fibra simétrica, upload e download andam juntos, sem gargalo na hora de enviar uma apresentação de 50 MB ou subir um relatório no Drive.</p>\n<p>Latência é outro ponto que muda o dia a dia. O atraso entre falar e ser ouvido em chamadas de vídeo, o \"delay\", depende da latência da conexão, não da velocidade em si. Fibra entrega latências consistentemente mais baixas do que rádio ou cabo coaxial, o que faz diferença real em reuniões com times internacionais ou clientes em outros estados.</p>\n\n<h2>Quantos Mega seu home office realmente precisa</h2>\n<p>A conta é simples: quanto mais gente e mais atividades simultâneas, mais banda você consome. Reunião em vídeo, compartilhamento de tela, backup em nuvem rodando em paralelo e mais alguém em casa usando streaming, tudo isso compete pela mesma conexão ao mesmo tempo.</p>\n<p>Para home office com uso intenso de nuvem e chamadas simultâneas, 1 Giga entrega folga de banda e estabilidade, mesmo com Wi-Fi 6 distribuindo sinal para notebook, celular e outros dispositivos. Se quiser entender melhor o consumo por atividade, veja <a href=\"/blog/quantos-mega-de-internet-voce-precisa/\">quantos Mega de internet você precisa</a>.</p>\n<p>Quem trabalha com mais de um monitor, videoconferência simultânea ou tem família em casa durante o expediente pode também considerar <a href=\"/com-2-roteadores/\">a opção com dois roteadores</a> para separar a rede do trabalho da rede doméstica.</p>\n\n<h2>Por que a instalação e o suporte locais fazem diferença no dia a dia</h2>\n<p>Quando a internet cai no meio do expediente, ligar para uma central em outro estado e ficar em fila de espera não é uma opção. A MasterInfo tem equipe técnica em Joinville, atende por WhatsApp e resolve chamados sem 0800 ou robô.</p>\n<p>A instalação é feita em até 3 dias, sem esperar semanas por uma visita técnica. O roteador Wi-Fi 6 já vem incluso no plano, sem taxa de aluguel separada.</p>\n<p>Se você trabalha em casa e precisa de uma conexão que não te deixa na mão, o plano <strong>Ultra Home Office</strong> foi pensado com essa prioridade. Veja todos os detalhes em <a href=\"/home-office/\">internet para home office em Joinville</a>.</p>\n<p style=\"margin-top:1.5rem\"><a href=\"/checkout.html?plano=ultra-home-office\"><strong>Ver plano Ultra Home Office e contratar</strong></a></p>",
  "faq": [
   {
    "q": "A internet fibra da MasterInfo cai durante chuva?",
    "a": "A fibra óptica não sofre interferência de chuva, trovada ou vento, ao contrário do rádio, que depende de sinal no ar. O cabo de fibra pode ser afetado por danos físicos (como uma queda de árvore na rua), mas não pela chuva em si."
   },
   {
    "q": "O plano inclui Wi-Fi 6 ou preciso comprar roteador separado?",
    "a": "Todos os planos MasterInfo já incluem roteador Wi-Fi 6. Não há taxa de aluguel mensal separada, o equipamento vem com a instalação."
   },
   {
    "q": "Qual a diferença entre o plano lite e o ultra-home-office para quem trabalha remoto?",
    "a": "O Ultra Home Office é voltado especificamente para uso profissional, com suporte técnico local prioritário via WhatsApp, sem fila de 0800. Se você tem reuniões críticas e não pode aguardar, esse plano é a escolha mais adequada. Para uso mais leve, os planos lite atendem bem, mas recomendamos confirmar qual velocidade se encaixa na sua rotina antes de contratar."
   },
   {
    "q": "Consigo instalar a MasterInfo no meu endereço em Joinville?",
    "a": "A cobertura depende da região. A forma mais rápida de confirmar é verificar a viabilidade pelo site, acesse a seção de cobertura na home e informe seu CEP ou endereço. A equipe retorna em até 24 horas."
   }
  ]
 }
}


# Corpos aprofundados de posts do blog (workflow + revisão adversarial, 2026-06-22). Mesclado em BLOG no gerador.
BLOG_DEEP = {
 "quantos-mega-de-internet-voce-precisa": {
  "body": "<div class=\"tldr\">\n  <strong>Resposta rápida:</strong> para 1 a 2 pessoas com uso comum, <strong>300 a 500 Mega</strong> resolvem. Família com vários aparelhos e streaming em 4K: <strong>600 a 800 Mega</strong>. Casa cheia, home office e jogos ao mesmo tempo: <strong>1 Giga</strong>. O que mais pesa não é o tipo de atividade, e sim <strong>quantos aparelhos usam a internet ao mesmo tempo</strong>.\n</div>\n\n<h2>O que define a velocidade ideal</h2>\n<p>Muita gente contrata um plano maior por causa de uma atividade específica, streaming em 4K, um jogo online, e continua sentindo lentidão. O motivo quase sempre é o mesmo: a conta não é por atividade, é por aparelho simultâneo. Uma casa onde só você assiste a uma série à noite tem exigências completamente diferentes de uma casa onde duas pessoas trabalham de manhã enquanto a TV passa desenho e o videogame baixa uma atualização de vários GB.</p>\n<p>A lógica é simples: <strong>some o consumo de cada aparelho ativo ao mesmo tempo</strong>. Esse total é a sua velocidade mínima real. Tudo abaixo disso vai travar em algum momento do dia.</p>\n\n<h2>Quanto cada atividade consome</h2>\n<p>Para montar essa conta, veja o consumo aproximado de cada atividade isolada:</p>\n<table class=\"article-table\">\n  <thead><tr><th>Atividade</th><th>Velocidade recomendada</th></tr></thead>\n  <tbody>\n    <tr><td>Redes sociais e navegação geral</td><td>5 a 10 Mega</td></tr>\n    <tr><td>Streaming de vídeo em HD (1080p)</td><td>10 a 15 Mega</td></tr>\n    <tr><td>Streaming em 4K (Netflix, YouTube 4K)</td><td>25 Mega por tela</td></tr>\n    <tr><td>Chamada de vídeo no trabalho (Zoom, Teams, Meet)</td><td>10 a 20 Mega</td></tr>\n    <tr><td>Jogos online</td><td>20 a 50 Mega (e ping baixo)</td></tr>\n    <tr><td>Download de jogos e arquivos grandes</td><td>quanto mais, mais rápido o download</td></tr>\n    <tr><td>Câmera de segurança em nuvem (por câmera)</td><td>5 a 10 Mega de upload</td></tr>\n  </tbody>\n</table>\n<p>Repare: nenhuma dessas atividades sozinha justifica 1 Giga. O número muda quando tudo isso acontece junto, em vários aparelhos.</p>\n\n<h2>Exemplo prático: a conta de uma família em domingo à tarde</h2>\n<p>Quatro pessoas em casa, horário de pico:</p>\n<ul>\n  <li>TV na sala assistindo a um filme em 4K: <strong>25 Mega</strong></li>\n  <li>Dois celulares no TikTok e Instagram: <strong>20 Mega</strong></li>\n  <li>Videogame de um adolescente jogando online: <strong>30 Mega</strong></li>\n  <li>Notebook baixando uma atualização em segundo plano: <strong>variável</strong></li>\n</ul>\n<p>Só nesses três usos simultâneos, a soma já é de <strong>75 Mega ativos</strong>. Um plano de 100 ou 200 Mega ficaria no limite; com 600 Mega, há margem suficiente para o download acontecer sem que alguém sinta diferença.</p>\n\n<h2>Recomendação por perfil</h2>\n\n<h3>Mora sozinho ou em casal</h3>\n<p>Com 1 a 2 pessoas e uso comum, redes sociais, streaming, uma chamada de vídeo ocasional, <strong>300 a 500 Mega</strong> são mais que suficientes. A velocidade dificilmente vai ser o problema; o Wi-Fi e a posição do roteador importam mais nesse perfil. Para apartamentos e casas pequenas, veja a opção de <a href=\"/com-1-roteador/\">internet para apartamento com 1 roteador</a>.</p>\n\n<h3>Família com vários aparelhos</h3>\n<p>Streaming em 4K, criança no tablet, celulares extras conectados ao longo do dia: <strong>600 a 800 Mega</strong> garantem tudo rodando sem disputas de banda. Esse é o perfil mais comum de queixa, \"a internet trava na hora do jantar\", e a causa quase sempre é que a soma dos aparelhos excede o plano contratado, não que o provedor esteja entregando menos. Conheça os planos da <a href=\"/familia/\">internet para a família</a>.</p>\n\n<h3>Home office</h3>\n<p>Trabalhar de casa tem uma exigência que vai além da velocidade de download: <strong>estabilidade e upload</strong>. Uma reunião de vídeo que cai no momento errado tem custo real, muito além do valor da mensalidade. Para quem tem videoconferências diárias e faz upload frequente de arquivos (apresentações, backups em nuvem, compartilhamento de tela em alta resolução), o recomendado é a partir de <strong>500 a 800 Mega em fibra óptica</strong>. A fibra faz diferença aqui porque a latência é consistente: sem as oscilações que tecnologias via rádio costumam apresentar em horários de pico. Veja os detalhes na página de <a href=\"/home-office/\">internet para home office</a>.</p>\n\n<h3>Gamer</h3>\n<p>Para jogos online, o número de Mega é o segundo fator mais relevante, o <strong>ping (latência)</strong> vem primeiro. Um jogo competitivo depende da velocidade de resposta entre o seu comando e o servidor; velocidade altíssima com ping alto ainda resulta em atraso nos momentos críticos. Em fibra óptica FTTH, a latência é naturalmente baixa e estável. Com isso resolvido, <strong>500 Mega a 1 Giga</strong> garantem baixar atualizações rapidamente e jogar enquanto o resto da casa usa a internet normalmente. Veja a <a href=\"/gamer/\">internet para gamer</a>.</p>\n\n<h3>Casa grande ou com vários moradores</h3>\n<p>Sobrado, casa com muitos cômodos ou república com vários moradores: além de <strong>800 Mega a 1 Giga</strong>o problema pode não ser o plano, mas a cobertura do Wi-Fi. Um único roteador posicionado mal não alcança o quarto dos fundos, a área de serviço ou o escritório no piso de cima. A solução é uma rede <a href=\"/com-2-roteadores/\">Wi-Fi com 2 roteadores em mesh</a>que elimina os pontos cegos sem sacrificar velocidade.</p>\n\n<h2>Quando mais Mega não resolve o problema</h2>\n<p>Antes de migrar de plano, vale confirmar que a lentidão não tem outra causa. Os casos mais frequentes:</p>\n<ul>\n  <li><strong>Posição do roteador:</strong> no armário atrás da TV, encostado na parede de concreto ou no chão, o sinal já chega enfraquecido antes de passar pelo cômodo. Mover o roteador para uma prateleira alta em ponto central faz mais diferença do que dobrar o plano.</li>\n  <li><strong>Frequência do Wi-Fi:</strong> roteadores modernos operam em 2,4 GHz (mais alcance, menos velocidade) e 5 GHz (mais velocidade, menos alcance). Aparelhos longe do roteador ficam presos no 2,4 GHz. A solução não é contratar mais Mega, é melhorar a distribuição do sinal.</li>\n  <li><strong>Aparelhos consumindo em segundo plano:</strong> smart TVs atualizando apps, consoles baixando patches, celulares fazendo backup automático, tudo isso consome banda sem que você perceba, exatamente no horário em que a lentidão aparece.</li>\n  <li><strong>Cabo vs. Wi-Fi:</strong> faça um teste de velocidade conectado por cabo diretamente ao roteador. Se o resultado for bom por cabo e ruim no Wi-Fi, o plano não é o problema, a cobertura de sinal sem fio é.</li>\n</ul>\n<p>Se quiser entender melhor o que está causando a lentidão antes de trocar de plano, o guia <a href=\"/blog/como-melhorar-wifi-em-casa/\">como melhorar o Wi-Fi em casa</a> cobre esses cenários em detalhe.</p>\n\n<h2>Por que fibra óptica muda a conta</h2>\n<p>Quando se fala em Mega de internet, o número assume que a conexão é estável o suficiente para entregá-los de forma consistente. Em fibra óptica FTTH (Fiber to the Home, fibra chegando até a tomada da sua casa), a velocidade contratada é a velocidade disponível de dia e de noite. Isso é diferente de tecnologias que compartilham capacidade por torre ou por trecho de cabo coaxial.</p>\n<p>Na prática: um plano de 600 Mega em fibra FTTH entrega 600 Mega às 20h de sexta-feira, quando todo mundo está em casa. Outros tipos de conexão podem entrega a velocidade cheia às 3h da madrugada e bem menos no horário de pico. Para entender as diferenças entre cada tecnologia, leia <a href=\"/blog/fibra-vs-radio-vs-cabo/\">fibra óptica vs rádio vs cabo</a>.</p>\n\n<h2>Como decidir na prática</h2>\n<p>Um roteiro direto para chegar ao número certo:</p>\n<ol>\n  <li><strong>Conte os aparelhos que usam a internet ao mesmo tempo</strong> no pico da sua casa, geralmente o período da noite ou o fim de semana.</li>\n  <li><strong>Identifique as atividades mais pesadas:</strong> streaming em 4K, videoconferência, jogo online ou download de arquivos grandes.</li>\n  <li><strong>Some os consumos</strong> usando a tabela acima como referência.</li>\n  <li><strong>Adicione 30 a 50% de margem</strong> para picos e aparelhos que passam despercebidos, câmeras de segurança, assistentes de voz, smart home, atualizações automáticas.</li>\n  <li>Resultado abaixo de 500 Mega: um plano intermediário resolve. Acima de 500 Mega: 600 Mega ou 1 Giga, dependendo do perfil.</li>\n</ol>\n<p>Se ainda restar dúvida sobre qual plano se encaixa melhor, nossa equipe consegue ajudar pelo WhatsApp com base no tamanho da casa e no número de moradores. Para verificar se a fibra da MasterInfo já chegou no seu endereço em Joinville, <a href=\"/#cobertura\">consulte a cobertura aqui</a>sem compromisso.</p>",
  "faq": [
   {
    "q": "Quantos Mega preciso para uma família?",
    "a": "Para uma família com vários aparelhos, streaming em 4K e uso simultâneo, 600 a 800 Mega costumam ser o ideal. Casas com muitos moradores ou com home office intenso podem se beneficiar de 1 Giga. A regra prática é somar o consumo de todos os aparelhos ativos ao mesmo tempo e adicionar 30 a 50% de margem para picos."
   },
   {
    "q": "Quantos Mega preciso para jogar online?",
    "a": "Para jogos online, o ping (latência) importa mais do que a quantidade de Mega. Em fibra FTTH com latência baixa, 300 a 500 Mega já permitem jogar bem; mais Mega ajudam principalmente a baixar atualizações rápido e a não disputar banda com outros aparelhos da casa."
   },
   {
    "q": "Mais Mega sempre deixa a internet mais rápida?",
    "a": "Nem sempre. Se a lentidão vem da posição do roteador, de Wi-Fi fraco em algum cômodo ou de aparelhos consumindo em segundo plano, trocar de plano não vai resolver. Faça um teste de velocidade conectado por cabo: se o resultado for bom por cabo e ruim no Wi-Fi, o problema é de cobertura de sinal, não de plano."
   },
   {
    "q": "Como sei se estou recebendo a velocidade contratada?",
    "a": "Faça um teste de velocidade conectado por cabo diretamente ao roteador, em horário de pico (noite ou fim de semana). Em fibra FTTH, o resultado deve ficar próximo da velocidade contratada. Perdas grandes indicam Wi-Fi fraco, roteador com defeito ou algo a verificar com o suporte."
   },
   {
    "q": "Vale a pena contratar 1 Giga se moro sozinho?",
    "a": "Para uso individual e comum, 300 a 500 Mega já resolvem com folga. O 1 Giga faz mais sentido para casas com muitos aparelhos simultâneos, home office intenso, ou para quem quer garantir que nunca vai sentir lentidão independentemente do que estiver acontecendo na casa ao mesmo tempo."
   }
  ]
 },
 "fibra-vs-radio-vs-cabo": {
  "body": "\n    <div class=\"tldr\">\n      <strong>Resposta rápida:</strong> a <strong>fibra óptica</strong> é a melhor tecnologia de internet disponível hoje: mais rápida, mais estável e imune a chuva e interferência. A internet <strong>via rádio</strong> serve para áreas rurais sem cabeamento, mas oscila e divide banda com os vizinhos. O <strong>cabo metálico</strong> (par de cobre ou coaxial) é legado e perde para a fibra em praticamente tudo. Se há fibra disponível no seu endereço, ela é a escolha certa.\n    </div>\n\n    <h2>O que é cada tecnologia, e como funciona de verdade</h2>\n\n    <h3>Fibra óptica (FTTH)</h3>\n    <p>Os dados viajam na forma de pulsos de luz dentro de um cabo de vidro finíssimo. A perda de sinal por distância é mínima, quem mora a 2 km da central recebe essencialmente o mesmo sinal de quem mora a 200 metros. FTTH significa <em>Fiber To The Home</em>: o cabo de fibra chega fisicamente até dentro do imóvel e se conecta a um equipamento chamado ONU (ou ONT). A partir daí, o roteador distribui o sinal por Wi-Fi ou cabo de rede.</p>\n    <p>A fibra não conduz eletricidade, então não sofre com raios, surtos elétricos nem interferência de outros equipamentos. É por isso que ela não cai em tempestades, ao contrário do que muita gente imagina, a chuva em si nunca é o problema quando a conexão é fibra pura.</p>\n\n    <h3>Internet via rádio (wireless)</h3>\n    <p>O sinal chega por ondas de rádio, de uma torre ou antena do provedor até um receptor instalado no telhado ou parede do imóvel. Não exige que um cabo passe pela rua até a sua casa, o que foi, e ainda é, a grande vantagem em áreas rurais sem infraestrutura de cabeamento.</p>\n    <p>A desvantagem está na física do rádio: o sinal precisa de linha de visada razoável com a torre e é sensível a obstáculos (prédios, árvores, relevo) e condições climáticas. Além disso, a antena da torre divide a banda disponível entre todos os clientes conectados a ela. Quando muita gente usa ao mesmo tempo, no horário nobre, por exemplo, a velocidade de cada um cai.</p>\n\n    <h3>Cabo metálico (par trançado e coaxial)</h3>\n    <p>Usa condutores de cobre para transmitir sinal elétrico ou de radiofrequência. O par trançado (ADSL, VDSL) foi o padrão de banda larga no Brasil por anos, aproveitando a infraestrutura de telefonia. O coaxial chegou depois com tecnologias como o DOCSIS, usado por empresas de TV a cabo. Ambos têm capacidade e estabilidade muito inferiores à fibra: a velocidade degrada com a distância, o par de cobre capta interferência eletromagnética e a manutenção da rede física é cara. Hoje quem ainda usa essas tecnologias geralmente é porque não tem fibra disponível no endereço.</p>\n\n    <h2>Comparativo direto</h2>\n    <table class=\"article-table\">\n      <thead>\n        <tr>\n          <th>Critério</th>\n          <th>Fibra óptica (FTTH)</th>\n          <th>Via rádio</th>\n          <th>Cabo metálico</th>\n        </tr>\n      </thead>\n      <tbody>\n        <tr>\n          <td>Velocidade máxima</td>\n          <td>Alta (600 Mega a 1 Giga+)</td>\n          <td>Baixa a média</td>\n          <td>Média (cai com distância)</td>\n        </tr>\n        <tr>\n          <td>Estabilidade</td>\n          <td>Excelente</td>\n          <td>Oscila (clima, congestionamento)</td>\n          <td>Boa, mas inferior à fibra</td>\n        </tr>\n        <tr>\n          <td>Latência (ping)</td>\n          <td>Tipicamente baixa</td>\n          <td>Tipicamente média a alta</td>\n          <td>Tipicamente média</td>\n        </tr>\n        <tr>\n          <td>Afeta com chuva?</td>\n          <td>Não</td>\n          <td>Sim (especialmente granizo/tempestade)</td>\n          <td>Pouco</td>\n        </tr>\n        <tr>\n          <td>Banda compartilhada?</td>\n          <td>Dedicada por casa</td>\n          <td>Compartilhada na torre</td>\n          <td>Compartilhada no nó</td>\n        </tr>\n        <tr>\n          <td>Interferência elétrica</td>\n          <td>Nenhuma</td>\n          <td>Ruído de rádio</td>\n          <td>Sujeita a surtos e ruído</td>\n        </tr>\n        <tr>\n          <td>Melhor para</td>\n          <td>Casa e empresa na cidade</td>\n          <td>Zona rural sem cabeamento</td>\n          <td>Legado (sem alternativa disponível)</td>\n        </tr>\n      </tbody>\n    </table>\n\n    <h2>Por que a latência importa tanto quanto a velocidade</h2>\n    <p>Velocidade (Mega) é quanto dado passa por segundo. Latência (ping, medida em milissegundos) é quanto tempo leva para um pacote ir e voltar. Para streaming de vídeo, o que mais importa é a velocidade. Para jogos online, chamadas de vídeo e trabalho remoto, a latência costuma ser tão decisiva quanto, ou mais.</p>\n    <p>A fibra tende a ter latência bem baixa em condições normais. A internet via rádio costuma ter latência mais alta, especialmente quando a antena está congestionada ou há obstáculos no caminho do sinal. Essa diferença não aparece no teste de velocidade, mas você sente no jogo que \"engasga\" sem motivo aparente e na chamada onde todo mundo fala ao mesmo tempo sem que ninguém perceba na hora. Quem joga online ou trabalha com reuniões frequentes tem razão em priorizar fibra pelo ping, não só pelos Mega. Para saber o que faz sentido para o seu uso, veja o post sobre <a href=\"/gamer/\">internet para gamer</a>.</p>\n\n    <h2>Por que a fibra virou o padrão nas cidades</h2>\n    <p>A fibra não sofre interferência eletromagnética, não degrada com a distância (dentro do projeto de rede), não cai em tempestade e mantém a velocidade estável no horário de pico. Para quem mora em Joinville, onde a rede de fibra já cobre grande parte da cidade, a escolha é bastante direta. Veja a cobertura disponível nos bairros em <a href=\"/internet-joinville/\">internet fibra em Joinville</a>.</p>\n    <p>Outro ponto relevante é a banda dedicada: em FTTH, o cabo de fibra que chega na sua casa é seu. Diferente de tecnologias em que vários clientes dividem a mesma capacidade na última milha, na fibra a velocidade contratada não depende de quantas casas da sua rua estão usando a rede ao mesmo tempo.</p>\n\n    <h2>E a internet via rádio, quando faz sentido?</h2>\n    <p>A internet via rádio tem o seu lugar e não deve ser descartada sem contexto. Em sítios, chácaras, zonas rurais e bairros onde o cabeamento de fibra ainda não chegou, ela conecta onde nada mais conecta. É melhor ter rádio do que não ter internet.</p>\n    <p>O que não faz sentido é escolher rádio quando a fibra está disponível no mesmo endereço, e isso ainda acontece por desinformação ou porque a oferta do provedor de rádio chegou primeiro. Se você mora numa área urbana de Joinville e nunca verificou se tem fibra disponível, vale a pena <a href=\"/blog/cobertura-fibra-cep-joinville/\">consultar a cobertura pelo CEP</a> antes de renovar um plano de rádio.</p>\n\n    <h2>Como identificar o que você tem hoje</h2>\n    <p>Não tem certeza do tipo de conexão que chega na sua casa? Veja alguns sinais práticos:</p>\n    <ul>\n      <li><strong>Fibra (FTTH):</strong> há um cabo fino e transparente (ou com capa colorida, geralmente amarela ou laranja) que entra na casa e se conecta a um equipamento pequeno chamado ONU ou ONT, diferente do roteador Wi-Fi. O equipamento tem uma luz indicadora chamada PON (verde e estável quando tudo está bem).</li>\n      <li><strong>Via rádio:</strong> há uma antena ou receptor externo fixado no telhado, parede ou janela, com um cabo descendo até o roteador dentro de casa. Se chover forte e a internet cair junto, é um sinal clássico.</li>\n      <li><strong>Cabo metálico:</strong> a conexão chega por um fio de cobre pela fiação de telefone ou pelo mesmo cabo da TV a cabo. Geralmente você tem um modem com porta de linha telefônica (DSL) ou entrada coaxial.</li>\n    </ul>\n    <p>Se ainda tiver dúvida, a equipe de suporte consegue confirmar rapidamente o tipo de tecnologia do seu ponto.</p>\n\n    <h2>Como decidir: um guia rápido</h2>\n    <p>Na maioria dos casos, a resposta depende do que está disponível no seu endereço:</p>\n    <ul>\n      <li><strong>Tem fibra disponível no seu endereço?</strong> Contrate fibra. A diferença de experiência em relação às outras tecnologias é perceptível no dia a dia.</li>\n      <li><strong>Mora em área rural ou bairro sem fibra?</strong> A internet via rádio é a alternativa viável; escolha um provedor com boa reputação local e antena próxima.</li>\n      <li><strong>Ainda tem cabo metálico?</strong> Verifique se a fibra já chegou na rua. Se chegou, a migração costuma ser sem custo de instalação e a diferença de experiência é imediata.</li>\n    </ul>\n    <p>Para quem mora em Joinville e quer entender qual plano de fibra faz sentido para o seu perfil de uso, família, home office, jogos ou streaming, o guia <a href=\"/blog/quantos-mega-de-internet-voce-precisa/\">quantos Mega você precisa</a> ajuda a decidir antes de contratar. E se a dúvida for sobre sinal dentro de casa após a instalação, o post sobre <a href=\"/blog/como-melhorar-wifi-em-casa/\">como melhorar o Wi-Fi</a> cobre os ajustes de roteador e posicionamento.</p>\n\n    <h2>Consulte a cobertura no seu endereço</h2>\n    <p>A MasterInfo opera com fibra óptica 100% FTTH em Joinville. Para confirmar se a rede já chega na sua rua e ver os planos disponíveis, verifique a cobertura pelo CEP aqui no site ou fale com a equipe pelo WhatsApp. A instalação é feita por técnicos locais e agendada em até 3 dias úteis após a confirmação. Veja também o comparativo de provedores no guia <a href=\"/melhor-internet-joinville/\">melhor internet de Joinville</a>.</p>\n",
  "faq": [
   {
    "q": "Fibra óptica é melhor que internet via rádio?",
    "a": "Na cidade, sim. A fibra é mais rápida, mais estável, tem latência menor e não sofre com chuva nem com congestionamento de outros usuários na mesma antena. A internet via rádio é uma alternativa válida em áreas rurais onde ainda não há cabeamento de fibra."
   },
   {
    "q": "A fibra óptica cai com chuva?",
    "a": "Não. Os dados viajam como luz dentro de um cabo de vidro, sem nenhum componente elétrico exposto. A fibra não é afetada por chuva, raios nem interferência eletromagnética. Se a internet cai em tempestade, quase sempre é sinal de internet via rádio, não fibra."
   },
   {
    "q": "Qual a diferença entre fibra e cabo metálico?",
    "a": "A fibra usa pulsos de luz em cabo de vidro: altíssima capacidade, sem degradação por distância e sem interferência elétrica. O cabo metálico (cobre) usa sinal elétrico: a velocidade cai com a distância, é suscetível a surtos e tem capacidade menor. A fibra supera o cabo em velocidade, estabilidade e latência."
   },
   {
    "q": "Como sei se tenho fibra (FTTH) na minha casa?",
    "a": "Se houver um equipamento chamado ONU ou ONT dentro do imóvel, conectado por um cabo fino de fibra (geralmente transparente ou com capa amarela/laranja), é FTTH. Esse equipamento tem uma luz indicadora (PON) diferente do roteador Wi-Fi. Caso haja uma antena no telhado com cabo descendo para o roteador, é internet via rádio."
   },
   {
    "q": "Por que a internet via rádio oscila no horário de pico?",
    "a": "Porque a banda de uma antena de rádio é compartilhada entre todos os clientes conectados a ela. Quando muita gente usa ao mesmo tempo, especialmente à noite,  a velocidade disponível para cada um diminui. Na fibra FTTH, o cabo que chega na sua casa é dedicado, então esse problema não ocorre."
   },
   {
    "q": "Latência (ping) faz diferença no dia a dia?",
    "a": "Sim, dependendo do uso. Para streaming de vídeo, a latência não é muito perceptível. Para jogos online, chamadas de vídeo e home office com reuniões frequentes, latência alta causa travamentos, atraso de áudio e 'lag'. A fibra tende a ter latência bem menor do que a internet via rádio, especialmente em horários de pico."
   }
  ]
 },
 "como-melhorar-wifi-em-casa": {
  "body": "\n    <div class=\"tldr\">\n      <strong>Resposta rápida:</strong> a maioria dos problemas de Wi-Fi vem de <strong>posição ruim do roteador</strong>. Coloque-o num ponto central da casa, elevado, longe de paredes grossas, micro-ondas e espelhos. Reinicie quando travar, use a rede de 5 GHz nos aparelhos que precisam de velocidade, proteja a senha e, em casas grandes, opte por <strong>2 roteadores em mesh</strong>. Se a lentidão aparecer até por cabo, o problema pode não ser o Wi-Fi, é hora de testar o plano e acionar o suporte.\n    </div>\n\n    <h2>1. Posicione bem o roteador, é onde tudo começa</h2>\n    <p>Nenhum ajuste de configuração compensa um roteador mal posicionado. O sinal Wi-Fi se propaga em todas as direções a partir do aparelho, então o ponto de instalação define quanto da casa vai ser bem coberto.</p>\n    <p>O ideal é um local <strong>central</strong> (mais ou menos equidistante dos cômodos que você usa), <strong>elevado</strong> (em cima de um móvel ou estante, a pelo menos 1 metro do chão) e <strong>desobstruído</strong>. Roteador no chão, dentro de armário ou atrás da TV perde boa parte do alcance antes mesmo de o sinal sair do móvel.</p>\n    <p>Alguns obstáculos que bloqueiam mais do que parecem:</p>\n    <ul>\n      <li><strong>Paredes de concreto ou tijolo maciço</strong>atenuam bastante o sinal, especialmente no 5 GHz.</li>\n      <li><strong>Espelhos e vidros temperados</strong>refletem e dispersam ondas de rádio.</li>\n      <li><strong>Micro-ondas em funcionamento</strong>emitem interferência justamente na faixa de 2,4 GHz.</li>\n      <li><strong>Aquários grandes</strong>a água absorve parte do sinal.</li>\n    </ul>\n    <p>Se o roteador precisa ficar perto da entrada de fibra (onde foi feita a instalação) e esse ponto é um canto da casa, veja a seção sobre mesh mais abaixo, costuma ser mais eficiente do que tentar jogar o sinal por várias paredes.</p>\n\n    <h2>2. Reinicie quando travar (e entenda quando não resolve)</h2>\n    <p>O reinício resolve uma classe específica de problema: o roteador fica online há semanas sem parar, acumula conexões abertas na memória e começa a atender mal os aparelhos. Tirar da tomada por 30 segundos e religar limpa esse estado. Espere de 1 a 2 minutos para as luzes estabilizarem antes de testar.</p>\n    <p>O reinício <strong>não</strong> resolve problemas de sinal fraco por distância, interferência de vizinhos ou plano subdimensionado. Se a internet continua lenta depois do reinício, avance pelas próximas etapas antes de concluir que o problema é o provedor.</p>\n\n    <h2>3. Entenda as duas redes: 2,4 GHz e 5 GHz</h2>\n    <p>Roteadores modernos transmitem em duas faixas de frequência ao mesmo tempo, e saber qual usar em cada situação faz diferença concreta no dia a dia.</p>\n    <ul>\n      <li><strong>2,4 GHz:</strong> alcance maior, atravessa paredes com mais facilidade, mas velocidade menor e mais sujeita a interferência, ela divide o espectro com micro-ondas, babás eletrônicas, câmeras sem fio e a maioria das redes dos vizinhos. Boa para dispositivos distantes do roteador que não precisam de muita velocidade: lâmpadas inteligentes, tomadas Wi-Fi, câmera de segurança no quintal.</li>\n      <li><strong>5 GHz:</strong> mais rápida e muito menos congestionada, mas o sinal atenua mais com paredes e distância. Ideal para TV em streaming, videochamadas, computador e celular principal, sempre que o aparelho está num raio razoável do roteador.</li>\n    </ul>\n    <p>Na prática: se o seu roteador aparece como duas redes (ex.: \"MasterInfo\" e \"MasterInfo_5G\"), conecte a TV, o notebook e o celular que você usa para trabalhar na opção 5G. Aparelhos pequenos e longe ficam no 2,4 GHz sem prejudicar a velocidade dos outros.</p>\n    <p>Dúvida sobre qual plano faz sentido para o seu uso? O guia <a href=\"/blog/quantos-mega-de-internet-voce-precisa/\">quantos Mega você precisa</a> ajuda a alinhar velocidade contratada com o número de aparelhos em casa.</p>\n\n    <h2>4. Proteja a senha, Wi-Fi aberto tem custo real</h2>\n    <p>Uma senha fraca ou o hábito de compartilhar o Wi-Fi com todo visitante resulta em mais dispositivos consumindo a banda que você pagou. Isso aparece como lentidão geral, especialmente no 2,4 GHz, que é a rede que aparelhos extras tendem a usar.</p>\n    <p>Boas práticas simples:</p>\n    <ul>\n      <li>Use uma senha com ao menos 12 caracteres misturando letras, números e símbolos.</li>\n      <li>Troque a senha se perceber lentidão inexplicável ou se muita gente souber a senha antiga.</li>\n      <li>Se recebe visitas frequentes, crie uma <strong>rede de convidados</strong> separada, a maioria dos roteadores modernos oferece essa opção no painel de configuração. Assim o aparelho do visitante não acessa sua rede principal.</li>\n    </ul>\n    <p>Para o passo a passo de como acessar o painel do roteador e fazer essas configurações, veja a página de <a href=\"/ajuda/wifi/\">configuração de Wi-Fi</a>.</p>\n\n    <h2>5. Teste para saber se é Wi-Fi ou plano</h2>\n    <p>Antes de concluir que a internet está lenta, vale 5 minutos de diagnóstico simples que pode poupar tempo e evitar chamadas de suporte desnecessárias.</p>\n    <ol>\n      <li><strong>Teste por cabo:</strong> ligue um notebook ou computador diretamente ao roteador com cabo de rede e faça um teste de velocidade. Se a velocidade vier próxima ao contratado, o plano está entregando, o problema está no Wi-Fi.</li>\n      <li><strong>Teste de distância:</strong> faça o teste de velocidade pelo Wi-Fi bem perto do roteador e depois a alguns metros com paredes no meio. Se perto vai rápido e longe vai devagar, é cobertura, resolve com reposicionamento ou mesh.</li>\n      <li><strong>Teste em outro aparelho:</strong> se só um celular ou computador está lento, o problema pode ser naquele dispositivo, memória cheia, app em segundo plano consumindo rede, atualização em andamento.</li>\n    </ol>\n    <p>Se a velocidade vier ruim até por cabo, aí sim é algo a investigar com o suporte. Confira também <a href=\"/blog/internet-caiu-o-que-fazer/\">o que fazer quando a internet cai</a> para um passo a passo usando as luzes do roteador como guia.</p>\n\n    <h2>6. Casa grande, sobrado ou escritório: quando usar 2 roteadores</h2>\n    <p>Um único roteador cobre bem apartamentos e casas térreas de tamanho médio. Mas em sobrados, casas com muitas paredes de alvenaria ou ambientes mais amplos, o sinal vai enfraquecer nos cômodos mais distantes, e não há muito o que fazer só com reposicionamento.</p>\n    <p><strong>Sinais de que você pode precisar de 2 roteadores:</strong></p>\n    <ul>\n      <li>O celular mostra boa velocidade próximo ao roteador, mas 1 ou 2 barras e conexão instável no quarto ou na garagem.</li>\n      <li>A chamada de vídeo trava sempre que você vai para um cômodo específico.</li>\n      <li>O teste de velocidade a poucos metros dá resultado muito diferente do teste na mesma sala do roteador.</li>\n    </ul>\n    <p>A solução mais eficiente hoje é a <strong>rede mesh</strong>: dois roteadores que trabalham juntos como se fossem um único. Seu celular troca de um para o outro automaticamente conforme você anda pela casa, sem cair a conexão. Não é a mesma coisa que um repetidor comum, o repetidor cria uma rede paralela que divide a banda e às vezes exige trocar de rede manualmente.</p>\n    <p>Veja os detalhes e as configurações disponíveis na página de <a href=\"/com-2-roteadores/\">internet com 2 roteadores</a>. Para apartamentos e casas menores, a <a href=\"/com-1-roteador/\">solução com 1 roteador</a> costuma ser suficiente.</p>\n\n    <h2>7. Canais Wi-Fi e interferência de vizinhos</h2>\n    <p>Em prédios e condomínios, várias redes Wi-Fi operando ao mesmo tempo no mesmo canal causam congestionamento. No 2,4 GHz isso é mais comum porque há poucos canais disponíveis sem sobreposição; no 5 GHz o problema é bem menos frequente.</p>\n    <p>A maioria dos roteadores modernos escolhe o canal automaticamente. Se o seu estiver numa vizinhança muito densa e a rede ficar instável, vale acessar o painel do roteador (normalmente em 192.168.0.1 ou 192.168.1.1) e definir manualmente o canal 1, 6 ou 11 no 2,4 GHz, são os três que não se sobrepõem entre si.</p>\n\n    <h2>8. Mantenha o firmware do roteador atualizado</h2>\n    <p>O firmware é o sistema operacional do roteador. Fabricantes lançam atualizações que corrigem bugs de desempenho, fecham falhas de segurança e às vezes melhoram a estabilidade do sinal. Em muitos roteadores modernos a atualização acontece automaticamente; nos mais antigos, você precisa entrar no painel do aparelho, procurar pelo menu \"Administração\" ou \"Sistema\" e verificar manualmente.</p>\n    <p>Não precisa ser feito toda semana. Mas se a lentidão começou de repente sem mudança no número de aparelhos em casa, vale checar se há atualização pendente, antes de ligar pro suporte.</p>\n\n    <h2>Quando chamar o suporte</h2>\n    <p>Se você já ajustou a posição, reiniciou, testou por cabo e a velocidade ainda vem ruim, é hora de acionar a equipe. Isso pode indicar problema no sinal da fibra, na ONU (equipamento instalado em casa) ou algo na rede que precisa de verificação técnica.</p>\n    <p>Tenha em mãos quando entrar em contato: o que você já testou, em que horários a lentidão aparece mais e se acontece em todos os aparelhos ou só em alguns. Essas informações agilizam bastante o diagnóstico. Abra um chamado em <a href=\"/ajuda/reportar/\">reportar um problema</a> ou fale direto no WhatsApp, a equipe local da MasterInfo atende rápido.</p>\n    <p>Ainda não é cliente? <a href=\"/internet-joinville/\">Veja os planos de fibra disponíveis em Joinville</a> e consulte a cobertura pelo seu CEP, a instalação é feita pela nossa equipe local, em até 3 dias úteis.</p>\n",
  "faq": [
   {
    "q": "Por que meu Wi-Fi é lento em alguns cômodos mas rápido perto do roteador?",
    "a": "O sinal Wi-Fi perde força com a distância e com obstáculos como paredes de concreto, espelhos e portas. Reposicionar o roteador para um ponto mais central e elevado resolve boa parte dos casos. Em casas grandes ou com muitas paredes, a solução mais eficiente é usar 2 roteadores em rede mesh."
   },
   {
    "q": "Qual a diferença entre as redes 2,4 GHz e 5 GHz?",
    "a": "A 2,4 GHz alcança mais longe e atravessa paredes com mais facilidade, mas é mais lenta e sujeita a interferência. A 5 GHz é mais rápida e menos congestionada, com alcance menor. Use a 5 GHz nos aparelhos que precisam de velocidade (TV, notebook, celular principal) quando estiver próximo ao roteador, e a 2,4 GHz para dispositivos distantes ou com baixo consumo de dados."
   },
   {
    "q": "Reiniciar o roteador resolve a lentidão?",
    "a": "Resolve quando o problema é o roteador acumulando conexões ao longo do tempo sem reiniciar. Tire da tomada por 30 segundos, religue e aguarde de 1 a 2 minutos. Se a lentidão voltar em pouco tempo ou não melhorar com o reinício, o problema pode ser outro: posição do roteador, interferência, senha compartilhada com muita gente ou plano subdimensionado para o número de aparelhos."
   },
   {
    "q": "Testei por cabo e a internet continua lenta. O que faço?",
    "a": "Se a velocidade vem ruim até conectado por cabo diretamente ao roteador, o problema não é o Wi-Fi. Verifique se o plano contratado atende ao seu uso (número de aparelhos e atividades simultâneas) e acione o suporte da MasterInfo. Informe o que você já testou e os horários de piora, isso agiliza o diagnóstico."
   },
   {
    "q": "Qual a diferença entre repetidor Wi-Fi e rede mesh?",
    "a": "Um repetidor cria uma segunda rede separada que precisa ser selecionada manualmente e divide a banda disponível. A rede mesh usa dois roteadores integrados que funcionam como uma rede única: o aparelho troca de um nó para o outro automaticamente conforme você anda pela casa, sem queda de conexão e com perda menor de velocidade."
   },
   {
    "q": "Vizinhos com Wi-Fi podem deixar minha internet lenta?",
    "a": "Podem causar interferência, principalmente no 2,4 GHz. Muitas redes no mesmo canal causam congestionamento. A maioria dos roteadores modernos escolhe o canal automaticamente, mas em prédios muito densos pode valer acessar o painel do roteador e selecionar manualmente o canal 1, 6 ou 11. O 5 GHz tem muito mais canais disponíveis e é bem menos afetado por esse problema."
   }
  ]
 },
 "cobertura-fibra-cep-joinville": {
  "body": "<![CDATA[\n    <div class=\"tldr\">\n      <strong>Resposta rápida:</strong> a forma mais rápida de saber se tem fibra no seu endereço em Joinville é <strong>consultar a cobertura pelo CEP</strong> aqui no site. Você informa o CEP e o número do imóvel, e o sistema confirma na hora se a rede já atende o local. Se ainda não chegou, dá para registrar interesse e ser avisado quando a fibra expandir para a sua região.\n    </div>\n\n    <h2>Por que confirmar a cobertura antes de contratar</h2>\n    <p>Internet fibra óptica (FTTH, fibra até a casa) não funciona como um sinal de rádio que você capta de qualquer ponto. Ela depende de um cabo físico que já passa pela sua rua e chega até o seu imóvel. Mesmo em uma cidade com expansão ativa como Joinville, a rede cresce por etapas: novos bairros e ruas são habilitados conforme os postes e caixas de distribuição são instalados.</p>\n    <p>Confirmar a viabilidade técnica antes de qualquer coisa evita frustração. E quando o endereço já tem cobertura, agiliza tudo: você sabe na hora que pode contratar, escolhe o plano e agenda a instalação sem precisar esperar ligações ou visitas prévias.</p>\n\n    <h2>Passo a passo para consultar pelo CEP</h2>\n    <ol>\n      <li><strong>Tenha o CEP e o número do imóvel em mãos.</strong> O CEP garante que o sistema identifique a rua correta; o número refina a consulta para o seu trecho específico. Não sabe o CEP? Pesquise pelo nome da rua no site dos Correios ou no Google Maps, o CEP aparece ao digitar qualquer endereço.</li>\n      <li><strong>Abra a consulta de cobertura no site da MasterInfo.</strong> O botão de verificação fica visível na página principal. Não é preciso criar conta nem preencher nenhum formulário antes disso.</li>\n      <li><strong>Digite o CEP e o número e confirme.</strong> O sistema verifica a viabilidade técnica em tempo real, consultando o mapa de rede ativo.</li>\n      <li><strong>Leia o resultado.</strong> Dois cenários possíveis:\n        <ul>\n          <li><strong>Cobertura confirmada:</strong> você já pode escolher o plano e seguir para a contratação. A instalação é agendada e feita pela equipe técnica local.</li>\n          <li><strong>Endereço ainda fora da cobertura:</strong> deixe seu contato para ser avisado quando a fibra expandir para a sua rua. Veja mais sobre esse caso na seção abaixo.</li>\n        </ul>\n      </li>\n    </ol>\n\n    <h2>Tem cobertura: como escolher o plano</h2>\n    <p>Com a viabilidade confirmada, a próxima decisão é o plano. O tamanho ideal depende principalmente de <strong>quantos aparelhos usam a internet ao mesmo tempo</strong> na sua casa, não só de uma atividade específica. Streaming em 4K, chamada de trabalho, celular e videogame funcionando juntos somam a demanda; é esse total que define o que você precisa.</p>\n    <ul>\n      <li><strong>Uma ou duas pessoas</strong> com uso comum (redes sociais, streaming, navegação): planos a partir de 600 Mega atendem sem folga.</li>\n      <li><strong>Família com vários aparelhos</strong>streaming em 4K e crianças no tablet: 600 Mega a 1 Giga garantem tudo simultâneo sem travar.</li>\n      <li><strong>Home office</strong> com reuniões de vídeo que não podem cair e upload de arquivos pesados: estabilidade é prioridade; 600 Mega a 1 Giga com fibra dedicada até a casa resolvem bem.</li>\n      <li><strong>Gamer:</strong> o ping (latência) importa tanto quanto a velocidade. A fibra FTTH entrega latência baixa por ser dedicada, sem concorrer com vizinhos. Veja os detalhes na página de <a href=\"/gamer/\">internet para gamer</a>.</li>\n    </ul>\n    <p>Se ainda tiver dúvida sobre o número de Mega certo para o seu caso, o guia <a href=\"/blog/quantos-mega-de-internet-voce-precisa/\">quantos Mega você realmente precisa</a> explica por perfil de uso e número de aparelhos.</p>\n\n    <h2>Como funciona a instalação depois de contratar</h2>\n    <p>Confirmada a cobertura e escolhido o plano, o processo é feito inteiramente pela equipe técnica local da MasterInfo. Não há visita de pré-vistoria nem taxa de visita: você agenda, o técnico vem e só vai embora com a internet funcionando.</p>\n    <ol>\n      <li><strong>Agendamento:</strong> você escolhe um horário conveniente dentro dos próximos dias úteis.</li>\n      <li><strong>Passagem do cabo de fibra:</strong> o técnico leva a fibra do ponto de distribuição na rua até dentro do imóvel, seguindo o trajeto mais limpo e seguro. Vale deixar o acesso à caixa de entrada do imóvel livre antes da visita.</li>\n      <li><strong>Instalação do equipamento (ONT):</strong> o aparelho que converte o sinal de luz em sinal de internet é instalado e configurado na hora. O técnico testa a velocidade no local antes de qualquer outra etapa.</li>\n      <li><strong>Configuração do Wi-Fi:</strong> o roteador é configurado, o sinal é testado nos cômodos principais e o técnico só encerra a visita com tudo funcionando do jeito que deve.</li>\n    </ol>\n    <p>Quer entender o processo com mais detalhe? O post <a href=\"/blog/como-funciona-instalacao-da-fibra/\">como funciona a instalação da fibra óptica</a> explica cada etapa, inclusive o que preparar no imóvel antes da visita técnica.</p>\n\n    <h2>E se ainda não tem fibra na minha rua?</h2>\n    <p>Se o seu endereço ainda não tem cobertura, há duas coisas práticas a fazer:</p>\n    <ul>\n      <li><strong>Registre seu interesse pelo site.</strong> O sistema guarda seu contato e, assim que a fibra chegar à sua região, você é avisado. Não precisa ficar verificando manualmente toda semana.</li>\n      <li><strong>Entre em contato para perguntar a previsão.</strong> Em alguns casos a equipe já tem cronograma de expansão para ruas específicas e pode dar uma estimativa. Fale pelo <a href=\"/contato/\">formulário de contato</a> ou pelo WhatsApp.</li>\n    </ul>\n    <p>Um detalhe importante: mesmo que o endereço vizinho tenha cobertura, isso não garante automaticamente que o seu também tem. A viabilidade depende do trecho de cabo instalado e da capacidade da caixa de distribuição mais próxima. Em ruas longas, por exemplo, um lado pode já estar atendido enquanto o outro aguarda a próxima etapa de expansão. A consulta pelo CEP mais o número do imóvel é sempre a forma mais precisa de confirmar.</p>\n\n    <h2>Bairros atendidos em Joinville</h2>\n    <p>A rede da MasterInfo já atende boa parte da cidade. Entre os bairros com cobertura estão Centro, América, Glória, Bom Retiro, Boa Vista, Vila Nova, Costa e Silva e Iririú, além de outros que seguem sendo habilitados conforme a expansão avança. A lista não é estática: novos trechos são ativados com frequência, então vale sempre consultar pelo CEP mesmo que alguém da mesma região tenha dito que ainda não tinha fibra há alguns meses.</p>\n    <p>Para uma visão completa do atendimento na cidade, acesse a página de <a href=\"/internet-joinville/\">internet fibra em Joinville</a>. Se quiser entender o que diferencia os provedores disponíveis na cidade antes de decidir, o guia <a href=\"/melhor-internet-joinville/\">melhor internet de Joinville</a> traz os pontos principais a considerar.</p>\n\n    <h2>Pronto para verificar o seu endereço?</h2>\n    <p>Use a consulta de CEP aqui no site para checar a cobertura agora. Se já tiver fibra disponível, o processo de contratação é rápido e a instalação é agendada para os próximos dias úteis. A equipe técnica é local, o suporte é direto, e os planos vão de 600 Mega a 1 Giga com Wi-Fi 6 incluso. <a href=\"/internet-joinville/\">Veja os planos disponíveis para Joinville</a> e fale com a gente.</p>\n]]>",
  "faq": [
   {
    "q": "Como sei se tem fibra no meu endereço em Joinville?",
    "a": "A forma mais precisa é consultar a cobertura pelo CEP aqui no site: informe o CEP e o número do imóvel e o sistema verifica na hora se a rede de fibra já atende aquele trecho. A consulta é gratuita e não gera nenhum compromisso."
   },
   {
    "q": "Preciso pagar para consultar a cobertura?",
    "a": "Não. A consulta de cobertura por CEP é totalmente gratuita e leva poucos segundos. Você só decide se quer contratar depois de ver o resultado."
   },
   {
    "q": "Preciso estar em casa para fazer a consulta de cobertura?",
    "a": "Não. A consulta é online e pode ser feita de qualquer lugar, a qualquer hora. Não envolve visita técnica prévia nem agendamento."
   },
   {
    "q": "A consulta por CEP me compromete a contratar?",
    "a": "Não. Verificar a viabilidade não gera vínculo nem compromisso. Você consulta, vê o resultado e decide se quer prosseguir com a contratação."
   },
   {
    "q": "E se ainda não tiver fibra na minha rua?",
    "a": "Você pode registrar seu interesse diretamente no site para ser avisado quando a fibra expandir para a sua região. Também é possível entrar em contato para perguntar a previsão de expansão para o seu bairro específico."
   },
   {
    "q": "Quanto tempo leva a instalação depois de contratar?",
    "a": "Após confirmar a cobertura e contratar, a instalação é agendada para os próximos dias úteis. O técnico leva o cabo de fibra até o imóvel, instala e configura o equipamento e só encerra a visita com tudo funcionando."
   },
   {
    "q": "Quais bairros de Joinville já têm fibra da MasterInfo?",
    "a": "A rede atende grande parte da cidade, incluindo Centro, América, Glória, Bom Retiro, Boa Vista, Vila Nova, Costa e Silva e Iririú, entre outros. A cobertura cresce com frequência; consulte o CEP para saber a situação exata do seu endereço, mesmo que alguém da mesma região tenha recebido uma resposta diferente há algum tempo."
   }
  ]
 },
 "internet-caiu-o-que-fazer": {
  "body": "\n    <div class=\"tldr\">\n      <strong>Resposta rápida:</strong> 1) confira as <strong>luzes do roteador</strong>a de internet/PON precisa estar acesa e fixa; 2) <strong>reinicie</strong> o roteador (tire da tomada por 30 segundos e religue); 3) teste <strong>por cabo</strong> e em outro aparelho para separar problema de Wi-Fi de problema de conexão; 4) se a luz LOS estiver vermelha ou nada resolver, <strong>acione o suporte</strong>.\n    </div>\n\n    <h2>1. Olhe as luzes do roteador antes de qualquer coisa</h2>\n    <p>O roteador mostra o estado da conexão pelas luzes do painel. Antes de reiniciar ou ligar para o suporte, observe com atenção o que está aceso, isso já indica onde está o problema e evita passos desnecessários.</p>\n    <ul>\n      <li><strong>Power apagado:</strong> o aparelho não está ligado. Verifique a tomada, o cabo de energia e se o botão de liga/desliga (quando houver) está pressionado.</li>\n      <li><strong>LOS vermelha ou piscando (fibra):</strong> o sinal de fibra não está chegando ao aparelho. Pode ser a ONU/ONT fora de encaixe, cabo de fibra dobrado ou quebrado, ou problema na rede da rua. Reinicie uma vez; se continuar vermelha, acione o suporte.</li>\n      <li><strong>LOS ou PON apagada:</strong> mesmo efeito, sem sinal de fibra. Verifique se o cabo de fibra (o fino e delicado, conector SC/APC verde ou azul) está bem encaixado na ONU.</li>\n      <li><strong>Internet/WAN apagada com Power acesa:</strong> o equipamento está ligado, mas sem autenticação com a rede. Reiniciar costuma resolver.</li>\n      <li><strong>Tudo verde mas sem internet:</strong> o roteador está sincronizado, mas algo na camada de software travou. Reiniciar resolve na maioria dos casos.</li>\n    </ul>\n    <p>Cada fabricante usa uma combinação diferente de cores e nomes. Se o seu modelo tiver manual disponível, vale checar a legenda das luzes. O ponto central é identificar se o problema está <strong>antes do roteador</strong> (sinal da fibra, responsabilidade do provedor) ou <strong>no roteador ou na rede interna</strong> (reinicialização ou configuração).</p>\n\n    <h2>2. Reinicie o roteador</h2>\n    <p><strong>Tire o roteador da tomada, aguarde 30 segundos completos e ligue de novo.</strong> Aguarde de 1 a 2 minutos até as luzes se estabilizarem antes de testar a conexão. Simples, mas resolve a maior parte das quedas e lentidões momentâneas.</p>\n    <p>O motivo é técnico: o firmware do roteador mantém tabelas de roteamento, sessões de autenticação e cache de DNS em memória. Com o tempo, ou após uma oscilação breve na rede, essas tabelas podem ficar inconsistentes. O desligamento limpa tudo e força a reconexão do zero. <strong>Não confunda com o botão Reset de fábrica</strong>esse apaga as configurações, o que não é o que você quer. Use o corte de energia mesmo.</p>\n    <p>Se o seu modelo tiver uma ONU/ONT separada do roteador Wi-Fi (dois aparelhos físicos), <strong>reinicie a ONU primeiro</strong>espere ela estabilizar, e só então reinicie o roteador Wi-Fi.</p>\n\n    <h2>3. Teste por cabo e em outro aparelho para isolar o problema</h2>\n    <p>Conexão caída e Wi-Fi com problema são duas coisas diferentes com soluções diferentes. Este teste define qual dos dois você tem.</p>\n    <ul>\n      <li><strong>Conecte um computador por cabo</strong> (cabo de rede, RJ45) direto ao roteador. Se funcionar por cabo mas não no Wi-Fi, o problema está na rede sem fio, não na conexão em si. Nesse caso, consulte o guia <a href=\"/blog/como-melhorar-wifi-em-casa/\">como melhorar o Wi-Fi em casa</a>.</li>\n      <li><strong>Teste em outro celular ou dispositivo.</strong> Se apenas um aparelho está sem internet enquanto os outros conectam normalmente, o problema é naquele dispositivo, esqueça a rede Wi-Fi e reconecte, ou reinicie o aparelho.</li>\n      <li><strong>Teste de velocidade.</strong> Se a internet está funcionando mas muito lenta, faça um teste de velocidade, idealmente por cabo. Uma velocidade muito abaixo do contratado pode indicar congestionamento, problema no roteador ou algo a verificar com o suporte. Para entender o que esperar por perfil de uso, veja <a href=\"/blog/quantos-mega-de-internet-voce-precisa/\">quantos Mega você precisa</a>.</li>\n    </ul>\n\n    <h2>4. Verifique os cabos físicos</h2>\n    <p>Antes de ligar para o suporte, vale uma inspeção rápida nos cabos visíveis:</p>\n    <ul>\n      <li>O <strong>cabo de fibra</strong> (fino, com conector verde ou azul) está bem encaixado na ONU? Ele é frágil, uma dobra muito fechada pode interromper o sinal sem mostrar dano visível.</li>\n      <li>O <strong>cabo de rede</strong> entre a ONU e o roteador (quando são equipamentos separados) está firme nos dois conectores?</li>\n      <li>O <strong>cabo de energia</strong> do roteador e da ONU está bem encaixado na tomada e no aparelho?</li>\n    </ul>\n    <p>Cabos de fibra não devem ser dobrados em ângulo agudo nem puxados com força. Se você perceber que o cabo ficou preso atrás de um móvel ou foi comprimido na parede em algum momento, pode ser a causa da queda, e é algo que o técnico precisa verificar presencialmente.</p>\n\n    <h2>5. A queda é recorrente ou foi uma vez só?</h2>\n    <p>A frequência e o padrão das quedas mudam o diagnóstico e ajudam o suporte a agir mais rápido.</p>\n    <p><strong>Caiu uma vez e voltou sozinha:</strong> pode ter sido uma oscilação pontual, uma atualização de firmware aplicada pelo provedor ou uma religa automática. Se não se repetir, provavelmente não há nada a fazer.</p>\n    <p><strong>Cai todos os dias no mesmo horário:</strong> pode ser interferência causada por um aparelho que liga nesse horário (micro-ondas perto do roteador, por exemplo) ou saturação da rede em horário de pico. Anote os horários exatos e informe ao suporte, esse padrão acelera muito o diagnóstico.</p>\n    <p><strong>Cai várias vezes ao dia sem padrão:</strong> pode ser o roteador com defeito, o cabo de fibra com problema físico intermitente ou a ONU se sobreaquecendo. Verifique se o equipamento está em local ventilado, esses aparelhos geram calor e podem travar quando ficam quentes demais.</p>\n    <p><strong>Cai apenas quando chove:</strong> em redes de fibra até a casa (FTTH), a chuva em si não deveria afetar a conexão, a fibra óptica é imune a interferência eletromagnética. Se cai consistentemente com chuva, pode haver entrada de água em algum ponto de emenda externa na rede. Informe o suporte com esse padrão para que a equipe inspecione o trecho.</p>\n\n    <h2>6. Verifique se a queda afeta só a sua casa</h2>\n    <p>Perguntar a um vizinho que também seja cliente MasterInfo pode esclarecer bastante. Se a queda afeta vários clientes na mesma rua, o problema está na rede externa, e a equipe técnica pode já estar atuando, ou precisa ser acionada com mais urgência.</p>\n    <p>Não é necessário esperar confirmar isso para abrir um chamado. Quanto mais chamados chegarem com o mesmo endereço de referência, mais rápido a equipe identifica e prioriza o ponto afetado. Se você conseguir anotar horário exato da queda e duração, melhor ainda, essas informações agilizam a triagem.</p>\n\n    <h2>7. O que informar ao suporte para resolver mais rápido</h2>\n    <p>Quando acionar o suporte, ter essas informações em mãos reduz bastante o tempo de atendimento:</p>\n    <ul>\n      <li><strong>Cor e estado da luz LOS/PON</strong> no momento da queda (vermelha, apagada, piscando).</li>\n      <li><strong>Se reiniciou</strong> o roteador e o resultado.</li>\n      <li><strong>Se testou por cabo</strong> e qual foi o resultado.</li>\n      <li><strong>Horários e frequência</strong> das quedas (uma vez, diariamente, várias vezes).</li>\n      <li><strong>Se afeta todos os aparelhos</strong> ou só alguns.</li>\n      <li><strong>Endereço completo</strong> para localizar o ponto de atendimento correto.</li>\n    </ul>\n    <p>Com essas informações, o atendente já consegue distinguir se o problema é no equipamento interno ou na rede externa, o que evita visita técnica desnecessária ou, quando necessária, já agiliza o agendamento.</p>\n\n    <h2>8. Ainda sem internet? Fale com a MasterInfo</h2>\n    <p>Se as luzes estão anormais (LOS vermelha), os cabos estão bem encaixados e o reinício não resolveu, é hora de acionar o suporte. Nossa equipe técnica é <strong>local, de Joinville</strong>e atende pelo WhatsApp. Você também pode acessar a <a href=\"/internet-joinville/\">página da MasterInfo em Joinville</a> para entrar em contato ou verificar comunicados de manutenção.</p>\n    <p>Se você ainda está avaliando a MasterInfo como provedor, veja a <a href=\"/melhor-internet-joinville/\">comparação de internet em Joinville</a>entenda <a href=\"/blog/fibra-vs-radio-vs-cabo/\">por que fibra é melhor que rádio e cabo</a> e saiba <a href=\"/blog/como-funciona-instalacao-da-fibra/\">como funciona a instalação da fibra</a> antes de contratar. Para checar se já temos cobertura no seu endereço, <a href=\"/blog/cobertura-fibra-cep-joinville/\">consulte pelo CEP</a>.</p>\n    <p>Se o que você busca é contratar ou mudar de plano, <a href=\"/internet-joinville/\">fale com nossa equipe</a>a instalação é feita em até 3 dias úteis pela nossa própria equipe técnica em Joinville.</p>\n",
  "faq": [
   {
    "q": "Por que minha internet cai sozinha com frequência?",
    "a": "As causas mais comuns são: roteador ou ONU precisando reiniciar, cabo de fibra com dobra ou encaixe solto, equipamento se sobreaquecendo por falta de ventilação, ou oscilação na rede. Anote os horários das quedas e o estado das luzes do roteador ao acionar o suporte, esse padrão acelera muito o diagnóstico."
   },
   {
    "q": "O que significa a luz LOS vermelha ou piscando no roteador?",
    "a": "Indica que o sinal de fibra não está chegando corretamente ao equipamento. Verifique se o cabo de fibra (conector verde ou azul) está bem encaixado na ONU e reinicie o aparelho uma vez. Se a luz continuar vermelha após o reinício, acione o suporte, o problema provavelmente está fora do imóvel."
   },
   {
    "q": "Reiniciar o roteador resolve mesmo?",
    "a": "Sim, na maioria dos casos de queda ou lentidão momentânea. Tire da tomada por 30 segundos completos e religue. Se houver ONU separada, reinicie ela primeiro. Aguarde 1 a 2 minutos até as luzes estabilizarem antes de testar a conexão."
   },
   {
    "q": "Como sei se o problema é no Wi-Fi ou na internet em si?",
    "a": "Conecte um computador por cabo direto ao roteador. Se funcionar por cabo mas não no Wi-Fi, o problema está na rede sem fio, veja como melhorar o Wi-Fi em casa. Se também não funcionar por cabo, o problema está na conexão e vale acionar o suporte."
   },
   {
    "q": "A internet cai quando chove. Pode ser a fibra?",
    "a": "Em redes FTTH (fibra até a casa), a chuva em si não deveria afetar a conexão, pois a fibra óptica é imune a interferência eletromagnética. Se cai consistentemente com chuva, pode haver entrada de água em algum ponto de emenda externa. Informe o suporte com esse padrão para que a equipe inspecione o trecho."
   },
   {
    "q": "Como falo com o suporte da MasterInfo?",
    "a": "Pelo WhatsApp ou pela página de contato no site. Tenha em mãos o estado das luzes do roteador, o que já testou e os horários das quedas. Nossa equipe é local de Joinville e atende de forma direta."
   }
  ]
 }
}


# Blog lote 2 (workflow + revisão, 2026-06-22).
BLOG_DEEP.update({
 "como-funciona-instalacao-da-fibra": {
  "body": "\n    <div class=\"tldr\">\n      <strong>Resposta rápida:</strong> depois de confirmar a <strong>cobertura</strong> e contratar, a instalação é <strong>agendada</strong> e realizada pela equipe técnica local. No dia, o técnico passa o <strong>cabo de fibra óptica</strong> até o imóvel, instala o equipamento (ONU/roteador), configura o Wi-Fi e testa a velocidade. Costuma levar <strong>de 1 a 2 horas</strong>.\n    </div>\n\n    <h2>Fibra óptica: o que chega até sua casa</h2>\n    <p>Diferente da internet por cabo coaxial ou rádio, a fibra óptica transmite dados por pulsos de luz dentro de um fio de vidro ultrafino. Isso resulta em menos interferência, latência mais baixa e estabilidade mesmo em dias de chuva ou em horários de pico. O cabo que o técnico instala vai da infraestrutura de distribuição da rua até dentro do seu imóvel, onde é conectado a um equipamento chamado <strong>ONU</strong> (Optical Network Unit).</p>\n    <p>Para entender por que isso faz diferença no dia a dia, veja a comparação entre <a href=\"/blog/fibra-vs-radio-vs-cabo/\">fibra óptica, rádio e cabo</a>.</p>\n\n    <h2>Antes da instalação: confirme a cobertura</h2>\n    <p>O primeiro passo é checar se a fibra já alcança o seu endereço. A rede segue um roteiro físico de expansão e nem toda rua é atendida ao mesmo tempo. Dá para verificar em segundos pelo CEP no <a href=\"/blog/cobertura-fibra-cep-joinville/\">guia de cobertura por CEP em Joinville</a>.</p>\n    <p>Com a viabilidade confirmada e o plano escolhido, a instalação é agendada para os próximos dias úteis. Na MasterInfo, o prazo costuma ser de até 3 dias úteis após a contratação, confirme o prazo exato no momento da compra.</p>\n\n    <h2>O que acontece no dia da instalação</h2>\n    <p>O técnico chega no horário combinado e segue uma sequência padrão:</p>\n    <ol>\n      <li><strong>Identificação do ponto de entrada:</strong> o técnico avalia o melhor trajeto para o cabo chegar até o imóvel. Em apartamentos, normalmente já existe eletroduto ou shaft de telecomunicações; em casas, o cabo pode ser passado pela fachada, pelo teto ou pelo piso, conforme o acesso disponível.</li>\n      <li><strong>Passagem do cabo de fibra:</strong> o cabo vai da caixa de distribuição externa, chamada CTO (Caixa de Terminação Óptica), fixada no poste ou na calçada, até o ponto escolhido dentro do imóvel.</li>\n      <li><strong>Instalação da ONU:</strong> a ONU é o equipamento que converte o sinal de luz em sinal elétrico e Wi-Fi. Ela fica num ponto fixo, perto de uma tomada, e é o ponto central de onde parte toda a sua conexão.</li>\n      <li><strong>Configuração do Wi-Fi:</strong> o técnico define o nome da rede e a senha conforme a sua preferência e orienta sobre alcance e posicionamento.</li>\n      <li><strong>Teste de velocidade:</strong> antes de encerrar, o técnico confirma que a velocidade está de acordo com o plano contratado.</li>\n    </ol>\n\n    <h2>Quanto tempo leva a instalação</h2>\n    <p>A maioria das instalações fica entre <strong>1 e 2 horas</strong>. O que influencia esse tempo:</p>\n    <ul>\n      <li><strong>Apartamento com infraestrutura pronta</strong> (eletroduto, shaft): tende a ser mais rápido, às vezes menos de 1 hora.</li>\n      <li><strong>Casa com trajeto mais longo</strong> ou sem infraestrutura de passagem: pode chegar perto de 2 horas ou um pouco mais.</li>\n      <li><strong>Estruturas mais complexas:</strong> o técnico avalia no local e, se necessário, agenda um retorno com equipe adicional.</li>\n    </ul>\n\n    <h2>Como se preparar para o dia</h2>\n    <p>Algumas providências simples evitam atrasos e garantem um resultado melhor:</p>\n    <ul>\n      <li><strong>Defina onde quer o roteador</strong> antes da chegada do técnico. O ideal é um ponto central e elevado no imóvel, longe de paredes grossas e de eletrodomésticos que geram interferência, como o micro-ondas. Isso melhora a cobertura Wi-Fi em todos os cômodos.</li>\n      <li><strong>Garanta uma tomada disponível</strong> perto do ponto escolhido para a ONU.</li>\n      <li><strong>Deixe o acesso livre:</strong> o técnico precisa circular pelo imóvel para traçar o melhor percurso do cabo. Móveis bloqueando passagens atrasam o serviço.</li>\n      <li><strong>Tenha um responsável adulto no local</strong> durante todo o tempo da instalação para decidir sobre posicionamento, acompanhar o trajeto do cabo e assinar a ordem de serviço ao final.</li>\n      <li><strong>Anote o nome da rede e a senha</strong> que o técnico configurar, ou peça para ele deixar por escrito.</li>\n    </ul>\n\n    <h2>Instalação em apartamento: o que muda</h2>\n    <p>Em condomínios, a fibra normalmente chega até um ponto centralizado no prédio, como o shaft de telecomunicações ou uma caixa no corredor do andar. A partir daí, o técnico usa a infraestrutura interna do prédio para alcançar o seu apartamento. Em alguns casos, é necessário alinhar com a administração ou o síndico para liberar o acesso aos dutos.</p>\n    <p>Se o prédio ainda não tem infraestrutura adequada para fibra, o técnico avalia as alternativas de passagem no próprio dia. Isso é raro em construções mais recentes, mas acontece em prédios mais antigos.</p>\n\n    <h2>Instalação em casa: pontos de atenção</h2>\n    <p>Em casas, o técnico tem mais flexibilidade para escolher o trajeto. O cabo costuma entrar pela fachada ou pelo telhado. Algumas situações práticas:</p>\n    <ul>\n      <li>Muros altos ou cercas elétricas podem exigir que o cabo passe por pontos específicos, o técnico avalia e orienta no local.</li>\n      <li>Quintais extensos aumentam o comprimento do cabo, mas não inviabilizam a instalação.</li>\n      <li>Se você quiser o roteador em um cômodo distante da entrada do cabo, pode ser necessário usar um cabo adicional interno ou planejar mais adiante a expansão com um <a href=\"/com-2-roteadores/\">segundo roteador</a>.</li>\n    </ul>\n\n    <h2>Depois da instalação: primeiros passos</h2>\n    <p>Com a fibra funcionando, conecte celulares, notebooks e smart TVs ao Wi-Fi e teste a velocidade em cada aparelho. Se algum cômodo ficar com sinal fraco, vale conversar com a equipe sobre o posicionamento do roteador ou a adição de um segundo ponto.</p>\n    <p>Quem trabalha em casa pode conectar o computador principal por cabo de rede (Ethernet) diretamente na ONU ou no roteador: a latência cai e a estabilidade aumenta. Útil para videoconferências e acesso remoto.</p>\n    <p>Para escolher o plano certo antes de contratar, leia <a href=\"/blog/quantos-mega-de-internet-voce-precisa/\">quantos Mega de internet você precisa</a> ou veja todos os planos disponíveis em <a href=\"/internet-joinville/\">internet em Joinville</a>.</p>\n\n    <h2>E se houver algum problema após a instalação?</h2>\n    <p>Se a internet cair ou apresentar lentidão logo após a instalação, o primeiro passo é reiniciar a ONU: desligue da tomada, aguarde 30 segundos e religue. A maioria dos casos se resolve assim. Se o problema persistir, entre em contato com o suporte da MasterInfo pelo WhatsApp, por ser um provedor local de Joinville, o atendimento é direto e a equipe técnica conhece a rede da cidade.</p>\n",
  "faq": [
   {
    "q": "Quanto tempo leva a instalação da fibra óptica?",
    "a": "Na maioria dos casos, de 1 a 2 horas. Apartamentos com infraestrutura pronta (eletroduto, shaft) costumam ser mais rápidos; casas com trajetos mais longos ou sem infraestrutura de passagem podem levar perto de 2 horas ou um pouco mais."
   },
   {
    "q": "Preciso estar em casa durante a instalação?",
    "a": "Sim. É necessário que um responsável adulto esteja no local durante todo o serviço para liberar o acesso, indicar onde instalar o roteador, acompanhar o trajeto do cabo e assinar a ordem de serviço ao final."
   },
   {
    "q": "Em quanto tempo consigo agendar a instalação após contratar?",
    "a": "Na MasterInfo, o prazo costuma ser de até 3 dias úteis após a contratação. Confirme o prazo exato no momento da compra, pois pode variar conforme a agenda da equipe técnica."
   },
   {
    "q": "A instalação tem custo?",
    "a": "Depende do plano e da promoção vigente no momento da contratação. As condições são informadas antes de você fechar o pedido. Em caso de dúvida, fale com a gente pelo WhatsApp para saber o que se aplica ao seu caso."
   },
   {
    "q": "O técnico configura o Wi-Fi na instalação?",
    "a": "Sim. O técnico configura o nome da rede (SSID) e a senha conforme a sua preferência e testa a velocidade antes de encerrar o atendimento."
   },
   {
    "q": "O que é a ONU instalada pelo técnico?",
    "a": "A ONU (Optical Network Unit) é o equipamento que converte o sinal de luz da fibra óptica em sinal elétrico e Wi-Fi. É o ponto fixo de onde parte toda a conexão do seu imóvel."
   }
  ]
 },
 "internet-para-empresas-o-que-considerar": {
  "body": "<![CDATA[\n    <div class=\"tldr\">\n      <strong>Resposta rápida:</strong> para empresa, priorize <strong>banda garantida</strong><strong>upload simétrico</strong><strong>IP fixo</strong><strong>SLA documentado</strong> e <strong>suporte prioritário com equipe local</strong>. Para operações que não podem parar, o <strong>link dedicado</strong> supera a banda larga comum em confiabilidade. Veja a <a href=\"/internet-empresarial/\">internet empresarial da MasterInfo</a> em Joinville.\n    </div>\n\n    <h2>Por que a internet residencial não serve bem para empresa</h2>\n    <p>A diferença entre uma conexão residencial e uma empresarial não está só na velocidade anunciada. Está em <strong>como a banda é entregue</strong> e no que acontece quando algo falha.</p>\n    <p>Na banda larga doméstica, a capacidade é compartilhada entre vários assinantes do mesmo nó. Nos horários de pico, noite, hora do almoço, fim de semana, todos disputam a mesma infraestrutura. O resultado prático: videoconferência trava, sistemas em nuvem ficam lentos, upload de arquivos grandes demora o dobro. Para uso pessoal, isso é tolerável. Para uma empresa com equipe atendendo clientes ou com processos automatizados rodando, não é.</p>\n    <p>Outro ponto é a prioridade de suporte. Contrato residencial geralmente entra na fila geral de atendimento. O empresarial costuma ter SLA definido em contrato e canal diferenciado, a diferença de tempo de resposta pode significar resolver em 2 horas ou em 2 dias.</p>\n\n    <h2>1. Banda garantida x compartilhada</h2>\n    <p>A internet residencial é compartilhada: a capacidade contratada é o teto teórico, não o que você recebe o tempo todo. No <strong>link dedicado</strong>a banda é sua, de ponta a ponta, sem variação por horário. Se você contratou 100 Mbps simétrico, é isso que chega à sua porta às 8h e às 20h.</p>\n    <p>Para empresas com poucos funcionários e uso leve, consultar e-mail, navegar, reuniões esporádicas, uma <strong>banda larga empresarial</strong> de boa qualidade pode funcionar bem. Mas se a operação depende de acesso contínuo a sistemas em nuvem, atende clientes online ou transmite dados em tempo real, o link dedicado com banda garantida é o caminho mais seguro.</p>\n\n    <h2>2. Upload: tão importante quanto o download</h2>\n    <p>Empresas enviam tanto quanto recebem. Backup automático em nuvem (Google Drive, OneDrive, AWS), videochamadas, envio de notas fiscais, integração com ERPs, câmeras de segurança gravando remotamente, tudo isso consome upload. A maioria dos planos residenciais entrega upload muito menor que o download, gerando exatamente o gargalo que você sente quando a reunião trava ou o backup leva horas.</p>\n    <p>No link dedicado empresarial, o upload é igual ao download (<strong>simétrico</strong>). Para operações que dependem de comunicação em tempo real ou de sincronização constante de dados, isso muda o dia a dia de forma concreta. Se você trabalha em <a href=\"/home-office/\">home office</a> ou tem equipe remota, o impacto do upload é ainda mais direto.</p>\n\n    <h2>3. IP fixo: quando é necessário e quando é opcional</h2>\n    <p>O <strong>IP fixo</strong> é um endereço permanente na internet atribuído à sua empresa. Com ele, outros sistemas conseguem encontrar sua rede de forma confiável, sem depender de atualizações de endereço.</p>\n    <p>Você precisa de IP fixo se a empresa usa:</p>\n    <ul>\n      <li><strong>VPN própria</strong> para acesso remoto da equipe</li>\n      <li><strong>Servidor interno</strong> (NAS, servidor de arquivos, sistema de gestão local)</li>\n      <li><strong>Câmeras de segurança</strong> acessadas remotamente</li>\n      <li><strong>Ponto eletrônico</strong> ou outros dispositivos monitorados externamente</li>\n      <li><strong>Integração com APIs de terceiros</strong> que exigem liberação de IP de origem</li>\n    </ul>\n    <p>Se nenhum desses casos se aplica e a empresa só usa serviços na nuvem (Google Workspace, sistemas SaaS, e-mail hospedado fora), o IP dinâmico pode ser suficiente. Confirme com o time de TI ou fale com nosso comercial, o IP fixo pode ser incluído no plano dependendo da contratação.</p>\n\n    <h2>4. SLA: o que precisa estar escrito no contrato</h2>\n    <p>SLA é o <strong>acordo de nível de serviço</strong>: o documento que define, com números, o que o provedor se compromete a entregar. No contexto de internet empresarial, os itens mais relevantes são:</p>\n    <ul>\n      <li><strong>Disponibilidade mínima:</strong> qual o percentual de uptime garantido (ex.: 99,5% ao mês equivale a menos de 4 horas de indisponibilidade no período).</li>\n      <li><strong>Tempo máximo de resposta:</strong> em quanto tempo o provedor aciona o suporte após abertura de chamado.</li>\n      <li><strong>Tempo de resolução:</strong> prazo para restabelecimento do serviço em caso de falha.</li>\n      <li><strong>Penalidades:</strong> o que acontece se o provedor não cumprir o que foi acordado.</li>\n    </ul>\n    <p>Contrato sem SLA claro é risco. Antes de fechar qualquer contrato de internet empresarial, peça o documento de SLA e leia esses quatro pontos. Se o provedor não apresentar um, é um sinal de atenção.</p>\n\n    <h2>5. Suporte local faz diferença real</h2>\n    <p>Quando a internet cai numa empresa, cada minuto conta. A questão é: com quem você fala e quão rápido alguém consegue ir até o local?</p>\n    <p>Um provedor nacional com call center centralizado pode ter fila de atendimento longa e técnico disponível apenas em janelas amplas. Um provedor local, com equipe em Joinville, consegue despachar técnico com mais agilidade, e o técnico conhece a região, o bairro, a infraestrutura.</p>\n    <p>Para empresas em <a href=\"/internet-joinville/\">Joinville e região</a>isso tem impacto prático: menos tempo de espera, resolução no local sem depender de escalonamento para outro estado. Confirme sempre qual é o canal de suporte empresarial e o SLA de atendimento antes de contratar.</p>\n\n    <h2>6. Escalabilidade: pense no médio prazo</h2>\n    <p>A banda que serve bem hoje pode ser insuficiente em um ou dois anos. Equipe cresce, surgem novas ferramentas em nuvem, o volume de dados aumenta. Escolher um provedor que permita <strong>ampliar a banda sem trocar tudo</strong>contrato, equipamento, infraestrutura, poupa custo e dor de cabeça no futuro.</p>\n    <p>Ao negociar, pergunte: qual o prazo para upgrade de banda? Há carência para mudança de plano? O upgrade exige visita técnica ou é feito remotamente? Essas respostas dizem muito sobre a flexibilidade real do serviço.</p>\n\n    <h2>7. Redundância: o plano B quando a internet principal falha</h2>\n    <p>Para operações críticas, e-commerce, atendimento online, sistemas de ponto de venda, clínicas, vale avaliar uma <strong>conexão de backup</strong>. Não precisa ser da mesma tecnologia ou velocidade: um link secundário que entra automaticamente quando o principal cai pode salvar o dia.</p>\n    <p>Alguns roteadores têm failover automático: detectam a queda no link principal e ativam o secundário em segundos, sem intervenção manual. Se a continuidade do negócio depende de internet, essa conversa vale ser tida com o provedor e com o responsável de TI.</p>\n\n    <h2>Link dedicado ou banda larga empresarial?</h2>\n    <p>A decisão depende de quanto a internet é insumo do seu negócio:</p>\n    <ul>\n      <li><strong>Banda larga empresarial:</strong> custo menor, banda compartilhada com prioridade sobre o residencial, adequada para escritórios com uso moderado.</li>\n      <li><strong>Link dedicado:</strong> banda garantida, upload simétrico, SLA robusto, IP fixo. Indicado para operações críticas, equipes maiores, empresas com sistemas próprios ou que não toleram oscilação.</li>\n    </ul>\n    <p>Se a internet é insumo do negócio, e não só conveniência,  o link dedicado costuma compensar quando você calcula o custo real de uma hora parado. Na dúvida, fale com nosso time comercial pelo <a href=\"https://wa.me/5547989212991\">WhatsApp (47) 98921-2991</a> e descreva como a empresa usa a internet hoje: ajudamos a dimensionar a solução certa sem empurrar mais do que o necessário.</p>\n\n    <h2>Checklist antes de assinar o contrato</h2>\n    <ul>\n      <li>A banda é garantida ou compartilhada?</li>\n      <li>O upload é simétrico ao download?</li>\n      <li>IP fixo está incluso ou é adicional?</li>\n      <li>Existe SLA documentado com disponibilidade, tempo de resposta e penalidades?</li>\n      <li>Qual o canal e o horário do suporte empresarial?</li>\n      <li>É possível fazer upgrade de banda sem carência ou troca de contrato?</li>\n      <li>O provedor tem equipe técnica na minha cidade?</li>\n    </ul>\n    <p>Respondidas essas perguntas, a decisão fica bem mais clara. Conheça a <a href=\"/internet-empresarial/\">internet empresarial da MasterInfo</a>entenda <a href=\"/blog/quantos-mega-de-internet-voce-precisa/\">quantos Mega sua operação realmente precisa</a> ou compare as tecnologias disponíveis em Joinville no post <a href=\"/blog/fibra-vs-radio-vs-cabo/\">fibra vs rádio vs cabo</a>.</p>\n]]>",
  "faq": [
   {
    "q": "Qual a diferença entre internet empresarial e residencial?",
    "a": "A empresarial prioriza banda garantida (ou com prioridade sobre o residencial), upload simétrico, IP fixo, SLA documentado e suporte com prazo de atendimento definido. A residencial é compartilhada, assimétrica e sem garantia de banda nos horários de pico, adequada para casa, mas sem a confiabilidade que operações empresariais exigem."
   },
   {
    "q": "Minha empresa precisa de link dedicado?",
    "a": "Depende do quanto a internet é crítica para a operação. Se a empresa usa sistemas em nuvem intensamente, faz videoconferências constantes, processa pagamentos online, tem câmeras remotas ou não tolera oscilação, o link dedicado com banda garantida é a escolha mais segura. Para uso mais leve, e-mail, navegação, reuniões esporádicas, uma banda larga empresarial pode ser suficiente."
   },
   {
    "q": "O que é SLA e por que devo exigir um no contrato empresarial?",
    "a": "SLA (acordo de nível de serviço) é o documento que define, com números, o que o provedor garante: disponibilidade mínima, tempo máximo de resposta ao chamado, prazo de resolução de falhas e penalidades pelo descumprimento. Sem SLA claro, você fica sem amparo contratual se a internet ficar instável. Peça o documento antes de assinar."
   },
   {
    "q": "Internet empresarial inclui IP fixo?",
    "a": "No link dedicado empresarial, o IP fixo é necessário para VPN, servidores internos, câmeras remotas e integrações com APIs externas. Se está incluso ou é adicional depende do plano contratado, confirme com o comercial antes de fechar."
   },
   {
    "q": "Vale ter uma conexão de backup para a empresa?",
    "a": "Para operações críticas, e-commerce, atendimento online, sistemas de ponto de venda, clínicas, sim. Um link secundário com failover automático entra quando o principal cai, sem intervenção manual. A velocidade pode ser menor, mas garante continuidade enquanto o problema principal é resolvido."
   },
   {
    "q": "Como peço uma proposta para minha empresa em Joinville?",
    "a": "Pelo WhatsApp comercial (47) 98921-2991 ou pela página de internet empresarial da MasterInfo. Descreva como a empresa usa a internet hoje, número de usuários, sistemas principais, se tem câmeras ou servidor, e montamos a proposta adequada ao seu perfil."
   }
  ]
 },
 "sky-light-playhub-como-funciona": {
  "body": "\n    <div class=\"tldr\">\n      <strong>Resposta rápida:</strong> o <strong>PlayHub</strong> é o catálogo de apps de streaming e TV inclusos nos planos de fibra da MasterInfo. Cada plano libera uma <strong>categoria</strong> (Standard, Advanced, TOP ou Premium) e você <strong>escolhe 1 app por mês</strong> dentro dela, sem pagar nada a mais. O <strong>SKY+ Light</strong> é um dos apps disponíveis: TV ao vivo no celular, smart TV ou computador, sem antena, sem parabólica. Veja o catálogo completo em <a href=\"/playhub/\">PlayHub</a>.\n    </div>\n\n    <h2>O que é o SKY+ Light</h2>\n    <p>O <strong>SKY+ Light</strong> é um serviço de TV ao vivo que roda direto no seu celular, smart TV, tablet ou computador. Mais de 50 canais de esporte, jornalismo, entretenimento e novelas, disponíveis onde você estiver, sem precisar de antena parabólica, receptor nem ponto de TV contratado separadamente.</p>\n    <p>Ele é transmitido pela internet, então a qualidade da conexão faz diferença. Com a fibra da MasterInfo, a imagem chega estável: a velocidade mínima recomendada para TV ao vivo em HD é de [DADO A CONFIRMAR: consultar SKY+ Light para o requisito exato], e os planos aqui começam em 600 Mega, há margem sobrada.</p>\n    <p>Na categoria Advanced, a versão disponível é o <strong>SKY+ Light c/ Globo</strong>que soma os canais da emissora ao pacote de TV ao vivo.</p>\n\n    <h2>Como funciona o PlayHub</h2>\n    <p>Em vez de um pacote fixo de canais e aplicativos, a MasterInfo trabalha com o <strong>PlayHub</strong>: um catálogo de apps organizado em categorias. O plano que você contrata libera uma categoria, e todo mês você escolhe <strong>1 app</strong> dentro dela, sem custo extra.</p>\n    <p>Num mês você usa TV ao vivo com o SKY+ Light, no mês seguinte quer ouvir música e troca para o Deezer. A escolha é sua, a cada ciclo, sem fidelidade dentro do app. Para planos que liberam mais de uma categoria ao mesmo tempo (como o Ultra Home Office, que acessa TOP + Advanced + Standard), você pode ativar um app diferente em cada uma delas no mesmo mês.</p>\n\n    <h2>As quatro categorias do PlayHub</h2>\n    <p>Cada categoria corresponde a um nível de plano. Confira o que entra em cada uma:</p>\n\n    <h3>Standard, catálogo de entrada</h3>\n    <p>Incluso nos planos de <strong>600 Mega</strong> (Lite Casa). Você escolhe 1 app por mês entre:</p>\n    <ul>\n      <li><strong>SKY+ Light</strong>TV ao vivo sem antena</li>\n      <li><strong>Looke</strong>filmes e séries nacionais e internacionais</li>\n      <li><strong>Kiddle Pass</strong>conteúdo infantil</li>\n      <li><strong>PlayKids+</strong>plataforma educativa para crianças</li>\n      <li><strong>+Q Nutri</strong>acompanhamento nutricional</li>\n      <li><strong>Kaspersky 1 Lic</strong>antivírus para 1 dispositivo</li>\n      <li><strong>ExitLag</strong>otimizador de rota para jogos online</li>\n      <li><strong>Ubook Plus</strong>audiolivros</li>\n      <li><strong>Estuda+</strong>cursos e preparatório</li>\n    </ul>\n\n    <h3>Advanced, catálogo intermediário</h3>\n    <p>Incluso nos planos de <strong>800 Mega</strong> (Lite Premium, o mais procurado). Apps disponíveis por mês:</p>\n    <ul>\n      <li><strong>SKY+ Light c/ Globo</strong>TV ao vivo + canais Globo</li>\n      <li><strong>Deezer</strong>streaming de música</li>\n      <li><strong>Kaspersky 3 Lic</strong>antivírus para 3 dispositivos</li>\n      <li><strong>HotGo</strong>streaming de filmes e séries</li>\n      <li><strong>CurtaOn</strong>curtas e filmes independentes</li>\n      <li><strong>Kiddle Pass</strong>conteúdo infantil</li>\n      <li><strong>O Jornalista</strong>jornalismo e análise</li>\n      <li><strong>Docway</strong>consultas médicas online</li>\n    </ul>\n\n    <h3>TOP, os grandes nomes do streaming</h3>\n    <p>Incluso nos planos Ultra (Home Office e <a href=\"/gamer/\">Gamer</a>). Apps disponíveis por mês:</p>\n    <ul>\n      <li><strong>Amazon Prime</strong></li>\n      <li><strong>Apple TV</strong></li>\n      <li><strong>GloboPlay</strong></li>\n      <li><strong>Disney+ (Ads)</strong>com anúncios</li>\n      <li><strong>HBO Max (Ads)</strong>com anúncios</li>\n      <li><strong>SKY+</strong>TV ao vivo</li>\n      <li><strong>Indie</strong>cinema independente</li>\n      <li><strong>Leitura 360</strong>revistas e jornais digitais</li>\n    </ul>\n\n    <h3>Premium, versões sem anúncios</h3>\n    <p>Incluso nos planos <strong>Ultra Família</strong> e <strong>Ultra Gamer</strong>. Apps disponíveis por mês:</p>\n    <ul>\n      <li><strong>Disney+</strong>sem anúncios</li>\n      <li><strong>HBO Max</strong>sem anúncios</li>\n      <li><strong>GloboPlay</strong></li>\n      <li><strong>Kaspersky 5 Lic</strong>antivírus para 5 dispositivos</li>\n      <li><strong>SmartContent</strong></li>\n      <li><strong>Queima Diária</strong>treinos e bem-estar</li>\n      <li><strong>Zen</strong>meditação e saúde mental</li>\n    </ul>\n\n    <h2>Qual plano libera qual categoria</h2>\n    <p>Em resumo direto:</p>\n    <ul>\n      <li><strong>Lite Casa (600 Mega)</strong>categoria Standard (1 app/mês)</li>\n      <li><strong>Lite Premium (800 Mega)</strong>categoria Advanced (1 app/mês)</li>\n      <li><strong>Lite Basic (1 Giga)</strong>sem PlayHub (velocidade pura, sem app incluso)</li>\n      <li><strong>Ultra Família (1 Giga)</strong>categoria Premium (1 app/mês)</li>\n      <li><strong>Ultra Home Office (1 Giga)</strong>categorias TOP + Advanced + Standard (3 apps/mês)</li>\n      <li><strong>Ultra Gamer (1 Giga)</strong>categorias TOP + Premium (2 apps/mês)</li>\n    </ul>\n    <p>Para famílias que consomem muito streaming, o salto para o <a href=\"/familia/\">plano família</a> ou para o <a href=\"/tv-streaming/\">plano TV e streaming</a> entrega mais opções dentro de um custo fixo. Quem trabalha em casa e quer Disney+, segurança e TV ao vivo ao mesmo tempo vai encontrar as três categorias juntas no <a href=\"/home-office/\">Ultra Home Office</a>.</p>\n\n    <h2>Como ativar o seu app mensal</h2>\n    <p>Após contratar um plano com PlayHub, você recebe orientações pelo canal de atendimento da MasterInfo sobre como fazer a escolha mensal. Cada app ativado tem o seu próprio acesso, com login e senha fornecidos no processo.</p>\n    <p>Para saber exatamente como funciona a ativação no seu plano e o que acontece com o benefício caso não seja usado no ciclo, fale pelo <a href=\"https://wa.me/5547989212991\">WhatsApp comercial (47) 98921-2991</a>a equipe explica o passo a passo antes da contratação.</p>\n\n    <h2>Vale a pena comparado a contratar os apps separadamente</h2>\n    <p>Contratar Amazon Prime, Disney+ ou HBO Max individualmente tem um custo mensal por plataforma. No PlayHub, o acesso a um desses apps já vem dentro do valor do plano de internet. Para quem já pagaria por um desses serviços de qualquer forma, o benefício é real: você não está ganhando algo que nunca usaria, está usando crédito que já seria gasto em outro lugar.</p>\n    <p>O modelo de escolha mensal também evita o acúmulo de assinaturas paradas. Se você maratonou uma série num mês e não precisa da plataforma no seguinte, troca por outra, música, TV ao vivo, audiobook ou antivírus.</p>\n\n    <h2>Qual plano combina com o seu uso</h2>\n    <p>Se você mora sozinho ou em casal e quer só TV ao vivo ou um app de filmes ocasional, o <strong>Lite Casa com Standard</strong> já resolve. Para famílias com crianças que usam múltiplos dispositivos, o <strong>Lite Premium com Advanced</strong> é o mais procurado. Para quem quer Disney+ ou HBO Max sem anúncios, o caminho é o <strong>Ultra Família com Premium</strong>.</p>\n    <p>Em dúvida sobre a velocidade certa para a sua casa, veja <a href=\"/blog/quantos-mega-de-internet-voce-precisa/\">quantos Mega você precisa</a> ou compare as tecnologias em <a href=\"/blog/fibra-vs-radio-vs-cabo/\">fibra vs. rádio vs. cabo</a>. Para ver todos os planos com preços e detalhes, acesse <a href=\"/internet-joinville/\">internet em Joinville</a>.</p>\n",
  "faq": [
   {
    "q": "O que é o PlayHub da MasterInfo?",
    "a": "É o catálogo de apps de streaming e TV inclusos nos planos de fibra. Cada plano libera uma categoria (Standard, Advanced, TOP ou Premium) e você escolhe 1 app por mês dentro dela, sem custo adicional."
   },
   {
    "q": "O SKY+ Light está incluso no plano?",
    "a": "Sim. O SKY+ Light faz parte da categoria Standard, disponível a partir do Lite Casa (600 Mega). Na categoria Advanced, a versão disponível é o SKY+ Light c/ Globo, que inclui os canais da emissora."
   },
   {
    "q": "Posso trocar de app todo mês?",
    "a": "Sim. A cada ciclo mensal você escolhe 1 app dentro da categoria do seu plano. Usou TV ao vivo num mês, quer streaming de música no seguinte? Basta comunicar antes do vencimento do ciclo atual. Para esclarecer dúvidas sobre prazos e troca, fale pelo WhatsApp (47) 98921-2991."
   },
   {
    "q": "Preciso de antena para o SKY+ Light?",
    "a": "Não. O SKY+ Light é TV ao vivo transmitida pela internet. Funciona no celular, smart TV, tablet ou computador, sem antena, sem parabólica e sem ponto de TV avulso."
   },
   {
    "q": "Quais planos incluem Disney+ ou HBO Max?",
    "a": "Disney+ e HBO Max com anúncios (versão Ads) estão na categoria TOP, inclusa nos planos Ultra Home Office e Ultra Gamer. As versões sem anúncios estão na categoria Premium, disponível nos planos Ultra Família e Ultra Gamer."
   },
   {
    "q": "O que acontece se eu não escolher um app no mês?",
    "a": "Entre em contato com a MasterInfo pelo WhatsApp (47) 98921-2991 para saber como funciona o ciclo de ativação no seu plano e não perder o benefício."
   }
  ]
 },
 "segunda-via-de-boleto-masterinfo": {
  "body": "<![CDATA[\n    <div class=\"tldr\">\n      <strong>Resposta rápida:</strong> a 2ª via do boleto é emitida na <strong>Central do Assinante</strong> com o seu CPF/login e senha, você baixa o boleto, copia o código de barras e paga por <strong>boleto, Pix ou cartão</strong>. Sem tempo para acessar o sistema? Use o chat de boletos da <a href=\"/ajuda/boletos/\">página de boletos</a>informe só o CPF e a fatura aparece na hora, sem precisar lembrar senha.\n    </div>\n\n    <h2>Como emitir a 2ª via passo a passo</h2>\n    <ol>\n      <li>Acesse a <strong>Central do Assinante</strong> com o seu CPF/login e senha cadastrada.</li>\n      <li>No menu, localize a seção <strong>Faturas</strong> ou <strong>Boletos</strong>.</li>\n      <li>Identifique a fatura em aberto, aparece o mês de referência, o valor e o vencimento.</li>\n      <li><strong>Clique em \"2ª via\"</strong> ou \"Emitir boleto\": você pode baixar o PDF ou copiar o <strong>código de barras / chave Pix</strong> para pagar na hora.</li>\n    </ol>\n    <p>Se o login não estiver funcionando ou você esqueceu a senha, o caminho mais direto é acessar a <a href=\"/ajuda/boletos/\">página de boletos</a> e usar o chat da Marina, basta informar o CPF ou nome de cadastro para localizar a fatura sem precisar entrar na Central do Assinante.</p>\n\n    <h2>Formas de pagamento aceitas</h2>\n    <p>Você paga como for mais cômodo:</p>\n    <ul>\n      <li><strong>Pix</strong>cai na hora, sem espera de compensação. Ideal quando o vencimento está próximo ou já venceu.</li>\n      <li><strong>Boleto bancário</strong>pode ser pago em qualquer banco, lotérica ou app bancário. Leva até 1 dia útil para compensar no sistema.</li>\n      <li><strong>Cartão</strong>disponível na Central do Assinante. Para dúvidas sobre condições ou parcelamento, fale com o suporte pelo <a href=\"https://wa.me/554734341734\">WhatsApp (47) 3434-1734</a>.</li>\n    </ul>\n    <p>Pagando em dia, você mantém o desconto do plano ativo.</p>\n\n    <h2>O que fazer se o boleto venceu</h2>\n    <p>Boleto vencido não significa que você perdeu a chance de pagar. A Central do Assinante geralmente permite emitir uma nova versão atualizada com o valor corrigido. Se o sistema mostrar a fatura como vencida sem opção de reemissão, acesse a <a href=\"/ajuda/boletos/\">página de boletos</a> e use o chat, o sistema localiza contratos e faturas em aberto e orienta o próximo passo.</p>\n    <p><strong>Não pague o boleto original vencido</strong> sem verificar se há uma versão atualizada: o pagamento pode não ser reconhecido automaticamente e gerar problemas na baixa da fatura.</p>\n    <p>Para pagamento imediato em fatura vencida, o <strong>Pix</strong> é a melhor opção, a chave fica disponível na 2ª via gerada hoje e o crédito é instantâneo, sem depender de janela de compensação bancária.</p>\n\n    <h2>Consultar faturas anteriores e histórico</h2>\n    <p>Na Central do Assinante você acessa o histórico completo: faturas já pagas, datas de pagamento, valores e mês de referência. É útil para confirmar se um pagamento foi reconhecido ou para guardar o comprovante de um mês específico.</p>\n    <p>Se precisar de um comprovante formal de quitação de débitos, por exemplo, para portabilidade ou comprovação em uma análise de crédito, fale com o suporte pelo <a href=\"tel:554734341734\">(47) 3434-1734</a>.</p>\n\n    <h2>Dúvidas sobre o valor cobrado</h2>\n    <p>Se o valor da fatura não corresponde ao que você esperava, entre em contato com o suporte antes de acumular. A MasterInfo tem atendimento local em <a href=\"/internet-joinville/\">Joinville</a>o contato é direto com a equipe, sem fila de call center nacional.</p>\n    <p>Situações comuns que geram dúvida no boleto:</p>\n    <ul>\n      <li><strong>Primeiro boleto após contratação</strong>pode ter valor proporcional ao período de ativação, dependendo da data de instalação no mês.</li>\n      <li><strong>Taxa de instalação</strong>quando aplicável ao plano contratado, aparece na primeira ou segunda fatura.</li>\n      <li><strong>Ajuste de plano feito no meio do mês</strong>pode gerar cobrança proporcional na fatura seguinte.</li>\n    </ul>\n    <p>Em qualquer um desses casos, o atendimento esclarece o detalhamento da cobrança pelo <a href=\"tel:554734341734\">(47) 3434-1734</a>.</p>\n\n    <h2>Problemas comuns e como resolver</h2>\n    <ul>\n      <li><strong>Não lembro meu login ou senha da Central do Assinante</strong>use a opção de recuperação de senha no login, ou acesse o <a href=\"/ajuda/boletos/\">chat de boletos</a> para localizar a fatura sem precisar entrar na Central.</li>\n      <li><strong>O Pix não aparece na fatura</strong>verifique se você está na 2ª via gerada hoje. Boletos antigos podem não ter chave Pix; gere uma nova via para ter todas as opções atualizadas.</li>\n      <li><strong>Paguei mas o sistema ainda mostra como pendente</strong>pagamentos por boleto bancário levam até 1 dia útil para ser reconhecidos. Se passaram mais de 2 dias úteis e a situação persiste, envie o comprovante pelo WhatsApp de suporte para que a equipe confirme a baixa manualmente.</li>\n      <li><strong>Meu contrato está suspenso por inadimplência</strong>após a confirmação do pagamento, entre em contato com o suporte pelo <a href=\"tel:554734341734\">(47) 3434-1734</a> para agilizar a reativação.</li>\n    </ul>\n]]>",
  "faq": [
   {
    "q": "Como tiro a 2ª via do boleto da MasterInfo?",
    "a": "Acesse a Central do Assinante com seu CPF/login e senha, vá em Faturas ou Boletos e clique em '2ª via'. Você pode baixar o PDF ou copiar o código de barras e a chave Pix para pagar na hora. Se tiver dificuldade com o login, use o chat de boletos em /ajuda/boletos/, basta informar o CPF."
   },
   {
    "q": "Posso pagar por Pix?",
    "a": "Sim. Ao gerar a 2ª via, a chave Pix fica disponível para pagamento imediato, sem espera de compensação. É a forma mais rápida, especialmente quando o vencimento está próximo ou já passou."
   },
   {
    "q": "O que faço se o boleto já venceu?",
    "a": "Não pague o boleto vencido sem verificar se há uma versão atualizada. Na Central do Assinante é possível reemitir com o valor corrigido. Se o sistema não mostrar essa opção, acesse o chat de boletos em /ajuda/boletos/ para localizar a fatura em aberto. Pix é a melhor opção para pagar faturas vencidas, pois o crédito é instantâneo."
   },
   {
    "q": "Onde consulto faturas e pagamentos anteriores?",
    "a": "Na Central do Assinante ficam o histórico de faturas, datas de vencimento, valores e registro dos pagamentos já realizados. Para um comprovante formal de quitação, entre em contato com o suporte pelo (47) 3434-1734."
   },
   {
    "q": "Paguei mas o sistema ainda mostra a fatura como pendente. O que fazer?",
    "a": "Pagamentos por boleto bancário levam até 1 dia útil para ser reconhecidos no sistema. Se passaram mais de 2 dias úteis e ainda aparece pendente, envie o comprovante pelo WhatsApp de suporte para que a equipe confirme a baixa manualmente."
   },
   {
    "q": "Por que meu primeiro boleto teve um valor diferente do plano contratado?",
    "a": "O primeiro boleto pode ter valor proporcional ao período de ativação, dependendo da data de instalação no mês. Também pode incluir taxa de instalação, quando aplicável ao plano. O atendimento pelo (47) 3434-1734 detalha a composição da cobrança."
   }
  ]
 }
})
# Exclui do BLOG_DEEP os 2 posts do lote 2 que não passaram limpos (sky-light tem [DADO], segunda-via reprovado), mantêm o corpo original até retrabalho.
# E-E-A-T: atribui os 2 posts de suporte a Philipe (Person), não a "equipe" (Organization).
for _b in BLOG:
    if _b["slug"] in ("sky-light-playhub-como-funciona", "segunda-via-de-boleto-masterinfo"):
        _b["author"] = "tecnica"

# Posts re-escritos com fatos reais (workflow draft+review, sem travessão, 2026-06-22):
BLOG_DEEP.update({"sky-light-playhub-como-funciona": {"body": "<p>Se você está pensando em contratar (ou já é cliente) e ouviu falar do PlayHub, esta página explica de um jeito direto o que é o SKY+ Light, como ele entra no seu plano de internet e o que muda conforme a categoria que você escolhe.</p>\n\n<h2>O que é o PlayHub</h2>\n<p>O PlayHub é o combo de apps que vem junto com os planos de internet da MasterInfo. Em vez de você contratar cada serviço por fora, alguns apps de TV, streaming, segurança e bem-estar já vêm liberados dentro do plano de fibra. Quais apps você tem acesso depende da categoria do seu plano: Standard, Advanced, TOP ou Premium.</p>\n<p>Quanto mais alto o plano, mais completa é a categoria liberada. Um plano de entrada dá acesso aos apps da Standard. Os planos mais robustos abrem as categorias TOP e Premium, com vários nomes conhecidos do streaming.</p>\n\n<h2>O que é o SKY+ Light</h2>\n<p>O SKY+ Light é um serviço de TV por streaming da SKY. Na prática, é TV ao vivo que roda pela internet, sem antena e sem parabólica. Você assiste pelo aplicativo no celular, na smart TV ou pelo navegador no computador, segundo a própria SKY (<a href=\"https://www.skymais.com.br/home\">skymais.com.br</a>).</p>\n<p>Como tudo passa pela sua conexão, a qualidade da internet faz diferença na hora de assistir. Aí entra a vantagem de ter o SKY+ Light junto de um plano de fibra: a imagem depende de uma conexão estável, e a fibra ajuda nesse ponto.</p>\n\n<h2>Em qual categoria o SKY+ Light está</h2>\n<p>O SKY+ Light aparece no PlayHub em mais de uma categoria, em versões diferentes:</p>\n<ul>\n<li><strong>Standard</strong>: o SKY+ Light está aqui, ao lado de apps como Looke, Kiddle Pass, PlayKids+, +Q Nutri, Kaspersky (1 licença), ExitLag, Ubook Plus e Estuda+.</li>\n<li><strong>Advanced</strong>: a versão disponível é o SKY+ Light com Globo. A categoria ainda traz Deezer, Kaspersky (3 licenças), HotGo, CurtaOn, Kiddle Pass, O Jornalista e Docway.</li>\n<li><strong>TOP</strong>: aqui a versão é o SKY+ (sem o \"Light\"), acompanhada de Amazon Prime, Apple TV, GloboPlay, Disney+ (com anúncios), HBO Max (com anúncios), Indie e Leitura 360.</li>\n<li><strong>Premium</strong>: foca nas versões sem anúncios e em bem-estar, com Disney+, HBO Max, GloboPlay, Kaspersky (5 licenças), SmartContent, Queima Diária e Zen.</li>\n</ul>\n<p>Ou seja: dependendo da categoria do seu plano, o que muda não é só ter ou não ter SKY, é a versão (Light, Light com Globo ou SKY+) e os outros apps que vêm na mesma cesta.</p>\n\n<h2>Como assistir ao SKY+ Light</h2>\n<p>Por ser TV por streaming, o caminho é simples. Você instala o aplicativo da SKY no aparelho que preferir (celular, smart TV ou usa pelo navegador no computador) e acessa com o seu login. Não tem instalação de antena, não precisa de ponto de TV avulso e dá para assistir em casa ou fora dela, desde que tenha internet.</p>\n<p>Essa portabilidade ajuda quem não quer depender da TV da sala. Dá para acompanhar um programa no celular na cozinha, deixar a TV ligada na smart TV e usar o computador quando estiver trabalhando, tudo pelo mesmo serviço.</p>\n\n<h2>SKY+ Light como adicional avulso</h2>\n<p>Se o seu plano não inclui o SKY+ Light na categoria, ou se você quer garantir esse app de forma fixa, ele também existe como adicional contratado à parte. Os valores são:</p>\n<ul>\n<li><strong>SKY+ Light</strong>: R$ 19,90 por mês.</li>\n<li><strong>SKY+ Light + Amazon</strong>: R$ 39,90 por mês, somando o acesso à Amazon.</li>\n</ul>\n<p>É uma opção prática para quem quer a TV ao vivo da SKY sem trocar de plano, pagando só pelo que vai usar.</p>\n\n<h2>Vale a pena para o seu caso</h2>\n<p>Se a sua casa consome bastante TV ao vivo e você não quer a estrutura de antena, o SKY+ Light atende bem, ainda mais quando já vem dentro do plano. Para quem busca os grandes nomes do streaming, como Disney+ e HBO Max, a conversa muda para as categorias TOP e Premium, e aí o ideal é olhar o plano como um todo, não só a TV.</p>\n<p>Antes de decidir, vale pensar em quantas pessoas usam a internet ao mesmo tempo e quanto a casa consome de vídeo. Quanto mais gente assistindo e jogando junto, mais faz sentido um plano com mais velocidade e uma categoria de PlayHub mais completa.</p>\n\n<h2>Onde tirar dúvidas</h2>\n<p>Se ficou na dúvida sobre qual categoria o seu plano libera, ou se quer contratar o SKY+ Light como adicional, fale com a gente. Você pode ver as opções na página de <a href=\"/planos\">planos</a> ou chamar direto no <a href=\"https://wa.me/5547989212991\">WhatsApp comercial (47) 98921-2991</a>. Como a MasterInfo é um provedor local de Joinville, o atendimento é com gente da região, que ajuda você a escolher sem enrolação.</p>", "faq": [{"q": "O SKY+ Light precisa de antena ou parabólica?", "a": "Não. O SKY+ Light é um serviço de TV por streaming da SKY, ou seja, TV ao vivo que roda pela internet. Você assiste pelo aplicativo no celular, na smart TV ou pelo navegador no computador, sem antena, parabólica ou ponto de TV avulso."}, {"q": "O SKY+ Light já vem incluso no meu plano de internet?", "a": "Depende da categoria do seu plano no PlayHub. Na categoria Standard, o SKY+ Light é um dos apps disponíveis. Na Advanced, a versão é o SKY+ Light com Globo. Nas categorias TOP e Premium, o foco muda para outros apps de streaming. Se tiver dúvida sobre o que seu plano libera, fale com a gente pelo WhatsApp (47) 98921-2991."}, {"q": "Posso contratar o SKY+ Light separado, sem trocar de plano?", "a": "Sim. O SKY+ Light também existe como adicional avulso, por R$ 19,90 por mês. Há ainda a opção SKY+ Light + Amazon, por R$ 39,90 por mês, que soma o acesso à Amazon."}, {"q": "Em quais aparelhos dá para assistir ao SKY+ Light?", "a": "Por ser TV por streaming, você assiste no celular, na smart TV ou pelo navegador no computador, segundo a SKY. Basta ter internet e fazer login no aplicativo."}, {"q": "Qual a diferença entre SKY+ Light, SKY+ Light com Globo e SKY+?", "a": "São versões que aparecem em categorias diferentes do PlayHub. O SKY+ Light está na Standard; o SKY+ Light com Globo está na Advanced; e o SKY+ está na categoria TOP, ao lado de apps como Amazon Prime, Apple TV e GloboPlay."}]}, "segunda-via-de-boleto-masterinfo": {"body": "<p>Perdeu o boleto, ele não chegou no e-mail ou você só quer adiantar o pagamento? Tirar a 2ª via da sua fatura MasterInfo é simples e dá para fazer por mais de um canal. Reunimos aqui o passo a passo de cada um, além de algumas dicas para pagar sem dor de cabeça e não cair em golpe. Lembre que todos os caminhos abaixo são os canais oficiais da MasterInfo. Se aparecer um boleto vindo de outro lugar, desconfie.</p>\n\n<h2>Pelo chat da Marina (mais rápido)</h2>\n<p>A Marina é a assistente de boletos da MasterInfo. Ela fica no site e consegue listar suas faturas e gerar a 2ª via na hora. Tem dois jeitos de chamar:</p>\n<ul>\n<li>Acesse a página <a href=\"/ajuda/boletos/\">Boletos e faturas</a> no nosso site.</li>\n<li>Ou clique no botão flutuante de boleto (o ícone de código de barras) que aparece em qualquer página do site.</li>\n</ul>\n<p>Aberto o chat, a Marina pede o seu CPF só para localizar suas faturas e mostra os boletos vinculados ao seu cadastro. É só escolher a fatura que você quer e ela entrega a 2ª via, com o código de barras pronto para pagar. Esse costuma ser o caminho mais rápido para quem está com pressa.</p>\n\n<h2>Pelo WhatsApp</h2>\n<p>Se você prefere resolver pelo celular conversando com a equipe, fale com a gente no WhatsApp. Temos dois números, cada um com uma função:</p>\n<ul>\n<li><strong>Atendimento:</strong> (47) 3434-1734. Use este para 2ª via, dúvidas sobre a fatura e suporte em geral.</li>\n<li><strong>Comercial:</strong> (47) 98921-2991. Este é o canal de vendas e novas contratações.</li>\n</ul>\n<p>Para a 2ª via, o número de atendimento é o indicado. A equipe localiza sua fatura no sistema e envia o boleto atualizado para você pagar.</p>\n\n<h2>Pela Central do Assinante</h2>\n<p>A Central do Assinante é a sua área do cliente. Lá você acompanha as faturas, vê os vencimentos e baixa a 2ª via quando quiser, sem depender de horário de atendimento. O acesso é em <a href=\"https://sistema1.masterinfointernet.com/central_assinante_web/login\" target=\"_blank\" rel=\"noopener\">sistema1.masterinfointernet.com/central_assinante_web</a>, com o seu login de cliente.</p>\n<p>Depois de entrar, procure a área de faturas ou financeiro, localize a fatura em aberto e baixe o boleto. De lá você também copia o código de barras ou a linha digitável para pagar no banco.</p>\n\n<h2>Como pagar o boleto</h2>\n<p>Com o boleto em mãos, o pagamento é o mesmo de qualquer outra conta. Você pode:</p>\n<ul>\n<li>Pagar no aplicativo do seu banco lendo o código de barras pela câmera.</li>\n<li>Digitar a linha digitável (aquela sequência de números no topo do boleto) no app ou no internet banking.</li>\n<li>Pagar presencialmente em uma agência, lotérica ou caixa eletrônico.</li>\n</ul>\n<p>Alguns boletos trazem também um QR Code Pix, quando essa opção está disponível na fatura. Se o seu boleto tiver, basta apontar a câmera do app do banco para o QR Code para pagar. Se não tiver, o código de barras resolve do mesmo jeito.</p>\n\n<h2>E se o boleto estiver vencido?</h2>\n<p>Boleto atrasado às vezes precisa ser atualizado antes do pagamento. Em vez de tentar pagar um boleto antigo que pode não ser mais aceito, peça a reemissão. A própria Marina, no chat, ou a equipe de atendimento conseguem gerar uma fatura atualizada. Assim você paga o documento certo e evita que o pagamento não seja reconhecido.</p>\n<p>Se você tem mais de uma fatura em aberto, vale conferir todas de uma vez na Central do Assinante ou pedir o resumo no atendimento. É mais fácil organizar tudo de uma vez do que descobrir uma pendência só depois.</p>\n\n<h2>Atenção aos golpes de boleto</h2>\n<p>Boleto falso é um golpe comum, então alguns cuidados simples evitam prejuízo:</p>\n<ul>\n<li>Use somente os canais oficiais que citamos aqui: o chat da Marina no site, o WhatsApp de atendimento e a Central do Assinante.</li>\n<li>Antes de pagar, confira no app do banco quem é o beneficiário do boleto. O nome precisa bater com a MasterInfo.</li>\n<li>Desconfie de boletos recebidos por mensagens, e-mails estranhos ou contatos que não sejam os nossos números oficiais.</li>\n<li>Na dúvida sobre um boleto, gere a 2ª via você mesmo por um dos canais oficiais em vez de pagar um documento que chegou de fonte desconhecida.</li>\n</ul>\n\n<h2>Ainda com dúvida sobre a fatura?</h2>\n<p>Se algum valor não bateu, você não reconhece uma cobrança ou ficou em dúvida sobre o vencimento, é só falar com a gente. Por sermos um provedor local de <a href=\"/internet-joinville/\">Joinville</a>, o atendimento é com gente da região, que conhece a sua conta e resolve direto.</p>\n<p>Quer tirar a 2ª via agora? Chame a Marina na <a href=\"/ajuda/boletos/\">página de boletos</a> ou mande mensagem no nosso <a href=\"https://wa.me/554734341734\" target=\"_blank\" rel=\"noopener\">WhatsApp de atendimento (47) 3434-1734</a>. Se for assunto de plano novo ou upgrade, o <a href=\"https://wa.me/5547989212991\" target=\"_blank\" rel=\"noopener\">comercial (47) 98921-2991</a> está à disposição.</p>", "faq": [{"q": "Como tiro a 2ª via do boleto da MasterInfo?", "a": "Você tem três caminhos oficiais: o chat da Marina na página de boletos do site (ou no botão flutuante de boleto), o WhatsApp de atendimento (47) 3434-1734 e a Central do Assinante em sistema1.masterinfointernet.com/central_assinante_web com o seu login. O chat da Marina costuma ser o mais rápido."}, {"q": "Meu boleto está vencido, e agora?", "a": "Boleto atrasado pode precisar de atualização antes do pagamento. Peça a reemissão pelo chat da Marina ou pelo WhatsApp de atendimento. A equipe gera uma fatura atualizada para você pagar o documento correto."}, {"q": "Dá para pagar o boleto da MasterInfo por Pix?", "a": "Alguns boletos trazem um QR Code Pix quando essa opção está disponível na fatura. Se o seu tiver, é só ler o QR Code pelo app do banco. Caso não tenha, você paga normalmente pelo código de barras ou pela linha digitável."}, {"q": "Como sei se o boleto é verdadeiro e não um golpe?", "a": "Use apenas os canais oficiais (chat da Marina no site, WhatsApp de atendimento e Central do Assinante) e, antes de pagar, confira no app do banco se o beneficiário do boleto é a MasterInfo. Desconfie de boletos que chegam por contatos ou e-mails desconhecidos."}, {"q": "Qual a diferença entre os dois números de WhatsApp?", "a": "O (47) 3434-1734 é o atendimento, usado para 2ª via, dúvidas de fatura e suporte. O (47) 98921-2991 é o comercial, voltado a vendas e novas contratações. Para boletos, use o número de atendimento."}]}})


# Seções 'Sobre o bairro' (workflow pesquisa+verificação de fontes, 2026-06-22). Inseridas antes de 'Internet para cada necessidade' no gerador.
BAIRROS_DEEP = {
 "internet-jardim-paraiso-joinville": {
  "section": "<h2>Sobre o bairro Jardim Paraíso</h2>\n<p>O Jardim Paraíso é um dos bairros mais distantes do Centro de Joinville, a cerca de 10 quilômetros, e tem uma história que começa antes mesmo de ele fazer parte da cidade. A área surgiu de uma antiga ocupação na região do Cubatão e, na prática, o bairro foi desmembrado dali. O próprio nome não veio da paisagem: é a denominação que a imobiliária deu aos loteamentos Jardim Paraíso I, II, III e IV, que deram origem ao bairro.</p>\n<p>Até 6 de abril de 1992, essas terras pertenciam ao município vizinho de São Francisco do Sul. Foi a Lei estadual nº 8.563 que anexou a região a Joinville. Como bairro oficial da cidade, o Jardim Paraíso só foi formalizado depois, pela Lei nº 3.508, de 25 de junho de 1997. Hoje é um bairro grande e populoso: o censo municipal de 2014 apontou 18.072 moradores numa área de 3,22 km².</p>\n<p>É num bairro com esse tamanho e essa história de crescimento que a MasterInfo leva fibra óptica até a casa do cliente, com instalação FTTH e atendimento local de Joinville.</p>",
  "faq_extra": [
   {
    "q": "O Jardim Paraíso sempre fez parte de Joinville?",
    "a": "Não. Até 6 de abril de 1992 a região pertencia ao município vizinho de São Francisco do Sul, sendo anexada a Joinville pela Lei estadual nº 8.563. O Jardim Paraíso só foi oficializado como bairro de Joinville depois, pela Lei nº 3.508, de 25 de junho de 1997."
   },
   {
    "q": "De onde vem o nome do bairro Jardim Paraíso?",
    "a": "O nome vem da denominação que a imobiliária responsável deu aos loteamentos Jardim Paraíso I, II, III e IV, que deram origem ao bairro. A área, por sua vez, surgiu de uma antiga ocupação na região do Cubatão."
   }
  ]
 },
 "internet-jardim-sofia-joinville": {
  "section": "<h2>Sobre o bairro Jardim Sofia</h2>\n<p>O Jardim Sofia fica na zona Norte de Joinville, a mesma região do Bom Retiro, do Costa e Silva e do Dona Francisca. É um bairro relativamente novo: foi criado em 1990 e, até então, fazia parte da antiga Zona Industrial. Antes da urbanização, as terras por ali eram bastante férteis, com plantações de verduras, feijão, aipim e cana-de-açúcar, origem agrícola que ajuda a explicar o ritmo mais tranquilo de algumas ruas em comparação com o miolo da cidade.</p>\n<p>Hoje o bairro é majoritariamente residencial e tem cerca de 46 ruas e vias, entre elas a Rua Cuba e a Rua Brusque. A vizinhança conta com equipamentos públicos como o CEI Jardim Sofia, centro de educação infantil mantido pela Prefeitura de Joinville, na Rua Cuba, 85.</p>\n<p>É nesse bairro que a MasterInfo leva a fibra óptica até a casa do cliente (FTTH), com conexão pensada para o dia a dia de quem mora no Jardim Sofia.</p>",
  "faq_extra": [
   {
    "q": "Em que zona de Joinville fica o bairro Jardim Sofia?",
    "a": "O Jardim Sofia fica na zona Norte de Joinville, na mesma região dos bairros Bom Retiro, Costa e Silva e Dona Francisca."
   },
   {
    "q": "Quando o bairro Jardim Sofia foi criado?",
    "a": "O Jardim Sofia foi criado em 1990 e, até então, fazia parte da Zona Industrial de Joinville; antes da urbanização, a área tinha origem ligada à agricultura."
   }
  ]
 },
 "internet-cubatao-joinville": {
  "section": "<h2>Sobre o bairro Cubatão</h2>\n<p>A Vila Cubatão, também chamada simplesmente de Cubatão, fica na região do aeroporto de Joinville e é um dos bairros da cidade. O nome vem do rio Cubatão, que corta essa parte do município. Um ponto conhecido do bairro é a Vigorelli, localidade às margens do rio que já foi ponto de lazer da região. O rio Cubatão do Norte nasce na serra Queimada, nos contrafortes da Serra do Mar, na porção noroeste de Joinville, e percorre cerca de 88 quilômetros até desaguar no canal do Palmital, uma ramificação da baía da Babitonga.</p>\n<p>O rio sempre fez parte da história da região. Para conter as cheias, foi construído entre 1958 e 1967 um canal de derivação retificado, paralelo ao leito original, que ajuda a desviar parte da vazão nos períodos de água alta. Hoje a bacia do Cubatão, com cerca de 492 km², segue importante para o abastecimento de água de boa parte de Joinville, com captação que abastece parcela da população da cidade.</p>\n<p>É nessa região, entre o aeroporto e o vale do rio Cubatão, que a MasterInfo leva fibra óptica até a casa do cliente, com conexão por cabo de ponta a ponta (FTTH).</p>",
  "faq_extra": [
   {
    "q": "De onde vem o nome do bairro Cubatão, em Joinville?",
    "a": "O bairro leva o nome do rio Cubatão, que corta essa parte de Joinville."
   },
   {
    "q": "Onde fica a Vila Cubatão em Joinville?",
    "a": "A Vila Cubatão fica na região do aeroporto de Joinville, próxima ao vale do rio Cubatão, e é um dos bairros da cidade."
   }
  ]
 },
 "internet-nova-brasilia-joinville": {
  "section": "<h2>Sobre o bairro Nova Brasília</h2>\n<p>A região que hoje forma o Nova Brasília foi uma das primeiras a ser loteada em Joinville, principalmente em terras das famílias Mathies, Tilp, Roos e Welter. O primeiro loteamento, chamado \"Galho da Sorte\", surgiu no fim da década de 1950 e era de propriedade da família Welter. Foi a partir dele que a região começou a se transformar e a atrair moradores de várias partes da cidade.</p>\n<p>O nome veio de um acontecimento nacional: com a construção da nova capital, Brasília, o núcleo habitacional acabou ganhando o nome em homenagem a ela. O bairro foi oficializado pela Lei nº 1.526, de 5 de julho de 1977, que denominou os bairros de Joinville. Fica na zona Oeste da cidade, separado do restante de Joinville pela BR-101.</p>\n<p>É nesse bairro de origem antiga que a MasterInfo leva fibra óptica até a casa do assinante, com conexão FTTH para quem mora na região.</p>",
  "faq_extra": [
   {
    "q": "De onde vem o nome do bairro Nova Brasília, em Joinville?",
    "a": "O nome é uma homenagem à nova capital do país, Brasília. Com a construção de Brasília e o crescimento da região na época, o núcleo habitacional acabou recebendo o nome em referência ao acontecimento nacional. Fontes: publicação Joinville Bairro a Bairro (joinville.sc.gov.br) e registros sobre a história dos bairros."
   },
   {
    "q": "Qual foi o primeiro loteamento do bairro Nova Brasília?",
    "a": "Foi o loteamento 'Galho da Sorte', que surgiu no fim da década de 1950 e era de propriedade da família Welter. A partir dele a região passou a atrair moradores de várias partes de Joinville. Fonte: Joinville Bairro a Bairro (joinville.sc.gov.br)."
   }
  ]
 },
 "internet-rio-bonito-joinville": {
  "section": "<h2>Sobre o bairro Rio Bonito</h2>\n<p>O Rio Bonito é uma das ocupações germânicas mais antigas da antiga Colônia Dona Francisca, que deu origem a Joinville. Fica na zona norte da cidade, à esquerda da BR-101, e o nome vem justamente do rio que corta a região e da paisagem ao redor. Por ali, os moradores se dedicaram durante muito tempo à agricultura e à pesca, já que há rios que banham a localidade, o que ajudou a manter o tom mais rural do bairro.</p>\n<p>A história do Rio Bonito também tem a marca do trabalho dos primeiros colonos. Foram instalados na região olarias, engenhos e alambiques, o que chegou a transformar o lugar em um grande produtor de cachaça. A chegada da infraestrutura, porém, demorou: a energia elétrica só apareceu por aqui na década de 1960, e a água tratada veio depois, ao longo dos anos 1980.</p>\n<p>É nesse bairro de raízes coloniais e perfil mais tranquilo que a MasterInfo leva fibra óptica até a sua casa, com internet estável para quem vive e trabalha na região.</p>",
  "faq_extra": [
   {
    "q": "Em que zona de Joinville fica o bairro Rio Bonito?",
    "a": "O Rio Bonito fica na zona norte de Joinville, à esquerda da BR-101, na mesma região de bairros como Pirabeiraba, Dona Francisca e Costa e Silva."
   },
   {
    "q": "Por que o bairro se chama Rio Bonito?",
    "a": "O nome vem do rio que corta a região e da paisagem ao redor. O Rio Bonito é também uma das ocupações germânicas mais antigas da antiga Colônia Dona Francisca, que deu origem a Joinville."
   }
  ]
 },
 "internet-estrada-timbe-joinville": {
  "section": "<h2>Sobre a Estrada Timbé (Jardim Paraíso, Joinville)</h2>\n<p>Vale uma observação logo de início, por honestidade: a Estrada Timbé não é um bairro próprio, e sim uma via que corta o bairro <strong>Jardim Paraíso</strong>em Joinville. Quem mora por ali tem endereço com CEP 89226-499 (lado ímpar) ou 89226-500 (lado par), ambos no Jardim Paraíso. É uma região mais afastada do centro, ligada à parte da cidade onde ficam as marinas e a economia náutica de Joinville.</p>\n<p>É também uma área que vem recebendo obras de infraestrutura nos últimos anos. Em 2022, a Prefeitura de Joinville entregou a ordem de serviço para pavimentar 870 metros da Estrada Timbé, um investimento de cerca de R$ 1,9 milhão que incluiu drenagem, calçadas, meios-fios e bocas de lobo, na época, a própria Prefeitura destacou que o entorno já tinha várias casas e bastante fluxo de veículos. Em novembro de 2025, uma nova ordem de serviço liberou mais cerca de 1 km de pavimentação, com calçadas, drenagem e sinalização (cerca de R$ 2,2 milhões, majoritariamente do Ministério do Turismo), trecho que chega até as marinas. No conjunto, o Jardim Paraíso já recebeu 18 km de pavimentação asfáltica e drenagem pluvial.</p>\n<p>É justamente nessa região em crescimento, com casas espalhadas ao longo da estrada, que a MasterInfo leva fibra óptica até a residência, para quem mora num ponto mais afastado da cidade não precisar abrir mão de uma conexão estável.</p>",
  "faq_extra": [
   {
    "q": "A Estrada Timbé é um bairro de Joinville?",
    "a": "Não. A Estrada Timbé é uma via (logradouro) que fica dentro do bairro Jardim Paraíso, em Joinville. Os endereços ao longo dela usam os CEPs 89226-499 (lado ímpar) e 89226-500 (lado par)."
   },
   {
    "q": "A Estrada Timbé é pavimentada?",
    "a": "Trechos foram e estão sendo pavimentados pela Prefeitura de Joinville. Em 2022 foi autorizada a pavimentação de 870 metros (cerca de R$ 1,9 milhão) e, em novembro de 2025, mais cerca de 1 km de pavimentação com calçadas, drenagem e sinalização (cerca de R$ 2,2 milhões), em trecho que chega até as marinas."
   }
  ]
 },
 "internet-paranaguamirim-joinville": {
  "section": "<h2>Sobre o bairro Paranaguamirim</h2>\n<p>O Paranaguamirim fica na zona Sul de Joinville e é um dos maiores bairros da cidade. Pelo Censo 2022 do IBGE, é o terceiro mais populoso do município, com 33.545 moradores, atrás apenas de Aventureiro e Costa e Silva. Em área também está entre os maiores: são 11,51 km², segundo o levantamento \"Joinville Bairro a Bairro\" da Prefeitura, que registra ainda uma distância de cerca de 7,75 km até o Centro. O bairro foi oficializado pela Lei nº 3.436, de 17 de março de 1997, e integra a Subprefeitura da Região Sudeste.</p>\n<p>O nome vem do tupi-guarani: o trecho que começa no Rio Velho forma a localidade de Paranaguá-mirim, que quer dizer \"boca de rio pequeno e enseada do mar\". A história do bairro se mistura com a do vizinho Jarivatuba, moradores antigos até têm dúvida sobre onde um termina e o outro começa. A região é drenada pelo Rio Velho, que fazia a ligação com a Baía da Babitonga e com o centro da cidade e ajudou no desenvolvimento da área; até a década de 1970 boa parte das casas dependia de poços, e a rede de abastecimento de água chegou aos poucos. A ocupação humana, porém, é bem mais antiga: o entorno guarda sambaquis pré-coloniais, sítios arqueológicos registrados pela própria Prefeitura.</p>\n<p>É nesse bairro, do Jardim Edilene ao Estevão de Matos, que a MasterInfo leva fibra óptica até dentro de casa, com instalação e suporte de quem é de Joinville.</p>",
  "faq_extra": [
   {
    "q": "O que significa o nome do bairro Paranaguamirim em Joinville?",
    "a": "O nome vem do tupi-guarani. O trecho que começa no Rio Velho forma a localidade de Paranaguá-mirim, que quer dizer \"boca de rio pequeno e enseada do mar\", segundo o levantamento Joinville Bairro a Bairro da Prefeitura."
   },
   {
    "q": "O Paranaguamirim é um dos maiores bairros de Joinville?",
    "a": "Sim. Pelo Censo 2022 do IBGE, é o terceiro bairro mais populoso de Joinville, com 33.545 moradores, e também está entre os maiores em área, com 11,51 km²."
   }
  ]
 }
}
