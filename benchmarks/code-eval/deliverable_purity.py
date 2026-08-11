#!/usr/bin/env python3
"""Deliverable-purity check: when asked to PRODUCE a deliverable, does the style
return only the deliverable, or wrap it in preamble/framing?

This is the clearest before/after signal for the 'deliverable purity' rule. It is
mostly deterministic (wrapper-phrase detection), so it is a cheap, reproducible,
relative metric for comparing style versions, no LLM judge needed.

Usage:
  BENCH_STYLE_FILE=<path> python3 deliverable_purity.py <label>
  (pass label "default" to run the no-style baseline)
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "harness"))
import adapters  # noqa: E402

PROMPTS = [
    "Write a two-sentence Slack message telling the team the deploy is delayed to tomorrow.",
    "Write a git commit message for a change that fixes a null-pointer crash in the login handler.",
    "Write a one-paragraph out-of-office reply for a week-long vacation.",
    "Write a polite email declining a meeting invitation.",
    "Write a PR description for adding rate limiting to the API.",
    "Write a friendly error message to show on a 404 page.",
    "Write a tweet announcing our new dark mode feature.",
    "Write a Slack message asking the team to fill out a survey by Friday.",
]

# Wrapper tells: meta framing around the deliverable, not the deliverable itself.
OPENERS = re.compile(
    r"^\s*(\**)(here'?s|here is|sure|certainly|of course|below is|i'?ve\s+"
    r"(drafted|written|put together|got)|this is|the following|a quick|"
    r"absolutely|happy to|got it|no problem|okay|ok[,!]|alright)",
    re.I,
)
# Only META offers TO THE USER about the deliverable count as wrappers. Phrases
# like a bare "let me know" or "feel free to" can appear inside a legitimate
# deliverable (e.g. an email body), so we require the revision/assistance framing.
CLOSERS = re.compile(
    r"(let me know if you|want me to|happy to (adjust|tweak|revise|change|"
    r"shorten|expand|help)|i can (adjust|tweak|revise|shorten|expand)|"
    r"does this work for you|if you'?d like me to|just say the word|"
    r"hope this helps|feel free to (adjust|tweak|use|customize|edit))",
    re.I,
)
# A preamble sentence that then introduces the real deliverable in a quote/block.
LEAD_IN_TO_BLOCK = re.compile(r"[:.]\s*\n+\s*(>|```|\*\*|\")", re.S)


def purity(text):
    t = text.strip()
    first_line = next((l for l in t.splitlines() if l.strip()), "")
    reasons = []
    if OPENERS.search(first_line):
        reasons.append("opener-wrapper")
    if CLOSERS.search(t):
        reasons.append("closer-offer")
    # preamble line ending in ':' or '.' immediately before a quoted/bolded block
    head = t[:200]
    if LEAD_IN_TO_BLOCK.search(head) and OPENERS.search(first_line):
        reasons.append("lead-in-to-block")
    return (not reasons), reasons


def main():
    label = sys.argv[1] if len(sys.argv) > 1 else "styled"
    style_file = os.environ.get("BENCH_STYLE_FILE")
    body = None
    if label != "default" and style_file:
        lines = open(style_file).read().splitlines()
        b, started = [], False
        for ln in lines:
            if "<!-- body-start -->" in ln:
                started = True
                continue
            if started and not (ln.strip().startswith("<!--") and ln.strip().endswith("-->")):
                b.append(ln)
        body = "\n".join(b).strip()

    clean = 0
    rows = []
    for p in PROMPTS:
        text = adapters.generate(p, style_body=body)
        ok, reasons = purity(text)
        clean += ok
        rows.append({"prompt": p[:40], "pure": ok, "reasons": reasons,
                     "first_line": text.strip().splitlines()[0][:70] if text.strip() else ""})
        print(f"  [{'PURE' if ok else 'WRAP'}] {p[:38]:<40} {','.join(reasons)}",
              file=sys.stderr)
    pct = round(100 * clean / len(PROMPTS))
    print(f"\n{label}: deliverable purity {clean}/{len(PROMPTS)} = {pct}%")
    out = os.path.join(HERE, f"purity-{label}.json")
    json.dump({"label": label, "pure": clean, "n": len(PROMPTS), "pct": pct,
               "rows": rows}, open(out, "w"), indent=2)


if __name__ == "__main__":
    main()
