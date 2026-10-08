# FC41 — Safety stock when shipments arrive late: demand variance over lead time must include lead-time variance

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Global component and finished-goods supply chains with volatile ocean/air lead times (electronics, pharma, humanitarian supply) |
| Domain | Supply chain planning / health commodities |
| Task shape | 04 · Setting one dial (safety stock for one product at one country warehouse) |
| Core method | Lead-time demand variance σ²_LTD = E[L]·σ²_D + E[D]²·σ²_L from monthly demand and observed order-to-delivery lead times for the planned shipment mode; z-score for the cycle service level |
| Analytical stump | The textbook z·σ_D·√L formula assumes a fixed lead time. When lead times vary by months, the second term dominates; ignoring it (or pooling air and ocean lead times) badly under- or over-states safety stock |
| Primary sources | USAID Supply Chain Shipment Pricing Data (PEPFAR/GHSC commodity shipments) |

## 1. The real-world situation

A national HIV programme's warehouse holds antiretroviral stock replenished by international shipments. Planning set safety stock
with the standard formula using average monthly demand variability and the average lead time. Stock-outs followed late shipments,
not demand spikes. The supply-chain adviser asked whether lead-time variability was in the calculation at all.

## 2. The decision (one deterministic recommendation)

**Safety stock (units) for the product and country in the folder, at a 95% cycle service level.**

Rules (supply planning memo):

* Demand proxy: monthly line-item quantity delivered to the country for the product (molecule/test type and dosage in the memo),
  by delivered-to-client month, over the 36 months before the planning date; months without deliveries count as zero.
* Lead time: days from "PO sent to vendor" to "delivered to client" for the product's shipments to that country with the planned
  mode (ocean); shipments with missing dates excluded; converted to months (÷ 30.44).
* σ_D, E[D]: sample SD and mean of monthly demand; E[L], σ_L: mean and sample SD of lead times (months).
* Safety stock = 1.645 × √(E[L]·σ²_D + E[D]²·σ²_L), rounded up to whole packs (pack size in the memo).

## 3. Why capable analysts get it wrong

* The fixed-lead-time formula is the one most planners learned.
* Lead-time variance is not visible in demand data; it lives in shipment timestamps.
* Pooling air and ocean shipments mixes two distributions; the plan uses one mode.
* Monthly zeros must be included; dropping them shrinks σ_D and inflates E[D].

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Supply_Chain_Shipment_Pricing_Data.csv` | CSV | ~10.3k | USAID (data.usaid.gov / catalog.data.gov) | U.S. Gov public domain | Shipments with dates, quantities, modes |
| 2 | `Supply_Chain_Shipment_Pricing_Data.json` | JSON | ~10.3k | Same (API export) | Public domain | Same data |
| 3 | `shipment_pricing_data_dictionary.pdf` | PDF | — | USAID | Public domain | Field definitions |
| 4 | `monthly_demand_country_product.csv` | CSV | ~3k | Derived | Public domain | Demand proxy series |
| 5 | `lead_times_by_mode.csv` | CSV | ~8k | Derived | Public domain | Lead-time observations |
| 6 | `who_arv_pack_sizes.xlsx` | XLSX | ~200 | Public product references | Public | Pack sizes |
| 7 | `silver_pyke_peterson_safety_stock_citation.pdf` | PDF | — | Inventory management text (cite) | Cite | Formula |
| 8 | `supply_planning_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `current_safety_stock_calc.xlsx` | XLSX | ~10 | Task author | — | Fixed-lead-time calculation |
| 10 | `country_product_scope.json` | JSON | — | Task author | — | Product, country, planning date |

## 5. Deterministic solution path

1. Filter the product and country; build 36 monthly demand values (with zeros).
2. Compute ocean lead times; mean and SD in months.
3. Apply the formula; round to packs.
4. Show each term's contribution; contrast with the fixed-lead-time and pooled-mode versions.

## 6. Wrong paths (method errors, not misreadings)

**A — z·σ_D·√L.** Safety stock far too low when lead times vary.

**B — pooled air + ocean lead times.** Wrong E[L] and σ_L.

**C — zeros dropped.** Demand variability misstated.

**D — scheduled instead of actual delivery dates.** Hides lateness.

## 7. Why the stump is analytical, not semantic

Every quantity is defined; the trap is the variance of a random sum (random number of demand periods) — a probabilistic modelling
choice.

## 8. Draft task prompt (prose)

> Set safety stock for the product in the folder at the country warehouse at a 95% cycle service level, following the supply planning
> memo — with lead times measured from the shipment records for ocean freight. Provide `safety_stock_calc.csv` (demand mean/SD, lead-time
> mean/SD, each variance term, safety stock in units and packs), `leadtime_distribution.png` (ocean vs air lead times), and a one-page
> `safety_stock_memo.pdf` comparing with the current calculation.

## 9. Deliverables

* `safety_stock_calc.csv`, `leadtime_distribution.png`, `safety_stock_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 36 monthly demands (spot-check 10); E[D], σ_D; E[L], σ_L; two variance terms; safety stock; packs; two contrasts.

## 11. Golden-output checklist

* Correct filters; zeros included; actual lead times by mode; full formula; rounding.

## 12. Build notes (scope tuning)

* Choose a product–country pair with ≥ 25 ocean shipments and lead-time SD ≥ 1.5 months; confirm the full formula at least doubles
  safety stock.
* Record the dataset version; the file is periodically updated.
