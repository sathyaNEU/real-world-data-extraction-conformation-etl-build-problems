# AD15 — Keeping bots off the trending list: real spikes look the same everywhere, fake ones don't

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Social and content platforms filtering inauthentic engagement from trending/recommendation surfaces |
| Domain | Content integrity / trust & safety |
| Task shape | 16 · Indicators into one score (inauthenticity composite over trending candidates → the article-day escalated, top 10 excluded) |
| Core method | Composition-consistency indicators relative to each article's own baseline: platform mix shift, hourly concentration, cross-language corroboration, automated-agent co-movement; percentile scaling within the candidate set; weighted composite |
| Analytical stump | Spike size (z-score of views) cannot separate news from manipulation — both are huge. Inauthentic traffic betrays itself in *composition*: one platform, flat or clockwork hours, no echo in other language editions. Indicators must be relative to the article's own baseline, not absolute |
| Primary sources | Wikimedia pageview_complete daily dumps (with hourly and access-method detail), Wikidata sitelinks |

## 1. The real-world situation

A media app builds a "trending topics" rail from Wikipedia attention. Several days the rail was topped by obscure articles whose views
jumped 100-fold — later traced to unidentified automated traffic classified as users. The integrity team wants a composite score to
review the day's top candidates and exclude the ten most suspicious.

## 2. The decision (one deterministic recommendation)

**For the evaluation day, the article-day escalated for manual review (highest composite) and the 10 excluded from the rail.**

Rules (integrity memo):

* Candidates: the 200 English Wikipedia articles with the largest ratio of the day's user views to their 28-day median (minimum 20,000
  user views that day).
* Indicators (relative to the article's previous 28 days): I1 change in desktop share of user views (percentage points); I2 hourly
  concentration: 1 − (normalized entropy of the 24 hourly user counts) minus the baseline's mean value; I3 cross-language corroboration:
  −(median view ratio of the same Wikidata item in the 5 largest other language editions where it exists); I4 automated-agent co-movement:
  ratio of the day's automated views to their 28-day median (log).
* Scale each indicator to its percentile within the 200 candidates; composite = 0.35·I1 + 0.25·I2 + 0.25·I3 + 0.15·I4.
* Escalate the top composite; exclude the top 10.

## 3. Why capable analysts get it wrong

* View spikes are the signal everyone sees; they are equally large for elections and for bot runs.
* Platform mix, hourly shape and cross-language echoes are the fingerprints; they require baselines per article.
* Absolute thresholds on desktop share penalize articles that are normally desktop-heavy.
* Indicators on different scales must be scaled before weighting.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–29 | `pageviews-YYYYMMDD-user.bz2` (pageview_complete, 29 days) | Text (bz2) | ~50–80M lines per day (all wikis) | Wikimedia dumps | CC0 | Daily views by article, access method, hourly letters |
| 30–31 | `pageviews-YYYYMMDD-automated.bz2` (evaluation day + baseline sample) | Text | ~5M | Wikimedia dumps | CC0 | Automated agent views |
| 32 | `wikidata_sitelinks_candidates.json` | JSON | ~200 items | Wikidata | CC0 | Cross-language links |
| 33 | `pageview_complete_format.pdf` | PDF | — | Wikimedia documentation | CC BY-SA | Encoding of hourly counts |
| 34 | `candidates_extract.parquet` | Parquet | ~200 × 29 days × languages | Derived | CC0 | Working table |
| 35 | `integrity_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 36 | `rail_history.csv` | CSV | ~300 | Task author | — | Past rails (context) |

## 5. Deterministic solution path

1. Decode pageview_complete lines for candidates; build daily and hourly user views by access method; automated views.
2. Baselines (28 days) per article; indicators I1–I4 for the evaluation day; cross-language ratios via sitelinks.
3. Percentile scaling; composite; rank; escalate and exclude.
4. Contrast with the top-10 by view z-score.

## 6. Wrong paths (method errors, not misreadings)

**A — rank by spike z-score.** Excludes genuine news.

**B — absolute desktop share.** Penalizes desktop-heavy topics.

**C — no cross-language check.** Misses the strongest corroboration signal.

**D — unscaled indicators.** One indicator dominates.

## 7. Why the stump is analytical, not semantic

Indicators, baselines and weights are defined. The trap is relying on magnitude instead of composition relative to a unit's own
baseline.

## 8. Draft task prompt (prose)

> Score today's 200 trending candidates for inauthentic traffic as the integrity memo specifies, escalate the most suspicious article-day and
> list the ten we exclude from the rail. Provide `inauthenticity_scores.csv` (article: raw indicators, percentiles, composite, rank),
> `fingerprints.png` (hourly and platform profiles for the escalated article vs a genuine news spike), and a one-page
> `integrity_decision.pdf`.

## 9. Deliverables

* `inauthenticity_scores.csv`, `fingerprints.png`, `integrity_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* Indicators for the top 10 (40 values); escalated article; excluded list; z-score contrast.

## 11. Golden-output checklist

* Correct decoding; baselines; indicator formulas; percentile scaling; weights; ranking.

## 12. Build notes (scope tuning)

* Pick an evaluation day with both a major news event and a known bot-driven spike (community reports of anomalous top-article entries).
* Ship candidate-level extracts rather than full dumps; publish the extraction script.
