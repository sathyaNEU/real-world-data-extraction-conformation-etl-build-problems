# task141: Okelan County, felony probation revocations when the Act takes the extension away (architecture 4)

Private, never ships. Architecture 4 of task141, re-rooted on 2026-10-27 at the author's instruction (oviya1301) after
architecture 3 was spent at stage 4 round 1: both of its scored readers modelled petitions on the days to each term's
scheduled expiration once the Act was read and landed its call. Architecture 1 (Dorrance County's presumptive release
tier) went FAILED_TO_STUMP on the portal and architecture 2 was superseded at stage 2. The number, the Forecasting lane,
the client domain and Okelan County's world are kept; the decisive step is new: architecture 3's expiry clock is now a
lower rung, and the call turns on how the capped terms will file once the Act takes away the extension the record's
terms used. The earlier architectures are under `## Earlier architectures`.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task141.json`, architecture v4, registered 2026-10-27; `guard.py check` on the filed card WARN only, each answered below, with one NOTE (task253 and task97, differentiated on the card); architectures 1 to 3 in `lineage` with their fates |
| Domain / task type | `criminology-justice` (client domain), task type `recidivism-risk-assessment`, the only one in the domain that serves Forecasting: the 2027 count of felony probation revocations, forecast from the county's own supervision record |
| Objective | Forecasting & Predictive Modeling: the felony probation revocation admissions the Detention Center will see in calendar 2027, a window not yet open at the extract (30 September 2026), under a statute that takes effect on 1 January 2027 |
| Shape | `02` (forecast across periods): the call (the pods), the projection's seven-pod band and its 2027 profile by month in the chart, and the asks (violator bed-days by quarter and level; felony probationers by supervising office and time on supervision) |
| Decision | `quantity_figure` (the violator pods the plan staffs, set by the filed standard from the 2027 admissions projection), answer unit `count` |
| Mechanism | gap population (decisive: the record's end-of-term petition rate is measured over terms that could mostly still be extended, the plan year's capped terms cannot) then time (the plan year runs under a rule the window never applied to most terms); pattern none, generators G11 (the extension's precondition, room under the offense class's statutory maximum, which the Act removes from every capped term) then G13; Gate G `forecasting`; strategy `population_selection` |
| Layer 2 family / pattern | `estimand_identification` (the right comparison group for the capped terms' end-of-term behaviour: the terms already at their class maximum); `own:end-of-term-petitions-where-no-extension-room-remains`. The client library's recidivism cards (calibration, fixed follow-up and time at risk, the fairness criterion, later release cohorts, selective labels, local base rates) are the default path's careful moves; the two-clock projection at the record's own rates is architecture 3's golden and here the default |
| Furniture | forum `council_or_assembly` (the County Board of Supervisors adopts the plan), forcing event `statutory_or_regulatory_filing` (the county files its 2027 Jail Operations Plan with the State Jail Standards Board by 1 December 2026, and the Board approves the violator housing staffing on it; SB 26-118's commencement on 1 January 2027 is why the plan's figure moves), organisation family `local_government`, role family `research_desk` (the Sheriff's Office jail planning analyst), context artifact `capacity_report` (the Detention Center's daily 06:00 count by housing unit, the five violator pods in use), calibration `none`, opening `question-first`, question form `how-many` |
| Spine | `detention_probation_bookings_2019_2026.csv` (46,347 rows), the Detention Center's probation bookings, one booking at a time per person, an annex move, a reclassification and the 2025 system replacement each writing a new row; synthetic (the crosswalk, 51,297 rows, is the largest file) |
| Deliverables | `violator_housing_plan_2027.xlsx` (the pods and the projection behind them, the asks), `violator_housing_memo_2027.docx` (the plan's violator housing section), `felony_revocation_admissions_2019_2027.png` (monthly admissions and the 2027 projection) |
| People | drawn with `guard.py names --geo us --seed 141 --n 30` for architecture 3 and kept: Gina Yoder (Sheriff's Office jail planning analyst), Larry Pugh (Chief Probation Officer), Colleen Cameron (Detention Center commander), Donald Russo (Probation research and data manager), Megan Chambers (Clerk of the Circuit Court), Gloria Lynch (County Budget Director); none appears in the prompt |

**Guard.** The first card (strategy `composition_mix`, decisive G14) BLOCKed on `ban.strategy` against task304 and on
`test.same_puzzle_older` and `test.same_driver_older` against six and four builds carrying gap population with G14, so
the decisive pattern is G11, the honest one: the gentler outcome at a term's end (an extension) has a precondition, room
under the class maximum, and the Act removes it from every capped term; the strategy is `population_selection`, the rate
being read off the sub-population that already lacks the room. After registration `ban.artifact` BLOCKed
`filed_standard` against task204, filed inside the window meanwhile; the context artifact is the jail's daily headcount
(`capacity_report`), which answers occupancy correctly and is the file the 2026 pod count comes from. A second re-registration redrew the forcing event: `statutory_or_regulatory_filing` (task273), `budget_or_appropriation` (task204) and `vote_or_meeting` (task157) all sit in the window, and what forces the call now is the Act's commencement and its 31 March transition, which the pods have to be staffed ahead of (`launch_or_rollout`). At ship the card was re-registered (27 October,
12:01) after the merge brought in task118's card, filed at 04:25 with `launch_or_rollout`, which then BLOCKed
`ban.forcing_event`; task273 had left the window by then, so the forcing event is the plan's filing,
`statutory_or_regulatory_filing`, the honester of the two labels (the filing deadline is what forces the call now, the
Act is why its figure moves). WARNs answered:
`driver.near` 0.14 is this slot's own architecture 3 (its step was the timing of the end-of-term petitions, a lower rung
here; the differentiation is on the card); `repeat.gate_g` and `overuse.gate_g` are the lane's objective (a forecast
call carries Gate G `forecasting`); `repeat.decision` (task204) and `repeat.question_form` (task157) are a count on a
different objective and a different domain; `repeat.deliverables` (task273's docx, png and xlsx) is the plan's own genre, a workbook, the plan's section and its chart.

**Same-puzzle test.** Gap population, decisive G11, `quantity_figure`: task253 (latent levels below a line from small
samples, a shrinkage question) and task97's architecture 4 (a funded total converting up to a per-category pool) carry
the triple; neither has an option whose removal moves every unit onto the behaviour the units already lacking it show.

**Abstraction test.** Stripped of nouns: at a term's end a unit with an open matter is extended where its term still has
room under a ceiling and filed against where it has none, so the record's end-of-term failure rate mixes units with and
without room; a cap that takes the room from every capped unit moves all of them to the rate the units already at their
ceiling show. The nearest drivers on file: this slot's architecture 3 (0.14, the review's timing, not its outcome),
task479's architecture 3 lineage (0.11, a total kept under a per-unit ceiling carried forward on a growth rate) and
task193 (0.07). None has an outcome that switches between two channels on a precondition a statute removes, read off the
units that already failed the precondition.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting`: no build reads an end-of-term outcome
conditioned on whether an option remains, or a statute that removes the option. `guard.py slots` on the mechanism's words
(at-ceiling, extension, statutory maximum, could not be extended, substitution) returns no slot screening it; task304's
and task461's hits are other extensions (a charter, a record). Architecture 3's two readers (this note, `## Stage 4 round
1`) set the default path: both built the two-clock projection at the record's own rates and capped the extensions, and
neither asked what an officer does when an extension is no longer available.

**World.** Okelan County (fictional, an unnamed state on Central time) supervises about 7,800 felony probationers. Under
the State's 2019 realignment a felony probation revocation is served in the county of supervision, so every felony
revocation is a commitment to the Okelan County Detention Center. A felony term's length is set within its offense
class's statutory maximum (Class 2 96 months down to drug felony Class 4 24 months), and the court may extend a term
within that maximum. Officers file violation petitions through the term, and as a term runs out they review it: a matter
still open (restitution, fees, unfinished treatment, a pending case) is met by asking the court to extend the term where
it has room under the maximum, and by a violation petition, which keeps the court's jurisdiction, where it has none.
Senate Bill 26-118 takes effect on 1 January 2027: a felony term runs no more than 24 months from the start of
supervision, a term in effect ends on the earlier of its scheduled expiration and the later of 24 months after
supervision began and 31 March 2027, and no court may extend a felony term past 24 months; proceedings pending at a
term's end continue. The Sheriff's Office writes the 2027 Jail Operations Plan, which states the felony probation revocation
admissions it projects and staffs violator pods by the county's filed standard (one 64-bed pod for each 210 projected
admissions or part of 210). Records to the extract of 30 September 2026; the extracts begin on 1 July 2016.

**Data-native sentence.** In Okelan County's record a felony term reaching its last months with a matter still open is
extended when it has room under its class maximum and violated when it has none: 38.7 per cent of the terms reaching
their last 120 days at their class maximum draw a petition (3,761 of 9,723 windows), against 6.0 per cent of the terms
with room (1,162 of 19,282), 53.5 per cent of which are extended instead, and 17.0 per cent of all terms; SB 26-118
leaves no capped term any room.

## Three rules

- Task type: criminology-justice, recidivism-risk-assessment (serves Forecasting): the 2027 count of felony probation
  revocations the Okelan County Detention Center will admit under SB 26-118, forecast from the county's supervision
  record.
- Domain test: the deciding quantity is the forecast count of revocations, which the field projects from failure on
  supervision (petition hazards by time on supervision and by time to the term's end, the share of petitions that end in a
  revocation, the time from petition to commitment, exposure counted while the record can see it); it turns on probation
  law's two tools for a matter still open as a term runs out, an extension within the offense class's statutory maximum or
  a violation petition that keeps the court's jurisdiction, and on the Act taking the first away from every capped term.
- Swap: "a gym chain forecasting 2027 cancellations after a cap on contract length" keeps a term and a cap, but a gym has
  no statutory maximum per class of member, no court that extends a contract to keep an obligation alive, and no petition
  filed to keep jurisdiction when it cannot, so the reasoning that decides (which tool the capped terms are left with, and
  which terms in the record already faced that) has no counterpart.
- Layer 1: the two case systems' layouts (CMS 1 with MM/DD/YYYY dates, one-letter offices, terms in days and risk screen
  version 1 totals of 0 to 40; CMS 2 in months and 0 to 20), the registers' term and expiration as they now stand beside
  the Clerk's orders that moved them, the Detention Center's one booking at a time (annex moves, reclassifications, the
  2025 replacement, UTC from 2025, a held probationer reclassified only when the commitment order arrives), CMS 2's office
  kept at intake beside the supervising officer, the Sheriff's merged numbers, misdemeanor terms and interstate holds in
  the same records, and the terms still in their confinement condition; each is what the named system produces, and none
  decides the call (`## Layer 1 inventory`).
- Layer 2: family `estimand_identification`; the choice that flips the call is the comparison group for the capped terms'
  end-of-term petitions: the terms in the record that already had no room to extend (at their class maximum), not the
  pooled record, whose end-of-term outcomes are mostly extensions the Act forbids.
- Decisive step: in the field's words, a revocation forecast under a policy change has to carry each behaviour at the rate
  of the cases that already faced the new condition: the record's end-of-term petition rate was earned by terms that could
  mostly be extended, the Act leaves no capped term that option, and the terms at their class maximum show what officers
  file when it is gone.
- Not semantics: every field, code and date read correctly (allegation codes, dispositions, order types, classes, booking
  classes, the Act's sections) still leaves the two-clock projection at 911 (five pods); no column or code marks a term's
  room to extend or a petition filed for want of it, and the room appears only when each window's term in force is set
  against its class maximum.
- Not rule application: SB 26-118 sets every term's new end and bars extension past 24 months, the class maxima set the
  room, and the standard turns admissions into pods; executing all of them on the two-clock projection with the extensions
  capped files five pods. No rule or document says what an officer files when an extension is unavailable. Measured on the
  cut pack: the enumerated family (persistence 827, the projection by month on supervision 503, the two clocks at the
  pooled end-of-term rate 911, the extension share reallocated in proportion 1,140, every would-be extension a petition
  1,780, the two clocks with the capped terms at the at-maximum rate 1,424) spreads three to nine pods; the standing
  family (the end-of-term window from 90 to 150 days, the score as a covariate or not, one conversion rate or two, the mean
  lag or the record's lags, the 31 March terms' windows from 1 January 2027 or before it, only the windows with nothing
  pending, the length of an extension) spreads 1,414 to 1,443 one choice at a time and 1,413 to 1,463 at its extreme
  combinations, every one seven pods (more than six pods' 1,260 and no more than seven's 1,470); the ruling-out is one
  comparison nothing invites, the end-of-term petition rate of the terms at their class maximum (38.7 per cent, 36 to 42
  in every class) against the terms with room (6.0).
- Analyst test: a strong analyst who conforms the two layouts, the orders, the petitions and the commitments, applies the
  Act to every term (its new end, no extension past 24 months) and builds the two-clock projection at the record's own
  end-of-term rates with the extensions capped, files 911 admissions (five pods), against the golden's 1,424 (seven
  pods); persistence files 827 (four pods).
- Estimand: felony probation revocation admissions to the Okelan County Detention Center in calendar 2027 (a person's
  commitment on the revocation of a felony term the Department supervises, counted once on the day the court orders it),
  including admissions on terms whose supervision begins after the extract, under SB 26-118 as enacted, with the courts,
  the Department and the Sheriff acting as the records to the extract show them acting, and the violator pods it calls
  for under the county's standard; filed in `jail_operations_plan_instructions_2027.pdf` sections 3 and 4 and the
  Annex.
- No decoy: nothing is planted; the extensions and the petitions at a term's end are what the review produces for every
  term, the terms at their maximum are the ones the classes' own maxima put there, no memo, briefing, draft or stakeholder
  figure forecasts revocations, the Department's annual report counts fiscal 2025 only and the headcount counts the jail at
  06:00.
- No certified replay: no certified, published or prior-period figure is reproduced to recover a method; nothing in the
  pack forecasts 2027 or scores a method.
- Lesson: a behaviour measured while an option was open does not survive the option's removal; the rate to carry is the
  one the cases that already lacked the option show. No build on file reads an outcome that switches channel on a
  precondition a statute removes.

## Layer 1 inventory

| Item | The system that writes it | File | Natural mishandling | Measured on the call |
|---|---|---|---|---|
| CMS 1's layout: MM/DD/YYYY, one-letter offices, hyphenated classes (F-3), terms in days, risk screen version 1 totals 0 to 40 | the legacy case system | `cms1_supervision_cases_2016_2023.csv` | version 1 totals read as version 2 | the golden reads no score: 1,424 unchanged; the score-adjusted member 1,368, seven pods (asserted, R2) |
| Expirations as they now stand in the registers, their history in the orders | CMS and the Clerk's system | registers, `circuit_court_term_orders_2016_2026.csv` | every expiration read as it now stands | 1,389, seven pods (asserted, R2) |
| Term length as it now stands (term_months, TERM_DAYS), the term in force on each date in the orders' term_months_after | CMS and the Clerk's system | registers, orders | each window's room read off the term as it now stands, or off the term imposed | a lower step on the golden's own path, ruled out by the code table's note and the orders (SF17): as it stands 973, five pods; imposed alone 1,363, seven pods, the same call |
| Terms still in their confinement condition are in neither register | CMS enters a term when supervision begins | both registers | new supervision starts from the trailing six months | 1,425, seven pods (asserted, R2) |
| One booking at a time, reclassified when the order arrives, UTC from 2025 | the jail management system | `detention_probation_bookings_2019_2026.csv` | the call reads no booking | none (Ask A's ground) |
| CMS 2's intake_office kept at intake; the personnel export of 2 October 2026 holding the caseload redistribution of 1 October | CMS 2, the personnel system | `cms2_supervision_cases_2023_2026.csv`, `apd_officer_assignments_2016_2026.csv` | the call reads no office | none (Ask B's ground) |
| Merged Sheriff's numbers | the Sheriff's records unit | `person_id_crosswalk.csv` | the call reads none | none |
| Misdemeanor terms and interstate holds in the same records | CMS, the jail | registers, bookings | a felony filter by level | none |

## Default path

1. Read SB 26-118 and the Board's instructions: the plan carries the felony probation revocation admissions of 2027 and
   staffs violator pods by the county's standard (one 64-bed pod for each 210 admissions or part of 210).
2. Conform CMS 1 and 2 (layouts, codes, scales), the term orders and the petitions by case number; keep the felony terms
   and count each term's exposure from 1 July 2016, the extracts' first day.
3. Set each term's end under the Act: a running term at the earlier of its scheduled expiration and the later of 24
   months after supervision began and 31 March 2027; a new term 24 months; no extension past 24 months.
4. Fit the field's two clocks: petitions by month on supervision, and the petitions and extensions in each term's last
   months before its expiration in force (architecture 3's construction, which both of its readers built).
5. Carry each open term to its end under the Act at those rates, the end-of-term extensions capped (a capped term ends),
   the pending petitions at their conversion and new starts at the trailing year's rate.
6. Sum the commitments dated in 2027: 911, five pods.

Ends on: five violator pods for 911 felony probation revocation admissions in 2027 (the trailing year carried 827).
Golden: seven pods for 1,424: the record's end-of-term petition rate (17.0 per cent) is earned by terms that could mostly
be extended (6.0 per cent of those with room draw a petition, while 53.5 per cent of them are extended); the Act leaves
no capped term any room, and the terms at their class maximum show the rate such terms file at (38.7 per cent), so
every capped term ending in 2027, the 3,114 terms section 4 ends on 31 March first, files at that rate.

## Stump sentence

A competent solver builds the two-clock projection with the record's pooled end-of-term petition rate, caps the
extensions under SB 26-118 and files 911 admissions (five pods); the step that lands it there is reading the end-of-term
rate off terms that could mostly still be extended, when the Act leaves no capped term any room and the terms already at
their class maximum show the rate such terms file at, so the plan staffs seven pods (1,424 projected).

## Build world

`generator/world.py`: felony and misdemeanor terms imposed from January 2008 (218 and 150 a month), so the record opens
on a settled caseload. A felony term's class and length are drawn together from the State's table (drug felony class 4
at 18 or 24 months, class 6 at 18 to 36, class 5 at 36 or 48, class 4 at 48 or 60, classes 3 and 2 at 60 or 84), 18 per
cent of each class but class 2 imposed at its maximum; misdemeanor terms run 12 months, class 1 (longest term 24 months)
or class 2 (12). 85 per cent of felony terms carry a confinement condition served before supervision begins. Ordinary
petitions arrive on a monthly hazard falling from 2.6 to 0.6 per cent over the first year and a half on supervision,
scaled by the risk screen. As a term reaches its last 90 days, 75 per cent of felony terms still have a matter open: a
term with room under its class maximum is then extended 6 to 18 months (75 per cent of those) or petitioned (3 per
cent), a term with none draws a petition on 50 per cent (the 3 per cent and 63 per cent of the would-be extensions).
Continued petitions extend within the room left, warrants toll, compliant terms end early after 18 months. 48 per cent
of petitions end in a revocation some 70 days after filing. The Department's officers carry the terms (four offices,
Eastfield opened on 2 June 2025 with the eastern townships' terms, residential moves and Central's specialized
caseloads transfer terms); the jail books a held probationer's commitment only when the order reaches it. The truth is
the generator re-run from every term's state at the extract under the Act, eight times: 1,409 (sd 39). `golden.py`
computes every route from the cut pack alone and `checks.py` asserts the table.

| Route | Admissions 2027 | Pods |
|---|---|---|
| Persistence (the trailing year) | 827 | 4 |
| The trailing year's rate over the Act's exposure | 559 | 3 |
| Time on supervision by term length | 488 | 3 |
| Time on supervision with the risk score | 503 | 3 |
| Two clocks, every term ending once at the pooled end-of-term rate | 884 | 5 |
| Two clocks at the pooled end-of-term rates, extensions capped (default) | 911 | 5 |
| Section 5 not applied (room under the class maximum alone) | 931 | 5 |
| The term in force read as it now stands | 973 | 5 |
| The lost extensions shared between petition and lapse in proportion | 1,140 | 6 |
| The extended terms' second windows left out | 1,335 | 7 |
| The class maximum read on the term imposed alone | 1,363 | 7 |
| Every lost extension a petition | 1,780 | 9 |
| The capped terms at the at-maximum rate (golden) | 1,424 | 7 |

## Readability screen

Measured on the cut pack (`checks.py` restates the figures on each build).

| Rung | What the response does | What in the pack points at it | Verdict |
|---|---|---|---|
| L0 persistence (827, four pods) | carries the trailing year's admissions into 2027 | the petitions' revocations by month, the annual report's counts | readable |
| L1 rate over the Act's exposure (559, three pods) | the trailing year's admissions per month on supervision, over the months the Act leaves in 2027 | the registers' supervision months | readable |
| L2 time on supervision with the risk score (503, three pods) | the field's survival projection, each term cut at its end under the Act | the registers, the petitions, the Act | readable |
| L3 two clocks, every term ending once (884, five pods) | architecture 3's construction at the pooled end-of-term rate | the petitions aligned on the expiration in force | readable |
| L4 two clocks with the extensions capped (default; 911, five pods) | both architecture 3 readers' route: the record's end-of-term petition and extension rates, each extension the Act forbids taken as the term's end | section 5, the EXTENSION orders near term ends | readable |
| L5 the lost extensions shared in proportion (1,140, six pods) | the forbidden extensions split between petition and lapse as the record splits its other end-of-term outcomes | the same rates | readable |
| L6 every lost extension a petition (1,780, nine pods) | every forbidden extension filed as a petition | the same rates | readable |
| G the capped terms at the at-maximum rate (decisive; 1,424, seven pods) | splits the record's end-of-term windows by whether the term in force had reached its class maximum and carries every term the Act leaves no room at the no-room rate | nothing labels a term's room or a petition's reason: no column holds either, end-of-term petitions carry the ordinary allegations (largest share gap 0.004), the code table gives each class's longest term and the orders the extensions; the split shows only when each window's term in force is set against its class maximum (38.7 against 6.0 per cent, every class at its maximum 36 to 42), while class alone or imposed length alone moves the end-of-term rate by at most 0.090 | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | an admission | a person's commitment on a day a felony term was revoked | each revoked petition | same call (one felony revocation a person and day; asserted) | instructions 3.1 |
| SF2 | how a felony commitment is served | consecutively, from the order | on weekends | same call (no felony commitment is served on weekends; asserted) | the petitions' served_as |
| SF3 | the day an admission is dated | the day the court orders the commitment | the day the jail books it, up to seven days later for a probationer it already held | same call (asserted: every commitment booking begins on its order day or within the week) | instructions 3.1 |
| SF4 | terms whose supervision begins after the extract | counted | left out | another call (1,247, six pods) | instructions 4.2 |
| SF5 | 24 months after supervision began | calendar months (the same day of the month two years on) | 730 days | same call (3,114 transition terms either way and the same pods; asserted) | the Act, section 4 |
| SF6 | a running term's end under section 4 | the earlier of its scheduled expiration and the later of 24 months after supervision began and 31 March 2027 | a term expiring on its own schedule between January and March 2027 carried to 31 March (the reading an earlier proviso allowed, at most 60 admissions and the same call) | not a reading the text allows (section 4 states the earlier and the later; asserted) | the Act, section 4 |
| SF7 | proceedings pending on the day a term ends under section 4 | continue | end with the term | another call (834, four pods) | the Act, section 6 |
| SF8 | the extract | petitions pending at 30 September 2026 carried as pending | none | same call (asserted) | instructions 1.2 |
| SF9 | or part of 210 | a ceiling: 6.78 pods is seven | rounding to the nearest pod | same call (6.78 rounds to seven too; asserted) | instructions, Annex |
| SF10 | what the plan carries | the pods the projection calls for under the standard | a projection rounded to a plan figure | closed: no shipped text sets a rounding for the projection and the call is the pods (asserted) | instructions 2.2, 4.3, the prompt |
| SF11 | a felony admission | a revoked term is a felony term | a felony probationer's commitment (PV-FEL) | same call (32 a year more; asserted) | instructions 3.2 |
| SF12 | the end-of-term window and the estimator's other choices | 120 days, no score, a rate per kind, the record's lags, 12-month extensions | 90 to 150 days, the score, one rate, the mean lag, windows opening before 1 January 2027, terms with nothing pending, 9-month or capped extensions | same call (1,413 to 1,463 over the extreme combinations, the extended terms' second windows left out 1,325 and 1,335; asserted) | the record |
| SF13 | an extension from 1 January 2027 | none past the term's end under sections 3 and 4 | any within the class maximum | another call (931, five pods) | the Act, section 5 |
| SF14 | a class's maximum | the code table's longest term for the class | none | same call (no term in force exceeds it; asserted) | the Clerk's code table |
| SF15 | at the maximum | the term in force equals its class's longest term | less than a month of room left | same call (terms run in whole months; asserted) | the code table |
| SF16 | on supervision at the extract | open at the end of 30 September 2026 | open at any time that day | Ask B only: 5 felony terms closed that day | instructions 1.2 |
| SF17 | a window's room | the class's longest term less the term in force when the window opened (imposed plus the extensions ordered before) | the term imposed alone; the term as it now stands | imposed alone the same call (1,363, seven pods); as it now stands another call (973, five pods) | the code table's note (no order imposing or extending a term may set it longer) and the orders' term_months_after, the term in force on each date |
| SF18 | the office supervising a term at the extract | its officer's office in the assignment in effect on 30 September 2026 | CMS 2's intake_office; the officer's open row in the export of 2 October, which holds the redistribution of 1 October | Ask B only (0 and 1 of 16) | instructions 6.1 (each office supervising them at the extract), the column's name, the roster's dates |
| SF19 | time on supervision | completed years from the day supervision began | 365.25-day years | Ask B only | instructions 6.1 (filed) |

## Ladder

Measured on the cut pack; `checks.py` asserts every row on each build.

| Rung | Admissions 2027 | Pods | Call kept |
|---|---|---|---|
| L0 persistence | 827 | 4 | no |
| L1 the trailing year's rate over the Act's exposure | 559 | 3 | no |
| L2 time on supervision with the risk score | 503 | 3 | no |
| L3 two clocks, every term ending once | 884 | 5 | no |
| L4 two clocks, extensions capped (default) | 911 | 5 | no |
| L5 the lost extensions shared in proportion | 1,140 | 6 | no |
| L6 every lost extension a petition | 1,780 | 9 | no |
| G the capped terms at the at-maximum rate | 1,424 | 7 | yes |

Every rung that skips the decisive step sits under the rung floor below the golden's pods (1,260 over 1.09 is 1,156),
the proportional reallocation the closest at 1,140, or above the seven-pod ceiling by more than a tenth (every lost
extension a petition, 1,780 against 1,617). The standing family runs 1,414 to 1,443 one choice at a time and 1,413 to
1,463 at its extreme combinations, all seven pods; leaving out the extended terms' second windows files 1,335 (1,325 at
the low extreme), seven pods. Two lower steps sit on the golden's own path, both filed: section 5's bar (without it 931)
and the term in force at each window (as it stands 973; imposed alone 1,363, the same call). The golden sits 164 over
six pods' cover and 46 under seven's: the three judge threads' own rebuilds ran from 153 under the golden to 12 over it,
and the steepest upward stack of standing choices adds 39. The truth is 1,409 (sd 39 over eight runs), 1.0 per cent
under the golden and in its seven pods.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | felony revocation admissions on terms the Department supervises, terms beginning supervision after the extract included | filed (instructions 3.1, 3.2, 4.2); SF4, SF11 |
| 2 | Unit of account | a person's commitment, counted once on the day the court orders it | filed (3.1); SF1, SF3 |
| 3 | Attribution window | calendar 2027, by the day the commitment is ordered | filed (1.1, 3.1); SF3 |
| 4 | As-of dating | records to the end of 30 September 2026 | filed (1.2); SF8, SF16 |
| 5 | Version basis | the one set of extracts pulled 2 October 2026 | C1 |
| 6 | Denominator | exposure while the extracts can see it, from 1 July 2016; each end-of-term window by its term in force | the survival method (delayed entry); SF17 |
| 7 | Weighting | none | not applicable |
| 8 | Window length | the plan year; the end-of-term window 120 days | filed (1.1); SF12 |
| 9 | Boundary inclusivity | one pod for each 210 or part of 210; at the maximum when the term in force equals the longest term | filed (Annex, code table); SF9, SF15 |
| 10 | Rounding path | pods from the unrounded projection; no plan figure is rounded from it | filed (4.3, Annex); SF10 |
| 11 | Tie-break | none needed | asserted: every standing construction 1,413 to 1,463, seven pods |
| 12 | Maturity and censoring | open terms and pending petitions at the extract; windows open at the extract left out of the rates | the decisive step; SF8 |
| 13 | Order of operations | apply the Act, split the record's windows by room, project, sum, apply the standard | linear |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | one row per term, order, petition and booking | asserted (unique numbers) |
| 16 | Identity normalisation | case numbers across both systems and the orders; Sheriff's numbers through the crosswalk, merged numbers included | asserted |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | admissions; terms in months (CMS 1 in days); county (Central) time | filed (instructions 1.3; the new system marks UTC) |
| 19 | Code and status semantics | dispositions, order types, closure codes, classes (CMS 1 hyphenated), booking classes | filed (code lists); SF11, SF14 |
| 20 | Integerisation | pods as whole units | filed (Annex) |
| 21 | Clause scope | felony terms; the Act leaves misdemeanor terms; section 5 binds every order from 1 January 2027 | filed (the Act, sections 5 and 7); SF13 |
| 22 | Forward window contents | the Act's ends, terms beginning supervision later, pending petitions, proceedings pending at an end, no extension past an end | filed (the Act 3 to 6, instructions 4.2); SF4, SF7, SF13 |

## Literal reader

Executing the prompt and every filed sentence word for word: the Board's instructions define the admission (3.1, 3.2)
and the projection (4.1: under the law in force in the plan year, with the courts, the Department and the Sheriff acting
as the records to the extract show them acting; 4.2: terms whose supervision begins after the extract included), the Act
sets every felony term's end and bars any order setting it later (sections 3 to 6), the code table gives each class's
longest term and the Annex the pods. Acting as the records show includes what a term does as it runs out: the record
shows terms with room extended and terms without it petitioned (38.7 against 6.0 per cent with a petition), so a
projection that gives the capped terms the record's pooled end-of-term rate acts as if the extension were still there,
which the law in force forbids. Every standing construction files 1,413 to 1,463 admissions and seven pods, which is
what instructions 4.3 ask the plan to state. Section 6 keeps the 31 March terms' pending petitions revocable (without it
834), section 5 removes the room (without it 931) and section 4.2 counts the terms beginning supervision after the
extract (without them 1,247), so each is filed rather than left to a reading.

## Oracles

No file ties only under the golden or only on a wrong read. The Department's fiscal 2025 report counts petitions,
revocations and closures and its caseload by risk level at intake from the shipped rows (asserted) and forecasts
nothing; it carries no office breakdown. The headcount is the jail's own 06:00 count by housing unit and answers
occupancy, not the projection or the bed-days (it counts at 06:00, by housing unit, holds and interstate holds
included). Nothing in the pack forecasts 2027, ranks a method or names a term's room. The referee for Ask A is the
court's revocation and the day it orders the commitment, the device's evidence and never an answer; for Ask B, the
officer assignments in effect on 30 September 2026.

## Ask sheet

The call's declared population is the felony terms of CMS 1 and 2 with their term orders and petitions; the bookings,
the crosswalk, the officer assignments, CMS 2's office and officer columns, the misdemeanor terms and the headcount are
outside it (asserted: the call reads no booking, office or officer). The annual report and the headcount ship as
distractors: the plan counts admissions by the instructions' definitions, not the report's fiscal-year counts or the
06:00 occupancy, and no golden figure opens them.

- **Ask A, violator bed-days by quarter, October 2025 to September 2026, felony and misdemeanor, whole days (8
  figures).** H18 home: the instructions' section 5, the violator housing in use that the pods add to. User: the
  Detention Center commander. Primary device (silent): a commitment begins when the court orders it, but the jail keeps a
  probationer it already holds on the warrant hold (PV-HOLD) until the commitment order reaches its records unit, the
  same afternoon or up to five business days later, and only then reclassifies the booking to PV-FEL or PV-MIS; the
  nights between are violator bed-days on a hold booking (4,157 such commitments in the bookings, some in every quarter
  and level, and a person revoked on 28 September 2026 still on the hold at the extract). Secondary (v3's device, kept):
  the jail books by status, so a felony probationer committed on a misdemeanor revocation is booked PV-FEL and is a
  misdemeanor bed-day (32 a year). Hazards: UTC in the new system, one booking at a time (annex moves, the 2025
  replacement), merged Sheriff's numbers, holds and interstate holds left out. Stops measured on the cut pack: linked to
  the court for the level but counted from the commitment booking 0 of 8; the classification as the level 0 of 8, with
  UTC read as local 0 of 8, with holds counted 0 of 8; linked with UTC read as local 0 of 8.
- **Ask B, the felony probationers on supervision at the extract in each supervising office by time on supervision
  (under one year, one to two, two to three, three or more), whole numbers (16 figures).** H18 home: the instructions'
  section 6, the caseload the Act shortens, by the office that will absorb it. User: the Chief Probation Officer. Primary
  device (silent): the office supervising a term at the extract is its officer's office in the assignment in effect on
  30 September 2026, and the personnel export, pulled on 2 October, already holds the Department's caseload
  redistribution of 1 October 2026 (seven officers moved with their caseloads out of Central, Riverside and Northgate),
  so each officer's open row is the office from 1 October; nothing narrates the redistribution, the dates alone show it.
  CMS 2's intake_office is the office that took the term in (Eastfield on its opening, residential moves and Central's
  specialized caseloads move terms after intake), which is why instructions 6.1 can say each office supervising them
  without naming a file. Stops measured on the cut pack: the officer's open row as exported 1 of 16; CMS 2's
  intake_office 0 of 16; the officer's first assignment 4 of 16; the officer's office when supervision began 2 of 16.

| Ask | What the cracker does | Cracker |
|---|---|---|
| A | links each commitment booking to the court's revocation for its level, county time from UTC, annex moves and reclassifications chained, counted from the commitment booking | misses |
| B | joins each open felony term's officer to the roster and takes the officer's open assignment as exported, completed years on supervision | misses |

Measured by: `generator/ceiling.py` on the cut pack.

| Ask | Graded figures | Cracker keeps | Mirror keeps | Naive handling keeps | Cracker |
|---|---|---|---|---|---|
| A violator bed-days by quarter and level | 8 | 0 | 0 | 0 | misses |
| B probationers by supervising office and time on supervision | 16 | 1 | 1 | 0 | misses |

Over the 24 figures the cracker keeps 4.2 per cent of ask weight (47.3 with the call) and the mirror the same off it
(14.3); the best half-handled stop keeps 4 of 24 (the officer's first assignment). A reader who finds Ask B's device
alone keeps 16 of 24 (66.7 per cent), Ask A's alone 9 of 24.

Pair ceiling: 30.8.
Mirror leakage: 4.2 per cent of ask weight.
The rubric's criteria: the call, the projection's seven-pod band, the transition terms, the end-of-term split and the
default construction ruled out (5), the 24 ask figures, the memo's section and the chart (2) and the whole-day rounding
(1), 32 in all.

## Stage 4 (architecture 4)

Run under the rule of 27 October (no solver, scored reader or probe on any build): the isolated leak reader and the
determinism judge only.

- Round 1 on zip 4066ee80. The leak reader quoted nothing for question 1, every question 5 sentence fixes the estimand
  (3.1, 3.2, 4.1 to 4.3, 5.1 to 5.3, 6.1, the Act's sections 2 to 7), and question 6 reads analytical; its one realism
  note (the enrolled Act short and tidy) was answered with a legislative declaration in section 1 and a safety clause in
  section 9, no section renumbered and no rule changed. The judge's thread (pass 2) returned DETERMINISTIC, APPROVE,
  Gate G forecasting and analytical_non_defect, Gate H domain, layers and decisive step all passing, the open terms,
  the 3,003 transition terms, the trailing 833 and all 16 Ask B cells reproduced exactly. Its residual points were all
  taken in one generator pass: the Act's 24 months read as calendar months (730 days files the same call, SF5); the
  county's standard on file set at one pod for each 210 admissions, so its own cruder rebuild (about 1,320) and every
  standing variant file seven pods with a margin of 110 or more over six (1,260); the write-up's construction-dependent
  figures (the parts in block 4, the exact window counts in the steps, the capped-term split) replaced by statements every
  standing variant shares, and the open terms' four groups defined strictly (2,457 ended at 24 months, matching its
  count); instructions 5.2 now count a person serving a commitment on weekends at each midnight spent in the jail.
- Round 2 on zip 2b591366 (two documents changed, so both ran again). The leak reader again quoted nothing for
  question 1 and read question 6 as analytical, with no realism tell. The re-judge (pass 3) returned DETERMINISTIC with
  a solution-side FIX_NOW: all eight bed-days and all 16 office cells reproduced exactly, the at-maximum split at 38.5
  per cent (the same in every class, drug felony class 4's 24-month maximum included), its own projection 1,357 to
  1,395 (seven pods, 1,400), Gate G forecasting and analytical_non_defect, Gate H passing, stump power strong. The
  FIX_NOW: the projection's parts committed with their admissions in block 4 (done, as built, adding to 1,383). Also
  taken: section 4 restated as the earlier of the scheduled expiration and the later of 24 months and 31 March 2027, so
  its former proviso cannot be read to carry terms expiring in early 2027 to 31 March (at most 60 admissions, the same
  call); block 1 no longer cites the 2026 pods; step 5 lists the two extension-length variants. Left as the judge left
  it: the golden already carries each term off as it is revoked or terminated early at the record's rates (step 4 now
  says so), and a build that removes terms again at the record's whole closure rate (about 1,300, seven pods) is refuted
  by its own back-test (the projection without the second removal predicts the 2026 petitions within 1.4 per cent, with
  it 3.9 per cent short); Ask B's office reading is the officer's office, the only file that places an officer in an
  office on a date.
- Round 3 on zip 9d45538d (section 4 of the Act changed, so the reader ran again; the pack has not moved since). The
  leak reader again quoted nothing for question 1, found no file that ranks or forecasts 2027 and read question 6 as
  analytical; its residual note (sections 4 and 6 with instruction 4.2 as a ladder of rules) is the filed estimand,
  since executing those rules leaves open the end-of-term rate a capped term files at. The same pass corrected the
  golden memo's pod counts (every lost extension filed as a petition is nine pods under the 210 standard, not eight;
  every pod word now comes from the figures and verify checks them), and made the write-up literal where a cold judge
  would read it: step 2 states the Act's end rule word for word, step 4 says each term leaves the projection as it is
  revoked or terminated early and that an extended term runs 12 months more or to the latest end the Act allows, and
  block 4 names the no-room group as the Act or the class maximum. The re-judge of the FIX_NOW (pass 4) on the same
  zip returned NOT_DETERMINISTIC, SEND_BACK, on margin fragility: its own cruder rebuild filed 1,282 to 1,350 (1,230
  with the extended terms' second windows left out) against the golden's 1,383, and the world's truth was 1,335, so the
  plan figure to the nearest 100 sat 33 over its rounding line under a method spread of about 115; its other surviving
  readings were the 6-pod proportional reallocation, Ask B's office (CMS 2's column against the officer's), and
  completed years against 365.25-day years; its Q1 2026 bed-days (felony 44 over, misdemeanor 20 under) came from
  chaining separate commitments across release gaps of up to three days, which counts nights out of the jail, and
  pass 3 had reproduced all eight. Stump power, Gate G and Gate H passed again. Repaired in the generator the same
  day, the decisive step untouched: the call is the pods alone (the prompt asks no admissions figure, instructions 4.3
  ask the units the projection calls for, the write-up states the projection as the band seven pods cover); the felony
  intake moved from 209 to 218 a month, which places the golden at 1,424, 164 over six pods' cover and 46 under
  seven's, with the truth at 1,409; the write-up names the record's own 24-month terms (drug felony class 4 at its
  maximum files at 38.9 per cent, every class at 36 to 42) against the proportional reallocation; CMS 2's office column
  is renamed intake_office, which is what it holds, and 6.1 files completed years; Ask B's device moved to the
  personnel export's redistribution of 1 October 2026 (the open row keeps 1 of 16).
- Round 4 on zip 2cea3299 (the prompt and two documents changed, so both ran again). The leak reader quoted nothing for
  question 1, found no file that ranks or forecasts 2027 and read question 6 as analytical, with no planted decoy; its
  realism notes (the jail's V PODS 1-5 unit and a tidy annual report) are the county's own records. The judge (pass 5)
  returned DETERMINISTIC, APPROVE: seven pods forced by the shipped files, no competing answer standing (the pooled rate
  five pods, the trailing year four, the proportional reallocation six ruled out by the at-maximum evidence in every
  class, drug felony class 4 at 39.0 per cent), the open terms, the 3,114 transition terms, the trailing 827 and all 16
  Ask B cells reproduced exactly, Gate G forecasting and analytical_non_defect, Gate H passing, stump power strong. Its
  caution on Ask A's whole days (its own rebuild within 0.2 per cent on felony and 2 to 5 per cent short on misdemeanor)
  stands answered on the record: the independent verifier and pass 3's thread reproduce all eight, only 2 of 8,311
  commitments run past their days ordered plus one (both before the window), the window's two stays holding a second
  order are felony throughout under 5.3, and the misdemeanor shortfall in every quarter is the weekend stays 5.2 counts;
  step 6 of the write-up now names both.

## Pre-ship check

- Rule 1: the deciding quantity is the field's forecast of felony probation revocations, built from petition hazards,
  conversion and lags, and decided by which terms' end-of-term behaviour the capped terms will follow; swapping the
  nouns breaks it (no other field has a class maximum, a court's extension and a petition that keeps jurisdiction).
- Rule 2: Layer 1 is what the county's systems write (two CMS layouts, classes hyphenated in CMS 1, terms in days, the
  orders' history, one booking at a time, the order reaching the jail after the hearing, UTC from 2025, merged numbers,
  CMS 2's intake office, the roster's redistribution of 1 October); no mishandling of it moves the pods (R2: 1,424, 1,389,
  1,425). Layer 2 is the comparison group for the capped terms, and the at-maximum split is what moves the call (911
  pooled to 1,424).
- Rule 3: nothing is planted (the terms at their maximum are what the class table and the extensions produce for every
  term), every field read correctly still files 911, and every filed rule executed on the pooled projection still files
  five pods; the decisive step is analytical, as both leak reads and the judge's Gate H found.
- Gates on the shipped zip (2cea3299): checks 103, verify 28, figures_check 79, precut 52, the prompt gate, leak.py
  REVIEW answered, guard heart WARN answered, surface clean, containers clean, two builds byte-identical.

## Earlier architectures (kept as history)

**Architecture 3 (drawn 2026-10-27, spent at stage 4 round 1 the same day).** The same world without classes: ordinary
petitions by month on supervision and end-of-term petitions in the last 90 days before each term's expiration in force,
the Act moving every expiration and ending 3,373 terms on 31 March 2027; golden 1,186 (1,200, six pods), default 607
(three pods). Both scored readers modelled petitions by tenure and days to the expiration in force and landed 1,200 and
six pods, keeping 14 and 16 of the 16 ask figures (the PV-FEL commitments linked to the revoked terms, the EXTENSION
months taken off term_months); the judge returned DETERMINISTIC with a wording FIX_NOW. Its full note is at 1976a763.

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
- 2026-10-27, architecture 4 at intake 217 felony terms a month: the golden filed 1,403 and the standing family's top
  combination (a 150-day window, only windows with nothing pending, the mean lag) 1,445, 5 under the 1,450 edge of the
  plan figure's rounding; intake set to 209, which centres the family at 1,370 to 1,428 around a golden of 1,383.
- 2026-10-27, Ask B with residential moves as the only transfer after intake: the first-year band separated the two
  office readings by 0 to 11 terms and one cell (Riverside, under one year) was equal under CMS 2's office; Central's
  specialized caseloads (10 per cent of felony terms, moved after the intake assessment) now separate all 16 cells.
- 2026-10-27, the officer roster with badges issued in the order the posts were generated: a 2026 hire held badge 1143
  beside 2003 hires at 1167, which no personnel system does; badges are now issued in order of hire.
- 2026-10-27, the plan figure to the nearest 100 (stage 4 pass 4, zip 9d45538d): the judge threads' own rebuilds ran
  from 153 under the golden of 1,383 to 12 over it, around a truth of 1,335, so a 100-wide bin cannot hold an
  open-method forecast whose reasonable builds spread about 115; the call is now the pods alone, the projection stated as
  the band seven pods cover, and the felony intake set to 218, which places the golden at 1,424 inside that band with
  room on both sides for the same spread.
- 2026-10-27, Ask B on CMS 2's office column (pass 4's surviving reading): no shipped text said the column was the
  intake office, so the column now carries that name and 6.1 files completed years; with the office then found from the
  roster, the device moved to the personnel export's redistribution of 1 October 2026, where an officer's open row is
  the office from that day.
