# determinism-check report, task269, 2026-10-31 (pass 4)

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Package: target.zip sha256 prefix 68bac91330383553. Thread: one general-purpose sonnet medium thread over /tmp/determinism-check-task269-pass4/ (verdict.md there).

## Why
Grant terms 2.1 to 2.4 file the estimand: compliance over every moment on every AM and PM shift of 2025-26, weighted by required care hours, funded below 80 per cent, at most six. Executed literally that includes unaudited shifts. The audits under-sample understaffed shifts (5.3 per cent of audited moments against 18.8 per cent of care hours) and compliance there is far lower (58.9 against 87.1), so the audit-as-it-stands answer (9B alone) is biased and the data separate it from the five-ward answer. Every ward-specific model the judge fitted funds AMU, ESSU, 4A, 7A, 9B and no other ward.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Audited compliance, 9B / others | 77.0 / 82.8 or above | same (audit moments, roster-shift placement, night-begun dropped, S1A as 6A) | yes |
| CC2 audited moments >10% short vs care hours | 5.3 / 18.8 | 5.3 / 18.8 | yes |
| CC3 compliance short vs rest | 58.9 / 87.1 | 58.9 / 87.1 | yes |
| Five-band ward model, funded five | below 80 | 9B 74.4, 4A 75.1, ESSU 75.3, AMU 76.1, 7A 76.2; next 8A 84.2 | yes |
| Ask 2 HOBSI counts and rates, 14 wards | per golden | all 14 exact | yes |
| Asks 3 and 4 litres and per-1,000, 28 figures | per golden | all 28 exact | yes |
| SVG chart wards and colours | five funded in orange | consistent with ask 1 | yes |

## Competing answers that survived
- 9B alone (audits as they stand, or AM/PM audit shares weighted by care hours): rejected; terms 2.1/2.2 define the population as every AM/PM shift and the audit sample is demonstrably skewed. It is the easy route, not a defensible fork.
- Four wards from a pooled ratio-only model (no ward term): gives 9B 83.5 against observed 77.0, so the model contradicts the data; excluded.
- RN-only worked hours: a different set, not a defensible reading of "nursing hours".
- F1 (ask 2): a readmission at the minute of separation continuing the stay is filed in the protocol only by "admitted to the hospital". Per-record reading gives 332 episodes against 351 (AMU 28, 4A 29, 7A 30, ESSU 12 against 29, 31, 32, 14). 47 zero-gap readmissions, next smallest gap 206 minutes. Rated forced, but unfiled.
- F2 (asks 3 and 4): handheld second sends (same dispenser, same minute of day, 1 to 16 days apart) are described in no file. A literal count gives 6A rub 289.4 L and soap 107.6 L against golden 279.4 and 103.6 (every ward moves). A rigorous solver finds the pattern (about 1 in 1,440 by chance; windows 17 to 30 days give the same set). A hidden-rule device in an ask, which the house rules allow.
Neither fork touches the main call.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | csv (11), pdf (3), xlsx (1) | yes |
| Large file | 25,000 rows or more | acuity 224,319 rows (roster 72,749; audit moments 26,265) | yes |
| Distractors | 2 or more in metadata.json, none labelled in a file name | patient_experience_survey, staff_influenza_vaccination; neither name labels it | yes |
| Distractors unused yet weighty | unused by the solution, ruled out by a shipped fact | survey is the patients' view, terms 2.3 makes gold-auditor sessions the record; neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | xlsx and svg, both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | HOBSI, rub and soap across 14 wards, count, rate and litres; unit and one decimal in prompt | yes |
| Rubric | prompt shape identifiable, 25 or more criteria | scorecard-style designation, 14 wards by 3 measures; well over 25 (the note's arithmetic says 100) | yes |
| Reads as real, not LLM | none flagged | thread found system-extract irregularities and no authoring language in the PDFs | yes |

I did not re-verify licence provenance from the bundle. metadata.json records source, date and licence for each file.

## Gate G reconciliation
Thread: statistical_rigor, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical, estimation_fit (audit sample selected on a covariate that drives the outcome, reweighted shift by shift), declared distractors are the survey and the flu list. These match. The thread did not name the declared distractor as the surface read; the surface read it names is the audits as they stand and the care-hour-weighted audit share, which are correct figures and not a shipped ranking. Borderline note: the audit skew is a built property of the sampling, not a corrupted value, so the thread passed Gate G.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical. Design note: the same (Layer 1 is the messy extracts, Layer 2 is estimation of compliance for a population only partly audited). Easy route: audit compliance, funding 9B alone. Rule application is not the decider: the terms file the estimand and say nothing on estimating it from a sample.

## Stump power (Gate F)
The thread rates it good. The trap is a selection effect that needs a three-way join (acuity, roster, audits) and a ward-specific ratio model, announced nowhere. Expect many strong runs to file 9B alone or a pooled-model four-ward set. The decisive step is a field-standard estimation correction rather than a textbook route a strong solver lands unprompted, so I record no landable-call concern. The main thread should weigh this against the ladder in the design note (the 60 build bar). Asks 2 to 4 carry their own devices (stay merge, linkage by date of birth and sex, handheld duplicates, S1A fold-in).

## Findings, ranked
1. Stale wording in the design note: item 7 and the Three rules text say `ward_compliance_2025_26.png` and "day-shift compliance", and the card's domain_test says "day shifts". The shipped deliverable is `ward_compliance_2025_26.svg` and the filed basis is AM and PM shifts. No effect on solvers, but a reviewer reading the note or card sees a mismatch. Fix both in the note and card.
2. F1: the same-minute readmission merge is unfiled (ask 2, 332 against 351 episodes). An optional protocol sentence would close it, but it changes what solvers see and needs a rerun. The thread rates the merge forced.
3. F2: handheld second-send duplicates are hidden-rule in asks 3 and 4, allowed by house rules. No change needed.
4. The thread found the audited-shift staffing comparison, not the audits themselves, to be the stump. The note's own estimate (several strong runs filing 9B alone) is consistent.

## Next action for the author
Correct the design note (png to svg, day shift to AM and PM shifts) and the card's domain_test wording, then ship. Add the F1 protocol sentence only if you accept a rerun.
