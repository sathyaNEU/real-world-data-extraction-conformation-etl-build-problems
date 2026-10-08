# RC30 — Wholesale power prices fell 40%: was it the wind and solar build-out, or cheaper gas?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Input-cost attribution when drivers move together (cloud unit costs vs hardware prices and utilisation; airline fares vs fuel and capacity), where a single-driver regression credits the wrong one |
| Domain | Electricity markets / energy procurement |
| Task shape | 03 · Bridge between two totals (load-weighted average day-ahead price, year A → year B, bridged by gas cost, carbon cost, residual-load profile and residual) |
| Core method | Hourly merit-order model fitted on both years jointly: price = β0 + β1·RL + β2·RL² + β3·SRMC + β4·SRMC × RL + hour-of-day and month fixed effects, where RL = load − wind − solar and SRMC = gas-plant short-run marginal cost (fuel + carbon at memo efficiency and emission factor); counterfactual load-weighted prices substituting each driver (gas price, carbon price, hourly RL profile) between years; Shapley over the three drivers; residual = actual − modelled change |
| Analytical stump | Regressing price on the renewable share (or residual load) alone attributes the fall to renewables because gas prices fell in the same period. Gas and residual load interact: high residual load sets the gas plant on the margin, so the price effect of one driver depends on the level of the other, and sequential attribution depends on order. The procurement-relevant average is load-weighted, not the simple hourly mean |
| Primary sources | Bundesnetzagentur SMARD — hourly day-ahead prices (DE-LU), electricity consumption and generation by technology; BAFA monthly natural-gas border import prices; EEX primary auction results for EU allowances |

## 1. The real-world situation

A data-centre operator buying power in Germany saw its average wholesale cost fall about 40% between two years. Its sustainability team credited
the renewable build-out and proposed a long-term solar PPA on the premise that renewables now set prices. Procurement suspected cheaper gas did most
of the work, which would make the PPA's value depend on gas prices staying low. The CFO asked for an attribution before signing.

## 2. The decision (one deterministic recommendation)

**The dominant driver of the price fall (gas cost, carbon cost, or residual-load profile) by Shapley contribution to the change in load-weighted
average price, with the three contributions and the residual in €/MWh.**

Rules (procurement memo):

* Data: SMARD hourly day-ahead price (DE-LU), total load (grid load), wind onshore, wind offshore and solar generation for years A and B; BAFA monthly
  gas border price (€/MWh thermal); EEX auction clearing prices for EUAs, averaged by month.
* RL_h = load − (wind onshore + wind offshore + solar), in GW.
* SRMC_month = gas price ÷ 0.50 + EUA price × 0.202 ÷ 0.50 (€/MWh electric; efficiency 50%, emission factor 0.202 t/MWh thermal).
* Model fitted by OLS on all hours of both years; hours with negative prices included.
* Load-weighted price for a set of hours = Σ price × load ÷ Σ load.
* Counterfactuals: the model's load-weighted price with each driver at its year-A or year-B values (gas price and EUA price enter through SRMC;
  the RL driver swaps the full hourly RL and load profile of year A for that of year B).
* Shapley values over the three drivers (8 combinations); residual = actual change − Σ Shapley values.
* Dominant driver = largest absolute Shapley contribution.

## 3. Why capable analysts get it wrong

* Renewable growth is visible and widely reported; fuel prices sit in different datasets.
* Correlated drivers and an interaction make single-driver regressions misleading.
* The time-weighted average understates what a load-following buyer pays.
* Order of substitution changes the answer without a symmetric method.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `smard_day_ahead_prices_<A>_<B>.csv` | CSV | ~17.5k | Bundesnetzagentur SMARD | CC BY 4.0 | Hourly prices |
| 2 | `smard_consumption_<A>_<B>.csv` | CSV | ~17.5k | SMARD | CC BY 4.0 | Hourly load |
| 3 | `smard_generation_<A>_<B>.csv` | CSV | ~17.5k × 12 technologies | SMARD | CC BY 4.0 | Hourly wind and solar |
| 4 | `bafa_gas_border_prices.xlsx` | XLSX | ~300 | BAFA (Bundesamt für Wirtschaft und Ausfuhrkontrolle) | Public statistics (reuse with attribution; verify) | Monthly gas price |
| 5 | `eex_euaa_auction_results_<A>_<B>.xlsx` | XLSX | ~400 | EEX primary auction reports | Public reports (verify terms) | EUA prices |
| 6 | `procurement_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `sustainability_ppa_case.xlsx` | XLSX | — | Task author | — | Renewables-only regression |

## 5. Deterministic solution path

1. Align hourly SMARD series (time zone and DST handling); compute RL; attach monthly SRMC.
2. Fit the model; report coefficients and fit.
3. Counterfactual load-weighted prices for all 8 driver combinations; Shapley; residual.
4. Dominant driver; contrast with the renewables-only regression.

## 6. Wrong paths (method errors, not misreadings)

**A — price on renewables share only.** Gas price omitted; renewables credited with the fall.

**B — sequential substitution.** Order changes the split because of the SRMC × RL interaction.

**C — time-weighted average.** Understates the buyer's cost change and shifts attribution toward solar hours.

**D — annual averages of RL and SRMC.** The model's nonlinearity is lost; counterfactuals are biased.

## 7. Why the stump is analytical, not semantic

The model, constants and counterfactual design are specified. The trap is confounded, interacting drivers and the wrong averaging weight.

## 8. Draft task prompt (prose)

> Our sustainability team says renewables drove the 40% fall in power prices and wants a long-term solar PPA. Attribute the fall with the procurement
> memo's merit-order model and Shapley method and tell me what actually drove it. Provide `price_attribution.csv` (driver: €/MWh, share),
> `price_bridge.png`, and a one-page `ppa_context_note.pdf`.

## 9. Deliverables

* `price_attribution.csv` — Shapley contributions, residual, and the 8 counterfactual prices.
* `price_bridge.png` — waterfall from year A to year B load-weighted price.
* `ppa_context_note.pdf` — dominant driver and implications for the PPA case.

## 10. Where 25+ rubric criteria come from

* Data alignment (hours, DST, RL): 3.
* Coefficients and fit: 6.
* Counterfactual prices (8): 8.
* Shapley values and residual: 4.
* Dominant driver: 1.
* Contrasts (renewables-only regression, time-weighted average): 3+.

## 11. Golden-output checklist

* RL definition; SRMC constants; monthly join.
* Joint fit across years with fixed effects.
* Load-weighted averages; 8-combination Shapley.

## 12. Build notes (scope tuning)

* Choose years with both a large gas price fall and a visible renewable increase (e.g., 2022 → 2023); confirm the gas contribution exceeds the RL
  contribution while the renewables-only regression suggests the reverse.
