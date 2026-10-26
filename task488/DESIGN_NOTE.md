# task488 design note

## Draw

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
