# DS02 — Which vulnerabilities to patch first: severity scores are not exploitation odds

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Vulnerability-management teams at enterprises and cloud providers choosing a patch-prioritisation policy under limited remediation capacity |
| Domain | Cybersecurity operations |
| Task shape | 04 · Setting one dial (the EPSS probability threshold that fills the team's monthly patch capacity and maximises exploited vulnerabilities covered) |
| Core method | Time-split evaluation: score open CVEs as of a decision date with EPSS (that day's scores) and CVSS; outcome = added to CISA KEV within the following 90 days; coverage (recall) and efficiency (precision) at a fixed capacity of N CVEs; threshold choice for EPSS; comparison with "CVSS ≥ 9.0 first" |
| Analytical stump | Ranking by CVSS severity patches many critical-but-never-exploited flaws. Evaluating EPSS with scores published *after* exploitation became known (look-ahead) inflates it. A fair comparison scores at the decision date and looks forward; capacity, not AUC, defines the policy |
| Primary sources | FIRST Exploit Prediction Scoring System (EPSS) daily score files; CISA Known Exploited Vulnerabilities (KEV) catalog |

## 1. The real-world situation

A security team can remediate about **300** vulnerabilities per month across its estate. It currently patches everything with CVSS ≥ 9.0 first.
A proposal to switch to EPSS was evaluated by checking EPSS scores of KEV-listed CVEs today, which showed near-perfect separation. The CISO asked
for an evaluation that mimics real decision-making.

## 2. The decision (one deterministic recommendation)

**Adopt EPSS-based prioritisation or keep CVSS ≥ 9.0, and the EPSS threshold that yields ~300 CVEs per month, judged on KEV additions in the 90
days after each of 12 monthly decision dates.**

Rules (vulnerability-management memo):

* Decision dates: first day of each month for 12 months (memo).
* Population at each date: CVEs published in the prior 3 years that match the estate's product list (`estate_cpe_list.json`, CPE matching
  against NVD configurations) and are not yet in KEV.
* EPSS policy: CVEs with EPSS score on that date ≥ t; t chosen per date as the score of the 300th-ranked CVE (ties included).
* CVSS policy: CVSS v3 base ≥ 9.0, ordered by score, capped at 300.
* Outcome: CVE added to KEV within 90 days after the decision date.
* Metrics per date: recall = exploited covered ÷ exploited; precision = exploited covered ÷ selected; average over dates.
* Adopt EPSS if mean recall is ≥ 10 percentage points higher than CVSS at equal capacity.

## 3. Why capable analysts get it wrong

* CVSS is the familiar severity standard.
* Looking up today's EPSS for already-exploited CVEs uses information created by the exploitation itself.
* Capacity constraints make precision at N the operational metric.
* KEV additions lag exploitation; a forward window is needed.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–12 | `epss_scores-<yyyy-mm-dd>.csv.gz` (12 decision dates) | CSV | ~230k each | FIRST EPSS | EPSS terms (free use with attribution) | Scores on decision dates |
| 13 | `known_exploited_vulnerabilities.csv` | CSV | ~1.2k | CISA KEV | U.S. Gov public domain | Exploitation outcomes with date added |
| 14 | `nvdcve-cvss.parquet` | Parquet | ~250k | Derived from NVD | Public domain | CVSS v3 base scores |
| 15 | `estate_cpe_list.json` | JSON | ~200 products | Task author (vendor/product list) | — | Estate scope; CVEs derived by CPE matching |
| 16 | `vm_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 17 | `proposal_lookahead_evaluation.xlsx` | XLSX | — | Task author | — | Naive evaluation |
| 18 | `epss_model_citation.pdf` | PDF | — | Jacobs et al. (cite) | Cite | EPSS |

## 5. Deterministic solution path

1. For each decision date, derive estate CVEs by CPE matching, drop those already in KEV; join that date's EPSS and CVSS.
2. Select under each policy with capacity 300; record outcomes in 90 days.
3. Per-date and mean recall/precision; thresholds; decision.
4. Contrast with the look-ahead evaluation.

## 6. Wrong paths (method errors, not misreadings)

**A — look-ahead EPSS.** Inflated performance.

**B — AUC comparison without capacity.** Not decision-relevant.

**C — including CVEs already in KEV at the decision date.** Trivially "predicted".

**D — CVSS ≥ 9.0 without cap.** Unequal capacity comparison.

## 7. Why the stump is analytical, not semantic

The dates, outcomes and policies are specified. The trap is temporal leakage and the capacity-constrained metric.

## 8. Draft task prompt (prose)

> Should we switch patch prioritisation from CVSS to EPSS? Evaluate both at 12 historical decision dates with forward KEV outcomes and our
> 300-per-month capacity, as the vulnerability-management memo specifies. Provide `policy_backtest.csv` (date × policy: selected, exploited covered,
> recall, precision; EPSS threshold), `recall_by_date.png`, and a one-page `prioritisation_decision.pdf`.

## 9. Deliverables

* `policy_backtest.csv`, `recall_by_date.png`, `prioritisation_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 12 dates × 2 policies recall = 24; thresholds; means; decision; look-ahead contrast.

## 11. Golden-output checklist

* Date-specific scores; KEV exclusion; capacity; forward window; metrics; rule.

## 12. Build notes (scope tuning)

* Choose a product list with a realistic enterprise mix; confirm the look-ahead evaluation overstates EPSS recall by ≥ 20 points.
