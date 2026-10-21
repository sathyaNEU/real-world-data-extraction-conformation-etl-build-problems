# task479 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 4, drawn 2026-10-21 after architectures 1
to 3 (NFIP claims replayed on elevated buildings, a lodging panel benchmarked to annual receipts, retained claims
under a fixed stop-loss deductible) were spent at stage 4; nothing of any earlier world or step is kept.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task479.json` (architecture v4, lineage v1 to v3 spent), registered
  2026-10-21 after a pull. Guard WARN only, answered here: `overuse.objective` (the lane is ETL by assignment),
  `people.first` (Sabrina, a first name on task177, drawn by `guard.py names --geo us --seed 479`). Redrawn at the
  draw: organisation from nonprofit_or_charity (task486's) to university_or_school (a charter management
  organisation runs schools), context artifact from published_series (task178's) to filed_model (the vendor's item
  bank), gap and generator from population and G14 (spent signatures) to population and G15 (responses that do not
  meet the evidence standard of an attempt). People: Sabrina Santos and Gregory Valdez.
- **Pairing:** Education & Learning Sciences, task type `item-response-theory-test-equating`, which serves ETL: the
  spring 2026 benchmark's item responses and response times conformed with the vendor's item bank and rescored onto
  the vendor's reporting scale.
- **The decision and the quantity:** the network's board designates the campuses for 2026-27 high-dosage math
  tutoring where 35 per cent or more of the students tested on the spring 2026 benchmark score below Basic. Forward
  facing: the tutoring year has not begun.
- **Data-native sentence:** in a few campuses' end-of-day sessions students answered a third or more of the items in
  under three seconds at the blind-guess rate of a quarter right, and the vendor's maximum likelihood scores read
  those guesses as wrong answers.
- **Shape:** `10`, a scorecard in one file: each of the fourteen campuses' share below Basic against the 35 per
  cent line (14), the designated set, a chart, and two asks of fourteen campuses times two figures (56).
- **Strategy:** `other` (effort moderation of rapid guesses); Gate G `etl_conformance`; gap `population`; generators
  G15, G16. Layer 2 family `estimation_fit`, pattern `own:responses given faster than any engaged reading carry no
  information and are scored as not administered`.

- **Sources, one line each:** seed ET36 (the lane and number only); the measurement literature's effort-moderated
  scoring of rapid guesses in low-stakes tests (a response faster than any engaged reading treated as not
  administered), stated in no shipped document; the client's education rigor patterns (linking, scoring), the
  vendor's maximum likelihood scoring filed as its standard's general method.
- **Same-puzzle test:** gap population, decisive generator G15, decision designation_set against the last twelve
  builds, lineage included: no match. Abstraction test: task253 (raw averages of small samples below a line) shrinks
  noise; task237 and task257 test a scale's structure; task464 links two instruments. None removes responses that carry
  no information before estimating each unit's level.
- **WHAT screen:** the memo files the population (students with a spring 2026 administration), the outcome (each
  student's achievement estimated from the spring responses on the vendor's scale and bank), the unit (the share of
  students tested below 470) and the comparison (35 per cent or more); the technical summary files the scoring model
  (maximum likelihood on the 3PL bank). The decisive step settles none of them: it decides which of a student's
  responses carry information about the achievement the memo estimates.

## Default path

A strong analyst with every field read correctly:

1. Reads the memo: a campus is designated when 35 per cent or more of its students tested on the spring 2026
   benchmark are below Basic, each student's achievement estimated from the spring responses on Quantilis's scale and
   bank.
2. Takes the vendor's spring score report, which is that estimate: each scale score is the maximum likelihood estimate
   from the student's forty scored responses on the bank (rescoring every response reproduces it for every student).
3. Counts each campus's students below 470 and applies the 35 per cent line.

**Ends on:** C01, C03, C04, C06, C07, C09, C11 and C13 designated

On that path C03, C06, C09 and C11 stand at 42.8, 42.7, 46.5 and 40.4 per cent.

**Golden:** C01, C04, C07 and C13 designated (42.4, 39.6, 41.3 and 39.1 per cent); C03, C06, C09 and C11 fall to 21.0,
19.6, 23.9 and 22.3 per cent once each student is scored on the responses given with effort.

## Stump sentence

The default path takes the vendor's reported scale scores and files C01, C03, C04, C06, C07, C09, C11 and C13 designated, because it never asks whether every response it scores was a real attempt: in the end-of-day sessions at C03, C06, C09 and C11 students answered a third or more of the items in under three seconds, right a quarter of the time at every difficulty, and those guesses, read as wrong answers, pull their scores under Basic.

## Three rules

Task type: item-response-theory-test-equating (Education & Learning Sciences): the spring 2026 benchmark's item responses and times, in two export layouts, conformed with the vendor's three-parameter logistic bank and rescored onto the vendor's reporting scale for each student, a conformation serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each campus's share of students whose achievement on the benchmark's scale is below Basic, worked the way psychometrics scores a low-stakes test with rapid guessing: a response given faster than any engaged reading of the item carries no information about the student's ability and is treated as not administered, and ability is estimated by maximum likelihood from the responses given with effort (effort-moderated scoring).

Swap: "which clinics' patients are below the blood-pressure target, from their readings" keeps a share below a line and loses the step: there is no item response model, no guessing floor and no response time that says a reading carries nothing.

Layer 1: the item response export in two layouts across the 30 March 2026 platform release (milliseconds against seconds, renamed fields), a restarted fall session's two administrations with the makeup under a temporary id, student ids reissued at the January 2026 migration with a crosswalk that misses the December transfers; each is how the producing system writes, nothing is placed to be caught, and checks.py asserts the main call holds under them (SF6, SF7).

Layer 2: estimation_fit, the information a response carries: the choice that flips the call is estimating each student from the responses given with effort instead of from all forty, which the vendor's maximum likelihood reads as forty attempts.

Decisive step: each student's maximum likelihood ability on the bank from the responses given in five seconds or more (no engaged response took under 7.5 seconds, no rapid one over 3), which brings C03, C06, C09 and C11 under the line and keeps C04 over it.

Not semantics: every field, unit and definition read correctly (milliseconds and seconds, scored 1 and 0, the bank's a, b and c, the scale and the cuts) still leaves the easy route taking the vendor's scores, because no field marks a response as a guess and the test is untimed; the step is the inference that responses at chance accuracy and a second or two carry no information, which the data shows and no sentence says.

Not rule application: the memo fixes the population, the outcome, the unit and the line, and the technical summary the scoring model; no rule says which responses a student's estimate should use, and executing every filed rule on all forty responses files the default eight.

Analyst test: a strong analyst who conforms every file and reads every rule, taking the vendor's maximum likelihood scores, files C01, C03, C04, C06, C07, C09, C11 and C13 designated (the default path's Ends on); one who drops the students with rapid responses files C01, C07 and C13, and so does one who drops the disengaged sessions; only scoring every student on the responses given with effort files the golden four; checks.py runs them on the clean truth (R3a, R3b, R3c).

Estimand: the designation memo (bellweather_tutoring_designation_2026-27.docx): the population (students with a spring 2026 benchmark administration), the outcome (each student's achievement estimated from the spring 2026 responses on Quantilis's scale and item bank, below 470), the unit (the campus's share of students tested) and the comparison (35 per cent or more); the scoring model in the technical summary, section 3.

No decoy: nothing is planted: the responses, times, bank and reports are the vendor's records and the rosters the network's, the memo states the basis without a method, and no earlier designation, staff list or published figure ranks the campuses on spring 2026.

No certified replay: no certified or published designation ships; the vendor's report is the easy route's input, not a figure the golden reproduces.

Lesson: an estimate from a response model is only as good as the responses it is fed: answers given too fast to have been read, at the chance rate, carry nothing and must be left out rather than scored wrong; no build on file removes uninformative responses before estimating each unit's level.

## Readability screen

Each rung, the sentence or file a reader would have to read to take it, and whether any shipped text hands it over.

| Rung | What takes the reader there | Verdict |
|---|---|---|
| R0 the vendor's performance levels counted | the score report's level column | readable |
| Layer 1: two layouts, temporary ids, reissued ids | the dictionary and the technical summary's section 5 | readable |
| R1 (default path) the vendor's scale scores, the MLE from all forty responses | the memo and the score report | readable |
| R2 the students or sessions with rapid responses dropped | the response times read as a validity screen | readable |
| R3 (decisive) every student scored on the responses given with effort | nothing: no sentence names rapid guessing or effort moderation, no column flags a response, the summary says only that the test is untimed and that the client records seconds on each item | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the scoring model | MLE on the 3PL bank, scale 500 + 40 theta, 350 to 650 | another estimator | not filed alternatives | technical summary sections 2 and 3 |
| SF2 | the test's timing | untimed | timed | same call | technical summary section 1 |
| SF3 | the rapid threshold | five seconds | any value from 3 to 7.4 | same call (asserted at 3 and 6) | the gap in the times (E1) |
| SF4 | students tested | every student with a spring administration | engaged students only | C01, C07, C13 | the memo: "A student tested is a student with a spring 2026 benchmark administration" |
| SF5 | a restarted fall session | the later administration | the first | the asks' figures only | technical summary section 5 |
| SF6 | the two export layouts | one student in one layout | both | same call (no overlap, asserted) | the export dates |
| SF7 | forty responses | every student answered forty | partial | same call (asserted) | the export |

## Ladder

Built values from the cut pack (generator/checks.py L1 to L4, C2, C3, E1, E2), share below Basic, per cent.

| Rung | Route | Designated | C03, C04, C06, C09, C11 |
|---|---|---|---|
| R1 (default path) | the vendor's scores | C01, C03, C04, C06, C07, C09, C11, C13 | 42.8, 52.5, 42.7, 46.5, 40.4 |
| R2a | students with rapid responses dropped | C01, C07, C13 | 16.2, 23.4, 17.9, 16.7, 17.6 |
| R2b | sessions with rapid responses dropped | C01, C07, C13 | 22.0, 15.3, 21.3, 20.1, 22.0 |
| Golden | every student on the responses given with effort | C01, C04, C07, C13 | 21.0, 39.6, 19.6, 23.9, 22.3 |

- Dominance: every campus sits at least 3 points off the line on the golden (C2), and each of the four the vendor's
  scores add stands at least 3 points over it there (C3). C04's rapid guessers are its weaker students in grades 7
  and 8, so dropping them or their sessions takes it off the list, while scoring them keeps it on.
- The data separates the readings: rapid responses are right 22 to 28 per cent of the time on easy and hard items
  alike (E2) and sit under 3 seconds while engaged ones sit over 7.4 (E1), so the threshold is forced by the gap.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | students with a spring 2026 administration | filed (memo; SF4) |
| 2 | Unit of account | the campus's share of students tested below 470 | filed (memo) |
| 3 | Attribution window | the spring 2026 window | filed |
| 4 | As-of dating | the exports of March and April 2026 | manifest |
| 5 | Version basis | one administration per student in spring | SF7 |
| 6 | Denominator | students tested | filed (SF4) |
| 7 | Weighting | none | C1 |
| 8 | Window length | one administration | filed |
| 9 | Boundary inclusivity | below 470; 35 per cent or more | filed (manual 4; memo) |
| 10 | Rounding path | scale scores to the whole point, shares unrounded against the line | manual 2; prompt |
| 11 | Tie-break | none (no campus within 3 points) | C2 |
| 12 | Maturity and censoring | none | C1 |
| 13 | Order of operations | conform, screen the times, score, count | commutes |
| 14 | Row order | item sequence | C1 |
| 15 | Duplicate resolution | none in spring | SF6 |
| 16 | Identity normalisation | student ids within spring | SF6 |
| 17 | Netting against gross | none | C1 |
| 18 | Dimensional units | milliseconds against seconds | the dictionary |
| 19 | Code and status semantics | scored 1 and 0 | the dictionary; never the stump |
| 20 | Integerisation | scale scores rounded | manual 2 |
| 21 | Clause scope | the line applies to every campus | filed |
| 22 | Forward window contents | the 2026-27 tutoring year | filed |

## Literal reader

The memo executed word for word asks for each student's achievement estimated from the spring responses on the bank,
and the technical summary fixes the estimator; the literal question is what the responses say about each student's
achievement, which the responses given in a second or two at chance accuracy do not speak to. A literal reader who
takes the vendor's report has assumed every response is an attempt, which the times and the chance accuracy
contradict; every other reading converges or violates a quoted sentence (fork table). Re-run on the finished pack.

## Oracles

- The vendor's score report reproduces the MLE on all forty responses for every student (L4); it is the easy route's
  input and arbitrates nothing.
- The state results and chronic absence are distractors (metadata.json); neither ranks the campuses on spring 2026.
- No control ties only under the golden on the asks.

## Ask sheet

- **Ask A, each campus's students tested on the fall 2025 benchmark and the share at or above Proficient (fourteen
  campuses, two figures each, whole students and one decimal).** H18 home: the baseline the Board reads beside the
  designation (memo, "With the designation"). Path: the fall score report (student id or temporary id, campus, date,
  score), the temporary id register (name, birth date), the fall roster, the technical summary's section 5. Primary
  device: D1, the same records under two key schemes: 7 per cent of students had their fall session restarted, the
  first administration under their own id and the makeup under a temporary id; only the register's name and birth
  date against the roster tie them. Hazards: the later administration is the score (SF5).
- **Ask B, by winter campus, the students tested in both fall and winter and their mean fall-to-winter growth
  (fourteen campuses, two figures each, whole students and one decimal).** H18 home: the network's mid-year growth, the
  second figure the memo brings. Path: the fall report, the winter report (new ids), the crosswalk, both rosters, the
  register. Primary device: D7, the true key elsewhere: the January 2026 crosswalk misses the students who changed
  campus in December, so only their names and birth dates across the two rosters link them; the restarted students'
  fall score is their makeup's. Hazards: the fall campus against the winter campus.
- **The construction layer:** the call, the fourteen shares and the chart; the cracker has them.
- **Main population zero-counts (asserted):** the call reads the spring responses, the bank and the spring report;
  every ask device sits in the fall and winter reports, the register, the rosters and the crosswalk (X1).
- **Hazard table (asserted):** A1, A2, B1, B2 in checks.py; none moves the call.
- **Referee:** none.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, fall students tested and share at or above Proficient | a row per student id, no repeated id to resolve; keeps 0 of 28 | miss |
| B, fall and winter students and their growth | the crosswalk's join; keeps 0 of 28 | miss |

- Mirror leakage: 0.0 per cent of ask weight on the cut pack (0 of 56).
- Pair ceiling: 30.0 on the cut pack (weights 38 / 7 / 55: the cracker keeps the call and instructions, 45.0; the
  mirror at the default path misses the set and keeps 4 of 14 shares, 15.0). Re-measured by the stage 4 readers.
- Measured by: generator/ceiling.py on the cut pack.

## Pre-ship check

READERS_LINE

JUDGE_LINE

## Tried and rejected

- The seed's own mechanisms as the decisive step (2026-10-20, screened at the draw): earning premium by term rather
  than by policy effective year is a stated accounting rule (rule application), and a condominium master policy's unit
  count read as units is a field reading (data semantics); both stay in the pack as Layer 1 under filed sentences.
- A catastrophe-adjusted expected loss ratio by county (2026-10-20, screened): the estimator family for an expected
  catastrophe loss from a short record is open (window mean, frequency from a long declarations record times the
  window's severity, a fitted severity tail), so the graded figure forks, and filing the method makes it rule
  application.
- Event-clustered confidence bounds on each county's loss ratio (2026-10-20, screened): a variance-only correction that
  widens every interval, so the conservative reflex lands the hold; and the annual series shows the spread directly.
- The Risk Rating 2.0 glide path's full-risk premium for policies still capped (2026-10-20, screened): every policy
  transitioned within one year, so the full-risk premium is censored at the same multiple for all of them and the
  distribution beyond it is not identified; the cap itself is a statutory rule.
- The latest event's claims completed by days since landfall, and open claims from their adjusters' damage estimates
  (2026-10-20, screened): the first is task181's route-specific delay and task451's arrival history, the second is a
  policy-terms computation (rule application).
- Claims linked to policies by quasi-identifiers to rate premium bands (2026-10-20, screened): linkage error correction
  is spent (task449, task468) and a fusion through shared attributes is task465's.
- Policy tenure from originalNBDate with left truncation (2026-10-20, screened): task133's delayed entry.
- Rating each insured building at the claim rate of buildings in its present condition (2026-10-20, screened): the
  policy terms carry an elevated-building indicator for every term, so the rate by present state is one group-by on a
  visible column, the opponent's stratification reflex; kept as a wrong rung (it gives a raised building the later rate
  of elevated buildings in general, which on the river is the low rate of buildings never in a 2016-sized flood).
- Bridge deck deterioration from inspection pairs of different lengths (2026-10-20, screened in another world): per-year
  normalisation, the obvious correction, lands within rounding of the interval-aware estimate on fair decks, so the
  lever is too small.
- Every insured building as the population (2026-10-20, stage 2): the buildings below the base flood level carry the
  counties' whole flood history, so the lowest rates fell to the upland counties with or without the replay, and the
  replay moved no county across the fifth place; the population narrowed to the elevated insured buildings the pilot's
  insurers will quote, where the raised buildings are a third of some counties' book.
- The re-entered transfer claims carrying only NFIP Direct's own payments (2026-10-20, stage 2): summing every
  record's payment then lands each county's payments, so the payment half of ask A carried no device; the re-entry
  carries the claim's payments to date, as NFIP Direct's record of a transferred claim does.
- The Saltreach surge of 2005 a foot under the base flood level and Kettlemoor's 2016 middle reach 0.6 feet under it
  (2026-10-20, stage 2): the protection-to-the-base-flood-level rung (R3) and the class-rate rung (R2b) each filed the
  golden five; with the 2005 surge 0.6 feet under the level in Saltreach (still two feet and more under the raised
  floors) and Kettlemoor's middle reach a foot under it, both rungs file a wrong five.
- A persona pair whose first name the names script does not return (2026-10-20, stage 2): replaced with Samantha
  Walter from `guard.py names --geo us --seed 479`.
- Contents-only and unit owners' records joined to the building rate (2026-10-20, stage 2): neither moves the call,
  so they stay Layer 1 under 2.1 and 2.3 rather than a device.
- Architecture 1, NFIP claims replayed on the elevated buildings as they stand (2026-10-21, spent at stage 4): reader 1
  quoted guidelines 3.1 ("would bring ... as they stand") as the decisive text, replayed each claim's water on the
  present floor and landed the call, every rate and 30 of 72 figures; reader 2 missed on the claims since elevation
  but took ask B's counts from the final inspections; the judge NOT_DETERMINISTIC FIX_NOW on ask B's share, completion
  and county keys and called the estimand's wording an announcement. The estimand that files a counterfactual names
  it; re-rooted to architecture 2 in a fresh world.
- Architecture 2, the lodging Monitor benchmarked to the Department's annual receipts (2026-10-21, spent at stage 4):
  both scored readers computed each county's Department-to-Monitor ratio for every published year as their first
  calibration, saw the straight-line drift and carried it a year, landing the call, every growth figure and most ask
  figures (exit 1, 50 and 54 of 80); both also used the register's county for the transferred properties and linked
  the crosswalk gaps. A drift that the first diagnostic of a benchmarked series prints is no stump; re-rooted to
  architecture 3 in a fresh world.
- Architecture 3, self-funded groups' 2027 retained claims under a fixed specific deductible (2026-10-21, spent at
  stage 4): reader 2 re-applied the $250,000 deductible to each large claimant's trended claims and landed the call
  (exit 1, 22 of 80); reader 1 trended the retained total and missed (exit 0, 9 of 80). Leveraging under a fixed
  deductible is textbook to a strong reader once a fixed deductible and a claimant list sit side by side; both readers
  missed both ask devices (reissued member ids, a reopened claimant file), which are worth re-skinning.
- Architecture 4, a charter network's spring benchmark rescored for rapid guessing (2026-10-21, spent at stage 4):
  both scored readers took the vendor's scores and missed the call, but the judge returned DETERMINISTIC and SEND_BACK
  on Gate G (planted_defect_flip): leaving out rapid-guessed responses is cleaning contaminated rows, the stump
  collapses on clean data, and the vendor's score report is a shipped figure that ranks the campuses wrongly. The asks
  leaked 85.7 per cent because a temporary id register and two named rosters documented both devices. A decisive
  step that removes bad responses is Layer 1, and any shipped report of the easy route's figure is a Gate G artifact.

