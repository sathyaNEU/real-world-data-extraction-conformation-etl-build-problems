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
| Shape | `02` (forecast across periods): the call (pods and the plan figure), its parts and its 2027 profile by month in the chart, and the asks (violator bed-days by quarter and level; felony probationers by supervising office and time on supervision) |
| Decision | `quantity_figure` (the plan's 2027 admissions, from which the filed standard sets the violator pods), answer unit `count` |
| Mechanism | gap population (decisive: the record's end-of-term petition rate is measured over terms that could mostly still be extended, the plan year's capped terms cannot) then time (the plan year runs under a rule the window never applied to most terms); pattern none, generators G11 (the extension's precondition, room under the offense class's statutory maximum, which the Act removes from every capped term) then G13; Gate G `forecasting`; strategy `population_selection` |
| Layer 2 family / pattern | `estimand_identification` (the right comparison group for the capped terms' end-of-term behaviour: the terms already at their class maximum); `own:end-of-term-petitions-where-no-extension-room-remains`. The client library's recidivism cards (calibration, fixed follow-up and time at risk, the fairness criterion, later release cohorts, selective labels, local base rates) are the default path's careful moves; the two-clock projection at the record's own rates is architecture 3's golden and here the default |
| Furniture | forum `council_or_assembly` (the County Board of Supervisors adopts the plan), forcing event `statutory_or_regulatory_filing` (the 2027 Jail Operations Plan is due to the State Jail Standards Board on 1 December 2026), organisation family `local_government`, role family `research_desk` (the Sheriff's Office jail planning analyst), context artifact `capacity_report` (the Detention Center's daily 06:00 count by housing unit, the five violator pods in use), calibration `none`, opening `question-first`, question form `how-many` |
| Spine | `detention_probation_bookings_2019_2026.csv` (about 48,000 rows), the Detention Center's probation bookings, one booking at a time per person, an annex move, a reclassification and the 2025 system replacement each writing a new row; synthetic |
| Deliverables | `violator_housing_plan_2027.xlsx` (the projection and how it is built, the pods, the asks), `violator_housing_memo_2027.docx` (the plan's violator housing section), `felony_revocation_admissions_2019_2027.png` (monthly admissions and the 2027 projection) |
| People | drawn with `guard.py names --geo us --seed 141 --n 30` for architecture 3 and kept: Gina Yoder (Sheriff's Office jail planning analyst), Larry Pugh (Chief Probation Officer), Colleen Cameron (Detention Center commander), Donald Russo (Probation research and data manager), Megan Chambers (Clerk of the Circuit Court), Gloria Lynch (County Budget Director); none appears in the prompt |

**Guard.** The first card (strategy `composition_mix`, decisive G14) BLOCKed on `ban.strategy` against task304 and on
`test.same_puzzle_older` and `test.same_driver_older` against six and four builds carrying gap population with G14, so
the decisive pattern is G11, the honest one: the gentler outcome at a term's end (an extension) has a precondition, room
under the class maximum, and the Act removes it from every capped term; the strategy is `population_selection`, the rate
being read off the sub-population that already lacks the room. After registration `ban.artifact` BLOCKed
`filed_standard` against task204, filed inside the window meanwhile; the context artifact is the jail's daily headcount
(`capacity_report`), which answers occupancy correctly and is the file the 2026 pod count comes from. WARNs answered:
`driver.near` 0.14 is this slot's own architecture 3 (its step was the timing of the end-of-term petitions, a lower rung
here; the differentiation is on the card); `repeat.gate_g` and `overuse.gate_g` are the lane's objective (a forecast
call carries Gate G `forecasting`); `repeat.decision` (task204) and `repeat.question_form` (task157) are a count on a
different objective and a different domain.

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

**World.** Okelan County (fictional, an unnamed state on Central time) supervises about 7,600 felony probationers. Under
the State's 2019 realignment a felony probation revocation is served in the county of supervision, so every felony
revocation is a commitment to the Okelan County Detention Center. A felony term's length is set within its offense
class's statutory maximum (Class 2 96 months down to drug felony Class 4 24 months), and the court may extend a term
within that maximum. Officers file violation petitions through the term, and as a term runs out they review it: a matter
still open (restitution, fees, unfinished treatment, a pending case) is met by asking the court to extend the term where
it has room under the maximum, and by a violation petition, which keeps the court's jurisdiction, where it has none.
Senate Bill 26-118 takes effect on 1 January 2027: a felony term runs no more than 24 months from the start of
supervision, a term in effect ends on the earlier of its scheduled expiration and 24 months after supervision began but
not before 31 March 2027, and no court may extend a felony term past 24 months; proceedings pending at a term's end
continue. The Sheriff's Office writes the 2027 Jail Operations Plan, which states the felony probation revocation
admissions it projects and staffs violator pods by the county's filed standard (one 64-bed pod for each 220 projected
admissions or part of 220). Records to the extract of 30 September 2026; the extracts begin on 1 July 2016.

**Data-native sentence.** In Okelan County's record a felony term reaching its last months with a matter still open is
extended when it has room under its class maximum and violated when it has none: about 37 per cent of the terms
reaching their last 120 days at their class maximum draw a petition, against about 6 per cent of the terms with room and
16 per cent of all terms, and SB 26-118 leaves no capped term any room.

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
  classes, the Act's sections) still leaves the two-clock projection at about 940 (five pods); no column or code marks a
  term's room to extend or a petition filed for want of it, and the room appears only when each term's term in force is set
  against its class maximum.
- Not rule application: SB 26-118 sets every term's new end and bars extension past 24 months, the class maxima set the
  room, and the standard turns admissions into pods; executing all of them on the two-clock projection with the extensions
  capped files five pods. No rule or document says what an officer files when an extension is unavailable. Measured on a
  prototype of the world (to be restated on the cut pack): the enumerated family (persistence about 860, the projection by
  month on supervision about 530, the two clocks at the pooled end-of-term rate about 940, the extension share reallocated
  in proportion about 1,170, every would-be extension a petition about 1,830, the two clocks with the capped terms at the
  at-maximum rate about 1,450) spreads three to nine pods; the standing family (the end-of-term window from 90 to 150 days,
  the score as a covariate or not, one conversion rate or two, the mean lag or the record's lags, the 31 March terms'
  windows from 1 January 2027 or before it) spreads 1,434 to 1,461, every one seven pods; the ruling-out is one comparison
  nothing invites, the end-of-term petition rate of the terms at their class maximum against the rest.
- Analyst test: a strong analyst who conforms the two layouts, the orders, the petitions and the commitments, applies the
  Act to every term (its new end, no extension past 24 months) and builds the two-clock projection at the record's own
  end-of-term rates with the extensions capped, files about 940 admissions (five pods), against the golden's about 1,430
  (seven pods); persistence files about 860 (four pods).
- Estimand: felony probation revocation admissions to the Okelan County Detention Center in calendar 2027 (a person's
  commitment on the revocation of a felony term the Department supervises, counted once on the day the court orders it),
  including admissions on terms whose supervision begins after the extract, under SB 26-118 as enacted, with the courts,
  the Department and the Sheriff acting as the records to the extract show them acting; filed in
  `jail_operations_plan_instructions_2027.pdf` sections 3 and 4.
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
| CMS 1's layout: MM/DD/YYYY, one-letter offices, terms in days, risk screen version 1 totals 0 to 40 | the legacy case system | `cms1_supervision_cases_2016_2023.csv` | version 1 totals read as version 2 | the golden reads no score: unchanged (to measure) |
| Term and expiration as they now stand in the registers, their history in the orders | CMS and the Clerk's system | registers, `circuit_court_term_orders_2016_2026.csv` | every term read as it now stands | to measure: the room is read off the term in force at each window, so a term read as it stands moves terms between the groups |
| Terms still in their confinement condition are in neither register | CMS enters a term when supervision begins | both registers | new supervision starts from the trailing six months | to measure |
| One booking at a time, reclassified when the order arrives, UTC from 2025 | the jail management system | `detention_probation_bookings_2019_2026.csv` | the call reads no booking | none (Ask A's ground) |
| CMS 2's office kept at intake | CMS 2 | `cms2_supervision_cases_2023_2026.csv` | the call reads no office | none (Ask B's ground) |
| Merged Sheriff's numbers | the Sheriff's records unit | `person_id_crosswalk.csv` | the call reads none | none |
| Misdemeanor terms and interstate holds in the same records | CMS, the jail | registers, bookings | a felony filter by level | none |

## Default path

1. Read SB 26-118 and the Board's instructions: the plan carries the felony probation revocation admissions of 2027 and
   staffs violator pods by the county's standard (one 64-bed pod for each 220 admissions or part of 220).
2. Conform CMS 1 and 2 (layouts, codes, scales), the term orders and the petitions by case number; keep the felony terms
   and count each term's exposure from 1 July 2016, the extracts' first day.
3. Set each term's end under the Act: a running term at the earlier of its scheduled expiration and 24 months after
   supervision began, not before 31 March 2027; a new term 24 months; no extension past 24 months.
4. Fit the field's two clocks: petitions by month on supervision, and the petitions and extensions in each term's last
   months before its expiration in force (architecture 3's construction, which both of its readers built).
5. Carry each open term to its end under the Act at those rates, the end-of-term extensions capped (a capped term ends),
   the pending petitions at their conversion and new starts at the trailing year's rate.
6. Sum the commitments dated in 2027: about 940, five pods.

Ends on: about 940 felony probation revocation admissions in 2027 (five pods; the trailing year carried about 860).
Golden: about 1,430 (seven pods): the record's end-of-term petition rate (16 per cent) is earned by terms that could
mostly be extended (6 per cent of those with room draw a petition, while about half of them are extended); the Act leaves
no capped term any room, and the terms at their class maximum show the rate such terms file at (37 per cent), so every
capped term ending in 2027, the 31 March terms first, files at that rate.

## Stump sentence

A competent solver builds the two-clock projection with the record's pooled end-of-term petition rate, caps the
extensions under SB 26-118 and files about 940 admissions (five pods); the step that lands it there is reading the
end-of-term rate off terms that could mostly still be extended, when the Act leaves no capped term any room and the terms
already at their class maximum show the rate such terms file at, so the plan carries about 1,430 (seven pods).

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
