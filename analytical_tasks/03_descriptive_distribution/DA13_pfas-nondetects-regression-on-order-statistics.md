# DA13 — PFAS in drinking water: what you do with "below reporting limit" decides the answer

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Quality and compliance analytics with detection limits (water utilities, food and pharma labs) and any metric with floor-censored values (latency below timer resolution, assay limits) |
| Domain | Environmental health / water utilities |
| Task shape | 14 · Cuts of a distribution (median, P90 and share above 4.0 ng/L for PFOA and PFOS across system size classes; the class prioritised for treatment grants) |
| Core method | Left-censored data: robust regression on order statistics (ROS) on a log scale with plotting positions accounting for the reporting limit (Helsel); per-system maximum before system-level percentiles; comparison with substitution (zero, MRL/2, MRL) |
| Analytical stump | Most results are non-detects. Substituting zero, half the reporting limit or the limit itself moves percentiles and exceedance shares by large amounts and can change which size class looks worst. ROS uses the detected values' distribution to fill the censored tail consistently |
| Primary sources | U.S. EPA Fifth Unregulated Contaminant Monitoring Rule (UCMR 5) occurrence data |

## 1. The real-world situation

A state revolving fund will prioritise one system size class for PFAS treatment planning grants based on the share of systems with a
maximum PFOA or PFOS concentration above 4.0 ng/L and the class's 90th-percentile system maximum. The first analysis substituted zero for
all non-detects; a second substituted the reporting limit; they disagreed on the priority class.

## 2. The decision (one deterministic recommendation)

**The system size class prioritised for grants, with its estimated share of systems above 4.0 ng/L and P90 system maximum for PFOA and
PFOS.**

Rules (fund memo):

* Data: UCMR 5 results for PFOA and PFOS, all sampling events released as of the memo date; minimum reporting level (MRL) 4.0 ng/L for
  both.
* Size classes: ≤ 3,300; 3,301–10,000; 10,001–100,000; > 100,000 people served (UCMR 5 includes a representative sample of small systems).
* System statistic: maximum result across the system's sampling points and events; a system with all non-detects is censored at the MRL.
* Distribution per class and analyte: ROS on log concentrations of system maxima with censoring at the MRL (Helsel plotting positions);
  percentiles from the combined detected + modelled values.
* Share above 4.0 ng/L = share of systems with a detected maximum ≥ 4.0 (identical under any method, reported) and P90 from ROS.
* Priority score = mean over the two analytes of P90 (ng/L); highest class wins.
* Report substitution results for contrast.

## 3. Why capable analysts get it wrong

* Substitution is quick and common; it is arbitrary and biased.
* With > 80% non-detects in some classes, the P90 may itself be censored; ROS provides a model-based value consistent with detects.
* System-level statistics must be computed before cross-system percentiles; sample-level percentiles overweight systems with many sampling
  points.
* Small-system results come from a sample; the memo uses them as given.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `UCMR5_All.txt` | Tab-delimited text | ~1M results | EPA UCMR 5 data | U.S. Gov public domain | Sample results |
| 2 | `UCMR5_AddtlDataElem.txt` | Text | ~200k | EPA | Public domain | System attributes, population |
| 3 | `UCMR5_ZIPCodes.txt` | Text | ~150k | EPA | Public domain | Context |
| 4 | `ucmr5_data_summary.pdf` | PDF | — | EPA | Public domain | MRLs, field definitions |
| 5 | `fund_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `substitution_analyses.xlsx` | XLSX | 2 × 8 | Task author | — | Earlier analyses |
| 7 | `helsel_ros_citation.pdf` | PDF | — | Helsel, Statistics for Censored Environmental Data (cite) | Cite | ROS |
| 8 | `ros_check_dataset.csv` | CSV | ~30 | Task author (published textbook example) | Cite | Method check |
| 9 | `system_maxima.parquet` | Parquet | ~10k | Derived | Public domain | Convenience |
| 10 | `size_class_bounds.json` | JSON | 4 | Task author | — | Classes |

## 5. Deterministic solution path

1. Filter analytes; compute system maxima with censoring flags; assign classes.
2. ROS per class × analyte; percentiles; exceedance shares.
3. Priority score; choose class.
4. Substitution contrasts; ROS check on the example dataset.

## 6. Wrong paths (method errors, not misreadings)

**A — zero substitution.** Understates P90.

**B — MRL substitution.** Overstates.

**C — sample-level percentiles.** Large systems overweighted.

**D — ROS on linear scale.** Misfit.

## 7. Why the stump is analytical, not semantic

The censoring limit and method are specified. The trap is handling censored observations in distributional statistics.

## 8. Draft task prompt (prose)

> Which system size class should the fund prioritise for PFAS planning grants? Use UCMR 5 system maxima and the ROS method in the fund memo.
> Provide `class_distribution.csv` (class × analyte: systems, % non-detect, share ≥ 4.0, P50, P90 by ROS and by substitution), `censored_qq.png`
> (ROS fits by class), and a one-page `grant_priority.pdf`.

## 9. Deliverables

* `class_distribution.csv`, `censored_qq.png`, `grant_priority.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 classes × 2 analytes × (share, P50, P90) = 24; priority score; substitution contrasts; method check.

## 11. Golden-output checklist

* System maxima; censoring flags; ROS plotting positions; log scale; class scores; choice.

## 12. Build notes (scope tuning)

* Freeze the release date of UCMR 5 results; confirm zero and MRL substitution pick different classes.
