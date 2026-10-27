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
| Objective | Forecasting & Predictive Modeling: the felony probation revocation admissions the Detention Center will see in calendar 2027, a window not yet open at the extract (30 September 2026), under a statute that takes effect on 1 January 2027 |
| Shape | `02` (forecast across periods): the call (pods and the plan figure), its parts and its 2027 profile by month in the chart, and the asks' 16 figures (violator bed-days by quarter and level, the imposed term by office and time on supervision); the arithmetic is under `## Ask sheet` |
| Decision | `quantity_figure` (the plan's 2027 admissions, from which the filed standard sets the violator pods), answer unit `count` |
| Mechanism | gap time (decisive: the record's petitions were made under terms that ended where they were set; the Act moves every end and ends 3,373 running terms on one day) then population (the terms past 24 months are a block no new term will form); pattern none, generators G4 (attribution at the transition: which clock each petition rides) then G13 (the forecast horizon holds a transition the window never exercised); Gate G `forecasting`; strategy `time_semantics` |
| Layer 2 family / pattern | `estimation_fit` (the data's real structure: which clock an event rides, and exposure that begins with the extracts); `own:violation-petitions-filed-before-each-term-lapses-ride-the-scheduled-end`. The client library's recidivism cards (calibration, fixed follow-up and time at risk, the fairness criterion, later release cohorts, selective labels, local base rates) are the default path's own careful moves here: the survival projection by time on supervision with the risk score is card 2 and card 4 done well, and it files three pods |
| Furniture | forum `council_or_assembly` (the County Board of Supervisors adopts the plan), forcing event `statutory_or_regulatory_filing` (the 2027 Jail Operations Plan is due to the State Jail Standards Board on 1 December 2026), organisation family `local_government`, role family `research_desk` (the Sheriff's Office jail planning analyst), context artifact `filed_standard` (the Board's instructions with the county's pod standard, and the Act), calibration `none`, opening `question-first`, question form `how-many` |
| Spine | `detention_probation_bookings_2019_2026.csv` (48,178 rows), the Detention Center's probation bookings, one booking at a time per person, an annex move, a reclassification and the 2025 system replacement each writing a new row; synthetic |
| Deliverables | `violator_housing_plan_2027.xlsx` (the projection and how it is built, the pods, the asks), `violator_housing_memo_2027.docx` (the plan's violator housing section), `felony_revocation_admissions_2019_2027.png` (monthly admissions and the 2027 projection) |
| People | drawn with `guard.py names --geo us --seed 141 --n 30`, skipping every first name the guard warns on: Gina Yoder (Sheriff's Office jail planning analyst), Larry Pugh (Chief Probation Officer), Colleen Cameron (Detention Center commander), Donald Russo (Probation research and data manager), Megan Chambers (Clerk of the Circuit Court), Gloria Lynch (County Budget Director); none appears in the prompt |

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

**World.** Okelan County (fictional, an unnamed state on Central time) supervises about 7,600 felony probationers
through its Adult Probation Department. Under the State's 2019 realignment a felony probation revocation is served in
the county of supervision, so every felony revocation is a commitment to the Okelan County Detention Center. Felony
terms run 18 to 84 months; most carry jail time as a condition, served before supervision begins. Officers file
violation petitions with the Circuit Court on new arrests, missed reporting, failed tests and treatment failures
through the term, and in the last weeks before a term's scheduled expiration on matters still open (restitution,
unfinished treatment, a pending charge), because a petition filed before expiration keeps the court's jurisdiction.
Senate Bill 26-118 takes effect on 1 January 2027: a felony term imposed from that day runs no more than 24 months
from the start of supervision, and a term in effect ends on the earlier of its scheduled expiration and 24 months
after supervision began, but not before 31 March 2027; proceedings pending on that day continue. The Sheriff's Office
writes the 2027 Jail Operations Plan, which states the felony probation revocation admissions it projects and staffs
violator pods by the county's filed standard (one 64-bed pod for each 220 projected admissions or part of 220).
Records to the extract of 30 September 2026; the extracts begin on 1 July 2016.

**Data-native sentence.** In Okelan County's record about a quarter of felony violation petitions (24.5 per cent)
are filed in the last 120 days before the scheduled expiration then in force, on matters left open as the term lapses:
26.4 per cent of the terms that reach their last 120 days on supervision with nothing pending carry one, against 4.5
per cent in the same days a year earlier. SB 26-118 moves every felony term's expiration and puts 3,373 of the terms
open at the extract on 31 March 2027.

## Three rules

- Task type: criminology-justice, recidivism-risk-assessment (serves Forecasting): the 2027 count of felony probation
  revocations the Okelan County Detention Center will admit under SB 26-118, forecast from the county's supervision
  record.
- Domain test: the deciding quantity is the forecast count of revocations, which the field projects from failure on
  supervision (the hazard of a violation petition by time on supervision, the share of petitions that end in a
  revocation, the time from petition to commitment, with exposure counted while the record can see it); it turns on
  probation law's tolling: a petition filed before a term expires keeps the court's jurisdiction, so officers file on
  open matters in the weeks before each scheduled expiration, a second clock that carries a quarter of the county's
  felony petitions.
- Swap: "a gym chain forecasting 2027 cancellations after a cap on contract length" keeps a term and a cap, but
  nothing in it is filed to keep an authority over a member before the term lapses, a cancellation at the end is the
  term's own end rather than a filing that extends it, and no transition ends thousands of running contracts on one
  day, so the reasoning that decides (which clock the petitions ride and where the Act moves it) has no counterpart.
- Layer 1: the two case systems' layouts (CMS 1 with MM/DD/YYYY dates, one-letter offices, terms in days and CSRS
  version 1 totals of 0 to 40; CMS 2 in months and 0 to 20), the registers' expiration as it now stands beside
  the Clerk's orders that moved it, the Detention Center's one booking at a time (annex moves and reclassifications
  write new rows, the 2025 replacement closes and reopens every open spell, the new system writes UTC), the Sheriff's
  merged numbers in the crosswalk, misdemeanor terms and interstate holds in the same records, and the terms still in
  their confinement condition, in neither register; each is what the named system produces, and none decides the call
  (`## Layer 1 inventory`).
- Layer 2: family `estimation_fit`; the choice that flips the call is reading the record's petitions on two clocks,
  months on supervision for the ordinary ones and days to the expiration in force for those filed as a term lapses,
  and moving the second clock to the end the Act sets; exposure counted from the extracts' first day is the survival
  method's own care and sits on the ladder below it.
- Decisive step: in the field's words, a revocation forecast built on time on supervision has to separate the
  petitions filed against the expiring term (the tolling petitions in its last months) from the violations through
  the term, because the Act moves every scheduled expiration and ends 3,373 running terms on one day, and the tolling
  petitions follow the end.
- Not semantics: every field, code and date read correctly (allegation codes, dispositions, order types, booking
  classes, the Act's sections) still leaves the time-on-supervision forecast at about 610 (three pods); no column,
  code or status marks a petition as filed against the expiring term (its allegations are the codes the ordinary
  petitions carry, the largest share gap 0.009), and the clock appears only when filing dates are aligned on each
  term's expiration in force.
- Not rule application: SB 26-118 sets every term's new end and the standard turns admissions into pods, and
  executing both on the time-on-supervision projection files three pods; no rule or document names a petition clock,
  a window or a rate. Measured on the cut pack (`generator/golden.py`, `checks.py`): the enumerated family
  (persistence 912, the trailing year's rate over the Act's exposure 663, the time-on-supervision projection pooled
  607 or by term length 591, the two clocks without the 31 March terms 766, the two clocks with exposure from
  supervision start 1,085, the expiry clock alone 1,127, the two clocks 1,186) spreads from 591 to 1,186, three to six
  pods; the standing family (the end-of-term window from 90 to 150 days, the CSRS score as a covariate or not, one
  revocation rate or two, the mean lag or the record's lags, the 31 March terms' windows opening on 1 January 2027 or
  before it, windows of terms with nothing pending) spreads 1,169 to 1,203 one choice at a time and 1,164 to 1,233
  over all 96 combinations, every one 1,200 to the nearest 100 and six pods; the ruling-out is one alignment nothing
  invites, petitions by days to the expiration in force, where 26.4 per cent of terms reaching their last 120 days
  carry one against 4.5 per cent a year earlier.
- Analyst test: a strong analyst who conforms the two layouts, the orders, the petitions and the commitments, applies
  the Act to every term and fits revocation by month on supervision with the risk score (the field's survival
  projection), each term counted from the extracts' first day, carrying each case to its new end and adding new
  starts, files about 610 admissions (three pods), against the golden's about 1,200 (six pods); persistence files 912
  (five pods).
- Estimand: felony probation revocation admissions to the Okelan County Detention Center in calendar 2027 (a person's
  commitment on the revocation of a felony term the Department supervises, counted once on the day it begins),
  including admissions on terms whose supervision begins after the extract, under SB 26-118 as enacted, with the
  courts, the Department and the Sheriff acting as the records to the extract show; filed in
  `jail_operations_plan_instructions_2027.pdf` sections 3 and 4.
- No decoy: nothing is planted; the petitions filed before a term lapses are what tolling makes officers do,
  generated by one process for every term; no memo, briefing, draft or stakeholder figure forecasts revocations, the
  Department's annual report counts fiscal 2025's petitions, revocations and closures only, and the headcount counts
  the jail at 06:00.
- No certified replay: no certified, published or prior-period figure is reproduced to recover a method; nothing in
  the pack forecasts 2027 or scores a method.
- Lesson: an event filed against a term's scheduled end rides that end, not the time since the term began; a reform
  that moves every end moves those events, and a transition that ends thousands of terms on one day fires them
  together. No build on file reads a second clock tied to each unit's scheduled end, or a transition that fires it.

## Layer 1 inventory

| Item | The system that writes it | File | Natural mishandling | Measured on the call |
|---|---|---|---|---|
| CMS 1's layout: MM/DD/YYYY, one-letter offices, terms in days, CSRS version 1 totals 0 to 40 | the legacy case system | `cms1_supervision_cases_2016_2023.csv` | version 1 totals read as version 2 | the golden reads no score: unchanged; the score-adjusted member 1,115, six pods |
| Expiration as it now stands in the registers, its history in the orders | CMS and the Clerk's system | `cms2_supervision_cases_2023_2026.csv`, `circuit_court_term_orders_2016_2026.csv` | every expiration read as it now stands | 1,200, six pods |
| Terms still in their confinement condition are in neither register | CMS enters a term when supervision begins | both registers | new supervision starts from the trailing six months | in the bin, six pods |
| One booking at a time: annex moves, reclassifications, the 2025 replacement, UTC from 2025 | the jail management system | `detention_probation_bookings_2019_2026.csv` | the call reads no booking | none (Ask A's ground) |
| Merged Sheriff's numbers | the Sheriff's records unit | `person_id_crosswalk.csv` | the call reads none | none |
| Misdemeanor terms and interstate holds in the same records | CMS, the jail | registers, bookings | a felony filter by level | none |

## Default path

1. Read SB 26-118 and the Board's instructions: the plan carries the felony probation revocation admissions of 2027
   and staffs violator pods by the county's standard (one 64-bed pod for each 220 admissions or part of 220).
2. Conform CMS 1 and 2 (layouts, codes, CSRS scales), the term orders and the petitions by case number; keep
   the felony terms and count each term's exposure from 1 July 2016, the extracts' first day.
3. Set each term's end under the Act: a running term at the earlier of its scheduled expiration and 24 months after
   supervision began, not before 31 March 2027; a new term 24 months.
4. Fit the field's survival model, revocation by month on supervision with the risk score (a discrete-time hazard,
   censored at closure and the extract); stratifying by term length leaves it where it is.
5. Carry each open term month by month to its end under the Act, the pending petitions at their conversion and new
   starts at the trailing year's rate.
6. Sum the commitments dated in 2027: about 610 (607), a third below the trailing year's 912, three pods.

Ends on: about 610 felony probation revocation admissions in 2027 (three pods; the trailing year carried 912).
Golden: about 1,200 (1,186; six pods): a quarter of the record's felony petitions are filed in the last months before
a term's scheduled expiration and ride that end, and under the Act 3,373 running terms end on 31 March 2027, so their
petitions come in the first quarter of 2027 and their commitments in the spring (419 admissions), on top of the terms
reaching 24 months through the year.

## Stump sentence

A competent solver fits revocation by month on supervision with the risk score, carries it over each felony term's
2027 months to its end under SB 26-118 and files about 610 admissions (three pods); the step that lands it there is
reading every petition on the time-since-start clock, when a quarter are filed in the last months before a term
lapses, ride each term's scheduled end, and under the Act fire at once for the 3,373 terms that end on 31 March 2027,
so the plan carries about 1,200 (six pods).

## Build world

`generator/world.py`: felony and misdemeanor terms imposed from January 2008 (210 and 150 a month), so the record
opens on a settled caseload; felony terms 18 to 84 months over nine lengths, 85 per cent with a confinement condition
(median about 110 days, longer for longer terms) served before supervision begins; ordinary petitions on a monthly
hazard that falls from 3.2 to 0.85 per cent over the first year and a half on supervision and scales with the risk
screen; on 23.5 per cent of terms that reach the last 90 days before the expiration in force with nothing pending, a
petition 7 to 90 days before it (mode 30); 48 per cent of each kind ending in a revocation some 70 days after filing;
extensions on continued petitions, tolling for absconders, early termination for compliant cases after 18 months. The
extracts begin on 1 July 2016 (terms closed, petitions filed and orders made from that day). The truth is the
generator re-run from every term's state at the extract under the Act, eight times: 1,197 (sd 33). `golden.py`
computes every route from the cut pack alone and `checks.py` asserts the table.

| Route | Admissions 2027 | Pods |
|---|---|---|
| Persistence (the trailing year) | 912 | 5 |
| The trailing year's rate over the Act's exposure | 663 | 4 |
| Time on supervision by term length | 591 | 3 |
| Time on supervision with the risk score (default) | 607 | 3 |
| Two clocks, exposure from supervision start | 1,085 | 5 |
| Two clocks without the 31 March terms | 766 | 4 |
| The expiry clock alone | 1,127 | 6 |
| Two clocks (golden) | 1,186 | 6 |

## Readability screen

Measured on the cut pack (`checks.py` restates the figures on each build).

| Rung | What the response does | What in the pack points at it | Verdict |
|---|---|---|---|
| L0 persistence (912, five pods) | carries the trailing year's 912 admissions into 2027 | the petitions' revocations by month, the annual report's counts | readable |
| L1 rate over the Act's exposure (663, four pods) | the trailing year's admissions per month on supervision, over the months the Act leaves in 2027 | the registers' supervision months | readable |
| L2 time on supervision by term length (591, three pods) | the projection by month on supervision and imposed term, each term cut at its new end | the term length columns | readable |
| L3 time on supervision with the risk score (default; 607, three pods) | the field's survival projection, each term to its new end | the registers, the petitions, the Act | readable |
| L3b two clocks from supervision start (1,085, five pods) | the two clocks with each term's exposure from the start of its supervision, before the extracts begin | the extracts' own first dates (petitions filed and orders made from 1 July 2016) against supervision dates from 2008 | readable |
| L4 two clocks without the 31 March terms (766, four pods) | the end-of-term petitions only for terms ending on their own expirations | section 4's 31 March floor | readable |
| G two clocks (decisive; 1,186, six pods) | ordinary petitions by month on supervision, end-of-term petitions in each term's last 120 days before its end under the Act | nothing labels a petition by its clock: no column holds the days to expiration, the end-of-term petitions carry the others' allegations (largest share gap 0.009), and the clock shows only on petitions aligned on the expiration in force (15-day bins from day 1: 230, 1,049, 1,271, 996, 670, 260, then about 110 a bin); on the supervision clock it peaks at 1.59 times its neighbours pooled and 1.1 to 2.3 times by term length | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | an admission | a person's commitment on a day a felony term was revoked | each revoked petition | same call (one felony revocation a person and day; asserted) | instructions 3.1 |
| SF2 | the day an admission is dated | the day the commitment begins, the hearing | the disposition date | same call (no felony commitment is served on weekends; asserted) | instructions 3.1, the petitions' served_as |
| SF3 | county time | court dates, bookings in county time | UTC dates | same call (every felony commitment begins on a revocation day in county time; asserted) | instructions 1.3; the call reads court dates |
| SF4 | terms whose supervision begins after the extract | counted | left out | another call (973, five pods) | instructions 4.2 |
| SF5 | 24 months after supervision began | calendar months | 730 days | same call (3,373 terms either way; asserted) | the Act, section 4 |
| SF6 | not before 31 March 2027 | a running term past its 24 months ends on 31 March 2027 | it ends on 1 January 2027 | same call (1,193, six pods; measured) | the Act, section 4 |
| SF7 | proceedings pending on the day a term ends under section 4 | continue | end with the term | another call (766, four pods) | the Act, section 6 |
| SF8 | the extract | petitions pending at 30 September 2026 carried as pending | none | same call (asserted) | instructions 1.2 |
| SF9 | or part of 220 | a ceiling: 5.39 pods is six | rounding to five | another call (five pods) | instructions, Annex |
| SF10 | pods from the projection or the plan figure | the unrounded projection | the figure to the nearest 100 | same call (six either way; asserted) | instructions 2.2, 4.3 |
| SF11 | a felony admission | a revoked term is a felony term | a felony probationer's commitment (PV-FEL) | same call (24 a year more; asserted) | instructions 3.2 |
| SF12 | the end-of-term window and the estimator's other choices | 120 days, no score, a rate per kind, the record's lags | 90 to 150 days, the score, one rate, the mean lag, windows from before 1 January 2027, terms with nothing pending | same call (96 combinations 1,164 to 1,233; asserted) | the record: the aligned petitions stop at 90 days |

## Ladder

Measured on the cut pack; `checks.py` asserts every row on each build.

| Rung | Admissions 2027 | Pods | Call kept |
|---|---|---|---|
| L0 persistence | 912 | 5 | no |
| L1 the trailing year's rate over the Act's exposure | 663 | 4 | no |
| L2 time on supervision by term length | 591 | 3 | no |
| L3 time on supervision with the risk score (default) | 607 | 3 | no |
| L3b two clocks, exposure from supervision start | 1,085 | 5 | no |
| L4 two clocks without the 31 March terms | 766 | 4 | no |
| G two clocks | 1,186 | 6 | yes |

Every rung that skips the decisive step sits under the rung floor (1,100 over 1.15 is 957), persistence the closest
at 912. L3b takes the decisive step without delayed entry and sits 15 below the six-pod edge. The standing family runs
1,169 to 1,203 one choice at a time and 1,164 to 1,233 over all 96 combinations; the expiry clock alone, a cheaper
route that also needs the alignment, files 1,127 and six pods. The truth is 1,197 (sd 33 over eight runs).

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | felony revocation admissions on terms the Department supervises, terms beginning supervision after the extract included | filed (instructions 3.1, 3.2, 4.2); SF4, SF11 |
| 2 | Unit of account | a person's commitment, counted once on the day it begins | filed (3.1); SF1 |
| 3 | Attribution window | calendar 2027, by the day the commitment begins | filed (1.1, 3.1); SF2 |
| 4 | As-of dating | records to the end of 30 September 2026 | filed (1.2); SF8 |
| 5 | Version basis | the one set of extracts pulled 2 October 2026 | C1 |
| 6 | Denominator | exposure while the extracts can see it, from 1 July 2016 | the survival method (delayed entry); rung L3b |
| 7 | Weighting | none | not applicable |
| 8 | Window length | the plan year; the end-of-term window 120 days | filed (1.1); SF12 |
| 9 | Boundary inclusivity | one pod for each 220 or part of 220 | filed (Annex); SF9 |
| 10 | Rounding path | pods from the unrounded projection; the plan figure to the nearest 100 | filed (4.3, Annex); SF10 |
| 11 | Tie-break | none needed | asserted: every standing construction 1,164 to 1,233 |
| 12 | Maturity and censoring | open terms and pending petitions at the extract | the decisive step; SF8 |
| 13 | Order of operations | apply the Act, project, sum, apply the standard | linear |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | one row per term, petition and booking | asserted (unique numbers) |
| 16 | Identity normalisation | case numbers across both systems; Sheriff's numbers through the crosswalk, merged numbers included | asserted |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | admissions, months and days, county (Central) time | filed (instructions 1.3; the new system marks UTC) |
| 19 | Code and status semantics | dispositions, order types, closure codes, booking classes | filed (code lists); SF11 |
| 20 | Integerisation | pods as whole units | filed (Annex) |
| 21 | Clause scope | felony terms; the Act leaves misdemeanor terms | filed (the Act, section 7) |
| 22 | Forward window contents | the Act's ends, terms beginning supervision later, pending petitions, proceedings pending at an end | filed (the Act 3 to 6, instructions 4.2); SF4, SF7 |

## Literal reader

Executing the prompt and every filed sentence word for word: the Board's instructions define the admission (3.1,
3.2) and the projection (4.1: under the law in force in the plan year, with the courts, the Department and the
Sheriff acting as the records to the extract show them acting; 4.2: terms whose supervision begins after the extract
included), the Act sets every felony term's end (sections 3 to 6) and the Annex the pods. Acting as the records show
includes when officers file: 26.4 per cent of the terms reaching their last 120 days carry a petition, against 4.5
per cent a year earlier, and the aligned petitions stop at 90 days, so a projection that books those petitions at the
expirations the Act removes acts as the old law, not as the records show. Every standing construction files 1,164 to
1,233 admissions, 1,200 to the nearest 100 and six pods; the construction that reads every petition on one clock
files three. Section 6 keeps the 31 March terms' pending petitions revocable (without it 766) and section 4.2 counts
the terms beginning supervision after the extract (without them 973), so both are filed rather than left to a
reading.

## Oracles

No file ties only under the golden or only on a wrong read. The Department's fiscal 2025 report counts petitions,
revocations and closures from the shipped rows (asserted) and forecasts nothing; the headcount is the jail's own 06:00
count by housing unit and answers occupancy, not the projection. Nothing in the pack forecasts 2027, ranks a method or
names a petition clock. The referee for Ask A is the court's revocation on the day a commitment begins (a PV-FEL
commitment begun on a day only a misdemeanor term of the person was revoked is a misdemeanor commitment), the device's
evidence and never an answer; for Ask B, the EXTENSION orders' months.

## Ask sheet

The call's declared population is the felony terms of CMS 1 and 2 with their term orders and petitions; the
bookings, the crosswalk, the misdemeanor terms and the headcount are outside it (asserted: the call reads no booking
and no term length). The annual report and the headcount ship as distractors: the plan counts admissions by the
instructions' definitions, not the report's fiscal-year counts or the 06:00 occupancy, and no golden figure opens
them.

- **Ask A, violator bed-days by quarter, October 2025 to September 2026, felony and misdemeanor, whole days (8
  figures).** H18 home: the instructions' section 5, the violator housing in use that the pods add to. User: the
  Detention Center commander. Primary device (silent): the jail books a commitment by the person's status (PV-FEL is
  a felony probationer's commitment) while section 5.3 counts a bed-day by the term the commitment revokes, so a
  person on felony probation committed on a misdemeanor revocation is booked PV-FEL and is a misdemeanor bed-day (24
  such commitments a year, some in every quarter). Secondary: the new system writes UTC, and a weekend period booked
  on a Friday evening loses a night read as local. Hazards: one booking at a time (annex moves, reclassifications, the
  2025 replacement), merged Sheriff's numbers, holds and interstate holds left out. Stops measured on the cut pack:
  the classification as the level 0 of 8, with UTC read as local 0 of 8, with holds counted 0 of 8; linked to the
  court but UTC read as local 5 of 8; linked through current Sheriff's numbers only 8 of 8 (no merged number touches
  a commitment in the four quarters).
- **Ask B, the average term imposed at sentencing of the felony probationers on supervision at the extract, months to
  one decimal, by office (4) and time on supervision (4) (8 figures).** H18 home: the instructions' section 6, the
  population the Act shortens. User: the Chief Probation Officer. Primary device (silent): CMS 2's term_months
  is the term as it now stands, extensions included; the term imposed is term_months less the months the EXTENSION
  orders added (the orders carry term_months_after). Every figure sits at least 0.021 from a rounding edge, under the
  extract-day closures and a 365.25-day year alike. Stops: term_months as it stands 0 of 8; the expiration less the
  supervision begin 1 of 8; open terms past their expiration left out 4 of 8.

| Ask | What the cracker does | Cracker |
|---|---|---|
| A | reads the bookings' classification as the level (PV-FEL felony, PV-MIS misdemeanor), county time from UTC, annex moves and reclassifications chained | misses |
| B | averages CMS 2's term_months over the open felony terms | misses |

Measured by: `generator/ceiling.py` on the cut pack.

| Ask | Graded figures | Cracker keeps | Mirror keeps | Naive handling keeps | Cracker |
|---|---|---|---|---|---|
| A violator bed-days by quarter and level | 8 | 0 | 0 | 0 | misses |
| B the average imposed term by office and time on supervision | 8 | 0 | 0 | 0 | misses |

Over the 16 figures the cracker keeps 0.0 per cent of ask weight (45.0 with the call) and the mirror the same off it
(12.0); the best half-handled stops keep 5 of 8 (Ask A, linked with UTC read as local) and 4 of 8 (Ask B, open terms
past their expiration left out).

Pair ceiling: 28.5.
Mirror leakage: 0.0 per cent of ask weight.
The rubric's criteria: the call and the plan figure, the transition terms, the end-of-term concentration and the
default construction ruled out (5), the 16 ask figures, the workbook's parts, the memo's section and the chart (3)
and the rounding (1), 25 in all.

## Stage 4 round 1 (architecture 3, zip 7cd8129f, 2026-10-27)

Both scored readers (sonnet, medium, fresh copies, briefed with the prompt's own figures) landed the call, 1,200
admissions and six pods. Reader A simulated the open felony terms with petition rates by tenure and by days to the
scheduled expiration in force ("filings spike 15 to 90 days before expiry ... stable every year"), the Act's ends with
the 31 March floor and section 6, back-tested at three earlier extracts and filed about 1,165; reader B built "a
petition-filing model by tenure and months to expiry, with the cap applied" and filed 1,150 to 1,185. Both kept the
asks almost whole: A 14 of 16 and B 16 of 16 (score_reader exit 1 twice), each linking the PV-FEL bookings to the
revoked terms and taking the EXTENSION orders' months off term_months. The judge thread returned DETERMINISTIC and
FIX_NOW on wording (state the end-of-term variants as a per-term share, show the cluster inside the last 90 days,
drop the 607 survival figure it could not reproduce); Gate G forecasting and analytical_non_defect, Gate H analytical.
The architecture is spent: the statute that moves every expiration points at the expiry clock, and the clock is one
subtraction and a histogram away for any reader who asks what the Act does to a term's end. Both ask devices were
found as well. Reports: `leak_check_report.md` (the two reads) and `determinism_check_report.md` (the judge).

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
- 2026-10-27, the golden adjusted for the CSRS score: a solver who leaves CMS 1's version 1 totals unhalved files
  1,115 with it (six pods, 1,100 to the nearest 100), so a Layer 1 slip moved a graded figure; the golden is now the
  unadjusted construction (the score-adjusted one is a standing member, within 5 of it), and the slip moves nothing.
- 2026-10-27, architecture 3 at stage 4 round 1 (zip 7cd8129f): both scored readers landed 1,200 admissions and six
  pods by modelling petitions on tenure and days to the scheduled expiration in force once the Act was read, and kept
  14 and 16 of the 16 ask figures; a step the forcing statute points at (it moves every expiration) is the reader's
  first model, not a silent rung. Re-rooted to architecture 4 the same day.
