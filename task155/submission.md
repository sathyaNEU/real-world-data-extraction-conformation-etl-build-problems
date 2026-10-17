## Tags

**Domain:** Economics & Econometrics (discrete-choice and limited-dependent-variable modelling: casual staff's take-up of extra shifts offered through call-in).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Place the relief crew at Camberwell; it will work 1,090 hours there.**
Call-ins would leave more of Camberwell's open Christmas hours unfilled than of any other store's, because its uplift runs 9 am to 3 pm on weekdays and none of it carries on from a casual's rostered shift: every shift needs a casual to make a separate trip in, and most of the casuals free for it work at Box Hill or Ringwood. Not Werribee, which lists the most open hours (3,250) but whose open shifts carry on from its own casuals' rostered shifts, the offer casuals take 32% of the time against 4% for a separate trip in; not Box Hill or Altona, whose evening uplift sits behind their casuals' afternoon shifts in the same way.

## 2. Critical Components

1. Offers that start as the casual's own rostered or booked shift at that store ends, or end as it starts, are accepted **32%** of the time, against **4%** for every other offer.
2. **100%** of Werribee's open Christmas shifts could be taken by one of its own casuals staying on from a rostered shift that ends as the open shift starts or starts as it ends, the module's checks passed (Box Hill **96%**, Altona **79%**), against **0%** of Camberwell's.
3. Camberwell's 215 open shifts carry **1,090** paid hours to the nearest 10.

## 3. Step-by-Step Solution

1. Summed the paid hours (less the unpaid meal break on shifts over five hours, per ea_2024_casual_employment_summary.pdf) of the OPEN lines on each sheet of christmas_roster_2026_published.xlsx: Werribee 3,250 hours, Box Hill 2,600, Altona 1,770, Camberwell 1,090.
2. Joined every offer in callin_offers_20250829_20261112.csv to the casual's roster lines that day (person code to payroll number through kws_people_20261112.csv and the previous numbers in payroll_casual_register_20261112.csv; both roster exports, less lines callin_register_20250829_20261112.csv shows vacated, plus call-ins the casual had accepted): 2,241 offers carried on from the casual's own shift at the store and 32% of them were accepted, against 4% of the other 153,829.
3. Fitted a logit of each offer's acceptance on that term and on another shift the same day, a Sunday shift, the shift's paid hours, finishing after 21:30, starting before 07:00, under four hours' notice, an offer repeated, a sister-store offer, rostered hours over 10 that week, the Christmas weeks, the casual's age band and home store.
4. Ran the fitted choice through the offer order, eligibility checks and offer hours in kws_callin_module_notes.pdf over the published Christmas rosters, every store's open shifts posted at 09:00 on 16 November with the crew at no store (relief_crew_placement_standard.pdf, section 4), 24 runs: call-ins would leave more of Camberwell's open hours unworked than of any other store's, well clear of the next store.
5. Placed the crew at Camberwell under section 3 of the standard; its crew hours under section 5 are the paid hours of Camberwell's open shifts: 1,090.

## 4. Deliverable Answers

### relief_crew_placement_xmas2026.pdf

1. The placement in the opening sentence: the relief crew to Camberwell, 1,090 crew hours.
2. A horizontal bar chart of every store's forecast unworked hours, largest first, Camberwell highlighted, each bar labelled, titled with the finding.

### relief_crew_xmas2026.xlsx

1. Last Christmas's call-ins, 28 November to 24 December 2025, paid hours: put out to call-in, covered, left uncovered:
   - Altona: 1,615.0, 843.0, 772.0
   - Ballarat: 2,262.0, 964.5, 1,297.5
   - Box Hill: 2,072.0, 1,266.5, 805.5
   - Camberwell: 2,140.5, 1,578.0, 562.5
   - Ringwood: 1,695.5, 1,002.5, 693.0
   - Sunshine: 2,023.0, 1,125.0, 898.0
   - Werribee: 299.0, 98.5, 200.5
   - Williamstown: 1,441.5, 605.0, 836.5
2. Cover across stores in those weeks, paid hours: the store's call-ins covered by casuals from other stores; its own casuals' cover at other stores:
   - Altona: 44.0; 4.0
   - Ballarat: 0.0; 0.0
   - Box Hill: 33.5; 90.0
   - Camberwell: 65.5; 54.0
   - Ringwood: 83.0; 38.0
   - Sunshine: 34.5; 32.0
   - Werribee: 0.0; 27.5
   - Williamstown: 24.0; 39.0
