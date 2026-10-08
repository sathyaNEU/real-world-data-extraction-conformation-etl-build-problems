# DS35 — Choosing contracted power for each customer: commit to a high quantile, and fix the clock first

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Committed-capacity decisions with overage penalties (contracted bandwidth, reserved database capacity, committed-use discounts) |
| Domain | Electricity retail / B2B energy |
| Task shape | 04 · Setting one dial (the contracted power level for each of 20 business clients from a standard ladder, minimising annual charges including excess-demand penalties) |
| Core method | Clean 15-minute consumption (remove daylight-saving artefacts: the dataset's March missing hour recorded as zeros and October's doubled hour); convert to kW; annual cost(C) = capacity charge × C × 12 + penalty × Σ_months max(0, monthly max kW − C); choose C from the ladder minimising cost; compare with C = annual mean demand × 1.2 and C = annual max |
| Analytical stump | Sizing contracts on average load ignores that penalties accrue on monthly maxima; sizing on the single annual maximum overpays every month. The optimum depends on the distribution of monthly maxima and the price ratio. DST artefacts (zeros, doubled values) distort maxima if not cleaned |
| Primary sources | UCI "ElectricityLoadDiagrams20112014" dataset (370 Portuguese clients, 15-minute kW readings) |

## 1. The real-world situation

An energy retailer advises business clients on contracted power. The advisory tool set contracted power at 120% of average demand. Several clients
paid large excess-demand penalties; others with spiky loads were advised to contract their single highest reading, overpaying all year.

## 2. The decision (one deterministic recommendation)

**The contracted power for each of 20 clients (from the ladder 3.45–41.4 kVA in the memo's steps, converted to kW at the memo's factor) for 2014,
and the total annual savings versus the advisory tool.**

Rules (advisory memo):

* Data: UCI ElectricityLoadDiagrams20112014; values are kW for each 15-minute interval per the documentation (kWh = value ÷ 4); demand is used
  directly in kW.
* DST cleaning: in the last Sunday of March, the hour 1:00–2:00 values are zeros → fill by linear interpolation; in October, the extra hour is
  aggregated → split equally (per dataset notes).
* Clients: 20 in `clients_in_scope.json` (selected with full 2014 data).
* Monthly maximum demand (kW) from cleaned data.
* Costs: capacity charge €/kW-month and excess penalty €/kW over contract per month (tariff file).
* Choose ladder step minimising annual cost; ties → lower step.
* Contrast: tool rule (1.2 × mean) and annual maximum.

## 3. Why capable analysts get it wrong

* Average load is simple and stable.
* Penalties depend on monthly peaks; the cost function is piecewise linear in C.
* DST artefacts create spurious peaks or zeros.
* Units in the dataset require careful conversion.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `LD2011_2014.txt` | Semicolon-separated text | ~140k timestamps × 370 clients | UCI ML Repository (id 321) | CC BY 4.0 | 15-minute loads |
| 2 | `electricityloaddiagrams_description.html` | HTML | — | UCI | CC BY 4.0 | Units, DST notes |
| 3 | `clients_in_scope.json` | JSON | 20 | Task author | — | Clients |
| 4 | `tariff.json` | JSON | — | Task author (structure modelled on published Portuguese tariffs; cite) | — | Charges and ladder |
| 5 | `advisory_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `tool_recommendations.xlsx` | XLSX | 20 | Task author | — | Current tool output |

## 5. Deterministic solution path

1. Load; convert units; clean DST days.
2. Monthly maxima per client.
3. Cost per ladder step; choose; savings versus tool and annual max.

## 6. Wrong paths (method errors, not misreadings)

**A — 1.2 × mean.** Penalties.

**B — annual maximum.** Overpays.

**C — uncleaned DST data.** Spurious peaks.

**D — unit confusion (treating values as kWh and multiplying by 4).** Factor-of-4 errors.

## 7. Why the stump is analytical, not semantic

The cleaning, units and cost function are specified. The trap is sizing commitments on averages and dirty maxima.

## 8. Draft task prompt (prose)

> What contracted power should each client take for 2014? Clean the data, compute monthly maxima and minimise annual charges as the advisory memo
> specifies. Provide `contract_recommendations.csv` (client: monthly maxima, chosen step, cost, tool step, tool cost), `cost_curves.png`, and a one-page
> `contract_advice.pdf`.

## 9. Deliverables

* `contract_recommendations.csv`, `cost_curves.png`, `contract_advice.pdf`.

## 10. Where 25+ rubric criteria come from

* 20 clients' chosen steps; costs for 6 clients; total savings; DST cleaning checks.

## 11. Golden-output checklist

* Unit conversion; DST cleaning; monthly maxima; cost function; tie rule.

## 12. Build notes (scope tuning)

* Include clients with spiky loads and flat loads so that both naive rules are wrong for some clients.
