# determinism-check report, task272 (architecture 2), 2026-10-21

This report replaces the architecture 1 report at the coordinator's instruction (that verdict is kept in the design note's "Architecture 1 record"). No repair follows: both isolated scored readers landed the call (16 grants, the golden set), so Gate F is spent for architecture 2. This report is the evidence record.

## Verdict
DETERMINISTIC (main call, asks 1 and 2 forced; asks 3 and 4 reproduce but rest on conventions the shipped guide does not state or contradicts). No SOLUTION_WRONG.
**Disposition:** APPROVE on determinism (the judge's own disposition, accepted). The architecture is still spent on Gate F.
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated judge rebuilt 92,053 first-review counsellor decisions. It put each application's three-month income on a twelve-month basis with a region x kind-of-work calendar fitted on the 2024 and 2025 first reviews. Applying the 200 percent limit gave 63,832 in-limit applications and 4,005 owing more than half. Sixteen hospitals sit at or above 6.0 percent: the lowest qualifier is H24 at 7.27 and the highest non-qualifier is H13 at 4.96. The answer is 16 grants, USD 1,024,000. The result holds across estimator choices (mean, median, geometric mean, dollar versus guideline share, 2024 only, 2025 only, hospital x work), so the margin is not a near tie.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| First-review counsellor decisions 2025 | 92,053 | 92,053 | yes |
| In-limit on twelve-month income | 63,832 | 63,832 | yes |
| Denied or 25 percent among them | 4,005 | 4,005 | yes |
| Qualifying hospitals | 16 (H02 H08 H10 H11 H12 H14 H15 H17 H20 H22 H23 H24 H26 H28 H29 H30) | same 16 | yes |
| Budget | 16 x USD 64,000 = USD 1,024,000 | same | yes |
| Ask 2, Yes/No for 31 hospitals | golden | matches | yes |
| Ask 3, write-off net of reversals, total thousands | 299,646.9, all 31 to 0.1 | matches only under the golden attribution | yes, with fork (Finding 3) |
| Ask 4, denials for documents not received | 3,558, all 31 | all 31 match | yes, with fork (Finding 2) |
| Policy yearly figure as twelve-month income | 5 (design note) | 5 | yes |
| One calendar per kind of work | 10 (design note) | 10 | yes |
| One calendar per region, or per hospital | 10 (design note and submission section 1) | 4 | NO (Finding 1) |

## Competing answers that survived
- Main call: none. Every estimator in the family files the same 16. The wrong readings file 5, 10 or 4 hospitals, and the data separates them. For example, farm work peaks Oct-Dec in Central Washington but Aug-Oct in Northwest Washington, so a pooled calendar is visibly mis-specified.
- Ask 4: a literal reader of data guide section 5 ("one list, 1 = documents not received") gets 3,003 (2,875 on first reviews only) against the golden 3,558. The data show the codes swap on 1 July 2025 (code 1 is 89 percent income above 400 percent of guideline before July; code 2 is 100 percent after). No shipped file states the renumbering. The golden is the data-true reading.
- Ask 3: (a) not collapsing the repeated write-off lines gives 603,992 thousand. Collapsing is evidenced by lines exceeding their account balance. (b) The golden credits each line to the household's last approval decided before posting. The guide's literal "posted under application_id" reading gives 299,022.1 thousand, and all 31 hospitals differ at one decimal. The re-attribution is evidenced: 95 lines post under denied applications, 17 under pends and 397 under superseded earlier approvals.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 (11 data files plus the contents.txt manifest) | yes |
| Formats | 3 or more | csv, pdf, xlsx (plus txt) | yes |
| Large file | 25,000 or more rows | Willamette hub 66,020; Puget hub 74,714; Columbia hub 73,184; adjustments 163,305; accounts 152,552 | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | fac_patient_experience_by_payer_2025.csv and state_charity_care_filings_fy2025.xlsx; neither name labels it | yes |
| Distractor behaviour | unused, weighable, ruled out by a shipped fact | Both are unused and answer other questions (patient experience, state charity-care filings). The judge did not read either as carrying the task. I did not independently test whether the state filings reproduce a graded quantity. | yes (partly checked) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png) | yes |
| Asks | multi-dimensional, unit and rounding stated | 31-hospital lists; thousands to one decimal; whole counts | yes |
| Prompt shape and rubric | identifiable, 25 or more criteria | Shape is a per-hospital qualify-and-quantify table. About 94 gradable figures, with figures_check at 85 of 85 as reported by the coordinator. The generated rubric itself was not inspected. | yes (inferred) |
| Reads as real, not LLM generated | no | The judge found nothing planted-looking. Provenance is CC0, constructed, with source and date recorded. | yes |

## Gate G reconciliation
The thread's line is method_or_model_selection / analytical_non_defect / surface_read_dependency no / sole_data_defect no. This matches the design note (Layer 2 method_or_model_selection; decisive step is each region's seasonal calendar for each kind of work) and the Gate H test fields in the note. The declared distractors are not the surface read: the surface read is the policy's quarter-times-four, a different estimand drawn from the shipped hub fields, not a distractor. Reconciled with no mismatch on Gate G.

One mismatch in a supporting claim (Finding 1): the design note's ladder row R1f and the submission's section 1 say a per-region or per-hospital calendar files 10. The judge's recompute files 4. Neither number is the golden, so the call is unaffected. The submission's text is not reproduced.

**Gate H:** domain: pass, layers: pass, decisive_step: analytical.
- Domain: putting a short-reference-period income on an annual basis with a seasonal calendar is a real income and poverty measurement step. The swap test fails (other fields' nouns do not fit).
- Layers: Layer 1 is hub schemas, UTC versus Pacific, the H23 hub move and crosswalk, repeated and twice-loaded adjustment lines, and the renumbered denial reasons. Layer 2 is the twelve-month income estimated from a seasonal three-month proxy.
- Three rules: no decoy (no shipped table states a share or seasonal factor); not semantics (every field read correctly still leaves the twelve months unrecorded); not rule application (no filed rule says how to estimate twelve months from three).
- Design-note agreement: the note's Three rules, analyst test (5 grants on the easy route) and domain test agree with the thread.
- Caution: the criteria file the estimand but not the method. A literal executor who skips the conversion files 5. This is judged analytical because the data itself shows and separates the calendars.

## Stump power (Gate F)
The judge rates it strong: the tempting paths file 5, 10 or 4 hospitals, and only region x kind-of-work gives 16. Measurement says otherwise. Both isolated scored readers landed the call with the golden set, so architecture 2 is spent on Gate F. The method is a recognised seasonal-adjustment route, a textbook one that a strong solver takes, and no judgment beyond applying it was needed to reach the golden. The asks 3 and 4 devices (collapsing repeated write-offs, household re-attribution, the 1 July renumbering) are the remaining places a reader can miss. The coordinator weighs that against the scored readers' per-ask results.

## Findings, ranked
1. Wrong-answer counts not reproduced (low to medium, no effect on the call): the submission (section 1) and the design note (ladder R1f and the stump sentence) say a per-region or per-hospital calendar finds 10. The judge's recompute finds 4. The golden and the 16 are unaffected, but a stated competing count fails reproduction and the claim should be corrected or dropped.
2. Ask 4, undocumented renumbering (medium): the guide contradicts the data. The golden 3,558 follows the data; the guide-literal reading gives 3,003. Recoverable from the data, but the shipped text points the wrong way.
3. Ask 3, unstated collapse and attribution rules (medium): collapsing repeated lines is required, and crediting the household's last prior approval (rather than the posting application_id) moves every hospital's figure. The guide-literal total is 299,022.1 against 299,646.9. Asks are exempt from the three-rules ban but this is a literal-reader fork.
4. Criteria 2.3 and the standard clause (low): "income standard from 1 January 2026" points to a standard not in the package. The twelve-month conversion is nowhere stated, which is the intended analytical gap, but the clause is loose.
5. Rounding note (minor): 299,646.9 is the unrounded-sum total (299,646.943). The sum of the rounded per-hospital figures is 299,646.6, so graders should expect the difference.

## Next action for the author
No repair follows: architecture 2 is spent on Gate F, so record this report as its determinism evidence. If any text is reused in a redraw, correct the competing-count claim in Finding 1, drop the guide's "common list" claim for the denial reasons, and file the WHAT (not the method) for the write-off attribution.
