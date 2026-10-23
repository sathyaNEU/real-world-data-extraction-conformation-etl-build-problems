# task178 design note

**Status: PAUSED (2026-10-23). Architecture 2 spent at stage 4, Gate F (pack cc9cb2f1): the judge returned
DETERMINISTIC / APPROVE, but both scored readers landed the call (`## Tried and rejected`). The number stays open
and rests.** Architecture 2, the rebuild. The number was RETIRED on 2026-10-21 and reopened under the author's
rule that no number stays retired (`## Rebuild (2026-10-23)`). Cell allocated by the main session:
physical-environmental-sciences / hydrology-flood-frequency, Forecasting. Organisation, decision, quantity and
mechanism were searched inside the cell; prototypes in the session scratchpad (b178n/proto: p1 to p4, the scans).

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task178.json`, registered and committed DRAWN on 2026-10-23 (9bb65027);
  guard `check` on the registered card WARN only: overuse.objective and overuse.gate_g (the lane is Forecasting),
  repeat.gate_g forecasting against task170 and task173 (the lane's objective, a different mechanism). Structural
  tests same_puzzle_older (task238, task101, task469) and same_driver_older (task138 and its round 2 lineage)
  differentiated on the card, one line each, with lines added unasked against task229, task249's v5 lineage,
  task452, task466 and task173, the nearest hydrometric and same-day ground. Architecture 1's identity (the harbour
  trestle deck) is in the card's `lineage` with its fate; the conjoint cell registered no card and is named there.
- **Window moves answered at the draw:** task173 registered while this card was drafted and BLOCKed `ban.artifact`
  (filed_standard), `ban.org_family` (local_government) and `test.same_driver` (population, G14, forecasting against
  task173's lineage). Redrawn honestly then: the owner became the company that runs the gauge and owns the pipe
  bridge (an investor-owned water utility, `utility_or_infrastructure`); the context artifact the crossing
  alternatives study, which carries each alternative's capacity (`capacity_report`: the standard's section is an
  input, the study frames the decision); the decisive generator G3 (the recorded stage against the discharge the river
  carried, as the gaugings measure it) with G14 second, the same two codes in the order the record reads them.
- **The window moved again after the PAUSED commit.** task170 and task173 were marked `architecture_spent` after this
  card was filed, so the card's live window fell back onto task175, task478 and task169, and `check` and `heart` BLOCKed
  `ban.org_family` (utility, task175), `ban.forcing_event` (purchase_order_or_contract, task478), `ban.artifact` and
  `ban.pattern` (capacity_report and G3, task169). Redrawn where the world honestly allows: the owner is now a pulp and
  paper mill, Callender Paper Company's Sauer mill, which runs TUM-02 for its water right and intake and carries its
  raw-water main on the pipe bridge (`manufacturer`; nothing in the analysis, the pack's numbers or the prompt
  changed, only the owner's name and the documents' voice), and the forcing event the 2027 in-water work season the
  waterway choice must meet (`season_or_peak`; the design-build award follows from it). The card was re-registered
  under the serial lock; at its new filing time the artifact and pattern clear with no change, which the card's notes
  say in so many words.
- **Pairing:** Physical & Environmental Sciences, task type `hydrology-flood-frequency` (F). The deciding quantity is
  the 1 per cent annual exceedance probability (AEP) peak discharge at a river gauge.
- **World (fictional):** Callender Paper Company's Sauer mill, a pulp and paper mill in a western Washington valley,
  carries its 36-inch raw-water main over the Tumwick River on the Sauer pipe bridge, 900 ft below its own stage gauge
  TUM-02 (no tributary between), which the mill has run since 1979 for its water right and intake. Drift struck the
  bridge in the January 2025 flood and it is being replaced, with in-water work in the 2027 season; the consultant's
  alternatives study gives seven waterway alternatives, A to G, passing 10,400, 11,600, 12,900, 14,700, 16,200,
  17,800 and 19,500 cfs with the pipe's clearance. The design discharge is the 1 per cent AEP peak at TUM-02 by the
  company's engineering standard from water years 1980 to 2025, and the alternative is the smallest that passes it.
  The gauge records stage only; discharge comes from a rating fitted to the mill's own 468 field measurements (wading
  and cableway current meter to 2004, ADCP and FlowTracker from 2005), 79 of them made at stages above the break, by
  cableway and boat while the river was on its pasture.
- **Shape:** 04, setting one dial: the seven capacities against the design discharge, the committed alternative and
  the one below; asks A (ten work windows, stage and date) and B (six water years, pipe level and fall) supply the
  rest (`## Ask sheet`).
- **Strategy:** `other` (a measurement relation that changes form, fitted per segment and carried through every
  annual peak, against one pooled relation), gap population (the rating's evidence is mostly in-bank measurements;
  the decision rests on the overbank peaks), G3 then G14, Gate G forecasting, layer2_family field_method,
  layer2_pattern own:floodplain-segment-of-the-rating-under-the-annual-peak-series.
- **Data-native sentence:** the Tumwick leaves its banks onto a wide left-bank pasture at about 10.3 ft on the gauge,
  which about half its annual peaks pass, while the hydrographers' routine measurements are made every five to seven
  weeks at wading and cableway stages, so the gauging record holds about five in-bank measurements for every overbank
  one, and any single stage-discharge curve fitted to it bends to the in-bank control and runs under the floodplain
  flows that set the upper tail of the annual peak series.
- **Sources (one line each):** no client card exists for this domain; the five families
  (`two-layer-task-design.md`): field_method, the field's own method done right (the stage-discharge rating fitted by
  control segment), with estimation_fit's "the data's real structure" behind it; the textbook route (a Bulletin
  17-style log-Pearson Type III on the annual maximum series with a weighted regional skew, or a GEV, with a trend
  check on the obvious covariate) is the default path and takes the peak discharges as given; task452's record (a
  kinked concentration-discharge rating set aside because data above the kink were too thin to fix its form) is the
  warning this draw answers by measuring the segmented family's spread with gaugings up to the flood of record.
- **Measured lever (checks.py on the cut pack; the scans on 40 worlds in the session scratchpad):** one power law
  fitted to every gauging on logs files 9,983 cfs (10,000, Alternative A), 28.5 per cent under the golden's 13,967
  (14,000, Alternative D); in arithmetic units 12,070 (Alternative C); a log-log quadratic 10,103 and a wide smooth
  10,318 (both A); GEV on the default's peaks 8,049; station skew alone 9,026; generalized skew alone 11,758; a
  log-linear trend to 2027 10,204. Across 40 seeds the single curve lands 22 to 48 per cent under. The standing
  family (21 constructions: channel plus floodplain and two separate power laws with the break at 9.9 to 10.5 ft, the
  fitted break, local smooths at spans 0.12 and 0.18, Poor measurements dropped, measurements from 1990 or 2005) runs
  13,804 to 14,126 cfs, a 2.3 per cent spread, every member printing 14,000 and D. One sigma of the golden over 200
  resampled gauging records is 343 cfs, which keeps 14,000 and D; D holds in 97.5 per cent of them.

## Default path

The field's textbook route for a design flood at a gauged site: the annual maximum series, discharges from the
gauge's rating, a log-Pearson Type III with the standard's weighted generalized skew.

1. Read the annual peak register (`tum02_annual_peaks_wy1980-2015.csv`) and take water years 2016 to 2025's maxima
   from the 15-minute export (`tum02_stage_15min_wy2016-2025.csv`, PST, water years October to September), all 46
   peak stages on the current gauge datum (2.00 ft onto the stages before October 2009).
2. Stack the two measurement files, converting the ADCP discharges from cubic metres a second and the pre-2009 gage
   heights to the current datum: 468 measurements.
3. Fit the rating Q = C (h - e)^b to every measurement (least squares on logs, the offset fitted).
4. Turn each of the 46 peak stages into a discharge through it.
5. Fit the standard's log-Pearson Type III (moments of the base-10 logs, station skew weighted with the generalized
   skew of 0.05 by their mean square errors) and read the 1 per cent AEP discharge: 9,983 cfs, which the smallest
   alternative passes.

Ends on: Alternative A (10,400 cfs)
Golden: Alternative D (14,700 cfs)

## Stump sentence

One power-law rating fitted to all of TUM-02's 468 gaugings and carried through the 46 annual peak stages into the
standard's weighted-skew log-Pearson Type III puts the 1 per cent flood at 10,000 cfs and files Alternative A
(10,400 cfs), because the 79 gaugings that bend the rating upward above the bank at about 10.3 ft are a sixth of the
record and the fit follows the in-bank control; a rating with its own floodplain term above the break, fitted on
those gaugings and carried through every peak stage, puts it at 14,000 cfs and files Alternative D (14,700 cfs).

## Three rules

Task type: physical-environmental-sciences / hydrology-flood-frequency (F): the 1 per cent annual exceedance discharge at a gauged river site, for a crossing's design.
Domain test: the deciding quantity is the 1 per cent AEP peak discharge, estimated the way flood hydrology estimates it (a log-Pearson Type III on the annual maximum series with a weighted generalized skew), on peaks a hydrographer turns from stage into discharge through a stage-discharge rating fitted to field measurements, which changes form where the river leaves its banks; with hospital or grid nouns there is no stage, control, bank or floodplain for the measurement step to live in, and the task stops making sense.
Swap: "which ward expansion is the smallest that holds the 1 per cent busiest day of admissions, from 46 years of a census index converted through a staffing ratio fitted to audits" reads, but nothing in a ward converts through a relation that changes form at a physical level about half the peaks cross, so the decisive step has nothing to act on.
Layer 1: the gauge datum lowered 2.00 ft in October 2009 with older stages and measurements on the old datum (the station description and the levels log); measurement notes transcribed from paper in three decade layouts in cfs to 2004 against the measurement database's export with ADCP discharges in cubic metres a second through water year 2014 (two systems); the peak register kept in a spreadsheet to water year 2015 and later peaks only in the time-series system's 15-minute export on PST; telemetry re-sent rows and short gaps; three peaks from a crest-stage gauge noted in the register's remarks; measurement ratings and remarks in free text; nothing is placed to be caught.
Layer 2: field_method: the annual peaks' discharges come from a stage-discharge rating fitted by control segment, with a floodplain term fitted on the measurements above the bank and carried through every peak stage, not from one curve fitted to every measurement; the frequency fit then follows the standard.
Decisive step: fitting the rating with its own segment above the bank, where the floodplain adds conveyance the channel's power law cannot carry, from the overbank gaugings, and turning every annual peak stage into discharge through it before the frequency analysis.
Not semantics: every field, datum, unit and clock read correctly (the 2009 datum, cubic metres a second to cfs, the PST export, the crest-stage remarks), one power law fitted to all the gaugings still files Alternative A; no column, code or remark carries the break, and the measurements' discharges are plain numbers.
Not rule application: no shipped sentence says how to build the rating, where it breaks or which measurements to weight; the standard files the frequency method and the study the capacities and the selection rule, and executing every filed sentence with one fitted curve files Alternative A. Enumerated family (one power law on logs or in arithmetic units with the offset fitted or fixed, a log-log quadratic, a wide smooth, the floodplain term from a break at 9.9 to 10.5 ft or fitted, as a channel-plus-floodplain sum or a separate power law, local smooths): 1 per cent floods from 8,049 to 14,126 cfs, Alternatives A to D; standing family (the forms the gaugings above the break do not refute): 13,804 to 14,126, a 2.3 per cent spread, all printing 14,000 and D; the ruling-out: one power law leaves the gaugings above 11 ft a median 13 per cent above it while the in-bank residuals stay within 4 per cent, a structured residual the curve's overall fit statistic hides.
Analyst test: a strong analyst who reads every file correctly, extracts all 46 peaks on the current datum, converts the ADCP discharges and runs the standard's weighted-skew log-Pearson Type III, but rates the peaks through one power law fitted to all the gaugings, files a 1 per cent flood of 10,000 cfs and Alternative A (10,400 cfs), against Alternative D (14,700 cfs); fitted in arithmetic units the same curve files Alternative C.
Estimand: the crossing alternatives study (section 3) and the design standard (4.2.2 to 4.2.5): the peak discharge at TUM-02 with a 1 per cent chance of being exceeded in any year, from the gauge's annual peaks of water years 1980 to 2025 (the largest instantaneous discharge of each water year), by the standard's log-Pearson Type III; the alternative is the smallest whose capacity is at least that discharge.
No decoy: no published discharge, rating table, earlier flood study, memo or contractor figure ships; the study gives only capacities and the rule, the standard only the frequency method and the generalized skew; nothing in the pack converts a stage to a discharge or names an alternative as the answer.
No certified replay: no figure in the pack is produced by the golden method; the gaugings are field measurements every route uses, and nothing certified is reproduced to recover a method.
Lesson: a flood-frequency estimate is only as good as the discharges under it, and at a stage gauge those come from a rating whose top is where the river leaves its channel; a curve fitted to the whole gauging record follows the many in-bank measurements and understates every overbank peak, and through the fitted skew it understates the rare flood far more than any single peak. No build on file teaches the rating's form under the annual peak series.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 one power law on logs, standard LP3 (Alternative A, 9,983 cfs) | no | no | yes (the textbook route) | no | no | no | readable |
| 1 GEV, station or generalized skew alone, a trend to 2027 on the same peaks (8,049 to 11,758) | no | no | yes | no | no | no | readable |
| 2 one power law in arithmetic units, a log-log quadratic, a wide smooth (Alternatives A and C) | no | no | partly | no | no | no | readable |
| 3 the rating with its own floodplain term above the break, carried through every peak (decisive) | no sentence names a break, a floodplain or a segment | the gaugings are one register in two systems, read by every route to fit the rating | not the textbook reflex for a rating, which is one power law | no control ties to it | no | no: the peaks' discharges enter the fit through the skew of their logs | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the water year | 1 October to 30 September, local | the PST export's dates | same call | same call (no peak within two days of 1 October) |
| SF2 | the 15-minute export's re-sent rows | collapsed | kept | same call | same call (exact repeats) |
| SF3 | the register's crest-stage years (1986, 1997, 2007) | entered as recorded | dropped | same call | same call |
| SF4 | Poor-rated measurements | kept | dropped | same call | same call (13,850, D) |
| SF5 | low outliers | none flagged | Grubbs-Beck applied | same call | same call (no low outlier, golden or default) |
| SF6 | trend check (4.2.6) | not significant | significant | same call | same call (Mann-Kendall p above 0.05 both ways) |
| SF7 | "at least the design discharge" | capacity at or above | strictly above | same call | same call (no capacity within 4 per cent) |
| SF9 | the 2000-04 notes' gage height | Mean GH | mean of start and end | same call | same call (within 0.01 on every row) |
| SF10 | measured discharge precision | three significant figures as shipped | the field values | same call | same call (under 0.5 per cent) |

## Ladder

| Rung | Route | 1 per cent flood (cfs) | Alternative | Dies to |
|---|---|---|---|---|
| 0 | one power law on logs, the standard's LP3 (default) | 9,983 | A | the gaugings above 11 ft, a median 13 per cent over the curve |
| 1 | the same peaks: GEV, station skew alone, generalized skew alone, a log-linear trend to 2027 | 8,049 to 11,758 | A or B | the same, and the standard |
| 2 | one power law in arithmetic units; a log-log quadratic; a wide smooth (span 2/3) | 12,070; 10,103; 10,318 | C; A; A | the same residuals above the bank |
| 3 | the floodplain term above a fitted break (golden), or any of the 21 standing forms | 13,967 (13,804 to 14,126) | D | |

Position: the golden is the highest of every route; every route that keeps one curve through the record sits one to
three alternatives under it. Margin: D's 14,700 cfs clears the golden by 5.2 per cent and C's 12,900 sits 7.6 per cent
under it; one sigma (343 cfs over 200 resampled gauging records) stays inside both and inside the 14,000 bin. Worth:
the decisive step moves the call three alternatives and the design discharge 4,000 cfs.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the 46 water years 1980 to 2025 | study section 3; standard 4.2.2 |
| 2 | Unit of account | one water year's peak | standard 4.2.2 |
| 3 | Attribution window | 1 October to 30 September | standard 4.2.2; SF1 same call |
| 4 | As-of dating | pack pulled 2026-01-20; record to 30 September 2025 | the files' own dates |
| 5 | Version basis | the 15-minute export for 2016 to 2025, the register before | station description, Records |
| 6 | Denominator | n of the 46 logs (n - 1 for the standard deviation) | standard 4.2.3 |
| 7 | Weighting | station and generalized skew by their MSEs | standard 4.2.4 |
| 8 | Window length | water years 1980 to 2025 | study section 3 |
| 9 | Boundary inclusivity | capacity at least the discharge | study section 3; SF7 same call |
| 10 | Rounding path | the discharge printed to the nearest 1,000 cfs after the pick | prompt; 467 cfs inside its bin |
| 11 | Tie-break | the smallest qualifying alternative | study section 3 |
| 12 | Maturity and censoring | none: every water year complete | standard 4.2.2 |
| 13 | Order of operations | rate each peak stage, then fit | standard 4.2.2 (discharges are fitted) |
| 14 | Row order | none | n/a |
| 15 | Duplicate resolution | re-sent rows collapsed | SF2 same call |
| 16 | Identity normalisation | gauge TUM-02 throughout | n/a |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | cfs; m3/s through water year 2014 | the export's discharge_unit column |
| 19 | Code and status semantics | quality Good, Fair, Poor; E, G, F, P | dictionary; SF4 same call |
| 20 | Integerisation | none on the call | n/a |
| 21 | Clause scope | 4.2 applies to the crossing at the gauge | study section 3 (the drainage area is the gage's) |
| 22 | Forward window contents | any year of the bridge's service, stationary record | standard 4.2.1; SF6 same call |

## Literal reader

Executed word for word, the study and the standard file the population (the 46 water years' annual peaks at TUM-02),
the outcome (the largest instantaneous discharge of each water year), the distribution and its fitting, the
generalized skew and its weighting, the 1 per cent exceedance and the selection rule; they leave the discharge of each
peak, and so the rating, open. Every literal reading of their terms (SF1 to SF10) gives 14,000 cfs and Alternative D
from the golden method, and the default path's Alternative A comes from an easier rating on the same literal
estimand, never from another reading. The asks' terms: "the highest stage the river reached" is the river's stage,
which a reading lifted by an orifice purge inside a logged visit is not (the lift follows each logged purge time by 0 to
15 minutes on the local clock, asserted on every purge); "the water level at the pipe bridge's radar" is the water's
elevation, the sensor face less the measured distance, and "the moment TUM-02 recorded each water year's crest" is
the gauge's crest reading, both forced by the records (the historian's legacy stamps read as UTC put the radar's
hydrograph 0 to 30 minutes behind the gauge's, read as local eight hours late; the levels log puts the face at 199.34
ft at install and 199.84 ft in 2023, with the bracket work order of 16 November 2022 between).

## Oracles

none. No control, published figure or reconciliation ties under one route only: no discharge, rating table or
earlier flood study ships; the alternatives' capacities and the generalized skew are inputs every route uses.

## Ask sheet

Criteria: the alternative (1), the design discharge (1), the station skew (1), the chosen and next-smaller capacities
(2), ask A's twenty cells (ten stages and ten dates), ask B's twelve cells (six levels and six falls), the chart (the
peaks, the curve, the seven capacities with D marked, the 1 per cent point, the title: 5), the two files (2): 44.

- Ask A, the contractor's work-area isolation (study section 5): the highest stage the river reached at TUM-02 in each
  15 July to 15 September window, 2016 to 2025, with its date. Rows: the 15-minute export's summer readings and the
  visit log, which the call never reads (the call reads each water year's single highest reading, all in winter).
  A1 (D8, primary, split evidence): the hydrographers purge the bubbler's orifice line at visits, which lifts the next
  two readings 0.3 to 1.45 ft; the visit log records arrival, departure and purge times on the local wall clock while
  the export is on PST, so in daylight time a careful path that drops the visit's readings on the export's clock drops
  the hour after the lift and keeps it. Every window's highest raw reading is a purge lift.
  A2 (hazard): the 11 June 2025 controller swap entered an offset 0.47 ft high until the 27 August reset; the visit
  log's logger and staff readings give it.
  Stops: the careful path (visit readings dropped on the export's clock, the offset taken off) keeps 0 of 10 stages and
  0 of 10 dates; with no visit handling, the same.
- Ask B, the reach model's calibration (study section 4): the water level at the pipe bridge's radar at TUM-02's crest
  reading in each water year 2020 to 2025, and the fall from the gauge to the pipe at that moment. Rows: the SCADA
  historian export, which the call never reads, and the gauge's six crest readings.
  B1 (D8, primary): the historian replaced on 21 June 2022 (work order) stored its legacy stamps in UTC with no zone in
  the export and the new one local wall clock; read on one clock, 2020 to 2022's crest moments land eight hours away.
  B2 (D2, primary, split evidence): the radar's bracket was replaced on 16 November 2022 (work order) and its face
  resurveyed 0.50 ft higher on 3 May 2023 (levels log), while SCADA kept computing the level from the install face, so
  the level tag reads 0.50 ft low from the bracket on.
  Hazards: debris spikes in the radar's distance during floods, short comms gaps, the daylight-time repeat hour.
  Stops: the careful path (stamps and level tag as exported) keeps 0 of 12; the clock fixed alone keeps 3 levels and 3
  falls, the face fixed alone 3 and 3.
- Zero device rows in the call's population: no purge lift or offset at any water year's crest reading, every lift a
  foot or more under its water year's crest, and the call reads no SCADA, visit or work-order file (asserted, SEP).

Pair ceiling: 28.5 (the cracker on the call keeps 0 of 32 ask figures, 45.0; the mirror off the call keeps 0 of 32,
12.0)
Mirror leakage: 0.0 per cent of ask weight
Measured by: generator/cracker.py

| Ask | Cracker sheet (every filed sentence executed, re-sent rows collapsed, the export on PST, visit times on the export's clock, the offset from the visit log, historian stamps and level tag as exported) | Hits | Verdict |
|---|---|---|---|
| Ask A, ten window stages | a purge lift kept in every window | 0 of 10 | miss |
| Ask A, ten window dates | the same | 0 of 10 | miss |
| Ask B, six pipe levels | legacy stamps eight hours off; the level tag 0.50 ft low after the bracket | 0 of 6 | miss |
| Ask B, six falls | the same | 0 of 6 | miss |

## Leak sweep

`leak.py --asof 2026-01-20` REVIEW, every line answered. Sweep 3: five ask B figures appear as SCADA level-tag
readings because the golden is a reading (the level tag at the true moment equals the water level before the bracket,
and coincides elsewhere by value); the study carries four of six words of the committed call because it is the WHAT
(the alternatives, the bridge). Sweep 4: the study and the station description use ordinary words of the field
(record, standard, reading, channel) and name no move. Sweep 5: the prompt's question. No decisive vocabulary
(floodplain, overbank, bankfull, breakpoint, rating curve, segment) appears in any shipped file (asserted in checks.py).

## Guard

`guard.py check` on the re-registered card and `heart`: WARN (overuse.objective, overuse.gate_g, the lane's objective;
repeat.question_form against task482, the decision being a pick among the study's alternatives), every BLOCK of the
moved window redrawn (`## Draw`); structural tests differentiated on the card. `surface`: exit 0; the one "persona"
it lifted (Gage Period) is a table header in the station description.

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

## Rebuild (2026-10-23)

Reopened by the author's rule that no number stays retired and rebuilt from scratch in
physical-environmental-sciences / hydrology-flood-frequency (Forecasting), the cell the main session allocated,
worktree `b_178n`. Architecture 1 (the harbour trestle deck) and the conjoint cell stay spent; the card's identity
for architecture 1 moved into `lineage`. Architecture 2, the floodplain segment of the stage-discharge rating under
the annual peak series, was registered and committed DRAWN on 2026-10-23 (9bb65027) and built the same day to stage 3
green (checks 151 of 151, verifier 26 of 26, two byte-identical builds, precut and figures_check exit 0, leak.py
REVIEW answered, guard surface exit 0 and heart WARN); it waits at stage 4 for the main session's two scored readers
and the judge. The cell's other candidates are lines at the foot of `## Tried and rejected`. Stage 4 (pack cc9cb2f1):
the judge approved, both readers landed the call, and architecture 2 is spent at Gate F; the card's re-registration
(d4521939) is moot with the architecture spent, and the card is left as filed with `architecture_spent` set.

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
- **Rebuild cell, hydrology-flood-frequency (Forecasting), screened 2026-10-23 before the draw; the field's
  textbook routes (log-Pearson Type III or GEV on the annual maximum series, a regional skew, a trend term on the
  obvious covariate) taken as the default path.** The siblings' findings read first (task174 and task176 on main:
  forward conditions die to the attaining subset, an unidentified behaviour or a filed mechanic; a finer per-case
  file replays or reduces to one group-by), so the search went to a measurement or reconstruction step the
  textbook route takes for granted. Dead on paper, each at the draw:
  - daily-mean maxima against instantaneous peaks for pre-recorder years (a peak-to-daily ratio fitted on the
    overlap, Sangal's neighbouring-day form): the ratio touches only the early years and moves the 1 per cent flood
    10 to 15 per cent at most, a constant overlap ratio lands within a bin, and a ratio by season is one group-by;
  - the loop rating at the peak (Jones's correction): at the stage crest the rate of rise is zero, so the peak's
    rated discharge moves a few per cent at most on a flashy river, under any bin;
  - a fall rating against backwater from a downstream confluence: the default's error changes sign with
    coincidence (free-flow peaks under-rated, backwater peaks over-rated) and nets small and unforced;
  - naturalising a regulated record (inflow from outflow plus the storage change): an identity once the
    elevation-storage table is read, a replay;
  - a burned catchment's next floods: the neighbouring burned basins are the attaining subset and the response
    curve past their range forks;
  - urbanisation through a continuous simulation of each storm at the future impervious share: the trend term on
    the covariate is the default, the loss model's form forks, and the future share lies past the record's range;
  - stage-frequency under a channel aggrading at the gauge: the forward shift is an extrapolated trend whose form
    forks;
  - two gauged tributaries routed to an ungauged confluence: the routed combination is a replay once the lag is
    fitted, and the short downstream record's own fit differs from the long reconstruction only by sample;
  - a crest-stage era read as censored years (EMA with perception thresholds): task466's driver, spent;
  - mixed rain and snowmelt populations: the climate cell's mixed-population death (few events, the mixture fit's
    spread over any lever);
  - a construction-season maximum (the in-water work window): a reading of the window, ask material only.
  - Held and drawn: the rating's floodplain segment (`## Draw`), measured on code (p1 to p4) before the card.
- **Architecture 2, the floodplain segment of the stage-discharge rating under the annual peak series: spent at stage 4,
  Gate F (2026-10-23, pack cc9cb2f1).** The judge returned DETERMINISTIC / APPROVE with no fix, but both scored readers
  landed the call. Reader C filed Alternative D and 14,000 cfs and kept 32 of 32 ask figures. Reader D also filed D and
  14,000 cfs: "in-bank power law with a steeper overbank term above about 10.3 ft. It is stable across eras and fits within
  about 5 percent". For the asks it found the purge spikes, the 0.47 ft offset and the stale radar face ("the sensor face
  was surveyed at 199.84 ft in May 2023"). Why it died: a rating segmented at the bankfull break is the field's own
  standard practice (a control change read off the gaugings), and with 79 gaugings above 10.3 ft the break shows plainly,
  so a careful reader fits it by default; measurement 1 of the brief (a correction the field teaches as standard is the
  default path) applies to hydrometry as it did to the tide table. The ask devices (a visit-log clock, a logged controller
  offset, a resurveyed sensor face) are all 1.1e hygiene that careful readers execute. The card's re-registration
  (d4521939) is moot now; the card is left as filed, marked spent.
