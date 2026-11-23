# Desempenho da skill por versão

Cada versão fica marcada no git (`git tag`). Para voltar a uma: `git checkout v1 -- SKILL.md` e commit.

## v1 (16 a 23/11/2026) — linha de base

Medido em 23/11 no projeto boletos (`chat-traffic-uso.csv`, 19 tarefas; `relatorio.py`).

| Onde | Tarefas | Passos (média) | Contexto no fim (média) | % do limite de 5 h por tarefa |
|---|---|---|---|---|
| aqui | 12 | 27 | 161 mil | 19% |
| chat novo | 6 | 95 | 319 mil | — |
| subagente | 1 | — | — | — |

- **Modelo:** 19 de 19 tarefas em Opus; 0 em Sonnet ou Haiku. A regra "Opus planeja, Sonnet executa" não foi seguida.
- **Tamanho dos chats:** chats novos cresceram até ~320 mil (deviam nascer pequenos); "principal" chegou a ~380 mil.
- **Arquivos do projeto:** CONTINUAR.md 19,6 mil e COMBINADOS.md 18,6 mil em 23/11 (depois limpos para 7,2 mil e 10,4 mil).
- **Medição incompleta:** só 6 das 19 linhas têm contexto do fim; esforço e passos quase sempre vazios; duas linhas com número errado ("275", "301" em vez de milhares).
- **Funcionou:** chats renomeados e agrupados; CONTINUAR.md lido por chats novos; sucessor antes de arquivar; perguntas em botões; skill seguida sem ser chamada (depois da linha global).
- **Não funcionou ou deu problema:** chats grandes demais; nenhuma delegação a Sonnet; Opus se arquivava sem sucessor quando só sobrava um Sonnet (corrigido em 23/11); medição esquecida.
- **Custo fixo da skill:** SKILL.md ~12 mil caracteres (~3,4 mil tokens por chat, ~2% de cada passo num chat de 160 mil) + ~1 passo no fim de cada tarefa + ~5 mil tokens para ler CONTINUAR/COMBINADOS num chat novo. Total estimado: 3 a 5% do gasto.

## v2 (a partir de 23/11/2026)

Muda: cada chat novo e subagente nasce com modelo e esforço escolhidos pela tarefa (Opus, Sonnet ou Haiku); o fim de tarefa diz com que modelo abrir a próxima; chat Sonnet pode abrir chat Sonnet/Haiku e, se a tarefa pede Opus, pede ao usuário. Valem também as regras de 23/11 (teto de 200 mil, fim de tarefa numa mensagem, COMBINADOS até ~8 mil).

**Em 30/11:** rodar `relatorio.py` nos boletos com `--desde 2026-11-24` (linhas da v2) e preencher a tabela abaixo. Decisão: chats menores (média abaixo de ~150 mil) e tarefas fora do Opus → manter v2; nada mudou → cortar a skill ao essencial (CONTINUAR.md curto + chat novo acima de ~200 mil + subagente Sonnet).

| Onde | Tarefas | Passos (média) | Contexto no fim (média) | % do limite de 5 h por tarefa |
|---|---|---|---|---|
| (preencher em 30/11) | | | | |
