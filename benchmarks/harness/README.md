# Benchmark harness

Reproducible, dependency-free tools for measuring what an output style does. Clone
the repo, have the CLIs below on your PATH, and run it. Everything is written to
disk so you can check the numbers instead of trusting a table. Full writeup:
[`../results/2026-08-11-benchmark-rebuild.md`](../results/2026-08-11-benchmark-rebuild.md).

## The idea

Measure the **work** and the **output** separately, and don't ask an LLM "is this
better?" (that question is what made the old benchmark circular, see
[#4](https://github.com/alexgreensh/attention-span/issues/4)).

- **Work** must be unchanged: judged by hidden tests, pass/fail, no opinion.
- **Output** should be shorter and easier to reach the point in: measured from the
  shape of the text, not an LLM's judgment of it.

## What's here

- `adapters.py` — hermetic answer generation (style off vs on, single variable, no
  CLAUDE.md / hooks / MCP / tools, so nothing leaks and runs reproduce).
- `scannability.py` — deterministic readability from text shape. Headline metric is
  **time-to-point**: how many words you read before the first emphasized point, and
  how often the answer is in the first line. Classic reading grades (Flesch-Kincaid
  etc.) only see word length and are blind to a wall of text; this is not.
- `../code-eval/` — the **work-equivalence** benchmark (coding tasks with hidden
  tests) and the **deliverable-purity** check. See its own README.

## Run it

```bash
# readability shape (time-to-point, walls, landing points), default vs styled
python3 scannability.py                 # reads ../results/raw/gen2.jsonl

# work-equivalence + deliverable purity live next door
cd ../code-eval && cat README.md
```

## Requirements

- `claude` — the [Claude Code CLI](https://code.claude.com), logged in. The model
  under test.
- Python 3.9+. No pip installs.

`../results/raw/gen2.jsonl` is a committed set of hermetic answers (24 held-out
questions, 3 generations per arm) so `scannability.py` runs out of the box. Swap in
your own answers file as the first argument to regenerate the numbers.
