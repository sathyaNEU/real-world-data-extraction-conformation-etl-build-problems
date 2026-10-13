# task131 submission

## Tags

**Domain:** Energy Systems & Utilities (tariff and demand-response evaluation: reading a randomised summer trial of three peak-window residential tariffs for what each would do to an isolated town system's design-day maximum demand).
**Analytical objective:** Experiment & Causal Analysis (which trialled design, if any, flat-rate households move onto from 1 July 2027, judged by its effect on the 2027-28 summer maximum demand at 50% probability of exceedance).

## 1. Final Recommendation

**Move every flat-rate residential customer onto Design C (Stepped) from 1 July 2027: it lowers the 2027-28 summer maximum demand at 50% probability of exceedance by 11 MW.**

Not Design A, which would raise the maximum by 5 MW once its households' pull-down after 9 p.m. is added to the design day; not Design B, which cuts the most inside its window yet would raise the maximum by 20 MW, its pull-down landing in the half-hour from 8 p.m. Keeping the Home Plan leaves the maximum at 214.6 MW.

## 2. Critical Components

1. The trial has **7** workdays at the heat of the 44.6-degree design day, at 43.7 to 45.3 degrees (19 to 23 January and 10 and 11 February 2026); no other workday was above 39.7 degrees
2. On those days Design B's households drew **0.7 kW** more than the control households in the half-hour from 8 p.m., and Design A's **0.6 kW** more in the half-hour from 9 p.m.
3. With every half-hour's effect added to the design-day profile for the forecast's **41,860** Home Plan customers, the maximum falls in the half-hour from **8 p.m.** under Designs B and C and from **9 p.m.** under Design A

## 3. Step-by-Step Solution

1. Parsed the four MRP_NEM12 extracts: the latest update of each meter serial's day, an exchange day summed across its two meters, 15-minute reads paired into half-hours; household demand is E1 plus E2 less B1, kWh times two, in kW.
2. Followed each household in summer_pricing_trial_register.xlsx by customer number through account_tariff_history_2026-03-12.csv to the premise it held each day, every household in its assigned arm as section 6 of summer_pricing_trial_plan.pdf reads the trial.
3. Took the trial's workdays (weekdays other than public holidays, 1 December 2025 to 28 February 2026) at the heat of the 44.6-degree design day in murrandi_demand_forecast_2026.xlsx: 7, at 43.7 to 45.3 degrees in IDCJAC0010_013027_1800_Data.csv, no other workday above 39.7.
4. For each design and half-hour, took its households' mean demand less the control households', averaged over those 7 days.
5. Added 41,860 times each half-hour's effect to the 2027-28 50% POE design-day profile and took the highest half-hour: Design C lowers the 214.6 MW maximum by 11 MW, Design A raises it by 5 MW and Design B by 20 MW.
6. For the tables: each household's general-supply tariff on 28 February 2026, followed by customer number; its general-supply charges at the gazetted 2025-26 charges in residential_charges_2025-26.pdf on the days it was billed on its design, against the Home Plan for the same reads; and its first submitted survey response, telephone answers to Q4 coded in the order read.
7. Recommendation: Design C from 1 July 2027, 11 MW off the 2027-28 maximum demand.

## 4. Deliverable Answers

### tariff_default_advice_2027-28.pdf

1. The call: move every flat-rate residential customer onto Design C (Stepped) from 1 July 2027.
2. Each design's change to the 2027-28 summer maximum demand at 50% probability of exceedance, nearest whole MW:
   - Design C (Stepped): lowers it by 11 MW
   - Design A (Evening 3 to 9): raises it by 5 MW
   - Design B (Evening 4 to 8): raises it by 20 MW
3. Bar chart of the three changes, Design C highlighted, each bar labelled with its change.

### tariff_trial_tables_2025-26.xlsx

1. Households on 28 February 2026 (still billed on the design; back on the Home Plan at their own request; no longer our customers):
   - Design A (Evening 3 to 9): 370; 22; 7
   - Design B (Evening 4 to 8): 361; 29; 9
   - Design C (Stepped): 374; 18; 6
2. Charges over the trial (households charged more than the Home Plan would have charged for the same metered use; mean of that difference per trial household including GST, a negative difference a saving):
   - Design A (Evening 3 to 9): 123; -$19.64
   - Design B (Evening 4 to 8): 45; -$42.86
   - Design C (Stepped): 52; -$31.61
3. Households answering the March 2026 survey who said they were likely or very likely to stay on the design, share to one decimal place:
   - Design A (Evening 3 to 9): 60.3 per cent
   - Design B (Evening 4 to 8): 41.5 per cent
   - Design C (Stepped): 58.8 per cent
