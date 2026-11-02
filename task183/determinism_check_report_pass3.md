# determinism-check report, task183, 2026-11-02 (pass 3, run a4b)

## Verdict
DETERMINISTIC, plus SOLUTION_WRONG (minor, SOLUTION_STEPS step 7 wording only)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The thread reproduced the golden from the raw files. A within-customer fit of each lodgement on the card trade since the previous lodgement day leaves a fixed per-lodgement sum only at BC-10896 (99,899, referral 100,000) and BC-10731 (49,952, referral 50,000). Every other card customer is at EUR 1,346 or less. Every till customer is negative under BCR-3 4.2. All 12 monthly post office cash and fee figures and all 12 monthly till cash sales and paid-outs reproduced to the cent.
Two defects. (1) SOLUTION_STEPS 7 says the repeated Z-log rows were dropped, but the Z log has none (9,271 rows, no duplicate rows, no duplicate till_account + z_no). The duplicates are in the AN POST export (39) and the account export (8,319). This is wording only, and no figure moves. (2) BCR-3 4.2 defines own trading only for till customers, so for card customers "what their own trading did not take" is unfiled. A peer cash-to-card reading would also refer BC-10444, BC-10643 and others. The thread judged that reading not defensible: the standard says "own" trading, peer ratios run 0.27 to 1.50 within a trade, and no benchmark ships. If a reviewer disagrees, the failure type is underspecified_objective.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| BC-10896 unexplained cash | 99,899 (EUR 100,000) | 99,899 (about 969.9 x 103) | yes |
| BC-10731 unexplained cash | 49,952 (EUR 50,000) | 49,952 (about 485.0 x 103) | yes |
| Highest other card customer | 1,346 | BC-10551 1,346; BC-10444 395; BC-10643 -1,487 | yes |
| Till customers (12) | all negative | -908 to -8,542 | yes |
| Post office cash and fee, 12 months | as listed | match to the cent | yes |
| Till cash sales and paid-outs, 12 months | as listed | match to the cent | yes |
| Z-report placement | 9,271 rows | 9,271 of 9,271 match | yes |
| Step 7 "repeated log rows dropped" | dropped | none exist | no (wording) |

## Competing answers that survived
1. Window convention. Counting the lodgement day's own card trade gives EUR 94,183 for BC-10896, which rounds to 95,000 against the golden 100,000. BC-10731 is 49,601, which is still 50,000. Fit residuals separate the two conventions only weakly (58.9 against 62.9 for BC-10896; 29.3 against 29.7 for BC-10731). No shipped sentence files the window.
   Do the data settle it? Yes, but only by calibration, not by a filed rule. On the 12 till customers the day-before window reproduces every lodgement as cash sales less paid-outs to the cent, and the own-day window misses on nearly every lodgement. The design note's fork SF4 also names the lodgement times as evidence, with every lodgement handed in before 13:00. A solver who never back-tests on the till customers has no sentence to close it and would file 95,000 for the car wash. That is a graded-precision tail risk, not an open fork for a careful reviewer. Disposition: closed by data, not by text; I recommend recording it as such and not adding a HOW sentence (filing the window would turn the decisive step into rule application).
2. Peer-ratio reading (BC-10444 and BC-10643 and others referred). Judged not defensible, as above. Main residual risk, and the intended easy route.
3. Through-origin fit gives about 13.6k and 1.9k, so no competing referral list. Counter date against posting date is closed by BCR-3 3.2.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | CSV, XLSX, PDF | yes |
| Large file | 25,000 rows or more | account export, 66,735 rows | yes |
| Distractors named in metadata.json, none labelled by file name | 2 or more | 3 (retail_sales_index, branch_cash_orders, an_post_office_list), no file name labels one | yes |
| Distractors unused yet weighable | yes | unused by every figure (thread confirmed); none answers a graded quantity | yes |
| Deliverables | 1 to 3, all in the golden | 2 (docx, xlsx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | referral to nearest EUR 5,000; 12-month tables to the cent; each states unit and rounding | yes |
| Prompt shape and 25 or more rubric criteria | yes | shape 01 per metadata; the rubric is generated and is not in the package, so the count is not verified here | not verified |
| Reads as real, not LLM generated | yes | thread found system-export artefacts (duplicate refs, platform change by office, batched Z uploads), no authoring language | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note's decisive step is the lodgement-window decomposition with a part that does not move, against a peer ratio (readability row 3, silent). These match. The thread does not name a declared distractor as the surface read, so no too-load-bearing finding. The thread's easy route (peer ratio) is the note's rows 1 and 2.
**Gate G line:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no; passes Gate G.
**Gate H line:** domain: pass, layers: pass, decisive_step: analytical. This matches the note's rule-3 reading. It is not a case of the field's standard method reached with no judgment, because the fit is chosen by the solver and the data have to separate it from the peer ratio.

## Stump power (Gate F)
Strong on the main call. The easy route (peer cash-to-card ratio) refers BC-10444 and BC-10643 and may miss BC-10731 (ratio 0.365 against a 0.552 median). A strong model that fits cash on card by customer will likely find both fronts, so one of the top two may well land the call. The second graded precision (100,000 against 95,000 under the own-day window) is a tail risk. The asks add real hardness (notes_eur platform rule, late and batched Z-reports, counter-date dating). The main thread should weigh landing probability against the design note's ladder.

## Findings, ranked
1. FIX_NOW: reword SOLUTION_STEPS 7. Drop the claim that repeated Z-log rows were dropped; the duplicates are in the AN POST and account exports. No figure moves and no rerun is needed.
2. Residual, by data only: window convention (95,000 against 100,000 for BC-10896). Record it in the fork table as closed by the till back-test and lodgement times.
3. Optional and not required: one sentence in the prompt or BCR-3 filing that, where there is no till, own trading is read from the customer's own card trade lodgement by lodgement. It would close the peer-ratio fork, but it names the card trade and so risks filing the HOW. The design note argues against it, and it would change what solvers see.
4. Rubric criteria count not verifiable from the package.

## Next action for the author
Reword SOLUTION_STEPS step 7 in the generator and in submission.md so it no longer says repeated log rows were dropped, rebuild, and confirm that the figures and byte-identity are unchanged.
