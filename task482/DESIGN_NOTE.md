# task482 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 8, drawn 2026-10-23 after architectures 1
to 7 were spent at stage 4: a fresh world and pack in the ETL objective, a regional pharmacy chain choosing the stores
whose vaccine refrigerators it replaces before the 2027 respiratory vaccine season, on the hours each store's vaccine
spent above 8 degrees C in 2026.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task482.json` (architecture v8, lineage v1 to v7 spent), registered
  2026-10-23 after a pull, `check` re-run on the filed card: PASS. `test.same_driver_older` against task477 (gap
  objective, G3, method or model selection) is answered by the card's differentiation: task477 re-composes a recorded
  total by its payment schedules' weekdays; nothing here is re-dated, a temperature record is carried through a
  measured lag before it is counted.
- **Redrawn at the draw, and why the labels are the honest ones.** The first form of this draw was a public health
  district's childhood vaccine program (government_agency, programme_officer, monitoring_export). After the pull,
  task171 v4 (filed 07:49) put government_agency and programme_officer in the window and task478 v7 monitoring_export.
  The world was redrawn rather than relabelled: a regional pharmacy chain that grew by buying three smaller chains,
  each with its own logger make, replacing store refrigerators from its own capital program
  (retailer_or_ecommerce; the director of pharmacy operations runs that program, operations_director; the chain's
  capital committee approves the list, committee_or_panel). The context artifact is the stores' temperature logs
  (operations_log): each store downloads its logger's log of the refrigerator's temperatures, and that log, not a
  dashboard, is what the decision is read from; the pilot's cloud export is the minority record. The first personas
  (Amanda Beck, then Darrell Cunningham) were set aside on `people.first` against task104 and task120, and the
  geography is a Midwest state so it does not repeat task478 v7's unnamed state.
- **Pairing:** General Statistics & Data Science, task type `data-integration-record-linkage-entity-resolution`, which
  serves ETL: each store's vaccine refrigerator temperature record, kept through 2026 by one of three data logger
  makes (each logging in its maker's layout, unit and clock) and, at ten pilot stores from mid-year, by a wireless
  in-carton sensor, conformed into one record per store of the vaccine's temperature, the record the replacement list
  reads. Two records of one refrigerator kept by instruments whose response differs are integrated by carrying one
  through the other's response (the precedent is task466's two observation mechanisms in one record).
- **The decision and the quantity:** Penwick Pharmacy runs thirty stores; every store stocks and administers vaccine
  (influenza, COVID-19, RSV, pneumococcal, shingles, Tdap, hepatitis and the childhood series for its clinic stores).
  Its Vaccine Storage and Handling Standard (revised 2026) puts into the 2027 capital program a new pharmaceutical-grade
  refrigerator, installed before 1 September 2027, for every store whose vaccine spent a cumulative 24 hours or more
  above 8.0 degrees C in calendar year 2026. The quantity is each store's 2026 hours with its vaccine above 8.0 degrees
  C; the call is the set at or above 24. Forward facing: the list sets which stores' vaccine sits in new refrigerators
  through the 2027 respiratory vaccine season.
- **Shape:** `10`, a scorecard against one threshold: thirty stores' 2026 hours in whole hours, replaced or not, the
  nearest store below the line and its shortfall; asks on records the call never reads (fixed at stage 2), a chart's
  named parts and the two files.
- **Strategy:** `other` (no family on the list states it: an instrument's record is carried through the response of
  the quantity it stands for, measured where a direct instrument ran beside it); Gate G `method_or_model_selection`;
  gap `objective` (a logger's readings are correct for its probe and are not the vaccine's temperature the
  replacements are decided on); pattern none; generators G3 (the record against what the vaccine went through,
  decisive) and G16. Layer 2 family `estimation_fit`, pattern `own:a fast instrument's record carried to a slow
  quantity through the response a parallel run measures`. Calibration organ `parallel_run_overlap`: the two weeks each
  pilot store's old logger kept recording after its in-carton sensor went in.
- **World:** an unnamed U.S. Midwest state; Penwick Pharmacy and its pharmacy operations; logger makes Frostline,
  Kelvra and Brumal (one per acquired chain); the Tellvane wireless monitoring system from Tamberlane Sensing; the
  chain's vaccine wholesaler, Meridale Pharmaceutical Distribution. People from `guard.py names --geo us --seed 482`
  and `--seed 4821`: Breanna Graham (director of pharmacy operations) and Julia Kaufman (the pilot's project lead).
- **Forcing fact:** the capital committee approves the 2027 refrigerator list in February 2027 so the units are
  installed and qualified before 1 September 2027, ahead of the respiratory vaccine season.
- **Forum and forcing event:** committee_or_panel, season_or_peak. Organisation retailer_or_ecommerce; role
  operations_director.
- **The physics:** a data logger's probe sits in a small sealed bottle of glycol (5 mL) and follows the refrigerator's
  air with a time constant of a few minutes; the vaccine in its cartons on the shelf follows the same air with a time
  constant of most of an hour. A delivery restock or inventory count holds the door open for minutes and the air near
  the shelves climbs toward the room's temperature: the probe crosses 8 degrees C, the vaccine warms by a degree or two.
  A busy afternoon of door openings keeps the air and the probe near 8 for hours; the vaccine follows the hourly
  average. A power outage, a door left ajar overnight or a failing thermostat warms the cabinet for hours, and the
  vaccine follows it up, late, and stays warm after the air has recovered.
- **Data-native sentence:** at the ten pilot stores the old logger kept recording for two weeks after the Tellvane
  sensor went into a vaccine carton on the same shelf, and in those weeks the logger crossed 8 degrees C on every
  restock while the in-carton sensor stayed under 8, and lagged the logger's rise and fall through every warm spell
  by about three quarters of an hour, so a logger's hours above 8 belong to its probe and not to the vaccine.
- **Default path and golden, by name:** each store's logger readings taken as its vaccine's temperature (each pilot
  store's in-carton sensor from its installation) replace the refrigerator of every store whose probe crossed 8 through
  restocks and busy hours, the busiest stores among them; the same records carried through the vaccine's response
  fitted on the overlaps replace the stores whose vaccine itself warmed through outages, doors left ajar and failing
  thermostats, about half as many. Names and figures are set at the build from `generator/figures.json`.
- **The WHAT screen.** Population: the thirty stores and each one's vaccine refrigerator. Outcome: the hours the
  vaccine spent above 8.0 degrees C. Unit: hours. Window: calendar 2026, local time. Comparison: 24 hours. The
  decisive step settles none of them: it is what temperature the vaccine was at while only a logger recorded the
  refrigerator, which no filed rule or procedure states.
- **Sources, one line each:**
  - the national vaccine storage and handling guidance's description of digital data loggers with buffered probes
    (a probe in a sealed bottle of glycol, glass beads or sand), read at intervals of 30 minutes or less;
  - packaged pharmaceutical product temperature practice: a product's temperature follows its surroundings through
    its packaging's thermal response, a first-order lag in the simplest description, measured by placing a sensor in
    the product's own pack;
  - first-order sensor dynamics: an instrument's reading follows its medium with its own time constant.
- **Surface screen (stage 3):** `guard.py surface` promoted three pairs on card labels, none on a driver. task481
  (shipped) shares the calibration form, a parallel-run overlap: there a dual-coded window gives conversion rates
  whose case mix differs from the months restated; here an old logger's last two weeks beside an in-carton sensor
  give a dynamic response, a shared organ under two drivers (clone-check's shape echo). task477 (shipped) shares gap,
  pattern and Gate G, answered on the card (re-dating payments by schedule against carrying a record through a lag).
  task484 (this lane, paused at stage 1) shares the pattern and decision type; its re-root draws off both.
- **Same-puzzle and same-driver tests:** (objective, none, designation_set) and (objective, G3,
  method_or_model_selection) against the last twelve builds, lineage included: no match in the last twelve; the older
  task477 match is differentiated on the card.
- **Abstraction test:** the nearest drivers stripped of nouns: task189 averages measurements known only to lie below a
  limit; task464 v2 links a new instrument's scale to an old one by a sample measured on both and warns against the
  regression's shrinkage; task478 v5 divides each instrument's reading by a bias measured on a component of known size;
  task466 enters two records kept under different observation mechanisms into one likelihood. Here no scale, bias or
  censoring separates the instruments: each logger reads its own probe correctly, and the difference from the vaccine is
  in time alone, a response measured where both instruments recorded one refrigerator and carried through every reading
  before the hours above a limit are counted.

## Default path

1. Read the Vaccine Storage and Handling Standard's section 7.3 on the 2027 replacements: a store whose vaccine spent a
   cumulative 24 hours or more above 8.0 degrees C in calendar year 2026 has its refrigerator replaced before
   1 September 2027, a record counting its ten minutes when the vaccine's temperature at its time stamp was above 8.0.
2. Conformed the three makes' exports to UTC and degrees C (Frostline's local times with their offsets, Kelvra's
   Fahrenheit and UTC with its one repeated day, Brumal's UTC-6 all year), joined each logger to its store through
   the monitoring roster, a replaced logger's two serials in sequence.
3. At each pilot store, took the Tellvane in-carton sensor's readings from its first reading (the device of record from
   installation, standard 6.4) and the store's logger before it.
4. Took each logger reading as the vaccine's temperature, as a buffered probe is meant to give it, counted each store's
   2026 records above 8.0 degrees C at ten minutes each, and summed the hours.
5. Compared each store's hours with 24.

Ends on: the 2027 replacements go to stores 103, 106, 108, 201, 204, 206, 207, 301, 303 and 309.

Golden: the 2027 replacements go to stores 103, 106, 109, 201, 206 and 303.

## Stump sentence

The default path takes each store's data logger readings as its vaccine's temperature and replaces the refrigerators
of stores 103, 106, 108, 201, 204, 206, 207, 301, 303 and 309, because a logger's probe in its 5 mL glycol bottle
follows the refrigerator's air within minutes while the vaccine in its cartons takes most of an hour, so the probe
reads above 8 degrees C through every defrost swing, quick restock and busy afternoon the vaccine rode out, and ends a
propped-door delivery's excursion long before the vaccine cools; carried through the vaccine's response, a first-order
lag whose time constant the two weeks each pilot store's old logger kept recording beside its new in-carton sensor fix
at about 42 minutes, the records replace stores 103, 106, 109, 201, 206 and 303: five of the default's ten (108, 204,
207, 301 and 309) drop out and store 109, whose season of propped-door deliveries the logger cut short, comes in.

## Three rules

Task type: data-integration-record-linkage-entity-resolution (General Statistics & Data Science), a task type serving
Data Extraction & Conformation (ETL): thirty stores' refrigerator temperature records kept by three data logger makes and, at
ten pilot stores from mid-2026, by an in-carton wireless sensor, conformed into one record per store of the vaccine's
temperature through 2026, the record the replacement list reads.

Domain test: the deciding quantity is each store's 2026 hours with its vaccine above 8.0 degrees C; integrating two
instruments whose response differs enters each logger record into the vaccine's record through the vaccine's thermal
response, which the pilot stores' fourteen-day overlaps measure, and replacing that with the generic union of the two
records (the logger's readings wherever no in-carton sensor ran) replaces about twice as many refrigerators.

Swap: General Statistics, so the swap is of the method: replace the response-carried record with the union of the
instruments' readings and the set roughly doubles; and with another field's nouns ("beds occupied" for "vaccine
temperature") there is no carton, no glycol bottle and no thermal response for a reading to be carried through.

Layer 1: three logger makes' exports, each in its maker's layout (Frostline in Celsius with local times and their
UTC offsets, the November fall-back hour twice; Kelvra in Fahrenheit and UTC behind a three-line preamble, one day
exported twice; Brumal in monthly download reports on UTC-6 all year), two loggers replaced mid-year under new
serials, battery-change gaps in quiet hours, the pilot vendor's cloud export in UTC keyed by sensor id, and in the ask
files the wholesaler's 11-digit NDCs against the item master's 10-digit forms, packages against doses, the Lindqvist
stores' old wholesaler accounts before April, and work finished in December invoiced in January: each is what these
systems write, none is placed to be caught, and no reading of them moves the call (asserted in checks.py, X1 and
X3).

Layer 2: estimation that fits the data (estimation_fit): the vaccine's temperature is not recorded at most stores for
most of the year and has to be estimated from the logger record through the vaccine's response, a first-order lag
whose time constant the pilot stores' overlaps fix; counting the logger's own time above 8 degrees C counts every
restock and busy afternoon the vaccine rode out.

Decisive step: carrying each logger record through the vaccine's thermal response, a first-order lag of about 42
minutes measured on the pilot stores' two-week overlaps where the old logger's probe and the in-carton sensor recorded
the same unit, before the hours above 8.0 degrees C are counted.

Not semantics: every field reads as written (each logger's probe temperature in its own unit and clock, the in-carton
sensor's temperature, the roster's dates and serials); read correctly, the logger's readings are still its probe's,
the easy route counts them as the vaccine's, and only the vaccine's response, which no field or definition states,
separates the two.

Not rule application: the standard files the WHAT (the vaccine's temperature, calendar 2026 local time, above 8.0
degrees C, 24 hours, a record counting its ten minutes by the vaccine's temperature at its time stamp) and no rule or
procedure says how a logger's reading becomes the vaccine's temperature; the enumerated family (the readings as
recorded, 30 and 60 minute duration filters, a 10-degree peak filter, the defrost swings dropped, the delivery
excursions dropped, the overlaps' hours ratio, 30 to 120 minute moving averages, the first-order lag) spreads the set
from one store to eleven across eleven distinct sets; the standing family (the lag fitted per make, pooled and per
pilot store, half a minute either side, the record opening or closing its interval) files one set and every store's
whole hours identically; and what rules out the rest is the overlaps' own fit, which a reader reaches only by using
the logger's two weeks past the device of record's start: 0.06 degrees C for the lag against 0.39 for the readings as
recorded and 0.12 for the best moving average (checks.py G1, G5).

Analyst test: with every field and rule read correctly, a strong analyst takes each store's logger readings as its
vaccine's temperature, as a buffered probe is meant to give it (each pilot store's in-carton sensor from its first
reading), counts the 2026 hours above 8.0 degrees C and replaces stores 103, 106, 108, 201, 204, 206, 207, 301, 303
and 309: the default path's Ends on (checks.py T1 on the clean truth, T2 on the pack).

Estimand: the Vaccine Storage and Handling Standard (revised 2026), the 2027 replacement section: the population (the thirty
stores' vaccine refrigerators), the outcome (the hours the vaccine spent above 8.0 degrees C,
each record standing for the ten minutes that follow its time stamp), the window (calendar 2026, local time), the
unit (hours) and the comparison (24 hours), in sections 6.3 and 7.2 to 7.3.

No decoy: nothing is planted: every logger is a compliant buffered-probe logger recording as built, the overlaps are
the pilot's routine changeover (the old logger collected at the first check-in visit), and no memo, draft, briefing or
stakeholder figure argues the loggers' hours.

No certified replay: the method is not recovered by reproducing certified or published figures; the chain publishes
no store's hours, and no figure in the pack ties only under the golden.

Lesson: a record kept by a fast instrument is not the slow quantity it stands for; integrating it with a direct
record means carrying it through the slow quantity's response, measured where both recorded the same unit, before any
threshold is counted; no build on file teaches carrying a record through a dynamic response.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, each logger's readings as the vaccine's temperature (the default path: ten stores) | the standard's "the vaccine's temperature" beside the loggers it requires: fires | each make's temperature column: fires | a buffered probe stands for the vaccine: fires | none | the clocks and units conformed: fires | a count of records above 8.0 | readable |
| R1, a minimum excursion length (30 or 60 minutes) or a peak above 10.0 before a run counts | none | the runs above 8.0 in the records: fires | brief door openings do not count: fires | none | none | one filter per run | readable |
| R2, a moving average of the logger record (30 to 120 minutes) | none | none | smoothing a noisy record: fires | none | none | one rolling mean | readable |
| R3, the overlaps' ratio of in-carton hours to logger hours applied to each store | none | the roster's two devices in the pilot stores' changeover weeks | scale by a calibration ratio: fires | the overlap weeks | none | one factor | readable |
| R4, the defrost swings dropped (runs under 9.5 degrees C lasting 25 to 75 minutes) | none | the twice-daily pattern in the household units' records | recognise and drop a defrost cycle: fires | none | none | one pattern filter | readable |
| R6, the excursions that start at a Meridale delivery dropped | the standard's delivery days | the invoices' delivery times beside the records | a restock is not a failure: fires | none | none | one join and a filter | readable |
| R5, the lag fitted on the overlaps and carried through every logger record before the hours are counted (decisive) | none: the standard files the vaccine's temperature and the counting, not how a logger record becomes it | none: no column holds a time constant or a carton's temperature outside the pilot stores' weeks after installation | none: the field's convention is that a buffered probe is the vaccine | the overlaps exist only implicitly, a collected logger's record running two weeks past its store's installation date in the roster | none | an exponential filter whose constant only a fit gives | silent |

R5 is silent: the in-carton sensor is the device of record from installation, so a solver never needs the old
logger's last two weeks; nothing labels those weeks a parallel run; the probe's 5 mL bottle is the national guidance's
buffered probe, the one the field treats as the vaccine; and the default path's answer reconciles (every logger reading
above 8.0 is counted, no record conflicts with another device of record).

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the vaccine's temperature | the temperature of the vaccine in its cartons (standard 7.2), read by the in-carton sensor where one ran and estimated from the logger record elsewhere | the logger's probe reading | the default ten | standard 7.2's definition, and the overlaps, where the probe crosses 8.0 at every restock while the carton stays under it (fit 0.39 degrees C as recorded against 0.06 through the lag); asserted |
| SF2 | above 8.0 degrees C | strictly above | at or above | same call; store 206's whole hours move from 52 to 54 on in-carton readings of exactly 8.0 | standard 7.3's "above 8.0"; asserted |
| SF3 | a cumulative 24 hours or more | at or above 24.0 | above 24.0 | same call | asserted: no store within an hour of 24 (the nearest at 20.17 and 27.17) |
| SF4 | calendar year 2026 | local (Central) time, 1 January 00:00 to 31 December 24:00 | the UTC year | same call, same whole hours | standard 7.3 ("local time at the store") and the store list's time zone; asserted |
| SF5 | each record stands for the ten minutes that follow its time stamp | the record holds over the next ten minutes | the record stands for the ten minutes before it | same call, same whole hours | standard 6.3; asserted |
| SF6 | the device of record at a pilot store | the in-carton sensor from its first reading | the logger until it was collected | same call, same whole hours | standard 6.4; asserted |
| SF7 | each make's clock | Frostline local with its offset, Kelvra UTC, Brumal UTC-6 all year, Tellvane UTC | Brumal read as daylight time; Kelvra's UTC read as local | the overlaps' fit fails (0.24 and 0.38 degrees C against 0.06) | each export's own header; asserted |
| SF8 | Kelvra's unit | degrees Fahrenheit, converted | read as Celsius | not a live reading: every Kelvra store far over the line | the export header; asserted |
| SF9 | gaps in a record (a battery change, a replaced logger) | each record covers its own ten minutes; a gap's time is covered by no record | the last record held through the gap | same call, same whole hours | standard 6.3; asserted |
| SF10 | the lag's grouping | one constant per make, fitted on that make's pilot stores (42.2, 42.2 and 41.9 minutes) | one pooled constant (42.1); each pilot store's own (41.5 to 43.6) | same call, same whole hours | asserted over the three groupings and half a minute either side |
| SF11 | the estimate's start | the first record of the year | the carton at the 5.0 setpoint | same call, same whole hours | asserted |
| SF12 | a store with a replaced logger | one record for the store's refrigerator, the two loggers in sequence | two units | same call | the roster's serial history; asserted |
| SF13 | ask A's balance | the 2025 year-end count, plus receipts by delivery time and transfers in, less doses administered, written off and transferred out, less the 2026 year-end count, each flow between the two counts' own closing times | the calendar year's flows with the counts as its ends | ask figures only | the data: each count's own closing time (a device, Ask sheet); asserted |
| SF14 | ask A's doses | doses, packages times the item master's doses per package | packages | ask figures only | the item master; asserted |
| SF15 | ask B's spend | what Brannon invoiced, sales tax included, for work completed in 2026 | the export's amount column summed by row | ask figures only | the data (devices, Ask sheet); the agreement's tax clause; asserted |
| SF16 | rounding | each store's hours from the unrounded estimate, rounded once to the whole hour; doses whole; dollars whole | rounding per record or per month | same call, same figures | asserted |
| SF17 | a record's vaccine temperature | the estimate at the record's time stamp | the mean of the estimate over the record's ten minutes | same call; five stores' whole hours move by one | standard 7.3's counting sentence ("a record counts its ten minutes when the vaccine's temperature at its time stamp was above 8.0"); asserted |

## Ladder

Measured on the cut pack (thirty stores, the overlaps' lag fitted per make at 42.2, 42.2 and 41.9 minutes) and
asserted in `checks.py`.

| Rung | Construction | Stores at 24 hours or more |
|---|---|---|
| R0 (default) | each logger's readings as the vaccine's temperature | ten: 103, 106, 108, 201, 204, 206, 207, 301, 303, 309 |
| R1a | runs above 8.0 counted only from 30 minutes | eight: 103, 106, 201, 204, 206, 301, 303, 309 |
| R1b | runs counted only from 60 minutes | three: 106, 201, 206 |
| R1c | runs counted only when they peak above 10.0 | five: 103, 108, 206, 207, 303 |
| R2 | moving averages of 30, 45, 60, 90 and 120 minutes | eleven, nine, seven, seven and seven, each a different set from the golden (306, 108, 301 or 208 in) |
| R3 | the overlaps' hours ratio applied to every store | one: 206 |
| R4 | the defrost swings dropped | nine: 103, 106, 108, 201, 204, 206, 207, 301, 303 |
| R6 | the excursions that start at a Meridale delivery dropped | six: 106, 201, 204, 206, 301, 309 |
| R5 (golden) | the lag fitted on the overlaps, per make or pooled, carried through every record | six: 103, 106, 109, 201, 206, 303 |

The default path's error is two-sided: it replaces five refrigerators the vaccine did not need (the household units
204, 301 and 309 on their defrost swings, the twice-weekly restockers 108 and 207) and misses 109, whose season-long
propped-door deliveries the vaccine felt for longer than the logger recorded them.

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | the thirty stores in the chain's store list, each one's vaccine refrigerator | filed (standard 7.3, the store list); C1 |
| 2 Unit of account | one store, one refrigerator | the question names the store; SF12 |
| 3 Attribution window | calendar 2026, local time | filed (standard 7.3); SF4, asserted |
| 4 As-of dating | the records as exported in January 2027 | the exports' own ranges; C1 |
| 5 Version basis | one export per make, no revisions | C1 |
| 6 Denominator | none: an hours total, not a rate | not live |
| 7 Weighting | none: each record stands for its ten minutes | filed (standard 6.3) |
| 8 Window length | the full year | filed |
| 9 Boundary inclusivity | above 8.0; 24 or more | filed; SF2, SF3 asserted |
| 10 Rounding path | from the unrounded estimate, once | SF16, asserted |
| 11 Tie-break | none: no store at 24.0 | C1, asserted margin |
| 12 Maturity and censoring | the year is closed; every store's record complete | C1 |
| 13 Order of operations | conform clocks and units, carry through the lag, count | the counting is filed; the lag follows conforming; C1 |
| 14 Row order | records ordered by time; Frostline's fall-back hour by its offset | C1, asserted over shuffled rows |
| 15 Duplicate resolution | one Kelvra day exported twice | exact duplicates collapse; same call, asserted |
| 16 Identity normalisation | logger serials to stores through the roster | the roster; C1 |
| 17 Netting against gross | none | not live |
| 18 Dimensional units | Kelvra in Fahrenheit, the rest Celsius | SF8, asserted |
| 19 Code and status semantics | the roster's device roles | dictionary semantics; never the stump |
| 20 Integerisation | whole hours, whole doses, whole dollars | SF16 |
| 21 Clause scope | the replacement clause covers the year's vaccine hours at each store | filed (standard 7.3) |
| 22 Forward window contents | the 2027 replacements go to the stores the 2026 hours name | filed (standard 7.3) |

## Literal reader

Executed word for word, the prompt and standard 7.2 to 7.3 ask for each store's 2026 hours with its vaccine (the
vaccine in its cartons) above 8.0 degrees C, each record standing for its ten minutes; standard 6.4 makes the in-carton
sensor the device of record from each pilot store's installation; nothing files the vaccine's temperature as the logger's
reading, and the overlaps show they differ, so the literal estimand is unobserved outside the pilot stores' later
months and has to be estimated from the logger record. The only estimator that fits the overlaps at their noise is the
lag (measured fits: 0.39 degrees C as recorded, 0.12 to 0.25 for moving averages, 0.06 for the lag), and its
groupings file one set (SF10). The golden is the literal estimand's estimate, not a reading of a term.

## Oracles

None ties only under the golden. The in-carton sensor's readings are the vaccine's temperature where they exist and are
used directly by every route; the store list, the roster and the makes' headers are conversions every route takes. No
file reports any store's hours above 8.0 or ranks the stores on them; no export carries a time-above-limit summary.

## Leak sweep

`leak.py --asof 2027-01-25` (stage 3, the renamed pack): REVIEW, no LEAK line. One line per REVIEW class:

- Store numbers in Schedule A of the Brannon agreement and in the Tellvane pilot plan's store table: identifiers in
  each document's own table, beside sites, units and installation weeks, never beside hours; harmless.
- The standard carries the call's words (Penwick Pharmacy, vaccine refrigerators, stores, 2027 respiratory): it is
  the governing standard whose section 7.3 files the criterion; harmless.
- Design-note vocabulary in the quotes, the pilot plan and the standard (logger, temperature, record, standard,
  minutes, sensor): the field's ordinary words; none of the three names a lag, a response, the vaccine trailing the
  probe or any use of the logger's last two weeks (`checks.py` I4 sweeps lag, time constant, parallel run and
  overlap); harmless.
- Dates after the as-of in the write-off log: lot expiration dates, future by nature; harmless.

## Ask sheet

Two asks, both on files the call never reads: Meridale's invoices, the administrations, the write-off log, Meridale's
credit memos, the store transfers and the two year-end physical inventories (ask A); Brannon's service history and its
agreement (ask B).

- **Ask A, each store's 2026 vaccine doses its stock records leave unaccounted for, whole doses (30 figures).** User:
  the capital committee's packet on vaccine loss. Devices: D8 a clock against a cutoff, at both ends (eight stores
  closed their 2025 year-end count on 30 December 2025 and eight others their 2026 count on 30 December 2026, each
  count's own closing time says so, so the next day's administrations fall after it: in the year the first group
  opens, out of the year the second closes); D1 the same doses in two records (the expired 2025-26 standard-dose
  influenza doses Halvorsen takes back were written off as expired on 1 July and then credited by Meridale, so the
  credits are not a second outflow; Corbel's high-dose leftovers are written off and never credited); D2 a label stored
  before a silent switch (the write-off log recorded multi-dose vials as vials until the 1 June 2026 inventory update
  and as doses after, the quantity column unchanged, the cost column a vial's before and a dose's after). Every store
  carries D1 and at least one of D2 and D8. Hazards: packages against doses, 11-digit against 10-digit NDCs, the
  Lindqvist stores' old ship-to accounts before April.
- **Ask B, each store's 2026 refrigerator service spend with Brannon, whole dollars as invoiced with sales tax
  (30 figures).** User: the packet's maintenance-cost line. Devices: D2 a label stored before a silent switch (the
  amount column is before sales tax on invoices dated before Brannon's 1 July 2026 platform move and includes it after;
  every store has an invoice from before it, and the maintenance-only invoices at Schedule B's prices show it); D6 an
  allocation at the wrong weight (before the move each morning's two-store maintenance route was one work order and one
  invoice, its amount on both stores' rows, split by each unit's Schedule B price); D6 an event's quantity on every
  line it covers (a multi-visit work order's amount repeated on each visit's row). Hazard: work finished in December
  invoiced in January, both years.

| Ask | What the cracker does | Cracker |
|---|---|---|
| A | the balance with every flow over the calendar year, the counts as the year's ends, write-offs as logged and return credits both taken off | miss |
| B | each invoice's amount once, by the work's completion date, the amounts as exported, a route's amount to each of its stores | miss |

Measured partial handlings on the cut pack: ask A keeps at most 14 of 30 under any handling short of all three devices
(the count times and the credits, 10; the vials and the credits, 14); ask B keeps 10 of 30 with the tax switch found
and the routes missed, 30 with both.

Pair ceiling: 28.5 (the cracker 38 + 7 with none of 60 ask figures, the mirror 5 + 7 with none).

Mirror leakage: 0.0 per cent of ask weight.

Measured by: generator/ceiling.py on the cut pack.

## Layer 1 inventory

- Three logger makes, one per chain the company is made of (Frostline at the Penwick stores, Kelvra at the stores
  bought from Vollmer Drug, Brumal at the stores bought from Lindqvist Apothecary), each exporting in its maker's
  layout: Frostline CSV in Celsius with ISO local times and UTC offsets (the November fall-back hour twice), Kelvra CSV
  in Fahrenheit and UTC behind a three-line preamble, Brumal tab-separated monthly download reports on UTC-6 all
  year, the Lindqvist stores under their old names.
- Tellvane's cloud export in UTC keyed by sensor id; the roster maps sensors and loggers to stores.
- Two loggers replaced mid-year under new serials; battery-change gaps in quiet hours; one Kelvra day exported twice.
- In the ask files: Meridale's 11-digit NDCs against the item master's 10-digit forms, packages against doses, the
  Lindqvist stores' old ship-to accounts before April, the stock extracts running from 30 December 2025, and Brannon's
  invoice dates against work dates, its site names still the acquired chains'.
- Each item is what these systems write; none is placed to be caught, and no reading of any of them moves the call
  (asserted in `checks.py`, X1 and X3).
- The clocks are the overlap fit's prerequisite, so they are loud rather than neutral: each misread (Brumal's UTC-6
  read as daylight time, Kelvra's UTC read as local, Frostline's offsets dropped) puts the fit at four to seven times
  its error with the constant at the search bound, so none can be mishandled silently; the call holds under the first
  two and moves under the third (`checks.py` R2, one assertion per item).

## Architecture 8 record (spent 2026-10-23)

Architecture 8 carried each store's data logger record through the vaccine's thermal lag, a first-order response
fitted per logger make on the two weeks each pilot store's old logger kept recording beside its new in-carton sensor
(42.2, 42.2 and 41.9 minutes), against the loggers' readings taken as the vaccine's temperature (six stores against
ten). At stage 4 (zip ad958ec9) reader B set the pilot stores' loggers beside their in-carton sensors over the overlap
unprompted, fitted the lag as a first-order filter (0.21 of the gap closed per ten minutes, about 42 minutes) and
landed the six stores and every store's whole hours, answering question 6 "an analytical choice" on standard 7.2; it
kept every ask figure too (122 of 122 graded figures, exit 1): the counts' own closing times, the credits found when
per-item balances went negative, the vial write-offs by cost over the per-dose cost, the tax switch by the
maintenance-only invoices at Schedule B's prices, and the two-store routes split by Schedule B. Reader A and the judge
thread were stopped at the spend.

## Architecture 7 record (spent 2026-10-23)

Architecture 7 read each production day's oxidizer outlet from the relation the ten oxidizers' tests trace (a floor of
about 45 ppmv as carbon, 1.8 per cent of the inlet above about 2,500) at the inlet the day's captured VOC and airflow
imply, against each plant's latest test efficiency (Ashcombe 21 and Kelvedon 20 against 29 and 28). At stage 4 (zip
5ab18e48) reader A read the floor straight off the test tables (Ashcombe's 2018 two-press test holds the same 45 ppmv
at half the inlet), rebuilt each hour's outlet as the greater of the floor and 1.8 per cent of the inlet and landed the
five and all 14 whole tons, Part 2 question 1 "none" and question 6 "an analytical choice"; reader B carried each
fixed-fan unit's test outlet to the year through the register's fan-drive column (R4, six plants). Both readers kept
all 28 ask figures: the revision log read, the payment lines parsed, Haldane matched on description. The judge thread
was stopped at the spend.

## Architecture 6 record (spent 2026-10-22)

Architecture 6 set Form 27A's placement scores from the bank difficulties carried from the old platform's field-test
section (positions 61 to 70) to the positions 21 to 70 the unique items take on Northgate Assess, by the position term
the 2026 attempts measure, against the default path's difficulties as filed (29 and 18 against 30 and 19). At stage 4
reader A rebuilt every response at its delivered position, fitted the Rasch model with the anchor block fixed, found
items harder later in the test on both platforms and landed 30 and 19 exactly (29.48 and 18.50), Part 2 question 1
"none" and question 6 "an analytical choice"; it kept 13 of 62 ask figures (the system totals and some twice counts).
Reader B and the judge thread were stopped at the spend.

## Architecture 5 record (spent 2026-10-22)

Architecture 5 designated rapid price growth areas on each dwelling type's own year effect weighted by the census
stock's value, with a pooled hedonic year term as the default path. At stage 4 both readers and the judge's own
derivation took the type-by-stock aggregation by reflex (type medians or type year effects weighted by the census
stock) and missed the call only on the location control (electoral division), which the judge read as unfiled; filing
it hands all three the call, so the decisive step as designed does not stump and the one that held is a fork.

## Tried and rejected
- Architecture 6, item position effects in pre-equating (2026-10-22, spent at stage 4): reader A fitted a Rasch model
  with a position term to the rebuilt attempts and carried the field-test difficulties to Form 27A's positions,
  unprompted by any sentence. The calibration context has to be recoverable for the truth to be fair (the report's
  delivery section and both exports' positions), and once it is, an analyst who knows the field checks the effect the
  context invites; a context effect measured by an obvious model term is a reflex for the field's own analysts.
- Architecture 6 draw (2026-10-22): re-rooted on the author's standing rule (no retirement) with a fresh world. Screened
  before it and dead: a CEMS gap fill on load (guard BLOCK on pattern G12 and strategy population_selection against
  task273, same-puzzle and same-driver spent in five to seven builds, the statutory filing against task249);
  multiplicative against additive seasonality (task146, task147); a moving holiday (task162, task467, task135);
  Denton benchmarking (this slot, below); retroactive eligibility as a denominator still developing (the completion
  driver of task451 and task479 v5); Fellegi-Sunter frequency weights (set aside at task486's draw against task468's
  linker error); the oldest old by extinct generations (task228); non-detects under several limits (task189).
- Architecture 5, the stock's price change as each dwelling type's own year effect weighted by the census stock's
  value (2026-10-22, spent at stage 4): both readers and the judge's first derivation weighted dwelling types by the
  census stock by reflex (the note's "dwellings the 2022 census counts" and the census workbook by type invite it) and
  missed only on the electoral-division control, which the judge read as unfiled (r5a); filing it hands them the call.
  A stock aggregation over a tabulated type mix is a reflex once the stock is the filed population.
- Architecture 5 draw (2026-10-22): re-rooted on the author's standing rule (no retirement); the world and pack of architecture 4 kept, the decisive step moved from the constant-quality regression its reader 9 found to the aggregation that regression skips (each type's own year effect over the stock's value), with the pooled regression now the default path. At registration the v4 identity BLOCKed on own_lineage, gap population on same-puzzle and same-driver (task251 v5), shape 10 and the statutory filing (task249 v6) and filed_standard (task478 v4); redrawn as recorded in the Draw, the circular changed to settle the 2027 fund allocations.
- Ask B's reissued student ids as a 7-digit id equal to the old one plus a campus constant, linked by birth date, sex and ZIP (2026-10-21, stage 4 round 1): both readers resolved it on the person columns and kept all six headcounts (score_reader 50 per cent); re-sited so the new ids share the old form with no arithmetic tie, birth date, sex and ZIP are shared by different students, and the movers' majors are recoded, so only the four-field key resolves it.
- Architecture 1, a coordinating board's instructional grant with four parents' consolidated returns apportioned by a cost model (2026-10-21, spent at stage 4): round 1's two readers split by FTE or total credit hours and missed; both round 2 readers fitted instruction expense on credit hours by level across the standalone campuses, split each parent's return by the modelled cost and landed the call (exit 1). Pricing activity by level from the units that report alone is a strong reader's reflex once the activity file by level ships beside the combined return.
- Architecture 2, regional register error rates from an audit drawn unequally by a risk screen (2026-10-21, spent at stage 4): both readers checked the audit's composition against the register (35 per cent referred against 8), weighted each stratum to the 30 April register and landed the call; both also read the UTC times into local time and dropped the restored companies (asks 28 of 28). A sample whose composition differs from its frame on a shipped flag is reweighted by a strong reader; a stated clock and a restoration notice are seen devices.
- Architecture 3, registration offices put on a timeliness plan from a quarter's median working days with part of the quarter still open at the extract (2026-10-21, spent at stage 4): both readers censored the open applications at their age, took the Kaplan-Meier median and landed the call, and dated payments by the batch terminal day (asks 28 of 28). An open caseload shipped beside a duration cohort, with a paper saying the open ones count, is read as right-censored by a strong reader; a settlement batch file carrying the terminal day is a seen device.
- Architecture 4, areas' house price change for the rapid price growth designation read from a shifting sample of the stock (2026-10-21, spent at stage 4): reader 9 fitted log price on type, floor area, age, newness and the address point file's electoral division with a year term and landed the call; reader 10 left location out and missed; the block purchases' one consideration on every line held both readers (0 ask totals of 32). A constant-quality index is a strong reader's reflex once the note cites the handbook and the attributes ship; location one join away is not a hidden dimension.
- A district's register error rise tested with the spread of the audit's sampled blocks (2026-10-21, screened at the draw): the guard put it beside task261 (subgroup statistics from one clustered sample, their difference's error from the clusters), the same driver.
- Regional quarterly output benchmarked to annual totals by Denton against pro-rata (2026-10-21, screened): Denton's extrapolation holds the end-of-year ratio, which sits within a few tenths of a point of pro-rata's annual ratio, while a trending ratio puts the truth far from both; the separation is too small and the truth not recoverable without forecasting the ratio.
- Architecture 7 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world.
  Screened before it and dead: gross labour-force flows corrected for reinterview misclassification (task244's
  driver); speededness on a timed form (task249's screen); a winner's curse in form assembly (task471's shrinkage
  coin flip); generic price erosion by entrant count (task484 v1's ramp, screened at task478's draw); percent-of-charges
  hospital contracts carried to each hospital's current chargemaster (the swap test reads it as any list-price
  contract); laboratory results harmonised by proficiency-test bias (the reported result is the measurement, so the
  correction is a fork); a cancer registry's completeness by the flow method (task249's screen); common-stack
  apportionment from single-unit hours (task263's unmixing); a concentration-discharge load (task452 v1, task135);
  change of support for block grades (task270, task254, task273 screens); linkage on an address the outcome changes
  (task468's linker error); calculator-type DIF and released-item drift on the item bank (architecture 6's lesson: a
  context an obvious model term measures).
- v7 stage 3, 2026-10-23: the first tuning let each oxidizer's test outlet carried to the year (its concentration on
  each day's air, or its rate over the year's hours) file the golden five, because a fixed-fan plant at the floor emits
  the same rate every day; Larkmoor Graphics was made a concentrated-test, mostly-dilute plant under 25 tons so those
  routes file six (R4, R4m, R4b).
- v7 stage 3, 2026-10-23: press VOC to one decimal: the standing family spreads up to 0.37 tons on a plant, so the
  figure is graded in whole tons, every member 0.19 tons or more from a half (G4); the CSV's used and captured
  columns went with it (free to both top responses), the CSV now the press VOC and coverage.
- v7 stage 3, 2026-10-23: the tuned plants landed on whole tons (29.00, 37.00); moved to ordinary offsets (G5). Days
  below the tests' lowest inlet at three plants opened an extrapolation fork (interpolated efficiency against the
  floor); the low days were raised inside the tested range.
- Architecture 7, 2026-10-23: spent at stage 4. The decisive relation was visible inside one oxidizer's own tests (the
  same outlet at two inlets) and in the register's fan-drive column, and a regenerative oxidizer's outlet floor is
  field knowledge both readers carried; the asks' devices each sat one file away from a careful reader's path (the
  master's revision log in the same workbook, the washer gallons in readable payment text, descriptions beside the
  renumbered items). Next architecture: a decisive step no table displays as a pattern and no column labels.
- Architecture 8 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world, aimed
  at architecture 7's lesson (no table displays the decisive relation, no column labels it). Screened before it and
  dead: vessel propulsion from AIS speed over ground carried to speed through the water by an estuary's tidal streams
  (a port world beside task472 and task474, and a tidal stream table has no other use in an emissions pack, so its
  presence announces the correction); container ships' at-berth auxiliary load by the reefers on board, calibrated on
  shore power meters (a port world, and a reader calibrating on the meters sees the per-call spread with reefers its
  first explanation); a tanker's boiler load at berth by its own steam cargo pumps on discharge (the at-berth tanker
  rules' own reasoning, a reflex once the transfer log is joined); dairy lagoon methane through the lagoon's
  temperature lag behind the air (the rate model is a filed procedure, and four inspection readings a year cannot fix
  the lag deterministically); switcher locomotives' idling through the start-stop system's restart temperature (a
  rate carried across a weather covariate, task478 v7's driver); crematory mercury by the decedents' dental cohort (a
  composition mix one survey table hands over); breaker SF6 leak rates from temperature-uncompensated pressures (the
  gas temperature at each reading is not recoverable). A cold-chain prototype (thirty-six refrigerators, probe 6 minutes,
  carton 48) put the logger's own hours at two to ten times the vaccine's, the default qualifying 29 against 12, with
  a 45-minute lag fitted on ten fourteen-day overlaps at 0.04 degrees C reproducing the carton's set exactly, while 30
  and 60 minute duration filters (17 and 6) and a 45-minute moving average (20) fell elsewhere and a 90-minute moving
  average missed by one refrigerator: the stage 2 world keeps the default's count plausible and every store clear of the
  line under the standing family.
- v8 stage 3, 2026-10-23: standard 7.1 first read "the records of each store's device of record are its vaccine
  temperature records", which a literal reader takes as the logger's readings being the vaccine's temperature (an
  official decoy for the default path); it became a records-custody clause.
- v8 stage 3, 2026-10-23: under the interval-mean reading of a record's vaccine temperature five stores' whole hours
  moved by one while the call held; 7.3 now files the counting (a record counts its ten minutes by the vaccine's
  temperature at its time stamp), WHAT and not HOW (SF17).
- v8 stage 3, 2026-10-23: return credits from both manufacturers put the cracker's balance below zero at eleven
  stores, a loud failure that points at the double count; only Halvorsen's standard-dose products are returnable, the
  leftovers leaner and the unrecorded losses scaled to each store's volume (cracker 15 doses or more, A6).
- v8 stage 3, 2026-10-23: maintenance-only invoices at one price per unit type tied ten stores' service figures (a
  constant response would have kept them); per-model prices and add-on parts at some visits, every store's figure now
  distinct (B5). With the tax switch as ask B's only silent device a reader who found it kept 23 to 30 of 30; the
  pre-move two-store maintenance routes on one invoice were added, so the tax switch alone keeps 10.
- v8 stage 3, 2026-10-23: the first names sat on real organisations, products or places in or near the field (H21):
  Coldline (a refrigeration manufacturer), Polarwatch (an ocean-data programme), Vaxtor, Homeline, Arctis, Glacier
  Medical, and the acquired chains Rookwood Drug and Saltash Apothecary; renamed Tellvane, Brumal, Stellane, Keswell,
  Brannon, Pendry Medical, Vollmer Drug and Lindqvist Apothecary before any reader saw the pack.
- Architecture 8, 2026-10-23: spent at stage 4. Two instruments recording one unit side by side are compared by a
  strong reader on reflex: the pilot stores' logger and in-carton series parted at every restock and defrost swing, so
  reader B fitted a first-order lag on the overlap with no sentence asking for it. Every ask device had one natural
  check that exposed it (per-item balances, cost per unit, a list price met exactly, one invoice on two sites).
  Next architecture: a decisive step whose evidence no single side-by-side comparison shows, and ask devices that no
  per-item reconciliation or unit-price check reveals.
