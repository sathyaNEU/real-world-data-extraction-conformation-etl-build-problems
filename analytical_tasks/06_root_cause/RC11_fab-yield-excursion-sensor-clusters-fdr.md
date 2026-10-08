# RC11 — A wafer-fab yield excursion and 590 sensors: which three signals does the yield team chase?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Semiconductor and electronics manufacturing yield excursions (Apple, Intel, TSMC supplier quality), and any "which of thousands of metrics moved with the incident" search |
| Domain | Semiconductor manufacturing |
| Task shape | 01 · Ranked list under a cap (the three sensor clusters handed to process engineering, ranked by stratified effect size) |
| Core method | Screen out constant and near-constant sensors; group the remaining sensors into correlation clusters (one physical cause moves many sensors); test each cluster's representative against pass/fail within weekly strata (time is a confounder: the fail rate and many sensors drift together); control the false discovery rate with Benjamini–Hochberg; rank significant clusters by stratified AUC |
| Analytical stump | Testing 590 sensors one by one at p < 0.05 yields dozens of chance "hits", and a single upstream fault floods the top of a sensor-level ranking with near-duplicate signals from one cluster. Worse, the fail rate changed over the observation window, so any sensor that merely drifted over time looks associated with failure. A pooled, unadjusted, sensor-level ranking sends engineers after drift and duplicates |
| Primary sources | UCI Machine Learning Repository — SECOM dataset (McCann & Johnston; 1,567 production runs × 590 sensor measurements, pass/fail label and timestamp) |

## 1. The real-world situation

A fab's in-line test showed a rise in failing lots. The yield team can instrument and audit three signal groups this week. A data scientist
produced a ranked list of the "top 20 sensors by p-value"; the first 11 were the same pressure–flow family, and several others drifted steadily
over the quarter. The yield manager asked for a defensible top-three.

## 2. The decision (one deterministic recommendation)

**The three sensor clusters sent to process engineering, in rank order, each with its representative sensor, cluster members, stratified AUC and
BH-adjusted q-value.**

Rules (yield memo):

* Data: `secom.data` (590 features) and `secom_labels.data` (label −1 pass / 1 fail, timestamp).
* Screening: drop features with > 40% missing, zero variance, or with a single value in ≥ 95% of non-missing runs. Remaining missing values:
  median imputation within the ISO week of the run.
* Clusters: Spearman correlation on screened features; hierarchical clustering, average linkage, distance 1 − |ρ|, cut at 0.2. Representative =
  the member with the fewest missing values (ties: lowest feature index).
* Strata: ISO week of the timestamp; weeks with no failures are dropped from testing.
* Test per cluster: stratified Wilcoxon rank-sum (van Elteren) of the representative, fail vs pass; two-sided p-values.
* FDR: Benjamini–Hochberg at q ≤ 0.10 across clusters.
* Effect size: stratified AUC = Σ_w n_w·AUC_w ÷ Σ_w n_w, where n_w = runs in week w, oriented so that values above 0.5 mean "higher in fails".
* Ranking: FDR-significant clusters by |AUC − 0.5|, descending; ties broken by lower q. Send the top 3.

## 3. Why capable analysts get it wrong

* The search is wide: hundreds of tests guarantee false positives without multiplicity control.
* Physical causes act through many redundant sensors, so a sensor-level ranking repeats one finding.
* The label is not stationary: fail rate varies by week, and so do many sensors (maintenance, recalibration), creating spurious association.
* Missingness is heavy and uneven; imputing with global means blends weeks with different baselines.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `secom.data` | TXT (space-separated) | 1,567 × 590 | UCI ML Repository (SECOM, id 179) | CC BY 4.0 | Sensor measurements |
| 2 | `secom_labels.data` | TXT | 1,567 | Same | CC BY 4.0 | Pass/fail and timestamp |
| 3 | `secom_long.parquet` | Parquet | ~925k (run × feature) | Task author (reshaped from 1–2, no values changed) | CC BY 4.0 | Long format for screening |
| 4 | `secom_description.html` | HTML | — | UCI | CC BY 4.0 | Dataset notes |
| 5 | `yield_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `top20_sensor_pvalues.xlsx` | XLSX | 20 | Task author (naive pooled t-tests on file 1) | — | The data scientist's list |
| 7 | `benjamini_hochberg_1995_citation.pdf` | PDF | — | Cite | Cite | FDR method |

## 5. Deterministic solution path

1. Parse both files; attach ISO week; screen features; impute within week.
2. Spearman matrix; cluster; choose representatives.
3. Stratified tests and AUC per cluster; BH adjustment.
4. Rank significant clusters; take the top 3; list members.
5. Compare with the naive top-20 list: how many of its entries collapse into one cluster, and how many fail the stratified test.

## 6. Wrong paths (method errors, not misreadings)

**A — sensor-level ranking at p < 0.05.** Dozens of false hits; the top of the list is one cluster repeated.

**B — pooled test ignoring week.** Sensors that drifted over the quarter rank highly because the fail rate also moved over time.

**C — Bonferroni on 590 sensors.** Over-conservative on correlated tests; real clusters are lost (and redundancy is not addressed).

**D — global-mean imputation.** Imputed values carry the overall mean into weeks with shifted baselines and dilute or fake effects.

## 7. Why the stump is analytical, not semantic

Features are anonymous, so nothing depends on interpreting sensor names. Every step (screening, clustering, strata, test, FDR, ranking) is
specified. The trap is multiplicity, redundancy and temporal confounding in a wide screen.

## 8. Draft task prompt (prose)

> Yield dropped and the team can chase three signals this week. Use the yield memo's method to give me the three sensor clusters most associated
> with failure, adjusting for time and multiple testing. Provide `cluster_ranking.csv` (cluster: representative, members, stratified AUC, q-value,
> rank), `cluster_effects.png`, and a one-page `excursion_shortlist.pdf`.

## 9. Deliverables

* `cluster_ranking.csv` — every tested cluster, with the top 3 flagged.
* `cluster_effects.png` — stratified AUC by cluster with q-values, top 3 highlighted.
* `excursion_shortlist.pdf` — the three clusters, members, and why the naive top-20 list misleads.

## 10. Where 25+ rubric criteria come from

* Screening counts (missing, constant, near-constant, remaining): 4.
* Number of clusters, representative rule, members of the top 3: 5.
* Weekly strata used and dropped: 2.
* AUC and q-value for each of the top 3, plus rank order: 9.
* BH threshold applied correctly; number significant: 2.
* Naive-list contrast (collapse into clusters, stratified failures): 3+.

## 11. Golden-output checklist

* Screening thresholds exactly as memo; within-week median imputation.
* Spearman, average linkage, cut at 0.2; representative tie-break.
* Van Elteren stratified test; stratified AUC weights; orientation.
* BH at 0.10; ranking by |AUC − 0.5|.

## 12. Build notes (scope tuning)

* Confirm on the actual file that the naive pooled ranking places at least one time-drifting cluster in its top 5 that drops out once tests are
  stratified by week, and that at least 5 of its top 20 sensors fall into one cluster.
