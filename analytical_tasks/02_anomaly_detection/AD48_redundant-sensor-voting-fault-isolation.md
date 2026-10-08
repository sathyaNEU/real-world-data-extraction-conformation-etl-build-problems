# AD48 — Three sensors, one drifting: averaging hides the fault, voting finds it

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Redundant-sensor management in aircraft (angle-of-attack disagreement), autonomous vehicles and data-centre environmental monitoring, where one faulty channel can bias a fused value |
| Domain | Environmental measurement / sensor reliability |
| Task shape | 10 · Scorecard against thresholds (stations × fault-isolation checks → which stations get a sensor swap in the next maintenance round) |
| Core method | Pairwise differences among three co-located sensors (d12, d13, d23); a sensor is suspect when both differences involving it exceed the tolerance while the third pair agrees; persistence over a window; comparison with single-sensor range/step checks and with station-mean anomaly checks |
| Analytical stump | The station's reported value is a fusion of three sensors; anomaly checks on the fused value miss a slow drift in one sensor (it shifts the mean by one third and stays within climatological ranges). Single-sensor range checks pass because the drifting sensor is still plausible. Only cross-sensor consistency isolates which channel is wrong |
| Primary sources | NOAA U.S. Climate Reference Network (USCRN) sub-hourly data with individual sensor channels |

## 1. The real-world situation

A monitoring network has triple-redundant air-temperature sensors at each station. A maintenance contractor swaps sensors when quality
checks flag them, but its checks run on the station's fused temperature and on each sensor against climatological limits. An audit found
that several stations had one sensor drifting by more than 0.3 °C for months without a swap.

## 2. The decision (one deterministic recommendation)

**The stations (among the 40 in the region) that receive a sensor swap in the next maintenance round, and which sensor at each.**

Rules (maintenance memo):

* Data: USCRN 5-minute data for the 40 stations, last 12 months; sensor channels T1, T2, T3 (per the product's documentation); exclude
  records with maintenance or calibration flags.
* Pairwise differences per 5-minute record; daily median of each difference.
* Tolerance: |daily median difference| > 0.3 °C.
* Suspect sensor on a day: both of its pair differences exceed tolerance and the remaining pair is within tolerance.
* Swap: a sensor suspect on ≥ 20 of the last 30 days with valid data.
* Comparison checks for the scorecard: (a) fused-value anomaly versus neighbour stations > 1.5 °C; (b) single-sensor range limits; report
  which stations each would have flagged.

## 3. Why capable analysts get it wrong

* Quality control on the published (fused) value is the natural first check.
* Range checks catch gross failures, not drifts.
* With three sensors, the faulty one is identified by disagreement with two agreeing peers; averaging dilutes it.
* Day-level medians are needed because radiative effects cause short-lived pairwise differences (aspirated shields differ briefly).

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–40 | `CRNS0101-05-<yyyy>-<station>.txt` (40 stations) | Fixed-width text | ~105k each | NOAA NCEI USCRN sub-hourly products (sensor-level channels per the raw data archive) | U.S. Gov public domain | 5-minute observations |
| 41 | `uscrn_subhourly_readme.txt` | Text | — | NOAA NCEI | Public domain | Field definitions, flags |
| 42 | `uscrn_stations.tsv` | TSV | ~140 | NOAA | Public domain | Station metadata |
| 43 | `region_stations.json` | JSON | 40 | Task author | — | Stations in scope |
| 44 | `maintenance_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 45 | `contractor_qc_flags.xlsx` | XLSX | ~200 | Task author | — | Current QC outcome |
| 46 | `daily_pair_differences.parquet` | Parquet | ~14.6k | Derived | Public domain | Convenience |
| 47 | `maintenance_visits.json` | JSON | ~60 | Task author (from station histories) | — | Exclusion windows |

## 5. Deterministic solution path

1. Parse files; exclude flagged records and maintenance windows.
2. Pairwise differences; daily medians; tolerance tests.
3. Suspect sensors per day; persistence over the last 30 valid days; swap list.
4. Run the comparison checks; scorecard; contrast with the contractor flags.

## 6. Wrong paths (method errors, not misreadings)

**A — QC on the fused value.** Drift diluted.

**B — single-sensor range checks.** Plausible values pass.

**C — 5-minute differences without daily aggregation.** Radiative transients flag good sensors.

**D — flagging the sensor with the largest absolute deviation from the mean.** The mean is pulled by the faulty sensor; pairs disagree.

## 7. Why the stump is analytical, not semantic

Channels, tolerances and voting rules are specified. The trap is fault isolation in redundant systems — fused-level checks versus
consistency checks.

## 8. Draft task prompt (prose)

> Which stations need a sensor swap, and which sensor? Apply the pairwise-voting check in the maintenance memo to the 40 stations and compare
> it with our fused-value and range checks. Provide `station_scorecard.csv` (station: suspect days per sensor, swap, other checks' flags),
> `pair_differences.png` (daily pair differences for the swapped stations), and a one-page `swap_list.pdf`.

## 9. Deliverables

* `station_scorecard.csv`, `pair_differences.png`, `swap_list.pdf`.

## 10. Where 25+ rubric criteria come from

* Each swapped station and sensor; suspect-day counts for 10 stations; comparison flags; contractor contrast; exclusions.

## 11. Golden-output checklist

* Flag exclusions; pair differences; daily medians; voting rule; persistence; comparison checks.

## 12. Build notes (scope tuning)

* Verify sensor-level channel availability and naming in the chosen product (the raw archive carries the three channels); document it.
* Confirm at least three stations have single-sensor drift invisible to fused-value checks.
