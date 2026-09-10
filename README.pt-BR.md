<p align="center">
  <img src="assets/banner.svg" alt="Attention Span — preste atenção, não em tokens" width="820">
</p>

<p align="center">
  <a href="https://github.com/alexgreensh/attention-span/releases"><img src="https://img.shields.io/github/v/release/alexgreensh/attention-span?label=vers%C3%A3o&color=6f42c1" alt="Versão mais recente"></a>
  <img src="https://img.shields.io/github/directory-file-count/alexgreensh/attention-span/output-styles?type=file&extension=md&label=estilos&color=blue" alt="estilos">
  <img src="https://img.shields.io/badge/trabalho-intacto-2ea44f" alt="trabalho intacto (benchmark com testes ocultos)">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/alexgreensh/attention-span?color=orange" alt="AGPL-3.0"></a>
  <img src="https://img.shields.io/badge/para-Claude%20Code-d97757" alt="Para Claude Code">
  <a href="https://github.com/alexgreensh/attention-span/stargazers"><img src="https://img.shields.io/github/stars/alexgreensh/attention-span?style=social" alt="Estrelas"></a>
</p>

<p align="center"><img src="assets/hero.png" alt="Mascote do Attention Span" width="900"></p>

<p align="center"><a href="README.md">English</a> · <a href="README.es-ES.md">Español</a> · <a href="README.zh-CN.md">中文</a> · <a href="README.ja.md">日本語</a> · <b>Português</b> · <a href="README.de.md">Deutsch</a> · <a href="README.fr.md">Français</a></p>

Uma pequena coleção de [estilos de saída](https://code.claude.com/docs/en/output-styles) para o Claude Code que mudam *como ele fala com você*, não como ele codifica. Resposta primeiro, linguagem simples, fácil de escanear. Cada um é um único arquivo markdown que você adiciona e ativa.

As regras de concisão por padrão cuidam da sua atenção primeiro. Reduzir a saída do Claude é um efeito colateral bem-vindo, não o objetivo.

Três até agora: **Attention-kind** (o principal), **Spartan** (conciso, zero calor) e **Rundown** (briefings em TL;DR). Cada um tem sua própria seção abaixo.

## Attention-kind

Um estilo amigável para TDAH. O Claude responde primeiro, mantém tudo curto, elimina o jargão técnico e só expande o que realmente merece sua atenção. Cada ponto é espaçado e marcado com um `→`, e as palavras importantes ficam em **negrito**, para você escanear só o negrito e ainda assim entender a resposta inteira.

A mesma capacidade de engenharia por baixo. Só muda a forma de entrega.

**Para quem é:** qualquer pessoa cuja atenção é um recurso limitado. TDAH, cansaço, imersão total no fluxo, ou simplesmente cansado de paredes de texto.

### Antes / depois

A pergunta: **"Qual banco de dados devo usar para um novo app social, PostgreSQL ou MongoDB?"** A mesma resposta, antes e depois do estilo.

<table>
<tr>
<th align="left" width="50%">Padrão &nbsp;·&nbsp; 430 palavras</th>
<th align="left" width="50%">Attention-kind &nbsp;·&nbsp; 94 palavras</th>
</tr>
<tr valign="top">
<td>

Para um novo app social, comece com PostgreSQL, e a barreira para escolher MongoDB é alta. Apps sociais são naturalmente cheios de relacionamentos: usuários seguem usuários, posts pertencem a usuários, comentários pertencem a posts, curtidas conectam usuários a posts. É uma teia de conexões, exatamente para o que um banco relacional foi feito. No MongoDB você ou amontoa dados relacionados em um único registro e briga com limites de tamanho, ou separa tudo e acaba costurando de volta no código do app de qualquer jeito. O problema do feed piora tudo: timelines, "posts de quem você segue" e buscas de amigos em comum dependem do tipo de referência cruzada que o Postgres faz em uma única query. Você ainda ganha consistência de graça, já que contagens de seguidores e verificações de "já curti isso" pedem transações de verdade… *[e continua assim]*

</td>
<td>

**→ Use PostgreSQL.** Um app social é todo relacionamento (amigos, follows, curtidas), e o Postgres lida com isso nativamente. Certo para ~90% dos novos apps sociais.

**→ Você mantém a flexibilidade.** A coluna JSONB guarda dados sem esquema dentro do mesmo banco, então você tem a flexibilidade do MongoDB sem sair do Postgres.

**→ Escolha MongoDB só se** seus dados forem documentos autocontidos, sem vínculos, e você precisar de volume massivo de escrita desde o primeiro dia.

**→ A armadilha inicial do MongoDB:** seis meses depois, cinco formatos diferentes de "usuário" e nenhuma correção limpa. O Postgres impõe a estrutura.

**→ Próximo passo:** comece com Postgres gerenciado (Supabase, Neon, RDS).

</td>
</tr>
</table>

A mesma informação. Uma delas você lê de relance.

### Isso realmente ajuda? (medido, e reproduzível)

O benchmark mede o trabalho e a saída separadamente, e os números principais **não usam juiz de LLM**. Todos os números são reproduzíveis a partir deste repositório. [Artigo completo e harness executável.](benchmarks/results/2026-08-11-benchmark.md)

- **O trabalho fica intacto.** 12 tarefas de código com suítes de testes ocultas, estilo off vs on: taxas de acerto iguais (**97% nos dois**, dentro da margem de ruído). Sem juiz, só testes passando.
- **~43% de saída mais curta** em média (mediana de 41%), e **50-71% nas respostas verbosas** onde importa; respostas já curtas quase não mudam.
- **Você chega ao ponto em ~6 palavras em vez de ~40.** A resposta está na primeira linha **75%** das vezes vs **3%**. (Notas de legibilidade não se aplicam, elas só medem comprimento de palavras e não enxergam uma parede de texto.)
- **Entregas saem limpas 88% das vezes** vs 12% sem estilo; peça uma mensagem ou um commit e você recebe exatamente isso, sem embalagem.

É mais curto, mais claro e fácil de entender de relance, com o trabalho intacto. Não afirmamos que ele produz respostas melhores; não é para isso que ele serve.

### O que muda

- **Resposta primeiro.** Conclusão na primeira linha. Sem enrolação.
- **Curto por padrão.** Diz o mínimo que responde completamente, e para.
- **Expande só o essencial**, então o tamanho em si sinaliza importância.
- **Linguagem simples.** Termos técnicos raros ganham uma definição de cinco palavras, uma vez.
- **Feito para escanear.** Marcadores `→`, negrito forte, espaçamento real entre os pontos.
- **Sem repetição.** Cada ponto traz um argumento único, nunca repetido ou reargumentado.
- **Reancora tarefas longas** e faz uma pergunta por vez, para você nunca perder o fio.
- **Comentários também.** Comentários de código herdam a regra de linguagem simples "explique o porquê", mas nunca a formatação de chat.

## Spartan

<p align="center"><img src="assets/cat-spartan.png" alt="Um gato com capacete espartano mira seu laser em uma linha acesa" width="860"></p>

Modo conciso com o calor removido. Mesmas setas e negrito do Attention-kind, mas direto e imperativo, sem suavização, sem transições, compressão máxima. Para trabalho focado quando você quer sinal, não conversa.

A pergunta: **"Três prioridades esta semana, espaço para duas, como decido o que cortar?"** Ambas são saídas reais de avaliação do Opus 5.

<table>
<tr>
<th align="left" width="50%">Padrão &nbsp;·&nbsp; 310 palavras</th>
<th align="left" width="50%">Spartan &nbsp;·&nbsp; 168 palavras</th>
</tr>
<tr valign="top">
<td>

Corte a que falha no teste mais barato: se atrasar uma semana, quem realmente sente, e quanto? Passe as três por quatro filtros rápidos e a perdedora normalmente cai sozinha. Consequência do atraso: duas das suas três provavelmente têm prazos flexíveis que você inventou e uma tem um prazo real, uma pessoa esperando, uma dependência a jusante, uma janela que fecha. Corte da pilha autoimposta, nunca da pilha "alguém está bloqueado por mim". Reversibilidade: algumas coisas ficam mais difíceis quanto mais esperam, outras ficam exatamente tão fáceis na semana que vem, então corte a que tem curva de custo plana. Quem mais é dono dela: se uma prioridade pode ser delegada ou feita a 80% por outra pessoa, é um corte melhor do que uma que só você pode fazer… *[e continua assim]*

</td>
<td>

**→ Ordene pelo custo de NÃO fazer, não pelo esforço ou interesse.** Pergunte a cada uma: o que quebra se isso escorregar uma semana? A de consequência mais leve é cortada.

**→ Elimine a reversível.** Se uma tarefa pode esperar, ser delegada ou recomeçada depois sem penalidade, corte. Proteja tudo com **prazo duro** ou **dependência** em que outros estão bloqueados por você.

**→ Rode o teste do arrependimento.** Sexta à noite, qual tarefa não feita dói mais? Fique com ela. Aquela que você ignoraria é o seu corte.

**→ Separe barulho de importância.** A prioridade que grita com você costuma ser só a mais **ansiosa**, não a mais valiosa. Corte por impacto, não por volume.

**→ Não faça as três pela metade.** Duas terminadas valem mais que três a 66%. Trabalho parcial na terceira é a armadilha, parece produtivo e não entrega nada.

**→ Corte em voz alta.** Avise quem é afetado agora, não na sexta. Um corte comunicado é uma decisão, um corte escondido é um **fracasso adiado**.

</td>
</tr>
</table>

A mesma garantia de apenas-estilo do Attention-kind: mais curto, mais escaneável, trabalho intacto. Veja o [benchmark](benchmarks/results/2026-08-11-benchmark.md).

## Rundown

<p align="center"><img src="assets/cat-rundown.png" alt="O gato Rundown mira seu laser em uma checklist, uma linha acesa" width="860"></p>

Estilo de briefing. Abre com um **TL;DR**, mostra o estado como uma checklist ✅ / 🟡 / ⬜ / ❔, marca as próximas escolhas com emoji e as numera para você escolher pelo número. Feito para atualizações de status e standups. **Otimiza para legibilidade e escaneabilidade, não para brevidade**, então use quando clareza importa mais que tamanho. Inclui uma proteção contra inventar status que não foi dado.

A pergunta: **"Resuma como está a contratação: 20 candidatos, 5 triados, 2 entrevistas, nenhuma oferta, um candidato forte escapando."** Ambas são saídas reais de avaliação do Opus 5.

<table>
<tr>
<th align="left" width="50%">Padrão &nbsp;·&nbsp; um parágrafo para ler</th>
<th align="left" width="50%">Rundown &nbsp;·&nbsp; um quadro para escanear</th>
</tr>
<tr valign="top">
<td>

A contratação está no topo do funil e fraca no fundo. Vinte candidatos entraram, cinco triados, duas entrevistas marcadas. Nenhuma oferta foi feita ainda, e essa lacuna é o problema: um dos candidatos mais fortes está esfriando enquanto o processo patina. Os números: candidatos 20, triados 5, entrevistas marcadas 2, ofertas feitas 0, em risco 1 candidato forte escapando. A leitura: é um problema de velocidade, não de oferta. O pipeline está saudável em cima, mas nada virou oferta, e o melhor prospect está indo embora. A jogada de maior valor é acelerar o candidato que está escapando antes que o atraso decida por nós. Gargalo: a etapa de oferta… *[e continua assim]*

</td>
<td>

TL;DR: O pipeline está saudável no topo mas travando na linha de chegada, e seu melhor candidato está prestes a desistir.

**Funil de contratação**
- ☑️ **Candidatos:** 20 captados
- ☑️ **Triagem:** 5 de 20 feita
- 🟡 **Entrevistas:** 2 marcadas, ainda não realizadas
- ⬜ **Oferta:** não redigida, não enviada

🔴 **Bloqueio:** Um candidato forte está escapando. Sem movimento de oferta, você o perde por inércia.

**Sua jogada:**
1. 🚀 Acelere o candidato forte, pule direto para a conversa de oferta hoje
2. 📞 Faça as 2 entrevistas marcadas antes de decidir
3. 📋 Trie mais dos 15 candidatos intocados como reserva
4. ✍️ Redija a oferta agora para ela estar pronta para disparar

Escolha um número: salvar o candidato agora (1), ou rodar o processo completo e arriscar perdê-lo?

</td>
</tr>
</table>

## Quer mesmo cortar sua conta de tokens?

O Attention Span existe para deixar as respostas dos seus agentes legíveis e fáceis de absorver de relance. A conta de tokens mais leve dessas respostas é um efeito colateral bem-vindo. Se cortar gasto de tokens é seu objetivo real, o maior custo é o *trabalho* que seu agente faz, não como ele fala, e duas ferramentas irmãs atacam isso diretamente, combinando naturalmente com estes estilos:

<p align="center"><img src="assets/save-tokens.png" alt="O mago do Outsourcerer e o gato do Attention Span aspirando tokens fantasma com o Token Optimizer" width="900"></p>

**[Token Optimizer](https://github.com/alexgreensh/token-optimizer)** ataca as três camadas de desperdício de tokens que a maioria das ferramentas nem toca:

- **Estrutural**, ex. configs inchadas, skills sem uso, memória velha
- **Runtime**, ex. saída verbosa, releituras
- **Comportamental**, ex. roteamento errado de modelo, expiração de cache, loops de retry

...e mais em cada uma. Além disso, ele comprime sua pilha de saída, faz checkpoint e restaura seu trabalho para suas sessões continuarem mesmo após compactação, e coloca cada token e dólar economizado num dashboard ao vivo. Também é a única ferramenta que mede a qualidade do seu contexto e se ajusta a ela, porque uma sessão mais barata que trabalha pior não é economia nenhuma.

*Roda no Claude Code, Codex, OpenCode, OpenClaw, Hermes e Copilot.*

**[Outsourcerer](https://github.com/alexgreensh/outsourcerer)** — fique em uma única sessão do agente que você mais gosta. Em segundo plano, ele:

- roda um esquadrão pelos modelos e harnesses que você já paga
- escolhe o melhor para cada tarefa **por benchmark, não só por preço**
- confere o trabalho deles e vigia seus limites em cada motor

Você fica com o cockpit; o trabalho pesado acontece em outro lugar.

*Funciona com Claude Code, Codex, Antigravity, Devin, Droid, Cursor, Warp e Hermes.*

O Attention Span enxuga o quanto o Claude fala. Essas duas governam quanto toda a sua stack gasta.

## Instalação

**O mais fácil: instale o plugin.** Um passo traz os três estilos, o seletor `/style` e as
skills invocadas pelo usuário (`/attention-kind`, `/spartan`, `/rundown`, `/tldr`). No Claude Code:

```
/plugin marketplace add alexgreensh/attention-span
/plugin install attention-span
```

Depois ative um estilo em `/config` → *Output style*, ou simplesmente digite uma skill como `/attention-kind`
para uma conversa. Prefere configurar na mão? Os passos manuais abaixo ainda funcionam e não mudaram.

**1.** Solte o estilo na sua pasta de output-styles. Global (todo projeto):

```bash
mkdir -p ~/.claude/output-styles
curl -o ~/.claude/output-styles/attention-kind.md \
  https://raw.githubusercontent.com/alexgreensh/attention-span/main/output-styles/attention-kind.md
```

Ou coloque em `.claude/output-styles/` dentro de um único projeto.

**2.** Defina como padrão em `~/.claude/settings.json`. Faça isso uma vez e vale para toda sessão, para sempre:

```json
{ "outputStyle": "Attention-kind" }
```

**3.** Reinicie ou use `/clear`. Pronto.

**Prefere não editar JSON?** Instale o comando `/style` e ele faz o passo 2 por você:

```bash
mkdir -p ~/.claude/commands
curl -o ~/.claude/commands/style.md \
  https://raw.githubusercontent.com/alexgreensh/attention-span/main/commands/style.md
```

Aí o `/style` mostra um popup com os estilos instalados. `/style spartan` define um na hora. `/style default` restaura o estilo padrão.

Ele procura em `~/.claude/output-styles/` e em `.claude/output-styles/` do projeto. Um estilo global é gravado em `~/.claude/settings.json`. Um estilo de projeto é gravado em `.claude/settings.local.json`, então fica fora dos checkouts dos seus colegas.

**Já tem instalado?** Os estilos são atualizados. Veja em qual versão você está e compare com o [selo de versão](https://github.com/alexgreensh/attention-span/releases) acima:

```bash
grep attention-span ~/.claude/output-styles/*.md
```

Ficou para trás? Rode de novo o comando de instalação do passo 1 para sobrescrever com a versão mais recente.

Quer testar por uma sessão primeiro? Rode `/config` e escolha em *Output style*, depois defina o padrão acima quando se convencer.

**Custo:** ~650 tokens, adicionados uma vez por sessão e cacheados após a primeira requisição. O benchmark mediu ~43% de saída mais curta, então o custo de entrada é negligível depois da primeira resposta.

## Uso nos chats do Claude (skills)

Os estilos também vêm como **skills**, então funcionam nos apps do Claude (claude.ai, desktop, mobile), não
só no Claude Code. Instale o plugin acima, ou adicione os arquivos de skill diretamente, e digite o comando:

- `/attention-kind`, `/spartan` ou `/rundown` — conversa nesse estilo pelo resto da conversa.
- `/tldr` — comprime um documento, thread, transcrição ou texto colado num briefing escaneável. (Os
  estilos moldam como o Claude reporta o *próprio* trabalho; o `/tldr` comprime algo que *outra pessoa* escreveu.)

As skills são **somente invocadas pelo usuário** (`disable-model-invocation`), então custam zero contexto passivo
até você chamar uma, e são geradas das mesmas fontes de estilo (`scripts/gen-skills.py`), então nunca
divergem do texto principal.

## Uso com outros agentes

O corpo do estilo é markdown puro, sem comportamento específico do Claude. A única parte do Claude Code é o frontmatter YAML no topo de cada arquivo (o bloco `name`/`description` que o seletor do `/config` lê). Outros agentes ignoram ou engasgam com frontmatter, então a instalação o remove.

Cada arquivo de estilo tem um marcador `<!-- body-start -->` depois do frontmatter. O comando de remoção é um `sed`:

```bash
curl -sfL <raw-url> | sed '1,/<!-- body-start -->/d'
```

Isso dá um markdown de corpo limpo, pronto para soltar no arquivo de regras ou instruções de qualquer agente.

### Instalação por agente

**Devin** (global, via compatibilidade Windsurf):

```bash
mkdir -p ~/.codeium/windsurf/memories
curl -sfL https://raw.githubusercontent.com/alexgreensh/attention-span/main/output-styles/attention-kind.md -o /tmp/attention-span.md \
  && sed '1,/<!-- body-start -->/d' /tmp/attention-span.md > ~/.codeium/windsurf/memories/attention-kind.md
```

Ou no nível do projeto: `.windsurf/rules/attention-kind.md` na raiz do seu repo.

**Codex** (anexar ao `AGENTS.md` global, idempotente via marcadores cercados):

```bash
mkdir -p ~/.codex
curl -sfL https://raw.githubusercontent.com/alexgreensh/attention-span/main/output-styles/attention-kind.md -o /tmp/attention-span.md \
  && { printf '\n<!-- attention-span:start -->\n'; sed '1,/<!-- body-start -->/d' /tmp/attention-span.md; printf '<!-- attention-span:end -->\n'; } >> ~/.codex/AGENTS.md
```

Para atualizar depois, remova o bloco antigo primeiro (in place) e rode a instalação de novo: `sed -i.bak '/<!-- attention-span:start -->/,/<!-- attention-span:end -->/d' ~/.codex/AGENTS.md`.

**Antigravity CLI (agy)** (`GEMINI.md` no nível do projeto, idempotente via marcadores cercados):

```bash
curl -sfL https://raw.githubusercontent.com/alexgreensh/attention-span/main/output-styles/attention-kind.md -o /tmp/attention-span.md \
  && { printf '\n<!-- attention-span:start -->\n'; sed '1,/<!-- body-start -->/d' /tmp/attention-span.md; printf '<!-- attention-span:end -->\n'; } >> GEMINI.md
```

Rode isso na raiz do seu repo. O agy descobre o `GEMINI.md` (ou `AGENTS.md`) subindo do diretório atual até a raiz do repo, então o estilo se aplica àquele projeto e a todos os subdiretórios.

Para atualizar depois, remova o bloco antigo primeiro (in place) e rode a instalação de novo: `sed -i.bak '/<!-- attention-span:start -->/,/<!-- attention-span:end -->/d' GEMINI.md`.

Para instalação global (todos os projetos sob seu home), anexe a `~/GEMINI.md`; o agy encontra na subida a partir de qualquer projeto.

Troque `attention-kind.md` por `spartan.md` ou `rundown.md` para instalar outro estilo. Mesmos comandos, nome de arquivo diferente.

**Notas:**

- O Devin carrega regras pela camada de compatibilidade Windsurf/Cursor, não por um diretório nativo de regras. O caminho `~/.codeium/windsurf/memories/` é global; `.windsurf/rules/` é por projeto.
- O Codex anexa a um `AGENTS.md` compartilhado, então os marcadores cercados (`<!-- attention-span:start -->` / `<!-- attention-span:end -->`) permitem atualizar ou remover o bloco sem duplicatas.
- O Antigravity CLI (agy) descobre regras subindo do cwd até a raiz do repo, carregando qualquer `GEMINI.md` ou `AGENTS.md` que encontrar. Sem suporte a frontmatter para regras avulsas. A instalação global funciona colocando o `GEMINI.md` num diretório pai (ex. `~/`) que está sempre no caminho de subida.
- O corpo tem ~650 tokens de entrada, carregados no início de cada sessão. O Claude Code cacheia após a primeira requisição; outros agentes podem ou não cachear (depende do provedor). A economia de saída (~43%) supera em muito o custo de entrada em poucas respostas.
- A remoção com `sed` assume macOS/Linux. No Windows, use WSL ou Git Bash.

## Os estilos

| Estilo | Arquivo | Melhor para |
|---|---|---|
| Attention-kind | [`output-styles/attention-kind.md`](output-styles/attention-kind.md) | TDAH, fadiga de atenção, quem está cansado de paredes de texto |
| Spartan | [`output-styles/spartan.md`](output-styles/spartan.md) | Modo espartano: sinal máximo, zero calor, trabalho focado |
| Rundown | [`output-styles/rundown.md`](output-styles/rundown.md) | Briefings, standups, atualizações de progresso (TL;DR + caixas de seleção) |

Cada um é um arquivo markdown legível, fácil de adaptar.

## Notas

- Os estilos se aplicam **somente à conversa principal**. Subagentes rodam com seu próprio prompt.
- Eles mantêm intacto o comportamento de código do Claude (`keep-coding-instructions: true`).

## Licença

AGPL-3.0. Veja [LICENSE](LICENSE).
