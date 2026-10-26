## Tags

**Domain:** Physical & Environmental Sciences, emissions inventory (an upstream oil producer's 2026 release-event methane return to its provincial energy board, conformed from two lease operator apps, an event register, a SCADA alarm journal, daily production and tank vapour analyses, with its fugitive emissions schedule from the leak survey log and tracker).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Budget CAD 171,000 for Vennholt Energy's 2027 release-event levy: its 2026 return falls in band C, at 54.5 t of release-event methane, CAD 950 for each of its 180 batteries.**
The band rests on when the undated events began, read from all of the operator's 2026 windows between visits: open hatches turn up more often after long windows than after short ones, but far less than in proportion to the window, because a share of them is left open by the departing visit and vents the whole window. Not band B, which starting every undated event halfway through its window gives: it prices the hatches the departing visit left open at half their windows. Not band E, which starting every hatch at the previous departure gives: most hatches open between visits.

## 2. Critical Components

1. Release events found in 2026: **1,660** (1,425 open thief hatches, 58 combustor pilots out, 177 relief valves not reseated, 54 of them timed by a tank pressure alarm).
2. Release-event methane for 2026: **54.5 t** on the fit of all the year's windows, band C.

## 3. Step-by-Step Solution

1. Joined each event in release_event_register_2026.xlsx to the visit that found it in route_app_visits_20251215_20260630.csv or checkin_app_visits_20260615_20270112.jsonl (check-in app re-entries within ten minutes and the June visits logged in both apps taken once, BT-0907 read as BT-0907A): 1,660 events, each with its window since the previous visit left.
2. Started each relief valve that did not reseat at a telemetered battery at the first alarm of the last lift before its find in scada_alarm_journal_20251215_20270112.csv, on the RTU's clock: 54 events.
3. Fitted, for each kind over all of the operator's 2026 windows, the chance that a window ends in an event of that kind as a share started as the previous visit left plus a rate an hour, by maximum likelihood, and took every other start at its expected value given its window (Directive 17 s.3.2), each hour at the battery's tank vapour methane that day (s.3.3) from battery_daily_production_20251215_20261231.csv and tank_vapour_analyses_2025_2026.xlsx: 54.5 t, band C.
4. Placed each tag in ldar_leak_tracker_20270112.xlsx at its battery's survey in ldar_surveys_2025_2026.csv, the last on or before the day it reached the tracker, reading a battery's surveys as the sessions that screened its points (the 318 re-checks of a few repaired fittings are not surveys), and took a tag hung on a component whose earlier tag had not been repaired by that survey as the same leak found again (Directive 17 s.5.2).
5. Took each leak's repair from the last leak repair in maintenance_work_orders_2026.csv that names its tag, a contract order's on its field ticket's day (the 251 contract orders were completed when the foreman approved their tickets, on the 10th of the next month or the next working day): 36 tags the tracker closed on a first repair were still leaking at a re-check, and their leaks run to the later work order.
6. Vented each leak from its battery's last survey before it was first found to its repair, at the rate measured then, split at 1 July and kept inside 2026, and carried each half by the run that served the battery then: the route app's Route to 30 June and the check-in app's run from 1 July, not the 2027 runs in battery_register_20270108.csv (12 batteries changed run on 1 July 2026 and 12 on 4 January 2027).
7. Recommended budgeting the band C levy of CAD 171,000 for 2027.

## 4. Deliverable Answers

### release_events_2026.csv

1. One row per release event found in 2026 in the Board's schema, 1,660 rows (1,425 HATCH, 58 COMBUSTOR, 177 RELIEF), each with its start, start basis (ALARM for 54, EXPECTED for the rest), find, closure, active hours and methane.

### release_levy_filing_2026.xlsx

1. Release-event methane for 2026: 54.5 t; band C; 2027 levy CAD 171,000 (CAD 950 for each of 180 batteries).
2. Schedule B, fugitive methane by route, tonnes, January to June and July to December:
   - R01: 8.8 and 7.8
   - R02: 10.6 and 3.2
   - R03: 8.2 and 3.7
   - R04: 11.2 and 11.1
   - R05: 4.3 and 3.3
   - R06: 6.1 and 4.0
   - R07: 12.7 and 4.3
   - R08: 6.2 and 4.2
   - R09: 7.4 and 3.7
   - R10: 12.3 and 7.8
   - R11: 10.3 and 3.9
   - R12: 5.7 and 4.8
