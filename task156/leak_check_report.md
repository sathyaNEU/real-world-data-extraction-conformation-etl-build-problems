# leak check, task156

**Verdict: REVIEW.** 10 files read, 57 golden figures and 31 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: golden, pillar, schedule, record, register, status, question, carried, decisive, repairs, service, replay, forecast, failure, repair, minutes, carries, history, orders, power-up, asserted, legacy, window, prototype, supply

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `asset_renewal_programme_2027.pdf`: 4 of 25 stump-paragraph terms appear (schedule, status, service, supply); read whether the document names the move
- **REVIEW** `concession_agreement_schedules_4_and_6.pdf`: 8 of 25 stump-paragraph terms appear (schedule, record, register, service, forecast, minutes); read whether the document names the move
- **REVIEW** `tariff_schedule_2026.pdf`: 3 of 25 stump-paragraph terms appear (register, service, minutes); read whether the document names the move

## 6 ranking artifacts (REVIEW 4)
- **REVIEW** `asset_renewal_programme_2027.pdf`: names 12 of 31 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `charge_point_register.xlsx`: names 30 of 31 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `planned_maintenance_schedule.xlsx`: names 30 of 31 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `work_orders_2023-2026.xlsx`: names 30 of 31 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `planned_maintenance_schedule.xlsx`: 84 ISO dates after 2026-11-06, e.g. 2027-01-18, 2027-01-20, 2027-01-21, 2027-02-04, 2027-02-08

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 32% of 208 prompts (cap 30%); reword at the role level, not the verb

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)
