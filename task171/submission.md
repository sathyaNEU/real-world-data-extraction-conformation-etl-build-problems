## Tags

**Domain:** Economics & Econometrics (discrete choice and limited dependent variable modeling).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Budget for 2,250 R-1 services moved to R-ON by December 31, 2027, giving up $200,000 a year at test-year use.** Members take an optional rate by what it saves them on their own use, so the overnight rate's take-up is the evening rate's first-year response to each service's saving on its use in the year before that offer, run through each service's overnight saving. Not the evening rate's take-up applied at the average member's bill change, which ignores who takes an optional rate. Not the same response read on the latest year's use, which the evening rate's takers had already changed by taking it.

## 2. Critical Components

1. The forecast population is **21,490** R-1 services billed in all twelve test-year months.
2. Of the **25,559** R-1 services open when R-TOU opened in March 2024, **2,017** had it in effect by the February 2025 read.
3. The services moved to R-ON by December 31, 2027 are **2,250**, giving up **$200,000** a year.

## 3. Step-by-Step Solution

1. Took from cis_rate_assignments_2026-10-31.csv and cis_service_accounts_2026-10-31.csv the R-1 services open when R-TOU opened in March 2024 (25,559) and the month each first had R-TOU in effect, 2,017 by the February 2025 read, a service leaving the risk set at its final read.
2. Priced each of those services' R-1 and R-TOU bills at the 2024 prices in residential_rate_schedules_2024-2027.pdf on its own use in billing months March 2023 to February 2024 in ami_load_research_extract_2023-03_2026-10.parquet, and fitted a monthly logit hazard of R-TOU taking effect on that saving with a term for each month since the offer.
3. Took the population of paper RC-26-19 in r-on_launch_plan_rates_committee_nov2026.docx, 21,490 R-1 services at October 31, 2026 billed in all twelve billing months November 2025 to October 2026, and priced each one's R-1 and R-ON bills on the 2027 schedules on that use.
4. Ran each population service's saving through the fitted hazard over the twelve months of 2027 and summed the probabilities and the probability-weighted savings: 2,250 services and $200,000.
5. For the R-TOU table, joined each service's contiguous R-TOU rows into one spell (the TOU module re-writes the row at account maintenance), ended an open R-TOU row at the service's final read, kept the re-collected actual row where the extract holds an estimate and an actual for one meter and read period, and summed the kWh by district.
6. For the requests table, converted received_utc in crm_rate_requests_2024-03_2026-10.xlsx to Central time, dropped cases closed as duplicates, placed each completed case in the district of the service that had R-TOU take effect at the next read after the case was completed (the case's service or the same member's other service) and each other case at the service it names.
7. Filed 2,250 services and $200,000 for the 2027 budget.

## 4. Deliverable Answers

### r-on_2027_forecast.xlsx

1. R-1 services moved to R-ON by December 31, 2027: 2,250.
2. Annual revenue those services give up at test-year use: $200,000.
3. Services on R-TOU at October 31, 2026, by district:
   - Sedge Flats: 247 on it without a break since November 1, 2025 or earlier; 1,327,738 kWh 4 p.m. to 9 p.m.; 1,800,772 kWh 11 p.m. to 6 a.m.
   - Brisco Bend: 396 on it without a break since November 1, 2025 or earlier; 1,819,585 kWh 4 p.m. to 9 p.m.; 2,515,310 kWh 11 p.m. to 6 a.m.
   - Kessel Mill: 547 on it without a break since November 1, 2025 or earlier; 2,199,290 kWh 4 p.m. to 9 p.m.; 3,840,128 kWh 11 p.m. to 6 a.m.
   - Pike Ridge: 149 on it without a break since November 1, 2025 or earlier; 805,489 kWh 4 p.m. to 9 p.m.; 1,045,518 kWh 11 p.m. to 6 a.m.
   - Tamsey: 358 on it without a break since November 1, 2025 or earlier; 1,567,329 kWh 4 p.m. to 9 p.m.; 2,426,413 kWh 11 p.m. to 6 a.m.
4. R-TOU enrolment requests received March 1 to May 31, 2024, by district:
   - Sedge Flats: 159 requests, 93 through the web form
   - Brisco Bend: 277 requests, 152 through the web form
   - Kessel Mill: 364 requests, 224 through the web form
   - Pike Ridge: 71 requests, 37 through the web form
   - Tamsey: 267 requests, 148 through the web form
