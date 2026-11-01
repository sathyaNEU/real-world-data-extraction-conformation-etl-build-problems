# determinism-check report, task453, 2026-11-01 (pass 3, reship after the leak-gate repair)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (decomposition of the apparent jump into interview mix versus questionnaire), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread: one pass, sonnet, medium, isolated scratch `/tmp/determinism-check-task453-run1793552026/target/` (md5 of target.zip f0225faebee7b06320587fc6bae6a6fa); its `verdict.md` is in the same folder. Bundle is the reshipped 11-file cut (no file dictionary, no export manifest).

## Why
Every graded figure reproduces from the shipped files alone. The Act (s8, s9(2)) files the WHAT (trigger plus the national published-rate change in full use against what the old questionnaire would have published for the same months, one decimal); the methodology note files the rotation structure; the data separate the candidate estimators. Well-specified estimators all give 0.48 to 0.52, which rounds to +0.5, so the trigger is 6.5. The 2026 averages split the regions cleanly (North Coast 6.44, 0.06 short). The dropped dictionary opened no second figure for any graded value (labels are in-file).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Conformed panel vs release (Tables 1 to 3) | each month reproduces | 0 rate mismatches in 60 months, 0 in 540 region-months, Table 3 0 diff | yes |
| First-interview excess | 1.3 | 1.30 (cai2014 cells, month x region FE) | yes (derived, not stated in text) |
| Change in published rate | +0.4848 / +0.5 | +0.4848; estimators 0.483 to 0.522 | yes |
| Arm gap Jul-Nov 2025 (rejected) | 1.2, trigger 7.2 | about 1.2 (0.99 to 1.37) | yes |
| Fixed-interview effect (rejected) | 6.3 or 6.4 | 0.31, worse fit (RSS 2.16M vs 1.83M) | yes |
| Restated trigger | 6.5 | 6.0 + 0.5 | yes |
| 2026 averages | ER 6.58, WC 6.64, RD 7.44, HL 8.32, NC 6.44 | 6.583, 6.642, 7.442, 8.317, 6.442 | yes |
| Dwellings, all regions | 88,040 | 88,040, nine regions match | yes |
| CSV | 324 rows | 324 = 9 x 36, rule per note s4 | yes |

## Competing answers that survived
None on the main call or the asks. Observations:
- Trigger 7.2 (arm gap) and 6.3/6.4 (shared interview profile) are the easy-route wrong answers; the data reject them (fit, year stability) and the Act's same-months wording excludes them.
- Dwelling identity (distinct `dwelling_ref` gives 73,051 against 88,040) is a data-semantics step on an ask only, allowed by rule 3; determinate from interview_no jumping 6 to 1 on the same ref and the note's replacement wording.
- "Responded", see the dedicated answer below: closed by the pack.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 11 | yes |
| Formats | 3+ | 4 (csv, parquet, pdf, xlsx) | yes |
| Large file | 25,000+ rows | 254,964 (parquet), 72,090 (cai2014 csv; counted by me) | yes |
| Distractors | 2+ named, none labelled by file name | 3 in metadata.json (population benchmarks, projected seasonal factors, response-rate workbook); names are neutral | yes |
| Distractors unused, weighty | yes | benchmarks and projected factors carry no graded quantity; the response workbook does not answer a graded quantity (it is a rate, not a count) | yes, with the note below |
| Deliverables | 1 to 3, all in golden | 2 (pdf, csv), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | trigger, change, CSV to one decimal; counts in dwellings by region | yes |
| Prompt shape, 25+ criteria | 25+ | design note counts 30 before selection (not verifiable from the bundle) | yes, on the note |
| Reads as real, not LLM generated | yes | judge found statistics-office artifacts, no generation disclosure; golden PDF/CSV not in target/, checked only by derivation | yes |

Note: the response-rate workbook is a declared distractor yet is the file that closes the "responding" definition (see below). It does not carry or rival a graded number, so it stays within the distractor rule, but the design note's "the solution never reads" claim is loose; the solver need not read it, the literal reader may.

## The coordinator's question: "responded" as outcome 11 only against 11 and 12
Not a second open figure; the pack closes it, three ways:
1. Plain-language labels in the fieldwork file: `outcome_desc` has 11 "Full response" and 12 "Partial response". Both are responses to the survey, so "responded" reads 11 and 12 on the shipped text.
2. The response-rate workbook (`lfs_response_rates_2025-2026.xlsx`) gives responding dwellings as a percentage of eligible ones (31, 32, 33 excluded per its footnote). I recomputed it on the parquet: 11 plus 12 gives 74.5, 74.1 and 71.5 for Oct, Nov, Dec 2026, equal to the workbook's All regions column; 11 only gives 70.0, 69.6 and 67.2, which do not match. The regional columns match too (judge: Capital Dec 65.2).
3. The only count of 11 alone (85,953) rests on treating a partial response as non-response, which no shipped text supports.
Residual risk is low: the closure comes from a labelled field plus a cross-check in a distractor file, not from a sentence in the Act or note. It also lies in an ask, where rule 3 permits semantics. No repair needed; an optional hardening is none, since adding a definition would be filing HOW.

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Gate H: domain pass, layers pass, decisive_step analytical.
Design note (read after the verdict): Three rules lines match: the decisive step is the comparison within interview number averaged over six interviews, the arm gap files 7.2, one effect with interview number fixed files 6.3/6.4, nothing planted. The thread did not name any declared distractor as the surface read carrying the task. Pass 1's note agrees (same mechanism, same easy routes). No mismatch. I did not locate a card file for `stump_class`, `analyst_test` or `domain_test` by name, so I reconciled against the design note's Three rules only.

## Stump power (Gate F)
Good on paper. Two well-evidenced wrong routes (7.2 with two regions, 6.3 with six regions) are attractive to a strong solver; only one that spots the rotation and interview-number structure, builds the panel by rotation group and estimates by-interview effects reaches 0.5. The decisive step is not a textbook route that a strong solver lands without data-settled judgment: the Act names no method and the data must separate the candidates. Risk that both top responses land the call exists (the note describes the rotation in prose), but the build plus the six-effect model and the four-region cut is heavy. Weighed against the design note's ladder by the main thread.

## Findings, ranked
1. None blocking.
2. Low: step 2 of the solution says the 1.3 first-interview excess without saying it is estimated from the CAI 2014 cells (the note does not state it). No graded figure depends on citing it.
3. Low: dwelling identity (refs reused after replacement) is allowed ask-level semantics.
4. Low: the "responded" definition closes through `outcome_desc` and the distractor workbook (above).

## Next action for the author
None required to ship; optionally reword solution step 2 to say the 1.3 is estimated from the CAI 2014 cells, then carry on with the pre-ship check.
