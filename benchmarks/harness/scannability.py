#!/usr/bin/env python3
"""Scannability: a deterministic readability metric that measures TEXT SHAPE, not
vocabulary. Classic grades (Flesch-Kincaid, Gunning Fog, SMOG, ...) only see word
and sentence length, so a dense wall of plain words scores "easy" on all of them.
That is exactly the failure mode this repo's style fixes. These metrics instead
measure how hard the text is to SCAN, which is the real readability dimension
here. No LLM judge, fully reproducible.

Headline metric (time-to-point): how far you read before you hit the point.
This is what "readable" means for this style, and what classic grades miss.
  words_to_emphasis    words before the first emphasized (bold) anchor. The
                       distance the eye travels before anything lands. LOWER is
                       better. (Full word count if the answer has no bold at all.)
  answer_first_pct     share of answers whose first line is a bold statement,
                       i.e. the point up front, not a warm-up. HIGHER is better.

Shape metrics (how dense the block is):
  longest_wall_words   longest paragraph with no bold and no list/arrow anchor,
                       the longest unbroken run the eye must grind through. LOWER.
  landing_per_100w     scannable anchors per 100 words. HIGHER is better.
  mean_para_words      average paragraph length in words. LOWER is better.
  wall_word_fraction   share of words in anchor-free prose blocks. LOWER is better.
"""

import json
import os
import re
import statistics
import sys

_ANCHOR_LINE = re.compile(r"^\s*(?:[-*→#>]|\d+\s*[.)→])", re.M)
_BOLD = re.compile(r"\*\*.+?\*\*", re.S)
_WORD = re.compile(r"\w+")


def _paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]


def _words(s):
    return len(_WORD.findall(s))


def _has_anchor(paragraph):
    return bool(_ANCHOR_LINE.search(paragraph) or _BOLD.search(paragraph))


def words_to_emphasis(text):
    """Words before the first bold anchor: the distance to the first thing that
    lands. No bold anywhere => the whole answer is undifferentiated, so the score
    is the full word count."""
    m = _BOLD.search(text)
    return _words(text[: m.start()]) if m else _words(text)


def answer_first(text):
    """1 if the first non-empty line is a bold statement (the point up front)."""
    for ln in text.strip().splitlines():
        if ln.strip():
            return 1 if ln.strip().startswith("**") else 0
    return 0


def longest_wall_words(text):
    """Longest paragraph that carries NO anchor (no bold, no list/arrow). The
    biggest block of pure prose the reader must consume with nothing to grab."""
    walls = [_words(p) for p in _paragraphs(text) if not _has_anchor(p)]
    return max(walls, default=0)


def landing_per_100w(text):
    bold = len(_BOLD.findall(text))
    lines = len(_ANCHOR_LINE.findall(text))
    w = _words(text)
    return round(100 * (bold + lines) / w, 2) if w else 0.0


def mean_para_words(text):
    ps = _paragraphs(text)
    return round(sum(_words(p) for p in ps) / len(ps), 1) if ps else 0.0


def wall_word_fraction(text):
    total = _words(text)
    wall = sum(_words(p) for p in _paragraphs(text) if not _has_anchor(p))
    return round(wall / total, 3) if total else 0.0


def metrics(text):
    return {
        "words_to_emphasis": words_to_emphasis(text),
        "answer_first": answer_first(text),
        "longest_wall_words": longest_wall_words(text),
        "landing_per_100w": landing_per_100w(text),
        "mean_para_words": mean_para_words(text),
        "wall_word_fraction": wall_word_fraction(text),
    }


def _agg(vals):
    return {"mean": round(statistics.mean(vals), 1),
            "median": round(statistics.median(vals), 1)}


def main():
    gen = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "results", "raw", "gen2.jsonl")
    gen = sys.argv[1] if len(sys.argv) > 1 else gen
    rows = [json.loads(l) for l in open(gen) if l.strip()]
    out = {}
    keys = ("words_to_emphasis", "answer_first", "longest_wall_words",
            "landing_per_100w", "mean_para_words", "wall_word_fraction")
    for arm in ("default", "styled"):
        per = {k: [] for k in keys}
        for r in rows:
            for g in r[arm]:
                m = metrics(g["text"])
                for k in per:
                    per[k].append(m[k])
        out[arm] = {k: _agg(v) for k, v in per.items()}
        out[arm]["answer_first"] = {
            "pct": round(100 * statistics.mean(per["answer_first"]))}
    print(f"scannability over {len(rows)} questions x 3 gens/arm\n")
    hdr = f"{'metric':<24}{'default':>12}{'styled':>12}   better"
    print(hdr); print("-" * len(hdr))
    print("TIME-TO-POINT (headline):")
    d = out["default"]["words_to_emphasis"]["mean"]; s = out["styled"]["words_to_emphasis"]["mean"]
    print(f"{'  words to the point':<24}{d:>12}{s:>12}   lower")
    print(f"{'  answer in first line':<24}{str(out['default']['answer_first']['pct'])+'%':>12}"
          f"{str(out['styled']['answer_first']['pct'])+'%':>12}   higher")
    print("SHAPE:")
    for k, lab, better in (("longest_wall_words", "  longest wall (words)", "lower"),
                           ("landing_per_100w", "  landing pts /100w", "higher"),
                           ("mean_para_words", "  mean paragraph (words)", "lower"),
                           ("wall_word_fraction", "  wall word fraction", "lower")):
        d = out["default"][k]["mean"]; s = out["styled"][k]["mean"]
        print(f"{lab:<24}{d:>12}{s:>12}   {better}")
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "scannability.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
