# determinism-check report, task140, 2026-11-01 (stage 4 re-check, dictionary and files note removed from target/)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting (driver-based busiest-hour forecast solved jointly with the guarantee), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One judge thread (sonnet, medium) saw only a fresh unzip of the shipped target.zip (22 files, no data dictionary, no files note) and the five blocks. Every committed figure reproduced from the shipped files. The main call: 5,220 x 96 x 1.45 = 726,624 reservable; firm approvals 576,972; cell-store 2.947 per machine plus 0.2082 per batch core (17,081 hours, residual s.d. 62.0); solving 1.208 x B = remainder gives B of about 109,3xx to 109,6xx, so 109,000 under rounded or unrounded platform reservations and under a driver-based cell-ctl. Margin to the 110,000 boundary is at least about 150 guarantee cores. The removal of the dictionary opens no fork that moves a graded figure at the golden's rounding; the one reading that depends on column naming alone is the checkpoint state time (below).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Reservable cores | 726,624 | 726,624 (hardware plan rev 11 Dec, memo 1.45) | yes |
| Firm approvals | 576,972 / 577,000 | 576,972 (requests, budgets Jan 2027 MAD1 C-22 line, rate 7.42) | yes |
| Fit slopes | 2.94 / 0.208, s.d. 62.0 | 2.947 / 0.2082, 62.0 on 17,081 hours | yes |
| cell-store / cell-ctl | 38,000 / 2,000 | 38,019 / 1,999 | yes |
| Guarantee | 109,000 | 109,3xx to 109,6xx floor 109,000 | yes |
| Ask 3 (six teams, core-hours and share) | 121,800 0.40; 80,500 0.37; 48,500 0.31; 144,300 0.59; 72,000 0.49; 134,900 0.77 | exact match, all six | yes |
| Ask 4 (hardware / planned) | 750/850; 730/910; 660/880 | 748/851; 731/909; 662/883 | yes (to nearest 10) |
| Ask 5 (eleven charges) | per submission | all eleven match to nearest 100 | yes |
| Ask 6 | 577,000 + 40,000 + 109,000 | 726,000 of 726,624 | yes |

## Competing answers that survived
No defensible competing answer on the graded figures. Wrong routes, all separated by the data: 122,000 (quarterly-busiest-hour line), 120,000 (drivers, batch left at current level), 118,000 (machines only; residual s.d. 727 rejects it). Residual risks, not forks:
- Ask 3, checkpoint training state time: closed only by the column name state_snapshot_utc against committed_utc, now that the dictionary is gone. A commit-time reading gives ranking-ml 117,400 / 0.38% and shifts the other teams. This is the weakest point.
- Batch level at cell-store's busiest hour: closed by CS-3 5.2 and the data (batch at 99 to 100% of its guarantee at each quarter's busiest hour). The demand note's "0.6 x 149,100" would give 113,000 but is "for information" and contradicted by its own monthly core-hours.
- Resizes (cores_at_start with batch_resizes), RUNNING at snapshot (49 runs, effect under 0.01 points), UTC month (CS-3 1.2, policy 2.1, _utc columns; Madrid gives the same figures to 10) and directory joins: all closed by shipped text and values.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 22 | yes |
| Formats | 3+ | 5 (csv, xlsx, pdf, docx, json) | yes |
| Large file | 25,000+ rows | usage csv 239,470 rows | yes |
| Distractors | 2+, in metadata.json, not labelled by file name | mad1_cells_quarterly_summary, batch_training_demand_2027H1 named; names do not label them | yes |
| Distractor behaviour | unused, weighable, ruled out by a shipped fact | demand note (0.6 x 149,100) ruled out by its own monthly core-hours and CS-3 5.2; quarterly summary unused | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pptx), asks 1 to 6 in golden | yes |
| Asks | multi-dimensional, unit and rounding stated | six teams, three months, eleven tenants; rounding in the prompt | yes |
| Prompt shape and 25+ rubric criteria | identifiable, 25+ | shape is "other" in metadata; criteria count not verifiable by me (rubric is generated, ~35 gradable figures in the golden) | not verified |
| Realism | no LLM tells, goldens real | judge found no authoring language, dates coherent; golden realism not re-read here | yes (judge) |

Stale-text finding: DESIGN_NOTE.md still describes 24 files in six formats and a README/dictionary in places; metadata.json says 22 files, five formats. Housekeeping only.

## Gate G reconciliation
Thread: mechanism forecasting, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: family allocation_constraints on a General Statistics regression, stump sentence 122,000 trend route against 109,000 joint solve. Same trap named (storage service forecast on its history instead of its drivers, solved jointly with the guarantee). Family labels differ in wording only. Neither distractor is named as the surface read carrying the task; the thread cites the demand note only as a residual risk. The note lists the wrong routes as 122,000/119,000/111,000/106,000; the thread found 122,000/120,000/118,000 (and 106,000 from the submission). Method labels differ, goldens and the stump agree. No mismatch finding.

## Gate H line
domain: pass | layers: pass | decisive_step: analytical (matches the note and the card's analytical class). The thread did not class the step analytical merely because the method is standard: CS-3 4.1 files "use forecast" without a method and the data separates the candidates.

## Stump power (Gate F)
Moderately high on the main call: the trend line is clean historically (batch 55 to 58k, smooth machines) and fails only on the 4,640 to 5,220 machine step and the batch doubling; the driver fit is discoverable only by regressing on both drivers. The coupling is a textbook-adjacent regression, so a strong solver can land it (stumping 1.3 consideration for the main thread against the note's ladder). Asks 3 to 5 add multi-source reconstructions (restore-checkpoint losses, asset-id joins, reconciler apply times).

## Findings, ranked
1. Ask 3 state-time reading rests on column names alone after the dictionary's removal (commit-time reading changes every team's figures). Optional pin: in the prompt, count losses from the training state each run was restored from. Taking it needs a prompt rerun and a voice-check.
2. CS-3 3.1 says the request window opens six weeks before the quarter (20 Nov), the ops log shows 16 Nov and search-api filed 17 Nov; no figure affected.
3. DESIGN_NOTE.md file count and format list stale against the shipped pack.

## Next action for the author
Ship as is; if hardening is wanted, add the single phrase in finding 1 to prompt.txt, then re-run voice-check and the judge once.
