# leak check, task450

**Verdict: REVIEW.** 12 files read, 98 golden figures and 65 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: shared, conversion, screen, change, cohort, rejected, cohorts, method, design, golden, decisive, difficulty, passing, student, full-academic-year, scores, curriculum, linking, system, tested, groups, report, reporting, designates, points

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `campus_designation_rules_2026-27.pdf`: golden figure 300 appears: ...ich the district set on its 2025 grade-5 form, is 300 or above. Results from later forms are reported o...
- **REVIEW** `dma_technical_report_2025_excerpt.pdf`: golden figure 300 appears: ...chose a linear scale so that the standard sits at 300 and each raw point on the 2025 form is worth six...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `campus_designation_rules_2026-27.pdf`: 6 of 25 stump-paragraph terms appear (design, student, full-academic-year, tested, report, reporting); read whether the document names the move
- **REVIEW** `dma_technical_report_2025_excerpt.pdf`: 6 of 25 stump-paragraph terms appear (conversion, student, scores, report, reporting, points); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: "Name them in intervention_schools_2027.docx with the share each was designated on, charted against the line, and put every rated campus's share with the counts behind it in grade5_math_results_2026.xlsx, along with, for "

## 6 ranking artifacts (REVIEW 1, INFO 1)
- **REVIEW** `campus_directory_2026-27.xlsx`: names 65 of 65 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `grade5_enrollment_projection_2026-27.csv`: names 65 of 65 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Two isolated reader passes (general-purpose, Sonnet, medium), each on fresh copies of prompt.txt and target/ from target.zip.

Rulings: pass 1 found no decisive-step sentence, no ranking or helper file and no answer figure, and on Q5 a main-call fork (rule 2's "Results from later forms are reported on the same scale" read as the 2025 conversion on the 2026 raw scores, 30 campuses), closed by the technical report's scope sentence (SF13) in one generator pass with its realism notes (campus numbers, opening years, Vereda's spring 2025 rows). Pass 2, on the fixed pack: Q1 to Q4 none; Q5 the literal reader cannot apply the 2025 conversion to the 2026 form and is left with linking through the shared items, which the records force (every common-item method gives 25, asserted); Q6 an analytical choice. Sweep lines: all harmless (the standard of 300 is the filed WHAT; campus names beside campus numbers, opening years and projected enrollment rank nothing).

### Pass 1 (on the first cut)

# Reader report, task450 r1

## 1. Sentence or file that tells the decisive step
None states it. Closest: campus_designation_rules_2026-27.pdf item 2, "a student's scale score on the District Mathematics Assessment's reporting scale, which the district set on its 2025 grade-5 form, is 300 or above. Results from later forms are reported on the same scale." It says the scale is shared but never says the 2026 form must be linked or equated to it. dma_technical_report_2025_excerpt.pdf Table 4 and 4.2 ("lies at a raw score of 26.5") lie on the easy path (raw 27 and up on the 2026 form). The item bank's two "Position" columns show 25 items common to both forms, but nothing labels them as anchors.

## 2. File that ranks or scores the campuses
None. No file holds a campus rate, a rank or a designation. The enrollment projection and the professional learning hours files give campus-level context only (they look like distractors).

## 3. File that exists only to help the analyst
None. data_dictionary.xlsx is ordinary field documentation. dma_key_correction_2026-05-19.pdf is a governing notice (item M545945 keyed C, not D). It is a required input and works as a rule to apply, not a hint.

## 4. Figure or name that reads as the answer
None. The only thresholds are 300 (scale), 40 percent, 10 students and the 31 Oct 2025 and 20 Apr 2026 dates, all filed rules. The "raw 26.5" in tech report 4.2 reads as the cut score to use but is context for the 2025 form.

## 5. Filed sentences that fix the main figure, and what they yield when executed literally
- Rules 2: scale score 300 or above, "Results from later forms are reported on the same scale." Read literally and in the shortest way, this means the 2026 raw score converts with the 2025 formula 141 + 6 x raw, so raw 27 or more meets the standard. Computed with the key correction (M545945 = C), merges applied, and full-academic-year students per rules 3 and 5: 54 campuses rated, 30 under 40 percent. Examples: 127 at 9.1 percent (5 of 55), 154 at 9.8 percent (13 of 132), 103 at 18.2 percent, down to 102 at 37.0 percent (51 of 138).
- Rules 3: full academic year means enrolled 31 Oct 2025 and every day through 20 Apr 2026 at one campus only. I got about 5,824 students, and 6,341 test takers (all map to a SIS id).
- Rules 5: campus 112 (Delgadillo) students count with 148 (Tobar). The directory says so.
- Rules 4, 6 and 7: rate = met / tested among full-academic-year students; fewer than 10 tested means unrated; rate under 40 percent is designated.
- Key notice: "Score the item with key C for every 2026 test."
- The prompt does not file the linking method. If the analyst equates the 2026 form to the 2025 scale through the 25 common items (my Tucker linear approximation, equivalent cut about raw 25 on the 2026 form instead of 27), the result is 54 rated and only about 15 under 40 percent (154 at 13.6 percent, 127 at 18.2 percent, 103 at 25.0 percent ... 151 at 37.6 percent). The literal text gives 30 campuses and the equated route about 15, so the answer depends on the linking choice.
- Determinism risk: nothing filed says to equate, or which method (Tucker, mean-sigma, IRT) to use. Campuses near 40 percent (for example 133, 151, 148) may flip between linking methods. A literal reader would take raw 27 and produce 30 campuses.

## 6. What decides the main answer
An analytical choice: whether the 2026 form's raw scores are put on the 2025 scale by equating through the 25 shared items (the 2026 form's new items are easier or harder than the old ones; the shared items alone show the 2026 students about 0.5 raw point better, yet total raw scores are about 0.8 lower). The decision comes from the data, not from a quoted sentence. The only nudge is the sentence "Results from later forms are reported on the same scale" plus the item bank position columns. The key correction, the full-academic-year rule, the merges, the closed campus and the 10-student minimum are real mess and rule application that complicate the work, but they do not decide the call. Risk: the literal text points to the shortcut and the equating is unfiled, so the "right" answer is the author's reading, not the literal reading.

## Realism tells
- campus_designation_rules_2026-27.pdf: rule 7 line starts with a stray leading space (" 7  Designation"), which suggests a generated layout. Page number "1" sits as its own line after the header on each PDF. All three PDFs share the same "Coraza Independent School District  |" header style.
- campus_directory_2026-27.xlsx: all 56 campuses are named "... Elementary", with plant-and-Spanish-surname names (Agarita Bend, Cenizo Flat, Huisachito). It reads as a name list built by pattern. All campuses are 'Open' except one closed. Campus numbers are text strings 101..156 in strict alphabetical name order, which a real district would not have (numbers are normally assigned by opening date or by sorting out secondary campuses). 'Opened' values do not follow numbering.
- dma_item_bank: item IDs M5xxxxx are random; every item is "Multiple choice", 1 point; sort order by ID. The item bank needs the 2026 correction but the notice says the bank "still shows the key as entered" (consistent, good).
- Tech report excerpt: Table 4 is a perfect linear 141 + 6 x raw with no rounding and a clean 26.5 cut, which looks synthetic (real scale conversions are non-linear). Only "sections 2 to 4 and Table 4" with no mention of linking or equating, where a real technical report would describe it.
- grade5_math_responses_2026.csv: submitted_at is "district local time" with exactly 50 items for all 6,341 takers, with no partial sessions. Real platform logs have missing sessions or gaps. 16.7 MB long format is plausible.
- grade5_math_responses_2025.csv: the report says given 21 April to 2 May 2025; I did not check TEST_DATE bounds fully (first rows begin 04/23). 'SCHOOL_NAME' abbreviations ("URSULINE AVE EL") are a nice touch.
- sis_grade5_enrollment: grade column all "05" strings, and exit date for open enrollments is 2026-05-28, which a real SIS would show as the last day. Dates 2025-08-13 repeated for most students.
- dma_registrations: registered_on 23 March 2026 for nearly all rows, tidy.
- sis_student_id_merges: merge date 2026-08-10, all "Duplicate person record", all on the same date (a batch), which is plausible but uniform. The merge is after the testing window and thus has to be applied backwards, fine.
- Rules approved 18 Aug 2026 (the results being "now in") is consistent with the setting; key notice 19 May 2026.

### Pass 2 (on the fixed pack)

# Leak read, task450 r2 (solver's-eye)

## 1. Sentence or file that tells the decisive step
None states it. Closest are context sentences. campus_designation_rules_2026-27.pdf s.2: "scale score on the District Mathematics Assessment's reporting scale, which the district set on its 2025 grade-5 form, is 300 or above. Results from later forms are reported on the same scale." This says 2026 results sit on the 2025 scale but gives no method. dma_technical_report_2025_excerpt.pdf 4.1: "The conversion applies to raw scores on the 2025 form only." This warns against the shortcut but does not say what to do instead. The item bank's two position columns show that 25 items are common to both forms. Nothing names or describes linking or equating.

## 2. File that ranks or scores campuses
None. All campus-level files are context: campus_directory (community, status), grade5_enrollment_projection, math_professional_learning_hours, and the SIS and registration extracts. No shipped file holds a rate, a score or a campus ordering.

## 3. File that exists only to help the analyst
None. data_dictionary.xlsx is ordinary field documentation. dma_key_correction_2026-05-19.pdf is a real-looking operational notice, not a hint. The projection and professional-learning files read as distractors.

## 4. Figure or name reading as the answer
None. The rule "under 40 per cent" is a stated threshold, not a result. Table 4 (141 + 6 x raw) and "raw score of 26.5" are the 2025 form's facts, not the answer.

## 5. Literal-execution sentences and yields
- Rules s.2, "A student meets the mathematics standard when the student's scale score ... is 300 or above."
- Rules s.2, "Results from later forms are reported on the same scale."
- Tech report 4.1, "On that form a raw score converts to a scale score as 141 + 6 x raw score, reported as a whole number (Table 4) ... The conversion applies to raw scores on the 2025 form only."
- Tech report 4.2, "On the 2025 form it lies at a raw score of 26.5."
- Key correction: "Score the item with key C for every 2026 test" (M545945, position 38).
- Rules s.3 (full academic year: enrolled 31 Oct 2025 through 20 Apr 2026, no other campus), s.4 (rate over FAY students who tested), s.5 (closed campus 106 counts with Tobar 143), s.6 (fewer than 10 FAY tested is not rated), s.7 (rated and under 40 per cent is designated).

A strictly literal reader cannot obtain a 2026 scale score from the files. No sentence supplies a 2026 conversion table, an equating rule or a 2026 cut raw score. The only formula and table are labelled 2025-form-only, so applying 141 + 6 x raw to 2026 raw scores contradicts 4.1 and no filed sentence permits it. A literal reader is left with "later forms are reported on the same scale" and no stated way to do it. The only data route is to link the forms through the 25 common items (item bank columns "Position, 2025 form" and "Position, 2026 form" both filled) and find the 2026 raw cut that matches 300. This route is not written anywhere. It is what an analyst must supply. The method is not filed, and that is the deliberate gap. Whether that counts as determinate is a determinism question. Executed literally, the 2026 standard is not computable from filed text alone.

Quick check from the files: the 2026 file has 6,341 testers, each with 50 rows. The common-item mean correct is 0.499 in 2025 and 0.503 in 2026, so the cohorts are similar on anchors. The 2026 raw mean is 24.05 against 24.97 in 2025, so the new items are harder. Naive raw >= 27 (the 2025 cut) gives 40.8 per cent meeting district-wide in 2026 against 44.8 per cent in 2025. An equated cut would sit lower, so the naive route files a wrong answer. After the key fix the naive and equated numbers differ for borderline campuses, which is where the wrong designations come from. I did not compute campus rates.

## 6. What decides the main answer
An analytical choice. The decisive step is placing the 2026 form on the 2025 scale through the 25 shared items (anchor linking, with the cohort-equivalence evidence from the anchor means), then the cut. The sentence that sets it up is rules s.2, "Results from later forms are reported on the same scale", together with tech report 4.1, "applies to raw scores on the 2025 form only". Using 141 + 6 x raw or raw 27 on the 2026 form is the easy route and gives a wrong answer. The key correction, the full-academic-year test, the merges and the closed-campus roll-up are Layer 1 or rule application, and they do not decide the call alone. Caveat: the files carry no sentence on how to link, so choosing among linking methods (mean shift, linear, equipercentile) is open, and a judge will ask whether the data separate them. The anchors are well matched in difficulty, so they probably do.

## Realism tells
- campus_directory_2026-27.xlsx: the Campus number column holds text strings ('101'), and the campus list runs 101 to 156 in a clean sequence. Real directories rarely have gap-free numbering. Campus 137 "Vereda" opened 2025 and 124 "Farias" 2018, which is plausible. Campus names ("Hackberry Slough", "Kidneywood Knoll", "Tepeguaje Draw", "Mustang Grape") skew toward a Texas-brush-plant naming pattern, which reads as generated.
- campus_designation_rules pdf, line "6 Rated campuses." has a stray leading space before "7 Designation." in the extraction, a minor layout slip. The numbered-paragraph style with headings in the same line is plausible for a board document. The rules have no board agenda item or resolution number.
- Rules s.2 and s.6 are too cleanly spelled out for a board document, and "Katherine Padilla, President" plus "Susan Bird, Executive Director" are fine, but the rules say nothing about the alternate assessment or students with no 2026 form.
- sis_grade5_enrollment_2025-26.csv: the grade column is "05" and exit_date for open enrollments is the last day of school, 2026-05-28. Entry date 2025-08-13 for most rows is uniform, which looks synthetic. A real SIS would carry varied entry dates and withdrawal reason codes beyond three.
- grade5_math_responses_2025.csv: SCHOOL_NAME is truncated platform style ("PINTO MESA EL", "OLD MILL RD EL") and the first rows show SCHOOL_CODE 142 against "PINTO MESA EL" (campus 111 in the directory). That is the intended crosswalk mess and reads as realistic. TEST_ID "D25-192352" is plausible.
- grade5_math_responses_2026.csv: long format with exactly 50 rows for every one of 6,341 takers, so there are no partial or abandoned sessions, and submission times run from 08:32 to 11:31 only. Real platform logs show retakes, partial records and irregular times. Dates stay within the 20 Apr to 1 May window, which is clean.
- dma_item_bank: every item is "Multiple choice", 1 point, with sequential 'First used' only 2025 or 2026. Item IDs M52xxxx to M54xxxx are plausible. All 25 new 2026 items sit at even positions, and the 25 shared items are not clustered by position, which suggests random assignment.
- dma_technical_report_2025_excerpt.pdf: the "chose a linear scale so that the standard sits at 300" and "raw 26.5" line is neat enough to look designed. Real technical reports would carry reliability, SEM and test information, and a district rarely publishes a bare linear raw-to-scale table.
- data_dictionary.xlsx: the dictionary is complete for each file with no gaps. The 2025 file's "I01 to I50" row is the one compressed row.
- math_professional_learning_hours_2025-26.csv: zeros for October for campus 101 (0.0 hours, 0 sessions) with constant teacher counts per month suggest synthetic regularity. It is clearly a distractor.

# Leak read, task450 r3 (solver's-eye, hardening loop 1: the shared items screened before the link)

## 1. Sentence or file that tells you the decisive step
None names it. The nearest are the technical report 4.1 ("The conversion applies to raw scores on the 2025 form only.") and the rules' section 2 ("Results from later forms are reported on the same scale."): together they say the 2026 form needs placing on the 2025 scale, never how. The item bank's two position columns show which items both forms carry: raw data, not an instruction. Nothing mentions a screen, an item's change between the years or the curriculum.

## 2. File that already ranks or scores the campuses
None. The directory, the professional learning hours and the enrollment projection carry campus-level numbers, none a rate or rank on the question.

## 3. File that exists only to help the analyst
None. The data dictionary is the weakest case and is plausible for a district; the id merges and the key correction notice read as operational records; the two distractors read as real records.

## 4. Figure or name that reads as the answer
None. 300 is the standard; the technical report's 26.5 is a 2025-form fact (a lure for the wrong path, not the answer); no campus is named or flagged.

## 5. Filed sentences that fix the computation, with literal result
Rules section 2 (300 or above on the scale set on the 2025 form; later forms on the same scale): no 2026 conversion is filed, so it leaves the 2026 cut open. Technical report 4.1: the 141 + 6 x raw conversion must not be applied to 2026 raw scores. Rules 3 to 7 (full academic year, the rate, the closed campus with its receiving campus, ten or more tested, under 40 per cent) and the key notice fix the population, the window and the scoring. The reader did not compute the cut; the filed text fixes the population and window and leaves the 2026 cut to the analysis. Each executes to the golden's population (checked by the main thread).

## 6. What decides the main answer
An analytical choice: how to carry the 2025 standard onto the 2026 form. No sentence says to equate on the common items or gives the 2026 cut; the rest (full academic year, the closure, the key correction, the id merges, the n-size rule) is Layer 1 following stated text.

## Review lines
- campus_designation_rules_2026-27.pdf, 300: harmless, the filed standard itself.
- dma_technical_report_2025_excerpt.pdf, 300: harmless, the 2025 form's scale definition.
- campus_designation_rules_2026-27.pdf, 5 stump terms: harmless, generic terms; the document never names linking or equating.
- dma_technical_report_2025_excerpt.pdf, 4 stump terms: harmless; 4.1 scopes the table without describing a step.
- prompt sentence with stump terms: harmless, deliverables and rounding.
- campus_directory_2026-27.xlsx, candidates beside numbers: harmless, campus numbers, opening years and status, no results.

## Realism tells
- The item bank's creator differs from the other workbooks' (plausible for a district office).
- Every 2026 test taker has a row for each of the 50 items, blanks encoded in-row as the dictionary describes (the platform's long export writes one row per item served).
- Otherwise none.

Main thread rulings (2026-10-13): no question-1 sentence, no question-2 or question-3 file, every question-5 sentence executes to the golden's population, question 6 analytical; the review lines harmless as read; the two realism observations are the platform's export format and a second author, kept.

### Read of 2026-10-31 (reship under the 10-30 gates, pack 12 files)

One isolated reader (Sonnet, medium) on fresh copies of `prompt.txt` and `target/`; it did not solve the task.

1. Decisive step: none named; the nearest is the technical report's "The conversion applies to the 2025 form only" beside the rules' later forms on the same scale, which imply the 2025 table cannot be used on 2026 raw scores and never say to link or screen anything.
2. Ranking file: none.
3. Helper-only file: none (the merges, the registration crosswalk and the item bank read as ordinary system extracts).
4. Answer-like figure or name: none (300, 40 per cent and ten are the rules' parameters).
5. Literal sentence: rules section 4's rate over the full-academic-year testers, with sections 2, 3 and 5: the WHAT, leaving how 2026 raw scores reach the scale open.
6. What decides: an analytical choice (putting the 2026 form on the 2025 scale); the filed rules and the key notice are rule application and data handling that do not settle the cut.

Item rulings: the rules, the directory, the technical report and the prompt sentence all harmless. Realism: campus numbers stored as text in the directory (an export's own type), tidy invented names, a compact policy; no LLM tells.
