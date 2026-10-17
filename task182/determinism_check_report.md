# Determinism verdict: task182

Isolation: read only this directory (prompt.txt, committed_answers.md, target/, judge_brief.md). Nothing outside it was opened or received. Scratch code is in scratch/.

- **Verdict:** NOT_DETERMINISTIC (the five-dwelling call reproduces; five supplementary answers do not).
- **Disposition:** FIX_NOW. Regenerate the graded blocks and either file or close the five forks below (a one-sentence rain convention, a sentinel rule, a gap rule for blower air, a runs definition, a week-boundary convention for biogas). The main call and its stump stay. No model rerun is needed.
- **Why:** The ranked five (NSL04, NSL11, NSL07, NSL02, NSL13) is forced by plan 3.1 ("both in dB LAeq", "combined and subtracted in energy") applied to the only plant-off record, the weekly 05:00-07:00 stops. The supplementary answers are not forced. (1) The valid and excluded minute counts for all 14 positions differ by 30 to 130 minutes between the literal rain reading of 4.2 and the committed one. (2) The week of 21 September has blower air of 617 vs about 700, centrifuge runs of 5 vs 6, and biogas that moves 1 to 3 m3 with the week-boundary convention. (3) The sixth dwelling and the margin the prompt asks for (NSL06, 0.8) turn on 77 sentinel minutes (-120.2 dB) in one residual window. Labels: prompt_ambiguity (rain, boundary, sentinel), competing_defensible_answer (blower air, runs), solution_incorrect (runs 5).

## Reproduction table (my own code, from target/ only)

Method: dedupe (D08, 120 identical minutes), UTC+1 to local, deployment windows by local date, calibration per 4.1 (signed: mean of checks minus 94.0, subtracted, 11 of 28 deployments: SLM-21907 -> subtract 0.4, SLM-19651 -> add 0.6), weekdays 07:00-19:00 local, wind > 5 m/s (km/h / 3.6 from 2026-09-20 00:00 UTC), energetic means, residual = energetic LAeq over the 240 minutes inside the six Tuesday 05:00-07:00 all-down intervals (two per position).

| Pos | measured | residual | specific (mine) | committed | valid/excl: committed | valid/excl: literal rain (10 min rate) |
|---|---|---|---|---|---|---|
| NSL01 | 44.12 | 31.04 | 43.90 | 43.9 | 6460/740 | 6490/710 |
| NSL02 | 47.34 | 32.38 | 47.19 | 47.2 | 6460/740 | 6490/710 |
| NSL03 | 44.58 | 37.64 | 43.60 | 43.6 | 6830/370 | 6890/310 |
| NSL04 | 53.28 | 39.28 | 53.10 | 53.1 | 6460/740 | 6490/710 |
| NSL05 | 40.52 | 33.35 | 39.60 | 39.6 | 6460/740 | 6490/710 |
| NSL06 | 46.56 | 40.86 | 45.20 | 45.2 | 6900/300 | 6970/230 |
| NSL07 | 48.17 | 35.89 | 47.90 | 47.9 | 6900/300 | 6970/230 |
| NSL08 | 42.24 | 32.89 | 41.71 | 41.7 | 6900/300 | 6970/230 |
| NSL09 | 44.73 | 29.27 | 44.60 | 44.6 | 6640/560 | 6690/510 |
| NSL10 | 38.49 | 31.57 | 37.50 | 37.5 | 6640/560 | 6690/510 |
| NSL11 | 50.08 | 36.24 | 49.90 | 49.9 | 6300/900 | 6410/790 |
| NSL12 | 44.28 | 36.42 | 43.50 | 43.5 | 6300/900 | 6410/790 |
| NSL13 | 46.19 | 32.40 | 46.00 | 46.0 | 6560/640 | 6690/510 |
| NSL14 | 42.48 | 32.64 | 42.01 | 42.0 | 6190/1010 | 6290/910 |

All 14 specific levels, the 53.3 / 39.3 / 53.1 / 0.8 critical components, the 240 residual minutes and the ranked five reproduce. Committed minute counts reproduce only under a trailing 60-minute rain total (tips x 0.2 mm > 0.5 mm summed over the stamp and the five before it, so 3 or more tips); under the sentence of 4.2 ("rain above 0.5 mm an hour for the ten minutes the minute falls in", one 0.2 mm tip in ten minutes = 1.2 mm/h) none of the 14 pairs reproduce. A centred hour changes NSL09/10 by -20 and NSL13/14 by +20; a leading hour by -50/+50; an end-of-interval stamp convention by up to 139. The levels barely move (max 0.005 dB).

Tone and band (assessment period, band file local time; same answers with the file treated as UTC): the committed highest band and tone verdict reproduce for all 10 positions with band rows (NSL01 100/no, NSL02 400/yes, NSL03 100/no, NSL04 400/yes, NSL06 100/no, NSL07 100/yes, NSL09 100/yes, NSL11 400/yes, NSL12 100/no, NSL13 100/no); NSL05, NSL08, NSL10, NSL14 have no rows. Tone excess over the adjacent mean: NSL09 5.54, NSL07 5.71 (closest to the 5.0 line), NSL13 3.38, NSL06 2.73. Top-two band gaps are small (NSL13 0.32, NSL02 0.35, NSL07 0.36 dB) but replicate week to week to 0.06 dB. Weather validity, calibration, UTC or arithmetic vs energy averaging do not change any verdict. NSL04 and NSL13 band answers rest on one deployment only (one week has no band module).

Plant weeks (scada_15min_2026.csv):

| Week | committed biogas | boundary-to-boundary counter | committed blower | recorded rows | gap filled | committed runs | log / distinct days |
|---|---|---|---|---|---|---|---|
| 31 Aug | 35,389 | 35,389 | 689 | 688.6 | 688.6 | 6 | 6 |
| 7 Sep | 34,821 | 34,824 | 678 | 677.6 | 677.6 | 6 | 6 |
| 14 Sep | 34,934 | 34,933 | 679 | 678.5 | 678.5 | 6 | 6 |
| 21 Sep | 36,030 | 36,028 | 617 | 616.8 | 704.1 (interpolated) / 700.2 (mean x 168 h) | 5 | 6 |
| 28 Sep | 34,376 | 34,377 | 669 | 668.5 | 668.5 | 6 | 6 |
| 5 Oct | 35,229 | 35,230 | 686 | 685.9 | 685.9 | 6 | 6 |

Committed biogas equals the sum of wrap-corrected increments stamped inside the week (a counter at Sunday 23:45 less the previous Sunday 23:45). The counter from Monday 00:00 to Monday 00:00 gives a different whole number in 5 of 6 weeks; an increment-within-week sum gives about 55 less. The file does not say which.

## Probes

**Probe 1, residual.** Ways the files let the residual be measured:
1. Energetic LAeq of the all-down stops (committed): ranked five NSL04/11/07/02/13, sixth NSL06 45.2, margin 0.8.
2. Same, dropping the -120.2 dB sentinel minutes: NSL06 44.37, sixth becomes NSL09 44.60, margin 1.4 (the five unchanged).
3. D06 window only for NSL06 (drop the sentinel-laden window): 45.17, as committed.
4. LA90 of the stops (energetic or median), median LAeq of the stops, arithmetic dB mean of LAeq, or no subtraction: NSL06 46.1 to 46.6, NSL06 enters and NSL13 leaves (margin 0.02 to 0.38). These contradict 3.1 ("both in dB LAeq", "in energy").
5. Own-record LA90 (energetic or 10th percentile): NSL06, NSL04, NSL03, NSL11, NSL12 order, five = NSL06, NSL04, NSL03, NSL11, NSL12 (energetic LA90). The plant runs through every assessment minute so this record contains it; closed by 3.1 and 5.1, not by a sentence on where to measure.
The records force reading 1 or 2 for the five. The residual is the only plant-off evidence in the pack (the stops are 05:00-07:00, outside the assessment period). The five holds as long as NSL06's residual is above 37.4 dB; the committed figure is 40.9 and the usable-minute figure 42.5.
The unflagged sentinel: NSL06 D22 (SLM-22043, 29 Sep 05:02-06:59) has 77 of 120 residual minutes at LAeq = -120.2 dB while LA90 in the same minutes reads 6 to 33 dB (so not a quiet reading, a missing flag), and NSL04 D04 has 6 such minutes (0.005 dB, harmless). No shipped file says how to treat it. Including it is the literal reading and gives the committed 45.2 / NSL06 / 0.8; excluding it is what any analyst who sees the LAeq below LA90 would do and gives 44.4 / NSL09 / 1.4. Bootstrap of NSL06's specific level over its non-sentinel residual minutes: 44.3, sd 0.47, 5-95% range 43.5 to 45.0. The sixth place and the margin are not forced.

**Probe 2, window and arithmetic.** Moves against base, rank of the five in every case unchanged:
- No calibration correction: up to 0.31 dB (NSL13), ten levels change rounded value, margin falls to 0.49. 4.1 is explicit, so this is not licensed.
- Calibration sign read as absolute value: NSL13 45.4, NSL04 52.5 (margin 0.2). Literal "that difference" is the signed one; low license but note it.
- No dedupe: 0.001 dB. No UTC to local: up to 3.76 dB; not licensed (2.2 and the notes say UTC).
- Wind unit not switched: -3,010 valid minutes (every position); not licensed. Switch at 00:00 UTC or 23:00 UTC: identical (the minutes are Sunday, outside the period).
- Weekend minutes included: up to 0.24 dB; not licensed (3.2 says weekdays).
- Rain as 10-minute rate vs committed hourly total: up to 0.005 dB on levels, 30 to 130 minutes on counts (not licensed by the committed text; licensed by the plan sentence).
- Remarks on D09 (mic moved) and D16 (windshield replaced): no plan clause, no step in the daily means (D16 53.22 to 53.31); no effect on the call.
Counts: the cal correction applies to 11 of 28 deployments (SLM-21907 and SLM-19651), not "the two deployments" as step 1 of the write-up says.

**Probe 3, supplementary answers.** Minute counts: not forced (above). Bands and tones: forced. Biogas: not forced to whole m3 (convention). Blower air: week of 21 September committed 617 is the sum of recorded rows; the quantity asked is air "delivered" in the week, and the 80 missing quarter hours (24 Sep 13:00 to 25 Sep 09:00) leave about 64 thousand Nm3 out; filling gives 700 to 704. Not forced. Centrifuge runs: committed 5 for the week of 21 September is an artefact of counting feed episodes that treat the two rows either side of the gap as continuous; plant_equipment_events_2026.csv shows 6 CF-01 and 6 CF-02 starts that week (21 to 26 Sep). So the committed 5 contradicts a shipped file, and "run" (plant shift 6, or per unit 12) is itself not defined.

## Three questions

1. **Decisive quantity forced, or forced only by data that cannot separate candidates?** The ranking turns on NSL13 vs NSL06 (measured 46.19 vs 46.56, so measured-only puts NSL06 in). Ways of establishing the specific level for that pair: energetic LAeq stops with sentinel: NSL13 46.00, NSL06 45.20; sentinel dropped: 46.00 vs 44.37; D06 only: 46.00 vs 45.17; mean-dB, median, LA90 or none: NSL06 above NSL13 (46.13 vs 46.15 at the closest, 0.02). The plan's text (energy, LAeq) separates the first three from the others, not the data. Within the licensed ones the data separate with margin 0.8 to 1.6 dB against a NSL06 sampling sd of 0.47 and NSL13 sd 0.03 (residual windows are event-dominated: 5 to 17 loud minutes per 120, the median LAeq is 22 to 33 dB while the energetic residual is 29 to 41 dB). Noise plausibility: between-week agreement of the assessment level at the same position gives chi-square per dof 4.95 over 14 positions (day-to-day standard errors; NSL13 week offset 0.19 dB against se 0.03, NSL14 0.11 vs 0.04 account for most; the other 12 average 1.8), so the record carries real week-level variation and is not noise-free; the one-third-octave gaps replicate with chi-square per dof 0.73 (8 dof); the residual windows between the two weeks give 1.9 (excluding the sentinel; NSL06 alone is 9.4 because of the 43-minute vs 120-minute split). Minute LAeq std is 0.45 to 2.3 dB with lag-1 autocorrelation 0.4 to 0.6 and skew 1 to 4, plausible for an industrial source plus traffic. This bundle sits on neither failure side for the five (noisy enough, separated), but the sixth place is inside the sentinel-handling difference. One tell of construction: ten of the 14 specific levels land within 0.002 dB (seven within 0.001) of a one-decimal value (53.1003, 49.9003, 37.4996, 43.5004, 46.0005 and so on), which a sample of event-dominated residuals would not give by chance.
2. **Rounding edges.** Specific levels, distance to the nearest half-unit edge (under the committed rain convention; the literal-rain reading moves each by at most 0.005): NSL14 42.0054 (0.044), NSL08 41.708 (0.042), NSL02 47.1946 (0.045), NSL05 39.5963 (0.046), all others 0.047 or more; with literal rain NSL14 42.0103 (0.040) is the nearest. Critical components: measured 53.2771 at NSL04 is 0.027 dB above the 53.25 edge (a 53.2 answer would need -0.03 dB, about 70 extra minutes at 50 dB or any 0.03 dB bias); residual 39.2848 is 0.035 above 39.25. One extra minute of record moves a position level by less than 0.003 dB, so no figure flips from a single row or minute. The margin 0.7994 (0.8036 literal rain) is 0.05 from the 0.75 and 0.85 edges. None of these is the weakness; the sentinel treatment (0.83 dB on NSL06) and the calibration sign are.
3. **Does a shipped file rank or score candidates on the prompt's question?** No file ranks specific level. complaints_register_2026.xlsx lists complaint contacts per dwelling (DW-107 five, DW-118 four, DW-121 four, DW-112 three, DW-114 three, DW-104 two, DW-101 two, DW-126 one) which orders dwellings differently, but plan 5.1 states "A complaint is a record of what a neighbour heard and is not a measurement". monitoring_positions.xlsx carries distance_m only. Nothing gets the ranking wrong in print.

## Gates
- **Gate H (three rules):** `domain: pass | layers: pass | decisive_step: analytical`. The deciding quantity is the plant's specific sound level at a dwelling (BS 4142 style: measured less a residual taken with the source off), which an acoustics engineer estimates; swapping in hospital or visits breaks the task. Layer 1 is the UTC stamps, the repeated download, the anemometer unit, the midnight-reset rain count; Layer 2 is finding the plant-off minutes in the process log (they sit outside the assessment period, 05:00-07:00) instead of using the position's own background. The strong analyst who reads the plan and cleans correctly but ranks the measured level, or takes the position's own LA90, files NSL06 in and NSL13 out (measured-only) or NSL06/NSL03/NSL12 (own LA90 minima). The caveat is that 3.1 and 6.1 give most of the recipe, so the step is close to rule application, but where to measure the residual is the engineer's choice.
- **Gate G:** `mechanism: decomposition (ETL conformation feeding it)`, `stumping_family: FINE-numbers`, `surface_read_dependency: no`, `sole_data_defect: no`. The difficulty survives deleting every wrong number (no shipped ranking); not a lens swap, but it is a single pair (NSL13/NSL06) decided by a subtraction whose size at NSL06 is 0.37 dB per dB of residual.
- **Gate A (file grain):** pass for the call; counts and plant weeks fail as above.
- **Gate B (rules/vocabulary):** open fork in 4.2 (rain) and an undefined sentinel and "run".
- **Gate C (margin):** the 0.8 dB margin is clean for NSL13 over NSL06 under 3.1, thin (0.02) if the residual is mis-summarised; the sixth place margin is contested (0.8 vs 1.4).
- **Gate D (objective):** pass. **Gate E (hygiene):** 13 files, formats csv, parquet, xlsx, pdf, md; 282,360-row parquet; 2 distractors (complaints register, effluent quality); no metadata.json in the bundle to check provenance or licence; nothing reads as exclusion-level. No temporal leak (survey notes dated 12 and 16 October, setting 17 October).
- **Gate F (stump power):** moderate. The residual-from-stops step plus a one-pair swap catches the measured-ranking and own-LA90 routes. Too-easy signal: nothing in the plan hides the method. Lever that would not break determinism: file the residual convention (energy LAeq, sentinel minutes as missing) and the rain rule.

## Fix
solution + prompt/plan text: (a) file the rain rule (rate per ten minutes or trailing hour) in clause 4.2 or regenerate counts from the literal one (valid 6,490 etc. above); (b) file that a meter's -120 dB record is a missing minute (or regenerate NSL06 as 44.4, sixth NSL09 44.6, margin 1.4); (c) state that blower air in an interval without a log is filled or left out, and fix 617; (d) define a centrifuge run and correct 5 to 6; (e) fix the week boundary convention for biogas; (f) correct step 1 ("two deployments" is 11 of 28).
