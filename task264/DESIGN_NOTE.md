# task264 design note

Architecture 1, drawn 2026-10-17 (wave 3, Descriptive lane, sathay3012). Seed DA14: the world (a grocery market-data firm's weekly price index built from its partner chains' scanner data, a GEKS-Tornqvist index within each store format, aggregated across formats), the decision (which of eighteen food categories the 2027 index publishes as stand-alone sub-indices, the rest folding into "other food") and the quantity (whether a category's index holds in every store format) are kept; the seed's mechanism rows were not read, and the pitfall is re-found from the data. The index committee adopts the 2027 structure on Wednesday 9 December 2026 from the 52 retail weeks to Saturday 28 November 2026, the latest the chains have all delivered; every file predates the build and the call (a structure for a year not yet begun) faces forward.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task264.json`, registered 2026-10-17. The firm is a grocery market-data company publishing a weekly scanner price index (`research_or_statistics_office`), its index committee (`committee_or_panel`) adopting the 2027 structure at its December meeting (`vote_or_meeting`); the requester is the firm's head of price indices (`statistical_office_head`); the context artifact is the data team's feed delivery log (`operations_log`); no calibration organ. `guard.py check`: WARN only. `three_rules.strategy_risk` (grain_or_unit) is answered by the analyst test below: every field read correctly, the store-level match is the careful route and still fails. `repeat.gate_g` against task235 (a tracking loss conditioned on a delivery chance; here the elementary unit of a price index) and `repeat.decision` against task465 (counties a reinsurer can write; here categories a price index publishes) are different mechanisms under one label. `test.same_puzzle_older` and `test.same_driver_older` are differentiated on the card against task48 (a population recovered by aggregating up to a pair grain) and task120 v1 (a percentile unit built by a two-hop join); task264 coarsens store rows to the chain that sets the price because a finer match throws away prices the chain's other stores record.
2. Pairing: General Statistics & Data Science (client domain) / missing-data-censoring-measurement-error / Descriptive & Distribution Analysis, a never-built pairing. The setting is retail price statistics; the task type's own object (how unobserved cells are handled) decides the call.
3. Niche: the firm's partner chains send weekly store-by-item sales (units and dollars) from every store in four formats: supermarkets, neighbourhood stores, convenience stores and online. Each chain sets one shelf price for an item across all its stores in a format, changed at its weekly price change, and a movement row exists only where a store sold the item that week. The index committee publishes a category on its own in 2027 only where one national figure holds for every format: its change over the 52 weeks to 28 November 2026 in each format within 1.5 points of its national change.
4. Call and shape: how many of the eighteen categories the 2027 index publishes on their own, and which (`designation_set`, question form how many). Shape 14 (cuts of a distribution, each cut per segment): eighteen categories, each with its change in each of the four formats and nationally, the largest format gap and the verdict.
5. Gate G `method_or_model_selection`, strategy key `grain_or_unit`, decisive generator G2 (the elementary unit of the index is the item at the chain that prices it), then G12 (a store-week with no sale is not a missing price: the chain's other stores record it) and G6 (pooling an item across chains lets shifts between dearer and cheaper chains move the unit value).
6. Data-native sentence: grocery chains price an item alike in all their stores, but a movement row exists only where a store sold the item that week, so a small convenience store that sold none of a slow line in a week still charged the chain's price; matching items store by store keeps a chain's price only in the weeks one particular store happened to sell it, which in convenience leaves the fast lines carrying nearly every comparison, while pooling an item's sales across the format's chains turns the value chain that joined the panel in July, and shoppers' moves between dearer and cheaper chains, into price falls.
7. Sources, one line each:
   - `analytical_tasks/03_descriptive_distribution/DA14`: world, decision and quantity; its pitfall is not used (the note was not read past its Situation). Its matched-pair minimum, filed literally, is a rule's execution.
   - The two-layer design reference's Layer 2 family `estimation_fit` (the estimator fitted to the data's real structure): the matched-model comparisons built at the unit that sets the price. The General Statistics library's missing-data patterns (Rubin's rules, attenuation, delta adjustment) teach other moves; the pattern here is `own:a-store-week-without-a-sale-is-a-known-chain-price`.
   - task463 (a supermarket transaction index whose month-on-month comparisons drift under stockpiling): task264 files a drift-free multilateral comparison; the move here is the unit at which a price is followed, which task463 never turns on.
   - task259 (pay reports read within employers) and task263 (a mass balance of blends) on file in this lane: task259's pooled-reports rung resembles this build's lowest rung only; neither turns on a store-week that sold nothing at a known price.
8. People, drawn with `guard.py names --geo Australia --seed 264`: Christy Chambers (the firm's head of price indices, author of the methodology statement and the paper), Manuel Zamora (the data team's feed delivery lead, owner of the partner register and feed dictionary). Invented names, each screened in checks.py against 17,509 Australian place names and a list of grocery banners, retailers, market-data firms and brands at three edits or containment (H21): the firm Delvett Retail Data and its Delvett Grocery Price Index; banners Haskard Fresh, Brevane Supermarkets, Fremett Foods, Pravard Discount, Gorvery Warehouse (the July chain), Lumbane Local, Ruskett Grocers, Skovard Local, Quorrix, Treskola, Jorvery Stop, Wiskane Online, Pembard Direct and Keskary. Store suburbs and postcodes are real (all 70 pairs checked against the public postcode table).

## Default path

1. Read the committee's terms of reference: a category gets its own 2027 sub-index where its national change over the
   52 weeks to 28 November 2026 is within 1.5 points of its change in each of the four store formats; and the index
   methodology: within each format, every pair of weeks compared by a Tornqvist index weighting items by spending,
   the comparisons combined by GEKS, the change taken from the first four weeks of the window to the last four, the
   national change combining the four format changes with the committee's format weights.
2. Load the movement file (store, item, week, units, dollars), join each store's format from the store register and
   each item's category from the item master.
3. In each format, add each item's units and dollars over the format's stores each week; the item's price is the
   dollars over the units.
4. Run the GEKS-Tornqvist on the items over the 52 weeks; take each category's change in each format.
5. Combine the formats with the committee's weights for the national change and compare each format with it.
6. Publish the categories within 1.5 points in all four formats.

Ends on: 4 categories.
Golden: 10 categories.

Built (checks.py, verify.py): the default path keeps Breakfast cereals, Cheese, Deli and cooked meats and Biscuits, the four categories whose lines the July value chain hardly ranges; the golden keeps ten, its widest gap 1.1 points (Yoghurt and desserts, online) against the nearest category left out at 2.3 (Fresh meat and poultry, neighbourhood).

## Stump sentence

The default path publishes 4 categories because it averages each item's sales over all the format's stores before
comparing weeks, so the value chain that joined the panel in July and shoppers' moves toward cheaper chains read as
price falls in the supermarket format, and six categories' other formats land more than 1.5 points from a national
change pulled down with it; the careful refinement that matches items store by store keeps the supermarkets right
but drops a convenience chain's price in every week one small store sold none of a slow line, so the convenience
change follows the fast lines and still misses (7 categories, four of the golden's dropped and one it folds kept);
following each item at the chain that prices it publishes 10.

## Three rules

Task type: missing-data-censoring-measurement-error (General Statistics & Data Science), which serves Descriptive & Distribution Analysis in the taxonomy; the setting is retail price statistics.
Domain test: the deciding quantity is each category's price change in each store format computed with every store-week that sold nothing treated as what it is, a week that store sold none of the item at the price its chain set for all its stores, which the chain's other stores record, not a missing price; how such unobserved cells are handled is the missing-data task type's own object, and replacing it with the complete-case match at each store, or with a pooled average that ignores who set each price, changes which categories the national figure holds for.
Swap: "which procedure groups' national cost index holds in every hospital type" keeps a grid of changes and a 1.5-point test but loses the shelf price a chain sets for all its outlets each week, the movement row that exists only when an outlet sold the item, and the shopper moving between dearer and cheaper chains, so the store-week that sold nothing at a known price, the thing the call turns on, has no counterpart and the call no longer reads the same.
Layer 1: the chains' weekly feeds as the firm's loader holds them, every load kept: one neighbourhood chain's April movement block resubmitted after a store's rows went missing (the four weekly loads superseded, the delivery log saying so); one neighbourhood chain's tills sending GTIN-13 codes against the item master's GTIN-14 (the loader keeps codes as sent); random-weight lines in kilograms beside packed lines in units (the tills); store markdowns of short-dated stock and register price check overrides on the movement rows (each chain's point-of-sale codes); refits re-coded under new store numbers in every chain, refurbishment closures of two to four weeks, store openings and closures (the chains' store masters, mirrored in the panel store register); the July chain entering at its data agreement; promotion codes in each chain's own vocabulary. Ask-side and outside the call's files: the store sales feed (a rejected resend kept in the table, the July chain's onboarding backfill, one convenience chain's own Sunday week-endings, four chains whose rows repeat the store's weekly total). Nothing is placed to be caught; checks.py asserts the call unchanged under each item's natural mishandling (R2a to R2e).
Layer 2: the estimation_fit family; the matched-model comparisons have to be built at the unit that sets the price, the item at its chain, because a store-level match is a complete-case analysis that drops a known price whenever one store sold nothing, which selects the comparisons on sales activity, while a pooled unit value mixes chains whose prices and shares differ.
Decisive step: following each item at the chain that prices it (the chain's weekly unit value over all its stores in the format), so a store-week with no sale costs no comparison and no two chains' prices are averaged, instead of matching each item store by store (which keeps a chain's price only in the weeks one store sold it) or pooling each item over the format's stores.
Not semantics: every field read correctly (store, chain, format, item, units, dollars, week, and the dictionary's statement that a movement row exists only where a store sold the item) still leaves the analyst matching at the store, the file's own grain, or pooling to the format; no field says at what unit an item's price is followed, and the chain column is read correctly by both wrong routes.
Not rule application: the methodology fixes the estimand (each category's change over the window in each format, every pair of weeks compared by a Tornqvist index weighting items by spending and combined by GEKS, the four-week ends, the national combination and the 1.5-point test) and says nothing about the unit at which an item's price is followed or how a store-week without a sale is treated, so executing every stated rule files the default path's answer.
Analyst test: a strong analyst who reads every rule and field correctly averages each item over the format's stores each week, runs the GEKS-Tornqvist and publishes 4 categories (Ends on: 4 categories), and the careful refinement that matches items store by store publishes 7; following each item at the chain that prices it publishes 10.
Estimand: the committee's terms of reference and the index methodology fix the population (the items of the eighteen food categories sold at the panel's stores in each of the four formats), the outcome (the category's price change from the first four weeks to the last four of the 52 weeks to 28 November 2026, each pair of weeks compared by a Tornqvist index weighting items by spending, the comparisons combined by GEKS), the unit (the category in a format, then nationally with the committee's 2026 format weights) and the comparison (each format's change within 1.5 points of the national change).
No decoy: nothing is planted; no memo, draft, published sub-index or staff note argues a category, a change or a structure, the July partner is the firm's data agreement taking effect, and the chains price centrally because that is how they set prices.
No certified replay: the method is not recovered by reproducing published or certified figures; no file publishes a category's change, a sub-index or a list.
Lesson: in store-level transaction data an unsold week at one store is not a missing price when the chain prices all its stores alike, so a price index follows each item at the unit that sets its price: a store-level match drops the slow lines from the comparisons and a pooled average lets shoppers' choice of chain pass for price change; no build on file teaches the price-setter grain (task463 teaches drift in linked month-on-month comparisons).

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 (default) each item's dollars and units added over the format's stores each week, the GEKS on items | the methodology prices an item at dollars over units without naming where they are added, which invites one figure per item per format | the store register gives each store's format in one join | yes: aggregate to one row per item and week before an index | none: no published sub-index or change | the battery finds nothing | no: a GEKS over 52 weeks | readable |
| R1 the same, on the stores in the panel all 52 weeks | the partner register gives the July chain's data-from date | the register's dates | yes: a balanced panel of reporters | none | none | no | readable |
| R2 items matched store by store, the GEKS on item-store products | none: it is the movement file's own grain | one row per store, item and week | yes: compare like with like at the finest level | none | none | no | readable |
| R3 (decisive) each item followed at the chain that prices it, the GEKS on item-chain prices | none: no sentence prices an item at its chain or says how a week with no row at one store is treated; the partner register says a chain prices an item alike in its stores, the dictionary that a row exists where a store sold | the chain column is one join away, but no column holds a chain's weekly price or marks an unsold store-week, and nothing invites grouping above the store | no: the opponent reads a missing row as a missing price, and reads identical prices as making the store grain harmless | no published figure to reproduce | the battery (keys, code formats, duplicates, resubmissions, unmatched joins, weighed lines) never asks what a week with no row means | no: a GEKS over item-chain unit values in each of 72 category-format cells | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the eighteen food categories | the eighteen the committee's terms list, each item placed by the item master's category | every category in the movement file (non-food lines included) | same call | the terms list the eighteen; the index covers food only |
| SF2 | the 52 weeks to 28 November 2026 | retail weeks ending Saturday 6 December 2025 to Saturday 28 November 2026 | calendar 2026's weeks; the latest 52 weeks a chain sent | ruled out | the terms name the window by its last week |
| SF3 | a category's change in a format | the GEKS index's average over the last four weeks of the window over its average over the first four, less one | geometric four-week means; the last week over the first | same call; ruled out | the methodology section 6 files the four-week averages (single end weeks publish one category, asserted different); geometric means asserted same call |
| SF4 | store format | the format the store register gives the store | the chain's main format | same call | every partner store has one format for the whole window (asserted) |
| SF5 | the national change | the category's four format changes averaged with the committee's 2026 format weights | a geometric combination; the panel's own spending shares as weights | same call; same call | the terms name the committee's weights; asserted: same call under a geometric combination and under the panel's shares |
| SF6 | within 1.5 points in every store format | each format's change less the national change, unrounded, at most 1.5 percentage points either way | the gaps rounded to one decimal before the test; strictly under 1.5 | same call | no category's largest gap lies within 0.15 of 1.5 (asserted) |
| SF7 | every store format | all four formats | the formats where a category sells | same call | every category sells in all four formats (asserted) |
| SF8 | an item's price for a line sold by weight | dollars over kilograms | dollars over the row's units field read as a count | same call | a price relative is the same in either unit; the dictionary gives kilograms for weighed lines |
| SF9 | the movement feed's resubmitted block | the later accepted load for each store, item and week | both loads kept | same call | the delivery log's statuses; asserted: same call keeping both |
| SF10 | the July chain | its stores in the index from their first week in the panel | the chain left out | same call | the panel includes it from its data-from date; asserted: same call without it |
| SF11 | item codes | the 13-digit codes of the feeds matched to the item master's 14-digit codes with the leading zero | raw string match | ruled out | the dictionary gives both lengths; every movement row joins once normalised (asserted) |
| SF12 | GEKS | the geometric mean, over every week of the window, of the two comparisons routed through it | the same over the weeks a pair can be compared through | same call | every pair of weeks shares items at the chain level in every cell (asserted) |
| SF13 | the comparison of a pair of weeks | a Tornqvist index over the items sold in both weeks, each weighted by the average of its two weeks' shares of the spending on them | none | same call | the methodology |
| SF14 | refitted stores | a store re-coded after a refit keeps its chain and format under both codes | the old code dropped | same call | the register lists both codes with chain and format; asserted: same call under either |
| SF15 | a gap reported to one decimal | the unrounded format change less the unrounded national change, then rounded | the rounded changes subtracted | digits move, verdicts do not | methodology section 7: changes and gaps computed unrounded and rounded only for publication |

## Ladder

Built values, asserted in checks.py and recomputed by verify.py from the bundle.

| Rung | Construction | Categories published | Smallest distance of a largest gap from 1.5 | Killed by |
|---|---|---|---|---|
| R0 (default) | each line's dollars and units added over the format's stores, a GEKS on lines | 4: Breakfast cereals, Cheese, Deli and cooked meats, Biscuits | 0.23 | methodology section 1: the index moves only when prices move, not when shoppers change stores; the July value chain's entry and the shift of supermarket spending toward the discount chain lower the pooled price with no shelf price falling |
| R1 | the same with the July chain left out, or on the balanced panel of store codes present all 52 weeks | 8: R3's ten less Yoghurt and desserts and Frozen foods (both variants) | 0.21 | the shift between the continuing chains still moves the pooled price |
| R2 | lines matched store by store (store codes as sent, or linked into sites) | 7: R3's ten less Breakfast cereals, Cheese, Deli and cooked meats and Biscuits, plus Coffee and tea (both variants) | 0.30 | methodology section 1: each item counts in proportion to what shoppers spend on it; a convenience store sold a slower line in 34 per cent of its weeks, so a store-level match keeps such a line in about one pair of weeks in nine and the index follows the big sellers |
| R3 (decisive) | each line followed at the chain that prices it | 10 (golden): Bread and bakery, Breakfast cereals, Cheese, Yoghurt and desserts, Eggs, Deli and cooked meats, Fresh fruit, Frozen foods, Biscuits, Chips and snacks | 0.41 | the golden |

- **Separation.** Four sets, four counts; no rung shares the golden's set.
- **Every reflex lands wrong.** Pooling errs in supermarkets, the store-level match in convenience; the golden is
  bracketed by the coarsest grain and the finest.
- **Worth.** The decisive move reverses R2's four drops (their convenience changes 1.1 to 1.8 points under the
  chain-level value; their slower lines rose 10.9 per cent against 2.3 for the three biggest sellers) and its one
  wrong keep (Coffee and tea, convenience gap 2.4 points at the chain level).
- **Convergence (asserted).** Each chain's own GEKS combined by spending (margin 0.37); the store level with a store's
  unsold week carrying its chain's price at no quantity (0.26); geometric four-week means; the panel's own spending
  shares or the household panel's category splits as format weights; a geometric national combination; the July
  chain left out; the resubmitted block kept twice; markdown rows dropped; the GTIN-13 rows left unmatched; kilograms
  read in grams: the same ten every time.
- **Clean truth.** On the generator's chain prices and demand before any mess the rungs give 4, 8, 7 and 10 (R3a, R3b).

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the items of the eighteen food categories sold at the panel's stores in each format in the window | filed (the terms, the partner register); SF1, SF10 |
| 2 | Unit of account | the category in a format, then nationally | filed (the terms) |
| 3 | Attribution window | retail weeks ending 6 December 2025 to 28 November 2026 | filed (the terms); SF2 |
| 4 | As-of dating | the movement feed as loaded by 4 December 2026, every chain's 28 November week accepted | filed (the delivery log) |
| 5 | Version basis | the latest accepted load for each store, item and week | filed (the dictionary, the delivery log); SF9 |
| 6 | Denominator | none: a change and a gap in percentage points | n/a |
| 7 | Weighting | each comparison by the two weeks' spending shares; formats by the committee's weights | filed (the methodology, the terms); SF5, SF13 |
| 8 | Window length | 52 weeks, four-week ends | filed (the methodology); SF3 |
| 9 | Boundary inclusivity | a gap of at most 1.5 points passes | filed (the terms); SF6 |
| 10 | Rounding path | changes and gaps unrounded until the deliverable; one decimal in the deliverable | filed (methodology section 7); SF6, SF15 |
| 11 | Tie-break | none needed: no gap within 0.15 points of 1.5 | asserted |
| 12 | Maturity and censoring | every chain's last week accepted before the pull | filed; asserted |
| 13 | Order of operations | each format's index, its change, the national combination, the gaps, the test | filed (the terms) |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | a resubmitted block replaces the accepted original | filed; SF9 |
| 16 | Identity normalisation | 13-digit feed codes to 14-digit master codes; refitted stores under two codes | dictionary; SF11, SF14 |
| 17 | Netting against gross | none: sales are net of offers at the till | n/a |
| 18 | Dimensional units | dollars; units or kilograms per line | dictionary; SF8 |
| 19 | Code and status semantics | promotion codes and load statuses for the asks; the call reads neither | never the stump |
| 20 | Integerisation | none in the call; store counts whole in the asks | n/a |
| 21 | Clause scope | the terms and the methodology govern the call; the dictionary, the delivery log and the partner register's code lists govern the asks | filed |
| 22 | Forward window contents | the 2027 structure rests on the window's changes, the latest year the chains have all delivered | filed (the terms) |

## Literal reader

Executed word for word: the terms (section 2) test each category's national change against its change in each of
the four formats over the 52 retail weeks to 28 November 2026, measured as the methodology statement sets out; the
methodology (section 5) compares every pair of weeks by a Tornqvist index over the products sold in both weeks, each
weighted by its spending shares, combined by GEKS, the change taken from four-week averages (section 6), and says the
index measures the change in the prices shoppers pay, moves only when prices move and not when shoppers change items
or stores, each item counting in proportion to what shoppers spend on it (section 1). The partner register says each
chain sets one shelf price for a line in all its stores in a format and runs its specials in every store; the feed
dictionary says a movement row exists only where a store sold the line that week. Pooling a line over the format's
stores moves with the July chain's entry and the shift between chains when no price moves (against section 1);
matching a line store by store weights a line by its spending only in the store-weeks it sold on both sides, a third
of a slow line's spending in convenience (against section 1's spending weights); following each line at the chain
that prices it satisfies both, and every consistent variant of it (the convergence line in the ladder) publishes the
same ten. The readings that differ (SF2, SF3 single end weeks, SF11 raw codes) each violate a quoted sentence; the
rest give the same call. The method's unit is not filed: the design and section 1 force it (determinism-check
section 1, HOW forced by the data's structure).

## Oracles

none for the call: no file publishes a sub-index, a category's change, a gap or a structure; the 2025 shelf-price audit
(distractor) records auditors' shelf prices for sampled items in 2025, in other stores and another year, and the
household panel's category shares (distractor) are not the committee's weights. For the asks, the delivery log's row
counts tie each accepted load under every handling, and nothing publishes a format's takings, a chain's continuous
stores or a category's promotion share.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops (built deltas) | Realism |
|---|---|---|---|---|---|---|---|---|
| A, the takings (store sales) of the panel's stores in each format over the window while they were in the panel, A$ million to one decimal | 4 | the audit trail of the data each format's index rests on | the paper's coverage line and the workbook's Panel sheet | D6: four chains (S3, N2, C3, O3, one per format) write the store's whole-week sales on both department-group rows (Food and Non-food carry the same figure every store-week); two benign chains (S4, C1) report the same two groups as a true split | H1 (D2): a supermarket chain's six-week resend, rejected at validation, kept in the table; H2 (D5): the July chain's onboarding backfill from January; H3 (D8): one convenience chain's own Sunday week-endings | store_weekly_sales_ry2026.csv (load_id, store_id, week_ending, dept_name, sales_aud), feed_delivery_log_ry2026.csv (load_id, status), panel_store_register.csv (store_id, format, first_week_ending, last_week_ending), partner_chains.xlsx (trading_week); 4 files, 12 columns | golden 804.4, 230.7, 86.7, 466.6; every row summed: +134.3, +63.8, +25.9, +138.2; the rejected resend kept: supermarket +9.9; the backfill kept: supermarket +111.3; Sundays filtered raw: convenience -0.6 | a flattened export repeating a store-level field on each detail row, a rejected resend, an onboarding backfill and a chain's own week-ending are what a retail data warehouse holds |
| B, for each partner chain, how many of its stores sent data in every week it was in the panel | 14 | the audit trail of the stores each chain's index rests on | the paper's continuity line and the workbook's Panel sheet | D7: every chain re-coded one refitted store under a new store number with no break in trading; only the register's trading name, suburb and postcode tie the codes (the register's grain sentence says one row per store code) | H4 (over-linking): six chains' refurbishment closures of two to four weeks, re-coded on reopening; H5: openings and closures during the year; the July chain counted from its agreement | gpi_movement_ry2026.csv (store_id, week_ending), panel_store_register.csv (store_id, chain_code, store_name, suburb, postcode), partner_chains.xlsx (data_agreement_from); 3 files, 8 columns | golden by chain (4, 3, 3, 4, 3, 3, 3, 4, 12, 15, 11, 2, 2, 2); by store code: one under in all 14; codes linked with gaps ignored: one over in S2, N1, C1, C2, C3, O2 | refits under new store numbers and refurbishment gaps are how a chain's store master changes |
| C, for each category, the share of its window spending sold on promotion, per cent to one decimal | 18 | a measure every category carries that the call does not turn on | the paper's promotions line and the workbook's Structure sheet | D2: convenience chain C2 coded its catalogue specials PC until its till upgrade (week ending 8 August 2026) and TPR from it, keeping PC for price check overrides; the partner register's code list puts TPR and PC (a price check override) in use from 2 August 2026, so read back over the year without its in-use dates it labels the chain's earlier specials as checks | H6: store markdowns (RC, MD, CLR) and price checks are not promotions (the dictionary's Terms); H7: each chain's own vocabulary; the resubmitted block counted twice | gpi_movement_ry2026.csv (load_id, store_id, item_code, week_ending, sales_aud, promo_code), partner_chains.xlsx (Price codes; code_list_supplied), gpi_item_master_2026.csv (category), panel_store_register.csv (chain_code), feed_delivery_log_ry2026.csv (status, note); 5 files, 11 columns | golden 12.4 to 14.4; the current code list read back: every category 0.21 to 0.6 under; every coded row counted: 9 or more categories moved; the block counted twice: 2 moved | a till upgrade that reuses a code is what a chain's point-of-sale history holds |

- **Main population zero-counts.** The call reads the movement rows' units, dollars, week, store and item and the
  register's chain and format; the store sales feed, the price codes, the register's names and dates and the log's
  notes are outside it, and the call is identical with store codes replaced by sites and with the promotion code and
  load columns dropped (asserted).
- **Hazard table.** H1 moves supermarket sales (A); H2 moves supermarket sales (A); H3 moves convenience sales (A);
  H4 moves six chains (B); H5 moves no figure for a path that counts every week and drops new stores; H6 and H7 move
  nine or more categories (C); the double-counted block moves two (C).
- **Referee.** The delivery log's statuses arbitrate the resend (A) and the resubmission (C); the dictionary defines a
  promotion by what it is, a temporary price reduction run in all a chain's stores for the week, and the code list's
  in-use dates say PC meant a price check only from 2 August 2026 (C); no file says which chains repeat the store total,
  which codes belong to one store, or what PC meant before 2 August.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A sales (4) | accepted loads, the backfill left out, Sunday weeks placed on the retail week, every department row summed | over in every format by 25.9 to 138.2 | miss |
| B continuous stores (14) | a store code with a row in every week the chain was in the panel | one under in every chain | miss |
| C promotion shares (18) | spending under each chain's special by the partner register's code lists | 0.21 to 0.6 under in every category | miss |

Mirror leakage: 0 per cent of the ask weight: the mirror (R2, the store-level match) takes A, B and C the cracker's way
and misses all 36; it keeps the supermarket, neighbourhood and online gaps where its national change rounds the same.
Pair ceiling: 37 (the cracker at about 50 with the call and its components; the mirror at about 24 with thirteen of
eighteen verdicts and part of the gap grid).

## Pre-ship check

- **Rule 1, the domain.** The deciding quantity is each category's GEKS-Tornqvist price change in each store format,
  the price statistician's own estimator, and the decisive step is its elementary unit: the line at the chain that
  sets its shelf price, because a store's week without a sale of a line is a week the chain's price still held.
  Swapped into hospital procedure costs, the chain's single shelf price, the outlet that sold nothing that week and
  the shopper moving between dearer and cheaper chains have no counterpart.
- **Rule 2, two layers.** Layer 1 is the feeds as loaded (resubmission, GTIN-13 codes, weighed lines, markdowns and
  price checks, refit re-codes, refurbishments, openings and closures, the July chain), each neutral on the call by
  assertion (R2a to R2e, separation); Layer 2 is the estimation_fit choice of unit, which moves the call from 4 or 7
  to 10.
- **Rule 3, the decisive step.** No filed sentence names the unit at which a line's price is formed; the analyst who
  reads every field and rule correctly still matches store by store (7) or pools the format (4). The ask devices sit
  in the store sales feed, the price codes and the register's names and dates, outside the call's population.
- **Gates.** checks.py 71 of 71; verify.py 0 mismatches; two builds byte-identical; figures_check 128 of 128;
  precut 49 of 49; leak.py REVIEW (the filed 1.5 test, document vocabulary, banners beside store counts, the retail
  calendar's forward weeks; each expected); guard heart WARN (answered at the draw), surface: task263 promoted as
  back to back on gap and generator G2, differentiated on the card (a mass balance of blends against a price-setter
  grain); container metadata clean; target.zip 5.8 MB.

## Tried and rejected

- The seed's reliability as a matched-pair minimum (every pair of weeks sharing a set share of spending): filed literally it is a rule's execution, and left vague it is a fork; dropped at the draw.
- Reliability as the sampling error of each format's index (stores or chains resampled): the decisive move would be the resampling unit, the lesson task260 and task261 already teach in this lane; dropped at the draw.
- Each format's change on items pooled across chains as the decisive step: binary, and its insight (read the change within each seller) is task259's lower rung; kept only as rung 0 and rung 1.
- Linking relaunched packs (a smaller pack under a new code) to price shrinkflation: the link reads an item master's attributes, an identity resolution the record says never held; dropped at the draw.
- Promotions drawn at random by line and week: the four-week ends carried about two points of promotional noise in every category and format, swamping the designed gaps; replaced by each chain's weekly catalogue, one line a category a week in a sixteen-week rotation (a second, eight-week rotation for heavier programmes), so the window's first and last four weeks carry the same specials.
- The promotion calendar started at the window's first week: that week carried a quarter of the usual specials and every change fell by about a point; the calendar now starts twenty weeks before the window.
- Four chains repeating the store's weekly total on each of six to eight department rows: an eightfold over-count shows in any per-store sanity check; they now report two department groups, beside two chains reporting the same groups as a true split.
- First-draft banner and firm names (Pellwick, Penhallow, Varnley, Corbel, Tovell, Hollin, Dunstar, Wenlow, Tallen, Marrin and others) sat within two edits of Australian places; renamed after the H21 screen, figures unchanged.
- Random streams keyed to store codes: giving the July chain a refit re-numbered every later code and reshuffled the world; streams are now keyed by chain, site and segment, and the ladder was refitted once.
- Gaps asked as distances ("how far its change sits from that"): a literal reader could give them unsigned; the ask now says above or below.
- A delivery-log note on the convenience chain's till release beside its first TPR week: the first reader took it for a planted hint; the code list's in-use dates carry the record instead.
- The PC rows before 2 August 2026 left to inference from the data's pattern: the first judge read the code list literally (PC never a special, every share 0.2 to 0.6 points lower); the in-use dates now force the reading.
- The gap ask's rounding path and the continuity ask's window left to the prompt's grammar: the first judge found both open (rounded changes subtracted; each store's own panel weeks); the methodology now files the rounding path and the prompt names the chain's weeks.
- The store sales file described as takings by department: a literal reader sums the four chains' repeated rows; the dictionary now describes the rows as the chain's export lays them out, and the repetition to the cent decides it.
