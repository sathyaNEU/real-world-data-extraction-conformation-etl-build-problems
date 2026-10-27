## Tags

**Domain:** Actuarial science and insurance (catastrophe exposure and accumulation).
**Analytical objective:** Opportunity sizing and decision support.

## 1. Final Recommendation

**Award the 2027 FORTIFIED Roof grant round to Cypress Ridge: re-roofing its portfolio removes about USD 3 million a year of expected hurricane loss, the most of the four counties.**
Not Marlin Shoals, the runner-up, which carries the largest annual expected loss (USD 10.08 million) almost all in events gusting 130 mph or more, where the roof cuts little. Not Heron Bay or Calloway Flats, which remove less.

## 2. Critical Components

1. 2027 annual expected loss on the portfolios' current roofs (USD million): Marlin Shoals **10.08**, Heron Bay **5.89**, Calloway Flats **0.53**, Cypress Ridge **4.42**.
2. The FORTIFIED Roof cut read class by class of peak gust reproduces the paid loss on FORTIFIED homes within **10 percent** in all **5** storms MG-04 tests (Darcy, Elspeth, Halsey, Dunstan, Greer); one cut for all storms misses in Elspeth, Halsey, Dunstan.
3. Expected annual loss removed: Cypress Ridge **USD 3 million**, ahead of Marlin Shoals.

## 3. Step-by-Step Solution

1. For each named storm since 2012 (named_storm_register_2008-2025.csv), summed every payment line coded to its catastrophe code in claims_payment_lines_2012-01_to_2026-09.csv by ZIP code and FORTIFIED credit (FORT-R), against Coverage A at landfall from inforce_at_landfall_by_zip_2008-2025.parquet (USD thousands before 2019) and the ZIP's peak gust from storm_peak_gust_footprints_2008-2025.xlsx (knots times 1.150779 before 2019).
2. Took the FORTIFIED Roof cut in each 10 mph gust class as one minus the FORTIFIED homes' paid per dollar of Coverage A over the standard homes', pooled over the class's storms and ZIP codes.
3. Ran MG-04's reproduction test on the 5 storms with USD 10 million or more paid on FORTIFIED homes: the class cuts pass on all 5, one cut for all storms fails in Elspeth, Halsey, Dunstan.
4. Joined corvane_hu27_elt_sandpiper_retrofit_2027.parquet to corvane_hu27_event_hazard_summary.csv on the event number (HU27- prefix dropped) and county, and took each portfolio's annual expected loss and the loss removed as the sum over events of annual rate times mean loss, and times the cut for the event's gust class.
5. For FORTIFIED homes, kept certificates in fortified_certificate_register_2012-2026.csv issued by September 30, 2026, expiring after it and not voided, and matched each to the home in force that day in policy_master_2006-2026.csv by parcel and building (the main house or the COTTAGE), not by the policy it was issued under nor by the street name, which the county has changed since some were issued, counting each home once.
6. For the storms before 2012, took each legacy claim's last paid to date in legacy_claims_valuations_2008-2011.csv and added its carried lines in the claims file (legacy_claim_ref), leaving out the January 1, 2012 line that repeats the legacy paid to date; paid after 2011 is those added lines.
7. For roof ages, raised each portfolio home's roof year on record in retrofit_2027_modeled_portfolios.csv to the year of its latest RE-ROOF permit by September 30, 2026 in county_building_permits_roofing_2013-2026.csv, matched on ZIP code, house number, street and building (BLDG 2 the cottage; ROOF REPAIR not a new roof), a permit on a renamed street read under its new name, the old and new names paired by the parcels fortified_certificate_register_2012-2026.csv lists under the old name and policy_master_2006-2026.csv under the new (Tram as Gulf Breeze, Boggy Creek as Marsh Hen, Sawmill as Laurel Hill, Pinebarren as Fort Dale), and counted roof years 2012 or earlier.
8. Recommended Cypress Ridge, the largest expected annual loss removed.

## 4. Deliverable Answers

### retrofit_round_2027.xlsx

1. County for the 2027 round: Cypress Ridge.
2. Expected annual hurricane loss the round removes there: USD 3 million.
3. Runner-up: Marlin Shoals.
4. 2027 annual expected loss on each county's portfolio (USD million):
   - Marlin Shoals: 10.08
   - Heron Bay: 5.89
   - Calloway Flats: 0.53
   - Cypress Ridge: 4.42
5. Insured homes holding a valid FORTIFIED Roof certificate on September 30, 2026, and their Coverage A (USD thousands):
   - Marlin Shoals: 1,711, 681,915
   - Heron Bay: 1,665, 605,650
   - Calloway Flats: 1,420, 504,862
   - Cypress Ridge: 1,813, 823,282
6. Net paid to date and the part of it paid after 2011 (USD thousands):
   - Hurricane Corwin: 47,101, 902
   - Tropical Storm Bettina: 10,486, 265
   - Hurricane Delmar: 19,875, 9,273
7. Portfolio homes with a roof 15 or more years old on June 1, 2027, and their Coverage A (USD thousands):
   - Marlin Shoals: 77, 30,285
   - Heron Bay: 382, 137,967
   - Calloway Flats: 520, 185,473
   - Cypress Ridge: 610, 283,409

### avoided_loss_by_county.png

1. Bar chart of each county's 2027 annual expected loss beside the loss the round removes, Cypress Ridge's bar the tallest of the loss removed.

### board_note_retrofit_2027.docx

1. One-page note to the board recommending Cypress Ridge at about USD 3 million a year removed, Marlin Shoals next, with the chart.
