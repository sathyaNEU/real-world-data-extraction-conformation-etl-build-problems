# leak check, task452

**Verdict: REVIEW.** 16 files read, 49 golden figures and 10 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: design, points, rejected, stratum, strata, agreement, estimator, preliminary, period, decisive, default, method, definition, reporting, adjudication, asserted, counts, window, weights, article, population, stratified, weight, stated, golden

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `emission_reductions_payment_agreement_extract.pdf`: carries 13 of 13 distinctive words of the committed call: 'The Lowland Forest Emission Reductions Program can offer the Rainforest Results Facility 23,229,780 tonnes of emission r'
- **REVIEW** `forest_reference_level_2015-2022_summary.pdf`: carries 10 of 13 distinctive words of the committed call: 'The Lowland Forest Emission Reductions Program can offer the Rainforest Results Facility 23,229,780 tonnes of emission r'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `emission_reductions_payment_agreement_extract.pdf`: 5 of 25 stump-paragraph terms appear (agreement, period, definition, reporting, article); read whether the document names the move
- **REVIEW** `forest_reference_level_2015-2022_summary.pdf`: 4 of 25 stump-paragraph terms appear (points, agreement, period, reporting); read whether the document names the move
- **REVIEW** `monitoring_plan_extract.pdf`: 4 of 25 stump-paragraph terms appear (points, period, definition, reporting); read whether the document names the move
- **REVIEW** `reference_sampling_design_2026-01.pdf`: 10 of 25 stump-paragraph terms appear (design, points, stratum, strata, preliminary, period); read whether the document names the move

## 6 ranking artifacts (REVIEW 1, INFO 2)
- **REVIEW** `final_change_map_v2_statistics.xlsx`: names 9 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `district_concordance_2019_2025.csv`: names 9 of 10 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `monitoring_plan_extract.pdf`: names 9 of 10 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

### Pass 1 (2026-10-14, isolated Sonnet reader at medium effort, fresh copies of prompt.txt and target/ only)

- **Q1** none announces the decisive step; the reader's nearest pointers are the monitoring plan's 4.1 and 4.2, the design report's section 2 (the strata are the preliminary map's classes) and the release note (version 2.0 replaces 0.9 and is the map the report presents), and its own reading was that the stratum weights "have to be reconciled with the final map".
- **Q2** none ranks the candidates or states the tonnes or the payment; the map statistics' 73,225 ha is the final map's mapped area, the easy route's raw material, not an answer.
- **Q3** none; every file has an organisational source.
- **Q4** none; the reference level and the emission factor are inputs.
- **Q5** the agreement's articles 2, 4, 5 and 6, the plan's 3.1 to 3.3, 4.4 and 4.5 quoted and executed; the reader computed 122,900 ha on the preliminary strata and 171,600 ha re-weighting by the final map's class areas and read the choice of weights as what flips the call. No filed sentence fixes the weights (the plan's 4.1 fixes the estimand: the reference sample, a probability sample), so this is the analytical choice, not a fork; the judge confirms the correctly weighted post-stratified estimator gives 122,934 ha, the same 122,900.
- **Q6** an analytical choice (which stratum weights the estimator applies); not a field reading, a stated procedure or a plant.
- **REVIEW lines** all harmless (the agreement and the reference level summary carry the call's nouns as the documents it executes; the plan and the design report state the design and the estimand and name no estimator; the map statistics rank nothing).
- **Realism** fixed in the generator: remarks drawn evenly, land cover and canopy one to one, the quality-control canopy differing on 36 points without an adjudication row, inventory plots even across years (see the design note's `## Tried and rejected`). Not changed: the district land areas are the statistics institute's round figures (the reader judged the pixel-counted totals plausible). Two claims did not hold: Nueva Esperanza (LT-06) holds 190 reference points, and the export manifest lists every other file.

### Pass 2 (2026-10-14, isolated Sonnet reader at medium effort, on the final pack: reference level 89,950 ha a year, repaired texture)

- **Q1** none names the move; the nearest sentences are the design report's strata and stratum areas, the release note's "Version 2.0 is the map the 2024-2025 monitoring report presents" (read by the reader as a lure toward the final map's areas) and the plan's 4.1.
- **Q2 to Q4** none; the map statistics' areas are the final map's mapped areas, not the estimate, and no file states the tonnes, the payment or the interval.
- **Q5** every filed rule quoted and executed; the reader's own estimate on the design strata is about 122,883 ha, 122,900 stated, with a 90 per cent half-width of about 20,130 ha; re-weighting by the final map's class areas gives about 171,581 ha. (Its reference level emissions figure, 89,411,030, is its own slip: 179,900 times 497 is 89,410,300.) It asked whether the patch counts follow the 2019 or the 2025 district layer: the plan's 3.3 sets the accounting area's districts on the 2019 layer and the concordance places LT-05 and LT-06 in La Esperanza (SF12).
- **Q6** an analytical choice (stratified estimation on the design's strata rather than weighting by the final map's areas); the forest definition, the adjudication, the rounding and the district layers are secondary and decide nothing on the main call.
- **Checks it ran** every main-against-quality-control difference (126) is in the adjudication log, none missing and none extra; the per-point change field agrees with the definition-based class; the quality-control export holds one point in five.
- **REVIEW lines** all harmless; the design report "borderline, leaning harmless": it states the design facts the correct method needs and never says to weight by them or warns against the final map.
- **Realism notes** minor: interpretation and quality-control dates on every day of the week and operators' workloads near equal, the adjudication dates spread evenly, the district land areas round in the statistics institute's figures (as in pass 1).
- **After pass 2** (figure-neutral, no random stream moved; checks, verify and the free gates re-run): interpretation and quality-control dates fall on working days (a draw on a Saturday becomes Friday's, on a Sunday Monday's) and two of the seven interpreters carry double loads; the adjudication dates (13 to 17 April 2026, Monday to Friday) and the statistics institute's round district land areas are kept.

### Pass 3 (2026-10-14, isolated Sonnet reader at medium effort, after the prompt repair: "how many tonnes, if any", "what would the Facility pay")

- **Q1** none states the move; the reader assembled the design report's strata, the release note's "Version 2.0 is the map the 2024-2025 monitoring report presents" and the plan's 4.1 and 4.2, and itself took the re-stratification on the final map as the route (the default path): the documents state facts, and the choice stays the analyst's.
- **Q2 to Q4** none ranks the candidates or states the tonnes, the payment or the interval; the statistics workbook's "Country 82665.36" is the final map's pixel count over the whole country, the easy route's raw material, not the estimate.
- **Q5** every filed rule quoted (articles 1, 2, 4(2), 5, 6; the plan's 3.1 to 3.3, 4.1, 4.3 to 4.5); no sentence fixes the weights.
- **Q6** an analytical choice (the estimator and its strata); the forest definition, the adjudication, the district layers and the rounding are secondary.
- **Prompt read** "if any" keeps none grammatical (article 5 provides for none); no phrase presupposes a non-zero quantity, a subset or a direction; none is a grammatical answer to every question and ask.

