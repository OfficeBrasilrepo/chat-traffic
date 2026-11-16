# chat-traffic

Skill para o Claude Code (app Claude, aba Code). Organiza um projeto em 4 arquivos curtos (`CLAUDE.md`, `CONTINUAR.md`, `COMBINADOS.md`, `HISTORICO.md`), decide se cada tarefa fica no chat atual, vai para um chat parado do mesmo assunto ou para um chat novo, e evita que vários chats atrapalhem um ao outro. Objetivo: gastar menos tokens sem perder qualidade.

## Instalar

Windows (PowerShell):

```
git clone https://github.com/OfficeBrasilrepo/chat-traffic "$env:USERPROFILE\.claude\skills\chat-traffic"
```

Mac/Linux:

```
git clone https://github.com/OfficeBrasilrepo/chat-traffic ~/.claude/skills/chat-traffic
```

Depois abra um chat novo na aba Code e diga "começar projeto" (ou "retomar projeto"). Também dá para chamar com `/chat-traffic`.

## Atualizar

```
git -C ~/.claude/skills/chat-traffic pull
```

Precisa de git instalado. Os números de custo na skill foram medidos num PC em 16/11/2026: são referência, não exatos.
