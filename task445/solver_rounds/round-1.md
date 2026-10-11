# solver round: round 1

**Proxy score 41.0 / 100** (recommendation 5.0 of 35, instruction 7.0 of 7, asks 29.0 of 58). Main call missed. 0 of 3 ask items cracked (80 per cent of tokens).

## Main call

golden: WHII, GLI, OTF, JEMS and SAF carry the crowded flag for the December 2022 quarter; AMRB, TAAV, FENN, ABBB, OLPD, HAMR and NOPR do not.

solver: Flag WHII (Whitby Instruments, 82.8% of 41,820,557 shares) and JEMS (Jessop Medical, 80.1% of 35,906,712 shares, 28,759,064 institutional shares against an 80.0% line at 28,725,370) as crowded for the December 2022 quarter and mark the other ten names (GLI 56.2%, OTF 58.8%, AMRB 72.4%, TAAV 68.0%, FENN 66.5%, ABBB 53.3%, OLPD 56.9%, SAF 65.8%, HAMR 48.6%, NOPR 50.4%) N, measured under OM-4 from the 275 holding managers whose December 13Fs were accepted by 3 Feb 2023.

tokens matched 10 of 10 (WHII, JEMS, December, AMRB, TAAV, FENN, ABBB, OLPD, HAMR, NOPR)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| crowded_flags_2022q4.csv | 1 | 74 | 99 | 75% |
| sep_quarter_bridge.png | 1 | 6 | 8 | 75% |
| sep_quarter_bridge.png | 2 | 0 | 0 | 0% |

## Solver's path

1. Read OM-4, layout, data_sources, readme; rules: SH no put/call, report as amended, CUSIP repair, latest dei count on or before period end, above 80.0%, whole dollars, per CIK.
2. Joined SUBMISSION/COVERPAGE/INFOTABLE across q3, q4 and daily build; September = q4 set plus 4 daily-build September filings; December = 282 HR in daily build.
3. Normalised CUSIPs; one check-digit failure 805185108 mapped to FENN.
4. September holdings 557,031,720 across 359 managers.
5. December holdings 470,654,945 across 275 managers (as filed by 3 Feb).
6. Shares outstanding from fsds, latest on or before period end; flag above 80.0%: WHII, JEMS.
7. Top holder per CIK in whole dollars; Wexley December values scaled x1000 (reported in thousands).
8. Bridge 568,922,286 to 557,031,720.

confidence: Medium-high; medium on JEMS; noted 91 September holders not yet filed.

notes: December understated because filings run to 3 Feb with deadline 14 Feb; GLI, SAF, FENN N mainly because filings are missing. Alternative bridge start 544,752,819 if SEC data set only.

### crowded_flags_2022q4.csv (solver's answers)
- WHII row: shares_outstanding 41,820,557; inst_own_pct 82.8%; crowded Y; prior_shares_outstanding 42,344,280; prior_inst_own_pct 86.3%; top holder PRESCOTT FUNDS GROUP INC (CIK 1093660) $275,146,453
- GLI row: shares_outstanding 63,104,219; inst_own_pct 56.2%; crowded N; prior_shares_outstanding 63,493,998; prior_inst_own_pct 83.2%; top holder WEXLEY TRUST WEALTH ADVISORS LLC (CIK 1266847) $288,595,000
- OTF row: shares_outstanding 28,559,804; inst_own_pct 58.8%; crowded N; prior_shares_outstanding 28,787,265; prior_inst_own_pct 78.7%; top holder PRESCOTT FUNDS GROUP INC (CIK 1093660) $298,144,931
- AMRB row: shares_outstanding 117,402,633; inst_own_pct 72.4%; crowded N; prior_shares_outstanding 119,104,904; prior_inst_own_pct 74.8%; top holder TREGARON NATIONAL BANK WEALTH MANAGEMENT (CIK 1560568) $312,917,973
- TAAV row: shares_outstanding 52,271,090; inst_own_pct 68.0%; crowded N; prior_shares_outstanding 52,586,203; prior_inst_own_pct 76.9%; top holder PRESCOTT FUNDS GROUP INC (CIK 1093660) $262,641,467
- JEMS row: shares_outstanding 35,906,712; inst_own_pct 80.1%; crowded Y; prior_shares_outstanding 36,555,036; prior_inst_own_pct 82.7%; top holder PRESCOTT FUNDS GROUP INC (CIK 1093660) $482,244,430
- FENN row: shares_outstanding 88,013,465; inst_own_pct 66.5%; crowded N; prior_shares_outstanding 89,139,533; prior_inst_own_pct 81.6%; top holder PRESCOTT FUNDS GROUP INC (CIK 1093660) $260,134,599
- ABBB row: shares_outstanding 74,660,128; inst_own_pct 53.3%; crowded N; prior_shares_outstanding 78,896,891; prior_inst_own_pct 61.1%; top holder WEXLEY TRUST WEALTH ADVISORS LLC (CIK 1266847) $438,038,000
- OLPD row: shares_outstanding 23,177,946; inst_own_pct 56.9%; crowded N; prior_shares_outstanding 23,252,212; prior_inst_own_pct 70.1%; top holder TREGARON NATIONAL BANK WEALTH MANAGEMENT (CIK 1560568) $238,979,219
- SAF row: shares_outstanding 46,318,551; inst_own_pct 65.8%; crowded N; prior_shares_outstanding 46,406,184; prior_inst_own_pct 89.9%; top holder PRESCOTT FUNDS GROUP INC (CIK 1093660) $270,339,439
- HAMR row: shares_outstanding 158,244,370; inst_own_pct 48.6%; crowded N; prior_shares_outstanding 159,228,320; prior_inst_own_pct 53.8%; top holder WEXLEY TRUST WEALTH ADVISORS LLC (CIK 1266847) $348,507,000
- NOPR row: shares_outstanding 31,052,683; inst_own_pct 50.4%; crowded N; prior_shares_outstanding 31,369,971; prior_inst_own_pct 66.2%; top holder PRESCOTT FUNDS GROUP INC (CIK 1093660) $149,577,226
- crowded names: 2 of 12 flagged Y: WHII, JEMS

### sep_quarter_bridge.png (solver's answers)
- starting bar: straight sum of September-quarter (30 Sep 2022 period) lines with an exact watchlist CUSIP: 568,922,286 shares (2,434 lines)
- put/call lines removed: -5,183,600 shares (43 lines)
- superseded original removed (Selwood Savings Bank Trust Dept, restatement filed 2 Dec 2022): -16,011,685 shares (13 lines)
- leading zeros restored: +5,846,688 shares (52 lines)
- lower-case CUSIP 359y60106 corrected: +2,993,879 shares (13 lines)
- bad check digit 805185108 matched to Fenwick by name and class: +464,152 shares (1 line)
- ending bar: September institutional shares, 12 names combined: 557,031,720 shares
