# AD19 — Catching air leaks on a train compressor: alarms must live on cycles, not on raw samples

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Rail and fleet predictive maintenance (compressor, HVAC and brake subsystems); any duty-cycled equipment monitored from sensor streams |
| Domain | Transportation maintenance / IoT analytics |
| Task shape | 17 · Periods around a change point (days before each documented failure checked against a committed healthy baseline; earliest sustained alarm; go/no-go) |
| Core method | Event segmentation of compressor ON/OFF cycles from the digital signal; per-cycle features (ON duration, OFF-period pressure decay rate, cycles per hour); robust healthy baseline; one-sided CUSUM on the decay-rate feature |
| Analytical stump | Raw pressure and motor-current thresholds fire every time the compressor loads and unloads; leaks show up as faster pressure decay while the compressor is off and shorter OFF periods — features that only exist after segmenting the duty cycle |
| Primary sources | UCI MetroPT-3 dataset (Porto metro train air production unit) |

## 1. The real-world situation

A metro operator wants to detect air leaks in train air-production units early enough to schedule repairs overnight. A first model flagged
whenever reservoir pressure fell below 8.2 bar or motor current exceeded a limit; it produced dozens of alarms a day — every normal
compressor cycle — and engineers ignored it. Four leak failures in 2020 were documented by maintenance.

## 2. The decision (one deterministic recommendation)

**Adopt the cycle-based CUSUM alarm or not: it must alarm at least 2 hours before each documented failure window and raise no more than
one alarm outside failure windows per month.**

Rules (maintenance analytics memo):

* Data: MetroPT-3 analog and digital signals (February–August 2020).
* Cycles: compressor ON periods from the `COMP` digital signal (per the memo's polarity convention); an OFF period is the interval between
  consecutive ON periods.
* Features per OFF period ≥ 60 s: decay rate = (TP3 at start − TP3 at end) ÷ duration (bar/min); also ON duration and cycles per hour.
* Healthy baseline: OFF periods in the first 30 days not within 7 days of a documented failure; μ = median decay rate, σ = 1.4826 × MAD.
* One-sided CUSUM on standardized decay rate z: S_t = max(0, S_{t−1} + z_t − 0.5); alarm when S_t > 8; reset to 0 after an alarm or after 6
  hours without positive increments.
* Lead time per failure = failure window start − first alarm within the preceding 48 hours.

## 3. Why capable analysts get it wrong

* Sensor streams invite sample-level thresholds; in duty-cycled machines, large swings are normal operation.
* The leak signature is a property of OFF periods (pressure bleed-down), which requires segmentation.
* Shewhart thresholds on a slowly worsening leak react late; CUSUM accumulates small persistent shifts.
* Baselines that include pre-failure days dilute the signature.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `MetroPT3(AirCompressor).csv` | CSV | ~1.5M | UCI ML Repository (MetroPT-3) | CC BY 4.0 | Sensor stream |
| 2 | `metropt3_failure_reports.json` | JSON | 4 | From the dataset paper's failure table | CC BY 4.0 (cite paper) | Failure windows |
| 3 | `metropt3_paper.pdf` (citation) | PDF | — | Scientific Data / dataset paper (cite) | Cite | Signal descriptions |
| 4 | `off_periods.parquet` | Parquet | ~40k | Derived | CC BY 4.0 | Segmented OFF periods with features |
| 5 | `on_periods.parquet` | Parquet | ~40k | Derived | CC BY 4.0 | ON periods |
| 6 | `signal_dictionary.csv` | CSV | 15 | Derived from paper | CC BY 4.0 | Units, polarity |
| 7 | `page_cusum_reference.pdf` (citation) | PDF | — | Cite | Cite | CUSUM |
| 8 | `maintenance_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `threshold_model_alarms.csv` | CSV | ~5k | Task author | — | Raw-threshold alarms |
| 10 | `monthly_calendar.csv` | CSV | ~7 | Derived | — | Month boundaries |

## 5. Deterministic solution path

1. Segment ON/OFF periods; compute features; baseline.
2. Run CUSUM over OFF periods in time order; record alarms.
3. Lead times per failure; false alarms per month outside failure windows; decide.
4. Contrast with raw-threshold alarm counts.

## 6. Wrong paths (method errors, not misreadings)

**A — raw thresholds.** Alarms on every cycle.

**B — sample-level CUSUM.** Duty cycle dominates.

**C — baseline including pre-failure days.** Signature diluted.

**D — Shewhart on decay rate.** Late detection.

## 7. Why the stump is analytical, not semantic

Signals, segmentation and alarm rules are specified. The trap is feature engineering on duty-cycled equipment and choice of a detector
for slow drifts.

## 8. Draft task prompt (prose)

> Decide whether the cycle-based leak alarm in the maintenance memo is good enough to deploy: segment compressor cycles in MetroPT-3, run the
> CUSUM on off-period pressure decay, and check lead times before the four documented failures and false alarms per month. Provide
> `alarm_evaluation.csv` (failure: first alarm, lead time; month: false alarms), `decay_rate_cusum.png`, and a one-page
> `deployment_decision.pdf`.

## 9. Deliverables

* `alarm_evaluation.csv`, `decay_rate_cusum.png`, `deployment_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* Baseline μ, σ; 4 lead times; 7 monthly false-alarm counts; decision; raw-threshold contrast; segmentation counts.

## 11. Golden-output checklist

* Correct segmentation and polarity; feature formula; robust baseline; CUSUM parameters and reset; evaluation windows.

## 12. Build notes (scope tuning)

* Verify the failure windows and the `COMP` polarity from the dataset paper; publish segmentation counts.
* Confirm at least one failure is caught > 2 hours early and the raw-threshold model exceeds 100 alarms per month.
