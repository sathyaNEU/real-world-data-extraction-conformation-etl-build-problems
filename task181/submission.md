# task181: Larchmere Credit Union, the card reissue after the counterfeit wave

## Tags

**Domain:** Banking, Credit & Financial Risk (fraud and AML detection: tracing a card compromise to its common point of purchase at a card-issuing credit union).
**Analytical objective:** Anomaly Detection & Diagnostics (separating the terminals that skimmed members' cards from the places their holders only passed through).

## 1. Final Recommendation

**Reissue 387 member cards: every card still open that the Ferrier Creek Travel Plaza pay-at-pump terminal LT723511 in Kemptville read by contact from 5 to 31 August 2026, or the Lombard Market terminal 02417158 in Smiths Falls read by contact from 13 August to 14 September 2026.**

The pump accounts for 205 of the 283 counterfeit cards, and Lombard Market for 47 of the 78 the pump leaves. Not the pump alone, which leaves every card Lombard Market read in its window in members' wallets. Not the plaza's coffee counter and car wash, which rank high in the pooled screen only because every counterfeit card they read had also been read at the pump in its window. Not the residual put down to travel, since none of the 47 Lombard Market cards was used outside Ontario.

## 2. Critical Components

1. The pay-at-pump terminal LT723511 read **205** of the 283 counterfeit cards by contact in their 60-day lookbacks; its window runs **5 to 31 August 2026**
2. Of the **78** counterfeit cards the pump does not account for, Lombard Market terminal 02417158 read **47**; its window runs **13 August to 14 September 2026**
3. Open cards read by contact inside the windows: **174** at the pump and **228** at Lombard Market, **15** of them at both
4. Cards to reissue: **387**

## 3. Step-by-Step Solution

1. Took the 283 counterfeit cards and each card's first counterfeit use (its earliest disputed counterfeit `txn_date`) from `fraud_cases_2026-08-01_2026-10-04.xlsx`.
2. Ran the CP-14 section 4 screen on contact reads (entry modes 05, 80 and 90 per `pos_entry_mode_codebook.pdf`) by `terminal_id` in `card_authorisations_2026-06-01_2026-10-04.parquet`, each card's 60-day lookback against the member base rate: terminal LT723511 leads with 205 cards, and every counterfeit card the plaza's coffee counter and car wash read was also a pump card.
3. Set the pump's 205 cards aside and screened the 78 left: Lombard Market terminal 02417158 read 47 of them, and the cards left after both were all used outside Ontario with no terminal standing out.
4. Took each terminal's window from the first to the last read of a card later used in counterfeit fraud (CP-14 section 5): 5 to 31 August 2026 at the pump, 13 August to 14 September 2026 at Lombard Market.
5. Counted the cards each terminal read by contact inside its window and kept those with status Open in `card_history_2026-10-05.xlsx` (CP-14 section 6): 174 and 228, 15 at both, 387 cards.
6. Losses: counterfeit rows taken once per `retrieval_ref`, priced at the authorisation log's `amount_billing_cad`, recovered as the signed `amount_cad` total in `chargebacks_2026-08-01_2026-10-04.csv`, split by card type from the card history (CP-14 section 7).
7. Refunds: merged cases sharing a `retrieval_ref` into one claim and counted MS-3 business days from the Eastern date of the first report to `refunded_on`, using the holiday list in `MS-3_member_service_standard.docx`.
8. Recommendation: reissue 387 cards.

## 4. Deliverable Answers

### card_reissue_request.pdf

1. Cards to reissue: 387
2. Ferrier Creek Travel Plaza - Pay at Pump, Kemptville, terminal ID LT723511: first read 5 August 2026, last read 31 August 2026
3. Lombard Market, Smiths Falls, terminal ID 02417158: first read 13 August 2026, last read 14 September 2026
4. Debit cards: gross loss $246,792.17, recovered $78,330.45, net $168,461.72
5. Credit cards: gross loss $35,217.25, recovered $11,845.28, net $23,371.97
6. Debit cards: 195 counterfeit cases refunded within ten business days; longest wait of a refunded member 20 business days
7. Credit cards: 21 counterfeit cases refunded within ten business days; longest wait of a refunded member 16 business days

### common_point_trace.xlsx

1. Sheet 1 Reissue: 387 cards to reissue; Ferrier Creek Travel Plaza - Pay at Pump, Kemptville, LT723511, 5 August to 31 August 2026; Lombard Market, Smiths Falls, 02417158, 13 August to 14 September 2026
2. Sheet 2 Losses: debit gross $246,792.17, recovered $78,330.45, net $168,461.72; credit gross $35,217.25, recovered $11,845.28, net $23,371.97
3. Sheet 3 Refunds: debit 195 within ten business days, longest wait 20 business days; credit 21 within ten business days, longest wait 16 business days
