# task482 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 17, drawn 2026-11-07 after architectures 1
to 16 were spent: a new client domain, world, dataset and shell. The Corlinn Schools Assessment Trust, owned by its
member independent schools across New Zealand, sets one Year 10 science paper each year (the Year 10 Science
Benchmark) and reports every candidate against its Achieved standard. Its Rasch item bank was calibrated on the August
2026 sitting, held in weeks 3 to 5 of Term 3, when every member school was part-way through the course outline's two
Term 3 units (forces and motion; Earth's systems) on its own scheme of work. The Trust's council has moved the 2027
sitting to November, after every school has finished every unit. The assessment committee must choose which of three
draft papers to print; the paper specification files the choice: the draft whose expected mark at the Achieved
standard sits nearest 25 of its 50 marks.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task482.json` (architecture v17; lineage v1 to v16 spent, v16 moved in
  with its fate and shell), registered 2026-11-07 after a fetch of main and of the second line's cards
  (claude/jolly-hypatia-06c61h, copied untracked for each run and deleted after). The last act of stage 1, `check` on
  the registered card: WARN only (Paul appears in one older build, task117; the which question form repeats task127's,
  the decision being a pick among three). A first draft read BLOCK and was redrawn, never relabelled: the decisive gap
  and pattern (population with G6) repeat thirteen older builds, so the decisive gap is time (the calibration is a
  mid-year sitting, the decision a year-end one) with G13 leading, which is the honester reading of what moves; Gate G
  is etl_conformance (the conformed difficulties judged against the paper specification, a contract); the shell was
  still v16's (read off the old prompt) and is redrawn with the world. The remaining older-build signature (time, G13,
  a pick) is differentiated on the card against task122 v2, task194 v3 and task501 v4. The window when drawn: task214,
  task268 and task127 (decomposition_attribution, population_selection and causal_design banned; composition_mix free
  again since task212 left it).
- **Pairing:** Education & Learning Sciences, task type `item-response-theory-test-equating`, which serves ETL. The
  August 2026 response export, its session log, the bank and its 2025 renumbering, each school's scheme of work and the
  three drafts are conformed into one table of the difficulty each draft item will have in November 2027 and each
  draft's expected Achieved mark, from which the pick is read. The slot's two earlier equating architectures (v6, a
  community college's mathematics placement form and its items' field-test positions; v11, plausible values by school)
  are other worlds and other drivers.
- **Strategy:** `composition_mix`: each Term 3 item's banked difficulty is a mix of the responses whose takers had
  finished the unit and those who had not, and the November 2027 sitting is all of the first kind; the property is
  rebuilt for each response from its student's sitting day against its own school's scheme of work, never read off a
  column. Not grain_or_unit (the unit, a draft's expected mark, is filed), not time_semantics (no clock is misread),
  not maturity_censoring (nothing is still arriving).
- **Data-native sentence:** the bank's Term 3 items were calibrated at a sitting held in weeks 3 to 5 of the national
  Term 3, while each member school's own sequence ends its first Term 3 unit in week 4 or 5 of its own term, 1 to 7
  school days after its first sitting day, and its second at the end of term; about nine in ten responses to those
  items came from candidates whose school had not yet finished the unit, and the November 2027 sitting follows every
  school's last unit.
- **ETL pincer (guide-to-prompt 1):** the forcing file pins a condition per response (taught or not when given), read
  off the session log against the course review's appendix; reading it correctly is not sufficient, because the call
  moves only when each Term 3 item is re-estimated on the taught responses with abilities held on the Term 1 and 2
  items and the drafts are pre-equated again, an estimation step no field or rule performs.
- **Abstraction sentence:** a calibrated parameter carried to a coming administration whose takers will all have been
  taught what many of the calibration's takers had not, the state set for each taker by their own institution's
  teaching calendar against the day they took it. No approved or delivered build on file reads this way: v6 carried
  items to new positions by a position term read off a column; task474 measured a retest gain on repeaters; task450
  linked through carried-over items; task445 read a choice advantage among optional questions.
- **The decision and the quantity:** which draft (A, B or C) the committee prints for November 2027, decided by each
  draft's expected mark at the Achieved standard under the Rasch model, the specification picking the draft nearest 25.
- **Sources (all synthetic, shaped on New Zealand Year 10 science practice and Rasch pre-equating; the Trust, the schools
  and the people are fictional):** the August 2026 response export (the spine, one row per scored response, about
  259,000 rows); the session log (each sitting, UTC, with dropped and resumed sessions); the item bank (the final 2026
  run's difficulties, unit, strand, anchor flag and fit); the calibration runs (2025 final, 2026 preliminary and
  final); the 2025 renumbering; the three drafts (item card numbers); the paper specification; the standard-setting
  record (the Achieved ability on the bank scale); the council's minute fixing the November 2027 dates; the 2026 course
  review (the course outline's units, strands and terms, and its appendix of member schools' Year 10 science
  sequences as returned, in each school's own words and term weeks); the member schools list; the request email; for
  the asks, the entries register, the make-up roster and the office's keyed make-up scripts; distractors, the 2026
  candidate survey of attitudes to science and the schools' bell schedules.
- **Shell WARN answered:** voice-check holds the which question form at 37 per cent of prompts against a 30 per cent
  cap; the decision is a pick among drafts, so the form follows the decision, and the shell is varied at the role
  level instead: the question carries the specification's rule in its own clause, and the workbook carries both asks
  beside the working, with no side table or count-once sheet.
- **People (guard.py names, en_NZ, seed 482):** Paul Shailer, head of assessment (asks for the recommendation); Theo
  Stevens, chair of the assessment committee; Jeremy York, the Trust's psychometrician (keeps the bank).

### The six go/no-go screens (`generator/screens.py`, 20 redraws, and `generator/checks.py` on the shipped seed)

The item pool and the drafts are held fixed (140 items on four 2026 forms of 50, a 20-item anchor block from the Term 1
and 2 units on every form; the drafts composed to taught expected Achieved marks A 26.0, B 23.0, C 25.0 with 6, 11 and
17 Term 3 items); each redraw re-draws the 48 schools' term starts, Term 3 sequences and sitting days, about 5,200
online candidates and their responses: each school sits over 6 to 9 school days of the 15-day window, its first Term 3
unit ends on a Friday 1 to 7 school days after its first sitting day (week 4 or 5 of its own term) and its second at
its term end; a response to a unit not yet taught is harder by about 1.0 logit, item by item (0.6 to 1.3); the
Achieved standard sits at 0.35 logits; about 11 per cent of the Term 3 responses were taught (shipped seed 10.8).

1. **Levels and the lever.** Golden marks A 25.94, B 22.81, C 24.90 over the redraws (shipped seed A 25.89, B 23.02, C 24.80); the golden
   picks C in 20 of 20, with C 0.20 from 25 at the shipped seed against A's 0.89. Levels: the untaught effect
   of about 1.0 logit sits inside the item-level instructional sensitivity reported for content not yet taught
   (Polikoff 2010, Educational Measurement: Issues and Practice 29(4)); Rasch fit norms (Wright and Linacre 1994, Rasch
   Measurement Transactions 8(3): 0.8 to 1.2 for high-stakes and 0.7 to 1.3 for run-of-the-mill multiple-choice
   tests); true-score pre-equating from a calibrated bank (Kolen and Brennan, Test Equating, Scaling, and Linking, 3rd
   ed., 2014). Every graded figure sits at least a quarter of a mark from a rounding edge, asserted in checks.py.
2. **The golden's own method holds.** Taught counted from the unit's last day or 2 or 4 days after it, the sitting day
   read in UTC, Warm's estimates for abilities, a joint recalibration dropping the untaught responses, and one taught
   shift shared by every Term 3 item: each picks C in 20 of 20 but the 4-day lag, 19 of 20 as it drops every Monday
   sitter (lag2 C 24.90; lag4 C 24.88; utc_day C 24.90; wle C 24.88; joint C 24.88; one_shift C 24.89), and, at the shipped seed, each puts every draft
   on the golden's whole mark.
3. **The first look lands wrong** in 20 of 20: the bank's difficulties pick A in 20 (marks A 24.83, B 20.62, C 21.71; shipped seed
   A 24.78, B 20.64, C 21.58).
4. **The careful readers land wrong**, over the 20 redraws: (a) the field-decomposing reader (true-score pre-equating
   on the bank after an anchor drift screen and item fit, all clean) is the bank, A; (b) the constructing readers: the
   last three days' sitters recalibrated pick A in 20 (A 25.13, B 21.15, C 22.54), the within-window trend carried to the window's
   last day picks A in 20 (A 25.15, B 21.21, C 22.59); (c) the per-record reader (school by item rates) has no all-taught cell to
   carry and returns the bank; (d) the mechanism-naming readers: the course outline's model weeks for every school
   leave no response taught and return the bank (A in 20), forces and motion taken as taught in the outline's
   fifth week picks A in 20 (A 24.99, B 20.90, C 22.17), whole schools that had finished a unit before sitting find none (no school's
   first unit ends before its first sitting day) and fall back to the bank, and each school's week numbers read against
   the national term calendar pick A in 19 and C in 1 (a Layer 1 misread below the decisive rung, ruled out
   by the appendix header); (e) the literal replay of every filed fact is the bank, A.
5. **Fit parity.** Under the bank calibration (shipped seed) the Term 3 items' infit (0.96 to 1.06, mean 1.00) sits
   inside the Term 1 and 2 items' range (0.95 to 1.08); every item's outfit sits inside 0.85 to 1.24, the one Term 3
   item over 1.2 ordinary in a 140-item multiple-choice bank; the anchor block's free 2026 estimates sit within 0.09
   logits of their banked values; the bank reproduces each 2026 form's observed mean mark; the Term 3 items' banked
   mean sits 0.20 logits above the Term 1 and 2 items'. The August 2025 and 2026 sittings share the same weeks, so the
   2025 run agrees with the 2026 run. No diagnostic a careful analyst runs points at the Term 3 items.
6. **Literal execution.** The specification, the standard-setting record, the bank's final run and the renumbering
   read word for word pre-equate on the banked difficulties and print A (asserted). No governing sentence (the
   specification, the record, the council's minute, the bank's notes) says which responses an item's difficulty rests
   on, when units are taught or whether candidates had been taught them: the specification files the candidates who
   sit the 2027 paper, the minute files only the November 2027 dates and an ordinary reason (results reaching families
   with end-of-year reports), and the course review's appendix is the curriculum committee's record of each school's
   sequence, from which it is read that every core unit ends before November.

## Default path

1. Conform the bank: map each draft's item card numbers to the bank's codes through the 2025 renumbering file, and take
   each item's final 2026 Rasch difficulty (the runs file's final run, not the preliminary one).
2. Read the Achieved ability on the bank scale from the standard-setting record (0.35 logits).
3. Pre-equate each draft by the test characteristic curve: the expected mark at the Achieved ability is the sum of its
   items' Rasch probabilities.
4. Check the bank the way the field does: the anchor block's drift (none), every item's infit and outfit (all inside
   0.7 to 1.3), and the 2026 forms' observed mean marks (reproduced).
5. Pick the draft whose expected mark sits nearest 25, compared before rounding.

Ends on: Paper A
Golden: Paper C

The default path's expected Achieved marks on the bank's difficulties are A 24.78, B 20.64 and C 21.58 at the shipped
seed (whole marks 25, 21, 22); the golden's, with the Term 3 items recalibrated on the taught responses, A 25.89, B
23.02 and C 24.80 (whole marks 26, 23, 25).

## Stump sentence

The default path pre-equates the three drafts from the bank's Rasch difficulties and prints Paper A, whose expected
Achieved mark sits nearest 25 of 50; the bank set the two Term 3 units' items on the August 2026 sitting, at which most
students' schools had not yet finished those units, which shows only when each student's sitting day is set against
their own school's scheme of work, and with those items recalibrated on the responses of students whose school had
finished the unit before they sat, Paper C is nearest.

## Three rules

- Task type: item-response-theory-test-equating (Education & Learning Sciences), which serves ETL: the August 2026
  response export, the session log, the bank and its renumbering, the schools' schemes of work and the three drafts are
  conformed into one table of each draft item's 2027 difficulty and each draft's expected Achieved mark, from which the
  pick is read.
- Domain test: the deciding quantity is each draft's expected mark at the Achieved ability under the Rasch model, the
  true-score pre-equating a testing programme runs from its bank; the decisive step is whether the banked difficulties
  hold for a sitting at which every candidate has been taught every unit (item parameter invariance across opportunity
  to learn). The swap fails: hospital forms or library loans have no item bank calibrated mid-way through a teaching
  sequence, no scheme of work, no sitting day.
- Swap: "which draft paper should the Trust print" with clinics for schools and questionnaires for papers becomes
  "which questionnaire should the clinics use", and the unit not yet taught, the scheme of work and the sitting day
  that decide it stop making sense.
- Layer 1: the bank renumbered its items in 2025 (the drafts list old numbers); the response export carries UTC times
  while schools sat on New Zealand school days; sessions that reconnected left duplicate response rows; each school's
  scheme of work is in its own format with units named in its own words; make-up sitters appear under the make-up
  centre's code; the bank history overlaps a preliminary and a final 2026 run. Each is what those systems produce, and
  none carries the call.
- Layer 2: estimation from the data's structure: each Term 3 item's banked difficulty mixes responses whose takers had
  and had not been taught its unit, and the coming sitting is all taught; the item has to be re-estimated on the taught
  responses, with abilities from the items every student had been taught.
- Decisive step: set each student's sitting day (the session log, in New Zealand time) against their own school's last
  day of each Term 3 unit (its scheme of work), recalibrate each Term 3 item on the responses of students whose school
  had finished its unit before they sat, abilities fixed on the Term 1 and 2 items, and pre-equate the drafts.
- No decoy: nothing is planted to be caught; no memo, earlier paper or published figure ranks the drafts; the bank's
  difficulties are the Trust's own calibration, correct for the sitting it was run on, and every file is what the
  Trust, its schools and its delivery platform keep for their own reasons.
- Not semantics: every field (each response's score, each session's time, each item's unit and difficulty, each scheme
  of work's weeks, every specification sentence) can be read correctly and the bank's difficulties still pick A,
  because no field holds whether a response was taught: the state exists only as each student's sitting day against
  their own school's calendar.
- Not rule application: the specification files what is chosen (the draft nearest 25 at the Achieved standard for the
  November 2027 sitting) and the standard-setting record files the Achieved ability; no rule or procedure says which
  responses an item's difficulty is estimated on, and the routes the files leave open (the bank as run, recalibration on
  late sitters, on whole schools, on the course outline's model weeks, on each response's own taught state) differ in
  the population behind each difficulty, which the data's structure decides.
- Analyst test: a strong analyst who conforms the renumbering, the UTC sessions and the duplicate rows, reads the
  specification correctly and pre-equates the drafts from the bank after a clean drift screen and clean item fit picks
  Paper A; the Term 3 items were calibrated on a sitting at which most students had not been taught them, and
  recalibrated on the taught responses Paper C is nearest.
- Estimand: the specification files it: the draft whose expected mark at the Achieved standard, for candidates sitting
  in November 2027, sits nearest 25 of 50, the expected mark being the Rasch model's at the Achieved ability on the
  bank's scale.
- No certified replay: no certified figure blesses the bank's route; the 2025 and 2026 sittings' own results agree with
  the bank because they were sat in the same weeks, which is what a sitting in November does not share.
- Lesson: a model learns that a bank's difficulties carry the teaching state of the sitting they were calibrated on,
  that a unit not yet taught makes its items look harder for every student who sat before their school finished it,
  and that a sitting after all teaching needs those items re-estimated on the responses whose takers had been taught.

## Survivor anatomy

- Actor: the deciding property, whether a response was given after the candidate's own school had finished the item's unit, has no column in any file: it is a relation between the response's session (UTC, in the session log), the candidate's school, that school's Term 3 sequence and term start (the course review's appendix, in the school's own words and week numbers) and the item's unit (the bank), and no file or single join holds it.
- Link: the comparison of each response's sitting day with its own school's last day of the item's unit is a cross-file comparison true-score pre-equating never asks for; the appendix lists schools by name in their own formats, nothing in the bank or the specification names a sequence or a sitting day, and no clause puts both sides in one sentence.
- Reflex: the field's own method for the deciding quantity, true-score pre-equating of each draft from the bank at the Achieved ability after an anchor drift screen and item fit, sits at rung 0 and files Paper A, written into the default path.
- Back-test: the textbook route validates on everything the pack holds: the bank reproduces every 2026 form's observed mean mark (it was calibrated on them), the anchor block's free 2026 estimates sit inside 0.10 logits of their banked values, every item's infit and outfit sit inside 0.8 to 1.2, and the 2025 run agrees with the 2026 run on the items both carried because both sittings fell in the same weeks.
- Second use: every file the decisive step reads sits in the pack for a reason it independently has: the session log is the sitting's record (and the participation ask reads it), the response export carries the item fit and the reconnect duplicates every route meets, and the course review is where the unit-to-strand map the blueprint check needs is filed, its appendix the curriculum committee's own return of member schools' sequences.
- Shock: the movement the step recovers reads as ordinary: the Term 3 items' banked difficulties sit inside the bank's spread (their mean about a quarter of a logit above the Term 1 and 2 items'), their fit matches the rest, no school, day or form is an outlier, and no sort of items on a shipped statistic puts the Term 3 items, or the drafts, in the golden's order.
- Pins: the WHAT is filed in the Trust's own genre, the paper specification (a candidate at the Achieved standard sitting the 2027 paper, the expected mark under the Rasch model on the bank scale, nearest 25 of 50, compared before rounding) and the standard-setting record (the Achieved ability on the bank scale); no filed sentence names a teaching sequence, a sitting day, a taught state or which responses an item's difficulty rests on, and the council's minute files only the November 2027 dates and its reason.

## Readability screen

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | 7 Organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 bank pre-equating after the renumbering, the final run, the drift screen and item fit (A) | spec and record | bank columns | the field's method | clean | clean | yes | no | readable |
| 1 the November move noticed, abilities grown to November, the Achieved point held (A) | minute's dates | no | growth models | none | no | yes | no | readable |
| 2 the outline's model weeks, whole schools finished before sitting, the last days' sitters, the within-window trend (A) | outline weeks | session days | late-sitter subset | none | no | no | no | readable |
| 3 each school's week numbers read against the national term calendar (A, 2 of 20 C) | appendix weeks | no | no | none | no | no | no | readable |
| 4 decisive: each response's taught state from its own school's sequence and term against its sitting day in New Zealand time, the Term 3 items recalibrated on the taught responses with abilities fixed on the Term 1 and 2 items, then pre-equated (C) | no clause names a sequence, a sitting day or a taught state | no column holds the state, and the join runs through a name-keyed appendix | the field's reflex is the bank, rung 0 | no control refutes the bank: it reproduces every 2026 form, its anchors do not drift, its items fit | the battery finds nothing on the Term 3 items | a recalibration on a per-response subset, not a subtraction or ratio | the course review is filed for its unit-to-strand map and the session log for the sitting record | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | which draft to print | one of the three drafts as submitted | a draft altered by item swaps | none computed | the specification: "the draft printed is the submitted draft whose expected mark ... is nearest 25" |
| SF2 | expected mark | the sum over the paper's 50 one-mark items of the Rasch probability of a correct answer | the probability of scoring 25 or more; a median raw mark | A or C, unfiled | the specification defines the expected mark as that sum, under the Rasch model on the bank scale |
| SF3 | the Achieved standard | 0.35 logits on the bank scale | the 2026 forms' raw cut scores; the Achieved rate | not a point on the scale | the standard-setting record files the standard as an ability on the bank scale, and the specification asks for a candidate at it |
| SF4 | nearest 25 | absolute distance, unrounded | rounded marks compared | same call | the specification: "compared before rounding"; C is nearest both ways (asserted) |
| SF5 | the bank scale | held by the anchor block at its banked values | the recalibrated bank re-centred on all items' mean | same call | the bank's notes: "the scale is held by the anchor block at its banked values"; re-centred, C stays nearest (asserted) |
| SF6 | which 2026 calibration | the final run | the preliminary run (sessions to 19 August) | same call | the runs file's header: the final run supersedes the preliminary; the golden and the default path keep their calls on either (asserted) |
| SF7 | item identity | each draft's item card numbers mapped through the 2025 renumbering | card numbers read as bank codes | none computed | the renumbering file; no card number is a bank code |
| SF8 | the sitting day's clock | the session's start in New Zealand time | its UTC date | same call | asserted: no school sits on its unit's last day and every first unit ends on a Friday, so no response crosses a unit's end under either clock |
| SF9 | finished before the sitting | sat on a later day than the school's last day of the unit | the last day itself counted; 2 or 4 days after it | same call | asserted: no session falls on a unit's last day, and the lag variants file C with every draft at the golden's whole mark |
| SF10 | a re-answered item after a reconnect | the later answer, the platform's final response | the earlier answer; both rows | same call | asserted on the golden and the default path |
| SF11 | the second Term 3 unit | taught at the school's term end, after every sitting day | none | same call | every appendix sequence ends at its school's term end, after 21 August (asserted) |
| SF12 | a school's week numbers | weeks of the school's own Term 3, from its start in the appendix | weeks of the national Term 3 calendar | A (2 of 20 redraws C) | the appendix header: weeks are the school's own Term 3 weeks, with each school's start date given |
| SF13 | the recalibration's form | Term 3 items re-estimated on the taught responses, abilities fixed on the Term 1 and 2 items | a joint calibration without the untaught responses; Warm's abilities; one taught shift for every Term 3 item | same call | asserted: each files C with every draft at the golden's whole mark |
| SF14 | the November 2027 candidates | taught every core unit before they sit | none in the record | same call | the course outline places every core unit in Terms 1 to 3 and every appendix sequence ends by its term end; no sequence reaches November |
| SF15 | make-up papers | not in the calibration (paper scripts carry no item responses) | none | same call | the response export holds online sessions only; the make-up scripts carry a total mark |

## Ladder

1. Rung 0, the bank: pre-equate each draft from the final 2026 run after the renumbering, the drift screen and item fit; Paper A in 20 of 20 (redraw means A 24.83, B 20.62, C 21.71; shipped seed A 24.78, B 20.64, C 21.58).
2. Rung 1, the move noticed: grow the 2026 abilities to November and hold the Achieved point; the standard is a point on the scale, so every draft's mark at it is unchanged; Paper A.
3. Rung 2, a taught set without each school's own sequence: the outline's model weeks (no response taught, the bank), forces and motion taken as taught in the outline's fifth week (A 24.99, B 20.90, C 22.17), whole schools finished before sitting (none), the last three days' sitters (A 25.13, B 21.15, C 22.54), the within-window trend (A 25.15, B 21.21, C 22.59); Paper A in 20 of 20 each.
4. Rung 3, each school's week numbers on the national calendar: Paper A in 19 of 20, C in 1 (a Layer 1 misread below the decisive rung).
5. Rung 4, decisive: each response's taught state from its own school's sequence and term against its New Zealand sitting day, the Term 3 items recalibrated on the taught responses with abilities fixed on the Term 1 and 2 items; Paper C in 20 of 20 (redraw means A 25.94, B 22.81, C 24.90; shipped seed A 25.89, B 23.02, C 24.80).

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | the estimand's candidates are those sitting the 2027 paper in November 2027 (the specification); the calibration's are every online response of the August 2026 sitting | filed; C1 for the calibration (make-up scripts carry no item responses) |
| 2 Unit of account | a draft of 50 one-mark items and its expected mark | filed in the question and the specification |
| 3 Attribution window | a response's sitting day against its school's unit end | C1: no session on a unit's last day, first units end on Fridays (asserted) |
| 4 As-of dating | the bank as at its final 2026 run; the specification's 2027 edition | filed; static |
| 5 Version basis | the final run over the preliminary | filed in the runs file; C1 for the call (asserted) |
| 6 Denominator | 50 marks | filed |
| 7 Weighting | one mark per item | filed (50 one-mark items) |
| 8 Window length | none: the taught state is per response | C1 across the lag variants (asserted) |
| 9 Boundary inclusivity | taught when sat on a later day than the unit's last day | C1: nothing on the edge (asserted) |
| 10 Rounding path | unrounded comparison, whole marks reported once | filed in the specification and the prompt |
| 11 Tie-break | none needed: C 0.20 from 25 against A's 0.89 at the shipped seed | C4, the margin asserted at the shipped seed |
| 12 Maturity and censoring | none: the 2026 responses are complete | not applicable, stated |
| 13 Order of operations | recalibrate, then pre-equate | C1: one order computes |
| 14 Row order | estimates do not depend on file order | C1, asserted on a shuffled export |
| 15 Duplicate resolution | the later answer of a re-answered item | C1: first and both give the same call (asserted) |
| 16 Identity normalisation | card numbers to bank codes through the renumbering; appendix school names to codes through the member schools file | C4: an unmapped card or name matches nothing (asserted) |
| 17 Netting against gross | none | not applicable, stated |
| 18 Dimensional units | logits on the bank scale; marks | filed (the record states the standard in logits on the bank scale) |
| 19 Code and status semantics | session status (dropped, submitted), unit codes U1 to U6 through the course outline | the files' own definitions; never the stump |
| 20 Integerisation | none: expected marks are real-valued | not applicable, stated |
| 21 Clause scope | the targeting clause applies to the 2027 paper; the blueprint clause holds for every draft | filed; C1 (every draft meets the blueprint, asserted) |
| 22 Forward window contents | the November 2027 sitting follows every core unit's teaching | the course outline and every appendix sequence (ends by its term end), asserted |

## Literal reader

Executed word for word, the prompt and the specification file the WHAT (a candidate at the Achieved standard sitting the 2027 paper in November 2027, the expected mark under the Rasch model on the bank scale, nearest 25 of 50, compared before rounding), the standard-setting record files the ability and the bank files the scale and every difficulty as calibrated on the August 2026 sitting. The text is silent on which responses an item's difficulty for a November sitting rests on, so every option is computed: the bank as run (A: its Term 3 difficulties describe a sitting at which about nine in ten of their responses came before the candidate's school finished the unit, which the session log against the appendix shows), the outline's weeks (A), whole schools (A, none qualify), the last days' sitters (A), the trend (A), each school's weeks on the national calendar (A; ruled out by the appendix header), and each response's own taught state (C, the golden, with every variant of its form C). The easy answer A comes from an easy method on the same literal estimand, never from another reading. checks.py asserts that the literal execution of every filed sentence alone (the specification, the standard-setting record, the bank's final run, the renumbering, with no response re-estimated) files Paper A, so no filed sentence hands over the decisive step, and that every golden variant files C.

## Oracles

No control ties only under the golden and none arbitrates the call: the bank reproduces the 2026 forms' observed mean marks because it was calibrated on them, the anchor block does not drift, every item fits, and the 2025 run agrees with the 2026 run; no file reports a November sitting, a taught-only calibration or any draft's expected mark; no memo, minute or email ranks the drafts or says which responses an item's difficulty should rest on. The specification and the standard-setting record each state a WHAT only.

## Ask sheet

Two asks, each on rows the main call never reads, each a component of the call's case (H18): ask A is the audit trail
of the population the bank was calibrated on (who was entered and who sat, by region); ask B reconciles the make-up
sitting, the part of the 2026 sitting the bank never saw. Criteria the shape supplies: the call, each draft's expected
Achieved mark (3), the chart's draft bars against the 25 line, the three named files and the rounding, then 16 ask
figures (4 regions by entered, sat, make-up candidates and mean make-up mark): 27.

- Ask A: for each region, the candidates its schools entered for the August 2026 sitting and how many of them sat it,
  online or at a make-up session (whole candidates; 8 figures).
  - Primary 1, D7 (block: sat): the office keys make-up scripts under the school code written on the script cover,
    which is the host centre's, and the hosts serve across regions (the Northern host takes four Central schools, the
    Central host half of Capital, the Southern host the other half); a script's home school is recoverable only
    through the host's typed roster (script number to entry), and the roster also lists booked candidates who did not
    attend.
  - Primary 2, D1 (block: entered): candidates who moved school inside a region stand twice in the entries register,
    the old school's upload with an NSN and the new school's office entry without one (the office form records no
    NSN), matched only by first name, surname and birth date; twins at one school share a surname and a birth date.
  - Primary 4, D4 (block: sat): unbooked absentees who turned up at a host sat at the end of the room and were written
    onto the supervisor's sheet by hand; the office never typed them, so they are absent from the roster and reach
    only the keyed file, where the office keyed the cover's entry number because no roster line matched (as one keyer
    does on every cover), and their home school is read through the entries register.
- Ask B: for each region, how many of its candidates sat a make-up paper and, where any did, their mean make-up mark
  (whole candidates and marks to one decimal; 8 figures).
  - Primary 4 (D4, shared with A's sat block, block: both B figures): walk-ins counted and their marks taken only
    through the entry number keyed.
  - Primary 3, D3 (block: the Central and Capital means): one keyer keyed the Central host's second day from the
    cover's percentage box, so that batch stands at twice its marks; only some of its rows exceed 50, and the batch is
    identified by its keyer and keying date, not by its values.
  - Shared hazard: Primary 1's host attribution (every region's count and mean).
- Hazards (ask side): the re-sent entry upload (exact duplicate rows) and withdrawn entries (status W, not
  candidates), each moving entered by itself; the session log's resumed sessions and UTC times are main-path texture
  both sides meet, and no ask figure rests on them.
- Separation: no device or hazard row sits in the main call's population (the response export, the bank and its runs,
  the renumbering, the drafts, the specification and the standard-setting record); the entries register, the make-up
  roster and the keyed scripts are read by the asks alone, and with them deleted no main file yields an ask figure.

| Ask block | Cracker path (landed the call, ran the battery, read every document) | Golden handling | Cracker |
|---|---|---|---|
| A entered, four regions | standing entries deduplicated on NSN after dropping exact duplicates and withdrawals: office entries carry no NSN, so moved candidates count twice | first name, surname and birth date across the region's schools, twins kept apart | miss |
| A sat, four regions | online candidates plus keyed scripts by the school code keyed: every host's scripts land in its own region | scripts placed through the roster, walk-ins through the entry number keyed and the register | miss |
| B make-up candidates, four regions | keyed scripts by the school code keyed | as for sat | miss |
| B mean make-up mark, four regions | keyed marks by the school code keyed, marks over 50 halved | marks by home school, the JT batch of 2 September halved whole | miss |

The full includer, who reads the cover codes as the hosts', joins every script to the typed roster and matches entries
on first name, surname and birth date, keeps the entered block (4 of 16, 25 per cent): with the unmatched scripts
dropped or placed at the code keyed, and whether or not it halves the percentage batch whole, it misses every region's
sat, make-up count and mean (asserted in checks.py, measured on the cut pack by ceiling.py).

- Pair ceiling: 35.4 (the full includer on the call, C = 38 + 7 + 55 x 0.25 = 58.8, with the mirror off it, S = 5 + 7 +
  55 x 0 = 12); two responses on the call, the full includer with the cracker, 51.9, and two full includers 58.8.
- Mirror leakage: 0 per cent of the ask weight (the mirror stops at the bank route and handles the asks as the
  cracker does).
- Measured by: generator/ceiling.py, which runs the cracker, mirror and full-includer paths on the cut pack and scores
  each graded figure against figures.json.

## Stage 3 record

- Gates on the cut pack (seed 482025, ask stream offset 6, target.zip sha256
  3f18332cb1b3e05ee59595f94783a7733276612a382f5b8fe4e9d9e4700c0cf5): two byte-identical builds (pack, goldens,
  submission, figures); checks.py 0 failures; verify.py PASS from the shipped files alone (marks A 25.89, B 23.02,
  C 24.80, bank A 24.78, B 20.64, C 21.58, every ask figure); figures_check PASS; precut exit 0; voice-check PASS
  (the which quota WARN answered in the Draw); leak.py REVIEW with no LEAK and no date after 6 November 2026; guard
  heart WARN; guard surface exit 0 with the three drawn personas only.
- ceiling.py on the cut pack: the golden path 16 of 16, the cracker and the mirror 0, the full includer 4 of 16 in all
  three of its variants; pairs 35.4 (one on the call, one off), 51.9 (the full includer and the cracker on it) and
  58.8 (two full includers on it).
- leak.py REVIEW lines, each ruled harmless: the two Notes sheets are the bank's and the office's own notes (the scale
  and the run order; the status and source codes) and say nothing of teaching or of any count; the specification
  shares the question's words because it is the rule the question cites, and carries no figure of the answer; the
  course review's shared terms are its own unit and strand names; the clone screen's two promoted pairs are the
  time, G13 and pick signature already differentiated on the card, for the author's adjudicated read.
- H13: identifiers advance by random steps (entries 1 to 3, sessions 1 to 2, late and withdrawn entries 3 to 39);
  session starts sit 0 to 6 minutes after a period start; every PDF and workbook carries its own created and modified
  stamps in order; the roster and the appendix read back whole under pdftotext -layout.

## Architecture 16 record (spent 2026-11-07)

Brackwell Alloys' 2026 product-family direct emissions for Velden's 2027 low-carbon premium (physical-environmental-
sciences, emissions-inventory, decomposition_attribution): the homogenizing furnace's gas allocated by its loads' firing
hours, not their tonnes, put 6082 billet at 0.263 over SCR-2's 0.235 and the premium at EUR 342,000 against the
per-tonne route's EUR 456,000. Shipped 2026-10-31 (judge DETERMINISTIC, APPROVE; target.zip 433ff500), reshipped
twice on 2026-11-07 for PDF provenance, and returned FAILED_TO_STUMP the same day: both portal responses filed EUR
342,000 on the firing-hours allocation, the method a careful analyst reaches for, which the hourly gas fitted at
R-squared 0.9985; the portal also flagged Domains Fit. The full record is in `pipeline.json` (`lineage_v16`).

## Architecture 15 record (spent 2026-10-31)

Architecture 15 priced Pembrook Castings' 2027 employee dental maximum under its Finance Policy F-17: each maximum's
cost per covered person month on the 2025 plan year at the 2027 fees, against Board Resolution 2026-31's 1.90 dollars.
The golden added back the predetermined work members at the 1,500 dollar maximum put off to the January reset, which
put 3,000 dollars over the limit and filed 2,000. The stage 4 judge returned NOT_DETERMINISTIC with SEND_BACK and the
reconciliation confirmed a withheld rule: F-17 executed word for word on the 2025 claims gives 0.83 and 1.23 dollars
and files 3,000, and no shipped text adds the put-off work; the asks left the put-off column's total, the deductible on
34 lines, "still in treatment" and an orphan case open. Its world (a manufacturer's self-insured dental plan) is left
with it, and its report is kept as `determinism_check_report_arch15.md`.

## Architecture 14 record (spent 2026-10-31)

Architecture 14 elected the Larrowbrook Physician Network's 2027 two-sided track practices: each practice's 2026
network measure carried from the October interim run by its own 2025 run-out at the same cut, plus the members in
hospital stays still running on 31 August, which the hospitals bill at discharge and the feeds show only as the
physicians' daily charges, each past the 250,000 dollar member cap (Mallowcrest Pediatrics' neonatal triplets,
Garrowdale Family Practice's trauma family). It shipped 2026-10-25 (zip 2c0f8d35, judged APPROVE on 04486b1a) with
eight practices entering. The repair's judge pass 2 returned FIX_NOW: two graded thresholds a cent off, the 2025
measures within a third of a cent of a rounding edge. The re-judge found the write-up's claim that all seven stay
members were past the cap by 31 August false under a pooled per-day reading (4,535.53 dollars a day against the
per-kind 6,380), the call's margins thin and the stay amount unfiled: a FIX_NOW that failed its second pass, which
spends the architecture. Its world (a clinically integrated network's risk track) is left with it.

## Architecture 13 record (spent 2026-10-25)

Architecture 13 elected the Larrowbrook Physician Network's 2027 two-sided track practices: each practice's 2026
network measure on the payers' final 2026 attribution, projected from the October interim run by the practice's own
2025 run-out at the same cut, against the default path that takes the interim measure as the 2026 figure (Ostrelwood,
Thornelfield and Jesselford alone, against the golden nine). At stage 4 round 1 (zip ab79a5f44c18f637) both scored
readers landed the call (exit 1): each read the prompt's "projected to the payers' final 2026 attribution" beside the
standard's attribution rules as a population the October run cannot hold, re-ran the October 2025 interim run on the
2025 claims with the standard's own rules and the Appendix C factors, and carried each practice's interim measure by
its own 2025 final-to-interim ratio. Reader A kept all 78 ask figures (Kesselcrest's reviewed 99215 visits at the
99214 rate out of level 5, Merrinlake's halved modifier-25 visits counted by their code, Pemberglen's coverage month
from its payment reference, Kesselcrest's Medicare Advantage lines at 6.50 out); reader B kept every benchmark,
threshold and ask B figure and no ask A figure. The judge thread was stopped at the spend. Asked to project an interim
figure to a final one, a careful reader takes last year's interim-to-final ratio, the field's completion reflex, and a
standard whose rules can be re-run on last year's claims hands it that ratio in one pass.

## Architecture 12 record (spent 2026-10-24)

Architecture 12 certified the Quillmere Lake basin's 2027 Seasonal Communities Aid: each city's average population
present in its busiest month of the measurement year read from its plant's influent BOD load divided by the load per
person its own January to April 2026 fix, against the default path that counts residents plus the paid stays the fee
returns and both platforms record (Sorrelton and Esker Narrows alone, USD 1,200,000 each, against the golden's five
cities at USD 480,000 each). At stage 4 round 1 (zip be45d7b75ea5cc24) both scored readers landed the call (exit 1):
each read the Act's "every other person staying in or visiting the city" as a population no record holds, went to the
one file that measures everyone (the plants' influent), divided the load by 0.17 lb a person a day (the population
equivalent the world had been tuned to agree with), checked it against the residents in winter and filed the five
cities; both also counted Kettle & Pine's nights back from the departure in its reference (reader A all 32 of ask A,
reader B 26 of 32 on half-dollar rounding) and missed only the pond systems' flow basis in ask B. The judge thread was
stopped at the spend. A statute that defines the population as everyone present, beside records that plainly hold
only the paid stays, sends a careful reader looking for a measure of everyone, and a pack whose influent rows have
no other use hands it one.

## Architecture 11 record (spent 2026-10-24)

Architecture 11 settled Lumenfold Learning's 2025-26 outcomes guarantee district by district, each partner district's
share of eligible students at or above Proficient on a matrix-sampled spring science assessment re-estimated from its
students' own two-module answers with the district in the population model, against the default path that averages
the contractor's five plausible values by district (19 districts owed USD 32,045.00 against the golden's 16 owed
USD 25,493.75). At stage 4 round 1 both scored readers missed the call, reader A kept all of ask A through the
catalog's hours per session, and the judge's pass 1 returned FIX_NOW on a cent tie in the credits (seat prices moved to
whole half dollars). In round 2 reader C refitted the 2PL latent regression from the item responses with district in
the conditioning model, validated it on the contractor's Table 6, filed the golden 16 districts and USD 25,493.75 and
kept every ask figure: a conditioning model that leaves out the grouping variable is a reflex for a reader who knows
plausible values, so the architecture was spent.

## Architecture 10 record (spent 2026-10-24)

Architecture 10 accrued each Medicare hospice provider number's FY2026 aggregate cap repayment at the December 2026
close, each beneficiary counted under the proportional method on the days to come from their state at the close (an
open stay by its length so far, a live discharge by its time out, returns read at every hospice from the benefit
periods extract), against the default path that runs the open stays on and takes the live discharges as finished
(Fallowmere USD 0.3 million against nothing). At stage 4 all four isolated readers across two rounds missed the call
and the round 1 judge returned DETERMINISTIC, APPROVE; the round 2 judge returned NOT_DETERMINISTIC, SEND_BACK
(margin_or_boundary_fragility and competing_defensible_answer): the printed 0.3 needed Fallowmere's count inside a
window of 2.9 beneficiaries while independent builds of the projection scattered about a beneficiary either way, and
the pool start, the number of later elections and the Kaplan-Meier tail were left unfiled (0.248 to 0.447 on the
judge's variants); ask A's routine-paid days read as an unstated rule. A designation set would have held (every variant
put Fallowmere above its cap); a figure printed to USD 0.1 million on a three-beneficiary window did not.

## Architecture 9 record (spent 2026-10-23)

Architecture 9 read each station's Schedule C availability from the bikes in working order docked, each bike's spells
rebuilt from the trips and fleet moves and a bike counted out of working order from the end of the ride that left it
when renters passed it over and a van then took it to the depot for a day or more, against the status feed's available
count (W-02, W-12, W-16 and W-19 against W-16 alone). At stage 4 (zip 14ceb178) both scored readers missed the call:
reader A subtracted the reported bikes and the bikes mechanics took in without a report, inside the inspection windows
(W-16 and W-19); reader B subtracted the reported bikes only (W-16). Both kept nearly every ask figure (65 and 64 of 74,
exit 1): the sales export's present-location column undone through the work orders' terminal replacements, and the
alarms ended at restarts once the clear pairing ran to hundreds of hours with sales inside them. The isolated judge
thread returned NOT_DETERMINISTIC, SEND_BACK, competing_defensible_answer (Gates B, C and E): no shipped file says that
unreported broken bikes exist or how to find them, so the records read literally (the feed, or the rebuild with the
reported bikes out) file W-16 alone, and the depot-stay cut and the pass test sit only in the solution's steps (at 36
and 48 hours W-17 and W-19 move by a point); Gate G `planted_defect_flip`, `surface_read_rejection`,
`surface_read_dependency: yes`, `sole_data_defect: yes`; Gate H `decisive_step: planted`.

## Architecture 8 record (spent 2026-10-23)

Architecture 8 carried each store's data logger record through the vaccine's thermal lag, a first-order response
fitted per logger make on the two weeks each pilot store's old logger kept recording beside its new in-carton sensor
(42.2, 42.2 and 41.9 minutes), against the loggers' readings taken as the vaccine's temperature (six stores against
ten). At stage 4 (zip ad958ec9) reader B set the pilot stores' loggers beside their in-carton sensors over the overlap
unprompted, fitted the lag as a first-order filter (0.21 of the gap closed per ten minutes, about 42 minutes) and
landed the six stores and every store's whole hours, answering question 6 "an analytical choice" on standard 7.2; it
kept every ask figure too (122 of 122 graded figures, exit 1): the counts' own closing times, the credits found when
per-item balances went negative, the vial write-offs by cost over the per-dose cost, the tax switch by the
maintenance-only invoices at Schedule B's prices, and the two-store routes split by Schedule B. Reader A and the judge
thread were stopped at the spend.

## Architecture 7 record (spent 2026-10-23)

Architecture 7 read each production day's oxidizer outlet from the relation the ten oxidizers' tests trace (a floor of
about 45 ppmv as carbon, 1.8 per cent of the inlet above about 2,500) at the inlet the day's captured VOC and airflow
imply, against each plant's latest test efficiency (Ashcombe 21 and Kelvedon 20 against 29 and 28). At stage 4 (zip
5ab18e48) reader A read the floor straight off the test tables (Ashcombe's 2018 two-press test holds the same 45 ppmv
at half the inlet), rebuilt each hour's outlet as the greater of the floor and 1.8 per cent of the inlet and landed the
five and all 14 whole tons, Part 2 question 1 "none" and question 6 "an analytical choice"; reader B carried each
fixed-fan unit's test outlet to the year through the register's fan-drive column (R4, six plants). Both readers kept
all 28 ask figures: the revision log read, the payment lines parsed, Haldane matched on description. The judge thread
was stopped at the spend.

## Architecture 6 record (spent 2026-10-22)

Architecture 6 set Form 27A's placement scores from the bank difficulties carried from the old platform's field-test
section (positions 61 to 70) to the positions 21 to 70 the unique items take on Northgate Assess, by the position term
the 2026 attempts measure, against the default path's difficulties as filed (29 and 18 against 30 and 19). At stage 4
reader A rebuilt every response at its delivered position, fitted the Rasch model with the anchor block fixed, found
items harder later in the test on both platforms and landed 30 and 19 exactly (29.48 and 18.50), Part 2 question 1
"none" and question 6 "an analytical choice"; it kept 13 of 62 ask figures (the system totals and some twice counts).
Reader B and the judge thread were stopped at the spend.

## Architecture 5 record (spent 2026-10-22)

Architecture 5 designated rapid price growth areas on each dwelling type's own year effect weighted by the census
stock's value, with a pooled hedonic year term as the default path. At stage 4 both readers and the judge's own
derivation took the type-by-stock aggregation by reflex (type medians or type year effects weighted by the census
stock) and missed the call only on the location control (electoral division), which the judge read as unfiled; filing
it hands all three the call, so the decisive step as designed does not stump and the one that held is a fork.

## Tried and rejected
- Architecture 6, item position effects in pre-equating (2026-10-22, spent at stage 4): reader A fitted a Rasch model
  with a position term to the rebuilt attempts and carried the field-test difficulties to Form 27A's positions,
  unprompted by any sentence. The calibration context has to be recoverable for the truth to be fair (the report's
  delivery section and both exports' positions), and once it is, an analyst who knows the field checks the effect the
  context invites; a context effect measured by an obvious model term is a reflex for the field's own analysts.
- Architecture 6 draw (2026-10-22): re-rooted on the author's standing rule (no retirement) with a fresh world. Screened
  before it and dead: a CEMS gap fill on load (guard BLOCK on pattern G12 and strategy population_selection against
  task273, same-puzzle and same-driver spent in five to seven builds, the statutory filing against task249);
  multiplicative against additive seasonality (task146, task147); a moving holiday (task162, task467, task135);
  Denton benchmarking (this slot, below); retroactive eligibility as a denominator still developing (the completion
  driver of task451 and task479 v5); Fellegi-Sunter frequency weights (set aside at task486's draw against task468's
  linker error); the oldest old by extinct generations (task228); non-detects under several limits (task189).
- Architecture 5, the stock's price change as each dwelling type's own year effect weighted by the census stock's
  value (2026-10-22, spent at stage 4): both readers and the judge's first derivation weighted dwelling types by the
  census stock by reflex (the note's "dwellings the 2022 census counts" and the census workbook by type invite it) and
  missed only on the electoral-division control, which the judge read as unfiled (r5a); filing it hands them the call.
  A stock aggregation over a tabulated type mix is a reflex once the stock is the filed population.
- Architecture 5 draw (2026-10-22): re-rooted on the author's standing rule (no retirement); the world and pack of architecture 4 kept, the decisive step moved from the constant-quality regression its reader 9 found to the aggregation that regression skips (each type's own year effect over the stock's value), with the pooled regression now the default path. At registration the v4 identity BLOCKed on own_lineage, gap population on same-puzzle and same-driver (task251 v5), shape 10 and the statutory filing (task249 v6) and filed_standard (task478 v4); redrawn as recorded in the Draw, the circular changed to settle the 2027 fund allocations.
- Ask B's reissued student ids as a 7-digit id equal to the old one plus a campus constant, linked by birth date, sex and ZIP (2026-10-21, stage 4 round 1): both readers resolved it on the person columns and kept all six headcounts (score_reader 50 per cent); re-sited so the new ids share the old form with no arithmetic tie, birth date, sex and ZIP are shared by different students, and the movers' majors are recoded, so only the four-field key resolves it.
- Architecture 1, a coordinating board's instructional grant with four parents' consolidated returns apportioned by a cost model (2026-10-21, spent at stage 4): round 1's two readers split by FTE or total credit hours and missed; both round 2 readers fitted instruction expense on credit hours by level across the standalone campuses, split each parent's return by the modelled cost and landed the call (exit 1). Pricing activity by level from the units that report alone is a strong reader's reflex once the activity file by level ships beside the combined return.
- Architecture 2, regional register error rates from an audit drawn unequally by a risk screen (2026-10-21, spent at stage 4): both readers checked the audit's composition against the register (35 per cent referred against 8), weighted each stratum to the 30 April register and landed the call; both also read the UTC times into local time and dropped the restored companies (asks 28 of 28). A sample whose composition differs from its frame on a shipped flag is reweighted by a strong reader; a stated clock and a restoration notice are seen devices.
- Architecture 3, registration offices put on a timeliness plan from a quarter's median working days with part of the quarter still open at the extract (2026-10-21, spent at stage 4): both readers censored the open applications at their age, took the Kaplan-Meier median and landed the call, and dated payments by the batch terminal day (asks 28 of 28). An open caseload shipped beside a duration cohort, with a paper saying the open ones count, is read as right-censored by a strong reader; a settlement batch file carrying the terminal day is a seen device.
- Architecture 4, areas' house price change for the rapid price growth designation read from a shifting sample of the stock (2026-10-21, spent at stage 4): reader 9 fitted log price on type, floor area, age, newness and the address point file's electoral division with a year term and landed the call; reader 10 left location out and missed; the block purchases' one consideration on every line held both readers (0 ask totals of 32). A constant-quality index is a strong reader's reflex once the note cites the handbook and the attributes ship; location one join away is not a hidden dimension.
- A district's register error rise tested with the spread of the audit's sampled blocks (2026-10-21, screened at the draw): the guard put it beside task261 (subgroup statistics from one clustered sample, their difference's error from the clusters), the same driver.
- Regional quarterly output benchmarked to annual totals by Denton against pro-rata (2026-10-21, screened): Denton's extrapolation holds the end-of-year ratio, which sits within a few tenths of a point of pro-rata's annual ratio, while a trending ratio puts the truth far from both; the separation is too small and the truth not recoverable without forecasting the ratio.
- Architecture 7 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world.
  Screened before it and dead: gross labour-force flows corrected for reinterview misclassification (task244's
  driver); speededness on a timed form (task249's screen); a winner's curse in form assembly (task471's shrinkage
  coin flip); generic price erosion by entrant count (task484 v1's ramp, screened at task478's draw); percent-of-charges
  hospital contracts carried to each hospital's current chargemaster (the swap test reads it as any list-price
  contract); laboratory results harmonised by proficiency-test bias (the reported result is the measurement, so the
  correction is a fork); a cancer registry's completeness by the flow method (task249's screen); common-stack
  apportionment from single-unit hours (task263's unmixing); a concentration-discharge load (task452 v1, task135);
  change of support for block grades (task270, task254, task273 screens); linkage on an address the outcome changes
  (task468's linker error); calculator-type DIF and released-item drift on the item bank (architecture 6's lesson: a
  context an obvious model term measures).
- v7 stage 3, 2026-10-23: the first tuning let each oxidizer's test outlet carried to the year (its concentration on
  each day's air, or its rate over the year's hours) file the golden five, because a fixed-fan plant at the floor emits
  the same rate every day; Larkmoor Graphics was made a concentrated-test, mostly-dilute plant under 25 tons so those
  routes file six (R4, R4m, R4b).
- v7 stage 3, 2026-10-23: press VOC to one decimal: the standing family spreads up to 0.37 tons on a plant, so the
  figure is graded in whole tons, every member 0.19 tons or more from a half (G4); the CSV's used and captured
  columns went with it (free to both top responses), the CSV now the press VOC and coverage.
- v7 stage 3, 2026-10-23: the tuned plants landed on whole tons (29.00, 37.00); moved to ordinary offsets (G5). Days
  below the tests' lowest inlet at three plants opened an extrapolation fork (interpolated efficiency against the
  floor); the low days were raised inside the tested range.
- Architecture 7, 2026-10-23: spent at stage 4. The decisive relation was visible inside one oxidizer's own tests (the
  same outlet at two inlets) and in the register's fan-drive column, and a regenerative oxidizer's outlet floor is
  field knowledge both readers carried; the asks' devices each sat one file away from a careful reader's path (the
  master's revision log in the same workbook, the washer gallons in readable payment text, descriptions beside the
  renumbered items). Next architecture: a decisive step no table displays as a pattern and no column labels.
- Architecture 8 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world, aimed
  at architecture 7's lesson (no table displays the decisive relation, no column labels it). Screened before it and
  dead: vessel propulsion from AIS speed over ground carried to speed through the water by an estuary's tidal streams
  (a port world beside task472 and task474, and a tidal stream table has no other use in an emissions pack, so its
  presence announces the correction); container ships' at-berth auxiliary load by the reefers on board, calibrated on
  shore power meters (a port world, and a reader calibrating on the meters sees the per-call spread with reefers its
  first explanation); a tanker's boiler load at berth by its own steam cargo pumps on discharge (the at-berth tanker
  rules' own reasoning, a reflex once the transfer log is joined); dairy lagoon methane through the lagoon's
  temperature lag behind the air (the rate model is a filed procedure, and four inspection readings a year cannot fix
  the lag deterministically); switcher locomotives' idling through the start-stop system's restart temperature (a
  rate carried across a weather covariate, task478 v7's driver); crematory mercury by the decedents' dental cohort (a
  composition mix one survey table hands over); breaker SF6 leak rates from temperature-uncompensated pressures (the
  gas temperature at each reading is not recoverable). A cold-chain prototype (thirty-six refrigerators, probe 6 minutes,
  carton 48) put the logger's own hours at two to ten times the vaccine's, the default qualifying 29 against 12, with
  a 45-minute lag fitted on ten fourteen-day overlaps at 0.04 degrees C reproducing the carton's set exactly, while 30
  and 60 minute duration filters (17 and 6) and a 45-minute moving average (20) fell elsewhere and a 90-minute moving
  average missed by one refrigerator: the stage 2 world keeps the default's count plausible and every store clear of the
  line under the standing family.
- v8 stage 3, 2026-10-23: standard 7.1 first read "the records of each store's device of record are its vaccine
  temperature records", which a literal reader takes as the logger's readings being the vaccine's temperature (an
  official decoy for the default path); it became a records-custody clause.
- v8 stage 3, 2026-10-23: under the interval-mean reading of a record's vaccine temperature five stores' whole hours
  moved by one while the call held; 7.3 now files the counting (a record counts its ten minutes by the vaccine's
  temperature at its time stamp), WHAT and not HOW (SF17).
- v8 stage 3, 2026-10-23: return credits from both manufacturers put the cracker's balance below zero at eleven
  stores, a loud failure that points at the double count; only Halvorsen's standard-dose products are returnable, the
  leftovers leaner and the unrecorded losses scaled to each store's volume (cracker 15 doses or more, A6).
- v8 stage 3, 2026-10-23: maintenance-only invoices at one price per unit type tied ten stores' service figures (a
  constant response would have kept them); per-model prices and add-on parts at some visits, every store's figure now
  distinct (B5). With the tax switch as ask B's only silent device a reader who found it kept 23 to 30 of 30; the
  pre-move two-store maintenance routes on one invoice were added, so the tax switch alone keeps 10.
- v8 stage 3, 2026-10-23: the first names sat on real organisations, products or places in or near the field (H21):
  Coldline (a refrigeration manufacturer), Polarwatch (an ocean-data programme), Vaxtor, Homeline, Arctis, Glacier
  Medical, and the acquired chains Rookwood Drug and Saltash Apothecary; renamed Tellvane, Brumal, Stellane, Keswell,
  Brannon, Pendry Medical, Vollmer Drug and Lindqvist Apothecary before any reader saw the pack.
- Architecture 8, 2026-10-23: spent at stage 4. Two instruments recording one unit side by side are compared by a
  strong reader on reflex: the pilot stores' logger and in-carton series parted at every restock and defrost swing, so
  reader B fitted a first-order lag on the overlap with no sentence asking for it. Every ask device had one natural
  check that exposed it (per-item balances, cost per unit, a list price met exactly, one invoice on two sites).
  Next architecture: a decisive step whose evidence no single side-by-side comparison shows, and ask devices that no
  per-item reconciliation or unit-price check reveals.
- Architecture 9 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world. Screened before it and set aside: phantom shelf inventory under a vendor-managed availability guarantee (on-shelf availability is an industry term that names its own correction); a plan directory's ghost providers read from claims (the directory and the claims sit side by side, architecture 8's reflex); a starting dose as the mark of a true initiator in an outcomes contract (population_selection, in the window against task275); rectifying inspection's over-weighted rejected lots (population_selection again); left truncation of a fleet's lifetimes (task133's delayed entry for a taken-over book); GPS chord distance by terrain for fuel-tax jurisdiction miles (the call would sit on a few per cent of one state's miles); meter error read off a system balance (the instrument-bias family task478 v5 and task480 v1 lost to readers); charger uptime from failed sessions (the failure is written in the session record itself). The bike-share draw keeps the listed count correct for what the operator knew and puts the difference in renters' choices, which no record states.
- v9 stage 2, 2026-10-23: the fleet's clock ran four hours off Eastern time after the move to absolute instants (its
  local minute of the day counted from midnight UTC), so the pack showed the morning rush at noon; the window's start was
  re-anchored to 20:00 on 23 September so the fleet's own clock is Eastern time, the trajectory byte for byte the same
  (46,883 trips), the station move and the dock expansions read at 23:00, and Schedule C's minutes taken from Eastern
  time itself; the designations held (W-16 alone against W-02, W-12, W-16, W-19).
- v9 stage 2, 2026-10-23: each station's three months to one decimal put nine of 72 cells within two minutes of a
  printed edge and W-12's lowest month (87.652) within a minute; graded at each station's lowest month in whole per cent
  instead (the tightest ten minutes clear, M1), the margin to one decimal (0.684, eleven minutes), the monthly figures
  kept in the workbook as context.
- v9 stage 2, 2026-10-23: ask B's hours to one decimal put W-18 within a second of an edge; graded in whole hours, each
  pay station's alarm stream chosen so its figure sits 0.08 hours or more inside its bin (M3).
- v9 stage 2, 2026-10-23: the union of overlapping alarms as ask B's device: at whole hours the summed and merged
  spans print alike at every station; kept as texture (B3), the restarts carrying the device.
- v9 stage 2, 2026-10-23: with only the alarms and restarts in the log, ending an open alarm at the pay station's next
  event of any kind kept 15 of 24 hours figures (the restart was nearly always the next event), an honest pair of 45.7;
  the cabinet heater's events on cold days and the service door at reader repairs added, the shortcut keeps 4 (33.1).
- v9 stage 2, 2026-10-23: invented names screened by web search (Wellhaven, Northlane Mobility, Corlund Kiosk
  Systems): no organisation, product or place on any of them in or near the field; Welland, Ontario is three edits away.
- Architecture 9, 2026-10-23: spent at stage 4 on the judge's SEND_BACK. A count the operator's system publishes as
  available, read against a state no record holds (a bike's working order inferred from what renters and the vans did
  with it), is a surface read rejected however the evidence is gathered: on clean data the feed would be right, so the
  judge files Gate G surface_read_rejection and Gate H planted, and with nothing filed saying unreported faults exist
  the records read literally give the feed's answer (competing_defensible_answer). The readers missed the call for the
  same reason the judge refused it. Both ask devices were found: a column filled from a present-day register is undone
  by a work-order log that lists every swap, and a pairing that runs alarms to hundreds of hours with sales inside them
  announces its own repair. Next architecture: a quantity every file visibly lacks (so no surface read stands in for it),
  estimated by a method the data forces, and ask devices whose wrong reading is plausible rather than absurd and whose
  evidence no log lists outright.
- Architecture 10 draw (2026-10-23), no card filed. The guard's window closes survey research for ETL (ban.pairing and
  ban.subdomain against task483, so census-register and seasonal adjustment are both out) and the strategies grain_or_unit,
  population_selection and composition_mix (task483, task275, task179); payment claims, emissions, IRT equating and data
  integration clear it. Screened on those four and dead on file or on measurement: competing exits against censoring
  (task169, task266; the competing exit is a reflex, task133); pooled-test infection rates (task188); age-length keys
  (post-stratification, a reflex once the aged subsample's design ships); a pooled tail share from parts' means and spreads
  (task483's lesson); a population's share past a cut from short matrix-sampled booklets (task464's shrinkage lesson);
  direct against indirect adjustment of a net series (task453 v2's fork); time-series consistency by splicing (task123's
  screen); chance agreement on name and birth date in a voter roll (task468's common-identifier lesson); credibility for
  site emission factors (the regulatory standard takes the site's own tests, a fork); tracer flux ratios (the integrated
  ratio is the method's own definition, so the default is the golden); flows traced through intermediaries to end markets
  (task451 v1's swap failure); uncompensated gas meters (a unit read, data semantics); correlated systematic errors in an
  activity-data uncertainty (the call is a monitoring decision, Data Quality); cohort waits from cumulative counts under
  first-in-first-out (generic queueing, the swap reads the same); a pick log matched to put-aways by each lane's access
  order (drive-in lanes are last-in-first-out, field knowledge a strong reader carries, architecture 7's death).
- Architecture 10 draw (2026-10-24): drawn on the hospice cap after a second screen of the four open ETL task types (survey research still closed by task483). Screened and dead: TRI range codes valued at the exact filings inside each range (the midpoint is the programme's own convention, a competing defensible answer, and the exact filings are one group-by away); charge compression in cost-plus repricing (the implant invoices put the cost-to-charge ratio against the charge in plain view, and the functional form forks); a stopped turbine's nacelle anemometer read through the running transfer function (readers impute from neighbours by habit, and Gate G reads an instrument bias as planted); unconstrained demand on sell-out days (the product-limit estimator is a reflex and converges with the intraday route); time-of-observation bias in daily maxima (the calendar-day maximum is not recoverable from a 5 p.m. reset and the nearest hourly station); trend uncertainty with shared emission factors (propagating through the difference carries the shared factor by construction, so the easy route is right); items dropped from scoring rescored through the test characteristic curve (the published conversion table replays the method); best-of-k seed reports deflated by each recipe's seed spread (the client's GSDS Layer 1 list names best seed against mean as harmonisation); inverter clipping, demand ratchets and dead-time counting losses (each leaves a flat top or a ceiling in the records that announces its correction); unit value against a fixed-basket price index for provider unit cost (composition_mix, banned against task179 for this registration); DIF purification, testing-window instruction time and single-group order effects in equating (field reflexes, or no bias in the equating); register status nowcast by a Markov chain (forecasting, and architecture 9's surface-read refusal); interpolation along a process curve between sparse readings (task478 v6's and task480's degradation and life-cycle families). The first card draft BLOCKed on test.same_puzzle against task171 v4 with G13 decisive; G12 is the honest decisive generator for the step that decides.
- v10 stage 2, 2026-10-24: a lifetime projection with Brackwater, Lindmoor and Wexmoor owing beside Fallowmere: the
  standing family (Aalen-Johansen or empirical return chances, three valuations of a return, the open stays' later
  returns overall or from their time so far) moves each core program's cap by USD 30,000 to 70,000 against cells of
  USD 100,000, and the overall-rate route kept three of the four amounts; the core programs were placed under the cap
  and Fallowmere carries the call alone (nothing accrued on the default path, USD 0.3 million on the golden).
- v10 stage 2, 2026-10-24: pooled models across provider numbers and a split by discharge reason each moved
  Fallowmere's count by up to 1.3 per cent on cells of small programs; the policy files the reference class (the same
  provider number and diagnosis group), and Fallowmere's seller's system records no revocation against discharge
  reason, so the reason split is not available for its history.
- v10 stage 2, 2026-10-24: with return stays as long as first stays the overall rate times the census average landed
  the golden's cell (0.325 against 0.300); re-elections run shorter (the beneficiary comes back in decline) and seldom
  end alive again, so that route files 0.53 and the census-average valuation by time out 0.19.
- v10 stage 2, 2026-10-24: the outside share of Fallowmere's returns was raised from a third to four in five, so the
  route that reads returns from Elderglen's own records files nothing (cap ratio 0.971) instead of landing beside the
  golden.
- v10 stage 3, 2026-10-24: the organisation and program names Elderglen, Brackwater, Corrinbrook, Dunsmere, Lindmoor,
  Pennacott, Sallowfield and Wexmoor sat within two edits of real places in the GeoNames register (Eden Glen,
  Blackwater, Swallowfield and Fallowfield, Dunmore and Dinsmore, Wyndmoor, Dixmoor) or carried a place word (Penna,
  and Cornbrook in Manchester two edits from Corrinbrook); renamed Wendleglen, Brindlemoor, Corvelfield, Darrelbrook,
  Marrellford, Rennickdale, Varrowmere and Farrinridge in the generator, every figure unchanged. The lines above keep the
  names they were written with.
- v10 stage 4 round 1, 2026-10-24: both scored readers missed the call (each ran the open stays on and took the
  live discharges as finished, nothing accrued) and the judge returned DETERMINISTIC, APPROVE (Gate G analytical, Gate H
  pass); reader A joined the claim lines to the remittance register and kept all 24 ask A figures (exit 1), so the
  device that the latest version is not the paid one sat off the careful path. Re-sited: the contractor's prepayment
  review pays some held inpatient days at the routine rate, visible only by repricing the paid version, with the
  returned replacements kept as a hazard and moved more than 118 days before the close (reader B had priced them as
  pending, cutting payments); the census report's length-of-stay table, blank on a group key mismatch, now prints.
- v10 stage 4 round 2, 2026-10-24, architecture spent: both fresh scored readers again missed the call (open stays
  run on, live discharges finished, nothing accrued) and kept 0 of 24 ask figures, but the judge thread returned
  NOT_DETERMINISTIC, SEND_BACK (margin_or_boundary_fragility, competing_defensible_answer): Fallowmere's printed 0.3
  needs its count inside 177.6 to 180.5, a window of 2.9 beneficiaries (USD 0.1 million at the cap amount and 98 per
  cent), while independent builds of the same projection scatter about a beneficiary either way (0.248 to 0.311 on the
  judge's variants, 0.279 to 0.314 on the standing family), and it named four choices the policy leaves open (the
  Kaplan-Meier tail, one later election or several, stays begun before 1 October 2016, the last provider number when the
  open stay is at another hospice); it also read ask A's routine-paid days as an unstated counting rule. Lesson: a cap
  repayment printed to USD 0.1 million moves a cell every 2.9 beneficiaries of count, so a projection whose honest
  spread is a beneficiary cannot print one cell; the next architecture's call has to be a quantity whose cell is wider
  than its estimator family's spread, measured on independent builds rather than on the author's own family.
- 2026-10-24, architecture 11 draw, screened on paper before any code against v10's lesson (a call whose cell is wider
  than its estimators' measured spread): Medicare Advantage post-payment recoupments or denial overturns for a
  hospital's 2027 contract notices carry v10's latent structure (a terminal-looking state that is not final) and
  task451's (amounts still to arrive).
- Architecture 11 draw: Medicaid procedural reinstatements and COBRA retroactive elections: retroactive eligibility was
  screened at task451 and task479 v5, and COBRA's selection is population_selection, banned against task275.
- Architecture 11 draw: ACA risk adjustment transfers estimated from competitors' public prior-year transfers: carrying
  a competitor's risk forward is a fork; ACA grace-period cures: rule-heavy, with the cure rate carried across the 2026
  subsidy expiry.
- Architecture 11 draw: censored transplant costs by inverse probability of censoring weights: mature cohorts are
  unbiased without a trend, and a trend makes the stump a dated step; authorization- or ADT-based claims reserves: the
  completion family, and a leading indicator is a reflex.
- Architecture 11 draw: price-standardised total cost of care tiers: the standardisation is a WHAT (filed is rule
  application, unfiled a fork); deductible leveraging is task479 v3's driver; prescription abandonment by out-of-pocket
  cost: the lever is too small; stop-loss and high-cost claimant pooling: non-linear aggregation at claimant level and
  level-dependent counts are closed.
- Architecture 11 draw: hospital coding intensity after an EHR conversion, separated by the same patients' successive
  admissions: adjacent to task453 (a measurement change read from a within-design contrast that nets a drift), the event
  study is the reflex and the WHAT signposts the method.
- Architecture 11 draw: low-voltage anode effect PFCs at aluminium potlines: task459's driver (a ratio with a fixed
  component carried across activity levels), and the IPCC slope method files it; wastewater digester relief-valve
  venting: v9's Gate G risk (an unmetered event inferred from indirect evidence); idle and shut-in wells: a setting clone
  of task462 and task450 v1; stack test-day tune-ups: population_selection and a surface read.
- Architecture 11 draw: a landfill's pre-record waste read from the volume survey: the gas collection record calibrates
  the decay model and absorbs the missing waste; refinery turnaround cycles: a schedule in a file is read; fuel switched
  during gas curtailments: a degree-day normalisation is the reflex.
- Architecture 11 draw: Fellegi-Sunter term-frequency weights: adjacent to task468 (false links on common
  identifiers); address agreement decaying with the gap between records: adjacent to task468 v1.
- Architecture 11 draw: majority-drifted or released anchors (v6, task450); rater severity drift on a shared
  constructed-response subset (task471 v2's driver); rapid guessing in a low-stakes sitting (task479 v4, sent back as
  cleaning contaminated data); speededness and not-reached items (an anchor-drift screen catches them).
- Architecture 11 draw: queue position for open appeals or a coding backlog against timely filing limits: the waiting
  time is a generic queue quantity, so the swap test fails and the domain is a backdrop; censored demand behind
  capacity is task18, task108 and task168; capture-recapture is task199, task243, task248 and task448.
- Architecture 11 draw: newborns and deliveries predicted from current pregnancies in an employer group's renewal: the
  base projection's credibility and trend choices fork, in a large group last year's deliveries already carry the
  component, and the honest strategy (who is in the 2027 population) is population_selection, banned against task275.
- Architecture 11 draw: race and ethnicity imputed from surname and geography for group counts: summing the
  probabilities is the reflex for counts, and the weighting-against-regression choice for rates needs a gold-standard
  subsample, banned against task275.
- Architecture 11 draw: the payroll survey's birth-death model against the lagged QCEW census is reserved for task484
  v2, and drawing it here through a house domain would game the survey x ETL ban against task483.
- Architecture 11 draw, first world: plausible values aggregated by school for a county school system's coaching list
  reskins task450's world and call (a district's own assessment naming the campuses below a share for coaching), so the
  mechanism moved to a company's guarantee settlement with its partner districts.
- Architecture 11 placement, benchmarks by prior tercile (12 to 20 for the lowest, up to 30 for the highest): no
  district the plausible values pull down could cross a benchmark it met, since the strong-implementation districts
  with weak backgrounds sit in the lowest tercile, so benchmarks became whole numbers from 12 to 35 per order form.
- Architecture 11 placement, a 5.5-point margin to the family's envelope with 2.5 points of crossing for every route:
  no maximum likelihood or curve-inversion count crossed anywhere, the routes' upward bias peaking near 9 points; the
  shipped margin is 4 points to the whole family's envelope with 1.5 to 3 points of crossing by route.
- Architecture 11 asks, a series' total on each row with series of up to 12 hours: the hours column summed put most
  districts at two to three times their contract, which reads as wrong at a glance; the series were cut to 3 and 4
  hours and the summer institute booked by day.
- Architecture 11 ask A, the offering's catalog hours on every session row (a series' total on each of its sessions):
  round 1's reader A set the series rows beside the catalog's hours per session and replaced them, keeping all 58 hours
  and 18 credits (exit 1); the catalog every reader opens for the live and recorded formats holds the tell one lookup
  away. Re-sited onto the session times the scheduler holds as hours and minutes after the point, every offering
  scheduled in whole hours so only the sessions that ran short or long carry minutes.
- Architecture 11, credits on quarter-dollar seat prices: a 15 per cent credit on a fee of 11,537.50 is 1,730.625, so the
  cent had a tie that no file breaks (judge pass 1, FIX_NOW); seat prices moved to whole half dollars, every credit a
  whole cent, the call's set unchanged.
Architecture 11 (the contractor's plausible values drawn from a conditioning model with no district term, each district re-estimated with the district in the model), spent at stage 4 round 2 on zip ce5456c3: reader C refitted the 2PL latent regression from the item responses with district in the conditioning model, validated its fit on the contractor's Table 6, filed the golden 16 districts and USD 25,493.75, and kept every ask figure (58 of 58 hours, 20 of 20 shortfall credits, 36 of 36 memo rows) by reading the hours field as hours and minutes from its fractions. A conditioning model that omits the grouping variable is a reflex for a reader who knows plausible values, so the round-3 PD re-site (series credit hours stacked on h.mm) is moot and the slot re-roots.
- 2026-10-24, architecture 12 draw: a Lunar New Year factory shutdown reaching a US East Coast port's container imports
  a Pacific or Cape crossing later, for its calendar-adjusted series: the decisive step is a lag and a window, the
  enumerable single choice the client's measured coin flips share, the effect is famous in trade data, and a port world
  would be this lane's third (task472, task474). Not drawn.
- 2026-10-24, architecture 12 draw: a state's payroll survey estimates early-benchmarked to the lagged unemployment
  insurance census where the birth-death model ran ahead in a slowdown: the two series count the same jobs side by side
  (architecture 8's reflex), the step is a choice between two files, and rejecting the published estimate for the census
  reads as a surface-read rejection at Gate G. Not drawn.
- 2026-10-24, architecture 12 draw: revisions measured from real-time vintages, or rebuilt pseudo-real-time by
  re-adjusting truncated spans: the client's pin makes the triangle rule application once the vintages ship, and the
  truncated re-adjustment forks between X-11 and STL end filters. A seasonal break from a school calendar moved to
  August: the post-break span is a window and the regime regressors are a reflex. Not drawn.
- 2026-10-24, architecture 12 draw: chain drift in a scanner-data price index (economics x ETL is undrawable, and the
  formula is one enumerable switch); suppressed county-industry cells rebuilt from their margins (identification is the
  step, so one linear solve is the easy route landing); custom-area margins of error from replicate tables against the
  approximation (the handbook licenses both, a fork at Gate C); register over-coverage by signs of life (every activity
  window is a threshold read as a fork). Not drawn.
- 2026-10-24, architecture 12 draw: the lake towns' population present also read from their transfer stations' scale
  tickets or their water meters: solid waste is collected on schedules that lag the stays, and summer water use carries
  the irrigation of empty cottages, so neither measures the people present as the sewer does; kept out of the pack.
- 2026-10-24, architecture 12 stage 4: the population present read through the plants' influent load per person,
  calibrated on the winter months; both round 1 readers landed the call at the 0.17 lb population equivalent (exit 1),
  because the Act's definition made the paid-stay records visibly incomplete and the influent rows had no other use in
  the pack. Spent.
- Architecture 13 draw (2026-10-24): re-rooted on the author's standing rule (no retirement) with a fresh world.
  Screened before it and dead: Medicaid exposure developed through retroactive enrollment (task474 v4's capitation
  world, task451 and task479 v5's completion, and the recent months' dip shows on any monthly tabulation); linkage
  sensitivity by identifier stratum for linked mortality (a pooled clerical correction lands the stratified set on
  paper, and stratifying by the identifier is a reflex); three measurement systems combined by triple collocation
  (task228, landed); regression against equating in a score crosswalk (task464); payday counts by weekday schedule
  (task477); data fusion through a small joint source (task465); a prospective capitation priced on experience chosen
  the same way a period earlier (task130's lineage); business deaths confirmed after two years without reactivation
  (the standard's definition makes the adjustment a reflex); out-of-state births to residents arriving through the
  vital records exchange (a completion the place-of-occurrence field shows).
- 2026-10-24, architecture 13 stage 2: the October run's short counts read as members still to come who cost nothing
  (the interim measure scaled by the run's members over the 2025 final run's, or by the member months) filed the golden
  set with the practices as first placed, so a reader who saw the counts and assumed the rest landed the call without
  the 2025 re-run. Birrelhaven, the paediatric clinic whose late members cost nearly what its others cost (run-out
  0.944 on a 22 per cent short count), was placed 5.5 per cent over its threshold, where the zero-cost reading takes it
  12.8 per cent under.
- 2026-10-24, architecture 13 stage 2: asks with one device each (the code on the claim for ask A, Pemberglen's
  posting period for ask B) handed a whole ask to any response that found its device; each ask now carries a second,
  independent silent device (Merrinlake's halved modifier-25 visits; Kesselcrest's Medicare Advantage lines on the same
  remittances), and the best single-device handling keeps 6 of 52 figures.
- 2026-10-24, architecture 13 stage 2: the projected 2026 figure graded to the cent was dropped from the prompt's
  columns: the licensed constructions agree on every election but not on the cents (per payer against per practice
  moves a projection by up to 0.6 per cent), so the workbook carries the projection as context and the rubric grades
  the benchmarks, thresholds and elections.
- 2026-10-25, architecture 13 (each practice's interim measure carried to the payers' final attribution by its own
  2025 run-out at the same cut), spent at stage 4: both scored readers re-ran the October 2025 interim run from the
  2025 claims and landed the call, reader A with all 78 ask figures; a projection from an interim run to a final one
  whose prior-year ratio the standard's own rules rebuild is the completion reflex, and the second ask devices (the
  halved modifier-25 visits, the Medicare Advantage lines at another rate) fell to a reader who checked only the payer
  whose rates looked wrong and the one fee that did not match the standard.
- 2026-10-25, architecture 14 draw: the member cap read as what the run-out truncates (a member whose year to date
  already sits at the cap carries fixed dollars while the year's months grow): in architecture 13's world no member
  reaches USD 250,000 by August and 25 reach USD 100,000 (2.9 per cent of the capped January to August amounts), and a
  practice's capped share moves from one year to the next by noise (about 1.5 per cent of a projection), so no flip
  holds.
- 2026-10-25, architecture 14 draw: competing exits read as censoring (a cumulative incidence against one minus
  Kaplan-Meier) is spent by task134, task254, task257, task264 and task266; a share above a cut counted from scores
  measured with error is task253's driver; random-groups equating with make-up sessions on one form fails on the
  group-equivalence check, which is the field's own quality control and lands by reflex.
- 2026-10-25, architecture 14 stage 2: the run-out (v13's golden) on the default path left Birrelhaven's 2025 twins,
  in a neonatal unit from 24 June to October 2025, running at the 2025 cut, and the same-cut figure read as the network
  would have reported it at 30 September 2025 then left their facility claims out of the run-out's denominator and kept
  them in its numerator: 32 of the 128 constructions entered seven, Birrelhaven out. Their stay now runs from 3 March to
  June 2025 and is paid by August, so no long stay runs at the 2025 cut and the run-out's precondition holds in 2025.
- 2026-10-25, architecture 14 stage 2: the asks' architecture 13 devices (Kesselcrest's reviewed 99215 visits at its
  99214 rate, Merrinlake's halved modifier 25 visits at no rate on the schedule, Pemberglen's coverage month in its
  payment reference, Kesselcrest's Medicare Advantage lines at another fee) all fell to one reader who matched every
  line to the schedule and every fee to the standard. The halved visit now passes that match (Merrinlake's 2026 level 5
  is twice its level 3, so a halved 99215 is a full 99213), Merrinlake's retro lines from its July run now carry a
  cohort's member months under its first month of coverage (every line its member count times the fee), and the
  Medicare Advantage lines are gone.
- 2026-10-25, architecture 14 stage 2: the benchmarks and thresholds as graded columns (26 figures every reader keeps,
  a third of the scored ask figures in architecture 13) were dropped from the prompt; the workbook carries them as the
  elections' context and the write-up names the two practices the stays move.
- 2026-10-25, architecture 14 stage 4 round 1 (target.zip cc4a6fbd821d4dfd): both scored readers filed the default ten
  and missed the call, and the judge returned DETERMINISTIC with FIX_NOW (Callowglen's share 0.002 points from its
  rounding boundary under 23 same-day duplicate visits, the chart graded on sign). Reader A rebuilt every payer's runs
  from the claims, read Kesselcrest's reviewed 99215 lines at their 99214 rate, took Merrinlake's halving as a payment
  reduction and spread Merrinlake's retro lines over the rebuilt members' months, keeping all 52 ask figures (score
  FAIL). Kesselcrest's review moved off the line onto a claim adjustment line (every line now matches its code), the
  world bills one visit a member a day, and the fees narrowed to each payer's July to September total, because a
  run-rebuilding reader reconciles any allocation of fees to the months they cover.
- 2026-10-25, architecture 14 fix pass: the narrowed fee ask (each payer's July to September coverage fees, 3 figures)
  withdrawn before any reader saw it: ceiling.py's cracker kept all three (Merrinlake's retro lines spread by their
  member counts, Pemberglen's from its payment reference), so precut's cracker row read "keeps 3", and a fee ask in
  these remittances has no device a run-rebuilding reader cannot reconcile. The remittances ship as distractors; ask A
  is the one device ask.
- Architecture 14, the network's stays still open at the cut carried at the member cap (2026-10-31, spent at stage 4):
  the repair's judge pass 2 found two graded thresholds a cent off with the 2025 measures within a third of a cent of
  a rounding edge, and the re-judge found the write-up's "all seven past the cap by 31 August" false under a pooled
  per-day reading (4,535.53 a day against the per-kind 6,380), thin margins and the stay amount unfiled. A FIX_NOW that
  fails twice is spent; the world goes with it. Lessons carried into architecture 15: every graded figure at least a
  quarter of its rounding unit from an edge under every defensible conformance, asserted; every factual write-up
  sentence true under every defensible reading of an unfiled amount; call margins no defensible variant comes within a
  few per cent of flipping.
- Architecture 15 draw screens (2026-10-31), each dead before a harness: fisheries observer-coverage discards (task275
  approved on it); a sum of probabilities against a count of shrunken predictions for a threshold count (task253
  approved on it); TNC deadhead at an airport curb (task467's airport ground-transport world); APU minutes from gate
  power draw (a reflex for the field's own analysts once the meter log is in the pack); crop insurance optional against
  enterprise units on prorated production histories (the prorated years print identical unit yields, which the hygiene
  battery flags); a funnel-flow grain bin's discharge order (physics no judge reproduces without a free regime
  parameter, and one of two traceability reflexes lands it); coincidental exact-key matches growing with the comparison
  file (task468's false links on common identifiers told in other words); a vendor's clustered coding audit (a filed
  confidence level plus a batch column points at the variance, readability test 1); queue time from backlog over
  intake (no ETL task type carries it); mine-to-mill change of support (a free choice of support correction, Gate C);
  record-linkage and seasonal-adjustment cells set aside on the directive's batch reading (task250 and task470 hold
  those client domains), the census-register cell on task470 itself.
- Architecture 15 stage 2 (2026-10-31), a limit of 3.0 per cent of the plan's cost on a menu of 2,000, 2,500 and 3,000
  dollars: the 2,500 option sat between the routes with margins under 1.2 on both sides; the resolution now allows
  2,000 or 3,000 dollars at no more than 1.90 dollars per covered person month.
- Architecture 15 stage 2, an ask on the persons at the maximum by relationship: a count the accumulators state
  outright; replaced by the orthodontic balances, whose units cross the migration.
- Architecture 15 stage 2, ask A as shares to one decimal: five of the seven quarters sat within a quarter unit of a
  rounding edge; asked as counts, which have none.
- Architecture 15 stage 3, a simulation that began on 1 January 2024 with nothing carried in: January 2024 held no work
  put off from 2023, so 2025 rose 11 per cent on 2024 and the October 2024 projection missed by 5 per cent, a search
  signal the back-test was meant not to give; a 2023 plan year now runs first and is not extracted.
- Architecture 15 stage 3, members putting work off before meeting the deductible, and new needs on a tooth whose work
  was put off: each opened a fork on the graded figures (the put-off work's deductible; a later claim on the same tooth
  matched by procedure family); a member now weighs a cut estimate only once the deductible is met, and work put off
  stands in for the next year's need on the same tooth and procedure family.
- Architecture 15 stage 3, a sentence in F-17 filing the deductible convention: it would have told a literal reader to
  charge the 2026 claim's deductible on the put-off work; the records carry the convention instead (SF6, SF14).
- Architecture 15 stage 3, a request stamped on the stroke of 5:00 p.m.: "after 5:00 p.m." and the golden's reading
  disagreed on it; no request is now stamped on the cutoff minute.
- Architecture 15 stage 3, the bound routes (every person at the maximum taking the whole rise; a year annualised from
  the day the maximum was met) reach 2,000 dollars without the decisive step, and no menu or limit moves them while
  the golden's correction raises the cost; they stay recorded in the ladder as the build's open exposure, each refuted
  by the records and each missing every graded cost figure.
- Architecture 15 (Pembrook Castings' dental maximum under F-17): the stage 4 judge returned NOT_DETERMINISTIC with
  SEND_BACK and the reconciliation confirmed a withheld rule: F-17 executed word for word on the 2025 claims gives
  increases of 0.83 (2,000) and 1.23 (3,000) and files 3,000, while the golden's 2,000 needed the work members put off
  to the January reset added back, which no shipped text states; the asks also left the put-off column's total, the
  deductible on 34 lines, "still in treatment" and an orphan case open. The slot's lesson: the filed standard's
  word-for-word execution must be the golden, and the difficulty is computing that filed quantity from the data's
  structure, never a correction the standard does not ask for.
- Architecture 16 design (2026-10-31): a third ask on the aluminium Midland recovered from each quarter's dross, read
  from its settlement statements, dropped before data was cut: with the lift date on each settlement line the figure
  is executed by any careful reader, and without it the figure rides the processor's booking lag, which no sentence
  can file without handing it over.
- Architecture 16 design (2026-10-31): the family intensities graded to two decimals, dropped on the measured spread:
  the defensible fits put 6082 billet between 0.260 and 0.268 and the castings between 0.45 and 0.52, so the call is
  graded on the premium and the families earning it, and the prompt pins no rounding on the intensities.
- Architecture 16, the homogenizing furnace's gas allocated by its loads' firing hours (2026-11-07, spent on its first
  portal round): both responses landed the golden premium of EUR 342,000 on the firing-hours allocation, the method a
  careful analyst reaches for, which the hourly gas fitted at R-squared 0.9985, so the fit handed over the route; the
  portal also flagged Domains Fit. The emissions-inventory world and the furnace-allocation driver are spent.
- Architecture 17 draw screens (2026-11-07), each set aside before a card: a linkage precision carried from a
  validation run onto a run with rarer true matches (task446's invariant, error rates carry and the yield moves, already
  screened at task174); claims completion by each nursing facility's own monthly billing day against the extract (the
  trap is per-reporter completion, 181's route, 445's reporters, task451's sender delay); IBNR from each member's
  infusion rhythm across the medical and pharmacy benefits (v14's skeleton: a per-member amount incurred and unbilled,
  read from a second stream, past a per-member threshold); same-event double capture across two lists, an ED-initiated
  treatment start recorded in both (task196's approved driver); chain-linked volume non-additivity (a named correction
  in the accounts manuals, the library test); construction value put in place spread by each project's own endpoints
  (the progress reports back-test the duration scaling, so the fit points at the golden); Medicaid encounter
  completeness by subcapitated vendor (encounter data validation is the actuary's own step); a regional series'
  seasonality rebuilt from its units' histories (one join and a per-cell mean); a year-end processing pattern absorbed
  as seasonality (the change is dated and visible).
- Architecture 17 draw, the due-contact family (2026-11-07, five prototypes): register children counted resident only
  where activity shows, and absence of activity is evidence of departure only where a well-child contact fell due under
  the child's own centre's schedule. District schedules put inactivity at 6 per cent against 36 (the pack's largest
  anomaly); masking it with district emigration biased the golden by +5.4 per cent; centre catchments left the pooled
  route within the golden's own noise (pooled minus golden sd 1.6, golden sd 1.1); a previous cohort's complete outcome
  made the golden exact (sd 0.8) but per-centre calibration landed within 1.4; a recall rule keyed to each child's own
  history removed the anomaly and the district by age-year calibration landed at +0.1 per cent. Its world also sat
  beside task471 v4's register-adjusted municipal population, and its honest label, composition_mix, was banned when
  the family was screened.
- Architecture 17, first prototype of the drawn mechanism (2026-11-07): with schools whose Term 3 unit ended before
  their first sitting day, recalibrating on whole schools that had finished the unit landed the golden in 20 of 20; the
  world gives every Term 3 unit at least five weeks against a sitting in weeks 3 to 5, so no school has finished one
  before it sits and taught responses exist only inside schools, after each school's own last lesson.
- Architecture 17 stage 2 (2026-11-07): both Term 3 units ending inside the sitting window (the prototype's world) is
  not how a ten-week term runs; the generator teaches the units in sequence, the first ending in week 4 or 5 of each
  school's own term and the second at its term end, which first left about 5 per cent of the Term 3 responses taught
  (about 60 per item, the golden 0.24 logits off the truth on the shipped seed) and was widened to a sitting of 6 to 9
  days with the first unit ending 1 to 7 school days after it (about 11 per cent, 150 per item).
- Architecture 17 stage 2 (2026-11-07): drafts composed on the shipped seed's golden estimates put the golden at B on
  redraws whose Term 3 estimates fell the other way; the drafts are composed on the items' taught difficulties and the
  shipped seed chosen from a scan (482025) where every graded figure sits a quarter mark inside its bin, the bank
  picks A, every golden variant keeps the whole marks and every rival route misses C.
- Architecture 17 stage 2 (2026-11-07): golden targets A 27, B 26, C 25 left the bank's pick split between A (8 of 20)
  and B (12 of 20); retargeted to A 26, B 23, C 25 so the bank lands on A in 20 of 20. A Term 3 taught mean of 0.15
  logits put the banked Term 3 items at the hard end of the bank (half a logit above the rest, two of them the bank's
  worst outfit); a mean of -0.85 with the untaught effect held to 0.6 to 1.3 logits puts them 0.20 above, inside the
  spread.
- Architecture 17 asks (2026-11-07): a licence-fee ask (one publisher's stimulus fee repeated on every item line, the
  other's fees in Australian dollars) needed either the agreement's per-stimulus clause or the publisher's invoice to
  find the repetition, the first a filed rule adjudicating the device and the second an oracle tying only under the
  golden; an item-exposure ask could move the call through a disqualified draft; both dropped for the make-up mean.
- Architecture 17 asks, parent review (2026-11-07): with the make-up count unasked and walk-ins absent, the full
  includer (roster join, entries on first name, surname and birth date) kept 6 of 12 ask figures, over two fifths;
  unbooked absentees who sat at a host and reach only the keyed file (D4, their home school through the entry number
  keyed and the register) put a second reconstruction on the sat block, the make-up count joined ask B by shape, and
  the full includer keeps 4 of 16.
