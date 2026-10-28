## Tags

**Domain:** Product Analytics, churn propensity and uplift modelling (a software company's choice of which of five apps takes a three-project limit on its free plan first, sized by the 2027 revenue the limit adds, with free accounts' response read from the accounts the free plan's storage allowance already stops, and each app's recurring revenue bridge from its billing records).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**Brindlecote should take the three-project limit first in Ledgerline, where it adds about GBP 100,000 to 2027 revenue.**
The limit adds GBP 102,022 to Ledgerline's 2027 revenue as built (GBP 85,980 to 121,063 across the standing variants of its construction), against GBP 70,314 in Formbox, the next best. The free plan already stops accounts at its two-gigabyte storage allowance: the month after an account reaches it, 5.2 per cent are on Plus and 36.7 per cent have stopped using the app, and over the following year a stopped account spends 0.46 more months on Plus and 4.5 fewer months on the free plan than an unstopped account over three projects. Ledgerline's GBP 28.00 Plus price outweighs the free-plan revenue (GBP 1.00 a month) each leaver takes with it. Not Tracewood, which the free accounts' own upgrade rate with nobody leaving puts first (GBP 179,082 against GBP 87,266 for Ledgerline): an account the limit stops is not an account upgrading of its own accord, and the leavers cost Tracewood GBP 2.00 a month each. Not Formbox either, which counting every account that does not pay as lost puts first.

## 2. Critical Components

1. The month after a free account first reached the storage allowance (January 2023 to September 2025, 1,685 accounts in the research panel), **5.2 per cent** were on Plus and **36.7 per cent** had stopped using the app, alike across apps, project counts and account ages, while free accounts over three projects move to Plus on their own at about **2.5 per cent a year**.
2. Set against unstopped free accounts over three projects, a stopped account gains **0.46 months on Plus** and loses **4.5 months of free use** in the year after the stop.
3. The limit reaches **10,219** free accounts over three active projects in Ledgerline and **3,035** more reaching a fourth during 2027, and adds **GBP 102,022** to Ledgerline's 2027 revenue (about GBP 100,000), more than in any other app (Formbox GBP 70,314).

## 3. Step-by-Step Solution

1. Read free_plan_limit_paper_2027.pdf: the limit stops a free account over three active projects from editing until it archives or moves to Plus; the addition is the app's 2027 revenue with the limit less without it, a month on Plus at the Plus price and a month of free use at the free-plan revenue per active free account (section 4), the limit reaching every free account over three active projects on 1 January 2027 and every one reaching a fourth during the year.
2. Built each research panel account's months from research_panel_account_months_2023_2026.csv (Leafnote read as Notewell before April 2025): plan, active projects, storage and whether it was used that month; an account with no row in a month was not used.
3. Found the free plan's existing stop in plan_catalogue_2026.csv (2 GB, 2,048 MiB, of storage on the free plan) and the free account-months at it (storage within one per cent of 2,048 MiB): 1,685 accounts reached it for the first time from January 2023 to September 2025, each followed for twelve months.
4. Compared them with free accounts over three active projects below the allowance in the same months (the accounts the limit stops, as they act unstopped), month by month for a year: 0.46 more months on Plus and 4.5 fewer months of free use for a stopped account.
5. Took the accounts the limit reaches from free_accounts_by_active_projects_2023_2026.xlsx for 2026-09 (bands 4-5, 6-9 and 10+), and the accounts reaching a fourth active project each month of a year from the panel's accounts below four in September 2025, applied to each app's accounts with three or fewer.
6. Valued each app's year: the accounts over the limit on 1 January for twelve months after the stop and each month's new arrivals for the rest of the year, at the paper's Plus price and free-plan revenue: Tracewood GBP 12,177; Taskfold GBP 20,087; Ledgerline GBP 102,022; Formbox GBP 70,314; Notewell GBP -11,355.
7. Checked the standing variants (every stop rather than the first, the allowance read at 2,000, 1,950 or 2,047 MiB, every unstopped free account as the comparison, the stops of one year, a year's crossings to September 2024, each app read from its own stopped accounts, only accounts with four or more projects): Ledgerline stays first, GBP 85,980 to 121,063.
8. For the bridge, valued every subscription on FIN-07 (recurring_revenue_policy_fin07.pdf): a monthly price as it is, an annual price over twelve, seat price times seats, after discounts of twelve months or more, euros and dollars at the 2026/27 plan rates in fx_plan_rates.csv; live from billing_subscriptions_20250930.csv and the events to the end of 30 September 2026 (a cancellation ends a subscription at its subscription.ended event, a past-due subscription stays live).
9. Took the customer as the person or organisation that pays: a subscription opened under a new customer record by the same account the day the platform ended its old one after failed payments is the same customer, and staff accounts' Plus subscriptions a company record moved onto one Team subscription stay with that company; then compared each customer's recurring revenue at the two dates, app by app.

## 4. Deliverable Answers

### free_plan_limit_2027.xlsx

1. App to take the three-project limit first: Ledgerline.
2. What it adds to Ledgerline's 2027 revenue: GBP 100,000 (nearest GBP 50,000; GBP 102,022 as built).
3. Each app's 2027 addition behind the call: Tracewood GBP 12,177; Taskfold GBP 20,087; Ledgerline GBP 102,022; Formbox GBP 70,314; Notewell GBP -11,355.
4. Each app's recurring revenue movements from 30 September 2025 to 30 September 2026, GBP a month (new, expansion, contraction, churned):
   - Tracewood: new 125,062, expansion 58,059, contraction 4,379, churned 69,365
   - Taskfold: new 17,212, expansion 4,109, contraction 846, churned 10,578
   - Ledgerline: new 62,034, expansion 22,497, contraction 2,086, churned 41,485
   - Formbox: new 36,825, expansion 7,015, contraction 1,672, churned 20,364
   - Notewell: new 15,536, expansion 4,060, contraction 940, churned 11,070

### free_plan_limit_case_2027.docx

1. The case for the executive: take the limit first in Ledgerline, about GBP 100,000 added to its 2027 revenue, read from the accounts the storage allowance already stops; not Tracewood, which only the free accounts' own upgrades with nobody leaving put first.
