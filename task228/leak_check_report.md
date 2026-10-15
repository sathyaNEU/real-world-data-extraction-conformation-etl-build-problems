# leak check, task228

**Verdict: REVIEW.** 14 files read, 13 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: variance, per-install, installs, decisive, platform, incidents, metric, install, allowance, method, sentence, record, telemetry, metric-definition-measurement-science, reconciliation, default, golden, estimand, exports, architecture, analytics, quality, duplicate, treatment, judged

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `data_dictionary.md`: carries 9 of 13 distinctive words of the committed call: 'The scorecard service should hold experiments on the gap-sessions check from January 2027, at a hold line of 0.28 percen'
- **REVIEW** `dh3_data_health_hold_standard.pdf`: carries 13 of 13 distinctive words of the committed call: 'The scorecard service should hold experiments on the gap-sessions check from January 2027, at a hold line of 0.28 percen'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `data_dictionary.md`: 9 of 25 stump-paragraph terms appear (installs, platform, incidents, install, telemetry, reconciliation); read whether the document names the move
- **REVIEW** `dh3_data_health_hold_standard.pdf`: 12 of 25 stump-paragraph terms appear (installs, platform, incidents, install, allowance, record); read whether the document names the move
- **REVIEW** `platform_change_log_2026.md`: 5 of 25 stump-paragraph terms appear (platform, install, record, exports, treatment); read whether the document names the move
- **REVIEW** `reconciliation_summary_2026.pdf`: 7 of 25 stump-paragraph terms appear (installs, install, record, telemetry, reconciliation, default); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `booking_queue_2027q1.csv`: 18 ISO dates after 2026-10-12, e.g. 2027-01-04, 2027-01-11, 2027-01-25, 2027-02-08, 2027-02-22

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

### Pass 1 (cut of 2026-10-15, before the reader's fixes)

1. **Decisive step.** No sentence names the decisive step as such. The nearest is DH-3 section 5: "Of the checks within the allowance, the service watches the one that would have held the most 2026 experiments with a confirmed data incident; where two would have held as many, the one that would have held fewer experiments without one." Section 4 gives the test ("significant at the two-sided 1 per cent level and lies in the check's hold direction"). Section 6 gives the hold-line frame ("A standard experiment from 2027 runs 14 days with 10,000 installs in each arm of its export and an even split. The line is set from both arms of the 2026 experiments that had no confirmed data incident."). The method is stated, not hidden. The "Each check judges each experiment once" line does not warn about multiplicity or power.
2. **Ranking file.** None. Nothing scores the checks against incidents. weekly_review_log_2026.csv ranks only the manual review. reconciliation_summary_2026.pdf lists confirmed incidents and their causes.
3. **Analyst-only file.** None clearly. reconciliation_summary_2026.pdf, the data dictionary, export_manifest.csv and platform_change_log_2026.md are plausible organisational files. booking_queue_2027q1.csv is the closest to a helper: it supplies the 2027 design shares, but it is not needed for the "standard experiment" line. app_releases_2026.csv and collector_daily_2026.csv look like distractors or context for the app-wide asks, and are natural to keep.
4. **Answer-like figure.** None. No file contains a hold line, a check ranking or a count of held experiments. The "5 October ... DH-3 approved" log entry names nothing. The app-wide `gap_sessions` column (identical on every platform row of an incident, for example 10152 on DI-26-025) is context for the asks, but it reads close to an answer cell for the "gap sessions it cost" ask.
5. **Literal sentences.**
   - "significant at the two-sided 1 per cent level and lies in the check's hold direction". Literal execution: a two-sided test at alpha 0.01, treatment against control, on the full run, with a direction filter per check. The test itself (two-proportion z, t, Welch, and so on) is not named.
   - "a check is within the allowance when it would have held no more than 2 per cent of the 2026 experiments without a confirmed data incident". Executed on the 82 experiments minus those with a confirmed incident.
   - "the one that would have held the most 2026 experiments with a confirmed data incident; where two would have held as many, the one that would have held fewer experiments without one". Gives the selection and the tie-break.
   - "the smallest difference between the arms, in the check's own unit (percentage points for a share), at which a standard experiment would be held. A standard experiment ... 10,000 installs in each arm of its export and an even split. The line is set from both arms of the 2026 experiments that had no confirmed data incident." Execution: pool the clean experiments' arms to get the baseline rate, and take the critical difference at 1 per cent two-sided for n=10,000 per arm. The variance method is not filed (pooled against unpooled, session-level against install-level clustering). "Both arms" is read as the pooling population.
   - "Treatment share ... below the design share in the registry". Compares the exported-install share with the design share.

   Ambiguous terms for the main question:
   - Whether sessions in the checks are clustered by install. Sessions are counted per session, but installs are the unit of assignment. The standard says "as a share of all sessions in the arm" and nothing about clustering. Nothing settles whether the test is a session-level proportion test or an install-level one. This could change both the holds and the line.
   - "Experiments with a confirmed data incident": matching the register to the registry is by typed titles (stray spaces and case differ), and some experiments have a preliminary row and then a confirmed row. "the incident register holds a confirmed incident against it" settles the status. App-wide incidents are not "against" an experiment.
   - The test is not named (z, chi-square, t on install means for events per install).
   - The "standard" 10,000 per arm: "install" in the export versus the pre-consent assigned count. "of its export" settles it.
   - Hold line sign and unit for the chosen check: a share check in percentage points is fixed, but if events per install were chosen the unit would be events, and the prompt says percentage points, which is itself a cue that a share check wins.
   - "Weekly review flagged": flag rows with later clear rows, notes only, flags carried over from 2025, review timestamps in UTC against Copenhagen weeks. No sentence settles whether a flag later cleared counts as flagged, or whether a flag that follows the readout counts.
   - Incident type: the register's `incident_type` ("the type of data incident the on-call engineer logged when the incident was opened") differs from the reconciliation's "Cause established" for some experiments (for example AV-26-008 is register "telemetry loss" and reconciliation "late delivery"; AV-26-039 is register "late delivery" and reconciliation "consent loss"). The register's wording suggests the logged type is initial, and the reconciliation's "cause established" is the confirmed one. Nothing explicitly says which type to use for "type of confirmed incident". This is a plausible semantic fork for the ask, not the main call.
   - "Share ... of the sessions that started in its window on the platforms it hit": `sessions_in_window` is per platform row and `gap_sessions` is the same total on each row, so the share is the total over the sum of the rows. The data dictionary mostly settles this.
6. **What decides the main answer.** An analytical choice, with some rule application. The check is chosen by a hold-rate comparison under a significance test, a 2 per cent false-hold allowance (82 experiments, so a few clean ones, which makes it a small-count / multiplicity judgment), and a 10,000-per-arm power line computed from the clean experiments. DH-3 sections 4 to 6 are the sentences that decide it. A solver who follows them literally gets a procedure, but the test choice (session against install clustering, overdispersion) is the real analytical step and is not filed. There is no planted decoy visible. The unmatched titles (stray spaces and case) are Layer 1 mess. The type difference between the register and the reconciliation is a data-semantics risk on the asks.

### Realism
- PDF metadata names a person as author and producer (Kaspar Gregersen, Inge Lund) with a midnight timestamp. There is no toolchain string. The xlsx creator is "Inge Lund", with no title.
- The reconciliation PDF looks plain and fine. The DH-3 standard text reads somewhat tailored: it states the allowance, the tie-break and the "standard experiment" in a way that reads like the task spec, and it names the 82 experiments and "every one a completed 14-day run".
- The register's `gap_sessions` repeats the same total on each platform row, which is odd but deliberate.
- The review log has two rows for AV-26-055 at the same second (flag and note, "no change in the data-health panel"), which is plausible mess. A flag on AV-25-190 and a note on AV-25-187 carried over from December are plausible.
- The reconciliation says "Sunday edition layout" is late delivery, while the register has telemetry loss. A non-confirmed finding in the reconciliation corresponds to a "withdrawn" register row, consistent.
- The change log entry for 12 October, "pulled for the choice of check", slightly announces the task's purpose.
- Review timestamps carry identical second values (07:37:07Z twice), a small oddity.

### Rulings on pass 1

- Questions 1 to 4: none. Harmless.
- Question 5, the test is not named: by design (the method is forced by assignment by install; every install-level method gives the same flags, asserted). Harmless.
- Question 5, the prompt's unit for the line (percentage points) cued a share check: fixed, the prompt now asks for the line in the check's own unit, which DH-3 s.6 defines.
- Question 5, flagged after the readout and cleared flags: fixed, every flag on a confirmed incident is logged at the review during its run and none is cleared; the prompt asks for flagged and never flagged.
- Question 5, the type of a confirmed incident: DH-3 s.7 now says the reconciliation establishes each incident's cause; the register's type is the call logged at opening (dictionary). The ask's device, kept.
- Realism: the change log's purpose clause removed; review stamps made unique and no note on an experiment flagged the same day; DH-3's specificity kept (a standard written for the choice names its record).

### Pass 2 (cut after the fixes)

1. Decisive step: no sentence names it. DH-3 section 5 gives the selection rule: "Of the checks within the allowance, the service watches the one that would have held the most 2026 experiments with a confirmed data incident", with the allowance "no more than 2 per cent of the 2026 experiments without a confirmed data incident". Section 4 gives the test: "significant at the two-sided 1 per cent level and lies in the check's hold direction". Section 6 says the line is "set from both arms of the 2026 experiments that had no confirmed data incident" for "10,000 installs in each arm ... an even split". These describe what to compute. They do not say which check wins or how to build the test (pooled-variance and the cluster/install-level question are left open). Nothing is flagged as the trap.
2. No file ranks the checks. No shipped file scores gap/duplicate/late/events/treatment share on the question. The weekly review log ranks nothing (it is the flag baseline). The reconciliation PDF gives server vs telemetry opens per experiment, not check performance.
3. Nothing exists only to help. reconciliation_summary_2026.pdf, weekly_review_log_2026.csv and data_dictionary.md are plausible desk records. booking_queue_2027q1.csv, app_releases_2026.csv and collector_daily_2026.csv look like distractors/context (booking queue is unused for the answer unless a hold line per queue is wanted). Mild: export_manifest.csv with row counts is tidy but normal.
4. No figure reads as the answer. The closest is the "2 per cent" allowance and the "10,000 installs in each arm" standard experiment in DH-3, which are the stated parameters, not results. Register gap_sessions on app-wide rows repeat one incident total on each platform row (e.g. DI-26-025: 10152 on android, ios and web), which looks like a cue for the share numerator but is context for an ask, not the main call.
5. Literal filed sentences:
   - "a check is within the allowance when it would have held no more than 2 per cent of the 2026 experiments without a confirmed data incident": executed literally, count non-incident experiments held (out of those with no confirmed incident), keep checks with count/N <= 0.02. With about 50+ clean experiments, that is at most 1 held.
   - "the one that would have held the most 2026 experiments with a confirmed data incident; where two would have held as many, the one that would have held fewer experiments without one": a full tie-break, closed.
   - "each counted as an experiment with a confirmed data incident when the incident register holds a confirmed incident against it": population is the 82 experiments; the match is by typed title (see ambiguities).
   - "significant at the two-sided 1 per cent level ... on the experiment's full run": literal execution gives a test on the export's installs/sessions; the test itself (two-proportion z on sessions, t/Welch on events per install, binomial/z on share vs design) is not named.
   - "the smallest difference between the arms ... at which a standard experiment would be held. ... 10,000 installs in each arm ... set from both arms of the 2026 experiments that had no confirmed data incident": population is the clean experiments pooled over both arms; the variance basis (session-level binomial vs install-level overdispersion, sessions per install, mean sessions) is left to the analyst.
   Ambiguities for the MAIN question:
   - Whether sessions or installs are the unit for the share checks (install-level clustering changes the 1% line); "as a share of all sessions in the arm" fixes the numerator and denominator but not the variance. Settled partly by the sentence on the measure, not by one on the test.
   - "confirmed data incident against it": register rows list the experiment by desk-typed title with irregular case and double spaces ("Sunday  edition layout", "search empty state"); matching to the registry needs normalisation. Experiments with preliminary then withdrawn are not confirmed; app-wide incidents hit no single experiment ("no comparison between arms can see them"), which settles those as excluded.
   - Experiments with a confirmed incident whose key is absent from the register by title (the PDF shows keys, e.g. AV-26-023, AV-26-031, AV-26-039, AV-26-056 confirmed) vs those in the register: the register is the stated authority.
   - Treatment share: "below the design share in the registry" uses exported installs (not assigned), consistent with section 3.
   - "Held by the weekly review" for the ask: action flag with a later clear is still a flag; "carried over from December" rows (AV-25-xxx) are outside the 2026 experiments; note is not a flag.
   - Incident type: register `incident_type` is what the on-call engineer logged at opening, while the PDF gives "Cause established"; the two can differ (e.g. DI-26-012 Most read rail order logged late delivery, PDF row AV-26-039 shows consent loss). The dictionary says register type is "logged when the incident was opened", which implies using the established cause for a per-type split, but the ask says "type of confirmed incident" without choosing. This is a possible fork for the asks, not the main call. The dictionary line is the nearest settling sentence.
   - App-wide share: sessions_in_window is per platform row and gap_sessions is the same incident total repeated on each row; "on the platforms it hit" implies summing the platform denominators once and counting gap sessions once. Not stated.
6. The main call is decided by analytical choice: how to test each check at the 1% level on a pooled null built from the clean experiments, and then the cost/benefit selection under the 2% allowance. There is some data-semantics load too (matching titles, using the reconciliation cause, deduplicating register rows, service 1 vs 2 column names) but that is Layer 1 cleaning. No decoy is planted; the notes, change log and dictionary support the intended path rather than argue a wrong one. Nothing in DH-3 section 5 reduces to a mechanical procedure without a statistical test choice, but a solver who runs a plain two-proportion test at session level will probably get a different set of holds than one who respects install-level or overdispersion, and DH-3 does not say which. That is the intended trap seat and it is not announced.

### Realism
- Prompt bundles five different asks in one paragraph; reads like a spec, slightly dense but plausible.
- Register titles typed with stray double spaces and case drift (intentional mess, looks authentic).
- Weekly review log timestamps are all in reviewer morning hours and unsorted within a week (fine); comments reuse four stock phrases ("telemetry looked off in the scorecard; readout held for a check") which looks templated.
- Reconciliation PDF has an empty "Reconciliation of September 2026" heading orphaned across the page break and no Aug/Oct sections although the register says reconciliations ran in August and October (register status_date 2026-08-11, 2026-10-09); the PDF months (Feb to Jul, Sep) do not match the register's reconciliation months (March to August, October). Looks inconsistent or generated.
- app_releases sdk_version values wobble (9.1.2 on 10.0.0 iOS after 9.1.1 on 9.6.0 and then 9.0.0 on 9.3.0) and do not track the change-log SDK 9.3 and 9.4.1 events; machine-random.
- app-wide incident gap_sessions identical across platform rows is a plausible reconciliation total but oddly formatted.
- All 82 experiments start on Mondays and last exactly 14 days with round assigned counts; very regular.

### Rulings on pass 2

- Questions 1 to 4: none. Question 6: analytical. Harmless.
- Ask-side readings (register type against cause established, the repeated app-wide figure): the ask devices, settled by the records (dictionary and DH-3 s.7; rows whose gap sessions exceed their own sessions). Kept.
- Realism: reconciliation months now named the same way in the summary and the register (the month the reconciliation ran, and the runs it covered); SDK versions in the release file follow the change log; review comments varied. Fixed in the generator; no graded figure moved (checks, verify and figures_check re-run).
