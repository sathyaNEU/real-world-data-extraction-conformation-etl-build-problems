# task464 determinism, pass 3: the judge's Gate C finding closed

Architecture 3. Written by the build thread after the stage-4 judge returned NOT_DETERMINISTIC,
SEND_BACK on Gate C `competing_defensible_answer`. Architecture 2's two reports are its own history and
are untouched.

## The finding

The judge read "which comes nearest the standard" against five readings and the golden held under one of
them, the weakest:

| Area | Slots | Required, unrounded | Gap unrounded | To nearest | Up | Down | Shortfall as a share of required |
|---|---|---|---|---|---|---|---|
| Bexhollow | 312 | 332.16 | 20.16 | 20 | 21 | 20 | 6.07 per cent |
| Durnsfield | 170 | 189.62 | 19.62 | 20 | 20 | 19 | 10.35 per cent |

Clause 4.4 said only that the required figure is "rounded once at the area level" and gave no direction,
and nothing said what nearest is nearest in. The judge also named three smaller things: ask 4's date basis
and area basis were unstated, ask 5 had no as-of date for the register, and `cc3` read 3,092 where the
quantity it names is 3,093.05 on the pack it judged.

## How it is closed, in the order `determinism-check` ranks the moves

1. **The golden moved to the absolute shortfall in slots.** "Nearest the standard" plainly means the
   smallest shortfall, and defending a percentage reading against four readings in slots is the wrong side
   of the argument.
2. **C1 on the data, not a pin in the prompt.** One short area is now nearest under the unrounded figure
   and under every rounding of it, built by adding one treatment at a time to a non-nearest short area's
   largest site until the separation holds:

   | Area | Gap unrounded | To nearest | Up | Down |
   |---|---|---|---|---|
   | **Durnsfield** | **19.62** | **20** | **20** | **19** |
   | Bexhollow | 22.07 | 22 | 23 | 22 |
   | Lowenbrook | 23.28 | 23 | 24 | 23 |
   | Granleigh | 22.08 | 22 | 23 | 22 |
   | Kettlebrook | 34.33 | 34 | 35 | 34 |
   | Innsmere | 47.06 | 47 | 48 | 47 |

   Durnsfield is nearest on all four readings with **2 slots of daylight** to the runner-up on the
   tightest of them, asserted in `checks.py` as `SF13` and recomputed by `verify.py` from the bundle.
3. **The rounding direction is filed at authority.** Clause 4.4 now reads that the figure an area is
   required to hold "is rounded once, at the area level, up to the next whole treatment slot, because it is
   a minimum". It fixes the WHAT and names no method. Asserted present in the shipped document through the
   same extractor as its positive controls, and no area's verdict depends on the rounding, asserted per
   area against the unrounded figure, the floor and the ceiling.
4. **Ask 4's two bases are closed, and its primary moved rather than dying.** Clause 4.4 also files that a
   treatment is counted in the period of the contract year in which it was delivered, in network or out,
   and the asking sentence now names the area of the site treated. Closing both would have left the ask
   with no primary, so the primary is now the register's own claim header lines: it writes a `line_no` 0
   header carrying a claim's own treatment count for about a sixth of its claims, and its reconciliation
   workbook reports the doubled unit total, so a count-tie check passes on a figure the ask cannot use.
   Measured on the cut pack: summing every unit row moves 24 of ask 4's 48 figures, the run-out supplement
   12, and the residence-area column 24. The cracker still reaches 0 of 48.
5. **`cc3` is computed forward.** It was the summed, rounded required total divided by the cushion; it is
   now the sum of each area's own growth factor times its own weekly base, 3,095 on this pack, recomputed
   by the verifier from the bundle.
6. **Ask 5 carries an as-of.** The asking sentence now reads "the state register now holds", which the
   register's own position-as-at line and the agreement's network position date both fix at 19 February
   2027.

## What moved, and what did not

Graded figures that moved: ten area required figures by one slot and Bexhollow's by three (the ceiling plus
the C1 separation); four area shortfall figures following them; the network required total 3,556 to 3,568;
`cc3` 3,092 to 3,095; `call.nearest_short_area` Bexhollow to Durnsfield; one ask 4 share, 3.3 to 3.2, as
its denominator took the added treatments; and the encounter row count 639,009 to 639,110.

Unchanged: all 40 per-site slot figures, all 12 area slot totals, the 3,886 network total, the 274
deliverable positions against 327 attested stations, the six short areas, the flip set of three, every ask
5 and ask 6 figure, and the nearest area's shortfall figure of 20.

## What the judge confirmed and this pass did not disturb

It reproduced from the bundle the population of 40, the 274 against 327, every per-site and per-area
figure, the 3,886 total, the six short areas, the attested-stations route flipping three of the six and the
busiest-week route at eight short, all 48 out-of-network figures and both register asks. Gate H passes with
the decisive step analytical. On the ceiling it confirmed that no filed sentence fixes how it is computed
and that the record maximum, the yearly maximum, the minimum of the monthly maxima, the 2025 and 2026 table
alone and the 95th to 99.9th percentile all return the same 274, with only the median and the 90th
percentile diverging, which is the risk already recorded in `## Readability screen`.

## Gates after the fix

`checks.py` 652 assertions, `verify.py` PASS, two byte-identical rebuilds, `figures_check.py` 146 figures
with 0 absent, `leak.py` REVIEW with no LEAK, `precut.py` exit 0 at 52 checks, `voice-check.py` PASS at 998
characters. One re-judge is licensed and is the author's to spawn.
