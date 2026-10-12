## Tags

**Domain:** Banking, Credit & Financial Risk (deposit liquidity behaviour: term deposit retention at maturity).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**We should book 5,500 agent-hours with Harbourline for the 18,400 term deposits on the January to March 2027 maturity list: 1,500 for the deposits maturing in January, 2,000 for February and 2,000 for March.**
About 62 per cent of the list's expected 14,000 conversations will go to the 22-minute retention offer, against 33 per cent across the seven closed campaigns, because 10,735 of the deposits are four-year deposits at 5.65 per cent reinvesting at the 3.15 per cent four-year card, a drop of 2.50 points. Not the past share of conversations that went to the retention offer, whether pooled, from the latest campaign or by term: it was measured on holders who met smaller drops, since the four-year deposits called so far had been opened at lower rates. Not the past share for deposits at the same locked rate, which was also measured on smaller drops.

## 2. Critical Components

1. **460** of the 18,400 listed deposits have no callable number once the holders' numbers are washed against the do-not-call register at the cut, and are not released.
2. **10,735** deposits on the list are four-year deposits at **5.65 per cent** that reinvest at the **3.15 per cent** four-year card for January to March 2027, a drop of **2.50 points**; in the seven closed campaigns **92 per cent** of conversations at drops of 2.5 points or more went to the retention offer.
3. About **62 per cent** of the list's expected **14,000** conversations go to the retention offer, against **33 per cent** of the seven campaigns' conversations.

## 3. Step-by-Step Solution

1. Normalised the numbers in kbs_contact_points_2026-11-02.csv to E.164 and dropped those on kbs_do_not_call_register_2026-11-02.csv as it stood on 2 November 2026 (recorded by then and not withdrawn by then): 460 of the 18,400 deposits on kbs_td_retention_list_2027Q1.csv have no callable number and, per the retention procedure, are not released.
2. Joined kbs_case_release_log_2025q1-2026q3.csv to harbourline_case_closeouts_2025q1-2026q3.csv and harbourline_dial_log_2025q1-2026q3.csv for every released case of the seven closed campaigns, averaged the dials that did not reach the holder (NOA, BSY, VML, DIS, WNG) and the chance of a conversation by the mix of the case's callable number types (how many mobile, home and work numbers), applied them to the list's mixes, and scaled them by the 95.5 per cent of listed deposits with a callable number that the seven campaigns released (the rest had given instructions): about 67,400 non-reaching dials and 14,000 conversations.
3. Took each past conversation's drop, the rate on its deposit's row in kbs_td_retention_lists_2025.csv or kbs_td_retention_lists_2026.csv less the reinvestment rate for its term in the quarter's campaign brief PDF: the share that went to the retention offer (RTK, RTW) rises with the drop in every campaign and every term, reaching 92 per cent at drops of 2.5 points or more, against 33 per cent overall.
4. Read each listed deposit's drop against the rates in harbourline_campaign_brief_2027Q1.pdf (four years 3.15 per cent) and gave it the past share of conversations in its 0.25-point band of drop: 10,735 deposits at 5.65 per cent meet a drop of 2.50 points, and about 62 per cent of the 14,000 conversations go to the retention offer.
5. Priced the list at schedule 2 of harbourline_sow_HCS-KBS-2025-01.pdf, 1.5 minutes per dial that does not reach the holder, 8 per conversation and 22 per retention-offer conversation: 5,568.0 agent-hours, 1,479.5 for January maturities, 2,044.1 for February and 2,044.4 for March.
6. Counted each listed deposit of the seven campaigns (account numbers without punctuation) as still on term deposit when kbs_td_account_events_2025-01_2026-10.csv shows a REINVEST on its own account on its maturity date, or kbs_member_transfers_2025-01_2026-10.csv shows any of its maturity proceeds paid that day into an account the events extract shows opened that day, with no BREAK or CLOSE on that account in the 30 days after maturity, taking its principal or only the part of its proceeds paid into the new account: the counts and principal in block 4.
7. Summed the principal in kbs_term_holdings_2026-11-02.csv maturing in each month once per account, added the certificates in kip_certificate_register_2026-06-30.csv maturing in the month that kip_migration_batches_2026.csv does not show as MIGRATED, and took off the list's principal for the month: the amounts in block 4.
8. Rounded once, as the retention procedure books: 5,500 agent-hours, 1,500 for January, 2,000 for February and 2,000 for March.

## 4. Deliverable Answers

### td_booking_q1_2027.xlsx

1. Agent-hours to book with Harbourline for the January to March 2027 list: 5,500
2. Agent-hours for the deposits maturing in each month:
   - January 2027: 1,500
   - February 2027: 2,000
   - March 2027: 2,000
3. Deposits on each campaign's list still on term deposit with the Society 30 days after maturity, and their principal:
   - January to March 2025: 6,520 deposits, NZ$486,794,000
   - April to June 2025: 7,007 deposits, NZ$526,875,000
   - July to September 2025: 6,902 deposits, NZ$504,704,000
   - October to December 2025: 6,917 deposits, NZ$500,989,000
   - January to March 2026: 6,860 deposits, NZ$503,624,000
   - April to June 2026: 6,933 deposits, NZ$512,433,000
   - July to September 2026: 7,001 deposits, NZ$521,207,000
4. Principal on term deposits and investment certificates maturing across all members, and the part not on the list:
   - January 2027: maturing NZ$467,102,000, not on the list NZ$60,860,000
   - February 2027: maturing NZ$633,665,000, not on the list NZ$74,665,000
   - March 2027: maturing NZ$633,034,000, not on the list NZ$80,661,000

### td_booking_note_q1_2027.docx

1. Opens with the booking: 5,500 agent-hours, 1,500 for January maturities, 2,000 for February and 2,000 for March.
2. Stacked bar chart of the agent-hours by maturity month, January, February and March 2027, each bar labelled with its hours to book (1,500, 2,000 and 2,000) and split into dials that do not reach the holder, conversations and the retention offer's further minutes.
