#!/usr/bin/env python3
"""Generate user-invoked skill files from the output-style sources.

Each skill is self-contained (works in Claude.ai chat, not just Claude Code) and
user-invoked only (`disable-model-invocation: true`) so it costs zero passive
context. The body is taken verbatim from output-styles/<slug>.md so the skill can
never drift from the flagship wording — regenerate after editing a style.

Run from the repo root:  python3 scripts/gen-skills.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION = (ROOT / "VERSION").read_text().strip()

# slug -> (skill name, one-line description stub shown in the picker)
STYLES = {
    "attention-kind": ("attention-kind", "Answer in the ADHD-friendly Attention-kind style for the rest of this chat."),
    "spartan": ("spartan", "Answer in the terse, zero-warmth Spartan style for the rest of this chat."),
    "rundown": ("rundown", "Answer in the Rundown briefing style (TL;DR + checklist + numbered choices)."),
}

# The style files justify the arrow-paragraph format by a terminal quirk. Skills
# also run in rich-markdown chat, so make the rationale surface-agnostic.
TERMINAL_PATCHES = [
    ("Terminal markdown collapses tight lists, so use paragraphs, not `-` bullets.",
     "Tight `-` bullets collapse in some terminals, so use blank-line-separated paragraphs, not bullets."),
    ("Not `-` bullets; terminals collapse them.",
     "Not `-` bullets; they collapse in some terminals."),
]

MARKER = f"<!-- attention-span v{VERSION} · check for updates: https://github.com/alexgreensh/attention-span -->"


def body_of(style_path: Path) -> str:
    text = style_path.read_text()
    # drop YAML frontmatter
    text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
    # drop the body-start + version-marker comment lines
    lines = [ln for ln in text.splitlines() if not ln.startswith("<!--")]
    body = "\n".join(lines).strip()
    for old, new in TERMINAL_PATCHES:
        body = body.replace(old, new)
    return body


def main() -> int:
    for slug, (name, desc) in STYLES.items():
        src = ROOT / "output-styles" / f"{slug}.md"
        if not src.exists():
            print(f"missing {src}", file=sys.stderr)
            return 1
        body = body_of(src)
        out_dir = ROOT / "skills" / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        skill = (
            "---\n"
            f"name: {name}\n"
            f"description: {desc}\n"
            "disable-model-invocation: true\n"
            "---\n\n"
            f"{MARKER}\n"
            f"Adopt this style for the rest of the conversation, starting with your next reply. "
            f"It changes how you *talk*, not how you code or what you can do.\n\n"
            f"{body}\n"
        )
        (out_dir / "SKILL.md").write_text(skill)
        print(f"wrote skills/{slug}/SKILL.md ({len(skill)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
