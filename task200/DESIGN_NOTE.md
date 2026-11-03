# task200 design note

Architecture 6, drawn 2026-11-03. Architectures 1 to 5 of this number died at stage 1 without a card on six
grounds (their lines are under `## Tried and rejected`, kept verbatim); this architecture re-roots into a client
domain the number had never used, with a new world, a new dataset and a new generator under `generator/`.

## Draw

| Item | Draw |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task200.json`, architecture 6, registered 2026-11-03T12:41:43Z; `guard.py check` on the registered card: WARN only (below) |
| Pairing | Human Factors & Ergonomics (client domain), task type `safety-incident-error-analysis`, which serves Root-Cause Analysis and Anomaly Detection & Diagnostics; objective Anomaly Detection & Diagnostics |
| Niche | an airport security department ordering its X-ray screening teams through the 2027 remedial image interpretation course from the threat image projection (TIP) records of two generations of screening machine |
| Call | the 2027 order of the remedial course, one team a month from February, the team whose X-ray operators are least likely to find a prohibited article in a passenger's cabin bag first (the screening standard SPS-04 files the WHAT) |
| Shape | 06, a sequence under capacity: one team per course month, six positions graded, beside a per-team grid of three asks |
| Strategy, gap, pattern | `composition_mix`; gap objective first (the projection detection rate is a correct number and is not what the order is scored on), population second; pattern none, generators G6 (composition shift: each team's mix of first and repeated meetings with an image) then G14 (the detection rate conditioned on a first meeting) |
| Gate G | `method_or_model_selection`: the pooled projection rate against the rate on first meetings, the data's own hit-by-meeting gradient choosing between them |
| Layer 2 | `estimation_fit`, `own:practice-inflated-proficiency-measure` |
| World | Brackenford Airport, a fictional regional airport in England owned by two councils, running its own security screening: Central Search (eight CT lanes since March 2024, each projecting from the CT system's own library of about 6,000 threat images) and Pier B Search (three legacy X-ray screens, PB1 to PB3, kept until a later replacement, projecting from the legacy library loaded on 11 September 2023, 420 images with 60 more added on 20 April 2026 in the same code range). Six screening teams on a rotating roster: Arden, Brook, Cleve, Dene, Esk, Fell. Fell is Pier B's team and works nowhere else; the other five work Central only. GBP |
| People | Marian Taylor, Head of Security Screening (the decision); Bernard Vincent, Security Training Manager (the course plan), drawn with `guard.py names --geo "United Kingdom" --seed 200`; no people warning on the card |
| Forum, forcing event, organisation | `other` (the Head of Security Screening sets the order herself, no formal forum), `season_or_peak` (the course runs in six monthly blocks, February to July, and the order is due by 22 January), `other` (a council-owned airport company) |
| Deliverables | `remedial_course_2027.xlsx` (the order and the per-team grid) and `remedial_course_2027_note.docx` (one page) |

**Data-native sentence.** Each screen projects its fictional threats from the library loaded on that machine,
so an operator meets the same threat images again and again, and a hit on an image already met measures memory
of that image rather than the skill of spotting a threat in a passenger's bag; the Pier B library is small and
Fell screens on it every shift, while the Central library is large enough that most of its projections are first
meetings.

**Abstraction sentence (Part 6).** "A unit's success rate on a test whose items recur is lifted by memory of the
items, so units drawing on the smallest item pool look able; the ability is read on each member's first meeting
with an item." No build on file is that sentence: no card's driver, stump or lineage carries a practice or
familiarity effect on repeated test items (searched over every card, and `guard.py slots` on the mechanism's
nouns and on the setting's nouns returns nothing on it; task171's screener prototypes priced a learning curve in
experience and stint length, both visible attributes, and died on the curve's form, which this construction does
not have, since a first meeting is a fact of each row's history).

**The spent drivers this draw stays off** (`guard.py mechanisms --objective anomaly-detection`, 35 builds, one
line each on what the nearest ones spend): task183, a part that has failed before keeps failing (heterogeneity
across units, not memory of test items); task181, exposure follows the crossings traffic creates; task180, events
recorded only above a daily noise cycle; task196, two capture channels with dependence; task199, an event recorded
only where a watcher filed; task190 architecture 3, items drawn into a tested set with probability proportional
to size (the card's one driver.near at 0.12: there the tested item stands for a share of the population, here the
tested item is the same item met again by the same member); task192, an instrument's validation batch covering
only the window's opening; task182, durations seen through snapshots; task202, unit averages losing the
within-unit spread; task241 (data quality, the same day), a classifier's error rate set by who is being
classified. None of them is a memory of the test's own items.

**Guard, read at the draw and on the registered card.** WARN only: `driver.near` 0.12 against task190
architecture 3 (answered in the line above) and `repeat.gate_g` against task241 (method_or_model_selection; the
mechanism differs, a classifier's error read from returns against a projection rate read on first meetings, and
gate_g carries no ban). Redrawn before registration: `context_artifact` filed_standard to planning_thread,
`forum` line_manager_or_team to other and `org_family` local_government to other, all three BLOCKed against
task194 v17 registered the same morning; the decisive gap population to objective and the decisive generator G14
to G6, because population with G14 under method_or_model_selection is spent in nine builds, and objective is the
honester gap here (the projection rate is right as a number and wrong as the order's basis).

**Sources, one line each** (every file generated, seeded, CC0; the airport, its teams, its systems and its
people are invented):
- the Central Search CT system's TIP exports for 2024, 2025 and 2026 (UTC, operator login, image identifier, threat
  category, result), the 2026 export the volume spine;
- the Pier B legacy X-ray TIP log since the September 2023 library load (UK local time, TIP operator number, image
  code, a three-line preamble);
- the screening roster at 31 December 2026 with each screener's staff number, team, role, CT login, Pier B TIP operator
  number, badge and start date, and the 2026 team moves; the ID Centre badge register;
- the Central CT workstation sessions for 2026 (UTC, one row per lane a queue served) and the Pier B screen event log
  (log-ons, log-offs, shutdowns and tray rejects in local time, by badge);
- the CT tray reject log for 2026 and the search team's 2026 search log;
- the LMS assessment export of 11 January 2027 and the assessment centre's certificate list;
- the screener performance standard SPS-04, the course planning email, the lane throughput, the queue time samples
  and the compliance team's 2026 review.

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' grain, with the field's own measure
of screener detection in it (the threat image projection detection rate, the regulator's and the airport's routine
performance figure, then signal detection theory's d-prime as the human-factors reflex):

1. Read the three Central CT TIP exports and the Pier B TIP log, drop the repeated first-of-month rows the CT exports
   carry, convert the Pier B local times, and drop cancelled projections (SPS-04 section 3).
2. Map each CT login and Pier B TIP operator number to a staff number and team through the 31 December roster
   (SPS-04's team definition), leaving out leavers.
3. For each team, take its 2026 projections and compute the share it hit: Brook 71 per cent, Dene 75, Esk 79, Fell 80,
   Arden 82, Cleve 86.
4. Check the figure the field's way: d-prime against each team's clear searches per screen-hour puts Esk lowest
   (2.96 against 3.04 to 3.47), and a logistic model with threat class and practice to date leaves Brook lowest;
   the score is stable for the Central teams year on year (Brook lowest in 2024, 2025 and 2026).
5. Order the teams from least to most likely to find an article (SPS-04 4.2).

**Ends on:** Brook first, the order Brook, Dene, Esk, Fell, Arden, Cleve (Fell fourth).
**Golden:** Fell first, the order Fell, Brook, Dene, Esk, Arden, Cleve.

## Stump sentence

A competent analyst orders the 2027 remedial course by each team's 2026 threat image projection detection rate and
starts with Brook (71 per cent, Fell fourth at 80), or by d-prime and starts with Esk; the step that lands it there
is treating every projection as a fresh test, when 4,104 of Fell's 5,229 projections in 2026 showed a Pier B library
image its operators had already met, and on the images each operator met for the first time Fell finds 63 per cent
against 69 for Brook, the lowest at the airport.

## Three rules

Task type: Human Factors & Ergonomics, `safety-incident-error-analysis` (serves anomaly-detection and root-cause): the anomaly is the screening team whose detection of threat articles is weakest, diagnosed through the airport's own threat image projection records, which is the domain's performance-monitoring analysis of a human error (a missed threat).
Domain test: the deciding quantity is each team's chance of detecting a threat article it has never seen, which aviation security monitors through threat image projection: fictional threat images superimposed on live bags from a fixed library loaded on each machine, scored per operator login as hits and misses and read beside the false searches on live bags; swap in another field's nouns and the projection mechanics, the per-machine library and the bag searches have nothing to stand for.
Swap: "the team whose X-ray operators are least likely to find a prohibited article in a passenger's bag, read from the threat images projected at their screens" becomes "the ward whose nurses are least likely to spot a deteriorating patient, read from the simulated alerts injected into their monitors": the simulated alerts would need a fixed library per monitor that some wards meet all day and others never repeat, which no hospital system has, so the sentence stops making sense.
Layer 1: two TIP systems written by different vendors (the CT system's annual exports in UTC with operator logins and HIT, MISS and CANCELLED; the Pier B legacy log in UK local time with a three-line preamble, TIP operator numbers and H, M and X codes); the CT exports' rows from the first hours of each month's first day repeated because each annual file is stitched from monthly pulls, each run at 06:00 UTC on the first and taking everything since the last pull began; cancelled projections; team moves in April and June 2026 and leavers absent from the roster; the CT workstation log writing one row per lane a queue served; the Pier B screens' access log writing a log-on but often no log-off, and ID badges replaced in 2026; reusable tray barcodes and two trays on one search record; the search tablet's codes changed in its July update; externally assessed certificates keyed into the LMS weeks after the assessment, so the centre's December 2026 certificates are not in the January LMS export yet. Each is the system's own behaviour, documented by the file's own header, codes or the register beside it, and none is placed to be caught.
Layer 2: estimation_fit: the projection score is a correct number measured on a test whose items recur, and the analysis that decides is reading the team's ability only on each member's first meeting with an image, because on an image already met the hit says more about remembering that image than about spotting a threat.
Decisive step: score each team on the threat images its operators met for the first time, counting every earlier projection of the same image to the same screener back to the load of each machine's library, because the Pier B library is small and Fell meets it all day while the Central library is large enough that most of its projections are first meetings.
Not semantics: every field, code, unit and definition read correctly (the result codes, the clocks, the operator mapping, the team rule, the cancelled projections) still gives the projection score Brook 71, Dene 75, Esk 79, Fell 80, Arden 82, Cleve 86 and an order that starts with Brook; no field says which projections were first meetings, the property is a relation between rows of one screener's history.
Not rule application: SPS-04 files what the order ranks (how likely the team's operators are to find a prohibited article in a passenger's bag) and no rule or procedure says how that chance is estimated from TIP records; the enumerated family a competent analyst reaches for (the projection rate, d-prime at five tray rates, logistic models with threat class, screening area and practice to date, Central-only rates, first meetings counted inside 2026) spreads from Brook first to Esk first and never puts Fell above third, the standing family the data leave defensible once each projection's earlier meetings are counted (pooled first meetings, the member mean, a logistic with earlier-meeting terms read at none) agrees on the whole order with a spread of 2.5 points on Fell's figure against a smallest gap of 3.4 points, and what rules the rest out is loud only once looked for: inside Fell the hit rate climbs from 63 per cent on a first meeting to 84 per cent on an image met before.
Analyst test: a strong analyst who cleans both TIP systems, maps every operator to the 31 December roster and reads SPS-04 ranks the teams on their 2026 projection score and starts the course with Brook (71 per cent, the default path's `Ends on:` Brook first), or on d-prime and starts with Esk, when Fell, whose operators had already met most of the Pier B library, finds 63 per cent of the images it meets for the first time.
Estimand: SPS-04 section 4.2 in `docs/SPS-04_screener_performance_standard_issue3.docx`: the course starts with the team whose X-ray operators are least likely to find a prohibited article in a passenger's cabin bag and runs to the team most likely to find one; population, the screeners on each team's 31 December 2026 roster (section 3, every X-ray operator on it, starters and supervisors included); outcome, finding a threat article in a bag; window, how the teams screened in 2026 (section 4.3); unit, the team; comparison, the teams against each other.
No decoy: nothing is planted to be caught: no copied block, no withheld rule, no memo, draft or briefing, no stakeholder figure written to carry the wrong answer; no shipped artifact ranks the teams on any measure, and the standard defines no metric.
No certified replay: the method is not hidden and recovered by reproducing certified or published figures; the pack carries no published TIP score, no certified rate and no prior order to reproduce.
Lesson: a performance test whose items recur measures memory of the items as well as the skill, so the units that meet a small item pool most often look most able; the ability is read on each member's first meeting with an item, from the member's own history. No build on file carries a practice or familiarity effect on recurring test items (every card's driver, stump and lineage searched).

## Survivor anatomy

Actor: the deciding property (whether the screener had met this image before) has no column in any file: it is a relation between rows of one screener's projection history across three CT exports or the Pier B log, two to three years deep, and no column holds a count, a flag or a date of first presentation.
Link: the signal is read through a comparison the field's method never asks for, each projection against the same screener's earlier projections of the same image; the keys exist (operator and image) but no sentence, header or document invites the comparison, and the TIP score as the airport and regulator use it pools every projection.
Reflex: the field's named measure for the deciding quantity is rung 0 (the TIP detection rate, Brook first) and signal detection theory's d-prime is rung 1 (Esk first); both file a wrong answer here, and the default path carries both.
Back-test: the textbook route validates: the projection score is stable for the Central teams across 2024, 2025 and 2026 (Brook lowest each year, the Central order unchanged), and Fell's rise from 75 to 80 per cent over the same years reads as a team improving.
Second use: every file the decisive step reads ships for its own reason: the 2024 and 2025 TIP exports are the system's own year files and carry the year-on-year check the textbook route validates on, the Pier B log is the pier's whole TIP record since its library was loaded, and the roster maps operators for every rung and every ask; delete the decisive step and the pack still carries all of them.
Shock: the movement the step recovers reads as ordinary: on every shipped per-team statistic Fell sits inside the range (fourth on the projection score, fourth on d-prime, second lowest on screen time behind Dene and on clear searches behind Brook, level with Cleve and Dene on certificates), and its upward trend reads as improvement rather than as the pack's largest anomaly.
Pins: SPS-04 files the WHAT (who is counted, what the order ranks, the year it is read on) in the organisation's own standard, and no filed sentence names a first meeting, a repeated image, the library, the history or any test; deleting 4.2 unforces the call, and it names only the outcome.

## Readability screen

The reflex row is enumerated from the field's vocabulary for screener detection (the TIP detection rate, a per-threat-class rate, d-prime or A-prime against false alarms, a learning curve in experience, machine-type adjustment, covert test results), never from the rungs.

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Readable |
|---|---|---|---|---|---|---|---|---|
| 0 the 2026 projection detection rate | no | yes (result column, one group-by) | yes | no | yes | yes | no | readable |
| 1 d-prime against clear searches | no | yes (the search log's outcome) | yes (the human-factors method) | no | no | yes | no | readable |
| 2 logistic with threat class | no | yes (threat class column) | yes | no | no | no | no | readable |
| 3 logistic with practice to date | no | no | yes (experience as a covariate) | no | no | no | no | readable |
| 4 Central projections only | no | yes (the system the file comes from) | yes (like-for-like machines) | no | no | yes | no | readable |
| 5 first meetings counted inside 2026 | no | no | no | no | no | no | no | readable |
| decisive: first meetings over each screener's whole history | no (no sentence names an earlier meeting, an image or a library) | no (no column marks a first presentation; the image codes of the 2026 additions are drawn from the same number range as the 2023 load) | no (the reflexes are rungs 0 to 3) | no (no control or corpus scores the teams) | no (the battery dedupes, converts clocks and maps codes, and stops) | no (a running count per screener and image across three years of two systems, then a filter) | no (the TIP exports are the system's own year files, used by every rung) | silent |

Rung 5 is marked readable because once the idea of a first meeting is held, the history is one file away; it is the
half-handled form of the decisive step and files Brook first.

## Semantic fork table

| Id | Term or convention | Golden reading | Alternatives | Call under each | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the CT exports' repeated first-of-month rows | dropped as exact copies | kept | same call | exact copies; asserted in `checks.py` (SF1) |
| SF2 | cancelled projections | not shown, so neither a projection nor a meeting (SPS-04 section 3) | read as shown misses | same call | SPS-04 section 3; asserted (SF2) |
| SF3 | a team's screeners | the 31 December 2026 roster (SPS-04 section 3) | the team each screener was in on the day of each projection | same call | SPS-04 section 3; asserted (SF3) |
| SF4 | 2026 | UK local dates | UTC dates | same call | no projection near midnight moves a team; asserted (SF4) |
| SF5 | an earlier meeting | any earlier projection of the same image to the same screener since the library's load, which is where each export begins | (the estimate, not a reading: no field holds it) | not applicable | recorded so the judge sees it is the decisive step, not a term; asserted as the golden's construction (SF5) |
| SF6 | screeners who left during 2026 | not on the roster, so outside every team | kept under their last team | same call | SPS-04 section 3; asserted (SF6) |
| SF7 | the Pier B clock | UK local time, as the log's own date and time columns are | UTC | same call | asserted (SF7) |
| SF8 | a team's figure | pooled over its screeners' first meetings | the mean of each member's own rate | same call | asserted (SF8) |
| SF9 | rounding | each team's rate computed from counts and printed to a whole per cent | rounded before ordering | same call | every first-meeting rate at least 0.23 points from a whole-per-cent edge; asserted (SF9) |
| SF10 | screening supervisors | X-ray operators on the team (SPS-04 section 2) | left out | same call | SPS-04 section 2; asserted (SF10) |
| SF11 | 2026 starters | on the team (SPS-04 section 3) | left out | same call | asserted (SF11) |
| SF12 | the images added to the Pier B library in April 2026 | projections like any other | left out | same call | asserted (SF12) |
| SF13 | screen time against SPS-04 5.1 (ask A) | logged-on time (section 3): a Pier B log-on runs to the operator's own log-off, the next log-on at that screen or the shutdown | 5.1's 20 minutes at a stretch read as a cap on each logged-on span | same call, same figures (no golden span is longer than 20 minutes, Pier B log-ons included) | C1 converge; asserted (SF13.cap20_inert, askA.variants_converge) |

## Ladder

Measured on the built pack (six teams, 35,517 shown projections in 2026, the history back to September 2023 at Pier B
and March 2024 at Central), every rung's first team and order asserted in `generator/checks.py`.

| Rung | Construction | First team | Fell's place | Killed by |
|---|---|---|---|---|
| 0 | every 2026 projection's hit rate (the field's measure) | Brook (71.3 per cent) | 4th (79.7) | Fell's hits on images met before |
| 1 | d-prime against clear searches per screen-hour, at 80 to 300 trays a screen-hour | Esk (2.96) | 4th | measures separation, not how often a team finds an article; and still pools repeats |
| 2 | logistic with threat class, read at the airport's mix | Brook (71.3) | 4th | threat class is not what differs |
| 3 | logistic with threat class and log practice to date | Brook (71.5) | 4th (79.2) | practice to date is similar across teams; memory is per image |
| 4 | Central projections only, like-for-like machines | Brook | absent | leaves the Pier B team out of the comparison |
| 5 | first meetings counted inside 2026 only | Brook (70.8) | 3rd (77.2) | most of Fell's earlier meetings fell in 2024 and 2025 |
| golden | first meetings over each screener's whole history | Fell (62.8 per cent, 707 of 1,125) | 1st | |

Order under the golden: Fell 62.8, Brook 69.2, Dene 73.7, Esk 77.1, Arden 80.9, Cleve 84.9 per cent; adjacent gaps
6.4, 4.5, 3.4, 3.7 and 4.1 points. Golden family: the member mean (Fell 64.1, Brook 68.7) and a logistic with
earlier-meeting terms read at none (Fell 61.6, Brook 69.6) give the same order, largest spread 2.5 points against
the smallest gap of 3.4. Position: Fell is fourth on rung 0, never first on an intermediate rung, second on none
(third on rung 5). Dominance: Fell's first-meeting deficit to Brook (6.4 points) against the advantage memory buys it
on every projection (Fell above Brook by 8.4 points on rung 0) is the reversal the step makes; inside Fell the hit
rate is 63 per cent on a first meeting and 84 per cent on an image met before (4,104 of its 5,229 shown projections).

**The pricing sequence.** (1) Residue the filed WHAT leaves: the estimator of each team's chance on a never-seen
article; a method, not a knob. (2) The move against the ceiling: Fell must move 8.4 points from rung 0 to fall
below Brook, and memory carries 4,104 of its 5,229 projections at 84 against 63 per cent, worth 16.9 points on its
overall score (no Central team gains more than 2.1). (3) The one-group-by route: no shipped column groups first meetings, and the running count is
not affine in any shipped column (the closest, practice to date, is rung 3 and files Brook). (4) The standard error
of what the step estimates: Fell's first-meeting rate rests on 1,125 projections (about 1.4 points), Brook's on 5,026
(0.7), against a 6.4-point gap. (5) Lever and noise are not the same variance: the step moves a level (which
projections count), not a variance. (6) Not a variance correction. (7) The subset the step reads (first meetings) does
not publish the answer in any other column. (8) The reflex sweep, run as code in `checks.py`: the projection rate, d-prime
at five tray rates, three logistic forms, Central only and first meetings inside 2026 all file Brook or Esk first.

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | each team's screeners on the 31 December 2026 roster, starters and supervisors included (members not yet observed: none) | filed in SPS-04 section 3; C1 (SF3, SF10, SF11) |
| 2 Unit of account | the team | filed in 4.2; C1 |
| 3 Attribution window | how the teams screened in 2026, UK local dates | filed in 4.3; C1 (SF4, SF7) |
| 4 As-of dating | the exports of January 2027 | C1 (no 2026 projection arrives later) |
| 5 Version basis | the CT annual exports and the Pier B log read as one history per screener | C1 (the image codes of the two systems never overlap) |
| 6 Denominator | each team's shown projections on first meetings | the estimate; its alternatives are rungs, not readings |
| 7 Weighting | pooled over screeners | C1 with the member mean (SF8) |
| 8 Window length | the history back to each library's load | the estimate (SF5); the exports begin at the loads |
| 9 Boundary inclusivity | not applicable (an order, no threshold) | C1 |
| 10 Rounding path | rates from counts, printed to whole per cent, ordered on the unrounded rate | asserted mid-bin (SF9) |
| 11 Tie-break | none needed (smallest gap 3.4 points) | C1 |
| 12 Maturity and censoring | none (2026 is closed; no projection is pending) | C1 |
| 13 Order of operations | dedupe, drop cancelled, map operators, count earlier meetings, filter to 2026, group | C1 (SF1, SF2) |
| 14 Row order | time order; same-second ties by file order | C1 (no same-second repeat of one image to one screener) |
| 15 Duplicate resolution | the repeated first-of-month rows dropped as exact copies | C1 (SF1) |
| 16 Identity normalisation | CT logins and Pier B TIP operator numbers mapped through the roster; Pier B badges read through the ID Centre register for the asks | C4 (an unmapped login or operator number is a leaver, outside every team; SF6) |
| 17 Netting against gross | not applicable | C1 |
| 18 Dimensional units | shares of projections; hours for the asks | C1 |
| 19 Code and status semantics | HIT, MISS, CANCELLED and H, M, X, crosswalked by the Pier B log's own preamble | C1 |
| 20 Integerisation | not applicable | C1 |
| 21 Clause scope | 4.2 orders all the teams; 4.1 one team a course month | filed |
| 22 Forward window contents | the 2027 course, February to July, one team a month (the planning email) | filed in 4.1 and the email |

## Literal reader

Executed on paper word for word: SPS-04 4.2 fixes the outcome (how likely the team's X-ray operators are to find a
prohibited article in a passenger's cabin bag), section 3 the population (the 31 December roster) and the meaning of a
hit, a miss and a cancelled projection, 4.3 the year; no shipped field states any team's chance of finding a real
article, so every literal reading needs an estimate from the projection records, and the easy answers (Brook on the
projection rate, Esk on d-prime) are easy methods on the same literal estimand, not other readings. Every convention
the estimate needs is closed in the fork table; the method is left open and forced by the data: inside every team the
hit rate on an image met before is far above the rate on a first meeting (63 against 84 per cent at Fell, 69 against 86
at Brook), so a hit on an image met before is not a hit on an unseen article, and a real article in a bag is always
unseen. Pass.

## Oracles

- The clean truth in the generator: each team's true chance on a first meeting orders the teams Fell, Brook, Dene,
  Esk, Arden, Cleve (63.7 to 84.4 per cent) and the mean member skill gives the same order; asserted.
- No control, published figure, reconciliation column or corpus in the pack scores the teams on detection, and the
  compliance review's covert tests are reported for the airport as a whole (and were missed at the divest and archway
  stage, not at a screen); nothing ties only under the golden.

## Ask sheet

Three asks, each per team (every team in every ask), each a reconstruction across two systems or grains no sentence
states, sited on files the main call never reads (the session logs, the screen events, the reject and search logs,
the badge register, the LMS and the centre's certificates), none touching the projection records.

**Ask A, screen time.** Each team's 2026 hours at an X-ray screen, to one decimal (6 figures). Use: Bernard Vincent's
cover plan for the course month. Primary device D6 (one event's quantity on every line it covers): the Central
remote-screening log writes one row per lane a workstation's queue served, and a two-lane queue picks its second lane
up part way through a session, so the second row lies inside the first; summed as exported the Central teams' hours
run about a fifth high (19.9 to 20.6 per cent). Second device, another family (a state rebuilt from an event log, D4): the Pier B screens
write a log-on but often no log-off, the next operator's log-on or the screen's shutdown ending a session; and the
Pier B badges are read through the ID Centre register, because badges replaced in 2026 are not on the roster.
Filed: SPS-04 section 3 (screen time is logged-on time), naming neither device. Stops: the rows summed with Pier B
closed at the next log-on through the roster's badges (the cracker); the rows summed with only paired Pier B log-ons
(the mirror); the rows merged with roster badges (Fell missed); golden.

**Ask B, clear searches.** Each team's 2026 clear searches (6 figures). Use: the trainers size each block's clutter
and false-alarm session on the team's clear searches (the planning email).
Primary device D6 (one record covering several events): at the busiest times an officer clears two trays of one
passenger on one search record, the tray tags joined by a semicolon, and the two trays were often rejected at
different screens by different screeners. Second: tray barcodes are reused all day, so each tray is read to its latest
reject before the search was taken, through the CT reject log (UTC) or the Pier B screen's REJECT event (local time,
by badge through the register). Hazard: the tablet's codes changed in July (NF to CLEAR). Filed: SPS-04 section 3 (a
search is charged to the screener whose decision sent the tray; a clear search finds nothing at all). Stops: each
record once against its first tray with roster badges (the cracker); each record once with the register (the
mirror); records split with roster badges (Fell missed, its replaced badges' rejects unread);
golden.

**Ask C, certificates.** Each team's screeners whose image interpretation certificate runs out before 1 July 2027 (6
figures). Use: recertifying them on the course. Primary device D8 (a recorded date for the event date): an
assessment sat at the external centre reaches the LMS as an EXT-IIC row dated when HR keyed it, weeks after the
assessment; the centre's certificate list carries the assessment date, joined by the certificate reference, and in
every team one or two long-serving screeners were assessed there in late spring 2024 and keyed after June. Second
device, another family (D4, absence in the habitual source evidenced in a file the habitual join does not reach): two
screeners in different teams (Arden and Dene on this cut) whose certificates run out in spring 2027 booked their
renewal at the centre early and sat it in early December 2026; the centre's list holds those certificates under the
candidate's staff number, and the LMS export of 11 January does not yet, so a solver who dates the LMS's EXT-IIC rows
through their references still counts both as running out. Filed: SPS-04 section 3 (a certificate runs three years
from the assessment that awarded it, a screener holds one at a time and a later pass replaces it), naming neither
device. Hazards: failed IIC sittings and the annual refresher, which SPS-04 says renew nothing. Stops: the LMS dates
(the cracker and the mirror); the centre's dates through the LMS references (Arden and Dene missed); the LMS dates
with the centre's unkeyed certificates added (every team missed); golden.

Main population zero-counts (asserted in `checks.py`): the call reads only the TIP exports and the roster, so no ask
device sits in its rows; deleting every ask file leaves the order and every first-meeting figure identical; the
distractors (throughput, queue samples, the compliance review) deleted move nothing.

| Ask | What the cracker does | Cracker |
|---|---|---|
| A | CT rows summed as exported; Pier B log-ons closed at the log-off, the next log-on or the shutdown, badges through the roster | misses |
| B | each clear record once, against its first tray's latest reject, badges through the roster | misses |
| C | each screener's latest passed certification on its LMS date | misses |

Measured by: `generator/ceiling.py` on the cut pack (stage 3), every route's figures asserted off the golden in
`generator/checks.py`.

| Ask | Graded figures | Cracker keeps | Mirror keeps | Cracker |
|---|---|---|---|---|
| A screen time | 6 | 0 | 0 | misses |
| B clear searches | 6 | 0 | 0 | misses |
| C certificates | 6 | 0 | 0 | misses |

On the cut pack the cracker keeps none of the 18 ask figures and the mirror none. Each device fixed alone buys under
a third of the ask weight: the CT rows merged 5 of 18 (27.8 per cent), the two-tray records split 5 of 18 (27.8), the
centre's dates through the LMS references 4 of 18 (22.2), the centre's unkeyed certificates 0 of 18, the badge
register 1 of 18 (5.6). With the call landed at 38 plus 7 and the
best miss at 5 plus 7, the pair is (45 + 55 x 0.000 + 12 + 55 x 0.000) / 2.

Pair ceiling: 28.5.
Mirror leakage: 0.0 per cent of ask weight.

**Shape arithmetic (the 25 criteria).** The order, six positions (6); screen time, clear searches and certificates
for each team (18); the note with the order and its reason (1 to 2); the files (2): 27 to 28.

## Leak sweep

`leak.py task200 --asof 2027-01-15` at stage 3: REVIEW on three lines, no LEAK, each ruled harmless.
- Sweep 4 on SPS-04 (11 of 25 stump-paragraph terms): the standard defines a threat image projection, a screener, a
  team, screen time, a search and a certificate, which is what a screener performance standard is for, and names no
  earlier meeting, repeated image, library or history of a screener (`doc.sps_silent` in `checks.py`); its one
  "history" is the revision history heading and its "standard" its own title.
- Sweep 4 on the compliance review (4 terms): its "meeting" is the security management meeting of 14 December 2026,
  its "articles" the covert test articles, and it puts screener image interpretation outside its own scope.
- Sweep 12 on SPS-04 (4 column names: Screen, Team, cancelled, workstation): ordinary words of the standard's own
  definitions (an X-ray screen, a team, a cancelled projection, a remote screening workstation), not a note on any
  file's columns; the standard names no file, column or code.
- `guard.py surface task200`: 0 of 302 pairs promoted (nearest task174 at 0.040); its persona NOTE "Vincent Security"
  is the planning email's signature, Bernard Vincent's name line run into his job title, not a person. `guard.py heart
  task200`: WARN only, the two lines answered under `## Draw`.

## Stage 4 rulings

Determinism judge r1: DETERMINISTIC, APPROVE, Gate H decisive_step analytical; the leak reader found no leak.
- Screen time off its rounding edges (the judge's one finding): Dene's 2026 screen time sat 0.011 h from the .75 edge
  and Arden's 0.014 h (the judge listed Brook at 0.029, Cleve and Esk at 0.04). `pack.clear_hours` now runs after the
  positions, searches and badge register are written: where a team's total, or the airport's, sits within 0.03 h of
  a tenth-of-an-hour edge, its latest sessions that end a screen's day (nothing after them at that screen that day,
  the operator's next session at least 25 minutes off, still no longer than 20 minutes and inside the area's hours)
  run a few whole seconds longer (Arden 184 s over two sessions, Brook 83 s over two, Dene 167 s in one). Every
  projection, reject and search was drawn before, inside the sessions as they were, so none moves. On the cut pack:
  Arden 5,168.81 (still 5,168.8), Brook 4,750.90 (still 4,750.9), Dene 4,593.79 (4,593.7 to 4,593.8, the one graded
  figure that moved), Cleve, Esk and Fell untouched; the nearest figure is 0.035 h from its edge, and every merge and
  clipping variant (rows that only meet merged, the year by UTC date, rows clipped to the year) files the same hours
  to the second. Asserted in `checks.py` (`askA.edge` at 0.02 h under every variant, `askA.variants_converge`,
  `askA.total_edge`, `askA.moves_small`, and `figures.graded_edges` over every graded figure: hours, the stated
  percentages and the whole counts). An authorised ask move: `freeze.py check --mode rubric` PASS (the main call, the
  stump and every frozen figure unchanged, one ask figure moved); `--mode determinism` fails on that figure by
  construction.
- The exposure window (judge's open point, no change): a memory window of 18 months or less puts Brook first, and it
  is outside the reasonable set. No shipped file grounds a memory window (SPS-04, the email and the exports name no
  period after which an image counts as new again), so any window is a parameter the solver invents; "never shown
  before in the exports" is the one parameter-free definition of a first meeting, and every window of 730 days or more
  agrees with it on the whole order. The prompt is unchanged.
- SPS-04 revision history: the reader's note dated Issue 3 at 31 December 2026; the shipped text read 1 December
  2026 in both the header and the table, so the claim did not reproduce. The table now carries an Issued column beside
  Effective, each issue issued before it took effect, Issue 3 issued 24 November 2026 (its approval date and the
  file's last save) and Issue 1 on the file's creation date, asserted in `doc.sps_issue_dates`.
- SPS-04 5.1 against ask A (pass 2's one live alternative, Fell only): read as a cap on a logged-on span, the 20
  minutes at a stretch put Fell at 4,522.7 against the golden 4,603.7, because a Pier B log-on left open could run past
  20 minutes to the next log-on or the shutdown. Closed in the data, not the text: the Pier B screens now prompt an
  operator still logged on 20 minutes after logging on, who logs off, so no log-on stays open past 20 minutes and the
  cap moves nothing (C1, `SF13.cap20_inert`; SPS-04 unchanged, no sentence names the device). Fell's screen time moves
  to 4,484.2 (an ask figure), Brook takes 15 more seconds to keep the airport total off its edge (4,750.9 unchanged),
  every other figure, the call and the main-call figures unchanged, the nearest figure still 0.035 h from its edge.
  Explicit log-offs only (2,476.2 on pass 2) remains the mirror's route, which section 3's logged-on time rules out
  for a log-on the next log-on closes.
- Judges r2 and r3: DETERMINISTIC, APPROVE (r2 derived before reading the blocks; r3 reproduced every critical
  component and all 24 ask cells). r3's residual, no change: the overall TIP rate is the surface read SPS-04 4.2's
  "a prohibited article in a passenger's cabin bag" does not license, and a first-meeting history cut to 2025 or later
  (Brook first) discards shipped export years that nothing in the pack retires, so it is not a licensed reading.
- r3's optional sentence (that the articles in passengers' bags are ones the operator has not been shown before)
  declined: it names the thing the decisive step recognises, which is filing the stump (the fork-is-the-stump test),
  and the call is forced without it.
- Write-up step 5 now says that no Pier B log-on runs past the 20 minutes at a stretch of SPS-04 section 5, the WHAT
  behind Fell's 4,484.2 (no new method).
- The compliance review (a distractor, nothing graded reads it) re-cut as a Word for Microsoft 365 export: PDF 1.7,
  the body font embedded as subsets, the document language and an XMP packet, created 4 December and last saved 10
  December 2026, before the 14 December meeting it was prepared for; its opening line now reads "For the security
  management meeting of 14 December 2026" so no stamp precedes what the file states. Asserted in
  `doc.review_word_export`; every graded figure unchanged.
- Second leak read (after the stage 4 repairs): clean. Rulings, harmless, one line each: SPS-04 with its Issued column
  is the organisation's own standard, issued before effective in every row and matching the file's metadata, its 5.1
  rule matching the data; the Pier B log is an authentic export, the 20-minute ceiling reading as the screen's
  prompted log-off under a stated rule; the documents and the email rank no team and suggest no measure.
- `target.zip` now holds the files under `target/` (25 members: the folder, its six subfolders and 17 files).
- Leak reader rulings, harmless, one line each: SPS-04 naming column words is the organisation's own standard with
  purpose, scope, revision history, owner and approver; the compliance review ranks nothing and puts image
  interpretation outside its scope; the planning email sets the schedule and the three fields and ranks no team; the
  stump-vocabulary lines (SPS-04, the compliance review) name no familiarity, repeat image or first meeting, the
  review's "meetings" being team briefings.

## Tried and rejected

- The exposed or ambient population denominator, a crime rate per ambient person or per opportunity
  rather than per resident (2026-10-18, stage 1, measured): dead three ways over 40 neighbourhoods and
  a top-8 funded band. Ten ambient-population forms a competent analyst would use produce **5 distinct
  designation sets and 4 distinct rank-1 neighbourhoods**, and the graded rate for one fixed
  neighbourhood runs 116.81 to 373.42 per 1,000, a spread of **256.61 against 0.04 permitted** at a
  printed unit of 0.1, over by a factor of about 6,400. So the family is not closed and cannot be
  closed by discretising the answer, because the spread crosses the band boundary. The WHAT screen
  kills it independently: the denominator **is** the estimand's unit, so naming it ("per 1,000 ambient
  person-hours on 24/9/3 weights") makes the decisive step the execution of a filed clause, and leaving
  it unnamed ("relative to the population at risk") forks the main recommendation across those 5 sets,
  with no third position. And the swap test fails outright: "the rate per ambient person present at the
  hours the offences happen" reads identically as an infection rate per ambient person or as faults per
  machine-hour, so per-exposure rather than per-head is the most general move in quantitative science
  and the generating process has dropped out.
- The baseline fitted on a window that already contains the intervention, with the field's method an
  interrupted series fitted on a clean period and projected (2026-10-18, stage 1, measured): dead on
  the 1.2b pincer. A council files its own rollout dates in the committee report that authorised the
  spend, so excluding the implementation period follows from reading one shipped sentence, which is
  rule application. Unfiled, the record does not measure its own rollout window: profiling the
  implementation start over plus or minus 10 periods with level, trend and shift free leaves a set **3
  periods wide** within 2 log-likelihood units, so recovering it is an unstated rule (banned) or case
  three. Worth recording that the reflex sweep did **not** kill this one: 0 of 6 reflexes landed within
  2.0 of the true shift of -14.00 (the all-pre-period baseline filed -7.78, a last-12-months baseline
  +0.44, pre mean against post mean -0.96), so the mechanism had real separation and died purely on the
  pincer. Any future attempt on this shape needs an implementation window no document states and that
  the record measures about itself exactly, which this ground does not supply.
- Displacement and diffusion between adjacent units, with the field's method a net effect over a buffer
  ring rather than a per-unit count (2026-10-18, stage 1, measured): dead four ways. A single citywide
  displacement fraction gives net = gross x (1 - df), a positive monotone rescaling of every candidate,
  so **the ranking cannot change at any value of df** and the mechanism is worth nothing on the graded
  object. A per-scheme fraction is needed instead, and from a closed roster of 24 past schemes the
  fraction estimates at 0.436 with a standard error of 0.109 against a truth of 0.32, while the
  per-scheme spread is 0.522 against the **0.109 difference needed to reorder the leading two
  candidates**, so the lever is 4.8 times the estimator's own noise and the call is seed hostage. The
  WHAT screen kills it again, because "the net change across the whole city" against "the change in the
  funded area" is the estimand's comparison population. And the objective is wrong: a funding pick on a
  causal effect is served by `intervention-policing-policy-evaluation`, tagged EC, so the
  `Task type:` line would not pass `precut.py`.
- Journey-to-crime attribution, the count the decision defines being offences committed by residents of
  each neighbourhood rather than offences occurring in it, apportioned by the distance decay the
  detected offence-offender pairs measure (2026-10-18, stage 1, measured): dead on the WHAT screen,
  which is the shape that killed task190, task192 and task193 at stage 4 with every figure reproducing.
  The two bases are not two methods for one quantity, they are two different populations, and the
  measured designation sets share only **2 of 8 members** with rank 1 moving between them. Filing the
  basis makes the offender join follow from the clause; leaving it unfiled forks the call. This is the
  strongest candidate the cell has on the swap test (no other field has an offender choosing a target a
  short distance from home) and it still cannot be drawn, which is the clearest single statement of why
  the cell is closed rather than merely picked over.

### Second pass, supply-chain-logistics x multiple-testing-selective-inference (2026-10-18, six mechanisms dead over seven screens, every kill measured)

- The latent count of genuinely short units behind a screen, with a filed trigger count deciding a
  network-wide remedy (screen 1, measured): dead on the one-live-degree-of-freedom law. On a 54-pairing
  audit grid (audited consignments 29 to 3,864, median 354) with 12 pairings genuinely 4.5 points short,
  the six routes a competent analyst would use file **15, 8, 6, 6, 0.0 and 0.0** pairings and the truth
  of 12 sits sixth of seven on that one axis, so **no trigger threshold between 1 and 59 puts the golden
  on its own side of the call**: every rung shares its verdict with the decisive step. A correction is a
  move along one axis, which is the general form of this kill.
- The same latent count graded as a figure rather than a verdict (screen 2, measured): dead on the
  estimator family. Six Storey lambdas from 0.3 to 0.8 all return **0.0** non-null pairings while
  central matching on the same statistics returns **27.6**, a family spread of **27.6 pairings against a
  printed unit of 1 and 0.4 permitted**, over by about seventy times. Nothing in a records pack closes
  the family, and filing the estimator files the method.
- Certification under a simultaneous bound, the audit covering every pairing whose own evidence does not
  rule out a material shortfall (screen 3, measured): dead on nesting. The slates are
  **8, 22, 27 and 27** pairings for the naive flag set, the per-pairing 95 per cent bound, the Sidak
  simultaneous bound and the Bonferroni simultaneous bound, and containment is **total at every step
  (8/8, 22/22, 27/27)**, so every rung is the same statistic at another level and the decisive rung adds
  no reordering at all. The level is a convention besides, so the pincer closes it independently.
- Dense and weak evidence combined across a unit's whole measured family rather than corrected within it
  (screen 4, measured): dead on the reflex sweep and on readability. With 40 of 54 pairings 1.2 points
  short, Bonferroni finds 5 and Benjamini-Hochberg 7, but **the pooling reflex lands the conclusion
  outright: the audit-wide rate is 94.49 per cent against an agreed 95.0, z = 4.6**, and the hygiene
  battery lands it too (Kolmogorov-Smirnov of the 54 p-values against uniform, **p = 3.45e-03**).
  A determinism objection stands behind both: a Bonferroni test of the global null is a valid test at
  the stated level, so "not established" is defensible and the fork is a competing defensible answer.
- The slate of k under a filed materiality, ranked by the chance a pairing is materially short rather
  than by its measured shortfall (screens 5 and 7, measured): dead twice over. First, the decisive step
  is **worth nothing on the graded slate**: all six corrected routes name the identical slate
  (1, 12, 36), so plain significance against the agreed level already lands it and the materiality
  construction, the lower bound, the empirical-Bayes posterior mean, the posterior probability and the
  likelihood ratio at a point mass add no reordering whatever. Only the crude ranking by measured
  shortfall differs, at (36, 40, 44), which makes the whole mechanism one rung rather than a ladder.
  Second, that agreement is a single draw's luck: over 20 redraws **the golden's own family returns 2.05
  distinct slates of 4 (min 1, max 3)**, so the designation is not determinate either (screen 7).
- The confirming review that re-reads the weeks which triggered it, read conditional on the trigger
  (screen 6, measured): dead on the single dial. Across overlap shares 0.15 to 1.00 the bias removed
  rises 0.185 to 0.461 points while the corrected estimator's standard error rises 0.302 to infinity, so
  **the lever over its own noise never clears 1 (0.61, 0.78, 0.80, 0.81, 0.60, 0.00)** and the corrected
  estimate is **worse than doing nothing above half overlap** (mean absolute error 0.409 against 0.402 at
  0.69, and 0.554 against 0.434 at 0.85). The overlap share that creates the bias is the share that
  removes the evidence, one dial at both ends.
- **The designation determinacy screen (`stumping` 1.2, sixth screen), run on both candidates whose
  graded object is a set, counted on the golden's own estimator family over 20 redraws** (screen 7,
  measured): both fail, and they fail on opposite halves of the screen, which is what makes the cell's
  shape clear. The audit slate under a simultaneous bound returns **2.90 distinct designated sets of 6
  forms per redraw (min 2, max 3)** across two simultaneous levels and three interval bases, so the call
  is not determinate; and the crude route lands inside that family in **0 of 20** redraws, so the
  mechanism is not crude-reachable, only indeterminate. The slate of three under a filed materiality
  returns **2.05 distinct slates of 4 per redraw**, and the crude ranking lands inside the golden family
  in **2 of 20**, so it fails both halves. Neither can be rescued by discretising against a filed
  tolerance, because the family's spread is what crosses the line: the sets differ by which pairings sit
  at the boundary, not by a figure a band could absorb.

**What the sixth screen settles, and it is the positive statement this ground owes.** The screen's own
shape, a quantity whose construction the data forces with the designation following from it rather than
being the graded object, is exactly the reference-or-statistic row of the table above. On this task type
those two slots are the whole of what is data-forced, and task191 holds the reference while task195 holds
the statistic. So a build here must grade the designation itself, and the sixth screen measures that as
either indeterminate (2.90 and 2.05 distinct answers) or crude-reachable. That is the cell's closure
stated from the client's side rather than ours, and it is why no seventh candidate was screened.

**One defect in the harness, found and repaired, because it moved a measured result.** The first pass of
screens 3, 5 and 7 took each pairing's standard error from the Wald formula, which is exactly zero where
a pairing's audited consignments are all compliant, so a perfect pairing took an infinite z and captured
a ranking. The harness now uses the Agresti-Coull (add-two) standard error, which cannot degenerate.
Repairing it moved the per-pairing bound's slate from 19 to 22 pairings and, in screen 5, moved the
material-aware routes from two slates to one, which strengthened that kill rather than weakening it.
Screens 1, 2, 4 and 6 are unchanged. The seven-screen harness reproduces byte-identically run to run,
stderr included (6,913 bytes).

### Third pass, biomedical-clinical-research x genomics-gwas-high-dimensional-association (2026-10-18, one architecture measured dead, eleven directions closed, nothing cut)

- The 2027 confirmation capacity split across seven programmes in proportion to the samples their
  nominated loci need at a fixed relative precision, sized on the effect each locus is expected to show
  in that wave rather than on the discovery estimate that nominated it, the client's own rigor pattern 2
  for this task type (2026-10-18, stage 1, measured): dead four ways on the graded split. The correction
  family (conditional maximum likelihood under the selection, the truncation-hazard correction, empirical
  Bayes with a fitted normal prior, Tweedie shrinkage off the scan's own z density, a parametric
  bootstrap) spreads the split by **565 slots of 36,000** against the **101 slots** the decisive step
  moves it by, mean 472 against 79 over 20 redraws. The dial that buys the lever spends the family: across
  a sevenfold sweep of the weak programmes' discovery size the ratio runs **0.007, 0.150, 0.007, 0.151,
  0.163, 0.159, 0.192** and never reaches 1, with the family spread blowing out to 9,345 slots at the
  settings where the conditional likelihood touches the line. The step **reorders nothing**: the decisive
  and naive routes return one identical ordering of the seven programmes over 20 redraws, because a
  selection correction is monotone in the discovery statistic and a share normalises it away.
  `corr(decisive measure, programme discovery size)` is **+0.962**, against the +0.98 that killed task57.
  And the designation half fails from the other side: the family names one largest-share programme in
  20 of 20 redraws, but so do the crude and naive routes, so discretising removes the indeterminacy and
  the lever together.
- The summed squared standard errors taken out of each bucket's summed squared effect estimates, so the
  split follows the signal part of the observed signal mass (2026-10-18, stage 1, killed on the
  abstraction test and then measured): this is task246's live driver in other nouns, a nuisance variance
  out of an observed dispersion, with task237 holding a second instance of the same axis triple. Measured
  besides: it lands **within 115 slots of 36,000** of the selection correction above, so the two are not
  separable on this ground. Structural rather than incidental, because for a selected locus the
  sampling-variance bias and the selection bias are both of order one over the squared discovery
  statistic, so no tuning makes one large while the other is negligible.
- The shared control panel, one set of controls reused across several disease studies so the studies'
  effect estimates covary and the meta-analysis overstates its own evidence (2026-10-18, stage 1, killed
  on the abstraction test): task195's driver, shared units making two estimates dependent, which is the
  driver this cell was told to draw away from. The overlap counts would have been stated plainly, so the
  inference rather than the reading would have decided, and it is still the same insight.
- Separating confounding inflation from polygenic signal by regressing chi-square on a linkage covariate
  (2026-10-18, stage 1, closed by `guard.py slots` before any screen): task201 v1a killed it at that
  slot's draw on this same cell, with the two-log-likelihood set 0.0204 wide against a printed precision
  of 0.01. Not re-screened. `stumping` Part 3 closes the family by construction. The cost of finding this
  by slot search rather than by screening is one pass, which is what the tool is for.
- Imputation quality used as a weight rather than as a filter, so a panel of rare and hard-to-impute
  variants keeps its contribution instead of losing it to the conventional information cut (2026-10-18,
  stage 1, paper, the 1.2b pincer): the standard practice is to filter, so a filed sentence telling the
  solver to weight makes the step rule application, and with nothing filed the filter route is defensible
  standard practice and the call forks. Naming the population ("over every variant on the panel") closes
  the fork by filing the estimand, at which point reading the estimand performs the step. No third
  position.
- The exact conditional null at low minor allele count under case-control imbalance, so a bucket's
  apparent excess is mostly the asymptotic approximation failing in the tail (2026-10-18, stage 1, paper):
  dead twice. It bites only through a count of variants past a line, and a filed significance level is a
  filed method wherever the decisive step is an inference; and the swap test fails, because an exact test
  in place of a chi-square at small counts reads the same in any field with sparse tables, so the
  generating process drops out.
- Expected confirmation averaged over the discovery estimate's own uncertainty rather than evaluated at
  the point estimate, whose error changes sign across the curve's inflection (2026-10-18, stage 1, paper):
  task187's driver, a capped curved response averaged over a spread whose width depends on the unit. It
  also needs a confirmation criterion, which is a filed test.
- The allele frequency transported to the next wave's own population, so a bucket whose variants are
  common in the discovery cohort and rare in the new catchment contributes less (2026-10-18, stage 1,
  paper): the flip comes from using the other frequency column, which is data semantics.
- Differential call rate across the compared groups, so part of a bucket's apparent signal is produced by
  which genotypes failed to call (2026-10-18, stage 1, paper): a data defect, so cleaning the data makes
  the call easy and the stump would sit in Layer 1, and the correction is the enumerated reflex "add a
  control".
- The bucket's whole signal mass against the count of its members crossing the line, so a bucket of many
  small real effects beats a bucket with one large hit (2026-10-18, stage 1, closed on this slot's own
  third-ground screen 4): this is the pooling reflex, which that screen measured landing the conclusion
  outright at z = 4.60, with the hygiene battery landing it too.
- The expected number of genuinely associated loci per bucket (2026-10-18, stage 1, closed on this slot's
  own third-ground screen 2): the latent-count estimator family, measured there at six Storey lambdas all
  returning 0.0 against central matching's 27.6, a spread of seventy times the printed unit, and nothing
  in a records pack closes the family.

### Fourth pass, general-statistics-data-science x exploratory-data-analysis-distribution-assessment (2026-10-20, architecture 2: three candidates dead, one measured, nothing cut)

- The share of one melting line's boards below a per-board thickness limit, recovered by solving the blend
  identity across the shift production log's varying tonnage split, where the in-line gauge sits after the
  two lines merge and no reading carries a line (2026-10-20, stage 1, measured): dead on contract screen 2,
  and dead by algebra rather than by a magnitude. The mixture identity is affine in the forcing file's own
  published share column, so one regression of the shift's below-limit share on that column, read at a share
  of 1.0, **is** the designed estimator: measured over 20 world draws its mean absolute error is **0.0026
  against the designed construction's 0.0028**, its worst **0.0083 against 0.0098**,
  `corr(one-line, designed) = +0.9582`, the two agree on the verdict **20 of 20** and differ by at most
  **3.29 printed units of 0.001**. The designed route's own estimator family fails closure besides, five
  defensible forms spreading the graded figure **0.00308 mean and 0.00791 max against 0.00040 permitted**,
  over by 7.7 and 19.8 times. Screens 1, 3, 8, 10 and 11 all passed, which is why the algebra is the finding:
  screen 1 passes because the correcting input is one share per shift identified in 36 of 36 periods, screen
  3 because the attaining subset (the shift closest to pure covered-line running) lands the golden verdict
  only 15 of 20 at a mean absolute error of 0.0370, screen 8 because the graded object is a population tail
  share rather than a level at a selected unit, screen 10 because the correction leaves no part of the record
  alone, screen 11 because the construction produces the graded statistic rather than a benchmark.
- A record of per-window **maxima** (a peak-hold instrument or a max-aggregating historian tag) inverted
  through `G(x) = F(x)^k` with the window's opportunity count from an operations file at another grain
  (2026-10-20, stage 1, paper): dead on a pincer that closes the family. Nothing in a record of maxima
  measures that it is a record of maxima, so either the pack documents the transformation and the
  documenting sentence is a clause the solver cannot avoid reading, which makes the decisive rung readable
  on `stumping` 2.1 test 1, or it does not and the construction is unavailable, which is 1.2b case three. No
  third position. **The general form: a decisive step that inverts a documented transformation of the
  recorded values cannot be silent, because the document that makes it available is the signpost.**
- A record of per-group **medians** (a gauge storing the median of each group of k consecutive items, k
  varying by line and period from the configuration register) inverted non-parametrically by solving the
  mixture-of-order-statistics equation at the limit (2026-10-20, stage 1, killed on card text before a world
  existed): this is **task202's driver** in other nouns. Stripped of nouns, task202 reads "the only
  item-level figure the record states is each unit's own average over its items, so every upper cut comes out
  far too low", which is the first clause of this candidate exactly. The corrections differ (task202
  transports a measured within-group shape from a reporting minority; this inverts an order statistic with no
  corpus), so two of the abstraction test's three clauses map rather than three, and the line that fails is
  `Lesson:`, since a model that learns this has already learned task202's. The second death above would have
  killed it independently.

### Fifth pass, architecture 3: the blessed shape itself priced and refused (2026-10-23)

Ground: the lane's allocation was read from `guard.py` rather than from a table. `recent` puts the live
three-build window at task273 (`population_selection`), task169 (`decomposition_attribution`) and task478
(`other`), so **no anomaly-detection subdomain is inside it** and `ban.subdomain` blocks no AD cell; what
binds a redraw is the driver, exactly as `coverage` states. `mechanisms --objective anomaly-detection`
prints 34 builds, and the per-case correction families they spend are the whole of the list a candidate
would reach for: exposure or at-risk time (task54, task201), size or length bias (task182), detection or
ascertainment (task180, task196, task199), opportunity count (task181), orderings and position (task193),
measurement basis (task185, task189, task192), shared-cause share (task103), record lag (task194), state
dependence (task183), per-group summary (task202), grouped tests (task188), interval censoring (task184).
Cell taken for the screens: `epidemiology-public-health` / `disease-surveillance-outbreak-anomaly-detection`
(one card, task188), chosen because the forcing-file inversion is clean there and the spent driver is a
single one. Nothing was cut and no card was filed.

**What this pass priced is not three candidates but the SHAPE `stumping` Part 3 step three blesses**, and
the four deaths below are one finding: the shape is closed as a family on this objective for a
multiplicative per-case correction. Harness `scratchpad/w8_200/screen_a3.py`, run with `python3 -I`, two
consecutive runs byte-identical at 8,186 bytes with stderr included, every number on the clean truth with
the correcting factor and the base quantity drawn from ONE generating process.

- The multiplicative-correction floor, validated on this harness before it was used: at rho 0.20, 0.48,
  0.80 and 1.00 the floor runs 0.9798, 0.8773, 0.6000 and 0.0000 and the reflex takes the top candidate
  0.778, 0.505, 0.230 and 0.023 of the time, reproducing the filed law.
- **The aggregation theorem, and it is the pass's first general finding** (2026-10-23, measured): in the
  blessed shape the correction is one per CASE while the decision is per CANDIDATE, so the candidate-level
  factor is an average and `sd(log factor)` falls as one over the square root of the case count. With a
  per-case correction of log sd 1.00 against a base of log sd 0.35, candidate-level rho measures 1.8808,
  1.1282, 0.6826, 0.3779 and 0.2224 at 3, 10, 30, 100 and 300 cases per candidate, so rho clears 0.80 only
  below about 13 cases per candidate. **Both horns are deaths.** At 13 cases the estimator's own relative
  standard error is 0.2774 against an across-candidate signal log sd of 0.35, which is 0.79 of the whole
  spread, so the ranking is seed hostage exactly where the correction clears the floor; and the only other
  way to carry rho is a systematic candidate-level mix term (rho stays above 1.50 at every case count with
  a mix of log sd 0.50), which is a stratification of the finer file and so one group-by.
- C1, ascertainment one per case (each notified case standing for `1/d` with `d` built per case from the
  specimen register's own specimen-taken, test-used and onset-to-collection-delay structure), 20 world
  draws, posture coupling both arms: **clears both floor tests and dies on the proxy screen and the
  abstraction test.** rho 1.0506 so no floor binds it, realised `corr(log true, log reflex) = +0.1183` and
  the reflex names the top in 2 of 20, which is a real separation; but the one-group-by route, the notified
  count divided by the facility's own mean ascertainment, matches the designed Horvitz-Thompson
  construction at **corr +0.9881**, names the top in **14 of 20 against the designed route's 14 of 20**,
  and does it at a **smaller** mean absolute error (0.001050 against 0.001146). That is architecture 2's
  death in another skin. It is also task199's live driver (a rate read against the observation effort that
  produced it) with task196 and task180 beside it, so the `Lesson:` line fails anyway.
- C2, a per-case denominator from the roster (each case's own wing roll on the day of onset), coupled
  through facility size: **dead on the floor and on the algebra.** rho 0.6362 against a floor of 0.7716,
  realised corr +0.8884, and the ladder is inverted, the reflex naming the top in **12 of 20 against the
  designed route's 1 of 20**. Screen 3 as algebra says why with certainty: `roll = S/wings * eps`, so the
  designed sum is `reflex * wings * E[1/eps]`, **affine in the roster's own published wing count**, and one
  join and one multiply by that column is the construction.
- C3, a gate non-linear in the rows (the days on which concurrently symptomatic residents exceed the
  facility's own single-room count, from the register's onset and clearance dates): **outside the floor law
  and dead three ways.** The raw count is genuinely weak, `corr = +0.4774` and the top in 7 of 20, but the
  cheap routes are not: Little's law over rooms reaches **+0.9486 and 16 of 20** and the count per room
  **+0.9475 and 18 of 20**, one divide by a column of the room register. The standing family is worse: five
  defensible readings of "concurrently symptomatic" (register onset to clearance, a fixed 48-hour
  infectious period, specimen date to clearance, both endpoint days counted, clearance at the next negative
  specimen) give **1.90 distinct top facilities per draw (min 1, max 4)** and spread the graded figure
  **24.38 days on average and 52 days at worst against a printed unit of 1 day**. Screen 4 counted jointly
  over 72 cells of burstiness by single-room share: 21 cells where the cheap route misses, 20 where the
  family is unanimous, 42 where the margin clears 1.15x, and **2 passing all three at once**.
- C4, **the corrected shape itself** (the per-case quantity UNOBSERVED and recovered with no free
  parameter), priced on its own dial because that is the question the correction leaves open: **the
  no-free-parameter clause fixes the determinacy screen and does not touch the proxy screen.** Whatever
  recovers the per-case values, the cheap route is the main file's count divided by the finer file's
  group-by mean of the correction, and the two constructions have the same expectation, so they separate
  only through the correction's WITHIN-candidate dispersion (Jensen, `E[1/d]` against `1/E[d]`). That same
  dispersion is what gives `1/d` its heavy tail, so the lever and the noise are one number and the dial
  fails at both ends: as `sd(log d)` runs 0.20, 0.50, 0.90, 1.40 the designed-against-cheap correlation
  runs **+0.9999, +0.9974, +0.9815, +0.9396** while the designed route's hit rate **falls 15, 14, 13, 10 of
  20** and the cheap route's **rises 15, 14, 15, 16 of 20**. Swept jointly over dispersion by coupling by
  case volume, **45 cells: 14 where the cheap route misses, 0 where the designed route holds at 19 of 20,
  and 0 passing cheap-misses with designed-holds and raw-misses together.**

**The law this pass earns, and it is general rather than about this cell.** For a per-case correction that
enters MULTIPLICATIVELY, the cheap route is the count divided by the finer file's own group-by mean of the
correction; that route shares the designed construction's expectation, so the two can only separate through
the correction's within-candidate dispersion, and that dispersion is the designed estimator's own variance.
So the blessed shape's multiplicative case is closed by arithmetic: the floor law closes it from above
(rho under 0.80 cannot reorder) and this closes it from below (rho over 0.80 needs either 13 cases per
candidate, which is seed hostage, or a candidate-level mix term, which is one group-by). **The one opening
left is a per-case correction that does NOT enter multiplicatively, and a non-multiplicative per-case
correction is non-linear in the forcing quantity, which reopens the free exponent the fleet wear-life death
measured at 2.55 distinct designated units of 5.** That is the next pass's one computation.

**Two directions closed from the record rather than by a screen, which cost one read each.** The fourth
pass left "a construction over **orderings** rather than over values" as the one unpriced direction; it is
**task193's live driver** on this objective (how many units would show one of two orderings if the
treatment had no bearing on it, each unit's room for each ordering set by where its first exposure falls),
and `strategies.md` Part 6 records it measured dead there: an ordering expectation over a window against a
level comparator is `n` times the window's end less the other side's mean date, over the window's length,
an identity, so the decisive construction is one group-by, one subtraction and one divide, which referred
the committed set 20 of 20 at corr +0.9954, and a blind reader at medium effort landed the call. So the
direction is both occupied and dead, and no harness was spent on it. And the records-fixed half of
`stumping` 1.2a, the half that needs the records to force a selection, is `population_selection`, which
`ban.strategy` BLOCKs against task273 in the live window; differentiation never clears an axis ban, so that
half is shut this sitting and open again three builds later.

- **Architecture 4 opens on the propagation family, 2026-10-23, and this bullet is written before the first
  harness so the plan is on record with its predicted failure modes.** The closed family is not re-entered: the
  "correcting quantity one per case from a second file at a finer grain" clause is shut as a clause and all six of
  its laws (the floor, the averaging-out, the pincer, the dispersion ceiling, the geometric mean, the
  cheapest-licensed-member) are taken as given. The ground drawn instead is the one task125 shipped on today: a
  change acts on a unit that is NOT the unit the data is reported at, and propagates through a structure the
  organisation's own process imposes, so each reported period is a mixture of regimes whose proportions move.
  **The family's binding screen is not separation and not the floor law; it is the abstraction test against
  task125**, whose own driver is the rotating-panel member of this family, so a candidate must differ in the
  LATENT STRUCTURE and in the CORRECTION, since the default path ("attribute the effect to the reporting unit")
  is shared by every member of the family by construction and therefore cannot differentiate anything.
- **Two members of the family killed structurally before any harness, each for one line's reason.**
  - **The queue's duration-selection member** (the change acts at entry, the statistic is measured on leavers, and
    the first post-change leavers are the fast ones) is the common-exposure subset screen's time-axis form, which
    `stumping` 1.2 measures dead: "use the entry cohorts old enough to be complete" is a filter and a divide with
    no model, reaching the truth 14 of 20, and the record's own completion date, one group-by and one divide,
    reaching 20 of 20. It is also `maturity_censoring`, which task194 holds as its live driver on this objective
    and task201 and task171 carry beside it.
  - **The staggered-conversion member whose conversion ORDER carries the selection** (a cycle brings the highest
    units through first, so the aggregate overshoots and comes back) dies on readability tests 2 and 3 together:
    the cycle's order is a risk band or a due date, both columns, so "stratify on the visible attribute and
    reweight" is the opponent's first reflex and it reaches the mixture directly. The member survives only where
    the affected unit's identity is NOT a column, which is the property task125 had to build (no field marks a
    later-wave record as recruited under the cap).
- **The one shape in the family whose CORRECTION differs from task125's, and the pass's lead candidate: a
  re-phasing.** Where the change moves WHEN a unit's recorded quantity falls rather than how large it is, the
  operator preserves each case's total and moves it across reporting periods, so the graded path sums to
  approximately zero over one full cycle and reverses sign partway through. task125's correction propagates a
  LEVEL gap through a fixed run and is one-signed in every period of that run. Predicted failure mode, to be
  priced first: the counterfactual schedule is exact arithmetic on recorded fields, so the `Not rule
  application:` line is argued from the unit-of-analysis carve-out rather than measured, exactly as task125's own
  note records of itself; and the determinacy screen passes trivially for the same reason (task125 measured 3e-06
  point of spread across six licensed variants), so this family trades the horn C3 died on for the horn task125
  survived by carve-out.

- **The not-a-per-case-correction test, written out and MEASURED as a discriminator rather than asserted.**
  The closed family's operator acts inside a case and scales its value, so the graded quantity is
  `sum_c obs_c (1 - 1/d_c)` and every reported period moves the SAME way; the propagation family's operator
  preserves each case's total and moves it across reporting periods. Two statistics separate them exactly:
  `R = sum_q |G(q)| / |sum_q G(q)|` over one full cycle, and the number of sign changes in the graded path.
  Measured on one world, with a genuine per-case correction built on the SAME rows as the control:
  the per-case correction returns **R = 1.000 and 0 sign changes at sd(log d) of 0.35, 1.00 and 2.00**
  (G/obs stays inside -0.073 to -0.053, -0.674 to -0.581 and -6.971 to -5.079 respectively, never crossing
  zero), while the re-phasing candidate returns **R = 4.393 with 1 sign change and G/obs running -0.0546 to
  +0.1072**. So R equal to 1 is an identity for the closed family rather than a tendency, and any candidate
  measuring R = 1 with no sign change IS a per-case correction in other nouns whatever its nouns are. **This
  test belongs in the next pass's first ten lines of code**, before any separation or determinacy work: it
  costs one aggregation and it is exact.
- **C5, the re-phasing member (a 30-day to 90-day fill-size change applied at each member's own prescription
  renewal, graded as the published spend per member per month in each reported period): separates strongly and
  dies on DETERMINACY, measured, which is C3's horn in new nouns.** Separation is real and every reflex lands
  wrong in a different direction, golden path per quarter from 2026Q1 **+0.00, +0.04, +11.40, +13.17, +0.52,
  -3.72, -5.80, -6.29 USD PMPM** against the "change acts on the period" route's constant **0.00** (max error
  13.17), the "apply it where it is visibly in force" route's **-0.00, -0.00, -1.30, -2.96, -6.17, -6.85,
  -6.94, -6.98** (max error 16.13, and the WRONG SIGN in the two roll-in quarters), the carried-forward route's
  constant **+11.40** (max error 17.69) and the cross-sectional 90-day-against-30-day route's **+28.94,
  +46.78, +48.78, +33.46, +113.73, +115.16** (max error 121.44). The kill: the counterfactual has to project
  each member's own refill CADENCE across the whole graded window, and four licensed readings of that cadence
  (the benefit's own 30 days; the member's own observed median interval; the member's own realised interval
  sequence; the plan-wide median interval) spread the graded figure a **mean of 13.32 and a maximum of 40.52
  USD PMPM against a printed unit of one cent**, about 1,330 times the printed unit on average and 13 times
  even at a printed unit of one dollar. **The window-length dial does not open it:** spread over mean absolute
  golden runs **294.7 at 2 periods, 1.790 at 4, 2.219 at 6, 1.730 at 8, 1.718 at 10 and 1.789 at 12**, so the
  licensed family is about twice the signal it has to carry at every window length, because a one-day
  difference in a licensed cadence compounds linearly in the window while the signal does not.
- **The law the C5 kill earns, and it is about the family rather than about pharmacy.** A counterfactual over
  a propagation structure is exactly one of two kinds. **K1, a re-selection or reweighting of RECORDED rows**
  (task125: drop the capped-out households from a pre-change quarter and re-rake), which is exact arithmetic,
  so the licensed family's spread is essentially zero (task125 measured 3e-06 point across six variants) and
  the `Not rule application:` line has to be argued from the unit-of-analysis carve-out. **K2, a re-timing or
  re-generation of events that were NEVER recorded**, which needs a behavioural quantity projected over the
  window, so the family spread compounds in the window length and the determinacy screen fires. The two are
  exhaustive: either the counterfactual's rows sit in the record as rows belonging to other units or other
  positions of the structure, or they do not exist and must be generated. **So price which kind a candidate is
  before anything else; K2 is closed by this measurement and K1 is where the family's one shipped build sits.**

- **C6, the structure-length member (the term of the structure itself shortens, here a 12-month
  prior-authorisation term cut to 6 at each authorisation's next renewal, graded as discontinuations per 1,000
  on therapy per quarter): dead twice over, and its first death is the useful one.** By the S1 test it carries
  **the closed family's own signature, R = 1.000 with 0 sign changes**, because shortening the structure's term
  can only add review opportunities, so every reported period moves the same way and the graded path is a
  per-unit level correction propagated through a calendar: the six closed laws therefore apply to it and the
  orchestrator's point 1 is answered by measurement rather than by argument. It also dies on determinacy on its
  own account: the counterfactual needs a drop-off outcome for reviews that never happened, and the five
  licensed hazard forms an analyst would estimate off the pre-change record (pooled, by class, by duration band,
  class by duration, a logistic fit on duration) spread the graded path a **mean of 11.33 and a maximum of
  33.24 per 1,000 against a printed unit of 0.1**, about 113 times the printed unit and **4.293 times the mean
  absolute truth**, with the pooled and by-class forms printing the wrong SIGN in eight periods of ten.
- **K1, the determinate kind, priced for a FRESH draw rather than taken on task125's result, and it is held by
  its own two pack conditions rather than by the family.** Prototype: units enter in cohorts, each cohort
  occupies five consecutive reported periods, a change at entry removes a class whose outcome gap decays with
  position, everything drawn from one process (a cohort's season drives its size, its affected share and the
  gap together).
  - **A, the rebuild period is a licensed choice and it is NOT free.** Rebuilding the removed class's position
    profile on each of the five pre-change cohorts spreads the graded path a **mean of 0.1038 and a maximum of
    0.1582 index points against a printed unit of 0.01**, 10 to 16 times the printed unit and **0.287 of the
    mean absolute truth**. task125 drove that to nothing with its SF4 row by showing exactly one quarter
    qualifies (every earlier uncapped quarter is missing visit histories for 15 per cent or more of the sample
    and every later quarter is itself capped). That is a property of task125's own pack, not of the family, so a
    fresh K1 draw has to reproduce the same condition.
  - **B, the generic data condition hands over the route.** With the affected class flagged at every position,
    which is what most structures do (a priority class, a scheme code, a tariff flag rides on every row), the
    one-group-by route (group by flag and position over recorded rows, add back) lands the golden path at
    **maximum absolute difference 0.0337 index points and corr +0.9979**. So K1 is drawable only where no column
    marks an affected unit at the later positions of the structure, which is again task125's own stated
    condition ("no column marks a later-wave record as recruited under the cap").
  - **C, K1's graded path carries R = 1.000 and 0 sign changes**, the closed family's signature, like C6.
- **The law the three candidates jointly earn, and it is the pass's main result: in the propagation family,
  R = 1 and determinacy are the same end of one dial.** A one-signed graded path (R = 1) means the correction is
  a per-unit LEVEL correction propagated through the structure, whose counterfactual is a re-selection of
  recorded rows: determinate, and carrying the closed family's own signature, so the six laws bind it. A graded
  path that changes sign (R greater than 1) means the counterfactual has to re-time or re-generate events that
  were never recorded, so its licensed family's spread compounds in the graded window and the determinacy
  screen fires. Measured at both ends in one pass: C5 **R 4.393** with a family spread of **1.7 to 2.2 times**
  the signal at every window length from 2 to 12 periods; C6 **R 1.000** with a spread of **4.293 times**; K1
  **R 1.000** with a spread of **0.287 times** and the cheap route at **corr +0.9979** once the affected class
  is flagged. The one unpriced cell of that dial is a path that changes sign while its counterfactual stays a
  re-selection of recorded rows, which needs the selected class's gap to reverse sign with position; that is
  the next measurement and it is priced below.
- **Two further members closed by arithmetic rather than by a screen, because each costs one line.**
  - **Removal and addition are not symmetric, and only removal forces the reasoning.** A change that ADDS units
    at entry leaves the counterfactual directly recorded, because the added units and all their later rows are
    in the pack with their own identifiers, so the counterfactual is a filter on two recorded columns and
    nothing is left to decide: rule application with no unit-of-analysis carve-out. A change that REMOVES units
    leaves the counterfactual absent from the post-change record, which is exactly what forces the analyst to
    ask at which positions of the structure the removed class would have sat and to rebuild on a period that
    observes it at every one. So the family's forcing configuration is removal, and task125 holds it.
  - **The no-counterfactual variant of the family is Forecasting and not this lane.** Grading the forward value
    of the published series itself needs no counterfactual, so the K1-versus-K2 pincer does not bite it at all,
    and the structure's own calendar pins each future period's mixture. But a predicted value the history pins
    is Forecasting by `guide-to-prompt`'s own tag rule, and separating a real event from an artifact on
    anomaly-detection IS a counterfactual comparison, so on this objective the family must grade a
    counterfactual and the pincer is binding. The family's live member sits on another objective.

- **The propagation shape is withdrawn as a driver mid-pass by the orchestrator, and this slot's own
  measurement had reached the same wall from the other side, independently and before the correction arrived.**
  The sibling's kill is that the cheapest licensed route IS the golden (one join to the register, one two-way
  group-by on regime by position, one reweight, RMSE 0.0072 and max 0.0170, 2.8 and 3.3 per cent of its own
  level) and that this is structural by a LINKAGE TRICHOTOMY: the mixture weights must be shipped for the path
  to be computable and the position variable ships with them, so a row carries its cohort directly (one
  group-by), or carries a key a register maps (one join plus one group-by, the same cost), or carries nothing
  identifying the unit, in which case the profile is recoverable only from the published series, which is the
  quantity in question (a cubic trend with seasonal terms reproduces 90.5 per cent of the distortion path's
  variance). **Measurement B above is the same finding reached from this slot's own prototype**: with the
  affected class flagged at every position, the one-group-by route lands the golden path at corr **+0.9979** and
  max absolute difference **0.0337 index points**, so the two passes agree that the family's cheap route is its
  golden wherever the position is linkable. The guard refuses it besides, BLOCK on `test.same_puzzle_older` and
  `test.same_driver_older` against task125 (v2) with `driver.near` 0.19, and task125's own `Lesson:` line states
  the generalisation verbatim, so no differentiation line can be written honestly. **Nothing in the propagation
  family is taken to a card by this pass.** The measurements above stand as the family's closure from this
  slot's side and are not to be re-screened: C5 on determinacy, C6 on determinacy and on the closed signature,
  K1 on the rebuild-period family and the flagged-position cheap route, plus the removal-versus-addition
  asymmetry and the Forecasting-only no-counterfactual variant.
- **The turning-point direction is refused without a harness, for one line's reason.** Grading the path's
  turning point instead of its levels changes the graded object and not the driver, and the orchestrator's own
  note concedes it "remains task125's driver unless the propagation is not task125's". A level-dependent
  discrete object on this lane is also proven ground rather than new (task164 and task263 grade a
  level-dependent threshold count), and this slot's architecture 3 already measured the nearest discrete
  crossing object dead on determinacy at 24.38 days against a printed unit of one day. Two reasons, no screen
  spent.

- **C8, the UNREGISTERED-POSITION member, the one direction the orchestrator left open: priced and dead on
  both predicted horns at once, so the lane's standing law on per-unit quantities holds here too.** Prototype:
  220 units in a staggered 16-period cycle, each unit's event rate falling at its cycle event and deteriorating
  after it, a programme change narrowing the work done at the cycle events in one window, no register and no
  cohort column, so each unit's position and regime have to be recovered from that unit's own count history.
  - **The per-unit position estimator is hopeless at any realistic event volume.** Five licensed change-point
    estimators (the smoothed-rate minimum, the running-maximum drop, a CUSUM, a Poisson profile likelihood, a
    two-sided t scan) recover the unit's phase with a **mean error of 2.84, 3.04, 3.92, 5.23 and 5.26 periods
    out of a 16-period cycle**, get the position cell right **8.6, 8.2, 15.5, 1.4 and 0.0 per cent** of the
    time, and get the REGIME cell right only **84.6, 84.5, 77.9, 72.3 and 70.5 per cent**, so 15 to 30 per cent
    of the mixture is assigned to the wrong regime before any arithmetic.
  - **The parametric horn fires on the graded path.** The five estimators spread the path a **mean of 0.0528
    and a maximum of 0.2343 events per unit per period against a printed unit of 0.001**, which is **1.439
    times the mean absolute truth** and 234 times the printed unit, with the cusum and t-scan routes printing
    the wrong SIGN in several periods.
  - **And the construction fails even WITH the register, which is the second horn and the more interesting
    one.** Given the exact position and regime for every cell, the same construction still misses the truth at
    **RMSE 0.0265, which is 72.3 per cent of the mean absolute truth**, because the position profile is itself
    estimated from the units' own counts. So the decisive step's own standard error is of the order of the
    whole quantity it must print, and no pack of this event volume closes it: this is `stumping` Part 3's rule
    that a quantity estimated per unit from that unit's own thin slice cannot carry a ladder.
  - C8's truth also carries **R = 1.000 and 0 sign changes**, the closed family's signature, like C6 and K1.
- **The running-sum crossing object, this lane's one measured non-multiplicative shape, is closed by a
  trichotomy that costs no harness, and recording it is the point of this bullet.** Architecture 3's C3 died
  because five licensed readings of its increment spread the graded figure 24.38 days against a printed unit of
  one day; the standing hope was that a running sum with DETERMINATE increments would open the object. It does
  not, because the increments have exactly three states. **Definitionally open** (what counts as one increment
  is a licensed reading): C3's death, and the nearest other measurement on file at 1.57 distinct months.
  **Recorded and exact** (a recorded currency amount, a count with one unambiguous definition): the crossing
  date is then exact arithmetic over shipped columns, which is rule application and a one-line cumulative sum.
  **Not yet recorded** (the increments lie in the forward window): the crossing date is a predicted value the
  history pins, which is Forecasting by `guide-to-prompt`'s tag rule and not this number's objective. The two
  variants that look like a fourth case collapse into the first: increments recorded but incomplete puts the
  completion's estimator family back in the deciding position, and a crossing LEVEL that is unobserved puts the
  level's estimator family there instead, while a filed level is rule application. **So the running-sum
  crossing object is closed on this objective, and architecture 3's C3 was not an unlucky instance of an open
  shape but the only state of it that is not rule application or another lane's objective.**

- **Reconciliation with task194, which priced the same family in the same hours, and the one place this pass
  sharpens it.** task194's note decomposes the graded path as `P(t) = sum_c w(c,t) * delta(t - c) * 1[c >= T]`
  and concludes the shape is not in the closed family because the correction is ADDITIVE in cohort-position
  cells, there is no per-case factor to measure `sd(log f)` on, and there is no candidate ranking for the six
  laws to bound. Every word of that is right and this pass agrees with it. **What this pass adds is that
  additivity is not sufficient to escape the closed family's BEHAVIOUR, and the measured discriminator says
  which members do:** three of the four propagation members priced here (C6 the structure-length change, K1 the
  removal member, C8 the unregistered-position member) return **R = 1.000 with 0 sign changes**, the closed
  family's own exact signature, while the only member that returns R greater than 1 is C5, the re-phasing, and
  C5 is precisely the member whose counterfactual has to re-time events that were never recorded. **So the
  additive decomposition and the per-case form behave identically whenever the path is one-signed, and the one
  thing that breaks the equivalence, a sign change in the path, is the same thing that makes the counterfactual
  K2 and therefore indeterminate.** That is the sentence the two notes jointly earn and neither carries alone.
- **The family is occupied by three concurrent slots, which settles the draw independently of the
  measurements.** task194 holds the vegetation-cycle instance with the linkage trichotomy and the
  cheapest-route kill; task202 holds the branch whose mixture weights are exact at a coarse reporting grain and
  has already killed its surge-schedule queue candidate twice over; task125 holds the shipped driver and its
  card's `Lesson:` line states the generalisation verbatim. A fourth slot drawing here would clone a concurrent
  slot even where it cleared task125, so nothing in the family is taken to a card by this pass and **the family
  is not to be re-screened from this number.**

- **Architecture 5, the overidentification axis on instrument and laboratory ground, refused with
  measurements (2026-10-24).** A few analyser offsets and scales identified across many split specimens by
  the network's own exchange. The design genuinely overidentifies (960 readings against 490 unknowns, the
  focal analyser's scale recovered to about 1 per cent), and that is the kill rather than the opening.
  **Horn 1:** with additive shared parameters the joint solve collapses to the pairwise group-by by algebra,
  max absolute difference **5.129e-13**, corr **1.00000000**, identical graded count in 10 of 10 seeds.
  **Horn 2:** with offset and scale the licensed family spreads the graded share **12.2 to 45.8 printed
  units** and agrees on the printed figure in **0 of 12** worlds at the largest case count, and the exact
  count above the limit is reached by only 2 to 6 of 20 even with the shared parameter precise, so the
  shared-parameter design does not rescue the discontinuous count. **Horn 3, the verdict:** the naive route
  fails (11 of 24) but **the ratio of each exchange pair's means, one group-by, lands it 22 of 24** and one
  ordinary least squares per pair lands it **23 of 24 at a smaller recovery error (0.989 per cent) than the
  designed joint solve (1.154)**, with the family unanimous 11 of 12 and 8 of 12; the field's own textbook
  route (Deming) is the worst member at 19 of 24. **R = 1.000 with 0 sign changes in every cell**, so the
  construction is a per-case correction in other nouns. The guard is independent of all of it: the probe
  card BLOCKs on `ban.artifact`, `ban.forum`, `test.same_driver_older` against task260 and an empty
  persona list, and `guard.py slots` on the setting's nouns returns task249 architecture 1 (the same
  candidate, landed by a medium-effort reader in about two minutes with an errors-in-variables slope) and
  task252 architecture 1 (the same candidate with a memory term, "every term of that model is identified by
  the readings, the checks and the grabs"), with task185 holding the level-dependent device conversion as a
  driver already. Not to be re-screened from this number in any nouns.
- **The whole line of architectures 1 to 5 abandoned, 2026-11-03 (stage 1, never registered).** Five passes on six grounds (crime hotspots, environmental exceedance, supply-chain multiple testing, genomics, exploratory distribution assessment, disease surveillance and provider quality) spent 38 mechanisms and closed the overidentification axis as a clause in any nouns; the slot moves off every one of those client domains rather than screening a sixth cell in them, and architecture 6 re-roots into human-factors-ergonomics (safety-incident-error-analysis) with a new world, dataset and generator, the decisive step a memory effect on recurring test items that no card on file carries.
