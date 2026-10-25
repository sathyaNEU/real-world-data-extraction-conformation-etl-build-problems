# task302: design note

## Draw

- Pairing: Economics & Econometrics (client domain `economics-econometrics`), task type `structural-equilibrium-modeling`
  (structural demand: where a product's demand goes when the product is unavailable), objective Opportunity Sizing &
  Decision Support. Never built before on this objective.
- World: Ridgeway Foodmarkets, a regional supermarket chain of 24 stores in the lower North Island and
  Nelson-Marlborough with its own distribution centre in Palmerston North. Its head of supply chain, Nikau Fletcher,
  moves one category's lines onto automated store ordering with daily deliveries from 1 February 2027.
- Call: which of bottled water, infant formula, dry pet food and gluten-free bakery goes first, and what it adds to the
  chain's 2027 sales in that category (the twelve months to 30 June 2026 repeated, at that year's prices, with three
  quarters of the category's out-of-stock line-days removed).
- Planning values: infant formula about NZD 90,000; the line-level route files bottled water at about NZD 150,000.
- Seed: OS04 kept as a world-type only (a capacity placement sized by realisable revenue); its battery congestion
  counterfactual died at the probes (Tried and rejected).
- Shape `other`: the call, its figure, a chart of the four candidates' additions, and three asks (the distribution
  centre's deliveries by store, suppliers' cases by quarter, the system trial's out-of-stock line-days).
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
Layer 1: the point-of-sale export changes its line codes at the March 2025 till migration (a code history maps them);
opening stock carries count corrections that set the system stock to zero when the shelf was found empty; returns are
booked as negative units; two stores closed for refits; the formula supplier moved its weekly delivery day in 2025.
Each comes from the chain's own systems and none is placed to be caught.
Layer 2: estimand identification (the counterfactual category sales without the out-of-stock spell): a line's absence
costs the category only the part of its demand that goes neither to the category's other lines on the out days nor to
the line itself after the restock.
Decisive step: measuring each category's diversion, the other lines' excess over their own level while a line is out
and the line's excess after it returns, so that the category's loss is the line's expected sales less both, before the
cut is applied.
Not semantics: every field, code and the out-of-stock definition can be read correctly and the line-level route still
prices each out day at the line's own sales, because nothing in any file says where a shopper went; the diversion lives
only in other lines' rows and later days.
Not rule application: no filed rule nets diversion; the plan files the population (the chain's stores), the outcome
(the category's net sales), the window (the twelve months to 30 June 2026 repeated) and the cut (three quarters of the
out-of-stock line-days), never how a spell's cost is measured. The enumerated family (line-level baselines at three
windows, same-weekday or all-day levels, rebound windows of 10, 14 and 21 days, base-year or two-year rates, other-out
days kept in or out of the levels) spreads the four additions from 15,000 to 60,000 for water and pet food and leaves
infant formula within 3 per cent of its line-level figure; every member that nets diversion files infant formula, and
the line-level route files bottled water with no ruling-out clause anywhere: what rules it out is the other lines'
rows on the out days and the line's own rows after the restock.
Analyst test: a strong analyst who joins the stock positions to the sales, reads every out-of-stock line-day correctly
and prices each at the line's same-weekday sales, cut by three quarters, moves bottled water at about NZD 150,000 (or
dry pet food at about 100,000 after netting only the other lines' extra sales on the out days), where the golden is
infant formula at about NZD 90,000.
Estimand: the planning note (store_ordering_2027.docx) files what the category's stores would have sold over the
twelve months to 30 June 2026 had its out-of-stock line-days been a quarter of what they were, at that year's prices,
against what they sold.
No decoy: nothing is planted; no memo, briefing, dashboard or vendor figure prices the candidates, and the stock
system publishes no lost-sales figure.
No certified replay: no certified or published figure is reproduced to recover a method; the trial's three quarters is
an input the plan files.
Lesson: a model learns that an unavailable product's demand is not lost to the group it belongs to until it has been
shown where it went, and that the evidence for where it went sits in the rows of the products that stayed and in the
days after the product returned; no build on file nets diversion from availability spells.

## Default path

1. Read the planning note: one category's lines move onto automated store ordering, which removes three quarters of
   the out-of-stock line-days; the addition is valued over the twelve months to 30 June 2026 at that year's prices.
2. Join the opening stock positions to the daily sales through the code history and mark every store-line-day that
   opened with none on hand (about 3 per cent of line-days in each category).
3. Price each out-of-stock line-day at the line's own expected sales in that store on that day (a store-line demand
   fit with weekday and season, or the same weekday in the surrounding weeks), at the line's price.
4. Total by category over the twelve months to 30 June 2026 and take three quarters.
- Ends on: bottled water at about NZD 150,000 (pet food second at about 140,000, infant formula about 90,000).
- Golden: infant formula at about NZD 90,000 (water about 20,000, pet food about 35,000 net of diversion).

## Stump sentence

A competent solver prices every out-of-stock line-day at the line's own same-weekday sales in the store, cuts the
total by three quarters and moves bottled water at about NZD 150,000, where the golden is infant formula at about NZD
90,000; the step that lands it there is counting a line's absence as the category's loss, when water's shoppers take
another brand from the same shelf and pet food's buy the bag after the restock, while a missed formula delivery
empties the whole shelf.

Data-native sentence: on a store-day a water line is off the shelf the other nine water lines sell about seven tenths
of its expected units above their own level, and in the fortnight after a pet food line returns it sells about half
its lost units above its level, while a formula spell has every formula line at zero and no excess after it.

## Tried and rejected

- OS04 world, the battery's own congestion relief (2026-10-24, probe seed 3021): a 20 MW / 80 MWh battery valued at five 2024 nodes on revenue settled at "the LMP the market would have cleared with the project's own charging or discharging included", where Northfield's curtailed wind and Harbor Point's afternoon pocket shortfall run under 20 MW (the battery's own MW unbind them) and Cedar Flats' evening shortfall runs over 22 MW (its premium survives); golden Cedar Flats on my storage convention against the price-taker's Northfield. Landed by both call-only probes in under three minutes: each read the policy's clearing-price clause as the instruction it is, took the curtailed volume (economic maximum less dispatch) and the pocket peakers' output as the margins, settled beyond them at energy plus loss, and filed the same construction (both named Harbor Point first only because the storage and cycle conventions were left open). A counterfactual price is a WHAT whose filing names the decisive step: the determinism the clause buys is the reach it pays, as stumping 1.1 records.
- Grocery prototype estimators (2026-10-25): a cross-store synthetic control on category totals (each store's expected category sales from the stores whose category was clean that day) and trailing pre-episode levels both spread the four additions over 100,000 and more, because a 1 to 3 per cent category deficit is a small difference of large totals and frequent outages leave few clean days; the line-by-line recapture accounting (symmetric same-weekday levels from clean days, other-out days excluded) holds every member on infant formula.
- Stock positions built by holding back the deliveries before a spell, so the shelf empties exactly at the close (2026-10-25): every run-out day then shows sales equal to the stock available, which both probes read as capped demand; the spells now open after an evening count correction instead.
