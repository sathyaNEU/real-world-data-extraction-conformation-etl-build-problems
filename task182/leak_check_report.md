# leak check, task182

**Verdict: REVIEW.** 13 files read, 43 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: residual, record, measured, minutes, decisive, background, quantity, clause, device, window, subtraction, forced, method, architecture, decline, process, in-house, rainfall, reader, nothing, baseline, change, exactly, comparison, population

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `noise_management_plan.pdf`: carries 3 of 5 distinctive words of the committed call: 'The October acoustic treatment slot should cover NSL04, NSL11, NSL07, NSL02 and NSL13.'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `noise_management_plan.pdf`: 5 of 25 stump-paragraph terms appear (residual, record, measured, minutes, process); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `calibration_records_2026.csv`: 6 ISO dates after 2026-10-16, e.g. 2026-11-26, 2027-01-22, 2027-02-18, 2027-03-11, 2027-04-07

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


---

# ARCHITECTURE 2 (archived evidence)

Everything above and below ran on architecture 2's pack, tree digest `ab3198a15c906f7b`, cut 2026-10-17
and removed when the build was re-rooted at architecture 3 the same day. It does not describe the shipped
files of this task folder now. It is kept so the folder shows why architecture 2 died.

## Solver's-eye read

One isolated reader at medium effort, run 2026-10-17 on the cut pack, seeing only `prompt.txt` and
`target/`. **It landed the call and both device asks**, which is what spent the architecture.

**Verdict on each REVIEW line, from the reader's own answers.**

| REVIEW line | Verdict | The reader's own words |
|---|---|---|
| sweep 3, the plan carries three of five distinctive words of the call | harmless | Question 4: "Reads as the answer rather than context: none (no figure or name is presented as the result)." No shipped file carried a level per position. |
| sweep 4, the plan carries five of the stump paragraph's terms | **fix, and the finding that spent the architecture** | Question 1: "no single sentence names it. The nearest is noise_management_plan.pdf 3.1 ... The plan never says how the residual is to be obtained". The document did not name the move, so the sweep was answered; but question 6 shows the pack supplied the move in one step anyway, which is a design finding, not a vocabulary one. |
| sweep 9, six dates after the as-of in the calibration file | harmless | Not raised by the reader at all: forward verification due dates are a real instrument record, `reduce-house-fixes` H16. |

**Question 6, the answer that decided the re-root.** "An analytical choice. Plant-off residual must be
estimated per position (nothing says how); the only plant-off data are the 2-hour weekly MCC stops in
`plant_equipment_events_2026.csv` (all blowers and CHP stopped, early morning Tuesdays, e.g. '2026-09-01
04:45,BL-01,STOP,HD,weekly MCC inspection and belt check'), cross-checked against `scada_15min_2026.csv`
zeros." A decisive step that the filed clause demands and the data supplies in one move, labelled in the
log's own words, is readable, and a readable decisive rung is dead.

**What it landed.** The five, NSL04, NSL11, NSL07, NSL02 and NSL13, at 53.0, 49.9, 47.8, 47.3 and 46.0,
with NSL06 sixth at 44.7 about 1.3 dB behind; all fourteen levels; the tone at 400 Hz with the six
positions; the A2 air figures by the aeration header plus BL-03 over the 07:00 to 19:00 counter
differences; and the A3 rule, "absent rows plus rows that repeat the previous row exactly with plant
running", with every per-position and per-week figure matching the goldens, week 4 at 687.2, 92 and 86
included. Its own confidence was about 70 per cent on the five and the sixth and about 75 per cent on the
plant figures. So the ask layer's measured pair ceiling of 37.3 was not evidence of anything: a pair
ceiling cannot validate the ladder it assumes.

**The three realism findings, which are in scope of the re-root because they would survive into the new
architecture.**

1. **Tutoring sentences in the plan.** The reader named plan 3.1's "Levels are combined and subtracted in
   energy, not in decibels" and plan 5.1's "A spell the historian did not record leaves those two
   readings as they stand" as "definitional tutoring sentences, unusual in a site plan", and plan 5.2's
   centrifuge-run definition as "a rule written to resolve a counting convention" for a question the
   prompt never asks. Architecture 3 takes them out or rewords them in the standard's own register.
2. **`survey_notes.md` itemising defects.** "'What went wrong': itemises every defect (card read error,
   logger reset, two dropped channels, radio link) and ends 'All of it is on the deployment record.'; a
   technician's notes enumerating the data traps. Also 'Also in the folder: The complaints register ...
   Neither was collected for this survey.' names the distractors." Architecture 3's notes stop itemising
   defects and stop pointing at what was not collected.
3. **The complaints register's cardinality.** "complaint_ref repeats per contact (C01 five times) while
   the header says 'One row per contact'". Architecture 3's register either honours one row per contact
   or explains the repeat in its own words.

**Also noted by the reader, carried forward:** the positions sheet anticipating a non-issue about mic
height, the export manifest's weather row carrying a unit-change warning "more explanatory than an
extract log would be", and the complaint texts hinting at hum, whine and drone when the data's tone is at
400 Hz.

**The reader's answers in full, as filed.**

# Reader answers, task 182 pack (worked from the 13 files only)

1. Decisive step: no single sentence names it. The nearest is noise_management_plan.pdf 3.1: "The specific sound level of the plant at a position is the position's measured sound level over the assessment period, less the residual sound, both in dB LAeq." and 7.1 "taken in order of the specific sound level at the position, highest first". The plan never says how the residual is to be obtained; nothing filed says to use the plant-stop windows (equipment log) for it. Otherwise: none.

2. Ranks/scores the candidates on the question: none. The nearest rank-like file is complaints_register_2026.xlsx (rows per dwelling; DW-107/NSL06 has most contacts, 5), but 6.1 says "A complaint is a record of what a neighbour heard and is not a measurement." No file carries a level per position.

3. Exists only to help the analyst: none as a stand-alone helper. export_manifest.csv (units/time-zone notes, e.g. weather wind unit change and "stamps in UTC") and survey_notes.md come nearest. calibration_records_2026.csv is context for the field checks.

4. Reads as the answer rather than context: none (no figure or name is presented as the result). The raw-loudest position NSL04 is just the closest dwelling (98 m).

5. Literal sentences fixing the main figure:
 - 3.1 (above) with 3.2 "The assessment period is 07:00 to 19:00 on weekdays, in local time."
 - 4.1 "Where that deviation is more than 0.3 dB away from zero, every level the deployment recorded is corrected by taking the deviation off it."
 - 4.2 "A minute is not valid where the met mast's record for the ten minutes the minute falls in counted rain on the gauge or shows wind above 5 m a second, or where the meter recorded no measurement for that minute."
 - 5.1 for weekly plant figures: "...the counter reading stamped at 00:00 on the Monday the week begins, taken from the reading stamped at 00:00 on the Monday after it..."
 Literal result: measured level (valid minutes, weekdays 07-19 local, corrected) NSL04 53.2, NSL11 50.1, NSL07 48.1, NSL02 47.4, NSL06 46.6, NSL13 46.2 ... but this is not the specific level; literally, 3.1 needs a residual that is never defined, so the literal result of the quoted text alone is only the measured level above (raw ranking would pick NSL06 fifth, NSL13 sixth).

6. What decides the main answer: an analytical choice. Plant-off residual must be estimated per position (nothing says how); the only plant-off data are the 2-hour weekly MCC stops in plant_equipment_events_2026.csv (all blowers and CHP stopped, early morning Tuesdays, e.g. "2026-09-01 04:45,BL-01,STOP,HD,weekly MCC inspection and belt check"), cross-checked against scada_15min_2026.csv zeros. Subtracting that residual in energy turns raw 5th/6th (NSL06 46.6, NSL13 46.2) round: NSL13 46.0, NSL06 44.6-44.7. Supporting but secondary: reading rules correctly (UTC minute data vs local-time deployment table and local assessment period; wind m/s before 2026-09-20 and km/h from 00:00 that day per export_manifest.csv; -120 dB no-measurement sentinel rows; 120 duplicated rows from the repeated download for NSL09; calibration minutes; per-deployment deviation correction).

## My answer as a solver
Specific sound levels (dB LAeq, energy subtraction, residual = energy mean of valid minutes inside the six plant-stop windows pooled for each position's two deployments, 3 min trim gives within 0.1 dB):
NSL04 53.0, NSL11 49.9, NSL07 47.8, NSL02 47.3, NSL13 46.0 | NSL06 44.7 (44.6 trimmed) | NSL09 44.0, NSL01 43.9, NSL03 43.6, NSL12 43.3, NSL14 42.0, NSL08 41.4, NSL05 38.7, NSL10 37.4.
Five dwellings: NSL04 (DW-101), NSL11 (DW-104), NSL07 (DW-110), NSL02 (DW-103), NSL13 (DW-105). Sixth: NSL06 (DW-107), short by about 1.3 dB (1.3 to 1.4 depending on trim).
Tone: 400 Hz one-third-octave band, excess over neighbours >= 5 dB at NSL02 (12.6), NSL04 (15.7), NSL07 (11.2), NSL09 (9.4), NSL11 (13.0), NSL03 (6.6). Not at NSL01 (3.5), NSL06 (1.7), NSL12 (3.1), NSL13 (2.5). NSL05, 08, 10, 14 have no band data (those meters lack the module), NSL13 has only one deployment with it.
Plant figures per position (air in knm3 = header counter + BL-03 counter differences 07:00 to 19:00 summed over the 10 weekdays; no-own-reading quarter hours = absent rows plus rows that repeat the previous row exactly with plant running; longest run):
NSL01 520.5/20/14, NSL02 520.5/20/14, NSL03 506.3/27/14, NSL04 520.5/20/14, NSL05 520.5/20/14, NSL06 498.0/24/13, NSL07 498.0/24/13, NSL08 498.0/24/13, NSL09 505.7/27/16, NSL10 505.7/27/16, NSL11 511.0/24/16, NSL12 511.0/24/16, NSL13 503.3/21/13, NSL14 517.5/14/8.
Six weeks (clause 5.1, Monday 00:00 to Monday 00:00; air knm3 / missing quarter hours / longest run): wk1 689.2/20/14, wk2 675.9/16/11, wk3 684.7/12/8, wk4 687.2/92/86 (the Friday evening to Saturday afternoon spell), wk5 653.8/18/13, wk6 674.9/21/16. If the weeks are meant over assessment hours only: 260.9/14/14, 252.6/11/11, 257.9/8/8, 259.6/6/6, 245.4/13/13, 253.1/16/16.
Confidence: top four and the fifth/sixth split moderate to fairly good (about 70 percent); the split relies on the residual method, and a floor-only residual (excluding passing-vehicle events) would put NSL06 ahead of NSL13. Plant figures about 75 percent (ambiguities: air in the stale rows, quarter-hour stamp convention (no effect found), whole-week versus assessment-hours weeks, whether BL-03 is counted).
Route: parsed everything; deployments to UTC (-1 h); calibration deviations; sentinel/duplicate removal; weather validity with unit fix; assessment filter; found residual from equipment stops; third-octave test at 400 Hz; SCADA counters, gap and stale-row detection.

## Where the pack reads written for a task rather than produced by an organisation
- noise_management_plan.pdf 5.2: "A centrifuge run is one start of a centrifuge in the equipment log and the first stop the log records for the same machine after it. A start the log does not stop before that machine starts again is not a run. A week's runs are the runs that start in that week." The request asks nothing about centrifuge runs, and the sentence reads like a rule written to resolve a counting convention.
- noise_management_plan.pdf 5.1 "A spell the historian did not record leaves those two readings as they stand." and 3.1 "Levels are combined and subtracted in energy, not in decibels." are definitional tutoring sentences, unusual in a site plan.
- noise_management_plan.pdf 7.1 "The number of dwellings the slot covers is set when the slot is ordered." (a setup for the five in the prompt) and the header "Parts 8 to 10 ... are not reproduced in this extract."
- survey_notes.md "What went wrong": itemises every defect (card read error, logger reset, two dropped channels, radio link) and ends "All of it is on the deployment record."; a technician's notes enumerating the data traps. Also "Also in the folder: The complaints register ... Neither was collected for this survey." names the distractors.
- complaints_register_2026.xlsx: complaint_ref repeats per contact (C01 five times) while the header says "One row per contact"; the complaint text hints at hum/whine/drone tones, none of which match the 400 Hz band the data shows.
- monitoring_positions.xlsx row 3 note: "Mic height is the height set for the position; a deployment that stood at another height says so in the deployment record." anticipates a non-issue.
- export_manifest.csv weather row carries the unit-change warning inside the "contents" cell, more explanatory than an extract log would be.
