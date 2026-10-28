# leak check, task236

**Verdict: LEAK.** 13 files read, 24 golden figures and 7 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: positivity, protocol, sentinel, network, infections, tested, laboratory, notifications, quality, influenza-like-illness, consultations, register, decisive, default, ascertainment, cut-off, practices, population, preliminary, states, reports, domain, method, postcode, consultation

## 1 file names (LEAK 2, REVIEW 1)
- **LEAK** `DATA_DICTIONARY.md`: a file whose name says it describes the data (DATA_DICTIONARY): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)
- **LEAK** `README.md`: a file whose name says it describes the data (README): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)
- **REVIEW** `testing_change_register_2027.xlsx`: a sheet named 'Notes': confirm it is the organisation's own notes and does not describe the data's columns or files

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `sentinel_gp_network_protocol_SGP-2027.pdf`: carries 19 of 24 distinctive words of the committed call: 'Flag the notified influenza series of Far North, Metropolitan South, Metropolitan West and South Coast from the report w'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `DATA_DICTIONARY.md`: 13 of 25 stump-paragraph terms appear (protocol, sentinel, network, tested, laboratory, consultations); read whether the document names the move
- **REVIEW** `README.md`: 9 of 25 stump-paragraph terms appear (protocol, sentinel, network, laboratory, quality, register); read whether the document names the move
- **REVIEW** `influenza_report_data_quality_protocol_CDB-FLU-03.pdf`: 12 of 25 stump-paragraph terms appear (protocol, sentinel, network, infections, tested, laboratory); read whether the document names the move
- **REVIEW** `sentinel_gp_network_protocol_SGP-2027.pdf`: 10 of 25 stump-paragraph terms appear (positivity, protocol, sentinel, network, tested, laboratory); read whether the document names the move

## 6 ranking artifacts (REVIEW 1, INFO 2)
- **REVIEW** `testing_change_register_2027.xlsx`: names 7 of 7 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `postcode_health_region_concordance.csv`: names 7 of 7 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `sentinel_gp_network_protocol_SGP-2027.pdf`: names 7 of 7 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Reader pass 1 (the full pack, before the fix pass):
1. none: no sentence names how to estimate a region's infections; CDB-FLU-03 s.4 gives the quantity, not the route.
2. none: the register lists the changes with no effect sizes.
3. the two distractors (vaccine doses, laboratory turnaround), the dictionary and the readme: ordinary furniture.
4. none: no figure or name reads as the answer.
5. s.2 and s.4 execute to the golden's quantities (14-day cases anchored on the first positive, collection week, region
   under the concordance in force, the requesting service's postcode for blank and 0000, the Monday 09:00 cut-off as
   23:00 UTC Sunday, week 14 onward, ERP 30 June 2026, four weeks against four); open choices: the infection estimator
   (the analysis) and "a quarter" as relative or absolute (fixed: s.4 now measures it against the level before the
   change).
6. (a) an analytical choice.
Realism: the register repeated one wording across regions (fixed), point-of-care codes overlapped across regions
(fixed); the services list does carry STH and the point-of-care codes (a misread). Every REVIEW line harmless.

Reader pass 2 (the reworded protocol and register): 1 none; 2 none; 3 the readme and dictionary, and the sentinel
protocol's clinical ILI definition reads partly as a pointer (kept: every sentinel protocol states its definition, and
it names no comparison with notified cases); 4 none, though the merger entry's "collection centres and courier runs
unchanged" came closest to a verdict (fixed: the clause is cut); 5 "a quarter of its level before the change" is now
clearly relative, no absolute reading left; 6 (a) an analytical choice. The register reads as operational, not
templated.

Reader pass 3 (the register after the cut): 1 none; 2 none; 3 none; realism good (specific, uneven, operational).

Reader pass 4 (the rubric reship, 2026-10-28; target.zip 5ef00068, a fresh copy of the pack and the prompt only):
1. CDB-FLU-03 s.4's flag rule (the estimand: the share of infections notified, four weeks against four, a quarter
   either way); its Q6 confirms no file says how a region's infections are estimated, so the route is not named.
2. none: the register lists each change with its date and scores nothing.
3. the dictionary and the readme (orientation; they name files and fields and state no outcome).
4. none.
5. s.3 (ERP at 30 June 2026 of the postcodes under the concordance in force) and s.2's Monday 09:00 cut-off: both
   execute to the golden's quantities.
6. an analytical choice: turning notified cases and the sentinel figures into infections is left open.
7 (the asks): nothing states or narrates that two gateway keys can be one person or one key two people (the
   dictionary's patient_key line says only that the key is the same for every service), and nothing beyond s.2 says
   which result's postcode places a case.
8 (the asks): no marker column, batch stamp, code or comment singles out rows of the gateway results.
REVIEW lines: the dictionary and readme, the register's Notes sheet, the sentinel protocol's shared vocabulary and the
register's regions beside dates all harmless. Realism: the protocol PDFs carry the author as producer (house fix H1's
stamp, as on every pass); otherwise departmental.
leak.py at the reship: LEAK on DATA_DICTIONARY.md and README.md under the describing-file rule added on 2026-10-27,
after this build shipped; both shipped in the pack the portal judged, the dictionary carries conventions the call and
its critical components read (local time at UTC+10, 0000 as an unrecorded address, the report status), and a rubric
repair leaves the documents the call reads as they are. Left as shipped, for the author's call.
