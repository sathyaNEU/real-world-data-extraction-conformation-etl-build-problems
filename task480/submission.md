## Tags

**Domain:** Physical & Environmental Sciences (emissions inventory: the 2027 NOx of a nonattainment area's older gasoline vehicles by county, conformed from the registration snapshot, the inspection program's test records, its station licences and the model-year rate table, each vehicle's 2027 miles estimated from its one odometer reading).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Hold 2027 Vehicle Retirement Program intake events in the five counties whose eligible vehicles will emit 10 short tons of NOx or more in 2027: Wexmoor, Halvering, Linnmere, Elkhollow and Marlbank.**
Marlbank, the designated county nearest the line, comes to 11 tons and Dunmarsh, the nearest below it, to 9. Not the nine counties the odometer reading divided by the vehicle's age files, which averages every year a car has been driven and overstates what an old car travels now. Not Dunmarsh, Halvering, Linnmere and Wexmoor, which the area's mileage by age without each vehicle's own reading gives, dropping the long-distance drivers of Elkhollow and Marlbank and adding Dunmarsh.

## 2. Critical Components

1. Marlbank's eligible vehicles' 2027 NOx: **11 short tons**.
2. Dunmarsh's eligible vehicles' 2027 NOx: **9 short tons**.
3. Counties at 10 tons or more: **5**.

## 3. Step-by-Step Solution

1. Took the eligible vehicles from vehicle_registrations_2026-07-01.csv under guidelines 2.1 (ACTIVE in a member county, model year 2005 to 2014, fuel code G or F, GVWR class 1 or 2a): 65,305 vehicles.
2. Gave each its reading from eip_inspections_2024_2025.csv: its first completed INITIAL test (PASS or FAIL; 0 and 999999 not usable, KM readings in miles), joined by VIN, or by plate and model year where the typed VIN matches no registration; 61,865 have one.
3. Fitted the cumulative miles the area's vehicles had travelled by age, a quadratic least-squares fit of every completed initial reading on age in years from 1 January of the model year (guidelines 3.3).
4. Took each vehicle's 2027 miles as its reading over the curve at its age when tested, times the curve's rise from its age on 1 January 2027 to its age on 1 January 2028; vehicles without a reading take the average of their county and model year (3.4).
5. Multiplied by the Table 2 rate in nox_running_rates_cy2027.xlsx for the model year and the class in registration_body_codes.csv and summed by county in short tons of 907,184.74 grams: five counties at 10.0 or more (3.1, 3.2).
6. Pilot: a voucher in vrp_pilot_vouchers_2025.xlsx whose VIN has an ACTIVE record on the registration snapshot was not retired (the owner took the vehicle back); each retired vehicle's charge is what the Calderwick and Thistlebury lines of vrp_pilot_dismantler_invoices_2025.csv bill for its tow_zone ($185, $280, $330, $395), since Oakhaven's export repeats each invoice's total on every line: Elkhollow 222 vehicles, $59,050; Dunmarsh 201 vehicles, $53,985; Larkhaven 154 vehicles, $42,590; Kinnard 102 vehicles, $26,625.
7. Stations: each vehicle ACTIVE at 1 July 2026 counted once at its completed initial inspection, its station_no read with the station holding that number on the test date: the six numbers eip_annual_report_2024.pdf lists in another county than eip_station_register_2026-06-30.xlsx belonged to the earlier station until the two to three month pause in that number's tests and to the register's station after it; kept where that station is in the vehicle's county.
8. Recommended intake events in Wexmoor, Halvering, Linnmere, Elkhollow and Marlbank.

## 4. Deliverable Answers

### retirement_program_county_nox_2027.xlsx

1. Each county's eligible vehicles' 2027 NOx in short tons to the nearest ton, and whether it qualifies:
   - Wexmoor: 15; qualifies
   - Halvering: 14; qualifies
   - Linnmere: 13; qualifies
   - Elkhollow: 12; qualifies
   - Marlbank: 11; qualifies
   - Dunmarsh: 9; does not qualify
   - Copperleaf: 8; does not qualify
   - Quarrybrook: 8; does not qualify
   - Larkhaven: 8; does not qualify
   - Thorncastle: 6; does not qualify
   - Kinnard: 5; does not qualify
   - Sallowford: 5; does not qualify
2. Bar chart of the twelve counties' 2027 NOx with a line at 10 tons, on the Chart sheet.
3. The vehicles the 2025 pilot retired and what the Department paid dismantlers for them:
   - Elkhollow: 222 vehicles; $59,050
   - Dunmarsh: 201 vehicles; $53,985
   - Larkhaven: 154 vehicles; $42,590
   - Kinnard: 102 vehicles; $26,625
4. For each county, the vehicles registered there on 1 July 2026 whose completed 2024 to 2025 initial inspection was at a station in that county:
   - Copperleaf: 6,591
   - Dunmarsh: 12,605
   - Elkhollow: 11,277
   - Halvering: 20,788
   - Kinnard: 4,693
   - Larkhaven: 9,340
   - Linnmere: 17,587
   - Marlbank: 10,471
   - Quarrybrook: 9,848
   - Sallowford: 5,849
   - Thorncastle: 7,398
   - Wexmoor: 30,798

### intake_counties_2027_memo.docx

1. The recommendation: intake events in Wexmoor, Halvering, Linnmere, Elkhollow and Marlbank.
