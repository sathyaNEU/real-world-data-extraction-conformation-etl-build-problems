# DS33 — Choosing referral hospitals for heart surgery: raw mortality punishes the hospitals that take the sickest patients

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Vendor or partner selection where performance depends on case mix (contact centres handling hard tickets, contractors on difficult sites, lenders with riskier borrowers) |
| Domain | Healthcare purchasing / centres of excellence |
| Task shape | 01 · Ranked list under a cap (4 hospitals designated as centres of excellence for isolated CABG) |
| Core method | Use risk-adjusted mortality rates (observed ÷ expected × statewide rate) with 95% confidence intervals from the state's cardiac surgery reports; designate hospitals whose upper CI bound is below the statewide rate, ranked by RAMR; volume floor; compare with raw (observed) mortality ranking |
| Analytical stump | Raw mortality rates rank hospitals that operate on lower-risk patients as best; Simpson's paradox can make a hospital better in every risk stratum yet worse overall. Risk adjustment and uncertainty (small numbers of deaths) change the designated set |
| Primary sources | New York State Department of Health Cardiac Surgery Reports (hospital-level CABG volumes, observed and expected mortality, RAMR and CIs; health.data.ny.gov) |

## 1. The real-world situation

A self-insured employer designates centres of excellence for coronary artery bypass grafting (CABG) and offers employees travel benefits to use
them. The benefits consultant ranked hospitals by raw in-hospital/30-day mortality and recommended the top four. A cardiologist pointed out that two
of them operate on far fewer high-risk patients.

## 2. The decision (one deterministic recommendation)

**The 4 designated hospitals (RAMR upper 95% CI < statewide mortality rate and ≥ 300 cases over the reporting period, ranked by RAMR), and the
hospitals in the consultant's list that fail the criterion.**

Rules (benefits memo):

* Data: NYS cardiac surgery hospital-level data for isolated CABG for the latest 3-year reporting period available.
* Fields: cases, observed deaths, observed mortality rate, expected mortality rate, RAMR, 95% CI (as published).
* Eligibility: ≥ 300 cases.
* Designate: RAMR upper CI < statewide observed mortality; rank by RAMR; top 4; if fewer than 4 qualify, designate those that qualify only.
* Contrast: raw observed mortality ranking among eligible hospitals.

## 3. Why capable analysts get it wrong

* Raw mortality is intuitive and widely quoted.
* Patient risk differs between hospitals; expected mortality captures it.
* Small death counts produce wide intervals; point rankings overinterpret noise.
* Simpson's paradox is common when mix differs strongly.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Cardiac_Surgery_and_PCI_by_Hospital_Beginning_2008.csv` | CSV | ~3k rows (hospital × procedure × period) | NYS DOH (health.data.ny.gov) | NY open data terms (public) | Volumes, observed/expected, RAMR, CIs |
| 2 | `Cardiac_Surgery_by_Surgeon.csv` | CSV | ~5k | NYS DOH | Public | Context |
| 3 | `nys_cardiac_report_methodology.pdf` | PDF | — | NYS DOH Adult Cardiac Surgery report | Public | Risk model |
| 4 | `benefits_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `consultant_raw_ranking.xlsx` | XLSX | ~40 | Task author | — | Naive list |
| 6 | `simpsons_paradox_example.json` | JSON | — | Task author (from published risk-stratum tables) | — | Illustration |

## 5. Deterministic solution path

1. Filter procedure and period; eligibility.
2. Apply designation rule; rank; select.
3. Contrast with raw ranking; list failures.

## 6. Wrong paths (method errors, not misreadings)

**A — raw mortality.** Case-mix confounding.

**B — RAMR point estimate without CI rule.** Noise-driven picks.

**C — mixing CABG with valve or PCI.** Wrong procedure group.

**D — ignoring the volume floor.** Small hospitals selected.

## 7. Why the stump is analytical, not semantic

The measures and rules are published and specified. The trap is comparing outcomes without risk adjustment and uncertainty.

## 8. Draft task prompt (prose)

> Which hospitals should we designate as CABG centres of excellence? Apply the risk-adjusted rule in the benefits memo to the NYS cardiac data and
> compare with the consultant's raw ranking. Provide `hospital_designation.csv` (hospital: cases, observed, expected, RAMR, CI, designated),
> `ramr_intervals.png`, and a one-page `centres_of_excellence.pdf`.

## 9. Deliverables

* `hospital_designation.csv`, `ramr_intervals.png`, `centres_of_excellence.pdf`.

## 10. Where 25+ rubric criteria come from

* Designated set; RAMR and CI for 10 hospitals; statewide rate; consultant failures; volume exclusions.

## 11. Golden-output checklist

* Procedure/period filters; eligibility; CI rule; ranking; contrast.

## 12. Build notes (scope tuning)

* Confirm at least two of the consultant's four fail the CI rule.
