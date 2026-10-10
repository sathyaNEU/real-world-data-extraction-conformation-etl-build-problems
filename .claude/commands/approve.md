---
description: The author's sign-off on a built task. Checks the heart of the stump against every card and ledger row for a template or a duplicate, re-runs the surface screen, refuses a LEAK, and on PASS writes the pipeline state to approved and brings the fingerprint card up to date.
argument-hint: taskNN
---

# /approve

The author is signing off the build named in `$ARGUMENTS` for the portal. Resolve a bare number or
`taskN` to `taskN/` at the repository root (the folder holding `CLAUDE.md`); if nothing is named, ask and stop.

Run these in order and stop at the first failure:

1. **The heart check.** `python3 .claude/skills/fingerprint/guard.py heart <task>`. It reads the
   card's `driver`, `driver_concrete` and `stump` and compares them with every card's driver, every
   lineage driver, every card's stump sentence and every shipped-ledger row, then runs the full
   structural check (the Part 6.1 bans, the same-puzzle and same-driver tests, names, furniture).
   Exit 1 is a BLOCK and the command stops there: relay the nearest builds it printed and the axis
   to redraw. A WARN is relayed with the one-line differentiation the design note carries, or the
   lack of one, which is a finding.
   If the card's `stump` or `driver` is empty, fill it from the design note's stump sentence first
   (`guard.py validate <task>` afterwards), because a card with no heart cannot be checked.
2. **The surface screen.** `python3 .claude/skills/fingerprint/guard.py surface <task>`. A promoted
   pair is a rename or a regeneration, not an approval.
3. **The leak report.** `<task>/leak_check_report.md` must exist and its verdict line must not read
   LEAK. If it is missing, run `python3 .claude/skills/leak-check/leak.py <task> --quiet` and read
   the verdict. REVIEW passes only if every REVIEW line is answered in the design note; say which
   are not.
4. **The design note's stump sentence.** Grep `DESIGN_NOTE.md` for the one sentence naming the
   wrong committed answer a competent solver files and the step that lands them there. Absent, the
   build has no stump to approve: stop and say so.
5. **The solver record.** If `<task>/pipeline.json` exists, read `solver_rounds`. Relay the last
   round's proxy scores. The author decides whether to approve a build no solver round has touched,
   so state it plainly rather than refusing.

On PASS:

- Update the fingerprint card's `answer`, `answer_source`, `spine.rows`, `deliverables` and
  `opening_move` from the submission and the pack if any is stale (`fingerprint` Part 2 step 5),
  then `guard.py validate <task>`.
- Write `<task>/pipeline.json` with `"stage": "approved"` and the ISO date (create the file with
  that one field if it does not exist).
- Tell the author: approved, the heart verdict line, the nearest build and its similarity, and
  that the ledger row waits for the portal result.

This command never writes the shipped ledger (that waits for the portal), never edits the prompt,
the bundle or the submission, and never spawns an adjudicator. Where the heart check promotes a
pair the author wants read, `/clone-check <task>` is the adjudicated route.
