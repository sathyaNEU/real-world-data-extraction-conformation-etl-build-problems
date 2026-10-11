# task132 design note: VPR-340 PSU last-time buy

Private, never ships. Architecture v1, drawn 2026-10-11; hardening loop 1 (module-age renewal) after solver round 1; realism repair 2 after reader round 4; realism repair 3 after reader round 5, with the world redrawn. Seed: `analytical_tasks/01_forecasting/FC03`
(service-parts lifecycle setting only; its withheld-rule shadow-run corpus is capped and not used).

## DRAW

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task132.json`, registered before the ladder and re-checked after loop 1 and repair 3 (guard PASS, nearest driver task87 at 0.06); world seed 1215 chosen by `seedsearch.py` in repair 3 (seed 150 through repair 2) |
| Domain / task type | energy-systems-utilities / asset-condition-maintenance (client domain itself) |
| Objective | Forecasting & Predictive Modeling |
| Shape | 04, setting one dial (whole lots against a 95 per cent cover bar), with a forecast across periods underneath |
| Gate G mechanism | forecasting |
| Gap, pattern | population (which module is in the relay each month) over time (wear-out across the horizon); pattern none |
| Generators | G6 composition shift (band occupancy moves to new modules as failures are replaced), G13 horizon mismatch, G12 absence of record against record of absence |
| Stump strategy | population_selection (the module-months each band will hold, given failures replace modules) |
| Layer 2 family / pattern | field_method / `own:renewal-of-replaced-modules-in-a-spares-forecast` |
| Decisive rule filed | yes: AM-PC-014 rev 4 files module age from the fitted date (3), rates per module-year with failures and module-years counted over the period the work-order history covers (5.3), a monthly expectation of rate over twelve for a module in service (6.1) and expected failures as the band rates applied to the module-months expected in each band (6.2); support to the end of the program period counts its last month (4.2); the purpose (1) and the prompt say failed modules are replaced from the buy |
| Official decoy, validated decoy | no, no |
| Decision | dial_setting, answer unit count (lots) |
| Stakeholder | Manager, P&C Asset Planning (capacity_planner); signs off to the Director, Asset Management (line_manager_or_team); forcing event the OEM last-time-buy window (other) |
| Context artifact | filed_standard (AM-PC-014 rev 4) |
| Calibration form | none: the method is filed and the difficulty is the construction |
| World | Ontario, CAD; Tarrock Hydro Distribution (fictional), Veldtek Protection Systems (fictional), VPR-340 (fictional); 27 transformer and 115 distribution stations with invented Ontario names (surname and road, English, Scottish, French and Indigenous-derived forms), a distribution station at 12 feeder bays at most |
| People | Rachael Villanueva, Kurt Allison, Angel Baird, George Ray (guard.py names, en_CA, seed 132) |

**Data-native sentence.** A relay's power supply is a field-replaceable module that wears out with its own age, and a module that fails is pulled and replaced with a new one, so the module in a relay two years from now is today's module only if today's module survives two years; for the fleet's oldest modules, a year's wear-out rate carried into every remaining month counts more failures than one relay position can have.

**Layer 1 (the mess, and the systems that make it).** An EAM export of the P&C crews' work orders (32,520 rows: relays, RTUs and recloser controls in the register, station batteries, chargers, breaker trip tests and CT and VT checks on assets the register does not carry, and station inspections at a monthly or quarterly cadence; periodic tests raised when due and closed after real slips; cancelled duplicates raised twice from SCADA alarms; logistics work orders that ship failed modules to Veldtek, some two to a box, and send each station rebuild's retired equipment to the e-waste processor under a manifest; follow-up work orders that fit the spare a day after a call-out; crew text in each person's own habits, with readings, LED states, times and references, bays written each person's way and now and then the wrong bay; work orders numbered as they were entered, so a call-out written up the next morning sits after later-dated work; PM work, and some planners for three weeks, still on the old region and crew codes after the April 2024 change until the PM masters were re-coded; in-progress work at the extract date); a rotating-item history for the PSU that starts at the January 2021 go-live with the modules then in place loaded at their legacy fitted dates (including the 2015 service-bulletin swaps of date codes 97 and earlier, which show only as fitted dates, and year-only legacy dates loaded as 1 July), and where each removed module went (the returns shelf of the store serving the station in the region of the day, or scrap with a relay retired by a rebuild, under its manifest); failures at every module age, random and early-life ones included, and repaired modules that fail again within months of refit and go back to Veldtek under its repair warranty; an asset register of eight models with a region column that the 2024 reorganization did not update, asset numbers set up in batches for each station rebuild, serials up to three years older than the install for units held in stores; a renewal program workbook whose approved 2026 version supersedes a 2025 plan with a different station set, its own 2026 entries and different scope wording, puts its first schemes in the autumn 2026 outage window, builds the large stations in two stages by bay, and lists spare bays and kept VPR-220 feeders inside its bay ranges; spares across depots in serviceable, quarantined and at-repair states, the last tied to Veldtek's RMA register, which runs from the 2015 bulletin returns through the legacy returns and a January 2021 receipt for a module removed before go-live, with blank and mistyped references and a skewed receipt lag; a maintenance compliance report with two corrections made by hand; a SCADA operations export that logs supervisory trips beside protection trips; Windows exports with fixed decimals, Excel's calculation chain, and the vendor's notice as a LibreOffice export.

**Layer 2 (the shortcut, and why an expert refuses it).** The shortcut ages the module now in each relay month by month to the end of support and adds its band rate over twelve in every month (the cumulative hazard of today's module). An expert sees that a module that fails is replaced and the replacement starts in the 0-9 band, so the expected failures in a relay are the present module's rate weighted by its chance of still being there, plus the replacement's rate after; summing the hazard counts, for an old module, more than one failure of a module that can fail once. This is the renewal function against the cumulative hazard, the standard distinction in spares forecasting for replaced wear-out items.

## GATE G

- **Litmus.** No reported figure or stakeholder conclusion is overturned; every file is correct. The difficulty is a forecast construction. Litmus: no.
- **Primary mechanism:** `forecasting`, with the expected occupancy of each age band under replacement as the decisive construction.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Deletion test.** There is no wrong number to delete; with every distractor removed the ladder is unchanged.
- **Clean-data and instrument tests.** A perfect instrument (failures recorded since 1992) would remove the go-live window step, which is now an ordinary step and not the stump; the renewal step survives any repair of the data, because it is about the future.
- **Lens swap.** Not one population under two lenses: the naive and the answer use the same rates and relays and differ in which module occupies each relay in each forward month.

## THE STUMP

A competent solver builds AM-PC-014's module-age band rates over the go-live window, ages the module fitted in each supported relay month by month to the end of its support, applies the band rate in every month and orders 19 lots; the step that lands it there is keeping today's module in the relay after it has probably failed, when 6.2 counts the module-months expected in each band and a failed module's replacement starts in the 0-9 band.

## LADDER (expected failures, lots, against the answer; 15 modules available)

| Rung | Construction | Expected failures | Lots | vs answer |
|---|---|---|---|---|
| 0 | Trailing twelve months' failures per in-service relay, over the forward relay-years | 230.4 | 10 | -22.9% |
| 1 | Band rates by relay age (installation date), relay ageing, no replacement | 249.9 | 11 | -16.3% |
| 2 | Module-age rates, module-months counted from each module's fitting (not the go-live), with replacement | 246.6 | 11 | -17.4% |
| 3 | Module-age rates over the go-live window, present module aged forward with no replacement | 431.4 | 19 | +44.5% |
| 4 (answer) | Module-age rates over the go-live window, present module weighted by survival, a 0-9 module after a failure | **298.6** | **13** | 0 |

Side cells (priced): module-months from fitting and no replacement 365.9 (16 lots, the two errors partly cancel and stay three lots high); every PSU work order counted, cancelled and logistics included, 393.1 (17); a staged scheme read by its first stage for every bay 273.7 (12) or its last 324.6 (14); the superseded 2025 plan 262.5 (11); module-age rates with relays aged from installation 819.4 (35); no ageing (current band held) 244.5 (11) without replacement and 188.9 (8) with it; one rate pooled over every age 195.4 (9); every relay to December 2035 541.3 (23). No rung or side cell lands on 13 (asserted).

**Bin.** With 15 modules available, 13 lots hold for expected failures from 287.3 to 311.2, so the answer sits 3.8 per cent above the lower edge and 4.2 per cent below the upper (asserted at 3). 12 lots give 83.6 per cent and 13 give 99.1.

## SURVIVAL PROPERTIES (Part 1)

1. Not written as a step: 6.2 defines the quantity (the band rates applied to the module-months expected in each band) and 3 defines module age from fitting; no sentence says how to split a month between the present module and its replacement.
2. No sweepable corpus nominates it: there is no corpus.
3. No arithmetic symptom: the no-replacement total reconciles to every control in the pack (rates, relay counts, stock); only a per-relay check (more than one expected failure of an old module) exposes it.
4. Not a per-row predicate: the occupancy is a recursion per relay over months.
5. Enumeration is arithmetic: no column carries a relay's expected failures.
6. No cutover date: replacements happen throughout the horizon.
7. Survives deletion: nothing wrong to delete.

## CLOSURE TABLE (22 axes)

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | VPR-340 relays in service at the count; failures per 5.1 (filed) |
| 2 | Unit | module-month; failure = one CM or EM work order (filed) |
| 3 | Attribution window | failure in its reported month, at the removed module's age on the first of that month (filed 5.2) |
| 4 | As-of dating | ages from the rotating-item fitted date on the first of each month (filed 3, definitions); a legacy date held only as a year is used as loaded, 1 July (dictionary) |
| 5 | Version basis | approved 2026 program, current at the count (filed 4.1); the 2025 sheet is labelled superseded |
| 6 | Divisor | module-years in service over the period the work-order history covers, the same period as the failures (filed 5.3); the history starts at the go-live (dictionary) |
| 7 | Weighting | rates per module-year, pooled within band (filed) |
| 8 | Window length | numerator pinned to every recorded failure; no shorter window admissible |
| 9 | Boundary | in service on the first day of a month (filed 3); support up to but not including the commissioning month of the bay's scheme or stage (filed 4.1), out of service from its first day (program notes), so a January commissioning is not supported on 1 January (5 relays in 2031, 6 in 2034); a relay at a station with no scheme in the period is counted through December 2035 (filed 4.2, 103 relays); a spare fitted on a follow-up work order goes in by the first day of the next month, so it counts from the same month (asserted) |
| 10 | Rounding | unrounded throughout; every one-decimal figure at least 0.012 from its rounding edge after TUNE (asserted 0.05 of a tenth) |
| 11 | Tie-break | none arises |
| 12 | Maturity | every PSU failure work order is complete at the count; INPRG excluded by 5.1 |
| 13 | Order of operations | rates, then occupancy, then Poisson; commutes |
| 14 | Row order | sums only |
| 15 | Duplicates | cancelled duplicates excluded by status (filed) |
| 16 | Identity | removal_wo ties each failure to the module it removed; the module in service on the first of the month gives the same module (verify.py) |
| 17 | Netting | none |
| 18 | Units | modules and relays are counts; cost CAD per module (notice) |
| 19 | Codes | CM, EM with failed component PSU count; LOG, PM, MOD, INSP do not, and a follow-up fitting work order carries no failed component (filed, dictionary) |
| 20 | Integerisation | smallest whole number of lots (filed) |
| 21 | Clause scope | 4.2 applies to stations with no scheme in the program period; every live VPR-340 bay sits in exactly one approved row (asserted), spare bays and VPR-220 feeders in a row's bay list carry no VPR-340 |
| 22 | Forward window | October 2026 to each relay's support end; the replacement is in service from the month after the failure (3: fitted during the month, in service from the next first day); with the 0-9 rate at 0.0052 a year, counting the replacement a month earlier or later moves the total by 0.13, which section 3 closes (a module fitted during a month is in service from the next first day) |

## ASK SHEET

| Ask | Figures | Device on the ask path |
|---|---|---|
| Lot count, modules, cost | 3 | the replacement construction |
| Cover and cost for 8 to 22 lots | 30 | the cover column moves with expected failures; the range spans every rung of the ladder, 10 to 19 lots |
| Expected failures by year, Q4 2026 to 2035 | 10 | the replacement effect grows with each relay's horizon, so later years move most |
| Relays supported on 1 January 2027 to 2035 | 9 | staged schemes by bay; January commissionings; the superseded 2025 sheet |
| Expected failures by region | 3 | the register's region column predates the 2024 regions; the current regions live in substations.csv |

Pair arithmetic: a solver on rung 3 (19 lots) keeps the costs (15) and, if it reads stages by bay, the nine supported-relay counts; it loses the lot call, every non-trivial cover cell, every year and every region. Criteria: 3 + 30 + 10 + 9 + 3 + memo items (2) + files (2), about 59.

## SOLVER ROUNDS

- Round 1 (architecture 1, before loop 1): both solvers landed 17 lots; hardened in loop 1 (module age with renewal).
- Round 2 (loop 1): both solvers missed the call with 18 lots on 411.9 expected failures, proxy 36.8 each, worth-it gate passed. Each completed every lower rung (module age from the fitted date, support by bay, exposure from January 2021, 14 available modules) and carried each relay's current module forward with no replacement. Both named the renewal reading (about 298, 13 lots) and declined it because the procedure does not spell it out. Read as the stump, not a fork: section 3 ages a module from the date it was fitted and counts it in service only while it is fitted to a relay, so after a failure the module in service is the one fitted in its place, and 6.2 applies the band rates to the module-months expected in each band; their own exposure counts replacement modules from their refit. The determinism judge rules on it.

## LEAK REVIEW

- Loop 1 `leak.py`: REVIEW. The procedure, dictionary and notice carry six to eight of the call's words (VPR340-PSU-02, lots, modules, last-time buy, Veldtek): the vocabulary of the subject, with no figure from the answer. The dictionary's run date 2026-10-01 is the extract job's stamp. Container audit clean (H1).
- Reader rounds 1 and 2 read architecture 1 (before loop 1): no decisive-step sentence, no ranking file, no planted file; the narrow settings window (13 to 19) was a prompt-level tell and is now 8 to 22; the realism list was taken into the loop-1 rebuild (names, crews, bays, serials, retirements, programme months and scheme numbers, RMA filtering, weekday patterns, labour hours, descriptions, containers).
- Loop 1 reader (round 3): no decisive-step sentence (it took the no-renewal reading, 412 failures and 18 lots, for the answer), no ranking file, no planted file; sixteen realism findings (the EOL PDF's container, planned work on weekends and holidays, corrective-work texture, completion lags, serial-number order, station rebuild cutovers, programme scope, storm wording, the AM-PC-014 container and dating, duplicate bays, RTU wording, workbook containers, RMA working days, feeder reclosing, the EOL repair terms) were fixed in the generator with no graded figure moving (checks 65 and the verifier green, double build byte-identical); two side cells moved (the 2025 plan 260.2 to 259.5, every PSU work order 410.2 to 427.2, neither on 13 lots). `leak.py` now also lists 273 dates after the as-of date: the programme's commissioning months, written as date cells.
- Loop 1 reader (round 4, after the realism rebuild): no sentence names the decisive step; it listed the procedure's filed rules (module age from the fitted date, support by bay, the failure definition, the stock count) and the Rev 4 change log as pointers to the lower rungs, and it read the renewal of a failed module as an open question rather than a named step. No file ranks or states the answer; no file is pure scaffolding (the dictionary's general block and the programme's notes come closest and are being rewritten). Realism findings taken into a second repair: tie-outs on the failure and stock path that are too complete, procedure and programme wording that reads as a specification, a programme that fits the register bay for bay, maintenance distractors that contradict the work orders, templated crew text, an inspection-padded work-order extract, legacy dates with no defaults, an RMA register that starts at go-live, dictionary drift, container tells, and British spelling at an Ontario utility. One determinism point taken as a pin: a relay whose bay is commissioned in January is out of service from 1 January.
- Repair 2 (after reader round 4), every finding fixed in the generator: follow-up fitting work orders (41), two-module boxes, blank and mistyped RMA references, a skewed removal-to-receipt lag and a January 2021 receipt for a module removed before go-live; AM-PC-014 section 3 as a definitions table and 8.3 as a filing rule; program notes on funding, outage windows and staging, with the two pins; spare bays and mixed VPR-220 stations in scope and a 2025 plan that differs in stations and wording; compliance counts derived from the PM work orders, with formulas; composed crew text (197 distinct failure write-ups); inspections cut to a monthly and quarterly cadence with asset work in their place; 1 July legacy dates, stores-held serials and trip-identity exceptions; the RMA register from 2015; the dictionary's stock fields and the sizing extracts; per-workbook Excel builds and windows, irregular Word revision ids, a PDF stamped to the second; Canadian spelling and the program file rename; the repair terms in the notice. Figures moved: expected failures 297.9 to 298.9 (the 1 July dates), modules available 14 to 15 (three open RMAs under the new turnaround), the years and regions by up to 0.4; cost, every cover cell and the supported relays unchanged; TUNE re-run (four shifts, clearance 0.058 of a tenth). Checks 1613 and the verifier green; double build byte-identical; `leak.py` REVIEW on the same three classes as before.

- Reader round 5 (after repair 2): no sentence names the decisive step and no file ranks or states the answer; the run-log dictionary's General block and the program's Notes sheet read as curated (exactly this analysis's caveats, and notes written to an analyst) and were rewritten as the reporting service's readme and as program management notes, every pin kept. Two determinism pins taken (5.3's exposure period, 4.2's last month) and fourteen realism findings.
- Repair 3 (after reader round 5), every finding fixed in the generator: 5.3 counts failures and module-years over the period the work-order history covers and 4.2 counts the last month of the program period; AM-PC-014 carries roles, records and approval from first issue, a revision history with ordinary changes and rev 4 (November 2025) prompted by internal audit IA-25-09, definitions phrased as a procedure; random and early-life failures (0-9 band 15 failures, 0.0052 a year) and repaired modules failing within months of refit with warranty rows in Veldtek's register, the RMA and repaired-module flow now inside the simulation so a repaired module's early-life risk is known when it is fitted; the 62 modules in relays retired by the 2022 to 2025 rebuilds scrapped with them under six e-waste manifests (history, LOG work orders, stock unchanged); crew write-ups by person with their own case, separators, vocabulary, readings, LED states, times and bay forms, rare typos; no fan in a relay PSU; stragglers on the old region and crew codes, work orders numbered as entered, asset numbers set up in batches, bay references written each person's way, two hand corrections in the compliance report, stores by the region of the day; schemes in the autumn 2026 window and 2026 entries on the 2025 plan; the EOL notice as LibreOffice Writer's own export (only its clock fields pinned); fixed decimals, Windows line endings, Excel-style cached values and a calculation chain; the procedure's revision sessions and measured statistics; the operations export closing with supervisory trips; SB-15-02 bounded to date codes 97 and earlier; Ontario station names and distribution stations at 12 feeder bays at most. The new failure law, station mix, bulletin scope and program months redrew the world, so seeds 1000 to 1499 were searched and seed 1215 taken, TUNE one shift (clearance 0.12 of a tenth). Figures: expected failures 298.9 to 298.6, modules available 15 (unchanged), cover 99.1 (unchanged) and 83.2 to 83.6 at 12 lots, the lot count 13 (unchanged), the stump 415.5 (18 lots) to 431.4 (19 lots); every year, region and supported-relay count moved. Checks 1716 and the verifier green; two scratch builds byte-identical to each other and to `target/` and `golden/`. Solver round 2 measured the seed-150 world; no round has been run on this one.

## Tried and rejected

- Healthcare same-day demand censored at sell-out time as task133's first draw (recorded here because it was drawn in the same wave): the censoring was too mild to separate the rungs (bookings 7 per cent low) and two rigorous uncensoring methods disagreed by one session in several cells, a fork.
- Install-date day shifts as the rounding knob: no effect. Install-month shifts: reseeded the failure draw (expected failures moved from 465 to 418), so the knob became a recorded-failure month shift, which leaves exposure untouched.
- The first world (seed 132): after the leak reader flagged the background work orders as machine-made (substation names like "Basswoodwood", crews named for the 2024 regions from 2021, work dated outside service windows, cancellations and logistics orders only on the analysed path, perfectly regular inspections, one scope line for every scheme), the rebuild changed the random stream and the trailing-rate rung fell to 9.7 per cent low, one lot from the answer. Seeds 140 to 165 were swept and seed 147 taken (trailing rate 30.7 and installation exposure 27.6 per cent low).
- Architecture 1 as built (relay-age rates, left-truncated exposure the decisive step): solver round 1, plain 85.0 and skeptic 85.4, both landed 17 lots. Both read the dictionary's go-live sentence and clipped exposure to January 2021, then followed AM-PC-014 step by step. Brief: let that step complete and still return the wrong lot count. Loop 1 moves the wear-out to the module, files module age in rev 4, and makes the replacement the decisive step; the go-live window stays as an ordinary step.
- Loop 1 world without the 2015 service bulletin: rates by relay age reproduce the module-age renewal forecast to within 1 per cent (the population-average rate by relay age already carries the replacement history), so the relay-age route landed on the answer; the bulletin swaps on the pre-1998 relays decouple module age from relay age and put that route 20 per cent low.
- Loop 1 with six bands (30+ on top): after the bulletin no module reaches 30 in the window, so the top band had no exposure; the top band is 25 and over.
- Loop 1 seeds 147, 148, 151, 152: module-months from fitting with no replacement cancelled to within 5 per cent and landed on the answer's lot count; seed 149 landed the staged-scheme last-stage reading. Seed 150 separates every rung.
- Repair 2, first cut of the work-order extract with inspections cut to a realistic cadence: 24,059 rows, under the 25,000-row gate. Volume restored with asset-level work a P&C crew does (transformer-station breaker trip tests yearly, CT checks four-yearly, two-yearly settings audits at transformer stations, more coordination studies), not with inspections.
- Repair 2, a failed module in transit to Veldtek at the count (shipped, not yet received): the stock count would carry it at repair while Veldtek's register would not, a second reading of the modules available. Any box Veldtek has not received by its last save before the count stays on the depot shelf.
- Repair 3, seed 150 kept under the new failure law and station mix: 11 lots, and keeping today's module in every month only two to three lots high, too close for the stump. Seeds 1000 to 1399 searched, then 1000 to 1499 again after the boxing rule changed.
- Repair 3, a repaired module's early-life excess at 1.2 per cent in its first month: one repeat failure reached Veldtek in the draw; 1.8 per cent gives several across seeds.
- Repair 3, boxing a failed module only with one shipping after it: two two-module boxes in the chosen draw; a module waiting at the same store within two weeks either way now shares the box, which leaves when the later one would have.
- Repair 3, a gate that no clause appear in more than 6 per cent of failure write-ups: short generic clauses (RTS, no LEDs) recur in any crew's notes, so the gate measured a property real notes have; with each person's vocabulary widened the gate is 13 per cent and at most 15 clauses recurring 11 times or more.
- Repair 3, SB-15-02 stated as date codes 91 to 97: a relay installed in early 1992 from stores carries a 1990 module, so the range is date codes 97 and earlier.
- Repair 3, keeping the youngest modules from the 2022 to 2025 rebuilds in quarantine: the stock count would then carry recovered modules the dictionary has to explain and the bench-test backlog would run to four years; every module in a retired relay went for scrap with it, and quarantine holds spares returned unused from site.
