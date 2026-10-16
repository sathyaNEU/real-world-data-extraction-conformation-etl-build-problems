# task189 determinism check

One isolated judge thread per pass, seeing only a fresh unzip of `target.zip`, `prompt.txt`, the
graded blocks of `submission.md` and the judge system prompt. No pass saw the design note, the card,
`metadata.json`, the generator or an earlier report.

## Pass 1: NOT_DETERMINISTIC, SEND_BACK

**Gate H passed** (domain pass, layers pass, decisive step analytical) and the thread confirmed the
stump has real analytic content: "substituting half the limit gives 7, treating non-detects as absent
gives 3, and dropping them gives 8. A solver who substitutes will miss 4 ... differing limits by
laboratory make substitution a function of which lab holds the points." **Gate G**:
`statistical_rigor`, `analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`,
"it would pass Gate G once the estimator is pinned".

The determinism block failed on one finding and three write-up defects.

| Finding | What the thread showed | Repair |
|---|---|---|
| The licensed readings diverged | Kaplan-Meier and regression on order statistics gave 4; a lognormal maximum likelihood fit's own distribution mean gave 5, adding Ballynure at 0.0532. "Neither the prompt nor any file selects between them." | Two moves. Clause 7.2 now files the estimand's unit: the average is "the mean of the concentrations of the compliance samples ... one concentration for each of those samples", and the authority "shall not report in place of the average any property of a distribution fitted to them". And Ballynure's pressure was lowered so the parametric reading converges as well: all five readings now give 4, every water body 12 per cent or more clear of the standard, asserted in `checks.py` and `verify.py`. |
| The nitrate basis rested on an outside constant | "No shipped file states the conversion factor. With a factor of 4.4, Sheskin's count falls from 19 to 17." | The field dictionary's determinand line now states that a result under `NO3N` is 4.4268 times smaller than the same water under `NO3`. Asserted (SF14). |
| "The export holds" had a second reading | 242 under the compliance and approval filters, 267 over all rows, 255 over FIELD only. | The ask now reads "how many the export holds for that quarter as approved results". The three figures are unchanged. |
| Step 5 contradicted the recommendation | It said results below a limit are "held at its own limit", which is the route that gives 11. | Step 5 now says the result is treated as "an observation known only to lie below the limit that row carries rather than as a value". |
| Critical component 3 did not reproduce | "nearest compliant 19 per cent below" was an artifact of one estimator; Kaplan-Meier puts Ballynure 31 per cent below. | The component now states what every reading agrees on: the four water bodies exceed under each of the four readings, and every water body is at least 12 per cent clear of the standard under all of them. |
| Step 1 named a file that does not ship | `sample_point_crosswalk.csv` against the shipped `monitoring_point_crosswalk.csv`. | Corrected. |

Files and hygiene passed in pass 1: "14 files, formats csv, json, pdf, xlsx. One 25,524-row csv.
Distractors present ... No authoring leakage seen. Fiction dates are coherent."

The repair moved no graded figure except the two the thread showed to be wrong: Ballynure's
below-limit count (33 to 35, after the pressure change) and the below-limit total (274 to 276). The
call, the four named water bodies, the rungs and every other ask figure are unchanged.

## Pass 2: NOT_DETERMINISTIC on one ask, FIX_NOW

The second thread recomputed everything from the bundle and found the **main call forced**: "Every
estimator that keeps a bounded result bounded gives these same four", with its own four estimators
(lognormal MLE, Kaplan-Meier on the flipped sample, a same-month fill from the sensitive method's
quantified results, and a conditional-mean fill) all giving Cloonfad, Glasheen, Kilcrohane and
Owenbeg, the tightest margin Owenbeg under Kaplan-Meier at 12 per cent over. Critical component 3
reproduced. The constant substitutions reproduced at 7, 11, 3 and 8. Asks 1 to 3 and ask 5 reproduced.
**Gate G** passes (`method_or_model_selection`, `analytical_non_defect`, no surface-read dependency,
no sole data defect): "the difficulty is censored-mean estimation on honest data ... Clean data would
still stump, because the censoring is in the data itself, not a planted defect." **Gate H** passes
(`domain: pass`, `layers: pass`, `decisive_step: analytical`).

It recorded the half-limit route as the main residual and did not fail on it: "regulation 7.2 does not
name a method ... I judge it excluded by the data, because the answer under any constant is a function
of which laboratory holds the points ... This is a method-selection stump on honest data, not a
wording fork."

The verdict failed on a rendering defect of mine, not on the design:

| Finding | What the thread showed | Repair |
|---|---|---|
| The nitrate basis was clipped off the page | "The dictionary cell for determinand_code is cut off at 'so a result under NO3N is 4.' on the page and in text extraction. The factor 4.4268 survives only in the clipped content stream. A solver using the usual 4.43 files 50.8 for Ballynure Borehole 1 and 28.6 for Moneycashen Intake." | Every cell of every shipped table is now a flowable that wraps inside its column, so no cell overflows its page. `checks.py` asserts the factor's whole sentence and each of nine field rows survives extraction. |
| The method schedule's rows overlapped | "overlapping text in the Tirneevin rows (cosmetic) ... it reads as a generated layout." | Same wrapping fix, with the method-code column widened so no code breaks across lines; asserted for all five method codes. |
| Ask 5's population was not forced | "the export holds 12 more approved OPO4 rows in the quarter that are QC types ... Counting them gives 254 and 30 in only one ... the ask never says so." | The ask now reads "how many ortho-phosphate results on water samples", which puts the quality-control rows plainly outside it. The three figures are unchanged. |

No graded figure moved in this pass. The call, the thirteen verdicts, the per-water-body counts, the
nitrate figures and the quarter's three figures are the same before and after.
