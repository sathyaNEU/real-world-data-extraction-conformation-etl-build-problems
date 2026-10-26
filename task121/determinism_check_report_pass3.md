# determinism-check report, task121, 2026-10-26 (pass 3, stage 4 round 2)

Bundle judged: target.zip md5 4eb36d04b220fc3258350d5d3f42d545, fresh unzip at /tmp/determinism-check-task121-s4r2-0cc1/target/. Thread verdict: /tmp/determinism-check-task121-s4r2-0cc1/verdict.md.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The call is forced by the shipped files. The rise (10.5 to 14.8 per cent) sits on shifts begun after a short turnaround: 31.1 per cent from March against 10.7 on rested shifts, which held at about 10.2 before March. Release 13.3 does not carry it, since rested shifts ran on it too. The roster's turnaround gap takes only two values (8 h, or 16 h and more), so any threshold from 9 to 15 hours picks the same shifts and "less than eleven hours" is not an open fork. Graduates, call mix, overtime and swaps, unit hours and case-review scores all fail on the data. Hygiene passes.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Under-triage Sep to Feb | 10.5 | 10.452 (1110/10620) | yes |
| Under-triage Mar to Aug | 14.8 | 14.760 (1471/9966) | yes |
| Quick-return share of shifts before / from March | 1.5 / 15.8 | 1.45 / 15.81 | yes |
| Rate on quick-return shifts from March | 31.1 | 31.07 (618/1989) | yes |
| Rate on rested shifts from March | 10.7 | 10.69 | yes |
| Rate on rested shifts before March | 10.2 | 10.17 | yes |
| Veterans before / from March | 10.4 / 14.5 | 10.37 / 14.49 | yes |
| Rate at the earlier protocol mix | 14.7 | 14.73 | yes |
| Ask A, 12 monthly P90 (121 to 130) | as submitted | all 12 | yes |
| Ask B, 12 monthly medians | as submitted | all 12 | yes |
| Ask C, 12 monthly shares | as submitted | all 12 | yes |

Sources: CAD calls, ePCR, call_takers, roster, unit history, CHE call detail, TCPR reviews.

## Competing answers that survived
No fork flips the main call. Four residual reading forks on the asks, each closed by a shipped definition:
1. Pooled period rate (10.5 / 14.8) against mean of monthly rates (10.4 / 14.7): QA programme defines a ratio of counts, so pooled. Touches the xlsx rate cells only.
2. Ask A per incident against per call: data dictionary defines che_call_id as the call, QA programme says "the month's medical calls", so per call.
3. Ask C including or excluding TG05: centre_reference.xlsx labels TG05 "911 calls", so included. Excluding it moves Nov, Dec, Mar, Jul by 0.1.
4. QA7 conversion against dropping QA7: conversion is evidenced in the data (no QA7 seconds above 59, against 182 of 488 others).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 4 (CSV, XLSX, PDF, TXT) | yes |
| Large file | 25,000 rows or more | CHE call detail 148,589 rows | yes |
| Distractors | 2 or more in metadata.json, no file name labels one | protocol_case_reviews and ems_unit_hours named; names carry no label | yes |
| Distractors unused yet weighable | unused, a shipped fact rules out | thread: relevant but unused; case-review scores flat, unit hours do not move the cause. Whether one reproduces a graded quantity arithmetically was not tested by the thread (not a defect, noted) | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | three 12-month series plus two rates; prompt states per cent to one decimal and whole seconds | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | card shape 18; design note counts 47 criteria | yes |
| Not LLM generated, goldens real | | thread saw no authoring language; mixed date formats, UTC, undashed keys read as exports. Golden realism not independently re-read here | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_strategy causal_design, estimand_identification, stump_class analytical; default path ends on protocol release 13.3, golden the quick returns. Match. The surface read the thread names (release 13.3, then the academy cohort) is the design note's default path, not a declared distractor; the declared distractors (protocol_case_reviews, ems_unit_hours) are not load-bearing for it. No shipped artifact ranks the candidates (note section on Gate G says none states a cause or rate by shift). No finding.

Gate H: thread `domain: pass, layers: pass, decisive_step: analytical`. Card and note: domain test (rest between shifts, quick return under eleven hours, a person's sleep), Layer 1 (UTC and local, undashed ePCR key, split incidents, transfer legs), Layer 2 (exposure varying inside the period against a coincident go-live). Match. The thread reached the golden by building rest from consecutive roster rows, a choice of estimand the data had to settle, not by executing a filed rule.

## Stump power (Gate F)
Thread: moderate to good. Easy routes are release 13.3 (pre/post puts 13.3 calls at 14.7 against 10.5) or the academy cohort; a solver who never derives rest from consecutive roster rows lands there. The asks carry independent silent devices (overwritten unit_assigned, split calls, QA7 keying, transfer legs, TG07, UTC against local, ePCR key). The rotation-by-rest method is the field's standard fatigue exposure, so the blind readers' result should be weighed with this by the main thread.

## Findings, ranked
1. None blocking.
2. Optional, rubric: "2026 rotation" in the golden is not stated in any shipped file; graders should accept "short rest between shifts / quick returns".
3. Minor: the thread computed rested shifts on release 13.3 at 10.6, while the golden says rested shifts "ran on the release too" with 10.7 from March; the 10.7 reproduces as the all-rested rate from March, so no figure is wrong.

## Next action for the author
Proceed to ship; add the rubric note that "short rest between shifts / quick returns" is accepted for the cause.
