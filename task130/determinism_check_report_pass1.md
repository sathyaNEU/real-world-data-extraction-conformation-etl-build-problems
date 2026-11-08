# determinism-check report, task130, 2026-11-07

(Architecture 6, Redbud Line Services' 2027 recordable injuries. Prior reports in this folder —
`determinism_check_report.md`, `determinism_check_report_round1/2/3a/3b.md`, `determinism_check_report_arch5*.md` —
belong to dead architectures (a medical-malpractice trust reinsurance task and an Elkhorn County return-inspection
task respectively) and are left untouched. This is the first pass for architecture 6, written to a new pass file.)

## Verdict
NOT_DETERMINISTIC
**Disposition:** SEND_BACK
**Stumping type:** mechanism: planted_defect_flip, stumping_family: surface_read_rejection, surface_read_dependency: yes, sole_data_defect: yes

## Why
Gates B and C fail on the main call (critical components 1-4, deliverable asks 1-4 of `safety_plan_recordables_2027.docx`, the chart). The golden's "No, 255 recordables, 3.57, over the 3.0 limit" is reached only by discarding the full 2021-2026 recorded rate (2.55 crews / 1.92 technicians, which CS-4 §3.1 and §5 license outright — "a recordable case... as finally classified," "Pinewater does not prescribe the method") in favor of the crews' days-0-34-of-count segment rate (3.84), on the stated premise that "crews leave injuries they can hide off the log as each count nears its award." No shipped file (`crew_safety_recognition_programme.docx`, `pinewater_contractor_safety_standard_cs4.docx`, `recognition_programme_2027_notice.docx`, either case-management export) states, documents, or evidences that injuries are concealed, miscoded, or withheld near an award. The judge thread reproduced both the golden's own path (255, 3.57, by quarter 60/66/67/62, exact) and the plain, equally-filed carry-forward of the full record (176, 2.46 — inside the limit, the opposite call) from the raw files, and found the declining day-of-count bucket rate is at least as consistent with ordinary selection/survivorship across a pooled hazard as with a true behavioral suppression story. Supplementary ask 5 (`recordables_forecast_2027.xlsx`, first-aid cases by district and quarter) is independently DETERMINISTIC and reproduces exactly.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 2027 plan hours (crew / tech / total) | 12,258,000 / 2,030,000 / 14,288,000 | same, from `work_plan_hours_2027.xlsx` | yes |
| 3.0-limit allowance | 214 (214.32) | 214.32 | yes |
| Golden path: crew rate days 0-34 (3.84) + tech 1.92 on plan hours | 255 (60/66/67/62), 3.57 | 255 (60.2/65.8/66.8/62.2), 3.57 | yes, exactly |
| Competing path: full 2021-2026 recorded rate (2.55 crew / 1.92 tech) on plan hours | not committed (golden explicitly rejects it) | 176 (175.8), 2.46 — inside the limit | yes, reproduces as a defensible alternative |
| First-aid cases by district/quarter (ask 5) | Blue Ridge 36/44/19=99; Piedmont 38/34/32=104; Lakes 45/46/30=121; Coastal 52/51/33=136 | identical, via crew-assignment district join and 0-3-day nurse-line/supervisor dedup | yes |

## Competing answers that survived
- **Fork, main call.** Operationalization A: plain carry-forward of the full recorded history (CS-4 §3.1's "finally classifies," §5's "method not prescribed") → within limit, "Yes." Operationalization B (the golden's): substitute the no-award-pressure segment of each crew's count for the whole history, premised on unevidenced concealment → over limit, "No." Both reproduce exactly from the shipped files; nothing shipped closes the fork in the golden's favor. This fork is not closed by the files — it is the central finding.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | >=10 | 12 | yes |
| Format count | >=3 | csv, docx, xlsx (3) | yes |
| Large file | one file >=25,000 rows or large DB | `timesheet_hours_by_pay_period_2021-2026.csv`, 152,804 rows | yes |
| Distractors named, not in a file name | >=2 in metadata.json | `good_catch_reports_2025-2026.csv`, `subcontractor_monthly_safety_2026.csv`, named in metadata.json, names don't self-label as distractors | yes |
| Distractors unused by solution but relevant to weigh | each distractor weighable | neither file appears in SOLUTION_STEPS; both are plausible safety-adjacent populations (near-miss reports, subcontractor-not-field-employee data) | yes (not independently verified whether either distractor arithmetically reproduces a graded quantity that a shipped fact rules out; not load-bearing to the verdict) |
| Deliverables | 1-3, all present in golden | 3 (docx, xlsx, png), all named in metadata.json's deliverables list | yes |
| Asks multi-dimensional, unit+rounding stated | required | main ask: year+quarter forecast and rate; ask 5: district x quarter; prompt states "Count injuries as whole numbers and rates to two decimals" | yes |
| Prompt shape identifiable, rubric >=25 criteria | required | design note names shape 02 (forecast across many periods); rubric criteria count not independently verified in this pass (no standalone rubric artifact found in task130/; generated at build per pipeline.json) | not verified |
| Nothing reads LLM-generated, goldens read as real work product | required | judge found hygiene PASS: 12 files read as genuine operational exports (payroll calendar, case-management export with revision history, a superseded policy memo), no provenance/benchmark disclosure | yes |

## Gate G reconciliation
The design note's own "Three rules" section (architecture 6) asserts `No decoy`, `Not semantics`, `Not rule application`, and frames the decisive step as recovering "the latent rate behind a count the crews thin by choosing not to report as a clean-record reward nears" — an analytical, behavioral-economics read it argues the domain's own method (discrete-choice/limited-dependent-variable modeling under an incentive) forces. The judge thread classified the same step as `planted` / `surface_read_rejection` / `planted_defect_flip`, on the grounds that no shipped file documents or evidences concealment, and that a pooled-hazard decline by count-day is equally explained by selection effects.

This is a mismatch, and the design note's own build record resolves it against the design note's narrative: the "Oracles" section states the generator's ground truth directly — "the injuries the simulation generated, recorded or not, give the crews' true rate of 3.72 and 247.5 recordables... 401 of the 1,278 injuries crews had on Pinewater work from 2021 to 2026 (31.4 per cent) never reached the log" — i.e. the mechanism is implemented in the generator as a literal, simulated non-reporting defect (roughly a third of true injuries are built to never appear in any shipped file), not as a derivable behavioral inference the data alone forces. The golden's 255 is explicitly tuned to land close to this hidden ground truth (3% above it), which is the signature of a stump built around recovering a planted, unrecorded true value rather than an analytical read of honest, complete data. The design note's own "Not semantics"/"Not rule application" framing does not address this: the step it calls analytical is, by its own oracle section, a catch of a hidden data defect (missing records) dressed in behavioral-economics vocabulary. This reconciliation confirms, rather than overturns, the judge's Gate G and Gate H classification, and is the single strongest predictor that this build sends back.

## Gate H (the three rules)
`domain: pass`, `layers: pass`, `decisive_step: planted`

H1 passes: the task type (forecasting a recordable-injury rate against an OSHA-style contractor safety standard) is native to the assigned domain/task-type pairing and survives the swap test. H2 passes: Layer 1 (two merged case systems, crew recodes, prior-period payroll adjustments, nurse-line/supervisor duplicate records, a stale district field) is genuine mess that resolves cleanly with care and does not carry the stump (ask 5 proves this). H3 fails: the step that separates the golden (255, over limit) from the answer a strong analyst who read every file and rule correctly would file (176, inside limit, following CS-4 §5's own "method not prescribed" instruction and the full recorded history) turns on importing an unevidenced claim that the shipped record under-states true injuries near an award — and the design note's own oracle section confirms this claim is implemented as a literal 31.4%-missing-records defect baked into the generator's ground truth, not as a conclusion the honest, complete, shipped data forces. A strong analyst applying the field's own standard method (carry the recorded rate forward, check for under-reporting using the two tests the record itself offers — the technicians' lower rate, the days-away share — both of which clear the record) files 176 and is marked wrong for not independently inventing the concealment story.

## Findings, ranked
1. **(Send-back, governs disposition) Gate B/C/H3 failure on the main call.** The golden's central move — discounting the shipped historical log as understated near an HR-14 award — is a planted, unevidenced data-defect claim (confirmed by the design note's own oracle section: 31.4% of true injuries are built to never reach any shipped file), not an analytical conclusion the files force. A plain, CS-4-licensed carry-forward of the full recorded rate gives the opposite call (176, inside the limit) and nothing shipped rules it out.
2. **Gate G banned_stumping_type.** The mechanism is `planted_defect_flip`/`surface_read_rejection` regardless of the design note's "Three rules" framing or the depth of the 90-day-count reconstruction chain used to reach it.
3. (Non-blocking) Supplementary ask 5 and its deliverable are fully sound and need no change.

## Next action for the author
Rebuild the decisive step around a FINE-numbers shape that does not require importing an unevidenced claim that the shipped historical log under-counts: for example, a genuine composition/mix shift between the 2021-2026 base and the 2027 work plan (a real change in crew-type, district, or OH/UG/SUB/VEG hour mix under the 2027 plan that a naive single blended rate mispredicts for a reason the data pins), or a method-selection question pinned by an out-of-sample validation, built on honest, complete records with no claim that the log itself is wrong. If concealment is to be kept as the mechanism, it must become a filed fact (an audit finding, a documented reclassification pattern, a whistleblower memo) rather than a behavioral inference with zero support in any shipped file. This is architecture 6's finding; per the project's own rule on a dead design (`precut.py`/judge send-back), re-root with a new draw rather than resume this device.
