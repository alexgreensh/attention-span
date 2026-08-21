#!/usr/bin/env python3
"""Non-regression probe for the blocking-question rule.

Feeds NON-blocking prompts through the post-fix spartan style and prints the
answers, so we can check the new rule doesn't (a) invent a spurious wait-on
question, (b) break deliverable-ships-bare, or (c) distort ordinary answers.
None of these prompts contains an irreversible go-ahead, so a correct reply has
NO trailing blocking question.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "harness"))
import adapters  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
STYLE = os.path.join(ROOT, "output-styles", "spartan.md")

PROMPTS = {
    "plain-qa": "What's the difference between TCP and UDP? Two sentences.",
    "deliverable-bare": "Write a one-line git commit message for adding rate "
                        "limiting to the login endpoint.",
    "deliverable-code": "Write a Python function that reverses a singly linked "
                        "list.",
    "advice-no-block": "I'm about to deploy to prod. Give me a short rollback "
                       "plan I can run if it goes bad.",
    "optional-followup": "Explain what a database index is, briefly.",
}


def style_body(path):
    text = open(path).read()
    text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    return text.strip()


def main():
    body = style_body(STYLE)
    for name, prompt in PROMPTS.items():
        ans = adapters.generate(prompt, style_body=body)
        ends_q = ans.rstrip().endswith("?")
        print("=" * 70)
        print(f"{name}   [ends in '?': {ends_q}]")
        print("-" * 70)
        print(ans)
        print()


if __name__ == "__main__":
    main()
