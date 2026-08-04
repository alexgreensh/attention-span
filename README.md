# Attention Span

**Pay attention, not tokens.**

![A blissful cat in a whirlwind of scattered paper points a laser at one clean block of text](assets/hero.png)

A small collection of [output styles](https://code.claude.com/docs/en/output-styles) for Claude Code that change how it *talks to you*, not how it codes. Answer-first, plain English, easy to skim. Each one is a single markdown file you drop in and switch on.

The concise-by-default rules aren't just kind to your attention, they trim Claude's output, so you literally spend fewer tokens. The pun pays for itself.

First in the set: **Attention-kind**.

## Attention-kind

An ADHD-friendly style. Claude answers first, keeps it short, drops the jargon, and expands only on what's actually worth your attention. Every point is spaced out and marked with a `→`, and the important words are **bold**, so you can skim just the bold and still get the whole answer.

Same engineering ability underneath. Only the delivery changes.

**Who it's for:** anyone whose attention is a limited resource. ADHD, tired, deep in flow, or just done with walls of text.

### Before / after

Both columns are **actual eval outputs** for the same question, *"How do I set up environment variables in a Node.js project?"* Both were judged correct. The style cut it from 346 words to 168.

| | Default | Attention-kind |
|---|---|---|
| **Opens with** | "Environment variables in Node, from simplest to most robust." (preamble, not the answer) | "**→ Fastest path: a `.env` file plus the built-in `--env-file` flag.**" (the answer) |
| **Length** | 346 words | 168 words |
| **Skim test** | 3 headers, dense prose under each | one bold arrow per point, gist reads from the bold alone |
| **The gotcha** | "everything is a string" buried at the bottom | surfaced as **→ Gotcha: everything in `process.env` is a string** |
| **Ends with** | a trailing rules list | a concrete next action |

The styled answer, as generated:

> **→ Fastest path: a `.env` file plus the built-in `--env-file` flag.** Node 20.6+ reads it natively, no library needed.
>
> **→ On older Node (or if you want zero flags): use `dotenv`.** Install it, load it at the top of your entry file.
>
> **→ Critical: git-ignore your `.env` so secrets never get committed.** The one step people skip and regret.
>
> **→ Gotcha: everything in `process.env` is a string.** `process.env.PORT` is `"3000"`, not `3000`.
>
> Next action: create `.env`, add it to `.gitignore`, run with `node --env-file=.env` on Node 20.6+.

Same information. One of them you can read at a glance.

### Does it actually help? (measured)

Ran 6 real dev questions through default vs Attention-kind, on Opus 4.8 and Opus 5, scored by a separate judge. [Full results.](benchmarks/results/2026-08-04-attention-kind-vs-default.md)

- **~48% fewer output tokens** (43% on Opus 4.8, 52% on Opus 5).
- **Answer-first: 67% → 100%.**
- **Skimmability: 3.7 → 5.0** on a 1-5 scale.
- **Unexplained jargon: ~4 → ~1 term per answer.**
- **Correctness held at 100%.** Shorter cost nothing.

### What changes

- **Answer first.** Conclusion in line one. No wind-up.
- **Short by default.** Says the least that fully answers, then stops.
- **Expands only on what's vital**, so length itself signals importance.
- **Plain English.** Rare technical terms get a five-word definition, once.
- **Built to scan.** `→` markers, heavy bold, real spacing between points.
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

**Cost:** ~470 tokens, added once per session, cached after the first request. The "short by default" rule tends to save more output tokens than that over a conversation.

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
