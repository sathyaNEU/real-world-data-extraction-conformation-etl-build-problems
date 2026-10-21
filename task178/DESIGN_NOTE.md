# task178 design note

**Status: RETIRED 2026-10-21 (see ## Retired). Architecture 1 spent at stage 4 Gate F on 2026-10-21. Before that: BUILD, stage 3 green (generator checks 84 of 84, verifier 19 of 19, two byte-identical builds, precut and figures_check exit 0, leak.py REVIEW answered, guard surface exit 0 and heart WARN), waiting on stage 4's two scored readers and the judge. Architecture 1 of the redraw, card registered 2026-10-21.** The author redrew the
number in a new cell after seed FC49's product-security world died at stage 1 (its record is kept below, in the FC49 screen
record and in the Tried and rejected list). Cell, allocated by the main session:
physical-environmental-sciences / climate-weather-extremes, Forecasting. Organisation, decision, quantity and
mechanism were searched inside the cell (prototypes in the session scratchpad, b178r/proto: p1 to p13).

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task178.json`, guard `check` WARN only (time_semantics strategy
  risk, answered under `## Three rules`: no field, code, unit or definition flips the call; repeat.gate_g
  forecasting against task479, answered: the lane is Forecasting and the mechanism differs). Structural tests
  same_puzzle_older (task461) and same_driver_older (task102, task130 lineage, task134 lineage, task162, task501
  lineage) differentiated on the card, one line each.
- **Pairing:** Physical & Environmental Sciences, task type `climate-weather-extremes` (F), never drawn before.
  The deciding quantity is an extreme-sea-level exceedance frequency in a coming window.
- **World:** a fictional Maine coastal city (Port Tessaly) rebuilding Granite Wharf from 1 April to 31 May 2027
  from a temporary work trestle; the waterfront project engineer sets the trestle deck elevation in the
  construction documents before the piles are ordered. Allowed deck elevations 10.60 to 12.60 ft above MLLW at
  the harbor gauge in quarter-foot steps; the deck is set at the lowest elevation at which high water is expected
  to reach it on no more than one tide in the window.
- **Shape:** 04, setting one dial: the expected number of tides reaching the deck at every allowed elevation,
  the committed elevation and the one below it; asks supply the rest (`## Ask sheet`).
- **Strategy:** `time_semantics` (F1, the window the decision bets on), gap time, G13 then G7, Gate G
  forecasting, layer2_family field_method, layer2_pattern own:skew-surge-joint-probability-over-a-known-tidal-window.
- **Data-native sentence:** the harbor's high waters are an astronomical tide known years ahead plus a weather
  surge, and April and May 2027 fall at the 18.6-year low of the semidiurnal tide with perigee at the quarter
  moons (perigee and syzygy anti-aligned about 7 April 2027), so the window's own predicted high waters sit
  about 0.2 m below the record's April and May average and the record's exceedance rate, however trended,
  overstates the window several times over.
- **Sources (one line each):** the five client families (`two-layer-task-design.md`): field_method, the field's
  own joint-probability method done right; the textbook route is a GEV or POT on observed levels with a sea-level
  trend (Coles' sea-level examples), which takes stationarity of the total level for granted; the actuarial
  catastrophe and energy load cards: an exposure-window count, here the window is fixed by the works; the
  epidemiology surveillance cards: a baseline from history, here the baseline is not exchangeable with the window
  because part of the signal is deterministic and known. No client card exists for this domain.
- **Measured lever (p13, three seeds, on the clean truth):** at 11.75 ft the window's JPM expects 0.51, 0.64 and
  0.93 tides (truth by Monte Carlo 0.36 to 0.43); the seasonal climatology at 2027 sea level 7.3 to 8.9, a linear
  or Poisson count trend 7.0 to 10.1, the last season 6 to 9, the last three 7.3 to 9.3, the 18.6-year analogs
  4.5 to 6.0; golden family (linear or recent-20-year surge base, GPD tail, per month) picks 11.75 ft in every
  seed, every route without the window's tide picks 12.25 to 12.50 ft.

## Default path

The field's textbook route for a design water level over a works window: an extreme-value or exceedance analysis of
the gauge's own record for the window's months, trended to the year of the works.

1. Read `ptg_verified_15min_1995-01_2026-06.csv` (V readings, station datum to MLLW at 4.21 ft) and the telemetry
   after June 2026 (STND 2026), one ft MLLW series.
2. Take each tide's high water in April and May of 1995 to 2026 (the highest reading of each tidal cycle, or the
   reading at each tabled high water).
3. Move each year's high waters to 2027 sea level with the guidance's annual means and its 5.40 ft design value.
4. Count, for each pile schedule elevation, the high waters reaching it per season and average over the 32 seasons
   (equivalently a peaks-over-threshold rate, a GEV on season maxima or a trend on the season counts).
5. Take the lowest elevation the record expects to be reached on one tide or fewer: 12.35 ft (0.9 tides there,
   7.4 at 11.60 ft).

Ends on: 12.35 ft
Golden: 11.60 ft

## Stump sentence

The seasonal exceedance rate of the record's April and May high waters, moved to 2027 sea level (or fitted as a
peaks-over-threshold rate, a GEV or a count trend), expects 7.4 tides at 11.60 ft and files a 12.35 ft deck, because
it averages over every spring's astronomical tides while April and May 2027 sit at the 18.6-year low of the
semidiurnal tide with perigee at the quarter moons; summing the season's skew surges over the window's own 118
predicted high waters expects 0.4 tides at 11.60 ft and 2.3 at 11.35 ft, so the deck is 11.60 ft.

## Three rules

Task type: physical-environmental-sciences / climate-weather-extremes (F): the frequency of an extreme water level over a coming window.
Domain test: the deciding quantity is the expected number of high waters exceeding a level in a known window, built the way extreme-sea-level analysis builds it (the window's astronomical high waters joined to the season's skew-surge distribution); with hospital or grid nouns there is no forcing known years ahead under a weather residual, so the task stops making sense.
Swap: "the lowest bed count at which admissions are expected to exceed capacity on no more than one night in April and May" reads, but nothing in a hospital is published a year ahead the way the tide is, so the decisive step has nothing to act on and the call collapses to the textbook route.
Layer 1: the 15-minute export with its preamble on the 1995 station datum and quality flags (the city data system), the 6-minute telemetry in metres on the 2026 station datum (the telemetry feed), the tide-table workbook in three layouts with EST-only times to 2006 and the pre-2007 daylight rule (the harbormaster's office), the April 2026 week the sensor was off (pier repair), the legacy work-order system's UTC times and reset work orders (WOMS), mixed date formats across the two work-order systems; nothing is placed to be caught.
Layer 2: field_method: the window's expected exceedances come from the window's own known astronomical high waters convolved with the season's skew surges, not from the record's exceedance rate however trended.
Decisive step: conditioning the forecast on the published 2027 high waters, the tide being a deterministic forcing known for the window, and joining each to the April-May skew-surge distribution (observed minus predicted high water, moved off each year's sea level).
Not semantics: every field, datum and unit read correctly (STND to MLLW, metres to feet, EST to UTC, the design sea level) the textbook exceedance route still files 12.35 ft; no column, code or definition carries the tide-surge split.
Not rule application: no shipped sentence says to use the tide table for the forecast or how to combine tide and surge; the basis files only the window, the schedule, the bar, the gauge and the sea level, and executing those literally with the record's rate files 12.35 ft.
Analyst test: the textbook seasonal exceedance route (peaks over threshold, or the season counts' climatology or trend, on the gauge's April and May high waters since 1995 at the 2027 design sea level) expects 7.4 tides at 11.60 ft and ends on 12.35 ft, three schedule steps too high.
Estimand: granite_wharf_trestle_design_basis.pdf section 2: the expected number of tides between 00:00 on 1 April and 24:00 on 31 May 2027 at which the gauge's highest 15-minute reading reaches each schedule elevation, ft MLLW (1983-2001 epoch), at the guidance's 2027 design mean sea level; the deck is the lowest elevation with one or fewer.
No decoy: no memo, draft, contractor figure or published design level ships; the guidance gives only the sea level, the datum sheet only datums, the basis only the WHAT; nothing in the pack names an elevation as the answer.
No certified replay: no figure in the pack is produced by the golden method; the guidance's annual sea levels and the tables' predictions are inputs, and nothing certified is reproduced to recover a method.
Lesson: a forecast over a short window of a quantity that is partly deterministic must be conditioned on the window's known part; the record's average exceedance rate is right only for an average window, and in tidal water the window is never average. No build on file teaches a known astronomical forcing under a stochastic residual.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 season exceedance climatology at 2027 sea level (12.35 ft) | no | no | yes (the textbook route) | no | no | no | readable |
| 1 trend or Poisson trend on season counts (12.35 to 12.60 ft) | no | no | yes | no | no | no | readable |
| 2 recent seasons, last season, 18.6-year analogs (12.10 to 12.60 ft) | no | no | yes | no | no | no | readable |
| 3 highest predicted tide plus a once-in-the-window surge (12.10 ft) | no | the tide table | partly | no | no | yes | readable |
| 4 the window's predicted high waters with the season's skew surges (decisive) | no sentence names the tide or the surge | the tables are the harbor's routine archive, one sheet a year over 33 years, read by the default path to find high waters | not the textbook reflex for an exceedance count | no control ties to it | no | no: a sum of 118 conditional exceedance shares | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "expected to reach the deck on no more than one tide" | expected count at most one | at least even odds of no more than one tide (Poisson) | same call | same call |
| SF2 | the window | local dates 1 April to 31 May 2027 | UTC dates | same call | same call |
| SF3 | 2027 sea level | the guidance's 5.40 ft design value | the trend at end-2027 (5.42) | same call | basis section 2 names the design value; same call |
| SF4 | which surges | April and May skew surges | every month's | same call | same call (and March surges run 0.27 ft higher at the 99th percentile, June lower) |
| SF5 | the surge record's years | 1995 to 2026 | the last 20 years | same call | same call |
| SF6 | moving surges off sea level | each year's guidance mean | the guidance trend line | same call | same call |
| SF7 | May and June 2026 | verified | telemetry | same call | same call |
| SF8 | a tide | every high water | daily higher high waters only | same call | same call; basis: "on no more than one tide" |
| SF9 | 1995 to 2006 table times | EST all year (sheet header) | local daylight time | same call | the sheet header; the three-hour window holds every maximum |
| SF10 | interpolated readings | dropped (quality I) | kept | same call | same call |
| SF11 | the 2017-18 bracket offset | corrected for the asks | left in | same call | no April or May reading falls in it |
| SF12 | telemetry datum | STND 2026 (datum sheet) | STND 1995 | same call | same call; datum sheet revision 2026-06 |

## Ladder

| Rung | Route | Deck | Tides expected at 11.60 ft | Dies to |
|---|---|---|---|---|
| 0 | season exceedance climatology at 2027 sea level (default) | 12.35 | 7.4 | the 2027 sheet's high waters |
| 1 | linear or Poisson trend on season counts; POT GPD; GEV on season maxima | 12.35 to 12.60 | 3.1 to 8.0 | the same |
| 2 | last season, last three seasons, the 2008 and 2009 analog seasons | 12.10 to 12.60 | 4 to 8.3 | the same; 2026's springs were weak in other weeks |
| 3 | highest predicted 2027 tide plus a once-in-the-window surge | 12.10 | n/a | it sizes one tide, not the window's count |
| 3b | the window's tides with surges not moved off each year's sea level | 11.85 | 1.3 | the guidance's annual means |
| 4 | the window's 118 predicted high waters with the April-May skew surges (golden) | 11.60 | 0.4 (2.3 at 11.35) | |

Position: the golden is the lowest of every route; every route that does not read the 2027 sheet sits two to four
steps above it. Margin: at the golden's deck the default expects 19.6 times the golden's tides; the golden sits 2.6
times under the bar and the next deck down 2.3 times over it. Every golden-family construction (annual or trend
detrending, the last 20 years, telemetry for May and June 2026, per-month surges, a GPD tail) picks 11.60 and prints
0.4 and 2.3; 200 resampled records keep the call 200 times, one sigma 0.03 and 0.08 tides. Grid: the only wrong
cell below the golden is rung 3b's, above it. Worth: the decisive step moves the deck three steps.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the high waters in the window | basis section 2; C1 |
| 2 | Unit of account | a tide (a high water) | basis "on no more than one tide"; SF8 same call |
| 3 | Attribution window | 1 April 00:00 to 31 May 24:00 local | basis; SF2 same call |
| 4 | As-of dating | the 2027 sheet issued 2026-10-01; record to 30 November 2026 | the pack's own dates |
| 5 | Version basis | verified over telemetry where both exist | SF7 same call |
| 6 | Denominator | each tide's share of surges reaching the gap | n/a for a count |
| 7 | Weighting | each season surge equally | SF5, SF6 same call |
| 8 | Window length | 1995 to 2026 surges | SF5 same call |
| 9 | Boundary inclusivity | at or above the deck | basis "at or above"; no figure on an edge |
| 10 | Rounding path | expected tides summed then printed to one decimal | prompt; edges 0.029 and 0.022 |
| 11 | Tie-break | lowest elevation meeting the bar | basis "the lowest of these" |
| 12 | Maturity and censoring | none open | n/a |
| 13 | Order of operations | sea level moved before summing | additive, commutes |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | May and June 2026 in two files | SF7 same call |
| 16 | Identity normalisation | high waters matched by time | three-hour window, C1 |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | feet MLLW; telemetry metres | datum sheet; SF12 |
| 19 | Code and status semantics | quality V, I, M | dictionary; SF10 same call |
| 20 | Integerisation | none on the call | n/a |
| 21 | Clause scope | the one-tide bar over the whole window | basis section 2 |
| 22 | Forward window contents | the 2027 sheet's 118 high waters | the tide-table workbook's 2027 sheet |

## Literal reader

Executed word for word, the basis files the window, the schedule, the gauge, the 15-minute reading and the 2027
design sea level, and asks for an expected count; it leaves the method open. Every literal reading of its terms
(SF1 to SF12) gives 11.60 ft from the golden method, and the default path's 12.35 ft comes from an easier method on
the same literal estimand, never from another reading. The asks' terms: "the five tides the survival check takes"
reads basis section 3 (no two within three days; no pair of candidates sits between two and four days apart),
"each closure counted once" is forced by the records (a reset work order opens within three hours of the previous
order's closing; consecutive tides' closures sit seven hours or more apart), and the legacy times' clock is forced by
the records (read as UTC they lead high water by a median 1.1 h as the new system's do by 1.3 h; read as local they
trail it by 3.0 h).

## Oracles

none. No control, published figure or reconciliation ties under one route only: the guidance's annual means and
design sea level are inputs every route uses; the tide tables are predictions every route may read; nothing
publishes an expected count, a design water level or a past project's deck.

## Ask sheet

Criteria: the deck (1), the two expected counts (2), the design sea level component (1), ask A's ten cells (five
dates and five readings), ask B's twelve cells (six years by closures and closures at 11.80 ft), the chart (the
bars, the line, the marked deck: 2), the two files (2): 30.

- Ask A, the survival check's five tides (basis section 3): rows are every high water from November 2016 to
  November 2026 in the verified record and the telemetry; the call reads only April and May high waters, none of
  them inside either device's rows (asserted, SEP). H18: the trestle frame's survival case.
  A1 (D2, primary, split evidence): from the bracket's re-securing at 1500 on 30 October 2017 to the sensor reset at
  1430 on 12 March 2018 the verified readings run 0.08 ft low (station log entries and the datum sheet's levelling
  row; nothing joins them), so the January and March 2018 storms read low.
  A2 (D3, primary): the telemetry is on STND 2026, 0.12 ft above the station datum of the verified export (datum
  sheet revision 2026-06; the May and June 2026 overlap shows it), so the October 2026 storm reads low on the
  verified export's offset.
  Stops: the careful path (neither found) ranks 2024-01-13, 2026-10-28, 2018-01-04, 2022-12-23, 2018-03-02 at 14.59,
  14.56, 14.56, 14.27, 14.24 and misses all ten cells; with A1 alone it keeps 4, with A2 alone 2.
- Ask B, Front Street flooding closures 2017 to 2022 and those with the gauge at 11.80 ft within three hours of
  the start: rows are DPW's work orders, which the call never reads, and the gauge's readings at the closures'
  starts (Front Street floods at 11.8 ft, far above any April or May reading the call's counts turn on, and the
  call reads the gauge only at April and May high waters). H18: the access allowance in the schedule (basis section 4).
  B1 (D1, primary): WOMS opened a second work order when barricades were reset on the same flooding, 40 to 170
  minutes after the first was closed, under a new number in the year's running sequence; counting work orders adds
  7, 9, 13, 11, 3 and 8.
  B2 (D8, primary, split evidence): WOMS (to June 2023) stored times in UTC with no zone in the export, PWWorks in
  local time; read as local, the legacy closures' three-hour windows miss the high water and the at-11.80 counts fall
  to 18, 22, 22, 18, 17 and 10 (asserted: read as UTC the legacy closures lead high water as the new system's do).
  Hazards: the bracket offset (A1) on the 2017-18 winter readings, mixed date formats across the systems, other
  streets' FLOOD orders, HM-requested closures.
  Stops: the careful path misses all twelve cells; with B1 merged it keeps the six closure counts; with B2 alone, 1.
- Zero device rows in the call's population: no April or May reading in the bracket window, no April or May
  telemetry after the verified product, no work order in the call (asserted).

Pair ceiling: 28.5 (the cracker on the call keeps 0 of 22 ask cells; credited with its best single device, the reset
work orders merged, it keeps 6 for 36.0; both top responses on the call with no device found, 45.0)
Mirror leakage: 0.0 per cent of ask weight
Measured by: generator/cracker.py

| Ask | Cracker sheet (every datum the datum sheet states for the file read, work orders as listed, each system's times as wall clock) | Hits | Verdict |
|---|---|---|---|
| Ask A, five dates | highest readings on the verified export's offset, telemetry on STND 1995 | 0 of 5 | miss |
| Ask A, five readings | the same | 0 of 5 | miss |
| Ask B, closures, six years | one closure per work order | 0 of 6 | miss |
| Ask B, at 11.80 ft, six years | legacy times read as local | 0 of 6 | miss |


## Retired

Retired on 2026-10-21 under the author's rule for this round (a number that dies in its second new cell is
retired). The seed's own world (FC49, product-security triage) died at stage 1. The first redraw cell
(physical-environmental-sciences / climate-weather-extremes) carried architecture 1, the April-May 2027 trestle deck
set against the window's own predicted tides; it was built to stage 3 green and spent at Gate F when a scored
reader conditioned on the 2027 tide table and landed every call figure. The second cell
(marketing-consumer-research / conjoint-choice-willingness-to-pay-analysis, Forecasting) yielded nothing that holds
on measurement or on the screens (`## Tried and rejected`, the conjoint lines): the judgments the textbook
simulators (a logit share simulator, an aggregate MNL, an HB simulator, the first-choice rule) take for granted
either move the forecast less than their own estimator family spreads it (price non-attendance under a normal-prior
HB; a brand-by-tier interaction), or rest on a linked file whose filter or calibration is the reader's first move
(a pilot's revealed uptake, the in-market population by contract timing or footprint), or are banned as hidden
rules (a competitor's matching reaction). No card was registered in the second cell. The card for architecture 1
stays filed with `architecture_spent` set.

## Leak sweep

`leak.py` REVIEW, two lines, both answered. Sweep 3: the design basis carries every word of the committed call
because it is the WHAT (the trestle, the pile schedule, the deck elevation in ft MLLW); the schedule's nine
elevations are declared stated inputs in `metadata.json`, and the basis names none of them as the answer. Sweep 9:
the tide-table workbook carries 2027 dates after the 8 December 2026 setting because it publishes the 2027
predictions, issued on 1 October 2026 like every year's sheet. No decisive vocabulary (skew surge, joint
probability, nodal, perigee, astronomical) appears in any shipped file (asserted in `checks.py`).

## Guard

`guard.py check` on the registered card and `heart`: WARN. The time_semantics strategy risk is answered by the
analyst test (no field, code or definition flips the call); the Gate G repeat (forecasting, task479) is the lane's
objective with a different mechanism; the structural tests are differentiated on the card against task461,
task102, task130's and task134's and task501's lineages and task162. `surface`: exit 0, top pair task449 at 0.123
(one CSV column set and the decision type); the one "persona" it lifted was a street name, since renamed.
After the PAUSED commit the window moved (task251 and task478 marked spent pulled task481 into it) and `check`
BLOCKed `ban.artifact` on published_series; the card's context artifact is redrawn to filed_standard, the honester
label, since the trestle design basis is the engineer's own filed document and the tide tables are an input.

## FC49 screen record (world spent, kept for the record)

**Status: PAUSED at stage 1, no card ever registered, nothing cut.** New, Forecasting, seed FC49: a
network-equipment vendor's product-security team has one extra triage analyst for the first quarter of 2027,
who goes to the product line with the most critical triages forecast for the quarter (one triage per CVE per
affected product line, done as part of that line's advisory) if its lead over the runner-up is larger than
the forecast's own error one quarter ahead, and otherwise stays in the shared pool; the staffing note is due
on 10 December 2026. The world, the decision and the quantity were kept. The seed's own mechanisms (the
policy's four-quarter mean and eight-quarter lead deviation as a filed HOW, the vendor's severity score as
the decider, the dashboard as an official decoy, the release-train swing inflating the lead's deviation into
a hold) were never candidates. Two decisive steps were screened on code, each one of the brief's ideas in
its strongest form, over three seeds each, and neither held. No architecture is live. This note holds the
screen record only; it carries none of the `precut.py` sections, because no design exists. The prototypes
stay in the session scratchpad (b178/proto: `protoA.py`, `protoB.py`, `screen178.py`, whose output
`screen178.out` is byte-identical with `screen178_run2.out` over two runs).

**The structural sentence, and the first thing to read.** A line's coming quarter differs from its own
record only where work reaches its advisories through a channel or a train slower than the quarter: reports
waiting under embargo in the coordination centre's queue, a component refresh that triages every
third-party critical accumulated since the line's last one, a supplier's pre-notified bulletins. Every
reading of that difference that holds is a count not yet arrived, completed for the slow unit, which is
task181 v2's driver ("the units whose records arrive slowest look quiet exactly while they are surging, so
the comparison has to be made on the complete count each unit's own arrival history implies"), landed on
the portal once its estimand was filed literally, and honestly `maturity_censoring`, which task201 holds in
the ban window. The readings that are not that driver either hand the call to the cheapest route (the queue
read at face value, a rule of thumb for a long-delayed refresh) or move the decisive step into composition
(conversion or slip by case type or by line, `composition_mix` held by task165) or into semantics (which
other lines a queued report's code also ships on). The quantity is also thin where it is not pipeline: a
real vendor's own-code criticals run one to five per line per quarter, so a lead that is real against the
forecast's own error needs the counts third-party CVEs supply, and third-party CVEs reach a line only
through its refresh train. A draw on this quantity needs a difference between the coming quarter and the
record that no recorded channel already carries and no slow channel is completing; none was found here.

**The registration finding.** The honest strategies were `maturity_censoring` (candidate 1, and every
per-line reading of the queue), held by task201 (registered 13:39), and `composition_mix` (candidate 2c),
held by task165 (14:10). The window on main at 5c5631d is task201 (`operations_desk`, `season_or_peak`,
`utility_or_infrastructure`, `field_unit_lead`, `published_series`), task247 (`executive_team`,
`vote_or_meeting`, `university_or_school`, `research_desk`, `operations_log`) and task165
(`council_or_assembly`, `purchase_order_or_contract`, `local_government`, `operations_director`,
`register`). The keys this world offers honestly outside them, had a design held: organisation
`manufacturer`, forum `committee_or_panel`, forcing event `budget_or_appropriation`, role
`capacity_planner`, calibration `none`. Nothing was registered and no axis of the window was spent.

**The taxonomy finding.** A product-security team's triage workload has no client task type of its own.
Product Analytics serves Forecasting through retention, churn and feature adoption only (task162's browser
reports sat in feature adoption because version adoption decided them), and none of them is a line's
critical CVE count. The honest home is General Statistics & Data Science,
`regression-classification-model-diagnostics` (the forecast model and its out-of-sample one-quarter error),
or the house domain `business-operations-analytics` (`workforce-labour-planning`) that maps there.

**The repeat screen.** `guard.py recent`, `coverage`, `mechanisms --objective forecasting` (82 builds) and
`slots` ran before any card, `slots` on embargo, advisory, triage, refresh, roll-up, freeze, deferred,
backlog, accumulated, Hawkes, self-exciting, excitation, follow-on, variant, code age, new code, churn,
lifetime, honeymoon, spillover, embedded, sibling, shared code, fan-out and observation effort: no slot or
card spent a refresh-accumulation or forward-batch mechanism in a product-security world, and the binding
matches are by the abstraction test (task181 v2 and v3, task174's vintage screen, task136, task163,
task132, task75 v1, task199). The brief's near drivers were read in full on their cards: task162 (restart
bursts after Patch Tuesday), task148 (abandonment in a 911 queue), task159 (backlog behind full trains);
none is touched by either candidate.

## Tried and rejected

- **Candidate 1: the deferred component refresh** (the brief's release-train idea in its strongest form;
  `protoA.py`, seeds 11, 12 and 13 fixed before outcomes). Driver as drafted: a line's kernel and crypto
  updates wait for its platform release, so its recent quarters record only the rest of its third-party
  flow, the held criticals keep arriving upstream at the rate its earlier refreshes and its siblings' current
  ones show, and they land in one roll-up with the release inside the quarter. Killed at stage 1 on
  measurement (a rule of thumb lands) and on the draw screens (it is task181 v2's driver, honestly
  `maturity_censoring`).
  - The world: eight upstream component groups (kernel 4.0, crypto 2.2, SSH 0.8, web 3.0, DNS and DHCP
    1.2, routing 1.5, management 1.0, libraries 5.0 critical CVEs a month), five lines with group-specific
    affected shares, refreshes monthly (DATACENTRE), quarterly (CAMPUS), half-yearly (BRANCH in April and
    October, WIRELESS in May and November) and every four months (GATEWAY in April, August and December),
    8 per cent of upstream criticals exploited and patched out of band within three weeks, own-code
    criticals 0.8 to 2.2 a month a line, chipset bulletins 2.5 a month for WIRELESS. GATEWAY's kernel and
    crypto groups were held after its 16 September 2025 refresh until the GATEWAY 10 platform release on
    10 February 2027: seventeen months at about 4.9 affected criticals a month. As-of 10 December 2026.
  - The golden family (GATEWAY's first-quarter critical triages): its own pre-freeze group rates over each
    group's months since its last update, the same on its last 24 pre-freeze months, and the held groups
    priced at the sibling lines' post-freeze rates scaled by GATEWAY's earlier ratio to them: 104.2, 109.4
    and 91.8; 111.2, 108.8 and 105.2; 105.5, 101.9 and 118.1 (a spread of 5.5 to 16.9 per cent of the
    median, so GATEWAY's figure needs a bin of 25 or more). Realised first-quarter truth 72, 82 and 96.
  - The routes as first drawn (the runner-up 43.7 to 48.1): the trailing four quarters BRANCH, DATACENTRE,
    BRANCH; eight quarters BRANCH, DATACENTRE, DATACENTRE; the same quarter last year DATACENTRE,
    DATACENTRE, CAMPUS; the latest complete quarter and an eight-quarter trend DATACENTRE in all three; the
    average roll-up per release GATEWAY in seeds 11 and 13 (46.2 against 45.0, 46.0 against 38) and
    DATACENTRE in 12; a factor of 1.5 to 3.0 on GATEWAY's recent roll-up GATEWAY in all three.
  - With DATACENTRE's own-code criticals raised to 9 a month (the naive leader at about 70 to 80, the
    runner-up 67.2 to 74.1): every time-series and per-release route files DATACENTRE; a factor of 1.5
    misses in all three seeds, 2.0 lands in seeds 11 and 13, 2.5 and 3.0 land in all three. The factor at
    which GATEWAY overtakes is 1.55, 2.03 and 1.52 against the golden's 2.20 to 2.51, and the 2.5 and 3.0
    factors (91 to 123) sit inside the family's own 94 to 117, so a rule of thumb for "a long-delayed
    refresh is two or three times a normal one" lands the line and the figure's bin.
  - The eda6c8c screens, as code: dispersion and truncation direction do not apply (a count, no
    suppressing threshold); variance-only passes (the step moves GATEWAY's point 2.20 to 2.51 times); the
    common-exposure subset fires in its once-thought-of form, since the golden is GATEWAY's own pre-freeze
    kernel and crypto months filtered and divided, times the seventeen-month gap (equal to the family's
    median in four of six runs), and no earlier refresh closes a gap like it (the longest is four months),
    so the step's whole difficulty is recognising the held groups.
  - Why it is dead whatever the tuning: the held criticals are incurred and not yet triaged, and the
    forecast completes them for one slow unit, which is task181 v2's driver by the abstraction test (latent
    structure: records that arrive late for one unit; default: what has arrived; correction: the complete
    count the unit's own history implies) and `maturity_censoring` honestly; relabelling it time or
    decomposition to pass the window would be a lie in the card.
- **Candidate 2: the coordinated batch in the coordination centre's acknowledgement queue** (the brief's
  known-forward-workload idea, read through the queue's own slip and conversion history; `protoB.py`, seeds
  21, 22 and 23 fixed before outcomes). Killed at stage 1 on measurement in all three configurations.
  - The world: own reports that become critical advisories 2.5 to 5.5 a month a line, each acknowledged
    with a planned disclosure 45 to 120 days on and a slip drawn per case; third-party criticals 4 to 12.5
    a month a line; five earlier coordinated batches of 9 to 18 (2023 to 2025, one a year somewhere) so the
    queue's history has precedents; at the as-of a coordinated multi-vendor batch of 34 criticals listed
    against GATEWAY.
  - 2a, the batch planned for 2 February 2027 and multi-party cases slipping as single-vendor ones do: the
    face-value reading (every open case planned in the quarter, on its listed line, at full size), the
    pooled-slip reading and the golden (slip by case type) all file GATEWAY in all three seeds, so the
    cheapest queue route lands; the golden's lead over DATACENTRE is 1.7, 12.6 and 11.7 against a model
    error of 11.1 to 11.4 (ratio 0.15 to 1.10), so even the golden's pick is not robustly real.
  - 2b, the brief's slip check (the batch planned for 2 March 2027, multi-party cases slipping by a gamma
    with a mean of 48 days): the batch lands inside the quarter with probability 0.35 to 0.36, its landing
    variance takes the error to 19.0 to 19.3 against leads of 10.1 to 17.7 (ratio 0.52 to 0.92), and the
    golden (DATACENTRE) is the trailing route's and the seasonal route's answer in all three seeds while the
    face value files GATEWAY: the slip noise swamps the lead exactly as it did task174's.
  - 2c, the batch listing GATEWAY and BRANCH, which ship the same VPN stack, BRANCH affected by about 30 per
    cent of the stack's earlier coordinated cases: the face value lands GATEWAY in all three seeds and the
    pooled conversion files GATEWAY, GATEWAY and BRANCH; the step that separates (conversion read per
    listed line from the stack's earlier cases) is `composition_mix`, held by task165, and reads the
    vendor's own affected determinations, which the brief names as semantics.
  - The eda6c8c screens, as code: dispersion and truncation direction do not apply; variance-only fires in
    2b (the step lowers GATEWAY's point and raises its error, so the golden sits near the hold); the
    common-exposure subset fires in 2a and 2c (the face value is a filter and a count, and it lands).
- **Paper screens, not coded.**
  - The queue read per line at the same lead (the share of each line's quarter already acknowledged three
    weeks before it starts, from the acknowledgements as they stood, including a line whose pre-notified
    supplier bulletins are light this quarter): task181 v2's driver exactly, and `maturity_censoring`.
  - Follow-on research after a high-profile disclosure (variant hunting): task181 v3's self-exciting runs
    in the opposite direction, and critical follow-ons per trigger are a handful, too few for a real lead.
  - Code age (criticals concentrated in code shipped in the last two years, a new release yielding a wave a
    few quarters on): own-code criticals are too thin for a real lead, and a component upgrade restarting
    the curve is task132's renewal.
  - A shared-code fan-out (a batch listed against the line it was found on also lands on the line that
    embeds the same daemon): the call flips at any fan-out, so the decisive step reduces to the triage
    standard executed on an affected set inferred from co-listing, rule application on a read of the
    acknowledgement's product field.
  - The open queue as survivors (old open reports rarely become critical advisories, so the pooled
    conversion overstates the line with the stalest queue): task75 v1's open cases against completed
    durations, censoring by its honest label, and own-code counts too thin.
  - A component refresh closing an ordinary interval (the release train alone): a read of the calendar, and
    the same quarter last year lands it.
  - An upstream group's flow stepping up, or a transient upstream wave ending: with prompt triage the latest
    quarter shows it and lands; with a lagged refresh it becomes candidate 1's held backlog.
  - A staggered programme (a reachability or VEX workflow, a memory-safe rewrite) read against lines not
    yet on it: task136's and task163's common rise between the before and after windows.
  - The queue's planned dates as they stood at each origin (a real-time back-test against the overwritten
    planned-date field): task174's vintage screen on a schedule's slips, and the overwritten field makes the
    step a reading.
  - The internal testing effort read against its findings: task199's observation-effort organ, and the
    testing plan names the step.
  - The lead's error narrowed by the CVEs the top two lines share: the seed's own uncertainty-hold
    architecture, banned as a near driver, and the Poisson reflex lands any narrowing.
- **Redraw cell, climate-weather-extremes: candidates screened (2026-10-19 to 21).**
  - Mixed populations in annual maxima (tropical against extratropical): paper; the tropical population rests on
    a few dozen events, the mixture fit's spread exceeds any lever, and the storm-track file needed to split
    them is single-purpose.
  - A summer hot-day count conditioned on spring soil-moisture deficit: paper; a regression on the obvious
    covariate (the textbook route the blind readers take) with skill near r 0.4, lever under the noise.
  - Fixed-interval against sliding-window rainfall maxima (Hershfield-Weiss factor from an hourly overlap):
    paper; lever 5 to 13 per cent and the textbook 1.13 lands.
  - A declustered heat-event count (extremal index): paper; the run-length is a knob, the dispersion screen
    fires.
  - Areal against point rainfall return levels: paper; the areal-mean series fitted directly is the golden.
  - A nonstationary GEV on a warming covariate: the textbook itself.
  - Frost after bloom (phenology-conditioned frost risk): paper; the bloom model's base temperature and stage
    thresholds are open knobs, determinacy fails.
  - Joint exceedance across a network (tail dependence): paper; the estimator family's spread is wide.
  - A saturating gauge or a recorder lost in its largest events: task172's cap and task245's driver.
  - The forward astronomical tide (this draw), first form: a winter (November to February 2026-27) closure
    count at a mesotidal semidiurnal site; killed on measurement (p1, p2): the window's tidal index sits at
    0.83 to 1.0 of the long-run mean, so the climatology lands within 17 per cent.
  - Second form: March to April 2027; killed on measurement (p6, p11): the last season (2026, also weak
    springs) lands (13 against a golden 12.4 to 15.2 at one threshold, 7 against 6.2 at another).
  - Hourly non-tidal residual against skew surge as the decisive rung: killed on measurement (p6, p9): with the
    timing interaction at 0.5 to 0.8 h per metre of surge the all-hours residual and the residual at predicted
    high water both land the golden; only the cycle-maximum residual overstates (x1.5), so it is at most a lower
    rung.
  - A macrotidal estuary site: rejected on paper (p3): the tide is so dominant that every reader opens the tide
    table first.
- **Ask B, first form: a dispatcher's call record beside each crew closure from 2022** (D1). Dropped on paper: the
  source column names the dispatcher, so a careful reader drops those rows by reading it; and the new system's
  years carried no second device, so 2019 to 2026 left five years' cells to the careful path. The ask moved to
  2017 to 2022, all on the legacy system, where the reset work orders and the UTC clock move every cell.
- **Ask A, first form: a storm-peak outage on the primary, the peak on the harbormaster's tide board** (D4).
  Dropped on paper: whether the board's reading is "at the gauge" is a fork the survival definition cannot close
  without naming the board, which announces the device. The outage was removed; the board ships as a distractor.
- **Names near a real waterfront.** The first cut used a Commercial Street, a Union Wharf, a Marginal Way and a
  Custom House on a Maine harbour (Portland's own) and a city name shared with a real village; renamed before any
  reader saw the pack (`reduce-house-fixes` H21).
- **Architecture 1, the April-May 2027 trestle deck set against the window's own predicted tides: spent at stage 4,
  Gate F (2026-10-21, pack d64099d2), the judge stopped since the readers decided it.** Scored reader A landed the
  call exactly (11.60 ft, 0.4 and 2.3): "the 2027 predicted highs for 1 April to 31 May were combined with
  observed-minus-predicted peak residuals from April and May of 1995 to 2026, each year shifted to 5.40". Reader B
  filed the default path, 12.35 ft. With the tide table in the pack the decisive step is a reflex for any reader who
  thinks of it, and hiding the table would be a plant, so the architecture is spent rather than hardened. Asks: A
  kept 15 of 22 and B 16 of 22; the sensor bracket offset fell (reader A: "the sensor read 0.08 ft low from the
  2017-10-30 storm until the 2018-03-12 reset; checked against the harbormaster board") and the reset work orders
  fell to a time-gap merge ("counts did not change for cutoffs from 6.5 to 9 hours"); the legacy system's unstated
  UTC clock held for both readers (both filed 18, 22, 22, 18, 17, 10 against 24, 36, 33, 30, 20, 18). Why it held: its
  only evidence is an alignment between two files that no document invites anyone to make, while the two that fell
  each had a document naming the event (a log line, a levelling row) or a gap a reflexive dedup closes.
- **Second cell, conjoint choice and willingness to pay (Forecasting), screened 2026-10-21; nothing held, no card.**
  - Price non-attendance hidden by a normal-prior HB (`cj/ana.py`, 700 respondents, 12 tasks, three alternatives
    and none, 30 per cent ignoring price): the vendor-style HB pulls the ignorers' price coefficient to -0.33
    against a true -0.04, but the simulated shares move only 0.151 against 0.176 at the top price, every route
    (truth, HB means, aggregate MNL, latent class with one to three classes) picks the same revenue price, and the
    latent-class forms recover the truth no better than HB. Dead on lever.
  - A stated-to-revealed calibration from a two-arm price pilot of the same respondents (`cj/sprp.py`, three
    seeds): the raw simulator (0.28) already sits within the full calibration's own spread (0.26 to 0.29, around
    a truth of 0.24), because the scale and the constant offset each other at the launch price. The calibration
    regressed on noisy HB utilities also attenuates (lambda 0.45 to 0.52 against 0.55), which leaves a
    measurement-error correction as an open knob, and the pilot arms' linear extrapolation lands in one seed. Dead
    on lever and determinacy.
  - A brand-by-tier interaction the main-effects simulator cannot carry (`cj/inter.py`, two seeds): it moves the
    premium configuration's revenue 20 to 45 per cent, but the interaction family itself spreads 40 per cent
    (aggregate against HB with the interaction). Forcing it needs a holdout or model-selection criterion, which is
    the window's G16 and backtest ground, and the pick flips only when tuned near the boundary. Dead on paper.
  - The in-market population (contract end or fibre footprint correlated with preference): a join and a filter
    give the golden. That is the common-exposure subset screen, and arch 1's measured reflex on any linked forward
    input. Dead on paper.
  - Within-respondent IIA for a near-clone: the correcting rule (randomized first choice) carries an error-scale
    knob and the first-choice rule (a textbook route) lands. Dead on paper.
  - Competitor price matching read off the price history: a reaction rule recovered from records, the banned
    hidden-rule family. Dead on paper.
  - The client's four conjoint cards (IIA clone, WTP as a ratio, preference against market share with the none
    option, no out-of-range prices) are themselves the textbook routes the readers take.

