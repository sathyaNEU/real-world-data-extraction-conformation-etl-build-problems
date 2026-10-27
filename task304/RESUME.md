# task304: where the build stopped and what comes next

Paused 2026-10-26 by the author mid stage 3 (repair of the asks and the world after the first stage 4 round).
Status in `pipeline.json` is still DESIGN; nothing below has been shipped.

## What was being done

Stage 3 rebuild of the mortgage collections build (Financial Support Team placement, four lending books,
possessions avoided in 2027). Changes made in `generator/` since the draw, all uncommitted until the PAUSED
commit:

- Main call rescaled: `EFFECT = 0.15` (plan section 3, "15 per cent"), pilot text now computed from the
  simulated team cut (`docs.py`), plan takes half the measured arrears cut. Writeup and goldens say First-time
  buyer 2019-21 about 10, High LTV 2022-24 and the others fewer than 5.
- Projection window fixed to January to December 2027, first entry absorbing (the earlier judge ran a
  12-step window from October 2026 and mismatched; see `## Tried and rejected` to add).
- Ask A re-sited: possession orders made or varied at hearings, re-sealed order lines (`RESEAL_SHARE`) are
  the same order, genuine same-terms variations after a hearing (`RETERM_SHARE`) count, open claims closed
  through the possession register. Prompt reworded to "orders the courts made or varied at hearings ...
  suspended on terms ... claims open at 30 September 2026" (824 chars, voice-check PASS).
- Ask B re-sited: loan parts (`PART2_SHARE`), two register rows and two completion statements per
  further-advance account; loss per property = sum of part debts less net proceeds, counted once.
- `checks.py` now collects every failure; `pair.py`, `verify.py`, `figs.py`, `golden.py`, `writeup.py`
  updated to the new asks.

## Last run (2026-10-27)

The three failures are fixed: owner-occupied High LTV accounts go to the panel solicitors faster
(`oo_lit=(0.45, 0.75, 0.45)` in `world.py`), seed 2 chosen from a scan of seeds 1 to 8 (`params.SEED`), the
recoveries stream offset 83 (`params.REC_OFFSET`), the pair-ceiling check now uses the current bar (60), and the pilot
report says "a 15 per cent cut ..., under half the cut in arrears" (asserted). `make.py --once`: 162 checks green;
golden First-time buyer 9.0 (family 8.0 to 11.9), High LTV 4.5, easy routes High LTV with the first-time buyer book at
most 3.7; pair 37.7, mirror leakage 16.7 per cent. The card, the design note's main-call sections, ask sheet, fork rows
SF12, SF13, SF18, SF22 and `## Tried and rejected` are updated.

## What to do next, in order

1. Run the full `make.py` in the background (no timeout: `verify.py` takes over ten minutes) and confirm it ends
   cleanly with two byte-identical builds and the verifier passing.
2. Write the design note's `## Pre-ship check` to the new build (checks count, zip digest, figures_check, precut,
   leak.py verdict lines, heart and surface).
3. `figures_check.py task304`, `precut.py task304`, `leak.py task304 --asof 2026-09-30`, `guard.py heart task304` and
   `surface task304`.
4. Fresh stage 4: two scored readers (hand-picked keys from the prompt's figures, no stump words or answer figures in
   the brief) and the determinism judge, all background, medium effort.
5. Ship and merge to main (`SHIPPED (task304): ...`, `git add -f task304/target.zip task304/golden/`).
6. Then the rest of the lane: task307 (PAUSED at draw), task308 (architecture 3 needs the author's decision),
   task309 to task312.

Delete this file in the SHIPPED commit (the design note's `## Tried and rejected` is the lasting record).
