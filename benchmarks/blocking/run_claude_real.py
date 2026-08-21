#!/usr/bin/env python3
"""Real on-target validation for issue #6.

Generate answers from the ACTUAL model under test (Claude via adapters.py),
cold, with the post-fix spartan style appended, over the blocking scenarios.
Then the caller scores them with blocking_placement.py. Unlike the GLM contrast
run, nothing here is authored to make the point: the model answers the scenario
on its own and we see whether it naturally lands the blocking question last.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "harness"))
import adapters  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SCENARIOS = os.path.join(ROOT, "benchmarks", "questions", "blocking-v1.jsonl")
STYLE = os.path.join(ROOT, "output-styles", "spartan.md")
OUT = os.path.join(ROOT, "benchmarks", "blocking", "results-claude-real.jsonl")


def style_body(path):
    """Strip YAML frontmatter and HTML comments, same as gen_answers.py."""
    text = open(path).read()
    text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    return text.strip()


def main():
    body = style_body(STYLE)
    rows = [json.loads(l) for l in open(SCENARIOS) if l.strip()]
    with open(OUT, "w") as f:
        for r in rows:
            ans = adapters.generate(r["prompt"], style_body=body)
            f.write(json.dumps({"id": r["id"], "arm": "claude-new", "answer": ans}) + "\n")
            print(f"[gen] {r['id']}  ({len(ans.split())} words)")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
