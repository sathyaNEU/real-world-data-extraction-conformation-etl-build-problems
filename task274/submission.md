## Tags

**Domain:** Survey Research & Official Statistics (nonresponse, calibration and measurement-error adjustment).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Open the 2027 vitamin D programme first in Wexmoor, Corvale, Lassiter and Inskeep: in each, more than 30 per cent of adults had serum 25(OH)D below 20 ng/mL on the reference measurement procedure's scale in the 2025 wave.**
Each 2025 result is put on the reference scale through the calibration it was measured under: the October accuracy check fixes the bias of IA1's calibration of 2025-10-12, and the December bridging run carries it to every calibration of both analyzers.

## 2. Critical Components

1. Accuracy-based check, event 2025-B (IA1, reagent lot 43012, 15 October 2025): mean difference **+13.4 per cent** from the reference values, under the IA1 calibration of 2025-10-12 07:50.
2. Bridging run: **959** stored duplicates paired with the same adults' primary results; the run reads about **20 per cent** above the reference scale.
3. The 4,861 final primary results were measured under **35** calibrations (17 on IA1, 18 on IA2), each with its own shift against the bridging run.
4. Share of adults below 20 ng/mL on the reference scale, to the nearest whole per cent: Wexmoor 36, Corvale 34, Lassiter 32, Ulverne 24, Vellance 20, Quennel 20, Yarrowmere 26, Inskeep 33.
5. Every county stands at least **1.6 points** from 30 per cent.

## 3. Step-by-Step Solution

1. Kept the final results (RESULT_STATUS F) in lis_vitd_results_2025.csv and joined each to its adult through the tracking export's labels (hyphen removed) and to county and WTMEC2025 through the examined persons file.
2. Placed each result under the calibration accepted on its analyzer most recently before it was run (analyzer_event_log_2025.csv in UTC, converted to Mountain time; LIS codes to serial numbers through the instrument register).
3. Paired each bridging result with the same adult's primary result and took, for each calibration, the mean of the log of the primary result over the bridging result.
4. Took the check's mean difference as the bias of the IA1 calibration in force on 15 October, so the bridging run's bias is that bias less the calibration's mean log ratio.
5. Divided each result by the bridging run's bias times its own calibration's ratio, weighted with WTMEC2025 and read each county's share below 20 ng/mL against 30 per cent.
6. Ask A: per adult, summed each product's vitamin D per unit (label amount in IU, mcg times 40, divided by the serving size; GENERIC lines as typed) times units a day times days taken, over 30; a GENERIC line that repeats one of the adult's labelled lines in strength per unit, days and units a day is that bottle's line appended by product matching and counts once; weighted with WTINT2025 over interviewed adults.
7. Ask B: where a dwelling was screened twice, kept the sample persons of its later screening only (the earlier screening's people were selected again); left out persons found ineligible; counted complete, partial and proxy interviews and persons examined at the MEC.

## 4. Deliverable Answers

### vitamin_d_status_2025.xlsx

1. Counties where the programme opens first: Wexmoor, Corvale, Lassiter, Inskeep; not Ulverne, Vellance, Quennel, Yarrowmere.
2. Interviewed adults whose supplements averaged at least 1,000 IU of vitamin D a day (per cent):
   - Wexmoor: 23.4
   - Corvale: 20.2
   - Lassiter: 20.3
   - Ulverne: 19.9
   - Vellance: 21.0
   - Quennel: 21.7
   - Yarrowmere: 22.1
   - Inskeep: 22.1
3. At least 2,000 IU a day (per cent):
   - Wexmoor: 9.0
   - Corvale: 8.3
   - Lassiter: 6.8
   - Ulverne: 6.4
   - Vellance: 8.5
   - Quennel: 9.6
   - Yarrowmere: 9.1
   - Inskeep: 8.7
4. Interview response rate (per cent):
   - Wexmoor: 80.1
   - Corvale: 81.9
   - Lassiter: 83.6
   - Ulverne: 77.7
   - Vellance: 80.4
   - Quennel: 78.3
   - Yarrowmere: 77.7
   - Inskeep: 80.9
5. Examination response rate (per cent):
   - Wexmoor: 62.6
   - Corvale: 63.7
   - Lassiter: 65.5
   - Ulverne: 68.7
   - Vellance: 66.5
   - Quennel: 64.3
   - Yarrowmere: 66.1
   - Inskeep: 60.2
