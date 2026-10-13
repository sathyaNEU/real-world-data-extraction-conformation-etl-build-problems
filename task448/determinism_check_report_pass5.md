# determinism-check report, task448, 2026-10-13 (pass 5)

Judged bundle: target.zip as it stood when the brief was made (fresh unzip at /tmp/determinism-check-task448-pass5/target/). The pack was later rebuilt for an in-thread repair; this report does not describe the rebuilt files. Verdict text is the thread's, unchanged. Thread: one general-purpose sonnet medium thread; brief at /tmp/determinism-check-task448-pass5/judge_brief.md, verdict at .../verdict.md.

## Verdict
NOT_DETERMINISTIC (supplementary ask 4, the program-year "All eight counties" total only; the main recommendation and the other 20 committed figures are forced). Label: margin_or_boundary_fragility (Gate C).
**Disposition:** SEND_BACK
**Stumping type:** mechanism: statistical_rigor (etl_conformance underneath), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Guidelines 7.5 force completion of the non-reporters and the file shows each lender's recording group, so the five, their order and the sixth are forced. The prompt does not file how the capture rate is estimated. The program-year total is 1,607.6 under the pooled ratio of sums (0.5975 late, 0.9665 same-day), answer 1,610. The unweighted mean of lender ratios gives 1,599.8 (1,600) and the highest late reporter ratio gives 1,600.5 (1,600). The range 1,599.8 to 1,612.8 straddles the 1,605 rounding line, so the unrounded total is 2.6 above the line and the rounded total is estimator-dependent.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Venridge stacked rows / closed 2024-25 | 3,770 / 2,628 | same | yes |
| Exclusions (re-rec, QCD, second, land-only, seller-carried) | 17/81/10/10/37 | same, leaves 2,473 | yes |
| HMDA reporters (7 shortlisted) | 311,228,182,151,141,138,133 | same | yes |
| Same-day capture | 1,673/1,731 = 97% | same (0.9665) | yes |
| After-deed capture | 236/395 = 60% | same (0.5975) | yes |
| Weyrauch / Mennwell / Heidebrecht / Kessinger / Eisenbrandt | 260/200/140/80/80 | 257.8/202.5/137.2/82.8/78.7 | yes |
| Ranking and rounded counts | 310,260,230,200,180; 150 | same | yes |
| Ask 3 counties (two-year) | 1,359.1/577.5/361.9/269.5/441.8 | same; stable across estimators | yes |
| Ask 4 counties (program year) | 710.9/311.1/191.8/151.9/241.9 | same; stable across estimators | yes |
| Ask 4 all-eight total | 1,607.6 -> 1,610 | pooled 1,607.6; mean 1,599.8; hi-late 1,600.5; mean>=20 loans 1,612.8; lo-late 1,611.3 | rounding not stable (1,600 vs 1,610) |
| April 2026 switch, 12 late lenders | 201 of 201 same-day, 0 of 79 earlier | same; rows 2.05x vs 0.92x | yes |

## Competing answers that survived
- Ask 4 "All eight counties": 1,610 (pooled ratio of sums, mean over lenders with 20 or more loans, lowest late ratio, HMDA-based July-Dec 2025) versus 1,600 (unweighted mean of lender ratios, highest late ratio). No shipped rule closes the estimator. Lender-level groups (1,736) and the median (1,570) are not credited.
- Minor open semantic fork, no top-six figure moves: 7 non-QCD deeds with the same grantor and grantee first token (guidelines 7.4 "relative" is not operationalised by a shipped field); the 10 second mortgages are inferred from amount (no lien field) and sit near the program total's line.
- Main call: no surviving competitor (Weyrauch 253.7 to 259.9, Mennwell 199.3 to 204.2 across variants; the set and order hold). Wrong routes: pooled 0.90 capture or raw rows gives Corvane, Halverd, Arkhaven, Weyrauch 170, Shunga 150 with Mennwell 130; counting the 43 Heidebrecht quitclaim refinances puts it near 209 (excluded by guidelines 7.3, 7.4). HMDA county_code for the county split gives 1,410/590/350/250/410 (wrong under guidelines 2.2).

## Spec gates
Checked from the unzipped bundle, the thread's hygiene section, and metadata.json.
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | csv, txt, pdf, xlsx | yes |
| Large file | 25,000 or more rows | hmda_lar_kansas_2024_2025.csv, 62,167 rows | yes |
| Distractors named, not in file names | 2 or more | metadata.json names hmda_2023_county_summary_ks.csv and homebuyer_education_completions_2024_2026.csv; judge found no file name labels one | yes |
| Distractors unused yet weighable; none reproduces a graded figure | yes | not independently tested by the thread beyond the hygiene line; neither is the surface read carrying the task | not fully checked |
| Deliverables | 1 to 3, all in golden | xlsx and pptx, both in golden/ | yes |
| Asks multi-dimensional with unit and rounding | yes | prompt: "Round every count to the nearest 10, each from its own unrounded figure"; ask 4 total is rounding-fragile | partial |
| Prompt shape and 25 or more criteria | identifiable, 25+ | shape 01 (ranked list under a cap); criterion count not verifiable here | shape yes, count unchecked |
| Not LLM-generated; goldens realistic | yes | judge found nothing; golden realism not re-read | yes (per thread) |

## Gate G reconciliation
Thread: mechanism statistical_rigor (coverage calibration of an incomplete extract by recording group), stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note declares a stratified (dual-system) capture for completing a register that misses producers, with the pooled capture as the wrong easy route (Mennwell about 135 against Shunga's 151). These agree. The declared distractors are not named as carrying the task. Gate G: PASS (FINE-numbers shape, not banned). Note the design note says the pooled path files a wrong five, and the judge confirms it (Weyrauch 170, Mennwell 130, Shunga fifth).

## Gate H line
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1: v3 to v4 layout change, MERS nominee names, re-recordings, cross-county land-only records, seller-carried notes. Layer 2: route-stratified capture calibration on the 46 lenders seen in both sources. Easy route: pooled 0.90 capture or raw rows, giving Weyrauch 170, Mennwell 130 and Shunga fifth. Matches the design note's Three rules.

## Stump power (Gate F)
Strong and analytical. The file captures after-the-deed mortgages at about 60 percent and same-day ones at about 97 percent, measurable only on the reporters in both sources. A strong model reading the layout guide's "not every PMM is in the file" plausibly applies one pooled capture and fails. A second layer is the April 2026 recording switch in the 12 late lenders, which only per-row capture handles (lender-level gives 1,736 against 1,610).

## Findings, ranked
1. Ask 4, "All eight counties: 1,610" (golden xlsx ask 4 and submission.md Section 4 item 4, step 8): estimator-dependent rounding, range 1,599.8 to 1,612.8 across valid estimators, unrounded value 2.6 above the 1,605 line. Gate C, margin_or_boundary_fragility. SEND_BACK.
2. Open semantic forks that move no top-six figure: the 7 same-surname deeds against the "relative" test (guidelines 7.4) and the 10 second mortgages inferred from amount with no lien field. They help put the program total near its line.
3. Per-county ask 3 and ask 4 figures: McPherson 577.5 and Marion 269.5 sit 2.5 and 4.5 from their rounding lines; every tested estimator stays put, so no finding, only a watch item.
4. Hygiene: PASS, nothing exclusion-level.

## Next action for the author
Fix ask 4's total only: either move the program-year data (the 2026 closings of the late-switch lenders) so the unrounded total sits near the middle of its 10-wide bin under every valid estimator (about 1,610 plus or minus 3 in all variants listed above), or drop the total or pose it as the sum of the five rounded rows. Do not file the estimator as the method. Also pin or confirm inert the 7 same-surname deeds and the 10 second mortgages. The main recommendation, ranking, ask 3 and the chart need no change.
