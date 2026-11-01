# determinism-check report, task447, 2026-11-01 (pass 3, reship after the leak-gate repair)

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (one cell-level unit pin in Exhibit C, sheet "Bayfield terms")
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every graded figure reproduces from the shipped files with the data dictionary and manifest gone. The call (proceed, +2.2M against the 2.0M line in OHCCR 4.06) is forced: professional repricing 609,633 plus referred repricing 1,599,572 gives 2,209,205. The figure stays at 2.2 under every defensible variant the judge ran (per-product shares 84 to 88, per-code shares 82 to 91, unrounded 85.9, with or without 2024 claims as "after" data).

One point is open. Exhibit C's Bayfield column "Percent of Medicare" holds 4.05, 1.55, 1.60, 1.15, 2.30. Read literally as percent, Bayfield's moved services price at about 1% of the golden amount, the referred part falls to about +0.03M, the total is about 0.64M and the review closes. That flips the main call and ask 2. The pack corroborates the multiplier reading (Bayfield's 2024 allowed amounts at Ledgestone sites run 1.46 to 7.29 times CY2025 Medicare; the other four carriers are about 6.7 times Medicare on MRI; the literal reading prices a brain MRI at 10.30 dollars), so the judge held DETERMINISTIC. But no sentence in the pack now states the unit, because the removed data dictionary was one of the places that did. The sheet's intro line ("paid at the percentage below of the Medicare amount") does not close it.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Professional repricing (23,970 lines, TIN 39-9943822, professional claims file, Exhibit C Professional) | 610,000 | 609,632.63 | yes |
| Referred repricing (8,029 lines, 2024 facility file, net of voids/replacements, paid by 30 Jun 2025) | 1,600,000 | 1,599,572 | yes |
| Total 2026 increase | 2.2M | 2,209,205 | yes |
| First-tier or untiered move share | 86% | 85.9% (86.1% with 2024 claims) | yes |
| Second-tier move share | none | -0.1% | yes |
| Bayfield Value Tier PPO Ledgestone tier from 2025 | first | first (2025 and 2026 filings) | yes |
| Ask 3 Manitowoc imaging / endo / arthro | 3,269 40.6 / 1,574 52.9 / 328 42.7 | 1,328/3,269; 833/1,574; 140/328 | yes |
| Ask 3 Kewaunee imaging / endo / arthro | 1,008 45.4 / 444 64.0 / 97 41.2 | 458/1,008; 284/444; 40/97 | yes |
| Ask 4 primary care B / L | 35.0 / 7.6 | 35.0 / 7.6 (39,070 visits) | yes |
| Ask 4 gastroenterology | 41.8 / 4.0 | 41.8 / 4.0 (1,468) | yes |
| Ask 4 orthopaedics | 35.7 / 3.7 | 35.7 / 3.7 (3,724) | yes |
| Ask 4 cardiology | 71.9 / 7.6 | 71.9 / 7.6 (1,538) | yes |

## Competing answers that survived
1. **Bayfield unit (decisive).** Multiples (4.05 times Medicare): +2.2M, proceed. Literal percent (4.05%): +0.64M, close. No shipped sentence closes it. Close it in the cell or header.
2. **Bayfield Value Tier PPO share (smaller).** 4.05 says a share is estimated per service and product, but Bayfield Value Tier PPO has no first-tier history of its own (Ledgestone was tier 2 through plan year 2024). Taking its own history gives 0 for it, referred about 1.0M, total about 1.6M, close. The 4.04(b) and 4.05 phrase "as the product stands in the projection year" forces the golden reading and the judge judged it closed, but a sentence would help. Optional; filing it must state the WHAT (placement in the projection year), not the method.
3. **Frequency codes 1, 7, 8.** Undefined now, but the structure fixes them and A2 and 4.02(c) say "latest version, net of voids". No second figure opens.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 (the judge wrote 15; the zip and metadata.json list 17) | yes |
| Formats | 3 or more | 4 (csv, json, pdf, xlsx) | yes |
| Large file | 25,000 rows or more | eligibility 102,665; professional 69,086; 2024 facility 67,976 | yes |
| Distractors | two or more named, none labelled by file name | hcris_hospital_outpatient_extract_fy2023.csv and apcd_medicare_advantage_facility_claims_2024.csv named in metadata.json; neither name says "distractor"; the MA file is not commercial (4.02(b)), HCRIS answers no graded quantity | yes |
| Deliverables | 1 to 3, all in the golden | 1 (N25-014_preliminary_review.pdf), present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 6 county-by-line cells and 8 specialty-by-system shares, one decimal; the prompt states unit and rounding | yes |
| Prompt shape, rubric 25 or more | identifiable, 25 or more | shape 07 (grid of cells); about 30 gradable items on paper (call, change, 6 counts, 6 shares, 8 shares, components); the rubric is generated and was not seen | yes (on paper) |
| Not LLM-read, goldens realistic | yes | no authoring language in the bundle (judge); I did not open the golden PDF | yes (judge) |

## Gate G reconciliation
Judge: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note's stump sentence names the same thing: pooled, carrier or product shares miss the tier gate, and the capture follows each patient's tier for the acquirer (Wolf River's 2024 re-tiering inside the history; Bayfield first-tier from 2025). Match, no mismatch finding. The declared distractors (MA claims, HCRIS) are not the surface read carrying the task. The judge names the pooled all-patient share (about 1.4M, close) as the easy route, which is the note's own default path, and not a distractor.

Gate H: judge domain pass, layers pass, decisive_step analytical. The note's `## Three rules` agrees (decisive step: tier placement gates the share, so it is 86 or nil; no filed sentence names tier placement). Match. The judge classed the step analytical on the substance (a conditional share estimated from past acquisitions), not because the method is the field's standard.

## Stump power (Gate F)
Strong on the main call on paper. Pooled gives about 1.4M and a closed review; tier-blind 86% gives 2.3M (right call, wrong figure); dropping Dr Brown gives 1.85M and close. Variants that keep the tier gate stay at 2.2, so the call is landable by a solver who finds the gate, and the main thread weighs that against the ladder. The A5 join rules and the tier-timing offset (July benefit period, Norbridge EPO first from plan year 2024) add depth without a planted rule. The Bayfield unit fork is not stump power. It is an unclosed reading and must be pinned.

## Findings, ranked
1. FIX_NOW. Bayfield "Percent of Medicare" unit is not pinned and the literal reading flips the call. Fix: relabel the column as a multiple of Medicare (header "Multiple of Medicare amount", or percent values 405, 155, 160, 115, 230). No claim row or analytic surface moves.
2. Optional. One sentence in 4.05 or A5 that a product placing the acquirer in its first tier takes the share observed for first-tier patients. The "as it stands" clause already implies it. Keep it to the estimand.
3. Note. The judge did not run the cross-batch check, so no duplicate finding is claimed here.
4. Note. The judge's count of 15 files is wrong (17 shipped); no effect on any gate.

## Next action for the author
Edit the Bayfield terms sheet in the generator so the unit reads unambiguously as a multiple of Medicare (and apply the same wording wherever the sheet text repeats it). Rebuild twice for byte-identity, then re-judge once, since this is a FIX_NOW. The /fix-rubric work on the ask layer is separate and must not touch the main call.
