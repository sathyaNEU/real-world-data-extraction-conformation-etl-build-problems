# task474 design note: a Medicaid managed care plan's 2027 provider group designations (architecture 4)

Architecture 4, drawn 2026-10-20 in a fresh world after architecture 3 (combined-cycle NOx with instrument-air gaps)
was spent at stage 4. Earlier architectures' sections are retired; their lessons stand in Tried and rejected.

## Draw

- **Pairing.** Client domain healthcare-delivery-health-economics, task type payment-claims-health-plan-analytics,
  objective Data Extraction & Conformation (ETL): paid medical claims, the plan's monthly enrollment roster snapshots,
  the state's capitation remittance, the provider attribution file and the pharmacy claims are conformed into one
  provider-group-by-year dataset of cost per member-month.
- **Decision.** How many, and which, primary care provider groups the plan designates for its 2027 cost-performance
  program: a group whose attributed members' 2026 (January to September) paid medical cost per member-month is at or
  above the plan's benchmark. Retrospective by necessity: the program reads the closed period at the year-end close.
- **The quantity.** Paid medical cost over member-months of coverage, each group over its attributed members.
- **Process structure (the data settle it, no document names it).** Members renew once a year in their enrollment
  anniversary month; some lose coverage at renewal and the state reinstates them retroactively to the date they lost
  it. The plan's monthly roster, a snapshot taken early in each month for the capitation file, never shows the lapse
  months, but the state's later capitation payments for those months, and the claims the plan paid for them, do.
- **Default path.** Member-months from the roster, cost from paid claims: the groups whose members churn most carry
  the most cost on the fewest roster months and cross the benchmark.
- **Golden.** Member-months rebuilt from the roster plus the months the state later paid capitation for (a cross-record
  cut of the remittance against the roster, the lapses clustered at each member's anniversary month).
- **Asks (carried device).** From the pharmacy claims, which the call never reads: a claim reversed and rebilled under
  the same claim number, the latest line standing.
- **Shape.** 07, a grid: provider groups by figures, plus the count, the set and the memo's chart.
- **Guard.** WARN (overuse of the objective and Gate G mechanism; decision type repeats task251); personas Paula Watts
  and Derrick Warren from guard.py names; coordinator reservations respected (shape 05 and census-register avoided).

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

