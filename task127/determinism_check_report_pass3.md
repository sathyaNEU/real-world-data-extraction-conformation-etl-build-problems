# determinism-check report, task127, 2026-10-31

(Filed as pass3 because determinism_check_report.md and _pass2 already exist and are never overwritten. Judge thread output: /tmp/determinism-check-task127-1793463831b/verdict.md, run against the submission.md current at spawn and a fresh unzip of target.zip.)

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: binding_constraint (counterfactual value net of the equipment wait; ETL conformance on the asks), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every committed figure reproduces from the shipped bundle: covered counts 508/350/120/285/361, nights 6.39/5.82/5.35/4.01/3.14, fill 508/350/120/222/0, 6,816 bed-days, all 45 chart labels, all 9 referral counts. The package value is the nights after the later of ready date and equipment delivery. The data force this: 0 of 794 equipment-delivered covered patients left before delivery, and 361 left the day it arrived (195 at Ashby Vale). Gates A, B, C, E pass. The three optional solution-text edits the thread listed (step 1's attribution of latest-submission handling to the note, step 3's stray restart parenthetical, step 2's "no pathway-1 patient" claim) are already applied in submission.md per the coordinator; no shipped file changed.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Covered patients (RMC/Wend/Holm/Cleeve/Ashby) | 508/350/120/285/361 (1,624) | same | yes |
| Nights per package | 6.39/5.82/5.35/4.01/3.14 | 6.3917/5.8200/5.3500/4.0070/3.1413 | yes |
| Fill and bed-days | 508/350/120/222/0; 6,816 | 3,247/2,037/642/889.56/0; 6,815.56 | yes |
| Unadjusted alternative | 10.81/9.86; 10,507 | same | yes |
| ICES join | 794 delivered, 0 after discharge | 822 joined, 794 delivered, 28 cancelled | yes |
| Delayed bed-days, 15 cells; total | 24,295 | all match | yes |
| Patients delayed, 15 cells | per submission | all match (per-hospital distinct spell) | yes |
| Referrals within 7 days, 9 cells | 178/228/166; 57/55/53; 106/103/95 | same | yes |

## Competing answers that survived
Advisory only, none licensed by the files:
1. Raw nights after ready date: 10,507 bed-days, Ashby Vale funded. This is the intended wrong route, defeated by the allocation note's value wording and the equipment data. It is the one place a skeptic can argue.
2. Superseded rather than latest submission: chart total 24,125 against 24,295. Not stated on the page; near-universal convention.
3. Discharge site rather than ward at midnight for the chart. Closed by the ward files, though no sentence states it (the evening dating and calendar-day wait are in the allocation note's monitoring section per the repair).
4. Ignoring spot invoices: Ashby 45/48/47, Marchford 163/208/138. Key join validates 815/815.
5. Hospital-discharge-only referrals or under-7 days: not licensed by the prompt. Calendar-day against 24-hour waits give identical counts.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000+ rows | 12 / csv, xlsx, pdf / 138,829 rows | yes |
| Distractors in metadata.json, none named in a file | 2+ | 3 (weekly return, bed census, reablement); file names do not label them | yes |
| Distractor unused yet weighty | | weekly return is the national view of the same delays; judge found nothing it answers | yes (judge) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | | prompt states whole numbers; asks are cells by hospital/district x month | yes |
| Prompt shape and 25+ criteria | | shape 05 recorded; criteria count not verifiable here (rubric is generated) | not checked |
| Reads as real, not LLM generated | | no authoring leakage seen by judge; golden realism not re-read here | judge yes |

## Gate G reconciliation
Thread: binding_constraint, analytical_non_defect, surface_read no, sole_data_defect no. The card/pipeline.json records "binding_constraint or decomposition_attribution by pass, analytical_non_defect, surface_read no, sole_data_defect no": match. The declared distractor (weekly return) is not the surface read carrying the task; the surface read is the recorded delay, an accurate number. Gate H: thread `domain pass, layers pass, decisive_step analytical`, matching pipeline.json.

Two items to weigh, both from the design note being behind the repair:
- DESIGN_NOTE.md `## Three rules` (No decoy line) still says "the equipment notes say what hospital-discharge equipment is for". Those notes are withdrawn. Update the line to the current basis (data pattern plus the allocation note's wording).
- The note's Not-rule-application line says nothing shipped says what equipment is for, while the thread reports the allocation note states a package removes only the care-provider wait. Confirm which is true in the shipped PDF; the judge's reading is the real reviewer's.

## Stump power (Gate F)
Good. A strong solver who joins no equipment data, or reads the value definition literally, files 10,507 bed-days with Ashby Vale funded: wrong on split and total. The equipment join is discoverable and not narrated. The decisive step is a counterfactual construction across two systems, not a rule execution. Thread notes it is borderline against rule_application only because the value definition is deliberately open; the main thread should weigh that against the ladder. Chart and referral asks add hard independent figures (ward at midnight, per-hospital patient counting, spot-invoice join).

## Findings, ranked
1. Design note Three-rules text stale against the withdrawn equipment notes (above).
2. Latest-submission and ward-at-midnight conventions not stated on the page (advisory forks 2 and 3).
3. Spot-invoice join key undocumented (validates exactly; advisory).
4. Rubric criteria count not verified in this pass.

## Next action for the author
Update the `No decoy:` and `Not rule application:` lines in DESIGN_NOTE.md to describe the current pack, then proceed to ship; no data or prompt change is needed.
