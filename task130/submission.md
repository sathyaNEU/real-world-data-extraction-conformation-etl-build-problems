## Tags

**Domain:** Actuarial Science & Insurance (pricing, ratemaking and credibility).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Corvane Health should put $784,000 into its professional liability trust for 2027.**
That is the expected cost of the 11.5 claims expected to be first made against the trust in 2027 from incidents on or after each entity's Transition Date. Not $4,854,000, a year of the experience's claims cost per FTE-year on each entity's FTE-years in the trust, because the trust pays only for the claims made by 31 December 2027 and those are the ones made soon after their incident. Not $1,784,000, the expected number of those claims at the average claim's cost, because the claims made soon after their incident cost far less than the average. Not $1,075,000, a full calendar year's in-year cost share applied to each entity's part year, because a part year catches a share that falls faster than its length.

## 2. Critical Components

1. The experience is **328** Claims, one per incident, from 2017 to 2024 incidents naming Covered Clinicians, against **6,188.6** covered FTE-years.
2. The trust's 2027 exposure is **555.8** covered FTE-years, each entity from its Transition Date.
3. The expected number of Claims first made against the trust in 2027 is **11.5**.

## 3. Step-by-Step Solution

1. From rm_claims_register_extract_20261002.csv, kept the incidents dated 2017 to 2024 whose rows name a Covered Clinician (a Schedule B job in clinician_fte_by_month_2016-01_2025-12.csv in the incident month, contracted rows aside), merged all claim numbers of an incident into one Claim made on its earliest claim_made_date per the trust agreement's Claim definition, and classed it by its first-named Covered Clinician per Schedule B: 328 Claims.
2. Valued each Claim at the paid and reserved indemnity and defense on its Covered Clinicians' rows, trended at 5.0% a year from the incident year to 2027 per the funding policy, and took its lag in days from the incident date to the Claim's first making.
3. Summed the covered FTE in clinician_fte_by_month_2016-01_2025-12.csv for 2017 to 2024 under both Schedule B code sets, each month one twelfth of an FTE-year, by specialty class: 6,188.6 FTE-years.
4. Spread each entity's monthly FTE in clinician_staffing_plan_2027.xlsx evenly over the days of each month from its Transition Date in Schedule A, per the funding policy: 555.8 FTE-years.
5. Charged each day of exposure its class's experience cost per FTE-year of the Claims whose lag, added to that day, falls on or before 31 December 2027, and counted those Claims the same way, the experience pooled within each class as recorded: 11.5 expected Claims costing $784,000.
6. Matched each entity's open register claims, one per incident, to its carrier's loss run valued 30 September 2026 on the insured reference, reading RMN references through rm_carrier_notices_2012_2026.csv and suits under their prior_claim_no: Alderwick 2 and the medical group 1 missing.
7. Counted one FTE per September 2026 position in hcm_clinician_pay_lines_2026-01_2026-09.csv, covered through hcm_job_profile_crosswalk.csv and Schedule B, on the entity of its cost centre in cost_centre_directory_2026.csv: 907.5 FTE.
8. Recommended the 2027 contribution of $784,000.

## 4. Deliverable Answers

### trust_funding_2027.xlsx

1. The 2027 contribution: $784,000.
2. Expected claims and cost by entity:
   - Tolliver Falls Hospital: 2.9 claims, $227,000
   - Alderwick Medical Center: 4.6 claims, $336,000
   - Corvane Medical Group: 3.9 claims, $214,000
   - Brennick Community Hospital: 0.1 claims, $7,000
3. Expected claims and cost by specialty class:
   - Obstetrics: 2.0 claims, $148,000
   - Surgery: 2.3 claims, $291,000
   - Emergency Medicine: 2.0 claims, $68,000
   - Anesthesiology: 0.5 claims, $65,000
   - Hospital and Medical Specialties: 2.3 claims, $124,000
   - Primary Care: 1.4 claims, $26,000
   - Advanced Practice: 1.0 claims, $62,000
4. Open claims under each entity's occurrence policies missing from its carrier's latest loss run, and our reserves on them:
   - Tolliver Falls Hospital: none
   - Alderwick Medical Center: 2 claims, $178,000
   - Corvane Medical Group: 1 claim, $6,000
   - Brennick Community Hospital: none
5. Covered clinician FTE in September 2026:
   - Tolliver Falls Hospital: 96.3
   - Alderwick Medical Center: 234.3
   - Corvane Medical Group: 522.0
   - Brennick Community Hospital: 54.9

### trustees_paper_2027.pptx

1. Slide 1 states the contribution, $784,000, with each entity's Transition Date, expected claims and expected cost.
2. Slide 2 charts each entity's expected cost of those claims by the month of 2027 they are made in, as stacked monthly columns, each entity from its Transition Date.
