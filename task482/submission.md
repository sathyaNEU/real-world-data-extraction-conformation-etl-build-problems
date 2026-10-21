## Tags

**Domain:** Survey Research & Official Statistics (census, register and administrative data quality).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Send AR01, AR05, AR08, AR11 and AR12 to the 2027 re-validation.**
Their registers' share of records in error exceeds 4 per cent; no other region's does. The summer audit drew the records the May risk screen had referred far more often than the rest, and referred records are in error far more often, so each audited record is carried to its stratum's records on the 30 April register. Read as the audited share, 11 regions would go (AR01, AR02, AR04, AR05, AR06, AR07, AR08, AR10, AR11, AR12 and AR13), at audited error shares the registers themselves do not have.

## 2. Critical Components

1. Regions going to re-validation: **AR01**, **AR05**, **AR08**, **AR11**, **AR12**
2. Regions not going: AR02, AR03, AR04, AR06, AR07, AR09, AR10, AR13, AR14

## 3. Step-by-Step Solution

1. Took the 30 April 2026 register: records created before 1 May in Ardmuir local time (the extract's times are UTC, an hour behind in summer), active and since dissolved.
2. Marked each record referred or not from the May risk screen's referral list.
3. Joined the audit outcomes by record, old region codes through the crosswalk; FAIL and codes 1 to 4 are errors.
4. In each region and stratum (referred, not referred) took the audited error rate and carried it to the stratum's records on the 30 April register; summed and divided by the region's records.
5. Chose the regions over 4 per cent: AR01, AR05, AR08, AR11, AR12.
6. Ask A: registrations created from 1 July to 30 September 2026 in Ardmuir local time.
7. Ask B: companies whose last notice in the quarter is struck off and dissolved (a later restoration takes a company back onto the register).

## 4. Deliverable Answers

### sar_register_revalidation_2027_regions.xlsx

1. Regions going to re-validation: AR01, AR05, AR08, AR11, AR12.
2. Chart of each region's register error rate against the 4 per cent line, the chosen regions marked.
3. New registrations in the third quarter of 2026:
   - AR01: 241
   - AR02: 108
   - AR03: 77
   - AR04: 118
   - AR05: 64
   - AR06: 85
   - AR07: 55
   - AR08: 152
   - AR09: 51
   - AR10: 104
   - AR11: 67
   - AR12: 88
   - AR13: 121
   - AR14: 76
4. Companies struck off and dissolved in the quarter and still dissolved at its end:
   - AR01: 195
   - AR02: 90
   - AR03: 69
   - AR04: 93
   - AR05: 42
   - AR06: 74
   - AR07: 49
   - AR08: 107
   - AR09: 36
   - AR10: 70
   - AR11: 68
   - AR12: 100
   - AR13: 66
   - AR14: 36
