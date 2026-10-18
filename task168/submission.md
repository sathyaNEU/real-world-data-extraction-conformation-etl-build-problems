## Tags

**Domain:** Urban & Regional Science (forecasting: an airline's passengers carried on nine Linate routes after a gauge change, each sold-out departure's demand completed from the booking build of its own month).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**The nine Linate routes will carry about 175,000 more passengers in summer 2026 than they carried in summer 2025.** 6,418 of their 7,560 summer 2025 departures sold out, so each sold-out departure's demand is its seats over the share of final bookings that departures of its own month which never sold out held when it sold out; re-flown at summer 2026's seats less no-shows, that demand puts about 175,000 more passengers into the 620,224 seats added. Not the 2025 gauge changes' 0.80 extra passengers per extra seat carried onto this one, about 500,000: those changes added 22 to 29 per cent to the seats of routes whose demand still filled most of them, while summer 2025's demand on the nine routes exceeds the A321neo's 232 seats on almost no departure. Not a booking build pooled over the summer, about 230,000, nor one from the nine routes' own departures that never sold out, about 270,000: both are weighted to spring and autumn departures, whose passengers book a few weeks out, so they read every July and August departure as further from its final bookings than it was. Not a normal EM on the final bookings, which reads the demand above the seats from the few departures that did not sell out and falls well short of it on the other routes' departures censored as deeply.

## 2. Critical Components

1. Summer 2025 passengers carried on the nine routes: **1,044,148**.
2. Summer 2025 departures on the nine routes that sold out: **6,418** of **7,560**.

## 3. Step-by-Step Solution

1. Took summer 2025 passengers carried from dcs_flight_close_s25.csv (pax_flown, lap infants and no-shows excluded per section 4 of planning_basis_NP-PB-26S_issue2.pdf): 1,044,148 on the nine routes.
2. In rm_booking_build_s25.csv, 6,418 of the nine routes' 7,560 summer 2025 departures carry a sold_out_utc, so their bookings stop at the seats.
3. From the summer 2025 departures off the nine routes that never sold out, built each departure month's mean share of final bookings on hand at every snapshot; censored at 85 per cent of their final bookings, those departures are recovered within 1 per cent in every month by their own month's build, while builds over coarser groups of months (peak against shoulder, or three or four periods) miss some month by 3 per cent or more and the build pooled over the summer puts July and August more than 10 per cent too high.
4. Censored instead so that each route direction's month holds the nine routes' sold-out share of that month at the cap (98 per cent in August), the month build overstates the demand above the cap by under a tenth in every month, while a normal EM on each route direction and month's final bookings falls short of it in every month from June to September, by about a fifth over the summer and by about half in August.
5. Completed each sold-out departure on the nine routes as its seats over its month's share on hand at its sold_out_utc.
6. Re-flew every summer 2025 departure 364 days later at its seats in summer2026_capacity_plan_v3.xlsx (232 on the A321neo, 144 on the A319 that Brindisi and Lamezia Terme keep to 31 May 2026), its bookings capped at the seats (section 5), less its route direction's summer 2025 no-show share from dcs_flight_close_s25.csv.
7. Against summer 2025's 1,044,148 passengers carried, the nine routes carry about 175,000 more, to the nearest 25,000.
8. Counted the turned-away passengers in booking_engine_refusals_s25.csv from requests logged at or after the departure's sold_out_utc, each website or app session, call or booking reference once per departure at its pax, each request's route and direction taken from its flight_no and dep_date in rm_booking_build_s25.csv.

## 4. Deliverable Answers

### summer2026_upgauge_forecast.xlsx

1. Additional passengers carried on the nine routes, summer 2026 over summer 2025: 175,000.
2. Passengers the booking engines turned away from summer 2025 departures because the flight was full, by route and direction:
   - LIN-CTA: 4,760
   - CTA-LIN: 4,374
   - LIN-PMO: 4,173
   - PMO-LIN: 4,063
   - LIN-NAP: 2,349
   - NAP-LIN: 2,264
   - LIN-BRI: 2,731
   - BRI-LIN: 2,676
   - LIN-BDS: 2,959
   - BDS-LIN: 2,749
   - LIN-SUF: 2,644
   - SUF-LIN: 2,554
   - LIN-REG: 1,609
   - REG-LIN: 1,711
   - LIN-CAG: 2,902
   - CAG-LIN: 2,737
   - LIN-TPS: 1,661
   - TPS-LIN: 1,716

### summer2025_turnaways.pptx

1. One slide charting the counts in answer 2 above, a bar for each route and direction, each bar labelled with its count.
