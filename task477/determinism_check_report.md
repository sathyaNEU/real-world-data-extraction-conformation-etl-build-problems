# determinism-check report, task477, 2026-10-20

Judged on the bundle the thread saw (fresh unzip of target.zip at /tmp/determinism-check-task477-1792497263/target/). The pack under task477/target was being regenerated while this report was written (two ask devices re-sited, next-in-line margin widened); nothing here speaks for the regenerated pack.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (with one soft spot on the next in line, below; the coordinator's regeneration already targets it, so the regenerated pack should be re-judged once if the author wants the margin confirmed)
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no (borderline), sole_data_defect: no

## Why
The slate (Information, Finance and insurance, Professional/scientific/technical, Construction) reproduces from the shipped QCEW files once wages are put on the Fund's work-performed basis (guidelines 2.2) and the quarter-paid rule in the layout notes is applied. The easy route (pay per job as recorded) files Transportation and Health care in and Professional and Construction out. Exiter counts and ITA payments follow filed rules (manual 4.1 to 4.3, guidelines 3.3) and reproduce exactly.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Eligible industries (2025 jobs >= 1,000, annual release, own 5, agglvl 74) | 15 | 15 (smallest in: Real estate 1,465, Arts 1,350; out: Utilities 424, Management 779) | yes |
| Growth, whole percent, all 15 industries | Info 22, Fin 21, Prof 19, Constr 19, Mfg 18, Transp 18, Health 18, Wholesale 17, Accom 17, Retail 15, Admin 15, Other 14, Arts 14, Educ 13, Real estate 13 | 21.9/21.1/19.2/18.9/18.2/17.9/17.7/17.2/16.8/15.2/14.8/14.1/13.8/13.2/12.9 | yes |
| Naive paid-basis slate | Info, Fin, Transp, Health (Prof next) | same | yes |
| Exiters in eligible industries | 753 (per industry as in submission) | 753, every industry matched; 1,084 participants after last-exit rule | yes |
| ITA payments by industry | 15 figures, total $876,413 | all 15 to the dollar; unrounded sum 876,412.47; 126 of 130 checks issued 2025 and not voided | yes |

## Competing answers that survived
1. Pay calendar and roll rule are not filed in any shipped text. Literal "paid basis, no correction" gives Info, Fin, Transp, Health, next Prof. Weekend-only or no-roll calendars give Info, Fin, Constr, Transp, next Health. The golden calendar (four biweekly phases from 2021, roll to the prior business day) is selected by fit (summed squared log residual 0.068 against 0.142 / 0.180 / 0.419), not by text. The design note closes this as SF5 "ruled out by the data"; the thread accepted that. Left as a finding, not a fork that flips the golden under the fitted method.
2. Order within 18% (Mfg 18.2, Transp 17.9, Health 17.7): needs unrounded growth. The ridge variant ties Mfg and Transp at 18.3 and the poorly fitting weekly model puts Transp first (18.5 against 17.9). All print as 18%, so the csv is unaffected; the "next in line" name is the exposed item.
3. Annual factor (14/365 per pay date against count over 26): under 0.05 point, no effect on any call.
4. Ledger voucher_amount is a voucher total repeated per installment line; undocumented but forced by reconciliation to the register.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 | yes |
| Formats | 3 or more | csv, xlsx, pdf | yes |
| Large file | 25,000 rows or more | 49,672 / 41,522 rows (QCEW csv) | yes |
| Distractors in metadata.json, none labelled by file name | 2 or more | 2 (tallis_industry_projections_2024_2034.xlsx, oews_tallis_county_may2025.xlsx); names neutral | yes |
| Distractors unused yet weighable, none answers a graded quantity | yes | projections are growth in jobs, OEWS is occupational hourly wages; neither reproduces pay-per-job growth; shipped notes rule them out | yes |
| Deliverables | 1 to 3, all in golden | 2 (csv, docx), both in submission section 4 | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 15-row by 4-column csv; prompt states whole percent, whole numbers, nearest dollar | yes |
| Prompt shape and 25+ rubric criteria | yes | ranked list under a cap (shape 01); 15 industries x 4 figures plus slate and next in line gives well over 25 gradable items (rubric itself not generated yet) | yes |
| Nothing reads LLM generated, goldens real work products | yes | thread found no authoring or benchmark language; fictional names, coherent dating; docx not opened by me | yes (docx unchecked) |

## Gate G reconciliation
Thread: mechanism decomposition_attribution, stumping_family analytical_non_defect, surface_read_dependency no (borderline), sole_data_defect no. Design note and card: strategy composition_mix, decisive generator G3 (record counts pay when paid, decision runs on work done), estimation_fit, nothing planted. Consistent: both place the difficulty in estimating a calendar effect from honest data. The thread notes a reader could call it a lens swap (paid against earned); route to live testing if the family is contested. Declared distractors (projections, OEWS) were not named by the thread as the surface read, so they are not too load-bearing. The surface read the thread named is the QCEW pay per job as recorded, which is the default path in the note and is wrong by design; the note's Gate G classification (no shipped artifact ranks candidates wrongly) holds.

Discrepancy to record: the design note says the golden family prints every growth at the same whole percent with nearest edge 0.14 and the fourth over fifth margin is 0.70. The thread finds the fifth place margin over Transportation is 0.3 point, with the ridge and weekly variants tying or flipping it. The note's margin claim covers the fourth/fifth slate boundary, not the order inside the 18% group; the regeneration the coordinator reports is aimed at exactly this.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. Matches the note's Three rules (domain test, Layer 1 vintage overlap, NAICS recode, undisclosed cells, PEO and co-enrollment mess; Layer 2 pay-date exposure estimated from the series). No mismatch with the card.

## Stump power (Gate F)
Strong per the thread: the reported ranking is the easy route and files the wrong slate (Transp and Health in, Prof and Constr out); the solver must recognise a 27th-pay-date year and estimate each industry's payroll mix from the quarterly pattern. The notes and guidelines say "paid versus performed" in plain words, which lowers but does not remove the difficulty. This is a field-standard method (calendar-effect regression), so a strong solver may land it; weigh against the scored readers' result. The exiter (PEO mapping) and ITA (check basis) asks add independent traps.

## Findings, ranked
1. Next in line (Manufacturing 18.2, Transportation 17.9, Health 17.7) has a 0.3 point margin and flips or ties under the ridge and weekly estimators. Soft spot; the regeneration to widen it addresses this.
2. The pay calendar (four phases, 2021 start, prior-business-day roll) is unfiled and recovered by fit. Closed by the data (SF5), thread accepted; a solver who fits a different calendar gets a different slate (Constr, Transp in; Health next), so the closing rests on the fit being visible.
3. ITA voucher_amount semantics undocumented, forced by register reconciliation. Not stump affecting.
4. Minor hygiene: register has no void check lines; ledger has no schema note.

## Next action for the author
Let the regeneration finish, confirm in checks.py that the new next-in-line margin clears the ridge and weekly variants, and re-judge once (FIX_NOW rule) only if you want the widened margin confirmed by the thread; otherwise proceed to ship on this APPROVE.
