# AD05 — Opioid prescribing outliers: small denominators, specialty peers and a composite that picks one prescriber

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Ranking outliers with small denominators (seller defect rates, click fraud by publisher, per-team incident rates), where shrinkage and peer groups are required |
| Domain | Health program integrity / prescription drug monitoring |
| Task shape | 16 · Indicators into one score (eligibility screen → shrunken indicators → percentile scaling within specialty → weighted composite → selected unit) |
| Core method | Beta-binomial empirical-Bayes shrinkage of rate indicators toward specialty means (method-of-moments prior), within-specialty percentile scaling, weighted composite |
| Analytical stump | Raw rates from small denominators produce extreme values by chance (3 of 3 claims long-acting = 100%); ranking them selects noise. Comparing across specialties flags clinically expected prescribing |
| Primary sources | CMS Medicare Part D Prescribers by Provider and by Provider & Drug; CMS opioid prescribing methodology |

## 1. The real-world situation

A state's program-integrity unit refers **one prescriber per quarter** for an opioid peer review, chosen by a composite
outlier score built from Medicare Part D data. The last two referrals were a nurse practitioner with 14 claims (all
long-acting opioids) and a hospice physician. Neither review found a problem; the panel asked for a method that would stop
"chasing small numbers and the wrong comparison group".

## 2. The decision (one deterministic recommendation)

**Which prescriber is referred this quarter (highest composite score), and who are the next four?**

Rules (program-integrity method):

* Universe: prescribers in the state with ≥ 50 total Part D claims; specialties listed as clinically expected high users
  (hospice/palliative, hematology-oncology, medical oncology, pain management, anesthesiology-pain) are excluded.
* Indicators (rates): I1 opioid claims ÷ total claims; I2 long-acting opioid claims ÷ opioid claims; I3 opioid
  beneficiaries ÷ total beneficiaries. Where a denominator is suppressed or zero, the indicator is missing and the prescriber
  is ineligible.
* Each rate is replaced by its **credibility-weighted estimate**: posterior mean under a beta prior fitted by the method of
  moments to that indicator's rates within the prescriber's specialty (specialties with < 30 eligible prescribers pool to
  "all other").
* Scale each shrunken indicator to its percentile rank within specialty (0–100). Composite = 0.4·I1 + 0.4·I2 + 0.2·I3.
* Refer the highest composite; ties by more opioid claims.

## 3. Why capable analysts get it wrong

* Rates feel comparable regardless of size; the binomial noise for n = 14 is enormous compared with n = 1,400.
* A simple volume cut-off helps but does not remove noise just above the cut-off; shrinkage weighs each rate by its
  reliability.
* Specialties differ legitimately; global percentiles flag specialists by design.
* Min–max scaling lets one extreme prescriber compress everyone else; within-specialty percentiles are robust.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `MUP_DPR_RY24_P04_V10_DY22_NPI.csv` (Prescribers by Provider, DY2022) | CSV | ~1.1M | CMS data.cms.gov | U.S. Gov public domain | Claims, opioid and LA counts, beneficiaries, specialty |
| 2 | `MUP_DPR_RY24_P04_V10_DY22_NPIBN.csv` (by Provider & Drug, state extract) | CSV | ~1–2M (state) | CMS | Public domain | Drug-level validation |
| 3 | `Medicare_Part_D_Prescribers_Data_Dictionary.pdf` | PDF | — | CMS | Public domain | Fields, suppression rules |
| 4 | `Opioid_Drug_List_Methodology.pdf` | PDF | — | CMS | Public domain | Opioid and long-acting definitions |
| 5 | `MUP_DPR_DY21_NPI_state.csv` | CSV | ~30–80k | CMS | Public domain | Prior-year stability check |
| 6 | `nucc_taxonomy.csv` | CSV | ~880 | NUCC | NUCC terms (attribution) | Specialty grouping cross-check |
| 7 | `efron_morris_eb_reference.pdf` (citation) | PDF | — | Cite | Cite | Shrinkage background |
| 8 | `program_integrity_method.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `excluded_specialties.json` | JSON | ~10 | Task author | — | Exclusions |
| 10 | `last_two_referrals.xlsx` | XLSX | 2 | Task author (public NPIs; outcomes generic) | — | Context |

## 5. Deterministic solution path

1. Filter the state; apply volume, specialty and missing-denominator screens.
2. For each indicator and specialty: compute raw rates; fit beta prior by method of moments (mean, variance of rates
   accounting for binomial variance as specified); compute posterior means.
3. Percentile ranks within specialty; composite; rank; refer #1; list #2–#5.
4. Contrast: raw-rate composite; global (cross-specialty) percentiles; min–max scaling.

## 6. Wrong paths (method errors, not misreadings)

**A — raw rates.** Low-volume prescribers with extreme proportions top the list.

**B — global percentiles.** Specialty with legitimately high use dominates.

**C — min–max scaling.** One extreme value compresses everyone; ranks reshuffle.

**D — averaging rates across indicators with different denominators before shrinkage.** Distorts reliability weighting.

## 7. Why the stump is analytical, not semantic

Indicator definitions, screens and weights are explicit; CMS defines opioid and long-acting classes. The error is
statistical: treating noisy small-sample proportions as precise, and choosing the wrong comparison distribution.

## 8. Draft task prompt (prose)

> We refer one prescriber for opioid peer review this quarter, chosen by the composite in our program-integrity method. Using
> the Part D files in the folder, build the composite exactly as specified — screened, credibility-weighted, scaled within
> specialty — and tell me who is referred and who the next four are. Provide `composite_scores.csv` (prescriber, specialty,
> raw and shrunken indicators, percentiles, composite, rank), `shrinkage_effect.png` plotting raw versus shrunken I2 against
> number of opioid claims with the referred prescriber marked, and a one-page `referral_memo.pdf` naming the referral and
> explaining why the top raw-rate prescriber is not referred.

## 9. Deliverables

* `composite_scores.csv`, `shrinkage_effect.png`, `referral_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* Top 5 × (3 shrunken indicators + composite) = 20; prior parameters for 2 specialties; referral; raw-rate contrast.

## 11. Golden-output checklist

* Screens; method-of-moments priors per specialty; posterior means; within-specialty percentiles; weights; tie rule.

## 12. Build notes (scope tuning)

* Pick a state where the raw-rate leader has < 30 opioid claims and the shrunken leader differs.
* Specify the method-of-moments formula (including how binomial sampling variance is removed) in the memo to make priors
  reproducible.
