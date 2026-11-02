# task138 determinism check (architecture 3)

Two isolated judge passes, each a Sonnet thread at medium effort that saw only a fresh unzip of target.zip, the prompt and the judge's system prompt, and opened the graded blocks only after its own derivation was on disk.

| Round | Pack | Verdict | Disposition | Action |
|---|---|---|---|---|
| 1 | 8bd974fc | DETERMINISTIC, SOLUTION_WRONG in wording only (order kept; F strong; G PASS; H PASS) | FIX_NOW | three solution-step wordings corrected; the switching order puts the moved sections on their new feeders from 00:00 on 1 July; T2 given its own scatter and its 15-minute realignment settled by T1 plus T2 against the historian; CVR filed as standing practice from June 2027; all asserted |
| 2 | 8bf93e16 | DETERMINISTIC (order kept; G PASS; H PASS) | APPROVE | one cosmetic wording fix (critical component 2's relief stated as computed, 1.14 MW), no other graded figure moved and target/ unchanged |

---

# Determinism check, architecture 3 round 1 (2026-11-01): DETERMINISTIC (SOLUTION_WRONG in wording only), FIX_NOW; order kept; Gate F strong; Gate G PASS (statistical_rigor); Gate H PASS

Isolated thread, Sonnet at medium effort, on target.zip 8bd974fc. The main call holds for any CVR effect between about 0.88 and 1.31 per cent.

# Verdict, task138 round 3

Order kept: yes. derivation.md was written to disk before graded_blocks.md was opened. My values for the main call and Ask A matched the golden independently. Ask B first came out different (my first pass dropped the repeated T2 stamp instead of shifting it); I then reproduced the golden's figures exactly by the shift and recorded the finding below.

- **Verdict:** DETERMINISTIC (SOLUTION_WRONG, wording only)
- **Disposition:** FIX_NOW. Correct two misstatements in the solution blocks (step 2 calls the Mossford observations "UTC" but the column is DATE_LST, local standard time; step 7 says "T2 replacement recorder" but no shipped file says a recorder was replaced). No file or prompt change, no model rerun.

## Why
The main call is forced by criteria rev 4 read literally. Pooled least-squares line over the 561 days at 85 F or more in summers 2022-2026 gives 102.93 MW at 101 F, which stands for 2024. Carried at 0.95 %/yr it reaches 105.89 (2027) to 109.97 MW (2031). Section 3.3 then asks for the CVR effect "at the planning peak". The 2025 pilot shows that effect falls with temperature, from 2.3 % on days under 85 F to about 1.03-1.1 % at 99-101 F. At that effect the excess over the 104.0 MW firm rating is 0.80, 1.80, 2.80, 3.82 and 4.84 MW, so the 0.5 MW blocks give 1.0, 2.0, 3.0, 4.0 and 5.0 MW, and the planning peaks round to 105 to 109 MW. Every committed answer reproduced from the files. No gate A-E failure that I could sustain.

## Evidence (recomputed from the bundle)
| Item | Mine | Golden | File / field |
|---|---|---|---|
| WN peak at 101 F, 2024 level | 102.930 (n=561; slope 3.448) | 102.9 | SCADA 2022-23 kW + 2024-26 MW, mossford_ap_obs |
| 2027 carried | 105.892 | 105.9 | forecast xlsx Substations, Dunraith base 0.95 |
| CVR effect at planning peak | 1.03 % (95 % band 0.97-1.08; T>=95 F 1.06; T>=100 F 1.02) | 1.1 % | pilot ratio DUN-2/5/7 to the other five feeders, state from VR_event_log |
| Planning peaks | 104.80, 105.80, 106.80, 107.82, 108.84 -> 105-109 | 105-109 | |
| Transfers | 1, 2, 3, 4, 5 MW | same | criteria 4.1 |
| Energy MWh (DUN-1 to 8) | 16,600; 16,210; 17,670; 11,150; 16,980; 8,990; 14,810; 15,850 | same | mdms + register + SO-2026-114 |
| Ten-day peaks | 94.7 99.1 97.3 91.0 92.9 101.3 101.0 114.1 97.1 95.7 | same | MV90 41-2207 + 41-2208 |

Golden's rejected routes reproduce as well: pilot all-hours 2.4 % (transfers 0.0 in 2027), each day's peak hour on 85 F+ days 1.43-1.5 % (0.5 in 2027). Peak-conditioned estimates from T>=90 F up to the 101 F regression (1.0-1.25 %) all give 1, 2, 3, 4, 5; the transfer pattern flips only below 0.88 % or above 1.31 %, well outside any estimate conditioned on hot days. Upside margin to a block edge is 0.16-0.24 MW.

Forks checked, none moves a committed answer except where marked:
- Round daily Tmax to whole F before the 85 F test (WN 102.77), LST versus clock day (102.95), routine-only observations, dropping 2022, the one cold-front outlier day 2025-08-07, a small correction for the pilot weeks inside the five-summer fit (about 0.03 MW): transfers unchanged.
- CVR not carried past 2027 (the operating plan covers calendar 2027 only): 1, 3, 4, 5, 6. The prompt's "now that the 2027 operating plan runs CVR" and the 2027 to 2031 span read as persisting; low-risk but a real silence in criteria 3.1.
- Ask A, meter multiplier: the three CT meters set 2-3 June read 20 times lower after the swap (3,707 then about 200 kWh/day on a 300 kVA transformer). Multiplying pre-swap days by 20 gives impossible values and overstates DUN-5 by 138 MWh and DUN-7 by 74 MWh. The golden rule (multiply from METER_SET) is the literal one and reproduces. Treating the 11 older CT meters as already scaled would move DUN-1 and others by over 1,000 MWh, but their loading against KVA only makes sense as raw readings (82-810 kW against 106-167 kW for the new meters after x20).
- Ask A, feeder membership: MDMS FEEDER equals the October register for every row, including June, so it is a current-state label. The 12 devices beyond S-1302, S-4471 and S-6120 (9, 7 and 9 transformers) were on DUN-1, DUN-4 and DUN-6 until 30 June 23:27-23:52. Time-varying, 30 June on the old feeder, gives the golden. Using the current label for all 122 days gives DUN-1 16,050; DUN-2 16,830; DUN-3 18,210; DUN-4 10,570; DUN-6 8,360; DUN-8 16,430 (550-630 MWh off). Putting 30 June on the new feeder shifts six feeders by 20 MWh, enough to change the 10 MWh rounding. I judge "delivered" to mean what the circuit carried, so the current-label reading is the weaker one, but the prompt never says so. This is the largest residual fork.
- Ask B, source: 41-2391 (69 kV line terminal L3, Rider LL-1) is not on the feeders. Including it changes five days (for example 08-08 104.0, 06-15 102.2, 08-05 96.2). SCADA feeder sum tracks T1+T2, not T1+T2+L3.
- Ask B, T2 stamps: 41-2208 repeats 2026-06-09 15:30 UTC (2352.9 and 2375.1) and lacks the final 2026-10-01 05:00 interval. Shifting the rows from the second repeated stamp forward by 15 minutes makes the series complete and makes T2 an exact constant multiple of T1 (12/13, std 1e-5). Dropping the repeat instead leaves T2 one interval out of step for the whole summer after 9 June and lowers all ten figures by 0.1 to 0.8 MW (for example 113.6 against 114.1). Derivable from the file (row count, completeness, the constant ratio) but nothing in the shipped files announces it. Both repairs are visible to a careful solver, so I keep Gate C passed, as a flagged risk.
- Ask B, time: no shipped file states the time zone of INTERVAL_END_UTC. Data start at 05:15 UTC (local midnight at UTC-5) and align with SCADA at UTC-5. Every offset from UTC-4 to UTC-7 gives the same daily peaks (peaks fall 17:15-19:45 local); only taking UTC calendar days differs (08-08 100.4, 08-28 96.3, 07-18 90.5).
- Ten hottest days: 08-09, 08-08, 08-06, 06-15, 08-28, 06-26, 09-28, 06-14, 07-18, 08-05 (10th 97.34 F, 11th 95.90 F, no tie).

Solution-block defects (wording only, answers unaffected): step 2 "(UTC, Celsius)" is wrong because the column is DATE_LST; step 7 "T2 replacement recorder" has no support in the shipped files; step 3's "65 CVR and 50 normal hours" reproduces only for a 16:00-20:00 window (13 and 10 days times 5 hours), while the text says "16:00 to 21:00".

## Files/Hygiene: PASS
15 files in three formats (8 csv, 5 pdf, 3 xlsx; one 70,272-row csv, 1.4-3.3 MB CSVs). Decoys and distractors present and unused: OMS_outage_events_2026.csv, the system sheet of the load forecast, the ties workbook, CVR pilot plan, 2027 operating plan reliability table, WPC Exhibit A (used only to exclude L3). No authoring or benchmark language, no solver-facing text. Dates are coherent (forecast accepted June 2025, pilot plan May 2025, operating plan 22 Sep 2026, register exported 9 Oct 2026, data through 30 Sep 2026). Fictional organisation names; nothing public whose canonical result is the answer. Minor realism tell: T2 is an exact 12/13 multiple of T1 across 11,700 intervals, which a real pair of transformers would never show; it is also what makes the repair provable. Not exclusion-level. Cross-batch fingerprint: not assessable inside the allowed folder; nothing in the bundle looks like a reuse of a delivered task.

## Stump power (Gate F)
Strong. The call turns on the CVR effect at planning-peak conditions. The pilot's own averages (2.4 % all hours, 1.4-1.5 % at each day's peak hour on 85 F+ days) are both easy, plausible and wrong (2027 transfer 0.0 or 0.5 against 1.0), and the temperature dependence has to be found and read at 101 F. Nothing shipped states the answer or the dependence. The pilot needs the event log read correctly (DUN-7 on at 09:40 on 14 July, DUN-5 command not executed in the week of 8 September) and a control group. The asks carry their own devices (CT multiplier discontinuity, three moved sections, L3, the T2 shift). Not too easy; stump probability on the main call is moderate to high.

## Stumping type (Gate G)
`mechanism: statistical_rigor` (conditional effect estimate on honest data, feeding a forward planning peak), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported number is misleading; the trailing figures are fine and the difficulty is estimating a treatment effect at the right operating point. On perfectly clean data the task would still stump.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
Domain: weather-normal peak regression, a CVR factor from a switched pilot, N-1 firm-capacity transfer in switching blocks; swapping in hospital or school nouns breaks it. Layer 1: hour-ending against hour-beginning stamps, kW against MW, Bad hours left out, UTC recorder stamps, raw CT registers, a 30 June feeder reconfiguration, a duplicated recorder stamp. Layer 2: the CVR relief at 101 F conditions, not its pilot average. Easy route that survives clean data and correct rule reading: take the pilot's relief over all CVR hours (2.4 %) or at each day's peak hour (1.5 %), which gives 0.0 or 0.5 MW in 2027 and 0.0-4.5 or 0.5-4.5 across the years against the golden 1-5. Criteria 3.3 files the WHAT (effect at the planning peak) and leaves the method (conditioning, interaction, extrapolation to 101 F) open, so this is analysis, not rule application. The asks may turn on data semantics and rule application, which is allowed.

## Fix
solution: reword step 2 (observations in local standard time), step 7 (no replacement recorder is documented; the T2 stamps from the repeated 9 June stamp onward are advanced one interval because the repeat and the missing final interval show the slip) and the step 3 window (16:00 to 20:00 stamps). No change to prompt or input files. Optional hardening against the one real residual fork, no rerun if skipped: the prompt could add "as each feeder was connected on the day" to the energy ask, but that changes what solvers see and would need a rerun, so I do not require it.


---

# Determinism check, architecture 3 round 2 (2026-11-01): DETERMINISTIC, APPROVE; order kept; Gate G PASS (statistical_rigor); Gate H PASS

The re-judge after round 1's FIX_NOW on target.zip 8bf93e16. One cosmetic wording fix in critical component 2 (the relief in MW), moving no graded figure. Isolated thread, Sonnet at medium effort.

# Verdict, task138 r4 (Breckwater / Dunraith)

- **Order kept:** yes. derivation.md was written to disk (own values for every figure) before graded_blocks.md was opened. Cross-batch check: not run (no corpus access in this run).
- **Verdict:** DETERMINISTIC (no SOLUTION_WRONG beyond one cosmetic rounding line, see finding 5).
- **Disposition:** APPROVE. Optional in-house touch-up (finding 5) needs no rerun.

## Why
Every committed answer is reproduced from the bundle alone. Criteria rev4 s3.2/3.3/4.1 file the estimand (five summers 2022-26, line on days at 85 F or more, value at 101 F, carried 3 to 7 years at 0.95 %, minus the CVR effect "at the planning peak", rounded up to 0.5 MW blocks). The data separate the candidate effect estimates: the 2025 pilot shows relief falling with temperature (2.3-2.5 % over all hours or cool days, about 1.5 % at each day's peak hour, 1.0-1.1 % on days near the design temperature), and every estimator conditioned on design-temperature days gives 1, 2, 3, 4, 5 MW. Main call fork risk is low and flagged below; no gate A-E failure.

## Evidence (recomputed from target/, all reproduced unless noted)
| Item | My value | Golden | Source |
|---|---|---|---|
| Fit, days >= 85 F, 2022-26 | n=561, 3.448 MW/F, 102.93 MW at 101 F | 561, 3.45, 102.9 | feeder files + mossford obs |
| Carried WN 2027-31 | 105.89, 106.89, 107.91, 108.93, 109.97 | 105.9 in 2027 | forecast xlsx Substations (0.95 %), base 2024 |
| CVR relief at planning conditions | 0.98 % (log model at 101 F), 1.08 % (hrs 16-20, Tmax>=99 F: 65 on / 50 off hours), 0.99 % (hr 19, >=99 F) | 1.1 % | VR log + feeder MW, pilot vs control feeders |
| Naive relief | 2.49 % all hours, 1.55 % at each day's peak hour, 2.3 % on days <85 F | 2.4 %, 1.5 %, 2.3 % | same |
| Planning peak 2027-31 | 104.8-104.9, 105.8, 106.8, 107.8, 108.8-108.9 -> 105,106,107,108,109 | same | |
| Transfer | 1.0, 2.0, 3.0, 4.0, 5.0 (PP rounded first gives the same) | same | |
| Energy MWh, Jun-Sep 2026 | 16,600 / 16,210 / 17,670 / 11,150 / 16,980 / 8,990 / 14,810 / 15,850 | identical | mdms + register + devices + SO-2026-114 |
| Ten-day demand | 94.4, 98.2, 96.2, 90.9, 92.8, 101.6, 101.2, 112.9, 97.9, 95.5 | identical | MV90 41-2207+41-2208 |

My first-pass demand figures (94.6, 98.7, 96.4, 90.5, 93.0, 101.7, 100.9, 112.6, 97.4, 95.3) differed because I had dropped the repeated 15:30 stamp of 41-2208 on 9 June. The shipped file has 41-2208 with a repeated stamp and no 05:00 final interval; shifting its rows from the repeat onward by 15 min completes the series and tightens the tie to the SCADA feeder sum (hourly ratio std 0.0165 -> 0.0080, min 0.89 -> 1.002). I accept the golden's repair as forced by the file (a duplicate stamp plus a missing end interval plus the reconciliation to the historian), not a semantic choice.

Layer-1 items verified: 2022-23 file is kW and hour-ending (peak hour lands on 19:00 only after the shift); three CT meters (T043654, T043737, T045658) swapped 2-3 Jun 2026 so pre-METER_SET reads are already kWh (applying x20 gives June DUN-5/7 ratios of 1.87/1.3 against a constant 0.97 elsewhere); SO-2026-114 moves 9+7+9 transformers on 1 Jul, mdms FEEDER is the post-move feeder, June is reassigned to the old feeder (June mdms/SCADA ratio becomes the steady 0.97-0.98 on all eight feeders); 41-2391 (69 kV L3, Rider LL-1) is not a feeder (ties are worse with it); a UTC day gives different maxima on 6 of the 10 days; the ten hottest days are unambiguous (10th 36.3 C, 11th 35.5 C).

### Forks I tried and what they give (main call)
| Option the text leaves open | Result | Verdict |
|---|---|---|
| Tmax rounded to whole F / drop 2025 pilot-on days from the fit | WN 102.77; same transfers at relief 0.98-1.1 % | no flip |
| Percent vs fixed-MW relief in later years | same 1..5 at 0.98-1.1 %; 2030-31 flip to 4.5/5.5 only at fixed 0.9 % | no flip in the plausible band |
| Relief estimated from days at/near design temperature (>=90 F: 1.2-1.28 %, >=93 F 1.1-1.15 %, >=95 F 1.05-1.12 %, >=99 F 1.0-1.1 %, 101 F regression 0.98 %) | 1,2,3,4,5 | forced band is 0.89 % to 1.31 % (as-run WN) |
| Relief averaged over all >=85 F days (1.39-1.54 %) or at each day's peak hour (1.55 %) | 0.5,1.5,2.5,3.5,4.5 | the wrong-easy route, ruled out by s3.1 "a day whose maximum temperature reaches the design temperature" and by the pilot's visible temperature gradient |
| All-hours relief 2.5 % | 0.0, 0.5, 1.5, 2.5, 3.5 | wrong-easy route |
| No CVR adjustment | 2,3,4,5,6 | wrong-easy route |
| Drop all of 2025 (not licensed by "as they ran") | 0.5..4.5 | not a licensed reading |

## Findings (none fails A-E; each named with its gate)
1. **Gate C watch, low:** no file pins the temperature population for "effect at the planning peak". A solver who adopts the criteria's own 85 F hot-day population for the relief lands on 1.4-1.5 % and files 0.5..4.5. It is not a reasonable reading (the 85-102 F average is not the effect at design temperature and ignores the gradient the pilot shows), so I do not fail C; the boundary sits at about 1.31 %, 0.2 percentage points above the golden's 1.1 %.
2. **Gate C margin, low (thin but clean):** the 2031 excess is 4.76-4.90 MW against the 5.0 / 5.5 boundary; a relief under 0.89 % (more than 1.5 standard errors below the 101 F estimate) would flip 2031. Every estimator in the design-temperature family stays above it.
3. **Gate A/E on supplementary 3, low:** device ID F-6122 appears twice in the Devices sheet (upstream S-6111 and S-6120, both labelled DUN-2); six transformers hang on it. They belong to the moved section (register feeder DUN-2 is not a DUN-6 child); this is settled only by reconciling mdms to the SCADA feeder energy (alternative shifts about 3 GWh between DUN-2 and DUN-6 and breaks the 0.97 tie). Forced by the files but needs the cross-check; Layer-1 mess, acceptable.
4. **Gate E on supplementary 4, low:** the 41-2208 stamp repair is not stated anywhere; forced by the file itself as shown above. Asks are allowed to turn on data repair.
5. **Solution wording, cosmetic (FIX_NOW, no rerun):** CRITICAL_COMPONENTS item 2 says 1.1 per cent is "1.1 MW in 2027"; 1.1 % of 105.9 is 1.16 MW (1.14 MW with the unrounded 1.076 % used). Either state 1.14 or round to 1.1 consistently; no graded figure moves.
6. No Gate B failure: every decisive fact (firm rating 104.0, design 101 F, growth 0.95 %, 85 F cut, switching block, CVR schedule, pilot states, moved sections, meter swap dates, recorder map) is in a shipped file. Action vocabulary (transfer, switching block) is the criteria's own.

## Files/Hygiene: PASS
15 files; formats pdf (5), xlsx (3: load forecast, ties, transformer register), csv (7); three formats, large files of 70,272, 49,166, 35,136, 15,158 and 5,856 rows. Distractors weighed but unused by the solution: DUN_feeder_ties_2026.xlsx (tie capacity 15.7 MW exceeds the 5 MW need, so not binding), OMS_outage_events_2026.csv, other substations in the forecast workbook, 41-2391 / Rider LL-1, the delivery-point exhibit's DP framing. Files read as operational exports with incidental noise (Bad-quality hours, duplicated stamp, E-status intervals, meter swaps, duplicate device row, hour-ending vs hour-start files, UTC vs local). Temporal coherence holds (plan approved 22 Sep 2026, register 2026-10, data to 30 Sep 2026). No authoring or benchmark language seen in the PDFs or sheets. No exclusion-level finding.

## Stump power
The trap that does the work is the CVR relief estimand: the pilot's relief is 2.3-2.5 % over all hours, about 1.5 % at each day's peak hour and about 1.0-1.1 % on design-temperature evenings, and only the last matches s3.1's planning peak. The two natural easy routes (all-hours or per-day-peak-hour relief) give 0.0/0.5/1.5/2.5/3.5 and 0.5/1.5/2.5/3.5/4.5, each at least a block low in every year; skipping the adjustment gives 2..6. Asks add a stamp slip, a meter swap and a feeder re-sectioning. A strong model reading the rules correctly can still take the easy route, so stump power is credible; it still needs the portal to confirm.

## Stumping type
`mechanism: statistical_rigor` (heterogeneous effect evaluated at the design condition, plus weather-normal regression and growth), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported surface number is overturned; the pilot data are honest and the difficulty remains on clean data. Gate G passes.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
Swap test: a hospital or a school cannot be substituted for a substation weather-normalised peak with a CVR relief evaluated at the design temperature, so the domain is used (planning peak, firm capacity, switching blocks). Layer 1: hour-ending kW against hour-start MW, UTC against local, duplicated recorder stamp, CT meter swap, section transfer on 1 July, Bad-quality hours. Layer 2: estimate the pilot's load relief conditional on planning-peak conditions rather than on all hours or each day's peak hour, and carry it through the weather-normal fit and the block rule. Easy route a capable analyst takes after cleaning and reading every rule: use the pilot's whole-day or peak-hour relief (2.5 % / 1.5 %), giving 0.0 or 0.5 MW for 2027 against 1.0.

## Fix
none required. Optional (solution): align the "1.1 MW in 2027" figure in CRITICAL_COMPONENTS (finding 5). No prompt or input-file change.

