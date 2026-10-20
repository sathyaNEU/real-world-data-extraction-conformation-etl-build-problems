## Tags

**Domain:** Physical & Environmental Sciences (sensor calibration and measurement: the converter efficiency of a network's chemiluminescence NOx analyzers, checked by gas-phase titration).  
**Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**Book 7 of the 16 station analyzers on the 17 to 21 January 2028 converter bench: BP01, BP02, BP03, BP04, BP05, BP08, BP13; the other 9 stay to their scheduled service.** A molybdenum converter is spent by the NO2 it reduces, and carried on its station's own load to the analyzer's 2028 service each of the seven converters is below 95 per cent by then. Not none on the latest titrations, every one at 95.2 per cent or more. Not BP08 alone on a curve against converter age, which brings every other converter to its service at about a year old and above 95 per cent.

## 2. Critical Components

1. No converter in service reads below 95 per cent at its latest titration; the lowest is BP01's at **95.2 per cent** on 11 October 2027.
2. The titrations separate on the NO2 the converter had reduced, not on its age: all **35** below 96.5 per cent came after more than **140 ppm-hours**, at 5 to 12 months, and every titration at 97.5 per cent or more came before 140.
3. BP08's converter, in since 13 October 2026, stays in to the analyzer's service on **15 February 2028**, its 2027 service put back.

## 3. Step-by-Step Solution

1. Put the 303 titrations on one scale: Tecnoaria's NO2 misurato over NO2 generato (titolazioni_Tecnoaria_2025-2026.xlsx) and Delta's rise in NOx less NO over the NO consumed (titolazioni_Delta_2026-2027.csv), the ratio UNI EN 14211 defines (AQBP-QA-07 section 3).
2. Summed each analyzer's hourly no2_ppb in archivio_analizzatori_NOx_2024-2027.csv, each hour once, from its converter change in registro_interventi_2024-2027.xlsx to each titration: the titrations below 96.5 per cent all lie past 140 ppm-hours.
3. Fitted one curve to every titration's efficiency against that NO2, linear to a knee and falling faster past it, and read each converter in service at its NO2 to 31 December 2027.
4. Carried each converter forward on its station's own NO2 from 1 January to its service in piano_manutenzione_2028.xlsx, the mean of the same days of 2025, 2026 and 2027: 7 station analyzers are below 95 per cent by their service (AQBP-QA-07 section 7).
5. Read no2_orari_validati_2027.csv, each row once, and took as valid the hours coded V or R, less every hour of which a Delta titration took more than 15 minutes (its ora_inizio and ora_fine, Italian civil time, put on the database's solar clock), so that the analyzer measured the station's air for under 45 minutes (AQBP-QA-07 section 5).
6. Gave BP07 the hours filed under MAG from 8 February to 1 March 2027, when the store spare stood in for its analyzer (the service log), and multiplied the six LGX-300 loggers' values between their installation and the visit that set them to 20 °C by 1.91 / 2.05 (their factory 0 °C setting).
7. Counted each station's valid hours, their mean NO2 and their 19th highest value (AQBP-QA-07 section 6).
8. Book the 7 analyzers on the bench; the other 9 stay to their scheduled service.

## 4. Deliverable Answers

### turno_banco_convertitori_2028.xlsx

1. Each station analyzer's verdict:
   - BP01, Gazzolo Po - via Emilia (NX4210-1187): book on the bench
   - BP02, Casalbuono - piazzale Stazione (NX4210-1203): book on the bench
   - BP03, Corte Mezzana - tangenziale (NX4210-1166): book on the bench
   - BP04, San Fermo - viale Rimembranze (NX4210-1219): book on the bench
   - BP05, Gazzolo Po - parco Ducale (NX4210-1174): book on the bench
   - BP06, Casalbuono - scuole Pascoli (NX4210-1191): stays
   - BP07, Ponte Ghiara - centro (CL62-0418): stays
   - BP08, Borgo Lanzone - giardini (CL62-0433): book on the bench
   - BP09, San Fermo - quartiere Lido (NX4210-1228): stays
   - BP10, Villa Saliceto (CL62-0402): stays
   - BP11, Motta Baluffa (CL62-0441): stays
   - BP12, Castelponzone (CL62-0427): stays
   - BP13, Zona industriale Ponte Ghiara (NX4210-1235): book on the bench
   - BP14, Polo chimico Casalbuono (CL62-0450): stays
   - BP15, Isola Pescaroli (CL62-0395): stays
   - BP16, Bosco Fontana Morta (CL62-0459): stays
2. The bench list: BP01, BP02, BP03, BP04, BP05, BP08, BP13, 7 analyzers.
3. Each station's 2027 NO2 record (valid hours; annual mean, µg/m³; 19th highest hourly value, µg/m³):
   - BP01: 8654 valid hours, mean 55.4 µg/m³, 19th highest 316 µg/m³
   - BP02: 8704 valid hours, mean 42.2 µg/m³, 19th highest 208 µg/m³
   - BP03: 8674 valid hours, mean 38.7 µg/m³, 19th highest 199 µg/m³
   - BP04: 8678 valid hours, mean 39.7 µg/m³, 19th highest 221 µg/m³
   - BP05: 8667 valid hours, mean 39.1 µg/m³, 19th highest 174 µg/m³
   - BP06: 8693 valid hours, mean 29.2 µg/m³, 19th highest 164 µg/m³
   - BP07: 8681 valid hours, mean 27.7 µg/m³, 19th highest 137 µg/m³
   - BP08: 8702 valid hours, mean 26.3 µg/m³, 19th highest 143 µg/m³
   - BP09: 8673 valid hours, mean 26.3 µg/m³, 19th highest 138 µg/m³
   - BP10: 8694 valid hours, mean 23.9 µg/m³, 19th highest 106 µg/m³
   - BP11: 8696 valid hours, mean 21.9 µg/m³, 19th highest 90 µg/m³
   - BP12: 8712 valid hours, mean 19.7 µg/m³, 19th highest 79 µg/m³
   - BP13: 8632 valid hours, mean 37.9 µg/m³, 19th highest 159 µg/m³
   - BP14: 8665 valid hours, mean 28.1 µg/m³, 19th highest 129 µg/m³
   - BP15: 8650 valid hours, mean 15.7 µg/m³, 19th highest 69 µg/m³
   - BP16: 8698 valid hours, mean 12.6 µg/m³, 19th highest 49 µg/m³

### rendimento_convertitori_2028.png

4. Each of the 16 converters' efficiency at its scheduled 2028 service against the 95 per cent line, with its efficiency at 31 December 2027, the 7 analyzers on the bench list marked.
