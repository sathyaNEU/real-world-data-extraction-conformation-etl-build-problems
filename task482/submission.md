## Tags

**Domain:** General Statistics & Data Science, data integration, record linkage and entity resolution (thirty pharmacy stores' 2026 vaccine refrigerator temperature records, kept by three data logger makes and at ten pilot stores from mid-year by an in-carton sensor, conformed into one record of the vaccine's temperature per store).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Penwick Pharmacy replaces the vaccine refrigerators of stores 103, 106, 109, 201, 206 and 303 before the 2027 respiratory season.**
Their vaccine spent 44, 63, 27, 57, 52 and 60 hours above 8 °C in 2026 against the 24-hour line; the nearest store below it, 306 Padbury, spent 20, 4 short. Not the loggers' own readings, which put 108, 204, 207, 301 and 309 over the line at 38, 142, 32, 146 and 75 hours and 109 under it at 22: a logger's probe in its glycol bottle crosses 8 °C through every defrost swing, restock and busy hour the vaccine in its cartons rode out, and ends a propped-door delivery's excursion before the vaccine has cooled.

## 2. Critical Components

1. On the pilot stores' overlaps the in-carton sensor trails its logger's record by a first-order lag of **42.2** minutes at the Frostline stores, **42.2** at the Kelvra stores and **41.9** at the Brumal stores.
2. Store 109's vaccine spent **27** hours above 8 °C, 22 on its logger's readings.
3. Stores 108, 204, 207, 301 and 309, over the line on their loggers' readings, spent **4, 0, 0, 0 and 1** hours.
4. The nearest store below the line is 306 Padbury at **20** hours, **4** short.

## 3. Step-by-Step Solution

1. Put frostline_temperature_logs_2026.csv (local times with their offsets), kelvra_logger_export_2026.csv (UTC and Fahrenheit, its one day exported twice counted once), brumal_downloads_2026.txt (UTC-6 all year) and tellvane_sensor_readings_2026.csv (UTC) on one clock in degrees C, and joined every serial and sensor id to its store through refrigerator_monitoring_roster_2026.xlsx, the replaced loggers at stores 207 and 302 in sequence.
2. Took 2026 as the stores' local (Central) year and, at the ten pilot stores, the in-carton sensor from its first reading, the logger before it (standard PO-114 section 6.4).
3. Fitted the vaccine's response on the weeks each pilot store's logger kept recording after its sensor's first reading: a first-order lag with each record holding over its ten minutes (section 6.3), 42.2, 42.2 and 41.9 minutes for Frostline, Kelvra and Brumal.
4. Carried every logger record through its make's lag and counted ten minutes for each record whose vaccine temperature at its time stamp is above 8.0 °C (section 7.3), with the in-carton readings above 8.0: stores 103, 106, 109, 201, 206 and 303 at 24 hours or more, 306 nearest below at 20.
5. For doses unaccounted for (section 8.2), took the YE 2025 count in vaccine_physical_inventory_ye2025_ye2026.xlsx, added meridale_vaccine_invoices_2026.csv deliveries (packages times vaccine_item_master_2026.xlsx doses per package, the Lindqvist stores' accounts before April by their former names) and transfers in from vaccine_store_transfers_2026.csv, took off pharmacy_vaccine_administrations_2026.csv, vaccine_writeoff_log_2026.csv and transfers out and the YE 2026 count, each flow between the two counts' own closing times, so the stores that counted on 30 December keep the next day's flows out of the year they close or in the year they open.
6. Read the write-off log's multi-dose vial quantities before the 1 June 2026 inventory update as vials of ten doses (their cost is a vial's) and left meridale_credit_memos_2026.csv out, every credited unit being an expired 2025-26 dose already written off on 1 July.
7. For Brannon spend (section 9.2), took each invoice in brannon_service_history_2026-01_2027-01.xlsx once for work orders whose last visit is in 2026, added 6.0 per cent sales tax to invoices dated before 1 July 2026 (the old platform's amounts are before tax, as its maintenance-only invoices at the agreement's Schedule B prices show), and split each two-store maintenance route by Schedule B's price for each store's unit.
8. Listed the stores at 24 hours or more: 103, 106, 109, 201, 206 and 303.

## 4. Deliverable Answers

### penwick_refrigerator_replacements_2027.xlsx

1. Stores that get a new refrigerator before the 2027 respiratory season: 103, 106, 109, 201, 206 and 303.
2. Each store's 2026 hours with its vaccine above 8 °C, whole hours, and whether it gets a new refrigerator:
   - Store 101 Corriden: 11, no
   - Store 102 Dalmore: 0, no
   - Store 103 Edgecott: 44, yes
   - Store 104 Farrowby: 0, no
   - Store 105 Gisborne: 0, no
   - Store 106 Hatherley: 63, yes
   - Store 107 Ilsington: 0, no
   - Store 108 Keverne: 4, no
   - Store 109 Marcham: 27, yes
   - Store 110 Oldcastle: 19, no
   - Store 201 Thurlby: 57, yes
   - Store 202 Ulverston: 0, no
   - Store 203 Vexley: 0, no
   - Store 204 Wedmore: 0, no
   - Store 205 Yelverton: 7, no
   - Store 206 Abbotsley: 52, yes
   - Store 207 Braxted: 0, no
   - Store 208 Chelwood: 17, no
   - Store 209 Embleton: 0, no
   - Store 210 Greystoke: 15, no
   - Store 301 Haddow: 0, no
   - Store 302 Inkpen: 4, no
   - Store 303 Lexden: 60, yes
   - Store 304 Mowbray: 0, no
   - Store 305 Nettlecombe: 7, no
   - Store 306 Padbury: 20, no
   - Store 307 Quarndon: 0, no
   - Store 308 Ruddington: 17, no
   - Store 309 Tilney: 1, no
   - Store 310 Upwood: 8, no
3. Nearest store below the line: 306 Padbury, 20 hours, 4 short.
4. Each store's 2026 vaccine doses its stock records leave unaccounted for, whole doses:
   - Store 101: 51
   - Store 102: 46
   - Store 103: 100
   - Store 104: 137
   - Store 105: 86
   - Store 106: 67
   - Store 107: 73
   - Store 108: 138
   - Store 109: 63
   - Store 110: 61
   - Store 201: 43
   - Store 202: 157
   - Store 203: 23
   - Store 204: 56
   - Store 205: 102
   - Store 206: 117
   - Store 207: 87
   - Store 208: 38
   - Store 209: 122
   - Store 210: 56
   - Store 301: 75
   - Store 302: 78
   - Store 303: 91
   - Store 304: 38
   - Store 305: 105
   - Store 306: 87
   - Store 307: 118
   - Store 308: 72
   - Store 309: 72
   - Store 310: 75
5. Each store's 2026 refrigerator service spend with Brannon, whole dollars:
   - Store 101: 372
   - Store 102: 336
   - Store 103: 322
   - Store 104: 1,131
   - Store 105: 296
   - Store 106: 1,108
   - Store 107: 349
   - Store 108: 313
   - Store 109: 589
   - Store 110: 1,237
   - Store 201: 2,071
   - Store 202: 682
   - Store 203: 667
   - Store 204: 351
   - Store 205: 996
   - Store 206: 368
   - Store 207: 1,109
   - Store 208: 780
   - Store 209: 1,027
   - Store 210: 645
   - Store 301: 317
   - Store 302: 774
   - Store 303: 297
   - Store 304: 612
   - Store 305: 714
   - Store 306: 350
   - Store 307: 314
   - Store 308: 737
   - Store 309: 298
   - Store 310: 582

### penwick_vaccine_hours_2026.svg

6. Horizontal bar chart of the thirty stores' 2026 hours with the vaccine above 8 °C, highest first, each bar labelled with its whole hours, a vertical line at 24 hours, the 6 stores that get a new refrigerator in blue and the rest in grey, and the nearest store below the line named in the subtitle.
