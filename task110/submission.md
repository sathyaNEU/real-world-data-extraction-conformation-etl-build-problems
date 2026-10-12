# task110: Yacaaba Radiology fixed asset migration, January to June 2027 depreciation

## Tags

**Domain:** Accounting, Audit & Forensic Analytics, fixed assets and leases (internal audit's re-performance of a practice's fixed asset register migration to the group ledger).  
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**The group ledger will post $931,458 of depreciation on Yacaaba Radiology's assets from January to June 2027.**

Each equipment upgrade runs over the remaining life of the imaging system its capital approval names, the only basis that reproduces both Yacaaba's depreciation postings and the 2024 depreciation in note 9 of its FY2025 report, and six upgrades on systems that run out between October and December 2026 load at nil book value. Not the five-year life the rates tab gives options and accessories: it replays every posting and balance but not the 2024 imaging depreciation. Not stopping each upgrade when its system's life ends while keeping five-year rates: it misses the same 2024 figure.

## 2. Critical Components

1. The rebuilt schedules reproduce all **90** account-months of Yacaaba's depreciation postings from July 2025 to September 2026 to the cent, and both years of note 9 in the FY2025 report.
2. **Six** equipment upgrades (assets 1176, 1177, 1180, 1183, 1184 and 1191) load at nil book value with no remaining months.
3. Yacaaba's ledger still posts **$627,241** of depreciation from October to December 2026.
4. **202** assets load, at a book value of **$6,315,591**.

## 3. Step-by-Step Solution

1. Cleaned `YCB_asset_register_2026-10-02.xlsx` to the ledger by dropping the Capitalised N items and the repeated invoice lines, after which cost ties to `YCB_trial_balance_30-09-2026.xlsx` account by account.
2. Rebuilt every asset straight line from its month of purchase on the Rates tab, with computer equipment moved to four years prospectively from July 2025 (FY2025 note 1(e)), the Cessnock OPG's $38,000 impairment from June 2025 (note 9), and the Bremer Voluson continued on the depreciation brought forward in its February 2026 intercompany journal.
3. Put each Equipment upgrades row on the remaining months of the imaging system its request in `YCB_capital_approvals_2018-2026.csv` names by system and site, the only upgrade basis that reproduces both the 90 account-months in `YCB_GL_detail_2025-07_to_2026-09.csv` and the 2024 depreciation in note 9 of `YCB_FY2025_financial_statements_extract.pdf`.
4. Ran the schedules to 31 December 2026: $627,241 of October to December depreciation.
5. Applied FIN-PRO-022 to `verification_scans_YCB_2026.csv` and `RAY_count_sheet_07-10-2026.pdf` (5:00 pm Sydney time cut-off on 9 October, serial where the tag is blank, site of record where sighted): 9 nil-book-value assets not sighted are written off and 202 assets load at $6,315,591.
6. Classed each asset with the approved v2 sheet of `group_asset_class_mapping.xlsx` on its account in the 9 October trial balance run, which moves the Charlestown reception joinery to leasehold improvements.
7. Depreciated the load from January 2027 under section 6 of `fa_migration_standard.pdf`: $931,458 for January to June 2027.
8. Recommendation: sign the load off; the group ledger will post $931,458 of depreciation on Yacaaba's assets from January to June 2027.

## 4. Deliverable Answers

### fa_load_2027-01-01.csv

1. 202 rows, one per asset that loads, with asset number, description, site, group asset class, cost, accumulated depreciation at 31 December 2026, book value, remaining months and January to June 2027 charge, amounts in dollars and cents.
2. Column totals: cost $26,925,203.71; accumulated depreciation at 31 December 2026 $20,609,613.13; book value $6,315,590.58; January to June 2027 charge $931,458.07.
3. Assets 1176, 1177, 1180, 1183, 1184 and 1191 (equipment upgrades) carry nil book value and 0 remaining months.

### cutover_signoff.docx

1. January to June 2027 depreciation on Yacaaba's assets: $931,458, stated first.
2. By site as the assets load (book value at 30 September 2026, October to December 2026 depreciation, book value loaded, January to June 2027 charge):
   - Charlestown: $2,934,245, $322,597, $2,611,648, $439,211
   - Maitland: $1,111,168, $131,657, $979,511, $152,095
   - Cessnock: $1,020,841, $84,413, $936,428, $168,692
   - Raymond Terrace: $1,876,578, $88,574, $1,788,004, $171,460
3. Assets coming across with nothing left to depreciate, count and original cost:
   - Charlestown: 28 assets, $3,653,162
   - Maitland: 24 assets, $3,231,776
   - Cessnock: 5 assets, $20,223
   - Raymond Terrace: 13 assets, $163,993
4. Book value loading by group asset class:
   - Imaging equipment: $2,775,536
   - Clinical equipment: $438,489
   - Computer equipment: $130,944
   - Leasehold improvements: $2,826,283
   - Furniture and fittings: $123,144
   - Motor vehicles: $21,195
5. Bar chart of the January to June 2027 charge by site at the end of the note, one bar per site labelled in dollars, titled with the $931,458 total.




