# task489 design note

Architecture 1, drawn 2026-11-04. Data Extraction & Conformation (ETL), Physical & Environmental Sciences,
emissions-inventory. An Alberta gas producer's 2026 source-level inventory of its pneumatic controllers, and the
2027 zero-emission conversion list that inventory fixes.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task489.json`, registered 2026-11-04 and re-checked as filed:
  WARN only (overuse.domain, overuse.objective, repeat.question_form), the older same-puzzle note differentiated
  against task182 v1, task270 v4 and task465's draft. Nearest driver 0.06 (task462 v2).
- **Seed:** ET46 (comparable sales in a 53-week year), read through `status.py task489` only. Its world was set
  aside at the draw: the 53rd week, the shifted 4-5-4 calendar and the comparable-store rule are readings, and every
  analytical candidate screened in retail comparable sales either settled the WHAT (the store population) or repeated
  a spent driver (Tried and rejected). The number moved to another client domain under the same objective.
- **Pairing:** Physical & Environmental Sciences / emissions-inventory (ETL, DD in the taxonomy) / ETL. The call
  is decided by a conformed dataset: one row per pneumatic controller, built from five systems that never share a
  key, judged against the producer's reduction plan.
- **Which of the five ETL moves, and what the forcing file pins:** recover a per-case input a second file pins.
  The forcing files pin an **opportunity count**: how many times each separator's level band emptied in 2026. The
  plunger lift controllers' event logs pin each well's arrivals, the closed daily allocations pin its liquid, and the
  equipment register pins each separator's bore and controller span. Reading them correctly is not sufficient: no
  field holds a dump count, and the count follows only from the physics of a snap-acting level controller under slug
  flow (a slug larger than the band empties it once however large; slugs much smaller than the band accumulate), so
  the deciding input is neither a filed column nor a count of shipped rows. It is not identity resolution (the well
  keys are Layer 1 and resolve exactly), not grain (the unit is the controller throughout) and not time semantics
  (every clock convention is closed and inert, asserted).
- **Shape:** other. Criteria from each site's 2026 controller methane and its in-or-out verdict against the plan's
  line (about 26 sites, two criteria each), the list, its count and its total, the per-controller CSV's columns, the
  chart's named parts and the two files; the ask figures add per-well arrivals, the bleed devices and the counters.
  Sized in `## Ask sheet` once the world is fixed.
- **Decision:** designation_set: which well sites the 2027 zero-emission controller conversion covers, under the
  reduction plan's line (sites whose pneumatic controllers vented more than 0.5 tonnes of methane in 2026). Forward
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
- **WARN answers:** overuse.domain and overuse.objective: the number fixes ETL, and the only ETL task types whose
  structure is physical sit in this domain; emissions-inventory is outside the last three builds and source-level
  pneumatics is new to the corpus (no card or slot note mentions a plunger, a dump valve or a level controller).
  repeat.question_form (which, against task398): the decision is a pick of sites, which asks which; the role
  sequence is redrawn instead (the second sentence opens on the deliverable's use, not "Put").
- **Furniture:** forum executive_team (the 2027 capital budget is the executive team's), forcing event
  budget_or_appropriation, org family other (an independent gas producer has no family of its own), stakeholder the
  producer's methane reduction lead (programme_officer). None is banned against the last three builds.
- **People** (drawn with `guard.py names --geo Canada`, seeds 489 and 4891): Kimberly Hinton, Stacy Frost, Valerie
  Sanders, Gregory Cook. Invented names: Larchmere Resources Ltd. (the producer), Sheldrake Field Measurement Ltd.
  (the 2026 measurement contractor), Corrigan Controls, Aldous Valve and Instrument and Brannick Instrument
  (controller makers).
- **Sources** (all synthetic, generated by `generator/`, CC0 1.0, dated within the fiction):
  - `plunger_events_2026.csv`: every event the wellsite plunger lift controllers logged in 2026 (the spine).
  - `production_daily_2026.csv`: the closed daily allocations by well (gas, condensate, water).
  - `equipment_register.xlsx`: sites, wells, separators (bore, controller span), every pneumatic device.
  - Controller data sheets (PDF), one per maker: supply gas per dump cycle, steady bleed.
  - `gas_analyses_2026.csv`: each site's laboratory gas analyses.
  - `dump_counters_2026.csv`: the SCADA dump counters on the five automated separators.
  - The producer's methane reporting standard and its 2027 reduction plan (PDF, DOCX).
  - The 2026 measurement campaign report (PDF).
  - Work orders for 2026 (CSV).
  - Distractors: the 2026 optical gas imaging survey and the storage tank vent measurements.

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
