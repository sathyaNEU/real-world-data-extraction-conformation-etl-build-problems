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
  compliance log and the plant's equipment register conformed into the permit's monthly record for process vent unit
  EU-P1, and the unit's 2026 total read against its limit.
- **The decision and the quantity:** whether Pellston Fine Chemicals' process vent unit EU-P1 kept within its
  calendar-year VOC limit of 3.2 tons in 2026, and by how much it went over if it did not. The Chalmont County Air Quality
  District's inspector reviews the 2026 records at the February 2027 compliance evaluation, and the plant's 2027
  production increase under the 2025 permit revision rests on the unit's compliance. Retrospective by nature, with its
  reason: the permit's compliance year closed on 31 December 2026 and the determination is the record the evaluation
  reads.
- **Shape:** 15 (fields to one schema): the permit's monthly EU-P1 record, each month across its fields, with the
  determination and its margin; the criteria sum is written at stage 2.
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
- **Prototype (the analyst test priced in code before the card):** a minute-level 2026 of six reactors, two fluid-bed
  dryers and a still on one header (scratch `proto_x6.py`, four seeds): at a 3,800 scfm fan and 99.4 per cent tested
  destruction the field's method with offline minutes files 2.1 to 2.4 tons, the fan's maximum checked on hourly mean
  header flow 2.7, and the minute-by-minute capture 4.0; at 4,000 scfm the golden is 3.2 to 3.5 against 2.1 to 2.4. The
  excess, about 1.8 tons, is under 1 per cent of the VOC the vents carry, spread over several hundred short
  coincidences. Targets for the generator, not shipped figures.
- **Sources:** every file is synthetic, written by `generator/`; the plant, district, vendors and people are invented;
  no real dataset is used.

## Default path

A strong analyst with every field read correctly:

1. Reads the permit: EU-P1 is the nine vents on closed-vent system CVS-1 routed to RTO-1; its VOC is limited to 3.2
   tons per calendar year; the control efficiency is the one demonstrated in the most recent performance test (99.4 per
   cent in May 2025); the month's EU-P1 VOC is calculated from the batch records and the vent calculation basis.
2. Conforms the batch records: the legacy historian's export (January to June, local time) and the new MES export
   (from July, UTC), the cutover week's steps once, the MES operation codes mapped to the basis's steps, and the
   licensed product line's Nm3/h and kg/h rows converted at the stated reference conditions.
3. For each executed step, VOC vented is the basis's rate for that product and step times the step's recorded minutes,
   summed by month.
4. Applies 99.4 per cent destruction to every pound vented while RTO-1 was on line in its one-minute log and counts the
   pounds vented in its offline minutes as uncontrolled: the closed-vent system's capture taken as complete, which is
   the field's method for controlled emissions from a closed-vent system with its downtime accounted for.
5. Sums 2026 and compares the total with the 3.2-ton limit.

**Ends on:** 2.2 tons, under the 3.2-ton limit

**Golden:** 4.0 tons, over the 3.2-ton limit by 0.8 tons

The figures are the prototype's targets and are replaced by the generator's measured ones at stage 3.

## Stump sentence

The default path applies RTO-1's tested 99.4 per cent destruction to every pound the batch records vent while the oxidizer was on line, counts its offline minutes uncontrolled and files EU-P1 at 2.2 tons, under its 3.2-ton 2026 limit, because it never asks whether the oxidizer could draw every vent at once: when the dryers' drying cycles and a reactor's charging exhaust coincide the header carries more than RTO-1's 3,800 scfm, the excess lifts PSV-31 to atmosphere untreated, and EU-P1 emitted 4.0 tons.

## Three rules

Task type: emissions-inventory (Physical & Environmental Sciences): the plant's two batch-system exports, its vent calculation basis in two unit systems, the oxidizer's one-minute compliance log and its equipment register conformed into the permit's monthly record for process vent unit EU-P1, a conformation serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is EU-P1's 2026 VOC emitted to atmosphere, worked the way an air permit engineer works a batch-process vent inventory: each executed step's vented VOC from the vent calculation basis, times one minus capture times destruction, where a closed-vent system captures every pound only while its control device can take every vent at once and the destruction applies only to the gas the device receives.

Swap: "did the call centre's queue drop more calls in 2026 than its contract allows" keeps a capped server shared in time and loses the step's ground: no vent stream carrying solvent vapour at its own concentration, no destruction applied to the share the fan draws, no relief releasing the header's mixed gas, so the swapped task has no counterpart to the VOC that left untreated at each coincidence or to the tested efficiency the easy route applies to every pound.

Layer 1: the batch records in two layouts across the July 2026 cutover (local time against UTC, batches renumbered, the cutover week's steps in both exports), the vent calculation basis in two unit systems (scfm and lb/hr against Nm3/h and kg/h for the licensed product line), the oxidizer's log in local standard time all year and the register's merged headers and tag spellings; each is how the producing system writes, nothing is placed to be caught, and checks.py asserts the call holds under every reading of them.

Layer 2: allocation under real constraints (capacity and queueing): the choice that flips the call is reading the closed-vent system's capture minute by minute from the vents' coincident flow against RTO-1's maximum draw, instead of taking it as complete.

Decisive step: rebuilding the header's total flow minute by minute from every vent's executed steps and the basis's flows, and charging as untreated the share of each minute's mixed gas above RTO-1's 3,800 scfm fan maximum, which lifts PSV-31 at the oxidizer inlet; the share is zero in most minutes and reaches a quarter of the gas in the minutes when both dryers dry while a reactor charges.

Not semantics: every field, unit and definition read correctly (the two layouts, UTC and local time, Nm3 and scf at their reference conditions, the step codes, the register's tags, the permit's standard conditions) still leaves the easy route treating every vented pound as reaching RTO-1, because no field records how much of each vent's gas the fan drew; the step is the inference that the header's summed flow exceeded the fan's maximum in thousands of minutes, which the coincidence of the steps shows and no column holds.

Not rule application: the permit files the population, outcome, window, unit and comparison, the records the month's VOC is calculated from and the tested efficiency, and no rule says how much of each vent the oxidizer received, so executing every filed rule files 2.2 tons; the enumerated family (destruction on every pound, offline minutes added, the fan's maximum checked on hourly, 15-minute, 5-minute and one-minute header flow, the excess charged to the last vent to open) spreads 1.7 to 4.0 tons, the standing family (the constructions that respect the fan's instantaneous maximum at the records' minute resolution with the relief at the oxidizer inlet) spreads under 0.05 tons, and the ruling-out is silent: no sentence names coincident flow, a capacity check or what PSV-31 releases.

Analyst test: a strong analyst who conforms every export and reads every condition, takes the basis's rate times each step's minutes, applies the tested 99.4 per cent to every pound vented while RTO-1 ran and counts its offline minutes uncontrolled files EU-P1 at 2.2 tons, under the 3.2-ton limit (the default path's Ends on); one who checks the fan's maximum against hourly mean header flow files about 2.7 tons, still under; only the minute-by-minute capture files 4.0 tons, over; checks.py runs each on the clean truth.

Estimand: the permit (Chalmont County Air Quality District permit to operate, Revision 3, conditions on EU-P1): the population (the nine vents of EU-P1 on closed-vent system CVS-1), the outcome (VOC emitted to atmosphere from EU-P1 at every release point), the window (calendar 2026), the unit (tons of VOC) and the comparison (the 3.2-ton calendar-year limit), the month's VOC calculated from the batch records and the vent calculation basis, with the efficiency demonstrated in the most recent performance test.

No decoy: nothing is planted: the batch exports, the vent basis, the compliance log, the register, the permit, the test report and the solvent balance are the producing systems' records; no memo, draft, earlier record, report or published figure states or ranks EU-P1's 2026 emissions.

No certified replay: no certified, filed or published 2026 EU-P1 figure ships, and the method is not recovered by reproducing any figure; the 2025 test confirms the efficiency, which both routes use.

Lesson: a closed-vent system captures every pound only while its control device can take every vent at once, so where intermittent batch vents share a fixed-draw oxidizer the capture is read from the vents' coincidences against the draw; no build on file reads a shared device's instantaneous limit against coincident loads rebuilt from batch records.

## Survivor anatomy

Actor: the minutes in which the header carried more than RTO-1's fan could draw, and the gas above the draw, have no column in any file: they are a relation across every vent's executed steps (their coincidence on one clock) and the register's fan maximum, which nothing stores.

Link: the coincidence is read by sweeping all nine vents' steps on one clock, a cross-unit comparison no key offers (the batch exports are keyed by unit and batch) and no sentence invites; the register carries RTO-1's maximum and PSV-31's discharge as equipment data among many.

Reflex: the field's method for controlled emissions (vented VOC times one minus the tested destruction, the closed-vent system's capture taken as complete, offline minutes uncontrolled) sits at R1 and files 2.2 tons, under the limit (the default path's Ends on).

Back-test: the textbook route validates: the plant's 2026 solvent balance (purchases less product, waste and recovery) reproduces the basis's vented VOC within about 2 per cent, the 2025 test confirms 99.4 per cent, and the compliance log shows the combustion temperature held; none of them sees what the fan did not draw.

Second use: every file the step reads is read by the default path too: the batch exports (each step's minutes), the vent basis (each step's flow and VOC, the flow being the basis's own input to its VOC), the register (which vents sit on CVS-1, RTO-1's rating, PSV-31) and the compliance log (offline minutes).

Shock: the excess is spread over several hundred short coincidences, and the months it lands in are not the months with the most vented VOC or the most batches; no shipped statistic shows it, and the golden's monthly figures are no interval of any shipped sort (asserted at stage 3).

Pins: the permit files the population, outcome, window, unit and comparison and the efficiency's source; no sentence names coincident flow, the header's total, a capacity check or what PSV-31 releases.

## Readability screen

Written at stage 2.

## Semantic fork table

Written at stage 2.

## Ladder

Written at stage 2.

## Closure table

Written at stage 2.

## Literal reader

Written at stage 2.

## Oracles

Written at stage 2.

## Ask sheet

Written at stage 2.

## Pre-ship check

Written at stage 5.

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
