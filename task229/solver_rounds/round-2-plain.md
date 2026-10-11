# solver round: round 2, plain

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

1. MDS-STD-114 r3 PDF: assessment week = 05/10/2026 to 11/10/2026 AEST (UTC 2026-10-04T14:00Z to 2026-10-11T14:00Z); cut-off = read date +1 06:00 AEST; reference 99.50; lower limit = 99.50 - 3 x sample SD / sqrt(n)
2. hes_meter_firmware_history.json: removed 249 duplicated event_ids, sorted by ts_utc not seq, build changes only on COMMISSIONED/FW_ACTIVATED, failed activations rolled back; current-build counts match hes_firmware_census_20261012.csv exactly; 1172 activations in the week (WAVE7-A/B), no meter activated twice
3. fw_release_catalogue.csv: HES image -> release name
4. mp_installation_register Meters: serial as integer (leading zeros differ) joined to HES meter_id digits, 7959 matched, 12 BENCH HES meters unmatched; 29 NMIs had a meter changed 08-09/10 -> not assessed
5. Data streams sheet (NMI first 10 chars) joined to MDM receipts: all 94912 rows matched, interval lengths agree; expected = 7 x 1440/interval summed per NMI
6. mdm_interval_receipts: kept deliveries with RECEIVED_UTC < cut-off, latest per NMI/suffix/read date, summed QTY_A per NMI -> installation read health = held actual / expected x 100
7. Assessed = IN_SERVICE meter, NMI with no meter change, no activation inside the week -> 6729 installations; mean, sample SD, SE, LL per build; fire if mean < LL -> 5 fire, 3 hold; sorted by (read health - LL) ascending
8. Wave 7: WAVE7 activations in week -> EM3.12.2 1109, PX5.3.1 63 installations; market day = AEST date of activation; missing = expected intervals that day - held-at-cut-off actuals -> 16907 and 1101
9. wave8_schedule.xlsx both batches: 1472 rows, serials as integers, 21 serials in both batches deduplicated; dropped meters already on the target image and REMOVED meters -> EM3.12.2 eligible 1274 (held because it fires, so 0), PX5.3.1 123 rows / 118 unique / minus 9 already on target = 109

confidence: high for the fire/hold split and figures under the standard as written; the split rests on applying the 06:00 cut-off (counting late deliveries would flip EM3.12.0, PX5.2.7 and EM3.12.2 to hold)

notes: The planned-interruption file was not used because the standard has no outage exclusion. 'Missing at cut-off' counts every expected interval without an actual read in the latest on-time delivery (substituted or estimated values count as missing).

### wave8_read_health_alerts.json (solver's answers)
- fire list: fire = [EM3.12.0, EM3.10.9, PX5.2.7, EM3.12.1, EM3.12.2]
- hold list: hold = [PX5.3.0, EM3.11.4, PX5.3.1]
- per-build records, furthest below limit first: EM3.12.0: read health 98.39%, SE 0.09%, lower limit 99.24%, assessed installations 2242; EM3.10.9: 98.06%, SE 0.20%, LL 98.89%, n 423; PX5.2.7: 98.48%, SE 0.16%, LL 99.02%, n 728; EM3.12.1: 98.92%, SE 0.06%, LL 99.32%, n 695; EM3.12.2: 97.92%, SE 0.41%, LL 98.27%, n 153; PX5.3.0: 99.49%, SE 0.04%, LL 99.37%, n 789; EM3.11.4: 99.57%, SE 0.05%, LL 99.34%, n 1662; PX5.3.1: 98.95%, SE 0.89%, LL 96.83%, n 37 (all percentages to 2 dp, counts whole)
- Wave 8 moves after call: onto EM3.12.2 = 0 installations (fires; 1274 eligible moves held); onto PX5.3.1 = 109 installations
- Wave 7 moves this week and reads missing at cut-off: EM3.12.2: 1109 installations moved, 16907 interval reads missing at delivery cut-off on their move market day; PX5.3.1: 63 installations moved, 1101 interval reads missing

### read_health_by_build_wk41.png (solver's answers)
- title: Read-health alert fires: EM3.12.0, EM3.10.9, PX5.2.7, EM3.12.1, EM3.12.2
- rows in order with point and limit tick: EM3.12.0 98.39 / 99.24; EM3.10.9 98.06 / 98.89; PX5.2.7 98.48 / 99.02; EM3.12.1 98.92 / 99.32; EM3.12.2 97.92 / 98.27; PX5.3.0 99.49 / 99.37; EM3.11.4 99.57 / 99.34; PX5.3.1 98.95 / 96.83 (read health % / lower limit %, 2 dp)
- reference line: 99.50% labelled on the line
