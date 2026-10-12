# solver round: round 2

**Proxy score 45.1 / 100** (recommendation 5.0 of 35, instruction 7.0 of 7, asks 33.1 of 58). Main call missed. 1 of 3 ask items cracked (80 per cent of tokens).

## Main call

golden: WHII, GLI, OTF, JEMS and SAF carry the crowded flag for the December 2022 quarter; AMRB, TAAV, FENN, ABBB, OLPD, HAMR and NOPR do not.

solver: Send crowded = Y for WHII (88.4%), GLI (83.6%), JEMS (84.7%) and SAF (90.6%) and N for the other eight (OTF 79.2%, AMRB 76.0%, TAAV 74.0%, FENN 79.6%, ABBB 62.1%, OLPD 70.8%, HAMR 55.0%, NOPR 67.0%), with December ownership estimated under OM-4 section 2: the 129 managers that filed for September and have no December report or notice by 3 Feb have their September holdings carried forward, because that method, tested on September with filings to 3 Nov, missed by at most 1.144 points against 2.894 for scaling and 26.48 for counting filed reports only.

tokens matched 10 of 10 (WHII, JEMS, December, AMRB, TAAV, FENN, ABBB, OLPD, HAMR, NOPR)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| crowded_flags_2022q4.csv | 1 | 95 | 99 | 96% |
| sep_quarter_bridge.png | 1 | 6 | 8 | 75% |
| sep_quarter_bridge.png | 2 | 0 | 0 | 0% |

## Solver's path

1. Read OM-4 etc.
2. Share counts latest cover count on or before period end; September uses 10-Q/A for HAMR, OLPD, TAAV
3. Holdings per OM-4: restatements replace (Thackeray, Selwood Savings); NEW HOLDINGS adds; put/call out incl. title-only; CUSIP repair; Wexley x1000
4. September ownership on all reports: 545,842,563 total
5. Back-test at 34 days: carry 1.144, scaled 2.894, on-file 26.48 -> carry
6. December: 272 filed + carried 129: WHII 88.42, GLI 83.62, OTF 79.18, FENN 79.56, SAF 90.59, JEMS 84.69 -> WHII, GLI, JEMS, SAF
7. Top holder among filed December reports, December cover-page names
8. Bridge 575,953,719 to 545,842,563

confidence: Medium-high

notes: Top holder among filed reports; Prescott renamed in December.

### crowded_flags_2022q4.csv (solver's answers)
- WHII 649698107: December: shares outstanding 41,820,557, institutional ownership 88.4%, crowded Y; September: shares outstanding 42,410,227, ownership 85.1%; largest holder CIK 1093660 PRESCOTT GLOBAL INDEXING INC, $288,777,102
- GLI 759069107: December: shares outstanding 63,104,219, institutional ownership 83.6%, crowded Y; September: shares outstanding 63,621,674, ownership 81.7%; largest holder CIK 1266847 WEXLEY TRUST WEALTH ADVISORS LLC, $297,586,000
- OTF 050469105: December: shares outstanding 28,559,804, institutional ownership 79.2%, crowded N; September: shares outstanding 28,748,299, ownership 78.8%; largest holder CIK 1093660 PRESCOTT GLOBAL INDEXING INC, $315,756,543
- AMRB 091728105: December: shares outstanding 117,402,633, institutional ownership 76.0%, crowded N; September: shares outstanding 119,140,192, ownership 74.1%; largest holder CIK 1560568 TREGARON NATIONAL BANK WEALTH MANAGEMENT, $314,448,044
- TAAV 981118102: December: shares outstanding 52,271,090, institutional ownership 74.0%, crowded N; September: shares outstanding 52,584,717, ownership 75.4%; largest holder CIK 1093660 PRESCOTT GLOBAL INDEXING INC, $276,601,483
- JEMS 165636101: December: shares outstanding 35,906,712, institutional ownership 84.7%, crowded Y; September: shares outstanding 36,359,137, ownership 81.8%; largest holder CIK 1093660 PRESCOTT GLOBAL INDEXING INC, $506,963,024
- FENN 805185105: December: shares outstanding 88,013,465, institutional ownership 79.6%, crowded N; September: shares outstanding 89,236,852, ownership 81.6%; largest holder CIK 1093660 PRESCOTT GLOBAL INDEXING INC, $263,252,333
- ABBB 767361108: December: shares outstanding 74,660,128, institutional ownership 62.1%, crowded N; September: shares outstanding 78,896,891, ownership 59.8%; largest holder CIK 1266847 WEXLEY TRUST WEALTH ADVISORS LLC, $434,533,000
- OLPD 016363103: December: shares outstanding 23,177,946, institutional ownership 70.8%, crowded N; September: shares outstanding 23,312,378, ownership 69.7%; largest holder CIK 1560568 TREGARON NATIONAL BANK WEALTH MANAGEMENT, $237,806,067
- SAF 331222109: December: shares outstanding 46,318,551, institutional ownership 90.6%, crowded Y; September: shares outstanding 47,198,603, ownership 88.9%; largest holder CIK 1093660 PRESCOTT GLOBAL INDEXING INC, $292,983,141
- HAMR 233712108: December: shares outstanding 158,244,370, institutional ownership 55.0%, crowded N; September: shares outstanding 159,842,638, ownership 49.1%; largest holder CIK 1266847 WEXLEY TRUST WEALTH ADVISORS LLC, $350,739,000
- NOPR 359Y60106: December: shares outstanding 31,052,683, institutional ownership 67.0%, crowded N; September: shares outstanding 31,720,316, ownership 65.5%; largest holder CIK 1093660 PRESCOTT GLOBAL INDEXING INC, $150,054,802

### sep_quarter_bridge.png (solver's answers)
- start: straight sum of September-quarter lines with a watchlist CUSIP as written: 575,953,719 shares
- reconciling item: superseded original reports: -25,339,912 shares (21 lines in Thackeray 0001567619-22-001105 and Selwood Savings 0000950123-22-001003, both replaced by restatements)
- reconciling item: put/call lines: -7,280,100 shares (48 lines, of which 2,096,500 are title-only PUT/CALL lines)
- reconciling item: CUSIPs restored to nine characters / upper case: +948,452 shares (4 lines)
- reconciling item: check-digit failures matched on issuer name: +1,560,404 shares (8 lines)
- end: our September institutional shares, 12 names combined: 545,842,563 shares
