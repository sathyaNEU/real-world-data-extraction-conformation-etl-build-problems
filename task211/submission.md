## Tags

**Domain:** Pharmacology, Pharmacoepidemiology & Safety (safety signal detection).
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Send Tessard to the third-quarter laboratory re-test: its patients have 4 more qualifying visits per 1,000 patient-months than tablets releasing like Levaril would give them.** Not Halvorne, whose raw excess is the first supply of its new pink tablets and goes with any change of tablet appearance, not with what Halvorne's tablets contain.

## 2. Critical Components

1. The excess over the reference sits on the days of each patient's first fill of a tablet that looks different from their previous fill, for every product, and not on a change between identical tablets.
2. Tessard's excess, held at that, is **4** qualifying visits per 1,000 patient-months, above the 2.0 bar.

## 3. Step-by-Step Solution

1. Took paid claims net of reversals from dispensing_claims_2025-04_to_2026-06.parquet, mapped both code schemes through claims_item_crosswalk.csv and ran each member's supply per MS-12 2.4.
2. Dated qualifying visits from both hospital feeds in Pacific time, counted transfers once and linked merged records through mrn_member_crosswalk.csv (MS-12 2.3); attributed each to the product covering its day (2.5).
3. Gave every fill its tablet from product_register.xlsx, dating Halvorne's Fort Wayne tablets by each distribution centre in halvorne_site_change_notice.pdf (pharmacies.csv) and Corwen's beige coat by corwen_film_coat_notice.pdf, and marked each patient's first fill of a differently looking tablet.
4. Fitted a Poisson model of qualifying visits on patient-months with product, that first-supply marker, age band (under 18, 18 to 64, 65 and over, on 2026 less birth year) and drug-resistant epilepsy, and set the product term to Levaril's with the marker held (MS-12 2.6): Tessard 4 per 1,000 patient-months, every other generic under the 2.0 bar.
5. Spend: joined wholesaler_invoice_lines.csv to dc_receiving_log.csv by delivery number and split each line by the quarter of each receipt part; spread each price adjustment over that ship-to's deliveries of the generic invoiced before it, counted back from the latest until its bottles were made up, and put each share in the quarter those bottles were received (purchasing manual 7.3).
6. Backorder days: resolved each notice's item through wholesaler_item_list.csv as it stood on the notice's day (a pre-cut-over number the list gives no product as a former number belongs to whichever product without a listed former number stopped shipping when the notice opened), and ended it the day before the product's next shipment in wholesaler_advance_ship_notices.json, case barcodes read to their bottle (clause 4).
7. Recommendation: send Tessard.

## 4. Deliverable Answers

### retest_referral.docx

1. Referral: Tessard, 4 excess qualifying visits per 1,000 patient-months.
2. Bar chart of each generic's excess over Levaril for January to June 2026, Tessard highlighted, with the 2.0 bar.

### levetiracetam_products.xlsx

1. Patient-months of supply and qualifying visits, January to June 2026:
   - Halvorne: 104,190 patient-months, 4882 qualifying visits
   - Pellbrook: 33,310 patient-months, 1402 qualifying visits
   - Corwen: 19,260 patient-months, 744 qualifying visits
   - Tessard: 53,040 patient-months, 1960 qualifying visits
   - Wynfield: 54,140 patient-months, 1743 qualifying visits
2. Spend by quarter received, dollars:
   - Halvorne: Q1 307,200, Q2 251,490
   - Pellbrook: Q1 70,640, Q2 114,700
   - Corwen: Q1 105,850, Q2 106,590
   - Tessard: Q1 77,180, Q2 168,640
   - Wynfield: Q1 164,840, Q2 133,850
3. Days on backorder at the wholesaler:
   - Halvorne: Q1 14, Q2 14
   - Pellbrook: Q1 59, Q2 33
   - Corwen: Q1 11, Q2 11
   - Tessard: Q1 44, Q2 9
   - Wynfield: Q1 12, Q2 17
