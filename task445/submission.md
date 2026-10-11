# task445 submission

## Tags

**Domain:** Quantitative Finance (institutional ownership analytics from Form 13F holdings filings).  
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**WHII, GLI, OTF, JEMS and SAF carry the crowded flag for the December 2022 quarter; AMRB, TAAV, FENN, ABBB, OLPD, HAMR and NOPR do not.**

The closest calls are OTF at 83.4% and FENN at 77.3%. Not the reports in hand alone, which flag only WHII and JEMS because 125 managers that filed for September had not yet filed for December. Not one aggregate completion share, which flags AMRB, TAAV and FENN and misses GLI and OTF because the managers still to file sit in some registers far more than others. Not September's flags, which miss OTF's rise and FENN's fall.

## 2. Critical Components

1. Managers with a September holdings or combination report and no December report by 3 February 2023: **125**
2. December ownership of the flagged names: WHII **88.6%**, GLI **84.4%**, OTF **83.4%**, JEMS **84.8%**, SAF **91.4%**
3. Highest unflagged December ownership: FENN **77.3%**, AMRB **76.2%**

## 3. Step-by-Step Solution

1. Unioned SUBMISSION, COVERPAGE and INFOTABLE from the three 13F drops and keyed every report to its REPORTCALENDARORQUARTER, applying amendments in filing order as the readme defines them (RESTATEMENT replaces, NEW HOLDINGS adds).
2. Kept SH lines with no put or call, read CUSIPs to nine upper-case characters with leading zeros restored, matched the one failed check digit on issuer name and title, and put VALUE on a dollar basis, including the one December filing still in thousands (OM-4 s.3, s.4, s.6).
3. Took shares outstanding as the latest cover-page count dated on or before each period end from fsds_cover_extract (OM-4 s.5).
4. Found 125 managers with a September report and no December report by 3 February, inside the 45-day window, and carried each at its September share position.
5. Back-tested the completion on the September window at the same day, completing from June: the holder-level carry misses every name by at most 2.6 points, one aggregate completion share by up to 22.3.
6. December ownership is December shares on file plus carried shares over the October-dated count; the flag is ownership above 80.0% (OM-4 s.7).
7. Recommendation: flag WHII, GLI, OTF, JEMS and SAF.

## 4. Deliverable Answers

### crowded_flags_2022q4.csv

1. One row per watchlist name in watchlist order, report period 2022-12-31:
   - WHII (649698107): December shares outstanding 41,820,557, ownership 88.6%, flag Y; September shares outstanding 42,344,280, ownership 86.3%; largest holder PRESCOTT FUNDS GROUP INC (CIK 1093660), $275,146,453
   - GLI (759069107): December shares outstanding 63,104,219, ownership 84.4%, flag Y; September shares outstanding 63,493,998, ownership 83.2%; largest holder WEXLEY TRUST WEALTH ADVISORS LLC (CIK 1266847), $288,595,000
   - OTF (050469105): December shares outstanding 28,559,804, ownership 83.4%, flag Y; September shares outstanding 28,787,265, ownership 78.7%; largest holder PRESCOTT FUNDS GROUP INC (CIK 1093660), $298,144,931
   - AMRB (091728105): December shares outstanding 117,402,633, ownership 76.2%, flag N; September shares outstanding 119,104,904, ownership 74.8%; largest holder TREGARON NATIONAL BANK WEALTH MANAGEMENT (CIK 1560568), $312,917,973
   - TAAV (981118102): December shares outstanding 52,271,090, ownership 74.3%, flag N; September shares outstanding 52,586,203, ownership 76.9%; largest holder PRESCOTT FUNDS GROUP INC (CIK 1093660), $262,641,467
   - JEMS (165636101): December shares outstanding 35,906,712, ownership 84.8%, flag Y; September shares outstanding 36,555,036, ownership 82.7%; largest holder PRESCOTT FUNDS GROUP INC (CIK 1093660), $482,244,430
   - FENN (805185105): December shares outstanding 88,013,465, ownership 77.3%, flag N; September shares outstanding 89,139,533, ownership 81.6%; largest holder PRESCOTT FUNDS GROUP INC (CIK 1093660), $260,134,599
   - ABBB (767361108): December shares outstanding 74,660,128, ownership 62.3%, flag N; September shares outstanding 78,896,891, ownership 61.1%; largest holder WEXLEY TRUST WEALTH ADVISORS LLC (CIK 1266847), $438,038,000
   - OLPD (016363103): December shares outstanding 23,177,946, ownership 71.1%, flag N; September shares outstanding 23,252,212, ownership 70.1%; largest holder TREGARON NATIONAL BANK WEALTH MANAGEMENT (CIK 1560568), $238,979,219
   - SAF (331222109): December shares outstanding 46,318,551, ownership 91.4%, flag Y; September shares outstanding 46,406,184, ownership 89.9%; largest holder PRESCOTT FUNDS GROUP INC (CIK 1093660), $270,339,439
   - HAMR (233712108): December shares outstanding 158,244,370, ownership 55.2%, flag N; September shares outstanding 159,228,320, ownership 53.8%; largest holder WEXLEY TRUST WEALTH ADVISORS LLC (CIK 1266847), $348,507,000
   - NOPR (359Y60106): December shares outstanding 31,052,683, ownership 67.2%, flag N; September shares outstanding 31,369,971, ownership 66.2%; largest holder PRESCOTT FUNDS GROUP INC (CIK 1093660), $149,577,226

### sep_quarter_bridge.png

1. Waterfall, twelve names combined, whole shares: information-table lines as filed 568,922,286; put and call lines -5,183,600; lines in reports superseded by a restatement -16,011,685; lines keyed under a malformed CUSIP +9,304,719; September institutional shares 557,031,720
2. One bar per reconciling item between the two totals, each labelled in whole shares.
