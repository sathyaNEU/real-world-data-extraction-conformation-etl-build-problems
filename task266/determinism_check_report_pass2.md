# determinism-check report (pass 2), task266, 2026-10-17

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (competing-risks cumulative incidence), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated sonnet thread (fresh unzip at /tmp/determinism-check-task266-1792249757/target/, no pass 1 report seen) recomputed every graded figure from the bundle. All reproduced. The policy files the population (three fall classes, entry program, deaths removed), the window (nine terms, summers included), the floor (30) and that the open classes are estimated. The registrar notes close the admission on transfer out and withdrawal and fix the census rule (RE, RW, WC) and the V-room combined-class rule. The estimator is left open, but the Aalen-Johansen, the imputation form and the TO/WD timing variants give identical values. Every estimator giving a different list breaks a filed rule. The pass 1 forks (open-class estimand SF5 and four ask forks) did not recur.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Completion share GS / Bio / Bus / Psy / MA / ECE / CJ / HVAC / Nursing | 20.9 / 24.9 / 22.2 / 25.9 / 26.2 / 19.5 / 32.5 / 44.4 / 36.7 | 20.92 / 24.88 / 22.23 / 25.87 / 26.23 / 19.47 / 32.52 / 44.43 / 36.72 | yes (ir xlsx, sis admissions, id map, register, term calendar) |
| Programs below 30 | 6 | 6 | yes |
| FTE, same order | 1164.1 / 358.0 / 531.7 / 404.0 / 386.6 / 343.6 / 397.1 / 274.5 / 538.3 | identical | yes (census registrations, section schedule Cr Hrs, program_of_record_history) |
| Classes under ten, same order | 1 / 13 / 5 / 5 / 9 / 3 / 3 / 13 / 78 | identical | yes (schedule, census, register Subjects sheet) |
| Cohort size | 5,292 (5 deaths removed) | 1,691 + 1,752 + 1,849 = 5,292; 5 DC | yes |

## Competing answers that survived
None. Alternatives and why each is closed:
- 1 minus KM with TO and WD censored gives 1 program (ECE only): closed by the "from the college" outcome and the registrar notes.
- Fall 2023 class alone gives 7 (CJ 26.8): closed by "taken together".
- Raw degrees over all entrants gives 8 (CJ 26.7, Nursing 27.6): closed by policy 3.3 requiring an estimate.
- Own-cohort hazards, with fall 2023 hazards beyond the observed window, give CJ 31.5. Same side of the floor, nothing flips. This is the closest variant to the line.
- Not combining V-room sections, or using schedule Enrl: closed by policy 4.3 and the registrar notes.
- Narrative nit (non-blocking): the "eight" quoted for the raw route holds only with exits after term 9 excluded (Nursing 27.6). Counting all GR regardless of term gives Nursing 30.04.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 (13 plus manifest) | yes |
| Formats | 3 or more | 4 (csv 6, xlsx 5, pdf 2, txt 1) | yes |
| Large file | 25,000 rows or more | census registrations 28,135 rows | yes |
| Distractors in metadata.json | 2 or more, none named in a file | course_success_rates, service_area_occupational_outlook; neither is labelled a distractor in its file name | yes |
| Distractors unused yet weighable | yes | Both unused by the solution, per the thread. Neither answers a graded quantity (success rates and occupational outlook are not completion share, FTE or class counts). | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both in submission.md section 4 | yes |
| Asks multi-dimensional with unit and rounding | yes | Three asks, each over nine programs. One-decimal rounding is in the prompt, and the counts are integers. | yes |
| Prompt shape and 25 or more criteria | yes | Program-by-program grid, nine programs times three measures plus the list, call and chart, about 30 gradable cells. The rubric itself is not in the folder (not verified). | yes (inferred) |
| Reads as real work product, not LLM generated | yes | Thread found no authoring language and no temporal incoherence. Goldens not re-read by me. | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card, design note and pipeline.json: stump_class analytical, decisive step Aalen-Johansen cumulative incidence in place of 1 minus KM, with no decoy shipped. The distractors are not named as the surface read. Match. Gate G passes, and the difficulty survives deleting every wrong number because the pack contains none.

## Stump power (Gate F)
Moderate. 1 minus KM is the natural reflex and lands on one program, with the four transfer-oriented programs at 35 to 41. The raw-share route lands on eight and the fall-2023-only route on seven. Policy 3.3 ("estimate") and the registrar notes steer strong models toward competing risks, so expect some runs to land on the call. The asks add silent traps: Cr Hrs absent for lab, shop and clinical sections, the census program taken from the history file (900 rows differ from the extract), WC counting, V-room pairing and cancelled sections.

## Findings, ranked
1. No blocking finding.
2. The prompt's "go into review" list and the "taken together" and "estimate" wording close the pass 1 forks as filed.
3. Non-blocking: the "eight" wording in the recommendation's rejected-route sentence is true only when exits after term 9 are excluded. Consider adding "within nine terms" for exactness.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical. Design note `## Three rules`: Domain test (event history, competing exits), Layer 1 (2024 system conversion, readmissions, WD-to-TO lag), Layer 2 (estimand_identification, competing risks), analyst test ending on the one-program default, with No decoy, Not semantics and Not rule application each present. Match.

## Next action for the author
Proceed to stage 5: ship. Optionally patch the "eight" nit wording in the recommendation block in the same rebuild.
