# DS23 — Reservoir releases: planning on average inflow breaks the minimum-level guarantee in dry years

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Capacity commitments with chance constraints (committing compute or inventory while keeping a probability of shortfall below a limit) |
| Domain | Water resources / hydropower |
| Task shape | 02 · Forecast across many periods (monthly release plan for the next 12 months; the annual release volume committed) |
| Core method | Monthly water balance: storage_{t+1} = storage_t + inflow_t − release_t − evaporation(storage_t); inflow scenarios from the historical record (ensemble of 30 years resampled by month with persistence per memo); choose the largest constant annual release (monthly shape fixed) such that P(end-of-month elevation ≥ protection level in all months) ≥ 95% across scenarios |
| Analytical stump | A plan computed on mean monthly inflow keeps the reservoir above the protection level only in average years; with skewed, persistent inflows, dry sequences breach it far more often than 5%. Chance-constrained planning over scenarios sets a lower, defensible release |
| Primary sources | U.S. Bureau of Reclamation Lower Colorado / RISE reservoir data (daily/monthly storage, elevation, inflow, release); area–capacity tables |

## 1. The real-world situation

A water authority sets next year's release volume from a large reservoir subject to a rule that end-of-month elevation must stay above a
protection level with 95% probability. The operations planner used average monthly inflows and found a release of 9.0 million acre-feet feasible.
Hydrologists warned that inflows are skewed and dry years cluster.

## 2. The decision (one deterministic recommendation)

**The annual release volume (0.1 MAF steps) satisfying the 95% chance constraint, with the monthly plan and the breach probability of the
planner's 9.0 MAF plan.**

Rules (operations memo):

* Data: monthly unregulated inflow (or the memo's inflow series), storage, elevation, evaporation for the reservoir, 1964–2023; area–capacity table.
* Starting storage: the memo's January 1 value.
* Scenarios: 30 historical water years' monthly inflow sequences (each a scenario), applied to the coming year (memo: no resampling to keep
  persistence).
* Release shape: fixed monthly fractions (`release_shape.json`) of the annual volume.
* Evaporation: monthly rate × surface area (from area–capacity table at start-of-month storage).
* Feasible if ≥ 95% of scenarios keep end-of-month elevation ≥ protection level in all months (i.e., ≤ 1 scenario of 30 may breach, per memo).
* Choose the largest feasible annual volume; report breach probability of 9.0 MAF.

## 3. Why capable analysts get it wrong

* Mean inflows give a single tidy plan.
* Constraints apply to all months; a dry spring can breach mid-year.
* Evaporation depends on storage (area), a nonlinear feedback.
* Persistence matters; resampling months independently understates dry runs.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `reservoir_monthly_1964_2023.csv` | CSV | ~720 | USBR RISE / Lower Colorado River Operations | U.S. Gov public domain | Storage, elevation, inflow, release |
| 2 | `reservoir_daily_2000_2023.csv` | CSV | ~8.7k | USBR | Public domain | Daily data (context) |
| 3 | `area_capacity_table.csv` | CSV | ~3k | USBR | Public domain | Elevation–area–storage |
| 4 | `monthly_evaporation_rates.csv` | CSV | 12 | USBR (published coefficients) | Public domain | Evaporation |
| 5 | `release_shape.json` | JSON | 12 | Task author | — | Monthly fractions |
| 6 | `operations_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `planner_mean_inflow_plan.xlsx` | XLSX | 12 | Task author | — | Naive plan |

## 5. Deterministic solution path

1. Build scenarios from historical water years; starting storage.
2. For candidate volumes, simulate monthly balances with evaporation and elevation lookup.
3. Feasibility by scenario count; choose volume; breach probability of 9.0.

## 6. Wrong paths (method errors, not misreadings)

**A — mean inflow plan.** Breaches too often.

**B — annual balance only.** Mid-year breaches missed.

**C — constant evaporation.** Ignores area feedback.

**D — independent monthly resampling.** Underestimates drought runs.

## 7. Why the stump is analytical, not semantic

The balance, scenarios and constraint are specified. The trap is planning on means under a probabilistic constraint.

## 8. Draft task prompt (prose)

> What release volume can we commit next year while keeping the 95% elevation guarantee? Simulate the reservoir over the historical inflow
> scenarios as the operations memo specifies. Provide `release_feasibility.csv` (volume: scenarios breaching, probability), `elevation_fan.png`, and a
> one-page `release_decision.pdf`.

## 9. Deliverables

* `release_feasibility.csv`, `elevation_fan.png`, `release_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* Chosen volume; monthly plan (12); breach counts at 10 volumes; 9.0 MAF breach probability; mean-plan contrast.

## 11. Golden-output checklist

* Scenario construction; evaporation; elevation lookup; constraint; choice.

## 12. Build notes (scope tuning)

* Confirm the 9.0 MAF plan breaches in ≥ 5 of 30 scenarios.
