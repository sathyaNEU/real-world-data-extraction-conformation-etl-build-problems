## Tags

**Domain:** Urban & Regional Science (municipal service demand and resource allocation).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Calderwick Police should give the Tanner Street custody hub a planning figure of 4,000 detentions for 2027-28.**
The hub will book the six wards' arrests by the force's own officers, 3,754 by the custody demand model, and the arrests British Transport Police officers make at Calderwick and Kingsway stations, 281, which BTP books into the suite serving the ward: 4,035.9 before rounding. Not 3,750, the model run on the force's arrest records alone, which hold none of BTP's arrests.

## 2. Critical Components

1. The six wards' 2027-28 arrests by Calderwick Police officers, by the custody demand model, are **3,754**.
2. British Transport Police recorded **1,702** crimes in the six wards in 2025-26, all at Calderwick station (1,600) and Kingsway station (102).
3. BTP's arrests at the two stations, those crimes at the force's own 2025-26 arrests per recorded crime of each type with its warrant share, are **281** a year.

## 3. Step-by-Step Solution

1. Took the six wards that move to Tanner Street from custody_suite_allocation_2027.xlsx and counted their arrests in calderwick_police_arrests_2021-04_2026-09.csv by financial year of the UK date of arrest: 3,732 in 2025-26.
2. Carried each ward's 2025-26 arrests two years at its capped three-year change and summed the six wards, per the method in custody_demand_model_v2.pdf: 3,754.
3. Read note 2 of the allocation's Notes sheet (a detainee goes to the suite serving the ward of arrest, whichever force or agency arrests them) and took British Transport Police's rows in police_uk_street_crime_2025-26.csv whose LSOA lies in the six wards by lsoa21_to_ward_lookup.csv: 1,702 crimes.
4. Multiplied BTP's crimes of each type by the force's 2025-26 arrests in that offence group over its own street-level crimes of that type, and added the force's warrant, recall or breach share (5.3 per cent): 281; with the model's 3,754 the hub's 2027-28 detentions are 4,035.9.
5. For the remand holds, matched each file in cju_remand_files_2025-03_2026-04.csv to the remanded arrest charged at its suite at its charge time (the linked arrest, or the later arrest when the linked one is the case's earlier release), added the remanded arrests with no file arrested in the same minute, ward and offence group, each on its own charge and booking times and the file's handover, and kept the defendants charged in 2025-26 (UK times converted to UTC): 1,206 defendants.
6. For the assessments, counted the initial health assessment lines in custody_healthcare_contacts_2025-26.csv, joining a line that starts at 07:00 or 19:00 on the end of the episode's previous assessment, and placed a closed suite's team's lines at the suite its wards were booked into while the arrest records show no booking at the closed suite, from the last booking before the gap to the first after it (Eastmoor at Northgate, 14 August to 2 September 2025; Wendle Cross at Southfields, 3 November 2025 to 30 January 2026).
7. Planning figure for 2027-28: 4,000 detentions.

## 4. Deliverable Answers

### tanner_street_planning_figure_2027-28.xlsx

1. Planning figure for 2027-28: 4,000 detentions (4,035.9 unrounded).
2. Built from: 3,754 arrests by Calderwick Police officers in the six wards (custody demand model) and 281 arrests by British Transport Police officers at Calderwick and Kingsway stations (from 1,702 recorded crimes).
3. Remand holds, defendants charged in 2025-26 and kept in custody for court, cell hours from charge to handover and holds over 24 hours from booking in:
   - Northgate: 4,487 cell hours, 183 held more than 24 hours
   - Eastmoor: 2,811 cell hours, 109 held more than 24 hours
   - Southfields: 7,767 cell hours, 296 held more than 24 hours
   - Wendle Cross: 5,595 cell hours, 240 held more than 24 hours
4. Initial health assessments in 2025-26, begun from 07:00 to 19:00 and begun at night:
   - Northgate: 1,178 by day, 1,470 at night
   - Eastmoor: 526 by day, 670 at night
   - Southfields: 1,571 by day, 2,078 at night
   - Wendle Cross: 1,115 by day, 1,515 at night

### hub_planning_note.docx

1. The note gives the planning figure of 4,000 detentions and its two parts, 3,754 and 281.
2. Bar chart of the six wards' arrests from the force's records for each financial year from 2021-22 to 2025-26 (3,472, 3,734, 3,615, 3,680, 3,732), beside a 2027-28 bar of 4,000 stacked as the model's 3,754 and BTP's 281.
