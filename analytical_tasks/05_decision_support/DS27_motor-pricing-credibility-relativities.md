# DS27 — Setting regional price relativities: small regions' raw claim experience is mostly noise

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Segment-level pricing with sparse data (marketplace fees by category, insurance-like guarantees, risk-based pricing by cohort) |
| Domain | Motor insurance pricing |
| Task shape | 07 · Grid of cells (regions × methods → relativity; the relativities filed for next year) |
| Core method | Claim frequency relativities by region with exposure; Bühlmann–Straub credibility: Z = E ÷ (E + k), k = expected process variance ÷ variance of hypothetical means estimated from the data; credibility-weighted relativity = Z × observed + (1 − Z) × complement (overall or density-band relativity); cap changes at ±10% per memo |
| Analytical stump | Setting relativities equal to observed frequency ratios lets random claim counts in thin regions swing prices; using full credibility only above an arbitrary exposure threshold creates discontinuities. Credibility weights grounded in the data's variance components balance stability and responsiveness |
| Primary sources | freMTPL2 French motor third-party liability dataset (CASdatasets: freMTPL2freq) |

## 1. The real-world situation

A motor insurer files regional frequency relativities annually. The pricing analyst set each region's relativity to its observed claim frequency
divided by the countrywide frequency. Several small regions' relativities moved by more than 30% from the prior year, triggering regulatory
questions.

## 2. The decision (one deterministic recommendation)

**The filed relativity for each of the 22 regions, using Bühlmann–Straub credibility toward density-band complements and the ±10% change cap, and
the regions whose filed change differs most from the raw approach.**

Rules (pricing memo):

* Data: freMTPL2freq (policies with exposure and claim counts; Region, Density).
* Frequency per region = Σ claims ÷ Σ exposure; countrywide frequency = totals.
* Complement: frequency of the region's density band (quartiles of policy-level density, exposure-weighted per memo) ÷ countrywide.
* Bühlmann–Straub: estimate expected process variance and variance of hypothetical means across regions by the standard non-parametric estimators
  (memo formulas); k = EPV ÷ VHM; Z_r = E_r ÷ (E_r + k).
* Credibility relativity = Z × raw + (1 − Z) × complement.
* Filed = prior relativity × clamp(cred ÷ prior, 0.9, 1.1) with prior relativities in `prior_relativities.csv`.

## 3. Why capable analysts get it wrong

* Raw ratios look like "the data speaks".
* Poisson noise in small regions is large relative to true differences.
* Complements matter: density captures part of regional risk.
* Caps limit year-over-year volatility but don't fix estimation noise.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `freMTPL2freq.csv` | CSV | 678,013 policies | CASdatasets (R package; Charpentier) | GPL (≥ 2) per CASdatasets | Exposure, claims, region, density |
| 2 | `freMTPL2sev.csv` | CSV | ~26k claims | CASdatasets | GPL | Claim amounts (context) |
| 3 | `casdatasets_documentation.pdf` | PDF | — | CASdatasets | GPL | Variable definitions |
| 4 | `prior_relativities.csv` | CSV | 22 | Task author | — | Prior filed values |
| 5 | `pricing_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `analyst_raw_relativities.xlsx` | XLSX | 22 | Task author | — | Raw approach |
| 7 | `buhlmann_straub_reference.pdf` | PDF | — | Cite (Klugman, Panjer & Willmot) | Cite | Estimators |

## 5. Deterministic solution path

1. Aggregate exposure and claims by region; raw relativities; density-band complements.
2. Estimate EPV and VHM; k; Z per region.
3. Credibility relativities; caps; filed values; contrast.

## 6. Wrong paths (method errors, not misreadings)

**A — raw relativities.** Volatile.

**B — fixed full-credibility threshold (e.g., 1,082 claims).** Ad hoc; not the memo's estimator.

**C — complement = 1.0 for all.** Ignores density information.

**D — caps applied before credibility.** Wrong order.

## 7. Why the stump is analytical, not semantic

The estimators, complements and caps are specified. The trap is treating sparse segment experience at face value.

## 8. Draft task prompt (prose)

> What regional relativities should we file? Apply Bühlmann–Straub credibility toward density-band complements with the change caps in the pricing memo.
> Provide `region_relativities.csv` (region: exposure, claims, raw, complement, Z, credibility, filed), `credibility_weights.png`, and a one-page
> `relativity_filing.pdf`.

## 9. Deliverables

* `region_relativities.csv`, `credibility_weights.png`, `relativity_filing.pdf`.

## 10. Where 25+ rubric criteria come from

* 22 filed relativities; k, EPV, VHM; Z for 6 regions; largest differences versus raw.

## 11. Golden-output checklist

* Aggregation; complements; variance estimators; Z; caps; order.

## 12. Build notes (scope tuning)

* Confirm at least four small regions' raw changes exceed ±20% while filed changes stay within the cap.
