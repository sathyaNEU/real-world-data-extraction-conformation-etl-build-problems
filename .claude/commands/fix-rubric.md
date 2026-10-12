---
description: Repair a build whose main call held on the portal but whose rubric score came back at or over 50. Reworks only the supplemental asks and their devices until the top two responses sit under 50 (built to 40), with the main recommendation side frozen so a passed verdict cannot turn into a failed one; proves the scope with freeze.py and re-ships.
argument-hint: taskNN <the portal result: the top two scores and which rubric rows each response passed>
effort: max
---

# /fix-rubric

The build named in `$ARGUMENTS` held its main call on the portal, and the top two responses still averaged
50 or more because they collected the asks. The job is to take ask weight away from those responses. The
main recommendation is what passed: its sentence, its figures, its ladder and the rows it reads are not
touched, because a change there can flip the call and turn the verdict.

Invoke `supplemental-stumping` (Parts 0, 1, 3 and 6) and `build-pipeline` first. If the portal rows are not
in `$ARGUMENTS`, read them from `pipeline.json` (`portal`, `returned`) or ask once and stop.

**1. Freeze before any edit.**
`python3 .claude/skills/build-pipeline/freeze.py snapshot taskNN`. Read the ask sheet, the cracker and mirror
sheets, and `## Tried and rejected`.

**2. Read where the points went.** For each of the top two responses, mark every ask criterion it passed and
the path that got it there: a construction it had (it landed the call, so the construction layer is free to
it), a device its hygiene battery executed, a figure a filed rule handed it, a control that confirmed it.
Write the pair arithmetic (`supplemental-stumping` Part 0): the ask weight each kept, against a fifth each.
The ask's points come back only from devices the cracker's path misses.

**3. Redesign the ask layer on the ask paths only** (Part 6, call held):
- Replace every device the responses executed with a primary from the **silent** list (Part 3), on rows
  outside the main call's declared population, under the nine laws and the four bans. A device on the
  measured-executed list is a work order, never a primary.
- Stack shared hazards so each moves several asks with per-ask deltas, and score the cracker sheet again:
  every ask row misses, the mirror keeps under 35 per cent of ask weight, the pair at or under 40.
- Change data on the ask paths first: devices, their rows, ask goldens, assertions. The prompt's ask wording
  changes only when no device can hold the ask as worded, and then with every figure, unit and rounding kept,
  the criteria count unchanged, no presupposition (H23) and `voice-check.py` green. The call sentence is
  frozen.
- Never touch: the main call's rows, the files it reads, the ladder, the stump, the card's driver, the
  Final Recommendation and Critical Components blocks. A device that needs any of them is dropped.

**4. Assert, rebuild, prove the scope.** `checks.py` asserts the separation line by count (zero device rows in
the main population), that files the call reads are byte-identical to the shipped commit, and that every
main-call figure recomputes unchanged. Rebuild twice (byte-identical), redraft block 4 of `submission.md`
from `figures.json` (`submission-writeup`), then the free gates: generator checks, `verify`,
`figures_check.py`, `precut.py`, `leak.py`, `voice-check.py`, `guard.py validate` and `heart`. Then:

```
python3 .claude/skills/build-pipeline/freeze.py check taskNN --mode rubric
```

Exit 1 means the main side moved: undo it. A PASS that reports no ask file moved changed nothing graded.

**5. Re-ship.** Re-cut `target.zip`, append to `pipeline.json` `returned` (`repair: "rubric"`), set `status`
`shipped`, one `## Tried and rejected` line per device replaced (what the responses did to the old one), an
ask-sheet line per new device, rewrite the ledger row's status, and commit `RESHIPPED (taskNN): rubric, <the
devices replaced>` with the zip and `golden/` force-added (`CLAUDE.md`, Git).

**Report:** the pair arithmetic before and after (on paper), the devices replaced, the `freeze.py` verdict,
the zip path. No judge (the determinism block passed and the main side is frozen; spawn it only if an ask
figure's wording changed in the prompt), no clone check, no solver.
