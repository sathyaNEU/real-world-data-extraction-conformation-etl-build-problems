# task474 design note: a port authority's 2027 air-corridor designations (architecture 5)

Architecture 5, drawn 2026-10-20 in a fresh world after architecture 4 (Medicaid exposure rebuilt from the
capitation remittance) was spent at stage 4. Earlier architectures' sections are retired; their lessons stand in
Tried and rejected.

## Draw

- **Pairing.** Client domain physical-environmental-sciences, task type emissions-inventory, objective Data
  Extraction & Conformation (ETL): three count programs' short-duration classification counts (the state DOT's, the
  county's and the port's consultant's, each in its own layout and class scheme), the state's continuous count
  stations (hourly volumes, a few classifying), the link register and an emission rate table are conformed into one
  link-level on-road NOx inventory for the program year.
- **Decision.** How many, and which, of the roadway links around the port's terminals the port authority designates
  for its 2027 air-corridor program (zero-emission truck charging, idle enforcement, roadside barriers): a link whose
  program-year (October 2025 to September 2026) on-road NOx per mile is at or above the program's line. Forward
  facing: the designations fund 2027 work from the year just closed.
- **The quantity.** Each link's program-year vehicle-miles by class (passenger vehicles, trucks) times the class's
  NOx emission rate, per mile of link.
- **Data-native sentence.** Each link is counted for 48 hours on weekdays at one time of year, and the year's miles
  come from expanding that count with calendar factors measured at the state's always-on stations; trucks fall away at
  weekends and barely move by season while cars do the opposite, so factors computed for all vehicles and applied to
  a weekday count overstate the year's trucks at every link, most where trucks are most of the traffic, and the
  stations that classify measure the trucks' own factors.
- **Default path.** The traffic monitoring guide's textbook expansion: the count times the stations' all-vehicle
  monthly and day-of-week factors, split by the counted truck share.
- **Golden.** Cars and trucks expanded separately, each with factors computed for that class at the classifying
  stations.
- **Shape.** 07, a grid: fourteen links' verdicts, three terminals by four quarters by two figures, plus the count,
  the set and the memo's chart.
- **Guard.** WARN (objective and Gate G overuse); nearest task452 v1 at 0.06; personas Paige Hodges and Martin
  Estrada from guard.py names; forum, forcing event and org family clear of the last three builds.

## Default path

1. Read the rules: every link in the register; a link's program-year NOx is the vehicle-miles each class traveled
   on it from 1 October 2025 to 30 September 2026 times the class's rate in the 2026 table, per mile; designate at
   5.00 tonnes per mile or more.
2. Conform the three count programmes' files to one table of each link's two count days by class, and the stations'
   hourly records to daily totals.
3. Expand each link's count to an annual average daily volume the way the traffic monitoring guide does it: the
   count times the stations' monthly and day-of-week factors for all vehicles; split it into classes by the counted
   class shares; multiply by 365 and the class rates.

Ends on: L01, L03, L04, L05, L06, L09, L10, L11, L13 and L14 designated

Golden: L01, L03, L05 and L14 designated

## Stump sentence

The default path expands each link's two-weekday count with the stations' all-vehicle monthly and day-of-week factors
and splits the year by the counted truck share, designating L01, L03, L04, L05, L06, L09, L10, L11, L13 and L14; the
classifying stations show trucks running about a quarter above their annual average on weekdays and falling away at
weekends while cars barely move, so one set of factors for all vehicles carries every weekday count's trucks into
the year at weekday strength, and only expanding each class with its own factors from the classifying stations
designates L01, L03, L05 and L14.

## Three rules

Task type: Physical & Environmental Sciences, emissions-inventory, which the taxonomy tags for ETL: conforming three count programmes' short-duration classification counts, the state's continuous count station records and the link register into a link-level on-road NOx inventory the program designates on.

Domain test: the quantity that decides the call is each link's program-year NOx per mile, worked as an on-road emissions inventory works vehicle-miles: each class's annual average daily traffic expanded from short counts by temporal factors from continuous count stations (the traffic monitoring guide's method) and multiplied by the class emission rate; the field's own step here is choosing factors by vehicle class.

Swap: "which of our clinics' annual patient-visits per room exceed the line, expanding a two-day sample with the network's weekly and seasonal factors" keeps the words and loses the step: nothing in a clinic splits its visits into classes with opposite weekly patterns and twenty-fold different weights, while here trucks carry almost all of the NOx and the classifying stations measure their own weekly pattern.

Layer 1: three count programmes' exports in different layouts (DOT hourly wide, county 15-minute sheets, consultant hourly by lane with UTC offsets); station records in local standard time beside counts in local time; detector outage days at the stations; volume-only stations beside classifying ones; link lengths that cancel in a per-mile figure; each the agency's own export, each asserted neutral on the call (checks.py R2).

Layer 2: estimation_fit. The methodological choice is which temporal factors expand a class's short count to the year: the all-vehicle factors of every station split by the counted shares, monthly factors only, or each class's own factors from the stations that classify.

Decisive step: expanding passenger vehicles and trucks separately, each with the monthly and day-of-week factors the classifying stations measure for that class, instead of applying all-vehicle factors to the whole count and splitting by the weekday truck share.

Not semantics: every field read correctly (class groups, hour ending, standard time, lanes, directions) still leaves the all-vehicle expansion on the wrong set; no field says the weekly pattern differs by class, the stations' own records show it.

Not rule application: rule 2.2 files the outcome (vehicle-miles by class times the class rates), the window, the classes and the unit; no rule or note says how a short count is expanded or which factors apply, and executing every stated rule with the textbook all-vehicle factors files L01, L03, L04, L05, L06, L09, L10, L11, L13 and L14.

Analyst test: a strong analyst who reads every field and rule correctly and expands each count with the stations' all-vehicle factors, splitting by the counted class shares, designates L01, L03, L04, L05, L06, L09, L10, L11, L13 and L14 designated (the default path's Ends on); only class-specific factors designate L01, L03, L05 and L14.

Estimand: rules 2.1 to 2.3 (air_corridor_program_rules_2027.pdf) file the population (every link in the register), the outcome (NOx from on-road vehicles, vehicle-miles by class times the 2026 table's class rate), the window (1 October 2025 to 30 September 2026), the unit (metric tonnes per mile of link) and the comparison (5.00 or more).

No decoy: nothing is planted to be caught; every count and station record is the traffic the generator drove, no factor table, AADT estimate, memo or earlier list ships, and no document mentions factors or truck patterns.

No certified replay: no certified or published figure is reproduced to recover the method; the class factors are computed from the classifying stations' own hourly records.

Lesson: an on-road inventory's short counts are expanded class by class, because the heaviest-emitting class has its own weekly and seasonal pattern; a weekday count expanded with all-vehicle factors overstates trucks, and with them NOx, most where trucks are most of the traffic. No build on file expands a sample by factors that differ by class of contributor.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the count times 365 (eleven links) | rule 2.2 "in those twelve months": fires | count dates: fires | none | none | none | one product | readable |
| R1, all-vehicle monthly factors only (ten links) | none | station dates: fires | seasonal expansion: fires | none | none | a ratio | readable |
| R2, the textbook all-vehicle month and weekday factors, the default path (ten links) | none | station hours: fires | the traffic monitoring guide's expansion: fires | none | none | a ratio | readable |
| R2b, class monthly factors with all-vehicle weekday factors (eleven links) | none | class groups: fires | none | none | none | a ratio | readable |
| G (decisive), each class with its own month and weekday factors (four links) | no clause names factors or classes' patterns | no column holds a factor | the textbook reflex applies one set | none | none | none | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | program year | 1 October 2025 to 30 September 2026, 365 days | a calendar year | not the rule's window | rule 2.2 |
| SF2 | vehicle classes | FHWA 1-3, 4-7, 8-13 | two classes (cars, trucks) | same call: the rates table's three groups are the rules' three (asserted) | rule 2.2 |
| SF3 | the 2026 emission rate table | the one calendar year in the file | none | same call (asserted) | the table |
| SF4 | 5.00 tonnes or more | at or above, unrounded | rounded to the tenth | same call (nearest family value 0.29 t away, asserted) | rule 2.3 |
| SF5 | per mile | NOx over length, which reduces to daily volume times 365 times the rate | VMT summed then divided | same call (asserted) | rule 2.2 |
| SF6 | directions | both summed | one direction | not the link's traffic | the counts carry both |
| SF7 | factor groups | the stations as one urban group | groups by road type | same call (asserted) | the register's one factor group |
| SF8 | the files the call reads | counts, stations, register, rates | the NO2 monitors, the 311 complaints, the drayage registry | same call (asserted) | rule 2 |

## Ladder

Built figures, read from the cut pack by `generator/checks.py` (tonnes of on-road NOx per mile, program year, against
5.00).

- **R0, the count times 365 (eleven links).** No expansion; weekday counts stand for the year.
- **R1, all-vehicle monthly factors only (ten links).** The weekly pattern left in.
- **R2, the textbook, the default path (L01, L03, L04, L05, L06, L09, L10, L11, L13, L14).** L06 5.39, L10 5.39,
  L11 5.59, L04 5.37, L13 5.33, L09 5.32 over the line. Dies to the classifying stations: their trucks run at
  about 1.2 times their annual average on Tuesdays to Thursdays and at under half on Sundays, their cars near 1.
- **R2b, class monthly with all-vehicle weekday factors (eleven links).** The seasonal half alone.
- **G (L01 5.71, L03 6.18, L05 5.46, L14 5.48; L13 4.44, L09 4.56 the nearest below).** The true program-year NOx
  (every day known, generator only) designates the same four.
- **Margins:** every family member's every link at least 0.25 t from the line (cell or separate factors, plain or
  AASHTO station averages, car factors from the classifying stations or from all, groups by road type, class
  weekday factors with all-vehicle monthly ones); every link the textbook flips 0.30 t or more over it.
- **Worth:** R2 keeps eight of fourteen verdicts and not the set; the asks carry the pair (Ask sheet).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the register's fourteen links (rule 2.1) |
| 2 | Unit of account | the link; metric tonnes of NOx per mile |
| 3 | Attribution window | 1 October 2025 to 30 September 2026 (SF1) |
| 4 | As-of dating | the exports compiled by 26 October 2026 |
| 5 | Version basis | the station records as the DOT publishes them; one count per link |
| 6 | Denominator | link length, cancelling (SF5) |
| 7 | Weighting | none: each link's own count |
| 8 | Window length | 365 days |
| 9 | Boundary inclusivity | 5.00 or more (SF4) |
| 10 | Rounding path | rates unrounded; turn minutes to one decimal |
| 11 | Tie-break | none: each link against the line |
| 12 | Maturity and censoring | the year closed and published |
| 13 | Order of operations | conform, daily totals, factors, expansion, rates, comparison |
| 14 | Row order | none |
| 15 | Duplicate resolution | one count per link; gate transactions merged into stays |
| 16 | Identity normalisation | count site ids to links through the register |
| 17 | Netting | none |
| 18 | Dimensional units | vehicles per day, grams per mile, tonnes |
| 19 | Code and status semantics | FHWA class groups and direction codes; never the stump |
| 20 | Integerisation | none before the comparison |
| 21 | Clause scope | rule 2 the designation, rule 3 the terminal review |
| 22 | Forward window contents | the 2027 program funded on the closed program year (Draw) |

## Literal reader

Executed word for word, the rules fix the population (the register's links), the outcome (vehicle-miles by class
times the class rates), the window, the unit and the line. The links are counted on two days, so each class's
vehicle-miles over the year have to be estimated from the count. The candidates are the count times the year, the
all-vehicle monthly factors, the all-vehicle month and weekday factors split by the counted shares, and factors by
class from the classifying stations. The data separate them: the classifying stations' trucks run near 1.2 times
their annual average on midweek days and their cars near 1, so the all-vehicle route files ten links, while every
class-factor variant (cell or separate factors, plain or AASHTO averages, all or road-type groups) files the same
four (checks.py). Every write-up step names the file and rule it executes.

WHAT screen (stumping 1.2): population, rule 2.1; outcome, rule 2.2 (vehicle-miles by class times the class rates);
window, rule 2.2; unit, rule 2.2 (tonnes per mile); comparison, rule 2.3. The decisive step settles none of them: it
is how the filed vehicle-miles are estimated from a two-day count.

## Oracles

None. No control, published AADT or reconciliation ties only under the golden: the stations publish hourly volumes,
not AADTs or factors, and no link's annual volume ships.

## Ask sheet

- **Ask A, each terminal's truck visits in each quarter of the program year: 12 figures.** H18 home: rule 3.1, the
  Board's terminal operations review beside the designations. Path: the gate transactions and the rules. Devices:
  D6, dual transactions (two rows, seconds apart at the in-gate, for one stay) at every terminal; D8 at Berth 20,
  whose in-gate kiosks keep standard time all year while its out-gate keeps local time, so in the daylight-time
  months each stay reads an hour long and a truck's consecutive stays overlap; D2 at Pacific Gateway, where a
  transaction keyed to the wrong truck's tag and voided minutes later stays in the export beside the re-keyed one
  (the same container and gate-in under a later transaction id); D6 at Berth 40, whose runs to the on-dock rail
  ramp leave through the ramp gate and come back through it (out_lane and in_lane RG1), one stay written as two legs.
  No sentence in the pack describes any of them.
- **Ask B, each terminal's average turn time per quarter, minutes to one decimal: 12 figures.** Same path and devices.
- **The construction layer:** each link's verdict and the set.

| Ask | Cracker (stays merged as recorded) | Mirror (textbook factors) |
|---|---|---|
| A, visits (12) | miss | miss |
| B, turn time (12) | miss | miss |

Pair ceiling: 36.1 (cracker 45.0 with the call and no ask figure; mirror 27.3, eight of fifteen main figures)

Mirror leakage: 0.0 per cent of ask weight

Measured by: generator/ceiling.py

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
- 2026-10-20, stage 4 round 3 on architecture 3: readers 5 and 6 missed the call (six of six now) and kept 10 and 1
  of 18 ask figures: reader 5 priced the strip days at the next line from the quantity tie and kept the contract's
  gas day despite the calendar-day tie; both left IEEE 762's reserve-shutdown term out of the outage rate. The
  round-3 judge returned NOT_DETERMINISTIC: no file tied the SCR to instrument air (the first hour back fitted a
  restart transient as well as an uncontrolled loss), the pooled start-up profile moved DF-1, and the asks' strip
  pricing, meter clock and EFOR terms were unfiled. The register now describes the SCR's ammonia flow control
  valves as air-to-open, rule 2.2 files that the NOx emitted counts in every operating hour, the pooled profile is
  ruled out by the record (asserted), and the asks' conventions are filed. Lowering DF-1's start-up outage share to
  cut its pooled sensitivity reshuffled every unit's draws and pulled CB-2 and AF-1 to within 0.005 of the target
  under interpolation; reverted.
- 2026-10-20, stage 4 round 4 on architecture 3: readers 7 and 8 missed the call (eight of eight; reader 7 at four
  units with a pooled start-up profile) and kept 18 and 12 of 18 ask figures: with the strip line, the meter clock
  and the EFOR formula filed, both asks were procedures executed. The fuel ask is dropped (the gas invoices and the
  agreement are now declared distractors) and both asks are IEEE 762 rates by the standard's own definitions, the
  formulas left to the standard and only the events, overlap rule, capacity basis and operating time filed; the
  golden EFOR now counts reserve-shutdown derates in EFDH as the standard does. Round-4 judge: DETERMINISTIC,
  FIX_NOW on the later-report rule (now: the earlier report counts for none of its hours).
- 2026-10-20, stage 4 round 5 on architecture 3: readers 9 and 10 missed the call (ten of ten) and kept 18 and 16 of
  18 IEEE 762 figures by reconstructing the standard; judge DETERMINISTIC, APPROVE. A failed-start device for EFORd
  (fuel burned with no operation) died on paper: Part 75 makes any hour with fuel combusted an operating hour, which
  would put device rows in the call's population. Taken instead, on the coordinator's measured list: revisions under
  the same event number (D2, latest revision, not latest delivered). An event spanning a month written once per month
  (D6) was screened and dropped: rule 3.2's overlap rule already resolves it.
- Architecture 3 (combined-cycle NOx with instrument-air gaps filled at the uncontrolled level) as a whole: spent at
  stage 4 on 2026-10-20 by the coordinator's ruling under the author's rule that both scored readers must miss the
  call. Eleven of twelve readers missed it, but reader 12 in round 6 landed it from the register's "air-to-open flow
  control valves", the grounding the round-3 judge required (1 of 6 readers since that line went in). A premise the
  judge needs filed becomes readable once filed, so the next decisive step must rest on a structure only a
  cross-record or cross-period cut shows, which no filed line describes. Carried forward: the event-revision ask
  device (a forced outage revised to MO or D4 under one event number with a later report date, no adjudicating
  sentence), which held at 0 of 18 for both round-6 readers; the realism fixes (part-hour loads under nameplate,
  start profiles that differ by unit). Dropping "air-to-open" was ruled out: it reopens the round-3 judge's finding.

- 2026-10-20, at stage 4 (architecture 4 spent): isolated reader 1 (sonnet, medium, fresh unzip) landed the call and
  all 24 ask figures (score_reader.py exit 1). It saw that the remittance's bulk lines tie to the roster's counts each
  month, read the member-level lines as retroactive adjustments, netted them per member and month (3,009 added, 923
  removed, rate cell pairs to zero) and noted the result equals the remittance total: the 820 is self-describing, an
  adjustment layer over a tied roster, and reconciling a roster to capitation is the reflex of any health plan ETL
  analyst, so the exposure rebuild is a work order, not a stump. The pharmacy latest-line device fell to the same
  reflex (5,646 claim numbers with two lines, each taken at its later line). Lesson for the re-root: a decisive step
  whose evidence is a second source that ties to the first and carries signed corrections is found by the first
  reconciliation; and the latest-line-per-key device is spent in this lane. Reader 2 and the judge were stopped.
