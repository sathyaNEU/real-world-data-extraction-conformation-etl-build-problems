# task169 design note: two-year returns of Pembroke's 2027 parole releases under Act 26-114

Architecture 2 (a fresh draw). Architecture 1 (Calvermouth's cycleway widening, urban-regional-science) was built
to stage 3 in scratch and never registered: the guard's window held it three days on its strategy, pattern,
forcing event, role and forum and on a same-driver test, and the author chose a fresh honest draw over waiting.
That draw's world, mechanism and blocked axes are not reused; its line is in `## Tried and rejected`.

## Draw

- **Cell.** Client domain Criminology & Justice, task type `recidivism-risk-assessment` (serves Forecasting &
  Predictive Modeling). Objective Forecasting: the call is the number of people released to parole in calendar
  2027 who will be back in prison within two years of release, a window not yet open, pinned by the record of the
  2019 to 2026 releases.
- **World.** The State of Pembroke (fictional; its agencies, people, systems and records are fictional, the field's
  method is real). The Pembroke Sentencing and Policy Commission prepares the prison population projection the
  General Assembly's appropriations committees take in January 2027. Act 26-114 (signed 30 June 2026, in force for
  every release from 1 January 2027) ends returns to prison for violations of parole conditions: a parolee may be
  returned to prison only on a new court commitment. The Department of Corrections (releases, admissions, the 2027
  projected releases), the Board of Parole (violation reports, revocation decisions), the Administrative Office of
  the Courts (case dispositions) and the State Bureau of Identification (arrests) hold the records.
- **Card.** `domain` criminology-justice, `subdomain` recidivism-risk-assessment, `objective` forecasting, `shape`
  other, `decision_type` quantity_figure, `answer_unit` count, `gap` [time, population], `pattern` [none],
  `generators` [G3, G13], `gate_g` forecasting, `calibration_form` none, `stump_strategy`
  decomposition_attribution, `context_artifact` capacity_report, `role_family` capacity_planner, `forum`
  council_or_assembly, `forcing_event` budget_or_appropriation, `org_family` research_or_statistics_office;
  `stump_class` analytical; `layer2_family` field_method; `layer2_pattern`
  own:revocation-in-lieu-of-prosecution-rerouted-under-a-conviction-only-act. People from `guard.py names --geo
  "United States" --seed 169`: Ashlee Clayton, Donald Kramer, Brandon Walter (Kristy, Karen and Cassandra dropped
  on people.first WARNs).
- **Axes redrawn at the probe, and why the replacement is the honest one.** `context_artifact` register blocked
  against task249: the stakeholder's own file is the Department's monthly population and capacity report, so
  capacity_report. `org_family` government_agency blocked against task273: in Pembroke, as in the states whose
  sentencing commissions own the projection, the forecast is the Commission's, a research_or_statistics_office.
  `forum` committee_or_panel blocked against task249: the projection goes to the General Assembly's
  appropriations committees, council_or_assembly.
- **Guard.** `guard.py check` WARN only. repeat.question_form (how-many against task273) is answered by the
  decision: the call is a count of people, so it asks how many. test.same_puzzle_older against task172 carries its
  differentiation on the card (a deadline cut against a route handed to another institution).
- **Strategy.** decomposition_attribution: every return in the record reached prison by one of two routes for the
  same behaviour (the Board's revocation on the arrest, or the court's commitment months later), whichever acted
  first; the Act closes one route, and the decisive step is how the closed route's arrests divide once they go
  through the other.
- **Data-native sentence.** In Pembroke's record a parolee's arrest reaches prison by whichever route acts first,
  a Board revocation within weeks or a court commitment months later, so the record's new-commitment returns
  measure how seldom the courts got there first, not how often parolees' arrests end in prison; the arrest
  register, the court dispositions and the Board's decisions show each arrest's route, and discharged parolees'
  arrests show the courts' conversion with the Board out of the way.
- **Sources read, and how this differs.**
  - `layer2-rigor-patterns.md` criminology recidivism-risk-assessment 1 (calibration), 2 (fixed follow-up, time at
    risk), 4 (later cohorts), 6 (base rates): each is a lower rung or the default path here; the golden is none
    of them applied as stated.
  - task134 v1 (this cell, spent): competing removals and deaths in a return forecast, and its loop-1 deaths
    (period against cohort, composition, cure models, a forward booking change as rule application). Here no exit
    is censored wrongly and nothing is restated by an order: the closed route's arrests are re-routed.
  - task141 (this cell): selective labels read through magistrates' release shares. Here no decision-maker
    selects whose outcome is seen.
  - task172 (held): a regime change makes a deadline-triggered request bind for most future units. Here a regime
    change hands one institution's share of the same events to another institution with its own conversion.
  - task163 (held): a reform's added applications at their own yield. Here nothing is added: the same arrests
    change route.
- **Screens run as code before the card** (prototype, scratch `proto/p3.py`, 24,000 history releases, 6,500
  projected; truth 21.6 per cent):
  - Lever: the record's new-commitment rate 9.1, with revocations as competing exits about 11; the golden family
    (arrest rate per street day times the courts' conversion by class with the lag to admission) 20.4 to 20.8;
    lever about 55 per cent of the graded figure.
  - Outsider spread: frailty on or off and a replay of the record's arrests with the courts' conversion put the
    family at 18.5 to 20.8, about a tenth of the figure against a lever of a half.
  - Subset (discharged parolees' time only, a flat rate): 9.6, misses (the hazard falls with time since release
    and discharged time sits late). Scalar route (the record's new-commitment rate over the share of parolees'
    arrests prosecuted): 14.0, misses (the record's rate is also cut by revocations removing people early).
  - Dispersion, variance-only and truncation-direction screens do not apply: the decisive quantity is a level,
    the step moves the point, no threshold suppresses a tail.

## Default path

The pipeline a strong analyst builds from the prompt, the Act and the files' grain, every filed rule applied.

1. Link the 2019 to 2024 parole releases to the Department's admissions by DOC number and keep each release's
   first admission within 730 days.
2. Keep the returns the Act still allows: admissions on a new court commitment; revocation admissions are
   dropped (Act 26-114, section 3).
3. Fit a logistic model of a new-commitment admission within 730 days on age, prior commitments, offence class,
   risk level and district over the releases with complete follow-up (AUC about 0.68), and apply it to the
   projected 2027 releases.

Ends on: about 600 of the 2027 releases back in prison within two years (prototype 9.1 per cent of 6,500).

Golden: about 1,300 (20 per cent), every arrest the Board would have answered by revocation going to court and
converting to a prison commitment at the courts' own rate for its class, with the time to admission.

## Stump sentence

A competent solver keeps only the returns the Act still allows, models each 2027 release's chance of a
new-commitment admission within two years on the record's 2021 to 2024 releases and files about 600 (about 700
with revocations treated as competing exits); the step that lands it there is reading the record's new-commitment
returns as what parolees' arrests produce, when the Board answered most parolees' arrests by revoking them and
under the Act those arrests go to court and become prison commitments at the courts' own rate for their offence
class, which puts about 1,300 of the 2027 releases back in prison within two years.

## Three rules

- Task type: recidivism-risk-assessment (Criminology & Justice), which serves Forecasting & Predictive Modeling:
  a release cohort's two-year return-to-prison forecast for the prison population projection.
- Domain test: the deciding quantity is the 2027 cohort's two-year return-to-prison probability, estimated the way
  a corrections forecaster builds it under a change in revocation law: the arrest process per day at liberty and
  the courts' conversion of arrests into prison commitments by offence class, with the route each past return
  took read from the Board's and the courts' records.
- Swap: "how many discharged patients will be readmitted within thirty days once observation stays stop counting"
  keeps a removed route but loses what decides it here: a second institution, the courts, that takes over the same
  arrests at its own conversion and timing; with readmissions there is no prosecutor waiting behind the closed
  route, so the record's other route is the forecast and the task collapses to the default path.
- Layer 1: (planned, each produced by the agencies' own systems) the Department's DOC number against the Bureau's
  state ID and the courts' tracking number, joined through the Bureau's crosswalk; the Board's 2024 move to a new
  case-management system (legacy decisions with condition codes, new ones with separate columns); admissions
  logged at reception and again at the receiving facility; court dispositions amended after appeal; arrests on a
  warrant with no new tracking number; fiscal-year folders against calendar dates; deaths from vital records.
- Layer 2: field_method; the methodological choice that flips the call is building the forward conviction-return
  rate from the arrests and the courts' conversion, against carrying the record's conviction-return rate.
- Decisive step: recognising that the record's new-commitment returns are what the courts reached before the Board
  did, and forecasting under the Act from every parolee arrest at the courts' conversion by class, read off the
  arrests the courts did process (discharged parolees' and the ones the Board left to court).
- Not semantics: every field, code and date read correctly (admission types, revocation bases, disposition codes,
  the Act's section 3) still leaves the default path on about 600, because no field says what a revoked arrest
  would have become in court; that is an inference about the courts' behaviour under a regime the record never ran.
- Not rule application: the Act files which returns remain and the methodology files the cohort, the window and
  the count; executing every filed sentence on the clean truth gives the record's new-commitment rate (9.1 per
  cent, about 600) or with competing exits about 11 per cent, never 20. Enumerated family spread 9.1 to 20.8
  per cent; standing family (the constructions the data leave defensible, all of which route the revoked arrests
  through the courts) 18.5 to 20.8 on the prototype, to be re-measured on the pack; what rules the rest out is the
  arrests' own fates (parolees' arrests reach a court commitment about a third as often while the Board can revoke
  as after discharge, in every district), a loud refutation but one no filed sentence states.
- Analyst test: a strong analyst who links the four agencies' records, reads the Act correctly and keeps only the
  new-commitment returns, modelling them on the obvious covariates, files about 600 (Ends on); with revocations as
  competing exits about 700; only re-routing the revoked arrests through the courts' conversion files about 1,300.
- Estimand: the Commission's projection methodology (filed in the pack) defines the cohort (releases to parole
  with a projected release date in calendar 2027, the Department's projected-release extract), the outcome (an
  admission to prison within 730 days of release), the count and its rounding; the Act files that from 1 January
  2027 the only admissions of parolees are new court commitments.
- No decoy: nothing is planted; no memo, briefing, fiscal note or stakeholder figure argues a return count; the
  Board's annual report gives revocation counts, not a forecast; the wrong answer comes from the easy model alone.
- No certified replay: no certified or published figure is reproduced to recover the method; nothing in the pack
  forecasts 2027 returns.
- Lesson: when a law closes one institution's route to an outcome the record reached by whichever route acted
  first, the forward rate is the behaviour times the remaining institution's own conversion, not the remaining
  route's share of the record; no build on file teaches route substitution between two institutions.

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
