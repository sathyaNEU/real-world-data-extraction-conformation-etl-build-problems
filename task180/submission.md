# task180: where the revenue protection field team works in January to March 2027

## Tags

**Domain:** Energy Systems & Utilities (revenue protection at an electricity supplier: screening smart-meter consumption for meter bypasses).
**Analytical objective:** Anomaly Detection & Diagnostics (separating a diversion on one metered supply from ordinary variation, empty properties and heating changes).
**Reasoning phases:** Explore/Discover, Hypothesize, Analyze/Validate, Synthesize, Recommend/Communicate.

## 1. Final Recommendation

**Place the field team in Caithness for January to March 2027; it starts the quarter with 54 referrals.**

Caithness leads Elgin and Lossiemouth by 19 referrals. Not Elgin and Lossiemouth, which leads only when the screen is run on the mart's weekly account totals, where a bypassed heating-only supply moves the account too little to clear the 30 per cent test. Not Lochaber, which has confirmed best over the last three winters but has the fewest referrals. Not Strathspey, whose heating-only supplies fell because heat pumps replaced storage heaters, a heating change RP-07 excludes. Not Inverness City, whose deepest falls are empty properties between occupiers.

## 2. Critical Components

1. Supplies referred in Caithness by the 7 December 2026 screening run: **54**
2. Supplies referred in Elgin and Lossiemouth: **35**

## 3. Step-by-Step Solution

1. Rebuilt weekly kWh (Monday 00:00 to Monday 00:00) for every supply number from `smart_daily_reads_2024-10-01_2026-12-07.parquet`, bridging meter exchanges with the reads on the register's Meter exchanges sheet and spreading comms gaps over their days.
2. Fitted each supply's weekly kWh on weekly 15.5 C degree days from its patch's station over the 104 weeks to 11 October 2026 (RP-07 section 3, `patch_weather_stations.json`).
3. Referred credit-account supplies whose kWh over the eight weeks to 6 December 2026 was 30 per cent or more below expected and below expected in every week (RP-07 section 4).
4. Dropped premises with a change of occupier or a heating change commissioned in those 112 weeks (RP-07 section 5), which removes Strathspey's heat pump premises and Inverness City's empty properties.
5. Counted referred supplies by patch: Caithness 54, Elgin and Lossiemouth 35.
6. For the winter history, kept one record per FieldLink job re-created in FieldOps (`legacy_job_no`), counted findings overturned in `tamper_appeals_register.xlsx` as no fault, and divided confirmations by visits with access (RP-07 section 8).
7. For capacity, counted 138 officer field days from 1 January to 31 March 2027 (Scottish public holidays, rota absences, the third officer from 15 February) and multiplied by FW-3's whole visits per day for each patch.
8. Recommendation: Caithness, 54 referrals.

## 4. Deliverable Answers

### field_team_q1_2027.pptx

1. Patch the team works in January to March 2027: Caithness
2. Referrals it starts the quarter with: 54
3. Runner-up: Elgin and Lossiemouth, 35 referrals
4. Referrals separating them: 19
5. Bar chart of referrals for all eight patches, largest first, Caithness highlighted, Elgin and Lossiemouth labelled as runner-up, title stating that Caithness gets the field team:
   - Caithness 54
   - Elgin and Lossiemouth 35
   - Inverness City 19
   - Skye and Lochalsh 17
   - Strathspey 16
   - Nairn and Ardersier 14
   - Forres 11
   - Lochaber 8
6. Every patch over the winters 2023/24 to 2025/26 (visits with access, diversions confirmed, confirmation rate) and the most visits the team could make there from 1 January to 31 March 2027:
   - Caithness: 41 visits, 17 confirmed, 41.5%, 552 visits
   - Elgin and Lossiemouth: 71 visits, 37 confirmed, 52.1%, 690 visits
   - Inverness City: 64 visits, 26 confirmed, 40.6%, 690 visits
   - Skye and Lochalsh: 29 visits, 13 confirmed, 44.8%, 414 visits
   - Strathspey: 33 visits, 15 confirmed, 45.5%, 552 visits
   - Nairn and Ardersier: 38 visits, 22 confirmed, 57.9%, 552 visits
   - Forres: 30 visits, 14 confirmed, 46.7%, 552 visits
   - Lochaber: 22 visits, 15 confirmed, 68.2%, 414 visits

### patch_screen_q1_2027.csv

1. Eight rows, one per patch, carrying each patch's referrals, winter visits with access, diversions confirmed, confirmation rate and Q1 visit capacity as listed above.
