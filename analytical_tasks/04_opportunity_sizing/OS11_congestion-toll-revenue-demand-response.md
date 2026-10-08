# OS11 — Toll increase revenue: entries fall when prices rise, and the baseline moved anyway

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Price-increase sizing at subscription and usage-priced businesses (streaming price hikes, API price changes) where demand responds and the pre-change trend must be separated from the price effect |
| Domain | Transportation pricing |
| Task shape | 13 · Scenarios and the flip point (toll level × elasticity scenarios → annual revenue; the toll increase adopted and the elasticity at which it stops raising revenue) |
| Core method | Estimate the entry response to the toll's introduction with a counterfactual from comparable crossings/periods (difference-in-differences against bridges and tunnels outside the zone, seasonally aligned); arc elasticity; revenue scenarios for proposed toll levels across an elasticity range; flip point where marginal revenue turns negative |
| Analytical stump | Multiplying current entries by the new toll ignores demand response; estimating the response as the raw before/after drop confounds it with seasonality and general traffic trends. A counterfactual is needed, and the revenue-maximising increase depends on the elasticity's range |
| Primary sources | MTA Congestion Relief Zone vehicle entries (NY Open Data); MTA Bridges and Tunnels hourly traffic (NY Open Data) |

## 1. The real-world situation

A transit authority must propose the peak toll level for the next phase of congestion pricing. The finance team multiplied 2025 entries by
candidate tolls and showed revenue rising linearly. Analysts pointed out that entries fell when tolling began, and that comparing January
with December mixes in seasonal effects.

## 2. The decision (one deterministic recommendation)

**The toll level adopted (from $9, $12, $15) that maximises annual revenue under the central elasticity estimate, and the elasticity at
which the next-higher option stops increasing revenue.**

Rules (pricing memo):

* Entries: CRZ vehicle entries by day and vehicle class, January–June 2025.
* Counterfactual: same weeks in 2024 for MTA bridges and tunnels crossings outside the zone (ratio scaling): expected 2025 entries = 2024 zone
  proxy × (2025 ÷ 2024 ratio at control crossings), with the zone proxy defined in the memo (crossings into Manhattan south of 60th Street).
* Response: Δln(entries) − Δln(control) between the 2024 and 2025 periods; price change from $0 to $9 handled with the memo's generalised cost
  formula (toll + time value) to compute arc elasticity ε.
* Scenarios: ε central and ±50%; tolls $9, $12, $15; revenue = entries(toll) × toll × (1 − exemption share), entries via constant elasticity on
  generalised cost.
* Choose the toll maximising central revenue; flip-point elasticity where revenue($15) = revenue($12).

## 3. Why capable analysts get it wrong

* Linear revenue projections ignore elasticity.
* Raw before/after comparisons include seasonality and trends.
* Price elasticity is defined on generalised cost; the toll is only part of the trip cost.
* Exemptions and discounts reduce effective revenue.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `MTA_Congestion_Relief_Zone_Vehicle_Entries.csv` | CSV | ~1–2M | NY Open Data (MTA) | NY Open Data terms (public) | Entries by time and class |
| 2 | `MTA_Bridges_and_Tunnels_Hourly_Traffic.csv` | CSV | ~5M | NY Open Data (MTA) | Public | Control crossings |
| 3 | `crossing_groups.json` | JSON | ~15 | Task author | — | Zone proxy and controls |
| 4 | `generalised_cost_parameters.json` | JSON | — | Task author | — | Time value, trip cost |
| 5 | `exemption_shares.json` | JSON | — | Task author (from public programme rules) | — | Discounts |
| 6 | `pricing_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `finance_linear_projection.xlsx` | XLSX | 3 | Task author | — | Naive projection |
| 8 | `cbd_tolling_program_citation.pdf` | PDF | — | MTA/FHWA environmental assessment (cite) | Public | Context |

## 5. Deterministic solution path

1. Build 2024 and 2025 weekly series for zone proxy and controls; counterfactual.
2. Response and arc elasticity on generalised cost.
3. Revenue scenarios; choose; flip point.
4. Contrast with linear projection.

## 6. Wrong paths (method errors, not misreadings)

**A — linear revenue.** Ignores response.

**B — raw before/after drop.** Seasonality and trend confounded.

**C — elasticity on toll alone.** Overstates sensitivity.

**D — ignoring exemptions.** Overstates revenue.

## 7. Why the stump is analytical, not semantic

The data and formulas are specified. The trap is estimating demand response with a counterfactual and using it in sizing.

## 8. Draft task prompt (prose)

> Which toll should the next phase use? Estimate the entry response to pricing against the control crossings, then size revenue for each toll
> level across elasticity scenarios as the pricing memo specifies. Provide `toll_scenarios.csv` (toll × elasticity: entries, revenue),
> `revenue_curves.png`, and a one-page `toll_recommendation.pdf` with the flip-point elasticity.

## 9. Deliverables

* `toll_scenarios.csv`, `revenue_curves.png`, `toll_recommendation.pdf`.

## 10. Where 25+ rubric criteria come from

* ε estimate; 9 scenario cells × (entries, revenue) = 18; choice; flip point; counterfactual figures.

## 11. Golden-output checklist

* Counterfactual construction; elasticity definition; scenarios; exemptions; flip point.

## 12. Build notes (scope tuning)

* Confirm the central-elasticity optimum differs from the linear projection's choice ($15).
