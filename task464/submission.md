## Tags
**Domain:** Healthcare delivery and health economics (payment, claims and health plan analytics).
**Analytical objective:** Data extraction and conformation (ETL).

## 1. Final Recommendation
**The 2027 outpatient dialysis and infusion network holds 3,886 weekly treatment slots, and six of the twelve service areas sit below the adequacy standard.**
Network slots are 3,886 against 3,568 required across the twelve areas, and Hesper Vale is the nearest of the six to the standard, 20 slots short. Not the stations the directory attests, which are 327 against 274 deliverable positions and put three of those six areas above the standard. Not the stations the state licence lists, which are higher again. Not each site's busiest week in the record, which measures demand and leaves 8 of the twelve areas short.

## 2. Critical Components
1. Deliverable treatment positions across the forty sites in scope are **274**, against **327** attested stations
2. Projected 2027 weekly treatment demand across the twelve areas is **3,095** treatments
3. The weekly treatment slots the standard requires across the twelve areas are **3,568**

## 3. Step-by-Step Solution
1. Took the sites carrying a 2027 contract intent on the attestation cycle current at the network position date in provider_directory_2027.csv: forty sites in twelve service areas.
2. Counted the treatment sessions each site's roster staffs in a week from staffing_roster_2026q4.csv, and the treatments a position delivers in a session from Schedule 4 clause 4.2.
3. Rebuilt each treatment's service interval from both tables of treatment_encounters.db, the 2023 and 2024 table carrying a stop time and the 2025 and 2026 table a length in minutes, and took each site's deliverable treatment positions as the greatest number of its own treatments running at one time over the four-year record: 274 positions against 327 attested stations.
4. Multiplied each site's positions by its sessions a week and by its category figure, as Schedule 4 clause 4.2 sets the unit: 3,886 weekly treatment slots for the network.
5. Took each area's 2026 contract year treatments a week from the same extract and grew them by the area's factor in enrolment_projection_2027.csv, then applied the 1.15 cushion and rounded each area up to the next whole slot as clause 4.4 requires: 3,095 treatments a week projected and 3,568 weekly slots required.
6. Counted the out-of-network treatments a claim at a time from out_of_network_payments_2026.csv with out_of_network_payments_runout_2027q1.csv, taking a claim's header line as its own treatment count where the register writes one and its service lines where it does not: 48 figures on the Out of Network 2026 sheet.
7. Took the state_licence_register.xlsx facility row covering the position date for each licence number, corporate rows excluded, for the licensed supply, and the row covering the 2026 filing's own position date to resolve each distinct site in state_adequacy_filing_2026.xlsx: 24 and 24 figures.
8. Compared each area's slots with its required figure: 6 of the twelve areas sit below the standard and the network holds 3,886 weekly treatment slots.

## 4. Deliverable Answers

### outpatient_capacity_2027.csv
1. Weekly treatment slots, forty rows in the file's order, whole slots:
   - PS-10404, Granleigh: 80
   - PS-10556, Granleigh: 80
   - PS-10682, Granleigh: 126
   - PS-10787, Granleigh: 40
   - PS-10803, Lowenbrook: 96
   - PS-10975, Lowenbrook: 120
   - PS-11153, Lowenbrook: 96
   - PS-11290, Ammerly: 40
   - PS-11491, Ammerly: 150
   - PS-11515, Ammerly: 96
   - PS-11650, Ammerly: 80
   - PS-11685, Hesper Vale: 40
   - PS-11912, Hesper Vale: 50
   - PS-11977, Hesper Vale: 80
   - PS-11992, Crannock: 126
   - PS-12060, Crannock: 96
   - PS-12122, Crannock: 80
   - PS-12285, Innsmere: 80
   - PS-12488, Innsmere: 144
   - PS-12630, Innsmere: 40
   - PS-12846, Innsmere: 96
   - PS-12899, Bexhollow: 108
   - PS-13100, Bexhollow: 96
   - PS-13158, Bexhollow: 108
   - PS-13209, Kettlebrook: 80
   - PS-13429, Kettlebrook: 80
   - PS-13569, Kettlebrook: 105
   - PS-13795, Eastmoor Reach: 120
   - PS-13828, Eastmoor Reach: 120
   - PS-13939, Eastmoor Reach: 50
   - PS-14074, Eastmoor Reach: 96
   - PS-14191, Durnsfield: 120
   - PS-14258, Durnsfield: 126
   - PS-14433, Durnsfield: 150
   - PS-14479, Jarrowmead: 162
   - PS-14583, Jarrowmead: 180
   - PS-14631, Jarrowmead: 144
   - PS-14653, Fallowbray: 105
   - PS-14822, Fallowbray: 40
   - PS-14888, Fallowbray: 60

### area_capacity_2027.xlsx
2. Area Capacity, the twelve areas in the sheet's order, whole slots:
   - Granleigh: 326 slots, 245 required, meets the standard yes
   - Lowenbrook: 312 slots, 335 required, meets the standard no, 23 slots short
   - Ammerly: 366 slots, 271 required, meets the standard yes
   - Hesper Vale: 170 slots, 190 required, meets the standard no, 20 slots short
   - Crannock: 302 slots, 239 required, meets the standard yes
   - Innsmere: 360 slots, 260 required, meets the standard yes
   - Bexhollow: 312 slots, 335 required, meets the standard no, 23 slots short
   - Kettlebrook: 265 slots, 207 required, meets the standard yes
   - Eastmoor Reach: 386 slots, 434 required, meets the standard no, 48 slots short
   - Durnsfield: 396 slots, 302 required, meets the standard yes
   - Jarrowmead: 486 slots, 521 required, meets the standard no, 35 slots short
   - Fallowbray: 205 slots, 229 required, meets the standard no, 24 slots short
3. Nearest the standard without meeting it: Hesper Vale, 20 slots short.
4. Out of Network 2026, twelve areas by half, whole treatments and shares to one decimal:
   - Granleigh, H1: 572 treatments, 9.7 per cent
   - Granleigh, H2: 559 treatments, 9.8 per cent
   - Lowenbrook, H1: 234 treatments, 3.2 per cent
   - Lowenbrook, H2: 229 treatments, 3.3 per cent
   - Ammerly, H1: 650 treatments, 10.1 per cent
   - Ammerly, H2: 638 treatments, 10.2 per cent
   - Hesper Vale, H1: 234 treatments, 5.4 per cent
   - Hesper Vale, H2: 228 treatments, 5.4 per cent
   - Crannock, H1: 546 treatments, 9.4 per cent
   - Crannock, H2: 535 treatments, 9.5 per cent
   - Innsmere, H1: 806 treatments, 12.8 per cent
   - Innsmere, H2: 790 treatments, 12.9 per cent
   - Bexhollow, H1: 468 treatments, 6.3 per cent
   - Bexhollow, H2: 457 treatments, 6.3 per cent
   - Kettlebrook, H1: 494 treatments, 9.9 per cent
   - Kettlebrook, H2: 484 treatments, 10.1 per cent
   - Eastmoor Reach, H1: 338 treatments, 3.6 per cent
   - Eastmoor Reach, H2: 329 treatments, 3.6 per cent
   - Durnsfield, H1: 364 treatments, 5.2 per cent
   - Durnsfield, H2: 357 treatments, 5.3 per cent
   - Jarrowmead, H1: 520 treatments, 4.5 per cent
   - Jarrowmead, H2: 510 treatments, 4.5 per cent
   - Fallowbray, H1: 676 treatments, 12.1 per cent
   - Fallowbray, H2: 664 treatments, 12.3 per cent
5. Licensed Supply, twelve areas, whole sites and stations:
   - Granleigh: 7 sites, 43 stations
   - Lowenbrook: 6 sites, 62 stations
   - Ammerly: 7 sites, 54 stations
   - Hesper Vale: 6 sites, 39 stations
   - Crannock: 5 sites, 51 stations
   - Innsmere: 8 sites, 66 stations
   - Bexhollow: 5 sites, 50 stations
   - Kettlebrook: 6 sites, 38 stations
   - Eastmoor Reach: 6 sites, 36 stations
   - Durnsfield: 6 sites, 59 stations
   - Jarrowmead: 5 sites, 55 stations
   - Fallowbray: 5 sites, 38 stations
6. Sites Dropped, twelve areas, whole sites and stations:
   - Granleigh: 2 sites, 15 stations
   - Lowenbrook: 1 sites, 8 stations
   - Ammerly: 1 sites, 10 stations
   - Hesper Vale: 1 sites, 5 stations
   - Crannock: 1 sites, 12 stations
   - Innsmere: 2 sites, 16 stations
   - Bexhollow: 1 sites, 6 stations
   - Kettlebrook: 1 sites, 5 stations
   - Eastmoor Reach: 1 sites, 6 stations
   - Durnsfield: 1 sites, 8 stations
   - Jarrowmead: 1 sites, 6 stations
   - Fallowbray: 1 sites, 8 stations
7. Bar chart of weekly treatment slots against the required figure on the Area Capacity sheet, the six areas below the standard carrying their shortfall in the sheet's own shortfall column.
