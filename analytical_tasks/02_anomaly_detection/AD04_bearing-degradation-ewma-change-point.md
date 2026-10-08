# AD04 — When should the bearing alarm have fired? Control limits from the healthy period, on autocorrelated signals

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Domain | Industrial condition monitoring / predictive maintenance |
| Task shape | 17 · Periods around a change point (snapshots after the baseline checked against committed limits; longest excess run; go/no-go) |
| Core method | Phase I/Phase II monitoring: baseline-only parameter estimation, AR(1) residuals to remove autocorrelation, EWMA chart on residuals, causal (one-sided-in-time) computation |
| Analytical stump | Limits estimated from the whole run (including degradation) are too wide; raw autocorrelated features break Shewhart assumptions; centered smoothing uses future snapshots and fakes early detection |
| Primary sources | NASA Prognostics Data Repository — IMS Bearing run-to-failure dataset (University of Cincinnati) |

## 1. The real-world situation

A plant's reliability team wants to adopt a vibration-monitoring rule for its pumps and must show, on public
run-to-failure data, that the rule (a) would have warned **at least 48 hours** before failure and (b) does not cry wolf
on healthy bearings. Their prototype computed control limits from the full test record and smoothed RMS with a centered
moving average; it detected the failure "five days early" — and also raised alarms on healthy bearings every few hours.

## 2. The decision (one deterministic recommendation)

**Adopt or reject the monitoring rule, with its first-alarm lead time on the failing bearing and its false-alarm count on
healthy bearings.**

Rules (reliability engineering memo):

* Feature: RMS of each 1-second, 20 kHz vibration snapshot (one value per file, in time order).
* Failing case: test set 2, bearing 1 (outer-race failure at end of test). Healthy validation: test set 1, bearings 1 and 2
  (channels as documented), full runs.
* Baseline (Phase I) = the first 200 snapshots of each run; parameters are estimated from the baseline only.
* Fit AR(1) to baseline RMS by OLS; residuals e_t = x_t − (a + b·x_{t−1}) for every later snapshot using the baseline
  coefficients; EWMA z_t = 0.2·e_t + 0.8·z_{t−1} (z₀ = 0); upper limit = 3·σ_e·√(0.2/(2−0.2)) with σ_e from baseline residuals.
* Alarm = first snapshot whose EWMA exceeds the upper limit for 3 consecutive snapshots (alarm time = the third).
* Adopt if lead time (end of test − alarm time) ≥ 48 h on the failing bearing and ≤ 1 alarm episode per healthy bearing.

## 3. Why capable analysts get it wrong

* Using all data to set limits mixes degradation into "normal"; detection is delayed (or the method looks good because of
  look-ahead in the other direction).
* Vibration features are strongly autocorrelated; Shewhart limits from i.i.d. assumptions produce excessive false alarms.
* Centered moving averages are standard smoothing, but at time t they use t+1…t+k — impossible online.
* Lead time must be measured from the online alarm time, not from when a retrospective plot first "looks" different.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `2nd_test/` (984 snapshot files) | ASCII text | 20,480 rows × 4 channels each | NASA PCoE / IMS Bearings | Public (NASA PCoE; cite IMS, Univ. of Cincinnati) | Failing run |
| 2 | `1st_test/` (2,156 snapshot files) | ASCII text | 20,480 rows × 8 channels each | Same | Same | Healthy validation |
| 3 | `ims_readme.pdf` | PDF | — | NASA PCoE / IMS | Same | Channels, timing, failure modes |
| 4 | `rms_features_test1_test2.parquet` | Parquet | ~3.1k snapshots × channels | Derived | Same | Pre-computed RMS (for convenience) |
| 5 | `snapshot_timestamps.csv` | CSV | ~3.1k | Derived from file names | Same | Time axis |
| 6 | `montgomery_ewma_reference.pdf` (citation) | PDF | — | Statistical quality control text (cite) | Cite | EWMA limits |
| 7 | `reliability_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `prototype_results.xlsx` | XLSX | ~50 | Task author | — | Full-record limits + centered smoothing |
| 9 | `qiu_et_al_2006_bearing_paper.pdf` (citation) | PDF | — | Journal of Sound and Vibration (cite) | Cite | Dataset background |
| 10 | `asset_criticality.json` | JSON | — | Task author | — | Context |

## 5. Deterministic solution path

1. Compute RMS per snapshot per bearing channel; order by timestamp.
2. Baseline AR(1) fit; residuals forward; EWMA; limits from baseline residual σ.
3. Failing bearing: first sustained alarm; lead time to end of test.
4. Healthy bearings: count alarm episodes over full runs.
5. Decide; compare with prototype (full-record limits, centered smoothing, raw Shewhart).

## 6. Wrong paths (method errors, not misreadings)

**A — limits from full record.** Delayed alarm; lead time may fall below 48 h.

**B — Shewhart on raw RMS.** Many false alarms on healthy bearings → reject.

**C — centered smoothing.** Earlier "alarm" that could never have been raised online.

**D — single-point alarm.** More false alarms; differs from the persistence rule.

## 7. Why the stump is analytical, not semantic

Feature, baseline, model and alarm rule are explicit. The errors are about estimation windows, temporal dependence and
causality of filters — core monitoring methodology.

## 8. Draft task prompt (prose)

> Before we roll this vibration rule out to our pumps, show me on the IMS run-to-failure data whether it passes the
> reliability memo's test: enough warning on the failing bearing and no more than one false alarm per healthy bearing.
> Compute the rule exactly as the memo specifies and give me adopt or reject. Provide `monitoring_results.csv` (per
> bearing: baseline AR(1) coefficients, residual σ, alarm times, alarm episodes, lead time), `ewma_chart.png` showing the
> failing bearing's EWMA with the limit, the baseline window and the alarm marked, and a one-page `adoption_memo.pdf` with the
> decision, the lead time and the false-alarm counts, and why the prototype's results were not achievable online.

## 9. Deliverables

* `monitoring_results.csv`, `ewma_chart.png`, `adoption_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* AR(1) coefficients and σ for 3 bearings; alarm time and lead time; false-alarm episodes (2 bearings); decision; prototype
  contrasts; chart elements; ~10 spot-checked EWMA values.

## 11. Golden-output checklist

* Baseline-only estimation; residual EWMA; persistence rule; causal computation; decision against both criteria.

## 12. Build notes (scope tuning)

* Verify channel-to-bearing mapping in the IMS readme and snapshot timing (10-minute spacing with gaps).
* Confirm the prototype passes lead time but fails the false-alarm criterion, and the correct rule's outcome is decisive.
