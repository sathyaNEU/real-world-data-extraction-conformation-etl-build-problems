# leak check, task230

**Verdict: REVIEW.** 17 files read, 53 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: november, stream, population, default, client, decision, processing, sentence, forecast, method, window, counts, carried, decisive, operations, quarter, workload, selection, nothing, asserted, closed, back-test, architecture, measured, suggestion

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `OQ-4_occupation_output_quality_standard.docx`: golden figure 3.2 appears: ...that the reference coding puts in the group. 3.2 The reference coding of a write-in is the code th...
- **REVIEW** `OQ-4_occupation_output_quality_standard.docx`: golden figure 2.0 appears: ...r group whose coding bias is beyond plus or minus 2.0 per cent carries the coding quality warning in th...
- **REVIEW** `census2026_coding_procedures.pdf`: golden figure 0.90 appears: ...up with a score from 0 to 1. A suggestion scoring 0.90 or more becomes the production code (the automati...

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `OQ-4_occupation_output_quality_standard.docx`: 5 of 25 stump-paragraph terms appear (population, method, counts, operations, selection); read whether the document names the move
- **REVIEW** `census2026_followup_field_manual.pdf`: 3 of 25 stump-paragraph terms appear (operations, workload, closed); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Isolated reader (stage 4)

Four reads, each a general-purpose agent (Sonnet, medium effort) that saw only prompt.txt and the 17 unzipped files. In every read, questions 1 to 4 came back none and question 6 came back analytical (how the study's evidence reaches the write-ins still to code).

- Read 1 (first cut): two ask figures had two readings, also raised by the judge: hours "logged that month" (shift date or entry date) and households "enumerated at those calls". The prompt now asks for the hours each team spent on occupation coding that month and for the September calls that made no contact. The dictionary names the timesheet date as the shift start and nets corrections as negative lines.
- Read 2: the procedures said CODA closes on "the last working night of each month", but Thursday 29 October showed night coding. They now name the night of the month's last working day, and checks.py asserts that no night shift crosses a month end. The LFS distractor's CVs no longer fall smoothly with group size.
- Read 3: the autocoder's stamps were spread evenly from 01:00 to 05:00; they now follow a nightly first-in-first-out run stamped to the second. Every fork it checked in the data is settled by a shipped sentence or the records.
- Read 4 (the shipped cut, sha256 c0157a47): reproduced below. Its team figures at the time of coding match the golden on every team.

### Solver's-eye read (fourth read)

1. Decisive step: no sentence names it. OQ-4 s2.1 ("A person whose write-in has not yet been coded on the date of an assessment is part of the release population") plus census2026_processing_plan_nov2026.xlsx Decision sheet ("From Monday 16 November 2026 the autocoder accepts a suggestion scoring 0.80 or more as the production code. Write-ins already coded keep their codes.") and the coding procedures s8 (selection intervals 10/4 self-response, 2 follow-up) point at the work, but none says how to project the uncoded ~103k (mostly follow-up) write-ins. OQ-4 s3.3 ("each studied write-in stands for as many coded write-ins as its selection interval") tells you to weight. Nothing states the decisive step (projecting the still-to-code follow-up population under the new 0.80 rule, with the study's follow-up codes and the 0.80-0.90 band).
2. Ranks or scores the groups: none. lfs_2026q3_employment_by_occupation.csv and census2021_occupation_by_region.csv give employment counts only, no bias.
3. Written only to guide the solution: none. The processing plan is capacity-framed ("capacity only") and reads as an organisation's own record; it is the closest to a hint (the 0.80 decision), but plausible as context.
4. Reads as the answer: none. No group, bias figure or list appears. Mild nearest: the plan's "Of these, scoring under 0.80 / 0.90" shares and "Clerical queue at acceptance score 0.80".
5. Filed sentences fixing the main figure:
 - OQ-4 3.1: "the number of persons in the release population that the release codes to the group, less the number that the reference coding puts in the group, as a percentage of the number that the reference coding puts in the group." Literal: per sub-major group (first two digits), (release count - reference count)/reference count, person-write-in level.
 - OQ-4 2.1: population = persons in employment, occupation coded from a write-in, by close of field operations, including not-yet-coded write-ins; blanks (imputed) excluded. Literal: all 634,479 write-ins in the plan / receipt register, not just the 531,112 coded.
 - OQ-4 3.2/3.3: reference = study adjudicated code; each studied record weighted by selection_interval; both numerator counts estimated from the same studied write-ins.
 - OQ-4 4.1: warning if unrounded |bias| > 2.0%.
 Literal execution: weighted study counts, but the study covers only already-coded write-ins; the uncoded ones are in the population and the filing does not say what code the release will give them (the release code for them does not yet exist). So a literal reader must decide how to treat them; the 0.80 decision and "Write-ins already coded keep their codes" are the only sentences bearing on it.
6. Decides the main answer: an analytical choice (how to estimate the release-population bias when about 16% of write-ins, mostly follow-up with different code mix and a sampling interval of 2, are not yet coded and will be coded under a new 0.80 rule; the easy route weights the coded study only and files wrong). Nearest sentences: OQ-4 2.1 and the Decision sheet of census2026_processing_plan_nov2026.xlsx. Some risk it reads as rule application (2.1 plus 3.3 plus the decision are all stated) if the projection is considered fully dictated; I judge it analytical because the projection method is not filed.

### Realism tells
- Processing plan sheet "Position 13 Nov" figures are round-trip tidy (449793/184686) and the Capacity sheet reads like a worked calculation ("Clerical capacity a week 1705", "Weeks to clear at 0.80 5.4"), slightly tutorial.
- export_manifest.csv with identical extracted date (2026-11-13) for every file, and every owner/source named uniformly; very tidy for a real export.
- Staff ids and coder ids sequential-ish (OC101..OC210), timesheet notes few and clean (6 notes, e.g. "OCC overclaimed 07/10, corrected by team lead").
- Visit log: uniform 09:00 to 20:xx call times, visit_no blank exactly on the administrative closures; synced_at lag is regular. Quality study autocoder scores to 3dp, plausible.
- Documents (OQ-4, procedures, field manual) are short, uniformly numbered and structured, with single named owners; read somewhat template-like but not wrong.
- Person names (Timothy Taggart, Tracey Brien, Lesley Ahearne, Erica Phayre) are alliterative-ish/invented style.

### Forks
- "how many occupation write-ins it coded in October" (team). Reading A: coded_at local month = October (clerical path, coder_id). Reading B: team of the coder per coding_staff_register (current team) vs team at the time of coding per coding_staff_movements (transfers on 5, 12, 19, 27 Oct). Data differ: A-current team gives T1 3916, T2 3887, T3 4372, T4 4049, T5 3535; team-at-time gives T1 4160, T2 3746, T3 4206, T4 3112, T5 2680 (my approximation; coder-id-only moves assumed). Total 17,904 either way (all clerical, October local date). Not settled by a shipped sentence; the staff movements file ("effective_date: first day in the team joined") settles it by data if one reads "it coded" as the team at the time. Mild residual: team-5 night shift crossing midnight (coded_at hours 0 to 5 present); local date vs shift start date. Month-start/end edge: no coded_at in 31 Oct or 1 Nov early hours for clerical, so no change there. Also whether automatic path write-ins count (no team, so no).
- "hours it spent on occupation coding that month": OCC activity only vs including QRY (query desk, "Experienced coders staff the desk... book that time as QRY"); lines by work_date (shift start) vs entered_on; negative correction lines ("a team lead corrects a line with a further line of negative hours"); team attribution at transfer; team leads (SUP) excluded. Timesheets contain 6 correction lines (note text) and one line entered after 1 Nov; readings change the hours. The data dictionary (hours netted, work_date = date shift started) settles most; OCC-only is the literal reading of "occupation coding" against procedures' activity list.
- "follow-up calls enumerators made in September": visit_time local month vs synced_at month (6,099 calls sync in a different month); administrative closures (outcome 60, staff_id blank, 1,329 in Sept) are not calls by enumerators. Region totals differ: e.g. PA calls 20,113 by visit_time vs 20,569 by sync month; excluding staff-blank rows needed. Field manual 5.2 "Record every call on the tablet" and data dictionary "Local time of the call" settle it by visit_time.
- "calls that made no contact": outcome 31 only ("No contact, calling card left", manual 5.3/5.7) vs also 32 Refusal (contact made) or 40/50. Data differ: PA 8,245 (31) vs 8,618 (31+32); AV 4,247 vs 4,450. Manual 5.3 settles it: 31 is the only "No contact" code; refusal is a contact. Proxy (20) is not no-contact.
- "coding bias": signed percentage per OQ-4 3.1 (negative possible); warning is beyond plus or minus 2.0; "every group's bias in that release" unambiguous after 2.1 but dependent on uncoded treatment (see 5).
