# determinism-check report, task464, 2026-10-28

Pass 9: the single re-judge licensed by `/fix-determinism` after the portal's determinism return on this
build. Bundle judged: `target.zip`, md5 `ab3f7d9afa77303ad3b4b8888f1eda6c` (14 files), with `prompt.txt` and
the five graded blocks of `submission.md`.

## Verdict
**NOT_DETERMINISTIC**
**Disposition:** SEND_BACK
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The thread's Gate C/E failure is on FINAL_RECOMMENDATION. `statin_continuity_sessions_brief.pdf` files the
estimand (population, outcome, window, unit, rounding) but, by design (the 2026-10-28 determinism repair
recorded in `DESIGN_NOTE.md`), leaves the forecasting method open. SOLUTION_STEPS 2-4 execute that method
with several specific numeric parameters -- a 60-day re-authorisation grace window, a "150 days per 28 days
of statin supply" stop-between-reviews threshold, each patient projected forward "at the record's mean
request interval," and each chance scaled "by the record's seven-month stay on the register" -- and the
thread found no shipped file states, implies, or forces any of these specific numbers (grepped every input).
Marrick House Surgery's raw population (1,648) trails Fennbridge Medical Centre's (1,961) by about 19%, so
the thread judged a differently-but-reasonably parameterized hazard construction a defensible competing
answer under Gate C, taxonomy `competing_defensible_answer` / `underspecified_objective`.

This finding is not fully corroborated by the thread's own recomputation: by its own account it did not
execute the full forward-projection chain (SOLUTION_STEPS 3-5) or the R1/R2 reconstruction (6-7) within its
time budget, so the "plausible competing construction" is argued, not demonstrated by computing a second,
divergent hazard. Ask 1's population figures and critical component 2 both reproduced closely from the raw
files; the unresolved piece is specifically whether the forecast's free parameters are robust, which the
thread flags as a risk rather than a confirmed fork.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Ask-1 population, all 7 practices | P81066 1,017 / P81177 829 / P81283 877 / P81402 1,961 / P81555 1,648 / P81719 1,192 / P81940 1,124 | Same, derived blind from `patient_register_2026-12-01.csv` read as a multi-spell history (16,005 rows / 15,864 unique patients) before opening the submission blocks | Yes, exact match on all 7 |
| Critical component 2: Marrick House 1,232 of 1,648 on a Feb/Mar 2026 six-issue 56-day repeat | 1,232 | 1,303 raw six-issue/Feb-Mar-2026 statin repeats at Marrick House, 1,243 intersecting the ask-1 population (within ~1%) | Plausible, not exact; thread attributes the gap to a dose-in-mg-to-strength join trimming 112-day-supply rows, not independently confirmed |
| Forward-projection chain (steps 3-5), expected non-reissue counts, all 7 practices | Marrick House largest, Cobbet Street second | Not executed (time budget) | Not attempted |
| R1 (ACE inhibitor/ARB adherence), all 7 practices | 81.0 / 80.3 / 81.9 / 77.8 / 79.9 / 75.8 / 92.9 | Not executed (time budget) | Not attempted |
| R2 (ticagrelor post-anniversary), all 7 practices | 80 / 80 / 82 / 74 / 83 / 64 / 60 | Not executed (time budget) | Not attempted |

## Competing answers that survived
- **Fork:** the main call's forecast method (how the forward window's non-reissue chance is modeled) is open
  in the shipped files; the thread names four specific unfiled parameters (60-day grace window, 150-day/
  28-day stop threshold, mean request interval pacing, seven-month retention scaling) and argues, without
  computing it, that a differently-parameterized construction could put Fennbridge Medical Centre (raw
  population 1,961) ahead of Marrick House Surgery (1,648). No second construction was actually computed to
  show the two answers; this is a named risk, not a confirmed fork, and the rule the judge brief gives for
  this is "a thin-and-contested margin (multiple valid estimates whose range straddles the line)" -- the
  thread did not establish that the range straddles the line, only that the line has no filed convention
  closing it from the shipped package alone.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | >=10 | 14 | Yes |
| Format mix | >=3 formats | csv, jsonl, pdf, xlsx (4) | Yes |
| Large file | >=25,000 rows or large DB | `repeat_issues_system_a...csv` 300,753 data rows; `repeat_issues_system_b...jsonl` 202,203 lines; both repeat-authorisation extracts ~33-35k rows | Yes |
| Distractors named, not in filenames | >=2 in `metadata.json`, none labelled by filename | `metadata.json.distractor_files`: `qof_cvd_achievement_2025-26.csv`, `dispensed_items_cvd_2025-26.csv`; neither filename says "distractor" | Yes |
| Distractor relevance/arithmetic-reproduction-and-rule-out | each distractor unused yet relevant; one reproduces a graded quantity and is ruled out by a shipped fact | `DESIGN_NOTE.md` (lines 471-472) records both as "harmless" (QOF indicators and dispensing totals measure nothing about statin stopping) but does not demonstrate the arithmetic-reproduction-then-ruled-out shape explicitly | Not independently verified this pass |
| Deliverables | 1-3, all present in golden | 2 (`statin_sessions_2027.xlsx`, `cvd_repeat_returns_2025.csv`), both present in `golden/` | Yes |
| Asks multi-dimensional, unit+rounding stated | yes | prompt states "to one decimal place" / "to a whole number"; asks resolve across 7 practices x 2 metrics each | Yes |
| Prompt shape identifiable, rubric >=25 criteria | yes | `metadata.json.prompt_shape: "01"` identifiable; no rubric artifact is stored in the task folder to count criteria against (design note references a prior portal rubric score of 72, not a file here) | Not verifiable from this folder |
| Not LLM-generated, goldens read as real work product | yes | Judge thread's hygiene check: PASS -- two independently-coded clinical system exports with different conventions, incidental messiness (multi-spell registrations, mixed drug-name strings, cancellations), no authoring/benchmark disclosures found | Yes (per thread) |

## Gate G reconciliation
Thread's classification: `mechanism: forecasting`, `stumping_family: analytical_non_defect`,
`surface_read_dependency: no`, Gate H `domain: pass`, `layers: pass`, `decisive_step: analytical`.

Card (`task464.json`): `stump_class: analytical`, `gate_g: method_or_model_selection`, `stump_strategy:
time_semantics`, `decisive_rule_filed: false`. Design note `## Three rules`: domain test and analyst test
both describe the decisive step as "run each patient now on a statin forward to the end of their current
repeat authorisation and apply the record's share of statin repeats that ran out and were not
re-authorised, instead of a persistence curve on months since the patient started" -- classified analytical
because "the record shows nearly every stop at the request after an authorisation's last issue," and the
easy route (a persistence curve on time since starting, the field's own standard method) files Cobbet
Street at ~83, the wrong answer. This matches the thread's independent Gate H reasoning closely: the thread
also named the persistence-curve-by-population route as the easy route a strong analyst would take, filing
Fennbridge or a population-driven answer instead of Marrick House. No mismatch between the thread's and the
design's mechanism or decisive-step classification: both land on `analytical` / a forecasting-method
selection, not a surface-read flip, a decoy, data semantics, or rule application. The card's own
`decisive_rule_filed: false` is the honest admission behind the thread's finding: the author's design choice
was to leave the specific hazard construction open and argue robustness on paper (the design note's
`## Ladder`, read only after the thread returned, per protocol), not to file a convention in the shipped
package. The `## Ladder` section records the golden family tested across eleven re-authorisation-rate and
pacing variants (pooled vs. by-practice rate, full record vs. trailing 12 months, mean vs. median vs.
issue-length pacing), landing Marrick House at 168.5-171.8 in every variant (all rounding to the printed 170)
against Fennbridge's naive-route figure of 73 and Cobbet Street's golden-family figure of ~109 -- a wide,
stable margin across the parameter space the design actually tested. That internal test is reassuring but
is not itself evidence inside the shipped package the thread was scoped to judge, and it does not cover the
exact four parameters SOLUTION_STEPS names (60-day grace window, 150/28-day stop rule, mean request
interval, seven-month retention) as a labelled sweep -- it is close kin to them, not an exact match. This is
the live tension the portal's SEND_BACK already flagged once (the design note records a prior "determinism
block's fork on the forecast" return on 2026-10-28, which this pass-9 re-judge was meant to close): the
repair filed the estimand but still leaves the method's specific numbers unfiled, and the thread's
re-judge reaches the same category of finding again.

## Stump power (Gate F)
The thread calls the intended mechanism genuinely strong if it survives scrutiny: a naive analyst ranks by
raw population (or a standard persistence curve) and lands on Fennbridge or Cobbet Street, missing that
Marrick House's patients are clustered on six-issue repeats that were all re-authorised together in
Feb/Mar 2026, so they all come up for re-authorisation again just inside the window. This is a
`method_or_model_selection` / `forecasting` shape per the client's library (CLAUDE.md "stumping" 1.3), a
textbook route a strong analyst correctly takes once the clustering is noticed, and the design note's
`## Ladder` shows the golden family converges robustly. The risk the thread raises cuts the other way from
"too easy": the specific unfiled hazard parameters invite "unfairly hard" rather than "fairly hard," because
a solver who builds their own equally sound hazard model with different (equally reasonable) knobs could
land elsewhere, and the package gives them nothing to check that against.

## Findings, ranked
1. **(Gate C/E, drives SEND_BACK)** The forecast's specific numeric parameters (60-day re-authorisation
   grace window, 150-day/28-day stop-between-reviews threshold, mean request interval pacing, seven-month
   register-retention scaling) are not stated, implied, or forced by any shipped file; this is the same
   category of finding the design note records as already returned once this build cycle ("the
   determinism block's fork on the forecast"), so the repair has not yet closed it from the shipped
   package's own point of view, even though the design's internal `## Ladder` sweep argues the golden
   family is robust to the parameters it tested.
2. **(Unresolved by this pass, not a new finding)** The forward-projection chain (steps 3-5) and the R1/R2
   reconstruction (steps 6-7) were not independently recomputed within the thread's time budget; critical
   component 2 (1,232) is close to but not identical with the thread's own pull (1,243 of 1,648), attributed
   to join handling the thread did not fully trace.
3. **(Process note, does not change the verdict)** The thread disclosed that it derived Ask 1 and the raw
   repeat-authorisation counts blind, matching exactly, but opened the full submission blocks before
   finishing the critical-component-2 cross-check, so that one check was not run fully blind. The thread
   states this does not affect the Ask-1 finding or the Gate C reasoning, which rests on grepping the shipped
   files for the hazard parameters rather than on comparing figures to the target.

## Next action for the author
File, inside the package (not merely in the design note), the specific convention or a general governing
method that pins the forward-projection's free parameters -- e.g. a sentence in
`statin_continuity_sessions_brief.pdf` or a short named methodology note among the shipped files stating the
re-authorisation grace period and continuity-review gap convention the pharmacist team actually uses (a
"filed selection criterion" per the current spec), or ship the equivalent of the design note's `## Ladder`
sweep as a back-test artifact a solver could run against the data so the convergence is forced by the data
itself rather than argued on paper outside the package; either way this is the fix the two prior returns on
this build have both pointed at, so re-root the repair at the convention itself rather than at a further
numeric adjustment.
