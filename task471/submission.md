## Tags

**Domain:** Survey Research & Official Statistics (census, register and administrative data quality: the population register's over-count of residents who left the country unreported, measured by the Register Coverage Audit 2026 and applied to each municipality's register count within the characteristics that carry it, the length of the current stay since the latest settlement from abroad and an earlier departure, both rebuilt from the register's event history).  
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Nine of the 24 municipalities in play qualify for the 2027 small-municipality supplement: Aldewolde, Borgermeer, Bremvoort, Dornhaghe, Eekhorst, Haverstede, Hilderloo, Koudenbeek and Zandloo.**
Each has an adjusted resident population on 1 January 2026 below 5,000: its register count less the registered persons the audit estimates were not living there, taken within the length of each person's current stay since the latest settlement from abroad and whether the person had left the country before it. Hilderloo is the qualifying municipality nearest the line and Dalmeer the nearest left out. Not the eight municipalities the register's own fields give (country of birth by years at the current address), which add Molenrade and Nijdorp and drop Eekhorst, Haverstede and Koudenbeek, because a move within the country resets the address date while only the event history shows who has come and gone before; not the six the current stay alone gives, which drops Eekhorst, Haverstede and Koudenbeek.

## 2. Critical Components

1. Sampled persons the audit found not living in their registered municipality on 1 January 2026 (final results 20, 30 and 40): **206 of 12,000** (1.72 per cent).
2. Not living there, by migration career: never settled from abroad **26 of 9,181** (0.28 per cent); settled from abroad with no earlier departure **139 of 2,598** (5.4 per cent); settled from abroad after an earlier departure **41 of 221** (18.6 per cent).
3. Registered persons settled from abroad who had left the country before: Eekhorst **729 of 1,840**; Haverstede **666 of 1,808**; Koudenbeek **678 of 1,755**; against Molenrade **62 of 1,825**; Nijdorp **49 of 1,813**; Hilderloo **53 of 1,930**.
4. Registered persons in the first to fourth year of their current stay: Hilderloo **1,503**, against Molenrade **94** and Nijdorp **86**.

## 3. Step-by-Step Solution

1. Read population_register_extract_20260101.txt (its trailer's 126,655 persons in the 24 municipalities in play, Ravenmeer one municipality under Article 14(4)) and population_register_events_extract.csv, dropped each annulled event with its ANN, and gave each person the completed years from the latest IMM to 1 January 2026 and whether an EMI came before that IMM.
2. Took each audited person's last record in register_coverage_audit_2026_visits.csv as the final result (91 is no contact; 50 counts as living there) and built the same two features from register_coverage_audit_2026_histories.csv: 206 of 12,000 not living there.
3. Measured the audit's share not living there within cells of the current stay (never settled from abroad, under 1, 1 to 4, 5 to 9, 10 or more years) by whether the person had left the country before; within those cells country of birth, nationality, years at the address, age and sex add nothing.
4. Gave each registered person the share of their cell, summed by municipality, took the sum from the register count, rounded to the whole person and compared with 5,000 (Article 14(1) to (3)): nine qualify.
5. Departures abroad: deregistration_messages_2025.csv's EMI messages the hub accepted (hub_acknowledgements_2025.csv), with a 2025 departure date and sent in 2025 in the country's time (the night batch logged at 23:00 UTC or later on 31 December left on 1 January 2026), each person who left twice counted twice, less the departures the register annulled as entered in error (an EMI with an ANN in the person's history).
6. Deaths: the OVL messages the hub accepted with a 2025 date of death and sent in 2025 in the country's time, less the deaths the register annulled and the former residents whose registration had ended before they died (non_resident_records_extract.csv, DEPARTURE_DATE before the date of death).
7. Wrote adjusted_population_supplement_2027.csv in the layout of the ministry's delivery specification and the chart of the adjusted resident populations against the 5,000 line.

## 4. Deliverable Answers

### adjusted_population_supplement_2027.csv

1. Whether each municipality qualifies, its departures abroad in 2025 and its deaths in 2025:
   - Aldewolde (GM0402): qualifies, 79 departures abroad, 55 deaths
   - Borgermeer (GM0417): qualifies, 58 departures abroad, 61 deaths
   - Bremvoort (GM0426): qualifies, 68 departures abroad, 32 deaths
   - Dalmeer (GM0438): does not qualify, 58 departures abroad, 50 deaths
   - Dornhaghe (GM0451): qualifies, 74 departures abroad, 53 deaths
   - Eekhorst (GM0465): qualifies, 291 departures abroad, 36 deaths
   - Haverstede (GM0473): qualifies, 304 departures abroad, 35 deaths
   - Heukelveen (GM0488): does not qualify, 49 departures abroad, 51 deaths
   - Hilderloo (GM0496): qualifies, 336 departures abroad, 32 deaths
   - Koudenbeek (GM0509): qualifies, 292 departures abroad, 36 deaths
   - Lemdorp (GM0514): does not qualify, 65 departures abroad, 43 deaths
   - Linterdam (GM0527): does not qualify, 75 departures abroad, 57 deaths
   - Molenrade (GM0533): does not qualify, 57 departures abroad, 49 deaths
   - Nijdorp (GM0546): does not qualify, 46 departures abroad, 49 deaths
   - Oosterzand (GM0552): does not qualify, 82 departures abroad, 57 deaths
   - Reitsloo (GM0568): does not qualify, 75 departures abroad, 51 deaths
   - Sloterwaard (GM0571): does not qualify, 72 departures abroad, 56 deaths
   - Steenwoude (GM0584): does not qualify, 66 departures abroad, 52 deaths
   - Tienhaven (GM0599): does not qualify, 57 departures abroad, 57 deaths
   - Uffeldijk (GM0603): does not qualify, 80 departures abroad, 56 deaths
   - Velderkamp (GM0615): does not qualify, 78 departures abroad, 51 deaths
   - Westerwierde (GM0628): does not qualify, 60 departures abroad, 64 deaths
   - Zandloo (GM0636): qualifies, 54 departures abroad, 56 deaths
   - Ravenmeer (GM1987): does not qualify, 69 departures abroad, 57 deaths

### adjusted_population_supplement_2027.png

1. Bar chart of the 24 municipalities' adjusted resident populations against the 5,000 line, the nine under it highlighted: Aldewolde, Borgermeer, Bremvoort, Dornhaghe, Eekhorst, Haverstede, Hilderloo, Koudenbeek and Zandloo.
