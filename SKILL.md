---
name: chat-traffic
description: Organiza um projeto entre vários chats do app Claude (aba Code) gastando poucos tokens - CLAUDE.md, CONTINUAR.md, COMBINADOS.md e HISTORICO.md, onde fazer cada tarefa, sem conflito entre chats. Use ao começar ou retomar um projeto, ao perguntar "onde paramos", ao decidir se abre chat novo, e ao terminar uma tarefa num projeto que tem CONTINUAR.md.
---

# chat-traffic (projeto entre chats)

Objetivo, acima de tudo: **economizar tokens sem perder qualidade**, delegar só a quem dá conta da tarefa, e manter os chats abertos organizados.

Responda em português simples. **Toda pergunta ao usuário vai em botões clicáveis**, nunca só escrita no texto: no meio do trabalho, AskUserQuestion com respostas prontas; no fim do turno, o quadro de próximo passo (`wrap_up` com pergunta + botões). Nunca termine a mensagem com "Quer que eu...?" sem os botões, nem peça texto digitado na caixinha.

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

1. Pergunte com botões, num só AskUserQuestion (até 4 perguntas, opções prováveis + "Outro"):
   - O que é o projeto (tipo: app web, script, planilha, outro).
   - Regras que nunca podem ser quebradas (ex.: não apagar sem OK, não mexer em produção sem OK, dados sensíveis).
   - Como testar (testes automáticos, abrir a tela, cópia de teste, ainda não sei).
   - Como publicar (não publica, branch principal, comando, manual pelo dono).
2. Crie os 4 arquivos a partir dos modelos, preenchendo `COMBINADOS.md` com as respostas (decisões com a data de hoje), e copie `modelos/.gitattributes` (tira o aviso de fim de linha do Windows; só em projeto novo, nunca em existente). Sem git: `git init`; sem `git config user.name`, pergunte o nome com botões. Primeiro commit.
3. Ofereça uma vez (botões) instalar o **alarme** se `~/.claude/settings.json` não existe ou não cita `chat-traffic/scripts/alarme.py` (instrução no `README.md` da skill).

## 2. Projeto existente

1. Leia `CLAUDE.md`, o topo do `CONTINUAR.md` e `git log --oneline -15`. Se o chat abriu com `[chat-traffic] Avisos`, resolva-os primeiro (o alarme só fala quando há problema). Sem alarme instalado, ofereça como na seção 1.
2. Renomeie este chat para `<projeto> · <tarefa>` (`set_session_title`, `self`) e ponha-o no grupo `<projeto>` da barra lateral (`list_groups`; sem grupo, `create_group`; `move_sessions` com `self`), tudo no mesmo passo da leitura. Assim os chats de cada projeto ficam juntos e se vê de longe qual espera você.
3. Falta algum dos 4 arquivos? Monte o que faltar a partir do git (log, README, estrutura) sem perguntar o que dá para deduzir; pergunte com botões só regras e publicação, se não houver pista.
4. `CONTINUAR.md` sem `Versão:` nem `## EM USO`: acrescente os dois no topo, como no modelo (`Versão: 1`).
5. `CONTINUAR.md` com mais de ~10 mil caracteres: **limpe antes de trabalhar** (`HISTORICO.md` reservado por outro chat: limpe depois). Escolha os números das linhas concluídas e rode, na pasta do arquivo, `python ~/.claude/skills/chat-traffic/scripts/limpar.py --versao <N lida> 12-40 55`: ele move sem mudar uma letra para o `HISTORICO.md`, confere que nada se perdeu, soma 1 na versão e recusa se outro chat gravou. Commit próprio da limpeza.

## 3. Em cada tarefa: onde fazer

Veja o tamanho deste chat com `get_usage` (ferramenta do app; carregue se estiver adiada) quando a tarefa for longa. Sem essa ferramenta (fora do app), estime pelo tamanho da conversa e fique aqui na dúvida. Escolha a primeira opção que serve:

1. **Aqui**: tarefa curta (até ~12 passos) ou este chat com menos de ~120 mil de contexto.
2. **Subagente** (ferramenta Agent, com `model`): pedaço desta tarefa cujo resultado você precisa já (ler muitos arquivos, buscar, revisar, testar). Ele trabalha à parte e devolve só o resumo, então este chat não engorda. Sonnet/Haiku para leitura e busca; o mesmo modelo deste chat para revisão. Não serve para trabalho que deve durar além deste turno, que o usuário quer acompanhar ou que publica.
3. **Chat parado do mesmo assunto** (`list_sessions`, ocioso): `SendMessage` com resumo curto. Barato **só se** ele parou há menos de 1 hora **ou** tem menos de ~100 mil de contexto (ver "cache" abaixo). Nunca para chat ocupado.
4. **Chat novo** (`start_session`, `cwd` na raiz, `title` `<projeto> · <tarefa>`): tarefa longa (~12 passos ou mais) saindo de chat acima de ~150 mil; ou trabalho que é uma entrega própria (branch, PR, publicação); ou depois de uma pausa longa num chat grande. Escolha modelo **e** esforço (`effort`):
   - Sonnet, esforço baixo/médio: mecânica, leitura, relatório, ajuste repetitivo.
   - Opus, esforço médio: código comum do projeto.
   - Opus, esforço alto: desenho, dinheiro, produção, código difícil, bug que não se acha.
   - Nunca acima do modelo deste chat sem o usuário pedir.

Para subagente, chat parado ou chat novo, escreva o pedido pelo `modelos/resumo.md` (curto: o que fazer, arquivos, pronto quando, o que não mexer). Na dúvida entre duas opções, fique com a de menos passagens: cada passagem perde detalhe.

**Cache (o que decide a conta).** Reler o que está no cache custa 10%; gravar no cache custa ~200% (no app o cache dura 1 hora). Cada passo relê o chat inteiro: num chat de 280 mil, ~28 mil por passo. Chat novo: ~65 mil gravados (~130 mil) + ~3 passos do chat grande para passar a tarefa e receber o aviso.
- Tarefa de 5 passos: separar sai ~70% mais caro. 10 passos: empate. 20 passos: economiza ~33%. 40 passos: ~43%.
- **Chat parado há mais de 1 hora perdeu o cache**: acordá-lo regrava tudo a ~200%. Voltar a um chat de 280 mil depois do almoço custa ~560 mil de uma vez, contra ~130 mil de um chat novo. Por isso, depois de pausa longa, chat grande com tarefa nova → chat novo (com o `CONTINUAR.md` em dia, nada se perde).
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
- **Reserva**: antes de mexer em arquivos, acrescente sua linha `EM USO:` na seção `## EM USO` (uma linha por chat; a hora vem de `date '+%Y-%m-%d %H:%M'`; sem nenhuma reserva, escreva `(nenhum)`). Se outra linha já reserva os mesmos arquivos, não mexa: trabalhe em outra coisa ou pergunte. Linha com mais de 24 h vale como abandonada: **pergunte com botões** antes de assumir. Com o OK, troque a linha dela pela sua (a única vez em que se mexe na linha de outro chat); sem OK, faça outra coisa.
- Cada chat só altera **a própria** linha `EM USO:`.
- **Commit a cada gravação** do `CONTINUAR.md` (só os arquivos que você mudou; nunca `git add -A` com outros chats na pasta).

## 5. Publicar

Cada chat publica o próprio trabalho, seguindo o `COMBINADOS.md` (inclusive pedir OK, se a regra pedir). Sem regra de publicação no `COMBINADOS.md` (ou "perguntar ao dono"): não publique; pergunte com botões (ex.: "Não publica", "Commit na main", "Push", "Eu publico") e grave a resposta lá como decisão, para não perguntar de novo. Dois chats no mesmo arquivo: um depois do outro (a reserva diz quem vai primeiro).

**Nada fica sem publicar porque outro chat está em andamento.** Se você terminou e não pode publicar ainda (outro chat reservou o mesmo arquivo ou vai publicar antes):
1. Escreva no `CONTINUAR.md`, seção `## EM USO`: `AGUARDA PUBLICAR: <seu chat> · <o quê, branch/commit> · depois de <outro chat>`.
2. Mande `SendMessage` ao outro chat: "quando publicar, me avise" (ou, se ele já terminou, publique você os dois, em ordem).
3. O chat que libera o arquivo, ao terminar, lê as linhas `AGUARDA PUBLICAR` e avisa cada um (SendMessage) ou publica por eles.
4. Sem como avisar (chat arquivado, fora do PC): pergunte ao usuário com botões quem publica.

## Resposta pendente do usuário (nunca fica escondida)

Com vários chats abertos, uma pergunta perdida trava tudo. Por isso:
- Toda vez que o próximo passo depende do usuário (OK para publicar, escolha, aprovação), termine o turno com `wrap_up` com pergunta + botões **e `blocked: true`**, para o app marcar o chat como "esperando você" e mostrar o aviso. No meio do trabalho, AskUserQuestion.
- Ao começar e ao terminar uma tarefa, veja `list_sessions` (`linked: true`): se algum chat do projeto está esperando resposta do usuário, avise no seu quadro de próximo passo qual é (com link `[título](#local_<id>)`).
- Pendência do usuário também vai escrita no `CONTINUAR.md` (`## PENDÊNCIAS`, "esperando o usuário: …"), para não depender da memória de nenhum chat.

## 6. No fim de cada tarefa

1. Em `ESTADO ATUAL`, no topo da lista: uma linha com data e o que ficou valendo (o que mudou, o que falta, o que não foi conferido). Tire sua linha `EM USO:`.
2. Pendência concluída sai do `CONTINUAR.md` e vai para o fim do `HISTORICO.md` como `- AAAA-MM-DD: <texto igual>`. Linhas velhas do `ESTADO ATUAL` que já não valem vão do mesmo jeito.
3. Regra ou decisão nova: no `COMBINADOS.md`, com data (e na memória, só se for regra que vale para outros projetos).
4. **Medição**: acrescente uma linha em `chat-traffic-uso.csv` (raiz; crie com o cabeçalho se faltar):
   `data,chat,tarefa,onde,modelo,esforco,passos,contexto_inicio,contexto_fim,plano5h_inicio,plano5h_fim`
   `onde` = aqui | subagente | chat-parado | chat-novo. Os números vêm do `get_usage`: o do fim, chamado **no mesmo passo** de outra ferramenta (não custa passo extra); o do começo, só se você já o chamou na seção 3 (senão, deixe vazio). Nunca gaste um passo só para medir. Para ver o resultado: `python ~/.claude/skills/chat-traffic/scripts/relatorio.py`.
5. Um commit só com os arquivos que mudaram.
6. **Chat que não é mais necessário** (este, com a tarefa terminada e acima de ~60% do contexto ou sem trabalho previsto; ou um chat que ele abriu e que já acabou): depois de gravar tudo no `CONTINUAR.md` (e na memória, se houver regra nova), peça para arquivar no quadro de próximo passo, com pergunta e botões. **Se este é o único chat aberto do projeto** (`list_sessions`, grupo do projeto), antes proponha o sucessor com `start_session` (`own_initiative`, `cwd` na raiz, `title` `<projeto> · principal`, modelo e esforço do trabalho comum do projeto, resumo: "Leia CLAUDE.md e o topo do CONTINUAR.md; continue o projeto"), para o usuário nunca ficar sem chat; só então peça para arquivar este. Se a ação `archive` estiver disponível no `wrap_up`, use-a; senão, botões de resposta ("Pode arquivar" / "Ainda não") e explique que se arquiva pelo menu do chat. O próximo chat começa lendo o `CLAUDE.md`.

Trabalho interrompido no meio vira pendência escrita no `CONTINUAR.md` na hora.
