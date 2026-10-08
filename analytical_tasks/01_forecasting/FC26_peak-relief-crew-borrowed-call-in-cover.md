# FC26 — Which store gets the peak relief crew, when the call-ins that cover it in ordinary weeks are borrowed from sister stores that will be short on the same shifts

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Economics · retail labour and store operations |
| Mirrors | Flex labour pools shared across sites that empty exactly when every site peaks together (Amazon fulfilment-centre flex pools at Prime Day, Apple Retail holiday cover borrowed between stores in one metro, marketplace couriers borrowed across zones at a city-wide surge) |
| Decision shape | Which of N gets one scarce thing: the 25-person relief crew for the four trading weeks to Christmas Eve |
| Committed call | The one store the crew is sent to, and the crew hours it will work there, to the nearest 10 hours |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · Pattern E (conditioned yield, S8), with a saturated tie (measured #19) broken at rung 1 |
| Gate G mechanism | forecasting, with decomposition_attribution |
| Measured traps engaged | #19 breaks a big tie instead of questioning it · #13 validates on one population, applies to another · #6 treats a mixed segment all one way |
| Calibration form | Retry log: every call-in request the eight stores raised in 32 closed weeks, with each offer, decline and retry |
| Driving force | A casual borrowed from a sister store accepts a call-in only when their own store has no open request in the same shift block. In the closed weeks shortages were scattered sick calls, so borrowing filled and the most cluster-reliant store had the best record in the chain. In the peak the four west-cluster stores are short in the same Saturday and late-night blocks, and borrowed cover fills almost nothing there, while the east cluster's staggered peaks leave most of its borrowing intact. The split shows only in a self-join of the call-in log, and its weight only in a block-level forecast of every lending store's shortage. |

## 1. Situation

A grocery chain with eight stores in one Australian state sets its peak labour from a turnover forecast. For the four trading weeks to
Christmas Eve it has one relief crew: 25 trained staff and 4,000 crew hours, sent whole to one store. Every store's peak roster is already
published. Where a roster leaves hours open, the store raises a call-in, and the workforce system offers the shift to the store's own casuals
in seniority order, then to the casuals of the other stores in its cluster, retrying until someone accepts or the shift starts. Seven stores
sit in two clusters (four in the west, three in the east), and one regional store has no cluster. The workforce standard places the crew
where it will work the most hours that would otherwise go unworked.

## 2. Gate G: why this is legal

* **Litmus.** Every figure in the pack is correct: the turnover history, the published peak roster, the call-in log's offers and outcomes,
  the casual register and the chain's 84% call-in fill rate. No stakeholder's reading of their own numbers is overturned; the regional
  manager is right that call-ins have covered the stores all year. The difficulty is that the fill the log measured belongs to a different
  population of offers from the one the peak will generate.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the manager's view and every voice. The logged fill rates still look like the obvious thing to carry forward,
  and the store that borrows most still has the best record in the file.
* **Instrument repair.** Imagine a call-in system that records the reason for every decline. The closed weeks would still hold too few
  shared-shift offers to show the peak's weight, because the peak has not happened; the forward overlap has to be built from the forecast
  either way.
* **Lens swap.** The naive read and the answer differ in population and moment: offers made in sick-call weeks, one store short at a time,
  against the offers the peak's shared shortages will generate.

## 3. The driving force

A strong solver forecasts peak turnover with the trading-day composition right, converts it to required hours with the labour standard,
subtracts the published roster and nets off call-ins at each store's own logged fill. Each step is correct. What it carries forward is a fill
rate measured on offers sent while one store at a time was short. A borrowed casual takes a sister store's shift only if their own store has
no open request in the same shift block, because the system offers home-store shifts first and the casual is already committed. In the
closed weeks fewer than one cross-store offer hour in ten met an open home-store request. In the peak the four west-cluster stores are short
in the same Saturday, late-night and Christmas Eve blocks, so four fifths of their borrowed cover meets a busy lender; the east cluster's
CBD and suburban stores peak in different blocks, so only two fifths of theirs does. Wattle Grove, a newer west-cluster store with a small
own pool, covered 74% of its call-in hours with borrowed casuals and filled 95% overall, the best record in the chain. Its peak fill falls to
about 36%.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Trading-day peak forecast × labour standard − published roster. The crew would work its full 4,000 hours at six stores, so the standard's tie-break (higher forecast peak turnover) decides | A, Harrow Quay (turnover 1.22× the next tied store) | The standard's own placement rule and tie-break, run on a clean calendar-aware forecast | The call-in log: across the closed weeks call-ins covered 84% of the hours rosters left open |
| 1 | Saturation broken: each store's open hours net of call-ins at the chain fill rate (84%) | B, Kellet Road (1.23× the runner-up) | Every open hour now nets the cover the record shows, and the six-way tie dissolves into one leader | The workforce standard assesses call-in cover store by store, and store fill in the log runs from 0.78 to 0.95 |
| 2 | Each store's open hours net of its own logged fill rate | C, Tamsin Creek (1.51×) | Store-specific, reconciled to the log to the hour, and it points at the one store with no cluster to borrow from | Within the log, a cross-store offer is never accepted when the casual's home store has an open request in the same block, and the peak forecast puts most west-cluster call-in hours in such blocks |
| 3 | **Decisive:** fill conditioned on whether the lending casual's home store is short in the same block, carried to each store's peak block profile (own-pool fill as logged; borrowed fill only in blocks where the lender is not short) | **E, Wattle Grove** (5th of 8 on rung 0) | — | — |

* **Position table.** Wattle Grove ranks 5th on rung 0 (fifth of the six saturated stores by forecast turnover), 4th on rung 1 and 8th on
  rung 2, and leads only rung 3. Rung leaders beat their runners-up by 1.22× (forecast turnover, the tie-break), 1.23×, 1.51× and 1.42×.
* **Discriminator dominance.** Tamsin Creek carries a 5.40× advantage into rung 3 (1,430 unfilled hours against Wattle Grove's 265). The
  peak conditioning multiplies Wattle Grove's unfilled hours 12.8× (265 to 3,400) and leaves Tamsin Creek's unchanged, because it borrows
  nothing: an edge of 12.8× against the 6.5× that 1.2 × 5.40 requires, with 1.98× headroom. The product, (1/5.40) × 12.8 = 2.38×, is Wattle
  Grove's margin over Tamsin Creek; over the rung-3 runner-up, Orwell Square (2,394), it is 1.42×.
* **Partial correction priced (L3).** Every half-applied construction names another store. Haircutting borrowed cover by the visible
  per-offer gap (55% against 61%), or weighting the split at the log's own shared-block share (9.8%), names Tamsin Creek at 1,430 hours,
  1.20× ahead of Orwell Square, with Wattle Grove last at about 650. One chain-wide shared share for every store (0.62), ignoring which
  cluster's peaks coincide, names Orwell Square at 3,272 hours, 1.21× ahead of Wattle Grove. Dropping all borrowed cover sends Orwell Square
  and Wattle Grove both past the crew's 4,000 hours, and the standard's tie-break names Orwell Square on turnover (1.17×).
* **Grid.** Forecast (seasonal naive or trading-day) × call-in treatment (none, chain rate, store rate, conditioned at the log's shared
  share, one chain-wide share, cluster shares from the block forecast) = 12 cells. Only the trading-day forecast with cluster shares names
  Wattle Grove at 3,400 hours; seasonal naive with cluster shares also names it, at 3,010 hours (11.5% low), because last year's window put
  Christmas Eve on a Wednesday and this one adds a late-trading Thursday. Every other cell names Harrow Quay, Kellet Road, Tamsin Creek or
  Orwell Square.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The workforce standard describes the offer order (own casuals, then the cluster's). No document says a casual whose
   own store is short never takes a sister store's shift, and none links the cluster stores' peak shortages to one another.
2. **Corpus blind to the weight.** The log pins the split only through a self-join, and cannot show how much it will matter: *across the 32
   closed weeks only 9.8% of cross-store offer hours met an open home-store request, because the log runs February to September, when
   shortages came from scattered sick calls rather than a trading peak every store shares.*
3. **No arithmetic symptom.** Requests, offers, acceptances, timesheets and roster hours reconcile on every rung, and the chain rate and
   every store rate reproduce exactly from the log.
4. **Not a row predicate.** Whether an offer met an open request at the casual's home store needs the home store from the casual register
   and a self-join of the request log on store, date and block; the forward weight needs a block-level shortage forecast for every lending
   store.
5. **The enumeration is arithmetic.** No column says "shared block" or "borrowed"; which peak call-in hours will meet a lender's shortage is
   computed from the forecast.
6. **No cutover date.** Nothing steps. The shared shortage is the peak's calendar acting on four stores at once.
7. **Survives deletion.** No wrong number exists to delete; every logged fill rate is correct for the weeks it describes.

## 6. The calibration corpus

* **Form.** The call-in log: 14,620 requests from the eight stores across 32 closed weeks, each with every offer (casual, sequence, time
  sent, outcome) and the request's final status.
* **What it certifies.** Rungs 1 and 2. The chain rate (84.0%) and every store's rate reproduce exactly, so a solver who back-tests its
  transport on the closed weeks is confirmed.
* **The absolute split (O2).** 0 of 1,184 cross-store offers to a casual whose home store had an open request in the same block were
  accepted; 6,648 of 10,898 other cross-store offers (61.0%) and 61.2% of own-store offers were. Pooled, cross-store offers fill 55.0%. No
  visible column (offering store, weekday, block, lead time, casual tenure) shows more than a 4-point spread in cross-store acceptance.
* **Twin pair.** Brindle Park in log weeks 19 and 23 raised identical requests (count, blocks and lead times) from the same pool with the
  same borrowed share. It filled 88% of its call-in hours in week 19 and 44% in week 23, because in week 23 its lenders had open requests in
  the same blocks and in week 19 they did not. Only the self-join separates the two weeks.
* **Resemblance points at the decoy.** Wattle Grove's peak request profile most resembles its own closed weeks, in which it filled 95%,
  the best in the chain.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The workforce standard: the crew goes where it will work the most hours that would otherwise go unworked. Its tie-break:
  where the crew would work its full hours at more than one store, the store with the higher forecast peak turnover. Call-in cover is
  assessed store by store. The labour standard (hours per thousand dollars of turnover, by store format) is in the same document.
* **Empirical pins.** The split, from the self-joined log. Each store's own-pool fill, from its own-store offers. Each cluster's shared
  blocks, from the block-level shortage forecast.
* **Voices.** The regional operations manager: "Our call-in fill is the best in the group; the stores will cope." The workforce analyst:
  "The store with nobody to borrow from always struggles most." The Wattle Grove store manager: "We borrow from Harrow Quay and Kellet Road
  whenever we're short, and it has always worked."
* **Licensed wrong basis.** The standard records that group retail finance sizes peak relief on the chain call-in fill rate applied to each
  store's roster gap, and will bring that basis to the planning meeting.

## 8. Determinism by construction

* **Shift blocks.** Every shift in the chain starts and ends on six fixed four-hour blocks, so "the same shift" has one meaning; overlap by
  hour and same-block readings select identical offers.
* **Fill weighting.** The standard counts cover in hours. Requests are single-block, so hour-weighted and request-weighted fill differ by
  under 0.3 points at every store.
* **Shortage forecast.** Every west-cluster store's forecast requirement exceeds its roster in every Saturday, late-night and Christmas Eve
  block and in no weekday-morning block, under a trading-day regression and a weekday-profile model alike, so the shared blocks do not
  depend on the forecast form.
* **Shared share by store or by cluster.** Every store in a cluster has the same peak shared-block share by construction (0.80 west, 0.40
  east), so computing it per store or per cluster gives the same figure.
* **Own-pool fill.** The published peak roster leaves each store the same number of own casuals unrostered per block as its closed-week
  average, so own-pool fill carries as logged.
* **Censoring and maturity.** A request still open when its shift starts is closed as unfilled in the log. The extract was taken on a
  Monday before any request of that week was raised, so nothing is open.
* **Rounding.** The committed hours land at 3,400, mid-bin at the nearest 10.

## 9. Prompt sketch and deliverables

> Our relief crew can go to only one store for the four trading weeks to Christmas Eve, and the regional operations manager is sure our
> call-in record means the stores will cope. Tell me which store gets the crew and how many crew hours it will actually work there, to the
> nearest 10 hours, in a sentence I can read out at Thursday's peak planning meeting. Send me `peak_relief.xlsx` with the build and the
> sheets below, a chart `peak_cover.svg`, and a one-page `relief_note.docx` that commits to the store.

* `peak_relief.xlsx` — the placement build for all eight stores, the penalty-hours sheet (ask A) and the attrition sheet (ask B).
* `peak_cover.svg` — one horizontal stacked bar per store, ordered by unfilled hours: the peak roster gap split into own-pool cover,
  borrowed cover and unfilled hours, with the crew's 4,000-hour line, a marker for the unfilled hours the chain rate implies, and the chosen
  store annotated with its hours.
* `relief_note.docx` — the committed store and hours, and why each of the other seven is not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the eight stores, the casual hours paid in the last 13 closed weeks in each penalty
  class (ordinary, weekday evening, Saturday, Sunday, public holiday). *Device:* night-fill shifts that cross midnight are stored against
  their start date in the payroll ledger, while the award prices each hour by the day it falls on, as the payroll guide documents. Reading
  the start date misprices Saturday-into-Sunday night-fill hours at the five stores that run overnight fills. Neither the payroll ledger nor
  night-fill shifts enter the crew build.
* **Ask B (device-carried).** For each store, casual attrition over the last 12 months and the median tenure of leavers. *Device:* a casual
  moving between stores is filed as a termination and a re-hire under the same employee number, as the HR guide documents; counting those as
  leavers overstates attrition at four stores. All 46 transfers predate the call-in log's first week.
* **Ask C (validity).** The crew hours each store would get under each of the four rung constructions, and the store each construction
  names.
* **Decoupling.** Clearing the shared-block conditioning changes no figure in asks A or B.

## 11. Rubric arithmetic

8 stores × 5 penalty classes (ask A) + 8 × 2 (ask B) + 8 stores × 4 constructions (ask C) + the committed store, its crew hours and its
margin over the runner-up + 5 named chart parts + 3 files ≈ 99 criteria.

## 12. World-building constraints

* Clusters: west (Harrow Quay, Kellet Road, Wattle Grove, Brindle Park), east (Orwell Square, Fenwick Lane, Sorrel Vale); Tamsin Creek has
  none. Forecast peak roster gaps (hours): Harrow Quay 5,000, Kellet Road 8,000, Tamsin Creek 6,500, Orwell Square 5,700, Wattle Grove 5,300,
  Brindle Park 4,400, Fenwick Lane 3,800, Sorrel Vale 3,200. Six exceed 4,000. Forecast peak turnover ($M): 15.4, 12.6, 10.4, 9.6, 8.2, 7.8,
  6.9, 6.0 in the same order.
* Logged fill (own + borrowed): Harrow Quay 0.75 + 0.06, Kellet Road 0.86 + 0.04, Tamsin Creek 0.78 + 0, Orwell Square 0.16 + 0.70, Wattle
  Grove 0.21 + 0.74, Brindle Park 0.56 + 0.26, Fenwick Lane 0.70 + 0.14, Sorrel Vale 0.72 + 0.08; chain 0.84.
* Peak shared-block share of borrowed hours: 0.80 at every west-cluster store and 0.40 at every east-cluster store. Unfilled hours at rung
  3: Wattle Grove 3,400 ± 2, Orwell Square 2,394, Brindle Park 1,707, Tamsin Creek 1,430.
* Half-applied constructions: haircut or log share names Tamsin Creek (1.20×); chain-wide share names Orwell Square (1.21×); no borrowed
  cover ties Orwell Square and Wattle Grove at 4,000 and the tie-break names Orwell Square (turnover 1.17×).
* 0 of 1,184 shared-block cross-store offers accepted, 61.0% of the other 10,898. Shared-block share in the log is 9.8% overall and under
  15% in every store-week except the twin weeks. The twin weeks are identical on every visible request and pool column.
* Penalty classes, night-fill shifts and transfers touch no quantity in the crew build.
