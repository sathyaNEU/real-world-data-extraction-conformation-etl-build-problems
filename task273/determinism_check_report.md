# Determinism check, task273 architecture 6 (stage 4, 2026-11-01)

One isolated judge thread (Sonnet, medium) on prompt.txt, target.zip d624d9e5 unzipped and the submission's graded blocks; spawned from the main thread because the determinism-judge agent has no Agent tool in this runtime. Its verdict follows verbatim; the repair is recorded at the end.

# Determinism verdict, task273 round 1

- **Verdict:** DETERMINISTIC (main call and the level/PB9/volume answers are forced), SOLUTION_WRONG on supplementary 4 (electricity per ML for PB5, PB6, PB7, PB8).
- **Disposition:** FIX_NOW. Regenerate the PB5 to PB8 electricity block (and its line in the write-up) with the missing SCADA run-hours rows handled, no prompt or input change, no rerun of the main side; see Fix for the one value still exposed.
- **Why:** The call (plan fails, PB3 in February and March, PB9 holds) reproduces exactly from the files and the easy routes give other answers. But the golden PB5 to PB8 kWh/ML only reproduces if a bore with no SCADA daily row on a day (4 days on SB-3, 9 on SB-4) is read as zero run hours, so the whole switchboard energy goes to the other pump, although the permit meters show both pumps delivered 1,800 to 3,400 m3 on those days. Every defensible treatment (fill the hours from metered volume, or exclude the days) gives flat values near 267/266/266/268 (PB5), against golden 267/265/264/273. Gate A fails for supplementary 4, PB5 to PB8 (taxonomy: solution_incorrect).

## Evidence (recomputed from the bundle)
| Item | Result | Source |
|---|---|---|
| Tag map KTG-BH0n to PBn, 23 exact duplicate rows 2021-08-03 to 05 dropped | reproduced | kaitanga_bores_daily |
| Reduced level = ground RL + MP height - pwl; level minus MB1 on all nine takes, least squares 2014 to 2026 (rmse 0.035 m, MB1 slope 1.00) | reproduced; interference matrix symmetric (PB3/PB4 -0.366/-0.368) | daily csv, register, MB1 |
| PB9 effect per ML/d: PB3 -0.663 (se 0.0034), PB4 -0.108; at 4.40 ML/d 2.92 m and 0.48 m | matches "3.0 m / 0.5 m" | PB9 logger moved UTC to NZDT, 8 test days |
| 32 lowest levels, Dec to Mar, nearest 0.5 m (MB1 lows 32.737, 31.074, 30.309, 30.201) | all 32 equal golden; closest to a rounding edge 0.14 m (PB7 Dec 28.395, PB1 Jan 29.394) | plan xlsx, SWS-03 |
| PB3 raw: Dec 33.98, Jan 34.48, Feb 35.45, Mar 35.50 vs 35.0 | fails Feb, Mar; every other bore passes | |
| PB9 (own drawdown from test net of neighbours' draw, a9 = +1.00 from both static readings): lowest 32.6, 33.9, 34.7, 34.7 vs 38.0 | holds | logger, coefficients |
| 32 volumes, local quarters (23:00 NZST edges), 1,000,000 rollover on WM-30456 and WM-35873, PB4 = WM-31702 + WM-40958 | all 32 equal golden | telemetry |
| Meter to bore: telemetry vs SCADA daily take correlation 1.000 for WM-30455 to PB2, WM-30456 to PB1, WM-33119 to PB6, WM-33120 to PB5; others 0.70 or less | forced by data, contradicts permit Schedule 1 | permit pdf |
| Electricity PB1 to PB4 (UTC to NZ local, MT921-02 x40 by meter_serial) | all 16 equal golden | icp csv, register |
| Electricity PB5 to PB8 (split hours x motor kW, zero hours for a missing row) | reproduces golden only under that treatment | see below |

Competing answers tried:
- Plan passes: ignore PB9 on neighbours (PB3 Feb 32.5). Plan fails at PB4 not PB3: infer by map distance (PB9 is 172 m from PB4, 326 m from PB3). Both are the easy routes, both wrong.
- PB9 fails: take its "static" as undisturbed and add the neighbours' draw again (double count, 40.0 vs 38.0 in Feb and Mar). The daily file shows the neighbours pumping during the test, so this is an error, not a reading.
- SB split hours only: PB5 243 against 267 with hours x kW. Not stated in the prompt or a file. The data separate them (SB-3 energy regressed on the two run hours gives 40.8 and 33.5 kW, ratio 1.216 = 45/37; SB-4 41.5 and 50.7, ratio 0.82 = 45/55 within 1%), so hours x kW is the forced split.
- Missing run-hours days (SB-3: 2025-12-23 PB6, 2026-02-15 PB5, 2026-04-10 PB6, 2026-06-01 PB6; SB-4: nine days, e.g. 2026-01-26 PB8): golden (zero hours) PB5 267/265/264/273, PB6 258/253/260/254, PB7 261/263/268/258, PB8 343/339/333/345. Fill from metered volume / observed 153.6 m3 per run hour: PB5 267/266/266/268, PB6 258/256/256/259, PB7 265/264/264/265, PB8 338/337/337/338. Fill at duty flow, or exclude the days from both energy and volume, give the same integers except PB8 Apr to Jun (338.4 to 338.5) and PB7 Jan to Mar (264.45 to 264.50). Golden differs from the filled values by up to 8 kWh/ML.

Minor Gate E/C notes: "each of those bores' pump electricity" has two antecedents (all eight in supply, or only the failing bore); the golden reads all eight, which is the natural reading and a superset. The permit Schedule 1 meter list (WM-30455 = Bore 1 etc.) disagrees with the telemetry for two pairs; a solver who trusts the permit swaps PB1/PB2 and PB5/PB6 volumes and kWh/ML. The data resolve it, so it is layer-1 key mess, but nothing in the files says which source governs.

## Files/Hygiene
PASS. 12 files; formats csv (8), pdf (2), xlsx (2), so 3 formats; telemetry 279,913 rows; distractors present (nitrate series, rainfall, permit conditions, PB9 logger step test). Timeline coherent (PB9 drilled 2026-08-27, pump 2026-09-29, test 5 to 14 Oct, plan 28 Oct, MB1 export 2 Nov). No authoring or benchmark language found. Fit is unusually exact (rmse 0.035 m) so the data read as generated, but nothing exclusion-level. Cross-batch fingerprint: no prior packages available to this reader, not assessed.

## Stump power
Moderate to good. A strong model that fits each bore on its own take (or on all eight takes) and does not use the October test as an interference source files "plan passes" (PB3 Feb 32.5 m); one that reasons by map distance files PB4. Reading the dip from the test days through a multi-bore regression is the stump. The supplementary side is heavy conformance work (UTC to NZST to local, rollover, meter swap, x40, key mismatch), which carries ask weight, not the call.

## Stumping type
`mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported levels and takes are fine; the difficulty is specifying interference (superposition across a new bore) from a pump test; on clean data it would still stump.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1: tag change in 2019, doubled gateway batch, datum offset, UTC vs NZDT vs NZST, meter rollover and swap, x40 register, permit meter key mismatch. Layer 2: drought-test interference drawdown from a constant-rate test (hydrogeology, not a backdrop: swap "megalitres" for "visits" breaks it). Easy route a careful analyst takes: each bore's own drought curve with no PB9 draw on neighbours, giving "plan passes" (or a distance argument giving PB4).

## Fix
Where: solution (golden xlsx PB5 to PB8 electricity sheet, and the write-up step 7 and figures). Regenerate with the missing run-hours rows filled from the metered volume (or excluded with their energy and volume) and say so in the write-up steps. Because PB8 Apr to Jun and PB7 Jan to Mar sit on a rounding edge across the defensible fills, either pin the treatment in the prompt/sheet note or nudge the data so the edge is cleared; if the data are touched, that part becomes a rerun.

## Round 1 repair

The shared-board pumps carry a SCADA row on every day of 2025-26 (the SB-3 and Paddock 14 radio links replaced in June 2025), each board's load factor is set so no electricity figure sits on a rounding edge, and the prompt's 'each of those bores' reads 'every bore now in supply'.

## Re-judge (round 2), verbatim

# Determinism verdict, task273 r2 (re-judge after the sup 4 FIX_NOW)

**Verdict:** DETERMINISTIC (main call forced and reproduced; two filed-nowhere conventions on the supplementary sheets remain, see Evidence).

**Disposition:** FIX_NOW. Optional in-house pins only (no change to the main call, the stump or any graded figure): file in the prompt (a) which meter belongs to which bore is taken from the bore the meter's volumes track (Schedule 1's meter column disagrees with the telemetry for Bores 1/2 and 5/6), and (b) that a shared switchboard is split between its pumps each day by run hours times motor rating. No stump-bearing file changes.

**Why:** At the plan's 4.40 ML/d PB9 lowers PB3 by 2.91 m (PB4 by 0.47 m) in its 8 to 13 October constant-rate test; with that in the multi-bore drawdown model PB3 reaches 35.45 m (Feb) and 35.49 m (Mar) against 35.0 m, nothing else fails, PB9 holds. Every defensible estimate I ran gives the same fail set and the same rounded table. The residual risk is in sup 4 and 5 (meter-to-bore key and the shared-board split), not in the call.

## Evidence (recomputed from the bundle)
Main call and sheet 1 (kaitanga_bores_daily, MRC_MB1, PB9 logger, register, plan, SWS-03):
- Conformed: KTG-BH0n to PBn (continuity at 13/14 May 2019 on take and level, no permutation), 23 exact duplicate rows Aug 2021 dropped, PB9 UTC to NZDT (full test days 8 to 13 Oct, 4.404 to 4.413 ML/d).
- Model: level + MB1 on all nine takes plus intercept, 2014 to 2026, residual sd 0.035 m for every bore (no hidden defect). PB9 coefficients: PB3 0.662, PB4 0.106, PB5 0.234, PB2 0.228, PB6 0.164, PB1 0.140, PB7 0.116, PB8 0.085 per ML/d. Fitted matrix is symmetric (reciprocity holds).
- Lowest PWL reproduced to 2 dp, then rounded: PB1 28.05/29.40/29.89/30.03; PB2 28.43/31.41/31.98/31.95; PB3 33.98/34.48/35.45/35.49; PB4 33.05/34.02/34.95/33.98; PB5 29.55/30.54/31.47/31.03; PB6 29.51/30.04/30.53/29.06; PB7 28.39/29.03/29.57/29.95; PB8 26.46/27.09/27.97/27.95. All 32 cells equal the golden's rounded grid.
- Robustness: start 2019 / 2020, MB1 coefficient free, UTC-day PB9 takes (PB3 35.33/35.38), full test days only: max shift 0.12 m, same fail set, same rounded grid except none. The nearest rounding edges are 0.14 to 0.2 m clear. Ignoring PB9 (own-curve route) gives PB3 32.5, no failure, plan "passes".
- PB9 itself: static 53.24 (level + MB1) from the two static spells (Oct 5 and Oct 6, they differ only by the neighbours' day takes), own drawdown 6.9 to 7.0 m at 4.4 ML/d, plus neighbours by reciprocity: peak PWL 32.5/33.8/34.6/34.6 against 38.0, margin over 3 m. Holds.
- Competing answers: "plan passes" (own curves) is the easy route and is wrong; "PB4 fails, PB3 passes" (distance decay, PB4 is 172 m from PB9, PB3 325 m) contradicted by the test dips (PB4 0.47 m vs PB3 2.91 m). Raw before/after dip (2.6 to 2.8 m) gives PB3 35.1 to 35.2, still a fail but rounds to 35.0, so the controlled estimate is needed for the grid. Permit condition 5 (MB1 below 30.00) never triggers, design-drought minimum is 30.201. Site totals (27.65/26.0/25.85/24.9) are under 28.5 ML/d.

Sup 5, permit-meter volumes (MRC telemetry, NZST to NZ local, rollovers of WM-30456 on 24 Jul and WM-35873 on 13 Aug 2025 added back 1,000,000 m3, meter totalisers differenced at local midnights): all 32 cells reproduce the golden exactly, with WM-40958 continuing PB4 from 17 Feb 2026 (first interval 10:15 to 10:30 unmeasured, about 0.04 ML, does not move 232.1).
Sup 4, kWh per ML (pump_icp_interval_data, UTC to NZ local, PB2 multiplier 40 from 10:30 local 11 Feb, SB-3 and SB-4 split by daily run hours times motor kW, divided by the sup 5 volumes): all 32 cells reproduce (e.g. PB3 302.88/305.31/310.04/316.12, PB5 263.04/261.78/262.30/263.93). Every bore now in supply has a SCADA row for every day of the year on the shared boards (the round 1 repair holds); PB9 is "commissioning", has no electricity or meter record in the year, correctly excluded.

Open forks (answers each produces):
1. Meter-to-bore key. Permit Schedule 1 lists Bore 1 = WM-30455, Bore 2 = WM-30456, Bore 5 = WM-33119, Bore 6 = WM-33120. The telemetry tracks SCADA the other way round (daily r = 1.000: WM-30455 to PB2, WM-30456 to PB1, WM-33119 to PB6, WM-33120 to PB5; metered 735.7 vs SCADA PB1 922.2 ML would be a 20 percent miss against the permit's plus or minus 5 percent). Flow rates agree (WM-30456 48.1 L/s = PB1 duty 48.6; WM-30455 39.9 L/s vs PB2 41.7), and the PB1 and PB2 switchboard kWh per run hour match. WM-40958 is in no shipped key, so tracking is unavoidable for PB4. No shipped sentence says Schedule 1 is out of date. Literal Schedule 1 mapping changes the 16 volume cells and 16 kWh/ML cells of PB1, PB2, PB5, PB6 (e.g. PB1 Jul-Sep volume 155.5 not 205.1). The data decide it overwhelmingly, so I hold it as forced by the evidence, but it is the weakest link.
2. Shared-board split is not filed in the prompt. Run hours times motor kW (golden) vs run hours alone vs metered or SCADA volume vs hours times duty flow: PB5 263 vs 240 to 258, PB6 254 vs 258 to 280, PB7 268 vs 296 to 304 (16 cells differ). The board's own kWh pins it: regression of daily board kWh on the two run-hour series gives 40.6:33.5 (SB-3) and 42.1:51.5 (SB-4) kW, the nameplate ratios 45:37 and 45:55 to within 0.4 percent, and a fitted-draw split reproduces all 32 cells. Within the golden convention, allocating on quarter totals instead of days moves one cell: PB6 Jan-Mar 252.35 (golden, 252) vs 252.51 (253).
3. A 00:00 reading closes the previous day. Grouping the increment by the reading's own date moves 6 volume cells by 0.1 ML (e.g. PB1 Apr-Jun 139.9 vs 140.0); differencing at local midnights (golden) is the physical reading.

## Files/Hygiene: PASS
12 files; formats csv (8), xlsx (2), pdf (2). One file over 25,000 rows (telemetry 279,913; pump intervals 105,120; daily 37,103). Distractors present and unused: nitrate, rainfall, permit combined-take and MB1 trigger conditions. No authoring or generator disclosure in the files; PDF and xlsx metadata name people and organisations in the fiction only. Temporal: PB9 test (5 to 14 Oct) precedes the permit variation (19 Oct), plan 28 Oct, MB1 export 2 Nov; coherent. Real-world contamination: none, fictional site. No exclusion-level finding. Deck not in the pack, not assessed.

## Stump power
Good. A strong model that cleans the data and reads SWS-03 can still file "passes" by fitting each bore's own curve on MB1 and its take (PB3 about 32.5 m), or fail the wrong bore by letting map distance set PB9's draw (PB4). Only a joint fit of all nine takes with the pumping test's response decides it. PB3's margin over 35.0 is 0.45 m, well inside what the controlled estimate resolves; the asks add a second layer (meter key, DST, rollovers, ×40 meter, board split).

## Stumping type
mechanism: method_or_model_selection (multi-bore interference from a constant-rate test, reciprocity, design-drought superposition), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no. No reported figure is wrong; the plan's per-bore take table and the drought curve are fine, the difficulty is the unmodelled neighbour interference, and the task still stumps on perfectly clean data.

## Three rules
domain: pass, layers: pass (Layer 1: KTG tags, duplicate batch, UTC vs NZDT, NZST telemetry, totaliser rollovers, meter swap, x40 register, shared boards; Layer 2: borefield interference), decisive_step: analytical. The field's own analysis is drawdown superposition from a pumping test under a design-drought boundary; the easy route (each bore's own curve, or distance-ranked influence) files "plan passes" or "PB4 fails" and is wrong. Swap test: replacing bores with another asset breaks the task.

## Fix
prompt (optional pin, no rerun of the stump): name the meter-to-bore basis ("each meter assigned to the bore whose daily take it matches") and the shared-switchboard split basis ("by daily run hours times motor rating"); alternatively correct Schedule 1's meter column order if the authors accept a re-cut of that one file. Solution blocks need no change.

## Round 2 answered

DETERMINISTIC on every graded figure. The judge's optional pins (naming the meter-to-bore matching and the shared-board split in the prompt) are not filed: each would name its ask's device and hand the ask over, and the judge found both forced by the data (meters at daily r = 1.000, a 20 per cent miss on the Schedule 1 reading against the permit's 5 per cent; the boards' own kWh fit the nameplate ratio within 0.4 per cent). Its two convention sensitivities are closed by construction instead: the volumes are graded in whole ML with each meter's error set so a reading's own date and its quarter-hour's start date round alike, and each board's load factor set so a day-by-day and a quarter-total split round alike; both asserted in checks.py.
