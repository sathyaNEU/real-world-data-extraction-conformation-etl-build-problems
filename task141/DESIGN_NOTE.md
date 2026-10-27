# task141: Okelan County, felony probation revocations under the 24-month cap (architecture 3)

Private, never ships. Architecture 3 of task141, re-rooted on 2026-10-27 at the author's instruction (oviya1301) to
give the number a stronger stump: architecture 1 (Dorrance County's presumptive release tier) went FAILED_TO_STUMP on
the portal, both responses landing it, and architecture 2 (the bed-day bill of the county's pretrial releases) was
superseded at stage 2, its decisive construction being one join and a sum once seen. The number, the Forecasting lane
and the client domain are kept; the world, the records and the decision are new. Both earlier architectures are under
`## Earlier architectures`.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task141.json`, architecture v3; `guard.py check` WARN only (`three_rules.strategy_risk`, answered below) with one NOTE (task152, differentiated on the card); architectures 1 and 2 in `lineage` with their fates |
| Domain / task type | `criminology-justice` (client domain), task type `recidivism-risk-assessment`, the only one in the domain that serves Forecasting: the 2027 count of felony probation revocations, forecast from the county's own supervision record |
| Objective | Forecasting & Predictive Modeling: the felony probation revocation commitments the Detention Center will admit in calendar 2027, a window not yet open at the extract (30 September 2026), under a statute that takes effect on 1 January 2027 |
| Shape | `02` (forecast across periods): the plan's quarterly admissions and their two parts carry the call's criteria, the asks the rest; the arithmetic goes under `## Ask sheet` at stage 2 |
| Decision | `quantity_figure` (the plan's 2027 admissions, from which the filed planning standard sets the violator pods), answer unit `count` |
| Mechanism | gap time (decisive: the record's petitions were made under terms that ended where they were set; the Act moves every end and ends some 2,900 running terms on one day) then population (the terms past 24 months are a block no new term will form); pattern none, generators G4 (attribution at the transition: which clock each petition rides) then G13 (the forecast horizon holds a transition the window never exercised); Gate G `forecasting`; strategy `time_semantics` |
| Layer 2 family / pattern | `estimation_fit` (the data's real structure: which clock an event rides); `own:violation-petitions-filed-before-each-term-lapses-ride-the-scheduled-end`. The client library's recidivism cards (calibration, fixed follow-up and time at risk, the fairness criterion, later release cohorts, selective labels, local base rates) are the default path's own careful moves here: the survival projection by time on supervision with the risk score is card 2 and card 4 done well, and it files three pods |
| Furniture | forum `council_or_assembly` (the County Board of Supervisors adopts the plan), forcing event `statutory_or_regulatory_filing` (the 2027 Jail Operations Plan is due to the State Jail Standards Board on 1 December 2026), organisation family `local_government`, role family `research_desk` (the Sheriff's Office jail planning analyst), context artifact `filed_standard` (the Board's planning instructions with the county's pod standard, and the Act), calibration `none`, opening `question-first`, question form `how-many`. The live window at the draw (task139 v2, task304, task166) carries none of the forum, forcing event, organisation family or role |
| Spine | `detention_bookings_2019_2026.csv`, the Detention Center's bookings (every booking, a transfer to the annex writing a new row), with the booking reason that marks a revocation commitment; rows set at stage 3; synthetic |
| Deliverables | `violator_housing_plan_2027.xlsx` (the forecast by quarter and part, the pods), `violator_housing_memo_2027.docx` (the plan's violator housing section), `felony_revocation_admissions_2019_2027.png` (monthly admissions and the forecast) |
| People | drawn with `guard.py names --geo us --seed 141 --n 30`, skipping every first name the guard warns on: Gina Yoder (Sheriff's Office jail planning analyst, the requester), Larry Pugh (Chief Probation Officer), Colleen Cameron (Detention Center commander), Donald Russo (Probation research and data manager), Megan Chambers (Clerk of the Circuit Court), Gloria Lynch (County Budget Director); none appears in the prompt |

**Guard.** The first probe (decisive G7, role `capacity_planner`, forcing `purchase_order_or_contract`) BLOCKed on
`ban.role` and `ban.forcing_event` against task137 v4 and on `test.same_puzzle_older` and `test.same_driver_older`
against seven builds; decisive G13 BLOCKed `ban.pattern` against task166 v3; `dial_setting` BLOCKed `test.same_puzzle`
inside the batch against task269 v1's lineage. The card reads the honest replacements: the jail planning analyst is a
research desk, the plan is a statutory filing, G4 names the attribution the stump turns on (each petition to the clock
it rides, at the transition the Act makes), and the committed answer is the forecast count from which the pods follow.
`three_rules.strategy_risk` WARNs that `time_semantics` often decides on reading a field or a stated rule: here no
field or rule carries the clock; it is a process in the record estimated by the field's hazard method from every term
that reached its end (`## Three rules`, Not semantics and Not rule application). Strategies `causal_design` (task139
v2) and `composition_mix` (task304) were barred by the window, which ruled out the supervision-intensity designs.
`people.first` WARNs on Robert, Jessica, Amanda, Justin, Anthony, Richard, Ryan, Lori and Michael were redrawn.

**Same-puzzle test.** Gap time, decisive G4, `quantity_figure`: task152 alone carries the triple, a solar plant's
decline at a module replacement split into wear the replacement removes and dust it keeps; nothing here is replaced
or decomposed into a kept and a removed loss: events tied to each term's scheduled end move with the end a statute
sets and fire together for the terms it ends on one day.

**Abstraction test.** Stripped of nouns: failures are filed at two moments of each unit's term, early on and at a
review held as the term lapses, so the failure rate by time since entry carries a spike at each term's own end; a cap
that moves every end earlier moves the review with it and fires it at once for every unit already past the cap, while
a forecast that truncates the time-since-entry curve at the cap drops the spike and files a fall. The nearest drivers
on file (0.09 and under): task134 v2's lineage (inflow from a pool held outside the register), task123 v1's lineage (a
trailing total over periods an annual filing closes), task62's lineage (an exclusion limited to an instrument's term)
and task304 (entries into failure from units whose good standing an organisation produced). None has events riding
each unit's scheduled end, and none has a transition that moves every end and fires the events together. task169 (a
parole act rerouting arrests the Board had revoked to the courts) is the nearest build in the domain: its insight is a
processing route the act closes, measured by the conversion the remaining route applies; nothing here is rerouted.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting` (every spent driver on the
objective): no build reads a second clock tied to each unit's scheduled end. `guard.py slots expiration "term end"
lapse anniversary`: task123's slot only, on an annual filing; `slots "max date" "remaining sentence" "earned credit"`:
none. task169's `## Tried and rejected` set aside a discontinuity at a supervision-tier cut-off (a logistic with the
tier lands it) and positive tests per sanction step (a filed grid), both read and avoided. task141's own portal
diagnosis (every large lever in the pretrial world is a counterfactual for a held defendant) moved the decision to a
population whose outcomes the record holds whole: the supervision record is complete for every case to the extract.
`layer2-rigor-patterns.md`, recidivism-risk-assessment: cards 2 and 4 are the default path's careful moves; card 5's
selective labels cannot arise (no decision-maker chooses who is supervised).

**World.** Okelan County (fictional, an unnamed state) supervises about 8,300 felony probationers through its Adult
Probation Department. Under the State's 2019 realignment a felony probation revocation term is served in the county
of supervision, so every felony revocation is a commitment to the Okelan County Detention Center, booked under its
own reason code. Felony terms are set by the sentencing judge, 18 to 72 months; a misdemeanor term is 12 months.
Officers file violation petitions with the Circuit Court: on new arrests, missed reporting, failed drug tests and
treatment failures through the term, and, in the weeks before a term expires, on matters still unresolved (unpaid
restitution, a pending charge, unfinished treatment, a probationer who cannot be found), because a petition filed
before expiration keeps the court's jurisdiction. Senate Bill 26-118, the Felony Probation Term Act, takes effect on 1
January 2027: a felony term imposed on or after that day may not exceed 24 months, and a running term ends on the
earlier of its original expiration and 24 months from its start, but not before 31 March 2027. The Sheriff's Office
writes the 2027 Jail Operations Plan, which the County Board of Supervisors adopts and files with the State Jail
Standards Board by 1 December 2026; the plan states the felony probation revocation admissions it expects in 2027 and
staffs violator pods by the county's filed standard. Records to the extract of 30 September 2026.

**Data-native sentence.** In Okelan County's record about a fifth of felony violation petitions are filed in the last
75 days before a term's scheduled expiration, on matters left unresolved as the term lapses, so that the court keeps
jurisdiction: 23 to 24 per cent of terms that reach their last 90 days on supervision carry one, against 3 per cent in
the same stretch a year earlier. SB 26-118 moves every scheduled expiration and puts some 2,900 of them on 31 March
2027.

## Three rules

- Task type: criminology-justice, recidivism-risk-assessment (serves Forecasting): the 2027 count of felony probation
  revocations the Okelan County Detention Center will admit under SB 26-118, forecast from the county's supervision
  record.
- Domain test: the deciding quantity is the forecast count of revocations, which the field projects from failure on
  supervision (the hazard of a violation by time on supervision and risk, the share of petitions that end in a
  revocation, the time from petition to commitment); it turns on probation law's tolling: a petition filed before a
  term expires keeps the court's jurisdiction, so officers file on unresolved matters in the weeks before each
  scheduled expiration, a second clock that carries about a fifth of the county's felony petitions.
- Swap: "a gym chain forecasting 2027 cancellations after a cap on contract length" keeps a term and a cap, but
  nothing in it is filed to keep an authority over a member before the term lapses, a cancellation at the end is the
  term's own end rather than a filing that extends it, and no transition ends thousands of running contracts on one
  day, so the reasoning that decides (which clock the petitions ride and where the Act moves it) has no counterpart.
- Layer 1: the two case-management systems' layouts (the legacy one to June 2023 with terms in days and its own status
  and office codes, the new one in months), amended petitions under the original number with a suffix, the Detention
  Center's bookings with annex transfers as new rows and UTC times after its 2025 migration, the person crosswalk
  across Probation, Sheriff and State identifiers with merged identities, misdemeanor and interstate-compact cases in
  the same register, and the risk screen's 2023 rescaling; each is what the named system produces, and none decides
  the call.
- Layer 2: family `estimation_fit`; the choice that flips the call is reading the record's petitions on two clocks,
  months on supervision for the ordinary ones and days to scheduled expiration for those filed as a term lapses, and
  moving the second clock to the end the Act sets.
- Decisive step: in the field's words, a revocation forecast built on the hazard by time on supervision has to
  separate the petitions filed against the expiring term (the tolling petitions in the last weeks before scheduled
  expiration) from the time-on-supervision violations, because the Act moves every scheduled expiration and ends some
  2,900 running terms on one day, and the tolling petitions follow the end.
- Not semantics: every field, code and date read correctly (allegation codes, dispositions, booking reasons, the
  Act's sections) still leaves the time-on-supervision forecast at about 450; no column, code or status marks a
  petition as filed against the expiring term (its allegations are the codes the ordinary petitions carry), and the
  clock appears only when filing dates are aligned on each term's scheduled expiration.
- Not rule application: SB 26-118 sets every term's new end and the planning standard turns admissions into pods, and
  executing both on the time-on-supervision projection files three pods; no rule or document names a petition clock,
  a window or a rate. Measured on three paper worlds (`generator/paper/fam.py` on `sim_rev.py`): the enumerated family
  (persistence, the time-on-supervision hazard pooled or by term length with the score, the two-clock forecast without
  the transition terms, the two-clock forecast, and the end window counted twice) spreads from 0.44 to 1.12 times the
  truth, 413 to 1,067 admissions; the standing family (two clocks, the window 60, 90 or 120 days, the score on or off)
  spreads by under 1 per cent of the figure on each world (968 to 1,008 across the three); the ruling-out is one
  group-by nothing invites, petitions by days to the term's scheduled expiration, where 23 to 24 per cent of terms
  that reach their last 90 days on supervision carry one against 3 per cent in the same stretch a year earlier.
- Analyst test: a strong analyst who conforms the two layouts, the petitions and the commitments, applies the Act to
  every term and fits revocation by month on supervision with the risk score (the field's survival projection),
  carrying each case to its new end and adding new starts on 24-month terms, files about 450 admissions (Ends on; a
  fall of a third from the trailing year's about 700), against the golden's about 950; persistence files about 700.
- Estimand: felony probation revocation commitments admitted to the Okelan County Detention Center with an admission
  date in calendar 2027, for felony cases Okelan County supervises, under SB 26-118 as enacted, with the courts, the
  Department and the Sheriff acting at the rates the record shows (the planning instructions' projection convention);
  filed in `jail_planning_standard_2026.pdf`.
- No decoy: nothing is planted; the petitions filed before a term lapses are what tolling makes officers do,
  generated by one process for every term; no memo, briefing, draft or stakeholder figure forecasts revocations, and
  the Department's annual report counts last year's admissions only.
- No certified replay: no certified, published or prior-period figure is reproduced to recover a method; nothing in
  the pack forecasts 2027 or scores a method.
- Lesson: an event filed against a term's scheduled end rides that end, not the time since the term began; a reform
  that moves every end moves those events, and a transition that ends thousands of terms on one day fires them
  together. No build on file reads a second clock tied to each unit's scheduled end, or a transition that fires it.

## Default path

1. Read SB 26-118's sections and the planning instructions: the plan carries the felony probation revocation
   commitments admitted in 2027 and staffs violator pods by the county's standard.
2. Conform the probation register (the legacy and new layouts), the petitions (amendments collapsed) and the Detention
   Center's bookings (annex transfers joined into stays, times to local), linked through the crosswalk; keep felony
   cases Okelan County supervises.
3. Set each case's end of supervision under the Act: new terms 24 months; a running term at the earlier of its
   original expiration and 24 months from start, not before 31 March 2027.
4. Fit the field's survival model of revocation by month on supervision with the risk score (a discrete-time hazard,
   censored at closure and the extract); stratifying by term length leaves it where it is.
5. Carry each active case month by month to its new end, add new starts at the trailing year's rate on 24-month terms
   and the petitions pending at the extract at their conversion rate.
6. Sum the commitments dated in 2027: about 450 (459, 449 and 456 on the three paper worlds), a fall of a third, three
   pods.

Ends on: about 450 felony probation revocation admissions in 2027 (three pods; the trailing year carried about 700).
Golden: about 950 (six pods): about a fifth of the record's felony petitions are filed in the last 75 days before a
term's scheduled expiration and ride that end, and under the Act the ends of some 2,900 running terms fall on 31 March
2027, so their petitions and about 300 commitments come in the first half of 2027, on top of the terms reaching 24
months through the year.

## Stump sentence

A competent solver fits revocation by month on supervision with the risk score, carries it over each felony case's
2027 months to its new end under SB 26-118 and files about 450 admissions (Ends on; three pods); the step that lands
it there is reading every petition on the time-since-start clock, when about a fifth are filed in the last weeks
before a term lapses, ride each term's scheduled end, and under the Act fire at once for the terms that end on 31
March 2027, so the plan carries about 950 (six pods).

## Paper world

`generator/paper/sim_rev.py`: a county's felony and misdemeanor probation cases from January 2017 to the extract
(about 210 felony and 150 misdemeanor starts a month, felony terms 18 to 72 months), ordinary petitions on a monthly
hazard that falls from 3.0 to 0.75 per cent over the first year and a half and scales with the risk score, a petition
filed between 6 and 75 days before a term's scheduled expiration on 22 per cent of terms that reach their last 90 days
with none pending, 48 and 50 per cent of the two kinds ending in a commitment some 72 days after filing on average,
early termination for compliant cases after 18 months and a small absconding hazard. The truth is the generator re-run
from every case's state at the extract under the Act, eight times. `generator/paper/routes.py` computes each route
from the record alone and `fam.py` runs them.

| World (seed) | Truth | Persistence | Time on supervision | By term length | Two clocks without the 31 March terms | Two clocks (golden) | End window counted twice |
|---|---|---|---|---|---|---|---|
| 1 | 949 | 694 (0.73) | 459 (0.48) | 423 (0.45) | 667 (0.70) | 1,008 (1.06) | 1,067 (1.12) |
| 2 | 917 | 715 (0.78) | 449 (0.49) | 420 (0.46) | 644 (0.70) | 969 (1.06) | 1,025 (1.12) |
| 3 | 948 | 692 (0.73) | 456 (0.48) | 413 (0.44) | 660 (0.70) | 982 (1.04) | 1,037 (1.09) |

The golden's members (the window 60, 90 or 120 days, the score on or off) run 1,000 to 1,008, 968 to 973 and 978 to
983. Its 4 to 6 per cent above the truth is the projection's monthly discretisation (the same formula with the
generator's own parameters sits 5 per cent above a Monte Carlo of new starts), and the time-on-supervision route's
error is ten times that. Stage 2 tunes the world so that the golden and every wrong route sit mid-bin under the pod
standard and measures the family again on the built pack.

## Earlier architectures (kept as history)

**Architecture 2 (drawn 2026-10-26, superseded at stage 2 on 2026-10-27).** Dorrance County's detention bed-day bill
of the pretrial releases it already makes: the default path priced a release at its own short stay (about 3,213
bed-days a year), the golden at the custody of the booking that follows a failure to appear (13,358 a year, 85.6 per
cent of it on charges the policy's eligibility list excludes). Drawn and registered by another session (f33106e5); its
stage 2 reached `precut.py` one FAIL short, the asks not yet redrawn, at 31378a11, where its Draw, Three rules,
readability screen, fork table, ladder and measurements stand. Superseded at the author's instruction: the decisive
construction is one person-and-date join from a release to the booking that follows and a sum of midnight counts, so
the call is arithmetic once the join is seen. Its card moved into `lineage` with that fate.

**Architecture 1 (drawn 2026-10-15, FAILED_TO_STUMP).** Dorrance County's 2027 presumptive written-promise release
tier on the Pretrial Assessment Scale, each score's safety rate read for every eligible defendant from the
magistrates' differing release shares under the duty rota (selective labels): both portal responses landed scores 1
to 3. The portal diagnosis (in full at 31378a11, `## Portal result and the stage 2 diagnosis`) found every large lever
in that world a counterfactual for a defendant a magistrate held, the selection family by construction, which is why
architecture 3 leaves the pretrial world for a record whose outcomes are held whole.

## Tried and rejected

- The seed's world, decision and quantity (a serverless platform's warm-pool memory to reserve for next quarter, a
  host released only when its last instance goes cold): a quarterly compute reservation at a capacity cut-off is the
  same project as task140 (shipped 2026-10-15, a compute cell's quarterly batch guarantee) to the guard's reader and a
  reviewer's, and the seed's mechanism (the union of keep-alive windows over an app's functions) is rule application;
  dropped at the draw for a client domain no forecasting build has used.
- An ML lab's compute-optimal model size from scaling-law runs (mid-schedule checkpoints overstate a short run's loss):
  "batch training", "compute budget" and "2027 Q1" echo task140's world; dropped at the draw.
- A school-age population projection with gross migration flows against net rates (Sociology & Demography): the
  cohort-component projection carries a fork for every component (fertility, mortality, international migration, the
  origin's own projection), and a net-rate method is a practice a judge could call defensible; dropped at the draw.
- A seat-majority probability from district polls with a correlated national error (Political Science): the national
  error component is sized from a handful of past elections (small counts); dropped at the draw.
- A shelter's nightly demand censored at its bed capacity (a Tobit on full nights): the cap is visible as a pile of
  nights at exactly capacity, so the censoring is a schema read; dropped at the draw.
- A per-score floor checked on the tier's whole population at once (the cumulative safety rate of scores 1 to k): the
  selection at score 4 is diluted by scores 1 to 3, leaving the full-release estimates within a point of the floor; the
  floor is applied score by score (each score included only if its own rate meets it), which keeps every leniency
  estimate on the same side.
- A first calibration of the selection at score 4 (the trait the magistrate sees on 30 per cent of score-4
  defendants, their new-offence rate 0.60 in the window): the lenient fifth of magistrates' own released defendants put
  score 4 at 86 per cent, on the default path's tier, and the weighted line sat a point from the floor in one draw; the
  trait's rate was raised to 0.80 at scores 4 to 6, so every construction of the gradient sits at least 4 points under
  the floor while the released defendants' rate stays near 88.
- Ask B counted defendants: a defendant released twice in the period carries two failure-to-appear scores, so the ask
  counts releases.
- The judge's optional prompt pins at stage 4 ("including days boarded out to Halsey County" in the bed-days ask,
  "within 90 days of release, inclusive" in the missed-court-date ask): the prompt stands at 992 of its 1,000
  characters and the first names the contract county, pointing at Ask A's device; the conventions went to the README
  in Pretrial Services' voice instead (custody through a boarding, day counts after a release, monitoring days by
  release), and the draft's 2.4 was left as filed, its disposition-day boundary a same-call row (SF30).
- One random stream per arrest keyed by the running count of every arrest: any change to one person's history moved
  every later person's draws, so the asks' year could not be set without moving the call; streams are keyed by person
  and the person's own arrest index, and the first appearances from 1 October 2025, the failures to appear and the
  monitoring each draw from their own stream.

- 2026-10-26, architecture 1's decisive step (the magistrates' leniency gradient read out to full release),
  after both portal responses landed scores 1 to 3. Spent, not repairable: the correction is pretrial risk
  assessment's own reflex rather than a step a competent analyst skips, and the ladder's seven constructions
  of the gradient are `stumping` 1.1j in plain sight, an estimator fitted over a chosen population. Measured
  at the same time and also dead: one row per defendant (0.6 points at score 4, the serial-arrest mix is flat
  across scores), the exposure family (windows are 104 to 108 days at every score with 98 per cent capped by
  disposition, and the 0.13 per cent daily hazard makes every window-lengthening mechanism about three times
  too small), and the uncapped window (very large but the draft rule defines the window, so taking it is rule
  application). The re-root is recorded in `## Portal result and the stage 2 diagnosis`.

- The re-root candidate's first reconnaissance pass: every figure computed on the raw stay convention (each NEW
  row ending at its own release, so an annex move reads as a release), which the README and the jail code list
  rule out, so the holding cost, the average stay and the per-release following figures were all wrong and the
  "understates 2.1 times" and "nearly a wash at score 6" readings rested on it; re-measured on the golden
  convention, where the mechanism survives at 3.16 times with the naive route capturing 5.3 per cent at score 6.
- The one-year FY25 frame for the re-rooted call: not gradeable per score (relative standard error 18 to 24 per
  cent, score 3 above score 4, 16 per cent of bootstrap draws monotone); the four closed years give 10 to 13 per
  cent and 99.6 per cent monotone, so the frame is four years.
- Architecture 1 (the 2027 presumptive release tier, the safety rate each score would show under full release, read
  from the magistrates' differing release shares): spent. Both portal responses landed the call. The decisive step was
  the domain's own reflex, which is what a pretrial researcher reaches for first, and it was an estimator with seven
  defensible constructions rather than a reconstruction the records force (`stumping` 1.1j). Hardening was refused on
  measurement: dedupe has no leverage, exposure is flat across the scores, and the window definition is the only other
  lever and a filed rule defines it; and structurally every large lever in that world is a counterfactual for a
  defendant a magistrate held, which is the same selection family, so the decision had to move rather than the rung.
- The re-rooted call framed as what a wider tier would free: refused at the draw. Pricing the release of defendants a
  magistrate currently holds needs their unobserved failure rate, which is architecture 1's counterfactual and the
  reason it was spent. The call is the releases the county already makes, whose outcomes the record holds whole and
  whose following stays are all closed at the extract.
- Summing every booking inside the window, and taking the failure arrest's own booking, as ladder rungs: refused on
  magnitude. Measured at 13.3 per cent high and 2.7 per cent low, both inside any bin the graded figure can carry, so
  they are semantic forks to close at authority rather than rungs to climb.

- 2026-10-27, architecture 2 superseded (the bed-day bill of the releases the county makes): at the author's
  instruction; the decisive construction (a release joined to the booking that follows by person and date, then a sum
  of midnight counts) is arithmetic once the join is seen, and the footprint of a defendant a wider tier would release
  but a magistrate holds is still architecture 1's counterfactual.
- 2026-10-27, architecture 3 draw: the supervision level a risk score assigns producing part of the violations
  recorded at each score (detection), read at the tier cut-off or through overrides: `causal_design` was barred by
  task139 v2 in the window, and task169 had set aside the cut-off discontinuity as a reflex (a logistic with the tier
  lands it).
- 2026-10-27, architecture 3 draw: the parole board's conversion of a violation to a return falling as the maximum
  sentence date approaches, under retroactive earned credits (a second clock, time to the max date): set aside without
  a paper run for the expiration review; its lever is a slope in the conversion over the last months before the max,
  where the expiration review moves the forecast's sign, and a board practice sharp enough to matter would read as a
  withheld rule.
- 2026-10-27, architecture 3 draw, the decision and the labels: three housing options as the decision type BLOCKed
  `test.same_puzzle` against task269 v1's lineage, and decisive G7 or G13 BLOCKed against task137 v4, task166 v3 and
  seven older builds; the card reads `quantity_figure` with G4, the pods following from the filed standard.
- 2026-10-27, architecture 3 paper world with felony terms of 36, 48 and 60 months only: the time-on-supervision hazard
  showed bumps at 33 to 36, 45 to 48 and 57 to 60 months that a careful reader of the hazard curve would read as term
  ends; felony terms now run 18 to 72 months over eight lengths, so the pooled curve smears and the clock shows only
  when petitions are aligned on scheduled expiration.
- 2026-10-27, architecture 3 paper world, the first truth runs: early termination keyed to the last three entries of
  the whole log in the record and to the case's own entries in the re-run, and the re-run skipping the extract's
  partial month, both biased the truth, and the golden counted reviews for terms whose window had opened before the
  extract; fixed (termination needs no petition on the case, a partial month carries its share of the hazard, the
  review's remaining share read off the record's own filing offsets).
- 2026-10-27, architecture 3's first build world (v3): the end-of-term petitions read 5 to 13 times the pooled
  hazard by time on supervision, so the default path's own curve showed them; reworked as v3b with a jail condition
  between sentencing and supervision (85 per cent of felony terms, median about 110 days), the Act's cap counted from
  the start of supervision, extensions and tolling moving the scheduled expiration, and no sentencing date in the
  registers. The supervision clock now peaks at 1.5 times its neighbours pooled and 1.1 to 2.1 times by term length,
  while the alignment on the expiration in force shows 26 per cent against 5.
- 2026-10-27, an ask on violator admissions by quarter, felony and misdemeanor: the Circuit Court's petitions give the
  felony column exactly (a REVOKED petition on a CF case is a felony admission, one felony term a person at a time),
  so the ask had no device on the route a careful solver takes. Replaced by violator bed-days by quarter, which only
  the jail's bookings carry and where a misdemeanor commitment of a person then on felony probation is booked PV-FEL:
  the classification route keeps 0 of 8, and the new system's UTC read as local 4 of 8.
- 2026-10-27, end-of-term filings spread over 7 to 120 days before the scheduled expiration (mode 40): a 90-day
  window filed 1,140 (1,100 to the nearest 100) and a 60-day window five pods. The filings now fall 7 to 90 days
  before it (mode 30): every window from 75 days prints 1,200, every window from 60 days files six pods, and the
  aligned histogram stops at about 90 days.
- 2026-10-27, a world that opens empty on 1 July 2016: the caseload took years to fill, so felony revocation
  admissions rose from about 45 a month in 2019 to 85 in 2025, a trend a solver could carry into 2027 in place of
  reading the record. The world now runs from January 2008 and the extracts begin on 1 July 2016 (terms closed,
  petitions filed and orders made from that day); the history runs flat at 920 to 1,020 a year, and every estimate
  takes delayed entry at the extracts' first day.
- 2026-10-27, the world at a felony intake of 218 a month with end-of-term filings on 23 per cent of terms: the
  golden sat at the low end of its own family, and 10 of the 96 combinations of the six standing choices printed
  1,300; intake 210 and 23.5 per cent centre the family, all 96 between 1,164 and 1,233 and every one six pods.
- 2026-10-27, Ask B's three time-on-supervision bands (under one year, one to two, two or more): the band of two
  years or more averaged 58.850 months, within a thousandth of a rounding edge, so one term more or less moved the
  graded figure; four bands (under one, one to two, two to three, three or more) leave every figure at least 0.021
  from an edge, under the extract-day closures and a 365.25-day year alike.
- 2026-10-27, the golden adjusted for the CSRS score: a solver who leaves CaseTrak 1's version 1 totals unhalved files
  1,115 with it (six pods, 1,100 to the nearest 100), so a Layer 1 slip moved a graded figure; the golden is now the
  unadjusted construction (the score-adjusted one is a standing member, within 5 of it), and the slip moves nothing.
