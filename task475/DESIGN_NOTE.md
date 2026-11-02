# task475 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 2, drawn 2026-11-01 at the Batch 3 queue
reset; architecture 1 is summarised under the Architecture 1 record section and its world is closed.

## Draw

1. **Card:** `.claude/skills/fingerprint/cards/task475.json`, architecture v2, registered 2026-11-01 at WARN only
   (`shell.repeat` against task461, raised by architecture 1's prompt, which this build replaced). Checked again as
   the draw's last act after task304's card landed in the same folder: no BLOCK, the three builds before this one in
   draw order (task452, task186, task160) hold no forum, forcing event or organisation family this card repeats.
2. **Pairing:** Education & Learning Sciences / `item-response-theory-test-equating` / Data Extraction & Conformation
   (ETL). The task type serves ETL and DD in the taxonomy. The deliverable is the sitting's results file conformed to
   the examination regulations: each candidate's marks on the questions they chose, moved onto one scale as
   regulation 14 requires, totalled and classified.
3. **Niche:** the Institute of Building Certification Practitioners (a fictional national professional institute
   in Australia) runs the Certifier Accreditation Examination twice a year; its Paper 2 is a three-hour written paper of
   eight optional questions of 20 marks, of which each candidate answers five. The November 2026 sitting was marked on
   the new e-marking platform; the May 2026 sitting's marks were migrated into it from the legacy system.
4. **Objective and facing:** ETL. The decision faces forward (the committee approves results not yet issued, on 10
   December 2026); the estimand is retrospective by nature, the difficulty each question proved at a sitting already
   held, because results are always conformed after the sitting they score. The fiction stands at 1 December 2026
   (the paper's date; the extracts were pulled on 30 November), the as-of date `leak.py` runs at.
5. **Shape 14** (cuts of a distribution, each cut per segment): the eight moves (8), the number passing and the
   results file's rows (3), the bar chart's parts (3), each centre's withdrawals, absentees and May sitters (6 by 3,
   18), the reviews' answer and refund (2), the files (2): 36 criteria, none stacked.
6. **Decision type** `conformed_dataset`, question form what, forum the Examinations Committee
   (`committee_or_panel`), forcing event its results meeting (`vote_or_meeting`), organisation a member body
   (`cooperative_or_member_body`), role `research_desk` (the assessment analyst in the Examinations Office).
7. **Deliverables:** `nov2026_paper2_results.csv` (the conformed results) and `paper2_results_committee_paper.docx`
   (the committee paper carrying the moves, the bar chart, the centres table and the May reviews). The csv+docx set
   cleared `guard.py`'s repeat.deliverables where pdf+xlsx and docx+xlsx warned.
8. **People,** from `guard.py names --geo AU --locale en_AU --seed 475`: Terri Brown (Chair, Examinations Committee), Stephanie
   Nguyen (Assessment Analyst, Examinations Office), Joshua Fitzgerald (Chief Examiner, Paper 2). None is in the prompt;
   no candidate carries their names (checks.py RS8).
9. **Candidates written before the choice,** each screened on the survivor anatomy and the WHAT screen:
   - A (taken): optional questions put on one scale under examinee choice. The field's question statistic (each
     question's mean mark among its answerers) sits at rung 1, and the dataset violates its precondition: the
     answerers of a question are not a random slice of the sitting, because the candidates choose.
   - B: candidates' carried scores across a change of paper (a score conversion through an anchor form): task464's
     ETL driver map closed the conversion cells, and the decisive step would be the linking method itself, the
     opponent's first move; dropped.
   - C: a harsh marking team scaled to the others by seeded scripts: the scaling is a named correction (a reflex),
     and a harsh team placed to be caught is a planted defect; dropped.
   - D: results counted over entries instead of sitters (absentees silently omitted from a reported total): a
     coverage gap is a planted defect (the batch's task123 lesson); absentees stay as Layer 1, neutral on the call.
   - E: the latest mark of record superseding the first after re-marks as the decisive step: it flips only on
     reading regulation 11.2 (data semantics); kept as a hazard of the May reviews ask.
   - F: the pass mark set by a standard-setting panel (an Angoff study): the procedure is the field's named method,
     and filing it is rule application; dropped.
10. **Screens before the draw:** `guard.py recent`, `coverage`, `mechanisms --objective etl` and `slots` on the
    mechanism nouns (choice, optional, examinee, facility, selection, difficulty) and the setting nouns (accreditation,
    examination, certifier, marking, results committee): no build on file carries examinee choice or optional-question
    difficulty. Decisive generator G6 (each question's answerers differ in composition from the sitting), with G14 and
    G17; G16 is banned in the window (task452) and G14 with `quantity_figure` read as task133's lineage puzzle, so the
    card leads with G6 and `conformed_dataset`.
11. **Abstraction test** against the nearest drivers (task479 v4 at 0.05: a unit's level from its answers through a
    known response model; task186 v2 at 0.04: a person's hit rate on items drawn again and again): both estimate a
    person; this build estimates the items, and the step is that the persons answering each item selected it. Against
    the same task type's builds `guard.py heart` lists: task488 (shipped, pending review) also ends on items and persons
    estimated together, but its driver is a calibration read against standings computed from the items' own ratings
    after adaptive delivery, a circularity; here no standing is shipped, the default is the plain question mean and the
    driver is the candidates' own choice of questions, so the shared piece is the field's standard estimator, not the
    trap. task249 v6 compares a candidate across items as its default and turns on a shared time budget; task474 v7
    carries a standard across a change of paper through candidates who sat both. None carries examinee choice.
12. **Data-native sentence:** the November paper's new fire safety question was answered by 321 candidates who
    averaged 13.5 on their other answers and 10.1 on it, and the plain consent conditions question by 481 who averaged
    8.9 elsewhere and 12.1 on it; the export holds every candidate's part marks on the five questions each chose, so
    the same candidates can be read across questions, while each question's mean mixes its difficulty with who chose
    it.

## Survivor anatomy

- Actor: the deciding property is each question's difficulty for the whole sitting, and no file has a column for it: the export carries part marks by candidate and item, the minutes carry only May's approved moves, and the property exists only as a relation between the same candidate's marks on different questions.
- Link: the signal is read through a comparison the field's question statistics never ask for: each candidate's mark on a question set against the same candidate's marks on the other questions they chose; the question means read one column at a time, and nothing in the regulations or the question paper invites a comparison across a candidate's answers.
- Reflex: the field's question-level statistic (each question's mean mark among those who answered it, set against the paper mean) sits at rung 1 and files Q6 +1, Q8 -1 and 422 of 714 passing.
- Back-test: the textbook route validates: on the May marks as they stood at the committee's 18 June meeting, the question means reproduce every move in the minutes and its 433 passes of 698 (May's choices did not sort the candidates, so the fit agrees there too).
- Second use: the export is every route's source for the results file, the minutes carry May's moves for the reviews ask, and the registers, request log, review requests, ledger and account register carry the asks; delete the decisive step and every file keeps its job.
- Shock: nothing stands out: Question 6's mean (10.1) sits among the others (9.7 to 12.1), Question 8's (12.1) is the highest but close to Questions 1 and 7 (11.6 each), the means' moves (+1 and -1) read as ordinary adjustments, and no sort of any shipped column puts Questions 6 and 8 together.
- Pins: the examination regulations file the WHAT (14.1 the move, each question against the average question counted once, for the candidates who sat; 2 defines those candidates as every candidate marked present; 14.2 the limits; 12 the pass mark; 11.2 the mark of record); no filed sentence names a method, a comparison across a candidate's answers, the choice or the candidates' standing.

## Default path

A strong analyst with every field read correctly:

1. Reads regulation 14.1 (each optional question moved by the whole marks it proved harder or easier than the
   average optional question, each counted once, for the candidates who sat the paper), 14.2 (the limits) and 12
   (a pass is 50 or more of 100 after the moves).
2. Takes the NOV26 rows of `cae_marking_export_2026.csv` and sums each candidate's part marks per question: 714
   candidates sat.
3. Takes each question's mean mark among those who answered it (the facility the field reports for every
   question), sets it against the mean of the eight means and rounds: Q1 -1, Q2 +1, Q3 0, Q4 +1, Q5 0, Q6 +1, Q7 -1,
   Q8 -1.
4. Checks the method on May: the same means on the May marks at the June meeting give every move in the minutes and
   its 433 passes of 698.
5. Applies the moves held within 0 and 20, totals and passes 50 or more.

Ends on: Q6 +1 and Q8 -1, 422 of the 714 candidates pass.

Golden: Q1 -1, Q2 +1, Q3 0, Q4 +1, Q5 0, Q6 +3, Q7 -1, Q8 -3; 401 of the 714 candidates pass.

## Stump sentence

The default path sets each question's mean mark among its answerers against the paper's mean, moves Question 6 by +1
and Question 8 by -1 and files 422 passes of 714; but the stronger candidates chose Question 6 and the weaker chose
Question 8 (their answerers averaged 13.5 and 8.9 on their other answers), so only each question read on the same
candidates across the questions they chose gives its difficulty for the candidates who sat, Question 6 +3 and
Question 8 -3, and 401 passes.

## Three rules

- Task type: item-response-theory-test-equating in Education & Learning Sciences, which serves Data Extraction & Conformation (ETL): a written paper's optional questions conformed onto one mark scale and the sitting's results file conformed to the examination regulations.
- Domain test: the deciding quantity is each optional question's difficulty for the whole sitting, which assessment practice reads from candidates' marks as a question effect on the paper's mark scale (the item difficulty of classical and item response analysis); with another field's nouns there is no optional question, no choice of five from eight and no mark scale for a move to act on.
- Swap: "set each optional hospital ward's staffing allowance by how much harder its patients proved than the average ward's" loses the deciding structure: patients do not each choose five of eight wards and get scored on every one they chose by the same examiners, so no person's results on several alternatives can be compared and nothing is moved on a common scale.
- Layer 1: the export spans two series in two code layouts (the legacy system's items 6(b) and component CAE2 on the migrated May rows, the platform's Q06.2 and CAE-P2 in November); part marks out of different maxima with no-response parts shown as '-'; marks of record re-entered after borderline re-marks and reviews in May; candidate numbers issued afresh at each sitting; the legacy register's SURNAME, Given names and dd/mm/yyyy dates against the portal's separate fields and ISO dates (a member's account pre-filled with a preferred first name); the Parramatta centre renamed Western Sydney at the portal launch; the portal's UTC stamps across the daylight-saving change; withdrawals actioned days after they were sent; the CRM keying candidate numbers as candidates type them; account lines carrying their invoice's total; absentees present in the register and absent from the export. Each is produced by the system named, none is placed to be caught, and none moves the call (R2.1 to R2.7).
- Layer 2: estimation under a violated precondition (selection on the outcome's driver): a question's mean mark estimates its difficulty for the sitting only if its answerers stand for the sitting; under examinee choice they do not, and the difficulty must be read with each candidate's own standing held fixed.
- Decisive step: recognising that each question's answerers chose it, so its mean mark carries its choosers' standing, and reading its difficulty from the same candidates' marks across the questions they chose: a candidate effect and a question effect fitted together, each question's effect set against the average question.
- Not semantics: every field, code and unit can be read correctly (series, item codes, part maxima, no-response parts, the mark of record, regulation 14's population, comparison and rounding) and the analyst still takes each question's mean as its difficulty; no field, code or definition holds a candidate's standing or flags a choice.
- Not rule application: regulation 14.1 names what is measured (the difficulty for the candidates who sat, against the average question counted once, rounded) and not how; executing every filed rule with the question means files 422. Enumerated family: no moves (432 passes), question means (422), means against an answer-weighted average (422), medians (435), the fit of candidate and question (401), its one-step form, each question's answerers' mark less their own mean on their other answers (401), the regression adjustment on the answerers' other marks (401), a random-intercept model (401), the fit on the logit scale carried back to marks (401): spread 401 to 435 over four distinct pass counts. Standing family once the choice is seen (alternating means, least squares, one-step differences, regression adjustment, random intercept, logit scale, a part-level fit, four-answer candidates in or out, an answer-weighted average): the same eight moves and 401 passes, every value at least 0.2 from a rounding line (checks.py L3, SF2, SF9, SF10). What rules the means out is the data, loudly for anyone who reads across a candidate's answers and silently for the column means: Question 6's answerers average 13.5 on their other answers and 10.1 on it, Question 8's 8.9 and 12.1.
- Analyst test: a strong analyst who conforms the export correctly and applies regulation 14 with each question's mean among its answerers against the paper mean files Q6 +1, Q8 -1 and 422 of 714 passing, against the golden's Q6 +3, Q8 -3 and 401.
- Estimand: regulations 2, 12, 14.1 and 14.2 in cae_examination_regulations_2026.pdf: the population is every candidate marked present for Paper 2 at the November 2026 sitting (whichever questions they answered), the outcome each optional question's mark of record, the comparison the average of the optional questions each counted once, the unit whole marks rounded to the nearest, the window the November sitting's marks of record, and a pass at 50 or more of 100 after the moves.
- No decoy: nothing is planted: no memo, draft, briefing or stakeholder figure argues a move or a pass count; the minutes report May's approved moves, which every route reproduces; no file computes a November question statistic; the two distractors (the results history and the 2027 venue holds) answer other questions.
- No certified replay: no November move, difficulty or pass count exists anywhere in the pack, and May's certified moves are reproduced alike by the means and by the fit, so nothing certified can be backed out into the method.
- Lesson: a question's mean mark is a property of the candidates who chose it as much as of the question; when candidates choose which items to answer, read each item's difficulty across the same candidates' other answers before putting it on one scale. No build on file teaches examinee choice or optional-question difficulty.

## Readability screen

| Rung | What the reader does | Test that could fire | Verdict |
|---|---|---|---|
| 0 no moves | totals the marks as they stand | regulation 14 sends any reader past it | readable |
| 1 question means | sets each question's mean among its answerers against the paper mean | the field's reflex, the question statistic every results meeting sees (test 3) | readable |
| 1b means, other centres | the same against an answer-weighted average or with medians | reflex variants (test 3) | readable |
| 2 candidate and question together (decisive) | reads each question on the same candidates across the questions they chose | no filed sentence names a comparison or the choice (1); no column holds standing or flags a choice (2); the reflex is rung 1 (3); the May minutes reproduce under the means (4); the battery compares no candidate across items (5); not one subtraction of a reported figure (6); no organ exists for it, the export is every route's source (7) | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "moved" | a whole-mark constant added to every answer to the question | a proportional scaling | another call | regulation 14.1 "moved by a whole number of marks", 14.2 "applied to the mark of record of every candidate who answered" |
| SF2 | "the average of the paper's optional questions, each counted once" | the eight question effects averaged equally | an average weighted by answers | same call (Q6 +3, Q8 -3, 401) | same call, and 14.1 "each counted once" |
| SF3 | "the candidates who sat the paper" | every candidate marked present (714) | those who answered the question | the means' answer, 422 | regulation 2 "every candidate marked present for that paper at the sitting" |
| SF4 | "rounded to the nearest whole mark" | round each move once | truncate toward zero | Q2 0, Q7 0, Q8 -2, 415 passes | 14.1 "rounded to the nearest whole mark"; no standing value within 0.2 of a rounding line |
| SF5 | the limits of 14.2 | moved marks held within 0 and 20 | no limits | same call (401) | same call |
| SF6 | the pass | 50 or more | more than 50 | 388 | regulation 12 "a total of 50 or more" |
| SF7 | the mark of record | the last mark entered for a part | the first | same call (one November mark per part) | same call, and regulation 11.2 |
| SF8 | a no-response part ('-') | counts nothing | dropped from the question | same call | same call |
| SF9 | candidates who answered four questions | in the results and the fit | out of the fit | same call | same call; in the results under regulation 2 |
| SF10 | the unit of the move | the question | a move per part | same call when summed to questions | regulation 14.1 "each optional question is moved" |
| SF11 | "the mark counted on each question" | the moved mark held within 0 and 20 | the raw mark | another results file | 14.2 and the prompt's "mark counted" |
| SF12 | the sitting's rows | series NOV26 (items Qnn.k) | every row of the export | another matrix | the export's series column; the question paper's numbering |
| SF13 | the total | the counted marks summed over the questions answered | out of five questions regardless | same call | regulation 12 "of the 100 marks available" |
| SF14 | a withdrawal's date | the request's receipt, Sydney time | the day actioned (status_changed), or the UTC date | another count at every centre | regulation 17.1 "has effect from the time the request is received", regulation 20 Sydney time |
| SF15 | "absentees" | entered, not withdrawn before the day, not sitting | every withdrawn entry with no marks | another count | regulation 17.2 and 17.3 |
| SF16 | a candidate's centre | the entry's centre after any transfer | the centre first entered | same call (transfers are carried into the entry) | regulation 18 |
| SF17 | "had sat Paper 2 in May" | marked present in May (MAY26 marks) | entered in May | another count | regulation 2 "marked present" |
| SF18 | the same person across sittings | member number where both carry one, else family name, given name and date of birth | the candidate number | another count | candidate numbers are issued per sitting (the directory's blocks, the register); the match is unique and the same under every name normalisation (checks.py SF18) |
| SF19 | "May results changed on review" | the result issued on the marks of record on 30 June against the result after review, both with the minutes' moves | the first marks against the last | same call among the requests | regulations 16 and 19.2 |
| SF20 | "the review fees to refund" | the fee paid for each changed review and each declined request | the schedule fee | another refund | regulation 19.4 "the fee paid", Schedule 1's agreed-rate sentence |
| SF21 | the refund's rounding | AUD 2,625.13 to the nearest dollar | none | same call | the cents sit 0.37 from the half dollar |

## Ladder

Built values from the cut pack (checks.py L1 to L7, verify.py).

| Rung | Route | Q6 | Q8 | Passing of 714 |
|---|---|---|---|---|
| 0 | no moves | 0 | 0 | 432 |
| 1 (default path) | each question's mean among its answerers against the paper mean | +1 | -1 | 422 |
| 1b | the same against an answer-weighted average | +1 | -1 | 422 |
| 1c | medians against the median | +1 | -1 | 435 |
| golden | candidate and question fitted together, each question against the average question | +3 | -3 | 401 |

- The rungs agree with the golden on Q2, Q3, Q4, Q5 and Q7 (+1, 0, +1, 0, -1) and on Q1 except the medians (0);
  they part on the two questions the choice sorted.
- Standing family values for Q6 and Q8: alternating means and least squares 3.04 and -2.94, one-step differences 3.22
  and -3.29, regression adjustment 2.85 and -2.72, random intercept 2.80 and -2.78, logit scale 3.28 and -2.94;
  smallest distance to a rounding line over all eight questions 0.21 (the one-step form), verify.py's own least
  squares 0.42.
- Evidence: Question 6's answerers score 3.39 marks less on it than on their other answers, Question 8's 3.12 more
  (L6).

## Closure table

| Axis | Name | Reading here | Move |
|---|---|---|---|
| 1 | Population | every candidate marked present for Paper 2 at the November sitting (714) | filed, regulation 2 with 14.1 (SF3); four-answer candidates in (SF9) |
| 2 | Unit of account | the candidate's answer to a question; one move per question | filed, 14.1 and 14.2 (SF10) |
| 3 | Attribution window | the November 2026 sitting, series NOV26 | C1 (SF12) |
| 4 | As-of dating | the marks of record exported on 30 November | C1: one mark per November part (SF7) |
| 5 | Version basis | the last mark entered per part | filed, 11.2; the asks read May as issued on 30 June and after review (SF19) |
| 6 | Denominator | the average question, each counted once | filed, 14.1; C1 against answer weights (SF2) |
| 7 | Weighting | each answer once in the fit | C1: every standing member gives the same moves (L3) |
| 8 | Window length | one sitting | not applicable, asserted by the series (SF12) |
| 9 | Boundary inclusivity | 50 or more passes | filed, regulation 12 (SF6) |
| 10 | Rounding path | each move rounded once, marks held, totals in whole marks | filed, 14.1; C1, no value within 0.2 of a rounding line (SF4) |
| 11 | Tie-break | none | C1: no move at a half mark |
| 12 | Maturity and censoring | none: every November script marked by the export | not applicable, asserted (A5, R1a) |
| 13 | Order of operations | move, hold within 0 and 20, total | filed, 14.2; C1, the limits change no result (SF5) |
| 14 | Row order | none | C1: the fit is order-free |
| 15 | Duplicate resolution | one November row per part; May's later marks supersede | C1 (SF7); filed 11.2 for the asks |
| 16 | Identity normalisation | candidate number within a sitting; across sittings member number or name and date of birth | C1 for the call; SF18 for the asks |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | part marks out of their maxima, 20 a question | units in the data (max_mark); C1 (R2.1) |
| 19 | Code and status semantics | '-' is no response and counts nothing; Qnn.k is question nn, part k | C1 (SF8); the question paper |
| 20 | Integerisation | whole-mark moves and marks | filed, 14.1 |
| 21 | Clause scope | 14.1 per question per sitting; 14.3 the moves stand for the sitting | filed; the May reviews keep May's moves (19.2) |
| 22 | Forward window contents | none: the results are for the sitting just marked | not applicable |

## Literal reader

Executed word for word, regulation 14.1 asks how much harder each question proved than the average question, each
counted once, for the candidates who sat the paper, which regulation 2 defines as every candidate marked present: all
714, each of whom answered five questions (18 answered four). No file holds a candidate's mark on a question they did
not choose, so every literal reader has to estimate each question's difficulty for the 714 from the marks that exist.
The question means estimate it only if a question's answerers stand for the 714, and the records show they do not;
the easy answer (422) therefore comes from an easier method on the same literal estimand, never from another reading.
Every term and convention has a fork-table row, every alternative reading gives the golden or violates a quoted
sentence, and every write-up step names the file and the regulation it executes. Regulation 14.1 names the
quantity and never the procedure: no formula, no averaging over candidates and no comparison of a candidate's
answers is filed, so joining the files leaves the estimate still to make, and the standard route a strong analyst
takes (the question means) files 422 against the golden's 401.

## Oracles

None. No file holds a November move, difficulty or question statistic; the minutes' May moves and pass count are
reproduced by the means and by the fit alike, so they arbitrate nothing; no control ties only under the golden. In the
asks no file pairs a withdrawal's receipt with its action, no column marks a May absentee, a surname change, a re-keyed
candidate number or an account's agreed fee, and the invoice ledger ties to its requests under every handling.

## Ask sheet

The asks sit on files the call never reads: the November portal's entries and request log, the legacy May register,
the export's May rows, the review requests, the invoice ledger and the account register. Ask 1: for each centre, the
withdrawals, the absentees and the November sitters who had also sat Paper 2 in May (18 figures). Ask 2: whether any
May results changed on review and, if so, how many, and the review fees to refund (2 figures).

- Pair ceiling: 35.0 (cracker 45.0 on the call with 0 of 20 ask criteria, mirror 25.0 with 6 of 8 moves and 0 of 20 ask criteria).
- Mirror leakage: 0.0 per cent of the ask weight (nothing in the asks comes from the call).
- Measured by: generator/ceiling.py on the cut pack.

| Ask | Primary device | Hazards | Cracker's handling | Cracker |
|---|---|---|---|---|
| Ask 1 withdrawals by centre | D8: the register's status_changed is the day the office actioned a withdrawal, and requests sent in the week before the sitting were actioned on 9 and 10 November; only the request log's submitted time dates the receipt (every centre holds at least one, A4) | UTC stamps across the daylight-saving change, Paper 1-only withdrawals, requests received on the day | dates each withdrawal by the register's status_changed | miss |
| Ask 1 absentees by centre | the same lagged withdrawals, which the register's date leaves absent | the same | the same | miss |
| Ask 1 May sitters by centre | D4: the legacy register shows May absentees as Entered and only the export's MAY26 rows show who sat; D7: candidate numbers are issued afresh, and members who changed surname match only on member number | the legacy SURNAME, Given names and dd/mm/yyyy dates, the Parramatta rename, new members | links the registers on name and date of birth and counts the May entrants shown as Entered | miss |
| Ask 2 results changed on review | D7: candidates keyed their own numbers and three carry two digits transposed; the true May candidate is the one whose family name matches | borderline re-marks before issue, a delayed script marked after issue, declined late requests | joins each request to the May marks on the keyed number | miss |
| Ask 2 refund | D6: each account line repeats its invoice's total, and the fee paid is Schedule 1's fee for the day received less the firm's agreed discount (an allocation by a recorded weight, equal to the invoice share to the cent, SF20) | the fee change on 1 July, declined requests refunded | refunds each account request at the schedule fee | miss |

The full includer (every device handled) keeps all 20 (stress row, ceiling.py). Zero device rows sit in the main
call's population: the call reads the export's NOV26 rows alone (R2.6), no withdrawn entry carries a November mark
(A5), and every ask figure recomputes the clean truth (A1, A2).

## Leak review

`leak.py --asof 2026-12-01` on the final cut: REVIEW, no LEAK; each line answered.

- Sweep 3, the regulations and the minutes carry most words of the committed call: they are the rules the call executes
  and May's results meeting; neither states a November move, difficulty or pass count (checks.py R3c).
- Sweep 4, the regulations (8 terms), the question paper (5) and the minutes (8): the regulations must say "a choice
  of questions", "the average of the paper's optional questions" and "mark of record" to file the WHAT; the other
  hits are "multiple choice paper", "minutes of meeting", "no member declared", "the closing date for reviews", the paper's "ten
  minutes reading time" and "each question carries 20 marks". No document relates a choice to a mark.
- Sweep 9, corporate_accounts.csv's agreement end dates (30 June 2027): forward-looking terms of a live agreement, the
  file's own allow-listed kind of date.
- Sweep 12, the regulations name "Sydney", "accredited", "mark", "paper", "papers" and "questions": ordinary words of
  the institute's own rules (Sydney time, accreditation), not a description of any file.

## Architecture 1 record

Drawn 2026-10-20 from seed ET32 in demographic-social-science / income-poverty-inequality (ETL): the Corran Valley
regional council of governments splitting its 2027 weatherization fund across fourteen member counties by tax-year
2023 earned income credit returns with qualifying children, from the IRS ZIP-code tables taken to counties through
the residential ZIP-to-county file, capped at 12 per cent. The default applied the statewide share of claimants with
children in each AGI class to every county and capped the seat county; the golden decomposed each county's lowest-AGI
claims into families and childless workers by their paired credit amounts, and left the seat county at 11.46 per cent
under the cap. Shipped 2026-10-20 (judge passes 1 and 2 DETERMINISTIC), no portal result; re-rooted 2026-11-01 at
the Batch 3 queue reset with its world closed. Its reports are kept as `determinism_check_report_arch1.md`,
`determinism_check_report_pass2_arch1.md` and `leak_check_report_arch1.md`.

## Tried and rejected

- The seed's own mechanisms as the decisive step (2026-10-20, screened at the draw): the crosswalk's direction, its
  ratio type and the other-ZIP-codes line each flip only on reading a file or a field correctly, so each is data
  semantics; all three stay in the pack as Layer 1 under filed sentences.
- Apportioning split ZIP codes by a better weight than residential addresses (2026-10-20, screened): a crossing
  partition split by an indicator whose ratio to the target differs within the coarse unit, which task474's first
  architecture spent at stage 4 (a reader landed it) and task476's first architecture carried to a SEND_BACK.
- Suppressed small cells recovered against the state total (2026-10-20, screened): task465 recorded the same stump
  sitting in Layer 1, and task201 found disclosure bounds reduce to interval arithmetic with no estimation choice.
- Late-filed returns completed from processing-year files, and two administrative lists for the families' true count
  (2026-10-20, screened): maturity and capture strategies, both banned in the current window and spent in this lane.
- A LEGACY_JOB_NO column in the job export as ask B's antidote (2026-10-20, stage 3, before any reader): a pack that
  names the renumbering hands the join to every careful solver (proven-in-production, 76 v1); the old numbers moved
  into the conversion notes of the status history.
- The close-out's jobs and spending by agency (2026-10-20, stage 3): agency totals tie only under the right join and
  the right completion date, a control tying only under the golden; the close-out now reports program-wide spending by
  category and fund and the agencies' intake, which tie under every handling.
- Agency-blocked renumbering at the conversion (2026-10-20, stage 3): the raw join piled the year's spending into the
  last two agencies' counties (one county at 2.4 times its true figure), loud enough to send any solver looking; the
  conversion now loads the old jobs in their old order.
- Program years from July to June (2026-10-20, stage 3): the asked year had not closed at the pull; program years are
  calendar years and the asks read the last closed one, 2025.
- The first ask devices (2026-10-20, stage 4 round 1, measured): D8 alone as ask A's primary, where policy 6.1's
  "first completed" sent both readers to the status history and both kept all fourteen dwellings; and D7 with the move
  after the year, where reader 2 read the conversion notes, validated the mapping by agency and kept all fourteen
  spending figures (score_reader exit 1, 28 of 71). Re-sited: ask A on the funding-code vintage, ask B on the invoice
  month behind a move inside the year; both readers had missed the call.
- Architecture 1 as a whole (2026-11-01, the Batch 3 queue reset): re-rooted with its world closed, one architecture
  per world; the weatherization-fund world is not drawn again.
- Carried scores across a change of paper as architecture 2's step (2026-11-01, draw): task464's driver map closed the
  conversion cells and the linking method would sit at the top of the ladder; candidate B.
- A harsh marking team scaled by seeded scripts (2026-11-01, draw): a named correction and a planted defect; candidate C.
- Absentees silently left out of a reported total (2026-11-01, draw): a coverage gap reads as a planted defect;
  candidate D, kept as neutral Layer 1.
- The latest mark of record after re-marks as the step (2026-11-01, draw): data semantics; candidate E, kept as a May
  reviews hazard.
- A standard-setting panel's pass mark (2026-11-01, draw): the field's named procedure, rule application once filed;
  candidate F.
- G16 as the decisive generator and G14 with `quantity_figure` (2026-11-01, guard): G16 banned against task452 in the
  window, and G14 with a figure decision read as task133's lineage puzzle (same_puzzle BLOCK); the card leads with G6
  and `conformed_dataset`.
- Choice strong enough for the means to move Question 6 the wrong way (2026-11-01, prototype on the clean truth): the
  regression adjustment and the random intercept then fell a whole mark short of the fit, a standing member on another
  call; the choice was set so every standing member agrees and the means under-move instead (+1 against +3).
- A compulsory Paper 1 shipped at item level (2026-11-01, design): an adjustment anchored on Paper 1 scores is a
  defensible member attenuated by that paper's own reliability and lands between the means and the fit; Paper 1 marks
  are not shipped.
- Duplicate portal accounts as a withdrawals device (2026-11-02, stage 3, before any reader): an entry the office
  closed as a duplicate reads as withdrawn or as absent depending on whether the entry or the person is counted, a fork
  on the ask; removed from the world.
- Every centre's May-sitter figure was first left to the draw (2026-11-02, stage 3, checks.py A3): at two centres the
  May absentees who re-entered and the members who changed surname cancelled, so the careful route kept those figures;
  the operating records were redrawn so the two never cancel at a centre.
- Given names cut to the first name for any candidate in the portal (2026-11-02, stage 3, measured): a match on all
  given names would have missed 22 non-members that a first-name match finds, a fork on the ask; the cut is now the
  membership database's pre-fill of a member's account, so every name rule gives the same 150 links (SF18).
- The November marks on seed 477238 (2026-11-02, stage 3): their unmoved pass count equalled the May minutes' 433, a
  coincidence a reader could take for a planted tie; the marks were redrawn (432 unmoved, 401 golden).
- The draft minutes as a PDF (2026-11-02, stage 3, `guard.py surface`): the pack's format mix matched two shipped
  builds exactly; minutes circulated as a draft for confirmation are a Word document, as the office keeps them.
