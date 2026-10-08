# FC22 — Signing free agents on next year's performance: last season is the loudest, least reliable signal

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Talent and performance forecasting (sports front offices; the same mechanics drive "star performer" bets in sales and hiring) |
| Domain | Sports analytics / player acquisition |
| Task shape | 01 · Ranked list under a cap (five free-agent hitters) |
| Core method | Marcel-style projection: weighted three-season rates, regression toward the league mean by an amount of "phantom" plate appearances, age adjustment |
| Analytical stump | A single season's on-base percentage over 300–600 plate appearances is heavily noise; ranking on it (or on an unweighted average of rates) chases luck. The projection must weight seasons by recency and volume and shrink toward the league mean |
| Primary sources | Lahman Baseball Database (batting, people) |

## 1. The real-world situation

A club's front office has budget for **five free-agent hitters** and ranks candidates by expected on-base percentage (OBP) next
season. The scouting director ranked them by last season's OBP. Two of last season's top performers had career years on modest
playing time; a veteran with three consistent seasons ranked 14th.

## 2. The decision (one deterministic recommendation)

**Which five free agents are signed (highest projected 2016 OBP), and who is sixth?**

Rules (analytics memo, Marcel method):

* Candidates: the 40 hitters listed in the folder (free agents after 2015).
* Seasons 2013, 2014, 2015 with weights 3, 4, 5. For OBP: projected numerator = Σ w × (H + BB + HBP) + 1,200 × league OBP
  (weighted league rate over the same seasons); denominator = Σ w × (AB + BB + HBP + SF) + 1,200.
* Age adjustment (age on 1 July 2016): multiply the projected rate by (1 + 0.006 × (29 − age)) if age < 29, else
  (1 + 0.003 × (29 − age)).
* League OBP per season from the Lahman `Batting` table (all non-pitcher batters with ≥ 1 PA, combined).
* Rank by projected OBP; ties by more 2015 plate appearances.

## 3. Why capable analysts get it wrong

* Last season is the most salient and most recent number.
* The binomial noise in a 500-PA OBP has a standard deviation of about 0.02 — the same size as the differences between candidates.
* Averaging three seasonal OBPs gives a 150-PA season the same weight as a 650-PA season.
* Age curves bend after 29; ignoring them over-values older players with strong histories.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Batting.csv` | CSV | ~110k | Lahman Baseball Database | CC BY-SA 3.0 | Season batting lines |
| 2 | `People.csv` | CSV | ~20k | Lahman | CC BY-SA 3.0 | Birth dates |
| 3 | `Appearances.csv` | CSV | ~110k | Lahman | CC BY-SA 3.0 | Positions (exclude pitchers) |
| 4 | `Fielding.csv` | CSV | ~150k | Lahman | CC BY-SA 3.0 | Context |
| 5 | `lahman_readme.pdf` | PDF | — | Lahman | CC BY-SA 3.0 | Field definitions |
| 6 | `free_agent_candidates_2016.json` | JSON | 40 | Task author (from public transaction lists) | — | Candidates |
| 7 | `marcel_method_reference.pdf` (citation) | PDF | — | Tango's Marcel description (cite) | Cite | Method |
| 8 | `analytics_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `scouting_ranking.xlsx` | XLSX | 40 | Task author | — | Last-season ranking |
| 10 | `Batting_2016_validation.csv` | CSV | ~1.5k | Lahman (2016 season) | CC BY-SA 3.0 | Realized OBP check |

## 5. Deterministic solution path

1. Compute league OBP per season (non-pitchers) and the weighted league rate.
2. For each candidate, weighted numerator/denominator with 1,200 phantom PA at league rate; projected OBP.
3. Age adjustment; rank; top five + sixth.
4. Validate against realized 2016 OBP (correlation and mean of chosen five) for both rankings.

## 6. Wrong paths (method errors, not misreadings)

**A — last-season OBP.** Picks career years.

**B — unweighted average of rates.** Low-volume seasons over-weighted.

**C — no regression to the mean.** Extreme small-sample candidates rise.

**D — no age adjustment.** Older candidates over-valued.

## 7. Why the stump is analytical, not semantic

OBP and the projection formula are defined in the memo. The trap is treating noisy observed rates as true talent — a statistical
error in forecasting individual performance.

## 8. Draft task prompt (prose)

> We can sign five free-agent hitters and want the five with the highest expected OBP next season, projected the way the analytics
> memo specifies. Using the Lahman files and the candidate list in the folder, give me the five and the sixth. Provide
> `obp_projections.csv` (candidate: age, 2013–2015 lines, weighted rate, regressed rate, age-adjusted projection, rank),
> `projection_vs_lastseason.png` plotting last season's OBP against projected OBP with plate appearances as point size, and a
> one-page `signing_memo.pdf` with the five, the margin at the cut and how the scouting ranking compares on realized 2016 OBP.

## 9. Deliverables

* `obp_projections.csv`, `projection_vs_lastseason.png`, `signing_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* League OBP per season (3); projections for the top 10 candidates; five signed + sixth; validation comparison; scouting contrast.

## 11. Golden-output checklist

* Weights 3/4/5; 1,200 phantom PA; correct denominators; age factor; tie rule.

## 12. Build notes (scope tuning)

* Choose the candidate list so that last-season OBP and Marcel differ in at least two of the top five.
* Confirm the Lahman version includes 2016 for validation.
