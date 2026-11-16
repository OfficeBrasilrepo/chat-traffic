Versão: 6

# Continuar — chat-traffic

## EM USO
(nenhum)

## ESTADO ATUAL
- 2026-11-16: nos boletos a skill não rodava: chats abertos na pasta pessoal (C:/Users/OFFICE01) não leem o CLAUDE.md do projeto. Correção: linha da skill no `~/.claude/CLAUDE.md` global (lido em todo chat, qualquer pasta, volta depois de compactar). Instalada neste PC; README manda pôr na instalação; a skill acrescenta sozinha no primeiro uso (seção 1, passo 3). Projeto com arquivos de mesmo papel (TODO, NOTAS, AGENTS.md...): junta num só e o antigo só aponta (seção 2, passo 3). Outro PC: `git pull` + a linha.
- 2026-11-16: skill era esquecida no meio do projeto (nenhum chat-traffic-uso.csv existia): a causa é a compactação e o chat aberto fora da pasta. Correção que vale para qualquer pessoa, sem gancho: linha "Use a skill `chat-traffic`..." no CLAUDE.md do projeto (o app o relê depois de compactar); a seção 2 a acrescenta em projeto existente. Ensaio Sonnet em projeto existente passou (trocou a linha velha e, depois de "compactar", fez o fim de tarefa pela seção 6).
- 2026-11-16: (1) chat novo: antes, `list_sessions` do grupo; se já há chat ou cartão com a função, usa-o e não propõe outro (no outro PC o cartão apareceu duas vezes). (2) Ensaio de projeto realmente novo, sem nome no git, com Sonnet: passou; achou que o git também exige `user.email` (regra corrigida). Skill também instalada no outro PC do Matheus: avisar quando precisar atualizar lá (`git pull` na pasta da skill).
- 2026-11-16: seção 6, item 6 reescrito: 3 condições separadas (a/b/c), `percentUsed` vem do `get_usage` do passo 4, cartão do sucessor antes e uma pergunta só (arquivar). Sonnet seguiu certo os dois casos de teste; sobras pequenas (quem arquiva no caso c, "na dúvida, trate como único") deixadas de propósito.
- 2026-11-16: skill publicada (GitHub público OfficeBrasilrepo/chat-traffic). Tem: 4 arquivos de projeto, onde fazer cada tarefa (aqui / subagente / chat parado / chat novo, com cache de 1 h), anti-conflito (Versão + EM USO + Edit), publicação sem ficar parada, pergunta sempre com botões e "esperando você", alarme por gancho (instalado neste PC), medição em CSV + `relatorio.py`, `limpar.py`, grupo do projeto na barra lateral, sucessor antes de arquivar o único chat. SKILL.md com ~12 mil caracteres (no teto: nova regra precisa tirar texto ou ir para arquivo à parte).
- 2026-11-16 conferido no uso real: cartão do sucessor funcionou (chat antigo arquivado, sucessor ficou vivo e no grupo). Agrupamento funciona, mas chat aberto por outro chat fica aninhado e só se move junto com o pai (regra corrigida). Nome do git: neste PC já está configurado, a regra não dispara; corrigida para não pedir nome digitado em botão.

## PENDÊNCIAS
1. Medir uma semana (`chat-traffic-uso.csv` nos projetos) e comparar pelo `relatorio.py` (ver DESENVOLVER.md, passo 5) — a partir de 23/11/2026.
