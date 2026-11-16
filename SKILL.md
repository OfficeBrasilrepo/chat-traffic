---
name: chat-traffic
description: Organiza um projeto entre vários chats do app Claude (aba Code) gastando poucos tokens - CLAUDE.md, CONTINUAR.md, COMBINADOS.md e HISTORICO.md, onde fazer cada tarefa, sem conflito entre chats. Use ao começar ou retomar um projeto, ao perguntar "onde paramos", ao decidir se abre chat novo, e ao terminar uma tarefa num projeto que tem CONTINUAR.md.
---

# chat-traffic (projeto entre chats)

Responda em português simples. **Toda pergunta ao usuário vai em botões clicáveis**, nunca só escrita no texto: no meio do trabalho, AskUserQuestion com respostas prontas; no fim do turno, o quadro de próximo passo (`wrap_up` com pergunta + botões). Nunca termine a mensagem com "Quer que eu...?" sem os botões, nem peça texto digitado na caixinha. (No texto, o usuário precisa perceber sozinho que é pergunta; o quadro deixa claro que você espera a resposta.)

## Os 4 arquivos (raiz do projeto, todos curtos)

| Arquivo | Para quê | Como ler |
|---|---|---|
| `CLAUDE.md` | Diz o que ler antes de tudo | Inteiro (poucas linhas) |
| `CONTINUAR.md` | Estado atual, reservas e pendências | **Só o topo** (até `## PENDÊNCIAS` + a lista); o resto, buscar |
| `COMBINADOS.md` | Regras que não se quebram, decisões, como testar e publicar | Inteiro antes de mudar algo |
| `HISTORICO.md` | Arquivo morto: o que já foi concluído | Nunca inteiro; buscar a palavra |

Modelos em `modelos/` nesta pasta da skill.

## 1. Projeto novo (não há CONTINUAR.md nem git com histórico)

1. Pergunte com botões, num só AskUserQuestion (até 4 perguntas, opções prováveis + "Outro"):
   - O que é o projeto (tipo: app web, script, planilha, outro).
   - Regras que nunca podem ser quebradas (ex.: não apagar sem OK, não mexer em produção sem OK, dados sensíveis).
   - Como testar (testes automáticos, abrir a tela, cópia de teste, ainda não sei).
   - Como publicar (não publica, branch principal, comando, manual pelo dono).
2. Crie os 4 arquivos a partir dos modelos, preenchendo `COMBINADOS.md` com as respostas (decisões com a data de hoje). Se não for repositório git, rode `git init` e faça o primeiro commit.
3. Tarefa que cabe numa conversa só (um script, um ajuste de poucos arquivos, sem volta prevista): não crie nada; diga em uma linha que não compensa.

## 2. Projeto existente

1. Leia `CLAUDE.md`, o topo do `CONTINUAR.md` e `git log --oneline -15`.
2. Falta algum dos 4 arquivos? Monte o que faltar a partir do git (log, README, estrutura) sem perguntar o que dá para deduzir; pergunte com botões só regras e publicação, se não houver pista.
3. `CONTINUAR.md` sem `Versão:` nem `## EM USO`: acrescente os dois no topo, como no modelo (`Versão: 1`).
4. `CONTINUAR.md` com mais de ~10 mil caracteres (`wc -c`): **limpe antes de trabalhar**, com reserva (seção 4) de `CONTINUAR.md` e `HISTORICO.md`. Mova o que está concluído, sem mudar uma letra, para o fim do `HISTORICO.md` (com a data da mudança). Nada é apagado: confira que as linhas não vazias movidas batem (`diff`). Commit próprio da limpeza.

## 3. Em cada tarefa: onde fazer

Veja o tamanho deste chat com `get_usage` (ferramenta do app; carregue se estiver adiada) quando a tarefa for longa. Sem essa ferramenta (fora do app), estime pelo tamanho da conversa e fique aqui na dúvida.

- **Tarefa curta** (até ~8 passos) ou chat com menos de ~120 mil de contexto: **aqui**.
- **Mesmo assunto de um chat parado** (`list_sessions`, estado ocioso): mande para ele com `SendMessage` (resumo curto, apontando arquivos). É o mais barato: não redescobre nada. Nunca para chat ocupado.
- **Tarefa longa num chat grande** (acima de ~150 mil): **chat novo** com `start_session`, `cwd` na raiz do projeto, resumo curto ("Leia CLAUDE.md e faça X; pronto quando Y"). Modelo e esforço:
  - Sonnet ou esforço menor: tarefa mecânica, só leitura, busca, relatório.
  - Opus: desenho, dinheiro, produção, código difícil.
  - Nunca acima do modelo deste chat sem o usuário pedir.

Por quê (medido): um chat novo começa com ~60 mil tokens fixos; cada passo num chat de 280 mil custa ~28 mil (cache a 10%); separar custa ~180–250 mil e economiza ~18 mil por passo. Só compensa em tarefa longa saindo de chat grande. Não passe a **publicação** para outro chat: ele redescobre tudo e corre risco.

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
- **Antes de gravar** (inclusive a própria reserva), releia só a linha `Versão:`. Mudou? Releia o topo, junte sua mudança com a nova e só então grave. Toda gravação depois da criação soma 1 na versão.
- **Reserva**: antes de mexer em arquivos, acrescente sua linha `EM USO:` na seção `## EM USO` (uma linha por chat; a hora vem do comando `date`; sem nenhuma reserva, escreva `(nenhum)`). Se outra linha já reserva os mesmos arquivos, não mexa: trabalhe em outra coisa ou pergunte. Linha com mais de 24 h vale como abandonada: **pergunte com botões** antes de assumir.
- Cada chat só altera **a própria** linha `EM USO:`.
- **Commit a cada gravação** do `CONTINUAR.md` (só os arquivos que você mudou; nunca `git add -A` com outros chats na pasta).

## 5. Publicar

Cada chat publica o próprio trabalho, seguindo o `COMBINADOS.md` (inclusive pedir OK, se a regra pedir). Dois chats no mesmo arquivo: um depois do outro (a reserva diz quem vai primeiro).

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
4. Um commit só com os arquivos que mudaram.
5. **Chat que não é mais necessário** (este, com a tarefa terminada e acima de ~60% do contexto ou sem trabalho previsto; ou um chat que ele abriu e que já acabou): depois de gravar tudo no `CONTINUAR.md` (e na memória, se houver regra nova), peça para arquivar no quadro de próximo passo, com pergunta e botões. Se a ação `archive` estiver disponível no `wrap_up`, use-a; senão, botões de resposta ("Pode arquivar" / "Ainda não") e explique que se arquiva pelo menu do chat. O próximo chat começa lendo o `CLAUDE.md`.

Trabalho interrompido no meio vira pendência escrita no `CONTINUAR.md` na hora.
