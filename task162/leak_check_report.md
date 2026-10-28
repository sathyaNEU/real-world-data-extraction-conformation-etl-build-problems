# leak check, task162

**Verdict: REVIEW.** 16 files read, 20 golden figures and 10 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: setting, method, factor, export, release, contract, restart, architecture, night-day, schedule, record, decisive, pressures, carried, window, outlet, settings, replayed, loggers, tuesday, target, reading, scheme, benefit, sentence

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `LW-LA-04_DMA_leakage_assessment_method.pdf`: candidate 'Cragthwaite Top' sits beside decision vocabulary: ...Road 1.18 NZ23 Thornsike Bridge 1.39 NZ07 Sorrelby End 0.91 NZ24 Brockmere Lane 1.58 NZ08 Cragthwaite Top 1.58 NZ25 Hagg Wood 1.22 LW-LA-04 issue 6 | Uncontrolled when printed Page 2 District...
- **REVIEW** `LW-LA-04_DMA_leakage_assessment_method.pdf`: candidate 'Kestle Road' sits beside decision vocabulary: ...enfold 1.02 NZ21 Chapelrigg 1.09 NZ05 Stainmoor Ings 0.92 NZ22 Netherskell Rise 1.09 NZ06 Kestle Road 1.18 NZ23 Thornsike Bridge 1.39 NZ07 Sorrelby End 0.91 NZ24 Brockmere Lane 1.58 NZ08 Crag...
- **REVIEW** `LW-LA-04_DMA_leakage_assessment_method.pdf`: candidate 'Sorrelby End' sits beside decision vocabulary: ...ngs 0.92 NZ22 Netherskell Rise 1.09 NZ06 Kestle Road 1.18 NZ23 Thornsike Bridge 1.39 NZ07 Sorrelby End 0.91 NZ24 Brockmere Lane 1.58 NZ08 Cragthwaite Top 1.58 NZ25 Hagg Wood 1.22 LW-LA-04 iss...

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `LW-LA-04_DMA_leakage_assessment_method.pdf`: 9 of 25 stump-paragraph terms appear (method, factor, contract, night-day, record, carried); read whether the document names the move
- **REVIEW** `TH-OUT-0417_calibration_certificate.pdf`: 3 of 25 stump-paragraph terms appear (method, outlet, reading); read whether the document names the move
- **REVIEW** `outcome_contract_schedule_4_phase3.pdf`: 5 of 25 stump-paragraph terms appear (method, export, contract, schedule, target); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: "Will the 22 fixed-outlet pressure reducing valves Coldbeck commissions in Lynmere Water's Northern zone by March 2027 cut the Phase 3 districts' leakage by the contracted 0.48 Ml/d in the 2027-28 assessment, and if not, "

## 6 ranking artifacts (REVIEW 1, INFO 1)
- **REVIEW** `LW-LA-04_DMA_leakage_assessment_method.pdf`: names 10 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `district_register.csv`: names 10 of 10 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

One isolated reader (Sonnet, medium) on a fresh copy of prompt.txt and target/ (target.zip 828ecbc5, the stage 3
pack), never the design note, generator, submission or report. The stump-vocabulary sweep's REVIEW lines were ruled in
the main thread and not handed over; the answer-figure sweep's lines went over with their numbers removed. Its answers,
in short:

1. Decisive step: none stated. Closest context: the planning note ("take each Phase 3 district's demand and pressures in
   each month of 2027-28 as they were recorded in the same month of 2025-26 ... with no growth. The valves are in
   service for the whole of 2027-28 at the settings in Annette's Phase 3 schedule (rev C).") and LW-LA-04 section 7 (N1
   "applies to the night-day factor and to any change in a district's leakage with its pressure"), a method standard
   that does not say how to apply it.
2. No file ranks the districts or states a 2027-28 leakage figure; the export's Year sheet is the 2025-26 baseline and
   the valve schedule's "AZNP after commissioning (m)" is a pressure, not a leakage figure.
3. No manifest or data dictionary; the registers and the code history are reference tables, LW-LA-04 and Schedule 4
   governing documents.
4. Nothing reads as the answer; the AZNP after commissioning column is the nearest thing to a handed-over intermediate.
5. Literal sentences: Schedule 4.2 (the 22 districts, annual-figure sums, the export as baseline, 2025-26 less
   2027-28), 4.4 (the shortfall over 0.05, rounded up), the planning note (each month as recorded, valves all year at rev
   C, no growth), LW-LA-04 sections 2 to 7 (GMT, the 03:00 mean, 1.7 l/h a dwelling and 8.0 a non-household connected
   that day, valid days, the factor with N1, month mean then year mean, groups summed), the valve schedule (settings
   metres head at the outlet, where the inlet logger reads).
6. An analytical choice: how the outlet settings translate into the zone pressures and then into leakage through each
   district's N1 is not executed by any filed text; GMT, the bar factor, valid days, the dwelling allowance and the code
   history are rule application around it.
7. Realism: the export's household and non-household means constant across all twelve months for each district; the
   monthly minimum night flow nearly flat with isolated bumps; the valve schedule's commissioning weeks two districts a
   week in code order; the AZP point codes sequential with a random suffix (not obviously wrong).
8. Supporting outputs: the twelve districts' figures read as closed (NZ04's two inlets by section 2, the closed-day rule
   by section 5, the dwelling allowance by the extract's dates, units by the 10.197 factor); system input could take
   the certificate's error by dividing by 0.986 or multiplying by 1.014, or from the test-point errors (-1.42, -1.39,
   -1.41 per cent); billed unmetered rests on the billing basis column read consistently.
a to c. Table C2 (district names beside N1), its listing of every district, and district_register.csv: harmless,
   parameter and reference tables that rank nothing on the question.

Main thread's ruling, one line each:
- 1 to 6: no decisive-step sentence, no ranking file, no helper file, nothing read as the answer; question 6 classes the
  deciding step as an analytical choice, which matches the design (Gate H from outside).
- The AZNP after commissioning column: the valve schedule's true night figure, the default path's input; kept (asserted
  in checks.py R3c as the pack's own replay at 03:00), it states no leakage and no benefit.
- 7, household counts flat: fixed in the generator, Phase 3 now carries single infill houses and demolitions (every
  count reads them alike, SF5 and A9 asserted).
- 7, night flows flat: fixed, background leakage rises through the winter and bursts are smaller and more frequent.
- 7, commissioning weeks in code order: fixed, the crews' route, one to three valves a week, the half-term week empty.
- 7, AZP point codes: harmless, the register's own point numbering.
- 8, the certificate: dividing and multiplying already print every balance figure alike (B2 asserted); the test points
  now read -1.41, -1.40 and -1.39 per cent, each inside the same corridor.
- a to c: harmless, as the reader ruled.
- The fixes changed no sentence under target/ (data, table values and commissioning dates only) and not the prompt's
  question; leak.py re-run on the rebuilt pack (target.zip a8146587): REVIEW, the same three sweeps, no LEAK.
