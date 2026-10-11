# solver round: round 2, skeptic

**Proxy score 54.5 / 100** (recommendation 2.5 of 35, instruction 7.0 of 7, asks 45.0 of 58). Main call missed. 3 of 5 ask items cracked (80 per cent of tokens).

## Main call

golden: Fire the read-health alert on PX5.2.7, EM3.12.1 and EM3.10.9, and hold PX5.3.0, EM3.11.4, EM3.12.0, PX5.3.1 and EM3.12.2 for Wave 8.

solver: The read-health alert fires on EM3.12.0, EM3.10.9, PX5.2.7, EM3.12.1 and EM3.12.2 and holds on PX5.3.0, EM3.11.4 and PX5.3.1.

tokens matched 1 of 2 (Fire, Wave)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| wave8_read_health_alerts.json | 1 | 2 | 2 | 100% |
| wave8_read_health_alerts.json | 2 | 15 | 24 | 62% |
| wave8_read_health_alerts.json | 3 | 4 | 4 | 100% |
| wave8_read_health_alerts.json | 4 | 6 | 6 | 100% |
| read_health_by_build_wk41.png | 1 | 1 | 4 | 25% |

## Solver's path

1. MDS-STD-114 r3: assessment week = Mon 05/10 00:00 to Sun 11/10 24:00 AEST (2026-10-04T14:00Z to 2026-10-11T14:00Z); cut-off = 06:00 AEST on read date + 1 (20:00Z on the read date); reference 99.50%; lower limit = 99.50 - 3*SE; SE = sample SD / sqrt(n)
2. hes_meter_firmware_history.json: 7971 meters, 49469 events; removed 249 re-ingested duplicate event_ids; ordered by ts_utc; build = last COMMISSIONED/FW_ACTIVATED image, so a failed activation plus rollback leaves the build unchanged (no failure lacked a rollback); image mapped to release via fw_release_catalogue.csv; 12 BENCH meters dropped
3. Joined HES meters to mp_installation_register Meters sheet on the serial zero-padded to 8 digits: 7959 matched (7930 current + 29 removed); all 12 unmatched are bench
4. Not assessed: 29 installations whose meter was changed 08-09/10 (local time) and 1172 meters with an FW_ACTIVATED in the week (Wave 7); 6729 installations assessed; builds at week end reconcile exactly to hes_firmware_census_20261012.csv
5. Expected reads from the Data streams sheet (12366 streams, 1:1 with MDM streams on the 10-character NMI): 7 x 1440/interval for each stream
6. mdm_interval_receipts: for each NMI/suffix/read date, took the latest delivery received before the cut-off and summed QTY_A (every delivery is complete; 614 first deliveries arrived 0.5-1.0 h after the cut-off, so those days count as 0 held); installation RH = held / expected x 100
7. Per build, over its own assessed installations only: mean, sample SD, SE, lower limit; fires if mean < LL; sorted by mean - LL ascending gives EM3.12.0 -0.85 ... PX5.3.1 +2.12; 5 fire, 3 hold
8. Wave 7: FW_ACTIVATED with job WAVE7-A/B in the week, market day = ts_utc + 10 h; missing = that day's expected intervals at the installation minus QTY_A held at cut-off; EM3.12.2 1109 / 16907, PX5.3.1 63 / 1101
9. wave8_schedule.xlsx (1472 rows): meter_id = serial zero-padded; dropped 21 meters appearing in both batches, REMOVED meters (22, all EM3) and meters already on the target as of the HES export (37 EM3.12.2, 9 PX5.3.1); eligible EM3.12.2 1274 (held, so 0 because it fires), PX5.3.1 109

confidence: medium-high: the method follows the standard literally and the build counts match the HES census exactly; the firing set depends on rule 3.5 excluding deliveries received after the cut-off (if they were counted, only EM3.12.1 and EM3.10.9 would fire), and EM3.12.2 fires by 0.35 points

notes: There were no earlier certified figures in the folder to reproduce; the only reconciliation was against the HES census, which matches for every image. The planned-interruption and comms_parent data were not used because the standard sets no exclusions for them.

### wave8_read_health_alerts.json (solver's answers)
- fire list: fire = [EM3.12.0, EM3.10.9, PX5.2.7, EM3.12.1, EM3.12.2] (in record order)
- hold list: hold = [PX5.3.0, EM3.11.4, PX5.3.1]
- per-build records, furthest below to furthest above lower limit: 1 EM3.12.0: read_health 98.39%, std_error 0.09%, lower_limit 99.24%, assessed_installations 2242, fire; 2 EM3.10.9: 98.06%, 0.20%, 98.89%, 423, fire; 3 PX5.2.7: 98.48%, 0.16%, 99.02%, 728, fire; 4 EM3.12.1: 98.92%, 0.06%, 99.32%, 695, fire; 5 EM3.12.2: 97.92%, 0.41%, 98.27%, 153, fire; 6 PX5.3.0: 99.49%, 0.04%, 99.37%, 789, hold; 7 EM3.11.4: 99.57%, 0.05%, 99.34%, 1662, hold; 8 PX5.3.1: 98.95%, 0.89%, 96.83%, 37, hold (all % to 2 dp; reference 99.50%)
- Wave 8 moves once call applied: onto EM3.12.2 = 0 installations (held; would have been 1274); onto PX5.3.1 = 109 installations
- Wave 7 moves this week and reads missing at cut-off on move day: EM3.12.2: 1109 installations moved (WAVE7-A 724, WAVE7-B 385), 16907 interval reads missing at cut-off on their market day of move (142704 expected - 125797 held); PX5.3.1: 63 installations moved (WAVE7-B), 1101 interval reads missing (9168 expected - 8067 held)

### read_health_by_build_wk41.png (solver's answers)
- title: Read-health alert fires: EM3.12.0, EM3.10.9, PX5.2.7, EM3.12.1, EM3.12.2
- rows in order with point and tick: EM3.12.0 point 98.39 / tick 99.24; EM3.10.9 98.06 / 98.89; PX5.2.7 98.48 / 99.02; EM3.12.1 98.92 / 99.32; EM3.12.2 97.92 / 98.27; PX5.3.0 99.49 / 99.37; EM3.11.4 99.57 / 99.34; PX5.3.1 98.95 / 96.83 (percent, 2 dp)
- reference line: vertical line at 99.50% labelled 99.50
