# leak check, task250

**Verdict: REVIEW.** 12 files read, 4 golden figures and 4 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: record, network, station, drifts, section, re-run, reader, decisive, architecture, readings, export, inside, neighbour, statistic, policy, stated, reading, window, orders, checks, decision, sensor, programme, repair, change

## 3 answer figures in the pack (REVIEW 7)
- **REVIEW** `QC-02_control_calidad_temperatura_v4.pdf`: golden figure 4.5 appears: ...ewer. 7. Settings The setting is 3.0, 3.5, 4.0 or 4.5. A lower setting catches a drift sooner and raise...
- **REVIEW** `QC-02_control_calidad_temperatura_v4.pdf`: golden figure 3.5 appears: ...llation if fewer. 7. Settings The setting is 3.0, 3.5, 4.0 or 4.5. A lower setting catches a drift soon...
- **REVIEW** `QC-02_control_calidad_temperatura_v4.pdf`: golden figure 3.0 appears: ...installation if fewer. 7. Settings The setting is 3.0, 3.5, 4.0 or 4.5. A lower setting catches a drift...
- **REVIEW** `QC-02_control_calidad_temperatura_v4.pdf`: golden figure 4.0 appears: ...on if fewer. 7. Settings The setting is 3.0, 3.5, 4.0 or 4.5. A lower setting catches a drift sooner an...
- **REVIEW** `resumen_alertas_2027.pdf`: golden figure 3.0 appears: ...8 from control_calidad_2025-2027.parquet. Setting 3.0 all year. Alerts the quality control raised in 20...
- **REVIEW** `QC-02_control_calidad_temperatura_v4.pdf`: carries 10 of 11 distinctive words of the committed call: 'Run the 4.0 setting from the January 2028 configuration: it raises 18 drift alerts a year, within the 28 visits the fiel'
- **REVIEW** `plan_campo_2028.pdf`: carries 7 of 11 distinctive words of the committed call: 'Run the 4.0 setting from the January 2028 configuration: it raises 18 drift alerts a year, within the 28 visits the fiel'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `QC-02_control_calidad_temperatura_v4.pdf`: 12 of 25 stump-paragraph terms appear (record, network, station, section, readings, export); read whether the document names the move
- **REVIEW** `data_dictionary.md`: 9 of 25 stump-paragraph terms appear (record, network, station, section, export, statistic); read whether the document names the move
- **REVIEW** `plan_campo_2028.pdf`: 7 of 25 stump-paragraph terms appear (network, station, section, reading, checks, sensor); read whether the document names the move

## 6 ranking artifacts (REVIEW 2, INFO 1)
- **REVIEW** `boletin_et0_2027.csv`: names 4 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `registro_estaciones.xlsx`: names 4 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `resumen_alertas_2027.pdf`: names 4 of 4 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Ten isolated readers (Sonnet, medium) over five rounds, each on a fresh copy of prompt.txt and the unzipped pack only,
scored with score_reader.py against generator/figures.json. Every one missed the call. Rounds 1 and 2 (packs d98d06f8
and 9fe46047) filed 3.5 at 22 and 23; reader D took 24 of 24 asks once the visit was filed, which sent the ask layer to
v3. Rounds 3 and 4 on v3 (E, F, G, H) kept 2, 2, 2 and 3 of 24 ask figures; G found the cut-short drifts and not the
network re-run and filed 3.5 at 21. Round 5 on the shipped pack (target.zip 19727806): reader I filed 3.5 at 17 and kept
4 of 24 asks, reader J filed 3.5 at 12 and kept 2 of 24, both exit 0.

1. The decisive step: neither final reader found it stated. Both quoted QC-02 sections 6 and 7 as the sentences that
   fix the limits; I took section 9's growth sentence as the cue and built its own replay, which still kept 3.5 inside
   the visits (17 a year); J executed section 7 literally on the recorded statistic (3.5 at 12).
2. No file ranks the settings: the 2027 summary counts the alerts at the setting in force (3.0, 59 in 2027) only.
3. The dictionary read as orientation for the analyst in both; the request as the request.
4. No figure or name reads as the answer: the plan's 28 visits and the summary's 59 at 3.0 read as context.
5. Sections 6 and 7 read literally give 49, 12.3, 2.7 and 1 alerts a year on the 131 stations kept (both readers),
   which files 3.5; the golden adds one alert for each drift the 3.0 alerts' repairs cut short.
6. An analytical choice decides it in both reads; nothing reads as planted.

Asks: both final readers built the 2027 visits from the calibration readings and counted the workshop days under the
station's order as visit days (J saw readings near 0 and 40 degrees at two stations and kept them as a judgement call);
neither tested a reading against the station's logged daily range.

Realism: nothing reads as generated (the work orders' notes, the duplicated daily rows and the decimal commas read as
the systems' own, the judge's hygiene read agreeing).

REVIEW lines: all harmless (the procedure's menu of four settings; the setting in force in the 2027 summary; the field's
ordinary vocabulary in the procedure and the plan; the ET0 bulletin's and the register's numbers of other meaning).
