# task241 design note

Architecture 2, drawn 2026-11-03, a re-root of the same number and objective (Data Quality Monitoring & Alerting)
into another client domain, world and dataset. Architecture 1 (the Iberian Basin float array's delayed-mode
salinity, shipped 2026-10-17 as 8dca2562 and still at the portal) was spent at the 11-01 re-check on its survivor
anatomy; its record, the 11-02 screen (A2.1 to A2.21) and the 11-03 screen (A3.1 to A3.22) are in Tried and
rejected.

Kettle River Research, an independent survey research firm in Saint Paul, Minnesota, runs a telephone centre for
public-agency, university and association clients. Its recurring projects (annual trackers fielded every year to
a fresh landline and business sample) are placed by a predictive dialer whose answering machine detection listens
to the first seconds of every answered call: a call it classes as a machine gets the project's recorded message
and is closed as an answering machine without reaching an interviewer, and a call it classes as a person goes to a
free interviewer or, when none is free inside two seconds, is abandoned with the same recorded message. Every
project dials out on its own caller-ID line, and calls returned to that line land on the inbound switch. Before
the 2027 project year opens in January, the director of telephone operations sets each project's detection on or
off under the firm's 2027 dialer policy: detection stays on for a project only while fewer than one in ten of the
calls it classed as answering machines on that project in 2026 had in fact been answered by a person.

## Draw

1. **Pairing.** General Statistics & Data Science / `missing-data-censoring-measurement-error` / Data Quality
   Monitoring & Alerting. The object is the health of the dialer's call-outcome data, the answering-machine
   disposition the detector writes; the call is a monitoring decision, the projects whose detection is switched
   off for 2027 because their machine-classed outcomes are not trustworthy. In General Statistics the swap is of
   the method (`## Three rules`).
2. **The 10/10 rules, answered first.** The deciding quantity is a recorded classification's error rate per
   population, the task type's own measurement-error object, estimated as a ratio of two conditional reaction
   rates; Layer 1 is the systems' own mess (formats, legs, test calls, two project keys, overlapping exports) and
   decides nothing; the decisive step is analytical (the classifier's error rate does not carry from the population
   it was certified on), not a plant, not a field reading and not a stated rule. The analyst test is answered in
   `## Three rules`.
3. **Niche.** A survey research firm's telephone centre deciding which recurring telephone projects run with the
   dialer's answering machine detection switched off in 2027, judged on each project's 2026 share of machine-classed
   calls that a person had answered, against the policy's one-in-ten limit.
4. **Decision and forcing event.** The 2027 project year opens in January and detection is set per project at
   project setup (`launch_or_rollout`); the forum is the telephone operations desk; the organisation is a
   professional services firm; the role family `field_unit_lead`.
5. **Shape.** 10, a scorecard: each project's false-machine share and its verdict against the limit (two
   criteria per project over every recurring project, the per-project return-call and abandoned counts behind each
   share), the call, the nearest project on each side of the limit and the share that would flip it, plus the
   asks. The sum is written in `## Ask sheet` at stage 2 and clears 25.
6. **Default path's answer against the golden.** The default path carries the detector's certified false-machine
   rate (2.1 per cent on the maker's reference set at the balanced setting, confirmed by the firm's 2025 listening
   test of 400 recorded machine-classed calls on the pilot project, 9 of them people) to every project and switches
   detection off on none. The golden switches it off on six projects (Medicare care experience, farm operators, alumni outcomes, veterans' health, small business conditions and child care providers), whose
   shares run 17 to 32 per cent on the built pack, while the other seven sit at 2 to 6 per cent.
7. **Data-native sentence.** The detector decides in the first two seconds of an answer from how long the voice
   runs before it pauses, so the people it hangs up on are the ones who answer with a long greeting, and how many of
   them a project dials depends on whom the project calls; the call detail records only what the detector decided,
   but the people it hung up on ring the project's caller-ID line back within minutes, as do the people the dialer
   abandoned for want of a free interviewer, while answering machines' owners ring back hours later from voicemail.
8. **Spine and files.** The dialer's 2026 call detail, twelve monthly exports under `dialer_exports/` (one row per
   answered outbound call, the old layout to June and the new one from July, each export repeating the last day of
   the month before; about 295,000 answered calls once the repeats are dropped); the inbound switch's log to
   14 January 2027 (one row per leg); the client case records; a state time zone list; the 2027 project setup
   register (xlsx); the 2027 dialer policy (docx); the detector maker's release sheet (pdf); the 2025 listening audit
   (xlsx); the payroll's interviewer hours in its two systems' layouts; and the distractors (the client invoices,
   the mobile consent log, the quality monitoring scores). File names avoid the words the leak sweep
   reads as authorial ("sample_", "test_").
9. **Nearest on file and the abstraction sentence.** `guard.py check` nearest drivers: 0.06 (task455 v1), 0.05
   (task265 v0, task449). The sentence a reviewer holding this build and its nearest approved build would say is
   the same: none can be written. task236 (approved) reads a capture rate against an independent fixed-protocol
   sample's volume times positivity; task192 carries class-conditional rates forward across a moved population;
   task230 v2 has detection falling with prevalence; this build measures a classifier's error rate on each
   population from a reaction only its misclassified members produce, scaled by the same reaction among known
   members of the true class, inside a window that excludes the other class's delayed reaction.
10. **Guard.** `guard.py check` PASS against the window of task479, task188 and task307 v3. The window moved while
    the card was drafted (task307 v3 registered at 11-03 and pushed task173 out): the first draft's
    `monitoring_export` artifact then repeated task307 v3's and was redrawn to `register`, the honest one, since the
    director decides on the firm's 2027 project setup register (one row per recurring project, its dialer settings
    for the year); against the earlier window the draft carried one WARN, `repeat.decision` against task188 v2,
    answered by the call being a set by its nature. Structural tests: `test.same_puzzle_older` against task281 and `test.same_driver_older` against
    task454 and task468 v1, each differentiated on the card. Pattern C (a serviceable share behind a join: the
    share of machine-classed calls that were people sits behind the join of the inbound log to the call detail);
    generators G16 (the certified rate against the per-project estimate) and G6 (the greeting mix behind it).
    Strategy `classification_error`, unspent on this objective. Personas from `guard.py names --geo us --seed 241`
    (Hailey Mullins, director of telephone operations; Vincent Armstrong, quality assurance lead; Brian Maynard,
    dialer administrator). The prompt shell is drawn new against architecture 1's (which, put, png+xlsx): the
    second sentence leads with the deliverable's use, and the deliverable set is a workbook and a pdf note.
    `voice-check.py` WARNs that the question form "which" stands at 38 per cent of the corpus: the call is a
    designation set, which the question form follows, and the shell's other classes are new for the slot.

## Default path

1. Load the dialer's twelve monthly exports of 2026, drop the day each export repeats from the month before, keep
   every project's answered calls and read the dispositions: completed or partial interview, refusal, appointment,
   live answer abandoned, answering machine (message played and closed).
2. Read the 2027 dialer policy: detection stays on a project only while fewer than one in ten of its 2026
   machine-classed calls had been answered by a person.
3. Read the detector maker's specification sheet: at the balanced setting the detector classes 2.1 per cent of live
   answers as machines on the maker's reference set of recorded greetings.
4. Read the firm's 2025 listening test on the pilot project: 400 recorded machine-classed calls drawn at random, 9
   answered by a person, 2.25 per cent, which confirms the maker's figure.
5. The field's method for a classifier's error: take the certified rate, validated on the hand-checked sample, as
   the detector's false-machine rate on every project; a few points either way for each project's mix leaves every
   project far under the limit.
6. File the scorecard: no project reaches one in ten; detection stays on everywhere in 2027.

Ends on: no project switched off; every project's share about 2 per cent.

Golden: six projects switched off (Medicare care experience, farm operators, alumni outcomes, veterans' health, small business conditions and child care providers), shares 17 to 32 per
cent; the other seven 2 to 6 per cent (`generator/figures.json`).

## Stump sentence

A competent analyst carries the detector's certified false-machine rate (2.1 per cent, confirmed at 2.25 per cent by
the firm's 2025 listening test on its pilot project) to every project and switches detection off nowhere, ending on
no project; the step that lands it there is treating a classifier's error rate as a property of the classifier,
when the people a detector mistakes for machines are the ones who answer with a long greeting, so the projects
calling older people, farms and businesses lose 17 to 32 per cent of their machine-classed calls to people the
dialer hung up on, a share that only the calls those people return within minutes, scaled by the same project's
abandoned callers' prompt return rate, can measure.

## Three rules

Task type: general-statistics-data-science / missing-data-censoring-measurement-error, which serves Data Quality
Monitoring & Alerting in the taxonomy.

Domain test: the deciding quantity is each project's misclassification rate of a recorded outcome (the share of its
machine-classed calls a person answered); the field's estimator for a classifier's error is the rate certified on a
reference set and validated by a hand-checked sample; the estimator the data force is the ratio of two conditional
reaction rates on the same project, prompt return calls after machine-classed hang-ups over prompt return calls
after abandoned live answers.

Swap: in General Statistics the swap is of the method: replace the per-project ratio with the classifier's certified
rate, a generic summary, and the call moves from six projects to none; replace the prompt window with every return
call at any delay and it moves to every project; the call reads only with the measurement-error estimator.

Layer 1: the dialer's monthly exports each repeat the last day of the month before (the export runs after midnight
and re-reads the late calls); phone numbers arrive as ten digits in the call detail, in +1 E.164 form in the inbound
switch and with punctuation in the client sample files; the inbound switch writes one row per leg, so a transferred
call appears two or three times; quality assurance places test calls from the firm's own extensions; the dialer
knows projects by client job number and the inbound switch by the caller-ID line's label; the July upgrade changed
the export layout and renumbered the cases, and the payroll's timekeeping system changed its layout the same month.
Each is produced by the systems themselves and none decides the call.

Layer 2: estimation_fit: a classifier's error rate estimated per population from a reaction only its misclassified
members produce, scaled by the same reaction among members known to be in the true class, counted inside a window
that excludes the other class's delayed reaction.

Decisive step: measuring each project's false-machine share on that project's own calls rather than carrying the
certified rate, from the calls people return within minutes of being hung up on, divided by the prompt return rate
of the same project's abandoned live answers.

Not semantics: every disposition, number and timestamp read correctly still leaves the certified rate as the reading
of the detector's error; no field marks a machine-classed call as answered by a person and no definition says the
error differs by project, so the right figure is an estimate, not a reading.

Not rule application: no filed rule or procedure says how to measure the detector's error, and the 2027 policy files
only the quantity, the limit, the window and the unit. The enumerated family on the prototype (the certified rate,
the listening test's rate, the machine-classed share against the firm's norm, the return-call ratio at any delay,
the prompt return-call ratio over a pooled abandoned rate, the prompt ratio over each project's own abandoned rate)
spreads the flagged set from 0 to 13 projects; the standing family once the data are read (the prompt ratio, with
each project's own abandoned callers' rate because those rates run from 9.6 to 48.7 per cent) spreads 0 projects
on the call and 0 points on every graded share across prompt windows of 5 to 40 minutes; what rules the others out sits
only in the inbound log and the calls' timing, which no document points to.

Analyst test: with every field and rule read correctly, the easy route carries the detector's certified 2.1 per cent
(confirmed by the 2025 listening test on the pilot) to every project, puts all of them under the one-in-ten limit and
keeps detection on everywhere, ending on no project; the golden switches it off on six.

Estimand: "Answering machine detection stays on for a project in 2027 only while fewer than one in ten of the calls
the dialer classed as answering machines on that project in 2026 had been answered by a person" (the 2027 dialer
policy, `dialer_policy_2027.docx`): population, every 2026 machine-classed call of the project; outcome, answered by
a person; window, calendar 2026; unit, the call; comparison, the one-in-ten limit.

No decoy: nothing is planted to be caught; the maker's specification sheet and the 2025 listening test are the
organisation's genuine evidence and correct for the populations they describe; no memo, draft, briefing or
stakeholder figure argues for keeping detection on.

No certified replay: the method is not hidden and recovered by reproducing certified figures; the listening test
validates both the certified rate and the return-call ratio on the pilot, and only the other projects separate them.

Lesson: a classifier's certified error rate is a property of the population it was certified on, so where the
populations it is applied to differ, its error is measured on each from a reaction only the misclassified produce,
scaled by that reaction among known members of the true class; no build on file teaches it (task192 carries
class-conditional rates forward, task230 v2 has detection falling with prevalence, neither measures the error per
population from a reaction).

## Survivor anatomy

Actor: whether a machine-classed call was answered by a person has no column in any file; the call detail writes
"answering machine" and nothing more, and the inbound log knows nothing of the detector.

Link: the evidence is the return call, read through the inbound switch's log and matched to the outbound call by the
dialed number and the minutes between them; no call identifier links the two systems, and no document connects
return calls to the detector.

Reflex: the field's method for a classifier's error (the certified rate validated by a hand-checked sample: the
maker's 2.1 per cent, the 2025 listening test's 2.25 per cent) sits at rung 1 and files no project.

Back-test: the 2025 listening test confirms the certified rate on the pilot project, the one population it checked.

Second use: the inbound log carries the completed-interviews ask (interviews done when a household rings the line);
the dialer exports carry all three asks; the register lists the 2027 projects and their lines, which every ask reports
on; the listening audit and the maker's sheet are the firm's own detection records, the setting each project ran at.

Shock: the projects whose detection loses people are the ones whose answering-machine share is already high for
ordinary reasons (older households keep landline answering machines, businesses run voicemail), so their
machine-classed calls read as explained; sorting the projects on any shipped statistic (machine-classed share,
abandoned rate, completion rate, return calls) does not give the golden set as an interval.

Pins: the 2027 dialer policy files the WHAT (the quantity, the limit, the window and the unit); no filed sentence
names return calls, the prompt window or the per-project denominator.

## Readability screen

The reflex row is enumerated from the field's vocabulary for a classifier's error rate (certified accuracy, a
hand-checked sample, the confusion matrix carried across, the class share against a norm), never from the rungs.

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Readable |
|---|---|---|---|---|---|---|---|---|
| 0 dispositions at face value | no | yes (the disposition column) | yes | no | yes | yes | no | readable |
| 1 the maker's certified rate, confirmed by the 2025 listening test | yes (the specification sheet states it) | no | yes (the field's method) | yes (the listening test confirms it) | no | yes | no | readable |
| 2 machine-classed share against the firm's norm | no | yes (one group-by) | yes | no | yes | yes | no | readable |
| 3 return calls at any delay over abandoned calls' returns | no | no | no | no | no | no | no | silent |
| 4 prompt return calls over the pooled abandoned callers' rate | no | no | no | no | no | no | no | silent |
| decisive: prompt return calls over the same project's abandoned callers' prompt rate | no (no sentence names return calls, a window or a denominator) | no (no column links an inbound call to an outbound call, and no marker separates people from machines) | no (the reflex is rung 1) | no (the listening test confirms rung 1 and is silent on every other project) | no (the battery cleans formats, legs and duplicates and stops) | no (a join across two systems by number and minutes, a window read off a two-cluster delay, two rates per project, a ratio) | no (the inbound log carries the completed-interviews ask, the exports every ask) | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternatives | Call under each | Closed by |
|---|---|---|---|---|---|
| SF1 | "classed as answering machines" | every 2026 call whose detector result is machine (the message-played closure, under its pre-upgrade letter code and its post-upgrade word) | only one of the two codes | same call | both codes carry the same detector result column; asserted in `checks.py` |
| SF2 | "on that project" | the call's client job number in the dialer | the caller-ID line's label in the inbound switch | same call | the project register maps each job to its line one to one; asserted |
| SF3 | "in 2026" | calls placed 1 January to 31 December 2026, Central local time, the month-boundary repeat rows dropped | rows kept twice; the window in UTC | same call | the repeated day is an exact copy, every share identical with or without it to the printed unit; asserted |
| SF4 | "a person had answered" | the outcome the estimate is of | (no reading: no field holds it) | not applicable | the stump; no reading, an estimate (the decisive step), recorded here so the judge sees it is not a field |
| SF5 | return call | an inbound call to any company line from the dialed number after the outbound call ended | only to the project's own line | same call | every return in the log lands on the calling project's line; asserted |
| SF6 | which outbound call a return belongs to | the latest outbound call to that number before the return | the first of the day | same call | the dialer's four-hour redial floor leaves one outbound call per number inside any return window; asserted |
| SF7 | how soon a return counts | inside the gap of the two-cluster delay (people within minutes, voicemail returns after the next half hour) | any window from 5 to 40 minutes | same call, same printed shares | C3 corridor: every project's whole-per-cent share identical across 5, 10, 15, 20, 30 and 40 minutes; asserted |
| SF8 | transferred return calls | one return per inbound call, the switch's call id collapsing its legs | one per leg | same call | legs fall alike on returns after machine-classed and after abandoned calls, so the ratio and the call do not move; asserted |
| SF9 | quality-assurance test calls | not returns (they come from the firm's own extensions, never dialed) | kept | same call | no test call matches a dialed number; asserted |
| SF10 | "fewer than one in ten" | strictly under 10 per cent on the unrounded share | at or under; on the rounded share | same call | the nearest project sits more than three points from the limit; asserted |
| SF11 | which projects are in the decision | the recurring projects on the 2027 setup register | every 2026 job, including the one-off study that ended in August | same call (the one-off is not on the register and is outside the call) | the register lists the 2027 projects; asserted |
| SF12 | December calls whose returns fall in January 2027 | counted (the inbound log runs to 14 January 2027) | dropped | same call | the last calls of the year ring on 30 December, so no return inside the window crosses the year; asserted |
| SF13 | rounding | the share computed from counts, rounded once to a whole per cent | each rate rounded to a whole per cent before the division | same call | every golden share at least 0.05 points from a rounding edge, and the early-rounded rates give the same set; asserted |

## Ladder

Measured on the built pack (13 recurring projects, 276,323 answered calls), every rung's set asserted in
`generator/checks.py`.

| Rung | Construction | Projects switched off | Against the golden |
|---|---|---|---|
| 0 | dispositions at face value (a machine is a machine) | none | misses all six |
| 1 | the maker's certified 2.1 per cent, confirmed by the 2025 listening test (2.25 per cent on the pilot) | none | misses all six (the reflex, `Ends on:`) |
| 2 | the projects whose answers the dialer most often classes as machines | the four highest machine-classed shares (large employers, Medicare care experience, veterans' health, retired educators; the fourth 2.7 points above the fifth) | two right, two wrong, four missed |
| 3 | return calls at any delay over the abandoned callers' return rate | every project | six right, seven wrong |
| 4 | prompt return calls over the pooled abandoned callers' prompt rate | five (alumni outcomes falls under the limit at 5.8 per cent, its own callers returning at 9.6 per cent) | one missed |
| golden | prompt return calls over the same project's abandoned callers' prompt rate | six: Medicare care experience, farm operators, alumni outcomes, veterans' health, small business conditions and child care providers (17 to 32 per cent; the nearest on project, cooperative members, at 5.7 per cent) | |

Margins asserted at stage 3: the golden's nearest project to the limit at least 3 points away; rung 4's flip
project at least 2 points under the limit; rung 2's four the top four on the machine-classed share by at least one
point; the golden set not an interval of any shipped per-project statistic (machine-classed share, abandoned rate,
completion rate, inbound volume, sample size). Gate F count: one cheap route lands the call (the golden family);
rungs 0 to 5 and the population-intuition route (older or business populations, which takes retired educators and
large employers and drops none) each file a wrong set.

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | each 2027 project's 2026 machine-classed calls (unobserved members: none, the year is closed) | filed in the 2027 dialer policy; C1 |
| 2 Unit of account | the call | filed (the policy counts calls); C1 |
| 3 Attribution window | calendar 2026 by the call's placement, Central local time | filed; C1 (no project changes at either year edge) |
| 4 As-of dating | the 2026 record as exported in January 2027 | filed by the export dates; C1 |
| 5 Version basis | the post-upgrade export layout and its pre-upgrade twin read as one year | C1 (the detector result column means the same in both) |
| 6 Denominator | the project's machine-classed calls | filed in the policy's sentence; C1 |
| 7 Weighting | none (counts within a project) | C1 |
| 8 Window length | the return window for a prompt return | C3 corridor, 5 to 40 minutes, asserted |
| 9 Boundary inclusivity | strictly fewer than one in ten | filed; C1 (no project within three points) |
| 10 Rounding path | shares computed from counts, rounded once | filed in the prompt's rounding; asserted mid-bin |
| 11 Tie-break | none needed (no two projects tie at the limit) | C1 |
| 12 Maturity and censoring | December's returns land by 15 January 2027 inside the inbound log | C1, asserted |
| 13 Order of operations | collapse legs, drop test calls, match returns, then count | C1 (the order moves no share) |
| 14 Row order | file order | C1, asserted over shuffles |
| 15 Duplicate resolution | the month-boundary repeat rows dropped as exact copies | C1 |
| 16 Identity normalisation | numbers normalised to ten digits across the dialer, the switch and the samples | C4 (raw strings match none of the switch's +1 numbers; normalised they match), asserted |
| 17 Netting against gross | not applicable (no offsetting quantities) | C1 |
| 18 Dimensional units | counts and minutes only | C1 |
| 19 Code and status semantics | the pre-upgrade letter codes and the post-upgrade words, crosswalked by the dialer's own export header note | the code's own crosswalk; never the stump |
| 20 Integerisation | not applicable | C1 |
| 21 Clause scope | the one-in-ten limit is per project per year | filed; C1 |
| 22 Forward window contents | the 2027 projects are the 2026 ones that recur, on the setup register | filed in the register |

## Literal reader

Executed on paper word for word: the policy's sentence fixes the population (each project's 2026 machine-classed
calls), the outcome (a person had answered), the window, the unit and the limit; no shipped field states the
outcome for any call, so every literal reading needs an estimate, and the shipped sentences scope the two ready
figures to their own populations: the specification sheet's 2.1 per cent is "measured on the maker's reference set
of recorded greetings" and the listening test's 9 of 400 is "machine-classed calls on the pilot project, October
2025". Neither is a reading of the policy's quantity for any other project; carried across, each is the easy
method on the same literal estimand (rung 1), not another reading. Every convention the estimate needs is closed
in the fork table, and the only open part is the method, forced by the data: the return calls after machine-classed
hang-ups exceed by many times what 2.1 per cent could produce on six projects, the abandoned callers' prompt return
rates differ across projects far beyond their sampling error, and the return delays fall into two clusters with a
gap between them. Pass.

## Oracles

- The pilot project: the 2025 listening test's 9 of 400 (2.25 per cent, a 95 per cent interval of about 1.0 to 4.2)
  against the 2026 return-call estimate on the same project, 3.1 per cent: inside the interval, and the
  only project where the certified route and the golden route meet.
- The clean truth in the generator: each project's true share of machine-classed calls answered by a person,
  against the golden estimate, within its sampling interval and on the same side of the limit, asserted.
- The delay profile: the share of returns after abandoned calls arriving inside the corridor equals the same share
  after machine-classed calls on the projects with many people among them, as the shared recorded message implies.

## Ask sheet

Three asks, each per project (every recurring project in both rows), each a reconstruction across two systems or
grains no sentence states, sited on quantities the main-call files cannot compute, none touching the main
population's construction.

**Ask A, calling hours.** Each project's 2026 answered calls that rang before 8 am or after 9 pm in the called
household's own local time (the 2027 policy's section 2, the register's calling-days column). Use: the director's
2027 dialing windows and the exceptions the policy has reported to her. Primary device D7 (the true key elsewhere): a
respondent who asks to be called back on another of the household's lines at a time they name gets an appointment
the interviewer dials in preview mode, to a number the client's case record does not hold; some of those lines are
kept from an earlier home and carry another state's area code, but they ring at the household. The household is the
case: from July the dialer writes the case record's own case number, and before July (the old case numbers are in no
record) the case is reached only through the same case's calls to its recorded number. Hazard D8: Arizona keeps
standard time all year (`state_time_zones.csv`). Hazards: the month-boundary repeats, three number formats. Files: the
twelve exports, `case_records_2026.csv`, `state_time_zones.csv`; 8 columns on the path. Stops: area codes for every
number; the record by number with area codes for the rest and Arizona on daylight time (the mirror); the record by
number, then the July case number, area codes for what is left (the careful route); the record through the case before
July (golden). Pin test: the asking sentence carries the rule and the year; the device sits in which record is the
household's, which the pins leave open, and the policy files the clock (the household's own local time), never the key.

**Ask B, completed interviews.** Each project's interviews completed in 2026. Use: the 2027 quotas and the client
reporting. Primary device D4 (absence evidenced in a file no habitual join reaches): a household that rings the line to
do its interview is answered by the desk and, four times in five, handed to an interviewer on a second leg; the switch
writes TRANSFER on the first leg and COMPLETE on the leg that ends the call, so the call table the main call builds
(first legs, one per switch call id) holds none of them. Second primary D1 (one record under two key schemes): a
supervisor's verification call on a completed case closes it as complete again under a new call id, and the July
upgrade renumbered the cases, so a case completed before July and verified after it carries two case numbers that only
its case record makes one. Hazard: the month-boundary repeats. Control that agrees with the wrong read: the client
invoices, built from the dialer's completed rows. The policy's section 5 files the WHAT (an interview counts once, when
it is completed) and names neither the legs nor the renumbering. Stops: the dialer's completed rows (ties to the
invoices, the mirror); once per case number; plus the line's completes read on first legs (the careful route); plus
completes on any leg, each case once through its record (golden).

**Ask C, interviewer hours.** Each project's 2026 interviewer hours, to one decimal. Use: the 2027 staffing of each
project, which switching detection off changes. The policy's section 5 files the allocation (a shift's hours shared by
each project's talk and wrap time in that shift, a shift with no calls not charged), so the allocation is a work order
and carries no device. Primary device D3 (units set per source and date): the payroll's timekeeping system changed in
July, and its export writes hours as hours.minutes (4.30 is four and a half hours) where the old one wrote decimal
hours; the rows read as decimals without an error. The evidence is internal: the new rows' fractions never pass .45
while the old rows run .25 to .75 on the same shifts, and read as decimals the July to December shifts end before
their own last calls. Hazards: training shifts booked to a project code with no calls (filed); the two layouts'
headers, date and job-code formats; shifts that worked two projects under the first one's code (the filed
allocation). Stops: hours by code read as decimals (the mirror); hours by code read right; the allocation read as
decimals (the careful route); the allocation read right (golden).

Main population zero-counts (asserted in `checks.py` from the shipped rows): no appointment number carries a
machine-classed or abandoned call; no verification call is machine-classed or abandoned; no inbound interview is a
return call; deleting every ask device leaves every share identical. The month-boundary repeats and the formats are
hazards the main shares are asserted not to move.

| Ask | What the cracker does | Cracker |
|---|---|---|
| A | the case record by the number dialed, the July case number for the rest, the area code for what is left; Arizona on standard time | misses |
| B | the dialer's completed rows once per case number, plus the line's completed calls read on their first leg | misses |
| C | the policy's allocation by talk and wrap time in each shift, July to December read as decimal hours | misses |

Measured by: `generator/ceiling.py` on the cut pack (stage 3), and every route's figure-by-figure gap asserted in
`generator/checks.py`.

| Ask | Graded figures | Cracker keeps | Mirror keeps | Cracker |
|---|---|---|---|---|
| A calling hours | 13 | 0 | 0 | misses |
| B completed interviews | 13 | 0 | 0 | misses |
| C interviewer hours | 13 | 0 | 0 | misses |

On the cut pack the cracker keeps none of the 39 ask figures and the mirror none. The gaps `checks.py` asserts and
prints: ask A's careful route misses every project, and so do the area-code route, the route that drops the calls it
cannot place and the golden route with Arizona on daylight time; ask B's careful route misses by 55 to 126
interviews and the invoiced count by 30 to 82; ask C's careful route misses by 50.0 to 138.7 hours, the hours by code
read right by 9.5 to 206.4 and the allocation with the training shifts charged by 32.5 to 80.0. The full includer
who reconstructs every device lands the asks; the sheet prices the careful route short of the reconstructions, as
the cracker is defined. With the call landed at 38 plus 7 and the best miss at 5 plus 7, the pair is
(45 + 55 x 0.000 + 12 + 55 x 0.000) / 2.

Pair ceiling: 28.5.
Mirror leakage: 0.0 per cent of ask weight.

## Tried and rejected

- The seed's pitfall (one raking pass against raking to convergence): executing a filed procedure, rule application;
  dropped at the draw.
- The seed's survey world: the pairing is banned against task240; dropped at the draw.
- A surveillance completeness check by capture-recapture with dependent sources (epidemiology): task236 already reads
  a capture rate against an independent sample; too close; dropped at the draw.
- A laboratory calibration curve's weighting (weighted against unweighted least squares): either the weighting is
  filed (rule application) or two least-squares readings stay open (a fork); dropped at the draw.
- A westward gradient of 0.0042 per degree at 6.8 degrees: the pooled-reference rung sat within 0.0002 of the
  tolerance on two floats and could collapse onto the golden; raised to 0.0060.
- Floats free to reach the box's edges, casts only inside it: nearest-cast mappings for edge floats were one-sided and
  the corridor ended at a 4 degree radius; floats now turn back inside the recirculation and the casts extend past
  them, so the corridor reaches 5 degrees.
- A pressure-level default on 50 dbar standard levels with profiles dropped unless they spanned the layer: a third of
  the profiles fell out on the levels' jitter; the default now differences each good value at its own pressure.
- Three partner floats: their on-time profiles cancelled the profile-time anchor in three months for a solver making
  both mistakes; one partner float, and the Argos latency drawn from 8 to 26 hours.
- A drifting sensor free to start drifting late in 2027: one drifting float's 2027 mean fell under the tolerance;
  drift now starts between July and November 2026 in a float in the water for a year or more.
- RHD casts ending at 1,980 m: 2,005 dbar by Saunders (1981) but 1,999.8 by the 1.01 rule of thumb, so the conversion
  chose the count (leak reader); the extract's deepest levels now sit clear of 1,962 to 1,981 m and the reference note
  names the database's conversion.
- One 10 m grid for every RHD institute and three deepest values across the archive read as generated (leak reader);
  each institute now submits on its own grid, and archive casts stop where the plan or the bottom stopped them.
- Resent Iridium files exactly ten days after the first, the year's first descent exactly ten days before the next,
  engineering values with no ageing, and no temperature or pressure value ever flagged (leak reader): the resend now
  comes with the float's next profile, the battery ages, and spikes are flagged in all three variables.
- The fixed-pressure and pooled-reference rungs quoted as single counts (15 and 13): the judge measured 14 and 12 with
  its own implementations (finding 2); the write-up now quotes the measured ranges over each family (13 to 17, 10 to
  14), asserted in `checks.py`.
- A second read found the institute's cruises all starting on the hour and one section on an exact latitude step; both
  now come from a separate random stream (station keeping and the first station's time), so nothing else moved, and
  the estimator reads a receipt in the repeated October hour in the pass that keeps it after its own surfacing (the
  counts were the same either way).
- Architecture 1, at the 11-01 re-check: the clean-truth analyst test holds (fixed pressure 15, nearest casts at fixed pressure 13, pooled temperature levels 12, drift 4, the decisive step alone the six), but the survivor anatomy written honestly fails Reflex, Back-test and Shock: the golden is the field's own delayed-mode calibration (potential-temperature levels mapped to the float's position) applied as the textbook states it, so the opponent's first move lands the call (stumping 1.1b; precut's method-family list misses this field's vocabulary, so its check passed lexically), and the six are the top six of the pooled rung's sort. Spent; not re-rooted on the orchestrating session's rule.
- Architecture 2 draw, 2026-11-02 (the re-root the orchestrating session asked for after the 11-01 re-check; moved off Physical & Environmental Sciences and ocean and float data, same objective and number): 21 candidates screened across seven task types (product-analytics metric-definition-measurement-science, general-statistics missing-data-censoring-measurement-error, survey-research census-register-administrative-data-quality and nonresponse-calibration-measurement-error-adjustment, epidemiology disease-surveillance, psychology psychometric-measurement-scale-validation, and official-statistics admin and price collection under the survey task types). None cleared the three rules and the screens, so the slot is PAUSED on the orchestrating session's rule (twelve screened across three task types). Bans in force at the draw: strategies population_selection, causal_design and composition_mix (task273, task157, task166), shape 10 (task157), forums minister_or_cabinet, customer_or_counterparty and auditor, forcing events season_or_peak, incident_or_complaint and period_close, org families government_agency, local_government and media_or_publishing. One line each:
- A2.1 Survey interviewers' fabricated interviews read from the travel time between consecutive addresses (survey measurement error): finding fabricated records is the client's planted-defect class, and the call retags as Anomaly Detection.
- A2.2 Price collectors' accepted pre-filled prices read from chain-wide price moves at sister outlets (price collection): the copied-readings block the client names as a planted defect.
- A2.3 Interviewer variance separated from area variance on the cases the case management system reassigned (survey measurement error): a random effect added to a fitted specification, which the bin test closes as a class by identity (determinism-check).
- A2.4 A mobile app build's event loss at crashes, read from the crash reports' breadcrumb trails (product analytics): task235's world and call (builds, tracking-loss alerts, events held on the phone).
- A2.5 An autocoder's error rate read from a quality sample drawn by confidence band (census coding): task230's world (the census occupation autocoder) and the selection-into-checks family (task229 v2, task251 v3).
- A2.6 Death registration completeness by the general growth balance with a residence correction (census and registers): task243.
- A2.7 Feed gaps that every source behind one gateway shows in the same minute: task303's approved driver in other nouns.
- A2.8 Training-serving skew read from paired online and offline features of the same request (general statistics): the paired comparison is the field's own standard, so the golden is the reflex.
- A2.9 Age heaping by Whipple's index against a real cohort bump (census demography): the precondition is broken by the population, not by the organisation's systems, and the refined digit-preference indices are the field's own methods.
- A2.10 Small areas misallocated by postcode-centroid geocodes, read from the address register's split of each postcode (census and registers): the expected misallocation needs an unfiled within-postcode distribution, a fork on the graded figure.
- A2.11 Alert-rule precision when auto-resolved alerts are never investigated (product analytics): filing "a real defect" computably makes the step rule application, and leaving it unfiled forks the unlabelled alerts.
- A2.12 Freshness SLO breaches hidden by probes phase-locked to each table's load cycle (general statistics, missing data): all seven anatomy lines hold on paper, but the decisive move (rebuild the age accrued since each load) is task229 v2's "rebuilt from the accrual since its last count", landed, and task251's architecture 5 screen set the same aliasing aside.
- A2.13 Census tablets' unsynced forms lost at re-images, read by bracketing each re-image between the last synced form and the next form in listing order (census operations): the prototype on the clean truth (20 worlds, 24 supervision areas each, a session prototype that was not kept in the pack) puts serial accountability, the listing reconciliation and the internal listing gaps on the true flagged set 0 of 20 times, the bracketing 19 of 20 and a productivity model 2 of 20; it dies on the swap test (a utility's meter readers' handhelds read the same), so the domain is a backdrop, and the truth flags 17 to 19 of 24 areas at a 0.5 per cent tolerance without retuning.
- A2.14 Hospital coding depth standardised on a case-mix that is itself derived from the coding (administrative health data): task236's insight (an adjustment the defect itself moves), and its honest label, composition_mix, is banned against task166.
- A2.15 A laboratory feed's capture read from the clinics that moved their testing to it (disease surveillance): a within-lab drill-down by ordering provider reaches the lossy lab's drop (Link fails), the losing lab's fall is the pack's largest move (Shock fails), and the honest label causal_design is banned against task157.
- A2.16 An audit's error rate under a two-stage stopping rule (general statistics): the likelihood estimate and the unbiased estimate disagree on the graded figure, a fork.
- A2.17 Equating-chain drift caught through items rested since the base form (psychometrics): task450's and task123's anchor-drift family, and the standard linking methods fork the cut.
- A2.18 Routine health information completeness when the platform stores no zeros (disease surveillance, DHIS2): data semantics.
- A2.19 Source outages read from processed counts plus the ingestion queue's backlog change (product analytics): task120's approved stock-flow identity.
- A2.20 Payroll software defects read by the Hidiroglou-Berthelot ratio method within industry (official statistics, admin data): the comparison group is composition_mix (banned) and the method is named.
- A2.21 A laboratory's message loss at interface restarts read against its monthly volume report (disease surveillance): one subtraction against a filed total, readable.
- The four strongest written in full, as the orchestrating session asked. A2.13: default path, per-tablet serial accountability (the census's questionnaire accountability) and the sync server's accountability report agree and flag none of the areas the truth flags; swap fails (meter readers); anatomy: Actor, Link (the re-image's time against the forms' timeline), Reflex, Back-test (the server report reconciles), Second use and Pins hold, Shock open (re-images cluster where a faulty batch went); bin: records-fixed bracketing against a productivity model that disagrees in 18 of 20 worlds, an implementation corridor to close. A2.12: default path, the share of probe readings over the limit; swap of the method holds; all seven anatomy lines hold; bin records-fixed; spent driver. A2.14: default path, coding depth against the national rate within each case-mix group, which reads the under-coding trusts as normal; swap holds; Link holds only in part (the administrative fields are columns); bin exact indirect standardisation; spent insight and banned label. A2.15: default path, each lab's quarter against its seasonal baseline, which alerts the lab that lost clinics and misses the lossy lab that gained them; swap holds; Link and Shock fail; bin a ratio estimator with a corridor; banned label.
- Architecture 2 draw, 2026-11-03 (continuing the 11-02 screen after it cleared nothing; the guard window then held task173, task479 and task188, so decomposition_attribution, binding_constraint and population_selection, the patterns G5, G3 and G14 and the operations-log artifact were banned): 22 more candidates, one line each, the last carded.
- A3.1 Parcel hubs' unscanned share placed by the trailer's departure from the hub before (supply chain, general statistics): every honest label is banned (population_selection or decomposition_attribution, G3, the operations log) and the signature (population, G3) repeats task270 v8 and task464 inside the last twelve.
- A3.2 Blood-pressure terminal-digit preference under a device mix: shallow, a field reading, and task246's measurer offsets.
- A3.3 Bounds for suppressed census cells by linear programming: the WHAT screen (the bound filed is the answer) and a fork on which bound.
- A3.4 Annotators anchored on pre-filled labels: Gate F (the anchoring check is the reflex) and task238's ground.
- A3.5 The seam effect in a rotating panel: the field's own method (the seam-adjusted transition rate) is the golden, the reflex at the top of the ladder.
- A3.6 Filter-question misreporting and diary fatigue: both settle the outcome or the window (WHAT screen).
- A3.7 Prorating a nine-item scale's missing item: multiple imputation is the reflex and the golden.
- A3.8 Pooled PCR dilution with Ct truncation, and post-processing bias from a privacy mechanism: neither has a determinate figure across defensible estimators.
- A3.9 Batching noise in weekly reports: retags as Anomaly Detection and is the overdispersed funnel task183 and task194 measured dead.
- A3.10 Exposure-based alert floors: the reflex reaches it, and the call retags as Forecasting.
- A3.11 Supplier-statement mismatches as the error rate of straight-through invoices, matched on vendor, amount and date (accounts payable): the supplier statement is an independent reference, task236's move.
- A3.12 An analyser's carryover read from each specimen's predecessor in run order (laboratory data): task252 architecture 1's driver and task184's screen.
- A3.13 Laboratory bias from patients tested at two laboratories against non-commutable quality-assessment material: task200 measured the split-specimen network dead (additive offsets collapse to a group-by, offset and scale fork the share).
- A3.14 Trial sites' adverse-event under-reporting against a front-loaded hazard by infusion number: task228's screen (a stratification by time on study) and the grouping dichotomy.
- A3.15 Reinterview response variance swollen by true change that grows with the reinterview lag: task244's organ, and the fork-is-the-stump test (filing "the same true situation" names the step, leaving it unfiled forks the index).
- A3.16 Subscores' added value with passage-level dependence: task270 architecture 4 and task237's driver.
- A3.17 Comorbidity under-coding found by bracketing an admission between the patient's coded admissions: task188's screen of a look-back through the patient's admissions elsewhere.
- A3.18 Practice effects in a cognitive panel identified from missed waves: task270 architecture 3 died when the filed outcome named the practice effect, and task280 screened it.
- A3.19 Women's ages displaced over the eligibility boundary, controlled by men's ages in the same households: interviewer falsification is the planted-defect class (A2.1).
- A3.20 Mirror trade asymmetries reconciled through a hub's re-exports: the origin and consignment conventions make it a field reading, and the honest label, decomposition_attribution, is banned.
- A3.21 A short form's validity inflated by part-whole overlap with the long form: retags as Descriptive, and the corrected correlation forks on the reliability estimator.
- A3.22 Answering machine detection's false-machine share per project, from the calls people return within minutes of the hang-up over the same project's abandoned callers' prompt return rate (a survey research firm's telephone centre, general statistics): carded as architecture 2. The prototype on the clean truth (13 projects, 283,000 answered calls, 60 seeds) puts the golden on the true set 60 of 60 times, the certified rate, the raw return-call share and the all-delay ratio 0 of 60, the closest golden share 1.1 points from the limit; guard.py check WARN (repeat.decision), the structural tests differentiated against task281, task454 and task468 v1.
- A3.23 Ask C on the shift allocation (a multi-project shift under its first project's code): the 2027 policy's section 5 files the allocation by talk and wrap time, so the pin names the device's dimension and the careful route executing it kept all 13 hours; re-sited to the payroll's July change to hours.minutes, the allocation left as a work order.
- A3.24 Ask A on the number's area code against the case record's address: the record's address_state is one join away from every dialed number, so the careful route that joins it kept all 13; re-sited to appointment numbers the record does not hold, reached through the case (the July case number, and before July the case's own calls). Without appointments after 9 pm the route that drops the unplaced calls kept 9 of 13, so respondents now also name times after the evening session.
- A3.25 Ask B's invoiced count against the golden: the verification calls' extra completed rows and the inbound completes the dialer never sees offset, the invoices tying to the golden on one project to the interview (no subset of mishandlings may compose back); the inbound completes were thinned and handed to a second leg four times in five.
- A3.26 The golden six an interval of interviewer hours, answered calls and line volume (the six call populations that answer with long greetings also had the fewer live calls): the projects' sizes and two populations' voicemail return rates redrawn so every shipped per-project statistic interleaves the two groups.
- A3.27 Shares within 0.02 points of a whole-per-cent rounding edge on most seeds: the seed is drawn by a search over the main call's own criteria (the six, rung 4 dropping one, rung 2's four, the pilot inside the 2025 audit's interval, no interval of any per-project statistic, the 5 to 40 minute corridor, the nearest share over three points from the limit) for the widest rounding margin; the random streams of staffing, returns, verification calls and late appointments were split so the ask devices never move the main call.

