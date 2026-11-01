## Tags

**Domain:** Pharmacology, Pharmacoepidemiology & Safety (medication adherence and persistence).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Yes: 6 general practices join the 2027 statin follow-up programme: Lægehuset Østergade (041219) 48%, Klinikken Bredgade (041236) 53%, Lægerne Skovvej (041248) 48%, Lægeklinikken Kirkebakken (041275) 48%, Lægerne Møllevej (041307) 54%, Lægerne Stationsvej (041322) 53%.**
Each kept fewer than 60 per cent of its new statin users of the second half of 2025 persistent for twelve months, with each patient's tablets timed at the daily dose their own refills show; every other practice is at 65 per cent or more.

## 2. Critical Components

1. Twelve-month persistence of the new statin users of 1 July to 31 December 2025 by practice (per cent, persistent of new users): 041207 68 (70 of 103); 041219 48 (40 of 84); 041224 66 (37 of 56); 041236 53 (30 of 57); 041248 48 (51 of 107); 041251 73 (75 of 103); 041263 67 (69 of 103); 041275 48 (55 of 115); 041282 76 (61 of 80); 041294 68 (65 of 96); 041307 54 (45 of 83); 041319 71 (59 of 83); 041322 53 (62 of 117); 041334 75 (65 of 87); 041346 71 (72 of 101); 041358 65 (72 of 110).
2. Joining (under 60): 041219, 041236, 041248, 041275, 041307, 041322; nearest to the line from above: 041358 at 65.

## 3. Step-by-Step Solution

1. Read statin_dispensings_202401_202612.csv (dates day-month-year to June 2024, ISO after), joined each product number to statin_products.csv for ATC code, strength and pack size, and took tablets as packs times pack size.
2. Took as new users the pseudonyms whose first dispensing from 1 July to 31 December 2025 had no statin dispensing in the 365 days before, at the practice (practice_register_2026.xlsx) that prescribed that first dispensing: 1,485 patients.
3. Estimated each new user's daily dose from their own dispensings as the tablets dispensed before the last dispensing over the days from the first to the last (median refill rate, last three refills and the first year only give the same status for every patient); a patient with one dispensing runs out within the year at any dose.
4. Laid each dispensing's tablets end to end at that dose from the first dispensing, tablets in hand used first, and called a patient persistent when no run of more than 30 days without tablets fell in the 365 days; took each practice's share and set it against 60 per cent (statin_followup_programme_2027.pdf 2.1, 3.1, 3.2).
5. For the pilot, recovered each pharmacy's rate from pilot_statements_2026.pdf as each statement's amount over the conversations of its quarter in pilot_conversations_2026.xlsx not cancelled by the quarter's last day (one rate across the four quarters), and multiplied it by the conversations held in 2026 and never cancelled (pharmacy_pilot_agreement_2026.pdf 2.1).
6. For continuing users, joined the two pseudonyms of each person whose personal number was replaced in 2026 (same birth date and sex, the first pseudonym's dispensings ending before the second's begin, on the same product line and practice), kept persons with a dispensing in each quarter of 2026 and counted them at the practice of their last 2026 dispensing (programme 3.3).

## 4. Deliverable Answers

### statinprogram_2027.xlsx

1. Joins the programme in 2027: 041219 Lægehuset Østergade, 041236 Klinikken Bredgade, 041248 Lægerne Skovvej, 041275 Lægeklinikken Kirkebakken, 041307 Lægerne Møllevej, 041322 Lægerne Stationsvej.
2. Twelve-month persistence by practice (per cent):
   - 041207 Lægerne Torvegade: 68
   - 041219 Lægehuset Østergade: 48
   - 041224 Lægerne ved Åen: 66
   - 041236 Klinikken Bredgade: 53
   - 041248 Lægerne Skovvej: 48
   - 041251 Lægehuset Hornslev: 73
   - 041263 Lægerne i Vejlby: 67
   - 041275 Lægeklinikken Kirkebakken: 48
   - 041282 Lægerne Havnegade: 76
   - 041294 Lægehuset Rødby Strand: 68
   - 041307 Lægerne Møllevej: 54
   - 041319 Lægeklinikken Ellerup: 71
   - 041322 Lægerne Stationsvej: 53
   - 041334 Lægehuset Tvede: 75
   - 041346 Lægerne Søndergade: 71
   - 041358 Klinikken Vestervang: 65
3. What each pilot pharmacy is entitled to for 2026 (DKK):
   - A102 Lindholt Apotek: 63,474
   - A107 Lindholt Torve Apotek: 43,708
   - A114 Hornslev Apotek: 41,174
   - A121 Vejlby Apotek: 26,928
   - A126 Rødby Strand Apotek: 29,133
   - A133 Ellerup Apotek: 36,408
   - A139 Tvede Apotek: 28,152
   - A145 Søndergade Apotek: 49,590
4. Continuing statin users of 2026 by practice (persons):
   - 041207 Lægerne Torvegade: 135
   - 041219 Lægehuset Østergade: 129
   - 041224 Lægerne ved Åen: 67
   - 041236 Klinikken Bredgade: 121
   - 041248 Lægerne Skovvej: 152
   - 041251 Lægehuset Hornslev: 119
   - 041263 Lægerne i Vejlby: 127
   - 041275 Lægeklinikken Kirkebakken: 249
   - 041282 Lægerne Havnegade: 79
   - 041294 Lægehuset Rødby Strand: 121
   - 041307 Lægerne Møllevej: 215
   - 041319 Lægeklinikken Ellerup: 110
   - 041322 Lægerne Stationsvej: 151
   - 041334 Lægehuset Tvede: 84
   - 041346 Lægerne Søndergade: 176
   - 041358 Klinikken Vestervang: 116

### statinprogram_2027.pdf

1. One-page note to the practice planning committee recommending the 6 practices, with a bar chart of each practice's persistence against the 60 per cent line.
