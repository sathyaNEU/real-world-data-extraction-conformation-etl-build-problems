## Tags

**Domain:** Urban & Regional Science (network analysis).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**The 2027 to 2031 plan should name Wrenfold and Pelmarsh, the only districts whose 2026 cover fell below the 75 per cent line.**
Wrenfold's cover was 73 per cent and Pelmarsh's 73 per cent. Not Altmoor and Skirwold, at 77 and 77 per cent: cover read from each engine's own station leaves out the Calderstow engines that stood by at their on-call stations. Not Tollesham, the nearest above the line at 78 per cent.

## 2. Critical Components

1. Wrenfold's 2026 cover is **73 per cent**
2. Pelmarsh's 2026 cover is **73 per cent**
3. Altmoor's and Skirwold's 2026 cover are **77 per cent** and **77 per cent**

## 3. Step-by-Step Solution

1. Took the homes as the addresses classed RD in address_register_extract.csv, each in the district of its output area per output_area_lookup.xlsx, and placed each at its nearest node of routing_network_nodes.csv.
2. Timed drives over routing_network_links.csv (drive_time_s, one-way links one way only) and added two minutes' turnout for wholetime-crewed and five for on-call-crewed engines per fleet_and_stations_2026.xlsx.
3. Read each engine free at the start of a minute when its latest Status row in mobilising_resource_log_2026.csv at or before that minute had code 1 (Available).
4. Placed each engine each minute at its station unless the same log had it out of base, after a Left base row and before the next Arrived base row; then at the node nearest its latest location row.
5. Counted a home covered when a free engine's turnout and drive to it took ten minutes or less, and averaged each district's covered share over the 525,600 minutes of 2026: Calderstow 84 per cent, Tollesham 78 per cent, Wrenfold 73 per cent, Hollinbury 80 per cent, Pelmarsh 73 per cent, Altmoor 77 per cent, Skirwold 77 per cent.
6. For each on-call station in Altmoor and Skirwold, counted the minutes its engine was at status 8 while four or more of its firefighters were booked in oncall_availability_bookings_2026.csv, a later-entered booking replacing the same firefighter's earlier booking it overlaps, and of those the minutes with no crew or watch commander booked, by role on the day per oncall_crew_register_2026.xlsx.
7. Counted incidents in incident_records_2022_2026.csv classified A01 or FAA at addresses classed C, a record whose call came before the closing time of an earlier record at the same premises being the same actuation, by district of the address, and per 100 addresses classed C.
8. Named the districts below 75 per cent on unrounded cover: Wrenfold and Pelmarsh.

## 4. Deliverable Answers

### district_fire_cover_2026.xlsx

1. Each district's 2026 cover and whether it is named, whole per cent:
   - Calderstow: 84 per cent, not named
   - Tollesham: 78 per cent, not named
   - Wrenfold: 73 per cent, named
   - Hollinbury: 80 per cent, not named
   - Pelmarsh: 73 per cent, named
   - Altmoor: 77 per cent, not named
   - Skirwold: 77 per cent, not named
2. Each on-call station in Altmoor and Skirwold, time in 2026 off the run with four or more firefighters booked, and of that time with no crew commander or watch commander booked, in hours and minutes:
   - Thornstead: 211 hours 18 minutes; 182 hours 30 minutes
   - Fernmere: 764 hours 55 minutes; 632 hours 5 minutes
   - Kescombe: 512 hours 30 minutes; 459 hours 45 minutes
   - Foxmoor: 588 hours 47 minutes; 280 hours 30 minutes
   - Nedbeck: 207 hours 55 minutes; 131 hours 15 minutes
   - Langgarth: 809 hours 8 minutes; 353 hours 44 minutes
   - Ludwold: 219 hours 1 minute; 166 hours 30 minutes
   - Kelmoor: 401 hours 7 minutes; 362 hours 0 minutes
3. Each district's actuations of fire alarm apparatus at non-domestic premises that brought engines out to a false alarm, 2022 to 2026, and per 100 non-domestic premises, one decimal:
   - Calderstow: 2632 actuations, 62.1 per 100 premises
   - Tollesham: 874 actuations, 66.9 per 100 premises
   - Wrenfold: 762 actuations, 63.2 per 100 premises
   - Hollinbury: 769 actuations, 59.2 per 100 premises
   - Pelmarsh: 714 actuations, 59.0 per 100 premises
   - Altmoor: 371 actuations, 63.4 per 100 premises
   - Skirwold: 375 actuations, 62.9 per 100 premises

### district_fire_cover_2026.png

1. A dot for each district's 2026 cover in whole per cent against a marked 75 per cent line, Wrenfold and Pelmarsh highlighted as named.
