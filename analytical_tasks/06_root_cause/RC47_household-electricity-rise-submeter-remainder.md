# RC47 — Winter electricity use up 18%: which appliance circuit, or the unmetered remainder and the cold?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Cost drill-downs where part of the total is untagged (cloud spend with untagged resources, shared-service costs not allocated to teams, warehouse energy with unmetered loads) |
| Domain | Residential energy / smart-home analytics |
| Task shape | 12 · Drill-down to one leaf (household winter consumption change → sub-meters and unmetered remainder → weather vs non-weather for the largest contributor → hour-of-day block) |
| Core method | Minute data converted to energy (global active power in kW × 1000 ÷ 60 = Wh per minute); unmetered remainder = global energy − Σ sub-meters; valid-day rules for missing data; per-day energy by circuit; heating-degree-day regression on the reference winter for weather-sensitive circuits; drill to the circuit and hour block carrying the non-weather increase |
| Analytical stump | Summing the three sub-meters omits the largest consumer, the unmetered remainder (lighting, plug loads and electric space heating), and the units differ (kW averages vs Wh counters). Comparing raw winter totals with different numbers of missing days and a colder second winter attributes weather and gaps to appliances |
| Primary sources | UCI Machine Learning Repository — Individual Household Electric Power Consumption (minute data, Sceaux, France, 2006–2010); Météo-France daily climatological data (open data) |

## 1. The real-world situation

A smart-home energy service's customer saw winter electricity use rise 18% from one winter to the next and asked which appliances to replace. The
app's dashboard showed only the three sub-metered circuits (kitchen, laundry, water heater and air conditioning), and its automated advice pointed to
the water heater. The service's analyst wanted a full drill-down before the recommendation went out.

## 2. The decision (one deterministic recommendation)

**The recommendation sent — "weather, no appliance action" (if the weather component is ≥ 50% of the increase) or an action on the leaf circuit and
hour block — with the drill-down.**

Rules (service memo):

* Data: the UCI minute file; winters W1 = Dec 2008 – Feb 2009 and W2 = Dec 2009 – Feb 2010.
* Missing minutes ('?'): gaps ≤ 60 minutes linearly interpolated; days with > 10% missing minutes excluded; comparisons use mean daily energy over
  valid days.
* Energy per minute: global = Global_active_power × 1000 ÷ 60 (Wh); sub-meters as recorded (Wh); remainder = global − (S1 + S2 + S3); negative
  remainders set to 0 and counted.
* Weather: daily mean temperature at the memo's Météo-France station; HDD = max(0, 15.5 − T).
* Weather model per circuit, fitted on W1 valid days: daily kWh = a + b × HDD; weather component for the circuit = b × (mean HDD_W2 − mean HDD_W1)
  if b is significant at p < 0.05, else 0.
* Non-weather change = total change − weather component, per circuit.
* Drill: circuit with the largest non-weather increase → hour block (00–06, 06–09, 09–17, 17–23, 23–24) with the largest increase in that circuit's
  mean daily energy.

## 3. Why capable analysts get it wrong

* Sub-meters are the visible breakdown; the remainder is easy to forget.
* Units differ across fields.
* Missing data differ between winters.
* A colder winter raises heating in the unmetered remainder.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `household_power_consumption.txt` | TXT (semicolon) | ~2.08M | UCI ML Repository (id 235) | CC BY 4.0 | Minute data |
| 2 | `household_power_description.html` | HTML | — | UCI | CC BY 4.0 | Field definitions and units |
| 3 | `meteofrance_daily_<station>_2008_2010.csv` | CSV | ~1,100 | Météo-France open data (meteo.data.gouv.fr) | Licence Ouverte / Etalab 2.0 | Daily temperature |
| 4 | `service_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `dashboard_advice.xlsx` | XLSX | — | Task author | — | Sub-meter-only advice |

## 5. Deterministic solution path

1. Parse, interpolate, flag valid days; convert units; compute the remainder.
2. Mean daily energy by circuit for each winter.
3. Weather models and components; non-weather changes.
4. Drill to circuit and hour block; recommendation; contrast with the dashboard advice.

## 6. Wrong paths (method errors, not misreadings)

**A — sub-meters only.** The largest circuit (remainder) is missing; the water heater is blamed.

**B — kW treated as kWh.** Global energy mis-scaled by a factor of 60.

**C — raw totals with different valid days.** Gaps read as savings or increases.

**D — no weather adjustment.** A colder winter is attributed to appliances.

## 7. Why the stump is analytical, not semantic

Fields and units are documented; the rules are numeric. The trap is an incomplete breakdown and unit and coverage mismatches.

## 8. Draft task prompt (prose)

> Our dashboard tells this customer to replace the water heater because winter use rose 18%. Drill down with the service memo's method, including the
> unmetered remainder and weather, and tell me what to recommend. Provide `consumption_drilldown.csv` (circuit: W1, W2, weather, non-weather; hour
> blocks), `drilldown_chart.png`, and a one-page `customer_recommendation.pdf`.

## 9. Deliverables

* `consumption_drilldown.csv` — circuit and hour-block detail.
* `drilldown_chart.png` — circuit contributions with the leaf hour block highlighted.
* `customer_recommendation.pdf` — recommendation and why the dashboard advice was wrong.

## 10. Where 25+ rubric criteria come from

* Valid days and interpolation counts per winter: 4.
* Mean daily energy for 4 circuits × 2 winters: 8.
* Weather coefficients and components: 4.
* Non-weather changes: 4.
* Leaf circuit and hour block: 2.
* Recommendation and contrast: 3.

## 11. Golden-output checklist

* Wh conversion; remainder; negative remainders handled.
* Valid-day rule; HDD base 15.5 °C.
* Weather component only if significant.

## 12. Build notes (scope tuning)

* Confirm on the data which winter pair shows a rise and whether the remainder carries it; adjust W1/W2 within the dataset if needed and record the
  choice in the memo.
