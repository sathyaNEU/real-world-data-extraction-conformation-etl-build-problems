# AD12 — Detecting attacks on a backbone link: volume spikes are mostly flash crowds, scans hide in the distribution

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Network-equipment and DDoS-protection vendors detecting floods and scans on provider links |
| Domain | Network security / traffic engineering |
| Task shape | 07 · Grid of cells (detector × attack class → recall, false-alarm rate; adopt the detector best on the operator's criterion) |
| Core method | Per-minute traffic features from packet headers (packets, bytes, flows, Shannon entropies of source/destination addresses and ports), robust baselines, evaluation against community anomaly labels at event level |
| Analytical stump | Volume thresholds catch big floods but also fire on benign heavy hitters, and miss scans and low-rate floods that barely change volume; attacks change the *distribution* of addresses and ports (entropy) far more than the total. Evaluating per minute rather than per event distorts recall |
| Primary sources | MAWI Working Group Traffic Archive (samplepoint-F), MAWILab anomaly labels |

## 1. The real-world situation

A transit provider's security team wants an anomaly detector on a backbone link that catches scans and floods without paging on every
big legitimate transfer. Its current rule — alert when packets per second exceed the 99th percentile of the past week — alerted mostly on
backups and software-update bursts, and missed port scans entirely.

## 2. The decision (one deterministic recommendation)

**Which detector to deploy: the one with the highest event recall for attack-labelled events while keeping false-alarm minutes ≤ 2%
of minutes, evaluated on the evaluation month.**

Rules (security engineering memo):

* Traces: daily 15-minute MAWI samplepoint-F traces; calibration = 20 days, evaluation = the following 30 days.
* Features per 10-second bin: packets, bytes, distinct flows, entropy of src IP, dst IP, src port, dst port.
* Detectors: D1 packets > calibration P99; D2 any entropy feature beyond median ± 4 × MAD of calibration (robust z); D3 = D2 restricted
  to ≥ 3 consecutive bins; D4 = D1 or D3.
* Ground truth: MAWILab events labelled "anomalous" (attack-type heuristics) mapped to time intervals; an event is detected if any
  detector alarm overlaps it; false-alarm time = alarm bins not overlapping any anomalous or suspicious event.
* Adopt the detector with the highest event recall subject to false-alarm time ≤ 2%; ties → lower false-alarm time.

## 3. Why capable analysts get it wrong

* Volume is the most intuitive signal and dashboards show it; many attacks are small relative to backbone volume.
* Entropy captures concentration/dispersion changes (one target, many sources; one source, many ports) that define attacks.
* Non-robust baselines (mean ± 3 SD) are dragged by heavy-tailed traffic.
* Scoring per bin rewards detectors that alarm long on one event; scoring per event reflects what operators care about.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–50 | `YYYYMMDD1400.pcap.gz` (50 daily traces) | PCAP (anonymized headers) | millions of packets each | MAWI Traffic Archive (WIDE) | Free for research (verify terms) | Packet headers |
| 51 | `features_10s_bins.parquet` | Parquet | ~4.5k bins per day × 50 | Derived | Same | Feature table |
| 52–53 | `mawilab_YYYYMMDD_anomalous_suspicious.csv` (50 days, combined into one file) | CSV | ~50k events | MAWILab | Free for research | Labels |
| 54 | `mawilab_documentation.pdf` (citation) | PDF | — | MAWILab paper (CoNEXT 2010) | Cite | Label semantics |
| 55 | `lakhina_entropy_anomalies_citation.pdf` | PDF | — | SIGCOMM 2005 (cite) | Cite | Entropy features |
| 56 | `security_engineering_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 57 | `current_volume_rule_results.xlsx` | XLSX | ~30 | Task author | — | Existing rule |

## 5. Deterministic solution path

1. Parse traces into 10-second features; build calibration baselines (P99, medians, MADs).
2. Run D1–D4 on evaluation days; map alarms to label intervals.
3. Event recall by attack class and overall; false-alarm time; select the detector.

## 6. Wrong paths (method errors, not misreadings)

**A — volume only.** Low recall on scans; false alarms on heavy hitters.

**B — mean ± 3 SD.** Unstable baselines.

**C — per-bin scoring.** Favours long alarms.

**D — calibrating on evaluation days.** Look-ahead.

## 7. Why the stump is analytical, not semantic

Features, detectors and scoring are specified. The trap is choosing the signal (volume vs distribution) and the evaluation unit.

## 8. Draft task prompt (prose)

> Pick the detector we deploy on the backbone link, as the security engineering memo describes: calibrate on 20 days of MAWI traces, run
> the four detectors on the next 30 days, score them against the MAWILab labels at event level, and choose the best within the 2%
> false-alarm budget. Provide `detector_grid.csv` (detector × attack class: recall; false-alarm time), `feature_timeline.png` for one day
> showing volume and entropies with labelled events, and a one-page `detector_decision.pdf`.

## 9. Deliverables

* `detector_grid.csv`, `feature_timeline.png`, `detector_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 detectors × ~5 attack classes recall = 20; false-alarm times (4); adopted detector; volume-rule contrast.

## 11. Golden-output checklist

* Correct binning; robust baselines; persistence rule; event-level overlap scoring; budget constraint.

## 12. Build notes (scope tuning)

* Choose a period with diverse labelled anomalies (scans, floods) and confirm D1 is not selected.
* Document MAWILab label filtering (which heuristics count as attacks).
