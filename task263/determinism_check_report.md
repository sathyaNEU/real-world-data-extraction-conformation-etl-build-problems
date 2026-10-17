# determinism-check report, task263, 2026-10-16

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (one wording fix to a non-graded rationale clause is advised before ship)
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Section 6.3 of the plan defines a well's own water as the water the well itself pumps. The only route to it from the files is to unmix each entry point's blended samples by the wells in service. The data grounds the capacity-proportional mixing: ep_flow_gpm equals the summed rated capacity of the wells in service (ratio 0.95 to 1.06). The 23 over-the-line wells separate cleanly (highest other well 2.39 ng/L). The answer 16 systems, Nordvold first not reached, $451,200 left, held under every variant tried: RT-only, a window that adds 2026, equal weights, non-detects at 0, half or full RL, and lowest or highest revision.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Wells over 4.0 | 23 of 53 | 23 of 53 | yes |
| 20 grants (Torvik 1,728,000 ... Opsahl 1,209,600; Halvorsen capped 6,000,000) | as filed | same | yes |
| Systems reached / first not reached / left | 16 / Nordvold / $451,200 | same | yes |
| Pumped 2025 MG Granlund, Engvall, Hedstrom, Sandholm | 1,342.9 / 1,318.4 / 913.5 / 714.6 | same | yes |
| People Granlund, Engvall, Hedstrom, Sandholm | 30,167 / 29,442 / 21,518 / 17,614 | same | yes |
| Rationale: averaging samples a well ran in | 7 systems | 7 ($672,000 left) | yes |
| Rationale: samples a well ran alone | 11 | 20 | NO (non-graded) |

## Competing answers that survived
No fork changes the main call or an ask figure. Low-risk readings, none moves a graded figure except where noted:
- "The listed systems' wells" read literally includes Kesselring's emergency Well 3: Hedstrom 913.5 with it, 912.7 without. The golden holds on the literal reading.
- "Get their water" read in the present tense excludes the Hagestad Corners connection (closed 2025-06-30), per in_service_to and the data request note.
- Buyers' people are attributed to the buyer's own county.
- Optional prompt pins: "all wells in the inventory", "as of 1 September 2026".

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | 4 (csv, pdf, xlsx, txt) | yes |
| Large file | 25,000 rows or more | pfas_entry_point_results 36,414 rows | yes |
| Distractors | 2 or more in metadata, no file-name label | national_pfas_survey_2023.csv, private_well_pfas_2024-2026.csv; names do not label them | yes |
| Distractors unused yet weighable | yes | judge listed the survey, private wells and laboratories as present and unused by the solution; none answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | county water (MG, 1 dp) and people (whole), dollars to the dollar | yes |
| Prompt shape, rubric 25 or more criteria | yes | list of 20 plus 4 counties x 2 figures plus chart give ample items; rubric itself is generated later, not checked here | yes (not verifiable here) |
| No LLM-generated feel | yes | judge: system exports with real mess, no authoring leakage | yes |

## Gate G reconciliation
Judge: mechanism method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical; the analyst test (average a well's samples, walk to 7 systems, vs unmixing giving 16) matches the judge's easy route (7, reproduced). The declared distractors (national survey, private wells) were not named as the surface read carrying the task. Design note: Decisive step is the inversion of mixtures; the judge reached the same step. No mismatch.
Gate H: domain pass (source-water attribution by mass balance of entry-point samples), layers pass (L1 revisions, non-detects, QC samples, free-text sources, meters, wholesale chains; L2 unmixing), decisive_step analytical. Matches the note's Three rules.

## Stump power (Gate F)
Strong. Entry-point averaging gives 7, flow weighting 8; only unmixing gives 16. No file names the method.

## Findings, ranked
1. Block 1 rationale "Not 11, from the samples a well ran alone" did not reproduce: the judge got 20. The design note's R2 defines it as the average of a well's solo samples, falling back to its samples where it never ran alone; the judge's reading differs and the fallback is unstated in submission.md. Non-graded, but a reviewer recomputing it would find a mismatch. Fix the wording to state the fallback, or the figure.
2. Optional pins for Kesselring Well 3 and the Hagestad closure date (see forks). No answer change.

## Next action for the author
Correct the "Not 11" clause in submission.md block 1 (state the fallback for wells that never ran alone, or the figure the stated rule yields), without touching any graded figure, then proceed to ship.
