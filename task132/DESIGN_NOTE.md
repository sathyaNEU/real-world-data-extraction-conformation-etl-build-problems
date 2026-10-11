# task132 design note: VPR-340 PSU last-time buy

Private, never ships. Architecture v1, drawn 2026-10-11; hardening loop 1 (module-age renewal) after solver round 1. Seed: `analytical_tasks/01_forecasting/FC03`
(service-parts lifecycle setting only; its withheld-rule shadow-run corpus is capped and not used).

## DRAW

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task132.json`, registered before the ladder and re-checked after loop 1 (guard PASS, nearest driver task87 at 0.06); world seed 150 chosen by `seedsearch.py` for loop 1 |
| Domain / task type | energy-systems-utilities / asset-condition-maintenance (client domain itself) |
| Objective | Forecasting & Predictive Modeling |
| Shape | 04, setting one dial (whole lots against a 95 per cent cover bar), with a forecast across periods underneath |
| Gate G mechanism | forecasting |
| Gap, pattern | population (which module is in the relay each month) over time (wear-out across the horizon); pattern none |
| Generators | G6 composition shift (band occupancy moves to new modules as failures are replaced), G13 horizon mismatch, G12 absence of record against record of absence |
| Stump strategy | population_selection (the module-months each band will hold, given failures replace modules) |
| Layer 2 family / pattern | field_method / `own:renewal-of-replaced-modules-in-a-spares-forecast` |
| Decisive rule filed | yes: AM-PC-014 rev 4 files module age from the fitted date (3), rates per module-year (5.3), a monthly expectation of rate over twelve for a module in service (6.1) and expected failures as the band rates applied to the module-months expected in each band (6.2); the purpose (1) and the prompt say failed modules are replaced from the buy |
| Official decoy, validated decoy | no, no |
| Decision | dial_setting, answer unit count (lots) |
| Stakeholder | Manager, P&C Asset Planning (capacity_planner); signs off to the Director, Asset Management (line_manager_or_team); forcing event the OEM last-time-buy window (other) |
| Context artifact | filed_standard (AM-PC-014 rev 4) |
| Calibration form | none: the method is filed and the difficulty is the construction |
| World | Ontario, CAD; Tarrock Hydro Distribution (fictional), Veldtek Protection Systems (fictional), VPR-340 (fictional) |
| People | Rachael Villanueva, Kurt Allison, Angel Baird, George Ray (guard.py names, en_CA, seed 132) |

**Data-native sentence.** A relay's power supply is a field-replaceable module that wears out with its own age, and a module that fails is pulled and replaced with a new one, so the module in a relay two years from now is today's module only if today's module survives two years; for the fleet's oldest modules, a year's wear-out rate carried into every remaining month counts more failures than one relay position can have.

**Layer 1 (the mess, and the systems that make it).** An EAM export of every protection asset's work orders (about 26,000 rows, eight work types, cancelled duplicates raised twice from SCADA alarms, logistics work orders that ship failed modules to Veldtek, in-progress work at the extract date); a rotating-item history for the PSU that starts at the January 2021 go-live with the modules then in place loaded at their legacy fitted dates (including the 2015 service-bulletin swaps on the oldest relays, which show only as fitted dates); an asset register of eight models with a region column that the 2024 reorganisation did not update; a renewal programme workbook whose approved 2026 version supersedes the 2025 plan and builds 27 large stations in two stages by bay; spares across depots in serviceable, quarantined and at-repair states, the last tied to Veldtek's RMA register.

**Layer 2 (the shortcut, and why an expert refuses it).** The shortcut ages the module now in each relay month by month to the end of support and adds its band rate over twelve in every month (the cumulative hazard of today's module). An expert sees that a module that fails is replaced and the replacement starts in the 0-9 band, so the expected failures in a relay are the present module's rate weighted by its chance of still being there, plus the replacement's rate after; summing the hazard counts, for an old module, more than one failure of a module that can fail once. This is the renewal function against the cumulative hazard, the standard distinction in spares forecasting for replaced wear-out items.

## GATE G

- **Litmus.** No reported figure or stakeholder conclusion is overturned; every file is correct. The difficulty is a forecast construction. Litmus: no.
- **Primary mechanism:** `forecasting`, with the expected occupancy of each age band under replacement as the decisive construction.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Deletion test.** There is no wrong number to delete; with every distractor removed the ladder is unchanged.
- **Clean-data and instrument tests.** A perfect instrument (failures recorded since 1992) would remove the go-live window step, which is now an ordinary step and not the stump; the renewal step survives any repair of the data, because it is about the future.
- **Lens swap.** Not one population under two lenses: the naive and the answer use the same rates and relays and differ in which module occupies each relay in each forward month.

## THE STUMP

A competent solver builds AM-PC-014's module-age band rates over the go-live window, ages the module fitted in each supported relay month by month to the end of its support, applies the band rate in every month and orders 18 lots; the step that lands it there is keeping today's module in the relay after it has probably failed, when 6.2 counts the module-months expected in each band and a failed module's replacement starts in the 0-9 band.

## LADDER (expected failures, lots, against the answer; 14 modules available)

| Rung | Construction | Expected failures | Lots | vs answer |
|---|---|---|---|---|
| 0 | Trailing twelve months' failures per in-service relay, over the forward relay-years | 194.4 | 9 | -34.8% |
| 1 | Band rates by relay age (installation date), relay ageing, no replacement | 238.0 | 10 | -20.1% |
| 2 | Module-age rates, module-months counted from each module's fitting (not the go-live), with replacement | 253.2 | 11 | -15.0% |
| 3 | Module-age rates over the go-live window, present module aged forward with no replacement | 411.9 | 18 | +38.3% |
| 4 (answer) | Module-age rates over the go-live window, present module weighted by survival, a 0-9 module after a failure | **297.9** | **13** | 0 |

Side cells (priced): module-months from fitting and no replacement 352.8 (15 lots, the two errors partly cancel and stay two lots high); every PSU work order counted, cancelled and logistics included, 427.2 (18); a staged scheme read by its first stage for every bay 271.6 (12) or its last 324.8 (14); the superseded 2025 plan 259.5 (11); module-age rates with relays aged from installation 697.0 (30); no ageing (current band held) 234.0 (10) without replacement and 188.1 (8) with it; every relay to December 2035 518.0 (22). No rung lands on 13 (asserted).

**Bin.** With 14 modules available, 13 lots hold for expected failures from 286.4 to 310.3, so the answer sits 4.0 per cent above the lower edge and 4.2 per cent below the upper (asserted at 2.5). 12 lots give 83.2 per cent and 13 give 99.1.

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
| 4 | As-of dating | ages from the rotating-item fitted date on the first of each month (filed 3) |
| 5 | Version basis | approved 2026 programme, current at the count (filed 4.1); the 2025 sheet is labelled superseded |
| 6 | Divisor | module-years in service over the window the numerator covers (go-live, dictionary); 5.3 "in the work-order history" |
| 7 | Weighting | rates per module-year, pooled within band (filed) |
| 8 | Window length | numerator pinned to every recorded failure; no shorter window admissible |
| 9 | Boundary | in service on the first day of a month (filed 3); support up to but not including the commissioning month of the bay's scheme or stage (filed 4.1) |
| 10 | Rounding | unrounded throughout; every one-decimal figure at least 0.004 from its rounding edge after TUNE (asserted 0.04 of a tenth) |
| 11 | Tie-break | none arises |
| 12 | Maturity | every PSU failure work order is complete at the count; INPRG excluded by 5.1 |
| 13 | Order of operations | rates, then occupancy, then Poisson; commutes |
| 14 | Row order | sums only |
| 15 | Duplicates | cancelled duplicates excluded by status (filed) |
| 16 | Identity | removal_wo ties each failure to the module it removed; the module in service on the first of the month gives the same module (verify.py) |
| 17 | Netting | none |
| 18 | Units | modules and relays are counts; cost CAD per module (notice) |
| 19 | Codes | CM, EM count; LOG, PM, MOD, INSP do not (filed) |
| 20 | Integerisation | smallest whole number of lots (filed) |
| 21 | Clause scope | 4.2 applies to stations outside the programme period only |
| 22 | Forward window | October 2026 to each relay's support end; the replacement is in service from the month after the failure (3: fitted during the month, in service from the next first day); with the 0-9 rate at 0.0019 a year, a one-month convention shift moves the total by under 0.05 |

## ASK SHEET

| Ask | Figures | Device on the ask path |
|---|---|---|
| Lot count, modules, cost | 3 | the replacement construction |
| Cover and cost for 8 to 22 lots | 30 | the cover column moves with expected failures; the range spans every rung from 9 to 18 lots |
| Expected failures by year, Q4 2026 to 2035 | 10 | the replacement effect grows with each relay's horizon, so later years move most |
| Relays supported on 1 January 2027 to 2035 | 9 | staged schemes by bay; the superseded 2025 sheet |
| Expected failures by region | 3 | the register's region column predates the 2024 regions; the current regions live in substations.csv |

Pair arithmetic: a solver on rung 3 (18 lots) keeps the costs (15) and, if it reads stages by bay, the nine supported-relay counts; it loses the lot call, every non-trivial cover cell, every year and every region. Criteria: 3 + 30 + 10 + 9 + 3 + memo items (2) + files (2), about 59.

## LEAK REVIEW

- Loop 1 `leak.py`: REVIEW. The procedure, dictionary and notice carry six to eight of the call's words (VPR340-PSU-02, lots, modules, last-time buy, Veldtek): the vocabulary of the subject, with no figure from the answer. The dictionary's run date 2026-10-01 is the extract job's stamp. Container audit clean (H1).
- Reader rounds 1 and 2 read architecture 1 (before loop 1): no decisive-step sentence, no ranking file, no planted file; the narrow settings window (13 to 19) was a prompt-level tell and is now 8 to 22; the realism list was taken into the loop-1 rebuild (names, crews, bays, serials, retirements, programme months and scheme numbers, RMA filtering, weekday patterns, labour hours, descriptions, containers).
- Loop 1 reader (round 3): no decisive-step sentence (it took the no-renewal reading, 412 failures and 18 lots, for the answer), no ranking file, no planted file; sixteen realism findings (the EOL PDF's container, planned work on weekends and holidays, corrective-work texture, completion lags, serial-number order, station rebuild cutovers, programme scope, storm wording, the AM-PC-014 container and dating, duplicate bays, RTU wording, workbook containers, RMA working days, feeder reclosing, the EOL repair terms) were fixed in the generator with no graded figure moving (checks 65 and the verifier green, double build byte-identical); two side cells moved (the 2025 plan 260.2 to 259.5, every PSU work order 410.2 to 427.2, neither on 13 lots). `leak.py` now also lists 273 dates after the as-of date: the programme's commissioning months, written as date cells.
- Loop 1 reader (round 4, after the realism rebuild): (filled when it returns)

## Tried and rejected

- Healthcare same-day demand censored at sell-out time as task133's first draw (recorded here because it was drawn in the same wave): the censoring was too mild to separate the rungs (bookings 7 per cent low) and two rigorous uncensoring methods disagreed by one session in several cells, a fork.
- Install-date day shifts as the rounding knob: no effect. Install-month shifts: reseeded the failure draw (expected failures moved from 465 to 418), so the knob became a recorded-failure month shift, which leaves exposure untouched.
- The first world (seed 132): after the leak reader flagged the background work orders as machine-made (substation names like "Basswoodwood", crews named for the 2024 regions from 2021, work dated outside service windows, cancellations and logistics orders only on the analysed path, perfectly regular inspections, one scope line for every scheme), the rebuild changed the random stream and the trailing-rate rung fell to 9.7 per cent low, one lot from the answer. Seeds 140 to 165 were swept and seed 147 taken (trailing rate 30.7 and installation exposure 27.6 per cent low).
- Architecture 1 as built (relay-age rates, left-truncated exposure the decisive step): solver round 1, plain 85.0 and skeptic 85.4, both landed 17 lots. Both read the dictionary's go-live sentence and clipped exposure to January 2021, then followed AM-PC-014 step by step. Brief: let that step complete and still return the wrong lot count. Loop 1 moves the wear-out to the module, files module age in rev 4, and makes the replacement the decisive step; the go-live window stays as an ordinary step.
- Loop 1 world without the 2015 service bulletin: rates by relay age reproduce the module-age renewal forecast to within 1 per cent (the population-average rate by relay age already carries the replacement history), so the relay-age route landed on the answer; the bulletin swaps on the pre-1998 relays decouple module age from relay age and put that route 20 per cent low.
- Loop 1 with six bands (30+ on top): after the bulletin no module reaches 30 in the window, so the top band had no exposure; the top band is 25 and over.
- Loop 1 seeds 147, 148, 151, 152: module-months from fitting with no replacement cancelled to within 5 per cent and landed on the answer's lot count; seed 149 landed the staged-scheme last-stage reading. Seed 150 separates every rung.
