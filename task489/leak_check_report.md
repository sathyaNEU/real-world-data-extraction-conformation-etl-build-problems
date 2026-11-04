# leak check, task489

**Verdict: REVIEW.** 18 files read, 130 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: separator, survey, liquid, counters, register, arrival, sentence, makers, arrivals, volume, sheets, harmless, decisive, domain, population, history, allocations, counts, objective, physical, physics, nothing, reader, repair, overuse

## 3 answer figures in the pack (REVIEW 41)
- **REVIEW** `MRS-03_methane_measurement_and_reporting_standard_rev4.pdf`: golden figure 101 appears: ...psia) are converted at 0.02826 m3 per scf (15 C, 101.325 kPa). Methane mass is the gas volume times t...
- **REVIEW** `brannick_DLC-3_TC-5_data_sheet.pdf`: golden figure 0.28 appears: ...dump cycle 0.47 scf n/a Steady bleed nil at rest 0.28 scf/h Supply 20 to 50 psig 20 to 50 psig Sensing...
- **REVIEW** `corrigan_CL-200_CP-10_data_sheet.pdf`: golden figure 0.35 appears: ...ated at 35 psig Bleed to atmosphere, steady state 0.35 scf/h (60 F, 14.696 psia) at 35 psig supply Propo...
- **REVIEW** `corrigan_CL-200_CP-10_data_sheet.pdf`: golden figure 0.62 appears: ...or air; rated at 35 psig Gas used per dump cycle 0.62 scf (60 F, 14.696 psia) at 35 psig supply Output...
- **REVIEW** `deep_basin_equipment_register.xlsx`: golden figure 132201 appears: ...trument SV-40 5 1 in LRL ELMWORTH 12-15 #2 8 93 V-132201 Kakwa 13-22 Wellsite separator, two-phase Vertica...
- **REVIEW** `deep_basin_equipment_register.xlsx`: golden figure 131203 appears: ...Controls CL-200 4 1 in LRL KAKWA 13-12 #2 15 68 V-131203 Kakwa 13-12 Wellsite separator, two-phase Vertica...
- **REVIEW** `deep_basin_equipment_register.xlsx`: golden figure 150802 appears: ...ntrols CL-200 8 2 in LRL ELMWORTH 15-8 #1 16 93 V-150802 Elmworth 15-8 Wellsite separator, two-phase Verti...
- **REVIEW** `deep_basin_equipment_register.xlsx`: golden figure 050303 appears: ...strument SV-40 6 1 in LRL ELMWORTH 5-3 #2 12 68 V-050303 Elmworth 5-3 Wellsite separator, two-phase Vertic...
- **REVIEW** `deep_basin_equipment_register.xlsx`: golden figure 081001 appears: ...ontrols CL-200 6 1 in LRL ELMWORTH 5-3 #3 16 73 V-081001 Kakwa 8-10 Wellsite separator, two-phase Vertical...
- **REVIEW** `deep_basin_equipment_register.xlsx`: golden figure 141601 appears: ...n Controls CL-200 10 2 in LRL KAKWA 3-9 #1 8 94 V-141601 Kakwa 14-16 Wellsite separator, two-phase Vertica...
- **REVIEW** `deep_basin_equipment_register.xlsx`: golden figure 131202 appears: ...nstrument DLC-3 6 1 in LRL KAKWA 13-12 #1 13 73 V-131202 Kakwa 13-12 Wellsite separator, two-phase Vertica...
- **REVIEW** `deep_basin_equipment_register.xlsx`: golden figure 132202 appears: ...nstrument DLC-3 8 2 in LRL KAKWA 13-22 #1 15 97 V-132202 Kakwa 13-22 Wellsite separator, two-phase Vertica...
- **REVIEW** `deep_basin_equipment_register.xlsx`: golden figure 121501 appears: ...Instrument DLC-3 8 1 in LRL KAKWA 8-10 #3 8 67 V-121501 Elmworth 12-15 Wellsite separator, two-phase Vert...
- **REVIEW** `deep_basin_equipment_register.xlsx`: golden figure 101102 appears: ...rument SV-40 8 2 in LRL ELMWORTH 10-11 #1 11 91 V-101102 Elmworth 10-11 Wellsite separator, two-phase Vert...
- **REVIEW** `deep_basin_equipment_register.xlsx`: golden figure 062702 appears: ...trols CL-200 10 2 in LRL KAKWA 6-27 #1 Yes 9 93 V-062702 Kakwa 6-27 Wellsite separator, two-phase Vertical...
- **REVIEW** `deep_basin_equipment_register.xlsx`: golden figure 011402 appears: ...nstrument DLC-3 10 2 in LRL KAKWA 1-14 #1 12 98 V-011402 Kakwa 1-14 Wellsite separator, two-phase Vertical...
- **REVIEW** `deep_basin_equipment_register.xlsx`: and 39 more golden figures
- **REVIEW** `deep_basin_work_orders_2026.csv`: golden figure 131203 appears: ...osed WO-261276,2026-06-16 08:12:00,Kakwa 13-12,LC-131203,Corrective,"Dump valve seat worn, replaced trim k...
- **REVIEW** `deep_basin_work_orders_2026.csv`: golden figure 150802 appears: ...ted WO-260460,2026-01-19 14:28:00,Elmworth 15-8,V-150802,Preventive,"Function test LSHH, well shut in on t...
- **REVIEW** `deep_basin_work_orders_2026.csv`: golden figure 081001 appears: ...osed WO-260800,2026-03-26 08:16:00,Kakwa 8-10,PLC-081001,Corrective,"Arrival sensor cable chafed, re-route...
- **REVIEW** `deep_basin_work_orders_2026.csv`: golden figure 141601 appears: ...losed WO-262146,2026-11-30 12:23:00,Kakwa 14-16,V-141601,Corrective,Painted separator skid and ladder,L. R...
- **REVIEW** `deep_basin_work_orders_2026.csv`: golden figure 131202 appears: ...losed WO-260804,2026-03-27 02:08:00,Kakwa 13-12,V-131202,Corrective,"Replaced sight glass gaskets, weeping...
- **REVIEW** `deep_basin_work_orders_2026.csv`: golden figure 132202 appears: ...sed WO-261377,2026-06-26 07:57:00,Kakwa 13-22,PLC-132202,Corrective,"Arrival sensor cable chafed, re-route...
- **REVIEW** `deep_basin_work_orders_2026.csv`: golden figure 101102 appears: ...d WO-261547,2026-07-22 14:55:00,Elmworth 10-11,LC-101102,Preventive,"Checked LLC operation, snaps clean at...
- **REVIEW** `deep_basin_work_orders_2026.csv`: golden figure 062702 appears: ...Closed WO-260632,2026-03-03 02:09:00,Kakwa 6-27,V-062702,Corrective,Painted separator skid and ladder,B. P...
- **REVIEW** `deep_basin_work_orders_2026.csv`: golden figure 011402 appears: ...Closed WO-260873,2026-04-13 14:20:00,Kakwa 1-14,V-011402,Preventive,"Annual PSV test, popped at 1654 kPa,...
- **REVIEW** `deep_basin_work_orders_2026.csv`: golden figure 062701 appears: ...losed WO-260661,2026-03-05 16:41:00,Kakwa 6-27,LC-062701,Corrective,"Dump valve stem packing weeping, repa...
- **REVIEW** `deep_basin_work_orders_2026.csv`: golden figure 042703 appears: ...d WO-261173,2026-06-03 06:58:00,Elmworth 4-27,PLC-042703,Corrective,"Plunger controller dead on LRL ELMWOR...
- **REVIEW** `deep_basin_work_orders_2026.csv`: golden figure 042701 appears: ...d WO-261311,2026-06-20 08:10:00,Elmworth 4-27,PLC-042701,Corrective,"Installed new plunger controller s/n...
- **REVIEW** `deep_basin_work_orders_2026.csv`: and 28 more golden figures
- **REVIEW** `methane_reduction_plan_2027.docx`: golden figure 0.5 appears: ...se intermittent-vent controllers vented more than 0.5 tonnes of methane in 2026 as reported under MRS-0...
- **REVIEW** `sheldrake_pneumatic_survey_2026.pdf`: golden figure 0.00 appears: ...0.472 2026-05-27 LRL ELMWORTH 15-8 #1 CL-200 60 0 0.00 n/a 2026-05-27 LRL ELMWORTH 6-17 #1 SV-40 60 1 0....
- **REVIEW** `sheldrake_pneumatic_survey_2026.pdf`: golden figure 0.28 appears: ...1.34 0.52 2026-05-26 Elmworth 6-17 TC-1 TC-5 0.30 0.28 2026-05-26 Elmworth 7-2 PC-1 CP-10 1.13 0.35 2026...
- **REVIEW** `sheldrake_pneumatic_survey_2026.pdf`: golden figure 0.35 appears: ...ting (scf/h) 2026-05-25 Kakwa 3-9 PC-1 CP-10 0.32 0.35 2026-05-25 Kakwa 11-22 PC-1 PC-60 0.74 0.52 2026-...
- **REVIEW** `sheldrake_pneumatic_survey_2026.pdf`: golden figure 0.74 appears: ...CP-10 0.32 0.35 2026-05-25 Kakwa 11-22 PC-1 PC-60 0.74 0.52 2026-05-25 Kakwa 16-23 PC-1 CP-10 0.68 0.35...
- **REVIEW** `sheldrake_pneumatic_survey_2026.pdf`: golden figure 0.62 appears: ...C-60 0.82 0.52 2026-05-27 Elmworth 7-18 TC-1 TC-5 0.62 0.28 2026-05-27 Elmworth 14-24 PC-1 CP-10 0.43 0....
- **REVIEW** `sheldrake_pneumatic_survey_2026.pdf`: golden figure 0.32 appears: ...'s rating (scf/h) 2026-05-25 Kakwa 3-9 PC-1 CP-10 0.32 0.35 2026-05-25 Kakwa 11-22 PC-1 PC-60 0.74 0.52...
- **REVIEW** `sheldrake_pneumatic_survey_2026.pdf`: golden figure 0.30 appears: ...C-60 1.34 0.52 2026-05-26 Elmworth 6-17 TC-1 TC-5 0.30 0.28 2026-05-26 Elmworth 7-2 PC-1 CP-10 1.13 0.35...
- **REVIEW** `trellick_PCX-300_plunger_controller_spec.pdf`: golden figure 295 appears: ...C Counters are 32-bit and roll over at 4,294,967,295....
- **REVIEW** `MRS-03_methane_measurement_and_reporting_standard_rev4.pdf`: carries 11 of 12 distinctive words of the committed call: 'Convert the separator level controllers at Elmworth 10-11, Elmworth 7-2, Kakwa 1-14, Kakwa 11-22, Kakwa 14-16, Kakwa 16-'
- **REVIEW** `sheldrake_pneumatic_survey_2026.pdf`: carries 11 of 12 distinctive words of the committed call: 'Convert the separator level controllers at Elmworth 10-11, Elmworth 7-2, Kakwa 1-14, Kakwa 11-22, Kakwa 14-16, Kakwa 16-'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `MRS-03_methane_measurement_and_reporting_standard_rev4.pdf`: 9 of 25 stump-paragraph terms appear (separator, survey, liquid, register, volume, population); read whether the document names the move
- **REVIEW** `sheldrake_pneumatic_survey_2026.pdf`: 3 of 25 stump-paragraph terms appear (separator, survey, volume); read whether the document names the move
- **REVIEW** `trellick_PCX-300_plunger_controller_spec.pdf`: 5 of 25 stump-paragraph terms appear (liquid, counters, register, arrival, arrivals); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 12 describing content (REVIEW 1)
- **REVIEW** `MRS-03_methane_measurement_and_reporting_standard_rev4.pdf`: names 4 column(s) of the data files verbatim (Kakwa, Reporting year, Tank, well): confirm it is the organisation's own record and not a note written for the analyst

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), architecture 1, on a fresh copy of prompt.txt and target/ (target.zip sha256 30d17931bfcf3386ec691df758f0c55d281c228c3ff7d5ef40f0264303780dae). Sweep 4's lines were kept out of the brief and ruled in the main thread (MRS-03 4.2 files dump cycles times rated volume and the counted-cycles rule, never how uncounted cycles are found). Verdict: no leak; question 6 an analytical choice; several realism tells below go to the generator.

# Leak read, task489 (read and quote only; nothing solved)

1. Decisive step: no file announces it. Closest are statements of the method, which are general standard text:
   - MRS-03 rev4 4.2: "An intermittent-vent controller vents its maker's rated supply gas per dump cycle each time it cycles. Its methane is its dump cycles in the reporting year times that volume. Where a pad's SCADA counts a separator's dump cycles, the counted cycles are used."
   - MRS-03 3.3 and 4.4 (mole fraction of the pad's analysis taken in the reporting year; 0.02826 m3/scf; 0.678 kg/m3).
   Nothing says which pads lack counts or how cycles are estimated there. Nothing says the survey is the evidence for a rate of cycling.
2. Ranking/scoring of candidates: none. No file lists pad totals. The plan gives a line only.
3. Files that exist only to help the analyst: MRS-03_annex_B_source_inventory_template.xlsx is the form the prompt names (headers "Pad | Surface location | Source tag | Source class | Make and model | Serial | Activity basis | Activity in the reporting year | Activity unit | Gas vented (m3) | Methane (kg)"), empty, so it shapes output but is not an aid to the call. The MRS-03 standard is the only mildly instructional document (see d). Otherwise none.
4. Figure/name reading as the answer: none. The only candidate is the plan's line, "more than 0.5 tonnes of methane in 2026", which is the stated threshold, not a result.
5. Filed sentence fixing the main figure and population:
   - methane_reduction_plan_2027.docx s.3: "at every pad whose intermittent-vent controllers vented more than 0.5 tonnes of methane in 2026 as reported under MRS-03. Pads at or under that line keep their controllers until the 2028 programme." Fixes: population = pads (all in the register), outcome = the pad's summed intermittent-vent controller methane, window = production days 2026 (MRS-03 3.2), strict > 0.5 t; continuous-bleed excluded (plan s.4, MRS-03 2.3).
   - MRS-03 5.1 "A source in service for part of the year is reported for the part it was in service" (partial-year sources).
   - "so the list of pads is fixed when the order is placed" (15 Feb 2027), i.e. the list is the 2026 reported figure, not a forecast.
   Literal result: the conversion list is every pad whose summed 2026 intermittent-vent methane in tonnes exceeds 0.5. Where a pad has no counted cycles the literal text gives only "dump cycles ... times that volume" with no estimation route, so a literal reader must choose how to get cycles there (the survey table and the SCADA counters are the only cycle evidence).
6. What decides the main answer: an analytical choice (how to estimate 2026 dump cycles for separators with no SCADA count, from the sample evidence and well/vessel characteristics, and the uncertainty of pads close to the line). Supporting parts are data handling (partial-year, stated in 5.1; unit conversion, stated in 4.4; SCADA counter resets or time zone, to be found in the data). Nothing in a file names this: sentence nearest is MRS-03 4.2 "Where a pad's SCADA counts a separator's dump cycles, the counted cycles are used," which implies the uncounted case without saying more. The register's "SCADA dump count" column is Yes/blank per vessel, which is data, not a rule.

## Flagged items
a. Harmless, because the datasheets carry only per-cycle and per-hour rated figures (CL-200 0.62, DLC-3 0.47, SV-40 0.88 scf/cycle; bleeds 0.35, 0.28, 0.52 scf/h) and the Sheldrake survey carries per-test measurements at 12 separators and 12 bleeders; none gives a pad's or maker's 2026 methane, none ranks pads. One mild point: the survey's summary ("Gas per dump cycle was within 4 per cent of each maker's published figure on every controller that cycled during its test", "Seven of the twelve continuous-bleed controllers bled at more than one and a half times their rating") guides the rate choice, but it is a normal contractor finding and the survey's cycle counts per hour are plain test data. The survey also covers only a sample, so it does not hand over pad totals.
b. Harmless, because the register's Vessels sheet is plain equipment data (make, model, span, bore, inlet well, "SCADA dump count" Yes/blank) and work orders are routine notes; the only substantive rows are the device swap, turnaround and heater move notes (Apr 22 PC-60 replacement, Jun 02 to Jun 07 isolation, heater TC-31833 pulled Jun 23 and set Jul 14), which fix in-service dates for partial-year sources in the organisation's own voice and do not name pads for conversion. They bear on the continuous-bleed table asked for and on who is in service, not on the list. No row points at a conversion pad.
c. Harmless, because the plan states only the line (0.5 t, strict, 2026, as reported under MRS-03), the order date and that bleed controllers are excluded. It names no pad and gives no estimating rule.
d. Harmless, because it reads as the company's own controlled standard (owner and approver table, effective date, supersedes line, revision history Rev 1 to 4 with names and dates, "Controlled copy when viewed in the document system" footer). It states a method (4.2, 4.3) as a standard would and repeats register and plan values only as definitions (241 kPa is in the register; 0.678 kg/m3 and 0.02826 are standard constants). It does not describe the data files by file name or quirk. Mild caution: 4.2's sentence "Where a pad's SCADA counts a separator's dump cycles, the counted cycles are used" is the one place that points at the SCADA/no-SCADA split, but it is natural standard text.

## Realism
Weak tells, no hard fail:
- methane_reduction_plan_2027.docx: docProps/app.xml is the python-docx default (Words 0, Characters 0, Lines 0, Template Normal.dotm, default thumbnail.jpeg, revision 0); a one-page "executive endorsed" plan with no header/footer, no page numbers, no revision block or sign-off.
- plunger_cycles_2026.csv: afterflow_min is uniform 0 to 44 (mean 22.8, quartiles 12/23/34) and travel_s uniform 240 to 1499 (quartiles 554/869/1184); received_local minutes and hours are flat. A real controller log is skewed, not flat. Only 29 controllers over 25 wells with exactly 25.8 MB of rows.
- deep_basin_work_orders_2026.csv: filler descriptions are assigned to tags they do not fit (e.g. "Calibrated sales meter, no change" on LC-141601 and V-093401; "Replaced battery in plunger controller" on LC-061701; "Painted separator skid" on LC-103201) and created times are spread flat across the clock (e.g. 22:07, 03:51 on corrective jobs); 132 of 136 are "Closed", 4 "Completed", one wording each.
- The three equipment sheets (corrigan, brannick, aldous) share the same two-table layout, wording ("Specifications subject to change without notice", "bench values"/"new relays") and 1-page length, with fixed 2-in/1-in dump valve capacity rows; they differ in revision styles and Corrigan's Producer is Adobe, but they look like one hand. All except Corrigan and Sheldrake/MRS use Word as the PDF producer, with named authors; Sheldrake and MRS-03 have letterhead lines and page numbers, the maker sheets do too.
- scada_dump_counters_2026.csv: five tags only, strictly hourly on the hour, no gaps or nulls (0 missing), so quite uniform for a SCADA export.
- ogi_leak_survey_2026.csv and gas_analyses_2025_2026.csv: single operator (J. Davis, 94 of 94 rows) and single lab and sample point for all 52 samples; plausible but uniform.

### Second read, on the main-call repair cut

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), on a fresh copy of prompt.txt and target/ (target.zip sha256 79851d408dc8e2800be242dbeeef6fb8e1932dd61b26d6f856c4627758c88bfb), after the makers' data sheets, the PCX-300 specification and the plan changed. Sweep 4's lines were kept out of the brief and ruled in the main thread (the PCX-300 Operation paragraph is a maker's description of plunger lift and names no separator, level, dump or band). Verdict: no leak. Question 6 reads the main call as stated rules plus one open piece (dump cycles where nothing counts them), which is the decisive analytical step.

# Leak read, task489 r2 (read and quote only; nothing solved)

1. Decisive step. Nothing announces it. Closest: methane_reduction_plan_2027.docx s.3, "at every pad whose intermittent-vent controllers vented more than 0.5 tonnes of methane in 2026 as reported under MRS-03", and MRS-03 s.4.2, "Where a pad's SCADA counts a separator's dump cycles, the counted cycles are used." The second states the principle for pads with a counter; it says nothing about how to estimate pads without one. Equipment register Vessels sheet column "SCADA dump count" (Yes/blank) shows which pads are counted but is a plain register field. No sentence names the plunger-lift non-arrival link.

2. Ranking/scoring file: none. Sheldrake survey, data sheets, SCADA, plunger cycles are inputs, none ranks pads.

3. File existing only to help the analyst: MRS-03_annex_B_source_inventory_template.xlsx is the output shell (empty headers), cited by the prompt. It is a template, not a hint. No other.

4. Figure/name reading as the answer: none. The 0.5 t line is context in the plan. The survey "Per cycle" values and "Summary" (3.03 scf/h average, "within 4 per cent of each maker's published figure", "Seven of the twelve ... more than one and a half times their rating") are context; the last two are slightly interpretive but about the survey's own sample, not any pad's 2026 total.

5. Literal-fixing sentences:
- MRS-03 s.4.2: "An intermittent-vent controller vents its maker's rated supply gas per dump cycle each time it cycles. Its methane is its dump cycles in the reporting year times that volume. Where a pad's SCADA counts a separator's dump cycles, the counted cycles are used." Fixes unit = controller, per-cycle volume = maker rating (scf at 60F/14.696), counted cycles where SCADA counts.
- s.4.4: 0.02826 m3/scf, methane = volume x mole fraction x 0.678 kg/m3; s.3.3 mole fraction of the pad's lab analysis taken in the reporting year; s.3.2 production day 08:00 local to 08:00, 1 Jan to 31 Dec; s.5.1 part-year in service reported for the part in service; s.5.2 kg per source, t per pad.
- Plan s.3: pads with intermittent-vent methane strictly > 0.5 t in 2026 convert; "at or under that line keep their controllers"; list fixed at order date. Prompt: per-controller kg to nearest kg, per pad t to 2 decimals.
Result: population = intermittent-vent (separator level) controllers only, 2026 production-day window, kg per controller summed to pad, compared to 0.5 t. It does not say how cycles are obtained where no counter exists.

6. What decides the main answer: mostly following a stated rule (MRS-03 s.4 applied to counted cycles, the plan's 0.5 t line). The part that is not stated anywhere is how to get dump cycles for uncounted separators; the files leave this open and the data (plunger cycles with non-arrival results, the prompt's "plunger lift well's 2026 cycles that ended without the plunger arriving") supply it. Decided by an analytical estimation choice for uncounted pads, but a reader following s.4.2 literally and cleaning the data gets partway on rules. I flag that the rule-application share is large: the MRS-03 text plus the prompt's own mention of non-arrival cycles carries much of it. Deciding sentence: MRS-03 s.4.2 last sentence. No planted defect/decoy sentence seen.

Sweep items
a. Harmless, because the Sheldrake report is a third-party sample survey (12 level controllers, 12 bleeds, one hour each in late May) with no pad 2026 totals, no ranking; the per-cycle figures only echo maker ratings; the bleed table is continuous-bleed, which the plan excludes. Data sheets give only per-trip/bleed ratings, no pad figures.
b. Harmless, because register rows are tags, makes, serials, SCADA yes/blank and settings; work orders are routine jobs (gaskets, packing, painting, controller swaps, turnaround/decommission supply isolations). One watch point: the Vessels "SCADA dump count" Yes/blank flag and the Plunger column in Wells tell the analyst which pads are counted or lift wells, but that is ordinary register data, not a pad list. No row says which pads convert.
c. Harmless, because the plan states only the 0.5 t line, scope (separator level controllers), the order date and that continuous-bleed is out; no pad list, no estimation method for uncounted cycles.
d. Harmless/realistic, because it reads as the company's own controlled standard (owner/approver block, supersedes, revision history, controlled-copy footer). Values (0.02826, 0.678, mole fraction year, 08:00 day) are its own rules. Minor: s.4.2 states the uncounted case only by omission, and the Annex B template sheet names mirror the prompt; no analyst-facing note.
e. Harmless, because it is a maker's spec: PCX-300 counters (cycle count, arrival count, travel time, non-arrival logged) and nothing on separators, level controllers or dump counting.

Realism: none that is strong. Minor tells: all PDFs/docx carry plausible different authors, creators (Word 2016/2019/365, Adobe PDF Library for Corrigan), dates and release years, distinct letterhead/doc numbers/footers, so the three makers read as different companies (Corrigan uses tables with ordering codes, Brannick prose, Aldous Issue 7). The docx has header/footer, revision block, three-person sign-off, template "Larchmere Report.dotx", company metadata, revision 9, TotalTime 212. Small oddities: the docx core.xml created 2026-11-30 but "Issued 12 January 2027" while file mtimes are Jan 2027 (consistent); MRS-03 PDF creation 2025-12-04 matches approval. Work-order notes for controller swaps (WO-2606xx/2607xx numbers, "Pulled controller s/n ... had it running here at 10:05") use a distinct template wording and lower WO number range than routine jobs, which reads templated; routine jobs repeat a small set of phrases ("Painted separator skid", "LLC pilot cleaned, stroked through span"), a little uniform. Sheldrake survey table has one row per tag with unusually neat round-ish values. Otherwise none.
