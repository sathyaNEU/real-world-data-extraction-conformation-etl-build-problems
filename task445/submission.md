# task445 submission

## Tags

**Domain:** Quantitative Finance (institutional ownership analytics from Form 13F holdings filings).  
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**WHII, GLI, OTF, JEMS and SAF carry the crowded flag for the December 2022 quarter; AMRB, TAAV, FENN, ABBB, OLPD, HAMR and NOPR do not.**

OTF clears the 80.0% line at 80.4% and FENN stays under it at 79.6%. Not the December reports in hand alone, which leave out the 129 managers OM-4 s.2 still counts. Not one change per register type pooled across the twelve names, which grows OTF's index and ETF sponsors still due by 4.5% when the filed sponsors' OTF holdings rose 10.4% with OTF's share count, and leaves OTF at 79.2%. Not each manager still due carried at its September position, which also leaves OTF under the line. Not every manager still due moved with the name or carried at its stake, which takes FENN's multi-strategy funds up with FENN's share count and FENN over the line.

## 2. Critical Components

1. Managers with a September holdings or combination report and no December filing by 3 February 2023: **129**
2. Index and ETF sponsors that filed both reports, change in OTF shares from September to December: **10.4%**, against **4.5%** across the twelve names
3. December ownership of the flagged names: WHII **88.6%**, GLI **84.4%**, OTF **80.4%**, JEMS **84.8%**, SAF **91.4%**
4. Highest unflagged December ownership: FENN **79.6%**, AMRB **76.2%**

## 3. Step-by-Step Solution

1. Unioned SUBMISSION, COVERPAGE and INFOTABLE from the three 13F drops, keyed every report to the period on its cover page (REPORTCALENDARORQUARTER) and applied amendments by their cover page (ISAMENDMENT, AMENDMENTTYPE) in filing order, amendments filed on the same day in AMENDMENTNO order.
2. Kept SH lines, dropped put and call lines by PUTCALL or a title of class of CALL or PUT, and read CUSIPs per OM-4 s.4 (failed check digits matched on issuer name and title).
3. Took shares outstanding as the cover-page count with the latest as-of date on or before each period end across 10-Q, 10-Q/A and 10-K (OM-4 s.5).
4. Applied OM-4 s.2: the managers reporting December holdings are those on file plus the 129 with a September holdings or combination report and no December filing, whose holdings are estimated.
5. Ran the s.2 criterion on the September window at 3 November 2022, completing from June: the largest miss against September is 0.04 points for growing each index and ETF sponsor still due by the change its filed peers show in that name, every other type by its own change pooled across the twelve names, against 0.66 for each register type's change pooled across the twelve names and 1.38 for carrying each manager still due at its June position.
6. Grew each index and ETF sponsor still due from its September position by the change in that name among the sponsors that filed both reports (OTF 10.4%), every other type by its own pooled change (flat to the first decimal), added the December reports on file and divided by the October-dated count; flag above 80.0% (OM-4 s.7).
7. Recommendation: flag WHII, GLI, OTF, JEMS and SAF.

## 4. Deliverable Answers

### crowded_flags_2022q4.csv

1. One row per watchlist name in watchlist order, layout v4, report period 2022-12-31:
   - WHII (649698107): December ownership 88.6%, flag Y; September ownership 85.1%
   - GLI (759069107): December ownership 84.4%, flag Y; September ownership 81.7%
   - OTF (050469105): December ownership 80.4%, flag Y; September ownership 78.8%
   - AMRB (091728105): December ownership 76.2%, flag N; September ownership 74.1%
   - TAAV (981118102): December ownership 74.3%, flag N; September ownership 75.4%
   - JEMS (165636101): December ownership 84.8%, flag Y; September ownership 81.8%
   - FENN (805185105): December ownership 79.6%, flag N; September ownership 81.6%
   - ABBB (767361108): December ownership 62.3%, flag N; September ownership 59.8%
   - OLPD (016363103): December ownership 71.1%, flag N; September ownership 69.7%
   - SAF (331222109): December ownership 91.4%, flag Y; September ownership 88.9%
   - HAMR (233712108): December ownership 55.2%, flag N; September ownership 52.5%
   - NOPR (359Y60106): December ownership 67.2%, flag N; September ownership 65.5%

### sep_quarter_bridge.png

1. Waterfall, twelve names combined, whole shares: information-table lines as filed 599,363,366; put and call lines -8,193,500; the other lines in reports replaced by a later amendment -50,329,359; lines matched back to their CUSIPs +6,508,236; September institutional shares 547,348,743
2. One bar each, in that order, for the three reconciling items between the two totals, each labelled in whole shares.
