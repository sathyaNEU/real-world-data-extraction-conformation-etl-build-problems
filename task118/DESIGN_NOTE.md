# task118 design note, architecture 5

The slot's fifth architecture: a city-owned electric utility's 2027 demand-response budget, in a new world, dataset,
generator and prompt shell. Architecture 4 (an island legislature's duty envelope) is spent at the portal; its card
entry moved to the lineage. Earlier architectures' notes live in git history and in `## Tried and rejected` below.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task118.json`, architecture v5. **Pairing:** client domain
  energy-systems-utilities, task type `generation-capacity-planning` (serves OS), objective
  opportunity-sizing-decision. The headline is a sized opportunity: from the units the USD 3.2 million buys in each
  program (the pool) to the load those units take off the design year's system peak hour (the realisable), and the
  sized figures drive the call.
- **Shape:** other. Criteria: each program's accredited megawatts from the budget (4), the call, the runner-up and the
  gap (3), the 2026 audit's Cool Credit premises online at 16:00 on each 2026 event day (17), the battery incentive by
  event month and the premises at the season cap (5), and the commercial capacity payment by month (4): 33, plus the
  two files.
- **Strategy and labels:** `binding_constraint` (the buffer each programme draws on is a capacity that binds after
  consecutive calls; the limit itself changes the pick), Gate G `binding_constraint`, gap objective then time, pattern
  none, generators G13 (the decision's occasion is not the record's typical one), G7 (the operating procedure fixes
  when calls happen), G14 (the pooled response does not apply to this occasion). Layer 2 `allocation_constraints`,
  pattern `own:consecutive-dispatch-depletion` (energy carries no client rigor card).
- **World:** Cholla Basin Municipal Utility (CBMU), the electric utility of an invented desert city in Arizona,
  Mountain Standard Time all year, USD. Four programmes: Cool Credit (smart thermostats, Halvern Controls the device
  platform), Peak Time Rewards (day-ahead alerts with a per-kWh rebate), Business Demand Partners (commercial cooling
  load through Arroyo Demand Services), Home Battery Network (customer batteries through Brightwell Storage). Ridgeway
  Analytics runs the programmes' measurement and verification.
- **Furniture, drawn and checked:** forum `council_or_assembly` (the city council adopts the budget with the resource
  adequacy plan), forcing `budget_or_appropriation`, org `utility_or_infrastructure`, role `capacity_planner`,
  artifact `capacity_report` (the 2027 resource adequacy plan's accreditation chapter is the governing document).
  Personas from `guard.py names --geo US --seed 118`: Corey Cox (resource planning), Nina Franklin (system
  operations), Lisa Jennings (Ridgeway), Kathy Gibson (Arroyo).
- **Data-native sentence:** the measurement record holds three summers of event days that mostly stand alone, because
  OP-7 calls the programmes only on weekdays whose forecast high reaches 110F and the city's heat rarely holds that
  long, while the design year's peak hour comes on the fourth weekday of a 110F spell; the thermostats' homes, the
  rebate customers and the commercial buildings each give less on every consecutive call and recover only on a day
  off, and the batteries recharge from rooftop solar every afternoon, so the record's average day and its hottest days
  both price the wrong occasion.
- **Abstraction sentence (stumping Part 6), against the nearest approved builds:** written for this build, "a
  resource's response falls with its own consecutive use, so its value on the occasion the decision prices is read at
  the run position the operating rule forces there, not at its average or its weather-matched level". Against 309 (an
  effect read class by class of an exogenous intensity and carried through a forward event mix), 162 (a device's
  effect replayed reading by reading through recorded upstream values) and 120 (a peak draw rebuilt as inflow plus the
  reserve drawn down) the shared sentence would be "the effect is read at the decision's condition", which names no
  decisive move; the moves differ (an exogenous class, a threshold replay, a storage identity against a state built
  from the resource's own call history), so no reviewer's sentence fits both builds of any pair. Setting neighbours on
  file, not approved: 131 (a peak tariff's rebound surge on the design day's whole curve) and 308 (a peaker credited
  from its sister units' shared fuel outages); neither turns on consecutive calls, and 308's screen of energy-limited
  demand response over long cold spells died on an unfiled call schedule, which OP-7 files here.
- **Shell (redrawn with the world):** question form `what`, the second sentence opening on the note itself, the
  rounding sentence opening on "Megawatts", deliverables `docx+csv`; the dead shell (how-much, put, docx plus xlsx)
  is in `lineage_shells`. `where` and `csv+pdf` were drawn first and moved when task181's draw took both an hour
  earlier (`repeat.question_form`, `repeat.deliverables`).
- **Guard:** `check` PASS on the registered card (2026-10-31T17:17Z). At 16:30 the draft met `ban.pairing` and
  `ban.org_family` against task464 (energy, opportunity sizing, a utility); the design went on on paper and the card
  registered once task181's draw moved the window, with no label changed to pass. `repeat.decision` (pick one after
  task268) is answered by the decision: one budget line expands one programme.
- **Sources, one line each.** The client's two-layer standard (the field's own analysis decides: a load impact
  evaluation's per-unit reduction at planning conditions). The California load impact protocols' ex post and ex ante
  structure (public, the field's method at rungs 0 and 1). Utility demand-response evaluations reporting event-day
  impacts by consecutive event day and the overnight-recovery argument (public domain knowledge; no text copied). The
  world, every figure and every file are synthetic, generated by `generator/build.py` under seed 118.
- **Re-root:** architecture 4's call landed three times at the portal and its determinism block failed twice, with
  the field's own welfare method as the golden (the card's lineage says so). The cell handed out first
  (pharmacology benefit-risk, a pharmacist medication review) was screened and left; each screen is a line in
  `## Tried and rejected`.

## Survivor anatomy

Actor: the property that decides is how many consecutive days a programme had already been called when an hour came, and no file stores it; the event log lists dates, the measurement panels list event dates, and the run a day sits in is a relation between rows of the event log's calendar (a weekend or holiday ends it).
Link: the design peak hour's place in its run is read by applying OP-7's weekday 110F trigger to the resource adequacy plan's design year (the three weekdays before Friday 23 July clear it, the Monday before does not), and the record's own run positions by applying the calendar to the event log; no key, column or sentence ties the plan's peak hour to the procedure's trigger or the panels to a run.
Reflex: the field's method for the deciding quantity, a load impact evaluation's treatment-against-holdout reduction at the planning hour (ex post averaged over events, or ex ante from a weather model evaluated at the design hour), sits at rungs 0 and 1 and files Cool Credit.
Back-test: the textbook route validates: a weather model of each programme's 18:00 reduction fitted on the 2024 and 2025 events predicts the 2026 season's average event reduction within a few per cent for every programme, because 2026's events stand alone as often as the earlier years' did.
Second use: every file the decisive step reads is in the pack for its own reason: the event log is how every rung finds its event days, the design year is where every rung reads the peak hour's weather, OP-7 sets the event window and the 16:00 start every rung and ask A use, and the panels are every rung's data; deleting the decisive step drops no file.
Shock: the lower reductions on later days of a run spread across about a third of the record's events and look like the ordinary scatter a weather model leaves (the hottest event days carry both full and small reductions, no season or programme stands out, and the record's largest step, the batteries' 2024 setting, is explained by the contract).
Pins: the resource adequacy plan files the WHAT in its own accreditation chapter (expected reduction in the design year's system peak hour, operated as the 2027 procedures operate it, per enrolled unit, against the load the same units would draw undispatched, under the contracts in force), and no filed sentence names consecutive days, run position, recovery, fatigue or a buffer.

## Default path

1. Read the resource adequacy plan's accreditation chapter: each programme counts at its expected reduction in the
   system peak hour of the design year (Appendix B), per enrolled unit; find the peak hour in `design_year_2027.csv`
   (Friday 23 July 2027, the hour beginning 18:00, 115F, the day's high 117F).
2. For each programme take the 18:00 reduction per enrolled unit the way a load impact evaluation does: Cool Credit
   from the thermostat panel (treatment mean less holdout mean, converting the panel's UTC stamps to MST), Peak Time
   Rewards from the group means, Business Demand Partners from the verified site reductions, Home Battery Network from
   the fleet summary (2025 and 2026, under the 3.0 kW setting).
3. Ex post: average each over the 2024 to 2026 events. Ex ante: fit the reduction on the day's high (and the overnight
   low or the three days' heat before it) and read the fit at the design hour.
4. Multiply by the units the USD 3.2 million buys at the cost sheet's per-unit costs (12,307 thermostat premises,
   50,000 rebate customers, 133 sites, 2,133 batteries) and rank.

Ends on: Cool Credit, about 11 MW (10.4 MW ex ante at 117F; 9.5 MW with the heat build-up)
Golden: Home Battery Network, about 6 MW (Peak Time Rewards 4, Cool Credit 3, Business Demand Partners 2)

## Stump sentence

The default path reads each programme's 18:00 reduction as the load impact protocols do, averaged over the record's
events or matched to the design hour's 117F, and files Cool Credit at about 11 MW; it never places the design peak hour
in its run of dispatch days, so it misses that OP-7 calls every programme on the three weekdays before it and that on
the record's fourth consecutive event days the thermostats give about a fifth of a first day's reduction, which puts
Cool Credit at 3 MW behind the Home Battery Network's 6.

## Three rules

Task type: generation-capacity-planning in energy-systems-utilities, which serves opportunity sizing: a resource adequacy plan's accreditation of demand-side resources, sized from the units a budget buys to the load those units take off the design year's peak hour.

Domain test: the deciding quantity is each programme's expected load reduction per enrolled unit in the design year's system peak hour, the capacity-accreditation quantity a resource adequacy plan prices, estimated the way a load impact evaluation estimates it (the treatment-against-holdout difference at the planning hour in the measurement and verification record, read at the planning conditions).

Swap: "which surge scheme should a hospital fund, valued at the beds it frees on the design surge day" keeps the sentence's shape and loses its substance: a hospital has no weekday 110F dispatch trigger, no randomised holdout read at an hour, no battery recharged by rooftop solar between calls and no design-year peak hour, so the quantity and its estimate stop making sense.

Layer 1: the thermostat panel is stamped in UTC by Ridgeway's meter-data pull (the MST hour beginning 18:00 is 01:00 the next UTC day); Brightwell's 2024 dispatch setting was 2.0 kW per battery until the 2025 amendment raised it to 3.0 kW; Ridgeway keys the commercial verification by its own anonymised site keys; the rebate evaluation's group sizes change by season; Halvern's status log keeps changes only and its own address strings; Arroyo's invoices carry Arroyo's site references. Nothing is placed to be caught, and none of it moves the call.

Layer 2: allocation under a binding constraint: each depleting programme's response is drawn from a buffer (the cool a home banks, a customer's attention, a building's thermal mass and its operators' patience) that refills only on a day without a call, and the methodological choice that flips the call is to read each reduction in the state the design occasion forces, the fourth consecutive dispatch day, rather than at the record's average or weather-matched state.

Decisive step: place the design peak hour in its run of dispatch days (Friday 23 July 2027 is the fourth consecutive weekday OP-7 calls) and read each programme's per-unit reduction on the record's own fourth consecutive event days, rebuilt from the event log's calendar, which puts the Home Battery Network first.

Not semantics: every field, unit, code and definition read correctly (the UTC stamps converted, the 3.0 kW setting applied, the hour beginning 18:00 MST taken, the plan's peak hour found) still leaves the easy route on Cool Credit at 10 to 11 MW, because an occasion's place in a run is not a reading of any field: it is a state the analyst has to recognise the response depends on and rebuild from the calendar.

Not rule application: no filed rule or procedure says a reduction depends on earlier calls or tells the analyst to read it by run day, so executing the plan's accreditation sentence and OP-7's trigger correctly still files Cool Credit when the reduction is taken at its average or weather-matched level. The enumerated family (ex post average, ex ante on the day's high, on the high and overnight low, on the three days' heat before, the hottest event days, a day-after-an-event indicator, the run day as a linear count, run-day indicators, the fourth-day mean) spreads Cool Credit's figure from 3.0 to 11.4 MW and names Cool Credit six times and the Home Battery Network three; the standing family once the design hour sits in its run (run-day indicators with the day's high, the fourth-day mean, a ratio model on run days) spreads Cool Credit 3.0 to 3.1 MW and the batteries 6.0 to 6.2 MW and is unanimous on the call; what rules out the rest is loud on a cut by run day (the fourth days sit about 0.9 kW under any weather model) and silent on every weather cut.

Analyst test: a strong analyst who reads every field and rule correctly takes each programme's 18:00 reduction as the load impact protocols do, averaged over the 2024 to 2026 events or read off a weather model at the design hour's 117F, multiplies by the units the USD 3.2 million buys and files Cool Credit, about 11 MW; the design hour is the fourth consecutive dispatch day, where the thermostats give about a fifth of a first day's reduction, so Cool Credit adds about 3 MW and the Home Battery Network's 6 MW is the call.

Estimand: the resource adequacy plan's accreditation chapter (`ra_plan_2027_accreditation.pdf`, section 4.3) files it: a demand-side programme's 2027 accredited capacity is its expected load reduction in the system peak hour of the design year in Appendix B, operated as the procedures in force for 2027 operate it, measured against the load the same units would have drawn had the programme not been called, an added unit credited at the programme's expected reduction per enrolled unit under the contracts in force for 2027.

No decoy: nothing is planted to be caught: no memo, briefing, draft, vendor claim or stakeholder figure states a per-unit reduction, a ranking or a capacity value for any programme; the cost sheet carries costs only, and the batteries' 2024 setting is the contract's own history.

No certified replay: the method is not recovered by reproducing certified or published figures: no evaluation report, settlement statement or published table carries a reduction a solver could match, and the fourth-day reduction is read from raw panel rows.

Lesson: a demand-side resource's capacity at a multi-day design peak is its response in the state the earlier calls of the run leave it, so the record's average or weather-matched response overstates every programme whose buffer does not refill overnight; no build on file prices a resource at the run position a filed dispatch rule forces.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 ex post average of each programme's 18:00 reduction | the plan's "expected reduction" invites it | event rows carry the reduction's inputs | the field's ex post estimate | none | none | one group-by | none | readable |
| R1 ex ante weather model at the design hour (117F) | Appendix B's design weather invites it | the day's high is on every event row | the load impact protocols' ex ante method | none | none | one fit | none | readable |
| R2 weather model with the overnight low and the three days' heat before | none | the design year carries the lows and earlier days | a seasoned evaluator's heat build-up terms | none | none | one fit | none | readable |
| R3 (decisive) the design hour placed in its run; reductions read on the record's fourth consecutive event days | silent: no sentence names consecutive days, run position, recovery or fatigue | silent: no run-day column, the event ids carry no run index | silent: the protocols condition on weather, not on the programme's own call history | silent: no file scores a run-day reading | silent: no duplicate, clock or key issue points at it | silent: the run is rebuilt from the calendar and crossed with the plan's peak day | silent: the event log, design year, OP-7 and the panels each serve every rung and the asks | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "system peak hour of the design year" | the hour beginning 18:00 MST on Friday 23 July 2027, the maximum of Appendix B's forecast load | the hour ending 18:00, or the hottest hour (16:00) | same call (the 16:00, 17:00 and 19:00 hours each name the Home Battery Network) | plan 4.3 and Appendix B's header ("hour beginning, MST"); asserted |
| SF2 | "operated as the procedures in force for 2027 operate it" | called on every weekday whose forecast high reaches 110F, so Tuesday to Friday of that week | a first-day event, or a schedule that saves the programme for the peak day | Cool Credit under the fresh reading | OP-7 section 3's trigger and plan 4.3's sentence; the design year's daily highs (108, 111, 113, 115, 117) |
| SF3 | the design year's forecast high | Appendix B's daily maximum, planned as forecast | a forecast-error band around it | same call | Appendix B's note that the design year is planned as forecast |
| SF4 | "expected load reduction" | the mean reduction | a low percentile read as firm capacity | the tenth percentile names Cool Credit (asserted) | plan 4.3's "expected" |
| SF5 | "per enrolled unit" | each panel's reduction over every enrolled unit, offline and opted-out units included | per responding unit | same call (asserted) | plan 4.3 and each file's enrolled denominators |
| SF6 | the units the budget buys | the whole units USD 3.2 million buys at the cost sheet's all-in cost per added unit | a fractional quotient | same call | the cost sheet's "per added unit" and the budget line |
| SF7 | the battery setting | 3.0 kW per battery, the 2025 amendment | the 2.0 kW setting, or the 2024 to 2026 mean | same call (asserted under both) | plan 4.3's "contracts in force for 2027" and Brightwell's amendment |
| SF8 | the comparison | the holdout or control load, the verified baseline, the battery's own discharge | a pre-event baseline | same call | plan 4.3's "load the same units would have drawn had the programme not been called" |
| SF9 | the panel clock | `interval_start_utc` converted to MST (UTC less seven hours) | UTC read as local | no call (no reduction at 11:00) | the column name and the plan's MST convention |
| SF10 | a run of event days | consecutive calendar days with an event; a weekend, holiday or uncalled day ends it | the event log's order with calendar gaps ignored | same call: the record holds no Friday-and-Monday pair, so both give the same run days (asserted) | C1 by construction |
| SF11 | the fourth-day estimator | the mean over the record's fourth consecutive event days | run-day indicators with the day's high, a ratio model | same call; every figure in its whole-megawatt bin (asserted) | C1, asserted |
| SF12 | the commercial unit | verified reduction per enrolled site at 18:00 | per dispatched site | same call (asserted) | the verification file's enrolled-site rows |
| SF13 | the rebate unit | control mean less treatment mean per enrolled customer | per notified customer | same call | the evaluation file's group definitions |
| SF14 | the hour column in the rebate and commercial files | hour beginning MST | hour ending | same call (asserted) | each file's header |

## Ladder

Four rungs, each a whole analysis a competent analyst could stop at, each naming its own figure; the figures are the
generator's (`generator/figures.json`, `ladder` block), printed here at design time from the clean truth.

| Rung | Construction | Cool Credit | Peak Time Rewards | Business Demand Partners | Home Battery Network | Winner, lead | Batteries' place |
|---|---|---|---|---|---|---|---|
| R0 | ex post: each programme's 18:00 reduction averaged over the 2024 to 2026 events | 11.4 | 8.6 | 6.1 | 5.5 | Cool Credit, 1.34 | 4th |
| R1 | ex ante: a model on the day's high read at 117F (batteries on the 3.0 kW setting) | 10.4 | 8.1 | 5.5 | 6.2 | Cool Credit, 1.28 | 3rd |
| R2 | ex ante with the overnight low and the three days' heat before (the design hour's 90F and 113F) | 9.7 | 7.7 | 5.2 | 6.2 | Cool Credit, 1.25 | 3rd |
| R3 (decisive) | the design hour placed on its run's fourth day; reductions on the record's fourth consecutive event days | 3.0 | 4.1 | 2.1 | 6.0 to 6.2 | Home Battery Network, 1.47 | 1st |

- **What kills each rung:** R0 dies to the plan's estimand (the design year's peak hour, not an average event); R1 to
  the design hour's place in its run (OP-7's trigger on Appendix B's week) and the record's fourth days; R2 to the
  Mondays after hot weekends, fresh event days with the heat build-up and hot nights of a fourth day that give a first
  day's full reduction, so the weather history is not what lowers a reduction; R3 is the golden.
- **Separation and position:** the batteries are 4th on R0, never first on an intermediate rung and never second;
  every rung's lead is 1.24 or more; the final lead over the runner-up is 1.47 (Peak Time Rewards), 2.0 over Cool
  Credit.
- **Dominance:** the decisive step moves Cool Credit against the batteries by a factor of about 4.2 (11.4 against 5.5
  on R0, 3.0 against 6.2 on R3) against Cool Credit's carried advantage of 2.07, and moves Peak Time Rewards by 2.3
  against its carried 1.55; both clear 1.2 times the carried advantage.
- **The reflex sweep, as code on the clean truth (`checks.py`):** every route that never reads run position files Cool
  Credit: ex post, ex ante on the high, on the high and the low, on the heat build-up, on all three, the hottest event
  days (115F and over), a day-after-an-event indicator (7.5 against 6.8), the tenth percentile (6.0 against 6.0 and
  5.8). The routes that read run position file the Home Battery Network: run-day indicators with the high, the
  fourth-day mean, a ratio model, a linear run-day count.
- **Pricing sequence:** (1) the residue the filed WHAT leaves is a method (how to estimate the expected reduction at
  the design hour's state), not a knob; (2) the move needed is Cool Credit from 10.4 to under 6.2 MW, and the affected
  population (the fourth days) can carry it to 3.0; (3) the one-group-by route to the call is "reductions by run day"
  once the run is rebuilt, and the run day is in no file, so the group-by needs the calendar construction first; (4)
  the fourth-day estimate's standard error is about 0.02 kW per thermostat premise (0.25 MW at 12,307 premises) and
  0.004 kW per rebate customer (0.2 MW), each a fraction of its whole-megawatt bin; (5) the lever (run position) is
  not the ranked quantity's noise; the call is a verdict on one named programme 1.8 MW, about seven standard errors,
  clear of the runner-up; (6) not a change call; (7) no subset is recovered exactly; (8) the reflex sweep above, with
  run position residualised against the visible attributes (correlation with the day's high 0.35, with the overnight
  low 0.03, with the three days' heat 0.48, none of them able to carry the call).
- **Grid:** the four candidates under every construction above; every cell names Cool Credit except the run-position
  family's, which names the batteries; no cell names Peak Time Rewards or Business Demand Partners.
- **Worth:** the decisive step is worth 7.4 MW on Cool Credit's figure (10.4 to 3.0), against the standing family's
  spread of 0.1 MW and the sampling interval of 0.5 MW.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the programmes' enrolled units; the expansion's added units counted at the enrolled units' expected reduction | plan 4.3 files it; C1 |
| 2 | Unit of account | an enrolled premise, customer, site or battery | plan 4.3 and the cost sheet's "per added unit" |
| 3 | Attribution window | the design year's system peak hour, the hour beginning 18:00 MST on 23 July 2027 | plan 4.3 and Appendix B; SF1 asserted |
| 4 | As-of dating | the 2027 procedures and contracts in force | plan 4.3; SF2, SF7 |
| 5 | Version basis | the 2025 battery amendment in force for 2027 | plan 4.3 "contracts in force"; SF7 asserted |
| 6 | Denominator | every enrolled unit, offline and opted-out included | each file's enrolled denominators; SF5 asserted |
| 7 | Weighting | each fourth-day reduction weighted by its event, the panels' own group means within an event | C1: weighting by event or by premise-hour gives the same call and bins (asserted) |
| 8 | Window length | the 2024 to 2026 record (2025 and 2026 for the batteries under the setting in force) | C1 across the three seasons and the last two (asserted) |
| 9 | Boundary inclusivity | the 110F trigger at "reaches 110F"; no design day sits within 1F of it | C1: the design week's highs are 108, 111, 113, 115, 117 |
| 10 | Rounding path | megawatts rounded once, from the unrounded per-unit reduction times units | the prompt's rounding sentence; asserted mid-bin |
| 11 | Tie-break | none needed: the call leads by 1.47 | n/a, asserted |
| 12 | Maturity and censoring | the 2026 season closed on 30 September; every event complete | C1 |
| 13 | Order of operations | per-unit reduction then units then rounding | asserted equal under both orders of averaging |
| 14 | Row order | none of the constructions depends on file order | asserted over a shuffle |
| 15 | Duplicate resolution | no duplicate rows on the main path | asserted by count |
| 16 | Identity normalisation | the panels' anonymised keys are consistent within a season | asserted |
| 17 | Netting against gross | a pre-cooling increase before 16:00 does not net against the 18:00 reduction | the plan's single hour; asserted |
| 18 | Dimensional units | kW per unit to MW for the programme, kWh per hour as kW | each file's units in its header |
| 19 | Code and status semantics | the event log's event type (system events only on the main path) | the log's own type column; asserted |
| 20 | Integerisation | whole units bought, the floor of budget over cost | SF6; same call |
| 21 | Clause scope | plan 4.3 governs demand-side programmes only | the chapter's own scope line |
| 22 | Forward window contents | the design year's weather and load are Appendix B's, shipped | `design_year_2027.csv` |

## Literal reader

Executed word for word, the plan's 4.3 names the design year's peak hour (Appendix B, the hour beginning 18:00 MST on
Friday 23 July 2027), operation under OP-7 (called on the four weekdays from Tuesday 20 July, the Monday at 108F
uncalled), the comparison against the units' own uncalled load, per enrolled unit under the 3.0 kW battery setting;
every literal reading of those sentences gives the golden (SF1 to SF14 asserted), and the easy answer comes from an
easy method on the same estimand (the reduction averaged or weather-matched), never from another reading.

## Oracles

none on the main call: no file carries a per-unit reduction, a capacity value or a ranking for any programme; the
evaluation files carry raw rows and group means only, the cost sheet carries costs only, and the battery fleet summary
ties to no other shipped total. On the ask side, Halvern's acknowledgements tie to no count (they cover dispatched
devices only, and the holdout is never dispatched), and Brightwell's records tie to no shipped total.

## Ask sheet

Three asks, each on files the main call never reads and each rebuilt by a reconstruction no sentence states. The
figures are the generator's (`generator/figures.json`, `asks` block); stops and deltas are asserted in `checks.py`.

**Ask A, Cool Credit premises online at 16:00 on each 2026 event day (17 figures, counts).**
- H18 home: the thermostat programme's dispatchable base on each event day, an audit trail of the enrolment the
  programme's per-unit reduction is read over; every programme carries such a base and the call does not turn on it.
- Files and columns: `cool_credit_enrolments_cis.csv` (premise, address, enrolled serial, enrolled and unenrolled
  dates), `halvern_device_registry.csv` (serial, install address, registered and retired), `halvern_status_log_2026.csv`
  (serial, status, UTC change time; changes only), `halvern_dispatch_acks_2025_2026.csv` (event date, serial, UTC ack
  time); ten columns on the golden's path.
- Primary 1 (D7, the true key elsewhere): a premise whose thermostat was replaced keeps the enrolled serial in the
  CIS, retired in Halvern's registry, and the replacement is registered under Halvern's install-address string, which
  writes the address its own way; the premise is online through the new serial.
- Primary 2 (D2, a label stored before a silent switch): Halvern's `IDLE` meant a sleeping radio until the 6.0
  firmware push of 6 July 2026 and from then means connected with no cooling call; no field dates the switch, and the
  acknowledgements show idle devices acknowledging dispatch only from 6 July.
- Hazards: the change-only log (state rebuilt at 23:00 UTC), UTC stamps, premises with two thermostats (counted once),
  unenrolments.
- Pin test: the sentence pins enrolled premises, a thermostat online and 16:00 on each 2026 event day; both primaries
  sit in which serial is the premise's and what a status meant that day, dimensions the pins leave open.

**Ask B, Home Battery Network incentive owed for each 2026 event month and the premises at the season cap (5 figures).**
- H18 home: the battery programme's operating cost in 2026, a measure every programme carries that the call does not
  turn on.
- Files and columns: `brightwell_dispatch_records_2026.csv` (record, enrolment number, battery serial, UTC start and
  end, delivered kWh, settled on), `hbn_participation_agreement.pdf` schedule 2 (USD 15 for each event in which the
  battery discharged at its dispatch setting through at least three of the four event hours; USD 180 a premise a
  season), `battery_interconnection_register.csv` (premise, battery serial, enrolment number).
- Primary 1 (D6, an event's dispatch split across records): a dispatch interrupted by a communications drop and
  resumed is two records for one battery and event, neither three hours long; together they qualify.
- Primary 2 (D8, a recorded date for the event date): Brightwell's `settled_on` is the day its settlement run read the
  record, a day or more after the event, so month-end events settle in the next month; the event month is the MST
  date of the dispatch.
- Hazards: UTC stamps, a re-sent batch (exact copies), two batteries at one premise sharing one cap.

**Ask C, Business Demand Partners kW nominated inside CBMU's territory for each 2026 month (4 figures).**
- H18 home: the commercial programme's contracted capacity in 2026, the base its per-site reduction is credited over.
- Files and columns: `arroyo_nominations_2026.csv` (month, Arroyo site reference, site name, service address, meter
  number, nominated kW), `cbmu_meter_register.csv` (meter number, premise, service address).
- Primary 1 (D5, out-of-scope rows known only by structure): from August Arroyo's file carries its sites on the
  neighbouring utility's system, whose meter numbers follow that utility's nine-digit scheme and match no CBMU meter.
- Primary 2 (D1, one site under two references): a site that changed owner is listed under its old and its new
  reference in the month of the change, the same meter, a re-typed name.
- Hazard: nominations restated within a month (the later row stands).

**Main population zero-counts (asserted):** no ask device row sits in the four main-call evaluation files, the event
log, the cost sheet, the plan or OP-7.

**Hazards and per-ask deltas:** stated in `checks.py` and printed by `generator/ceiling.py` on the cut pack.

**Referee:** none; each ask is forced by its own records.

| Ask figures | Cracker (lands the call, runs the battery, executes every filed rule) | Mirror (stops at R2) | Verdict |
|---|---|---|---|
| A, 17 event-day counts | joins the CIS serial and reads `IDLE` one way all season | the same | miss |
| B, 4 months and the cap count | tests each record alone; months by the dispatch date | the same | miss |
| C, 4 months | keeps the neighbouring utility's sites; counts the transition month's two references | the same | miss |

Pair ceiling: to be measured by `generator/ceiling.py` on the cut pack (design target 45 and 12, pair 28.5).
Mirror leakage: to be measured (design target 0 per cent of ask weight).
Measured by: generator/ceiling.py

## Tried and rejected

- The note's own decisive rung, shrunk lift times platform-drawn clicks (pattern C, gap objective, decomposition_attribution): blocked at the draw by ban.pattern C against task116, test.same_puzzle_older against six builds and test.same_driver_older against task38 v3, and its driver (a reachable share of each candidate's magnitude certified by closed interventions) is task38 v3's and task28 v2's, so it can sit at rung 3 but cannot carry the stump.
- A G7 operating-window rung (a winner earns only on platform clicks after its fixed test window closes, invisible to the evergreen app-exclusive embeddings): blocked by test.same_puzzle (time, G7, pick_one_of_n) against task105 v1, a timing driver the portal already solved, and an in-window same_puzzle takes no differentiation.
- Grading every desk's four chain stages as requested figures (the draw's 24 chain criteria): the rung-3 mirror keeps the platform-clicks and lift stages (12 of 24) and the cracker all 24, so the one-cracker pair sits near 50 before any device ask; only the terminal stage is requested.
- The note's ask B, newsletter click-to-open with privacy-proxy opens: fails H18, because a person could act on it with the squad call unmade; its export ships as a distractor.
- The note's ask C as written, each desk's clicks under each of the four rung bases: names the ladder in the prompt and hands the mirror the shallow cells; only its back-test count survives.
- A workload ask (headlines a week the squad would test) and extra clicks per article: the workload puts each desk's article count beside its test count and nudges toward the netting; a per-article figure at whole-click precision inherits up to 1% of admissible shrinkage spread and cannot be binned.
- The committed figure to the nearest 10,000, the note's rounding: method of moments and maximum likelihood move Culture's figure by up to about 12,500 clicks, more than half a 10,000 bin; every click figure goes to 50,000.
- Matched squad-run and desk-run tests to close what the squad adds on a desk-tested headline: a closed embedding at a self-testing desk would let the change log see the netting and break its blindness, and squad loan tests at a shortlisted desk would blur who ran the tests; closed by construction instead.
- The advertising value of the extra clicks as a both-layer ask: at publisher yields the best desk's gain is worth tens of thousands of dollars against a six-person squad, which raises whether the squad should exist at all.
- A Culture·metro desk inside the Culture vertical to keep the dashboard-plus-netting cell off Culture: read as lift alone, the editor-in-chief's basis then names Local·metro; Politics·metro's raw lift at 8.3% keeps both readings of that basis on Politics·national and clears the cell.
- Method of moments as the golden prior: Sport·metro's and Politics·metro's tiny packages (about 120 clicks) bias the unweighted moments (mean -0.82% against -1.04% by maximum likelihood), Culture's figure moved 3.2% (out of its bin margin) and maximum likelihood failed the back-test 0 of 7; the golden became maximum likelihood, with DerSimonian-Laird convergent and method of moments refuted on the corpus.
- Raising the two small metro desks to about 350 clicks per package so the moment fits agree: the raw-lift netting cell then needs Sport·metro's rung-4 figure near 300,000, which the remaining spread between estimators cannot hold mid-bin, and rung 1 needs a 130M-click Sport·metro.
- Shipping the leader with no gate on the Brisbane instance: Local·metro ships 79% of its tests, its won-only share of platform clicks reaches 0.58 and the won-only netting cell names Culture at 1.07x; the Brisbane gate is 80 per cent (z above 0.84).
- Culture at 2,900 clicks per package (factor 0.70, raw 2.6%) with the gated Brisbane instance: the dashboard-plus-netting cell named Culture at 1.10x; Culture's tests lengthened (factor 0.80) and Politics·metro given 210 shorter tests.
- The design's lifts under one true-lift distribution: Sport·metro at 11% raw cannot keep a 3.08% shrunk lift, and the squad's raw lifts of 3.0% to 7.9% are out of reach through a 95% gate; built at 10.8% / 0.39% and 2.7% to 3.7%, with every ladder margin held through the solved planned clicks.
- The ask layer as designed (S1, S2, HZ1 to HZ4): with the export notes' and the standards policy's rules executed per document, the national desks' correction counts, rates and medians were all right and the pair simulated at 53.6; HZ5 (the migration's carried documents) brings the same reading to 38.0.
- Panel section codes reissued in alphabetical order: the careless join moved readers but left extra per reader in its bin at most desks; codes re-cut so the careless months read a section of very different size.
- Test sizes drawn independently of article size: 561 tests carried more clicks than their article's first-two-hours platform pageviews; tested-article sizes compressed and given an earlier platform profile, and the squad's in-window tests placed on enlarged lead items.
- The ask layer as shipped at stage 3 (S1, S2, HZ1 to HZ5, R1, HZ2, HZ3), round 1 plain solver: it missed the call at rung 3 exactly as the stump sentence says (Local·metro 2,800,000, runner-up Business·national) but scored 46.0 because it kept every device figure, readers, headline corrections, rate per 1,000 and median minutes at all six desks plus the back-test, by executing the filed rules per document in its own words: "merged documents recreated by the 14 Nov 2025 Brisbane restore into their originals. Dropped the 1,704 documents migrated from the old CMS", "a headline correction is a revision that adds a new correction note and changes headline_sha1, following standards s7.4. Notes copied forward to later revisions ... were not counted again", "Mapped section codes to desks through the Section history sheet ... using R26-07B's restated April to June 2026"; every primary and hazard falls to a field or a filed rule the solver reads, so device leakage is near 1.0 against the 0.10 the pair arithmetic needs. It also named rung 4 and declined it ("I also did not net off the testing the web desks already do themselves"), so the rung is visible though not taken.
- Hardening loop 1, the principle under the stage-3 ask layer: every primary and hazard adjudicated by a field or a filed rule on the ask's own path (the copied-note line, s7.4 with `headline_sha1`, `restored_from_doc`, `migrated_from`, `doc_type`, the section history's dates, the R26-07B release note), with two free confirmations beside them, the spine's per-desk article counts and the bulletin's March figures. A solver that reads every field executes each rule per document and then checks itself twice, in its own words "Story and live-blog counts match the article counts in the pageview data exactly" and "March 2026 (AEST) has 12 headline and 31 text corrections, matching the April standards bulletin exactly", so those devices stay only as hazards and the primaries move to constructions no field names: which revision published the headline, when a scheduled article went live, an entry's headline corrected under its live blog's note, and which section list a history release was issued on.
- Hardening loop 1's ask layer (primaries moved to which revision published the headline, scheduled go-live, live-blog entry headlines under the blog's note, and the section list a release was issued on), round 1 re-run as "round 2, plain" (38.0, main call missed at rung 3 on Local·metro 2,800,000 against Business·national 1,750,000): the round passes, but on the rung-3 extra-clicks tokens alone, because the solver again kept readers, headline corrections, rate per 1,000 and median minutes at all six desks plus the back-test, executing every new primary in its own words ("Go-live = first live save, or publish_at for a schedule that fired", "For live blogs, a note added to the blog in the same minute as a post headline change also counts", "Section codes are mapped by the taxonomy of the release ... including R26-04H") and confirming against the bulletin's March figures; device leakage stays near 1.0, so a solver that takes rung 4 keeps the whole xlsx row and the ask layer cannot hold the pair at round 2. It joined `owner_staff_id` to the staff list and saw every web test was desk-run, then declined the netting ("The files do not say whether a squad embedding adds to or replaces a desk's own testing"), so rung 4 is seen and refused, not silent.
- Round 3 (plain and skeptic together) on the hardening-loop ask layer: both missed the call at rung 3 on Local·metro (plain 2,800,000, skeptic 2,400,000 after re-applying the squad's 95% ship rule to every desk, runner-up Business·national 1,750,000 in both), proxies 46.5 and 36.8, average 41.65 with neither under 25, so the round does not pass. Neither path mentions `owner_staff_id` or the staff list this time, so rung 4 was silent and held. The asks did not: both kept readers at all six desks by catching R-back ("mapped section codes by release taxonomy ... 2026 codes for R26-04 onward, including the history release"), the skeptic kept every headline correction count and rate by catching K-auto, K-entry and M1 together ("Built the published sequence ... scheduled revisions at publish_at only if no later save came first ... plus live-blog entry notes matched to a post headline change in the same minute (16)"), the plain solver all but Local·metro's, and both kept the 7 of 7 back-test; only the medians held (timed from the entry going live rather than the blog), and the plain solver's notes list five of the six golden medians as its alternative. Device leakage stays near 1.0 for the second consecutive round, which under the Stopping rule re-roots the ask layer rather than adding a fifth primary.
- Hardening loop 2, the principle under hardening loop 1's ask layer: primaries that were constructions no field names (which revision published the headline, scheduled go-live, an entry's headline fixed under its blog's note in the same minute, the section list a history release was issued on), each still adjudicated by a sentence on the ask's own path that names its own construction (the status line, policy 7.4 and 7.5, the `publish_at` and `doc_type` lines, the R26-04H note "rerun on the 2026 content taxonomy"). A solver that reads every field note writes the construction from the sentence, in round 3's own words "Built the published sequence (live saves at saved_at; scheduled revisions at publish_at only if no later save came first ...) ... plus live-blog entry notes matched to a post headline change in the same minute (16)" and "mapped section codes by release taxonomy (old 2024 codes only for the R25-11 Oct 2025 release; 2026 codes for R26-04 onward, including the history release)", then confirms itself on the bulletin's March figures and the spine's article counts, so readers, counts and rates leaked at 5 or 6 of 6 for the second round running; the medians held only because both solvers timed an entry's fix from the entry going live rather than the blog, a reading choice and not a device. What dies is the organ that states its construction; what the round shows untouched is every assumption the solvers' own path makes and never checks: that a note and the headline fix it records arrive on one save (or one minute), and that the latest release per period is the record for every section in it.
- Update notices in the note field (a developing story's "This story has been updated ..." line saved with a headline change, excluded by 7.2): rejected on paper at hardening loop 2, because the notices form a visible family in any scan of the note texts and 7.2 already names updates, so a solver who lists note openings executes the exclusion; the note that follows its fix was taken instead, whose rows read like every other correction.
- A backdated `publish_at` for the medians (a scheduled revision saved after its own publish time): rejected on paper at hardening loop 2, because whether the CMS publishes at the save, at its next run or not at all needs a filed rule, and a filed rule on the field-notes path is executed.
- Readers devices that need a new sentence in the panel workbook (unique browsers on the Brisbane site, three-month rolling regional estimates, units set by agreement, an experimental release that does not replace the standard series): each needs a conversion nothing pins or a note the solver reads and executes; only a structure the release rows carry themselves (which sections a supplementary release reruns or restates) survived.
- The first lag sub-seeds left round 3's path on the golden median at Local·metro and Culture·national, and two partial readings on Culture's: a median moves only if the fix-then-note corrections sit around the median article, so each desk's lag stream was searched until all eleven readings miss every median (Local·metro's nearest by 15 minutes and Culture·national's by 19; the thinnest misses are Business·national's 88 against 89 and Sport·national's 45 against 47).
- R-part as the readers primary (supplementary releases carrying only the sections they rerun or restate), round 5 plain and skeptic: both solvers kept the latest release per period and section and reproduced all six readers, in the plain solver's words "kept the latest release for each period and desk (R26-04H for Nov 2025 to Feb 2026 BLN; R26-07B for Apr to Jun 2026 BLB)", because a per-section latest-release rule is what a careful solver writes by default and the partial release does not punish it; with the readers block leaking at 6 of 6 in every round since stage 3, the plain solver keeps enough ask weight to sit at 43.9 and no response reaches 25.
- K-lag as the corrections primary (a headline note on the save after the fix it records, and an entry's fix with its blog's note minutes later), round 5 plain and skeptic: both solvers paired a note with the headline published just before it, in the plain solver's words "A note counts as a headline correction if the live headline changes on the revision that publishes it, or if it is a headline-worded note whose headline changed live up to 10 minutes earlier. For a live-blog entry, it counts if the entry's headline changed live within 10 minutes" and the skeptic's "Also counted: notes that name the headline and follow a just-published headline change by 0 to 9 minutes, and live-blog notes paired with an entry whose headline changed", because a note that names the headline on a save that leaves the headline alone sends a careful reader to the save before it; the counts then sat 0 to 3 off the golden for the plain solver (Sport·metro's 18, 7.3 and 55 kept whole) and 1 to 7 off for the skeptic, so the block held on older hazards by a few corrections a desk, not on the primary, and K-lag is spent as a primary.
- Readers devices weighed on paper at hardening loop 3 and dropped: a desk's section split into content groups with a deduplicated total the audience team never mapped, because a mapping of the parts without the whole reads as planted and two or three rows a desk a month is a symptom the hygiene battery finds.
- A January rerun issued on the 2026 list with no taxonomy note: it fails only solvers who map codes by month (round 5's plain solver mapped by release), and the national sections a misread swaps differ in size by 25 to 180 per cent, a spike any monthly look shows.
- A supplementary release coded after the first month it replaces, so that code order and publication order disagree: the release notes say what each release replaces, and round 5's solvers applied the notes rather than a sort.
- An unlisted parallel-run delivery left in the panel export: setting it aside needs a sentence that names it, which a careful solver executes, and without one the record leaves its status undetermined; the July file's repeat of figures a filed restatement replaced was taken instead, decided by the release log's months and by the repeated figures themselves.
- The July file's repeat with the restatement as an overcount (a 4.5 per cent duplication fault, the first figures high): round 1's readers path cancelled back onto Culture·national's golden (the history release's lower 2024-basis figures against the repeat's higher ones) and per month and code fell inside half a per cent there; with an undercount every readers mishandling at Politics·national and Culture·national errs low, and every naive readers stop moves all six desks.
- Taking a per-reader figure from the cracker through the July file: a silent repeat (a 7 per cent undercount over three months) moves readers under 2 per cent and no one-decimal per-reader figure with it, and moving one needs readers 3 per cent low at Local·metro or 4.3 per cent high at Culture·national, a plateau any monthly look shows; tuning a golden readers figure toward its bin edge so the repeat could take one was rejected as moving a graded answer for the device's sake, so the one-cracker pair sits at the layer's floor, 40.6.
- Corrections devices weighed at hardening loop 3 and dropped: a longer gap between a fix and its note (10 to 45 minutes), which lives in the population round 5's solvers already examined and fails only a window choice; and a correction logged on a corrections page, which needs a filed rule naming the page that a careful solver executes.
- The first note-first and put-back sub-seeds: Local·metro's round-5 reading netted back to the golden count (two notes before their fix against two put back) and Culture·national drew no note-first case, so each desk's sub-seeds were searched until every partial reading missed every count and median (Business·national's at the 48th note-first seed).
- The loop-3 ask layer (R-echo for readers, note-first and put-back sub-seeds for corrections), round 7 plain and skeptic: both kept readers at 6 of 6 by reading the release log's scope per period (the skeptic: "each period took only the release the release log lists for it ... I ignored R26-08's stale reload of Apr to Jun"), and both kept counts and rates at 6 of 6 by pairing a new note with a headline change within 10 or 15 minutes either side and checking it on the bulletin's March figures; the skeptic kept all six medians ("Minutes to first headline correction run from go-live to the live save that published the corrected headline", with the live blog as the article), so R-echo and the note-first and put-back sub-seeds are spent as primaries and the medians are the only device left that a reading choice decides.
- Stage 6 fix cycle 1, closing the judge's residual entry-pairing fork (a live blog's note paired with an entry headline changed 21, 22 and 59 minutes after it under a symmetric 30 to 60 minute window, Sport·national 43 and Politics·national 48) by widening the generator's entry guard to the hour after every blog note: it would flip three ordinary entry updates in the CMS export, which is regenerating measurement data (a SEND_BACK-class change under judge v3 that the solver rounds' supplementary results would not survive), so the fork is closed instead by one line in the CMS field notes, a data-dictionary pin that only fixes what the correct count is and also rules out pairing a note with a headline change hours away.
- Stage 6 fix cycle 2, restating critical components 1 and 4 at a coarser rounding (1.8% and 70,000,000) so admissible variants cannot move them: a prior on the web engine's packages only, which the change log cannot refute (7 of 7, worst 1.90%), puts Culture·national's lift at 1.7746% (1.77%), and the in-window corridor variants put its untested platform clicks at 70,138,602 (pre-window articles left out) or 69,790,626 (7-day-and-older clicks left out). Rejected: every graded ask figure, the call and the back-test count converge under all three, every solver round fitted its prior on all 10,111 packages and kept the base whole, the judge reproduced 1.78% and 70,300,000 twice, and coarsening breaks the golden paper's reproducible line (70,300,000 at 1.78% is 1,250,000); pinning the prior's population in a filed document instead would put the estimator on a main-path file, which the method must not have. Recorded in the fork grid and the 22-axis table instead.
- Stage 6 fix cycle 2, the verifier's first read of the stored-headline surfaces checked the `canonical_headline` row but still took its platform classes from a fixed list, so its figures did not depend on the row: run on the unpinned fix-cycle-1 pack it failed only the row check and reproduced the call. The classes now come from the row itself (a source code carries the stored headline when the row names its surface), and the same control fails the call figure, the runner-up and every desk's extra clicks.
- Stage 6 fix cycle 3, redrawing the staff list's 201 non-persona names with `guard.py names --geo Australia --seed 118` as the judge's third report suggests: the installed Faker carries no en_AU person provider, so the en_AU locale falls back to en_US's pools and the draw reproduces the very skew the judge flagged (33 of its 201 surnames sit in Faker's es_ES or es_MX pools and in none of its British, Irish or New Zealand ones: Carrillo, Molina, Hernandez, Garza, Figueroa, Garcia and on; lowercase Mcdonald, Mcdowell and Mccarty; US first names such as Caleb, Bryan, Kelsey and Zachary), and `suggest_people` also refuses any surname used in any build and any surname repeated within the list, which a 207-row newsroom list should not look like. The six personas stay as drawn for the card; the staff rows are drawn instead from Faker's own en_NZ, en_GB and en_IE pools with romanized zh_CN, de-accented vi_VN, en_IN and de_DE surnames mixed in, seeded, with Mc, Mac and O' recased. it_IT was in the first mix and was dropped: its surname list is drawn from notable Italians (the first draw gave "Viridiana Berlusconi"). The second draw still gave "Peter Murdoch" in a news publisher's staff list, so Murdoch, Packer, Fairfax and Stokes are filtered as media-dynasty surnames, with en_IE's misspelt "O'Loughlinn".
- Stage 6 fix cycle 3, loosening the change log's fit, which the judge's third report reads as fitted (realised clicks within 1.2% of shrunk lift x planned clicks in all seven years), by widening the realised noise toward the 2% bound: the admissible fits already spread to 1.90% on the worst embedding (the web-engine prior, which the corpus cannot refute) against the golden's 1.16%, so the margin that keeps every admissible fit on 7 of 7 is 0.10 point, and any widening spends it and turns the graded back-test count into a fork between two admissible priors; it would also recut calibration data every solver round read. The tight fit stays, because the 2% back-test needs it; the judge's own report says as much.
- The change log as planned and realised clicks (wave-1 redesign): every closed embedding sat at an app desk where the platform share and the untested share are both 1.000, so rung 3's construction reproduced all seven realised gains and only the forward desks broke it, the validated decoy the guard now blocks; the log records the realised holdback lift instead, which selects the estimator and says nothing about the click base.
- The brief's line that the editor-in-chief's office reviews placement on the dashboard's average winning lift by vertical (wave-1 redesign): a filed basis whose literal reading gives another answer, an official decoy; cut, with the dashboard export kept as the declared wrong-basis distractor.
- The thread's four beliefs (readers, "a winner is a winner", Business like Puzzles, the dashboard view) (wave-1 redesign): a roll call handing a solver one rung to refute per voice; only the head of audience's belief stays.
- The per-desk extra clicks, the chart walk and the back-test count as asks (wave-1 redesign): the call's construction, which a response on the call keeps whole (12 of 42 criteria free); the chain stays in the golden, unrequested.
- Extra clicks per reader as an ask (wave-1 redesign): no silent readers shift moves a one-decimal per-reader figure (Local·metro's would need readers 3 per cent low), so a response on the call kept all six whatever the readers device did, and the figure tied the readers device to the call.
- The headline-correction count and rate as asks (wave-1 redesign): every corrections device is adjudicated by a filed line (policy 7.4 and 7.5, the field notes' ten-minute pairing and put-back lines), so a response that executes the filed rules keeps all twelve figures.
- The July file's repeat with the release log's months shipped (R-echo as built at hardening loop 3): round 6's solver set the rows aside from the months column ("the release log scopes R26-08 to Jul only"); the column is gone, so only the restatement's note and the repeated figures find the rows.
- `publish_at` in UTC beside a field-notes line naming its clock (M1 as built at hardening loop 1): a filed scheduling rule every solve executed; `publish_at` now carries the editor's Brisbane wall-clock time with no zone line, and only the record's own inconsistency on the saves' clock finds it.
- Sport·metro's lag draw 50 and Business·national's note-first draw 47 (the loop-3 draws, wave-1 redesign): with `publish_at` read on UTC, the round-3 path and the lag-blind reading landed back on Sport·metro's golden median and the note-first-blind reading on Business·national's; redrawn to 218 and 102, where every corrections reading on either clock misses every median and every structural assertion holds (Sport·metro's draw 53 passed the medians but put half its own fixes on a lagged note and left one note-first fix).
- Realised holdback lifts to two decimals of a per cent (wave-1 redesign): the smallest realised lift (0.70%) carried a rounding error near 0.7 per cent, which pushed the convergent web-engine prior to 5 of 7 (worst 2.50%); three decimals restore 7 of 7.
- Visits left wherever the draw put them (wave-1 redesign): Culture·national's average sat 67 visits from its rounding edge; the September release, which nothing restates, now absorbs each section's remainder so every average sits at least 150 inside its thousand.
- The brief's counting phrase "counted at the owning desk on every click an article earns from publication, the hours its headline is under test included" (wave-1 redesign, stage 4): the isolated reader executed "every click" as an all-sources click base for the lift, a main-call fork against the field reference's stored-headline surfaces; the brief now says "counted at the owning desk from each article's publication, the hours its headline is under test included", which pins the period and names no click base.
- Related links classed as Bightline surfaces only by their absence from the `canonical_headline` list (wave-1 redesign, judge pass 2): read the other way the call figure is 1,050,000 with the same desks; the `related_links` row now says the links show each linked article's current headline.
- Architecture 1, the headlines each desk's own editors already test netted out of the squad's gain (2026-10-27, portal
  FAILED_TO_STUMP): both responses kept the clicks from Bightline's own surfaces, dropped the articles a desk had already
  tested and filed Culture·national at 1,250,000; the netting reads as a filter anyone applies (a tested headline cannot be
  tested again), and the shrinkage that the change log selects moved the figure, never the desk. The resume line had
  already measured it: own surfaces plus the drop plus distrust of Sport·metro's small-test mean reaches Culture·national
  with no shrinkage at all. Re-rooted onto what share of a shipped headline's clicks is new to the site.
- The corrections ask with every rule filed in the corrections standard (going live, the ten-minute pairing, a note put back, entries, restored copies) and no silent device (architecture 2, 2026-10-27): a response executing the filed rules kept all 18 cuts and the pair measured 60.5 on the readers device alone; an autosave of a live article's working copy now carries the article's status, live, typed `autosave`, so reading the status column alone moves 15 of the 18 cuts.
- Quartiles of minutes to the first correction (the draw's shape line, architecture 2): the 25th and 75th percentiles of 13 to 43 values differ by several minutes between inclusive, exclusive and nearest-rank methods, a percentile-method fork; counts within the hour and after more than three hours carry the same cuts determinately.
- A six-hour mark for the second count (architecture 2): 0 to 3 a desk, two desks at 0 and two at 1, so a constant response files a third of them; the mark moved to three hours (2 to 7 a desk), and every first correction sits at least three minutes clear of 60 and 180.
- Readers and visits per desk as graded figures (architecture 2's first cut, 2026-10-27): the July file's April to June rows repeat replaced figures byte for byte, which the battery's duplicate sweep finds unprompted (supplemental-stumping 1.1e), and with the release log silent on R26-08 the house judge's pass on that cut marked the reading open; the log's months, restored for determinism, make the readers block Layer 1 work every careful response lands, as it has 6 of 6 in every round since stage 3, and a cracker keeping it fails precut. No readers device both silent and forced by the record was found, so readers and visits leave the graded asks and the panel files ship as declared distractors.
- The autosave status as the corrections primary (architecture 2's final cut, determinism pass 6, 2026-10-27): NOT_DETERMINISTIC on the workbook asks alone, because no shipped file said what an autosave is and the status column on those saves reads live, so counting them as published versions was a defensible reading that moved three desks' cuts. Filed in the corrections standard 7.3 ("An autosave of an editor's working copy publishes nothing"), which makes the autosaves a hazard every careful response executes; the primary moved to a schedule set back to draft before its time, which the status column decides by itself (a draft at the time first set, a draft saved after it, no document ever set back to draft once live) and which the round-3 skeptic's own rule, a scheduled time only if no later save came first, already handles.
- The method left to the change log alone (architecture 2 as shipped, portal determinism return 2026-10-27): one judge passed it as analytical, the other read it as replay, the lift estimator and the share of a won click new to Bightline stated in no file and recoverable only by matching the seven embeddings, and filed the portal's off-call response as a competing answer, each desk's raw mean winning lift scaled by one factor fitted on the change log (0.3209), Sport·metro at 900,000 with Culture·national runner-up. Closed with a filed selection criterion at authority, not the method: the brief's sign-off (a working run unchanged on each closed embedding within 2 per cent of the lift and the extra clicks it realised against its holdback), which that route fails on both halves (0 of 7, 1 of 7) and which every passing working on the filed netting meets with the golden call, figure, runner-up and gap. The fork was not the stump: rungs 4 and 5 still end on Culture·national, and the sign-off says a working must pass, never what passes.
- The ask layer as shipped at that return (18 figures on one silent primary; the on-call response at 87, the pair at 65.5): the median and the two counts move only when a mishandled article crosses the middle or a mark, so a response that mishandles a few stories away from them keeps the figure, and a response that repairs the set-back schedules by reading the status at each scheduled time keeps every figure. The total minutes a desk's wrong headlines stood went beside the median, because every mishandled article moves it, and a second silent primary (a schedule moved to a later time and saved again, still scheduled, after the time first set) went under that repair. Neither moves a golden ask figure.
- Architecture 2 as reshipped with Experimentation's sign-off (portal 2026-10-27, FAILED_TO_STUMP): both responses filed Business·national at 500,000, runner-up Local·metro, 100,000 behind. The sign-off, filed to close the second judge's replay finding, told every reader that a working must reproduce each closed embedding, which rules out the one average shortfall and sends the reader to what differs between the embeddings: the desks' page mixes and each page's click-through. The closure and the stump were one dial: without a filed criterion the method is recoverable only from the change log (a replay and a competing answer), with it the decisive step is a work order. Architecture 2 is spent; re-root.
- Architecture 3, first prototype (2026-10-27, scratch t118v3/proto.py, never built): the excess fall risk by time on the drug estimated from the board's own 2023 to 2026 records, the extract's start diluting the early band. Six networks avoided only 6 to 14 admissions each, the truth ranking nearly tied (A 11, C 10), and the hazard estimate's own noise reordered it across seeds: the bin narrower than the estimator, a fitted rate per band besides (stumping 1.1j). Replaced by a filed standard (the board's medicines safety policy gives the fall rate ratio by months on the drug) and a short extract (April to September 2026), so the decisive step is each user's start, rebuilt through the repeat-template re-authorisation chain, a reconstruction with one answer.
- Architecture 3 with a three-band schedule (first 3 months 4.0, 3 to 12 months 2.2, then 1.05) and the reviews on 1
  January (2026-10-27, scratch t118v3/proto2.py): with every current user started by 30 September 2026, no one is in the
  first band in 2027 and the second band reaches only the starts after January 2026, almost all of them visible in the
  extract, so treating the users present at its opening as long-term reproduced the golden ranking: a cheap route
  landing the call. The raised band now runs to 24 months and patients come off from 1 April 2027, so the year before
  the extract (1,485 of Selbourne Coast's users) carries the excess and that route names Wychcombe or Harrowden Central.
- Primary care networks of 1,600 to 3,400 current users (the draw's first sizing): a real network has a few hundred,
  and at a base of 4 per 100 the figures fell to about 10 admissions with a gap of 2; the decision moved to six
  localities of 3,200 to 6,800 users, where the figure is 19 and the gap 4.
- A base rate of 7 per 100 a year (the draw's first parameter): about three times the national rate of emergency
  admissions for a fall at 65 and over; set at 4.0, a frail population's rate.
- Thornbury Rise's whole locality moving clinical system in July 2026 (2026-10-27, first full build): read off the
  current system, every one of its 4,583 users started on the move's date and Thornbury Rise led at 49.9, so a Layer 1
  item carried a rung (dataset-generation 7.1 R2); one practice (Mill Road Group Practice, 266 users) moves instead,
  and mishandled it leaves Thornbury Rise at 13.2, under Wychcombe's 15.3, the call, runner-up and gap unchanged. The
  second-smallest practice left Thornbury Rise 0.05 behind Wychcombe and was not taken.
- The asks' stays joined on the receiving hospital's codes, with transfers coded consistently (the first SUS cut): a
  careful join kept 13 to 24 of the 24 figures; the receiving codes now vary as hospitals record them (a move coded as a
  fresh A&E admission or from home), hip fractures at district sites go to the trauma unit mostly the same day, and the
  natural joins keep 0 to 2.
- The extract's first-item route measured against the template route in a prototype where the extract began in April
  2023: a patient on the drug since before 2023 is long past 24 months either way, so the extract's dating moved nothing
  and there was no stump; the extract was cut to the platform's first six months.
- The localities and hospital sites as first named (stage 3, reduce-house-fixes H21): Harrowden and Thornbury are real
  places (Thornbury has a real community hospital), and Selbourne and Wychcombe sit one and two letters from Selborne and
  Wycombe; renamed Corvenham Central (CC), Saltreach Coast (SC), Quenford Rise (QR) and Hethermoss (HM), with their
  hospital sites, every figure unchanged (asserted on figures.json across the rename). Lines above this one keep the
  names they were written with.
- Architecture 3 as shipped (portal 2026-10-27, FAILED_TO_STUMP): both responses filed the golden, Saltreach Coast at 19
  (one at 19.2) with Hethermoss runner-up 4 fewer (one at 15.3 and 3.9). The policy's "months since the patient first
  started" sends every reader to ask when each patient started, the extract's April pile-up answers that it cannot
  say, and the template chains are a file any reader opens: the quiet step was loud once the filed risk model named its
  quantity. Architecture 3 is spent; re-root to architecture 4 in another client domain.

- Architecture 4 at a GBP 3 million envelope: cider's cut took 89 per cent of its duty, so the straight-line welfare
  formula moved cider 0.04 above the exact integral and the gap's family straddled 0.95; at GBP 1.5 million every cut is
  a smaller share of its duty and spirits, cider and the gap each sit 0.015 or more inside a bin.
- Architecture 4 with the release layout changing in 2020: the 2020 to 2026 file alone fits spirits at 1.3 against the
  full series' 0.9, so a reader who dropped the back series moved a graded figure (Layer 1 carrying a figure); the
  change moved to 2012, where the newer file alone files 0.9 and 0.4.
- Architecture 4's first ask device, a premises renumbered at a change of keeper (removals declared to the old
  approval number): with CE14 filing the rule by premises it is executed by any reader who checks the premises, and by
  approval number it is no device; replaced by the declaration's duty repeated on every item row.
- Architecture 4's first declarations draft: duty_gbp was each line's own duty, so every CE14 handling was a filed rule
  the cracker executes (20 of 20 kept); and declaration numbers from a nine-digit hash collided once in 26,752 lines
  (two declarations merged), replaced by a multiplier prime to ten.
- Architecture 4's furniture as drawn (a Treasury research desk taking the envelope to the Council of Ministers in the
  Budget round): BLOCKed by `heart` on role, forum, forcing event and organisation against task310, drawn the same day
  and delivered after this draw; redrawn to the Assembly's scrutiny panel and its adviser, the analysis unchanged.
- Architecture 4's first invented names: Castelmere sits two letters from a real Rochdale district, and Granary Wharf,
  Westfield, a saint's name and two retail brands in the shop quotes were real or distinctive; renamed (Eskerholm,
  Ardvane, Ropewalk, Moorside) with every figure unchanged.
- Architecture 4's ask primary as first built, each declaration's duty repeated on every item row: the battery's
  repeated-total reflex sees it, and a careful solver prices every item as litres times the rate, which reaches the
  golden without ever reading the repeated total (the coordinator's review; every careful path would have kept 20 of
  20 and the pair sat near 83.5, not 28.5). Demoted to a hazard; replaced by corrections lodged as new declarations
  naming the one they correct, chained across quarter ends, which acts on which rows are releases and in which
  quarter rather than on the price.
- The first chain draft spread stock-count corrections evenly over the quarter ends: the one-hop error in a quarter is
  its inflow from the quarter before less its outflow to the next, and in one cell they cancelled to GBP 151; with the
  year-end count fullest and the half-year next every careful path misses every cell by GBP 3,600 or more.

- Architecture 4 as shipped (portal, 2026-10-28 to 10-31): the call landed three times and the determinism block
  failed twice; the golden was the field's own welfare method (the existing wedge plus the cut's triangle on the
  year's partial-adjustment quantity), which the responses applied by reflex. Spent; re-rooted to architecture 5 in
  another client domain, world, dataset and prompt shell.
- Architecture 5's handed-out cell, pharmacology benefit-risk with a pharmacist medication review whose harms avoided
  depend on whether two interacting drugs come from one prescriber or two (2026-10-31, screened on paper): the
  realisable share carried from a pilot within the prescriber-split stratum is approved 124's abstraction (a share that
  holds only within the stratum, carried to the population); dropped.
- The same cell's other mechanisms, each screened and dropped before any harness: pharmacy-counter interaction alerts
  already resolving part of the pool (the netting architecture 1 spent); generic substitution resetting exposure (task302
  and architecture 2's ground); discharge supplies misdating treatment start (architecture 3's ground); the review's lag
  against harm onset (task105 v1, solved); a self-controlled case series as the golden (the field's reflex); OTC aspirin
  co-exposure (a reflex, and purchase is not use, an open determinism fork); 90-day conversion with manufacturer
  switching (a behavioural model with no forced form); long-term-care mandatory reviews (netting again); prescribing
  cascades (task193's sequence symmetry). The cell could not carry an honest unbanned stump, so the build moved to
  energy-systems-utilities, which the brief allows (not epidemiology, criminology or marketing).
- An operating-theatre instrument-tray draw in healthcare delivery (screened on paper): the decisive quantity rode on
  how surgeons book, a behavioural fork the WHAT cannot file without filing the step; dropped.
- The demand-response draw labelled gap time with pattern E (first probe, 2026-10-31): structural BLOCKs against nine
  older builds; the honest labels are gap objective first (the measured average is right and is not what the plan
  prices) with G13, G7 and G14, which clear every structural test.
- A water-pumping shift as the fourth programme (draw, 2026-10-31): its reservoir drawn down across a heat wave sits on
  approved 120's setting (tank drawdown behind a peak), a reviewer's setting match; replaced by Peak Time Rewards.
- The first calendar with every non-event day just under the trigger (harness dgp3, 2026-10-31): the three days' heat
  before an event proxied its run day so closely that a weather model with heat build-up named the batteries at 1.22,
  a cheap route landing the call; hot weekends (uncalled under OP-7's weekday rule) now precede several fresh Mondays,
  and the heat build-up route files Cool Credit at 1.24.
- A hot weekend whose Monday sat the day before a four-day run (harness dgp4): the Monday made it a five-day run and
  the record's fourth day moved; the weekend moved two weeks.
- A Friday event followed by a Monday event after an uncalled hot weekend (harness dgp4): whether the Monday is a run's
  second day or a fresh first day is a construction fork (calendar days against the log's order); every Friday before
  a hot weekend now falls just under the trigger, and the record holds no Friday-and-Monday pair (SF10, asserted).
- A flat battery record (harness dgp5): the tenth percentile of each programme's event reductions named the batteries
  at 1.03, a reading of "firm" that lands the call for the wrong reason; Brightwell's communications drops (four
  events in 2025 and 2026 at about two thirds of the fleet) are the record's own texture and put the batteries'
  tenth percentile under Cool Credit's.
- Peak Time Rewards and Business Demand Partners within 1.07 of each other on the fourth day (harness dgp4): the
  runner-up was not determinate; the commercial sites' fourth-day reduction deepened to about three tenths of a first
  day's, which also puts every programme's figure mid-bin at whole megawatts.
- A commercial settlement audit as an ask (each 2026 event's delivered kW against the nomination, with the baseline's
  excluded days as the device): it computes a depleting programme's reduction event by event and so shows it falling
  on consecutive event days, which hands the main call's decisive pattern to any solver doing the ask; replaced by the
  nominated kW in CBMU's territory.
- A battery energisation-date ask (register upload against the inspector's pass date): the governing sentence that
  makes it determinate names the pass date, so the device is executed by every reader of that sentence; dropped.
- Megawatts to one decimal place: the standing family spreads Cool Credit 0.1 MW and the rebate programme 0.2 MW at
  the fourth day, and the thermostat panel's sampling interval is about 0.5 MW, so one-decimal figures fork; graded to
  the whole megawatt with every figure mid-bin.
