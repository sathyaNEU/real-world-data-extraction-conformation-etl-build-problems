# OS50 — Valuing a salary-sacrifice benefit: the saving depends on the marginal rate, not the average rate

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Pricing or valuing benefits whose worth depends on a customer's marginal position (tax brackets, tiered pricing, loyalty tiers, marginal cost of capital) |
| Domain | Employee benefits / personal tax |
| Task shape | 14 · Cuts of a distribution (taxpayers by marginal-rate band × income decile → annual tax saving from a $12,000 pre-tax lease deduction; the income threshold above which the product is marketed) |
| Core method | From a sample of individual returns, compute each taxpayer's taxable income and marginal tax rate (including Medicare levy) at the relevant schedule; saving from a pre-tax deduction D = tax(T) − tax(T − D) (crossing brackets handled exactly); weighted (sample weight) distribution of savings by decile; threshold where median saving ≥ the product's fee |
| Analytical stump | Using average tax rates (tax ÷ income) understates the saving for those near bracket tops and overstates for those just above thresholds; using a single top marginal rate overstates. The deduction can cross bracket boundaries; exact recomputation is required. Marketing thresholds change accordingly |
| Primary sources | Australian Taxation Office (ATO) Individuals sample file (2% sample of individual tax returns) |

## 1. The real-world situation

A novated-lease provider markets EV salary-packaging to employees. Its calculator used each customer's average tax rate to estimate savings, and
marketing targeted everyone earning above $60,000. Analysts pointed out that the saving depends on the marginal rate and on whether the deduction
moves a person into a lower bracket.

## 2. The decision (one deterministic recommendation)

**The taxable-income threshold (rounded to the nearest $5,000) above which the weighted median annual tax saving from a $12,000 pre-tax deduction
exceeds the product's $2,200 annual fee, with savings by decile.**

Rules (product memo):

* Data: ATO individuals sample file for the income year in memo; weight = 50 (2% sample) per record; residents only; taxable income > 0.
* Tax schedule: resident rates for the year plus 2% Medicare levy (low-income thresholds per memo); ignore offsets except the memo's LITO.
* Saving per person = tax(TI) − tax(max(0, TI − 12,000)) computed exactly.
* Deciles of taxable income (weighted); median saving per decile.
* Threshold: lowest $5,000 band boundary where the weighted median saving among taxpayers above it ≥ $2,200 (memo's search).
* Report average-rate-based savings for contrast.

## 3. Why capable analysts get it wrong

* Average tax rates are easy to compute from totals.
* Deductions save at the marginal rate, which differs from the average.
* Bracket crossing and offsets create nonlinearities.
* Sample weights scale counts but don't change medians here; consistency matters for totals.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `2pc_individuals_sample_file_<year>.csv` | CSV | ~270k records | ATO (data.gov.au) | CC BY 2.5 AU | Sample returns |
| 2 | `individuals_sample_file_data_dictionary.xlsx` | XLSX | — | ATO | CC BY 2.5 AU | Variables |
| 3 | `resident_tax_rates_<year>.json` | JSON | — | Task author (from ATO published rates) | CC BY (ATO) | Schedule |
| 4 | `medicare_levy_lito_rules.json` | JSON | — | Task author (from ATO) | CC BY | Levy and offset |
| 5 | `product_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `calculator_average_rate.xlsx` | XLSX | — | Task author | — | Naive calculator |
| 7 | `tax_check_cases.json` | JSON | ~10 | Task author | — | Hand-computed examples |

## 5. Deterministic solution path

1. Filter residents; compute tax at TI and TI − 12,000 with levy and offset.
2. Savings; weighted deciles; medians.
3. Threshold search; contrast with average-rate savings.

## 6. Wrong paths (method errors, not misreadings)

**A — average tax rate × deduction.** Biased savings.

**B — top marginal rate for all.** Overstated.

**C — ignoring bracket crossing.** Overstated near thresholds.

**D — ignoring Medicare levy.** Understated.

## 7. Why the stump is analytical, not semantic

The schedule and computation are specified. The trap is average versus marginal rates.

## 8. Draft task prompt (prose)

> Who should we market EV salary-packaging to? Compute exact tax savings from the deduction on the ATO sample file as the product memo specifies and
> find the income threshold where the median saving beats our fee. Provide `savings_by_decile.csv` (decile: income range, median saving marginal and
> average-rate methods), `saving_curve.png`, and a one-page `marketing_threshold.pdf`.

## 9. Deliverables

* `savings_by_decile.csv`, `saving_curve.png`, `marketing_threshold.pdf`.

## 10. Where 25+ rubric criteria come from

* 10 deciles × 2 methods = 20; threshold; check cases; weighted counts above threshold.

## 11. Golden-output checklist

* Residency filter; schedule; levy; offset; exact recomputation; threshold search.

## 12. Build notes (scope tuning)

* Confirm the average-rate calculator implies a threshold at least $15,000 different.
