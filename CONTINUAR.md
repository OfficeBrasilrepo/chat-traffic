Versão: 4

# Continuar — chat-traffic

## EM USO
(nenhum)

## ESTADO ATUAL
- 2026-11-16: (1) chat novo: antes, `list_sessions` do grupo; se já há chat ou cartão com a função, usa-o e não propõe outro (no outro PC o cartão apareceu duas vezes). (2) Ensaio de projeto realmente novo, sem nome no git, com Sonnet: passou; achou que o git também exige `user.email` (regra corrigida). Skill também instalada no outro PC do Matheus: avisar quando precisar atualizar lá (`git pull` na pasta da skill).
- 2026-11-16: seção 6, item 6 reescrito: 3 condições separadas (a/b/c), `percentUsed` vem do `get_usage` do passo 4, cartão do sucessor antes e uma pergunta só (arquivar). Sonnet seguiu certo os dois casos de teste; sobras pequenas (quem arquiva no caso c, "na dúvida, trate como único") deixadas de propósito.
- 2026-11-16: skill publicada (GitHub público OfficeBrasilrepo/chat-traffic). Tem: 4 arquivos de projeto, onde fazer cada tarefa (aqui / subagente / chat parado / chat novo, com cache de 1 h), anti-conflito (Versão + EM USO + Edit), publicação sem ficar parada, pergunta sempre com botões e "esperando você", alarme por gancho (instalado neste PC), medição em CSV + `relatorio.py`, `limpar.py`, grupo do projeto na barra lateral, sucessor antes de arquivar o único chat. SKILL.md com ~12 mil caracteres (no teto: nova regra precisa tirar texto ou ir para arquivo à parte).
- 2026-11-16 conferido no uso real: cartão do sucessor funcionou (chat antigo arquivado, sucessor ficou vivo e no grupo). Agrupamento funciona, mas chat aberto por outro chat fica aninhado e só se move junto com o pai (regra corrigida). Nome do git: neste PC já está configurado, a regra não dispara; corrigida para não pedir nome digitado em botão.

## PENDÊNCIAS
1. Medir uma semana (`chat-traffic-uso.csv` nos projetos) e comparar pelo `relatorio.py` (ver DESENVOLVER.md, passo 5) — a partir de 23/11/2026.
