# OS43 — Savings from switching to biosimilars: the incumbent cuts its price, so the gap you sized shrinks

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Vendor-switching savings when incumbents respond (cloud contract renegotiations, telecom carrier switching, procurement of generics) |
| Domain | Pharmaceutical pricing / payers |
| Task shape | 02 · Forecast across many periods (quarterly savings over 8 quarters from a biosimilar-first policy for one biologic; the policy's two-year savings booked in the budget) |
| Core method | Quarterly Average Sales Price (ASP) payment limits for the reference product and biosimilars; model the reference product's ASP trajectory after biosimilar entry from past molecules' post-entry ASP declines (event-time median), units from Part B spending files; savings = switched units × (reference ASP_t − biosimilar ASP_t) plus the incumbent price drop on non-switched units if the payer benefits per memo |
| Analytical stump | Freezing today's price gap between reference and biosimilar ignores that reference ASPs fall after entry (and biosimilar ASPs fall faster). Projected switching savings based on the pre-entry gap overstate; ignoring the incumbent's price drop on remaining units misattributes savings. Event-time comparables from earlier molecules give the trajectory |
| Primary sources | CMS Medicare Part B ASP pricing files (quarterly); CMS Medicare Part B Spending by Drug |

## 1. The real-world situation

A Medicare Advantage plan's pharmacy team proposes a biosimilar-first policy for a biologic that recently gained biosimilar competition. The
proposal sized savings as current units × 60% switching × today's ASP gap and booked it for two years. Finance asked for a forecast that
reflects how prices move after biosimilar entry.

## 2. The decision (one deterministic recommendation)

**The two-year savings booked (sum of 8 quarterly savings), with quarterly components (switching savings and incumbent price savings).**

Rules (pharmacy memo):

* Prices: ASP payment limits by HCPCS by quarter (latest 3 years and comparator molecules' post-entry histories).
* Comparators: molecules in `comparator_molecules.json` (e.g., earlier biologics with biosimilar entry); event time q = quarters since first
  biosimilar ASP listing.
* Trajectory: median across comparators of reference ASP_q ÷ ASP_0 and biosimilar ASP_q ÷ reference ASP_0.
* Plan units: the plan's quarterly units (memo) for the reference product.
* Switching: 60% of units switch linearly over the first 4 quarters (memo ramp), then constant.
* Savings_t = switched_t × (reference ASP_t − biosimilar ASP_t) + non-switched_t × (reference ASP_0 − reference ASP_t) × 1.06 (ASP + 6%
  payment convention per memo).
* Report the frozen-gap estimate for contrast.

## 3. Why capable analysts get it wrong

* Current prices are known; future prices are not, so analysts freeze them.
* Incumbents respond with discounts that flow into ASP with a lag.
* Event-time alignment of comparators is required.
* Savings on non-switched units are often omitted or double counted.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–12 | `<quarter>-asp-pricing-file.xlsx` (12 quarters) | XLSX | ~900 HCPCS each | CMS ASP pricing files | U.S. Gov public domain | Payment limits |
| 13–24 | historical ASP files for comparator post-entry periods | XLSX | ~900 each | CMS | Public domain | Comparator trajectories |
| 25 | `DSD_PTB_RY<yy>_P06_V10_DYT<yy>_HCPCS.csv` | CSV | ~800 | CMS Part B Spending by Drug | Public domain | Units and spending (context) |
| 26 | `comparator_molecules.json` | JSON | ~5 | Task author | — | Comparators and HCPCS codes |
| 27 | `plan_units.json` | JSON | — | Task author | — | Plan volumes |
| 28 | `pharmacy_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 29 | `proposal_frozen_gap.xlsx` | XLSX | — | Task author | — | Naive sizing |
| 30 | `asp_methodology_citation.pdf` | PDF | — | CMS (cite) | Public domain | ASP lag and +6% |

## 5. Deterministic solution path

1. Extract comparator ASP histories; event-time ratios; medians.
2. Apply trajectories to the target molecule from its entry quarter.
3. Switching ramp; quarterly savings components; two-year total.
4. Contrast with the frozen-gap estimate.

## 6. Wrong paths (method errors, not misreadings)

**A — frozen price gap.** Overstated switching savings.

**B — ignoring incumbent price drops.** Misattributes total savings.

**C — calendar-time alignment of comparators.** Mixed maturities.

**D — omitting +6% convention.** Payment misstated.

## 7. Why the stump is analytical, not semantic

Data and formulas are specified. The trap is assuming static competitor prices in switching savings.

## 8. Draft task prompt (prose)

> How much should we book for the biosimilar-first policy over two years? Forecast prices after entry from comparator molecules as the pharmacy memo
> specifies. Provide `quarterly_savings.csv` (quarter: prices, switched units, savings components), `post_entry_price_paths.png`, and a one-page
> `budget_booking.pdf`.

## 9. Deliverables

* `quarterly_savings.csv`, `post_entry_price_paths.png`, `budget_booking.pdf`.

## 10. Where 25+ rubric criteria come from

* 8 quarters × (switching, incumbent) = 16; trajectories at 8 event quarters; total; contrast.

## 11. Golden-output checklist

* Comparator selection; event time; medians; ramp; formulas; total.

## 12. Build notes (scope tuning)

* Confirm the frozen-gap estimate exceeds the forecast total by ≥ 30%.
