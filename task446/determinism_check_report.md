# determinism-check report, task446, 2026-10-21

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (design note: forecasting), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Pass: stage 4 re-judge after the FIX_NOW (CRM-07 5.2 now files the closed cohorts "taken together"). One isolated sonnet thread, fresh unzip of target.zip (sha256 06a4c8d5...01bc6, 17 members) at /tmp/determinism-check-task446-r3/target/. The brief and the thread's verdict.md are in that folder.

## Why
Every golden figure rebuilt from the shipped files: 913 groups, 165 flagged, 127 flagged on a customer, cohort rates 120/240 = 50.0%, 11/176 = 6.25%, 50/3,092 = 1.62%, 77.97 expected arrivals (78), and all five band rows. The cohort window is now closed by the filing: the cohort-window variants all land on 78 (77.95 to 78.23). The only structure stable across the four closed cohorts is whether the flag was raised on a member the bank lends to. Every variant that keeps that split gives 78.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Book at 30 Sep 2026 | 913 | 913 | yes (group register, watch-list history) |
| Flagged / on a customer | 165 / 127 | 165 / 127 | yes (ews signals, GLEIF RR, obligor master) |
| Cohort rates | 50.0 / 6.25 / 1.62% | 120/240, 11/176, 50/3,092 | yes |
| Expected arrivals | 78.0 | 77.97 | yes |
| Bands, groups | 201/304/248/120/40 | same | yes |
| Bands, committed GBP m | 499.9/3,112.0/6,936.6/8,402.7/6,712.2 (25,663.4) | same | yes |
| Bands, flagged | 34/54/46/20/11 | same | yes |
| Bands, arrivals | 16.2/25.8/21.9/9.0/5.1 | same | yes |
| Bands, exposure arriving GBP m | 38.5/257.1/596.8/576.3/826.8 (2,295.5) | same | yes |
| Back-test largest miss | 3.9% split, 14.4% pooled | 3.9% / 14.4% | yes |

## Competing answers that survived
None that survive. Rejected by the data: pooled hit rate plus unflagged rate 64; base rate 47; capture/false-alarm with this year's flag share 136; latest cohort only 65 (back-test misses 12.9% to 14.4%).
Small residual forks, none moving the call except the first two (73.7 to 73.8 against 78):
- CLOSED customers treated as non-customers gives 74. Closed customers have no facility and 498 of 512 sit in ended groups, so counting them at the cohort date is the correct historical reading.
- Customer defined by an in-force facility on the 1 Oct extract gives 73.7. The extract holds no purged older facilities, and the obligor master is the file's own customer list.
- Exposure arriving as arrivals times band mean exposure gives 2,401.1 against 2,295.5. Standard 5.2 asks for the expected groups' exposure.
- Skipping the 22 duplicate removals moves band rows only (199/302/250/118/44), not the 78. The duplicates are identified by identical user, timestamp and limit histories; no document names double booking. Watch item on the band rows only.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 | yes |
| Formats | 3 or more | 6 (csv, xlsx, pdf, docx, md, txt) | yes |
| Large file | 25,000 rows or more | ews_entity_signals 125,975 rows | yes |
| Distractors | 2 or more in metadata.json, none labelled in a file name | internal_rating_master_scale_2026.xlsx, group_economics_uk_outlook_oct2026.xlsx; neither named in a file name as a distractor | yes |
| Distractor weight | unused by solution, relevant, ruled out by a shipped fact | the rating file is current-date only (look-ahead, cannot be back-tested); outlook is macro, does not reproduce a graded quantity | yes |
| Deliverables | 1 to 3, all in the golden | xlsx and svg, both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | band table of 5 columns by 5 bands plus total; whole number, one decimal, GBP m to one decimal in prompt | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 05 (allocation to a fixed total); 25 band figures plus total row, heading, chart items | yes |
| LLM-generated look | none | none seen by the thread; golden realism passed at stage 3 | yes |

Licence and source records are in metadata.json (CC0-1.0, constructed); the thread could not check them from inside the package.

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and Gate G section: mechanism forecasting, analytical_non_defect, no, no. The match is full (the thread's label is a finer name for the same forecasting-model choice). The thread names pooled-rate (64) and base-rate (47) routes as the naive reads, not the declared distractors, so neither distractor is too load-bearing. No shipped artifact ranks or forecasts. The card file was not at cards/task446.json in this checkout, so stump_class, analyst_test and domain_test were taken from the design note's Three rules section, which matches the thread.

Gate G classification: analytical_non_defect, surface_read_dependency no, sole_data_defect no.

## Stump power (Gate F)
Good. A strong analyst applying the standard's 4.3 hit rate and unflagged rate files 64; one using the base rate files 47. Only the cohort-by-cohort stability check exposes the mix shift (customer share of flags 58% historically, 77% now). The thread did not class the decisive step as the field's standard method applied without judgment: the segmentation had to be found, and the data separated it. Expect partial failures, with the 22-duplicate and UK-time cut-off devices thinning the asks.

## Findings, ranked
1. None blocking.
2. Watch: the 22 double-booked facilities are identified by the data pattern alone; the 78 is unaffected, only band rows.
3. Watch: licence and source record not verifiable from inside the package.

## Next action for the author
Proceed to stage 5 ship; no repair needed.

Gate H line: domain pass, layers pass, decisive_step analytical (matches the design note: the flag-source segmentation validated leave-one-cohort-out is the decisive step; Layer 1 mess does not carry it).
