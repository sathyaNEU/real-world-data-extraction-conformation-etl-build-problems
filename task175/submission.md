## Tags

**Domain:** Urban and regional science, land use and spatial development modeling.  
**Analytical objective:** Forecasting and predictive modeling.

## 1. Final Recommendation

**Port Ardell will issue about 300 single-family building permits in 2027 on lots in North 6, North 7 and Northwest 3 together, to the nearest 50.**
The figure takes each vacant lot's chance of a permit from served vacant lots on streets with as many homes standing as its own, and 10,309 of the 14,232 vacant lots stand on streets with no home. Not the first-year permits per vacant lot of the earlier extension areas, which were connected when most of their streets already had homes. Not a lot model without the street, or one built on the plat block, which mixes the lots of two streets.

## 2. Critical Components

1. Vacant lots on 1 January 2027: **14,232** in the three areas (North 6 **3,893**, North 7 **5,363**, Northwest 3 **4,976**)
2. Vacant lots on streets with no home standing on 1 January 2027: **10,309**

## 3. Step-by-Step Solution

1. Placed every lot in its area through the plat unit in its legal description in pa_parcel_extract_2026.csv and the plat units and acceptance dates in uep_program_schedule_rev12_2026.pdf.
2. Joined the Residential New Single Family permits of bldg_permits_legacy_2008_2018.csv (by site address) and bldg_permits_2019_2026.xlsx (by parcel), dropping the legacy copy of each carried-over permit, for each lot's issue and certificate of occupancy dates.
3. Counted the homes standing on each lot's street (the street and hundred-block of its site address, both sides) on 1 January of each year from YR_BUILT and the certificates of occupancy issued in 2026, which the 2026 roll does not yet show.
4. Fitted served vacant lot-years 2008 to 2026 (exposure from each area's acceptance date to the permit) as a Poisson rate: a year effect times a canal effect times a separate effect for each band of homes standing on the street (0, 1, 2, 3, 4 to 5, 6 to 8, 9 to 12, 13 to 17, 18 or more), not a slope on the count.
5. Applied the 2026 level, as the forecasting conventions require, to the 14,232 vacant lots of the three areas by their streets and canals, each area served from its scheduled acceptance date and at the well and septic rate before it, and summed each lot's chance of a permit in 2027 (one less the exponential of its cumulative rate, the expected number of distinct lots the conventions define): 300 permits.
6. Placed every premise in cis_premise_extract_20261231.csv on its lot by its parcel number where recorded and otherwise by service address (street types normalised), and took fiscal 2026 new connections from ami_headend_installs_fy25_fy26.csv as each lot's first install in the log, when it falls in fiscal 2026 at a lot with no account in cis_account_history_20261231.csv opened before it: a lot carried under two premises (its stub and one set up at the counter when a stalled build's meter was set again) is one connection whatever their address strings, a later install at a lot is a meter set again, and an install at a billed lot is a meter exchange; phases through the plat unit into the schedule's phases rather than by the premise's stored UEP_PHASE.
7. Summed capacity_fee_receipts_fy2026.xlsx once per payment by receipt date, a payment being a receipt number and its payer: a receipt covering several permits repeats its amount on each permit line, and receipt numbers run by drawer and day, so two payers' receipts can share a number; each payment placed in the phase of its permits' lots through the parcel numbers in bldg_permits_2019_2026.xlsx.

## 4. Deliverable Answers

### uep_2027_permit_forecast.xlsx

1. Single-family building permits in 2027 in the three areas together: **300** (nearest 50)
2. New single-family connections in fiscal 2026: Phase 1 **206**, Phase 2 **293**, Phase 3 **462**, Phase 4 **396**
3. Water and sewer capacity fees received in fiscal 2026 (Q1 October to December 2025 through Q4 July to September 2026), USD:
   - Core service area: Q1 **526,050**, Q2 **578,655**, Q3 **531,895**, Q4 **420,840**
   - Phase 1: Q1 **859,215**, Q2 **672,175**, Q3 **835,835**, Q4 **841,680**
   - Phase 2: Q1 **999,495**, Q2 **941,045**, Q3 **1,467,095**, Q4 **754,005**
   - Phase 3: Q1 **1,467,095**, Q2 **1,776,880**, Q3 **1,940,540**, Q4 **1,876,245**
   - Phase 4: Q1 **1,472,940**, Q2 **1,332,660**, Q3 **1,601,530**, Q4 **1,379,420**

### fy2026_capacity_fees.png

1. One stacked bar per fiscal 2026 quarter with a segment for the core service area and each of Phases 1 to 4, each segment labelled with its fees in whole dollars as in answer 3 above.
