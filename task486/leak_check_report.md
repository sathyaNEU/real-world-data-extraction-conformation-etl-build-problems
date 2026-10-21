# leak check, task486

**Verdict: REVIEW.** 21 files read, 24 golden figures and 13 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: release, groups, blocks, housing, population, published, census-day, silent, formally, private, twelve, allocation, nothing, decisive, points, non-negative, consistent, inside, nested, conformed, dataset, wickmoor, fallowmere, boundaries, policy

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `kaaa_provider_allocation_policy_2023.docx`: carries 18 of 20 distinctive words of the committed call: "On census day 2020 Kelvane County's provider areas held, aged 60 and over and aged 75 and over: Wickmoor City 15,580 and"

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `dhc2020_notes_for_local_users.pdf`: 7 of 25 stump-paragraph terms appear (release, groups, blocks, housing, population, published); read whether the document names the move
- **REVIEW** `fy2027_area_plan_update_instructions.pdf`: 4 of 25 stump-paragraph terms appear (release, housing, population, allocation); read whether the document names the move
- **REVIEW** `kaaa_provider_allocation_policy_2023.docx`: 5 of 25 stump-paragraph terms appear (allocation, wickmoor, fallowmere, boundaries, policy); read whether the document names the move

## 6 ranking artifacts (REVIEW 1, INFO 2)
- **REVIEW** `provider_area_blocks.csv`: names 6 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `kaaa_provider_allocation_policy_2023.docx`: names 3 of 13 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `kaaa_provider_directory.xlsx`: names 12 of 13 answer-set candidates; confirm it does not rank them on the decision question

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

Two isolated readers (general-purpose, medium), each on a fresh unzip of target.zip (sha256 915a6b4afe4113ee) with prompt.txt only, scored with score_reader.py before their verdicts were read.

- Reader 1: call 0 of 12 (the block sum, North Kelvane 850 aged 60 and over); ask figures 12 of 12 (exit 1). Question 1: no sentence told it how to get the figures right. Question 6: "following the stated procedure and reading fields correctly ... I found no analytical choice that a careful reader could get wrong."
- Reader 2: call 0 of 12 (the block sum); ask figures 12 of 12 (exit 1). Question 1: none. Question 6: "reading definitions and applying stated rules ... I did not find an analytical choice for the census counts beyond summing blocks."
- Ask devices: both readers capped each client's hot meals at the roster's meals_per_day (the re-sent rows collapsed, the second meals kept) and joined the death match through the registry's links; both devices sat on the careful path.
- Verdict on the REVIEW lines: the policy's word overlap with the call, the notes' and instructions' design vocabulary and the assignment's area names beside block codes were read by neither reader as the answer or the method; harmless.
