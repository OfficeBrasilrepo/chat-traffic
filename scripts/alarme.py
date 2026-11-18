"""Alarme da chat-traffic (gancho SessionStart): confere o CONTINUAR.md da pasta
do chat e só escreve algo se houver problema. Sem problema, não gasta tokens.
Teste: python alarme.py --teste"""
import datetime, os, re, sys, tempfile

LIMITE = 10000
HORAS = 24


def achar(pasta):
    """CONTINUAR.md na pasta do chat, ou o caminho que o CLAUDE.md da pasta aponta
    (ex.: `sub/CONTINUAR.md`). Não varre subpastas: pasta pessoal não é projeto."""
    caminho = os.path.join(pasta, "CONTINUAR.md")
    if os.path.isfile(caminho):
        return caminho
    claude = os.path.join(pasta, "CLAUDE.md")
    if os.path.isfile(claude):
        for m in re.findall(r"[\w./\\-]*CONTINUAR\.md", open(claude, encoding="utf-8", errors="replace").read()):
            c = os.path.join(pasta, m)
            if os.path.isfile(c):
                return c
    return None


def conferir(pasta, agora=None):
    agora = agora or datetime.datetime.now()
    caminho = achar(pasta)
    if not caminho:
        return []
    texto = open(caminho, encoding="utf-8-sig", errors="replace").read()  # -sig: Bloco de Notas grava BOM
    avisos = []
    if len(texto) > LIMITE:
        avisos.append(f"CONTINUAR.md tem {len(texto)} caracteres (limite ~{LIMITE}): limpar antes de trabalhar (seção 2).")
    if not re.search(r"^Versão:\s*\d+", texto, re.M):
        avisos.append("CONTINUAR.md sem linha 'Versão:' (seção 2).")
    for linha in texto.splitlines():
        l = linha.strip()
        if l.startswith("EM USO:"):
            m = re.search(r"desde\s+(\d{4}-\d{2}-\d{2} \d{2}:\d{2})", l)
            if m and agora - datetime.datetime.strptime(m.group(1), "%Y-%m-%d %H:%M") > datetime.timedelta(hours=HORAS):
                avisos.append(f"Reserva com mais de {HORAS} h (perguntar ao usuário antes de assumir): {l}")
        elif l.startswith("AGUARDA PUBLICAR:"):
            avisos.append(f"Publicação esperando: {l}")
        elif "esperando o usuário" in l.lower():
            avisos.append(f"Resposta pendente do usuário: {l}")
        elif l.startswith("#") and re.search(r"pendente com\b|esperando", l.lower()):  # \b: "comigo" não conta
            avisos.append(f"Pendências do usuário na seção: {l.lstrip('# ')}")
    return avisos


def teste():
    d = tempfile.mkdtemp()
    assert conferir(d) == []  # sem CONTINUAR.md: silêncio
    p = os.path.join(d, "CONTINUAR.md")
    agora = datetime.datetime(2026, 11, 16, 12, 0)
    open(p, "w", encoding="utf-8").write("Versão: 3\n## EM USO\n(nenhum)\n")
    assert conferir(d, agora) == []
    open(p, "w", encoding="utf-8").write(
        "Versão: 3\n## EM USO\nEM USO: a · src · desde 2026-11-14 09:00\nEM USO: b · x · desde 2026-11-16 10:00\n"
        "AGUARDA PUBLICAR: b · v2 · depois de a\n## PENDÊNCIAS\n1. esperando o usuário: OK para publicar\n")
    av = conferir(d, agora)
    assert len(av) == 3 and "a · src" in av[0], av
    open(p, "w", encoding="utf-8").write("x" * (LIMITE + 1))
    assert len(conferir(d, agora)) == 2
    raiz = tempfile.mkdtemp(); os.mkdir(os.path.join(raiz, "sub"))
    open(os.path.join(raiz, "sub", "CONTINUAR.md"), "w", encoding="utf-8").write("sem versao\n")
    assert conferir(raiz, agora) == []  # não varre subpastas sozinho
    open(os.path.join(raiz, "CLAUDE.md"), "w", encoding="utf-8").write("Leia `sub/CONTINUAR.md`.\n")
    assert len(conferir(raiz, agora)) == 1  # segue o CLAUDE.md
    open(p, "w", encoding="utf-8-sig").write("Versão: 3\n## PENDENTE COM O MATHEUS\n1. ver tela\n## PENDENTE COMIGO\n1. x\n")
    av = conferir(d, agora)
    assert len(av) == 1 and "PENDENTE COM" in av[0], av  # BOM não esconde a Versão; seção própria conta
    print("ok")


if __name__ == "__main__":
    if "--teste" in sys.argv:
        teste()
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        try:
            avisos = conferir(os.getcwd())
        except Exception:
            avisos = []  # o alarme nunca pode travar a abertura do chat
        if avisos:
            print("[chat-traffic] Avisos deste projeto:\n- " + "\n- ".join(avisos))
