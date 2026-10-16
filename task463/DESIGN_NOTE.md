# task463 design note: Kellesay RPI transaction data readiness (architecture 1)

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task463.json`, registered 2026-10-16, re-keyed at stage 3 the same day
  (below). Heart WARN; the older same-puzzle and same-driver signatures (population, G16) against task453 v1, task104,
  task134 v1, task70 v2 and task501 (lineage) are differentiated on the card. The WARNs are answered below.
- **Re-key at stage 3:** task233 (registered 21:39) and task148 v2 (registered 15:08 and shipped while this draw was
  being filed) reached the guard after the draw's check, and `guard.py heart` blocked on shape 07, the role family and
  the forcing event against task233 and on the time gap with G16 against task148. Keyed again on the skill's own
  definitions: the gap is population first (stumping 1.4: what one row is against one decided unit; twelve month-pair
  comparisons stand in for the one 12-month comparison the call is scored on), the shape 10 (each item scored against
  the 1.5-point line), the stakeholder redrawn as the transaction-data programme manager who owns the introduction plan,
  the forcing event the January 2027 source cutover. The prompt, the call and every graded figure are unchanged.
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
- **Shape:** 10, a scorecard of sixteen items against the 1.5-point line. Arithmetic: for each of sixteen RPI items the lines compared, the
  transaction-data 12-month rate to September 2026, the published rate, the difference and whether it moves (80); the
  moved set and its count (2); the asks (each supermarket's average days to complete monthly records, 3; each item's
  2025 coverage, 16); the chart's named parts (5); the conformed product-month file (2): 108.
- **Strategy:** other (index-number path dependence; no vocab key names it: it is not a grain, population, censoring or
  composition choice) on the population gap (the month-pair comparisons are not the decided unit, the item's one
  12-month comparison) with the time gap behind it. Generators G16 (method selection) decisive, G6 (the quantity mix
  swings between an offer month and the month after) and G13 (horizon: the year is one comparison of two months, not
  twelve) behind.
- **World:** Statistics Kellesay, the statistics office of Kellesay (an invented self-governing island in the British
  Isles with its own pound at par and a 5 per cent GST), compiles the Kellesay Retail Prices Index monthly. Its sixteen
  packaged grocery and household items are priced by field collection (a collector's shelf price for a fixed sample of
  products on one day a month). Since September 2025 the island's three supermarket groups, Wrenfold Stores, Gorsedale
  Co-operative and Calderby's, have sent their full sales records; the office's introduction plan (June 2026) moves an
  item to transaction data from the January 2027 index when, over the parallel year, the two sources agree on its
  12-month rate to September 2026 within 1.5 points.
- **Forcing fact:** the January 2027 index takes its first items from transaction data, and the island's Statistics
  Code requires two months' notice of a change of method, so the notice is published on 13 November 2026. The call
  faces forward (which items the 2027 index takes from transaction data) on a closed parallel year.
- **Forum and forcing event:** line_manager_or_team (the transaction-data programme manager recommends, the Chief
  Statistician signs), cutover_or_migration (the January 2027 source cutover). Organisation
  research_or_statistics_office; role programme_officer. Persona from `guard.py names --geo "United Kingdom" --seed
  463`: Diana Lawson (transaction-data programme manager, owner of the introduction plan and the data dictionary).
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
- **Same-puzzle and abstraction:** gap population, G16, Gate G method_or_model_selection, decision designation_set.
  Nearest drivers on file 0.05 to 0.09 (task95, task500 lineage, task254 lineage, task453 lineage); task453 v1 took a
  dated step out of a labour series before its seasonal factors, task104 replays a self-adapting scorer, task134 v1
  projected returns under competing risks, task70 v2 built per-record dates under a class rule; none compiles a price
  change whose linked path drifts under stockpiling.
- **WARNs answered:** repeat.gate_g and overuse.gate_g (method_or_model_selection against task233, six of the last
  twelve): the deciding move is a choice between index constructions, and the mechanism differs from task233's
  (nonresponse departing from its allocation); no other Gate G key is honest. repeat.decision (designation_set against
  task233): a readiness decision designates the items that move. repeat.question_form (which, against task233): the
  moved items are a which; the deliverable set (xlsx, csv, png) differs from task233's.

## Default path

1. Read the introduction plan (`rpi_transaction_data_introduction_plan_2026.pdf`): an item moves from the January 2027
   index when its 12-month rate from transaction data is within 1.5 points of its published 12-month rate to September
   2026; a product line is a GTIN at one supermarket; a week belongs to the month in which it ends; a line's monthly
   price is its sales value with GST over its units, returns netted; the lines compared are those each supermarket sold
   in every month of the parallel year; each item's index is compiled monthly over them, September 2025 = 100, a line
   counting by its spending share as in a Törnqvist index; the 12-month rate is the index's change from September 2025
   to September 2026.
2. Conform the three feeds into product-months: Wrenfold's weekly file with each resent week at its latest extract,
   Gorsedale's fiscal weeks dated through its calendar and its EANs padded to 13 digits, Calderby's daily rows through
   its SKU table with 5 per cent GST added; classify each line through the office's classification and keep the lines
   sold in every month.
3. Compile each item's monthly index the usual way: each month compared with the one before at the plan's Törnqvist
   weights, the twelve comparisons linked from September 2025 = 100, and read the 12-month rate at September 2026.
4. Set each rate against the published rate and move the items within 1.5 points.

- **Ends on:** five items move (Bread, Pasta and rice, Yoghurt, Butter and spreads, Fruit juice); the nine items whose
  goods keep end 4.7 to 8.4 points under their published rates and stay (Breakfast cereals -3.6 against 1.8, Biscuits
  -2.6 against 2.6, Coffee -0.9 against 5.8, Tea -3.6 against 1.4, Soft drinks -4.9 against 2.3, Bottled water -4.0
  against 0.7, Laundry products -5.8 against 2.6, Toilet and kitchen rolls -3.7 against 2.5, Toiletries -4.2 against
  2.4), and Pasta and rice moves at 2.9 against 2.4.
- **Golden:** thirteen items move: Bread, Breakfast cereals, Biscuits, Yoghurt, Butter and spreads, Coffee, Tea, Soft
  drinks, Bottled water, Fruit juice, Laundry products, Toilet and kitchen rolls and Toiletries, each within 0.8 points
  of its published rate; Pasta and rice (4.7 against 2.4), Cheese (-0.2 against 2.7) and Chocolate and sweets (-0.3
  against 2.5) stay, their transaction prices parting from the shelf prices for real (own-label lines that rose fastest
  carry most of pasta and rice's spending; Wrenfold's member prices from March 2026 cut what members paid for branded
  cheese and chocolate). The 12-month rate compares September 2026 with September 2025 directly over the lines compared
  (Törnqvist); GEKS and CCDI over the thirteen months and a direct Fisher give the same sixteen rates to the tenth.

## Stump sentence

The default path builds each item's monthly index the usual way, comparing each month with the one before at the
plan's Törnqvist weights and linking the twelve comparisons, and moves five items in January 2027 (Bread, Pasta and
rice, Yoghurt, Butter and spreads, Fruit juice), the nine items whose goods keep ending 4.7 to 8.4 points under their
published 12-month rates (Laundry products -5.8 against 2.6, Coffee -0.9 against 5.8) though each linked index
ends below every one of its own lines' changes, because stocking up in an offer month makes every month-on-month
comparison weight the cut heavily and the recovery lightly; comparing September 2026 with September 2025 directly, or
over the thirteen months together, moves thirteen and holds only Pasta and rice, Cheese and Chocolate and sweets.

## Three rules

- **Task type:** survey-research-official-statistics/seasonal-adjustment-official-time-series-production (serves ETL):
  a monthly retail prices index compiled from three supermarkets' transaction feeds, conformed into product-months and
  set against the published index over a parallel year.
- **Domain test:** the deciding quantity is each item's 12-month price change compiled from transaction records the way
  price statisticians compile it: monthly unit values per product line, spending-weighted superlative comparisons, and
  a comparison free of the drift that linked superlative comparisons show when temporary price cuts come with
  stockpiling.
- **Swap:** "move the items whose 12-month price change from the supermarkets' sales records is within 1.5 points of
  the published one" with a hospital's nouns ("move the wards whose 12-month change in cost per admission from the
  billing records is within 1.5 points of the published one") loses what decides it: a price cut that pulls a stored
  good's purchases forward and empties the month after, so spending weights swing against price in consecutive months;
  admissions are not stockpiled when a tariff dips.
- **Layer 1:** three feeds in three layouts (Wrenfold's weekly CSV with two February weeks resent after a till fault,
  Gorsedale's 4-4-5 fiscal-period file with EANs held as numbers, Calderby's daily point-of-sale database net of GST
  with returns as negative units and its own SKUs keyed to GTINs); retailer weeks running Sunday to Saturday and Monday
  to Sunday across month ends; lines entering and leaving the range; out-of-scope lines and two reclassified between
  out-of-scope items. Each comes from the system named; nothing is placed to be caught, and each mishandled leaves the
  call and the critical components where they are (asserted per item).
- **Layer 2:** estimation_fit (chain-linked aggregation): the choice that flips the call is building the 12-month rate
  from a comparison that does not chain the twelve monthly comparisons through the offer months' spending weights.
- **Decisive step:** with quantities that jump in an offer month and fall below normal in the month after, a
  spending-weighted comparison of consecutive months gives the cut more weight than the recovery, so the linked index
  drifts below every line's own change; the 12-month rate has to come from comparing September 2026 with September 2025
  directly, or from a multilateral comparison over the thirteen months, which agree.
- **Not semantics:** every field read correctly (values, units, returns, weeks, GST, keys, classifications) and the
  plan's comparison applied to each pair of consecutive months still leaves the nine storable items 4.7 to 8.4 points
  under; no field, code or unit carries the drift, which lives in how the comparisons are combined.
- **Not rule application:** the plan fixes the quantity (each item's 12-month rate, the change in its monthly
  transaction-data index), the 1.5-point line, the product line, the month, the monthly unit value, the lines compared
  and that a line counts by its spending share as in a Törnqvist index; it says nothing on how a month's index reaches
  back to September 2025 (through the months between, directly, or over all months at once), so executing every stated
  rule month by month and linking the comparisons files the five-item answer.
- **Analyst test:** a strong analyst who conforms the three feeds correctly, reads the plan and builds each item's
  monthly index the usual way, linking the plan's month-on-month comparisons, moves the default path's `Ends on:`
  items, five (Bread, Pasta and rice, Yoghurt, Butter and spreads, Fruit juice), the nine items whose goods keep left 4.7
  to 8.4 points under their published rates, instead of thirteen.
- **Estimand:** the plan's 12-month rate (3.6): the percentage change in an item's transaction-data index from
  September 2025 to September 2026, the change in the item's prices over the year, from the three supermarkets'
  records, over the lines each sold in every month (3.4), each line priced at its monthly unit value with GST (3.3) and
  counting by its spending share as in a Törnqvist index (3.5), set against the item's published 12-month rate to
  September 2026; an item moves within 1.5 points (4.1).
- **No decoy:** no document gives a transaction-data rate, a link, an index or a move list; the published index is the
  office's own series, correct for what it measures (shelf prices of a fixed sample), and ranks nothing on the
  decision; no document describes or endorses linking monthly comparisons, and no column flags an offer.
- **No certified replay:** no published or certified figure is reproduced by the golden method and missed by another;
  the published rates are the comparison the plan names, not a control the method must replay.
- **Lesson:** a superlative index of transaction data linked month to month drifts when sales come with stockpiling; a
  year's price change compares the year's two ends directly or across all months at once. No build on file compiles a
  price index or meets path dependence in linked comparisons.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 each item's unit value, its spending over its units (12 move: Coffee stays) | the plan's 3.1 and 3.3 price each line, not the item | spending and units per row | yes: an average price | no | no | one ratio per month | readable |
| R1 unweighted price relatives, direct or linked (14 move: adds Pasta and rice) | the plan's 3.5 weights each line by its spending | no weight column; values and units | yes: the geometric mean the field collection uses | no | no | a mean of logs | readable |
| R2 linked month-on-month Törnqvist (5 move; the default path) | the plan's 3.5 compiles the index monthly at Törnqvist shares, which each link satisfies | product-months by month | yes: a monthly index built month to month | no | no | a product of twelve links | readable |
| R3 September 2026 against September 2025 by a comparison that does not route through the offer months' weights, direct or multilateral (decisive) | no: the plan defines the index (monthly, September 2025 = 100, Törnqvist shares) and the 12-month rate as its change, the change in the item's prices over the year; no sentence names linking, drift, a direct comparison or a multilateral index | no column flags an offer, a promotion or a stocked-up month; prices and units only | no: the reflexes (link the months, Fisher for Törnqvist, every line for the lines compared, unweighted relatives) land on 5, 5, 5 or 14 items; only a comparison that leaves out the offer months' weights reaches 13 | no | no | one comparison per item | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | item | the RPI item the office's classification gives the line in the month | the supermarkets' own categories | not executable: the feeds carry no category | the plan's 3.1 |
| SF2 | product line | a GTIN at one supermarket | a GTIN pooled across the supermarkets | same call | the plan's 3.1 ("the same GTIN at two supermarkets is two lines"); asserted |
| SF3 | month | a calendar day by its month, a retailer week by the month in which it ends | a week by the month it starts in | same call | the plan's 3.2; asserted |
| SF4 | monthly price | sales value with GST over units, returns netted | Calderby's net value as given; returns dropped | same call | the plan's 3.3; the dictionary's GST rate; asserted |
| SF5 | lines compared | the lines each supermarket sold in every month of the parallel year | the lines sold in both Septembers; every line in each comparison | same call | the plan's 3.4; asserted |
| SF6 | weights | each line's spending share averaged over the two months a comparison holds (Törnqvist) | Fisher; Laspeyres on September 2025 quantities | same call (Fisher the same sixteen rates; Laspeyres the same critical components) | the plan's 3.5; asserted |
| SF7 | 12-month rate | the change in the item's index from September 2025 to September 2026 | the average of the year against the year before | not executable: the records start in September 2025 | the plan's 3.6 |
| SF8 | within 1.5 points | the two rates, each to one decimal, differ by 1.5 or less | unrounded rates; strictly less than 1.5 | same call: no item within 0.6 of the line | the plan's 4.1; asserted |
| SF9 | published 12-month rate | the published rate for September 2026, one decimal | recomputed from the rounded published indices | same call | the published workbook's notes; asserted |
| SF10 | a resent week | its latest extract | both extracts; the first | same call | the dictionary (extract date); asserted |
| SF11 | Gorsedale's EAN | the barcode as 13 digits | the number as written | same call (imported lines unclassified otherwise) | the classification's GTINs; asserted |
| SF12 | rounding | rates and differences to one decimal | two decimals | same call | the prompt's rounding sentence |
| SF13 | a line's share of the item's spending | across the three supermarkets' lines of the item | each line's share within its supermarket, the supermarkets combined by their spending | same call, the same sixteen rates | the plan's 3.5 ("the item's spending"); asserted |

## Ladder

| Rung | Construction | Items moving | Nearest the line |
|---|---|---|---|
| R0 | each item's unit value, its spending over its units | twelve (Coffee stays at 1.8 against 5.8) | Coffee -4.0; Breakfast cereals +0.8 |
| R1 | unweighted price relatives, direct or linked | fourteen (adds Pasta and rice at 2.9 against 2.4) | Pasta and rice +0.5 |
| R2 | linked month-on-month Törnqvist (the default path) | five: Bread, Pasta and rice, Yoghurt, Butter and spreads, Fruit juice | Bread +0.5 (moves); Bottled water -4.7 the nearest held |
| R2a | linked month-on-month Fisher | the same five (Pasta and rice at 3.1); the nine storable items still held | Coffee -5.5 |
| R3 | September 2026 against September 2025, direct Törnqvist over the lines compared (golden; GEKS, CCDI and direct Fisher alike) | thirteen | Breakfast cereals +0.8 (moves); Pasta and rice +2.3 (stays) |

- **Margins:** the golden's thirteen sit within 0.8 of their published rates (0.7 inside the line), Breakfast cereals
  alone above 0.5; its three stays sit 2.3 to 2.9 away (0.8 outside), Pasta and rice the only one under 2.8; the
  default path's nine wrongly held sit 4.7 to 8.4 points under.
- **Dominance:** in the nine storable items the stocked-up month after an offer runs at 55 to 65 per cent of a line's
  normal sales while the offer month runs at about 2.7 to 4 times normal (generator parameters, `world.ITEMS`), so the linked index drifts 4.6 to 8.4 points
  below the golden; in the four fresh items that move, the month after an offer is normal and the links drift 0.4 or
  less.
- **Grid:** two choices (path: linked or drift-free; weights: spending or none) give four cells: linked and weighted
  five, linked and unweighted fourteen, drift-free and weighted thirteen (golden), drift-free and unweighted fourteen
  (asserted).
- **Worth:** every storable item's 12-month rate moves 4.6 to 8.4 points between R2 and the golden; the fresh items'
  rates move 0.4 or less, so the rung bites only where goods keep.
- **Data-native structure:** the nine storable items' linked indices end 0.9 to 5.8 per cent down over the year (Coffee
  -0.9, Laundry products -5.8) while their lines' own price changes run from -0.8 to +9.3 per cent: each linked index
  ends below every one of its own lines' changes.
- **R0's miss is real:** coffee buyers move to own label over the year (own-label units up about 30 per cent, branded
  down about 10), so the item's average price per unit falls behind every line's price; the plan prices lines, not
  the item, so the move leaves the golden where it is.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the lines each supermarket sold in every month of the parallel year, by item | the plan's 3.4 (SF5) |
| 2 | Unit of account | the product line, a GTIN at one supermarket | the plan's 3.1 (SF2) |
| 3 | Attribution window | September 2025 to September 2026; a week by the month it ends in | the plan's 3.2 and 3.6 (SF3) |
| 4 | As-of dating | the feeds as received to 7 October 2026; the published rates of 15 October 2026 | the manifest; the published workbook |
| 5 | Version basis | each resent week at its latest extract; Calderby's final extract | SF10 asserted |
| 6 | Denominator | the item's spending over the lines compared, for the weights | the plan's 3.5 |
| 7 | Weighting | spending shares as in a Törnqvist index | the plan's 3.5 (SF6) |
| 8 | Window length | twelve months, September to September | the plan's 3.6 |
| 9 | Boundary inclusivity | within 1.5 points moves, either way | the plan's 4.1 (SF8) |
| 10 | Rounding path | rates to one decimal, the difference of the rounded rates | SF8, SF12 |
| 11 | Tie-break | none needed | no item within 0.6 of the line; the moving and staying items nearest it each 0.3 or more clear of the next (asserted) |
| 12 | Maturity and censoring | every month of the parallel year is closed and delivered | the delivery log; the manifest |
| 13 | Order of operations | conform, classify, keep the lines compared, compare the two Septembers | C1: every drift-free comparison gives the same rates (asserted) |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | a resent week replaces the first extract | SF10 |
| 16 | Identity normalisation | EANs padded to 13 digits; Calderby's SKUs through its SKU table | SF11 |
| 17 | Netting against gross | returns netted | the plan's 3.3 |
| 18 | Dimensional units | pounds with GST; Calderby's net values grossed up at 5 per cent | the dictionary; SF4 |
| 19 | Code and status semantics | Wrenfold's extract dates; the classification's validity dates | the dictionary |
| 20 | Integerisation | none | n/a |
| 21 | Clause scope | the test applies to each of the sixteen items alike | the plan's 4.1 |
| 22 | Forward window contents | the January 2027 index takes the items that pass on the closed parallel year | the plan's 1.1 and 4.1 |

## Literal reader

Executed word for word, the plan asks for each item's index compiled monthly over the lines each supermarket sold in
every month, September 2025 = 100, each line priced at its monthly unit value with GST and counting by its spending
share as in a Törnqvist index, and for the 12-month rate as the index's change from September 2025 to September 2026,
the change in the item's prices over the year; it moves the items within 1.5 points of the published rate. The text
leaves open how a month's index reaches back to September 2025: compared with it directly, over all thirteen months at
once (GEKS, CCDI) or through the months between (linked). The direct and multilateral constructions file the thirteen,
with the same sixteen rates to the tenth, and a direct Fisher the same rates; the linked index files five, and in the
nine items whose goods keep it ends below every one of its own lines' changes (Laundry products -5.8 per cent while
its lines' changes run from -0.8 to +5.5), which no change in the item's prices can do: the data rule it out, as the first
judge pass also found.

## Oracles

None ties only under the golden. The published index is the comparison the plan names: it measures the shelf prices of
a fixed field sample, differs from the golden in the three items whose transaction prices part from the shelf prices,
and confirms no method. The field quotes are the published index's own inputs, declared a distractor; the retail sales
index is a neighbouring statistic, declared a distractor.

## Ask sheet

- **Ask A, each supermarket's average number of calendar days after a month's end until its records for that month
  were complete, over the thirteen months of the parallel year (3 figures, one decimal).** H18 home: the switch's production
  timetable (a month's index is compiled only once all three supermarkets' records for it are in). Path: the delivery
  log (file, covers from, covers to, received), the plan's week rule (3.2) and the dictionary's note that dates are
  Kellesay dates (three files, six columns). Primary device: D8, a clock against the island's dates: the log stamps each
  file's arrival in UTC, and the supermarkets' nightly exports reach the server just after midnight Kellesay time, so in
  British Summer Time (September and October 2025, April to September 2026) a file's UTC date is the day before its
  Kellesay date; every supermarket's average moves. Hazards: H1 Wrenfold's two February weeks resent on 9 March (the
  month complete only then); H2 Calderby's March extract sent again on 22 April; H3 weeks and fiscal periods crossing a
  month's end (a week's records belong to the month in which it ends). Stops (asserted): UTC dates (the cracker) 1.8,
  7.4 and 8.3 days; weeks by calendar overlap 7.9 and 20.6 (Calderby's daily extracts unchanged at 8.6); the first file
  for each month in place of the last (Wrenfold's resend and Calderby's second extract missed) 1.7, 8.0 and 7.4; the
  golden 2.0, 8.0 and 8.6. Realism: an office's receipt server logs in UTC while its timetable runs on local dates.
- **Ask B, each item's 2025 coverage: the three supermarkets' 2025 retail sales with GST as a share of households' 2025
  spending on it (16 figures, whole per cent).** H18 home: how much of each item's household spending the transaction
  data hold, a measure every item carries that the call does not turn on. Path: the supermarkets' annual returns (three
  sheets in three layouts), the office's category map, the household spending estimates and the dictionary's GST rate
  (four files, ten columns). Primary device: D7, codes reissued: Wrenfold's 2025 return lists its categories under the
  codes of its 2025 hierarchy, while the office's map holds the codes its categories carried before, so the code join
  completes (only toiletries' new department code, P310, finds no row) and puts every category's sales on another item;
  the names agree. Hazards: H4 Calderby's sheet net of GST (5 per cent added); H5 Gorsedale's trade rows (sales on trade
  accounts) beside its retail rows. Stops (asserted): the code join (the cracker) moves every item 3.1 to 39.8 points
  (Bread 47 against 68, Toiletries 33 against 73); trade sales kept move the nine items with trade sales and Calderby left
  net moves every item; the golden 55 to 77 per cent.
  Realism: a retailer renumbers its category hierarchy and the statistics office's map lags a year.
- **The construction layer:** each item's lines compared, transaction-data 12-month rate, published rate, difference and
  verdict, the moved set, the chart and the conformed product-month file; the cracker has them.
- **Main population zero-counts (asserted):** the main call reads no delivery log, annual return, category map or
  household spending row (the call and every rung computed with those files deleted are identical); the asks read no
  feed, classification or published row (Ask A and B computed with those files deleted are identical). No device or
  hazard row sits in a file the call reads.
- **Hazard table (asserted):** H1 moves Wrenfold's average (February complete on 9 March); H2 Calderby's (March complete
  on 22 April); H3 Wrenfold's and Gorsedale's; H4 every item's coverage; H5 the nine items with trade sales.
- **Rounding edges (asserted):** each supermarket's average 0.03 or more from its tenth's edge; each coverage 0.1 or more
  from its whole-per-cent edge; each item's transaction-data rate 0.015 or more from its tenth's edge under every
  drift-free comparison.
- **Referee:** none; no total in any ask file ties only under one handling.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| A, average days to complete records by supermarket | applies the week rule, takes the resend and Calderby's second extract as the last files, reads each arrival on its UTC date | miss |
| B, coverage by item | grosses up Calderby, drops Gorsedale's trade rows, joins each return to the map on the category code | miss |

- Mirror leakage: about 10 per cent of ask weight (a response on R2 keeps the conformed product-month file; it misses
  every Ask A and Ask B figure on the same devices as the cracker).
- Pair ceiling: 33.7 (planning weights 38 / 7 / 55 with the call, each item's rate, difference and verdict and the chart
  in the main block and r = 5; the ask weight spread over 21 criteria: A 3, B 16, the file 2; the cracker keeps the
  file, 2 of 21 or 0.095, 38 + 7 + 5.2 = 50.2; the mirror keeps r, instruction-following and the file, 5 + 7 + 5.2 =
  17.2; average 33.7), rerun from the generated rubric at ship.

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Effect (asserted) |
|---|---|---|---|---|
| Two February weeks resent after a till fault | Wrenfold's extract job | Wrenfold weekly file | both extracts kept | call and critical components unchanged |
| EANs held as numbers | Gorsedale's export | Gorsedale period file | joined unpadded, imported lines lost | call and critical components unchanged |
| Values net of GST | Calderby's point-of-sale database | Calderby database | not grossed up | call and critical components unchanged |
| Returns as negative units | Calderby's point-of-sale database | Calderby database | returns dropped | call and critical components unchanged |
| Weeks crossing month ends | Wrenfold's and Gorsedale's calendars | both weekly files | a week by its first day | call and critical components unchanged |
| Lines entering and leaving | all three ranges | all three feeds | every line compared | call and critical components unchanged |
| Out-of-scope lines, two reclassified | the office's classification | classification | kept with their items | none (other items) |


## Pre-ship check

- **Three rules, re-read against the built pack.** Domain: the deciding quantity is each item's 12-month price change
  compiled from transaction records the way price statisticians compile it (monthly unit values per product line, a
  spending-weighted superlative index, and a construction free of the drift linked comparisons carry under stockpiling);
  linking the month-on-month comparisons moves five, unweighted relatives fourteen, the item's unit value twelve. Two
  layers: the Layer 1 inventory above, each main-call item asserted neutral (R2: SF3, SF4, SF5, SF10, SF11) and each ask
  item confined to its ask with zero main-call rows (the separation checks); Layer 2 the drift-free construction. The
  decisive step is none of the three banned kinds, each executed in `checks.py`: not a plant (R3c: no line's 13-month
  series of units and unit values repeats another's; no document names a move, a transaction-data rate, a link, a
  drift or a multilateral index; no feed carries an offer or promotion column); not data semantics (R2 and SF1 to SF12:
  every field mishandled leaves the call and the critical components where they are, and every field read correctly
  still leaves the default path on five); not rule application (R3a: every filed rule executed with linked comparisons
  on the clean truth files the five; R3b: only a drift-free construction files the thirteen, while unweighted
  relatives, the unit value and linked Fisher land elsewhere; since the round-1 fix the plan defines the monthly index
  and the rate as its change and leaves the construction to the analyst).
- **Gates.** 15 files in 5 formats (csv, pdf, sqlite, txt, xlsx); Calderby's daily_sales at 287,409 rows; two
  distractors (the field quotes and the retail sales index) the solution never reads, the call and every ask unchanged
  with them deleted; 69 checks; `verify.py` from the bundle alone; two builds byte-identical; `figures_check.py`,
  `precut.py` (49) and `voice-check.py` exit 0; `leak.py` REVIEW (no LEAK); guard heart WARN (answered in the draw);
  surface promoting task462 (back to back: the population gap and designation_set) and task70 and task104 (older
  same-driver signatures, differentiated on the card) for the author's read; the containers carry the fiction's owners
  and dates (H1 audit clean); the folder manifest, whose column set repeated task462's, reshaped as the programme's
  folder register; the real Jersey names among the outlets and Calderby's stores (St Aubin, Northfield, Mont Cochon)
  renamed Elskirk, Thornsay and Gullhaven.

## Leak check

`leak.py --asof 2026-10-21`: REVIEW, no LEAK. The sixteen item codes are stated inputs (`metadata.json`); each REVIEW
line answered:
- Gorsedale's period file carries 1.3 to 1.5: pack sizes in product descriptions (4X330ML, 1.4L, 1.5L). Harmless.
- The plan carries 1.1, 2.2, 3.1, 3.3 and 3.5: its section numbers. Harmless.
- The plan carries 1.5: the filed line of 4.1, which the call needs. Harmless.
- The plan carries the item names: Table 1 lists the sixteen items assessed, the candidate set the prompt names.
  Harmless.
- The plan carries some stump-paragraph terms (change, points, statistics, compiled, programme, manager): a price
  statistics plan's own vocabulary; it names no link, chain, direct comparison or multilateral index (asserted in
  R3c). Harmless.
- Gorsedale's fiscal calendar carries dates after 21 October 2026: the FY2027 calendar lists its whole year to 31
  January 2027, as a calendar does (H16 allow-list). Harmless.

**Reader, round 1** (the first cut): Q1 none; Q2 none (the published rates are the comparator); Q3 none; Q4 none; Q5
quoted the plan's 3.1 to 3.6 and 4.1, reading 3.6 as "a Tornqvist chain or direct comparison"; Q6 "mostly rule
application": with 3.5's weights "averaged over the months compared" beside 3.6's change from September 2025 to
September 2026, a word-for-word reader computes the direct comparison from the text. Fixed at design level: 3.5 now
compiles a monthly index at Törnqvist shares and 3.6 takes the rate as the index's change, so the construction is the
analyst's choice and the data rule out linking (back to stage 2, precut re-run, `## Tried and rejected`). Every REVIEW
line harmless. Realism tells: the published item indices flat from September to October for most items (fixed:
reviews in any month on each line's own calendar, the field history's and the independents' staggered; seven items
still flat from September to October 2025, a promotion-free month in which no sampled line was repriced); "Tornqvist"
unaccented (now Törnqvist in the plan, the golden notes and the write-up); the dictionary dated after the receipt log
(the log now pulled on the folder's date, 21 October); the fresh produce and meat categories no larger than tea in the
annual returns (now at their weight); the round register and dictionary counts agree because they count the same rows;
the future dates against the reader's clock are the fiction's (earlier builds the same).

**Reader, round 2** (the plan and prompt changed): Q1 none (the plan's 3.4 and 3.5 are procedure, not a pitfall); Q2
none; Q3 a weak candidate, the folder register, "real programmes do keep such registers"; Q4 none; Q5 the plan's 3.1 to
3.6, with "the text does not fix how a month's index is built", chained month to month or compared directly with
September 2025, flagged as the largest determinism risk (the judge's ground: pass 1 excluded linking on the data, and
the re-judge reads the reworded text); Q6 the pipeline is procedure, and "if the weighting or index-form choice is left
open and decisive, it is the analytical element, but the text doesn't mark it": it is open and decisive (thirteen
against five), so the decisive step reads from outside as the analytical choice the design intends. Every REVIEW line
harmless. Realism: the classification's assignments nearly all dated 1 January 2019 for a programme begun in 2025 (fixed:
the lines on sale before the parallel year carry the summer 2025 batch dates by department, later lines their first
month); a line's share within its supermarket raised as unfiled (closed: SF13, the same sixteen rates); the September to
October flatness in some published items again called minor; the register's and the delivery log's Calderby's counts
differ by the March extract the second delivery replaced.

## Determinism judge

**Pass 1** (the first cut): DETERMINISTIC, FIX_NOW. Every figure reproduced; chain-linking "excluded on the data" (it
ends below every line's own change in the nine items). Two ask-level forks pinned in the prompt: Ask A's days as
calendar days (elapsed time from midnight gives 1.1, 7.0 and 8.0) and the product-month file's scope and fields (every
product-month of the sixteen items' lines with units, sales with GST and unit price). Gate G method_or_model_selection,
analytical_non_defect; Gate H domain and layers pass, decisive step analytical but borderline (the literal plan named
September to September); Gate F moderate. The borderline Gate H and the reader's Q6 are the same finding, fixed as
above.

**Pass 2** (the re-judge, on the cut after the round-1 fixes; the shipped cut differs from it only in the
classification's valid_from dates, which no figure reads): DETERMINISTIC, APPROVE. Every figure reproduced (the sixteen
rates, direct Fisher and GEKS agreeing to the tenth, the 13/3 split with Breakfast cereals 0.82 inside and Pasta and
rice 2.32 outside, the days, the coverage, 14,364 rows over 1,172 lines with 1,012 compared). The one surviving fork is
the construction, direct against linked: "the intended method choice, not a semantic gap", the linked index ending
below every line's own change in the nine items. Gate F strong (linking is "the standard monthly chain, and the plan's
phrase 'compiled monthly' invites it"); Gate G method_or_model_selection, analytical_non_defect, no surface read, no
sole data defect; Gate H domain pass, layers pass, decisive step analytical. Its optional pin ("comparing each month
with September 2025") is declined: it would file the construction, the decisive step, as a rule.

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
- Per-item nudges calibrated on the drift-free agreement and the line margins alone: the item unit value moved the
  golden's thirteen (Coffee's mix too steady to part it from the line-level index), Bread and Yoghurt tied at 0.7 as the
  moving item nearest the line, Cheese sat 0.1 inside Pasta and rice as the staying item nearest it, and those items'
  rates moved by 0.1 to 0.2 with a week dated by its first day; recalibrated with roles (Breakfast cereals the nearest
  move, Pasta and rice the nearest stay, each rate held under every Layer 1 mishandling) and coffee buyers moving to own
  label over the year, which parts Coffee's unit value from its lines' prices.
- Direct Laspeyres among the converging comparisons: it parts from the superlatives by 0.1 in Chocolate and sweets, where
  members' prices move what members buy; the plan's 3.5 rules it out, and it is asserted as the same call and the same
  critical components only.
- Plan 3.5 with weights "averaged over the months compared" beside 3.6's change "from September 2025 to September
  2026": a word-for-word reader computed the direct comparison from the text alone (the stage 4 reader read the main
  call as following the stated procedure; the judge's Gate H called it borderline and Gate F moderate). 3.5 now
  compiles a monthly index at Törnqvist shares and 3.6 takes the rate as the index's change, so how a month's index
  reaches back to September 2025 is the analyst's choice, and the data rule out linking.
- Price reviews in five fixed months and the field history's reviews on one half-yearly beat: the published item
  indices sat flat from September to October and from August to September for most items (the reader's realism tell).
  Reviews now fall in any month on each line's own calendar, and the field history's and the independents' on their
  own months.
