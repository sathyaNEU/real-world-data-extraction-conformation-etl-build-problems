# leak check, task118

**Verdict: REVIEW.** 12 files read, 24 golden figures and 5 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: headline, release, extract, national, readers, template, clicks, culture, policy, section, current, months, golden, article, system, change, architecture, reading, corrections, minutes, device, record, export, counts, primary

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `falls_indicator_definition_v2.pdf`: 3 of 25 stump-paragraph terms appear (national, change, counts); read whether the document names the move
- **REVIEW** `hypnotics_deprescribing_policy_2026.pdf`: 4 of 25 stump-paragraph terms appear (policy, current, months, primary); read whether the document names the move

## 6 ranking artifacts (REVIEW 1, INFO 1)
- **REVIEW** `hypnotic_prescribing_dashboard_q2_2026.xlsx`: names 4 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `practice_locality_register_2026.xlsx`: names 4 of 5 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `repeat_templates_hypnotics_2026-10-01.csv`: 31183 ISO dates after 2026-10-20, e.g. 2026-10-21, 2026-10-22, 2026-10-23, 2026-10-24, 2026-10-25

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Architecture 3, read 1 on target.zip 900e68f6 (isolated Sonnet reader, fresh copy of prompt.txt and target/ only).

1. Decisive step: quoted the policy's section 6 placement sentence (the estimand: the admissions the 45 in 100 who come
   off would have had on the drug from 1 April to 31 December 2027, less those off it). It names no source for a start
   and no dating step. Ruled: no decisive-step sentence.
2. Ranking file: none (the dashboard carries prescribing volumes and cost only).
3. Helping file: provider_site_codes.csv. Ruled harmless: the ODS site list the SUS cohort's site codes come from, the
   publisher's own reference data, which a reader needs to know the community sites are hospitals; it changes no
   figure.
4. Answer figure or name: none.
5. Population sentence: the policy's section 4 current-user definition; its literal result (everyone 65 or over on 1
   January 2027 with an item dispensed 1 July to 30 September 2026, by registered practice) is the golden's population.
6. What decides: an analytical choice, the start of each user's time on the drug, which the April to September extract
   cannot show and the template chains (through the moved practice's previous system) hold.

REVIEW lines: the dashboard harmless (no falls or avoided figure ranks the localities); the templates' post-setting
dates harmless (all in review_date, the next planned review). Realism tells: none.
