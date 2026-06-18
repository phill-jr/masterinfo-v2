# Plano Editorial — Conteúdo SEO/GEO MasterInfo

> Camada de conteúdo do site (blog + páginas-pilar) para crescer tráfego orgânico local, autoridade tópica e citação em IAs (GEO). Tudo **estático**, gerado pelo `gerar_subpaginas.py`, sem banco/WordPress. Fundamentado em dados **reais** do Google Search Console (`sc-domain:masterinfointernet.com`, últimos 3 meses) e na estrutura de páginas que já rankeiam no Google BR.

## Arquitetura — Hub & Spoke (2 camadas)

- **Camada A — Páginas-Pilar comerciais** (landing, intenção de compra, maior ROI): `/internet-joinville/` (hub da cidade), `/internet-empresarial/` (gap de página), `/melhor-internet-joinville/` (comparativa avaliativa).
- **Camada B — Blog informacional** (`/blog/`, topo de funil, GEO, E-E-A-T): posts que respondem perguntas e **linkam internamente** para os planos e pilares (fluxo de autoridade blog → conversão).

## Onda 1 — construir agora

| # | Página / Post | Keyword-alvo (impressões reais GSC) | Intenção | Tipo | Hub | Link interno | Autor | Prio |
|---|---|---|---|---|---|---|---|---|
| A1 | `/internet-joinville/` | internet joinville (45), internet em joinville (27), internet fibra joinville (32), internet joinville fibra (31), internet residencial joinville (9), provedor de internet joinville (6) | Comercial/local | Pilar | Cidade | → /familia/, /home-office/, /gamer/, checkout | Philipe (Fundador) | P0 |
| A2 | `/internet-empresarial/` | internet empresarial (11, pos 54.9), plano de internet empresarial (13), internet empresa (3), planos empresariais (2) | Comercial/B2B | Pilar | Empresarial (gap) | → contato, WhatsApp comercial 5547989212991, checkout | Philipe (Fundador) | P0 |
| A3 | `/melhor-internet-joinville/` | melhor internet joinville (12, pos 2.9, **0 cliques**), melhores internet fibra joinville (9), melhor internet fibra joinville (5), qual a melhor internet de joinville (5) | Comercial/avaliativa | Pilar comparativo | Cidade | → /internet-joinville/, checkout | Philipe (Fundador) | P1 |
| B0 | `/blog/` (índice) | — (hub de autoridade) | Navegacional | Índice | Blog | → todos os posts | Equipe MasterInfo | P0 |
| B1 | Quantos Mega de internet você precisa? Guia por perfil | apoia seleção de plano; internet planos (1) | Informacional→comercial | Post (guia) | Planos | → /familia/, /gamer/, /home-office/, /com-2-roteadores/, checkout | Equipe Técnica | P1 |
| B2 | Fibra óptica vs rádio vs cabo: o que é e qual a melhor | internet fibra ótica (2), internet por fibra óptica (1), internet óptica (1), o que é fibra (GEO) | Informacional/definicional | Post | Tecnologia | → /internet-joinville/, /melhor-internet-joinville/ | Equipe Técnica | P1 |
| B3 | Como saber se tem fibra no seu endereço (cobertura por CEP) | internet no meu cep (2), internet wifi perto de mim (1), instalação de internet residencial (2), internet em joinville sc (4) | Informacional→ação | Post (passo a passo) | Cobertura | → modal de cobertura, /internet-joinville/, checkout | Equipe Técnica | P2 |
| B4 | Wi-Fi lento ou caindo? Como melhorar o sinal em casa | apoia /ajuda/wifi/; internet wifi (1) | Informacional/troubleshooting | Post (dicas) | Wi-Fi | → /ajuda/wifi/, /com-2-roteadores/, chat Marina | Equipe Técnica | P2 |

> **Autor técnico:** os posts B1–B4 nascem assinados por **Equipe Técnica MasterInfo** (real, não autor fake). Quando o nome/cargo do técnico for definido, troca-se em um único lugar (`BLOG` no gerador) — E-E-A-T melhora para autor-pessoa.

## Onda 2 — backlog (após validar a Onda 1)

| Post | Sinal/keyword | Hub | Link interno |
|---|---|---|---|
| A internet caiu? Passo a passo pra voltar a conectar | troubleshooting; apoia /ajuda/reportar/ | Suporte | → /ajuda/reportar/, Marina |
| Como funciona a instalação da fibra (e quanto tempo leva) | instalação de internet residencial (2) | Cobertura | → /internet-joinville/, checkout |
| Internet para empresas: o que considerar antes de contratar | internet empresa (3) | Empresarial | → /internet-empresarial/ |
| SKY+ Light e os apps inclusos: como funciona o PlayHub | sky+ light (22, pos 8.4, 0 cliques) | Apps | → /aplicativos/sky-light/, /playhub/ |
| 2ª via de boleto MasterInfo: como emitir e pagar | master fatura 2 via, master boleto, portal do assinante master | Suporte | → /ajuda/boletos/ |

## Princípios editoriais (todos os posts)

- **TL;DR answer-first** no topo (caixa de resposta direta — featured snippet + citação em IA/GEO).
- **Schema** `BlogPosting` (headline, author, datePublished, dateModified, image, publisher) + `BreadcrumbList` (Início › Blog › Post) + `FAQPage` quando houver perguntas.
- **Link interno obrigatório** para ≥1 plano e/ou ≥1 pilar.
- Tom conversacional e local ("aqui em Joinville", "equipe da região"). Sem cara-de-IA, sem em-dash (alinhado ao pass `home-refresh`).

## Blueprints validados por SERP (o que já rankeia fora de Joinville)

- `/melhor-internet-joinville/` → modelo melhorplano.net/Florianópolis: longa (3.000+ palavras), critérios + FAQ + CTA de CEP. **Ângulo avaliativo por critérios** (não "TOP 5" fingindo neutralidade — a MasterInfo é parte interessada).
- `/internet-empresarial/` → modelo Alares/internet dedicada: ~1.500 palavras, "o que é → vantagens → dedicada x compartilhada → para quem → CTA". + FAQ (ganho de SEO).
- B1 Quantos Mega → modelo melhorplano: tabela atividade × Mbps + FAQ; recomendação mapeada aos planos MasterInfo.
- B2 Fibra vs rádio vs cabo → padrão Tecnoblog/Brisanet: tecnologia → velocidade → estabilidade → cobertura → "qual é melhor" + FAQ.
- **Diferencial competitivo a explorar:** provedor regional ganha no ângulo "suporte local + atendimento próximo" — exatamente a MasterInfo (+6 anos em Joinville, equipe da região).

## Estratégia de imagens (sem violar direito autoral)

🔴 NÃO reutilizar imagens das páginas-base (concorrentes). Fontes legítimas: **(a)** acervo próprio do site, **(b)** Freepik licenciado/gerado, **(c)** HTML/CSS (tabela/diagrama).

- **Reuso próprio** (autêntico, melhor E-E-A-T): `imgs/historia/{sede-fachada,momento-time-tecnico,momento-frota,momento-atendimento,turma-toda}.jpg`, `imgs/hero/sub/{familia,home-office,gamer,2-roteadores}-*.jpg`, `imgs/wifi6.svg`, `imgs/depoimentos/*`.
- **Gerar via Freepik (~2–4):** hero B2B (empresarial), conceito fibra óptica (B2), mapa/Joinville (B3), banner do blog (opcional).
- **Autores:** `historia/fundador-philipe.jpg` (Philipe); foto do técnico a fornecer.

## Pipeline & técnico

- Páginas geradas por funções no `gerar_subpaginas.py` (usam `head()/header()/footer()` → nascem compatíveis com os syncs) e registradas em `MENU_PAGES` + `SEO_META` → canonical/og/schema/menus aplicados automaticamente pelo default `--menus`. **Nunca `--full`** (reverte corpos).
- Blog gerado por flag dedicado (`--blog`). Sitemap atualizado manualmente com as novas URLs.

## Métrica de sucesso (revisar em 2–4 semanas)

Re-rodar no GSC `find_quick_wins` / `find_content_gaps` / `seo_health_check` e medir: cliques nas queries-alvo, posição média do cluster "internet joinville", e descoberta/indexação das novas URLs.
