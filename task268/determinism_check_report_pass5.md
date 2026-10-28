# determinism-check report, task268, 2026-10-28 (pass 5, re-judge after /fix-determinism)

## Verdict
NOT_DETERMINISTIC
**Disposition:** SEND_BACK
**Stumping type:** mechanism: single_conceptual_flip, stumping_family: surface_read_rejection, surface_read_dependency: yes, sole_data_defect: no

Thread: one sonnet/medium judge, scratch `/tmp/determinism-check-task268-1793193148/target/`. It wrote
`my_reading.md` before opening the graded blocks (order kept, confirmed in its handback).

## Why
The judge reproduced every load-bearing figure in CRITICAL_COMPONENTS and the two deliverable grids exactly
(cohort 9,339 / Gullhaven 2,996; Gullhaven's 612 two-year leavers with 581 at NYHA III/IV; the 11,694/7,524
NT-proBNP dedup; the 1,555/897 2025-diagnosis/inpatient figures). It failed the main call on Gate C and
independently on Gate G: it re-ran textbook Kaplan-Meier with every leave-event as ordinary censoring and
reproduced the solution's own cited alternative exactly (Fennick 61.16%, Gullhaven 62.35%), a fully standard,
non-negligent treatment that names a different host hospital than the committed Gullhaven/58%/3-point call.
Because neither the charter nor the registry manual states or requires the hospital-by-NYHA-class
inverse-probability-of-censoring correction the golden actually uses, the judge classed the fork as
`competing_defensible_answer` (Gate C) and, independently, classed the task's core mechanic as
"compute the standard statistic, recognize it is misleading because censoring is informative, flip to a
corrected lens" — textbook `single_conceptual_flip` / surface-read-rejection, banned under Gate G at any
depth regardless of the statistical sophistication of the correction. A secondary figure did not reconcile:
the Wrenhaven aside's "347 patients" who left at the 2025 re-consent reproduced as 931 (all cohort CNR
events) or 336 (those whose two-year window overlaps the 2025-05-01 cutoff), neither exactly 347.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Cohort 2022-23 | 9,339 (Gullhaven 2,996) | 9,339 (Gullhaven 2,996) | yes |
| Gullhaven two-year leavers / NYHA III-IV at move | 612 / 581 | 612 / 581 (564 class IV + 17 class III) | yes |
| NT-proBNP Gullhaven 2025: specimens / >=400 | 11,694 / 7,524 | 11,694 / 7,524 (dedup + off-scale rule) | yes |
| 2025 new diagnoses Gullhaven / inpatient | 1,555 / 897 | 1,555 / 897 (re-dated + crosswalk-dedup rows) | yes |
| KM, every move as ordinary censoring | Fennick 61, Gullhaven 62 | Fennick 61.16%, Gullhaven 62.35% | yes |
| Committed (class-weighted) survival | Gullhaven 58, Fennick 61 | reproduced as the construction's own output; not independently re-derived from a filed rule | not forced |
| Wrenhaven "347 patients" at 2025 re-consent | 347 | 931 (all CNR) or 336 (window-overlap filter) | no |

## Competing answers that survived
- **The main-call fork.** Plain Kaplan-Meier (every leave-event as ordinary, non-informative right-censoring)
  names Fennick General Hospital lowest (61% vs Gullhaven's 62%) — reproduced exactly from the shipped
  files, using only the cohort/censoring rules the charter and manual actually state. The committed answer
  (Gullhaven, 58%) requires an additional, un-filed statistical choice: correcting for informative censoring
  via a hospital-by-NYHA-class IPCW or a class-hazard projection. Neither the charter (silent on estimator)
  nor the manual (silent on estimator) names, requires, or points to this specific correction; the manual
  states only how the cohort and the censoring events are defined, never how survival should be estimated
  once follow-up ends early. The judge judged this fork open: a rigorous analyst reading every field and
  every rule correctly and applying the single most standard tool for right-censored survival data lands on
  Fennick, not Gullhaven.
- **Naive "deaths on file"** gives Fennick 61.3% lowest, Gullhaven 66.9% — a third reading, also closed by
  the manual's note that the registry learns of no death after a patient leaves, which the judge accepted.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 (pack_contents + 12 input files) | yes |
| Formats | 3 or more | pdf, csv, xlsx, txt (4) | yes |
| Large file | 25,000 or more rows, or large DB | visits 104,323; ntprobnp 49,127; crosswalk 42,859 | yes |
| Distractors named, not in file names | 2 or more in metadata.json | `echo_lab_activity_2025.xlsx`, `hf_clinic_sessions_2026.csv`; names don't label them | yes |
| Distractor relevance | unused, relevant enough to weigh | echo EF/limited-study volumes and the 2026 clinic timetable are plausible capacity/severity signals, genuinely unused by the solution; neither was checked against a graded figure for an arithmetic coincidence in this pass | yes (not stress-tested this pass) |
| Deliverables | 1-3, all present in golden | 2 (xlsx, pptx), both named in metadata.json and submission.md | yes |
| Asks multi-dimensional, unit/rounding stated | required | survival x5 hospitals, specimen/referral counts, diagnosis/inpatient counts; prompt states whole-percent survival and point-rounded gap | yes |
| Prompt shape, rubric >= 25 | identifiable shape, 25+ criteria | hospital-ranking shape with per-hospital grids; no shipped rubric file found this pass to count directly (same gap noted in pass 4) | yes (estimated, unverified) |
| Not LLM-generated, golden realism | required | judge found no authoring leakage, no LLM tells in the files it opened; golden realism not independently re-checked this pass | yes (not independently re-checked) |

## Gate G reconciliation
The judge thread classed the mechanism as `single_conceptual_flip` / `surface_read_rejection`, `surface_read_dependency: yes`,
and raised `banned_stumping_type`, reasoning that the task's core move is "compute Kaplan-Meier (the standard tool),
get Fennick; recognize the lens is wrong because censoring is informative; switch lens; get Gullhaven" — and that
this is banned however much statistical machinery the correction carries.

The design note's card disagrees on classification but **agrees on the underlying mechanics**: `stump_class: analytical`,
with `analyst_test` stating almost verbatim what the judge found independently -- "a strong analyst ... runs
Kaplan-Meier for each hospital ... and names Fennick General Hospital at 61 per cent (Gullhaven 62) ... carried
from [NYHA] class Gullhaven Hospital's two-year survival is 58 per cent, the lowest" -- and `domain_test` naming
informative censoring by clinical state as the field's own concept. The note's `## Three rules` section states
"Not rule application: ... no rule or procedure says how survival is estimated when follow-up ends early" and
"Not semantics: every field read correctly ... still leaves Kaplan-Meier on Fennick ... an estimation choice no
field, code or definition settles" -- i.e. the design's own account concedes exactly the gap the judge is
flagging: the correction is a method choice no filed rule forces, closed (in the design's argument) only by the
data itself (the measured class-specific hazard gap) rather than by a filed selection criterion.

This is the reconciliation case this skill's contract calls out explicitly: a thread that classes the decisive
step analytical, where the golden is reached by applying one of the field's own textbook tools for exactly this
situation (inverse-probability-of-censoring correction for dependent/informative censoring is standard
clinical-epidemiology practice, not an invented procedure), can be describing a landable call rather than a true
Gate G violation -- IF the data leaves no real judgment for the solver to exercise. The design note argues the
data does settle it (class IV movers die far faster everywhere, in every hospital, so a lost patient's class at
exit is informative regardless of hospital); the judge's own evidence corroborates this (it reproduced 581/612
of Gullhaven's movers at NYHA III/IV). But the judge's independent Gate C check still found a second, fully
defensible, rule-compliant reading (plain KM) that a rigorous analyst reaches without any negligence, and the
design note's own analyst_test names the same fact under the "Not rule application" heading rather than closing
it with a filed criterion. The mismatch is real and is exactly the kind that most reliably predicts a send-back:
the judge is not confused about the mechanics (it reproduced the design's own analyst_test numbers to the
decimal), it disagrees about whether an un-filed, data-justified statistical correction can carry a main call
under the current Gate G text, which bans "single_conceptual_flip" (reject the standard tool's answer because
it is "misleading") at any depth. Net: this is a genuine construction risk the main thread must weigh against
the design note's ladder (R1 "the default path" is readable and gives Fennick; the decisive R4 rung is "silent"
and gives Gullhaven only via an estimator no filed text selects), not a reviewer error to dismiss.

## Gate H line
`domain: pass`, `layers: pass`, `decisive_step: analytical`. The judge itself ran the H3 easy-route test and
concluded analytical: "plain Kaplan-Meier is the easy, defensible route and it names Fennick... H3's own test
would classify this as analytical." It flagged the SEND_BACK as independent of H3 -- a Gate C/G failure on top
of an H3 pass, not instead of one. The design note's own Three rules section agrees on domain and layers and on
H3 being analytical, naming the same easy route (plain KM -> Fennick) and the same decisive correction
(class-at-move-carried survival -> Gullhaven). Gate H itself is not the blocker here; Gates C and G are.

## Stump power (Gate F)
The judge rates stump power as genuinely strong in substance (a careful analyst running the standard tool, KM,
gets a specific, named-wrong hospital, and the task buries real, measurable evidence -- NYHA class at exit,
the differential class-specific hazard -- that only a sharp analyst would use to catch the dependent censoring)
but disqualifies it on construction grounds: a model that reaches Fennick via a standard, defensible estimator
has not failed for an analytical reason distinguishable from "chose a different, equally licensed estimator,"
and the shape (reject the textbook tool's answer as misleading) is the banned Gate G scaffold regardless of the
statistical sophistication involved.

## Findings, ranked
1. **High.** Gate C / Gate G: the main call is not forced by a filed rule or standard; plain Kaplan-Meier (fully
   standard, charter- and manual-compliant) names Fennick, not Gullhaven. Independently, the judge classes the
   mechanic as banned `single_conceptual_flip`. Reconciliation above: the design note concedes no filed rule
   settles the estimator choice and leans on "the data separates the candidates," which the main thread must
   weigh against the current Gate G text before deciding whether this is a landable method-selection stump or
   a send-back.
2. **Medium, unreconciled.** FINAL_RECOMMENDATION's Wrenhaven aside cites "347 patients" leaving at the 2025
   re-consent; the judge could only reproduce 931 (all cohort CNR events) or 336 (those whose two-year window
   overlaps the 2025-05-01 cutoff). Needs reconciliation against `hf_registry_followup_events.csv` regardless
   of the main-call outcome.
3. **Low.** The rubric-criteria count (>=25) and golden-realism/LLM-tell checks were not independently
   re-verified this pass (same gap noted in pass 4); carried forward as housekeeping.

## Next action for the author
Resolve the Gate G reconciliation above as a design decision before any further rebuild: either (a) file the
estimator choice explicitly (a sentence in the charter or manual that names the required correction for
informative loss to follow-up, or points to a governing clinical-epidemiology convention, so Kaplan-Meier-with-
ordinary-censoring is excluded by filed text rather than by an after-the-fact argument -- this does not by
itself clear Gate G's "no surface-read-rejection, any depth" ban if the judge's classification stands), or (b)
re-root the decisive step around a FINE-numbers shape that keeps the registry/survival world but moves the
split off "which censoring treatment is right" (a binding capacity/eligibility constraint on honest survival
figures, or a forward-looking projection the closed 2022-23 cohort does not pin). Either path needs a rebuild
and a fresh judge pass; also fix the Wrenhaven "347" figure regardless of which path is taken.
