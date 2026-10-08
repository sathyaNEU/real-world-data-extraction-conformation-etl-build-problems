# DS43 — Sell the flat now or in five years? Prices fall faster as the lease runs down

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Asset disposal timing with nonlinear depreciation (vehicles, equipment, licences, software contracts nearing renewal) |
| Domain | Real estate / household finance |
| Task shape | 13 · Scenarios and the flip point (hold period × market growth scenarios → net proceeds in present value; sell now or hold, and the market growth at which holding wins) |
| Core method | Hedonic regression of log resale price on remaining lease (piecewise or spline), flat type, floor area, storey band, town and month fixed effects; implied lease-decay curve; projected value after h years = current value × market growth^h × exp(f(lease − h) − f(lease)); compare PV of selling now versus after holding (with rental income and costs per memo) |
| Analytical stump | Assuming a constant annual depreciation (straight-line over 99 years) or using town-level average price growth ignores that value loss accelerates as remaining lease falls below ~60 years. For an older flat, holding five years can lose more to lease decay than the market gains |
| Primary sources | Singapore HDB resale flat prices (data.gov.sg) |

## 1. The real-world situation

A household owns a 4-room HDB flat with 52 years of lease remaining and must decide whether to sell now or rent it out for five years and sell
later. A property agent projected the future price using the town's average annual price growth since 2017.

## 2. The decision (one deterministic recommendation)

**Sell now or hold 5 years under the central market-growth scenario, the PV difference, and the market growth rate at which holding breaks even.**

Rules (household memo):

* Data: HDB resale transactions 2017–2024 (registration date, town, flat type, floor area, storey range, lease commencement, remaining lease).
* Model: log(price) = month FE + town FE + flat type + log(floor area) + storey band + spline(remaining lease in years; knots at 50, 60, 70, 80, 90)
  on 4-room flats.
* Current value: predicted price for the household's flat (profile in memo) at the latest month.
* Projection: value_h = current × g^h × exp(f(52 − h) − f(52)), g scenarios 1.00/1.02/1.04.
* Holding cash flows: net rent per memo for 5 years; PV at 4%; selling costs 2% at sale.
* Decision: hold if PV(hold) > PV(sell now); flip growth rate g*.
* Contrast: agent's projection = current × (1 + town average growth)^5 with no lease effect.

## 3. Why capable analysts get it wrong

* Average price growth is easy to compute and quote.
* Lease decay is nonlinear and invisible in aggregate growth (newer flats enter the sample).
* Hedonic models separate market movement from flat attributes.
* Rental income and discounting matter for holding decisions.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv` | CSV | ~200k | data.gov.sg (HDB) | Singapore Open Data Licence | Transactions |
| 2 | `hdb_resale_data_dictionary.pdf` | PDF | — | data.gov.sg | SODL | Fields |
| 3 | `household_profile.json` | JSON | — | Task author | — | The flat |
| 4 | `household_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `agent_projection.xlsx` | XLSX | — | Task author | — | Naive projection |
| 6 | `rent_assumptions.json` | JSON | — | Task author (from public HDB rental statistics; cite) | — | Rent |
| 7 | `lease_decay_reference.pdf` | PDF | — | Cite (leasehold decay studies) | Cite | Context |

## 5. Deterministic solution path

1. Filter 4-room flats; prepare variables; fit the hedonic model.
2. Lease curve; current value; projections by scenario.
3. PVs; decision; flip growth.
4. Contrast with agent's projection.

## 6. Wrong paths (method errors, not misreadings)

**A — town average growth.** Ignores lease decay.

**B — straight-line lease depreciation.** Misses acceleration.

**C — no month fixed effects.** Confounds market and lease.

**D — ignoring rent and discounting.** Wrong comparison.

## 7. Why the stump is analytical, not semantic

The model and cash-flow rules are specified. The trap is projecting with aggregate trends instead of asset-specific depreciation.

## 8. Draft task prompt (prose)

> Should the household sell now or rent out and sell in five years? Estimate the lease-decay curve from HDB resale data and compare scenarios as the
> household memo specifies. Provide `hold_vs_sell.csv` (scenario: PV sell now, PV hold, difference), `lease_decay_curve.png`, and a one-page
> `sell_or_hold.pdf` with the break-even growth.

## 9. Deliverables

* `hold_vs_sell.csv`, `lease_decay_curve.png`, `sell_or_hold.pdf`.

## 10. Where 25+ rubric criteria come from

* Coefficients (spline values at 6 lease years); current value; 3 scenarios × 2 PVs; flip growth; agent contrast.

## 11. Golden-output checklist

* Filters; spline; fixed effects; projection formula; PVs; flip point.

## 12. Build notes (scope tuning)

* Confirm the agent's projection favours holding while the hedonic projection favours selling under the central scenario.
