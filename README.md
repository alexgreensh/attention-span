<p align="center">
  <img src="assets/banner.svg" alt="Attention Span — pay attention, not tokens" width="820">
</p>

<p align="center"><img src="assets/hero.png" alt="Attention Span mascot" width="900"></p>

A small collection of [output styles](https://code.claude.com/docs/en/output-styles) for Claude Code that change how it *talks to you*, not how it codes. Answer-first, plain English, easy to skim. Each one is a single markdown file you drop in and switch on.

The concise-by-default rules aren't just kind to your attention, they trim Claude's output, so you literally spend fewer tokens. The pun pays for itself.

Three so far: **Attention-kind** (the flagship), **Spartan** (terse, zero warmth), and **Rundown** (TL;DR briefings). Each has its own section below.

## Attention-kind

An ADHD-friendly style. Claude answers first, keeps it short, drops the jargon, and expands only on what's actually worth your attention. Every point is spaced out and marked with a `→`, and the important words are **bold**, so you can skim just the bold and still get the whole answer.

Same engineering ability underneath. Only the delivery changes.

**Who it's for:** anyone whose attention is a limited resource. ADHD, tired, deep in flow, or just done with walls of text.

### Before / after

The question: **"Which database should I use for a new social app, PostgreSQL or MongoDB?"** Same answer, before and after the style.

<table>
<tr>
<th align="left" width="50%">Default &nbsp;·&nbsp; 430 words</th>
<th align="left" width="50%">Attention-kind &nbsp;·&nbsp; 120 words</th>
</tr>
<tr valign="top">
<td>

For a new social app, start with PostgreSQL, and the bar for choosing MongoDB instead is high. Social apps are relationship-heavy by nature: users follow users, posts belong to users, comments belong to posts, likes connect users to posts. That's a web of connections, exactly what a relational database is built for. In MongoDB you either cram related data into one record and fight size limits, or split it out and end up stitching it back together in your app code anyway. The feed problem makes this worse: timelines, "posts from people you follow," and mutual-friend lookups all lean on the kind of cross-referencing Postgres does in a single query. You also get consistency for free, since follow counts and "did I already like this" checks want real transactions…

</td>
<td>

**→ Use PostgreSQL.** A social app is all relationships (friends, follows, likes), and Postgres handles those natively. Right for ~90% of new social apps.

**→ You keep flexibility.** Its JSONB column stores schema-less data inside the same database, so you get MongoDB's looseness without leaving Postgres.

**→ Pick MongoDB only if** your data is self-contained documents with no links, and you need massive write volume on day one.

**→ The early trap with MongoDB:** six months in, five different shapes of "user" and no clean fix. Postgres forces the structure.

**→ Next:** start on managed Postgres (Supabase, Neon, RDS).

</td>
</tr>
</table>

Same information. One of them you can read at a glance.

### Does it actually help? (measured)

12 questions across 8 categories (dev, research, analysis, explaining, writing, quick lookups), each answered 4 times, two runs averaged, scored by a separate judge. [Full results.](benchmarks/results/2026-08-05-diverse-variance.md)

- **47% fewer output tokens.**
- **Answer-first: 63% → 96%.** The default buried the answer under preamble a third of the time.
- **Skimmability: 2.7 → 4.8**, on a scale anchored to an ADHD reader (dense prose caps at 2, no matter how well organized).
- **Unexplained jargon: 2.0 → 0.9 terms per answer.**
- **Correctness held at 100%** across all 48 answers. Shorter cost nothing.

It holds beyond code: research (-53%), analysis (-55%), and explaining (-50%) cut as hard as debugging. The one place it barely moves is already-short output, a two-line email only shrank 4%, because the style trims rambling and leaves tight answers alone. The gains scale with how much Claude would have over-explained. [Earlier dev-only run, Opus 4.8 vs 5.](benchmarks/results/2026-08-04-attention-kind-vs-default.md)

### What changes

- **Answer first.** Conclusion in line one. No wind-up.
- **Short by default.** Says the least that fully answers, then stops.
- **Expands only on what's vital**, so length itself signals importance.
- **Plain English.** Rare technical terms get a five-word definition, once.
- **Built to scan.** `→` markers, heavy bold, real spacing between points.
- **No repetition.** Each point makes one distinct argument, never restated or re-argued.
- **Re-anchors long tasks** and asks one question at a time, so you never lose the thread.
- **Comments too.** Code comments inherit the plain-English "explain the why" rule, but never the chat formatting.

## Spartan

<p><img src="assets/cat-spartan.png" alt="A cat in a Spartan helmet aims its laser at one lit line" width="300"></p>

Terse mode with the warmth stripped out. Same arrows and bold as Attention-kind, but blunt and imperative, no cushioning, no transitions, maximum compression. For heads-down work when you want signal, not conversation.

Same question as above, **"PostgreSQL or MongoDB for a new social app?"** Both real Opus 5 eval outputs.

<table>
<tr>
<th align="left" width="50%">Default &nbsp;·&nbsp; 449 words</th>
<th align="left" width="50%">Spartan &nbsp;·&nbsp; 199 words</th>
</tr>
<tr valign="top">
<td>

For a new social app, default to PostgreSQL. Social apps are relationship engines. Users follow users, posts have authors, comments nest under posts, likes join users to content, feeds fan out across a graph. That is a highly relational workload, exactly what a relational database is built for. Joins, foreign keys, and transactional integrity are core features in Postgres, not bolt-ons. Consistency that matters socially: follow counts, like counts, and "did this send" all benefit from ACID transactions. In Mongo you often end up hand-rolling consistency across documents. It is also a good document store: Postgres has native JSONB with indexing, so the flexible-schema pitch for Mongo is largely neutralized…

</td>
<td>

**→ PostgreSQL. Default to it for a social app.**

**→ Social data is relational.** Users, follows, likes, feeds. All joins between entities. Postgres does joins natively; Mongo makes you fake them in app code.

**→ Postgres does JSON too.** JSONB gives you Mongo's flexible-schema trick when you need it, without giving up structure.

**→ Consistency matters.** Follower counts, likes, payments. Postgres has real transactions across tables. Mongo's are bolted on and slower.

**→ Mongo only if** your data is genuinely document-shaped and schema-chaotic.

</td>
</tr>
</table>

Opus 5 eval (4 questions): **~50% fewer tokens** than default, skimmability to **5.0**, correctness held. [Full results.](benchmarks/results/2026-08-05-pointblank-and-rundown-opus5.md)

## Rundown

<p><img src="assets/cat-rundown.png" alt="The Rundown cat aims its laser at a checklist, one line lit" width="300"></p>

Briefing style. Opens with a **TL;DR**, shows state as a ✅ / 🟡 / ⬜ checklist, tags the next choices with emoji. Built for status updates and standups. It trades tokens for scannability, so use it for clarity, not to shrink output. Includes a guard against inventing status it wasn't given.

The question: **"Summarize where hiring stands: 20 applicants, 5 screened, 2 interviews, no offer, one strong candidate slipping."** Both real Opus 5 eval outputs.

<table>
<tr>
<th align="left" width="50%">Default &nbsp;·&nbsp; 154 words</th>
<th align="left" width="50%">Rundown &nbsp;·&nbsp; 127 words</th>
</tr>
<tr valign="top">
<td>

Hiring stands at the top of the funnel and thin at the bottom. Twenty applicants in, five screened, two interviews booked. No offer has gone out yet, and that gap is the problem: one of the strongest candidates is cooling off while the process idles. The numbers: applicants 20, screened 5, interviews booked 2, offers out 0, at risk 1 strong candidate slipping away. The read: this is a speed problem, not a supply problem. The pipeline is healthy up top, but nothing has converted to an offer, and the best prospect is drifting. The highest-value move is to fast-track the slipping candidate before the delay decides for us. Bottleneck: the offer stage…

</td>
<td>

**TL;DR:** healthy up top, the finish line is stalling, and your best candidate is about to walk.

**Hiring funnel**
- ☑️ **Applicants:** 20 sourced
- ☑️ **Screened:** 5 of 20
- 🟡 **Interviews:** 2 booked, not run
- ⬜ **Offer:** not drafted

🔴 **Blocker:** one strong candidate slipping. No offer motion means you lose them by default.

**Your move:**
- 🚀 Fast-track them to an offer today
- 📞 Run the 2 booked interviews
- ✍️ Draft the offer now

</td>
</tr>
</table>

## Install

**1.** Copy the style you want into your output-styles folder.

Global (every project):

```bash
mkdir -p ~/.claude/output-styles
curl -o ~/.claude/output-styles/attention-kind.md \
  https://raw.githubusercontent.com/alexgreensh/attention-span/main/output-styles/attention-kind.md
```

Or drop the file into `.claude/output-styles/` inside a single project.

**2.** Run `/config`, pick the style under *Output style*.

**3.** Optional, make it the permanent default in `~/.claude/settings.json`:

```json
{ "outputStyle": "Attention-kind" }
```

**4.** Restart or `/clear`. Styles load once at session start.

**Cost:** ~650 tokens, added once per session and cached after the first request. The eval measured ~48% lower output, so it pays for itself within the first couple of replies.

## The styles

| Style | File | Best for |
|---|---|---|
| Attention-kind | [`output-styles/attention-kind.md`](output-styles/attention-kind.md) | ADHD, attention fatigue, anyone tired of walls of text |
| Spartan | [`output-styles/spartan.md`](output-styles/spartan.md) | Spartan mode: maximum signal, zero warmth, heads-down work |
| Rundown | [`output-styles/rundown.md`](output-styles/rundown.md) | Briefings, standups, progress updates (TL;DR + checkboxes) |

Each is one readable markdown file, easy to adapt.

## Notes

- Styles apply to the **main conversation only**. Subagents run their own prompt.
- These keep Claude's coding behavior intact (`keep-coding-instructions: true`).

## License

AGPL-3.0. See [LICENSE](LICENSE).
