"""Limpeza do CONTINUAR.md da chat-traffic: move as linhas escolhidas para o fim do
HISTORICO.md (sob "## Movido em AAAA-MM-DD"), sem mudar uma letra, confere que
nenhuma linha se perdeu e soma 1 na Versão. Quem escolhe as linhas é o chat.

Uso:  python limpar.py --versao N 12-40 55 60-62     (na pasta do CONTINUAR.md)
      --versao N: a Versão que você leu; se mudou, não grava nada (outro chat mexeu).
Teste: python limpar.py --teste"""
import datetime, os, re, sys, tempfile


def faixas(args):
    linhas = set()
    for a in args:
        ini, _, fim = a.partition("-")
        linhas.update(range(int(ini), int(fim or ini) + 1))
    return linhas


def limpar(pasta, versao_lida, escolhidas, hoje=None):
    hoje = hoje or datetime.date.today().isoformat()
    cont = os.path.join(pasta, "CONTINUAR.md")
    hist = os.path.join(pasta, "HISTORICO.md")
    texto = open(cont, encoding="utf-8", newline="").read()
    eol = "\r\n" if "\r\n" in texto else "\n"
    linhas = texto.split(eol)
    m = re.match(r"Versão:\s*(\d+)", linhas[0])
    if not m:
        raise SystemExit("CONTINUAR.md não começa com 'Versão: N'. Acrescente antes (seção 2).")
    if int(m.group(1)) != versao_lida:
        raise SystemExit(f"Versão mudou ({versao_lida} -> {m.group(1)}): outro chat gravou. Releia o topo e escolha as linhas de novo.")
    fora = [n for n in escolhidas if n < 2 or n > len(linhas)]
    if fora:
        raise SystemExit(f"Linhas fora do arquivo (ou a linha da Versão): {fora}")
    movidas = [linhas[n - 1] for n in sorted(escolhidas)]
    ficam = [l for i, l in enumerate(linhas, 1) if i not in escolhidas]
    ficam[0] = f"Versão: {versao_lida + 1}"
    antigo = open(hist, encoding="utf-8", newline="").read() if os.path.isfile(hist) else "# Histórico (arquivo morto)" + eol
    novo_hist = antigo.rstrip("\r\n") + eol + eol + f"## Movido em {hoje}" + eol + eol.join(movidas) + eol
    # conferência: toda linha não vazia de antes está em um dos dois arquivos
    cheias = lambda ls: [l for l in ls if l.strip()]
    assert sorted(cheias(linhas[1:])) == sorted(cheias(ficam[1:]) + cheias(movidas)), "linha perdida"
    open(hist, "w", encoding="utf-8", newline="").write(novo_hist)
    open(cont, "w", encoding="utf-8", newline="").write(eol.join(ficam))
    return len(movidas), len(eol.join(ficam))


def teste():
    d = tempfile.mkdtemp()
    open(os.path.join(d, "CONTINUAR.md"), "w", encoding="utf-8", newline="").write(
        "Versão: 4\r\n## ESTADO ATUAL\r\n- feito A\r\n- vale B\r\n- feito C\r\n## PENDÊNCIAS\r\n1. x\r\n")
    n, _ = limpar(d, 4, faixas(["3", "5"]), "2026-11-16")
    c = open(os.path.join(d, "CONTINUAR.md"), encoding="utf-8", newline="").read()
    h = open(os.path.join(d, "HISTORICO.md"), encoding="utf-8", newline="").read()
    assert n == 2 and c.startswith("Versão: 5\r\n") and "feito" not in c and "- vale B" in c, c
    assert "## Movido em 2026-11-16\r\n- feito A\r\n- feito C\r\n" in h, h
    for args in ((4, {3}), (5, {1})):  # versão velha; tentar mover a linha da Versão
        try:
            limpar(d, *args); raise AssertionError("devia recusar")
        except SystemExit:
            pass
    print("ok")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8"); sys.stderr.reconfigure(encoding="utf-8")
    if "--teste" in sys.argv:
        teste()
    else:
        a = sys.argv[1:]
        if len(a) < 3 or a[0] != "--versao":
            raise SystemExit(__doc__)
        n, tam = limpar(os.getcwd(), int(a[1]), faixas(a[2:]))
        print(f"{n} linhas movidas para o HISTORICO.md; CONTINUAR.md agora com {tam} caracteres; nenhuma linha perdida.")
