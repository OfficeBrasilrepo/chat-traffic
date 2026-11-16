"""Resumo da medição da chat-traffic: lê chat-traffic-uso.csv (raiz do projeto)
e mostra, por lugar onde a tarefa foi feita, quantas tarefas, passos médios,
contexto médio e % do limite de 5 h gasto por tarefa.
Uso: python relatorio.py [caminho.csv]   Teste: python relatorio.py --teste"""
import csv, os, sys, tempfile
from collections import defaultdict

COLUNAS = "data,chat,tarefa,onde,modelo,esforco,passos,contexto_inicio,contexto_fim,plano5h_inicio,plano5h_fim"


def resumo(caminho):
    grupos = defaultdict(list)
    with open(caminho, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            grupos[r["onde"]].append(r)
    linhas = []
    for onde, rs in sorted(grupos.items()):
        num = lambda c: [float(r[c]) for r in rs if r.get(c, "").strip()]
        media = lambda v: sum(v) / len(v) if v else 0
        ctx = [(float(r["contexto_inicio"]) + float(r["contexto_fim"])) / 2 for r in rs if r["contexto_inicio"] and r["contexto_fim"]]
        gasto = [float(r["plano5h_fim"]) - float(r["plano5h_inicio"]) for r in rs if r["plano5h_inicio"] and r["plano5h_fim"]]
        linhas.append((onde, len(rs), media(num("passos")), media(ctx), media(gasto)))
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
        "2026-11-16,d,t4,aqui,sonnet,baixo,,,,,\n")
    l = dict((x[0], x) for x in resumo(p))
    assert l["aqui"][1] == 3 and l["aqui"][2] == 5 and l["aqui"][4] == 1.5, l
    assert l["chat-novo"][3] == 115000, l
    print("ok")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--teste" in sys.argv:
        teste()
    else:
        arq = sys.argv[1] if len(sys.argv) > 1 else "chat-traffic-uso.csv"
        if not os.path.isfile(arq):
            sys.exit(f"Sem {arq} nesta pasta: rode na raiz de um projeto que já mediu tarefas.")
        mostrar(resumo(arq))
