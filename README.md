<p align="center">
  <img src="assets/wordmark.svg" alt="Attention Span — pay attention, not tokens" width="780">
</p>

![A blissful cat in a whirlwind of scattered paper points a laser at one clean block of text](assets/hero.png)

A small collection of [output styles](https://code.claude.com/docs/en/output-styles) for Claude Code that change how it *talks to you*, not how it codes. Answer-first, plain English, easy to skim. Each one is a single markdown file you drop in and switch on.

The concise-by-default rules aren't just kind to your attention, they trim Claude's output, so you literally spend fewer tokens. The pun pays for itself.

First in the set: **Attention-kind**.

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

- **48% fewer output tokens.**
- **Answer-first: 50% → 100%.** The default buried the answer under preamble half the time.
- **Skimmability: 3.3 → 4.9** on a 1-5 scale.
- **Unexplained jargon: 2.8 → 1.0 terms per answer.**
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

## Install

**1.** Copy the style you want into your output-styles folder.

Global (every project):

```bash
mkdir -p ~/.claude/output-styles
curl -o ~/.claude/output-styles/attention-kind.md \
  https://raw.githubusercontent.com/USER/attention-span/main/output-styles/attention-kind.md
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

More coming. Each is one readable markdown file, easy to fork and tune.

## Notes

- Styles apply to the **main conversation only**. Subagents run their own prompt.
- These keep Claude's coding behavior intact (`keep-coding-instructions: true`).

## License

MIT. Use it, fork it, make it kinder.
