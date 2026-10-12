# leak check, task230

**Verdict: REVIEW.** 27 files read, 36 golden figures and 3 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: segment, patients, method, quarter, forecast, inside, decisive, operations, back-test, patient, architecture, closed, repeat, driver, detection, default, phones, registered, window, series, selection, design, monthly, nothing, shift-day

## 3 answer figures in the pack (REVIEW 4)
- **REVIEW** `QCP-04_first_pass_quality_control.docx`: golden figure 4.3 appears: ...e). A forecast equal to the limit stays off. 4.3 Records. Every stream's forecast, a new client's...
- **REVIEW** `client_quality_schedules_2026.pdf`: golden figure 5.2 appears: ...9.80% 6% of the stream's monthly invoice KBA-PROF 5.2 99.48% 6% of the stream's monthly invoice Measure...
- **REVIEW** `client_rate_cards_2026.pdf`: golden figure 0.80 appears: ...M-FNOL Core 0 to 39,999 0.86 Plus 40,000 and over 0.80 Hollings & Pryce (GBP, per document captured (doc...
- **REVIEW** `client_rate_cards_2026.pdf`: golden figure 3.9 appears: ...act anniversary, 16 November, unit prices rise by 3.9% (rounded to the nearest 0.0001 of a unit) for do...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `QCP-04_first_pass_quality_control.docx`: 6 of 25 stump-paragraph terms appear (method, quarter, forecast, operations, closed, shift-day); read whether the document names the move
- **REVIEW** `capture_mis_extract_notes.md`: 5 of 25 stump-paragraph terms appear (forecast, closed, design, nothing, shift-day); read whether the document names the move
- **REVIEW** `hollings_pryce_pilot_report.docx`: 3 of 25 stump-paragraph terms appear (forecast, inside, shift-day); read whether the document names the move

## 9 dates after the setting (REVIEW 5)
- **REVIEW** `form_specifications.xlsx`: 4 ISO dates after 2026-10-28, e.g. 2026-11-09, 2026-11-16, 2026-11-23
- **REVIEW** `hollings_pryce_forecast_nov26.json`: 10 ISO dates after 2026-10-28, e.g. 2026-11-02, 2026-11-09, 2026-11-16, 2026-11-23, 2026-11-30
- **REVIEW** `november_operating_plan.xlsx`: 30 ISO dates after 2026-10-28, e.g. 2026-11-01, 2026-11-02, 2026-11-03, 2026-11-04, 2026-11-05
- **REVIEW** `stream_register.csv`: 3 ISO dates after 2026-10-28, e.g. 2026-10-31, 2026-11-01
- **REVIEW** `wattlebird_coolabah_forecasts_fy27.xlsx`: 19 ISO dates after 2026-10-28, e.g. 2026-11-01, 2026-11-02, 2026-11-08, 2026-11-09, 2026-11-15

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read (architecture 2)

Read 1 (2026-10-11, Sonnet at medium effort), verbatim:

I read prompt.txt and the readable files in target/. I did not open the large parquet and CSV logs (first-pass verifications, field edits, blind re-key audit, second-pass sessions, delivery manifests, keystroke telemetry, OCR summary, the client audit returns). I computed nothing.

**1. Decisive step.** No sentence announces it. Closest are two filed statements, which I read as the estimand and method rather than a hint:
- QCP-04_first_pass_quality_control.docx s4.3: "Every stream's forecast, a new client's included, is made by the same method, from the last closed quarter's first-pass log and blind re-key audit and from the operating plan of record for the month."
- QCP-04 s4.1: "...over every document the month's operating plan of record routes to the stream's queue."

Together they signal that a forecast is needed, not just last quarter's rate. "A new client's included" points at Hollings & Pryce, where the pilot is the only evidence. It names no move, but it is the nearest thing to a pointer. I would not call it a leak.

**2. File that ranks or scores the candidates.** None. The nearest are:
- november_operating_plan.xlsx, sheet "October second pass": last month's list of streams. It lists the five US streams (I saw seven rows, five of them stream rows). That is the prior month's call, not this one.
- hollings_pryce_pilot_report.docx: for the new client only (see Q4).

**3. File with no reason to exist except to help.** None clearly. The closest is second_pass_labour_planning_note.docx, which spells out how to get hours: documents = daily key fields / key fields per document by form version in force; minutes per document by form family from the September sessions export, with typed forms taking the Hollings & Pryce pilot sessions. It is plausible as an MIS planning note, but it is the only file that is pure method for one ask. capture_mis_extract_notes.md is a normal data dictionary.

**4. Figure or name that reads as the answer.** hollings_pryce_pilot_report.docx: "The pilot's residual sat inside the limit agreed for go-live" and the table row "Residual after first pass, per 1,000 key fields | 0.69", set against the 0.77 limit in the quality schedule. It reads as "H&P stays off". The same report says second-pass verification ran on the pilot's documents throughout, which a careful reader will question. As written it is a context figure with a visible caveat, not an instruction.

**5. Filed sentence fixing the main figure.** QCP-04 s4.2: "A stream is on second-pass verification for the month when its forecast exceeds its contract limit... A forecast equal to the limit stays off." With s4.1, a literal execution gives:
- One forecast per stream, built the same way for all eleven streams.
- The forecast is a first-pass residual: key fields whose value after first pass differs from the image as the blind re-key adjudicates, per 1,000 key fields first-pass verified, over every document the November plan of record routes to that stream's queue.
- It is compared with the contract limit in the client's schedule, using the unrounded forecast, and the stream goes on second pass only if strictly above the limit.
- The inputs are the closed Q3 log and audit, re-weighted to the November plan. The plan changes the queue for TCM-FNOL (to night) and adds HPY-TYPD (day), and form versions change within the month.

**Fork line.** Yes, several:
- "its third-quarter residual as the client's own audit counted it." Each client schedule defines its own capture-error codes, time zone for the quarter and delivery date, and "the re-review replaces the original". Hollings & Pryce has no client audit until 1 January 2027 ("Until then the supplier's own blind re-key audit is the measure"). One reading gives a figure for H&P from our own audit or the pilot. The other reads it as not applicable or blank. That changes one asked figure.
- "the service credit its client could claim if the stream broke its quality limit in November, in that contract's currency". "Monthly invoice" could mean November documents at the band the account's whole-month volume sets, with or without the indexation uplift from the anniversary shift-day (20 Nov for Kessington, Northgate, Brightmoor and Harbison; 9 Nov Coolabah; 16 Nov Whinfell). The billing register's October bands could be read as the November price instead. This changes the credit figures.
- "ordered by the credit". The credits are in USD, AUD and GBP. The plan's budget-rate sheet ("compared at these budget rates") gives INR conversion. Ordering and the title stream could be by converted value or by raw numbers. This changes the slide, not a cell.
- "the second-pass hours November would take" for streams the rule leaves off: hours for every stream "whichever way it is called" is clear. The unit is not: the planning note's minutes per document are productive minutes, while the pilot report's "6.5 productive hours a person-shift" suggests a staffing reading. This is minor.
- "Plan of record" is Version 3, and the stream forecasts have several revisions. The plan notes "forecasts as accepted for planning", which probably settles it.

**REVIEW lines:**
- QCP-04 "4.3": harmless. It is the section number "4.3" in the text, not the figure 4.3.
- client_quality_schedules "5.2": harmless. It is the filed KBA-PROF limit, a context input and not an output.
- client_rate_cards "0.80": harmless. It is the filed TCM-FNOL Plus unit price, an input.
- client_rate_cards "3.9": harmless. It is the filed Whinfell indexation percentage, an input.
- QCP-04 stump-term overlap: harmless. The matched words (method, quarter, forecast, closed, shift-day) are the procedure's own vocabulary. s4.3 states the forecast method but names no move beyond the estimand.
- capture_mis_extract_notes.md term overlap: harmless. It is a data dictionary and it does not name a step.
- hollings_pryce_pilot_report.docx term overlap: harmless on vocabulary. The content itself is the Q4 context decoy, but it is a filed report and not an instruction.
- form_specifications.xlsx dates after 2026-10-28: harmless. They are forward form-version effective dates (9, 16 and 23 Nov), which is normal for a plan.
- hollings_pryce_forecast_nov26.json dates: harmless. Forward week-commencing dates in a November forecast.
- november_operating_plan.xlsx dates: harmless. The November plan's own shift-days.
- stream_register.csv dates: harmless. It is the 31 Oct and 1 Nov queue switch for TCM-FNOL and the H&P effective dates, which are facts of the setting.
- wattlebird_coolabah_forecasts_fy27.xlsx dates: harmless. Forward weeks in a forecast file.

**Realism tells:**
- The three-revision forecast series in several clients' files look like one revision scaled by a constant factor per client and per file, applied to every week. For example H&P rev 1 to rev 2 is about +7.4 to 7.6% every week, Kessington R1 to R2 about +4.7% to every row, Whinfell and Thistlecombe also move in lockstep. Real revisions drift unevenly.
- client_quality_schedules_2026.pdf uses identical boilerplate for every client's measurement paragraph, differing only in code list and time zone. It reads as templated rather than lawyered per contract.
- The operating plan's daily key fields are near-flat per weekday with remainders on the earliest days, which is what the plan's own note describes. That reads as formula-spread, as expected for such a plan.
- The pilot report's table is perfectly tidy: 5,933 documents × 12 key fields = 71,196, and the audited count equals the verified count exactly (100% audit share). That is plausible given the 100% pilot sample, but very clean.
- The extract notes list row counts to the unit (1,259,599; 466,253; 2,381,352) and state the exact export dates. This is slightly too tidy for an MIS README, but not objectionable.
- The Hollings & Pryce schedule row has accuracy "99.923%" and a 0.77 limit, while every other stream's accuracy has two decimals. It is consistent arithmetically and looks fine.
