# leak check, task173

**Verdict: REVIEW.** 11 files read, 21 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: elective, hospital, capacity, population, admission, method, decisive, demand, spells, planning, listed, hazard, centre, forecasting, month-end, series, definitions, migration, systems, window, monthly, episodes, activity, cholecystectomy, default

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `elective_capacity_plan_2027_28_general_surgery.pdf`: golden figure 430 appears: ...990 810 650 460 330 200 170 Hernia repair 510 510 430 330 280 230 180 130 Other general surgery 300 300...
- **REVIEW** `operational_plan_2027_28_activity_lines.pdf`: carries 5 of 6 distinctive words of the committed call: 'The 2027/28 plan should carry 400 emergency admissions with gallstone disease on NEL-GS-07.'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `elective_access_policy_v6.pdf`: 3 of 25 stump-paragraph terms appear (elective, hospital, admission); read whether the document names the move
- **REVIEW** `elective_capacity_plan_2027_28_general_surgery.pdf`: 5 of 25 stump-paragraph terms appear (elective, hospital, capacity, centre, cholecystectomy); read whether the document names the move
- **REVIEW** `operational_plan_2027_28_activity_lines.pdf`: 10 of 25 stump-paragraph terms appear (elective, hospital, capacity, admission, method, spells); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `admitted_ptl_snapshots_2021_2026.parquet`: 124 ISO dates after 2026-10-31, e.g. 2026-11-01, 2026-11-02, 2026-11-03, 2026-11-04, 2026-11-05

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated reader (general-purpose, sonnet, medium), fresh copies of prompt.txt and target/ only, 2026-11-02.

1. Decisive step: none; nearest, the capacity plan's sessions sentence and the activity lines' plan basis, both generic.
2. Ranking or scoring file: none.
3. Helper-only file: none (the Fennick number map a plain join key; the access policy, ECDS and theatre log read as context).
4. Figure or name reading as the answer: none.
5. NEL-GS-07 with "counted once per spell in the month of the admission date" and "the expected number, not a prudent, stretch or contract figure": spells with an emergency method and a first-episode gallstone code, the central expectation for 2027/28, consistent with the capacity plan, to the nearest 50; it fixes the WHAT and no method. The golden's literal estimand.
6. An analytical choice: a forward forecast that has to take account of the Wyecross opening and the planned list fall; the line definition sets only the population.
- a (a plan-table value equal to an ask figure): harmless, a planned waiting-list count.
- b (the activity lines share the call sentence's words): harmless, the filed estimand.
- c (PTL dates after 31 October 2026): harmless if TCI dates; they are (`tci_date`, booked admissions), no snapshot or date added after the cut.
- Realism tells: tidy ID sequences, ECDS text with little variety, M-prefixed numbers everywhere, a short capacity plan.

## Solver's-eye read

Isolated reader (general-purpose, sonnet, medium), fresh copies of prompt.txt and target/ only, 2026-11-02 (before the
round-1 WHAT sentences; the documents changed only by those three sentences afterwards).

1. Decisive step: none; nearest, the capacity plan's sessions sentence and the activity lines' plan basis, both generic.
2. Ranking or scoring file: none.
3. Helper-only file: none (the Fennick number map a plain join key; the access policy, ECDS and theatre log read as context).
4. Figure or name reading as the answer: none.
5. NEL-GS-07 with "counted once per spell in the month of the admission date" and "the expected number, not a prudent, stretch or contract figure": the golden's literal estimand; it fixes the WHAT and no method.
6. An analytical choice: a forward forecast that has to take account of the Wyecross opening and the planned list fall.
- a (a plan-table value equal to an ask figure): harmless. b (the activity lines share the call's words): harmless, the filed estimand. c (PTL dates after 31 October 2026): harmless, all 124 in `tci_date`, booked admissions (checked).
- Realism tells: tidy ID sequences, ECDS text with little variety, a short capacity plan (presentation only).
