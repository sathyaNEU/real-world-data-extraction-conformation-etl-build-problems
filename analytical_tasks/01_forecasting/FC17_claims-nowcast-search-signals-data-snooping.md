# FC17 — Nowcasting jobless claims from web attention: the predictors that only work in hindsight

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Search/attention-based nowcasting that collapsed out of sample (the Flu Trends class of failure) |
| Domain | Macroeconomic nowcasting / labour-market analytics |
| Task shape | 10 · Scorecard against thresholds (candidate nowcast models × out-of-sample tests → adopt / hold) |
| Core method | Real-time rolling-origin evaluation with predictor selection repeated inside each training window; seasonal differencing of predictors and target |
| Analytical stump | Picking the attention series most correlated with claims over the whole sample is look-ahead and, with hundreds of candidates, selects seasonal coincidences ("holiday" pages track the January claims spike). In-sample fit is superb; real-time accuracy is worse than a naive baseline |
| Primary sources | U.S. DOL ETA 539 weekly unemployment insurance claims, Wikimedia pageviews |

## 1. The real-world situation

A bank's economics team wants a Thursday-morning **nowcast** of the week's initial jobless claims before the official release,
using Wikipedia attention to pages about unemployment, layoffs and benefits. A data scientist screened 220 candidate pages,
kept the 30 most correlated with claims over 2015–2023, and fitted a regression with R² = 0.96. Leadership wants to know whether
to adopt it for client notes.

## 2. The decision (one deterministic recommendation)

**Adopt one nowcast model or keep the baseline, judged on 2022–2024 real-time performance.**

Rules (research memo):

* Target: national not-seasonally-adjusted initial claims for week t (week ending Saturday). Information at nowcast time: claims
  through week t−1 and daily pageviews (user agent) through the Saturday of week t.
* Baseline M0: claims(t−1) × [claims(t−52) ÷ claims(t−53)] (last week scaled by last year's week-over-week change).
* M1: OLS of claims(t) on the 30 pages most correlated with claims over **2015–2023** (as the data scientist did).
* M2: same, but the 30 pages are re-selected each year using only data before that year's first nowcast.
* M3: as M2, but target and predictors in 52-week log differences (y/y), with predictions mapped back to levels.
* Evaluation: weekly nowcasts for 2022–2024, models refitted at the start of each quarter on all prior data (2015 onward,
  excluding March 2020 – June 2021 as an extreme regime).
* Adopt the model with the lowest MAE if it beats M0's MAE by ≥ 10%; otherwise keep M0.

## 3. Why capable analysts get it wrong

* Correlation screens over the full sample use the evaluation period to choose predictors — look-ahead.
* With 220 candidates, many correlations are seasonal coincidences; claims have strong January and July patterns.
* Levels regressions of trending/seasonal series produce high R² that does not transfer.
* In-sample fit is what the screening procedure maximizes; it says little about real-time accuracy.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `ar539.csv` (weekly claims, national and state) | CSV | ~40k | U.S. DOL ETA | Public domain | Target |
| 2 | `weekly_claims_release_calendar_2022_2024.csv` | CSV | ~160 | DOL news releases | Public domain | Publication timing |
| 3–14 | `pageviews_candidates_YYYY.parquet` (2015–2024, plus 2 supplements) | Parquet | ~80k page-days per year | Wikimedia Pageviews API | CC0 | Daily views for 220 candidate pages |
| 15 | `candidate_pages.json` | JSON | 220 | Task author | — | Page list and rationale |
| 16 | `ui_claims_definitions.pdf` | PDF | — | DOL ETA handbook extract | Public domain | Definitions |
| 17 | `ginsberg_2009_lazer_2014_citations.pdf` | PDF | — | Nature 2009; Science 2014 (cite) | Cite | Background on nowcasting pitfalls |
| 18 | `research_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 19 | `data_scientist_model.xlsx` | XLSX | ~40 | Task author | — | M1 selection and in-sample fit |

## 5. Deterministic solution path

1. Build weekly pageview sums aligned to claims weeks (Sunday–Saturday).
2. Implement M0–M3 with quarterly refits and yearly re-selection (M2, M3) using only prior data.
3. Generate 2022–2024 nowcasts; compute MAE per model; apply the adoption rule.
4. Report each model's in-sample R² alongside real-time MAE.

## 6. Wrong paths (method errors, not misreadings)

**A — M1 judged in sample.** Adopted despite worse real-time MAE.

**B — full-sample selection with rolling refits.** Still look-ahead; flatters M1.

**C — levels for M3.** Seasonal coincidence persists.

**D — publication timing ignored.** Using claims(t) information that is not yet released.

## 7. Why the stump is analytical, not semantic

Target, information set, models and adoption rule are defined. The trap is the validation design (selection inside vs outside the
training window) and spurious correlation among many seasonal series.

## 8. Draft task prompt (prose)

> Should we adopt a web-attention nowcast of weekly jobless claims for client notes? Evaluate the four models in the research memo
> as they would have run in real time over 2022–2024, using the claims and pageview files in the folder, and give me adopt or hold.
> Provide `nowcast_scorecard.csv` (model: in-sample R², real-time MAE, improvement over baseline, decision), `nowcast_vs_actual.png`
> showing the four models' weekly nowcasts against actual claims in 2023, and a one-page `nowcast_decision.pdf` explaining why the
> best in-sample model is or is not the best real-time model.

## 9. Deliverables

* `nowcast_scorecard.csv`, `nowcast_vs_actual.png`, `nowcast_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 models × (R², MAE, improvement, pass) = 16; quarterly MAE by model for 2022–2024 (sampled); selected pages overlap between M1 and
  M2; decision.

## 11. Golden-output checklist

* Correct week alignment; selection inside training windows; quarterly refits; regime exclusion; adoption rule.

## 12. Build notes (scope tuning)

* Curate the 220 candidates to include obviously relevant and seasonal decoy pages; confirm M1 has the highest in-sample fit and a
  real-time MAE worse than M0.
* Record pageview API parameters (access, agent) used for every page.
