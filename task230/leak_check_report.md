# leak check, task230

**Verdict: REVIEW.** 15 files read, 53 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: default, november, population, processing, sentence, counts, decision, carried, stream, client, decisive, register, workload, nothing, method, window, forecast, operations, asserted, closed, domain, coded-so-far, selection, acceptance, questionnaire

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `OQ-4_occupation_output_quality_standard.docx`: golden figure 3.2 appears: ...that the reference coding puts in the group. 3.2 The reference coding of a write-in is the code th...
- **REVIEW** `OQ-4_occupation_output_quality_standard.docx`: golden figure 2.0 appears: ...r group whose coding bias is beyond plus or minus 2.0 per cent carries the coding quality warning in th...
- **REVIEW** `census2026_coding_procedures.pdf`: golden figure 0.90 appears: ...up with a score from 0 to 1. A suggestion scoring 0.90 or more becomes the production code (the automati...

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `OQ-4_occupation_output_quality_standard.docx`: 5 of 25 stump-paragraph terms appear (population, counts, method, operations, selection); read whether the document names the move
- **REVIEW** `census2026_followup_field_manual.pdf`: 5 of 25 stump-paragraph terms appear (register, workload, operations, closed, questionnaire); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 40% of 196 prompts (cap 30%); deliverable set 'png+xlsx' at 24% of 196 prompts (cap 20%); reword at the role level, not the verb

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)


## Solver's-eye read (fourth read)

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

## Solver's-eye read (re-check, 2026-11-01)

Two isolated reads (general-purpose, Sonnet, medium) on fresh copies of prompt.txt and target/, 2026-11-01. Read 1 on the first re-check cut; read 2 on the final cut (procedures 4 trimmed after read 1's realism tell).

### Read 1 (first re-check cut)

Questions 2 and 4 none; question 1 and 6 named OQ-4 2.1 with the plan's 0.80 Decision (ruled as in read 2); question 3 the processing plan (capacity only, unchanged since ship). Realism tell: procedures 4 and manual 5.6 packed the timesheet, movement and tablet readings into crowded sentences that read as pre-answering the ask hazards; answered by trimming them to the two readings the records do not settle (the final cut). Every mechanical-sweep item ruled harmless.

### Read 2 (final cut)

Reader pass on leak-task230 (read only prompt.txt and target/; computed nothing)

1. Decisive step: OQ-4 clause 2.1: "A person whose write-in has not yet been coded on the date of an assessment is part of the release population." Together with the processing plan's Decision sheet ("From Monday 16 November 2026 the autocoder accepts a suggestion scoring 0.80 or more as the production code. Write-ins already coded keep their codes.") and procedures s3 ("CODA stores the autocoder's suggestion and score on every write-in, on either path"), the pack states the route. It states it as context, not as an instruction to the analyst. Nothing says "use the 0.80 rule for the uncoded".

2. Ranks or scores the candidates: none. No file lists groups with a bias or a warning flag. The study CSV is raw rows (per-write-in), and the LFS and 2021 files are context. The study's production_code and reference_code columns are inputs, not a ranking.

3. Exists only to help the analyst: none. coding_staff_register / coding_staff_movements and the enumeration_districts file are lookup inputs for the secondary asks. The OQ-4 standard (s3) and the procedures PDF are the organisation's own rules. Closest to a helper: census2026_processing_plan_nov2026.xlsx "Capacity" sheet, which is a ready-made rate (14.3 write-ins an hour) and a 0.80 under-score share, but its stated purpose is "capacity only". It is a decoy for the secondary ask and the main call, not a solver aid.

4. Figure or name that reads as the answer: none. No group is named as warned. The plan's "Still to code" 103,367 is context. The only prominent thresholds are +/-2.0 per cent (OQ-4 4.1) and 0.90 / 0.80.

5. Sentences fixing the computation:
- OQ-4 3.1: bias = (release-coded count less reference count) / reference count, as a percentage, per sub-major group. Literal result: signed relative difference, not an absolute difference or an error rate.
- OQ-4 2.1: include every person in employment with a coded-from-write-in occupation, including ones not yet coded at the assessment date. Exclude blank-occupation (imputed) persons.
- OQ-4 3.3: each studied write-in is weighted by its selection_interval, and both counts come from the same studied write-ins. Literal result: weighted estimate over the study sample, not a raw row count.
- OQ-4 4.1: the test is on the unrounded bias, beyond +/-2.0 (both directions). Literal result: a group at, say, a displayed 2.0 may or may not be flagged, and flagging must not use the rounded 1-dp value.
- Procedures s8 / s3: the interval depends on batch type and path (ONL/PAP 10 auto, 4 clerical; FUP 2 both), and the study covers both paths.
- Plan Decision: write-ins coded before 16 Nov keep their codes; later ones are auto at >=0.80. (Applied to the uncoded population this fixes their release code for auto-scoring ones.)

6. What decides the main answer: following a stated rule/definition (OQ-4 s2-s4, read together with the Decision sheet) plus catching the "not yet coded" population trap. The deciding sentence is OQ-4 2.1, with the plan's Decision sheet as the planted-looking twist (a rule change that affects what the not-yet-coded will be coded to). Not an analytical choice.

Mechanical-sweep items
- OQ-4 docx numbers (the warning clause 4.1 "2.0" and a clause number such as 2.0 / 3.x): harmless. The 2.0 is the published threshold itself, which the task needs the solver to be given, and the clause numbers are labels. Neither is a derived figure.
- census2026_coding_procedures.pdf autocoder number (0.90): harmless. It is the organisation's own acceptance score, a rule parameter, not a result. It is the stale threshold superseded by the plan's 0.80, which is part of the puzzle, not an answer.
- prompt.txt shell quota (question form 'which', png+xlsx deliverable): harmless to the pack (a format/shape quota only, not content). Nothing in the files depends on it. Both are cosmetic and no answer leaks.

Main-call forks
- For uncoded clerical-path write-ins, the filed material never says outright what the "release codes" them to. A solver might (a) apply the 0.80 autocoder rule to those scoring above and use some clerical code for others, or (b) use the 0.90 rule. Two defensible readings: apply the Nov-12 decision (0.80) or ignore it, because the release is on 30 March 2027 and the plan is "capacity only". The Decision sheet is dated after the study but is the only statement of the current rule, so (a) is probably the intended, but it is a real fork. For the uncoded clerical write-ins the code the release will have is not in the pack.
- "Beyond plus or minus 2.0 per cent": exact boundary treatment of rounded vs unrounded is spelled out (unrounded), so no fork.
- Reading "persons in employment enumerated by the close of field operations": receipt register vs. study scope; moderate ambiguity about whether study rows past 31 Oct are excluded.

Asks whose figure can be read two ways
- "Hours spent on occupation coding that month": OCC activity only, versus all coding hours (IND, QRY). Procedures s4 defines the activities, so OCC is the literal reading. The note/entered_on columns and a timesheet "dated by the day its shift began" rule (night shift across month end 31 Oct to 1 Nov) matter. Team attribution is via transfers (effective date), per s4.
- "No contact" calls: outcome 31 only, versus also unanswered visits with missing codes. Field manual s5.3 defines 31. "Follow-up calls made in September" depends on visit_time versus synced_at, duplicates, and region via the ED lookup, and caseload reassignments in September (5.8: "a case keeps its calls").
- Write-ins "coded in October": batch of coding date vs. load date; the extract's coded timestamp presumably decides.

Realism tells
- The processing plan "Capacity" sheet has computed derived rates with round numbers ("Clerical capacity a week 1705") that read as written for an analyst: ready-made 14.3/hour and 12 hours/week figures, and a "Position 13 Nov" sheet whose totals look tool-generated. They appear to be there as a tempting shortcut for the secondary ask.
- The 13 Nov dates of the plan are after "today" semantics in a pack that is supposedly as of 1 Nov (file mtime 13 Nov), which is consistent with the organisation's own record, so fine.
- The OQ-4 docx and PDFs are short, tidy and each section maps one-to-one to a step of the task; clause 3.3 ("both estimated from the same studied write-ins") reads written to steer the analyst. The study CSV carrying "reference_basis" AGREED/ADJUDICATED is realistic. Nothing reads as LLM chatter; the staff owners have invented-name styling, fine.

### Main-thread rulings

- Questions 1 and 6: OQ-4 2.1 and the plan's Decision are the filed WHAT and the readable rung R1; executed on the coded-so-far mix they file 35, 41 and 93 (judge pass 3), so the decisive step (the route carry) is named by no sentence. Harmless; Gate H analytical per the judge.
- Main-call fork 0.80 against 0.90: closed by the Decision sheet (from 16 November the autocoder accepts 0.80; coded write-ins keep their codes), SF12.
- Capacity sheet tidy rates: the processing plan's own capacity answer, unchanged since ship and read at ship; harmless.
- Sweep 4 lines: ruled in the design note (pre-ship check 10).
