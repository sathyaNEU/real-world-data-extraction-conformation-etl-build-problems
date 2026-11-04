# task489 design note

Architecture 1, drawn 2026-11-04. Data Extraction & Conformation (ETL), Physical & Environmental Sciences,
emissions-inventory. An Alberta gas producer's 2026 source-level inventory of its pneumatic controllers, and the
2027 zero-emission conversion list that inventory fixes.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task489.json`, registered 2026-11-04 and re-checked as filed:
  WARN only (overuse.domain, overuse.objective, repeat.question_form), the older same-puzzle note differentiated
  against task182 v1, task270 v4 and task465's draft. Nearest driver 0.06 (task462 v2). Brought up to the built pack
  at stage 3 (`## Duplicate check`).
- **Seed:** ET46 (comparable sales in a 53-week year), read through `status.py task489` only. Its world was set
  aside at the draw: the 53rd week, the shifted 4-5-4 calendar and the comparable-store rule are readings, and every
  analytical candidate screened in retail comparable sales either settled the WHAT (the store population) or repeated
  a spent driver (Tried and rejected). The number moved to another client domain under the same objective.
- **Pairing:** Physical & Environmental Sciences / emissions-inventory (ETL, DD in the taxonomy) / ETL. The call
  is decided by a conformed dataset: one row per pneumatic controller, built from five systems that never share a
  key, judged against the producer's reduction plan.
- **Which of the five ETL moves, and what the forcing file pins:** recover a per-case input a second file pins.
  The forcing files pin an **opportunity count**: how many times each separator's level band emptied in 2026. The
  plunger lift controllers' cycle history pins each well's arrivals, the closed daily allocations pin its liquid, and the
  equipment register pins each separator's bore and controller span. Reading them correctly is not sufficient: no
  field holds a dump count, and the count follows only from the physics of a snap-acting level controller under slug
  flow (a slug larger than the band empties it once however large; slugs much smaller than the band accumulate), so
  the deciding input is neither a filed column nor a count of shipped rows. It is not identity resolution (the well
  keys are Layer 1 and resolve exactly), not grain (the unit is the controller throughout) and not time semantics
  (every clock convention is closed and inert, asserted).
- **Shape:** other. Criteria from each of the 26 pads' 2026 intermittent-vent methane and its place against the
  plan's line, the list and each listed pad's figure on the deck, the chart, the 51 controllers' kilograms in the
  inventory, and the asks: 25 plunger wells' cycles without an arrival and 4 maker-area totals (`## Ask sheet`).
- **Decision:** designation_set: which well sites the 2027 zero-emission controller conversion covers, under the
  reduction plan's line (pads whose intermittent-vent controllers vented more than 0.5 tonnes of methane in 2026). Forward
  facing: the conversion is the 2027 capital programme; 2026 is the closed window that fixes it.
- **Strategy:** other (no family in the vocabulary names an opportunity count set by discrete arrivals against a
  buffer). Gap objective, decisive pattern G16 (the dump-count construction is selected per separator by what its
  data show), G14 second (the volume-over-band yield does not hold for slug-fed vessels), G19 depth. Gate G
  etl_conformance. Calibration organ physical_verification (the five dump counters, which confirm the volume rung).
- **Data-native sentence:** plunger lift wells deliver their liquid to the wellsite separator as one slug per
  plunger arrival while flowing wells deliver it continuously, so the number of times each separator's level band
  empties, which is what its controller vents on, is set by each well's slug against its own separator's band, and
  no system the producer runs records either the slug or the band.
- **Abstraction sentence** (what a reviewer holding this build and its nearest approved build would say is the same):
  none can be written. The nearest approved physical builds turn on a tank's gain between midnights (120), a valve's
  hours above its setting (162), sibling feeders' simultaneous tickets (303) and a wear curve restarted by
  replacement (132); none counts the emptyings of a buffer from the size of each arriving load against its band.
  The nearest pending build is task229 (`## Duplicate check`): its validation record also confirms the standard
  conversion only at steady input, but its step corrects a convex conversion of a continuous daily mean, while this
  one counts discrete events under saturation, one per load at most, so the sentence does not hold past its first
  clause.
- **WARN answers:** overuse.domain and overuse.objective: the number fixes ETL, and the only ETL task types whose
  structure is physical sit in this domain; emissions-inventory is outside the last three builds and source-level
  pneumatics is new to the corpus (no card or slot note mentions a plunger, a dump valve or a level controller).
  repeat.question_form (which, against task398) was answered at the draw; the final prompt asks where the conversion
  goes (question form where), and its second sentence opens on what the order rests on, not "Put".
- **Furniture:** forum executive_team (the conversion programme is the executive team's), forcing event
  purchase_order_or_contract (the conversion packages are ordered against their lead time, so the site list is fixed
  when the order is placed), org family other (an independent gas producer has no family of its own), stakeholder the
  producer's methane reduction lead (programme_officer). The forcing event was first carded as
  budget_or_appropriation and redrawn at the post-registration check, when task285 (registered ten minutes earlier)
  put that value in the window; the order is the honester label anyway, since the list must exist before the kits
  are bought, while the budget already holds the programme's line. None is banned against the last three builds.
  repeat.decision (designation_set, against task285): the call is a set of sites under a filed line, which no other
  decision type states honestly.
- **People** (drawn with `guard.py names --geo Canada`, seeds 489, 4891 and 48912): Kimberly Hinton, Stacy Frost,
  Valerie Sanders, Gregory Cook, Adam Hunter, Gloria Ward, David Thompson, Anthony Keller, Lisa Rollins, Brittany
  Welch, Joshua Castillo, Brandon Phillips, Stephanie Clements, Michael Espinoza, Jerry Davis, Todd Harrison, Donna
  Simpson, Laura Mendoza, Sherry Eaton. Invented names: Larchmere Resources Ltd. (the producer), Sheldrake Field
  Measurement Ltd. (the 2026 measurement contractor), Corrigan Controls, Aldous Valve and Instrument and Brannick
  Instrument (controller makers), Trellick Automation Ltd. (the plunger controller maker).
- **Sources** (all synthetic, generated by `generator/`, CC0 1.0, dated within the fiction; `metadata.json`):
  - `plunger_cycles_2026.csv` (the spine, 240,855 rows): every cycle the PCX-300 plunger controllers sent the SCADA
    host, received and opened in local time, with each unit's cycle and arrival counters.
  - `daily_well_volumes_2026.csv`: the closed daily allocations by UWI (hours, gas, condensate, water, run).
  - `scada_dump_counters_2026.csv`: hourly historian samples of the five automated separators' dump counters (UTC).
  - `deep_basin_equipment_register.xlsx`: pads, wells, vessels (bore, span, controller, SCADA flag), pneumatic devices.
  - `gas_analyses_2025_2026.csv`, `deep_basin_work_orders_2026.csv`.
  - Three makers' data sheets and the Trellick PCX-300 plunger controller specification (PDF).
  - `MRS-03_methane_measurement_and_reporting_standard_rev4.pdf`, `methane_reduction_plan_2027.docx` and
    `MRS-03_annex_B_source_inventory_template.xlsx` (the governing documents and the reporting form).
  - `sheldrake_pneumatic_survey_2026.pdf`: the spring 2026 survey (level controllers for an hour, bleed devices).
  - Distractors: `ogi_leak_survey_2026.csv`, `tank_vent_measurements_2026.xlsx` (MRS-05 and MRS-07, outside the
    pneumatic inventory by 4.5), `volumetric_adjustments_2026.csv` and `allocation_runs_2026.csv` (gas re-runs only).

## Default path

The pipeline a strong emissions engineer builds from the prompt's words, the standard and the files' grain, with
the field's own source-level method for an intermittent-vent controller in it (dump cycles times the maker's gas per
cycle):

1. Reads MRS-03 4.2: a level controller's methane is its 2026 dump cycles times its maker's rated supply gas per
   cycle, with the SCADA count where a pad counts them; 4.4 for the conversions; 3.3 for each pad's 2026 analysis.
2. Joins the register's Vessels sheet (bore, controller span, inlet well, SCADA flag) to its Wells sheet's UWIs and
   the daily allocations, the makers' sheets for gas per cycle, the gas analyses by surface location.
3. Counts the five automated separators' cycles from the historian's dump counters over the production days,
   unwrapping each 16-bit counter.
4. For every other separator, estimates its dump cycles the way a field engineer estimates a dump frequency: the
   2026 condensate and water it handled divided by the liquid between its controller's settings (the bore's area
   times the span). The five dump counters confirm this to within 1.8 per cent on every automated separator.
5. Sums each pad's intermittent-vent methane and takes the pads over the plan's 0.5 t line.

Ends on: 11 pads (the 8 golden pads with Elmworth 5-3, Elmworth 12-15 and Kakwa 8-10)
Golden: 8 pads (Elmworth 10-11, Elmworth 7-2, Kakwa 1-14, Kakwa 11-22, Kakwa 14-16, Kakwa 16-23, Kakwa 3-9, Kakwa 6-27)

## Stump sentence

The default path counts every unautomated separator's dumps as its 2026 liquid over its level band, which the five
dump counters confirm, and so files 11 pads, adding Elmworth 5-3, Elmworth 12-15 and Kakwa 8-10, whose plunger wells
lift slugs of 1.6 to 4.6 bands: each such slug empties the band in one dump however large it is, so those controllers
dumped once per arrival and the three pads vented 0.40, 0.37 and 0.24 t, under the plan's 0.5 t line.

## Three rules

- Task type: emissions-inventory (Physical & Environmental Sciences), which serves ETL: the conformed source-level
  inventory, one row per controller built from five systems that share no key, decides the conversion list.
- Domain test: the deciding quantity is each separator level controller's 2026 dump-cycle count, which a methane
  inventory estimates from the liquid each separator handled over the band between its controller's settings; the
  survey-average emission factor per device-hour is the older population route the standard has just retired.
- Swap: "convert every school whose boilers burned more than 0.5 t of gas" keeps the sentence and loses the task:
  a boiler has no level band, no plunger slug and no dump, so nothing in the count survives the swap.
- Layer 1: the SCADA host's cycle history in Mountain local time with the November repeated hour, against production
  days from 08:00; three keys (the allocations' UWIs, the register's and the host's well names, the historian's point
  tags); makers' sheets in scf at 60 F and psig, the standard in m3 at 15 C; bores and spans in inches; a 16-bit dump
  counter wrapping; outage re-sends; controller units moved between wells with the host label lagging; renumbered
  tags after re-pipes; replaced and relocated devices dated only in work orders; gas re-runs posted by journal. Each
  is what the producing system writes; none is placed to be caught, and none moves the call (R2, one assertion each).
- Layer 2: estimation that fits the data (field_method): the dump-frequency estimate assumes liquid reaches the
  separator continuously, and on plunger wells it arrives as one slug per plunger arrival.
- Decisive step: recognising that a snap-acting controller cannot dump more than once per slug, so where a plunger
  well's slug (its production day's liquid over that day's arrivals) is larger than its separator's band the count is
  its arrivals, and where the slug is a small fraction of the band the slugs accumulate and the count follows the band.
- Not semantics: every field is read right on the default path (two-phase separators, condensate and water, UTC
  counters, production days, units); the wrong answer comes from an estimate whose precondition (continuous inflow)
  the plunger wells break, which no field, code, unit or definition states.
- Not rule application: MRS-03 4.2 files the quantity (dump cycles times rated gas) and no rule says how to count an
  uncounted separator's cycles. The enumerated family a competent engineer reaches for files 8 to 18 pads (volume
  over band 11, one dump per arrival 11, the larger of the two 14, the survey rate times hours 18, the level replay
  8); the standing family once each day's slug is set against its band (the replay, the per-day minimum of arrivals
  and volume over band, the per-day ceiling, volume over band for the small-slug wells only) files one set, 8 pads,
  every pad within 0.0003 t across it. The ruling-out is silent: no sentence compares a well's arrivals with its
  liquid, and no column holds a slug or a band.
- Analyst test: a strong analyst who conforms every file and applies every filed rule counts dumps as liquid over band
  (counters where fitted), sees the five counters agree to within 1.8 per cent, and files 11 pads, Elmworth 5-3,
  Elmworth 12-15 and Kakwa 8-10 among them, wrong; checks.py R3a runs it on the clean truth.
- Estimand: the plan's section 3 files the population (pads whose intermittent-vent controllers vented more than
  0.5 t of methane in 2026 as reported under MRS-03) and MRS-03 files the outcome (each source's methane vented, 4.1),
  the window (production days 1 January to 31 December, 3.2), the unit (kg per source, t per pad, 5.2) and the
  conversions (4.4).
- No decoy: nothing is planted: no memo, draft or stakeholder figure argues for a pad; the survey's mean vent rate is
  the contractor's own statistic of what it measured, and the dump counters are true counts on the separators that
  have them, all five of which take flowing wells.
- No certified replay: no certified or published figure is reproduced to recover a method; the counters validate the
  volume route honestly where it is right, and the golden comes from the controller's documented snap action.
- Lesson: a frequency estimate built on volume over capacity assumes continuous arrival; when the input arrives in
  discrete loads, the count is set by each load against the capacity, one event per load above it and one per
  capacity below it. No build on file counts discrete emptyings of a buffer from the size of its arriving loads.

## Survivor anatomy

- Actor: the deciding property is each plunger well's slug against its own separator's band, which no file stores:
  the slug is a relation between the daily allocations and the cycle history's arrivals, the band one between two
  register columns, and their comparison sits in neither.
- Link: wells reach separators only through the register's well names, the cycle history carries controller serials
  and the host's labels, and the allocations carry UWIs; nothing invites comparing a well's arrivals with its volumes.
- Reflex: the field's method for an uncounted dump frequency (liquid over the band) is rung 1 and files 11 pads; the
  survey's mean rate per device-hour, the retired population route, is rung 0 and files 18.
- Back-test: the five dump counters confirm the volume route to within 1.8 per cent on every automated separator,
  because all five take flowing wells, where the volume route is right.
- Second use: the cycle history carries the plunger wells' own record (the ask on cycles without an arrival); the
  allocations carry every well's volumes; the register and the makers' sheets carry every device for both asks.
- Shock: the three big-slug pads' plunger wells look like any other plunger wells (plunger types, controller models,
  bores and spans shared with the small-slug wells, both areas on each side), and no sort of any shipped statistic
  gives the golden set.
- Pins: the WHAT sits in the plan (the population and the line) and MRS-03 (outcome, window, unit, constants); no
  sentence names slugs, bands, arrivals or how an uncounted dump frequency is estimated.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| Rung 0: survey mean rate times 8,760 h | the survey's summary line | none | the old population route | none | no | one product | the survey has its own bleed use | readable |
| Rung 1: liquid over band (counters where fitted) | MRS-03 4.2 names dump cycles | register bore and span | the field's dump-frequency estimate | the counters confirm it | no | one divide | no | readable |
| Rung 1b: one dump per plunger arrival | none | ARRIVE rows | a natural plunger reading | none | no | one count | no | readable |
| Rung 2 (decisive): each slug against its band | none | no column holds a slug or a band | no | the counters are blind to it (flowing wells only) | no | a minimum over arrivals, day by day | the cycle history serves the non-arrival ask | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "pads" | the register's Pads, one reporting facility each | the reporting facility | same call | same call |
| SF2 | "more than 0.5 tonnes" | strictly above | at or above | same call | same call (no pad within 0.05 t of the line) |
| SF3 | "2026" | production days from 08:00, MRS-03 3.2 | local or UTC calendar days | same call | MRS-03 3.2; same call asserted |
| SF4 | gas per dump cycle | the maker's rating, MRS-03 4.2 | the survey's measured per cycle | same call | MRS-03 4.2; same call |
| SF5 | methane fraction | the 2026 analysis, MRS-03 3.3 | 2025, or the mean of both | same call | MRS-03 3.3; same call |
| SF6 | scf to m3 | 0.02826, MRS-03 4.4 | 0.0283168 | same call | MRS-03 4.4; same call |
| SF7 | automated separators | counted cycles, MRS-03 4.2 | liquid over band | same call | MRS-03 4.2; same call |
| SF8 | a cycle | each once by serial and cycle count | every row the host loaded | same call | same call |
| SF9 | which well a cycle is on | the unit's well by the work orders | the host's label | same call | same call |
| SF10 | the slug | each production day's liquid over its arrivals | the year's mean slug | same call | same call |
| SF11 | the level at the year's start | empty | full | same call | same call |
| SF12 | the liquid a two-phase separator dumps | condensate and water | condensate only | 1 pad | the register's "Wellsite separator, two-phase" |
| SF13 | when the controller dumps | at the upper setting | only above it | same call | same call |
| SF14 | a cycle's production day | by valve open | by arrival | same call | same call |
| SF15 | intermittent-vent controllers | the register's level controllers | with the plunger controllers | same call | MRS-03 2.2 and the register's Vent class column |

## Ladder

Each pad's 2026 intermittent-vent methane (t) on the clean truth, for every pad any of the three middle routes puts
over the line (`checks.py` asserts every margin):

| Pad | Golden | Rung 1: liquid over band | Rung 1b: one dump per arrival | Rung 0: survey rate x 8,760 h |
|---|---|---|---|---|
| Kakwa 3-9 | 0.95 | 0.95 | 0.95 | 0.44 |
| Kakwa 11-22 | 0.86 | 0.86 | 0.86 | 0.44 |
| Kakwa 14-16 | 0.75 | 0.75 | 0.75 | 0.86 |
| Kakwa 6-27 | 0.74 | 0.74 | 0.74 | 0.87 |
| Elmworth 10-11 | 0.71 | 0.79 | 0.71 | 0.88 |
| Kakwa 16-23 | 0.70 | 0.70 | 0.83 | 1.34 |
| Elmworth 7-2 | 0.64 | 0.78 | 0.64 | 0.86 |
| Kakwa 1-14 | 0.62 | 0.62 | 0.70 | 0.85 |
| Elmworth 5-3 | 0.40 | 0.64 | 0.40 | 1.24 |
| Elmworth 12-15 | 0.37 | 0.57 | 0.37 | 0.82 |
| Elmworth 9-34 | 0.36 | 0.36 | 0.62 | 0.84 |
| Kakwa 13-22 | 0.31 | 0.31 | 0.64 | 1.28 |
| Kakwa 8-10 | 0.24 | 0.70 | 0.24 | 1.26 |
| Elmworth 4-27 | 0.02 | 0.02 | 0.63 | 1.30 |

- Rung 0 (18 pads, Kakwa 3-9 and Kakwa 11-22 out): the survey's 3.03 scf per controller-hour for every hour; dies to
  MRS-03 4.2, which counts dump cycles.
- Rung 1, the default path (11 pads): adds the big-slug pads; dies to the cycle history, where their slugs exceed
  their bands every producing day (1.5 bands or more, asserted).
- Rung 1b (11 pads): adds the small-slug pads Elmworth 9-34, Kakwa 13-22 and Elmworth 4-27; dies to the same
  comparison, their slugs under 0.07 of a band.
- Rung 1c, the larger of the two (14 pads); condensate only (1 pad), a reading ruled out at SF12.
- Rung 2, decisive (8 pads): the slug against the band, every execution agreeing (R3b).
- Margins: the lowest pad in 0.62 t (Kakwa 1-14), the highest out 0.41 t (Elmworth 14-24); each flipped pad 1.5 times
  or more higher under its route than under the golden; every route's added pads 0.57 t or more on that route.
  Position: the golden set is no interval of any sort.
- Pricing: the step is worth 0.20 to 0.46 t on each big-slug pad and 0.26 to 0.61 t on each small-slug pad, against
  a standing-family spread of 0.0003 t at most (bins asserted); the counting input is per separator and per day,
  never one scalar.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | pads whose intermittent-vent controllers vented more than 0.5 t in 2026 | plan section 3; C1 |
| 2 | Unit of account | the pad; the source for kg | plan section 3, MRS-03 5.2 |
| 3 | Attribution window | production days 2026 | MRS-03 3.2; SF3 C1 |
| 4 | As-of dating | the register and work orders at the January 2027 export | C1, every stint dated |
| 5 | Version basis | the reporting year's analysis, the makers' current sheets | MRS-03 3.3; SF5 C1 |
| 6 | Denominator | none | n/a, no rate graded |
| 7 | Weighting | none | n/a |
| 8 | Window length | the year | MRS-03 3.1 |
| 9 | Boundary inclusivity | more than 0.5 t | SF2 C1, nothing within 0.05 t |
| 10 | Rounding path | kg per source, t per pad from unrounded kg | prompt; bins asserted |
| 11 | Tie-break | none needed | C1, no two pads share a figure |
| 12 | Maturity and censoring | the year closed at the export | C1 |
| 13 | Order of operations | cycles, then gas, then methane | C1, the products commute |
| 14 | Row order | the host's receipt order | C1, counts are order-free |
| 15 | Duplicate resolution | each cycle once by serial and cycle count | SF8 C1 for the call; ask device |
| 16 | Identity normalisation | UWI, well name, point tag | the register's Wells and Vessels sheets; C4 |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | scf at 60 F to m3 at 15 C; inches to metres | MRS-03 4.4; SF6 C1 |
| 19 | Code and status semantics | ARRIVE and NO ARRIVAL; two-phase | SF12; the PCX-300 specification's counters |
| 20 | Integerisation | whole cycles on counted and replayed separators | C1 |
| 21 | Clause scope | 4.2 for level controllers, 4.3 for bleed | MRS-03 2.2, 2.3 |
| 22 | Forward window contents | the conversion order's list | plan section 3 |

## Literal reader

Executed word for word, the plan's section 3 and MRS-03 4.2 ask for each controller's 2026 dump cycles times its
rated gas; the only literal question left is how many cycles an uncounted separator made, and every reading that
takes the controller's documented snap action (open at the upper setting, close at the lower) against the cycle
history's arrivals and the allocations gives 8 pads (SF3 to SF14 converge); the volume route is an estimate whose
continuous-inflow assumption the plunger wells break, not another reading of a sentence.

## Oracles

- The dump counters confirm the volume route within 1.8 per cent on their five separators, all on flowing wells: true
  where taken, blind to slugs because no counted separator takes a plunger well, and they never tie only under the
  golden.
- The survey confirms the makers' gas per cycle within 4 per cent; its mean rate per hour is the contractor's own
  statistic and ranks nothing.
- No control, total or published figure ties only under the golden.

## Ask sheet

Planning weights 38 / 7 / 55. The call's own construction (each controller's kg, each pad's tonnes, the list) is
scored with it. The asks sit on rows the call never reads.

- **Ask P, each plunger lift well's 2026 cycles that ended without the plunger arriving (25 figures).** H18 home: the
  plunger wells' own record in the inventory workbook, a measure every plunger well carries and the call does not
  turn on. Path: the cycle history (controller_sn, well, cycle_count, arrival_count, valve_open_local, result), the
  PCX-300 specification's counter registers, the work orders' controller moves. Primary 1 (D4, absence in the
  record's own counters): openings the controller closed again on its line pressure interlock are counted and never
  sent to the host, so every well's logged non-arrivals fall short by its aborted openings; the reconstruction is the
  rise in cycle count less the rise in arrival count. Primary 2 (D7, the true key elsewhere): four controller units
  moved between small-slug plunger wells ran for days under their old well's host label; the serial and the work
  order's time place them. Hazards: outage re-sends (the same rows loaded twice with later receipt times), the
  November repeated hour, the 08:00 production day. Pin test: the asking sentence pins the wells, the year and the
  unit (cycles); no pin names a counter, an interlock or a label.
- **Ask B, the sales gas pressure controllers' 2026 methane for each maker in each area (4 figures).** H18 home: the
  2028 instrument air programme's measured baseline (plan section 4). Path: the register's Pneumatic devices sheet,
  the survey's bleed table (pad, tag, model, reading), the work orders (replacements, isolations), the makers'
  ratings, the analyses. Primary (D7, codes reissued to other entities): two re-piped pads' pressure controllers were
  renumbered in the register after the survey, so the survey's tag points at the other device and only the model on
  the survey date finds the measured one. Hazards: two replaced controllers dated in the work orders, two pads
  depressured, two relocated heater controllers. Pin test: MRS-03 4.3 files the rate basis and the hours; nothing
  names the renumbering.
- **Main population zero-counts:** no outage re-send sits on a big-slug well's rows and no moved controller ran a
  big-slug well (asserted); the bleed devices are outside the intermittent-vent population.
- **The full includer:** a response that reconstructs the counters and the units keeps ask P, and one that joins the
  survey by model on its date keeps ask B; each remedy is a reconstruction across two systems, not a filed rule.
- **Referee:** none; every ask figure is recomputed on `generator/verify.py`'s own path.

| Ask figure | Cracker (logged non-arrivals once by host label; survey by pad and tag) | Golden | Cracker |
|---|---|---|---|
| P: LRL ELMWORTH 10-11 #2 | 167 | 261 | miss |
| P: LRL ELMWORTH 10-32 #1 | 415 | 520 | miss |
| P: LRL ELMWORTH 10-32 #2 | 166 | 295 | miss |
| P: LRL ELMWORTH 12-15 #2 | 168 | 305 | miss |
| P: LRL ELMWORTH 3-29 #1 | 152 | 326 | miss |
| P: LRL ELMWORTH 4-27 #1 | 714 | 920 | miss |
| P: LRL ELMWORTH 4-27 #2 | 1006 | 1236 | miss |
| P: LRL ELMWORTH 4-27 #3 | 1283 | 1856 | miss |
| P: LRL ELMWORTH 5-3 #2 | 442 | 571 | miss |
| P: LRL ELMWORTH 5-3 #3 | 133 | 267 | miss |
| P: LRL ELMWORTH 7-18 #2 | 413 | 643 | miss |
| P: LRL ELMWORTH 7-18 #3 | 617 | 834 | miss |
| P: LRL ELMWORTH 7-2 #2 | 594 | 813 | miss |
| P: LRL ELMWORTH 9-34 #2 | 633 | 923 | miss |
| P: LRL KAKWA 1-14 #2 | 244 | 407 | miss |
| P: LRL KAKWA 12-36 #1 | 280 | 713 | miss |
| P: LRL KAKWA 12-36 #2 | 665 | 982 | miss |
| P: LRL KAKWA 13-22 #2 | 908 | 1310 | miss |
| P: LRL KAKWA 13-22 #3 | 256 | 581 | miss |
| P: LRL KAKWA 16-23 #2 | 469 | 696 | miss |
| P: LRL KAKWA 16-23 #3 | 354 | 583 | miss |
| P: LRL KAKWA 8-10 #1 | 612 | 744 | miss |
| P: LRL KAKWA 8-10 #2 | 118 | 214 | miss |
| P: LRL KAKWA 8-10 #3 | 465 | 880 | miss |
| P: LRL KAKWA 8-35 #1 | 275 | 331 | miss |
| B: Aldous Valve and Instrument, Elmworth (kg) | 409 | 518 | miss |
| B: Aldous Valve and Instrument, Kakwa (kg) | 276 | 256 | miss |
| B: Corrigan Controls, Elmworth (kg) | 513 | 380 | miss |
| B: Corrigan Controls, Kakwa (kg) | 383 | 427 | miss |

Pair ceiling: 39.9 (the cracker 45.0: the call landed and no ask figure kept; the mirror 34.8 at rung 1, 57 of 78 call
criteria and no ask figure)
Mirror leakage: 0.0 per cent of ask weight
Measured by: generator/ceiling.py, on the cut pack of this build (the table above is its output)

## Leak review

`leak.py task489 --asof 2027-01-25` on the final cut: REVIEW (exit 1), no LEAK; sweeps 1, 2, 5 to 9 and 11 clean,
sweep 10 INFO (no writer signature). Each REVIEW line, ruled here:

- Sweep 3, the register and the work orders: the six-digit "figures" are the level controllers' tag numbers (the
  LC-141601 of Kakwa 14-16's first separator), which the write-up names beside each controller's kilograms. They are
  identifiers the register issues, not computed answers. Harmless.
- Sweep 3, the survey: 0.35, 0.28, 0.62, 0.31 and 0.32 are bleed rates and ratings in scf/h, and 0.00 is a test hour
  with no dump; each coincides with a pad's tonnes or a controller's figure only as digits. Harmless. The first cut
  listed the tested level controllers by register tag, which leak.py read as LEAK (the tag digits are on the
  write-up's controller lines); the survey now names each tested separator by the well it takes, as a field crew
  records it, and nothing graded moved.
- Sweep 3, the makers' sheets: 0.62 scf per cycle and the bleed ratings 0.35 and 0.28 scf/h are the makers' published
  figures, inputs the method needs. Harmless.
- Sweep 3, the plan: 0.5 is the plan's own line, the filed WHAT. Harmless.
- Sweep 3, MRS-03 and the PCX-300 specification: 101 is in 101.325 kPa and 295 in the 32-bit rollover
  4,294,967,295. Harmless.
- Sweep 3, the call's words in MRS-03 and the survey: both name separators, level controllers and the two areas'
  pads, as their genres do; neither lists, ranks or scores pads for the conversion. Harmless.
- Sweep 4, MRS-03 (separator, survey, liquid, allocations, volume, register): the standard defines a dump cycle,
  files the quantity and lists the records kept; it names no slug, band or arrival and no way to count an uncounted
  separator (checks.py asserts the absence). Harmless.
- Sweep 4, the survey (separator, survey, volume): its method section and results; it describes no separator's
  inflow. Harmless.
- Sweep 4, the PCX-300 specification (counters, arrivals, register): the maker's register map for the controller's
  cycle and arrival counters, which ask P reads; it says nothing about separators or liquid. Harmless.
- Sweep 12, MRS-03 naming Kakwa, Reporting year, Tank and well: ordinary words of the operator's own standard
  (its scope, 3.1 and 4.5), not a description of any file's columns. Harmless.
- Single-use test: every file the decisive step reads has another use (the cycle history carries ask P, the
  allocations every route, the register and the makers' sheets both asks, the counters MRS-03 4.2's counted cycles).

## Duplicate check

- `guard.py check` on the final card: WARN (people.first, overuse.domain, overuse.objective, repeat.decision against
  task285, registered after this draw). A people.inside BLOCK (two personas named Kimberly) was cleared by replacing
  the allocation run log's second user with Adam Hunter from the same draw.
- `guard.py heart task489`: WARN, nearest driver 0.06 (task462 v2), test.same_puzzle_older a NOTE differentiated on
  the card against task182 v1, task270 v4 and task465's draft.
- `guard.py surface task489`, re-read after the final pull: five pairs promoted, all on card axes or the corpus
  surface percentile; the only shared-text hit (a work-order export named as task487's) was renamed to
  `deep_basin_work_orders_2026.csv`. For the author's adjudication:
  - task488 (back to back; gap objective and designation_set): task488 traces a recalled batch through always-full
    conduits by the volume drawn downstream of each segment (G13, a population of sections); here a count of discrete
    emptyings is rebuilt from each arriving load against its own vessel's band (G16), and nothing is traced.
  - task487 (two apart; the same domain and objective, an operations log): task487 prices release events an
    inspection itself starts, read from incidence against window length (censoring); here no event is found at a
    visit and no window is priced: every dump is set by slug against band.
  - task229 (the calibration form physical_verification): both validation records confirm the easy route only where
    the input is steady, which is the nearest abstraction on file. task229 corrects a convex rating applied to a daily
    mean for the river's swing inside each day (a continuous quantity, a Jensen bias, read from sub-daily levels);
    here the count is a saturation of discrete loads, one dump per slug at most and one per band of accumulated
    slugs, read per production day from two systems that share no key. Flagged for the reader and the clone check.
  - task182 (gap, pattern and decision family against its dead v1): differentiated on the card at the draw.
  - task240 (surface percentile and designation_set): task240 judges which survey estimates carry a reliability
    warning from their sampling error under post-stratified weights; nothing here is sampled or weighted, and the
    set is decided by a physical count against a filed line.
- People in the cut pack: guard reads "Red Deer" as a persona; it is the Alberta city in Brannick's address.

## Tried and rejected

- 2026-11-04, draw: seed ET46's own pitfalls (the 53rd week, the shifted 4-5-4 calendar, the comparable-store
  rule). Rejected: each flips the answer only on reading a calendar or a definition correctly (data semantics or rule
  application), banned as the decisive step.
- 2026-11-04, draw, retail comparable sales: stores made non-comparable by a sibling's refurbishment (transferred
  sales), cannibalisation by new stores, pipeline fill at launches, sell-in against sell-through, DSD replenishment
  re-timed by delivery interval, weather-normalised comps. Rejected: each either settles the WHAT (which stores or
  which sales the comparable figure counts, so filing it is rule application and not filing it is a fork) or repeats
  a spent driver (calendarisation from a daily sample, task123; trading-day exposure, task477; stockpiling in a price
  index, task463; returns arriving late, the maturity family).
- 2026-11-04, draw, official time-series production in retail (an industry like-for-like index from members'
  returns): calendarisation, late returners, matched-sample chaining. Rejected: spent drivers (task123, task445,
  task451) or the field's own method as the golden (chain-linking, Denton, regARIMA).
- 2026-11-04, draw, emissions-inventory: refrigerant top-ups re-timed to leak periods across the year boundary.
  Rejected: task270's architecture 7 spent it (each pack's charge short at the year ends).
- 2026-11-04, draw, emissions-inventory: pneumatic chemical injection pumps venting per stroke, strokes read from
  the chemical vendor's delivery tickets. Rejected: matching the exposure to the mechanism (gallons pumped, not
  device-hours) is the practitioner's first move, which `stumping` 1.1b records as landed eleven times in twelve.
  The same objection removes the per-dump count as a decisive step; it is rung 1 here, and the decisive step is the
  precondition plunger slugs violate.
- 2026-11-04, draw, emissions-inventory and data integration: grain silo funnel flow (core-first withdrawal) and
  reefer containers on board at berth from crane move sequences. Rejected: both trace inputs to outputs by a
  physical withdrawal order, the abstraction task488 holds (and the reefer case sits beside task476's screens S3.6
  and S3.7 on at-berth load).
- 2026-11-04, draw, water audit (customer meter under-registration by flow profile) and district metered area
  breaches. Rejected: the first is unidentifiable without a second measurement of the meters' low flows, the second is
  topology from series (task461 v3), and every water utility's organisation family is banned in the window.
- 2026-11-04, design, ask on each pad's 2026 gas produced (the allocations with the re-runs' journal). Dropped
  before the cut: the careful route sums the allocations and posts each journal line to its run's production month,
  which is the whole remedy, so its 26 figures carried no device after the notice (supplemental 1.0); the journal and
  the run log stay as distractors.
- 2026-11-04, build, ask B over every continuous-bleed controller, the heater temperature controllers included. The
  bundle-side ceiling found the careful route keeping both Brannick totals, because the relocated heater controllers
  carry their survey readings by serial; ask B narrowed to the sales gas pressure controllers.
- 2026-11-04, build, first vessel layouts: the big-slug wells on the small bores and short spans, and every big-slug
  pad in Elmworth. checks.py's no-partition assertions caught both (a bore, a span or an area sorted the flipped
  pads); bores, spans and models now overlap and four pads sit in the other area.
- 2026-11-04, build, Kakwa 16-23's counted separator on a CL-200 passing 65,536 dumps in the year: the last reading
  less the first, modulo the counter, then gives 1,414 cycles and drops the pad, so a Layer 1 wrap could move the
  call (R2). The controller is an SV-40, every counter stays inside one turn a year, and R2 asserts every reading of
  the wrap.

