## Tags

**Domain:** Energy Systems & Utilities (load forecasting).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Allocate the 400 replacements as Foothill 77, Railyard 68, Canal 50, Mission 23, West Bluff 16, Crestview 5, Lakeside 4, Sunrise 5, Sandhill 71, Kingsley 27, Highland 8 and Brookside 46.**

Foothill's 353 of the 1,830 transformers forecast above 120 percent of nameplate carry its 77 replacements, each default-rate vehicle taken at the 4.9 kVA it adds to a transformer's recorded summer peak. Not the load study's 4 to 9 pm average of 0.61 kVA a default-rate vehicle, which gives Foothill 59: it is the vehicle's mean draw over the window, not its effect on the transformer's highest quarter hour.

## 2. Critical Components

1. Transformers forecast at risk across the twelve districts: **1,830**
2. Foothill's transformers forecast at risk: **353**
3. Weather-adjusted rise in a transformer's recorded summer peak when it gained one vehicle between the 2024, 2025 and 2026 summers, pooled over sizes: **4.9 kVA** a default-rate vehicle, **0.9 kVA** an R-EV2 vehicle

## 3. Step-by-Step Solution

1. Placed each DMV notification at its matched_sp_id and that service point's transformer, a vehicle present on a date from reg_start_date up to its status_date, its premise on R-EV2 from the rate change effective_date.
2. Counted each transformer's default-rate and R-EV2 vehicles on the dates of its 2024, 2025 and 2026 TLM peaks and on the record date of Ordering Paragraph 5.
3. Took the rise in recorded peak of the transformers that gained one vehicle between summers, less the district's median ratio on transformers with no change, by size group and position: 4.9 kVA pooled for a default-rate vehicle, 0.9 kVA for an R-EV2 one.
4. Forecast each transformer per Ordering Paragraph 4 as its 2026 TLM peak plus the rises of its record-date vehicles less those of its peak-day vehicles, and counted those exceeding 1.2 times the register's kva_rating: 1,830, Foothill 353.
5. Pilot: counted the PTR changes from 6 October 2025 to 24 April 2026 whose installed_serial differs from the removed_serial, their kVA change, and every cost line on the district's pilot work orders over those units.
6. Failures: took the EQ-XFMR lines starting 1 June to 30 September local time (UTC less seven hours), each line's customers from its transformer's service points and its hours to restored_utc.
7. Split the 400 by largest remainder per Ordering Paragraph 2: Foothill 77.

## 4. Deliverable Answers

### ptr_2027_district_allocation.xlsx

1. Transformers forecast at risk and replacements by district:
   - Foothill: 353 at risk, 77 replacements
   - Railyard: 312 at risk, 68 replacements
   - Canal: 228 at risk, 50 replacements
   - Mission: 105 at risk, 23 replacements
   - West Bluff: 74 at risk, 16 replacements
   - Crestview: 22 at risk, 5 replacements
   - Lakeside: 19 at risk, 4 replacements
   - Sunrise: 23 at risk, 5 replacements
   - Sandhill: 324 at risk, 71 replacements
   - Kingsley: 123 at risk, 27 replacements
   - Highland: 36 at risk, 8 replacements
   - Brookside: 211 at risk, 46 replacements
2. Foothill's replacements: 77
3. 2025-26 pilot by district:
   - Railyard: 94 transformers replaced, 1,812.5 kVA added, $6,799 per transformer replaced
   - Canal: 81 transformers replaced, 1,532.5 kVA added, $7,049 per transformer replaced
   - Brookside: 88 transformers replaced, 1,615.0 kVA added, $7,008 per transformer replaced
4. Service transformer failures from 1 June to 30 September 2026 by district:
   - Foothill: 1,010 customer-hours, 50 customers out more than eight hours
   - Railyard: 1,676 customer-hours, 80 customers out more than eight hours
   - Canal: 1,185 customer-hours, 54 customers out more than eight hours
   - Mission: 1,231 customer-hours, 52 customers out more than eight hours
   - West Bluff: 810 customer-hours, 42 customers out more than eight hours
   - Crestview: 717 customer-hours, 39 customers out more than eight hours
   - Lakeside: 540 customer-hours, 21 customers out more than eight hours
   - Sunrise: 1,181 customer-hours, 41 customers out more than eight hours
   - Sandhill: 1,527 customer-hours, 87 customers out more than eight hours
   - Kingsley: 1,063 customer-hours, 35 customers out more than eight hours
   - Highland: 764 customer-hours, 18 customers out more than eight hours
   - Brookside: 652 customer-hours, 35 customers out more than eight hours

### summer_2026_transformer_failures.png

1. Horizontal bar chart of the customer-hours by district, each bar labelled with its customer-hours and its customers out more than eight hours.
