# Real-session quality retrospective — does the style cost work quality?

**Date:** 2026-08-07
**Question:** The token benchmarks show output shrinks and correctness holds on synthetic eval questions. This asks the harder, real-world version: across actual day-to-day work, did turning output styles on change the *quality of the work itself*, not just the shape of the answer?

**Design:** Observational before/after on real Claude Code session history. The split point is the first time a config-level `outputStyle` was set (2026-08-04); everything before is "off", everything from that date is "on". 44 real sessions were sampled across 4 recurring task types, extracted (user ask + reasoning trace + final output), shuffled, stripped of any date or condition label, and scored by independent blind judge subagents. Judges were instructed to score **substance only** (task completion, correctness, completeness, actionability) and explicitly to ignore tone, length, terseness, and formatting, so the visible style could not leak into the score. Each session also got a task-difficulty rating (1-5) as a normalization covariate.

Claude Code only. Devin and Codex sessions were excluded, output styles do not apply to them.

## Headline

**Work quality held; no degradation detected.** On the one task type where task difficulty was identical across both arms (code work), pre and post were a dead heat.

| Metric (composite, 1-5) | Off | On | Δ |
|---|---|---|---|
| Task completion | 4.38 | 4.50 | +0.12 |
| Correctness | 4.46 | 4.55 | +0.09 |
| Completeness | 4.08 | 4.30 | +0.22 |
| Actionability | 4.21 | 4.50 | +0.29 |
| **Composite quality** | **4.28** (n=24) | **4.46** (n=20) | **+0.18** |
| Dropped-something-load-bearing rate | 29% | 15% | -14pt |

The pooled composite difference is **+0.18, 95% CI [-0.34, +0.70]** — not statistically distinguishable from zero.

## The confound, before the numbers

The pooled numbers tilt slightly positive, but **do not credit the style for it.** The "on" sessions came from a 3-day window in which the underlying tasks were simply easier: mean difficulty **2.70 on vs 4.04 off**. Easier work scores higher regardless of style. The apparent lift is the task mix, not the style.

The honest way to read this is per task type, and especially the one type where difficulty matched:

| Task type | Off quality (difficulty) | On quality (difficulty) | Δ | 95% CI |
|---|---|---|---|---|
| **code / dev** | **3.96 (4.2)** | **3.95 (4.2)** | **-0.01** | [-1.58, +1.58] |
| briefing | 4.62 (3.3) | 4.05 (2.8) | -0.58 | [-1.53, +0.38] |
| linkedin | 4.17 (4.7) | 4.85 (2.2) | +0.68 | [-0.03, +1.40] |
| client | 4.38 (4.0) | 5.00 (1.6) | +0.62 | [+0.16, +1.09] |

**Code work is the clean comparison:** difficulty 4.2 on both sides, quality 3.96 vs 3.95. On the hardest recurring work, with difficulty held constant, the style changed nothing measurable. The linkedin and client positives are confounded (difficulty dropped by half), so they are not evidence the style *helps* — if anything they show the confound is real.

## Limitations, stated plainly

- **Observational, not causal.** Which sessions got a style was not randomized. It shows no drop; it does not prove exact equivalence.
- **Underpowered.** n=44, cells of 5-6, wide within-type variance (code sessions ranged 2.0-5.0 within a single arm). Confidence intervals are broad.
- **Short "on" window.** 3 days, all Opus 4.8. The "off" arm was restricted to Opus 4.8 sessions to hold the model constant, but the eras still differ in task mix.
- **Reasoning was not measurable.** Extended thinking was on in only 11 of 44 sessions, and just 2 in the "on" arm. No claim about reasoning-trace quality can be made from this data.

## What this licenses you to say

> In a blind, observational review of 44 real historical sessions across 4 task types, turning output styles on showed no statistically significant drop in task quality and no sign of degradation; on difficulty-matched code work the two were indistinguishable.

It rules out a large, obvious quality cost in real use. It is evidence for "style-only", not proof of it. Proof needs a controlled A/B: same prompt, same model, thinking on, style as the single toggled variable, enough repetitions to power an equivalence margin.
