# task479 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 7, drawn 2026-11-03 after architectures 1 to
6 were spent (6 at the 11-01 re-check's stage 4, still at the portal pending). Nothing of any earlier world, dataset,
decisive step or prompt shell is kept; the slot moves out of healthcare into Physical & Environmental Sciences.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task479.json` (architecture v7, lineage v1 to v6 spent), registered
  2026-11-03 after a pull. Guard WARN only, answered in the card's notes: `repeat.gate_g` (binding_constraint repeats
  task307 v2, a spent card in another domain, and the label is the honest one for a shared draw limit). Redrawn at the
  draw: the context artifact from operations_log (ban.artifact against task157) to filed_standard; the forcing event
  from statutory_or_regulatory_filing (ban against task173) to audit_or_inspection; the decisive pattern from C (spent
  under gap objective and binding_constraint in ten builds) and from G7 (ban.pattern against task157) to none with G3
  first; personas from Kenneth and Calvin (older builds) to Alyssa Alexander and Dylan Gonzalez, drawn with
  `guard.py names --geo us --seed 4797`. Differentiation lines on the card for task106, task303, task482 v7, task87 and
  task472.
- **Pairing:** Physical & Environmental Sciences, task type `emissions-inventory`, which serves ETL: two batch-system
  exports across the July 2026 cutover, a vent calculation basis kept in two unit systems, the oxidizer's one-minute
  log and the plant's equipment register conformed into the District's quarterly record for process vent unit EU-P1,
  and the unit's 2026 total read against its limit.
- **The decision and the quantity:** whether Pellston Fine Chemicals' process vent unit EU-P1 kept within its
  calendar-year VOC limit of 2.5 tons in 2026, and by how much it went over if it did not. The Chalmont County Air
  Quality District reviews the 2026 records at its February 2027 compliance evaluation, and the plant's 2027 production
  increase under the 2025 permit revision rests on the unit's compliance. Retrospective by nature, with its reason: the
  permit's compliance year closed on 31 December 2026 and the determination and the fourth-quarter AQ-117 are the
  record the evaluation reads.
- **Shape:** 15 (fields to one schema): the AQ-117 form's fields for each quarter (emitted, year to date) with the
  determination, the total and the margin, and the solvent deliveries sheet's fields: the call 3, the quarters 8, the
  deliveries by solvent 7 and by quarter 4, the two files and the deliveries sheet 3, 25 criteria.
- **Strategy:** `binding_constraint`; Gate G `binding_constraint`; gap `objective` (the controlled figure the field
  computes is right for what reached the oxidizer and is not what the limit counts); generators G3 (record against
  operation) and G7 (operating window). Layer 2 family `allocation_constraints` (capacity and queueing), pattern
  `own:the capture of a closed-vent system read minute by minute as the control device's maximum draw over the
  concurrent vent flow`.
- **Data-native sentence:** nine vents share one header to an oxidizer whose fan was sized before the 2025 expansion
  added the second fluid-bed dryer and the reactor bay's charging exhaust, and each vent's flow follows its own batch's
  progress, so the header's total flow is set by coincidences between batches that no record stores.
- **Abstraction sentence:** against task106, the nearest approved build in the shared-capacity family, the sentence a
  reviewer would write for both ("a capacity several users draw on, counted in full for each") names the family and not
  a driver: task106 sizes each supplier against a whole pool of spare legs that only one of them can use, a static
  double-booking per corridor, while here nothing is allocated, every vent's gas is real and reaches the header, and
  the step finds the minutes in which the vents' summed flow exceeded one fan's instantaneous maximum. Against task303,
  the nearest approved build on the link (siblings' records in the same minute), co-timed tickets there are one
  upstream event to subtract, while co-timed vents here are all genuine discharges and the step adds the share the
  shared device could not draw. No driver-level sentence covers either pair.
- **Measured (the generator's clean truth, checks.py R3):** a minute-level 2026 of six reactors, two fluid-bed dryers
  and a still on one header: the vents carried 194.8 tons of VOC; at RTO-1's 3,800 scfm and the tested 99.4 per cent
  the field's method files 1.9 tons, the fan checked on hourly mean header flow 2.1 and the minute-by-minute capture
  3.2 against the 2.5-ton limit. The header ran above the fan in about 10,000 minutes (peak 6,745 scfm) and about
  2,700 lb, 0.7 per cent of what the vents carried, left untreated at PSV-31.
- **Sources:** every file is synthetic, written by `generator/`; the plant, district, vendors and people are invented;
  no real dataset is used.

## Default path

A strong analyst with every field read correctly:

1. Reads the permit: EU-P1 is the nine vents on closed-vent system CVS-1 routed to RTO-1; its VOC is limited to 2.5
   tons per calendar year; the destruction efficiency is the one demonstrated in the most recent performance test (99.4
   per cent in May 2025); the quarter's EU-P1 VOC is calculated from the batch records and the vent calculation basis.
2. Conforms the batch records: the legacy system's export (January to the 1 July cutover, local time) and the new MES
   export (from the cutover, UTC), the in-flight batches' steps once, the MES operation codes mapped to the basis's
   steps, and the licensed product line's Nm3/h and kg/h rows converted at the permit's standard conditions.
3. For each executed step, VOC vented is the basis's rate for that product and step times the step's recorded minutes,
   summed by quarter.
4. Applies 99.4 per cent destruction to every pound vented while RTO-1 was in RUN in its one-minute log and counts the
   pounds vented in its other minutes as uncontrolled: the closed-vent system's capture taken as complete, which is
   the field's method for controlled emissions from a closed-vent system with its downtime accounted for.
5. Sums 2026 and compares the total with the 2.5-ton limit.

**Ends on:** 1.9 tons, under the 2.5-ton limit

**Golden:** 3.2 tons, over the 2.5-ton limit by 0.7 tons

## Stump sentence

The default path applies RTO-1's tested 99.4 per cent destruction to every pound the batch records vent while the oxidizer was in RUN, counts its other minutes uncontrolled and files EU-P1 at 1.9 tons, under its 2.5-ton 2026 limit, because it never asks whether the oxidizer could draw every vent at once: when the dryers' drying cycles and a reactor's charging exhaust coincide the header carries more than RTO-1's 3,800 scfm, the excess lifts PSV-31 to atmosphere untreated, and EU-P1 emitted 3.2 tons.

## Three rules

Task type: emissions-inventory (Physical & Environmental Sciences): the plant's two batch-system exports, its vent calculation basis in two unit systems, the oxidizer's one-minute compliance log and its equipment register conformed into the District's quarterly record for process vent unit EU-P1, a conformation serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is EU-P1's 2026 VOC emitted to atmosphere, worked the way an air permit engineer works a batch-process vent inventory: each executed step's vented VOC from the vent calculation basis, times one minus capture times destruction, where a closed-vent system captures every pound only while its control device can take every vent at once and the destruction applies only to the gas the device receives.

Swap: "did the call centre's queue drop more calls in 2026 than its contract allows" keeps a capped server shared in time and loses the step's ground: no vent stream carrying solvent vapour at its own concentration, no destruction applied to the share the fan draws, no relief releasing the header's mixed gas, so the swapped task has no counterpart to the VOC that left untreated at each coincidence or to the tested efficiency the easy route applies to every pound.

Layer 1: the batch records in two layouts across the July 2026 cutover (local time against UTC, batches renumbered, the in-flight batches' history migrated into the new system while the old one holds their steps to the cutover, the step in progress left open), the vent calculation basis in two unit systems (scfm and lb/hr against Nm3/h and kg/h for the licensed product line), the oxidizer's log in Eastern Standard Time all year with a degraded chamber thermocouple in August, and the register's merged headers and tag spellings; each is how the producing system writes, nothing is placed to be caught, and checks.py R2 and SF7 to SF10 assert the call holds under every mishandling of them.

Layer 2: allocation under real constraints (capacity and queueing): the choice that flips the call is reading the closed-vent system's capture minute by minute from the vents' coincident flow against RTO-1's maximum draw, instead of taking it as complete.

Decisive step: rebuilding the header's total flow minute by minute from every vent's executed steps and the basis's flows, and charging as untreated the share of each minute's mixed gas above RTO-1's 3,800 scfm maximum, which lifts PSV-31 at the oxidizer inlet; the share is zero in most minutes and reaches two fifths of the gas at the year's peak coincidence, when both dryers dry while two reactors charge.

Not semantics: every field, unit and definition read correctly (the two layouts, UTC and standard time, Nm3 and scf at their reference conditions, the step codes, the register's tags, the permit's definitions) still leaves the easy route treating every vented pound as reaching RTO-1, because no field records how much of each vent's gas the fan drew; the step is the inference that the header's summed flow exceeded the fan's maximum in about 10,000 minutes, which the coincidence of the steps shows and no column holds.

Not rule application: the permit files the population, outcome, window, unit and comparison, the records the quarter's VOC is calculated from and the tested efficiency, and no rule says how much of each vent the oxidizer received, so executing every filed rule files 1.9 tons; the enumerated family (destruction on every pound 1.2, downtime uncontrolled 1.9, the fan checked on hourly 2.1, 15-minute 2.8, 5-minute 3.1 and one-minute 3.2 mean header flow) spreads 1.2 to 3.2 tons, the standing family (the constructions that respect the fan's instantaneous maximum at the records' minute resolution under every licensed convention of the fork table) spreads 3.18 to 3.20 tons, and the ruling-out is silent: no sentence names coincident flow, a capacity check or what PSV-31 releases.

Analyst test: a strong analyst who conforms every export and reads every condition, takes the basis's rate times each step's minutes, applies the tested 99.4 per cent to every pound vented while RTO-1 was in RUN and counts its other minutes uncontrolled files EU-P1 at 1.9 tons, under the 2.5-ton limit (the default path's Ends on); one who checks the fan's maximum against hourly mean header flow files 2.1 tons, still under; only the minute-by-minute capture files 3.2 tons, over by 0.7; checks.py R3a to R3f run each on the clean truth.

Estimand: the permit (Chalmont County Air Quality District permit to operate PTO-2219-0447, Revision 3, conditions B.1, B.4, B.5 and D.1): the population (the nine vents of EU-P1 on closed-vent system CVS-1, Section A), the outcome (VOC emitted from EU-P1, emitted meaning released to the atmosphere), the window (calendar 2026 in local time, summed from its quarters), the unit (tons of 2,000 lb) and the comparison (the 2.5-ton calendar-year limit), the quarter's VOC calculated from the batch records and the vent calculation basis, with the efficiency demonstrated in the most recent performance test.

No decoy: nothing is planted: the batch exports, the vent basis, the compliance log, the register, the permit, the test report and the purchasing records are the producing systems' records; no memo, draft, earlier record, report or published figure states or ranks EU-P1's 2026 emissions, and the District's AQ-117 template ships blank.

No certified replay: no certified, filed or published 2026 EU-P1 figure ships, and the method is not recovered by reproducing any figure; the 2025 test confirms the efficiency, which both routes use.

Lesson: a closed-vent system captures every pound only while its control device can take every vent at once, so where intermittent batch vents share a fixed-draw oxidizer the capture is read from the vents' coincidences against the draw; no build on file reads a shared device's instantaneous limit against coincident loads rebuilt from batch records.

## Survivor anatomy

Actor: the minutes in which the header carried more than RTO-1's fan could draw, and the gas above the draw, have no column in any file: they are a relation across every vent's executed steps (their coincidence on one clock) and the register's fan maximum, which nothing stores.

Link: the coincidence is read by sweeping all nine vents' steps on one clock, a cross-unit comparison no key offers (the batch exports are keyed by unit and batch) and no sentence invites; the register carries RTO-1's maximum process flow and PSV-31's discharge as equipment data among eighteen rows.

Reflex: the field's method for controlled emissions (vented VOC times one minus the tested destruction, the closed-vent system's capture taken as complete, minutes not in RUN uncontrolled) sits at R1 and files 1.9 tons, under the limit (the default path's Ends on).

Back-test: the textbook route validates: the 2025 test confirms 99.4 per cent, the plant's calculated loading from the vent basis for the steps in progress, which the report gives as process data, sits within 3 per cent of the measured inlet loading (its runs at 3,342 to 3,371 scfm, under the fan), and the DAHS log shows RTO-1 in RUN at its operating temperature through the coincidences; none of them sees what the fan did not draw.

Second use: every file the step reads is read by the default path too: the batch exports (each step's minutes), the vent basis (each step's flow and VOC, the flow being the basis's own input), the register (which vents sit on CVS-1, RTO-1's rating, PSV-31) and the compliance log (the minutes not in RUN).

Shock: the release is spread over about 10,000 minutes in short coincidences, and the months it lands in are not the months with the most vented VOC (rank correlation 0.75, checks.py S1); no shipped statistic shows it, and the golden's quarters are no interval of any shipped sort.

Pins: the permit files the population, outcome, window, unit and comparison and the efficiency's source; no sentence names coincident flow, the header's total, a capacity check or what PSV-31 releases.

## Readability screen

Each rung against the seven tests (1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear, 7 second use); the reflex row comes from the field's vocabulary for controlled emissions (destruction efficiency, capture efficiency taken as 100 per cent for a closed-vent system, downtime uncontrolled).

| Rung | 1 | 2 | 3 | 4 | 5 | 6 | 7 | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 tested destruction on every vented pound, downtime ignored (1.2 t) | B.4 names the efficiency | DAHS mode column | yes | test report | no | yes | no | readable |
| R1 the field's method, minutes not in RUN uncontrolled (1.9 t) | B.2 and B.4 | DAHS mode column | yes | test report | no | yes | no | readable |
| R2 the fan checked on hourly mean header flow (2.1 t) | no | no | no | no | no | no | no | silent |
| R3 (decisive) the fan's maximum against each minute's summed vent flow, the excess untreated at PSV-31 (3.2 t) | no sentence names flow, capacity or the relief | no column holds a capture, a header flow or a release | the field's reflex is complete capture | no control scores it | no hygiene step finds it | a sweep over every vent's steps on one clock, not one subtraction | every file it reads is read by R1 | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | VOC emitted | released to the atmosphere at S-1, S-2 or PSV-31 | the S-1 and S-2 stacks of Section A only | within, 1.9 t | permit D.1: "Emitted means released to the atmosphere"; B.1 limits VOC emitted from EU-P1 |
| SF2 | calendar 2026 and its quarters | local time | EST or UTC boundaries | same call, same bins | D.1, and asserted: every quarter in the same bin |
| SF3 | ton | 2,000 lb | metric tonne | over, 2.9 | D.1: "Ton means 2,000 pounds" |
| SF4 | standard conditions for the PX line's Nm3 | 68 F and 29.92 inHg | 60 F (3.2) or Nm3 uncorrected (3.1) | over | D.1: "Standard conditions means 68 F and 29.92 inches of mercury" |
| SF5 | destruction efficiency | 99.4 per cent, the test's mean | the lowest run, 99.36 (3.3) | over | B.4 and the report: "The VOC destruction efficiency demonstrated is 99.4 per cent, the mean of the three runs" |
| SF6 | a step's duration | end less start | the end minute counted too (3.4) | over | B.7: the records show the start and end of each step; a step from 08:00 to 08:36 lasts 36 minutes |
| SF7 | the cutover's in-flight steps | once | twice, Batchwise and Orbitas's migrated rows | same call, 3.2 | same call, asserted |
| SF8 | the Batchwise step open at the cutover | completed from Orbitas's migrated row | ended at the cutover | same call, 3.2 | same call, asserted |
| SF9 | the DAHS clock | Eastern Standard Time all year | prevailing local time | same call, 3.2 | the export's header line, and same call |
| SF10 | the Orbitas clock | UTC | local time | same call, 3.2 | the columns start_utc and end_utc, and same call |
| SF11 | the fan's maximum | 3,800 scfm | none: RTO-1's maximum process flow and FN-1's rating are one figure | same call | the register, both rows |
| SF12 | what PSV-31 releases | the header's mixed gas, the VOC share equal to the flow share | the excess charged at one vent's concentration | over | the register: PSV-31 on HDR-1 at RTO-1's inlet plenum, downstream of every vent's line |
| SF13 | minutes not in RUN | uncontrolled through the bypass | WARMUP as controlled (2.9) | over | the register: XV-30 "Open whenever RTO-1 is not in RUN" |
| SF14 | rounding path | quarters unrounded, the year their sum (B.5), each rounded once | rounded quarters summed | same figures | asserted: both paths give 1.4, 2.1, 2.6, 3.2 and 0.7 |
| SF15 | the comparison | 2.5 tons in any calendar year | none | over | B.1 |
| SF16 | delivered (the asks) | the supplier's delivery date on the invoice line | the warehouse posting date | asks only, every ask figure moves | the asking sentence's "delivered"; AP's Delivery Date column |
| SF17 | each solvent (the asks) | the solvent delivered, named on its invoice line | SOL-07 read through the master's current description | asks only, n-heptane and isohexane move | the deliveries' own invoice lines name n-heptane before June 2026 |
| SF18 | how much of the gas above the fan's draw leaves untreated | all of it: the header's mixed gas above 3,800 scfm leaves at PSV-31 | a part of it (the call needs 48 per cent or more of the proportional release; at 48 per cent the year is 2.5 tons) | over at the whole release, within only under 48 per cent | the register: RTO-1's maximum process flow and FN-1's rating are both 3,800 scfm, a hard cap on the draw, and in RUN PSV-31 at the inlet plenum is HDR-1's only outlet besides RTO-1 (XV-30 "Open whenever RTO-1 is not in RUN"); ruled at stage 4 |

## Ladder

| Rung | Construction | 2026 tons | Call | Margin |
|---|---|---|---|---|
| R0 | tested 99.4 per cent on every vented pound, RTO-1's downtime ignored | 1.2 | within | 2.14x under |
| R1 | the field's method: 99.4 per cent on every pound vented in RUN, other minutes uncontrolled (the default path) | 1.9 | within | 1.35x under |
| R2 | R1 with the fan checked on hourly mean header flow | 2.1 | within | 1.18x under |
| R2b | the fan on 15-minute or 5-minute mean flow (not cheap: the capacity question already asked) | 2.8, 3.1 | over, wrong figure | |
| R3 | the fan's maximum against each minute's summed flow, the excess untreated at PSV-31 (golden) | 3.2 | over by 0.7 | 1.28x over |

Quarters (golden): 1.4, 0.7, 0.5, 0.6 tons; year to date 1.4, 2.1, 2.6, 3.2. Under R1: 1.0, 0.3, 0.3, 0.3. Bin edges: the total 0.046 t, the quarters 0.026 t or more, the year-to-date figures 0.030 t or more (checks.py M1).

## Closure table

| Axis | Reading here | Move |
|---|---|---|
| 1 Population | the nine vents of EU-P1 on CVS-1 (Section A); the boiler, generator and LDAR files are other units | filed: Section A and B.1 |
| 2 Unit of account | VOC in tons for the unit | filed: B.1, D.1 |
| 3 Attribution window | a step's minutes fall in the local quarter they occur in | C1: EST and UTC boundaries give the same bins (SF2) |
| 4 As-of dating | the 2026 record as exported in January 2027, every 2026 step closed | static, asserted |
| 5 Version basis | vent basis Rev 7, the only revision shipped, covering every product and step run | C1 |
| 6 Denominator | none, a total | not applicable |
| 7 Weighting | none, a sum over minutes | not applicable |
| 8 Window length | calendar 2026 | filed: B.1 |
| 9 Boundary inclusivity | a step occupies its start minute to the minute before its end | SF6, B.7 |
| 10 Rounding path | unrounded quarters, the year their sum, rounded once | SF14, asserted |
| 11 Tie-break | none | not applicable |
| 12 Maturity and censoring | no step open at the year end; the open cutover step closed in Orbitas | C1 (SF8) |
| 13 Order of operations | capture before destruction: only the drawn share reaches RTO-1 | the design: PSV-31 upstream of RTO-1 on the register (SF12) |
| 14 Row order | sums independent of order | C1 |
| 15 Duplicate resolution | the in-flight batches' steps once | SF7, same call |
| 16 Identity normalisation | R101, PFC-R-101 and R-101 are one unit; batch numbers differ across the systems, steps matched by unit and start | C1 on the systems' own unit codes |
| 17 Netting against gross | none | not applicable |
| 18 Dimensional units | Nm3/h at 0 C to scfm at 68 F, kg/h to lb/hr; the asks' gallons at the master's density and kilograms at 2.20462 | SF4 (D.1), asserted |
| 19 Code and status semantics | Orbitas op codes and operation numbers to the basis's steps; DAHS modes RUN, WARMUP, OFF | SF13 (XV-30 on the register) |
| 20 Integerisation | none | not applicable |
| 21 Clause scope | B.1 the unit's calendar-year total; B.3's temperature blocks are not part of the call | filed |
| 22 Forward window contents | none: retrospective, the compliance year closed on 31 December 2026 | the reason in Draw |

## Literal reader

Executed word for word, the prompt and the permit give VOC emitted from EU-P1 (released to the atmosphere, D.1) in calendar 2026 in local time, in tons of 2,000 lb, from the batch records and the vent basis (B.5) with the tested efficiency (B.4), against 2.5 tons (B.1): every reading in the fork table gives over and the golden's figures except those each ruled out by a quoted sentence (SF1, SF3 and SF4 by D.1, SF5 by B.4 and the report's summary, SF6 by B.7, SF13 by the register's XV-30), and the easy answer, 1.9 tons, comes from the easy method on the same literal estimand (every vented pound taken as reaching RTO-1), not from another reading.

## Oracles

None ships: no file states or ranks EU-P1's 2026 emissions (the AQ-117 template is blank, checks.py G7), no capture, header flow or release figure exists in any file, the test report's runs are from 2025 at 3,342 to 3,371 scfm, under the fan, and the DAHS log carries RTO-1's temperatures and mode only. For the asks, the warehouse receipts and the invoice lines agree on every delivery's quantity (verify.py asserts it), and no file totals deliveries by solvent or by quarter.

## Ask sheet

- **Ask A, all solvents delivered in each quarter of 2026** (four figures, nearest 100 lb). Primary D8, a recorded date for the event date: the warehouse receipts carry only the clerk's posting date, and postings stop for the half-year count (24 to 30 June) and the year-end count (17 December to the New Year), so the deliveries inside a count post in the next quarter or year; the supplier's delivery date is on the invoice line, joined by the delivery ticket. Hazards: units (gallons at the master's density, kilograms at 2.20462) and split tankers (one delivery on two tank receipts, each its own part, which a dedup on the bill of lading cuts in half).
- **Ask B, each solvent delivered in 2026** (seven figures, nearest 100 lb). Primary D2, a label stored before a silent switch: material SOL-07 was n-heptane drums until 1 June 2026 and isohexane since, and the material master as of January 2027 names it isohexane, so the as-of join files January to May's n-heptane drums as isohexane; the invoice lines name what was delivered. Shared hazards: the year-end counts move every solvent (the 2025 restock posted in January 2026, the 2026 restock, ordered against the 2027 plan, posted in January 2027), and subsequent debits repeat their order's quantity on the invoice file.
- **Use:** the plant's solvent deliveries are the cross-check the District's inspector runs against the vented VOC the basis gives, and the delivered pounds feed the annual emission statement's material usage.
- **Separation:** the asks read only the purchasing files (receipts, invoice lines, material master), none of which the call reads (checks.py A6); delete every device and the call is unchanged.
- **Literal pins:** "delivered" and "each solvent" are the asking sentence's WHAT (SF16, SF17); no filed sentence names a count freeze, a posting lag or the code's change.

| Ask figure | Cracker (posting date, master names) | Golden | Cracker |
|---|---|---|---|
| Methanol | 1,438,300 | 1,435,200 | miss |
| Toluene | 851,500 | 855,300 | miss |
| Isopropanol | 54,100 | 55,100 | miss |
| Ethyl acetate | 106,700 | 108,700 | miss |
| n-Heptane | 221,100 | 295,500 | miss |
| Isohexane | 92,100 | 47,900 | miss |
| Tetrahydrofuran | 89,900 | 88,700 | miss |
| Q1 all solvents | 763,600 | 659,500 | miss |
| Q2 all solvents | 616,000 | 660,600 | miss |
| Q3 all solvents | 772,600 | 775,200 | miss |
| Q4 all solvents | 701,500 | 791,100 | miss |

Pair ceiling: 26.0 (the cracker 45.0 on the call with no ask figure kept, the mirror 7.0 off it); the invoice-line route that counts the subsequent debits keeps 2 of the 7 solvent figures.

Mirror leakage: 0.0 per cent of ask weight

Measured by: generator/ceiling.py on the cut pack

## Stage 4 rulings

The leak reader (one isolated thread, `leak_check_report.md` ## Solver's-eye read) and the determinism judge
(`determinism_check_report.md`, DETERMINISTIC, APPROVE, Gate G PASS, Gate H analytical) read target.zip 43c1d6c4;
every finding was closed in one generator pass.

- Judge finding 1, ruled: the over call needs 48 per cent or more of the proportional excess released at PSV-31 (the judge's thinnest point, non-blocking). RTO-1's 3,800 scfm (its maximum process flow and FN-1's rating, one figure) is a hard cap on what the oxidizer draws, and while RTO-1 is in RUN PSV-31 at the inlet plenum is HDR-1's only outlet besides RTO-1 (XV-30 opens only out of RUN), so all of the header's mixed gas above the draw leaves untreated; SF18 in the fork table, and checks.py SF18 asserts the register's outlets, the proportional release (2,704 lb, 3.196 tons, over) and the call holding at 48 per cent of it or more.
- Judge finding 2, fixed in the generator: the planned outage's work order opened on 21 July while the DAHS shows RUN to 29 July; it now opens 20 minutes before the DAHS shows RTO-1 OFF and closes 75 minutes after RUN resumes (WO26101811, 2026-07-29 00:40 to 2026-07-31 09:35 local; the orders opened between 21 and 29 July renumber with it); checks.py S13.
- Judge finding 3, fixed in the generator: the register's PSV-31 last-inspected date is 2026-05-21, the day of its annual inspection order WO26101668; checks.py S13.
- Judge finding 4, process: the leak reader ran in the same stage; the rubric's 25 criteria are the shape's count in Draw.
- Reader Q6 (what decides), ruled analytical: RTO-1's 3,800 scfm maximum and PSV-31 appear only as equipment-register ratings and no rule says what the excess does, so what decides the call is the minute-by-minute reconstruction of the vents' coincident flow; the judge's Gate H reads the same.
- Reader realism note, the BST report's sentence setting the expected inlet loading against the measured: softened in the generator to process data (the plant's calculated loading for runs 1 to 3, the comparison left to the reader); the paragraph carries nothing the golden reads (the golden takes the 99.4 per cent from the summary).
- Reader realism note, permit B.3's block-validity detail: harmless, kept; B.3 is the oxidizer's temperature condition with the averaging rules a permit's monitoring condition files, and it enters no figure (closure axis 21).
- leak.py sweep 2, "generator" in the permit: harmless, EU-G1's own row (Emergency generator GEN-1).
- leak.py sweep 3, golden figures in the pack: harmless, the permit's limit (2.5, B.1), EU-G1's 100-hour cap (C.3), the test's 99.4 per cent that both routes use, and a DAHS digit run (12:47,900.6).
- leak.py sweep 3, the permit carrying the call's words: harmless, the governing document naming its own unit, limit and pollutant.
- leak.py sweep 4, design-note terms in the permit (record, records, county, minute, method, oxidizer): harmless, the District's condition language; none names coincident flow, a capacity check or what PSV-31 releases.
- leak.py sweep 12, column words in the permit (Closed, Description, Equipment, Permittee, Unit): harmless, the District's own record sharing the plant's naming.

## Pre-ship check

- The 10/10 rules re-read against the built pack: the decisive step is analytical (checks.py R3a to R3f: no cheap route lands the call, the field's method 1.9 tons, the hourly check 2.1, the golden 3.2; SF18: the call holds at the proportional release and down to 48 per cent of it); the mess is Layer 1 only (R2a to R2d and SF7 to SF10, the call unchanged under every mishandling); no decoy (G7, the AQ-117 template ships blank, and no file states a 2026 EU-P1 figure).
- Stage 4: the leak reader found no decisive-step sentence, no ranking file and no file that exists to help the analyst (question 6 ruled analytical); the judge returned DETERMINISTIC, APPROVE, Gate G PASS and Gate H analytical, so reader and judge agree on Gate H. Every finding was closed in one generator pass (## Stage 4 rulings). The pass moved three pack files and no value the call reads: the CMMS planned outage order and the register's PSV-31 date (data only) and the BST report's process sentence; verify.py still reads the fan's 3,800 scfm from the register and the 99.4 per cent from the test's summary. The reader was not re-run (no sentence moved beyond the BST wording) and the judge not re-judged (APPROVE, no FIX_NOW).
- Free gates on the final cut (target.zip sha256 cbe457c6): checks.py 62 of 62 (SF18 and S13 added at stage 4); verify.py 28 of 28 from target/ alone; two builds byte-identical, the second in its own process under another hash seed; figures_check.py 54 of 54, figures.json, submission.md, metadata.json and golden/ byte-identical to the stage 3 cut; freeze.py check --mode determinism PASS against the snapshot taken before the first edit; precut.py 61 checks, 0 FAIL, 0 WARN; voice-check.py PASS; leak.py REVIEW (as of 2027-01-29), every line ruled harmless in ## Stage 4 rulings; guard.py heart WARN (repeat.gate_g against task307 v2, answered on the card) and surface exit 0, its four promoted pairs (task477, task478, task480, task310) answered by differentiation lines on the card; the container sweep (leak.py 10) clean on target/.
- The card is current: answer, stump, driver_concrete, deliverables, spine rows, layer1 and the prompt's shell (other, fill, docx+xlsx) match the measured build.

## Tried and rejected

- The seed's own mechanisms as the decisive step (2026-10-20, screened at the draw): earning premium by term rather
  than by policy effective year is a stated accounting rule (rule application), and a condominium master policy's unit
  count read as units is a field reading (data semantics); both stay in the pack as Layer 1 under filed sentences.
- A catastrophe-adjusted expected loss ratio by county (2026-10-20, screened): the estimator family for an expected
  catastrophe loss from a short record is open (window mean, frequency from a long declarations record times the
  window's severity, a fitted severity tail), so the graded figure forks, and filing the method makes it rule
  application.
- Event-clustered confidence bounds on each county's loss ratio (2026-10-20, screened): a variance-only correction that
  widens every interval, so the conservative reflex lands the hold; and the annual series shows the spread directly.
- The Risk Rating 2.0 glide path's full-risk premium for policies still capped (2026-10-20, screened): every policy
  transitioned within one year, so the full-risk premium is censored at the same multiple for all of them and the
  distribution beyond it is not identified; the cap itself is a statutory rule.
- The latest event's claims completed by days since landfall, and open claims from their adjusters' damage estimates
  (2026-10-20, screened): the first is task181's route-specific delay and task451's arrival history, the second is a
  policy-terms computation (rule application).
- Claims linked to policies by quasi-identifiers to rate premium bands (2026-10-20, screened): linkage error correction
  is spent (task449, task468) and a fusion through shared attributes is task465's.
- Policy tenure from originalNBDate with left truncation (2026-10-20, screened): task133's delayed entry.
- Rating each insured building at the claim rate of buildings in its present condition (2026-10-20, screened): the
  policy terms carry an elevated-building indicator for every term, so the rate by present state is one group-by on a
  visible column, the opponent's stratification reflex; kept as a wrong rung (it gives a raised building the later rate
  of elevated buildings in general, which on the river is the low rate of buildings never in a 2016-sized flood).
- Bridge deck deterioration from inspection pairs of different lengths (2026-10-20, screened in another world): per-year
  normalisation, the obvious correction, lands within rounding of the interval-aware estimate on fair decks, so the
  lever is too small.
- Every insured building as the population (2026-10-20, stage 2): the buildings below the base flood level carry the
  counties' whole flood history, so the lowest rates fell to the upland counties with or without the replay, and the
  replay moved no county across the fifth place; the population narrowed to the elevated insured buildings the pilot's
  insurers will quote, where the raised buildings are a third of some counties' book.
- The re-entered transfer claims carrying only NFIP Direct's own payments (2026-10-20, stage 2): summing every
  record's payment then lands each county's payments, so the payment half of ask A carried no device; the re-entry
  carries the claim's payments to date, as NFIP Direct's record of a transferred claim does.
- The Saltreach surge of 2005 a foot under the base flood level and Kettlemoor's 2016 middle reach 0.6 feet under it
  (2026-10-20, stage 2): the protection-to-the-base-flood-level rung (R3) and the class-rate rung (R2b) each filed the
  golden five; with the 2005 surge 0.6 feet under the level in Saltreach (still two feet and more under the raised
  floors) and Kettlemoor's middle reach a foot under it, both rungs file a wrong five.
- A persona pair whose first name the names script does not return (2026-10-20, stage 2): replaced with Samantha
  Walter from `guard.py names --geo us --seed 479`.
- Contents-only and unit owners' records joined to the building rate (2026-10-20, stage 2): neither moves the call,
  so they stay Layer 1 under 2.1 and 2.3 rather than a device.
- Architecture 1, NFIP claims replayed on the elevated buildings as they stand (2026-10-21, spent at stage 4): reader 1
  quoted guidelines 3.1 ("would bring ... as they stand") as the decisive text, replayed each claim's water on the
  present floor and landed the call, every rate and 30 of 72 figures; reader 2 missed on the claims since elevation
  but took ask B's counts from the final inspections; the judge NOT_DETERMINISTIC FIX_NOW on ask B's share, completion
  and county keys and called the estimand's wording an announcement. The estimand that files a counterfactual names
  it; re-rooted to architecture 2 in a fresh world.
- Architecture 2, the lodging Monitor benchmarked to the Department's annual receipts (2026-10-21, spent at stage 4):
  both scored readers computed each county's Department-to-Monitor ratio for every published year as their first
  calibration, saw the straight-line drift and carried it a year, landing the call, every growth figure and most ask
  figures (exit 1, 50 and 54 of 80); both also used the register's county for the transferred properties and linked
  the crosswalk gaps. A drift that the first diagnostic of a benchmarked series prints is no stump; re-rooted to
  architecture 3 in a fresh world.
- Architecture 3, self-funded groups' 2027 retained claims under a fixed specific deductible (2026-10-21, spent at
  stage 4): reader 2 re-applied the $250,000 deductible to each large claimant's trended claims and landed the call
  (exit 1, 22 of 80); reader 1 trended the retained total and missed (exit 0, 9 of 80). Leveraging under a fixed
  deductible is textbook to a strong reader once a fixed deductible and a claimant list sit side by side; both readers
  missed both ask devices (reissued member ids, a reopened claimant file), which are worth re-skinning.
- Architecture 4, a charter network's spring benchmark rescored for rapid guessing (2026-10-21, spent at stage 4):
  both scored readers took the vendor's scores and missed the call, but the judge returned DETERMINISTIC and SEND_BACK
  on Gate G (planted_defect_flip): leaving out rapid-guessed responses is cleaning contaminated rows, the stump
  collapses on clean data, and the vendor's score report is a shipped figure that ranks the campuses wrongly. The asks
  leaked 85.7 per cent because a temporary id register and two named rosters documented both devices. A decisive
  step that removes bad responses is Layer 1, and any shipped report of the easy route's figure is a Gate G artifact.
- Architecture 5, a schools health cooperative's 2026 plan year completed under each district's 2026 deductible (2026-10-21, spent at stage 4): both scored readers completed each district's January to June 2026 by the 2025 factor of its 2026 plan, naming deductible leveraging unprompted, and landed the call and every expected PMPM (exit 1, 32 of 64 each); reader 7 also resolved ask A's reissued ids on person attributes, while ask B's reopened claimant files held for both. A field-standard correction whose inputs (a design history and per-unit experience by design) sit side by side in the pack is found by a strong reader; the judge thread was stopped as moot.
- Adverse selection in dual-option employers as the decisive step (2026-10-21, screened at the draw): a simulation of members choosing the high-deductible plan by their own risk put the electees' plan-year factor at 1.06 to 1.12 against 1.19 for a whole-employer move, but a dual-option employer's blended factor stayed within 0.005 of its own history and plan-level pooling is dominated by the non-electees' claims, so neither the easy route nor plan pooling moved the call.
- Architecture 6, each employer's expected claims by credibility against the trust's level (2026-11-01, spent at the re-check's stage 4): the judge (pass 2) returned NOT_DETERMINISTIC, SEND_BACK, the memo's literal reading filing each employer's own trended experience (the default path) and the broker survey left open as a complement, and the leak reader read section 3 as filing the method; filing the WHAT that closes it names the decisive step, so the fork is the stump. The 10-21 judge had approved the same memo. A dictionary and a manifest also shipped (leak.py sweep 1).
- Architecture 7 draw (2026-11-01, the re-root after architecture 6's SEND_BACK), twelve candidates screened across five ETL task types before any card was registered, each with a default path ending wrong, the swap test, the survivor anatomy and the bin test on paper, the strongest priced in code; none clears, so the slot is paused at the draw on the orchestrating session's stop rule (twelve screened across three or more task types). task464 architecture 5 (2026-10-27) had already measured cells A to D mechanism-dead; the twelve lines below are this draw's own screens.
- Screen 1, IRT test equating, a single-group linking study whose administration order was not counterbalanced, concordant cut read by equipercentile on both scores (2026-11-01): a single-group bridge concordance is task464 architecture 2, solved on the portal, and order effects in a single-group design are a textbook check, so the decisive rung is readable.
- Screen 2, IRT test equating, each 2027 form's passing raw score pre-equated from a Rasch bank whose pretest-only items were all calibrated in the last section of the paper (2026-11-01): priced in code (proto p1.py, 24 seeds, four classes, 96 forms: the section-7 penalty moves each form's expected raw score at the standard 0.55 to 1.84 marks, the bank-as-filed route lands the truth's passing score on 12 of 96 forms, the mean and median adjustments from the promoted items agree on 95 of 96), then found spent: task482 architecture 6 (2026-10-22) is the same draw, a placement form pre-equated from a Rasch bank with its scored items calibrated in the end field-test section, landed at stage 4 by a reader who fitted a Rasch position term; guard.py driver.text scored it only 0.09, the abstraction test caught it.
- Screen 3, IRT test equating, repeat candidates' prior exposure to anchor items reused across consecutive forms inflating the new group's anchor scores (2026-11-01): item exposure is spent in the cell (task464 architecture 4, C4; task249), and excluding repeaters from an equating sample is the field's standard practice, a reflex.
- Screen 4, data integration and record linkage, the distinct-person count of a shelter system where transitive closure chains namesakes and the same-night bed register splits the chains (2026-11-01): resolving pairwise matches into entities is spent at task486 architecture 2 (stage 4) and BLOCKs at driver.text 0.40, task464 architecture 5 measured the dial one-ended (the cutoff decides how many pairs exist), and identity resolution may not decide a call.
- Screen 5, data integration, a count moved from source zones to target zones by address occupancy evidence (2026-11-01): task486's driver (multi-site units' members placed at each site in proportion to size times density).
- Screen 6, data integration, low-cost sensors calibrated by co-location and carried outside the co-location's humidity range (2026-11-01): the response outside the overlap is not identified (Gate B) and a calibration curve is a model of the measurement.
- Screen 7, census and register data quality, emigrants left on a population register read through signs of life in other administrative sources (2026-11-01): task471 architecture 4 (the units a field audit finds absent) spent at Gate F, and sign-of-life capture is the capture family (task448, task456, task473).
- Screen 8, census and register data quality, transfers out left in a spell base as censoring rather than as a competing exit (2026-11-01): the maturity family (task485, task469), and cumulative incidence over competing exits is a survival analyst's reflex.
- Screen 9, official time-series production, a survey's level drifting from its benchmark since the sample frame was last refreshed (2026-11-01): task474's re-root screen found it dead on paper (the drift is disclosed by past benchmark revisions), and task464 architecture 5 closes the per-case recovery shape in cell D.
- Screen 10, seasonal adjustment, a seasonal break at a survey reference-period change (2026-11-01): the regARIMA rigor card is held by task146 and an estimated seasonal factor is a model of the measurement (task464 architecture 5, cell D).
- Screen 11, emissions inventory, refrigerant service top-ups read as the year's leakage (2026-11-01): on a stable fleet the timing bias cancels, so the lever is near zero, and the activity-level input is on record (task470, task474, task480, task484; task464 architecture 5's six inputs).
- Screen 12, emissions inventory, boilers sharing one gas meter allocated pro rata while they run in a lead and lag order (2026-11-01): task459's staging driver (a ratio that changes once a supplementary stage engages above a unit's base capability).
- Architecture 7 draw resumed 2026-11-03 on the author's word to proceed (the 11-01 pause waited on the author's ruling, which `CLAUDE.md` no longer allows): five more candidates screened outside the twelve above and outside task464 architecture 5's cell map, each with a default path ending wrong, the swap test, the survivor anatomy and the bin test on paper; screens 13 to 16 die below, and the fifth (a closed-vent system whose oxidizer fan cannot draw every batch vent at once) was priced in code and carded as architecture 7.
- Screen 13, official time-series production, a repeat-sales house price index whose sale pairs include homes renovated between sales, the permits linked to the parcels (2026-11-03): the field's own repeat-sales methodology excludes substantially remodelled homes where the data allow (a reflex), and excluding the pairs against adjusting them by permit value forks the index by more than the decisive step is worth.
- Screen 14, census and register data quality, dual-system estimation with people moving between census day and the coverage survey (2026-11-03): the mover treatment is a filed procedure of the field's coverage methodology and the closed-population check is textbook, and dual-system estimation is cell C's card 1 family (task448, task249 architecture 3, task471).
- Screen 15, emissions inventory, an equity-share consolidation in which two subsidiaries hold each other's shares, so the effective shares need the ownership matrix's inverse (2026-11-03): the swap test fails, because the effective equity share is a corporate-finance quantity that reads the same with profits in place of emissions, so the domain is a backdrop.
- Screen 16, emissions inventory, a carbon adsorber's working capacity per regeneration cycle overrun by the heavy cycles (2026-11-03): the breakthrough curve (sharp against a mass-transfer zone) forks the passed share, and the vendor's working capacity is defined at a breakthrough level that leaves the excess open; carried in its flow-limited form, where the cap is a fan's hard maximum and the excess is mixed header gas.
- Architecture 7's first prototype (proto_x2, reactor depressurisations at 2,700 scfm for about twelve minutes, 2026-11-03): rejected as physically unreal, because blowing a reactor down from two atmospheres releases about a thousandth of that volume; the high flows on a batch header are fluid-bed dryer purges and charging exhaust.
- Architecture 7's second prototype (proto_x3 to proto_x5, dryer purges and charging exhaust at realistic flows, 98.6 per cent destruction, 2026-11-03): the golden ran only 1.03 to 1.27 times the field's method, under the 1.38 the rung and final margins need together, because a lower destruction raises the controlled base as fast as the excess; carried at the tested 99.4 per cent and a 3,800 scfm fan, where the golden runs 1.5 to 1.9 times the method.

- RTO-1's 3-hour block temperature deviations as an ask (2026-11-03, stage 2): each device it could carry (the DAHS's standard-time clock against the permit's local blocks, the 135-minute validity rule, TE-101A's degraded readings against TE-101B) is found by the hygiene battery, read from a work order or executed from a filed rule, so the cracker keeps every figure; the chamber channel ships as Layer 1 and the asks moved to the purchasing records.
- The PSV-31 release as an asked figure (2026-11-03, stage 2): naming the relief in the prompt announces the decisive step, so the release stays in the golden's memo and is graded only through the quarters and the total.
- Test runs averaging 99.43 per cent (2026-11-03, stage 3): a reader taking the runs' unrounded mean filed 3.1 tons against the golden's 3.2, a fork on a number the report states; the runs were set to average exactly 99.40, and the lowest run (3.3 tons) is ruled out by B.4 and the report's summary (SF5).
- The warehouse receipts with a received date beside the posting date (2026-11-03, stage 3): the field reads itself, so the delivery date moved to the supplier's invoice line, the receipts keeping the posting date their system writes.
- The BST report's process paragraph setting the inlet loading the vent basis expects against the measured, "within 3 per cent" (2026-11-03, stage 4): the leak reader read the comparison as written for the analyst; the paragraph now gives the plant's calculated loading as the process data a test report carries.
- The planned outage's work order opened on 21 July, eight days before the DAHS shows RTO-1 OFF (2026-11-03, stage 4): the judge read the two records as disagreeing; the order now opens and closes on the DAHS's outage.
- PSV-31's last inspection on the register a day before its inspection order (2026-11-03, stage 4): one date in both, 21 May.
