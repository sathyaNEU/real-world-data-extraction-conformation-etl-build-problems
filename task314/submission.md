## Tags

**Domain:** Economics & Econometrics (elasticity, welfare and policy impact estimation).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**Adopt Option C, the drought surcharge, as the Stage 2 rate measure for summer 2027: it takes about 30 acre-feet off the June to September 2027 single-family bills, about 10 more than Option B.**
The city's customers answer what the whole bill comes to per thousand gallons: the Fenwick Mesa capital recovery charge moved no block price and still cut that area's summer use 4.6 per cent against the rest of the city. Not Option B, the drought volume charge (about 20 acre-feet), which adds less than the surcharge to most bills. Not Option A, the conservation blocks (about 10 acre-feet), which looks best only when every option is priced through the block price of a household's last thousand gallons, the price the 2023 restructuring showed households barely answer.

## 2. Critical Components

1. The plan's baseline: **4,341** single-family accounts and about **770** acre-feet on their June to September bills
2. Customers answer the whole bill per thousand gallons, not the block price: the Fenwick Mesa charge gives an elasticity of **-0.27 to -0.32** on the whole bill across its summers and price readings
3. June to September 2027 savings, priced on the whole bill at each account's baseline: Option C about **30** acre-feet, Option B about **20**, Option A about **10**

## 3. Step-by-Step Solution

1. From cis_water_bills_2022-06_to_2026-10.csv took the RES-SF bills that stand (a REBILL in place of the bill it cancels), hundred cubic feet at 748.052 gallons (Resolution 2023-12, Section 2), and kept the accounts billed in each of the eight June to September bill months of 2025 and 2026 (Drought Contingency Plan, Section 5.3): 4,341 accounts and about 770 acre-feet of baseline.
2. Read the July 2023 restructuring (Resolution 2023-12 against Resolution 2021-44) on the block price: households between the old and the new third-block thresholds saw their last-block price more than double and their summer use barely moved, so a block-price model gives the surcharge no effect and cannot by itself say which price customers answer.
3. Compared Fenwick Mesa with the rest of the city across the capital recovery charge (Resolution 2024-17: a USD 14.00 charge on every Fenwick Mesa bill from July 2024, no block price changed), on the accounts billed July to September in 2023 and 2025: use 4.6 per cent lower against a whole bill per thousand gallons 18.5 per cent higher, an elasticity of -0.28 (-0.27 to -0.32 across the other summers and price readings).
4. Priced each option in the agenda report on every account's baseline bill for each June to September 2027 bill month, at the Resolution 2023-12 rates and the capital recovery charge plus the option, and took each account's fall in use at that elasticity on the whole bill per thousand gallons: Option C about 30, Option B about 20, Option A about 10 acre-feet.
5. From fill_station_transactions_2026-01-01_2026-10-31.csv counted one tank fill per opening register on each bay (a bay 2 session resumed after the coupling fault repeats its opening register and carries the session's whole volume on its second row), dated by the local start, each fill's water its last closing register less its opening register: 678, 717, 630 and 682 thousand gallons and 244, 258, 229 and 240 tank fills, June to September.
6. From city_facility_meter_reads_2025-09_2026-10.csv took the later read of each visit and each meter's advance to the read dated in the month, walked the golf course and cemetery exchanges through meter_shop_completed_work_orders_2025-2026.xlsx with their register units, and left out the Westbrook pool fill meter, whose every advance sits inside the pavilion meter's at the same address (city_facility_meters_2026-10-30.csv): 22.6, 29.7, 31.2 and 23.7 acre-feet, June to September.
7. Recommended Option C, the drought surcharge, about 10 acre-feet ahead of Option B.

## 4. Deliverable Answers

### stage2_drought_rates_2027.xlsx

1. June to September 2027 saving against the plan's baseline, acre-feet to the nearest 10:
   - Option A, conservation blocks: 10
   - Option B, drought volume charge: 20
   - Option C, drought surcharge: 30
2. Bulk fill station, 2026, water drawn in thousand gallons to the nearest thousand, and tank fills:
   - June: 678, 244 tank fills
   - July: 717, 258 tank fills
   - August: 630, 229 tank fills
   - September: 682, 240 tank fills
3. City facilities, 2026, water used on the month's reads, acre-feet to one decimal:
   - June: 22.6
   - July: 29.7
   - August: 31.2
   - September: 23.7

### stage2_rate_recommendation.docx

4. Recommended option: Option C, the drought surcharge; runner-up: Option B, the drought volume charge; gap: about 10 acre-feet.

### summer_2027_savings.png

5. Stacked bar chart, one bar per option split into its June, July, August and September bills, each bar labelled with its June to September saving.
