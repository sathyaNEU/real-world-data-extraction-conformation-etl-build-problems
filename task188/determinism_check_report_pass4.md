# determinism-check report, task188, 2026-11-03 (pass 4)

Record note: pass 3 on this folder belongs to architecture 1 (West Nile). This pass checks architecture 2 (cash review, zip sha256 prefix 192490f7). The judge thread was spawned by the main session from /tmp/determinism-check-task188-r1/judge_brief.md (no Agent tool in my runtime); its verdict is /tmp/determinism-check-task188-r1/verdict.md.

## Verdict
NOT_DETERMINISTIC (competing_defensible_answer, confined to supplementary ask 4's night-depository column); no SOLUTION_WRONG. Main call and asks 1 to 3 deterministic.
**Disposition:** SEND_BACK per the thread. The defect is a data repair in one ask file (rebuild, not a redesign): the main call, the stump and the other graded figures stay frozen. The author may treat it as a generator fix plus one re-judge.
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Segment postings of transit 19004 are placed at a depository through cit_pickup_manifests_2026.csv (bag_number + pickup_date). The manifest lists some bag-days at two different depositories on the same day (the thread found 8 bag-days / 32 NDEP postings in 2026; my own count of the whole file is 16 bag-days with more than one depository). No shipped file or rule picks between the listings: not the programme, not the bag register, not pickup time, manifest size, number or seal. The golden night-depository column reproduces only under "keep the last listing in file order"; other tie-breaks move six of nine thousand-rounded cells (Newton, Richmond Centre, Coquitlam, Uptown, Langley, Willowbrook). Guildford, Metrotown and Ladner reproduce. The design note never mentions these double listings (SF19 and ask B describe only the one-listing-per-bag reading), so they look unintended generator output, not a declared device.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Cash paid in 2026 Seaview / Pacifica | 477,000 / 299,000 | 476,947 / 299,345 | yes |
| Card settlements | 321,676 / 183,043 | same | yes |
| Median cash per card dollar grocery / quick service | 0.379 / 0.392 | same | yes |
| Produced (25k bins) | 125,000 / 75,000 | 121.9k / 71.8k | yes |
| Excess (25k bins) | 350,000 / 225,000 | 355.0k / 227.6k | yes |
| Multiple of produced | 2.91 / 3.17 | same | yes |
| Largest non-qualifier | Sunrise Fresh Market | Sunrise (0.75x, excess 471.8k) | yes |
| LCTR required by quarter | 25 / 40 / 44 / 38 | same | yes |
| LCTR filed | 19 / 44 / 44 / 37 | same | yes |
| LCTR late | 2 / 6 / 11 / 9 | same, under the Pacific receipt day reading | yes |
| ATM cash, nine branches | as submitted | all exact | yes |
| Night depository: Guildford, Metrotown, Ladner | 1,832 / 1,208 / 1,064 | same | yes |
| Night depository: Newton, Richmond, Coquitlam, Uptown, Langley, Willowbrook | 1,494 / 1,631 / 1,569 / 1,000 / 441 / 488 | match only with last-listing-in-file-order; other tie-breaks give 1,489-1,496 / 1,631-1,639 / 1,565-1,569 / 999-1,003 / 440-441 / 485-488 | no |

## Competing answers that survived
- Night depository, six branches: last listing in file order (golden) against first listing, home listing, or counting both. Closed by no shipped rule. Needs the manifest repaired.
- Lateness on transaction_date instead of the Pacific receipt day gives 1 / 1 / 2 / 6 against 2 / 6 / 11 / 9. Residual, not disqualifying: programme 6.2 ("the day on which the first cash it reports was received") and section 5 support the golden; the due-day time zone is not stated.
- Cash-produced estimator unfiled: referral set and Sunrise answer hold under mean, pooled, trimmed, q25, q75 and all-segment median; the 25k rounding absorbs most variants but q25 and an all-segment median move the excess to 375k / 225k. Matches the design note's standing family (F1 to F4), which holds a printed bin for the chosen family.
- Platform payouts as not cash-producing rests on description text only (DASHDROP CANADA PAYOUT, PLATEPASS REMIT).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | csv, xlsx, pdf, docx | yes |
| Large file | 25,000 rows or more | postings 321,917 rows | yes |
| Distractors in metadata.json | 2 or more, none named in a file name | 3: str_submissions_2025_2026.csv, fiu_case_register_2026.xlsx, international_wires_2026.csv; names do not label them | yes |
| Distractors unused yet weighable | yes | thread found all three present and unused by the solution; none answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 3 (docx, xlsx, png), all present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | branch and quarter grids; rounding stated in the prompt | yes |
| Prompt shape and rubric | identifiable, 25 or more criteria | shape `other`, 49 criteria by the note's arithmetic (not independently regenerated) | yes |
| Reads as real, not LLM generated | yes | thread saw no authoring disclosure; golden realism not re-judged here | yes (unchecked beyond the thread) |
| Prompt | one paragraph, under 1,000 characters | 946 characters | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical, driver "inflow beyond what the unit's own activity produces; peer, declared and other-inflow benchmarks move with the anomaly". Design note ladder: declared activity (rung 0), peer mean and turnover band (1), cash share of credits (2), non-cash credits (2b) all refer the wrong set or nobody; rung 3 (card plus platform payouts) refers Seaview alone. These match the thread: the easy routes are the card's. The declared wrong-basis distractor is the card-plus-platform basis, which the thread names as the surface read that clears Pacifica but does not carry the task: the call needs the counter-card benchmark, so the distractor is not too load-bearing. The three declared distractor files are not the surface read. No mismatch found. The card carries no mechanism or stumping_family fields, so those two compare by the note's strategy line (`population_selection`, estimand identification), which the thread's method_or_model_selection matches in substance.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. Thread and note agree: Layer 1 is the UTC against business-date postings, relocated terminals and bags, the mixed-grain LCTR log; Layer 2 is the expected-cash benchmark from peer cash-to-card ratios.

## Stump power (Gate F)
Good per the thread. Turnover, peer-ratio, declared-activity and card-plus-platform routes refer nobody or Seaview only; the strong analyst must build a counter-trade benchmark from the acquirers' settlements. Caution for the main thread: the thread did not itself derive the benchmark without the hint of the filed estimand structure, and the ratio-of-card-settlements method is the field's standard peer-calibrated expected-activity estimate, so a strong solver can land it (stumping 1.3). The note's pair ceiling of 50.5 holds only if the ask devices stay hard; this fix must keep ask B's night column device intact (the bag-to-depository placement through the manifest) while removing the ambiguity.

## Findings, ranked
1. Night-depository column of ask 4 (six of nine branches) is determined only by an unfiled "last listing wins" tie-break across 8 same-day double listings in cit_pickup_manifests_2026.csv; competing_defensible_answer. Fix: remove the second listing of each double-listed bag-day (or add a field that makes the true depository derivable), regenerate the night column in golden, workbook, submission and the note's ceiling.py figures.
2. The design note's SF19 closure and ask B description do not account for double listings, so the fork table is incomplete for this term; add a row and assert it in checks.py once repaired.
3. Count discrepancy to settle in the generator: the thread reports 8 double-listed bag-days on 2026 night postings, my whole-file count is 16 with more than one depository; the fix should cover the whole file.
4. Lateness time zone for the due day is unfiled (residual); optional one-sentence close in programme 6.2. The golden is the better-supported reading.
5. Estimator for produced cash is unfiled and not decisive at the printed bins; do not file the HOW (it would turn the decisive step into rule application).
6. Platform payouts as non-cash rests on description text; acceptable domain knowledge, noted only.

## Next action for the author
Repair cit_pickup_manifests_2026.csv in the generator so each (bag_number, pickup_date) lists one depository, regenerate ask B's night-depository figures in the golden, workbook and submission under that rule, keep the main-call data frozen, rebuild twice byte-identical, and re-judge once.
