## Tags

**Domain:** Physical & Environmental Sciences (sensor calibration and measurement: the daily spatial-consistency check of an agro-climatic station network's air temperature).  
**Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**Run the 4.0 setting from the January 2028 configuration: it raises 18 drift alerts a year, within the 28 visits the field plan leaves for them.** At 3.5 the quality control would raise 33 a year: the record re-run with the 2028 network raises 23, and 30 drifts the record's own alerts repaired at kept stations never reached the 3.5 limit before their repair and would have kept growing until they did. Not 3.5 on the re-run alone, which counts those drifts only as far as the 3.0 alerts let them run.

## 2. Critical Components

1. The 2028 network is **131 stations**: the register's 148 less the **17** closing on 31 December 2027.
2. Re-run on the 2025 to 2027 record with that network and the limits set from the recorded statistic, the quality control raises **66, 23, 7 and 3** drift alerts a year at 3.0, 3.5, 4.0 and 4.5.
3. The sensor history holds **35** adjustments or replacements at drift-alert visits to kept stations; the re-run never reaches **10, 30, 33 and 34** of them before their repair at 3.0, 3.5, 4.0 and 4.5.
4. Each setting's drift alerts a year in 2028: **69, 33, 18 and 14** at 3.0, 3.5, 4.0 and 4.5; the most sensitive within the **28** visits is **4.0**.

## 3. Step-by-Step Solution

1. Took the 2028 network from registro_estaciones.xlsx (sheet Estaciones): the 148 stations less the 17 with a baja_prevista of 31/12/2027, 131 stations.
2. Re-ran QC-02 sections 4, 5 and 8 on the anomalies in control_calidad_2025-2027.parquet with the 131 kept stations as the network (the 3 nearest with an anomaly that day within 75 km, inverse-square weights, the 14-day mean where at least 10 residuals exist, so from 10 January 2025 as in the export, no alert within 14 days of the last), against each station's limit by section 6 (the setting times the standard deviation, n - 1, of its estadistico_14d over 2025 to 2027), counting the kept stations' alerts: 66, 23, 7 and 3 a year at 3.0, 3.5, 4.0 and 4.5.
3. Took the drifts the record's alerts cut short from the sheet Historial sensor T: every row with motivo Alerta de deriva (an adjustment or a replacement, as-found error recorded) at a kept station, 35, each answering the station's latest alert in the export on or before its day, within 10 days.
4. A drift goes on growing until a check sets it right (QC-02 section 9), so a drift the re-run's alerts at a setting never reached, from 14 days before the alert its visit answered to the adjustment, would have raised one alert at that setting later, each two months or more before its station's next spring round: 10, 30, 33 and 34 drifts at 3.0, 3.5, 4.0 and 4.5, added to the re-run's count and the three years divided by 3: 69, 33, 18 and 14 a year.
5. Chose the most sensitive setting within the 28 drift-alert visits in plan_campo_2028.pdf: 4.0.
6. Took the 2027 drift-alert visits from ordenes_trabajo_2025-2027.xlsx: on the old contractor's sheet every Alerta deriva order closed with a Visita, on that day; on the new contractor's sheet each station of a closed Corrective opened within 3 days of an alert there, on the first day from its opening to its visit_date with readings at the station in comprobaciones_patron_2025-2027.csv (under whatever order), leaving out a day with a reading outside the station's tmin to tmax in estaciones_diario_2025-2027.csv (a sensor read in a bath, not the check in place in the station's air that every visit includes, plan_campo_2028.pdf), and no visit where no such day exists. Days waited run from the alert's day in the quality-control export.
7. Took the 2027 breakdown visits at kept stations as the old contractor's Avería orders closed with a Visita and, by the same reading test, the stations of the new contractor's closed Correctives that answered no alert.
8. Run the 4.0 setting in 2028.

## 4. Deliverable Answers

### drift_alert_setting_2028.xlsx

1. Drift alerts a year in 2028, by setting:
   - 3.0: 69
   - 3.5: 33
   - 4.0: 18
   - 4.5: 14
2. The setting: 4.0, 18 drift alerts a year.
3. Drift-alert visits made in 2027 and the days their alerts waited for them in total, by district:
   - Cinco Villas: 3 visits, 9 days
   - Ribera Alta del Ebro: 6 visits, 25 days
   - Valdejalón: 7 visits, 26 days
   - Hoya de Huesca: 5 visits, 25 days
   - Monegros: 9 visits, 34 days
   - Somontano de Barbastro: 2 visits, 4 days
   - Cinca Medio: 3 visits, 8 days
   - Bajo Cinca: 5 visits, 16 days
4. Breakdown visits made in 2027 at the stations kept in 2028, by district:
   - Cinco Villas: 14
   - Ribera Alta del Ebro: 15
   - Valdejalón: 20
   - Hoya de Huesca: 14
   - Monegros: 23
   - Somontano de Barbastro: 12
   - Cinca Medio: 12
   - Bajo Cinca: 5

### alerts_by_setting_2028.png

5. Bar chart of each setting's drift alerts a year in 2028 against a line at the field plan's 28 visits, each bar split into the network re-run's alerts and the drifts the record's alerts cut short, the 4.0 bar marked as the setting.
