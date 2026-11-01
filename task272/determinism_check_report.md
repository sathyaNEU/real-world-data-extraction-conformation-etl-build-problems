# determinism-check report, task272 (architecture 3), 2026-11-01

target.zip sha256 811762642f4a39e7d2662cd99382434112b751153dba38a13e82bfc484bde5c5. Judge thread: one pass, scratch /tmp/determinism-check-task272-010406/, verdict at /tmp/determinism-check-task272-010406/verdict.md. The brief carried the submission after the rival-clause fix. Critical Components 2 and 3 were edited after the thread's read: CC2 no longer lists the modelled rate to one decimal, and CC3 grades the four products as over 10 and every other as under 3. The pack is unchanged and the thread's classification confirms CC3.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (with statistical_rigor, etl_conformance), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
**Gate H line:** domain: pass, layers: pass, decisive_step: analytical

## Why
PH-QP-07 2 and 3.1 file the estimand: the 2026 out-of-tolerance rate per 100,000 doses made, "whether or not weighed", configured when it is over 10. The weighed sample (about 2%, taken early in each set) therefore has to be modelled, and the data separate the candidates. Weighed deviation falls linearly with litres pumped since SET_UP on PC-1 to PC-3 (p < 1e-4 for every product) and is flat on PC-4. Under that model the call is Cefazolin 2 g 20 mL, Cefoxitin, Phenylephrine and Midazolam. Every other product is at or below 0.2, so the gaps to 10 are wide. No gate A to E failure was found.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Monthly doses, PC-1 to PC-4 and GC-1 (60 values) | golden CSV | all 60 match, UTC to America/Toronto | yes |
| Sets per product (12) | 441, 148, 354, 420, 169, 130, 271, 272, 172, 114, 167, 166 | identical | yes |
| Completed vs aborted | only completed are "made" | 476,230 completed, 1,645 aborted | yes |
| Dose to SET_UP assignment | every dose on a set | 0 unmatched | yes |
| Weighed rows to doses | by batch and dose number | 8,179 matched, 0 unmatched, 0 duplicates | yes |
| Rate, Cefoxitin | 451.2 | 453.8 (OLS variant 457.9) | classification yes |
| Rate, Phenylephrine | 266.6 | 266.7 (OLS 263.6) | yes |
| Rate, Cefazolin 2 g | 131.4 | 138.8 (OLS 146.7) | classification yes; method difference of about 7, far above 10 |
| Rate, Midazolam | 43.7 | 43.7 | yes |
| Rate, Ampicillin | 0.2 | 0.2 | yes |
| Other 7 products | under 0.1 | 0.0 | yes |
| Slopes | PC-1 to PC-3 drift, PC-4 flat | p < 1e-4 on PC-1 to PC-3; Heparin p = 0.85 and Midazolam p = 0.45 (no slope) | yes |

The 4-in, 8-out classification is identical under every drift-aware variant tried. The CC2 decimal spread between the golden and the judge's rates (largest on Cefazolin 2 g) is why CC2 no longer grades the modelled rate to one decimal.

## Competing answers that survived
None on the main call.
- Pooled normal fit on weighed doses (the easy route) gives Cefoxitin 35, Ampicillin 183, Pip-taz 110, Vancomycin 309, Midazolam 42, Cefazolin 2 g 0.4 and Phenylephrine 3.1. It adds Ampicillin, Pip-taz and Vancomycin and drops Cefazolin 2 g and Phenylephrine. It is separated by the data: weighed doses sit early in each set, and the litres-pumped slope is significant.
- Register FAILs plus quarantine rejects (7 weighed FAILs, all Cefoxitin) is not a rate per doses made, so it is not a defensible estimand under PH-QP-07 2.

## Residual risks (not failures)
1. Midazolam (43.7) rests on a normal-tail extrapolation. 0 of 334 weighed doses fall outside tolerance, and 0.15 are expected, so that is consistent. Standard errors on mean and sd move the rate between roughly 20 and 90, still over 10. PH-QP-07 3.1 tests the rate, not significance, so "insufficient evidence" is not licensed. The ask never says "estimate"; the policy definition plus the sample design force a model.
2. The dose log's UTC clock is not labelled in the file (the events carry Z). It is derivable: SOP-12 hours of 07:00 to 23:00 and Saturday close fit only after UTC to Toronto conversion, and the GC-1 weights give local anchors. A local-time misreading moves only boundary counts, but those are graded exact whole numbers. The thread's optional fix is a one-line local/UTC note in the dose log export, which needs no rerun of the call.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 5 (csv x6, xlsx x3, pdf x2, parquet, eml) | yes |
| Large file | 25,000 rows or more | dose log 477,875 rows | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | 3 named: gc1_dose_weights, ward_issues, cleanroom_monitoring; none labelled by file name | yes |
| Distractor quality | unused, relevant, ruled out by a shipped fact | GC-1 covers products PH-QP-07 3.2 keeps out of scope; the judge found all unused by the answer; quarantine_register is evidence per metadata (the thread listed it among distractors, a labelling difference only) | yes |
| Deliverables | 1 to 3, all in golden | 2 (PDF, CSV), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 60 monthly cells plus 12 set counts plus 12 in/out marks; "whole numbers" stated; the month basis is Ontario local per the golden, not stated in the prompt (see risk 2) | yes, with the UTC caveat |
| Prompt shape and rubric 25 or more | identifiable shape, 25 or more criteria | 84+ separately gradable figures (60 + 12 + 12 + the call); the rubric is generated, not seen here | yes on grading surface |
| Reads as real work | no LLM tells | the thread found operational artifacts with real irregularities (gross/net switch, recount rows); no provenance leakage | yes |

## Gate G reconciliation
Read from DESIGN_NOTE.md and the card after the thread returned. Verdict: match.
- Design note stump sentence: the default path is a capability study on weighed doses reading the weights as one stationary spread, configuring P0431, P0610, P0614, P0618 and P0702. The golden is P0412, P0431, P0507 and P0702 once the sets are rebuilt with litres pumped. Mapped to product names, the default path is Cefoxitin, Ampicillin, Pip-taz, Vancomycin and Midazolam, which is the thread's pooled-normal competing answer exactly. The golden is its four.
- Card: `stump_class: analytical`, with `analyst_test` and `domain_test` present. The thread's `analytical_non_defect`, Gate H `decisive_step: analytical`, `domain: pass` and `layers: pass` agree with them, as does the note's `## Three rules` (No decoy, Not semantics, Not rule application).
- `surface_read_dependency: no` and `sole_data_defect: no`. No declared distractor carries the surface read. The easy route is built from the evidence files, not from any distractor.
- Layer 1 mess (UTC against local months, two PC-3 serials, gross/net switch, recount rows, re-seats) does not carry the stump.

## Stump power (Gate F)
Good on paper. A strong analyst who runs the textbook pooled fit or trusts the register's PASS/FAIL adds Ampicillin, Pip-taz and Vancomycin and misses Cefazolin 2 g and Phenylephrine. Nothing in the pack states the litres-pumped drift, so the solver has to rebuild set history from the events, the UTC log and the programmed volumes. The 24-hour set-reuse limit, the re-seat convention and early-in-set sampling raise the difficulty, and Midazolam is a second easy-route miss (flat but still over 10).
For the main thread to weigh: the drift-aware mixed or OLS model is the field's standard process-capability approach. The thread classes the decisive step analytical because the data separate pooled from drift, not because the method is standard. A solver who checks weighted deviation against litres pumped lands the call, so the ladder should be weighed on that route.

## Findings, ranked
1. None blocking.
2. Dose log UTC clock unlabelled; boundary counts in 60 graded cells depend on it (derivable; optional one-line in-fiction note).
3. Midazolam rate rests on a tail extrapolation, still over 10 across the plausible range.
4. Minor: CC2 and CC3 were edited after the read. They moved nothing the thread verified.

## Next action for the author
Optional: add a local/UTC line to the dose log export. If you do, the pack changes, so rebuild and rerun the gates. Otherwise, no repair; continue the stage 4 ship checks.
