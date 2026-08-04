# Spartan + Rundown — focused eval (Opus 5)

**Date:** 2026-08-05
**Method:** Opus 5 only. Spartan tested on 4 general questions, Rundown on 3 briefing prompts, baseline vs styled, judged by a separate Opus 5 subagent. Style rules injected into the styled agent's prompt (output styles do not apply to subagents). Two judging passes: first with a generic 1-5 skimmability scale, then re-judged with a scale **anchored to an ADHD reader's lived experience** (dense prose caps at 2, no matter how organized; 5 = full gist from bold lead-ins alone).

## Spartan (terse)

| Metric | Default | Spartan |
|---|---|---|
| Output tokens (4 Qs) | 2486 | **1250 (-50%)** |
| Skimmability, anchored (1-5) | 3.25 | **5.00** |
| Answer-first | 4/4 | 4/4 |
| Correctness | 4/4 | 4/4 |

Cuts as hard as Attention-kind while staying correct and answer-first. The anchored baseline still landed at 3-4 on two questions (React, four-day-week) because those default answers genuinely had bold bullets and headers, not pure walls. The dense ones dropped to 2.

## Rundown (TL;DR + emoji)

| Metric | Default | Rundown |
|---|---|---|
| Output tokens (3 Qs) | 852 | **510 (-40%)** |
| Skimmability, anchored (1-5) | 2.33 | **5.00** |
| Answer-first | 3/3 | 3/3 |
| Correctness | 3/3 | 3/3 |

Nails the format. Every default briefing scored 2-3 on the anchored scale (state buried in prose); Rundown hit 5 every time.

## What the anchored re-judge changed

The first pass scored dense baselines ~3.3. An LLM judge reads a wall of text effortlessly, so it under-feels the attention cost a human with ADHD pays. Anchoring the scale (dense prose = max 2) dropped those baselines to 2, matching the lived experience. The gap to the styled versions is therefore **wider** than the first pass showed, not narrower.

## Caveats

- **The Rundown hallucination is not fully proven fixed.** On the website-status prompt the styled answer invented details it was not given (staging up, domain pointed, QA passed). A guard rule ("never invent status") is now in `rundown.md`, but this run predated it, so the fix is untested.
- Single judge; skimmability is a subjective score; word counts are approximate (words / 0.75); the style rules were injected into the prompt rather than loaded as a Claude Code output style (styles do not apply to subagents).
