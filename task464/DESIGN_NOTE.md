# task464 design note: the 2027 Adolescent Literacy Partnership grants (architecture 2)

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first: architecture 1 (the
Wendlemere building emissions slate) was sent back by the determinism judge and a first redraw was dropped before
registration; architecture 2 is drawn afresh in the ETL objective.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task464.json` (architecture v2, architecture 1 in `lineage`), registered
  2026-10-17 09:40 UTC, guard WARN only. Answered: the first name Jeffrey appears in one older build (task141); the
  state department of education is the honest organisation (government_agency, overused); Gate G
  method_or_model_selection repeats across the batch, the honest mechanism; the question form is which, because the
  call picks districts. Differentiated: task450 (common-item linking of two forms given to different groups, the
  instrument's change separated from the groups' difference; here one group took both tests and the trap is a
  regression's prediction used as a concordance) and task184 (an offence spread over its occurrence window).
- **Seed:** none kept. ET21's world (a building emissions slate) is spent with architecture 1; the slot is re-drawn in
  a new world.
- **Pairing:** Education & Learning Sciences / item-response-theory-test-equating / ETL, own pattern "concordance by
  distribution matching, not regression". Placing a retired test's scores on a new test's scale is the task type's own
  work, and the conformed file (each counted student's latest grade 8 result and its level on the new scale) is the
  dataset the grants are set on. The task type is the least drawn of the six that serve ETL (task450 alone), and none
  of its three listed patterns (DIF matched on ability, anchor drift, anchor-based equating for nonequivalent groups)
  is this mechanism.
- **Shape:** 01, a ranked list under a cap: the six of fourteen applicant districts funded, every applicant's grade 9
  and 10 students at Level 1, the first district left out and its gap to the sixth, and a chart; the conformed file and
  the ask add the rest.
- **Strategy:** other (scale linking). The decisive step is the field's concordance between the retiring and the new
  test, on the population gap (a regression's predicted scores are not the scores the 2025 cohort would have had, and
  the grants count a distribution's tail) with G1 (a score on one scale read on another's) and G16 (method selection).
  Gate G method_or_model_selection.
- **World:** an unnamed state of the United States. Its Department of Education replaced the Grade-Level Reading
  Assessment (grades 3 to 8, last given in spring 2025; a fixed 30-item paper form per grade whose raw-to-scale table
  reports scale scores from 150 to 450, so only 31 scale scores occur on each form, six to eleven points apart near the
  Level 1 boundary; four levels) with the Statewide Literacy Measure (first given in spring 2026; adaptive, any integer
  from 2100 to 2900; four levels). In spring 2026 the Office of Assessment ran a bridge study: the grade 8 students of 24
  public middle schools drawn at random took the retiring test's grade 8 form as well, the order set by school. The
  2027 Adolescent Literacy Partnership grants go to the six of the fourteen districts that filed a notice of intent with
  the most students in grade 9 or 10 on the roll on 1 October 2026 whose latest grade 8 state reading result is at the
  Measure's Level 1 (a grade 8 score below 2415), a retiring-test result counted at the level it places at on the
  Measure's scale. This year's grade 9 took the new test in grade 8; grade 10 took the retiring one. The 2025 grade 8
  cohort read less well than the 2026 one statewide (0.20 standard deviations; its retiring-test mean 291.3 against the
  bridge sample's 301.3 on the same form). The vendor's June student file reports performance levels on the cut scores
  known in June: the Board adopted grade 8's on 11 June 2026 and set grades 3 to 7 on 13 August 2026.
- **Forcing fact:** the State Board of Education awards the grants at its December 2026 meeting for calendar 2027; the
  call faces forward (the 2027 grants on the students now in grades 9 and 10).
- **Forum and forcing event:** trustees_or_governors (the State Board of Education), budget_or_appropriation (the 2027
  grant appropriation). Organisation government_agency; role programme_officer. Personas from `guard.py names --geo
  "United States" --seed 464`: Jeffrey Warren (the programme's director, who issues the grant rules) and William
  Holloway (the assessment office's psychometrician who ran the bridge study).
- **Data-native sentence:** the state changed its reading test after spring 2025, so this year's grade 10 carries only
  the retiring test's grade 8 scores while grade 9 carries the new test's, and the only link is a bridge study in which
  each student's two scores both carry measurement error, so the regression of one score on the other is flatter than
  the line that matches the two scales, and placing each 2025 score at its regression prediction pulls the low scores
  toward the bridge sample's mean and out of Level 1.
- **The WHAT screen.** The estimand's five parts are filed by the grant rules: the population (students in grade 9 or 10
  on the roll of each applicant on 1 October 2026), the outcome (the latest grade 8 state reading result at the new
  test's Level 1, a 2025 result counted at the level it places at on the new scale), the window (the latest grade 8
  administration, spring 2025 or spring 2026), the unit (students) and the comparison (the fourteen applicants, the six
  with the most). The decisive step settles none of them: it is how a 2025 score is placed on the new scale, a
  regression's prediction or a concordance that matches the two tests' score distributions, two ways of estimating one
  filed quantity, and the bridge data rule out the easy one (placed by the regression, 11.1 per cent of the bridge
  students sit at Level 1 against 15.7 per cent on the new test itself).
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, item-response-theory-test-equating: DIF, anchor drift and
    nonequivalent-groups equating are the listed patterns; this build takes the linking design itself (a single-group
    bridge) and the decision between prediction and scale alignment, which none of them covers.
  - `stumping/references/client/two-layer-task-design.md`, estimation that fits the data: both variables carry error,
    so the least-squares line of one on the other is attenuated; here the attenuation decides who counts at Level 1.
  - The field's own practice: tests are placed on a common scale by equating or concordance (equipercentile or linear,
    symmetric and invariant across groups), and a regression of one test on the other is a prediction, not a linking;
    the build files neither, it files the quantity.
  - `dataset-generation/references/layer1-messiness.md`: two vendors' layouts and identifiers, not-tested and
    invalidation codes with make-up sessions, transfers between districts, a merged district, enrolment spells, new
    arrivals and nonpublic test takers; none on the decisive step.

## Default path

1. Read the grant rules: for each of the fourteen applicants, count the students in grade 9 or 10 on the roll on
   1 October 2026 whose latest grade 8 state reading result is at the Measure's Level 1 (a grade 8 score below 2415), a
   retiring-test result counted at the level it places at on the Measure's scale; fund the six with the most.
2. Conform the two vendors' files: the retiring test's 2025 rows keyed to state identifiers through Calderwood's
   test-taker crosswalk; the new test's 2026 rows; a make-up session's score after an invalidation; absent and exempt
   rows left out.
3. Take the October 2026 enrolment spells that cover 1 October in grades 9 and 10 of the applicants (Ashgrove-Fenley as
   one district) and each student's latest grade 8 result.
4. Grade 9 on the new test: Level 1 below 2415.
5. Place the 2025 retiring-test results on the new scale with the bridge study: regress the new test's score on the
   retiring test's (3,968 students in 24 schools, slope 1.39), take each 2025 score's predicted new-scale value and count
   it at Level 1 when the prediction is below 2415 (retiring scores of 231 and below).
6. Sum each applicant's grade 9 and 10 students at Level 1 and fund the six with the most.

Ends on: Harlenbrook funded in Elmorrow's place (Harlenbrook 323 against Elmorrow 315)

Golden: Elmorrow funded and Harlenbrook the first left out (Elmorrow 368 against Harlenbrook 353, a gap of 15)

## Stump sentence

The default path places each 2025 retiring-test score at its regression prediction on the new scale, which pulls the
low scores toward the bridge sample's mean and out of Level 1, so it counts too few of the grade 10 students at Level 1
and lands on Harlenbrook funded in Elmorrow's place (Harlenbrook 323 against Elmorrow 315), where the bridge study's
concordance funds Elmorrow at 368 and leaves Harlenbrook out at 353.

## Three rules

Task type: item-response-theory-test-equating: placing the retiring test's scores on the new test's scale through a single-group bridge study to build one conformed dataset of grade 8 reading levels, a task type serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each district's count of students below the new test's Level 2 cut when its grade 10 students were measured only on the retiring test; psychometrics places one test's scores on another's scale by a concordance that matches the two score distributions (equipercentile or linear linking, symmetric and the same in every subgroup when the tests are equally reliable), while a regression of one score on the other is a prediction that pulls every converted score toward the sample's mean.

Swap: "the six hospitals with the most patients below the new triage score's level 2, a third of them scored only on the old score" keeps the shape and loses the move: no bridge sample of two error-laden measures of one ability, no reported scale with performance cut scores, no field standard placing one scale on another by matching distributions, so the swapped call is a lookup and the linking is what this task tests.

Layer 1: two vendors' layouts and identifiers (retiring-test booklets scanned without a pre-ID label carry only the vendor's test-taker number, joined through its crosswalk), absent, exempt and invalidated sessions with make-ups, the merged district's predecessor codes in both test files, students tested in one district and enrolled in another, enrolment spells (September transfers, late entrants, September withdrawals), arrivals with no state record, nonpublic test takers now in public high schools and the files' other grades; each written by the system that produces it, none placed to be caught, each neutral on the call (asserted).

Layer 2: field method (scale linking): the call flips on linking the two tests by matching their score distributions in the bridge study instead of predicting new-test scores from retiring-test scores by regression.

Decisive step: placing the retiring test's 2025 scores on the new scale with a concordance from the single-group bridge study (every equipercentile convention and linear linking place 241 and below at Level 1), not a regression prediction (231 and below), the field's choice between linking and prediction.

Not semantics: every field, code, unit and definition read correctly (the 2415 cut, the latest grade 8 result, the count day, the make-ups, the crosswalk, the merged codes) still leaves the regression route on Harlenbrook, because the error is in how a score is carried from one scale to the other, which no field or definition sets.

Not rule application: the rules file the population and the outcome and no rule or procedure says how a retiring-test score is placed on the new scale; executing every filed rule with a regression placement funds Harlenbrook, so the step no rule performs is the choice of a linking method.

Analyst test: a strong analyst who conforms both vendors' files, keys each student through the count-day spells, takes each latest grade 8 result and applies the 2415 cut places the 2025 scores by the bridge regression and lands on Harlenbrook funded in Elmorrow's place (Harlenbrook 323 against Elmorrow 315), executed in checks.py on the generator's clean truth.

Estimand: alp_2027_grant_rules.pdf, sections 3 and 4: each applicant's students in grade 9 or 10 on its roll on 1 October 2026 whose latest grade 8 state reading result is at the Statewide Literacy Measure's Level 1 (a grade 8 score below 2415), a Grade-Level Reading Assessment result counted at the level it places at on the Measure's scale; the six applicants with the most.

No decoy: nothing is planted to be caught; no file states a regression, a predicted score, a conversion, a concordance or a linking method, no memo or briefing argues for a method, the bridge memo describes the study's design and participation only, and no file counts or ranks the applicants.

No certified replay: no certified or published figure reproduces a method; the bridge memo's means, standard deviations and correlation describe the sample under every method, and no table of converted scores or district counts ships.

Lesson: a score from one test placed on another test's scale to count students below a cut must be linked by matching the two distributions, because a regression prediction regresses to the mean and empties the tails; no build on file teaches the choice between prediction and linking (task450 links two forms through common items given to different groups).

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 each 2025 score placed at its regression prediction from the bridge (231 and below; Harlenbrook; the default path) | the rules count a result "at the level it places at on the Measure's scale", which a predicted score satisfies | the bridge file pairs each student's two scores | yes: predict the new score from the old | no | no | one fitted line | readable |
| R0b a classifier: Level 1 where the bridge's chance of Level 1 at that score passes one half (a logistic fit, or the score's majority) (231; Harlenbrook) | none | the pairs | yes: classify each score by its likeliest level | no | no | one rule | readable |
| R1 the two cohorts matched statewide by percentiles or z-scores (231; Harlenbrook) | none | the two statewide files | yes: standardise both tests | no | no | one match | readable |
| R1b the retiring test's own levels, Below Basic read as Level 1 (220; Harlenbrook and Garnet Hills ahead of Elmorrow) | the guide's level table | the file's performance level column | yes | no | no | none | readable |
| R2 the retiring score at the cut predicted from the new score, inverse regression (249; the golden slate, every count high) | none | the pairs | yes | no | no | one fitted line | readable |
| R3 a concordance matching the two score distributions in the bridge (241; decisive) | no: the rules file the population and the outcome, the memo the study's design; no sentence names a concordance, equating, linking, a percentile match, an equivalent or a conversion | no column holds an equivalent or a converted score; no table of equivalents ships | no: the prediction reflexes and the cohort match land on 231 | no | no | no: the move is the choice of a distribution match, not a figure | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | on the roll on 1 October 2026 | an enrolment spell whose entry is on or before 1 October and whose exit is blank or on or after it (an October withdrawal counts) | every spell in the extract (late entrants, September withdrawals, closed transfer spells and October moves kept); only the spells still open at the extract | same call under each (asserted) | the rules' count day; no spell opens or closes on 1 or 2 October (asserted) |
| SF2 | each applicant's students | the district of the count-day spell | the district of the grade 8 test | same call (asserted) | the rules ("on its roll") |
| SF3 | latest grade 8 state reading result | the most recent grade 8 administration that produced a score, a make-up session's score after an invalidation | the earliest grade 8 result; make-ups ignored; the invalidated score kept | same call under each (asserted) | the rules ("latest ... result"); the vendors' status codes |
| SF4 | Level 1 | a grade 8 score below 2415 | the vendor's performance level column | same call and figures: the column agrees with the cut on every grade 8 row (asserted) | the rules and the grade 8 summary |
| SF5 | a retiring-test result counted at the level it places at on the Measure's scale | the level of the new-scale score the bridge's distributions link it to (241 and below at Level 1 under all 30 conventions) | the level of its regression prediction (231 and below) | a different call (the stump) | the bridge study's own scores: placed by the regression 11.1 per cent of its students sit at Level 1 against 15.7 per cent on the new test; placed by the concordance 14.6 per cent, the nearest the form's attainable scores allow (asserted) |
| SF6 | the concordance's convention | equipercentile with mid-percentile ranks | at-or-below ranks, log-linear presmoothing of degree 4 or 6, a quantile match, nearest ranks, linear linking, rounded or unrounded equivalents, cut scores carried to the retiring scale and rounded | same call and figures: every convention places 241 highest at Level 1, with 1.8 new-scale points and 41 bridge students to spare, and so it stays with any 2 per cent of the bridge rows or any one school left out (asserted) | C1, convergence |
| SF7 | the merged district | Ashgrove-Fenley Consolidated (1700) as one applicant, its students tested under 1701 and 1702 | the predecessor codes counted apart | same call (asserted) | the directory's note on the consolidation; the rules' applicant list |
| SF8 | a nonpublic school's test taker now in a public high school | counted with that result (a state reading result) | left out | same call (asserted) | the rules ("latest grade 8 state reading result") |
| SF9 | a grade 9 student retained after grade 8 in 2025 | placed through the concordance like grade 10 | left out | same call (asserted) | the rules count grade 9 and grade 10 alike |
| SF10 | the six with the most | the six highest counts; no tie at the sixth place | n/a | same call | asserted: 15 between the sixth and the seventh |
| SF11 | applicants | the fourteen districts in the rules' list of notices of intent | every district | same call: no other district would rank in the top six (asserted) | the rules' attachment |
| SF12 | each applicant's grade 7 students (the ask) | students tested in the applicant's own middle schools in spring 2026 (the directory's schools; the merged district's two predecessors') | rows under the vendor's district code, nonpublic schools' students included | different figures (the ask's device) | the nonpublic schools registry |
| SF13 | grade 7 Level 1 (the ask) | a grade 7 score below 2390 | the vendor's June performance level (below 2383) | different figures (the ask's device) | the Board's resolution of 13 August 2026 |
| SF14 | with a score (the ask) | a scored session or a make-up score; absent, exempt and invalidated sessions without a make-up left out | none open | same figures | the ask's wording |

## Ladder

| Rung | Construction | Retiring scores at Level 1 | Funded (sixth; first left out) | Elmorrow, Harlenbrook, Garnet Hills, Dunstree |
|---|---|---|---|---|
| R0 | the bridge regression's prediction (the default path) | 231 and below | Harlenbrook in Elmorrow's place (Harlenbrook 323; Elmorrow 315) | 315, 323, 327, 277 |
| R0b | a logistic or per-score majority classifier from the bridge | 231 and below | the same | 315, 323, 327, 277 |
| R1 | the two cohorts' statewide percentiles or z-scores | 231 and below | the same | 315, 323, 327, 277 |
| R1b | the retiring test's own levels | 220 and below | Harlenbrook and Garnet Hills ahead of Elmorrow (Garnet Hills 288; Elmorrow 252) | 252, 299, 288, 237 |
| R2 | inverse regression | 249 and below | the golden six, every count high (Garnet Hills 413; Harlenbrook 382) | 431, 382, 413, 371 |
| R2b | the two scales' ranges matched | 265 and below | the golden six, every count far off (Garnet Hills 535; Dunstree 455) | 610, 444, 535, 455 |
| R3 | a concordance from the bridge (golden) | 241 and below | Elmorrow (368; Harlenbrook 353) | 368, 353, 372, 320 |

- **Margins:** the golden's sixth (Elmorrow 368) is 15 above the first left out (Harlenbrook 353); the fifth (Garnet
  Hills 372) is 19 above it. Under R0 Harlenbrook leads Elmorrow by 8; under R1b by 47.
- **Position and dominance:** R0 moves every applicant's count (Kessick 1,113 to 971) and drops Elmorrow from sixth to
  seventh: a large, strong-reading district with most of its Level 1 students in grade 10 loses 53 of them to the
  regression's pull toward the mean, Harlenbrook (a small, weaker district whose Level 1 students are mostly in grade 9)
  loses 30.
- **Grid:** two choices, the placement (prediction, cohort match, the retiring test's levels, a concordance, the
  inverse line, the range match) and the Layer 1 handling (each item in the inventory either way): every prediction and
  cohort cell funds Harlenbrook, the retiring test's levels fund Harlenbrook and Garnet Hills, every concordance cell
  files the golden, and every Layer 1 handling keeps each cell's slate (asserted).
- **Worth:** the decisive rung moves all fourteen counts and the slate; R2 and R2b land the slate with every count
  wrong.
- **Truth:** the 2025 cohort's expected Level 1 count on the new test, from each student's reading ability, funds the
  golden six with 29.4 between the sixth and the seventh, and the regression route's slate differs from it (asserted).

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | grade 9 and 10 students on the fourteen applicants' rolls on 1 October 2026 with a grade 8 state reading result | the rules, sections 3 and 4; SF1, SF2, SF11 |
| 2 | Unit of account | the student | the rules |
| 3 | Attribution window | each student's latest grade 8 administration, spring 2025 or spring 2026 | SF3 |
| 4 | As-of dating | the count day, 1 October 2026; the enrolment extract of 2 November 2026 | SF1 |
| 5 | Version basis | one release of each vendor's file; the make-up session's score after an invalidation | SF3 |
| 6 | Denominator | none: counts | n/a |
| 7 | Weighting | none: each student once | n/a |
| 8 | Window length | one count day | the rules |
| 9 | Boundary inclusivity | below 2415 at Level 1; a retiring score placed at or below 241 | SF4, SF6; no applicant within 15 of changing the slate |
| 10 | Rounding path | whole students, no rounding before the ranking; shares to one decimal in the ask | the prompt |
| 11 | Tie-break | none needed | SF10 |
| 12 | Maturity and censoring | the spring tests and the count day are closed | n/a |
| 13 | Order of operations | conform, key, take the latest result, place, count, rank | C1: order-free counts |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | one count-day spell per student; an invalidated session and its make-up give one result | SF1, SF3 |
| 16 | Identity normalisation | state identifiers as ten-digit text; retiring-test numbers through the crosswalk | every retiring-test row joins through the crosswalk (asserted) |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | two score scales, 150 to 450 and 2100 to 2900 | SF5, SF6 |
| 19 | Code and status semantics | the vendors' status codes and sessions | SF3 |
| 20 | Integerisation | whole students | n/a |
| 21 | Clause scope | grades 9 and 10 alike; the grade 8 cut for every grade 8 result | the rules; SF9 |
| 22 | Forward window contents | the 2027 grants on the students on the roll on 1 October 2026 | the rules, section 3 |

## Literal reader

Executed word for word, the rules count, for each of the fourteen applicants, the students in grade 9 or 10 on its roll
on 1 October 2026 whose latest grade 8 state reading result is at the Measure's Level 1 (a grade 8 score below 2415), a
Grade-Level Reading Assessment result counted at the level it places at on the Measure's scale, and fund the six with
the most. The text leaves open how a retiring-test score is placed on the new scale; the bridge study is the folder's
only link. A regression of the new score on the old satisfies every filed sentence and funds Harlenbrook; the bridge's
own scores reject it (placed by the regression 11.1 per cent of its students sit at Level 1 against 15.7 per cent on the
new test). Every concordance that matches the two distributions in the bridge (equipercentile with mid-percentile or
at-or-below ranks, presmoothed or not, a quantile match, linear linking, rounded or unrounded equivalents, cut scores
carried either way) places 241 and below at Level 1 and files the golden, every applicant's count identical.

## Oracles

None ties only under the golden. The bridge memo's means, standard deviations and correlation describe the sample under
every method; the Measure's grade 8 summary reports the statewide grade 8 results every route reads alike; the retiring
test's guide publishes its own levels and its raw-to-scale tables. No file reports a converted score or a district's
count. The expenditure and graduation files are distractors that confirm nothing.

## Ask sheet

- **Ask A, each applicant's grade 7 students at Level 1 on the Measure in spring 2026 and their share of its grade 7
  students with a score (28 figures: 14 in whole students, 14 in per cent to one decimal).** H18 home: the students who
  reach grade 9 in fall 2027, inside the 2027 grant year, a measure every applicant carries that the call does not turn
  on. Path: the new test's results file (its grade 7 rows: district code, school code, session, status, scale score,
  performance level), the 2026 directory's schools, the nonpublic schools registry, the Board's resolution of 13 August
  2026 and the dictionary (five files, nine columns). Primary device: D2, an attribute at the wrong vintage: the
  vendor's June file reports grades 3 to 7 on the panel's recommended cut scores; the Board set grade 7's Level 2 at
  2390 in August, seven points above the June cut, so every applicant's grade 7 scores from 2383 to 2389 read Level 2 in
  the file and are Level 1. Second device: D5, out-of-scope rows known only by structure: nonpublic schools' students
  sit the test under the code of the district the school stands in; every applicant has a nonpublic grade 7 test taker
  at Level 1 (asserted). Texture: the merged district's predecessor codes; make-up sessions after invalidations. Stops
  (asserted): the file's district code with its June levels (the cracker), every applicant low on both figures (Kessick
  461 and 16.6 against 532 and 19.8); the directory's schools with the June levels, every count 10 to 74 low; the file's
  district code with the adopted cut, every count 1 to 7 high and every share 0.1 to 0.5 points off; the golden 69 to
  532 students and 7.1 to 23.5 per cent. Realism: a vendor's June file carries the levels known in June, and nonpublic
  schools test under their host district's code.
- **The construction layer:** every applicant's grade 9 and 10 students at Level 1, the six funded, the first left out
  and its gap, the chart and the conformed file; the cracker has them.
- **Main population zero-counts (asserted):** none of the spring 2026 grade 7 test takers is in grade 9 or 10 on the
  count day; the ask reads no enrolment, bridge or retiring-test row; the main call reads no grade 6 or 7 row, no Board
  resolution and no registry row.
- **Hazard table (asserted):** the June levels move all fourteen counts and shares; the nonpublic rows move all fourteen
  counts and shares read by district code.
- **Referee:** none; no total in the ask's files ties only under one handling.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, each applicant's grade 7 students at Level 1 in spring 2026 and their share | counts scored grade 7 rows at the file's performance level 1 under the file's district code, the merged codes joined; the June cut and the nonpublic rows both kept | miss |

- Mirror leakage: about 7 per cent of ask weight (a response on R0 keeps the two files and misses every Ask A figure on
  the same devices as the cracker).
- Pair ceiling: 32.2 (planning weights 38 / 7 / 55 with the call, the six funded, every applicant's count, the first
  left out and its gap, the chart and the conformed file in the main block and r = 5; the ask weight over 30 criteria:
  Ask A 28, the two files 2; the cracker keeps the files, 38 + 7 + 3.7 = 48.7; the mirror keeps r, instruction-following
  and the files, 5 + 7 + 3.7 = 15.7; average 32.2), rerun from the generated rubric at ship.

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Effect (asserted) |
|---|---|---|---|---|
| Booklets scanned without a pre-ID label carry only the vendor's test-taker number | the retiring test's scanning | retiring-test results, crosswalk | rows without a state identifier dropped | call unchanged |
| Absent, exempt and invalidated sessions; make-ups after an invalidation | both vendors' scoring | both results files | make-ups ignored; the invalidated score kept | call unchanged |
| Students tested in one district and enrolled in another | the enrolment system and the test registrations | results, enrolment | counted by the testing district | call unchanged |
| The merged district's students tested under its predecessors' codes | the consolidation of 1 July 2026 | both results files, directory | the predecessor codes unmapped | call unchanged (counted by enrolment) |
| Transfers in August and September, late entrants, withdrawals in September and in October | the enrolment system's spells, with exit reasons | enrolment | every spell kept; only open spells kept | call unchanged |
| Arrivals with no state test record | the enrolment system | enrolment | none likely (no result to count) | call unchanged |
| Nonpublic test takers now in public high schools | the vendors' nonpublic testing | both results files | their results left out | call unchanged |
| Grade 9 students retained after grade 8 in 2025, and students tested in grade 8 twice | the schools' promotion decisions | both results files, enrolment | the earliest grade 8 result taken | call unchanged |
| Grades 6, 7, 11 and 12 rows | the vendors' and the enrolment system's full files | both results files, enrolment | none likely (filtered by grade) | call unchanged |

## Pre-ship check

- **Three rules, re-read against the built pack.** Domain: the deciding quantity is each applicant's count of grade 9
  and 10 students at the new test's Level 1 when its grade 10 students carry only retiring-test scores, built the way
  psychometricians place one test on another's scale (a concordance matching the two score distributions in the
  single-group bridge study); the regression of new on old funds Harlenbrook (323 against Elmorrow's 315), the
  retiring test's own levels Harlenbrook and Garnet Hills, the two cohorts' statewide percentiles or z-scores
  Harlenbrook, and every concordance convention the golden. Two layers: the Layer 1 inventory above, each item
  asserted neutral on the call (SF1, SF2, SF3, SF7, SF8, SF9 and the identifier check); the ask's two devices confined
  to the spring 2026 grade 7 rows (the separation checks); Layer 2 the linking method. The decisive step is none of
  the three banned kinds, each executed in `checks.py`: not a plant (R3c: no document names a concordance, equating,
  linking, a regression, a prediction, percentiles or an equivalent; no repeated record in any file); not data
  semantics (SF1 to SF11: every field read right still leaves the regression route on Harlenbrook); not rule
  application (R3a: every filed rule executed with the regression placement funds Harlenbrook; R3b: only the
  concordance funds the golden, every count equal to the pack's).
- **Gates.** 16 files in 3 formats (csv, pdf, xlsx); enrollment_october_2026_grades_9_12.csv at 91,075 rows; two
  distractors (district spending and graduation rates) the solution never reads; 61 generator checks; `verify.py` from
  the bundle alone (its own equipercentile and linear linking, the applicants and cut scores read from the PDFs); two
  builds byte-identical; `figures_check.py` (79 figures), `precut.py` (49) and `voice-check.py` exit 0; `leak.py`
  REVIEW (no LEAK); guard heart WARN (answered in the draw); the containers clean (H1 audit). The surface screen
  promotes five card-level pairs for the author's read, none on the pack's surface: task465 and task450 (the
  population gap; task450 the same pairing, retired), task136 and task131 (surface similarity only) and task184 (the
  same gap, pattern and decision family, differentiated on the card). The folder index and the dictionary's columns
  were renamed after the screen matched them to task465's.

## Leak check

`leak.py --asof 2026-11-20`: REVIEW, no LEAK (a first run's LEAK on the crosswalk's file name, which held the author
word "test_", fixed by naming it calderwood_examinee_id_crosswalk_2025.csv). Each REVIEW line answered:
- Eight three-digit golden figures (168, 225, 231, 241, 262, 264, 280, 320) sit in the retiring test's raw-to-scale
  table, scale scores of the forms: harmless (the reader read each as a table cell; 241 is also the boundary, a
  coincidence of the table the concordance lands on, and the table states no cut).
- The grant rules carry every district name of the call and name fourteen candidates beside numbers: Attachment A lists
  the applicants with their codes and notice dates, no count and no ranking. Harmless.
- The rules, the guide, the bridge memo and the grade 8 summary carry three to six generic stump terms (scores,
  levels, bridge, retiring, schools, window): each describes its own subject; none names a placement method. Harmless.
- The directory and the graduation rates file name the candidates beside numbers: codes, counties and a different
  measure, no ranking on the question. Harmless.

Reader, round 1 (answers and rulings in `leak_check_report.md`): nothing quoted for question 1 (the rules' "counts at
the level it places at on the Measure's scale" says a conversion is needed, not how); no ranking file; its literal
reading put the cut at the linear equivalent of 2415 (241 and below) and reproduced the golden exactly (the six, 368
and 353, the gap of 15), listing the regression (231), the inverse line (249), the retiring test's levels (220) and
per-order subsets as the open choices; question 6 an analytical choice (the conversion of about 21,500 grade 10
results through the bridge study). Its realism tells were fixed in the generator, nothing graded moving: school names
drawn from varied invented names instead of a rotating list of directions; the rules' attachment on its own page; the
registry holding non-participating schools too; the 2025 spending and graduation files under the predecessor codes
1701 and 1702 (the consolidation came in July 2026), two graduating classes, whole-dollar spending; the two tests'
stated reliabilities 0.87 and 0.88, no longer equal to the bridge correlation; October withdrawals and moves in the
enrolment extract with varied exit reasons (asserted neutral, SF1); each file dated by its own as-of date; each
issuer's documents in its own layout. The district codes in tens stay (codes assigned in blocks).

Judge, pass 1 on architecture 2 (`determinism_check_report_pass2.md`): DETERMINISTIC, APPROVE. Every figure reproduced
(the fourteen counts, the conformed file's levels, the fourteen grade 7 counts and shares, the bridge shares); every
linking convention it tried placed 241 and below; the regression (231) and the statewide cohort match refuted by the
bridge file. Gate G method_or_model_selection, analytical_non_defect, no surface-read dependency, no sole data defect;
Gate H domain pass, layers pass, decisive step analytical; no mismatch with this note or the card. Three minor notes,
none on the call: the conformed file's Level 2 to 4 placements follow the same concordance (asserted at 2508 and 2579,
SF6); whether nonpublic schools' grade 7 students are an applicant's (the golden leaves them out, SF12, the ask's
device); the distractors bear on no graded quantity (as distractors must).

Reader, round 2 (after the realism fixes): nothing quoted for question 1; no ranking file; its literal execution put
the linear and the equipercentile equivalents of 2415 between 241 and 249, placed 241 and below and reproduced the
golden exactly (the six, 368 and 353, the gap of 15), naming the regression (231) and the retiring test's Below Basic
(220) as the easy routes, both funding Harlenbrook in Elmorrow's place; question 6 an analytical choice, no planted
defect and no executed rule. Its determinism caveat (the method is not filed) is the design: every linking
convention places 241 and below (SF5, SF6; the judge found the same) and the regression is a prediction, not a
placement. Its open question on a student with both results is the rules' "latest" (SF3). Its realism tells were
fixed in the generator, nothing graded moving (figures.json, submission.md and both goldens byte-identical): every
enrolment date on a school day (the largest district first day had fallen on a Saturday; no Labor Day dates), October
moves re-entering one to seven days after their exit instead of exactly two, every test session on one of its
window's school days (no Monday pile-up from weekends rolled forward, no Memorial Day make-up), the bridge's
retiring-test sessions two school days before or three after the new test. Left as they are: the folder's as-of date
of November 20 (assembled after the October count for the December 10 meeting), first days clustered on a few dates
(district calendars), the index's record counts (its own column), the equal grants (the rules set them). A data-only
repair: `leak.py` re-run (REVIEW, the same lines), no third reader.

## Tried and rejected

- Weather normalization alone, with oil fills and estimated reads as the interval structure: in a prototype of 150
  buildings, a degree-day regression on calendar-month bills with oil deliveries summed by month landed within 2 per
  cent of the fill-to-fill fit for most oil buildings (6 at most) and on the golden's slate, so a strong analyst's
  regression lands the call; the estimated reads and fills are Layer 1 (cleaning them makes the call easy) and stay
  there. The decisive structure is each building's change in how it runs.
- A first keying of the card on the time gap with pattern A and Gate G forecasting: the signature is spent in seven
  older builds; keyed on the population gap with G4 first, which also reads truer (the bills before a change are not
  the decided building).
- The 2025 benchmarking year scaled by degree days as the default path: the cycle rules name the bills, statements and
  tickets as the records, so a competent analyst fits them; the filings route stays below rung 0 and the default path
  is the whole-record fit.
- Ask B on the gap between the filings and the bills for 2025: its golden sat near zero for most types; Ask B now
  carries the filings' own emissions and site energy by type on the export's lot rows.
- A six-day sensor outage in April 2024 in the weather record: leaving missing days out of the degree days moved 808
  Thornwick Avenue and 686 Fenwright Avenue across their $5,000 bins; the outage now sits in April 2019, outside the
  billing years.
- Partial oil deliveries at random on every building: taking them as fills hid one building's boiler change from the
  search and put it in the slate; partials now fall in the 2022 to 2023 season, on no building near the cut, and every
  building away from the cut is held under $55,000 on a whole-record fit.
- The law's billing sentence ("bills it to the property's tax lot and posts any deduction ... against the same
  notice"): an ask organ in a document the call reads, and wrong against the ledger (a reassessment opens a new
  notice); cut.
- Round floor areas on the twenty buildings placed around the cut (each a multiple of 1,000, against none of the other
  138): a giveaway; each now carries an ordinary area and the calibration re-aims.
- Keeping estimated reads and partial deliveries off the buildings around the cut, to hold those items neutral: a second
  giveaway. Every building now carries the same processes: the utility's estimates land within a few per cent, as a
  weather-adjusted routine does (estimates missing by 20 to 40 per cent, read as actual, hid two slate properties'
  changes from the search), none after the advanced meters of October 2025 or the steam company's January 2025 system,
  and partial deliveries stop a few hundred gallons short, in the 2022 to 2023 season only.
- A window started one span after the found break as a variant the golden must hold under: no reader would choose it
  (the first span after a change is wholly post-change), and 62 Merrow Street moves 2 per cent under it; the variant
  asserted is the generator's own change dates.
- Architecture 1, the degree-day fit on each fuel's spans after its last change found in the property's own bills
  (2026-10-17): judged NOT_DETERMINISTIC, SEND_BACK (margin_or_boundary_fragility, underspecified_objective). The post-
  change window's first span and whether electricity is refit with the heating fuel are open (461 Tallman Street's
  electricity rises 1.35 times when its gas falls; refit, it is the first left out at $70,990 against 633 Lattermore
  Place's $68,577), a step search run as written flags dozens of series and moves four $5,000 amounts, and a $7,000
  12th-to-13th margin sits inside a $40,000 to $57,000 window freedom. Filing the window or a dated change log would make
  the step rule application; an undated change cannot be pinned without it. The architecture is spent and re-rooted.
- A first redraw (architecture 2 on paper, 2026-10-17): each district's claim under a state challenge judged by the
  upper end of its inventory's 95 per cent interval, the decisive move carrying each shared emission factor's error on
  the district's fuel total instead of building by building. The correlated-error lesson is already task228's,
  task229 v1's, task260's and task261's (an error shared by the units does not average away); dropped before
  registration.
- The retiring test on a continuous scale (every integer a possible score): the concordance conventions disagreed at
  the Level 1 boundary unless the bridge's share sat within a student of a cumulative step (an exact count match tied
  the at-or-below conventions, a gap of one to three students split the quantile cut's "below" and "at or below"); the
  retiring test is now a 30-item paper form whose raw-to-scale table leaves six to eleven points between scale scores
  near the cut, and all 30 conventions agree with 41 bridge students to spare.
- A bracket of the slate, the overcounting routes (inverse regression, the range match) also wrong: it needed grade 9
  cohorts two to three times the grade 10 ones in two districts; those routes land the golden six with every count
  wrong, and the ladder rests on the prediction and cohort routes.
- Equal cohorts statewide: matching the two cohorts' statewide percentiles or z-scores landed the golden; the 2025 grade
  8 cohort now reads 0.20 standard deviations below the 2026 one, which the bridge sample's retiring-test mean shows,
  and every cohort match places 231.
- Bridge draw 0: 53 per cent of its students with a retiring score of 241 sat at Level 1, so a per-score majority rule
  placed 241 at Level 1 and filed the golden; the bridge's schools are drawn again (draw 11: 43.5 per cent, all 30
  conventions still agreeing at every cut).
- A school realignment between two districts as an ask hazard, the vendor's file keeping the old district: the date of
  the move could not be read from the folder without a filed sentence, a fork; dropped.
- Asks on the students the count leaves out (no grade 8 result) or on the movers: the complement or a split of the main
  population, so a device on them moves the call's rows; dropped.
