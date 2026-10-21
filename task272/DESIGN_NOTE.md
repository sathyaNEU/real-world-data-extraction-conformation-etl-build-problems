# task272 design note

Architecture 1, drawn 2026-10-21 (wave 4, Descriptive lane, sathay3012) from seed DA22's world, decision and quantity only: a health foundation's FY2027 coaching grants, one per qualifying organisation, a six-point line, 31 applicants and the board's budget vote on 12 March 2027. The Vellacott Health Foundation in Portland, Oregon runs the Fair Billing Initiative, whose 31 participating hospitals in Oregon and Washington pool their financial-assistance determination logs. From 1 July 2027 the initiative funds decision coaching for hospital financial-assistance teams: one grant per hospital whose counsellors are at least six percentage points less likely to approve an application right after approving the one before than right after denying it, on the same working day, measured on the 2025 logs. Kristin Robertson, the initiative's program officer, needs the number of grants for the FY2027 budget.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task272.json`, architecture 1, registered 2026-10-21 at WARN (item 9). The foundation funds the initiative (`foundation_or_funder`); its board approves the FY2027 budget (`board_of_directors`); the forcing event is the coaching's start on 1 July 2027 (`launch_or_rollout`); the requester is the initiative's program officer (`programme_officer`). Context artifact `filed_standard` (the initiative's coaching criteria); no calibration organ.
2. Pairing: General Statistics & Data Science (client domain) / resampling-simulation-monte-carlo-methods / Descriptive & Distribution Analysis (the README tags the task type F and DD). The task type's own object decides the call: a dependence statistic read against its distribution under random reordering within each session, the benchmark the null makes exchangeable.
3. Niche: a health foundation's FY2027 decision-coaching grants for hospital financial-assistance teams, one per hospital whose counsellors approve an application markedly less often right after approving one, measured from the counsellors' 2025 determination logs, worked in short daily queues whose mix of applicants swings from day to day.
4. Call and shape: how many grants the FY2027 budget carries (`quantity_figure`, a count; question form how-many). Shape 10 (a scorecard against a threshold): each hospital's verdict against six points, the qualifying hospitals named and the count, with the measured drops charted. The drops are charted and never graded at a printed precision: the estimator family agrees on every verdict by 1.5 points or more and spreads up to about 4 points on a level (item 10), so a printed level is not forced while the set and the count are.
5. Gate G `decomposition_attribution`, strategy `decomposition_attribution`: every record measures the within-day drop after an approval correctly, and the analysis assigns it to its drivers, the day's mix of applicants, the length of the day's queue and the counsellors' tendency. The decisive step measures each hospital's drop against what the same day's determinations would show in any order (the exact expectation under reordering within each counsellor's working day, or a conditional likelihood that conditions on each day's count), rather than pooling consecutive determinations over days of different mix, which credits the mix's strings of approvals against the drop, or comparing within each day, which in a queue of n determinations manufactures a drop of about 100/(n-1) points with no tendency at all. Decisive generators G6 (composition shift: the day's mix is what the comparison has to hold fixed and what pooling credits to the counsellors) then G16 (method selection: the estimator that holds the day fixed without manufacturing a drop). G6 leads because the pattern axis was redrawn off G16 at the draw (`ban.pattern` against task480), and it is the honest first key, not merely the passing one: both rungs of the ladder are failures to hold the day's mix fixed correctly.
6. Data-native sentence: the initiative's counsellors work short daily queues (7 to 24 determinations a day, by hospital) fed by intake that swings from presumptive Medicaid referrals and outreach events to mailed balances, so consecutive determinations share their day's mix while a short day's own determinations, compared after an approval and after a denial, carry a drop of about 100/(n-1) points that no counsellor put there.
7. Sources, one line each:
   - The client's rigor library, resampling-simulation-monte-carlo-methods 3 (permute only what the null makes exchangeable; within strata, not across all rows): the cousin of this build's benchmark, and its pin files the permutation scheme, which this build does not; here the data's structure forces the stratum (the working day), and the decisive point the card does not carry is that the within-stratum statistic of a short session is not centred on zero under the null.
   - The lane's builds (task263 BISG unmixing, task264 size-biased exits, task267 design weights, task268 losses to follow-up, task269 a decision study, task270 range restriction, task271 the kin-cohort): none measures serial dependence or a session's own benchmark.
   - `guard.py slots` on gambler, hot hand, streak, previous decision, sequence effect, Nickell, permutation, reordering, serial dependence and lagged: no screen of this mechanism on file; task177's "streak breaks" is a rate-by-state design carried to a new state mix, a different driver.
8. People, drawn with `guard.py names --geo "United States" --seed 272`: Kristin Robertson (the initiative's program officer, the requester) and Spencer Frank (the foundation's director of programs, who takes the budget to the board). Jacob Burgess, Stephen Graham, Patricia Morse and Olivia Maldonado were set aside on `people.first` WARNs. Invented names Vellacott Health Foundation and Fair Billing Initiative, screened against the H21 register at stage 3.
9. BLOCKs cleared and WARNs answered. Cleared at the draw by redrawing the axis: `ban.pattern` G16 and `ban.strategy` causal_design against task480 (generators reordered, strategy `decomposition_attribution`, Gate G `decomposition_attribution`); `test.same_puzzle_older` and `test.same_driver_older` against task185, task80 v2 and task457 v1 (cleared by the reordered generators); `ban.forcing_event` budget_or_appropriation against task480, then vote_or_meeting against task484 (the coaching's start, `launch_or_rollout`, is the honest event: the budget vote is the forum's act, the launch is what forces the count now). WARN `repeat.question_form` how-many against task484 v1: the call is the number of grants, a count, so how-many is the honest form. Re-filed at stage 3 (2026-10-21): task479 v5 (shape 10), filed at 01:37Z in another lane, reached this checkout only in the rebase before the DRAWN push, so the draw's check never saw it and the heart screen blocked `ban.shape`; shape 10 is the honest shape (each hospital's measure against its six-point threshold) and was kept, not relabelled; with task482 v2 and task251 v5 filed since, the re-filed card clears with one WARN, `repeat.deliverables` png+xlsx against task251 v5 (the scorecard and its chart are the honest pair). The surface screen read "Monte Carlo" in the task type's name as a persona, so the submission's tag and metadata name the task type as resampling and simulation.
10. Screens, run as code at the draw (scratch `t272/proto/s1.py` to `s6.py`, the world's own generator to come), to be asserted on the built world in `generator/checks.py`:
    - WHAT screen: population (each participating hospital's counsellors' determinations recorded in 2025, the system's own presumptive determinations aside), outcome (approval, any discount granted), window (calendar 2025), unit (percentage points of a counsellor's chance of approving) and comparison (right after the same counsellor approved the previous application against right after the counsellor denied it, among the applications one counsellor decides on one working day, against six points) are filed in the criteria; the decisive step settles none of them, it estimates a chance that the records hold only as short days' relative frequencies.
    - 1.2a: the filed quantity is unobserved (a counsellor's chance of approving given the previous determination and the day's applications); the raw within-day drop, the pooled drop and the excess over reordering are estimators of one quantity, and the records decide between them: the counsellors' daily approval rates spread far beyond chance (pooling refuted), and every hospital's held-day drop falls with the day's length as 100/(n-1) does (the raw within-day drop refuted).
    - 1.2b: no break in the records decides; one hospital's billing migration re-keys counsellor IDs and changes how no determination is made.
    - Family and lever (the build's world, `generator/world.py`: effects 9.5 to 12.5 points at 11 hospitals and 0 to 2 at 20, mean queues 8 to 32 a day, the day mix's spread 0.10 to 0.20): eight estimators of the one filed chance, the excess over reordering by counts (the golden), the held-day slope less its reordering expectation, Miller and Sanjurjo's per-day excess, the conditional logit read as a marginal effect, a random intercept for each counsellor-day by maximum likelihood, the split-panel jackknife, and the day's rate over the counsellor's other determinations as a control (one or both of the pair left out), name the same 11 hospitals, every member at least 1.81 points from the line on every hospital, by construction (a hospital is redrawn until its whole family sits on one side with 1.5 points to spare; 40 draws for 31 hospitals).
    - Reflexes on the cut pack (`generator/cracker.py`): consecutive determinations pooled 2 (H03, H06); the counsellor held 3; the day's rate over every determination as a control 24; each counsellor-day held 23 (the default path); each day's own drop averaged 24; the golden 11.
    - Designation screen: one set across the eight family members; the levels spread up to 8.1 points (H27, the shortest queues, where the day's rate without the pair as a control reads -7.5 against the other members' -0.6 to 0.5, far on the steady side), which is why the levels are charted and never graded.
    - Two routes that land the call, measured and kept as family members rather than treated as reflexes: the day's rate over the counsellor's other determinations as a control (the others' count carries what the day's applications say about the chance, so it conditions as the golden does) and a random intercept for each counsellor-day by maximum likelihood (within an exchangeable day its within-day bias and its between-day information cancel). Both need the insight that a day's own determinations, not its mean, are what the comparison holds; a reader who takes either has found the decisive step.
    - Common-exposure subset and partial-coverage screens: the session-length bias touches every day (about 4 points even at 26 a day), so no subset of days is free of it; the long days alone still put the short-queue hospitals' nulls over the line, and the short-queue hospitals have no long days.
    - Null-region screen: the system's presumptive determinations run under a system account and are in no counsellor's queue, and a day's first determination has no same-day predecessor; neither publishes the benchmark.
    - Benchmark screen: the benchmark is one figure per hospital built from every day's own count and length; no column, document or one-group-by route publishes it, and the analytic shortcut (100/(n-1) per day) is itself the decisive step.
    - One-number screen: the correcting input is per day (each day's length and count), and it reorders the hospitals, being largest where queues are short.
    - Readability: no filed sentence names a reordering, a chance benchmark, a streak or a session's length; no column marks a day as short.

## Default path

1. Read the criteria: a hospital qualifies when its counsellors are at least six percentage points less likely to approve an application right after approving the previous one than right after denying it, among the applications one counsellor decides on one working day, in 2025.
2. Conform the three billing systems' exports (their layouts and decision codes, one system's UTC clock against the others' local time, rows re-sent, the system account's presumptive determinations set aside, the re-keyed counsellor IDs joined through the crosswalk).
3. Order each counsellor's determinations within each local working day.
4. Hold each counsellor-day fixed, the day's applicants being what the criteria compare within: regress each approval on the previous same-day determination with a fixed effect per counsellor-day (each day's own drop, averaged, files 24).
5. Count the hospitals at six points or more.

Ends on: 23 hospitals (H01, H02, H03, H06, H07, H08, H09, H10, H11, H14, H17, H18, H19, H20, H21, H22, H23, H24, H26, H27, H28, H29 and H31).
Golden: 11 hospitals (H03, H06, H09, H10, H17, H19, H20, H21, H22, H26 and H31).

## Stump sentence

A competent analyst who conforms the three exports and holds each working day's mix fixed by regressing every determination on the counsellor's previous one with a fixed effect per counsellor-day puts 23 of the 31 hospitals over the six-point line, because a queue of eight determinations shows a drop of about 14 points after an approval with no counsellor swayed at all, and one who pools consecutive determinations instead puts 2 over it, because days fed by presumptive referrals string approvals together; only the excess over what each day's own determinations would show in any order puts the 11 hospitals whose counsellors are really swayed over it.

## Three rules

Task type: resampling-simulation-monte-carlo-methods (General Statistics & Data Science), which serves Descriptive & Distribution Analysis in the taxonomy.
Domain test: the quantity that decides the call is each hospital's sequence effect, the dependence of a counsellor's approve-or-deny determination on the counsellor's previous one within a working day; the resampling task type measures such a dependence statistic against its distribution under random reordering within each session, because in a short session the statistic's expectation with no dependence is not zero, and replacing that benchmark with a pooled or fixed-effects contrast moves the count from 11 to 1 or 27.
Swap: in this domain the setting is always another field's, so the swap is of the method: the same call with loan officers' decisions or umpires' calls reads the same, as the taxonomy expects, while the call read off the pooled contrast (2) or the held-day contrast (23) instead of the excess over reordering (11) stops being the counsellors' tendency: it becomes the intake's mix, or the queue's length.
Layer 1: three regional hubs' extracts with their own layouts, outcome codes and clocks (the Columbia hub's in UTC, so a working day is a Pacific date); the presumptive screening's approvals under each hub's system user; reconsiderations recorded as further determinations once missing documents arrive; pends and withdrawals between determinations; H23's billing conversion on 2 June 2025 moving its rows from one extract to another under re-keyed counsellor IDs, with a crosswalk; the Willamette hub's December 2025 adjustments loaded twice. Each is produced by the systems and nothing is placed to be caught; on the call's path each mishandled keeps the call (SF1 to SF4 asserted: the UTC clock read as local, first determinations only, pends and withdrawals as denials, the presumptive screening kept, each files the same 11).
Layer 2: estimation_fit: the serial dependence measured as the excess over each counsellor-day's own reorderings, against pooling consecutive determinations (the day's mix) and against the raw within-day drop of short queues (the finite-session bias).
Decisive step: benchmarking each hospital's drop after an approval against what the same day's determinations would show in any order, rather than reading the raw within-day drop of short queues or pooling days whose mix differs.
Not semantics: with every field, code, clock and account read correctly, the within-day drop of an eight-determination day still carries about 14 points with no tendency at all, so the easy route on correctly read records files 23 hospitals.
Not rule application: the criteria fix the population, the outcome, the year, the unit and the comparison; no filed rule or procedure says how a short day's within-day drop is benchmarked, and executing every stated rule with the easy route files 23.
Analyst test: a strong analyst who conforms the three exports and holds each counsellor-day fixed (a fixed effect per counsellor-day) files 23 hospitals, and one who pools consecutive determinations files 2; only the excess over each day's reorderings files 11 (`checks.py`, ANALYST TEST, on the generator's clean records).
Estimand: the foundation's criteria (`fac_decision_coaching_criteria_fy2027.pdf`): 2.1 "A hospital qualifies when its financial-assistance counsellors are at least six percentage points less likely to approve an application right after approving the application before it than right after denying it"; 2.2 the hospital's counsellors' 2025 approvals and denials, first and on reconsideration, by local date, without pends, withdrawals or the presumptive screening; 2.3 each determination "compared by the determination the same counsellor recorded just before it on the same working day"; 2.4 "Likely refers to the counsellor's chance of approving the application in hand ... the comparison is between the chance right after an approval and right after a denial among the same working day's applications; the difference between one day's applications and another's is not part of it"; 2.5 an approval reduces what the patient owes, in full or in part; 2.6 percentage points, compared with six unrounded; the terms' "Chance of approving: the probability that the counsellor approves an application of the kind the working day brings".
No decoy: nothing is planted to be caught: no memo, dashboard, prior screening or stakeholder figure states any hospital's drop, the survey and the state filings rank nothing on the question, and no copied block or hidden rule sits in the extracts.
No certified replay: the pack publishes no sequence-effect figure, so no method is recovered by reproducing a certified or published number.
Lesson: a dependence statistic measured within short sessions is pulled one way by the sessions' own length and the other way by pooling sessions of different mix, and each session's own reorderings give the benchmark; no build on file teaches it (the slot search above).

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 consecutive determinations pooled over the whole year, day boundaries ignored | criteria 2.3 confines the comparison to the same working day | the date in every timestamp | none | none | none | one cross-tab | readable |
| R1 within-day pairs pooled over a hospital's days (2 hospitals) | criteria 2.4 says the difference between days is not part of it | none | the plain conditional share | none | none | one cross-tab | readable |
| R1b within-day pairs with the counsellor held (3) | criteria 2.4, as R1 | the user ID | the counsellor fixed effect | none | none | one regression | readable |
| (default path) R2 each counsellor-day held by its own fixed effect (23) | none: 2.4 asks for the comparison among a day's applications and says nothing of how a short day's own drop is read | the counsellor and the date | holding the unit of the comparison fixed, the opponent's first repair of R1 | none | none | one regression | readable |
| R2b each day's own drop averaged (24) | as R2 | as R2 | the per-session conditional share | none | none | one mean | readable |
| R2c the day's approval rate over every determination as a control (24) | as R2 | as R2 | controlling for the day's leniency | none | none | one regression | readable |
| (decisive) R3 each hospital's within-day contrast less its expectation with each day's determinations in any order (11) | none: no file says that a short day's drop is not centred on zero, names a reordering, a session's length or a chance benchmark | no column marks a day as short or carries a day's expected drop | none: the opponent's repairs hold the day (R2, R2b, R2c), which is the step that manufactures the drop | none: no shipped figure ties under either reading | none: the battery passes on the extracts as written (one row a determination, every code mapped, every clock converted) | a closed form per day, once the bias is seen | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | 2025, by date | the hospital's local date | the Columbia extract's UTC date | same call (asserted) | criteria 2.2: "(the hospital's local date)"; the guide: ts_utc "in UTC" |
| SF2 | determinations | first and on reconsideration alike | first determinations only | same call (asserted) | criteria 2.2: "first determinations and determinations on reconsideration alike" |
| SF3 | a pend or a withdrawal | not a determination | counted as a denial | same call (asserted) | criteria 2.2: "A pend or a withdrawal is not a determination" |
| SF4 | the presumptive screening | not a counsellor | its approvals kept | same call (asserted) | criteria 2.2: "The nightly presumptive screening is not a counsellor, and its approvals are not counted" |
| SF5 | the determination before it | the one before it on the same working day | the previous working day's last for a day's first | 0 hospitals (asserted different) | criteria 2.3: "on the same working day ... A counsellor's first determination of a working day follows none" |
| SF6 | an approval | any reduction, full or partial | full approvals only | same rows: every approval carries its percent (asserted) | criteria 2.5: "in full or in part" |
| SF7 | six points | percentage points | six percent of the rate | not a reading: a difference of two shares | criteria 2.1 and 2.6: "percentage points" |
| SF8 | likely | the chance among the same working day's applications | the chance over all of a hospital's determinations together | 2 hospitals (asserted different) | criteria 2.4: "the difference between one day's applications and another's is not part of it"; the terms (Chance of approving) |
| SF9 | its counsellors | the hospital's counsellor-days pooled | each counsellor's own measure averaged | same call (asserted) | same call |
| SF10 | at least six | six included | above six | same call: no hospital within 0.5 points (asserted) | criteria 2.1 and 2.6 |
| SF11 | the order the counsellor recorded them | the recorded time | the hub's row number | same order on every counsellor-day (asserted) | criteria 2.3 |
| SF12 | the same counsellor across H23's conversion | one user ID on each side | the two IDs joined through the crosswalk | same call: no working day spans the conversion (asserted) | the guide, section 1; the crosswalk |
| SF13 | a working day with one determination | no pair | none | same call | criteria 2.3 |
| SF14 | a reconsideration of a 2024 denial recorded in 2025 | a 2025 determination | left out | same call (asserted) | criteria 2.2 (recorded from 1 January to 31 December 2025) |

## Ladder

Built figures from the cut pack (`generator/analysis.py`, every route in `generator/models.py`, asserted in `generator/checks.py`, recomputed by `generator/verify.py` with a Monte Carlo reordering in place of the closed form). Drop in the chance of approving right after an approval, percentage points, 197,939 counsellor determinations:

| Rung | Construction | Hospitals over six | What kills it |
|---|---|---|---|
| R0 | consecutive determinations over the whole year | not built: 2.3 confines pairs to a day | criteria 2.3 |
| R1 | within-day pairs pooled | 2 (H03, H06) | days of presumptive referrals string approvals together, so the mix reads as a rise after an approval (pooled measures -16.7 to 6.5) |
| R1b | the counsellor held | 3 (H03, H06, H26) | the day's mix still moves within each counsellor |
| R2 (default path) | each counsellor-day held | 23 | a day of n determinations shows about 100/(n-1) points with no counsellor swayed: every one of the 20 steady hospitals measures 2.2 to 12.9 on it |
| R2b | each day's own drop averaged | 24 | as R2, the per-session bias undiluted |
| R2c | the day's rate over every determination as a control | 24 | the control contains the pair: as R2 |
| R3 (golden) | the within-day contrast less its expectation with each day's determinations in any order | 11 | none |
| R3 | the held-day slope less its reordering expectation; Miller and Sanjurjo's per-day excess; the conditional logit; a random intercept per counsellor-day; the split-panel jackknife; the day's rate over the other determinations (one or both of the pair left out) | 11, the same set under every member | none |

By hospital, the golden against the two easy routes and the family's range (points):

| Hospital | Golden | Held day | Pooled | Family low | Family high |
|---|---|---|---|---|---|
| H03 | 10.9 | 18.2 | 6.2 | 9.5 | 12.6 |
| H06 | 9.8 | 21.1 | 6.5 | 8.4 | 11.9 |
| H09 | 9.2 | 14.1 | -3.0 | 8.1 | 11.1 |
| H10 | 9.4 | 14.0 | -1.0 | 8.3 | 11.1 |
| H17 | 10.5 | 17.1 | 0.9 | 8.7 | 12.7 |
| H19 | 10.6 | 18.1 | 2.0 | 8.7 | 12.9 |
| H20 | 9.6 | 14.3 | 1.7 | 8.7 | 11.4 |
| H21 | 9.0 | 13.6 | -2.2 | 7.8 | 10.6 |
| H22 | 9.4 | 14.8 | -3.3 | 8.4 | 11.5 |
| H26 | 9.5 | 18.0 | 2.8 | 7.9 | 11.6 |
| H31 | 10.2 | 16.8 | -0.7 | 8.2 | 12.4 |
| H18 (highest steady) | 2.8 | 12.4 | -12.8 | -2.2 | 3.4 |
| H27 (shortest queues) | -0.2 | 12.9 | -16.3 | -7.5 | 0.5 |
| H05 (long queues) | -0.1 | 3.8 | -11.2 | -2.3 | 0.1 |

The family closes on the call: every member's verdict is the same on every hospital, the nearest any member comes to the line is 1.81 points (H21's leave-two-out at 7.81; H18's highest member 3.4). The clean truth (the generator's own determinations) names the same 11.

The world under it: each hospital's counsellors work queues averaging 8 to 32 determinations a day on about half their working days; a counsellor's chance of approving sits at a level of the counsellor's own (0.52 to 0.80) moved each day by the day's intake (a spread of 0.10 to 0.20); reconsiderations are 0.15 likelier to be approved; inside a day the applications come in the order they became complete, unrelated to merit; at 11 hospitals the chance falls by 9.5 to 12.5 points after an approval against a denial, at 20 by 0 to 2.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | each hospital's counsellors' approvals and denials of 2025, first and on reconsideration | filed: criteria 2.2 (SF2, SF3, SF4, SF14) |
| 2 Unit of account | the determination; the hospital's measure | filed: criteria 2.1 and 2.2 |
| 3 Attribution window | 1 January to 31 December 2025, local date | filed: criteria 2.2 (SF1) |
| 4 As-of dating | the extracts as the hubs wrote them; adjustments posted through 31 March 2026 | filed: the data guide, sections 1 and 7 |
| 5 Version basis | each determination as recorded | C1 |
| 6 Denominator | the determinations that follow another on the same working day, by what came before | filed: criteria 2.3 |
| 7 Weighting | the hospital's counsellor-days pooled | same call (SF9) |
| 8 Window length | one calendar year | filed |
| 9 Boundary inclusivity | six points included | filed: criteria 2.1 (SF10) |
| 10 Rounding path | compared unrounded; verdicts and the count graded, levels charted | filed: criteria 2.6; the prompt |
| 11 Tie-break | none needed | C1 asserted (SF10) |
| 12 Maturity and censoring | none: every 2025 determination is final | C1 |
| 13 Order of operations | conform, select, order within the day, pair, measure, compare | C1 |
| 14 Row order | the recorded time within a counsellor's day | filed: criteria 2.3 (SF11) |
| 15 Duplicate resolution | none in the extracts; the adjustments' twice-loaded lines once (Ask A) | C1; the prompt |
| 16 Identity normalisation | the counsellor's user ID on each side of H23's conversion | the data guide, the crosswalk (SF12) |
| 17 Netting against gross | Ask A net of reversals | filed: the prompt |
| 18 Dimensional units | percentage points; thousands of dollars | filed: criteria 2.6; the prompt |
| 19 Code and status semantics | each hub's outcome codes; the common reason list | the data guide, sections 2 to 5 (SF6) |
| 20 Integerisation | the count of grants; the denials in whole counts | the prompt |
| 21 Clause scope | section 2 for the call; the prompt for the scorecard columns | filed |
| 22 Forward window contents | the counsellors' 2025 tendency stands for the coaching year from 1 July 2027 | filed: criteria 1.1 to 1.3 |

## Literal reader

Executed word for word, the criteria file each hospital's measure as how much less likely its counsellors are to approve an application right after approving the one before than right after denying it, comparing each 2025 determination with the one the same counsellor recorded just before it on the same working day, where likely is the counsellor's chance of approving an application of the kind the working day brings, the difference between days not part of it. The records give every one of those determinations and their order; the chance is not a column, and each working day carries only a handful of pairs. Read off a day's own pairs, the chance after an approval is the day's other approvals over its other determinations, and that is lower than the chance after a denial by about 100/(n-1) points in a day of n determinations even when the order carries nothing: the 20 steady hospitals measure 2.2 to 12.9 on the held-day route and their held-day measure falls with their queues' length. Against the expectation of the same contrast with each day's determinations in every order, which is what a chance among a day's own applications leaves when the order carries nothing, the measure is the counsellors'. The family closes on the 11 hospitals (Ladder).

## Oracles

No shipped figure states a hospital's drop, ranks the hospitals or gives a day's expected drop. The state charity care filings (fiscal year 2025, at full charges, every program) tie to Ask A under no reading, and the survey's would-recommend rates rank nothing on the question.

## Ask sheet

The asks are decoupled from the call: neither reads the order of a counsellor's determinations, and the call reads no adjustment, account, reason code, survey or filing (asserted: the call unchanged with every reason code blanked; the call is computed from the three extracts' outcome, user and time columns alone). Both are columns of the board's scorecard, a measure every hospital carries that the call does not turn on. The data guide describes the adjustments and the reason codes in the voice the warehouse would and adjudicates no device (asserted: no device word in the guide or the criteria).

**Ask A. For each hospital, the assistance its counsellors' 2025 approvals wrote off, net of the reversals posted by 31 March 2026, thousands of dollars to one decimal (31 figures).**
- H18 home: the scale of each hospital's assistance beside its verdict, the scorecard's money column.
- Use: the board packet's scorecard.
- Path: fac_assistance_adjustments_2025.csv (hospital_code, application_id, account_number, posted_date, adjustment_code, amount), fac_patient_accounts_2025.csv (account_number, patient_balance), the three extracts (application, user, outcome, the system users): five files, eleven columns.
- Primary device (D6, an event's quantity on every line it covers, grain unstated): the warehouse's extract writes an approval's whole write-off on every account line the approval covers; 49,308 of the counsellors' 129,227 approvals (38.2 percent) cover two to four accounts. Summed as given, every hospital's figure is 5,067.3 to 23,193.3 thousand high (asserted, 31 of 31). No duplicate, every key unique, every join complete: the battery finds nothing. Found only by the cross-file cut: a line larger than its own account's balance in the accounts file, at every hospital (asserted), while no single-account approval's line exceeds its account's.
- Hazards: the Willamette hub's December 2025 lines loaded twice (exact duplicates); reversals (FAWR) at account grain; the presumptive screening's approvals in the same extract; the posting date against the determination date.
- Stops (built, against the golden): every line as given, the cracker (each hospital 5,067.3 to 23,193.3 high); every line, duplicates kept (6,125.5 to 25,054.5 high); every line, the presumptive approvals kept (7,411.2 to 26,165.7 high); each approval once, reversals ignored (205.9 to 834.9 high); the answer, 402,933.0 thousand in all.
- Realism: an extract that joins an application-level amount to account-level lines repeats it on every line, and nothing in the extract's own columns says which grain an amount sits at.

**Ask B. For each hospital, how many of its counsellors' 2025 denials were for documents not received, whole counts (31 figures).**
- H18 home: the denials the coaching's case reviews start from, beside each hospital's verdict.
- Use: the board packet's scorecard.
- Path: the three extracts (denial_reason, DENY_RSN, reason; the outcome, user, type and date columns; application numbers for the reconsideration link), the data guide's reason list: four files, nine columns.
- Primary device (D2, a label stored before a silent switch): the collaborative renumbered its common reason list on 1 July 2025 (documents not received from code 2 to code 1, income above the limit from 1 to 2); the guide carries the list in force since. Read by the guide for the whole year, every hospital's count is 79 to 378 high (asserted, 31 of 31). Found only by the cross-row link: the denials that a later reconsideration reopens (an applicant supplying what was missing) carry code 2 to 30 June and code 1 from 1 July, at every hub (asserted).
- Hazards: reconsiderations that are themselves denied; the three hubs' outcome codes; the Columbia clock.
- Stops (built): the guide's list for the year, the cracker (79 to 378 high); the first list for the year (82 to 402 high); the denials later reopened (32 to 340 low); first determinations only (19 to 95 low); the answer, 22,683 in all.
- Realism: a shared code list revised mid-year leaves the earlier rows on the earlier numbers, and a data guide documents the list in force.

Main population zero-counts: device and hazard rows on the call's path (the order, outcome, user and date of the counsellors' determinations): 0; the reason codes and the adjustments are columns and files the call never reads (asserted: the call unchanged with the reason codes blanked).

| Hazard | Asks moved | Per-ask delta (built) |
|---|---|---|
| the twice-loaded December lines | A | with the golden's handling otherwise, 10 Willamette hospitals 15.1 to 105.3 low (their December reversals taken twice) |
| the presumptive screening's approvals | A | with the golden's handling otherwise, each figure 830.7 to 2,464.8 high |
| reversals at account grain | A | each figure 205.9 to 834.9 high when ignored |
| reconsiderations denied again | B | each figure 19 to 95 low when left out |

Referee: none (Oracles).

| Ask figure | The cracker's figure against the golden | Cracker (lands the call, runs the battery: exact duplicates dropped, key uniqueness on every extract and on the adjustment lines, every application and account joined; executes the guide's codes, the criteria's population and the extract's cut) |
|---|---|---|
| A, each hospital's assistance (31) | each 5,067.3 to 23,193.3 thousand high | miss |
| B, each hospital's denials for documents not received (31) | each 79 to 378 high | miss |

Measured by: generator/cracker.py
Mirror leakage: 0.0 per cent of ask weight (the mirror reads both asks as the cracker does and misses all 62 figures)
Pair ceiling: 28.5 (cracker 45.0 on the call alone, mirror 12.0), Part 0's weights; stage 4's scored readers are the measurement.

## Leak check

`leak.py task272 --asof 2027-01-26`: REVIEW, no LEAK (the grant's price left block 4, where the sweep read it as an answer, after the first run). Each REVIEW line, harmless:
- contents.txt and the criteria carry the program's name (Decision Coaching Grants, FY2027, budget): the call's words because they are the program's.
- The criteria carry the estimand's words (counsellor, determination, working day, chance, comparison, points): filed WHAT; no file names a reordering, a session's length, a streak or a benchmark (asserted in `checks.py`, LEAK words).
- The guide carries the extracts' own vocabulary (counsellor, determination, approval, application, screening): column descriptions.
- The prompt's two sentences carry counsellors and determinations: the program's subject.
- The member hospitals workbook and the state filings name the 31 hospitals beside beds, policy limits and charity care at charges: neither ranks them on the question, and the filings tie to Ask A under no reading.

## Tried and rejected

- The seed's own quantity (the Medicaid gap on the "would recommend" top-box rate across a state report's hospitals), every route screened at the draw: composition and patient mix settle the comparison population (WHAT screen); shrinkage of small cells repeats task253; design weighting repeats task264's lesson and task268 v2's reflex; nonresponse either fails determinacy or repeats the inverse-probability weighting of task264, task267 and task268; survey mode effects belong to Experiment & Causal Analysis; misclassification is the spent sensitivity-and-specificity family; nowcasting the late returns repeats task181; telescoping sits next to task453.
- A race-probability (BISG) regression for the equity gap (prototype `p1.py`): a strong ladder, but the same linear unmixing of a mixed population as task263, a clone of its driver.
- Traffic count factor groups for an annual average (prototype `t1.py`): count differences of one or two units at tiny margins, and the ground overlaps task474.
- The sequence effect at queues of 4 to 14 determinations with effects of 2 to 13 points (`s1.py`, `s2.py`): the two corrected estimators (the excess over reordering by counts, the held-day slope less its reordering expectation) disagreed on 1 to 3 hospitals a seed, with the closest margins 0.01 to 0.3 points; the queues were lengthened and the effect hospitals separated from the line.
- Effects of 12 to 17 points (`s4.py`, `s5.py`): the family agreed, but the day's rate without the pair as a control landed 10 or 11 of the 11 hospitals, its bias of 3 to 5 points smaller than the gap to the line; the effects were lowered to 9.5 to 12.5 with a wider day mix (`s6.py`), where it lands 9.
- Ask B as presumptive approvals with nightly re-runs replayed under fresh application numbers (D1): dropped at stage 2, because no asking sentence makes the count determinate without naming the device (a replay is a fresh application record, so "each application once" counts it, and any wording that excludes it narrates the re-run); replaced by the reason list renumbered on 1 July 2025 (D2).
- Queues of 6 to 28 a day with counsellors sitting on 55 percent of working days: the held-day route filed 28 of 31, an answer a reader distrusts on sight; queues of 8 to 32 on 48 percent of days put it at 23 with the family still closed (1.81 points).
- Effects of 9.5 to 12.5 points with the day's rate over the other determinations as a reflex: it landed the golden set (the others' count is the day's sufficient statistic), so it was moved into the family and the construction made every member agree, rather than the world bent to break it.
