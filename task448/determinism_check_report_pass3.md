# determinism-check report, task448, 2026-10-12 (pass 3)

## Verdict
DETERMINISTIC (the main call, order and all twelve counts reproduce and are forced); SOLUTION_WRONG on one prose clause (Heidebrecht "lifts it to 200").
**Disposition:** FIX_NOW
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: yes (borderline, routed to live testing)

## Why
The bundle forces Corvane 310, Weyrauch 260, Halverd 230, Mennwell 200, Arkhaven 180, Shunga Valley 150 sixth. The only routes to a different five skip or pool the coverage correction. Capture splits 97% (recorded with the deed) against 60% (recorded after), and no other filed attribute separates it (MERS vs direct naming: 96.4% vs 96.7%). Residual weakness sits in the numbered asks and one prose clause.
The judge thread ran from the scratch unzip only. The main session spawned it from judge_brief.md (this runtime has no Agent tool).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Reporters' HMDA counts (hmda_lar, action 1, purpose 1, lien 1, 8 counties, 2024-25) | Corvane 311, Halverd 228, Arkhaven 182, Shunga 151, Tessaline 141, Saltfork 138, Ninnescah 133 | same | yes |
| Venridge rows after cleaning | Weyrauch 154, Mennwell 121, Heidebrecht 82, Kessinger 80, Eisenbrandt 47 | same (2,473 rows in window) | yes |
| Capture with the deed | 1,673 / 1,731 (97%) | same | yes |
| Capture after the deed | 236 / 395 (60%) | same (each of four lenders 59-61%) | yes |
| Adjusted non-reporters | 260, 200, 140, 80, 80 | 257.7, 202.5, 137.2, 82.8, 78.7 | yes |
| Two-year counties | 1,360 / 580 / 360 / 270 / 440 | 1,359.1 / 577.5 / 361.9 / 269.5 / 441.8 (total 3,009.9) | yes |
| Program year | 710 / 310 / 190 / 150 / 240; total 1,610 | 710.9 / 311.1 / 191.8 / 151.9 / 241.9; total 1,607.6 | yes |
| Heidebrecht with quitclaims ("lifts it to 200") | 200 | 125 / 0.597 = 209, rounds to 210 | no (prose only; design note R4 says 202.4) |

## Competing answers that survived
- Program-year total: 1,610 if rounded once from unrounded figures, 1,600 if summed from rounded rows or from rounded capture rates (1,601.5). The golden sits 2.6 above the 1,605 edge. The prompt says only "Round every count to the nearest 10"; the "rounded once" pin lives in the golden text, not the prompt. Open fork on one cell.
- County of the home for reporters: HMDA county_code (institution geocode) gives 1,410 / 590 / 350 / 250 / 410; the recorder's county gives the golden. The dictionary and guide now support the golden reading, but no file says the HMDA geocode is wrong. Residual fork on the county asks (design note SF4/SF11 already close it by a sentence).
- Discoverable only from the data, not documented: the 6 April 2026 switch to same-day recording. Ignoring it gives a program-year total of 1,736. Layer 1.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | 4 (csv, txt, pdf, xlsx) | yes |
| Large file | 25,000 or more rows | hmda_lar 62,167 rows | yes |
| Distractors in metadata.json | 2 or more, none labelled in a file name | hmda_2023_county_summary_ks.csv, homebuyer_education_completions_2024_2026.csv | yes |
| Distractors relevant and unused | yes | judge: relevant and unused by the solution | yes |
| Deliverables | 1 to 3, all in golden | xlsx and pptx, both present | yes |
| Asks multi-dimensional, unit and rounding stated | yes | county by period grid plus ranking; "nearest 10" stated once | yes (see the total fork) |
| Prompt shape and 25 or more rubric criteria | identifiable, 25+ | shape 01 (ranked list under a cap); criteria count not checked here (rubric is generated downstream) | shape yes, count not verified |
| Reads as real, not LLM generated | yes | judge notes: manifest calls invented HMDA data "public FFIEC", and the lender names read somewhat generated; neither is exclusion-level | pass with notes |

## Gate G reconciliation
Judge: `mechanism: statistical_rigor`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: yes` (borderline). The design note and the earlier passes record the same family (analytical_non_defect, sole_data_defect borderline: the recorder file's partial capture is the object the method estimates). No mismatch. Neither declared distractor carries the task; the surface read is "rows as filed" or the pooled 90% rate, and neither is a distractor file. The easy wrong routes (rows as filed, or the pooled 89.8% rate) recruit Shunga Valley fifth and omit Mennwell, which matches the design note's R1 and R2.
Gate H: domain pass, layers pass, decisive_step analytical. This matches the card and the design note. The exclusion rules (quitclaim, seller-carry, re-recording, shared deed) are rule application but are lower steps, not the decisive one.

## Stump power (Gate F)
Moderate to good. The layout guide's one-line incompleteness warning prompts the coverage check. A solver must then find that capture splits by recording timing and that all the non-reporters sit in the 60% group. Strong models that check capture lender by lender will see the 97% vs 60% split quickly, so the stump may be weaker than designed; the portal decides.

## Findings, ranked
1. Program-year total (1,610 against 1,600) is a one-cell rounding fork. Pin the rounding in the prompt, or shift the figures off the boundary.
2. The Heidebrecht clause says 200, but the judge recomputes 209 (rounds to 210). The design note's R4 says 202.4. The author should reconcile the clause with `verify.py`; the conclusion is unchanged because Heidebrecht is above Mennwell and Arkhaven either way.
3. The county of a home (recorder against HMDA geocode) is closed only by the dictionary and guide sentences. The judge asked for an explicit pin.
4. The 6 April 2026 switch is visible only in the data. This is Layer 1, and the judge calls it discoverable.
5. Hygiene: the manifest provenance label overstates the HMDA files as public data when the institutions are invented.

## Next action for the author
Run /fix-determinism for the Heidebrecht clause (reconcile 200 against 210 using verify.py) and the program-year total rounding pin, without moving any frozen figure or filing the capture method. Then regenerate and re-run freeze.py.
