# task308: which district gets the 600 e-bikes, and the net fare revenue a year they add

Architecture 1, drawn 2026-10-25 (wave 7, Opportunity Sizing & Decision Support, perssathya; the author allowed a third
build in flight). Seed OS10's world, decision and quantity are kept (a city bike-share operator, 600 e-bikes for one of
five districts, the net fare revenue a year they add); the seed's mechanism rows are decoy-era design and were not
used, and the pitfall was re-found from the data.

## Draw

| Field | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task308.json`, architecture v1 |
| Pairing | Product Analytics / churn-propensity-uplift-modeling / Opportunity Sizing & Decision Support |
| Niche | which district of a city bike-share gets 600 new e-bikes and the net fare revenue a year they add, when the busiest district's docks rarely run dry and another district's run dry at every term-weekday class change |
| Call | the district that gets the e-bikes, and the net fare revenue a year they add there, to the nearest USD 10,000 |
| Decision | `pick_one_of_n`, answer unit `named_option` (with its USD figure) |
| Mechanism | gap population then objective; pattern none; generators G7 (decisive: the windows in which a dock held no bike, pinned only by the operations records of stock moving in and out), G12 (a step with no trip at an empty dock is a non-answer, not zero demand) |
| Gate G | `method_or_model_selection`: which requests count as the e-bikes' added trips |
| Strategy | `informative_censoring`; layer 2 family `estimation_fit`, own pattern: served trips censored by empty docks |
| Calibration | `parallel_run_overlap` (the 2025 pilot: e-bike docks beside matched classic-only docks for the whole year) |
| Furniture | forum `board_of_directors`, forcing event `season_or_peak` (the e-bikes must be on the street for the 2027 riding season), organisation `software_or_platform` (the bike-share operator), role `product_manager`, context artifact `monitoring_export` (the nightly dock count) |
| People | Joseph Graham (e-bike product lead, the requester), Gina Wells (operations director, who would put the e-bikes where the riders are); drawn with `guard.py names --geo usa --seed 308` |

**Data-native sentence.** A bike-share trip exists only when a rider meets a dock holding a bike, so the trip record is
demand censored by each dock's stock; University's dorm docks are drained by the morning class change and are not
restocked until the 14:00 van, so its noon class-change requests leave no row, while Central's four daily van runs keep
its docks stocked and its record close to its demand.

**Guard.** `guard.py check` on the card: WARN, no BLOCK. `repeat.gate_g` (method_or_model_selection, as task485 and
task269): the honest key, since the decisive step chooses which requests the e-bikes add. `repeat.decision`
(pick_one_of_n, as task303) and `repeat.question_form` (which): the seed's decision is a pick of one district.
`test.same_driver_older` against task271 v2 and task471 v1 (both lineage), and the signature lines against task199,
task268 v2, task196 v2, task255 v1 and task305, each differentiated on the card. The axes redrawn and why: the forcing
event `launch_or_rollout` and the calibration form `pilot_log` were barred against the live window; `season_or_peak`
is the honester label anyway (the deadline is the riding season), and `parallel_run_overlap` names what the pilot is
(e-bike docks run beside matched docks over the same year). Nearest driver 0.06.

**Abstraction test.** Stripped of nouns: a launch's added revenue is sized from the existing product's requests, the
record holds only the requests the existing supply met, and the candidate whose supply runs out at every peak hides the
most requests. Against task302 (lost sales while a product is unavailable, net of what goes to a substitute): there the
record overstates the loss; here it understates the demand, and no substitute exists, since the neighbouring dorm docks
run dry together. Against task305 (occupants counted at homes outside the area): there a population sits outside the
record's base; here every rider is in the base and only the requests made at an empty dock are missing.

**Call-only probes (2026-10-25, the draw pack at scratchpad `t308/probe`).** Both isolated probes (sonnet and opus at
medium, prompt and pack only) named Central: sonnet at USD 270,000, opus at USD 100,000. Both rebuilt the pilot's
e-bike stock and found the choice share when an e-bike is docked (0.42); neither rebuilt the districts' classic stock.
Both flagged that Central's docks cannot hold 600 more bikes, and opus that the pilot's e-bikes were ridden to the
matched docks (the comparison was not clean): both are world defects fixed at the build (new dock points come with the
e-bikes; e-bikes dock only at charging docks).

**Sources, one line each.**
- `layer2-rigor-patterns.md`, churn-propensity-uplift-modeling #1 and #4 (target persuadables; rank by effect, not by
  treated response): the board's net fare revenue is an uplift, and the district with the most riders is where the
  e-bikes mostly convert riders who ride anyway; this build's step is the censoring that hides the persuadables.
- task302 (stockout diversion) and task305 (an omitted population), differentiated above.

## Default path

1. Read the pilot note, the trips, the docks and the board extract. Rebuild the pilot's e-bike stock: when an e-bike is
   docked, 42 per cent of the pilot docks' trips take it.
2. Pilot docks carry about 8 per cent more trips a day than the matched docks: new riders drawn by the e-bikes.
3. Net per trip: a switched rider pays the e-bike fare instead of the classic fare (about USD 0.46 more), a new rider
   pays the full e-bike fare.
4. Carry that mix to each district's 2025 trips; the district with the most trips gains most.
Ends on: Central, about USD 100,000 a year.
Golden: University, about USD 200,000 a year (to be fixed by the generator's golden construction at stage 3).

## Stump sentence

A competent analyst carries the pilot's e-bike choice share and new-rider uplift to each district's recorded trips and
names Central at about USD 100,000 a year, because the trip record holds only the requests that found a bike:
University's dorm docks run dry at every term-weekday class change and stay empty until the afternoon van, so its
turned-away requests leave no row, and the requests rebuilt for its empty minutes (from each dock's stock, rebuilt from
the nightly count, every trip and every van move, and its requests per stocked minute) put University first at about
USD 200,000 a year.

## Three rules

Task type: churn-propensity-uplift-modeling (product-analytics), which serves Opportunity Sizing: the call sizes the incremental fare revenue a product launch adds against the existing product, from a pilot's uplift carried to each candidate's demand.
Domain test: the deciding quantity is a launch's uplift against the existing product (the e-bike trips that are new, against the ones that only convert a classic trip), measured as product analysts measure it in shared mobility, from trip logs whose usage is censored by availability: a docked-bike service records a request only when the dock holds a bike, so demand is rebuilt from each dock's stock and its requests while stocked.
Swap: "University gets the e-bikes because its dorm docks turn away the class-change requests the trip log never shows" with hospital beds and admissions in place of docks and trips reads as a capacity question with no launch, no product being converted against another and no stock moving between stations through the day; with a retailer it loses the dock-by-dock flows that empty one station while filling another, which is what hides the requests here.
Layer 1: minute-stamped trip records across a year (the operator's trip system), van rebalancing moves (the operations dispatch system), the nightly dock count (the fleet audit), open data by district, month and rider type with cells under 10,000 trips suppressed (the city's open-data portal), dock capacities and elevations (the asset register); nothing placed to be caught.
Layer 2: estimation_fit, censoring: the requests a district would make of the e-bikes are its recorded trips plus the requests its empty docks turned away, and the turned-away requests are estimated from each dock's rebuilt stock and its requests in the minutes it was stocked.
Decisive step: treat each district's recorded trips as demand censored by dock stock, rebuild every dock's stock through the day from the nightly count, trips and van moves, and add the requests its empty minutes turned away before carrying the pilot's uplift.
Not semantics: every field can be read correctly (what a trip is, what a van move is, what the count counts) and the analyst still takes the district's trips as its demand, because no field, flag or document says a request was turned away; only the rebuilt stock shows the empty minutes.
Not rule application: no filed rule says how to count requests; the board extract files the estimand (the e-bike trips' fares less the classic fares their riders would otherwise have paid, in a year at 2025 demand) and the deployment, and nothing names censoring, stock or empty docks. Enumerated family on the pick: recorded trips, recorded fares, trips per dock, the pilot's uplift per dock or per e-bike, and the censoring-aware request count; the first five name Central or Riverside, the last names University, so the standing family (the constructions that count turned-away requests) is unanimous on the pick, and its spread on the graded figure is measured at stage 2 (a censored-demand fit by dock, hour and day type against coarser strata). The ruling-out is quiet: no column or clause eliminates the recorded-trips route; only the rebuilt stock does.
Analyst test: the easy route, the pilot's choice share and new-rider uplift carried to each district's recorded trips, names Central at about USD 100,000 a year (the default path's Ends on), against University.
Estimand: the board paper extract: the net fare revenue the 600 e-bikes add in a year in the chosen district, the fares of the e-bike trips less the classic fares of the trips those riders would otherwise have taken, at 2025 demand, with the e-bikes spread over the district's docks on new dock points and restocked every night.
No decoy: nothing is planted; the operations director's view (put the e-bikes where the riders are) is the natural framing, stated once in the board extract with no figure, and no document ranks the districts.
No certified replay: no certified or published figure is shipped for a method to be recovered from; the open data's district totals are counts of recorded trips, the same quantity the trip log gives.
Lesson: usage records of a capacity-limited service are demand censored by the capacity, so sizing a launch on recorded usage sends it where supply already meets demand; a model learns to rebuild the supply from the flows and count the requests the empty moments hid, which no build on file teaches for station-based stock.

## Tried and rejected

- 2026-10-25, before the pack: the seed's own step (cannibalisation measured on flat streets carried to a hilly
  district) is a visible-state stratification on elevation, which the probes on this lane land by reflex; a
  dock-level pilot comparison missing members who switched docks is a contaminated comparison, found by both probes on
  task304; battery swaps capping a hilly district's trips are handed over by battery columns. Set aside on paper.
