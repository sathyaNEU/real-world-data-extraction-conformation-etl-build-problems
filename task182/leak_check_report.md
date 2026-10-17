# leak check, task182

**Verdict: REVIEW.** 13 files read, 57 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: position, measured, residual, record, background, quantity, decisive, subtraction, register, records, asserted, method, energetic, running, architecture, minute, decline, correction, nothing, window, change, criteria, sentence, inside, deployment

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `noise_management_plan.pdf`: carries 3 of 5 distinctive words of the committed call: 'The October acoustic treatment slot should cover NSL04, NSL11, NSL07, NSL02 and NSL13.'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `noise_management_plan.pdf`: 8 of 25 stump-paragraph terms appear (position, measured, residual, record, register, records); read whether the document names the move
- **REVIEW** `survey_notes.md`: 8 of 25 stump-paragraph terms appear (position, measured, record, register, records, running); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: "Put the answer in specific_sound_levels.csv, a row for each of the 14 monitoring positions: the plant's specific sound level in dB LAeq, the valid and the excluded assessment minutes, the one-third-octave band with the h"

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `calibration_records_2026.csv`: 5 ISO dates after 2026-10-16, e.g. 2027-03-11

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

# task182 reader answers (isolated solver read)

Committed answer: slot = NSL04 (53.1), NSL11 (49.9), NSL07 (47.9), NSL02 (47.2), NSL13 (46.0); sixth NSL09 (44.6), short by 1.4 dB. Confidence about 80 percent on the five (NSL06 is the only real challenger for fifth/sixth). Full tables and caveats are in the report returned to the caller.

1. Decisive step: no sentence names it. Plan 3.1 says "less the residual sound ... the sound at the position from sources other than the plant" but never says how to get it. The only pointer is plant_equipment_events_2026.csv: every Tuesday 05:00 to 07:00 all blowers and CHP-01 are STOP ("weekly MCC inspection"), centrifuges start about 07:05; scada shows blower_air and engine_export_kw at 0 in that window. The file's presence and those rows are the hint; the move (use the plant-off window as the residual, outside the 07-19 assessment period) is mine.
2. No file ranks or scores the candidates. monitoring_positions.xlsx distance_m would rank by proximity (nearest five = 04, 11, 02, 13, 06); complaints_register ranks by complaint count (06 has 5). Both are plausible wrong routes, neither is a ranking of the answer.
3. Helper files: none obviously. effluent_quality_2026.csv and complaints_register_2026.xlsx are unused context (survey_notes calls them "not collected for this survey"), a fair distractor pair. The export_manifest.csv is a tidy helper (it lists the gaps) that a real export would rarely carry this neatly. A real effluent file would carry a lab ID, accreditation, detection limits and non-detect flags; this has uniform 24-hour composites every 2 to 3 days with no censoring.
4. Nothing reads as the answer. NSL04 stands out as loudest at 98 m but nothing is labelled.
5. Literal sentences. Plan 3.1: measured = energy-equivalent of valid minutes in the assessment period, specific = measured minus residual in energy. 3.2: 07:00 to 19:00 weekdays local. 4.1: correct deployment if mean of two checks differs from 94.0 by more than 0.3 (subtract the difference; SLM-21907 deployments: mean 94.4, subtract 0.4; SLM-19651: mean 93.4, subtract -0.6 so add 0.6); not used if checks differ by more than 1.0 (none do; max 0.8). 4.2: invalid if rain above 0.5 mm/h or wind above 5 m/s in the ten minutes. Literal result for NSL04: 7200 weekday-daytime minutes (UTC+1 shift, duplicates removed), 6490 valid, measured 53.28, residual 39.39 (Tuesday 05-07 valid minutes, 234), specific = 10log10(10^5.328 - 10^3.939) = 53.1. The pooling of both deployments and the choice of residual window are not filed.
6. What decides it: an analytical choice (how to estimate the residual, and that it must be subtracted in energy; raw measured level swaps NSL06 (46.56) in for NSL13 (46.19)). Hygiene steps that must be right but do not flip the five: UTC to local (+1 h), de-duplicating D08 (120 repeated minutes), -120 dB dropouts, km/h anemometer after 2026-09-20 00:00 UTC, rain tips reset at midnight, calibration offsets. Not planted-defect; the rules in section 4 are stated.
7. Work done. Pooled both deployments per position, dedupe on (meter, minute), local = UTC+1, dropouts (laeq below zero, 83 minutes, D04 and D22) invalid, weather invalid (wind m/s with km/h/3.6 from 2026-09-20 00:00 UTC; any rain tip in the ten minutes since 0.2 mm x 6 = 1.2 mm/h), cal correction, energy mean of valid assessment minutes, residual = energy mean of valid Tuesday 05:00-07:00 local minutes pooled over the position's two Tuesdays.
   Specific dB LAeq (valid/excluded of 7200): NSL04 53.1 (6490/710); NSL11 49.9 (6410/790); NSL07 47.9 (6970/230); NSL02 47.2 (6490/710); NSL13 46.0 (6690/510); NSL09 44.6 (6690/510); NSL06 44.4 (6970/230); NSL01 43.9 (6490/710); NSL03 43.6 (6890/310); NSL12 43.5 (6410/790); NSL14 42.0 (6290/910); NSL08 41.7 (6970/230); NSL05 39.6 (6490/710); NSL10 37.5 (6690/510).
   Choices left to me: (a) the residual estimator (Tuesday stop window; I could not verify it represents weekday-daytime non-plant sound; roadside positions NSL03/06/12 would have higher daytime traffic); (b) NSL06 D22 residual window is mostly -120 dropout (77 of 120 minutes) and the 43 survivors are the loud vehicle-pulse minutes, so pooled residual 42.5 is biased up; using D06 alone gives residual 40.9 and specific 45.2, sixth place by 0.8 below NSL13 rather than 44.4 (then NSL09 44.6 would be sixth, margin 1.4; with D06-only residual NSL06 45.2 is sixth, margin 0.8). Sixth and margin therefore not forced; the five are the same either way; (c) pooling vs per-deployment residual; (d) rain rule (tip in the ten minutes vs rolling hour) and whether the 10-minute stamp is start or end: moves excluded minutes by 10 to 30 at some positions (NSL04 690-740) but not the levels at 0.1 dB; (e) treating dropout minutes as invalid (I did, not stated in the plan); (f) D09 mic move (NSL08) and D16 windshield not corrected, not in the top five.
8. Realism: reads generated in the minute file. NSL04 hourly means are 53.1 flat from 07:00 to 17:00 to 0.1 dB (no diurnal variation of plant or ambient; weather wind hourly mean 3.1 every hour); plant-on minutes sit at e.g. 43.3, 43.3, 43.3, 43.4, 43.3 with identical LA90 and tiny LAmax; 36 percent of minutes have LAmax below LAeq and 13 percent LA90 above LAeq, which a real meter cannot do; the plant-off residual is a clean low floor with vehicle pairs of minutes (+10 dB) dropped in; the weather decile pattern is uniform. The -120.2 / -120.6 sentinel and the duplicated card download are credible mess. One-third-octave quarter hours drop 17 to 20 dB uniformly in the Tuesday window, and the 100 Hz and 400 Hz excess is the same in every deployment of a position (4.15 and 4.21 at NSL01 across two meters, 5.72 and 5.71 at NSL07), too repeatable. Calibration table: meter-level post-check values repeat per meter across every deployment (21907 always 94.0/94.8). Deployment table 'operator' always OOH. Complaint wording is a short repeated list of five phrases. The mic_height_m varies by deployment while the schedule says 1.5 for all. SCADA counters, wrap, hour counter replaced, PLC gap and the distinct plan/clauses read as real mess.
9. Supplementary asks.
   Specific levels: forced to 0.1 for the top five and most others under the stated rules except as in 7(b) (NSL06 44.4 or 45.2).
   Valid/excluded minutes: not fully forced (rain convention and stamp alignment, 10 to 30 minutes; whether dropout minutes count as excluded; whether day uses 7200 deduplicated). My values above.
   Highest band (unweighted, assessment period, weekday 07-19 local, band file is already local): NSL01 100 Hz, NSL02 400, NSL03 100, NSL04 400, NSL06 100, NSL07 100 (42.47 vs 42.10 at 400), NSL09 100, NSL11 400, NSL12 100, NSL13 100. NSL05, NSL08, NSL10, NSL14: no band row (meters 19651/19744 only); NSL04 and NSL13 have a single band-equipped deployment. Forced except NSL07 is a 0.4 dB call, and the weather/cal handling for bands is unfiled.
   Tone (adjacent-mean arithmetic, 5 dB): yes at NSL02 (7.5 at 400), NSL04 (8.9), NSL07 (6.3), NSL09 (5.8), NSL11 (7.8); no at NSL01 4.2, NSL03 4.2, NSL06 3.1, NSL12 3.6, NSL13 4.0. Energy-mean adjacent gives the same. Forced; NSL03 (complaint says a tone) is no.
   Weekly plant figures (weeks Mon 31 Aug...): biogas m3 from the counter with wrap (week-boundary 00:00 readings): 35389, 34824, 34933, 36028, 34377, 35230 (row-sum variants differ by 1 to 3 m3); blower air thousand Nm3 (x0.25 h): 689, 678, 679, week 4 raw 617 vs 704 if the 24-25 Sep PLC gap is interpolated (not forced), 669, 686; centrifuge runs: equipment log gives 12 per week (6 per centrifuge, 2 per day shift), SCADA blocks give 6 per week (5 in week 4 owing to the gap); "run" unit not forced (6 shifts vs 12 starts), week 4 only forced via the log. Gas figures differ by up to 3 m3 with boundary convention.
