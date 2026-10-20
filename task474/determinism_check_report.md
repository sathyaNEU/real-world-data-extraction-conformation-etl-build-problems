# determinism-check report, task474, 2026-10-20

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (one wording pin on the registry end-date convention; the main call and analytic surface unchanged)
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Scope caveat: the judge thread read a fresh unzip of target.zip as it stood at run time (registry 2,813 rows). The working target/ registry has since been regenerated (2,786 rows, commit 48fb16c, 16 end-before-start registrations fixed) and target.zip still holds the older registry. The main call is unaffected (the registry feeds only the supplementary asks), but the fleet figures below were reproduced on the old registry and must be re-verified after the registry fix and the ask re-siting. target.zip must be rebuilt from the final target/ before ship.

## Why
Rules 2.1 to 2.3 and the link register fix the estimand (twelve-month vehicle-miles by class times the 2026 rates, 5.00 tonnes per mile or more). The judge reproduced L03, L05 and L14 as the only links at or above the line. No file states how two-day counts are carried to the year, so the method is open and is closed by the data: class-specific month-by-weekday factors from the four classifying stations, and on the three register-flagged terminal access roads (L01, L06, L14) the combination trucks carried by the terminal gate record. Count-day volumes on those roads move one-for-one with the gate (CU times gate ratio agrees across each road's two days within 0.2 to 1.5 percent, against 20 to 55 percent spread under highway factors). The easy route (stations' factors everywhere) gives L01, L03, L05, L06.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| NOx per mile L03 / L05 / L14 | designated | 6.182 / 5.461 / 5.400 t | yes |
| Other eleven links | under 5.00 | max L09 4.564, L01 4.549, L06 4.451 | yes |
| Links at or above 5.00 | 3 of 14 | 3 | yes |
| Fleet at quarter ends (old registry) | 2,313 / 2,348 / 2,387 / 2,425 | same | yes (old registry) |
| MY 2009 or older | 297 / 303 / 307 / 311 | same | yes (old registry) |
| Carriers 30 Sep 2026 | 8 carriers, sums 2,425 and 311 | same | yes (old registry) |

## Competing answers that survived
1. L01, L03, L05, L06 (no gate on terminal roads): the one place a good-faith reader can disagree; the rules never link the gate report to the counts and the register's "Terminal access" column is the only pointer. The judge eliminated it by data (analytical miss, not a reading fork) and flagged it as the residual risk. This is the intended stump.
2. L03, L04, L05, L14 (gate over-extended to L04): eliminated, L04 not flagged terminal access.
3. Eight or nine link sets (all-class or month-only factors): eliminated as poor method.
4. Supplementary counts under an exclusive registered_to: genuine unpinned boundary (2 trucks at 31 Dec, 2 at 31 Mar, 0 at 30 Jun, 1 at 30 Sep). The only open fork; supplementary asks 2 and 3 only.
5. truck_id instead of VIN: contradicted by rule 3.1 ("counts once") and the data notes.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | csv, xlsx, pdf, txt (4) | yes |
| Large file | 25,000 rows or more | 347,376 rows (ccs hourly) | yes |
| Distractors | 2 or more in metadata.json, none named in a file | no2_monitor_hourly_2026.csv, truck_complaints_311_2025_2026.csv; neither name labels it | yes |
| Distractors unused yet weighable | yes | ambient NO2 and 311 complaints, plausible, unused, ruled out by what they measure; neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | quarter by carrier by old/total; "whole trucks" stated | yes |
| Prompt shape, rubric 25 or more | identifiable, 25 or more | grid shape (design note); the rubric is generated later and not checked here | not verified |
| Reads as real, not LLM generated | yes | judge: system-export layouts, no generation text | yes |
| Metadata vs registry | consistent | metadata rows 2,786 matches target/; target.zip is stale (2,813) | FAIL until rezip |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note declares no distractor as the stump; the two metadata distractors are not the surface read carrying the task. The thread's decisive step (annualise terminal-road trucks by the gate record) matches the design note's stump sentence and its R2 default path (L01, L03, L05, L06) exactly. No mismatch.

Gate H reconciliation: the thread says domain pass, layers pass, decisive_step analytical, consistent with the note's Three rules (Domain test, Layer 2 estimation_fit, Analyst test). The note's Not rule application line is borne out: the thread found the method filed nowhere and the rules silent on the gate.

## Stump power (Gate F)
Moderate to good. The trap is the standard route (TMG factors on every road), which a strong solver takes by default; margins of 8 to 9 percent mean a partly correct run lands on a different set. Weakness for the main thread to weigh against the scored readers: the gate-to-count relation is discoverable by cross-checking count days against the gate report, so a strong model may find it, and the judge notes the reader result (reader 2 missed the call, per the pause commit). Fleet asks are rule application and are not the decisive step.

## Findings, ranked
1. The registered_to boundary is filed nowhere. Pin in data_notes.txt that registered_to is the last day in force, inclusive. Wording only; no rerun if the analytic surface stays byte-identical.
2. target.zip is stale against the regenerated registry; the judge's fleet reproduction is on the old registry. Rebuild the zip, then re-verify all quarterly and carrier counts and the golden xlsx.
3. Residual risk: the terminal-road method is unfiled by design; do not file the gate method (it would turn the stump into rule application).
4. Rubric criteria count not verified here.

## Next action for the author
Add the one-line inclusive registered_to convention to data_notes.txt, rebuild twice, re-zip target.zip, recompute the fleet figures on the final registry and re-site the asks; re-judge once only if the analytic surface or the asks' definitions change beyond that wording.
