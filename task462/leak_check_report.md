# leak check, task462

**Verdict: REVIEW.** 27 files read, 19 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: surface, asserted, height, contractor, density, register, golden, sentence, conformed, contractors, systems, record, nothing, checks, decisive, lattice, rotation, procedure, roll-forward, report, lowest, control, laboratory, harbour, reclaimed

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `fuel_security_procedure_PR-07.pdf`: golden figure 3.2 appears: ...wn in December by the plant's survey contractor. 3.2 Reserve: the tonnes of coal held in the coal yar...
- **REVIEW** `fuel_security_procedure_PR-07.pdf`: carries 14 of 16 distinctive words of the committed call: "Do not nominate Silesia's winter option cargo: the coal yard held 150,000 t at the 16 December survey, 62 days of the fi"

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `fuel_security_procedure_PR-07.pdf`: 8 of 25 stump-paragraph terms appear (contractor, density, register, record, procedure, control); read whether the document names the move
- **REVIEW** `survey_control_report_2026-07.pdf`: 7 of 25 stump-paragraph terms appear (surface, height, register, systems, lattice, report); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `coal_burn_plan_2027Q1.xlsx`: 2 ISO dates after 2027-01-04, e.g. 2027-02-15, 2027-02-17

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 12 describing content (REVIEW 1)
- **REVIEW** `fuel_security_procedure_PR-07.pdf`: names 7 column(s) of the data files verbatim (Days, cargo, contractor, date, tonnes, unit): confirm it is the organisation's own record and not a note written for the analyst

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read, architecture 1 (the old methane-ratings pack, target.zip 33e6d0c4, superseded; kept as history)

1. Decisive step. No sentence names a correction, but the standard's definitions bound it. tarvane_low_methane_rating_standard_2026.pdf 4.3: "A site's methane emitted ... is the site's emission rate at 5 kg per hour or more, averaged over the campaigns flown in that part with each campaign counting equally, times the hours in that part." talmora_survey_methods_note_2026.pdf 2.1: "A pass does not detect every plume: the chance of detecting a plume rises with its emission rate." Also 4.2: "the chance that a pass detects a plume as a logistic function of the natural logarithm of the plume's emission rate alone, fitted by maximum likelihood to the study's releases". No file says to gross up for missed plumes. What I think decides it: detected plumes undercount emissions, especially just above 5 kg/h, so a fitted detection curve (controlled-release workbook) and perhaps a quantification-bias check should adjust the sum before intensity is compared with 0.20. Nothing states that step. The note and workbook only supply the ingredients. The pack never says "correct for detection".
2. Ranking file. None. Closest context: ghgrp_subpart_w_tollaver_facilities_2023_2025.csv (producer CH4 by source, 2023-2025, a different basis) and the satellite JSON (basin total only, "does not resolve individual facilities or operators"). Neither ranks producers on the question.
3. Helper file. None as a hint. The data dictionary (tarvane_rating_folder_data_dictionary.xlsx) and manifest are plain field definitions. The talmora_controlled_release_study_2025.xlsx is a validation dataset, and the methods note section 4 describes it neutrally; it is the nearest thing to a pointer to the method but gives no instruction.
4. Answer-like figures. None. The 0.20 per cent threshold is in the prompt and standard 3.1, which is context. No producer-level intensity or rating appears anywhere. The note's wording "Talmora describes the chance that a pass detects a plume as a logistic function of ln(rate) alone" is the nearest to a method hint (see 1), though it is validation prose and states no use.
5. Sentences bearing on plume-to-annual methane (all in the standard unless noted):
 - 2.5 "Measured methane intensity: the methane the producer's sites emitted over the rating year at rates of 5 kg per hour or more, measured with the year's aerial campaigns, as a share of its methane produced, both in metric tonnes; in per cent."
 - 4.2 "A plume belongs to the register site nearest its estimated origin within 150 m."
 - 4.3 (quoted in 1) plus "A site imaged on two lines in a campaign counts the mean of the two passes; a campaign that left a site without an image does not count for that site."
 - 2.2 "A site counts to the producer operating it on the day a campaign images it, and for the part of the rating year that producer operated it."
 - 2.4 methane produced: latest report per well and month, "at 14.73 psia and 60 °F" (dictionary says OGC gas_mcf is at 14.65), times methane share of the field's latest composite, 19.2 kg per Mcf.
 - 4.1 "a line lost to cloud leaves its sites without an image in that campaign".
 - Note 1.2, 2.1, 2.2 (rate uncertainty 20 to 30 per cent), 2.3 (nearest facility within 150 m), 3.1 (coverage lists imaged or not), 4.2 (logistic on ln rate).
 Literal execution: for each site and campaign, sum plume rates of 5 kg/h or more detected (my reading: summed per line, then mean over the lines imaged), average over imaged campaigns equally in each operator's tenure, times hours, no detection correction. My rough computation (plume rate at or above 5, mapped via register facility numbers, tenure split at operator_since, composite latest, 14.73/14.65 scaling) gives intensities: Calbrent 0.076, Ostrel 0.084, Corrandale 0.108, Brushy 0.125, Anchell 0.148, Pinyon 0.153, Pellisto 0.177, Ashmund 0.179 (eight at or below 0.20), then Lechuza 0.213, Sunmere 0.230, Marrowind 0.233, Ruskmoor 0.386. This is approximate and my pressure conversion and zero-for-no-plume handling are unverified. The detection-corrected figures would be higher, so the set rated would shrink; the literal text does not do that correction.
6. What decides it: an analytical choice. The literal standard yields a plume-sum count, and a strong analyst who cleans the data and follows 4.3 exactly gets a set of producers that the detection-probability and quantification evidence (methods note 2.1, 4.2 and the workbook) would change. The deciding step is the estimand adjustment (whether and how to correct detection) and is not stated anywhere. Supporting cleaning layer: operator changes (7 Calbrent sites to Sunmere 2026-07-01, 6 Ruskmoor sites to Pellisto 2026-04-01 in the register), cloud-lost lines, two-line sites, amended reports, pressure base, composite choice. These are semantics and rule application, not the decider.
7. Realism tells. Mostly clean. Items: (a) ogc_flaring_venting_reports has a third disposition code FR (3,751 rows) not defined in the dictionary (only FL and VT). (b) Operator names in the register are shortened ("Calbrent Energy", "Pinyon Draw Production") and the producers sometimes operate sites with other producers' names ("Ostrel Lechuza 19-2 Pad", "Marrowind Corran 13-1 Pad"), plausible as acquisitions. (c) The OGC well file's 16 operator numbers include four small ones outside the twelve rated. (d) Round 18 lines per campaign, 4 campaigns at near-identical dates, rate_uncertainty and nearest_facility consistent. (e) Controlled-release study: 182 releases exactly as stated, rates continuous, fine. (f) The satellite JSON ranges are tidy. (g) The standard says it was "Version 1.1 ... Supersedes version 1.0 (11 March 2025)" and the manifest includes as_of dates after the standard (data dictionary dated 2026-11-18, after the note issue date 2026-10-12), so the setting is ambiguous (the pack says 2026 Nov). No LLM-flavoured prose found; the PDFs are terse and plausible.
8. Ask-figure forks.
 Gas delivered to the plant (tollaver_plant_allocation_statements, meter stations, heating values):
 - Readings: (a) sum of volume_mcf by shipper over statement months Oct 2025 to Sep 2026 with latest revision (R2 for 2026-03), including or excluding PPA (prior period adjustments) lines; (b) bill by statement month (Alloc line + PPA) versus by the production month the PPA refers to; (c) stations with blank volume (M-133 and M-169 from 2026-07, energy only) converted from energy_mmbtu / heating value (heating values file), at 14.73 psia (dictionary) which matches the standard base, versus taking OGC 14.65; (d) 2026-10 statement is outside the year; (e) R1 versus R2 for 2026-03 (R2 is a complete resubmission of 45 lines). The files settle some: dictionary says "Gas received, thousand cubic feet at 14.73 psia", and the plant's statements each month. They do not state the PPA treatment, revision precedence, or the energy-only conversion. Decisive fields: reference, revision, statement_month, volume_mcf/energy_mmbtu, heating_value_btu_scf. Shipper to producer via the meter station file (operator_number). Also a producer's shipper mapping covers only the Sunmere/Calbrent site handover, not delivery.
 Gas flared (ogc_flaring_venting_reports, lease register, summary):
 - Readings: (a) FL only versus FL plus VT (vented is not flared); (b) FR code (undefined, plausibly "fuel/flare returned" unknown) included or not; (c) AMENDED replaces ORIGINAL by lease and month; (d) rating year Oct 2025 to Sep 2026 by production_month versus received_date; (e) lease operator via lease register effective_date (13 leases changed hands after 2025-10-01, so the producer by month); (f) units Mcf versus the "whole million cubic feet" asked, rounding Mcf/1000. The dictionary settles FL flared, VT vented, volume_mcf, AMENDED replaces; it does not define FR or lease handover splitting. Decisive field: disposition_code (FR) and lease register effective_date.
9. Name check. Nothing misspelled-looking. All names read fictitious (Tollaver, Talmora Aerial, Tarvane, Mossreed, etc.). EPA GHGRP and "Subpart W" are real programme names used correctly, and "TROPOMI-class" is a real sensor family. "State Oil and Gas Commission" generic.

Verdict: REVIEW. No file hands over the detection-correction step or any producer's rating. Items to look at: the undefined FR code (genuine semantic fork on the flaring ask), unstated PPA/revision precedence on the delivery ask, and the methods note section 4.2 ("logistic function of the natural logarithm of the plume's emission rate alone") which is close to announcing the method for the decisive step, though it is phrased as validation.

## Solver's-eye read, architecture 2 (this pack, target.zip 07da6cdd)

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), architecture 2, on a fresh copy of prompt.txt and target/ (target.zip sha256 07da6cdd4d1288e828c3f52219dab9a76e11d9d712ba9fb0364539cde71169e3). Sweep 4's lines were kept out of the brief and ruled in the main thread.

1. Decisive step: none stated. Nearest is PR-07 3.2 "For each pile area it is the volume of coal above the yard pad at the survey multiplied by the bulk density the fuel laboratory last determined for that coal before the survey" (standing procedure; does not say how to find the pad or cross the datum change).
2. none (no file ranks or scores the call; bunker file and plan give inputs only).
3. none as an analyst-helper. survey_control_report_2026-07.pdf is a contractor handover report (control points, transformation) and is ordinary.
4. none. Burn plan "Quarter ... 218740" and "Version 3, approved ... 9 December 2026" are inputs, not the answer.
5. PR-07 3.3 "the coal burn of January to March in the first-quarter burn plan ... the plan's quarter total divided by the days of the quarter, in tonnes a day" (fixes 218,740 t / 90 days); 3.2 reserve = per-pile-area volume above the pad times the lab density last determined before the survey, summed; 3.4 "the reserve divided by the planned burn"; section 4 floor 60 days; section 5 nominate by 8 January if under 60. OH-12 1.1/1.2 fix receipts by CV-01 and deliveries by CV-21 weighed tonnes; 2.1 Finnish time, calendar months and quarters.
6. Mostly following stated procedure plus a data-handling chain (datum and grid transformation, pad level, lab density by pile and unit). Deciding text: PR-07 3.2 to 3.4 and survey_control_report_2026-07.pdf section 3 and 4. The filed documents state the rule, so the call leans on rule application and unit/datum reading; I see no analytical-choice stump in the pack itself (a possible judgement on the yard pad level is not stated anywhere I could find). Flag for the author against the three rules.

a. harmless, because it is a standing controlled procedure (rev 4, 2026-03-11, approved before the December survey) and states no December figure or outcome.
b. harmless, because it is the plant's own controlled document with revision history, signatures and no address to an analyst; it refers to the pile area register and lab density tests by their ordinary names.
c. harmless, because it reads as an ordinary approved forward plan (Version 3, 9 Dec 2026, monthly t/d by unit, availability, heat demand sheets).
d. harmless, because .asc headers are standard ESRI grid headers, .xyz is a plain semicolon-delimited, decimal-comma contractor export, survey_deliveries.csv logs flights, checkpoints and RMSE, and pile_areas is a plain register. Note only: lab density units switch from kg/m3 to t/m3 from Aug 2026 and the grid/datum change at July are mess, not hints; nothing is remarked on in the files themselves.
e. harmless, because OH-12 is a plain booking/time/calibration instruction and the control report gives control points and the transform without telling the analyst what to measure (it does state the 0.384 m N60-N2000 offset and rotation, which is ordinary survey handover content).
f. harmless, because they read as plant logs: shift log totalisers at 00:00/08:00/16:00, historian 15-min UTC tag series, unloader START/STOP events with HATCH/SHIFT/WIND/END reasons, all unremarked.

Realism: none that I could see. Minor tell: berth_log tonnes carried to three decimals and a uniform shift-log layout, both plausible.
