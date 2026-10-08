# FC10 — Are recent accident years really better? Developing immature losses before comparing them

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Immature cohort metrics compared with mature ones (LTV of recent user cohorts, warranty claims by build month, chargebacks by transaction month) without development to ultimate |
| Domain | Property & casualty insurance / reserving and pricing |
| Task shape | 03 · Bridge between two totals (paid-to-date → developed ultimate, by accident year) |
| Core method | Chain-ladder development on the cumulative paid triangle as known at the evaluation date (volume-weighted age-to-age factors), ultimate loss ratios by accident year |
| Analytical stump | Immature accident years have paid only part of their eventual losses; comparing paid-to-date loss ratios across maturities makes recent years look profitable. The dataset also contains later diagonals — using them is look-ahead |
| Primary sources | Casualty Actuarial Society Loss Reserving Database (NAIC Schedule P, 1988–1997) |

## 1. The real-world situation

A workers' compensation insurer's pricing committee meets after year-end 1997. The decision rule: **file a rate increase if
the 1996–1997 accident-year loss ratio exceeds the 1990–1992 average by more than 5 points.** The analyst compared paid
loss ratios for each accident year and found 1996–1997 far better than 1990–1992. The reserving actuary asked how much of
1997's losses had actually been paid after twelve months.

## 2. The decision (one deterministic recommendation)

**File the rate increase or not, with the 1996–1997 and 1990–1992 developed loss ratios.**

Rules (committee memo):

* Company: the group code in the folder; line: workers' compensation (`wkcomp_pos.csv`); net basis
  (`CumPaidLoss_D`, `EarnedPremNet_D`).
* Information: only cells with `AccidentYear + DevelopmentLag − 1 ≤ 1997` (the triangle as known at 12/31/1997).
* Development: volume-weighted age-to-age factors from all available pairs at each lag; tail factor 1.000 beyond lag 10.
* Ultimate(AY) = latest paid × product of remaining factors; loss ratio = ultimate ÷ net earned premium.
* Compare the premium-weighted loss ratio of 1996–1997 with that of 1990–1992; file if the difference > 5.0 points.

## 3. Why capable analysts get it wrong

* Loss ratios on paid losses are readily computed from one table and look like like-for-like comparisons.
* Long-tail lines pay slowly; a 12-month-old accident year may have paid a fraction of its ultimate.
* The CAS file includes the full 10×10 square (later diagonals) for research; filtering to what was known in 1997 is easy to
  forget, and the "future" data change the answer.
* Factor-to-maturity alignment errors (applying lag-1 factors to lag-2 losses) are common in spreadsheets.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `wkcomp_pos.csv` | CSV | ~13k | CAS Loss Reserving Database | CAS research data (free download; verify terms) | Workers' comp triangles (all companies) |
| 2 | `ppauto_pos.csv` | CSV | ~15k | CAS | Same | Context / alternative line |
| 3 | `othliab_pos.csv` | CSV | ~11k | CAS | Same | Context |
| 4 | `comauto_pos.csv`, `medmal_pos.csv`, `prodliab_pos.csv` | CSV | ~7–15k each | CAS | Same | Context |
| 5 | `cas_loss_reserving_database_readme.pdf` | PDF | — | CAS | Same | Field definitions |
| 6 | `friedland_estimating_unpaid_claims_ch7.pdf` (citation) | PDF | — | CAS monograph (Friedland 2010; cite) | Cite | Chain-ladder method |
| 7 | `company_selection.json` | JSON | 1 | Task author | — | Group code |
| 8 | `committee_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `analyst_paid_ratio_table.xlsx` | XLSX | ~10 | Task author | — | Undeveloped comparison |
| 10 | `naic_schedule_p_instructions_extract.pdf` | PDF | — | NAIC (public excerpt) | Cite | Context |

## 5. Deterministic solution path

1. Filter company, line, and the upper triangle (calendar ≤ 1997).
2. Build the cumulative paid triangle; compute volume-weighted factors for lags 1→2 … 9→10.
3. Develop each accident year to ultimate; compute loss ratios.
4. Premium-weighted averages for the two groups; apply the rule.
5. Validation only: compare 1997 chain-ladder ultimates with the later diagonals in the file (not used for the decision).

## 6. Wrong paths (method errors, not misreadings)

**A — paid-to-date loss ratios.** Recent years look much better; no filing.

**B — using the lower triangle.** Decision uses information unavailable in 1997.

**C — simple-average loss ratios across years.** Not premium-weighted; group comparison shifts.

**D — factor misalignment.** Ultimates for recent years off by a whole development step.

## 7. Why the stump is analytical, not semantic

Every column and rule is specified. The mistakes are comparing quantities at different maturities and using information
from the future — methodological errors in time-dependent estimation.

## 8. Draft task prompt (prose)

> The pricing committee needs a yes or no on filing a workers' compensation rate increase, using the rule in the committee
> memo and only what we knew at the end of 1997. Develop the paid triangle for our company in the CAS file, compare the
> 1996–1997 and 1990–1992 loss ratios and give me the call. Deliver `development_bridge.xlsx` with the triangle, the
> age-to-age factors, and for each accident year paid-to-date, development to ultimate, ultimate loss and loss ratio, and
> `accident_year_loss_ratios.png` comparing paid-to-date and developed loss ratios by accident year with the two comparison
> groups shaded. On the first sheet, state the decision, both group loss ratios, and the decision an undeveloped
> comparison would have produced.

## 9. Deliverables

* `development_bridge.xlsx`, `accident_year_loss_ratios.png`.

## 10. Where 25+ rubric criteria come from

* 9 factors, 10 ultimates (or loss ratios), 2 group averages, decision, undeveloped contrast, validation comment.

## 11. Golden-output checklist

* Upper triangle only; volume-weighted factors; correct alignment; premium-weighted groups; decision stated.

## 12. Build notes (scope tuning)

* Pick a group code with a complete triangle and a developed 1996–1997 deterioration > 5 points while paid-to-date shows
  improvement; verify with both computations before freezing.
* Confirm the CAS column suffixes for the line (e.g. `_D` for workers' comp) in the readme.
