## Tags

**Domain:** Physical & Environmental Sciences (sensor calibration and measurement).
**Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**Six tanks need their gauge charts redone before the 2027 season: BP-2, CF-2, DH-1, FL-1, GC-1 and HS-2.**
Each misstates the change in stock by more than 25 gallons between two of its reorder, half-full and normal fill heights once the 2026 sales intervals are anchored on the deliveries. Not none, as the monthly reconciliations read: every fill-and-draw cycle cancels both kinds of chart error. Not CF-2 and GC-1 alone, as the delivery check reads: BP-2, DH-1, FL-1 and HS-2 misstate most through the middle of the range, which every delivery spans end to end. Not the 9 tanks the sales intervals alone give: that fit charges DH-2, EB-1, EB-2 and HS-1's dock meter errors to their charts and drops GC-1.

## 2. Critical Components

1. BP-2, DH-1, FL-1 and HS-2 misstate most between the reorder and half-full heights, each by more than **25** gallons.
2. CF-2 and GC-1 misstate most between the reorder and normal fill heights, each by more than **25** gallons.
3. The other **14** tanks misstate less than 25 gallons between every pair of the three heights.

## 3. Step-by-Step Solution

1. Took each tank's reorder, half-full and normal fill heights from tank_register.xlsx and its chart from tank_charts.csv, keyed console tank numbers to tanks by the dates in atg_tank_setup.csv, and read the 2026 season, 1 April to 31 October (FS-3 section 3.4).
2. Paired consecutive two-hour readings in atg_inventory_2026.csv that no delivery overlaps and summed the gallons each tank's hoses metered between them in dock_sales_legacy_2026.csv (hoses to tanks by dock_piping.xlsx), corrected to 60 F with FS-3 Table 1.
3. Set each delivery's net rise in atg_deliveries_2026.csv against its bill of lading's net gallons in bols_2026.csv.
4. Fitted each tank's chart error as a piecewise-linear function of height (3-inch knots, the three register heights among them) to the intervals with a dock meter factor and to the deliveries without one, together: 6 tanks misstate more than 25 gallons between two heights.
5. For the gauge feed, re-dated each console's rows stamped 2016 after the 24 January storm along its record sequence, kept Dellwood's tanks apart either side of the 17 February console change by atg_tank_setup.csv, and counted each tank's local days of 2026 with no reading.
6. For leak tests, kept one row per console, tank and test number in atg_leak_tests_2026.csv, dated each test by its own Sunday-night row or, for a test logged only when re-polled after an outage, by the weekly test numbers, and counted each marina's tank-months with no PASS.
7. For dock gallons, took the legacy export to go-live and the new export after the last legacy sale (its shadow-week card copies dropped), dated card sales to the day before their settlement stamp, and read each new-export row's product from its price, because pos_grades.csv lists Ashby Hollow's and Gilliam Creek's former E10 grade as REC-90.
8. Re-chart BP-2, CF-2, DH-1, FL-1, GC-1 and HS-2 before the service starts on 1 April 2027.

## 4. Deliverable Answers

### recharting_list_2027.csv

1. Six rows:
   - BP-2: Brannock Point Marina, E10 unleaded, 10,000 gallons, reorder and half-full
   - CF-2: Cedar Fork Boat Dock, REC-90 ethanol-free, 10,000 gallons, reorder and normal fill
   - DH-1: Dellwood Harbor, REC-90 ethanol-free, 10,000 gallons, reorder and half-full
   - FL-1: Foxtail Landing Resort & Marina, REC-90 ethanol-free, 12,000 gallons, reorder and half-full
   - GC-1: Gilliam Creek Marina, REC-90 ethanol-free, 10,000 gallons, reorder and normal fill
   - HS-2: Hackett Shoals Dock, E10 unleaded, 8,000 gallons, reorder and half-full

### cutover_readiness_2027.pdf

1. Number: 6 tanks need their charts redone.
2. Chart: paired bars of each listed tank's misstatement over reorder to half-full and over half-full to normal fill, with the 25-gallon lines.
3. Days of 2026 each tank's gauge sent no inventory reading:
   - AH-1: 10 days
   - AH-2: 10 days
   - AH-3: 10 days
   - BP-1: 14 days
   - BP-2: 14 days
   - BP-3: 14 days
   - CF-1: 9 days
   - CF-2: 9 days
   - DH-1: 10 days
   - DH-2: 14 days
   - EB-1: 13 days
   - EB-2: 13 days
   - EB-3: 13 days
   - FL-1: 11 days
   - FL-2: 11 days
   - GC-1: 11 days
   - GC-2: 13 days
   - GC-3: 11 days
   - HS-1: 13 days
   - HS-2: 13 days
4. Tank-months of 2026 without a passing monthly leak test, by marina:
   - Ashby Hollow Marina: 0
   - Brannock Point Marina: 17
   - Cedar Fork Boat Dock: 12
   - Dellwood Harbor: 1
   - Elkhorn Bend Marina: 15
   - Foxtail Landing Resort & Marina: 12
   - Gilliam Creek Marina: 1
   - Hackett Shoals Dock: 9
5. 2026 dock gallons by marina and product, to the nearest gallon:
   - Ashby Hollow Marina: REC-90 ethanol-free 75,025; E10 unleaded 37,588; Diesel 35,964
   - Brannock Point Marina: REC-90 ethanol-free 86,206; E10 unleaded 40,609; Diesel 34,248
   - Cedar Fork Boat Dock: REC-90 ethanol-free 62,140; Diesel 20,789
   - Dellwood Harbor: REC-90 ethanol-free 93,626
   - Elkhorn Bend Marina: REC-90 ethanol-free 66,829; E10 unleaded 30,522; Diesel 33,148
   - Foxtail Landing Resort & Marina: REC-90 ethanol-free 77,018; Diesel 29,319
   - Gilliam Creek Marina: REC-90 ethanol-free 75,997; E10 unleaded 33,908; Diesel 32,719
   - Hackett Shoals Dock: REC-90 ethanol-free 63,380; E10 unleaded 30,502
