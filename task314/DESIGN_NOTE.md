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
  Opportunity Sizing only) / Opportunity Sizing & Decision Support. The pool is the plan's single-family baseline,
  772.1 acre-feet over the June to September bills of 4,341 accounts; the realisable is what each option takes out
  of it; the call is the option that takes out the most.
- **Shape 07 (a grid):** the options by their June to September saving (three cells, a bill-month split in the
  workbook and the chart), the call, the runner-up and the gap; the asks add a twelve-cell grid, three figures for
  each of June to September 2026 (Ask sheet); the chart's named parts and the files. About 26 criteria.
- **Mechanism:** stump strategy `forecast_method_backtest` (the natural price model, the marginal block price, gives
  the one option that moves no block price no effect, and the city's own rate history selects the price customers
  answer; no back-test is filed); gap objective (the block price is a correct record and is not what the response
  is scored on); pattern none with G1 decisive (the unit of value, the price the household answers) and G16 behind
  it; Gate G `method_or_model_selection`; Layer 2 family `estimand_identification`, own pattern
  `the-price-block-rate-customers-answer-read-off-a-fixed-charge-on-one-area`.
- **World:** the City of Ardley Springs (about 19,000 people, an unnamed Mountain West state), its Water Department,
  4,800 single-family premises (1,500 in Fenwick Mesa), the Fenwick Mesa area annexed in 2021 from the old Fenwick
  Mesa Water Company and billed a USD 14.00 capital recovery charge from the July 2024 bills to repay the 2021B
  bonds, the Upper Brennan Basin Water Conservancy District that wholesales the summer supply and has set its 2027
  allocation at 78 per cent of entitlement (the Stage 2 trigger). Furniture: forum `council_or_assembly` (the
  council's December 8, 2026 hearing), forcing event `vote_or_meeting`, organisation `local_government`, role
  `finance_controller` (the department's rates and finance manager), context artifact `filed_standard` (the drought
  contingency plan).
- **People** (`guard.py names --geo "United States" --seed 314`, none warning): Tami Weaver (rates and finance
  manager), Jason Morgan (utilities director), Clifford Haley (water resources manager, the drought plan's author),
  Beth Sheppard (city clerk); on the documents also Laurie Stuart (mayor), Randy Silva, Ebony Valentine, Corey Lam,
  Nathaniel Cannon, Gary Riley and Julie Bowers (council), Theresa Howard (city attorney), Sylvia Chavez and Helen
  Nelson (the district), and the meter shop's technicians by initial, all from `guard.py names --seed 314 --n 60` and
  screened clean of first-name and surname reuse (`guard.py surface`: no people WARN).
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
- **As built** (bundle figures, `checks.py` and `verify.py`): the Fenwick Mesa comparison gives an elasticity of
  -0.280 on the whole-bill price (Fenwick Mesa's July to September use 4.6 per cent below the rest of the city's
  movement from 2023 to 2025, its bill per thousand gallons 18.5 per cent above it); the thirteen licensed
  estimates run -0.271 to -0.320. Options A, B and C save 7.9, 19.0 and 28.9 acre-feet (bins 10, 20 and 30, every
  estimate inside); the gap 9.9 (bin 10). Revenues per bill at baseline use are USD 5.21, 8.69 and 13.60.

## Default path

1. Take the single-family accounts billed in each June to September bill month of 2025 and 2026 from the billing
   export (both service areas, Fenwick Mesa's hundred cubic feet at 748.052 gallons, each rebill in place of the
   bill it cancels) and average each account's 2025 and 2026 use bill month by bill month: the baseline, 772.1
   acre-feet on 4,341 accounts.
2. Estimate the summer price response the block-rate demand model's way, on the city's own record: each account's
   change in July to September use across the July 2023 restructuring against its change in marginal block price at
   its own 2022 use, in the rest of the city. Accounts whose block price jumped (15,001 to 20,000 gallons, from 4.40
   to 10.80) barely moved, and the elasticity comes out at -0.120.
3. Price each option through each account's marginal block price at its baseline use: Option A raises the third
   block for every bill above 15,000 gallons and cuts the first, Option B adds 0.60 to every block, Option C moves no
   block price and saves nothing.
4. Sum each option's June to September saving to acre-feet and take the largest.

Ends on: Option A, the conservation blocks, about 16 acre-feet (15.9 on the pack).
Golden: Option C, the drought surcharge, about 30 acre-feet (28.9 on the pack).

## Stump sentence

The default path files Option A, the conservation blocks, at about 16 acre-feet, because it prices every option
through each account's marginal block price, the block-rate demand model's own price, with the elasticity the July
2023 restructuring gives, under which the drought surcharge saves nothing; the July 2024 Fenwick Mesa capital
recovery charge, which added 14 dollars to every Fenwick Mesa bill and moved no block price, cut that area's summer
use about 4.6 per cent against the rest of the city, so customers answer what the whole bill comes to per thousand
gallons, and on that price Option C takes out the most, about 29 acre-feet against Option B's 19.

## Three rules

Task type: elasticity-welfare-policy-impact-estimation (Economics & Econometrics), which serves Opportunity Sizing & Decision Support in the taxonomy.
Domain test: The quantity that decides the call is each Stage 2 option's June to September 2027 saving, a price response under a block tariff estimated the way residential water demand is estimated, on the utility's own billing panel against the rate changes in its history, and with another field's nouns (pupils and minutes of reading, say) there is no bill, block price or fixed charge for a response to answer.
Swap: "Which reading programme cuts absence the most" keeps a pick and a sized figure but loses the tariff: no household pays a stepped price and no fixed charge sits on a bill, so the question of which price is answered disappears and the task stops reading.
Layer 1: The billing system writes Fenwick Mesa's unreplaced legacy meters in hundred cubic feet beside thousand gallons (12.6 per cent of single-family bills), cancels a misread bill and rebills it in the month (806 pairs), estimates a read and catches it up on the next (1,992 estimates), opens a new account when a premise changes hands, bills base charges by meter size, and reads twenty cycles across each month; the facility read log keys rejected reads that the reader retakes and writes dates month first; the fill station stamps local time with its offset; none is placed to be caught and each mishandled leaves the call and every bin (R2).
Layer 2: estimand_identification, the price concept the response is read on: each option is priced through the change in the whole bill per thousand gallons each account would see, with the response measured where the record moved that price alone, rather than through the marginal block price the tariff's structure invites.
Decisive step: recognising from the city's own rate history that customers answer what the whole bill comes to per thousand gallons, because the one change that moved every Fenwick Mesa bill and no block price cut use while the restructuring's block jumps barely did, and pricing the three options on that.
Not semantics: Every charge, use, unit, area, meter size and date read correctly leaves two correct prices on every bill, the marginal block price and the whole bill per thousand gallons, and the easy route takes the marginal one because the block tariff invites it; no field or definition says which one customers answer.
Not rule application: No filed rule or procedure says how customers respond to price (the resolutions compute bills, the plan defines the reduction); the enumerated family spans Option A at 50.6 acre-feet (a literature block-price elasticity of -0.40), Option A at 15.9 (the city's own block-price estimate, -0.120), Option B at 37.0 (the per-gallon volumetric price, -0.404) and Option C at 28.9 (the whole-bill price, -0.280), while the standing family, the price both past changes leave standing, is the whole-bill price alone across thirteen estimates at 28.0 to 33.0 acre-feet, and what rules the others out is quiet, a 4.6 per cent area difference across two summers.
Analyst test: A strong analyst who conforms every bill, reads every rate correctly and estimates the summer price response on the city's July 2023 restructuring against each account's marginal block price files Option A, the conservation blocks, at about 16 acre-feet, the surcharge saving nothing.
Estimand: The drought plan's Section 5.3 files it: the fall a Stage 2 rate measure brings about in the water billed to single-family residential accounts on the June to September bills of the year it applies, from what those bills would carry at the rates otherwise in force, against each account's baseline (the average of its use on each bill month's bills in the two preceding years), for the accounts billed in each of the eight June to September bill months of those years, in acre-feet.
No decoy: Nothing is planted: no memo, staff projection or consultant model argues for Option A, the textbook route is the solver's own, and the Fenwick Mesa charge and the 2023 restructuring are ordinary rate actions recorded where the city records them.
No certified replay: No published or certified saving ships for any option or past rate change; the response is estimated from the bills, never recovered by reproducing a printed figure.
Lesson: Under a block tariff which price customers answer is an empirical question the utility's own rate history can settle, and a fixed charge that moves no marginal price can still cut use; no build on file teaches the marginal-against-average price test.

## Survivor anatomy

Actor: The deciding property, which price on a bill a household answers, has no column: every bill carries its charges and use correctly, and the response lives only in how use moved when a past change moved one price without the other.
Link: The signal is read across the two service areas through the July 2024 Fenwick Mesa capital recovery charge, a comparison between areas the block-rate demand model never asks for, set against the July 2023 restructuring that moved marginal prices city-wide; no key, flag or sentence ties the charge to use.
Reflex: The field's named method, a summer price elasticity applied to each account's marginal block price (a literature elasticity at rung 0, the city's own estimate from the 2023 restructuring at rung 1), files Option A.
Back-test: The marginal-price model estimated on the 2023 restructuring fits that restructuring (accounts whose block price jumped barely moved, which a small marginal elasticity reproduces) and tracks every summer's city-wide total with weather, so nothing in the textbook route's own checks refutes it.
Second use: The bills carry the baseline, the population and every bill an option changes; the area and the capital charge sit on every Fenwick Mesa bill because the annexation agreement bills them; the rate resolutions exist to set rates; nothing ships for the decisive step alone.
Shock: The Fenwick Mesa difference is 4.6 per cent of summer use against the rest of the city, smaller than the 5.7 per cent rise the warmer 2025 summer brought the rest of the city and smaller than the restructuring's own movements, so it is not the pack's largest anomaly.
Pins: The drought plan files the WHAT (the accounts, the June to September bills, the 2025 and 2026 baseline, acre-feet); no sentence names a marginal price, an average price, an elasticity or the Fenwick Mesa charge's effect on use (asserted over every document).

## Readability screen

Each rung against the seven tests (1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear, 7
dedicated organ); the reflex row comes from the field's vocabulary for a residential water price response under a
block tariff (the marginal-price elasticity with a difference variable, the discrete-continuous block model, the
perceived price, the volumetric average price, and a fixed charge read as sending no price signal).

| Rung | 1 | 2 | 3 | 4 | 5 | 6 | 7 | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 a literature block-price elasticity, -0.40 (A 50.6, B 26.0, C 0) | no | the block charges on each bill | yes: the textbook block-rate model | no | no | yes | no | readable |
| R1 the city's own block-price elasticity from the 2023 restructuring, -0.120 (A 15.9, B 7.9, C 0) | no | the block charges and the dated schedules | yes: the block-rate model on the utility's own record | the restructuring's fit confirms it | no | yes | no | readable |
| R2 the per-gallon (volumetric) price from the restructuring, -0.404 (A 9.5, B 37.0, C 0) | no | the block charges | yes: the volumetric average price | no | no | yes | no | readable |
| G (decisive) the whole bill per thousand gallons, read off the Fenwick Mesa charge, -0.280 (A 7.9, B 19.0, C 28.9) | no sentence names a price concept, a response or the charge's effect on use | the charge's column says what each bill carried; no column holds a response or ties the charge to use | no: the rate-design reflex reads a fixed charge as sending no price signal | quiet: the restructuring's own fit supports the block price | no | no: two areas over two summers, an elasticity, then each option priced bill by bill at each account's baseline | every file it reads has its own use | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | single-family residential accounts | RES-SF (W10) in both service areas | Fenwick Mesa left out | same call; every saving moves | plan 1.1 (every part of the service area) and 1.2 (an account billed under rate code W10); Resolution 2023-12 Section 1 |
| SF2 | bill month | the month of the bill date | the month of the read date | same call and figures (asserted: every bill is dated in its read month) | plan 1.2 (the calendar month in which a bill is issued); convergence |
| SF3 | use billed on a month's bills | the standing bill (a rebill in place of the bill it cancels) | cancelled bills kept | same call and bins (R2 asserted) | the export's replaces_bill_no |
| SF4 | the two preceding years | 2025 and 2026 for a 2027 measure | 2024 and 2025 | not licensed | plan 5.3, the year it applies |
| SF5 | the baseline | each account's average for each bill month, summed | the average of the two summers' totals | identical (asserted) | arithmetic |
| SF6 | acre-feet | 325,851 gallons | 325,853 | same bins (asserted) | convergence |
| SF7 | the rates otherwise in force | Resolution 2023-12 with the Fenwick Mesa charge | the charge left off 2027 bills | same call (asserted) | Resolution 2024-17 Section 2 (to June 2044); the staff report, every option |
| SF8 | the June to September bills of the year it applies | bills dated June to September 2027, all under the option | the option on part of the summer | same call (asserted) | the staff report, bills issued May 1 to October 31, 2027 |
| SF9 | hundred cubic feet | 748.052 gallons | 748 | same bins | Resolution 2023-12 Section 2 |
| SF10 | base charges | by meter size, 3/4 or 1 inch | one base for all | same call and bins (R2 asserted) | Exhibit A |
| SF11 | estimated bills | billed use (kept) | dropped | same call and bins (R2 asserted) | plan 5.3, use billed |
| SF12 | the unit | the account | the premise | same call and bins (R2 asserted) | plan 5.3, the accounts |
| SF13 | Option A | first block 2.70, third 14.80, limits 6,000 and 15,000 | other limits | not licensed | the staff report |
| SF14 | Option B | 0.60 added in every block | the third block only | not licensed | the staff report, in every usage block |
| SF15 | Option C | 13.60 on each monthly bill, one standing bill an account a month | per rebill | same (asserted, one standing bill each account month) | the staff report, each monthly bill |
| SF16 | the reduction | against what the bills would carry at the rates otherwise in force (each account's baseline) | the change from 2026 to 2027 with weather in | not licensed | plan 5.3 |
| SF17 | rounding the gap | the difference of the savings, rounded once | a difference of rounded savings | same (asserted, 10 both ways) | the prompt's rounding sentence |
| SF18 | Ask, a fill's month | the local date the session starts | the UTC date | same figures (asserted: no session after 4:30 p.m. on a month's last day) | convergence; the offsets on every timestamp |
| SF19 | Ask, a fill across midnight | counted where it starts | split | same (asserted: none spans a month end) | convergence |
| SF20 | Ask, a facility's use on a month's reads | the register advance to the read dated in that month | a calendar month interpolated | the asking sentence's reading; one read date per facility a month (asserted) | the asking sentence |
| SF21 | Ask, the turbine meter's hundred cubic feet | 748.052 gallons | 748 | same one-decimal figures (asserted) | convergence |

## Ladder

Every rung priced on the cut pack (`verify.py`) and on the clean truth (`checks.py` R3a and R3b):
- **Rung 0, a literature block-price elasticity (-0.40):** A 50.6, B 26.0, C 0; files A at 1.95.
- **Rung 1, the default path, the city's own block-price estimate from the 2023 restructuring (-0.120):** A 15.9,
  B 7.9, C 0; files A at 2.01.
- **Rung 2, the per-gallon volumetric price, estimated on the restructuring (-0.404):** A 9.5, B 37.0, C 0; files B
  at 3.88.
- **Decisive, the whole bill per thousand gallons, estimated on the Fenwick Mesa charge (-0.280):** A 7.9, B 19.0,
  C 28.9; files C at 1.52. The thirteen licensed estimates of the comparison (other summers and months, billed
  against simulated prices, the account mean, a vacancy screen, pooled years) run -0.271 to -0.320 and give A 7.7 to
  9.0, B 18.4 to 21.7, C 28.0 to 33.0 and a gap of 9.6 to 11.3, every one in its bin; the world's own -0.32 too.
- **Positions:** C is last on every rung below the decisive one; no rung margin under 1.15; the final 1.52.
- **The whole-bill price assumed:** a solver who takes the whole-bill price from the literature without testing it
  lands C at any elasticity (the ranking does not depend on the elasticity), and the largest bill increase lands C
  too (revenues per bill USD 5.21, 8.69, 13.60); both are the decisive belief taken on faith, and the city's own
  record is what a solver needs to hold it against the block-price model the restructuring supports (Gate F count in
  `checks.py`).

## Closure table

| Axis | Reading here | Closure |
|---|---|---|
| 1 Population | single-family accounts billed in each of the eight June to September bill months of 2025 and 2026 | plan 5.3; SF1, SF2, SF3, SF12 |
| 2 Unit of account | the account; acre-feet | plan 5.3; SF6, SF12 |
| 3 Attribution window | June to September bills, by bill date | plan 5.3; SF2, SF8 |
| 4 As-of dating | the export of November 2, 2026; the 2027 rates are Resolution 2023-12 plus the option | the staff report; SF7 |
| 5 Version basis | the standing bill; the rate schedule by bill date | SF3; Resolutions 2021-44, 2023-12 and 2024-17 effective dates |
| 6 Denominator | none for the call; the whole bill per thousand gallons inside the method | the method (HOW), forced by the record |
| 7 Weighting | every account's bill months summed | plan 5.3 |
| 8 Window length | two preceding years | plan 5.3; SF4 |
| 9 Boundary inclusivity | bills dated in the month | SF2 converges; no bill dated outside its read month |
| 10 Rounding path | savings and gap to the nearest 10 acre-feet once; fill water to the thousand gallons; facility use to one decimal | the prompt; SF17; every figure clear of its edge (asserted) |
| 11 Tie-break | none | margins 1.52 and above |
| 12 Maturity and censoring | every baseline bill issued by the export | the export closes after the October 2026 run |
| 13 Order of operations | response per account per bill month, summed | the method; SF5 |
| 14 Row order | none | not applicable |
| 15 Duplicate resolution | cancelled and rebilled; resumed fill sessions (ask) | SF3; the ask's device |
| 16 Identity normalisation | account against premise; facility meters across exchanges | SF12; the work orders (ask) |
| 17 Netting against gross | Option A cuts one block and raises another: netted per bill | the staff report defines the option |
| 18 Dimensional units | hundred cubic feet against thousand gallons; acre-feet | SF9, SF6, SF21 |
| 19 Code and status semantics | customer class, rate code, bill status, read type | the export's own codes; SF1, SF3, SF11; never the stump |
| 20 Integerisation | none | not applicable |
| 21 Clause scope | plan 5.3 covers Stage 2 rate measures for the single-family class | plan 4.2(f) and 5.3 |
| 22 Forward window contents | 2027 bills priced at each account's baseline use under 2026 rates plus the option | plan 5.3, the baseline is the use without the measure |

## Literal reader

Executed word for word on the cut pack: plan 5.3 files the population, the bills, the baseline and the unit; the
staff report files each option as an addition to Resolution 2023-12's single-family rates on the bills issued May
1 to October 31, 2027; the resolutions file every rate by bill date, the hundred cubic feet conversion and the
capital recovery charge; the prompt files the rounding. Nothing filed says how customers respond to a rate, so the
literal reader must estimate the response from the bills, and the easy answer (the marginal block price with the
restructuring's elasticity) is an easy method on the same literal estimand, not another reading of a term. Every
convention the computation needs (SF1 to SF17) is ruled out by a quoted sentence or converges on the same call and
bins, asserted in `checks.py`; the ask conventions SF18 to SF21 converge or are fixed by the asking sentence.

## Oracles

- The 2023 restructuring: its fit supports the block-price model (heavy users' block price jumped and their use
  barely moved), so it confirms the reflex; read on the whole-bill price it agrees with the golden's ranking, and it
  never arbitrates on its own.
- The Fenwick Mesa capital recovery charge: one fixed charge on one area, in the bills and Resolution 2024-17; it
  separates the whole-bill price from the block price and hands over no figure.
- The district notice and the plan's stage table: the Stage 2 trigger and the demand reduction sought; no option is
  sized or ranked.
- The distractors (the agricultural weather station's daily record, the state water use program's 2025 table, the
  conservation rebate register): relevant to summer use, read by no rung; the rebates are spread across both areas
  and every year, so they do not explain Fenwick Mesa's fall.

## Layer 1 inventory

Each item, the system that writes it, its file and its natural mishandling; each mishandled leaves the call and
every bin (R2 in `checks.py`):
- Hundred cubic feet on Fenwick Mesa's legacy meters (the meters the 2022 to 2023 change-out did not reach): the
  billing system, the bill export's uom column; read as thousand gallons (C 31.6, bins hold).
- Cancelled and rebilled misreads: the billing system's high-low edit, bill_status and replaces_bill_no; cancelled
  bills kept (C 29.7).
- Estimated reads caught up on the next actual read: read_type E; dropped (C 26.9).
- Premises changing hands: a new account number at the premise; keyed by premise (C 33.1).
- Base charges by meter size: meter_size_in; priced as 3/4 inch (C 28.9).
- Read cycles across the month: read_date and bill_date; bill month from the read date (identical).
- Facility reads: month-first dates, a keyed read the handheld rejected and the reader retook on the visit, two
  meter exchanges in the work orders (ask hazards).
- Fill station timestamps in local time with the offset across the DST change (ask, converges).

## Ask sheet

Planning weights 38 / 7 / 55. The call (the option, the runner-up, the gap and the three savings) carries 38. The
asks are the 2026 base for the City's own Stage 2 measures, which the staff report says Water Resources sets its 2027
targets from (plan 4.2(c) and (d)), twelve figures: for each of June to September 2026, the water drawn at the bulk
fill station (thousand gallons), the tank fills, and the water City facilities used on that month's reads (acre-feet to
one decimal).

- **Fill station, water and tank fills (8 figures):** H18 home: the base for the fill station's Stage 2 permit and card
  limits. Path: the transaction export (txn_start with its offset, bay, card_no, meter_start_gal, meter_end_gal,
  gallons, amount_usd), the vendor's monthly activity report, Resolution 2023-12's bulk water charge. Primary (D1,
  one event in two rows): from June 3 to September 26 the bay 2 coupling faulted and a hauler re-swiped to finish;
  the controller resumed the session and wrote the session's opening register and its whole volume on the new row,
  so the first row's water is carried twice (27 to 36 resumed sessions a month); the vendor's report sums the rows,
  so the wrong path reconciles; a trailer filled straight after its truck is a separate session from the closing
  register on both bays (the benign twin), and only the shared opening register tells the two apart. Hazards: the
  DST offset, City trucks billed at zero, the 100-gallon billing increment.
- **City facilities (4 figures):** H18 home: the base for the 20 per cent facility irrigation cut. Path: the read
  log (facility_id, meter_id, read_date month first, read_time, register), the meter list (service_address,
  service_type, register_unit), the work orders (old_final_read, new_initial_read, the register units). Primary (D1,
  the same water through two meters): the Westbrook Aquatic Center's pool fill meter sits on the pavilion's service at
  1450 Westbrook Dr, so its water is already on the pavilion meter (the May fill and the July refill show on both, and
  the pavilion's advance always exceeds the pool's by a steady remainder); summing every meter counts the pool twice
  (0.41 to 1.21 acre-feet a month). Hazards: the golf course's meter exchanged on June 2 to a turbine meter that
  registers in hundred cubic feet, the cemetery's exchange on August 4, the retaken keyed reads.
- **Tank fills:** the asking sentence counts tank fills, so a trailer filled after its truck is a second fill and a
  session resumed after the bay 2 fault is one; the register shows which is which (a new session opens at the last
  closing register, a resumed one repeats its own opening register).
- **Pin test:** the asking sentences pin the months, the units and "on that month's reads"; no pin names a bay, a
  register, a session, a sub-meter or an address. No filed rule adjudicates a device; nothing narrates one.
- **Main population zero-counts:** no fill or facility row among the bills, no device row in the single-family
  population (asserted); the call holds with every ask file deleted.
- **The full includer:** a response that pairs the resumed sessions by their opening register and finds the pool
  meter inside the pavilion's keeps all 12, a known limit; one that finds only the sessions keeps 8, only the pool 4.

Pair ceiling: 28.5 (the cracker on the call at 45.0 with 0 of 12 asks; the mirror off the call at 12.0 with 0 of 12).
Mirror leakage: 0.0 per cent of ask weight.
Measured by: generator/ceiling.py on the cut pack (digest printed by the script).

| Ask figure | Cracker (rows summed as the vendor sums them, every listed meter counted, exchanges walked) | Golden | Cracker |
|---|---|---|---|
| Fill water, June | 725 | 678 | miss |
| Tank fills, June | 280 | 244 | miss |
| Facilities, June | 23.8 | 22.6 | miss |
| Fill water, July | 757 | 717 | miss |
| Tank fills, July | 285 | 258 | miss |
| Facilities, July | 30.3 | 29.7 | miss |
| Fill water, August | 670 | 630 | miss |
| Tank fills, August | 259 | 229 | miss |
| Facilities, August | 32.1 | 31.2 | miss |
| Fill water, September | 719 | 682 | miss |
| Tank fills, September | 268 | 240 | miss |
| Facilities, September | 24.1 | 23.7 | miss |

## Leak review

`leak.py task314 --asof 2026-11-03`, verdict REVIEW, no LEAK (sweeps 1, 2, 5 to 9 and 11 clean; sweep 10 INFO). An
earlier pass read LEAK on the capital recovery charge's amount, a pack input quoted in the write-up's first block; the
amount now sits only in the step that reads it. Each REVIEW line ruled here:
- Sweep 3, the agenda report (14 of 17 words of the committed call) and the drought plan (15 of 17): the report
  defines the candidates by their own names and the plan the Stage 2 measure, so both carry Option C, drought
  surcharge, Stage 2, rate measure, summer 2027, acre-feet, June to September and single-family; neither states a
  saving, a ranking or a recommendation (R3c asserted). Harmless.
- Sweep 4, six documents with three to eight of the stump paragraph's common words (charge, account, billed,
  customers, effect, reading, record, average): rate-resolution and plan vocabulary ("effective", "meter readings",
  "the former company's customers", plan 5.3's "average of the use billed" for the baseline). `checks.py` asserts that
  no document carries a price-concept or response term, and Resolution 2024-17's recitals no longer describe how the
  charge relates to an account's use (that clause was cut at this pass; the charge's amount and scope are what the
  bills need). Harmless.
- Sweep 12, the agenda report and Resolutions 2021-44 and 2023-12, five column words each (gallons, consumption,
  station, service, date, action, facility, completed): ordinary words of a rate schedule and an agenda report, in
  the organisation's own records; none lists or glosses a file's columns. Harmless.
- Sweep 13 read REVIEW on the capital recovery charge resolution's file name, which carried its title; the three
  resolutions now ship under the clerk's record numbers (`RES 2021-44.pdf` and its siblings), and the sweep is clean.

## Tried and rejected

- 2026-11-04, the seed OS16's own world (a workforce board's USD 2M fund, randomised pilots of outreach, exam vouchers, placement coaching and childcare stipends): its pairing has no Opportunity Sizing task type; re-homed to economics, every decisive step the pilots offer is spent or barred on file (Draw); not built.
- 2026-11-04, the same workforce world with non-experimental evidence (Ashenfelter's dip read through a comparison aligned on time since job loss): the aligned comparison is the field's own best practice for non-experimental training evaluation, so the golden would be the opponent's reflex (stumping 1.1b); not drawn.
- 2026-11-04, a workforce surrogate index (pilot effects on the second quarter after exit predicted from early outcomes): the surrogate set is a free method choice and the family forks the graded figure; not drawn.
- 2026-11-04, ambulance posts sized by late calls under correlated unit busyness (urban optimisation): dead on file (task313's note records task308's screen, readers replaying dispatch) and its honest label is binding_constraint, barred by task210; not drawn.
- 2026-11-04, a booster or lift station's added pump read through a system curve rebuilt from SCADA once the varying tank or wet-well lift is taken out: the honest strategy is decomposition_attribution (the measured head split between lift and friction), barred against task398 at the time, and a water-capacity answer in gallons a minute would sit beside task120; not drawn.
- 2026-11-04, a district metered area's recoverable leakage read off its own post-survey night-flow floor: leakage worlds are on file (task162, task301's landed probe, task194); not drawn.
- 2026-11-04, the price-concept stump with three options raising equal revenue: under the whole-bill average price, equal-revenue options save within 12 per cent of each other (best margin 1.125, proto3 and proto5), under the 1.15 floor; the options now carry the revenues their designs give.
- 2026-11-04, G16 as the decisive generator: `ban.pattern` against task489 and `test.same_driver` against task462 in the batch; G1 (the unit of value, the price a household answers) is the honest decisive code and G16 sits behind it.
- 2026-11-04, Option A as a third-block drought rate alone (no cut to the first block): under the whole-bill price it raised heavy users' bills so far that it beat the surcharge; Option A became conservation blocks (a cheaper first block with the dearer third), which barely moves a typical bill.
- 2026-11-04, the savings at one decimal of an acre-foot: the licensed estimates spread about 15 per cent, several bins at that precision; the savings are graded to the nearest 10 acre-feet, and the option levels (adder 0.60, surcharge 13.60) were set so every estimate sits inside its bin with 2.9 or more to spare.
- 2026-11-04, a water balance ask on the district's turnout report and the wells' totalizers (a check meter left on the report beside its replacement, a well meter reset): both devices are found by the hygiene battery (a second series repeating the first, a change log walked) and the district's statements arbitrate, so the cracker kept them; replaced by the fill station's resumed sessions and the pool fill meter inside the pavilion's.
- 2026-11-04, Fenwick Mesa's legacy meters replaced through 2026: the change-out switched units inside the comparison's own window, so reading hundred cubic feet as thousand gallons moved the call; the change-out now ends in June 2023, before the comparison's first summer, and the mishandling leaves every bin (R2).
- 2026-11-04, the plan's population as accounts billed in every month of both baseline years: on a November 2026 export the second year is not complete; filed as the eight June to September bill months.
