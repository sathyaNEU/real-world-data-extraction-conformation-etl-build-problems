# task246 design note

Architecture 1, wave 4, seed DQ19 (how many public alerts a monitoring network should have issued, and the alert
configuration that follows): the seed's world (a surveillance network whose figures feed public alerts), decision (the
configuration each site's alert figure is published on) and quantity (each site's alert figure) only. The seed's
pitfall is an averaging-period reading (data semantics), so the pitfall is re-found in the readings: every figure the
network publishes is a measurer's reading of a child, and the readings carry each survey team's tape offset and field
error as well as the child's arm, so the share below the wasting cut-off has to be read from the children's own
distribution, net of the measurers.

A fictional arid county in northern Kenya: the county government's Department of Health runs a long-rains nutrition
surveillance round each year in twelve survey zones (its sub-counties split by livelihood zone), with two partner
NGOs' survey teams measuring children aged 6 to 59 months in sampled clusters; each zone's wasting prevalence by
mid-upper arm circumference (MUAC under 125 mm, or bilateral oedema) goes into the county's monthly early warning
bulletin, where it sets the zone's public nutrition alert. Every measurer and the survey supervisor take a
standardisation test before the round and a refresher mid-round, reading the same children twice. The MUAC cut-offs
and the standardisation test are real practice; the county, its zones, the partners and every person are invented.

## Draw

Card `cards/task246.json` (architecture 1, registered 2026-10-18). Guard verdict PASS; the two NOTEs
(test.same_puzzle_older and test.same_driver_older against task266 v1) are differentiated on the card: task266 builds a
completion share from competing endings' hazards among students still enrolled, while here each child is measured once
and the share comes from splitting each reading into the child's own arm and the measurer's offset and field error.
task198's spent v2 (interviewer effects inferred from the survey data through measurers who crossed regions) is
differentiated too: here the measurers' offsets and errors are measured directly against a supervisor on the same
children. Nearest driver task198 v2 (lineage) at 0.09.

- **Pairing.** General Statistics & Data Science / missing-data-censoring-measurement-error, a task type serving
  Descriptive & Distribution Analysis and Data Quality Monitoring; drawn for Data Quality Monitoring & Alerting. Not
  banned against the last three builds (task471 survey register quality, task166 banking stress testing, task198 survey
  anomaly detection). The object is the health of each zone's MUAC readings (how far the measurers' error moves the
  zone's published wasting figure), the call a monitoring decision: which zones' figures carry the measurement note and
  go into the bulletin at their error-free value.
- **Niche.** A county surveillance round's measurement note: each zone's MUAC readings were taken by one to three
  teams, each team's anthropometrist has a tape offset (a tight or loose pull, a misread window) and a field error
  against the supervisor, both found in the standardisation test, and the note is carried where the measurers' error
  moves the zone's wasting prevalence by two points or more, either way.
- **The call.** How many of the twelve zones' 2027 long-rains wasting figures carry the measurement note, and which:
  a zone carries it when the wasting prevalence read from the normal distribution of its readings and the prevalence
  read from the normal distribution of its children's own MUAC differ by two percentage points or more.
- **Shape.** 14, cuts of a distribution per segment: per zone the readings' prevalence, the children's own prevalence
  with its accepted range and the note (12 zones), the noted set and its count, a chart of the two prevalences per zone
  against the alert bands, and the ask's three figures per zone (36), well over 25 criteria. Decision
  designation_set, answer set_of_items, question form how-many.
- **Strategy.** decomposition_attribution: each zone's readings split into the children's own arm and each team's
  offset and field error. G17 decisive (the error-free distribution needs the measurement error estimated and taken
  out, not assumed away), G16 (the error taken as the repeat readings' technical error, as the error against the
  supervisor, with or without the offsets); gap population (the readings are not the children); Gate G
  decomposition_attribution; calibration other (the standardisation test, each measurer and the supervisor reading the
  same children twice); context artifact filed_standard (the county's surveillance protocol); Layer 2 family
  estimation_fit, pattern own:measurer-offset-and-field-error-out-of-the-spread.
- **Forum, event, organisation.** operations_desk (the county's early warning bulletin desk, which publishes each
  zone's alert from the round's figures), other for the forcing event (the July bulletin's issue to the County Steering
  Group on 30 July, a monthly public release no vocabulary key fits), local_government (the county government's
  Department of Health). Role programme_officer (the county nutrition programme's nutrition information officer, who
  runs the round and signs off its figures); context artifact monitoring_export (the round's survey exports). Redrawn at
  stage 3: task199, task168 and task167 were filed before this card but reached this checkout after it, and banned
  field_unit_lead (task199), filed_standard and season_or_peak (task168); every axis now clears them (forums
  line_manager_or_team, executive_team, board_of_directors; events period_close, season_or_peak, vote_or_meeting;
  organisations university_or_school, other, foundation_or_funder; roles field_unit_lead, capacity_planner,
  compliance_or_audit). Guard WARNs answered: the pdf and xlsx pair repeats task167, and is what a nutrition unit sends
  a bulletin desk (a workbook of zone figures and a one-page note); the how-many form repeats task168, and is the
  decision's own form, a count of zones with the note and which.
- **People** (`guard.py names --locale en_KE --seed 246`; the geography's own locale, `--geo "Kenya"` falls back to
  en_US): Winny Karisa, the county's nutrition information officer, who asks; Purity Maina, the round's survey
  supervisor, who reads the standardisation children as the reference; Barasa Kahindi and Caroline Nthenya, the two
  partner NGOs' survey coordinators; Kelvin Omollo, the early warning bulletin's drought information officer. None
  appears in the prompt.
- **Data-native sentence.** Each zone's readings were taken by one to three teams and each team's anthropometrist pulls
  the tape a little tighter or looser than the supervisor and places it a little differently child to child, so a
  zone's spread and mean of readings are its children's plus its measurers', and a cut-off in the tail turns a small
  offset into several points of wasting; the standardisation test is the only place the measurers are separated from
  the children, because each team works its own clusters.
- **Sources.** The client's two-layer standard (estimation_fit: an estimate that ignores the data's measurement
  structure) and the task type's pattern 2 in layer2-rigor-patterns.md (error carried from replicate measurements,
  shortcut: treat the readings as exact); here the error is in the outcome and moves a tail share, and the replicate
  organ has two parts, repeat readings and readings against a supervisor. The seed DQ19 gave the world, the decision
  and the quantity only. Anthropometric survey practice gave the reflexes the ladder is built against: the
  standardisation test's technical error of measurement as the measurer's error, and the readings' own share as the
  prevalence.
- **Mechanisms on file** (`guard.py mechanisms --objective data-quality-monitoring`, 17 builds), the insight each
  spends: 229 a convex conversion of a daily mean; 231 exits reaching the record late; 232 a transmission rate from
  delayed closed episodes; 230 a late channel moving items to default categories; 228 events clustered within
  randomised units; 233 a gold-standard follow-up carried across base rates; 234 a share in a source's output that
  transit loss cannot move; 235 an item lost only once its device had its next chance; 236 a capture change changing
  which cases are reached; 237 the share of a composite's variance due to its attribute; 238 a channel effect through a
  randomised nudge; 239 a group-level factor; 240 the error of a post-stratified total; 241 a sensor's error against a
  reference at a displaced position; 242 a detector whose sensitivity fades with time since the event; 243 a growth
  balance carrying movement; 245 losses falling on the outcome's own high values. None spends a reading's offset and
  field error, measured on reference children, taken out of a tail share.

The call is retrospective by design: the round's fieldwork closed on 8 July and the note is a monitoring decision on
its figures before they are published; what faces forward is the use (each zone's published figure sets its alert band
in the bulletin of 30 July and holds until the next round).

## Default path

1. Read NCHA's export (MUAC in mm, the child's age in completed months from `dob` to `today`, team 2's rows of 22 June
   sent again under new `_uuid`s taken once, each child once on cluster, household and line) and PRK's workbook (MUAC
   in cm times ten, `Age (months)`); keep the children aged 6 to 59 months with MUAC from 75 to 220 mm or oedema
   (section 6); each cluster's zone from the sample; the anthropometrist on duty from the teams workbook (PRK team 4's
   anthropometrist changed from the cluster of 28 June).
2. Each zone's readings' figure (section 6): oedema counted, the rest's share below 125 mm read from the normal with
   the readings' mean and standard deviation: NP 10.7, NA 5.9, NL 17.8, CP 7.0, CA 5.2, LT 12.1, EP 14.5, ER 6.3, EA
   7.4, WP 17.4, WA 7.9, WR 18.2.
3. The standardisation test (section 5): each anthropometrist's readings of the test children against the supervisor's
   mean of her two readings, both sessions taken together: the offset (the mean departure) and the technical error of
   measurement of the two repeat readings (TEM), the test's two headline statistics.
4. The children's own figure: each reading less its anthropometrist's offset; the zone's variance less the mean TEM
   squared of its readings' anthropometrists; the share below 125 read the same way.
5. The note where the two figures, each to one decimal, differ by 2.0 points or more.

Ends on: four zones noted, North Pastoral, Central Pastoral, Laga Town and East Pastoral (points 3.3, -4.2, 4.6 and
4.7); North Lakeshore, West Pastoral and West Riverine at 1.1, 0.4 and 1.1.

Golden: seven zones noted, North Pastoral, North Lakeshore, Central Pastoral, Laga Town, East Pastoral, West Pastoral
and West Riverine (points 4.0, 4.1, -3.8, 5.2, 5.1, 2.9 and 4.5), each anthropometrist's random error taken as the
variance of its single readings' departures from the supervisor about its offset (the field error), not the repeat
readings' TEM.

## Stump sentence

A competent analyst builds each zone's error-free figure from the standardisation test's two headline statistics, each
reading less its anthropometrist's offset against the supervisor and the zone's spread less the anthropometrists' TEM
squared, and ends on four zones (North Pastoral, Central Pastoral, Laga Town and East Pastoral, points 3.3, -4.2, 4.6
and 4.7); the step that lands it
there is taking the repeat readings' TEM as the error a field reading carries, when the three scattered anthropometrists
(NCHA team 3 and PRK teams 5 and 6) repeat their own reading of a child with a repeat error of 1.0 to 1.7 mm yet depart
from the supervisor child to child by 5.1 to 6.3 mm about an offset near zero, so only the variance of each single reading's departure
from the supervisor about its offset takes the measurers out of the spread and gives the seven.

## Three rules

- **Task type:** general-statistics-data-science / missing-data-censoring-measurement-error, which serves Data Quality
  Monitoring & Alerting (the round's MUAC readings are the monitored data; the measurement note is the monitoring
  decision taken on them before the bulletin publishes them).
- **Domain test:** the quantity that decides is each zone's prevalence of MUAC below 125 mm in the children's own arm
  circumference, the readings' distribution deconvolved of the measurers' error under the classical additive error
  model: each reading is the child's arm plus the anthropometrist's offset plus a random error, the offset and the
  error variance estimated from a validation sample measured against a reference (the standardisation test against the
  supervisor), the error variance taken out of the spread and the tail read from the corrected normal. Replacing that
  object with a generic summary (the readings' own share, or the error read off the repeats) changes the call.
- **Swap:** in General Statistics the swap is of the method. "Which zones' figures carry the measurement note" with
  the error read as the measurers' repeatability (a reliability coefficient, the generic summary of an instrument's
  noise) files four zones; the call needs the error against the reference, a different statistical object on the same
  data. With the field's nouns swapped out ("which hospitals' readmission rates carry a coding note"), there is no
  continuous reading, no reference reader measuring the same subjects twice and no tail cut-off, and the note cannot be
  computed at all.
- **Layer 1:** two partners' exports in their own layouts (NCHA's CSV in mm with dates of birth and anthropometrist
  codes; PRK's workbook in cm with ages in months and names; two standardisation layouts, NCHA's long sheet of codes
  and readings, PRK's wide sheets in cm, one a session), NCHA team 2's uploads of 22 June sent again after a sync
  failure, typed MUAC errors outside 75 to 220 mm, children measured outside 6 to 59 months, PRK team 4's
  anthropometrist changing on 28 June (the teams workbook), and on the household side the form's version 4 codes. Each
  is produced by the system that records it; none is placed to be caught, and the call is the same under every handling
  of each (SF rows) or loudly wrong.
- **Layer 2:** estimation_fit, an estimate that ignores the data's measurement structure: the error carried by a single
  field reading has a fixed part (the offset) and a random part that includes the anthropometrist's child-to-child
  placement, which two readings of the same child by the same anthropometrist repeat and so never show; only the
  departures from the reference measure it.
- **Decisive step:** taking each anthropometrist's random error as the variance of its single readings' departures from
  the supervisor's reference about its offset, and taking it out of the zone's spread with the offset out of each
  reading, rather than the repeat readings' technical error of measurement (or no random error at all).
- **Not semantics:** reading every field, unit and code right (mm and cm, dates of birth and ages, the anthropometrist
  codes, the supervisor's rows, the sessions, the change of anthropometrist) still leaves the TEM route on four zones:
  the test's sheets say how each anthropometrist read each child, never which error statistic a field reading carries.
- **Not rule application:** the protocol files the estimand (the figure from the children's own arm circumference at
  the round's standard, read like the bulletin's figure and compared at one decimal, section 7) and the reference (the
  supervisor's mean of her two readings, section 5), and no way of estimating a measurer's error: executing every
  stated rule with the test's usual statistic files the four.
- **Analyst test:** a strong analyst who reads every file right and applies sections 5 to 7 as filed takes each
  anthropometrist's offset out of its readings and its TEM squared out of the spread and ends on four zones (North
  Pastoral, Central Pastoral, Laga Town, East Pastoral, points 3.3, -4.2, 4.6 and 4.7); on the simulator's clean truth the same route files the same
  four and changing the error statistic alone gives the seven (R3 in checks.py).
- **Estimand:** the protocol (`laga_nutrition_surveillance_protocol_v2_1.pdf`, sections 6 and 7): for each zone the
  readings' figure (children aged 6 to 59 months measured in its clusters, oedema counted, the rest's share below 125
  mm read from the normal with their mean and standard deviation) against the figure read the same way from the arm
  circumference of the zone's children themselves at the round's standard, the supervisor's technique (section 5); the
  note where the two, each to one decimal, differ by 2.0 points or more; the prompt asks how many zones carry it and
  which.
- **No decoy:** nothing is planted: no memo, earlier figure, draft or stakeholder argues a method or a zone; the June
  bulletin (a distractor) gives community screening shares by sub-county and says they are not comparable with the
  round; no file ranks the zones on the note.
- **No certified replay:** no certified or published 2027 figure exists for a method to reproduce; the error statistic
  is found from the data's structure (the scattered anthropometrists' repeats close, their departures from the
  supervisor wide, their offsets near zero).
- **Lesson:** a measurer's repeatability is not its error against the reference: an anthropometrist who repeats their
  own reading closely can still place the tape differently from the standard on each child, and the error that
  inflates a tail share is the single reading's departure from the reference, offset and scatter both. No build on file
  spends it (task241 a sensor's error against a reference at a displaced position, task237 the share of a composite's
  variance due to its attribute, task233 a gold-standard follow-up carried across base rates).

## Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control or
corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or half of
a reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 (default) offsets out, the TEM squared out of the spread: NP, CP, LT, EP | section 7's "at the round's standard" and section 5's reference send it to the supervisor | the supervisor's rows | yes, bias and TEM are the test's statistics | none | no | a subtraction | readable |
| 1 the TEM squared out of the spread, the readings' mean kept: none | none | the repeat readings | yes, the TEM as the measurer's error | none | no | a subtraction | readable |
| 2 the departures from the supervisor out of the spread, no offsets: NL, WP, WR | section 5's reference | the supervisor's rows | yes, accuracy against the supervisor | none | no | a variance | readable |
| 3 offsets out and the mean squared departure out of the spread: eight (adds ER) | section 5's reference | the supervisor's rows | yes, the test's accuracy figure | none | no | a mean of squares | readable |
| 4 (decisive) offsets out and the variance of the single readings' departures about the offset out of the spread: the seven | no sentence names an error statistic; section 5 names the reference and pools the sessions | no column; the sheets carry readings only | no: the reflex statistic is the TEM | no control, published figure or earlier round | no | not linear: an error model, an offset a reading and a pooled error variance, then a tail read from the corrected normal | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | differ by 2.0 points or more | the difference's size, 2.0 or more | more than 2.0 | same call | no zone within 0.4 of 2.0 under any variant; the nearest, East Riverine at 1.5 and West Pastoral at 2.6, are 0.5 and 0.6 away (asserted) |
| SF2 | compared as the bulletin prints them | each figure to one decimal, then the difference | the unrounded difference | same call | same call (asserted) |
| SF3 | the readings' standard deviation | divisor n - 1 | divisor n | same call | same call (asserted) |
| SF4 | a child's age | completed months on the day of measurement | months as days over 30.4375 | same call | same call (asserted) |
| SF5 | each child counts once | NCHA team 2's rows of 22 June sent again taken once | every row kept | same call | same call (asserted); section 6 "each child counts once" |
| SF6 | a MUAC below 75 mm or above 220 mm | a recording error, the child left out | kept | ruled out | section 6 "is a recording error, and that child is left out" (asserted that four such readings exist) |
| SF7 | children aged 6 to 59 months | 6 to 59 completed months | the 16 children measured at 4 to 5 or 60 to 63 completed months kept | same call | same call (asserted); section 6 |
| SF8 | PRK team 4's anthropometrist | Sharon Kinuthia from the cluster of 28 June | Albert Bosire through 28 June | converge | Albert Bosire's last cluster was 26 June and no cluster was worked on 27 June (asserted) |
| SF9 | the round's standard | the supervisor's mean of her two readings of each test child | the median of the anthropometrists | ruled out | section 5 "The supervisor's mean of her two readings is each test child's reference value" |
| SF10 | an anthropometrist's sessions | taken together | each reading against its own session's offset | same call | same call (asserted, variant V_session_offsets) |
| SF11 | the offset | every anthropometrist's mean departure | only offsets two standard errors from zero | same call | same call (asserted, variant V_significant_offsets) |
| SF12 | the departures' variance | divisor n - 1 | divisor n | same call | same call (asserted, variant V_ddof0) |
| SF13 | the reference's own error | the supervisor's mean as the reference | the supervisor's repeat error added back | same call | same call (asserted, variant V_reference_error) |
| SF14 | where the correction is made | each reading | the zone's mixture of offsets and errors | same call | same call (asserted, variant V_zone_level) |
| SF15 | the error variance's route | single readings' departures | departures of each child's mean of two readings plus half the TEM squared | same call | same call (asserted, variant V_means_route) |
| SF16 | a zone's children | those measured in its clusters, both teams' in a shared zone | none differs | converge | section 6 "a zone's children are those measured in its clusters" |
| SF17 | oedema | counted malnourished whatever the MUAC, in both figures | none differs | converge | section 6; no oedema child's reading moves either figure (asserted) |

## Ladder

Four wrong rungs and the golden, each a defensible way to estimate a measurer's error from the test, each dying to one
fact of the record (figures on the cut pack, printed by `generator/pair.py --ladder`, asserted in `checks.py`).

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 1 | the TEM squared out of the spread, no offsets | none (points 0.0 to 0.2) | the test: NCHA teams 1 and 5 and PRK teams 2, 3 and 4 read 2.1 to 4.0 mm off the supervisor, and section 7 compares at the round's standard |
| 0 (default) | offsets out, the TEM squared out of the spread | NP, CP, LT, EP | the test: NCHA team 3 and PRK teams 5 and 6 repeat with an error of 1.0 to 1.7 mm and depart from the supervisor by 5.1 to 6.3 mm about an offset near zero |
| 2 | the departures from the supervisor out of the spread, no offsets | NL, WP, WR | the offsets, as rung 1 |
| 3 | offsets out and the mean squared departure out of the spread | NP, NL, CP, LT, EP, ER, WP, WR | the mean squared departure holds the offset squared, which the readings have already had taken out (East Riverine's opposite offsets of plus and minus 3.8 mm counted twice) |
| 4 (golden) | offsets out and the variance of the departures about the offset out of the spread | NP, NL, CP, LT, EP, WP, WR | |

- **Margins.** The seven's points are 2.6 to 5.2 in size under every one of the seven readings of the golden (NP 3.9
  to 4.2, NL 3.2 to 4.2, CP -3.8, LT 5.2, EP 5.1 to 5.2, WP 2.6 to 3.0, WR 3.5 to 4.6); the other five at 1.5 or less
  (ER 1.5, EA 0.4 to 0.9, CA 0.6 to 0.7, WA 0.5, NA -0.1 to 0.4).
- **Position.** The seven are reached by no other rung; the default files four of them, rung 2 the other three, rung 3
  the seven and ER.
- **Dominance.** The decisive move adds NL, WP and WR to the default's four (their points from 1.1, 0.4 and 1.1 to
  4.1, 2.9 and 4.5) and moves the default's four by 0.4 to 0.7; it leaves the precise teams' zones at 0.9 or under.
- **Grid.** Offsets out or not, and the random error as nothing, the TEM, the departure variance or the mean squared
  departure: none (no offsets, TEM), four (offsets, TEM or nothing), three (departure variance or mean squared
  departure, no offsets), eight (offsets, mean squared departure), seven (offsets, departure variance). On the
  simulator's clean truth the default files the four and the decisive step alone the seven (R3).
- **Worth.** The decisive step is worth three zones on the count (four to seven) and three of the seven on the set; no
  single other correction reaches the seven.

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the children aged 6 to 59 months measured in the round, by zone (section 6); the twelve zones of Annex A |
| 2 | Unit of account | one zone's figure and one note a zone (section 7) |
| 3 | Attribution window | the 2027 long-rains round, fieldwork 14 June to 8 July 2027 |
| 4 | As-of dating | the exports as gathered after the round; the request of 14 July 2027 |
| 5 | Version basis | protocol version 2.1; the household form's version 4 for the household files (asks) |
| 6 | Denominator | the zone's measured children for each figure; households selected less empty dwellings and person-days for the asks |
| 7 | Weighting | none: each zone's sample is self-weighting and each reading counts one child |
| 8 | Window length | the round |
| 9 | Boundary inclusivity | MUAC below 125 mm; 2.0 points or more (SF1); MUAC from 75 to 220 mm kept (SF6); 6 to 59 completed months (SF7) |
| 10 | Rounding path | each figure to one decimal, then the difference (SF2); the asks at their stated rounding |
| 11 | Tie-break | none needed |
| 12 | Maturity and censoring | the round is complete; nothing later arrives |
| 13 | Order of operations | eligibility and duplicates, units, the anthropometrist on duty, the offsets, both figures, the comparison |
| 14 | Row order | no step depends on file order |
| 15 | Duplicate resolution | NCHA team 2's 22 June rows taken once (SF5); one cluster's household forms sent twice (asks) |
| 16 | Identity normalisation | NCHA's anthropometrist codes to the teams workbook's names; PRK's sheets by name |
| 17 | Netting against gross | none |
| 18 | Dimensional units | MUAC in mm (PRK's cm times ten); per cent; deaths per 10,000 a day |
| 19 | Code and status semantics | oedema y and n, 1 and 0; SUPERVISOR rows; the household form's outcome and reason codes (asks) |
| 20 | Integerisation | none for the call |
| 21 | Clause scope | sections 6 and 7 apply to every zone; section 5's pooling of an anthropometrist's sessions (SF10) |
| 22 | Forward window contents | the bulletin of 30 July and the months until the next round; nothing is forecast |

## Literal reader

Executing the prompt and sections 5 to 7 word for word: for each zone the readings' figure, and the figure read the
same way from the arm circumference of the zone's children themselves at the supervisor's standard, compared at one
decimal. The children's own arm circumference is recorded nowhere, so the literal estimand needs it estimated from the
readings and the test; every standard way of estimating the classical error model's offset and error variance from the
test (seven readings: the correction made a reading or a zone, the sessions pooled or apart, the variances on n or n -
1, the reference's own error added back, the offsets kept only where they stand out, the error routed through the
children's means) files the seven. The easy answer, the four, comes from an easy method on the same literal estimand
(the TEM as the error), never from another reading: every row of the fork table files the seven.

## Oracles

None for the call: no earlier round's zone figures, published 2027 figure or ranking of the zones ships, and the June
bulletin's community screening shares are by sub-county, from colour-banded tapes, and declared not comparable with the
round. For the ask, the visits' `members_present` ties to the rosters' present members under every reading of the
codes, and the births module ties to the rosters' members born in the period under every reading; neither arbitrates.

## Ask sheet

**Ask A, each zone's household response rate (per cent, one decimal), crude death rate and under-five death rate
(deaths per 10,000 people per day, two decimals)** (36 figures). H18: the round's annex figures every zone carries
beside its wasting figure (the request: "the mortality and household response figures for the annex"); the call reads
no visit, roster or birth. Use: the bulletin desk prints each zone's response and death rates in the annex. Primary
device D2 (a label stored before a silent switch): the county's household form went to version 4 on 21 June, and
version 4 swapped the third and fourth choices of two lists, the visit's outcome (version 3: 3 absent, 4 dwelling
empty) and the reason a member left (version 3: 3 died away from home, 4 moved with the mother or caregiver); the
server keeps each submission's codes as the tablet's form set them, and the dictionary gives version 4's. Nothing marks
a row's version; the visits show it (before 21 June all 55 households coded 3 at a first visit were visited again and
none of the 32 coded 4; from 21 June none of the 118 coded 3 and all 168 coded 4, against section 2's rule that a
household not at home is visited again and an empty dwelling is not), and so do the rosters (before 21 June, 7 of the
10 members coded 3 are aged 15 or more and 35 of the 48 coded 4 are under five; from 21 June, none of the 125 coded 3
is 15 or more). Hazards: deaths away from home entered among the members who left, with that reason (section 9 counts a
death wherever it happened; D3), newborns who died kept only on the births module (section 9's child born and dying
within the period; D4), one NCHA cluster's household forms sent twice under new form ids (D1), under-fives' ages in
months and everyone else's in years (D3), the recall start by sub-county (Annex B; D8). Path: the visits, the rosters,
the births module, the sample, the protocol's sections 2, 9 and 10 and Annex B, the dictionary (6 files, 16 columns:
the visits' cluster, hh_no, visit, date, outcome; the rosters' cluster, hh_no, interview_date, line_no, age, age_unit,
status, joined, born, left_reason; the births module's outcome). Stops: the dictionary's codes on every row, every
other handling right (the cracker): response -2.3 to +1.3, crude death rate -0.04 to +0.38, under-five death rate
+0.23 to +1.50, all 36 missed; deaths by the status alone: -0.33 to -0.10 in all 12 crude and -0.93 to 0.00 in 11
under-five; the births module left out: -0.21 to 0.00 in 10 crude and -1.05 to 0.00 in 10 under-five; the forms sent
twice kept: North Agro-pastoral +0.05 and -0.16; the age column read as years: -0.68 to +20.51 in all 12 under-five.
Realism: a tablet form updated mid-round with a reordered choice list keeps each older submission's stored codes, and
an export documented from the current form reads them at the wrong vintage; household forms record a member who died
while away with the herds or at a facility among those who left, and newborn deaths on the births module.

Main population zero-counts: the call reads the two anthropometry exports, the two standardisation files, the teams
workbook, the sample and the protocol's sections 5 to 7; no visit, roster or births row is among them, no device or
hazard row of the ask sits in an anthropometry or standardisation file, and the call computes identically with the
three household files removed (S1 in checks.py).

| Hazard | Asks moved | Per-ask deltas (largest) |
|---|---|---|
| the version 3 codes read as version 4 (D2, primary) | A | response -2.3, crude +0.38, under-five +1.50 |
| deaths by the status alone (D3) | A | crude -0.33, under-five -0.93 |
| the births module left out (D4) | A | crude -0.21, under-five -1.05 |
| the forms sent twice kept (D1) | A | crude +0.05, under-five -0.16 |
| ages read as years (D3) | A | under-five +20.51 |

Referee: the protocol's section 2 for the outcome codes and the rosters' ages for the reasons; neither names a version
or a code.

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed) | Verdict |
|---|---|---|
| Ask A, response, NP, NA, NL, CP, CA, LT | the last visit's outcome with the dictionary's version 4 codes, empty dwellings out of the selected | miss |
| Ask A, response, EP, ER, EA, WP, WA, WR | the same | miss |
| Ask A, crude death rate, all twelve zones | deaths with status D or left with reason 4, the births module's newborns who died, each member once, the recall from the sub-county's event, the mid-point population of section 9 | miss |
| Ask A, under-five death rate, all twelve zones | the same for the members whose age is in months | miss |

Measured by: generator/pair.py on the cut pack: the cracker keeps 0 of the 36 ask figures; the lazier paths keep 1
(deaths by the status alone: the under-five rate of Laga Town; the births module left out: the crude rate of West
Riverine) and 0 (the forms sent twice kept); the mirror (stopped at the mean squared departure, eight zones) keeps 21.4
of the 38 recommendation points (11 of 12 notes, 7 of 12 own figures inside the accepted range) and 1 of the 36 ask
figures.

Pair ceiling: 37.5 ((38 + 7 + 55 x 0) and (21.4 + 7 + 55 x 0.028), averaged)

Mirror leakage: 2.8 per cent of ask weight

## Pre-ship check

1. Domain: the call stands on each zone's prevalence below 125 mm in its children's own arm circumference, the readings
   deconvolved of each anthropometrist's offset and error against the supervisor under the classical additive error
   model; replacing that object with the readings' own spread or the repeat-reading error changes which zones are noted,
   and with another field's nouns there is no reference reader, no replicate test and no tail cut-off, so the task stops
   making sense.
2. Two layers: Layer 1 (two partners' layouts and units, NCHA's re-sent uploads, typed MUAC slips, children measured
   outside 6 to 59 months, PRK team 4's change of anthropometrist, the household form's version 4 codes) is neutral on
   the call (SF1 to SF17; the call is the same without the household files, S1). Layer 2 is the error statistic, asserted
   alone to move the default path to the golden on the simulator's clean truth (R3), where the golden also matches the
   children's own arm circumference as drawn in every zone.
3. No banned stump decides: nothing is planted (no figure, memo or ranking ships; the bulletin's screening shares are by
   sub-county and declared not comparable); not semantics (every field read right, the TEM route still files four); not
   rule application (the protocol files the estimand and the reference, no error statistic).
4. Gate G: no shipped artifact ranks the zones on the note; the three distractors give no zone a figure.
5. Determinism: the seven hold under all seven readings of the golden (points 2.6 or more in size) and the other five
   at 1.5 or under; each own figure is graded inside its accepted range; each readings' figure prints the same under
   either divisor; 17 fork rows asserted; the verifier recomputes the call and the household figures by its own code;
   two builds byte-identical.
6. Fingerprint: heart WARN (repeat.deliverables against task167, repeat.question_form against task168, both answered in
   the Draw); three card axes redrawn at stage 3 when task199, task168 and task167 reached this checkout; surface screen
   promotes task245 against task246 on the shared gap and decision type (population, designation_set) with different
   patterns (G9 against G17) and strategies; the stumps differ (lost days on a fixed source's wind against a measurer's
   error against a reference).
7. Judge (one isolated thread a pass, Sonnet, medium, the bundle and the graded blocks only). Pass 1 on the first cut:
   DETERMINISTIC, APPROVE; every figure reproduced (the count, both figures of all twelve zones, the offsets and errors,
   all 36 household figures); Gate G statistical_rigor, analytical_non_defect; Gate H domain, layers and decisive step
   pass. Its one minor note (Gate C/E): the protocol does not say the children's own figure is net of random error as
   well as offset; it judged the golden forced by the text and the data and the clause optional. Not added: section 7
   already files the estimand as the figure read the same way (mean and spread) from the children's own arm
   circumference, and a clause naming the error to remove would hand over the decisive step. Pass 2 on the shipped
   bundle, after the reader's realism pass: DETERMINISTIC, APPROVE, fix none; every figure reproduced (all twelve zones'
   two figures, the offsets, the departure SDs and the TEMs, all 36 household figures); Gate G statistical_rigor,
   analytical_non_defect; Gate H domain, layers and decisive step pass. Its two low notes: the estimator stays open,
   its spread covered by the accepted ranges; and a reading that counts the born-and-died newborns as deaths only moves
   five under-five rates by 0.01, which the literal mid-point formula of section 9 rules out. Its wrapper's note that
   the four-zone gaps quoted above are the first cut's does not hold: solve.py on the final pack gives 3.3, -4.2, 4.6
   and 4.7 under the default route, the figures quoted, so nothing moved.

## Leak check

`leak.py --asof 2027-07-21`: REVIEW, no LEAK. Each REVIEW line:
- Sweep 3, the protocol: 1.0 is a version number in the document history, not an answer; the 26 shared words are the
  twelve zone names of Annex A and the note's own vocabulary in section 7, which names no zone as noted. Harmless.
- Sweep 3, the June bulletin: 4.1, 5.2 and 5.8 are the community screening shares of Laga North, Laga East and Laga
  West (colour-banded tapes, children the volunteers reached), by sub-county and declared not comparable with the
  round; they equal graded figures only by coincidence of value. Harmless.
- Sweep 4, the dictionary, the README and the protocol: the shared terms are the field's nouns (supervisor,
  anthropometrist, reading, reference, standardisation, section); none names an error statistic, a variance or the
  departures about the offset. A governing clause that would exist without the build (section 5 names the reference).
  Harmless.
- Sweep 6, the protocol's Annex A, the cluster sample and the teams workbook: they name the zones beside cluster
  numbers, listings, teams and days; none gives a zone a wasting figure or ranks the zones on the note. Harmless.

Reader (one isolated agent, Sonnet, medium, the prompt and the pack only), on the first cut: Q1 to Q4 none ("No file
in the pack announces the answer"); Q5 section 6 fixes the readings' figure and section 7 the comparison, and it read
the open point as whether the correction is the mean only or the mean and the spread (4 against 7), the design's own
open method rather than a reading of the estimand, since section 7 asks for the figure read the same way (mean and
spread) from the children's own arm circumference; Q6 an analytical choice. Its attempt filed the seven. Its realism
notes were taken in one generator pass: the standardisation offsets and errors made less regular (offsets 2.1 to 4.0
mm off at six anthropometrists, no mirrored pair, the test sessions varying naturally about each anthropometrist's
offset), the scattered three's errors 5.1 to 6.3 mm, and NCHA's upload times following each team's tablet sync (the
evening at base, else the next morning or later) instead of the whole day. Exactly 15 households a cluster is the
protocol's design. The pass changed data only, so leak.py was rerun and the judge ran a second pass on the final bundle.

## Tried and rejected

- The seed's own pairing in air quality (public PM10 or ozone alerts): set aside at the draw; task245 shipped the same
  pairing and world type the same day, and the seed's averaging-period pitfall is a reading of the standard.
- Wastewater alert lines from off-season baselines with non-detects (a censored fit with each sample's own detection
  limit): rejected at the draw; task189 spends censored results with per-instrument limits, and the field's own
  convention (half the limit) would stand as a competing defensible answer.
- West Nile virus risk alerts from pooled mosquito tests (the pooled maximum-likelihood rate against the minimum
  infection rate): rejected at the draw; task188 spends it, and the alerts are about the world, not the data.
- Next season's alerts after a sampling or replicate cut (the noise decomposed at the new design): rejected at the
  draw; the honest strategy is signal against noise (uncertainty_hold, banned against task198) and a strong solver
  decomposes the noise by reflex once the cut is filed.
- Beach advisories caught by weekly sampling (a two-state process fitted to irregular samples): rejected at the draw;
  task182 spends length-biased observation, the monitoring rates from a few dozen routine samples a season are too
  noisy to force one answer, and a rainfall model would stand as a competing one.
- Inflation measured as the counted share less the error-free share: rejected in prototype; the counted share's
  binomial noise (about 1.5 points at 550 children) is the size of the two-point line, so the note is filed on two
  normal-frame prevalences, the readings' and the children's.
- Death rates held by documented devices only (deaths away from home among the members who left, newborn deaths on the
  births module, forms sent twice): rejected in measurement; section 9 and the hygiene battery hand each to a careful
  solver, so the cracker kept all 24 death rates.
- Household devices on one partner's own forms: rejected in measurement; a device on one partner's export touched half
  the zones, so the household interview moved to the county's form, which both partners' teams use.
- A one-sided note (the readings' figure above the children's own by 2.0 or more): rejected in design; Central
  Pastoral's loose tape understates its figure by 3.5 points, and a surveillance protocol would not publish that
  uncorrected; the note is now two-sided.
- A form version column on the household exports: rejected in design; it isolated the earlier submissions, a marker,
  so the switch is left to the visits' own pattern and the dictionary's "version 4".
- The form's update dated in the teams workbook's changes: rejected in design; the call reads that sheet for PRK team
  4's change of anthropometrist, so an ask's organ would sit in a main-call document.
