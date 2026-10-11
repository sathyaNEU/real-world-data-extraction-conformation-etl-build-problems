# task132 design note: VPR-340 PSU last-time buy

Private, never ships. Architecture v1, drawn 2026-10-11. Seed: `analytical_tasks/01_forecasting/FC03`
(service-parts lifecycle setting only; its withheld-rule shadow-run corpus is capped and not used).

## DRAW

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task132.json`, registered before the ladder, guard PASS (after redrawing context artifact, forum and forcing event, which were BLOCKs against task129 to task131) |
| Domain / task type | energy-systems-utilities / asset-condition-maintenance (client domain itself) |
| Objective | Forecasting & Predictive Modeling |
| Shape | 04, setting one dial (whole lots against a 95 per cent cover bar), with a forecast across periods underneath |
| Gate G mechanism | forecasting |
| Gap, pattern | population (exposure denominator) over time (ageing over the horizon); pattern none |
| Generators | G12 absence of record against record of absence, G13 horizon mismatch, G6 composition shift |
| Stump strategy | population_selection (who is in the denominator: exposure) |
| Layer 2 family / pattern | estimation_fit / `own:delayed-entry-exposure-for-age-banded-failure-rates` |
| Decisive rule filed | yes: AM-PC-014 files the band rates, the relay-month convention, the support end and the cover test. The step it does not write is where relay-years start |
| Official decoy, validated decoy | no, no |
| Decision | dial_setting, answer unit count (lots) |
| Stakeholder | Manager, P&C Asset Planning (capacity_planner); signs off to the Director, Asset Management (line_manager_or_team); forcing event the OEM last-time-buy window (other) |
| Context artifact | filed_standard (AM-PC-014) |
| Calibration form | none, because the strategy needs no corpus: the method is filed and the difficulty is an estimation step |
| World | Ontario, CAD; Tamarack Hydro Distribution (fictional), Veldtek Protection Systems (fictional), VPR-340 (fictional) |
| People | Rachael Villanueva, Kurt Allison, Susan Huff (guard.py names, en_CA, seed 132) |
| Nearest driver on file | task46 at 0.08 (age on the wrong clock); differentiation filed on the card |

**Data-native sentence.** A utility's maintenance system was replaced in January 2021 and its work-order history starts there, while the relays it covers went in from 1992 to 2018; any failure rate by age built from that history has to count exposure only over the window the history can see, and the VPR-340 fleet's middle-aged bands were lived mostly before 2021.

**Layer 1 (the mess, and the systems that make it).** EAM export of every protection asset's work orders (26,700 rows, eight work types, cancelled duplicates raised twice from SCADA alarms, LOG work orders that ship failed modules to the OEM, in-progress orders with no completion date); an asset register holding six relay models, with a region column frozen at go-live; substations with a 2024 regional reorganisation; a renewal programme workbook whose approved 2026 sheet supersedes the 2025 planning sheet (deferrals and schemes brought forward); spares split across depots in serviceable, quarantined and at-repair states, the last only visible against the OEM's RMA log.

**Layer 2 (the shortcut, and why an expert refuses it).** The procedure says a band's rate is failures over "relay-years in service in the band". The shortcut counts each relay's years in each band from its installation date. The numerator holds only failures recorded since January 2021, so relay-years before 2021 sit in the denominator with no chance of contributing a failure: the estimator mixes two observation windows. A reliability engineer recognises this as left truncation (delayed entry): each relay enters the risk set at the later of installation and the start of observation.

## GATE G

- **Litmus.** No reported number or stakeholder conclusion is overturned. Every file is correct: the history is complete for its window, the register is right, the procedure is right. The difficulty is estimating a rate from a window that opened after most of the fleet's middle years had passed. Litmus: no.
- **Primary mechanism:** `forecasting`, with `statistical_rigor` (delayed entry) as the decisive estimation step inside it.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Deletion test.** There is no wrong number to delete. With every voice and distractor removed the ladder is unchanged.
- **Clean-data and instrument tests.** The suspect file is the work-order history (it starts in 2021). Repairing it is not possible inside the fiction (the legacy work orders were archived, not lost in error), and the judge's version of the repair, an instrument that recorded failures back to 1992, would make the install-dated exposure correct and remove the decisive rung. What survives that repair is still a forecast with a real pitfall: the trailing twelve-month rate is 17.6 per cent low, because the forward horizon ages the fleet into its wear-out bands. So the build carries two independent difficulties, one estimation (delayed entry) and one forecasting (age mix over the horizon), and neither is a defect: a coverage window is how every observational record works, and the client lists censoring and truncation as Layer 2 estimation pitfalls. This is the line most exposed at the judge, and it is written here so the rehearsal can test it.
- **Lens swap.** The naive read and the answer are not one population under two lenses: they differ in the exposure window, and the forward relay-months are identical under both.

## THE STUMP

A competent solver builds the procedure's age-banded failure rates per relay-year in service, counting each relay's years from its installation date, applies them to the relay-months each band carries until the renewal programme reaches each substation, and orders 16 lots; the step that lands it there is counting exposure before January 2021, when the work-order history it divides into does not exist.

## LADDER (expected failures, lots, against the answer)

| Rung | Construction | Expected failures | Lots | vs answer |
|---|---|---|---|---|
| 0 | One pooled rate per relay-year, exposure from installation | 68.9 | 2 | -85.3% |
| 1 | One pooled rate, exposure from January 2021 | 229.6 | 9 | -50.9% |
| 2 | Last twelve months' failures per in-service relay, carried over the forward relay-years | 385.6 | 16 | -17.6% |
| 3 | AM-PC-014 band rates, exposure from installation | 383.1 | 16 | -18.1% |
| 4 (answer) | Band rates, exposure from January 2021, each relay to its programme month | **467.8** | **19** | 0 |

Side cells (Layer 1, priced): trailing twelve months' count times the horizon length 703.0 (29 lots, ignores the programme); every relay supported to December 2035 1,120.0 (46 lots); every PSU work order counted, cancelled and LOG included, 649.3 (27 lots) with window exposure and 532.8 (22 lots) with install exposure; the superseded 2025 plan 454.4 (19 lots, converges on the call and misstates the supported relays in most years). Every methodological rung sits at least 17 per cent from the answer, all on the low side, so the decisive move reverses the direction of every shortcut.

**Bin.** With 39 modules available, 19 lots hold for expected failures from 454.2 to 478.2, so the answer sits 2.9 per cent above the lower edge and 2.2 per cent below the upper (asserted at 2 per cent). 18 lots give 84.2 per cent and 19 give 98.3.

## SURVIVAL PROPERTIES (Part 1)

1. Not written: AM-PC-014 4.3 says "relay-years in service in the band" and pins the numerator to every recorded failure; no sentence says where relay-years start. The dictionary states, as any EAM dictionary would, that work-order history starts at go-live.
2. No sweepable corpus nominates it: there is no corpus.
3. No arithmetic symptom: install-exposure rates reproduce every recorded failure exactly in their own back-test (asserted), as do window rates.
4. Not a per-row predicate: exposure is a sum over relay-months, clipped per relay at the later of installation and migration, then grouped by band.
5. Enumeration is arithmetic: which relay-months enter is computed per relay, no column carries it.
6. No cutover date in an outcome series: the migration is a date in the dictionary, not a step in any failure series (failures rise smoothly with age).
7. Survives deletion: nothing wrong to delete.

## CLOSURE TABLE (22 axes)

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | VPR-340 relays in the register; failures per AM-PC-014 4.1 (filed pin) |
| 2 | Unit | relay-month; failure = one CM or EM work order (filed) |
| 3 | Attribution window | failure in its reported month (filed: age on the first of the failure month) |
| 4 | As-of dating | ages on the first of each month from the register's installation date (filed) |
| 5 | Version basis | approved 2026 programme, current at the count (filed 3.1); the 2025 sheet is labelled superseded |
| 6 | Divisor | relay-years in service in the band, over the window the numerator covers: the decisive axis; the install-dated divisor is an inconsistent estimator, not a reading (argued above) |
| 7 | Weighting | rates per relay-year, pooled within band (filed) |
| 8 | Window length | numerator pinned to every recorded failure (4.3 "all of them"), so no shorter window is admissible |
| 9 | Boundary | in service on the first day of a month (filed); support up to but not including the commissioning month (filed) |
| 10 | Rounding | unrounded throughout; every graded figure at least 0.012 from its rounding edge after TUNE (asserted) |
| 11 | Tie-break | none arises |
| 12 | Maturity | all failures in the window are completed work orders; INPRG excluded by 4.1 |
| 13 | Order of operations | rate then exposure then Poisson; commutes |
| 14 | Row order | sums only |
| 15 | Duplicates | cancelled duplicates excluded by status (filed) |
| 16 | Identity | asset_id joins register and work orders one to one |
| 17 | Netting | none |
| 18 | Units | modules and relays are counts; cost CAD per module (notice) |
| 19 | Codes | CM, EM count; LOG, PM, MOD, INSP do not (filed) |
| 20 | Integerisation | smallest whole number of lots (filed) |
| 21 | Clause scope | 3.2 applies to substations outside the programme period only |
| 22 | Forward window | October 2026 to each relay's support end (filed); retired relays carry none |

## ASK SHEET

| Ask | Figures | Device on the ask path |
|---|---|---|
| Lot count, modules, cost | 3 | none beyond the main construction |
| Cover and cost for 15 to 21 lots | 14 | the cover column moves with expected failures |
| Expected failures by year, Q4 2026 to 2035 | 10 | the age mix by year |
| Relays supported on 1 January 2027 to 2035 | 9 | the superseded 2025 sheet; early-retired substations |
| Expected failures by region | 3 | the register's region column is frozen at go-live; the 2024 regions live in substations.csv |

Pair arithmetic: a solver on rung 2 or 3 loses the lot count, every cover cell, every year and every region (all move with expected failures) and keeps the nine supported-relay counts if it reads the 2026 sheet; on the planning weights that is about 5 + 7 + 58 x 9/39 = 25. Criteria: 3 + 14 + 10 + 9 + 3 + memo items (2) + files (2), about 43.

## LEAK REVIEW

(filled at stage 4)

## Tried and rejected

- Healthcare same-day demand censored at sell-out time as task133's first draw (recorded here because it was drawn in the same wave): the censoring was too mild to separate the rungs (bookings 7 per cent low) and two rigorous uncensoring methods disagreed by one session in several cells, a fork.
- Install-date day shifts as the rounding knob: no effect. Install-month shifts: reseeded the failure draw (expected failures moved from 465 to 418), so the knob became a recorded-failure month shift, which leaves exposure untouched.
