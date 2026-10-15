# determinism-check report, task446, 2026-10-15

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (one metadata correction below, not a determinism finding)
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The judge thread (one pass, sonnet, medium, isolated to a fresh unzip of target.zip) recomputed every load-bearing figure from the bundle. The 133 is forced by the book (913), flags (165), pooled capture (78.1%) and false-alarm (7.83%) rates under CRM-07 2.2, 3.2, 4.1 to 4.3, with the 18.1% flagged share solved through those rates (133.04). With CRM-07 5.2 now filing the estimand only, the method is left open and the closed cohorts separate the candidates: capture/false-alarm validates within 1.6% leave-one-cohort-out, hit/miss rates miss by 40.6%, the trended basis by 8.0%. Band table, totals and SVG figures reproduce. Prompt is prompt.txt.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Book at 30 Sep 2026 | 913 | 913 (register + watch list) | yes |
| Flagged groups | 165 | 165 (EWS 2026-09-30, GLEIF chain, CRN keys) | yes |
| Pooled capture / false alarm | 78.1% / 7.83% | 157/201, 259/3307 | yes |
| Implied arrival share | 14.6% | 14.57% | yes |
| P(arrive) flagged / not | 63.0% / 3.9% | 62.98% / 3.89% | yes |
| Caseload | 133 | 133.04 | yes |
| Worst LOO miss, capture/FA vs hit/miss | 1.6% / 40.6% | 1.6% / 40.6% | yes |
| Five bands, groups and committed £m, total 913 / 25,500.5 | as submission | identical | yes |
| Band arrivals flagged / not, total 103.9 / 29.1 | as submission | identical | yes |
| Exposure arriving, total £3,994.6m | as submission | identical | yes |

## Competing answers that survived
None on the main call. Hit/miss pooled 73, trend 147, proportional-to-flags 80, unconditional share 52 are each rejected by the out-of-sample record. Single-cohort or last-3/last-2 capture/false-alarm give 127 to 139 (132, 129); CRM-07 4.3 reports on the four closed cohorts taken together, which pins the window. Residual risk only: the method is not filed, so a solver ignoring 4.3's window could land 127 to 139. The rating PD distractor sums to 7.6 and the macro paths link to nothing.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 17 | yes |
| Formats | 3+ | 6 (csv, xlsx, docx, pdf, md, txt) | yes |
| Large file | 25,000+ rows | EWS 125,317 | yes |
| Distractors in metadata, none named in a file | 2+ | internal_rating_master_scale_2026.xlsx, group_economics_uk_outlook_oct2026.xlsx | yes |
| Distractor unused yet weighable, none answers a graded quantity | yes | PD sum 7.6, no macro link; ruled out by shipped facts | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 5 bands x 6 columns plus total and chart; unit and rounding in the prompt | yes |
| Prompt shape, 25+ criteria | yes | shape 05; design note plans about 50 | yes |
| Not LLM-flavoured, goldens business-real | yes | judge found none; no em dashes in prompt or submission | yes |

## Gate G reconciliation
Thread: mechanism forecasting, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note Gate G and card: the same four values (card stump_strategy composition_mix, stump_class analytical). Match. The declared distractors are not the surface read carrying the task (the thread names the 73 hit-rate build as the trap, which is a method choice, not a distractor).
Gate H: thread domain pass, layers pass, decisive_step analytical. Design note `## Three rules` and card analyst_test/domain_test agree: easy route (hit rate onto 165 flags) files 73, correct basis 133; Layer 1 (GLEIF, UK-time cutoff, limit versions, FX) does not move the headcount. Match. No decoy, not semantics, not rule application stand against the shipped text.

## Stump power (Gate F)
Plausible but not certain: the 73 default is the natural route, and a solver who back-tests or sees the flagged share jump from 11 to 14% to 18.1% finds the prevalence dependence. 133 is reachable by a standard prior-shift adjustment that a capable model may know. The band table adds Layer 1 work that is graded but does not move the headcount.

## Findings, ranked
1. metadata.json `objective` reads "Data Extraction & Conformation (ETL)" while the card, pipeline.json and submission tags say Forecasting & Predictive Modeling (the repair moved the pairing). Stale metadata; correct it to match. Not a determinism issue.
2. Residual method spread (127 to 139) for single-cohort or shorter-window capture/false-alarm variants; closed by CRM-07 4.3's window and the back-test, so no repair.
3. Optional wording: the submission says the trended basis misses "far more" out of sample; it is 8.0% against 1.6%, and the decisive argument is the extrapolation beyond the cohorts' flagged-share range.
4. Note: the extract log says the facility extract ran after the 1 October start-of-day batch, which signals the limit-timing issue; consistent with the fiction, not stump-affecting.

## Next action for the author
Set metadata.json `objective` to Forecasting & Predictive Modeling, then ship; no determinism repair and no re-judge needed.
