# DA03 — Severe rent burden by neighbourhood: survey weights, household weights and honest margins of error

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Domain | Housing policy / grant eligibility / survey statistics |
| Task shape | 10 · Scorecard against thresholds (PUMA × test → designated / not; city go/no-go) |
| Core method | Weighted proportions from ACS PUMS household records, successive-difference replicate weights (80) for standard errors, 90% intervals compared with a threshold |
| Analytical stump | Unweighted shares misrepresent the population; person weights mis-weight a household measure; naive binomial standard errors ignore the complex design and understate uncertainty, so borderline areas get designated |
| Primary sources | Census ACS Public Use Microdata Sample (household file with replicate weights), PUMS accuracy documentation |

## 1. The real-world situation

A city applies for a state anti-displacement grant. Eligibility is assessed for each of its Public Use Microdata Areas
(PUMAs): a PUMA is designated when **severe rent burden** (renters paying more than 50% of income on rent) is above 25% with
90% confidence. The city qualifies if at least three of its PUMAs are designated. The analyst computed shares from the PUMS
records without weights and used a textbook binomial standard error; five PUMAs were designated. The state's reviewer
recomputed and found fewer.

## 2. The decision (one deterministic recommendation)

**Which PUMAs are designated, and does the city qualify?**

Rules (state eligibility standard):

* Data: ACS 5-year PUMS (2019–2023) household file for the state; the city's PUMAs listed in the folder.
* Universe: renter-occupied households (TEN = 3) paying cash rent with a computed gross-rent-to-income percentage (GRPIP not
  missing). Severe burden: GRPIP > 50 (GRPIP top-code treated as > 50).
* Estimate: household-weighted share using WGTP. Standard error from the 80 replicate weights:
  SE = √[(4/80) × Σ_r (p_r − p)²], where p_r uses WGTPr.
* Designated if the lower bound p − 1.645 × SE > 0.25.
* City qualifies if ≥ 3 PUMAs are designated.

## 3. Why capable analysts get it wrong

* Microdata invite simple counting; PUMS records are sampled with unequal probabilities, so weights matter.
* PUMS has person and household files with different weights; mixing them changes both the estimate and its universe.
* Textbook binomial SEs assume simple random sampling; the ACS design effect is larger, and the official method is the
  replicate-weight formula.
* With intervals that are too narrow, borderline PUMAs pass a confidence-based threshold.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `psam_h<st>.csv` (5-year household file) | CSV | 0.2–1.5M | Census ACS PUMS | U.S. Gov public domain | Household records with WGTP, WGTP1–80 |
| 2 | `psam_p<st>.csv` (5-year person file) | CSV | 0.5–3M | Census ACS PUMS | Public domain | Present (person weights — not for this measure) |
| 3 | `PUMS_Data_Dictionary_2019-2023.pdf` | PDF | — | Census | Public domain | Variables, codes, top-codes |
| 4 | `ACS_2019-2023_PUMS_Accuracy.pdf` | PDF | — | Census | Public domain | Replicate-weight SE formula |
| 5 | `2020_PUMA_names.xlsx` | XLSX | ~2.5k | Census | Public domain | PUMA names |
| 6 | `tl_2023_<st>_puma20.zip` | Shapefile | ~PUMAs | Census TIGER/Line | Public domain | Map |
| 7 | `acs5_2023_B25070_puma.csv` | CSV | ~PUMAs | Census ACS tables | Public domain | Published table cross-check |
| 8 | `city_pumas.json` | JSON | ~8 | Task author | — | Scope |
| 9 | `eligibility_standard.pdf` | PDF | — | Task author | — | Rules in §2 |
| 10 | `city_first_submission.xlsx` | XLSX | ~8 | Task author | — | Unweighted/binomial results |

## 5. Deterministic solution path

1. Filter the household file to the city's PUMAs and the universe.
2. Weighted share with WGTP; 80 replicate shares; SE by the formula; lower bound.
3. Designations; city decision; reconcile point estimates with published table B25070 (bins ≥ 50%).
4. Contrast: unweighted shares with binomial SEs; person-weighted shares.

## 6. Wrong paths (method errors, not misreadings)

**A — unweighted share.** Point estimates shift; designations change.

**B — binomial SE.** Intervals too narrow; extra designations.

**C — person weights / person file.** Wrong universe weighting.

**D — 1.96 for a 90% bound or two-sided logic.** Changes borderline outcomes.

## 7. Why the stump is analytical, not semantic

The measure, universe and formula are all spelled out. The difficulty is statistical: survey weighting and design-based
variance, which a naive microdata analysis gets wrong even when every variable is read correctly.

## 8. Draft task prompt (prose)

> The state designates a PUMA when its severe rent burden is above 25% with 90% confidence, and we qualify with at least
> three designated PUMAs. Using the PUMS files and the eligibility standard in the folder, estimate each of our PUMAs
> properly and tell me whether we qualify. Provide `puma_scorecard.csv` (PUMA, weighted households in universe, share, SE,
> lower bound, designated) and `rent_burden_intervals.png` with each PUMA's estimate and 90% interval against the 25% line.
> Add a one-page `eligibility_memo.pdf` with the decision and why our first submission over-designated.

## 9. Deliverables

* `puma_scorecard.csv`, `rent_burden_intervals.png`, `eligibility_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* ~8 PUMAs × (share, SE, lower bound, designation) = 32; city decision; first-submission contrast.

## 11. Golden-output checklist

* Household file, WGTP, replicate SE formula, one-sided 90% bound, designation rule, city decision.

## 12. Build notes (scope tuning)

* Choose a city with 2–4 PUMAs near the threshold so the binomial SE changes the qualification outcome.
* Confirm the GRPIP top-code and missing conventions in the 2019–2023 data dictionary.
