# AD49 — Solar underperformance: when the irradiance sensor is dirty, every array looks broken

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Fleet-monitoring and O&M teams at solar operators and inverter makers comparing sites and strings against each other rather than against a single weather sensor |
| Domain | Renewable energy operations |
| Task shape | 01 · Ranked list under a cap (5 systems for a site visit) |
| Core method | Peer-relative index: each system's daily specific yield (kWh/kWp) divided by the site median of specific yield on that day; normalised by the system's own ratio during a reference period; sustained-deficit rule; contrast with irradiance-based performance ratio (PR) alarms |
| Analytical stump | Performance ratio needs measured irradiance; when the pyranometer soils, drifts or is shaded, PR falls for every system and alarms flood. Systems on the same site share weather and sensor errors; a ratio to the peer median cancels them. Technology differences are fixed effects, removed by each system's own reference ratio |
| Primary sources | DKA Solar Centre (Alice Springs) system data — 5-minute power and site weather |

## 1. The real-world situation

An O&M contractor monitors about 30 PV systems of different technologies at one test site and can make **5** targeted visits per quarter.
Its alarm flags any system whose monthly PR falls below 0.75. Last quarter almost every system alarmed for six weeks; the cause turned out to
be dust on the reference pyranometer. A genuinely failing string was lost in the noise.

## 2. The decision (one deterministic recommendation)

**The 5 systems visited this quarter, ranked by sustained peer-relative deficit, and the 6th.**

Rules (O&M memo):

* Data: 5-minute AC power for systems in `systems_in_scope.csv` (rated kWp given) and site global horizontal irradiance, for the reference
  year and the target quarter.
* Daily specific yield Y = Σ power × (5/60) ÷ kWp; exclude days with > 10% missing intervals for that system.
* Peer index I = Y ÷ median(Y across all systems with valid data that day).
* Reference ratio ρ = median of I over the reference year; normalised index N = I ÷ ρ.
* Deficit day: N < 0.92. Sustained deficit: the longest run of consecutive valid deficit days in the target quarter.
* Eligibility: runs ≥ 7 days. Rank by mean (1 − N) over the run × run length (deficit-days); top 5; report #6.
* PR comparison: monthly PR = Σ energy ÷ (kWp × Σ GHI ÷ 1 kW/m²) with the existing 0.75 threshold.

## 3. Why capable analysts get it wrong

* PR is the industry's standard KPI and assumes a trustworthy irradiance sensor.
* Shared errors (sensor soiling, calibration drift, clipping at site level) affect all systems equally.
* Technologies differ in yield; comparing raw yields across them flags low-efficiency designs as faulty.
* Single bad days (cloud edges, outages) are not sustained underperformance.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–30 | `<system_id>_<year>.csv` (≈ 30 systems × 2 years) | CSV | ~105k each | DKA Solar Centre data download | DKASC terms (free use with acknowledgement; verify) | 5-minute power |
| 31 | `site_weather_<year>.csv` | CSV | ~105k each | DKA Solar Centre | Same | GHI, temperature |
| 32 | `systems_in_scope.csv` | CSV | ~30 | Task author (from DKASC system pages) | — | kWp, technology |
| 33 | `om_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 34 | `pr_alarm_log.xlsx` | XLSX | ~200 | Task author | — | PR alarms |
| 35 | `pyranometer_cleaning_log.json` | JSON | ~10 | Task author | — | Context |
| 36 | `daily_yield.parquet` | Parquet | ~22k | Derived | Same | Convenience |
| 37 | `iec_61724_pr_citation.pdf` | PDF | — | IEC 61724 (cite) | Cite | PR definition |

## 5. Deterministic solution path

1. Daily yields with missing-data rule; site medians.
2. Peer index; reference ratios; normalised index.
3. Deficit runs in the target quarter; eligibility; ranking.
4. PR replay; contrast.

## 6. Wrong paths (method errors, not misreadings)

**A — PR alarms.** Sensor soiling floods alarms.

**B — raw yield comparison.** Technology differences flagged.

**C — mean instead of median peer.** A failing system pulls the benchmark.

**D — ranking by worst single day.** Transients dominate.

## 7. Why the stump is analytical, not semantic

The index and rules are specified. The trap is relying on a shared reference that can fail, and confounding fixed technology effects
with faults.

## 8. Draft task prompt (prose)

> Which five systems should our technicians visit this quarter? Use the peer-relative method in the O&M memo and compare it with our PR alarms.
> Provide `system_deficits.csv` (system: ρ, run start, run length, mean deficit, score, rank), `peer_index.png` (normalised index for all systems
> with visited ones highlighted), and a one-page `visit_plan.pdf`.

## 9. Deliverables

* `system_deficits.csv`, `peer_index.png`, `visit_plan.pdf`.

## 10. Where 25+ rubric criteria come from

* 5 systems + #6; ρ and run data for 8 systems; PR alarm counts; contrast; exclusions.

## 11. Golden-output checklist

* Specific yield; missing rule; median peer; reference ratio; runs; ranking.

## 12. Build notes (scope tuning)

* Choose a quarter with a known pyranometer soiling period and at least one real system fault.
