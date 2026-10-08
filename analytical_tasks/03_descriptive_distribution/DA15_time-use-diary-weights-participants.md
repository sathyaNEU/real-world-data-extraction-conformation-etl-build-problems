# DA15 — Time spent: per participant, per person, and per day of the week

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | "Time spent" reporting at social, video and gaming companies (minutes per daily active user versus per registered user; weekday versus weekend mix) |
| Domain | Media / consumer behaviour |
| Task shape | 07 · Grid of cells (5 age groups × 3 activities → average minutes per day on two bases; the age group targeted by a streaming product's campaign) |
| Core method | Diary-day weights that correct for the survey's weekend oversampling (one diary day per respondent); population average = weighted mean including zeros; participant average = weighted mean among those with > 0 minutes; participation rate; identity: population mean = rate × participant mean |
| Analytical stump | Unweighted diary averages overweight weekends (half of diaries are weekend days by design); "average time spent" quoted among participants is far higher than the population average and changes rank order across groups. The campaign target depends on which base the memo specifies |
| Primary sources | U.S. Bureau of Labor Statistics American Time Use Survey (ATUS) multi-year microdata files |

## 1. The real-world situation

A streaming company targets its next campaign at the age group with the largest *population* average daily minutes of TV and video
watching that is not already a heavy streaming segment. A market-research summary quoted average daily minutes "among those who watch",
computed from unweighted diaries; it ranked the youngest group highest, which contradicted the company's own panel.

## 2. The decision (one deterministic recommendation)

**The age group targeted (highest population-average minutes of "watching TV" among groups whose participant-average minutes of "computer
use for leisure" are below the memo's cap), with both bases reported for all cells.**

Rules (research memo):

* Data: ATUS 2019 + 2022 + 2023 respondent and activity summary files (pandemic-affected 2020–2021 excluded per memo).
* Weights: final statistical weights (`TUFNWGTP` or `TU20FWGT` per year as documented) — they account for day-of-week sampling; pooled
  years weighted per BLS guidance (divide by number of years).
* Activities (activity-summary codes): watching TV (t120303, t120304), computer use for leisure excluding games (t120308), playing games
  (t120307).
* Age groups: 15–24, 25–34, 35–49, 50–64, 65+.
* Population average = Σ w × minutes ÷ Σ w; participation = Σ w × 1(minutes > 0) ÷ Σ w; participant average = Σ w × minutes over
  participants ÷ Σ w over participants.
* Target: highest population-average TV minutes among groups with participant-average leisure computer use < 120 minutes.

## 3. Why capable analysts get it wrong

* Diary files look like simple samples; weighting seems optional.
* Weekend days are oversampled so each day type has adequate sample; unweighted means overweight weekends.
* "Among participants" averages answer a different question and inflate low-participation activities.
* Pooling years requires weight scaling.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–3 | `atusresp_<yyyy>.dat` (3 years) | CSV-like text | ~8–9k each | BLS ATUS | U.S. Gov public domain | Respondent file, weights |
| 4–6 | `atussum_<yyyy>.dat` (3 years) | CSV-like text | ~8–9k each (400+ columns) | BLS ATUS | Public domain | Activity summary minutes |
| 7–9 | `atusact_<yyyy>.dat` (3 years) | CSV-like text | ~180k each | BLS ATUS | Public domain | Activity episodes (context) |
| 10 | `atus_user_guide.pdf` | PDF | — | BLS | Public domain | Weights, pooling guidance |
| 11 | `atus_activity_lexicon.pdf` | PDF | — | BLS | Public domain | Activity codes |
| 12 | `research_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 13 | `market_research_summary.xlsx` | XLSX | 15 | Task author | — | Unweighted participant averages |
| 14 | `bls_published_check_table.xlsx` | XLSX | ~20 | BLS ATUS published tables | Public domain | Validation |

## 5. Deterministic solution path

1. Load respondent and summary files; select activities and age groups.
2. Apply weights with year pooling.
3. Compute population averages, participation and participant averages for 15 cells.
4. Validate against published tables; apply target rule.

## 6. Wrong paths (method errors, not misreadings)

**A — unweighted means.** Weekend overweighting.

**B — participant averages as population figures.** Ranks change.

**C — pooled years without scaling.** Weighted totals inflated (means unaffected, totals wrong).

**D — including 2020–2021.** Not per memo.

## 7. Why the stump is analytical, not semantic

The codes, weights and bases are specified. The trap is the sampling design (day-of-week) and conditional versus unconditional means.

## 8. Draft task prompt (prose)

> Which age group should our next streaming campaign target? Follow the research memo using ATUS microdata, weighting properly and keeping
> population and participant averages separate. Provide `time_use_grid.csv` (age group × activity: population average, participation,
> participant average), `minutes_by_group.png`, and a one-page `campaign_target.pdf`.

## 9. Deliverables

* `time_use_grid.csv`, `minutes_by_group.png`, `campaign_target.pdf`.

## 10. Where 25+ rubric criteria come from

* 15 cells × (population average, participant average) = 30; participation rates; target; validation.

## 11. Golden-output checklist

* Weights by year; pooling; activity codes; three bases; identity check; target rule.

## 12. Build notes (scope tuning)

* Confirm the unweighted participant-average ranking differs from the weighted population ranking.
