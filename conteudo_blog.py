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
        "img": "/imgs/historia/fundador-philipe.jpg", "url": "/#nossa-historia",
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
        "img": "/imgs/historia/fundador-philipe.jpg", "url": "/#nossa-historia",
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
# body = HTML entre o hero e o bloco de planos/FAQ. faq = [(pergunta, resposta), ...].

PILARES = [
    {
        "slug": "internet-joinville",
        "title": "Internet Fibra em Joinville | Planos e Cobertura | MasterInfo",
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
      <strong>Resumo rápido:</strong> a MasterInfo é um provedor de <strong>internet 100% fibra óptica em Joinville</strong>, com planos a partir de 600 Mega, Wi-Fi 6 incluso e instalação rápida. O diferencial é o <strong>suporte local</strong>: equipe da região, sem call center distante. Consulte a cobertura no seu endereço e contrate em minutos.
    </div>

    <h2>Por que escolher uma internet fibra em Joinville</h2>
    <p>Joinville é a maior cidade de Santa Catarina e cresce rápido, com bairros novos e demanda cada vez maior por internet estável para trabalho remoto, estudo e streaming. A fibra óptica é, hoje, a melhor tecnologia disponível na cidade: ela leva o sinal por luz dentro de um cabo de vidro, sem a interferência e a instabilidade da internet via rádio ou dos cabos antigos.</p>
    <p>Na prática, isso significa <strong>mesma velocidade de dia e de noite</strong>, navegação que não cai quando chove e latência baixa para chamadas de vídeo e jogos. Para entender as diferenças entre as tecnologias, leia <a href="/blog/fibra-vs-radio-vs-cabo/">fibra óptica vs rádio vs cabo</a>.</p>

    <h2>Planos de internet em Joinville</h2>
    <p>Nossos planos vão de 600 Mega (ideal para apartamento e casa pequena) até 1 Giga (para casa cheia, com muita gente conectada ao mesmo tempo). Todos incluem <strong>roteador Wi-Fi 6</strong> e pelo menos 1 app de TV ou streaming por mês. Veja as opções abaixo e escolha pela sua realidade:</p>

    <!--PLANS_GRID-->

    <h2>Cobertura: tem fibra no seu bairro?</h2>
    <p>Atendemos grande parte de Joinville com rede própria de fibra. A forma mais rápida de saber se já chegamos no seu endereço é <strong>consultar a cobertura pelo CEP</strong> aqui no site, em poucos segundos. Se preferir o passo a passo, leia <a href="/blog/cobertura-fibra-cep-joinville/">como saber se tem fibra no seu endereço</a>.</p>
    <p>Já atendemos regiões como Centro, América, Glória, Bom Retiro, Boa Vista, Vila Nova, Costa e Silva, Iririú e muitos outros bairros, com expansão constante para novas áreas.</p>

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
    <p>Tem provedor grande que atende metade do Brasil de um call center distante. A MasterInfo é diferente: somos <strong>de Joinville, para Joinville</strong>, há mais de 6 anos. Quando você fala com a gente, fala com alguém da região, que conhece a cidade e resolve rápido. É o motivo de termos <strong>4,9 de 5 estrelas</strong> com milhares de avaliações no Google.</p>
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
        "title": "Internet Empresarial em Joinville (Link Dedicado) | MasterInfo",
        "desc": "Internet empresarial em Joinville: link dedicado em fibra óptica, banda garantida, IP fixo, SLA e suporte local prioritário. Peça uma proposta.",
        "tag": "INTERNET · EMPRESAS",
        "h1": "Internet empresarial em Joinville, com banda garantida",
        "lead": "Link dedicado em fibra óptica para a sua empresa em Joinville: velocidade garantida em download e upload, IP fixo, SLA e suporte prioritário de uma equipe que fica na cidade.",
        "hero_img": "/imgs/hero/sub/home-office-1.jpg",
        "gradient": "linear-gradient(135deg, #0a1f44 0%, #14366b 50%, #1f5fa8 100%)",
        "cta": "Pedir proposta empresarial",
        "cta_whatsapp": "5547989212991",
        "plans": [],
        "body": """
    <div class="tldr">
      <strong>Resumo rápido:</strong> a internet empresarial da MasterInfo é um <strong>link dedicado em fibra óptica</strong> em Joinville: a banda contratada é só sua (não dividida com vizinhos), com a <strong>mesma velocidade de download e upload</strong>, IP fixo, SLA de disponibilidade e suporte prioritário local. Ideal para empresas que dependem de internet estável o tempo todo. <a href="https://wa.me/5547989212991">Peça uma proposta no WhatsApp</a>.
    </div>

    <h2>O que é internet empresarial (link dedicado)</h2>
    <p>Internet empresarial não é a mesma coisa que o plano residencial. Em um <strong>link dedicado</strong>, a banda contratada é exclusiva da sua empresa: ninguém mais compartilha aquela capacidade. O resultado é uma conexão estável e previsível, com <strong>velocidade simétrica</strong> (download e upload iguais) e garantia de entrega, mesmo nos horários de pico.</p>

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
        "title": "Qual a Melhor Internet de Joinville? Critérios para Escolher | MasterInfo",
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
      <strong>Resumo rápido:</strong> a melhor internet de Joinville é a que combina <strong>fibra óptica</strong>, <strong>estabilidade real</strong> (não só velocidade no papel), <strong>suporte local que resolve</strong> e <strong>boa reputação</strong>. Provedores regionais costumam ganhar no atendimento. A MasterInfo atende esses critérios com 4,9/5 no Google e equipe 100% de Joinville.
    </div>

    <p class="article-note">Transparência: a MasterInfo é um provedor de Joinville, então esta página tem o nosso ponto de vista. Em vez de um ranking "neutro" de concorrentes, listamos os <strong>critérios objetivos</strong> que você deve usar para decidir, seja qual for o provedor.</p>

    <h2>1. Tecnologia: fibra óptica até a sua casa</h2>
    <p>O primeiro filtro é a tecnologia. Fibra óptica (FTTH, fibra até a casa) é mais estável e rápida que internet via rádio ou cabo antigo, e não sofre com chuva ou interferência. Se o provedor não leva fibra até o seu imóvel, dificilmente será a melhor opção. Entenda melhor em <a href="/blog/fibra-vs-radio-vs-cabo/">fibra vs rádio vs cabo</a>.</p>

    <h2>2. Estabilidade real, não só velocidade no papel</h2>
    <p>Velocidade alta no contrato não significa nada se a conexão cai à noite ou trava quando todo mundo está usando. O que importa é a <strong>estabilidade no dia a dia</strong>: a mesma velocidade de manhã e às 21h, latência baixa para chamadas e jogos, e zero quedas. Pergunte a vizinhos e olhe avaliações que falem de estabilidade, não só de preço.</p>

    <h2>3. Suporte local que resolve</h2>
    <p>Esse é o critério que mais separa um bom provedor de um provedor qualquer. Quando a internet cai, você quer falar com alguém que entende e resolve, não esperar horas num call center. Provedores regionais como a MasterInfo têm <strong>equipe na cidade</strong>, técnicos que conhecem os bairros e tempo de resposta menor.</p>

    <h2>4. Reputação e avaliações reais</h2>
    <p>Avaliações no Google e indicações de quem já é cliente valem mais que qualquer propaganda. A MasterInfo tem <strong>4,9 de 5 estrelas</strong> com milhares de avaliações, reflexo de mais de 6 anos conectando famílias e empresas em Joinville.</p>

    <h2>5. Preço justo e sem letra miúda</h2>
    <p>O mais barato nem sempre é o melhor, e o mais caro também não. Procure um plano com <strong>preço claro</strong>, sem surpresas na fatura, com o que está incluso bem explicado (roteador, apps, suporte). Veja os planos da MasterInfo abaixo, com preço transparente e desconto por pagamento em dia.</p>

    <!--PLANS_GRID-->

    <h2>Como aplicar tudo isso na prática</h2>
    <p>Resumindo: priorize fibra óptica, confirme a estabilidade com quem mora perto, valorize o suporte local e cheque as avaliações. Se quiser ir direto ao ponto, veja o <a href="/internet-joinville/">guia de internet em Joinville</a> ou descubra <a href="/blog/quantos-mega-de-internet-voce-precisa/">quantos Mega você precisa</a>.</p>
""",
        "faq": [
            ("Qual é a melhor internet de Joinville?", "Não há uma resposta única para todos, mas a melhor internet é a que reúne fibra óptica até a sua casa, estabilidade real no dia a dia, suporte local que resolve e boa reputação. A MasterInfo atende esses critérios com nota 4,9/5 no Google e equipe 100% de Joinville."),
            ("Provedor local é melhor que operadora grande?", "Em atendimento, quase sempre sim. Provedores regionais têm equipe na cidade, conhecem os bairros e respondem mais rápido. Em fibra óptica, a qualidade do sinal de um bom provedor local costuma igualar ou superar a das grandes."),
            ("Como confirmar a estabilidade antes de contratar?", "Pergunte a vizinhos que já usam o provedor, leia avaliações que falem de quedas e velocidade à noite (não só de preço) e confirme se a tecnologia é fibra óptica até o imóvel."),
            ("A MasterInfo atende meu bairro?", "Atendemos boa parte de Joinville com fibra própria. Consulte a cobertura pelo seu CEP aqui no site para confirmar em segundos."),
        ],
    },
]

# ─── BLOG (posts informacionais) ──────────────────────────────────────────
# slug → /blog/slug/ (depth 2). author = chave em AUTHORS. image = destaque (og).
BLOG = [
    {
        "slug": "quantos-mega-de-internet-voce-precisa",
        "title": "Quantos Mega de Internet Você Precisa? Guia por Perfil | MasterInfo",
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
    <p>Muita gente, muitos cômodos: além de <strong>800 Mega a 1 Giga</strong>, considere <a href="/com-2-roteadores/">Wi-Fi com 2 roteadores</a> para não ter ponto cego.</p>

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
        "title": "Fibra Óptica vs Rádio vs Cabo: Qual a Melhor Internet? | MasterInfo",
        "desc": "Fibra óptica, internet via rádio ou cabo: entenda as diferenças de velocidade, estabilidade e cobertura, e descubra qual é a melhor internet pra você.",
        "h1": "Fibra óptica vs rádio vs cabo: qual a melhor internet?",
        "lead": "Os três tipos de conexão mais comuns no Brasil têm diferenças grandes de estabilidade e velocidade. Entenda cada um em linguagem simples e veja por que a fibra virou o padrão.",
        "author": "tecnica",
        "date": DATE_DEFAULT,
        "image": "/imgs/wifi6.svg",
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
    <p>A fibra não sofre interferência eletromagnética, não perde sinal com a chuva e mantém a mesma velocidade independentemente da distância (dentro do projeto da rede). Para quem mora na cidade, como em <a href="/internet-joinville/">Joinville</a>, é disparado a melhor opção: estável de dia e de noite, com latência baixa para chamadas e jogos.</p>

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
        "title": "Como Saber se Tem Fibra no Seu Endereço em Joinville | MasterInfo",
        "desc": "Veja como descobrir se tem internet fibra no seu endereço em Joinville: consulta de cobertura por CEP, passo a passo e o que fazer se ainda não chegou.",
        "h1": "Como saber se tem fibra no seu endereço em Joinville",
        "lead": "Antes de contratar, vale confirmar se a fibra já chegou na sua rua. Dá pra checar em segundos pelo CEP, sem precisar ligar pra ninguém. Veja o passo a passo.",
        "author": "tecnica",
        "date": DATE_DEFAULT,
        "image": "/imgs/hero/sub/2-roteadores-1.jpg",
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
        "title": "Wi-Fi Lento ou Caindo? Como Melhorar o Sinal em Casa | MasterInfo",
        "desc": "Wi-Fi lento, travando ou com ponto cego? Veja dicas práticas para melhorar o sinal em casa: posição do roteador, canais, senha e quando usar mesh.",
        "h1": "Wi-Fi lento ou caindo? Como melhorar o sinal em casa",
        "lead": "Às vezes a internet é boa, mas o Wi-Fi não chega direito em todo canto da casa. A maioria dos problemas se resolve com ajustes simples. Veja o que fazer antes de chamar o suporte.",
        "author": "tecnica",
        "date": DATE_DEFAULT,
        "image": "/imgs/hero/sub/2-roteadores-2.jpg",
        "tags": ["Wi-Fi", "Dicas", "Suporte"],
        "body": """
    <div class="tldr">
      <strong>Resposta rápida:</strong> a maioria dos problemas de Wi-Fi vem de <strong>posição ruim do roteador</strong>. Coloque-o num ponto <strong>central e alto</strong>, longe de paredes grossas, micro-ondas e espelhos. Reinicie quando travar, mantenha a senha protegida e, em casas grandes, use <strong>2 roteadores em mesh</strong>. Se nada resolver, fale com o suporte.
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
]
