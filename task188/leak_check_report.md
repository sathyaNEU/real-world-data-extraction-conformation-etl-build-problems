# leak check, task188

**Verdict: REVIEW.** 12 files read, 11 golden figures and 9 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: likelihood, westbrook, infected, positive, protocol, minimum, decisive, prairie, riverside, county, species, caught, estimate, prompt, method, second, district, gravid, results, population, maximum, domain, surveillance, laboratory, report

## 2 author vocabulary (REVIEW 2)
- **REVIEW** `RCVCD_surveillance_and_control_protocol_2026.pdf`: \btraps?\b x21, a field term declared in metadata.json: ...rial application. 3 Adult mosquito sampling 3.1 CO2-baited light traps (CDC miniature light traps baited with 2 kg of dry ice, light off) st...
- **REVIEW** `field_database_data_dictionary.txt`: \btraps?\b x14, a field term declared in metadata.json: ...e ISO (YYYY-MM-DD); times are Central time. Table sites: one row per trap site site_id site ID (RC-nnn), assigned at the 15 June 202...

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `Ostby_Aviation_aerial_ULV_agreement_2026.pdf`: golden figure 2.3 appears: ...; a block is not split across nights or aircraft. 2.3 If the flight cannot be made on Thursday night...
- **REVIEW** `RCPHL_arbovirus_report_2026-W32_RCVCD.pdf`: golden figure 186 appears: ...Culex tarsalis 7 Undet. Negative RCPHL-26-5422 RC-186 08/11/2026 Culex pipiens 3 Undet. Negative RCPHL-...
- **REVIEW** `RCVCD_surveillance_and_control_protocol_2026.pdf`: golden figure 2.3 appears: ...heet Zone sections) and mapped in the zones file. 2.3 Each zone is one block for aerial application....

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `Ostby_Aviation_aerial_ULV_agreement_2026.pdf`: 3 of 25 stump-paragraph terms appear (county, district, maximum); read whether the document names the move
- **REVIEW** `RCPHL_arbovirus_report_2026-W32_RCVCD.pdf`: 8 of 25 stump-paragraph terms appear (positive, county, species, method, district, results); read whether the document names the move
- **REVIEW** `RCVCD_surveillance_and_control_protocol_2026.pdf`: 14 of 25 stump-paragraph terms appear (westbrook, positive, protocol, prairie, riverside, county); read whether the document names the move
- **REVIEW** `field_database_data_dictionary.txt`: 8 of 25 stump-paragraph terms appear (county, species, district, gravid, results, surveillance); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: 'All eight of our treatment zones returned West Nile-positive Culex pools in the week ending 15 August 2026; which one should get the single aerial adulticide application we can fly on Thursday 20 August, judged by the es'

## 6 ranking artifacts (REVIEW 5, INFO 1)
- **REVIEW** `RCVCD_site_register_2026.xlsx`: names 7 of 9 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `RCVCD_surveillance_and_control_protocol_2026.pdf`: names 8 of 9 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `RCVCD_zones_2026.geojson`: names 7 of 9 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `WNV_human_case_log_2026.xlsx`: names 8 of 9 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `rcvcd_surveillance_2024_2026.sqlite`: names 7 of 9 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `aerial_applications_2024_2026.csv`: names 6 of 9 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)
