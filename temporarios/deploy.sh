#!/usr/bin/env bash
# ============================================================
# Deploy da v2 -> PRODUCAO (masterinfointernet.com @ 45.168.4.18, DirectAdmin)
# Uso (PowerShell/cmd):  wsl bash "temporarios/deploy.sh"
#   (ou no WSL):         bash temporarios/deploy.sh
# Auth: chave SSH (sem senha). Aplica via receptor root NOPASSWD escopado.
# Protege na producao: secrets/ .well-known/ faq/ telefonia/ (nao sao tocados).
# IMPORTANTE: usa git.exe (Windows) p/ o pull — o git do WSL trata fim-de-linha
#   diferente e gera churn CRLF/conflitos em massa. NUNCA trocar por 'git' puro.
# config.json E deployado (conteudo vem do repo). Edite pelo admin LOCAL + deploy,
#   nao pelo admin de producao (seria sobrescrito).
# ============================================================
set -euo pipefail

REPO="/mnt/c/Users/Philipe Alves/Masterinfo/masterinfo-v2"
WIN_REPO='C:\Users\Philipe Alves\Masterinfo\masterinfo-v2'
KEY_WIN="/mnt/c/Users/Philipe Alves/.ssh/id_ed25519_masterinfo"
HOST="philipe@45.168.4.18"
PORT=9152
STAGING="/home/philipe/v2_staging"

g() { git.exe -C "$WIN_REPO" "$@"; }

# ---- 0) Trava de colaboracao: git pull --rebase antes (Eike commita direto) ----
if command -v git.exe >/dev/null 2>&1; then
  BRANCH=$(g rev-parse --abbrev-ref HEAD 2>/dev/null | tr -d '\r' || true)
  if [ -z "$BRANCH" ] || [ "$BRANCH" = "HEAD" ]; then echo "ERRO: detached HEAD. Abortando."; exit 1; fi
  UPSTREAM=$(g rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null | tr -d '\r' || true)
  if [ -n "$UPSTREAM" ]; then
    RN="${UPSTREAM%%/*}"
    g fetch "$RN" "$BRANCH" || { echo "ERRO: git fetch falhou."; exit 1; }
    LOCAL=$(g rev-parse HEAD | tr -d '\r'); REMOTE=$(g rev-parse "$UPSTREAM" | tr -d '\r')
    if [ "$LOCAL" != "$REMOTE" ]; then
      g pull --rebase --autostash "$RN" "$BRANCH" || { echo "ERRO: git pull falhou (conflito?). Resolva e rode de novo."; exit 1; }
    fi
    echo "git: $BRANCH sincronizado com $UPSTREAM"
  else
    echo "AVISO: $BRANCH sem upstream — pulando git pull."
  fi
else
  echo "ERRO: git.exe (Windows) nao encontrado no WSL. Abortando (nao usar git do WSL)."; exit 1
fi

# ---- 0.5) config.json: a FONTE e o admin de PRODUCAO ----
# O conteudo (planos, etc.) e editado no admin do site NO AR. Pra o rsync (repo->prod)
# NAO sobrescrever essas edicoes, puxamos o config.json atual de producao pro repo
# ANTES de enviar. config.json e publico (o site faz fetch). Valida que e JSON; se
# falhar, mantem o do repo (nao-fatal). Commita (git.exe) pra deixar a arvore limpa.
# CONSEQUENCIA: editar config.json direto no repo NAO adianta — seria sobrescrito aqui.
#   Pra mudar conteudo, use o admin de producao.
echo "== puxando config.json de producao -> repo (admin de prod e a fonte) =="
TMPCFG=$(mktemp)
if curl -fsS "https://masterinfointernet.com/config.json?cb=$(date +%s%N)" -o "$TMPCFG" \
   && python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$TMPCFG" 2>/dev/null; then
  if ! cmp -s "$TMPCFG" "$REPO/config.json"; then
    cp "$TMPCFG" "$REPO/config.json"
    g add config.json >/dev/null 2>&1 || true
    g commit -m "chore(config): sync config.json do admin de producao" >/dev/null 2>&1 || true
    echo "  config.json de producao copiado + commitado (estava diferente do repo)."
  else
    echo "  config.json do repo ja esta igual ao de producao."
  fi
else
  echo "  AVISO: nao consegui puxar/validar config.json de producao — mantendo o do repo."
fi
rm -f "$TMPCFG"

# ---- 0.7) recortes de celular: todo imgs/mobile/*.jpg citado tem que existir em disco ----
# No celular o hero das subpaginas troca a foto por CSS (style id="hero-m") para um recorte
# em imgs/mobile/. Se um HTML/JSON citar um recorte que nao esta em disco, o rsync publicaria
# pagina apontando para arquivo inexistente. Aborta antes (conserto: python gerar_subpaginas.py).
echo "== conferindo recortes de celular citados =="
python3 - "$REPO" <<'PY' || { echo "ERRO: paginas desatualizadas (recorte de celular ausente ou escala do site diferente do config). Rode 'python gerar_subpaginas.py' no Windows, confira imgs/mobile/ e rode o deploy de novo. Deploy abortado."; exit 1; }
import json, os, re, sys
repo = sys.argv[1]
pasta = os.path.join(repo, "imgs", "mobile")
# nomes exatos (maiusculas/minusculas contam em producao) e so arquivos com conteudo
em_disco = set(f for f in (os.listdir(pasta) if os.path.isdir(pasta) else [])
               if os.path.getsize(os.path.join(pasta, f)) > 0)
falta = set()
n = 0
for raiz, dirs, arqs in os.walk(repo):
    dirs[:] = [d for d in dirs if d not in (".git", "temporarios", "node_modules", "__pycache__", "masterinfointernet.com-audit")]
    for a in arqs:
        if not a.endswith((".html", ".json")):
            continue
        try:
            s = open(os.path.join(raiz, a), encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        for m in set(re.findall(r"""imgs/mobile/([^"'()\s<>]+?\.jpg)""", s)):
            n += 1
            for nome in (m, m + ".webp"):
                if nome not in em_disco:
                    falta.add("imgs/mobile/" + nome)
if falta:
    print("  faltando (ou vazio): " + ", ".join(sorted(falta)))
    sys.exit(1)
print("  %d citacao(oes) de recorte, todos os arquivos em disco." % n)
# A condicao de tela do recorte depende da escala do site (config.layout.siteScale) e fica
# gravada no HTML pelo gerador. Se a escala do config (que acabou de vir de producao) nao e
# a que esta gravada nas paginas, o HTML esta desatualizado em relacao ao config.
try:
    escala = round((json.load(open(os.path.join(repo, "config.json"), encoding="utf-8")).get("layout", {}).get("siteScale", 100) or 100) / 100, 3)
    m = re.search(r"--site-scale:([0-9.]+)", open(os.path.join(repo, "familia", "index.html"), encoding="utf-8", errors="ignore").read())
    if m and abs(float(m.group(1)) - escala) > 1e-9:
        print("  escala do site no config.json (%s) difere da gravada nas paginas (%s)." % (escala, m.group(1)))
        sys.exit(1)
except SystemExit:
    raise
except Exception as e:
    print("  aviso: nao conferi a escala do site (%s)" % type(e).__name__)
PY

# ---- 1) chave SSH com permissao 600 (/mnt/c nao mantem 600) ----
KEY=/tmp/dk_masterinfo
cp "$KEY_WIN" "$KEY" && chmod 600 "$KEY"
SSHC="ssh -i $KEY -o StrictHostKeyChecking=accept-new -o BatchMode=yes -p $PORT"

# ---- 2) rsync local -> staging (exclui dev + protegidos de runtime) ----
echo "== enviando arquivos para o staging =="
rsync -az --delete -e "$SSHC" \
  --exclude='.git/' --exclude='.github/' --exclude='temporarios/' --exclude='__pycache__/' \
  --exclude='*.md' --exclude='.gitignore' --exclude='.claude/' --exclude='*.tmp' \
  --exclude='secrets/' --exclude='.well-known/' --exclude='faq/' --exclude='telefonia/' \
  "$REPO/" "$HOST:$STAGING/"

# ---- 3) aplicar no docroot (receptor root) ----
echo "== aplicando no docroot de producao =="
$SSHC "$HOST" 'sudo -n /usr/local/sbin/deploy-masterinfo-v2.sh'

# ---- 4) smoke test publico ----
echo "== smoke test https://masterinfointernet.com =="
ok=1
for p in "" "index-light.html" "contato/" "checkout.html" "api/marina.php"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 12 "https://masterinfointernet.com/$p?cb=$(date +%s%N)" 2>/dev/null || echo ERR)
  mk=$(curl -s --max-time 12 "https://masterinfointernet.com/$p?cb=$(date +%s%N)" 2>/dev/null | grep -cE '^(<{7}|={7}|>{7})' || true)
  echo "  /$p -> $code (marcadores: $mk)"
  { [ "$code" = "200" ] && [ "$mk" = "0" ]; } || ok=0
done
[ "$ok" = "1" ] && echo "✅ DEPLOY COMPLETO." || echo "⚠️ DEPLOY aplicado, mas algo != 200 ou com marcador — confira acima."
