#!/usr/bin/env bash
# Exact, surgical commit+push for the issue-#6 fix. Stages ONLY this task's
# files (never the pre-existing untracked WIP), commits to main, pushes,
# and verifies the push actually landed on origin/main.
set -euo pipefail
cd /Users/alexgreenshpun/CascadeProjects/Prompts/PERSONAL_OS/PROJECTS/attention-span

git add output-styles/spartan.md output-styles/attention-kind.md \
        benchmarks/harness/blocking_placement.py \
        benchmarks/questions/blocking-v1.jsonl \
        benchmarks/blocking/

echo "=== staged ==="
git status --short | grep '^[AM]' || true

git commit -q -F - <<'MSG'
Fix issue #6: blocking questions get buried mid-reply

Add a placement rule to spartan + attention-kind: a question you must wait
on is the last block, nothing after it; line one carries it when the reply
has other content; a proceed-without question stays inline. Deliverable +
go-ahead resolves to artifact-first, go-ahead-last. Rundown already handles
this (blocker in TL;DR, ends on pick-one), left untouched.

Adds benchmarks/blocking: 6 side-effect scenarios, a deterministic placement
checker (blocking_placement.py), a GLM-authored old/new contrast, and a real
on-target Claude run. Real Claude passes 6/6; the buried-question arm still
fails 6/6, so the checker discriminates. Non-regression probe confirms
deliverables still ship bare and ordinary answers are unchanged. Caveats
(n=6, hermetic no-tools env, post-hoc checker calibration) documented in
benchmarks/blocking/SUMMARY.md.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015YDHX92v3TcR2mhVYD3Dwx
MSG

echo "=== local HEAD ==="
git log -1 --oneline

git push origin main

echo "=== verify landed on origin ==="
git log origin/main -1 --oneline
echo "SHIP_OK"
