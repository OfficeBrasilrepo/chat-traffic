# Limpeza do CONTINUAR.md ou do COMBINADOS.md

Vale quando o `CONTINUAR.md` passa de ~10 mil caracteres ou o `COMBINADOS.md` passa de ~8 mil. `HISTORICO.md` reservado por outro chat: limpe depois.

1. A limpeza é a exceção à leitura só do topo: leia o arquivo inteiro com números de linha e escolha as linhas concluídas (ou as decisões antigas).
2. Na pasta do arquivo, rode `python ~/.claude/skills/chat-traffic/scripts/limpar.py --versao <N lida> 12-40 55`. Ele move as linhas sem mudar uma letra para o `HISTORICO.md`, confere que nada se perdeu, soma 1 na versão e recusa se outro chat gravou. Para o `COMBINADOS.md`: `--arquivo COMBINADOS.md --versao 0`.
3. Commit próprio da limpeza.
