# determinism-check report, task253, 2026-10-12 (pass 1)

## Verdict
DETERMINISTIC (the thread's verdict), with one fork the thread settled by the natural reading.
**Disposition:** FIX_NOW. The thread wrote APPROVE; this report overrides it under "our judge is the floor, not the bar" (a fork settled by the natural reading is a FIX_NOW, not a pass).
**Stumping type:** mechanism: statistical_rigor / method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The call (42 places, expected count 41.95) and every downstream figure recompute from the bundle, and the mean, median and mode of the count all give 42; the 28 (model averages) and 56 (raw averages) are rejected by the prompt's own "underlying average" definition and guidelines 2 and 3. One graded input is not filed: the prompt asks for "the Year 3 to 6 students the places will serve in 2027", and no shipped file says 2027 Years 3 to 6 are the August 2026 census Years 2 to 5. The thread reached 7,072 students by that roll-forward and called a literal reader's stop at the census Years 3 to 6 (6,946) "a minor fork, the natural reading". That is a fork closed by inference, so it is a FIX_NOW.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Participating Year 5 reading results | 30,956 | 30,956 | yes |
| Grand mean / school SD / year-group SD / student SD | 496.5 / 16.5 / 9.3 / 69.9 | 496.48 / 16.47 / 9.28 / 69.86 | yes |
| Sum of chances below 480 (the call) | 41.95, so 42 | 41.947 | yes |
| Schools with model average below 480 (default path) | 28 | 28 | yes (wrong path) |
| Schools with raw average below 480 | 56 | 56 | yes (wrong path) |
| Region shares (%) | 15.5, 25.6, 12.2, 16.7, 14.1, 15.9 (sum 100.0) | identical | yes |
| Students by region, total | 1,578; 3,530; 356; 768; 431; 409; 7,072 | identical | yes, only under the Year 2 to 5 roll-forward (not filed) |
| Hub students | 3,068; 2,243; 725; 671; 365 (7,072) | identical | yes, same dependency |
| Hub km | 813; 1,957; 1,826; 1,593; 2,138 (8,327) | identical | yes |
| Chart (Haskwick South longest, 2,138 km) | as claimed | consistent by derivation, PNG not read | yes (derived) |

## Competing answers that survived
1. Students served in 2027. Answer A (golden): census Years 2 to 5 rolled to 2027 Years 3 to 6, 7,072 (regions 1,578/3,530/356/768/431/409). Answer B: census Years 3 to 6 as printed, 6,946 (regions 1,503/3,379/373/458/809/425). The shipped rule meant to close it: none. Guidelines 1 names "Years 3 to 6", the census is as of August 2026, and no sentence says the cohort moves up a year level. The design note itself records "no filed rule speaks to it" (device A1). This changes every student figure and every hub student figure, and the kilometres are unaffected only because they are weighted by school chance, not students.
2. Hub assignment (2026 directory against the November 2026 plan): closed by the shipped facts (the directory predates Haskwick South's July 2026 opening, the plan is the 2027 servicing plan). Not a surviving fork.
3. Count summary (sum, median, mode): all 42, converged. Not a surviving fork.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files in pack | 10 or more | 13 | yes |
| Distinct formats | 3 or more | 5 (csv, xlsx, pdf, docx, txt) | yes |
| Largest table | 25,000 rows or more | 110,515 (naplan_results_2026.csv) | yes |
| Declared distractors | 2 or more, in metadata.json, not labelled in file names | 2 (literacy_specialist_rates_2027.xlsx, literacy_PL_register_2026.csv), no label in names | yes |
| Distractors look relevant and are unused | yes | same world as the decision (literacy programme staffing); none answers the call | yes |
| Deliverables | 1 to 3 | 2 (xlsx, png) | yes |
| Deliverables present | all named | golden/ holds both | yes |
| Asks multi-dimensional | yes | call plus shares, students by region, hub students and km, chart | yes |
| Units and rounding stated | yes | "whole numbers", "per cent to one decimal" | yes |
| Prompt length | under 1,000 characters | 820 | yes |
| Prompt shape and 25-criteria floor | 25 or more | shape 14, about 32 per the design note | yes (design-note arithmetic, not independently regenerated) |
| Realism | no LLM tells | thread saw none in the files it read; golden realism not re-audited here | yes, unverified for the golden |
| Input hygiene | no authoring disclosure | none seen by the thread | yes |

## Gate G reconciliation
Thread: method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: Gate G `method_or_model_selection`, strategy `uncertainty_hold`, stump_class analytical. They match for the main call. The one divergence is on the asks: the design note builds the graded students and kilometres asks on two declared devices (A1, the year a record describes, and B1, the stale directory) whose figures leave their bins under the natural read. A1 is a data-semantics device with no filed rule, which the thread rightly saw as the single un-filed bridge. The main call is analytical; the ask-level stump on students is not, and it is also a fork.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical. Design note: analyst_test reaches the 42 only by counting expected schools from probabilities, stump_class analytical. They match. Neither the declared distractors (which the thread did not name as the surface read) nor the stale directory carries the call.

## Stump power (Gate F)
The thread expects most solvers to commit to 28 (the filed model's natural output) or 56, so the main call is hard for the right reason. Its one pointer is the phrase "underlying average ... over many years", which tells a solver the target is latent. No too-easy signal beyond that. The design note's own pair arithmetic has the ask figures resting on A1 and B1, so closing the A1 fork by filing a rule lowers ask-level stump power for the students figures; the main-call stump is untouched.

## Findings, ranked
1. FIX_NOW, student roll-forward is unfiled. File as a fact (not a handling instruction) in `data_team_notes.txt`, beside the census entry, that census year levels are the 2026 school-year levels and that a cohort takes the next level at the start of the school year, with the census headcount the only enrolment source. This is the smallest closure: it states what the census year level means, so 2027 Years 3 to 6 = census Years 2 to 5 follows by reading and no fork is left on a graded ask. It keeps 7,072 and every regional and hub figure. Regenerate through `make.py`, not by editing target/. Tension to note: the spec lets an ask device (A1, D8) go unpinned by a filed rule (`supplemental-stumping` 2.2), but the determinism rule treats a fork our thread settles by the natural reading as a FIX_NOW, and the portal reads more strictly; this report applies the stricter rule. If the author judges A1 a legal silent device, the alternative is to accept the risk of a Gate D flag on the student figures.
2. Consequence of finding 1: the fix changes a shipped document, so a fresh solver round is required before the re-judge (the stump on the students asks falls, and the stage 3 assertions that A1 moves every region by at least 3 per cent need to be rewritten to treat A1 as a closed reading). Re-judge once after.
3. Minor, no action: hub assignment is closed by the plan's date and the directory's Hubs remark; keep both dates visible in the files.
4. Minor, no action: the PNG was outside the thread's allow-list; chart values follow from the ledger.

## Next action for the author
Add the one-sentence cohort roll-forward to guidelines section 1 in the generator, rebuild, rerun checks.py, then run a fresh solver round and one re-judge.
