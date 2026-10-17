# task153: Keeble Supply's six yard islands, how many of Overton's discounted loads to contract (architecture 1)

Private, never ships. A new build (wave 4, the last of the wave), numbered from seed FC24. The seed (a delivery fleet on
network fuel cards at six depots in three card accounts, offered discounted 8,000-gallon tanker loads after a 60-cent
wholesale drop) was read at its header and Situation only. Its world, decision and quantity are kept. Its two filed
methods are not shipped: the procurement standard that places loads one at a time where the next lowers cost most (the
HOW of an allocation) and the procurement memo's retail-price regression (the HOW of the forecast); the rebate floor is
not a withheld rule (the card agreements state their terms plainly, no agreement carries a volume rebate, and none of
them decides the call). The pitfall is re-found from how the fleet's own records come to exist: a card fill records
where a vehicle bought fuel and how much, the telematics service records how far it drove, what it burned and where it
stopped, and an island at the yard can only fuel a vehicle when the vehicle is at the yard, at most a tankful at a time.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task153.json`, architecture v1; `guard.py check` WARN (`three_rules.strategy_risk`, `repeat.gate_g`), answered below; the older same-puzzle signature (objective, C, quantity_figure) differentiated on the card against task105, task37, task69, task87 and task94, the older same-driver match task105 v2 likewise; kin lines also against task150, task145, task16 and task106 |
| Domain / task type | house domain `supply-chain-logistics` (subdomain `sourcing-procurement`, fleet fuel procurement), client domain `general-statistics-data-science`, task type `resampling-simulation-monte-carlo-methods` (serves Forecasting): the eight-week draw is a trace-driven simulation, each vehicle's own recent duty replayed through what an island can put aboard at its independent unit, the stretch of driving between two yard visits, never the card fill or the vehicle-day. Client-domain check (stage 4): the house map sends supply chain to `urban-regional-science` or `general-statistics-data-science`; Urban & Regional Science's `forecasting` and `municipal-service-demand-resource-allocation` model a region's land use and public services, not a fleet's fuel channel, and Energy Systems & Utilities' `load-forecasting` is a utility's grid load; the deciding quantity here is the output of a simulation that replays recorded traces through a capacity limit, the method family this task type names, so the tag stays |
| Objective | Forecasting & Predictive Modeling: each yard island's draw over 14 September to 8 November 2026, a window not yet begun at the as-of date (Friday 28 August 2026), built from the fleet's own telematics, card and island history |
| Shape | `other`: the load count with its six yard counts and the saving it books, a chart of each yard's island draw against its card gallons, and row-set asks on rows the call never reads; criteria counted in `## Ask sheet` |
| Decision | `quantity_figure`, answer unit `count` (whole loads, each yard's loads the whole loads its island hands out in the window) |
| Mechanism | gap objective (decisive: the card gallons are correct and the call is not scored on them, it is scored on what the islands can put aboard, which a yard visit and a tankful limit) with population (the unit that limit applies to is the stretch between yard visits); pattern C (the serviceable share of each vehicle's fuel, built behind a join of telematics days, yard geofence visits and the maintenance system's tank specs), D; generators G7, G2, G6; Gate G `forecasting`; strategy `grain_or_unit` |
| Layer 2 family / pattern | `field_method` (the field's own convertible-volume sizing for on-site fueling, done at the duty cycle rather than read off the card history); `own:yard-island-draw-built-segment-by-segment-between-yard-visits-capped-at-a-tankful` |
| Furniture | forum `customer_or_counterparty` (Overton Petroleum needs a firm count by Friday 4 September), forcing event `purchase_order_or_contract` (the offer's take-or-pay count), organisation family `other` (a wholesale distributor), role family `procurement_lead`, context artifact `operations_log` (the 2025 island transactions from the fuel management system), calibration `pilot_log` (the two 2025 island programmes), opening `question-first`, question form `how-many` |
| Spine | the telematics service's vehicle-day export, September 2024 to August 2026 (79,042 vehicle-day rows: miles, engine hours, idle hours, engine-reported fuel, first and last position, device serial), beside its geofence event export (42,446 rows, March to August 2026); constructed |
| Deliverables | `overton_loads_sep-nov_2026.xlsx` (the count by yard, the saving, the two ask tables, the draw build, notes) and `yard_island_draw.png` (each yard's island draw against its card gallons, the loads marked); the format set (xlsx and png) rotates away from task152 (xlsx and pdf) and task151 (docx) |
| People | drawn with `guard.py names --geo "United States" --seed 153` (first names and surnames checked clean against every pack): Theresa Mercado (Overton Petroleum's commercial account manager, the offer and the 2025 programme letters), Gabriel Wyatt (Keeble's fleet services manager, the unit list, the yard notes and the file list), Dennis Stewart (Keeble's controller, signatory on the card programmes' pricing schedules); the requester, the fleet cost analyst, is in no file and not in the prompt |

**Guard.** `guard.py check` at the draw: BLOCK twice on the first card (gap population, pattern D: the
`test.same_puzzle_older` signature is spent in 14 builds, `test.same_driver_older` against task181 v4 and task60 v8),
redrawn to the honest keys (the decisive gap is the objective: the card gallons are right and the call is scored on
what the islands can put aboard; the pattern is C, a serviceable share built behind a join). That signature repeats five
older builds (task105 v2, task37, task69 v3 and v4, task87 v5) and task94, each a different insight, differentiated on
the card in one line. A trial of Gate G `binding_constraint` collided with ten more (task128, task28, task32, task51,
task53, task92) and was dropped: `forecasting` is the honest mechanism, the stump lives in how the forward draw is
forecast. Two WARNs stay, answered: `three_rules.strategy_risk` (grain_or_unit): the analyst test below is the easy
analytical route that still fails with every field and term read correctly (the card gallons, the 2025 islands' share
pooled, by account or by model); `repeat.gate_g` (forecasting, task464): this is the Forecasting lane and task464 is an
emissions back-test of fit windows, sharing no other axis. Three personas first drawn (Carla, Robert, Lisa, then
Garrett, Bethany, Shane) warned on first names in older packs and were replaced from the same seed's list. At stage 3
and after the stage 4 fix `guard.py heart` is WARN (the same two), nearest driver 0.09 (task146).

**Surface screen (stage 3).** `guard.py surface task153` first promoted task152 (back to back, on the shared file name
`README.md` beside the same decision and context-artifact types); the file was renamed to the fleet's own
`fuel_review_files_2026-08-28.md` and the re-run clears it. Three pairs stay promoted for adjudication, task94, task69 and
task105, all on the card-level gap, pattern and decision collision the draw already differentiated, with surface scores
of 0.080 to 0.087 and no shared file, sentence or name (unchanged after the stage 4 fix). The adjudicated
`/clone-check` is the author's call.

**Same-puzzle and same-driver tests.** Gap objective, decisive pattern C, decision `quantity_figure`, Gate G
`forecasting`: no build in the last twelve carries either triple; the older matches carry their differentiation.

**Abstraction test.** Stripped of nouns: the volume a site's own supply takes over from a roaming supply is set segment
by segment, between each unit's visits to the site, at the smaller of the segment's need and what one fill carries; the
units' purchase history overstates it where segments outrun a fill, a share measured at sites whose units visit often
misstates sites whose units visit rarely, and segments cut only at overnight stops understate it where units come back
during the day. The nearest by mechanism, read for latent structure rather than score:
- task16 floors each building's shortfall at zero because stock cannot move between buildings; here nothing is netted
  across sites, the cap is one vehicle's tankful at one visit and the unit is built from where and when it comes back.
- task94 tests whether a site's tank can take a full delivery on top of its held stock; here every yard tank takes a
  whole load over its unpumpable bottom with 2,000 gallons or more to spare and receiving never binds, the draw does.
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
visits than one fill carries, while Nashville's double-loop sleepers come back to the yard at midday every Wednesday, a
visit no overnight position shows; the island's draw is built stretch by stretch between visits, and the 2025 Jackson
and Knoxville programmes, whose vehicles mostly came back daily or between one-night loops, measured it on a different
duty mix.

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
  history-calibrated family (the 2025 islands' pooled share, by account, by model, by nights at the yard) is swept and
  asserted to miss (`## Ladder`).

**World.** Keeble Supply Co. (fictional), a Nashville wholesale distributor of janitorial, paper and foodservice-disposable
supplies, delivers to schools, hospitals, restaurants and building-service contractors across Tennessee from six yards:
Memphis and Jackson (the West, from the 2019 purchase of Delta Paper & Chemical), Nashville and Cookeville (the Central,
Keeble's own), Knoxville and Blountville (the East, from the 2022 purchase of Holston Sanitary Supply). Each acquisition
kept its fleet card account, so the fleet buys on three: Delta's direct-bill account with a truck-stop chain, Keeble's
network fleet card, and Holston's marketers' group card, each priced cost-plus off the TriState contract average at the
station's supply terminal. Each yard has one above-ground diesel tank (12,000 to 25,000 gallons; Jackson's and
Knoxville's 20,000) and a self-serve island on the fuel management system, kept on standby since the fleet moved to
cards in 2023; Overton Petroleum Co. (fictional), a
Cookeville jobber, supplied the Jackson tank from 10 March to 29 May 2025 and the Knoxville tank from 9 June to 22
August 2025 on promotional terms (each island then ran its last load down, to 2 June and 3 September). In August 2026
the Gulf Coast rack fell a little over 60 cents; Overton, long on terminal allocation, offers up to 32 transport loads
of 8,000 net gallons for the eight weeks from Monday 14 September to Sunday 8 November 2026 at the TriState contract
average on the day of lifting plus 1.9 cents delivered, the count firm by Friday 4 September and every confirmed load
billed. Keeble wants only the loads its islands will hand out by 8 November. The fleet (157 active units; two spare box
trucks and five units sold in the autumn of 2024 stay on the maintenance list): vans and box
trucks on metro routes out of each yard every working day; Jackson's day cabs on regional day runs with a midday reload
at the yard on Tuesdays and Thursdays; sleeper tractors at Jackson (three-night loops), Nashville (two two-night loops a
week, back at the yard at midday every Wednesday), Knoxville (one-night loops, and two on four-night loops) and
Blountville (four-night loops, the Appalachian routes at about 5 mpg); Cookeville's 32 vans based at the Sparta and
Crossville lots, stocked by shuttle and in the yard on Mondays.

## Default path

Built figures (`generator/calc.py` on the shipped files; asserted in `generator/checks.py`).

1. Read Overton's offer: up to 32 loads of 8,000 net gallons, 14 September to 8 November, the TriState average on the
   day of lifting plus 1.9 cents, the count firm and every confirmed load billed; Keeble takes only what its islands
   hand out by 8 November.
2. Stack the three card exports (Riverbend's CSV, the Crossroads XLSX, the SMPM fixed-width TXT), drop DEF and the
   re-sent SMPM week, map each fill to its unit and each unit to its yard through the maintenance system's unit list.
3. Forecast each yard's card gallons for the eight weeks from its recent weeks (the trailing eight complete weeks; 13
   weeks, a working-day scaling and the same weeks of 2025 agree).
4. Each yard takes the whole loads its card gallons fill, the island taking over what the cards now carry; sum.

Ends on: 29 loads (Memphis 2, Jackson 5, Nashville 8, Cookeville 3, Knoxville 5, Blountville 6).

Golden: 23 loads (Memphis 2, Jackson 5, Nashville 8, Cookeville 1, Knoxville 4, Blountville 3), saving $17,408: each
island hands each vehicle, at each yard visit, the smaller of the fuel burned since its previous yard visit and its tank
less the 10.2 per cent reserve the 2025 islands show sleepers coming back on, built from the telematics days and the
geofence visits of the eight weeks 29 June to 23 August and scaled from their 39 working days to the window's 40.

## Stump sentence

Taking each yard island to hand out what its vehicles now buy on the three card accounts contracts 29 loads, and scaling
the card gallons by the share the 2025 Jackson and Knoxville islands handed out (pooled, by account or by vehicle model)
still files 26 to 28; the step that lands each there is treating a yard as able to supply a vehicle's whole fuel, when an
island fuels a vehicle only while it is in the yard and at most a tankful at a time, so Blountville's four-night
sleepers and Cookeville's vans at the Sparta and Crossville lots move far less than their card gallons; and capping each
vehicle's run between nights at the yard instead (19) undershoots, because Nashville's double-loop sleepers reload at the
yard every Wednesday at midday: only the stretch between yard visits, capped at a tankful, contracts 23.

## Three rules

- **Task type:** general-statistics-data-science, resampling-simulation-monte-carlo-methods (serves Forecasting), house
  domain supply-chain-logistics (fleet fuel procurement): the eight-week island draw is forecast by a trace-driven
  simulation, replaying each vehicle's recent duty at its independent unit, the stretch of driving between two yard visits, through what one island
  fill can put aboard, and checked against the two 2025 island programmes.
- **Domain test:** the deciding quantity is each yard island's draw over the window, which fleet fuel management sizes
  as convertible volume from duty cycles (how often each vehicle is at its yard against how far a tankful carries it) and
  checks against past on-site programmes, never from the card history alone.
- **Swap:** "how many of a hospital's medication deliveries its ward stock would replace" keeps a channel switch and a
  history of purchases, but a fuel tank that caps what one visit can put aboard, yard visits that the telematics geofence
  records apart from overnight stops, and a driver's reserve have no counterpart, so the quantity that sets the count
  stops making sense.
- **Layer 1:** three card exports in three layouts and time conventions, each stated in its own schedule or layout (a
  truck-stop chain's direct-bill CSV stamped in UTC, a network's XLSX dated by its business day closing at 10 pm Central,
  a marketers' group fixed-width TXT with implied decimals, business days and a week sent twice), each with a day a site
  posted twice and credited in a later week; telematics vehicle days in local time beside geofence events in UTC, under device
  serials, eight new devices reporting under their serials for a few days in March and April; unit numbers written three
  ways across the maintenance system, the card prompts and the telematics names; the 2025 island transactions with a
  day's buffer the fuel management system uploaded twice after a modem outage; Overton's bills of lading in net gallons
  beside drops in gross gallons; rack postings effective 6 pm Central for the next day's liftings; tank capacities in the
  maintenance system's spec sheet by model, not on the unit record. Each is what these systems write; none carries the
  stump (asserted item by item in `checks.py`, R2a to R2f).
- **Layer 2:** `field_method`: the convertible volume of an on-site fueling programme is built at the duty cycle, the
  stretch between yard visits capped at a tankful, and validated on past programmes before it is carried onto yards whose
  duty mix differs.
- **Decisive step:** build each vehicle's stretches of driving between consecutive yard visits from the telematics days
  and the geofence visits, take for each the smaller of the fuel burned and the tankful above the driver's reserve (the
  fills the 2025 islands put aboard returning sleepers), sum by yard over the recent weeks and replay the window.
- **Not semantics:** every field (the fill's gallons, unit and site, the vehicle day's fuel and positions, the geofence
  entries and exits, the tank spec, the island's gallons) and every filed term (the offer's count, window and price, the
  card schedules' charges, the meaning of "hand out by 8 November") is read the same way by the easy routes; no field,
  code or definition says how much of a vehicle's fuel an island can supply, and the routes that read them all file 29,
  26 to 28 or 19.
- **Not rule application:** the six shipped sentences that bear on how the count is computed (the offer's load, count,
  commitment and price; the yard notes' working week and card use) and the prompt's scenario (our own vehicles running
  as in the eight weeks to 23 August) are executed word for word in `checks.py`: their only literal product, on the
  gallons the files record as bought, is 29, never the golden; no filed
  sentence says when an island can fuel a vehicle or how much it can put aboard (asserted: no tankful, reserve, midday,
  Wednesday, visit or reload wording anywhere in the pack).
- **Analyst test:** a strong analyst who stacks the three card exports, maps cards to units and units to yards, and reads
  the offer and the card schedules correctly forecasts each yard's eight-week card gallons and contracts the loads they
  fill, 29; scaling by the 2025 islands' share files 26 to 28 (pooled, by account or by model, on the eight weeks as
  bought or scaled to the window's working days), by nights at the yard 12;
  capping each vehicle's run between overnight stays at a tankful files 19 (executed on the generator's clean truth in
  `checks.py`, R3a and R3b).
- **Estimand:** the prompt and Overton's offer letter: the number of 8,000-gallon loads to contract for 14 September to 8
  November 2026, each yard taking only the whole loads its island will hand out in those eight weeks to Keeble's own
  vehicles, with the saving those loads book against the same gallons on the vehicles' card accounts at their agreement
  terms; the population (the six yards' vehicles), the scenario (running as in the eight weeks to 23 August, the
  prompt), outcome (gallons handed out), window, unit (whole loads per yard, each load one drop at one yard tank) and
  comparison (the same number of gallons on the cards at their agreement terms: each gallon's card charge over the
  TriState average, the Crossroads network fee part of its diesel price, against Overton's 1.9 cents over the same
  average, the offer's price term) are filed, the method is not.
- **No decoy:** no consultant study, prior programme memo, desk draft or stakeholder figure states or argues a load
  count, a convertible share or an island draw for any yard (asserted: no document states a load count for the window, a
  draw or a capture share); Overton's 2025 letters state their terms and nothing about what the islands handed out.
- **No certified replay:** no certified or published figure for the window ships and nothing graded is reproduced; the
  2025 island transactions are raw records every candidate method is scored on, and they cannot tell the overnight cut
  from the visit cut for a stated structural reason (no 2025 run that outlasted a tankful came back during the day).
- **Lesson:** a channel switch moves only what the new channel can reach: an on-site supply fuels a vehicle only at its
  visits and at most a tankful each time, so the volume a yard tank takes over is built from duty cycles, the stretch
  between visits against the tank, checked on past programmes, and never read off the old channel's purchases or off a
  share measured on another duty mix; no build on file teaches it.

## Readability screen

Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a
predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds it, 6 one
subtraction, ratio or half of a figure). Built figures.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the island takes over what the yard's vehicles buy on the cards (29) | the offer's "loads" and the prompt's "hand out" invite it | card exports carry unit and gallons | yes, the default | the 2025 island record refutes it (the vehicles' card gallons of the eight weeks before each programme overstate the islands by 5.7 and 10.8 per cent) | no | yes, a sum | readable |
| R1 the card gallons scaled by the 2025 islands' share, pooled (0.925), by account or by model (26 to 28) | no | the island transactions carry unit and gallons | yes, the calibration reflex | it is fitted on the 2025 record; Jackson's share (0.969) carried to Knoxville (0.881) misses by 10 per cent | no | yes, one ratio | readable |
| R2 a tankful per run between nights at the yard (19), the card gallons by nights at the yard (12) | no | the vehicle day carries first and last positions | a fleet-savvy physics reflex | the 2025 record ties R2 and R3 (blind to the cut: both reproduce each island within 1 per cent) | no | no | readable |
| R3 (decisive) a tankful above the driver's reserve per stretch between yard visits, overnight or midday (23) | no sentence says when an island can fuel a vehicle or how much it can put aboard | no column carries visits, stretches or capture: the geofence export lists crossings of every geofence (six yards, two lots, ten customer docks), the tank sits on the model's spec row | no: the reflexes are card gallons, a calibrated share, an overnight trip | blind: no 2025 programme vehicle whose run outlasted a tankful came back to its yard during the run; the only midday visits were Jackson's day cabs, whose days never outran their tanks | no: nothing is duplicated, missing or mis-keyed on the call's rows | no: a minimum per stretch built from paired crossings | silent |

## Semantic fork table

Every term in the main ask and every convention the main computation needs. Ids asserted in `generator/checks.py`.

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "load" | 8,000 net gallons at 60 F, one drop at one yard tank (the offer letter) | 8,000 gross gallons at the island meter | same call (gross runs about 0.55 per cent over net; asserted) | same call, asserted |
| SF2 | "hand out by 8 November" | dispensed by the yard's island to the yard's own vehicles, 14 September to 8 November inclusive | delivered into the tank by 8 November, dispensed later | 32 (the offer's ceiling) | the prompt ("only the whole loads its island will hand out ... by 8 November") and the offer (every confirmed load billed whether or not called off) |
| SF3 | "whole loads" | the whole number of 8,000-gallon loads within the yard's draw (floor) | the nearest whole load | 28 | the prompt: a load the island will not have handed out is not wanted |
| SF4 | where the rounding sits | per yard, then summed | the fleet's total draw over 8,000 | 26 | the offer letter: each load is "lifted for and delivered to one yard tank" |
| SF5 | "our own vehicles" | the units on the maintenance system's list at the six yards, as they run now | include any unit of another yard passing through | same call (no unit enters another yard's geofence in 2026; asserted) | same call, asserted |
| SF6 | Cookeville's lot-based vans | Cookeville vehicles (the unit list), fueled at the island when they are in the yard | not Cookeville's (they are based at the Sparta and Crossville lots) | 22 | the unit list's Location (Cookeville) and the yard notes ("based at the Sparta and Crossville lots") |
| SF7 | the window's days | the eight calendar weeks, the yards working Monday to Friday, no holiday inside | 56 days at the base's daily rate including weekends | same call (no vehicle reaches its yard on a weekend; asserted) | same call, asserted |
| SF8 | the base period the duty is read from | the eight weeks to 23 August (29 June to 23 August), scaled by working days | 13 or 25 weeks; by weeks; the holiday week left out; a 2025 seasonal ratio | same call (C3: twelve constructions, each yard 0.15 of a load or more inside its bin; asserted) | the prompt ("if they run as in the eight weeks to 23 August"); same call besides, asserted |
| SF9 | what one island fill can put aboard | every tank less the 10.2 per cent reserve the T680s' own 2025 fills show (48 fills over 225 gallons, all T680s, averaging 269.3 of 300); no other model's fills come back on a reserve | the nominal tank; each 2025 sleeper's own largest fill; the cap each model's own fills show (the Sprinters' largest, 23.9 of 24.5, passes the replay's 22.0; each model's largest fill, or the mean of its fills of three quarters of its tank or more) | same call under each (asserted; the Sprinters at 23.9 put Cookeville at 13,399 gallons, still 1 load) | same call, asserted |
| SF10 | the saving's basis | each account's charge over the TriState average (the Crossroads network fee included, $0.080 a gallon saved) less Overton's 1.9 cents, on the loads' 8,000 gallons | the Crossroads margin without the network fee ($0.065 a gallon, $16,328 in all) | a different saving | Pricing Addendum 4 clause 2 ("is part of the diesel price under this addendum") and the prompt ("at their agreement terms") |
| SF11 | the as-of | 28 August 2026, data through 27 August | (none) | same call | the file list's pull date and the offer's date |
| SF12 | stock already in a tank | each tank at or near its unpumpable bottom (the register's 24 August dips against each tank's own unpumpable, 400 to 750 gallons) | add the usable stock to the draw | same call (at most 201 usable gallons, at Jackson, left from its 2025 programme; asserted) | same call, asserted |
| SF14 | how the tank's heel and overfill alarm enter the count | neither binds: every tank takes a whole load over its unpumpable bottom with 2,000 gallons or more to spare under its alarm, and the loads are counted on the gallons handed out | the old stock handed out first (less the dips' usable gallons); a tank below its bottom topped up from the first load; the heel kept under the last load | same call under each (asserted) | same call, asserted |
| SF15 | "the same number of gallons" on the cards | the loads' 8,000 net gallons each, bought on the cards | the gross gallons the island meter would show (0.55 per cent over net) | a different saving ($19,458; asserted) | the prompt ("the same number of gallons") |
| SF16 | the saving's price basis | Overton's 1.9 cents against each card margin over the same TriState average: $17,408 | the replaced card gallons priced at each account's own site terminals over the eight weeks to 23 August (6 per cent of the SMPM gallons price off Nashville at its Kentucky sites; some Crossroads and Riverbend sites off Knoxville and Nashville) | $17,449 (asserted) | the offer's price term: "The TriState Rack Report contract average for ULSD No. 2 at the supplying terminal on the day of lifting, the same average your three card programmes bill from, plus $0.019 per net gallon, delivered." (asserted in the pack) |
| SF13 | Ask A's months | May, June and July 2026 (the prompt says "last year's" only of the 2025 programmes) | the same months of 2025 | an ask reading, not the call | the prompt's "last year's" marks the only 2025 figures |

## Ladder

Built figures (calc.py on the shipped files, every route asserted in checks.py; each count is MEM, JXN, NSH, CKV, KNX, TRI).

| Rung | Construction | Count | Dies to |
|---|---|---|---|
| R0 default | each yard's card gallons for the trailing eight weeks, filled with whole loads (13 weeks, x 40/39 and the same weeks of 2025 all 29) | 29 (2, 5, 8, 3, 5, 6) | the 2025 island record: the vehicles' card gallons of the eight weeks before each programme overstate what the island handed out, by 5.7 per cent at Jackson and 10.8 at Knoxville |
| R1a | R0 times the 2025 islands' pooled share (0.925); by account (Jackson 0.969 for the West, Knoxville 0.881 for the East) the same; scaled by the window's 40 working days against the base's 39, pooled 28 (2, 5, 8, 3, 4, 6) and by account 27 (2, 5, 8, 3, 4, 5) | 26 (2, 5, 7, 3, 4, 5) as bought; 26 to 28 | leave one yard out: Jackson's share carried to Knoxville misses by 10 per cent; the share is a mixture over duty |
| R1b | R0 times the 2025 share by model (T680 0.830, every other model about 1.0), as bought or scaled | 26 (2, 5, 7, 3, 4, 5) | the model share mixes Knoxville's one-night sleepers (all of their fuel) with the four-night ones (about half) |
| R2a | a tankful per run between nights at the yard | 19 (2, 5, 5, 0, 4, 3) | Nashville's sleepers are in the yard every Wednesday at midday (the geofence export), and an island fuels whatever is in the yard (Jackson's day cabs took 216 midday island fills in 2025) |
| R2b | the card gallons times each vehicle's share of nights at the yard | 12 | a night away is not fuel the yard cannot supply: a full tank at departure carries most of a run |
| R3 decisive | per stretch between yard visits, the smaller of the fuel burned and the tankful above the reserve, summed by yard over the base weeks and scaled to the window | 23 (2, 5, 8, 1, 4, 3) | golden |

**Reflexes swept** (each asserted to miss the total and two yards or more): card fills in the yard's own city 6; the
daily-return vehicles only 7; the mean of R0 and R2a 24 (2, 5, 7, 2, 4, 4).

**Position and margins.** The golden is bracketed: R0 29 and R1 26 to 28 above, R2a 19 below; only the cut at every yard visit
reverses the overnight cut (Nashville 5 to 8, Cookeville 0 to 1). The nearest principled wrong totals are 26 and 19,
three and four loads away; the hedging reflex (24) misses at three yards. Every rung's six counts differ from the
golden's at one yard or more.

**The corridor (C3).** Twelve constructions of the golden, every one landing the six counts (asserted): the raw eight
weeks; the eight full working weeks (the 3 July week left out); 13 weeks scaled by working days or by weeks; 25 weeks
from 2 March; the nominal tank; each 2025 sleeper's own largest fill as its tankful; a midday visit's day split in equal
halves; the 2025 seasonal ratio (window weeks against base weeks of 2025) applied, alone and on the two lowest
constructions; engine fuel calibrated to pump gallons unit by unit. Ranges in loads: Memphis 2.52 to 2.66, Jackson
5.29 to 5.65, Nashville 8.22 to 8.69, Cookeville 1.53 to 1.69, Knoxville 4.43 to 4.76, Blountville 3.32 to 3.83. The
eight-week totals' sampling sigma from the regular weeks (Memphis 41, Jackson 115, Nashville 210, Cookeville 45,
Knoxville 136, Blountville 24 gallons) moves no count. Flip condition: the thinnest margin is Knoxville's, whose count
would become 5 only on a draw 0.30 of a load (2,400 gallons) higher; Nashville's would fall to 7 only on one 0.68 of a load
(5,400 gallons) lower.

**Worth on the graded quantity.** The cap is worth 10 loads (R0 29 to R2a 19: Blountville 3, Cookeville 3, Nashville
3, Knoxville 1); the decisive cut gives back 4 (Nashville 3, Cookeville 1). Without the cut every other correction
lands at 19 or below; without the cap no cut moves R0.

**Strength.** P(one strong solver lands) about 0.15: it must turn down the card gallons and the calibrated share (the
2025 record invites the share), see that a yard can only fuel a vehicle at a visit and only a tankful at a time, and build
the visits from the geofence export rather than the vehicle days' overnight positions the 2025 check was run on. P(both
land) about 0.03 if independent, under 0.1 with any plausible correlation. The seed was fixed by rule (task number,
then the as-of month and day: 1530828) before any data was generated and never searched; every later move was a design
parameter (fleet mix, fuel per day, reorder point), each recorded in `## Tried and rejected`.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the six yards' units on the maintenance list as they run now | filed (prompt "our own vehicles", unit list); C1: no unit enters another yard's geofence (asserted) |
| 2 | Unit of account | whole 8,000-net-gallon loads per yard | filed (prompt, offer) |
| 3 | Attribution window | 14 September to 8 November 2026 | filed (offer); draws accrue by working day, no boundary event |
| 4 | As-of dating | 28 August 2026, data through 27 August | filed (the file list, the offer date) |
| 5 | Version basis | the current unit list and spec sheet | C1: no spec or yard changed in 2026 |
| 6 | Denominator | none on the golden path (sums); R1's share is a wrong rung | named in the ladder |
| 7 | Weighting | none (sums of gallons) | n/a |
| 8 | Window length | the base period the duty is read from | C3: twelve constructions land the same counts (asserted) |
| 9 | Boundary inclusivity | 14 September and 8 November inclusive | filed (offer); C1, no weekend draw (asserted) |
| 10 | Rounding path | floor per yard, then sum | filed (prompt, offer: one drop at one yard tank) |
| 11 | Tie-break | none | n/a |
| 12 | Maturity and censoring | a vehicle out on a run at the base's end | C1: no vehicle runs on the Sundays that bound the base (asserted) |
| 13 | Order of operations | the minimum per stretch before the sum | the decisive step; sum then cap is R0 or R2, separated |
| 14 | Row order | sums | C1 |
| 15 | Duplicate resolution | the geofence export's paired entry and exit crossings | C1: no unpaired crossing (asserted) |
| 16 | Identity normalisation | device serials to units through the dated assignment table | C1: every swap and its serial-named days fall in March and April, before the base (asserted); dropping them moves nothing (R2a) |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | US gallons throughout the call's rows; loads in net gallons | SF1 same call (asserted) |
| 19 | Code and status semantics | unit status (active, spare, sold) | C1: the two spare trucks have no vehicle days, and the five units sold in the autumn of 2024 none after their disposal dates and no yard visit in 2026 (asserted) |
| 20 | Integerisation | floor per yard | filed; each yard's draw 0.25 of a load or more inside its bin (asserted) |
| 21 | Clause scope | "every confirmed load is billed" | applies to the count only; n/a for the draw |
| 22 | Forward window contents | each vehicle's current duty, run as in the eight weeks to 23 August | filed (the prompt's "if they run as in the eight weeks to 23 August"); the base's regular weeks within 3.3 per cent of each other at every yard (asserted) |

## Literal reader

Executing the prompt and Overton's offer word for word gives, for each yard, the whole 8,000-gallon loads its island
will hand out to Keeble's own vehicles from 14 September to 8 November with the vehicles running as in the eight weeks to
23 August, summed over the six yards; no shipped sentence
says when an island can fuel a vehicle or how much one fill can put aboard, so a literal reader must estimate the draw;
the easy method on the same literal estimand (the island taking over what the vehicles buy on the cards) files 29, and
the fork table leaves no reading under which 29, 26 to 28 or 19 is the golden.

## Oracles

- The 2025 Jackson and Knoxville island transactions: on the wrong path they refute the card gallons (5.7 and 10.8 per
  cent over) and suggest a share to carry, which misses the window's yards; they tie R2 and R3 because no 2025
  programme vehicle whose run outlasted a tankful came back to its yard during the run (the midday visits were Jackson's
  day cabs, whose days never outran their tanks), so they are blind to the decisive cut for that structural reason (L1).
  They carry no figure for any yard of the window.
- Overton's 2025 programme letters (the terms): consistent with every method; no window figure.
- The tank register (six tanks of 12,000 to 25,000 gallons, standby status, dips at the unpumpable bottom): no draw.
- No control ties only under the golden.

## Ask sheet

**Main call's declared row population:** the telematics vehicle days, the geofence export, the maintenance system's
unit list and spec sheet, the device-assignment table, the 2025 island transactions, the offer letter, the card
schedules' price terms and the yard notes. Device and hazard rows in it: 0 (asserted: the golden reads no card export,
no Overton file and no rack). The asks read files the call never reads (the three card exports, Overton's 2025 delivery
tickets, invoices and credits, its rack history) and use the vehicle days only as a referee. Neither ask is keyed to the
call or its construction, and they share no primary device or path.

**Ask A. The diesel gallons each card account's vehicles bought in each of May, June and July 2026** (9 figures,
gallons to the nearest gallon). Golden: Delta's Riverbend account 33,472, 36,732 and 37,170; Keeble's Crossroads 46,569,
54,781 and 52,821; Holston's SMPM 46,391, 51,215 and 53,258 (each the world's diesel bought by the local day it was
pumped, asserted).
- H18 home: a reconciliation: the three exports put on one calendar, the card side of the comparison the chart sets
  each island against. The call never reads a card fill.
- Construction: every diesel sale (DEF excluded) on the local day it was pumped: Riverbend's UTC stamps put on Central
  time (Schedule A, A5); a Crossroads or SMPM sale made at 10 pm or later carries the next day's date (Addendum 4 clause
  5, on Central time; the SMPM layout, positions 15-22), so it goes back a day; a posting a site sent twice and the
  credit that reverses it are no purchase (A6; clause 6; the layout's C record); summed by account and month. Each
  convention is filed in the programme's own document and executed, never a device.
- Primary A3 (D8 amendments dated when processed, on D1 a replay under fresh ids): on six days a site sent its day's
  sales twice (Riverbend's Jackson sites 112 on 30 April and 115 on 30 June, the Crossroads merchants at Hopkinsville
  on 29 May and Dalton on 30 June, the SMPM sites at Strawberry Plains on 29 May and Beckley on 30 June). Each copy is a
  full posting under a fresh transaction number beside genuine same-day fills, and its credit comes in a later week,
  dated the day it was processed (5 May and 7 July; 2 June and 2 July; 9 June and 14 July). Summing every line where the
  programme books it puts a duplicate day's gallons in one month and their credit in the next, and misses all nine;
  dropping only the credits keeps the copies and misses the five account-months with a duplicate day. Fair: each credit
  carries the number or reference of the posting it reverses, and the copy matches its original field for field.
- Fair checks on the filed conventions: put on Central time every Riverbend price is the TriState average for that day
  plus $0.119, and read as local 8,697 of 16,958 fills fall an hour or more after the vehicle's last ignition off that
  day; every Crossroads and SMPM sale stamped 10 pm or later with a readable odometer (2,134 of 2,233) shows one at or
  below the starting odometer of the vehicle day on its recorded date; dated by an Eastern merchant's own clock the
  1,723 Crossroads sales at its four Eastern-time merchants give the same nine figures (asserted).
- Hazards: HA1 DEF on the same cards (every account-month by 922 to 1,684 gallons); HA2 the SMPM batch for 6 to 12 July
  transmitted twice under two batch numbers (Holston's July by 12,808 gallons); HA3 the SMPM file's gallons with three
  implied decimals (the layout PDF).
- Stops (built; deltas by account, May, June, July): S1 every line on the date the files give it, the natural read
  (Riverbend -246, +230, -230; Crossroads +718, +8, -354; SMPM +948, -358, +55: 9 miss); S2 the dates as filed, the
  copies and credits handled (+172, -165, +165; +373, -261, +260; +646, -437, +437: 9 miss); S3 every filed date
  convention applied, each credit on its own date (-508, +469, -470; +345, +269, -614; +303, +79, -382: 9 miss); S4 the
  credits dropped, the copies kept (0, +469, 0; +345, +614, 0; +303, +381, 0: 5 miss); S5 UTC corrected, the 10 pm dates
  kept (6 miss); S6 the 10 pm dates corrected, UTC read as local (3 miss); S7 DEF in (9 miss); S8 the golden.
- Span: the three exports, the SMPM layout, the card schedules, the vehicle days, the unit list (card to unit, for the
  referee) and the rack history (the Riverbend price check): 8 files; date, time, card, unit, product, gallons,
  odometer, site, credit reference, first ignition, last ignition off and starting odometer (12 columns).
- Realism: a chain's head-office system logs UTC and its schedule says so; a network closes its business day at 10 pm
  on its home clock and its addendum says so; a site whose day's upload times out sends it again and the programme
  credits the copy on a later invoice; a marketers' group re-sends a week whose acknowledgement times out.

**Ask B. For each month of the 2025 Jackson (March, April, May) and Knoxville (June, July, August) island programmes,
the net gallons Overton delivered and the dollars it billed over the posted rack value of those gallons after credits,
taxes aside** (12 figures; gallons to the nearest gallon, dollars to the nearest dollar). Golden: Jackson 31,911
gallons and $891, 24,004 and $811, 7,986 and $254; Knoxville 23,977 and $446, 24,021 and $542, 8,021 and $191.
- H18 home: the audit trail of the two programmes whose island record the count's method is checked on: what the loads
  cost over the rack against the 1.9 cents now offered.
- Construction: each load (terminal bill of lading) once, in the month it was delivered (one invoice per bill, dated the
  day of delivery, the letters); the dollars billed: the invoices' product and delivery service lines, the two July
  invoices credited in full and their rebills in their place, taxes aside; less each load's net gallons at Overton's
  posting in effect when it was lifted (the letters: posted at 6 pm Central with the next day's date; the delivery
  export's clock is Central, its own headers). Each convention is filed and executed, never a device.
- Primary B1 (D6, grain unstated): a load the tank could not take whole was dropped in two visits under one terminal bill;
  Overton's delivery export carries one row per drop under its own ticket number, each with the bill's net gallons and
  the drop's own gross; every programme month has one such load or more (none across a month end). Summing the net column
  over the rows misses all six gallon figures, and pricing each row at the rack misses all six dollar figures. Fair: the
  invoices bill each terminal bill once.
- Hazards: HB1 the two July Knoxville loads invoiced with a freight-zone charge in error, credited in full on 21 July
  and rebilled (original, credit and rebill in two files; the credits unread add $38,499 to Knoxville July, the credited
  loads dropped with their rebills take $414 off it); HB2 the split-drop and gate wait-time service lines (left out,
  every month's dollars fall by $62 to $235); HB3 the tax lines (Class TAX); HB4 the load lifted on 30 June and
  delivered on 1 July (dated by lifting, it moves 8,030 gallons and $286 from July to June).
- Stops (built): S1 net per row, rack per row (12 miss); S2 per bill, the posting dated the lifting day (5 dollar
  figures miss); S3 per bill, the posting dated the delivery day (5 miss); S4 the credits unread (Knoxville July); S5 the
  credited loads dropped with their rebills (Knoxville July); S6 the service lines left out (6 miss); S7 loads dated by
  lifting (June and July); S8 the golden. Dated by invoice instead of delivery, the same twelve (asserted).
- Span: the delivery export, the invoice export, the credits file, the rack history, the two 2025 letters and the
  file list (6 files); terminal bill, ticket, net, gross, lifted, delivered, invoice, class, item, amount, effective date,
  posting (12 columns).
- Realism: a terminal bill of lading carries the load's total on every drop made against it; jobbers lift in the
  afternoon and at night for the morning; racks post at 6 pm for the next day; a jobber credits and rebills a mis-zoned
  invoice in full.

**The chart** (`yard_island_draw.png`) is the call's own figure: each yard's island draw for the contract weeks beside
the diesel its vehicles bought on the cards in the eight weeks to 23 August (both windows in the prompt), the loads
marked; it is graded on its parts and its loads, which are the call's. Its card bars sit on no device: no fill falls on
the Sundays that bound the eight weeks, and the one duplicate day inside them (30 June) is credited inside them too.

**Hazard table.**

| Hazard | Asks moved | Per-ask delta (built) |
|---|---|---|
| Time stamps on a stated clock (Riverbend's UTC; Crossroads' and SMPM's 10 pm business day; Overton's 6 pm posting) | A, B | A: Riverbend's three months by 165 to 172 gallons, Crossroads' and SMPM's by 260 to 646; B: five months' dollars each way |
| Lines that are not diesel or not over the rack (DEF on the cards; taxes and service lines on the invoices) | A, B | A: every account-month by 922 to 1,684 gallons; B: every month by $62 to $235 |
| Documents sent twice (the six duplicate days and their credits; the SMPM July week; Overton's July rebill) | A, B | A: up to 948 gallons an account-month, Holston July by 12,808 gallons; B: Knoxville July by $38,499 |

**Referee.** The vehicle days (Ask A) and the invoices (Ask B), each byte-clean; neither hands over a level.

**Cracker sheet** (the cracker landed the call, ran the hygiene battery, executed every filed rule and matched every
control):

| Ask figures | The cracker's route | Device that holds | Verdict |
|---|---|---|---|
| A, Delta's Riverbend account, May to July (3) | UTC put on Central time (A5), every line summed where the programme books it | A3 the 30 April copy's credit on 5 May, the 30 June copy in June and its credit on 7 July | miss |
| A, Keeble's Crossroads account, May to July (3) | the 10 pm sales moved back a day (clause 5), every line summed | A3 the 29 May copy in May and its reversal on 2 June, the 30 June copy and its reversal on 2 July | miss |
| A, Holston's SMPM account, May to July (3) | reads the layout, drops the re-sent week, moves the 10 pm sales back, signs the C records | A3 the 29 May and 30 June copies, credited on 9 June and 14 July | miss |
| B, net gallons by month (6) | ticket-level delivery rows, key unique | B1 a split load's net on each drop | miss |
| B, dollars over the rack by month (6) | rows priced at the posting in effect at lifting (6 pm rule executed) | B1 a split load's rack value taken twice | miss |

**Mirror sheet.** The mirror stops at R1 (26 to 28 loads) and meets the same devices; it keeps the chart's parts that do
not carry the call, the yard counts R1 shares with the golden (Memphis, Jackson, Knoxville) and nothing in A or B unless
it cracks a device.

Mirror leakage: 15 per cent of ask weight (the chart's card-gallon bars and a share of the B figures if it finds the
repeated bills, no A figure).

Pair ceiling: 39.5 (the cracker at 38 + 7 + about 14 of 55 ask points: the chart's parts and, if it finds the repeated
bills, the six B gallon figures; the mirror at about 5 + 7 + 8, its three matching yard counts included). The filed
conventions cost the asks the A1 and A2 stops a strong response used to miss; A3 and B1 hold them, rerun from the
generated rubric at stage 4.

## Leak review

`leak.py --asof 2026-08-28` (rerun after the stage 4 fix): REVIEW, no LEAK. Each REVIEW line:
- `fms_island_transactions_2025.csv` "golden figure 37,170": a substring match on an island fill of 170.1 gallons;
  harmless.
- `overton_offer_2026-08-26.pdf` carries the call's words (Overton, loads, the window, the yard names): the
  counterparty's own offer naming its terms; it states no count but the 32 offered and no saving, only its own price
  term on the TriState average; harmless.
- Design-note vocabulary in the card schedules, the file list, the 2025 Jackson letter, the SMPM layout, the yard notes
  and the prompt (vehicle, islands, telematics, geofence, programme, carries, supply): the fiction's own nouns ("each
  posting carries the next day's date", "keep the Jackson yard tank supplied"); no sentence names the move (asserted in
  checks.py: no tankful, reserve, midday, Wednesday, visit, reload or once-a-week wording in the pack); harmless, for the
  stage 4 reader to confirm.
- The stage 4 reader's findings are fixed in the generator: the Crossroads network fee is part of its diesel price
  (Addendum 4 clause 2; $0.080 against $0.065 asserted, SF10); the offer's saving sentence is gone (the offer states its
  price term, the saving is Keeble's computation from the card schedules, SF16); the tank register and the unit list
  are no longer uniform; the heel and the alarm are asserted not to bind under any of three readings (SF14); and the
  yard notes no longer close the forward window (the prompt carries the scenario).

## Pre-ship check

- **The 10/10 rules against the built pack.** The decisive step is still analytical: the prompt and the offer file
  the estimand (the loads each island hands out by 8 November, the vehicles running as in the eight weeks to 23 August,
  whole loads per yard, the saving on the same TriState average) and no shipped sentence says when an island can fuel
  a vehicle or how much one fill puts aboard; the six filed sentences executed alone give 29 (HOW); the card gallons
  file 29 on the clean truth too (R3a); only the stretch between yard visits capped at a tankful lands, in every one of
  the twelve constructions of the corridor and under every cap the models' own fills show (SF9). Layer 1 (three card
  layouts and clocks, the duplicate postings and their credits, device serials, UTC geofences, the resent island
  batch, the split drops, the 6 pm posting, the tanks by model) is neutral: each mishandled reading leaves the call
  (R2a to R2f), and the card exports are not on the golden's path.
- **Free gates on the final rebuild.** `checks.py` 107 assertions, 0 failed; `verify.py` agrees on its own path; two
  builds byte-identical, target.zip sha256 1808f2c1, the stage 4 fix's cut; `figures_check.py` 52 figures, 0 absent;
  `freeze.py` (determinism) moves only block 1's four rival figures (29, 26, 28, 19) and their figures.json keys,
  taken out on the round 2 notes, the one move it reports;
  `precut.py` exit 0; `voice-check.py` PASS (982 characters); container audit clean on the pack and the goldens;
  `guard.py` check WARN (three_rules.strategy_risk, repeat.gate_g), validate clean, heart WARN, surface three promoted
  pairs on the differentiated card signature (task94, task69, task105).
- **Stage 4.** Judge round 1 NOT_DETERMINISTIC, FIX_NOW on asks 4 and 5 (`determinism_check_report_round1.md`), fixed
  in one generator pass with the reader's findings; judge round 2 DETERMINISTIC, APPROVE (`determinism_check_report.md`),
  every figure reproduced; its notes answered in the write-up and the checks: step 3 names the cap the T680s' own fills
  show (SF9), the saving's basis is the offer's price term (SF16, the by-site $17,449 excluded), and the rival figures
  are out of the graded blocks; the leak reader clean on the fresh read of the round 2 pack.
- **Personas in the pack.** Theresa Mercado, Gabriel Wyatt and Dennis Stewart (drawn with `guard.py names`), all on the
  card.

## Build record

- Generator: `world.py` (the fleet, its duty, legs, fills, the 2025 programmes, the tanks), `records.py`, `docs.py`,
  `calc.py`, `asks.py`, `deliver.py`, `metadata.py`, `postprocess.py`, `checks.py` (107 assertions: the three-rules
  block, the HOW sentences and the prompt's scenario, the ladder, the corridor, SF1 to SF16, the closure axes, the 2025
  out-of-sample record, both asks with their filed conventions, stops and fairness, the cracker, the separation line,
  the realism sweep, the input gates and the distractors' deletion), `verify.py` (its own path), `build.py` (two
  byte-identical builds, the zip).
- Pack: 22 files in five formats (csv, xlsx, pdf, txt, md); the largest 79,042 rows; distractors the tank wagon prices
  and the IFTA returns, named in `metadata.json`.

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
- Sleepers at 118 to 130 gallons a day (740 to 820 miles a day, beyond one driver's hours) to keep the card gallons far
  above the draw: rejected at stage 3 for realism; the East's sleepers now run the Appalachian routes at about 5 mpg and
  112 gallons a day, Jackson's at 92, and the default fell from 30 to 29.
- Nashville's holiday weeks without the midweek reload: dropped at stage 3; the 3 July week's one capped run put
  Nashville's 13-week construction with the season 0.02 of a load from its bin edge, so the reload now follows the
  week's run.
- A dispatcher reading the tank at 5 pm with an 11,700-gallon reorder point and the remainder of a split load dropped
  piecemeal: rejected at stage 3; loads went in three drops and a tank ran dry before the programme ended. The dispatcher
  now reads at 3 pm, sends a load only while the programme still needs one, and the island runs the last load down.
- The Jackson programme ending 16 May: its last load came in late April and May had no delivery to ask about; the letter
  now runs to 29 May.
- Every load lifted in the evening: the posting dated the delivery day was always the one in effect, so B2 caught only a
  lifting-date join; liftings now run from mid-afternoon, and each naive join misses five months.
- A $65 split-drop charge: one month's dollars sat a tenth of a cent from its rounding edge; $62.50 puts every month 13
  cents or more inside.
- Jackson's day cabs at 83 gallons a day: Jackson's draw fell to 5.14 loads on the lowest construction (13 weeks by weeks
  with the season), 0.14 from its edge; at 86.5 the corridor is 5.29 to 5.65.
- A pack file named `README.md`: the surface screen promoted task152 on the shared name; renamed to the fleet's own
  `fuel_review_files_2026-08-28.md`.
- A yard-notes sentence pointing to the tank sizes ("Tank sizes are on the model rows of the unit list"): cut at stage 3
  as a pointer toward the cap.
- Real hospitals, schools, a resort and two fuel brands named in the geofence and station lists: replaced with fictional
  customer docks and station names at stage 3.
- Ask A's date conventions left unstated as its primary devices (Riverbend's UTC stamps, the cards' 10 pm business
  day): the stage 4 judge read the file dates as a defensible second answer; both are now stated in the programmes' own
  documents (Schedule A, A5; Addendum 4, clause 5 with its Central clock; the SMPM layout), and Ask A's silent device is
  a day a site posted twice, its credit dated in a later week.
- The cards' 10 pm rule as "after 10:00 pm": 25 sales stamped 22:00 had two readings; the addendum and the layout now
  say "at 10:00 pm or later".
- Ask B's posting rule left to the invoices (the rack file carries only an effective date): the judge read the posting
  dated the lifting day; the 2025 letters now state the 6 pm Central posting with the next day's date, the delivery
  export labels its clock, and the prompt defines the dollars as everything billed over the posted rack value of the
  gallons after credits, taxes aside.
- The offer's saving sentence ("every gallon taken on this offer saves the card programme's charge over the average
  less our 1.9 cents"): the leak reader read it as the vendor handing over the saving's method; the offer now states only
  its price term on the same TriState average the cards bill from.
- Six identical 20,000-gallon tanks and a unit list with every unit active under one model string per model: too tidy
  for the leak reader; the tanks run 12,000 to 25,000 gallons, five units sold in 2024 stay on the list with their
  disposal dates, each branch writes model names its own way, and in-service dates fall on working days before each
  unit's first vehicle day.
- The yard-notes sentence "No route, fleet or yard changes are planned before December": read by the leak reader as
  the author closing the forward window; removed, and the prompt carries the scenario instead ("if they run as in the
  eight weeks to 23 August").
- "Monte Carlo" in the submission's domain tag: the surface screen read it as a persona (task147); the tag names
  resampling and simulation methods.
- The rejected routes' load counts in the Final Recommendation (29, 26 to 28, 19): figures no graded block carries
  and the round 2 judge did not reproduce; the rivals are named without them, as in task151 and task152.
- Step 3's "each vehicle's fill is capped at its tank less 10.2%": read by the round 2 judge as a claim about every
  model's fills, when only the T680s' fills show that cap (two Sprinter fills pass it); the step now names the cap the
  T680s' own fills show and the replay applying it to every tank, and SF9 asserts every model-by-model cap.
