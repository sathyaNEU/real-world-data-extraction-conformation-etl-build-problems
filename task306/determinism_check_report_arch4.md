# Determinism verdict, task306

- **Verdict:** NOT_DETERMINISTIC
- **Disposition:** SEND_BACK. The cost-curve convention that sets the runner-up, the gap and the kept-alpha figures is in no shipped file. It has to be filed in the pack (or the asks re-pinned to figures that survive the method), so solvers see different files and need a rerun.

## Why
The main call (UK Mid Cap Value) is forced: it wins in every variant I ran. The runner-up, the GBP 2 million gap and the "alpha kept" figures (asks 2, 3 and 4 on the deck) are not forced. They come from a fitted cost curve: band intercepts plus a single slope on daily volatility times the square root of participation, unweighted least squares over every order, with consolidation days skipped. None of that is in the files. The IC-07 policy says only "estimated from the desk's own executions", and the TCA standard defines shortfall and participation but no curve. The square-root law appears only in the solution blocks. Gates C and E fail, taxonomy label underspecified_objective. The fix is in the input files.

## Evidence (recomputed with pandas from target/)
**Reproduced:**
- The 125 duplicate exec ids are identical rows.
- GBP fills are converted to pence (times 100).
- All 564 BACKUP-RECOVERY orders match one TERMINATED original each on account, stock, side and London date, and the recovery quantity equals the original's unfilled quantity (100%).
- Block orders split by oms_block_allocations; the allocated quantities sum to the filled quantity.
- Rebalances from 1 Dec 2025 to 30 Nov 2026 scaled to GBP 400 million trade GBP 1214 million (SCM), 523 million (MCV) and 493 million (LCQ). This matches the golden.
- Gross alpha is 20.2, 11.6 and 7.2 (summary sheet of research_backtests_2027_candidates.xlsx), which round to 20, 12 and 7.
- Fit A (band intercepts 3.3 / 9.0 / 26.3 bp, slope 0.865 on vol times sqrt participation, unweighted OLS over orders with a full vol history) gives kept alpha 4.93, 7.68 and 5.67. That is 5, 8 and 6, a gap of 2.01, with LCQ as runner-up. The golden reproduces under this one fit.
- Workbook ask 1, quarterly shortfall, matches every cell. It uses the dated account register: WM-DYN-01 is UK Dynamic to 30 June 2026, and the Severnvale slice (17 Aug to 13 Nov) is excluded. Counting that slice would give Q3 53.2 and Q4 48.3 instead of 52.1 and 35.4.
- Workbook ask 2, value traded by half year, matches every cell (360, 252, 113, 122, 1088, 899, 801, 967).

**Forks that move the committed answers (kept alpha SCM / MCV / LCQ, GBP million):**

| Variant | SCM | MCV | LCQ | Runner-up | Gap |
|---|---|---|---|---|---|
| Fit A, the golden | 4.93 | 7.68 | 5.67 | LCQ | 2.0 |
| Exponent 0.4 | 5.88 | 7.90 | 5.65 | LCQ | 2.0 |
| Exponent 0.6 | 4.28 | 7.55 | 5.72 | LCQ | 1.8 |
| Exponent 0.7 | 3.91 | 7.50 | 5.79 | LCQ | 1.7 |
| Common intercept instead of band terms (unweighted) | 3.35 | 6.62 | 4.93 | LCQ | 1.7 |
| No band, one slope, through the origin (unweighted) | -0.97 | 5.57 | 4.80 | LCQ | 0.8 |
| Value-weighted, one slope, no band | 7.19 | 7.89 | 5.72 | SCM | 0.7 |
| Value-weighted, common intercept | 7.74 | 7.91 | 5.51 | SCM | 0.2 |
| Fit A with the ESG-listed names dropped from the rebalance log | 5.64 | 7.72 | 5.77 | LCQ | 1.95 |
| Fit A with volatility not skipping consolidation days | 7.11 | 8.29 | 5.89 | SCM | 1.2 |

- Data separation is weak. R2 for vol times sqrt(p) with band terms is 0.4655, against 0.4637 for p^0.6, 0.4630 for p^0.4 and 0.4344 for p^1. Residual spread rises with participation (13 bp to 27 bp), so a value-weighted fit is a defensible alternative. The data do not force the golden's form.
- The ESG list (esg_exclusions_2026.csv) is not mentioned in IC-07. The rebalance log still holds 77 SCM and 24 LCQ rows in names listed from 15 Jan 2026, which contradicts the workbook note that the simulations apply the exclusions in force. If a solver drops them, SCM kept alpha is 5.64, which rounds to 6, not 5. The runner-up margin over SCM shrinks to 0.13.
- The consolidation dates are dd/mm and the data are resolvable. Skipping consolidation days in the volatility is not stated in the TCA standard, and not skipping flips the runner-up. This is a legitimate Layer-1 cleaning step, but it sits on top of the unfiled curve.
- 755 early-2025 orders (Feb 2025) lack 60 sessions of history and are silently dropped from the fit.
- Under the literal reading, the main call (MCV) and gross alpha (ask 5) are determinate. The runner-up (ask 2), the gap (ask 3), kept alpha for SCM and LCQ (ask 4) and the SCM figure inside critical component 3 are open.

## Files/Hygiene
PASS, with notes. There are 13 files in 5 formats (csv x7, pdf x2, xlsx x2, parquet, eml). One file has 329,800 rows (market data) and the fills file has 61.7k. The files read as operational extracts, with duplicate exec ids, mixed price units, backup-recovery orders and dd/mm consolidation notes. The ESG list and the commission schedule are plausible distractors. I found no authoring or provenance leakage and no temporal incoherence. The TCA standard is dated 1 Jan 2026 and IC-07 14 Apr 2026, and the request is dated 1 Dec 2026, which is consistent. Nothing is exclusion-level. The ESG-listed trades in the log versus the workbook note is a minor in-fiction inconsistency.

## Stump power
The consolidation days in daily volatility (skip them or not) flip the runner-up, as shown above. The decisive 400 million call is not stumped by this: MCV wins in every variant. The load-bearing stump is therefore on the supplementary and kept-alpha figures, not the main call. The easy route is a naive volatility, a simple average-cost-per-bp curve, or ignoring that participation scales with size. Those route to a different runner-up and kept alpha, which a solver can also reach legitimately through the unfiled curve choice. Stump power for the main call is weak because the winner survives all variants. A natural lever is to make the ranking depend on the capacity effect: the SCM versus MCV order has to come out on the fitted impact curve, not on gross alpha. Today SCM is the large-gross-alpha decoy and loses in every fit.

## Stumping type
mechanism: method_or_model_selection (cost-curve fit for impact at size), plus etl_conformance; stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no. The difficulty is estimating a participation-driven cost curve from the desk's own executions and extrapolating it to a large size. Reported numbers are not misleading, so Gate G passes.

## Three rules
domain: pass, layers: pass, decisive_step: analytical. The field's own analysis is market-impact modelling and capacity-adjusted alpha: fit the desk's shortfall against participation and volatility, then net each strategy's alpha at the allocated size. Layer 1 is the order conformance (duplicates, pence and pounds, recovery merge, block allocation, consolidation days, the dated register). Layer 2 is the impact fit and extrapolation. The easy route is to rank on gross alpha (picks SCM, 20 million) or to apply a flat average cost; both fail the call. The decisive step is analytical. The problem is that its method is not pinned for the supplementary figures.

## Fix
- **Where:** input_files. Prompt changes are an alternative.
- **Change 1:** File the WHAT for the cost estimate in IC-07 section 2 or the TCA standard: that expected cost is to be estimated on the participation-driven impact curve from the desk's orders, with the weighting, whether the index band enters, and the treatment of orders with fewer than 60 prior sessions pinned. If that would turn the decisive step into rule application, file only the estimand and let the data separate the form. That needs the data to separate the candidate forms, which it currently does not (R2 gap 0.002).
- **Change 2:** State how the ESG exclusion list relates to the rebalance trade log (in or out), or remove the post-effective-date names from the log.
- **Change 3:** Alternatively re-pin the asks to figures robust to the form: keep the recommendation and the gross alpha (ask 5), but drop or coarsen the runner-up and gap (asks 2 and 3), or widen the margin between the runner-up candidates.
- **Frozen:** workbook asks 1 and 2 reproduce and need no change.
