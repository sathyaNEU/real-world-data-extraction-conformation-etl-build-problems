# determinism-check report, task471, 2026-10-20 (run v5r3, target.zip sha256 5b89c291378b1d76)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (correlation-bias correction of the dual-system estimates against a demographic-analysis benchmark; etl_conformance on the asks), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated thread (sonnet, medium, one pass, scratch prefix only) rebuilt all 16 organiser counts, 16 added counts and 16 died-removal counts from the fresh unzip, and all matched the golden. The totals also matched: 3,329,031 electors, 3,593,178 DSE adults, 166,710 new electors and 33,188 death removals. The main call is forced: the men aged 18 to 49 are about 4% short of the demographic-analysis sex ratio, while the women and the men aged 50 to 64 agree to within 0.1 to 0.6%. The ask conventions each have an in-data test. Two residual forks remain, both confined to the asks (see Findings).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Electors, ADDRESS_TYPE R, via electorates_and_regions.csv (roll_at_close_of_census_day_2025.csv) | 3,329,031 | 3,329,031 | yes |
| DSE adults (methods report cells, census xlsx incl. "100 and over", pes_2025_census_records.csv, pes_2025_people.csv) | 3,593,178 | 3,593,178 | yes |
| DSE men per woman 18-24, 25-34, 35-49 | 1.01, 0.99, 0.97 | 1.006, 0.991, 0.973 | yes |
| DA men per woman, same groups (births, both deaths files, movements, 2025 provisional period included) | 1.04, 1.03, 1.02 | 1.043, 1.031, 1.020 | yes |
| Adults after correction | about 3.63M | about 3.633M | yes |
| 16 organisers (largest remainders, minimum 2) | 27, 20, 25, 26, 29, 5, 11, 12, 7, 5, 4, 8, 6, 3, 8, 4 | identical | yes |
| New electors, total and 16 regions | 166,710 | 166,710, all 16 equal | yes |
| Death removals, total and 16 regions (280 reversals netted) | 33,188 | 33,188, all 16 equal | yes |
| DSE as it stands | 26, 26, 28, 31, 4, 6, 4, 3 in the eight changed regions | identical | yes |

## Competing answers that survived
No forced fork on the main call. Two residual forks on the asks, both closed by shipped text or data:
- **Reversals after 30 June 2026.** 34 of the 280 reversals fall after the window. Counting only reversals inside the window gives 33,222 (up to 8 more in a region) against the golden's 33,188. Specification definition 4 says "later reversed" with no bound, and the extract runs to 30 September 2026, so the literal text favours the golden. The design note's fork row SF18 closes it the same way. It is closed but it is not a one-clause-proof pin.
- **Electorate numbering on the old platform.** The 2020-review numbering (roll_at_2023_general_election_by_electorate.csv) is not stated in any filed sentence. Reading R25- numbers through electorates_and_regions.csv instead moves all 16 regions on both asks (new electors by up to 604, deaths by up to 147). Two in-data tests settle it:
  - The correlation of old-platform DEL counts per electorate is 0.974 with the 2023 roll and 0.290 with the 2025 roll.
  - All 102 old-platform removals later reinstated on the new platform keep their region under the 2023 mapping, against 38% under the 2025 mapping.
  - The migration notes do mention the 2020 review's numbers.

The other conventions tested all produce distinct, ruled-out wrong answers: person as PERSON_REF (218,760), naive UTC (167,048 and 33,554), window from 4 March (167,001 and 33,203), no reversals (33,468), and reason 01 read as own request (22,612). Rounded ratios, other birthday mappings, a single 18-49 factor, and UTC+12 or +13 throughout all give the same organisers or counts. A men's factor of 1.01 moves one organiser from Rowanlea to Glenwhite. The remainder order has no tie (.598 against .381).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 20 | yes |
| Formats | 3 or more | 4 (csv 12, xlsx 4, pdf 4, docx 1) | yes |
| Large file | 25,000 or more rows | roll_transactions_2025_2026.csv, 362,786 rows | yes |
| Distractors | 2 or more in metadata.json, none named in a file name | subnational_population_estimates_jun2024.csv (wrong-basis), census_2025_field_operations_summary.pdf | yes |
| Distractor weighs but is unused | relevant, unused, ruled out by a shipped fact | the June 2024 estimates are ruled out by plan 2.1 (adults on census day); the thread found the field operations summary unneeded | yes |
| Deliverables | 1 to 3, all in the golden | 2 (CSV and PNG), both present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 16 regions by 3 quantities, whole numbers stated in the prompt | yes |
| Prompt shape and rubric of 25 or more criteria | identifiable shape, 25 or more | shape 05 (allocation to a fixed total); 16 regions by 3 values plus chart gives well over 25 gradable items. The rubric itself is generated elsewhere and was not inspected | yes |
| Not LLM-generated, goldens read as real work | none | the thread saw no authoring language; I did not read the goldens beyond confirming they exist | yes (provisional) |

## Gate G reconciliation
The thread's mechanism is method_or_model_selection with etl_conformance on the asks. It reads the decisive step as the correlation-bias correction against the demographic-analysis sex ratio. The design note's stump sentence says the same: the textbook dual-system estimate is wrong in eight regions because the census and the survey miss the same young men, and the men are raised to the sex ratio that births, deaths and border movements fix. The card's declared stump matches. The declared distractor (the June 2024 estimates) was not named as carrying the task, so the distractor is not too load-bearing. The thread's Gate H line (domain pass, layers pass, decisive_step analytical) matches the note's Three rules: its domain test and Layer 1 and Layer 2 split agree with the thread's. The note also records Layer 1 as asks-only for the platform mess. No mismatch.

## Stump power (Gate F)
The main call is analytical. A strong analyst who cleaned everything and read every rule can still file the dual-system estimates as they stand (8 regions wrong) or the census counts (14 wrong). The thread notes that the Lincoln-Petersen estimate, the cohort-component rebuild and the largest-remainder rule are textbook routes a strong solver reaches. It also notes that the shipped demographic-analysis series are an obvious cue, so a strong model may find the correction. I record this as a landable call: the library's methods are textbook routes (`stumping` 1.3), so the main thread should weigh it against the scored readers' result. Hardness on the asks is high, with five conventions that must all be right to hit all 32 counts. That hardness is Layer 1 and rule work, not the stump.

## Findings, ranked
1. **Electorate numbering is unfiled and settled only by data tests.** It touches every region on both asks and not the main call. Under the literal-determinism rule this is a convention the filed text does not state, though the data settles it twice. The judge classes it as a Layer 1 key mismatch, not an open fork. Optional pin: one clause in roll_platform_migration_notes.pdf naming the numbering. Not required for the verdict, and it would pre-disarm part of the mess.
2. **"Later reversed" has no stated bound.** The golden counts reversals anywhere in the extract (33,188). The window-only reading gives 33,222. The literal text favours the golden. Optional pin: one clause in the definition.
3. **Temporal oddity (minor, not exclusion-level).** pes_2025_methods_report.pdf is dated September 2025 and lists census_2025_usual_residents_by_region.xlsx, which is stamped "Released 18 November 2025".
4. Some REF_TXN values are malformed (for example "R25--006800"). They read as realistic noise.

## Next action for the author
No fix is required; proceed to ship. If you want to harden determinism at the cost of a rerun, add the one-clause pins in findings 1 and 2. Both change what solvers see, so a pin is not free.
