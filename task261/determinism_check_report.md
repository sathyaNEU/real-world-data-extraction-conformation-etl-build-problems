# determinism-check report, task261, 2026-10-15

## Verdict
DETERMINISTIC (main call and docx/svg/xlsx asks 1 and 2 forced; xlsx ask 3 carries two narrow edge forks)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Literal execution of the brief (older of reference person and partner, six groups, 1.96 x SE of the difference, SE per user guide 7.2 applied to the difference itself) gives 55-64 vs 65-74 at ratio 2.71 (kept apart) and 65-74 vs 75+ at -1.56 (shared): five segments. Margins are stable under every reasonable variant tried. The independent-errors route gives 1.57 and four segments; it is a wrong method (replicate-median correlation 0.70), not a competing reading. The two forks sit only in the customer-count ask (xlsx ask 3) and do not touch the call.

## Recomputation ledger
Judge method: weighted median = first value where cumulative weight reaches half the total; 5 implicates averaged; sampling variance from 200 replicate weights on implicate 1; imputation variance divisor 4, x1.2. The user guide's Queensland worked example reproduced exactly.
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Medians U35, 35-44, 45-54, 55-64, 65-74, 75+ ($000) | 69; 281; 534; 790; 1,048; 815 | 69,233; 281,337; 533,999; 790,343; 1,048,229; 815,286 | yes |
| SE of medians ($000) | 7; 25; 50; 93; 136; 139 | 6,655; 24,831; 50,385; 92,827; 135,820; 139,158 | yes |
| Adjacent diff / SE / ratio | 212,104/23,733/8.94; 252,663/45,354/5.57; 256,343/76,861/3.34; 257,885/95,175/2.71; -232,943/149,133/-1.56 | same | yes |
| Independent-error SE, 55-64 vs 65-74 | 165,000 (1.6) | 164,511 (1.57) | yes |
| Replicate-median correlation | 0.70 | 0.699 | yes |
| SVG interval 65-74 vs 75+ | -525,000 to 59,000 | -525,244 to 59,358 | yes |
| Pension households 55-64 / 65-74 / 75+ | 442 / 1,168 / 746 | same | yes |
| Pension balance | 207,655,000 / 520,479,000 / 249,568,000 | 207,654,6xx / 520,479,1xx / 249,567,9xx | yes |
| Annual payments | 11,448,000 / 30,320,000 / 17,994,000 | 11,447,850 / 30,319,980 / 17,994,300 | yes |
| Annuity households / income | 176 / 467 / 284; 3,606,000 / 9,011,000 / 5,614,000 | 176 / 467 / 284; 3,606,196 / 9,011,085 / 5,613,884 | yes |

Source files: nhws2025_household_summary, persons, replicate_weights, user guide s.7.2, brief; crm_clients (status, date_of_death, merged_into), ria_nominations, PDS s.5, annuity key facts indexation table, data dictionary ("as at the pull"). The customer figures reproduce only under the golden's reading (merged ids followed; deaths on or before 31 Dec 2026 excluded; reversionary pension kept only with a Reversionary nomination; non-client partner from a Spouse or De facto nominee of ANY nomination type for single-client households; annuity amount divided back by 3.1% CPI or 2.5% Fixed for anniversaries 1 to 12 Jan 2027).

## Competing answers that survived
All on xlsx ask 3; none touches the call.
1. Partner source. Golden: Spouse/De facto nominee on any nomination type. Alternative: Reversionary nominations only gives 446 / 1,174 / 736 pension households; ignoring non-client partners gives 455 / 1,184 / 717. No shipped file says a Binding or Non-binding Spouse nominee identifies the partner (PDS speaks only of the reversionary). Unpinned.
2. Partner who died in December but is still nominated as spouse (4 households, e.g. RIA4737307, RIA5007964). Counting the dead partner's age gives 441 / 1,169 / 746. The brief says "at that date" but not that a deceased partner is excluded.
3. Annuity anniversary on the pull date, contract LA484722 (CPI, 12 Jan 2021 start, $21,708, 75+). Increase applied: 75+ income $5,613,884 (rounds $5,614,000). Not applied: $5,614,536 (rounds $5,615,000). One rounded figure flips.
Closed, not forks: annuity increase not taken back (forced by dictionary "as at the pull" plus key facts); survivor pension counted only for December deaths (forced by PDS s.5).
Main-call check: placing by reference person (bulletin basis) gives ratio 0.81; ruled out by the brief, so a Layer 1 lower step, not a fork.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 4 (csv 8, pdf 4, xlsx 2, docx 1) | yes |
| Large file | 25,000+ rows | 29,940-row household extract, plus 5,988 x 200 replicate file | yes |
| Distractors in metadata.json, none named in a file name | 2 or more | nhws2025_results_bulletin.xlsx, retirement_customer_research_2026.pdf | yes (file name of the bulletin is the survey's own, not a label) |
| Distractors unused yet weighable; wrong basis ruled out by a shipped fact | yes | bulletin reproduces on reference-person basis, ruled out by the brief | yes |
| Deliverables | 1 to 3, all in golden | 3 (docx, xlsx, svg), all present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | per-group counts, balances, payments, incomes; nearest thousand stated | yes |
| Prompt shape and 25+ criteria | identifiable, 25+ | prompt 897 characters, one paragraph; rubric is generated downstream and not countable here | not verifiable here |
| Reads as real, not LLM generated | yes | judge found no authoring or benchmark language; goldens not reviewed for realism by this check | yes per judge |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card and design note: stump_class analytical; the decisive step is the SE of the difference of two correlated medians (replicate-wise recomputation, ratio 2.71, five segments) against summing two SEs (1.57, four segments). Match. The declared distractor (the bulletin) is not the surface read carrying the task: it changes the structure but the brief rules it out. The distractor is not too load-bearing. Gate G: no shipped artifact ranks the candidates wrongly beyond the declared wrong-basis bulletin; PASS.
Note for the author: the design note's "Not rule application" line says no filed rule gives the error of a difference. The judge read guide s.7.2 ("compute the estimate again with each replicate") as directly executable on the difference, so a literal executor can reach 2.71. This is consistent with the call being determined, but it narrows the stump toward rule execution; the thread still rated the decisive step analytical because the easy route (adding SEs) is the common wrong one.

## Stump power (Gate F)
Good. The covariance of neighbouring medians (shared areas) is what the easy route misses; the reference-person bulletin is a second easy wrong route. The ask-3 conventions should hold each solver to a fraction of the ask weight.

## Gate H
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Swap test fails to preserve the task (replicate-weight variance of a difference of weighted medians in a household wealth survey is survey statistics). Layer 1: five implicates, replicate file, top-coded ages, merged CRM records, reversionary pensions, January annuity amounts. Layer 2: SE of the difference of two correlated medians.

## Findings, ranked
1. Customer-count partner convention unpinned (Spouse/De facto nominee on any nomination type; dead partner excluded). Shifts pension household counts (e.g. 446 / 1,174 / 736, or 441 / 1,169 / 746).
2. Annuity increase on an anniversary falling on the pull date (12 Jan 2027, LA484722) unpinned. 75+ income rounds to $5,614,000 or $5,615,000.
3. Minor tension between the design note's "no filed rule gives the SE of a difference" and guide s.7.2 being literally applicable to a difference.
No finding on the main call, svg, or xlsx asks 1 and 2.

## Next action for the author
Add one sentence each to the brief or data dictionary (text only, no data change): (a) for a household with one client record, the partner is the Spouse or De facto partner nominee on any of its pension nominations, placed by the nominee's date of birth, and a partner who died on or before 31 Dec 2026 is not counted; (b) an annual annuity amount includes any anniversary increase falling on or before the pull date of 12 Jan 2027 (or move the boundary contract off the pull date). File the WHAT only. Rebuild twice for byte identity, then one re-judge.
