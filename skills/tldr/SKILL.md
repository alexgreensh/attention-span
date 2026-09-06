---
name: tldr
description: Compress a document, thread, transcript, or pasted text into a scannable TL;DR.
disable-model-invocation: true
---

<!-- attention-span v0.8 · check for updates: https://github.com/alexgreensh/attention-span -->
Compress the content the user pointed you at (a pasted block, a file, a link, a
thread, a transcript, or the current selection) into a briefing they can absorb in
seconds. This is a **transform on someone else's content**, not a style for your own
answers, so summarize what's there, add nothing, invent nothing.

If they didn't say what to compress, ask which one thing, then stop. One question, nothing after it.

## Output shape

1. **TL;DR:** one line that carries the whole thing. A reader who reads only this line
   has the gist and the outcome. If the source has a decision, deadline, or ask, that
   goes here, not below.

2. **Key points**, three to seven, each its own line, bold the subject then a short
   clause. Keep every load-bearing number, name, date, threshold, and condition exactly
   as written, source wording over your paraphrase when it changes the meaning. Drop
   throat-clearing, repetition, and filler.

3. **Action items** only if the source actually contains them: who owns what, by when.
   Skip the heading entirely when there are none, never pad it.

4. Optional **Open questions / unclear:** one line each for anything the source leaves
   genuinely ambiguous. Flag it, don't resolve it by guessing.

## Rules

- **Faithful, not creative.** No new claims, no inferred conclusions, no spin. If the
  source is thin, the TL;DR is thin, say so rather than inflate it.
- **Keep the load-bearing detail.** A risk, caveat, number, or scoped condition survives
  compression, that's the point a reader would act wrong without.
- **Match the length to the source**, not to a template. A short note gets a short TL;DR
  and maybe two points; a long report earns more. Never stretch to fill the shape.
- **Attribute contested or two-sided claims** to whoever made them; don't flatten a
  debate into one voice.
- Plain words. Tag an unavoidable term in five words or fewer. No preamble, no "here's a
  summary", output the briefing itself.
