# task153: Keeble Supply's six yard islands, how many of Overton's discounted loads to contract (architecture 1)

Private, never ships. A new build (wave 4, the last of the wave), numbered from seed FC24. The seed (a delivery fleet on
network fuel cards at six depots in three card accounts, offered discounted 8,000-gallon tanker loads after a 60-cent
wholesale drop) was read at its header and Situation only. Its world, decision and quantity are kept. Its two filed
methods are not shipped: the procurement standard that places loads one at a time where the next lowers cost most (the
HOW of an allocation) and the procurement memo's retail-price regression (the HOW of the forecast); the rebate floor is
not a withheld rule (the card agreements state their terms plainly and none of them decides the call). The pitfall is
re-found from how the fleet's own records come to exist: a card fill records where a vehicle bought fuel and how much,
the telematics service records how far it drove, what it burned and where it stopped, and an island at the yard can only
fuel a vehicle when the vehicle is at the yard, at most a tankful at a time.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task153.json`, architecture v1; `guard.py check` WARN (`three_rules.strategy_risk`, `repeat.gate_g`), answered below; the older same-puzzle signature (objective, C, quantity_figure) differentiated on the card against task105, task37, task69, task87 and task94, the older same-driver match task105 v2 likewise; kin lines also against task150, task145, task16 and task106 |
| Domain / task type | house domain `supply-chain-logistics` (subdomain `sourcing-procurement`, fleet fuel procurement), client domain `general-statistics-data-science`, task type `resampling-simulation-monte-carlo-methods` (serves Forecasting): the eight-week draw is a replay of each vehicle's own recent duty through what an island can put aboard, at its independent unit, the stretch of driving between two yard visits, never the card fill or the vehicle-day |
| Objective | Forecasting & Predictive Modeling: each yard island's draw over 14 September to 8 November 2026, a window not yet begun at the as-of date (Friday 28 August 2026), built from the fleet's own telematics, card and island history |
| Shape | `other`: the load count with its six yard counts and the saving it books, a chart of each yard's weekly island draw against its card gallons, and row-set asks on rows the call never reads; criteria counted in `## Ask sheet` |
| Decision | `quantity_figure`, answer unit `count` (whole loads, each yard's loads the whole loads its island hands out in the window) |
| Mechanism | gap objective (decisive: the card gallons are correct and the call is not scored on them, it is scored on what the islands can put aboard, which a yard visit and a tankful limit) with population (the unit that limit applies to is the stretch between yard visits); pattern C (the serviceable share of each vehicle's fuel, built behind a join of telematics days, yard geofence visits and the maintenance system's tank specs), D; generators G7, G2, G6; Gate G `forecasting`; strategy `grain_or_unit` |
| Layer 2 family / pattern | `field_method` (the field's own convertible-volume sizing for on-site fueling, done at the duty cycle rather than read off the card history); `own:yard-island-draw-built-segment-by-segment-between-yard-visits-capped-at-a-tankful` |
| Furniture | forum `customer_or_counterparty` (Overton Petroleum needs a firm count by Friday 4 September), forcing event `purchase_order_or_contract` (the offer's take-or-pay count), organisation family `other` (a wholesale distributor), role family `procurement_lead`, context artifact `operations_log` (the 2025 island transactions from the fuel management system), calibration `pilot_log` (the two 2025 island programmes), opening `question-first`, question form `how-many` |
| Spine | the telematics service's vehicle-day export, September 2024 to August 2026 (about 112,000 vehicle-day rows: miles, engine hours, idle hours, engine-reported fuel, first and last position, device serial), beside its yard geofence event export; constructed |
| Deliverables | `overton_loads_sep-nov_2026.xlsx` (the count by yard, the saving, the weekly draw build, the ask tables, notes) and `yard_island_draw.png` (each yard's weekly island draw against its card gallons, the loads marked); the format set (xlsx and png) rotates away from task152 (xlsx and pdf) and task151 (docx) |
| People | drawn with `guard.py names --geo "United States" --seed 153` (first names and surnames checked clean against every pack): Theresa Mercado (Overton Petroleum's commercial account manager, the offer letter and the 2025 programme letters), Gabriel Wyatt (Keeble's fleet services manager, the maintenance system's unit list and the yard notes), Dennis Stewart (Keeble's controller, the card programme summary); the requester, the fleet cost analyst, is in no file and not in the prompt |

**Guard.** `guard.py check` at the draw: BLOCK twice on the first card (gap population, pattern D: the
`test.same_puzzle_older` signature is spent in 14 builds, `test.same_driver_older` against task181 v4 and task60 v8),
redrawn to the honest keys (the decisive gap is the objective: the card gallons are right and the call is scored on
what the islands can put aboard; the pattern is C, a serviceable share built behind a join). That signature repeats five
older builds (task105 v2, task37, task69 v3 and v4, task87 v5) and task94, each a different insight, differentiated on
the card in one line. A trial of Gate G `binding_constraint` collided with ten more (task128, task28, task32, task51,
task53, task92) and was dropped: `forecasting` is the honest mechanism, the stump lives in how the forward draw is
forecast. Two WARNs stay, answered: `three_rules.strategy_risk` (grain_or_unit): the analyst test below is the easy
analytical route that still fails with every field and term read correctly (the card gallons, the 2025 islands' share,
the share by vehicle class); `repeat.gate_g` (forecasting, task464): this is the Forecasting lane and task464 is an
emissions back-test of fit windows, sharing no other axis. Three personas first drawn (Carla, Robert, Lisa, then
Garrett, Bethany, Shane) warned on first names in older packs and were replaced from the same seed's list.

**Same-puzzle and same-driver tests.** Gap objective, decisive pattern C, decision `quantity_figure`, Gate G
`forecasting`: no build in the last twelve carries either triple; the older matches carry their differentiation.

**Abstraction test.** Stripped of nouns: the volume a site's own supply takes over from a roaming supply is set segment
by segment, between each unit's visits to the site, at the smaller of the segment's need and what one fill carries; the
units' purchase history overstates it where segments outrun a fill, a share measured at sites whose units visit often
misstates sites whose units visit rarely, and segments cut only at overnight stops understate it where units come back
during the day. The nearest by mechanism, read for latent structure rather than score:
- task16 floors each building's shortfall at zero because stock cannot move between buildings; here nothing is netted
  across sites, the cap is one vehicle's tankful at one visit and the unit is built from where and when it comes back.
- task94 tests whether a site's tank can take a full delivery on top of its held stock; here every yard tank holds two
  loads with room and receiving never binds, the draw does.
- task106 sizes suppliers that share one corridor's return legs; here no capacity is shared between yards or vehicles.
- task150 places a fixed 24 classrooms at most eight a school on a cohort-component projection; here the total is the
  answer, no site has a fixed cap, and the deciding quantity is a channel switch's draw.
- task145 forecasts a count above a line through each segment's exchange-rate pass-through; here the card prices are
  cost-plus on the same rack the loads are priced on, so no price is forecast and the decisive step is on volume.
- task138 replays driver traces through a store rebuilt from recorded inputs; here no store is rebuilt, each segment is
  capped on its own.
None shares the latent structure, the default path and the correction.

**Data-native sentence.** Keeble's card exports record a fill wherever a driver bought fuel, its telematics service
records each vehicle's miles, fuel burned and where it stopped and stayed each night, and its yard islands can fuel a
vehicle only while it is in the yard, at most what its tanks hold above the reserve its driver keeps: Blountville's
sleepers on four-night loops and Cookeville's vans parked at the Sparta and Crossville lots burn far more between yard
visits than one fill carries, while Nashville's double-loop sleepers come back to the yard to reload midweek, a visit no
overnight position shows; the island's draw is built stretch by stretch between visits, and the 2025 Jackson and
Knoxville programmes, whose vehicles came back daily or between short loops, measured it on a different duty mix.

**Sources read, one line each.**
- `guard.py mechanisms --objective forecasting` (64 builds): the nearest spent ground is per-site netting (task16), a
  receiving limit on a full delivery (task94), a store rebuilt from traces (task138), runs that need every unit to have
  room (task147) and a fixed-plus-variable rate re-paid on a denser period (task67); none sizes a channel switch by the
  segment between visits and a fill.
- The five kin cards the brief names (task150, task145, task16, task106, task11): the decision shape moves from a fixed
  24 placed across sites to a total that is the answer; the pitfall is on volume, not pass-through; nothing is floored
  at zero across sites, nothing is shared, and no rebate threshold decides anything.
- `two-layer-task-design.md`: "the data's real structure" and "validating a forecast properly" are the client's frames;
  the 2025 programmes are the out-of-sample record every candidate method is scored on.
- `layer2-rigor-patterns.md`, general statistics: "resample the independent unit" is the pattern this build's own
  version stands on (the unit is the segment between visits).
- task148 and task151 design notes (a one-scalar calibration and a reference class landed their calls): here the
  history-calibrated family (the 2025 islands' pooled share, by yard, by class, by nights away) is swept and asserted to
  miss (`## Ladder`).

**World.** Keeble Supply Co. (fictional), a Nashville wholesale distributor of janitorial, paper and foodservice-disposable
supplies, delivers to schools, hospitals, restaurants and building-service contractors across Tennessee from six yards:
Memphis and Jackson (the West, from the 2019 purchase of Delta Paper & Chemical), Nashville and Cookeville (the Central,
Keeble's own), Knoxville and Blountville (the East, from the 2022 purchase of Holston Sanitary Supply). Each acquisition
kept its fleet card account, so the fleet buys on three: Delta's direct-bill account with a truck-stop chain, Keeble's
network fleet card, and Holston's marketers' group card, each priced cost-plus off the day's rack at the station's supply
terminal. Each yard has a 20,000-gallon above-ground diesel tank and a self-serve island on the fuel management system,
kept on standby since the fleet moved to cards in 2023; Overton Petroleum Co. (fictional), a Cookeville jobber, filled
the Jackson tank from 9 March to 16 May 2025 and the Knoxville tank from 8 June to 9 August 2025 on promotional terms.
In August 2026 the Gulf Coast rack fell 60 cents in three weeks; Overton, long on terminal allocation, offers up to 32
transport loads of 8,000 net gallons for the eight weeks from Monday 14 September to Sunday 8 November 2026 at its
posted rack on the day of lifting plus 1.9 cents delivered, the count firm by Friday 4 September and every contracted
load billed. Keeble wants only the loads its islands will hand out by 8 November. The fleet: cargo vans and box trucks
on metro routes out of each yard every working day; Jackson's day cabs on regional day runs; sleeper tractors at
Jackson, Nashville, Knoxville and Blountville on loops of one to four nights (Nashville's on two two-night loops a week
with a midweek reload at the yard); Cookeville's vans parked at the Sparta and Crossville lots, fed by a shuttle and in
the yard once a week for inspection.

## Default path

Paper figures from the prototype (`scratch proto/ev2.py`, fleet F5); built figures replace them at stage 3.

1. Read Overton's offer: up to 32 loads of 8,000 net gallons, 14 September to 8 November, rack plus 1.9 cents, the
   count firm and every contracted load billed; Keeble takes only what its islands hand out by 8 November.
2. Stack the three card exports (Delta's CSV, Keeble's monthly XLSX statements, Holston's fixed-width TXT), map each
   fill to its unit and each unit to its yard through the maintenance system's unit list.
3. Forecast each yard's card gallons for the eight weeks from its recent weeks (flat across the year; the same weeks of
   2025 agree).
4. Each yard takes the whole loads its card gallons fill, the island taking over what the cards now carry; sum.

Ends on: 30 loads (Memphis 2, Jackson 5, Nashville 8, Cookeville 3, Knoxville 5, Blountville 7).

Golden: 23 loads (Memphis 2, Jackson 5, Nashville 8, Cookeville 1, Knoxville 4, Blountville 3): each island hands each
vehicle, for every stretch of driving between two of its yard visits, the smaller of the fuel burned on that stretch and
what its tanks hold above the reserve its driver keeps, built from the telematics days and the yard geofence visits of
the recent weeks and replayed over the window.

## Stump sentence

Taking each yard island to hand out what its vehicles now buy on the three card accounts contracts 30 loads, and scaling
the card gallons by the share the 2025 Jackson and Knoxville islands handed out (27) or by that share for each vehicle
class (26) still overshoots; the step that lands each there is treating a yard as able to supply a vehicle's whole fuel,
when an island fuels a vehicle only while it is in the yard and at most a tankful at a time, so Blountville's four-night
sleepers and Cookeville's vans at the Sparta and Crossville lots move far less than their card gallons; and capping each
vehicle's run between nights at the yard instead (19) undershoots, because Nashville's double-loop sleepers reload at the
yard midweek: only the stretch between yard visits, capped at a tankful, contracts 23.

## Three rules

- **Task type:** general-statistics-data-science, resampling-simulation-monte-carlo-methods (serves Forecasting), house
  domain supply-chain-logistics (fleet fuel procurement): the eight-week island draw is forecast by replaying each
  vehicle's recent duty at its independent unit, the stretch of driving between two yard visits, through what one island
  fill can put aboard, and checked against the two 2025 island programmes.
- **Domain test:** the deciding quantity is each yard island's draw over the window, which fleet fuel management sizes
  as convertible volume from duty cycles (how often each vehicle is at its yard against how far a tankful carries it) and
  checks against past on-site programmes, never from the card history alone.
- **Swap:** "how many of a hospital's medication deliveries its ward stock would replace" keeps a channel switch and a
  history of purchases, but a fuel tank that caps what one visit can put aboard, yard visits that the telematics geofence
  records apart from overnight stops, and a driver's reserve have no counterpart, so the quantity that sets the count
  stops making sense.
- **Layer 1:** three card exports in three layouts and time conventions (a truck-stop chain's direct-bill CSV in Central
  time, a network's monthly XLSX statements, a marketers' group fixed-width TXT in Eastern time); telematics vehicle days
  in UTC under device serials mapped to units through a dated device-assignment table with swaps; unit numbers written
  three ways across the maintenance system, the card prompts and the telematics names; the 2025 island transactions with
  a batch the fuel management system resent after a modem outage; Overton's bills of lading in net gallons at 60 F
  against island meters in gross gallons; rack postings effective 6 pm for the next day's liftings; tank capacities in
  the maintenance system's spec table by model, not on the unit record. Each is what these systems write; none carries
  the stump (asserted item by item at stage 3).
- **Layer 2:** `field_method`: the convertible volume of an on-site fueling programme is built at the duty cycle, the
  stretch between yard visits capped at a tankful, and validated on past programmes before it is carried onto yards whose
  duty mix differs.
- **Decisive step:** build each vehicle's stretches of driving between consecutive yard visits from the telematics days
  and the geofence visits, take for each the smaller of the fuel burned and the tankful above the driver's reserve (the
  fills the 2025 islands put aboard returning sleepers), sum by yard over the recent weeks and replay the window.
- **Not semantics:** every field (the fill's gallons, unit and site, the vehicle day's fuel and positions, the geofence
  entries and exits, the tank spec, the island's gallons) and every filed term (the offer's count, window and price, the
  card agreements' margins, the meaning of "hand out by 8 November") is read the same way by the easy routes; no field,
  code or definition says how much of a vehicle's fuel an island can supply, and the routes that read them all file 30,
  27, 26 or 19.
- **Not rule application:** the shipped sentences that bear on how the count is computed (the offer's load size, window,
  count and billing; the islands' self-serve status; the tank capacities; the card terms) are executed word for word in
  `checks.py`: their only literal product is the card gallons filled with whole loads, 30, never the golden; no filed
  sentence says when an island can fuel a vehicle or how much it can put aboard.
- **Analyst test:** a strong analyst who stacks the three card exports, maps cards to units and units to yards, and reads
  the offer and the card agreements correctly forecasts each yard's eight-week card gallons and contracts the loads they
  fill, 30; scaling by the 2025 islands' share files 27, by that share per vehicle class 26, by nights at the yard 17;
  capping each vehicle's run between overnight stops at a tankful files 19 (to be executed on the generator's clean truth
  at stage 3).
- **Estimand:** the prompt and Overton's offer letter: the number of 8,000-gallon loads to contract for 14 September to 8
  November 2026, each yard taking only the whole loads its island will hand out in those eight weeks to Keeble's own
  vehicles, with the saving those loads book against the same gallons bought on the vehicles' card accounts; the
  population (the six yards' vehicles as they run now), outcome (gallons handed out), window, unit (whole loads per yard)
  and comparison (the card accounts' price for the same gallons) are filed, the method is not.
- **No decoy:** no consultant study, prior programme memo, desk draft or stakeholder figure states or argues a load count,
  a convertible share or an island draw for any yard (asserted at stage 3); Overton's 2025 programme letters state the
  loads delivered and nothing about capture; the controller's card summary states card gallons and spend.
- **No certified replay:** no certified or published figure for the window ships and nothing graded is reproduced; the
  2025 island transactions are raw records every candidate method is scored on, and no wrong method reproduces them
  vehicle by vehicle (asserted at stage 3).
- **Lesson:** a channel switch moves only what the new channel can reach: an on-site supply fuels a vehicle only at its
  visits and at most a tankful each time, so the volume a yard tank takes over is built from duty cycles, the stretch
  between visits against the tank, checked on past programmes, and never read off the old channel's purchases or off a
  share measured on another duty mix; no build on file teaches it.

## Readability screen

To be written at stage 2.

## Semantic fork table

To be written at stage 2.

## Ladder

To be written at stage 2.

## Closure table

To be written at stage 2.

## Literal reader

To be written at stage 2.

## Oracles

To be written at stage 2.

## Ask sheet

To be written at stage 2.

## Tried and rejected

- Retail pass-through after the drop as the decisive quantity (the seed's own driver: card prices fall slowly, so early
  loads save most): rejected at the draw as a pass-through echo of task145; the card agreements are cost-plus off the
  same rack the loads are priced on, so no price is forecast.
- The regional rack's basis reverting after the drop (a lock worth more where the local rack fell further than the
  benchmark): rejected at the draw; "will the drop last" is the headline question every solver asks, and it is an
  adjustment speed, a pass-through cousin.
- Summer-grade loads usable only until each yard's first night below the fuel's cloud point (a first-passage probability
  under serially dependent nights): rejected at the draw; a fleet would additise, and thirty years of daily minima pin a
  ten-per-cent first-freeze date too loosely to grade.
- A per-trip tankful cap with no midday visits and no past programme (pure physics): rejected at the draw; the 2025 island
  record would bless the card gallons (a validated decoy) and the physics alone would be argued, not shown out of sample.
- The first card's keys (gap population, pattern D): blocked by the guard as a spent signature (14 builds) and as task181
  v4's and task60 v8's driver signature; the honest keys are objective and C.
