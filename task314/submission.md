## Tags

**Domain:** Economics & Econometrics (elasticity, welfare and policy impact estimation).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**Adopt Option C, the drought surcharge, as the Stage 2 rate measure for summer 2027: it takes about 20 acre-feet off the June to September 2027 single-family bills, about 10 more than Option B.**
Customers answer what the whole bill comes to per thousand gallons, not the block price of their last thousand gallons: a panel fit of every single-family bill with both prices in it gives the whole-bill price an elasticity of -0.3126 and the block price none. Not Option B, the drought volume charge (about 10 acre-feet), which adds less than the surcharge to most bills. Not Option A, the conservation blocks, which take no measurable water off once customers answer the whole bill and lead only when every option is priced through the block price.

## 2. Critical Components

1. The plan's baseline: **4,341** single-family accounts and about **770** acre-feet on their June to September bills
2. The price test, a panel fit of every single-family bill with account-by-calendar-month and bill-month effects and each price read at the account's mean use for that month: with both prices in, the whole-bill price **-0.3126** and the block price **+0.0041**; the whole-bill price alone **-0.3112**
3. June to September 2027 savings at -0.3112, priced on the whole bill at each account's baseline use: Option C **19.44** acre-feet (about **20**), Option B **10.86** (about **10**), Option A **0.70** (no measurable saving, **0** to the nearest 10); the gap **8.58** (about **10**)

## 3. Step-by-Step Solution

1. From cis_water_bills_2022-06_to_2026-10.csv took the RES-SF bills that stand (a REBILL in place of the bill it cancels), hundred cubic feet at 748.052 gallons (Resolution 2023-12, Section 2), and kept the accounts billed in each of the eight June to September bill months of 2025 and 2026 (Drought Contingency Plan, Section 5.3): 4,341 accounts and about 770 acre-feet of baseline.
2. Priced every single-family bill from June 2022 to October 2026 twice at the account's mean use for that calendar month, under the schedule and charges its bill date carries (Resolutions 2021-44, 2023-12 and 2024-17): the whole bill per thousand gallons and the block price of the last thousand gallons.
3. Fitted log use on both log prices with account-by-calendar-month and bill-month effects: the whole-bill price -0.3126, the block price +0.0041. The rest of the city alone, where only the 2023 restructuring moved prices, gives the same reading (-0.3330 and +0.0142). Fenwick Mesa against the rest of the city around the 2024 charge, which moved no block price, agrees: use 4.6 per cent lower against a whole bill per thousand gallons 18.5 per cent higher.
4. Refitted on the whole-bill price alone (-0.3112) and priced each option in the agenda report on every account's baseline bill for each June to September 2027 bill month, at the Resolution 2023-12 rates and the capital recovery charge plus the option: Option C 19.44, Option B 10.86, Option A 0.70 acre-feet, the gap 8.58; the same bins hold for any estimate from -0.26 to -0.325 in constant-elasticity, linear or midpoint form.
5. From fill_station_transactions_2026-01-01_2026-10-31.csv counted one tank per opening register on each bay (a bay 2 session resumed after the coupling fault repeats its opening register and carries the session's whole volume on its second row; a trailer filled after its truck opens a session of its own), dated by the local start, each tank's water its last closing register less its opening register: 678, 717, 630 and 682 thousand gallons and 244, 258, 229 and 240 tanks filled, June to September.
6. From city_facility_meter_reads_2025-09_2026-10.csv took the later read of each visit and each meter's advance to the read dated in the month, walked the golf course and cemetery exchanges through meter_shop_completed_work_orders_2025-2026.xlsx with their register units, and left out the Westbrook pool fill meter, whose every advance sits inside the pavilion meter's at the same address (city_facility_meters_2026-10-30.csv): 22.6, 29.7, 31.2 and 23.7 acre-feet, June to September.
7. Recommended Option C, the drought surcharge, about 10 acre-feet ahead of Option B.

## 4. Deliverable Answers

### stage2_drought_rates_2027.xlsx

1. June to September 2027 saving against the plan's baseline, acre-feet to the nearest 10:
   - Option A, conservation blocks: 0 (no measurable saving)
   - Option B, drought volume charge: 10
   - Option C, drought surcharge: 20
2. Bulk fill station, 2026, water drawn in thousand gallons to the nearest thousand, and tanks filled:
   - June: 678, 244 tanks filled
   - July: 717, 258 tanks filled
   - August: 630, 229 tanks filled
   - September: 682, 240 tanks filled
3. City facilities, 2026, water used on the month's reads, acre-feet to one decimal:
   - June: 22.6
   - July: 29.7
   - August: 31.2
   - September: 23.7

### stage2_rate_recommendation.docx

4. Recommended option: Option C, the drought surcharge; runner-up: Option B, the drought volume charge; gap: about 10 acre-feet.

### summer_2027_savings.png

5. Stacked bar chart, one bar per option split into its June, July, August and September bills, the surcharge and the volume charge labelled with their savings and the conservation blocks marked as no measurable saving.
