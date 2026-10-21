## Tags

**Domain:** Product Analytics, churn propensity and uplift modelling.
**Analytical objective:** Forecasting and predictive modelling.

## 1. Final Recommendation

**20 per cent of the 48,000 subscriptions on the 26 January 2027 list will still be subscribed on 31 March 2027 because they are sent the offer.**
Last January the offer kept 20 per cent of the test's subscriptions whose next bill fell within 14 days of the send, and every bill on this year's list falls 6 days after it. Not the test's whole-list 10 per cent, which averages in subscriptions billed later in the month, where the offer kept almost none.

## 2. Critical Components

1. Every subscription on this year's list bills next on **1 February 2027**, **6 days** after the 26 January send (**48,000** of 48,000).
2. Last January the offer kept **20 per cent** of the test's subscriptions whose next bill fell within 14 days of the send, and almost none of those billed later.

## 3. Step-by-Step Solution

1. Joined retention_campaign_2026-01_assignment.csv to subscription_events.csv: a test subscription is subscribed on 31 March 2026 unless its access ended before then and it did not restart by then (data dictionary, access_ended); offer against holdout as randomised.
2. Took each test subscription's billing day from its January 2026 SUB line in legacy_billing_invoices.csv and its next bill in February (on the month's last day where the billing day is past it): 1 to 28 days after the send.
3. Compared the arms by those days: within 14 days of the send the offer kept 20 per cent, later 0 per cent, the whole list 10 per cent (nearest 5).
4. Took this year's next bill from the lines of subscriptions_platform_invoices.csv: every list subscription's last bill covers January 2027, so all 48,000 bill next on 1 February 2027, 6 days after the send, as the 1st-of-month calendar in billing_move_note_2026.pdf has it.
5. Carried the rate within 14 days of the bill to the whole list: 20 per cent.
6. Took last January's offer discounts as the DISC lines in legacy_billing_invoices.csv whose applied_ref is an acceptance in offers_engine_acceptances_2026.csv (app acceptances carry their own code and the app's user key; the save desk's STAY50 cases are not the offer), by the month the bill was raised and the plan in subscriber_profile_2026-01-31.csv; the subscriptions on those lines took it.
7. Took each list subscription's own lines from the lines column of subscriptions_platform_invoices.csv by their subscription_id (an account's invoice also carries its add-ons and any other plan it pays for, and some list subscriptions are billed on another account's invoice) by the UK date each bill was raised (times are UTC), added its legacy 1 October bill through subscription_id_crosswalk.csv and took off each bill a credit note covers at that bill's own amount.
8. Recommendation: 20 per cent of the list kept to 31 March 2027 by the offer.

## 4. Deliverable Answers

### retention_offer_forecast_2027.xlsx

1. Share of the 26 January 2027 list still subscribed on 31 March 2027 because of the offer: 20 per cent.
2. Discount last January's offer gave, pounds to the nearest hundred:
   - February 2026 bills, Digital: GBP 31,100
   - February 2026 bills, Digital Plus: GBP 22,200
   - February 2026 bills, Family: GBP 12,600
   - March 2026 bills, Digital: GBP 28,200
   - March 2026 bills, Digital Plus: GBP 20,200
   - March 2026 bills, Family: GBP 11,800
3. Subscriptions that took last January's offer:
   - Digital: 6,224
   - Digital Plus: 3,174
   - Family: 1,402
4. Billed to this year's list for its plans after credits, pounds to the nearest hundred:
   - October 2026, Digital: GBP 135,700
   - October 2026, Digital Plus: GBP 105,500
   - October 2026, Family: GBP 72,700
   - November 2026, Digital: GBP 257,900
   - November 2026, Digital Plus: GBP 199,400
   - November 2026, Family: GBP 136,100
   - December 2026, Digital: GBP 259,100
   - December 2026, Digital Plus: GBP 200,200
   - December 2026, Family: GBP 136,500
   - January 2027, Digital: GBP 259,100
   - January 2027, Digital Plus: GBP 200,300
   - January 2027, Family: GBP 136,600

### january_offer_note.docx

1. The case: 20 per cent of the list kept to 31 March 2027, from last January's rate within 14 days of the bill, with every bill this year 6 days after the send.
2. Bar chart of the share last January's offer kept by days from the send to the next bill, the days within 14 of the bill highlighted and this year's 6 marked.
