# determinism-check report, task478, 2026-10-22 (run r4a)

## Verdict
NOT_DETERMINISTIC (narrow: supplementary ask 3 only, Thistlebank 409). The main call and asks 1 and 2 reproduce.
**Disposition:** SEND_BACK (an input-file or data-dictionary edit closes it, but it changes what solvers see).
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Work order WO-27004908 (section 409) has two severity-2 lines, each entered as 60 lb. 60 is feasible as a per-line figure (single-line severity-2 orders run 30 to 65 lb) and as an order total (30 lb per pothole minimum). The golden sums it (120 lb, so Thistlebank 2,145) only through a heuristic no shipped file states: the data dictionary says only "cold_mix_lb is the cold mix pounds as entered" on "one row per task line". The order-total reading gives 2,085. Of 91 identical-figure multi-line orders, 73 can only be totals, 17 only per-line, and 1 fits both. A literal reader who sums every line is wholesale wrong on ask 3, so the convention must be inferred from the data; it is forced for 90 of 91 orders.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Roadway lane-miles (inventory less 5 turnback segments) | 2,428.9 | 2,428.94 | yes |
| Per-unit latency (covers within 0.05 mi, through origin on speed) | 0.47 to 1.74 s | 0.473 to 1.743 | yes |
| Distinct potholes on roadway | 1,427 | 1,427 | yes |
| Potholes per ten lane-miles, 14 sections | 8,7,8,4,4,7,9,3,8,4,5,3,8,2 | 8.14, 6.90, 8.00, 3.71, 4.06, 7.09, 9.13, 2.96, 8.15, 3.98, 4.95, 3.14, 7.93, 2.03 | yes |
| Designated at 6.0 or more | seven named | same seven (nearest margins 6.90 and 4.95) | yes |
| 200 ft join designates | five sections | five (401, 403, 407, 409, 413) | yes |
| 100 ft uncorrected adds Grisholt, Oxbrae | claimed | 7.02 and 6.51 | yes |
| Cold-mix pounds, 13 sections | golden values | match under the golden rule | yes |
| Cold-mix pounds, Thistlebank | 2,145 | 2,145 (sum) or 2,085 (order total) | NO, fork |

## Competing answers that survived
Ask 3, 409 Thistlebank: 2,145 (sum WO-27004908 as 120) against 2,085 (count once as 60). The shipped data dictionary does not close it; no shipped file states the mobile-app order-total convention. The 10 ft join is unfiled but forced by the data (bimodal gaps, any threshold from about 7 to 20 ft agrees).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | 4 (CSV, PDF, XLSX, JSON) | yes |
| Large file | 25,000 rows or more | 103,162 detections | yes |
| Distractors in metadata.json, none named in a file | 2 or more | 3 (pavement_condition_2026, winter_operations_2027-03, kerbline_unit_sessions_2027-03); judge also saw the 2025/2026 crosswalk as unused, not declared | yes |
| Distractors unused, weighable, ruled out by a shipped fact | yes | none answers a graded quantity | yes |
| Deliverables | 1 to 3 | 2 (CSV, PDF), both in the golden | yes |
| Asks multi-dimensional with unit and rounding | yes | 14-section asks, whole numbers stated; units stated | yes |
| Prompt shape and 25 or more criteria | yes | shape identifiable (per-section table plus chart); the rubric is generated and not visible here, 14 x 3 graded cells make 25 plausible | not verified |
| Reads as real, not LLM generated | yes | judge found no authoring disclosure; manifest reads as an export index | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note's Three rules section names the latency correction on the covers as the decisive step and states there is no decoy; this agrees. The declared distractors (condition survey, winter operations, sessions) are not the surface read; the surface read is a fixed-distance join, which is the easy route, not a shipped artifact. No finding. The thread's borderline note (latency offset as a planted defect) is answered by the note's No decoy line: the detections are what the system writes, and no shipped line states the offset.

## Gate H line
domain: pass, layers: pass (Layer 1: local time against UTC across the 14 March DST change, 2025 against 2026 segment ids, turnback roadway, repeated cold-patch figures; Layer 2: per-unit GPS-latency calibration on surveyed covers, then pothole entity resolution), decisive_step: analytical. Matches the note's Three rules.

## Stump power (Gate F)
Strong: a single fixed join distance fails (200 ft designates five and misses Kestrelton and Fenwick Gap; 100 ft uncorrected adds Grisholt and Oxbrae and drops two). Finding the latency reaches the golden. The decisive step is a textbook calibrate-then-deduplicate route, so the blind readers' measure rules on how landable it is. The ask-3 miss for a literal reader is semantics, not stump power.

## Findings, ranked
1. Ask 3 (409): WO-27004908 repeated 60 lb fits both a per-line and an order-total reading; the golden's heuristic is unfiled. Gate C, competing_defensible_answer.
2. Convention for 90 other multi-line orders is inferred, not filed; the dictionary line "as entered" is the only text. Thin, forced by the data.
3. Thread notes licence and source columns were not verifiable from the shipped files (metadata.json records them).

## Next action for the author
Edit WO-27004908 in the generator so the repeated figure fits only one reading (55 lb allows only per-line, Thistlebank 2,195; 90 lb allows only an order total, Thistlebank 2,175), update the golden and submission.md to match, rebuild and re-judge once; or add one WHAT-level sentence to tamsett_pilot_data_dictionary.pdf that an app-raised order carries its total on every line. Leave the pothole data, units, covers, inventory and traversals alone.
