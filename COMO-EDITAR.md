# Como editar o site MasterInfo

## 1. Acessar o projeto
- Repositório: **github.com/phill-jr/masterinfo-v2**
- Site no ar: **https://phill-jr.github.io/masterinfo-v2/**
- Peça ao Philipe pra te adicionar como colaborador (Settings → Collaborators).

## 2. Baixar pro seu PC (uma vez só)
```
git clone https://github.com/phill-jr/masterinfo-v2.git
cd masterinfo-v2
```

## 3. Ver o site localmente antes de subir
```
python -m http.server 8091
```
Abre no navegador: **http://localhost:8091/**
(Sempre que mexer, dá **Ctrl + Shift + R** pra recarregar sem cache.)

## 4. Onde ficam as Landing Pages
| Página | Arquivo |
|---|---|
| Home | `index.html` |
| TV e Streaming | `tv-streaming/index.html` |
| Internet (Família, Gamer, etc.) | `familia/`, `gamer/`, `home-office/`, `com-1-roteador/`, `com-2-roteadores/` |
| Aplicativos (SKY, Disney+, etc.) | `aplicativos/<nome>/index.html` |

> As páginas de **Internet** e **Aplicativos** são GERADAS pelo script `gerar_subpaginas.py`.
> Pra mudar essas, edite o script e rode: `python gerar_subpaginas.py` (NÃO edite os HTML direto, senão perde na próxima geração).
> A Home e a TV/Streaming você edita o HTML direto.

- Estilo visual de tudo: `styles.css`
- Imagens: pasta `imgs/`

## 5. Regra importante ao mexer no CSS
Toda vez que mudar `styles.css`, troque a "versão" no topo do HTML pra forçar atualização:
`styles.css?v=20260531-l` → mude a última letra (`-m`, `-n`...).

## 6. Salvar e publicar
```
git add -A
git commit -m "descreva o que mudou"
git push
```
Em ~1 minuto já aparece no site no ar.

## 7. Pegar atualizações de outras pessoas (antes de começar)
```
git pull
```

---
Dúvida? Fala com o Philipe.
