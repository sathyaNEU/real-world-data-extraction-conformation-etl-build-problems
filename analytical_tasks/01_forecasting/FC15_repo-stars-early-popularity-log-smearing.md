# FC15 — Predicting a repository's 90-day stars from its first week: decay, log scales and the back-transformation

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Platforms predicting long-run popularity from launch-week engagement to allocate featured slots and capacity (developer platforms' Explore pages, app-store features, video and streaming promotion) |
| Domain | Developer platforms / content promotion |
| Task shape | 01 · Ranked list under a cap (up to 10 featured slots, gated by an expected-stars threshold) |
| Core method | Log–log regression of cumulative stars (day 90 on day 7) fitted on a prior cohort; expected values via Duan's smearing back-transformation; day 0 aligned to the date the repository became public; stars deduplicated by user and repository ID |
| Analytical stump | Attention to a launch is front-loaded and decays, so scaling the first week linearly overstates the total; a levels regression is dominated by a few viral launches; exponentiating a log-scale prediction gives the conditional median, not the expected value, so a threshold stated on expected stars is missed unless the back-transformation is corrected |
| Primary sources | GH Archive (public GitHub event timeline: WatchEvent, PublicEvent and CreateEvent records); GitHub REST API repository metadata |

## 1. The real-world situation

A developer platform features new open-source projects in a weekly newsletter and on its Explore page. Each featured repository must be expected
to reach at least **2,000 stars within 90 days** of going public, because featuring also commits sponsored CI minutes and package-mirror capacity.
The analyst multiplied first-week stars by 90/7; the featured list filled with repositories whose attention collapsed after a launch-day spike on
social media.

## 2. The decision (one deterministic recommendation)

**Which repositories that went public in the first two weeks of January 2024 are featured (at most 10, each with expected 90-day stars ≥ 2,000),
ranked by expected stars?**

Rules (featuring memo):

* Day 0: the date of the repository's PublicEvent (private repository made public) or, for repositories created public, the date of its
  CreateEvent with ref_type = repository. Repositories identified by repository ID, not name (names change).
* Exclusions: forks (GitHub API `fork = true`); repositories without an identifiable day 0.
* Stars: WatchEvent records (action "started"), deduplicated to the first event per (actor ID, repository ID); V7 = stars from day 0 through
  day 6; V90 = through day 89 (UTC dates).
* Candidates: V7 ≥ 50. Training cohort = repositories with day 0 in January–September 2023; decision cohort = day 0 from 1 to 14 January 2024.
* Model: ln V90 = a + b·ln V7 + ε, OLS on the training cohort.
* Expected V90 for a new repository = exp(a + b·ln V7) × S, where S = mean of exp(residuals) on the training cohort (smearing).
* Feature repositories with expected V90 ≥ 2,000, highest first, at most 10.

## 3. Why capable analysts get it wrong

* Linear scaling assumes a constant daily rate; launch attention is front-loaded and decays.
* Regressing in levels lets a few viral launches set the slope and produces heteroscedastic errors.
* The log model's raw back-transform is the conditional median; a threshold stated on expected stars needs the smearing factor.
* Repository creation dates misalign windows for projects developed privately before launch, and re-star events inflate counts.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–12 | `gharchive_watch_events_2023-MM.parquet` (2023-01 … 2023-12) | Parquet | ~5–10M each | Task author (WatchEvent rows extracted unchanged from GH Archive hourly files) | GH Archive public event data (verify terms) | Training-cohort stars |
| 13–16 | `gharchive_watch_events_2024-MM.parquet` (2024-01 … 2024-04) | Parquet | ~5–10M each | Same | Same | Decision-cohort stars and hold-out validation |
| 17 | `gharchive_public_create_events_2023_2024.parquet` | Parquet | ~30M | Task author (PublicEvent and repository CreateEvent rows extracted from GH Archive) | Same | Day 0 per repository |
| 18 | `repo_metadata_candidates.json` | JSON | ~6k | GitHub REST API (repository objects) | GitHub API terms (verify) | Fork flag, IDs, current names |
| 19 | `github_event_types.html` | HTML | — | GitHub Docs ("GitHub event types") | CC BY 4.0 (GitHub Docs content) | Event payload definitions |
| 20 | `gharchive_extraction.sql` | SQL | — | Task author (the BigQuery/GH Archive filter used for files 1–17) | — | Reproducible extraction |
| 21 | `duan_1983_smearing_reference.pdf` (citation) | PDF | — | JASA 1983 (cite) | Cite | Smearing estimator |
| 22 | `featuring_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 23 | `analyst_linear_scaling.xlsx` | XLSX | ~400 | Task author | — | The 90/7 projections |
| 24 | `source_manifest.json` | JSON | ~24 | Task author | — | Provenance: source URL, download date, licence and SHA-256 for every input file |

## 5. Deterministic solution path

1. Establish day 0 per repository ID; drop forks and repositories without a day 0.
2. Deduplicate stars per (actor, repository); compute V7 and V90 on UTC days.
3. Fit the log–log OLS on the training cohort; compute residuals and S.
4. Predict expected V90 for the decision cohort; apply the threshold; rank; cap at 10.
5. Report hold-out accuracy for the decision cohort's realised V90 (validation, not used in the decision).
6. Contrast with 90/7 scaling and with the un-smeared back-transform.

## 6. Wrong paths (method errors, not misreadings)

**A — 90/7 scaling.** Over-features front-loaded launches.

**B — levels regression.** Slope driven by viral outliers; wrong list.

**C — no smearing.** Expected values too low; fewer repositories clear 2,000.

**D — creation-date alignment or re-stars counted.** Windows start months early for privately developed projects, or counts are inflated.

## 7. Why the stump is analytical, not semantic

Windows, cohorts, model and the expected-value threshold are explicit; event types are defined in the shipped documentation. The errors are about
decay dynamics, regression scale and retransformation bias — statistical method choices.

## 8. Draft task prompt (prose)

> We feature January's new repositories whose expected 90-day stars clear 2,000, up to ten, following the featuring memo. Fit the early-popularity
> model on the 2023 cohort and apply it to repositories that went public in the first two weeks of January 2024. Provide `featured_list.csv`
> (repository ID, name, V7, expected V90, median V90, rank, featured), `early_vs_final.png` plotting ln V90 against ln V7 for the training cohort
> with the fitted line and the decision cohort's predictions, and a one-page `featuring_memo_response.pdf` with the list, the smearing factor, and
> which repositories the 90/7 rule would have featured instead.

## 9. Deliverables

* `featured_list.csv`, `early_vs_final.png`, `featuring_memo_response.pdf`.

## 10. Where 25+ rubric criteria come from

* Day-0 and deduplication counts (repositories, forks dropped, re-stars removed): 4.
* a, b, S and fit statistics: 5.
* Expected V90 for the top 15 candidates: 15 (scored in groups of 5).
* Featured list (≤ 10) and order: 2.
* 90/7 contrast and median vs mean contrast: 3.
* Hold-out validation: 2.

## 11. Golden-output checklist

* Day 0 from PublicEvent/CreateEvent by repository ID; forks excluded.
* First star per (actor, repository); UTC windows.
* Log–log OLS; smearing; threshold; cap.

## 12. Build notes (scope tuning)

* Choose the threshold so that the smearing correction changes the number of featured repositories by at least one, and confirm that 90/7 scaling
  features at least two repositories the model does not.
* Publish the extraction query with the files; GH Archive hourly files are large, so ship cohort extracts rather than full dumps.
