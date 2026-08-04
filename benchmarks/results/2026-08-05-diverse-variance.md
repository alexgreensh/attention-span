# Attention-kind vs default — diverse eval with variance

**Date:** 2026-08-05
**Method:** 12 questions across 8 categories (dev, knowledge work, research, analysis, explanation, writing, lookup), each answered 4 ways on Opus 4.8 — baseline twice, Attention-kind twice, by independent Claude Code subagents. Two runs per cell so the numbers survive model randomness. Output length measured deterministically (words / 0.75); a separate judge subagent scored answer-first, skimmability, unexplained jargon, and correctness. 60 agents, no API key, ~1.7M tokens.

## Headline (averaged across both runs)

| Metric | Default | Attention-kind |
|---|---|---|
| Output tokens (12 Qs) | 7026 | **3624 (-48%)** |
| Answer-first | 12/24 (50%) | **24/24 (100%)** |
| Skimmability (1-5) | 3.29 | **4.92** |
| Unexplained jargon / answer | 2.79 | **0.96** |
| Correctness | 24/24 | **24/24** |

**Correctness held at 100% across all 48 answers.** Concise cost nothing.

## It holds beyond code

Token cut by category, dev and non-dev alike:

| Category | Default → kind | Cut |
|---|---|---|
| analysis (vendor migration) | 917 → 414 | -55% |
| dev-error (CORS) | 634 → 278 | -56% |
| research (4-day week) | 690 → 327 | -53% |
| dev-review (JWT in localStorage) | 842 → 418 | -50% |
| explain (moat, RAG) | ~660 → ~329 | -50% |
| dev-debug (React renders) | 643 → 342 | -47% |
| knowledge-work (prioritize, standup) | 490 → 278 | -43% |
| dev-decision (Postgres vs Mongo) | 606 → 360 | -41% |
| lookup (affect vs effect) | 308 → 189 | -39% |
| **writing (decline email)** | **84 → 81** | **-4%** |

## The honest exception: short outputs

The decline-a-meeting email barely changed (-4%). That is the style working correctly, not failing: a two-line email is already concise, so there is nothing to trim, and the style did not pad it or mangle it. **The gains scale with verbosity.** The more Claude would have rambled, the more the style saves. On an already-tight answer it gets out of the way.

## Where the default fell down

- **Answer-first was a coin flip for the default (50%).** It opened with preamble or a rhetorical reframe on the prioritization, Docker, and env-var style questions. Attention-kind was answer-first every single time.
- **Jargon nearly tripled in the default** (2.79 vs 0.96 unexplained terms per answer): GIN indexes, ACID, HS256, $lookup, ORM went untagged.
- **Skimmability gap is the felt difference:** 3.29 vs 4.92. The default was often correct but dense; you had to read the paragraphs to find the point.

## Caveats

- **How the style was applied.** Output styles only load into the main Claude Code conversation, not subagents. So the eval injected a condensed version of the style's rules into each styled agent's prompt. That is a faithful proxy for the effect, but it is not the literal output-style file loaded by the harness, and the condensed rules were slightly looser than the full file. Real in-session use should be at least this good, likely tighter.
- Token counts are approximate (words / 0.75), applied identically to every arm, so relative cuts are sound.
- Judge is a single Claude subagent; scores are directional, not calibrated against human raters.
- One model (Opus 4.8). The earlier 2026-08-04 run showed Opus 5 behaves the same, with slightly larger cuts.
