# Task number reservations and objective lanes

Several developers build in parallel, each in one Axis 1 objective lane with two builds at a time.
A build takes its number from this table, never from "the next free number" alone, because two
sessions that both read the corpus would otherwise draw the same `taskNN`. A session that needs a
number not listed here adds a row on `main` before it cuts its branch.

The suggested draw is a starting point for the build's own `guide-to-prompt` and `fingerprint`
stages; the guard decides, and a BLOCK means redraw inside the same lane.

| Task | Lane (objective) | Owner | Suggested draw (client domain / task type, Layer 2 family) | Status |
|---|---|---|---|---|
| task132 | Forecasting & Predictive Modeling | sathya8571 | actuarial-science-insurance / reserving-development-triangles, `field_method` (development across a settlement-speed change) | reserved |
| task133 | Forecasting & Predictive Modeling | sathya8571 | criminology-justice / recidivism-risk-assessment, `estimation_fit` (follow-up censoring, scored on later cohorts) | reserved |
| task134 | Experiment & Causal Analysis | developer 2 | energy-systems-utilities / tariff-demand-response-evaluation, `estimand_identification` (staggered rollout against not-yet-treated units) | reserved |
| task135 | Experiment & Causal Analysis | developer 2 | economics-econometrics / causal-identification-did-iv-rd-synthetic-control, `estimand_identification` (an eligibility threshold read as a regression discontinuity) | reserved |
| task136 | Data Quality Monitoring & Alerting | developer 3 | survey-research-official-statistics / census-register-administrative-data-quality, `estimation_fit` (alert limits that respect small-count noise) | reserved |
| task137 | Data Quality Monitoring & Alerting | developer 3 | physical-environmental-sciences / sensor-calibration-measurement, `forecast_uncertainty` (a drift alert rule's false-alarm rate across many stations) | reserved |

Each developer replaces "developer 2" or "developer 3" with their branch prefix when they start, and
sets Status to `in build`, then `shipped`, on `main`.
