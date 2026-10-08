# OS14 — Sizing loss avoided by a security control: the mean breach is driven by a handful of giants

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Security and resilience investment cases (MFA rollout, backup programmes, DDoS protection) sized from incident data with extreme tails |
| Domain | Cybersecurity / healthcare |
| Task shape | 13 · Scenarios and the flip point (control effectiveness × breach-cost-per-record scenarios → expected annual loss avoided versus the control's cost; the go/no-go and the flip point) |
| Core method | Breach size distribution (individuals affected) for the relevant attack type: empirical body plus generalised Pareto tail above the memo's threshold (MLE); frequency per covered entity per year; expected annual loss = frequency × E[size] × cost per record, with E[size] from the fitted mixture (finite only if ξ < 1); scenario grid and flip point |
| Analytical stump | Using the median breach size understates expected loss by orders of magnitude; using the sample mean is dominated by a few mega-breaches and is unstable. A fitted tail (with the shape parameter checked) gives a defensible expectation and shows how sensitive the business case is to the tail |
| Primary sources | U.S. HHS Office for Civil Rights breach portal (breaches of unsecured protected health information affecting 500+ individuals) |

## 1. The real-world situation

A hospital network weighs a $6M-per-year programme (MFA and email hardening) that the vendor says prevents 60% of hacking/IT incidents.
The CISO's analyst sized loss avoided using the median breach size and found the programme not worth it; the CFO's analyst used the mean
and found it overwhelmingly worth it.

## 2. The decision (one deterministic recommendation)

**Go or no-go on the programme under the central scenario (effectiveness 60%, $165 per record), and the effectiveness at which expected loss
avoided equals the programme cost.**

Rules (risk memo):

* Data: OCR breach portal records (archive + under investigation) 2015–2024; type "Hacking/IT Incident"; covered entity type "Healthcare
  Provider".
* Frequency: breaches per provider-year for providers of the network's size class = count ÷ number of hospitals (from `hospital_counts.json`) ×
  the network's hospital count (memo).
* Size distribution: individuals affected; threshold u = 95th percentile; GPD fitted to excesses by MLE; mixture mean = empirical mean below u
  × P(below) + (u + σ ÷ (1 − ξ)) × P(above), valid for ξ < 1.
* Expected annual loss = frequency × mixture mean × cost per record.
* Avoided = effectiveness × expected annual loss. Go if avoided ≥ $6M.
* Scenario grid: effectiveness {40, 60, 80}% × cost per record {$100, $165, $250}; flip-point effectiveness at the central cost.

## 3. Why capable analysts get it wrong

* Medians are robust but irrelevant for expected cost.
* Sample means are dominated by rare mega-breaches and change with one new record.
* A fitted tail makes the expectation explicit and testable (ξ estimate).
* Frequency must be per entity, not total breaches nationally.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `breach_report_archive.csv` | CSV | ~5k | HHS OCR breach portal | U.S. Gov public domain | Archived breaches |
| 2 | `breach_report_under_investigation.csv` | CSV | ~800 | HHS OCR | Public domain | Open cases |
| 3 | `hospital_counts.json` | JSON | — | Task author (from AHA/CMS public counts; cite) | Public | Exposure |
| 4 | `risk_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `ciso_median_case.xlsx` | XLSX | — | Task author | — | Median-based case |
| 6 | `cfo_mean_case.xlsx` | XLSX | — | Task author | — | Mean-based case |
| 7 | `cost_per_record_citation.pdf` | PDF | — | Cite (industry breach-cost studies) | Cite | Cost scenarios |
| 8 | `gpd_fit_check.json` | JSON | — | Task author | — | Check values from a published worked example |

## 5. Deterministic solution path

1. Combine files; filter type and entity; years.
2. Frequency per provider-year; scale to the network.
3. Threshold; GPD fit; ξ check; mixture mean.
4. Expected loss; avoided; scenario grid; flip point; decision.

## 6. Wrong paths (method errors, not misreadings)

**A — median-based sizing.** No-go by understatement.

**B — sample mean.** Dominated by mega-breaches; unstable.

**C — national frequency without exposure.** Wrong scale.

**D — ignoring ξ ≥ 1 possibility.** Infinite-mean tail unflagged.

## 7. Why the stump is analytical, not semantic

The filters, fit and formulas are specified. The trap is estimating expectations under heavy tails.

## 8. Draft task prompt (prose)

> Is the $6M security programme worth it? Size expected annual loss avoided from the OCR breach data with the fitted-tail method in the risk memo,
> and show the scenarios and flip point. Provide `loss_scenarios.csv` (effectiveness × cost per record: avoided loss), `breach_size_tail.png`, and a
> one-page `programme_decision.pdf`.

## 9. Deliverables

* `loss_scenarios.csv`, `breach_size_tail.png`, `programme_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* Frequency; u, σ, ξ; mixture mean; 9 scenario cells; decision; flip point; median/mean contrasts.

## 11. Golden-output checklist

* Filters; exposure; threshold; GPD MLE; mixture mean; grid; flip point.

## 12. Build notes (scope tuning)

* Freeze the portal download date; confirm the median and mean cases fall on opposite sides of the decision while the fitted case is decisive.
