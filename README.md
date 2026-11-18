# chat-traffic

Skill para o Claude Code (app Claude, aba Code). Organiza um projeto em 4 arquivos curtos (`CLAUDE.md`, `CONTINUAR.md`, `COMBINADOS.md`, `HISTORICO.md`), decide se cada tarefa fica no chat atual, vai para um chat parado do mesmo assunto ou para um chat novo, e evita que vários chats atrapalhem um ao outro. Objetivo: gastar menos tokens sem perder qualidade.

## Por que, se já existem subagentes?

Subagentes resolvem um pedaço **dentro de um turno** e somem: não guardam nada para amanhã, você não os vê nem conversa com eles, e eles não publicam. A chat-traffic cuida do que fica **entre** chats e entre dias:

- memória do projeto em 4 arquivos curtos, que qualquer chat novo lê em segundos;
- escolha entre fazer aqui, mandar a um subagente, a um chat parado ou a um chat novo, com modelo e esforço certos, pela conta do cache;
- vários chats ao mesmo tempo sem um estragar o trabalho do outro (versão + reserva de arquivos);
- nenhuma pergunta perdida nem publicação esquecida: tudo em botões, "esperando você" no app, pendências escritas.

Ela usa subagentes quando eles são a opção mais barata.

## Instalar

Windows (PowerShell):

```
git clone https://github.com/OfficeBrasilrepo/chat-traffic "$env:USERPROFILE\.claude\skills\chat-traffic"
```

Mac/Linux:

```
git clone https://github.com/OfficeBrasilrepo/chat-traffic ~/.claude/skills/chat-traffic
```

E acrescente esta linha em `~/.claude/CLAUDE.md` (lido em todo chat, em qualquer pasta, e de novo depois que a conversa é compactada; sem ela a skill é esquecida no meio do projeto). Se esquecer, a skill acrescenta sozinha no primeiro uso:

```
Em projeto com `CONTINUAR.md`, use a skill `chat-traffic`: ao começar, ao decidir onde fazer cada tarefa e no fim de cada tarefa, inclusive depois de a conversa ser compactada. Antes de sugerir arquivar um chat, veja se ele é o único aberto do projeto; se for, proponha antes o chat que continua (seção 6 da skill).
```

Depois abra um chat novo na aba Code e diga "começar projeto" (ou "retomar projeto"). Também dá para chamar com `/chat-traffic`.

## Alarme (opcional, recomendado)

Um gancho que, ao abrir um chat, confere o `CONTINUAR.md` do projeto: grande demais, reserva esquecida há mais de 24 h, publicação esperando, resposta sua pendente. **Só escreve se houver problema**, então não gasta tokens no dia a dia. Precisa de Python. Acrescente em `~/.claude/settings.json` (ou peça ao Claude: a skill oferece instalar):

```json
"hooks": {
  "SessionStart": [
    { "hooks": [ { "type": "command", "command": "python \"$HOME/.claude/skills/chat-traffic/scripts/alarme.py\"" } ] }
  ]
}
```

## Medição

No fim de cada tarefa a skill anota uma linha em `chat-traffic-uso.csv`, ao lado do `CONTINUAR.md` do projeto. Para ver se está compensando, rode nessa pasta:

```
python ~/.claude/skills/chat-traffic/scripts/relatorio.py
```

## Atualizar

```
git -C ~/.claude/skills/chat-traffic pull
```

Precisa de git instalado. Os números de custo na skill foram medidos num PC em 16/11/2026: são referência, não exatos.
