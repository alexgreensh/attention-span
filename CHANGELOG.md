# Changelog

Versioning: single rightmost number bumps (0.2 → 0.3 → 0.4 …).

## 0.5

- **Sharper styles.** All three styles get four rules tuned from real-session history:
  deliverable purity (produce a message/email/commit and you get just that, no "here's a
  draft" wrapper), never trim a warning when compressing, keep every essential point (brevity
  is shorter points, not fewer), and the bold/TL;DR alone must carry the whole answer.
- **Benchmark rebuilt, honest and reproducible.** In response to
  [#4](https://github.com/alexgreensh/attention-span/issues/4): the old benchmark measured
  compliance (style followed) with a Claude judge against the style's own rules. The new one
  measures only defensible claims, most with no LLM judge. Work is unchanged (hidden-test
  coding A/B, styled 100% vs default 97%), output ~40% shorter, and you reach the point in ~6
  words vs ~40 (answer in the first line 75% vs 3%). Deliverable purity 50% → 88%. Full
  writeup and runnable harness under `benchmarks/`.

## 0.4

- **`/style` command.** Sets your output style for you, no editing `settings.json` by hand.
  `/style` opens a popup of your installed styles; `/style spartan` sets one directly;
  `/style default` restores Claude Code's built-in style. It reads both the global and the
  project `output-styles/` folder and writes whichever settings file matches, so a project
  style never leaks outside its project. New `commands/` folder, one-line install in the
  README. (PR #3, tkrevh)
- **Safer settings writes.** `/style` edits the settings file as JSON, not by line, so
  clearing a style from a single-key `settings.local.json` leaves `{}` instead of an empty
  (invalid) file that Claude Code would fail to load.
- **Dynamic styles badge.** The README styles count is now a live file-count, so it never
  goes stale as styles are added or removed.

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
