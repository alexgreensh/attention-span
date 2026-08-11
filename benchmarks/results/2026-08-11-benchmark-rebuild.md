# The benchmark, rebuilt: honest and reproducible

**Date:** 2026-08-11

Issue [#4](https://github.com/alexgreensh/attention-span/issues/4) made a fair point: the
earlier benchmarks measured **compliance** (did the output follow the style's own rules,
scored by a Claude judge against a rubric lifted from those same rules) rather than
**quality**. A style scoring well on its own formatting rules proves the style is followed,
not that anything is better.

So we rebuilt it. The new benchmark measures only claims we can defend, most of them with **no
LLM judge at all**, and the whole thing is reproducible from this repo. Here is what it shows.

## The one principle

**Separate the work from the output, and measure only what we claim.**

- **The work** (the code it writes, the task it does) must be unchanged. The styles are built
  that way (`keep-coding-instructions: true`). We test it objectively.
- **The output** (how it talks to you) should be shorter and easier to read, without losing
  what a human needs. We measure the shape of the text, not an LLM's opinion of it.

Nothing here asks a language model "is this better?" That question is what went wrong before.

## Results

All figures use a single-variable A/B: the same model (`claude-opus-4-8`), hermetically, with
the ambient style forced off; the styled arm adds only the style file. Full method and raw
data under [`../harness`](../harness/) and [`code-eval`](../code-eval/).

### 1. The work is untouched (objective, no judge)

12 coding tasks, each with a **hidden test suite**. We generate a solution with the style off
and on (3 runs each), extract the code, and run the tests. Pass or fail is ground truth.

| Attention-kind | Passes hidden tests |
|---|---|
| Style off | 35/36 (97%) |
| **Style on** | **35/36 (97%)** |

Identical. Both arms miss the same one flaky task on a single run out of three; the difference
is zero, well within run-to-run noise. Spartan and Rundown clear the same gate (100%/100% and
97%/92%, styled matching or beating the unstyled arm). This is the causal, controlled version
of an earlier [observational finding](2026-08-07-real-session-quality-retrospective.md): a
blind review of 44 real work sessions that also showed no quality drop, a dead heat on
difficulty-matched code. (As a side effect the styled code ran ~40% shorter, fewer comments,
same behavior.)

### 2. The output is ~43% shorter (and much more on verbose answers)

Across 24 held-out questions, styled answers are **~43% fewer characters** on average (median
41%) than the unstyled default. The range is the real story: **verbose answers cut 50-71%**
(explanations, lookups, anything the default would ramble on), while already-short answers
barely move, a two-line message shrank only 7%. The savings scale with how much the default
would have over-explained; on tight answers the style gets out of the way.

### 3. You reach the point in 6 words instead of 40 (readability, measured)

We do **not** use a reading-grade score (Flesch-Kincaid and its cousins only measure word and
sentence length; a dense wall of plain words scores "easy" on all of them). We measure the
thing that actually makes text skimmable: **how far you read before you hit the point.**

| | Style off | Style on |
|---|---|---|
| Words before the first emphasized point | ~40 | **~6** |
| Answer stated in the first line | 3% | **75%** |
| Longest unbroken block (words) | 37 | **15** |

The unstyled model isn't unformatted, it uses headers and bold too. Its problem is that it
*warms up*: you read a framing paragraph before the answer. The style front-loads it. That is
the readability win, and it is the style's headline promise ("answer first"), measured.

### 4. Deliverables come out clean

Ask a model to *write* something (a Slack message, a commit message, an email) and it often
wraps it in "Here's a draft: … let me know if you'd like changes." You delete the wrapper
before pasting. Over 8 such tasks:

| | Deliverable returned clean |
|---|---|
| No style | 12% |
| Attention-kind (previous) | 50% |
| **Attention-kind (this release)** | **88%** |

This one improved because we tuned the style and re-ran the benchmark, which is the point of
having one.

## What we retired

The earlier "answer-first 63→96, skimmability 2.7→4.8, jargon 2.0→0.9" figures are **kept but
relabeled as compliance**: they measure whether the style is followed, scored by a Claude
judge against the style's own rules. Useful to know a style takes effect; not evidence it is
better. We no longer present them as quality, and we do not claim the style produces "better
answers", a blind cross-model preference test does not support that, and we would rather say so
than dress it up.

## Reproduce it yourself

```bash
# work-equivalence (no judge): does the style change the code?
cd benchmarks/code-eval && python3 run_code_eval.py selfcheck   # validate the tests
python3 run_code_eval.py run --reps 3 && python3 run_code_eval.py agg

# readability shape: time-to-point, walls, landing points
cd ../harness && python3 scannability.py

# deliverable purity
cd ../code-eval && BENCH_STYLE_FILE=../../output-styles/attention-kind.md \
  python3 deliverable_purity.py styled
```

Every answer and every test result is written to disk. Swap the model or the style file and
rerun; nothing here is hand-scored.

## Honest limits

- **Work-equivalence is shown on verifiable coding tasks**, the class with hidden tests. It
  does not speak to open-ended design work, which has no ground-truth test.
- **Small n** (12 coding tasks, 24 questions, 8 deliverables). The effects reported are large
  and consistent; subtle ones would need more runs.
- **We deliberately did not run a human comprehension study.** The strongest evidence that the
  style helps understanding is daily use, which we don't put a number on.
