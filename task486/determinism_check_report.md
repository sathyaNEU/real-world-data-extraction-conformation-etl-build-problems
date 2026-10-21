# determinism-check report, task486, 2026-10-21

## Verdict
NOT_DETERMINISTIC (competing_defensible_answer on asks 1 and 2, the census counts; asks 3 and 4 reproduce)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The ask is the 60+ and 75+ counts per provider area. AP-27-02 s.3 says only that they are "estimated from the 2020 DHC release". The pack ships the published block-level P12 (dhc2020_kelvane_blocks_sex_by_age.csv), which sums exactly to every block group. Summing the blocks inside each area is a literal, defensible reading and gives North 850/250, East 590/210, South 860/290, West 1,100/330, Fallowmere 4,840/1,590, Wickmoor 15,380/5,070. The golden discards the block ages inside the 12 cut block groups and splits the block-group count by H1 housing units (North 700/200, and so on). No shipped file selects that over the block sum; the bulletin says only that small-area counts are noisier and housing units are invariant, and the same noise note applies to block groups. Six of 12 rounded figures differ by 100 to 150, against a "nearest ten" ask. A third reading (split by block population) gives yet another answer. Two soft forks on asks 3 and 4 (duplicate-upload and HOT cap rule; weaker death-match basis giving 625 clients) are closed only by inference or by the literal reading and are not decisive.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| County 60+ / 75+ | 23,621 / 7,751 | same (block groups P12_018-025, 042-049 / 023-025, 047-049; blocks sum equals block groups) | yes |
| Cut block groups | 12 of 62 | 12 (205 blocks with a 2023-07-01 assignment) | yes |
| Area counts, housing-unit split | Wickmoor 15,580/5,150 ... West 1,060/310 | all 12 reproduced | yes (under the golden's method only) |
| Rural-side published blocks in cut groups | 695 / 262 (split about 370 / 120) | 695 / 262; 374 | yes |
| Meals | 221,098 (139,058 / 40,951 / 9,793 / 8,883 / 9,855 / 12,558) | same, after dedup and HOT cap, by client home_block area | yes, with an inferred rule |
| Active clients | 616 (397/114/25/22/27/31) | 645 open less 29 dead through current and prior registry numbers | yes (literal reading) |

## Competing answers that survived
1. Census (decisive): block sum (North 850/250) against block-group count with housing-unit split (North 700/200); also block-population split. Rural-side cut blocks hold 3.7 residents per housing unit against 2.2 in uncut rural blocks, so the choice is live. Shipped rule meant to close it: none.
2. Meals duplicate rule (minor): the field guide says "one row per item handed over"; the dedup and HOT cap are inferred. Raw row count gives a different total.
3. Death-match basis (minor): SSN-only or ignoring prior-number links gives 625; 616 is the literal reading.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 21 | yes |
| Formats | 3+ | 5 (csv, docx, pdf, txt, xlsx) | yes |
| Large file | 25,000+ rows | hdm_route_delivery_log_fy2026.csv 186,886 (blocks file 130,594) | yes |
| Distractors named in metadata.json, none by file name | 2+ | 3 (address points, ACS B01001, licensed residential care) | yes |
| Distractor weighs, unused, ruled out by a shipped fact | yes | address points split gives 830/810 (same drift); ACS is another period and concept. Not too load-bearing, but the judge found the unfiled block sum, not a distractor, is the competitor | yes |
| Deliverables | 1 to 3 | 1 (xlsx), all asks in the golden | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 6 areas x 4 quantities, rounding stated | yes |
| Prompt shape and 25+ criteria | identifiable, 25+ | shape 14 per metadata; rubric is generated later, not checkable here | not checked |
| Reads as real, not LLM generated | yes | judge found none | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and metadata: the stump is the estimation choice of level and splitting measure (analytical, no decoy). Match on type. The declared distractors are not the surface read carrying the task. The mismatch is on forcing: the design note's own Not-rule-application line says the choice is "an estimation choice no document makes", which is exactly why a rigorous solver can legitimately file the block sum. The note's case that the block sum is wrong rests on a bias the pack does not document in a way that separates the candidates.

Gate H: domain pass, layers pass, decisive_step analytical (thread); the note's Three rules agree (analytical). Not a mismatch, but analytical and unforced.

## Stump power (Gate F)
Real but invalid until the estimand is pinned. A stumped solver would be right on a defensible reading rather than committing a provable error. The housing-unit split is the field's textbook areal-apportionment method, so a strong solver who reaches the block-group level lands the golden.

## Findings, ranked
1. Census counts: block sum is an equally literal answer; no shipped selection criterion. SEND_BACK.
2. Meals dedup and HOT cap are inferred, not filed (soft).
3. Death-match basis not filed (soft; literal reading holds).

## Next action for the author
Close the census fork by filing the WHAT, not the HOW (CLAUDE.md rule on determinism repairs): add a selection criterion the data can apply, for example ship a documented error or accuracy measure for block and block-group ages (or state in AP-27-02 s.3 that counts are to be taken from the finest level whose published accuracy meets a stated bar), so the block sum is disqualified by a shipped fact while the split method stays open between candidates the data separate. Filing "split by housing units" outright would turn the decisive step into rule application, and dropping the blocks age file would leave no stump. A rerun is required. Optionally file the duplicate-upload convention and the death-match basis.
