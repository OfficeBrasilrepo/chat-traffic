---
name: chat-traffic
description: Organiza um projeto entre vários chats do app Claude (aba Code) gastando poucos tokens - CLAUDE.md, CONTINUAR.md, COMBINADOS.md e HISTORICO.md, onde fazer cada tarefa, sem conflito entre chats. Use ao começar ou retomar um projeto, ao perguntar "onde paramos", ao decidir se abre chat novo ou delega (Opus planeja, Sonnet executa), ao arquivar chats, e ao terminar uma tarefa num projeto que tem CONTINUAR.md.
---

# chat-traffic (projeto entre chats)

Objetivo, acima de tudo: **economizar tokens sem perder qualidade**, delegar só a quem dá conta da tarefa, e manter os chats abertos organizados.

Responda em português simples. **Toda pergunta ao usuário vai em botões clicáveis**, nunca só escrita no texto: no meio do trabalho, AskUserQuestion com respostas prontas; no fim do turno, o quadro de próximo passo (`wrap_up` com pergunta + botões). Nunca peça texto digitado na caixinha do "Outro" (ele se perde); texto livre, peça na caixa de mensagem do chat.

## Os 4 arquivos (raiz do projeto, todos curtos)

| Arquivo | Para quê | Como ler |
|---|---|---|
| `CLAUDE.md` | Diz o que ler antes de tudo | Inteiro (poucas linhas) |
| `CONTINUAR.md` | Estado atual, reservas e pendências | **Só o topo** (até `## PENDÊNCIAS` + a lista); o resto, buscar |
| `COMBINADOS.md` | Regras que não se quebram, decisões, como testar e publicar | Inteiro antes de mudar algo |
| `HISTORICO.md` | Arquivo morto: o que já foi concluído | Nunca inteiro; buscar a palavra |

Modelos em `modelos/` nesta pasta da skill.

## 1. Projeto novo (não há CONTINUAR.md nem git com histórico)

Antes de tudo: tarefa que cabe numa conversa só (um script, um ajuste de poucos arquivos, sem volta prevista)? Não crie nada; diga em uma linha que não compensa. Senão:

1. Siga `modelos/novo-projeto.md`: 4 perguntas em botões, os 4 arquivos a partir dos modelos, git e primeiro commit.
2. Avise em uma linha o que foi criado.
3. `~/.claude/CLAUDE.md` sem a linha do `README.md` ("Em projeto com `CONTINUAR.md`...") ou com versão antiga dela: ponha a linha atual, sem perguntar, e avise em uma frase.
4. Ofereça uma vez (botões) ligar `auto_archive_on_pr_close` (`set_setting`: chat se arquiva quando o PR dele é juntado) e instalar o **alarme** se `~/.claude/settings.json` não existe ou não cita `chat-traffic/scripts/alarme.py` (instrução no `README.md` da skill). Recusou? Grave no `COMBINADOS.md` e não ofereça de novo.

## 2. Projeto existente

1. Leia `CLAUDE.md`, o topo do `CONTINUAR.md` e `git log --oneline -15`. Se o chat abriu com `[chat-traffic] Avisos`, resolva-os primeiro. Faça os passos 3 e 4 da seção 1.
2. Renomeie este chat para `<projeto> · <tarefa>` (`set_session_title`, `self`) e ponha-o no grupo `<projeto>` da barra lateral (`list_groups`; sem grupo, `create_group`; `move_sessions` com `self`; recusou por estar aninhado: inclua o chat pai que o erro nomeia, se for do projeto; senão, fique sem grupo), tudo no mesmo passo da leitura.
3. Arquivo com o mesmo papel de um dos 4 (TODO, NOTAS, PROGRESS, `AGENTS.md`, docs de estado)? **Nunca dois com o mesmo papel** (o chat leria tudo duas vezes): junte no da skill e deixe no antigo uma linha apontando. Falta algum dos 4? Monte o que faltar a partir do git (log, README, estrutura) sem perguntar o que dá para deduzir; pergunte com botões só regras e publicação, se não houver pista.
4. `CONTINUAR.md` sem `Versão:` nem `## EM USO`: acrescente os dois no topo, como no modelo (`Versão: 1`).
5. `CONTINUAR.md` com mais de ~10 mil caracteres: **limpe antes de trabalhar** (`HISTORICO.md` reservado por outro chat: limpe depois). Escolha os números das linhas concluídas e rode, na pasta do arquivo, `python ~/.claude/skills/chat-traffic/scripts/limpar.py --versao <N lida> 12-40 55`: ele move sem mudar uma letra para o `HISTORICO.md`, confere que nada se perdeu, soma 1 na versão e recusa se outro chat gravou. Commit próprio da limpeza.

## 3. Em cada tarefa: onde fazer

Veja o tamanho deste chat com `get_usage` (ferramenta do app; carregue se estiver adiada) quando a tarefa for longa: `tokensUsed` decide o custo (limites em mil abaixo), `percentUsed` o risco de compactar. Sem essa ferramenta (fora do app), estime pelo tamanho da conversa e fique aqui na dúvida. Escolha a primeira opção que serve:

1. **Aqui**: tarefa curta (até ~12 passos) ou este chat com menos de ~150 mil de contexto.
2. **Subagente** (ferramenta Agent, com `model`): pedaço desta tarefa cujo resultado você precisa já (ler muitos arquivos, buscar, revisar, testar). Sonnet para ler, buscar e executar pedido fechado; o mesmo modelo deste chat para revisar. Não serve para trabalho que deve durar além deste turno, que o usuário quer acompanhar ou que publica.
3. **Chat parado do mesmo assunto** (`list_sessions`, ocioso): `SendMessage` com resumo curto. Barato **só se** ele parou há menos de 1 hora **ou** tem menos de ~100 mil de contexto. Nunca para chat ocupado nem arquivado (desarquivar regrava tudo: chat novo lê o `CONTINUAR.md`). Pedido que é de outro chat aberto do grupo: mande para ele por esta mesma regra.
4. **Chat novo** (`start_session`, `cwd` na raiz, `title` `<projeto> · <tarefa>`). Antes, `list_sessions` do grupo: já existe chat (ou cartão que você propôs) com essa função? Use-o ou espere; nunca proponha outro. Este chat fora do grupo? Entre nele antes (seção 2, passo 2): o chat novo fica pendurado neste e só entra junto. Serve para: tarefa longa (~12 passos ou mais) saindo de chat acima de ~150 mil; ou trabalho que é uma entrega própria (branch, PR, publicação); ou depois de uma pausa longa num chat grande.

**Modelo e esforço** (`model`, `effort`) para subagente e chat novo:
   - **Opus planeja, Sonnet executa** (Sonnet custa metade): Opus escreve o pedido fechado (`modelos/resumo.md`: arquivos, passos, como testar, pronto quando); Sonnet, esforço médio, executa como subagente ou chat novo e pergunta se o pedido tiver dúvida; Opus revisa o diff e publica.
   - Opus faz ele mesmo, aqui ou em chat novo Opus (alto se difícil): desenho, dinheiro, produção, bug que não se acha, ou o que não dá para fechar em pedido.
   - Não troque o modelo de um chat no meio, nem com `opusplan`: cada troca regrava o chat inteiro no cache.
   - Nunca acima do modelo deste chat sem o usuário pedir.

Para subagente, chat parado ou chat novo, escreva o pedido pelo `modelos/resumo.md`. Na dúvida entre duas opções, fique com a de menos passagens: cada passagem perde detalhe.

**Cache (o que decide a conta).** Reler o que está no cache custa 10%; gravar no cache custa ~200% (no app o cache dura 1 hora). Cada passo relê o chat inteiro: num chat de 280 mil, ~28 mil por passo.
- **Chat parado há mais de 1 hora perdeu o cache**: acordá-lo regrava tudo a ~200%. Depois de pausa longa, chat grande com tarefa nova → chat novo.
- Não passe a **publicação** para outro chat: ele redescobre tudo e corre risco.

## 4. Sem conflito entre chats

No topo do `CONTINUAR.md` (ver o modelo):

```
Versão: 12
...
## EM USO
EM USO: <nome do chat> · <arquivos ou pasta> · desde <AAAA-MM-DD HH:MM>
EM USO: <outro chat> · <outros arquivos> · desde <...>
```

- **Ao ler**, guarde o número da versão.
- **Ao gravar** (inclusive a própria reserva), use a ferramenta Edit, não o shell: ela recusa se o arquivo mudou desde a sua leitura, sem passo extra. Recusou ou a `Versão:` mudou? Releia o topo, junte sua mudança com a nova e grave. Toda gravação depois da criação soma 1 na versão.
- **Reserva**: antes de mexer em arquivos, acrescente sua linha `EM USO:` na seção `## EM USO` (uma linha por chat; sem nenhuma reserva, escreva `(nenhum)`). Se outra linha já reserva os mesmos arquivos, não mexa: trabalhe em outra coisa ou pergunte. Linha com mais de 24 h vale como abandonada: **pergunte com botões** antes de assumir. Com o OK, troque a linha dela pela sua; sem OK, faça outra coisa.
- Cada chat só altera **a própria** linha `EM USO:`.
- **Commit a cada gravação** do `CONTINUAR.md` (só os arquivos que você mudou; nunca `git add -A` com outros chats na pasta).

## 5. Publicar

Cada chat publica o próprio trabalho, seguindo o `COMBINADOS.md` (inclusive pedir OK, se a regra pedir). Sem regra de publicação no `COMBINADOS.md` (ou "perguntar ao dono"): não publique; pergunte com botões e grave a resposta lá como decisão, para não perguntar de novo.

**Nada fica sem publicar porque outro chat está em andamento.** Terminou e não pode publicar ainda (outro chat reservou o arquivo ou publica antes)? Siga `modelos/aguarda-publicar.md`.

## Resposta pendente do usuário (nunca fica escondida)

- Toda vez que o próximo passo depende do usuário (OK para publicar, escolha, aprovação), termine o turno com `wrap_up` com pergunta + botões **e `blocked: true`**, para o app marcar o chat como "esperando você" e mostrar o aviso.
- Ao começar e ao terminar uma tarefa, veja `list_sessions` do grupo do projeto: se algum está esperando resposta do usuário, avise no seu quadro de próximo passo qual é.
- Pendência do usuário também vai escrita no `CONTINUAR.md` (`## PENDÊNCIAS`, "esperando o usuário: …"), para não depender da memória de nenhum chat.

## 6. No fim de cada tarefa

1. Em `ESTADO ATUAL`, no topo da lista: uma linha com data e o que ficou valendo (o que mudou, o que falta, o que não foi conferido). Tire sua linha `EM USO:`.
2. Pendência concluída sai do `CONTINUAR.md` e vai para o fim do `HISTORICO.md` como `- AAAA-MM-DD: <texto igual>`. Linhas velhas do `ESTADO ATUAL` que já não valem vão do mesmo jeito.
3. Regra ou decisão nova: no `COMBINADOS.md`, com data (e na memória, só se for regra que vale para outros projetos).
4. **Medição**: acrescente uma linha em `chat-traffic-uso.csv` (ao lado do `CONTINUAR.md` principal, nunca numa cópia de trabalho; crie com o cabeçalho se faltar):
   `data,chat,tarefa,onde,modelo,esforco,passos,contexto_inicio,contexto_fim,plano5h_inicio,plano5h_fim`
   `onde` = aqui | subagente | chat-parado | chat-novo. Os números vêm do `get_usage`: o do fim, **sempre**, chamado junto com a gravação do passo 1; o do começo, só se você já o chamou na seção 3 (senão, deixe vazio). Sem `get_usage`, grave a linha mesmo assim, com os números vazios: ela conta a tarefa. Nunca gaste um passo só para medir. Resultado: `scripts/relatorio.py`.
5. Um commit só com os arquivos que mudaram. Linha `AGUARDA PUBLICAR` esperando por você: passo 3 de `modelos/aguarda-publicar.md`.
6. **Arquivar chats** (grave tudo no `CONTINUAR.md` antes). Vale qualquer um:
   - (a) este, com a tarefa terminada e o `percentUsed` do `get_usage` do passo 4 acima de ~60% (sem a ferramenta: conversa muito longa); (b) este, sem trabalho previsto; (c) um chat aberto por este que já acabou; (d) chats do grupo parados há mais de 1 dia, todos num botão só, depois de passar ao `CONTINUAR.md` o que só existia na conversa deles (`list_events`; decisão esperada vira pendência).
   - **Nenhum outro chat aberto do projeto** (`list_sessions` com `group` = projeto, que não lista este; sem grupo, títulos `<projeto> · …`; na dúvida, trate como único)? Antes de arquivar este, proponha o sucessor com `start_session` (`own_initiative`, `cwd` na raiz, `title` `<projeto> · principal`, modelo e esforço do trabalho comum, resumo: "Leia CLAUDE.md e o topo do CONTINUAR.md, mostre ao usuário onde o projeto está (até 8 linhas) e continue").
   - Sugerir arquivar é sempre pergunta com botões, nunca só no texto. O quadro de próximo passo traz uma pergunta só: arquivar. Use a ação `archive` do `wrap_up` se houver; senão, botões ("Pode arquivar" / "Ainda não"). Arquivando outro chat (`archive_session`) e o app recusa por controle remoto: `set_remote_control` desligado e de novo. Arquivar um chat leva junto os chats terminados pendurados nele.
   - Depois de arquivar outros, mostre ao usuário **onde o projeto está** em até 8 linhas do `CONTINUAR.md`: últimas entregas, o que ele aprovou, o que espera por ele.

Trabalho interrompido no meio vira pendência escrita no `CONTINUAR.md` na hora.
