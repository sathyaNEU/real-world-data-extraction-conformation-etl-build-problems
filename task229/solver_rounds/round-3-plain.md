# solver round: round 3, plain

**Proxy score 47.0 / 100** (recommendation 2.5 of 35, instruction 7.0 of 7, asks 37.5 of 58). Main call missed. 1 of 4 ask items cracked (80 per cent of tokens).

## Main call

golden: Fire the read-health alert on EM3.12.1, EM3.10.9 and PX5.2.7, and hold PX5.3.0, EM3.12.0, EM3.11.4, PX5.3.1 and EM3.12.2 for Wave 8.

solver: The read-health alert fires on EM3.12.0, EM3.10.9, EM3.12.2, EM3.12.1 and PX5.2.7, and holds on PX5.3.0, EM3.11.4 and PX5.3.1.

tokens matched 1 of 2 (Fire, Wave)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| wave8_read_health_alerts.json | 1 | 20 | 34 | 59% |
| wave8_read_health_alerts.json | 2 | 4 | 4 | 100% |
| wave8_read_health_alerts.json | 3 | 1 | 2 | 50% |
| read_health_by_build_wk41.png | 1 | 2 | 4 | 50% |

## Solver's path

1. MDS-STD-114 r3: assessment week 05/10-11/10/2026 AEST = 2026-10-04T14:00Z to 2026-10-11T14:00Z; cut-off 06:00 AEST on read date +1 = 20:00Z on the read date; reference 99.50 %; lower limit = 99.50 - 3*SE; SE = sample SD (n-1)/sqrt(n); mean of installation read health; only the build's own assessed installations
2. hes_meter_firmware_history.json (7971 meters): dropped 275 replayed duplicate event_ids, sorted by ts_utc (15 meters have seq order different from ts order), build = image of the latest COMMISSIONED/FW_ACTIVATED; FAILED, ROLLBACK_OK and STAGED do not change the build; mapped images to releases via fw_release_catalogue.csv; 12 BENCH meters excluded
3. mp_installation_register Meters: serials zero-padded to 8 digits, 7959/7959 joined to HES; Installed/Removed taken as Australia/Sydney local time (AEDT); 29 installations had a meter changed during the week (removed 8-9 Oct) and are not assessed
4. Assessed = covering meter, no meter change, no activation inside the week: 6729 installations (EM3.12.0 2242, EM3.11.4 1662, PX5.3.0 789, PX5.2.7 728, EM3.12.1 695, EM3.10.9 423, EM3.12.2 153, PX5.3.1 37); Wave 7 meters activated during the week are excluded
5. Expected reads = register Data streams (12366 streams, all active before the week) x 7 x 1440/interval; register NMI first 10 characters joined to the MDM 10-character NMI, all streams matched, interval lengths agree
6. mdm_interval_receipts: for each NMI/suffix/read date, kept the latest delivery with RECEIVED_UTC before the cut-off (85973 of 86562 stream-days); held = QTY_A summed; missing stream-days count 0 held; installation read health = 100*held/expected
7. Per-build mean, sample SD, SE, lower limit and gap; fires if read health < lower limit -> 5 fire, 3 hold (without the cut-off rule all would sit near 99.0-99.9 %)
8. wave8_schedule.xlsx batches A+B: 1472 rows; serials padded, 21 duplicates across batches removed; skipped meters already on the target and REMOVED meters (per the Notes sheet); EM3.12.2 1274 candidates -> 0 because it fires; PX5.3.1 118 unique - 9 already on target = 109
9. Substitution load: current installation meters (Removed blank, 7930) by current HES build, counting firing builds = 5379; matches hes_firmware_census_20261012.csv IN_SERVICE counts exactly

confidence: medium-high: the figures reconcile with the census and the stream/meter joins are complete; the substitution-load scope (all current installations rather than only assessed ones) is the main interpretive choice

notes: Planned interruptions were not excluded because MDS-STD-114 counts every interval as expected. If the substitution load were limited to assessed installations it would be 4241 rather than 5379.

### wave8_read_health_alerts.json (solver's answers)
- fire list: fire = [EM3.12.0, EM3.10.9, EM3.12.2, EM3.12.1, PX5.2.7] (5 builds)
- hold list: hold = [PX5.3.0, EM3.11.4, PX5.3.1] (3 builds)
- record EM3.12.0: order 1; read health 98.21 %; standard error 0.09 %; lower limit 99.22 %; gap -1.01 % (below); assessed installations 2242; FIRE
- record EM3.10.9: order 2; read health 98.06 %; standard error 0.20 %; lower limit 98.89 %; gap -0.83 % (below); assessed installations 423; FIRE
- record EM3.12.2: order 3; read health 97.87 %; standard error 0.40 %; lower limit 98.30 %; gap -0.43 % (below); assessed installations 153; FIRE
- record EM3.12.1: order 4; read health 98.92 %; standard error 0.06 %; lower limit 99.32 %; gap -0.40 % (below); assessed installations 695; FIRE
- record PX5.2.7: order 5; read health 98.73 %; standard error 0.15 %; lower limit 99.05 %; gap -0.32 % (below); assessed installations 728; FIRE
- record PX5.3.0: order 6; read health 99.49 %; standard error 0.04 %; lower limit 99.37 %; gap +0.12 % (above); assessed installations 789; HOLD
- record EM3.11.4: order 7; read health 99.57 %; standard error 0.05 %; lower limit 99.34 %; gap +0.23 % (above); assessed installations 1662; HOLD
- record PX5.3.1: order 8; read health 98.98 %; standard error 0.89 %; lower limit 96.83 %; gap +2.15 % (above); assessed installations 37; HOLD
- Wave 8 moves onto EM3.12.2: 0 installations (held because EM3.12.2 fires; would have been 1274)
- Wave 8 moves onto PX5.3.1: 109 installations
- substitution load: 5379 installations on firing builds (EM3.12.0 2242 + EM3.12.2 1291 + PX5.2.7 728 + EM3.12.1 695 + EM3.10.9 423)

### read_health_by_build_wk41.png (solver's answers)
- title: names the firing builds: EM3.12.0, EM3.10.9, EM3.12.2, EM3.12.1, PX5.2.7
- row order: EM3.12.0, EM3.10.9, EM3.12.2, EM3.12.1, PX5.2.7, PX5.3.0, EM3.11.4, PX5.3.1 (8 rows)
- points and ticks: read health point / lower limit tick, % 2dp: EM3.12.0 98.21/99.22; EM3.10.9 98.06/98.89; EM3.12.2 97.87/98.30; EM3.12.1 98.92/99.32; PX5.2.7 98.73/99.05; PX5.3.0 99.49/99.37; EM3.11.4 99.57/99.34; PX5.3.1 98.98/96.83
- reference line: 99.50 % labelled on the line

## Main thread's read (worth-it gate)

Path: R4. The solver executed MDS-STD-114 to the letter and gave the mean the textbook error ("SE =
sample SD (n-1)/sqrt(n)"), with no use of `comms_parent`; it fired EM3.12.0, EM3.10.9, EM3.12.2,
EM3.12.1 and PX5.2.7. Main call missed at the error-unit step, which the pack's own structure decides
(design note, `## Stump or fork`): a stump, not a fork.

Facts against the golden, at the prompt's rounding (both round-3 solvers filed identical figures):

| Criterion | Golden | Solver | Kept |
|---|---|---|---|
| fire list, hold list, order | 3 fire, 5 hold | 5 fire, 3 hold | 0 of 3 |
| read health, 8 builds | | identical | 8 of 8 |
| standard error, 8 builds | node-level | installation-level | 0 of 8 |
| lower limit, 8 builds | | | 0 of 8 |
| distance from the limit, 8 builds | | | 0 of 8 |
| alert per build | | EM3.12.0 and EM3.12.2 wrong | 6 of 8 |
| Wave 8 onto EM3.12.2, onto PX5.3.1 | 1,274 / 109 | 0 / 109 | 1 of 2 |
| substitution load | 1,846 | 5,379 | 0 of 1 |
| chart: title, order, points, ticks, reference | | | 2 of 5 |

17 of 51 ask criteria kept, a third. With the recommendation's surviving components at about 5 and
instruction following at 7, the criterion-level read is about 31; on grade.py's own four-item
weighting with each item read for what the solver actually filed, about 27.

Why grade.py's decimal is higher: its number match accepts anything within 0.5 per cent of the
golden value, which on percentages near 99 is about 0.49 points, so wrong limits (98.89 for 98.40,
99.32 for 99.30, 99.34 for 99.05) count as hits; it matches numbers anywhere in an answer rather than
on their build (0.05, 0.15, 0.23 and 99.05 each appear somewhere in the solver's text for another
build); it credits the Wave 8 item from the eligible "1274" the solver quoted beside its committed 0;
and the substitution-load item's capitalised word scores half of it. With the tolerance set to the
prompt's rounding the decimal is 44.5 (plain) and 40.8 (skeptic); the remaining excess is the
unbound matches, the quoted 1274 and the word token.
