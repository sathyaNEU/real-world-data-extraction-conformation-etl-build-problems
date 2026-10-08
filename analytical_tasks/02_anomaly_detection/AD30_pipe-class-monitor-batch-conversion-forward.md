# AD30 — Which pipe gets its own rare-incident chart for 2027, when the miles converted to batch service last year have not failed yet

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Supply Chain & Logistics · pipeline integrity oversight |
| Mirrors | Monitoring rare failures by the population that will carry the hazard in the monitoring year rather than the one that carried it last year (drive-failure monitoring after a fleet moves to write-heavy workloads at cloud providers, component reliability after airlines move aircraft onto short-haul cycling, battery incidents after device makers change charging profiles) |
| Decision shape | A structure the body adopts: the partition of the state's pipe into separately monitored classes for 2027, and which class's chart is signalling, scored on the commission's rule that no chart may pool pipe whose incident rates in the monitoring year differ by more than 1.5× |
| Committed call | The monitored classes and the signalling class, with the miles an inspection order would cover, filed with the commission on 1 December as the 2027 monitoring structure |
| Gap · Pattern | Gap 1 (time: the monitoring year's rates, not the record's) over Gap 2 (population: which pipe shares the hazard) · change-log natural experiments that measure what a conversion to batch service does to seam failures, applied forward to the miles converted in 2025, with a saturated tie broken by the record's open gaps below it |
| Gate G mechanism | forecasting, with decomposition_attribution support |
| Measured traps engaged | #25 assumes an effect the log could measure · #19 breaks a big tie instead of questioning it · #13 validates on one population, applies to another |
| Calibration form | Change-log natural experiments: nine pipeline segments that changed operator in 2015–2024 and six lines converted to batch service in 2016–2022, each with its incident record before and after |
| Driving force | Seam failures on low-frequency ERW pipe follow how the line is run. Batch service swings the pressure every day, and the change log's six past conversions measure what that does: on the four LF-ERW lines the seam-failure rate rose 3.9 to 4.6 times within two years, while on the two seamless lines it held. In March 2025 operator Y converted 120 miles of LF-ERW to batch service for a new terminal, and those miles have failed once since, so on their own record they sit with quiet pipe. The commission's rule asks about rates in the monitoring year, and at the measured multiple the converted miles will run at the rate of LF-ERW that has always cycled. The signalling class is 370 miles, not the 430 miles of all LF-ERW and not the 250 that the record alone shows. |

## 1. Situation

The state pipeline commission's integrity office monitors 6,200 miles of hazardous-liquid pipe run by ten operators. Incidents are rare
(38 since 2021), so it watches time between incidents, normalised by mileage, on control charts. For 2027 it must file the monitoring
structure: which populations get their own chart, and which chart, if any, is signalling at the 30 June 2026 review, since a signalling
population gets an inspection order. The commission's rule says no chart may pool pipe whose incident rates in the monitoring year differ
by more than 1.5×. The office holds the incident reports (each failed segment's line, seam type and install decade), the operators' line
inventory, the service register (each line's operating mode and conversion dates, filed for tariffs) and the integrity change log of
transfers and conversions. Operations believes operator X slipped after its reorganisation.

## 2. Gate G: why this is legal

* **Litmus.** Every reported figure is correct: incident dates, the line inventory, the service register and the change log. Operations is
  right that X had a run of short gaps. Nothing reported is overturned; the difficulty is a population whose rate in the monitoring year is
  not the rate in its record.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the operations view and the office's old operator charts. A class build by era and seam type still splits off
  all 430 miles of LF-ERW, and a build on each line's own record still leaves the converted miles with quiet pipe.
* **Instrument repair.** No file is suspect. The incident reports carry every failed segment's line, seam and decade; the inventory, the
  service register and the change log are complete. A perfect record of 2021–2026 still shows the 120 converted miles at one failure in 660
  mile-years, because their batch-service rate lies in 2027, so rung 0 still names X, rung 1 Y and rung 2 the 430-mile seam split, and
  only the measured conversion multiple places the converted miles.
* **Lens swap.** The naive structure watches operators, or all LF-ERW; the answer watches the pipe that will cycle in 2027, a different set
  of miles that includes 120 whose own record is quiet.

## 3. The driving force

A strong solver moves from annual counts to time between incidents, breaks the saturated tie with open gaps, reads the transfer log as
natural experiments that show rates follow the pipe, and builds class charts by era and seam type: LF-ERW (430 miles) fails at 4.6 per
thousand mile-years against 1.7 for other pre-1970 pipe, so it gets its own chart, which signals. Every step is correct, and every step
reads rates off 2021–2026. Ten of LF-ERW's eleven failures sit on the 250 miles that have run in batch service for a decade, where pressure
cycles daily. The service register shows operator Y converted another 120 miles of LF-ERW to batch service in March 2025, and the change log
holds six earlier conversions with before-and-after records: on the four LF-ERW lines the seam-failure rate rose 3.9 to 4.6 times within two
years; on the two seamless lines it held within 10%. Splitting LF-ERW by each line's own record puts the converted miles with quiet pipe. The
commission's rule asks about 2027, and at the measured multiple those miles join the batch class: LF-ERW in batch service (370 miles), other
pre-1970 pipe with the 60 steady LF-ERW miles (1,470), and post-1970 pipe, with only the first chart signalling.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Per-operator time-between-incident charts; six operators tie at 100% of 2025–26 gaps below their lower limit, broken by the monitor's documented tie-break (largest mileage) | Per-operator structure, operator X on enhanced inspection | The office's standing monitor and its written tie-break | The incident file to the review date: X's open gap since March 2025 is above its lower limit, so X's share is 67% |
| 1 | Saturation broken by the standard's rule (the lowest share consistent with every file of record, counting each open gap to 30 June) | Per-operator structure, operator Y | The standard applied exactly; only Y stays at 100% | The transfer log: in all nine transfers the segment kept its rate within 12% while the acquirers' own rates differ up to 3× |
| 2 | Class charts by era and seam type on each class's 2021–2026 record | Three classes (LF-ERW, other pre-1970, post-1970); the LF-ERW chart signals; order on all 430 LF-ERW miles | Rates follow the pipe, the split clears the 1.5× rule at 2.8×, and the transfers confirm it | The change log's conversions: on all four LF-ERW lines converted to batch service the seam-failure rate rose 3.9 to 4.6 times within two years, and the service register shows 120 LF-ERW miles converted in March 2025 |
| 3 | **Decisive:** classes on each line's rate for the monitoring year: batch LF-ERW at its record, the 2025 conversions at their steady-service rate times the measured multiple, steady LF-ERW at its own | **Three classes (LF-ERW in batch service, 370 mi; other pre-1970 with steady LF-ERW, 1,470 mi; post-1970); only the batch LF-ERW chart signals; order on 370 miles** | — | — |

* **Structure table.** Four different structures: two per-operator structures naming different operators, a three-class seam split ordering
  430 miles, and the three-class service split ordering 370. No lower rung holds the answer's partition or its order scope.
* **Separation at the decisive rung.** At the measured multiple (4.3, the mean of the four LF-ERW conversions) the converted miles run at 7.3
  per thousand mile-years in 2027, level with LF-ERW that has always cycled (7.3) and 4.3× the pooled pre-1970 class (1.7). At the low end of
  the measured range (3.9) they still sit within 1.5× of the batch class (6.6 against 7.3) and 3.9× the pooled class.
* **Partial correction priced (L3).** A solver who splits LF-ERW by each line's own 2021–2026 record finds the 120 converted miles at 1.5
  per thousand mile-years, puts them and the 60 steady miles in a class of their own, and orders inspection of the 250 always-cycling miles:
  four classes and an order 120 miles short. A solver who sees the conversion but applies the integrity guidance's assumed 1.3× allowance
  puts the converted miles at 2.2, within 1.5× of steady pipe, and orders the same 250 miles. Both name structures no rung names.
* **Grid.** Monitored unit (operator or class) × tie handling (documented tie-break or open gaps) × rate basis (seam record, line record,
  monitoring year at the measured multiple) = 12 cells. Operator cells name X or Y; class cells name the 430-mile seam split, the four-class
  250-mile line split, or the answer, which only the monitoring-year basis reaches (with either tie handling, which class charts do not use).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The service register records operating modes and conversion dates for tariff purposes, and the change log records
   conversions as operational events; no document reports what a conversion did to failures or connects service to seam fatigue.
2. **Corpus blind for a computable reason.** *In every transfer the segment kept its operating mode, because the commission's transfer
   approvals require the acquirer to run the line as filed for two years.* The transfer log certifies that rates follow the pipe (rung 1's
   kill and rung 2's construction) and is silent on what a change of service does.
3. **No arithmetic symptom.** Inventory miles sum to the federal totals, incidents tie to the regulator's annual summary, and every class
   chart reproduces from the incident dates.
4. **Not a row predicate.** Each conversion's multiple is a before-and-after rate within one line, computed for six events and joined to
   seam type through the inventory, then carried to the 2025 conversions' steady-service rate and tested against the 1.5× rule.
5. **The enumeration is arithmetic.** Which lines belong to the 2027 batch class is computed; no column carries a line's monitoring-year
   rate.
6. **No cutover date.** The 2025 conversion has not stepped the converted miles' record (one failure since); the decision turns on a
   multiple measured across six earlier conversions, not on finding a step.
7. **Survives deletion.** Remove the operations view and the old charts, and the seam-split class build is still the natural one.

## 6. The calibration corpus

* **Form.** The integrity change log: nine operator transfers (2015–2024) and six conversions to batch service (2016–2022), each with four
  years of incidents and mileage before and after.
* **What it certifies.** Rates follow the pipe through transfers: each segment's post-transfer rate is within 12% of its pre-transfer rate.
  The rival "rate follows the operator" predicts each segment at its acquirer's system rate and misses eight of nine by 40% or more, all
  toward the acquirer, so it fails on the total as well. A back-tester is confirmed at rung 2.
* **What it is blind to.** Changes of service (above). The refusal sits in the less inviting record, the six conversions: four LF-ERW lines
  at 3.9–4.6× within two years, two seamless lines within ±10%, and no LF-ERW conversion under 3.9.
* **Twin pair.** Harlan and Mercer counties each hold 120 miles of 1950s LF-ERW with identical inventory columns and one failure each in
  2021–2026. Forty of Harlan's miles are among Y's 2025 conversions, so at the measured multiple Harlan's LF-ERW will fail 2.1× as often as
  Mercer's in 2027; only the service register and the multiple separate them.
* **Resemblance points at the decoy.** On every column of the record the converted miles resemble Y's steady LF-ERW, which has not failed
  since 2019.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The commission's rule: no chart may pool pipe whose incident rates in the monitoring year differ by more than 1.5×, and a
  signalling population receives an inspection order. The monitoring standard: chart construction, the review date and the share defined as
  the lowest value consistent with every file of record. The service register as the record of each line's operating mode. One sentence
  each.
* **Empirical pins.** That rates follow the pipe, from the transfers; the conversion multiple, from the six conversions.
* **Voices.** The head of operations: "X has not been the same since the reorganisation." The integrity engineer: "A line's own record is
  the best guide we have, and Y's new batch line has been clean."
* **Licensed wrong basis.** The standard records that the operators' association applies the integrity guidance's assumed 1.3× allowance
  for cycling service and will present its classes at the filing hearing.

## 8. Determinism by construction

* **The multiple.** The four LF-ERW conversions run 3.9–4.6×; at either end the converted miles sit within 1.5× of the batch class and at
  least 3.9× the pooled class, so no point estimate inside the range is a fork.
* **Steady-service rate.** The converted miles' steady-service rate comes from their own 2015–2024 record (1.7 per thousand mile-years);
  2018–2024 or 2015–2024 windows give 1.6–1.8, and no LF-ERW line changed mode in the window except Y's 2025 conversion.
* **Chart settings.** The transformation, the baseline (2015–2020) and the limits are filed in the standard; the review date is 30 June
  2026.
* **Seam and line of incidents.** Every incident report carries the failed segment's line, seam type and decade, with no blanks.

## 9. Prompt sketch and deliverables

> The 2027 monitoring structure goes to the commission on 1 December: which pipe gets its own rare-incident chart, and which chart, if any,
> is signalling now and needs an inspection order. Operations is sure X has slipped since its reorganisation. Give me the classes and the
> signalling one in a paragraph I can file, with the miles any order would cover to the nearest ten, plus `monitor_structure.xlsx`, a chart
> `class_charts.png`, and a one-page `filing_note.pdf`.

* `monitor_structure.xlsx` — rates by class on each basis, the assessments sheet (ask A), the one-call sheet (ask B) and the structure table
  (ask C).
* `class_charts.png` — one panel per adopted class: transformed gaps since 2021, centre line and lower limit labelled with their values, the
  2025 conversions' miles marked within the batch class, and the signalling points marked.
* `filing_note.pdf` — the committed structure, the signalling class and the order's scope.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each operator, in-line inspection runs completed in 2025 and the miles assessed. *Device:* a
  run repeated after a tool failure keeps its run ID with a revision suffix, and the assessment guide counts only the accepted revision.
  Counting every revision inflates four operators. The monitor never uses assessment records.
* **Ask B (device-carried).** For each operator, 2025 excavation tickets with a marking dispute and the share resolved within the statutory
  two business days. *Device:* business days exclude the holidays in the one-call centre's calendar; calendar days misstate the share for
  four operators.
* **Ask C (validity).** For each of the four rung structures: its monitored populations, which chart signals, the order's miles, and its
  result on the nine transfers and the six conversions.
* **Decoupling.** Clearing the conversion multiple and the open-gap rule changes no figure in asks A or B.

## 11. Rubric arithmetic

10 operators × 2 (ask A) + 10 × 2 (ask B) + 4 structures × 2 (ask C) + the committed classes, the signalling class, the order's miles and
the conversion multiple + 5 named chart parts + 3 files ≈ 60 criteria.

## 12. World-building constraints

* 6,200 miles; pre-1970 1,840 (LF-ERW 430: 250 in batch service throughout, 120 converted in March 2025, 60 steady); post-1970 4,360.
  Incidents since 2021: LF-ERW 11 (10 on the always-batch miles, 1 on the converted miles in December 2025), other pre-1970 13, post-1970 14.
* Rates per thousand mile-years over 2021–2026: always-batch LF-ERW 7.3, all LF-ERW 4.6, other pre-1970 1.7, post-1970 0.6; the converted
  miles 1.5 on their record.
* Change log: nine transfers within 12%; six conversions, four LF-ERW at 3.9–4.6× within two years and two seamless within ±10%.
* Y holds 300 LF-ERW miles (120 always-batch, the 120 converted and the 60 steady) and Z 130 always-batch. Six operators tie at 100% on
  closed gaps; only Y stays there with open gaps counted.
* Harlan and Mercer are identical on every inventory and record column.
* Assessment records and one-call tickets never touch incident reports, the inventory, the service register or the change log.
