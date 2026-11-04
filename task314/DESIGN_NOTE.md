# task314 design note

Architecture 1, drawn 2026-11-04. Opportunity Sizing & Decision Support, Economics & Econometrics,
elasticity-welfare-policy-impact-estimation. A small Mountain West city's water department chooses which
Stage 2 drought rate option in its drought plan goes to council for summer 2027, each sized as the
single-family use billed June to September that it takes out.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task314.json`, architecture v1, registered 2026-11-04T15:17:49Z
  and re-checked as filed: WARN only (repeat.gate_g against task285, repeat.question_form against task285 and
  task489), the older same-puzzle and same-driver notes differentiated on the card against task118 (v4, and v2 in
  lineage), task184 (v1 in lineage), task198 (v4), task307 (v2 in lineage) and task472 (v1 in lineage). Nearest
  driver 0.09 (task134 v3).
- **WARNs answered.** Gate G `method_or_model_selection` is the honest mechanism: two defensible price models
  (the marginal block price the block-rate demand model uses, the whole bill's average price) and the city's own
  rate history pins the right one; task285's model choice is a network reachability reading, a different thing.
  The question form `which` is the decision's own form, a pick of one option; it is under its corpus quota.
- **Seed and why its world was left.** OS16 (a workforce board's USD 2M fund for one intervention, scored on
  additional participants employed in the second quarter after exit), read through `status.py task314` only. Its
  pairing (policy-education x Opportunity Sizing) has no task type serving the objective. Re-homed to Economics &
  Econometrics / elasticity-welfare-policy-impact-estimation, the randomised-pilot world's decisive steps are spent
  or barred on file: binding seats (`ban.strategy` binding_constraint against task210), at-scale interference
  (task139, task131, task249), transport by composition (task309's approved abstraction, task177 v2), harvesting
  and pull-forward (task122, task136), delayed entry (task272, task183, task133), length bias (task120, task130,
  task135, task182), and the workforce-board world itself is carried by task477. The number moved to a city water
  department's 2027 drought rates in the same client domain and task type, keeping the seed's decision shape: which
  one option a fixed public decision buys, sized on the extra outcome it delivers.
- **Pairing:** Economics & Econometrics (client domain) / elasticity-welfare-policy-impact-estimation (serves
  Opportunity Sizing only) / Opportunity Sizing & Decision Support. The pool is the single-family class's June to
  September billed use (about 1,216 acre-feet a summer on the prototype); the realisable is what each option takes
  out of it; the call is the option that takes out the most, set against the drought plan's Stage 2 target for the
  class.
- **Shape 07 (a grid):** each option's saving on each of the four summer bills (12 cells), each option's summer
  total and its share of the class target, the call, the runner-up and the gap, the chart's named parts and the
  files; the asks add their own rows (Ask sheet).
- **Mechanism:** stump strategy `forecast_method_backtest` (the natural price model, the marginal block price, is
  wrong out of sample on the one option it gives no effect, and the city's own rate history selects the price
  customers answer; no back-test is filed); gap objective (the block price is a correct record and is not what the
  response is scored on); pattern none with G1 decisive (the unit of value, the price the household answers) and
  G16 behind it; Gate G `method_or_model_selection`; Layer 2 family `estimand_identification`, own pattern
  `the-price-block-rate-customers-answer-read-off-a-fixed-charge-on-one-area`.
- **World:** the City of Ardley Springs (about 19,000 people, an unnamed Mountain West state), its Water Department,
  about 6,200 single-family accounts, the Fenwick Mesa area annexed in 2021 from the old Fenwick Mesa Water Company
  and billed a capital recovery charge from the July 2024 bills to repay the annexation bonds, the Upper Brennan Basin
  Water Conservancy District that wholesales the city's summer supply and has noticed a dry-year cut to its 2027
  delivery. Furniture: forum `council_or_assembly` (the council's December 2026 rate hearing), forcing event
  `vote_or_meeting`, organisation `local_government`, role `finance_controller` (the department's rates and finance
  manager), context artifact `filed_standard` (the drought contingency plan).
- **People** (`guard.py names --geo "United States" --seed 314`, none warning): Tami Weaver (rates and finance
  manager), Jason Morgan (utilities director), Clifford Haley (water resources manager, the drought plan's author),
  Beth Sheppard (city clerk).
- **Data-native sentence.** Every bill the city sends shows a month's water as one total, and the only rate change
  in the record that moved bills without moving any block price, the Fenwick Mesa capital recovery charge, is also
  the one that moved use while the 2023 redesign's block jumps barely did, so the city's customers answer what the
  whole bill comes to per thousand gallons, fixed charges included.
- **Abstraction sentence** (the one a reviewer holding this build beside its nearest approved build would say is
  shared): a unit's response is to the total charge divided by what it bought rather than to the charge on its last
  unit, which shows only where a past change moved the total without moving the last unit's charge, so ranking
  options by the last unit's charge gives a charge that leaves every step alone no effect. It cannot be written
  against any approved build: task309 carries an effect that varies with an intensity class, task120 a storage
  mass balance, task303 a shared upstream event, task128 a capacity natural experiment, task105 and task106 a
  catchment and a shared pool; none turns on which of two correct prices a unit answers.
- **Mechanisms on file** (`guard.py mechanisms --objective opportunity-sizing-decision`, one line each): task105
  nearest-open-branch catchment; task106 a shared pool of spare legs; task116 a contract keyed to one member;
  task120 production less storage gain; task127 a fused wait; task128 a call's effect where the queue outran the
  team; task301 attrition carried from recent lists to old; task302 substitution inside a group; task303 a shared
  upstream loss in the same minute; task304 a forward yield that is not the pilot's; task305 a forced choice read
  from members already forced; task306 old units still to arrive; task307 wear inside one duty band; task308 a
  common-mode outage; task309 an effect by intensity class; task310 output held at a send-out limit; task311
  variance components; task313 an intervention acting only after a variable hand-off; task464 quadratic branch
  losses; task118 a welfare wedge on the quantity reached in the appraisal year. None is a price-concept step.
- **`slots` screens** (mechanism and setting nouns, before the first harness): average price, marginal price,
  perceived, ironing, schmeduling, fixed charge, surcharge, inclining, block tariff, nonlinear tariff, rate design,
  conservation rate, water rates, drought, billing, annex, capital recovery, price response, elasticity, bunching,
  kink. No slot screened a price-concept step; bunching estimators fork (task157, task174), so no graded figure here
  rests on a bunching estimate; task123 is a water-billing world on a proration reading (ETL), unrelated.
- **Sources, one line each.** The client's rigor cards for the task type (an existing wedge, short against long
  run, price and quantity jointly set) supply the family, none of them the step. The field's literature supplies the
  rung models: the marginal price with a difference variable (Taylor 1975, Nordin 1976), the perceived price between
  marginal and average (Shin 1985), the average-price response under block tariffs (Ito 2014 for electricity,
  Wichman 2014 for water). The pack's own rate history decides between them.
- **Clean-truth prototype** (scratchpad `t314proto/proto4.py` to `proto8.py`, before carding): the Fenwick Mesa
  charge recovers the true elasticity on the clean truth (Wald -0.324 against -0.32); an encompassing fit gives
  -0.316 on the whole-bill average price and 0.008 on the marginal price; the marginal-only route reads demand as
  nearly inelastic (-0.014 to -0.016). At the planned scale (6,200 accounts) the four routes file different options
  with every margin above 1.15: the whole-bill average price files Option C at 46.3 acre-feet (1.17 over Option B's
  39.6), a literature marginal elasticity of -0.4 files Option A at 88.0 (1.88 over B), the own marginal estimate
  files A at 11.6 (1.94), and the per-gallon average price files B at 52.7 (1.24 over A). Options A and C raise
  the same revenue (about USD 14 an account a summer month) and B about 12, so neither a revenue ranking nor a
  breadth ranking singles out C.

## Default path

1. Take the single-family accounts billed in every month of 2025 and 2026 from the billing export (both service
   areas, Fenwick Mesa's hundred cubic feet converted to thousand gallons, each rebill in place of the bill it
   cancels) and each account's June to September billed use in both summers; their average, bill month by bill
   month, is the baseline, about 1,216 acre-feet a summer.
2. Estimate the summer price response the block-rate demand model's way, on the city's own record: each account's
   change in June to September use across the July 2023 redesign against its change in marginal block price, weather
   taken out by comparing accounts within each bill month. Accounts whose block price jumped (15 to 20 thousand
   gallons, from 4.40 to 10.80) barely moved, so the elasticity is about -0.05.
3. Price each option through each account's marginal block price at its baseline use: Option A raises the tier-3
   price for every account above 15 thousand gallons, Option B adds 0.75 to every block, Option C moves no block
   price and saves nothing beyond a negligible income effect.
4. Sum each option's June to September saving to acre-feet and take the largest.

Ends on: Option A, the tier-3 drought rate, about 12 acre-feet (prototype 11.6).
Golden: Option C, the 14-dollar drought surcharge, about 46 acre-feet (prototype 46.3).

## Stump sentence

The default path files Option A, the tier-3 drought rate, at about 12 acre-feet, because it prices every option
through each account's marginal block price, the block-rate demand model's own price, with the elasticity the July
2023 redesign gives, under which the 14-dollar surcharge saves nothing; the July 2024 Fenwick Mesa capital recovery
charge, which raised every Fenwick Mesa bill by 14 dollars and moved no block price, cut that area's summer use
about 6 per cent against the rest of the city, so customers answer what the whole bill comes to per thousand
gallons, and on that price Option C takes out the most, about 46 acre-feet.

## Three rules

Task type: elasticity-welfare-policy-impact-estimation (Economics & Econometrics), which serves Opportunity Sizing & Decision Support in the taxonomy.
Domain test: The quantity that decides the call is each Stage 2 option's June to September 2027 saving, a price response under a block tariff estimated the way residential water demand is estimated, on the utility's own billing panel against the rate changes in its history, and with another field's nouns (pupils and minutes of reading, say) there is no bill, block price or fixed charge for a response to answer.
Swap: "Which reading programme cuts absence the most" keeps a pick and a sized figure but loses the tariff: no household pays a stepped price and no fixed charge sits on a bill, so the question of which price is answered disappears and the task stops reading.
Layer 1: The billing system's two eras (Fenwick Mesa's first-year legacy layout after its March 2022 migration), hundred cubic feet against thousand gallons per bill, cancelled bills and the rebills that replace them, estimated reads followed by catch-up reads, meter exchanges that split one service period, base charges by meter size, account turnover at a premise and read cycles that straddle calendar months, each produced by the city's billing system and meter shop and none placed to be caught.
Layer 2: estimand_identification, the price concept the response is read on: each option is priced through the change in the whole bill per thousand gallons each account would see, with the response measured where the record moved that price alone, rather than through the marginal block price the tariff's structure invites.
Decisive step: recognising from the city's own rate history that customers answer what the whole bill comes to per thousand gallons, because the one change that moved every Fenwick Mesa bill and no block price cut use while the redesign's block jumps barely did, and pricing the three options on that.
Not semantics: Every charge, use, unit, area, meter size and date read correctly leaves two correct prices on every bill, the marginal block price and the whole bill per thousand gallons, and the easy route takes the marginal one because the block tariff invites it; no field or definition says which one customers answer.
Not rule application: No filed rule or procedure says how customers respond to price (the rate resolutions compute bills, the drought plan defines the reduction); the enumerated family spans Option A at about 88 acre-feet (a literature marginal elasticity), Option A at about 12 (the city's own marginal estimate), Option B at about 53 (the per-gallon average price) and Option C at about 46 (the whole-bill average price), while the standing family, the models both past changes leave standing, is the whole-bill price alone at about 45 to 47 acre-feet, and what rules the others out is quiet, a 6 per cent area difference across one year's summers.
Analyst test: A strong analyst who conforms every bill, reads every rate correctly and estimates the summer price response on the city's July 2023 redesign against each account's marginal block price files Option A, the tier-3 drought rate, at about 12 acre-feet, the surcharge saving nothing.
Estimand: The drought plan's Stage 2 section files it: the fall in single-family use billed on the June to September 2027 bills against the same accounts' average June to September billed use in 2025 and 2026, for the accounts billed in every month of 2025 and 2026, in acre-feet.
No decoy: Nothing is planted: no memo, staff projection or consultant model argues for Option A, the textbook route is the solver's own, and the Fenwick Mesa charge and the 2023 redesign are ordinary rate actions recorded where the city records them.
No certified replay: No published or certified saving ships for any option or past rate change; the response is estimated from the bills, never recovered by reproducing a printed figure.
Lesson: Under a block tariff which price customers answer is an empirical question the utility's own rate history can settle, and a fixed charge that moves no marginal price can still cut use; no build on file teaches the marginal-against-average price test.

## Survivor anatomy

Actor: The deciding property, which price on a bill a household answers, has no column: every bill carries its charges and use correctly, and the response lives only in how use moved when a past change moved one price without the other.
Link: The signal is read across the two service areas through the July 2024 Fenwick Mesa capital recovery charge, a comparison between areas the block-rate demand model never asks for, set against the July 2023 redesign that moved marginal prices city-wide; no key, flag or sentence ties the charge to use.
Reflex: The field's named method, a summer price elasticity applied to each account's marginal block price (a literature elasticity at rung 0, the city's own estimate from the 2023 redesign at rung 1), files Option A.
Back-test: The marginal-price model estimated on the 2023 redesign fits that redesign (accounts whose block price jumped barely moved, which a small marginal elasticity reproduces) and tracks every summer's city-wide total with weather, so nothing in the textbook route's own checks refutes it.
Second use: The bills carry every ask (revenue, tier volumes, bill impacts); the area and the capital charge sit on every Fenwick Mesa bill because the annexation agreement bills them; the rate resolutions exist to set rates; nothing ships for the decisive step alone.
Shock: The Fenwick Mesa difference is about 6 per cent of summer use against the rest of the city, inside the summer-to-summer swing that weather causes and smaller than the redesign's own movements, so it is not the pack's largest anomaly.
Pins: The drought plan files the WHAT (the accounts, the June to September bills, the 2025 and 2026 baseline, acre-feet); no sentence names a marginal price, an average price, an elasticity or the Fenwick Mesa charge's effect on use.

## Tried and rejected

- 2026-11-04, the seed OS16's own world (a workforce board's USD 2M fund, randomised pilots of outreach, exam vouchers, placement coaching and childcare stipends): its pairing has no Opportunity Sizing task type; re-homed to economics, every decisive step the pilots offer is spent or barred on file (Draw); not built.
- 2026-11-04, the same workforce world with non-experimental evidence (Ashenfelter's dip read through a comparison aligned on time since job loss): the aligned comparison is the field's own best practice for non-experimental training evaluation, so the golden would be the opponent's reflex (stumping 1.1b); not drawn.
- 2026-11-04, a workforce surrogate index (pilot effects on the second quarter after exit predicted from early outcomes): the surrogate set is a free method choice and the family forks the graded figure; not drawn.
- 2026-11-04, ambulance posts sized by late calls under correlated unit busyness (urban optimisation): dead on file (task313's note records task308's screen, readers replaying dispatch) and its honest label is binding_constraint, barred by task210; not drawn.
- 2026-11-04, a booster or lift station's added pump read through a system curve rebuilt from SCADA once the varying tank or wet-well lift is taken out: the honest strategy is decomposition_attribution (the measured head split between lift and friction), barred against task398 at the time, and a water-capacity answer in gallons a minute would sit beside task120; not drawn.
- 2026-11-04, a district metered area's recoverable leakage read off its own post-survey night-flow floor: leakage worlds are on file (task162, task301's landed probe, task194); not drawn.
- 2026-11-04, the price-concept stump with three options raising equal revenue: under the whole-bill average price, equal-revenue options save within 12 per cent of each other (best margin 1.125, proto3 and proto5), under the 1.15 floor; the options now carry the revenues their designs give (A and C about 14 dollars an account a summer month, B about 12).
- 2026-11-04, G16 as the decisive generator: `ban.pattern` against task489 and `test.same_driver` against task462 in the batch; G1 (the unit of value, the price a household answers) is the honest decisive code and G16 sits behind it.
