# task276 design note

Architecture 3, re-rooted on 2026-11-03 after architecture 2 (Urban & Regional Science, network-analysis, the
level crossing world) was spent at stage 4. Nothing of architecture 2's world, survey or replay is carried over; its
death is the A2.7 line in the tried-and-rejected section.

## Draw

- **Pairing.** Human Factors & Ergonomics (`human-factors-ergonomics`), task type `anthropometric-design-fit`, which
  serves Descriptive & Distribution Analysis in the taxonomy. The call is how a measured population of drivers is
  composed against each candidate cab's package: how many of them each cab cannot accommodate.
- **World.** Hallowfen Ambulance Service, an invented regional ambulance service formed in April 2023 from two
  predecessor services (Strakemoor in the north, which measured in millimetres and kilograms, and Vennerley in the
  south, whose occupational health forms were kept in feet, inches, stones and pounds). Its Fleet and Estates
  Committee specifies one cab for the 2027 front-line ambulance order: a base chassis (FD35 or RD43) with one
  converter's cab conversion (Pennick Coachbuild, Wrenfold Bodies, Ostrel Vehicle Conversions), five combinations
  on the tender shortlist, every one fitted with the same Brevin AS-7 seat.
- **Niche.** The converter that buys a longer patient saloon by moving the cab bulkhead forward, and fits the
  extended seat slide so that its stated seat travel is the longest on the shortlist.
- **The decision and its filing.** The service's cab fit standard files the criterion: the committee specifies the
  shortlisted cab that the fewest rostered drivers fail to fit, a driver failing a cab when they cannot be seated in
  the posture the service's driver posture model predicts for them in that cab with their eye point inside the
  standard's vision zone. Prices are tendered and shipped (a distractor); the criterion does not read them.
- **Forward facing.** The cab is specified for vehicles delivered in 2027; the population is the roster published on
  1 October 2026, filed as the population the order is bought for.
- **Shape 01**, each shortlisted cab with two figures (drivers it fails, of whom women): 10 criteria; the call, the
  runner-up and the gap: 3; the chart's named parts (one bar per cab, the bar values, the recommended cab marked, the
  axis in drivers): 4; the two files: 2; the asks, each shortlisted converter with vehicles in the fleet (its jobs in
  four quarters, its miles, its rate) and each shortlisted chassis (its days off the road in four quarters, its
  vehicle-years, its rate): 24. Forty-three criteria, the asks a little over half.
- **Deliverables.** `cab_fit_2027.xlsx` (the committee workbook) and `cab_fit_2027.pdf` (the chart printed for the
  committee pack).
- **Shell.** Question form how-many, second-sentence opener "set", rounding opener "keep", deliverable set pdf+xlsx.
  Architecture 2's shell was what, build, give and docx+xlsx, so every element moves (shell.lineage).
- **Card.** `guard.py register` filed it at WARN: `repeat.deliverables` (pdf+xlsx against task241 v2 and task194
  v17), answered here: the pair is what a fleet team sends a committee (a workbook and the chart printed as a PDF),
  and neither build shares a world, a driver or a shell element beyond the format pair. `test.same_puzzle_older`
  differentiated against task258 (v1) and task303 (v2) on the card. Nearest driver 0.06 (task230's lineage).
- **The one other build in this cell.** task256 (shipped, pending) is the only Human Factors build on Descriptive &
  Distribution: a transit authority's bus workstation share inside a box of ranges, its operators known only by
  stature and weight and the box filled from a reference survey carried through them. Here every driver is measured,
  every stated range is already met on paper by the default path, and the miss is physical: the structure behind the
  seat stops the backrest short of the posture. The card carries the line; the shell, the decision rule (no price
  line, no share threshold), the population's data and every file differ.
- **Data-native sentence.** Ambulance converters buy saloon length by moving the cab bulkhead forward and quote seat
  travel as the slide's own length, so the drivers who need the rear of the slide are the drivers whose backrests,
  reclined to their own torso angle, meet the bulkhead first; a seat-travel count cannot see it because the stop
  moves with each driver's posture.

## Default path

1. Build the population from the front-line driving roster published on 1 October 2026, joined to the cab fit
   measurements through the staff-number crosswalk (Vennerley's legacy numbers), the latest measurement standing
   where a driver was measured twice, Vennerley's imperial entries converted: 2,658 drivers.
2. Place every driver in every shortlisted cab with the service's driver posture model: hip point aft of the
   accelerator heel point from stature, body mass index and the cab's seat height; torso angle from stature and body
   mass index; eye point from the hip point and sitting eye height.
3. Fail the driver in a cab when the predicted hip point lies outside the cab's stated hip-point travel (each
   converter's package data, Wrenfold's moved from its seating reference point to the heel point), or the eye point
   misses the standard's up-vision or down-vision angle at the chassis's windscreen header and bonnet points. This is
   the field's seat-position accommodation method (the SAE J1517 and J4004 way of placing a hip point in a travel
   range) with the vision check, executed on the stated ranges.
4. Count the drivers each cab fails, and specify the cab that fails the fewest.

Ends on: Wrenfold Bodies on the FD35 chassis, failing 109 drivers (Wrenfold on the RD43 next at 134, Pennick FD35
third at 166).

Golden: Pennick Coachbuild on the FD35 chassis, failing 166 drivers, with Ostrel on the FD35 the runner-up at 319
and Wrenfold on the FD35 at 450 once each driver's backrest is placed against its bulkhead.

## Stump sentence

A competent analyst places every rostered driver with the service's posture model, checks the hip point against each
cab's stated seat travel and the eye point against the vision standard, and specifies Wrenfold Bodies on the FD35
chassis, failing 109 drivers against the other Wrenfold cab's 134 and Pennick FD35's 166; the step that lands it
there is treating Wrenfold's stated travel as travel its drivers can use, when its forward bulkhead stops the
backrest, set at each tall driver's predicted torso angle, before the seat reaches that driver's hip point, which
fails 341 more drivers in Wrenfold's FD35 cab and 301 more in its RD43 cab and leaves Pennick Coachbuild on the FD35
chassis failing the fewest.

## Three rules

Task type: `anthropometric-design-fit` in Human Factors & Ergonomics, which serves Descriptive & Distribution
Analysis: the call is the composition of the service's measured driver population against each cab's package.

Domain test: the deciding quantity is the number of rostered drivers each cab fails to accommodate, which
anthropometric design fit estimates by placing each person's predicted driving posture (hip point, torso angle, eye
point) from a posture-prediction model into the vehicle package and testing it against the package's constraints.

Swap: "how many of our patients would each ward bed fail to fit" keeps the count and loses the work: a bed has no
hip point placed by a posture model, no torso angle that sets a backrest against a bulkhead, no eye point against a
windscreen header, so the question stops making sense.

Layer 1: Vennerley's occupational health forms in feet, inches, stones and pounds beside Strakemoor's metric e-forms
(the merged OH system keeps both column sets); Vennerley's legacy staff numbers on measurements taken before the
September 2025 HR migration (HR's crosswalk); drivers re-measured on query (the standard's latest stands); measured
staff no longer on the roster; Wrenfold's package data dimensioned from each cab's seating reference point while
Pennick and Ostrel use the heel point; the seat maker's sheet in inches. On the asks' rows only: the Vennerley
workshop system's jobs under legacy codes and fleet numbers with jobs open at its closure carried into the fleet
system; renumbered vehicles whose fleet-system in-service date is the date their records were created; fleet numbers
of disposed vehicles reused; telematics units swapped, the old unit reporting until collected; jobs whose off-road
spells overlap; a current register beside a disposals list. Every item comes from the system named, none is placed
to be caught, and none moves the call (asserted in `checks.py`, `R2.mess_neutral` and the separation block).

Layer 2: the data's real structure is physical: the seat is an object whose backrest occupies space set by its
occupant's own posture, and the cab's structure behind the seat bounds where that object can go; the methodological
choice that flips the call is placing the whole seated posture against the package rather than the hip point
against the seat's stated travel.

Decisive step: setting each driver's backrest to the torso angle the posture model predicts for them and placing its
top rear corner, at the driver's predicted hip point, against the bulkhead line, so the travel a driver can use ends
where the backrest meets the bulkhead rather than at the slide's stated rear stop.

Not semantics: the default path reads every field correctly (the travel is the converter's stated travel, the
bulkhead dimension is the bulkhead's trim face, the inches and the datum are converted) and still files Wrenfold
FD35; no field, code, unit or definition carries the clearance, which is a geometric relation across the seat
sheet, the package data and each driver's predicted posture.

Not rule application: the standard files the WHAT (who must fit, what failing means, the vision zone) and the
posture model files the posture; no filed rule or procedure performs the clearance test. Enumerated family (the 5th
to 95th percentile check, hip point in travel, hip point in travel with vision, the same with the seat's recline
range, the whole posture against the package): Wrenfold FD35's count spreads from 107 to 450 drivers (the percentile
check finds no shortfall at all for either Wrenfold cab) and the call splits between Wrenfold FD35 and Pennick FD35.
Standing family under the filed text alone (the three hip-point constructions and the whole posture): spread 341
drivers on Wrenfold FD35 and the same split call. What rules the easy members out is the geometry itself (a backrest
set through the bulkhead line is not a seat setting), silent: no sentence, column or flag states it, and only the
constructed corner position shows it.

Analyst test: a strong analyst who places each rostered driver with the posture model, checks the hip point against
each cab's stated travel and the eye point against the vision standard (the service's fit method executed on the
stated ranges) specifies Wrenfold Bodies on the FD35 chassis at 109 drivers, when Wrenfold's forward bulkhead stops
the reclined backrest of its tall drivers before the seat reaches their hip points and Pennick Coachbuild on the FD35
chassis fails the fewest.

Estimand: the cab fit standard (`policy/cab_fit_standard_issue2.docx`) files the population (every member of staff
on the front-line driving roster to be published on 1 October 2026), the outcome (a driver fails a cab when they cannot be
seated in the posture the service's driver posture model predicts for them in that cab with their eye point inside
the vision zone the standard defines), the unit (drivers, each counted once), the comparison (every cab on the 2027
shortlist) and the decision (the cab the fewest fail).

No decoy: nothing is planted to be caught; each converter's data describes its own product as converters do, no
memo, draft, briefing or stakeholder figure argues for any cab, and no fit count ships anywhere in the pack.

No certified replay: no certified or published fit figure exists to reproduce; the posture model's validation is of
the posture predictions against seat positions observed in the current fleet, honest, and it ranks no 2027 cab.

Lesson: a seat's stated travel is not the travel its occupants can use, because the structure behind the seat, met
by the backrest at each occupant's own torso angle, ends the usable travel early for exactly the occupants who need
the rear of the slide; no build on file teaches that an adjustment range is tested by placing the whole posture
against the surrounding structure (task256 teaches a multivariate share carried from a reference survey).

## Survivor anatomy

Actor: the deciding property, whether a driver's backrest at their torso angle clears the bulkhead at their hip
point, has no column in any file; it is a relation between each driver's predicted posture, the seat's backrest
geometry and the cab's bulkhead line.

Link: the comparison runs through a construction no key offers: the backrest's top rear corner (seat sheet, inches,
measured along and behind the torso line) set at the driver's torso angle and hip point (measurements through the
posture model) against the bulkhead line at the corner's height (package data, Wrenfold's in another datum), a
comparison the field's seat-position method never asks for.

Reflex: the field's seat-position accommodation method with the vision check is the default path's rung and files
Wrenfold FD35, the cab with the longest stated travel and the most forgiving front stop.

Back-test: the posture model validates honestly: the 2025 seat trial's observed seat positions in the current fleet
match its predictions, and the fit method applied to the current fleet reproduces the trial's observed fits, because
no current cab has a forward bulkhead, so the clearance never binds where the record was made.

Second use: every file the decisive step reads is on the default path anyway: the seat sheet for its travel and
recline, the package data for travel, seat height and vision points (the bulkhead is one dimension among the
package's), the measurements and the posture model.

Shock: Wrenfold's forward bulkhead reads as its selling point (the longer saloon) and its longer slide as an
advantage; Pennick FD35 is first on no single shipped statistic (Pennick RD43 has the rearmost bulkhead, Wrenfold
RD43 the rearmost travel, Wrenfold FD35 the longest slide's lowest seat and most forward front stop, Ostrel the
lowest price, Wrenfold the shortest lead time).

Pins: the WHAT is filed in the service's cab fit standard in its own genre, and no filed sentence names the
backrest, the bulkhead, clearance or recline as a test; deleting any filed sentence leaves the clearance exactly as
silent as before.

## Readability screen

Each rung against the seven tests (1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear, 7
second use). The reflex row is enumerated from the field's vocabulary for accommodation (the percentile manikin
check, seat-track accommodation, the vision check), not from the rungs below.

| Rung | 1 filed | 2 schema | 3 reflex | 4 bench | 5 hygiene | 6 linear | 7 second use | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 5th to 95th percentile hip point inside the stated travel | no | no | fires (the classic manikin range check) | no | no | yes | yes | readable |
| R1 each driver's hip point inside the stated travel | no | fires (travel columns) | fires (SAE J1517 seat accommodation) | no | no | yes | yes | readable |
| R2 R1 and the vision zone, the default path | fires (section 4) | fires | fires | no | no | yes | yes | readable |
| R2r R2 and the seat's stated recline range | fires (S7) | fires | fires | no | no | yes | yes | readable |
| R3 (decisive) the backrest at each driver's torso angle against the bulkhead line | silent (no sentence names backrest, bulkhead or clearance) | silent (no column) | silent (the reflex treats the seat as a hip point on a slide) | silent (the posture validation and the current fleet agree with R2) | silent | silent (a per-driver construction across three files) | silent (every file is on R2's path) | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | rostered drivers | the 2,658 staff on the roster published 1 October 2026 | everyone the programme measured | same call (Pennick FD35 fails 181) | standard section 2 |
| SF2 | which measurement | the latest | the first, or the mean of two | same call (Pennick FD35 fails 166 under both) | standard section 5, "the latest measurement stands" |
| SF3 | former Vennerley numbers | mapped through the crosswalk | unmapped drivers dropped | same call (144) | the crosswalk file; every roster driver has a measurement |
| SF4 | imperial conversion | 25.4 mm an inch, 14 lb a stone, 0.45359237 kg a pound | rounded factors | same counts | asserted, no count moves |
| SF5 | inside the travel | inclusive limits | strict limits | same counts | no hip point within 1.5 mm of a limit |
| SF6 | vision angles | at least 11 and 5 degrees | strictly more | same counts | no sight line within 0.05 degrees of a limit |
| SF7 | eye point | 18 mm forward of the hip point | 18 mm aft | same call | the model report's words |
| SF8 | where the backrest meets the bulkhead | its top rear corner | any point of the rear face | same counts | asserted: no rear-face point binds before the corner |
| SF9 | recline | the torso angle inside 8 to 34 degrees | recline ignored | same counts | every predicted angle lies inside S7 |
| SF10 | Wrenfold's datum | each cab's stated SgRP moved to the heel point | figures read as heel-point figures | not a reading: negative travel | the package data's own SgRP sentence |
| SF11 | women | Sex F on the roster | another source | one source ships | the roster's Sex column |
| SF12 | shortlist | the five cabs in section 6 | other converter and chassis pairs | not offered | standard section 6 |
| SF13 | runner-up and gap | second fewest, the difference | none | no ties | five distinct counts |
| SF14 | chassis sight points | one set per chassis | per converter | identical in every package | asserted |
| SF15 | body mass index | latest weight over latest stature squared | a recorded index | none recorded | the model report's definition |
| SF16 | quarters | financial quarters from 1 April | calendar quarters | asks only | the reporting definitions |
| SF17 | a job carried across the workshop cutover | once, in the quarter first raised | twice, or at the fleet system's date | asks only | the definitions, "first raised" |
| SF18 | a unit's miles | from the odometer entered at fitting to its last reading before removal | readings after removal kept, or the first daily reading as the baseline (moves both converters' miles and rates) | asks only | the reporting standard's Miles run row, "measured from the odometer reading entered when the unit was fitted" and "from the date it was fitted up to the date it was removed, that date not counted" (`SF18.miles_from_the_entered_odometer`, `SF18.first_reading_baseline_moves_the_miles`) |
| SF19 | days off the road | the days a vehicle was off the road, once each | each job's spell added | asks only | the definitions' state of a vehicle |
| SF20 | vehicle-year | 365 days in the fleet | 365.25 or the year's days | asks only | the definitions |
| SF21 | in service, renumbered vehicles | from the Vennerley asset list's date | from the register's 1 July 2025 | asks only | the definitions' "entered front-line service" and the vehicles' Vennerley jobs before July |
| SF22 | converters with vehicles | Pennick and Ostrel | Wrenfold | asks only | no Wrenfold vehicle in the fleet |
| SF23 | rate rounding path | exact denominator | rounded denominator | same printed rates | asserted |
| SF24 | which vehicle a record belongs to | the vehicle holding the fleet number on the record's date | the number's current holder | asks only | the register's in-service dates against the disposals |

## Ladder

Measured on the shipped pack (2,658 drivers; `checks.py` asserts winners, positions and margins).

| Rung | Construction | Pennick FD35 | Wrenfold FD35 | Wrenfold RD43 | Ostrel FD35 | Pennick RD43 | Names | Margin |
|---|---|---|---|---|---|---|---|---|
| R0 | percentile hip point against travel (shortfall, mm) | 4.6 | 0.0 | 0.0 | 22.3 | 29.0 | the two Wrenfold cabs | no shortfall |
| R1 | hip point in travel | 165 | 107 | 119 | 316 | 370 | Wrenfold FD35 | 1.11 over Wrenfold RD43 |
| R2 | R1 and vision (default path) | 166 | 109 | 134 | 319 | 399 | Wrenfold FD35 | 1.23, then 1.24 to Pennick FD35 |
| R2r | R2 and recline range | 166 | 109 | 134 | 319 | 399 | Wrenfold FD35 | as R2 |
| G | the whole posture against the package | 166 | 450 | 435 | 319 | 399 | Pennick FD35 | 1.92 over Ostrel FD35 |

The golden is third on the default path, behind both Wrenfold cabs, so a solver who sets Wrenfold FD35 aside for any
reason but the backrest lands on Wrenfold RD43. Dominance: the decisive step adds 341 drivers to Wrenfold FD35
against the 57 its stated travel carries over Pennick FD35. Every graded main-call figure is a whole count with no
fitted parameter, and the dead zone keeps every driver at least 1.5 mm and 0.05 degrees from every limit, so no
consistent reading moves a count.

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | the roster published 1 October 2026 | filed (standard section 2); C1 against the measured population |
| 2 Unit of account | drivers, each once | filed; one row per driver on the roster |
| 3 Attribution window | the asks' financial year | filed in the definitions; quarters from 1 April |
| 4 As-of dating | the roster's date; each fleet record on its own date | filed; SF24 asserted |
| 5 Version basis | the latest measurement | filed (standard section 5) |
| 6 Denominator | asks: miles while fitted, vehicle-years | filed in the definitions |
| 7 Weighting | none, a count | inert |
| 8 Window length | the financial year | filed |
| 9 Boundary inclusivity | limits and angles inclusive | C1: the dead zone, SF5 and SF6 |
| 10 Rounding path | rates from exact denominators | C1: SF23, both paths print one rate |
| 11 Tie-break | none needed | C1: five distinct counts |
| 12 Maturity and censoring | none | inert: every driver measured, the year closed |
| 13 Order of operations | convert, map, place, test | C1: the steps commute on the shipped rows |
| 14 Row order | none | C1: counts over sets |
| 15 Duplicate resolution | latest measurement; a carried job once | filed (standard section 5; the definitions) |
| 16 Identity normalisation | the crosswalk; former and reused fleet numbers | the systems' own keys and dates, C4 for reused numbers |
| 17 Netting against gross | none | inert |
| 18 Dimensional units | millimetres, inches, stones, pounds | units in the files; SF4 asserted |
| 19 Code and status semantics | job codes B12 and B30 and their Vennerley codes | the code map and the definitions |
| 20 Integerisation | whole drivers, jobs and days | C1 by construction |
| 21 Clause scope | the standard for the main call, the definitions for the asks | filed scope; separation asserted |
| 22 Forward window contents | the 2027 cab fits the roster it is bought for | filed population; no projection |

## Literal reader

Executed word for word: the standard's population is the roster (2,658 rows, each with a measurement under its own
or its former number); "the latest measurement stands"; the posture model's equations place each driver; "can be
seated in the driving posture the model predicts" needs the seat at the predicted hip point with the backrest at the
predicted torso angle, and a backrest whose top rear corner would lie behind the bulkhead trim face cannot be set
there, so those drivers fail; the vision zone's angles are tested at the eye point. Every reading the text leaves
open (SF1 to SF15) prints the same call, and the counts are whole numbers clear of every limit. The easy answer is an
easy method on the same literal estimand (the hip point checked against the slide alone), never another reading. On
the asks, each definition fixes the figure's population, window and unit; the reconstructions (the vehicle holding a
number on a date, a carried job's first raise, a unit's fitted window, a renumbered vehicle's original service date)
are what the definitions mean applied to the records, never a second reading of them.

## Oracles

No control ties only under the golden or only on the wrong read. The posture model's validation ties under both
routes (no current cab has a forward bulkhead). No shipped file ranks the shortlisted cabs on drivers fitted: the
tender prices rank them on price (Ostrel FD35 cheapest) and the package data on dimensions, neither the decision
question. On the asks, no file carries a vehicle's converter-history, its reused number or its original service date
in a column that names the reconstruction; each is found from an internal inconsistency (a job raised before the
current holder of its number entered service, a renumbered vehicle with Vennerley jobs before its stated service
date, a unit reporting after its removal).

## Ask sheet

The asks are a second measure per candidate that the call does not turn on (supplemental-stumping 1.3, H18): the
record on the service's own fleet of the shortlisted converters (seat and cab-structure defect jobs per quarter, the
miles their vehicles ran, jobs per 100,000 miles) and of the shortlisted chassis (days off the road per quarter,
vehicle-years, days per vehicle-year). They read only fleet files the call never opens (`separation` asserted both
ways), and Wrenfold has no vehicles in the fleet.

- Ask A, the converters (8 quarter figures, 2 miles, 2 rates). Primary D7: fleet numbers of disposed vehicles reused
  for new vehicles of another converter, so a job or a unit on a reused number belongs to whichever vehicle held it on
  the record's date, read from the disposals against the register (moves every quarter of both converters and both
  miles). Second, another family: a unit's miles run from the odometer entered at fitting, so the first reading in the
  window is not the baseline (moves both miles and both rates). Hazards: a Vennerley job carried into the fleet
  system at the cutover counted once at its first raise; legacy codes through the code map; legacy fleet numbers.
- Ask B, the chassis (8 quarter figures, 2 vehicle-years, 2 rates). Primary D2: renumbered Vennerley vehicles carry
  1 July 2025 as their fleet-system in-service date, so their year in the fleet runs from the Vennerley asset list's
  date (moves both vehicle-years and both rates). Second, another family (D1 by overlap): jobs whose off-road spells
  overlap hold one vehicle off the road once, so adding each job's days over-counts every quarter. Shared hazard: the
  reused numbers (D7) move every quarter's days between chassis.

| Ask rows | Figures | The cracker's handling | Cracker keeps | Verdict |
|---|---|---|---|---|
| A jobs by quarter | 8 | current holder of each number, carried job at the fleet system's date | 0 of 8 | miss |
| A miles | 2 | current holder, first reading as baseline | 0 of 2 | miss |
| A rate | 2 | as above | 0 of 2 | miss |
| B days by quarter | 8 | current holder, each job's days added | 0 of 8 | miss |
| B vehicle-years | 2 | the register's and disposals' service dates | 0 of 2 | miss |
| B rate | 2 | as above | 0 of 2 | miss |

The cracker lands the call, runs the hygiene battery (former staff and fleet numbers, the code map, the disposals, a
carried job deduplicated to the record the fleet system holds) and executes the filed definitions (a unit's fitted
window, 365-day vehicle-years). The mirror takes the default path's call with the same ask handling and keeps the
three cabs the backrest does not move (Pennick FD35, Ostrel FD35, Pennick RD43, both figures each).

Pair ceiling: 32.4 (cracker 45.0, mirror 19.8, on the 38, 7 and 55 split).

Mirror leakage: 0.0 per cent of the ask weight.

Measured by: `ceiling.py` on the cut pack; each single device's lift on the cracker stays under a third of the ask
weight (reused numbers 9.2 points, original service dates 4.6, the carried job's first raise, a unit's fitted
baseline and days counted once 0.0 each alone, against a cap of 18.3), asserted.

## Leak sweep answers

`leak.py task276 --asof 2026-10-09`: REVIEW, no LEAK; sweeps 1, 5, 7, 8, 9 and 11 clean. One line per REVIEW:

- Sweep 2, "the model" six times in `policy/driver_posture_model_ellisand_2025.pdf`: the report is the driver posture
  model the standard cites, and the phrase is the field's own name for it; it never refers to an analyst or a solver.
- Sweep 3, the call's words in `policy/cab_fit_standard_issue2.docx`: the shortlist table lists the five cabs in
  tender order with their package data reference, no figure and no order of merit; the decision rule is the filed
  criterion, which names no cab.
- Sweep 3, `fleet/package_drawing_data_pennick.pdf`: the converter's own tender data for its two cabs names itself
  and its chassis and states dimensions only, as the other two packages do.
- Sweep 3, `policy/driver_posture_model_ellisand_2025.pdf`: the validation table names the four current cab types of
  the 2025 trial (two of them Pennick and Ostrel builds now in service) with the model's error in each; it finds no
  cab type different and ranks nothing on fit.
- Sweep 4, the three package PDFs, the seat sheet, the standard, the posture model and the reporting standard: each
  term is the documents' ordinary vocabulary (driver, bulkhead, travel, package, backrest, posture, standard); no
  document relates the backrest to the bulkhead, mentions a clearance or says a stated travel can overstate the usable
  one, which `checks.py` asserts over every document (`leak.no_sentence_relating_backrest_and_bulkhead`).
- Sweep 6 (INFO), the standard and the tender prices name every shortlisted converter: the standard's shortlist
  carries no figure, and the prices rank the cabs on price (a declared distractor, cheapest Ostrel FD35, not the
  call), so no file ranks the cabs on drivers fitted (Gate G, asserted).
- Sweep 12, the standard names six column values of the data files (Converter, Chassis, FD35, RD43 and two
  converters' names): the organisation's own record of its shortlist; it defines no column and states no join.

## Stage 4 findings

- Judge: DETERMINISTIC, APPROVE, Gate H decisive_step analytical (`determinism_check_report.md`).
- Reader, question 6 (rule application): harmless. The reader never reached the backrest-against-bulkhead check and
  read the filed posture model as the decisive step; the judge's full derivation rules the whole-posture check
  analytical, and the judge recomputed where the reader did not.
- Reader, question 5 gap (travel limits and recline not named in section 3): harmless, the intended stump; "seated
  in the driving posture" and the Wrenfold geometry stay as filed, since naming the travel or the bulkhead files the method.
- Reader REVIEW, the posture model's author-like vocabulary: harmless as the reader ruled, a consultant's model report.
- Reader REVIEW, `package_drawing_data_pennick.pdf`: harmless as the reader ruled, geometry only, recommends nothing.
- Reader REVIEW, the standard's decision vocabulary: harmless as the reader ruled, the decision rule names no winner.
- Reader REVIEW, the posture model's decision vocabulary: harmless as the reader ruled, it recommends no cab.
- Reader REVIEW, the standard naming data columns: harmless as the reader ruled, the organisation's governing record.
- Reader realism, fixed in the generator: the disposals return now dated after its last row (created 2 April 2026)
  and kept by Gareth Davis; HR's crosswalk by Christine Rees and Occupational Health's measurements by Linda Cooper,
  Liam Jackson left on the fleet register and code map (`realism.department_editors`,
  `realism.disposals_dated_after_its_rows`); each converter's package from its own toolchain (Pennick from Excel,
  Wrenfold through Acrobat PDFMaker in Arial, Ostrel printed to Distiller in Cambria, `realism.package_toolchains_differ`);
  the Wrenfold source note kept on its table's page (`realism.no_orphaned_note.*`). No package wording changed.
- Miles baseline (SF18): no shipped sentence fixed a unit's miles from the odometer entered at fitting rather than the
  first daily reading, which moves both converters' miles and rates; closed by one clause in the reporting standard's
  Miles run row, the only wording change in the pack. A reworded document, so the reader re-reads before ship.

## House fixes

- H1: `scrub_producer_metadata.py` audits `target/` and `golden/` clean (no writer signature, no stamp outside the
  fiction); the Word and Excel packages carry the service as company and Word 16 and Excel 16 as application, and
  each PDF its own date in the fiction.
- H2 and H3: every figure in `submission.md` is emitted from `figures.json` by `writeup.py`, the rate's 100,000 miles
  included (`figures_check.py` PASS); the note's measured numbers are printed by `ceiling.py` and `checks.py`.
- H4 and H7: `target.zip` holds `target/` and its folders only, cut last from the second of two byte-identical builds;
  `golden/` holds exactly the two deliverables.
- H9: no readme, dictionary, notes, manifest or codebook file or sheet under `target/`, asserted by name and content.
- H11: one `submission.md` and one `prompt.txt` in the tree; architecture 2's generator files are removed.
- H16: every extract's last date is on or before 9 October 2026 (the odometer to 31 March 2026, the measurement
  programme to September 2026, the roster and the register at 1 October 2026); sweep 9 clean.
- H18: each ask is a second measure per shortlisted converter and chassis, read on fleet rows the call never opens
  (`separation` asserted both ways).
- H21: invented names normalised and compared with the reference registers; the first cut's coachbuilder, northern
  predecessor and six hub names sat near real firms or places and were renamed in the generator (Corvane,
  Strakemoor and the hubs), every figure unchanged.
- H23: "none" is grammatical in every ask (the women among a cab's failures, a quarter's jobs or days).
- H25: every shipped PDF, the chart included, reads the same through pypdf lenient and strict and through poppler's
  `pdftotext`, with no parser warning (`container.readers.*` asserted); the standard is read by python-docx in the
  verifier and as raw XML in the checks.

## Duplicate check

- `guard.py heart task276`: WARN, from `repeat.deliverables` alone (pdf+xlsx against task241 v2 and task194 v17,
  answered in the draw) beside the NOTE `test.same_puzzle_older` (task258 v1 and task303 v2, differentiated on the
  card); no BLOCK. Nearest text on file 0.04 (task305 v3's stump, task281's ledger row), nearest driver 0.06 (task230
  v1's lineage).
- `guard.py surface task276`: 304 builds screened, two pairs promoted for the author's adjudicated read, task303
  (0.032, corpus percentile 18) and task258 (0.024, percentile 16), each on the card axes alone (gap population,
  pattern G8, pick one of n) with no surface overlap. The card's differentiation answers both: task258 moves units
  across a threshold through a step each served document must carry, task303 credits an intervention with a shared
  upstream loss, and here nothing is moved or credited, each driver's predicted posture being placed against a fixed
  structure behind an adjustable seat. Nearest unpromoted neighbours 0.040 (task167, task188, task229, task240,
  task241); no other build's persona in the cut pack.
- task256, the one other Human Factors build on this objective, is in neither screen's nearest list; the draw's line
  above carries the difference.

## Tried and rejected

- Overlap and saturation alone (`binding_constraint`, G8): the first-order correction a careful analyst makes by reflex (collaborators already seeded cannot be invited) lands the call, and overlap among invitees is a second-order effect at launch densities that stay plausible.
- Acceptance delay completed community by community (`maturity_censoring`): the nowcast by unit-specific delay is task181's and task451's driver.
- A dated platform campaign inflating some pilots (`decomposition_attribution`): a cause with a cutover date is adjusted by reflex (the strategy record, F8).
- The pilots' evidence judged at the pilot rather than the invitation (`uncertainty_hold`): the client's record has interval stumps landing on the natural computation.
- Exposure-response at launch density (`composition_mix`, pattern E, 2026-10-24): a developer's chance of accepting rises steeply with how many seeded collaborators invite, read at each member's own invitation count at launch density, is task175's driver (a unit's chance of being taken rises steeply with how many units on its own run are already taken, read at its own run's fill and carried run by run) with the count created by the seeding instead of found on the street; `guard.py check` scored it 0.06 against task175 and passed it with WARNs only, so the repeat was found by the abstraction test, not the guard.
- A1.1 Year-one retention by market against the month's sign-ups, when members who leave erase their accounts (in-app deletion under App Store guideline 5.1.1(v) and GDPR Article 17) and the accounts table and the analytics export hold only accounts not erased (Product Analytics, metric-definition-measurement-science, `population_selection`, G9): the strongest; honest, prototyped, and the routes separate, but `guard.py check` BLOCKs `test.same_driver` inside the twelve-build window (population, G9, method_or_model_selection against task270's v1 and v6 lineage), the G12 reading of the same step BLOCKs against task268 v2 and task273 v1 lineage, and no honest redraw of the gap or the pattern keeps the mechanism, so it cannot register. Written in full below.
- A1.2 The share of checkout requests over a latency line from traces weighted by their recorded sample rate, when the collector's rate limit drops traces at peak minutes without changing the recorded rate (Product Analytics, metric-definition-measurement-science): the swap fails (a laboratory audit desk with a daily cap reads the same; inclusion probabilities under a capacity cap are generic survey sampling), so the domain is a backdrop. Written in full below.
- A1.3 Block parking occupancy for a demand-responsive rate change, from paid space-hours that miss free placard parkers, completed from enforcement licence-plate sweeps matched to pay-by-plate sessions (General Statistics, missing-data-censoring-measurement-error): all seven anatomy lines hold on paper, but the abstraction sentence (the part a measuring channel misses is completed from a second channel's sample cell by cell and added) is task275's, approved. Written in full below.
- A1.4 A release's store rating read from reviews posted during a phased release (Product Analytics): regressing each day's ratings on the day's version mix from the analytics is task263's driver (each source's own level measured only in mixtures whose proportions change), spent. Written in full below.
- A1.5 A free plan's monthly limit set from a usage distribution held down by the current rolling-window cap (Product Analytics, metric-definition): the capped rows hand over the signal (stumping Part 3, step 7), and the uncensored demand above the cap needs a fitted model with a free parameter (Gate C).
- A1.6 Checkout funnel losses at a payment step that hands the buyer to a bank app and returns them under a new browser identity (Product Analytics, funnel-journey-analysis): identity resolution carried by Layer 1; once the join is cleaned the call is easy.
- A1.7 Multi-visit web funnels fragmented by WebKit's seven-day cap on script-set cookies (Product Analytics, funnel-journey-analysis): a reflex for web analysts and a reading of a platform behaviour (data semantics).
- A1.8 A candidate primary metric scored for sensitivity on an experiment corpus whose experiments were stopped early on the old primary metric (Product Analytics, metric-definition): the swap fails (a hospital's trials stopped on the old endpoint read the same) and each experiment's planned horizon is a registry column (the schema test).
- A1.9 Push deliveries under APNs store-and-forward coalescing once the 2027 schedule sends more alerts (Product Analytics, metric-definition): devices' offline spells are unobservable at the new schedule's resolution, a free-parameter model (Gate C), and the effect is small outside a few segments.
- A1.10 New items' first-week views held down until the next recommendation-model retrain, carried to a daily cadence (Product Analytics, feature-adoption-diffusion-modeling): task258's abstraction (an effect that reaches only the units a step's condition lets it reach), and the step rides on an as-of time join (time semantics risk).
- A1.11 A legacy feature's distinct users over 2027 read from an event log retained for six months (Product Analytics, feature-adoption): the off-window seasonal users are absent (Gate B) and any projection is a fitted reach model, the field's method as the golden or a fork.
- A1.12 Email-verification losses from deliveries deferred at corporate mail gateways (Product Analytics, funnel-journey-analysis): a root-cause question; the losses are real losses at the step, so the descriptive answer does not move.
- A1.13 A new version's crash rate during a phased release with self-selected manual updaters mixed into the random slice (Product Analytics, metric-definition): a comparison-group question, `causal_design` (banned against task157) and Experiment and Causal Analysis ground.
- A1.14 Durable usage inflated by in-product prompts (Product Analytics, feature-adoption): already dead in this slot (a dated campaign adjusted by reflex).
- A1.15 Search requests' tail latency once the index is split across more shards and every request waits for its slowest shard (Product Analytics, metric-definition): the swap fails (a discharge that waits on every laboratory result reads the same).
- A1.16 Life expectancy of a group under-recorded on death certificates, corrected locally through a linkage to an enrolment register (Sociology, fertility-mortality-life-table-estimation): misclassification among decedents outside the register is absent (Gate B), and carrying the linked rate within a place is task124's abstraction.
- A1.17 Ward peak occupancy against the midnight census (Healthcare, provider-quality-risk-adjustment): the estimand's clock (midnight against hourly) is the step, a WHAT fork (stumping 1.2).
- A1.18 Claims-based disease prevalence by area with practice-dependent coding intensity (Healthcare, provider-quality-risk-adjustment): task271 v1's driver (a risk property recorded at other units), and the honest label `composition_mix` is banned against task166.
- A1.19 Small-area support for a ballot measure by MRP with engagement-driven nonresponse corrected through voter-file turnout (Political Science, small-area-public-opinion-estimation-mrp): several defensible model specifications split the districts near the line (Gate C).
- A1.20 Brand duplication inflated by shared store access (Marketing, segmentation-market-structure): the honest label `composition_mix` is banned against task166 and partitioning by distribution is a known correction in the duplication-of-purchase literature (reflex).
- A1.21 A port passenger survey whose interviewers fall behind at peak hours, so realised sampling rates fall under the designed interval (Survey Research, sample-design-allocation-weighting): post-stratifying by hour is a grouping (stumping 1.1c), which the data separate by reflex.
- A1.22 Plan-limit and pricing replays (seat licences, AI token costs under a new cache rule, per-organisation rate limits) over the 2026 history (Product Analytics, metric-definition): executing a filed plan rule over the history is rule application.
- The four strongest written in full, as the orchestrating session asked. A1.1: default path, each matured monthly cohort (November 2024 to October 2025) built from the accounts table's sign-up date and country, a member retained when the analytics export shows a session in the twelfth month after the sign-up month, pooled by market (or cohort rates averaged, or a Kaplan-Meier on the last active month), the market with the highest rate named; the analytics vendor's own retention dashboard agrees because the vendor honours the same erasures; ends on the market whose leavers erase most (the prototype: Germany, 0.268, against Spain 0.210). Golden: retention over the month's sign-ups, the erased members placed in their cohorts by the account id's order among surviving ids and their country from the request register's residence field, counted not retained unless the erasure came after their twelfth month, those few bounded both ways: Spain, 0.192, bounds 0.190 to 0.195, Portugal next at 0.181. Swap: holds (a hospital cannot erase a patient's record under records-retention law and a utility keeps a leaver's account for years, so the route that removes leavers does not exist there). Anatomy: Actor holds (whether a sign-up later erased their account has no column; the erased are absent), Link holds (the register keys requests by an account id the accounts table no longer holds; the cohort comes from the id order), Reflex holds (the cohort retention table files the wrong market), Back-test holds (the vendor dashboard agrees with the survivors), Second use holds (the register sits for a GDPR one-month completion ask), Shock open (the high-erasure markets lead the survivors' ranking by a visible margin), Pins hold (the plan files retention over the month's sign-ups and no sentence names erasure). Bin: margins 1.08 on the survivors and 1.06 on the sign-ups, both under the 1.15 floor, with erasure shares of 9 to 37 per cent of sign-ups; realistic shares of 10 to 25 per cent bound the swing. Prototype: a seeded replay of ten markets' sign-ups, monthly activity and erasure behaviour (leavers erase at a market-specific rate, stayers rarely, a delay after the last session), run in the session scratchpad and not kept in the pack. Guard: BLOCK as A1.1 states. A1.2: default path, each request's latency weighted by its trace's recorded sample rate, the share over one second, which reconciles with the load balancer's per-minute counts within 2 per cent on monthly volume and understates the peak-minute tail; swap fails; Actor, Link (kept traces per second against the load balancer's counts), Reflex, Back-test, Second use, Shock and Pins hold on paper; bin not reached; dead on the swap. A1.3: default path, paid space-hours over available space-hours by block and rate period, validated on the 2019 sensor pilot's low-placard blocks; golden adds the unpaid occupancy the sweeps read cell by cell; swap holds; all seven anatomy lines hold; bin a ratio estimator with a corridor; dead on task275's abstraction. A1.4: default path, the rating before and after the release date; golden the daily rating regressed on the day's version mix; swap holds; Link holds (the store's reviews carry no version, the mix comes from the analytics); Shock open; dead on task263's driver.
- A2.0 (2026-11-03, architecture 2's draw): the count of vehicles held over five minutes as the deciding quantity. Died
  on the prototype: with the bridge near its capacity the count above five minutes moved by a factor of four between
  neighbouring storage settings, so the graded figure had no stable bin; the deciding quantity moved to the closures'
  vehicle-hours, whose spread across every reasonable convention is about three per cent.
- A2.1: the first card check BLOCKed on `ban.pattern` (C against task241) and on the older same-puzzle and same-driver
  tests against task147 and task159 with G7 decisive; G7 with pick_one_of_n hard-blocks against task307 inside the
  twelve. Redrawn to pattern none with G8 decisive and differentiation lines against task147 and task159.
- A2.2: a downstream signal 400 metres beyond the crossing. Rejected: the estimand's section would have to reach it at
  every crossing, and a far count site that counts departures records the slow discharge directly, a back-test that
  refutes the closure model at the stump crossing in plain sight.
- A2.3: approach counters that count both directions. Rejected for the same reason: the departure lane is a Newell
  input-output measurement of the paced discharge, a second route to the golden that needs no network walk.
- A2.4: vehicle-actuated bridge signals with logged greens. Rejected: the greens on a morning without closures are
  unknowable, so the comparison the brief files has two readings (Gate C); fixed-time shuttle working in the
  morning plan closes it.
- A2.5: a signal lost-time convention left open. Rejected after measuring it: two seconds of lost time a green moved
  Mill Lane's figure by 31 per cent, far outside any bin; the timing register's own note files effective green as the
  displayed green.
- A2.6: crossing, county and bridge names drawn as invented place names (Sallowby, Tewsley, Hawsby). Renamed to
  descriptive road names under H21: two of them sat within two letters of real villages.
- A2.7 (2026-11-03, architecture 2 spent at stage 4 after four determinism judge rounds): the queue survey, the
  default path's validation organ, agreed with the no-blocking replay and contradicted the world, and an honest
  survey names Mill Lane at a glance (a mean queue at the barriers' rise of 37.7 vehicles against 28.6, westbound
  rows to 113 against at most 53 elsewhere), so no honest survey both agrees with the world and keeps the stump; the
  finite-storage rule the golden needs could only be filed by stating most of the decisive step. The general lesson:
  a validation record of the default path that is true only under the wrong mechanism is a certified record blessing
  the wrong method, and when the honest record reveals the answer, the stump is a surface read. The level crossing
  world, its survey and its closure replay stay dead.
- A3.1 (2026-11-03, architecture 3 search, each dead at the screens before any data was cut): part-load NOx from
  dry low-NOx combustors (Jensen at the period mean is task229's and task187's driver, part-load factors task450's);
  tidal speed through the water (task482); out-of-home loop and dwell audiences (task281); adherence variants
  (task281, and task270 v8's supplier-filled supply); historian deadband and compression (task486, and the swap
  fails); aliasing of sampled series (task241, task249, task251); radio day-after recall, retransmission blackouts and
  panel reporting weeks (dead in task271's and task281's notes); the dissimilarity index's small-unit bias,
  tempo-adjusted fertility, emigration in old-age death rates, capture-recapture, interval-censored onsets and
  testlets (spent, task262, task265, task123, task236 and the notes that list them); care-home falls with held beds,
  FX last-look re-trades and infusion pump dosing (each step settles the population or the outcome, the WHAT pincer,
  or is a field reading); not-reached items (the golden is the field's own method and the scoring rule forks);
  bonus hunger in claim reporting (a free behavioural model); analyser carryover (linear and small); a steering
  column's rake arc against a converter's adjustment box (a field reading or one cheap comparison, prototyped as
  `proto_cab`); survey multiplicity and respondent-driven sampling, legislative cohesion, multilevel regression and
  poststratification, segregation indices (spent or forked across the field's estimators); retest lift, intensive
  sampling RMS moves, reporting-cost claims, slot landing and subscores (task270's lineage); pooled testing,
  age-length keys and glycolysis in delayed specimens (screened dead in task307's, task482's and task274's notes).
- A3.2 (2026-11-03): the first cut of this world put one vision angle per cab in the standard; one standard angle for
  every cab replaced it (a per-cab angle is a rule the reader executes), and the FD35 header was raised so the
  shortlist reads as a real shortlist (the first tuning failed a quarter of all drivers on the RD43 cabs).
- A3.3 (2026-11-03): the first ask layer (drivers' musculoskeletal absence by hub, and weekly driving hours by hub
  from card sessions) was tied to the call only by grammar (H18), and its devices were filed rules a careful solver
  executes (episodes running through rest days, a spare card's sign-out); replaced by the shortlisted converters' and
  chassis' record on the service's own fleet, a second measure per candidate on rows the call never reads.
- A3.4 (2026-11-03): the first tuning left Pennick FD35 second on the default path, so a solver setting Wrenfold FD35
  aside for any reason at all landed the call; the RD43 package was retuned so the other Wrenfold cab sits second and
  only a reason that removes both Wrenfold cabs reaches Pennick.
- A3.5 (2026-11-03): reused fleet numbers alone carried three quarters of the ask layer's protection (one finding
  over a third of the ask weight, the cap `ceiling.py` asserts); a unit's miles now run from the odometer entered at
  fitting and the definitions no longer spell out calendar days, so each ask figure needs two corrections and no
  single device lifts the cracker past 9.2 points.
