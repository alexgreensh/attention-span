# Benchmark: what the styles do

**Date:** 2026-08-11

The benchmark measures two things separately, most of them with **no LLM judge at all**, and
every figure is reproducible from this repo.

- **The work** (the code the model writes, the task it does) should be unchanged. The styles
  are built that way (`keep-coding-instructions: true`). We test it with hidden tests, pass or
  fail, no opinion.
- **The output** (how it talks to you) should be shorter and easier to read, without losing
  what a human needs. We measure the shape of the text, not a model's opinion of it.

All figures use a single-variable A/B: the same model (`claude-opus-4-8`), hermetically, with
the ambient style off; the styled arm adds only the style file. Method and raw data under
[`../harness`](../harness/) and [`../code-eval`](../code-eval/).

## 1. The work is unchanged (objective, no judge)

12 coding tasks, each with a **hidden test suite**. We generate a solution with the style off
and on (3 runs each), extract the code, and run the tests. Pass or fail is ground truth.

| Attention-kind | Passes hidden tests |
|---|---|
| Style off | 35/36 (97%) |
| **Style on** | **35/36 (97%)** |

Identical. Both arms miss the same one flaky task on a single run out of three; the difference
is zero, well within run-to-run noise. Spartan and Rundown clear the same gate (100%/100% and
97%/92%, styled matching or beating the unstyled arm). No judge, just tests passing. (As a
side effect the styled code runs ~40% shorter, fewer comments, same behavior.)

## 2. The output is ~43% shorter (and much more on verbose answers)

Across 24 questions, styled answers are **~43% fewer characters** on average (median 41%). The
range is the real story: **verbose answers cut 50-71%** (explanations, lookups, anything the
model would ramble on), while already-short answers barely move, a two-line message shrank only
7%. The savings scale with how much the answer would otherwise over-explain; on tight answers
the style gets out of the way.

## 3. You reach the point in 6 words instead of 40

We do **not** use a reading-grade score (Flesch-Kincaid and its cousins only measure word and
sentence length; a dense wall of plain words scores "easy" on all of them). We measure the
thing that makes text skimmable: **how far you read before you hit the point.**

| | Style off | Style on |
|---|---|---|
| Words before the first emphasized point | ~40 | **~6** |
| Answer stated in the first line | 3% | **75%** |
| Longest unbroken block (words) | 37 | **15** |

Plain Claude isn't unformatted, it uses headers and bold too. Its habit is to *warm up*: you
read a framing paragraph before the answer. The style front-loads it. That is the readability
win, and it is the style's headline promise ("answer first"), measured.

## 4. Deliverables come out clean

Ask a model to *write* something (a Slack message, a commit message, an email) and it often
wraps it in "Here's a draft: … let me know if you'd like changes." You delete the wrapper
before pasting. Over 8 such tasks: **88% come out clean with the style on, vs 12% with no
style.**

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

## Limits

- **Work-equivalence is shown on verifiable coding tasks**, the class with hidden tests. It
  does not speak to open-ended design work, which has no ground-truth test.
- **Small n** (12 coding tasks, 24 questions, 8 deliverables). The effects reported are large
  and consistent; subtle ones would need more runs.
- The readability metrics are proxies for how a human reads, chosen because they measure text
  shape deterministically. They are not a substitute for a human comprehension study.
