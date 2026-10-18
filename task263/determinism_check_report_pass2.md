# determinism-check report (pass 2), task263, 2026-10-18

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Note after the verdict (verdict unchanged): the thread's optional tightening was applied after it returned. Ask 6 in prompt.txt now reads "how many people living in the county get their water from any of those wells" (previously "how many people get their water from those wells"), which closes the seller-county reading the thread priced (Granlund 30,354, Engvall 29,743, Hedstrom 21,298, Sandholm 17,346). No graded figure moved: the golden still files 30,167, 29,442, 21,518 and 17,614, and the rebuild is byte-identical apart from the golden workbook's county header and notes line. Submission step 7 now also states how the four inactive buyer ids are taken to the active system of the same name and county. The judge saw the earlier prompt wording.

## Why
Section 6.3 of the IUP defines a well's own water literally, with a literal stop rule in 6.4. Solving each entry point's samples as a capacity-weighted mass balance gives 23 of 53 active wells over 4.0 ng/L (highest non-over well 2.39, lowest over well 5.04 to 7.16). The classification held under RT only, 2024 only, 2025 only, 2024-2026, non-detects at 0 or RL, first revision, and NNLS. Funding stops at Nordvold ($691,200 against $451,200 left).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Samples in scope | 302 used (305, 3 without sources) | same | yes |
| Wells over 4.0 | 23 of 53 | 23 of 53 | yes |
| 20 grants (Halvorsen capped 6,000,000) | as filed | same, to the dollar | yes |
| Funded / total / left / first not reached | 16 / $35,548,800 / $451,200 / Nordvold | same | yes |
| Water 2025, MG: Granlund, Engvall, Hedstrom, Sandholm | 1,342.9 / 1,318.4 / 913.5 / 714.6 | 1,342.89 / 1,318.38 / 913.54 / 714.60 | yes |
| People: Granlund, Engvall, Hedstrom, Sandholm | 30,167 / 29,442 / 21,518 / 17,614 | same | yes |
| Rationale: Not 7 / 8 / 11 | 7 / 8 / 11 | 7 / 8 / 11 | yes |

## Competing answers that survived
- Seller-county attribution of downstream buyers (30,354 / 29,743 / 21,298 / 17,346): closed by the prompt wording applied after the verdict.
- Renumbered buyers resolved by name only (retired ids literally give 29,988 / 29,231 / 21,221 / 17,563): judged a mistake, not an alternative, since each name has one Inactive and one Active register row; step 7 now states the rule.
- Closed Hagestad Corners connection (adds 846 to Granlund) excluded by present tense; emergency connections excluded as not Full purchase.
- Kesselring Well 3 (emergency) included in ask 5 on the plain reading ("wells pumped"); active-only gives Hedstrom 912.7.

## Spec gates
Taken from the judge's Files/Hygiene section; I did not re-audit them myself in this pass.
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | 4 (csv, pdf, xlsx, txt) | yes |
| Large file | 25,000 rows | 36,414-row results file | yes |
| Distractors | 2 or more, unused, weighable | national survey, private-well file, laboratories.csv | yes |
| Deliverables | 1 to 3 | 2 (xlsx, png) | yes |
| Not LLM-generated feel | yes | agency-export mess, no authoring language | yes |
| Rubric 25 or more criteria | yes | 20 systems plus 4 counties x 2 plus chart; rubric generated later | not verifiable here |

## Gate G reconciliation
Judge: mechanism method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Same classification as pass 1; the easy route (averaging each well's samples, 7, 8 or 11 systems) matches pass 1. No distractor was named as carrying the task. I did not re-read the design note or card this pass.
**Gate G:** PASS (analytical_non_defect; difficulty survives clean data).
**Gate H:** domain pass (mass-balance source attribution of well PFOA/PFOS, then grant sizing), layers pass (L1: revisions, non-detects, FD/FRB, free-text sources, shared meters, a meter swap, renumbered buyers; L2: unmixing entry-point samples into wells), decisive_step analytical.

## Stump power (Gate F)
Strong. The plain average gives 7 systems, flow-weighted 8, solo-sample 11, against the correct 16. The data separates the methods. No model responses were seen.

## Findings, ranked
1. No blocking finding. The pass 1 "Not 11" rationale now reproduces (11).
2. The ask 6 county wording, the one residual fork, is closed after the verdict (see note above).

## Next action for the author
Proceed to ship; no further determinism work is needed.
