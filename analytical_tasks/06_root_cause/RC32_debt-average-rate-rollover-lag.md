# RC32 — Auction yields peaked a year ago, so why is the government's average borrowing rate still climbing?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Stock metrics that lag flow metrics (recognised revenue vs bookings, ARR vs new-contract pricing, a bank's book yield vs new-lending rates, installed-base ASP vs new-sale prices) |
| Domain | Public finance / fixed-income treasury management |
| Task shape | 17 · Periods around a change point (new-issue yields peak at month M; the average rate on marketable debt keeps rising after M; the post-peak rise explained by rollover, bill repricing and composition) |
| Core method | Security-level reconstruction of the outstanding marketable stock from the monthly public-debt statement; each security carries its issue yield (from auction results); average rate = Σ outstanding × yield ÷ Σ outstanding; decompose the 12-month change after M into bill repricing (bills rolled at new rates), coupon-security rollover (maturing notes and bonds replaced at new yields), composition (bill share), and inflation-indexed accruals; compare with the published average interest rate |
| Analytical stump | Comparing the average rate with current auction yields suggests something is wrong or that "rates are still rising". The average rate is a stock measure: bills reprice within months, but notes and bonds issued at 2020–2021 yields mature over years, so the average keeps rising after new-issue yields peak until the low-coupon stock has rolled. Ignoring the maturity profile, or modelling the average as a simple moving average of auction yields, mis-times and mis-sizes the rise |
| Primary sources | U.S. Treasury Fiscal Data — Monthly Statement of the Public Debt (MSPD) detail by security, Average Interest Rates on U.S. Treasury Securities; TreasuryDirect auction results |

## 1. The real-world situation

A budget office's briefing noted that 10-year and bill auction yields had peaked twelve months earlier, yet the average interest rate on marketable
debt had risen another 40 basis points since. Legislators asked whether the rise reflected new borrowing at high rates, a shift toward bills, or
something else, and when it would stop. The analysts must attribute the post-peak rise.

## 2. The decision (one deterministic recommendation)

**The dominant source of the post-peak rise in the average rate (bill repricing, coupon rollover, composition, or inflation-indexed accrual) by
contribution in basis points, with the reconciliation to the published average rate.**

Rules (budget-office memo):

* Data: MSPD detail (marketable securities outstanding by CUSIP, month-end) for months M − 12 to M + 12; auction results (high yield, issue date,
  CUSIP) for all marketable securities outstanding in that window (reopenings carry the yield of each reopening, weighted by amount).
* Security yield: amount-weighted high yield across the security's auctions; TIPS use the real yield plus the memo's inflation accrual rule;
  floating-rate notes use the latest 13-week bill high rate plus spread.
* Average rate in month t = Σ_s outstanding_s,t × yield_s ÷ Σ_s outstanding_s,t, by class (bills, notes, bonds, TIPS, FRNs) and total.
* Reconciliation: compare with the published Average Interest Rates by class; differences > 10 bp must be explained in the notes.
* Decomposition of the change from M to M + 12 (sequential, in this order, per memo):
  * Composition: class shares at M + 12 with class average rates at M.
  * Bill repricing: bills' rate change × bill share at M + 12.
  * Coupon rollover: notes and bonds rate change × their share at M + 12.
  * TIPS and FRN accrual: their rate change × their share at M + 12.
* Dominant source = largest contribution.

## 3. Why capable analysts get it wrong

* New-issue yields are the headline rate; the average looks out of step.
* The maturity profile determines how fast the stock reprices; it is invisible in aggregate series.
* Bills reprice quickly and dominate the early response; coupons dominate later.
* Reopenings and indexed securities need explicit rules.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `mspd_table_3_market_<months>.csv` | CSV | ~25k (security × month) | Treasury Fiscal Data API (MSPD detail of marketable securities) | U.S. Government work (public domain) | Outstanding by security |
| 2 | `auctions_query_<years>.csv` | CSV | ~6k auctions | TreasuryDirect / Fiscal Data auction results | Public domain | Issue yields by CUSIP |
| 3 | `avg_interest_rates_<years>.csv` | CSV | ~3k | Fiscal Data: Average Interest Rates on U.S. Treasury Securities | Public domain | Published averages |
| 4 | `daily_treasury_bill_rates.csv` | CSV | ~800 | Treasury daily bill rates | Public domain | FRN index rates |
| 5 | `budget_office_memo.pdf` | PDF | — | Task author | — | Rules in §2, month M |
| 6 | `briefing_note.xlsx` | XLSX | — | Task author | — | The "rates still rising" briefing |

## 5. Deterministic solution path

1. Join outstanding securities to auction yields by CUSIP; handle reopenings, TIPS and FRNs.
2. Compute class and total average rates by month; reconcile with published averages.
3. Decompose the M → M + 12 change; dominant source.
4. Show the maturity profile of low-yield notes still outstanding at M + 12 and the implied remaining rollover; contrast with the briefing.

## 6. Wrong paths (method errors, not misreadings)

**A — compare with current auction yields only.** Misreads a stock lag as new borrowing costs.

**B — moving average of auction yields.** Ignores the actual maturity profile and issuance mix.

**C — coupon rate instead of issue yield.** Mis-states securities issued at discounts or premiums and all reopenings.

**D — unweighted security averages.** Small, old securities distort the average.

## 7. Why the stump is analytical, not semantic

Securities are matched by CUSIP; all formulas are specified. The trap is reading a stock measure as a flow measure.

## 8. Draft task prompt (prose)

> Legislators ask why the average rate on our debt is still rising a year after auction yields peaked. Rebuild the average from the security-level
> data and decompose the post-peak rise as the budget-office memo specifies. Provide `average_rate_decomposition.csv` (component: bp),
> `rollover_profile.png`, and a one-page `debt_cost_rca.pdf`.

## 9. Deliverables

* `average_rate_decomposition.csv` — composition, bill repricing, coupon rollover, TIPS/FRN components; reconciliation table.
* `rollover_profile.png` — outstanding low-yield coupon stock by maturity year, with the average-rate path.
* `debt_cost_rca.pdf` — dominant source and why the briefing misreads the stock.

## 10. Where 25+ rubric criteria come from

* CUSIP matching coverage and reopenings handled: 3.
* Class average rates at M and M + 12 (5 classes): 10.
* Reconciliation differences: 2.
* Four components and closure: 5.
* Dominant source: 1.
* Maturity profile and contrast: 4.

## 11. Golden-output checklist

* Amount-weighted yields across reopenings; TIPS and FRN rules.
* Month-end outstanding weights.
* Sequential decomposition in memo order; closure.

## 12. Build notes (scope tuning)

* Choose M as the month of peak bill and note auction yields (e.g., late 2023); confirm that coupon rollover dominates the following 12 months while
  the briefing attributes the rise to new borrowing.
