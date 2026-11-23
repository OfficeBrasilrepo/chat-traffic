"""Resumo da medição da chat-traffic: lê chat-traffic-uso.csv (ao lado do CONTINUAR.md)
e mostra, por lugar onde a tarefa foi feita, quantas tarefas, passos médios,
contexto médio e % do limite de 5 h gasto por tarefa.
Uso: python relatorio.py [caminho.csv] [--desde AAAA-MM-DD]   Teste: python relatorio.py --teste"""
import csv, os, sys, tempfile
from collections import Counter, defaultdict

ONDES = {"aqui", "subagente", "chat-parado", "chat-novo"}
COLUNAS = "data,chat,tarefa,onde,modelo,esforco,passos,contexto_inicio,contexto_fim,plano5h_inicio,plano5h_fim"


def numero(v):
    try:
        return float(v) if v and v.strip() else None
    except ValueError:
        return None


def resumo(caminho, desde=""):
    grupos = defaultdict(list)
    puladas = 0
    with open(caminho, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            # vírgula solta num texto empurra as colunas: a linha não entra na conta
            if None in r or None in r.values() or r["onde"] not in ONDES:
                puladas += 1
                continue
            if r["data"] >= desde:  # datas AAAA-MM-DD comparam como texto
                grupos[r["onde"]].append(r)
    if puladas:
        print(f"{puladas} linha(s) com colunas fora do lugar (vírgula num texto?) ficaram de fora.")
    mod = Counter(r["modelo"].split("-")[0].strip().lower() or "?" for rs in grupos.values() for r in rs)
    print("modelos: " + ", ".join(f"{m} {n}" for m, n in mod.most_common()))
    linhas = []
    for onde, rs in sorted(grupos.items()):
        num = lambda c: [x for x in (numero(r[c]) for r in rs) if x is not None]
        media = lambda v: sum(v) / len(v) if v else 0
        # contexto do fim: é o que a skill grava sempre (o do começo quase nunca)
        gasto = [numero(r["plano5h_fim"]) - numero(r["plano5h_inicio"]) for r in rs
                 if numero(r["plano5h_inicio"]) is not None and numero(r["plano5h_fim"]) is not None]
        linhas.append((onde, len(rs), media(num("passos")), media(num("contexto_fim")), media(gasto)))
    return linhas


def mostrar(linhas):
    print(f"{'onde':<14}{'tarefas':>8}{'passos':>8}{'contexto':>10}{'% 5h/tarefa':>13}")
    for onde, n, p, c, g in linhas:
        print(f"{onde:<14}{n:>8}{p:>8.1f}{c/1000:>9.0f}k{g:>12.1f}%")
    print("% do limite de 5 h é da conta inteira: outros chats abertos ao mesmo tempo somam junto (medida aproximada).")


def teste():
    p = os.path.join(tempfile.mkdtemp(), "u.csv")
    open(p, "w", encoding="utf-8").write(COLUNAS + "\n"
        "2026-11-16,a,t1,aqui,opus,medio,4,200000,220000,10,12\n"
        "2026-11-16,b,t2,chat-novo,sonnet,baixo,20,65000,165000,12,20\n"
        "2026-11-16,c,t3,aqui,opus,medio,6,100000,120000,20,21\n"
        "2026-11-16,d,t4,aqui,sonnet,baixo,,,,,\n"
        "2026-11-16,e,ajuste de cor, botão,aqui,opus,medio,3,,,,\n")
    l = dict((x[0], x) for x in resumo(p))
    assert l["aqui"][1] == 3 and l["aqui"][2] == 5 and l["aqui"][4] == 1.5, l
    assert l["chat-novo"][3] == 165000 and l["aqui"][3] == 170000, l  # a linha com vírgula ficou de fora
    open(p, "a", encoding="utf-8").write("2026-11-24,f,t5,aqui,haiku,baixo,2,,,,\n")
    assert dict((x[0], x) for x in resumo(p, "2026-11-24"))["aqui"][1] == 1
    print("ok")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--teste" in sys.argv:
        teste()
    else:
        livres = [a for i, a in enumerate(sys.argv[1:], 1) if a != "--desde" and sys.argv[i - 1] != "--desde"]
        arq = livres[0] if livres else "chat-traffic-uso.csv"
        if not os.path.isfile(arq):
            sys.exit(f"Sem {arq} nesta pasta: rode na raiz de um projeto que já mediu tarefas.")
        desde = sys.argv[sys.argv.index("--desde") + 1] if "--desde" in sys.argv else ""
        mostrar(resumo(arq, desde))
