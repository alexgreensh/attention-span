#!/usr/bin/env python3
"""Blocking-question placement checker.

Tests the fix for attention-span issue #6: "Blocking questions get buried
mid-reply." A blocking question is a yes/no the agent MUST wait on before an
irreversible / side-effecting step. The fix (output-styles/spartan.md) says:
the blocking question is the LAST block, nothing after it, and line one flags
it when the reply has other content.

This checker is deterministic, stdlib-only, and intentionally strict enough
that a reply which buries the question mid-paragraph (the pre-fix failure
mode) can actually FAIL. A checker that always passes is worthless; the
discrimination proof is that the `old` arm fails more than `new`.

Rules and why each exists
-------------------------
has_question
    The reply must actually ask something. A blocking ask that the agent
    silently skips (just does the irreversible step) is the worst failure,
    so we surface it as its own signal rather than folding it into PASS.

question_is_last
    The final `?` in the reply must sit in the last non-empty paragraph, with
    no substantive prose after it. This is the core of issue #6: a question
    buried in paragraph 1 with three paragraphs of status after it gets skimmed
    past. We allow a short yes/no options list after the `?` because that list
    belongs to the question (it is the question's affordance, not new prose).

flagged_line_one
    When the reply carries other content (findings, status, next notes), the
    first non-empty line must reference the ask, so a skimmer who reads only
    line one knows there is something to answer. Allowed signals: a `?` on
    line one, or flag words ("before I", "need", "confirm", "sign off",
    "go-ahead", "one thing"). Without this, a long reply can put the question
    last yet still hide it behind a wall of status.

PASS = has_question AND question_is_last AND (flagged_line_one OR short_reply)
    A short reply (< 40 words) has no room to bury anything, so we waive the
    line-one flag for it. A long reply must both end on the question and flag
    it up front. Both conditions are required because either alone still lets
    the question get lost: last-but-unflagged gets skipped by skimmers;
    flagged-but-not-last gets buried under the trailing status.
"""

import json
import re
import sys

# A "word" for the short-reply escape and options-list word cap.
_WORD = re.compile(r"\w+")

# Flag words that indicate line one is pointing at the ask. Kept tight: these
# are the brief's list plus the close synonyms that unambiguously reference a
# pending decision. Generic verbs like "send" or "run" are deliberately
# excluded, they describe the action, not the wait.
_FLAG_WORDS = re.compile(
    r"\b(before I|need|confirm|sign[- ]?off|go[- ]?ahead|one thing|"
    r"should I|want me|wait|hold off|your call)\b",
    re.IGNORECASE,
)

# A decisive verdict opener also satisfies line-one intent: when the agent
# DECIDES not to proceed, "No —", "Don't", "Stop", "Hold", "I can't" on line one
# is the actionable signal a skimmer needs (the reader learns the state at a
# glance), which is what the flag exists to guarantee. Matched only at the start
# of line one so a "no" buried mid-sentence doesn't count.
_VERDICT_OPENER = re.compile(
    r"^\**\s*(?:→\s*)?\**\s*"
    r"(no\b|don'?t\b|do not\b|stop\b|hold\b|wait\b|i can'?t\b|cannot\b|"
    r"not (?:as-is|yet|until))",
    re.IGNORECASE,
)

# Imperative blocking asks: a real go-ahead is often phrased as a command, not
# a literal question — "Confirm before I proceed", "Paste it and I'll do it",
# "Say no if you want it gone", "Answer those three and I'll...". These are asks
# the reader must respond to before the agent acts, so they count as the ask
# even without a trailing `?`. Kept tight to a pending-decision shape so ordinary
# imperatives ("Run the delete") don't trip it.
_IMPERATIVE_ASK = re.compile(
    r"\b(confirm|approve|paste|tell me|let me know|say (?:yes|no)|answer)\b"
    r"[^.?!]*\b(before I|and I'?ll|then I'?ll|first|if you)\b",
    re.IGNORECASE,
)

# Trailing markdown decoration that may follow a `?` on the same line
# (closing bold `**`, italics `_`, inline-code backticks). The `?` is the
# real sentence end; the decoration is just emphasis. Strip it before
# deciding whether a line "ends in ?" or whether prose follows the `?`.
_TRAIL_DECOR = re.compile(r"[\s*_`]+$")


def _strip_trail(s):
    """Strip trailing whitespace and markdown emphasis/code decoration."""
    s = s.rstrip()
    while True:
        new = _TRAIL_DECOR.sub("", s)
        if new == s:
            return s
        s = new


# An options list belonging to the question: short, each line a yes/no-style
# affordance. This is the only thing allowed after the final `?`.
_OPT_LINE = re.compile(
    r"^\s*(?:[-*]\s+|\d+[.)]\s+)?"
    r"(?:yes|no|y|n|maybe|ok|okay|cancel|abort|go|stop|proceed|skip|"
    r"hold|wait|yep|nope|y/n)\b",
    re.IGNORECASE,
)


def _words(s):
    return len(_WORD.findall(s))


def _paragraphs(text):
    """Blank-line-separated blocks, stripped, empties dropped."""
    return [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]


def _first_nonempty_line(text):
    for ln in text.strip().splitlines():
        if ln.strip():
            return ln.strip()
    return ""


def _is_options_list(para):
    """A short block of yes/no-style affordance lines. Belongs to the
    question, so it does not count as 'substantive prose after the ?'."""
    if _words(para) > 15:
        return False
    lines = [ln.strip() for ln in para.splitlines() if ln.strip()]
    if not lines:
        return False
    return all(_OPT_LINE.match(ln) for ln in lines)


def _para_has_ask(p):
    """A paragraph counts as an ask if a line ends in `?` or it contains an
    imperative blocking ask ("confirm ... before I", "paste ... and I'll")."""
    for ln in p.splitlines():
        if _strip_trail(ln).endswith("?"):
            return True
    return bool(_IMPERATIVE_ASK.search(p))


def has_question(text):
    """True if the reply contains an ask: a line ending in `?` (ignoring
    trailing whitespace/markdown emphasis), OR an imperative go-ahead the reader
    must answer. A `?` mid-sentence inside prose does not count; the question has
    to land as a line-ending so it reads as an ask, not a parenthetical."""
    return any(_para_has_ask(p) for p in _paragraphs(text))


def question_is_last(text):
    """The last ask (a `?`-line or an imperative go-ahead) sits in the last
    non-empty paragraph, with nothing substantive after it. A short yes/no
    options list after it is allowed because it belongs to the ask."""
    paras = _paragraphs(text)
    if not paras:
        return False
    # Locate the last paragraph that contains an ask (question or imperative).
    last_q_para = -1
    for i, p in enumerate(paras):
        if _para_has_ask(p):
            last_q_para = i
    if last_q_para == -1:
        return False
    # Anything after the ask paragraph must be options-list only.
    for p in paras[last_q_para + 1:]:
        if not _is_options_list(p):
            return False
    # If the ask is a literal `?`, the ask paragraph must end on it (or an
    # options list inside the same block). An imperative ask is checked at the
    # paragraph level only, since it has no single terminal marker.
    qp = paras[last_q_para]
    if "?" not in qp:
        return True
    qpos = qp.rfind("?")
    tail = _strip_trail(qp[qpos + 1:])
    if not tail:
        return True
    # Tail inside the same paragraph: allow only options-list lines.
    return _is_options_list(tail)


def flagged_line_one(text):
    """Line one references the ask: a `?` on line one, or a flag word."""
    first = _first_nonempty_line(text)
    if not first:
        return False
    if first.rstrip().endswith("?") or "?" in first:
        return True
    if _VERDICT_OPENER.match(first):
        return True
    return bool(_FLAG_WORDS.search(first))


def is_short_reply(text):
    """< 40 words. A short reply has no room to bury a question, so the
    line-one flag is waived for it."""
    return _words(text) < 40


def score(answer_text):
    """Score one reply. Returns a dict of all signals plus PASS."""
    hq = has_question(answer_text)
    ql = question_is_last(answer_text)
    fl = flagged_line_one(answer_text)
    short = is_short_reply(answer_text)
    passed = hq and ql and (fl or short)
    return {
        "has_question": hq,
        "question_is_last": ql,
        "flagged_line_one": fl,
        "short_reply": short,
        "word_count": _words(answer_text),
        "PASS": passed,
    }


def main():
    if len(sys.argv) < 2:
        print("usage: blocking_placement.py <results.jsonl>", file=sys.stderr)
        sys.exit(2)
    path = sys.argv[1]
    rows = [json.loads(l) for l in open(path) if l.strip()]

    by_arm = {}
    print(f"blocking placement over {len(rows)} rows\n")
    hdr = f"{'id':<26}{'arm':<6}{'Q?':<5}{'last':<6}{'flag':<6}{'wc':>5}  verdict"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        s = score(r["answer"])
        rid = r.get("id", "?")
        arm = r.get("arm", "?")
        by_arm.setdefault(arm, []).append(s["PASS"])
        verdict = "PASS" if s["PASS"] else "FAIL"
        print(f"{rid:<26}{arm:<6}"
              f"{'Y' if s['has_question'] else 'N':<5}"
              f"{'Y' if s['question_is_last'] else 'N':<6}"
              f"{'Y' if s['flagged_line_one'] else 'N':<6}"
              f"{s['word_count']:>5}  {verdict}")
    print()
    print("pass rate by arm:")
    for arm, vals in sorted(by_arm.items()):
        rate = round(100 * sum(vals) / len(vals), 1)
        print(f"  {arm:<6} {sum(vals)}/{len(vals)}  ({rate}%)")


if __name__ == "__main__":
    main()
