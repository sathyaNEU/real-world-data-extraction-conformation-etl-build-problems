# task302: design note

## Draw

- Pairing: Economics & Econometrics (client domain `economics-econometrics`), task type `structural-equilibrium-modeling`
  (structural demand: where a product's demand goes when the product is unavailable), objective Opportunity Sizing &
  Decision Support. Never built before on this objective.
- World: Ridgeway Foodmarkets, a regional supermarket chain of 24 stores in the lower North Island and
  Nelson-Marlborough with its own distribution centre in Palmerston North. Its head of supply chain, Nikau Fletcher,
  moves one category's lines onto automated store ordering with daily deliveries from 1 February 2027.
- Call: which of bottled water, infant formula, dry pet food and gluten-free bakery goes first, and what it adds a year
  to the chain's sales in that category (the twelve months to 30 June 2026 repeated, at that year's shelf prices, with
  half of the category's out-of-stock line-days removed, the share the vendor's contract commits to and the planning
  note takes).
- Golden: infant formula at about NZD 60,000 a year (57,775); the line-level route files bottled water at about NZD
  110,000.
- Seed: OS04 kept as a world-type only (a capacity placement sized by realisable revenue); its battery congestion
  counterfactual died at the probes (Tried and rejected).
- Shape `other`: the call, its figure, a chart of the four candidates' additions, and three asks (the cereal trial's
  out-of-stock line-days after go-live and their per cent change, by trial store, 6 cells; the distribution centre's
  deliveries that reached a store after it opened, by island, 2 cells; the pallets the distribution centre received
  from each category's suppliers, by month, 36 cells). Criteria: the call, its figure and the three rivals' clauses
  (5), the chart's four bars and highlight (5), the components (3), the two files (2), the asks (44): 59.
- Furniture: role operations_director (the head of supply chain decides with the team, forum line_manager_or_team),
  forcing event cutover_or_migration (the store ordering go-live), organisation retailer_or_ecommerce, no calibration
  organ, context artifact other (the head of supply chain's planning note).

## Three rules

Task type: structural-equilibrium-modeling, the structural demand part of it (diversion of a product's demand when the
product leaves the choice set), which the taxonomy lets serve Opportunity Sizing & Decision Support.
Domain test: the deciding quantity is the share of a stocked-out line's first-choice demand the category loses
outright, which demand economics estimates from availability variation, each out-of-stock spell an exogenous change to
the shopper's choice set, as diversion to the category's other lines on the out days and to the line itself after the
restock (the household's own stock carrying a storable good across the gap).
Swap: put megawatt-hours or hospital beds in for lines on a shelf and the call loses its terms: nothing takes the next
brand from the same shelf, and nobody buys next week's bag from the stock at home; the task reads only as a
supermarket's.
Layer 1: the point-of-sale export changes its line codes at the March 2025 till migration (a code history maps them,
and two pack changes in the base year give lines new GTINs); opening stock carries count corrections that set the system
stock to zero when the shelf was found empty; returns are booked as negative units; two stores closed for refits; the
formula supplier moved its weekly delivery day in 2025. Each comes from the chain's own systems and none is placed to be
caught.
Layer 2: estimand identification (the counterfactual category sales without the out-of-stock spell): a line's absence
costs the category only the part of its demand that goes neither to the category's other lines on the out days nor to
the line itself after the restock.
Decisive step: measuring each category's diversion, the other lines' excess over their own level while a line is out
and the line's excess after it returns, so that the category's loss is the line's expected sales less both, before the
plan's half is applied.
Not semantics: every field, code and the out-of-stock definition can be read correctly and the line-level route still
prices each out day at the line's own sales, because nothing in any file says where a shopper went; the diversion lives
only in other lines' rows and later days.
Not rule application: no filed rule nets diversion; the plan files the population (the 24 stores), the outcome (the
category's sales at each line's 2025-26 shelf price), the window (the twelve months to 30 June 2026) and the cut (half
of the out-of-stock line-days), never how a spell's cost is measured. Enumerated family, 14 constructions (the
line-level route, either netting alone, a store-week regression and ten that net both): three categories named, the
named figure from about NZD 57,000 to 107,000. Standing family, the ten that net both the other lines' excess on the
out days and the line's own excess after the restock (level windows of three to five weeks, rebounds of 10 to 21 days,
same-weekday or all-day levels, other-out days kept in or out of the levels, global weekday levels, a store-month
regression): all ten name infant formula at a printed 60,000 (56,843 to 61,506, 0.47 of one printed unit), at 1.12 to
5.06 times the next. Ruling-out loudness: no clause rules any rung out; the other lines' rows on the out days and the
line's own rows after the restock do, a cross-row cut nothing invites.
Analyst test: a strong analyst who joins the stock positions to the sales, reads every out-of-stock line-day correctly
and prices each at the line's same-weekday sales, halved as the plan sets, moves bottled water at about NZD 110,000 (or
dry pet food at about 70,000 after netting only the other lines' extra sales on the out days), where the golden is
infant formula at about NZD 60,000.
Estimand: the planning note (store_ordering_2027.docx) files what the category would have sold in the 24 stores over
the twelve months to 30 June 2026 had half of its out-of-stock line-days not happened, less what it did sell, at each
line's 2025-26 shelf price, and defines an out-of-stock line-day as the store opening with none of the line on hand.
No decoy: nothing is planted; no memo, briefing, dashboard or vendor figure prices the candidates, the stock system
publishes no lost-sales figure, and the two distractors (shelf space, ordering hours) rank nothing on the question.
No certified replay: no certified or published figure is reproduced to recover a method; the contract's half is an
input the plan files.
Lesson: a model learns that an unavailable product's demand is not lost to the group it belongs to until it has been
shown where it went, and that the evidence for where it went sits in the rows of the products that stayed and in the
days after the product returned; no build on file nets diversion from availability spells.

## Default path

1. Read the planning note: one category's lines move onto automated store ordering, which the vendor's contract commits
   to removing half of the category's out-of-stock line-days; the addition is valued over the twelve months to 30 June
   2026 at that year's shelf prices.
2. Join the opening stock positions to the daily sales through the code history and mark every store-line-day that
   opened a trading day with none on hand.
3. Price each out-of-stock line-day at the line's own expected sales in that store on that day (the same weekday in the
   surrounding weeks, or a store-line demand fit with weekday and season), at the line's price.
4. Total by category over the twelve months to 30 June 2026 and halve it.
- Ends on: bottled water at about NZD 110,000 (dry pet food second at about 90,000, infant formula about 60,000).
- Golden: infant formula at about NZD 60,000 (water and pet food at about 10,000 and 20,000 net of diversion).

## Stump sentence

A competent solver prices every out-of-stock line-day at the line's own same-weekday sales in the store, halves the
total and moves bottled water at about NZD 110,000, where the golden is infant formula at about NZD 60,000; the step
that lands it there is counting a line's absence as the category's loss, when water's shoppers take another brand from
the same shelf and pet food's buy the bag after the restock, while a missed formula delivery empties the whole shelf.

Data-native sentence: on a store-day a water line is off the shelf the other water lines sell about three quarters of
its expected units above their own level, and in the fortnight after a pet food line returns it sells about three
quarters of its lost units above its level, while a formula spell has every formula line at zero and the category
gets back about 3 per cent of it.

## Ladder

| Rung | Construction | Names | Infant formula |
|---|---|---|---|
| R0 | each out-of-stock line-day at the line's own expected sales, halved (the default path) | Bottled water (106,857) | 59,746 |
| R1 | net of the category's other lines' excess on the out days only | Dry pet food (69,684) | 59,746 |
| R2 | net of the line's own excess in the fortnight after its restock only | Bottled water (73,998) | 57,775 |
| R3 | a store-week regression of category sales on the share of its line-days out | Dry pet food (84,811) | 59,391 |
| R4 (decisive) | net of both, line by line within each store | Infant formula | 57,775 (60,000) |

Each rung is asserted in `generator/checks.py` (`ladder:` lines) at 1.1 times the next or more, and the ten standing
constructions (`family:` lines) all print infant formula at 60,000. R1 and R2 are each a careful analyst's half of the
netting and land on another category; only netting both separates formula, whose loss nothing recaptures.

## Readability screen

| Rung | What the pack shows a reader | Verdict |
|---|---|---|
| R0 | the stock positions' zero openings and each line's sales on its other days | readable |
| R1 | the category's other lines' sales on the days a line is out | readable |
| R2 | a line's sales in the days after its restock | readable |
| R3 | the category's store-week sales against its line-days out | readable |
| R4 (decisive) | nothing says where a missing line's shoppers went or that the category's loss differs from the line's; the plan values the category's sales and the dictionary describes the fields | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | out-of-stock line-day | the line opening a trading day with none on hand | the line sold out by the close | Infant formula (70,000) | the plan: "when the store opened with none of the line on hand, as the stock system's opening position records it"; same call |
| SF2 | half of the out-of-stock line-days not happened | half of the category's loss, no half being named | half of the spells removed whole | Infant formula, 60,000 | same call and figure (each spell equally likely to go); the plan names no half |
| SF3 | the year valued | the twelve months to 30 June 2026 | both years averaged | Infant formula (70,000) | the plan: "over the twelve months to 30 June 2026"; same call |
| SF4 | the value of sales | units at each line's 2025-26 shelf price | the till's net_sales_nzd | Infant formula, 60,000 | same call and figure: the till's 2025-26 values are units at that price |
| SF5 | price basis | shelf price including GST | excluding GST | Infant formula (50,000) | the dictionary: "Shelf price in NZD including GST"; same call |
| SF6 | units | the till's units net of returns | the rows netting to negative units dropped | Infant formula, 60,000 | same call and figure |
| SF7 | a line's sales | every till code's article over its dates, from till_item_codes.csv | lines.csv's article numbers and current GTINs only | Infant formula, 60,000 | same call and figure |
| SF8 | a year's addition | the twelve months valued as one year | February to December 2027 only | Infant formula (50,000) | the prompt's "add a year" and the plan's twelve months; same call |
| SF9 | goes first | the category that adds the most across the chain | the category leading in the most stores | Infant formula (18 of 24 stores) | the plan: "The category that adds the most goes first"; same call |
| SF10 | store-days with no sales at all | the two refit weeks, days the stores did not open | trading days with nothing sold | Infant formula, 60,000 | no line opens at zero on those days; same call and figure |

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | the 24 stores and each candidate category's lines in lines.csv | filed in the plan and lines.csv |
| 2 Unit of account | NZD of the category's sales a year | the question and the plan |
| 3 Attribution window | the twelve months to 30 June 2026, each line-day in its own day | filed in the plan (SF3) |
| 4 As-of dating | the stock system's opening position each day | the plan's definition (SF1) |
| 5 Version basis | one sales export and one stock export | one of each ships |
| 6 Denominator | none: an amount, not a rate | no rate in the estimand |
| 7 Weighting | each line-day at its line's 2025-26 shelf price | the plan |
| 8 Window length | levels from the same weekday within four weeks either side, eight where four hold fewer than two clean days | C1: windows of three to five weeks and rebounds of 10 to 21 days all print 60,000 (family) |
| 9 Boundary inclusivity | 1 July 2025 and 30 June 2026 both in; the year before carries levels only | the plan's twelve months |
| 10 Rounding path | the category's addition rounded once to the nearest NZD 10,000 | stated in the prompt; every standing construction prints 60,000 |
| 11 Tie-break | none needed | formula leads the next by 3.49 times |
| 12 Maturity and censoring | a spell ending near 30 June 2026 has part of its fortnight after the window | C1 across rebound windows (family) |
| 13 Order of operations | levels, out days, recapture, net, halve, round | one path |
| 14 Row order | sorted by store, line and day | the result does not depend on file order |
| 15 Duplicate resolution | none: one row per store, line and day in the stock file, per store, day and code in the sales | asserted by the stock identity |
| 16 Identity normalisation | till codes to articles through till_item_codes.csv | C1 (SF7) |
| 17 Netting against gross | the till's units net of returns | C1 (SF6) |
| 18 Dimensional units | units and NZD including GST | the dictionary (SF5) |
| 19 Code and status semantics | an out-of-stock line-day is an opening position of zero on a trading day | the plan (SF1, SF10) |
| 20 Integerisation | none before the final rounding | one rounding |
| 21 Clause scope | the contract's half applies to every category alike | the plan (SF2) |
| 22 Forward window contents | the twelve months to 30 June 2026 taken as the guide to 2027 | the plan (SF8) |

## Literal reader

Executed word for word, the planning note fixes the population (the 24 stores), the outcome (what the category would
have sold had half of its out-of-stock line-days not happened, less what it did sell), the window (the twelve months to
30 June 2026, taken as the guide to 2027), the price (each line's 2025-26 shelf price, including GST by the dictionary)
and the out-of-stock line-day (the store opening with none of the line on hand). It says nothing about what a shopper
does when a line is missing, so the literal reader has to estimate what the category would have sold, and every reading
in the fork table names infant formula (SF1 to SF10, asserted). The easy answer comes from the easy method on the same
estimand, pricing each out day at the line's own sales, never from another reading.

## Oracles

No file reproduces the golden or ranks the four categories on the question. The stock system publishes no lost-sales
figure; the shelf space workbook and the store ordering hours file (the two distractors: the hours staff spend ordering
bear on the move but not on its sales) rank nothing on it; the cereal trial export, the trailer stops, the trading days
and the goods received carry the asks only, and the purchase orders and the EDI log (a third distractor) are context
no figure needs.

## Ask sheet

Ask A, the cereal out-of-stock line-days in each trial store in the 13 weeks after the ordering system went live and
their per cent change from the 13 weeks before (6 cells): the vendor's export joins two reports, the stores' own stock
report up to 1 February 2026, whose on_hand is the stock when the store opened, and the ordering system's from 2
February, whose on_hand is the stock when it closed. Device D3 (a field's meaning set by date), silent: the dictionary
says "Units on hand", and the evidence is a cross-row cut, lines selling on 42 days they show nothing on hand and never
before go-live; a day's opening after go-live is the previous day's close plus that morning's delivery, and the day's
close plus its sales gives the same count (a count correction only falls on a day the line sold). Read as openings
throughout, the falls are 62.6, 19.7 and 42.3 per cent against the golden's 73.7, 42.4 and 58.8. Every cell moving.

Ask B, the distribution centre's deliveries in the twelve months to 30 June 2026 that reached a store after it opened,
by island (2 cells): the stores opened at 6:30 until the chain moved to a 7 am opening on 1 April 2026, and stores.csv
carries the current 07:00. Device D2 (an attribute at the wrong vintage), seen: the tills' first sales in
store_trading_days_2025-26.csv show it, and three of three readers found it, so the ask is cut to the two islands and
carries little weight. The store list's 7:00 all year drops the 52 stops that reached a store between 6:40 and 6:50
before April (North 305 and South 151 against 339 and 169). No stop arrives within ten minutes of either opening time,
so the first sale and the half hour it falls in give one answer.

Ask C, the pallets the distribution centre received from each candidate category's suppliers in each month (36 cells):
a supplier sends a dispatch advice for each order and ships the orders it has ready on one truck where they fit (the
two orders a buyer raises when a supplier's lines sit in two buying groups; a bakery's held order with its next one)
and on two trucks the same day where they do not, and the receiving system books each truck's pallets onto every line
it received from that truck, under every dispatch advice the truck carried. Device D6 (an event's quantity on every
line it covers, grain unstated) one level below where a reader repairs it: the pallets repeat on every line of a
dispatch advice, so taking each dispatch advice once looks like the repair, but 166 dock appointments carry two or
more dispatch advices, each booking the truck's pallets; only dc_dock_appointments_2025-26.csv groups them. Each
dispatch advice once, each receipt once, each order once and every line all miss every cell; each supplier-day once
matches 5 of 36. Every cell moving.

| Ask | Cracker's handling | Cracker |
|---|---|---|
| A | the export's on_hand read as the opening stock throughout | miss |
| B | the store list's opening time all year | miss |
| C | each dispatch advice's pallets taken once | miss |

Pair ceiling: 28.5 (cracker 45.0 on the call with no ask cell, mirror 12.0 off it with none); a cracker that also finds
ask A's device alone reaches 32.2, ask B's 29.8, ask C's 51.0.
Mirror leakage: 0.0 per cent of ask weight.
Measured by: generator/pair.py on the cut pack.

Separation: none of the ask files is read by the main call (the golden opens the sales, the stock positions, lines.csv,
the till codes and stores.csv for its store list), and the asks' devices sit in the trial export, the trailer stops
with the trading days, and the goods received with the dock appointments.

## Pre-ship check

- Free gates on the shipped pack (target.zip 3b9ace95): generator checks 56 passed (the call at 57,775 printed 60,000,
  3.49 times the next category, the ladder and the standing family, SF rows, the three rules on the clean truth, every
  ask figure's edge, the three devices with every modelled wrong path missing, separation, the input gates, the stock
  identity); verify.py recomputes the call and all 44 ask figures from the zip alone (47 checks); two builds
  byte-identical at ship; figures_check 59 of 59; precut 51 checks clean; voice-check PASS; leak.py REVIEW only (the plan
  names the candidates beside the decision's words; stump-paragraph words in the dictionary and the plan); guard heart
  WARN as answered at the draw, surface clean.
- Stage 4 over three rounds: all six scored readers filed bottled water (five at about 110,000, one at 90,000) and the
  judge's three runs reproduced the golden. Round 3 (3b9ace95): both readers fitted several demand estimators each
  (water 108,800 to 114,000, pet food about 92,000, formula about 60,000, all at line level), kept asks A and B whole
  and none of ask C's 36 cells: 8 of 44 each, 18.2 per cent, measured pair 22.0 with both off the call and 38.5 if one
  response landed it. The judge's run r3 DETERMINISTIC, APPROVE (Gate F strong, Gate G decomposition_attribution,
  analytical_non_defect, surface_read_dependency no; Gate H pass), the five residual forks each closed by the files.
- Realism after the round: both readers read the formula bay's whole-shelf outages as planted-looking. They are the
  supplier's missed visits, the evening count correcting the bay to zero and a call-out refilling it (95 per cent of
  formula deliveries fall on the visit weekday), which is the process the call measures and nothing to catch; the
  judge found no planted element, and the readers' other notes (regular trailer times, first sales soon after opening)
  touch no graded figure.
- The 10/10 rules re-read against the built pack: the decisive step is the category's loss net of diversion to the
  shelf on the out days and to the line after its restock, which no filed rule performs (the plan files the
  counterfactual sales and the out-of-stock definition, never the netting); the Layer 1 mess (the till migration, count
  corrections, the code history, refits, returns, the moved visit day) carries no part of the call.

## Tried and rejected

- OS04 world, the battery's own congestion relief (2026-10-24, probe seed 3021): a 20 MW / 80 MWh battery valued at five 2024 nodes on revenue settled at "the LMP the market would have cleared with the project's own charging or discharging included", where Northfield's curtailed wind and Harbor Point's afternoon pocket shortfall run under 20 MW (the battery's own MW unbind them) and Cedar Flats' evening shortfall runs over 22 MW (its premium survives); golden Cedar Flats on my storage convention against the price-taker's Northfield. Landed by both call-only probes in under three minutes: each read the policy's clearing-price clause as the instruction it is, took the curtailed volume (economic maximum less dispatch) and the pocket peakers' output as the margins, settled beyond them at energy plus loss, and filed the same construction (both named Harbor Point first only because the storage and cycle conventions were left open). A counterfactual price is a WHAT whose filing names the decisive step: the determinism the clause buys is the reach it pays, as stumping 1.1 records.
- Grocery prototype estimators (2026-10-25): a cross-store synthetic control on category totals (each store's expected category sales from the stores whose category was clean that day) and trailing pre-episode levels both spread the four additions over 100,000 and more, because a 1 to 3 per cent category deficit is a small difference of large totals and frequent outages leave few clean days; the line-by-line recapture accounting (symmetric same-weekday levels from clean days, other-out days excluded) holds every member on infant formula.
- Stock positions built by holding back the deliveries before a spell, so the shelf empties exactly at the close (2026-10-25): every run-out day then shows sales equal to the stock available, which both probes read as capped demand; the spells now open after an evening count correction instead.
- Ask layer v1 (stage 4 round 1, target.zip e91ca190): both readers took all 25 ask figures, the trial export's switch
  from opening to closing stock by the stock identity, the 6:30 opening by the trading days' first sales and the order
  date by the ORDCHG messages, while both missed the call (bottled water at 110,000 and 90,000). Three seen devices,
  each found by one cross-check; ask C now rests on a truck's pallets booked onto every line it delivered.
- Ask layer v2 (stage 4 round 2, target.zip 690c9ee7): ask C's pallets, booked on every line of each dispatch advice,
  were taken by both readers, who saw the repeat and kept each dispatch advice once; the opening hours again fell to
  the first sales (seen by all three readers who met it) and reader C rebuilt the trial's openings from the close plus
  the sales, which the judge's run r2 showed gave store 210 a second answer. The call held again (bottled water at
  110,000 from both). Ask C's truck grain now sits one level below the dispatch advice, the trial's count corrections
  fall only on days a line sold, and ask B is cut to the two islands.
