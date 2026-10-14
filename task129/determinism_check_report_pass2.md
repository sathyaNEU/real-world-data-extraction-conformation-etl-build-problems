# determinism-check report, task129 (pass 2), 2026-10-14

## Verdict
DETERMINISTIC (the thread also flagged SOLUTION_WRONG on one solution-block item, since removed; see Findings).
**Disposition:** FIX_NOW as returned by the thread. The main session has since removed the chart line from submission.md block 4, so the item is closed with no figure, prompt or data moved. Nothing remains that needs a rebuild. Recorded here, not re-judged (one thread only).
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Policies ENG-REL-02 and OPS-ROW-01 file the rate, ticket folding, the major event days and the driver-to-programme map, so every graded figure falls out of a literal reading. The main call (hazard-tree removal) reproduces. North carries about 77 percent of the cooperative's rise (about 8.2 of 10.7 points). North's 2025 rise is nearly equal at 0 to 2, 2 to 4 and 4+ years since trim. Units last trimmed by either contractor fail at about the expected rate. North's 2025 rate climbs with ash share (quartiles 14.9 / 21.6 / 31.1 / 52.4 against flat 10 to 13 in 2021 to 2023). Pass 1's ticket-folding fork is closed: the thread folded 391 duplicate tickets per device and got the golden. The thread ran with no knowledge of pass 1.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Cooperative rate 2025 / 2021-23 avg | 21.9 / 11.2 | 21.92 / 11.17 | yes |
| North rate 2025 / 2021-23 avg | 30.2 / 11.1 | 30.21 / 11.08 | yes |
| Major event days 2025 | 18 Jun, 9 Dec | 18 Jun (135.2), 9 Dec (88.6); threshold 8.28, next day 4.98; unchanged under sample/population SD or own-year members | yes |
| Workings ask 2, North | 160 / 5,956 / 1,821,820 | same | yes |
| Workings ask 2, East | 123 / 3,559 / 1,203,168 | same | yes |
| Workings ask 2, South | 112 / 3,598 / 1,150,972 | same | yes |
| Workings ask 3 miles N/E/S | 1,773.3 / 1,237.8 / 1,138.3 | same (168 future UNDERGROUND retirements still in service) | yes |
| Workings ask 1, Hollenbeck Q1-Q4 | 66.5 / 80.9 / 84.4 / 56.6 | same | yes |
| Workings ask 1, Garrity Q1-Q4 | 94.7 / 136.3 / 114.9 / 178.5 | same (feet at 5,280, credits netted to service month) | yes |
| Contractor expected-count ratios | Garrity 0.98, Hollenbeck 1.01 | coarse bins 0.88 / 1.03 (within Poisson noise); both near 1 | direction yes, exact values not from coarse bins |
| North 18.8 rise at 0-2 yrs | 18.8 | 0-2 yrs about 4 to 23.5 (coarse bins) | direction yes |

## Competing answers that survived
- Main call: none.
- Workings ask 1 only: gross invoices ignoring credit memos, or credits dated by memo date, move a few tenths of a mile. Policy 4.3 and the dictionary's service_month and applies_to_invoice lines favour the golden's netted service-month reading (the thread agrees). The coordinator treats this as answered; supplementary figure only.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 in target.zip | yes |
| Formats | 3 or more | 5 (csv, xlsx, docx, pdf, parquet) | yes |
| Large file | 25,000 rows or more | parquet 168,644 rows; OMS csv 30,934; completions csv 29,820 | yes |
| Distractors named, none labelled by file name | 2 or more in metadata.json | statewide_cooperative_reliability_2020-2024.csv and ami_momentary_events_2025.csv; names are neutral | yes |
| Distractors unused yet weighable, ruled out by a shipped fact | as stated | thread found both unused by any graded figure (weather also present); I did not separately test that either reproduces a graded quantity | yes (not independently tested) |
| Deliverables | 1 to 3, all in golden, no format family | 2 (docx, xlsx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | as stated | 2x4 grid, 3 districts x 3 measures, 3 districts' miles; prompt gives one decimal for rates and miles. Counts and customer-minutes are integers; the prompt does not state a rounding for them | yes |
| Prompt shape, rubric 25 or more criteria | identifiable, 25+ | shape 07 in metadata; rubric is generated and was not available to count | shape yes, rubric count unverified |
| Not LLM-generated; goldens real work products | as stated | thread found no authoring or provenance leakage; golden-realism is a separate gate | yes (thread read) |

## Gate G reconciliation
Match. Thread: mechanism decomposition_attribution, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card and note: gate_g and stump_strategy decomposition_attribution; Layer 2 family estimand_identification (the same thing named differently: a correct rise booked to the right driver; no planted defect). The declared distractors are not named by the thread as the surface read carrying the task. The easy routes the thread names (re-bid from the contractor timeline, catch-up from time since trim, forgetting ticket folding and major event days) are the note's default path (a re-bid), so the stump sentence agrees.

## Gate H reconciliation
domain: pass, layers: pass, decisive_step: analytical. This matches the note's three rules (Domain test, Layer 1 and Layer 2, decisive step: North's rate at the same time since trim for both contractors and against the ash within falling distance, sized against East and South). The thread's swap test and the note's hospital-wards swap agree. The thread calls the OPS-ROW-01 6.3 map from driver to programme a minor rule-application step; the note files the same map and has the decisive step upstream of it, so this is not a mismatch.

## Stump power (Gate F)
Decent per the thread: the contractor-timeline route to re-bid and the time-since-trim route to catch-up both fail the standardised comparison, and the ash gradient needs the FRAX to ASH join across two surveys. Not measured; the portal is the only stump evidence.

## Findings, ranked
1. Solution block 4 listed the memo's bar chart as deliverable answer "ask 3" although prompt.txt never asks for one. Main session has removed that line from submission.md; no prompt, figure or data change. Closed by that edit.
2. Mild fork in workings ask 1 (credit-memo treatment), closed by policy 4.3 and the dictionary. Optional: state netting by service month in the prompt. Not required.
3. Contractor ratios 0.98 and 1.01 reproduce only approximately with the thread's coarse bins. Both sit inside noise either way and the conclusion does not move.
4. Not checked by me: the rubric's 25-criteria count and a separate arithmetic test of each distractor.

## Next action for the author
Confirm submission.md block 4 now carries only the docx asks 1 and 2 and the three workings asks, with no rebuild needed, then continue stage 4 toward ship. Do not re-judge.
