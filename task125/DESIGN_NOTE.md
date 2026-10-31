# task125 design note (architecture 3, the Umzimela sulfate loads)

Architecture 1 (Wealdmoor County Council's digit filter) and architecture 2 (Merrowland Statistics' Household Labour
Survey) are spent and in the card's lineage; their measured deaths are in `## Tried and rejected`. Architecture 3 draws
a new domain, world and dataset.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task125.json`, architecture v3, registered 2026-10-31 after `guard.py
  recent`, `coverage`, `mechanisms --objective anomaly-detection` and `slots` on the mechanism's words (mixing, mixing
  zone, confluence, mass balance, plume) and the setting's (sulfate, sulphate, acid mine, dissolved oxygen, diurnal,
  grab sample, sonde, lightning, arrester, vegetation, trim cycle). `check` WARN only: `overuse.org_family`
  (government_agency is the honest kind for a catchment management agency) and `repeat.decision` against task181 v6
  (the call is which resource units are over their allocations, a designation by nature; the answer unit differs in
  kind, units of a river against consultants). The two older structural matches are differentiated on the card
  (task84, task257, task269).
- **Pairing:** Physical & Environmental Sciences, task type environmental-monitoring-exceedance, objective Anomaly
  Detection & Diagnostics: which resource units of a coal-mining catchment carried more sulfate past their boundaries
  in the 2025/26 dry season than their load allocations allow, the units whose mines the Governing Board directs in
  2027.
- **Shape:** other (a designation against filed allocations: each resource unit's dry-season load and verdict, with
  the asks' per-site, per-gauge and per-discharge grids supplying the rest of the criteria). Scorecard shape 10 is
  barred against task181 by the guard's two-build window, and the structure is honestly a designation with
  per-unit loads rather than a scorecard of indicators.
- **Strategy:** `composition_mix`. The water a boundary monitor samples a few kilometres below a mine stream's
  confluence is a different blend of the two inflows than the whole river carries past the boundary, so the point's
  concentration is the bank's mix, not the section's. Gate G `method_or_model_selection` (two ways to put a load on
  the boundary, the boundary sample times the boundary flow or the inflows' loads carried down, the right one forced
  by conservation in the record); gap objective then population; generators G2 (the point against the section), G5
  (the load is measured where each inflow is mixed, upstream), G3.
- **Data-native sentence:** the agency's boundary monitors stand at gauging weirs chosen for bridge access, two to
  four kilometres below the confluences of the mine streams, where a stream's water still runs along the bank it
  entered on, so on every run the near-bank monitor samples the mine stream's water and the far-bank monitor the
  main river's, while each inflow's own monitor upstream samples water that is already mixed.
- **Abstraction sentence** (what a reviewer holding this build and its nearest approved build would say is the same):
  none writable. The nearest drivers on file score 0.07 and under; task263 (a source's level recovered from blends
  of sources running together) is the inverse move, a blend's level recovered from sources, and task120 (a draw read
  as inflow less storage gained) closes a balance over a stock in time rather than over a river's inflows in space.
- **Sources:** synthetic throughout. The world (the Umzimela Catchment Management Agency, its rivers, gauges, monitors,
  mines and people) is fictional and modelled on how South African catchment agencies, the national gauging network
  and coal-mine water use licences work; personas from `guard.py names --locale zu_ZA --seed 125`.

## Default path

1. Read the allocation schedule: a resource unit is over its allocation when the sulfate its water carries past its
   lower boundary on the days of the routine runs from 1 May to 30 September, averaged over those runs, exceeds
   Table 2 (section 3).
2. Conform the laboratory's sulfate (a re-run, suffix -R, replaces the first result) and the gauging network's daily
   mean flows, and take the dry season's eleven routine runs.
3. Put a load on every unit on every run the way load at a compliance point is computed: the boundary monitor's
   sulfate times the boundary weir's mean flow that day times 0.0864, and average the runs.
4. Compare each mean with Table 2 and flag the units above it.

Ends on: KH1, MZ2, NT1 and NY3 over their allocations (MZ2 at 36 t/d against 32, NY3 at 67 against 58), MZ4 and
NY2 within theirs (31 against 34, 30 against 35).
Golden: KH1, MZ4, NT1 and NY2 over their allocations (MZ4 at 40 t/d, NY2 at 40), MZ2 and NY3 within (27 and 52).

## Stump sentence

The default path puts each unit's load on its boundary monitor's sample times the boundary flow and files KH1, MZ2,
NT1 and NY3 over their allocations; the step that lands it there is taking the boundary sample for the unit's water,
when four boundary weirs stand two to three kilometres below a mine stream's confluence, inside the reach where the
stream still runs along the bank it entered on, so Esikhotheni and Siphethu sample the mine stream's plume and
Ngwelezane Drift and Mabhokweni the main river's water, and each of those units carries what its inflows bring in.

## Three rules

Task type: environmental-monitoring-exceedance in Physical & Environmental Sciences, which serves Anomaly Detection & Diagnostics: which reaches of a mining catchment are carrying more of a pollutant than their allocations allow.
Domain test: the deciding quantity is each resource unit's sulfate flux past its lower boundary, which river water-quality practice reads as a representative, fully mixed concentration times the gauged flow; whether a sample is representative turns on the lateral mixing of a tributary into a river over kilometres below a confluence, river hydraulics with no meaning once the nouns are a hospital's or a school's.
Swap: "which wards carried more infections than their allocations allow" has no confluence, no channel width across which two inflows run side by side for kilometres and no conserved substance carried down a network of reaches, so the comparison of a point sample with what the inflows bring in stops making sense.
Layer 1: the laboratory's long export one row per analyte with re-runs under a suffixed sample number (the laboratory system), EC in mS/m at the laboratory against uS/cm in the field log (two instruments), the loggers' UTC telemetry timestamps against SAST field sheets (the telemetry server), month-end totaliser readings rather than volumes and one totaliser replaced in February (the mines' returns), a resubmitted return (the licence process), below-detection metals written as <0.05 (the laboratory), sulfate written sulphate in the mines' returns; each is what the producing system does and none decides the call.
Layer 2: estimation_fit, the data's real structure: the boundary samples at four weirs are not samples of their units' mixed water, and the choice that flips the call is reading each of those units' load from what its inflows carry in, measured where each inflow is mixed, instead of from the boundary sample.
Decisive step: recognising that a monitor a few kilometres below a confluence sits in the lateral mixing zone, so its sample is one bank's blend of the two inflows, and putting the unit's load on the conserved sum of its inflows' loads, confirmed by the mixed weir downstream.
Not semantics: every field, unit and code read correctly (the re-runs, mg/L as SO4, the flows in m3/s, the runs' dates) leaves the boundary samples looking like ordinary compliance samples; no column, code or sentence marks a sample as unmixed, and the register's sites read "boundary monitor" alike for all fourteen units.
Not rule application: the schedule files what the load is (the sulfate the unit's water carries past its boundary) and names no sampling point, mixing or balance; executing every filed rule on the boundary samples gives the default path's answer. The enumerated family (boundary sample times flow; the flow-weighted ratio estimator; the loggers' EC turned to sulfate; the inflows' conserved sum; the blend's concentration times the boundary flow; the mixed weir below less what joins between) files two sets, the default's four and the golden's four; the standing family (the constructions that respect conservation, since the record shows the boundary loads breaking the balance by more than 12 per cent on every run at the four weirs and holding it within 3 per cent everywhere else) files the golden at every member, spread under one per cent on every unit's load and none on the set, asserted.
Analyst test: a strong analyst conforms the laboratory results, units and gauged flows, multiplies each unit's boundary sulfate by its boundary flow on every dry-season run, averages and files KH1, MZ2, NT1 and NY3 over their allocations; every field is read and the schedule executed, and the call is wrong because the boundary samples at Esikhotheni, Ngwelezane Drift, Mabhokweni and Siphethu are one bank's water.
Estimand: umzimela_sulfate_load_allocation_schedule_2025.pdf section 3 with section 2 and Table 2: population, the catchment's resource units; outcome, the sulfate as SO4 a unit's water carries past its lower boundary in tonnes a day; window, the routine runs from 1 May to 30 September 2026, averaged; unit, the resource unit; comparison, its Table 2 allocation, over when the average exceeds it.
No decoy: nothing is planted to be caught; no memo, draft, briefing or stakeholder figure argues the boundary-sample loads, the register calls every boundary site the same thing, and the boundary weirs stand where the gauging network built them.
No certified replay: no certified or published figure reproduces either construction; the pack holds no earlier assessment, and the mines' returns reconcile with their own streams' loads under every construction alike.
Lesson: a concentration is a property of a mixed volume of water, and a sample a short reach below a confluence measures one bank's blend; a model that gets this right learns to check a monitoring point's representativeness against conservation before computing a load, which no build on file teaches (task263 recovers sources from blends, task120 balances a store in time).

## Survivor anatomy

Actor: the deciding property, whether a boundary sample is of the unit's mixed water, has no column in any file; it is a relation between the boundary sample's load and the loads its inflows carry in on the same run, across sites and the register's upstream units.
Link: the comparison that finds it, each boundary load against the sum of its upstream units' loads on the same run and against the mixed weir below, is one the compliance computation never asks for; the register lists upstream units by code, no key ties a sample to its inflows' samples, and no sentence invites the balance.
Reflex: the field's method, load at the compliance point as the sample's concentration times the gauged flow, is rung 0 and files KH1, MZ2, NT1 and NY3; the flow-weighted ratio estimator on the same samples (rung 2) files the same set.
Back-test: the textbook route validates where a solver checks it: at the ten mixed boundary weirs the sample-times-flow load agrees with the inflows within 3 per cent, the mine streams' loads sit within the range their licensed discharges and seepage explain, and the laboratory's re-runs agree with their first results within 9 per cent.
Second use: every file the decisive step reads has its own reason to be in the pack: the laboratory results and the gauges carry the default computation itself, and the register's upstream units define each unit's reach for the schedule; deleting the decisive step drops no file.
Shock: the units the step moves are not the pack's extremes: by boundary load MZ4 and NY2 sit mid-table, and the golden set is not the top or bottom four of any sort of boundary load, sulfate, flow or allocation (asserted).
Pins: the WHAT sits in the schedule (population, outcome, window, unit, comparison), and no filed sentence names a sampling point, mixing, a bank, a balance or conservation (asserted on the PDF's text); deleting section 3 unforces the call and that section names no step.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 boundary sample times boundary flow | section 3 defines the load | the boundary monitor per unit | the field's compliance load | none refutes it | the battery runs it | one product | none | readable |
| 1 re-runs, units and the dry runs conformed | the dry-season window filed | the -R suffix | battery item | none | yes | filter | none | readable |
| 2 the flow-weighted ratio estimator or the loggers' EC as surrogate | none | the loggers' series | a load-estimation reflex | none | a textbook load method | one ratio | the loggers have their own ask | readable |
| 3 (decisive) each unit's load from its inflows' conserved loads | none names mixing, a bank or a balance | no column marks a sample unmixed | not the compliance reflex | no file states a balance | no battery item | not affine in a shipped column | the register's upstream units define the reaches anyway | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the load past the boundary | the sulfate the unit's water carries, its inflows' loads conserved | the blend's concentration times the boundary weir's flow | same call, same whole tonnes (asserted) | schedule section 3; convergent |
| SF2 | which weir reads the unit's water | the conserved sum of the inflows | the next mixed weir below, less what joins between | same call within one per cent (asserted) | convergent |
| SF3 | a sample re-run by the laboratory | the re-run replaces the first result | the first result | same call (asserted) | the laboratory's -R suffix and later analysis date |
| SF4 | exceeds its allocation | above the Table 2 figure | at or above it | same call (no unit within 0.5 t/d, asserted) | schedule section 3 |
| SF5 | sulfate on the call's path | mg/L as SO4 throughout the laboratory's results | as S | not live (asserted) | the laboratory's unit column |
| SF6 | the as-S restatement factor in the asks | 96.06 over 32.06 | 3 | same figures in their bins (asserted) | ask A's ten-tonne rounding |

## Ladder

| Rung | Construction | Files | Dies to |
|---|---|---|---|
| 0 | boundary sample times boundary flow, mean of the dry runs | KH1, MZ2, NT1, NY3 | the four weirs' loads break the balance with their inflows on every run |
| 1 | rung 0 with re-runs, units and the dry runs conformed | the same four | the same fact |
| 2 | the flow-weighted ratio estimator, or the loggers' EC as a sulfate surrogate | the same four | the loggers sit at the same bank points |
| 3 (decisive) | each unit's load from its inflows' conserved loads, the mixed weir below confirming | KH1, MZ4, NT1, NY2 | the golden |

- **Margins on the cut pack** (asserted): every unit's conserved load is at least 8 per cent from its allocation
  (the tightest NY3 at 52 against 58 and NY2 at 40 against 35); the four flipped units' boundary loads sit at least
  8 per cent across their allocations the other way (MZ2 36 against 32, MZ4 31 against 34, NY2 30 against 35, NY3
  67 against 58); every whole-tonne load is at least 0.15 t from its rounding edge.
- **Pricing sequence.** (1) The residue the WHAT leaves is how a unit's flux is measured, a method, not a knob.
  (2) The move: four units' loads change by 9 to 15 t/d against margins to their allocations of 5 to 6 t/d. (3) The
  one-group-by route (load by unit) is rung 0 itself and files the default; no route is affine in a shipped column.
  (4) The step estimates nothing per unit: it sums measured loads, so its standard error is the inflows' sampling
  noise, under one per cent of the move. (5) and (6) No variance is corrected. (7) No subset of rows prints the
  mixed load at the four weirs. (8) The reflex sweep runs as code: rungs 0 to 2, the convergent members SF1 and SF2,
  the mess-neutral readings SF3.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the fourteen resource units of the schedule's Table 2 | filed, Table 2 |
| 2 | Unit of account | the resource unit, its load in t/d of sulfate as SO4 | filed, section 3 |
| 3 | Attribution window | the routine runs from 1 May to 30 September 2026 | filed, section 3 |
| 4 | As-of dating | the agency's extract of 9 October 2026, after the year closed | the files' dates |
| 5 | Version basis | the 2025 schedule replacing the 2019 one | the schedule's header |
| 6 | Denominator | none: a load is a total, not a rate | n/a |
| 7 | Weighting | each run's load equally, as section 3 averages them | filed |
| 8 | Window length | eleven dry-season runs | the run log |
| 9 | Boundary inclusivity | exceeds is strictly above; no unit within 0.5 t/d | asserted (SF4) |
| 10 | Rounding path | loads rounded once to whole tonnes from the unrounded mean | the prompt |
| 11 | Tie-break | none needed | n/a |
| 12 | Maturity and censoring | the dry season closed on 30 September; every run analysed | the laboratory's dates |
| 13 | Order of operations | run loads first, then the season's mean | filed, section 3 |
| 14 | Row order | no construction depends on file order | by construction |
| 15 | Duplicate resolution | a re-run replaces the first result | SF3, asserted |
| 16 | Identity normalisation | site, weir and station codes join through the register | the register |
| 17 | Netting against gross | none: loads are gross past the boundary | n/a |
| 18 | Dimensional units | mg/L times m3/s times 0.0864 to t/d | arithmetic |
| 19 | Code and status semantics | the gauges' quality code A throughout | the gauge file |
| 20 | Integerisation | none on the call | n/a |
| 21 | Clause scope | section 3 governs every unit alike | the schedule |
| 22 | Forward window contents | the 2027 directives follow from the 2026 dry season alone | schedule section 4 |

## Literal reader

Executed word for word, the schedule's section 3 asks for the sulfate each unit's water carries past its lower
boundary on the dry-season run days, averaged; the literal reader who computes it from the boundary samples files the
default, and the reader who checks the balance the river must keep files the golden; every member of the standing
family (SF1, SF2) files the golden to the whole tonne, and nothing filed reads to another set.

## Oracles

none: no file states any unit's load, a verdict or a ranking; the mines' returns reconcile with their streams under
every construction, and the mixed weirs downstream confirm the conserved loads without naming them.

## Ask sheet

Two asks on files the call never reads, each with two primaries from different families; the figures are the
generator's (`generator/figures.json`), stops and deltas asserted in `checks.py`.

**Ask A, sulfate each licensed mine discharge sent out in each quarter of the hydrological year (24 figures,
tonnes to the nearest ten).**
- H18 home: the discharges the directives act on, an audit trail every unit's case carries that the call does not
  turn on.
- Files and columns: `wul_discharge_returns_2025_26.csv` (point, month, totaliser, sulphate, EC, submitted),
  `cma_compliance_inspections_2025_26.csv` (findings), `wul_register_mine_discharges.xlsx` (the conditions sheet).
- Primary 1 (D3, units set per source and date): the commercial laboratory three of the mines use reported sulfate
  as S from its November 2025 batches, under the same column and header; the returns' EC stays level while the
  sulfate falls by a factor of three, and only that inconsistency finds it.
- Primary 2 (D2/D6, a state rebuilt across a change): Silwane's totaliser was replaced at the 14 February
  inspection; the February volume is the old meter's run to its final reading, which only the inspection log holds,
  plus the new meter's reading.
- Hazards: month-end totaliser readings differenced, the opening September 2025 return, a resubmitted March return.
- Pin test: the asking sentence pins the quantity (sulfate as SO4), the grain (each licensed discharge, each quarter)
  and the rounding; the devices sit in which unit a return's figure is in and which reading closes a month.

**Ask B, hours each continuous logger read the river's EC above its trigger level in each month from November 2025
to April 2026 (36 figures, whole hours).**
- H18 home: the early-warning record each unit's case carries, which the call does not turn on.
- Files and columns: `umzimela_ec_loggers_hourly_2025_26.csv`, `ec_logger_service_visits_2025_26.csv` (readings
  before and after cleaning), `ec_logger_memory_downloads_2025_26.csv`, the register's trigger column.
- Primary 1 (D9/D2, a reading that is not the river's): fouling drift grows between service visits and is cleaned
  off at each; the river's EC is the reading less the drift, allocated linearly over the interval from the visit's
  before-and-after pair.
- Primary 2 (D4, absence evidenced in a file no habitual join reaches): telemetry outages leave hours missing from
  the hourly file that the loggers' memory downloads hold.
- Hazard: the telemetry server's UTC timestamps against SAST months.
- Pin test: the sentence pins the river's EC, the trigger's source and the months; the devices sit in what a reading
  is and which hours exist.

**Main population zero-counts (asserted):** no ask device row (returns, inspections, logger readings, service
visits, memory downloads) is read by the call.

| Ask figures | Cracker (lands the call, runs the battery, executes every filed rule) | Mirror (stops at rung 0) | Verdict |
|---|---|---|---|
| A, 24 quarter figures | differences totalisers, takes the latest return and the inspection's final reading, reads the returns' sulfate as it stands | the same | miss |
| B, 36 logger-months | converts the clock, counts the telemetry as it stands | the same | miss |

The full includer (as-S restated, drift taken off, gaps filled) keeps 61 of 61; it is a stress row, not the gate.

Pair ceiling: 33.0 (the cracker on the call at 49.5, the mirror off it at 16.5, each keeping 5 of 61 ask criteria).
Mirror leakage: 8.2 per cent of the ask weight.
Measured by: generator/ceiling.py (run on the cut pack, target.zip ad0c0db7)

## Leak sweep

`leak.py task125 --asof 2026-10-09` on the final cut (target.zip ad0c0db7): REVIEW, no LEAK; each line ruled.
- Sweep 3 on `umzimela_sulfate_load_allocation_schedule_2025.pdf` (12 of 14 distinctive words of the call):
  harmless; Table 2 names every one of the fourteen resource units with its river, reach, weir and allocation, and
  section 4 says what a directive is, so the four units' names and the directive's words are there beside the ten
  others; the schedule states no load, no verdict and no order among the units.
- Sweep 4 on the same schedule (boundary, sample, section, samples, laboratory, carries): harmless; they are the
  WHAT's own words (the sulfate a unit's water carries past its lower boundary, the routine sampling runs, the
  agency's laboratory, section 19 of the National Water Act), and the schedule names no mixing, plume, bank, balance
  or conservation (asserted in `checks.py`).
- Architecture 2's reader section, which `leak.py` had been carrying over in the report, is dropped: it read a pack
  that no longer exists. This architecture's reader section is the main thread's stage-4 read.

## Pre-ship check

On target.zip ad0c0db71e2cf1bd (`python3 task125/generator/make.py`):
- Generator checks 37 of 37, the independent verifier (pandas, its own reading of the pack) all passed, two builds
  byte-identical (target, golden, submission).
- `figures_check.py` 75 figures, none absent from `generator/figures.json`; `precut.py` 61 checks, no FAIL or WARN;
  `voice-check.py` PASS (875 characters); `leak.py` REVIEW ruled above; `generator/ceiling.py` pair 33.0, leakage 8.2
  per cent.
- The prompt's second sentence first read "The case belongs in ...", an idiom only task127 and task457 also use; it
  now names the directives paper, the shell unchanged (where, the, pdf+xlsx). `surface` holds task127 at 0.100 after
  the reword, so the pair rests on other surface features (both ask "where" of a public body's allocation) and stays
  with the four for the author's adjudicated read.
- `guard.py heart` WARN and `surface` exit 0. The WARNs: `overuse.org_family` (a catchment management agency is a
  statutory body under the minister, and government_agency is its honest kind) and `repeat.gate_g` against task474
  v7 (method_or_model_selection is the honest key here, two ways to put a load on a boundary with the record's
  balance choosing; task474's is a pass mark carried across a test-vendor change through common candidates, another
  mechanism in another domain). The four pairs `surface` promotes for the author's adjudicated read (task127 and
  task304 on surface similarity at 0.100 and 0.101, task257 and task84 on the card axes already differentiated) share
  no driver; the people screen's one note (the schedule's approving Chief Executive Officer, drawn third in the same
  `names --locale zu_ZA --seed 125` draw) is on the card.
- Realism sweep before the final cut: the register's six non-boundary sites had coordinates on an arithmetic
  sequence, now placed up their own rivers from each unit's boundary monitor; the inspection log's numbers now run in
  date order (the meter change had an out-of-sequence number); the schedule's reach for MZ1 read as ending at
  MZ2's weir and now ends at the Khambule Stream; a reservoir site shared a place name with MZ5's weir and was
  renamed.
- Stage 4 (the leak reader and the determinism judge) runs from the main thread, since a fork cannot spawn them.

## Tried and rejected


- The source note's decisive rung (Housing Support's cohort run off on the 2021 intake's 30-instalment term) as the decisive rung: the pilot's plain solver replays records at the finest grain and runs event studies on staggered cohorts, and the 2021 intake's full rise and run-off sits in the same flagged-cell series, so a strong solver constructs it; kept as rung 3.
- Re-pricing Adult Social Care's standing stream at a 2027/28 tariff filed in the council's budget (band 2 from 366 to 399 a week, out of cell 14): honestly labelled (time, A) or (time, G13), which the guard blocks inside the batch (task121 v1 lineage) and as spent in ten older builds, with G13 task122's decisive generator; a relabel to G11 or G6 would not name the move as a reviewer would. It also hangs on a stated rate one multiplication from the digit consequence.
- An upward entrant move with the cohort drop under about a sixth of the closed-year figure: the run-off (down) and the entrants (up) cancel near the closed-year carry-forward, which then lands inside 10 per cent of the answer (L4); the targets keep the drop near 30 per cent.
- Step-down hosts inside the flagged cell, paid the same 1,464 as long-term band 2 hosts and separable only by the turnover pattern in their payment histories (a downward decisive move): its honest label is G3 (record versus operation), task121's decisive generator, and the affected payments sit in the very cell the solver is already examining.
- A guest-level arrangements register in the pack: it turns the carers' composition into a schema-visible join from payee to guests, RC01 v2's death (a two-hop join found from the schema alone) and FC01 loop 2's (a dated attribute of an entity the chain already joins); not shipped.
- Landlord-consolidated remittances in the Tenancy Sustainment scheme (a landlord's monthly payment falling into cell 14 once one household remains): the forward entrants are a few per cent of the answer at any realistic landlord mix, too small for a decisive rung.
- A fourteenth four-weekly cycle in 2027/28 (a 366-day year with a payment date on 1 April 2027) or a 53-Thursday year as a rung: worth 2 to 8 per cent of one stream, a knife-edge hazard; the design picks cycles that add no plan-year date unless it prices the cell.
- A plan-year move from four-weekly to monthly payment, or to fortnightly payment runs: a stated change the solver applies at first order, and its amount consequence sits on the remittance grain a screen rung already validates.
- The filter's own examination holds merging held payments into the next run: a council's digit filter examines after payment, and the merge timing opens forks the judge would read as unpinned.
- The 2025/26 screen close-out as the context artifact (close_out_summary): blocked at registration by ban.artifact against task124, drafted in parallel; the same closed-year figures ship in the filter's 2025/26 run log (operations_log).
- One step-down rate with 70 dual carers on one combined amount (3,044): 910 payments a year land in Adult Social Care cell 30, which then flags itself on the 2025/26 screen (paper ratio about 1.4), so the closure moves payments from one flagged cell to another and the decisive rung is worth zero; three tiers and 60 carers keep every Shared Lives cell under 0.86 of threshold.
- Twins identical on every statement figure (payments tested and MAD as well as the cell-14 count): Housing Support would need about 50,000 payments a year in range, which a county's housing-related support service cannot carry; the twin is held on the run log's 2025/26 line only.
- A second plan-year monthly series for the department that moves most (the draw's criteria arithmetic): a denser split of the committed figure, twelve more criteria the cracker banks free; replaced by the two 2025/26 tables.
- Annotating the plan-year month furthest from the closed-year line: January, February and March 2028 tie at 476 routed payments, an ungradable part; the busiest month (December 2027, 638 by run month) is annotated instead.
- The 2027/28 payment-run calendar on the main path, with "four weeks ending on the run date" as the pin against a 12-run reading: unnecessary, since the 28-day cadence fixes 13 runs and a 12-run reading files the same hundred; kept for the monthly ask only, so the main path carries no file an ask device lives in.
- The spending file from April 2021 with every department's background (build): about 100 MB of CSV; the file starts April 2023 and the 2021 round's histories ship in the Housing Support case extract, which is where the term pin lives anyway.
- Waste & Environment cell 25 as the run log's extra cell (build): a cell-25 count near 500 under 0.86 of its threshold needs a Waste department of more than 22,000 payments a year; cell 11 reaches it with 11,000.
- The rung-1 lever at net cell 20 with Property & Facilities at 7,400 invoices (build): rung 1 landed 8,348, and the net basis with the run-off applied then filed 6,458, inside the answer's hundred; the gross cells 20 to 25 had no room for more bills, so the lever moved to net cell 15 and rung 1 to 8,992.
- Rung 4 (Shared Lives carers' combined amounts decomposed against the weekly rate schedule, step-down placements dropped) as the decisive rung, round 1: the plain solver landed 6,522, filed 6,500, by listing the carer amounts against the rates at its step 4 in its own words, "On each carer pay date, 102 payments are £1,464, and 22 + 20 + 18 more are £1,464 plus a step-down rate (£3,044, £3,272, £3,524). When Home First step-down closes on 31 March 2027 those 60 drop to £1,464". The noisy amount universe did not hide them: the three combined amounts are the only carer amounts equal to 1,464 plus a step-down rate, so the decomposition is one subtraction, not a construction.
- Harden loop 1 (opening line), rung 4 as the decisive rung measured by round 1 plain (proxy 80.2, call landed at path step 4): the solver read every "Shared Lives carer payments" row as one carer's whole fee, summed at the carer grain in its own words, "ASC total: 115 x 12 + 162 x 13 = 3,486", having climbed rungs 2 and 3 and stepped over the side cell by taking the 2025/26 cells; a louder pin, a second decoy or a noisier amount list would only lengthen the same subtraction, so the repair attacks the assumption the sentence holds fixed (one row is one carer's fee) rather than the decomposition itself.
- Rung 5 (joint households' half-fees at the household grain) as the decisive rung, round 2 plain (proxy 85.1, call landed at path step 4, filed 6,700): the solver never constructed the household grain; it decomposed each half against the rate card on its own, read the 2,274, 2,388 and 2,514 halves as two weeks of each rate, dropped the step-down weeks and got 1,484 per vendor, in its own words "2,274/2,388/2,514, which leave 1,484 (16). That gives 178 per run". The halves are linear in the household fee, so halving the rates gives the same result as re-summing the household and halving it again; the grain gap never moves a single vendor's post-closure amount, and the rung cannot change the answer (discriminator dominance failed, not silence).
- Harden loop 2 (opening line), rung 5 as the decisive rung measured by round 2 plain (proxy 85.1 after the --landed yes regrade, call landed at path step 4): the solver treated each joint half as two weeks of each weekly rate, in its own words "2,274/2,388/2,514, which leave 1,484 (16). That gives 178 per run", so a grain step whose arithmetic is linear in the fee (halve, then subtract the halved step-down rate) can never move a vendor's post-closure amount; the repair has to make the household grain change the result, which only a non-linear step at that grain (a household-level threshold, cap or rate that a half cannot see) can do.
- Centring the loop 2 answer at 6,902 by trimming a flat stream by one payment a month (Property & Facilities 81 to 80, or Highways cell 49 66 to 65): the 2025/26 batch returns are drawn per payment, so the trim reshuffled the examined counts and put both unused-volume charges 2 pence off a half-pound edge (1,604.48 and 603.52 or 655.04); loop 1's stream counts were kept, the answer is 6,914 (36 from its upper edge) and asks B1, B2 and C are unchanged.
- The whole build after harden loop 2 (rung 6, the joint-household one-guest payment rule, as the decisive rung; round 3 plain missed at 43.3): the determinism judge returned SEND_BACK on 2026-10-10 with the mechanism matching the note on every field, so the build was retired and not submitted.
- Architecture 1 as a whole (2026-10-12, at the re-root): spent by two in-house solves and a judge SEND_BACK; the
  author's no-retirement rule re-roots the slot to architecture 2 on a new pairing.
- Interviewer falsification in a victimisation survey (2026-10-12, at the draw, never registered): fabricated
  interviews are wrong records, so catching them is a planted defect under the three rules whatever the method.
- A sample boost entering all at wave 1 against rotation-group bias (2026-10-12, at the draw): the first-interview
  bias moves a regional rate by about 0.1 point at any realistic boost, too small to carry a call.
- A staggered web-first rollout read by event time (2026-10-12, at the draw): the arm comparison and the per-wave
  phasing are what a survey-literate solver does first, and every estimator choice opens a numeric fork.

- Architecture 2's first ladder (2026-10-20, at this re-root): the methods note's section 5 stated the procedure the
  decisive step executes ("applying the change to the last full quarter collected before it and re-running the
  estimation as in section 4"), so a blind Sonnet reader at medium effort, holding only a fresh unzip of target.zip,
  the prompt and the figure names, took 2 of 2 call figures and 38 of 53 ask figures and quoted that sentence as what
  told it the step. Under rule 3 that is rule application, not analysis. Not repairable by deleting the sentence
  alone, because the base quarter it pinned would then be an open knob (measured: up to 0.085 point of movement on a
  figure printed to 0.01); the re-root deletes the sentence, lets the call-record app's coverage settle the base
  quarter, and moves the cap's timeline so the decisive step carries the headline.
- Keeping the cap on one intake and removing section 5 only (2026-10-20, at the re-root, measured): with the cap
  issued for a single quarter before the released one, the wave-1 route and the golden give the same cap share of the
  April to June to July to September change, because only one of the two quarters has a capped wave 1. The decisive
  step then carries no graded figure of the headline, only the forward path, which is exactly the half the measured
  reader took last. Rejected for the field-year timeline, which puts a capped intake in both compared quarters and
  makes the wave-1 route file 0.00 of the 0.27-point rise.
- Grading the non-contact bias of the published rate instead of the six-visit counterfactual (2026-10-20, at the
  re-root): the level of the bias is genuinely unobserved (measured at +0.78 to +0.84 point of unemployment in every
  pre-cap quarter against the eligible population, and +0.99 under the cap), which would put an estimated quantity in
  the deciding position. Rejected on the determinacy screen: it needs the never-contacted households, whose outcomes
  are reached only by extrapolating a level-of-effort gradient past the sixth visit, and the geometric contact process
  behind the pack is a three-class mixture whose tail mass is identified only to within a wide band, so the estimator
  family would be open on a figure printed to 0.01.
- Making the wave structure something the solver infers from the sample's own composition rather than from the methods
  note's section 1 (2026-10-20, at the re-root): a methods note that does not document a rotating panel's rotation is
  not a methods note, and the person file carries a `wave` column besides, so the rotation is schema-visible whatever
  the documents say. Readability test 2 fires. The re-root leaves the rotation filed and moves the decisive step to
  the unit the change acts on instead.
- Identifying the capped-out households from the capped intakes rather than from a pre-cap quarter, so that the
  counterfactual is estimated rather than subset (2026-10-20, at the re-root): with the pre-cap call records removed
  the forward path is unidentified, because nothing then measures how the selected households' outcomes persist
  across the telephone waves; with them shipped the counterfactual is exactly recoverable by subsetting and the step
  is arithmetic. Same dial, both ends. Recorded as the architecture's structural ceiling: no stage-2 move puts an
  estimated quantity in the deciding position on this draw, and a third measured Gate F failure retires the number
  rather than hardening it.

- Architecture 2 as a whole (2026-10-31, at the batch audit, re-rooted rather than repaired): it shipped before the survivor-anatomy gates and falls short on all three of them. The actor is schema-visible (the person file's `wave` and `intake` columns, the visit number reaching the later waves through the household serial, a key that invites the join), so there is no actor without a column and no link without a key; and the field's method (re-running the calibrated estimator on the capped subset) is the golden rather than the bottom of the ladder, which its own "Not rule application" line conceded by calling the decisive step exact arithmetic on recorded fields, argued rather than measured. Architecture 3 draws a new domain and world.

