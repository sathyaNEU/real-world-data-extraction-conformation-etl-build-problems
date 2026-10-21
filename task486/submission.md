## Tags

**Domain:** General Statistics & Data Science (data integration, record linkage and entity resolution: an area agency on aging's provider-area counts of older residents fused from a formally private census release's block group tables and its exact census-day housing counts, with each provider's FY2026 home-delivered meals and active clients conformed from the route tablets' log, the agency's case records and the state's death match).  
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**On census day 2020 Kelvane County's provider areas held, aged 60 and over and aged 75 and over: Wickmoor City 15,580 and 5,150, Fallowmere Town 4,960 and 1,660, North Kelvane 700 and 200, East Kelvane 560 and 190, South Kelvane 760 and 240, West Kelvane 1,060 and 310.**  
Each area takes its block groups' published counts, with the 12 block groups the 2023 boundaries cut split by their blocks' census-day housing units. Not the sum of each area's published block counts, which gives North Kelvane 850 aged 60 and over and puts all eight rural counts above these and all four town counts below them, because the release forced its noise-infused block counts to be non-negative and to add up to their block group, which moves residents from the dense town blocks into the sparse rural blocks of the cut groups. Not the cut groups split by the county's 2026 address points or by the blocks' published population, which carry the same drift (North Kelvane 830 and 810), nor whole tracts split by housing units, which overrides the block groups' own counts (North Kelvane 710).

## 2. Critical Components

1. The provider areas as drawn since 1 July 2023 cut **12** of the county's **62** block groups; the other **50** lie wholly inside one area.
2. The 12 cut block groups publish **4,890** residents aged 60 and over and **1,526** aged 75 and over; split by their blocks' census-day housing units, about **370** and **120** fall on the rural areas' side of the boundaries, where the published blocks hold **695** and **262**.

## 3. Step-by-Step Solution

1. Took each block's provider area from provider_area_blocks.csv, the row with no EFFECTIVE_TO, reading TRACT_BLOCK as the block's ten-digit tract and block code: 12 block groups have blocks in two areas.
2. Summed each block group's residents aged 60 and over (P12_018N to P12_025N and P12_042N to P12_049N) and aged 75 and over (P12_023N to P12_025N and P12_047N to P12_049N) in dhc2020_kelvane_block_groups_p12.csv.
3. Gave each of the 50 whole block groups' counts to its area.
4. Split each cut block group's counts between its two areas in proportion to its blocks' H1_001N in dhc2020_kelvane_blocks_h1.csv: about 370 aged 60 and over and 120 aged 75 and over to the rural sides, to the nearest ten.
5. Added each area's parts, which together equal the county's 23,621 and 7,751 in dhc2020_kelvane_county_tracts_p12.csv, and rounded each area's count once to the nearest ten (North Kelvane 700 aged 60 and over).
6. Meals: counted each client's rows in hdm_route_delivery_log_fy2026.csv once per delivery_date and item_code, a HOT code up to the client's meals_per_day in hdm_client_roster_2026-10-09.csv, valued each at its meals in hdm_item_codes.csv and placed it under the provider of the area of the client's home_block, whichever route carried it: 221,098 meals.
7. Active clients: kept the clients with an episode in hdm_service_episodes_2026-10-09.csv open on 30 September 2026, dropped those state_death_match_runs_2025-07_to_2026-10.csv shows died on or before that day under their state_participant_id or a prior_participant_id that state_registry_number_links.csv links to it, and counted the rest under the provider of their home_block's area: 616 clients.
8. Wrote kelvane_provider_area_counts.xlsx.

## 4. Deliverable Answers

### kelvane_provider_area_counts.xlsx

1. Residents aged 60 and over on census day 2020, to the nearest ten:
   - Wickmoor City: 15,580
   - Fallowmere Town: 4,960
   - North Kelvane: 700
   - East Kelvane: 560
   - South Kelvane: 760
   - West Kelvane: 1,060
2. Residents aged 75 and over on census day 2020, to the nearest ten:
   - Wickmoor City: 5,150
   - Fallowmere Town: 1,660
   - North Kelvane: 200
   - East Kelvane: 190
   - South Kelvane: 240
   - West Kelvane: 310
3. Home-delivered meals served from October 2025 through September 2026, by provider:
   - Wickmoor Senior Services (Wickmoor City): 139,058
   - Fallowmere Community Center (Fallowmere Town): 40,951
   - North Kelvane Senior Center (North Kelvane): 9,793
   - East Kelvane Senior Center (East Kelvane): 8,883
   - South Kelvane Senior Center (South Kelvane): 9,855
   - West Kelvane Senior Center (West Kelvane): 12,558
4. Active home-delivered meal clients on 30 September 2026, by provider:
   - Wickmoor Senior Services (Wickmoor City): 397
   - Fallowmere Community Center (Fallowmere Town): 114
   - North Kelvane Senior Center (North Kelvane): 25
   - East Kelvane Senior Center (East Kelvane): 22
   - South Kelvane Senior Center (South Kelvane): 27
   - West Kelvane Senior Center (West Kelvane): 31
