## Tags

**Domain:** Product Analytics (feature adoption and diffusion modeling).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**We should put the 2027 onboarding pod with the Southwest team: it adds about 600 new paying customers in calendar 2027, the most of any region.** Not Texas & Gulf, second, which leads every forecast built on the regions' own history, trend, season and spend, but carries none of the customers that the Southwest's 2026 leavers will found.

## 2. Critical Components

1. Between April and September 2026 the Southwest's paying customers removed about **6,500** users from their workspaces, about four times the region's 2025 monthly pace.
2. About two in five of 2025's new paying customers were founded by someone who had left a paying customer, and the new company pays its first invoice a median of **10 to 11** months after they leave.
3. Counted where each new company bills, about **400** of the Southwest's 2027 new customers are founded by leavers, beside a usual intake of about **150 to 200**.

## 3. Step-by-Step Solution

1. Counted new paying customers by the memo's rules from billing_legacy_subscriptions_2015-2023.csv and the Subscriptions sheet of billing_subscription_register_2022-12_2026-09.xlsx through crm_accounts_2026-10-01.csv (dual-run migrations once, voided invoices, divisions and reactivations out, each in the region of its own parent company's billing state on sales_territories_2024-03.csv): 1,744 in 2025.
2. Fitted each region's monthly new customers on its own trend, month and log marketing spend from marketing_spend_FY2020-FY2028.xlsx: Texas & Gulf leads every such model, and the CRM's customer-referral lead source stays small and flat.
3. Linked each new workspace's first user in product_user_directory_2026-10-01.csv by mobile number to the latest earlier removal of that person from another paying customer's workspace (account closures out, per the Seats line of fy2028_planning_basis.pdf): 4,451 founders, a median lag of about 11 calendar months to the first paid invoice, about 5.7 founders per hundred removals and 88 per cent billing in the region they left.
4. Counted the Southwest's removals from April to September 2026: about 6,500, about four times its 2025 monthly average.
5. Projected 2027 as the founders from the removals to September 2026 and, per the planning basis, each region's 2025 monthly average from October, spread by the lag and counted in the region where each new company bills, plus a Poisson model of the customers no leaver founded (region, trend, month, log spend at the plan): the Southwest about 400 founded by leavers and about 200 usual intake, about 600 in all, with Texas & Gulf second.
6. Took specialist hours from onboarding_sessions_2024-01_2026-09.csv as one session per host and start, held when any of its bookings was completed, its length once for that host, group sessions being the Field app training and Office hours templates of data_dictionary.pdf, each in the pod onboarding_team_roster_2026-10-01.csv has its host in on the session's date; a specialist listed on a colleague's booking that lies wholly inside a session of their own, which no one else hosts, spent no time on it, the colleague being free then (every overlap in the log is such a pair, so counting each specialist's minutes once gives the same hours), while a shadowing second specialist with no clash spent their own hour: the 24 hours in block 4.
7. Took each 2025 new customer's plan and contract value in force on its first paid invoice date, the register's terms today taken back through every amendment on the Amendments sheet effective after that date, latest first and a day's amendments in the order their own terms either side chain rather than by amendment number (a plan move is applied before the seats taken with it), a change effective on that date kept, each customer on the plan its SKU names as numbered when it was set: before product_catalog_2026-07-01.csv the SKUs ran PLW-100 Pro, PLW-200 Enterprise, PLW-300 Core, as the starting contract values against the catalog's list and seat prices show, and the 36 PLW-100 starts invoiced at exactly Core's list price for their seats are Pro (each that reached its first anniversary moved that day to Pro's list price with its SKU and seats unchanged): the 18 counts and 18 values in block 4.
8. Placed the pod with the Southwest, about 600 new paying customers in 2027, Texas & Gulf second.

## 4. Deliverable Answers

### onboarding_pod_2027.docx

1. The 2027 onboarding pod sits with the Southwest team; the Southwest adds about 600 new paying customers in calendar 2027; Texas & Gulf comes second.

### onboarding_staffing_2025.xlsx

1. Hours of specialist time each pod's specialists spent in sessions held with customers, 2025, two decimals:
   - West, one-to-one: Q1 316.25, Q2 379.50, Q3 461.25, Q4 405.75
   - West, group: Q1 58.00, Q2 56.00, Q3 61.50, Q4 61.50
   - Central, one-to-one: Q1 418.50, Q2 438.25, Q3 378.25, Q4 403.00
   - Central, group: Q1 60.00, Q2 59.50, Q3 60.50, Q4 45.50
   - East, one-to-one: Q1 290.00, Q2 325.75, Q3 396.00, Q4 302.50
   - East, group: Q1 54.00, Q2 57.00, Q3 59.50, Q4 52.00
2. New paying customers of 2025 by the plan they started on:
   - Southwest: Core 114, Pro 138, Enterprise 51
   - Southeast: Core 114, Pro 133, Enterprise 41
   - Texas & Gulf: Core 154, Pro 162, Enterprise 72
   - Midwest: Core 111, Pro 109, Enterprise 44
   - Northeast: Core 88, Pro 86, Enterprise 48
   - Pacific: Core 110, Pro 120, Enterprise 49
3. Annual contract value they signed on each plan, on the terms in force on the first paid invoice date, thousands of dollars to one decimal:
   - Southwest: Core 569.8, Pro 1,449.7, Enterprise 1,379.5
   - Southeast: Core 578.9, Pro 1,380.1, Enterprise 1,117.9
   - Texas & Gulf: Core 802.5, Pro 1,693.1, Enterprise 1,970.3
   - Midwest: Core 570.9, Pro 1,105.6, Enterprise 1,185.2
   - Northeast: Core 428.8, Pro 873.4, Enterprise 1,283.4
   - Pacific: Core 566.1, Pro 1,280.1, Enterprise 1,306.4
