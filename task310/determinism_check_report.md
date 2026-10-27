# determinism-check report, task310, 2026-10-27

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (judge's disposition; see Findings for the one Gate G item to weigh)
**Stumping type:** mechanism: other (counterfactual solar reconstruction under export-limit censoring), stumping_family: mixed, surface_read_dependency: yes (borderline), sole_data_defect: yes

## Why
Gates A to E pass: the main call and all four supplementary blocks reproduce from the bundle. The literal estimand (guideline s3: the battery's average annual delivery to the panel homes in 2025, hour by hour) is forced to Yarrandale first once the limited homes' solar is read as censored output. Six reconstruction variants (mean, orientation-matched, no cap, no floor, neither) leave every rounded figure and the order unchanged. Run on the recorded solar, the same estimand gives the Sandhaven order; that is the easy route and the only fork that moves the call. The files rule it out rather than license it (counterfactual wording in s3, ES-114 s3.1, B1 pinned at the limit).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| kWh/battery Yarrandale / Sandhaven / Eastbrook / Tarrock | 2,450 / 1,900 / 1,500 / 1,300 | 2,457.7 / 1,907.8 / 1,502.3 / 1,293.8 | yes |
| Round MWh, same order | 5,900 / 4,600 / 3,600 / 3,100 | 5,899 / 4,579 / 3,606 / 3,105 | yes |
| Eligible homes Sandhaven / Eastbrook / Yarrandale / Tarrock | 6,591 / 8,535 / 4,381 / 4,539 | same (6,552 / 8,494 / 4,356 / 4,515 without previous_nmi) | yes |
| Pilot MWh Q1 to Q4 2025 | 324.6 / 287.8 / 271.3 / 309.9 | same (every serial counted: 343.4 / 305.2 / 288.3 / 328.6) | yes |
| Installers' batteries Sandhaven / Eastbrook / Yarrandale / Tarrock | 410 / 456 / 292 / 161 | same | yes |
| Round years | 2027 Yarr, 2028 Sand, 2029 East, 2030 Tarr | same order | yes |

## Competing answers that survived
- Recorded solar, read literally: Sandhaven 4,579, Eastbrook 3,524, Tarrock 3,105, Yarrandale 2,905 MWh, so the order is Sandhaven, Eastbrook, Tarrock, Yarrandale. Not a surviving fork (the shipped counterfactual wording and ES-114 close it), but it is the stump's wrong answer.
- Reconstruction method is unfiled; the data separate the candidates and no rounded figure moves (Gate C pass).
- Duo meter double report on ask 5 is inferred from 24 sites with identical daily energy and counters, and is undocumented. The judge rates this a moderate Gate C/E exposure on ask 5 only; no other figure is affected. The judge suggests an optional one-line Duo note.
- Batteries read as installations: natural reading, no fork.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 19 | yes |
| Formats | 3 or more | 4 (csv, parquet, pdf, xlsx) | yes |
| Large file | 25,000 rows or more | 2,803,200 rows (meter half-hours), 919,800 and 481,800 rows in two others | yes |
| Distractors | 2 or more in metadata, none named by file name | standing_offer_tariffs_2025-26.xlsx, hemp_household_survey_2024.csv; names are neutral | yes |
| Distractor weighing | unused by solution, relevant, ruled out by a shipped fact | not tested by the thread (the design note says they carry no figure the call reads); not verified here | not verified |
| Deliverables | 1 to 3, all in golden, no format family required | 3 (xlsx, png, pdf), all present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | prompt states unit and rounding for each of the six figures families | yes |
| Prompt shape and rubric 25 or more | identifiable shape; rubric not generated yet | shape 06 (metadata); the count of 25 rests on the many graded cells, not checked | yes, with the rubric count unverified |
| Not LLM generated, goldens realistic | n/a | thread: hygiene PASS; golden-realism is the author's gate | yes |
| prompt.txt | under 1,000 characters, one paragraph | 930 characters | yes |

## Gate G reconciliation
Thread: mechanism other, stumping_family mixed, surface_read_dependency yes (borderline), sole_data_defect yes. Card and design note: gate_g binding_constraint, stump_class analytical, layer 2 estimation_fit (censoring and truncation); the note says nothing is planted and the recorded flows are the field's standard method.

This is a mismatch, and the finding to weigh. The thread reads the stump as correcting a throttled record (the reported solar is a floor), which is the planted_defect_flip family, and it says the task collapses on clean data (sole_data_defect yes). The author labels it binding_constraint, but the binding limit is on the record and not on the decision, and the guideline's own valuation constrains nothing. The thread did not name a declared distractor as the surface read; the tariff and survey files are not load-bearing, so the distractor-too-load-bearing finding does not apply. The mismatch is the kind that predicts a send-back. A reviewer could class it as surface_read_rejection, with the recorded solar as the misleading read.

## Stump power (Gate F)
Moderate. A strong analyst who aligns clocks, differences counters and reads every connection code can still simulate on the recorded flows and file Sandhaven first. ES-114 states the mechanism and B1 sitting at the limit is visible, so the thread rates the trap as moderately pre-disarmed. The wrong answer is concrete: Yarrandale last at about 1,200 kWh a battery. The design note weighs the ladder; no solver was run.

## Gate H
Thread: domain pass, layers pass, decisive_step analytical. This matches the card (stump_class analytical, domain_test an hour-by-hour storage simulation with no noun-swap counterpart). The thread's analytical classing rests on the estimand: the battery must run on what the arrays produced. The thread did not class it as the field's standard method applied with no judgment. The route is not a textbook rule the guideline files; the note says no filed rule rebuilds the output. No stump-power downgrade is needed on that ground.

## Findings, ranked
1. Gate G mismatch: thread says surface_read_dependency yes, sole_data_defect yes, family mixed; the card says binding_constraint and analytical. The core of the stump is that recorded solar at export-limited homes is wrong and must be rebuilt. Weigh this against the client's litmus before shipping.
2. Ask 5 (pilot energy) depends on an undocumented Duo double report, inferred from data. It does not touch the call.
3. Guideline s3 does not say the battery runs on array output, so a literal reader of s3 on recorded solar gets the Sandhaven order. The thread offers an optional sentence on array output; adding it would help the determinism case but make the stump easier, so it is the author's call.
4. Distractor weighing and the 25-criterion rubric count are unverified here.

## Next action for the author
Decide whether the Gate G finding stands. Run the design note's litmus on whether the rebuilt solar overturns a wrong reported read or applies a modelling method. If the author keeps the design, record the answer in the note; otherwise re-root. No fix is required for determinism.
