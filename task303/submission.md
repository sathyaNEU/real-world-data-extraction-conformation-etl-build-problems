## Tags

**Domain:** Energy systems and utilities (asset condition and maintenance).
**Analytical objective:** Opportunity sizing and decision support.

## 1. Final Recommendation

**Convert the backbone of F-205 (Sorrel Hill) in 2027: it removes 237,600 customer-minutes of sustained interruption a year, worth USD 499,000 a year at the commission's USD 2.10 a customer-minute.**
F-112 (Pell Creek) comes next at 137,800; it leads at 455,400 only when every breaker ticket is credited to its own backbone, and most of its vegetation, wind and wildlife breaker tickets fall on the 12 occasions all three Pell Creek feeders lost supply in the same minute, which no backbone conversion prevents. F-114 falls from 285,400 to 29,600 the same way; F-301, F-208 and F-303 come to 67,300, 39,000 and 32,100.

## 2. Critical Components

1. Outside the accepted major event days of 2019 to 2025, the breakers of all three Pell Creek feeders (F-112, F-114, F-117) opened in the same minute **12** times, and the Byers Mill feeders' **3** times; Sorrel Hill's never did. Each is a loss of the substation's supply, logged on every feeder's own breaker with the cause found on the line feeding the substation, and the conversion does not prevent it.
2. Without those tickets the conversion removes **237,600** customer-minutes a year on F-205 against **137,800** on F-112, where crediting every breaker ticket gives F-112 **455,400**.

## 3. Step-by-Step Solution

1. Stacked oms_interruptions_2019_2022.csv (feeder 112 as F-112, the cause and device codes and Eastern local times as oms_export_notes.txt describes) and oms_interruptions_2023_2025.csv (UTC stamps put on Eastern time); a ticket's minutes are DUR_MIN, or its restoration less its start, and its customer-minutes are its customers interrupted times its minutes.
2. Left out every ticket that began on an Eastern date listed in major_event_days_2019_2025.csv.
3. Kept the six candidates' feeder breaker and line recloser tickets caused by vegetation, wind or wildlife (storm_hardening_plan_2027.docx, section 1).
4. Took out the tickets opened in the same minute on every feeder at the substation (the substations' feeders from feeder_inventory_2026.xlsx): 12 on each Pell Creek feeder, 3 on each Byers Mill feeder, none at Sorrel Hill; they are losses of the substation's supply, not faults on the candidate's backbone.
5. Took nine in ten of the remaining customer-minutes and divided by seven (the plan, section 3): F-205 237,600; F-112 137,800; F-301 67,300; F-208 39,000; F-303 32,100; F-114 29,600; F-205 at USD 2.10 (section 4) is USD 499,000 a year.
6. Storm record: each candidate's tickets in oms_interruptions_2023_2025.csv that began on an accepted major event day of 2023 to 2025, each restored at its crew's Restored time in storm_crew_status_2023_2025.csv, not at the outage system's restoration (the storm desk's later entry, or the crew's time as it arrived), with the contract crews' device times read as Eastern standard time, which they keep all year (read as daylight time, every contract crew on a summer storm day is en route before the desk gave it the job); customer-minutes summed, and over the customers interrupted.
7. Taps: each candidate's fuse tickets outside the major event days over 2019 to 2025, where a legacy DUR_MIN with a decimal point is a trouble crew's handheld ticket, its duration in hours and minutes (7.28 is 448 minutes, and no such entry has more than 59 after the point) and its OUT_DT the day the crew closed it, so it began on the day that, with its duration, ends on OUT_DT (only then do the ticket numbers run in the order the interruptions began); customer-minutes over seven, and over the customers interrupted.
8. Recommend converting F-205, the largest figure, as the plan funds.

## 4. Deliverable Answers

### hardening_memo_2027.pdf

1. Convert the backbone of F-205 (Sorrel Hill) in 2027.
2. Customer-minutes of sustained interruption it removes a year: 237,600
3. Every candidate's figure, customer-minutes a year:
   - F-205: 237,600
   - F-112: 137,800
   - F-301: 67,300
   - F-208: 39,000
   - F-303: 32,100
   - F-114: 29,600
4. What F-205's figure earns a year at the commission's incentive rate: USD 499,000

### hardening_tables_2027.xlsx

1. Customer-minutes on the commission's accepted major event days of 2023 to 2025, and those minutes per customer interrupted:
   - F-112: 11,615,000 customer-minutes; 411.9 minutes per customer interrupted
   - F-114: 5,773,000 customer-minutes; 339.7 minutes per customer interrupted
   - F-205: 7,332,000 customer-minutes; 393.5 minutes per customer interrupted
   - F-208: 6,210,000 customer-minutes; 413.5 minutes per customer interrupted
   - F-301: 9,952,000 customer-minutes; 406.1 minutes per customer interrupted
   - F-303: 4,391,000 customer-minutes; 420.3 minutes per customer interrupted
2. Customer-minutes a year from interruptions the tap fuses cleared outside the major event days over 2019 to 2025, and those minutes per customer interrupted:
   - F-112: 23,840 customer-minutes a year; 125.1 minutes per customer interrupted
   - F-114: 14,450 customer-minutes a year; 116.3 minutes per customer interrupted
   - F-205: 25,950 customer-minutes a year; 119.2 minutes per customer interrupted
   - F-208: 9,000 customer-minutes a year; 116.5 minutes per customer interrupted
   - F-301: 16,410 customer-minutes a year; 110.6 minutes per customer interrupted
   - F-303: 13,540 customer-minutes a year; 118.5 minutes per customer interrupted
