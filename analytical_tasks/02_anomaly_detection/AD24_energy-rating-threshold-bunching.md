# AD24 — Energy certificates that land just above the legal minimum: bunching, not a spike detector

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Integrity analytics wherever a score has a pass mark: emissions and safety inspections, energy ratings, credit-score cut-offs, seller-quality thresholds on marketplaces |
| Domain | Housing / energy regulation |
| Task shape | 01 · Ranked list under a cap (15 local authorities for an assessor-audit programme) |
| Core method | Bunching estimator: fit a polynomial counterfactual to the score distribution excluding a window around the threshold, with round-number dummies; excess mass just above the threshold; difference against the non-rental (sales) distribution in the same authority |
| Analytical stump | Every score histogram has spikes at round numbers and natural lumps; a raw "spike at 39" test flags them. Manipulation shows as *excess mass above* and *missing mass below* the pass mark, only for the population the rule binds (private rentals after the minimum standard), measured against a counterfactual that excludes the manipulation window |
| Primary sources | Energy Performance of Buildings Register — domestic EPC bulk data (England and Wales) |

## 1. The real-world situation

Since 2018, privately rented homes in England and Wales must have an energy rating of E or better (SAP score ≥ 39) to be let. A regulator
funds audits of energy assessors in **15** local authorities. An analyst ranked authorities by the share of rental certificates scoring
exactly 39–41. Scheme managers pointed out that some authorities simply have many homes near band E/F, and that SAP scores heap at
round numbers.

## 2. The decision (one deterministic recommendation)

**The 15 local authorities selected for audit, ranked by excess bunching of private-rental certificates above the E/F threshold, and the
16th.**

Rules (audit memo):

* Certificates: domestic EPCs lodged 2019-01-01 to 2023-12-31; keep the latest certificate per building reference number per transaction
  type; scores 1–100.
* Populations: R = transaction type "rental (private)"; S = "marketed sale".
* For each authority and population, bin by integer score. Fit a degree-7 polynomial plus dummies for scores divisible by 5 and by 10 to
  counts excluding the window 35–43. Excess mass B = Σ(observed − predicted) over 39–43; missing mass M = Σ(predicted − observed) over
  35–38.
* Normalized bunching b = B ÷ (average predicted count per score in 39–43).
* Score per authority = b_R − b_S; eligible if R has ≥ 2,000 certificates and M_R > 0.
* Rank by score; top 15; report #16.

## 3. Why capable analysts get it wrong

* Share-in-a-band metrics confuse the location of the distribution with manipulation.
* Round-number heaping is an assessor habit unrelated to the threshold; without dummies, the counterfactual is biased.
* The counterfactual must exclude the manipulated window, otherwise the polynomial bends toward the bunch and hides it.
* Sales certificates in the same authority control for housing stock; the rule does not bind them.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–20 | `domestic-<LA code>-<LA name>/certificates.csv` (20 authorities in scope) | CSV | 30k–200k each | EPC Register bulk download (DLUHC) | Open Government Licence v3 for non-address data (address data under register terms) | Certificates |
| 21 | `columns.csv` (register schema) | CSV | ~90 | EPC Register | OGL | Field definitions |
| 22 | `sap_band_thresholds.json` | JSON | 7 | From SAP methodology | OGL (cite) | Band boundaries |
| 23 | `mees_regulations_summary.pdf` | PDF | — | GOV.UK guidance (cite) | OGL | Legal context |
| 24 | `audit_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 25 | `analyst_band_share_ranking.xlsx` | XLSX | 20 | Task author | — | Naive ranking |
| 26 | `bunching_estimator_citation.pdf` | PDF | — | Kleven (2016) survey (cite) | Cite | Method |
| 27 | `authority_lookup.csv` | CSV | ~330 | ONS (OGL) | OGL | Codes and names |

## 5. Deterministic solution path

1. Load, de-duplicate per building reference and transaction type, filter dates.
2. Build integer-score histograms per authority × population.
3. Fit the counterfactual excluding 35–43 with round-number dummies; compute B, M, b.
4. Score = b_R − b_S; eligibility; rank; top 15 + #16.
5. Compare with the band-share ranking.

## 6. Wrong paths (method errors, not misreadings)

**A — share of certificates at 39–41.** Flags authorities with many near-threshold homes.

**B — no round-number dummies.** Counterfactual biased by heaping at 40.

**C — fitting the counterfactual through the window.** Bunching absorbed into the fit.

**D — no sales control.** Housing-stock differences remain.

## 7. Why the stump is analytical, not semantic

The threshold, populations and estimator are specified. The trap is distinguishing threshold manipulation from distribution shape and
heaping — an estimation problem.

## 8. Draft task prompt (prose)

> Which 15 authorities should our assessor audits cover? Following the audit memo, estimate bunching of private-rental EPC scores just above
> the E/F threshold against a counterfactual that excludes the threshold window, net of the same estimate for sales, and rank the
> authorities. Provide `bunching_ranking.csv` (authority: B, M, b for rentals and sales, score, rank), `bunching_example.png` (observed vs
> counterfactual for the top authority and for the analyst's top authority), and a one-page `audit_selection.pdf`.

## 9. Deliverables

* `bunching_ranking.csv`, `bunching_example.png`, `audit_selection.pdf`.

## 10. Where 25+ rubric criteria come from

* 15 authorities + #16; b_R and b_S for 6 authorities; eligibility exclusions; overlap with the naive ranking.

## 11. Golden-output checklist

* Correct de-duplication; window and degree; dummies; normalization; score; eligibility; ranking.

## 12. Build notes (scope tuning)

* Select 20 authorities including some with large stocks near band E (high naive share, low bunching) and some with clear rental-only
  bunching.
* Record the register download date; certificates can be cancelled or superseded.
