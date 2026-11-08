## Tags

**Domain:** Urban & Regional Science (optimization: siting one platform dispatch team on a rail network).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**Site the 2027 platform dispatch team at Pellingham: it takes 4,100 passenger-minutes of lateness a weekday off the network's trains, 1,200 more than Saltgate's 2,900.** Not Saltgate, which removes the most overrun minutes on its own trains but whose units turn round with time to spare and pass almost none of it on; not Ambrey Parkway, whose longest dwells fall on the park-and-ride extras, whose units do not work again until the evening.

## 2. Critical Components

1. Pellingham saves **4,100** passenger-minutes per weekday across the network's weekday trains
2. Saltgate saves **2,900** passenger-minutes per weekday
3. The other shortlisted stations save Brathwick Road **1,700**, Ambrey Parkway **1,600**, Holcroft Green **400**, Ostley Lane **400**

## 3. Step-by-Step Solution

1. Took the valuation from dispatch_team_brief_2027.docx section 3: passenger lateness on every weekday passenger train on the 60 autumn 2026 weekdays as they ran, each passenger's minutes after the booked arrival where they leave the train, with the team removing three fifths of each train's dwell over its booked dwell at its station for trains booked to depart there from 06:30 up to 19:30.
2. Joined each weekday's calls in train_running_autumn_2026.csv to working_timetable_autumn_2026.xlsx on headcode and TIPLOC, and weighted each train's arrival lateness at every station by its alighters in passenger_census_2026-10-13.csv, matched through station_register.csv.
3. Replayed each weekday with the team at each shortlisted station in turn: a train leaves that station earlier by three fifths of its overrun but never before its booked departure, keeps every later section's recorded running time, and leaves each later station at its booked time or its replayed arrival plus the dwell it recorded, whichever is later.
4. Followed each unit through its day by the running record's unit numbers: no working that left its origin late left sooner than four minutes after its unit's arrival, so a working that left late exactly four minutes after that arrival leaves four minutes after the unit's replayed arrival instead, not before its booked time, and the unit's later workings are replayed the same way.
5. Averaged the passenger lateness taken off over the 60 weekdays: Pellingham 4,100, Saltgate 2,900, Brathwick Road 1,700, Ambrey Parkway 1,600, Holcroft Green 400, Ostley Lane 400.
6. Gateline ask: differenced each array's cumulative counters in gateline_readings_2026-10-12_to_16.csv over 13 October 2026 in BST, adding 65,536 across a wrap, resuming a restarted controller from the 02:00 reading it restored, and counting a tidal array's entries-counter passages in its exit-only hours as people leaving.
7. Delay Repay ask: summed every approved payment row in delay_repay_claims_extract_2027-01-15.csv for journeys to or from RVC, appeal top-ups under the same claim_ref included; matched each claim to the train leaving its stated origin at its booked departure and calling at its destination, or the other way round where none does (a return ticket's claim names the ticket's stations); dated a claim whose journey date is the day it was first submitted, and whose train did not reach the destination 15 minutes late that day, by the last earlier weekday its train did; kept the weekdays from 7 September to 27 November 2026 and banded each claim by its train's lateness at the destination in the running record.
8. Pellingham gets the team: 4,100 passenger-minutes a weekday, 1,200 ahead of Saltgate.

## 4. Deliverable Answers

### dispatch_team_siting_2027.xlsx

1. Weekday saving by shortlisted station, passenger-minutes to the nearest 100:
   - Pellingham: 4,100
   - Saltgate: 2,900
   - Brathwick Road: 1,700
   - Ambrey Parkway: 1,600
   - Holcroft Green: 400
   - Ostley Lane: 400
2. Pick Pellingham (4,100); runner-up Saltgate (2,900); gap 1,200 passenger-minutes.
3. Passengers through the gates at each gated shortlisted station on Tuesday 13 October 2026:
   - Brathwick Road: entered 1,974; left 2,054
   - Ambrey Parkway: entered 1,968; left 2,337
   - Pellingham: entered 2,055; left 3,757
   - Saltgate: entered 2,543; left 2,633
4. Delay Repay compensation paid, weekday journeys to or from Ravelstoke Central, 7 September to 27 November 2026, pounds:
   - Crossmoor line: 15 to 29 minutes £109; 30 to 59 minutes £150; 60 minutes or more £586
   - Ambrey line: 15 to 29 minutes £114; 30 to 59 minutes £213; 60 minutes or more £301
   - Holm Ferry line: 15 to 29 minutes £209; 30 to 59 minutes £207; 60 minutes or more £116

### lateness_saved_by_station.png

5. Ranked horizontal bar chart of every shortlisted station's weekday saving, Pellingham highlighted at the top.
