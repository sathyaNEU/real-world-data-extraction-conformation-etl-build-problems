# determinism-check report, task125 (architecture 3), 2026-10-31

## Verdict
NOT_DETERMINISTIC (competing_defensible_answer / underspecified_objective; the golden figures themselves reproduce)
**Disposition:** SEND_BACK (the reconciliation confirms the judge's send-back)
**Stumping type:** mechanism: planted_defect_flip (unmixed boundary samples), stumping_family: surface_read_rejection, surface_read_dependency: yes, sole_data_defect: yes

## Why
1. Main call. Read literally, schedule section 3 (load = run-day boundary sample x weir flow) gives MZ2 36.2 over 32, NY3 67.2 over 58, MZ4 31.0 within 34, NY2 30.3 within 35: the opposite of the golden on all four units. The golden replaces those boundary loads with inflow sums on a mass-balance inference. No shipped file says the four samples are unrepresentative (register calls all 14 sites "boundary monitor"; run-log remarks empty). Both directive lists are licensed by the text.
2. Logger ask: the golden removes fouling drift linearly (additive). No file files the correction or its form. Proportional ramp changes counts (ECL-10 Mar 402 vs 308, ECL-03 Mar 17 vs 27, ECL-06 Dec 256 vs 239, ECL-14 Nov 426 vs 442); uncorrected hours differ again.
3. Discharge ask: the S-to-SO4 restatement (x2.996) of three mines from Nov 2025 is inferred from a ratio break; the licence conditions say only "sulfate" of the composite and no basis change is documented. A literal reader files returns as reported.
4. Side note: MZ4 and NY2 have no licensed discharge in the register, so "mines discharging into them" has no mine for those units.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Boundary-sample loads MZ2/MZ4/NY2/NY3 | not claimed | 36.2 / 31.0 / 30.3 / 67.2 | n/a (contradicts golden) |
| Inflow-sum loads MZ2/MZ4/NY2/NY3 | 27 / 40 / 40 / 52 | 27.1 / 40.0 / 40.2 / 51.9 | yes (under the inflow-sum method only) |
| KH1, NT1, other units | 22, 27, ... | 22.1, 26.9, ... | yes |
| 36 logger hour counts | as filed | additive linear drift: all match; proportional: differ | only under the unfiled additive method |
| Discharge quarters | as filed | not recomputed; S-basis break confirmed | not verified |

## Competing answers that survived
- Boundary-sample load vs inflow-sum: over set {KH1, MZ2, NT1, NY3} vs golden {KH1, MZ4, NT1, NY2}. No shipped rule closes it.
- Drift correction additive vs proportional vs none.
- Discharge sulfate as reported vs restated from S.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000 rows | 13 / csv, xlsx, pdf / hourly logger csv (2.5 MB) | yes |
| Distractors | 2+ in metadata, none in file names | raingauges, nyathi WTW raw water log; names unlabelled | yes |
| Distractors unused yet weighable | yes | judge saw both as unused; not tested further | yes (not stress-tested) |
| Deliverables | 1 to 3, all in golden | 2 (pdf, xlsx), both present | yes |
| Asks multi-dimensional, unit and rounding stated | yes | yes in the prompt; but the logger and discharge asks rest on unfiled methods | partial |
| Prompt shape, 25+ criteria | yes | design note cites 61 ask criteria; not independently counted | yes (per note) |
| Not LLM-generated; goldens realistic | yes | judge: system-like exports, no disclosures | yes |

## Gate G reconciliation
Thread: mechanism planted_defect_flip, surface_read_rejection, surface_read_dependency yes, sole_data_defect yes. Design note and card: stump is the boundary sample being one bank's water, "No decoy" and "Not semantics" claimed on the grounds that nothing marks the samples. That is the same defect seen from the other side: the declared stump is a sample-location defect with no field or sentence exposing it, which the three rules classify as a planted defect, and the retired surface-read-rejection scaffold. The thread reads the boundary load as the surface read carrying the task; the declared distractors (raingauge, WTW log) are not involved. The note's "Not rule application" line concedes that executing the filed rule yields the wrong answer, which confirms the rule as filed does not reach the golden: a mismatch with the claimed analytical class. The thread's analyst-test finding (a strong analyst who reads every rule correctly still lands wrong unless suspecting the samples) agrees with the note's own analyst_test but classes it planted rather than analytical.

Gate H: domain pass; layers pass; decisive_step planted.

## Stump power (Gate F)
Plausible: a model tabulating loads along each river sees constant boundary/inflow ratios (1.34, 0.78, 0.75, 1.60) and may catch it, but this is spotting a data defect, not judging evidence. Margins are wide once the golden method is adopted. The reconstruction is a textbook mass balance, not a method the data forces.

## Findings, ranked
1. Main call is a planted-defect flip with the golden resting on an unfiled method (blocking).
2. Logger drift correction unfiled and form-ambiguous (blocking for that ask).
3. Discharge S-basis restatement undocumented in the pack (blocking for that ask).
4. MZ4 and NY2 have no licensed mine, so "directed mines" is unsupported for them (prompt logic).
5. Discharge quarterly totals not recomputed by the judge (residual unverified).

## Next action for the author
Re-root the main call (Rule 3: no planted defect as decisive step) onto honest samples with a field-estimated quantity; file the drift correction (or drop it) and the SO4/S basis of each return in the shipped text or licence conditions; fix the MZ4/NY2 "mines" wording. Rebuild, then re-judge.
