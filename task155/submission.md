## Tags

**Domain:** Economics & Econometrics (discrete-choice and limited-dependent-variable modelling: casual staff's take-up of extra shifts offered through call-in).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Place the relief crew at Camberwell; it will work 1,090 hours there.**
Call-ins would leave more of Camberwell's open Christmas hours unfilled than of any other store's, because its uplift runs 10 am to 4 pm on weekdays, when most of its casuals are unavailable, and almost none of it carries on from a casual's rostered shift. Not Werribee, which lists the most open hours (3,250) but whose open shifts carry on from its own casuals' rostered shifts, the offer casuals take 33% of the time against 4% for a separate trip in; not Box Hill or Altona, whose evening uplift sits behind their casuals' afternoon shifts in the same way.

## 2. Critical Components

1. Offers that start as the casual's own rostered or booked shift at that store ends, or end as it starts, are accepted **33%** of the time, against **4%** for every other offer.
2. **100%** of Werribee's open Christmas shifts could be taken by one of its own casuals staying on from a rostered shift that ends as the open shift starts or starts as it ends, the module's checks passed (Box Hill **96%**, Altona **79%**), against **2%** of Camberwell's.
3. Camberwell's 215 open shifts carry **1,090** paid hours to the nearest 10.

## 3. Step-by-Step Solution

1. Summed the paid hours (less the unpaid meal break on shifts over five hours, per ea_2024_casual_employment_summary.pdf) of the OPEN lines on each sheet of christmas_roster_2026_published.xlsx: Werribee 3,250 hours, Box Hill 2,600, Altona 1,770, Camberwell 1,090.
2. Joined every offer in callin_offers_20250829_20261112.csv to the casual's roster lines that day (person code to payroll number through kws_people_20261112.csv and the previous numbers in payroll_casual_register_20261112.csv; both roster exports, less lines callin_register_20250829_20261112.csv shows vacated, plus call-ins the casual had accepted): 2,159 offers carried on from the casual's own shift at the store and 33% of them were accepted, against 4% of the other 137,390.
3. Fitted a logit of each offer's acceptance on that term and on another shift the same day, a Sunday shift, the shift's paid hours, finishing after 21:30, starting before 07:00, under four hours' notice, an offer repeated, a sister-store offer, rostered hours over 10 that week, the Christmas weeks, the casual's age band and home store.
4. Ran the fitted choice through the offer order, eligibility checks and offer hours in kws_callin_module_notes.pdf over the published Christmas rosters, every store's open shifts posted at 09:00 on 16 November with the crew at no store (relief_crew_placement_standard.pdf, section 4), 24 runs: call-ins would leave about 670 of Camberwell's open hours unworked, the most of any store, with Ringwood next at about 400.
5. Placed the crew at Camberwell under section 3 of the standard; its crew hours under section 5 are the paid hours of Camberwell's open shifts: 1,090.

## 4. Deliverable Answers

### relief_crew_placement_xmas2026.pdf

1. The placement in the opening sentence: the relief crew to Camberwell, 1,090 crew hours.
2. A horizontal bar chart of every store's forecast unworked hours, largest first, Camberwell highlighted, each bar labelled, titled with the finding.

### relief_crew_xmas2026.xlsx

1. Last Christmas's call-ins, 28 November to 24 December 2025, paid hours: put out to call-in, covered, left uncovered:
   - Altona: 1,616.5, 873.0, 743.5
   - Ballarat: 2,281.0, 996.0, 1,285.0
   - Box Hill: 2,050.5, 1,232.0, 818.5
   - Camberwell: 2,131.0, 1,475.0, 656.0
   - Ringwood: 1,709.0, 981.0, 728.0
   - Sunshine: 2,012.5, 1,161.5, 851.0
   - Werribee: 301.5, 98.5, 203.0
   - Williamstown: 1,453.0, 679.5, 773.5
2. Cover across stores in those weeks, paid hours: the store's call-ins covered by casuals from other stores; its own casuals' cover at other stores:
   - Altona: 33.5; 23.5
   - Ballarat: 0.0; 0.0
   - Box Hill: 24.0; 31.5
   - Camberwell: 15.0; 54.0
   - Ringwood: 56.0; 9.5
   - Sunshine: 42.0; 31.0
   - Werribee: 5.5; 21.5
   - Williamstown: 29.5; 34.5
