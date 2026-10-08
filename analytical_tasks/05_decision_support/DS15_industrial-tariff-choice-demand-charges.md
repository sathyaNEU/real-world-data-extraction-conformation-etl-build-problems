# DS15 — Choosing an industrial tariff: the bill is set by the worst 15 minutes, not the average load

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Choosing pricing plans billed on peaks (burstable bandwidth at the 95th percentile, cloud reserved capacity, demand charges) where averages hide what drives cost |
| Domain | Industrial energy procurement |
| Task shape | 07 · Grid of cells (3 tariffs × 2 operating options → annual bill; the tariff and option adopted) |
| Core method | Annual bill per tariff computed from 15-minute load data: energy charges by time-of-use period plus demand charges on each month's maximum 15-minute demand (and on-peak maximum where applicable); operating option B shifts the memo's flexible process loads out of peak windows subject to daily energy conservation; compare with bills from hourly or monthly averages |
| Analytical stump | Estimating bills from average load or hourly energy misses the 15-minute coincident maxima that set demand charges; the option that lowers energy cost (shifting to off-peak) can raise the billing maximum if shifted loads stack. The tariff choice flips when demand charges are computed correctly |
| Primary sources | UCI "Steel Industry Energy Consumption" dataset (DAEWOO Steel, Gwangyang, 15-minute data for 2018) |

## 1. The real-world situation

A steel plant can choose among three industrial tariffs and can reschedule some flexible processes. The energy manager estimated annual bills
from hourly averages and recommended a time-of-use tariff with high demand charges plus shifting flexible loads to the night. The utility's account
manager warned that shifting may create a new night-time peak.

## 2. The decision (one deterministic recommendation)

**The tariff × operating option with the lowest annual bill computed from 15-minute data, and the bill difference versus the energy manager's
choice.**

Rules (procurement memo):

* Data: UCI steel dataset (Usage_kWh per 15 minutes, load type labels) for 2018.
* Tariffs (`tariffs.json`): A flat energy rate + low demand charge; B time-of-use energy + monthly max demand charge; C time-of-use energy +
  on-peak max demand charge + lower energy rates.
* Demand (kW) per interval = Usage_kWh × 4.
* Option A: as operated. Option B: loads labelled "Maximum_Load" in peak windows reduced by 20% and the energy moved to the following off-peak
  hours evenly across intervals (memo's shifting rule).
* Bill = Σ energy × rate(period) + Σ_months demand charge × max demand (as defined per tariff) + fixed charges.
* Choose the lowest bill; report hourly-average-based bills for contrast.

## 3. Why capable analysts get it wrong

* Hourly or daily aggregation is common in energy analysis.
* Demand charges depend on the highest 15-minute interval in a month.
* Shifting load can create new peaks; the effect must be recomputed at 15-minute resolution.
* On-peak versus anytime demand definitions differ by tariff.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Steel_industry_data.csv` | CSV | 35,040 | UCI ML Repository (id 851) | CC BY 4.0 | 15-minute consumption and load type |
| 2 | `steel_dataset_description.html` | HTML | — | UCI | CC BY 4.0 | Variables |
| 3 | `tariffs.json` | JSON | 3 | Task author (structures modelled on published industrial tariffs; cite) | — | Tariff definitions |
| 4 | `procurement_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `energy_manager_hourly_estimate.xlsx` | XLSX | 6 | Task author | — | Naive bills |
| 6 | `tou_periods.json` | JSON | — | Task author | — | Period definitions |

## 5. Deterministic solution path

1. Load 15-minute data; compute demand; tag periods.
2. Apply option B shifting rule.
3. Compute bills for 6 combinations; choose; contrast.

## 6. Wrong paths (method errors, not misreadings)

**A — hourly averages for demand.** Understated maxima.

**B — shifting without recomputing peaks.** New peaks missed.

**C — anytime demand for tariff C.** Wrong charge basis.

**D — ignoring fixed charges.** Small but changes close cases.

## 7. Why the stump is analytical, not semantic

The tariffs, shifting rule and resolution are specified. The trap is the aggregation level for peak-based billing.

## 8. Draft task prompt (prose)

> Which tariff and operating option minimise our annual electricity bill? Compute bills from the 15-minute data as the procurement memo specifies,
> including demand charges, and compare with the hourly estimate. Provide `bill_grid.csv` (tariff × option: energy, demand, fixed, total),
> `monthly_peaks.png`, and a one-page `tariff_decision.pdf`.

## 9. Deliverables

* `bill_grid.csv`, `monthly_peaks.png`, `tariff_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 6 combinations × 4 components = 24; monthly maxima for the chosen combination (12); decision; contrast.

## 11. Golden-output checklist

* kW conversion; period tagging; shifting rule; demand definitions; bills; choice.

## 12. Build notes (scope tuning)

* Set tariff parameters so that the hourly-based choice differs from the 15-minute-based choice.
