## Tags

**Domain:** Survey Research & Official Statistics (official time-series production: a monthly accommodation series benchmarked to quarterly administrative totals).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**3 member comuni qualify for the 2027 peak-month services co-financing: Sant'Elvira a Mare (61.3 guest nights per resident in August 2026), Capo Ferrino (36.9 guest nights per resident in August 2026), Marina di Cervessa (31.4 guest nights per resident in August 2026).**
Marina di Cervessa is the comune closest to the line, 31.4 nights per resident against 30; every other member comune is below 30.

## 2. Critical Components

1. August 2026 guest nights and nights per resident by member comune: Sant'Elvira a Mare 210,800 and 61.3; Capo Ferrino 84,000 and 36.9; Marina di Cervessa 228,600 and 31.4; Acquanera Marina 124,900 and 28.0; Calarossa 82,700 and 27.6; Lido di Arzena 186,300 and 26.3; Alvea Salvina 152,900 and 24.6; Montelusa 43,900 and 19.8; Roccaferrata 18,800 and 13.4; Borgo Sant'Elmo 38,100 and 12.3; Serra d'Ulmo 8,600 and 9.5; Poggio Ventoso 11,000 and 8.8; Pievefosca 6,900 and 4.1; Porto Levarna 83,900 and 3.5; Fontecupa 5,800 and 2.3; San Gaudenzio 6,000 and 1.8; Castelpieno 6,600 and 1.2; Collebruno 6,400 and 0.9.
2. Qualifying (30 or more): Sant'Elvira a Mare, Capo Ferrino, Marina di Cervessa; closest to the line: Marina di Cervessa at 31.4.
3. Each comune's August 2026 nights are its July to September 2026 declared nights (latest filing for each category) less its reported July and September returns, which are complete; the comuni without the tourist tax (Collebruno, San Gaudenzio, Fontecupa) take their August returns as filed, all of which were filed.

## 3. Step-by-Step Solution

1. Read mov_clienti_strutture_LV12_2025-07_2026-09_estr20261117.csv, kept for each establishment and month the rows of its latest submission (PROGR_INVIO), and summed PRESENZE over residence groups.
2. Matched July to September 2026 returns (CIN codes) to registro_strutture_ricettive_LV12_20261116.xlsx; every establishment on the register filed July and September, and some open in August filed no August return.
3. Read the quarterly tourist-tax declarations from the five tax-office files (the concessionaire's workbook, Porto Levarna's and Sant'Elvira a Mare's csv files, the hill comuni's shared file and Lido di Arzena's pdf), keeping for each comune, quarter and category the filing received last, and took total nights (liable and exempt), as the union's regulation (art. 3) counts every night.
4. Where every establishment of a comune filed every month, its survey quarter equals its declared quarter; set each comune's August 2026 nights to its declared July to September 2026 nights less its reported July and September nights.
5. Divided by residents at 1 January 2026 (popolazione_residente_1gennaio_2025_2026_LV12.csv, with Alvea Salvina as one comune) and compared with 30 (regulation art. 2).
6. January to April 2026: summed the latest returns of every establishment by the comune code in its CIR (the first three digits after 112), mapping 006 and 007 to Alvea Salvina (variazioni_amministrative_2026_estratto.txt), so the establishments that closed before the May code change, absent from the register, still count.
7. October 2025 occupancy: October nights over bed-places available on the days each register establishment was open, with the bed-places in force in October (VARIAZIONI), no days for the suspended establishments and the opening period's closing day.
8. 2025 tourist tax: each comune's liable nights per quarter and category from the last filing, times the rate in force that quarter (aliquote_imposta_soggiorno_comuni_LV12.csv), Torre Alvea and Salvina Marina included.

## 4. Deliverable Answers

### august_2026_guest_nights.xlsx

1. August 2026 by member comune (guest nights; nights per resident; qualifies):
   - Sant'Elvira a Mare: 210,800; 61.3; yes
   - Capo Ferrino: 84,000; 36.9; yes
   - Marina di Cervessa: 228,600; 31.4; yes
   - Acquanera Marina: 124,900; 28.0; no
   - Calarossa: 82,700; 27.6; no
   - Lido di Arzena: 186,300; 26.3; no
   - Alvea Salvina: 152,900; 24.6; no
   - Montelusa: 43,900; 19.8; no
   - Roccaferrata: 18,800; 13.4; no
   - Borgo Sant'Elmo: 38,100; 12.3; no
   - Serra d'Ulmo: 8,600; 9.5; no
   - Poggio Ventoso: 11,000; 8.8; no
   - Pievefosca: 6,900; 4.1; no
   - Porto Levarna: 83,900; 3.5; no
   - Fontecupa: 5,800; 2.3; no
   - San Gaudenzio: 6,000; 1.8; no
   - Castelpieno: 6,600; 1.2; no
   - Collebruno: 6,400; 0.9; no
2. Qualifying comuni: Sant'Elvira a Mare, Capo Ferrino, Marina di Cervessa.
3. Closest to the line: Marina di Cervessa, 31.4 nights per resident.
4. Guest nights for January to April 2026 by member comune:
   - Porto Levarna: 197,400
   - Marina di Cervessa: 81,800
   - Sant'Elvira a Mare: 69,700
   - Capo Ferrino: 31,200
   - Lido di Arzena: 64,000
   - Calarossa: 32,400
   - Acquanera Marina: 42,100
   - Borgo Sant'Elmo: 34,200
   - Roccaferrata: 13,100
   - Montelusa: 35,500
   - Castelpieno: 9,400
   - Serra d'Ulmo: 9,800
   - Poggio Ventoso: 13,200
   - Collebruno: 9,300
   - San Gaudenzio: 8,700
   - Pievefosca: 10,100
   - Fontecupa: 8,100
   - Alvea Salvina: 59,400
5. Net bed-place occupancy in October 2025 by type of establishment (per cent):
   - ALBERGO: 29.9
   - CAMPEGGIO: 24.2
   - CASA VACANZE: 26.2
   - BED AND BREAKFAST: 28.2
   - AGRITURISMO: 27.7
   - AFFITTACAMERE: 28.5
6. Tourist tax due to the member comuni in 2025 (EUR):
   - Q1: 468,700
   - Q2: 2,452,800
   - Q3: 3,861,200
   - Q4: 854,100

### peak_cofinancing_2027_note.pdf

1. Decision: Sant'Elvira a Mare, Capo Ferrino, Marina di Cervessa qualify; Marina di Cervessa is closest to the line at 31.4.
2. Chart: horizontal bars of August 2026 guest nights per resident for every member comune, the qualifying comuni highlighted, a dashed line at 30, each bar labelled with its value.
