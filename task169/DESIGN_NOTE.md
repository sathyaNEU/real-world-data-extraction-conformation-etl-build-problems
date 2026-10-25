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
  - Lever: the record's new-commitment rate 5.90 per cent (step 5), with revocations as competing exits 9.10
    (step 10); the golden 20.40 (step 20); the record's return rate of every kind 52.32 (step 50).
  - Outsider spread (nine constructions of the golden family: frailty 4 and 2, pooled conversion, one class mix for
    everyone, conversion from discharged parolees only, exposure stopped at the first admission, a flat arrest rate,
    the risk score added, the last two complete years only): 18.42 to 20.64, every one on 20; the largest move 1.98 points against a lever of 11.3 to 14.5 points.
  - Subset (discharged parolees' new-commitment admissions per day, flat): 14.45, misses (the hazard falls with
    time since release and discharged time sits late). Scalar route (the record's rate over the share of arrests
    the courts decided): 9.44, misses (the record's rate is also cut by revocations removing people early).
  - Stage 4 round 1 routes, run on the cut pack (`checks.py` RIV and SF11, SF12): the readers' route (arrests that
    ended in a Department sentence per day at liberty, with the arrest-to-admission time) 11.69, misses; the courts'
    conversion on arrests counted with no time at risk 15.67, misses; the judge's crude in-window count at the
    courts' conversion with no arrest-to-admission time 17.46 (step 15, ruled out by methodology 3.1) and its pooled
    conversion 20.45 (step 20, the decisive step taken); the same crude count without the step 10.10, misses.
  - Simulated forward truth under the Act, eight redraws of the cohort's two years: 20.53 per cent.
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
   district over the 30,959 complete releases (AUC 0.64), apply it to the 6,466 people on the projected-release
   extract and round to the methodology's step.

Ends on: 5 per cent (5.90 per cent unrounded)

Golden: 20 per cent (20.40)

## Stump sentence

A competent solver keeps only the returns the Act still allows, models each 2027 release's chance of a
new-commitment admission within two years on the record's complete releases and files 5 per cent (10 per cent with
revocations treated as competing exits, 11.69 per cent counting the arrests that ended in a Department sentence per
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
  (5.90 per cent, step 5) or with competing exits 9.10 (step 10), never 20. Enumerated family 5.90 to 20.64 per
  cent (the default, competing exits, the scalar uplift 9.44, the readers' route 11.69, the courts' conversion on
  every arrest with the revoked ones in 13.43, discharged time 14.45, the crude count 15.67, and the nine golden
  constructions); standing family (the nine that route the revoked arrests through the courts) 18.42 to 20.64, all
  on 20; what rules the rest out is the arrests' own fates, a DOC sentence for 7.7 per cent of parolees' arrests
  while the Board could revoke against 22.3 per cent after discharge (2.5 against 22.5 in Garrison, 15.8 against
  21.4 in Corliss), and the revoked arrests' cases nolle prossed (14,318 of 14,445, against 2.3 per cent of the
  others), loud in the records and stated in no sentence.
- Analyst test: a strong analyst who links the four agencies' records, reads the Act correctly and keeps only the
  new-commitment returns, modelling them on the obvious covariates, files 5 per cent (Ends on); with revocations as
  competing exits 10 per cent; counting the arrests that ended in a Department sentence per day at liberty 11.69
  per cent (step 10, as both stage 4 readers filed it); only routing the revoked arrests through the courts' conversion files 20 per cent
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
| R3 (decisive) the revoked arrests re-routed through the courts' conversion by charge grade, with the arrest-to-admission time | nothing names it: no column carries an arrest's would-be court outcome, no sentence says the courts will take the revoked arrests, the disposition file's NP code covers the courts' own nolle prosequis too | none of the seven fires: no clause, no column or marker, not an opponent default, no control bench, no hygiene finding, not one subtraction (the scalar uplift misses at 9.44), no dedicated organ (with the step deleted the court file still feeds the projection's first flow, new court commitments (methodology 1.1), and the arrests are the field's rearrest measure among the extracts 1.2 lists; readers A to D used both and filed 10) | silent |

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
| SF8 | round the share to a multiple of five percentage points | the nearest multiple, 20 | half-up against half-even, or rounding down | same call | the rate sits 2.10 points from the nearest rounding edge (asserted) and rounds down to 20 as well |
| SF9 | a member who dies | in the denominator, no return | out of the denominator | same call | methodology 3.2 |
| SF10 | the history the forecast stands on | every complete release since 2019 | the last two complete years | same call | asserted at 20.33 |
| SF11 | the arrests a member makes in the window (the round 1 judge's crude count) | arrests per day out of custody, each timed by the arrest-to-admission time | every arrest in the 730 days counted, no time at risk, no time to admission | 17.46, step 15 | methodology 3.1: a return is an admission by the 730th day, and 10 per cent of the count's returns are admitted after it; with that time the count prints 15.67 (step 15), still short of the days the record's parolees spent recommitted, which the Act ends (4.1); without the step 10.10 (asserted) |
| SF12 | the courts' conversion (the judge's flat conversion) | by charge grade | one rate pooled over grades | same call (20.45) | the route still takes the decisive step; the grade mix moves it less than a point (asserted) |
| SF13 | the courts' conversion (portal judge 2's basis) | arrests whose cases had closed (to 30 June 2024) | every arrest, cases open at the extract counted as no sentence | same call (19.43) | open cases are 5 per cent of the arrests the Board did not revoke on (asserted) |
| SF14 | within two years of release (the arrest-to-admission time) | each conversion timed by its arrest-to-admission time | every conversion admitted at once | 22.35, step 20 | methodology 3.1: a conversion admitted after the 730th day is no return (asserted) |
| SF15 | what share of the people will be admitted | the share of members with a return | the expected number of returns per member | 23.38, step 25 | methodology 3.2: the share of its members with a return (asserted) |
| SF16 | the time at risk (portal judge 1's early exposure) | every day out of custody in the window | arrests and days only to each release's first admission | same call (18.42) | the route still sends every parolee arrest through the courts (asserted, FAM) |
| SF17 | the courts' conversion's base (portal round 2, both judges) | the arrests the Board did not revoke on, their DOC sentences by grade (3,483 of 15,707) | every arrest with the revoked ones in (3,483 of 25,117; judge 1 at 14.8, judge 2 at 10.0, ladder 2f 13.43, step 15); the revoked arrests dropped from the counts too (11.70); a DOC or county-jail endpoint (judge 2's 19.4, a coincidence near the golden, not its route) | 15 or 10 | the record: the 9,410 revoked arrests were all nolle prossed against 374 of the 15,707 others, so their record outcome is the Board's; the 10,576 arrests made on or after the parole's maximum date, when the Board could not revoke, convert class by class at the same rates (1,092 of 1,748, 1,143 of 4,338, 122 of 4,490), and the projection on them files 20.44; write-up steps 3 to 5 state it; the endpoint is DOC alone (Act section 3(c), the dictionary's sentence_type) (asserted SF17, verify) |
| SF18 | ask 2's unit, "the recommitments the Board ordered" (stage 4 judge r3) | one per parolee per hearing date, two cases decided together one order (3,174) | each REVOKE or REVOKED decision row (3,523) | asks only | the prompt's clause "one per parolee per hearing date" (2026-10-25); "those on conditions alone" closes any against all cited arrests (asserted SF18) |
| SF19 | ask 4's trip end, "the day the trip ended" (stage 4 judge r3) | the person back from the writ (WRI) or released, whichever comes first; 28,287 trips end at a WRI and 2,110 at a release, none open | WRO paired with WRI alone, the released trips dropped (every cell lower) | asks only | the prompt's clause "with the person back from the writ or released" (2026-10-25) (asserted SF19) |
| SF20 | ask 3's detainer end where the courts sent the person to the Department before the Board lifted the detainer (portal round 3, judge 2) | the day of the admission, when the person left the county jail | the recorded lift date, 1 to 39 days later (123 detainers, 21 touching 2025, five cells) | asks only | C1 in the records: the Board lifts such a detainer on the admission day, so the recorded end and the physical exit select the same days (asserted SF20, verify) |
| SF21 | the days at risk under the Act (portal round 4, judge 2) | every day out of Department custody from release to a return: the record's arrests read per day out of custody (the record's releases spent 554.5 of their 730 days out, on average) and carried over all 730 | the record's arrests over the 730 calendar days, each through the courts' DOC share (14.77, judge 2's 14.8; 13.50 with the arrest-to-admission time); the share scaled whole by 730 over the mean days out (23.04, judge 2's 23.5) | 15 or 25 | methodology 4.1 now files it: "A member of the 2027 cohort is therefore out of Department custody from release until a return, and for all 730 days where there is none"; the scaled share falls to 3.1 (a return is an admission by day 730) and 3.2 (a share of members); on the days out of custody every route files 20 (no covariates 19.91, one rate 20.11, detainer days out of the exposure too 21.64 and 21.76, each release's own arrests scaled to its own days out 20.50) and the default path read on the same days still files 10 (11.12) (asserted SF21) |

Every row is asserted in `generator/checks.py` (labels SF1 to SF6, SF8 to SF21; SF7, the districts' order, left
with the districts at stage 4 round 1).

## Ladder

| Rung | Construction | The pack's answer |
|---|---|---|
| 0 | the record's return rate of every kind, modelled on the covariates | 52.32 per cent (step 50) |
| 1 (default) | the record's new-commitment rate, logistic on the covariates, complete releases | 5.90 (step 5) |
| 2 | new-commitment admissions as a cause-specific hazard by time since release, revocations censoring | 9.10 (step 10) |
| 2b | the record's rate over the share of arrests the courts decided (one-number uplift) | 9.44 (step 10) |
| 2c | arrests that ended in a Department sentence, per day at liberty, with the arrest-to-admission time (the stage 4 readers) | 11.69 (step 10, as the readers filed it) |
| 2d | the courts' conversion on arrests counted with no time at risk, with the lag | 15.67 (step 15) |
| 2e | discharged parolees' new-commitment admissions per day, flat over 730 days | 14.45 (step 15) |
| 2f | the courts' conversion on every arrest, the revoked ones in, over full time at risk (portal judge 2's all-arrest basis) | 13.43 (step 15) |
| 3 (golden) | arrests per day out of custody by time since release and covariates, times the courts' DOC share by charge grade, timed by the arrest-to-admission lag | 20.40 (step 20) |

Position and margins: every rung below 3 misses by one full step or more; the golden family's nine constructions sit
18.42 to 20.64 (edge distances 0.92 to 2.33); the round 1 judge's pooled conversion (SF12, 20.45) takes rung 3's step
and its crude count (SF11, 17.46) falls to methodology 3.1; the portal judges' readings SF13 and SF16 take it too.

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
| 23 | Exposure under the counterfactual | every day out of Department custody from release to a return | filed, methodology 4.1 (portal round 4); SF21 asserted |

## Literal reader

Executed word for word, the methodology fixes the cohort (2.2), the return (3.1), the share (3.2), the step (3.3),
the Act's scope (4.1 to 4.2) and the cohort's days at risk, every day out of Department custody to a return (4.1); the Act's section 3 fixes that only new commitments remain. Nothing filed says how
the share of the cohort the Department will admit on a new commitment is estimated, so the method stays open, and
the records force it: parolees' arrests while the Board could revoke reached a DOC sentence 7.7 per cent of the
time against 22.3 after discharge, in every district (2.5 against 22.5 in Garrison), so the record's
new-commitment rate is a censored route and the courts' own conversion is the forward one. Every construction that
routes the revoked arrests through the courts files 20 per cent (nine of nine, `checks.py` FAM, and the judges'
SF12, SF13 and SF16); every term's alternative reading gives the same call or breaks a quoted sentence (SF1 to SF6,
SF8 to SF16). A literal reader who stops at the filed
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

Round 4 re-siting (portal round 4, 2026-10-25). Both portal responses reproduced all three tables of the round 3 pack:
the round 2 ask clauses state A1's unit and C1's trip end, and B1's union and A2's cut sit on a careful path, so the
rubric came back at 74 per cent with the call missed. Each new primary needs a reconstruction after it is seen (a case's
actions replayed in date order, a cross-system match on the carried-over key, a detainer spliced across the two systems);
none is flagged, narrated in a file or isolated by one column, and each leaves a count a grader can check in the records.

**Ask A. For each district office, the recommitments the Board ordered from 1 July 2025 to 30 June 2026 and had not
rescinded by 30 June 2026, one per parolee per hearing date, split between those that took up a reported arrest and
those on conditions alone** (8 figures, whole numbers). H18 home: the record the Act ends, which the projection replaces
and the committees read beside it.
- A1 (one order per parolee per hearing) and A2 (rescissions dated by 30 June 2026) stand as WHAT closures in the
  prompt's clause and the records; a careful path executes both.
- A3 (a revocation set aside on appeal and heard again; silent primary, a case's actions replayed in order): the Board
  rescinds an order with the parolee still in Department custody and recommits on the same term at a second hearing on
  the same case. The legacy action table writes REVOKE, RESCIND, REVOKE on one case number, the second action row
  repeating the case's detainer columns as every action row does (32 cases, two to eleven per cell). A rescission sets
  aside the order standing on its case when it came (the dictionary: "an earlier revocation"), so the later order
  stands; the round 3 golden's own rule, every order on a case with a RESCIND row out, loses it. Every cell moves (1 to
  11).
- The parallel run stays a hazard: every legacy decision dated after the close copies one the new system holds.
- Stops (asserted): every order on a rescinded case out (all 8), case rows (all 8), both systems added (all 8).

**Ask B. For the county jails of each parole district, the parolee-days held on Board detainers in each half of 2025,
counting the day a detainer was lodged but not the day the person left** (8 figures). H18 home: the detainer days the
State reimburses from 2027 (Act section 4(b)), the projection's cost line beside the returns.
- B1 (each parolee's overlapping detainers merged) and the round 3 lift at an admission stand; a careful path executes
  both.
- B3 (the go-live re-issue; silent primary, one detainer rebuilt from the two systems): the Board re-issued the detainer
  of every carried-over case still undecided at go-live under the new case, lodged 5 January 2026 (450 of the 473
  carried-over detainers; 14 new cases' detainers were lodged that day too), and the legacy table keeps the detainer it
  replaced, lodged 12 November 2025 to 2 January 2026 and lifted in neither system before go-live. A carried-over
  detainer runs from its legacy lodge day to its end in the new system; taking the carried-over case from the new
  system, as the round 3 golden's step 7 did, loses its 2025 days. Every July to December cell moves (920 to 3,232
  days).
- The January to June cells carry no device: they are the construction's, free to a careful path.
- Stops (asserted): the new system's date for a carried-over detainer (the four July to December cells), detainers
  summed (all 8), both systems and every row ended at the decision (all 8), blank lifts dropped (all 8), both end days
  counted (all 8).

**Ask C. For each institution, the days its people spent out on court writs in each half of 2025, counting the day
they went out but not the day the trip ended, with the person back from the writ or released** (10 figures). H18 home:
the Department's writ transport cost, the per-institution line the projection's custody days carry.
- No device: C1's trip end is the prompt's clause (round 2). No person has two trips open at once (asserted), so every
  pairing gives the same trips; the construction alone, free to a careful path.
- Stops (asserted): an unreturned trip dropped (all 10).

**Hazard table.**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| H1 companion reports | a second report on a held parolee decided at the same hearing | A, B | executed by a careful path (the clause; the union) |
| H2 rescissions after 30 June 2026 | reconsideration after the fiscal year | A | executed by a careful path (the cut) |
| H3 releases from a writ | the court releases a person out on a writ | C | executed by a careful path (the clause) |
| H4 the parallel-run fortnight | decisions entered in both Board systems 5 to 23 January 2026 | A | handled on a careful path |
| H5 postponed hearings, blank lifts | the legacy action table | B | handled on a careful path |
| H6 appeals heard again | an order set aside on administrative appeal and re-heard on the same case | A | A3: every cell, 1 to 11 |
| H7 the go-live re-issue | open detainers re-issued under the new case on 5 January 2026 | B | B3: the July to December cells, 920 to 3,232 days |

**Referee.** For A3, the PAROLE VIOLATOR admission after the first order and no release before the second hearing
(the parolee held on the second order); for B3, the 450 carried-over detainers all lodged on the go-live day
against legacy lodges in the eight weeks before it, none lifted before go-live. Each is countable from the shipped rows
and none needs a filed definition.

**Cracker sheet** (the cracker is portal round 4's two responses, which reproduced every table of the round 3 pack,
executed by `generator/cracker.py` along the round 3 golden's own path: the call landed, every convention the asking
sentences state, every order on a rescinded case out, a carried-over case's detainer from
the new system, overlaps merged, writs ended at the WRI or the release)

| Ask row | Figures | Cracker's path | Device that holds | Verdict |
|---|---|---|---|---|
| Ask A, recommitments by office and basis | 8 | every order on a rescinded case out | A3 | miss |
| Ask B, July to December by district | 4 | carried-over detainers from the new system | B3 | miss |
| Ask B, January to June by district | 4 | the construction | none | kept |
| Ask C, writ days by institution and half | 10 | the construction | none | kept |

One crack at a time (`cracker.py`): A3 repaired, the cracker keeps 22 of 26; B3 repaired, 18 of 26.

Measured by: `generator/cracker.py` (run on the cut pack; Part 0's weights, the call and its components 38, the
instructions 7, the asks 55 over the 26 ask figures; a response off the call keeps 5).

Mirror leakage: 0.0 per cent of ask weight (the mirror, off the call on 5 per cent, adds both Board systems, keeps
rescissions, leaves blank lifts out and drops unpaired writs, and keeps none of the 26 figures).

Pair ceiling: 43.3 measured on the cut pack (the cracker on the call keeps 14 of 26 and scores 74.6, the mirror 12.0).
The repair is built to the author's target for this return, not to this file's 40: the portal's cutoff is 70 and the
target the high 50s to low 60s, with both responses off the call in every portal round. On the round 4 rubric a response
off the call scored 74 with all 26 ask figures, so each figure is worth 1.3 to 2.3 points: keeping the 14 free figures
it lands near 46 to 58, and near 56 to 65 if it repairs both Table 1 devices or B3. `precut.py` fails this sheet's two
kept rows and the 43.3 by design, recorded in `## Repairs, portal round 4`.

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
- Four coincidences in the court file (a date's day digits running into the next field's sentence length, as in
  "2022-12-19,163") read as detainer-day figures; they are sentence lengths, unrelated to any ask.
- The methodology carries seven of the call's words because it files the estimand (the cohort, the return, the
  share, the step); it states no rate and no method. Round 4's sentence in 4.1 (the cohort out of Department custody
  from release until a return) brings its stump-paragraph terms from 10 to 12 of 25 (custody, release); it names no
  arrest, court, conversion or rate.
- Design-note vocabulary in the Act, the PRAT study and the methodology is the field's own (record, return,
  sentence, courts, cohort, parolees, custody); none of the three says what a revoked arrest becomes in court.
- The projected-release extract carries 2027 dates by nature (projected release and maximum dates).

## Pre-ship check

- Rule 1, the domain: the deciding quantity is the 2027 release cohort's two-year return-to-prison rate, built the
  way a corrections forecaster builds it under a change in revocation law (arrests per day out of custody, the
  courts' conversion by charge grade, the arrest-to-admission time); the swap test holds (the judge's Gate H).
- Rule 2, two layers: Layer 1 is the Department's renamed movement codes, writs and transfers beside admissions, the
  Bureau's hyphenated IDs, amended dockets, open cases, probabilistic deaths, the Board's two case systems with their
  parallel run, carried-over cases, blank lifts and companion reports, each asserted neutral on the call (R2, SEP);
  Layer 2 decides.
- Rule 3: no plant, no filed method, no field names what a revoked arrest becomes in court; the easy route on the clean
  truth files 5 (R3a); every route without the step misses (5, 10, 15, 50 or 55), and the judge's own wrong routes
  land in their own buckets or break a filed sentence (raw arrests 15; no lag 20, against 3.1; an expected count 25,
  against 3.2).
- Determinism: the stage 4 re-judge on 501d0e28 approved, but the portal's judges found its routes at 11 to 16 and
  the call unforced (`## Determinism repair`); rebuilt so every route that takes the step files 20.
- Stage 4 record: round 1 (8912821b) readers A and B and the judge APPROVE, districts and asks re-sited; round 2
  (f3ef6705) readers C and D both off the call (asks 1 and 9 of 26), the judge FIX_NOW on Table 3, repaired in the
  data; the heart BLOCK on ban.strategy ruled as task177's, the window fixed at the draw.

## Determinism repair (portal, 2026-10-25)

- Portal round 1 on 501d0e28: both responses off the call and the rubric at 50, but the determinism block failed.
  Judge 1 unsure, Gate C margin fragility (observed-window, pooled band-hazard and early-exposure routes at 13.3 to
  15.6 against a full-exposure proxy at 20.9); judge 2 FAIL, competing_defensible_answer (11.4 with every arrest's
  conversion, 15.68 with the Board-revoked arrests left out, the golden needing choices no file forces).
- Measured on the shipped pack, a route map over conversion basis, arrest-rate construction, timing and probability:
  the routes that take the decisive step and follow the filed definitions ran 17.5 to 21.0. Counting the cases still
  open at the extract as no sentence cost 2.4 points (0.188 against 0.222, the courts taking about eight months on a
  felony A-B case); the courts' own nolle prosequis (28 per cent of their dismissals) and the Board's lighter hand on
  felony A-B arrests moved pooled bases by 1 to 2 points; the arrests counted per release sat on the 17.5 edge.
- Stump test: the fork is not the stump. No reading moved the call; the spread was in how the record let a sound
  method be implemented, so the closure is C1 in the world and nothing is filed.
- Move (C1): the courts decide faster (arrest to admission about three months for felony A-B, two for C-E, six weeks
  for misdemeanours), revocations run 9 to 20 months, the Board's in-lieu share is the same for every grade and
  15 per cent higher in each district (Garrison 0.90 to Corliss 0.25), the courts' own nolle prosequis are 8 per cent of
  their dismissals, and the cohort keeps its 6,466 members. Every route that takes the step and follows 3.1 and 3.2
  now files 20: the nine golden constructions 18.42 to 20.64, the portal judges' bases 19.43 (open cases as no
  sentence, SF13) and 18.42 (exposure to first admission, SF16), pooled 20.45 and from discharged parolees 20.44. The
  routes without it stay out (5.90, 9.10, 9.44, 11.69, 13.43, 14.45, 15.67); the forward truth is 20.53; the stump
  sentence holds as written (5 per cent; the Board revoked on 31.4 per cent of the record's arrests).
- Asks: the three tables re-derive from the new world with every device as it was (`cracker.py`: 0 of 26 on every
  stop, the one-crack keeps unchanged at 4, 0, 8 and 10 of 26, pair ceiling 28.5).
- Gates: checks 88 PASS, verify 0 failed, two builds byte-identical over 20 files and a later full rebuild identical
  to the pack on disk, figures_check 36, precut 51, voice-check PASS, leak.py REVIEW (answered in `## Leak sweep`),
  guard validate 292 cards. freeze, rubric mode: the call, the components, the stump, the card and the call sentence
  untouched; it flags only the ladder and default-path sections, whose figures are re-derived from the new world (each
  rung's method and the default path's steps and end step as they were, rung 2f added for judge 2's basis).
  Determinism mode fails by construction on 30 items: the 26 ask figures, the history's 30,959 releases in step 1,
  the Deliverable Answers block that carries them and those two sections, the latitude the author gave.
- Heart: BLOCK on ban.forcing_event and ban.org_family against task125 (v2), registered 2026-10-23, after this card
  (2026-10-22); the class the ruling at ship covers (the window fixed at the draw), the card untouched by the repair
  and not relabelled.
- Re-judge (determinism-check-task169-r2, order kept): DETERMINISTIC, APPROVE, no fix. Its blind estimate 19.7 per
  cent (arrest hazard per day at liberty, times each grade's conversion to a DOC sentence, an 82-day lag), 20.2 with
  the cohort's covariates, 20.8 at a 60-day lag; every correct variant prints 20. The only surviving rival is an
  incomplete method (arrests imputed without the exposure correction, 16.5 to 18.2). All three tables reproduce
  exactly; its residual ask notes (per case or per order in table 1, the unreturned writs' end in table 3) are each
  closed by a shipped sentence or the records. Gate G analytical_non_defect, Gate H pass.
- Readers (scored): reader E filed 10 against 20 and kept 23 of 26 ask figures (88.5 per cent; tables 1 and 2 whole,
  three writ cells off); reader F filed 10 and kept 18 of 26 (69.2 per cent; tables 2 and 3 whole, table 1 missed on
  every cell). The call held in both; the asks leak as the portal's round 1 measured them (two responses off the call
  at about 50 means about seven tenths of the ask weight kept), so the ask layer stands where it shipped and a rubric
  repair of tables 2 and 3 is the next step if the portal returns it on the rubric. E's leak answers quote no sentence
  naming the step and read the validation study's 45 to 61 per cent all-returns figures as a wrong basis.

## Determinism repair, portal round 2 (2026-10-25)

- Portal round 2 on 73e3137b: the determinism block failed again. Judge 1 unsure (A and C fail, answer_contradicts_files,
  fix location the solution, the model response a valid stump): five reconstructions at 10 to 15 per cent, the covariate
  Poisson over full exposure 14.8; it read step 3's "leaving out the arrests the Board revoked on" as dropping arrests,
  which it expected to push the rate down. Judge 2 failed (A, C, D, golden_wrong): every DOC route at 9 to 10.5, and 20
  only with county-jail sentences counted (19.4).
- Diagnosis: both judges converted over every arrest, the revoked ones in (ladder 2f, 13.43 on the golden's hazard), so
  the call held on them; the write-up never showed why the courts' rate leaves the revoked arrests out, and judge 2 found a
  coincidental 19.4 to explain the golden. The golden reproduces (20.40; on the discharged arrests' conversion 20.44).
- Stump test: the fork is the decisive step's own working, not a reading. Filing it would hand it over; the record already
  decides it, so the move is in the solution (both judges' fix location): steps 3 to 5 now state the evidence as exact
  counts, every one recomputed by verify. Nothing a solver sees changed: target.zip 73e3137b unchanged.
- Gates: checks 120 (SF17's eleven rows), verify 0 failed, two builds byte-identical over 20 files, figures_check 59,
  precut 51, freeze --mode determinism PASS.
- Re-judge (determinism-check-task169-r3, order kept): the main call forced (every sound estimate 18.2 to 20.9, all
  20; the revoked arrests' nolle prosequis and the after-maximum-date control reproduced), table 2 (detainers) exact;
  Gate F good (wrong routes at 10, 15 and 50), Gate G analytical_non_defect, Gate H pass. NOT_DETERMINISTIC on two
  asks, labelled SEND_BACK but a Gate C and E failure confined to supplementary asks with the main call forced, so an
  ask-layer wording repair that spends no architecture: ask 2 counted per decision row (3,523 against 3,174) and ask 4
  with WRO paired to WRI alone (every cell lower). Closed in the prompt's ask clauses with the units the judge named,
  "one per parolee per hearing date" and "with the person back from the writ or released" (SF18, SF19); the call
  sentence untouched; 951 characters, voice-check PASS. Step 3 now names its base (every linked arrest dated to 30
  June 2024, release-day arrests included: the judge's 25,053 left out 64 arrests made on a release day). Its step 8
  note (four trips ending at an ADM or TRN) does not hold on the record: all 30,397 trips end at a WRI or a release, and
  the eleven with an ADM or TRN between end at their WRI. No further judge: the closures are the ones the judge wrote,
  and no graded figure moved.

## Determinism repair, portal round 3 (2026-10-25)

- Portal round 3 on 73e3137b with the ask clauses: judge 1 passed every gate (the call, all three tables exact); judge 2
  passed the call (20.1 per cent on its own decontamination) and tables 1 and 3, and failed table 2 on C and E: where a
  person was admitted to the Department before the Board's recorded lift date, the days held in the county jail end at the
  recorded lift (the golden) or at the admission (the physical exit), and five cells differ.
- Diagnosis: 123 detainers (21 touching 2025), every one a parolee the Board continued after an arrest whom the courts sent
  to the Department on a new sentence before the Board's hearing lifted the detainer, 1 to 39 days earlier. The golden
  counted jail days after the person was in a State institution; the prompt counts days held in the county jails.
- Move (C1 in the records): the Board lifts such a detainer on the admission day (pack.py, no random draw, every other row
  unchanged), so the recorded end and the physical exit select the same days; SF20 in checks and verify. Six table 2 cells
  move (Garrison 34,632 to 34,613 and 35,505 to 35,500; Ridgway 21,448 to 21,409; Linwood 19,236 to 19,163; Corliss
  10,265 to 10,241 and 10,627 to 10,611), the golden counting by the literal reading (judge 2's figures). The realism check
  now allows one ask figure of 26 on a hundred (Garrison's 35,500 is the record's count) and none on a thousand.
- Gates: checks 125, verify 0 failed, two builds byte-identical over 20 files, figures_check 60, precut 51, freeze rubric
  PASS (the call, the stump and every frozen figure unchanged; six ask figures and the golden workbook moved), determinism
  mode listing the same six cells. target.zip 972382ac (the two Board files changed).
- Re-judge (determinism-check-task169-r4, order kept): DETERMINISTIC, APPROVE, no fix; the call 19.5 to 20.4, all three
  tables exact with the new cells; Gate G analytical_non_defect, Gate H pass. Report: determinism_check_report_pass3.md.

## Repairs, portal round 4 (2026-10-25)

- Portal round 4 on f958b874 (target.zip 972382ac): judge 1 passed every gate (F strong), reproducing the call's chain
  (25,117 arrests, 3,483 DOC sentences) and all three tables; judge 2 failed C and D, competing_defensible_answer on the
  call's exposure basis (the calendar counterfactual 14.8, step 15; the golden's days out of custody 20.4; a share scaled
  by the days out 23.5, step 25), fix location a shipped governing file. Both responses filed 10 on the naive route, and
  the rubric came back at 74 per cent with the call missed: they reproduced every table, the round 2 clauses having
  spelled out A1 and C1 and B1 and A2 sitting on a careful path.
- Determinism move (a WHAT at authority, once): methodology 4.1 adds "A member of the 2027 cohort is therefore out of
  Department custody from release until a return, and for all 730 days where there is none." It fixes the
  counterfactual cohort's custody state, the estimand's population condition, and names no arrest, court, conversion,
  rate or model. Readability screen: it does not name the decisive quantity (the courts' conversion of the arrests the
  Board revoked on), and the default path read on the same days still files 10 (11.12). SF21 and closure row 23.
- Rubric move (the call frozen): A3 and B3 (`## Ask sheet`; A4 withdrawn at stage 4) on rows outside the call's population. The call reads
  the Board's REVOKE and REVOKED rows only for the arrest numbers they cite (the shipped 14,445, asserted), no hold and
  no writ; every file it reads that no device touches is byte-identical to 972382ac (asserted, SEP), and the
  unrounded rate is the shipped 20.403944. Only the two Board files, the methodology and the manifest's row counts
  changed. The Table 1 golden moved by one to three orders in five cells (seven re-heard orders whose first order fell
  before 1 July 2025); Tables 2 and 3 are unchanged. The prompt is unchanged.
- Gates (target.zip 457a4616): checks 129, verify 0 failed, two builds byte-identical over 20 files (again after the
  write-up's step 5 cited its file and section), figures_check 63 of 63, voice-check exit 0, leak.py REVIEW with no
  LEAK (answered in `## Leak sweep`), guard validate 296 cards and none invalid, freeze rubric PASS (the call, the
  stump and every frozen figure unchanged; the golden workbook and nine ask figures moved). precut 51 checks with two
  FAIL by design (the pair ceiling 43.3 and the two kept cracker rows, the author's target above). heart BLOCK on
  ban.forcing_event and ban.org_family against task125 (v2), whose card was registered on 23 October after this
  draw on 22 October: ruled as the earlier window rulings, the window fixed at the draw and the card not relabelled.
- Stage 4 on 457a4616: judge r5 DETERMINISTIC, APPROVE, no fix; its blind pass filed 10 against 20 (the record's
  new-commitment rate) and reproduced all three tables; Gate F strong, G analytical_non_defect, H pass; the calendar
  route its closest rival, ruled out by 4.1's sentence and the arrests' near absence in custody (0.36 per cent). Scored
  readers: g filed 10 and kept 26 of 26 ask figures; h filed 20 (the revoked arrests' nolle prosequis found in the data)
  and kept 25 of 26. Before this pack the in-house readers A to F and the portal's eight responses all filed 10.
- Expected portal effect: a response off the call that keeps the 14 free figures lands near 46 to 58 on the round 4
  rubric, near 56 to 65 if it repairs both Table 1 devices or B3, 74 only if it repairs all three.

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
- Writ trips generated stay by stay (stage 4 round 2, judge FIX_NOW on Table 3): a person with two admissions and no
  release between them got two overlapping writ loops, 96 WRO rows in overlapping pairs, so no filed rule said which
  open WRO a WRI closed, and the golden's pairing (a second WRO replacing the first) matched no reading of the files.
  The generator now writes one trip at a time per person (a later trip that would leave before the earlier one came
  back is not written), asserted in `checks.py` and `verify.py`; next-WRI and same-institution pairings both
  reproduce Table 3 exactly. No pairing rule and no trip-end rule is filed.
- Portal round 1 (2026-10-25) on the first world: the sound routes ran 17.5 to 21.0, because open cases, the courts'
  own nolle prosequis and the Board's lighter hand on felony A-B arrests moved the courts' conversion with the basis
  a judge chose. A filed conversion basis, hazard model or timing rule would make the decisive step rule application,
  so the world was rebuilt instead (`## Determinism repair`).
- Portal round 2 (2026-10-25, 73e3137b): the write-up's step 3 as the only account of the courts' conversion. Both judges converted over every arrest and could not reproduce 20; the evidence (revoked arrests all nolle prossed, the no-Board arrests at the courts' rate) moved into steps 3 to 5 as exact counts; nothing filed, the pack unchanged.
- Stage 4 re-judge r3 (2026-10-25): asks 2 and 4 with their units left to the write-up and the records. The judge read the recommitments per decision row and the writ trips paired WRO to WRI; both units are now in the ask clauses.
- Portal round 3 (2026-10-25): table 2 counted to the Board's recorded lift date for detainers whose holder the courts had already sent to the Department; judge 2 stopped at the admission. Closed in the records (the Board lifts at the admission), not by a prompt clause the 1,000-character budget could not carry.
- Portal round 4 (2026-10-25): the round 2 clauses spelled out A1's unit and C1's trip end, and B1's union and A2's cut sat on a careful path, so both responses reproduced every table (rubric 74 with the call missed). A1 and C1 stay as WHAT closures; the ask weight moved onto A3, A4 and B3.
- Judge 2's suggested pin (state the liberty-day Poisson and the full-730 assumption, or the calendar basis with the courts' rate applied to expected arrests): either sentence files the method and makes the decisive step rule application; the WHAT, the cohort's custody state under the Act, closes the same fork.
- A device on the parole maximum date (holds and orders past the Board's jurisdiction): the world lets the Board act after the maximum date on violations before it (86 recommitments and 722 PAROLE VIOLATOR admissions after it), so "a parolee" past the date is a fork, not a device. Set aside on code.
- A writ trip split across a transfer while out: "the days its people spent out" reads as the institution left or the one holding the person each day, a fork the prompt's budget cannot close. Set aside on paper.
- A re-hearing in the new system, the rescinded date kept on the case's one row beside a later decision timestamp: a judge can read the date as rescinding the row's decision, so the device would ride on a reading; kept to the legacy action table, where the order of the rows decides it.
- An arrest report with no arrest number (condition 01 cited, the number missing): the split would turn on reading condition 01 as an arrest, a semantic fork. Set aside on paper.
- Re-issuing every carried-over detainer open at go-live (the first cut): the cases decided on 3 and 4 January 2026 have no legacy row, so their 2025 days were in no record (law 6) and three July to December cells fell; the re-issue is limited to the cases still undecided at go-live.
- A Table 3 device to bring the pair under 40: the author's target for this return is the high 50s to low 60s against the portal's 70 cutoff, and Table 3's trip end has already cost two judge passes; left as the construction.
- A4, the parallel run's decisions that reached only the legacy system (27 recommitments left undecided in the new system): the stage 4 judge (r5) read it as a soft fork, nothing filed saying which system governs a carried-over case whose new-system decision is blank, and readers g and h kept every one by deduplicating the two systems on parolee and hearing date. It bought no figure and cost a reading; withdrawn.
- A3 and B3 as primaries, measured on target.zip 457a4616: readers g and h and the judge's blind pass reproduced every Table 1 and Table 2 cell (g: "legacy RESCIND paired with the latest prior REVOKE", "legacy lodged date (not the reset new-system start)"; h: both systems merged per case, the earliest lodge kept). Seen and repaired right by a careful path; kept as hazards that cost a looser path cells, not counted on for the rubric.
