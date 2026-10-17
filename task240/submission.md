# task240 submission

## Tags

**Domain:** Survey Research & Official Statistics (nonresponse, calibration and measurement-error adjustment: the sampling error of a household survey's post-stratified regional estimates, judged against the commissioning statistics branch's low-reliability line).
**Analytical objective:** Data Quality Monitoring & Alerting (which of the wave's published estimates carry the low-reliability warning in the quality report delivered with the tables).

## 1. Final Recommendation

**Nine of the 48 estimates carry the low-reliability warning: adults in privately rented homes in North West (R02); adults providing unpaid care in Far North (R01), North West (R02), North East (R03), Lakes (R04); adults in households behind on a household bill in Far North (R01), North West (R02), North East (R03), Lakes (R04). The other 39, the public pension estimates of all twelve regions among them, do not.**

Each warned estimate's coefficient of variation is 27.6 per cent or more and every other estimate's 18.4 or less, against the line of 20.0. The final weights were post-stratified within health region, age group and sex, so the estimate as published is a post-stratified estimator, and its Taylor linearisation is each adult's departure from the weighted rate of their cell, not the adult's own weighted value. Treating the final weights as fixed instead warns 15 estimates, adding R01 PEN, R01 RENT, R02 PEN, R03 PEN, R03 RENT, R04 PEN: the number receiving a public pension is almost fixed by the age and sex totals the weights were scaled to, and the fixed-weight error counts the weights' spread as sampling error.

## 2. Critical Components

1. The public pension estimates of the four northern regions carry no warning: coefficients of variation **5.0** (R01), **7.5** (R02), **8.4** (R03), **6.5** (R04).
2. The private renting estimates of Far North (R01) and North East (R03) carry no warning: **18.4** and **16.5**.
3. The nine warned estimates' coefficients of variation are all **27.6 or more**; the highest of the other 39 is **18.4**.

## 3. Step-by-Step Solution

1. Built the responding adults: the members aged 16 and over in hrs27_household_members.csv joined to hrs27_final_weights.csv on household and person number, and to hrs27_households.csv on household for health region, stratum, PSU and the household answers: 7,238 adults in 3,764 households, 707 PSUs in 24 strata.
2. Coded the four estimates from hrs27_codebook.xlsx (sheet Published tables): pension = 1, tenure = 3 for every adult in the household, care = 1, arrears = 1 for every adult in the household; don't know and refused not counted, proxy answers counted (QS-7 2.3).
3. Estimated each of the 48 totals with the final weights (QS-7 2.1).
4. Read hrs27_weighting_note.docx: the final weights are the design weights post-stratified within the 96 cells of health region, age group (16 to 29, 30 to 49, 50 to 64, 65 and over, from age at interview) and sex. The estimate as published (QS-7 3.2) is therefore a post-stratified total, and its Taylor linearisation is z = w(y - p), where p is the weighted rate of the adult's cell.
5. Totalled z by PSU, took each stratum's with-replacement variance (n_h/(n_h - 1) times the sum of squared deviations of the PSU totals from their stratum mean), summed over the region's strata, and divided the standard error by the unrounded estimate (QS-7 3.1).
6. Applied the 20.0 per cent line (QS-7 3.3): 9 estimates carry the warning. The same 9 follow from a delete-one-PSU jackknife with every replicate post-stratified again; with the final weights held fixed the linearisation warns 15.
7. Response rates (QS-7 4.1 and 4.2): every address in hrs27_issued_sample.csv (7,823) in the health region its PSU lies in, read from the PSU's region in hrs27_households.csv (the master-sample code in hrs27_issued_sample.csv predates the 2025 boundary review for 12 PSUs); each address's outcome from its last issue in hrs27_outcomes_2027-09-30.csv, every household in hrs27_households.csv taken as a full interview (the 30 September extract still holds 107 of them under an earlier status: their interviews reached the office after it was taken, as the call records' receipt times show), and the 94 issued addresses absent from the extract, each with only its advance letter in the call records, counted as eligibility not established; e = 0.9170 across the wave.
8. Calls (QS-7 4.3): the visit and telephone records in hrs27_call_records.csv for every issue of each address with a full interview, a call a tablet wrote twice (same address, issue, time, type, result and interviewer, 769 copies) counted once, by health region.

## 4. Deliverable Answers

### hrs27_quality_report.xlsx

1. Each estimate's coefficient of variation (per cent) and warning:
   - Far North (R01): adults receiving a public pension 5.0; adults in privately rented homes 18.4; adults providing unpaid care 27.6, warned (E); adults in households behind on a household bill 30.1, warned (E)
   - North West (R02): adults receiving a public pension 7.5; adults in privately rented homes 32.7, warned (E); adults providing unpaid care 48.7, warned (E); adults in households behind on a household bill 39.4, warned (E)
   - North East (R03): adults receiving a public pension 8.4; adults in privately rented homes 16.5; adults providing unpaid care 38.6, warned (E); adults in households behind on a household bill 30.0, warned (E)
   - Lakes (R04): adults receiving a public pension 6.5; adults in privately rented homes 12.6; adults providing unpaid care 34.3, warned (E); adults in households behind on a household bill 28.1, warned (E)
   - Capital (R05): adults receiving a public pension 2.2; adults in privately rented homes 6.2; adults providing unpaid care 8.0; adults in households behind on a household bill 10.1
   - Central (R06): adults receiving a public pension 1.9; adults in privately rented homes 6.5; adults providing unpaid care 9.3; adults in households behind on a household bill 10.1
   - East (R07): adults receiving a public pension 2.4; adults in privately rented homes 6.8; adults providing unpaid care 9.4; adults in households behind on a household bill 10.2
   - South East (R08): adults receiving a public pension 2.8; adults in privately rented homes 9.7; adults providing unpaid care 9.4; adults in households behind on a household bill 12.2
   - South (R09): adults receiving a public pension 2.8; adults in privately rented homes 10.7; adults providing unpaid care 9.5; adults in households behind on a household bill 14.3
   - South West (R10): adults receiving a public pension 3.7; adults in privately rented homes 10.1; adults providing unpaid care 9.1; adults in households behind on a household bill 11.7
   - West (R11): adults receiving a public pension 4.6; adults in privately rented homes 15.1; adults providing unpaid care 14.2; adults in households behind on a household bill 14.0
   - Valley (R12): adults receiving a public pension 3.0; adults in privately rented homes 12.4; adults providing unpaid care 12.8; adults in households behind on a household bill 14.1
2. Each health region's response rate (per cent) and calls to its addresses with a full interview:
   - Far North (R01): 59.6, 96 calls
   - North West (R02): 49.9, 78 calls
   - North East (R03): 48.7, 120 calls
   - Lakes (R04): 52.7, 169 calls
   - Capital (R05): 50.2, 1,660 calls
   - Central (R06): 53.6, 1,602 calls
   - East (R07): 52.1, 1,238 calls
   - South East (R08): 51.3, 987 calls
   - South (R09): 55.9, 873 calls
   - South West (R10): 54.8, 728 calls
   - West (R11): 50.0, 454 calls
   - Valley (R12): 54.4, 425 calls

### hrs27_quality_note.docx

3. The note the Branch publishes with the tables, naming the nine warned estimates with their coefficients of variation: R01 adults providing unpaid care 27.6; R01 adults in households behind on a household bill 30.1; R02 adults in privately rented homes 32.7; R02 adults providing unpaid care 48.7; R02 adults in households behind on a household bill 39.4; R03 adults providing unpaid care 38.6; R03 adults in households behind on a household bill 30.0; R04 adults providing unpaid care 34.3; R04 adults in households behind on a household bill 28.1.
