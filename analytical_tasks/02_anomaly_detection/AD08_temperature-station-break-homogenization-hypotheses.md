# AD08 — A weather station's sudden warm jump: climate, instrument, relocation or observing time?

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Domain | Climate data / weather-index insurance / infrastructure design data |
| Task shape | 18 · Hypotheses versus evidence (candidate causes × lines of evidence, each cell with its figure) |
| Core method | Relative homogeneity analysis: station-minus-neighbour difference series, step estimation around candidate dates, Tmax/Tmin signature analysis, seasonal structure of the step |
| Analytical stump | A station compared with itself cannot separate climate from a measurement break — shared regional climate cancels only in a difference with neighbours. The step's sign pattern in Tmax vs Tmin and its seasonality distinguish instrument, siting and observing-time causes |
| Primary sources | NOAA GHCN-Daily, USHCN v2.5 monthly (raw / TOB / adjusted), NOAA HOMR station history metadata |

## 1. The real-world situation

A crop-insurance company prices a heat-index product off one long-record cooperative station. Its annual mean temperature
jumps by about half a degree in the mid-1980s and stays there. The pricing analyst attributed it to climate warming and
raised premiums. The reinsurer's meteorologist asked whether anything else happened at the station that year.

## 2. The decision (one deterministic recommendation)

**Which single cause explains the step, and how large is the step (°C) that the pricing series should be adjusted for?**

Hypotheses (rows): H1 regional climate shift; H2 instrument change (liquid-in-glass shelter to electronic MMTS); H3
station relocation; H4 change in observation time (time-of-observation bias); H5 gradual local warming (urbanization).

Evidence (columns), each with a stated figure: E1 step in the station's own annual Tmean (5 years after − 5 years before the
candidate date); E2 step in the station-minus-neighbour difference series (neighbour composite = mean of the 5 nearest
stations with complete records, first-differenced composite as in the memo); E3 sign and size of the difference-series step
separately for Tmax and Tmin; E4 seasonality of the Tmean difference step (DJF vs JJA); E5 metadata events within ±12 months
(HOMR).

Rules (analysis memo): a cell is "consistent" if the figure matches the hypothesis's expected signature as tabulated in the
memo (e.g. MMTS: Tmax step negative, Tmin step positive, little seasonality; observation-time change from afternoon to
morning: cooling of mean, seasonal; relocation: steps of the same sign in Tmax and Tmin; regional climate: E2 ≈ 0). The
adopted cause is the hypothesis consistent with all five lines; the adjustment = the E2 Tmean step (two decimals).

## 3. Why capable analysts get it wrong

* A step in one station's series looks like climate unless compared with neighbours that share the climate.
* Instrument changes affect maximum and minimum temperatures in opposite directions, so the mean can hide them.
* Observation-time changes create seasonal biases; annual means average them away partially.
* Metadata are incomplete; the statistical signature must corroborate them.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `USC00xxxxxx.dly` (target) | Fixed-width | ~50k days | NOAA NCEI GHCN-Daily | U.S. Gov public domain | Daily Tmax/Tmin |
| 2–6 | `USC00yyyyyy.dly` … (5 neighbours) | Fixed-width | ~50k days each | NOAA NCEI | Public domain | Neighbours |
| 7 | `ushcn_v2.5_raw_tmax_tmin.txt` (region extract) | Fixed-width | ~50k station-months | NOAA NCEI USHCN v2.5 | Public domain | Monthly raw |
| 8 | `ushcn_v2.5_tob_tmax_tmin.txt` | Fixed-width | same | NOAA NCEI | Public domain | TOB-adjusted monthly |
| 9 | `ushcn_v2.5_fls52_tmax_tmin.txt` | Fixed-width | same | NOAA NCEI | Public domain | Fully adjusted (validation only) |
| 10 | `homr_station_history_target_neighbours.json` | JSON | ~100 events | NOAA HOMR | Public domain | Equipment, location, observation-time changes |
| 11 | `menne_williams_pha_reference.pdf` (citation) | PDF | — | Journal of Climate (cite) | Cite | Pairwise homogenization background |
| 12 | `analysis_memo.pdf` | PDF | — | Task author | — | Hypothesis signatures, windows, rules |
| 13 | `pricing_series_current.csv` | CSV | ~100 years | Task author | — | Unadjusted pricing series |

## 5. Deterministic solution path

1. Build monthly and annual Tmax/Tmin/Tmean for target and neighbours (completeness rules in memo).
2. Construct the neighbour composite and difference series; compute E1–E4 around the candidate date; read E5.
3. Fill the 5 × 5 grid; select the consistent hypothesis; report the E2 step as the adjustment.
4. Validate against USHCN adjusted data (should show a similar adjustment).

## 6. Wrong paths (method errors, not misreadings)

**A — own-series step as evidence of climate.** H1 adopted; no adjustment; premiums overstated.

**B — Tmean only.** Instrument signature invisible; H3 or H1 adopted.

**C — no seasonal split.** Observation-time effects mistaken for instrument effects (or vice versa).

**D — metadata alone.** An undocumented change missed, or a documented but immaterial one blamed.

## 7. Why the stump is analytical, not semantic

The data are standard temperature records; the memo tabulates each hypothesis's expected signature. The difficulty is
constructing the right comparison (difference with neighbours, split by element and season) — an analytical design.

## 8. Draft task prompt (prose)

> Before we reprice the heat product, tell me what caused the mid-1980s step in our station's temperatures and how much we
> should adjust for it. Using the GHCN and USHCN files and the station histories in the folder, test each hypothesis in the
> analysis memo against each line of evidence. Deliver `hypothesis_grid.xlsx` (5 × 5 cells with the figure and a
> consistent/inconsistent mark, plus the step calculations) and `difference_series.png` showing annual Tmax and Tmin
> station-minus-neighbour differences with the candidate date and the HOMR events marked. On the first sheet, state the
> cause, the adjustment in °C, and how the pricing series changes.

## 9. Deliverables

* `hypothesis_grid.xlsx`, `difference_series.png`.

## 10. Where 25+ rubric criteria come from

* 25 grid cells with figures; adopted cause; adjustment; validation against USHCN; chart marks.

## 11. Golden-output checklist

* Neighbour composite as specified; windows; element and seasonal splits; metadata cross-check; signature matching.

## 12. Build notes (scope tuning)

* Choose a target station with a documented 1980s MMTS conversion (common in the U.S. cooperative network) and neighbours
  without simultaneous changes; confirm the E3 signature is clear.
* Write the signature table in the memo from the cited literature, with expected signs and approximate magnitudes.
