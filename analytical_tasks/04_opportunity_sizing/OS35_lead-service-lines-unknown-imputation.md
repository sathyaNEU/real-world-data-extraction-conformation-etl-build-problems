# OS35 — How many lead pipes are there? "Unknown" is not "not lead"

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Remediation sizing with incomplete inventories (devices with unknown firmware, assets with unknown condition, accounts with unknown compliance status) |
| Domain | Water utilities / public health infrastructure |
| Task shape | 03 · Bridge between two totals (known lead and galvanised-requiring-replacement lines → expected total replacements including unknowns; the replacement programme budget) |
| Core method | Predict the probability that an unknown-material line is lead or galvanised-requiring-replacement from verified lines (logistic model on building age band, utility, neighbourhood and line size, per memo); calibrate on held-out verified lines; expected replacements = known + Σ predicted probabilities for unknowns; cost = expected count × unit cost |
| Analytical stump | Budgeting only known lead lines ignores that a large share of the inventory is "unknown", concentrated in older housing where lead is likely. Assuming all unknowns are lead overstates. The expected count requires calibrated probabilities from verified lines, not the overall known-lead share applied uniformly |
| Primary sources | Michigan EGLE public water supply distribution system materials inventories (preliminary/complete inventories by community water supply) |

## 1. The real-world situation

A state revolving fund budgets lead service line replacement across its community water systems. The first estimate counted lines reported as
lead or galvanised-requiring-replacement; a second assumed all unknowns were lead. The two differed by a factor of four.

## 2. The decision (one deterministic recommendation)

**The expected total number of service lines requiring replacement across the systems in scope and the 10-year programme budget at the memo's
unit cost, with the bridge from known lines.**

Rules (fund memo):

* Data: inventories for the systems in scope (latest submission); line-level or system-level counts by material category (lead, GRR,
  non-lead, unknown) and by building age band where provided.
* Verified training set: systems with line-level data and verification flags (field-verified materials) per memo.
* Model: logistic regression P(lead or GRR) on building age band, system size class and region (memo's variables); fit on 70% of verified
  lines, calibrate (Platt) on 30%.
* For systems with only aggregated unknown counts by age band: apply the model's band-level probabilities.
* Expected replacements = known (lead + GRR) + Σ unknown × p.
* Budget = expected × $9,500 (memo) over 10 years.
* Bridge: known → expected from unknowns → total; report "all unknowns lead" and "unknowns zero" bounds.

## 3. Why capable analysts get it wrong

* Reported counts look like the answer.
* Unknown status correlates with age and risk; it is not missing at random.
* Applying the overall known share to unknowns ignores that unknowns are older on average.
* Calibration matters for expected counts (sum of probabilities).

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `egle_dsmi_summary_<year>.xlsx` | XLSX | ~1.4k systems | Michigan EGLE | Public (state public records) | System-level material counts |
| 2 | `egle_dsmi_line_level_<systems>.csv` | CSV | ~500k lines (systems with line-level submissions) | Michigan EGLE / utility submissions | Public | Line-level materials, verification |
| 3 | `parcel_year_built.csv` | CSV | ~500k | County assessor open data (where available) | Public | Building age |
| 4 | `dsmi_guidance.pdf` | PDF | — | Michigan EGLE | Public | Material categories |
| 5 | `fund_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `first_estimates.xlsx` | XLSX | 2 | Task author | — | Known-only and all-unknown estimates |
| 7 | `model_spec.json` | JSON | — | Task author | — | Variables, split seed |
| 8 | `epa_lcri_inventory_guidance_citation.pdf` | PDF | — | U.S. EPA (cite) | Public domain | Context |

## 5. Deterministic solution path

1. Assemble verified lines with attributes; fit and calibrate the model.
2. Predict probabilities for unknowns (line-level or band-level).
3. Expected replacements; bridge; budget; bounds.
4. Contrast with first estimates.

## 6. Wrong paths (method errors, not misreadings)

**A — known lines only.** Understated.

**B — all unknowns lead.** Overstated.

**C — overall known share applied to unknowns.** Ignores age mix.

**D — uncalibrated scores summed.** Biased expected count.

## 7. Why the stump is analytical, not semantic

Categories, model and conversion are specified. The trap is treating unknowns as either zero or worst case rather than estimating them.

## 8. Draft task prompt (prose)

> How many service lines will need replacing, and what should the 10-year budget be? Estimate unknown materials with the calibrated model in the
> fund memo. Provide `replacement_bridge.csv` (step: lines), `probability_by_age.png`, and a one-page `lslr_budget.pdf`.

## 9. Deliverables

* `replacement_bridge.csv`, `probability_by_age.png`, `lslr_budget.pdf`.

## 10. Where 25+ rubric criteria come from

* Bridge steps; probabilities by 6 age bands; calibration metrics; budget; bounds; contrast; system-level values for 8 systems.

## 11. Golden-output checklist

* Training set; split; calibration; band application; sum of probabilities; budget.

## 12. Build notes (scope tuning)

* Record inventory submission dates; confirm the expected total lies between bounds and far from both first estimates.
