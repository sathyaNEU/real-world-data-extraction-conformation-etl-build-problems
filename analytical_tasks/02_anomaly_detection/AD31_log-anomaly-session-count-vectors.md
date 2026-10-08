# AD31 — Log anomalies: rare lines are not failed jobs; the unit is the session

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Log-analytics teams at cloud and storage providers (distributed file systems, job schedulers) choosing between line-level rarity rules and session-level models |
| Domain | Distributed systems / AIOps |
| Task shape | 07 · Grid of cells (detector × evaluation unit → precision, recall, alerts per day; adopt the detector meeting the memo's bar) |
| Core method | Parse log lines to templates; group by block ID into sessions; event-count matrix (sessions × templates) with TF-IDF weighting; PCA residual (squared prediction error, SPE) with the Q-statistic limit; evaluation at session level with a time-ordered split |
| Analytical stump | Flagging rare templates or ERROR/WARN lines alerts on benign noise and misses failures that consist of ordinary lines in an abnormal *combination or count*. Labels are per block, so evaluating per line inflates both counts and accuracy. Random splits leak sessions' templates across train and test |
| Primary sources | Loghub HDFS_v1 (Hadoop Distributed File System logs with block-level anomaly labels; Xu et al., SOSP 2009) |

## 1. The real-world situation

A storage platform team wants an automated detector for failed block operations. The first attempt raised an alert for any log line
whose template appeared fewer than 100 times in the training week, plus any WARN/ERROR line. On-call engineers received thousands of alerts
a day, and many failed blocks never produced a rare or WARN line.

## 2. The decision (one deterministic recommendation)

**Adopt the session-level PCA detector or keep the line-rarity rule, judged at block level on the later 30% of the log.**

Rules (AIOps memo):

* Parsing: use the provided template file (`HDFS.log_templates.csv`) and the structured log to assign template IDs.
* Sessions: all lines sharing a block ID (`blk_…`); a line naming two blocks belongs to both.
* Split: order sessions by first timestamp; first 70% train, last 30% test.
* Line-rarity rule R: a block is alerted if any of its lines has a template with train frequency < 100 or level WARN/ERROR.
* PCA detector P: count matrix on train blocks labelled normal; TF-IDF weighting and mean-centering per the memo; keep components
  explaining 95% variance; SPE threshold = Q-statistic at α = 0.001 (Jackson–Mudholkar).
* Metrics on test blocks: precision, recall, F1, alerted blocks per day.
* Adopt P if recall ≥ 0.6, precision ≥ 0.8 and alerted blocks per day < 25% of R's.

## 3. Why capable analysts get it wrong

* Line-level heuristics are easy and familiar in log tooling.
* Many failures are visible only in the counts of normal events (a missing "replica added" message).
* Ground truth is per block; per-line metrics count each block many times.
* Random splits put near-identical sessions on both sides, inflating results.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `HDFS.log` | Text | ~11.2M lines | Loghub HDFS_v1 (LogPAI) | Research use (Loghub terms; cite Xu et al. 2009) | Raw logs |
| 2 | `anomaly_label.csv` | CSV | ~575k blocks | Loghub | Same | Block labels |
| 3 | `HDFS.log_templates.csv` | CSV | ~30–50 | Loghub | Same | Templates |
| 4 | `HDFS.log_structured.parquet` | Parquet | ~11.2M | Derived | Same | Parsed lines |
| 5 | `aiops_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `current_rule_alerts_sample.csv` | CSV | ~10k | Task author | — | Line-rule alerts |
| 7 | `xu_2009_sosp_citation.pdf` | PDF | — | Cite | Cite | PCA on event-count vectors |
| 8 | `jackson_mudholkar_q_citation.pdf` | PDF | — | Cite | Cite | SPE threshold |
| 9 | `block_first_seen.csv` | CSV | ~575k | Derived | Same | Split order |
| 10 | `oncall_feedback.json` | JSON | ~20 | Task author | — | Context |

## 5. Deterministic solution path

1. Map lines to templates and blocks; build sessions.
2. Time-ordered split by first-seen.
3. Apply R; build count matrix, TF-IDF, PCA on normal train sessions; SPE and Q threshold.
4. Block-level metrics on test; alerts per day; decision.

## 6. Wrong paths (method errors, not misreadings)

**A — line-level evaluation.** Inflated metrics.

**B — random split.** Leakage.

**C — PCA trained on all sessions including anomalies.** Anomalies absorbed into components.

**D — threshold by eye.** Not reproducible.

## 7. Why the stump is analytical, not semantic

Templates, sessions, detector and metrics are specified. The traps are unit of analysis, feature representation and evaluation design.

## 8. Draft task prompt (prose)

> Should we replace the rare-line alert with the session-level PCA detector in the AIOps memo? Evaluate both per block on the later part of the
> HDFS log. Provide `detector_grid.csv` (detector × metric), `spe_distribution.png` (SPE for normal vs anomalous test blocks with the threshold),
> and a one-page `detector_decision.pdf`.

## 9. Deliverables

* `detector_grid.csv`, `spe_distribution.png`, `detector_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 2 detectors × 4 metrics = 8; components retained; threshold; session counts; split boundary; decision; line-level vs block-level contrast.

## 11. Golden-output checklist

* Template assignment; multi-block lines; split; weighting; PCA on normal train; Q threshold; block metrics.

## 12. Build notes (scope tuning)

* Publish the template mapping to remove parser variance.
* Confirm R's precision < 0.3 and P meets the bar.
