# determinism-check report, task138 round 3, 2026-10-15

The determinism judge's verdict (one isolated thread at medium effort, on the round 3 pack and prompt as built at stage 3, `target.zip` sha256 50c887dca427e7ad), verbatim:

## Verdict: task138 (KBID 2027 order), fresh judge pass r3

Scope note: cross-batch check against other tasks was not run (other task folders are forbidden to this pass). Everything below was recomputed from `target/` only.

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair is required and no rerun is needed. The one optional hardening is to file the estimand for the 31 January root-zone state in the prompt (WHAT, not HOW; see Fix).

**Why:** The 24th smallest of the thirty replays is about 211,565 AF (211,381 to 211,685 across the variants I ran), so the smallest whole thousand covering it is 212,000. I reproduced it independently from the shipped files, and every reasonable way I tried to fit the 2026 delivery share gave the same thousand. The one soft spot is that neither the prompt nor the WOP says how "the root zone as it stands at the end of 31 January" is to be built. The shipped data separate the candidate methods: a model run at Table 4 efficiency misses the soil moisture stations' season by about 0.5 in RMSE, against 0.05 in (their noise floor) when the share is fitted. This is a method fork that the data resolve, not a semantic fork. All 36 lateral figures also reproduce.

## Evidence (all recomputed; file and field named)

Main call.
| Item | Golden | My recompute | Source |
|---|---|---|---|
| Fields on accepted requests | 631 | 631 (47 Superseded and 10 Withdrawn dropped; no duplicate field) | kbid_water_requests_2027.xlsx (Status, Version) |
| Acres | 40,309 | 40,309.43 | same |
| Weather splice | per WOP 6.1 | station39 mm/25.4 to 30 Apr 2014, yard from 1 May 2014, 7 flagged-M and 8 absent yard days filled from station 39; no gaps in the 1997-2026 window | station39_daily_1995-2027.csv, kbid_station_daily_2014-2027.csv |
| Fitted share by method (least squares, 2026 sets, 9 stations) | above Table 4 at all 9 | Drip .940/.932/.936/.934 (T4 .90); Micro .880/.886/.880 (T4 .85); Sprinkler .780/.782 (T4 .75); Border .704/.690 (T4 .70) | kbid_soil_moisture_network_2026.xlsx joined by APN to the register, each UTC stamp read as the end of the day before; sets from kbid_irrigation_orders_2023-2026.csv |
| 24th smallest requirement | between 211,000 and 212,000 (2012 replay) | 211,565 (2012 replay) | replay of WOP 3.1-3.5 and 4.1 |
| Order | 212,000 | 212,000 | WOP 2.3 |
| Ranking and chart | smallest 2024, largest 2002 | 2024 = 163,355; 2002 = 219,461; 24 at or below 211,565; above it 2003, 2010, 2009, 2005, 2021, 2002 | |

The 2026 sets, from the same ordered flows, agree with the turnout meters within +/-3.6% per turnout (mean ratio 1.0003). There are no overlapping or duplicated Delivered sets.

Alternatives for the 31 January state (all other steps held fixed):
| 31 January state | Order |
|---|---|
| Fitted share (golden) | 212,000 |
| 2026 rebuilt at Table 4 efficiency | 215,000 |
| Each field's last set taken as a refill | 209,000 |
| Every field full | 196,000 |
| Every field empty | 221,000 |

The station data refute the last three. The Table 4 route is also refuted by the stations' in-season readings (RMSE .34 to .60 in at the nine non-border stations, against .05 to .09 fitted), though not by their 31 January readings, which read the same under both.

Robustness of 212 (24th-value ranges):
- Fitted share by method mean, pooled fit, or median: 211,564 to 211,662.
- Fit window Apr-Oct or Mar-Nov: 211,611 to 211,614. Same-day stamp reading: 211,381.
- Set water credited entirely to its start day or its end day: 211,685 / 211,549.
- 2026 acres from the request log instead of the crop report: 211,477 (about 90 AF lower).
- 2026 acres on the GIS basis with the share refitted: 211,083 to 211,101, still 212 but only about 85 to 100 AF above the 211,000 line. It is the one variant that comes close.
- Rounding shares to 0.94/0.89/0.78 or 0.95/0.90/0.80 drops to 211,000. A solver who fits properly does not round that coarsely.
- A fit on the post-season window only (Oct 15 to Jan 31) is unreasonable and gives 216,000.

The golden sits near the centre of the 211,000 to 212,000 band. I judge this a thin-but-clean margin: every rigorous fit lands in the same thousand.

Supplementary answers (all reproduce to the stated rounding):
| Lateral | Delivered (AF) | Put in (AF) | Not delivered | Over tail weir (AF) |
|---|---|---|---|---|
| 1 | 17,872 (17,870) | 19,678 (19,680) | 9.18% (9.2) | 578.8 (580) |
| 2 | 17,530 | 19,409 (19,410) | 9.68% (9.7) | 630.6 (630) |
| 3 | 15,399 (15,400) | 16,879 (16,880) | 8.77% (8.8) | 440.1 (440) |
| 4 | 17,888 (17,890) | 21,018 (21,020) | 14.89% (14.9) | 270.1 (270) |
| 5 | 18,162 (18,160) | 19,758 (19,760) | 8.08% (8.1) | 548.5 (550) |
| 6 | 18,211 (18,210) | 21,060 | 13.53% (13.5) | 650.5 (650) |
| 7 | 15,311 (15,310) | 16,711 (16,710) | 8.38% (8.4) | 510.8 (510) |
| 8 | 11,488 (11,490) | 13,110 (13,110) | 12.37% (12.4) | 419.2 (420) |
| 9 | 15,082 (15,080) | 17,371 (17,370) | 13.17% (13.2) | 360.6 (360) |

Golden values in brackets.
- Deliveries come from kbid_meter_book_2026.csv: rollovers carried, CCF converted at 100/43,560, each of 31 swaps chained through Reg. out and Reg. in of the work order in kbid_meter_shop_log_2026.xlsx, and west spur turnouts 05-021 to 05-034 split at their 15 June read (kbid_canal_operations_log_2026.docx). The spur split is 1,719 AF to Lateral 5 and 4,581 AF to Lateral 6. Without the split, Lateral 5's share would be 16.8% and Lateral 6's 5.4%, so the data themselves expose the re-feed.
- Water put in is the heading logger totals plus the Water Master's log estimates. The 32 missing logger days (3,4,3,5,2,3,4,3,5 by lateral) match the 32 log estimates one for one.
- Spills use Q = C*L*H^1.5 with H = gauge less the crest gauge reading less 2 in per board, a reading held until the next one, 1 Feb to 31 Oct. Every board remark time precedes its read time, so there is no same-day ambiguity. Without the board correction the spills would be 660 to 1,460 AF, so the board handling matters, and the remarks ("set 2in brd", "added 2in brd", "pulled 1 brd", "brds out") are unambiguous.
- Three meters are logged "bearing worn, under-reading" (T08017, T01007, T04035). No correction factor is shipped, so the unadjusted reads stand and no fork arises.

Competing answers and forks (Gates C and E):
- 215,000 (Table 4 reconstruction). This is the strongest rival. Table 4 is labelled "design application efficiency ... as WOP 3.5 uses it", i.e. the replay value. WOP 2.4 asks for the root zone "as it stands", an actual state. The stations show the actual shares plainly (see above). I do not find 215 defensible once the sensor series is read. It is the intended trap.
- Fork on the 2026 acres basis (crop report irrigated acres or request acres, versus GIS acres): 212,000 under crop or request acres, 212,000 under GIS with the share refitted, so no flip.
- Whole-thousand rounding, the 24-of-30 count, the 1997-2026 window and the leap-day handling are all filed in WOP 2.3 and 2.4. No fork.
- Literal-reading note: the text is silent on how the 31 January state is to be rebuilt. A purely literal executor has no instruction and must model 2026. The result of the lowest-effort literal route (Table 4) is 215,000, which differs from the golden. I count this as an unfiled method that the data force, not an open fork, because the stations' record is in the package and discriminates sharply. If the author wants zero reliance on the solver's judgement, see the optional Fix.

Gate B: every decisive fact is in a shipped file (efficiency evidence in the soil moisture network and orders; losses in Table 5; weir equations in kbid_canal_structures.xlsx; estimates in the operations log docx). No external dependency. Gate A grain check: the orders file is an event log, the meter book is a cumulative register, headings are daily totals, none is a delta feed.

## Files/Hygiene: PASS (no exclusion-level finding)
19 files. Formats: csv (9), xlsx (6), pdf (2), docx (1), txt (1). One file has 107,067 rows (orders) and one 16,311 (meter book). Real-world mess is native to the systems: former field ids against current ids, superseded request versions, hundred-cubic-foot against acre-foot registers with rollovers, a UTC-stamped sensor series, logger outages with log-book estimates, and mm against inches. Distractors present and unused by the answer: groundwater levels, crop report, TVWA allocation notice (100% allocation, 241,000 AF contract, so 212,000 is within the cap), tail weir structures. Temporal coherence is fine (exports 1 Feb 2027, tables adopted 9 Dec 2025, allocation notice 15 Dec 2026). README_order_working_files.txt is an in-fiction file index with no authoring or benchmark language; mildly artificial but not a provenance violation. No LLM-generation tell found in the files I read.

## Stump power (Gate F)
Strong. A capable solver has to notice that the starting root zone must be rebuilt at all (assuming full gives 196,000; refill gives 209,000), then calibrate the 2026 delivery share to the sensors instead of using Table 4 (215,000), then run the 30-year replay exactly (a single slip moves the thousand). The asks add 36 separately gradable figures with meter rollovers, swaps, a spur re-feed, logger gaps and flashboard remarks, which are independent traps. Too-easy signals: none (nothing in the package documents the share defect or hands out the corrections). Risk the other way: the stump margin is a 3,000 AF (1.4%) gap, so a solver who gets the fit right but errs elsewhere also fails; that is acceptable difficulty.

## Stumping type (Gate G)
`mechanism: method_or_model_selection` (parameter calibration of the delivery share against observed soil moisture, then propagation to a forecast quantile), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
No reported number is wrong: Table 4 is a legitimate design value used as filed in the replays, and the stations are honest data. The difficulty survives clean data, because even then the 2026 share has to be estimated from the sensors. Borderline note: if a reviewer reads Table 4 as "an official figure the solver must reject", the type leans toward a refutation; I read it as calibration, not a catch of a misleading number.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Domain: crop water balance, root-zone state estimation and an exceedance quantile over replayed weather years are irrigation water management proper; swap "hospital" or "visits" in and the task collapses.
- Layer 1: unit and register conversions, id re-keying, superseded versions, UTC stamps, logger gaps, meter swaps. Layer 2: estimate the actual application share from the sensor series and carry the resulting starting root zone through a 24-of-30 replay.
- Decisive step: calibrating the starting state. The easy route a strong analyst who read every rule correctly would take is the 2026 reconstruction at Table 4, which gives 215,000 (not 212,000); the check against the stations that would catch it is analysis, not a rule or a field reading.

## Fix
none required. Optional (prompt, no rerun if the estimand is unchanged): file the WHAT in one clause, e.g. "from the root zone the District's 2026 deliveries and soil moisture readings put each field in on 31 January", without naming the share fit. This would remove the single literal-reading gap noted above. Do not file the least-squares method itself (that would turn the decisive step into rule application).
