# determinism-check report, task266, 2026-10-18 (pass 3, stage 4 of the reship)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Policy 3.2 follows each student only under the admission recorded at entry, so transfer out and withdrawal end the chance of the degree. That forces a competing-risks cumulative incidence over the pooled classes, with open admissions censored at spring 2027. It gives six programs below 30 per cent. Kaplan-Meier (1 minus KM) gives one program and crude shares give eight; the policy text excludes both. All 27 committed figures (nine shares, nine FTE, nine under-ten class counts) reproduced from the bundle, including the two re-cut asks. The main call is unchanged from pass 2.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Completion share GENS / BIOL / BUSA / PSYC / MEDA / ECED / CRJU / HVAC / NURS | 20.9 / 24.9 / 22.2 / 25.9 / 26.2 / 19.5 / 32.5 / 44.4 / 36.7 | 20.92 / 24.88 / 22.23 / 25.87 / 26.23 / 19.47 / 32.52 / 44.43 / 36.72 | yes (ir_fall xlsx, id map, admissions csv, term_calendar) |
| FTE, same order | 1,148.8 / 352.5 / 525.2 / 399.4 / 381.5 / 341.0 / 391.2 / 272.3 / 533.1 | 1148.80 / 352.53 / 525.20 / 399.40 / 381.47 / 341.00 / 391.20 / 272.33 / 533.07 | yes (registrations, schedule Cr Hrs, program_of_record_history) |
| Classes under ten, same order | 2 / 15 / 7 / 7 / 10 / 5 / 8 / 21 / 79 | 2 / 15 / 7 / 7 / 10 / 5 / 8 / 21 / 79 | yes (schedule, registrations, register Subjects sheet) |
| Cohort 5,292; 5 DC removed; exits GR 1,169, TO 843, WD 1,378, open 1,897 | as filed | same | yes |

## Competing answers that survived
None. Alternatives tested and closed by shipped text:
- 1 minus KM gives 1 program (ECED only); closed by policy 3.2.
- Crude nine-term shares give 8; closed by policy 3.3.
- Fall 2023 class alone gives 7 (CRJU 26.8); closed by policy 3.3.
- Own-cohort extrapolation moves shares by at most about 1 point (CRJU 31.5, still above the floor); the call holds.
- Advisory only, ask 3: grouping online TBA sections by instructor would change 7 of 9 counts. The registrar notes say online sections have no meeting days or times, so the golden reading is forced.
- Advisory only, FTE: summing registrations credit_hours double counts lab rows (NURS 847.7). The registrar notes define both columns, so the schedule's Cr Hrs is forced.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats, large file | 10+, 3+, 25,000+ rows | 14 files in target/, 4 formats (csv, xlsx, pdf, txt), registrations csv 28,117 rows | yes |
| Distractors | 2+ in metadata.json, none labelled by file name | course_success_rates xlsx and service_area_occupational_outlook csv, unused by the solution; file names do not label them | yes (judge confirmed unused; I did not re-test that they reproduce a graded quantity) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf) | yes |
| Asks | multi-dimensional, unit and rounding stated | 3 asks x 9 programs; one decimal for percentages and FTE, counts are whole numbers | yes |
| Prompt shape, rubric 25+ | identifiable, 25+ criteria | per-program grid, 27 gradable figures plus the call and the chart; I did not generate the rubric | yes (basis: figure count) |
| Reads as real, not LLM generated | | judge found no authoring leakage; the golden reads as a registrar and IR work product | yes |

## Gate G reconciliation
The judge named mechanism statistical_rigor and family analytical_non_defect, with surface_read_dependency no and sole_data_defect no. The design note files strategy key `decomposition_attribution` (decisive generator G17, the event-history estimator) and Gate G `competing risks` as `estimand_identification`; this is the same stump under the design's label. The judge did not name the declared distractors as carrying the task. Both runs of the Kaplan-Meier route (1 program) and the crude route (8) match the wrong answers the design note anticipates. No mismatch.
Gate G: PASS, no shipped artifact ranks the candidates wrongly; difficulty survives deleting every wrong number.
Gate H: domain pass, layers pass, decisive_step analytical (cumulative incidence with TO/WD competing and open admissions censored). It matches the card and the note's `## Three rules`.

## Stump power (Gate F)
Good. The easy routes (KM and crude shares) are tempting and give 1 and 8 programs; the correct 6 needs competing risks. The re-cut asks add FTE and small-class counts that require the program of record at the census, the schedule's Cr Hrs, and combined meeting sections.

## Findings, ranked
1. None blocking.
2. Advisory: the two ask readings above (online sections, lab-row credit hours) are closed by the registrar notes and the policy, not forks.
3. The nearest main-call margin is CRJU at 32.5 against the 30 floor (1.5 to 2.5 points under alternative estimators); the call holds.

## Next action for the author
Proceed to ship (APPROVE); no generator change is needed.
