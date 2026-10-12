# determinism-check report, task135, 2026-10-12

One isolated judge thread (Sonnet, medium effort) on the stage 3 cut (`target.zip` sha256 550f9762), the prompt and the submission's graded blocks. Its verdict follows verbatim; the Disposition after it is the build session's.

# Verdict, task135

**Verdict:** DETERMINISTIC (all committed answers reproduced; one residual fork noted below, not disqualifying).

**Disposition:** APPROVE. Optional FIX_NOW-grade tightening is listed under Fix; none changes what solvers see, so no rerun is required if skipped.

**Why:** The main call (60 per cent) is forced once the shipped pricing facts are applied. The mandate is priced at the London close (export notes), the funds are dealt at 12 noon on "latest available prices" (key facts PDF), and the data show the mandate correlating 0.20 with the North American fund's same-day return but 0.49 with its next-day return. Every period choice that policy 4.3 allows other than plain daily (2-day to 5-day blocks, weekly on any weekday anchor) puts 60 per cent at or under 9.6 and 70 per cent at or over 10.2. The lead/lag-corrected daily estimate gives 9.6 and 11.0. The only route to 70 per cent is the unadjusted daily estimate (9.41), which the pricing facts rule out for an expert. Gate C, residual risk: policy 4.3 does not forbid daily periods, so a purely literal solver who ignores the dealing-time facts can reach 70 per cent. The data separate the candidates, so this is method selection, not an open definition.

**Evidence (recomputed from the bundle):**
| Item | Golden | Mine | Source |
|---|---|---|---|
| Mandate daily TWR, 505 returns (equity + cash + rights + accrued, contributions and withdrawals stripped, demerger/rights/takeover carried in the lot values) | 505 | 505; annualised daily vol 15.1% | valuation_lots, capital_movements |
| Weekly Fri-Fri, 104 weeks, vol at 60 / 70 per cent | 9.0 / 10.3 | 8.97 / 10.34 | prices xlsx, lots |
| Daily with one-day lead and lag, 60 / 70 per cent | 9.6 / 11.0 | 9.60 / 10.99 | same |
| Daily alone, 60 / 70 / 80 per cent | 70 per cent clears at 9.4 | 8.24 / 9.41 / 10.63 | same |
| Range over 2- to 5-day blocks and weekly anchors Mon to Fri, 60 / 70 per cent | not stated | 8.9 to 9.6 / 10.2 to 10.9 | same |
| Sensitivity to mandate-return variants (flows at start or end of day, fees in or out, accrued in or out) | not stated | at most 0.02 point | same |
| Portfolio market value at 30 Nov 2026, accrued excluded | 32,908,401 | 32,908,401 | valuation_lots |
| Mandate income yield (ex-dates 1 Dec 2025 to 30 Nov 2026, one amount per designation, security and event; over mandate MV with cash) | 3.70% | 3.7018% | income_entitlements |
| Fund distribution yields NA / EU / JP / Gilt / Corp | not stated | 1.17 / 2.88 / 2.20 / 4.28 / 5.50% | prices xlsx |
| Income at 20 to 100 per cent steps | 1,442 / 1,368 / 1,295 / 1,221 / 1,148 / 1,074 / 1,001 / 927 / 854 (thousand) | 1,441,762 / 1,368,262 / 1,294,761 / 1,221,261 / 1,147,760 / 1,074,260 / 1,000,759 / 927,259 / 853,759 | derived |
| Running costs | 328,949 | 328,949 | budget xlsx, 13 lines of B2:B14 |
| 2027 grant payments (66 open instalments of non-withdrawn grants; core and first instalments on due date, later project instalments +35 to 70 days; 2 euro instalments at 1.1460) | 1,260,000 | 1,260,071; identical for every lag from 35 to 70 days | instalments, register, payments |
| Capital release 20 to 100 per cent | 147 / 221 / 294 / 368 / 441 / 515 / 588 / 662 / 735 | same, with and without rounding before subtraction | derived |
| Highest step with income at or above grants | 40 per cent | 40 per cent (1,294,761 vs 1,260,071); 50 per cent is short at 1,221,261 | derived |
| Grants plus running costs | 1,589,000 | 1,589,020 | derived |

Rounding margins are at least 239 pounds from a .5 boundary at every step.

Competing answers tested:
- **Daily alone gives 70 per cent.** Residual fork, see Why.
- **Summing the income file's lot lines gives a mandate yield of 5.31 per cent**, which pushes the 50 per cent step to 1,327k, above the grants, and flips the chart title from 40 to 50 per cent. The notes say "One line per tax lot", but the file repeats the whole event amount on every lot line. In 158 of 176 mandate events with a matching cash receipt in capital_movements, the max (and any single) line equals "Dividend received"; the sum is 2x on the 35 two-lot events. The shipped files resolve it, but only by reconciliation, not by any stated rule. This affects the supplementary answers (income rows, the 40 per cent title), not the main call.
- **Due dates only for grants** gives 1,298k instead of 1,260k. Procedure 7.4 says "expects to pay", and the payments file shows the 35 to 70 day lag for every later project instalment (140 of 140) and 0 days for core and first instalments (170 of 170), so the golden is the data-supported reading.
- **Excluding Glenrothes dividends, using accrued-inclusive MV, or excluding cash from the mandate base** moves 40 per cent income by 1k to 5k and leaves the title at 40 per cent.
- **Fernside's 15.3% and the factsheet volatilities** are distractors; neither can be combined without the correlations.

**Files/Hygiene:** PASS. 18 files, 5 formats (csv, txt, pdf, xlsx, docx). One 42,895-row lot file. Several distractors (Fernside report, factsheets, benchmark index, policy annex "2026 is 80%"). Dates are coherent (valuation 30 Nov 2026, exports 2 Dec 2026, budget draft 24 Nov 2026). Files read as system exports or house documents, with incidental mess: demerger, rights issue, takeover, legacy contribution, repeated lot lines, mixed date formats, euro grants. No authoring or benchmark disclosure found. No exclusion-level finding. Public-data contamination is not applicable (fictional entities). The cross-batch check was not run beyond the isolated bundle.

**Stump power:** Moderate. The attractive daily estimate stays inside the cap at 70 per cent (9.41), so a solver who ignores the noon dealing point and the previous-New-York-close pricing files a wrong call. The cure (weekly, or lead/lag) is well known and the dealing facts are visible in the key facts PDF, so a strong run that reads them gets the call right. The asks add independent failure points: the repeated lot lines (income, title), the payment lag (grants), the 12-month ex-date window, and the TWR handling of flows and corporate actions. Estimated: the main call stumps some runs, the asks do more of the work. Too-easy signals are limited to the documented pricing points.

**Stumping type:** `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The difficulty is choosing a volatility estimator that survives non-synchronous valuation points on honest data, with no reported number being wrong. On clean, synchronously priced data the task would collapse, but the staleness is the dataset's own structure, not a planted defect. This passes Gate G.

**Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1 is the mess: a mandate with corporate actions and external flows across two designations, funds dealt at noon, lot-repeated income lines, euro grants and a payment-lag history. Layer 2 is estimating policy volatility with non-synchronous pricing (Epps-type bias). Swap test: with other nouns, the stale-pricing volatility estimate against a cap stops making sense, so the domain is real. The easy route is the daily covariance estimate, which gives 9.41 at 70 per cent and a wrong call of 70. A strong analyst who cleaned everything correctly can still take it, so H3 passes as analytical. Data semantics (lot repeats) and rule application appear only in the asks.

**Fix:** none required (location: none). Optional, if the author wants to shrink the residual forks without changing the solver-visible analytic surface:
1. Add one sentence to the income-entitlements export notes, or to the prompt, saying the entitlement on each lot line is the event total for the security. Doing so would weaken the semantics step. Alternatively leave as is; the reconciliation to capital_movements resolves it.
2. Record in the design note that daily periods are permitted by 4.3 and ruled out by the pricing facts. That fork is already closed in the golden's own critical components.

## Disposition

**APPROVE.** No FIX_NOW item, no re-judge.

- Gate G and Gate H: the thread's stumping type (method_or_model_selection, analytical_non_defect, no surface-read dependency, no sole data defect) and its three-rules line (domain pass, layers pass, decisive_step analytical) match the card (`gate_g` method_or_model_selection, `stump_class` analytical) and the design note.
- The residual under Gate C, daily periods, is the designed method selection. Policy 4.3 admits daily periods; the data rule out the plain daily estimate (at 60 per cent the portfolio's daily returns carry a lag-1 autocorrelation of 0.177, t 3.97, the variance of five-day sums is 1.347 times five daily variances, and the mandate correlates 0.20 with the North American fund's same-day return against 0.49 with its next-day return), and daily periods with their lead and lag terms land 60. Optional fix 2 is done: the record is in the design note's `### Stage 4`.
- Optional fix 1, a sentence saying each lot line carries the event total, is declined. The repetition is ask A's designed primary device (D6), it touches no main-call figure, the thread itself resolved the grain from the shipped dividend receipts, and the sentence would name the device.
- The grant lag is the ask's clock device (D8), supported by the payment ledger as the thread found; every lag from 35 to 70 days gives the same 2027 total (asserted).
- The leak reader's three readings (the number of equal periods, the month-end valuation, a cap on the release at the expendable endowment's value) are answered in the design note without a pin. The cap never binds: the expendable endowment is worth £11,002,669 at 30 November against the largest release of £735,262, now asserted in `checks.py` and `verify.py`.
- The stage 4 pass changed no document under `target/` and moved no graded figure: `target.zip` rebuilds byte-identical to the judged cut (sha256 550f976258b084f0e1d055571c322cee3bcf25160c8ba482df7a3364a9f67330), the goldens are byte-identical, and `freeze.py check --mode determinism` passes. The verdict stands.
