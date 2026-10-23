## Tags

**Domain:** Urban and regional science, land use and spatial development modeling.  
**Analytical objective:** Forecasting and predictive modeling.

## 1. Final Recommendation

**Port Ardell will issue about 300 single-family building permits in 2027 on lots in North 6, North 7 and Northwest 3: 90 in North 6, 115 in North 7 and 95 in Northwest 3.**
The figure takes each vacant lot's chance of a permit from served vacant lots on streets with as many homes standing as its own, and 10,309 of the 14,232 vacant lots stand on streets with no home. Not the first-year permits per vacant lot of the earlier extension areas, which were connected when most of their streets already had homes. Not a lot model without the street, or one built on the plat block, which mixes the lots of two streets.

## 2. Critical Components

1. Vacant lots on 1 January 2027: **14,232** in the three areas (North 6 **3,893**, North 7 **5,363**, Northwest 3 **4,976**)
2. Vacant lots on streets with no home standing on 1 January 2027: **10,309**

## 3. Step-by-Step Solution

1. Placed every lot in its area through the plat unit in its legal description in pa_parcel_extract_2026.csv and the plat units and acceptance dates in uep_program_schedule_rev12_2026.pdf.
2. Joined the Residential New Single Family permits of bldg_permits_legacy_2008_2018.csv (by site address) and bldg_permits_2019_2026.xlsx (by parcel), dropping the legacy copy of each carried-over permit, for each lot's issue and certificate of occupancy dates.
3. Counted the homes standing on each lot's street (the street and hundred-block of its site address, both sides) on 1 January of each year from YR_BUILT and the certificates of occupancy issued in 2026, which the 2026 roll does not yet show.
4. Fitted served vacant lot-years 2008 to 2026 (exposure from each area's acceptance date to the permit) as a year effect times a canal effect times the number of homes standing on the street.
5. Applied the 2026 level, as the forecasting conventions require, to the 14,232 vacant lots of the three areas by their streets and canals, each area served from its scheduled acceptance date and at the well and septic rate before it: 300 permits.
6. Took fiscal 2026 new connections from ami_headend_installs_fy25_fy26.csv as the installs at premises with no account in cis_account_history_20261231.csv opened before the install (the rest are meter exchanges at billed homes), placed by parcel or service address through the plat unit into the schedule's phases rather than by the premise's stored UEP_PHASE.
7. Summed capacity_fee_receipts_fy2026.xlsx once per receipt by receipt date, since a receipt covering several permits repeats its amount on each permit line.

## 4. Deliverable Answers

### uep_2027_permit_forecast.xlsx

1. Single-family building permits in 2027: **300** in total; North 6 **90**, North 7 **115**, Northwest 3 **95**
2. New single-family connections in fiscal 2026, by quarter (Q1 October to December 2025 through Q4 July to September 2026):
   - Core service area: Q1 47, Q2 35, Q3 42, Q4 29
   - Phase 1: Q1 52, Q2 37, Q3 56, Q4 61
   - Phase 2: Q1 71, Q2 61, Q3 97, Q4 64
   - Phase 3: Q1 107, Q2 97, Q3 130, Q4 128
   - Phase 4: Q1 98, Q2 101, Q3 96, Q4 101
3. Water and sewer capacity fees received in fiscal 2026: Q1 **USD 4,290,230**, Q2 **USD 4,196,710**, Q3 **USD 4,991,630**, Q4 **USD 4,348,680**

### fy2026_new_connections.png

1. One stacked bar per fiscal 2026 quarter with a segment for the core service area and each of Phases 1 to 4, each segment labelled with its connection count as in answer 2 above.
