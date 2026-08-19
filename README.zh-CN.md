<p align="center">
  <img src="assets/banner.svg" alt="Attention Span — 关注注意力，而非 token" width="820">
</p>

<p align="center">
  <a href="https://github.com/alexgreensh/attention-span/releases"><img src="https://img.shields.io/github/v/release/alexgreensh/attention-span?label=%E7%89%88%E6%9C%AC&color=6f42c1" alt="最新版本"></a>
  <img src="https://img.shields.io/github/directory-file-count/alexgreensh/attention-span/output-styles?type=file&extension=md&label=%E9%A3%8E%E6%A0%BC&color=blue" alt="风格数量">
  <img src="https://img.shields.io/badge/%E5%B7%A5%E4%BD%9C-%E6%9C%AA%E5%8F%97%E5%BD%B1%E5%93%8D-2ea44f" alt="工作未受影响（隐藏测试基准）">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/alexgreensh/attention-span?color=orange" alt="AGPL-3.0"></a>
  <img src="https://img.shields.io/badge/%E9%80%82%E7%94%A8%E4%BA%8E-Claude%20Code-d97757" alt="适用于 Claude Code">
  <a href="https://github.com/alexgreensh/attention-span/stargazers"><img src="https://img.shields.io/github/stars/alexgreensh/attention-span?style=social" alt="Stars"></a>
</p>

<p align="center"><img src="assets/hero.png" alt="Attention Span 吉祥物" width="900"></p>

<p align="center"><a href="README.md">English</a> · <a href="README.es-ES.md">Español</a> · <b>中文</b></p>

一小组给 Claude Code 用的[输出风格](https://code.claude.com/docs/en/output-styles)，只改变它*怎么跟你说话*，不改变它怎么写代码。答案先行、大白话、易于扫读。每个风格都是一个 markdown 文件，放进去、切换开启即可。

「默认简洁」的规则首先是善待你的注意力。顺带削减了 Claude 的输出，是受欢迎的副产品，而不是目的。

目前有三款：**Attention-kind**（旗舰款）、**Spartan**（极简、零温度）、**Rundown**（TL;DR 简报）。每一款下面都有各自的章节。

## Attention-kind

一款对 ADHD（注意力缺陷）友好的风格。Claude 答案先行、保持简短、去掉术语，只在真正值得你注意的地方展开。每个要点都有空行隔开、用 `→` 标记，重点词加**粗**，所以你只扫读粗体也能拿到完整答案。

底层的工程能力完全一样。变的只是表达方式。

**适合谁：** 任何把注意力当作稀缺资源的人。ADHD、疲惫、正在心流里，或者只是受够了大段文字。

### 前后对比

问题：**「新做一个社交 app，数据库该用 PostgreSQL 还是 MongoDB？」** 同一个答案，套用风格前后的样子。

<table>
<tr>
<th align="left" width="50%">默认 &nbsp;·&nbsp; 430 词</th>
<th align="left" width="50%">Attention-kind &nbsp;·&nbsp; 94 词</th>
</tr>
<tr valign="top">
<td>

对于新的社交 app，先从 PostgreSQL 开始，改选 MongoDB 的门槛很高。社交 app 天生就是关系密集型的：用户关注用户、帖子属于用户、评论属于帖子、点赞把用户和帖子连起来。这是一张连接之网，正是关系型数据库被设计出来处理的东西。在 MongoDB 里，你要么把相关数据塞进一条记录里、跟大小上限较劲，要么把它们拆开、最后还是在应用代码里把它们重新拼回去。信息流的问题让这更糟：时间线、「你关注的人的帖子」、共同好友查询，全都依赖 Postgres 用一条查询就能完成的那种交叉引用。你还能免费得到一致性，因为关注数和「我是不是已经点过赞了」这类检查需要真正的事务…… *[后面还是这样一直写下去]*

</td>
<td>

**→ 用 PostgreSQL。** 社交 app 全是关系（好友、关注、点赞），而 Postgres 原生就能处理。适合约 90% 的新社交 app。

**→ 灵活性照样在。** 它的 JSONB 字段能在同一个数据库里存无模式数据，让你不离开 Postgres 就拿到 MongoDB 的那份松散。

**→ 只有在以下情况才选 MongoDB：** 你的数据是彼此无关联的独立文档，而且第一天就需要极大的写入量。

**→ MongoDB 的早期陷阱：** 半年后，「用户」有五种不同的形状，且没有干净的补救办法。Postgres 会强制结构。

**→ 下一步：** 从托管 Postgres 起步（Supabase、Neon、RDS）。

</td>
</tr>
</table>

同样的信息。其中一个你一眼就能读完。

### 真的有用吗？（已测量、可复现）

这个基准把「工作」和「输出」分开衡量，头条数字**不用任何 LLM 裁判**。每个数字都能从本仓库复现。[完整说明与可运行的测试框架。](benchmarks/results/2026-08-11-benchmark.md)

- **工作原封不动。** 12 个带隐藏测试套件的编码任务，关风格 vs 开风格：通过率相等（**都是 97%**，在噪声范围内）。没有裁判，只有测试通过与否。
- **输出平均短约 43%**（中位数 41%），在真正要紧的**冗长回答上短 50-71%**；本来就短的回答几乎不变。
- **你用约 6 个词就到点，而不是约 40 个词。** 答案出现在第一行的比例是 **75%**，对比默认的 **3%**。（可读性年级分不适用，它们只量词长，看不出一堵文字墙。）
- **交付物有 88% 的时候是干净的**，对比无风格时的 12%：你要一条消息或一次 commit，拿到的就是那个，没有包装。

更短、更清楚、一眼就能领会，同时工作原封不动。我们不声称它产出更好的答案，那不是它的用途。

### 有哪些变化

- **答案先行。** 结论放第一行。不做铺垫。
- **默认简短。** 说完足以完整回答的最少内容，然后就停。
- **只在关键处展开**，让篇幅本身成为重要性的信号。
- **大白话。** 少见的技术术语给一个五词以内的解释，且只给一次。
- **为扫读而生。** `→` 标记、大量粗体、要点之间有真正的空行。
- **不重复。** 每个要点只做一个独立论证，绝不复述或反复论证。
- **长任务会重新锚定**，且一次只问一个问题，让你永远不丢线索。
- **注释也一样。** 代码注释继承「解释为什么」的大白话规则，但绝不带聊天里的格式。

## Spartan

<p align="center"><img src="assets/cat-spartan.png" alt="一只戴斯巴达头盔的猫，把激光对准一行点亮的字" width="860"></p>

极简模式，把温度剥掉。和 Attention-kind 一样的箭头和粗体，但直白、命令式，不缓冲、不过渡，最大压缩。适合埋头干活、只要信号不要对话的时候。

问题：**「这周三个优先事项，只有做两个的余地，我该怎么决定砍哪个？」** 两个都是 Opus 5 的真实评测输出。

<table>
<tr>
<th align="left" width="50%">默认 &nbsp;·&nbsp; 310 词</th>
<th align="left" width="50%">Spartan &nbsp;·&nbsp; 168 词</th>
</tr>
<tr valign="top">
<td>

砍掉那个通不过最便宜检验的：如果它推迟一周，谁真正会感到疼、疼多少。把三个都过一遍四个快速筛子，输的那个通常自己就掉出来了。延迟的后果：你三个里大概有两个的截止日期是你自己发明的软日期，一个是真的，有人在等、下游有依赖、有一扇会关上的窗。从自己强加的那堆里砍，绝不从「有人被你卡住」的那堆里砍。可逆性：有些事拖得越久越难，有些下周做也一样容易，所以砍掉成本曲线平的那个。除了你还有谁负责它：如果一个优先事项能被委派、或者别人能做到 80%，那它比只有你能做的那个更该砍…… *[后面还是这样一直写下去]*

</td>
<td>

**→ 按「不做的代价」排序，不按投入或兴趣。** 逐个问：这个推迟一周，会有什么坏掉？后果最软的那个砍掉。

**→ 砍掉可逆的那个。** 如果一个任务能等、能委派、或事后重启且无惩罚，砍掉它。守住任何有**硬截止**或有**依赖**、别人被你卡住的事。

**→ 做后悔测试。** 周五晚上，哪个没做完的任务最扎心？留下那个。你会耸耸肩的那个就是你要砍的。

**→ 把吵闹和重要分开。** 冲你喊得最凶的优先事项，往往只是最**焦虑**的，不是最有价值的。按影响砍，别按音量。

**→ 别把三个都做一半。** 两个做完胜过三个各 66%。在第三个上做的半截活是陷阱，它感觉高产、却什么都交付不出。

**→ 大声地砍。** 现在就告诉受影响的人，别等周五。你标出来的砍是一个决定，你藏起来的砍是一个**延迟发作的失败**。

</td>
</tr>
</table>

和 Attention-kind 一样的「只改风格」保证：更短、更易扫读，工作原封不动。见[基准](benchmarks/results/2026-08-11-benchmark.md)。

## Rundown

<p align="center"><img src="assets/cat-rundown.png" alt="Rundown 的猫把激光对准一份清单，其中一行点亮" width="860"></p>

简报风格。以 **TL;DR** 开头，用 ✅ / 🟡 / ⬜ 清单展示状态，用 emoji 标注接下来的选项。为状态更新和站会而生。**它优化的是可读性和可扫读性，不是简洁**，所以当清楚比短更重要时用它。内置一道防线，防止它编造没给过它的状态。

问题：**「总结一下招聘进展：20 位申请人，5 位初筛，2 场面试，还没发 offer，一位强候选人正在流失。」** 两个都是 Opus 5 的真实评测输出。

<table>
<tr>
<th align="left" width="50%">默认 &nbsp;·&nbsp; 一段读的文字</th>
<th align="left" width="50%">Rundown &nbsp;·&nbsp; 一块扫的看板</th>
</tr>
<tr valign="top">
<td>

招聘目前是漏斗顶部厚、底部薄。二十份申请进来，五份初筛，两场面试已约。还没有 offer 发出去，而这道缺口就是问题：最强的候选人之一正在冷下来，而流程却在空转。数字：申请 20，初筛 5，已约面试 2，发出 offer 0，有风险 1 位正在流失的强候选人。判断：这是速度问题，不是供给问题。漏斗上部健康，但没有一个转化成 offer，最好的人选正在飘走。价值最高的动作是在延迟替我们做决定之前，加速那位正在流失的候选人。瓶颈：offer 阶段…… *[后面还是这样一直写下去]*

</td>
<td>

TL;DR：漏斗上部健康，但终点线在卡壳，你最好的候选人快走了。

**招聘漏斗**
- ☑️ **申请进来：** 20 份来源
- ☑️ **已初筛：** 20 中的 5 份完成
- 🟡 **面试：** 已约 2 场，尚未进行
- ⬜ **Offer：** 未起草、未发出

🔴 **阻塞点：** 一位强候选人正在流失。没有 offer 动作，意味着你会默认失去他们。

**你的一步：**
- 🚀 加速那位强候选人，今天就直接跳到谈 offer
- 📞 在决定前把已约的 2 场面试跑完
- 📋 从没碰过的 15 份申请里多筛一些做备选
- ✍️ 现在就把 offer 起草好，随时能发

选一个：现在就保住候选人，还是跑完整流程、承担失去他们的风险？

</td>
</tr>
</table>

## 真的想削减你的 token 账单吗？

Attention Span 的目的，是让你的智能体的回答变得可读、一眼能领会。那些回答上更轻的 token 账单是一份受欢迎的副产品。如果削减 token 开销才是你真正的目标，那更大的成本是你智能体做的*工作*，而不是它怎么说话，有两个姊妹工具正对着这一点下手，和这些风格天然配套：

<p align="center"><img src="assets/save-tokens.png" alt="Outsourcerer 巫师和 Attention Span 的猫用 Token Optimizer 吸走幽灵 token" width="900"></p>

**[Token Optimizer](https://github.com/alexgreensh/token-optimizer)** 直击大多数工具从不触碰的三层 token 浪费：

- **结构层**，例如臃肿的配置、没用的 skill、过期的记忆
- **运行层**，例如冗长的输出、重复读取
- **行为层**，例如模型路由错误、缓存过期、重试循环

……每一层里还不止这些。在此之上，它压缩你的输出栈，为你的工作做检查点并恢复，让你的会话在压缩（compaction）后仍然连续，并把省下的每个 token 和每一块钱放到一个实时看板上。它还是唯一一个衡量你上下文质量并据此调整的工具，因为一个更便宜、却把活干得更差的会话，根本算不上省。

*支持 Claude Code、Codex、OpenCode、OpenClaw、Hermes 和 Copilot。*

**[Outsourcerer](https://github.com/alexgreensh/outsourcerer)** —— 待在你最喜欢的那个智能体的同一个会话里。它在后台：

- 在你已经付费的那些模型和框架之间跑一支小队
- **按基准而非只按价格**，为每个任务挑最好的那个
- 检查它们的工作，并在每个引擎里盯着你的额度

驾驶舱还是你的；重活在别处发生。

*可用于 Claude Code、Codex、Antigravity、Devin、Droid、Cursor、Warp 和 Hermes。*

Attention Span 削减 Claude 说多少。这两个则管着你整个技术栈花多少。

## 安装

**1.** 把风格放进你的 output-styles 文件夹。全局（所有项目）：

```bash
mkdir -p ~/.claude/output-styles
curl -o ~/.claude/output-styles/attention-kind.md \
  https://raw.githubusercontent.com/alexgreensh/attention-span/main/output-styles/attention-kind.md
```

或者放进某个单独项目里的 `.claude/output-styles/`。

**2.** 在 `~/.claude/settings.json` 里把它设为默认。设一次，之后每个会话都开着，永久生效：

```json
{ "outputStyle": "Attention-kind" }
```

**3.** 重启或 `/clear`。就这样。

**不想改 JSON？** 装上 `/style` 命令，它替你做第 2 步：

```bash
mkdir -p ~/.claude/commands
curl -o ~/.claude/commands/style.md \
  https://raw.githubusercontent.com/alexgreensh/attention-span/main/commands/style.md
```

然后 `/style` 会弹出你已安装风格的列表。`/style spartan` 直接设一个。`/style default` 把内置风格换回来。

它会在 `~/.claude/output-styles/` 和某个项目的 `.claude/output-styles/` 里查找。全局风格写进 `~/.claude/settings.json`。项目风格写进 `.claude/settings.local.json`，所以它不会进到你队友的检出里。

**已经装过了？** 风格会有更新。查一下你在哪个版本，和上面的[版本徽章](https://github.com/alexgreensh/attention-span/releases)对一下：

```bash
grep attention-span ~/.claude/output-styles/*.md
```

落后了？重跑第 1 步的安装命令，用最新版覆盖。

想先试用一个会话？运行 `/config`，在 *Output style* 里选它，试到满意后再按上面设成默认。

**成本：** 约 650 个 token，每个会话加载一次，首次请求后即被缓存。基准测得输出短约 43%，所以首次回复之后，这点输入成本可以忽略不计。

## 配合其他智能体使用

风格正文是纯 markdown，没有任何 Claude 专属行为。唯一属于 Claude Code 的部分，是每个文件顶部的 YAML frontmatter（`/config` 选择器读取的 `name`/`description` 块）。其他智能体会忽略 frontmatter 或被它卡住，所以安装时会把它剥掉。

每个风格文件在 frontmatter 之后有一个 `<!-- body-start -->` 标记。剥离命令就是一条 `sed`：

```bash
curl -sfL <raw-url> | sed '1,/<!-- body-start -->/d'
```

这样就得到干净的正文 markdown，可以直接放进任何智能体的规则或指令文件里。

### 各智能体安装方式

**Devin**（全局，通过 Windsurf 兼容层）：

```bash
mkdir -p ~/.codeium/windsurf/memories
curl -sfL https://raw.githubusercontent.com/alexgreensh/attention-span/main/output-styles/attention-kind.md -o /tmp/attention-span.md \
  && sed '1,/<!-- body-start -->/d' /tmp/attention-span.md > ~/.codeium/windsurf/memories/attention-kind.md
```

或项目级：仓库根目录的 `.windsurf/rules/attention-kind.md`。

**Codex**（追加到全局 `AGENTS.md`，用围栏标记保证幂等）：

```bash
mkdir -p ~/.codex
curl -sfL https://raw.githubusercontent.com/alexgreensh/attention-span/main/output-styles/attention-kind.md -o /tmp/attention-span.md \
  && { printf '\n<!-- attention-span:start -->\n'; sed '1,/<!-- body-start -->/d' /tmp/attention-span.md; printf '<!-- attention-span:end -->\n'; } >> ~/.codex/AGENTS.md
```

之后要更新，先就地移除旧块，再重跑安装：`sed -i.bak '/<!-- attention-span:start -->/,/<!-- attention-span:end -->/d' ~/.codex/AGENTS.md`。

**Antigravity CLI (agy)**（项目级 `GEMINI.md`，用围栏标记保证幂等）：

```bash
curl -sfL https://raw.githubusercontent.com/alexgreensh/attention-span/main/output-styles/attention-kind.md -o /tmp/attention-span.md \
  && { printf '\n<!-- attention-span:start -->\n'; sed '1,/<!-- body-start -->/d' /tmp/attention-span.md; printf '<!-- attention-span:end -->\n'; } >> GEMINI.md
```

在你的仓库根目录运行。agy 会从当前目录向上走到仓库根来发现 `GEMINI.md`（或 `AGENTS.md`），所以风格会作用于该项目及其所有子目录。

之后要更新，先就地移除旧块，再重跑安装：`sed -i.bak '/<!-- attention-span:start -->/,/<!-- attention-span:end -->/d' GEMINI.md`。

若要全局安装（作用于你家目录下的所有项目），改为追加到 `~/GEMINI.md`，agy 从任何项目向上走时都会找到它。

把 `attention-kind.md` 换成 `spartan.md` 或 `rundown.md` 就能装另一款风格。命令一样，只是文件名不同。

**说明：**

- Devin 通过它的 Windsurf/Cursor 兼容层加载规则，而不是原生的规则目录。`~/.codeium/windsurf/memories/` 路径是全局的；`.windsurf/rules/` 是按项目的。
- Codex 追加到共享的 `AGENTS.md`，所以围栏标记（`<!-- attention-span:start -->` / `<!-- attention-span:end -->`）让你能在不产生重复的情况下更新或移除该块。
- Antigravity CLI (agy) 通过从 cwd 向上走到仓库根来发现规则，加载沿途找到的任何 `GEMINI.md` 或 `AGENTS.md`。独立规则不支持 frontmatter。全局安装的做法是把 `GEMINI.md` 放到一个始终在向上路径里的父目录（例如 `~/`）。
- 正文约 650 个 token 的输入，在每个会话开始时加载。Claude Code 在首次请求后缓存它；其他智能体是否缓存视提供方而定。无论哪种，输出上的节省（约 43%）几次回复内就盖过了输入成本。
- 这条 `sed` 剥离假设是 macOS/Linux。在 Windows 上，用 WSL 或 Git Bash。

## 各款风格

| 风格 | 文件 | 最适合 |
|---|---|---|
| Attention-kind | [`output-styles/attention-kind.md`](output-styles/attention-kind.md) | ADHD、注意力疲劳、任何受够了文字墙的人 |
| Spartan | [`output-styles/spartan.md`](output-styles/spartan.md) | Spartan 模式：最大信号、零温度、埋头干活 |
| Rundown | [`output-styles/rundown.md`](output-styles/rundown.md) | 简报、站会、进展更新（TL;DR + 清单框） |

每一款都是一个可读的 markdown 文件，容易改。

## 说明

- 风格**只作用于主对话**。子智能体运行它们自己的提示词。
- 这些风格保持 Claude 的编码行为不变（`keep-coding-instructions: true`）。

## 许可证

AGPL-3.0。见 [LICENSE](LICENSE)。
