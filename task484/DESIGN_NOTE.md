# task484 design note: Wrenford's road sections over three million vehicles in 2025 (architecture 4)

Architecture 4, drawn 2026-11-02 at the Batch 3 re-root. Architecture 3 (Halvard County's wood smoke zones,
physical-environmental-sciences) is closed with its world and kept below as `## Architecture 3 record`; the
append-only `## Tried and rejected` closes the note.

## Draw

- **Pairing.** `survey-research-official-statistics` / `seasonal-adjustment-official-time-series-production`
  (serves ETL), objective Data Extraction & Conformation (ETL). Shape 15, decision `conformed_dataset`: the
  conformed supply of every section counted in 2025 for the noise mapping round, with the sections over the line.
  The objective fixes the slot's lane; the domain moved because every other ETL client domain is held (task123
  general statistics, task485 healthcare claims, task475 education, task452 and the brief close physical sciences).
- **World.** Wrenford, a fictional unitary borough in the West Midlands. Its transport data and monitoring team
  (local government, a statistics function: it publishes the borough's traffic estimates) supplies the 2026 noise
  mapping round with the 2025 annual traffic of every section it counted in 2025; Environmental Protection fixes
  the mapping contractor's scope on the sections over three million vehicle passages. Personas from
  `guard.py names --geo England --locale en_GB --seed 484`: Irene Griffiths (head of transport data and
  monitoring), Melanie Watts (traffic data analyst), Beth King (Environmental Protection, contract manager); the
  draw's other names were already first names in older builds (people.first), Cheryl Dixon among them once
  task304's fresh card took the name.
- **The call.** How many, and which, of the 18 sections counted in 2025 carried more than three million vehicles
  (8,219 a day). Golden: nine. The call is forward facing in use (the contract scope for the 2026 round) and
  retrospective in quantity by the round's own definition (the round models the closed year 2025), the reason
  the window is closed.
- **Candidates written before choosing** (the dropped ones are in `## Tried and rejected`): (1) a short count
  taken to the year by the section's own partial record, chosen; (2) domestic gas meter reads re-timed to the
  month with heat pump installations from the certification register; (3) VAT turnover calendarised from three
  staggered quarterly panels; (4) long-term migration under the 12 of 16 months rule from border crossings;
  (5) small solar generation re-timed from feed-in meter reads by irradiance; (6) vehicle kilometres from
  odometer readings at inspections; (7) household waste tonnage per round from bin lifts and weighbridge tickets;
  (8) bus passenger kilometres by tap-on trip chaining; (9) the honey e-mark draw carried from the first screen.
- **Why (1).** The field's named method for the deciding quantity, the short-count expansion with same-day factors
  from the permanent counters by setting, sits at rung 0 and files a wrong set; the precondition it needs (the
  section shares its group's weekly and seasonal rhythm) is what this dataset violates at the six sections whose
  ends are a campus, a school, an industrial estate, a retail park, a leisure park and a hospital; and the
  violation is recoverable only through a record kept in another system for another reason.
- **The ETL pincer, named.** The forcing file (the UTC system's daily detector summaries) pins an overlap: the
  counted day, which the manual count and the section's approach detectors both recorded. Reading it correctly is
  not sufficient: the detectors see one lane of one direction, a different grain from the section's two-way flow,
  so no detector figure is the section's traffic; the section's year enters only as the ratio of the detectors'
  mean full day to their own 07:00 to 19:00 flow on the counted day, and the detectors are tied to the section
  only by junction and arm names that the two registers write differently.
- **Data-native sentence.** Signal-controlled minor sections in a town of retail parks, a campus and an
  industrial estate carry traffic whose week and year follow the shops, the terms and the shifts at their ends
  rather than the commuter roads the permanent counters sit on, and the town's signal detectors record that year
  on one approach lane of each such section.
- **Axes against the window** (last three at registration: task123, task301, task142): forum
  customer_or_counterparty, forcing event purchase_order_or_contract, org family local_government, role
  statistical_office_head, context artifact monitoring_export, calibration none, strategy grain_or_unit, decisive
  generator G2 (G14 and G13 behind it), shape 15. Registered WARN only (strategy risk, objective use); the
  registered card re-checked as the last act of the draw.
- **Strategy-risk WARN, answered.** grain_or_unit here is not a field read: no column states a detector's share of
  a section or a section's factor; the grain bridge (one lane of one direction to the section's two-way year) is
  an estimate through the overlap day, and the analyst test below files the wrong set with every field read.
- **Shape arithmetic.** 18 sections' 2025 traffic (18), each section's over-or-under mark (18), the count and the
  set (2), the chart's parts (bars, labels, the line at 3.0, the highlight, the title stating the finding: 5),
  three files (3), ask A's 11 counters and ask B's 8 approaches (19): 65 criteria.

## Survivor anatomy

- **Actor:** the counted section has rows (its 12-hour count by hour, direction and class) and the property that
  decides, its own week and year as the school, campus, shops, shifts or wards at its end set them, has no column:
  the count register holds road class and urban or rural only, and no file stores a section's factor.
- **Link:** the section's year sits on the UTC detectors of its own approach at the signalised junction at one
  end: the count register names the section by its road and its end roads in full, the UTC register names
  junctions with abbreviated street types and detectors by junction reference, channel and approach; no key or
  sentence ties a count point to a detector, and the detectors see one lane, so the link carries the year only as
  a ratio through the day both recorded.
- **Reflex:** the field's named method for the deciding quantity, the short-count expansion with same-day factors
  from the permanent counters of the section's setting, is rung 0 and files 8 sections over the line (College Road
  and Grange Road in, Brookfield Way, Hollins Lane and Infirmary Road out).
- **Back-test:** the textbook route validates: the council's expansion factor review reproduces every counter's own
  annual flow from its single weekdays with its group's same-day ratio, leave-one-out, largest error 7.0 per cent
  against a 10 per cent target.
- **Second use:** every file the decisive step reads has its own reason: the detector summaries and the UTC asset
  register carry ask B (the noise model's corrections at the two signals renewed in 2025), the counts and the count register
  carry the supply's own fields, and the counter export carries ask A and the sections with no detector.
- **Shock:** the six sections the step moves are ordinary: their counts (5,384 to 8,647 vehicles in 12 hours) sit
  inside the others' range on ordinary neutral weekdays, and sorted on count, length, class or the default figure
  the golden set is no interval (Hollins Lane at 5,384 and Brookfield Way at 6,722 are over while Grange Road at
  8,647 and College Road at 8,318 are under).
- **Pins:** the WHAT is filed in the council's own genres: the terms note (a count point stands for the whole
  section between its two junctions; annual traffic is every motor vehicle passing along it, both directions,
  on all the days of the year) and Environmental Protection's scope note (every section counted in 2025; more
  than three million vehicle passages). No filed sentence names an expansion, a counter group, a detector, a
  factor, a pattern or a window; deleting any of them leaves the call forced by the records.

## Default path

1. Read the terms note and the scope note: the population is every section with a 2025 manual count, annual
   traffic is all motor vehicles both directions on all days of 2025, the line is 3,000,000 vehicle passages.
2. Sum each section's 12-hour count in manual_counts_2025.csv (07:00 to 19:00, both directions, all motor vehicles).
3. Expand each count with the permanent counters of the section's setting (atc_daily_2025.csv, atc_sites_2025.csv):
   the group's annual mean daily flow over its 07:00 to 19:00 flow on the counted day (the textbook same-day
   factor; month-and-weekday factor tables and pooling every counter give the same figures).
4. Check the factors against expansion_factor_review_2025.xlsx: every counter inside the 10 per cent target.
5. Annual traffic is the daily flow times 365; mark the sections over 3.0 million.

Ends on: 8 sections over 3.0 million, Ashfield Road, College Road, Grange Road, Holloway Hill, Kingsway, Priory Road, Station Street and Wharf Street, with Grange Road at 3.3 and College Road at 3.1 over and Brookfield Way at 2.6, Hollins Lane at 2.0 and Infirmary Road at 2.6 under.

Golden: 9 sections over 3.0 million, Ashfield Road 3.8, Brookfield Way 3.4, Hollins Lane 3.2, Holloway Hill 3.4, Infirmary Road 3.2, Kingsway 4.3, Priory Road 3.4, Station Street 3.6 and Wharf Street 5.0, with Grange Road 2.7, College Road 2.5 and Castlegate Road 2.6 under.

## Stump sentence

A strong analyst expands each section's 12-hour count to the year with the permanent counters' same-day factors,
the textbook expansion the council's own review validates on every counter, and files 8 sections over three
million, College Road and Grange Road in and Brookfield Way, Hollins Lane and Infirmary Road out, because the
counters sit on commuter roads while those sections' weeks and years follow the campus, the school, the retail
park, the leisure park and the hospital at their ends; each section's own year is on the signal detectors of its
approach, which see one lane and so give that year only through the day the count and the detectors both recorded.

## Three rules

- **Task type:** survey-research-official-statistics, seasonal adjustment official time series production: short-period observations conformed into an official annual series with the weekly and seasonal factors of continuous records, which serves Data Extraction & Conformation.
- **Domain test:** the deciding quantity is each section's expansion factor, the ratio of its annual average daily flow to its counted 12-hour flow, which official traffic statistics estimate from continuous counts and apply to short counts; replacing it with a stated figure or a sort changes the call.
- **Swap:** put ward admissions for vehicles and the call loses its object: no short count is carried to a year by the factor of a recorder that sits on one lane of the same unit, and no threshold of vehicle passages decides a mapping scope.
- **Layer 1:** street types abbreviated in the UTC register and written in full in the count register; British National Grid against latitude and longitude; the detector export in two half-year parts with its header repeated; detector days with partial or no availability from loop faults; one counter's six January days lost to a modem failure; register points not counted in 2025; section ends written in either order; per-system date formats. Each is the producing system's own and none moves the call (checks L1a to L1j).
- **Layer 2:** field method: the expansion factor of a short count taken from the section's own continuous record through the day both observed, where the field's group factors assume a rhythm the section does not share.
- **Decisive step:** recognising that a counted section is recorded through the year by the signal detectors of its own approach, and taking the section's own year from them as their mean full day over their own 07:00 to 19:00 flow on the counted day, so that their level, one lane of one direction, cancels and only the section's week and year remain.
- **Not semantics:** every field, code, unit and definition read correctly (the counts, the counters, the settings, the terms note's annual traffic) still files the 8 sections: the error is the counters' rhythm standing in for the section's, and no field, code or unit states either.
- **Not rule application:** no filed sentence names a method, a record, a factor or a window, so executing the terms and scope notes leaves the expansion open; the enumerated family on Brookfield Way (counter forms, the detectors' raw mean, the nearest junction's whole flow, the detectors pooled as a counter group, the own approach with the counters' 24/12 ratio, the own-approach forms) spans 1.66 to 3.59 million, the standing family (the own-approach forms on the nine detector sections, the counter forms on the other nine) spans at most 0.06 million inside one 0.1 million bin on every section, and the ruling out is quiet: the terms note's section definition and the counted day's own detector reading.
- **Analyst test:** a strong analyst who cleans the data and reads every rule expands each count with the permanent counters' same-day factors by setting, checks them against the factor review (every counter inside 10 per cent) and files 8 sections over three million: College Road and Grange Road in, Brookfield Way, Hollins Lane and Infirmary Road out.
- **Estimand:** traffic_estimate_terms_2025.pdf files a section as the road between its two named junctions and its annual traffic as every motor vehicle passing along it, both directions together, on all the days of the calendar year; noise_mapping_2026_scope.pdf files the population (every section counted in 2025) and the line (more than three million vehicle passages).
- **No decoy:** nothing is planted: no memo, draft or figure argues the counters' answer, the one context artifact (the factor review) answers another question correctly for counters only and recomputes from the counter export at zero tolerance, and no file carries a section's annual figure.
- **No certified replay:** no published section figure, prior-year estimate or certified table ships, so the method is not recovered by reproducing figures; the factor review's numbers are about counters and agree with every route.
- **Lesson:** a short count's expansion factor belongs to the section, and a continuous record that sees only part of the section still carries the section's year through the day both observed; the corpus's traffic builds (task251's station errors, task307's re-routing) teach neither.

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | 7 dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 counters' same-day factors by setting | no | no | fires (the textbook) | no | no | no | no | readable |
| R1 counter forms: month-and-weekday tables, every counter pooled | no | no | fires | no | no | no | no | readable |
| R2 the approach detectors' mean day read as the section's flow | no | no | fires once the detectors are seen | no | no | fires | no | readable |
| R3 the nearest junction's whole detected flow as the section's record | no | coordinates | no | no | no | no | no | readable |
| R4 every detector pooled as one more counter group | no | no | fires | no | no | no | no | readable |
| R5 the own approach with the counters' 24/12 ratio | no | no | partly | no | no | no | no | readable |
| R6 (decisive) the section's own approach detectors through the counted day | no: the terms note's definitions are the field's standard ones and name no record | no: no key, junction names abbreviated | no: linking signal detectors to count points is not the textbook expansion | no: the review validates R0 | no | no: the ratio is over a record no key joins to the section | no: the detectors carry ask B and the signal renewal review | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "the road sections we counted in 2025" | sections with a 2025 manual count (18) | every point in the register (30) | other population | the scope note: every section the Council counted in 2025; others come from the national dataset |
| SF2 | vehicles | motor vehicles | pedal cycles included | same call | terms note section 3; asserted same call |
| SF3 | in the year | calendar 2025, 365 days | a financial year | other window | terms note section 4: the calendar year |
| SF4 | more than three million | strictly over 3,000,000 passages | at or over | same call | no licensed figure within 0.12 million of the line, asserted |
| SF5 | traffic of a section | both directions together | one direction | other call | terms note section 4: both directions together |
| SF6 | the counted 12 hours | sum over both directions, 07:00 to 19:00 | per direction | other call | terms note section 5; the count rows |
| SF7 | the detectors' counted-day reading | the counted day's own 07:00 to 19:00 flow | the month-and-weekday mean | same call, same figures | asserted (checks SF7) |
| SF8 | partial detector days | full days only | scaled up, or kept as recorded | same call, same figures | asserted (checks SF8) |
| SF9 | two-lane approaches | both lanes summed | one lane alone | same call, same figures | asserted (checks SF9) |
| SF10 | days a detector did not record | left out of the annual mean | filled with zero | other figures | the export leaves those days blank; zero is not a reading |
| SF11 | counter group off the detectors | the section's setting | every counter pooled | same call, same figures | asserted (checks SF11) |
| SF12 | counter factor form off the detectors | same-day ratio | month-and-weekday factors | same call, same figures | asserted (checks SF12) |
| SF13 | the section's own junction | the junction named by its road and one of its end roads | a junction on the same road elsewhere | other figures | terms note section 2: a count point stands for the road between its two junctions |
| SF14 | annual traffic | daily flow times 365 | times 366 | same call | 2025 has 365 days |
| SF15 | rounding path | one decimal on the annual figure | the daily flow to 10 first | same call, same figures | asserted (checks SF15) |
| SF16 | heavy goods vehicles (ask A) | goods vehicles over 3.5 t: legacy classes 5 to 7, TX-8 classes 6 to 8 | buses or light vans included | other figures | terms note section 3 and the class tables |
| SF17 | a counter's missing days (ask A) | the recorded days' mean | filled from its own weekdays | same figures | asserted (checks SF17) |
| SF18 | an approach (ask B) | road and heading, its lanes summed, abbreviations read as the road | lanes as approaches | other figures | the register's approach and heading columns |
| SF19 | vehicles recorded (ask B) | sum of the recorded daily flows | imputed dark days | other figures | the prompt asks what the detectors recorded |
| SF20 | the renewal day (ask B) | read from the dark days, matching the log | the register's commissioning date | same day | asserted (checks SF20) |

## Ladder

| Rung | Route | Sections over 3.0 million | What moves |
|---|---|---|---|
| R0 | counters' same-day factors by setting (the field's method) | 8 | College Road 3.1 and Grange Road 3.3 in; Brookfield Way 2.6, Hollins Lane 2.0, Infirmary Road 2.6 out |
| R1 | counter forms T2 to T5 (mean of ratios, month-and-weekday tables, every counter pooled) | 8, the same | every form inside 0.1 million of R0 |
| R2 | the approach detectors' mean day read as the section's flow | 4 | every detector section under (1.2 to 2.1 million: one lane of one direction) |
| R3 | the nearest junction's whole detected flow as the section's record | 9, another nine | Castlegate Road 3.1, College Road 3.3, Grange Road 3.1 in; Brookfield Way, Hollins Lane, Infirmary Road out |
| R4 | every detector pooled as one more counter group | 8 | as R0 |
| R5 | own approach with the counters' 24/12 ratio | 7 | Brookfield Way 3.6 in; Hollins Lane 2.6 and Infirmary Road 2.9 out (the leisure park's evenings and the hospital's shifts fall outside 07:00 to 19:00) |
| Golden | own approach detectors through the counted day | 9 | Brookfield Way 3.4, Hollins Lane 3.2, Infirmary Road 3.2 in; Grange Road 2.7, College Road 2.5, Castlegate Road 2.6 under |

Separation: every rung names a different set; the decisive sections move by 0.23 million or more between R0 and
the golden (BE5); on the three commuter sections with detectors (Station Street, Kingsway, Mill Lane) R0 and the
golden print the same figure (BE6), so the method moves only the sections whose rhythm differs.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | every section with a 2025 manual count | filed in the scope note; C1 (18 sections, one count each) |
| 2 | Unit of account | the section between its two named junctions | filed in the terms note section 2 |
| 3 | Attribution window | calendar 2025 | filed; the detectors and counters cover 2025 only |
| 4 | As-of dating | the exports pulled January 2026 | static: every 2025 day closed before the pull |
| 5 | Version basis | one export per system | C1: no re-issued figures |
| 6 | Denominator | days in 2025 (365) | filed: annual traffic over the days in the year |
| 7 | Weighting | the setting group's ratio of sums | C1: mean of ratios and pooled inside the bin (SF11, SF12) |
| 8 | Window length | the detectors' whole year | C1: full days, scaled or kept as recorded inside the bin (SF8) |
| 9 | Boundary inclusivity | strictly over three million | C1: nothing within 0.12 million of the line (SF4) |
| 10 | Rounding path | one decimal on the annual figure | asserted (SF15) |
| 11 | Tie-break | none needed | C1: no two sections share a figure at the line |
| 12 | Maturity and censoring | none: the year is closed | C1 |
| 13 | Order of operations | sum the count, then expand | C1: expansion is linear in the count |
| 14 | Row order | file order irrelevant | C1: sums and means only |
| 15 | Duplicate resolution | the repeated header line dropped | C1: no duplicated data rows (L1b) |
| 16 | Identity normalisation | street types read in full | C4: the abbreviated join finds nothing, the read-in-full join finds one junction per section (SF13, L1a) |
| 17 | Netting against gross | none | n/a, asserted no negative flows |
| 18 | Dimensional units | vehicles per day and per year | units in the column names and the terms note |
| 19 | Code and status semantics | detector availability per cent | the export's own column; SF8 shows it inert |
| 20 | Integerisation | none | the figures are rounded once at the end |
| 21 | Clause scope | the round's line applies per section | filed in the scope note |
| 22 | Forward window contents | none: the round maps 2025 | closed year, nothing projected |

## Literal reader

Executed word for word on paper and again on the cut pack: the scope note's population is the 18 sections with a
2025 count; the terms note's annual traffic is every motor vehicle passing along the section, both directions, on
all the days of 2025. For a section whose own approach detectors record every day of 2025, the default's figure
stands other roads' days in for 364 of the section's days that the section's own record holds, so it does not
execute "passing along it on all the days" on the evidence shipped; the golden takes those days from the section's
own record and only the detectors' level, which the counted day measures, from the count. For the nine sections
with no detector, nothing but the counted day records the section, and every licensed counter form prints the same
figure (SF11, SF12). Every term and convention has a row above, each closed by a sentence or shown inert, and no
reading of a sentence moves the set; the easy answer comes from an easier method on the same literal estimand.

## Oracles

- The expansion factor review: answers how well the counters' group ratios reproduce a counter's own year; it
  validates R0 on counters and says nothing of sections (the back-test, never a referee for the call).
- The operations log: dates the two junction renewals and the firmware push as facts (no mapping, no effect named),
  so each ask's device is confirmable by a grader from the data and the log together.
- Nothing arbitrates the main call: no published, prior-year or certified section figure ships.

## Ask sheet

**Ask A: each permanent counter's average daily heavy goods vehicles in 2025 (11 figures, nearest 10).** Use: the
noise model's heavy vehicle inputs are calibrated on the counters, part of the round's supply. H18: a component of the round's supply on rows
the call never reads (the class channels; the call reads the all-vehicle columns). Primary device (D2, a label
stored before a silent switch): every counter got a TX-200 outstation in March to June 2025 (the site list's
installed date and the log), but the outstations kept the legacy class output until the firmware push of
8 September, when channel 5 changed from two-axle rigid lorries to buses; the site list carries only the current
TX-8 table, so the install-date reading and the current-table reading both miss every counter by three bins or
more (BE7). The switch is in the data (channel 5 over channel 8 flips on that weekday at every counter) and the
push is in the log without its effect. Stops: current table all year 244 to 1,302; install-date switch 309 to
1,433; legacy table all year; golden 350 to 1,740.

**Ask B: the vehicles the detectors recorded in 2025 on each approach to the Western Avenue / Fenwick Road and Ring
Road / Tanyard Lane junctions (8 figures, thousands).** Use: the noise model's corrections at those two renewed
signals, part of the round's supply. H18: a component of the supply on detectors no counted section uses (S1). Primary device (D7, codes reissued): both controllers were replaced in 2025
and the detectors re-terminated, so before the renewal each channel number carried another lane; the register
holds the current assignment only. The repair groups the pre-renewal channels into approaches by their day-to-day
co-movement and matches each group to the current approach on level, weekend shares and 07:00 to 19:00 share
across the dark days. Hazard: the register's abbreviated approach names split an approach in two unless read in
full. Stops: register mapping all year; pre-renewal days dropped; golden.

| Ask | Figures | Cracker's handling | Cracker's result |
|---|---|---|---|
| A | 11 counters' heavy goods vehicles a day | each counter's table switched on its installed date (the site list and the log) | miss |
| B | 8 approaches' recorded vehicles | channels joined to the register's current approaches, pre-renewal days kept or dropped | miss |

Pair ceiling: 33.6 (cracker 45.0 with no ask figure kept; mirror 22.2, sharing 12 of the 18 section figures with the golden and no ask figure).

Mirror leakage: 0.0 per cent of the ask weight.

Measured by: generator/ceiling.py on the cut pack.

## Architecture 3 record

Architecture 3 as shipped on 2026-10-24 (zip 87a0101c91c1a4ef), kept as history; its headings are demoted so this note carries each required section once.

**task484 design note: Halvard County's 2025-26 wood smoke zone determinations after a propane price spike (architecture 3)**

Drawn 2026-10-24 on the author's standing rule (no retirement) after architecture 2 was spent at stage 4 on the
judge's SEND_BACK; a fresh world and mechanism. The candidates screened before it are in Tried and rejected.

**Architecture 3, Draw.**

- **Pairing:** Physical & Environmental Sciences / `emissions-inventory`, drawn for Data Extraction & Conformation
  (ETL). The task type builds an inventory from activity data and emission factors. ETL because the deliverable is
  the conformed 2025-26 inventory by burn zone and SCC, built from the device registry, the household survey's
  responses, three propane distributors' exports in three layouts (a ticket csv, a fixed-width billing export with
  account and transaction records, a workbook of monthly gallons by member account), the airport station's daily
  readings, the state tool's documentation, the state's fuel and factor tables and the Census files the tool reads,
  which disagree in layout, units and keys.
- **Objective check:** the call is a determination per burn zone read off the conformed inventory; nothing future
  is predicted (not Forecasting), and the work is the conformation and the season's activity estimate (not
  Descriptive or Causal: the comparison is a means of estimating one season's wood burned, not a policy effect).
- **Shape:** 07, a grid of cells: the five burn zones by PM2.5, determination and share of the fund, the PM2.5 from
  wood burned in place of propane beside them, and the asks' grids (each zone's commercial propane in gallons and
  tons of NOx; the county outside the maintenance area, appliances and PM2.5 by SCC). Criteria: the call 1, zone PM2.5
  5, determinations 5, shares 5, the propane component 5, ask A 10, ask B 12, the two files 2: 45.
- **Decision and window:** which of the maintenance area's five burn zones, if any, had 2025-26 PM2.5 from
  residential wood combustion above its allotment in Table 4-2 of the maintenance plan, and so shares the 2026-27
  changeout fund, which the county ordinance splits equally among the zones over their allotments. The quantity is
  retrospective with its reason: the ordinance reads the latest complete heating season (1 October 2025 to 30 April
  2026), and the decision it drives (the 2026-27 changeout season, opening 1 November) is forward.
- **World:** Halvard County Air Quality Program, a county program in Montana for the Halvard Valley PM2.5
  maintenance area: five burn zones (Valley Floor North and South on the gas utility; East Bench, West Bench and
  Upper Valley mostly on propane), a solid fuel device registry kept since 2008, a 2024-25 household heating survey
  (the program surveys every third winter), and three propane distributors' exports under a 2019 data sharing
  agreement. Winter 2025-26 had the degree days of 2024-25 to within 0.02 per cent (2023-24 ran 7 per cent colder);
  propane prices spiked from December to February, which no shipped file records. Personas from `guard.py names
  --geo us --seed 484`: Billy Davis, Kimberly Rogers, Martin Booth.
- **Pack (21 files):** the registry (csv), the burn zone parcel list (csv), the device code crosswalk (csv), the
  survey responses (csv) and methods note (pdf), Wapiti Propane's accounts and tickets (csv, 43,811 tickets),
  Coldwater Fuel & Propane's fixed-width export and its record layout (txt, 64,123 lines), the Halvard Valley Farmers
  Cooperative's monthly workbook (xlsx), the station's daily readings (csv), the fuel equivalents and the 2023 factor
  table (csv), the maintenance plan's Chapter 4 with the changeout fund ordinance (pdf), the state tool's
  documentation (pdf), two ACS block-group releases, the assessor's housing units on 2010 block groups and the
  Census relationship file (csv); distractors in metadata.json: the burn curtailment calls and the national forest's
  firewood permits.
- **Deliverables:** `rwc_inventory_2025_26.xlsx` (the inventory by zone and SCC, the propane comparison it rests on,
  the commercial propane category, the county outside the area) and `zone_determinations_2026_27.csv` (one row per
  zone in the program's determination layout).
- **Card:** `.claude/skills/fingerprint/cards/task484.json` (architecture v3, lineage v1 and v2 spent), checked
  before registration: WARN only. Differentiation lines are filed against task123 (the same decisive gap, G4 and
  decision type) and task152, task232 and task269 (the same decisive gap, G4 and Gate G).
- **WARN answers:** repeat.question_form (which): the decision is a designation set, so the question asks which
  zones, with "if any" so that none is a grammatical answer.
- **Data-native sentence:** the propane price spike moved part of the heat in propane homes with a heating
  appliance onto the appliance, which no meter records; it shows only in the propane exports, as deliveries falling
  26 to 32 per cent at the accounts whose parcel has a registered heating appliance while the zone's other propane
  accounts took what they took in 2024-25, where the two groups moved alike in proportion from 2023-24 to 2024-25.
- **Strategy label:** causal_design: the season's wood burned is recovered through a difference-in-differences on
  the displaced fuel, with the comparison group (propane homes without a heating appliance) and the pre-period
  check the design's organs. Gate G decomposition_attribution: the exports' change is split between what every
  propane home shared and the switch only the appliance owners could make.
- **Measured on the generator's world** (`generator/golden.py` on the cut pack): carrying the survey's 2024-25 wood
  per appliance into 2025-26 puts the zones at 57.5, 56.3, 77.9, 68.2 and 47.3 tons; adding the wood burned in place
  of propane puts them at 59.2, 59.0, 98.1, 83.0 and 54.2 (the world's truth 59.1, 58.7, 95.9, 77.9 and 50.4, the
  same set). Every member that reads the switch (the zone's comparison ratio, a pooled one, no comparison at all, the
  comparison in gallons, fireplaces out, fill years) lands within 0.21 tons of the golden and prints the same whole
  tons in every zone; the comparison in gallons fails the 2023-24 to 2024-25 check at z 4.3 to 14.8 where the ratio
  passes at |z| 1.3 or less.

**Architecture 3, Three rules.**

Task type: Physical & Environmental Sciences, emissions-inventory, which serves ETL in the taxonomy.
Domain test: the quantity that decides is each burn zone's 2025-26 PM2.5 from residential wood combustion, the wood its appliances burned that winter times the 2023 emission factors, estimated for a season the household survey did not cover; a winter's fuel switching is measured where the displaced fuel is metered, a difference-in-differences on propane deliveries between the homes with and without a registered heating appliance, checked on the earlier pair of winters, carried through the heat balance at the furnace's and each appliance's seasonal efficiency.
Swap: "which of our five burn zones were over their wood smoke allotment" with clinics for stoves and patient visits for cords has no fuel a household switches between, no heat balance and no propane home without an appliance to compare against, so it stops making sense.
Layer 1: three propane distributors export in three layouts (a ticket csv, a fixed-width billing export with account and transaction records and an implied decimal, a monthly workbook by fiscal year), each its own billing system; geocodes are written with separators by one, without by another and not at all by the cooperative, whose system spells street words out; the survey vendor's instrument takes cords, face cords, pickup loads, tons or 40-pound bags; the county registry keeps every device with its removal history and year-only install dates for devices older than the 2008 program; the station reports daily maxima and minima with summer gaps, not degree days; the distributors send their whole valley book, accounts outside the maintenance area included; nothing is placed to be caught.
Layer 2: estimand identification, a difference-in-differences with a pre-period check: a season's wood burned is not measured, the survey's rates describe the winter before, and a price shock on the competing fuel moved heat onto the appliances of the homes that heat with it; the choice that flips the call is reading that switch from the propane deliveries against the zone's homes without a heating appliance, in proportion, against carrying the survey's rates into the new winter.
Decisive step: estimating each zone's 2025-26 wood burned as the survey's wood per appliance plus the heat the propane homes with a registered heating appliance moved off propane, measured by how much further their deliveries fell than at the zone's propane homes without one (in proportion, as the two groups moved alike from 2023-24 to 2024-25) and carried into cords at the propane furnace's and each appliance's seasonal efficiency.
Not semantics: with every field read correctly (tickets in gallons, accounts joined to parcels, the fixed-width decimal placed, face cords and pickup loads converted, device codes mapped to SCCs, zones from the parcel list, degree days from the readings) the easy route still carries the survey's wood into 2025-26 and reads the propane exports only for the commercial category, and no field, code, unit or definition read differently moves it.
Not rule application: the plan's 4.3 files the estimand (the PM2.5 emitted from the wood burned that season by the appliances in use, at the 2023 factors, against Table 4-2) and says nothing on how the season's wood burned is estimated; on the cut pack the enumerated family (the survey carried as reported or at the degree days, plus the switch read by the zone's comparison ratio, by a pooled ratio, against no change at all, in gallons, or over fill years) spans 77.9 to 98.2 tons on the East Bench and files two different sets, the standing family (every member that reads the switch) spans 98.00 to 98.21 there and prints the same whole tons in every zone, and what rules out the survey carried alone is the exports' own 26 to 32 per cent shortfall at the homes with a heating appliance against 0.996 to 1.002 at the homes without one, which no filed clause states and no table displays; the cheapest licensed member (each home's 2024-25 gallons less its 2025-26 gallons, no comparison at all) files the golden set at 98.03 on the East Bench, so the step is the recognition, not a choice inside the family.
Analyst test: A strong analyst who reads every file correctly builds the 2025-26 inventory from the 2024-25 household survey's wood per appliance class, carried at the two winters' (equal) degree days, times the registry's appliances in use, uses the propane distributors' exports only for the commercial propane category, and names Valley Floor South alone as over its allotment, where the benches' propane homes with a heating appliance took 26 to 32 per cent less propane and both benches are over.
Estimand: each burn zone's PM2.5 from residential wood combustion in the 2025-26 heating season (1 October 2025 to 30 April 2026), the PM2.5 emitted from the wood burned that season by the appliances in use, at the 2023 emission factors, against the zone's allotment in Table 4-2; filed in the plan's 4.2 and 4.3 and the ordinance's 8.30.140 (pdf).
No decoy: nothing is planted; the registry, survey, exports, readings and conversion factors are the program's and its suppliers' own records as their systems produce them, no memo, draft, briefing or stakeholder figure carries a wrong answer, and no filed sentence prescribes carrying the survey into a later winter.
No certified replay: no certified or published figure is reproduced to recover the method; the construction follows from the estimand and from the data.
Lesson: an unmetered fuel's use in a season the survey missed can be read off the metered fuel the households left, but only against the households that could not switch and only in proportion, as the earlier winters show; no build on file teaches recovering one fuel's use from another fuel's deliveries by appliance ownership.

**Architecture 3, Default path.**

1. Conform the registry, the survey responses, the three distributors' exports, the station's readings and the state's
   tables: device codes to SCCs, survey units to cords and tons, accounts to parcels and burn zones.
2. Count each zone's appliances in use in 2025-26 by class from the registry (installed before 1 October 2025, not
   removed).
3. Take the 2024-25 survey's wood per appliance for each zone and class as its methods note estimates it, carried
   into 2025-26 as reported or at the two winters' degree days (equal to 0.02 per cent).
4. PM2.5 at the 2023 factors, each zone against Table 4-2; the propane exports read for the commercial and
   institutional category, the county outside the area on the state tool.

Ends on: Valley Floor South alone exceeds its allotment and takes the whole fund.

Golden: Valley Floor South, East Bench and West Bench exceed their allotments and share the fund at USD 155,000 each.

**Architecture 3, Stump sentence.**

The default path carries the 2024-25 survey's wood per appliance into 2025-26 (the two winters had the same degree days) and reads the propane exports only for the commercial category, so the benches' appliances burn at last winter's rate, their PM2.5 sits at 78 and 68 tons under allotments of 89.9 and 77.6, and Valley Floor South alone exceeds its allotment and takes the whole fund, where the benches' propane homes with a heating appliance took 26 to 32 per cent less propane in 2025-26 while their neighbours without one took the same, and the wood burned in its place puts both benches over.

**Architecture 3, Readability screen.**

Measured on the cut pack (`generator/golden.py`); zones Valley Floor North, Valley Floor South, East Bench, West
Bench and Upper Valley, allotments 63.9, 52.6, 89.9, 77.6 and 58.6 tons.

| Rung | What the response does | What in the pack points at it | Verdict |
|---|---|---|---|
| L0 the survey as reported | each zone's appliances in use at the survey's 2024-25 wood per appliance | the survey is the only file that states burning | readable |
| L1 the survey at the degree days (default) | the same, scaled by the two seasons' degree days from the station (1.0001) | the station's readings | readable |
| L2 a uniform uplift | every zone's burning raised by one share for a dearer or colder winter | nothing: no price or burning series ships | readable |
| L3 the commercial category | the exports summed by account class for their own category | the plan's 4.4, the prompt | readable |
| G golden (decisive) | the propane homes split by the registry's heating appliances, the 2025-26 shortfall against the zone's homes without one, carried into wood at the efficiencies | nothing labels a propane account by appliance or compares its seasons; the split runs account to parcel to registry, and the exports' only stated use is the propane categories | silent |

L2 never lands the golden set: Valley Floor North goes over at an 11.1 per cent uplift, before the West Bench
(13.8) and the East Bench (15.5), so any uniform uplift that puts a bench over puts Valley Floor North over first.

**Architecture 3, Semantic fork table.**

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | PM2.5 from residential wood combustion | the wood-burning appliances' PM2.5 at the 2023 factors by SCC | the zone's residential propane combustion added | same call (propane PM2.5 is under a ton a zone) | plan 4.4: those categories do not count against the allotments |
| SF2 | the 2025-26 heating season | 1 October 2025 to 30 April 2026, deliveries by delivery date | the July to June fill years for the comparison | same call and whole tons (asserted) | plan 4.2 names the season; the fill-year comparison converges |
| SF3 | appliances in use | registry devices installed before 1 October 2025 and not removed | every device Active at the 15 May 2026 extract | identical counts (asserted) | plan 4.3; nothing was installed or removed after 30 April |
| SF4 | exceeded its allotment | unrounded PM2.5 above the allotment | whole tons against the allotment | same call: every zone 4.45 tons or more from its allotment (asserted) | plan 4.2 and the ordinance's A |
| SF5 | a parcel's burn zone | the burn zone parcel list | the registry's burn_zone field | identical for every device (asserted) | plan 4.1 |
| SF6 | survey units | a face cord a third of a cord, a pickup load half, 40-pound bags | pickup loads at a third of a cord | same call (asserted) | the survey methods note |
| SF7 | the survey's grain | each zone's weighted class mean, classes under 10 respondents at the five-zone mean | classes pooled across zones | another set (Valley Floor North over, 64.6) | the survey methods note's estimator |
| SF8 | the survey's weights | each respondent's weight | unweighted means | same call and whole tons (asserted) | the survey methods note |
| SF9 | the weather between the winters | degree days from the station's daily maximum and minimum, base 65, ratio 1.0001 | no weather adjustment | same call and whole tons (asserted) | the readings make the readings converge |
| SF10 | a heating appliance home's expected 2025-26 gallons | its 2024-25 gallons at the ratio of the zone's propane homes without a heating appliance | a pooled ratio; no change; the change in gallons; fireplaces out of the comparison | same call and whole tons under every one (asserted) | the records converge; the gallon form fails the 2023-24 to 2024-25 check |
| SF11 | a heating appliance | a class the state tool gives a seasonal heating efficiency | fireplaces counted as appliances that took heat | not computable (no efficiency); fireplace homes in or out of the comparison, same whole tons (asserted) | the tool's Table 1 |
| SF12 | the propane furnace's efficiency | 85 per cent, the fuel sheet's existing furnace or boiler | any other value | not available | heating_fuel_equivalents.csv carries one propane row |
| SF13 | heat in a gallon of propane | 91,500 Btu | a lower heating value | not available | heating_fuel_equivalents.csv |
| SF14 | a cord's heat and weight | 18.5 million Btu and 1.163 tons; pellets 16.4 million Btu a ton | another wood | not available | the tool's section 2 |
| SF15 | the propane homes | the residential accounts on parcels in the zones | commercial accounts or accounts outside the area in the comparison | same call and whole tons (asserted) | the accounts' class and the parcel list |
| SF16 | the homes compared | accounts with deliveries in all three seasons | an unbalanced panel | identical (every residential account in the zones has all three; asserted) | the records converge |
| SF17 | a home whose 2025-26 gallons exceed its expectation | netted in its class's sum | floored at zero | same call and whole tons (asserted) | 14 of 3,813 homes; the records converge |
| SF18 | the fund's split | equally among the zones over their allotments | in proportion to the excess | USD 155,000 each | the ordinance's B |

**Architecture 3, Ladder.**

Measured in the generator (`golden.py` on the cut pack, `checks.py` on the world's clean truth; allotments 63.9,
52.6, 89.9, 77.6 and 58.6 tons for Valley Floor North, Valley Floor South, East Bench, West Bench and Upper Valley).

| Rung | Zones over their allotment | Flips from the golden | Call kept |
|---|---|---|---|
| L0 the survey as reported | Valley Floor South | 2 | no |
| L1 the survey at the degree days (default) | Valley Floor South (57.5, 56.3, 77.9, 68.2, 47.3 tons) | 2 | no |
| L2 a uniform uplift of any size | Valley Floor North joins before either bench | 1 or more | no |
| L3 the switch read in gallons (fails the 2023-24 to 2024-25 check) | Valley Floor South, East Bench, West Bench | none | yes |
| G golden | Valley Floor South, East Bench, West Bench (59.2, 59.0, 98.1, 83.0, 54.2 tons) | none | yes |
| T the world's true burning | Valley Floor South, East Bench, West Bench (59.1, 58.7, 95.9, 77.9, 50.4 tons) | none | yes |

The golden's margins are 4.70 tons under, 6.37 over, 8.19 over, 5.39 over and 4.45 under; the default's are 6.36
under, 3.72 over, 12.03 under, 9.38 under and 11.26 under. The correction tracks each zone's propane homes with a
heating appliance (184, 262, 1,586, 1,218 and 563 accounts), not its size.

**Architecture 3, Closure table.**

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | each zone's wood-burning appliances in use in the season | filed (plan 4.3); SF3, C1 on the extract date |
| 2 | Unit of account | a zone's tons of PM2.5 from residential wood combustion in the season | filed (plan 4.2 and 4.3) |
| 3 | Attribution window | the 2025-26 heating season, deliveries by delivery date | filed (plan 4.2); SF2, C1 (no device installed or removed inside a season, the cooperative's months whole) |
| 4 | As-of dating | the registry of 15 May 2026, nothing installed or removed after 30 April | C1, asserted |
| 5 | Version basis | the 2023 factor table, the tool's 2023 edition, the 2019-2023 ACS release the tool names | filed (plan 4.3, the tool) |
| 6 | Denominator | none: tons against tons | not applicable |
| 7 | Weighting | the survey's respondent weights; the comparison as a ratio of summed season gallons | filed (methods note); SF8, SF10 converge, asserted |
| 8 | Window length | one season for the inventory; the comparison on the two seasons either side of the price spike with the season before as its check | the design; SF2 converges, asserted |
| 9 | Boundary inclusivity | exceeded means above the allotment | filed (the ordinance's A); SF4, margins asserted |
| 10 | Rounding path | determinations on unrounded tons; whole tons in the file; the asks at the prompt's rounding from unrounded sums | the prompt's rounding sentence; bin distances asserted |
| 11 | Tie-break | none needed | asserted: no zone within 4.45 tons of its allotment |
| 12 | Maturity and censoring | none: the season closed on 30 April | not applicable |
| 13 | Order of operations | units converted, zone and class means, counts, the switch's wood added, factors | linear, the same in any order |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | one account per propane home; a removed device and its replacement are separate devices | C1 (no residential account repeats a parcel; asserted) |
| 16 | Identity normalisation | accounts to parcels by geocode with or without separators, the cooperative's by spelled-out address | Layer 1; every residential account in the zones matches exactly one parcel (asserted) |
| 17 | Netting against gross | a home whose 2025-26 gallons exceed its expectation nets within its class | SF17 converges, asserted |
| 18 | Dimensional units | gallons, Btu, cords, tons of wood, pounds per ton, short tons | filed (fuel sheet, tool, factor table); SF6, SF12 to SF14 |
| 19 | Code and status semantics | device codes to SCCs, registry status, account class | filed (the crosswalk, the exports' layouts); SF15 |
| 20 | Integerisation | none for the call; fund shares divide evenly | not applicable |
| 21 | Clause scope | plan 4.3 covers residential wood combustion; 4.4's other categories do not count | filed; SF1 |
| 22 | Forward window contents | the determination governs the 2026-27 changeout season; nothing forward is estimated | not applicable |

**Architecture 3, Literal reader.**

Executing the prompt and every filed sentence word for word: the plan's 4.3 measures each zone's PM2.5 as what the
appliances in use emitted from the wood they burned in the 2025-26 season at the 2023 factors, and the ordinance
compares it with Table 4-2. No file states what any appliance burned in 2025-26: the survey's methods note scopes its
estimates to the 2024-25 heating season, and the plan, the tool and the ordinance file no method for a season the
survey did not cover. A literal reader therefore has to estimate the 2025-26 burning from what the pack measures of
that season, and the only 2025-26 household heating record is the propane exports, which show the homes with a
registered heating appliance taking 26 to 32 per cent less propane while the zone's other propane homes took what
they took in 2024-25. Carrying the survey into 2025-26 unchanged assumes those homes heated the same way, which the
exports contradict; the golden is the burning those records imply.

**Architecture 3, Oracles.**

No file ties only under the golden or only on a wrong read. No shipped file states a zone's 2025-26 wood burned or
PM2.5, or ranks the zones; the survey states 2024-25 burning per device, the exports state deliveries per account,
the curtailment calls and the forest's permits carry no zone's burning, and the plan states allotments only. The
asks' referees: the Coldwater ticket reference carries each delivery's date (the device's evidence, never an answer),
and the Census relationship file carries the 2010 block groups to 2020.

**Architecture 3, Ask sheet.**

The call's declared population is each zone's appliances in use in 2025-26 (the registry's devices in the zones),
the survey's respondents and the residential propane accounts on parcels in the zones in all three seasons. No ask
computes over it.

| Ask | Quantity (unit, rounding in the prompt's closing sentence) | Population, outside the call's | Primary device (silent) | How it enters the call (H18) |
|---|---|---|---|---|
| A | each zone's commercial and institutional propane delivered in the 2025-26 season, gallons (nearest hundred) and tons of NOx (two decimals) | the distributors' commercial accounts, which the call never reads | D8 a settlement date for the event date: Coldwater's statement accounts post a month's deliveries on the first of the next month, so the export's TRANS-DT moves late-April deliveries out of the season and September top-offs into it; the delivery date sits only in the ticket reference, and residential accounts post on delivery | a measure every zone carries that the call does not turn on: the inventory's commercial and institutional heating category (plan 4.4) |
| B | Halvard County outside the maintenance area, 2025-26 appliances (whole) and tons of PM2.5 (one decimal) by SCC on the state tool | the county's households outside the area, from the Census and assessor files the call never reads | D7 codes valid in both vintages but drawn differently: the assessor's housing units sit on 2010 block groups whose codes match the ACS's 2020 block groups while the valley's edge was redrawn, so a code join reads the outer block group's rural units into a block group inside the area; the relationship file carries them across | the inventory's rows outside the maintenance area, which the program submits with the zones (plan 4.4) |

Shared hazards: survey units (the call path, neutral: pickup loads at a third of a cord keep the call); geocodes
with and without separators and the cooperative's spelled-out addresses (the call path and ask A); accounts
outside the maintenance area in every export (the call path and ask A); the ACS release the tool names against the
latest one in the pack (ask B). Fair handling, asserted: reading Coldwater's delivery date from the ticket reference
reproduces all 10 of ask A, and carrying the assessor's 2010 block groups to 2020 through the relationship file
reproduces all 12 of ask B. Separation, asserted by count: every Coldwater account whose transaction date differs
from its ticket reference is a commercial account, and no ask B file is read by the call.

Measured by: `generator/ceiling.py` on the cut pack (target.zip 87a0101c91c1a4ef).

| Ask | Graded figures | Cracker keeps | Mirror keeps | Naive handling keeps | Cracker |
|---|---|---|---|---|---|
| A commercial propane by zone, gallons and NOx | 10 | 0 | 0 | 0 | misses |
| B outside the maintenance area by SCC, appliances and PM2.5 | 12 | 0 | 0 | 0 | misses |

Over the 22 figures the cracker keeps 0.0 per cent of ask weight (scores 45.0 with the call), the mirror 0.0 per cent
(12.0), the naive handling 0.0 per cent.

Pair ceiling: 28.5.
Mirror leakage: 0.0 per cent of ask weight.
The cracker reads each export's own date field as the delivery date and joins the assessor's housing units to the
ACS on the block-group code, as the tool documentation's words invite; neither leaves a symptom in the hygiene
battery (no duplicate, no unmatched join, no fan-out). This is the paper measurement of the cracker the script
models; the stage 4 readers measure the real one.

## Tried and rejected

- 2026-10-20, at the draw: ET41's own world, broadband grant allocation from the FCC map: served, underserved,
  reliable technology, enforceable commitments and the location fabric are filed BEAD definitions and the base is a
  recorded count, so every lever was a filed definition, a fabric clean-up (Layer 1) or maturity of pending
  challenges; re-worlded.
- 2026-10-20, at stage 4 (architecture 1 spent): isolated reader 2 (sonnet, medium, fresh unzip) landed the call
  (Fairhaven and Linden) and all 24 ask figures. It read rule 2.2's "occupied housing units on 1 April 2026" as units
  occupied, not units existing, saw in the utility file that premises first billed after January 2021 start near
  empty while the older ones sit flat at 0.947, built the lease-up curve and applied it to every city; and it keyed
  the permits on city and parcel, which exposed every expired-and-reissued permit. Lessons: a fill record whose new
  premises begin at zero beside a flat stock is a ready-made curve one step from use, so it is the reflex, not a
  skipped step; the word "occupied" in the estimand points at it; a parcel key exposes re-issues to any hygiene
  pass. Reader 1 and the judge were stopped.
- 2026-10-24, architecture 2 draw: the payroll survey's birth-death model against the lagged QCEW census (reserved
  in task482's note). The months after the benchmark need a forecast of the net birth-death residual, and no filed
  criterion closes that carry-forward family; survey-research/etl is also under ban.pairing while task483 sits in
  the window. Not drawn.
- 2026-10-24, architecture 2 draw: a health plan's paid claims completed by received-date development after a
  processing speed-up. Spent in task451 (received-date development against the paid-date chain ladder).
- 2026-10-24, architecture 2 draw: a scanner-data price index's chain drift under sales, a multilateral index
  against linked Tornqvist. Spent in task463.
- 2026-10-24, architecture 2 draw: the variance of a year-on-year change over an overlapping member panel (a cost
  growth target read through a confidence interval). Spent in task195 (the paired difference), where a reader landed
  it.
- 2026-10-24, architecture 2 draw: rapid guessing read from response times. Spent in task479 (Gate G
  planted_defect_flip).
- 2026-10-24, architecture 2 draw: an aerial survey's intermittent plumes annualised as detections over overflights.
  That is task478 architectures 1 to 4's insight (detections over the coverage that could have seen them), and
  readers landed it there.
- 2026-10-24, architecture 2 draw: orphan wells' methane from a measurement campaign after worst-first plugging. The
  surviving wells' domain is one hygiene filter from the golden: a reader who counts unplugged wells drops the
  plugged ones from the sample too, so the reflex lands it.
- 2026-10-24, architecture 2 draw: an inventory base year recalculated after a method change, where the per-class
  recalculation (the reflex) is wrong because worst-first replacement left a cleaner surviving stock. Unspent at the
  slot screens, but its natural world is gas distribution mains, which is task476's (a niche repeat); a vehicle
  fleet's model-year rates tangle age with model year and reopen the family. Carried to the next draw as a lead, not
  drawn.
- 2026-10-24, architecture 2 ask draft (first cut pack 8b1df16c3144cafa): ask A on re-registrations linked by a
  predecessor id and ask B on a filed ACS vintage rule with labelled split block groups; ceiling.py measured the
  cracker and the mirror keeping 54 of 54 figures (pair ceiling 83.5), because every device was a field or a filed
  rule. Re-site both with silent devices (supplemental-stumping Part 3).
- 2026-10-24, ask A re-sited (second cut pack c7ccb8e1679941e1): the predecessor id removed and the split's old
  record closed as an ordinary closed record beside genuine same-day pairs; the cracker now keeps 3 of 36. Ask B unchanged.
- 2026-10-24, ask B re-sited (third cut pack 79bf825cac69ff18): the assessors' housing units keyed to 2010 block
  groups, the relationship file shipped, and every area-and-class cell given a genuine same-day pair; ceiling.py measures
  the cracker keeping 0 of 54 and a pair ceiling of 28.5.
- 2026-10-24, architecture 2 spent at stage 4 (zip 79bf825cac69ff18): both scored readers missed the call (each
  filed all six areas) and kept none of the 54 ask figures, but the judge returned NOT_DETERMINISTIC, SEND_BACK,
  competing_defensible_answer: the provision's 4.2 with the appendix's "by appliance class" executes literally as
  the survey's class mean times the plan's 2014 count, so the survivorship correction the golden makes is licensed
  by no shipped sentence, and filing that the base year means the stock that burned then, changed-out units
  included, would name the move. The judge also failed the golden's 2014 cells to one decimal (its fireplace rate
  0.372 against a class mean of 0.383, unexplained). Lesson: where the reflex is the literal execution of the filed
  estimand, the stump is a fork, not a step; the decisive population must follow from the WHAT as filed, with the
  easy route a different reading of the data rather than of the text.
- 2026-10-24, architecture 3 draw: road fuel sold at border stations to drivers from a neighbouring state (fuel
  tourism) read by a difference-in-differences around the neighbour's tax change. The swap test fails (cigarette
  sales read the same), and the territorial estimand's reading, not an analysis, decides. Not drawn.
- 2026-10-24, architecture 3 draw: a staggered rollout read with not-yet-treated comparisons against two-way fixed
  effects. Spent in task177's note.
- 2026-10-24, architecture 3 draw: a gas utility's unaccounted-for gas split into billing lag, the temperature
  under-registration of uncompensated residential meters and meter drift, leaving leaks as the residual. task476's
  gas distribution niche; the billing lag is task123's calendarization, and the temperature term executes Charles's
  law as a formula once seen. Not drawn.
- 2026-10-24, architecture 3 draw: landfill methane by first-order decay (task480's age-declining increments and
  four slot notes), capture-recapture across overlapping lists (task123, task180, task196, task253, task269,
  task448), gross flows corrected for reinterview misclassification (task244), equivalent soil mass for a soil
  carbon stock change (task279's conserved-component insight), glider kits' engine age (task474's ask device) and a
  replaceable component's own age (task132). Spent.
- 2026-10-24, architecture 3 draw: container ships' at-berth load by the reefers on board, calibrated on shore
  power meters. Rejected in task482's architecture 8 screens (a reader calibrating on the meters sees the per-call
  spread with reefers its first explanation).
- 2026-10-24, architecture 3 draw: hydropower turbine degassing of hypolimnetic methane. The pathway is either
  named by the filed estimand (then executed as a rule) or left to a reading of "reservoir emissions" (a fork, as
  architecture 2's judge ruled). Not drawn.
- 2026-10-24, architecture 3 draw: low-voltage anode effects emitting CF4 outside the potline's anode effect log.
  The cheapest licensed member is one regression with an intercept on the logged anode-effect minutes, task263's
  unmixing lesson. Not drawn.
- 2026-10-24, architecture 3 draw: flared gas booked as the balancing item of a production report and recovered
  by weighted least squares on the meters' stated uncertainties. Pro-rata and uncertainty-based allocation are both
  industry methods and the flare meter alone is a third defensible reading; filing one names the move. Not drawn.
- 2026-10-24, architecture 3 draw: N2O outside a growing-season chamber window (the spring thaw pulse) carried by
  fall-applied nitrogen. The gap is read off the estimand's dates (semantics), and the off-season transport forks
  between a ratio to the season and a ratio to fall nitrogen. Not drawn.
- 2026-10-24, architecture 3 draw: the leveraged trend of stop-loss excess claims (a reader with claimant-level
  claims trends each claimant by reflex), commercial cooking PM by device from health inspection equipment lists (a
  device-based inventory joins the season's device counts by reflex), bunching below a regulatory threshold (the
  counterfactual density's polynomial and window fork), and residential wood use moved by heat pumps or read from the
  assessor's heating type (architecture 2's heat-status variable, a composition one table hands over). Not drawn.
- 2026-10-24, architecture 3 draw: a Lunar New Year factory shutdown reaching a US port's container imports a
  Pacific crossing later, for its official seasonally adjusted series. The calendar regressor is a reflex in
  official statistics (task135, task467), and survey-research/etl sits under ban.pairing while task483 is in the
  window. Kept as a lead for task482's next architecture once the pairing frees.
- 2026-10-24, stage 2: thrift at the propane homes without a heating appliance (their deliveries falling with the
  price) dropped. The appliances' own burning then forks between the degree days and the comparison's ratio (the
  propane thrift applied to the wood), about 2 tons on the East Bench at whole tons, and no file can tell the two
  apart; with no thrift the comparison holds flat (0.996 to 1.002) and every member lands the same whole tons.
- 2026-10-24, stage 2: a 2025-26 four per cent colder than 2024-25 dropped. Carrying the survey with or without the
  degree days moved every zone by 2 to 3 tons and the comparison in gallons sat 1 to 2 tons from the ratio; equal
  degree days close both (C1), and the 2023-24 to 2024-25 check (7 per cent colder) still refutes the gallon form.
- 2026-10-24, stage 2: fireplaces in the switch dropped. At a 10 per cent efficiency each gallon of delivery noise is
  0.05 tons of wood, so the fireplace class swung 0.2 to 0.5 tons a zone between members; the tool gives fireplaces
  no heating efficiency and their propane homes join the comparison (fireplaces out of it: the same whole tons).
- 2026-10-24, stage 2: a fill-year (July to June) comparison printed the East Bench at 97 and the Upper Valley at 53
  against 98 and 54 while each year's summer top-off was drawn afresh; each account's top-off and spring fill are now
  a habit (a fixed amount with 5 per cent variation), and the fill-year member lands the same whole tons.
- 2026-10-24, stage 2: zone figures at one decimal rejected: the standing family spans 0.21 tons on the East Bench,
  so the zones are graded in whole tons with every member mid-bin (the survey's draw searched over 300 seeds,
  clearance 0.28 or more).
- 2026-10-24, ask B first cut: the redrawn tracts' 2010 codes read as 2020 moved the county's outside households by
  0.2 per cent and kept four of the twelve figures. The redraw now moves the outer block group's rural units into the
  first as the valley's edge built out, so the code join undercounts them by 7.5 per cent and misses all twelve.
- 2026-10-24, names: the first distributor was Larkspur (task483's college) and the survey vendor Bitterbrush
  (task135's note); renamed Wapiti Propane and Arrowleaf Survey Research.
- 2026-10-24, stage 4 round 1 (zip d51a7c26815e683b): both scored readers missed the call (Valley Floor South alone,
  the survey carried into 2025-26 at the equal degree days; neither read the propane exports beyond the commercial
  accounts) and missed all 10 of ask A (each took Coldwater's TRANS-DT as the delivery date), but both kept all 12 of
  ask B: the assessor file's name said 2010 block groups, so both carried its units through the relationship file.
  Scored 17 of 37 (ask B's 12 and the five determination figures the default gets right). The assessor file renamed to
  its housing units by block group as the assessor issues it, and the two commercial accounts whose parcel draw landed
  on a home's geocode (reader A found one) given parcels of their own; no figure moved (zip 87a0101c91c1a4ef).
- 2026-11-02, Batch 3 re-root: architecture 3 (Halvard County's wood smoke zones, shipped 2026-10-24 with no portal
  result) re-rooted at the Batch 3 queue reset; its world is closed and its card entry moved to the lineage.
- 2026-11-02, first screen (before architecture 4's draw): casino, whisky, grape, lead service line, minimum night
  flow, rule-out diagnosis, item response, claims, rail season ticket, plausible value and censored demand ideas
  were screened against the ETL pincer and the window; each reduced to a filed rule, a field read, a reflex or a
  held pairing, and none reached a card.
- 2026-11-02, architecture 4 draw: a honey packer's e-mark batches, the packaging tare placed from depalletiser
  scans and goods-in jar weights. The best candidate of the first screen, but general statistics with ETL is held
  by task123's re-root and routing it through a house domain would game the ban. Not drawn.
- 2026-11-02, architecture 4 draw: domestic gas meter reads re-timed to calendar months with heat pump
  installations dated in the certification register. Residential heating sits next to architecture 3's closed
  world, and the per-meter base and heating slope is the field's own weather normalisation, a reflex at the top.
  Not drawn.
- 2026-11-02, architecture 4 draw: VAT turnover calendarised from three staggered quarterly panels. The staggered
  three-month sums leave a zero-sum period-three pattern unidentified, and that pattern is the within-quarter shape
  the calendarisation needs, so no data separate the candidates. Not drawn.
- 2026-11-02, architecture 4 draw: long-term migration under the 12 of 16 months rule from border crossings. The
  recent arrivals' undecided stays make it maturity censoring, banned in the window (task301), and linking each
  traveller's crossings is identity resolution. Not drawn.
- 2026-11-02, architecture 4 draw: small solar generation from feed-in meter reads re-timed by irradiance. Over a
  calendar year the two ends' re-timing errors cancel for steady installations, and pro-rata against a profile is
  an estimator fork the data barely separate. Not drawn.
- 2026-11-02, architecture 4 draw: vehicle kilometres from odometer readings at inspections. Interpolation errors
  cancel over a year, and a keeper change joins on the registration number (a key). Not drawn.
- 2026-11-02, architecture 4 draw: household waste tonnage per collection round from bin lifts against weighbridge
  tickets. The per-round density from paired tickets is task133's architecture. Not drawn.
- 2026-11-02, architecture 4 draw: bus passenger kilometres from tap-on records by trip chaining. Trip chaining is
  the transit field's named method, so the golden would be the reflex; transfers need identity across two ticket
  systems. Not drawn.
- 2026-11-02, stage 3: Station Street and Kingsway first drawn with their far ends at the College Road and Grange
  Road junctions, both signalised, which gave each a second approach record generated apart from the section (a
  fork between two own records); their far ends moved to priority junctions.
- 2026-11-02, stage 3: street names first drawn read as one real town's (its ring of radial roads); replaced with
  generic names.
- 2026-11-02, stage 3: the renewed junctions' channels first matched on level and weekend shares alone. Ring Road's
  two approaches carried near-equal flows and the match swapped their lanes; the approaches now differ in level as
  a gyratory's do, and the pre-renewal channels are first grouped by their day-to-day co-movement.
- 2026-11-02, stage 3: ask B first asked each approach's average daily flow. Dropping the pre-renewal days moved it
  under one bin, so that over-correction kept the ask; it now asks the vehicles recorded in 2025, which the drop
  misses by months and the register join misses by tens of thousands.
- 2026-11-02, stage 3: ask A's counters first carried bus shares near their two-axle rigid shares, so the current
  table landed one counter inside its bin; the two-axle share now runs at about half of heavy goods vehicles, as on
  urban roads, and each counter's share is tuned so its figure sits two vehicles inside its bin and the
  install-date reading three bins away.
