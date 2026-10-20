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

## Tried and rejected` first. Architecture 2, a
re-root drawn 2026-10-20 after architecture 1 (the planning-region poverty split) was spent at stage 4; its identity
is in the card's lineage.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task474.json` (architecture v2), registered 2026-10-20 with --force over
  the slot's spent v1 card; the check showed WARNs only after the test.same_puzzle_older BLOCK against task243 and
  task450 v2 was answered with differentiation lines (and task476, task459 differentiated besides). Redrawn at the
  draw: the organisation family (cooperative_or_member_body is task250's; a generation and transmission cooperative
  files as utility_or_infrastructure), the strategy (population_selection is task471's), the decisive generator (G12
  is task250's, G10 task471's, G3 task477's; G4, attribution at the start transition). WARNs answered: ETL in 6 of 12
  (the lane); Gate G method_or_model_selection after task471 (the decisive step is which fill a missing monitor hour
  gets, among defensible estimators, forced by the monitored hours' own start-state profile); designation_set and
  "which" after task471 (the program funds every unit over its target); time_semantics' strategy risk (the analyst
  test runs on the clean truth with every field and rule read correctly and still files the wrong set).
- **Seed:** ET31's number, re-rooted; nothing of ET31's world is kept. The lane's objective stays.
- **Pairing:** Physical & Environmental Sciences / emissions-inventory / Data Extraction & Conformation (ETL). The
  cooperative conforms its continuous-emissions-monitor hourly records, the plants' control-system load logs and the
  monitor outage log into a unit-level ozone-season NOx inventory for its upgrade program.
- **Shape:** 07, a grid: each of the combined-cycle units' 2026 ozone-season NOx, MWh, NOx per MWh and verdict against
  the target, the designated units, the chart, the files.
- **Strategy:** time_semantics. A unit's analyzers drop out mostly in the first hours after a start (purge and
  calibration after a shutdown), the hours in which the selective catalytic reduction catalyst is still cold and NOx
  runs several times the steady rate at the same load; every start is in the load log, so each missing hour's start
  state is known and the fill conditions on it. Decisive generator G4 (attribution at the start transition), with G17.
- **Data-native sentence:** the analyzers' purge and calibration after a shutdown put most monitor gaps in the first
  hours after a start, and those are the hours a cold catalyst lets NOx run several times its steady rate, so the
  hours the record leaves blank are not like the hours it fills, while the load log records every start.
- **World:** United States, a fictional inland region (unnamed state). Ridgeline Power Cooperative, a generation and
  transmission cooperative, runs nine 1x1 combined-cycle units with SCR at four plants, three simple-cycle peakers
  and one coal unit. Its Clean Air Commitment holds each combined-cycle unit to 0.170 lb of NOx per gross MWh over
  the ozone season; the 2027 capital budget's SCR Upgrade Program funds every unit that did not meet it in 2026.
  Personas from `guard.py names --geo "United States" --seed 4742`: Tamara Gill (senior environmental compliance
  engineer), Kevin Cohen (manager, generation engineering).
- **Forcing fact:** the Board adopts the 2027 capital budget on 17 December 2026; the call faces forward (the 2027
  upgrades) on the closed 2026 ozone season the rules name.
- **Forum and forcing event:** board_of_directors (the cooperative's Board), budget_or_appropriation (the 2027 capital
  budget). Organisation family utility_or_infrastructure.

## Default path

1. Read the rules: every combined-cycle unit in the register; its 2026 ozone-season NOx rate is the NOx it emitted
   while operating from 1 May to 30 September 2026 over its gross generation in the same hours; designate at 0.170
   lb per MWh or more.
2. Take the combined-cycle units' operating hours in the season from the DAHS export; some hours carry no NOx value
   (status OOC, MAINT, CALFAIL, COMM).
3. Fill each blank hour from the unit's own NOx-on-load fit over its measured hours (the careful repair; dropping
   the blanks or scaling by the measured share is the cruder one), sum, divide by generation, compare.

Ends on: AF-2, CB-1 and SR-1 designated

Golden: AF-1, AF-2, CB-1, DF-1, DF-3, SR-1 and SR-2 designated

## Stump sentence

The default path fills each hour without a NOx measurement from the unit's NOx at the same load and designates AF-2,
CB-1 and SR-1 designated, three units; the analyzers were out mostly in the first hours after a start, when the cold
catalyst lets NOx run several times its steady level at the same load, so the fill puts steady-state NOx into
start-up hours and understates the units that cycle hardest, and only a fill by the hours since the unit's start
designates the seven the program should fund.

## Three rules

Task type: Physical & Environmental Sciences, emissions-inventory, which the taxonomy tags for ETL: conforming the data acquisition system's hourly export, the unit register and the monitors' gaps into a unit-level ozone-season NOx inventory the program designates on.

Domain test: the quantity that decides the call is each combined-cycle unit's 2026 ozone-season NOx per gross MWh, worked as an emissions inventory works monitor data gaps: each missing hour estimated from the unit's own measured hours in the same operating condition, here the hours since start that decide whether the SCR catalyst is hot.

Swap: "which of our nine hospitals' infection rates per patient-day exceed the target, filling the days a ward did not report" keeps the words but loses the step: nothing about a hospital's missing days is tied to a cold catalyst, and the SCR's temperature window, the analyzers' purge and calibration after a shutdown and the start sequence in the load log are what make the gaps fall in the high-emission hours and what identify the fill.

Layer 1: a whole-year export with every monitored unit (peakers and the coal unit outside the program); status codes on blank hours; the DAHS on standard time against the event report and maintenance tickets in local time; tickets that cover only some gaps and include checks while the unit was offline; units renamed in the 2025 dispatch system; invoices by facility, not unit; each the cooperative's or its supplier's own record, each asserted neutral on the call.

Layer 2: estimation_fit. The methodological choice is how an hour without a NOx measurement is filled: left out, scaled by the measured share, filled from the unit's NOx at the same load, or filled from the unit's measured hours at the same number of hours after its start.

Decisive step: filling each unmeasured hour from the same unit's measured hours at the same number of hours since its start, found from the load record's run of operating hours, rather than from a fit on load that the steady hours dominate.

Not semantics: every field, status code, clock and unit read correctly still leaves the blanks to fill, and no field says which fill; the load fill is the careful analyst's repair and files the wrong set.

Not rule application: rule 2.2 files the population (the operating hours), the outcome (the NOx the unit emitted), the window and the unit; no rule says how a missing hour is estimated, and executing every stated rule with the load fill designates three units.

Analyst test: a strong analyst who reads every field and rule correctly and fills each blank hour from the unit's NOx-on-load fit designates AF-2, CB-1 and SR-1 designated (the default path's Ends on); only the fill by hours since start designates AF-1, AF-2, CB-1, DF-1, DF-3, SR-1 and SR-2.

Estimand: rules 2.1 to 2.3 (scr_upgrade_program_rules_2027.pdf) file the population (the register's combined-cycle units and their operating hours in the DAHS record, start-up and shutdown included), the outcome (the NOx the unit emitted, in pounds), the window (1 May to 30 September 2026, standard time), the unit (pounds per gross MWh) and the comparison (0.170 or more).

No decoy: nothing is planted to be caught; every measured hour is the unit's true NOx, the gaps are the analyzers' ordinary outages, and no memo, earlier list or reported figure ships.

No certified replay: no certified or published figure is reproduced to recover the method; the start-hour levels are measured directly in each unit's own monitored start hours.

Lesson: when a record's gaps fall in a particular operating state, the missing values are estimated within that state, which the record's own operating log identifies; a fit on the variable the steady hours dominate carries the steady state into the gaps. No build on file fills monitor gaps by the state that causes them.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the measured hours only (AF-2, SR-1) | rule 2.2 "the NOx the unit emitted": fires | blank NOX_MASS_LB: fires | none | none | blanks dropped: fires | one sum: fires | readable |
| R1, scaled by the measured share of generation (AF-2, SR-1) | none | blanks: fires | ratio estimate: fires | none | none | one ratio: fires | readable |
| R2, the load fill, the default path (AF-2, CB-1, SR-1) | none | GLOAD_MW in every hour: fires | regression imputation on the always-recorded covariate: fires | none | none | a regression | readable |
| G (decisive), the fill by hours since start (AF-1, AF-2, CB-1, DF-1, DF-3, SR-1, SR-2) | no clause names a start, a catalyst or a fill | no column holds a start state: it is the run of OP_TIME above zero | no reflex fill conditions on the start | none | none | none | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the season's hours | standard-time dates 1 May to 30 September | local-time dates | same call (asserted) | rule 2.2 "kept in standard time" |
| SF2 | gross generation | GLOAD_MW over operating hours (OP_TIME 1.00) | GLOAD_MW times OP_TIME | same call (every operating hour 1.00, asserted) | the export notes |
| SF3 | 0.170 or more | at or above, unrounded | above | same call (no family rate within 0.009, asserted) | rule 2.3 |
| SF4 | the NOx emitted | measured and estimated NOx in every operating hour | the measured hours only | not the rule's quantity: files AF-2, SR-1 | rule 2.2 "the NOx the unit emitted while operating" |
| SF5 | hours since start | counted along the whole year's record | counted from 1 May | same call (asserted) | the record: a run continuing on 1 May started before it |
| SF6 | the start hours filled by state | hours 1 to 3 | hours 1 to 4 | same call (asserted) | the data |
| SF7 | whose start hours | each unit's own | the fleet's pooled | same call (asserted) | the data |
| SF8 | units | the register's combined-cycle units | every monitored unit | not the program's population | rule 2.1 |
| SF9 | the comparison | unrounded rates | rounded | same call (asserted) | rule 2.3 |

## Ladder

Built figures, read from the cut pack by `generator/checks.py` (lb of NOx per gross MWh, 2026 ozone season, against
0.170).

- **R0, the measured hours only (AF-2, SR-1).** Drops every blank: DF-1 at 0.095, SR-2 at 0.095. Dies to rule 2.2.
- **R1, scaled by the measured share (AF-2, SR-1).** Assumes the blank hours emit at the measured average: CB-1 at
  0.126. Dies to the record: the blanks fall at starts.
- **R2, the load fill, the default path (AF-2, CB-1, SR-1).** Fills each blank from the unit's NOx at that load: AF-1
  0.162, DF-1 0.150, DF-3 0.161, SR-2 0.152. Dies to the record's start hours: measured hour-1 NOx runs several times
  the load fit's value at the same load.
- **G, the decisive move (AF-1 0.188, AF-2 0.228, CB-1 0.262, DF-1 0.186, DF-3 0.189, SR-1 0.187, SR-2 0.186).** Each
  blank start hour from the unit's measured hours at the same hour after a start; the truth (every hour known,
  generator only) designates the same seven.
- **Margins (cut pack):** every family member (per-hour means, start-hour rate times load, hours 1 to 4, a regression
  with start dummies) at least 0.009 from the target; every load-fill rate at least 0.0075 from it.
- **Position, separation and dominance:** a designation, not a ranking; R0 and R1 name two units, R2 three, G seven;
  only the start-state fill brings AF-1, DF-1, DF-3 and SR-2 over together.
- **Worth:** the call and each unit's verdict; R2 keeps five of nine verdicts and none of the set, so the asks carry
  the pair (Ask sheet).

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
| 10 | Rounding path | rates unrounded (SF9); MWh, hours and costs whole |
| 11 | Tie-break | none: each unit against the target |
| 12 | Maturity and censoring | the season closed and exported |
| 13 | Order of operations | hours since start, the fill, the sum, the rate, the comparison |
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
those hours. The candidates are leaving them out, scaling by the measured share, a fill from the unit's NOx at the same
load and a fill from the unit's measured hours in the same start state. The data separate them: each unit's measured
hours one to three after a start sit several times above the load fit at the same load, and the blank hours fall
mostly there; every start-state estimator (per-hour means, a start-hour rate times load, hours 1 to 4, a regression
with start dummies, start counted along the year or from 1 May) designates the same seven (checks.py). Every write-up
step names the file and rule it executes.

## Oracles

None. No control, published figure or reconciliation ties only under the golden: the export carries no substitute
data and no reported total ships; the allowance holdings are by facility and tons held, not emitted.

## Ask sheet

- **Ask A, each unit's 2026 ozone-season fuel cost: 9 figures.** H18 home: rule 3.1, the capital budget weighs the
  upgrades against what each unit costs to run. Path: the DAHS heat input, the gas invoices, the supply agreement, the
  rules: four files, eight columns. Primary device (re-sited after stage 4 readers 1 and 2, who executed the gas day
  and the daylight hour and kept all nine): D4, absence repaired through another file's structure. One month of
  invoices is missing at each delivery point (not yet approved when the file was pulled), and the agreement prices
  every point at a common Daily Index plus its own adder, so a missing day's price is another point's price that day
  plus the constant difference between the two points; carrying the last invoiced price forward, averaging, or
  dropping the hours each misses every unit. Hazards: the gas day on Central clock time against the DAHS's standard
  time, invoices by facility (peakers share the meter), gas days with no burn.
- **Ask B, each unit's 2026 ozone-season forced outage hours: 9 figures.** H18 home: rule 3.2 (a later report of the
  same outage stands). Path: the event report, the rules: two files, six columns. Primary device (re-sited after
  readers 1 and 2, who kept the later of each same-start pair and took three units): D1, a resubmission that opens no
  second case. A corrected outage was reported again under a new event number with a corrected start and end, so no
  key or start time pairs it with the original; only the overlap of two full outages on one unit, which one outage
  cannot make, finds the pair. Hazards: derate events (D1, D2) overlapping outages legitimately, events crossing the
  season's ends.
- **The construction layer:** each unit's verdict and the set.
- **Main population zero-counts (asserted):** the call reads no invoice, agreement or event row.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, fuel cost by unit | each operating hour priced at its gas day on Central clock time, the missing invoice month carried from the last invoiced price; every unit burns in a missing month, so every unit's cost falls outside its bin | miss |
| B, forced outage hours by unit | U1 to U3 event hours in the season per unit, a later report kept where two share a unit and start; the corrected re-reports start at another hour, so both count and every unit's hours fall outside its bin | miss |

- Mirror leakage: 0.0 per cent of ask weight (the asks read no rung's construction).
- Pair ceiling: 35.5 on the cut pack (weights 38 / 7 / 55; the cracker keeps the main block and instructions, 45.0,
  and none of the 18 ask figures; the mirror, R2, keeps 5 of 10 main figures, 26.0).
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

