# DA06 — Daily and monthly active contributors: uniques do not add up

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Engagement reporting at social and consumer platforms (DAU, MAU, stickiness by country and surface) |
| Domain | Online community / product analytics |
| Task shape | 07 · Grid of cells (10 countries × 12 months → DAU, MAU, stickiness; the country selected for a contributor-retention programme) |
| Core method | Distinct-count metrics computed from user-level activity: DAU = mean over days of distinct active users; MAU = distinct users active in the month; stickiness = DAU ÷ MAU; country assignment by the memo's rule for users active in several countries; global figures computed on the union, not summed |
| Analytical stump | Summing daily uniques to get monthly uniques, summing country MAUs to get a global MAU, or averaging country stickiness ratios each produce wrong numbers because distinct counts are not additive across days or segments. A user mapping in two countries is one global user |
| Primary sources | OpenStreetMap changeset metadata dump (changesets with user ID, timestamp and bounding box) |

## 1. The real-world situation

A mapping community foundation funds a contributor-retention programme in one country per year — the country with the lowest stickiness
among its ten largest contributor bases. Last year's analysis summed daily unique contributors across the month as "MAU", added country MAUs
for the global total, and averaged country ratios for the global stickiness; board members noticed the global MAU exceeded the number of
accounts that had edited at all.

## 2. The decision (one deterministic recommendation)

**The country selected for the programme (lowest average monthly stickiness over the 12 months among the ten largest), with its DAU, MAU and
stickiness by month; plus correctly computed global figures.**

Rules (community memo):

* Data: changesets created in the 12 calendar months in scope; activity = at least one changeset that day (UTC).
* Country of a changeset: the country containing the centroid of its bounding box (country polygons provided); changesets with empty or
  very large boxes (> 1° in either dimension) are excluded from country attribution but count toward global activity.
* Country user-month assignment: a user counts in every country where they were active that month (country metrics are country-scoped);
  global metrics count each user once.
* DAU (month) = mean over days of the month of distinct users active that day; MAU = distinct users active in the month; stickiness = DAU ÷ MAU.
* Ten largest countries = top 10 by average MAU over the year.
* Selection: lowest mean of the 12 monthly stickiness values; ties → larger MAU.

## 3. Why capable analysts get it wrong

* Additive aggregation is the reflex in dashboards; uniques need set operations.
* Summing country MAUs counts multi-country users several times.
* Averaging ratios across countries ignores their different sizes and overlap.
* Excluding unattributable changesets from global metrics loses active users.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `changesets-latest.osm.bz2` (12-month extract) | XML | ~25M changesets (extract) | OpenStreetMap planet changeset dump | ODbL 1.0 | Changesets with user, time, bbox |
| 2 | `changesets_12m.parquet` | Parquet | ~25M | Derived | ODbL 1.0 | Parsed changesets |
| 3 | `country_polygons.geojson` | GeoJSON | ~250 | Natural Earth admin-0 | Public domain | Country attribution |
| 4 | `community_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `last_year_dashboard.xlsx` | XLSX | ~130 | Task author | — | Additive metrics |
| 6 | `bbox_exclusion_rule.json` | JSON | — | Task author | — | Attribution exclusions |
| 7 | `user_day_activity.parquet` | Parquet | ~15M | Derived | ODbL 1.0 | Distinct user-days |
| 8 | `reference_counts.json` | JSON | ~20 | Task author | — | Check values for a test month |
| 9 | `osm_changeset_format.html` | HTML | — | OSM wiki | CC BY-SA 2.0 | Format reference |
| 10 | `month_calendar.csv` | CSV | 12 | Derived | — | Days per month |

## 5. Deterministic solution path

1. Parse changesets; compute centroids; attribute countries; apply exclusions.
2. Build distinct user-day and user-month sets per country and globally.
3. Compute DAU, MAU, stickiness for each country-month and globally.
4. Select the ten largest; mean stickiness; choose the country; contrast with last year's numbers.

## 6. Wrong paths (method errors, not misreadings)

**A — MAU = Σ daily uniques.** Inflated by repeat visitors.

**B — global MAU = Σ country MAUs.** Multi-country users duplicated.

**C — global stickiness = mean of country ratios.** Wrong weighting and overlap.

**D — dropping unattributable changesets globally.** Active users missing.

## 7. Why the stump is analytical, not semantic

Metrics are defined precisely. The trap is non-additivity of distinct counts across time and segments.

## 8. Draft task prompt (prose)

> Which country gets this year's contributor-retention programme? Compute DAU, MAU and stickiness for the ten largest countries and globally
> following the community memo. Provide `engagement_grid.csv` (country × month: DAU, MAU, stickiness), `stickiness_small_multiples.png`, and a
> one-page `programme_country.pdf` that also corrects last year's global figures.

## 9. Deliverables

* `engagement_grid.csv`, `stickiness_small_multiples.png`, `programme_country.pdf`.

## 10. Where 25+ rubric criteria come from

* 10 countries × 12 months stickiness (sampled), MAU for the ten; global DAU/MAU for 12 months; selection; corrections to last year.

## 11. Golden-output checklist

* Centroid attribution; exclusions; distinct sets; country versus global scoping; selection rule.

## 12. Build notes (scope tuning)

* Publish reference counts for one month to anchor parsing.
* Confirm last year's additive method would select a different country.
