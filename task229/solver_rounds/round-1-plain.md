# solver round: round 1, plain

**Proxy score 91.3 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 49.3 of 58). Main call LANDED. 4 of 5 ask items cracked (80 per cent of tokens).

## Main call

golden: Fire the read-health alert on EM3.10.9, EM3.12.1 and PX5.2.7, and hold EM3.12.0, PX5.3.0, EM3.11.4, EM3.12.2 and PX5.3.1 for Wave 8.

solver: The read-health alert fires on PX5.2.7, EM3.10.9 and EM3.12.1, and holds on EM3.12.0, PX5.3.0, EM3.11.4, EM3.12.2 and PX5.3.1 (both Wave 8 targets hold, so those moves can proceed).

tokens matched 2 of 2 (Fire, Wave)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| wave8_read_health_alerts.json | 1 | 2 | 2 | 100% |
| wave8_read_health_alerts.json | 2 | 24 | 24 | 100% |
| wave8_read_health_alerts.json | 3 | 4 | 4 | 100% |
| wave8_read_health_alerts.json | 4 | 6 | 6 | 100% |
| read_health_by_build_wk41.png | 1 | 1 | 4 | 25% |

## Solver's path

1. MDS-STD-114 r3 PDF: assessment week Mon 05/10 00:00 to Sun 11/10 24:00 AEST (UTC 2026-10-04T14:00Z to 2026-10-11T14:00Z); delivery cut-off 06:00 AEST the day after the read date (READ_DATE 20:00 UTC); reference 99.50; lower limit = 99.50 - 3*sample SD/sqrt(n); fire if mean < lower limit
2. hes_meter_firmware_history.json: removed 248 duplicate event_ids (repeat ingests); the build is set by COMMISSIONED/FW_ACTIVATED only (staged, and failed then rolled back, events ignored); builds at the time of export matched hes_firmware_census_20261012.csv for every image and status
3. fw_release_catalogue.csv: hes_image -> release name
4. mp_installation_register Meters: serial zero-padded to 8 digits and joined to HES MTR-<serial> (7959/7959 matched; 12 BENCH HES meters are not in the register and are excluded); NMI cut to 10 characters for the MDM join; Installed/Removed converted from Australia/Sydney time to UTC; 29 NMIs had a meter exchange on 08-09/10 and were excluded
5. Assessed installations: meter in place all week, no activation in the week, not bench = 6729 (EM3.10.9 423, EM3.11.4 1662, EM3.12.0 2242, EM3.12.1 695, EM3.12.2 153, PX5.2.7 728, PX5.3.0 789, PX5.3.1 37)
6. Data streams sheet: expected reads = 7 x sum over streams of 1440/interval (5/15/30 min); MDM interval lengths match the register for all 12366 streams
7. mdm_interval_receipts: for each NMI/suffix/read date, kept the latest delivery received before the cut-off (86409 of 86562 stream-days have one) and summed QTY_A = reads held; installation read health = held/expected*100; build = mean of its installations, sample SD, SE, limit as above -> 3 fire, 5 hold
8. Wave 7: successful FW_ACTIVATED events in the week with job WAVE7-A/B joined to the register; EM3.12.2 1109 NMIs, PX5.3.1 63 NMIs; market day = activation time + 10h; missing = expected minus held for that NMI and day -> 17455 and 933
9. wave8_schedule.xlsx both batches (1472 rows): Meter No zero-padded; 21 serials appear in both batches (counted once); removed 22 REMOVED meters and 46 meters already on target -> distinct installations EM3.12.2 1274, PX5.3.1 109

confidence: high

notes: The verdicts are the same whether the cut-off is in AEST or AEDT; ignoring the cut-off would flip PX5.2.7 to hold, so its failure comes from late deliveries, which the standard excludes. EM3.12.0 is the closest hold, 0.06 points above its lower limit.

### wave8_read_health_alerts.json (solver's answers)
- fire list: fire = [PX5.2.7, EM3.10.9, EM3.12.1]
- hold list: hold = [EM3.12.0, PX5.3.0, EM3.11.4, EM3.12.2, PX5.3.1]
- per-build records in order (assessed installations; read health %, 2dp; lower limit %, 2dp): PX5.2.7: 728; 98.45; 98.99 | EM3.10.9: 423; 98.55; 98.98 | EM3.12.1: 695; 99.13; 99.39 | EM3.12.0: 2242; 99.44; 99.38 | PX5.3.0: 789; 99.51; 99.36 | EM3.11.4: 1662; 99.78; 99.42 | EM3.12.2: 153; 99.85; 99.39 | PX5.3.1: 37; 98.96; 96.83
- Wave 8 installations moved onto targets: EM3.12.2 = 1274 installations; PX5.3.1 = 109 installations
- Wave 7 moves this week and reads missing at cut-off on move day: EM3.12.2: 1109 installations moved, 17455 interval reads missing; PX5.3.1: 63 installations moved, 933 interval reads missing

### read_health_by_build_wk41.png (solver's answers)
- title: Alert fires on PX5.2.7, EM3.10.9, EM3.12.1
- rows in order with assessed-installation labels, read-health point and lower-limit tick (%, 2dp): PX5.2.7 (n=728) 98.45 / 98.99; EM3.10.9 (n=423) 98.55 / 98.98; EM3.12.1 (n=695) 99.13 / 99.39; EM3.12.0 (n=2242) 99.44 / 99.38; PX5.3.0 (n=789) 99.51 / 99.36; EM3.11.4 (n=1662) 99.78 / 99.42; EM3.12.2 (n=153) 99.85 / 99.39; PX5.3.1 (n=37) 98.96 / 96.83
- reference line: 99.50%
