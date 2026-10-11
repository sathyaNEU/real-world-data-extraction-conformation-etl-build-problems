# solver round: round 1

**Proxy score 94.5 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 52.5 of 58). Main call LANDED. 8 of 10 ask items cracked (80 per cent of tokens).

## Main call

golden: Reissue 387 member cards: every card still open that the Ferrier Creek Travel Plaza pay-at-pump terminal LT723511 in Kemptville read by contact from 5 to 31 August 2026, or the Lombard Market terminal 02417158 in Smiths Falls read by contact from 13 August to 14 September 2026.

solver: Reissue 387 open cards (349 debit, 38 credit) read by contact at two compromised terminals: Ferrier Creek Travel Plaza – Pay at Pump, Kemptville, terminal LT723511 (exposure 5 Aug 2026 to 31 Aug 2026, 174 open cards), and Lombard Market, Smiths Falls, terminal 02417158 (exposure 13 Aug 2026 to 14 Sep 2026, 228 open cards); 15 cards were read at both terminals, and of the 667 distinct cards read in the windows 279 replaced and 1 closed are excluded.

tokens matched 11 of 13 (387, 5, 31, 02417158, 13, 14, Reissue, Ferrier Creek Travel Plaza, Kemptville, August, Lombard Market, Smiths Falls, September)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| card_reissue_request.pdf | 1 | 2 | 2 | 100% |
| card_reissue_request.pdf | 2 | 5 | 6 | 83% |
| card_reissue_request.pdf | 3 | 5 | 7 | 71% |
| card_reissue_request.pdf | 4 | 4 | 4 | 100% |
| card_reissue_request.pdf | 5 | 4 | 4 | 100% |
| card_reissue_request.pdf | 6 | 3 | 3 | 100% |
| card_reissue_request.pdf | 7 | 3 | 3 | 100% |
| common_point_trace.xlsx | 1 | 9 | 14 | 64% |
| common_point_trace.xlsx | 2 | 8 | 8 | 100% |
| common_point_trace.xlsx | 3 | 6 | 7 | 86% |

## Solver's path

1. Reconciled row counts against cudw_job_fraud_weekly_20261005.txt: auths 1,257,657; Cards 16,951; Replacements 1,814; Members 9,840; disputes 1,012; chargebacks 992; merchants 1,316, all matching.
2. fraud_cases xlsx: fraud_type = Counterfeit gives 583 rows, 291 cases, 283 cards and 562 unique retrieval_refs. The 21 duplicate refs are 8 closed-then-reopened claims. txn_date is in Eastern time (verified against auth timestamps converted to America/Toronto).
3. First counterfeit date per card is the minimum txn_date. Lookback is the 60 days before it, D-60 to D-1. The screen span runs 2026-06-25 to 2026-10-01, with 16,487 other cards active in that span.
4. Common-point screen on contact reads (POS entry mode 05/80/90) by merchant_id and terminal_id. LT723511 read 205/283 counterfeit cards vs a 1.87% base rate. Coffee counter LT314033 (95) and car wash LT938930 (47) contain only pump cards. Of the 78 non-pump cards, 47 were read at Lombard 02417158 (16.6% vs 3.62% base), disjoint from the pump cards. The remaining 31 have no common point.
5. Exposure window is the first to last pre-fraud read of a counterfeit card at each terminal: LT723511 2026-08-05 to 2026-08-31 (the terminal was replaced by LT320679 from 2026-09-02, which no counterfeit card touched); 02417158 2026-08-13 to 2026-09-14.
6. Cards read by contact in the window (any response code): 399 at LT723511 and 283 at 02417158, 667 in the union. Joined to card_history Cards status: 387 Open, 279 Replaced, 1 Closed. Every Replaced card appears in the Replacements sheet. The 387 split 349 debit and 38 credit.
7. Losses: 562 unique retrieval_refs joined to the auth parquet (one message each: 540 0200 and 22 0100) using amount_billing_cad, then card_type from Cards. Debit 246,792.17, credit 35,217.25. Members' entered amounts differ on 332 USD rows and were not used.
8. Recovered: chargebacks with reason Counterfeit transaction, all on those refs, summing amount_cad (184 Credited 93,974.64, 6 Pre-arbitration debit -3,798.91). Debit 78,330.45, credit 11,845.28. Net = gross - recovered.
9. MS-3: 283 claims (reopened cases linked by shared retrieval_ref), 240 refunded. Day 0 is the first case_opened converted to Eastern, rolled forward to a business day. Waits are counted in business days excluding the MS-3 holidays (Labour Day 7 Sep). On time means refunded on or before day 0 + 10. Debit 195/215, max 20; credit 21/25, max 16.

confidence: High for the reissue count, terminals, windows and losses. Medium-high for treating Lombard 02417158 as a second compromised terminal (strong but smaller signal than the pump) and for page 3, which depends on linking reopened claims and using Eastern report dates.

notes: Pages 2 and 3 cover all 283 counterfeit cards (the whole wave), of which 31 cards cannot be tied to either terminal. Gross loss includes the 43 claims still open and not yet refunded.

### card_reissue_request.pdf (solver's answers)
- Page 1: number of cards to reissue: 387 cards (349 debit, 38 credit)
- Page 1: compromise point 1 (merchant, town, terminal, first and last read of a later-counterfeit card): Ferrier Creek Travel Plaza – Pay at Pump (merchant 530174549862810), 1845 County Road 43, Kemptville ON, terminal LT723511; first read 5 Aug 2026 (06:28:38 ET), last read 31 Aug 2026 (18:01:13 ET); 205 of 283 counterfeit cards read there; 399 cards read in the window, 174 still open
- Page 1: compromise point 2: Lombard Market (merchant 882084246162166), 210 Lombard St, Smiths Falls ON, terminal 02417158; first read 13 Aug 2026 (07:56:43 ET), last read 14 Sep 2026 (19:25:43 ET); 47 of 283 counterfeit cards read there; 283 cards read in the window, 228 still open
- Page 2: debit losses: Gross CAD 246,792.17; recovered CAD 78,330.45; net CAD 168,461.72 (502 transactions)
- Page 2: credit losses: Gross CAD 35,217.25; recovered CAD 11,845.28; net CAD 23,371.97 (60 transactions)
- Page 2: total (reference): Gross CAD 282,009.42; recovered CAD 90,175.73; net CAD 191,833.69
- Page 3: debit refunds within ten business days and longest wait: 195 of 215 refunded debit claims within 10 business days; longest wait 20 business days
- Page 3: credit refunds within ten business days and longest wait: 21 of 25 refunded credit claims within 10 business days; longest wait 16 business days

### common_point_trace.xlsx (solver's answers)
- Sheet 1 (page 1): cards and terminals: 387 cards to reissue (349 debit, 38 credit). LT723511, Ferrier Creek Pay at Pump, Kemptville, 2026-08-05 to 2026-08-31, 399 read, 174 open; 02417158, Lombard Market, Smiths Falls, 2026-08-13 to 2026-09-14, 283 read, 228 open; union 667 read, 279 replaced, 1 closed. Screen: LT723511 72.4% (205/283) vs base 1.87% (308/16,487); 02417158 16.6% (47/283) vs base 3.62% (597/16,487)
- Sheet 2 (page 2): losses by card type, CAD to the cent: Debit gross 246,792.17, recovered 78,330.45 (80,644.26 credited less 2,313.81 pre-arbitration debits), net 168,461.72; Credit gross 35,217.25, recovered 11,845.28 (13,330.38 less 1,485.10), net 23,371.97
- Sheet 3 (page 3): MS-3 refund record: Debit 195 of 215 refunded claims on time, longest wait 20 business days (FC26-41679/FC26-42768); Credit 21 of 25 on time, longest wait 16 business days (FC26-41711/FC26-42540)

## Where the solver left the ladder (main thread's read, against the three rules)

It did not leave it. The path read every field and applied every stated rule correctly (contact reads 05/80/90, the
60-day lookback, the member base over the screen's span, latest-issue dispute rows by retrieval reference, the billing
amount rather than the dispute-form amount, re-opened claims as one, Eastern business days with the MS-3 holidays) and
then took the decisive analytical step unprompted: "Coffee counter LT314033 (95) and car wash LT938930 (47) contain only
pump cards. Of the 78 non-pump cards, 47 were read at Lombard 02417158 (16.6% vs 3.62% base), disjoint from the pump
cards. The remaining 31 have no common point." Explaining the co-visited sites away by their subset of the pump's
victims and screening the residual is what a careful fraud analyst does on the second pass; the rung was executed as
ordinary practice, not as a work order from any sentence. Landed: 387, both terminals and windows, and every ask figure.
