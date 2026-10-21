## Tags

**Domain:** General Statistics & Data Science (resampling and simulation).  
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**The FY2027 budget should carry 11 Decision Coaching Grants, $704,000, for H03, H06, H09, H10, H17, H19, H20, H21, H22, H26 and H31.**
At each of these hospitals the counsellors are six points or more less likely to approve right after an approval than right after a denial, once each working day is measured against its own determinations in any order; at no other hospital are they. Not holding each counsellor-day fixed, which puts most hospitals over the line because a short working day shows a drop after an approval with no counsellor swayed. Not pooling consecutive determinations, which clears nearly every hospital because days of easier applications string approvals together.

## 2. Critical Components

1. The counsellors' 2025 approvals and denials, by counsellor and local working day: **197,939** determinations across the 31 hospitals
2. Hospitals at six points or more against their own working days' determinations in any order: **11** (H03, H06, H09, H10, H17, H19, H20, H21, H22, H26, H31)
3. FY2027 budget line: **11** grants at **$64,000**, **$704,000**

## 3. Step-by-Step Solution

1. Conformed the three hub extracts by the data guide's codes, put the Columbia extract's UTC times on Pacific time, and kept each hospital's counsellors' 2025 approvals and denials, first and on reconsideration, without pends, withdrawals or the presumptive screening (criteria 2.2): 197,939 determinations.
2. Ordered each counsellor's determinations within each local working day by the recorded time and paired each with the one before it that day (criteria 2.3).
3. For each hospital, pooled over its counsellor-days, took the share approved right after a denial less the share approved right after an approval, and subtracted that contrast's expectation with each working day's determinations in every order and its approvals held (a day with k approvals among n gives k(k-1)/n approval-approval pairs in expectation), which measures the counsellors within their own day's applications (criteria 2.4).
4. Compared each measure with six points unrounded (criteria 2.1 and 2.6): 11 hospitals qualify, H03, H06, H09, H10, H17, H19, H20, H21, H22, H26, H31.
5. Priced the grants at $64,000 each (criteria 1.2): $704,000.
6. For the assistance, took each counsellor-approved 2025 application's write-off once (the adjustments extract carries an approval's whole write-off on every account it covers, which is why a line can exceed its own account's balance in fac_patient_accounts_2025.csv), subtracted the reversals posted through 31 March 2026 and counted the Willamette hub's twice-loaded December 2025 lines once: $402,933.0 thousand in all.
7. For the denials, counted the counsellors' 2025 denials for documents not received, reading code 2 before 1 July 2025 and code 1 from 1 July, when the reason list was renumbered (the denials that reconsiderations reopen carry code 2 to 30 June and code 1 after): 22,683 in all.
8. Recommendation: 11 grants, $704,000.

## 4. Deliverable Answers

### fair_assistance_coaching_2027.xlsx

1. Number of grants: 11, the FY2027 budget line $704,000
2. Whether each hospital qualifies, 31 hospitals in code order:
   - H01 Whitlock Memorial Hospital: No
   - H02 Ostrander Community Hospital: No
   - H03 Brannigan Regional Medical Center: Yes
   - H04 Copperhill Medical Center: No
   - H05 Halvorsen General Hospital: No
   - H06 Delacroix Memorial Hospital: Yes
   - H07 Underhill Community Hospital: No
   - H08 Pettibone Medical Center: No
   - H09 Carmody Memorial Hospital: Yes
   - H10 Kittredge Hospital: Yes
   - H11 Marchbanks Regional Hospital: No
   - H12 Nesbitt Community Hospital: No
   - H13 Beckwith Medical Center: No
   - H14 Jessup Memorial Hospital: No
   - H15 Lindqvist Medical Center: No
   - H16 Vandermeer Hospital: No
   - H17 Thackery Memorial Hospital: Yes
   - H18 Sorensen Regional Medical Center: No
   - H19 Rasmussen Community Hospital: Yes
   - H20 Ingersoll General Hospital: Yes
   - H21 Stromberg Medical Center: Yes
   - H22 Jorgenson Memorial Hospital: Yes
   - H23 Lundgren Regional Hospital: No
   - H24 Bellweather Community Hospital: No
   - H25 Castellan Medical Center: No
   - H26 Dunleavy Memorial Hospital: Yes
   - H27 Mattingly Hospital: No
   - H28 Nygaard Community Hospital: No
   - H29 Petrakis Medical Center: No
   - H30 Sundquist Memorial Hospital: No
   - H31 Wennberg Regional Hospital: Yes
3. Assistance written off on the counsellors' 2025 approvals, net of reversals posted by 31 March 2026, thousands of dollars to one decimal:
   - H01: 10,071.8
   - H02: 11,187.7
   - H03: 13,217.4
   - H04: 19,886.1
   - H05: 17,819.1
   - H06: 10,289.7
   - H07: 7,684.8
   - H08: 4,918.9
   - H09: 22,369.0
   - H10: 21,814.1
   - H11: 9,023.1
   - H12: 19,971.7
   - H13: 17,245.0
   - H14: 8,211.1
   - H15: 13,171.6
   - H16: 16,352.3
   - H17: 8,286.1
   - H18: 11,550.8
   - H19: 7,789.7
   - H20: 20,302.5
   - H21: 13,756.6
   - H22: 19,787.1
   - H23: 11,964.7
   - H24: 9,987.6
   - H25: 16,991.5
   - H26: 13,660.6
   - H27: 6,025.8
   - H28: 6,402.7
   - H29: 8,740.0
   - H30: 15,041.4
   - H31: 9,412.5
4. Counsellor denials in 2025 for documents not received, whole counts:
   - H01: 710
   - H02: 597
   - H03: 591
   - H04: 863
   - H05: 1,079
   - H06: 458
   - H07: 357
   - H08: 322
   - H09: 1,405
   - H10: 1,174
   - H11: 419
   - H12: 1,131
   - H13: 1,025
   - H14: 479
   - H15: 564
   - H16: 922
   - H17: 508
   - H18: 585
   - H19: 589
   - H20: 1,215
   - H21: 816
   - H22: 1,073
   - H23: 633
   - H24: 409
   - H25: 948
   - H26: 733
   - H27: 375
   - H28: 461
   - H29: 401
   - H30: 1,199
   - H31: 642

### fair_assistance_coaching_2027.png

1. Horizontal bar chart of the 31 hospitals' measures against the six-point line, the 11 qualifying hospitals highlighted.
