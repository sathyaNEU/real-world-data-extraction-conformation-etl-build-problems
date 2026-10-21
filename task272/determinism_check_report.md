# determinism-check report, task272, 2026-10-21

## Verdict
DETERMINISTIC (main call and every graded figure recompute from the bundle).
**Disposition:** FIX_NOW (asks 3 and 4 only, optional documentation in the data guide; the main call and data stay frozen)
**Stumping type:** mechanism: method_or_model_selection (statistical_rigor), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Scope note: the judge thread was one isolated sonnet/medium pass (brief and unzip at /tmp/determinism-check-task272-030546/, verdict at .../verdict.md). Per the coordinator this report is evidence for the record, not a repair driver.

## Why
Conforming the three hubs (Columbia UTC to Pacific, H23 crosswalk, presumptive screening, pends and withdrawals dropped) gives 197,939 determinations. With each counsellor-day measured against its own determinations in any order, 11 hospitals clear 6.0 points (H03 H06 H09 H10 H17 H19 H20 H21 H22 H26 H31; values 8.97 to 10.89) and the other 20 sit at or below 3.1. The margin is clean (weakest qualifier about 6 points above the strongest non-qualifier). 11 x 64,000 = 704,000.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Determinations (3 hubs, 93 counsellor IDs after H23 map) | 197,939 | 197,939 | yes |
| Qualifying hospitals, excess over every-order expectation | 11, listed | same 11 | yes |
| Variants: realised-pair denominators; Mantel-Haenszel with Monte-Carlo expectation; Columbia left in UTC | 11 | same 11 each | yes |
| Budget line | 704,000 | 11 x 64,000 | yes |
| Ask 3 assistance, 31 values and total | 402,933.0 thousand | all 31 to 0.1 and total (FAWO once per application, FAWR on every line, 6,207 duplicate Willamette December lines dropped) | yes |
| Ask 4 denials for documents not received | 22,683 | all 31 and total (code 2 before 1 July, code 1 from 1 July) | yes |
| Workbook and PNG | not in the thread's universe | not checked | n/a |

## Competing answers that survived
1. 23 grants (1,472,000 dollars): the within-day contrast without the every-order expectation (day fixed effects or stratified contrast, H04 sits at 6.00). The only live fork on the main call. Criteria 2.4 files "the chance of approving ... of the kind the working day brings" and never names the correction, so a literal reader who treats the observed within-day share as the chance gets 23. The thread judges this the stump itself (small-sample bias of conditioning on the previous outcome), every bias-correcting estimator returning 11, but notes a challenger could call the text silent.
2. 2 grants from the pooled contrast: ruled out in words by criteria 2.4.
3. Ask 4: a literal guide-reader using code 1 only gets different counts. Ask 3: summing all adjustment lines gives 816,026.6 thousand. Neither convention is stated in a shipped file (the guide says hubs use the common list and that lines post "to" an account), though both are recoverable from the data (reopened denials swap codes at 1 July; write-off lines up to 413x their account balance).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | csv, pdf, xlsx, txt | yes |
| Large file | 25,000 rows or more | 234,729 rows (adjustments), 219,929 (accounts) | yes |
| Distractors in metadata.json | 2 or more, no file name labels one | fac_patient_experience_by_payer_2025.csv, state_charity_care_filings_fy2025.xlsx; names unlabelled | yes |
| Distractors weigh, unused, ruled out | relevant, a shipped fact rules out | thread found them usable and ranking nothing on the question; neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png) | yes |
| Asks | multi-dimensional, unit and rounding stated | 31-hospital cuts, thousands to one decimal, whole counts | yes |
| Prompt shape and 25 criteria | identifiable, 25 or more | 31-hospital list, measures, two scorecard columns; criteria count not tallied here, expected above 25 | yes (inferred) |
| Reads as LLM generated / golden realism | none | thread found no authoring leakage in contents.txt or PDFs; goldens (xlsx, png) not opened by me | not verified |
| Hygiene | licence, source, date | all 12 files CC0, dated | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Gate G passes. Design note (read after the thread returned): stump is the excess over each day's reorderings against pooled and held-day contrasts, estimation_fit, Layer 2. These match. Neither declared distractor is the surface read carrying the task. One internal inconsistency in the design note: the stump sentence says the held-day route files 23, while the Three rules domain test says "1 or 27". The thread measured 23 for stratified or fixed-effect contrasts, so the note's 27 and its pooled count "1" are stale, as the pooled route files 2 (judge: H03, H06 only). Not a bundle defect.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. Layer 1 is the three-hub conformance (UTC, hub move, double load, renumbering); Layer 2 is judging the within-day contrast against what chance alone produces given each day's determinations. Design note's `## Three rules` agrees (No decoy, Not semantics, Not rule application all present and substantive). Card file not located in the repo by search, so stump_class, analyst_test and domain_test were compared against the note only.

## Stump power (Gate F)
Thread: strong. The easy route (pooled gives 2, within-day held contrast gives 23) fails against the true 11, and it is natural to stop at the observed within-day contrast. Caveat for the main thread: the decisive step is a recognised standard method (permutation or every-order benchmark); the coordinator reports both blind stage 4 readers landed the 11, so the call is landable by a strong solver and architecture 1 is recorded as spent at Gate F. The asks (3 and 4) carry the rest of the stump.

## Findings, ranked
1. Residual main-call fork (23 vs 11): criteria 2.4 does not say the observed within-day share is not the chance. Closing it by naming the correction would file the HOW and turn the decisive step into rule application, so the thread's advice to edit the criteria is not endorsed here; accept the residual or file only the WHAT (net of what the same day's determinations would show in any order) after weighing that.
2. Ask 4 convention unstated: the 1 July 2025 renumbering of the reason list is not in the guide. Recoverable from data.
3. Ask 3 convention unstated: FAWO carries the application's whole write-off on every account it covers. Recoverable from data.
4. Design note counts (1 and 27) disagree with the stump sentence and the measured 2 and 23.
5. Cross-batch fingerprint not run by the thread; workbook, PNG and golden realism not checked.

## Next action for the author
If any repair is made, add two guide sentences (the 1 July reason-list renumbering with the code meaning on each side, and that an FAWO line carries the application's whole write-off on each account) touching only asks 3 and 4; otherwise record the report as evidence and proceed with the stage 4 result.
