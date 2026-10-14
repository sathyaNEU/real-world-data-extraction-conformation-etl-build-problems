## Tags

**Domain:** Actuarial Science & Insurance (pricing, ratemaking and credibility).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Corvane Health should put $587,000 into its professional liability trust for 2027.**
That is the expected cost of the 10.2 claims expected to be first made against the trust in 2027 from incidents on or after each entity's Transition Date, costed on Tolliver Falls' and Alderwick's experience because from its Transition Date every entity's patients can bring their claims through the Early Resolution Program, which until now served only those two hospitals. Not $312,000, the same claims-made window costed on the System's pooled experience, because the medical group's and Brennick's claims never came through the Program and a first claims-made year catches almost only the early requests it produces. Not $3,617,000, a year of the experience's cost per FTE-year, because the trust pays only for the claims first made by 31 December 2027. Not $966,000, the window's expected number of claims at the average claim cost, because the claims made soon after their incident cost far less than the average.

## 2. Critical Components

1. The experience generated under the Early Resolution Program is Tolliver Falls' and Alderwick's **123** Claims from 2017 to 2024 incidents, against their **2,655.2** covered FTE-years.
2. The trust's 2027 exposure is **599.9** covered FTE-years, each entity from its Transition Date.
3. The expected number of Claims first made against the trust in 2027 is **10.2**.

## 3. Step-by-Step Solution

1. From rm_claims_register_extract_20261002.csv, kept the incidents dated 2017 to 2024 whose rows name a Covered Clinician (a Schedule B job in clinician_fte_by_month_2016-01_2025-12.csv in the incident month, contracted rows aside), merged all claim numbers of an incident into one Claim made on its earliest claim_made_date per the trust agreement's Claim definition, classed it by its first-named Covered Clinician per Schedule B, and valued it at the paid and reserved indemnity and defense on its Covered Clinicians' rows trended at 5.0% a year from the incident year to 2027 per the funding policy: 192 Claims.
2. Took the experience the 2027 window will meet: the data dictionary's matter_type places the Early Resolution Program at Tolliver Falls and Alderwick since September 2015, the trust agreement's claims administration article opens it to every entity's patients from its Transition Date, and all 62 Claims made within 120 days of their incident are at those two hospitals, so the rate is built on their 123 Claims and the 2,655.2 FTE-years their cost centres paid in the payroll, by specialty class, one rate for every entity as the funding policy rates the entities alike.
3. Spread each entity's monthly FTE in clinician_staffing_plan_2027.xlsx evenly over the days of each month from its Transition Date in Schedule A, per the funding policy: 599.9 FTE-years.
4. Charged each day of exposure its class's cost per FTE-year, on that experience, of the Claims whose lag from incident to first making, added to that day, falls on or before 31 December 2027, and counted those Claims the same way: 10.2 expected Claims costing $587,000.
5. Split the contribution by each entity's share of the 2027 exposure, per section 2 of the funding policy: Tolliver Falls $111,000, Alderwick $201,000, the medical group $260,000, Brennick $15,000.
6. Matched each entity's open register claims, one per incident, to its carrier's loss run valued 30 September 2026 on the insured reference, reading RMN references through rm_carrier_notices_2012_2026.csv, and a carrier claim under a notice whose incident number holds no register claim as the register claim with the notice's entity, event date and category: Alderwick 1 and the medical group 1 missing.
7. Counted one FTE per September 2026 position in hcm_clinician_pay_lines_2026-01_2026-09.csv, covered through hcm_job_profile_crosswalk.csv and Schedule B, on the entity of its cost centre in cost_centre_directory_2026.csv rather than the home entity on the worker's current record: 957.3 FTE.
8. Recommended the 2027 contribution of $587,000.

## 4. Deliverable Answers

### trust_funding_2027.xlsx

1. The 2027 contribution: $587,000.
2. The expected number of claims first made against the trust in 2027: 10.2.
3. What each entity pays toward the contribution:
   - Tolliver Falls Hospital: $111,000
   - Alderwick Medical Center: $201,000
   - Corvane Medical Group: $260,000
   - Brennick Community Hospital: $15,000
4. Open claims under each entity's occurrence policies missing from its carrier's latest loss run, and our reserves on them:
   - Tolliver Falls Hospital: none
   - Alderwick Medical Center: 1 claim, $7,000
   - Corvane Medical Group: 1 claim, $20,000
   - Brennick Community Hospital: none
5. Covered clinician FTE in September 2026:
   - Tolliver Falls Hospital: 106.9
   - Alderwick Medical Center: 271.5
   - Corvane Medical Group: 525.0
   - Brennick Community Hospital: 53.9

### trustees_paper_2027.pptx

1. Slide 1 states the contribution, $587,000, with each entity's Transition Date and what it pays.
2. Slide 2 charts each entity's expected cost of those claims by the month of 2027 they are made in, as stacked monthly columns, each entity from its Transition Date.
