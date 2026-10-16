# task463 design note: Kellesay RPI transaction data readiness (architecture 1)

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task463.json`, registered 2026-10-16. Guard WARN only; the older
  same-driver signature (gap time, G16, method_or_model_selection) against task254 v2 and task501 v2 (both lineage) is
  differentiated on the card. The four WARNs are answered below.
- **Seed:** ET20's world is EPA air-quality monitoring (a county's PM2.5 design value from daily values across
  monitors, for a manufacturer choosing a plant site). It sits in Physical & Environmental Sciences, whose monitoring
  task type serves anomaly detection and data quality only, and whose one ETL task type (emissions inventory) is banned
  for this draw by the pairing rule after task462. The draw keeps the seed's quantity form, an official statistic
  compiled from many high-frequency records into a period figure and held against a line for each candidate, in
  official statistics: a retail prices index item's 12-month rate compiled from supermarket transaction records.
- **Pairing:** Survey Research & Official Statistics / seasonal-adjustment-official-time-series-production / ETL, own
  pattern chain drift of linked superlative price indices under sales with stockpiling. Compiling a monthly price index
  from retailers' transaction feeds, conformed into product-months and set against the published index over a
  parallel year, is official time-series production; the last three draws are data integration, emissions inventory and
  metric definition, and this task type last carried task453 (a labour force survey restated across a questionnaire
  redesign), ten builds back.
- **Why this task type and mechanism:** the ETL builds on file spent completion of open periods (445, 451, 457),
  capture and coverage of registers (448, 454, 455), links and continuity (449, 455), a link through shared items (450),
  a rotating panel's measurement change (453), a stratified sample on a revised map (452), latent classes (456),
  partial observation selected on the trait (458), an operating level (459), a dispatch margin (460), a record extended
  through an auxiliary series (461) and detection-weighted snapshots (462); none compiles a price index, and none turns
  on the path dependence of linked comparisons.
- **Shape:** 07, a grid of items by measures. Arithmetic: for each of sixteen RPI items the transaction-data 12-month
  rate to September 2026, its difference from the published rate and whether it moves (48); the moved set and its count
  (2); the asks (each retailer's sales in each item over the parallel year, 48; each item's products in the conformed
  file, 16); the chart's named parts (5); the conformed product-month file (2): 121.
- **Strategy:** other (index-number path dependence; no vocab key names it: it is not a grain, population, censoring or
  composition choice) on the time gap (the twelve monthly links stand for the year) with the population gap behind it
  (the products a comparison holds). Generators G16 (method selection) decisive, G13 (horizon: the year is one
  comparison of two months, not twelve) behind.
- **World:** Statistics Kellesay, the statistics office of Kellesay (an invented self-governing island in the British
  Isles with its own pound at par and a 5 per cent GST), compiles the Kellesay Retail Prices Index monthly. Its sixteen
  packaged grocery and household items are priced by field collection (a collector's shelf price for a fixed sample of
  products on one day a month). Since September 2025 the island's three supermarket groups, Wrenfold Stores, Gorsedale
  Co-operative and Calderby's, have sent their full sales records; the office's introduction plan (June 2026) moves an
  item to transaction data from the January 2027 index when, over the parallel year, the two sources agree on its
  12-month rate to September 2026 within 1.5 points.
- **Forcing fact:** the island's Statistics Code requires two months' notice of a change of method, so the notice of
  the January 2027 changes is published on 13 November 2026. The call faces forward (which items the 2027 index takes
  from transaction data) on a closed parallel year.
- **Forum and forcing event:** line_manager_or_team (the head of prices statistics recommends, the Chief Statistician
  signs), statutory_or_regulatory_filing (the Code's advance notice). Organisation research_or_statistics_office; role
  statistical_office_head. Personas from `guard.py names --geo "United Kingdom" --seed 463`: Diana Lawson (head of prices
  statistics, owner of the introduction plan), Dennis Gill (Calderby's data manager, sender of its delivery note).
- **Data-native sentence:** laundry liquid, toilet rolls, bottled water and fizzy drinks keep, so a household that takes
  four on the month's multibuy buys none the month after; in the transaction records the offer month's low price
  carries a large share of the item's spending and the next month's restored price a small one, so a month-on-month
  comparison counts every cut at nearly full weight and every recovery at a fraction, while each product's own price
  ends the year about where its shelf price did.
- **Sources, one line each:**
  - `stumping/references/client/two-layer-task-design.md`, estimation that fits the data: chain-linked aggregation;
    here linked superlative comparisons of monthly unit values drift when quantities swing with temporary price cuts.
  - `stumping/references/client/layer2-rigor-patterns.md`, seasonal adjustment and official time-series production:
    revisions and turning points are the listed patterns; this build takes the task type's production side (an index
    compiled month by month from a new source) under its own pattern.
  - `dataset-generation/references/layer1-messiness.md`: several feeds for one picture in three layouts, imperfect keys
    (GTINs with and without leading zeros, a retailer's own SKUs, reclassified products), resent weeks, GST-exclusive
    values, a 4-4-5 fiscal calendar, returns, products entering and leaving the range; none on the decisive step.
- **Same-puzzle and abstraction:** gap time, G16, Gate G method_or_model_selection, decision designation_set. Nearest
  drivers on file 0.05 to 0.09 (task95, task500 lineage, task254 lineage, task453 lineage); task254 v2 truncates a
  time-to-event distribution at a lock date, task501 v2 picks a pacing basis by walk-forward test, task453 v1 seasonally
  adjusted across a coverage change; none compiles a price change whose linked path drifts under stockpiling.
- **WARNs answered:** overuse.objective (ETL in four of the last twelve): the lane is ETL. repeat.gate_g
  (method_or_model_selection against task461 and task462): the deciding move is a method, and the mechanism differs (a
  drift-free comparison against linked monthly comparisons, not a record extension or a detection weighting).
  repeat.decision (designation_set against task462): a readiness decision designates the items that move.
  repeat.question_form (which, against task462): the moved items are a which; the deliverable set adds a chart file
  (csv, png, xlsx) so the format set differs.

## Default path

1. Read the introduction plan (`kellesay_rpi_transaction_data_plan_2026.pdf`): an item moves from the January 2027 index
   when its transaction-data 12-month rate to September 2026 is within 1.5 points of its published 12-month rate; a
   product is a GTIN at a retailer; a product's monthly price is its sales value including GST over its units sold,
   returns netted, a retailer week counting in the month in which it ends; a comparison between two months takes the
   products sold in both and weights each by its share of the item's spending averaged over the two months.
2. Conform the three feeds into product-months: Wrenfold's weekly file with each resent week at its latest delivery,
   Gorsedale's fiscal-period weeks to calendar months through its calendar, Calderby's daily sales from its database with
   GST added and its SKUs keyed to GTINs; classify each product to its item through the office's classification file.
3. Build each item's monthly index the usual way: each month compared with the one before at the plan's weights, the
   twelve comparisons linked from September 2025 = 100, and read the 12-month rate at September 2026.
4. Set each rate against the published rate and move the items within 1.5 points.

- **Ends on:** about five items move (bread, yoghurt, butter and spreads, fruit juice and one more); the nine items whose
  goods keep (laundry products, toilet and kitchen rolls, soft drinks, bottled water, coffee, breakfast cereals,
  biscuits, tea, toiletries) end 4 to 12 points under their published rates and stay.
- **Golden:** thirteen items move; three stay because their transaction prices genuinely part from the shelf prices
  (chocolate and sweets and cheese, where Wrenfold's member prices from March 2026 cut what members paid; pasta and rice,
  where own-label lines that dominate spending rose far faster than the branded lines the field sample prices). The
  12-month rate is a comparison of September 2026 with September 2025 that does not route through the offer months'
  weights: directly over the products sold in both months, or over the thirteen months together (GEKS or CCDI), which
  agree within a tenth of a point.

(Figures are the prototype's; the generator's asserted values replace them at stage 3.)

## Stump sentence

The default path builds each item's monthly index the usual way, comparing each month with the one before at the
plan's Tornqvist weights and linking the twelve comparisons, and moves about five items in January 2027; for the nine
items whose goods keep, the linked index ends 4 to 12 points under the published 12-month rate though each product's
own price rose about as much as its shelf price, because stocking up in an offer month makes every month-on-month
comparison weight the cut heavily and the recovery lightly; comparing September 2026 with September 2025 directly, or
over the thirteen months together, moves thirteen and holds only chocolate and sweets, cheese and pasta and rice.

## Three rules

- **Task type:** survey-research-official-statistics/seasonal-adjustment-official-time-series-production (serves ETL):
  a monthly retail prices index compiled from three supermarkets' transaction feeds, conformed into product-months and
  set against the published index over a parallel year.
- **Domain test:** the deciding quantity is each item's 12-month price change compiled from transaction records the way
  price statisticians compile it: monthly unit values per product, spending-weighted superlative comparisons between
  months, and a comparison free of the drift that linked superlative comparisons show when temporary price cuts come
  with stockpiling.
- **Swap:** "move the items whose 12-month price change from the supermarkets' sales records is within 1.5 points of
  the published one" with a hospital's nouns ("move the wards whose 12-month change in cost per admission from the
  billing records is within 1.5 points of the published one") loses what decides it: a price cut that pulls a stored
  good's purchases forward and empties the month after, so spending weights swing against price in consecutive months;
  admissions are not stockpiled when a tariff dips.
- **Layer 1:** three feeds in three layouts (Wrenfold's weekly CSV with resent weeks, Gorsedale's 4-4-5 fiscal-period
  file, Calderby's daily point-of-sale database with values net of GST and its own SKUs keyed to GTINs through a lookup);
  GTINs with and without leading zeros; the office's classification file with reclassifications by effective date;
  returns as negative units; products entering and leaving the range. Each comes from the system named; nothing is
  placed to be caught, and every item is neutral to the call (asserted per item at stage 3).
- **Layer 2:** estimation_fit (chain-linked aggregation): the choice that flips the call is building the 12-month rate
  from a comparison that does not chain the twelve monthly comparisons through the offer months' spending weights.
- **Decisive step:** with quantities that jump in an offer month and fall below normal in the month after, a
  spending-weighted comparison of consecutive months gives the cut more weight than the recovery, so the linked index
  drifts below every product's own change; the 12-month rate has to come from comparing September 2026 with September
  2025 directly, or from a multilateral comparison over the thirteen months, which agree.
- **Not semantics:** every field read correctly (values, units, returns, weeks, GST, keys, classifications) and the
  plan's comparison formula applied to each pair of consecutive months still leaves the nine storable items 4 to 12
  points under; no field, code or unit carries the drift, which lives in how the comparisons are combined.
- **Not rule application:** the plan fixes the quantity (each item's 12-month rate to September 2026 from transaction
  records), the 1.5-point line, the product, the monthly unit value, the week rule and how two months are compared; it
  says nothing on how a year's change is built from the months, so executing every stated rule month by month and
  linking the comparisons files the five-item answer.
- **Analyst test:** a strong analyst who conforms the three feeds correctly, reads the plan and builds each item's
  monthly index the usual way, linking the plan's month-on-month comparisons, moves the default path's `Ends on:`
  items, about five instead of thirteen, the nine storable items 4 to 12 points under their published rates.
- **Estimand:** the plan's 12-month rate: the percentage change in an item's prices from September 2025 to September
  2026 compiled from the three supermarkets' transaction records, each product a GTIN at a retailer priced at its
  monthly unit value including GST, products weighted by their spending, set against the item's published 12-month rate
  to September 2026; an item moves when the two differ by 1.5 points or less.
- **No decoy:** no document gives a transaction-data rate, a link, an index or a move list; the published index is the
  office's own series, correct for what it measures (shelf prices of a fixed sample), and ranks nothing on the
  decision; no document describes or endorses linking monthly comparisons.
- **No certified replay:** no published or certified figure is reproduced by the golden method and missed by another;
  the published rates are the comparison the plan names, not a control the method must replay.
- **Lesson:** a superlative index of transaction data linked month to month drifts when sales come with stockpiling;
  a year's price change compares the year's two ends directly or across all months at once. No build on file compiles a
  price index or meets path dependence in linked comparisons.

## Tried and rejected

- ET20's own world (EPA PM2.5 design values for a plant site): its monitoring task type serves anomaly detection and
  data quality, and Physical & Environmental Sciences' ETL task type is banned for this draw after task462; not drawn.
- A custom sector's real output summed from chained volume components (national accounts non-additivity): real, but
  second-order (0.2 to 0.8 points a year on realistic deflators) and readable as a definition (chained volumes do not
  add), which a judge may class as semantics; dropped at the draw.
- Differential item functioning screens for field-test items (test equating): the filed estimand ("examinees of equal
  proficiency") names the matching, so the decisive step reads as rule application; dropped at the draw.
- Healthcare payment-claims ETL: completion of recent claims is maturity_censoring (banned for this draw), PMPM as a
  ratio of totals is grain_or_unit (banned), contract-order reconciliation is rule application; dropped at the draw.
- Scanner prototype with offers in every month including the year's two ends: GEKS and the time-product dummy parted
  from the direct comparison by 2 to 4 points in the heavily promoted items, leaving the method among drift-free indices
  open; kept the Septembers and their neighbouring months free of offers (the retailers' campaign calendar runs November
  to July) and the range changes neutral, after which direct, GEKS and TPD agree within 0.12 point.
