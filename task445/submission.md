# task445 submission

## Tags

**Domain:** Quantitative Finance (institutional ownership analytics from Form 13F holdings filings).  
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**WHII, GLI, OTF, JEMS and SAF carry the crowded flag for the December 2022 quarter; AMRB, TAAV, FENN, ABBB, OLPD, HAMR and NOPR do not.**

OTF clears the line and FENN does not. Not the December reports in hand alone, which leave out the managers OM-4 s.2 still counts. Not each manager still due carried at its September position, which misses the index and ETF sponsors' growth and drops OTF. Not one rate for every manager still due, which grows the multi-strategy funds too and adds FENN. Not September's flags, which miss OTF's rise and FENN's fall.

## 2. Critical Components

1. Managers with a September holdings or combination report and no December filing by 3 February 2023: **129**
2. Change in twelve-name share holdings, September to December, among managers that filed both reports: index and ETF sponsors **5.5%**, every other register type flat to the first decimal
3. December ownership of the flagged names: WHII **88.6%**, GLI **84.4%**, OTF **80.4%**, JEMS **84.8%**, SAF **91.4%**
4. Highest unflagged December ownership: FENN **79.6%**, AMRB **76.2%**

## 3. Step-by-Step Solution

1. Unioned SUBMISSION, COVERPAGE and INFOTABLE from the three 13F drops, keyed every report to the period on its cover page (REPORTCALENDARORQUARTER) and applied amendments by their cover page (ISAMENDMENT, AMENDMENTTYPE) in filing order, amendments filed on the same day in AMENDMENTNO order.
2. Kept SH lines, dropped put and call lines by PUTCALL or a title of class of CALL or PUT, read CUSIPs per OM-4 s.4 (failed check digits matched on issuer name and title), and put VALUE in dollars, including the December report whose cover page states thousands.
3. Took shares outstanding as the cover-page count with the latest as-of date on or before each period end across 10-Q, 10-Q/A and 10-K (OM-4 s.5).
4. Applied OM-4 s.2: the managers reporting December holdings are those on file plus the 129 with a September holdings or combination report and no December filing; their holdings are estimated.
5. Ran the s.2 criterion on the September window at 3 November 2022, completing from June: growing each manager still due by its register type's change among managers that filed both reports misses September by at most 0.04 points, against 1.14 for carrying each at its June position and 0.89 for one rate for all.
6. Grew each manager still due from its September position by its type's change (index and ETF sponsors 5.5%, other types flat), added the December reports on file and divided by the October-dated count; flag above 80.0% (OM-4 s.7).
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
   - HAMR (233712108): December ownership 55.2%, flag N; September ownership 49.1%
   - NOPR (359Y60106): December ownership 67.2%, flag N; September ownership 65.5%

### sep_quarter_bridge.png

1. Waterfall, twelve names combined, whole shares: information-table lines as filed 598,531,990; put and call lines -8,203,900; lines in reports replaced by a later amendment -50,938,469; CUSIPs keyed off-format, matched back +6,452,942; September institutional shares 545,842,563
2. Title: our September institutional shares sit 52.7 million shares below the straight sum of the SEC lines
3. One bar for each reconciling item between the two totals, each labelled in whole shares.
