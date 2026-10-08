# AD16 — Choosing a telemetry anomaly detector: the benchmark metric that makes a clock look clever

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | AIOps and spacecraft/industrial telemetry teams evaluating anomaly detectors (vendor claims built on inflated benchmark metrics) |
| Domain | Mission operations / observability |
| Task shape | 07 · Grid of cells (detector × evaluation metric → score; adopt by the operations-relevant metric) |
| Core method | Event-level evaluation of alarms against labelled anomaly segments (alarm grouping, segment hit, false events per day), compared with point-wise and point-adjusted F1 |
| Analytical stump | Point-adjusted scoring marks a whole anomaly segment as detected if any single point inside it alarms; long segments make even a trivial periodic alarm score highly. Point-wise F1 penalizes detectors for not alarming on every point of a segment. Only event-level scoring reflects how operators experience detectors |
| Primary sources | NASA SMAP and MSL telemetry anomaly dataset (Hundman et al., KDD 2018) |

## 1. The real-world situation

A satellite operator is choosing an anomaly detector for spacecraft telemetry. A vendor's deck reports a point-adjusted F1 of 0.93 on the
public SMAP/MSL benchmark. The operations lead asked how a detector that triggers every few hundred samples would score under the same
metric.

## 2. The decision (one deterministic recommendation)

**Which detector to adopt — the one with the highest event-level F1 across all channels — and how each candidate (including a trivial
periodic detector) scores under the three metrics.**

Rules (evaluation memo):

* Data: the test series of all 82 channels with the labelled anomaly sequences; only the telemetry value (first dimension) is used.
* Detectors: D0 periodic (alarm at every 250th timestep); D1 rolling z-score (window 250, |z| > 4); D2 robust first-difference score
  (|Δx − median| ÷ (1.4826 · MAD) over the training series > 6); D3 = D1 or D2.
* Event-level scoring: consecutive alarms within 10 timesteps form one alarm event; a labelled segment is detected if any alarm event
  overlaps it; event precision = alarm events overlapping any labelled segment ÷ all alarm events; event recall = detected segments ÷
  all segments; F1 from these.
* Point-wise F1 and point-adjusted F1 computed in the standard way for comparison.
* Adopt the detector with the highest event-level F1 (pooled over channels).

## 3. Why capable analysts get it wrong

* Published benchmarks often report point-adjusted F1; it is the number in the vendor's slide.
* Long labelled segments reward sparse, random-like alarms under point adjustment.
* Point-wise metrics penalize sensible detectors that alarm at onset only.
* Operators care about alarm events per day and whether each anomaly was caught — an event view.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `data/train/*.npy` (82 channels) | NumPy arrays | ~2k–3k timesteps each | NASA SMAP/MSL dataset (telemanom release) | Public release (verify terms) | Training series |
| 2 | `data/test/*.npy` (82 channels) | NumPy arrays | ~3k–9k timesteps each | Same | Same | Test series |
| 3 | `labeled_anomalies.csv` | CSV | 82 | Same | Same | Anomaly sequences per channel |
| 4 | `test_values_long.parquet` | Parquet | ~600k | Derived | Same | Long format (channel, t, value, label) |
| 5 | `hundman_2018_kdd.pdf` (citation) | PDF | — | KDD 2018 (cite) | Cite | Dataset description |
| 6 | `kim_2022_rigorous_evaluation.pdf` (citation) | PDF | — | AAAI 2022 (cite) | Cite | Point-adjust critique |
| 7 | `evaluation_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `vendor_benchmark_slide.pdf` | PDF | — | Task author | — | Claimed PA-F1 |
| 9 | `channel_metadata.csv` | CSV | 82 | Derived | Same | Spacecraft, channel type |
| 10 | `scoring_reference_cases.json` | JSON | — | Task author | — | Toy cases to validate scorers |

## 5. Deterministic solution path

1. Implement D0–D3 exactly; produce alarm series for every channel.
2. Implement event grouping and the three metrics; validate on the reference cases.
3. Pool across channels; fill the 4 × 3 grid; adopt by event F1.

## 6. Wrong paths (method errors, not misreadings)

**A — adopt by point-adjusted F1.** A trivial or noisy detector looks competitive.

**B — adopt by point-wise F1.** Penalizes onset-only detectors; wrong choice.

**C — per-channel averages vs pooled counts mixed.** Inconsistent metrics.

**D — training data used for thresholds of D1 at test time** incorrectly (look-ahead into test windows).

## 7. Why the stump is analytical, not semantic

Detectors and metrics are fully specified. The trap is the evaluation protocol — what a metric rewards — a methodological issue.

## 8. Draft task prompt (prose)

> Before we buy, evaluate the candidate detectors on the SMAP/MSL benchmark the way operations will experience them, per the evaluation memo,
> and show how the vendor's metric would rank them — including a detector that just alarms periodically. Provide `metric_grid.csv`
> (detector × metric), `alarm_examples.png` (two channels with segments and each detector's alarms), and a one-page
> `detector_selection.pdf`.

## 9. Deliverables

* `metric_grid.csv`, `alarm_examples.png`, `detector_selection.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 detectors × 3 metrics = 12 scores; event precision/recall (8); adopted detector; D0's PA-F1 vs event F1; reference-case checks.

## 11. Golden-output checklist

* Exact detector definitions; event grouping; overlap rule; pooled metrics; adoption.

## 12. Build notes (scope tuning)

* Confirm D0 achieves a high point-adjusted F1 (it typically does with long segments) and a low event F1.
* Pin the dataset release (some channels' labels were revised by the community).
