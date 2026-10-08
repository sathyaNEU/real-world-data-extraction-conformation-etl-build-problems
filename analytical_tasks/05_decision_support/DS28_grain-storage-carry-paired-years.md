# DS28 — Store the harvest or sell it? Compare each year's own spring price with its own harvest price, net of carrying costs

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Inventory timing decisions (buy-ahead, hold-or-sell, stockpiling) where seasonal price patterns must be netted against carrying costs and judged year by year |
| Domain | Agriculture / commodity marketing |
| Task shape | 13 · Scenarios and the flip point (storage cost × interest rate scenarios → expected net gain from storing to May; the storage decision and the storage cost at which it flips) |
| Core method | For each crop year, cash bid at a local elevator at harvest (first week of October) and in May; return to storage = May price − harvest price − storage cost (per bushel-month) − interest on harvest value; distribution across years (mean, share of years positive); decision rule from the memo; contrast with comparing average May and average harvest prices across all years |
| Analytical stump | Comparing multi-year averages of spring and harvest prices ignores that the spread varies by year and mixes years with different price levels; omitting interest and shrink makes storage look better. The decision depends on the paired per-year returns net of carrying costs |
| Primary sources | USDA AMS Market News daily grain bids (local cash prices by location) |

## 1. The real-world situation

A farmer with on-farm bins asks whether to store corn after harvest and sell in May. A marketing newsletter showed that average May prices exceeded
average October prices by 40 cents over 15 years. The farm's lender asked for a year-by-year analysis net of storage and interest.

## 2. The decision (one deterministic recommendation)

**Store or sell at harvest under the central cost scenario (decision: store if mean net return ≥ $0.05/bu and positive in ≥ 60% of years), and the
storage cost per bushel-month at which the decision flips.**

Rules (marketing memo):

* Data: AMS daily cash corn bids for the elevator/location in memo, crop years 2008–2023.
* Harvest price: mean bid in the first full week of October; May price: mean bid in the first full week of May (next calendar year).
* Costs: on-farm storage $0.02/bu-month (central), shrink 1% of value, interest at the prime rate + 1% on harvest value for 7 months (rate by year
  from `interest_rates.csv`).
* Net return_y = May − harvest − 7 × storage − shrink − interest.
* Decision rule above; flip point on storage cost.
* Contrast: average May − average October across years without costs.

## 3. Why capable analysts get it wrong

* Averages of seasonal prices look like a typical spread.
* Price levels change across years; spreads must be paired within years.
* Carrying costs (interest especially in high-rate years) can erase the spread.
* Consistency of positive returns matters to a lender.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `ams_grain_bids_<location>_2008_2024.csv` | CSV | ~4k trading days | USDA AMS Market News (MARS API/reports) | U.S. Gov public domain | Daily cash bids |
| 2 | `ams_report_descriptions.pdf` | PDF | — | USDA AMS | Public domain | Report definitions |
| 3 | `interest_rates.csv` | CSV | ~16 | Federal Reserve H.15 prime rate (public) | Public domain | Interest |
| 4 | `marketing_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `newsletter_average_spread.xlsx` | XLSX | — | Task author | — | Naive analysis |
| 6 | `storage_cost_scenarios.json` | JSON | — | Task author | — | Scenarios |

## 5. Deterministic solution path

1. Extract harvest and May prices per crop year.
2. Net returns per year with costs; distribution; decision.
3. Flip point; contrast with the newsletter spread.

## 6. Wrong paths (method errors, not misreadings)

**A — average spread across years.** Ignores pairing and costs.

**B — ignoring interest.** Overstates returns.

**C — using futures instead of local cash bids.** Basis ignored.

**D — monthly averages instead of the memo's weeks.** Different prices.

## 7. Why the stump is analytical, not semantic

Prices, windows and costs are specified. The trap is unpaired averages and missing carrying costs.

## 8. Draft task prompt (prose)

> Should the farm store corn to May this year? Compute paired per-year storage returns net of costs from AMS cash bids as the marketing memo specifies.
> Provide `storage_returns.csv` (crop year: harvest, May, costs, net), `returns_by_year.png`, and a one-page `storage_decision.pdf` with the flip point.

## 9. Deliverables

* `storage_returns.csv`, `returns_by_year.png`, `storage_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 16 yearly net returns; mean; positive share; decision; flip point; newsletter contrast.

## 11. Golden-output checklist

* Week windows; pairing; costs; decision rule; flip point.

## 12. Build notes (scope tuning)

* Choose a location where the naive average spread is positive but the paired net mean is below the threshold.
