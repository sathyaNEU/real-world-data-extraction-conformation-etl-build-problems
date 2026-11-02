# determinism-check report, task274, 2026-11-02

## Verdict
DETERMINISTIC on the thread's reading, with one open fork on the main call that the author must weigh (the thread's own first literal pass landed on the other answer). Thread verdict: DETERMINISTIC / APPROVE.
**Disposition:** FIX_NOW (reviewer overrides the thread's APPROVE: the main-call estimand fork below is unclosed in the shipped text; one wording closure, then re-judge once)
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every filed figure reproduces from the bundle (main call 56% / 38% / 18 pp, pilot scale; class, division, hours and restitution asks identical). The fork is the estimand: Resolution s3 says "on the courts' records as they stand on 31 August 2026" and "at its final disposition ... whether or not the case has reached its final disposition". The thread's literal pass gave 53.3% vs 17.7% = 35.6 pp (full scale); only after reading the filed blocks did it adopt the projection reading (18 pp, pilot). The design note's literal-reader paragraph argues the unreached-case clause would be idle under the as-recorded reading, which is a good argument but a real reviewer can still execute "every defendant counts" as open cases counted unconvicted. Nothing in prompt.txt closes it.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Offered / not offered | 1,801 / 1,807 | 1,801 / 1,807 (xlsx, 12 sheets) | yes |
| Not offered convicted at final disposition | 56% | 964/1,718 disposed = 56.1% | yes |
| Declined share, their conviction | 12%, 55% | 215/1,801; 114/206 | yes |
| Terminated cases convicted | 91% | 205/225 | yes |
| Final-review termination | 23% | 62/269 | yes |
| P(terminated in term) | 39% | 0.39 to 0.40 | yes |
| Offered convicted | 38% | 37.9 to 38.3% | yes |
| Reduction | 18 pp | 17.8 to 18.2 | yes |
| FY2026 classes | 1,962 / 655 / 1,219 / 1,125 / 947 | identical | yes |
| Divisions | 2,325 / 1,445 / 1,219 / 919 | identical | yes |
| Hours by site | 8,051 / 5,194 / 4,926 / 3,339 | identical | yes |
| Restitution by site | 37,165 / 33,175 / 25,530 / 19,325 | identical | yes |

## Competing answers that survived
1. Main call estimand. As recorded (open = unconvicted): 53.3 vs 17.7, 35.6 pp, full scale. Cumulative incidence at longest follow-up: 31 pp, full scale. Closed cases only: about 0 pp, lapse. Projected eventual shares (filed): 18 pp, pilot. Shipped rule meant to close it: s3 "whether or not the case has reached its final disposition". Closes it only by inference; the "as they stand" clause leaves the as-recorded reading executable. The method of projection is open by design, standing family 17.98 to 18.23, which is acceptable.
2. Section numbering follows offense date: recoverable from the data, not stated in prose (filing-date rule 5,826; convert-all 5,443; none 5,253). Keep the fork-table row.
3. Restitution gross vs reported net (115,195 vs 111,440) closed by agreement clause 6; January source recoverable. Site = report Location column.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000 rows | 28 files (13 top level), csv, xlsx, pdf, docx; docket extracts 53,371 and 49,380 rows | yes |
| Distractors | 2+ in metadata.json, no file name label | district_court_annual_statistics_fy2025.pdf, county_jail_population_2025_2026.csv; neither answers a graded quantity (thread: unused for the call) | yes |
| Deliverables | 1 to 3, all in golden | 2 (docx, png), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | prompt states whole points, per cents, cases, hours, dollars | yes |
| Prompt | one paragraph, under 1,000 chars | 949 chars | yes |
| Rubric 25+ criteria, prompt shape | 25+ | not generated at this stage; asks yield many gradable cells (reduction, 2 shares, 5 classes, 4 divisions, 8 site figures, chart) | not verified |
| Reads as real work product / not LLM generated | yes | thread found no authoring disclosure; golden realism not judged here | yes (thread) |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_strategy maturity_censoring, stump_class analytical, gate_g forecasting, layer2_family estimation_fit. Match. The declared distractors (district statistics, jail population) are not named by the thread as the surface read; the surface read it names is the as-recorded 35.6 pp. No finding.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. Matches the card's analyst_test and domain_test and the design note's Three rules (No decoy, Not semantics, Not rule application present). The thread reached 36 pp, not 18, with no judgment beyond reading the files, so the survival projection is the step a strong solver may or may not take; that is the stump, not a landable-call concern.

## Stump power (Gate F)
Thread: good. 1,236 of 1,801 offered cases are open against 89 not offered, so the recorded gap is a timing artifact. Easy routes file full scale (36 or 31) or lapse (closed only). Margin 18 vs 15 and 25 is clean; life-table variants stay at 17 to 18. Note the same open fork raises risk that a grader-side or solver reading as recorded files the wrong tier.

## Findings, ranked
1. Estimand fork (as-recorded 35.6 vs projected 18) is not closed by prompt.txt or a plain WHAT sentence; the thread itself first executed the other answer.
2. Offense-date numbering rule and gross-versus-net restitution are recoverable only from data and the agreement; ensure fork table rows and `checks.py` assertions.
3. Rubric count unverified.

## Next action for the author
Close finding 1 by filing the WHAT in the resolution text or prompt (the share each list's defendants will have convicted at final disposition, open cases included, not the share recorded by 31 August 2026), without filing the HOW, rebuild, and re-judge once.
