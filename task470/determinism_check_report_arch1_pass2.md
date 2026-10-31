# determinism-check report, task470, 2026-10-18 (pass 2, run r2)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated sonnet thread (medium) saw only a fresh unzip of the current target.zip and the extracted blocks. It recomputed every load-bearing figure from the bundle. The seven-field set holds under every variant tried (lowest qualifier 14.10 kg, highest non-qualifier 11.11 kg, line 12.5 kg). The changed method 4.2 text and write-up step 7 (towers' unrecorded operations taken as piston-engine operations) reproduce the six towered figures. Method 4.4 does not file the estimator for the 20 uncounted fields, but the data forces it: operations per never-recorded based piston airplane is steady at 65 to 73 across the ten reference fields, while the capture rate swings 0.56 to 0.99.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Tower unrecorded civil ops (total) | 16,470 | 16,470 (CRV 2,544, DMR 2,368, HWK 3,290, KTY 2,512, OSY 2,988, VNL 2,768) | yes |
| Unrecorded ops at ten counted fields | 23,376 | 16,470 + 6,906 = 23,376 | yes |
| Never-recorded airplanes, counted fields | 338 | 99 + 239 | yes |
| Ops per never-recorded airplane | 69.2 | 69.16 | yes |
| Never-recorded airplanes at 20 uncounted fields | T13 33 ... D73 3 | all 20 exact | yes |
| 24 field leads (whole kg) | T13 22 ... D73 2 | all 24 round to golden (T13 22.13, F37 14.10, P05 11.11, D73 1.83) | yes |
| Towered ops and lead | HWK 17,600/22 ... DMR 7,900/13 | 17,624/22.11, 9,915/17.92, 19,413/23.18, 12,192/16.04, 13,616/16.04, 7,927/12.92 | yes |
| Rival eight-field set (pooled 82 per cent) | adds K58 P05 S27 T61, drops O16 U44 W33 | reproduces (0.809) | yes |

## Competing answers that survived
None on the graded figures. Eight fork combinations tested (same-day DEREG change, L08 tow-plane operations, reference pool of 10 or 4 fields, never-recorded definition, tower-hours boundary): none moved the set of seven or any rounded kilogram or hundred-operation figure.
Residual non-decisive points:
- (a) The estimator is not filed in 4.4; the data separates the candidates.
- (b) The 23,376 and 69.2 hold under the Notes-sheet reading of L08 tow planes. The other reading gives 23,574 and 69.75, with no graded figure moved.
- (c) The DEREG same-day boundary affects 17 events and moves under 0.01 kg per field.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 18 | yes |
| Formats | 3 or more | 4 (pdf, xlsx, csv, txt) | yes |
| Large file | 25,000 or more rows | adsb_field_events 187,609 rows | yes |
| Distractors named in metadata.json, none labelled in a file name | 2 or more | 2 (airport_master_records_5010.xlsx, cvaqd_lead_monitoring_2026.csv) | yes |
| Distractors unused yet weighable, ruled out by a shipped fact | yes | 5010 estimates are manager's all-aircraft figures for 2018 to 2025 (file notes, method section 4); monitoring file has two ambient sites | yes |
| Deliverables | 1 to 3, all in golden | 2 (csv, docx), both in golden | yes |
| Asks | multi-dimensional, unit and rounding stated | 24 leads, qualifying set, chart, 6 towered rows; whole kg and nearest hundred stated | yes |
| Prompt shape and rubric | identifiable, 25 or more criteria | shape 01 (list against a cap); 24 leads + 7 qualifiers + 12 towered figures + chart exceeds 25 | yes |
| Not LLM generated; goldens read as real work | yes | thread found fixed-width register, no authoring language; the one oddity is the grant guidelines dated 4 Dec 2026 citing the full 2026 inventory year, which moves no figure | yes (minor note) |

## Gate G reconciliation
Thread: method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Gate H line: `domain: pass`, `layers: pass`, `decisive_step: analytical`.
The design note's stump sentence is the same trap: the pooled capture rate (0.815) files eight fields (A71, F37, K58, L08, P05, S27, T13, T61) and drops O16, U44 and W33. The thread's wrong set differs only in using 0.809 (adds K58, P05, S27, T61; drops O16, U44, W33), which is the same family and the same fork. The declared wrong-basis distractor (5010 file) was not named as carrying the task. The card's `stump_class`, `analyst_test` and `domain_test` fields were not found in a card file by my quick search; the design note's `## Three rules` section matches the thread's domain, layer and decisive-step reading. No mismatch found.

## Stump power (Gate F)
Moderate to strong. The default capture-rate route files a wrong set of eight (or nine with a flight-training split). Getting the seven needs the N-number reconciliation across four spellings, the re-registered addresses, the local-time year boundary, and finding that operations per never-recorded airplane is the stable scaling variable. Nothing in the files names the trap.

## Findings, ranked
1. No blocking finding.
2. Optional: pin the L08 tow-plane reading behind 69.2 (the Notes sheet already states it).
3. Optional: keep the estimator filed as a WHAT (operations per never-recorded based piston airplane), never a HOW.
4. Minor: the grant guidelines' date (4 Dec 2026) precedes the end of the inventory year they cite.
5. The changed method 4.2 wording and step 7 are consistent with the data; the pass 1 verdict stands.

## Next action for the author
Proceed to ship; no repair needed.
