# Work-equivalence + deliverable purity

The objective half of the benchmark: does the output style change the **work**?
No LLM judge, code either passes hidden tests or it does not.

## Work-equivalence

12 coding tasks (`tasks.py`), each a natural request plus a **hidden test** with
edge cases. We generate a solution with the style off and on (hermetically, 3 runs
each), extract the function, and run the test. Pass/fail is ground truth.

```bash
python3 run_code_eval.py selfcheck   # first prove the tests are correct
python3 run_code_eval.py run --reps 3
python3 run_code_eval.py agg
```

`selfcheck` runs every hidden test against a known-correct reference solution
(`reference_solutions.py`), so a broken test can't silently skew a result. Point at
a different style with `BENCH_STYLE_FILE=<path>`; write results elsewhere with
`BENCH_CODE_RESULTS=<path>`.

Result on the shipped v0.5 styles: pass rates are equal to the unstyled arm
(Attention-kind 97%/97%, Spartan 100%/100%, Rundown 97%/92%). Committed runs:
`results.jsonl` (Attention-kind), `results-spartan.jsonl`, `results-rundown.jsonl`.

## Deliverable purity

When you ask a model to *write* something (a Slack message, a commit, an email),
does it hand you just that, or wrap it in "Here's a draft: … let me know if you'd
like changes"? 8 deliverable prompts, mostly deterministic wrapper detection.

```bash
python3 deliverable_purity.py default                                   # no style
BENCH_STYLE_FILE=../../output-styles/attention-kind.md \
  python3 deliverable_purity.py styled
```

Result: 88% clean with the style on, vs 12% with no style.

## Requirements

`claude` CLI (the model under test), `codex` not needed here, Python 3.9+, no pip
installs.
