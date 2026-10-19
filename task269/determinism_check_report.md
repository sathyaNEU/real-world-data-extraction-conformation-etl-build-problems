# determinism-check report, task269, 2026-10-19

## Verdict
NOT_DETERMINISTIC (no SOLUTION_WRONG: every golden figure reproduces)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The decisive estimand, which departures count as a branch-route boarding's wait, is filed nowhere in the shipped text. Standard v4 s3.2 works a boarding's wait "at the last timing point" from the revised departures and the timetable in force. Read word for word, that is all departures at the timing point in the direction of travel, and it files routes 7, 14, 31, 40 (route 3 fifth). The golden (3, 7, 31, 40) holds only under the unfiled branch-conditioned reading, where each outbound tag-off is placed in the two branches' stop patterns. That is a competing defensible answer (underspecified_objective). It affects the main call and asks 1, 2, 3. Filing the estimand as a rule would turn the decisive step into rule application, so the step has to be redesigned, not patched.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Corridor boardings, weekday peaks 10 to 21 Aug | 66,404 | 66,404 | yes |
| Excess wait R3/7/9/14/22/31/40/52 | 1.0/1.1/0.8/0.7/0.6/1.5/1.1/0.4 | 1.010/1.096/0.814/0.695/0.604/1.493/1.087/0.388 | yes |
| Shifts, same route order | 205/160/103/167/165/106/209/101 | identical | yes |
| Pilot cost, same route order | 59,702/47,275/28,316/47,414/47,368/28,381/59,728/28,274 | identical | yes |
| Route 14 branch-bound 0.1 vs 1.6 | stated | consistent with the judge's cells | broadly |

## Competing answers that survived
1. **Which departures serve a boarding (main call).** Branch-conditioned via tag-off gives 3, 7, 31, 40. The literal s3.2 reading (all departures at the timing point) gives 7, 14, 31, 40 (R14 1.35, R31 2.19, R7 1.34, R3 1.01 fifth). Nothing shipped closes it: guidelines 2.3 and standard 3.1 to 3.3 name no serving-bus set, and standard 2.4 mentions tag-off only for the default fare.
2. **Pilot cost (ask 5).** "What the pilot cost there" read as post charges only, without the fee share: route 3 is $54,754, not $59,702. The pilot plan files the fee share only "for reporting by route". This is an ask and does not move the call.
3. **Boardings with no tag-off (ask 3).** Placement is unfiled and the cell average is used. The call holds under every handling tried; the judge's route 14 and 31 figures move by 0.02 or less.
4. **First release instead of revised.** The call holds, but ask 3 figures move (R14 0.76, R31 1.59). The standard rules this out, so it is closed.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | csv, xlsx, pdf, zip(GTFS txt), txt | yes |
| Large file | one of 25,000 or more rows | ticketing 123,997 rows | yes |
| Distractors | two or more named in metadata.json, none labelled in a file name | service_performance_report_august_2026.pdf, customer_feedback_term3_2026.xlsx; neither name labels it | yes |
| Distractor behaviour | unused by the solution, relevant, ruled out by a shipped fact | the judge found both unused; the August report ranks by on-time running, not excess wait. The first-release AVL is an extra Layer 1 alternative, not a declared distractor | yes |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 8 routes by 3 measures, each with unit and rounding in the prompt | yes |
| Prompt shape and 25 or more criteria | identifiable | criteria are generated downstream; the shape (every route and cell graded) supports it, but I could not count them | not verifiable here |
| Reads as real | no LLM tells, goldens real | no authoring leakage found by the judge; I did not open the golden files | not independently checked |

## Gate G reconciliation
Declared by the note: Layer 2 is field_method, the common-lines wait over each rider's attractive set; the easy path is route-level excess wait, giving 7, 14, 31, 40. Thread: mechanism method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. These match, and the declared distractors are not named as carrying the task. The mismatch is on the line below.

## Gate H reconciliation
The thread says domain pass, layers pass, decisive_step analytical, only if the estimand is the unit of analysis. The design note's `## Three rules` says "no rule or procedure says over which departures a rider's wait is worked", and its fork table has no row for it (SF1 to SF14 do not cover it). The note therefore admits the decisive rule is left unstated against a stated one. CLAUDE.md names that as a banned hidden rule, and `guard.py` blocks it. The thread read it as a reading fork; the note's own wording makes it the hidden-rule stump as well. The note's "Not semantics" and "Not rule application" lines argue the opposite from the same fact, but only the unfiled-rule reading survives the literal read.

## Stump power (Gate F)
The easy all-departures reading is the literal reading of s3.2, so a strong solver who executes the text exactly files the wrong answer (7, 14, 31, 40). That is a text-licensed fork, not a method error against a clear spec. The cut margin under the golden reading is clean (route 3 at 1.01 vs route 9 at 0.81). Pilot shifts and costs are deterministic and need no change.

## Findings, ranked
1. Main call turns on an unfiled population choice, so both answers are defensible from the files (SEND_BACK).
2. The design note's fork table lacks a row for it, and `precut.py` should have refused the note. The note's no-rule claim and the fork table conflict.
3. The pilot cost scope (fee share) is ambiguous for ask 5.
4. The no-tag-off handling is unfiled for ask 3, which is harmless to the call.

## Next action for the author
Re-root the main call's decisive step so it does not depend on an unfiled rule. One option is to file the WHAT, the serving-departure population (a boarding waits for the buses that can carry it to its destination stop), and move the stump to a genuinely analytical step elsewhere, such as validation or censoring. Do not file the HOW. Also state in the prompt or pilot plan that cost includes the coordination fee share, and add fork rows for both.
