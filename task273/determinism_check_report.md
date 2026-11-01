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
