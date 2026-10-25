# leak check, task485

**Verdict: REVIEW.** 16 files read, 48 golden figures and 13 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: census, register, animal, factor, inventory, housing, annual, national, movement, housed, western, animal-days, exports, nothing, designates, counts, holding, factors, november, architecture, family, regional, bovine, seasons, october

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `arp_designation_rules_2025.pdf`: candidate 'Ammonia Action Regions' sits beside decision vocabulary: ...agriculture towards the national ceiling for 2030. Each autumn the Minister designates as Ammonia Action Regions the regions whose ammonia from cattle manure is highest for their farmed land, and the me...
- **REVIEW** `epo_cattle_ammonia_factors_2025.pdf`: carries 21 of 29 distinctive words of the committed call: 'The Minister should designate Northern Vale, Eastern Vale, Southern Vale, Midland Basin, Inner Basin and Lower Basin as '

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `arp_designation_rules_2025.pdf`: 10 of 25 stump-paragraph terms appear (register, factor, housing, national, housed, designates); read whether the document names the move
- **REVIEW** `epo_cattle_ammonia_factors_2025.pdf`: 11 of 25 stump-paragraph terms appear (register, animal, factor, inventory, housing, national); read whether the document names the move
- **REVIEW** `nbr_export_notes.txt`: 9 of 25 stump-paragraph terms appear (census, register, animal, national, movement, exports); read whether the document names the move
- **REVIEW** `nso_june_livestock_census_2026_tables.pdf`: 8 of 25 stump-paragraph terms appear (census, register, national, western, counts, holding); read whether the document names the move

## 6 ranking artifacts (REVIEW 7)
- **REVIEW** `basin_agri_job_sheets_2026.xlsx`: names 3 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `creamery_milk_intake_by_region_2025.csv`: names 12 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `epo_cattle_ammonia_factors_2025.pdf`: names 12 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `moa_fertiliser_sales_by_region_2025-26.csv`: names 12 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `moa_livestock_housing_survey_2025.xlsx`: names 12 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `nbr_herd_register_2026-11.xlsx`: names 12 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `nso_june_livestock_census_2026_tables.pdf`: names 12 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Round 1 on zip 37f7e1986e84036128ca2496b64197b3, two isolated scored readers (sonnet, medium, fresh copies of the
prompt and target/ only).

- Question 1 (the decisive step announced): none from both. Nearest quoted: the rules' section 3 ("the ammonia from
  cattle manure arising in the region over the programme year") and the export notes' "the register holds an animal in
  its departure herd until this date".
- Question 2 (a ranking on the prompt's question): none from both; the factor note's Table 5 read as per-head factors,
  not a regional measure.
- Question 3 (a file existing only to help): the export notes as a field dictionary, the herd register's Regions sheet.
- Question 4 (an answer read as context): none; the 26 kilogram line read as the stated threshold.
- Question 5 (the literal sentence): the rules' sections 3 and 5 with the factor note's Table 3 caption; both executed
  them to the golden six.
- Question 6: reader A, an analytical choice (the year from the register's animal-days rather than the census day),
  largely procedure once the year and Table 3 are read literally; reader B, closer to rule application than to a hidden
  analytical choice, because the factor note's Tables 3 and 4 and the rules' sections 3 to 5 spell the method out.
- Question 7 (generated look): registration lags uniform on 1 to 27 days; exit dates past the extract date (to 23
  November 2026); other pigs a near-constant multiple of breeding sows; three tanker capacities in near-equal thirds.
- Part 3: every flagged line harmless on both reads.

Outcome: both readers landed the call (score_reader FAIL on both); ask A held at 0 of 24 on both. The architecture is
spent at stage 4; see the design note's architecture 2 record.
