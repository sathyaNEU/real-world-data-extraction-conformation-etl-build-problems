# task303: design note

Architecture 2 (re-rooted 2026-10-25 from architecture 1, the pet insurer's renewal increase, spent at stage 4).

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task303.json`, architecture v2, registered 2026-10-25 17:59 UTC and
  re-checked against the registered card: WARN only, each answered below.
- **Pairing:** Energy Systems & Utilities / `asset-condition-maintenance`, drawn for Opportunity Sizing & Decision
  Support. The task type sizes what an asset investment buys: here the customer-minutes of sustained interruption a
  year that converting one feeder's three-phase backbone to covered conductor removes, pool (the candidate's recorded
  customer-minutes outside major event days) to realisable (nine in ten of those from vegetation, wind and wildlife
  faults on the backbone the conversion replaces).
- **Niche:** Shenmore Valley Electric (fictional investor-owned distribution utility in the US south-east; the pack is
  its Valley district, 18 feeders on six substations) files its 2027 storm-hardening plan with the state commission by
  1 December 2026. The 2027 budget converts one feeder's backbone, from the feeder breaker to the end of the
  three-phase line, from bare conductor on wood poles to covered conductor on steel poles; six feeders on three
  substations are candidates.
- **The call:** F-205 (Sorrel Hill), 237,600 customer-minutes a year (generator seed 154, storm stream 382, customer
  growth 0.0062), worth USD 499,000 a year at the commission's USD 2.10. Every route that credits each feeder-breaker
  ticket to the feeder's own backbone converts F-112 (Pell Creek) at 455,400, worth USD 956,000.
- **Shape 01:** the six candidates ranked by their figure (six graded figures), the call, the incentive value, then two
  asks of twelve figures each. Shape `other` is banned against task166 and task301.
- **Strategy:** `decomposition_attribution` (a feeder's recorded customer-minutes split by where each interruption
  began: its own backbone, its taps, or its substation's supply), gap population (what one breaker-level ticket is),
  generators G8 (the conversion cannot reach a loss of the substation's supply, decided ticket by ticket) and G3 (the
  ticket names the feeder's own breaker while the interruption began upstream); Gate G `decomposition_attribution`.
  Pattern none: pattern C's serviceable share behind a join is not the form here.
- **Furniture:** forum regulator_or_inspector (the commission reviews the filing), forcing statutory_or_regulatory_filing
  (the plan due 1 December 2026), organisation utility_or_infrastructure, role capacity_planner (the distribution
  planning engineer who prepares the filing), context artifact operations_log (the outage system's exports),
  calibration none.
- **People** (`guard.py names --geo US --seed 303`): Zachary Sanders, distribution planning engineer, author of the
  valuation guidance. Not in the prompt.
- **Spent mechanisms on the objective** (`guard.py mechanisms --objective opportunity-sizing-decision`, twelve builds):
  task105 the part of a catchment nearer the new outlet; task106 candidates drawing on one shared pool; task116 a group
  offer reachable through one signatory; task118 the gain on volume a unit does not already treat; task120 a supply
  system's draw net of what accumulated inside it; task127 the part of a fused wait the intervention removes; task128 a
  contact's effect read only on over-capacity days; task306 an asset base taking in units the roll does not hold yet;
  task305 short-stay occupants who sit in no origin; task302 a stocked-out line's loss net of diversion and rebound;
  task301 a recorded state decaying between recordings; task303 v1 the owners a renewal increase drives away. None
  attributes a unit's recorded losses to their origin through the minute its sibling units share.
- **Abstraction test:** nearest driver task127 v2 at 0.08 (the part of a recorded wait the intervention removes,
  because the wait fuses the replaced step with a concurrent one): there the fusion is inside one unit's own record and
  the replaced step's excess is read from its timestamps; here the record is complete and correct for its feeder, and
  the part the conversion cannot reach shows only across the sibling feeders' tickets. task252 v2 at 0.05 (error
  arising upstream of every channel) reads an error common to channels against a truth; here nothing is in error.
  task201 (storm restoration-time accounting) times interruptions from the first customer report; here no start or
  restoration on the call's rows is in question.
- **Probes before the draw:** four concept probes (sonnet, medium, no files) on four candidate designs; three applied
  their decisive step unprompted (Tried and rejected), the fourth, this design, filtered by major event day, cause and
  device, shrank the history and never asked where a breaker ticket began. Then two call-only probes, isolated, sonnet
  at medium, on a prototype pack (scratch `p303uo/`, /tmp/r303ua and /tmp/r303ub: both OMS exports, the major event
  days, the inventory, the plan's valuation guidance, the export notes and the vegetation work orders): both converted
  F-112 by crediting every breaker ticket (356,000 on that prototype), the default path to the figure; neither looked
  across the sibling feeders. The built pack keeps that world's mechanism (seed scan in scratch `scan6b.py`).
- **WARNs answered:** `people.first` (Zachary, one older build); `repeat.gate_g` (task121 v5, spent); `repeat.decision`
  and `repeat.question_form` (task166 v2): the decision is a pick of one of six feeders, so the question asks which.
- **Data-native sentence:** Pell Creek's three feeders open their breakers in the same minute twelve times in the 2019
  to 2025 record outside the major event days, and the outage system records each as an interruption on that feeder's
  breaker with the cause the crew found on the line feeding the substation (a tree, wind, lightning), so eleven of
  F-112's thirteen vegetation, wind and wildlife breaker and recloser tickets, 70 per cent of their customer-minutes,
  are losses of the substation's supply that no backbone conversion can prevent.

## Three rules

Task type: asset-condition-maintenance (Energy Systems & Utilities), tagged in the taxonomy for Opportunity Sizing & Decision Support: the customer-minutes of sustained interruption a backbone conversion removes from each candidate feeder, pool (its recorded customer-minutes outside major event days) to realisable (nine in ten of those from vegetation, wind and wildlife faults on the backbone it replaces).
Domain test: The deciding quantity is the customer-minutes a backbone conversion removes, which reliability engineering attributes interruption by interruption to where it began (the feeder's own backbone, its taps, or the substation's supply) from the protective device that cleared it and, for a loss of supply, the sibling feeders that all lose supply in the same minute; only the interruptions that began on the converted backbone from the causes it addresses are credited.
Swap: "the feeder whose backbone conversion removes the most customer-minutes once the breaker tickets every feeder at its substation opened in the same minute are traced to the substation's supply" put into a hospital's wards or a retailer's stores loses its mechanism: no ward or store records a shared upstream loss of supply under its own protective device, and no refit of one ward is credited with the minutes of the circuits it carries.
Layer 1: the outage system migrated on 1 January 2023 (legacy tickets with feeder numbers, codes, Eastern local dates and clock times and minutes of duration; current tickets with feeder ids, worded categories and UTC start and restoration stamps); major event days as Eastern calendar days against UTC stamps; transformer and service tickets beside the tap fuses; on the asks' paths, the storm crews' records (the storm desk's screen in Eastern local time, the contract crews' own devices on standard time all year, the desk's late entries) and the legacy handheld tickets (hours and minutes, dated the day they closed); nothing is placed to be caught.
Layer 2: field_method: interruptions are attributed to their origin before an investment on one feeder is credited; a loss of the substation's supply, which every feeder there records at its breaker in the same minute, is not a fault on any feeder's backbone and the conversion removes none of it.
Decisive step: separating, among each candidate's feeder-breaker tickets, those every feeder at its substation opened in the same minute (losses of the substation's supply) before crediting the conversion with nine in ten of the remaining vegetation, wind and wildlife customer-minutes on the backbone.
Not semantics: every field reads as what it is (the breaker is the feeder's breaker, the cause is the cause on the ticket, the customers are the customers who lost power); no field, code or note says where an interruption began, and an analyst who maps both exports, converts every clock and drops the major event days exactly still credits every breaker ticket to the feeder's backbone, as both call-only probes did.
Not rule application: the guidance files the WHAT (the conversion's scope, faults on the converted backbone from vegetation, wind or wildlife, nine in ten prevented; the 2019 to 2025 record outside the accepted major event days divided by seven; customer-minutes as customers times minutes) and nothing about where a ticket's interruption began. Enumerated family on the pack: crediting every breaker and recloser ticket (the probes' route) files F-112 at 455,400 and F-205 third at 237,600; removing the shared-minute tickets files F-205 at 237,600 and F-112 at 137,800, a spread of 317,600 on F-112's figure, 3.3 times its value once the shared tickets are removed. Standing family (the constructions that remove the shared-minute tickets: the same start minute, within 1, 2 or 5 minutes, at least two sibling feeders within 0 or 2 minutes): an identical figure for every candidate, spread zero, F-205 every time (asserted). What rules the crediting route out is no filed clause but the record: a fault on one feeder's backbone cannot interrupt its sibling feeders' customers.
Analyst test: A strong analyst who reads every file correctly sums each candidate's feeder-breaker and line-recloser tickets caused by vegetation, wind or wildlife outside the accepted major event days over 2019 to 2025, takes nine in ten of their customer-minutes divided by seven and converts F-112 at 455,400 customer-minutes a year, where the golden is F-205 at 237,600; checks.py runs both on the pack (the default rung and the standing family).
Estimand: the customer-minutes of sustained interruption the conversion would have removed from the 2019 to 2025 record had it been in place, outside the major event days the commission accepted, divided by seven, the conversion preventing nine in ten of the faults on the converted backbone from vegetation, wind or wildlife and nothing else (storm_hardening_plan_2027.docx, sections 1 and 3).
No decoy: nothing is planted: the outage exports are the utility's tickets as its two systems kept them, the major event days the commission's; no memo, draft or figure argues for a feeder, no file ranks the candidates, no past plan or valuation is in the pack, and no stakeholder figure is set up to be overturned.
No certified replay: no certified or published figure sits in the pack; no file states a reliability index, a daily SAIDI, a past valuation or a past plan to be reproduced, and the attribution is not recovered from any figure.
Lesson: a feeder's outage record carries every interruption its customers suffered, wherever it began, and an investment in the feeder is worth only the interruptions that began on the part it changes; a loss of the substation's supply shows only as the same minute on every sibling feeder's breaker. No build on file attributes a unit's recorded losses to their origin through the minute its sibling units share.

## Default path

The pipeline a strong analyst builds from the prompt, the guidance and the exports' fields:

1. Stack the two outage exports: legacy feeder numbers to F-nnn, legacy codes to the current wording, current UTC
   stamps to Eastern time; customer-minutes are customers times minutes (legacy duration, or restoration less start).
2. Drop the tickets that began on an accepted major event day (Eastern dates).
3. Keep the backbone tickets (feeder breaker and line recloser) and drop the fuses and transformers.
4. Keep vegetation, wind and wildlife.
5. Sum each candidate over 2019 to 2025, take nine in ten and divide by seven.
6. Rank: F-112 455,400, F-114 285,400, F-205 237,600, F-301 132,100, F-303 83,300, F-208 39,000.

Ends on: convert F-112 (Pell Creek) at 455,400 customer-minutes a year, USD 956,000 at the incentive.
Golden: convert F-205 (Sorrel Hill) at 237,600 customer-minutes a year, USD 499,000 at the incentive.

## Stump sentence

A competent solver credits every feeder-breaker and line-recloser ticket caused by vegetation, wind or wildlife outside
the major event days to the feeder's own backbone and converts F-112 at 455,400 customer-minutes a year, where the
golden is F-205 at 237,600; the step that lands it there is reading each Pell Creek breaker ticket as a fault on F-112's
backbone, when the tickets all three Pell Creek feeders open in the same minute are losses of the substation's supply,
which the conversion cannot prevent.

## Readability screen

| Rung | What it needs | Verdict |
|---|---|---|
| the two exports stacked, codes mapped, UTC put on Eastern time | the export notes | readable |
| the accepted major event days left out by the day an interruption began | the plan, section 3; the notes | readable |
| feeder breaker and line recloser tickets from vegetation, wind or wildlife | the plan, section 1; the notes | readable |
| nine in ten, divided by seven, at USD 2.10 | the plan, sections 3 and 4 | readable |
| the tickets every feeder at a substation opened in the same minute are losses of its supply (decisive) | the start minutes across the sibling feeders' tickets; no field, code or sentence anywhere | silent |

## Ladder

| Rung | Construction | Ranking (customer-minutes a year, nearest hundred) | Pick |
|---|---|---|---|
| R0 | every interruption on every device, every cause, nine in ten over seven | F-112 515,200, F-114 377,900, F-205 341,300, F-301 184,900, F-303 137,500, F-208 116,300 | F-112 |
| R1 | backbone tickets, every cause | F-112 476,100, F-114 354,900, F-205 304,300, F-301 154,600, F-303 114,000, F-208 95,900 | F-112 |
| R2 | backbone tickets from vegetation, wind or wildlife (the default path) | F-112 455,400, F-114 285,400, F-205 237,600, F-301 132,100, F-303 83,300, F-208 39,000 | F-112 |
| R2a | R2 per backbone mile, or per customer | F-112 first either way (36,147 a mile; 206.1 a customer) | F-112 |
| R2b | the over-correction: every breaker ticket dropped as possibly upstream, reclosers only | F-301 37,100, F-303 32,100, F-208 13,400, F-114 11,500, F-112 7,000, F-205 0 | F-301 |
| R2c | R2 with the major event days kept (against the plan) | F-112 1,808,500 first; with the shared minutes removed F-301 1,496,300 first | F-112 or F-301 |
| R3 | R2 less the tickets every feeder at the substation opened in the same minute (golden) | F-205 237,600, F-112 137,800, F-301 67,300, F-208 39,000, F-303 32,100, F-114 29,600 | F-205 |

R2 is the stump; R2b is the over-correction a suspicious reader takes when it doubts the breaker tickets without
testing them against the sibling feeders; every rung is asserted in checks.py.

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | customer-minutes | customers interrupted on the ticket times its minutes | customers served times minutes | another figure | the plan, section 3: the customers interrupted times the minutes from interruption to restoration |
| SF2 | outside the major event days | tickets that began on an accepted day, by the Eastern date | the UTC date of the start | another population (asserted) | the export notes: Eastern calendar days; an interruption belongs to the day it began |
| SF3 | the 2019 to 2025 record | both exports, every ticket in them | a subset of years | none | the plan, section 3; both exports hold exactly 2019 to 2025 (asserted) |
| SF4 | vegetation, wind or wildlife | TREE, WIND, ANML and the current system's Vegetation, Wind, Wildlife | other causes | none | the notes map the codes one to one (asserted) |
| SF5 | faults on the converted backbone | interruptions that began on the backbone, cleared by the feeder breaker or a line recloser | fuse or transformer tickets included | R0 | the plan, section 1 (nothing for taps and laterals); the notes (fuses protect the taps) |
| SF6 | a year | the seven-year sum over seven | the mean of the seven yearly figures | same figure (asserted) | same call |
| SF7 | nine in ten | of the customer-minutes | of the tickets | same figure (a multiplier) | same call |
| SF8 | the feeders at a substation | the inventory's three per substation | the feeders the tickets show | same feeders (asserted) | same call |
| SF9 | opened in the same minute | equal start minutes on every sibling feeder | within 1, 2 or 5 minutes; at least two sibling feeders | same figures (the standing family, asserted) | same call |
| SF10 | the call's legacy minutes | DUR_MIN on breaker and recloser tickets, whole minutes | none | none | every breaker and recloser DUR_MIN is a whole number (asserted) |
| SF11 | the repeated hour each November | the first reading of a legacy time in it | the second | same call (asserted) | same call |
| SF12 | the value at the incentive | the exact figure times USD 2.10 | the stated figure times USD 2.10 | the same thousand (asserted) | same call |
| SF13 | the candidates | the six in the plan's table | none | none | the plan, section 2 (asserted) |
| SF14 | an interruption running past midnight | all its minutes, on the day it began | clipped at midnight | another figure | the export notes: an interruption belongs to the day it began |
| SF15 | the incentive rate | USD 2.10 a customer-minute a year | a rate per SAIDI minute | another value | the plan, section 4; the order, section III |
| SF16 | customers | each ticket's customers interrupted | the inventory's customers | another figure | the plan, section 3 (asserted: breaker tickets carry the year's customers) |
| SF17 | ask A, the storm days | tickets that began on an accepted major event day of 2023 to 2025, by the Eastern date | the UTC date | 11,436,000 ... (a stop) | the export notes |
| SF18 | ask A and B, per customer interrupted | customer-minutes over the customers interrupted on the tickets | the mean ticket duration | another figure | the asking sentence: those minutes per customer interrupted |
| SF19 | ask B, interruptions its tap fuses cleared | fuse tickets | fuse and transformer tickets | another figure | the export notes: fuses protect the taps; a transformer ticket is a transformer or a service |
| SF20 | ask B, a year over 2019 to 2025 | the seven-year sum over seven | the current system's three years | another figure | the asking sentence (over 2019 to 2025) |
| SF21 | ask A, which days | the commission's accepted major event days dated 2023 to 2025 | the days accepted in dockets of 2023 to 2025 (the 2022 to 2024 days) | another population (asserted) | the prompt: the commission's accepted major event days of 2023 to 2025 |

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | every ticket on the six candidates in 2019 to 2025 that did not begin on an accepted major event day | filed literally (plan section 3; the notes' day rule) |
| 2 | Unit of account | a ticket's customer-minutes; a candidate feeder | filed (plan section 3) |
| 3 | Attribution window | 2019 to 2025 by the Eastern date an interruption began | filed (plan section 3; notes) |
| 4 | As-of dating | the exports of September 2026, the record closed at 31 December 2025 | filed (notes) |
| 5 | Version basis | the commission's accepted days as listed | filed (the major event day file) |
| 6 | Denominator | seven years; for the asks, the customers interrupted | filed (plan section 3; the asking sentences) |
| 7 | Weighting | each ticket by its customers | filed (customers times minutes) |
| 8 | Window length | seven years | filed |
| 9 | Boundary inclusivity | a ticket beginning at 00:00 on a major event day is on it | C1: no call ticket within a minute of midnight on a major event day's edge moves the call (the figure is by start date) |
| 10 | Rounding path | sum the customer-minutes, nine in ten, over seven, once to the nearest hundred; the value from the exact figure | filed (the prompt); C1 (the stated figure gives the same thousand, SF12) |
| 11 | Tie-break | none at the pick | asserted (F-205 clears F-112 by 1.72 times) |
| 12 | Maturity and censoring | none: the record is closed | not live |
| 13 | Order of operations | filter, then nine in ten, then over seven | C1 (multipliers commute) |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | no duplicate ticket in either export | asserted (ticket ids unique) |
| 16 | Identity normalisation | FDR 112 is F-112; legacy device ids to the current ones | filed (notes) |
| 17 | Netting against gross | none | not live |
| 18 | Dimensional units | minutes, customers, USD | filed |
| 19 | Code and status semantics | cause and device codes | filed (notes); never the stump |
| 20 | Integerisation | none | not live |
| 21 | Clause scope | the conversion's nine in ten applies to the converted backbone's three causes only | filed (plan section 1) |
| 22 | Forward window contents | the 2019 to 2025 record stands for the conversion's years | filed (plan section 3: had it been in place) |

## Literal reader

Executed word for word, the plan files the estimand (the customer-minutes the conversion would have removed from the
2019 to 2025 record outside the accepted major event days, over seven, the conversion preventing nine in ten of the
faults on the converted backbone from vegetation, wind or wildlife) and every convention closes by a filed sentence or
converges (SF1 to SF20). The literal estimand's only open question is which tickets are faults on the converted
backbone, and the records answer it: a ticket every feeder at the substation opened in the same minute cannot be a
fault on one feeder's backbone. The default answer is an easy method on that same literal estimand (every breaker ticket
taken as a backbone fault), never another reading. The write-up's eight steps each name the file and the rule that
produce their result.

## Oracles

None. No file ranks the candidates on the decision quantity (the plan's table lists feeder, substation, backbone miles
and cost in feeder order); no published reliability index, daily system SAIDI, storm report or past valuation is in the
pack, so nothing ties out under either handling; the major event day file lists dates and the year's threshold only.
For ask A the storm crews' records are the truth source the golden reads, not a control: they carry restoration times,
no total. For ask B nothing in the pack states a tap figure.

## Ask sheet

Two asks, each a component of the filing's candidate pages (the plan, section 5; the commission's order, section IV),
each computed over rows the main call's declared population does not contain, each with its own silent primary.

**Ask A, the storm record (12 figures: each candidate's customer-minutes on the commission's accepted major event days
of 2023 to 2025, nearest thousand, and those minutes per customer interrupted, one decimal).** H18: the order's section
IV asks each project's record on the accepted major event days of the three preceding years. Use: the candidate page's
storm line. Primary device, silent (D3, a time scale set per source): the mobile workforce system records Assigned on
the storm desk's screen and every other status on the crew's own device, and the contract crews' devices keep Eastern
standard time all year, so on the daylight-saving storm days each contract crew's En route, On site, Restored and
Released read an hour early as Eastern local time; where a ticket was closed as the crew called it in, the outage system
took the crew's Restored time as it arrived, so 536 of those restorations are an hour early as well. The first level is
filed (the export notes: on storm-operation days the storm desk entered restorations from the crews' reports) and every
reader so far has made the repair it invites: the desk entered 3,078 of the 4,991 crewed storm tickets' restorations in
its sessions from the top of every third hour, at least a quarter hour after the crew's restore, and the other 1,913
carry the crew's time as it arrived (FA1 to FA4). The only trace of the primary is a cross-row cut nothing invites: read
as Eastern local time, all 1,359 contract crews on daylight-saving storm days are en route before the desk gave them the
job, none of the 209 in standard time and none of the 4,536 other crews' jobs (asserted FA5); the reader's route reads
only the Restored rows, where nothing is out of place. Interior: the company, mutual assistance and assessor crews'
devices keep Eastern local time and the contract crews' winter statuses need nothing, so moving every crew or every
season is another wrong figure. Hazards: the outage system's UTC against the crews' local times; the major event day by
the Eastern date an interruption began. Files: oms_interruptions_2023_2025.csv, storm_crew_status_2023_2025.csv,
major_event_days_2019_2025.csv, mobile_workforce_export_notes.txt, oms_export_notes.txt (5 files, 15 columns). Stops
(F-112, F-114, F-205, F-208, F-301, F-303): the crew's Restored read as Eastern local time (the careful read) 11,069,000
/ 392.5, 5,606,000 / 329.9, 7,136,000 / 383.0, 6,053,000 / 403.0, 9,797,000 / 399.8, 4,149,000 / 397.1; the outage
system's restoration (the natural read) 14,020,000 / 497.2, 7,371,000 / 433.8, 8,468,000 / 454.4, 7,102,000 / 472.9,
11,992,000 / 489.4, 5,043,000 / 482.6; every crew's device on standard time 12,620,000 / 447.5, 6,569,000 / 386.5,
8,103,000 / 434.8, 6,650,000 / 442.8, 10,820,000 / 441.6, 4,696,000 / 449.5; the contract crews an hour later all year
11,650,000 / 413.1, 5,783,000 / 340.3, 7,357,000 / 394.8, 6,334,000 / 421.8, 9,966,000 / 406.7, 4,421,000 / 423.2;
golden 11,615,000 / 411.9, 5,773,000 / 339.7, 7,332,000 / 393.5, 6,210,000 / 413.5, 9,952,000 / 406.1, 4,391,000 /
420.3. Realism: a contractor's own field devices on standard time feeding the utility's mobile workforce system, and an
outage system taking each crew's time as it arrives. Reused device: none in this lane's window.

**Ask B, the taps' record (12 figures: each candidate's customer-minutes a year from interruptions its tap fuses
cleared outside the major event days over 2019 to 2025, nearest ten, and those minutes per customer interrupted, one
decimal).** H18: the plan's candidate page shows the interruptions on the candidate's taps, which the conversion leaves
as they are. Use: the candidate page's taps line. Primary device, silent (D8, a clock against a filed cutoff): a legacy
tap or transformer ticket a trouble crew closed on its handheld carries the day the crew closed it as OUT_DT (the notes:
"ticket date"), beside the clock time the interruption began, so an interruption that ran past midnight reads a day late
against the filed cutoff (major event days are Eastern calendar days and an interruption belongs to the day it began).
On storm days the control room closed nearly every tap ticket itself; the handhelds closed 1,395 legacy tickets, 300 of
them dated a day after they began, 196 of those begun on an accepted storm day, and on the six candidates 7, 10, 8, 2, 7
and 3 storm-day tap tickets read as the day after the storm. The forcing is a filed sentence and the records: the notes
say the control room issues ticket numbers in the order it opens tickets, and only with each handheld ticket dated the
day it closed do the numbers run in the order the interruptions began (no break; read as the day each began, 255
breaks, every one beside a handheld ticket, asserted FC1). The first level is filed: the notes give DUR_MIN as whole
minutes or hours and minutes after a point (no decimal entry past .59, FB1). Interior: the control room's tickets are
dated the day they began, so dating every legacy ticket the day it closed is another wrong figure. Hazards: the legacy
codes and local times and the major event days, shared with the call. Files: oms_interruptions_2019_2022.csv,
oms_interruptions_2023_2025.csv, major_event_days_2019_2025.csv, oms_export_notes.txt (4 files, 19 columns). Stops:
hours and minutes read right, OUT_DT read as the day each began (the careful read) 34,890 / 162.5, 36,770 / 211.7,
44,140 / 167.3, 11,440 / 142.5, 63,520 / 329.1, 32,670 / 221.6; decimal hours, OUT_DT as the start (the natural read)
33,600 / 156.5, 35,770 / 205.9, 42,530 / 161.2, 11,110 / 138.4, 61,790 / 320.1, 31,770 / 215.5; decimal hours with the
closing date handled 22,870 / 120.0, 15,430 / 119.5, 29,540 / 127.0, 8,710 / 112.7, 15,130 / 101.9, 19,930 / 149.4;
every legacy ticket dated the day it closed 517,800 / 559.6 and the like; golden 23,840 / 125.1, 14,450 / 116.3, 25,950
/ 119.2, 9,000 / 116.5, 16,410 / 110.6, 13,540 / 118.5. Realism: a handheld form whose date field holds the day it was
completed, an old source of a day's slip in outage records.

**The main population's zero-counts** (asserted in checks.py): no breaker or recloser ticket carries a handheld
duration (SEP1); every crew record is a major event day ticket (SEP2); every restoration the desk entered late is on a
major event day (SEP3); no storm-day breaker ticket in 2023 to 2025 opened with every sibling feeder (SEP4); the call
files the same six figures with every legacy ticket's OUT_DT read as the day it began (SEP6).

**Hazard table.** The UTC and Eastern clocks (the call, ask A); the major event day by the date an interruption began
(the call, asks A and B); the legacy codes and feeder numbers (the call, ask B); the storm desk's late entries (ask A)
and the handheld hours and minutes (ask B), the first levels a careful reader repairs. Each is executed by the hygiene
battery and moves no figure for a response that executes it.

**Referee.** None: no designed disagreement needs one. The crews' records carry each storm ticket's restoration, the
level the golden reads, and tie to the outage system to the minute on every ticket the desk closed as the crew called
it in.

| Ask | Figures | The cracker's path (lands the call, runs the battery, executes every filed rule) | Kept | Verdict |
|---|---|---|---|---|
| A | 12 | the crews' Restored time joined to every storm ticket, every status read as Eastern local time | 0 of 12 | miss |
| B | 12 | the hours and minutes read right, OUT_DT read as the day each interruption began | 0 of 12 | miss |

Pair ceiling: 30.8 (cracker 45.0 on the call with no ask figure, mirror 16.5 off it: two of eight call criteria, F-205's and F-208's figures, which the default path files the same, and no ask figure); a cracker that also finds ask A's device reaches 44.5, ask B's 44.5. Measured: round 2's two scored readers (target.zip 784cd964) both filed F-112 and kept 2 of 30 scored figures (the two candidate figures the default path shares, no ask cell), each on a route pair.py prints as the careful read and scores 0 of 12 on the shipped pack; measured pair 16.5.
Mirror leakage: 0.0 per cent of ask weight.
Measured by: generator/pair.py on the cut pack (target.zip c2fb8f15).

## Tried and rejected

- Permit centre standard plans (the seed's world, municipal permitting x Opportunity Sizing: ten funded positions across
  intake, plan review, corrections and issuance, plan review's 2027 load driven by the builders entering the city with
  their plan libraries): both call-only probes landed the allocation (intake 3, plan review 3, corrections 1, issuance
  3) from the builders' outlook; and staffing a stage pipeline reads the same in any office, so the swap test fails.
- A world with the Lifetime Dog tariff at its first level and narrow claim costs: marking a continuing condition only
  once it recurs in a second policy year put Lifetime Dog above Essentials in 21 of 144 constructions, and raising the
  tariff 10 per cent instead let the claims-paid route land Essentials; claim costs were given a wider spread and the
  tariff 5 per cent, with a larger Essentials book, so every split names Essentials and every route Lifetime Dog.
- A policy history from 2014 instead of 2019: the lifetime books' held owners piled up, and the recurrence and span
  markings named Lifetime Dog.
- Architecture 1, the lifetime owners held by a continuing condition (Essentials at CAD 0.5 million, every one-response route on Lifetime Dog), spent at stage 4: reader A named Essentials with a retention logit carrying claims in the expiring and prior terms by product (lifetime claimants almost never leave), a covariate reflex that reaches the split without marking a condition; the judge returned SEND_BACK because the printed addition ran from CAD 0.32 to 0.51 million across condition markings, flag timings and response fits; both readers took all 48 ask cells (the wrap codes against the menu option, the case-number gaps against the letters, a same-amount debit 10 to 14 days after each return).
- 2026-10-25, architecture 2 screen, three concept probes (sonnet, medium, no files), each landed by the probe applying
  the decisive step unprompted: a winter-peaking utility's efficiency programmes at the peak hour (the lamps' heat
  made up by electric heat in resistance-heated homes, the pilot's gas-heated homes measuring the gross saving); a
  water company's meter cohorts (bench errors at four test flows weighted by each cohort's consumption profile from
  the logger panel); a card issuer's collections team (the treated cures valued against the recoveries the control's
  charge-offs bring in after charge-off, the immature vintages completed).
- 2026-10-25, architecture 2 screen, earlier in the re-root: county input-output commuting leakage (both call-only
  probes landed on the Type II caveat); an excise's efficiency cost on a partial-adjustment path with the existing
  wedge's rectangle (a concept probe applied both moves; economics x Opportunity Sizing banned against task302).
- 2026-10-25, architecture 2 screen, dead on paper with the reason in one clause each: a card cure's re-default
  (task177); a deflated Sharpe ratio (task175); win-back waves (task157, task134 v2); a bonus's pull-forward (task161,
  task180); depletion of responsive members (task124, task176); deadweight (task136); regression dilution (task200);
  traffic assignment (task253's lineage); common-cause redundancy (task201); transformer thermal ageing (task121's
  screen); private equity commitment pacing (task167, task501); EV home-charging composition (a stratification reflex);
  stormwater green infrastructure timing and annuity late reporting (earlier probes and task181 v2); housing moving
  chains; the bus wait inspection paradox; a pension sleeve's market impact; a design-effect boost; refinance
  burnout; catastrophe as-if (the replay law); transmission N-1 (the capacity-credit pincer); a vegetation trim cycle's
  phase (task129's world); wind farm wakes and long-term mast correction (named caveats the setting cues); technical
  against non-technical losses (a named caveat); tap-changer wear per operation (task46's driver).
- 2026-10-25, ask layer round 1 (target.zip 66cc0eca): both isolated readers missed the call, and both joined the storm
  crews' Restored time to every storm ticket, because the outage system's restoration ran later on six storm tickets in
  ten (a device whose discovery and remedy were one comparison of two files on one key), and one of the two read the
  handheld durations as hours and minutes from fractions that never pass .59; ask A went 12 of 12 to both and ask B 12
  of 12 to one (86.7 and 46.7 per cent of the scored figures). Re-sited one level below each repair: ask A onto the
  contract crews' devices keeping standard time (traced only by their En route before the desk's Assigned), ask B onto
  the handheld tickets dated the day they closed (traced only by the ticket numbers' order).
- 2026-10-25, the re-site on paper: step restoration recorded as a child ticket (task301 C's overlapping-legs shape); a
  re-fault job carrying two Restored statuses (seen on the reader's own join); a crew operating day from 07:00 (the
  storms start after five, so it moved two of six candidates); every storm-day handheld ticket dated the day it closed
  (the legacy years' taps at up to ten times the current system's, a loud year-on-year tell), kept at four in a hundred.
- 2026-10-25, stage 4 round 2 (judge r2 on 784cd964, DETERMINISTIC, FIX_NOW on the asks only): the storm desk's late
  entries and the handheld hours and minutes as unfiled first levels, which the judge read as open forks on the asks'
  literal text (the outage system's restoration against the crews' time; the decimal durations), and the prompt's
  "accepted in 2023 to 2025", readable by docket year; both first levels are now filed in the export notes, the ask's
  days reworded as the accepted major event days of 2023 to 2025, and the silent primaries carry the asks. In the same
  pass, the storm tickets that piled up at 23:25 (330 in the record, fifteen same-fuse same-minute pairs a round 1
  reader noticed) were folded back into the evening, with the handheld share on storm days at six in a hundred so each
  candidate keeps at least two date-device rows.
