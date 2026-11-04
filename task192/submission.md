## Tags

**Domain:** Energy Systems & Utilities, grid reliability and outage analysis (finding the component breaking down on a distribution feeder from its protective devices' fault records).  
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Send the overhead line patrol crew to MLR-2 for the week of 9 November 2026, walking the main line from the Millrace feeder breaker MLR-F2-52 to recloser R-2207 at pole MLR2-P071 and the taps fused off it.** Its breaker has recorded 11 momentary faults on phase C at 1,423 to 1,448 A on separate mornings since 14 August, one place on the line failing again and again, against 7 at one current behind the second choice SYC-3's recloser R-3114. Not NYD-3, whose rise in non-storm momentary events per overhead mile is squirrels scattered along the feeder; not NYD-2, whose damp-morning blinks are wet limbs on overgrown taps; not BLV-3, whose phase B concentration is the phase of its taps.

## 2. Critical Components

1. MLR-2's breaker MLR-F2-52 recorded **11** momentary faults on phase C at **1,423 to 1,448 A**, each a single trip cleared on the first reclose, on separate mornings from 14 August to 31 October 2026.
2. SYC-3's recloser R-3114 recorded **7** on phase A at **996 to 1,005 A** from 23 September; no other feeder carries more than **5** at one phase and one current since 1 August.
3. The faults sit in the breaker's zone, so a failure there locks out the feeder and its **2,625** customers, against **863** behind R-3114.

## 3. Step-by-Step Solution

1. Read every momentary interruption event from soe_breakers_reclosers_2025_2026.csv (feeder breakers) and recloser_control_events_2025_2026.csv (operations within five minutes of the first, DRP-04 2.5), and took each one's first trip from feeder_relay_events_2025_2026.csv or the control's TRIP row (terminals to phases through protective_device_register.csv): its faulted phase and recorded current.
2. Grouped each device's momentary faults since 1 August 2026 by faulted phase and current within 2 per cent, counted on separate days: MLR-2's breaker 11 on phase C at 1,423 to 1,448 A, SYC-3's recloser 7, no other feeder above 5.
3. Took the stretch as the recording device's zone (DRP-04 5.4) from protective_device_register.csv: MLR-F2-52 to recloser R-2207 at MLR2-P071, 2,625 customers behind the breaker against 863 behind R-3114.
4. Found the 2026 major event days under DRP-04 4 (daily system SAIDI over 38.03 minutes on 35,404 customers): 19 May and 27 June.
5. Built every sustained interruption from oms_outage_history_2025_2026.xlsx (legacy child tickets timed from their parent's Out, incidents with their restoration steps) and the openings over five minutes that soe_breakers_reclosers_2025_2026.csv holds with no ticket, each reaching the service points below its device on the day through the register's dated rows and service_points_2026-10-31.csv; customers already without supply are not interrupted again, and a service ticket opened at the minute the device above closed is the same interruption carrying on: SAIDI by feeder.
6. Counted each customer's momentary interruption events under DRP-04 2.5: a device event reaches the customers below it, less those already out and those whose fuse or transformer fuse blew in the event's minute, and a customer's events within five minutes of the first are one: MAIFI-E by feeder.
7. Counted the service points each feeder supplies on 31 October with more than two of those sustained interruptions: CEMI-2 by feeder.
8. Sent the crew to MLR-2's breaker zone for the week of 9 November, SYC-3 next.

## 4. Deliverable Answers

### line_patrol_2026-11-09.xlsx

1. Patrol feeder: MLR-2; stretch to walk: the main line from the feeder breaker MLR-F2-52 to recloser R-2207 at pole MLR2-P071, with the taps fused off it.
2. Second choice: SYC-3 (recloser R-3114, 7 momentary faults on phase A at 996 to 1,005 A since 23 September).
3. What keeps it second: 11 repeat faults against 7, MLR-2's beginning 14 August against 23 September, and a failure on MLR-2 locks out the feeder breaker and 2,625 customers against R-3114's 863.
4. Minutes of interruption per customer served, January to October 2026, major event days (19 May and 27 June) left out, one decimal:
   - BLV-1: 308.4
   - BLV-2: 83.2
   - BLV-3: 169.2
   - CTR-1: 144.6
   - CTR-2: 208.4
   - CTR-3: 76.7
   - MLR-1: 301.1
   - MLR-2: 139.3
   - MLR-3: 87.7
   - NYD-1: 23.6
   - NYD-2: 411.5
   - NYD-3: 64.3
   - NYD-4: 113.7
   - SYC-1: 151.8
   - SYC-2: 126.9
   - SYC-3: 356.1
5. Momentary interruption events per customer served, same window, two decimals:
   - BLV-1: 5.77
   - BLV-2: 2.00
   - BLV-3: 27.23
   - CTR-1: 43.00
   - CTR-2: 37.35
   - CTR-3: 14.66
   - MLR-1: 13.72
   - MLR-2: 35.79
   - MLR-3: 14.60
   - NYD-1: 4.76
   - NYD-2: 47.12
   - NYD-3: 44.83
   - NYD-4: 3.68
   - SYC-1: 43.64
   - SYC-2: 45.29
   - SYC-3: 22.92
6. Customers with more than two sustained interruptions, same window:
   - BLV-1: 980
   - BLV-2: 7
   - BLV-3: 434
   - CTR-1: 113
   - CTR-2: 467
   - CTR-3: 15
   - MLR-1: 241
   - MLR-2: 1,030
   - MLR-3: 14
   - NYD-1: 0
   - NYD-2: 2,237
   - NYD-3: 0
   - NYD-4: 393
   - SYC-1: 1,950
   - SYC-2: 137
   - SYC-3: 2,325

### reliability_2026.svg

7. Scatter of each feeder's minutes of interruption per customer served against its momentary interruption events per customer served, MLR-2 labelled as the feeder the crew walks.
