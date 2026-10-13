# task451 submission

## Tags

**Domain:** Healthcare Delivery & Health Economics, payment, claims and health plan analytics (a multiemployer health fund's 2026 shared-loss reconciliation with its accountable care partners, the open service months completed from the claims' development).
**Analytical objective:** Data Extraction & Conformation (ETL) (the claims administrator's versioned extract across its platform change, the hour-bank eligibility spans, the monthly attribution roster, the pharmacy benefit manager's claims and the partners' clinician roster conformed into each partner's 2026 total cost of care per attributed member month, its members' pharmacy spending and its professional spending outside the group).

## 1. Final Recommendation

**Four of the twelve partners owe the Fund a shared-loss payment for 2026: Stonecrest Internal Medicine, Bellmont Clinic Network, Kettle Run Health Partners and Harrow Point Medical Group.**

With the claims not yet paid developed on their received dates, their 2026 total cost of care per attributed member month is 108.9% to 109.4% (Stonecrest), 107.1% to 107.5% (Bellmont), 103.7% to 104.1% (Kettle Run) and 103.2% to 103.7% (Harrow Point) of target, each more than 2.0 per cent over, and none of the other eight is over the corridor. Not the nine partners a paid-date chain ladder over 2025 and 2026 names, adding Ashby Lane, Calder, Juniper Hollow, Ridgeline and Tamarack: its factors carry the old receipt-to-payment time (a median of 23 days) into the October to December claims that Tallis pays in a day. Not Bellmont and Stonecrest alone, which the claims paid through January give with nothing estimated for the claims still to come, though Schedule B counts them whenever paid.

## 2. Critical Components

1. Stonecrest Internal Medicine's 2026 total cost of care is **108.9% to 109.4%** of its target and Bellmont Clinic Network's **107.1% to 107.5%**.
2. Kettle Run Health Partners' is **103.7% to 104.1%** and Harrow Point Medical Group's **103.2% to 103.7%**, both more than 2.0 per cent over.

## 3. Step-by-Step Solution

1. Kept each claim's latest version in medical_claims_extract_2025-01_2027-01.csv (a replacement carries the claim's full corrected amounts and a void zero, under the legacy O, A, V and the Tallis 1, 7, 8 frequency codes in keswold_extract_dictionary_2027-02-01.txt) and its medical claims with a first date of service in 2026, each in the month of that first date (Schedule B, B.1.4).
2. Attributed claims and member months to partners through attribution_roster_2026.csv in months the member is eligible on the latest version of each span in eligibility_spans_2025-2027.csv (B.1.3), and took off each member's 2026 paid amount above $200,000, shared across partners in proportion (B.1.5): 7 members.
3. Measured the claims' timing on their first versions: from receipt to payment, a median of 23 days for claims received before 5 October 2026, when the dictionary's release note moves the Fund's claims to Tallis, and 1 day after; from the last date of service to receipt, which the providers set, a median of 13 days for claims received in 2025 and 14 for claims received from 5 October 2026.
4. Completed each 2026 service month on the received dates (B.3.1): every claim's paid amount in the extract (its latest version) by month of first service and month received from January 2025, volume-weighted chain-ladder link ratios over all of it, and each month's factor at its development in January 2027 applied to each partner's paid amount for that month; the same link ratios from the latest twelve receipt months only, and the same by claim type (professional, outpatient, inpatient), give the ranges in step 5, and a paid-date chain ladder using only the link ratios into the payment months November 2026 to January 2027 names the same four partners.
5. Divided by attributed member months (B.1.6) and compared each partner with its Exhibit 1 target unrounded (B.2.1, B.2.3): Stonecrest 108.9% to 109.4%, Bellmont 107.1% to 107.5%, Kettle Run 103.7% to 104.1% and Harrow Point 103.2% to 103.7% of target, the other eight under 102%; a paid-date chain ladder of each version's payment by the month it was paid, over all of 2025 and 2026, overstates the year by 10 per cent and names nine partners.
6. Matched each fill in corvane_pharmacy_claims_2026.csv to the Fund member with the same cardholder, date of birth and sex (corvane_claims_file_layout_v4.pdf numbers dependants by date of birth, laurelford_data_notes_2027-02.docx by order of enrollment), netted reversals, and summed plan paid in each member's attributed member months by partner (B.4.1(a)).
7. Took each partner's professional claims from step 2 as paid through 29 January 2027, before B.1.5, and the share of their paid amount billed under any NPI other than the partner's group NPI in Exhibit 1, the group a clinician billed through when the service was given (B.4.1(b)).
8. Recommendation: Stonecrest Internal Medicine, Bellmont Clinic Network, Kettle Run Health Partners and Harrow Point Medical Group owe the Fund a shared-loss payment for 2026.

## 4. Deliverable Answers

### partner_settlement_2026.xlsx

1. Whether each partner owes a shared-loss payment for 2026:
   - Owes: Stonecrest Internal Medicine, Kettle Run Health Partners, Harrow Point Medical Group, Bellmont Clinic Network
   - Does not owe: Ridgeline Physician Group, Brookhollow Medical Associates, Sycamore Pediatric Partners, Wren Valley Physicians, Calder Family Practice, Tamarack Health Alliance, Juniper Hollow Primary Care, Ashby Lane Medical
2. The Fund's 2026 pharmacy spending for each partner's members, to the nearest thousand dollars, in the workbook's order:
   - Ridgeline Physician Group: $550,000
   - Brookhollow Medical Associates: $581,000
   - Sycamore Pediatric Partners: $403,000
   - Stonecrest Internal Medicine: $553,000
   - Kettle Run Health Partners: $525,000
   - Harrow Point Medical Group: $577,000
   - Wren Valley Physicians: $533,000
   - Bellmont Clinic Network: $505,000
   - Calder Family Practice: $524,000
   - Tamarack Health Alliance: $660,000
   - Juniper Hollow Primary Care: $579,000
   - Ashby Lane Medical: $543,000
3. The share of each partner's members' 2026 professional spending, as paid through January, that went to clinicians who were not then with the partner, to one decimal place, in the workbook's order:
   - Ridgeline Physician Group: 35.9%
   - Brookhollow Medical Associates: 42.1%
   - Sycamore Pediatric Partners: 31.6%
   - Stonecrest Internal Medicine: 40.7%
   - Kettle Run Health Partners: 32.1%
   - Harrow Point Medical Group: 44.5%
   - Wren Valley Physicians: 31.4%
   - Bellmont Clinic Network: 38.4%
   - Calder Family Practice: 30.3%
   - Tamarack Health Alliance: 41.6%
   - Juniper Hollow Primary Care: 26.2%
   - Ashby Lane Medical: 39.9%

### partners_against_target_2026.png

4. Bar chart of each partner's 2026 total cost of care per attributed member month as a share of its Exhibit 1 target, the 102 per cent line marked and the four owing partners in dark bars.
