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

## Last run (scratchpad make2, before the pause)

`checks: 159 passed, 3 failed`:

1. `R3a`: the easy route (rate rise by months since the switch) must file High LTV and currently does not.
2. `ask B primary moves the sales and the losses, Shared ownership`: the loan-part device does not move the
   Shared ownership row (too few further advances there).
3. `pair ceiling and mirror leakage`: pair above 40 (last measured 40.7, cracker keep 0.222, hits on askA
   open for all three books and Shared ownership suspended).

## What to do next, in order

1. Fix the three failures in the generator: retune the world so the easy route lands on High LTV again
   (`world.py` hazard / `book_h`), give Shared ownership enough loan-part accounts in the sales window,
   and make the open-claims count move under the cracker's handling (the register closure must bite in
   every book) so the pair falls to 40 or under.
2. Full `make.py` (two byte-identical rebuilds, `verify.py` agrees), regenerate `figures.json`.
3. Rewrite `DESIGN_NOTE.md` to the new figures: fork table, closure table, literal reader, ladder, ask sheet,
   pre-ship check, and append to `## Tried and rejected`: the judge's 12-step window slip, the rescale to a
   15 per cent effect, the ask re-site (old asks cracked).
4. Update the card (`.claude/skills/fingerprint/cards/task304.json`) answer to the new call; `submission.md`
   from `figures.json`.
5. `figures_check.py task304`, `precut.py`, `leak.py task304 --asof 2026-09-30`, `guard.py heart task304`
   and `surface task304`.
6. Fresh stage 4: two scored readers (hand-picked keys from the prompt's figures, no stump words or answer
   figures in the brief) and the determinism judge, all background, medium effort.
7. Ship and merge to main (`SHIPPED (task304): ...`, `git add -f task304/target.zip task304/golden/`).
8. Then the rest of the lane: task307 (PAUSED at draw), task308 (architecture 3 needs the author's decision),
   task309 to task312.

Delete this file in the SHIPPED commit (the design note's `## Tried and rejected` is the lasting record).
