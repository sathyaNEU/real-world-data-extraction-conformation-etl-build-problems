# leak check, task198

**Verdict: REVIEW.** 19 files read, 34 golden figures and 10 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: quarters, framework, standard, positions, offered, asserted, states, extract, decisive, member, export, quantity, sentence, migration, minutes, occupancy, corrections, points, client, reading, staffed, carried, rostered, window, history

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `member_service_standard_2025.pdf`: golden figure 4.2 appears: ...to be answered within the target for that queue. 4.2 A quarter below the ceiling is reported to the Me...
- **REVIEW** `service_assurance_framework_2026.pdf`: golden figure 4.2 appears: ...practice and is directed at a single case queue. 4.2 The review candidate for a half year is the case...

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `fee_schedule_2025.pdf`: 3 of 25 stump-paragraph terms appear (extract, member, corrections); read whether the document names the move
- **REVIEW** `member_service_standard_2025.pdf`: 4 of 25 stump-paragraph terms appear (standard, extract, member, corrections); read whether the document names the move
- **REVIEW** `service_assurance_framework_2026.pdf`: 13 of 25 stump-paragraph terms appear (quarters, framework, standard, positions, offered, extract); read whether the document names the move
- **REVIEW** `work_measurement_standard_2022.pdf`: 7 of 25 stump-paragraph terms appear (standard, positions, offered, member, minutes, corrections); read whether the document names the move

## 6 ranking artifacts (REVIEW 1, INFO 1)
- **REVIEW** `trustee_report_membership_2026.pdf`: names 10 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `schemes_register_2026.csv`: names 10 of 10 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `public_holidays_ie_2022_2026.csv`: 6 ISO dates after 2026-04-30, e.g. 2026-05-04, 2026-06-01, 2026-08-03, 2026-10-26, 2026-12-25

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

One isolated reader, medium effort, seeing only `prompt.txt` and a fresh unzip of the 19-member
`target.zip` (md5 2d0a08cf33b050578a0d0beefdafb64d). It read every workbook sheet, both case extracts and
every PDF; no hidden sheets, no cell comments.

**It landed the call.** MS-CQ (Contribution queries), FY2026 breach share 12.4 per cent on 6,480 cases
received, at about 65 per cent confidence, with the naive all-quarters route rejected (it gives MS-DC at
+20.5 points). It also reproduced the FY2026 share for all nine queues, the late-case ask at 1,799 of
19,222, and the ten scheme rates per 1,000 exactly.

**Question 1, a sentence it quoted.** `service_assurance_framework_2026.pdf` clause 4.2: "The review
candidate for a half year is the case queue whose share of cases received in the preceding financial year
that were answered later than the target set for that queue stands furthest above, in percentage points,
the share the same queue reached in those of its quarters in the three financial years before that one
which carried the same offered load." With 4.3 defining offered load in positions-equivalents. Its answer
to question 6 is "an analytical choice, which baseline quarters are comparable", with the caveat that "a
reader who follows 4.2 and 4.3 as a procedure can reach it by execution, and 4.2 does not fix how close
'the same' load must be."

**The flip it measured, which is the ship-blocking finding.** Load-matched excess: MS-CQ +10.2 to +11.0
points, MS-IS +4.6 at tight matching but +11.7 if the tolerance is loose. So the call is MS-CQ when load
is matched within about 0.1 positions and MS-IS under a loose reading, and no shipped sentence fixes the
tolerance. An answer that flips on an unstated convention is Gate C, `underspecified_objective`.

**Question 2, none.** The nearest is `service_monitoring_export.xlsx`, on a closed-in-quarter basis, which
says in its own notes that it does not rank queues.

**Question 3, four helper files named:** `data_dictionary.csv`, `export_manifest.csv`,
`case_status_reference.json` and `queue_reference.csv`, with `public_holidays_ie_2022_2026.csv` as a fifth
for the clock.

**Question 4, none.** The raw FY2026 ranking (MS-IS 29.8, MS-DC 25.8) is what a first pass produces.

**An ask fork.** On the chargeable-cases ask it is "about 50 per cent sure which basis the asker wants":
by response date over the six fee-schedule queues it gets Q1 1,905, against the golden's 1,593 by charge
date. April to June 2025 charges fall short of responses (April 377 against 673) with nothing in the pack
explaining it.

**Realism and signposting, its own list.** Clause 4.2 reads as an analytical specification rather than a
board framework, and 4.4 mirrors the prompt's deliverable. The authority letter pointing at the firm's own
clause reads as a pointer built into the pack. The monitoring export's notes tell the solver it is the
wrong basis. The roster notes explain the one structural break the answer depends on (MS-DC's nine
temporary positions, both ended 31 March 2025). The trustee report and the data dictionary each state a
cleaning rule outright, and standard 3.6 and the TRF note in `case_status_reference.json` read as
resolutions to traps.
