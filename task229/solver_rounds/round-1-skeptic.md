# solver round: round 1, skeptic

**Proxy score 87.4 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 45.4 of 58). Main call LANDED. 3 of 5 ask items cracked (80 per cent of tokens).

## Main call

golden: Fire the read-health alert on EM3.10.9, EM3.12.1 and PX5.2.7, and hold EM3.12.0, PX5.3.0, EM3.11.4, EM3.12.2 and PX5.3.1 for Wave 8.

solver: The read-health alert fires on PX5.2.7, EM3.10.9 and EM3.12.1, and holds on EM3.12.0, PX5.3.0, EM3.11.4, EM3.12.2 and PX5.3.1, so both Wave 8 targets (EM3.12.2 and PX5.3.1) hold and Wave 8 can go ahead.

tokens matched 2 of 2 (Fire, Wave)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| wave8_read_health_alerts.json | 1 | 2 | 2 | 100% |
| wave8_read_health_alerts.json | 2 | 16 | 24 | 67% |
| wave8_read_health_alerts.json | 3 | 4 | 4 | 100% |
| wave8_read_health_alerts.json | 4 | 6 | 6 | 100% |
| read_health_by_build_wk41.png | 1 | 1 | 4 | 25% |

## Solver's path

1. 1. MDS-STD-114 r3: the assessment week is Mon 05/10/2026 00:00 to Sun 11/10/2026 24:00 AEST (UTC+10), which is 2026-10-04T14:00Z to 2026-10-11T14:00Z; the delivery cut-off is 06:00 AEST on the day after the read date (20:00Z on the read date); a build's read health is the mean of its installations' read health; its lower limit is 99.50 minus 3 x (sample standard deviation / square root of n); the alert fires when read health is below the lower limit.
2. 2. hes_meter_firmware_history.json: 7971 meters; dropped 248 duplicate re-ingested event_ids; ordered events by ts_utc. A meter's build is set by COMMISSIONED or FW_ACTIVATED (staged, failed and rolled-back events are ignored); images mapped to release names with fw_release_catalogue.csv. The builds at census time (2026-10-11T13:00Z) match all 12 cells of hes_firmware_census_20261012.csv by image and status.
3. 3. Build at week start and week end: 1172 Wave 7 activations happened in the week (WAVE7-A 724, WAVE7-B 448, including 41 retries of rolled-back failures) and 29 new meters were commissioned.
4. 4. mp_installation_register Meters sheet: serials zero-padded to 8 digits (all 7959 join to HES; the 12 unmatched HES meters are bench meters); register NMIs cut to 10 characters to join the MDM. Excluded the 29 installations whose meter was changed on 08-09/10, meters activated during the week and bench meters. Result: 6729 assessed installations.
5. 5. Data streams sheet: expected reads = 7 x 1440 / interval length summed over each NMI's streams (all 86562 stream-days join the MDM, interval lengths agree).
6. 6. mdm_interval_receipts: per NMI, suffix and read date, kept the latest delivery received before READ_DATE 20:00Z (no ties; 153 stream-days had no delivery before the cut-off and count 0); held reads = QTY_A; installation read health = 100 x held / expected.
7. 7. Grouped by build: mean, sample standard deviation, standard error and lower limit; sorted by (read health - lower limit) to get the order PX5.2.7 -0.54, EM3.10.9 -0.43, EM3.12.1 -0.26, EM3.12.0 +0.06, PX5.3.0 +0.15, EM3.11.4 +0.36, EM3.12.2 +0.46, PX5.3.1 +2.13.
8. 8. wave8_schedule.xlsx Batch A (726 rows) + Batch B (746 rows) = 1472; removed 21 meters listed in both batches, leaving 1451 unique (EM3.12.2 1333, PX5.3.1 118); dropped 22 meters removed from their installations (status REMOVED) and 46 already on the target image (37 EM3.12.2, 9 PX5.3.1), as the HES job skips these. Moves: EM3.12.2 1274, PX5.3.1 109.
9. 9. Wave 7: successful WAVE7 FW_ACTIVATED events in the week, market day = AEST date of the activation; missing reads = that installation's expected reads for the day minus QTY_A held at the cut-off. EM3.12.2: 1109 installations, 17455 missing; PX5.3.1: 63 installations, 933 missing.

confidence: high on the fire/hold split and all counts (the method matches all 12 census cells exactly); medium-high on EM3.12.0 holding, since its margin is only 0.06 percentage points

notes: PX5.2.7 fires only because so many of its reads arrive after the 06:00 AEST cut-off (with late deliveries counted it would be 99.89%). Carrier maintenance notices were not used because the standard has no exclusion for them, and the chart's EM3.10.9 row is point 98.55%, tick 98.98%.

### wave8_read_health_alerts.json (solver's answers)
- fire list: fire = [PX5.2.7, EM3.10.9, EM3.12.1] (3 builds)
- hold list: hold = [EM3.12.0, PX5.3.0, EM3.11.4, EM3.12.2, PX5.3.1] (5 builds)
- per-build records, ordered furthest below to furthest above lower limit: 1 PX5.2.7: assessed installations 728, read health 98.45%, lower limit 98.99%, fire; 2 EM3.10.9: 423, 98.55%, 98.98%, fire; 3 EM3.12.1: 695, 99.13%, 99.39%, fire; 4 EM3.12.0: 2242, 99.44%, 99.38%, hold; 5 PX5.3.0: 789, 99.51%, 99.36%, hold; 6 EM3.11.4: 1662, 99.78%, 99.42%, hold; 7 EM3.12.2: 153, 99.85%, 99.39%, hold; 8 PX5.3.1: 37, 98.96%, 96.83%, hold (percentages to 2 dp, counts whole)
- Wave 8 installations moved onto each target if it goes ahead: EM3.12.2: 1274 installations; PX5.3.1: 109 installations (whole numbers)
- Wave 7 moves this week and reads missing at cut-off on the move day: EM3.12.2: 1109 installations moved, 17455 interval reads missing at cut-off (06/10: 264 moved, 1242 missing; 07/10: 602, 12569; 08/10: 243, 3644); PX5.3.1: 63 installations moved, 933 interval reads missing (07/10: 25, 274; 08/10: 38, 659)

### read_health_by_build_wk41.png (solver's answers)
- title: Read-health alert fires on PX5.2.7, EM3.10.9 and EM3.12.1 (week 41, 05-11 Oct 2026)
- rows in order with labels, points and ticks: PX5.2.7 (n=728) point 98.45% tick 98.99%; EM3.10.9 (n=423) 98.45->98.55% point, tick 98.98%; EM3.12.1 (n=695) point 99.13% tick 99.39%; EM3.12.0 (n=2242) point 99.44% tick 99.38%; PX5.3.0 (n=789) point 99.51% tick 99.36%; EM3.11.4 (n=1662) point 99.78% tick 99.42%; EM3.12.2 (n=153) point 99.85% tick 99.39%; PX5.3.1 (n=37) point 98.96% tick 96.83%
- reference line: line at 99.50%, labelled 99.50%
