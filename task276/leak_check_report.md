# leak check, task276

**Verdict: REVIEW.** 20 files read, 19 golden figures and 3 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: driver, bulkhead, posture, wrenfold, travel, stated, backrest, standard, population, measured, package, committee, pennick, forward, fewest, vision, predicted, cannot, specifies, coachbuild, failing, factors, descriptive, distribution, vennerley

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `policy/driver_posture_model_ellisand_2025.pdf`: \bthe model\b x6: ...vice's own drivers rather than against published percentile manikins. The model was fitted to the seat trial run in May and June 2025 in the service'...

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `fleet/package_drawing_data_pennick.pdf`: carries 4 of 7 distinctive words of the committed call: 'We should specify Pennick Coachbuild on FD35 for the 2027 front-line ambulance order.'
- **REVIEW** `policy/cab_fit_standard_issue2.docx`: carries 7 of 7 distinctive words of the committed call: 'We should specify Pennick Coachbuild on FD35 for the 2027 front-line ambulance order.'
- **REVIEW** `policy/driver_posture_model_ellisand_2025.pdf`: carries 5 of 7 distinctive words of the committed call: 'We should specify Pennick Coachbuild on FD35 for the 2027 front-line ambulance order.'

## 4 design-note vocabulary (REVIEW 7)
- **REVIEW** `fleet/package_drawing_data_ostrel.pdf`: 6 of 25 stump-paragraph terms appear (driver, bulkhead, travel, standard, measured, package); read whether the document names the move
- **REVIEW** `fleet/package_drawing_data_pennick.pdf`: 7 of 25 stump-paragraph terms appear (driver, bulkhead, travel, measured, package, pennick); read whether the document names the move
- **REVIEW** `fleet/package_drawing_data_wrenfold.pdf`: 6 of 25 stump-paragraph terms appear (driver, bulkhead, wrenfold, travel, stated, package); read whether the document names the move
- **REVIEW** `fleet/seat_dimension_sheet_brevin_as7.pdf`: 4 of 25 stump-paragraph terms appear (driver, stated, backrest, standard); read whether the document names the move
- **REVIEW** `policy/cab_fit_standard_issue2.docx`: 13 of 25 stump-paragraph terms appear (driver, posture, wrenfold, standard, measured, package); read whether the document names the move
- **REVIEW** `policy/driver_posture_model_ellisand_2025.pdf`: 6 of 25 stump-paragraph terms appear (driver, posture, measured, pennick, forward, factors); read whether the document names the move
- **REVIEW** `policy/fleet_performance_reporting_standard_issue4.pdf`: 6 of 25 stump-paragraph terms appear (driver, bulkhead, standard, measured, committee, vennerley); read whether the document names the move

## 6 ranking artifacts (INFO 2)
- **INFO** `policy/cab_fit_standard_issue2.docx`: names 3 of 3 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `procurement/tender_prices_2027_shortlist.xlsx`: names 3 of 3 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 12 describing content (REVIEW 1)
- **REVIEW** `policy/cab_fit_standard_issue2.docx`: names 7 column(s) of the data files verbatim (Chassis, Converter, FD35, Ostrel Vehicle Conversions, Pennick Coachbuild, RD43): confirm it is the organisation's own record and not a note written for the analyst

## 1 file names (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

1. Decisive step: no sentence announces it. The nearest is cab_fit_standard_issue2.docx s.3, "A driver fits a cab when they can be seated in the driving posture the service's driver posture model (Ellisand Human Factors, report EHF-2507) predicts for them in that cab, with their eye point in that posture inside the vision zone". It points at the model and the zone but does not say any alternative route is wrong. s.7 "The Committee will specify the shortlisted cab that the fewest drivers fail" is the decision rule. Neither is a leak.
2. No file ranks or scores the cabs on the prompt's question. tender_prices gives prices and lead times only. The package PDFs give geometry only. The workshop jobs and odometer files are raw records.
3. Files that exist only to help the analyst: none stands out. adult_body_dimensions_reference_tables.pdf (population percentiles) and tender_prices are plausible distractors, since both are relevant but unused. workshop_code_map.xlsx and vennerley_staff_number_crosswalk.xlsx are ordinary system-migration artefacts.
4. No figure or name reads as the answer. No shipped number is a count of failing drivers, a cab ranking or a recommended cab.
5. Sentences that fix the computation:
   - Standard s.4, "The sight line from the eye point to the lower edge of the windscreen header's clear area rises at least 11 degrees above horizontal, and the sight line ... to the lowest road sight point falls at least 5 degrees below horizontal." Run literally, this tests each driver's predicted eye point against two angle thresholds using the converter's package points.
   - Standard s.5, "the latest measurement stands" plus the conversion of imperial paper-form entries. This fixes the population and the per-driver inputs.
   - Standard s.2, the roster published on 1 October 2026. This fixes the population.
   - EHF-2507 s.2 formulas. Run literally, they give each driver's predicted hip point, torso angle and eye point for a given cab's seat height.
   - Gap to note: s.3 says "can be seated in the driving posture the model predicts", but no sentence says outright that the predicted hip point must fall inside the seat's travel limits (which the package sheets give). A literal reader may read "seated" as that travel check or may ignore it. The design note's fork table should close this. The torso angle against the seat's recline range (Brevin sheet, 8 to 34 degrees) is the same kind of gap. The model's stated fitted range (stature 1,480 to 2,010 mm, BMI 18 to 47) is likewise silent on out-of-range drivers.
6. What decides the main answer: mostly following the filed standard and model (rule application: apply the model, then the zone and travel tests) plus reading data correctly (the Wrenfold package is in SgRP-relative signed coordinates, not heel-point coordinates; the paper-form imperial entries; latest measurement per driver; Vennerley to service staff numbers through the crosswalk). The analytical element is only the choice of per-driver prediction against the reference percentile tables. That choice is closed by the standard naming the model, so a careful solver is not tempted off it. The stump is therefore weak on the client's rule 3: it reads as rule application and data semantics. No sentence announces a planted trap.
   - The ask side (converter jobs per 100,000 miles, chassis days off the road) is a pure reconstruction across systems: Vennerley codes to B12/B30, former fleet numbers, telematics fit and removal dates, disposals, quarters.
7. Realism:
   - vehicle_disposals_2025_26.xlsx: created 2025-05-02, last edited by Brenda Ward, yet its rows run to Oct 2025 and beyond. The dates are inconsistent. Also, the creator is "Fleet Services" and the editor is the Head of Fleet.
   - Liam Jackson is the last editor of the fleet register, workshop code map, HR staff crosswalk and Occupational Health measurements. One person editing HR and OH workbooks looks implausible. The crosswalk (HR) and measurements (OH) should have department-appropriate editors.
   - cab_fit_standard_issue2.docx: created 2026-06-12, modified 2026-07-09, but issue 1 is dated 14 March 2025 and the docx has 7 revisions at 214 minutes. Acceptable, but the creation date postdates issue 1; a fresh file for issue 2 is plausible.
   - EHF-2507 is dated 21 July 2025 and says the model is suitable for the 2027 order. The shortlist and tender came in 2026. Mildly anticipatory but plausible.
   - Package PDFs from converters have Creator "Microsoft Excel" with a Word-style layout, and all PDFs share the same "Microsoft Word for Microsoft 365" look and typography. This is a uniform generator signature, minor.
   - Wrenfold has a tiny orphaned footnote on page 2 (layout artefact).
   - Tone is otherwise plausible; no LLM tell-tale prose.

Flagged files:
- policy/driver_posture_model_ellisand_2025.pdf, author-like vocabulary: harmless. It is a consultant's model report with formulas and a validation table, which is the kind of document a service would hold. "The model is suitable for assessing cabs offered for the 2027 order" is a method endorsement, not a candidate recommendation.
- package_drawing_data_pennick.pdf: harmless. Pure geometry; it recommends nothing.
- cab_fit_standard_issue2.docx, decision vocabulary overlap: harmless in itself. It is the organisation's decision rule and shortlist, and it names no winner.
- driver_posture_model_ellisand_2025.pdf, decision vocabulary overlap: harmless. It recommends no candidate cab.
- cab_fit_standard_issue2.docx, names data columns verbatim (stature, sitting eye height, weight): the organisation's own governing record (owner Head of Fleet, issue control table, committee approval), not an analyst note. It does fix the method literally, which is the intended determinism filing, and it states no result. Harmless.

## Solver's-eye read (re-read after the reporting standard clause)

Read: prompt.txt and all 20 files under target/ (PDF text, docx XML, xlsx sheets and properties, csv heads). No figures, ranking or answer are produced here.

1. Decisive step. No sentence announces it. The nearest is the cab fit standard (policy/cab_fit_standard_issue2.docx) section 3: "A driver fits a cab when they can be seated in the driving posture the service's driver posture model ... predicts for them in that cab, with their eye point in that posture inside the vision zone in section 4." plus section 7 "The Committee will specify the shortlisted cab that the fewest drivers fail." These state the criterion and the decision rule, not the pitfall. Nothing says what an easy route gets wrong.

2. Ranking or scoring of candidates on the prompt's question. None. No file counts or lists drivers failing a cab. The tender prices workbook lists price, lead time and warranty only (no fit or defect ranking). The Ellisand model PDF validates the model on current cabs only. The defect and off-road data are raw job-level rows, not rolled up by converter or chassis.

3. Files that exist only to help the analyst. None clearly. The adult body dimensions reference tables (percentile manikin values, with the sentence "Values for occupational groups differ from these population values and should be measured") and the Brevin seat dimension sheet (inches) read as context or distractor material. The workshop_code_map and staff-number crosswalk are ordinary system-migration artefacts. The reporting standard is a definitions file (see item 5 and the focused section below).

4. Figures or names reading as the answer. None. The package drawing PDFs carry only dimensions; the prompt names no cab. The Wrenfold sheet gives SgRP-relative coordinates (a conformation task, plausible as vendor practice). No sentence or label highlights a preferred cab.

5. Sentences that fix how the main figure is computed or over which population (literal execution, in words):
- Standard s.2: "Every member of staff on the front-line driving roster to be published on 1 October 2026." Population is the whole 1 Oct 2026 roster, including drivers who have not been measured in the way a naive join would require; literal execution counts each roster member against each cab.
- s.3 and s.4: fit = posture predicted by the Ellisand model in that cab, eye point inside the two sight-line angle limits to the windscreen header and to the lowest road sight point. Literal execution: for each driver and cab, compute predicted hip point, torso angle and eye point from the model, then test the two angles with the converter's package points; fails when either test fails (and the posture is outside the cab's seat travel or recline, if the executor reads "can be seated" that way; this is the one place wording leaves a slightly open reading of "can be seated" versus the stated vision-zone test).
- s.5: latest measurement stands; paper-form imperial values converted. Literal execution: one measurement per driver (via the crosswalk for former Vennerley numbers), converted.
- Reporting standard (for the asks): vehicle in front-line fleet from entry date to disposal date, disposal not counted; vehicle-year = 365 days in fleet; miles from the odometer entered at fitting, unit fitted from fitted date to removed date, removed not counted; off the road from declared date to return date, return not counted; seat and cab-structure jobs = codes B12 and B30; job counted in the quarter first raised. Each is a filed definition whose literal execution gives the figure.

6. What decides the main answer. Mostly an analytical choice plus method execution: the posture model is filed and the standard says how fit is judged, so the steps are largely stated-rule execution (model, angle limits, latest measurement, unit conversion, crosswalk). The analytical part is the roster-versus-measurement population and what the model's validation table (current cabs only, spread of the hip-point prediction about 17 to 19 mm s.d., torso 2 s.d.) implies, but nothing in the pack tells the analyst to use or reject that spread. A reviewer should judge whether the main call's decisive step is really analytical or is rule application here: on a literal reading, a careful solver who follows s.3 to s.5 reaches the golden without any judgement. The decisive material is the standard s.3 plus s.4 and the model equations in the Ellisand PDF s.2; no planted decoy is visible (the reference tables are a population-percentile decoy, but are not official or presented as the method; Brevin sheet in inches is a unit semantic, not the stump).

7. Realism. Mostly consistent and plausible. Observations:
- Author and date metadata are varied and sensible (Fleet Services, Liam Jackson, Gareth Davis, Christine Rees, Linda Cooper, Procurement, vwfleet); the docx creator is Brenda Ward, revision 7, created 2026-06-12, modified 2026-07-09, consistent with issue 2 approved 8 July 2026.
- cab_fit_measurements workbook property creation date 2025-03-03 holds records to Sept 2026 (a rolling file; fine). Disposals workbook created 2026-04-02 contains disposals dated Oct 2025 (fine).
- The telematics unit changes workbook has many rows with blank odometer-at-fitting (probably intended for original units; reads as natural).
- The Ellisand report is dated 21 July 2025 and says the model is "suitable for assessing cabs offered for the 2027 order", and the report reads clean and slightly promotional of its own suitability; mild but not out of tone for a consultant report.
- Standard issue 2 says the points "taken from the package data" in the document control table, which is natural.
- Package PDFs differ in convention (Ostrel/Pennick from heel point, Wrenfold from SgRP) and reference "issue 1.1 / B / 2": plausible vendor variation. Round numbers in the Wrenfold and Pennick sheets look slightly tidy but not machine-made.
- No toolchain signatures seen in the files read. No file name names the trap. prompt.txt is a single paragraph under 1,000 characters, question first.

### Focus: policy/fleet_performance_reporting_standard_issue4.pdf

Does any sentence read as written for an analyst or as pointing at a trick? Read in full, it does not. It is a one-page definitions table: a header ("These definitions apply to every fleet figure reported to the Fleet and Estates Committee and to the Board. Figures are reported by financial year (1 April to 31 March) and by financial quarter."), nine term rows, and a "Systems" note. The date convention, "up to the date ... that date not counted", is repeated in the same form for front-line fleet, miles run and off the road, which is how an organisation's own standard would be written and is uniform rather than singled out. The phrase "whatever their conversion or chassis" and "a job counts in the quarter in which it was first raised" are definitional. The "Systems" paragraph ("The Vennerley workshop system closed on 30 June 2025. From 1 July 2025 every vehicle's jobs are raised in the fleet management system, and the former Vennerley vehicles carry service fleet numbers from that date.") states a fact about the migration; it is the one sentence that reads close to explaining the data to an analyst (it effectively tells the solver that the Vennerley jobs and fleet numbers need joining via the former-fleet-number column), but it is phrased as an organisational note about systems, and it does not say how to join or where a trap sits. Verdict: light flag only on the Systems paragraph as the single sentence nearest to data explanation; it is plausible as the organisation's own reporting rule and does not announce the stump. The standard does not touch the cab-fit main call at all; it feeds only the asks, where its filed definitions make execution literal (rule application is permitted for asks).
