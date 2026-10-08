# DS40 — Retiming traffic signals: the peak hour average hides the 15 minutes that break the intersection

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Provisioning for bursts (server pools sized on peak 5-minute load rather than hourly averages, call-centre staffing by interval) |
| Domain | Traffic engineering |
| Task shape | 07 · Grid of cells (intersections × time periods → Webster optimal cycle length and critical v/c; the timing plans adopted for the corridor) |
| Core method | From turning-movement counts in 15-minute intervals, compute peak-hour flow rates as 4 × the peak 15-minute volume (equivalently hourly volume ÷ peak hour factor); critical lane flows per phase; flow ratios y_i = q_i ÷ s_i; Webster's C0 = (1.5L + 5) ÷ (1 − Y), bounded per memo; green splits proportional to y_i; check critical v/c ≤ 0.90 |
| Analytical stump | Using full-hour volumes understates the flow rate during the peak 15 minutes; cycle lengths and splits computed on hourly averages leave the critical movement oversaturated during the surge, causing queues that persist into the rest of the hour. Peak-hour factors differ by intersection and period |
| Primary sources | City of Toronto Open Data — traffic volumes at intersections (turning movement counts, 15-minute intervals) |

## 1. The real-world situation

A city retimes signals on a corridor of 8 intersections. The consultant computed cycle lengths from total AM-peak-hour turning volumes. After
implementation, two intersections had long queues during the 15 minutes before school start, while the hourly v/c looked acceptable.

## 2. The decision (one deterministic recommendation)

**The cycle length (s, rounded to 5) and green splits for each intersection in the AM and PM peaks, using peak-15-minute flow rates, and the
intersections where the consultant's plan exceeds v/c 0.90 during the peak 15 minutes.**

Rules (signal memo):

* Data: Toronto turning movement counts for the 8 intersections (latest count per intersection), 15-minute intervals, by approach and movement.
* Peak hour: the 60-minute window with highest total volume within 07:00–10:00 (AM) and 15:00–19:00 (PM); peak 15-minute volume within it.
* Design flow rate per movement = 4 × its volume in the intersection's peak 15-minute interval (memo convention).
* Phasing and lane groups from `phasing.json`; saturation flow 1,800 veh/h/lane adjusted for turns per memo factors; lost time 4 s per phase.
* Webster C0 bounded to [60, 150] s; splits proportional to critical y_i; v/c check per lane group.
* Contrast: consultant plan from hourly volumes (`consultant_plans.csv`), evaluated at peak 15-minute flows.

## 3. Why capable analysts get it wrong

* Hourly volumes are the standard reported unit.
* Peaks within the hour cause oversaturation and residual queues.
* PHF varies across intersections (schools, shift changes).
* Webster's formula is sensitive to Y near 1.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `tmc_raw_data_<years>.csv` | CSV | ~3M rows (15-minute × movement) | City of Toronto Open Data (Traffic Volumes at Intersections) | Open Government Licence – Toronto | Turning movement counts |
| 2 | `tmc_locations.csv` | CSV | ~10k | City of Toronto | OGL – Toronto | Intersection metadata |
| 3 | `phasing.json` | JSON | 8 | Task author | — | Phase/lane group definitions |
| 4 | `signal_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `consultant_plans.csv` | CSV | 16 | Task author | — | Hourly-based plans |
| 6 | `webster_1958_citation.pdf` | PDF | — | Cite | Cite | Method |
| 7 | `hcm_saturation_flow_reference.pdf` | PDF | — | Cite | Cite | Adjustments |

## 5. Deterministic solution path

1. Extract counts for the 8 intersections; peak hours; peak 15-minute volumes.
2. Design flow rates; critical flow ratios; Webster cycles; splits.
3. v/c checks; consultant plan evaluation; differences.

## 6. Wrong paths (method errors, not misreadings)

**A — hourly volumes.** Undersized cycles/splits for peaks.

**B — corridor-wide PHF.** Intersection differences lost.

**C — ignoring turn adjustments.** Overstated capacity.

**D — unbounded Webster cycles.** Impractical results.

## 7. Why the stump is analytical, not semantic

The flow conversions and formula are specified. The trap is averaging over bursts when sizing capacity.

## 8. Draft task prompt (prose)

> Retime the corridor's signals for AM and PM peaks using peak-15-minute flow rates as the signal memo specifies, and test the consultant's plans at
> those flows. Provide `timing_plans.csv` (intersection × period: PHF, C0, splits, critical v/c), `peak_15min_profile.png`, and a one-page
> `retiming_decision.pdf`.

## 9. Deliverables

* `timing_plans.csv`, `peak_15min_profile.png`, `retiming_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 8 intersections × 2 periods × (C0, critical v/c) = 32; consultant failures; PHFs.

## 11. Golden-output checklist

* Peak hour search; peak 15 minutes; flow rates; saturation adjustments; Webster bounds; v/c.

## 12. Build notes (scope tuning)

* Choose intersections near schools or plants with PHF < 0.85 so hourly-based plans fail.
