# DA06 — The contributor-stickiness baseline a mapping foundation signs into a grant, when the months that matter are withheld by the statistics service

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Product Analytics · contributor engagement on an open mapping platform |
| Mirrors | Committing a market-level engagement baseline from privacy-thresholded reporting that withholds small cells while its totals still include them (country metrics below privacy thresholds in App Store Connect and Google Play Console, thresholded rows in Google Analytics, small-segment suppression in Meta audience reporting) |
| Decision shape | One figure committed at a date: the KPI baseline written into the grant agreement signed on 1 March 2027 |
| Committed call | Kessa's Q4 2026 contributor stickiness (mean of the three monthly DAU/MAU ratios of contributors homed there), as a percentage to one decimal |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · E25, withheld cells fixed by an identity the published tables carry, with E07 (active-in-country against home-country grain) below it and an existing book blind to suppression (L1) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #24 treats an unpublished figure as unknown · #7 uses the ready-made measure · #4 never tests its reading against the control · #14 coarsens the segment it was asked about |
| Calibration form | Existing-book actuals: the foundation's 14 existing country grants, each with its filed baseline and the value later audited from raw logs |
| Driving force | The grant counts contributors in their home country, and the statistics service withholds Kessa's daily-active cells in November and December because they fall under its privacy threshold of 25. The cells are not unknown. Home-country tables partition each chapter region, and the regional summary carries every contributor, so each withheld cell is the region's total less its eight other countries, exactly. Every fallback an analyst reaches for (drop the months, borrow the region's rate, take the midpoint) moves the baseline by 12% to 32%. |

## 1. Situation

An open mapping foundation signs a two-year grant with a humanitarian fund on 1 March to grow the local contributor community in Kessa.
The fund pays a bonus if Kessa's contributor stickiness rises a quarter above the baseline, and the baseline is Q4 2026. The grant's
verification clause requires the baseline and every later reading to come from the platform's public statistics service, so the fund
can reproduce them. The service publishes monthly tables by country in two views: activity in a country, and contributors by home
country. It also publishes a regional summary for each volunteer chapter. Cells under its privacy thresholds are shown as "<50" for MAU
and "<25" for DAU. The pack also holds the 14 existing grants with their filed and audited baselines.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: both views, the regional summaries, the existing grants' baselines and audits. The dashboard's
  headline stickiness for Kessa is a true statement about activity in Kessa, and nobody's reading of their own numbers is overturned.
  The difficulty is the grain the grant counts and two cells the service withholds by design.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the partnerships lead's view and the fund's licensed basis. The activity view still offers complete,
  unsuppressed monthly figures for Kessa, and the home view still shows two withheld cells that invite a fallback.
* **Instrument repair.** The statistics service is exact and complete, and its threshold is its privacy rule, not a fault. The
  verification clause fixes the instrument, so the cells stay withheld in this baseline and in every reading the fund will take. Repair
  the raw logs as much as you like: they are not the instrument of record.
* **Lens swap.** The two reads cover different populations. In October, 498 contributors were active in Kessa, 248 of them homed abroad
  and mapping remotely, against the 250 contributors homed in Kessa, whose November and December daily counts the service withholds.

## 3. The driving force

A strong solver opens the dashboard's country view, where Kessa's figures are complete and print to the decimal, then reads the grant's
annex and moves to the home-country view, which the existing grants reproduce exactly. There, November and December show "<25" daily
active contributors, and every careful fallback is defensible. It can drop the two months, borrow the chapter region's stickiness, or
take the midpoint of the band. Each is a choice about an unknown. But the cells are not unknown. Home-country tables give each
contributor one country a month, so the nine countries of the Lakes chapter partition its regional summary. The summary's daily totals
carry every contributor, Kessa's included, while the other eight countries are all published. Each withheld cell is the region's total
less those eight, with no choice anywhere: 19 in November and 15 in December.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The dashboard's activity-in-country view, mean of the three monthly ratios | 15.1% (−37.7%) | Complete, unsuppressed, and the figure the dashboard prints | The grant's annex counts contributors in their home country, and the existing grants reproduce only on the home view |
| 1 | Home-country view, the two withheld months dropped | 32.0% (+32.3%) | The grant's grain, using only the months the service publishes | The verification clause makes the quarter's three months the baseline; a one-month quarter cannot be filed |
| 2 | Home-country view, withheld months filled with the Lakes region's home stickiness for the month | 21.2% (−12.5%) | The standard small-area fallback, borrowing the nearest published rate | The regional summary: its daily totals less the eight published countries leave exactly 19 and 15, not the region's rate |
| 3 | **Decisive:** withheld DAU recovered exactly as the regional total less the other eight countries, then the three monthly ratios averaged | **24.2%** | — | — |

* **Figure shape.** The answer is bracketed: the dropped-months and upper-bound fills file 32% and 24% high, while the activity view, the
  region-rate fill and the midpoint fill file 12% to 38% low. No fallback lands near it, because the withheld months sit far from every
  band-based guess.
* **Partial correction priced (L3).** A solver who differences but takes its regional totals from the activity view's regional summary
  mixes grains, recovers 31 and 27, and lands at 33.8% (+39.7%), further away than any fallback.
* **Grid.** View (activity or home) × withheld handling (drop, region rate, midpoint, upper bound, recovered) gives 6 distinct cells (the
  activity view has nothing withheld). The nearest non-answer cell is the region-rate fill at −12.5%.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The service's methodology note says each contributor has one home country a month, and the chapter charter lists
   the Lakes region's nine countries. No document connects the two, or says a withheld cell can be recovered.
2. **Corpus blind for a computable reason.** *In every existing grant every baseline month was published, because each past programme
   country had more than 400 homed contributors and at least 60 active on an average day.* The existing book certifies the home view
   (14 of 14 filed baselines, against 2 of 14 on the activity view) and has never met a withheld cell.
3. **No arithmetic symptom.** Every published cell is exact, the activity and home views each tie to their own regional summaries in the
   months with nothing withheld, and the fallbacks fail no check a solver writes unless it reconciles the home rows to the summary.
4. **Not a row predicate.** The recovered value lives in no row. It is an identity across nine country rows and a separately published
   regional total, valid only because the home view is a partition.
5. **The enumeration is arithmetic.** Two cells, recovered by subtraction from totals that are never presented beside them.
6. **No cutover date.** Kessa drops under the threshold because its community is small, not because anything changed, and no series
   steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the activity view still prints the only complete figure.

## 6. The calibration corpus

* **Form.** The 14 existing country grants (2021–2025): each with the baseline filed from the public service and the value the
  foundation's audit later recomputed from raw logs.
* **What it certifies (E07).** The home grain: all 14 filed baselines reproduce exactly from the home view and match their audits. The
  activity view reproduces 2 of 14, the two countries where nearly every mapper is homed locally. Every miss is low, because remote
  mappers' bursty activity drags the activity view's stickiness down.
* **What it is blind to.** Withheld cells (above).
* **Twin pair.** Kessa in November and Doru in November show identical home-view cells: 88 MAU, "<25" DAU. Recovered from their
  chapters' summaries, they hold 19 and 10 daily contributors: stickiness of 21.6% against 11.4% (1.9×). Every fallback gives them the
  same value, and only the regional identity separates them.
* **Resemblance points at the decoy.** Kessa's activity profile most resembles Halvar's, an existing grant whose filed baseline equals its
  activity-view headline because almost all its mappers are local.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The grant's KPI annex: "Contributors are counted in their home country as the statistics service assigns it each month;
  a quarter's stickiness is the mean of its three monthly ratios of average daily to monthly active contributors, stated to one decimal
  of a per cent." The verification clause: "The baseline and every KPI reading are taken from the platform's public statistics service."
  The service's methodology note gives the privacy thresholds (MAU under 50, DAU under 25).
* **Empirical pins.** The home grain, from the existing book.
* **Voices.** The partnerships lead: "The fund will check the dashboard's headline for Kessa; that's the number to sign." The chapter
  coordinator for the Lakes region: "Kessa behaves like the rest of the Lakes chapter. When their figures are hidden, ours are the best
  guide."
* **Licensed wrong basis.** The verification clause records that the fund's monitoring team reads the activity view and will report its
  figure beside the foundation's.

## 8. Determinism by construction

* **Partition.** Home countries are assigned per contributor-month, and every Lakes chapter contributor has exactly one home country in
  each month. In Q4 Kessa is the only withheld daily cell in the region, so each subtraction has one unknown.
* **Monthly MAU.** Kessa's home MAU (250, 88, 79; October carried a mapathon) is published in all three months, so only the numerators
  are recovered.
* **Averaging.** The annex fixes the mean of monthly ratios. The ratio of summed DAU to summed MAU (27.3%, +13.0%) is a hazard the annex
  refutes.
* **Rounding.** No construction lands within 0.05 points of a rounding boundary.

## 9. Prompt sketch and deliverables

> The grant with the humanitarian fund is signed on 1 March, and it needs Kessa's baseline: contributor stickiness for last quarter, the
> number every future reading is measured against. Our partnerships lead believes the dashboard's headline for Kessa is what the fund
> will check. Give me the baseline as a percentage to one decimal, as the line that goes in the agreement, and send
> `baseline_build.xlsx` with the build and the sheets below, plus `stickiness_months.png`.

* `baseline_build.xlsx` — the recovery and the baseline, the four rung constructions (ask C), the new-contributor sheet (ask A) and the
  building-edits sheet (ask B).
* `stickiness_months.png` — Kessa's monthly stickiness for October to December under the four rung constructions, with the "<25" band
  shaded, the region's rate as a dashed line, the recovered months marked, and Doru's November twin annotated.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** New contributors (first-ever edit) homed in each of the nine Lakes countries in each month of Q4
  2026. *Device:* accounts created in bulk through the humanitarian tasking tool often wait months before a first edit. The service's
  definitions page dates a new contributor by first changeset, not account creation. Counting by creation date misplaces 22% to 61% of
  new contributors in six countries.
* **Ask B (device-carried).** Net buildings added in each of Kessa's three priority districts in each month from July to December 2026.
  *Device:* bulk imports carry an import tag and are excluded from mapped totals, as the import guidelines document, and a reverted
  changeset is listed in the revert log against its original id. Ignoring either overstates 13 of the 18 cells.
* **Ask C (validity).** The baseline under each of the four rung constructions, and the two recovered DAU values.
* **Decoupling.** The new-contributor export and the changeset statistics share no row with the DAU and MAU tables. Clearing the recovery
  changes no figure in asks A or B.

## 11. Rubric arithmetic

9 countries × 3 months (ask A) + 3 districts × 6 months (ask B) + 4 constructions and 2 recovered cells (ask C) + the committed baseline,
the twin values and the grain gap in October + 5 named chart parts + 2 files ≈ 63 criteria.

## 12. World-building constraints

* Kessa's home view: MAU 250 / 88 / 79 and DAU 80 / 19 / 15 (the last two withheld). Activity view: MAU 498 / 331 / 318 and DAU 98 / 44
  / 39. The Lakes region's home stickiness is 16.5% in November and 15.0% in December.
* Constructions land at 15.1% / 32.0% / 21.2% / 24.2%, and the other cells at 20.7% (midpoint), 29.9% (upper bound), 33.8% (mixed
  grains) and 27.3% (pooled ratio). None lies within 12% of the answer.
* Kessa is the only withheld daily cell in the Lakes region in Q4. Doru's November cell is the only other "<25" with an MAU of 88.
* All 14 existing baselines reproduce on the home view, and none had a withheld month.
* The new-contributor export and the changeset statistics touch no DAU or MAU cell.
