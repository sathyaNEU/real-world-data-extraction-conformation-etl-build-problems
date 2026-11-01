# task452 design note: Kilcarrow Works, mercury to air in 2026 against the annual load from 2028

Architecture 3, re-rooted 2026-11-01 at the Batch 3 queue reset (one architecture per world: architecture 2, the
jurisdictional forest programme's deforestation area, and architecture 1, the tributary phosphorus loads, are closed
worlds; their records sit under the Architecture 2 record and in the Tried and rejected list). Fiction as-of date
2027-01-11.

## Draw

- **Pairing.** Physical & Environmental Sciences, task type `emissions-inventory`, objective Data Extraction &
  Conformation (ETL). The headline is a conformed figure (each kiln's 2026 mercury to air, conformed from the
  production ledger, the laboratory's composites, the control system's records and the annual stack tests into the
  licence's quantity) and the call is the monitoring-and-investment consequence of that figure under the 2028 load.
- **World.** A two-kiln cement works in Ireland (Kilcarrow Cement Ltd, fictional; no real plant, firm or licence),
  its quarry and quality laboratory. Personas from `guard.py names --geo Ireland --locale en_IE --seed 452`: Naomi
  Lynskey (environment and quality, the memo's author), Helena Sheane, Charlie Redican (unused in the pack so far).
- **Card.** v3 registered 2026-11-01T21:33:33Z and re-registered at 22:23:18Z once prompt.txt carried the new shell
  (whether | for | mercury | pdf+xlsx; the dead architecture's how-many | put | give | pdf+xlsx moved to
  `lineage_shells`): gap objective then population, pattern none, generators G16, G7,
  G13, Gate G etl_conformance, strategy forecast_method_backtest (the data support one route, conservation of the
  element through the kiln system, because the tested rate is stationary only per gram of mercury fed, not per kiln
  hour), decision quantity_figure, question form whether, forum executive_team, forcing budget_or_appropriation,
  org manufacturer, role compliance_or_audit, calibration none, context artifact monitoring_export. The v2 identity
  moved to `lineage` with fate "shipped 2026-10-14 with no portal result, re-rooted 2026-11-01 at the Batch 3 queue
  reset". Check on the registered card: WARN only. WARNs answered: `shell.repeat` read the dead architecture's
  prompt (how-many, put, pdf+xlsx); the new prompt's shell is whether, a use-led second sentence ("For the capital
  round") and pdf+xlsx under the corpus caps, which `voice-check.py` passes. On the re-registered card the check
  reads WARN only: `repeat.decision` (quantity_figure, task160) is the lane's natural decision for a conformed
  figure, and `repeat.deliverables` (pdf+xlsx, task123) is the genre of a works' memo to its executive with the
  annual-report workbook; neither is a similarity finding. Redrawn at the draw: shape 07 (banned
  against task259), the triples (objective, G16, method_or_model_selection) and (population, G7 or G13, method
  selection), each spent in four or more builds, so Gate G is etl_conformance, the honest label for a conformed
  figure judged against a licence.
- **Candidates written before choosing** (each death is a `## Tried and rejected` line): ET09 hospital margin peers;
  capitated encounters completed from order footprints; rod-packing vent methane under packing replacements;
  landfill surface methane from hot-spot-sited chambers; daytime-only chamber fluxes on a temperature model; IRT
  pre-equating under exposure drift; cement kiln mercury with the raw mill stopped (drawn).
- **Data-native sentence.** A kiln's raw mill takes the mercury in the kiln gas into the raw meal and hands it back
  to the kiln while it runs, and lets it go up the stack when it stops for a full meal silo, which it does most days;
  the annual stack test is always run with the mill on, so the tested rate is one operating state's, while the
  year's release is fixed by what the kiln line took in and what left it by its other exits.
- **What the forcing file pins (the ETL pincer).** The ledger and the laboratory pin an opportunity count, the
  year's mercury fed per input and per month; reading every field correctly still files the tested rate times the
  hours, because no field says the tested rate does not hold in the other operating state.

## Survivor anatomy

- **Actor:** the deciding property, each kiln's mercury in the hours its raw mill was stopped, has no column in any
  file: the stack tests record one state, the historian records no mercury at all, and the year's release exists
  only as the relation between the ledger's monthly tonnages, the laboratory's monthly composites and the two exits.
- **Link:** the ledger names inputs one way in January to June and another from July (Rathmore shale and Shale, Fly
  ash (PFA) and PFA, Clinker produced and Clinker made), the laboratory names them by sample code (LS-2603, FA-2609)
  and some only by quarter, and no key joins a month's tonnage to its composite; the field's own route (a tested
  rate scaled to hours or clinker) never asks for the inputs at all.
- **Reflex:** the field's method for a kiln's annual mercury where no continuous monitor runs, the accredited test's
  mass rate carried over the kiln hours (or per tonne of clinker over the year's clinker), is rung 0 and files the
  works at about 70 kg, under the 85 kg load, with no abatement.
- **Back-test:** the textbook route validates: the three annual tests agree on each stack within about 9 per cent
  (kiln 1 4.37, 4.06 and 3.99 g/h; kiln 2 4.83, 4.63 and 4.83 g/h), every run is far under the 50 ug/Nm3 limit, and
  the per-clinker and per-hour scalings agree within a kilogram; nothing in the pack refutes the tested rate.
- **Second use:** the ledger carries the clinker and hours the default path scales by and the annual report's
  tonnages; the laboratory's composites carry every oxide and fuel figure the works reports; the register maps
  emission points to kilns for the NOx ask; the historian, journal and logger carry the hours and NOx asks; delete
  the decisive step and every file is still in the pack.
- **Shock:** nothing moves: the release is a balance of the year's own ordinary inputs; no month, input or kiln is
  the pack's largest anomaly (shale and fly ash carry the most mercury because they carry the most clay minerals),
  and the raw mill stops are routine silo-full stops, trips and Tuesday maintenance spread through every month.
- **Pins:** licence condition 5.6 files the WHAT (the mass released over every hour each kiln fires, in compound
  operation and in direct operation, both kilns together, a calendar year, against 85 kg) and 1.4, 1.5, 1.7 define
  the terms; no sentence names a balance, a capture, the raw mill's effect on mercury, the dust, or a test's
  representativeness.

## Default path

1. Read licence condition 5.6 for the quantity and the 85 kg load, and the register for which stack is which kiln.
2. Take the 2026 test report for each stack in stack_tests_Hg_2024-2026.pdf: the mean of the three runs' mercury
   mass emission, 3.99 g/h on A1-1 (kiln 1) and 4.83 g/h on A1-2 (kiln 2), each at the licence's reference conditions
   and below the 50 ug/Nm3 limit.
3. Count each kiln's 2026 hours on feed from the journal (or the historian's feed rate): the quarters' figures sum to
   7,941 and 8,037.
4. Carry the tested rate over the hours: kiln 1 31.7 kg, kiln 2 38.8 kg (per tonne of clinker: 31.3 and 38.4 kg;
   three-year mean rate: 32.9 and 38.3 kg).
5. Compare the works' total with the load.

Ends on: 70 kg for the works, 15 kg under the 85 kg load, no carbon injection
Golden: 151 kg for the works (kiln 1 68 kg, kiln 2 83 kg), 66 kg over the load, carbon injection needed

## Stump sentence

A competent analyst carries each stack's 2026 tested mercury rate over its kiln's hours on feed and files the works at
70 kg, under the 85 kg load, with no carbon injection; the step that lands it there is taking a rate every test
measured with the raw mill running as the year's, when condition 5.6 counts the hours with the mill stopped too and
the year's release is the mercury the kilns took in with their raw materials and fuels less what left in clinker and
in the filter dust kiln 1 bled to silo S7: 68 kg and 83 kg, 151 kg, 66 kg over.

## Three rules

- **Task type:** physical-environmental-sciences / emissions-inventory, which serves Data Extraction & Conformation:
  the works' inventory of mercury to air is conformed from five systems' records into the licence's quantity.
- **Domain test:** the deciding quantity is each kiln's mass of mercury released to air in 2026, which an inventory
  for a cement works without a continuous mercury monitor estimates from its periodic stack tests scaled to the
  kiln's operating hours or its clinker.
- **Swap:** "whether the hospital keeps under its annual load if it releases what it released in 2026" with wards for
  kilns: nothing in a hospital cycles a volatile element between a grinding mill and a furnace so that the measured
  state and the year's release part company, and no grinding mill stops for a full silo; the call stops meaning.
- **Layer 1:** the ledger's layout and item names change at July (Production Accounting's new template); the
  laboratory reports raw materials on the dry basis and fuels as received, with sand and slag composited by quarter;
  the ledger's second half carries a clinker-to-cement-mills transfer row beside clinker made; the historian stamps
  half-hours in UTC and has a nine-day hole from the May server migration; the journal is in Irish local time with
  the two clock changes logged; the CEMS logger exports interval ends in local time with semicolons; the weighbridge
  has void tickets and reprints; each written by the system named, none placed to be caught, each neutral on the
  call (R2a to R2g in checks.py).
- **Layer 2:** estimand identification over a measurement that covers one operating state: the field's tested rate
  is right for compound operation and the year is not compound operation; the year's release is identified by
  conservation of the element through the kiln line, which needs no model of the stopped-mill rate.
- **Decisive step:** recognising that the year's release is fixed by what the kiln line took in and what left it by
  its other exits (clinker and filter dust taken out of the system), and building that balance from the ledger's
  monthly tonnages and the laboratory's composites.
- **Not semantics:** every field read correctly (the reference conditions, the raw mill in operation in every run,
  the dry and as-received bases, the ledger's names, the emission points) still leaves the easy route on 70 kg,
  because no field says the tested rate does not hold with the mill stopped and no field holds mercury to air.
- **Not rule application:** no filed rule or procedure computes the release: condition 5.6 names the quantity and
  the hours it covers and no method. Enumerated family: tested rate times kiln hours 70.5 kg, per tonne of clinker
  69.7, three-year mean rate 71.2, the balance without the dust 162.7, the balance with moisture taken off dry
  tonnes again 141.4, the balance 151.1 (and its annual-mean, silo-stock and shipped-dust readings 150.9 to 151.3).
  Standing family (what the data and 5.6 leave defensible): the balance and its readings, 150.9 to 151.3, all 151;
  the tested-rate routes stand outside it because 5.6 counts the stopped-mill hours the tests never covered and the
  balance shows 80 kg the tests do not. The ruling-out is quiet: two sentences of 5.6 and the tests' process tables.
- **Analyst test:** a strong analyst who reads every field and condition correctly takes each stack's 2026 tested
  rate, carries it over the kiln hours, and files 70 kg for the works, 15 kg under the 85 kg load, with no carbon
  injection; the golden is 151 kg, 66 kg over.
- **Estimand:** licence condition 5.6 in IEL-1186-03_conditions_consolidated_2026.pdf: the mass of mercury released
  to air from emission points A1-1 and A1-2 together in a calendar year (1.7, Irish local time), over every hour each
  kiln fires, in compound operation and in direct operation (1.4, 1.5), against 85 kg; the prompt fixes 2026's
  release as the comparison ("if it releases what it released in 2026") and asks the margin in kilograms.
- **No decoy:** nothing is planted to be caught: no memo, draft, briefing or stakeholder figure ships; the stack
  tests are correct for the conditions they were run in and say so; no prior-year annual report or computed annual
  mercury figure ships; the weighbridge, fuel receipts and quarry log are declared distractors that answer other
  questions.
- **No certified replay:** no certified or published mercury figure for any year ships, so the method is not
  recovered by reproducing a control; the tests certify a concentration and a rate for their own runs only.
- **Lesson:** a measurement made in one operating state is not the year's release when the unit spends part of the
  year in another state that changes where the substance goes; where every input and every other exit is measured,
  conservation over the year fixes the release without modelling the unmeasured state. No build on file teaches it:
  the corpus's samplings are fixed by a covariate relation (task452 v1) or a sampling design (v2), never by
  conservation through the unit.

## Readability screen

Seven tests per rung: filed sentence, schema, reflex, control bench, hygiene, linear, dedicated organ.

| Rung | What it does | Tests that fire | Verdict |
|---|---|---|---|
| R0 tested rate x kiln hours | the field's reflex for a kiln without mercury CEMS | reflex (it is the field's named method) | readable |
| R1 per tonne of clinker, three-year mean | the reflex's own variants | reflex | readable |
| R2 the 2026 tests' process tables | reads that every run had the raw mill in operation | schema (the tables say it) | readable |
| R3 (decisive) the year's balance: inputs less clinker less dust | conservation over the kiln line, from ledger and composites | none: no sentence names a balance or the mill's effect; the inputs' mercury is one column among fifteen oxides in a composite sheet the field's route never opens; nothing reconciles the tested rate to anything; no hygiene check flags it; it is a sum over two files joined by a worked-out crosswalk, not one column; the ledger and laboratory are in the pack for every other figure | silent |
| R4 the dust term | kiln 1's filter dust to silo S7 removes 11.6 kg | none beyond R3's: the ledger row is a by-product line among twenty | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "released to air" (5.6) | every hour each kiln fires, compound and direct | the tested compound-operation rate for every hour | 70 kg, under | 5.6's "in compound operation and in direct operation" against every test run "in operation" (D5; asserted SF1) |
| SF2 | calendar year | 1 January to 31 December, Irish local time | UTC year | same call | 1.7; Irish winter time is UTC, so both years are one (asserted) |
| SF3 | each kiln | A1-1 is kiln 1, A1-2 kiln 2 | stacks swapped | same call (works total) | site register (asserted) |
| SF4 | a month's composite | each month's composite on each month's tonnage | annual mean composite on annual tonnage | same call, same figures (67.8, 83.1, 150.9) | asserted SF4 |
| SF5 | the meal silo | stock change ignored (no meal analysis) | stock change times the mix's mercury | same figures (68.0, 83.3, 151.3) | asserted SF5 |
| SF6 | dust out of kiln 1 | ledger's filter dust to silo S7 | weighbridge tickets shipped | same figures (67.9, 151.1) | asserted SF6 |
| SF7 | clinker in the second half | Clinker made | Clinker to cement mills | same figures | asserted SF7 |
| SF8 | works total rounding | the sum rounded once | the kilns rounded then summed | 151 both | asserted SF8 |
| SF9 | keep under | 151 against 85 | at or under, strictly under | same call | 66 kg clear (asserted SF9) |
| SF10 | the comparison | the 2026 release itself | a projection to 2028 | not licensed | the prompt's "if it releases what it released in 2026" (asserted SF10) |
| SF11 | composite basis | dry for raw materials and clinker, as received for fuels | moisture taken off again | not the golden (141.4), a misread | the composites' own Basis column (asserted SF11) |
| SF12 | quarterly composites | the quarter's composite on each month | the first month only | same figures | asserted SF12 |
| SF13 | "hours" in the asks (1.4, 1.5, 6.5) | elapsed time summed: direct 1,391.9 and 1,731.2, on feed 7,940.1 and 8,036.6 | a count of clock hours: direct 1,509, 1,223 or 1,396 (kiln 1) and 1,863, 1,551 or 1,729 (kiln 2) as any, full or majority hours | different figures | licence 1.8: elapsed time from start to end of each period, summed, not a count of clock hours (asserted SF13) |
| SF14 | the fuels' mercury | the laboratory's as-fired composites | the suppliers' certificates, by month (coal: the cargo in use), as a tonnage-weighted or plain annual mean | same figures: 67.9, 83.2 and 151.1 to 151.1 kg under each (asserted SF14) | convergence by construction: each certificate describes the fuel the composites describe |

## Ladder

| Rung | Construction | Kiln 1 kg | Kiln 2 kg | Works kg | Call |
|---|---|---|---|---|---|
| R0 | 2026 tested rate x hours on feed (7,941 and 8,037 h, the quarters summed) | 31.7 | 38.8 | 70.5 | under by 15 |
| R1a | tested rate per tonne of clinker x 2026 clinker | 31.3 | 38.4 | 69.7 | under |
| R1b | three-year mean tested rate x hours | 32.9 | 38.3 | 71.2 | under |
| R2 | balance without kiln 1's dust | 79.5 | 83.2 | 162.7 | over by 78 |
| R2b | balance with moisture taken off dry tonnes | 61.2 | 80.2 | 141.4 | over by 56 |
| Golden | balance: inputs 80.8 and 84.1 kg, less clinker 1.3 and 0.9, less kiln 1's dust 11.6 | 67.9 | 83.2 | 151.1 | over by 66 |

Margins: the golden sits 0.43, 0.31 and 0.38 kg inside its whole-kilogram bins; every defensible reading
(SF4 to SF7, SF12) lands in the same bins (asserted). The decisive step is worth 80.6 kg against a standing spread
of 0.4 kg. Cheap routes to the call: one (the balance); R0 and its variants all file under.

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | both kilns' stacks, every hour each fires | filed 5.6; C1 |
| 2 Unit of account | kilogram of mercury per kiln and for the works | the prompt; C1 |
| 3 Attribution window | calendar 2026, local | 1.7; ledger months are calendar months; C1 |
| 4 As-of dating | the ledger and composites as issued in January 2027 | one vintage ships; C1 |
| 5 Version basis | one ledger, one composite set | C1 |
| 6 Denominator | none (a mass) | not applicable, C1 |
| 7 Weighting | monthly tonnage times monthly composite | C1 against annual means (SF4) |
| 8 Window length | the calendar year | 5.6; C1 |
| 9 Boundary inclusivity | months whole | C1 |
| 10 Rounding path | each kiln and the works rounded from unrounded sums | C1 (SF8) |
| 11 Tie-break | none | not applicable |
| 12 Maturity and censoring | the year is closed and every composite issued | C1 |
| 13 Order of operations | sum then subtract | commutes; C1 |
| 14 Row order | none | C1 |
| 15 Duplicate resolution | weighbridge reprints and voids (distractor file only) | C1: the call never reads it (S3) |
| 16 Identity normalisation | ledger names to composite codes | one-to-one crosswalk (R2a) |
| 17 Netting against gross | exits subtracted from inputs | 5.6's "released to air"; C4 against the no-dust rung (SF6) |
| 18 Dimensional units | tonnes times mg/kg on one basis | the Basis column (SF11) |
| 19 Code and status semantics | mill START, STOP, TRIP; FEED ON and OFF; MAIN BURNER TRIP | asks only; the journal's own words |
| 20 Integerisation | whole kilograms, whole hours, whole tonnes | the prompt's rounding sentence; C1 |
| 21 Clause scope | 5.6 for the call; 6.4 and 6.5 for the hours and NOx | filed scope |
| 22 Forward window contents | none: the comparison is the 2026 release | the prompt; SF10 |

## Literal reader

Executed word for word: the prompt asks whether the works keeps under 85 kg "if it releases what it released in
2026"; 5.6 makes that the mass released over every hour each kiln fires, in compound operation and in direct
operation; the tests say each run was made with the raw mill in operation; the journal shows both kilns ran with the
mill stopped for 1,392 and 1,731 hours. A literal reader therefore cannot take the tested rate for every hour without
an estimate of the stopped-mill hours, and the only estimate the shipped records support is the year's balance,
which already counts every hour: 68 and 83 kg, 151 kg, 66 kg over. The default's inputs do not comply with 5.6 on a
literal reading (they price direct-operation hours at a compound-operation test). Every alternative reading in the
fork table either prints the same figures or violates a quoted sentence.

## Oracles

None ships. The tests certify their own runs only; no annual mercury figure, prior-year report or reconciled control
exists in the pack. The NOx ask's two sources (historian and logger) overlap for about four days on purpose of the
systems' export windows, not as a referee: they disagree in level because they report different oxygen bases.

## Ask sheet

H18 homes: every ask is part of the annual environmental report under 6.4 and the abatement case (the carbon
injection's sorbent use is sized on direct-operation hours), and none is computed over the call's rows (the call
reads the ledger and the laboratory only; asserted S3 with the historian, journal, logger and tests deleted).

- **Ask 1, hours in direct operation by quarter (8 figures, whole hours).** Golden from DCS_event_journal_2026.txt:
  on feed (FEED ON until FEED OFF or MAIN BURNER TRIP) with the raw mill stopped (STOP or TRIP until START), from the
  start-of-log states, local time, the repeated hour of 25 October after the logged clock change: kiln 1 288, 345,
  379, 380; kiln 2 352, 452, 469, 458. Primary device: unplanned kiln stops are logged as MAIN BURNER TRIP with no
  FEED OFF line (the interlock stops the feed), found only by FEED ON following FEED ON; read as no stop, every
  quarter moves 5 to 92 hours. Second device: the historian's raw mill status is the value at each half-hour stamp,
  so its route misses every quarter by 2 to 8 hours, and its May hole by more. Hazard: the clock change (kiln 1 Q4 by
  one hour). Pin test: 1.5 and 6.4 file the WHAT (producing clinker with the raw mill stopped); neither names the
  journal's vocabulary. Realism: interlocked trips log their cause, not each consequence.
- **Ask 2, hours on feed by quarter (8 figures, whole hours).** Golden from the same rebuilt state: kiln 1 1,542,
  2,107, 2,116, 2,176; kiln 2 1,637, 2,168, 2,126, 2,106. Primary device: the burner trips (every quarter 5 to 92
  hours over). Second device: the historian's feed rate at half-hour grain with the May hole pro-rated (Q2 off by 1 to
  8 hours; Q1, Q4 land within a half-hour). Pin test: 6.5 files hours of operation as hours producing clinker.
- **Ask 3, NOx to air (2 figures, whole tonnes).** Golden: the historian's half-hours, each 10 per cent oxygen
  concentration restated to the measured oxygen times the dry flow, plus the logger's half-hours for the historian's
  May hole only, the logger already at measured oxygen: kiln 1 932 t, kiln 2 605 t. Primary device: the logger's
  basis differs from the historian's (read on the historian's basis: 936 and 607). Second device: the overlap (the
  logger appended whole: 944 and 612). Hazards: the 10 per cent basis itself (unconverted 828 and 550), the hole
  pro-rated (926 and 601).

Main population zero-counts: no device row in the ledger's tonnage rows or the laboratory's mercury column the call
reads (the clinker-transfer row is a hazard beside the population, inert on the call, SF7).

| Ask | Cracker figures (careful route: journal FEED lines, start-of-log, mill TRIP, clock change; logger found and read on the historian's basis) | Golden | Verdict |
|---|---|---|---|
| Ask 1 direct hours | kiln 1 293, 403, 447, 407; kiln 2 358, 459, 537, 550 | 288, 345, 379, 380; 352, 452, 469, 458 | miss |
| Ask 2 hours on feed | kiln 1 1,547, 2,184, 2,208, 2,209; kiln 2 1,643, 2,184, 2,208, 2,209 | 1,542, 2,107, 2,116, 2,176; 1,637, 2,168, 2,126, 2,106 | miss |
| Ask 3 NOx | 936, 607 | 932, 605 | miss |

The historian route (a second careful route) keeps 3 of 18 ask figures (Q1 and Q4 hours on feed). A full includer
who reads the burner trip as the feed stop and the logger on its own basis keeps every ask figure; the ask layer's
hold rests on those two judgments.

Pair ceiling: 26.0 (journal route; 35.2 on the historian route), the cracker 45.0 on the call with no ask kept and
the mirror 7.0 off it
Mirror leakage: 0.0 per cent of ask weight on the journal route (16.7 on the historian route)
Measured by: generator/ceiling.py, run on the cut pack


## Leak check

`leak.py task452 --asof 2027-01-11` on the final cut: REVIEW, no LEAK. Each REVIEW line answered:
- DCS_event_journal_2026.txt is a text file: it is the control system's own alarm and event journal (an operator
  station export with its own header line and the station's time base), not a description of the data.
- IEL-1186-03_conditions_consolidated_2026.pdf carries 9 of the swept terms: they are the licence's own words
  (reference conditions, reporting, emission points, period) and the sweep also read architecture 2's record; no
  sentence names a balance, the raw mill's effect on mercury, the dust or a test's representativeness.
- stack_tests_Hg_2024-2026.pdf carries 7 of the swept terms (reference, report, emission, laboratory, clinker,
  monitoring): a test report's standard vocabulary; it states each run's conditions and ranks nothing.
- Sweeps 2, 3, 5 to 9 and 11 clean; the container sweep finds no writer signature (producers scrubbed per issuing
  body in build.py).

## Architecture 2 record

Architecture 2's note as it stood when it shipped on 2026-10-14 (headings demoted one level).

### task452 design note (architecture 2 title)

Architecture 2 (re-rooted 2026-10-14 at the author's request for a stronger stump). Architecture 1 (tributary phosphorus loads by a concentration-discharge rating curve) shipped 2026-10-13 and is in the card's lineage and in `## Tried and rejected`: its decisive step is the field's standard load method, which careful solvers apply.

### Draw

- **Card:** `.claude/skills/fingerprint/cards/task452.json`, architecture v2, registered 2026-10-14 (guard WARN only: overuse.objective, overuse.gate_g, repeat.decision, repeat.question_form, answered below; v1, task459, task230, task448, task133, task255, task253 and task139 differentiated on the card).
- **Pairing:** Physical & Environmental Sciences / emissions-inventory / Data Extraction & Conformation (ETL). An emissions inventory's land-use sector rests on activity data: the area of forest converted in the period, estimated from a change map and a reference sample interpreted on high-resolution imagery. Here a university forest monitoring laboratory conforms two interpretation campaigns into one reference dataset on the national forest definition and the reporting period, estimates the 2024-2025 deforested area from it, and turns it into the emission reductions a results-based payment agreement pays for.
- **Shape:** other, with the arithmetic: the tonnes offered and the payment (2), the area of deforestation they rest on (1), its 90 per cent confidence interval (2), each district's area (12), the final map's deforestation patches by district in three counts (all, under 1 ha, 5 ha or more: 36 and 3 totals), the conformed reference sample (2), the report's chart (4) and the two files (2): about 64 criteria before the generated rubric selects. The call is one amount (the tonnes the program can offer and what they bring), which no numbered shape carries with a conformed reference dataset beside it. It is retrospective by the agreement's design: a results-based payment pays on a closed reporting period's monitored results, and the payment itself is still to come.
- **Strategy:** population_selection (who each reference point stands for). The 4,000 reference points were drawn in January 2026 by stratified random sampling on the preliminary 2024-2025 change map; the final map, reprocessed in April with radar and late-season imagery, removed most of the preliminary map's cloud-shadow false alarms and some true clearings. Each point's inclusion probability is fixed by the preliminary stratum it was drawn from, so the area is estimated on the sampling strata (each point weighted by its stratum's area over the stratum's sample size), and the final map, which the monitoring report presents, cannot supply the strata.
- **World:** a fictional Spanish-speaking tropical country's lowland forest emission reductions program (about 11.8 million hectares, six million of them forest), its ministry of environment, the university forest monitoring laboratory that prepares the program's monitoring report under contract, and a results-based climate fund's trustee. The payment agreement pays USD 5 per tonne of CO2e of emission reductions for the 2024-2025 reporting period: the reference level's emissions for the two years less the program's monitored emissions from deforestation, each the deforested area times the reference level's emission factor, less a buffer of 18 per cent set aside against reversals. The reference level (2015-2022, approved) is 89,950 hectares of deforestation a year at 497 tCO2e per hectare; the period's true deforestation runs about a third below it. The monitoring report is due 30 June 2026; the extract is dated 22 May 2026. No real agency, fund, program or country is named.
- **Forum and forcing event:** funder_or_donor (the fund's trustee pays on the monitoring report), purchase_order_or_contract (the payment agreement's reporting date). Organisation university_or_school, role field_unit_lead (the head of the university forest monitoring laboratory). Personas from `guard.py names --geo "Mexico" --seed 452`: Lilia Solano, César Verduzco, Raquel Saavedra.
- **Data-native sentence:** the reference points were drawn on the preliminary change map three months before the final map, so the 400 points drawn from the preliminary map's deforestation class each stand for about 300 hectares and a stable-forest point for about 2,500, and when the final map moved most of the preliminary false alarms, and some real clearings, into stable forest, those lightly weighted points went with them into a class whose own points weigh eight times more.
- **Sources, one line each:**
  - `stumping/references/client/two-layer-task-design.md`, estimation_fit (weighting and post-stratification; the estimator follows the design): here the design is a stratified sample whose strata are a map revised after the draw, and the estimator must follow the strata the sample was drawn on.
  - `stumping/references/client/layer2-rigor-patterns.md`, census-register-administrative-data-quality 1 (estimates within the strata the design defines, not pooled) and data-integration-record-linkage 1 (propagate classification error to the estimate): the nearest library patterns; no emissions-inventory pattern is listed, and this build's move is design-based area estimation from reference data, the land-use inventory's own activity-data method.
  - `stumping/references/strategies.md` Part 6 (every reflex lands wrong): the final map's area, the map corrected by its user's accuracy, the error matrix on the final map's classes and the sample's raw proportions each file a named wrong amount.
  - `dataset-generation/references/layer1-messiness.md` (two export layouts, legends against a definition, pixels against hectares, renumbered codes): the Layer 1 here, none of it on the decisive step.
  - `supplemental-stumping` Part 3 (the device book): D6, an event's quantity on every line it covers (a patch's area on each polygon that delivers it, by tile and by quarter of first detection), with D1's over-cleaning half (distinct patches share an area of whole pixels, so deduplicating on it deletes real patches), for the change-map ask.
- **Same-puzzle and abstraction:** decisive gap population, generator G9 and Gate G method_or_model_selection clear the twelve-build window; the older signature task139 (an intervention read per assigned unit, not per surviving recorded case) is differentiated on the card. The abstraction test against the nearest drivers (task253 lineage 0.07, a population count from a sample whose response rate varies by frame; task95, task37, task69 at 0.05): none weights a probability sample by strata that a later revision of the stratifying map no longer shows.
- **Guard WARN overuse.objective:** the slot is in the author's ETL lane (task445 to task493).
- **Guard WARN overuse.gate_g (method_or_model_selection):** the stump is which estimator the design forces; no other key is honest.
- **Guard WARN repeat.decision (quantity_figure) and repeat.question_form (how-much):** the call is an amount of emission reductions and the payment it brings; a designation or a pick would misstate it.
- **Forced parameters:** 4,000 reference points over 11.8 million hectares (a large national sample, as results-based programs fund); the preliminary map's false alarms (about 0.6 per cent of stable forest, cloud shadow and leaf-off) and omissions (about two clearings in five) sit within what preliminary tropical change maps show; the draw (seed 54533) is the one of 60,000 searched on which every design-consistent implementation reports the same hundred hectares and no district sits within 10 ha of a hundred-hectare edge.

### Default path

1. Conform the main interpretation campaign and the quality-control re-interpretation (the adjudicated label where the two disagree) into one reference class per point on the national forest definition and the reporting period: deforestation 2024-2025, stable forest or non-forest.
2. Assess the final 2024-2025 change map, the map the monitoring report presents, against the reference points: build its error matrix on the final map's classes and estimate the deforested area by the stratified estimator of good practice, each final class's mapped area times the share of its points that are deforestation: 171,581 hectares, 171,600 as reported.
3. Monitored emissions: 171,600 hectares at 497 tCO2e per hectare, 85.3 MtCO2e, against the reference level's 89.4 MtCO2e for the two years: 4,125,100 tonnes of emission reductions.
4. Offer them less the 18 per cent buffer: 3,382,582 tonnes, for USD 16,912,910.

Ends on: 3,382,582 tonnes offered for USD 16,912,910 (a deforested area of 171,600 hectares, 8,300 under the reference level's 179,900 for the two years).
Golden: 23,229,780 tonnes offered for USD 116,148,900 (a deforested area of 122,900 hectares, 28,329,000 tonnes of emission reductions before the 18 per cent buffer).

### Stump sentence

The default path offers 3,382,582 tonnes for USD 16,912,910 because step 2 estimates the deforested area with the textbook stratified estimator on the final map's classes (171,600 hectares, only 8,300 under the reference level's 179,900 for the two years): the reference points were drawn on the preliminary map, and the final map moved 124 of the 400 densely sampled points of the preliminary deforestation stratum, false alarms and 21 real clearings alike, into stable forest, where the estimator weights each of them at 2,367 hectares instead of the 329 its stratum gives it; the final map's own area (73,200 hectares) understates the other way and offers 43,484,518 tonnes; the stratified estimator on the strata the sample was drawn from gives 122,900 hectares and 23,229,780 tonnes to offer for USD 116,148,900.

### Three rules

- Task type: Physical & Environmental Sciences, emissions-inventory (the land-use sector's activity data: the reporting period's area of forest converted to other land, estimated from a reference sample interpreted on high-resolution imagery), which serves Data Extraction & Conformation.
- Domain test: the quantity that decides the call is the reporting period's area of deforestation, the inventory's activity data, estimated the way the land-use sector estimates it from a probability sample of reference points: the design-based stratified estimator, each point standing for the area of the stratum it was drawn from over the points drawn there, with the stratified sampling variance for its 90 per cent interval; the area then becomes monitored emissions through the reference level's emission factor and emission reductions against the reference level.
- Swap: "the deforested area the reference sample shows, which sets the tonnes the program offers" with hospital nouns reads "the readmissions a chart-review sample shows, which sets the penalty the hospital pays", and the wall-to-wall change map whose mapped class areas weight its own accuracy sample, the preliminary and final versions of that map, the forest definition's canopy threshold and the reference level's emission factor have nothing to attach to: no hospital measure is a classification of every hectare whose class areas a reviewer multiplies by the sample's class shares, so the choice between the map that drew the sample and the map that replaced it stops making sense.
- Layer 1: the laboratory's two interpretation campaigns export different layouts (the main campaign from the laboratory's tool, land-cover codes 1 to 8 and canopy classes A to D; the ministry's quality-control re-interpretation of one point in five, exported from its form tool as JSON records with Spanish labels, canopy bands and "LFM26/" point ids), the adjudication log settles only the fields the two recorded differently, the interpreters' legend carries plantations and 10 to 30 per cent woodland that the national forest definition excludes, remarks note clearings of 2021 to 2023 on land that was pasture in January 2024, the points carry the 2019 district codes while the final map's statistics and polygons carry the 2025 layer (La Esperanza split into La Esperanza and Nueva Esperanza), and map areas come from pixel counts on the 30 m grid; each is what the laboratory's and the ministry's systems write, and none is placed to be caught.
- Layer 2: field_method, the land-use sector's design-based area estimation: the estimator follows the sampling design, so a point drawn from the preliminary map's deforestation stratum stands for 329 hectares whatever class the final map later gives it.
- Decisive step: estimating the area of deforestation on the strata the reference sample was drawn from (each point weighted by its preliminary stratum's area over the points drawn there: 329 hectares in the deforestation stratum, 2,469 in stable forest, 4,785 in non-forest) rather than on the classes of the final map the report presents, whose error matrix weights the 124 points the final map moved from the preliminary deforestation stratum into stable forest, 21 of them real clearings, at 2,367 hectares each.
- Not semantics: with every field, code, unit and definition read correctly (the forest definition, the reporting period, the adjudication, both district layers) the easy route still files 171,600 hectares and 3,382,582 tonnes; no field or definition names a point's weight, and the error lies in which strata the estimator uses.
- Not rule application: the payment agreement and the monitoring plan fix what is estimated (the area of deforestation in the accounting area in the reporting period, from the reference sample, a probability sample, stated to the nearest hundred hectares) and the arithmetic after it; no filed rule or procedure says how the points are weighted, and executing every stated rule on the final map's error matrix files 3,382,582 tonnes.
- Analyst test: a strong analyst who conforms both campaigns and the adjudication on the national forest definition and the reporting period correctly, and executes every article of the payment agreement, assesses the final change map against the reference points (the monitoring plan's 4.2: the report presents the final map with its accuracy assessment) and estimates the area from its error matrix with its mapped class areas, the stratified estimator of good practice: 171,581 hectares, 171,600 as stated, only 8,300 under the reference level's 179,900 for the two years, so 3,382,582 tonnes offered for USD 16,912,910 (the default path's Ends on); the final map's own area (73,200 hectares, 43,484,518 tonnes) misses the other way, and neither is the 23,229,780 tonnes the design gives.
- Estimand: the payment agreement's article 4(2) (`emission_reductions_payment_agreement_extract.pdf`): the area of deforestation in the Accounting Area in the Reporting Period, as the monitoring report states it to the nearest hundred hectares; the monitoring plan's 4.1 (`monitoring_plan_extract.pdf`): estimated from the reference sample, a probability sample of points in the accounting area classed on section 3's definitions; the population the twelve lowland districts on the 2019 layer (3.3), the outcome land that is forest on 1 January 2024 and other land on 31 December 2025 (3.2), the window 2024-2025, the unit hectares to the nearest hundred, the comparison the reference level's 89,950 hectares a year for the two years (article 2).
- No decoy: nothing is planted: no memo, briefing, draft or stakeholder figure states an area, a weight, a number of tonnes or a payment; the final map's statistics give its class areas as mapped and the release note says what the reprocessing changed, both true; the forest inventory's tree measurements and the fire hotspots are relevant distractors carrying no deforestation estimate.
- No certified replay: no certified or published figure reproduces only under one method; the reference level and the emission factor are filed values that no route reproduces from the sample, and the method is left to the design.
- Lesson: a model learns that a probability sample is estimated by the design it was drawn under: when the map that stratified a reference sample is revised after the draw, each point keeps the weight of the stratum it was drawn from, and the final map's error matrix with its own class areas, the textbook area estimator, misweights the points the revision moved; no build on file teaches design-based area estimation from a stratified reference sample or a stratifying map revised after the draw (task253's frame-dependent response rates, task230's net classification bias and task139's per-assigned-unit reading are differentiated on the card).

### Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the final map's own deforestation (73,200 ha, 43,484,518 t) | the plan's 4.1 says the area is estimated from the reference sample | the statistics workbook's deforestation column | yes: the map the report presents read as the activity data | no | no | yes: one column summed | readable |
| R0' the preliminary map's deforestation stratum (131,500 ha, 19,724,936 t) | the design report states the stratum's area | the design table | yes: the stratum's area read as the deforestation | no | no | yes | readable |
| R1' the final map's area times its user's accuracy (60,700 ha, 48,578,768 t) | no | the points' final map class beside their reference class | yes: correct the map for its commission error | no | no | yes: one product | readable |
| raw share of the points times the accounting area (660,800 ha, no reductions) | no | the points file | yes: a sample proportion scaled up | no | no | yes | readable |
| R1 (default) the error matrix on the final map's classes, its mapped class areas as weights (171,600 ha, 3,382,582 t) | the plan's 4.2: the report presents the final map with its accuracy assessment, which names no estimator | the points' final map class and the final map's class areas | yes: the good-practice area estimator on the map being assessed (the default path) | no | no | no | readable |
| R3 (decisive) the stratified estimator on the strata the sample was drawn from (122,900 ha, 23,229,780 t) | no: the design report states the strata of the draw, their areas and the points drawn, and the plan the estimand; no document names a weight, an inclusion probability or an estimator, or says the final map cannot stand in for the strata | no: the stratum label and the final map class sit side by side in the bundle and neither says which stratifies the estimate | no: the reflex on a revised map is the version that replaces it (the release note: "Version 2.0 replaces the preliminary version 0.9") | no: no published or certified figure ties to the area | no: the battery checks keys, duplicates and joins, never the weights | no: the weights come from the design table and the points drawn in each stratum | silent |

### Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the Reporting Period | 1 January 2024 to 31 December 2025, two years: reference level emissions 89,410,300 t | one year (44,705,150 t) | another call (none) | the agreement's articles 1 and 2 |
| SF2 | the area as the report states it | to the nearest hundred hectares (122,900), then times the factor | the unrounded 122,882.7 ha | another amount (23,236,830 t) | the agreement's article 4(2) |
| SF3 | the tonnes the Ministry may offer | the reductions less 18 per cent, in whole tonnes, any fraction dropped | rounded to the nearest tonne | same call: 28,329,000 times 0.82 is whole (asserted) | the agreement's article 5 |
| SF4 | the payment | USD 5.00 for each tonne offered | for each tonne of reductions before the buffer (USD 141,645,000) | another payment | the agreement's article 6 |
| SF5 | the area of deforestation | the reference sample's estimate | the final map's mapped deforestation (73,200 ha, 43,484,518 t) | another call | the plan's 4.1 |
| SF6 | deforestation in the period | forest on 1 January 2024 and other land on 31 December 2025 | any clearing the interpreters note, the remarks' 2021 to 2023 clearings included | same call: those points were pasture in January 2024 (asserted) | the plan's 3.2 |
| SF7 | forest | 0.5 ha or more, canopy cover of 30 per cent or more, plantations excluded | plantations counted, or a 10 per cent canopy threshold | same call: plantations and woodland are stable over the period (asserted) | the plan's 3.1 |
| SF8 | the 90 per cent confidence interval | of the estimate, to the nearest ten thousand hectares: 100,000 to 140,000 | z 1.645 or 1.6449, n or n - 1, t with 3,997 degrees of freedom, centred on the stated 122,900, post-stratified to the final map with the design weights | same interval under all five (asserted, each bound 1,000 ha or more from an edge) | the plan's 4.3 and the prompt's rounding |
| SF9 | each district's area to the nearest hundred | the golden figures | the unrounded sums | same: every district 10 ha or more from a hundred-hectare edge (asserted, closest 12.4) | the prompt's rounding |
| SF10 | the accounting area | the twelve lowland districts on the 2019 layer | the whole country (the final map covers the highland districts too) | same call: every reference point is in the twelve (asserted) | the agreement's article 1 and the plan's 3.3 |
| SF11 | each district's area of deforestation | the part of the accounting area's estimate contributed by the reference points in the district | the district's land area times its points' weighted share of deforestation (a ratio estimator) | another figure in all twelve districts (asserted) | the plan's 4.5 |
| SF12 | each district (the patch counts and the chart) | the twelve districts on the 2019 layer, La Esperanza with Nueva Esperanza (LT-05 and LT-06) | the 2025 layer's thirteen districts | another count for La Esperanza | the plan's 3.3 and the concordance |
| SF13 | a deforestation patch | the connected area of change on the national mosaic, whose area each of its polygons carries (patch_ha), counted once | a polygon | another count in every district (asserted) | the dictionary's patch_ha and the polygon file's grain (by tile and by quarter of first detection) |
| SF14 | under 1 hectare; of 5 hectares or more | the patch's area (patch_ha) | the polygon's own area; the boundary on either side | the polygon's area: another count; the boundary: same call (no patch measures 1.00 or 5.00 ha, asserted) | the dictionary's patch_ha |
| SF15 | the totals | the accounting area's twelve districts | the country, the highland districts included | another total | the concordance's accounting_area and the plan's 3.3 |
| SF16 | a point's reference class | the main campaign with the adjudicated fields applied | the main campaign alone; the quality-control labels wherever they exist | same call (asserted from the shipped exports) | the plan's 4.4 and the design report's section 4 |

### Ladder

As built on the seed (`generator/checks.py` asserts every rung by name; `verify.py` recomputes the golden from the bundle alone).

| Rung | Method | Area stated (ha) | Tonnes offered | Payment (USD) | Dies to |
|---|---|---|---|---|---|
| R0 | the final map's own deforestation | 73,200 | 43,484,518 | 217,422,590 | the plan's 4.1 (the area is estimated from the reference sample); 45 of the 224 deforestation points lie outside the final map's deforestation class |
| R0' | the preliminary map's deforestation stratum | 131,500 | 19,724,936 | 98,624,680 | the plan's 4.1; 199 of its 400 points are not deforestation |
| R1' | the final map's area times its user's accuracy (179 of its 216 points) | 60,700 | 48,578,768 | 242,893,840 | the clearings the final map left in stable forest and non-forest |
| raw | the points' share of deforestation times the accounting area | 660,800 | none | none | the draw: a point of the preliminary deforestation stratum was about fifteen times likelier to be drawn than a non-forest one |
| R1 (default) | the error matrix on the final map's classes, its mapped class areas as weights | 171,600 | 3,382,582 | 16,912,910 | the design: the 124 points the final map moved out of the preliminary deforestation stratum's class (21 clearings among them) stand for 329 ha each, not the 2,367 the stable-forest class gives them |
| R3 (golden) | the stratified estimator on the strata the sample was drawn from | 122,900 | 23,229,780 | 116,148,900 | none |

- **Separation.** Six routes file six amounts (43,484,518; 19,724,936; 48,578,768; none; 3,382,582; 23,229,780); only the design's strata file the golden, and every route but the raw share offers a positive amount, so no wrong route looks broken.
- **Corridor (asserted, C3).** The design report's whole-hectare stratum areas or the unrounded pixel areas, the estimator by stratum or point by point, and post-stratification to the final map with the design weights: 122,882.7 to 122,933.9 ha, every one stated as 122,900 and offering 23,229,780 tonnes.
- **Margins.** The golden area sits 32.7 ha from the nearest hundred-hectare edge; the default route 48,699 ha above it and the final map's area 49,657 ha below.
- **Worth.** The decisive step moves the area by 48,700 ha and the offer from 3.4 million to 23.2 million tonnes; the first correction a solver reaches for (the map's own area, or the map corrected by its user's accuracy) overshoots the offer about twofold.
- **Direction.** The default overshoots the area (3.4 million tonnes, a seventh of the golden), the final map and its user's-accuracy correction undershoot it (43.5 and 48.6 million tonnes), the preliminary map's stratum overshoots (19.7 million); only the design's strata land.
- **Grid.** Six estimators by the four conformance handlings (adjudicated, main campaign alone, quality-control labels wherever they exist, plantations or woodland read as forest) by the rounding and variance variants: every cell outside the design-weighted family files another amount, and every cell inside it files 23,229,780 tonnes (asserted through C3 and the R2 block).
- **Dominance.** The golden family spreads 51 ha; the nearest wrong routes sit 48,699 ha above and 49,657 ha below.
- **Position.** The default path files a seventh of the golden and the cheapest corrections about twice it.

### Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the twelve lowland districts on the 2019 layer, every reference point in them | the agreement's article 1; the plan's 3.3; SF10 |
| 2 | Unit of account | the area of deforestation in hectares; tonnes of CO2e offered; US dollars | the agreement's articles 4 to 6 |
| 3 | Attribution window | forest on 1 January 2024 and other land on 31 December 2025 | the plan's 3.2; SF6 |
| 4 | As-of dating | the final map of 22 April 2026, the adjudication of April 2026, the extract of 22 May 2026 | the release note; the manifest |
| 5 | Version basis | the area from the reference sample; the final map (version 2.0) presented; the preliminary map (0.9) the strata of the draw | the plan's 4.1 and 4.2; the design report's section 2; SF5 |
| 6 | Denominator | none for the call; each stratum's area and points for its weight | the design report's table |
| 7 | Weighting | each point by the stratum it was drawn from | the design (the decisive step); C3 asserted |
| 8 | Window length | two years | the agreement's articles 1 and 2; SF1 |
| 9 | Boundary inclusivity | the patch size classes on whole pixels | SF14 |
| 10 | Rounding path | the area to the nearest hundred before the factor; tonnes whole, fraction dropped; whole dollars; the interval to the nearest ten thousand; district areas to the nearest hundred | SF2, SF3, SF8, SF9 |
| 11 | Tie-break | none needed | not applicable |
| 12 | Maturity and censoring | none: the period closed on 31 December 2025, the interpretation and adjudication are complete | the manifest; the adjudication log |
| 13 | Order of operations | conform the campaigns with the adjudication, class each point, weight by stratum, sum, state to the hundred, then the factor, the buffer and the price | the agreement's articles 4 and 5; C1: no conformance order moves a class (asserted) |
| 14 | Row order | none | not applicable |
| 15 | Duplicate resolution | one row per point in each export; a patch delivered in several polygons counted once | SF13 |
| 16 | Identity normalisation | "LFM26/" ids in the quality-control export against "LFM26-" in the main; the 2025 district codes to the 2019 layer through the concordance | SF12, SF16 |
| 17 | Netting against gross | the reductions are the reference level emissions less the monitored emissions; the buffer comes off the reductions | the agreement's articles 4(1) and 5 |
| 18 | Dimensional units | hectares (strata and map by pixel counting), tCO2e per hectare, USD per tonne | the agreement; the statistics workbook |
| 19 | Code and status semantics | land-cover codes 1 to 8 and canopy classes A to D, Spanish labels and canopy bands, DEF, BOS and NOB | the dictionary |
| 20 | Integerisation | tonnes whole with the fraction dropped; each district's polygon shares sum to whole patches | the agreement's article 5; SF13 asserted |
| 21 | Clause scope | article 4 states the area, article 5 the buffer, article 6 the price; the plan's 4.5 governs only the district figures | each stated once |
| 22 | Forward window contents | the payment follows the report due 30 June 2026 for a closed period; retrospective because the agreement pays on the closed period's monitored results | the agreement's article 3 |

### Literal reader

Executed word for word, the agreement fixes one quantity: the area of deforestation in the twelve districts over 2024-2025, as the monitoring report states it to the nearest hundred hectares, times 497.0, taken from 2 times 89,950 times 497.0; 82 per cent of the difference, the fraction dropped, is offered at USD 5.00 a tonne. The plan says the area is estimated from the reference sample, a probability sample of points classed on its definitions, and the design report says how that sample was drawn: stratified random sampling on the preliminary map's three classes, with their areas and the points drawn in each. How to estimate is left to the analysis, and the design forces it: a probability sample's estimate weights each point by the inverse of the probability with which it was drawn, which the draw fixed by stratum, so every design-consistent implementation (published or pixel areas, by stratum or point by point, post-stratified to the final map with the design weights) states 122,900 hectares and offers 23,229,780 tonnes. The literal reading gives the golden; the wrong amounts come from easy methods on the same literal quantity (the final map's error matrix with its own class areas, its mapped area, its user's accuracy), never from another reading of a term. For the asks, the plan's 4.5 fixes the district figures as the points' parts of the accounting area's estimate, and the dictionary's patch_ha with the polygon file's grain fix a patch as the connected area of change, counted once.

### Oracles

None for the call. The final map's statistics and polygons give its mapped areas, which tie to no estimate; the release note describes the reprocessing without a figure; no document states an area, a weight, a number of tonnes or a payment; the reference level summary's figures (579,200 ha over 2015-2022, 497.0 tCO2e per ha) are filed inputs that tie under every route. For the ask, the statistics workbook's deforestation by district equals the sum of the district's polygon areas under every count of patches (asserted), so it confirms no count.

### Ask sheet

**Construction (on the decisive construction's output).** The 90 per cent interval to the nearest ten thousand hectares (two figures: 100,000 to 140,000) and each district's area of deforestation to the nearest hundred (twelve figures, the plan's 4.5; they sum to 122,900), with the report's chart setting each district's mapped deforestation beside its estimate. A wrong estimator misses every one (the default's interval is 140,000 to 200,000); the cracker keeps them, so they never stand alone.

**Ask A: deforestation patches on the final map, by district.** Figures: for each of the twelve districts and in all, how many deforestation patches the final map shows, how many of them are under 1 hectare and how many of 5 hectares or more (39 whole numbers; golden Caoba Alta 1,806, 729, 205; Caoba Baja 4,892, 1,982, 494; Cerro Azul 996, 404, 99; El Encanto 2,851, 1,118, 290; La Esperanza 5,083, 1,972, 539; Las Palmas 3,368, 1,365, 359; Llano Grande 2,610, 1,069, 259; Montealto 797, 333, 75; Puerto Viejo 2,025, 803, 225; Río Verde 3,932, 1,579, 431; Tres Ríos 1,263, 500, 145; Arroyo Hondo 925, 352, 100; all 30,548, 12,206, 3,221). H18 home: the report's district table beside each district's estimate, the map's account of where deforestation sits (the plan's 4.2). Use: the ministry's enforcement units and the benefit-sharing plan count clearing events by size, the smallholder clearings under a hectare apart from the large ones. Construction: each polygon placed in its 2019 district through the concordance (LT-05 and LT-06 both La Esperanza, the highland districts outside); each polygon is the share area_ha / patch_ha of one patch, so a district's shares sum to its patches, in all and by the patch's size class. Primary device: D6, an event's quantity on every line it covers: the final map's polygons are delivered by 10 km tile and by quarter of first detection, so a patch cleared over several quarters or crossing a tile edge is several polygons, each carrying the patch's area (43,321 polygons deliver 30,548 patches). Its over-cleaning half (D1, keys recycled): patch areas are whole 30 m pixels, so distinct patches share an area (the 30,548 patches take 1,821 distinct areas by district), and deduplicating on the area deletes real patches; first detection and tile differ between a patch's polygons. Hazards: Nueva Esperanza (LT-06), a 2025 district carved out of La Esperanza that the 2019 list lacks; the highland districts (SR-01 to SR-06) outside the accounting area in the same file. Path: the polygon file, the concordance, the dictionary and the release note (four files, eight columns). Stops (asserted, each missing all twelve districts on all three counts and every total): polygons counted (43,321, 15,488, 5,913), deduplicated on the patch area (1,821, 72, 1,222), on the patch area within the 2025 district (1,945, 78, 1,296), on the patch area and first detection (38,606, 11,810, 5,883), on the patch area and tile (20,877, 4,952, 3,315), polygons sized by their own area (43,321, 23,439, 2,704), the golden. Realism: change-map deliveries cut polygons at tile edges and alert-based maps by detection period, a patch-level attribute repeated on each polygon is how a vector export carries the patch, and areas by pixel counting repeat.

Main population zero-counts (asserted): the call reads no polygon and no district code; deleting the polygon file moves no figure of the call.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| A, patches by district (all, under 1 ha, 5 ha or more) | counts the polygons by their patch_ha: Caoba Alta 2,600, 926, 405; Caoba Baja 6,881, 2,490, 891; Cerro Azul 1,406, 502, 180; El Encanto 3,919, 1,413, 505; La Esperanza 7,241, 2,517, 987; Las Palmas 4,831, 1,748, 671; Llano Grande 3,683, 1,359, 462; Montealto 1,121, 402, 143; Puerto Viejo 2,915, 1,031, 413; Río Verde 5,585, 2,018, 790; Tres Ríos 1,791, 625, 266; Arroyo Hondo 1,348, 457, 200 (all 43,321, 15,488, 5,913); the cracker that sees the repeated areas and deduplicates on them files 1,821, 72, 1,222 | miss |

Mirror leakage: 7 per cent of ask weight (the mirror, stopping at the default path, keeps the conformed classes in the workbook and the chart's mapped series; it misses the interval, every district area and every patch count).

Pair ceiling: 39.7 (planning weights 38 / 7 / 55 with the tonnes, the payment and the area as the main block and r = 5; the ask weight spread over about 59 criteria: the interval 2, the district areas 12, Ask A 39, the workbook 2, the chart 4; the cracker keeps the main block, the interval, the district areas, the workbook and the chart, 20 of 59 or 0.34, 38 + 7 + 18.6 = 63.6; the mirror keeps r, instruction-following, the workbook and the two chart criteria its estimated series does not touch, 4 of 59 or 0.07, 5 + 7 + 3.7 = 15.7; (63.6 + 15.7) / 2 = 39.7).

### Pre-ship check

- **Three rules.** Domain: the land-use sector's design-based area estimation from a stratified reference sample, turned into emission reductions against the reference level (swap test in the Three rules section). Two layers: the Layer 1 inventory (the main campaign's CSV and the ministry's form-tool JSON with Spanish labels and "LFM26/" ids, the field-by-field adjudication log, the legend's plantations and woodland against the forest definition, the remarks' 2021 to 2023 clearings, the 2019 and 2025 district layers, pixel-counted areas), all of it what the laboratory's and the ministry's systems write, each item asserted neutral on the call (R2: plantations and woodland read as forest, the main campaign alone, the quality-control labels wherever they exist, the remarks, the district layers); and the estimator on the sampling strata, which decides it. Decisive step analytical: the analyst who conforms everything and executes every article files 3,382,582 tonnes on the final map's error matrix (asserted on the generator's clean truth, R3a); changing the strata alone gives 23,229,780 tonnes (R3b); nothing is planted (R3c).
- **Gates.** 16 files in 5 formats (CSV, JSON, Parquet, PDF, XLSX), the final map's polygons at 48,947 rows, two distractors (the forest inventory's tree measurements at 39,122 rows and the fire hotspots at 17,340) the solution never reads, asserted; 68 checks; `verify.py` PASS from the bundle alone (its own reader recomputes the area, the tonnes, the payment, the interval, the twelve district areas and the 39 patch counts); two builds byte-identical; `figures_check.py` exit 0 (100 figures); `precut.py` exit 0 (49 checks); `voice-check.py` PASS; `leak.py --asof 2026-05-22` REVIEW with no LEAK; `guard.py validate` PASS, `surface` 0 promoted (task453 at 0.095 once the dictionary took its own columns and the quality-control export its form tool's JSON; the personas on the card), `heart` WARN (overuse.objective, overuse.gate_g, repeat.decision, repeat.question_form, answered in `## Draw`), nearest text 0.07; the container audit clean on `target/` and `golden/`.
- **Mechanical leak lines.** The agreement and the reference level summary carry the call's nouns (the program, the Facility, emission reductions, tonnes) because they are the documents the call executes, and no figure of the answer; the agreement, the summary, the plan and the design report share the stump paragraph's vocabulary (agreement, period, points, strata, preliminary) because they are the program's own documents and none names a weight, an estimator or the final map's place in the estimate; the map statistics name the districts beside their mapped class areas, which rank nothing on the call.

### Leak check

- `leak.py --asof 2026-05-22` (after every rebuild): REVIEW, no LEAK. The REVIEW lines are answered under `## Pre-ship check` (the call's nouns in the documents it executes, the program's documents sharing the stump paragraph's vocabulary without naming a weight or an estimator, the map statistics ranking nothing). Two earlier LEAK lines were fixed in the generator: the design report's file name carried `sample_` (now `reference_sampling_design_2026-01.pdf`) and the write-up stated the 4,000 points the design report states (now dropped from the write-up).
- Reader, pass 1 (isolated, Sonnet, medium, fresh copies of the prompt and the pack): Q1 none (the nearest pointers are the plan's 4.1 and 4.2, the design report's strata and the release note, and the reader's own reading was that the weights "have to be reconciled with the final map"); Q2 to Q4 none; Q5 every filed rule executed, with the reader computing 122,900 ha on the preliminary strata and 171,600 ha on the final map's class areas and naming the weights as what flips the call (no filed sentence fixes them, so this is the analytical choice, not a fork); Q6 an analytical choice. Every REVIEW line harmless. Realism fixed in one generator pass (see `## Tried and rejected`); the district land areas kept as the statistics institute's round figures; two of its claims did not hold (Nueva Esperanza holds 190 points; the manifest lists every other file).
- Reader, pass 2 (isolated, Sonnet, medium, on the final pack): Q1 none (the nearest sentences state the design facts, and the reader read the release note's "Version 2.0 is the map the 2024-2025 monitoring report presents" as a lure toward the final map's areas); Q2 to Q4 none; Q5 every filed rule executed, its own estimate 122,900 ha on the design strata against 171,600 on the final map's areas; Q6 an analytical choice. Every REVIEW line harmless; every quality-control difference is in the adjudication log (126 of 126). Its question on the patch counts' district layer is closed by the plan's 3.3 and the concordance (SF12).
- Reader, pass 3 (isolated, Sonnet, medium, after the prompt repair): Q1 none (the reader itself took the re-stratification on the final map as the route, the default path); Q2 to Q4 none; Q5 every filed rule quoted, none fixing the weights; Q6 an analytical choice; the prompt presupposes nothing and none is grammatical everywhere.

### Determinism judge

- Pass 1 (2026-10-14, isolated thread on the first cut, reference level 72,400 ha a year): DETERMINISTIC, APPROVE. Every load-bearing figure reproduced from the bundle (224 deforestation points, the weights 329, 2,469 and 4,785, 122,882.7 ha stated as 122,900, the interval, the twelve district areas, the 39 patch counts, the workbook's class counts); the correctly weighted post-stratified estimator gives 122,934 ha and the same rounding everywhere, so the estimator is not a fork; the adjudication changes no class. Gate G method_or_model_selection, analytical_non_defect, no surface-read dependency, no sole data defect; Gate H domain pass, layers pass, decisive step analytical, with the caution that the design report states the strata plainly (Gate F moderate). Low findings, not changed: the chart title's share carries no stated decimals; the workbook's labels are free. Its "stale note" line is a timing artifact: the note already carried the retuned reference level of the rebuilt pack. Report: `determinism_check_report.md`.
- Pass 2, the one re-judge (2026-10-14, isolated thread on the final pack, reference level 89,950 ha a year): DETERMINISTIC, APPROVE. Every figure reproduced (224 points, 201 in the preliminary deforestation stratum, 23 in stable forest; 122,882.7 ha stated as 122,900; the interval 100,000 to 140,000 under every variance variant, the post-stratified one included; 28,329,000 tonnes of reductions, 23,229,780 offered, USD 116,148,900; the twelve district areas summing to 122,900; the 39 patch counts; the workbook's class counts). Gate G statistical_rigor in the thread's words (the family and the decisive step as on the card: the estimator the design forces), analytical_non_defect, no surface-read dependency, no sole data defect; Gate H domain pass, layers pass, decisive step analytical; stump power moderate (a solver who reads the design report closely lands the call; the asks carry the rest). Its one finding was wording: step 7's parenthesis read as calling LT-05 and LT-06 highland districts, reworded in `submission.md` with no figure moved; the interval's bounds sit about 2,000 ha from their edges; the January 2026 image dates read for December 2025 are the nearest clear scenes (the dictionary's "image read for December 2025"). Report: `determinism_check_report_pass2.md`.

## Tried and rejected

- 2026-10-13, draw: the seed's world (ET09, hospital margin peers from cost reports). Rejected: health economics is task451's pairing among the last three draws; the domain moved to Physical & Environmental Sciences.
- 2026-10-13, draw: population_selection as the strategy, with the gap population and G14 first. Rejected: the guard blocks population_selection against task258 and the triple (population, G14, method selection) against task256; the gap is time (the samples describe their own days, the load the whole year) and the strategy other.
- 2026-10-13, draw: the time gap with G16 first. Rejected: the triple (time, G16, method selection) repeats task501's lineage inside the batch; G14 leads (the sampled concentration does not apply to the storm days).
- 2026-10-13, draw: a designation set (every tributary over its allocation) with an xlsx and png pair. Rejected: both repeat task451; the program's three projects make a ranked slate, delivered as a memo and a CSV.
- 2026-10-13, design: Hessick River at a residual scatter of 0.62, so that a rating curve without the retransformation correction drops it from the slate (a rung for regression-savvy solvers). Rejected: at that scatter Hessick's load moved by up to 18 per cent across defensible rating curves, and calibrating on two years, or dropping the college's storm samples, swapped it for Ambrey River; the scatter is 0.30 like the other streams, and the uncorrected curve funds the golden three.
- 2026-10-13, design: monthly sampling rounds (the second Tuesday). Rejected: with about 14 samples a station in water year 2026, a rating curve calibrated on that year alone moved loads by up to 30 per cent; the Commission samples on the first and third Tuesdays, and every calibration window funds the same three.
- 2026-10-13, design: the agreement's load definition naming the record's start year (water year 2024). Rejected: a sentence telling the solver to estimate one year's load from three years of samples points at a fitted relationship; the definition names the record's sources instead, and the calibration window converges in the data.
- 2026-10-13, design: Orrinwood and Ambrey placed between their rating-curve and interpolated loads. Rejected: their interpolated loads sat under the rating curve's on several seeds, so the default funded only one or two; they sit just under both, and the default's three come from interpolation sinking Kestle and Hessick.
- 2026-10-13, stage 4: the asks' primary devices as first built, the receiving-water name join (Ask A) and the contract's watershed label against the program's overlay (Ask B). Rejected: a careful solver walks the register's stream network, and once 4.1(b) is read to the acres lying in each watershed it takes the overlay, so both asks would have fallen to the cracker; the judge also found the label against the overlay an open reading. The primary devices are now the quarterly reports (each report covering its period's days) and the contract acres repeated on each enrolled field's line, with the network and the straddling fields kept as second devices, and 4.1(b) counts the acres lying in each watershed.
- 2026-10-13, stage 4: the 15-minute record's timestamps converted with each local date's offset. Rejected: it repeated an hour at the spring clock change and dropped one in the autumn (the judge found both); the record runs in UTC from each local midnight, the days of the clock changes holding 92 and 100 values, and the local days are built from the exact switch instants.
- 2026-10-13, stage 4: each tributary's load graded to the nearest 10 kg as a point. Rejected: Pellow, Dunmarsh and Hessick sat within a kilogram of a rounding edge on defensible curves (the judge); the write-up gives each load and excess as its range over the full-record curves, rounded outward to 10 kg.
- 2026-10-13, second-layer attempt after shipping: the season made decisive (a tributary-specific seasonal shift in concentration at a given discharge, so a rating curve with no season term funds another slate). Rejected: with the Commission's fixed rounds spread across the year the no-season curve averages the seasons, and even a fivefold swing moved one tributary's load by about 10 per cent (11 with the college's storm samples confined to spring), no more than the spread among the golden curves' calibration windows, so the two families overlapped on every placement tried.
- 2026-10-13, second-layer attempt after shipping: the retransformation correction made decisive (Varrow Brook's scatter raised so the uncorrected curve drops it). Rejected: the correction grows with the variance while the water-year-2026-only calibration's noise grows with the scatter too; at a scatter of 0.65 the uncorrected and corrected families sat 10 per cent apart against a placement window of under 200 kg, too thin for every defensible curve to land one slate.
- 2026-10-14, hardening prototype: the retransformation correction made decisive on a dense record (the college's automated sampler at Varrow Brook, a sample every third day or every day, each sample scattered about its day's mean at 0.72, on their own random streams so every other station and both asks stayed byte-stable). Rejected on the prototype: the uncorrected curve fell 21 and 23 per cent under the corrected one (3,392 against 4,320 kg; 3,089 against 4,032), but at that scatter the corrected curves still spread 7 to 9 per cent across calibration windows (water year 2026 alone 4,076 and 3,671 kg) and the composite and direct sums sat 3 to 12 per cent under them, so against Ambrey River the window held margins under 210 kg and a log-space composite landed on the uncorrected side.
- 2026-10-14, hardening prototype: concentration steepening above each station's 90th-percentile flow (an added log slope of 0.6), so a curve calibrated on water year 2026 alone, at the stations whose 2026 storm crews reached only modest storms, would extrapolate under the 2024 and 2025 storm samples. Rejected on the prototype: Kestle River's water-year curve fell 16 to 20 per cent under the full-record curves (17,018 against 20,307 to 21,332 kg), but a kinked relation splits the full-record curves themselves (Hessick River 7,419 to 9,242 kg across log-linear, quadratic and two-year fits), and the stations whose crews reached the spring peaks run high on their water-year curves, so the window and the curve's form become a choice between standard practices a judge can rule competing answers (the finding task453's hardening drew).
- 2026-10-14, re-root (architecture 2): v1, each unsampled day's concentration from a concentration-discharge rating curve, shipped and approved by the judge, but the rating curve is the field's standard load method, which a careful solver reaches for, and four attempts at a second layer (season, retransformation, a dense automated sampler, a kinked relation) were either too thin for one answer or a choice between standard practices. Re-drawn in the same task type, in the land-use sector: the reporting period's deforested area estimated from a reference sample drawn on a preliminary change map that the final map later revised.
- 2026-10-14, design: the change-map ask as the patches of 5 ha or more with their area and their share of the district's mapped deforestation, the polygons cut by tile only. Rejected: deduplicating the polygons on the patch area and first detection recovered the count in 11 of 12 districts (a tile-split patch's pieces shared the patch's date), and any route that filtered on patch_ha and summed area_ha landed every area and share whatever it counted; the polygons are now cut by tile and by quarter of first detection, each with its own first detection, areas are whole 30 m pixels, and the ask is three counts by size class.
- 2026-10-14, design: the mean patch size by district as a third figure. Rejected: one district's mean sat exactly on a one-decimal edge (2.4500 ha) and another 0.006 ha from one; the third figure is the count of patches under 1 hectare, whose boundary no patch touches.
- 2026-10-14, design: the monitoring plan's 4.2 as drafted ("The forest change map of the period stratifies the reference sample"). Rejected: beside "the period's final change map" a literal reader takes the final map as the stratifier, a filed sentence licensing the default route; 4.2 now says only that the report presents the final map with its accuracy assessment, and the design report alone says which map drew the sample.
- 2026-10-14, design: the interval to the nearest thousand hectares and "its stratum" in the workbook sentence of the prompt. Rejected: post-stratifying to the final map with the design weights states the same 122,900 ha but an interval of 104,000 to 142,000 against 103,000 to 143,000, so the interval rounds to the nearest ten thousand (100,000 to 140,000 under every variant, asserted); the stratum beside the final map class in the requested workbook pointed at the draw, and the workbook sentence asks for the reference class and the final map class, the accuracy assessment's own pair.
- 2026-10-14, design: each district's area left as "each district's area of deforestation" with no basis. Rejected: the district's land area times its points' weighted share (a ratio estimator) files another hundred in all twelve districts; the plan's 4.5 files the district figures as the part of the accounting area's estimate contributed by the district's points (post-stratification leaves every district's hundred unchanged, checked).
- 2026-10-14, stage 4: the reference level at 72,400 hectares a year, where the default route's 171,600 hectares sat above the two years' 144,800 and offered nothing. Rejected after the first leak read and judge: a default path ending on no tonnes meets a prompt that asks what the Facility will pay for them, so a solver landing on nothing is told to look again; at 89,950 hectares a year (719,600 over 2015-2022) every route but the raw share offers a positive amount (the default 3,382,582 tonnes, the map's area 43,484,518, the golden 23,229,780) and the sample, the strata and every ask stay as they were.
- 2026-10-14, stage 4: the interpreters' texture as first built (remarks drawn evenly from each list, so three stable-forest remarks each sat near 360; land cover and canopy class one to one; the quality-control form's canopy differing from the main campaign's on 36 points with no adjudication row; inventory plots spread evenly over the five years). Rejected on the leak reader's realism read: remarks now follow uneven frequencies, canopy calls scatter around each cover class without crossing the 30 per cent line, every field the two campaigns record differently is logged and each point is settled as a whole, and the inventory's plots follow its measurement cycle; no class, area or count moved (asserted).
- 2026-10-14, stage 4: interpretation and quality-control dates drawn on every day of the week, nine interpreters with equal loads. Rejected on the second leak read: dates fall on working days and two interpreters carry double loads, remapped from the same draws so no random stream, class, area or count moved (asserted, verify PASS, byte-identical); the round district land areas stay, since moving them moves the sample's draw.
- 2026-10-14, after shipping: the prompt's opening "How many tonnes of emission reductions can the program offer ..., and what will the Facility pay for them?". Rejected on the house-fix register's H23: the payment clause presupposes tonnes to offer, a fact only the analysis establishes; it reads "How many tonnes of emission reductions, if any, can ... offer ..., and what would the Facility pay for them?", every figure, file and rounding kept, and the reader re-run on the repaired prompt (pass 3).

- 2026-11-01, re-root: architecture 2 (the forest programme's deforestation area from a reference sample drawn on the preliminary change map) shipped 2026-10-14 with no portal result and is re-rooted at the Batch 3 queue reset; its world is closed (one architecture per world) and its identity moved to the card's lineage.
- 2026-11-01, draw: the seed's world (ET09, hospital operating-margin peers from cost reports). Rejected: the margin is an accounting computation and the peer pick a sort on it, so the domain is a backdrop at any depth; every layer the world offers (fiscal-year calendarisation, partial-year reports, cost-to-charge ratios) is rule application or semantics.
- 2026-11-01, draw: capitated primary-care encounters completed from other providers' order footprints. Rejected: the completion factor has to be measured on a complete-reporting sub-population (an escape evidence.md 1.2b records as spent), a per-group factor is the grouping dichotomy (1.1c), and it sits beside task196, task458 and task473.
- 2026-11-01, draw: compressor rod-packing vent methane carried from one annual measurement across a packing replacement. Rejected: a replacement restarting a wear curve is task132's approved insight.
- 2026-11-01, draw: landfill surface methane from flux chambers sited on the walking survey's hot spots, carried to the grid through the survey. Rejected: a sample selected on an auxiliary and estimated through it is architecture 2's own lesson, and population_selection is banned in the window (task264).
- 2026-11-01, draw: daytime-only chamber fluxes scaled with a temperature model. Rejected: the temperature response is a kinetic fork (Q10 against Arrhenius) and the scaling is the field's reflex, so the golden would be the opponent's first move.
- 2026-11-01, draw: IRT pre-equating under item-exposure drift. Rejected: drift under compromise was screened dead at task249 and position effects at task482 v6; task464's note bars the cell.
- 2026-11-01, draw: earlier screens this session, each dead on its own record: newborn deemed-eligibility exposure (needs a dated change or composition, beside task445), LNG ferry methane slip (the IMO bottom-up reflex, task459 and task478 adjacency), chargemaster cost-to-charge period matching (generic under the swap), refrigerant top-ups and anaesthetic gases (rule application), APU against preconditioned air (task281-like), accommodation non-response (a G12 fork), ghost cattle (dual-system), IRT testlets (1.1c), feed-additive dose (Jensen, task162 and task309), cookstoves (rule), behind-the-meter solar (sampling monoculture), AADT factor groups (task474 v6).
- 2026-11-01, draw: the kiln mercury world with the conservation route as the golden was also checked against the lineage: v1 corrected a sampled concentration by a covariate relation; this build has no covariate relation and never models the stopped-mill rate, so it is kept with the differentiation line on the card.
- 2026-11-01, design: calcination CO2 as the third ask. Rejected after cutting: the licence sentence that fixes its WHAT (CO2 released by the carbonates) leads a careful solver straight to the non-carbonate correction, so the ask was executable from a filed sentence; replaced by hours on feed, which share the journal's reconstruction.
- 2026-11-01, build: a re-sent historian batch as texture. Removed: an exact copied block is a plant kind R3c bars, whatever its role.
- 2026-11-01, build: the ledger in wet tonnes with the laboratory's moisture on the main path. Rejected: mishandled, the moisture moves both kilns' figures, so R2 fails; the ledger now carries raw materials dry and fuels as fired, and the composites state their basis.
- 2026-11-01, build: kiln 1's dust taken from the weighbridge. Rejected: the weighbridge then had no use but the decisive step (second-use test); the ledger's filter dust to silo S7 is the dust source and the weighbridge ships as a declared distractor (the readings agree, SF6).
- 2026-11-01, build: the historian's raw mill as a run fraction to one decimal. Rejected: the fraction route lands the direct-operation hours in most quarters; the historian now carries the mill's status at each half-hour stamp.
- 2026-11-01, stage 4 round 1 (judge DETERMINISTIC, APPROVE; leak reader clean, question 6 analytical): two advisory forks closed before the one re-judge. Hours: the clock-hour grid readings (kiln 1 direct 1,509, 1,223 or 1,396 against 1,392; kiln 2 1,863, 1,551 or 1,729 against 1,731) are ruled out by a new licence definition 1.8 (elapsed time, summed, not a count of clock hours), and 1.4, 1.5 and 6.5 now read "the time during which"; no graded figure moved. Fuel mercury: the supplier certificates had carried a moisture factor and a 15 per cent cargo spread, giving about 65, 82, 147 and 62 kg; they are now built from the fuel the as-fired composites describe (coal per cargo over the quarter it feeds, SRF per month, each within 0.6 per cent), so every certificate reading prints 68, 83, 151 and 66 kg (SF14); no graded figure moved. The design note's annual hours now state the quarters summed (7,941), and the test reports' closing lines differ report by report.
- 2026-11-01, stage 4 round 2 (re-judge, order kept): the main call and every hours figure reproduced; one FIX_NOW on the NOx ask, the oxygen content of air unfiled (20.9 put kiln 2 at 605.503 t, a knife-edge). Licence 1.6 now files 21%; NOx asserted at 931.90 and 605.00 t with the historian kept or the logger preferred in the overlap. metadata.json declares each distractor's reason. No graded figure moved.
- 2026-11-01, build: hours on feed and direct-operation hours read from FEED lines only. Kept as the device: unplanned stops are logged as burner trips, as interlocked trips are; the planned shutdowns log FEED OFF.
