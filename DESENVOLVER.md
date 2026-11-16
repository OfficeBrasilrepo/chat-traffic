# Como mudar a chat-traffic sem ela perder o sentido

Objetivo que nunca muda: **economizar tokens sem perder qualidade**, delegar só a quem dá conta da tarefa, e manter os chats organizados.

Toda mudança passa por esta conferência antes do commit:

1. **Quanto custa?** `wc -c SKILL.md`. O SKILL.md é lido em todo chat que usa a skill (~1 token a cada 3,5 caracteres, gravado no cache a ~200%). Teto: **~12 mil caracteres**. Passou? Leve detalhe para um arquivo à parte (`modelos/`, `scripts/`), lido só quando precisa.
2. **Quanto devolve?** Escreva em uma linha qual economia ou qual ganho de qualidade a mudança traz e quando. Sem resposta clara, não entra.
3. **Custa passo?** Instrução que faz o chat chamar uma ferramenta a mais em todo turno custa ~10% do contexto por chamada. Prefira o mesmo passo de outra ferramenta, ou um gancho (hook) que não gasta tokens.
4. **Ainda funciona?** Rode os testes dos scripts (`python scripts/alarme.py --teste`, `python scripts/relatorio.py --teste`) e repita os dois ensaios com um subagente Sonnet, em cópia: projeto novo e projeto existente com `CONTINUAR.md` grande. Peça a ele a lista do que ficou ambíguo e corrija.
5. **Ainda compensa?** Com uma semana de `chat-traffic-uso.csv`, rode `python scripts/relatorio.py` e compare com a semana anterior. Regra que não se paga sai.

Registre a mudança e o resultado da conferência na mensagem do commit.
