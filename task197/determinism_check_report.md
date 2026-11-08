# determinism-check report, task197 (architecture 2, run a2), 2026-11-02

## Verdict
NOT_DETERMINISTIC, on referral_tables.xlsx ask 2 only (the antidote course counts). The main recommendation is DETERMINISTIC and reproduced.
**Disposition:** SEND_BACK. The send-back touches the supplementary asks only, not the decisive step. Fix location: input_files and prompt, ask 2 only.
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The 12 hospital by half-year course counts (acetylcysteine, deferoxamine for an iron poisoning, the sum; 36 figures) do not follow from the shipped text. The prompt says only "courses started". The regimens, the dose ratios and hours, the iron-poisoning chain rule and the transfusion-admission exclusion appear in no shipped file, including both procedure PDFs. They exist only in submission.md step 7. The judge's literal reconstruction missed the golden in roughly 20 of 36 cells (off by 0 to 4). Riverbend (H34) prepares its sets in a batch, so a literal "at the regimen's hours" rule gives it zero acetylcysteine courses, against a golden of 59/77/57. Gates B and C fail for ask 2. Label: underspecified_objective, with an external_dependency component.
The main call is forced. Feverkind 1.3, Embercalm 1.1, gap 0.2, and the other six at 1.0 all reproduce.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Feverkind exposures, Oct 2024 to Sep 2025 (case export: reason, age under 6, product_code, local month) | 5,475 | 5,475 | yes |
| Embercalm exposures, May 2025 to Apr 2026 | 13,038 | 13,038 | yes |
| Feverkind effect | 1.3 | 1.302 | yes |
| Embercalm effect | 1.1 | 1.094 | yes |
| Dozinox, Vapocare, Coughex, Ibucalm, Sunnybear, Clearview | 1.0 each | 1.011, 1.000, 1.001, 0.990, 0.989, 0.977 | yes |
| Gap | 0.2 | 0.208, and 0.2 from the rounded effects | yes |
| Eight changes and Feverkind first sale 16 Sep 2024 (register, Packaging changes sheet) | as claimed | as claimed | yes |
| Acetylcysteine and deferoxamine, 12 cells x 3 columns (36 figures) | as in submission.md | about 20 cells differ; Riverbend not reproducible from the text | no |

Robustness of the main call: the effects hold across the fit start (2019 or 2021) and the fit end. Feverkind stays within 1.297 to 1.303 and Embercalm within 1.092 to 1.095.

## Competing answers that survived
Ask 2 (the antidote courses) has open forks, none closed by a shipped sentence:
- Whether a lone or repeat bag starts a course.
- Whether a 0 to 4 h pair of deferoxamine bags is a course.
- Chain length and spacing for an iron-poisoning course.
- How a transfusion admission is told apart.
- The Riverbend batch-preparation convention.
- The regimen ratios and hours themselves.

Main call, counterfactual baseline. This is the residual the thread flagged. Procedure 3.1 reads "the number the product's packs would have produced", and it never says "packs in use". The readings give:

| Reading | Feverkind | Embercalm | Dozinox | Call |
|---|---|---|---|---|
| Packs in use (golden) | 1.30 | 1.09 | 1.01 | Feverkind |
| Exposures per pack sold | 1.19 | 0.92 | 1.64 | Dozinox |
| Raw count against prior year | 1.37 | 2.75 | 0.86 | Embercalm |

The thread's own held-out back-test removes the competing readings on the data. The stock model's deviance is 6 to 20 per 12 months on all eight products, against 130 to 1,580 for per-pack-sold. Feverkind's decay is tightly pinned. The thread treats this as a method choice the data forces, which is allowed, and records the residual as a risk and not a failure. The residual stands: a literal reader who takes "packs" as packs sold lands on Dozinox. The method is open only through the data's separation of the candidates, and no filed selection criterion names the back-test. I record it as an open risk and not a failure. The thread's optional line for procedure 3.1 (that packs "in use" are meant) is filing the WHAT, but it would sit close to naming the stump. The main session should weigh that against CLAUDE.md's rule to file WHAT and never HOW.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 11 | yes |
| Formats | 3 or more | csv, pdf, xlsx | yes |
| Large file | 25,000 rows or more | case_export_watched_products.csv, 470,106 rows | yes |
| Distractors | 2 or more in metadata.json, none named by file name | census/population_age_0_5_by_state.csv and packaging_review/adverse_event_reports_watched_products.csv; neither file name labels it | yes |
| Distractor relevance | unused by the solution, relevant enough to weigh, ruled out by a shipped fact | the thread found both unused; I did not recompute whether either reproduces a graded quantity | partial, not recomputed |
| Deliverables | 1 to 3, all in the golden, no format family required | 3 (docx, xlsx, png); the golden folder holds all three | yes |
| Asks | multi-dimensional, unit and rounding stated | 8 effects, plus 12 hospital/half-year cells x 3 columns; "ratios to one decimal and courses are whole numbers" is in the prompt | yes on form, ask 2 fails determinism |
| Prompt shape and rubric | shape identifiable; 25 or more criteria | prompt is one paragraph, question first, under 1,000 characters, with no data-held count; the 25-criteria rubric is generated downstream and not checkable here (8 effects + 36 cells + referral items is ample) | yes, rubric not verified |
| Reads as real, not LLM generated | clean | the thread found the antidote file clean and plausible, and the layer-1 mess realistic; I did not independently judge golden realism | yes, per thread |

## Gate G reconciliation
The thread reports `method_or_model_selection`, `analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The design note and card agree. The card says `stump_class: analytical`. The note's stump sentence is the packs-in-use baseline fitted per product and validated on its held-out year, against the per-pack-sold default that refers Dozinox. The thread did not name the declared distractors (population and adverse-event reports) as the surface read, so they are not too load-bearing. No mismatch. The reported counts and sales are honest, and the difficulty is the exposure base.

## Gate H reconciliation
Thread: `domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1 is the case-system change on 10 Jul 2023, preliminary against revised POS, 4-week periods against calendar months, and UPC mapping. Layer 2 is the pack-stock counterfactual baseline validated by back-test. Design note and card match (`estimation_fit`, analyst test and domain test both present). The thread classed the decisive step analytical by the easy-route test, and not merely because the packs-in-use method is a field standard: the per-pack-sold route files Dozinox at 1.64, or no referral at all. The thread did not reach the golden by applying a textbook method with no judgment. It found the method by comparing candidate models on held-out years. The residual is that the method is not filed (procedure 3.1 never says "packs in use"), so the stump is analytical only because the back-test separates the candidates, and the thread's own back-test confirms that it does. No Gate H failure.

## Stump power (Gate F)
Good. The per-pack-sold route is the field's conventional base and gives a specific wrong call, Dozinox at 1.64, with Feverkind at 1.19 below the 1.20 line. A strong model that does not model the stock of packs in homes and validate it out of sample falls into it. The stock model is a recognised organ in the field, so a strong solver could land it by modelling the home stock without the back-test. That is for the main thread to weigh against the ladder in the design note. Ask 2 adds determinism risk, not stump power.

## Findings, ranked
1. Ask 2, referral_tables.xlsx, 36 figures: the regimen, chain, lone-bag and transfusion-exclusion definitions are filed nowhere in the shipped files. The golden is not reproducible from the text, and Riverbend is zero under a literal reading. SEND_BACK. Note CLAUDE.md allows asks to turn on semantics or rule application, but they still must be determinate from shipped text.
2. Main call residual: procedure 3.1 does not say "packs in use". This is a risk the held-out back-test closes on the data. No finding on the main call's determinism.
3. The distractor spec check is incomplete: I did not recompute whether either distractor reproduces a graded quantity arithmetically.

## Next action for the author
Re-derive ask 2 from filed definitions. File in the shipped text or pack what makes a course (the regimen ratios and hours, how a hospital's preparation time relates to administration, whether a lone or repeat bag starts a course, and the chain length and spacing that make an iron-poisoning course and tell a transfusion admission apart), then recompute all 36 figures from those definitions. Or drop the antidote asks. Keep the main call, the packaging data and the eight effects frozen, since they reproduce.
