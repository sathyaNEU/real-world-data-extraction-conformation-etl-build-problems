# leak check, task162

**Verdict: REVIEW.** 13 files read, 11 golden figures and 4 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: release, restart, record, version, adoption, reports, installs, tuesday, releases, first-quarter, windows, export, restarts, calendar, install, first-use, method, thread, profile, dashboard, exposure, forward, scaled, update, window

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `release_calendar_2025_2027.pdf`: 5 of 25 stump-paragraph terms appear (release, version, releases, calendar, update); read whether the document names the move
- **REVIEW** `tracker_cutover_runbook.docx`: 5 of 25 stump-paragraph terms appear (release, record, version, reports, export); read whether the document names the move

## 6 ranking artifacts (INFO 1)
- **INFO** `component_groups.xlsx`: names 3 of 4 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

One isolated reader (Sonnet, medium) on a fresh copy of prompt.txt and target/ (target.zip 62e91745, the determinism
repair of 2026-10-27), never the design note, generator or submission. The stump-vocabulary sweep's REVIEW lines were
ruled in the main thread and not handed over. Its answers, verbatim:

1. Decisive step: none stated as such. Closest, staffing_plan_q1_2027.eml: "size for the expected load in the quarter's busiest week at 120 triage items per triager-week, rounding up" (fixes the sizing rule, not the forecasting method). The method for turning the old record into the triage-item series is left to the analyst; the runbook only defines what counts.
2. No file ranks candidates or states a forecast. triage_dashboard_weekly.xlsx gives weekly "New defects" by product, but on the old definition (excludes DUPLICATE/INVALID/WORKSFORME/MOVED, groups by current product), and its parallel-run weeks are zero. The eml says the old dashboard's number "won't line up". No figure on the main question.
3. Helper-type files: tracker_cutover_runbook.docx (definitions of what is migrated and what counts as a triage item); triage_working_agreement.docx (definitions of triage action, closed, week, group intake); component_groups.xlsx (component-to-group mapping, a lookup register); triage_dashboard_weekly.xlsx header and notes explain its own counting. No readme, manifest or data dictionary as such.
4. Nothing reads as the answer. The only quantities are context: "120 triage items per triager-week", the dashboard's old-definition weekly counts.
5. Literal sentences:
- eml: "size for the expected load in the quarter's busiest week at 120 triage items per triager-week, rounding up. Q1 ... the 13 weeks Mon 4 Jan to Sun 4 Apr, weeks Monday to Sunday, Helsinki time." Reading: forecast each of the 13 weeks, take the largest, divide by the capacity, round up.
- runbook: "Every report filed through the report form is a triage item, duplicates included" (include duplicates). "Reports in the security group ... are not triage items. Spam caught by the form's filter never reaches the queue." (exclude security). "A report the team moves to another team's project during triage stays a triage item." (include moved). "The form takes reports from release, beta and nightly builds, and each is a triage item whatever version the reporter runs." (include all channels). "Reports filed with the Report a site issue tool go to ... WEBC ... and are not triage items." (exclude site-issue reports). "Migrated reports keep their state and are not new triage items." (exclude migrated). "A report is counted in the week it is filed." "Until the cutover the team counts from the old tracker's weekly triage export: every report filed through the form there and no other, wherever the report sits now." (count all form-filed reports on the old tracker regardless of current status or product).
- working agreement: "A triage action is a change by one of the rota's triagers to a report's status, resolution, component or priority, or a move of the report to another team's project. The target is a triage action on every report within 24 hours of its filing." (only rota triagers' changes count, not bridge changes). "A report is closed when it is in Resolved or Closed, or sits in another team's project." "Weeks run Monday to Sunday, Helsinki time ... The parallel run's reports are those filed from 00:00 on Monday 2 November to 23:59 on Sunday 29 November." "A group's intake is the reports that arrive in its components, each report counted once, in the group of the component it comes in with; a component set in triage does not change where a report arrived." (group by the initial component; multi-group reports once).
- component_groups.xlsx: "A report with components in more than one group is in each of those groups' queues." (this sits against the agreement's "each report counted once"; a possible tension, see 8).
6. (a) an analytical choice, with a rule-application and data-reading layer around it: the forecast of the busiest week from the conformed old-tracker series (no filed method, in the data only), with the counting definitions all stated literally in tracker_cutover_runbook.docx. Deciding source: the eml's busiest-week sizing instruction plus the old export.
7. Mostly realistic (Jira JSON with changelogs, Bugzilla-style CSV, dated eml, release calendar). Possibly neat: the repeated, near-identical rota rows and dashboard "New defects" formulas; the runbook sentence "so that the parallel run's duplicates had reports to link to" and the dashboard note "closed MOVED here on 30.11.2026" read as explanatory for the analyst. The dashboard's zero rows for the run weeks are an intentional tell but plausible.
8. Yes. (i) Group intake: working_agreement says each report counted once in the group of the component it arrives with, while component_groups.xlsx says a multi-group report is in each group's queue and the working agreement says "A report that spans two areas gets both components". Readings: count once by the first/arrival component, or count in every group it touches (group counts then exceed the report total). The "arrive ... comes in with" wording probably resolves it but "which component if two arrive together" is open. (ii) "closed by the time the run ended": run end could be 29 Nov 23:59 or the 4 Dec export; the runbook says exported 4 Dec and the rota speaks of follow-up through 4 Dec, so this is arguable. (iii) "no triage action within 24 hours" for a report filed in the final hours of the run or ones migrated by the bridge: baseline is clear, little else. (iv) The "busiest week" is not stated as a forecast window but the eml supplies the 13 weeks; low risk.

Main thread's ruling, one line each:
- Q1, Q2, Q4: none. Q6: analytical. Every Q5 sentence executes to the golden's population (each is a filed WHAT).
- Q3: the runbook, the working agreement and the component register are the organisation's own governing documents
  and lookup; no file describes the data (the manifest and the field notes were withdrawn in this repair).
- Q7: the runbook's trial-migration sentence and the dashboard's note on the run's weeks were in the pack the stage 4
  reader and both portal judges read; each states an operational fact the document's genre records. Harmless.
- Q8 (i): every one of the run's 1,533 items comes in with exactly one grouped component (asserted, SF15), so the
  register's queue sentence and the agreement's count once give the same figures; read over later components it is
  ruled out by "a component set in triage does not change where a report arrived". Closed.
- Q8 (ii): the run is 2 to 29 November in the runbook's heading and the agreement's span ("to 23:59 on Sunday
  29 November"); the 4 December export is the export's date, not the run's end. Both portal judges reproduced Ask A on
  that reading. Closed.
