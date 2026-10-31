# determinism-check report (pass 2), task268, 2026-10-31

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: etl_conformance, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread verdict: /tmp/determinism-check-task268-20261031205332/verdict.md (one re-judge pass on target.zip f51f0c63748484a1, after the FIX_NOW on ask 4 from pass 1).

## Why
The main call reproduces: Oro Rosso 741 of 1,857 (40%), Nordhavn 764 of 1,568 (49%), gap 9 points. All seven overlap rows and the multibuy grid (20 cells) match. The pass 1 defect is closed. With the price board's Paying section filed (card within 25 minutes, cash the same day, unpaid labels void), the counter payments resolve to a single assignment (9,460 payments) and all 12 kilogram cells equal the new golden (Glenmore 514.4 / 503.7 / 521.9 / 542.9, Ardcath 441.7 / 464.9 / 470.2 / 471.3, Inish Bean 361.1 / 363.3 / 375.4 / 347.7).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Card-paid receipts matched | 50,047 sales | 50,172 receipts, one row each (50,047 sales plus 125 refunds); window-insensitive | yes |
| Homes that bought coffee | 3,802 | 3,802 | yes |
| Oro Rosso, Nordhavn | 1,857 / 741 / 40% and 1,568 / 764 / 49% | same | yes |
| Other five rivals | 51, 52, 52, 56, 79% | same | yes |
| Multibuy grid | 20 cells | 20 of 20 | yes |
| Counter kg grid | 12 cells | 12 of 12 | yes |

## Competing answers that survived
- Home definition: card-by-card gives Nordhavn 16.5%, and linking through online accounts only gives Nordhavn 28%. The brief's "A home is the people who live in it" rules both out, and shared-card closure is the only coherent reading. Residual risk is low to moderate, because no file states the linking rule.
- Multibuy rate column: reading "Agreed" instead of "Effective from" moves 3 cells (Cafetto Q4 156, Halloran's Q2 141, Nordhavn Q3 239). The header makes the golden the literal reading.
- Counter accessories: a cap of 3 or 4 accessories per sale, instead of at most 2, leaves 89 sales with more than one consistent set, moving cells by up to about 4 kg. Every sale is explainable with at most 2, so the fewest-accessories reading gives one answer. This cap is filed nowhere in the pack. Hardening note only.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | 6 | yes |
| Large file | 25,000 rows or more | 257,557 (settlement), 73,375 (till) | yes |
| Distractors | 2 or more, in metadata, no file name labels one | census households and brand tracker in metadata.json | yes |
| Distractors unused yet weighable | required | thread found them unused by the solution; I did not independently check whether either reproduces a graded quantity | partial |
| Deliverables | 1 to 3, all in golden | 2 | yes |
| Asks | multi-dimensional, unit and rounding stated | yes | yes |
| Prompt shape and rubric 25 or more criteria | required | shape identifiable; rubric not available to count | not verified |
| Reads as real work product | required | no authoring language found; golden realism not re-judged | yes |

## Gate G reconciliation
Gate G is unchanged from pass 1 (`etl_conformance`, `analytical_non_defect`, no surface read, no sole data defect), and it matches the design note, the card's `stump_class: analytical` and the ladder (R1 Nordhavn 16.5%, R3 Oro Rosso 39.9% against Nordhavn 48.7%). No declared distractor carries the call. Gate H: domain pass, layers pass, decisive_step analytical. The thread notes the unit is borderline with data_semantics because the brief names it. Assembling the home from the data is the analysis, and SF1 closes the reading.

## Stump power (Gate F)
Moderate to good. The card-level route files Nordhavn at 17%, and cards plus unlinked online files Westquay at about 26%. Only the full home build lands Oro Rosso. The weight sits on the settlement join and household closure, so the main-call ladder is untouched by the ask 4 repair.

## Findings, ranked
1. The home-linking rule is stated in no shipped file (low to moderate risk). Closed by SF1 and the brief. No change recommended, because a filed linking sentence would turn the decisive step into rule application.
2. The two-accessory cap on a counter sale is filed nowhere. Optional hardening: add an SF row naming the fewest-accessories convention, and assert in checks.py that the generator's assignment is the unique minimal one. SF17 to SF21 already cover the windows and the dating.

## Next action for the author
No repair is required. Proceed to ship, optionally recording the two hardening rows in the design note first.
