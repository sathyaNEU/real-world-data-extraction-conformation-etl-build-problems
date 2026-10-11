# solver round: round 3, skeptic

**Proxy score 43.4 / 100** (recommendation 2.5 of 35, instruction 7.0 of 7, asks 33.9 of 58). Main call missed. 1 of 4 ask items cracked (80 per cent of tokens).

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
| read_health_by_build_wk41.png | 1 | 1 | 4 | 25% |

## Solver's path

1. fw_release_catalogue.csv: map each HES image to its release name (12 images).
2. hes_meter_firmware_history.json: remove duplicate events by event_id (275 duplicates, all identical), sort by ts_utc rather than seq (15 meters have late-stored events out of order), and take the build a meter runs from COMMISSIONED and FW_ACTIVATED only, ignoring FW_ACTIVATION_FAILED, FW_ROLLBACK_OK and FW_IMAGE_STAGED. Builds now reproduce all 12 cells of hes_firmware_census_20261012.csv exactly (for example EM3.12.0 IN_SERVICE 2242, REMOVED 19; EM3.12.2 IN_SERVICE 1291, BENCH 5).
3. Assessment week: Monday 05/10 to Sunday 11/10/2026 AEST, i.e. 2026-10-04T14:00Z to 2026-10-11T14:00Z. A meter is kept only if it runs the same build at both ends with no activation inside the week; 1172 Wave 7 meters change build in the week and are dropped.
4. mp_installation_register_20261012.xlsx Meters sheet: pad serials to 8 digits and join to HES meter_id (all 7959 match); 29 installations whose meter was removed on 08-09/10 are excluded; bench meters (12) are out of scope; join register NMI (11 chars) to MDM NMI (10 chars) on the first 10 characters.
5. Expected reads come from the Data streams sheet: 1440/interval reads per day x 7 days per stream (5-min streams give 288, 15-min 96, 30-min 48). All 12366 register streams match the MDM interval length.
6. mdm_interval_receipts: cut-off = READ_DATE 20:00Z (06:00 AEST next day). 86491 rows were received before it and 8649 after. For each NMI, suffix and read date the latest pre-cut-off delivery by RECEIVED_UTC counts, and its QTY_A is reads held; a stream-day with none counts as 0. Installation read health = held / expected x 100.
7. Build read health = mean over assessed installations; SE = sample SD (n-1) / sqrt(n); lower limit = 99.50 - 3*SE; the alert fires if read health < lower limit. Assessed counts: EM3.12.0 2242, EM3.11.4 1662, PX5.3.0 789, PX5.2.7 728, EM3.12.1 695, EM3.10.9 423, EM3.12.2 153, PX5.3.1 37. Result: 5 fire, 3 hold.
8. wave8_schedule.xlsx batches A and B: 1472 rows, 21 meters in both batches, serials padded and joined to HES and register. EM3.12.2 target has 1274 in-service meters not yet on the target (402 from EM3.11.4, 872 from EM3.12.0) but goes to 0 because the build fires. PX5.3.1 target: 118 distinct meters minus 9 already on PX5.3.1 = 109 in-service installations moved.
9. Substitution load: current in-service installations on firing builds = 2242 + 423 + 1291 + 695 + 728 = 5379.

confidence: medium-high: the build mapping matches the HES census exactly and the rule follows MDS-STD-114 r3 literally. The thinnest margins are PX5.3.0 holding by +0.12 points and EM3.12.2 firing by -0.43 points on 153 installations. The folder publishes no earlier read-health figures, so the method could not be tested against any.

notes: Planned interruptions are not excluded, because MDS-STD-114 gives no such exclusion. Deliveries after cut-off are ignored for read health even where they later supplied actual reads.

### wave8_read_health_alerts.json (solver's answers)
- fire list: fire = [EM3.12.0, EM3.10.9, EM3.12.2, EM3.12.1, PX5.2.7]
- hold list: hold = [PX5.3.0, EM3.11.4, PX5.3.1]
- record EM3.12.0 (1st): assessed installations 2242; read health 98.21%; standard error 0.09%; lower limit 99.22%; vs limit -1.01 percentage points; FIRE
- record EM3.10.9 (2nd): assessed installations 423; read health 98.06%; standard error 0.20%; lower limit 98.89%; vs limit -0.83 percentage points; FIRE
- record EM3.12.2 (3rd): assessed installations 153; read health 97.87%; standard error 0.40%; lower limit 98.30%; vs limit -0.43 percentage points; FIRE
- record EM3.12.1 (4th): assessed installations 695; read health 98.92%; standard error 0.06%; lower limit 99.32%; vs limit -0.40 percentage points; FIRE
- record PX5.2.7 (5th): assessed installations 728; read health 98.73%; standard error 0.15%; lower limit 99.05%; vs limit -0.32 percentage points; FIRE
- record PX5.3.0 (6th): assessed installations 789; read health 99.49%; standard error 0.04%; lower limit 99.37%; vs limit +0.12 percentage points; HOLD
- record EM3.11.4 (7th): assessed installations 1662; read health 99.57%; standard error 0.05%; lower limit 99.34%; vs limit +0.23 percentage points; HOLD
- record PX5.3.1 (8th): assessed installations 37; read health 98.98%; standard error 0.89%; lower limit 96.83%; vs limit +2.15 percentage points; HOLD
- Wave 8 moves onto EM3.12.2: 0 installations (all held because EM3.12.2 fires; 1274 would otherwise have moved)
- Wave 8 moves onto PX5.3.1: 109 installations
- substitution load: 5379 installations on a firing build (EM3.12.0 2242 + EM3.10.9 423 + EM3.12.2 1291 + EM3.12.1 695 + PX5.2.7 728)

### read_health_by_build_wk41.png (solver's answers)
- title: Read-health alert fires: EM3.12.0, EM3.10.9, EM3.12.2, EM3.12.1, PX5.2.7
- rows in order: EM3.12.0, EM3.10.9, EM3.12.2, EM3.12.1, PX5.2.7, PX5.3.0, EM3.11.4, PX5.3.1
- points (read health %, 2 dp): 98.21, 98.06, 97.87, 98.92, 98.73, 99.49, 99.57, 98.98
- lower-limit ticks (%, 2 dp): 99.22, 98.89, 98.30, 99.32, 99.05, 99.37, 99.34, 96.83
- reference line: 99.50%

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
