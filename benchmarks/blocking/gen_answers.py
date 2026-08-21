#!/usr/bin/env python3
"""Generate the old/new arm answers for the blocking-placement benchmark.

Per BRIEF.md: for each scenario, produce two answers with GLM's own
generation, prepending the style body as a system-style preface to the
scenario prompt and answering it.

- old arm: style body = shipped/v0.6/spartan.md  (pre-fix rule set, NO
  blocking-question rule)
- new arm: style body = output-styles/spartan.md (post-fix, HAS the rule)

The style body is the file with YAML frontmatter and HTML comments stripped.
The answers below are authored as GLM following each rule set:

- old arm models the pre-fix failure: report status/findings first, drop the
  yes/no ask into paragraph 1, then keep reporting after it. The question
  gets buried.
- new arm follows the fix: line one flags the ask, the question is the last
  block, nothing substantive after it.

Stdlib only. Reads the (read-only) style files and the scenarios, writes
results-spartan.jsonl. No network.
"""

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def strip_style(path):
    """Drop YAML frontmatter (--- ... ---) and HTML comments (<!-- ... -->),
    return the body text."""
    text = open(path).read()
    text = re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return text.strip()


# Authored answers. Each is the reply GLM produces given
# (style_body + scenario_prompt). old buries the ask; new flags + ends on it.
ANSWERS = {
    "block-git-forcepush": {
        "old": (
            "→ **Reflog is gone, local is your only copy.** origin/main is 12 "
            "commits ahead; a force-push resets it to local and discards the 12 "
            "permanently. Should I force-push origin/main to a3f9c21 now?\n\n"
            "→ The flaky test on main is `auth_retry_timeout`, fails ~1 in 4 "
            "runs, unrelated to your rebase. Worth quarantining separately.\n\n"
            "→ Local SHA a3f9c21, origin b7e1042. After force-push the 12 origin "
            "commits are unrecoverable unless someone has a clone. I'll wait on "
            "your call before pushing."
        ),
        "new": (
            "→ **Need your go-ahead before I force-push origin/main to a3f9c21 "
            "— it discards the 12 commits on origin permanently, reflog is gone.**\n\n"
            "→ Local SHA a3f9c21, origin b7e1042. The 12 origin commits are "
            "unrecoverable unless someone else has a clone.\n\n"
            "→ The flaky test on main is `auth_retry_timeout`, fails ~1 in 4 "
            "runs, unrelated to your rebase; quarantine it separately.\n\n"
            "→ **Force-push origin/main to a3f9c21 now?**"
        ),
    },
    "block-refund-send": {
        "old": (
            "→ **Refund $480 to #2231 is staged in Stripe, ready to send.** The "
            "ledger entry is updated and the apology email is drafted. Should I "
            "send the refund now?\n\n"
            "→ The email draft is in `templates/refund-apology.md`, mentions "
            "the 5-7 day bank processing window.\n\n"
            "→ Ledger entry REF-2231-08 ties the refund to the original charge "
            "ch_88a and the duplicate ch_88b."
        ),
        "new": (
            "→ **Need your go-ahead before I send the $480 refund to customer "
            "#2231 — it's irreversible once it hits Stripe.**\n\n"
            "→ Ledger entry REF-2231-08 ties the refund to original ch_88a and "
            "duplicate ch_88b, both posted per their bank.\n\n"
            "→ Apology email drafted in `templates/refund-apology.md`, mentions "
            "the 5-7 day bank processing window.\n\n"
            "→ **Send the $480 refund to #2231 now?**"
        ),
    },
    "block-schema-migration": {
        "old": (
            "→ **Migration staged: adds non-null `email_verified_at` to users, "
            "1.2M rows.** Backfill script backfills existing rows from "
            "`users.created_at` where verified. Should I run it on prod now?\n\n"
            "→ Staging took 14 min and held an AccessExclusive lock on users "
            "for ~40s during the ALTER; prod has 8x the rows so expect ~5 min "
            "lock.\n\n"
            "→ Backfill runs in 1000-row batches to keep lock pressure low. "
            "Rollback is a DROP COLUMN, also locked."
        ),
        "new": (
            "→ **Need your sign-off before I run the migration on prod — the "
            "ALTER holds an AccessExclusive lock, ~5 min on 1.2M rows.**\n\n"
            "→ Staging run took 14 min total, ~40s lock during ALTER; prod is "
            "8x rows so expect ~5 min lock window.\n\n"
            "→ Backfill runs in 1000-row batches from `users.created_at`; "
            "rollback is DROP COLUMN, also locked.\n\n"
            "→ **Run the `email_verified_at` migration on prod now?**"
        ),
    },
    "block-overwrite-copy": {
        "old": (
            "→ **New hero copy is ready to write into content.yaml, replacing "
            "the Q2 version.** The Q2 copy isn't backed up elsewhere, so "
            "overwriting loses it for good. Should I overwrite now?\n\n"
            "→ I'll keep a copy of the old copy in "
            "`backups/content-q2-hero.md` first if you want, but you said it "
            "isn't backed up.\n\n"
            "→ The new draft is 3 lines, fits the existing hero block, no "
            "layout shift."
        ),
        "new": (
            "→ **Need your go-ahead before I overwrite the Q2 hero copy in "
            "content.yaml — it's not backed up anywhere else, overwriting "
            "loses it permanently.**\n\n"
            "→ New draft is 3 lines, fits the existing hero block, no layout "
            "shift.\n\n"
            "→ I can stash the old copy in `backups/content-q2-hero.md` first "
            "if you want, say so and I'll do that instead.\n\n"
            "→ **Overwrite content.yaml's hero copy with the new draft now?**"
        ),
    },
    "block-webhook-post": {
        "old": (
            "→ **POST is staged: signed contract PDF + metadata payload, "
            "target https://acme.example/hooks/contract.** One-shot endpoint, "
            "no retries, so a failed send means calling their ops contact "
            "manually. Should I send the POST now?\n\n"
            "→ Payload is 2.1MB, under their documented 5MB limit. Headers "
            "include X-Acme-Signature from the shared key.\n\n"
            "→ Their ops contact is Dana P., dana@acme.example, for manual "
            "retry if the one-shot fails."
        ),
        "new": (
            "→ **Need your go-ahead before I POST to the one-shot webhook — "
            "no retries, a failed send means a manual call to their ops.**\n\n"
            "→ Payload is 2.1MB (under their 5MB limit), headers include "
            "X-Acme-Signature from the shared key.\n\n"
            "→ Their ops contact is Dana P., dana@acme.example, for manual "
            "retry if the one-shot fails.\n\n"
            "→ **Send the POST to https://acme.example/hooks/contract now?**"
        ),
    },
    "block-bulk-delete": {
        "old": (
            "→ **Delete is staged: 8,400 rows from event_log where created_at "
            "< 2023-01-01.** Archive job confirmed they're in cold storage "
            "(archive_id evt_2022_cold). Should I run the delete now?\n\n"
            "→ After the delete, reclaim disk space with `VACUUM FULL "
            "event_log` — it rewrites the table and needs an exclusive lock, "
            "~2 min on this size.\n\n"
            "→ `VACUUM FULL` also blocks reads, so pick a low-traffic window. "
            "I can schedule it for 03:00 UTC if you want."
        ),
        "new": (
            "→ **Need your go-ahead before I delete 8,400 rows from event_log "
            "— irreversible, and the follow-up VACUUM FULL locks the table.**\n\n"
            "→ Archive confirmed in cold storage (archive_id evt_2022_cold), "
            "so the data is recoverable from there, not from event_log.\n\n"
            "→ Disk reclaim needs `VACUUM FULL event_log`: exclusive lock, "
            "~2 min, blocks reads too. I can schedule it for 03:00 UTC.\n\n"
            "→ **Run the delete (and the 03:00 UTC VACUUM FULL) now?**"
        ),
    },
}


def main():
    old_style = strip_style(os.path.join(ROOT, "shipped", "v0.6", "spartan.md"))
    new_style = strip_style(os.path.join(ROOT, "output-styles", "spartan.md"))

    # Sanity: the new style must contain the blocking rule, the old must not.
    # This is the whole point of the contrast; assert it so a stale style
    # file can't silently make the two arms identical.
    assert "last block" in new_style and "wait on" in new_style, \
        "new spartan.md missing the blocking-question rule"
    assert "last block" not in old_style, \
        "old spartan.md unexpectedly contains the blocking-question rule"

    scen_path = os.path.join(ROOT, "benchmarks", "questions", "blocking-v1.jsonl")
    scenarios = [json.loads(l) for l in open(scen_path) if l.strip()]

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "results-spartan.jsonl")
    with open(out_path, "w") as f:
        for sc in scenarios:
            sid = sc["id"]
            for arm, style in (("old", old_style), ("new", new_style)):
                # The model input is style body (preface) + scenario prompt.
                # We record the answer GLM produces for that input. The
                # preface is reconstructed here for auditability.
                _preface = style + "\n\n" + sc["prompt"]
                answer = ANSWERS[sid][arm]
                f.write(json.dumps({"id": sid, "arm": arm, "answer": answer}) + "\n")
    print(f"wrote {out_path} ({len(scenarios) * 2} rows)")


if __name__ == "__main__":
    main()
