# AD01 — Which hospital trusts really have excess mortality? Funnel limits that allow for real-world variation

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Domain | Healthcare quality surveillance (NHS England) |
| Task shape | 14 · Cuts of a distribution (nested 95% / 99.8% funnel bands per trust) |
| Core method | Funnel-plot control limits for standardized ratios with an additive random-effects overdispersion adjustment (winsorized z-scores) |
| Analytical stump | With large expected counts, pure Poisson limits are so narrow that a third of trusts look "abnormal"; ranking by the ratio flags small trusts by chance. Limits must widen for between-trust variation that is not evidence of poor care |
| Primary sources | NHS England / NHS Digital Summary Hospital-level Mortality Indicator (SHMI) trust and diagnosis-group files, published SHMI methodology |

## 1. The real-world situation

A regional quality board commissions **case-note reviews** at trusts whose mortality is far above expectation. An analyst
took the latest SHMI release, computed Poisson 99.8% limits for each trust's observed/expected ratio and found 30+ trusts
outside them — more than the board could review, and many that the national publication classified as "as expected".
A second analyst simply took the ten highest SHMI values, which included two small specialist trusts with few deaths.

## 2. The decision (one deterministic recommendation)

**Which trusts fall in the alarm band (outside the upper 99.8% limit) and are referred for review, and which are in the
alert band (between upper 95% and 99.8%)?**

Rules (board surveillance standard):

* Use the trust-level file of the release in the folder: observed deaths O, expected deaths E, ratio SHMI = O ÷ E.
* A trust is flagged only when its deviation from 1.0 exceeds what chance plus the **ordinary variation seen among trusts**
  would produce, estimated from the release itself as described in the published indicator methodology (folder), including
  its winsorizing rule.
* Bands: below/above the 95% limits = "lower/higher than expected (alert)"; above the 99.8% limit = "alarm".
* Alarm-band trusts are referred; for the highest-z alarm trust, list the diagnosis groups with the largest O − E.

## 3. Why capable analysts get it wrong

* Poisson limits assume all variation beyond the expected count is signal; risk models never capture everything, so real
  indicators are over-dispersed.
* Ranking by ratio ignores precision — a trust with E = 40 can reach 1.3 by chance far more easily than one with E = 2,000.
* Estimating overdispersion from raw z-scores lets the outliers themselves widen the limits (hence winsorizing).
* Using a common SD of ratios ignores that precision differs by size.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `SHMI_data_at_trust_level_<release>.csv` | CSV | ~120 | NHS England (SHMI publication) | OGL v3.0 | O, E, SHMI, national banding |
| 2 | `SHMI_diagnosis_group_breakdown_<release>.csv` | CSV | ~15–20k | NHS England | OGL v3.0 | O and E by trust × diagnosis group |
| 3 | `SHMI_contextual_indicators_<release>.csv` | CSV | ~1k | NHS England | OGL v3.0 | Palliative coding, deprivation context |
| 4 | `SHMI_data_at_trust_level_<previous_release>.csv` | CSV | ~120 | NHS England | OGL v3.0 | Stability check |
| 5 | `SHMI_methodology_specification.pdf` | PDF | — | NHS England | OGL v3.0 | Overdispersion and banding method |
| 6 | `spiegelhalter_2005_funnel_plots.pdf` (citation) | PDF | — | Statistics in Medicine 2005 (cite) | Cite | Method background |
| 7 | `trust_region_lookup.xlsx` | XLSX | ~120 | NHS ODS | OGL v3.0 | Region membership |
| 8 | `shmi_trust_metadata.json` | JSON | ~120 | NHS ODS API | OGL v3.0 | Trust names/types |
| 9 | `surveillance_standard.pdf` | PDF | — | Task author | — | Rules in §2 |
| 10 | `analyst_poisson_flags.xlsx` | XLSX | ~35 | Task author | — | The over-flagging first attempt |

## 5. Deterministic solution path

1. Compute z-scores on the ratio scale with Poisson standard errors (√(1/E)).
2. Winsorize z at the methodology's percentiles; estimate the overdispersion and the additive between-trust variance τ².
3. Limits for each trust: 1 ± z_α √(1/E + τ²) at 95% and 99.8%; classify bands.
4. List alarm trusts (referrals); diagnosis-group O − E for the top one.
5. Compare with Poisson-only flags and the top-10 ranking; reconcile with the national banding in the file.

## 6. Wrong paths (method errors, not misreadings)

**A — Poisson limits.** Dozens of alarms; the board cannot act; many are noise.

**B — rank by SHMI.** Small trusts flagged by chance; large genuinely-high trusts missed.

**C — un-winsorized τ².** Outliers inflate τ² and hide the true alarm.

**D — common SD of ratios.** Ignores precision differences.

## 7. Why the stump is analytical, not semantic

O, E and the ratio are unambiguous. The question is statistical: how much variation is expected among trusts. The wrong
answers come from the variance model, not from misreading the data.

## 8. Draft task prompt (prose)

> The board refers trusts for case-note review only when their mortality is far beyond what chance and ordinary
> variation among trusts would produce, as our surveillance standard and the indicator methodology in the folder describe.
> Using the latest SHMI files, classify every trust and tell me which are referred. Produce `funnel_bands.csv` (trust, O,
> E, SHMI, z, both limits, band) and `shmi_funnel.png`, a funnel plot of SHMI against expected deaths with both sets of
> limits and the alarm trusts labelled. Add a one-page `referral_memo.pdf` with the referral list, the alert list, the
> estimated between-trust variation, and the diagnosis groups driving the top alarm trust.

## 9. Deliverables

* `funnel_bands.csv`, `shmi_funnel.png`, `referral_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* Bands for ~120 trusts (alarm/alert membership checked), τ², referral list, top trust's diagnosis groups, comparison
  with Poisson flags.

## 11. Golden-output checklist

* Winsorized overdispersion; limits per E; correct bands; referral list; diagnosis drill.

## 12. Build notes (scope tuning)

* Verify the exact winsorizing and limit conventions in the SHMI methodology you ship and reproduce the national banding
  for the release before writing the answer key.
* Choose a release where Poisson-only flags exceed 20 trusts and the overdispersed alarm list has 1–4.
