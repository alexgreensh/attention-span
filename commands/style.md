---
description: Pick a Claude Code output style from a popup (attention-span styles)
argument-hint: "[attention-kind|spartan|rundown|default]"
allowed-tools: Glob, Read, Write, Edit, AskUserQuestion
disable-model-invocation: true
---

Set the active Claude Code output style. Argument (may be empty): `$1`

Do exactly this, no extra work:

1. Find the installed styles. `Glob` both locations, expanding `~` to the user's home directory:
   - global: `~/.claude/output-styles/*.md`
   - project: `.claude/output-styles/*.md`, relative to the current directory

   `Read` each file and note its frontmatter `name:`, its `description:`, and which of the two locations it came from. If the same `name:` appears in both, keep the project one and ignore its global twin, matching Claude Code's own project-over-user precedence. If neither location holds any style, say so, point at the install step in the README, and stop.

   Also note the style already set, so the popup can lead with it: read `outputStyle` from `.claude/settings.local.json` if that file exists, and otherwise from `~/.claude/settings.json`.

2. Decide the target style:
   - If `$1` is non-empty, match it case-insensitively against those `name:` values or the filename stem. `default`, `none`, or `off` means "remove the setting". No match → say so, list the valid names, and stop.
   - If `$1` is empty, ask with `AskUserQuestion`: header `Style`, question "Which output style?", one option per style file (label = its `name:`, description = its `description:`, prefixed with `Project style.` when it came from the project so the user can see which settings file is about to change), plus a final option `Default` / "Claude Code's built-in style, no custom instructions". The popup holds at most 4 options, so page it:
     - 3 or fewer styles: one popup with all of them + `Default`.
     - More than 3: put the style already set first, then the rest alphabetically by `name:`, so the order is stable and the current style is the first thing the user sees. Do not sort by file modification time: installing several styles in one go leaves them near-identical timestamps, and the paging comes out in an arbitrary order that changes on reinstall. First popup = the first 2 styles + `Default` + `More styles…`. If `More styles…` is picked, ask again the same way with the styles not yet shown (last page holds up to 3 styles + `Default`, otherwise 2 styles + `Default` + another `More styles…`). Every page carries `Default`, so it is always one click away.
     - Whatever the user types under Other, match it the same way as `$1`.

3. Pick the settings file from where the chosen style lives, so a style is never set in a project it does not exist in:
   - a global style → `~/.claude/settings.json`
   - a project style → `.claude/settings.local.json`, which is personal and not meant to be committed, so a preference never lands in a teammate's checkout

4. Write it. Treat each settings file as JSON, never as lines — line-based edits corrupt a single-key or minified file. `Read` the file first if it is there and parse it as JSON:
   - Chosen a style → set the top-level `"outputStyle"` to that style's exact `name:` value: add the key if absent, otherwise change the value. Keep every other key untouched, and write valid JSON back. If the file does not exist or is empty, `Write` it as `{ "outputStyle": "<name>" }`.
   - Chose `Default` → for both settings files, remove the `"outputStyle"` key and write the remaining object back as valid JSON. Clearing only one would leave the other still setting a style, so "off" would not be off. If removing the key empties the object, write `{}`, never an empty file (an empty settings file is invalid JSON and Claude Code will fail to load it). If a file is absent or has no `"outputStyle"`, leave it as is.
   - Touch nothing else, and keep the file valid JSON at every step. Do not delete lines; edit the parsed structure.

5. Reply in two lines: what the style is now and which file you wrote, and that it takes effect on the next request. If it does not, `/clear` or a restart applies it.
