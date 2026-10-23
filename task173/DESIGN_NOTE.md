# task173: Hollis Bend Water Utilities' 2027 utility-side service leak repairs, the year its AMI contractor exchanges two thirds of the city's meters (architecture 3)

**Status (2026-10-23).** Reopened by the author for a from-scratch rebuild (`## Retired`, `## Rebuild (2026-10-23)`).
Architecture 2 (load forecasting) is spent at Gate F and the psychology and human-reliability cells died at stage 1;
every world, cell and mechanism in `## Tried and rejected` is spent and is not re-screened. Architecture 3 is drawn in
`energy-systems-utilities` / `asset-condition-maintenance` (Forecasting), chosen shape first (below).

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task173.json`, architecture v3 (v1 and v2 in `lineage`, v2 marked spent) |
| Domain / task type | `energy-systems-utilities`, task type `asset-condition-maintenance` (serves Forecasting): the deciding quantity is the count of buried service failures a water utility's crews will repair in 2027, a failure hazard per service carried to a year in which most services are worked on |
| Objective | Forecasting & Predictive Modeling: utility-side service leak repairs completed in calendar 2027, a window not yet open; records run to 30 September 2026 |
| Shape | `02`, a forecast with its history: the call (the 2027 count, nearest 250), three critical components (the 2027 base, the added repairs per 100 exchanges, the scheduled exchanges), Form 3B's base-year grids (Item 201 by service centre and month, 36 figures; Items 301 to 305 by surface type and quarter, 16 figures), the monthly chart and the two files: about 58 criteria |
| Spine | `cis_meter_events_2012_2026.csv`, one row per meter set or removal, 141,859 rows; with `gis_service_lines_20260930.csv` (147,361 services), `cis_premises_20260930.csv` and `ami_install_schedule_2027.csv` (155,460 premises each) |
| Deliverables | `service_leak_forecast_2027.xlsx` (the forecast, its working, the two Form 3B tables, notes), `service_leaks_by_month.png` |
| Decision | `quantity_figure`, answer unit `count`: the estimated quantity of service leak repairs in the 2027 service repair and restoration term contract |
| Mechanism | gap time (decisive: the record spreads meter exchanges thinly, about one meter in twenty a year, and the forward year exchanges about two in three within six months), with population (the 2027 service-months sit mostly inside the weeks after an exchange, where the record has few); pattern none; generators G2 (decisive: the unit the failure rate is read on is each service's own exchange visit and the weeks after it, not the service-year, its route or its street), G7 (when the induced failures can happen is pinned by an operations file, the AMI deployment schedule), G6 (the forward year's service-months move to the post-exchange state); Gate G `forecasting`; strategy `causal_design` (a transient risk window after a discrete visit, identified on each service against its own baseline) |
| Layer 2 family / pattern | `estimand_identification` (which exposure the failure rate is read on); `own:work-induced-failure-risk-window-carried-to-a-mass-meter-exchange` (Energy carries no client cards; the five families and the nearest domains' cards are the seeds) |
| Furniture | forum `council_or_assembly` (the City Council awards term contracts above the purchasing threshold on the estimated quantities), forcing event `purchase_order_or_contract` (the 2027 service repair and restoration term contract goes to bid with estimated quantities), organisation `local_government` (the utility is a department of the City), role `operations_director`, context artifact `other` (the bid schedule of estimated quantities), calibration `none` |
| World | Hollis Bend, a fictional Texas city of about 380,000 on shrink-swell clay; Hollis Bend Water Utilities, a city department, about 140,000 metered services with meters in curb boxes on setters with angle valves; meters exchanged at end of life by the utility's meter shop (and in 2022 by a contractor clearing stopped meters); a 2026 AMI contract exchanges every pre-2019 meter February to July 2027 and fits radio endpoints to the rest. All fictional; the field's method is real |
| People | `guard.py names --geo us --seed 173`: Mario Barnett (the planner; the golden workbook's author, in no pack file); Heidi Snyder drawn and not used; Michelle Russell dropped on a people.first WARN |

**Why this cell, shape first.** The shape that held this round is a forward population sitting at one end of an
exposure the record measures at a finer grain than the textbook model uses, the right exposure chosen by fit (task175),
or a structural estimand choice the textbook route does not make (task169). In buried-asset failure forecasting the
textbook route is a failure rate per asset-year by material, age and environment carried to the forward inventory;
the judgment it takes for granted is what exposure the failures are read on. Here the forward year is the end of an
exposure (work on the service) that the record holds only thinly, and the exposure is visible only by linking each
service's leaks to its own meter history.

**Data-native sentence.** In Hollis Bend a meter exchange means closing and reopening a decades-old angle valve and
breaking and remaking the setter's couplings in a clay-filled box, and about one exchange in a hundred leaks within
weeks, while the record's routine exchanges touch only about one meter in twenty a year, so the leaks per service-year
the record shows carry almost none of what the 2027 exchange of two thirds of the meters sets off; the induced chance
is readable only on each service's own record, its leaks in the weeks after its own past exchanges against its own
baseline.

**Screen measured before the card** (`scratchpad/b173s/proto/s1b.py` to `s1d.py`, 140,000 services, 2012 to 2026,
about 60,000 routine exchanges and 16,000 leaks, four seeds): the default (leaks per service-year of the last two
years) files 0.53 to 0.57 of the 2027 expected truth; the golden family (the per-exchange excess over each service's
own base inside a 120, 180 or 365 day window, with the delay profile applied to the 2027 schedule) sits at 0.98 to 1.05
of the truth across seeds and within 1 to 3 per cent of itself within a seed; windows of 60 to 90 days without the
delay tail file 0.89 to 0.96. Final magnitudes are set on the generator (`## Ladder`).

## Guard

`guard.py check`: WARN only (`overuse.objective`, `overuse.gate_g`: the lane's objective and its Gate G;
`repeat.decision` quantity_figure and `repeat.question_form` how-many against task176: a count of repairs is a
quantity and asks how many; `repeat.deliverables` xlsx and png against task175: a forecast workbook and its chart).
Axes redrawn at the probe and under the registration lock, each on the axis the guard named: forum
`council_or_assembly` first blocked against task274 and `board_of_directors` against task177, then `executive_team`
blocked against task175 once task274's card was spent; the City Council awards term contracts above the purchasing
threshold, and with task274 spent that forum is open again, so `council_or_assembly`. Organisation
`utility_or_infrastructure` blocked against task175: the utility is a department of the City, `local_government`.
Pattern G6 blocked against task175 and G14 against task176: the decisive rung is the unit the rate is read on (each
service's own visit and the weeks after it), G2, with G7 and G6 kept beside it. Context artifact `planning_thread`
blocked against task171, so `other` (the bid schedule). Same-puzzle and same-driver signatures differentiated on the
card against task125, task150 and task501 v3, with lines against task132, task149, task177 v3, task183 and task480 v1.

**Abstraction test.** Nearest drivers task149 (hazard per unit of working time against the pace of work, 0.10),
task183 (a part's own failure history as a frailty, 0.10), task111 v1 (a failure's originating delay in earlier work,
0.07), task132 (a wear curve reset by replacement, 0.07). None raises a unit's hazard for weeks after a discrete visit
of work to that unit and carries the visit count of a forward window; task480 v1 read old meters' under-registration at
their exchange, which is what the meter recorded, not what the visit set off.

## Default path

The pipeline a strong analyst builds from the prompt, the bid schedule's measurement section and the files' grain,
every filed rule applied.

1. Stitch the two work order systems: the legacy export to 14 May 2021 (keyed by typed street address) and the EAM
   workbook from 17 May 2021 (keyed by GIS service ID), dropping CANCELLED orders and counting each MIGRATED order once,
   in EAM.
2. Count one repair per leak, as Item 101 measures it: the CLOSED REP orders of WORK_TYPE SERVICE LEAK (investigation
   and restoration orders are not repairs; customer-side investigations carry no repair order), dated by COMPLETED.
3. Take the last two full years of the record, October 2024 to September 2026: 3,872 repairs, 1,936 a year; the
   2016 to 2025 trend (the 2021 freeze year left out) projects 1,998 for 2027, and the same rate by material and
   pressure zone carried to the 2027 inventory gives 1,936.
4. Carry the rate to 2027 (the CIP 2027 renewals move it by about 15, inside every bin).

Ends on: 2,000 repairs (1,936.0 a year, the record's rate)

Golden: 3,000 repairs (2,977.6 unrounded)

## Stump sentence

A competent solver carries the record's service leak repairs per year (or the same rate by material and pressure
zone, or its trend) to 2027 and files 2,000 repairs against 3,000, because it never reads a service's failures on its
own meter exchange visits: an exchange closes and reopens the old angle valve and remakes the setter's couplings, and
the record shows about one added repair per 100 exchanges in the weeks after the new meter is set, while the Meter
Shop's routine change-outs touched about one meter in thirty a year and the AMI contract exchanges 108,398 meters
between February and July 2027.

## Three rules

- Task type: asset-condition-maintenance (Energy Systems & Utilities), which serves Forecasting & Predictive Modeling: a
  water utility's count of buried service failures for the contract year, a failure hazard per service carried forward.
- Domain test: the deciding quantity is the expected number of utility-side service failures in 2027, estimated the
  way buried-asset failure forecasting estimates it, a rate per service read on each service's own exposure, here the
  weeks after each service's own meter exchange against the service's base rate, carried to a schedule that exchanges
  two meters in three.
- Swap: "how many infusion pump incidents will the hospital log in 2027, the year it replaces two thirds of its pumps"
  keeps a replacement wave but loses what decides it: an old angle valve and setter operated on a buried service when
  its meter is changed, failing in the weeks after; a new pump does not disturb an old part it sits on, so the task
  collapses to a replacement count.
- Layer 1: two work order systems across a May 2021 cutover (legacy by typed address, EAM by GIS service ID, MIGRATED
  orders in both), investigation, repair and restoration orders for one leak, CANCELLED call-centre duplicates, a
  premise-to-service crosswalk with 2.6 per cent of premises unlinked and multifamily premises sharing a service, meter
  exchanges as REMOVE and SET rows a day or a weekend apart, material codes from two GIS conversions and unknown
  install years, contract pay estimates resubmitted, payments in vouchers that cover two months, a fiscal year from
  October against calendar counts; each written by its system and none placed to be caught (`## Layer 1 inventory`).
- Layer 2: `estimand_identification`, which exposure the failure rate is read on: the record's rate per service-year
  averages a thin share of service-years inside the weeks after an exchange, and the forward year puts most of its
  service-years there.
- Decisive step: read each service's leak repairs against its own meter exchange history (a risk window after each
  exchange against the service's base rate) and carry the added rate per exchange to the 2027 exchange schedule.
- Not semantics: every field, code and definition read correctly (a leak is one unit, utility side only, the
  retrofit leaves the meter in place) still files 2,000, because no field, code or sentence says an exchange visit
  raises a service's failure rate; the risk window exists only in the timing of each service's repairs against its own
  meter history, two systems apart.
- Not rule application: no filed rule or procedure links exchanges to leaks, so executing every stated rule files the
  record's rate (1,936); once the exposure is read, the licensed family (windows of 90, 120, 180 and 365 days, the
  pooled base or each service's own prior year, the full record or the EAM years only, the exchange dated by its SET or
  its REMOVE) spreads 2,933.8 to 3,040.3, 0.43 of the printed unit of 250, all on 3,000; the standing family
  (windows of 90 to 180 days) spreads 2,933.8 to 2,985.2; what rules the easy route out is the data's own excess, 929
  repairs inside the 120-day windows of 65,620 exchanges against 269 expected from the base rate, a difference of
  about 40 standard errors that no filed clause states.
- Analyst test: a strong analyst who stitches both systems, counts one repair per leak and reads Item 101's scope
  correctly carries the last two years' 1,936 repairs a year (or its trend, 1,998) to 2027 and files 2,000, against
  3,000 (`Ends on:`).
- Estimand: Item 101 of the bid schedule (`itb_27-0114_service_repair_restoration_bid_schedule.pdf`, section 02)
  files the unit (one leak, however many work orders, on the City's portion of a service from the corporation stop
  through the meter's outlet coupling), the period (completion), the population (City crews and the contractor
  together, section 01) and the window (the contract year, 1 January to 31 December 2027, an estimate of the work the
  year will require); the prompt asks for calendar 2027 to the nearest 250.
- No decoy: nothing is planted; no memo, draft or stakeholder figure states a 2027 quantity, the AMI schedule and the
  meter history are the organisation's own operational files, and no document argues for the record's rate.
- No certified replay: no published or certified figure is reproduced by one method only; the method is not hidden and
  recovered, it is the analysis of each service's own repairs against its own exchanges.
- Lesson: a failure rate learned per unit-year carries to a period only at the period's own exposure to the visits that
  raise it, so a forecaster reads the record's failures on each unit's own work history before carrying a rate into a
  year when most units are worked on; no build on file reads a maintenance-induced risk window (task132 resets a wear
  curve at replacement, task149 reads a hazard per unit of working time, task183 carries a part's own failure history).

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the record's repairs a year (two years) | none needed | the EAM count | yes | none | n/a | one count | readable |
| R1 the same rate by material and pressure zone | none | GIS columns | yes (rate by attribute) | none | n/a | rates times counts | readable |
| R2 the trend through 2016 to 2025 | none | yearly counts | yes | none | n/a | a fit on counts | readable |
| R3 the exchange effect read on the route | none | ROUTE column | partly (an area grain) | none | n/a | no | readable |
| R4 (decisive) each service's repairs in the weeks after its own exchange, against its base | no sentence names exchange visits and leaks together (asserted, R1d) | no column holds it; the meter history (CIS, by premise) and the repairs (EAM by service, legacy by address) join only through the premise-to-service crosswalk and a date window | no textbook leak forecast reads a meter history | none | no sweep joins meter events to repairs | a time-windowed join across two systems through a crosswalk, then a base subtraction | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a repair | one per leak (the REP order) | every service leak order (INV, REP, RST) | 3,244 base, another call | Item 101: "A leak is one unit however many work orders or visits its repair takes" |
| SF2 | the City's side | corporation stop through the meter outlet | customer-side investigations | same call (they carry no repair order) | Item 101's scope sentence |
| SF3 | in 2027 | repair completed in 2027 | the report date | same call (2,974.2) | Item 101: counted in the period its repair is completed |
| SF4 | who repairs | City crews and the contractor | the contractor's share only | the contractor's share is assigned later | section 01: the City's total |
| SF5 | the window | calendar 2027 | fiscal 2027 | the prompt and section 01 | prompt, section 01 |
| SF6 | the quantity | the expected count | a percentile or a cap | section 01: the City's estimate of the work the year will require | section 01 |
| SF7 | the schedule | the deployment schedule as filed | four weeks' slippage | same call (2,972.2) | asserted |
| SF8 | rounding | the unrounded total to the nearest 250 | rounding parts first | same call | prompt |
| SF9 | HOLD - CIP 2027 rows | not exchanged by the AMI contractor | counted as exchanges | same call (2,981.2) | the CIP: services renewed, meter reset by the main contractor |
| SF10 | ENDPOINT RETROFIT rows | the meter stays, no exchange | every AMI visit an exchange | 3,447.4, prints 3,500 | the schedule's WORK_TYPE definition in the field definitions (the meter in place keeps its register); the record measures exchanges only |
| SF11 | Meter Shop change-outs before February 2027 | none scheduled (age change-outs stopped on the AMI award in April 2026) | continuing to March 2027 | same call (2,989.8) | asserted |
| SF12 | CIP 2027 renewals | renewed services from completion | ignored | same call (within 15) | asserted |

## Ladder

| Rung | Construction | 2027 figure | Prints | Dies to |
|---|---|---|---|---|
| R0 | the record's repairs a year, Oct 2024 to Sep 2026 | 1,936.0 | 2,000 | the record's own excess after exchanges |
| R1 | the same rate by material and pressure zone, carried to the 2027 inventory | 1,936.0 | 2,000 | the same |
| R2 | the 2016 to 2025 trend (2021 left out) | 1,998.1 | 2,000 | the same |
| R3 | the exchange effect read on the meter route | 1,954.7 | 2,000 | the fit: the excess sits on the exchanged service, not its route |
| R4 | each service's repairs after its own exchange, against its base, carried to 108,398 exchanges | 2,977.6 | 3,000 | golden |
| rival | every AMI visit read as an exchange (retrofits too) | 3,447.4 | 3,500 | SF10 |

Margins: the golden sits 102.6 inside its bin's nearest edge (2,875) against a sampling sigma of 57.2 on the added
repairs (asserted F2); the default sits 1,041.6 below the golden, more than four bins; the truth expectation is 3,004.6
(3,000). Family members W90 2,974.0, W120 2,977.6, W180 2,980.2, W365 3,040.3, own base 2,933.8, EAM years 2,985.2,
REMOVE date 2,977.6, all 3,000 (F1). Components: the 2027 base 1,887.2 (1,900 at the nearest 100; 1,884.3 to 1,887.4
across windows) and 1.006 added repairs per 100 exchanges (1.0 at one decimal).

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every utility-side service leak repaired in 2027, City crews and contractor | Item 101, section 01; C1 |
| 2 | Unit of account | one leak | Item 101 sentence; SF1 asserted |
| 3 | Attribution window | completion date in calendar 2027 | Item 101; SF3 C1 |
| 4 | As-of dating | the record to 30 September 2026, schedule rev. 4 | manifest; SF7 C3 |
| 5 | Version basis | the deployment schedule as filed | SF7 C3 |
| 6 | Denominator | per exchange (the METER EXCHANGE rows) | the schedule's WORK_TYPE definition; SF10 C4 |
| 7 | Weighting | pooled over exchanges | C1: own-base and pooled both 3,000 (F1) |
| 8 | Window length | 90 to 365 days | C1 asserted (F1) |
| 9 | Boundary inclusivity | a repair on the exchange day is outside the window | C1: none moves a bin |
| 10 | Rounding path | the unrounded total to the nearest 250 | prompt; SF8 |
| 11 | Tie-break | none | no candidates to tie |
| 12 | Maturity and censoring | exchanges whose window closes after 30 September 2026 left out | C1 across windows |
| 13 | Order of operations | base less the record's own exchange repairs, then the added repairs | C1: either order the same call |
| 14 | Row order | none | sums |
| 15 | Duplicate resolution | MIGRATED counted once, CANCELLED out | R2a, R2b asserted |
| 16 | Identity normalisation | legacy addresses normalised to the GIS; premises to services by SERVICE_ID or address | R2c, R2d asserted |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | counts | n/a |
| 19 | Code and status semantics | WORK_CLASS REP is the repair; INV, RST are not | dictionary; SF1 |
| 20 | Integerisation | none before the final rounding | SF8 |
| 21 | Clause scope | Item 101 applies to the contract year | section 01 |
| 22 | Forward window contents | the AMI schedule (rev. 4) and the CIP 2027 program | shipped driver files |

## Literal reader

Executed word for word, the prompt and Item 101 ask for the expected count of leaks repaired on the City's side of
services in calendar 2027; every literal reading of a term (SF1 to SF12) either files 3,000 or violates a quotable
sentence (SF1, SF10). The easy answer (2,000) comes from an easy method on the same literal estimand, never from another
reading.

## Oracles

none for the call: no shipped control, published figure or corpus ties under the record's rate or under the golden.
For Items 301 to 305 the accounts payable vouchers are the referee (they confirm which revision was paid and hand over
no square yards); for Item 201 nothing ties.

## Ask sheet

**Ask A, Item 201 base-year quantities: fiscal 2026 main break repairs by service centre and month (36 figures).**
H18 home: Form 3B, the base-year quantities the bid schedule's Item 201 estimate is set against. Use: the bid form.
Primary device (D1/D7, which records are one event): a break the crew clamps and the contractor repairs carries two
repair orders (REP and REPC) with one REPORTED time and one location, counted once at the permanent repair; a second
break found on the same call carries its own crew REP with the same REPORTED time at another location, a second unit.
No field says which orders are one break. Hazards: CANCELLED duplicates; the crew yard against the GIS centre (mutual
aid on 12 per cent of breaks); breaks reported in fiscal 2025 whose permanent repair falls in October 2025. Path:
`eam_workorders_2021_2026.xlsx` (WORK_TYPE, WORK_CLASS, STATUS, ASSET_ID, ADDRESS, REPORTED, COMPLETED, CREW_YARD),
`gis_water_mains_20260930.csv` (MAIN_ID, SVC_CENTER, STATUS). Stops: every REP and REPC row (0 of 36); crew REP rows only
(4); the crew yard (7); one break per asset and reported time (11); the crew's completion date (12); per asset and
initiated date (2). Realism: crews clamp and hand large breaks to the term contractor, and a crew pressurising a main
finds a second break on the same call; both are how an EAM records it. Separation: no REPC class on any service leak
order (asserted); the call reads no main break row.

**Ask B, Items 301 to 305 base-year quantities: fiscal 2026 restoration in square yards by surface type and quarter
(16 figures).** H18 home: Form 3B. Use: the bid form. Primary device (D9, a paper row covering several ledger lines):
the contractor resubmits pay estimates (the inspector's re-measure paid at its revision; a later resubmission with
added quantities returned unpaid), and in each fiscal 2026 quarter one invoice covers two months, one paid at its
revision and one as first submitted, so no voucher matches either month alone. Hazards: quarter by the estimate's month
against WORK_COMPLETED; every revision summed. Path: `mabry_teague_pay_estimates_fy2025_fy2026.xlsx` (ESTIMATE_NO, REVISION,
ITEM, QTY, AMOUNT, WORK_COMPLETED), `ap_payments_contract_23-0388.csv` (GROSS_AMOUNT), the bid schedule's item
crosswalk. Stops: the latest revision (0 of 16), the first (0), every revision (0), one-to-one reconciliation with the
latest (0) or first (1) where no voucher matches, the estimate month for the quarter (5). Realism: contract
administration systems keep every submission; a contractor invoices two months together over the holidays and at
quarter ends. Separation: the call reads neither file (asserted).

| Ask | Figures | Cracker path (lands the call, runs the battery, executes the filed rules, reconciles controls one to one) | Cracker keeps | Mirror path and keep | Cracker |
|---|---|---|---|---|---|
| A Item 201 by centre and month | 36 | every REP and REPC row once CANCELLED orders are out | 0 of 36 | the same, 0 of 36 | miss |
| B Items 301-305 by surface type and quarter | 16 | each estimate matched one to one to a voucher's gross, the latest (or the first) revision where no voucher matches | 0 of 16 | the latest revision, 0 of 16 | miss |

Pair ceiling: 28.5 (cracker keeps 0 of 52, 45.0; mirror keeps 0 of 52, 12.0; weights 38, 7, 55; every other priced reader route keeps at most 12 of 52, `generator/ceiling.py` output)

Mirror leakage: 0.0 per cent of ask weight

Measured by: generator/ceiling.py

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Neutral (asserted) |
|---|---|---|---|---|
| two work order systems across the 17 May 2021 cutover, MIGRATED in both | legacy WMS and EAM | lwms, eam | counting MIGRATED twice | R2a, same call |
| typed legacy addresses (long suffixes, a dropped directional, a stray space) | legacy WMS | lwms | exact matching only | R2c, same call |
| investigation, repair and restoration orders for one leak | EAM, legacy | both | counting every order | SF1, ruled out by Item 101 |
| CANCELLED call-centre duplicates | EAM, legacy | both | counting them | R2b, same call |
| premises with no SERVICE_ID, multifamily premises on one service | CIS | cis_premises | dropping them | R2d, same call |
| REMOVE and SET a day or a weekend apart | CIS | cis_meter_events | dating by REMOVE | R2e, same call |
| one-letter material codes, HDPE, UNK, blank install years | GIS conversions | gis_service_lines | reading them as classes | R2f, rung 1 only |
| a 2022 stopped-meter contractor's exchanges | CIS | cis_meter_events | leaving them out | R2g, same call |
| resubmitted pay estimates, combined invoices | contract system, AP | pay estimates, AP | latest revision | Ask B only |
| fiscal year October to September | Finance | bid schedule | calendar quarters | asks only |

## Leak sweep

`leak.py task173 --asof 2026-10-21`: REVIEW, no LEAK. Each REVIEW line answered:
- Sweep 3, `field_definitions.txt` and the bid schedule carry the call's nouns (water service leak repair, Item 101,
  estimated quantity, 2027): the bid schedule asks the question the call answers and defines Item 101, and the field
  definitions name the work types; neither carries a 2027 figure. Harmless.
- Sweep 4, `field_definitions.txt` carries record, exchange, history, schedule, family, carried: the file describes
  the CIS meter history (an exchange is a REMOVE and a SET), the deployment schedule, single-family premises and
  orders carried into EAM; no sentence relates an exchange to a leak (asserted, R1d). Harmless.
- Sweep 9, the AMI schedule's planned weeks in 2027: a forward plan on the allow-list (H16), as are the CIP's
  completion months and the contract year. Harmless.
- Single-use test: the AMI schedule's only use in the solution is the decisive step; it sits in the folder as one of
  three 2027 programmes (the CIP, used by the default path to take renewed services out, and the flushing plan, a
  distractor), so its presence is the planner's 2027 context, not a pointer. The meter history is the CIS's own
  record and the default path reads none of it. Recorded for the stage 4 reader's question 3.

## Stage 3 gates

- `generator/checks.py`: 81 ok, 0 FAIL (input gates, R1, R2a to R2g, R3a to R3c, the golden family F1 to F5, SF1 to
  SF12, the asks' devices and separation, documents, registers and realism).
- `generator/verify.py` (pandas and pypdf, its own path): 0 FAIL; the call 2,977.9 against 2,977.6.
- Two consecutive full builds byte-identical (16 target files, 2 golden files, the write-up).
- `figures_check.py task173`: PASS, 51 figures, 0 absent.
- `generator/ceiling.py`: pair ceiling 28.5, mirror leakage 0.0.
- `leak.py --asof 2026-10-21`: REVIEW, no LEAK (`## Leak sweep`).
- `scrub_producer_metadata.py` on `target/` and `golden/`: clean.
- `precut.py task173`: exit 0; `voice-check.py task173`: PASS.
- `guard.py surface task173`: exit 0, no persona in the cut pack. `guard.py heart task173`: WARN, no BLOCK (overuse of the lane's objective and Gate G; quantity_figure, how-many and xlsx with png against task175 and task176; nearest drivers task149 and task183 at 0.10).

## Tried and rejected

- Lazy abandonment in the 2026 simulation (a customer's patience checked only when an expert came free): it pushed a
  retry before the clock and one expert served two customers at once; abandonment and the queue's close are now events
  in time order, asserted (no event out of order, no overlapping interactions).
- Demand at the 2026 scale of 1.03: the 2026 fortnight served more new cases than the 2027 plan, an implausible fall; the
  2026 scale is 1.00 and the plan grows 3.4 per cent on the CRM's count.
- A graded figure for the fortnight's forecast contacts to the nearest thousand: its constructions spread 400 contacts
  and the golden sat within 100 of a cell edge at every placement the booking allowed; dropped from the prompt, kept in
  the workbook as working.
- Shrinkage at 11 per cent with a handle-time ramp of 0.47: the nearest flat-haircut rival landed the block; the ramp is
  0.455 and shrinkage 12 per cent, every canonical haircut now orders another block.
- Ask B as counts of customers answered after more than three minutes by day: the connect time flips too few customers
  on the quiet days after the deadline, so the cracker landed 2 and 3 May; the daily average wait moves every day by 9
  seconds.
- Crashes drawn per agent-day at a flat rate: some days had none, so the cracker landed them; each day now has at least
  three planned and a blocked one retries later in the shift.
- Hillsborough's Sunday shifts ending at 22:00: one contact ran past 23:00 Eastern, Atlantic midnight, and the invoice
  weeks read in Atlantic and Eastern time split by 0.08 h; Sunday shifts now end by 20:30.
- Frozen sessions all lasting exactly the 90-minute timeout: a uniform organ; team leads now force some out after 10 to
  75 minutes, and the timeout carries the heartbeat's 30 seconds.
- Personal Not Ready of 3 to 8 minutes: put 25 April's billable time on an exact rounding tie (209.05 h); 2 to 9
  minutes, every Ask A figure now clears its tie.
- An invoice header with a street address and an HST registration number: invented details that could match a real
  business; dropped.
- Registering after task165's DRAWN (23bd05a): `guard.py check` on 18 October blocks on the last-three bans on G14,
  `composition_mix` (task165), forum `executive_team` and forcing event `vote_or_meeting` (task247), and beyond them on
  `test.same_puzzle` and `test.same_driver` against task165 in the twelve-build window. Putting G6 first would clear the
  two tests and was rejected as a relabel of a real kinship (both builds carry a conditioned yield to a new mix); stage
  3 is built in scratch and committed without a card, which registers when task165 has left the window.
- Architecture 1 (Ashdale Tax Live's deadline-fortnight outsourcer booking, comebacks set by whoever opened each case) abandoned unregistered on 22 October: the guard's window blocked it for three days on `composition_mix`, G14, `filed_standard`, `executive_team` and `vote_or_meeting` while other lanes kept drawing those axes, and the author chose a fresh draw in a new world rather than wait; nothing of its world, mechanism or blocked axes is carried.
- Redraw cell 1, candidate A (a hospital's ALC census, its patients awaiting long-term care leaving at a fixed weekly placement count set by the region's vacancies, cut after a home closed, while other ALC exits leave in proportion to the stock; default path Little's law on the 12-month ALC stay): measured on the clean truth over 4 seeds (`proto_a2.py`), the textbook rivals bracket the golden instead of missing it on one side (Little on 12-month stays 98 to 128, Little on 13-week stays 150 to 209, occupancy over arrivals 103 to 197, Holt-Winters on the weekly census 112 to 156, against golden 120 to 171), and the golden's own spread from the post-closure placement rate alone is plus or minus 3.5 per cent at one standard error; the closure recency that separates Little's law from the count model is the same dial that starves the post-closure rate, and a census time series is a random walk with drift exactly where the placements are a count. Dead.
- Candidate B (the same placements shared at random across five hospitals' waiting lists, so another hospital's filed rise in designations lengthens every hospital's wait): measured over 3 seeds and two shock sizes (`proto_b.py`), Little on the hospital's own 12-month hazard lands at 32 to 54 against golden 35 to 53, again on both sides, with the golden plus or minus 3 per cent on the pooled placement rate; the spillover moves the level by about 15 per cent, under the 30 per cent the bar needs. Dead.
- Paper screens on the same cell, each killed before a harness: the holiday discharge backlog (the 2026-27 Christmas and New Year run of no-discharge days matches 2025-26 and 2023-24 within a day, so the seasonal naive on aligned dates carries it; `time_semantics` besides); length of stay that shortens with occupancy (the slope's estimator family is open and confounded with season); ED diversion by geography after a neighbour closes (nearest-hospital allocation is the cheap twin of the choice model, one dial); a census capped at staffed beds (the latent demand is either the boarders' count, a population reading, or arrivals times stay, which is the default path itself); new Saturday operating lists (no Saturday surgery in the record, so the weekday discharge model is extrapolated and the family forks); nursing workload from turnover (lever under 10 per cent); float-pool pooling and sickness moving with demand (the empirical daily percentile reaches the golden); a discharge-count cap first binding in the forward peak (the driver of task156, task159 and task172); a transitional unit's 60-day stay limit returning patients (task172's deadline); follow-up echoes of a new-patient surge (task157 and architecture 1's comebacks); nurse retirement at a pension eligibility date (a teachers' plan reads the same, rule 1 fails).
- Redraw cell 2, candidate C1 (a discrete cohort mortality step, the cohorts born 1944 to 1947 carrying 25 per cent excess mortality at every adult age, against Lee-Carter fitted on 1995 to 2025 and a fixed 1.5 per cent improvement; `proto_c.py`, expected values, a fictional country of about 20 million): on the deaths at 75 to 89 in 2027 to 2031, the planning quantity, Lee-Carter files 0.990 of the truth and the fixed improvement 1.012, a one per cent lever, because the step sits on four cohorts among fifteen; it reaches 20 per cent only on the cohort's own ages (83 to 86 in 2030), a quantity no decision funds, and grading it needs the cohort effect separated from age and period, the APC identification fork. Dead on lever.
- Cell 2 paper screens, each dead before code: oldest-old register over-coverage rebuilt by extinct cohorts (already dead twice, task228 candidate 2 and task271's re-root screens, not re-screened); mortality displacement after a severe 2025 winter (one to two per cent of a year's deaths, sized from a handful of past shocks); tempo and recuperation in period fertility, and second births echoing a first-birth surge (task176's paper deaths, not re-screened); depletion of the childless pool after a pulled-forward first-birth wave (about 4 per cent of a year's births, and the time-since-entry family); select mortality in a recently enrolled group (a hazard by time since entry, task468 and task134 v2); exposure bias where adjacent birth cohorts differ sharply in size (a local, sub-per-cent move on any planning total); late registration of inquest deaths at young adult ages (the standard truncation correction, lesson 1 of this round); incomplete death registration estimated by the death distribution methods (a coverage defect, the judge's planted-defect list, as task228 found); the first year deaths exceed births (the difference amplifies the golden family's spread as much as the lever); Lee-Carter's rotation, jump-off and fitting window, and cause-specific forecasting (method forks); a disability-free life table by Sullivan against a multistate projection (prevalence as incidence times duration, cell 1's bracketing death in other nouns); a once-in-sixty-years zodiac dip in births (a single past event).
- Rebuild (2026-10-23), cell `energy-systems-utilities` / `load-forecasting`, paper screens killed before a harness:
  large customers chasing a coincident-peak charge that a 2027 tariff removes (the add-back is the field's known 4CP
  correction and a null region publishes it: the non-alert days are the uncurtailed load); heat build-up over a
  heat wave's days (a lever of 3 to 6 per cent of a peak, and the lag family forks); dual-fuel heat pumps losing gas
  when a gas network is decommissioned (the pre-emption shows in the hybrids' own cold-day load, and the all-electric
  homes publish the answer); rooftop PV export limits raised under a minimum-demand forecast (task136's PV world in the
  same cell, and unclipping a known limit is the reflex); suppressed demand after rotating outages end (the restoration
  rebound is task131's driver); a direct load control programme ending (task131 again, and the non-event days are a
  null region); a district cooling plant with ice storage closing (contrived, one plant); data-centre cooling load by
  design (a visible attribute, stratified by reflex); prepaid metering conversion (stratify by payment type);
  efficiency savings embedded in the trend (about one per cent a year).
- Candidate P1 on code (`proto_p.py`, `proto_p2.py`, 12 seeds): senior plants with separate well and river-lift meters.
  The lever held (the bench wells' fitted energy per curtailed acre-foot carried over filed 1.44 to 2.31 times the
  golden), but each senior well's energy per acre-foot was then one divide of two shipped files (its bills over its
  metered extraction), a single-purpose route to the golden; the wells were moved onto the river lifts' meters, as the
  bottomland plants are built, so the pair has to be fitted (`proto_p3.py`: per-plant fit, pooled fit and the
  separate-plant average within 0.25 GWh of the truth over 16 seeds).
- The decreed allotment against the water actually diverted (the cut is the diversion above a quarter of the
  allotment, not three quarters of the allotment): kept only as a lower rung, because the order files the limit and
  applying it to each right's statements is rule application.
- Architecture 2 (Varner Valley PUD's 2027 Apr-Sep irrigation pumping under the first senior curtailment, bottomland plants a river lift and a well on one meter) spent 2026-10-23 at stage 4 on zip be677673 (Gate F): blind reader A filed 155,000 MWh, the golden, by the path "345 river lift plus well services: energy = a x diverted AF + b x well AF per service (fit 2017-2026) ... Diversion capped at 25 percent of allotment, balance pumped from the service's own well"; reader B filed 130,000 (it read the cap as leaving the land unirrigated). Both readers hit all 56 ask figures: the check meter repeating each revenue meter one interval early was dropped as a duplicate, and the meter clock's missing DST gap gave its standard time away. The judge returned DETERMINISTIC with one FIX_NOW (which meter in each pair is the revenue meter) and warned that the plant strings "RIVER LIFT + WELL" invite the two-source fit. Lessons: a plant description that names both pumps makes the per-service two-regressor fit a reflex, so the decisive quantity was named in the pack; a duplicated series and a clock with a tell-tale gap are visible hygiene and keep nothing.
- Third cell, chosen by this build after architecture 2's Gate F death: `psychology-behavioral-science` / `decision-making-computational-behavioral-modeling` (Forecasting), task177 v1's driver (imposed experiences in a learner) avoided. Why the cell: the field's own quantity, a reference-dependent stopping rule, is read from within-shift choices, no field or string names it, and a pay standard moves every worker's stopping point in a way no shift in the record ran. `guard.py check` on a probe card passes the pairing (its BLOCKs were the probe's own axes, G3 and `capacity_planner` against task169, and the older same-puzzle tests without a differentiation line). Candidate Q1 on code (`proto3/q1.py`, `q1b.py`, scratchpad b173n, 3 and 2 seeds): a food-delivery platform's 19:00 to 23:00 courier-hours after a per-order base fee rise, targeters stopping at the first drop-off past their own day's amount, clock couriers at their planned end. With the base fee from 4.10 to 5.00 (earnings per order up about 11 per cent) and 55 per cent targeters, the late hours fall 8 per cent and the courier-FE elasticity route (minus 0.30, division bias included) files 1.05 times the truth; the lever reaches 32 per cent only with the fee nearly doubled and three quarters of couriers targeting, and the record-only reconstruction of each courier's rule then sits 2 to 3 per cent off the truth. The lever is bounded by the size of the pay change, and the textbook elasticity already moves the right way. Dead.
- Third-cell paper screens and the untouched Forecasting cells beside it, each dead before code: an infectious disease's post-campaign season by the final-size relation (the nonlinearity that makes the lever is the sensitivity: near an effective R of 1.2 a 1 per cent error in R moves the season about 5 per cent, and R and the season-start susceptible share are separately identified only from season-to-season variation, so the golden family spreads past any bin); vaccine effectiveness waning under an earlier campaign (a test-negative record's per-bin effectiveness carries 2 to 3 points of sigma, and campaign timing against waning is the field's open debate a reader raises unprompted); household prophylaxis courses counted per index household (counting households with a case by address is the natural route); stress-test losses convex in unemployment (the logit or probit transform forks, and either is the satellite model's textbook); a percentile of a summed demand under cross-site dependence (resampling whole dates is the natural route); a housing-led small-area projection (net migration regressed on completions, the obvious covariate); a redistricting stripped of incumbents' personal votes (election-polling, excluded by task179's `## Rebuild`); monthly subscribers forced onto annual billing (the per-decision churn hazard does not transfer identified). Infectious disease's two earlier drivers (task179's truncated serial interval, task501's next-generation matrix) were not re-screened.

- Fourth cell, assigned 2026-10-23: `human-factors-ergonomics` / `human-reliability-assessment` (Forecasting), read against task149, task171, task175 and task176's deaths in this task type and task230 v2's driver (detection falling with a shared pool's prevalence), all avoided. Candidate R1 on code (`proto/r1.py`, scratchpad b173h, one seed, 580,000 runs and 15,300 events): a train operator's overspeed events per run rising with the days since the driver last drove that route (route-knowledge decay, truth g = 0.95 + 0.30 ln(1 + days/4)), the December timetable merging two depots' links so every driver signs twelve routes instead of seven. The lever is bounded by the merge: a driver's gap on a route goes from about 6 to about 10 days and about half of all runs are a second or third run of the day at zero recency, so the route-rate default files 0.971 of the truth and the pooled rate 0.981, against a golden family (route by recency bins at three binnings, log-recency fits) at 1.007 to 1.023; the HEART-style binary unfamiliarity split at 14 days lands 1.000. Even a tripled route set with a steep decay moves first runs about 40 per cent and all runs about 20. Dead on the lever, which the size of the roster change caps.
- Candidate R2 on code (`proto/r2.py`, `proto/r2b.py`, three seeds, 596,000 to 599,000 runs): a ten-week blockade of the main line diverting its services over a diversionary route the drivers keep signed but drive only on engineering weekends (every three weeks), the diversion's own base 1.8 times the main line's, truth amplitude 1.2 and decay 25 days; graded the overspeed events on the diverted services (truth 190 to 327). The default (the diversion's historical rate per run) files 1.28 to 1.38 of the truth and the main line's rate 0.53 to 0.58, but the golden family (route by recency bins, three binnings and a coarse one) sits at 1.013 to 1.149 of the truth across seeds (the diversion's base is read from 350 to 680 events, all at long recency, so its own scatter is about 5 per cent), leaving the default only 23 to 26 per cent above the golden; the parametric decay forms spread 0.98 to 1.25 with the likelihood picking the true decay; and the attaining subset, the diversion's own runs at 7 days or less (the second day of a weekend, the return run), files 0.92 to 1.09 of the truth, 4 to 10 per cent from the golden, a filter and a divide once the recency is built. With a three-week analogue closure in the history its rate by week of closure carried the call besides. Dead on the subset screen and the lever.
- Candidate R3 on code (`proto/r3.py`, three seeds, 8,760 shift records and about 1,300 errors in three years): a gas control centre's operator errors as slips per switching operation plus monitoring lapses per console-hour, the forward roster moving four desks on 12-hour shifts to three consolidated desks on 8-hour shifts, the duty cycle unlike the history's. The two single-exposure routes bracket the truth at 1.10 to 1.17 (per operation) and 0.81 to 0.87 (per hour), levers of 13 to 17 per cent, under the 30 the bar needs; with every history shift at 12 hours, a regression on operations leaves its intercept readable per shift (1.13 to 1.21) or per hour (0.93 to 1.05), a form the data cannot settle; with relief shifts of 8 hours in the history the two-exposure fit lands within 4 to 6 per cent, which is the two-regressor fit a medium reader took on architecture 2, and the golden's own scatter is about 4 per cent on that error count. This field's reflex (a human error probability per opportunity) does not split the two, but the data either split them for any regression or not at all. Dead three ways.
- Fourth-cell paper screens, each dead before code: errors by hour of day under a timetable moving work into the night (a stratification on the timestamp, the reflex); handover-related errors under the 12-hour to 8-hour change (the time-on-shift curve inside its observed range, task171's shift death); a workload U-curve at a consolidated desk (the forward load sits outside the record, a form fork); an error taxonomy that types slips and lapses (the split is one group-by, then each type on its natural exposure); a plant-specific HEP updated from a generic prior (a level at a selected unit, the shrinkage law); latent pre-initiator miscalibrations under a surveillance-interval extension (a regression on the interval since the last test, the obvious covariate, and equipment reliability more than human); simulator-derived HEPs for a PSA human failure event (which runs are demands is the estimand's population, the WHAT screen); steps of a procedure lengthened under a new work plan (task176's paper death, the condition in the record or its curve extrapolated). The cell's recurring death: in human reliability the forward condition either moves a performance-shaping factor the record already spans (the attaining subset, or the reflex stratification once the factor is built) or moves it outside the record (a form fork), and the roster or plan changes that are realistic move the factor too little for a 30 per cent lever.

- Rebuild cell 5, chosen by this build shape first on 2026-10-23 (`energy-systems-utilities` /
  `asset-condition-maintenance`), after these directions died on paper in the search: sewer blockages from food
  establishments upstream under a 2027 bypass (grease from restaurants is the field's best-known cause of blockages,
  and the bypass names it); deposit runoff by salary-credit primacy (the field's stable-deposit definition names
  primacy); lapse at the end of a level-term period by premium jump (the post-level-term studies tabulate it); rent
  index lag through the lease stock (the new-tenant rent index is the field's known lead); retirements at unreduced
  eligibility (experience studies tabulate rates by eligibility, and the plan rule is filed); water main breaks after a
  worst-first replacement (a level at selected units, the shrinkage law); fibre take-up by competitor presence (the
  forward areas' defining feature names the covariate); involuntary lapse at card expiry (a calendar-locked trigger,
  task162 by abstraction).
- Architecture 3, stage 3 (2026-10-23), the asks re-sited three times on the cracker script before any reader:
  Item 201 by service centre and quarter (12 figures) left the asks' weight on Items 301 to 305, which a cracker
  reconciling each estimate to its voucher kept whole (16 of 52, pair 37.0), so Item 201 went to months (36); the
  paid revision read one estimate to one voucher fell to that reconciliation, so each fiscal 2026 quarter now has one
  invoice covering two months (one paid at its revision, one as first submitted), and the cracker keeps 0 of 16;
  breaks counted once per main and reported time kept 11 of 36 with nothing to over-clean, so a second break found
  on the same call carries its own crew repair at another location.
- Architecture 3, stage 3, the induced chance per exchange at its first setting (about 1.4 per 100) put the 2027
  forecast near 3,300 with the AMI's added repairs at seven tenths of the base, more than a planner would find
  credible; it was lowered to about 1.0 per 100 (the record's routine exchanges carry about 3 per cent of its
  repairs), which still leaves the record's rate 35 per cent under the expectation.

## Retired

**RETIRED 2026-10-22 under this round's rule that a number which dies in its second new cell is retired.** Three
worlds were screened at stage 1 and none held:
- the seed's world (Ashdale Tax Live), architecture 1, built in scratch but never registered, abandoned for a fresh draw
  after three days blocked by the guard's window;
- redraw cell 1, healthcare delivery patient flow (Forecasting): candidates A and B on code, twelve on paper; a
  count-limited exit lands between the textbook routes, not outside them;
- redraw cell 2, sociology and demography life tables (Forecasting): C1 on code, fourteen on paper; national vital
  counts give sigma near one per cent, but every structural judgment the textbook routes take for granted moves a
  planning total by a few per cent, or is a coverage defect, a future-rate assumption or a spent driver.

No card was ever registered, so no guard axis is held. The screens above are the number's record for `guard.py slots`.

## Rebuild (2026-10-23)

Reopened by the author for a from-scratch rebuild under the rule that no number stays retired; architecture 2 drawn
in `energy-systems-utilities` / `load-forecasting` (Forecasting), card v2 registered, `pipeline.json` architecture 2.

Architecture 2 spent at Gate F on be677673 (`## Tried and rejected`). The coordinator then left the next cell to this build under four conditions (a forward window that changes the process in a way not on file, no field or plant string naming the decisive quantity, no ask device that is visible hygiene, every listed cell excluded). Chosen: psychology-behavioral-science / decision-making-computational-behavioral-modeling, for the reason in `## Tried and rejected`; Q1 measured dead on code and eight more directions dead on paper. No card registered for it; v2 stays the card's identity, marked spent. PAUSED at stage 1 for another cell.

Fourth cell (assigned by the main session): human-factors-ergonomics / human-reliability-assessment (Forecasting). R1 (route-knowledge decay under a depot merger), R2 (a blockade's diversion over a route driven only at long recency) and R3 (operator errors per operation against per console-hour under a new duty cycle) measured dead on code, eight more on paper (`## Tried and rejected`). No card registered; v2 stays the card's identity, marked spent. PAUSED at stage 1 for another cell.

Fifth cell (chosen by this build, 2026-10-23): energy-systems-utilities / asset-condition-maintenance (Forecasting),
architecture 3, card v3 registered with v2 moved into `lineage` as spent, `pipeline.json` architecture 3.
