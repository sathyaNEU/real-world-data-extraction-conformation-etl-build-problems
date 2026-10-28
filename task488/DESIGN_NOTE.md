# task488 design note

## Draw

**Status: DESIGN 2026-10-28, architecture 1 drawn in education at the user's request** (an education task with a
data-engineering feel and an analytical stump). The seed ET45 world (barcode catalog matching) was paused at stage 1
with no card; its resume line allows a redraw outside the seed's world, so the slot keeps its number and objective
(ETL) and moves to `education-learning-sciences / item-response-theory-test-equating`, the only education task type
that serves ETL. The ET45 screen is kept below as a record.

- **Card:** `.claude/skills/fingerprint/cards/task488.json`, v1, registered 2026-10-28; `guard.py check` PASS (one
  NOTE: `driver.near` 0.13 against task479's architecture 4, differentiated on the card: that build removed answers
  given too fast to read before scoring; this one removes nothing).
- **Pairing:** Education & Learning Sciences, item response theory and test equating, Data Extraction & Conformation.
  The deliverable is the conformed item bank in the new platform's import layout, and the decisive field is each
  item's difficulty on the consortium's reporting scale.
- **World:** the Quarrystone Regional Assessment Consortium, eleven Wisconsin school districts that own an adaptive
  mathematics interim for grades 3 to 8, delivered since 2021 on Tessaline Learning Systems' platform. Its bank holds
  the items calibrated in the 2021 launch field test and about 340 items the member districts' teachers wrote in the
  2024 to 2026 summer workshops to measure students far below grade level; Tessaline ran those items on the writing
  panel's provisional difficulty ratings. Tessaline's contract ends 30 June 2027 and the bank moves to Corvane
  Assessment, whose blueprint needs a floor of items below each grade's Approaching cut.
- **Decision:** how many new low-band items the consortium must commission from the summer 2027 item-writing
  workshop, grade by grade, so every grade's bank meets Corvane's floor at the July 2027 cutover. Forcing event: the
  cutover; forum: the consortium's board (member superintendents), which funds the workshop by the accepted item.
- **Gap, pattern, generators:** gap objective (the panel's ratings, the percent correct and the reported scale scores
  are each correct as recorded and none is an item's difficulty on the scale); pattern none, generators G14 (an
  item's difficulty is its success rate conditioned on the takers' ability), G16 (two calibrations, the right one
  confirmed by the calibrated items' own values), G19 (the import contract). Labels population / G16 /
  method_or_model_selection were tried first and refused by `test.same_puzzle` and `test.same_driver` (task177's
  lineage and eight older builds).
- **Strategy:** other (contaminated conditioning: the variable each estimate would condition on, the reported scale
  score, was computed from the quantities being estimated). Gate G etl_conformance. Calibration form
  gold_standard_subsample (the calibrated items' bank values, which only the right calibration reproduces).
- **Personas:** `guard.py names --geo us --seed 488`; Sheri Brady and Timothy Fitzgerald on the card (Natasha Fox and
  Kevin Thornton, drawn first, warned on first names used in older builds).
- **Data-native sentence:** an adaptive engine serves each item to the students its recorded difficulty matches and
  scores them with the recorded difficulties, so an item whose recorded difficulty is wrong is met by the wrong
  students and corrupts their scores in the same direction.

## Screen

- **Prototype (scratchpad t488/proto, cat4 to cat7):** six grades, about 340 calibrated items and 45 to 95 provisional
  items a grade, 7,000 to 8,000 students, a 35 to 45 item adaptive test selecting the item nearest the running
  estimate among a randomised few, scored by EAP with the bank's operational values. Writers rated single-step items
  about right and multi-step word problems about 2 logits too easy.
- **Routes on the prototype (low-band totals over six grades, cut at -0.75):** truth 618; marginal likelihood with the
  calibrated items fixed 620; alternating EAP 620; re-scoring on the calibrated items only, EAP 620; calibration
  against the reported scale scores (the default path) 644; joint maximum likelihood 662; maximum-likelihood
  re-scoring on calibrated items only 654; the panel's ratings 740; percent correct mapped to difficulty through the
  calibrated items 397 (every provisional item out of the band).
- **Multi-step word problems (true mean about -0.05):** marginal likelihood -0.06 to -0.11; reported-score calibration
  -0.42 to -0.66; joint maximum likelihood -0.49 to -0.66.
- **The separating check:** the calibrated items re-estimated from the same responses. Mean error on items below
  -1.2: marginal likelihood +0.015, reported-score calibration -0.160, joint maximum likelihood -0.282 (and +0.168
  above 1.2). Only the marginal calibration reproduces the bank, so the data refute both wrong calibrations without
  any filed method.
- **Determinism risk carried into the generator:** items near the band edge. Under the right calibration the two item
  types sit on either side of the edge with a gap (single-step at or below -1.35, word problems at or above -0.4
  true), and the generator must keep every principled estimate at least 0.2 from the edge with enough takers per
  word problem (about 600) to hold its standard error near 0.1.

## ET45 screen record (paused 2026-10-26, superseded by the redraw)

Stage 1, not yet drawn. Seed ET45 (a nutrition app's product master merged from USDA FoodData Central
Branded Foods and Open Food Facts on barcodes), header and situation only. Objective ETL. The only client
task type that serves ETL in this world is `general-statistics-data-science/data-integration-record-linkage-entity-resolution`,
so the deciding quantity has to be record linkage's own statistical object (match and non-match agreement
rates, a key's evidence, linkage error, entity counts), and the seed's barcode normalization (leading zeros,
UPC-E, GTIN-14 indicator digits, check digits, restricted circulation codes) can only be Layer 1 or an ask
device, because the answer flipping on it is data semantics.

Banned against the last three builds at the screen (task304, task271, task270): strategies composition_mix,
forecast_method_backtest and maturity_censoring; forums committee_or_panel, board_of_directors and
executive_team; forcing events launch_or_rollout and period_close; org families financial_institution and
retailer_or_ecommerce. Personas drawn with `guard.py names --geo us --seed 488`: Natasha Fox, Kevin Thornton,
Mary Adams (unused until the draw is fixed).

Live candidates when the screen stopped, both unspent in the corpus (no driver mentions value-specific
agreement or matcher calibration):

1. The weight of an agreement depends on how common the agreeing value is (Fellegi-Sunter value-specific
   u-probabilities, the client's rigor pattern 2 for this task type taken to the value level). Its open
   problem is determinism: the probability that a unique exact agreement is the record's own product needs
   the share of records whose product is in the target file at all, and every route to it is a model.
   The cleanest determinate form found is the birthday-problem one, coincidences counted from pairs whose
   quasi-random field differs by a step (birth dates a few days apart), which lives in person linkage and
   would leave the seed's world.
2. A matcher's stated probabilities are overconfident where its fields record one fact (independence
   assumption broken), measured in the reviewed band and carried on the log-odds scale to the unreviewed
   auto-link band; a coarse dial of offered cut-offs keeps it determinate. Open problem: stump power, since
   the review band shows the miscalibration to anyone who bins it.

## Tried and rejected

- Precision of an attribute matcher carried from a small-block pilot to the full build, rebuilt from the
  per-comparison false-acceptance rate times the comparisons each block makes: the lesson is task192's
  (an instrument's error rates carry, its predictive values do not when the base rate moves) and task446
  v2's, in record-linkage nouns, so it is a repeated driver whatever the guard's lexical score (0.07).
- Resolving pairwise links into entities under a one-record-per-source constraint, chains cut at the
  weakest link: task486 architecture 2's driver, landed by its scored reader A.
- Correcting a noisy disagreement flag for its own error rates measured on known true and false links to
  estimate a barcode join's false-match share: task468's heart (linker misses and false links measured on
  control groups) and close to task456's latent class.
- Self-null coincidence rate (how often FDC's own distinct products agree on brand, serving and panel)
  applied to label-snap stubs: a paper simulation on seeds 488, 7 and 11 showed pair-level precision
  dominated by visible ties, so the tie rung lands the golden, and the per-link form needs the
  counterpart share, which no file pins.
- Clustered audit errors read with a design effect at the company prefix: task228's and task261's lesson
  (variance built at the unit the errors cluster within).
</content>
</invoke>
- The ET45 world's two live record-linkage candidates (value-specific agreement weights; a matcher's overconfidence carried to the auto-link band) were left unbuilt at the 2026-10-28 redraw into education at the user's request; the first had no determinate form inside the seed's world and the second's miscalibration shows to anyone who bins the review band.
