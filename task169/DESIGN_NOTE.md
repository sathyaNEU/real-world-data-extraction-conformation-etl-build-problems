# task169 design note: two-year returns of Pembroke's 2027 parole releases under Act 26-114

Architecture 2 (a fresh draw). Architecture 1 (Calvermouth's cycleway widening, urban-regional-science) was built
to stage 3 in scratch and never registered: the guard's window held it three days on its strategy, pattern,
forcing event, role and forum and on a same-driver test, and the author chose a fresh honest draw over waiting.
That draw's world, mechanism and blocked axes are not reused; its line is in `## Tried and rejected`.

## Draw

- **Cell.** Client domain Criminology & Justice, task type `recidivism-risk-assessment` (serves Forecasting &
  Predictive Modeling). Objective Forecasting: the call is the share of the people the Department expects to
  release to parole in calendar 2027 who will be admitted to prison again within two years of release, a window
  not yet open, pinned by the record of the 2019 to 2026 releases. The call faces forward.
- **World.** The State of Pembroke (fictional; its agencies, people, systems and records are fictional, the field's
  method is real). The Pembroke Sentencing and Policy Commission prepares the prison population projection the
  General Assembly's appropriations committees take in January 2027. Act 26-114 (approved 30 June 2026, in force 1
  January 2027) ends recommitment by the Board of Parole for technical violations and bars an arrest or pending
  charge as a ground of recommitment; a parolee comes back to the Department only on a new sentence of total
  confinement. Records to 30 September 2026 from the Department of Corrections (releases, admissions, the 2027
  projected-release extract), the Board of Parole (two case systems either side of its 5 January 2026 go-live),
  the Administrative Office of the Courts (case dispositions) and the State Bureau of Identification (arrests).
- **Card.** `domain` criminology-justice, `subdomain` recidivism-risk-assessment, `objective` forecasting, `shape`
  other, `decision_type` quantity_figure, `answer_unit` count (to be set to rate_or_share at the card refresh),
  `gap` [time, population], `pattern` [none], `generators` [G3, G13], `gate_g` forecasting, `calibration_form`
  none, `stump_strategy` decomposition_attribution, `context_artifact` capacity_report, `role_family`
  capacity_planner, `forum` council_or_assembly, `forcing_event` budget_or_appropriation, `org_family`
  research_or_statistics_office; `stump_class` analytical; `layer2_family` field_method; `layer2_pattern`
  own:revocation-in-lieu-of-prosecution-rerouted-under-a-conviction-only-act. People from `guard.py names --geo
  "United States" --seed 169`: Ashlee Clayton, Donald Kramer, Brandon Walter (none appears in the pack or the
  prompt; Kristy, Karen and Cassandra dropped on people.first WARNs).
- **Axes redrawn at the probe, and why the replacement is the honest one.** `context_artifact` register blocked
  against task249: the stakeholder's own file is the Department's monthly population and capacity report, so
  capacity_report. `org_family` government_agency blocked against task273: in Pembroke, as in the states whose
  sentencing commissions own the projection, the forecast is the Commission's, a research_or_statistics_office.
  `forum` committee_or_panel blocked against task249: the projection goes to the General Assembly's
  appropriations committees, council_or_assembly.
- **Guard.** `guard.py check` WARN only. repeat.question_form (how-many against task273) is answered by the
  decision; the leading question asks what share, so the card's form is refreshed to `what` at the card update,
  where the WARN against task482 is answered the same way. test.same_puzzle_older against task172 carries its
  differentiation on the card (a deadline cut against a route handed to another institution).
- **Strategy.** decomposition_attribution: every return in the record reached prison by one of two routes for the
  same behaviour (the Board's revocation on the arrest, or the court's commitment months later), whichever acted
  first; the Act closes one route, and the decisive step is how the closed route's arrests divide once they go
  through the other.
- **Shape and criteria.** The call is the cohort's rate alone (1); the districts were dropped at stage 4 round 1
  (a route without the decisive step ranked them right). Ask A, the Board's recommitments ordered in fiscal 2025-26
  and not rescinded by 30 June 2026, by district office and basis (8). Ask B, the parolee-days held on Board detainers
  in each district's county jails in each half of 2025 (8). Ask C, the days each institution's people spent out on
  court writs in each half of 2025 (10). The workbook, its three tables and the rounding (3). About 30 criteria, every
  one a cell of the prompt's shape.
- **Data-native sentence.** In Pembroke's record a parolee's arrest reaches prison by whichever route acts first,
  a Board revocation within weeks or a court commitment months later, so the record's new-commitment returns
  measure how seldom the courts got there first, not how often parolees' arrests end in prison; the arrest
  register, the court dispositions and the Board's decisions show each arrest's route, and the courts' own
  decisions on the arrests the Board left alone (and on discharged parolees' arrests) show the conversion with the
  Board out of the way.
- **Sources read, and how this differs.**
  - `layer2-rigor-patterns.md` criminology recidivism-risk-assessment 1 (calibration), 2 (fixed follow-up, time at
    risk), 4 (later cohorts), 6 (base rates): each is a lower rung or the default path here (the default path's
    model is validated by AUC, uses complete follow-up and the latest cohorts); the golden is none of them applied
    as stated. Card 2's time at risk is inside the golden (days out of Department custody) but does not decide it.
  - task134 v1 (this cell, spent): competing removals and deaths in a return forecast, and its loop-1 deaths
    (period against cohort, composition, cure models, a forward booking change as rule application). Here no exit
    is censored wrongly and nothing is restated by an order: the closed route's arrests are re-routed.
  - task141 (this cell): selective labels read through magistrates' release shares. Here no decision-maker
    selects whose outcome is seen.
  - task172 (held): a regime change makes a deadline-triggered request bind for most future units. Here a regime
    change hands one institution's share of the same events to another institution with its own conversion.
  - task163 (held): a reform's added applications at their own yield. Here nothing is added: the same arrests
    change route.
- **Screens run as code** (prototype first, scratch `proto/p3.py`; then the cut pack, `generator/checks.py` FAM and
  RIV blocks):
  - Lever: the record's new-commitment rate 6.61 per cent (step 5), with revocations as competing exits 11.02
    (step 10); the golden 20.37 (step 20); the record's return rate of every kind 52.24 (step 50).
  - Outsider spread (nine constructions of the golden family: frailty 4 and 2, pooled conversion, one class mix for
    everyone, conversion from discharged parolees only, exposure stopped at the first admission, a flat arrest rate,
    the risk score added, the last two complete years only): 18.50 to 20.87, every one on 20; the largest move 1.88 points against a lever of 9.4 to 13.8 points.
  - Subset (discharged parolees' new-commitment admissions per day, flat): 15.75, misses (the hazard falls with
    time since release and discharged time sits late). Scalar route (the record's rate over the share of arrests
    the courts decided): 10.11, misses (the record's rate is also cut by revocations removing people early).
  - Stage 4 round 1 routes, run on the cut pack (`checks.py` RIV and SF11, SF12): the readers' route (arrests that
    ended in a Department sentence per day at liberty, with the arrest-to-admission time) 12.59, misses; the courts'
    conversion on arrests counted with no time at risk 16.25, misses; the judge's crude in-window count at the
    courts' conversion with no arrest-to-admission time 21.78 and its pooled conversion 20.87 both land 20, and both
    take the decisive step (every parolee arrest at the courts' rate); the same crude count without the step 14.23,
    misses.
  - Simulated forward truth under the Act, eight redraws of the cohort's two years: 20.41 per cent.
  - Dispersion, variance-only and truncation-direction screens do not apply: the decisive quantity is a level, the
    step moves the point, no threshold suppresses a tail.

## Default path

The pipeline a strong analyst builds from the prompt, the Act and the files' grain, every filed rule applied.

1. Conform the release movement codes across the 2022 upgrade and link each 2019 to September 2024 release to
   parole to the Department's admissions (ADM movements, transfers and writs left out), keeping each release's
   first admission within 730 days.
2. Keep the returns the Act still allows: admissions on a new court commitment; Board recommitments (PAROLE
   VIOLATOR) are dropped (Act 26-114, section 3; methodology 4.2).
3. Fit a logistic model of a new-commitment admission within 730 days on age, prior commitments, offence, sex and
   district over the 35,818 complete releases (AUC 0.59), apply it to the 6,466 people on the projected-release
   extract and round to the methodology's step.

Ends on: 5 per cent (6.61 per cent unrounded)

Golden: 20 per cent (20.37)

## Stump sentence

A competent solver keeps only the returns the Act still allows, models each 2027 release's chance of a
new-commitment admission within two years on the record's complete releases and files 5 per cent (10 per cent with
revocations treated as competing exits, 12.59 per cent counting the arrests that ended in a Department sentence per
day at liberty); the step that lands it there is reading the record's new-commitment returns as what parolees' arrests
produce, when the Board answered about a third of parolees' arrests by revoking them before any court could, and
under the Act those arrests go to court and become prison commitments at the courts' own rate for their charge
grade, which puts the cohort at 20 per cent.

## Three rules

- Task type: recidivism-risk-assessment (Criminology & Justice), which serves Forecasting & Predictive Modeling:
  a release cohort's two-year return-to-prison forecast for the prison population projection.
- Domain test: the deciding quantity is the 2027 cohort's two-year return-to-prison probability, estimated the way
  a corrections forecaster builds it under a change in revocation law: the arrest process per day out of custody
  and the courts' conversion of arrests into prison commitments by charge grade, with the route each past return
  took read from the Board's and the courts' records.
- Swap: "what share of discharged patients will be readmitted within thirty days once observation stays stop
  counting" keeps a removed route but loses what decides it here: a second institution, the courts, that takes over
  the same arrests at its own conversion and timing; with readmissions nothing waits behind the closed route, so the
  record's remaining route is the forecast and the task collapses to the default path.
- Layer 1: the Department's two movement-code vocabularies across its March 2022 upgrade; admission rows beside
  transfer and court-writ movements in one table; the Bureau's state ID written with and without a hyphen before
  the check letter; amended court dispositions as later rows on a docket; cases still open at the cut; deaths from
  a probabilistic vital-records match; county names in two casings; the Board's legacy and new systems across the
  January 2026 go-live, with carried-over cases, a parallel-run fortnight, postponed hearings repeating a case's
  detainer columns and legacy detainers with no lift date when the person went to the Department; a second report
  decided at the same hearing as its own case; writ movements, some ending in a release with no return. Each is listed
  in `## Layer 1 inventory` with its R2 assertion.
- Layer 2: field_method; the methodological choice that flips the call is building the forward conviction-return
  rate from the arrests and the courts' conversion, against carrying the record's conviction-return rate.
- Decisive step: recognising that the record's new-commitment returns are what the courts reached before the Board
  did, and forecasting under the Act from every parolee arrest at the courts' conversion by charge grade, read off
  the arrests the courts did decide.
- Not semantics: every field, code and date read correctly (movement reasons, revocation bases, disposition codes,
  the Act's section 3, the methodology's 3.1 to 4.2) still leaves the default path on 5 per cent, because no field
  says what a revoked arrest would have become in court; that is an inference about the courts' behaviour under a
  regime the record never ran.
- Not rule application: the Act files which returns remain and the methodology files the cohort, the window, the
  outcome and the step; executing every filed sentence on the clean truth gives the record's new-commitment rate
  (6.61 per cent, step 5) or with competing exits 11.02 (step 10), never 20. Enumerated family 6.61 to 20.87 per
  cent (the default, competing exits, the scalar uplift 10.11, the readers' route 12.59, discharged time 15.75, the
  crude count 16.25, and the nine golden constructions); standing family (the nine that route the revoked arrests
  through the courts) 18.50 to 20.87, all on 20; what rules the rest out is the arrests' own fates, a DOC sentence for 10.4 per
  cent of parolees' arrests while the Board could revoke against 21.2 per cent after discharge (6.8 against 21.4 in
  Garrison, 17.1 against 21.8 in Corliss), loud in the records and stated in no sentence.
- Analyst test: a strong analyst who links the four agencies' records, reads the Act correctly and keeps only the
  new-commitment returns, modelling them on the obvious covariates, files 5 per cent (Ends on); with revocations as
  competing exits 10 per cent; counting the arrests that ended in a Department sentence per day at liberty 12.59
  per cent, which both stage 4 readers filed as 10; only routing the revoked arrests through the courts' conversion files 20 per cent
  (`checks.py` R3a, R3b, RIV).
- Estimand: `prison_population_projection_methodology_2026.pdf` 2.1 to 2.3 (the cohort: every person on the 9
  October 2026 projected-release extract with a projected movement to parole in 2027, once each, the district
  holding the county of commitment), 3.1 to 3.3 (a return is an ADM movement from the day after release to the
  730th day after it, transfers and writs excluded; the share of members with a return, deaths kept in; steps of
  five percentage points), 4.1 to 4.2 (the Act governs the cohort's whole window; returns are new court
  commitments); the prompt names the cohort and the window.
- No decoy: nothing is planted; no memo, briefing, fiscal note or stakeholder figure argues a rate; the PRAT study
  reports the old law's returns of every kind for two early cohorts and says so; the wrong answer comes from the
  easy model alone.
- No certified replay: no certified or published figure is reproduced to recover the method; nothing in the pack
  forecasts 2027 returns or states a conversion rate.
- Lesson: when a law closes one institution's route to an outcome the record reached by whichever route acted
  first, the forward rate is the behaviour times the remaining institution's own conversion, not the remaining
  route's share of the record; no build on file teaches route substitution between two institutions.

## Readability screen

Reflex row written from what the field does to the deciding quantity (a release cohort's return rate): a risk model
on the obvious covariates validated by AUC, Kaplan-Meier or a hazard model by time since release, competing risks,
recalibration to the latest complete cohort, standardisation to the projected cohort's mix, an analogue population
(discharged parolees), dropping the returns a law ends.

| Rung | What the solver must see | Test that fires | Verdict |
|---|---|---|---|
| R0 the record's return rate of every kind, modelled | the admissions table | 3 reflex | readable |
| R1 the Act's returns only: the record's new-commitment rate (the default path) | Act section 3, methodology 4.2 | 1 filed sentence | readable |
| R2 revocations as competing exits | the admissions' two reasons | 3 reflex | readable |
| R2b discharged parolees as the analogue, flat | the release file's maximum dates | 3 reflex | readable |
| R2c arrests that ended in a Department sentence, per day at liberty (both stage 4 readers) | the crosswalk and the court file | 3 reflex | readable |
| R3 (decisive) the revoked arrests re-routed through the courts' conversion by charge grade, with the arrest-to-admission time | nothing names it: no column carries an arrest's would-be court outcome, no sentence says the courts will take the revoked arrests, the disposition file's NP code covers the courts' own nolle prosequis too | none of the six fires: no clause, no column or marker, not an opponent default, no control bench, no hygiene finding, not one subtraction (the scalar uplift misses at 10.11) | silent |

No confidence level, significance level or test threshold is filed anywhere in the pack.

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | share of the people | share of persons on the extract | share of release movements | same call | the extract lists each person once (methodology 2.2; asserted) |
| SF2 | the people the Department expects to release to parole in 2027 | the extract's PAR and RPR movements dated 2027 | every 2027 release movement | same call | the extract holds only PAR and RPR in 2027 (asserted) |
| SF3 | admitted to prison again | an ADM movement | any inbound movement (TRN, WRI) | same call | methodology 3.1; asserted with transfers read as admissions |
| SF4 | within two years of release | day 1 to day 730 | 731 days, two calendar years | same call | methodology 3.1; asserted at 731 |
| SF5 | under Act 26-114 | no recommitment; returns only as new commitments | the Act applying only to violations after its date | same call | every cohort member is released after 1 January 2027 (asserted) |
| SF6 | parole district | the district holding the county of commitment | the releasing institution's district | same call | methodology 2.3, Table 1; one district per county (asserted) |
| SF8 | round the share to a multiple of five percentage points | the nearest multiple, 20 | half-up against half-even, or rounding down | same call | the rate sits 2.13 points from the nearest rounding edge (asserted) and rounds down to 20 as well |
| SF9 | a member who dies | in the denominator, no return | out of the denominator | same call | methodology 3.2 |
| SF10 | the history the forecast stands on | every complete release since 2019 | the last two complete years | same call | asserted at 20.30 |
| SF11 | the arrests a member makes in the window (the judge's crude count) | arrests per day out of custody, each timed by the arrest-to-admission lag | every arrest in the 730 days counted, no time at risk, no lag | same call (21.78) | the route still sends every parolee arrest through the courts' conversion, the decisive step; its two mishandlings offset; without the step the same count gives 14.23 (asserted) |
| SF12 | the courts' conversion (the judge's flat conversion) | by charge grade | one rate pooled over grades | same call (20.87) | the route still takes the decisive step; the grade mix moves it less than a point (asserted) |

Every row is asserted in `generator/checks.py` (labels SF1 to SF6, SF8 to SF12; SF7, the districts' order, left
with the districts at stage 4 round 1).

## Ladder

| Rung | Construction | The pack's answer |
|---|---|---|
| 0 | the record's return rate of every kind, modelled on the covariates | 52.24 per cent (step 50) |
| 1 (default) | the record's new-commitment rate, logistic on the covariates, complete releases | 6.61 (step 5) |
| 2 | new-commitment admissions as a cause-specific hazard by time since release, revocations censoring | 11.02 (step 10) |
| 2b | the record's rate over the share of arrests the courts decided (one-number uplift) | 10.11 (step 10) |
| 2c | arrests that ended in a Department sentence, per day at liberty, with the arrest-to-admission time (the stage 4 readers) | 12.59 (step 15; the readers filed 10) |
| 2d | the courts' conversion on arrests counted with no time at risk, with the lag | 16.25 (step 15) |
| 2e | discharged parolees' new-commitment admissions per day, flat over 730 days | 15.75 (step 15) |
| 3 (golden) | arrests per day out of custody by time since release and covariates, times the courts' DOC share by charge grade, timed by the arrest-to-admission lag | 20.37 (step 20) |

Position and margins: every rung below 3 misses by one full step or more; the golden family's nine constructions sit
18.50 to 20.87 (edge distances 1.00 to 2.13); the judge's two readings (SF11 21.78, SF12 20.87) take rung 3's step.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the extract's 2027 PAR and RPR people, once each | filed, methodology 2.2 |
| 2 | Unit of account | a person | filed, methodology 2.2, 3.2 |
| 3 | Attribution window | day 1 to day 730 after release | filed, methodology 3.1 |
| 4 | As-of dating | records to 30 September 2026, extract of 9 October 2026 | filed, methodology 1.2, 2.2; manifest |
| 5 | Version basis | a docket's latest entry | dictionary (later row amends); R2 L4 asserted |
| 6 | Denominator | every cohort member, deaths kept | filed, methodology 3.2 |
| 7 | Weighting | each member equally | filed, methodology 3.2 (share of members) |
| 8 | Window length | 730 days | filed, methodology 3.1 |
| 9 | Boundary inclusivity | the day after release to the 730th day | filed, methodology 3.1; SF4 asserted |
| 10 | Rounding path | the cohort rate once, to its step | filed, methodology 3.3 and the prompt |
| 11 | Tie-break | none reached | not applicable: the call is one rate |
| 12 | Maturity and censoring | the history uses complete releases and arrests old enough to have closed | C1: open cases counted as no sentence still files 20 (R2 L5) |
| 13 | Order of operations | rate, conversion, projection | one order; the projection is per person |
| 14 | Row order | file order irrelevant | C1 |
| 15 | Duplicate resolution | admissions are ADM rows; amended dockets latest | dictionary; R2 L2, L4 asserted |
| 16 | Identity normalisation | state ID with and without its hyphen | dictionary; R2 L3 (loud) |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | days and people | units in the data |
| 19 | Code and status semantics | movement codes before and after 2022; ADM, TRN, WRO, WRI; GP, GT, AQ, DM, NP, OPEN | dictionary; R2 L1, L2 asserted |
| 20 | Integerisation | none on the call | C1 |
| 21 | Clause scope | the Act from 1 January 2027 for every parolee | filed, Act section 6; methodology 4.1 |
| 22 | Forward window contents | 2027 to 2029 under the Act; the cohort is on the extract | filed, methodology 2.2, 4.1 |

## Literal reader

Executed word for word, the methodology fixes the cohort (2.2), the return (3.1), the share (3.2), the step (3.3)
and the Act's scope (4.1 to 4.2); the Act's section 3 fixes that only new commitments remain. Nothing filed says how
the share of the cohort the Department will admit on a new commitment is estimated, so the method stays open, and
the records force it: parolees' arrests while the Board could revoke reached a DOC sentence 10.4 per cent of the
time against 21.2 after discharge, in every district (6.8 against 21.4 in Garrison), so the record's
new-commitment rate is a censored route and the courts' own conversion is the forward one. Every construction that
routes the revoked arrests through the courts files 20 per cent (nine of nine, `checks.py` FAM, and the judge's two,
SF11 and SF12); every term's alternative reading gives the same call (SF1 to SF6, SF8 to SF12). A literal reader who stops at the filed
sentences has the estimand and no estimate.

## Oracles

Nothing in the pack states a 2027 return rate or ranks the districts on one. The PRAT study
(distractor) reports the old law's returns of every kind by risk level for the 2019 and 2020 releases, a figure the
Act ends; the caseload extract (distractor) counts people under supervision; the capacity report (context
artifact) gives month-end populations. No file carries a conversion rate, an in-lieu share or a forecast (R1
asserted).

## Ask sheet

**Main call's declared row population:** releases to parole from 1 January 2019 to 30 September 2024, the
Department's ADM movements and the release file, arrests and court cases with arrests to 30 June 2024 (and the later
rows only as custody and arrest counts), the Board's REVOKE and REVOKED rows only for the set of arrest numbers they
cite, the deaths and the projected-release extract. Device and hazard rows in it: 0 (asserted, `checks.py` SEP: no
parallel-run row cites an arrest the call converts; the call never reads a detainer; deleting every writ row leaves
the call unchanged; companion reports add no arrest number the Board did not already revoke on).

Round 1 re-siting. Both stage 4 readers landed the round 0 devices by reflex (carried-over cases taken once, a blank
lift ended at the next admission, rescissions out). Every device below sits on the line a careful reader's quoted
path already executes and is a grain the path takes for granted, with no flag, no time zone, no time-gap merge and
no second file needed to see it; each leaves an inconsistency a grader can count in the data.

**Ask A. For each district office, the recommitments the Board ordered from 1 July 2025 to 30 June 2026 and had not
rescinded by 30 June 2026, split between those that took up a reported arrest and those on conditions alone** (8
figures, whole numbers). H18 home: the record the Act ends, which the projection replaces and the committees read
beside it.
- A1 (one order, two case rows; silent primary): a second report on a parolee already held (a supplemental report
  on the same arrest, or a conditions report filed during the hold) opens its own case, and the Board decides both
  at one hearing with one recommitment term: two REVOKE or REVOKED rows, the same DOC number, the same decision
  date and time, the same term, the same hold end. The ask counts recommitments, so one per parolee per hearing,
  on an arrest when either case cites one. Both readers count case rows: reader A's dedupe key (DOC number, report
  date, arrest number) never meets a companion, whose report date differs. Every cell moves (D1 +114 arrests, +109
  conditions; D4 +12, +19).
- A2 (WHAT closure, not a device): rescissions are counted when dated on or before 30 June 2026; 9 recommitments
  rescinded later stay in (the judge's fork). Both readers removed every rescission to the cut, which moves the
  four conditions cells by 1 to 3.
- Hazards kept from round 0, now on the readers' own path: the parallel-run fortnight (legacy entries after the 2
  January close), rescissions.
- Stops (asserted): case rows counted (all 8); rescissions to the cut (the 4 conditions cells).

**Ask B. For the county jails of each parole district, the parolee-days held on Board detainers in each half of
2025, counting the day a detainer was lodged but not the day the person left** (8 figures). H18 home: the detainer
days the State reimburses from 2027 (Act section 4(b)), the projection's cost line beside the returns.
- B1 (overlapping detainers on one person; silent primary): a companion case lodges its own detainer on a parolee
  already held, ending with the first, so the person's two intervals overlap. Parolee-days are days a parolee was
  held: the union of each person's intervals in the jail. Both readers sum one hold per case. Every cell moves (351 to
  2,795 days).
- Hazards kept from round 0 and on the readers' path: legacy detainers with no lift date (ended at the person's next
  admission), the legacy action table repeating a case's detainer on every action row, carried-over cases in both
  systems.
- Stops (asserted): intervals summed (all 8); blank lifts dropped or ended on the decision (all 8).

**Ask C. For each institution, the days its people spent out on court writs in each half of 2025, counting the day
they went out but not the day the trip ended** (10 figures). H18 home: the Department's writ transport cost, the
per-institution line the projection's custody days carry.
- C1 (a trip ended by a release; silent primary): a person taken out on a writ is sometimes released by the court
  or from the county without coming back, so the WRO has no WRI and the person's next movement is a release to
  parole in the Department's own release file. The trip ended with the release; 2,544 of 26,687 trips end that way.
  The quoted path pairs WRO with WRI and drops a trip with no return. Every cell moves (147 to 202 days).
- Stops (asserted): unpaired trips dropped (all 10); a trip with no return run to the next movement in the
  admissions table (all 10).

**Hazard table.**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| H1 companion reports | a second report on a held parolee decided at the same hearing | A, B | A every cell, +12 to +114; B every cell, +351 to +2,795 |
| H2 rescissions after 30 June 2026 | reconsideration after the fiscal year | A | the conditions cells, -1 to -3 |
| H3 releases from a writ | the court releases a person out on a writ | C | every cell, +147 to +202 |
| H4 the parallel-run fortnight | decisions entered in both Board systems 5 to 23 January 2026 | A, B | handled on the readers' path |
| H5 postponed hearings, blank lifts | the legacy action table | B | handled on the readers' path |

**Referee.** For A, the shared hearing time and term on two cases of one DOC number; for B, the overlap of one
person's intervals; for C, the release movement that follows an unreturned WRO. Each is countable from the shipped
rows and none needs a filed definition.

**Cracker sheet** (the cracker is the two stage 4 readers' quoted paths, executed literally on the cut pack by
`generator/cracker.py`: the call landed, every convention the asking sentences state, carried-over cases once, blank
lifts ended at the next admission, writs paired WRO to WRI)

| Ask row | Figures | Cracker's path | Device that holds | Verdict |
|---|---|---|---|---|
| Ask A, recommitments by office and basis | 8 | case rows counted, rescissions to the cut (reader A and reader B tables run separately) | A1, A2 | miss |
| Ask B, parolee-days by district and half | 8 | one hold per case, intervals summed | B1 | miss |
| Ask C, writ days by institution and half | 10 | WRO paired to WRI, unpaired trips dropped | C1 | miss |

One crack at a time (`cracker.py`): A1 cracked, the cracker keeps 4 of 26 and the pair is 32.7; A2 alone, 0 and 28.5;
B1, 8 and 37.0; C1, 10 and 39.1.

Measured by: `generator/cracker.py` (run on the cut pack; Part 0's weights, the call and its components 38, the
instructions 7, the asks 55 over the 26 ask figures; a response off the call keeps 5).

Mirror leakage: 0.0 per cent of ask weight (the mirror, off the call on 5 per cent, adds both Board systems, keeps
rescissions, leaves blank lifts out and drops unpaired writs, and keeps none of the 26 figures).

Pair ceiling: 28.5 measured on the cut pack (the cracker 45.0 on either reader's path, the mirror 12.0); the worst
single crack 39.1 (C1).

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | R2 (checks.py) |
|---|---|---|---|---|
| L1 movement codes PAROLE, REPAROLE, MAX EXP before 14 March 2022, PAR, RPR, EXP after | DOC offender management system | doc_release_movements_2019-2026.csv | pre-2022 releases dropped | call unchanged |
| L2 ADM beside TRN, WRO and WRI movements | DOC offender management system | doc_admission_movements_2019-2026.csv | transfers and writs read as admissions | call unchanged |
| L3 the state ID with and without a hyphen | SBI repository and its crosswalk | the arrest parquet and the crosswalk | a raw join matches nothing | loud (0 against 100 per cent) |
| L4 amended dispositions as later rows | AOC case management | aoc_case_dispositions_2019-2026.csv | the first row kept | call unchanged |
| L5 cases still OPEN at the cut | AOC case management | aoc_case_dispositions_2019-2026.csv | open cases counted as no sentence | call unchanged (17.88) |
| L6 deaths from a probabilistic match | Department of Health | vital_records_death_matches_2019-2026.csv | deaths ignored | call unchanged |
| L7 the Board's two systems and the parallel run | Board case systems | the two Board files | duplicates added | the revoked-arrest set unchanged; Ask A device |
| L8 county names in capitals and in title case with County | DOC and AOC | release, projection and court files | mapping missed | every county maps (asserted) |
| L9 legacy detainers without a lift date, repeated on postponed hearings | Board legacy system | board_violation_actions_legacy_2019-2026.xlsx | blanks dropped or ended on the decision | outside the call's population; Ask B hazards |
| L10 a second report on a held parolee as its own case, decided at the same hearing | both Board systems | the two Board files | case rows counted as orders | no arrest number added to the call (asserted); Ask A and B device |
| L11 writ movements, some ending in a release with no return | DOC offender management system | doc_admission_movements_2019-2026.csv | writs read as admissions; unpaired trips dropped | call unchanged with every writ row deleted (asserted); Ask C device |

## Leak sweep

`leak.py task169 --asof 2026-10-14`: REVIEW, no LEAK. Each REVIEW line, answered:
- Two coincidences in the court file (a sentence length in days such as 248 or 769 after a date's day digits)
  match the tail of a detainer-day figure; they are sentence lengths, unrelated to any ask.
- The methodology carries seven of the call's words because it files the estimand (the cohort, the return, the
  share, the step); it states no rate and no method.
- Design-note vocabulary in the Act, the PRAT study and the methodology is the field's own (record, return,
  sentence, courts, cohort, parolees); none of the three says what a revoked arrest becomes in court.
- The projected-release extract carries 2027 dates by nature (projected release and maximum dates).

## Tried and rejected

- Candidate A with five summers of record (2022 to 2026): the extra cool summers made growth by hour without
  weather land Tolland Road on most seeds, so the no-weather rung stopped missing; dropped for three summers.
- Candidate A with four summers: the same failure on three seeds of ten.
- Hybrid-working layer (Tuesday to Thursday commuting above Monday and Friday): Market Street dominated and pooled
  weekdays offset the effect; the layer added no separation and was dropped.
- Grading the forecast crowded days as a whole number: the golden family spans 25 to 35 days for Tolland Road, so
  the figure is not determinate; the call is graded categorically with the segment and the hour, and blocks 1 to
  3 carry only record facts and the family's shared range.
- Weather-only decisive step (no hour cells): growth with weather held on daily totals lands Estuary Path, so the
  weather alone carries no stump; the decisive step needs the binding hour too.
- Ramp-up of a new route, factor-group expansion (spent by task177) and saturation at capacity (spent by task168):
  rejected on paper before any prototype.
- Summer holiday commuting at 0.72 of term (to keep every crowded morning in term): Brickfields rose to within 1.12x
  of Tolland Road and an evening hour appeared on the bridge; reverted to 0.80 and the hours are stated as weekday
  mornings.
- Ask A with the Quayside laptop clock as its only second device: cracking the stamp convention alone left 10 of 24
  ask figures to the cracker and a single-crack pair of 40.0; the Corn Exchange restart from the same laptop was
  added, measured 37.7.
- Ask B with a contractor twin and a recurrence on the same Cathedral Green fault: the two mishandlings cancelled on
  the stoppage count (the cracker kept it); the fault was made the unit's own and the twin kept elsewhere.
- 2026-10-22, architecture 1 (the cycleway widening, never registered) set aside for a fresh draw: the guard's
  window blocked it three days running on its strategy (composition_mix), pattern (G14), forcing event
  (vote_or_meeting), role, forum and a same_driver test as other lanes kept drawing those axes; the author chose to
  continue with a fresh honest draw rather than wait, and the old world, mechanism and blocked axes are not reused.
- Street time as the decisive step (a "no prison for technicals" act lengthening time at liberty): it is the
  client's recidivism card 2 (time at risk) applied forward, a correction the field teaches; at realistic custody
  shares the lever is under a tenth of the figure. Set aside on paper.
- A supervision-term cap on technical returns (shorter terms for new-law releases): close to definitional (no
  revocation after discharge), and caught in the pincer between the new-law cohorts' own observed rate (a subset)
  and an extrapolation the survival forms split on. Set aside on paper.
- A discontinuity at the risk tool's supervision-tier cut-off moved by policy: a logistic with the tier as a
  covariate lands it, so the decisive step is a reflex. Set aside on paper.
- Failure to appear per court date under longer scheduling leads: the filed court rule names the lead time and
  the history's hearings at that lead are a filter and a divide. Set aside on paper.
- Positive tests per sanction-grid step under a lower testing frequency: the grid is a filed rule, so the replay is
  rule application. Set aside on paper.
- Rates by district graded in five-point steps: Garrison's family ran 21.9 to 25.6 against a 22.5 edge on one world
  and Ridgway's and Linwood's sat a point from 17.5, so district rates are not graded; the call grades the highest
  and lowest district, which every construction names the same way at 1.31x and 1.40x.
- The count of returns to the nearest hundred: the family's 18.5 to 20.9 per cent of about 6,500 people spans
  1,200 to 1,350, two hundreds; the rate is carried in the methodology's five-point steps instead.
- In-lieu shares that fell much harder on misdemeanours than on felonies A-B (scale 0.45): pooling the conversion
  over grades then moved the rate 1.5 points; the scale was set to 0.8 so the pooled form stays in the step, the
  grade-level conversion still forced by the records (60.7, 26.2 and 2.6 per cent).
- Ask B over fiscal 2025-26 quarters and a monthly revocations chart: the last fiscal quarter sat wholly in the new
  system and every month but January outside the parallel run, so a cracker kept four of sixteen detainer cells and
  eleven of twelve chart labels; Ask B moved to calendar 2025 quarters (every quarter in the legacy era) and the
  chart to the year's detainer totals, with the legacy action table's repeated detainer columns as a second device.
- Stage 4 round 0 (target.zip 8912821b): the judge approved, both readers filed 10 on the share but named Garrison
  and Corliss from the sentence-bound arrest route (12.59), which skips the decisive step, and both landed 24 of 24
  ask figures; the districts were dropped from the call (no route without the step was ever going to rank them
  wrong at Garrison's 0.40 log-rate lead) and the call is the share alone.
- Round 0 ask devices (the parallel-run duplicates, blank legacy lifts, per-case repeated detainer rows, carried-over
  cases) all sat on a careful reader's path and fell to reflex; replaced by grain devices (one recommitment per
  hearing, the union of one person's detainers, writ trips ended by a release), and the stacked chart left with
  Ask B's quarters.
- The heart BLOCK on ban.strategy (task252 entered the window after this card was registered) is ruled as the
  author ruled task177's: the window stays fixed at the draw; the card is not relabelled.
