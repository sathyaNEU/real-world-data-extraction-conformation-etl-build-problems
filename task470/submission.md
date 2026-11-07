## Tags

**Domain:** Survey Research & Official Statistics (census, register and administrative data quality: a register-based dwelling statistic conformed from the cadastre, the meter data hub's metering points and hourly values, the population register and the land, business and shareholder registers).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Five of the ten municipalities qualify for the 2027 grant: Tverrvika (5802), Hesteby (5803), Solmoen (5805), Ørnevik (5807) and Fjordeid (5809).**
Their vacancy shares run from 5.4 to 8.2 per cent against the regulation's 5.0; the highest share below the line is Snøholt's 4.7 per cent. Not none, which a consumption floor anywhere from 1 to 10 kWh a day gives, because an empty dwelling in November is left heated and uses more electricity than many lived-in ones; and not all 10, which the population register's empty dwellings give, because the regulation counts who lived there, not who was registered.

## 2. Critical Components

1. Counted dwellings in the county: **8,020**; vacant in the fortnight: **396**.
2. A dwelling was lived in when, on at least one day, its morning or evening use rose above its own night-time use by more than **0.5 kWh** an hour; vacant when no day did.
3. Vacant dwellings still carrying a registered resident on 1 November: **118**; lived-in dwellings with nobody registered: **557**.

## 3. Step-by-Step Solution

1. Took the cadastre's units of type Bolig in use on or before 1 November 2026 (Section 3): 8,020 dwellings.
2. Joined each to its household metering points by bruksenhet_id, else by municipality and address for a single-unit house; Snøholt's points carry Fjordeid's old municipality number.
3. Put the hourly values on Norwegian time (UTC+1), kept the later delivery where an estimated day was replaced, and added a dwelling's two points where its meter changed.
4. For each day took the mean of 06 to 09 and of 16 to 22 against the mean of 01 to 05; a rise above 0.5 kWh on any day marks the dwelling as lived in (Section 4: nobody lived in it on any day).
5. Divided each municipality's vacant dwellings by its counted dwellings, rounded to one decimal, and designated those at 5.0 per cent or more (Section 6).
6. Rolled the population register of 5 January 2027 back to 1 November by undoing every later event, reading the November block renumberings as a change of unit number and the earlier events' old numbers as the renumbered flats; ages on 1 November.
7. Rolled the land register back to 1 November by tinglyst date and counted the dwellings held by the municipality, its KF or a company whose shares it holds all of with its own companies, titles without an organisation number in the municipality's own name included.

## 4. Deliverable Answers

### county_dwelling_occupancy_2026-11.xlsx

1. Counted dwellings listed: 8,020, of which vacant: 396; persons registered on 1 November 2026 across them: 13,599.
2. Vacant dwellings and vacancy share by municipality:
   - Brekkevoll (5801): 66 of 1,640 counted dwellings, 4.0 per cent
   - Tverrvika (5802): 38 of 520 counted dwellings, 7.3 per cent
   - Hesteby (5803): 63 of 980 counted dwellings, 6.4 per cent
   - Kvernhaug (5804): 33 of 860 counted dwellings, 3.8 per cent
   - Solmoen (5805): 28 of 430 counted dwellings, 6.5 per cent
   - Ravnsund (5806): 34 of 740 counted dwellings, 4.6 per cent
   - Ørnevik (5807): 31 of 380 counted dwellings, 8.2 per cent
   - Langgrav (5808): 36 of 1,120 counted dwellings, 3.2 per cent
   - Fjordeid (5809): 30 of 560 counted dwellings, 5.4 per cent
   - Snøholt (5810): 37 of 790 counted dwellings, 4.7 per cent

### vacancy_grant_certification_2027.docx

1. Qualifying municipalities: Tverrvika (7.3 per cent), Hesteby (6.4 per cent), Solmoen (6.5 per cent), Ørnevik (8.2 per cent) and Fjordeid (5.4 per cent).
2. Bar chart of the ten municipalities' vacancy shares against the 5.0 per cent threshold, the qualifying municipalities highlighted.
3. Persons registered in the counted dwellings on 1 November 2026, under 18, 18 to 66, 67 and over:
   - Brekkevoll (5801): 115, 1,748, 636
   - Tverrvika (5802): 86, 670, 227
   - Hesteby (5803): 106, 1,122, 425
   - Kvernhaug (5804): 80, 907, 281
   - Solmoen (5805): 72, 516, 215
   - Ravnsund (5806): 57, 875, 301
   - Ørnevik (5807): 86, 462, 189
   - Langgrav (5808): 141, 1,342, 503
   - Fjordeid (5809): 78, 716, 228
   - Snøholt (5810): 128, 936, 351
4. Counted dwellings held on the land register on 1 November 2026 by the municipality or a company it owns:
   - Brekkevoll (5801): 133
   - Tverrvika (5802): 17
   - Hesteby (5803): 149
   - Kvernhaug (5804): 80
   - Solmoen (5805): 27
   - Ravnsund (5806): 141
   - Ørnevik (5807): 23
   - Langgrav (5808): 136
   - Fjordeid (5809): 86
   - Snøholt (5810): 58
