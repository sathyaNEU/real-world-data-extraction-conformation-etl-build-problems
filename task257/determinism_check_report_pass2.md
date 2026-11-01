# determinism-check report, task257, 2026-11-01 (pass 2)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (etl_conformance on the asks), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread: one pass, general-purpose, sonnet, medium, spawned by the main session from judge_brief.md; verdict at /tmp/determinism-check-task257-r1/verdict.md. Bundle sha256 prefix 132068cecc1c0a8b. prompt.txt is current (not legacy prompt.md).

## Why
Three sub-scales is forced by the shipped data: polychoric/tetrachoric eigenvalues 9.75, 6.01, 2.21 above the random-data 95th percentile, fourth 0.78 against 1.07; Kaiser and Velicer MAP agree. Item placement 11/11/8 is clean (own-factor loadings 0.48 to 0.90, other loadings at most 0.06) across extraction and rotation choices. Respondent set and the department table reproduce exactly from the bundle.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Respondents | 13,717 | 13,717 | yes |
| Polychoric eigenvalues | 9.75, 6.01, 2.21, 0.78 | same (5th 0.76) | yes |
| PA 95th pct, 4th | 1.07 | 1.066 | yes |
| Pearson 4th, 5th | 1.49, 1.34 | 1.49, 1.34 | yes |
| Tools / growth yes rates | 93.7-95.0 / 4.5-6.7 | same | yes |
| Placement | 11/11/8 | identical, 30 items | yes |
| Store respondents | 12,245 | 12,245 | yes |
| Department table (8 rows) | as filed | exact match | yes |

## Competing answers that survived
None on the main call. Five (Pearson) and six (wording areas) are rejected by the data; four fails every criterion. Respondent-definition forks (UTC close 13,494; paper by keyed date 13,147; October department) do not survive the standard's text. Residual risk, advisory only: the department labels rest on the HRIS header sentence ("descriptions as of run date") and the 1 Oct code-pair swap; a reader taking the September row's department column literally gets every label wrong (Grocery 3,262/137/63.4 and so on). The store counts are knife-edge (55 groups at exactly 10, 71 at 9), deterministic only because the standard fixes each term. Sub-scale names are not pinned; the grouping is the graded content.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 11 | yes |
| Formats | 3+ | 4 (pdf, csv, xlsx, jsonl) | yes |
| Large file | 25,000+ rows | responses 417,225 lines; HRIS 43,050 | yes |
| Distractors | 2+ in metadata.json, no file name labels one | pulse_survey_2026_q2_site_results.csv, kestrava_retail_benchmark_2026.xlsx; names neutral | yes |
| Distractor relevance | unused, weighable, ruled out by a shipped fact | judge: unused by solution; benchmark priors are real-looking, not the answer | yes (judge basis; not independently recomputed) |
| Deliverables | 1-3, all in golden | 3 (xlsx, png, md), all present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 30-item grouping plus 8-department table, whole numbers and one decimal stated in prompt | yes |
| Prompt shape / 25+ criteria | identifiable | one paragraph, question first; rubric not generated here, rows (30 items, 8 departments x 3 figures, scree, count) support 25+ | yes (inferred) |
| Reads as real | no LLM tells | judge found none; run stamps, cover sheet, test tokens | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: default path is Pearson correlations keeping five; stump is the correlation basis (latent correlations), nothing planted, no decoy, no certified replay, "Not semantics" and "Not rule application" lines present. Matches. Neither declared distractor is named as the surface read; no shipped artifact ranks candidates wrongly. Gate G: clean, no finding. (I did not locate the card file to compare stump_class directly; the note's Three rules and analyst test are consistent with analytical.)

## Gate H
domain: pass, layers: pass, decisive_step: analytical. Layer 1 is the ETL mess (French codes, time zones, repeated links, kiosk, paper, 1 Oct code swap); Layer 2 is correlation basis and retention testing. Reconciles with the design note's domain test and analyst test.

## Stump power (Gate F)
A strong analyst defaulting to Pearson files five confidently (Kaiser, PA and MAP all give five on Pearson). Methods like polychoric are textbook for binary and ordinal items and the prompt does not hint, so moderate landing probability by a solver who knows them. The call is invariant to the cleaning choices, so ETL does not carry the stump; the ask layer is hard because counts flip on exact definitions. Main thread weighs against the ladder in the design note.

## Findings, ranked
1. Advisory: department label reading rests on the header sentence and code-pair swap (low residual risk, no change required).
2. Advisory: sub-scale names free; grade on grouping.
3. Cross-batch duplicate check not possible in isolation (guard.py is the free gate).

## Next action for the author
Proceed to ship; optionally note in submission.md that sub-scale names are free and grading is on the item grouping.
