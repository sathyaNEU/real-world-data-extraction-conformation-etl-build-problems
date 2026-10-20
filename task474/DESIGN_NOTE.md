# task474 design note: Ridgeline Power Cooperative's 2027 SCR upgrade designations (architecture 3)

Architecture 3, drawn 2026-10-20 after architecture 2 (monitor gaps filled by hours since start) was spent at stage 4.
The world, the decision and the program rules carry over; the decisive step is new and the architecture 2 fill is
now the default path.

## Draw

- **Pairing.** Client domain physical-environmental-sciences, task type emissions inventory (hourly continuous
  emissions monitoring conformed into a seasonal unit inventory), objective Data Extraction & Conformation (ETL): the
  DAHS export, the monitor maintenance tickets (local time), the generating unit register, the gas invoices and the
  outage event report are conformed into one unit-season inventory that the program's rate rule runs on.
- **Decision.** How many, and which, of the nine combined-cycle units the 2027 SCR Upgrade Program designates: a unit
  whose 2026 ozone-season NOx per gross MWh is 0.170 or more. Retrospective by necessity: the program's rule reads the
  closed 2026 season, and the call funds the 2027 capital budget.
- **The quantity.** Each unit's NOx emitted over its season operating hours, divided by its gross MWh. The NOx in the
  hours the analyzers were out is unobserved and estimated; that estimate is the field's work.
- **Pitfall, data-native.** Two plants' instrument air headers tripped through the summer; instrument air feeds both
  the analyzers' dilution probes and the SCR's air-operated ammonia flow valves, so in those gap hours the unit ran
  uncontrolled at about twenty times its controlled NOx per MMBtu, and the first measured hour after each trip, before
  the ammonia vaporizer is back to temperature, shows that level.
- **Default path's answer.** Fill every gap from the unit's own measured hours in the same start state and load (the
  architecture 2 golden, the field's standard handling): AF-2, CB-1, DF-1, DF-3, SR-1 (five).
- **Golden.** Fill the instrument-air gaps at the unit's NOx per MMBtu in the first measured hour after its air losses,
  times each hour's heat input, and every other gap as the default path does: AF-1, AF-2, CB-1, CB-2, DF-1, DF-3, SR-1
  (seven).
- **Shape.** 07, a grid: nine units by three figures (designated, fuel cost, forced outage hours) in the workbook,
  plus the count, the designated set and the memo's chart with its named parts.
- **Deliverables.** cc_unit_nox_inventory_2026.xlsx and scr_upgrade_designations_2027.pdf (a bar chart of every unit's
  rate against the target).
- **Guard.** WARN (driver 0.28 against this slot's architecture 2; differentiation lines for task193 and task254);
  personas Tamara Gill and Martin Estrada from guard.py names.

## Default path

1. Read the rules: every combined-cycle unit in the register; its 2026 ozone-season NOx rate is the NOx it emitted
   while operating from 1 May to 30 September 2026 over its gross generation in the same hours; designate at 0.170
   lb per MWh or more.
2. Take the combined-cycle units' operating hours in the season from the DAHS export; some hours carry no NOx value
   (status OOC, MAINT, CALFAIL, COMM), and the outages fall more often in the first hours after a start.
3. Fill each blank hour from the unit's own measured hours in the same operating state: hours 1 to 3 after a start
   from the measured hours at the same position, later hours from the unit's NOx-on-load fit (the field's standard
   handling, the architecture 2 golden); sum, divide by generation, compare.

Ends on: AF-2, CB-1, DF-1, DF-3 and SR-1 designated

Golden: AF-1, AF-2, CB-1, CB-2, DF-1, DF-3 and SR-1 designated

## Stump sentence

The default path fills every hour without a NOx measurement from the unit's own measured hours in the same start
state and load and designates AF-2, CB-1, DF-1, DF-3 and SR-1, five units; the gaps that came with Cutler Bend's and
Ashfork's instrument air trips are hours in which the air-operated ammonia flow valves of the SCR had closed as well,
so the unit ran uncontrolled at about twenty times its controlled NOx per MMBtu, as the first measured hour after each
trip shows, and only filling those hours at that uncontrolled level designates the seven the program should fund.

## Three rules

Task type: Physical & Environmental Sciences, emissions-inventory, which the taxonomy tags for ETL: conforming the data acquisition system's hourly export, the monitor maintenance tickets in local time and the unit register into a unit-level ozone-season NOx inventory the program designates on.

Domain test: the quantity that decides the call is each combined-cycle unit's 2026 ozone-season NOx per gross MWh, worked as an emissions inventory works monitor data gaps: each missing hour estimated at the emission control state the unit was in, here an instrument air loss that blinds the dilution probe and closes the SCR's air-operated ammonia valves together, so the hour is filled at the uncontrolled NOx per MMBtu measured on the analyzer's return times the hour's metered heat input.

Swap: "which of our nine hospitals' infection rates per patient-day exceed the target, filling the days a ward did not report" keeps the words but loses the step: nothing ties a ward's missing days to a lapse in its infection control, while here one compressed-air header feeds both the monitor and the control device, and the uncontrolled level on the monitor's return is what identifies the fill.

Layer 1: a whole-year export with every monitored unit (peakers and the coal unit outside the program); status codes on blank hours; the DAHS on standard time against the tickets and the event report in local time; tickets covering only some ordinary gaps and including checks while the unit was offline; start-up hours whose analyzers are out more often than the run's; invoices by delivery point, not unit, one month per point not yet approved; each the cooperative's or its supplier's own record, each asserted neutral on the call.

Layer 2: estimation_fit. The methodological choice is how an hour without a NOx measurement is filled: left out, scaled by the measured share, from the unit's NOx at the same load, from its measured hours in the same start state and load, from the average of the hours either side, or at the control state the unit was in while unmonitored.

Decisive step: recognising that the gaps a plant instrument air loss caused are hours without NOx control, because the same air works the SCR's ammonia flow valves, and filling them at the uncontrolled NOx per MMBtu the analyzer measured in its first hour back, times each hour's heat input, rather than from the controlled hours that every state, load or neighbouring-hour fill draws on.

Not semantics: every field, status code, clock and ticket read correctly still leaves the blanks to fill, and nothing in any file says what NOx the unit emitted in them; a reader who reads the instrument air tickets correctly and fills those hours from the unit's state and load files the wrong set.

Not rule application: rule 2.2 files the population (the operating hours), the outcome (the NOx the unit emitted), the window and the unit; no rule says how a missing hour is estimated or that an air loss disables the SCR, and executing every stated rule with the standard fill designates five units.

Analyst test: a strong analyst who reads every field and rule correctly and fills each blank hour from the unit's own measured hours in the same start state and load designates AF-2, CB-1, DF-1, DF-3 and SR-1 designated (the default path's Ends on); only filling the instrument-air gaps at the uncontrolled level designates AF-1, AF-2, CB-1, CB-2, DF-1, DF-3 and SR-1.

Estimand: rules 2.1 to 2.3 (scr_upgrade_program_rules_2027.pdf) file the population (the register's combined-cycle units and their operating hours in the DAHS record, start-up and shutdown included), the outcome (the NOx the unit emitted, in pounds), the window (1 May to 30 September 2026, standard time), the unit (pounds per gross MWh) and the comparison (0.170 or more).

No decoy: nothing is planted to be caught; every measured hour is the unit's true NOx, the gaps are the analyzers' ordinary outages and the plants' real air trips, the tickets describe each trip as a maintenance ticket would, and no memo, earlier list or reported figure ships.

No certified replay: no certified or published figure is reproduced to recover the method; the uncontrolled level is measured directly by each unit's own analyzer in its first hour back after each air loss.

Lesson: a monitor gap with a common cause that also disables the control device is an uncontrolled hour, and is estimated at the uncontrolled level the monitor itself shows on its return; filling it from the unit's controlled hours in the same operating state, the standard repair, carries controlled NOx into it. No build on file fills a monitor gap by the control state a shared utility failure put the unit in.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the measured hours only (AF-2, SR-1) | rule 2.2 "the NOx the unit emitted": fires | blank NOX_MASS_LB: fires | none | none | blanks dropped: fires | one sum: fires | readable |
| R1, the load fill (AF-2, CB-1, SR-1) | none | GLOAD_MW in every hour: fires | regression imputation on the always-recorded covariate: fires | none | none | a regression | readable |
| R2, the start-state fill, the default path (AF-2, CB-1, DF-1, DF-3, SR-1) | none | the run of OP_TIME: fires | the gap rate by hours since start: fires | none | none | a grouped mean | readable |
| R2b, the before-and-after average (AF-2, CB-1, DF-1, DF-3, SR-1) | none | none | the regulator's short-gap substitution for some pollutants: fires | none | none | an average | readable |
| G (decisive), the air-loss hours at the uncontrolled level (seven) | no clause names an air system, an SCR state or a fill | no column holds a control state | no reflex fill conditions on a utility outage | none | none | none | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the season's hours | standard-time dates 1 May to 30 September | local-time dates | same call (asserted) | rule 2.2 "kept in standard time" |
| SF2 | gross generation | GLOAD_MW times OP_TIME over operating hours | GLOAD_MW over operating rows | same call (asserted) | the export notes |
| SF3 | 0.170 or more | at or above, unrounded | above | same call (no family rate within 0.009, asserted) | rule 2.3 |
| SF4 | the NOx emitted | measured and estimated NOx in every operating hour | the measured hours only | not the rule's quantity: files AF-2, SR-1 | rule 2.2 "the NOx the unit emitted while operating" |
| SF5 | hours since start | counted along the whole year's record | counted from 1 May | same call (asserted) | the record |
| SF6 | the start hours filled by state | hours 1 to 3 | hours 1 to 4 | same call (asserted) | the data |
| SF7 | the uncontrolled level per run | the unit's mean over its runs | each run's own first hour back | same call (asserted) | the data |
| SF8 | units | the register's combined-cycle units | every monitored unit | not the program's population | rule 2.1 |
| SF9 | the comparison | unrounded rates | rounded | same call (asserted) | rule 2.3 |
| SF10 | the tickets' clock | local time moved to standard | read as standard | same call (asserted) | the tickets' column names |
| SF11 | whose uncontrolled level | the unit's own, the plant's where none | the plant's pooled for every unit | same call (asserted) | the data |
| SF12 | which gaps are air losses | blank hours inside an instrument air ticket | blank runs whose first hour back reads five times the unit's median or more | same call (the two coincide, asserted) | the data |

## Ladder

Built figures, read from the cut pack by `generator/checks.py` (lb of NOx per gross MWh, 2026 ozone season, against
0.170).

- **R0, the measured hours only (AF-2, SR-1).** Drops every blank: DF-1 at 0.095, SR-2 at 0.080. Dies to rule 2.2.
- **R1, the load fill (AF-2, CB-1, SR-1).** Fills each blank from the unit's NOx at that load: DF-1 0.150, DF-3 0.161.
  Dies to the record's start hours: the gaps fall more often there and measured hour-1 NOx runs several times the
  load fit.
- **R2, the start-state fill, the default path (AF-2, CB-1, DF-1, DF-3, SR-1).** CB-2 0.125, AF-1 0.124. Dies to the
  first measured hour after each instrument air ticket: about twenty times the unit's controlled NOx per MMBtu.
- **R2b, the before-and-after average (the same five).** CB-2 0.153, AF-1 0.149: half the hours either side is
  controlled.
- **G, the decisive move (AF-1 0.190, AF-2 0.251, CB-1 0.268, CB-2 0.187, DF-1 0.186, DF-3 0.189, SR-1 0.187).** The
  truth (every hour known, generator only) designates the same seven, every rate within 0.010 of it.
- **Margins (cut pack):** every family member (unit mean or per-run level, hours 1 to 4, a regression with start
  dummies, the plant's pooled level) at least 0.009 from the target; every R1, R2 and R2b rate at least 0.0075 from it.
- **Position, separation and dominance:** a designation, not a ranking; R0 names two units, R1 three, R2 and R2b
  five, G seven; only the air-loss fill brings CB-2 and AF-1 over.
- **Worth:** the call and each unit's verdict; R2 keeps seven of nine verdicts and not the set, so the asks carry the
  pair (Ask sheet).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the register's nine combined-cycle units (rule 2.1) |
| 2 | Unit of account | the unit; lb of NOx per gross MWh |
| 3 | Attribution window | 1 May to 30 September 2026, standard time (SF1) |
| 4 | As-of dating | the DAHS export of 19 October 2026 |
| 5 | Version basis | the raw DAHS record, no substitute data (export notes) |
| 6 | Denominator | gross generation over the same operating hours (SF2) |
| 7 | Weighting | none: each unit's own hours |
| 8 | Window length | the season, 153 days |
| 9 | Boundary inclusivity | 0.170 or more (SF3) |
| 10 | Rounding path | rates unrounded (SF9); costs to the hundred dollars, hours whole |
| 11 | Tie-break | none: each unit against the target |
| 12 | Maturity and censoring | the season closed and exported |
| 13 | Order of operations | air-loss hours, the fills, the sum, the rate, the comparison |
| 14 | Row order | the export's order per unit; hours since start along it |
| 15 | Duplicate resolution | one row per unit and hour |
| 16 | Identity normalisation | unit IDs as the register gives them; the pre-2025 dispatch names not used by the call |
| 17 | Netting | none |
| 18 | Dimensional units | pounds, MW, MWh, MMBtu, dekatherms |
| 19 | Code and status semantics | blank values under every non-OK status; never the stump |
| 20 | Integerisation | none before the comparison |
| 21 | Clause scope | rules 2: the 2027 program |
| 22 | Forward window contents | the 2027 upgrades designated on the closed 2026 season (Draw) |

## Literal reader

Executed word for word, the rules fix the population (the register's combined-cycle units and their operating hours
in the DAHS record), the outcome (the NOx each emitted, start-up and shutdown hours included), the window, the unit and
the target. The record leaves some operating hours without a NOx value, so the filed outcome has to be estimated in
those hours. The candidates are leaving them out, a fill from the unit's NOx at the same load, a fill from its measured
hours in the same start state and load, the average of the hours either side, and a fill at the control state the
unit was in. The data separate them: every blank run inside an instrument air ticket that is measured on its return
reads at five or more times the unit's median NOx per MMBtu in its first hour back and no other blank run does, and
every estimator of the uncontrolled level (the unit's mean, each run's own, the plant's pooled) with any start-state
fill of the other gaps designates the same seven (checks.py). Every write-up step names the file and rule it executes.

## Oracles

None. No control, published figure or reconciliation ties only under the golden: the export carries no substitute
data and no reported total ships; the allowance holdings are by facility and tons held, not emitted.

## Ask sheet

- **Ask A, each unit's 2026 ozone-season fuel cost to the hundred dollars: 9 figures.** H18 home: rule 3.1, the
  capital budget weighs the upgrades against what each unit costs to run. Path: the DAHS heat input, the gas invoices,
  the supply agreement, the rules: four files, eight columns. Primary device (re-sited after rounds 1 and 2): D8, two
  clocks on one line, with every tie passing on the wrong one. The meter stations read midnight to midnight on
  standard time, so each line's quantity reconciles exactly to the plant's DAHS burn by calendar day, while the line's
  price is the price for the gas day the agreement defines (9:00 a.m. Central clock time): a reader who lets the
  quantity tie fix the day prices an hour by its calendar date and misses every unit. Secondary: strip billing (gas
  traded on a business day flows until the next business day's gas, and a weekend's or holiday's strip is one line
  dated on its last gas day), so a gas day with no line takes the point's next line; the previous line, an
  interpolation or leaving the day out each misses every unit. Hazards: invoices by facility (peakers share the
  meter), gas days with no burn.
- **Ask B, each unit's 2026 ozone-season equivalent forced outage rate, per cent to one decimal: 9 figures.** H18
  home: rule 3.2, IEEE Std 762's EFOR on local time, the register's nameplate as the capacity. Path: the event report,
  the DAHS operating time, the register, the rules: four files, eight columns. Primary device: D6 grain, an event's
  hours split across states. A forced derate found in a run often stays on the unit past the shutdown and into the
  reserve shutdown hours that follow, where IEEE 762 counts it in the denominator's reserve-shutdown derated hours
  and not in the numerator, and a derate's hours inside a full outage count in neither; the start and shutdown hours
  are part hours (OP_TIME below 1), so service hours are operating time, not operating rows. Counting rows, leaving
  out the reserve-shutdown term, or counting every derate hour at full each misses most units. Secondary: re-reports
  with a corrected start and end, a later report replacing an earlier one it overlaps. Hazards: the DAHS on standard
  time against the report's local time, events crossing the season's ends.
- **The construction layer:** each unit's verdict and the set.
- **Main population zero-counts (asserted):** the call reads no invoice, agreement or event row.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, fuel cost by unit | each operating hour priced at its gas day on Central clock time, a gas day without its own line at the point's previous line; every unit burns on strip days, so every unit's cost falls outside its bin | miss |
| B, outage rate by unit | IEEE 762's EFOR executed with service hours as the unit's operating rows; the part hours at every start and shutdown move every unit's rate outside its bin | miss |

- Mirror leakage: 0.0 per cent of ask weight (the asks read no rung's construction).
- Pair ceiling: 39.3 on the cut pack (weights 38 / 7 / 55; the cracker keeps the main block and instructions, 45.0,
  and none of the 18 ask figures; the mirror, R2, keeps 7 of 10 main figures, 33.6).
- Measured by: generator/ceiling.py

## Tried and rejected

- 2026-10-20, at the draw: the seed's own move (rebuild from towns rather than an area crosswalk): a careful analyst
  rebuilds from towns unprompted; kept as Layer 1.
- 2026-10-20, at the draw: re-basing the 2020 to 2021 estimates onto the population the 2020 census revised (the silent
  break behind the loud geography break): the population base is the series' version basis, an axis that must be
  filed, and filing it makes the step rule application while leaving it open forks the call against the published
  figures; dead by the WHAT screen.
- 2026-10-20, at the draw: the auxiliary for splitting the former counties (SNAP recipients over each region's take-up,
  measured where both are published): the same insight as task470 and task448 (the ratio the target actually scales
  with, measured where both are observed); a clone in the lane.
- 2026-10-20, at the draw: the five-year window centred on each year picked from a full run of overlapping releases: a
  lookup once the idea is there, and the one-window routes (2018-2022 or 2019-2023 for both years) sit within half a
  year of the golden, about $5,000 a region; replaced by two non-overlapping releases, where every route but the
  interpolation at the middle years misses by a year of drift or more.
- 2026-10-20, at the draw: a region formed by differencing overlapping published geographies (the pieces pinned by two
  partitions' margins): exact arithmetic with no field in it; the swap test reads it the same for sales territories.
- 2026-10-20, at stage 2: two non-overlapping five-year releases (2015-2019, 2020-2024) placed at their middle years
  and a year's town shares interpolated between them: its forcing evidence (the native years 2023 and 2024 on the line
  through the middle years) sat inside the regions' survey noise of 5 to 12 per cent, and the drift between the two
  releases' middle years, five years apart, was smaller than that noise; replaced by an annual indicator benchmarked to the one release.
- 2026-10-20, at stage 2: a growth component (each town's drift estimated from the two releases and carried by year):
  the difference of two town releases carries both sampling errors and swamped the drift; dropped.
- 2026-10-20, at stage 2: shipping the 2015-2019 release beside the 2020-2024 one under the benchmarked indicator: with
  two benchmarks a proportional Denton spreads the ratio across the years and moves amounts by up to $12,000 against
  the pro-rata golden, an open method; only the 2020-2024 release ships, where Denton and pro-rata coincide.
- 2026-10-20, at stage 2: SNAP benefits in dollars in the DSS file: a dollar indicator for a person count carries the
  emergency allotments of April 2020 to February 2023 and moves two amounts; the file ships recipients and households.
- 2026-10-20, at stage 2: the client address changes as their own file: a file named for address changes announces
  that the extract's town is not the town when served, and with it a reader keeps 14 of the 18 figures in asks A and B;
  the moves ship as address edits inside the grants data system's profile audit trail.
- 2026-10-20, at stage 3: the two relocations dated July 2023 to June 2024: the State Data Center's own planning region
  series then showed the drift outright (Greater Ormsby down 10.6 per cent from 2023 to 2024, Mill River Valley up
  8.1), so the record displayed the step; both relocations now run from April 2021 to February 2022, inside a former
  county each, where no published estimate shows them (the planning region estimates begin in 2023, and every region
  moves under 1.3 per cent from 2023 to 2024).
- 2026-10-20, at stage 4 (architecture 1 spent): two isolated scored readers. Reader 1 benchmarked each town's SNAP
  recipients to its own five-year survey count unprompted ("SNAP levels are not proportional to poverty across towns,
  but SNAP's year-to-year movement is usable") and landed all nine amounts (score_reader.py exit 1); reader 2 took SNAP
  shares (missed the call) but, like reader 1, rebuilt the town at service date from the audit trail, mapped Corbin's
  numbers and counted one energy payment per household, keeping 27 of 27 ask figures. Rule 2.2's "in that year" beside
  a single five-year release and a monthly town series displays the decisive step, and the ask devices are work orders
  a careful reader executes; the architecture is spent and the draw is re-rooted at stage 1.
- 2026-10-20, stage 4 judge on architecture 1: DETERMINISTIC, APPROVE, Gate H analytical; it named two pins worth
  carrying into the re-root (an effective date is the first day the new value applies; a household payment repeats on
  each member's row), and that the release-shares route is defensible enough that a miss there can read interpretive.
- 2026-10-20, re-root screen: keep the world and add a second correction to the benchmark (relocated households keep
  the origin city's SNAP take-up, so a constant town ratio misplaces the move): every route, the benchmark included,
  misses a split on the true poor by six or more amounts through the survey's sampling error, and a movers-aware
  estimator (backing the moves out of the conserved recipients) has no form the data close to one; dead as a decisive
  step.
- 2026-10-20, re-root screen: a second, independent correction from students (off-campus students counted poor by the
  survey and the estimates but absent from SNAP, away for remote teaching April 2020 to August 2021, timed by a
  university's residence counts): with campuses of 6,200 to 9,800 students in three towns of split counties, the
  SNAP-only benchmark still lands all nine amounts (largest gap $3,959), because the absence is two partial years of
  a five-year average and moves people only between pieces of one county; dead without implausible enrolments.
- 2026-10-20, re-root screens also run against the corpus: item-response test equating is spent in the lane
  (task450's anchor equating with a drift screen, task464's concordance, task123's and task249's drift screens), and
  census-register coverage carries nine cards and repeated screens (task123, task228, task243); neither is redrawn.

- Re-root screen, gas-network methane with undetected leaks scaled from quality-assurance re-surveys: dead on paper, the re-survey file displays its own miss rate so readers scale by it, it repeats task470's sensor-completion insight, and emissions-inventory is now held by task476 v2 inside the last-three window.
- Re-root screen, survey employment benchmarked to an annual census count with post-benchmark bias estimated from past benchmark revisions: dead on paper, the bias is displayed by the past revisions themselves and the bias forms (mean, recent, growth-scaled) fork the graded level with no design closing the family; task477 drawn first while task474 waits for a fresh world.
- Architecture 1 (the planning-region poverty split, each town's SNAP recipients benchmarked to its five-year survey
  level) as a whole: spent at stage 4 on 2026-10-20 (reader 1 landed the call, reader 2 kept every ask); re-rooted to
  architecture 2 in a fresh world after six screens on the old one died.
- Asks of the first cut (fuel priced on the gas day across the clock change; outages re-reported with a corrected end
  only; generation and operating hours graded): stage 4 readers 1 and 2 both missed the call (two and four units) and
  both kept all nine fuel costs, three forced-outage figures and every generation and hours figure; the judge read the
  re-report as a fork (union against the later report). Generation and hours left the deliverables, rule 3.2 files
  that the later report stands, re-reports correct the start as well, and one invoice month per delivery point is
  missing; a generation total that sat on a half MWh is gone with the two-decimal load.
- Architecture 2 (combined-cycle NOx with monitor gaps filled by hours since start): spent at stage 4 on 2026-10-20.
  The judge returned DETERMINISTIC and APPROVE and readers 1 and 2 missed the call (two and four units), but round-2
  reader 3 filled the start hours by position after a start unprompted, designated the golden seven and kept all 18
  ask figures (score_reader exit 1); the judge had already named the start-state fill the field's standard handling of
  missing monitor hours. A gap filled by the condition that causes it is a repair a careful analyst reaches; the next
  architecture needs a decisive step no standard repair performs.
- Architecture 3 screens at the draw (2026-10-20): hot-afternoon duct firing behind shelter-overheat outages (the heat
  input in every gap carries it, so a fill on load and heat input is a standard repair that lands it); start class
  (cold, warm, hot starts) behind longer start-up outages (hardens the spent start-state design and its thresholds are
  a knob); an analyzer over-range censoring (the tail above the span is unidentified without a second measurement).
  Kept: the shared instrument air outage, whose uncontrolled level shows only in the first hour back.
- Architecture 3, ask A first cut: the transporters' fuel retention as a fixed share (a straight-line fit of one
  point's price on another's rebuilds a missing month exactly, the agreement's formula pointing at it); the retention
  now resets monthly, so only a point on the same transporter rebuilds it. Ask B's first device, a month and day
  exchanged, found a qualifying outage on one unit only; replaced by an entry dated a day late.
- 2026-10-20, stage 4 round 1 on architecture 3: both readers missed the call (the start-state fill, five units:
  the architecture holds) but kept 17 of 18 ask figures each (score_reader exit 1 on the asks): the meters on one
  transporter differ by exactly the same amount every day, so the missing invoice month was rebuilt exactly, and the
  day-late outage entries started 24 hours from their true reports, inside the readers' 30-hour pairing window. Ask A
  re-sited to strip billing (weekend and holiday gas on one line dated on the strip's last gas day, no missing month);
  ask B to entries a month early. The round-1 briefs quoted the leak sweep's line carrying the committed call; later
  briefs paraphrase it.
- 2026-10-20, stage 4 round 2 on architecture 3: readers 3 and 4 missed the call again (five units; four of four
  readers now) and kept 18 of 18 ask figures each: the strip lines reconciled exactly on the gas day, and rule 3.2's
  definition of a later report (overlapping, or repeating type, cause, length and hours under other dates) was a
  procedure they executed. Both flagged the regular start-up shape, OP_TIME 1.00 in every operating hour and the
  repeated outage pairs as looking generated. The month-early entries and the definition are gone; ask B is now
  IEEE 762's EFOR; the meter quantities run midnight to midnight on standard time; start and shutdown hours are part
  hours; each unit has its own start shape and each start its own size. The round-2 re-judge returned DETERMINISTIC,
  FIX_NOW on wording (the write-up now states the air-loss fill by what the record shows, the fill of air-loss hours
  without a measured hour after them, and the strip rule with its quantity tie).
