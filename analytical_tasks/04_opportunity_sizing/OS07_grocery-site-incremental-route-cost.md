# OS07 — Which site gets next year's one new grocery store, when the audited cost per case charges every site for delivery routes some of them would ride for free

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Supply Chain & Logistics · grocery store network planning |
| Mirrors | Store, dark-store and locker siting at grocery and e-commerce chains (Amazon Fresh, Walmart, Kroger) where a site's cost to serve depends on whether it rides an existing delivery route or needs a new one, while finance charges every location the network's average cost per case |
| Decision shape | Which of N gets one scarce thing, with the sizing kept as the graded figure: one store opening, six shortlisted sites |
| Committed call | The site opened next year, and the incremental annual contribution it adds to the chain, to the nearest $10k |
| Gap · Pattern | Gap 3 (objective) over Gap 1 (time) · S6 (a correct share carried onto a different book), with a suppressed competitor-size cell bounded from published totals (#24) and own-store cannibalisation below it |
| Gate G mechanism | decomposition_attribution, with binding_constraint |
| Measured traps engaged | #7 uses the ready-made measure · #24 treats an unpublished figure as unknown · #13 validates on one population, applies to another |
| Calibration form | Gold-standard verification subsample: the internal audit's fully traced P&L for 15 randomly sampled stores |
| Driving force | Finance charges logistics to stores at the audited network rate of $1.10 a case, a correct share of route costs for the stores that produced it. A new store's real logistics cost is what it adds: one stop and its cases on a route with slack, a second truck where the route it would join is already full, or a whole route-day where no route reaches. Carried onto a new store, the share charges route fixed costs a second time to a site that joins a route, and undercharges a site that needs its own. Which candidate rides which route, with how much slack, comes only from joining each site to the route plan. The audit cannot show it, because every audited store sits mid-route on a dense metro route. |

## 1. Situation

A regional grocery chain can open one store next year and has shortlisted six sites: Northgate, Riverside, Pine Ridge, Millbank,
Brookfield and Ashgrove. The real-estate team ranks sites by grocery spend within three miles. The chain's location model gives
store-choice shares from store size and distance with filed parameters. Competitor sizes come from the state retail census, which
publishes sales floor area by size class and county and suppresses cells with fewer than three stores. The finance manual charges
logistics to store P&Ls at the network rate per case, and the internal audit has verified it on a random sample of stores. The capital
committee judges a new store on the incremental annual contribution it adds to the chain.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the spend estimates, the census tables, the audited P&Ls, the network rate, and the route plan
  with its slack. The finance manual's rate is right for the store P&Ls it was built for. No stakeholder read is overturned. The
  difficulty is what a new store adds to delivery cost, and that depends on the route each site would join.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the three-mile ranking and every voice. The location model and the audited rate still produce a confident
  ranking with Pine Ridge on top.
* **Instrument repair.** Trace every logistics dollar to source, as the audit already does. The audited shares stay correct for today's
  stores, and a new stop on a route with slack still costs only its stop and its cases.
* **Lens swap.** The naive read is a share of today's routes. The answer is the change in next year's route plan, a different book.

## 3. The driving force

A strong solver discounts the three-mile spend because two of the chain's own stores sit near Northgate, and it runs the location model
for incremental chain sales. It finds the competitor near Riverside listed by the scouts without a size, sees that the census suppresses
that store's size class, and bounds it from the county's published total floor area: at least 98,000 square feet, a hypermarket that takes
Riverside's catchment. It then charges logistics at the audited rate, which the audit confirms on all 15 sampled stores, and Pine Ridge
wins. But Pine Ridge sits 41 miles past the end of any route and needs its own route-day seven days a week, $1.04M a year. Millbank sits
on Route 6, which already runs at its drivers' hours limit, so adding it splits the route and puts a second truck on the road five days a
week. Brookfield sits two miles off Route 14, which runs with three and a half hours of slack, so it adds one stop and its cases. The
audited rate charges every site the same per case, so it overcharges Brookfield by $350k and undercharges Pine Ridge by $580k and Millbank
by $170k.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Grocery spend within three miles | A, Northgate ($98M) | The real-estate team's screen on the census spend estimates | The chain's store list: two of its own stores lie within four miles of Northgate, and the location model gives the new store mostly their shoppers |
| 1 | Incremental chain sales from the location model, the scouted competitor without a size set at the county's mean store (32,000 sq ft), margin less opex less cases × $1.10 | B, Riverside ($1.61M, 1.20× over C) | Cannibalisation removed with the chain's own model and the audited cost rate | The census: county K's published total floor area, against its published size classes, puts the suppressed store at no less than 98,000 sq ft |
| 2 | The same with the hypermarket bounded from the published totals | C, Pine Ridge ($1.34M, 1.20× over Millbank) | Every competitor sized from published figures; the audited rate verified 15 of 15 | The route plan: Pine Ridge lies 41 miles beyond the last stop of any route and needs its own route-day seven days a week |
| 3 | **Decisive:** the same sales, with logistics as the cost the site adds to next year's route plan (stop and cases on a route with slack, or the fixed cost of the route-day it needs) | **E, Brookfield** (5th of 6 on rung 0), **$1.22M a year** | — | — |

* **Position table.** Brookfield ranks 5th on rung 0, 4th on rung 1 and 3rd on rung 2 (tied with Ashgrove each time), and leads only
  rung 3 (1.28× over Millbank).
* **Discriminator dominance.** Pine Ridge carries a 1.54× advantage into rung 3 ($1.34M against $0.87M). Replacing the share with the
  added cost multiplies Brookfield's contribution by 1.40 and Pine Ridge's by 0.57, an edge of 2.45×, 1.33 times the 1.85× floor.
  Product: 2.45 / 1.54 = 1.59, Brookfield $1.22M against Pine Ridge $0.77M.
* **Partial correction priced (L3).** Every half-applied construction names a wrong site. A solver who costs logistics by added route
  cost but leaves the hypermarket at the county mean names Riverside ($2.11M against Brookfield's $1.22M, 1.73×). One who charges every
  site only a stop and its cases, as if each joined a route with slack, names Pine Ridge ($1.77M against Millbank's $1.47M, 1.20×). One
  who keeps the audited rate and adds route-days for the two sites no route reaches names Millbank ($1.12M against $0.87M, 1.29×), and
  so does one who charges each site its route's cost per case after adding it ($1.10M against Brookfield's $0.92M, 1.20×), because both
  miss Route 6's split and still charge Brookfield a share of Route 14.
* **Grid.** Sales (three-mile capture, location model) × hypermarket (county mean, bounded) × logistics (audited rate, added cost) gives 8
  cells. Capture-based cells all name Northgate (4.2× clear on the audited rate, the only positive site on added cost); model-based cells
  name Riverside (1.20×), Riverside (1.73×), Pine Ridge (1.20×) and the answer. Brookfield's figure in any other cell is at least 28% from
  $1.22M.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The finance manual says how store P&Ls are charged. The fleet cost schedule gives route-day, stop and case
   costs. No document says a new store should be charged what it adds rather than its share.
2. **Corpus blind for a computable reason.** *In every audited store the verified logistics cost equals its cases × $1.10 within 3%,
   because the audit sample was drawn from the twelve metro routes, each carrying six to eight stores at the same fixed cost per case.*
   No audited store sits at a route's end or alone on a route, so the audit reproduces the share 15 of 15 and cannot show an added cost.
3. **No arithmetic symptom.** Shares sum to total logistics cost under either reading, sales reconcile to the location model, and the
   census bound ties to the county total.
4. **Not a row predicate.** Each site is placed against the route plan (nearest route, its days and slack hours), the added cost is
   built from the fleet schedule, and only then does the contribution re-rank.
5. **The enumeration is arithmetic.** No column gives a site's route or slack; the route plan lists stops and hours.
6. **No cutover date.** Routes and slack are this year's standing plan, and no series steps.
7. **Survives deletion.** Removing the three-mile ranking and every voice leaves the audited rate certified 15 of 15.

## 6. The calibration corpus

* **Form.** The internal audit's gold-standard sample: 15 stores drawn at random from the metro routes, every cost line traced to
  source, with verified contribution.
* **What it certifies.** The location model's sales for those stores and the network rate of $1.10 a case, 15 of 15 within 3%. A
  per-store fixed charge instead of a per-case rate reproduces 4 of 15, all its misses running high.
* **What it is blind to.** Added route cost (above).
* **Twin pair.** Brookfield and Ashgrove are identical on three-mile spend, modelled sales ($18.0M), format, rent and operating cost.
  Brookfield joins Route 14; Ashgrove lies 22 miles from any route and needs its own route-day five days a week. They add $1.22M and
  $0.60M, 2.0× apart, separated only by the route each would ride.
* **Resemblance points at the decoy.** Pine Ridge, the largest-format candidate, most resembles the audit's highest-contribution stores.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The capital committee's rule: a new store is judged on the incremental annual contribution it adds to the chain. The
  location model's parameters (size exponent 1, distance exponent 2). The fleet cost schedule: a route-day costs $1,950 plus $2.40 a mile, a stop $150
  and a case $0.35. The route plan: each route's days, stops and slack hours.
* **Empirical pins.** The hypermarket's size, bounded from the census totals. Each site's route, from the route plan.
* **Voices.** The head of real estate: "Northgate has the most grocery spend within three miles of any site we've looked at." The
  finance controller: "Our audited cost per case is the number. I don't want site-by-site logistics games."
* **Licensed wrong basis.** The committee's rule records that the board's property advisers rank sites on three-mile grocery spend and
  will present that ranking at the meeting.

## 8. Determinism by construction

* **The bound.** County K publishes two suppressed stores, one in the 50,000–80,000 class and one above 80,000, and a total that leaves
  178,000 sq ft for the pair, so the hypermarket lies between 98,000 and 128,000 sq ft. Every value in that range keeps Riverside below
  Pine Ridge and Brookfield, and Riverside's own figures are graded as upper bounds.
* **Slack.** Route 14 has 3.5 hours of slack on each of its five days and Brookfield's stop takes 40 minutes, so no rerouting reading
  changes its added cost. Route 6 has 10 minutes of slack against Millbank's 55-minute stop and detour, so it splits under any reading,
  and the split and the new route-days are priced from the schedule alone.
* **Sales.** The location model's parameters are filed, and every site's catchment is closed at 15 miles with no store at that edge.
* **Rounding.** Brookfield's contribution is $1,221,000, mid-bin at the nearest $10k.

## 9. Prompt sketch and deliverables

> We can open one store next year and the capital committee meets on the 9th. Our head of real estate swears by Northgate's catchment.
> Which of the six shortlisted sites do we open, and what incremental contribution a year will it add, to the nearest $10k? Give me the
> answer as one sentence I can read out, with `site_contribution.xlsx`, a map `catchment_routes.png`, and a short `capital_note.pdf`.

* `site_contribution.xlsx` — the six sites on four bases, the logistics build per site, the shrink sheet (ask A) and the county sheet
  (ask B).
* `catchment_routes.png` — a script-rendered map: the six sites, the chain's stores and the hypermarket, delivery routes drawn with their
  slack hours, each site's catchment shaded by incremental sales, the route-day Pine Ridge would need dashed, and Brookfield's stop
  marked on Route 14.
* `capital_note.pdf` — the committed site, its contribution, and why each of the other five falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 chain stores within 15 miles of a candidate, last year's shrink as a share of
  sales and its change on the prior year. *Device:* damaged goods returned to a supplier for credit post as negative shrink lines with a
  credit-memo reference, and the shrink policy excludes credited items. Counting them inflates shrink at the four stores with
  direct-delivery vendors.
* **Ask B (device-carried).** For each candidate's county, the share of households receiving food assistance and its margin of error.
  *Device:* the survey publishes one-year estimates only for counties above 65,000 people, and its guide says to compare counties on
  five-year estimates throughout. Mixing the two puts two counties in the wrong order.
* **Ask C (validity).** Each site's contribution under each of the four rung bases, and the hypermarket's size bound.
* **Decoupling.** Charging logistics at the audited rate changes no figure in asks A or B. Shrink records and county survey tables touch
  neither the route plan nor the location model's sales.

## 11. Rubric arithmetic

12 stores × 2 (ask A) + 6 counties × 2 (ask B) + 6 sites × 4 bases and the bound (ask C) + the committed site, its contribution, the
runner-up and the margin + 5 named chart parts + 3 files ≈ 73 criteria.

## 12. World-building constraints

* Three-mile spend ($M): 98, 80, 70, 72, 55, 55; the screen's capture is 20% of it. Modelled incremental sales ($M): 14.0, 25.0 (18.6
  with the hypermarket bounded), 21.5, 18.0, 18.0, 18.0. Operating cost ($M): 3.9, 4.6, 4.0, 3.35, 3.6, 3.6. Margin 28%; 28,571 cases per
  $1M of sales.
* Added route fixed cost ($M a year): Northgate, Riverside and Brookfield $0.04 (a stop five days a week on a route with slack),
  Millbank $0.56 (a stop, and Route 6's split: 260 route-days of 20 miles), Pine Ridge $1.04 (364 route-days of 380 miles), Ashgrove
  $0.66 (260 route-days of 240 miles). Route 6 carries 3.12M cases a year, Route 14 3.5M.
* Rung leaders A, B, C, E at 1.23×, 1.20×, 1.20×, 1.28×; Brookfield is 5th, 4th, 3rd, 1st.
* Every audited store sits mid-route on a metro route of six to eight stores.
* Brookfield and Ashgrove match on every column outside the route plan.
* Shrink and county survey records never touch routes, sales or the census size table.
