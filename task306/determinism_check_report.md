# determinism-check report, task306 (architecture 4, pass 2 re-judge), 2026-10-31

Pass 1 of architecture 4 is kept as determinism_check_report_arch4.md. This pass judges target.zip sha256 7f2aba0203b068e17d4e9f34b8d8a86f19cc4ca361c02f18128409d045b2ad35 (rebuilt byte-identically) after the FIX_NOW. Judge thread output: /tmp/determinism-check-task306-225642/verdict.md.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
**Gate H:** domain: pass, layers: pass, decisive_step: analytical

## Why
IC-07 section 2 files the estimand: the 2015 to 2026 gross alpha as the workbook reports it, less the implementation shortfall of the twelve months of rebalances to 30 November 2026, scaled to GBP 400 million. It also files that costs are estimated from the desk's executions in the index band the candidate trades. TCA standard sections 1 to 3 fix shortfall, value, participation and volatility, including the consolidation day giving no return and the 60-session history. The judge rebuilt everything from the raw files. UK Mid Cap Value wins, UK Large Cap Quality is runner-up and the gap is GBP 2 million under every band-wise form tried, and all workbook figures reproduce.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Rebalance value at GBP 400m (SCM / MCV / LCQ) | 1211 / 524 / 485 | same (12, 4, 4 rebalance dates; no traded ISIN on the ESG list; every ISIN joins to a SEDOL) | yes |
| Gross alpha (Summary column "Annualised gross alpha, 2015 to 2026") | 20 / 12 / 7 | 20.2 / 12.08 / 7.36 | yes |
| Band-wise cost with intercept | not filed as a figure | 15.3 / 4.09 / 1.46 | n/a |
| Kept alpha | 5 / 8 / 6 | 4.9 / 7.99 / 5.9 | yes |
| Runner-up and gap | LCQ, 2 | LCQ in all band-wise variants; gap 2 in 15 of 16 unrounded (1.78 in the other, which also rounds to 2) | yes |
| Conformance: duplicates, pence/pounds, backup merge, blocks, consolidations | as filed | 122 duplicate rows; 15,584 pound fills; 494 backup orders one to one; block allocations sum exactly; 8 consolidation days match 8 jumps of about 10x | yes |
| Workbook ask 1 (16 cells) | as filed | matches every cell | yes |
| Workbook ask 2 (8 cells) | as filed | matches every cell | yes |

## Competing answers that survived
Recorded residual (not a blocker): the form of the cost curve is not filed. Fitted without an intercept, UK Smaller Companies Momentum (SCM) keeps 3.64, which rounds to 4 instead of 5. The call, the runner-up and the gap are unchanged. The data separate the forms: the SmallCap R2 is 0.77 with an intercept against 0.68 without, and free-exponent fits recover 0.46 to 0.51 with intercepts of about 3, 9 and 22 to 25 bps. So the intercept form is the one the data favour. It touches only SCM's figure in deck ask 4 and critical component 3.
Considered and closed:
- A pooled all-band fit makes SCM the runner-up, but IC-07 section 2 excludes it ("stocks of the index band the candidate trades").
- The arithmetic mean of the Annual alpha sheet differs from the Summary column. IC-07 says "as the workbook reports it", and the Summary column carries that label.
- Sample against population standard deviation, and 59 against 60 returns across a consolidation day: every rounded figure is stable.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | 5 | yes |
| Large file | 25,000 rows or more | market data 329,800; fills 61,700 | yes |
| Distractors | 2 or more, named in metadata.json, none labelled by file name | broker_commission_schedule_2026.xlsx, esg_exclusions_2026.csv | yes |
| Distractors unused yet weighed; ruled out by a shipped fact | required | commissions are excluded by IC-07. No traded ISIN is on the ESG list, so it is now inert | yes |
| Deliverables | 1 to 3, each in the golden | 2 (pptx, xlsx) | yes |
| Asks | multi-dimensional, unit and rounding stated | deck asks 1 to 6, workbook 24 cells; rounding stated in the prompt | yes |
| Prompt | one paragraph, question first, under 1,000 characters, no data counts | 608 characters | yes |
| Rubric of 25 or more criteria | required | not generated here; the 6 deck asks and 24 workbook cells make it plausible | not verified |
| Reads as real, not LLM generated | required | the judge found authentic operational mess and no authoring leakage | yes |

## Gate G reconciliation
The design note and card were read after the thread returned. Thread: method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Note and card: a size-dependent shortfall curve, stump_class analytical, with the band-average capacity check as the default path that files SCM. These match.
- The declared distractors are not the surface read carrying the task.
- Pass 1's mismatches are closed. The consolidation skip is now filed in the TCA standard (SF12, SF13), the ESG list is inert (SF14), and the index band is filed in IC-07 (SF11).
- One mild gap in the note: it asserts that kept alphas hold across 31 variants. The no-intercept form moves SCM from 5 to 4, which is the recorded residual above. The note's fork table should carry that form as a row.

## Gate H
domain pass, layers pass, decisive_step analytical. This agrees with the card's `analyst_test` and `domain_test`. Layer 1 is the order conformance. Layer 2 is a participation-scaled cost curve per band, read at the size the desk never traded.

## Stump power (Gate F)
The thread rates it good. Even after correct cleaning, the easy route of a flat desk-average shortfall on turnover files SCM (cost about 7 against 20.2 gross), and the right analysis overturns it to about 5. The thread classed the decisive step analytical. IC-07 now files the population (the candidate's own index band) but not the curve's shape, so the shape is still read from the executions. For the main thread to weigh: a per-band square-root fit is the field's textbook impact route, so a strong solver can reach the call. The quarterly and half-year workbook asks add independent multi-cell reconstruction through the account register, backup merge and block allocations. The main thread weighs this against the design note's ladder.

## Findings, ranked
1. Residual, recorded: the cost-curve intercept is unfiled. The no-intercept fit gives SCM kept 3.64, rounding to 4 against the golden's 5. The data favour the intercept (R2 0.77 against 0.68). The main call, runner-up, gap and every workbook figure are unaffected.
2. Note hygiene: the "31 variants" claim and SF3 should record the no-intercept fit.
3. The thread offered an optional prompt or IC-07 touch naming the curve's form. It is not taken. Naming the form would file the HOW and turn the decisive step into rule application.

## Next action for the author
None required. Approve and proceed. Optionally, add the no-intercept form as a fork-table row in the design note, citing that the data separate the forms. Do not name the curve's form in the prompt or IC-07.
