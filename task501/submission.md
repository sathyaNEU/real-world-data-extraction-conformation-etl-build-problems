## Tags

**Domain:** Energy Systems & Utilities (asset condition and maintenance: water distribution trunk mains).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Flush two mains before the relining starts on 15 March 2027: TM112 Coldharbour Road main and IC05 Coldharbour-Ferrars interconnector.**
TM112 will carry 140 l/s during the works against at most 65 l/s in November 2025 to October 2026, and IC05 121 l/s against none. Not TM104, TM109, TM110 or IC03: the relining loads them to 229, 179, 124 and 84 l/s, below the 263, 228, 177 and 141 l/s they carried in the June and July 2026 Mill Road jobs. Not all six mains the relining loads, which is what flows read through the register's normal valve positions give.

## 2. Critical Components

1. The relining arrangement sends more water through six trunk mains in every hour: TM104, TM109, TM110, TM112, IC03 and IC05.
2. Highest hourly flow during the works: TM104 **229**, TM109 **179**, TM110 **124**, TM112 **140**, IC03 **84** and IC05 **121** l/s.
3. Highest hourly flow carried in November 2025 to October 2026, through the valve positions in force each hour: TM104 **263**, TM109 **228**, TM110 **177**, TM112 **65**, IC03 **141** and IC05 **0** l/s.

## 3. Step-by-Step Solution

1. Read nos12_planned_supply_route_changes_issue3.pdf (section 4) and tm107_ferrars_lane_relining_outage_plan_v1.pdf: the reference is November 2025 to October 2026, works flows are judged on the districts' inflows for 15 March to 15 September 2026, and the plan opens the IC05 and IC03 boundary valves and shuts TM115 and TM107.
2. Built the network from trunk_mains_register_2026-11.xlsx (mains by junction, valves by main, districts by inlet junction) and read dma_inlet_flows_2025-11_2026-10.csv on UTC hours, re-sent rows dropped and blank hours left out.
3. Routed the 15 March to 15 September 2026 inflows through the plan's valve positions: six mains carry more than in normal running in every hour, peaking at 229 (TM104), 179 (TM109), 124 (TM110), 140 (TM112), 84 (IC03) and 121 (IC05) l/s.
4. Applied every OPEN and CLOSE on a register valve in control_room_valve_log_2025-11_2026-10.csv (local time to UTC) to get the positions in force each hour, among them TM105 out from 13 April to 19 June with Brook End fed through IC02, TM108 out from 24 to 27 June with Mill Bridge and Sallowby fed through IC03 and TM115, and TM108 out from 20 to 22 July with Mill Bridge fed through IC08.
5. Routed every hour's inflows through that hour's positions: the highest hourly flow carried was 263 (TM104), 228 (TM109), 177 (TM110), 65 (TM112), 141 (IC03) and 0 (IC05) l/s.
6. Flushing water: from mains_flushing_job_sheets_2025-26.csv, dropped re-sent rows, differenced crew C14's volume_m3 within each night from 1 December 2025 (a running meter reading, each later figure well above that row's gauge flow times its minutes), added the two hydrants of a twin-hydrant flush and counted its section length once, then divided water by length by diameter and year of night_of.
7. Non-household water: summed nonhousehold_monthly_consumption_2025-04_2026-10.csv for 2025-11 to 2026-10 by SPID; the logged supply points AMR6641, AMR7233, AMR8131, AMR8432 use more in some hours than their recorded DMA's whole inflow (amr_large_users_hourly_2025-11_2026-10.csv against the inlet meters) and were placed in the neighbouring DMA whose inflow carries their load steps (AMR6641 from BRK146 to BRK142; AMR7233 from BRK137 to BRK134; AMR8131 from BRK155 to BRK153; AMR8432 from BRK168 to BRK155).
8. Compared each main's works peak with its highest hourly flow carried (NOS 12 section 4): only TM112 and IC05 pass it, so those two are flushed and the other four are not.

## 4. Deliverable Answers

### ferrars_lane_flushing_2027.xlsx

1. Flush two mains before the relining starts on 15 March 2027: TM112 Coldharbour Road main and IC05 Coldharbour-Ferrars interconnector.
2. Trunk mains the relining arrangement sends more water through, highest hourly flow during the works (l/s) and whether to flush:
   - IC03 Highfield-Sallowby interconnector: 84 l/s, no flush
   - IC05 Coldharbour-Ferrars interconnector: 121 l/s, flush
   - TM104 Eastgate main: 229 l/s, no flush
   - TM109 North Road main: 179 l/s, no flush
   - TM110 Highfield main: 124 l/s, no flush
   - TM112 Coldharbour Road main: 140 l/s, flush
3. Water used per 100 m of main flushed, 2025-26 flushing programme (m3 per 100 m):
   - 75 mm: 1.5 in 2025, 1.5 in 2026
   - 100 mm: 2.7 in 2025, 2.7 in 2026
   - 150 mm: 6.1 in 2025, 6.2 in 2026
   - 225 mm: 13.8 in 2025, 14.0 in 2026
   - 300 mm: 23.0 in 2025, 22.1 in 2026
4. Water used from November 2025 to October 2026 by the non-household customers each re-routed district supplies (Ml):
   - BRK134 Ferrars: 141.9
   - BRK137 St Anne's: 40.5
   - BRK142 Mill Bridge: 203.2
   - BRK146 Weir Lane: 85.7
   - BRK153 Sallowby: 160.7
   - BRK155 Sallowby Park: 104.4
   - BRK168 Hollow Lane: 26.7

### ferrars_lane_flushing_note.pdf

1. One page that leads with the call and charts each of the six mains' highest hourly flow during the works as a bar (TM112 and IC05 in orange, the others in blue), each with a marker at the highest hourly flow it carried in November 2025 to October 2026.
