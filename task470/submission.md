## Tags

**Domain:** Physical & Environmental Sciences (emissions inventory: airport lead inventory built from an ADS-B receiver network's operations, the FAA aircraft register, tower and commissioned counts and the state's based aircraft list, the operations the network cannot see estimated from the airplanes that never broadcast).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Seven of the 24 fields without a tower qualify for the 2027 round: Thornacre Regional (T13), Ambrell County Airport (A71), Lanthorne Field (L08), Umber Creek Airport (U44), Wickrow Airfield (W33), Orrin Flats Airport (O16) and Fennick Airpark (F37).**
Their 2026 lead from piston-engine aircraft runs from 14 to 22 kg against the round's 12.5 kg; the highest field below the line, Pellow Municipal, has 11 kg. Not the eight fields one capture rate gives (the counted fields' 82 per cent applied to every field's recorded operations, which adds Kestrel Ridge Airpark, Pellow Municipal, Saltry Field and Tavish Aero Field and drops Orrin Flats Airport, Umber Creek Airport and Wickrow Airfield), because the operations the network misses belong to the airplanes that never broadcast, few at the flight-school fields and many at the vintage ones; not the nine fields a capture rate split by flight training gives (86 per cent and 73 per cent, which adds Kestrel Ridge Airpark, Norwick Field, Pellow Municipal, Saltry Field and Tavish Aero Field).

## 2. Critical Components

1. Operations the network did not record at the ten counted fields: **23,376**, against **338** based piston airplanes there that the network never recorded in 2026: **69.2** operations a never-recorded airplane.
2. Based piston airplanes the network never recorded in 2026 at the 20 fields without a count: T13 **33**, A71 **26**, U44 **65**, W33 **58**, O16 **62**, P05 **1**, S27 **0**, K58 **2**, T61 **1**, N26 **9**, H52 **11**, W85 **18**, C66 **11**, Y02 **22**, Z14 **8**, L29 **9**, M09 **8**, R31 **4**, B48 **5** and D73 **3**.
3. Lead of the qualifying fields, 2026: T13 **22 kg**, A71 **21 kg**, L08 **16 kg**, U44 **15 kg**, W33 **14 kg**, O16 **14 kg** and F37 **14 kg**.

## 3. Step-by-Step Solution

1. Read adsb_field_events_20251230_20270102.csv with times from UTC to Pacific time, kept 2026, and gave each event its aircraft through icao24 and MASTER.txt or, for a registration cancelled during 2026, DEREG.txt by its issue and cancel dates; priced each piston-engine operation by ACFTREF.txt's engines and Table 1 of cvaqd_aircraft_lead_inventory_method_rev3.pdf, a touch-and-go two operations.
2. At the six towers, took atct_daily_operations_2026.csv's civil operations less the civil events the network recorded in the tower hours of state_airport_directory_2026.xlsx (method 4.2); at the four count fields, the studies' piston-engine operations less those recorded (method 4.3).
3. Matched state_based_aircraft_validation_2027.xlsx's N-numbers, written four ways, to the register and found the based piston airplanes whose addresses the network never recorded in 2026.
4. Divided the counted fields' unrecorded operations by their never-recorded airplanes: 69.2 operations an airplane.
5. At each field without a count, priced 69.2 operations for each never-recorded airplane at 1.625 g (method 3.2 and 4.4) and added the recorded lead.
6. Compared each field's 2026 lead with the 12.5 kg of the round's guidelines (section 2.2): seven qualify.
7. Built the towered fields' piston operations and lead the same way, each recorded operation assigned to the aircraft that held its address that day and each tower's unrecorded civil operations taken as piston-engine operations (method 4.2).
8. Recommended the seven fields for the 2027 round.

## 4. Deliverable Answers

### corrisan_2026_field_piston_lead.csv

1. Lead from piston-engine aircraft, 2026, each field without a tower:
   - Thornacre Regional (T13): 22 kg
   - Ambrell County Airport (A71): 21 kg
   - Lanthorne Field (L08): 16 kg
   - Umber Creek Airport (U44): 15 kg
   - Wickrow Airfield (W33): 14 kg
   - Orrin Flats Airport (O16): 14 kg
   - Fennick Airpark (F37): 14 kg
   - Pellow Municipal (P05): 11 kg
   - Saltry Field (S27): 11 kg
   - Kestrel Ridge Airpark (K58): 11 kg
   - Tavish Aero Field (T61): 11 kg
   - Graylow Municipal (G42): 10 kg
   - Norwick Field (N26): 10 kg
   - Hollin Gap Airport (H52): 9 kg
   - Dunmarsh Airport (D19): 9 kg
   - Wenmore Airport (W85): 9 kg
   - Cobbett Airport (C66): 8 kg
   - Yarrow Bend Strip (Y02): 6 kg
   - Zellner Field (Z14): 6 kg
   - Lissom Field (L29): 6 kg
   - Marsh Hollow Field (M09): 4 kg
   - Ravelle Field (R31): 4 kg
   - Brannoch Airstrip (B48): 3 kg
   - Dellow Strip (D73): 2 kg

### cvaqd_2027_unleaded_grant_qualification.docx

1. Qualifying fields, 2026 lead:
   - Thornacre Regional (T13): 22 kg
   - Ambrell County Airport (A71): 21 kg
   - Lanthorne Field (L08): 16 kg
   - Umber Creek Airport (U44): 15 kg
   - Wickrow Airfield (W33): 14 kg
   - Orrin Flats Airport (O16): 14 kg
   - Fennick Airpark (F37): 14 kg
2. Bar chart of the 24 fields' 2026 lead against the round's 12.5 kg threshold, the qualifying fields highlighted.
3. Towered fields, 2026 piston-engine operations and lead:
   - Halwick Municipal (HWK): 17,600 operations, 22 kg
   - Corrisan Valley Regional (CRV): 9,900 operations, 18 kg
   - Ostrey Field (OSY): 19,400 operations, 23 kg
   - Varnell County Airport (VNL): 12,200 operations, 16 kg
   - Kesterly Field (KTY): 13,600 operations, 16 kg
   - Dunmore Municipal (DMR): 7,900 operations, 13 kg
