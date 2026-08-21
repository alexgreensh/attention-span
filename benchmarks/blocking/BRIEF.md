# Grunt task: blocking-question placement test

You are building a small, dependency-free test for GitHub issue #6 of the
attention-span repo: "Blocking questions get buried mid-reply." Repo root is the
`attention-span` project. Work only inside `benchmarks/`. Python 3.9+, stdlib only,
no pip.

## The failure being tested

A question the model MUST wait on (a yes/no before a step with a side effect) gets
buried in paragraph 4 of a longer reply, with non-urgent content after it. The
reader skims, reads it as a status update, misses the ask. The fix (already written
into `output-styles/spartan.md` and `output-styles/attention-kind.md`) says: a
blocking question is the LAST block, nothing after it, and line one flags it when
the reply has other content.

## Deliverables (create these files)

1. `benchmarks/questions/blocking-v1.jsonl` — 6 scenarios, one JSON object per line:
   `{"id": "...", "prompt": "...", "blocking": true, "note": "why this needs a wait-on question"}`.
   Each prompt must be a realistic task where a good agent should ask ONE yes/no
   question before an irreversible/side-effecting step, AND where there is other
   content to report (status, findings, next notes) that could bury the question.
   Vary the domains: a destructive git op, a payment/send, a schema migration, an
   overwrite, an external API call, a bulk delete. Keep prompts 1-3 sentences.

2. `benchmarks/harness/blocking_placement.py` — a deterministic checker. Given a
   model answer (string), compute:
   - `has_question`: contains a line ending in `?`
   - `question_is_last`: the LAST non-empty block/paragraph contains the final `?`
     and there is no substantive prose after that `?` (allow only trailing
     whitespace or a short options list that belongs to the question)
   - `flagged_line_one`: the first non-empty line references the ask (contains `?`,
     or words like "before I", "need", "confirm", "sign off", "go-ahead", "one
     thing")
   - `PASS` = has_question AND question_is_last AND (flagged_line_one OR the whole
     reply is short: < 40 words)
   Expose `score(answer_text) -> dict` and a `__main__` that reads a results jsonl
   (path as argv[1]) and prints a per-scenario table + pass rate. Comment WHY each
   rule exists; keep it readable.

3. Generate answers for contrast. For EACH scenario, produce two answers with YOUR
   OWN generation (you are GLM, prepend the style body as a system-style preface to
   the scenario prompt and answer it):
   - `old`: style body = `shipped/v0.6/spartan.md` (the pre-fix rule set)
   - `new`: style body = `output-styles/spartan.md` (post-fix)
   Strip the YAML frontmatter and the HTML comments from the style body before using
   it. Write to `benchmarks/blocking/results-spartan.jsonl`, one object per line:
   `{"id": ..., "arm": "old"|"new", "answer": "..."}`.

4. Run the checker over that results file and write
   `benchmarks/blocking/SUMMARY.md`: the pass rate for `old` vs `new` arm, and a
   one-line per-scenario verdict. The expected shape of a real fix: `new` passes
   more than `old`. If it does not, say so plainly, do not fudge it.

## Rules

- Stdlib only. No network except your own model calls to generate answers.
- Do NOT edit anything in `output-styles/` or `shipped/` — read-only there.
- Report honestly. A checker that always passes is worthless; make sure `old` can
  actually fail (that is the proof the checker discriminates).
- When done, print the SUMMARY.md contents to stdout so the orchestrator sees them.
