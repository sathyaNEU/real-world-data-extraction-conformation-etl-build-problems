# task474 design note: a Medicaid managed care plan's 2027 provider group designations (architecture 4)

Architecture 4, drawn 2026-10-20 in a fresh world after architecture 3 (combined-cycle NOx with instrument-air gaps)
was spent at stage 4. Earlier architectures' sections are retired; their lessons stand in Tried and rejected.

## Draw

- **Pairing.** Client domain healthcare-delivery-health-economics, task type payment-claims-health-plan-analytics,
  objective Data Extraction & Conformation (ETL): the paid medical claims, the plan's monthly enrollment roster, the
  state's capitation remittance (keyed on the state's recipient id, crosswalked through the roster) and the pharmacy
  claims are conformed into one provider-group dataset of paid cost per member-month.
- **Decision.** How many, and which, of the twelve primary care groups the plan designates for its 2027 Cost
  Performance Program: a group whose members' paid medical cost per member-month for services January to June 2026,
  paid by 31 October 2026, is $412.00 or more. Retrospective by necessity: the program reads the closed half year at
  the year-end close, for the contract year that has not begun.
- **The quantity.** Paid medical cost over the member-months in which the group's members were covered.
- **Data-native sentence.** Members renew once a year in their enrollment anniversary month and some lose coverage at
  renewal and are reinstated back to the lapse, while members who die stay on the state's file for a month or more,
  so the plan's roster, built from the state's file as processed by the 5th, is short of covered months in the
  high-churn groups and long in the frail groups, and only the state's member-level capitation lines, paid and
  recouped months later, record the difference.
- **Default path.** Member-months from the roster, cost from paid claims: PG02, PG04, PG08 and PG11.
- **Golden.** Member-months rebuilt as the roster's months plus the months the state later paid capitation for and
  less the roster months it recouped: PG04, PG07, PG08 and PG10.
- **Asks (carried device).** From the pharmacy claims, which the call never reads: later lines under the same claim
  number (a reversal at zero, a rebill moving the fill date or the product), the latest line standing.
- **Shape.** 07, a grid: twelve groups' verdicts, twelve classes by two figures, plus the count, the set and the
  memo's chart.
- **Guard.** WARN (nearest task100 v1 at 0.07); personas Paula Watts and Derrick Warren from guard.py names;
  coordinator reservations respected (shape 05 and census-register avoided).

## Default path

1. Read the rules: every group in the register; a group's members as the roster assigns them; paid medical cost of
   services January to June 2026 paid by 31 October 2026, over the member-months in which its members were covered by
   the plan; designate at $412.00 or more.
2. Take the paid claims in the window by the member's group, and count each group's member-months as its members'
   rows in the monthly enrollment roster (one row per member per month, January to June).
3. Divide, compare with $412.00.

Ends on: PG02, PG04, PG08 and PG11 designated

Golden: PG04, PG07, PG08 and PG10 designated

## Stump sentence

The default path counts each group's member-months as its members' rows in the plan's monthly roster and designates
PG02, PG04, PG08 and PG11; the roster is the state's enrollment as processed by the 5th of each month, so it never
shows the months members were reinstated back to after a renewal lapse and still lists members for months after they
died, and only rebuilding coverage from the roster together with the state's later member-level capitation lines (the
months paid off the roster added, the months recouped taken away) designates PG04, PG07, PG08 and PG10.

## Three rules

Task type: Healthcare Delivery & Health Economics, payment-claims-health-plan-analytics, which the taxonomy tags for ETL: conforming paid claims, the monthly roster and the state's capitation remittance (on its own recipient id) into a group-level cost per member-month the program designates on.

Domain test: the quantity that decides the call is each group's paid medical cost per member-month, worked as health plan analytics works an exposure base: member-months of eligibility rebuilt from enrollment and the state's eligibility adjustments (retroactive reinstatements paid on the 820, recoupments after death), not from a point-in-time roster.

Swap: "which of our twelve gyms' cost per member-month is over target, counting members from the monthly membership list" keeps the words and loses the step: a gym's list is its own record of who paid, while here the payer of record is the state, whose eligibility decisions arrive months after the roster is cut and reach the plan only as capitation paid and taken back.

Layer 1: the remittance keyed on the state's recipient id rather than the plan's member id (crosswalk on the roster); bulk capitation lines by rate cell with no member beside member-level lines; rate cell corrections as a +1 and -1 pair; institutional stays running past 30 June; a whole year of remittance advices with payment dates months after coverage; each the plan's or the state's own record, each asserted neutral on the call (checks.py R2).

Layer 2: estimand_identification by exposure construction. The methodological choice is what counts as a member-month of coverage: the roster's rows, the rows plus the months with a claim, the rows plus reinstated months, the rows less recouped months, or the covered months rebuilt from both sources.

Decisive step: rebuilding each group's member-months of coverage from the roster and the state's member-level capitation adjustments, adding the reinstated lapse months the roster never caught and removing the post-death months the state recouped, rather than taking the point-in-time roster as the exposure base.

Not semantics: every field read correctly (the roster's as_of, the remittance's signed member_count, the recipient id) still leaves the easy route on the roster's rows; no field or definition says the roster is short or long, and the roster is exactly what the notes say it is.

Not rule application: rule 2.2 files the outcome, the window and "the member-months in which its members were covered by the plan"; no rule or note says where coverage is recorded or that the roster misses any of it, and executing every stated rule on the roster files PG02, PG04, PG08 and PG11.

Analyst test: a strong analyst who reads every field and rule correctly and counts member-months from the roster designates PG02, PG04, PG08 and PG11 designated (the default path's Ends on); only the coverage rebuilt from the roster and the remittance's member lines designates PG04, PG07, PG08 and PG10.

Estimand: rules 2.1 to 2.3 (cost_performance_program_rules_2027.pdf) file the population (the register's groups and the members the roster assigns them), the outcome (paid medical cost of services 1 January to 30 June 2026, paid by 31 October 2026), the unit (per member-month of coverage by the plan), the window and the comparison ($412.00 or more).

No decoy: nothing is planted to be caught; the roster is the plan's ordinary monthly file, the remittance the state's ordinary 820 advices, no memo, earlier list or reported rate ships, and no document mentions lapses, reinstatement or deaths.

No certified replay: no certified or published figure is reproduced to recover the method; coverage is rebuilt from member-level records directly.

Lesson: in Medicaid managed care the exposure base is eligibility as the state finally adjudicates it, which the capitation adjustments record months after the roster is cut; a point-in-time roster understates exposure where renewal churn is high and overstates it where members die, and a cost per member-month on it ranks groups by their churn and frailty. No build on file rebuilds an exposure base from a payer's later adjustments.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the roster's member-months, the default path (PG02, PG04, PG08, PG11) | rule 2.2 "member-months": fires | one row per member per month: fires | none | none | none | a count | readable |
| R1, roster plus months with a claim (PG02, PG04, PG08, PG11) | none | claims for members off the month's roster: fires | the orphan-claim reflex: fires | none | an unmatched join: fires | a union | readable |
| R2, roster plus reinstated months (PG04, PG08) | none | member-level remittance lines: fires | none | none | none | a union | readable |
| R3, roster less recouped months (six groups) | none | negative member lines: fires | none | none | none | a difference | readable |
| G (decisive), coverage rebuilt from both adjustments (PG04, PG07, PG08, PG10) | no clause says the roster misses coverage | no column holds coverage | no reflex reconciles a roster to capitation both ways | none | none | none | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | member-month | a calendar month of coverage | a day-weighted month | same call (both files monthly, asserted) | the roster and remittance grain |
| SF2 | paid by 31 October | paid_date on or before 2026-10-31 | none in the extract later | same call (asserted) | the extract |
| SF3 | services received January to June | service_from in the window | service_to in the window | same call (asserted) | rule 2.2 |
| SF4 | $412.00 or more | at or above, unrounded | rounded to the cent or dollar | same call (nearest group $5.83 away, asserted) | rule 2.3 |
| SF5 | a group's members | pcp_group_id on the roster, one group per member | none: every claim's member is on the roster | same call (asserted) | rule 2.1 |
| SF6 | the month of death | covered (the state recoups only later months) | dropped | same call (asserted) | the remittance |
| SF7 | covered by the plan | roster plus paid, less recouped | roster only | not the rule's quantity: files PG02, PG04, PG08, PG11 | rule 2.2 "covered by the plan" |
| SF8 | the files the call reads | claims, roster, remittance, register | the pharmacy or quality files | same call (asserted) | rule 2 |

## Ladder

Built figures, read from the cut pack by `generator/checks.py` (paid medical cost per member-month, against $412.00).

- **R0, the roster, the default path (PG02, PG04, PG08, PG11).** PG02 $421.29, PG11 $420.26 over; PG07 $406.52 and
  PG10 $402.41 under. Dies to the remittance's member lines: 3,009 member-months paid off the roster and the roster
  months recouped.
- **R1, roster plus claim months (the same four).** PG11 $415.60: a lapse month with no claim stays out.
- **R2, reinstatements only (PG04, PG08).** PG07 $402.69, PG10 $399.67: the post-death months stay in.
- **R3, recoupments only (six: PG02, PG04, PG07, PG08, PG10, PG11).** The lapse months stay out.
- **G (PG04 $467.94, PG07 $417.83, PG08 $431.18, PG10 $418.29).** The truth (coverage known, generator only) gives
  the same rates to the cent.
- **Margins:** every golden rate at least $5.00 from $412.00; every group a rung flips crosses by $3.00 or more; of
  the sixteen combinations of the construction's steps (reinstatements, recoupments, claim months, rate cell pairs
  netted or not), only those with both adjustments land the golden (checks.py).
- **Worth:** R0 keeps eight of twelve verdicts and not the set, so the asks carry the pair (Ask sheet).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the register's twelve groups and the members the roster assigns (rule 2.1) |
| 2 | Unit of account | the group; dollars per member-month |
| 3 | Attribution window | services 1 January to 30 June 2026 (SF3) |
| 4 | As-of dating | claims paid by 31 October 2026 (SF2); extracts of 2 November |
| 5 | Version basis | the remittance as paid through the extract |
| 6 | Denominator | member-months of coverage (SF7) |
| 7 | Weighting | none: each group's totals |
| 8 | Window length | six months |
| 9 | Boundary inclusivity | $412.00 or more (SF4) |
| 10 | Rounding path | rates unrounded; pharmacy dollars summed then rounded to the dollar |
| 11 | Tie-break | none: each group against the benchmark |
| 12 | Maturity and censoring | four months of claims run-out, filed |
| 13 | Order of operations | crosswalk, net the member lines, coverage, cost, rate, comparison |
| 14 | Row order | none |
| 15 | Duplicate resolution | the remittance's lines netted per member and month; pharmacy lines at the latest per claim number |
| 16 | Identity normalisation | the state's recipient id to the plan's member id through the roster |
| 17 | Netting | rate cell pairs net to zero (SF7) |
| 18 | Dimensional units | dollars, member counts |
| 19 | Code and status semantics | signed member_count; never the stump |
| 20 | Integerisation | none before the comparison |
| 21 | Clause scope | rule 2 the designation, rule 3 the pharmacy summary |
| 22 | Forward window contents | the 2027 program designated on the closed 2026 half year (Draw) |

## Literal reader

Executed word for word, the rules fix the population (the register's groups and the roster's assignment), the
outcome (paid medical cost of the window's services paid by 31 October), the unit (the member-months in which the
members were covered by the plan), the window and the benchmark. Where coverage is recorded is not filed: the
candidates are the roster's rows, the roster with claim months, and the roster corrected by the state's member-level
capitation lines (one or both directions). The data separate them: the remittance pays 3,009 member-months for months
the roster does not list and recoups months it does, and every combination short of both adjustments files another
set (checks.py). Every write-up step names the file and rule it executes.

WHAT screen (stumping 1.2): population, rule 2.1 ("the members the plan's enrollment roster assigns to it", every
group in the register); outcome, rule 2.2 (paid medical cost of services 1 January to 30 June 2026, paid by 31 October
2026); window, rule 2.2; unit, rule 2.2 ("the member-months in which its members were covered by the plan"); comparison,
rule 2.3 ($412.00 or more). The decisive step settles none of them: covered member-months are filed plainly, and the
step is how that filed quantity is measured where the roster under-records it (reinstatements) and over-records it
(deaths), the remittance's member lines and the paid claims separating the candidates and no file naming the move.

## Oracles

None. No control, published figure or reconciliation ties only under the golden: the bulk capitation lines pay the
roster's counts, so the remittance's own totals tie to the roster under every route.

## Ask sheet

- **Ask A, every drug class's paid pharmacy cost, January to June 2026 fills, dollars to the nearest dollar: 12
  figures.** H18 home: rule 3.1, the committee's formulary review beside the designations. Path: the pharmacy claims,
  the drug class crosswalk, the rules. Primary device: D2, the record is the latest line under a claim number; later
  lines under the same number reverse a fill at zero, move its fill date by a few days, or change the product to
  another class, with no sentence describing them. Filtering to the window and class first and then keeping the
  latest line per claim number (the careful path) keeps the superseded line of every class change and every fill moved
  out of the window; summing every line counts each rebill twice.
- **Ask B, every drug class's number of fills: 12 figures.** Same path; a reversed fill is not a fill.
- **The construction layer:** each group's verdict and the set.

| Ask | Cracker (filter first, then latest) | Mirror (roster) |
|---|---|---|
| A, paid by class (12) | miss | miss |
| B, fills by class (12) | miss | miss |

Pair ceiling: 37.7 (cracker 45.0 with the call and no ask figure; mirror 30.4, eight of thirteen main figures)

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

