# task482 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 6, drawn 2026-10-22 after architectures 1
to 5 were spent at stage 4: a fresh world and pack in the ETL objective, a community college system pre-equating its
2027 mathematics placement form from a Rasch item bank.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task482.json` (architecture v6, lineage v1 to v5 spent), registered
  2026-10-22 after a pull, `check` re-run on the filed card. Guard WARN only, answered here: `repeat.gate_g` (task273,
  live, decides a descriptive cut over censored records by the method its censoring entitles; here the method carries
  an item parameter across the measurement condition it was calibrated under). Nearest drivers 0.07 and below.
- **Redrawn at the draw, and why the replacements are the honester labels.** The first draft BLOCKed on `ban.role`
  (research_desk) and `ban.forum` (committee_or_panel), both against task249 v6, and on `ban.forcing_event`
  (launch_or_rollout) against task177 v2. Placement scores in this system are policy the State Board of Community
  Colleges approves, so the forum is trustees_or_governors and the forcing event the Board's approval meeting
  (vote_or_meeting) ahead of the form's go-live; the stakeholder runs the placement programme rather than a research
  office, so the role family is programme_officer.
- **Pairing:** Education & Learning Sciences, task type `item-response-theory-test-equating`, which serves ETL: the
  item bank in two systems, the two delivery platforms' exports of the 2026 attempts, the form maps and the technical
  report conformed into Form 27A's score conversion, the load file the new platform reads to place each student.
- **The decision and the quantity:** the Brackett Plains Community College System places entering students into
  college algebra, corequisite college algebra or developmental mathematics by their raw score on the Quantitative
  Placement Inventory (QPI). Form 27A goes live on 1 March 2027 and its two placement scores must be approved by the
  State Board on 18 February, before any student sits it, so the form is pre-equated from the bank. Each placement
  score is the lowest whole raw score at or above the expected raw score, on Form 27A, of a student standing exactly
  at that placement's standard on the bank scale (the technical report files both standards from the 2022 standard
  setting). Forward facing: the scores govern every placement from 1 March 2027.
- **Shape:** `04`, setting one dial twice: the two placement scores and the expected raw score each rests on, the
  default path's scores as the rivals, the conversion's placement level at every raw score near each cut; the asks
  carry each college's 2026 placements by level (14 colleges by two levels, 28) and the 2026 field test's accepted
  items by content strand; a curve chart's named parts and the three files. About 50 criteria, sized at stage 2.
- **Strategy:** `other` (no family on the list states it: a parameter calibrated under one measurement condition is
  carried to another by the condition's effect, measured where the same items were presented in varied orders); Gate
  G `method_or_model_selection`; gap `objective` (the bank's difficulty is a correct figure for the slot it was
  calibrated in, not the difficulty the form's curve needs); pattern none; generators G14 (does the calibrated value
  apply under this condition, decisive) and G16. Layer 2 family `field_method`, pattern `own:bank difficulties carried
  from their calibration position to their operational position before pre-equating`.
- **World:** an unnamed state of the United States; the Brackett Plains Community College System, fourteen colleges,
  about 9,600 QPI attempts in the 2026 testing year (1 February 2026 to 31 January 2027) on two delivery platforms,
  the old one until 30 June 2026 and the new one from 1 July. People from `guard.py names --geo 'United States' --seed
  482`: Breanna Graham (Director of Placement and Developmental Mathematics) and John Huang (Psychometrician).
- **Forcing fact:** the State Board approves Form 27A's placement scores on 18 February 2027; the form goes live on 1
  March 2027.
- **Forum and forcing event:** trustees_or_governors, vote_or_meeting. Organisation university_or_school; role
  programme_officer.
- **Form design (both platforms, every form):** 60 scored items, a 20-item anchor block in positions 1 to 20 kept in
  place on every form, then 40 unique items, then an unscored 10-item field-test section in positions 61 to 70. The old
  platform delivered each form in two fixed versions (the unique section and the field-test section in reverse order on
  version B); the new platform shuffles the unique section and the field-test section for each attempt. Field-test
  items are calibrated with the anchor block fixed at its bank values; unique items are retired after their
  operational year. Form 27A's 40 unique items are new: every one was calibrated in a field-test section.
- **Data-native sentence:** at the same ability a student answers an item less often the later it comes, by about
  0.0075 logits per position in the 2026 attempts, so a difficulty calibrated in the field-test section (positions 61
  to 70) states the item harder than it will be at positions 21 to 60 on Form 27A, by about 0.19 logits; the bank's
  difficulties as filed put the expected raw score at the college algebra standard near 27.9 (placement score 28), the
  difficulties carried to their Form 27A positions near 29.5 (placement score 30).
- **The WHAT screen.** Population: Form 27A's 60 scored items as students will sit them (the unique section shuffled
  for each attempt). Outcome: the expected raw score of a student at each standard. Unit: the whole raw score.
  Comparison: the lowest whole raw score at or above that expectation. Window: the form's live period from 1 March
  2027. The decisive step settles none of them: it is how each item's difficulty on Form 27A is estimated from a bank
  difficulty calibrated elsewhere on an earlier form, which nothing files.
- **Sources, one line each:**
  - The client's IRT equating rigor patterns (anchor screening; nonequivalent groups through anchors): here no groups
    are linked and no anchor drifts; the item's own parameter is carried across a presentation condition.
  - Kingston and Dorans (1984), item location effects in IRT equating and adaptive testing; Debeer and Janssen (2013),
    position effects as a Rasch facet: the field's method (a position term in the Rasch model, estimated where order
    varies) is what the golden runs.
  - Kolen and Brennan, Test Equating, Scaling, and Linking: pre-equating rests on item parameters holding in their
    operational context.
- **Same-puzzle and same-driver tests:** (objective, none, dial_setting) and (objective, none,
  method_or_model_selection) against the last twelve builds, lineage included: no match (the guard's tests pass).
- **Abstraction test:** the nearest drivers stripped of nouns (task190's size-proportional sample, task255's floored
  record, task87's capped procedure) neither carry a calibrated parameter across a condition nor measure the
  condition's effect from varied orderings; within this objective the IRT builds link groups through anchors
  (task450), convert by distribution matching (task464), or rejected a judged anchor (task471 v2) and rapid guessing
  (task479 v4) as planted, and none moves an item's own parameter.

## Default path

1. Read QPI-TR-2027: a placement score is the lowest whole raw score at or above the raw score a student exactly at
   the standard is expected to obtain on the form's 60 scored items (section 7); the standards are 0.20 and -0.70
   logits on the bank scale (section 6); Itemstore holds difficulties in bank units, 500 plus 100 times the logit
   (section 4).
2. Converted the assembly pool's difficulties to logits and took Form 27A's 20 anchor items and 40 unique items from
   qpi_form_27A_assembly.csv.
3. Summed the 60 items' Rasch probabilities at each standard, the form's test characteristic curve from the bank
   difficulties as filed: 28.2 at College Algebra (28.204) and 17.5 at Corequisite College Algebra (17.489).
4. Took the lowest whole raw scores at or above them.

Ends on: College Algebra from 29, Corequisite College Algebra from 18.

Golden: College Algebra from 30, Corequisite College Algebra from 19.

## Stump sentence

The default path reads each item's bank difficulty as its difficulty on Form 27A and sets College Algebra from 29,
Corequisite College Algebra from 18, because the form's 40 unique items carry the difficulties of their field tests,
calibrated in the old platform's field-test section at positions 61 to 70, and at the same ability a student answers
an item less often the later it comes (0.0075 logits a position across the 2026 attempts, two fixed orders on the old
platform and a fresh order for every sitting on the new one); carried from the section's mean position, 65.5, to the
positions 21 to 70 they take on Northgate Assess (mean 45.5), each unique item is 0.15 logits easier than its bank
record says, the expected raw scores at the standards rise from 28.2 and 17.5 to 29.5 and 18.5, and the placement
scores to 30 and 19.

## Three rules

Task type: item-response-theory-test-equating (Education & Learning Sciences), pre-equating a new form's raw scores
to the bank scale's standards before it goes live, a task type serving Data Extraction & Conformation (ETL): the bank,
the two delivery platforms' exports and the forms' layouts conformed into Form 27A's score conversion, the load file
the new platform reads to place each student.

Domain test: psychometrics: the deciding quantity is Form 27A's test characteristic curve at each standard, which
needs each item's difficulty where it sits on the form as delivered; the field estimates item position effects as a
facet of the Rasch model from administrations that vary item order (Kingston and Dorans, 1984; Debeer and Janssen,
2013) and carries field-test difficulties to their operational positions before pre-equating; with another field's
nouns there is no form, no item position, no characteristic curve and no standard on a latent scale, so nothing is
left to decide.

Swap: put "hospital" for "college" or "megawatt-hours" for "raw score" and nothing reads: there is no item calibrated
in a field-test section, no shuffled form and no expected number correct at a latent standard; the abstract move (a
parameter calibrated under one condition carried to another) needs the field's own estimator, the Rasch model with a
position term fitted to responses at the person-by-item grain, which no other field's data supply.

Layer 1: the item bank in Itemstore's bank units; the old platform's wide export (a 70-character response string per
sitting in its version's delivered order, US dates, local time) against the new platform's long item-response export
(UTC, delivered seq, field-test items scored but not counted); item identifiers in two schemes (Itemstore and the old
platform's) joined through the layout; the old platform's student numbers per college joined to the new platform's
identifiers through the cutover crosswalk; the review log's decisions at the session grain, three of them withdrawn;
omitted items as an asterisk or a blank. Each is written by the system named, none is placed to be caught, and each
read the natural wrong way leaves the call where it is (checks.py R2a to R2g).

Layer 2: field_method, an item position effect in pre-equating: a field-test difficulty is the item's difficulty at
the field-test section's positions; the 2026 attempts' varied orders identify the position term within each item, and
each unique item is carried to the positions it takes on Form 27A before the curve is summed.

Decisive step: estimating the position term from the 2026 attempts (0.0075 logits a position, 0.15 over the 20
positions between the field-test section's mean and Form 27A's) and carrying each of Form 27A's 40 unique items to the
positions 21 to 70, which moves the expected raw scores at the standards from 28.2 and 17.5 to 29.5 and 18.5 and the
placement scores from 29 and 18 to 30 and 19.

No decoy: nothing is planted: the bank, the forms, both platforms' exports and the documents are what each system
writes; no memo, report or earlier figure proposes scores for Form 27A, states a position effect or says how any
form's scores were computed; the 2026 forms' approved scores ship as history for forms whose unique items are retired
and absent from the pool.

Not semantics: every field, unit, code and clock read correctly (bank units to logits, the versions' delivered order,
the new platform's seq, the unscored field-test sets) still leaves the careful route summing the bank difficulties as
filed; no field holds a carried or operational difficulty and nothing says one is needed; the step is an estimate
(the position term) and the carry it sets, not a reading.

Not rule application: the report files the standards, the raw score, the placement score's definition and how Form
27A is delivered (the WHAT); no filed rule or procedure says how an item's difficulty on a form is obtained from its
bank record or that position matters.

Analyst test: a strong analyst who conforms the bank's units, joins Form 27A's assembly to the pool and reads the
report correctly sums the bank difficulties as filed and sets College Algebra from 29, Corequisite College Algebra
from 18 (expected raw scores 28.2 and 17.5); only the difficulties carried from the field-test section to Form 27A's
positions give 30 and 19 (checks.py R3a on the generator's clean truth: 29.429 and 18.436 against the bank's 28.204
and 17.489).

Estimand: QPI-TR-2027 section 7: each placement score is the lowest whole raw score at or above the raw score that a
student whose ability is exactly at the standard (section 6: 0.20 and -0.70 logits) is expected to obtain on the
form's 60 scored items; section 3 files how Form 27A is delivered (the anchor block in positions 1 to 20, the unique
items and the field-test set shuffled in positions 21 to 70 for every sitting).

No certified replay: no conversion of Form 27A ships; the 2026 forms' approved scores cannot be recomputed by either
route (their unique items are retired and not in the pool), so no certified figure ties under the default path.

Lesson: a bank difficulty is the item's difficulty where it was calibrated; where a student's chance on an item falls
with its position, a form's expected scores need each item at the positions it will take, estimated from
administrations that varied the order, and a field-test section at the end of the form makes every new item look
harder than it will be.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the bank difficulties as filed, the default path (29 and 18) | report s.7 the estimand: fires | difficulty_bu: fires | a form's characteristic curve from bank difficulties: fires | none | none | one sum | readable |
| R1, the 2026 forms' scores carried over by analogy (28 and 18) | report s.7's history table: fires | none | last year's scores: fires | none | none | a lookup | readable |
| R2, the anchor block carried too, or every item carried to position 1 (32 and 21; 33 and 21) | none | seq: fires | remove a nuisance effect from every item: fires | none | none | a shift | readable |
| G (decisive), the position term fitted to the 2026 attempts and each unique item carried from 65.5 to positions 21 to 70 (30 and 19) | no sentence says position matters or how a bank difficulty applies on a form | no column holds a position term or a carried difficulty | no reflex refits the 2026 responses to price a bank record | none | none | none | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | raw score | number correct of the 60 scored items | all 70 delivered | not the report's | report s.2; every old-platform raw score recomputes on 60 (asserted) |
| SF2 | the standards' scale | logits, 0.20 and -0.70 | bank units, 520 and 430 | same call (asserted) | report s.4, s.6 |
| SF3 | expected to obtain | the Rasch expected number correct on the form's 60 scored items | an observed median of students near the standard | none observed: no student has sat Form 27A | report s.7 |
| SF4 | lowest whole raw score at or above | the ceiling of the expected raw score | the nearest whole number | 29 and 18 under marginal maximum likelihood (29.48 and 18.50): not the report's | report s.7 ("at or above") |
| SF5 | Form 27A as delivered | the shuffle averaged over positions 21 to 70 | each unique item at the mean position 45.5 | same call (asserted) | report s.3 |
| SF6 | the anchor block on Form 27A | its bank difficulties, calibrated in place | carried like the unique items | 32 and 21: not the report's | report s.2 (the block kept in positions 1 to 20 on every form) and s.4 (its 2022 base calibration fixed the scale) |
| SF7 | a field-test calibration's position | the section's mean, 65.5, on both versions | an item's version A slot only | same carry for every slot (61 to 70 on A, 70 to 61 on B) | report s.3 |
| SF8 | the 2026 attempts the position term rests on | every attempt | valid sittings only | same call (asserted) | not a filed choice; both converge |
| SF9 | the position term's estimator | marginal maximum likelihood, the anchor block fixed | joint maximum likelihood; a population-averaged slope | same call (asserted); the conditional estimators agree on 29.5 and 18.5 | report s.4 (Rasch) |
| SF10 | the position term's form | linear over positions 21 to 70 | fitted on 21 to 45 or 46 to 70 alone | same call (asserted) | the data (0.0068 and 0.0077) |
| SF11 | the platforms | both | either alone | same call (asserted) | the data |
| SF12 | rounding | half up to one decimal from the unrounded sum | none | none | the prompt's rounding |
| SF13 | the college that placed a student | the college they were registered through when they sat the placing sitting | the college now on the student record | every college's placements differ: not the policy's | Policy 4.12 s.3 |
| SF14 | a student | one person across both platforms and both identifiers | each identifier | every college's students placed and second sittings differ: not the policy's | Policy 4.12 s.3 (a student's placement, once) |
| SF15 | invalidated sessions | left out, withdrawn invalidations restored | all attempts; invalidations without their withdrawals | figures differ: not the policy's | Policy 4.12 s.4 |
| SF16 | sat twice | two sittings | two attempts, an invalidated one included | not the policy's | Policy 4.12 s.4 |
| SF17 | the window's dates | local dates, 1 March 2026 to 31 January 2027 | UTC dates | same figures (asserted: both boundary days are Sundays) | the prompt |
| SF18 | a tie between two sittings | the later sitting places the student | the earlier | 32 students' colleges differ: not the policy's | Policy 4.12 s.3 |
| SF19 | the files the call reads | the pool, the Form 27A assembly, the 2026 layout, both platforms' responses, the report | the attempt records, score reports, review log, crosswalk, centres | same call (asserted, X1) | the estimand |

## Ladder

Built figures, read from the cut pack by `generator/bundle.py` (expected raw score at each standard, then the placement
scores).

- **R0, the bank difficulties as filed, the default path: 28.2 and 17.5, College Algebra from 29, Corequisite College
  Algebra from 18.** Dies to the field-test section: the 40 unique items were calibrated at positions 61 to 70 and will
  sit at 21 to 70.
- **R1, the 2026 forms' approved scores carried over by analogy (28 and 18).** Dies to the forms: Form 27A's items are
  not Form 26A's, and the history table records approvals, not a method.
- **R2, the anchor block carried too (32 and 21), or every unique item carried to position 1 (33 and 21).** Dies to
  the report's sections 2 and 4: the block is kept in positions 1 to 20 on every form and was calibrated there, and an
  item on Form 27A takes positions 21 to 70, not 1.
- **G: 29.5 and 18.5, College Algebra from 30, Corequisite College Algebra from 19.** The position term (0.0075 by
  marginal maximum likelihood; 0.15 logits over the carry) applied to each unique item at each position it can take.
- **Margins:** every licensed member (marginal maximum likelihood at 41 or 21 nodes, joint maximum likelihood, valid
  sittings only, either platform alone, a population-averaged slope, the slope fitted on 21 to 45 or 46 to 70, each
  item at the mean position) files 30 and 19, every one 0.2 or more inside both bins (checks.py G2, G5); the
  conditional estimators on every 2026 attempt agree on 29.5, 18.5 and the 0.15 carry (G3, G4).
- **Position, separation and dominance:** a dial set twice, not a ranking; there is no decoy to dominate.
- **Worth:** the call, the two expected raw scores and the carry; the default path keeps none of them.

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | Form 27A's 60 scored items as delivered (SF1, SF5); for the asks every student with a sitting from 1 March 2026 to 31 January 2027, once (SF14) |
| 2 | Unit of account | the whole raw score; the student |
| 3 | Attribution window | the asks: 1 March 2026 to 31 January 2027, local dates (SF17); the call: the form's live period from 1 March 2027 |
| 4 | As-of dating | the pool export of 3 February 2027; the attempts to 31 January 2027 |
| 5 | Version basis | QPI-TR-2027 supersedes the 2026 report; the pool's difficulties are their calibrations' |
| 6 | Denominator | none |
| 7 | Weighting | none: every scored item counts once |
| 8 | Window length | the call's form year; the asks' eleven months |
| 9 | Boundary inclusivity | "at or above" the expected raw score (SF4) |
| 10 | Rounding path | the ceiling of the unrounded expected raw score; reported half up to one decimal (SF12) |
| 11 | Tie-break | the later sitting places the student on a tie (SF18) |
| 12 | Maturity and censoring | the asks' window closed on 31 January 2027; no sitting is open |
| 13 | Order of operations | conform the bank's units, score the 2026 responses, fit the position term, carry the unique items, sum, take the ceiling |
| 14 | Row order | none |
| 15 | Duplicate resolution | one student across identifiers (SF14); no duplicate rows ship |
| 16 | Identity normalisation | item identifiers through the layout; old-platform student numbers through the crosswalk; students across identifiers on birth date, sex, high school code and registration date |
| 17 | Netting | none |
| 18 | Dimensional units | logits and bank units (SF2); raw scores; students |
| 19 | Code and status semantics | the old platform's placement codes (131, 131C, 091); the review log's decisions; never the stump |
| 20 | Integerisation | the placement score is whole by definition |
| 21 | Clause scope | report s.7 governs Form 27A's scores; Policy 4.12 governs the 2026 placements |
| 22 | Forward window contents | Form 27A from 1 March 2027, placing every first sitting until Form 28A |

## Literal reader

Executed word for word, the report fixes the estimand: the lowest whole raw score at or above the raw score a student
exactly at each standard is expected to obtain on Form 27A's 60 scored items, with the form delivered as section 3
says (the anchor block in positions 1 to 20, the unique items and the field-test set shuffled in 21 to 70). The
expected score of a student at a standard is a property of how students answer the form as delivered, so the
candidates are the bank difficulties as filed and the difficulties the items will have where they sit. The data
separate them: in the 2026 attempts every unique and field-test item was answered at 20 or more positions, and at the
same ability its chance falls by 0.0075 logits a position, linear across 21 to 70 (0.0068 on 21 to 45, 0.0077 on 46
to 70); the pool's items were calibrated at the field-test section's positions, 61 to 70, and every estimator of the
term files 30 and 19, while the bank difficulties as filed file 29 and 18 (checks.py G2, R3b).

WHAT screen (stumping 1.2): population, report s.2 and s.3; outcome, s.7; window, s.8; unit, the raw score; comparison,
s.6 and s.7. The decisive step settles none of them.

## Oracles

None. No control, published figure or conversion ties only under the golden: the 2026 forms' approved scores cannot be
recomputed (their unique items are not in the pool), and no figure for Form 27A ships. The asks' files carry no total
that ties under one handling: the score reports, the review log and the crosswalk tie under every handling of the
devices.

## Ask sheet

The Board's packet carries each college's 2026 placements beside the scores it approves, the baseline the colleges
plan their fall 2027 sections against (H18: a component of the call's case, the input the call consumes, the 2026
sittings, traced to the colleges that placed their students). The asks read no row the call reads in the columns the
call reads: the call uses the 2026 responses' items, positions and scores; the asks use the sittings' identities,
colleges, levels and sessions (checks.py X1 to X3).

- **Ask A, each college's students placed into College Algebra and into Corequisite College Algebra: 28 figures, whole
  students.** Path: both platforms' attempt records, the score reports, the review log, the crosswalk and Policy 4.12
  (five files, eleven columns). Primary device: D7, a field overwritten later: the new platform's attempt records
  carry the college now on the student's record, so a student who moved their registration after sitting shows the new
  college on the earlier sitting (384 sittings, every college gaining and losing); only the score report sent
  automatically at the sitting records the college that placed them (Policy 4.12 s.3). Every college's two figures
  move (checks.py A1). Hazards: the re-keyed students (Ask B's primary) put a second sitting's lower level in as another
  student (Corequisite College Algebra 107 high across the System); the review log (A5, A6). Stops: the attempt
  records' college (the cracker and the mirror: every figure off); the score reports' college with identifiers as
  recorded (9 Corequisite figures still off); the golden. Realism: a delivery platform's export joins the student
  record as it stands.
- **Ask B, each college's students placed in all and how many of them sat twice: 28 figures, whole students.** Path:
  the same files. Primary device: D1, the same students under two identifiers: from 1 October 2026 the new platform
  keys students by a new nine-digit identifier, the same form as the old, so the 259 students who sat before and after
  the change appear as two students who each sat once; only birth date, sex, high school code and registration date
  together tie them (three of the four over-merge 109 students, checks.py A4). Every college's two figures move (A2).
  Hazards: the moved registrations (Ask A's primary) and the review log. Stops: identifiers as recorded (256 students
  too many, 256 second sittings too few, across the System); three fields (109 too few, 84 second sittings too many);
  the golden. Realism: a student identifier changes with no history kept, and a nine-digit number looks like a
  nine-digit number.
- **The construction layer:** the call, the two expected raw scores, the carry, the conversion and the curve; the
  cracker has them.
- **Main population zero-counts (asserted):** the call reads no attempt record's identity, college, level or session
  field and no score report, review log or crosswalk row (X1); the device rows leave the position term within 0.0001
  (X3).
- **Hazard table (asserted):** the review log ignored moves 18 figures and its withdrawals ignored 14 (A5, A6); the
  three-field link moves 51 of 56 (A4).
- **Referee:** none.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, each college's placements into the two levels | the crosswalk applied, the review log with its withdrawals, Policy 4.12's higher level and later sitting, each sitting's college from its attempt record: 0 of 28 | miss |
| B, each college's students placed and second sittings | the same, students as their identifiers: 0 of 28, and 0 of the four System totals | miss |

Pair ceiling: 28.5 (weights 38 / 7 / 55, r 5: the cracker keeps the call and the instructions, 45.0; the mirror at the
default path keeps r and the instructions, 12.0; the asks read alike under both, 0 of 60)

Mirror leakage: 0.0 per cent of ask weight

Measured by: generator/ceiling.py

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Effect (asserted) |
|---|---|---|---|---|
| bank units | Itemstore | the pool export | logits read as bank units | none once the standards are taken in the same unit (R2a) |
| version B in reverse order | Kestrel Testing Suite | the old platform's attempts | every sitting read in version A's order | the call holds (R2b) |
| item identifiers in two schemes | Itemstore, Kestrel Testing Suite | the layout, both exports | the old platform's rows dropped | the call holds (R2c) |
| field-test items scored but not counted | Northgate Assess | the item responses | field-test responses left out of the fit | the call holds (R2d) |
| invalidated and withdrawn sessions | the Office | the review log | ignored | the call holds (R2e); ledgered asks move (A5, A6) |
| omitted items | both platforms | both exports | dropped rather than scored 0 | the call holds (R2f) |
| UTC against local time; the cutover crosswalk; the session grain | both platforms, the migration, the Office | the exports, the crosswalk, the review log | each misread | the call reads none of them (R2g, X1); ledgered asks only |

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
