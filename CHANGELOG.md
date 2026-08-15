# Changelog

Versioning: single rightmost number bumps (0.2 → 0.3 → 0.4 …).

## 0.6

- **Rebuilt around the human, not the rule.** All three styles now open by telling the model what
  it is actually doing: spending a real person's limited attention, where burying the key point in
  a wall of text loses it just as surely as cutting it. That reframing (not a word limit, never a
  word limit) is what finally shortens replies that ballooned deep in a long session. Measured on
  Opus 5: long-session answers run ~30% shorter (p90 ~46%) with completeness held against the
  source context and coding work quality unchanged at 100% pass.
- **The zero-whitespace wall is gone.** The unbroken block that showed up deep in long sessions is
  fixed: one idea per block, blank-line-separated, on every turn including acknowledgments ("on
  it") and status. (Longest run of unbroken lines dropped 3.4 → 1.0 in testing.)
- **Depth requests stay deep.** Ask it to "really explain" or "walk me through it" and brevity
  switches off for that reply, you get the whole picture, every number and condition. No more
  compressing the one answer you wanted long.
- **Precision is protected.** Numbers, thresholds, and scoped conditions ("only for workspaces
  under 14 days") are treated as essentials and stated exactly, never rounded off or widened to
  "all".
- **Sharper opening line.** Every reply leads with one sentence carrying the whole takeaway, so
  reading just the first line (or the bold, or the TL;DR) gives you the answer.

## 0.5

- **Sharper styles.** All three styles get four rules: deliverable purity (produce a
  message/email/commit and you get just that, no "here's a draft" wrapper), never trim a
  warning when compressing, keep every essential point (brevity is shorter points, not fewer),
  and the bold/TL;DR alone must carry the whole answer.
- **Benchmark: honest and reproducible.** Measures the work and the output separately; the
  headline claims use no LLM judge. Work is unchanged (hidden-test coding A/B, pass rates
  equal), output ~43% shorter on average (50-71% on verbose answers), and you reach the point
  in ~6 words vs ~40 (answer in the first line 75% vs 3%). Deliverable purity 88%. Full writeup
  and runnable harness under `benchmarks/`.

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
