# task445 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 3, drawn 2026-11-01 after architecture 1
(the 13F holdings carry, failed the portal's determinism block) and architecture 2 (the heat deaths integrated from the
register and the medical examiners' logs, sent back at its stage 4 judge on Gate H3): a new world, dataset and shell.
The Arafura Examinations Board, a not-for-profit board in Darwin, sets and marks the Arafura Senior Certificate for
schools across Australia, the Pacific and South-East Asia. Its History Paper 2 has a compulsory Section A (source
analysis, 40 marks) and a Section B in which candidates answer two of three optional essay questions (25 marks each);
the board marks every essay a candidate writes and credits the best two. Before the 2026 results are certified, its
code of practice asks whether an optional question was more demanding than the others for the paper's candidates and,
if it was by a mark and a half or more, raises that question's marks by the difference, to the nearest whole mark,
before the best answers are credited and the grade boundaries are applied. The question is whether Question 6 is
scaled, and by how many marks.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task445.json` (architecture v3, lineage v1 and v2 spent), registered
  2026-11-01T00:50:34Z after a fetch of main: WARN only. A first draft read BLOCK on five axes and was redrawn, never
  relabelled: the context artifact (task145's monitoring export, then task231's operations log; the board's marking
  close-out summary is what the executive reads), the forum (task231's committee; the board's executive certifies the
  results), the forcing event (task146's meeting; the results are certified to the admissions centres on a fixed
  date) and the structural signature (decisive gap, pattern and Gate G against older builds, each differentiated on
  the card in one line: no assignment, no follow-up, no reference group, no sampling design, the comparison is the
  units that chose nothing). WARNs: first names in older builds (Mary), Gate G and question form against
  task231, decision type against task146, each answered in `## Pre-ship check`.
- **Pairing:** Education & Learning Sciences, task type `item-response-theory-test-equating`, which serves ETL: the
  board's marking export (one row per marking event), the Section A scanning extract, the entries register and the
  centres register are conformed into one result per candidate on a scale on which marks earned on different chosen
  questions mean the same, and the scaling decision is read off that conformation. The slot's education ground is the
  only ETL client domain it has left (quantitative finance and general statistics are spent here, and the batch's
  other ETL domains carry this week's builds), and task464's enumeration recorded the cell's estimated quantities
  closed: this draw takes the one property it did not reach, a question's demand when the candidates choose their
  questions.
- **Strategy:** `population_selection`: the population that measures a question's demand without the choice in it is
  the candidates who answered every optional question; every chooser comparison carries the choice. Not
  composition_mix (no rate is fixed within a mix), not causal_design (nothing is assigned), not
  grain_or_unit (the unit, a candidate's marks, is filed).
- **Data-native sentence:** candidates choose their essays by the topics they know, so the few who attempt the
  question that looks hardest are the ones who know its topic best; their marks on it, and on it beside their other
  essay, carry that knowledge, while the candidates who wrote all three essays (the board marks every essay and
  credits the best two) chose nothing, and their own three marks show how demanding each question was.
- **Abstraction sentence:** a property of one option is read from the units that took it, and each unit took the
  options it holds a private advantage on, so the option's takers misstate it however they are compared, and the
  units that took every option are the comparison with no choice in it. No approved or delivered build on file reads
  this way: task238 identifies a channel's effect through a randomised nudge, task267 weights a two-phase check,
  task473 completes positives an observer noticed, task474 links two papers through candidates who sat both.
- **The decision and the quantity:** whether Question 6's marks are raised before the grade boundaries are applied,
  and by how many whole marks, decided by Question 6's demand against the other optional questions for the paper's
  candidates, a mark and a half the code's line.
- **Sources, one line each (all synthetic, shaped on public senior-certificate examining practice; the board, its
  schools and people are fictional):** the essay marking export for 2026 (the spine, one row per marking event, UTC);
  the Section A extract from the scanning system; the entries register; the centres register; the code of practice
  (PDF); the executive's request (email); for the asks, the 2025 post-results reviews log; distractors, the
  teachers' predicted grades and the 2025 paper's question statistics.

## Default path

1. Conform the marking export: one final mark per candidate and essay (a senior examiner's re-mark stands), absent
   candidates set aside, the merged Queensland centres' old codes read through the centres register.
2. Read each optional question's demand the way the field compares questions on a paper: each question's marks
   against the others' for the candidates who answered it, first as question means (Question 6 0.53 marks harder than
   Questions 4 and 5 together), then adjusted for Section A, the paper's common measure of attainment (0.51), then
   inside the candidates who answered it beside another essay, each candidate's own pair (0.50).
3. Every route puts Question 6 about half a mark harder, under the code's line of 1.5, so no optional question is
   scaled; credit each candidate's best two essays and apply the committee's boundaries.

Ends on: no optional question scaled (Question 6 about 0.5 marks more demanding than the others, under 1.5).
Golden: Question 6 raised by 2 marks before crediting and grading (2.09 marks more demanding among the 1,422
candidates who wrote all three essays).

## Stump sentence

The default path reads Question 6's demand from the candidates who chose it, by its mean, by a Section A adjustment
or by each two-essay candidate's own pair, finds it about half a mark harder and scales nothing; the candidates who
chose Question 6 knew its topic, so every comparison among its choosers carries that knowledge, and the 1,422
candidates who wrote all three essays, who chose nothing, put it 2.09 marks harder, so its marks are raised by 2.

## Three rules

- Task type: item-response-theory-test-equating (Education & Learning Sciences), which serves ETL: the marking export,
  the Section A scan, the entries register and the centres register are conformed into one result per candidate on
  a scale on which marks earned on different chosen essays mean the same, and the scaling is read off that
  conformation.
- Domain test: the deciding quantity is an optional question's demand for the paper's candidates, the examinee-choice
  problem of test equating, which makes marks earned on different questions comparable before one set of grade
  boundaries is applied to them; the swap fails because wards or library loans have no rubric choice, no topic a
  person chooses by and no marking of every attempt.
- Swap: "should the essay its candidates find hardest have its marks raised" with wards for questions and bed-days
  for marks becomes "should the ward its patients find hardest have its scores raised", and choosing one's essays by
  the topics one knows, a rubric that credits the best two and an examiner marking every essay written stop making
  sense.
- Layer 1: the marking export one row per marking event in UTC, a senior examiner's re-mark a later row for the same
  essay; absent candidates as one row with no mark; the merged Queensland centres under their pre-merger codes; a
  moved candidate's essay booklet under the number and centre it was printed with while the Section A sheet and the
  entry carry the later ones; candidates who wrote no essay present only in the Section A scan; Section A under the
  scanning system's own item codes; the entries register's dates as day, month, year. Each is what those systems
  produce, and none carries the call.
- Layer 2: identification under self-selection: each essay's takers chose it by their knowledge of its topic, so the
  marks of its takers estimate its demand only for candidates who knew its topic, and the comparison that removes the
  choice is the candidates who took every option.
- Decisive step: recognise that the candidates who chose Question 6 knew its topic, so no comparison among choosers
  reads its demand, and read it from the candidates who wrote all three essays, whose own three marks carry no choice.
- Not semantics: every field can be read correctly (each mark, the credited flag, the marking event, each centre code
  and its region, each entry and its earlier number) and the chooser routes still file no scaling, because no field
  holds a candidate's knowledge of a topic: it shows only as the gap between what the choosers and the candidates who
  chose nothing show.
- Not rule application: the code files what demand is (what the paper's candidates would have earned on a question
  against the others taken together) and the line and the rounding, and no rule says whose marks measure it; the
  enumerated family (question means 0.53, a Section A adjustment 0.51, each candidate's pair 0.50, the credited answers
  alone 0.52, the candidates who wrote all three 2.09 and its forms 1.85 to 2.33) spreads from 0.50 to 2.33, the
  standing family once the choice is recognised is the all-three route in each of its forms, 1.85 to 2.33, every one
  raising Question 6 by 2, and the ruling-out is quiet: no column or sentence marks the choosers' advantage, only the
  gap between their differences and those of the candidates who wrote everything.
- Analyst test: a strong analyst who conforms the marking export, joins the moved candidates, reads the code correctly
  and compares each optional question's marks with the others for the candidates who answered it (means, a Section A
  adjustment, each candidate's own pair) puts Question 6 about half a mark harder and files no scaling (the default
  path's Ends on: no optional question scaled); candidates chose Question 6 by knowing its topic, and the candidates
  who wrote all three essays put it 2.09 marks harder, so it is raised by 2.
- Estimand: the code of practice files it in sections 4.2 and 4.3: an optional question is more demanding when the
  paper's candidates would have earned fewer marks on it than on the others taken together, measured in marks, and
  one more demanding by 1.5 or more is raised by the difference to the nearest whole mark, no mark above the
  question's maximum, before the best answers are credited and the boundaries applied.
- No decoy: nothing is planted to be caught; no memo, quote, minute or earlier figure states a question's demand or a
  scaling, the 2025 question statistics are last year's paper (a named distractor), and every file is what the board,
  its scanning system and its marking system keep for their own reasons.
- No certified replay: no certified or published figure blesses a chooser route; the minute sets boundaries, not
  demand, and no file carries a corpus of past scaling decisions to reproduce.
- Lesson: a model learns that the takers of an optional item chose it by an advantage on it, so their marks, adjusted
  or paired, measure the item only for those who chose it, and that the units who took every option are the
  comparison with the choice taken out; no build on file reads an option's property from the units that declined to
  choose.

## Survivor anatomy

- Actor: a candidate's knowledge of an essay's topic has no column in any file; the marking export carries marks, the
  credited flag and the marking event, and the topics are only the questions' numbers.
- Link: the choosers' advantage is read only by setting the candidates who wrote all three essays against those who
  chose two, a comparison between two groups of the same export that no key, column or sentence invites; the code's
  rubric clause credits the best two essays and says nothing of measuring with the third.
- Reflex: the field's way to compare questions on a paper, question means and then an adjustment for the paper's
  common section (and the within-candidate pair a careful analyst adds), sits at rungs 0 to 2 and files no scaling,
  the default path's Ends on.
- Back-test: the textbook route validates: on Questions 4 and 5, which most candidates chose (about 85 per cent each),
  the Section A adjustment and the pairs agree with the all-three candidates' difference to a tenth of a mark, so the
  method checks out on the questions where choice barely selects.
- Second use: the third essays are in the export because the board marks every essay written and credits the best
  two (code 3.1 and 3.2); the Section A scan grades every candidate; the entries register certifies every result; the
  centres register places every centre.
- Shock: Question 6's lower mean among its takers is about half a mark, the size of ordinary question-to-question
  variation (the 2025 paper's questions spread by more), and its smaller entry reads as an unpopular topic.
- Pins: the code files the WHAT at authority in the board's own genre (demand as the candidates' marks on a question
  against the others, the line, the rounding, the order of scaling and crediting), and no filed sentence names whose
  marks measure it, the third essays or a choice.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Second use | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 question means | code 4.2 names the marks on a question | the export's marks | the paper's question means | none | none | a difference of means | yes | readable |
| R1 a Section A adjustment | code 4.2's comparison | the scan's totals | adjusting for a common section | none | none | a regression | yes | readable |
| R2 each candidate's own pair | code 4.2 | candidate numbers | the within-candidate comparison | none | none | a mean of differences | yes | readable |
| R3 (decisive) the candidates who wrote all three essays | no sentence names whose marks measure demand or the third essays | the credited flag invites filtering the third essays out | the field compares choosers | no control refutes the choosers | the battery dedups, it does not group | a mean of differences on a group no rule names | yes, marked because the board marks every essay | silent |

## Semantic fork table

| SF | Term or convention | Readings | Ruled out by |
|---|---|---|---|
| SF1 | the mark that stands | the senior examiner's re-mark; the first mark | code 3.1; same call (asserted) |
| SF2 | who sat | every candidate present, an essay marked or Section A scanned; candidates with a marked essay | code 2.3 (present, whatever the candidate wrote); absent candidates not graded (asserted) |
| SF3 | the others taken together | the mean of the other two; either other question alone | code 4.2 (taken together); same call on each (asserted) |
| SF5 | the maximum | no raised mark above 25; uncapped | code 4.3; asserted |
| SF6 | the order of scaling and crediting | raise, then credit the best two; credit, then raise | code 4.3 (before the best answers are credited); the call is the scaling either way (asserted) |
| SF7 | the boundaries | the minute's, unmoved; moved with the scaling | code 5.2; no grade falls (asserted) |
| SF8 | a moved candidate | one result under the later number and centre; two half records | code 2.2; the register's earlier numbers join every booklet (asserted) |
| SF9 | a merged centre's region | the register's region under the old code; the code's letters | code 2.1; the old codes present (asserted) |
| SF12 | the answers that measure | every essay marked; the credited essays only | code 3.1 (every answer is marked); the credited essays alone file no scaling (asserted) |
| SF13 | a candidate who wrote no essay | sat, graded on Section A; not sat | code 2.3 and 5.1; present in the scan (asserted) |

## Ladder

| Rung | Route | Question 6 harder by | Call |
|---|---|---|---|
| R0 | the takers' question means | 0.53 | no scaling |
| R1 | a Section A adjustment of every answer | 0.51 | no scaling |
| R2 | each two-essay candidate's own pair | 0.50 | no scaling |
| R2b | the credited essays only (every third essay filtered out) | 0.52 | no scaling |
| R3 (decisive) | the 1,422 candidates who wrote all three essays | 2.09 | raised by 2 |

Every form of the decisive route raises Question 6 by 2: against Questions 4 and 5 together 2.09, against Question 4
alone 1.85, against Question 5 alone 2.33, on first marks 2.09, and 1.95, 2.48 and 1.90 for the candidates with low,
middle and high Section A marks; the clean truth gives 2.09 against 0.54, 0.51 and 0.51 for the chooser routes. The
pricing: the move must carry Question 6 across 1.5 from about 0.5 (a mark), and the candidates' topic knowledge carries
3.4 marks a standard deviation, chosen by about a third of the candidates for Question 6 against about 85 per cent for
the others, so the choosers' advantage is worth about 1.6 marks; the all-three group is 1,422 candidates, so the
difference's standard error is under a tenth of a mark; the decisive move is the largest and the only one that
reverses the call, and no single statistic sorts the questions to it.

## Closure table

| Axis | Reading in this build | Move |
|---|---|---|
| 1 Population | the paper's 2026 candidates, every candidate present | filed (code 2.3); SF2, SF13 |
| 2 Unit of account | marks on a question, a candidate's paper total | filed (code 4.2, 5.1) |
| 3 Attribution window | the 2026 examination | the export and the minute |
| 4 As-of dating | the request of 1 December 2026 | the email and the files' dates |
| 5 Version basis | the senior examiner's re-mark stands | filed (code 3.1); SF1 |
| 6 Denominator | the candidates whose marks measure demand | the design (the all-three candidates); asserted across forms |
| 7 Weighting | none: a mean over candidates | code 4.2 |
| 8 Window length | one examination | the export |
| 9 Boundary inclusivity | 1.5 or more is scaled | filed (code 4.3) |
| 10 Rounding path | the difference to the nearest whole mark | filed (code 4.3); C2 (mid-bin) |
| 11 Tie-break | none: one question over the line | C1 |
| 12 Maturity and censoring | marking closed; every essay marked | the email; the export |
| 13 Order of operations | conform, measure, raise, credit, total, grade | filed (code 4.3, 5.1); SF6 |
| 14 Row order | none: keyed by candidate and question | C1 |
| 15 Duplicate resolution | one mark per candidate and essay, the later event | SF1 |
| 16 Identity normalisation | a booklet's earlier number to the later entry; merged centres' old codes | filed (code 2.1, 2.2); SF8, SF9 |
| 17 Netting against gross | none | none |
| 18 Dimensional units | marks out of 25 and 40; totals out of 90 | the minute |
| 19 Code and status semantics | MARKED and ABSENT; FIRST and SENIOR; the credited flag | the export's own codes; SF12 |
| 20 Integerisation | whole marks throughout; the raise a whole mark | filed (code 4.3) |
| 21 Clause scope | optional questions only; no mark lowered | filed (code 4.1, 4.3) |
| 22 Forward window contents | the results certified on 14 December 2026 | the email |

## Literal reader

Executed word for word, the code files the population (every candidate present for the paper), each essay's mark
(the senior examiner's re-mark standing), what demand is (the marks the paper's candidates would have earned on a
question against the others taken together), the line (1.5 marks or more), the raise (the difference to the nearest
whole mark, no mark above 25), the order (raise, then credit the best two, then apply the minute's boundaries) and one
result for each candidate under the later entry. What it leaves to the reader is whose marks measure the demand, which
no sentence says: every reading that measures it on the candidates who chose a question files no scaling, and the
reading that measures it on the candidates who wrote every essay raises Question 6 by 2 in every form. Each convention
the call needs is closed in the fork table and asserted in checks.py, and every step of the write-up executes as
written.

## Oracles

No shipped file ranks the questions or states a scaling: the minute sets boundaries, the 2025 statistics are last
year's questions, and the email names the files. The credited flag is the marking system's own rubric record; read as
the answers to measure, it filters out every third essay and falls back on the pairs, which agree with the choosers.
Nothing ties only under the golden.

## Ask sheet

One ask on the board's entries, read through files the main call reads for other reasons, on records whose join no row
labels.

**Ask A, candidates who sat Paper 2 and answers to each optional question, by region (24 figures).**
- Files: the marking export, the Section A scan, the entries register and the centres register.
- Primary (whose records are one candidate, across two systems): a moved candidate's essay booklet keeps the number
  and centre it was printed with, while the Section A sheet and the entry carry the later number and centre, so the
  export places 160 candidates' essays at their earlier centres under withdrawn numbers; the register's earlier numbers
  join them, and code 2.2 puts each at the later centre.
- Secondary (who sat, across two systems): 195 candidates wrote no essay and appear only in the Section A scan, so a
  count from the marking export loses them; code 2.3 counts every candidate present.
- Hazards: merged centres under their old codes (the register's merged_from), senior re-marks as second rows, absent
  candidates as rows with no mark, every essay written counted whether credited or not.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Mirror (stops at R0) | Verdict |
|---|---|---|---|
| A, 24 regional figures | counts the candidates and essays in the marking export with every filed rule, so the moved candidates sit at their earlier centres and the no-essay candidates are lost | reads a centre's region off its code's letters and counts every row | miss |

Cracker: misses all 24 ask figures; mirror keeps 0 of 24.
Pair ceiling: 28.5
Mirror leakage: 0.0
Measured by: task445/generator/ceiling.py on target.zip 51f94b0e

## Leak sweep

`leak.py --asof 2026-12-01` on the final cut (target.zip 51f94b0e): REVIEW, no LEAK. A first cut read LEAK on the word
"rubric" in the code's crediting clause (sweep 2), reworded to "the paper's instructions". Each REVIEW line, ruled:

- Sweep 3, the code of practice carries most words of the committed call (raise, marks, before the best two essays
  are credited, the boundaries applied): harmless. They are sections 4.2 and 4.3's own rule, which the call executes;
  no sentence says whether any question is more demanding or is scaled.
- Sweep 4, stump-paragraph nouns in the code (marking, section, register, demand, option, choice): harmless. They are
  the code's own nouns for its marking, entries and optional questions; "choice" is "every paper that offers a choice"
  in section 4.1, and no sentence says how candidates choose or whose marks measure demand.
- Sweep 4, the minute (section, essays, option): harmless. It sets the boundaries and notes that Research and Standards
  will report under section 4, judging no question.
- Sweep 6 (INFO), the centres register names regions beside codes: it is the board's register and ranks nothing.

## Pre-ship check

- WARNs answered: the first name Mary appears in an older build as one person (the guard's names
  for this seed); Gate G method_or_model_selection and the whether question form against task231, and dial_setting
  against task146, are different mechanisms in different domains, the decision a scaling dial.

## Tried and rejected

- Seed ET02 as written (amendment-type supersession and filing-date value units deciding the flag):
  rule application and data semantics as the decisive step, banned; kept as Layer 1 on the asks.
- A top-holder ask with every manager in contention, including index sponsors still to file: the top
  holder would be unknowable at the extract; the large early complexes are made the top holders and every
  pending manager's carried value is asserted under 80 per cent of the top.
- The issuer-level completion factor as a rigorous variant: once the September window carried one-off
  lateness (January reports, a 10 November original) it stopped converging, so it is a wrong rung (R4),
  refuted by the June-to-September back-test.
- Whole-percent December ownership to absorb estimator spread: dropped; the back-test selects the
  holder-level construction and every graded figure is held at one decimal.
- Portal round 1 (author's report 2026-10-11): rubric average 52 (top responses passed the bridge end
  557,031,720 and the restated-reports bar -16,011,685; in-house round 1 had every September figure, every
  December count and every top holder); Determinism QC failed (A pass, B C D fail, E pass, F plausible, G
  unsure; answer_contradicts_files, golden_wrong): OM-4 s.2 counted the managers that "file" for the period
  and filed no completion, so the literal reading flags WHII and JEMS from the reports on file, and the
  count of managers to carry (128 against 125) and the carry basis were unpinned. Filing the completion
  method itself would make the decisive step rule application and hand the call over; loop 1 files the
  estimand and a basis-selection criterion instead and moves the stump to the basis.
- task181 collision (task446's pre-flight, 2026-10-11): the shipped driver ("complete reporter by reporter
  from each one's last report, not one aggregate completion share") shared the decisive gap, G12, the
  calibration form and the stump strategy with task181 ("the complete count each unit's own arrival history
  implies, not an arrival speed pooled across units"); replaced by a different claim (the last report is
  stale for the filer class that drifts), stump strategy `forecast_method_backtest`, decisive pattern E.
- Flat carry as the golden: with the estimand filed literally it is the natural method and every solver
  reaches it; it is the stump rung now.
- Ask devices on hosts whose September filings fall after 3 November (the brief's placement): a
  mishandling that removes September lines (a failed CUSIP dropped, latest-accession-wins on a new-holdings
  host) then lowers only the back-test's final figure, shifts every basis's miss upward and can hand the
  selection to flat carry; every September device host files all its September reports by 3 November
  instead, so every mishandling cancels between the day-34 estimate and the final figure.
- The three September reports filed in January and NH's 10 November original: any mishandling that drops
  them (one data set only, latest accession wins) lowers only the back-test's final figure by 2 to 3 points
  and hands the selection to flat carry; removed, NH re-homed and re-timed.
- Optional A4 as proposed (a market maker's December option lines worth more than the largest holder's
  stock): counting them in ownership moves on-file December by several points on those names, so the main
  call's own option filter becomes load-bearing on a device, and the option family repeats A2; replaced by
  the top holder's rename on its December cover page.
- Active types left to drift (scratch prototype): per-type changes of -9 to +26 per cent on the twelve
  names, and the type-change completion then sits up to 1.5 points from the index-only version; fixed by
  holding every active type flat in aggregate.
- OTF as the only name near the line (prototype): one rate for every manager still due (3.3 per cent or
  more) then lands the golden set; FENN is placed at 79.6 with multi-strategy funds still due, so no single
  rate gives both.
- Attrition (four advisers that file September and never December): under the literal estimand they are
  still due and estimated, and in a back-test window a June filer that never files September has no final
  figure; removed, the register's inactive rows are managers absent from all three drops.
- Mean of per-manager ratios with position turnover alone (builder, 2026-10-11): the per-manager ratios
  average back to the pooled change and the basis missed the September window by only 0.30 to 0.38, under
  the 0.6 target; fixed with manager-level book flows (1.171).
- FENN's multi-strategy holdings still due at 14 per cent (builder): one rate crosses the line on FENN at 3.02
  per cent and on OTF at 3.24, 0.22 apart against the 0.3 the design asserts; moved to 16 per cent (2.66
  against 3.24).
- Late active filers moving 1.0 per cent a position (builder): own-trend carry put GLI at 84.33 against the
  golden's 84.39, across the bin edge; 0.7 per cent and GLI's target at 84.43 keep both in 84.4.
- Device sizes drawn freely inside the design's ranges (builder): SAF's COM-only drop (-0.36) and its October
  count (+0.36) cancelled to 0.005, and A2 kept with COM-only and keyed dropped left the bridge end 21,178
  shares from the golden; sizes now come from a search asserting every combination clears 0.06 points and
  100,000 shares.
- Loop 1 asks as device-carried lookups (September counts and ownership, top holders, the September bridge, devices A1 to A5), round 2, 2026-10-11: the solver missed the call at the designed rung but landed every one of these figures; each device was a work order an OM-4 rule points at (s.3, s.4, s.5, the cover-page amendment fields, the December cover-page name). Proxy 45.1 with the call missed. The ask layer is rebuilt on the decisive construction's outputs.
- Round 2's leak in the spec's terms (2026-10-11): every ask device was adjudicated by a filed rule on its own path (OM-4 s.3 options, s.4 check digit, s.5 latest count, the readme's amendment types, Wexley's cover note, the layout's cover-page name pin), so the careful path executed each as a work order; and the plan recorded with round 2, rebuilding the asks on the decisive construction's outputs, is rejected too (keyed to the construction, ban 4: the cracker banks it). The December share counts and the top holder are dropped as graded asks because no silent device fits them (December twelve-name lines stay clean, VALUE is fixed by the readme's filing-date rule and s.6, the holder's name needs a pin); the layer moves to the September figures the criterion runs against, on two devices no filed sentence speaks to (same-day amendments ordered by number, a restatement's header period).
- Ordinary same-day pairs as June restatements filed with the September original (builder, ask layer, 2026-10-11): an identical June restatement dated in October moves the department's June lines past the June window's day 34, so the issuer-level rival's back-test miss moved from 2.894 to 3.127 and the main-call identity assertion failed; replaced by three September re-filings in full on the original's day, which move no share, no date and no main-call figure.
- The ask sheet's full-grid floor of 3.0 million shares on the bridge end (builder): unreachable, since A2 kept alone moves the end 2.1 million and the negative hazards sum to 3.4 million; asserted on the stops instead, with every grid cell's end different from the golden (closest 12,431 shares).
- Loop 1 main call (completion by register-type change pooled across names), round 3, 2026-10-11: the solver tested five bases in OM-4 s.2's back-test (none, carry, per-security ratio, pooled ratio, type-pooled ratio) and landed the call on the type-pooled ratio (0.042 pp); round 2's solver had stopped at carry. The ask layer held (ask share 18 per cent, 0 of 4 items). Loop 2 deepens the decisive step past the type-pooled basis.
- Loop 2 with the sponsors' stakes held constant (no creations) and only each name's share count moving, the first
  form considered (prototype, 2026-10-12): the sponsors' change pooled across the names then sits at the
  share-weighted mean count move (about 1.00), so the type-pooled basis collapses onto flat carry, the register-type
  signal that drew round 3 to it disappears, and the default path no longer ends on the type-pooled answer; the
  creations stay at 5.5 per cent, so the golden's stake formulation grows the September stake by the filed sponsors'
  stake change.
- The type by name change for every type as the golden's second formulation beside the stake carry: the active
  types' per-name changes are noisy by construction and the grid misses the back-test by 11.0, and making them converge
  would turn the decisive step into the reflex "condition on every visible attribute" (readability test 3); the
  per-name change is the golden for the sponsors only, and the full grid is an R4c rival.
- Creations at 3.5 per cent to retire the realism debt (prototype): the sponsors' stake without growth becomes the
  closest rival (0.77, ahead of the type-pooled change at 0.82) with OTF 0.39 under the line; kept at 5.5.
- Share-count moves on OTF, FENN, GLI and SAF only (prototype): the type-pooled rung then kept the golden's one-decimal
  December figure on eight of twelve names, so a response stopping there banks most of the December figures; buybacks
  and at-the-market issuance spread across the watchlist in both windows cut that to three (GLI, FENN, HAMR) without
  moving the back-test (the type-pooled change 0.66, the golden 0.04).
- An accelerated repurchase on HAMR in the December window: HAMR's August offering (A5) makes a buyback in the next
  quarter implausible; the December-window buybacks sit on WHII, AMRB, JEMS and NOPR.
- GLI's December target at 84.43 (loop 2 build): the golden sat at 84.424, 0.026 under the 84.45 edge, and the judge's pass 3 (2026-10-12) found the near-argmin family (peers read as every December filer, other types mixed carry and pool, best miss 0.0402 against the golden's 0.0408) at 84.452, which rounds to 84.5; the target moved to 84.39 (family 84.384 to 84.414) with HAMR's December target at 55.22 to hold its September slack at 52.479, and SF14 asserts the family.
- The bridge asked as "one bar for each item between the two totals" (judge pass 3): 435,800 option shares sit inside replaced reports, so replaced-first and options-first both tie to the end total with different first two bars, and the matched-back bar could be split three ways by kind of mis-keying; the prompt now names the three bars and their order (SF15), and the stakes clause about never reissuing a file came out to keep it under 1,000 characters.
- Architecture 1 itself (the 13F holdings carry, quantitative finance): the portal's determinism block failed it
  (answer_contradicts_files: OM-4 section 2 named the filers for the period and filed no completion, so a literal
  reading flagged WHII and JEMS, and the 128 against 125 managers to carry was unpinned), and this session's batch
  audit found it short of the survivor anatomy (its decisive basis was a filed criterion's selection, not a link no
  key invites); re-rooted rather than repaired, so the portal sees one strong build.
- Architecture 2's first draw, coroner-held registrations completing a provisional count in
  census-register-administrative-data-quality as a designation set for a statistics office with a funder as the
  forum (2026-10-31, at the draw, never registered): its card axes sat on task485's (the same subdomain, objective,
  strategy, decision type and organisation family, a provisional register count completed for a period still
  maturing), and by the time it was ready to register its forum (funder_or_donor) and shape (01) repeated the last
  three builds; the world and the decisive step kept, the build moved to official time series production, an
  allocation, an NHS board and its panel.
- A repeat-homelessness draw (2026-10-31, at the draw, never registered): eight councils' case records linked
  across councils on the applicant's name and birth date, where households housed out of district come back on the
  host council's file. It died on the analyst test: once the grant letter files that a duty owed by any housing
  authority counts, which determinism needs, a strong analyst who reads it correctly links the councils' records and
  lands the golden, so the decisive step was reading the scope, with no textbook estimate a careful reader would
  prefer to the link.
- The draw as first registered (2026-10-31T22:45:01Z, pushed in 9b6e0799): survey-research-official-statistics with
  seasonal-adjustment-official-time-series-production, shape 05 (an allocation of GBP 2.4 million on each place's
  excess), the board's Heat Resilience Panel as forum and a programme officer as the role. task468 v5 had registered
  the same pairing, subdomain, shape, forum, role and decision type eight minutes earlier on another branch, so on
  main the card took six bans; the same world and decisive step were redrawn onto data integration, a scorecard
  designation, the board itself and a policy adviser, with gap time and pattern G3, because every honest (population,
  G12) and (population, G3) signature with a designation was already spent five or more times.
- A data-notes PDF in the pack (2026-10-31, at the leak sweep): a page describing every field of the three mortality
  extracts, written to close the version, timestamp and certification forks; sweep 12 found 49 of the extracts'
  column names in it verbatim (a describing file, LEAK). Removed; each fork it closed is closed by the terms or by the
  rows themselves, and the board's care home list joined the pack as its tenth file.
- Ask C with one device (the correction's date read as the registration's): the full includer, reading version 1 for
  every field, kept all 24 figures (pair stress row 86.2); the districts' 2026 review of care home residents
  registered at a family address in another place was added as a second device, so the entry as it now stands takes
  its address from version 2 and its date from version 1, and the full includer keeps 8 of 32.
- Ashwold with 34 heat-wave deaths held for inquest (build, 2026-10-31): its completed excess, 7.4 per cent, made the
  golden set the top three of the completed register's sort, an interval; at 40 held deaths it is fifth of six (6.3).
- Architecture 2 (NHS Ellesmoor ICB's 2027 heat resilience grants, the summer's deaths integrated from the register and
  the two medical examiner offices' logs) dead at its stage 4 judge, 2026-11-01: NOT_DETERMINISTIC with SOLUTION_WRONG,
  SEND_BACK. Gate H3 failed: the fund's terms counted every death "whether or not it has been registered", so matching
  the logs to the register executed the filed rule and nothing was left to decide, and the gross-up by earlier
  summers' registered share contradicted that sentence, so no strong reader files it; supplementary 5 rode an unfiled
  version convention (the latest fields with version 1's registration date); the recommendation prose contradicted
  itself on Ashwold. A SEND_BACK re-roots (report kept as determinism_check_report_arch2.md).
- Architecture 3 draw, 2026-11-01, the strand-weighted anchor (a paper's common questions mostly number, a cohort
  that gained on geometry under a new syllabus, the drift screen dropping the geometry anchors as drifted), measured
  on a two-strand Rasch prototype: chained linear equating per strand set the boundary at 35 against the generator's
  truth of 33 and an anchor reweighted to the blueprint at 34, because a four-question geometry anchor is too short for
  observed-score chaining, so the strand-aware family split by two marks; the anchor's representativeness and its
  length are one dial (Gate C), dead before data was cut.
- Architecture 3 draw: the estimated quantities of item-response-theory-test-equating recorded closed at task464
  architecture 4 (a scale or instrument property reopens the estimator family, a precision is a variance, a reported
  outcome is a certified function, a process fact is a key or a stated rule); the draw stays in education, the one ETL
  client domain the slot has left, and takes the property that enumeration did not reach: an optional question's
  demand when the candidates choose their questions.
- Optional questions compared within the centres that taught every topic (a centre grouping): refused on paper,
  stumping 1.1c (a grouping is a reflex or a fork).
- Optional questions compared through two spiralled booklet versions as an instrument (the versions' difference over
  the choosers' share): refused on paper, offering a different question moves the other questions' choosers too, so
  the exclusion fails and the family forks.
- A pretest of every optional question on a trial sample with no choice: refused on paper, a helper organ the opponent
  reads first, and its motivation differs from the live paper's.
