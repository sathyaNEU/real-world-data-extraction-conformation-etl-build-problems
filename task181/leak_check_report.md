# leak check, task181

**Verdict: REVIEW.** 11 files read, 2 golden figures and 6 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: nowcast, notifications, decisive, method, definition, notified, pooled, expected, health, another, griffith, specimen, received, fortnight, forecasting, eventual, excess, window, complete, recent, specimens, record, maturity, censoring, nothing

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `cd_weekly_report_2026_wk35.pdf`: golden figure 100 appears: ...a Last 4 weeks Year to date Year-to-date rate per 100,000 Wagga Wagga 16 73 106.0 Griffith 3 29 104.7 L...
- **REVIEW** `PR-07_pertussis_response_protocol.pdf`: carries 4 of 5 distinctive words of the committed call: 'Send the response team to Griffith this week.'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `PR-07_pertussis_response_protocol.pdf`: 11 of 25 stump-paragraph terms appear (notifications, definition, notified, expected, health, griffith); read whether the document names the move
- **REVIEW** `SIPHU_PERTUSSIS_LINELIST_job_20261005_0700.txt`: 5 of 25 stump-paragraph terms appear (health, specimen, received, complete, record); read whether the document names the move
- **REVIEW** `cd_weekly_report_2026_wk35.pdf`: 6 of 25 stump-paragraph terms appear (notifications, health, griffith, specimen, received, specimens); read whether the document names the move
- **REVIEW** `pertussis_line_list_notes.md`: 5 of 25 stump-paragraph terms appear (notified, health, specimen, received, record); read whether the document names the move

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

## Solver's-eye read

Pass 4: one isolated reader on Sonnet, 2026-10-11, after PR-07 4.2 pinned the estimand.

1. **none.** PR-07 4.2 "reads as a definition and does not say to nowcast, dedupe or adjust"; 3.3 and 3.5 are
   routine definitions.
2. **none.** The week 35 report ranks areas by notifications received and by rate, a different quantity; it gives
   no 14-day excess, no school clusters and no CSV figure.
3. **none.** The nearest is the line-list notes, a data dictionary a surveillance officer keeps.
4. **none.** The weekly report's counts are received-date counts, not the protocol's quantity.

**Plan (summarised).**
- Episodes under 3.3, dated by the first specimen (3.5), on the 21 September to 4 October window.
- It reads the window as incomplete under 4.2 and completes it from the specimen-to-notification lags, "per area or
  overall".
- Then the excess over the 2021 to 2025 mean, the Griffith-area school clusters, and the CSV.

**REVIEW lines: all harmless.** Each one reads as context or the protocol's own definitions; none ranks the areas on
the 14-day excess.

**Realism notes (deferred):**
- the extract holds no notification after 3 October;
- school fields are sparse, since the form changed on 1 September;
- the week 35 report is five weeks older than the extract;
- the run report reads tidier than a real scheduler log;
- the concordance ratios are not ABS-style RATIO_FROM_TO columns;
- the roster sheet names are shortened, with no key to the free-text school names.
