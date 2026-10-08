# AD33 — Grid frequency events: every hour boundary looks like a lost power plant

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Transmission operators' disturbance logging; data-centre operators whose batteries and UPS fleets sell fast frequency response and must log real grid events |
| Domain | Power systems |
| Task shape | 04 · Setting one dial (the rate-of-change-of-frequency threshold for the event logger) |
| Core method | Remove the deterministic minute-of-hour frequency profile (market schedule changes at hour and quarter-hour boundaries) estimated by robust averaging; rate of change of frequency (RoCoF) over 500 ms windows on residual frequency; threshold chosen to capture labelled disturbances within a false-trigger budget |
| Analytical stump | Frequency routinely dips or overshoots around full hours because generation schedules step while demand ramps — "deterministic frequency deviations". Thresholds on absolute deviation or raw RoCoF trigger at nearly every hour boundary. Real disturbances (unit trips) are steep and not tied to the clock |
| Primary sources | Fingrid open data — Nordic grid frequency measurements at 10 Hz |

## 1. The real-world situation

A battery operator providing frequency containment reserve logs grid disturbances to reconcile its activation records. Its logger triggers
when frequency leaves 49.9–50.1 Hz; it produced hundreds of triggers a month, clustered within a minute of full hours. Engineers need a logger
that records real disturbances (generator trips, interconnector faults) without hour-boundary noise.

## 2. The decision (one deterministic recommendation)

**The RoCoF threshold (mHz/s, to the nearest 1) that captures every labelled disturbance in the calibration month with no more than 10
non-disturbance triggers.**

Rules (operations memo):

* Data: Fingrid 10 Hz frequency for the calibration month and an evaluation month (named in the memo).
* Deterministic profile: for each second-of-hour (0–3599), the median frequency deviation from 50 Hz across all hours of the month;
  residual = deviation − profile.
* RoCoF: slope of a least-squares line through the residual over a 500 ms window (5 samples), evaluated every 100 ms.
* Trigger: |RoCoF| ≥ T; triggers within 60 s merge into one.
* Labels: `disturbance_log.json` (time stamps of documented Nordic disturbances); a label is captured if a trigger occurs within ±10 s.
* Choose the largest T (grid 5–100 mHz/s) capturing all labels with ≤ 10 unlabelled triggers in the calibration month; report performance in
  the evaluation month.

## 3. Why capable analysts get it wrong

* Band thresholds on frequency are standard and intuitive.
* Hour-boundary deviations are large and systematic; they look like disturbances without context.
* Raw RoCoF also spikes at hour boundaries because the schedule ramps are steep; the profile must be removed first.
* Short windows amplify measurement noise; the memo fixes the window.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `fingrid_frequency_<month1>.zip` (daily CSVs) | CSV | ~26M samples | Fingrid open data | CC BY 4.0 | Calibration month |
| 2 | `fingrid_frequency_<month2>.zip` | CSV | ~26M | Fingrid | CC BY 4.0 | Evaluation month |
| 3 | `frequency_1s_summary.parquet` | Parquet | ~5.2M | Derived | CC BY 4.0 | Convenience |
| 4 | `disturbance_log.json` | JSON | ~15 | Task author (from published Nordic disturbance reports) | — | Labels |
| 5 | `entsoe_deterministic_frequency_deviations_report_citation.pdf` | PDF | — | ENTSO-E (cite) | Cite | Phenomenon |
| 6 | `operations_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `current_band_logger_triggers.csv` | CSV | ~600 | Task author | — | Existing triggers |
| 8 | `fcr_activation_records.xlsx` | XLSX | ~1k | Task author (illustrative from public FCR rules) | — | Context |
| 9 | `fingrid_data_description.html` | HTML | — | Fingrid | CC BY 4.0 | Measurement notes |
| 10 | `profile_check_values.json` | JSON | ~20 | Task author | — | Reference profile values |

## 5. Deterministic solution path

1. Load and align samples; deviation from 50 Hz.
2. Compute the second-of-hour median profile; residuals.
3. RoCoF on residuals; triggers and merging for each candidate T.
4. Choose T; evaluate on the second month; contrast with the band logger.

## 6. Wrong paths (method errors, not misreadings)

**A — absolute frequency band.** Hour-boundary triggers dominate.

**B — RoCoF on raw frequency.** Still triggered by schedule ramps.

**C — mean profile instead of median.** Disturbances contaminate the profile.

**D — choosing T on both months.** No out-of-sample check.

## 7. Why the stump is analytical, not semantic

The profile, RoCoF definition and selection rule are specified. The trap is failing to separate a deterministic periodic component from
event signatures.

## 8. Draft task prompt (prose)

> Set the RoCoF threshold for our disturbance logger following the operations memo: remove the hour-pattern from Fingrid frequency, compute
> RoCoF, and pick the largest threshold that captures every documented disturbance with at most ten other triggers. Provide `threshold_sweep.csv`,
> `hour_profile.png` (median deviation by second-of-hour with trigger counts by minute-of-hour before and after), and a one-page
> `logger_setting.pdf` with evaluation-month results.

## 9. Deliverables

* `threshold_sweep.csv`, `hour_profile.png`, `logger_setting.pdf`.

## 10. Where 25+ rubric criteria come from

* T; captures and false triggers at 6 checkpoints; per-label capture times; evaluation-month results; profile values at 4 seconds; band-logger
  contrast.

## 11. Golden-output checklist

* Profile computation; residual RoCoF; merging; selection; out-of-sample evaluation.

## 12. Build notes (scope tuning)

* Pick months with several documented disturbances.
* Confirm > 70% of band-logger triggers fall within ±60 s of a full hour.
