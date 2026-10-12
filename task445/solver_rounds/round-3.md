# solver round: round 3

**Proxy score 52.3 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 10.3 of 58). Main call LANDED. 0 of 4 ask items cracked (80 per cent of tokens). Ask share kept 18%. Gate: LANDED.

## Main call

golden: WHII, GLI, OTF, JEMS and SAF carry the crowded flag for the December 2022 quarter; AMRB, TAAV, FENN, ABBB, OLPD, HAMR and NOPR do not.

solver: Flag WHII (Whitby, 649698107) at 88.6%, GLI (Glenrock, 759069107) at 84.4%, OTF (Otterburn, 050469105) at 80.4%, JEMS (Jessop, 165636101) at 84.8% and SAF (Sandford, 331222109) at 91.4% as crowded for 2022-12-31, and leave AMRB 76.2%, TAAV 74.3%, FENN 79.6%, ABBB 62.3%, OLPD 71.1%, HAMR 55.2% and NOPR 67.2% unflagged. December ownership is estimated for the 129 September filers not yet filed by 3 Feb 2023, by scaling their September holdings by the in-hand change pooled by manager type, the basis that won the 34-day September backtest with a 0.042 pp maximum error; OTF clears 80.0% only on this basis (79.2% on carry-forward).

tokens matched 10 of 10 (WHII, JEMS, December, AMRB, TAAV, FENN, ABBB, OLPD, HAMR, NOPR)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| crowded_flags_2022q4.csv | 1 | 34 | 48 | 71% |
| sep_quarter_bridge.png | 1 | 0 | 8 | 0% |
| sep_quarter_bridge.png | 2 | 0 | 3 | 0% |
| sep_quarter_bridge.png | 3 | 0 | 0 | 0% |

## Solver's path

1. Loaded SUBMISSION/COVERPAGE/INFOTABLE; quarter from SUBMISSION.PERIODOFREPORT; 0000950123-22-001007 treated as a June restatement
2. Amendments by AMENDMENTNO
3. SH only; options by PUTCALL or title; CUSIP repairs
4. Share counts latest as-of on or before period end
5. September ownership 549,916,383 shares
6. Back-test at 34 days: none 26.5, carry 1.14, per-security 3.16, pooled 0.60, type-pooled 0.042
7. Type-pooled ratio applied to December: WHII, GLI, OTF, JEMS, SAF
8. Bridge 586,016,591 to 549,916,383

confidence: Medium-high

notes: Candidate bases not listed in OM-4.

### crowded_flags_2022q4.csv (solver's answers)
- v4 rows in watchlist order (report_period 2022-12-31; inst_own_pct, crowded, prior_inst_own_pct): WHII 649698107: 88.6%, Y, prior 85.8%; GLI 759069107: 84.4%, Y, prior 82.2%; OTF 050469105: 80.4%, Y, prior 79.3%; AMRB 091728105: 76.2%, N, prior 74.7%; TAAV 981118102: 74.3%, N, prior 75.9%; JEMS 165636101: 84.8%, Y, prior 82.3%; FENN 805185105: 79.6%, N, prior 82.2%; ABBB 767361108: 62.3%, N, prior 60.3%; OLPD 016363103: 71.1%, N, prior 70.1%; SAF 331222109: 91.4%, Y, prior 89.2%; HAMR 233712108: 55.2%, N, prior 49.5%; NOPR 359Y60106: 67.2%, N, prior 66.1% (all percentages to one decimal place)
- count of crowded names: 5 of 12 flagged Y: WHII, GLI, OTF, JEMS, SAF

### sep_quarter_bridge.png (solver's answers)
- starting total: 586,016,591 shares
- bar: superseded: -31,141,964 shares
- bar: put and call: -7,467,100 shares
- bar: CUSIP format repairs: +948,452 shares
- bar: check-digit name matches: +1,560,404 shares
- ending total: 549,916,383 shares
