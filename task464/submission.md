## Tags
**Domain:** Healthcare delivery and health economics (payment, claims and health plan analytics).
**Analytical objective:** Data extraction and conformation (ETL).

## 1. Final Recommendation
**The 2027 outpatient dialysis and infusion network holds 3,886 weekly treatment slots, and six of the twelve service areas sit below the adequacy standard.**
Network slots are 3,886 against 3,568 required across the twelve areas, and Durnsfield is the nearest of the six to the standard, 20 slots short. Not the stations the directory attests, which are 327 against 274 deliverable positions and put three of those six areas above the standard. Not the stations the state licence lists, which are higher again. Not each site's busiest week in the record, which measures demand and leaves 8 of the twelve areas short.

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
   - PS-10437, Ammerly: 80
   - PS-10474, Ammerly: 80
   - PS-10511, Ammerly: 126
   - PS-10548, Ammerly: 40
   - PS-10585, Bexhollow: 96
   - PS-10622, Bexhollow: 120
   - PS-10659, Bexhollow: 96
   - PS-10696, Crannock: 40
   - PS-10733, Crannock: 150
   - PS-10770, Crannock: 96
   - PS-10807, Crannock: 80
   - PS-10844, Durnsfield: 40
   - PS-10881, Durnsfield: 50
   - PS-10918, Durnsfield: 80
   - PS-10955, Eastmoor Reach: 126
   - PS-10992, Eastmoor Reach: 96
   - PS-11029, Eastmoor Reach: 80
   - PS-11066, Fallowbray: 80
   - PS-11103, Fallowbray: 144
   - PS-11140, Fallowbray: 40
   - PS-11177, Fallowbray: 96
   - PS-11214, Granleigh: 108
   - PS-11251, Granleigh: 96
   - PS-11288, Granleigh: 108
   - PS-11325, Hesper Vale: 80
   - PS-11362, Hesper Vale: 80
   - PS-11399, Hesper Vale: 105
   - PS-11436, Innsmere: 120
   - PS-11473, Innsmere: 120
   - PS-11510, Innsmere: 50
   - PS-11547, Innsmere: 96
   - PS-11584, Jarrowmead: 120
   - PS-11621, Jarrowmead: 126
   - PS-11658, Jarrowmead: 150
   - PS-11695, Kettlebrook: 162
   - PS-11732, Kettlebrook: 180
   - PS-11769, Kettlebrook: 144
   - PS-11806, Lowenbrook: 105
   - PS-11843, Lowenbrook: 40
   - PS-11880, Lowenbrook: 60

### area_capacity_2027.xlsx
2. Area Capacity, the twelve areas in the sheet's order, whole slots:
   - Ammerly: 326 slots, 245 required, meets the standard yes
   - Bexhollow: 312 slots, 335 required, meets the standard no, 23 slots short
   - Crannock: 366 slots, 271 required, meets the standard yes
   - Durnsfield: 170 slots, 190 required, meets the standard no, 20 slots short
   - Eastmoor Reach: 302 slots, 239 required, meets the standard yes
   - Fallowbray: 360 slots, 260 required, meets the standard yes
   - Granleigh: 312 slots, 335 required, meets the standard no, 23 slots short
   - Hesper Vale: 265 slots, 207 required, meets the standard yes
   - Innsmere: 386 slots, 434 required, meets the standard no, 48 slots short
   - Jarrowmead: 396 slots, 302 required, meets the standard yes
   - Kettlebrook: 486 slots, 521 required, meets the standard no, 35 slots short
   - Lowenbrook: 205 slots, 229 required, meets the standard no, 24 slots short
3. Nearest the standard without meeting it: Durnsfield, 20 slots short.
4. Out of Network 2026, twelve areas by half, whole treatments and shares to one decimal:
   - Ammerly, H1: 572 treatments, 9.7 per cent
   - Ammerly, H2: 559 treatments, 9.8 per cent
   - Bexhollow, H1: 234 treatments, 3.2 per cent
   - Bexhollow, H2: 229 treatments, 3.3 per cent
   - Crannock, H1: 650 treatments, 10.1 per cent
   - Crannock, H2: 638 treatments, 10.2 per cent
   - Durnsfield, H1: 234 treatments, 5.4 per cent
   - Durnsfield, H2: 228 treatments, 5.4 per cent
   - Eastmoor Reach, H1: 546 treatments, 9.4 per cent
   - Eastmoor Reach, H2: 535 treatments, 9.5 per cent
   - Fallowbray, H1: 806 treatments, 12.8 per cent
   - Fallowbray, H2: 790 treatments, 12.9 per cent
   - Granleigh, H1: 468 treatments, 6.3 per cent
   - Granleigh, H2: 457 treatments, 6.3 per cent
   - Hesper Vale, H1: 494 treatments, 9.9 per cent
   - Hesper Vale, H2: 484 treatments, 10.1 per cent
   - Innsmere, H1: 338 treatments, 3.6 per cent
   - Innsmere, H2: 329 treatments, 3.6 per cent
   - Jarrowmead, H1: 364 treatments, 5.2 per cent
   - Jarrowmead, H2: 357 treatments, 5.3 per cent
   - Kettlebrook, H1: 520 treatments, 4.5 per cent
   - Kettlebrook, H2: 510 treatments, 4.5 per cent
   - Lowenbrook, H1: 676 treatments, 12.1 per cent
   - Lowenbrook, H2: 664 treatments, 12.3 per cent
5. Licensed Supply, twelve areas, whole sites and stations:
   - Ammerly: 7 sites, 43 stations
   - Bexhollow: 6 sites, 62 stations
   - Crannock: 7 sites, 54 stations
   - Durnsfield: 6 sites, 39 stations
   - Eastmoor Reach: 5 sites, 51 stations
   - Fallowbray: 8 sites, 66 stations
   - Granleigh: 5 sites, 50 stations
   - Hesper Vale: 6 sites, 38 stations
   - Innsmere: 6 sites, 36 stations
   - Jarrowmead: 6 sites, 59 stations
   - Kettlebrook: 5 sites, 55 stations
   - Lowenbrook: 5 sites, 38 stations
6. Sites Dropped, twelve areas, whole sites and stations:
   - Ammerly: 2 sites, 15 stations
   - Bexhollow: 1 sites, 8 stations
   - Crannock: 1 sites, 10 stations
   - Durnsfield: 1 sites, 5 stations
   - Eastmoor Reach: 1 sites, 12 stations
   - Fallowbray: 2 sites, 16 stations
   - Granleigh: 1 sites, 6 stations
   - Hesper Vale: 1 sites, 5 stations
   - Innsmere: 1 sites, 6 stations
   - Jarrowmead: 1 sites, 8 stations
   - Kettlebrook: 1 sites, 6 stations
   - Lowenbrook: 1 sites, 8 stations
7. Bar chart of weekly treatment slots against the required figure on the Area Capacity sheet, the six areas below the standard carrying their shortfall in the sheet's own shortfall column.
