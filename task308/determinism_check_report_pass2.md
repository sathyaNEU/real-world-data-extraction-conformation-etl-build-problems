# determinism-check report, task308, 2026-10-26 (pass 2, run r2)

## Verdict
DETERMINISTIC (main call), with a minor SOLUTION_WRONG on the wording of solution step 6.
**Disposition:** FIX_NOW (solution-text wording; one ask-denominator fork to close). No change to the main call, the stump or any graded figure.
**Stumping type:** mechanism: method_or_model_selection (cost at the 2027 load, a forward projection), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every graded value reproduced from the fresh unzip. The call turns on pricing each past event at the repair cost its 2027 scale implies (claims per panel firm on the fixed 2025 panel). Pennine's four pre-2021 freezes then exhaust the layer. The index-only route files Severn Vale. The thread found the lead thin (+0.087 against -0.084) but invariant to every estimation choice it tried (hinge 10 to 22, minimum occurrence size 100 to 300, window 2/6, 3/7 or 4/8 days, surge threshold 5/10/20 claims, 2027 panel one or two firms larger). Size-based surge forms (claim count, log count) flip the call to Severn Vale, but the data separates the candidates (R2 0.9987 for claims per firm against 0.964 and 0.956).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pennine value (GBP m) | 0.1 | +0.087 | yes |
| Severn Vale | -0.1 | -0.084 | yes |
| Coastal North | -0.5 | -0.488 | yes |
| Fenland | -0.8 | -0.784 | yes |
| Pennine expected recoveries | 3.75 | 3.750 (4 x 15 / 16) | yes |
| Pennine expected reinstatement premium | 0.73 | 0.732 (premium 2.93, cat_xl_quotations_2027.pdf) | yes |
| 64 occurrences of 150+ claims; Pennine freezes claims per firm | 22.6-25.1 -> 44.1-49.5 | 22.57, 23.81, 25.09, 24.16 -> 44.10, 47.85, 49.54, 46.36 | yes |
| Fit slope above hinge 16.5 | 2.8% | 2.82% | yes |
| Ask A, 12 incurred per policy figures | as filed | all 12 match to the penny | yes |
| Ask B, 4 sums insured | 68,319.8 / 79,813.6 / 118,294.5 / 75,396.7 | identical | yes |

## Competing answers that survived
1. **Ask A denominator (open).** The prompt says "per policy in force" with no date. The golden uses mid-year policies from exposure_by_district_2010_2025.csv, the only series covering 2023 to 2025. A 31 December 2025 denominator (direct_policies file) would shift the 2025 pence figures by about 1.5%. It does not touch the main call. Closing rule is not shipped in the prompt; the valuation basis speaks of mid-year proportions only for the cover-year book.
2. Index-only repricing gives Severn Vale: the intended wrong route, ruled out by the fit on the shipped claims, not by a stated rule. Not a surviving fork, but the judge notes a strict literal reader could call the surge cost response a withheld method (the design note's Not rule application line holds: the basis files the WHAT, "what repairing them would cost in the cover year").
3. Platform-only Ask A answers (e.g. Pennine 2023 = 106.95) are wrong; the Major Loss Unit supersession is derivable from the files.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 13 | yes |
| Formats | 3+ | 4 (csv, parquet, pdf, xlsx) | yes |
| Large file | 25,000+ rows | home_claims parquet 474,049; bordereaux CSV 79,090 | yes |
| Distractors in metadata.json, none labelled by file name | 2+ | group_catastrophe_programme_2026.pdf, flood_resilience_survey_2024.csv | yes |
| Distractors unused yet weighable | yes | programme and survey are not on the solution path. claims_operations_report_2025 gives platform-only counts that mislead Ask A and is ruled out by the Major Loss Unit file | yes |
| Deliverables | 1 to 3, all in golden | 2 (pdf, xlsx); both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 12 + 4 figure grid; GBP million 1dp, pounds and pence | yes |
| Prompt shape / 25+ criteria | identifiable, 25+ | shape in metadata; graded figures counted 1 + 4 + 3 + 12 + 4 = 24 before instruction-following criteria, so 25+ is plausible but the generated rubric is not in the folder to count | not verified |
| Reads as real work product, not LLM generated | yes | thread found coherent operational documents, no toolchain banners | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: Mechanism gap objective then time, decisive generator G14 (cost of a claim conditioned on its event's claims per panel firm, carried to 2027 scale), stump_class analytical. Match. The declared distractors (group programme, flood survey) were not named as the surface read carrying the task. Gate G: no shipped artifact ranks the regions on the decision question; PASS.
Gate H line: domain: pass, layers: pass, decisive_step: analytical. Matches the card's domain_test (post-event demand surge in cat pricing) and analyst_test (index-only route files Severn Vale -0.1, golden files Pennine +0.1) and the note's Three rules. No mismatch.

## Stump power (Gate F)
Strong on paper. A strong analyst who cleaned the data and read every rule still files Severn Vale unless they build claims per firm and estimate the cost response. The thread reached the golden by doing exactly that estimation, which is a judgment the data had to settle (fit selection and extrapolation), not a stated procedure. The asks add independent traps (Major Loss Unit supersession and re-dated cases, Lowther and Pike cancel/reinstate/rewrite handling). The thin Pennine margin (0.17 gap) is robust but rounds: -0.084 shows as -0.1, so the "GBP 0.2 million more" claim holds on rounded figures only.

## Findings, ranked
1. Ask A per-policy denominator is not pinned in the prompt (mid-year against year-end, about 1.5% on the 2025 figures). Pin it by a sentence in the prompt or by a filed rule, then rerun the affected check.
2. Solution step 6 misdescribes the Major Loss Unit additions. The golden also includes MLU-26-0043 (2025-05-08) and MLU-26-0044 (2024-07-09, Severn Vale 2024), which carry no 2026 date and have no platform record. Reword to "unit claims with no platform record, in the year of the unit's date of loss". Figures are right.
3. Rubric count of 25+ is unverified from the folder.

## Next action for the author
Reword submission.md step 6 as in finding 2 and close the Ask A denominator fork (finding 1) through `/fix-determinism`, holding the main call, the stump and all graded figures frozen.
