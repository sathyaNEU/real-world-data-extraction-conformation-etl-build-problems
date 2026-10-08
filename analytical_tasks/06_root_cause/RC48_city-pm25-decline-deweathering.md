# RC48 — The city's PM2.5 fell 25% in three years: did the clean-air plan deliver it, or did the weather?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Weather- or seasonality-normalised KPIs (retail sales normalised for weather, energy savings normalised for degree days, ad performance normalised for seasonal demand) used to credit an intervention |
| Domain | Environmental policy / air quality |
| Task shape | 11 · Before and after with a control (observed PM2.5 change vs a meteorologically normalised counterfactual built by resampling weather; emission-driven change vs weather-driven change by site) |
| Core method | Per monitoring site, a random-forest model of log PM2.5 on meteorology (temperature, pressure, dew point, rain, wind speed, wind direction) and time variables including a trend term; weather normalisation by repeatedly predicting each hour with meteorology resampled from the same season across all years; emission (normalised) change vs meteorology effect = observed − normalised change |
| Analytical stump | A raw before/after comparison credits the policy with any favourable weather (windier, wetter winters disperse pollution). Including weather as linear covariates misses the strongly nonlinear effects of stagnation, humidity and wind direction on PM2.5. Normalising requires predicting under resampled weather, not just adjusting coefficients |
| Primary sources | UCI Machine Learning Repository — Beijing Multi-Site Air-Quality Data (12 sites, hourly, March 2013 – February 2017, with meteorology) |

## 1. The real-world situation

A city government reported that annual PM2.5 had fallen 25% between the first and fourth year of its clean-air action plan and credited the plan.
An international lender financing the next phase asked for evidence that the decline reflected emissions rather than meteorology, since loan
tranches are tied to emission reductions.

## 2. The decision (one deterministic recommendation)

**Whether the plan's claim is accepted for the loan milestone (accepted if the weather-normalised decline is ≥ 80% of the observed decline,
averaged over sites), with site-level emission and meteorology effects.**

Rules (lender memo):

* Data: the UCI multi-site hourly files; Year 1 = March 2013 – February 2014; Year 4 = March 2016 – February 2017.
* Cleaning: hours with missing PM2.5 excluded from targets; missing meteorology imputed by linear interpolation for gaps ≤ 3 hours, else the hour is
  excluded; PM2.5 values < 1 set to 1 before logging.
* Model per site: random forest (300 trees, mtry = 3, minimum node size 5, seed 2017) predicting log PM2.5 from TEMP, PRES, DEWP, RAIN, WSPM, wind
  direction as a 16-level factor, hour of day, day of week, day of year, and a trend term (days since start).
* Normalisation: for each hour, 200 predictions with the meteorology and day-of-year resampled from hours within ± 14 days of the same day of year in
  any year (seeded), trend and hour of day kept; normalised value = mean of exp(prediction).
* Annual means (observed and normalised) per site; emission effect = normalised Year 4 − Year 1; meteorology effect = observed change − emission
  effect.
* Accept if the mean across sites of emission effect ÷ observed change ≥ 80%.

## 3. Why capable analysts get it wrong

* Before/after averages are the policy's own headline.
* Meteorology has large year-to-year swings in northern China winters.
* Linear weather adjustment is inadequate for stagnation episodes.
* Wind direction is categorical/circular, not a number.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `PRSA_Data_<site>_20130301-20170228.csv` (12 files) | CSV | ~35k each (~420k total) | UCI ML Repository (id 501) | CC BY 4.0 | Hourly pollutants and meteorology |
| 2 | `beijing_air_quality_description.html` | HTML | — | UCI | CC BY 4.0 | Fields |
| 3 | `zhang_2017_dataset_paper_citation.pdf` | PDF | — | Cite | Cite | Dataset paper |
| 4 | `grange_2018_deweathering_citation.pdf` | PDF | — | Cite (Grange et al., Atmos. Chem. Phys. 2018) | Cite | Method |
| 5 | `lender_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `city_progress_report_excerpt.pdf` | PDF | — | Task author (summary of the claim) | — | The 25% claim |

## 5. Deterministic solution path

1. Clean and impute per site; build features.
2. Fit seeded forests; report out-of-bag fit.
3. Weather-normalised series; annual means; effects per site.
4. Mean share; decision; contrast with the raw comparison and with a linear-adjustment model.

## 6. Wrong paths (method errors, not misreadings)

**A — raw before/after.** Weather credited to policy.

**B — linear regression with weather covariates.** Misses stagnation and wind-direction effects.

**C — wind direction as degrees.** Treats 350° and 10° as far apart.

**D — normalising without resampling.** Predicting at average weather is not the same as averaging over the weather distribution.

## 7. Why the stump is analytical, not semantic

The model, seeds and resampling are specified. The trap is attributing a weather-sensitive outcome to an intervention without a meteorological
counterfactual.

## 8. Draft task prompt (prose)

> The city says its plan cut PM2.5 by 25%. Separate emissions from weather with the lender memo's deweathering method and tell me whether the
> milestone claim holds. Provide `deweathered_effects.csv` (site: observed, normalised, emission and meteorology effects), `deweathered_trends.png`,
> and a one-page `milestone_assessment.pdf`.

## 9. Deliverables

* `deweathered_effects.csv` — 12 sites plus the mean share.
* `deweathered_trends.png` — observed and normalised monthly series for the city mean of sites.
* `milestone_assessment.pdf` — decision and site heterogeneity.

## 10. Where 25+ rubric criteria come from

* Cleaning counts per site (sampled 4 sites): 4.
* Model fit statistics per site (sampled 4): 4.
* Observed and normalised annual means for 12 sites (scored in groups): 6.
* Effects and shares; mean share: 4.
* Decision: 1.
* Contrasts (raw, linear model): 4.
* Chart elements: 2+.

## 11. Golden-output checklist

* Imputation rules; log transform floor.
* Seeded forest settings; factor wind direction.
* Seasonal resampling window ± 14 days; 200 draws.

## 12. Build notes (scope tuning)

* Run the method once and confirm that the emission share for the mean of sites is below 80% while the raw decline exceeds 20%. If it is not, use
  the memo's alternative Year-4 window (March 2015 – February 2016) and re-check; record the final windows and the computed share in the golden
  output.
