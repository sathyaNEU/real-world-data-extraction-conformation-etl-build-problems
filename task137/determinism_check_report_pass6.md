# determinism-check report, task137 (pass 6), 2026-11-01

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (two optional soft items below, no re-run)
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

One thread, one pass. Pack unchanged (target.zip md5 8f5c6aa228c4385bd09c5d4fdf29e2c8, 12 files). Judge output: /tmp/determinism-check-task137-1793551442/verdict.md.

## Why
Read literally, the plan is 2025-26 GP-form arrivals with the run-out suppression taken out, grown by 1.035 squared. It lands in the 45,000 bucket (43,750 to 46,250) for every window of 5 weeks or more and for all the spec variants the judge ran (44.7k to 45.4k; two cruder specs gave 46,085 and about 43.9k, still 45,000). Shipped-text easy routes land on 42,500 (seen plus turned away, or a window of 4 weeks or fewer) or 40,000 (seen only). Pass 5's two soft forks: the AIC margin claim now reads "at least 60", and the judge reproduced it only on the golden's own common sample (30 worse on its sample; see findings). Fork on the unassigned roster lines is still not stated in any pack sentence.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| GP seen 2025-26 | 37,853 | 37,853 | yes |
| Hospital seen 2025-26 | 17,222 (implied by grid) | 17,222 | yes |
| GP turned away | 1,365 on 56 of 253 days | 1,365 on 56 of 253 | yes |
| Window by AIC | 8 weeks | 8 (AIC 7003.0; 9 weeks 7005.9) | yes |
| Lag coefficient | about -0.37, SE 0.026 | -0.372, SE 0.026 | yes |
| Windows of 5 weeks or fewer | at least 60 worse | at least 60 on the golden's sample, at least 30 on the judge's | partly |
| Underlying 2025-26 | about 41,800 to 42,000 | 41,768 (L=8), 41,987 (L=9); practice split 41,803 | yes |
| Plan | 45,000 | 44,745 to 44,980 | yes |
| Hospital visits, 28 cells | as filed | all 28 match | yes |
| Old to new clinic code link | C01=DIA, C02=CAR, C03=RHE, C04=GAS, C05=REN, C06=GEN, C07=HAE | unique, weekday sets pairwise distinct; register clinic_days match no old set | yes |
| Sickness days and rate by quarter | 29/6.8, 23/5.6, 39/8.7, 23/5.2 | 29/6.79, 23/5.60, 39/8.71, 23/5.22 | yes |

## Competing answers that survived
- Window under 5 weeks: 42,500 vs 45,000. Closed by the fit across windows (the data separate them); intended wrong route.
- Q3 sickness: Sickness lines only gives 11/10/13/9 days (rates about 2.0 to 2.9 per cent) vs the golden's 29/23/39/23. No pack sentence ties unassigned lines after five Sickness days to sickness; the single-vacancy statement in the annual report plus a 5-of-5 pattern is the only closure. Ask-level, not the main call.
- Chart content (stack of seen, turned away, kept in-house) and the partial weeks at the financial-year ends are not pinned by the prompt. Ask-level, minor.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, json) | yes |
| Large file | 25,000 or more rows | queue events 204,783 rows by the judge (metadata says 306,115); legacy 85,649 | yes (metadata row count disagrees with the judge's, either clears the gate) |
| Distractors | 2 or more in metadata.json, none labelled by file name | patient survey, hub session plan; neither named as distractor in a file name | yes |
| Distractors unused, relevant | yes | unused by the answer; the judge found no graded quantity reproduced from either | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 7x4 specialty grid, quarterly days and rates; units and rounding in the sentence | yes |
| Prompt shape and 25 or more criteria | yes | shape "other"; 28 grid cells plus plan, 4 days, 4 rates, chart: well over 25 gradable figures, rubric itself not seen | yes (rubric not inspected) |
| Not LLM-looking, goldens real | yes | judge found no disclosure; mixed time formats, text dates, month-total rows, test tickets | yes (golden realism not re-judged here) |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and metadata: the card's stump is displaced demand from the practices' in-house habit, window chosen by fit; the declared distractors (survey, session plan) are not the surface read carrying the task, so the distractors are not too load-bearing. The thread's mechanism matches the note. One numeric drift: the design note's Three rules lines say "at least 67 worse" in AIC for windows of 5 weeks or fewer, the write-up says "at least 60", and the judge's own sample gives 30. The 65.3 gap the pass-5 judge saw at L=5 on the golden sample sits between them; the note should be brought in line with the write-up. No effect on the call.

## Gate H
domain: pass, layers: pass, decisive_step: analytical (thread). The note's analyst test agrees: a strong analyst who reads every file correctly files 42,500 from the previous week's or ten days' run-out share. This is a model-selection decisive step (window by fit), not a decoy, field reading or executed rule; the note's stump_class and domain_test were read and are consistent.

## Stump power (Gate F)
Good on paper. Both easy routes (seen plus turned away, short-window models) file 42,500 and seen alone files 40,000; only the full lag window with the practice-level check lands the call. Risk: the 2,500 rounding band is wide, so any solver whose lag effect runs 5 weeks or more banks the main call, and the thread's spec spread shows the band absorbs most specification noise. The ask layer (7x4 grid behind a code-mapping inference, the sickness-rate inference, two-layout turned-away log) carries independent difficulty. The main thread weighs this against the design note's ladder.

## Findings, ranked
1. Soft, ask-level: unassigned roster lines after five Sickness lines are counted as sickness (Q3) with no pack sentence stating it. Consider one sentence in the write-up or accept the exposure.
2. Soft, wording: the "at least 60 worse" AIC claim reproduces on the golden's sample only (judge's own common sample gave at least 30 worse). Say "on the model's sample" or soften; align the design note's 67.
3. Soft, ask-level: chart stack not specified by the prompt; kept-in-house layer is model-estimated and moves with the window (8 or 9); partial weeks at financial-year ends not pinned.
4. Hygiene: metadata.json queue-events row count (306,115) differs from the judge's count (204,783); correct the record. Licence and source records not visible to the judge, unchecked here beyond metadata saying CC0-1.0.

## Next action for the author
Ship. Optionally, before the reship, align the AIC margin wording and the design note's 67, and correct the row count in metadata.json; no regeneration needed.
