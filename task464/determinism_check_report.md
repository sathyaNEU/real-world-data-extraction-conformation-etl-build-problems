# determinism-check report, task464, 2026-10-17

## Verdict
NOT_DETERMINISTIC (competing_defensible_answer on the first property left out, its gap and four of the twelve $5,000 amounts; governing label margin_or_boundary_fragility, with underspecified_objective on the unfiled step-change method). Not SOLUTION_WRONG: the same twelve members came out in the judge's run.
**Disposition:** SEND_BACK
**Stumping type:** mechanism: forecasting (structural-break-aware normal-year projection), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The cycle rules say only that the 2027 penalty is "estimated from the property's own records" at the 1991-2020 normal. The golden needs a step search (BIC gain over 30, 6 spans a side, 6 per cent difference) and a refit after the last break, and none of that is in the prompt, the rules or the data dictionary; it exists only in SOLUTION_STEPS. The answer moves with reasonable choices: where the post-step window starts (the step falls inside a billing span) and whether electricity, which steps up on the same dates, is refit. Under those choices the first left out can be 461 Tallman Street ($70,990, electricity honoured) instead of 633 Lattermore Place ($68,577), and the $1,000 gap and four ask-1 amounts change. The 12th-to-13th margin ($7k) is inside the estimation freedom. Wrong-reason stump: a correct analysis can miss the golden.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Normal HDD / CDD (lindqvist_field_daily, base 65 F) | 4,735 / 1,048 | 4,735.4 / 1,048.1 | yes |
| Energy record rows | 16,124 | 16,124 (14,740 bills + 1,384 deliveries) | yes |
| Ask 4 penalties and counts by type | MF 2,508,379 / 46; Mixed 591,784 / 10; Hotel 94,657 / 2; Office 42,848 / 1 | identical | yes |
| Ask 5 emissions and site energy by type | MF 112,776 t, 1,678,848; Mixed 31,951, 456,003; Hotel 7,887, 119,295; Office 12,292, 165,192 | identical (thin rounding margins: hotel 7,886.51, office 12,291.52, MF 1,678,847.53) | yes |
| Whole-record fit slate | 173 Orrin, 429 Quillen, 461 Tallman in; 137 Ashlar, 843 Merrow out | same | yes |
| 137 Ashlar (12th) / 633 Lattermore (13th) | $75,000 / $70,000, gap $7,000 | $75,494 / $68,577, gap $6.9k | yes |
| 34 Thornwick | $160,000 | $169k | no |
| 62 Merrow | $150,000 | $163k | no |
| 151 Orrin | $90,000 | $120k | no |
| 937 Haddon | $80,000 | $84k | no |
| First left out | 633 Lattermore | 461 Tallman ($70,990) if electricity is refit | no (fork) |

## Competing answers that survived
- Step method: a step search implemented as filed flags dozens of series, not three; ask-1 differs on four of twelve rows and 151 Orrin vs 758 Fenwright flips. Shipped rule closing it: none.
- Post-step window start: 429 Quillen gas gives 1,609 / 1,580 / 1,526 / 1,454 / 1,466 t by first post-step span (about $40k swing; 15 Dec start ties 633 Lattermore at $68,600). 461 Tallman gas gives 1,542 t (22 Jan) or 1,334 t (20 Feb), about $57k. Shipped rule: none.
- Electricity refit with the heating fuel: 461 Tallman electricity runs about 1.35 times its fit Jan-Apr 2026. Honoured, first left out is 461 Tallman; not refit, 633 Lattermore. Shipped rule: none.
- Energy-record CSV: decimals for quantity and mmbtu, fuel sort order (alphabetical vs Table 1) and bill sort date (start vs end) unfiled (lower weight).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 16 | yes |
| Formats | 3+ | csv, xlsx, pdf | yes |
| Large file | 25,000+ rows | 52,094 (daily weather) | yes |
| Distractors | 2+ in metadata.json, none labelled in file names | energy_grades_2025.csv, grid_marginal_emissions_hourly_2025.csv; file names are neutral | yes |
| Distractor weight and ruling out | unused, relevant, ruled out by a shipped fact | not load-bearing in the judge's run (judge surface read was the whole-record fit); not separately audited | yes (as judged) |
| Deliverables | 1 to 3, all in golden | 2, both present in golden/ | yes |
| Asks multi-dimensional with unit and rounding | yes | yes (nearest $5,000, $1,000, whole dollars, tonnes, million Btu) | yes |
| Prompt shape and 25+ criteria | identifiable, 25+ | shape 01 (ranked list under a cap); rubric count not generated at this stage | shape yes, count not checked |
| Reads as real work product | yes | judge found no authoring leakage or incoherence | yes |

## Gate G reconciliation
Judge: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical; the declared stump is the whole-record fit that files 429 Quillen, 461 Tallman and 173 Orrin in place of 758 Fenwright, 843 Merrow and 137 Ashlar. This matches the judge's easy route (the judge confirmed the whole-record slate). Neither declared distractor carried the task. Mismatch is in the estimand, not the family: the design note's Not rule application line says "nothing states how a property's 2027 is estimated", which is exactly the open fork the judge found. Gate G: PASS (no shipped artifact ranks the candidates wrongly; stump is not a planted defect).
Gate H: domain pass, layers pass, decisive_step analytical. Matches the card's domain_test and analyst_test.

## Stump power (Gate F)
Moderate. A model with no step test files the wrong slate, but a model that finds the steps can still miss the golden, so the stump is partly a wrong-reason stump.

## Findings, ranked
1. Step-change method and post-step window start are unfiled; the answer moves by up to $40-57k per stepped series against a $7k 12th/13th margin.
2. Electricity step on the same dates is not addressed; honouring it changes the first left out.
3. Four of twelve ask-1 amounts (34 Thornwick, 62 Merrow, 151 Orrin, 937 Haddon) are not stable under a literal run of the filed search, and 151 Orrin / 758 Fenwright order flips.
4. Energy-record CSV decimals and sort conventions unfiled.
5. Hygiene passes; asks 4 and 5 reproduce exactly.

## Next action for the author
Close the fork with the WHAT, not the HOW: file in the prompt or rules that each property's estimate uses only its bills since its last change in how it runs, with a dated change log or works dates in the files for the stepped properties, and say whether electricity is refit; then widen the 12th/13th margin (stepped properties' post-step penalties at least about $25k under the 13th under any reasonable window), move ask-1 amounts off $5,000 boundaries, pin CSV decimals and sort order, and rebuild. Run /fix-determinism with this report; the judge's Fix section is at /tmp/determinism-check-task464-025216/verdict.md.
