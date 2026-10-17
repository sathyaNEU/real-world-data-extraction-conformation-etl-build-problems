# determinism-check report, task264, 2026-10-17

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Executed literally, resolution 14/2026 counts residents once each, estimated from the survey. The exit survey is size-biased by visit frequency, so each interview counts as weight/Q9. That reproduces the golden (50.60% top three; nine levies summing to 7,416,300) to the pound. The main call and asks 1-4 are forced. One real residual fork sits in ask 5 (the bank cut-off basis), plus minor wording defects in the solution blocks. No data change is needed.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Interviews | 4,470 | 4,470 (2,349 + 2,121), keys unique | yes |
| Kept interviews | 3,973 | 3,973 (473 OUT, 24 NK dropped) | yes |
| Residents total | 271,900 | 271,888; all nine councils to the nearest hundred | yes |
| Top-three share | 50.6% (137,600) | 50.60% (137,581) | yes |
| Nine levies | golden schedule | 1,250,310; 1,525,314; 977,169; 717,236; 743,901; 650,135; 549,836; 513,321; 489,078; sum 7,416,300 | yes |
| Wrong answer 85.1% | expanded visits | 85.09% | yes |
| Wrong answer 53.4% | 1/q9 unweighted | 53.41% | yes |
| Wrong answer 24.9% | visits / mean q9 | 24.94% weighted-mean variant; unweighted mean gives 25.10%, median 26.4% | yes, variant-dependent |
| Parking income net of VAT (4 parks) | golden | 439,313; 543,124; 449,759; 400,761; total 1,832,957 | yes |
| Vehicles (4 parks) | golden | 171,505; 134,156; 166,487; 126,385; total 598,533 | yes |
| Levy collection | golden | all paid in full except Chaldale (paid 510,932, owed 3,455) | yes, by value date |

## Competing answers that survived
1. Bank cut-off basis (ask 5), the one real fork. All nine Q4 instalments are posted 1 April 2026 with value date 31 March 2026. The prompt says "paid ... by 31 March 2026" and names no basis. Value date gives the golden. Posting date leaves every council owing its full Q4 instalment (Keldmere 166,072, Chaldale 132,054), so ask 5 flips for all nine. The design note's D8 relies on this being closed by the reader, but no shipped text states it.
2. Register-literal placement (PM-2103, C-07, C-09). The register shows current status only. Read literally it gives Gorthfield 416,922 / Daskbeck 565,515 and Daskbeck vehicles 208,402 / Lockshaw 246,565 / Thruscote 46,307. The takings and ticket-to-count ratios contradict these, so the golden is forced from data, but no document says the placements are to be inferred. An ask-side device, not a surviving alternative.
3. Hundreds-rounding. The nine rounded residents sum to 271,800, against a stated 271,900. Levies from rounded counts differ by up to about 1,340 pounds. The resolution's paragraph 5 supports the unrounded share, but a one-line note would pin it.
4. VAT rate. 20% is recoverable from the app lines (sessions x tariff / 1.2 exact). Closed by the data.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 19 | yes |
| Formats | 3 or more | 3 (csv x12, xlsx x5, pdf x2) | yes |
| Large file | 25,000 or more rows | 246,404 rows (pay machine), 53,063 (hourly counts) | yes |
| Distractors | 2 or more in metadata.json, none named by file name | 3 (annual_permits, population_estimates, supplier_payments); file names carry no label | yes |
| Distractors unused and relevant | unused, weigh, ruled out by a shipped fact | judge found none used (only Appendix B population share in the bar chart) | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx), both present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | per-council / per-park, one rounding sentence | yes (see finding 3) |
| Prompt shape and 25+ criteria | identifiable, 25 or more | shape identifiable; the design note says the pair ceiling is to be rerun on the generated rubric, so the count is unconfirmed | not verified |
| Reads as real, not LLM generated | yes | judge found no authoring disclosures; realistic exports | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no.
Design note and card: stump_class analytical, with an analyst test ending on 24.9% against the golden 50.6%. The design note's Layer 2 is "estimation_fit". The card's mechanism and stumping_family fields are null, so there is nothing to mismatch on. The decisive step matches exactly (weight over own Q9, residents once). The declared distractors (permits, population estimates, supplier payments) do not carry the task. Nothing in the pack ranks the candidates wrongly. The three wrong routes (85.1, 24.9, 53.4) appear only as the judge's reconstructions, not in any file. Gate G: pass, no mismatch.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. Matches the design note's `## Three rules` (domain test, Layer 1 and Layer 2, decisive step). The judge's swap test fails to read the same, as the note's does.

## Stump power (Gate F)
Moderate on the main call. A frequency-aware analyst reaches 50.6%. The 24.9% route (visits / mean frequency) is the tempting wrong one, and the other two are cheap to dismiss. The asks carry the heavy reconciliation (PM-2103 relocation, C-09 halving, C-07 swap, C-05/C-10 overlap, duplicate uploads, shared-service remittance splits, Chaldale's short payment), so the top two should not average well even if the call is cleared.

## Findings, ranked
1. Ask 5 cut-off basis is open (value date against posting date); posting date flips all nine councils. Add "by the bank's value date" (or "credits value-dated on or before 31 March 2026") to prompt.txt. This files the WHAT (the date basis), not the HOW. The change also touches design note device D8, which currently relies on the reader choosing the column.
2. Solution blocks: step 7 states the PM-2103 and C-07 relocations and C-09 "in and out" as facts. No shipped file says so; reword it to say they are established from takings and ticket-to-count ratios. The "24.9 per cent" in FINAL_RECOMMENDATION holds only for the weighted-mean variant (24.94%), so attribute it to that variant.
3. Optional: pin the levy rounding ("from unrounded estimates") in the levy sentence. The 271,800 / 271,900 sum mismatch invites a rounded-counts reading.
4. Optional: the register-literal placement fork is closed only by inference from data. This is an ask-side device and is acceptable, but confirm the write-up says how it is derived.
5. Rubric count (25 or more criteria) not verified by this pass.

## Next action for the author
Edit prompt.txt ask 5 to name the bank's value date as the cut-off basis. Reword solution step 7 and the 24.9% attribution in submission.md. Then rebuild and re-judge once, via /fix-determinism if the pipeline requires it.
