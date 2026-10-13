## Tags

**Domain:** Epidemiology & Public Health (arbovirus surveillance: mosquito trapping, pooled RT-PCR testing and the estimate of infected vector mosquitoes that books aerial adult mosquito control).
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Fly Thursday's single aerial adulticide application over Westbrook: an estimated 2.3 West Nile virus-infected Culex females per CO2 trap-night in the week ending 15 August 2026, against 1.8 in South Prairie, the runner-up; Westbrook keeps the flight unless the infection of its CO2-caught Culex females is below 18 per 1,000.**
Not Riverside South, which leads only when each positive pool is counted as one infected mosquito and its gravid-trap pools, made of females that have already fed, stand in for the host-seeking females its CO2 traps catch. Not Old Town, whose lead under the likelihood estimate comes from the same gravid-trap pools. Not South Prairie, ahead only when Westbrook's pools of 50 are read as one infected mosquito each. Not Coulee Hills, which has the most human cases (7), all with onsets from late June to late July.

## 2. Critical Components

1. Westbrook's estimate: **2.3** virus-infected Culex females per CO2 trap-night.
2. South Prairie's estimate: **1.8** virus-infected Culex females per CO2 trap-night.
3. Westbrook's Culex females per functioning CO2 trap-night in week 32: **99.0**.
4. Infection rate at which Westbrook's figure falls to South Prairie's: **18 per 1,000** Culex females.

## 3. Step-by-Step Solution

1. Read RCVCD_surveillance_and_control_protocol_2026.pdf: a trap-night is a trap run from set to pickup (3.4), Culex females are pooled by trap-night and species in pools of up to 50 at the district laboratory and up to 10 at the county laboratory (4.1), and the retest of an inconclusive pool is its final result (4.3).
2. From rcvcd_surveillance_2024_2026.sqlite took the CO2 trap-nights set on 10 and 11 August 2026 with status OK and their Culex tarsalis and Culex pipiens females: Westbrook 99.0 per trap-night, South Prairie 143.0.
3. Took each week-32 pool's final result from the database's pool_tests (district laboratory) and from RCPHL_arbovirus_report_2026-W32_RCVCD.pdf (county laboratory, not yet keyed), and each pool's zone and trap type from its trap-night's site.
4. Estimated each zone's infection by species by maximum likelihood for pools of varying size, from the pools of its CO2 traps alone: 42 of Westbrook's 70 Culex tarsalis pools were positive, 23.7 per 1,000 where positive pools over mosquitoes tested gives 14.7.
5. Multiplied each species' females per CO2 trap-night by its infection and summed the two species: Westbrook 2.3, South Prairie 1.8, every other zone lower; the bias-corrected estimate and a single Culex rate give the same figures.
6. The other readings of the same pools name other zones: positive pools over mosquitoes tested across every pool names Riverside South, the likelihood estimate across every pool names Old Town, and positive pools over mosquitoes tested across the CO2 pools names South Prairie.
7. Divided South Prairie's figure by Westbrook's 99.0 Culex females per CO2 trap-night: 18 per 1,000, against Westbrook's 23.5 in week 32.
8. For the season: placed each case in the zone of its residence section on the register's Zone sections sheet (the log's zone column follows the March 2025 list), counting confirmed and probable cases exposed in Rindal County with onset from 1 June to 15 August once per state case ID; counted CO2 trap-nights by status with the 206 records the second load of 22 June entered again counted once.

## 4. Deliverable Answers

### aerial_spray_recommendation.pdf

1. Zone for the flight on Thursday 20 August 2026: Westbrook, 2.3 estimated virus-infected Culex females per CO2 trap-night in the week ending 15 August 2026.
2. Runner-up: South Prairie, 1.8.
3. Infection rate below which Westbrook would lose the flight to South Prairie: 18 per 1,000 Culex females.

### zone_season_2026.xlsx

1. Locally acquired human cases by onset, 1 June to 15 August 2026:
   - North Bottoms: 3
   - Maple Ridge: 2
   - Westbrook: 2
   - Old Town: 2
   - Riverside South: 3
   - South Prairie: 4
   - Coulee Hills: 7
   - Airport East: 2
2. CO2 trap-nights run, 1 June to 15 August 2026:
   - North Bottoms: 256
   - Maple Ridge: 252
   - Westbrook: 319
   - Old Town: 215
   - Riverside South: 211
   - South Prairie: 251
   - Coulee Hills: 188
   - Airport East: 186
3. CO2 trap-nights lost to trap failures, 1 June to 15 August 2026:
   - North Bottoms: 6
   - Maple Ridge: 5
   - Westbrook: 9
   - Old Town: 3
   - Riverside South: 6
   - South Prairie: 11
   - Coulee Hills: 7
   - Airport East: 10

### human_cases_by_zone.png

1. One panel per zone with a bar of locally acquired cases for each MMWR week of onset from week 22 to week 32, each panel titled with the zone's total, the counts matching the workbook.
