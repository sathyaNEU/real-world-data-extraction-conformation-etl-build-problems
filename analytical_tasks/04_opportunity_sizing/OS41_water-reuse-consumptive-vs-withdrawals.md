# OS41 — Water reuse market: withdrawals are not consumption, and return flows are already reused downstream

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Gross versus net flow sizing (gross merchandise value versus net revenue, traffic versus unique demand, gross versus net emissions) |
| Domain | Water resources / industrial services |
| Task shape | 03 · Bridge between two totals (thermoelectric and industrial withdrawals in a basin → net reusable volume after consumptive use and existing return-flow reuse; the basins where a reuse-services firm opens offices) |
| Core method | County water-use estimates by category (withdrawals, consumptive use where estimated); reuse opportunity = consumptive-use reduction potential (memo factor) rather than withdrawals; subtract return flows already appropriated downstream (memo's basin factor); aggregate by basin |
| Analytical stump | Sizing reuse by total withdrawals counts once-through cooling water that is returned to the river almost entirely; the opportunity is in consumptive use and in withdrawals that are not already reused downstream. Basin rankings by withdrawals favour power-plant-heavy basins with little net opportunity |
| Primary sources | USGS "Estimated Use of Water in the United States" county-level data (2015); USGS water-use data dictionary |

## 1. The real-world situation

A water-reuse services firm will open offices in **3** river basins with the largest addressable industrial reuse volume. The deck ranked basins by
thermoelectric plus industrial withdrawals. A hydrologist pointed out that most thermoelectric withdrawals are returned and that downstream users
already rely on return flows.

## 2. The decision (one deterministic recommendation)

**The 3 basins selected (largest net reusable volume, Mgal/d), with the bridge from withdrawals for each.**

Rules (strategy memo):

* Data: USGS 2015 county water use (thermoelectric and industrial self-supplied withdrawals, freshwater and saline; consumptive use where
  reported; otherwise the memo's category coefficients).
* County → basin (HUC4) assignment by county centroid (memo).
* Reusable volume per county = consumptive use × reuse potential factor (0.4 industrial, 0.25 thermoelectric recirculating, 0 once-through).
* Return-flow appropriation: basin factor from `basin_appropriation.csv` (share of return flows already allocated downstream); net reusable =
  reusable × (1 − factor) per memo for withdrawal-based components.
* Bridge per basin: withdrawals → minus returned flows (withdrawals − consumptive) → × reuse potential → minus appropriated → net.
* Choose top 3 basins by net reusable.

## 3. Why capable analysts get it wrong

* Withdrawals are the headline USGS figure.
* Once-through cooling withdraws vast volumes and consumes little.
* Downstream rights depend on return flows; "new" reuse may not be new water.
* County-to-basin assignment needs a consistent rule.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `usco2015v2.0.csv` | CSV | ~3.2k counties × ~140 columns | USGS ScienceBase | U.S. Gov public domain | County water use |
| 2 | `usco2015_data_dictionary.xlsx` | XLSX | — | USGS | Public domain | Column definitions |
| 3 | `usgs_circular_1441.pdf` | PDF | — | USGS Circular 1441 | Public domain | Methods |
| 4 | `county_to_huc4.csv` | CSV | ~3.2k | Task author (centroid overlay) | Public-domain sources | Assignment |
| 5 | `basin_appropriation.csv` | CSV | ~200 | Task author (from state water-rights summaries; cite) | Public | Downstream factors |
| 6 | `consumptive_coefficients.json` | JSON | — | Task author (from USGS published coefficients) | Public domain | Fallback coefficients |
| 7 | `strategy_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `deck_withdrawal_ranking.xlsx` | XLSX | ~200 | Task author | — | Naive ranking |

## 5. Deterministic solution path

1. Load county data; compute consumptive use with fallbacks; assign basins.
2. Reusable and net reusable per county; basin totals.
3. Bridge; top 3; contrast with withdrawal ranking.

## 6. Wrong paths (method errors, not misreadings)

**A — withdrawals ranking.** Once-through cooling dominates.

**B — consumptive use without reuse potential factors.** Overstated.

**C — ignoring downstream appropriation.** Overstated in arid basins.

**D — saline withdrawals included as freshwater reuse.** Not the memo's scope (report separately).

## 7. Why the stump is analytical, not semantic

The factors and bridge are specified. The trap is gross versus net flow in resource sizing.

## 8. Draft task prompt (prose)

> Which three basins should get our reuse offices? Size net reusable industrial and thermoelectric volume from USGS county data as the strategy
> memo specifies. Provide `basin_reuse.csv` (basin: withdrawals, consumptive, reusable, net, rank), `basin_bridge.png`, and a one-page
> `office_locations.pdf`.

## 9. Deliverables

* `basin_reuse.csv`, `basin_bridge.png`, `office_locations.pdf`.

## 10. Where 25+ rubric criteria come from

* Top-3 basins; values for 8 basins × 3; bridges for 3 basins; contrast.

## 11. Golden-output checklist

* Columns; fallbacks; basin assignment; factors; bridge; ranking.

## 12. Build notes (scope tuning)

* Confirm at least two withdrawal top-3 basins drop out.
