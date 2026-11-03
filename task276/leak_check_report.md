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
