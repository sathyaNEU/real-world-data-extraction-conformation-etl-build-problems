# leak check, task482

**Verdict: REVIEW.** 17 files read, 14 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: architecture, school, taught, reader, golden, reflex, population, decisive, readers, member, record, shipped, carried, carries, inside, family, register, screened, nothing, sentence, appendix, graded, landed, reading, window

## 1 file names (REVIEW 2)
- **REVIEW** `corlinn_item_bank_2026.xlsx`: a sheet named 'Notes': confirm it is the organisation's own notes and does not describe the data's columns or files
- **REVIEW** `entries_register_aug2026.xlsx`: a sheet named 'Notes': confirm it is the organisation's own notes and does not describe the data's columns or files

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `y10sci_paper_specification_2027.pdf`: carries 9 of 9 distinctive words of the committed call: 'Set Paper C for the November 2027 sitting: its expected mark at the Achieved standard is 25 of 50 (24.80), against 26 fo'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `y10sci_course_review_2026.pdf`: 3 of 25 stump-paragraph terms appear (school, member, appendix); read whether the document names the move
- **REVIEW** `y10sci_paper_specification_2027.pdf`: 3 of 25 stump-paragraph terms appear (school, member, record); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 36% of 192 prompts (cap 30%); reword at the role level, not the verb

## 12 describing content (REVIEW 1)
- **REVIEW** `y10sci_course_review_2026.pdf`: names 8 column(s) of the data files verbatim (Cells and body systems, Physical World, Planet Earth and Beyond, Unit, schools, start): confirm it is the organisation's own record and not a note written for the analyst

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)


## Solver's-eye read

Two isolated reads (general-purpose agents on Sonnet at medium effort, each on its own byte-identical copy of the prompt and the pack, with no design note, generator or golden). Round 1 on zip 3f18332c: CLEAN. Round 2 on zip 02c4e9b7, after the make-up roster header and the batch column were added and the forum redrawn: CLEAN.

### Round 2

# Leak read round 2, task482

Not solved; no figures given. Verdict: CLEAN, with two low-severity notes (items 1 and 11).

### New or changed sentences
1. makeup_roster pdf header, "Paper form M26 is marked out of 50 at the host centre, and the marker writes the candidate's mark on the script cover out of 50 and as a percentage. The office keys each cover's mark out of 50, each keyer's session as one batch on one template."
   Mostly a fact about the form and the office's keying (what is marked, how the cover is written). The last clause ("each keyer's session as one batch on one template") is a mild hint that a batch may differ from the stated scale, since a batch column now exists and one batch holds marks above 50 (a visible anomaly in the CSV). It does not say how to correct or what the make-up mean turns on. It touches only the supplemental ask, not the main call. Low severity: it is borderline between record and nudge, but it reads as an office note, not as handling.
2. makeup_scripts_keyed.csv `batch` column: a fact (the keying session). Lets the analyst see batch structure; states no handling.
3. Council minute item 5, "The Council will set the 2027 paper at its meeting of 2 December, on the head of assessment's recommendation." Fact/context only. Nothing about the answer.
4. Email: "The Council meets on 2 December...", "Could you work up the recommendation...", "carry the August sitting's entries and sittings by region, and the make-up sitting's numbers and marks". Request context only; names the deliverable content, not the method.
5. prompt.txt "Write the recommendation to the Council as council_memo.docx": deliverable naming, consistent with the email. No leak.
6. Entries register: one entry date per row, all datetimes; "Status" E/W and Source notes are plain record facts. Nothing handling-like.

Other new-to-me analyst-facing sentences: none found.

### Standing questions
7. Decisive step: no file states it. The spec section 4 ("expected mark ... for a candidate sitting the 2027 paper, is nearest 25 ... sum over the items of the probability, under the Rasch model on the bank scale ... compared on their expected marks before rounding") states the estimand, the formula and the no-rounding rule (the how of the figure at the level of the standard definition), not which difficulty set or whether anything must be adjusted.
8. No file ranks or scores the three drafts. The drafts workbook holds only item card lists. The standard-setting record gives per-form raw marks for the 2026 forms (F1 to F4), not for the drafts.
9. None exists solely to help the analyst. The renumbering file, calibration runs and bank are working inputs; the course review, bell times, survey and minutes read as distractors/context.
10. No figure or name reads as the answer. The "25" is the spec's stated target. The 0.35 Achieved cut is a stated standard.
11. Literal sentence: spec section 4, "The paper set for 2027 is the submitted draft whose expected mark at the Achieved standard, for a candidate sitting the 2027 paper, is nearest 25 of its 50 marks. The expected mark is the sum over the paper's items of the probability, under the Rasch model on the bank scale, that a candidate at the Achieved standard answers the item correctly. Drafts are compared on their expected marks before rounding." Literal result in words: for each draft, sum Rasch probabilities at the 0.35 logit Achieved standard over its 50 items, pick the draft nearest 25. The phrase "for a candidate sitting the 2027 paper" and the bank note ("final run supersedes the preliminary") are fact-like and do not spell out which difficulty values or card-to-item mapping to use. Low severity note: the "2027 paper" wording and the 2026 form raw marks (26 to 28 at Achieved) in the standard-setting record sit close to the analyst's path but state no handling.
12. Decided by an analytical choice (which item difficulties apply to a 2027 sitting, given the final versus preliminary calibration, the anchored scale and renumbered cards), judged from the data; no sentence announces it. I see no planted decoy: the preliminary run is plainly labelled as superseded, the sort of thing an organisation would keep.
13. Realism: nothing reads as generated. The roster is typed returns, the email and minutes are plain, the bank notes are terse, and the spelling of schools' dates varies as real uploads do. No toolchain signatures, hidden sheets or tracked changes found (all sheets visible).
14. Regional entries and sittings: no sentence says how to count. The entries register notes define status (W is not a candidate) and source; member_schools.csv maps school to region. No file hands over a count by region. The roster header and sessions file give no counts.
15. Make-up candidates and mean by region: the roster header says the form is out of 50 and the keyed batches share one template per keyer; the roster's Attended column and the keyed CSV (script number, school code, entry no, mark) support the work. No sentence says how to count or average them (for example which marks to correct or which attendees to include), and no file hands over a regional figure or mean.

### Round 1

Verdict: CLEAN (no leak found; two minor observations below, neither hands over an answer).

1. Decisive step sentence: none. The 2027 specification (y10sci_paper_specification_2027.pdf s4) files the estimand ("expected mark is the sum over the paper's items of the probability, under the Rasch model on the bank scale, that a candidate at the Achieved standard answers the item correctly... compared before rounding") but no file says which calibration run, anchor handling or item-code mapping to use, or announces any step as decisive.
2. Ranking/scoring file: none. y10sci_2027_drafts.xlsx lists only Q/Card/Unit/Marks per paper; no expected marks. The standard-setting record gives raw marks for the 2026 forms only.
3. Files existing only to help the analyst: none evident. Notes sheets are short and read as bank/register housekeeping. member_bell_times_2026.json, candidate_survey_2026.csv, course review Appendix B and the council minute read as plausible context or distractors.
4. Figure or name reading as the answer: none. No expected mark, draft preference or regional count appears anywhere.
5. Sentence fixing computation/population: spec s4, "the submitted draft whose expected mark at the Achieved standard, for a candidate sitting the 2027 paper, is nearest 25 of its 50 marks... sum over the paper's items of the probability, under the Rasch model on the bank scale, that a candidate at the Achieved standard answers the item correctly." Literal result: a Rasch expected-score sum over each draft's 50 items at the Achieved standard theta (0.35 logits per the standard-setting record), compared unrounded to 25. The standard-setting record s1: "A candidate is reported at a standard when their ability estimate on the bank scale reaches it." Reading the spec literally also means 2027 bank difficulties (final calibration) for the cards, with the 2027 sitting date (council minute, Nov 1-12) and the course review sequences as context; the pack states no adjustment rule.
6. What decides the main answer: an analytical choice (which item difficulties are the right ones on the bank scale at the 2027 sitting, given calibration runs, anchors, renumbering and scale drift). No single sentence or file settles it; the pack gives the raw materials (bank_calibration_runs.csv with 2025 final / 2026 preliminary / 2026 final, item_renumbering_2025.csv, the bank Notes: "The final run supersedes the preliminary run"). The superseding statement is a stated ordering of runs, not the stump. Nothing reads as planted.
7. Realism: no tell found. PDFs all LibreOffice 24.2, author the Trust, with distinct, plausible creation dates; the make-up roster text is not clipped in extraction; the roster, keyed scripts (three keyers, keyed 31 Aug to 7 Sep) and register (status E/W, school upload/office) read as kept records. Session starts cluster around 21:50 and 02:02 UTC, consistent with NZ period bell times, not a generated pattern. Minor: all xlsx files share author names consistent with the story (Jeremy York, Paul Shailer, Trust Office); the register's every row shows "Entered on" 2026-05-18 in the first rows (sorted by school; may vary later), which is mildly uniform but not clearly a tell.
8. Regional entries/sittings: no file hands over a count by region. member_schools.csv maps school_code to region; the register Notes say "W withdrawn by the school before the sitting (a withdrawn entry is not a candidate)", which states the entry-counting rule. How to count online sittings (sessions with status submitted vs dropped) is not stated anywhere; no regional figure appears.
9. Make-up candidates and mean mark by region: no file states how to count or average them and none hands over a regional figure. The roster PDF has an Attended Yes/No column and "Booked candidates by host centre, as typed from the host supervisors' returns"; makeup_scripts_keyed.csv has script_no, school_code (host), entry_no (mostly blank), mark. The link from script to home school and region has to be reconstructed; no sentence says how.

Rulings on flagged files:
- corlinn_item_bank_2026.xlsx Notes: reads as the Trust's own record (calibration run date, anchor block, supersession, fit definition). Not a note for the analyst.
- entries_register_aug2026.xlsx Notes: reads as the office's own register legend (as-at date, status codes, source codes). Fine.
- y10sci_paper_specification_2027.pdf: reads as a genuine committee specification; shared wording with the prompt is natural (the prompt cites it). It files the estimand, not a step-by-step method; acceptable.
- y10sci_course_review_2026.pdf: reads as a curriculum committee paper with messy school-returned Appendix B (mixed date formats, varying unit names); unit names also appear as column values in the drafts workbook, but nothing in it points to a decisive step.
