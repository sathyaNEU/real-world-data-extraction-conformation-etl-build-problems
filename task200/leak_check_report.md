# leak check, task200

**Verdict: REVIEW.** 17 files read, 14 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: projection, screener, meeting, threat, library, asserted, meetings, projections, section, history, standard, points, sentence, member, decisive, operator, readable, carries, operators, earlier, memory, method, article, system, exports

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `docs/SPS-04_screener_performance_standard_issue3.docx`: 11 of 25 stump-paragraph terms appear (projection, screener, threat, section, history, standard); read whether the document names the move
- **REVIEW** `docs/security_compliance_review_2026.pdf`: 4 of 25 stump-paragraph terms appear (screener, meeting, meetings, article); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 12 describing content (REVIEW 1)
- **REVIEW** `docs/SPS-04_screener_performance_standard_issue3.docx`: names 4 column(s) of the data files verbatim (Screen, Team, cancelled, workstation): confirm it is the organisation's own record and not a note written for the analyst

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated reader (medium effort), fresh copies of prompt.txt and target/ only, nothing solved.

1. Decisive step announced: none. Nearest is SPS-04 4.2 ("The course starts with the team whose X-ray operators are least likely to find a prohibited article in a passenger's cabin bag ..."), the organisation's own ordering rule: it names the estimand, not a method.
2. File ranking or scoring the teams: none; every file is raw.
3. File existing only to help the analyst: none.
4. Figure or name reading as the answer: none.
5. Filed sentences fixing a figure or population: SPS-04 4.2 and 4.3 (teams ordered by how likely their operators are to find a prohibited article, on the year just ended), section 3 definitions (team as rostered on 31 December; a TIP hit and miss, cancelled projections neither; a search charged to the screener whose decision sent it, a clear search finding nothing; screen time as logged-on time; a certificate running three years from the assessment that awarded it, a later pass replacing it), and the prompt's roster date, certificate cut-off and rounding. Main thread: each literal execution is the golden's reading (fork table).
6. What decides the main answer: an analytical choice of estimator for each team's likelihood of finding a real article, on top of ETL linkage; no method is filed and nothing reads planted. Main thread: the decisive step is restricting the evidence to first meetings with each library image, since a real article is always new to the screener; no column marks a first meeting, so it is a relation across each screener's history, not a field reading (checks.py analyst test).

Rulings:
- docs/SPS-04_screener_performance_standard_issue3.docx naming column words: harmless, the organisation's own standard with purpose, scope, revision history, owner and approver; no file names or data-describing language.
- docs/security_compliance_review_2026.pdf: harmless, ranks nothing and puts screener image interpretation outside its scope.
- re_remedial_course_2027.eml: harmless, sets the schedule and the three fields, ranks no team, suggests no measure.
- Stump-vocabulary lines (SPS-04: projection, screener, threat, section, history, standard; the compliance review: screener, meeting, meetings, article): ruled in the main thread, harmless; "meetings" in the review are team briefings, and neither document mentions familiarity, repeat images or first meetings.

Realism note fixed before ship: SPS-04's revision history dates Issue 3 at 31 December 2026 against an effective date of 1 December 2026 in its header.

## Solver's-eye read (round 2, after the stage 4 repairs)

Isolated reader (medium effort), fresh copies of prompt.txt and target/ only, nothing solved.

1. Decisive step announced: none. Nearest is SPS-04 4.2, the filed estimand (what to rank on), not the method.
2. File ranking or scoring the teams: none.
3. File existing only to help the analyst: none.
4. Figure or name reading as the answer: none; the compliance review's figures concern other areas.
5. Filed sentences fixing a figure or population: SPS-04 section 3 (team as rostered on 31 December, TIP hit and miss with cancelled projections neither, screen time as logged-on time, a search charged to the deciding screener, the certificate rule) and 4.2 and 4.3 (the order on the year just ended). Main thread: each literal execution is the golden's reading (fork table SF1 to SF13).
6. What decides the main answer: an analytical choice of how each team's likelihood of finding a real article is estimated; no decoy, no single field that flips it.

Rulings:
- SPS-04 with its Issued column: harmless, the organisation's own standard; issued precedes effective in every row and matches the docx metadata; its 5.1 twenty-minute rule matches the data.
- Pier B log: harmless, an authentic export; the twenty-minute ceiling reads as the system's prompted log-off tied to a stated rule.
- Documents and email: harmless, none ranks teams or suggests a measure.

Realism note fixed before ship: docs/security_compliance_review_2026.pdf was a 3.3 KB single page with equal creation and modification stamps, more typical of a library than of Word.
