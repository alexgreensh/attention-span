# Laconic + Status — focused eval (Opus 5)

**Date:** 2026-08-05
**Method:** Opus 5 only. Laconic tested on 4 general questions, Status on 3 briefing-shaped prompts, baseline vs styled, judged by a separate Opus 5 subagent. 21 agents, ~592k tokens. Style rules injected into the styled agent's prompt (output styles do not apply to subagents).

## Laconic (Spartan)

| Metric | Default | Laconic |
|---|---|---|
| Output tokens (4 Qs) | 2511 | **1201 (-52%)** |
| Skimmability (1-5) | 3.50 | **5.00** |
| Answer-first | 4/4 | 4/4 |
| Correctness | 4/4 | 4/4 |

**Verdict: strong.** Cuts harder than Attention-kind (-52% vs -48%) while staying correct and answer-first. On the React question it went 923 → 373 tokens (-60%) with every technical claim intact. This is the heads-down power-user style working as intended.

## Status (TL;DR + emoji)

| Metric | Default | Status |
|---|---|---|
| Output tokens (3 Qs) | 751 | **597 (-21%)** |
| Skimmability (1-5) | 3.33 | **5.00** |
| Answer-first | 3/3 | 3/3 |
| Correctness | 3/3 | 3/3 |

**Verdict: nails the format, two honest caveats.**

- **It hallucinated on one prompt.** Asked for a website-launch status, the styled answer invented specifics that were never given (deploy pipeline, staging, domain wired). The checklist format tempts the model to fill rows it has no data for. **Fix applied:** added a rule to the style, "Never invent status; report only what you were given; unknown state is ⬜ or 'unknown.'"
- **It can run longer on already-short input.** The standup prompt went 167 → 207 tokens (+24%), because adding TL;DR + checklist + emoji scaffolding to a tiny brief costs more than it saves. Status is a format for clarity, not a compression play; token savings are a side effect, not the point.

## Takeaways

- Laconic is a clean win on the same axis as Attention-kind: fewer tokens, more skimmable, still correct.
- Status trades tokens for scannability and structure. Use it for briefings, not to shrink output. Watch the hallucination tendency; the new guard rule should curb it (not yet re-measured).
- Same caveat as prior runs: token counts approximate (words / 0.75), single judge, rules injected rather than harness-loaded.
