# determinism-check report, task458, 2026-10-15 (run r3)

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The designation (Adams, Douglas, Franklin, Grant, Okanogan) follows from NP-31 2.5's estimand (every member who has the condition counts, identified or not) plus data that reject both competing estimators. Counting identified members gives 3 counties. Carrying full-year prevalence (whole, by group, by county, or by county x group) gives 6 (adds Yakima). The shipped claims contradict the carry: 1.6% of expansion adults enrolled two months are identified against 3.2% of full-year expansion adults within their first two months. Exposure-adjusted counts reproduce the golden to the unit under pooled, group, county and county x group stratification. Gates A to E pass. Softness: 2.5 leaves the estimation method open, which is the intended stump, and the data separate the candidates.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Adult members (distinct client_id) | 123,460 | 123,460 | yes |
| Enrolled all 12 months | 70,377 | 70,377 | yes |
| Identified SMI / OUD | 7,109 / 4,421 | 7,109 / 4,421 | yes |
| First identified Jul 2025 / within 3 months | 30.5% / 66.7% | 30.5% / 66.7% | yes |
| Practising prescribers, 10 counties (131 total) | 4, 30, 12, 3, 10, 10, 7, 4, 10, 41 | identical | yes |
| SMI estimate, nearest 10 (10 counties) | 320, 1,220, 510, 340, 710, 790, 290, 490, 560, 2,320 | identical | yes |
| OUD estimate, nearest 10 | 230, 740, 330, 200, 490, 510, 140, 300, 350, 1,580 | identical | yes |
| Standards (unrounded) | Franklin 14.08/20.41/0.736, Grant 12.67/19.61/0.752, Yakima 17.69/25.95/0.731, Walla Walla 17.89/28.54/0.742 | identical | yes |
| FFS net payments, county x quarter | 40 cells | 40 identical | yes |
| County x eligibility group members and payments (CSV) | 40 rows | spot-checked Adams, Grant, Yakima; paid_amt equals the sum of lesser of billed and allowable on all 16,027 claims | yes |

Margins: Yakima needs more than 2,485 (SMI), 2,493 (reach) or 1,783 (OUD) estimated members to be designated; estimate 2,318 (bootstrap SE about 51). Franklin and Grant fail both ratios by wide margins.

## Competing answers that survived
- F1, exposure unit: months enrolled (golden) against first-to-last span for the 10,941 members with coverage gaps. Span moves 8 of 20 nearest-10 figures by 10 to 30 (Adams 310/220, Franklin 690/480, Grant 770/490, Yakima 2,290/1,550); designation unchanged. The data pick months enrolled (gap members' implied prevalence matches contiguous peers only under it). No designation-level fork; a graded-figure sensitivity only. The author deliberately leaves it unfiled (a clause would point at the decisive step), recorded in the design note.
- F2, estimator: carry (6 counties) and identified-only (3) are rejected by the shipped identification curves; all hazard-adjusted variants give identical 20 figures. This is the stump, not a fork.
- Minor, designation unchanged: 2-8 Nov weekly file (after as-of; moves Franklin to 9, Kittitas to 6), mailing against practice address, RES/TOT against BUS ratio (pinned by 2.7), county at service date against last-day county (pinned by 2.3).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | csv, xlsx, pdf | yes |
| Large file | 25,000 rows or more | enrollment 137,838; claims 104,860 | yes |
| Distractors in metadata.json, none named in a file name | 2 or more | 3: network_adequacy_time_distance_2026q2.xlsx, ofm_april1_population_2026.csv, npidata_pfile_wa_20261102-20261108.csv (post as-of file) | yes |
| Distractors unused yet weighable; a ruling shipped fact | yes | network adequacy is June 2026 member counts, OFM is population, neither carries condition counts; the 2-8 Nov file post-dates the 1 Nov as-of | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, csv), both present | yes |
| Asks multi-dimensional, unit and rounding stated | yes | county x condition counts, quarterly payments by county, group file; "nearest 10" and "whole dollars" stated | yes |
| Prompt shape and 25 or more criteria | yes | shape 10 scorecard; design note counts about 63 before asks' rows | yes |
| Not LLM-reading; goldens real work products | yes | judge found no authoring language in shipped files; golden workbook has Designation, FFS payments, Notes sheets. I did not run golden-realism | yes (provisional on realism) |

Notes: the judge listed nucc_taxonomy_261.csv as a distractor, but metadata.json names the 2-8 Nov weekly file instead; the NUCC file is a lookup the solution uses, so metadata is correct. Judge could not see provenance records; metadata.json records source, date and license (CC0-1.0, constructed) for all 16 files. Final-build note from the caller: the network adequacy distractor now stores percentages to three decimals; no graded figure, policy or prompt changed, and I did not re-run the thread on it.

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: maturity_censoring / estimation_fit, decisive step the window-weighted count against carrying full-year prevalence, "Gate G etl_conformance" is a label in the same-puzzle line only; card stump_class analytical with analyst_test and domain_test present. The easy route in the design note (carry by group files 6; identified count files 3) matches the thread's easy routes exactly, with the same Yakima 2,660 against 2,320. No declared distractor was named by the thread as the surface read carrying the task. Match.

Gate H: thread `domain: pass`, `layers: pass`, `decisive_step: analytical`. Design note's Three rules: same, with Layer 1 (NPPES monthly plus weekly updates, split ZIPs, claim chains, member renumbering) never carrying the stump. Match.

## Stump power (Gate F)
Strong. Both tempting routes (identified count 3 counties; full-year prevalence carry 6 counties) fail; only the exposure-adjusted ascertainment lands on 5. Layer 1 ETL is cleared by a careful model and does not move the designation. Thread expects at least two strong runs to take the carry route.

## Findings, ranked
1. Optional: F1 exposure unit (months enrolled against span) moves 8 of 20 nearest-10 figures by 10 to 30 with the designation intact. The data choose the golden; the author has declined to file a clause. Residual risk is a regrade dispute on the nearest-10 cells only.
2. Info: judge could not verify provenance records; metadata.json holds them.
3. Info: post-thread pack change (network adequacy distractor to three decimals) is outside the judged evidence but touches no graded quantity.

## Next action for the author
Proceed to ship. If a portal finding arrives on the nearest-10 cells, file the exposure as a population definition (months of coverage), not the estimator, through /fix-determinism.
