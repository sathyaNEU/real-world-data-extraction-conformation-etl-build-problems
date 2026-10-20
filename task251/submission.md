## Tags

**Domain:** General Statistics & Data Science (missing data, censoring and measurement error: bedside glucose meters' systematic error against the laboratory, read from meter and laboratory pairings).  
**Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**Send 8 of the 52 meters to the 17 to 21 January 2028 recalibration: GX2-A564E (TI), GX2-J921X (MED), GX2-K532W (NIDO), GX2-P722J (DIAB), GX2-R842P (TIN), GX2-S959P (MEDV), GX2-W228Y (TIN), GX2-W234L (CHIR); the other 44 stay on their wards.** On the pairings the plan drew on the morning round since each meter's January 2027 calibration, each listed meter's systematic error lies beyond 5 per cent, from -8.2 to +11.0 per cent, and no other meter's is beyond 3.4 per cent. Not the list from every pairing since the calibration: it counts the confirmations of critical readings, drawn because the meter itself read under 50 or over 400 mg/dL, which carry that reading's own error, so on the nursery it drops GX2-K532W (+8.4 per cent on the scheduled pairings, +4.8 on all) and adds GX2-M707F (-1.6 against -5.8).

## 2. Critical Components

1. The pairings the plan drew, on the meter's planned day with the laboratory's draw between 6:00 and 7:30, after each meter's last calibration: **5,590 pairings**, 98 to 149 per meter.
2. The laboratory's values drawn before 13 September 2027 divided by **1.035**, the C600 against the C900.
3. The margin: the nearest listed meter, GX2-R842P, at **-7.4 per cent**; the nearest unlisted, GX2-J313P, at **+3.4 per cent**.

## 3. Step-by-Step Solution

1. Read the 13,938 pairings in GlyLink_abbinamenti_laboratorio_2026-2027.xlsx, each a meter result and the laboratory's result on the tube whose barcode the meter read (POCT-GLU-02 sections 5 and 6).
2. Kept the pairings the plan drew: the meter's days in piano_abbinamenti_glucometri_2026-2027.xlsx, a holiday moved to the next working day, with data_ora_prelievo between 6:00 and 7:30 (section 5); every other pairing is the confirmation of a reading under 50 or over 400 mg/dL (section 6), drawn because of the meter's own result, so it carries that result's error and does not measure the meter's bias.
3. Kept those after each meter's ultima_taratura in anagrafica_glucometri.xlsx with a numeric meter value, and divided the laboratory's values drawn before 13 September 2027 by 1.035 (nota_laboratorio_cambio_analizzatore_glicemia.pdf): 5,590 pairings.
4. Took each meter's systematic error as the mean of its meter over laboratory ratios less one, the factor section 7 defines: 8 meters lie beyond 5 per cent.
5. Read GlyLink_risultati_2026-2027.csv's patient results once per matricola and n_memoria, keeping the first reception (a docking the meter never saw acknowledged re-sends its results under new id_risultato), each at data_ora_test less one hour (the meters' clocks keep solar time all year: in summer the scheduled pairings show the meter an hour before the laboratory's draw).
6. Placed each result on the ward and hospital where its meter stood on the test's date (anagrafica_glucometri.xlsx, Storico ubicazioni; the export's presidio and reparto are the meter's current assignment), and dated it in Italian civil time.
7. For 2027, took per hospital and quarter the share of results whose data_ora_ricezione came more than 120 minutes after the test, and counted the results per ward (POCT-GLU-02 section 8).
8. Send the 8 meters to the January 2028 visit; the other 44 stay.

## 4. Deliverable Answers

### ritiro_glucometri_gennaio_2028.xlsx

1. The meters to recalibrate, 8 (matricola, ward, hospital, systematic error):
   - GX2-A564E, TI, Presidio di Castelmarne: -8.2 per cent
   - GX2-J921X, MED, Presidio di Castelmarne: -7.9 per cent
   - GX2-K532W, NIDO, Presidio di Castelmarne: +8.4 per cent
   - GX2-P722J, DIAB, Presidio di Castelmarne: +8.4 per cent
   - GX2-R842P, TIN, Presidio di Castelmarne: -7.4 per cent
   - GX2-S959P, MEDV, Presidio di Valdarena: +8.3 per cent
   - GX2-W228Y, TIN, Presidio di Castelmarne: -8.2 per cent
   - GX2-W234L, CHIR, Presidio di Castelmarne: +11.0 per cent
2. Share of 2027 patient results that reached the clinical record more than two hours after the test:
   - Presidio di Castelmarne: first quarter 27.3 per cent, second 27.7 per cent, third 27.9 per cent, fourth 27.3 per cent
   - Presidio di Rivobello: first quarter 39.7 per cent, second 43.3 per cent, third 42.7 per cent, fourth 44.0 per cent
   - Presidio di Valdarena: first quarter 66.3 per cent, second 66.8 per cent, third 68.3 per cent, fourth 65.1 per cent
3. Patient tests performed in 2027, by ward:
   - TIN: 10,146
   - NIDO: 5,930
   - TI: 10,952
   - DIAB: 5,839
   - PS: 6,712
   - MED: 9,896
   - CHIR: 6,704
   - PED: 3,115
   - OST: 2,046
   - MEDR: 8,015
   - PSR: 2,417
   - MEDV: 7,322
   - LUN: 2,957

### errore_sistematico_glucometri_2027.png

4. Each of the 52 meters' systematic error on the scheduled pairings since its last calibration, by hospital and ward, against the band from -5 to +5 per cent, the 8 listed meters marked and labelled.
