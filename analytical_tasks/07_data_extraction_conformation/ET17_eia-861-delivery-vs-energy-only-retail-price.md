# ET17 — All-in retail electricity price in restructured states: one kWh, two bills, counted once

| Field | Value |
|---|---|
| Domain | Energy procurement / retail electricity / corporate sustainability |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 07 · Grid of cells (state × customer sector average price) |
| Core technique | Service-type-aware aggregation (bundled, energy-only, delivery-only) so quantities are counted once and revenues from both legs are included; inclusion of imputed/short-form records |
| Trap family (honest data) | Sales double counted across energy-only and delivery-only rows; delivery revenue omitted; adjustment rows dropped |
| Primary sources | EIA-861 annual (Sales to Ultimate Customers, Short Form), EIA State Electricity Profiles |

## 1. The real-world project

A national retailer with stores in eight restructured states plans one **on-site solar pilot** where it saves the most
per kWh, using EIA's 2023 state average commercial price as the benchmark. The procurement analyst summed revenue and
sales over all rows of the EIA-861 "Sales to Ultimate Customers" file per state. In states where most commercial load buys
energy from competitive suppliers, the computed price came out near half the price on the retailer's actual invoices.

## 2. The business decision (one deterministic recommendation)

**Which of the eight states has the highest all-in 2023 commercial average price (and therefore gets the pilot)?**

Rules (procurement benchmark method):

* Use EIA-861 2023 final data. Quantities (MWh sales and customers) are counted **once**: bundled + energy-only rows.
  Delivery-only rows contribute **revenue only** (their sales and customers duplicate the energy-only quantities).
* Revenue = bundled revenue + energy-only revenue + delivery-only revenue (thousand dollars).
* Include EIA adjustment rows and short-form (EIA-861S) utilities as EIA does in its state totals.
* Average price (¢/kWh) = revenue × 1,000 × 100 ÷ (sales MWh × 1,000).
* Compute the full grid (8 states × residential, commercial, industrial) and reconcile each cell to EIA's published state
  table (tolerance ±0.05 ¢/kWh); pick the highest commercial cell.

## 3. Why this gets overlooked in real projects

* The file is one long table; rows for the same customers appear under the distribution utility (delivery-only) and under
  their retail supplier (energy-only). A plain `groupby(state).sum()` doubles kWh in high-choice states.
* The opposite shortcut — bundled rows only — ignores most commercial load in states like Pennsylvania, Ohio, Illinois,
  Maryland, Massachusetts, New York or Texas.
* Delivery-only revenue is large (wires charges); dropping it understates the all-in price.
* Adjustment and short-form records lack familiar utility names and get filtered as "junk".

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `Sales_Ult_Cust_2023.xlsx` | XLSX | ~3.5k rows × service types | EIA-861 | U.S. Gov public domain | Revenue, sales, customers by service type |
| 2 | `Sales_Ult_Cust_CS_2023.xlsx` (customer-sited) | XLSX | ~3k | EIA-861 | Public domain | Context |
| 3 | `Short_Form_2023.xlsx` | XLSX | ~1k | EIA-861S | Public domain | Small utilities |
| 4 | `Utility_Data_2023.xlsx` | XLSX | ~3.3k | EIA-861 | Public domain | Utility attributes, ownership |
| 5 | `Service_Territory_2023.xlsx` | XLSX | ~10k | EIA-861 | Public domain | Utility–county coverage |
| 6 | `eia861_file_layout_2023.pdf` | PDF | — | EIA | Public domain | Part/service-type definitions |
| 7 | `eia861_technical_notes.pdf` | PDF | — | EIA | Public domain | Double-counting avoidance, adjustments |
| 8 | `state_electricity_profiles_2023_table8.xlsx` (one per state) | XLSX | 8 files | EIA State Electricity Profiles | Public domain | Reconciliation targets |
| 9 | `eia861m_2023_monthly.xlsx` | XLSX | ~12k | EIA-861M | Public domain | Cross-check of annual totals |
| 10 | `store_states.json` | JSON | 8 | Task author | — | States in scope |
| 11 | `benchmark_method.pdf` | PDF | — | Task author | — | Rules in §2 |

## 5. Deterministic solution path

1. Load the sales file with its multi-row header; tidy into service type × sector columns.
2. For each state and sector: quantities from bundled + energy-only (incl. adjustment rows); revenue from all three.
3. Add short-form utilities per EIA's documented treatment.
4. Compute 24 prices; reconcile to EIA's state profile tables; resolve any gap > tolerance before proceeding.
5. Select the state with the highest commercial price; report the runner-up gap.

## 6. The traps

**Trap A — sum everything.** kWh doubled in high-choice states; their price roughly halves; the pilot goes to a
low-choice state.

**Trap B — bundled only.** Prices reflect the minority of customers on default service; ranking shifts.

**Trap C — no delivery revenue.** Energy-only revenue ÷ sales understates all-in prices in choice states.

**Trap D — dropping adjustment/short-form rows.** Small but enough to reorder close states.

## 7. Why the data is honest

EIA-861 reports each respondent's own revenue and sales by service type exactly as filed; the double-count structure
is how retail choice works and is documented by EIA. Published state totals provide a reconciliation anchor.

## 8. Draft task prompt (prose)

> We will put the solar pilot in whichever of our eight states had the highest all-in 2023 commercial electricity price,
> measured the way our benchmark method describes. Using the EIA-861 files and the state profile tables in the folder,
> compute residential, commercial and industrial average prices for all eight states and tell me the pilot state. Deliver
> `price_grid.xlsx` with the 24-cell grid, the revenue and sales components behind each cell (bundled, energy-only,
> delivery-only) and the reconciliation to EIA's published tables; and `price_heatmap.png`, the state-by-sector grid
> shaded by price with the pilot cell outlined. On the first sheet, state the pilot state, its price, the runner-up gap,
> and which state would have won if every row had simply been summed.

## 9. Deliverables

* `price_grid.xlsx`, `price_heatmap.png`.

## 10. Where 25+ rubric criteria come from

* 24 price cells; pilot state, price, runner-up gap; summed-rows alternative; reconciliation status per state.

## 11. Golden-output checklist

* Quantities once, revenue from all legs, adjustment rows kept, reconciliation done; decision stated.

## 12. Build notes (scope tuning)

* Choose eight states mixing high-choice and low-choice commercial markets so Traps A–C each change the winner.
* Confirm the exact Part/service-type labels and EIA's double-count rule in the 2023 technical notes before freezing the
  method text.
