## Tags

**Domain:** Banking, Credit & Financial Risk (deposit liquidity behaviour: term deposit retention at maturity).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**We should book 5,250 agent-hours with Harbourline for the 18,400 term deposits on the January to March 2027 maturity list: 1,250 for the deposits maturing in January, 2,000 for February and 2,000 for March.**
About 54 per cent of the list's expected 14,000 conversations will go to the 22-minute retention offer, against 21 per cent across the seven closed campaigns, because 10,697 of the deposits are money the 4-year special of January to March 2023 won at 5.65 per cent, and at its first maturity money a special won went to the retention offer in 87 per cent of conversations, much the same at every drop it met. Not the past share at the same drop from the deposit's rate to the rate it reinvests at: at drops of 1.50 to 1.75 points, where the special's 1.65-point drop to the 4.00 per cent 4-year rate falls, almost every past conversation was about other deposits, which went to the offer at 28 per cent. Not the pooled share, the latest campaign's, a trend, the share by term or by locked rate: each carries other deposits' share onto a list that is mostly the special's money.

## 2. Critical Components

1. **464** of the 18,400 listed deposits have no callable number once the holders' numbers are washed against the do-not-call register at the cut, and are not released.
2. **10,697** deposits on the list are 4-year deposits opened at the **5.65 per cent** special in January to March 2023 (the list's other 4-year deposits of that quarter from 5.15 per cent); they reinvest at the **4.00 per cent** 4-year rate, a drop of **1.65 points**.
3. In the seven closed campaigns **87 per cent** of conversations about money a special won went to the retention offer, much the same at every drop it met.
4. About **54 per cent** of the list's expected **14,000** conversations go to the retention offer, against **21 per cent** of the seven campaigns' conversations.

## 3. Step-by-Step Solution

1. Normalised the numbers in kbs_contact_points_2026-11-02.csv to E.164 and dropped those on kbs_do_not_call_register_2026-11-02.csv as it stood on 2 November 2026 (recorded by then and not withdrawn by then): 464 of the 18,400 deposits on kbs_td_retention_list_2027Q1.csv have no callable number and, per the retention procedure, are not released.
2. Joined kbs_case_release_log_2025q1-2026q3.csv to harbourline_case_closeouts_2025q1-2026q3.csv and harbourline_dial_log_2025q1-2026q3.csv for every released case of the seven closed campaigns, averaged the dials that did not reach the holder (NOA, BSY, VML, DIS, WNG) and the chance of a conversation by the mix of the case's callable number types (how many mobile, home and work numbers), applied them to the list's mixes, and scaled them by the 95.2 per cent of listed deposits with a callable number that the seven campaigns released (the rest had given instructions): about 66,700 non-reaching dials and 14,000 conversations.
3. Gave each past conversation its deposit's drop (the rate on its row in kbs_td_retention_lists_2025.csv or kbs_td_retention_lists_2026.csv less the reinvestment rate for its term in the quarter's campaign brief PDF) and its class: money a special won where the rate stood 0.40 points or more above the lowest rate of the same list's deposits of its term opened in the same quarter (the one-year deposits at 6.35, 5.45, 5.10, 4.75 and 4.45 per cent, the two-year at 6.30 and the three-year at 6.00). Of 46,298 conversations, the 4,093 about special money went to the retention offer (RTK, RTW) at 87 per cent, much the same at every drop they met; the rest far less often, rising with the drop.
4. Classed the list the same way and read its drops against harbourline_campaign_brief_2027Q1.pdf (4 years 4.00 per cent): 10,697 deposits at 5.65 per cent, against 5.15 for the lowest of their term and quarter, meet a drop of 1.65 points. Each deposit took its class's past share in its 0.25-point band of drop (special money at 1.50 to 1.75 points, 88 per cent), so about 54 per cent of the 14,000 conversations go to the retention offer.
5. Priced the list at schedule 2 of harbourline_sow_HCS-KBS-2025-01.pdf, 1.5 minutes per dial that does not reach the holder, 8 per conversation and 22 per retention-offer conversation: 5,280.9 agent-hours, 1,206.9 for January maturities, 2,013.3 for February and 2,060.7 for March.
6. For each listed deposit of the seven campaigns (account numbers without punctuation), took its principal when kbs_td_account_events_2025-01_2026-10.csv shows a REINVEST on its own account on its maturity date, or otherwise the amounts kbs_member_transfers_2025-01_2026-10.csv shows the maturity settlement account paying that day under the deposit's account number in the narrative into accounts the events extract shows opened that day; either counted only with no BREAK or CLOSE on the account in the 30 days after maturity: the principal and the deposits it came from in block 4.
7. Summed the principal in kbs_term_holdings_2026-11-02.csv maturing in each month once per account, added the certificates in kip_certificate_register_2026-06-30.csv maturing in the month that are not in the core (not MIGRATED in kip_migration_batches_2026.csv, and matching no core certificate on issue date, maturity date, rate and term), and took the list's principal off the quarter's total: the amounts in block 4.
8. Rounded once, as the retention procedure books: 5,250 agent-hours, 1,250 for January, 2,000 for February and 2,000 for March.

## 4. Deliverable Answers

### td_booking_q1_2027.xlsx

1. Agent-hours to book with Harbourline for the January to March 2027 list: 5,250
2. Agent-hours for the deposits maturing in each month:
   - January 2027: 1,250
   - February 2027: 2,000
   - March 2027: 2,000
3. Principal on each campaign's list still on term deposit with the Society 30 days after maturity, and the deposits it came from:
   - January to March 2025: NZ$497,825,000 from 6,700 deposits
   - April to June 2025: NZ$537,491,000 from 7,186 deposits
   - July to September 2025: NZ$532,430,000 from 7,226 deposits
   - October to December 2025: NZ$536,002,000 from 7,172 deposits
   - January to March 2026: NZ$562,096,000 from 7,591 deposits
   - April to June 2026: NZ$557,067,000 from 7,494 deposits
   - July to September 2026: NZ$573,831,000 from 7,765 deposits
4. Principal on term deposits and investment certificates maturing across all members:
   - January 2027: NZ$415,506,000
   - February 2027: NZ$646,816,000
   - March 2027: NZ$672,944,000
   - Not on the list, January to March 2027: NZ$214,491,000

### td_booking_note_q1_2027.docx

1. Opens with the booking: 5,250 agent-hours, 1,250 for January maturities, 2,000 for February and 2,000 for March.
2. Stacked bar chart of the agent-hours by maturity month, January, February and March 2027, each bar labelled with its hours to book (1,250, 2,000 and 2,000) and split into dials that do not reach the holder, conversations and the retention offer's further minutes.
