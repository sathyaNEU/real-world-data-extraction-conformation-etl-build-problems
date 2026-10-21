# determinism-check report (pass 2), task481, 2026-10-20

Re-judge of the rebuilt pack (target.zip sha256 prefix ee83d775b423fed3) after the pass 1 FIX_NOW. Scratch: /tmp/determinism-check-task481-1792540294r2/. One thread, no retry.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every golden figure reproduces from the shipped files. 2025 = 5,254 and 2024 restated = 5,193 (5,200 to the nearest hundred), a change of +1 per cent. The methods docx pins the estimand: 13A offenses, one per victim, by report month in local time, deleted incidents excluded, 2024 restated to what NIBRS would have recorded. October to December 2024 (extract plus ucr_summary_class) gives each Return A line's conversion to 13A; the DVU log gives the January to September domestic mix of line 4e. The easy pooled October to December rate lands on about 5,400 and -3 per cent and is a measurably biased estimator (domestic victims 35.8 per cent of 4e in October to December against 29.1 per cent in January to September, converting at 21.2 per cent against 0.31 per cent). No other defensible estimator reaches 5,400. The pass 1 township-block fork is closed: the methods docx now files the shootings population within the City's limits and the quarter shot in local time, and the judge's pipeline reproduces all 12 quarters.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 2024 Return A 4a-4d actual | 4,829 | 4,829 (return_a_2024.xlsx col 4, 12 sheets; equals state table 8) | yes |
| 2025 13A, local report month | 5,254 | 5,254 (UTC 5,264; incident date 5,247; state repository 5,320 incl. deleted incidents) | yes |
| Q4 2024 13A | 1,204 | 1,204, equals the certification letter; Return A 4a-4d Q4 = 1,076, also equals the letter | yes |
| 4d to 13A share | 32.4 per cent | 135/417 = 32.4 | yes |
| 4a-4c to 13A share | 100.0 per cent | 659/659 = 100 | yes |
| 4e domestic to 13A | 21.2 per cent | 348/1,642 = 21.2 | yes |
| 4e other to 13A | 0.31 per cent | 9/2,948 = 0.31 | yes |
| DVU Q4 domestic 4E (not UNFOUNDED) | 1,642 | 491 + 535 + 616 = 1,642, equals extract family and intimate codes | yes |
| Domestic share of 4e | 35.8 / 29.1 (4,756 of 16,321) | Q4 35.8; Jan-Sep 4,756/16,321 = 29.1 | yes |
| Hierarchy-hidden (NS) victims | 202 | Q4 53 (46 robbery incidents, 7 homicides) + Jan-Sep 149 = 202 | yes |
| 4e converted to aggravated | 1,400 | 357 + 1,043 = about 1,400 | yes |
| 4d lost to simple | 1,238 | 1,831 x (1 - 0.324) = 1,238 | yes |
| 2024 restated | 5,193 | 5,192.98 unrounded | yes |
| Change | +1 per cent | +1 from the rounded or unrounded figure | yes |
| Shootings, 12 quarters (victims / shootings) | 110/105 ... 126/115 | all 24 values match from an independent pipeline | yes |

## Competing answers that survived
Main call (all close to the golden):
- Splitting 4d by domestic status gives 5,196.
- Scaling NS victims to total Return A lines gives 5,229.
- Scaling NS victims to robbery plus homicide gives 5,193.
- All three round to 5,200 and +1 per cent.
- The state's 5,320 is ruled out by the methods docx (the department's own extract, deletions removed).

Ask 2 conventions, each pinned by the docx, the prompt or the data:
- Each row's own inside_city flag, instead of the block's flag across all rows, moves 2023Q1 to 2024Q3 by 1 to 8 victims. The docx now files the City-limits population, so the block-level reading is the filed one.
- Skipping the ME drop shifts every quarter.
- Not converting UTC time shifts 2024Q4 to 2025Q4.
- Matching ME deaths on date, age and sex alone removes seven wrong people; block-level matching is the natural identity test.

Residual (ask 2 only, minor, no repair): no shipped file states that the shooting log's new-system rows (entered from 1 October 2024) carry UTC. It is derivable from the hour-of-day profile and from the 21 re-entered duplicate rows offset by exactly 5 hours, and is supported by the docx's "Ellsmere local time" instruction and the extract dictionary's UTC statement. Converting by report-number format and deduping gives practically the same quarters (171 against 169 in 2024Q3 before the ME drop). The judge advises adding no text to any shipped file.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 16 | yes |
| Formats | 3+ | 5 (csv, xlsx, pdf, docx, txt) | yes |
| Large file | 25,000+ rows | 119,713 (extract); DVU log 50,325 | yes |
| Distractors | 2+ named in metadata.json, none in a file name | 3 named (census, CAD calls, state repository download); judge found them present and unused | yes |
| Distractor weight | relevant, unused, ruled out by a shipped fact | repository 5,320 reproduces as an alternate 2025 count and is closed by the methods docx | yes |
| Deliverables | 1 to 3, all in golden | 1 (ellsmere_aggravated_assault.xlsx) | yes |
| Asks | multi-dimensional, unit and rounding stated | restated total to the hundred, counts whole, change whole percent; 12 quarters x 2 counts | yes |
| Prompt shape and rubric | shape identifiable, 25+ criteria | shape 07, 29 graded items (unchanged from pass 1; the rebuilt prompt.txt keeps the same asks) | yes |
| Reads as real | no LLM tells | judge found realistic mess, coherent dates, no authoring or benchmark disclosure | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection (stratified bridging estimator against a pooled rate under a mix shift), stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note and card declare composition_mix, Gate G etl_conformance, Layer 2 estimation_fit, with the same easy route (5,400, -3). These agree, and the classification is the same as pass 1. The declared distractors (census, CAD calls, state repository) are not named as the surface read; the repository's 5,320 is a wrong-basis alternate for 2025 closed by the docx. The judge states the numbers are correct as published and the difficulty survives clean data, because the domestic share of other assaults is genuinely seasonal. Passes Gate G, not borderline.

Gate H line: domain: pass, layers: pass, decisive_step: analytical. Field analysis: bridging a crime series across the UCR-to-NIBRS change with line-by-line, domestic-stratified conversion rates. Layer 1: UTC against local time, records-system renumbering, deleted incidents, a state repository that differs from the department's count, a township flagged differently across systems. Layer 2: estimating the NIBRS-basis 2024 total with stratified rates. The decisive step is a mix-shift judgment the data settle, not a textbook method applied without a data-settled choice. The design note's Three rules lines are consistent with this reading.

## Stump power (Gate F)
Moderate to good, per the thread. The certification letter's 1,204 against 1,076 invites the pooled-rate shortcut (5,400, -3 per cent, sign flips); the fix needs the DVU log joined to line 4e plus the hierarchy (NS) adjustment. Ask 2 adds independent chances to err. The thread rated this a little below pass 1's "Strong"; the main thread should weigh it with the scored readers' result.

## Findings, ranked
1. None at exclusion level. The pass 1 findings (township-block fork, step 6 wording) are closed.
2. Residual, minor: the UTC basis of the shooting log's new-system rows is unstated and derivable (ask 2 only). No repair advised.

## Next action for the author
Proceed to ship (stage 5). No determinism repair is needed and no further judge pass is licensed.
