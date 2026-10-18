## Tags

**Domain:** General Statistics & Data Science (regression, classification and model diagnostics: a software company's global mobility team quoting in its benefits portal the wait within which four in five of its January to March 2027 work-permit renewals will have USCIS's decision, each renewal's wait cut at its own card's expiry by the team's expedite request, the model chosen on the renewals filed since automatic extension ended that were still pending at their card's expiry).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**The benefits portal should quote 5.5 months for the work-permit renewals filed from January to March 2027.** USCIS is setting fingerprint appointments 17 weeks after receipt, so more than half of the quarter's renewals will still be pending on the day the filer's card expires, and since renewals stopped extending the card, those still pending at their card's expiry have mostly been decided about a week after the expedite request the team files when the card expires. Not 7.0 months, the new appointment delay laid on the record's appointment-route waits, which ignores that those waits now end at the card's expiry. Not 4.0 months, the 80th percentile of the record's own waits with open renewals censored, which reflects appointments 4 weeks out.

## 2. Critical Components

1. Fingerprint appointments for renewals received in October and November 2026: a median of **17 weeks** after receipt, against **4 weeks** for renewals received before September 2026.
2. Renewals filed in the quarter still pending on the day the filer's card expires: **more than half**.
3. From the team's expedite request when a card expires to USCIS's decision, renewals filed since 30 October 2025: a median of **about a week**.

## 3. Step-by-Step Solution

1. Joined renewal_case_notices_2024-01_2026-12.csv to renewal_case_register.xlsx (client_ref through case_id or legacy_case_id) and kept, for each renewal counsel filed, the receipt date (standard 2.3), the latest biometrics appointment notice, the decision notice and the expiry of the card it renews, withdrawn renewals left out (standard 4.2).
2. Read the latest appointment notices: a median of 17 weeks after receipt for renewals received in October and November 2026, 4 weeks before September 2026.
3. Estimated the review, from the appointment (or the receipt where USCIS reused fingerprints) to the decision, by Kaplan-Meier, censored at the export, at a stop of work or at an expedite request in case_actions_2024-2026.csv.
4. For renewals filed since 30 October 2025 (standard 3.1), the case log shows the team's expedite request when each renewal still pending in its care reached its card's expiry (the expiry date or the next business day), USCIS accepted most of the requests and decided those renewals a median of about a week later, where the stage model fitted on the earlier renewals puts their typical remaining wait at more than two weeks.
5. Simulated the quarter's renewals with the new appointment lead, the review, the card-expiry gaps of the renewals filed since 30 October 2025 and the expedite response: more than half reach their card's expiry undecided.
6. Took the 80th percentile of the simulated waits in months of 30.4 days, to the nearest half month (standard 4.3): 5.5 months.

## 4. Deliverable Answers

### q1_2027_renewal_quote.xlsx

1. Wait to quote for the renewals filed from January to March 2027: 5.5 months.
2. Work permits held by current employees and the spouses of current employees expiring, by month and category:
   - July 2027: (c)(9) 279, (c)(26) 186
   - August 2027: (c)(9) 140, (c)(26) 206
   - September 2027: (c)(9) 63, (c)(26) 825
3. Renewal packets the lockbox rejected, by the notice date on the rejection, and those filed again within 30 days of that date:
   - October to December 2025: 26 rejected, 21 filed again within 30 days
   - January to March 2026: 17 rejected, 15 filed again within 30 days
   - April to June 2026: 45 rejected, 35 filed again within 30 days
   - July to September 2026: 16 rejected, 11 filed again within 30 days

### q1_2027_expiring_permits.svg

1. Grouped bar chart of the work permits expiring in July, August and September 2027, a (c)(9) and a (c)(26) bar for each month, each labelled with its count (279 and 186, 140 and 206, 63 and 825).
