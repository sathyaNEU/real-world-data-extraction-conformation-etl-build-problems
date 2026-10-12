# leak check, task180

**Verdict: REVIEW.** 16 files read, 39 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: asserted, catalogue, pfeilbrunn, record, completeness, scheme, lanzenried, decisive, method, reviewed, origin, window, earthquake, magnitude, complete, fourth, nothing, growth, ordinance, moorstetten, detection, sentence, counting, injection, federal

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `monitoring_ordinance_2026.pdf`: golden figure 0.6 appears: ...at it locates every earthquake of local magnitude 0.6 or more with an epicentre within 5 km of the open...
- **REVIEW** `tls_bulletin_2026Q3.pdf`: golden figure 120 appears: ...atalogue as at 8 October 2026. Amber is more than 120 in a quarter. Networks From 1 January 2027 the co...
- **REVIEW** `tls_scheme_2024.pdf`: golden figure 120 appears: ...Green: normal operation. 4.2 Amber: more than 120 earthquakes counted under section 3 in a calendar...
- **REVIEW** `tls_bulletin_2026Q3.pdf`: carries 7 of 10 distinctive words of the committed call: 'Pfeilbrunn will run over the traffic-light amber in the first and fourth quarters of 2027, at about 223 and 206 earthqua'
- **REVIEW** `tls_scheme_2024.pdf`: carries 8 of 10 distinctive words of the committed call: 'Pfeilbrunn will run over the traffic-light amber in the first and fourth quarters of 2027, at about 223 and 206 earthqua'

## 4 design-note vocabulary (REVIEW 6)
- **REVIEW** `datenabgabe_ampel_2026-10-12.md`: 12 of 25 stump-paragraph terms appear (catalogue, pfeilbrunn, record, scheme, lanzenried, reviewed); read whether the document names the move
- **REVIEW** `monitoring_ordinance_2026.pdf`: 8 of 25 stump-paragraph terms appear (completeness, scheme, earthquake, magnitude, complete, ordinance); read whether the document names the move
- **REVIEW** `operating_plans_2027.pdf`: 8 of 25 stump-paragraph terms appear (pfeilbrunn, scheme, lanzenried, complete, fourth, ordinance); read whether the document names the move
- **REVIEW** `tls_bulletin_2026Q3.pdf`: 9 of 25 stump-paragraph terms appear (catalogue, pfeilbrunn, scheme, lanzenried, reviewed, earthquake); read whether the document names the move
- **REVIEW** `tls_scheme_2024.pdf`: 10 of 25 stump-paragraph terms appear (catalogue, pfeilbrunn, record, scheme, lanzenried, reviewed); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: 'For each plant and each of the first three quarters of 2026 I also need, in tls_annex_2026.xlsx, its injected volume, the earthquakes of ML 1.0 or more within 5 km that our automatic system located, and the hours its net'

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read (pass 1, Sonnet, 2026-10-12)

Q1. none. Nearest pieces: scheme 7.2 ("each at the system's final automatic solution", the annex's reading), the
bulletin's "From 1 January 2027 the counts are made on the networks the 2026 ordinance requires", ordinance 3(1) (the
2027 networks locate every earthquake of ML 0.6 or more within 5 km), the plans note (each quarter at its 2026 volume,
the fourth at 2025's). Plan of attack: count ML 1.0 and over per plant and local quarter in the reviewed catalogue
(explosions out, distance to the open-hole segments), note the 2027 networks are complete to ML 0.6, fit the
magnitude-frequency relation (b-value, completeness) down to ML 0.6 and scale it to the 2027 volumes against 120; the
annex from the reports (MST-Th4a as MST-GT4), the origin table's final automatic solutions, and the gaps against the
inventory's channel epochs on the vertical channel.

Q2. none ranks the 2027 question; the bulletin's 2025 Q4 to 2026 Q3 counts are a baseline, all green.

Q3. none; the data office's cover note is complete but plausible.

Q4. none; "all five plants stayed green" is context, 0.6 is the law's design value.

Q5. Scheme 3.1 (ML 1.0 or more in the zone, local calendar quarters), 3.2 (the reviewed catalogue, explosions out),
2.1 (5 km of the open-hole section of any injection well, from the well register), 4.2 (more than 120), ordinance 3(1)
and 4 (counts on the 2027 networks), the plans note (2026 volumes, Q4 as 2025), scheme 7.2 (final automatic solution),
5.2 (vertical channel), 6.2 (reported volumes over the injection wells). Each executes to the golden's convention; none
fixes the forecast method.

REVIEW lines: all harmless (the 0.6 and 120 are the filed design value and amber line; the bulletin and scheme share the
call's words because they define the scheme; the notes, ordinance, plans, bulletin and scheme name plants and the
scheme's terms and none names the move; the prompt's annex sentence mirrors scheme 7.2).

Realism tells: the cover note is detailed; the well register's remark explains the MST-Th4a rename in a sentence (reads
as a planted join key); pandas reads the gap log's location codes "00" as 0 beside the inventory's "00" and "10"; the
bulletin table is neat; received dates fall on the 2nd to the 10th; an English unofficial translation beside German
titles; random event-id suffixes against regular origin ids; one sensor and logger model per epoch; the groundwater file
is plainly a neighbour's.

Repair (2026-10-12, in the stage 4 pass): the well register carries a former_designation column (MST-Th4a for MST-GT4,
MST-B3 for MST-GT3) in place of the explanatory remark; a data file, so leak.py re-runs and the reader does not. Kept:
the cover note (it carries the time zones and grains the conventions rest on), the location codes as the archive writes
them, the bulletin, the received dates (the reporting deadline is the 10th), the translation (labelled as such).
