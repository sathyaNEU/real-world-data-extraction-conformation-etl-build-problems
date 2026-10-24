## Tags

**Domain:** Healthcare Delivery & Health Economics, payment, claims and health plan analytics (a hospice organisation's EMR admissions, its acquired hospice's census register, claim lines and remittances and the Medicare hospice benefit periods extract conformed into the FY2026 aggregate cap schedule its December 2026 accrual reads).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Accrue USD 0.3 million for FY2026 Medicare hospice cap repayments, all of it at Fallowmere Hospice (provider number 361798); the other seven provider numbers are under their caps.**
Fallowmere's FY2026 payments before sequestration of USD 6,636,768 run above its aggregate cap once each beneficiary it discharged alive carries the hospice days still expected after the close. Not nothing, which taking every beneficiary discharged alive as finished gives: two in five of Fallowmere's elections end in a live discharge, and the extract's later benefit periods show many of those beneficiaries electing hospice again, most at hospices outside the organisation.

## 2. Critical Components

1. Fallowmere's FY2026 payments before sequestration are **USD 6,636,768**.
2. Fallowmere has **304** FY2026 beneficiaries: at 31 December 2026 **62** on service, **44** discharged alive and not back, **198** died.
3. Fallowmere's FY2026 repayment is **USD 0.3 million**; every other provider number's is nil.

## 3. Step-by-Step Solution

1. Read medicare_hospice_benefit_periods_20270105.txt (66,364 benefit periods, the periods sharing an election date one stay), with wendleglen_emr_admissions.csv and fallowmere_census_register_20250228.xlsx matched to MBIs through hicn_mbi_crosswalk.csv and each beneficiary's group taken from diagnosis_groups.csv: 3,540 FY2026 beneficiaries across the eight provider numbers.
2. Took each beneficiary's FY2026 days at each provider number, days to 31 December 2026 in every hospice and year, and state at the close (at Fallowmere 62 on service, 44 discharged alive and not back, 198 died).
3. Read the days expected after the close from the experience since 1 October 2016 of the provider number that cared for the beneficiary last, in the beneficiary's group (wendleglen_cap_liability_policy.docx section 2.4): for a stay still open, the further days of that provider number's stays that had run as long (Kaplan-Meier), plus the chance such a stay ends alive times the chance of a later election times the days a later election brings.
4. For a beneficiary discharged alive and alive at the close, the chance of a later election at any hospice among the provider number's live discharges still alive and not back after as many days out (Aalen-Johansen on the extract's later elections and dates of death), times the days a later election brings (the Kaplan-Meier mean of those elections); a beneficiary who died has none.
5. Counted each beneficiary at each provider number as its FY2026 days over the days to the close plus the expected days (section 2.3) and multiplied each provider number's count by USD 35,361.44 (section 2.1).
6. Summed each provider number's FY2026 payments from remittance_register_fy2026.csv (CLP rows with reversals, adj_carc_253 added back, PLB interest left out) and took 98 per cent of any excess over the cap (section 3.2): only Fallowmere's payments exceed its cap.
7. For the inpatient cap, took the version of each FY2026 claim in wendleglen_claim_lines_fy2026.csv that remittance_register_fy2026.csv shows paid and not reversed (a returned replacement was never paid, so the claim it would have replaced stands), repriced it from its dated level-of-care lines with fy2026_hospice_payment_rates.pdf, the routine care count from the extract and the wage index in provider_numbers.json, and where the payment falls short, counted its last general inpatient and respite days paid at the routine rate (the one count that closes the gap to the cent) out of the 0656 and 0655 units, over each provider number's FY2026 days of care in the extract.
8. The accrual is as in the Final Recommendation.

## 4. Deliverable Answers

### fy2026_hospice_cap_accrual.xlsx

1. FY2026 aggregate cap repayments to accrue, USD millions to one decimal:
   - Brindlemoor (361791): 0.0
   - Corvelfield (361792): 0.0
   - Darrelbrook (361793): 0.0
   - Marrellford (361794): 0.0
   - Rennickdale (361795): 0.0
   - Varrowmere (361796): 0.0
   - Farrinridge (361797): 0.0
   - Fallowmere Hospice (361798): 0.3
   - Total: 0.3
2. FY2026 inpatient cap, general inpatient days and inpatient respite days Medicare paid for (whole days) and the inpatient share of days of care (per cent to one decimal):
   - Brindlemoor (361791): general inpatient 837, respite 69, share 2.7
   - Corvelfield (361792): general inpatient 1,280, respite 158, share 3.0
   - Darrelbrook (361793): general inpatient 716, respite 159, share 1.9
   - Marrellford (361794): general inpatient 195, respite 60, share 0.8
   - Rennickdale (361795): general inpatient 1,047, respite 151, share 3.1
   - Varrowmere (361796): general inpatient 478, respite 157, share 1.1
   - Farrinridge (361797): general inpatient 413, respite 93, share 1.5
   - Fallowmere Hospice (361798): general inpatient 327, respite 72, share 1.4
3. The cap schedule: one row per FY2026 beneficiary per provider number (3,572 rows) with the FY2026 days there, the hospice days to the close, the days expected after it and the share counted.
