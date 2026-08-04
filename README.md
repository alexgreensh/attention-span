# Kind output styles for Claude Code

A small collection of [output styles](https://code.claude.com/docs/en/output-styles) that change how Claude Code *talks to you*, not how it codes. Each one is a single markdown file you drop in and switch on.

First in the set: **Attention-kind**.

## Attention-kind

An ADHD-friendly style. Claude answers first, keeps it short, drops the jargon, and expands only on what's actually worth your attention. Every point is spaced out and marked with a `→`, and the important words are **bold**, so you can skim just the bold and still get the whole answer.

Same engineering ability underneath. Only the delivery changes.

**Who it's for:** anyone whose attention is a limited resource. ADHD, tired, deep in flow, or just done with walls of text.

### Before / after

Same question, same answer. **"My Node app is leaking memory in production. Where do I start?"**

**Default Claude Code:**

> There are several potential causes for memory leaks in a Node.js application, and diagnosing them typically involves a systematic approach. First, it's worth understanding that memory leaks often stem from unintentionally retained references, such as global variables, closures that capture large objects, event listeners that are never removed, or growing caches that lack an eviction policy. To investigate, you'll want to start by taking heap snapshots using the Chrome DevTools inspector, which you can attach to your running process with the `--inspect` flag. By capturing multiple snapshots over time and comparing them, you can identify which objects are accumulating...

**Attention-kind:**

> **Start by confirming it's a real leak, then snapshot the heap to find what's piling up.**
>
> **→ Confirm it's real.** Log memory every minute. A **true leak climbs and never comes back down**. Sawtooth up-and-down is just normal cleanup.
>
> **→ Snapshot the heap.** Run with `node --inspect`, take **two snapshots** a few minutes apart, compare. Whatever **grew between them** is your suspect.
>
> **→ Check the usual culprits.** Listeners never removed, a cache with **no size limit**, timers holding old data.
>
> **The one that bites most people:** listeners added per-request and never removed. **Look there first.**

Same information. One of them you can read at a glance.

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
  https://raw.githubusercontent.com/USER/kind-output-styles/main/output-styles/attention-kind.md
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
