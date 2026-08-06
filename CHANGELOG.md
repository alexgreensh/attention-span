# Changelog

Versioning: single rightmost number bumps (0.2 → 0.3 → 0.4 …).

## 0.3

- **Use with other agents.** The style body is provider-agnostic; only Claude Code's YAML
  frontmatter is Claude-specific. New README section with one-line installs for Devin, Codex,
  and Antigravity CLI (agy), stripping the frontmatter at a `<!-- body-start -->` marker. No
  duplication, no drift. (PR #1, danikdanik)
- **Version marker in every style file.** Each style now carries a `<!-- attention-span vX.Y -->`
  line so you can tell whether your downloaded copy is current: `grep attention-span
  ~/.claude/output-styles/*.md`, then compare to the version badge.
- **README badges** (version, license, styles, token savings) and a `release.yml` workflow that
  fails the release if VERSION, the in-file markers, and the tag ever drift.
- **Spanish README** (`README.es-ES.md`), with a language switcher on both. (PR #2, webbrain-one)

## 0.2

- **Attention-kind + Spartan: answer vs deliverable split.** An *answer* (explaining, deciding,
  advising, reporting) says its point and stops; a *deliverable* (doc, plan, spec, reconstruction,
  code) runs as long as the work needs. Ambiguous defaults to "answer, keep it lean."
- **Tightened the expansion bar.** "Expand only what's vital" now requires that cutting the
  expansion would cost the reader, not merely that it's relevant.
- Both styles state explicitly that brevity trims the reply, never the internal reasoning. No word
  ceiling by design (a hard cap makes the model optimize for the number over the answer).
