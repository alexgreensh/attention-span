# Attention-kind

An ADHD-friendly **output style** for [Claude Code](https://code.claude.com/docs/en/output-styles). It changes how Claude *talks to you*, not how it codes.

Claude answers first, keeps it short by default, uses plain English, and expands only on what's actually worth your attention. Every point is spaced out and marked with a `→` so your eyes never have to dig for the answer.

You can skim just the **bold** and still get the whole thing.

## Who it's for

Anyone whose attention is a limited resource: ADHD, tired, deep in flow, or just done with walls of text. It keeps Claude's full engineering ability intact and only reshapes the delivery.

## What it does

- **Answer first.** The conclusion or fix lands in line one. No wind-up.
- **Short by default.** Says the least that fully answers, then stops.
- **Expands only what's vital.** Length becomes a signal that something actually matters.
- **Plain English, no jargon.** Rare technical terms get a five-word definition, once.
- **Built to scan.** `→` markers, heavy bold, real blank lines between every point.
- **Keeps the engineer.** Claude still scopes, verifies, and codes the same way.

## Install

**1.** Copy the style into your Claude Code output-styles folder.

For every project (global):

```bash
mkdir -p ~/.claude/output-styles
curl -o ~/.claude/output-styles/attention-kind.md \
  https://raw.githubusercontent.com/USER/attention-kind/main/output-styles/attention-kind.md
```

Or for a single project, drop the file in `.claude/output-styles/` inside that repo.

**2.** Turn it on. Run `/config`, pick **Attention-kind** under *Output style*.

> The old `/output-style` command was removed in v2.1.91. Use `/config`, or set it directly (next step).

**3.** To make it the permanent default without the menu, add one line to `~/.claude/settings.json`:

```json
{
  "outputStyle": "Attention-kind"
}
```

**4.** Restart Claude Code or run `/clear`. The style loads once at session start, so it takes effect on the next session.

## Cost

About **470 tokens**, added to the system prompt **once per session**, not per message. Prompt caching covers it after the first request. It's a rounding error, and the "short by default" rule tends to *save* output tokens over a conversation.

## Customize it

The whole thing is one readable markdown file: [`output-styles/attention-kind.md`](output-styles/attention-kind.md). Tune the tone, swap the `→` marker, loosen the bold. It's yours.

Two design choices worth knowing:

- **Each point is its own paragraph**, not a markdown list. Terminal renderers squeeze tight list items together, so paragraphs are the only way to guarantee real spacing.
- **Chat formatting stays out of your code.** Comments inherit the plain-English "explain the why" rule, but never the arrows or bold.

## Notes

- Applies to the **main conversation only**. Subagents run their own prompt, so they won't inherit it.
- `keep-coding-instructions: true` is set, so Claude's software-engineering behavior is untouched.

## License

MIT. Use it, fork it, make it kinder.
