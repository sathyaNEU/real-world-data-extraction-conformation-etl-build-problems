# leak check, task233

**Verdict: REVIEW.** 15 files read, 40 golden figures and 12 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: follow-up, allocation, points, departure, district, nonrespondent, nonrespondents, pooled, survey, allocations, golden, statistics, carried, default, method, decisive, followed-up, nonresponse, sentence, asserted, missing-data-censoring-measurement-error, respondents, outcomes, rejects, ratios

## 3 answer figures in the pack (REVIEW 4)
- **REVIEW** `QS-4_quality_flags_standard.pdf`: golden figure 3.0 appears: ...t Standard published without comment 1.0 to under 3.0 points Caution published with the caution note 3....
- **REVIEW** `nonresponse_followup_2025_report.pdf`: candidate 'Upper Valley' sits beside decision vocabulary: ...The follow-up ran in five districts chosen across the island's range of area deprivation: Upper Valley, Northern Plains, Riverside, City East and Mill Towns. On 31 October 2025 the field team...
- **REVIEW** `nonresponse_followup_2025_report.pdf`: candidate 'Mill Towns' sits beside decision vocabulary: ...land's range of area deprivation: Upper Valley, Northern Plains, Riverside, City East and Mill Towns. On 31 October 2025 the field team drew a simple random sample of 88 in every 100 of the...
- **REVIEW** `nonresponse_followup_2025_report.pdf`: candidate 'City East' sits beside decision vocabulary: ...across the island's range of area deprivation: Upper Valley, Northern Plains, Riverside, City East and Mill Towns. On 31 October 2025 the field team drew a simple random sample of 88 in ev...

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `DATA_DICTIONARY.md`: 9 of 25 stump-paragraph terms appear (follow-up, allocation, points, district, nonrespondent, nonrespondents); read whether the document names the move
- **REVIEW** `QS-4_quality_flags_standard.pdf`: 15 of 25 stump-paragraph terms appear (follow-up, allocation, points, departure, district, nonrespondent); read whether the document names the move
- **REVIEW** `README.md`: 9 of 25 stump-paragraph terms appear (follow-up, allocation, points, district, survey, allocations); read whether the document names the move
- **REVIEW** `leaver_destinations_methodology_2026.pdf`: 12 of 25 stump-paragraph terms appear (follow-up, allocation, points, district, nonrespondent, nonrespondents); read whether the document names the move
- **REVIEW** `nonresponse_followup_2025_report.pdf`: 5 of 25 stump-paragraph terms appear (follow-up, district, survey, nonresponse, outcomes); read whether the document names the move

## 6 ranking artifacts (REVIEW 1, INFO 2)
- **REVIEW** `destinations_release_2025_tables.xlsx`: names 11 of 12 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `nonresponse_followup_2025_report.pdf`: names 4 of 12 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `school_register.xlsx`: names 11 of 12 answer-set candidates; confirm it does not rank them on the decision question

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

Architecture 2 (after the furniture redraw), two reads on fresh copies of `prompt.txt` and `target/` (isolated
reader, medium effort), 2026-10-16.

**Read 1.**
1. Decisive step: none. The closest sentences are QS-4 s.3 (the headline rate recomputed with each nonrespondent's
   allocation moved as the most recent follow-up found) and s.6 (the departure measured on resolved cases still
   nonrespondents in the final file, each counted once); neither says how a departure found in five of twelve
   districts is carried to the others.
2. Ranks or scores the candidates: none (the 2025 release tables hold 2025 rates on the 2025 map, no flags).
3. Exists only to help the analyst: the data dictionary and the readme (the pack's registers).
4. Reads as the answer: none; no flag, shift or 2026 headline figure appears anywhere.
5. Filed sentence fixing the main figure: QS-4 s.2's headline rate, whose literal result is the golden's definition.
   Open items named: the scale of the departure (the decisive analytical step, forced by the follow-up's data);
   districts outside the follow-up (closed in this pass by a scope sentence in QS-4 s.6); the base of the shift (s.3
   moves the 2026 nonrespondents' allocations, s.6 measures the departure against the 2025 final file's); the
   follow-up's weighting (one sampling fraction in all five districts, so self-weighting).
6. What decides: an analytical choice (carrying a departure found on a non-random set of districts to the others).
REVIEW lines: all nine harmless.
Realism notes and dispositions: the methodology dated before the allocation run it describes (fixed, now dated
10 November); its reason for the previous year's shares (reworded to the processing calendar); QS-4 silent on
districts the follow-up did not cover (s.6 now says the follow-up stands for every district, scope only); the field
report's "most affluent to the most deprived" (inaccurate, since Southern Shore was not followed up; reworded to the
range of area deprivation, and the write-up's copy with it); the 88-in-100 fraction kept (3,617 of the 4,102
nonrespondents at the close, 88.2 per cent).

**Read 2 (after the fixes).**
1 to 4: none. 5: QS-4 s.2's headline rate, literal result the golden's definition; the reader lists the departure's
form (pooled or by district or band, additive or a ratio) as open, which is the decisive analytical step the
follow-up's cases settle, and a constant 1/0.88 weight, which leaves every estimate unchanged. 6: an analytical
choice, "how to estimate a departure and carry it to the other seven districts", with the maps, crosswalk keys,
duplicate routes, revised points and form builds as Layer 1. Changed passages: QS-4 s.6 fixes the population and not
the method; the methodology's allocation sentence and the field report's design sentence are harmless. Realism notes:
none needing a change (QS-4 approved before fieldwork, the crosswalk's reference form, the standard leaving the
departure's form to the analysis, the careers distractor's window).
