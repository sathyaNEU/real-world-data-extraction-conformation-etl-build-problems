# leak check, task181

**Verdict: REVIEW.** 11 files read, 2 golden figures and 6 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: nowcast, expected, decisive, health, window, recent, excess, october, fortnight, specimens, record, director, public, operations, analytical, notifications, notified, griffith, episode, target, question, around, eventual, population, pattern

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `cd_weekly_report_2026_wk35.pdf`: golden figure 100 appears: ...a Last 4 weeks Year to date Year-to-date rate per 100,000 Wagga Wagga 16 73 106.0 Griffith 3 29 104.7 L...
- **REVIEW** `PR-07_pertussis_response_protocol.pdf`: carries 4 of 5 distinctive words of the committed call: 'Send the response team to Griffith this week.'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `PR-07_pertussis_response_protocol.pdf`: 12 of 25 stump-paragraph terms appear (expected, health, excess, specimens, record, director); read whether the document names the move
- **REVIEW** `SIPHU_PERTUSSIS_LINELIST_job_20261005_0700.txt`: 4 of 25 stump-paragraph terms appear (health, october, record, public); read whether the document names the move
- **REVIEW** `cd_weekly_report_2026_wk35.pdf`: 6 of 25 stump-paragraph terms appear (health, specimens, public, notifications, griffith, population); read whether the document names the move
- **REVIEW** `pertussis_line_list_notes.md`: 6 of 25 stump-paragraph terms appear (health, record, public, notified, episode, population); read whether the document names the move

## 6 ranking artifacts (REVIEW 5)
- **REVIEW** `PR-07_pertussis_response_protocol.pdf`: names 3 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `cd_weekly_report_2026_wk35.pdf`: names 3 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `pertussis_notifications_2019-2026.csv`: names 4 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `postcode_lga_concordance.xlsx`: names 3 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `school_rosters_term3_2026.xlsx`: names 4 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `antenatal_vaccinations_2019-2026.parquet`: 1177 ISO dates after 2026-10-05, e.g. 2026-10-06, 2026-10-07, 2026-10-08, 2026-10-09, 2026-10-10

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt form (clean)
## Solver's-eye read (pass 1, isolated reader, architecture 2, 2026-10-11)

1. "The team goes to the area with the largest excess of cases with specimens collected in the 14 days before the extract day over its expected count." (PR-07 4.2). The reader: the organisation's own rule, which the prompt sends you to; no file says which data step (case episodes, split postcodes, the extract day) tips the result.
2. none. The only per-area table (cd_weekly_report_2026_wk35.pdf) counts notifications received to 30 August and year-to-date rates, in the protocol's fixed order, five weeks before the window, with no expected count or excess.
3. none. Every file is something a public health unit holds anyway.
4. none. Every area name and figure sits in ordinary context; nothing states or scores the 5 October excess; the one tell found is the roster sheet order (REVIEW).

Plan (reader's own, abridged): pin the extract day (5 October local, window specimens 21 September to 4 October); collapse notifications to cases under 3.3 and 3.5; assign areas by postcode with split postcodes to the larger ratio; observed cases in the window; expected = mean of the same 14 dates in 2021 to 2025; excess; sensitivity checks (UTC extract day, notifications instead of cases, baseline without 2021). "Also note that Inland Pathology (178 of Griffith's 202 notifications) reports about 12 days after collection, against about 2 days for the hospital lab, so Griffith's last fortnight is incomplete. Report that, but PR-07 has no lag adjustment." Its result on the extract: Wagga Wagga 7.6, Griffith and Snowy Valleys 5.6, so Wagga Wagga. "No PR-07 reading I tried puts Griffith first; only a reporting-lag nowcast does."

REVIEW lines (reader's verdicts): the bulletin's 100 (rate label per 100,000): harmless; PR-07 carrying 4 of 5 call words (Griffith only in the 1.2 list): harmless; PR-07, bulletin, run report and notes vocabulary: harmless (their own subject matter; nothing about what to compute); PR-07, bulletin, line list and concordance naming areas beside numbers: harmless (fixed order, no scores on the decision question); school_rosters_term3_2026.xlsx: LEAK for ask B (the first five sheets were exactly the five schools that qualify on 5 October, the last four the near-misses; not by date received); the parquet's 1,177 future dates (estimated due dates of pregnancies in progress): harmless.

## Solver's-eye read (pass 2, isolated reader, architecture 2, after the roster fix, 2026-10-11)

1. "The team goes to the area with the largest excess of cases with specimens collected in the 14 days before the extract day over its expected count." (PR-07 4.2): the reader read it as the measure the prompt sends it to, not the result or which data step tips it; context, not a leak.
2. none. The bulletin counts notifications received to 30 August in fixed administrative order, with no 14-day specimen window and no expected count.
3. none. Every file is one the unit would keep anyway (the rosters as asked for under PR-07 5.2).
4. none. No document gives a 14-day count, expected count, excess or cluster list.

Plan (reader's own, abridged): pin the extract day from the run report; cases under 3.3; areas under 3.4; observed against the five-year expected count; Wagga Wagga 7.6, Griffith and Snowy Valleys 5.6; robustness checks; "Caveat: Inland Pathology (6 of Griffith's 7 window cases) reports about 12 days after collection against 2 for the hospital lab, but PR-07 4.1 fixes the count to the 07:00 extract"; the five clusters as the golden lists them.

REVIEW lines: all harmless, including the rosters workbook: "the sheets run in the order rosters arrived (08/09 Hurley Street to 01/10 Kooyoo Street). That order does not mark this week's clusters: Hurley Street, Fernleigh Road, Canal Road and Twynam Street have rosters but are not clusters, and the five clusters are sheets 4, 5, 6, 8 and 9."

Since pass 2 (2026-10-11): PR-07 5.1's slide sentence and the prompt's slide sentence changed (the slide now lists only the clusters in the area the team goes to, its school visits that week); leak.py rerun REVIEW with the same twelve lines and no new one; a reader re-read follows.
