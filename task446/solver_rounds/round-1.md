# solver round: round 1

**Proxy score 93.4 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 51.4 of 58). Main call LANDED. 3 of 3 ask items cracked (80 per cent of tokens).

## Main call

golden: Credit committee should approve GBP 21.8m of Kelderby Facilities Ltd's GBP 30.0m term loan.

solver: Credit Committee can approve £21.8m (in £0.1m multiples) of Kelderby Facilities Ltd's £30.0m term loan on 4 November 2026, because Kelderby Group plc (ultimate parent LEI 2138C0A0BNVDI9Z01R67, grouped as at 30 Sep 2026 including Tarrant Hydraulics and excluding Norbeck Coatings) has a projected 31 Dec 2026 exposure of £148.1m (30 Sep 2026 £146.4m plus a least-squares slope of £1.7m per quarter) against a £170.0m house limit, 87.1% utilisation, leaving £21.88m of room.

tokens matched 3 of 4 (21.8, 30.0, Credit, Kelderby Facilities Ltd's GBP)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| limit_check_2026-11-04.xlsx | 1 | 3 | 3 | 100% |
| limit_check_2026-11-04.xlsx | 2 | 102 | 126 | 81% |
| projected_utilisation_2026Q4.png | 1 | 17 | 20 | 85% |

## Solver's path

1. Read agenda, policy v4.2, LMS-03 v2.0; projection date 30 Sep 2026
2. Group map from 2026-09-30 GLEIF archive (successors, branches, ultimate then direct parent, lapsed kept, funds ignored, exceptions head themselves)
3. Applied the 30 Sep 2026 membership to all five quarter-ends (LMS 2.3): Tarrant in Kelderby throughout, Norbeck in Meridale, Corrin Cold Chain out
4. Loans incl. late CWB-DUB file; migrated facility source removed; drawn 100%, undrawn 50%, overdraft nil; FX divided by rate per GBP
5. Securities at carrying value with ISIN-LEI fill
6. Derivatives from R2 rerun, GBP thousands x1000, positive MTM less cash collateral
7. Kelderby quarter-ends 139.40, 141.53, 140.36, 144.51, 146.42; slope 1.702; projected 148.12
8. Room 21.88, rounded down to 21.8

confidence: Medium-high

notes: Meridale Packaging twin loans kept separate; R2 rerun changes only Stannard derivatives.

### limit_check_2026-11-04.xlsx (solver's answers)
- Headline Kelderby approvable amount: B1 Kelderby term loan: approvable £21.8m of £30.0m requested
- Row order: B4 Corrin 90.7%; B5 Pellow 87.6%; B1 Kelderby 87.1%; B2 Meridale 86.7%; B3 Brauneck 83.7%; B6 Stannard 71.6%
- B4 Corrin Logistics Group plc (limit £90.0m): 30 Sep 2026 drawn £73.5m, undrawn (50%) £8.0m, securities £0.0m, derivatives £1.5m; quarter-end exposures £88.1m, £87.4m, £86.0m, £83.2m, £83.1m; projected £81.6m; utilisation 90.7%; approvable £16.7m of £25.0m RCF
- B5 Pellow Foods Group plc (limit £85.0m): 30 Sep 2026 drawn £59.6m, undrawn £5.7m, securities £9.8m, derivatives £0.0m; quarter-ends £77.4m, £77.3m, £74.7m, £75.5m, £75.1m; projected £74.4m; utilisation 87.6%; approvable £10.5m of £14.0m
- B1 Kelderby Group plc (limit £170.0m): 30 Sep 2026 drawn £128.2m, undrawn £18.2m, securities £0.0m, derivatives £0.0m; quarter-ends £139.4m, £141.5m, £140.4m, £144.5m, £146.4m; projected £148.1m; utilisation 87.1%; approvable £21.8m of £30.0m
- B2 Meridale Holdings Ltd (limit £85.0m): 30 Sep 2026 drawn £68.3m, undrawn £6.3m, securities £0.0m, derivatives £0.0m; quarter-ends £78.0m, £77.6m, £75.3m, £75.4m, £74.6m; projected £73.7m; utilisation 86.7%; approvable £11.2m of £12.0m
- B3 Brauneck Holding SE (limit £100.0m): 30 Sep 2026 drawn £78.5m, undrawn £4.6m, securities £0.0m, derivatives £0.0m; quarter-ends £80.2m, £81.3m, £79.2m, £81.5m, £83.1m; projected £83.7m; utilisation 83.7%; approvable £16.2m of £20.0m
- B6 Stannard Capital Group plc (limit £30.0m): 30 Sep 2026 drawn £17.4m, undrawn £2.8m, securities £0.0m, derivatives £1.3m; quarter-ends £21.6m, £21.0m, £20.5m, £21.0m, £21.5m; projected £21.5m; utilisation 71.6%; approvable £17.0m of £20.0m RCF

### projected_utilisation_2026Q4.png (solver's answers)
- Bars: Corrin 90.7%, Pellow 87.6%, Kelderby 87.1%, Meridale 86.7%, Brauneck 83.7%, Stannard 71.6%
- Limit line: 100% house limit line, labelled 100%
- Kelderby bar annotation: Approvable £21.8m of £30.0m (projected £148.1m vs £170.0m limit)
- Title: Kelderby can be approved for £21.8m of its £30.0m term loan
