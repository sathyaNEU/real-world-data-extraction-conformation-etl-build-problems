# AD18 — End-of-line test station: seventeen good-looking sensors can still describe a bad unit

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Manufacturing end-of-line and burn-in test stations (consumer electronics, pumps, actuators) moving from per-parameter limits to multivariate screening |
| Domain | Manufacturing quality / test engineering |
| Task shape | 10 · Scorecard against thresholds (fault class × detection test → adopt / reject the multivariate screen) |
| Core method | Phase I reference from healthy cycles; per-cycle features; Hotelling T² on standardized features (PCA retaining 95% variance) with an empirical 99th-percentile limit; comparison with per-sensor 3σ limits |
| Analytical stump | Seventeen univariate 3σ checks raise the false-alarm rate (multiple testing) and still miss faults that shift the *relationships* between sensors (pressure vs flow vs power) while each stays in range. Multivariate distance from the healthy correlation structure catches them |
| Primary sources | UCI "Condition monitoring of hydraulic systems" dataset |

## 1. The real-world situation

A hydraulic-unit manufacturer screens every unit on a 60-second test cycle with 17 sensor channels. Each channel has 3σ limits from
healthy units. Field returns showed units with degraded valves and mild internal leakage passing the test, while the line flagged good
units for retest several times a shift.

## 2. The decision (one deterministic recommendation)

**Adopt the multivariate T² screen or keep per-sensor limits, judged on detection by fault class and false-alarm rate.**

Rules (test engineering memo):

* Features per cycle: mean of each of the 17 sensor channels over the cycle (PS1–PS6, EPS1, FS1–FS2, TS1–TS4, VS1, CE, CP, SE).
* Phase I (healthy): cycles with cooler 100%, valve 100%, no pump leakage, accumulator 130 bar and stable flag = 0; first 70% of them
  (in file order) for estimation, last 30% for false-alarm evaluation.
* Per-sensor rule U: alarm if any feature is outside mean ± 3 SD of Phase I estimation cycles.
* Multivariate rule M: standardize with Phase I means/SDs; PCA on Phase I; keep components reaching 95% variance; T² = Σ score² ÷
  eigenvalue; limit = 99th percentile of Phase I estimation T²; alarm if exceeded.
* Fault classes (each excluding other faults): valve 73%, valve 80%, pump leakage 2, accumulator 90 bar, cooler 3%.
* Adopt M if, for every fault class, detection ≥ 90% and false-alarm rate on the held-out healthy cycles ≤ 2%; otherwise keep U (report
  both).

## 3. Why capable analysts get it wrong

* Per-parameter limits are standard, auditable and familiar to line engineers.
* With 17 checks at 3σ, the chance a good unit fails at least one is much larger than 0.27%, especially with heavy tails.
* Many faults change sensor relationships, not levels; each sensor remains in range.
* Phase I must exclude faulty and unstable cycles, or limits widen.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–6 | `PS1.txt` … `PS6.txt` | TSV | 2,205 × 6,000 | UCI ML Repository (id 447) | CC BY 4.0 | Pressure, 100 Hz |
| 7 | `EPS1.txt` | TSV | 2,205 × 6,000 | Same | CC BY 4.0 | Motor power |
| 8–9 | `FS1.txt`, `FS2.txt` | TSV | 2,205 × 600 | Same | CC BY 4.0 | Flow, 10 Hz |
| 10–13 | `TS1.txt` … `TS4.txt` | TSV | 2,205 × 60 | Same | CC BY 4.0 | Temperatures |
| 14–17 | `VS1.txt`, `CE.txt`, `CP.txt`, `SE.txt` | TSV | 2,205 × 60 | Same | CC BY 4.0 | Vibration, efficiency |
| 18 | `profile.txt` | TSV | 2,205 | Same | CC BY 4.0 | Condition labels, stable flag |
| 19 | `documentation.txt` | Text | — | Same | CC BY 4.0 | Sensor descriptions |
| 20 | `cycle_features.csv` | CSV | 2,205 × 17 | Derived | CC BY 4.0 | Features |
| 21 | `test_engineering_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 22 | `line_retest_log_summary.xlsx` | XLSX | ~20 | Task author | — | Context |

## 5. Deterministic solution path

1. Compute cycle means; label Phase I and fault classes.
2. Estimate U limits and the PCA/T² model on Phase I estimation cycles; T² limit.
3. Evaluate detection per fault class and false alarms on held-out healthy cycles; decide.

## 6. Wrong paths (method errors, not misreadings)

**A — univariate limits only.** Misses relationship faults; high false alarms.

**B — Phase I including faulty/unstable cycles.** Limits too wide.

**C — T² without standardization.** Dominated by high-variance channels.

**D — limits evaluated on the same healthy cycles used to fit.** Optimistic false-alarm rate.

## 7. Why the stump is analytical, not semantic

Features, classes and rules are explicit. The trap is univariate thinking about a multivariate process, plus multiple testing.

## 8. Draft task prompt (prose)

> Should our test station move from per-sensor limits to the multivariate screen? Follow the test engineering memo on the hydraulic rig data:
> build both rules from healthy cycles, test them on each fault class and on held-out healthy cycles, and give me adopt or keep. Provide
> `screen_scorecard.csv` (rule × fault class: detection; false-alarm rate), `t2_chart.png` (T² by cycle with the limit and fault classes
> coloured), and a one-page `test_station_decision.pdf`.

## 9. Deliverables

* `screen_scorecard.csv`, `t2_chart.png`, `test_station_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 2 rules × 5 fault classes = 10 detection rates; 2 false-alarm rates; components retained; T² limit; decision; examples.

## 11. Golden-output checklist

* Correct Phase I selection and split; standardized PCA; empirical limit; per-class evaluation; decision.

## 12. Build notes (scope tuning)

* Check the number of cycles per pure fault class (some combinations are sparse); if a class has < 30 cycles, merge per the memo.
* Publish the feature table to make grading independent of signal processing.
