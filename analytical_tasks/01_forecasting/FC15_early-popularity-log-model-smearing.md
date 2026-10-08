# FC15 — Predicting a title's 60-day audience from its first week: decay, log scales and the back-transformation

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Video/streaming platforms predicting long-run popularity from early views to allocate promotion and cache capacity |
| Domain | Media / content promotion / CDN capacity |
| Task shape | 01 · Ranked list under a cap (up to 10 promotions, gated by an expected-audience threshold) |
| Core method | Log–log regression of cumulative views (day 60 on day 7) fitted on a prior cohort; expected values via Duan's smearing back-transformation |
| Analytical stump | Daily attention decays after release, so scaling the first week linearly overstates the total; a levels regression is dominated by blockbusters; exponentiating a log-scale prediction gives the median, not the expected value, so a threshold on expected views is missed unless the back-transformation is corrected |
| Primary sources | Wikimedia daily per-article pageviews, Wikidata film metadata |

## 1. The real-world situation

A streaming service's merchandising team promotes newly released films on its home page and pre-positions them in edge caches.
Each title promoted must be expected to reach at least **1.5 million** views within 60 days of release (the team uses public
Wikipedia attention as a proxy until first-party data mature). The analyst multiplied first-week views by 60/7; the list was
full of films whose attention collapsed after opening weekend.

## 2. The decision (one deterministic recommendation)

**Which 2024-release films are promoted (at most 10, each with expected 60-day views ≥ 1.5M), ranked by expected views?**

Rules (merchandising memo):

* Films: English-language feature films with a Wikidata publication date (U.S. theatrical or streaming release) in the
  calendar year; training cohort = 2022–2023 releases, decision cohort = 2024 releases (lists in folder).
* V7 = cumulative English Wikipedia user (non-bot) pageviews of the film's article from release day through day 6; V60 = through
  day 59.
* Model: ln V60 = a + b·ln V7 + ε, OLS on the training cohort.
* Expected V60 for a new film = exp(a + b·ln V7) × S, where S = mean of exp(residuals) on the training cohort (smearing).
* Promote films with expected V60 ≥ 1.5M, highest first, at most 10.

## 3. Why capable analysts get it wrong

* Linear scaling assumes a constant daily rate; attention to releases is front-loaded and decays.
* Regressing in levels lets a few blockbusters set the slope and produces heteroscedastic errors.
* The log model's raw back-transform is the conditional median; a threshold stated on expected views needs the smearing factor.
* Using the article creation date instead of the release date misaligns windows.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–36 | `pageviews_daily_film_articles_YYYY-MM.parquet` (2022-01 … 2024-12) | Parquet | ~20–40k article-days each | Wikimedia Pageviews API / pageview dumps | CC0 (pageview data) | Daily views per article |
| 37 | `films_2022_2024_wikidata.json` | JSON | ~3k | Wikidata SPARQL export | CC0 | Release dates, language, article titles |
| 38 | `films_training_cohort.csv`, `films_decision_cohort.csv` | CSV | ~1k / ~500 | Derived | CC0 | Cohorts |
| 39 | `pageviews_api_documentation.pdf` | PDF | — | Wikimedia | CC BY-SA (docs) | Agent types (user vs bots) |
| 40 | `duan_1983_smearing_reference.pdf` (citation) | PDF | — | JASA 1983 (cite) | Cite | Smearing estimator |
| 41 | `merchandising_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 42 | `analyst_linear_scaling.xlsx` | XLSX | ~500 | Task author | — | The 60/7 projections |

## 5. Deterministic solution path

1. Align each film's day 0 to its release date; compute V7 and V60 (user agent only).
2. Fit the log–log OLS on the training cohort; compute residuals and S.
3. Predict expected V60 for 2024 films; apply threshold; rank; cap at 10.
4. Report hold-out accuracy for 2024 films with complete 60 days (validation, not used in the decision).
5. Contrast with 60/7 scaling and with the un-smeared back-transform.

## 6. Wrong paths (method errors, not misreadings)

**A — 60/7 scaling.** Over-promotes front-loaded titles.

**B — levels regression.** Slope driven by outliers; wrong list.

**C — no smearing.** Expected values too low; fewer titles clear 1.5M.

**D — bot traffic included / creation-date alignment.** Inflated or misaligned windows.

## 7. Why the stump is analytical, not semantic

Windows, cohorts, model and the expected-value threshold are explicit. The errors are about decay dynamics, regression scale and
retransformation bias — statistical method choices.

## 8. Draft task prompt (prose)

> We promote 2024 releases whose expected 60-day audience clears 1.5 million, up to ten titles, following the merchandising memo.
> Fit the early-popularity model on the 2022–2023 films and apply it to the 2024 films using the pageview data in the folder. Provide
> `promotion_list.csv` (film, V7, expected V60, median V60, rank, promoted), `early_vs_final.png` plotting ln V60 against ln V7 for
> the training cohort with the fitted line and the 2024 films' predictions, and a one-page `promotion_memo.pdf` with the list, the
> smearing factor, and which titles the 60/7 rule would have promoted instead.

## 9. Deliverables

* `promotion_list.csv`, `early_vs_final.png`, `promotion_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* a, b, S; expected V60 for the top 15 candidates; promoted list (≤ 10) and order; 60/7 contrast; median vs mean contrast.

## 11. Golden-output checklist

* Release-date alignment; user agent only; log–log OLS; smearing; threshold; cap.

## 12. Build notes (scope tuning)

* Choose the threshold so that the smearing correction changes the number of promoted titles by at least one.
* Freeze the Wikidata query and the article-title mapping (redirects!) used to pull pageviews.
