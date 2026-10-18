## Tags

**Domain:** Survey Research & Official Statistics (anomaly detection in official waste statistics).
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**The 2027 supplementary collection module goes to Metal and metal-bearing wastes, the only stream whose 2026 recovery rate is established below its plan target.**

Its rate is 56.6 per cent against a 59.5 per cent target, a 2.9 point shortfall at 4.57 standard errors, and its 95 per cent interval of 55.4 to 57.8 per cent excludes the target. Not Mixed commercial and industrial wastes, which leads on the size of the shortfall at 4.9 points but stands at only 1.45 standard errors because its arisings estimate is the least precise of the eight. Not any of the remaining six streams, none of which reaches 1.45 standard errors.

## 2. Critical Components

1. Tonnage confirmed received at a recovery operation for Metal and metal-bearing wastes is **70,384 t**
2. Its estimated arisings are **124,354 t**
3. Its 2026 recovery rate is **56.6 per cent** against a plan target of **59.5 per cent**
4. The rate's 95 per cent interval is **55.4 to 57.8 per cent**, which lies wholly below the target
5. The shortfall for Mixed commercial and industrial wastes is **4.9 points** at **1.45 standard errors**, so it is not established

## 3. Step-by-Step Solution

1. Mapped the renamed columns of waste_movement_legs_2026_h2.csv onto waste_movement_legs_2026_h1.csv and resolved every waste code through waste_code_crosswalk.csv, honouring its mid-year revision: 82,835 legs for consignments despatched in the reference year.
2. Chained each producer consignment to its final treatment using facility_register.csv for the facility role and treatment_operation_codes.xlsx for the operation kind, and counted each tonnage once at the producer's despatch leg: 70,384 t confirmed at a recovery operation for Metal and metal-bearing wastes.
3. Estimated each stream's arisings from bws_2026_microdata.csv by applying the design weight to every usable return in each stratum, the reported zeros included: 124,354 t for Metal and metal-bearing wastes.
4. Divided the two: a 56.6 per cent recovery rate.
5. Took the rate's sampling error as its denominator's alone, the register tonnage being a complete administrative total, and computed that error over each stratum of bws_2026_design_and_weighting.pdf with the stratum's own finite-population correction, so the completely enumerated large-enterprise stratum, which holds 95.8 per cent of this stream's arisings, contributes none of it: a standard error of 0.63 points.
6. Read each stream's target from national_waste_management_plan_targets.pdf and tested the shortfall against the standard error: 2.9 points at 4.57 standard errors.
7. Repeated for the other seven streams: Metal and metal-bearing wastes is the only one established below target, and the larger 4.9 point shortfall for Mixed commercial and industrial wastes stands at 1.45 standard errors.
8. Committed the module to Metal and metal-bearing wastes.

## 4. Deliverable Answers

### recovery_attainment_2026.xlsx

1. Attainment, a row per stream with confirmed recovered tonnage, estimated arisings, the recovery rate, its 95 per cent interval, the plan target and the shortfall:
   - Metal and metal-bearing wastes: 70,384 t recovered, 124,354 t arising, 56.6 per cent, interval 55.4 to 57.8 per cent, target 59.5 per cent, shortfall 2.9 points
   - Mixed commercial and industrial wastes: 93,294 t recovered, 156,533 t arising, 59.6 per cent, interval 53.0 to 66.2 per cent, target 64.5 per cent, shortfall 4.9 points
   - Paper and board wastes: 31,721 t recovered, 63,569 t arising, 49.9 per cent, interval 43.1 to 56.7 per cent, target 51.8 per cent, shortfall 1.9 points
   - Wood wastes: 20,003 t recovered, 45,773 t arising, 43.7 per cent, interval 36.7 to 50.7 per cent, target 45.3 per cent, shortfall 1.6 points
   - Mineral construction and demolition wastes: 95,414 t recovered, 158,494 t arising, 60.2 per cent, interval 44.8 to 75.6 per cent, target 62.6 per cent, shortfall 2.4 points
   - Glass wastes: 13,376 t recovered, 24,908 t arising, 53.7 per cent, interval 47.3 to 60.1 per cent, target 55.7 per cent, shortfall 2.0 points
   - Plastic wastes: 7,659 t recovered, 22,659 t arising, 33.8 per cent, interval 29.4 to 38.2 per cent, target 35.4 per cent, shortfall 1.6 points
   - Textile and leather wastes: 1,819 t recovered, 6,429 t arising, 28.3 per cent, interval 23.2 to 33.4 per cent, target 29.2 per cent, shortfall 0.9 points
2. Stage chain, a row per stream with the tonnage at each movement chain stage and the stage to stage pass through rate:
   - Metal and metal-bearing wastes: 124,354 t arising, 77,384 t despatched, 75,682 t confirmed at a final treatment operation, 70,384 t confirmed at a recovery operation, pass through 62.2 per cent, 97.8 per cent, 93.0 per cent
   - Mixed commercial and industrial wastes: 156,533 t arising, 146,634 t despatched, 141,355 t confirmed at a final treatment operation, 93,294 t confirmed at a recovery operation, pass through 93.7 per cent, 96.4 per cent, 66.0 per cent
   - Paper and board wastes: 63,569 t arising, 34,388 t despatched, 33,391 t confirmed at a final treatment operation, 31,721 t confirmed at a recovery operation, pass through 54.1 per cent, 97.1 per cent, 95.0 per cent
   - Wood wastes: 45,773 t arising, 22,937 t despatched, 22,226 t confirmed at a final treatment operation, 20,003 t confirmed at a recovery operation, pass through 50.1 per cent, 96.9 per cent, 90.0 per cent
   - Mineral construction and demolition wastes: 158,494 t arising, 102,677 t despatched, 98,365 t confirmed at a final treatment operation, 95,414 t confirmed at a recovery operation, pass through 64.8 per cent, 95.8 per cent, 97.0 per cent
   - Glass wastes: 24,908 t arising, 14,305 t despatched, 13,933 t confirmed at a final treatment operation, 13,376 t confirmed at a recovery operation, pass through 57.4 per cent, 97.4 per cent, 96.0 per cent
   - Plastic wastes: 22,659 t arising, 11,001 t despatched, 10,638 t confirmed at a final treatment operation, 7,659 t confirmed at a recovery operation, pass through 48.6 per cent, 96.7 per cent, 72.0 per cent
   - Textile and leather wastes: 6,429 t arising, 3,438 t despatched, 3,307 t confirmed at a final treatment operation, 1,819 t confirmed at a recovery operation, pass through 53.5 per cent, 96.2 per cent, 55.0 per cent
3. Collection effort, a row per region with the field days consumed and the usable returns per field day:
   - Norte: 32.54 field days, 16.53 usable returns per field day
   - Centro: 25.69 field days, 14.83 usable returns per field day
   - Lisboa: 29.80 field days, 14.43 usable returns per field day
   - Alentejo: 10.11 field days, 16.42 usable returns per field day
   - Algarve: 7.66 field days, 15.01 usable returns per field day
4. Tonnage confirmed received at a recovery operation in the prior reference year, per stream:
   - Metal and metal-bearing wastes: 67,709 t
   - Mixed commercial and industrial wastes: 89,749 t
   - Paper and board wastes: 30,516 t
   - Wood wastes: 19,243 t
   - Mineral construction and demolition wastes: 91,788 t
   - Glass wastes: 12,868 t
   - Plastic wastes: 7,368 t
   - Textile and leather wastes: 1,750 t
5. Municipal reconciliation, a row per region with the gap between reported collections and licensed facility receipts on a receipt date basis, and that gap as a share of collections:
   - Norte: 118,494 t collected, 115,419 t received, gap 3,075 t, 2.6 per cent of collections
   - Centro: 121,209 t collected, 116,299 t received, gap 4,910 t, 4.1 per cent of collections
   - Lisboa: 112,806 t collected, 108,725 t received, gap 4,081 t, 3.6 per cent of collections
   - Alentejo: 75,192 t collected, 72,603 t received, gap 2,589 t, 3.4 per cent of collections
   - Algarve: 85,532 t collected, 82,069 t received, gap 3,463 t, 4.0 per cent of collections

### attainment_against_target_2026.png

1. One horizontal bar per stream giving the 2026 recovery rate, a whisker for the 95 per cent interval and a vertical mark at the plan target, ordered by standard errors from target, with Metal and metal-bearing wastes drawn in the darker fill and labelled as established below target.

