# leak check, task459

**Verdict: REVIEW.** 12 files read, 49 golden figures and 12 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: output, records, commitment, contract, hourly, decisive, operating, generator, inventory, generation, district, outage, method, average, asserted, sentence, tamarack, landing, rejected, annual, firing, default, objective, selection, nothing

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `rfo2026_evaluation_data_dictionary.txt`: \bdesign note\b|\bgenerator\b x2: ...or_offered_plants.xlsx Form EIA-860, 2025 final release, Schedule 3 generator data (operable units) for the offered plants' EIA plant codes, ever...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `calder_pud_rp7_resource_procurement_procedure.pdf`: 7 of 25 stump-paragraph terms appear (records, commitment, contract, hourly, generation, district); read whether the document names the move
- **REVIEW** `rfo2026_baseload_request_for_offers.pdf`: 9 of 25 stump-paragraph terms appear (output, records, commitment, contract, hourly, generation); read whether the document names the move
- **REVIEW** `rfo2026_evaluation_data_dictionary.txt`: 11 of 25 stump-paragraph terms appear (records, contract, hourly, operating, generator, generation); read whether the document names the move

## 6 ranking artifacts (REVIEW 5, INFO 4)
- **REVIEW** `eia860_2025_generator_offered_plants.xlsx`: names 9 of 12 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `eia923_2024-2025_generation_and_fuel_offered_plants.xlsx`: names 9 of 12 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `rfo2026_offer_gads_events_2025.csv`: names 9 of 12 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `rfo2026_offer_meter_data_2024-2025.csv`: names 9 of 12 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `rfo2026_offers_received.xlsx`: names 10 of 12 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `camd_hourly_emissions_offered_units_2024-2025.csv`: names 9 of 12 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `camd_monitoring_plans_offered_units.csv`: names 9 of 12 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `epa_eia_crosswalk_2025.csv`: names 9 of 12 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `rfo2026_offer_planned_outages_2027.csv`: names 9 of 12 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `rfo2026_offer_planned_outages_2027.csv`: 26 ISO dates after 2026-11-06, e.g. 2027-04-08, 2027-04-11, 2027-04-15, 2027-04-18, 2027-04-20
- **REVIEW** `rfo2026_offers_received.xlsx`: 20 ISO dates after 2026-11-06, e.g. 2027-01-01, 2036-12-31

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)
