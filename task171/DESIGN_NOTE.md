# task171 design note

**Status: PAUSED at stage 1. Architecture 5 is drawn on paper and not yet registered: its card
(`generator/paper/card_draft.json`) BLOCKs on `ban.strategy` alone, causal_design against task139's architecture 2 in
the last three builds. Register it once that build leaves the window, answer the two WARNs, commit DRAWN and run stage
2.**
Architecture 5 is Corvane Therapeutics' dovikizumab phase 3 induction dose, in pharmacology-pharmacoepidemiology-safety
/ population-pharmacokinetics-exposure-response. It was drawn on 2026-10-26 in the task141 rework, which found task141
already re-rooted by its own session, and the author chose to park it here, the next open Forecasting number.
Architecture 4 (the Marrowfield Turnpike's toll-by-mail collection) was spent at Gate F at stage 4 on 9451b6bd
(2026-10-23) and the fifth rebuild cell found no draw; its record and architectures 1 to 3 are under `## Earlier
screens`. The tracked generator, golden and `target.zip` are architecture 4's until stage 3 replaces them.

## Draw

| Axis | Value |
|---|---|
| Card | `generator/paper/card_draft.json`, architecture v5, not yet registered: `guard.py check` BLOCKs only on `ban.strategy` (causal_design repeats task139's architecture 2, one of the last three builds), with WARNs `repeat.gate_g` and `repeat.deliverables` against task141's architecture 2 and two NOTEs (task104 and task168, older builds differentiated on the card); architecture 4 moved into `lineage` with its fate |
| Domain / task type | `pharmacology-pharmacoepidemiology-safety` (client domain), task type `population-pharmacokinetics-exposure-response` (serves Forecasting): the week-12 clinical remission each candidate induction dose would produce in phase 3, forecast from the exposure-response of the one dose phase 2b tested |
| Objective | Forecasting & Predictive Modeling: the remission rate patients meeting the phase 2b eligibility criteria, which the phase 3 protocol repeats and none of whom is yet enrolled, would show on 300, 600 or 900 mg; forward facing (phase 3 opens in 2027) |
| Shape | `07` (grid of cells): the asks' arm-by-visit grids carry most of the criteria, the call, its components, the chart's named parts and the three files the rest; the arithmetic goes under `## Ask sheet` at stage 2 |
| Decision | `dial_setting` (the induction dose, one setting of three allowed), answer unit `named_option` |
| Mechanism | gap population (decisive: the exposure the file records after week 4 is not the exposure the dose sets, because clearance falls in the patients who remit) then time (it is read after the response began); pattern none, generators G16 (which exposure the forecast is entitled to) then G3 (the recorded exposure is partly the response's doing, not the dose's); Gate G `forecasting`; strategy `causal_design` |
| Layer 2 family / pattern | `estimand_identification` (the variation that identifies a dose's effect); `own:exposure-read-after-the-response`. The library's card 3 for this task type (exposure-response confounded by clearance, cured by several randomised doses or by adjusting for clearance determinants) is the default path's own careful version here: adjusting for every baseline clearance determinant leaves the call at 900 mg |
| Furniture | forum `regulator_or_inspector` (the dose is the sponsor's proposal at the end-of-phase-2 meeting, whose agreement on the phase 3 dose the meeting seeks), forcing event `statutory_or_regulatory_filing` (the briefing package is due to the agency on 4 December 2026), organisation family `manufacturer`, role family `research_desk` (the head of clinical pharmacology owes the dose), context artifact `filed_standard` (the phase 3 dose-selection charter: the candidates, the forecast's population, outcome and window, the rule, and no exposure measure), calibration `none`, opening `question-first`, question form `what`. The last three builds at the screen (task270, task141's architecture 2, task139's architecture 2) carry none of them |
| Spine | `cvn2184_201_serum_concentrations.csv`, the bioanalytical laboratory's dovikizumab results: one row per serum sample and analytical run, pre-dose at weeks 0, 4 and 8 and at week 12 for every dosed patient, with the intensive-sampling substudy's first-interval samples; synthetic |
| Deliverables | `induction_dose_memo.docx` (the dose for the briefing package and its case), `phase2b_induction_tables.xlsx` (the ask tables), `exposure_response_chart.png` (the chart the call rests on) |
| People | drawn with `guard.py names --geo us --seed 171 --n 30`, skipping architecture 4's names and every first name the guard warns on: Kathy Harvey (head of clinical pharmacology, the requester), Bryan Castro (biostatistics lead), Kristin Lucas (bioanalytical study director, Brightwater Bioanalytics), Darryl Terry (clinical program lead), Theresa Mcdowell (clinical data manager), Kathleen Riggs (drug safety physician); none appears in the prompt |

**Guard.** `guard.py check` on `generator/paper/card_draft.json`: BLOCK on `ban.strategy` alone. causal_design is
the honest label (the recorded exposure is partly the response's doing, so the dose's effect has to be read where the
design isolates it), and it repeats task139's architecture 2, drawn the same evening, so the card is registered only
once task139's architecture 2 leaves the last three builds; the label is not changed to clear the ban. The WARNs
`repeat.gate_g` (forecasting, beside task141's architecture 2) and `repeat.deliverables` (docx, png and xlsx, the same)
are answered at stage 2: the Gate G mechanism follows from a forecast dose in the Forecasting lane, and the deliverable
set is re-chosen if task141 still sits in the window then. The two NOTEs are differentiated below. In the session that
drew it, before it moved here, a first version (gap time, decisive G16, `pick_one_of_n`) BLOCKed `test.same_puzzle`
against task270 and `test.same_driver_older` against five builds, and a second (decisive G3) BLOCKed `ban.pattern`
against task304; the card reads gap population first, G16 decisive and `dial_setting`. Four first names the guard
flagged on seed 171 (Sandra, Sean, Erika, Andrew) and three more on the second pass (Bethany, Todd, Marissa) were
redrawn.

**Same-puzzle and same-driver tests.** Gap population, decisive G16, `dial_setting`: task104 alone carries the triple,
and its insight is re-thresholding a self-adapting scorer's log whose flagged observations never enter the scorer's
reference; nothing here is replayed at another setting. Gap population, G16, Gate G `forecasting`: task168 alone, a
capped departure's demand completed from the same month's booking build; nothing here is censored or completed, the
record holds every exposure and every outcome.

**Abstraction test.** Stripped of nouns, the driver: each unit's response is modelled on its own level of an input it
is given, but units that respond lose the input more slowly once they respond, so every level read after the response
began carries the response; a change in the amount given moves only the level the amount sets, read before the
response could change how the input is lost, and there the relationship is flat. The three nearest drivers on file
(0.07): task182 v1 lineage (a level following a shared external driver through a lagged response), task270 v7 (losses
recorded only as they are replaced, completed at the year's ends) and task479 v4 lineage (a level estimated through a
known response model). None shares the latent structure, a feedback from the outcome to the exposure within each unit,
or the default path, a dose-response read on the fed-back exposure. task178's absorbing agent (a forward dispersion
once an agent that traded against each shock stops) is the nearest idea in kind, a simultaneity, and it removes an
agent rather than reading an exposure before its feedback.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting` (90 builds): no build carries an
exposure fed back by its own response; `guard.py slots` on the setting's nouns finds this task type screened three
times, each set aside before a card: task179 (target-mediated elimination measured dead, eleven on paper including card
3 and an anti-drug-antibody feedback left as an open fork in a PK forecast), task178 (sixteen on paper, card 3
blocked as the cell's own card) and task170 (twenty on paper, the confounded exposure-response card blocked by the
window). Each screened a pharmacokinetic forecast or card 3's baseline confounding; none screened response-dependent
clearance in an exposure-response dose forecast, and the reason it differs from card 3 is measured below (covariate
adjustment leaves every late-exposure member at 900 mg). `layer2-rigor-patterns.md`, this task type: card 1
(covariates inside the mixed model) and card 2 (allometric centring) are lower-rung conventions, card 3 is the default
path's careful version. `two-layer-task-design.md`: rule 1's swap is run on the call sentence under `## Three rules`.
`measured-drivers.md`: held tasks sit upstream of every graded figure; the exposure choice sits upstream of every
forecast and of the call.

**World.** Corvane Therapeutics (fictional, Cambridge, Massachusetts) develops dovikizumab (CVN-2184), a humanised
IgG1 monoclonal antibody against the p19 subunit of interleukin-23, for moderately to severely active ulcerative
colitis. Study CVN2184-UC-201, a randomised, double-blind phase 2b at 71 sites in the United States, Canada, Poland and
Hungary, randomised 540 patients 2 to 1 to dovikizumab 600 mg or placebo, IV at weeks 0, 4 and 8, stratified by prior
biologic or JAK inhibitor failure; the primary endpoint is clinical remission at week 12 on the modified Mayo score.
Serum dovikizumab was drawn before the infusions at weeks 0, 4 and 8 and at week 12, and in an intensive-sampling
substudy of 36 patients also through the first dosing interval. Phase 1 (healthy volunteers, 100 to 1,200 mg IV) found
linear, dose-proportional pharmacokinetics. Corvane's phase 3 dose-selection charter, adopted before unblinding, sets
the rule: phase 3 carries the lowest of 300, 600 and 900 mg IV at weeks 0, 4 and 8 whose forecast week-12 clinical
remission rate is no more than 5 percentage points below the highest of the three forecasts. As-of: the database lock
of 14 July 2026; the request is made in late October 2026 for the briefing package due 4 December 2026.

**Data-native sentence.** The phase 2b records remission at week 12 but serum troughs at weeks 4, 8 and 12, and
dovikizumab's clearance falls by about a third once a patient's colitis starts to heal, from around week 4, while it
drifts up in patients who do not respond, so every trough after the first is partly drawn by the response; the dose
sets the week-4 trough, which comes before it, and on it week-12 remission is flat.

## Three rules

- Task type: pharmacology-pharmacoepidemiology-safety, population-pharmacokinetics-exposure-response (serves
  Forecasting): the week-12 remission each candidate induction dose would produce, forecast from the phase 2b
  exposure-response of the 600 mg arm.
- Domain test: the deciding quantity is the forecast week-12 clinical remission at 300, 600 and 900 mg, which
  model-informed dose selection reads off an exposure-response model of the tested arm with exposure scaled to dose by
  linear pharmacokinetics; it turns on the pharmacokinetic fact that an antibody's clearance tracks the inflammatory
  burden of the disease it treats and falls as the colitis heals, so the field's own exposure measures differ in what
  they carry.
- Swap: "a call centre setting its agent count from the answer speed each staffing level would give, read off its
  past weeks" keeps a dose-like dial and an outcome, but nothing in it has a clearance the outcome changes, a dosing
  interval, or a first trough drawn before the response, so the reasoning that decides (which exposure the dose sets)
  has no counterpart and the task stops making sense.
- Layer 1: the two central laboratories' units (albumin in g/dL and CRP in mg/dL in the US, g/L and mg/L in Europe);
  the bioanalytical laboratory's reassays beside reported results and below-limit concentrations as text; pre-dose
  samples drawn after the infusion started at a few visits, the sample log in site local time and the pump log in UTC;
  interrupted infusions recorded by delivered volume; site-subject numbers against randomisation numbers through the
  randomisation log; the efficacy data in two overlapping releases (topline extract and database lock with adjudicated
  endoscopy); e-diaries from two device generations, one in UTC and one in local time, with re-synchronised
  duplicates. Each is what the named system produces; none decides the call.
- Layer 2: family `estimand_identification`; the choice that flips the call is reading the dose's effect on exposure
  the dose sets (the week-4 trough, drawn before any patient's clearance moved, or the dose itself through it) rather
  than on steady-state exposure, which the remission itself raises.
- Decisive step: in the field's words, the exposure-response that carries a dose forecast is read on the first-interval
  trough, because clearance is time-varying and response-dependent here, so the week-8 and week-12 troughs, the
  induction-average concentration and every post-hoc exposure from a time-invariant fit are partly an outcome of the
  remission they are meant to predict.
- Not semantics: every field, unit and code read correctly (the troughs, the remission flags, the dosing records, the
  laboratories' units) still leaves the field's steady-state exposure-response on 900 mg; no column, code, flag or
  definition marks which concentration the dose set, and the step is the causal reading of when each sample was drawn
  against when clearance moved.
- Not rule application: the charter files the candidates, the forecast's population, outcome and window and the
  5-point rule, and no filed rule names an exposure measure, a model or a sample. Measured on five paper worlds
  (`generator/paper/fam5.py` on `sim_er4.py`): the enumerated family (the week-4, week-8 and week-12 troughs, the mean of
  the troughs and a one-compartment fit's average concentration, each unadjusted, stratified, fully adjusted for the
  baseline clearance determinants, as an Emax model and on the week-12 albumin) spreads the 300 mg forecast from 12.6
  to 43.6 per cent, 31 whole percentage points, and files 300, 600 or 900; the standing family (exposure read before
  clearance moved: the week-4 trough under every model and adjustment, and the week-12 trough instrumented by it)
  spreads the 300 mg forecast by 1.7 to 4.8 points on those worlds (median 2.5 over 40) and files 300 on every member
  in 24 of 40 worlds in the sweep, the build's world chosen and asserted among them. The ruling-out is one group-by
  nothing invites: the remitter to non-remitter geometric-mean trough ratio by visit, 0.95 to 1.16 at week 4, 2.1 to
  2.5 at week 8 and 3.0 to 3.6 at week 12.
- Analyst test: a strong analyst who reads every file correctly, keeps valid troughs and applies the charter runs the
  field's standard exposure-response on each patient's steady-state exposure (the week-8 or week-12 trough, the mean of
  the troughs or a one-compartment fit's average concentration), with or without baseline albumin, weight, CRP and
  prior biologic, forecasts 300 mg 8 to 29 points below 600 mg and 900 mg 5 to 22 points above, and files 900 mg
  (600 mg in one member of 85 on the five paper worlds, never 300).
- Estimand: the week-12 clinical remission rate, on the phase 2b protocol's modified Mayo definition with
  non-responder imputation, that patients meeting the phase 2b eligibility criteria (which phase 3 repeats; none yet
  enrolled) would show on each candidate induction regimen, each dose's forecast compared with the highest of the
  three; filed in `cvn2184_phase3_dose_selection_charter.pdf`.
- No decoy: nothing is planted. The troughs, remission flags and laboratory values come from one generating process;
  no memo, plan, slide, draft or prior analysis states an exposure measure, an exposure-response or a dose preference;
  the investigator's brochure states linear pharmacokinetics and phase 1's clearance covariates and nothing about the
  phase 2b data.
- No certified replay: no certified, published or prior-period figure is reproduced to recover the method; the
  forecast is built from the phase 2b records alone and nothing in the pack scores an exposure measure.
- Lesson: an exposure the response itself changes cannot carry a dose forecast; when an antibody's clearance falls as
  the disease remits, only the exposure read before the response moved it measures what the dose set. No build on file
  teaches response-driven exposure, and the library's clearance-confounding card is cured by an adjustment the default
  path already makes here.

## Default path

1. Read the charter: candidates 300, 600 and 900 mg IV at weeks 0, 4 and 8; the forecast is week-12 clinical
   remission in the phase 2b population; phase 3 carries the lowest dose within 5 points of the highest forecast.
2. Join the bioanalytical results (`cvn2184_201_serum_concentrations.csv`) to the randomisation log, keep the reported
   result of each sample and the troughs drawn before the infusion started, and put every concentration in ug/mL.
3. Take each 600 mg patient's steady-state exposure, the field's measure for an induction exposure-response: the week-8
   trough (or the week-12 trough, the mean of the troughs, or the average concentration from a one-compartment fit).
4. Attach the week-12 clinical remission flag from the database-lock efficacy release, non-responder imputation for
   discontinuation and rescue.
5. Fit week-12 remission on log exposure by logistic regression with prior biologic failure, baseline albumin, CRP,
   modified Mayo score and weight (the library's adjustment for clearance determinants).
6. Scale every patient's exposure by dose over 600 (linear pharmacokinetics, phase 1) and average the predicted
   remission: in world 1, on the week-12 trough fully adjusted, about 23 per cent at 300 mg, 40 at 600 mg and 51 at
   900 mg.
7. Apply the charter: 900 mg has the highest forecast and 600 mg sits 10.5 points under it, so phase 3 carries 900
   mg.

Ends on: 900 mg (the steady-state exposure-response; every late-exposure member of the family files 900 mg on the
paper worlds, and `checks.py` will assert it on the built world).
Golden: 300 mg: on the week-4 trough, drawn before any patient's clearance moved, week-12 remission is flat in
exposure, so 300 mg forecasts within a few points of 600 and 900 mg and is the lowest dose within 5 points of the
highest forecast.

## Stump sentence

A competent solver fits the exposure-response on each patient's steady-state dovikizumab exposure, adjusted for every
baseline clearance determinant, scales it by dose and files 900 mg (Ends on; 300 mg 8 to 29 points below 600 mg and
900 mg 5 to 22 above across the late members on the paper worlds); the step that lands it there is reading exposure
after clearance had already fallen in the patients who remit, when the week-4 trough, drawn before any patient's
clearance moved, shows week-12 remission flat in exposure and puts 300 mg within a few points of 600 mg, so phase 3
carries 300 mg.

## Paper world

`generator/paper/sim_er4.py` (one-compartment linear clearance about 0.40 L/day, log-normal between-patient variation 35
per cent, weight and albumin on clearance, the true dose effect an Emax on the induction-average concentration with
EC50 1 ug/mL so every candidate dose sits on the plateau; in patients who remit an unmeasured inflammatory-burden term
lowers clearance by 38 per cent from a median of day 26, in responders without remission by 10 per cent, and in
non-responders clearance rises 10 per cent; albumin rises 2 g/L in remitters and adds its own small fall in clearance),
360 on 600 mg and 180 on placebo, troughs before the week-4 and week-8 infusions and at week 12, assay error 12 per
cent. `generator/paper/fam5.py` scores every member on five worlds and `fam5_sweep.py` on 40.

| World (seed) | 600 mg observed | true 300 mg | week-4 trough family, 300 mg forecast | its calls | late family, 300 mg forecast | its calls |
|---|---|---|---|---|---|---|
| 1 | 40.0 | 39.2 | 38.9 to 41.1 | 300 in 7 of 7 | 16.8 to 29.8 | 900 in 17 of 17 |
| 2 | 39.2 | 38.6 | 37.2 to 38.9 | 300 in 7 of 7 | 14.6 to 31.3 | 900 in 16 of 17 (one files 600) |
| 4 | 41.7 | 40.8 | 40.3 to 43.4 | 300 in 7 of 7 | 19.2 to 32.3 | 900 in 17 of 17 |
| 17 | 41.4 | 40.0 | 35.2 to 40.0 | 300 in 5 of 7 | 12.6 to 27.6 | 900 in 17 of 17 |
| 29 | 42.5 | 41.4 | 40.7 to 43.6 | 300 in 7 of 7 | 17.3 to 31.0 | 900 in 17 of 17 |

Over 40 worlds the standing family files 300 on every member in 24 (its worst member's gap to the top forecast median
3.9, at most 9.4) and the default family never files 300 (its closest member's gap at least 11.5, median 15.8). World 17
is one of the 16 that fail: its week-4 geometric-mean ratio sits at 1.16, so two week-4 members file 600. The build's world is drawn
among the 24 and its margins asserted. These figures are `python3 generator/paper/fam5.py 1 2 4 17 29` and
`python3 generator/paper/fam5_sweep.py 40` on the parameters `sim_er4.py` now carries as defaults (the draw's
calibration; the run that first measured it was not kept, and its figures were one world and a tenth of a point
apart). The 600 mg forecast equals the observed rate under every logistic member,
so the three forecasts differ only at 300 and 900 mg.

## Earlier screens (architectures 1 to 4, kept as history)

**Architecture 4 (2026-10-23, spent at Gate F on 9451b6bd).** The Marrowfield Turnpike Authority's first
all-electronic tolling year (economics-econometrics / forecasting-forecast-evaluation): the 2027 toll billed by mail to
today's cash-lane users and how much of it is collected, matured on each in-state plate's two-year registration renewal
rather than on the invoice's age (golden $13.75 million, in-state 94 per cent and out-of-state 60 per cent, against the
default path's $12.00 million on year-old invoices). Stage 3 was green (checks 69 of 69, verify, two byte-identical
rebuilds, figures_check 43 of 43, precut 51 checks, voice-check PASS) and blind reader B landed the call by measuring
the renewal-hold channel the policy states; the asks held 0 of 22. Its card moves into the architecture 5 draft's
`lineage` with that fate. Its draw and stage-2 sections (readability screen, fork table, ladder, closure, literal
reader, oracles, ask sheet) are in this note as of da7c0b81; its generator, golden and zip are still tracked here. The
death line is in `## Tried and rejected`.

**Architecture 3 (2026-10-23, spent at Gate F on ce04ed65).** Sablewood Electric Cooperative's optional overnight
rate R-ON for 2027, its members and shortfall priced on each R-1 member's own bill saving through the first-year
take-up of the March 2024 evening-peak rate R-TOU, read on the use of the year before that rate was offered because
its takers moved use out of 4 to 9 p.m. after joining (golden 2,250 services and $200,000 against the default path's
1,000 and $100,000). Stage 3 was green (checks 76 of 76, verify, byte-identical rebuilds, figures_check 41 of 41,
precut 51 checks, voice-check PASS) and scored reader B landed the call and all 20 ask figures, calibrating the launch
cohort on its pre-launch use by default; its card moved into `lineage` with that fate and its generator was replaced
by architecture 4's. The death line is in `## Tried and rejected`.


**The 2026-10-19 status: PAUSED at stage 1, no card registered, nothing cut.** The receiving-desk architecture was
re-rooted on the coordinator's call, and the re-draw screened the actuarial mortality-longevity cell on code
(three designs, prototypes a1 to a7 and b1) and the human-reliability cell on code (h1, h2). A second screen
took the coordinator's two candidates on code (screenA: event prediction in an outcomes trial, then fatigue
under a longer-shift roster), and neither held on measurement. A third and final screen (screenC) took the
coordinator's read-across candidates on code, F (a first annual renewal in a second market, measured in full
in an earlier market) and G (a new meter batch's failures, read from an older batch of the same design), with
the four stumping 1.2 screens of eda6c8c run first, and neither held. A fourth screen, the author's redraw in a
new world, took the political-science-public-policy cell (election-polling-forecasting) on code under the
round's bans (scratch r171/proto: seats_sim.py, tactical_sim.py), with stumping 1.3's library test applied, and
nothing held; a fifth took the scaling-laws cell the same way, and nothing held there either. No architecture
is live. This note holds the screen record only; it carries none of the `precut.py` sections, because no
design exists.

**The election cell, in one sentence.** The quantities with enough rows to price at the bar (seats from
constituency results, turnout from registers, ballots from tracking files) have textbook routes a back-test
settles, and the judgments beyond them are composition-type (who is in the electorate, which ballots remain,
which seats declared first, out this round), or carry levers under 20 per cent because the last result already
embeds the structure, or rest on an election-level behaviour estimated from a handful of past elections;
poll-based shares and margins fail on arithmetic before any of that.

**The scaling-laws cell, in one sentence.** A fifth screen took general-statistics-data-science (scaling-laws, the
subdomain never drawn) on code (scratch r171/proto: cbs_sim.py, dir_sim.py), with the client's three cards as the
default path: every judgment beyond the cards puts runs on a common exposure (batch-efficient tokens, the value of a
repeated token, a completed-schedule equivalent), so where some runs attain the plan's condition the effect is a filter
and a divide on them, and where none does its dependence is extrapolated by forms the runs cannot tell apart, while the
graded figures that can carry a 30 per cent lever (token and compute budgets) carry inversion noise of 10 to 50 per cent.

**The structural sentence, and the first thing to read.** A near-term mortality quantity of a population the
record observes every year is reproduced by carrying the last period's amount-weighted rate onto the current
roll, because next year's population is this year's population one year older; every analytical correction
the field owns (the amounts gradient, credibility, improvement, banding, a covariate model) corrects a
quantity the persistence route already measures in the right units, so the decisive step has to act on a
period the record never contained (the client's "a known schedule change makes the next period genuinely
differ"), and in mortality the scheduled changes are premium steps, which live on thin life-insurance deaths,
and benefit changes, which only move weights the persistence route can re-weight. The second screen met the
same wall from the other side: where the coming window differs from the record only in cells the record has
not yet filled (durations the late, lower-risk entrants have not reached; hours on duty most of a workforce
has never worked), either the field's standard forms disagree in those cells by more than any rival misses
by, or a straight line carried through the filled cells lands, so a draw here needs a coming-window
difference that the record measures in full somewhere else in itself. The third screen built exactly that and
found the read-across is the common-exposure subset screen's completion branch: no unit of the target has
reached the exposure, so the step aligns its units with a population that has, at a common point (the same
month of the term, the same age), and that alignment is itself a filter and a divide on the attaining
population, while every partial alignment (an earlier common point, a ratio of a related rate, a band at the
wrong point, a haircut) lands inside the bin the full alignment's own family needs, because the family spreads
as the target moves away from the attaining population, so the gap that moves the rivals out widens the bin
with them.

## Tried and rejected

- **Architecture 1, a regional grocery network's receiving desks (supply chain, never registered).** The 90th-percentile tractor count a DC closure needs was meant to turn on queueing at the receiving desks, but a flat 20 to 30 minute dwell uplift reproduces the queue's effect on that statistic within a tractor, and in the overload regime the stump needs the standard congestion constructions disagree (the M/D/1 desk is undefined there, the fluid queue runs 3 tractors under the discrete-event replay, the empirical wait curve 9 under, the hourly M/D/1 23 over or 3 under), so neither strength nor determinism held (prototypes p1 to p27, p27 the coordinator's four-construction and flat-uplift test).
- **Levers rejected inside architecture 1.** Drive-time calibration (another scalar correction a flat uplift absorbs); reverse congestion at a slow Northgate desk (about one response in three lands it); roster-capped demand rebuilt from release times (task168's driver, and the release times would have to be named in the estimand); dispatch re-timing (it works only with a filed or withheld dispatch rule).
- **A miners' pension trust's 2027 pension release, where larger pensions die sooner (actuarial mortality-longevity, prototypes a2 to a7).** A flat dollar rate per year of credited service makes the pension track years underground, so the amount-weighted experience ratio runs 11.6 to 13.0 per cent above the head-count ratio and every textbook factor (amounts lighter than lives) points the wrong way; on a cohort-built fund (miners only, 2023 to 2026 experience) the head-count route misses by 10.4 to 11.5 per cent, the head-count ratio times 0.95 by 14.9 to 15.9, times 0.90 by 19.4 to 20.3, the table at face value by 26.7 to 28.7, and the head-count route fails the 2026 hold-out by 3.3 to 5.6 standard deviations. It died because the release is observed every year: last year's release rate on the December roll lands 3.1 to 5.8 per cent from the golden even in a closed, ageing fund (the four-year crude rate 6.5), inside any bin that holds the twelve golden-family estimators (range 1.2 per cent) and one sigma (1.0 per cent), so the plainest rule of thumb lands, and a solver who weights by amounts lands too (the step is a coin flip).
- **The same trust's liability for the miners' pensions.** No persistence route exists, but on the same fund at 6 per cent the head-count multiplier moves the present value only 4.1 per cent against the generator's member-level model while a single amount-weighted multiplier lands 1.0 per cent under it (the service GLM 0.2 under, the table at face value 13.0 over), so no bin separates the rival while holding the estimators, and the decisive step reduces to the weighting a literate solver takes by reflex.
- **A term insurer's ten-year level-premium step (series A through its step in 2022 to 2024, series B stepping in 2027, healthy lives leaving at the step; prototype b1).** It died on determinism: series A's 27,332 persisters carry 117 deaths in their first post-step year and series B's forecast year 32, so face-weighted rates by jump band carry 10 to 20 per cent sampling error, and the band-matched golden route moved minus 13 and plus 33 per cent against the simulated claims across two seeds. A step at an anniversary is also task107's driver.
- **Screeners' threat-image detection under a summer roster with 30-minute X-ray stints and a large new-hire cohort (human-reliability-assessment, prototypes h1 and h2).** Persistence, tenure-only and minutes-only routes sit 1.5 to 4.3 points above a golden family that spreads 0.34 to 0.38 points within a seed, but the learning curve's form alone (exponential against logarithmic in experience) moves the figure 0.34 to 0.38 points, so whole-percent grading has no quarter-bin margin; both moves are visible attributes (stint length on the roster, tenure from the hire date), which is the reflex death task202 recorded for time on task and task182 for experience composition. The stronger variant, vigilance restored only by a break and not by a rotation, repeats task132's reset clock.
- **Paper screens, not coded.** A pandemic-contaminated window (the fund's level against contemporaneous population mortality): excluding 2020 and 2021 is the field's reflex and lands within 2 per cent, and the as-of would sit in early 2023, where a solver's own knowledge of 2023 mortality is an outside fork. Experience-rated employer groups chosen for the worst ratio: credibility toward the manual rate is the field's reflex and lands. Election polling: every vote-share family (house effects, likely-voter turnout, undecided allocation) spreads wider than the margin any rival misses by. Population pharmacokinetics: the decisive structures (renal covariate, accumulation to steady state, Michaelis-Menten elimination, unbound fraction) are filed formulas (rule application) or tail counts whose method families spread.
- **Event prediction in a blinded event-driven outcomes trial whose protocol amendment opened enrolment to lower-risk patients (biomedical-clinical-research, survival-time-to-event-analysis, the forecasting task type, since clinical-trial-design-analysis serves only experiment-causal; prototypes in screenA).** The count of first adjudicated primary events over the next 3 to 12 months, forecast from blinded pooled data, was to turn on the hazard by time since randomisation within entry cohort, because a hazard pooled over every entrant lends the late, lower-risk entrants the early entrants' hazard at the durations they are about to reach. It died on measurement in every layout tried. On a frailty-and-mixture truth (12,000 patients, Weibull shape 0.6, gamma frailty 0.5, the post-amendment cohort at about 0.6 of the earlier risk, 9 and 12 months ahead) the standard cohort-aware forms spread from 13 to 25 per cent under to 4 to 10 per cent over their median (log-normal 11 to 13 under, Cox 5 to 11 under, the stratified piecewise model 13 to 25 under, the Weibull 3 to 7 over), sigma 9 to 16 events on medians of 185 to 263, while the pooled Weibull sits only 15 to 18 per cent over the median and the pooled log-logistic 13 to 15. On a clean proportional-hazards Weibull truth (6,500 to 11,000 patients, cohort hazard ratio 0.4 to 0.5, 12 months ahead) the family spread 58 to 157 events on medians of 289 to 572 with a patient-bootstrap sigma of 16 to 22, so a bin holding it needs 197 to 396 events, against a nearest rival (the pooled log-logistic, or the last three months' events per patient-month) 25 to 85 off. On the most favourable layouts (a small early cohort with a long low-risk enrolment, or a late amendment, 3 to 12 months ahead) the three core forms alone (Weibull, Cox with its baseline carried on, piecewise exponential, each with the cohort term) spread 20 to 45 events on about 230 at nine months, sigma 3 to 15, bins needed 45 to 204, nearest rival 9 to 62 off, and even with no family spread the pooled log-logistic sits under four sigma of the golden in two of three seeds. The dial: the cohort effect bites only at durations the late entrants have not reached, so the golden itself carries a hazard into unobserved cells (proportional hazards borrowed from the early cohort, or the late cohort's own shape extrapolated), and that carry is what spreads the family; shortening the horizon to stay inside observed durations hands the call to the last months' events per patient-month, 12 to 30 per cent over at 9 to 12 months and 9 to 12 events off on about 100 at 3 months. The amendment notice the pack would carry also makes the decisive rung readable, and the duration piece without the cohort is task134 v2 round 1's driver (guard 0.18, the nearest).
- **Dispensing errors in a hospital pharmacy moving from 8-hour to 12-hour shifts, with hours 9 to 12 worked only on overtime extensions taken by staff whose own error rate is low (human-factors-ergonomics; the forecast would sit in human-reliability-assessment, since workload-fatigue-shift-analysis serves only root-cause; prototype simB).** On 70 staff over two years (about 32,000 shifts, 7,500 to 8,000 errors, volunteers selected two standard deviations on the logit of the person effect) the right family (person fixed effects with hourly or grouped duty-hour categories, a two-slope spline, with or without time of day) agrees within 1.0 per cent and a within-person shift bootstrap puts sigma at 2.2 to 2.3 per cent, so a bin holding it needs about 11 per cent of the forecast (440 to 470 errors); the pooled duty-hour model misses by 15 to 19 per cent and the flat rate per item by 13 to 15, but the gradient over hours 1 to 8 carried in a straight line to hour 12 lands 0.4 to 9.2 per cent from the golden (0.8 to 9.3 pooled), and the published 27.5 per cent excess for 12-hour shifts 8 to 11 per cent over, both inside the bin. The decisive step itself (the gradient read within each person rather than across people, applied to a forward plan that lengthens every shift) is task149's driver by the abstraction test (guard 0.15, the nearest), in the human-reliability cell where this slot's screener design already died.
- **A first annual renewal in a second market, read across from a first market whose annual cohorts have renewed in full (product-analytics, retention-cohort-lifetime-value-modeling; prototypes simF, runF, sweepF and screensF in screenC).** Market B's annual terms, six to eleven months run at the as-of, renew inside the window; market A's 29,900 complete first terms carry the only renewals on file; the golden reads each open B term from the state it has reached (auto-renew status, engagement) through A's renewals at the same month of the term. The eda6c8c screens, as code: dispersion and truncation do not apply (a level, no suppressing threshold); variance-only passes (the step moves the point estimate, lever over noise 9 to 45); the common-exposure subset screen fires, because no B term attains month 12 (0 of about 10,600), so the escape is completion from an attaining population that differs from B (B's engagement 0.34 to 0.50 sd lower at the same month), and the golden is itself a filter and a divide on A (banded same-month rates within 1.4 to 2.1 per cent of the logistic) while the attaining population's plain filter and divide (A's raw rate) misses by 16 to 28 per cent. Separation fails as well: across 36 runs (market gaps of 0.25 to 0.8 sd of habit, three persistence settings, three seeds) the family (two logistics, banded rates, a forest, a tree, engagement only, every month observed, a second-order chain) spreads 1.0 to 6.0 per cent with sigma 0.74 to 1.27, so the bin needs 5.3 to 16.1 per cent, and 6 to 11 routes land inside it in every run: A's renewal by month-1 engagement band in all 36 (0.25 to 0.92 bins), the end-of-term engagement band scored on present engagement (0.18 to 1.02), trial-day bands (0.40 to 1.17), the memoryless chain (0.46 to 1.10), the engagement-ratio and monthly-plan-ratio adjustments at the smaller gaps, a 10 to 30 per cent haircut and a textbook 30 to 35 per cent renewal rate at every gap. The bin widens with the gap because the family spreads as B moves away from A (a single dial), and the A-trained family itself runs up to 6 per cent above the truth on B's prior shift. guard.py slots found no earlier screen of the mechanism.
- **A new smart-meter batch's failures in its third year, read from an older batch of the same design observed to age ten (energy-systems-utilities, asset-condition-maintenance; prototypes simG, simG2 and sweepG in screenC; task164's peak-coincidence driver untouched).** 600,000 new meters at ages 2.0 to 2.5 and 900,000 old ones at 8 to 10, about 9,800 new-batch failures, a bathtub hazard (early-life decay, a constant, a wear-out onset); the golden is the old batch's age-specific rate at the window's ages scaled by the new batch's level against the old at the ages both have reached. The common-exposure subset screen fires: no new meter attains ages 2.5 to 3.5, the attaining old batch's own filter and divide misses by -23 to -27 per cent, and the golden is two filters and a divide (the new-to-old ratio over ages 1 to 2.5 times the old forward rate lands -0.2 to +3.2 per cent from it), the batch comparison at common ages any reliability analyst makes first. Under a proportional-hazards truth (five seeds) the family spreads 1.2 to 8.6 per cent with sigma 2.6 per cent, so the bin needs 13 to 27 per cent, and the accelerated-time form (+18 to +22), the new batch's cumulative rate carried (-13 to -17) and its last six months' rate (-15 to -23) sit inside it in most seeds, the new batch's 2026 rate (-20 to -26) and the old batch raw at about one bin. And the form that carries the batch difference into the ages the new batch has not reached decides the figure: under an accelerated-time truth, or a difference in the early-life mode only, the proportional-hazards family runs 16 to 27 per cent off the truth, told apart only by a likelihood ratio on the early ages (+17 to +63 units under the proportional truth, -29 to -55 under the accelerated one), which is the structural sentence's first horn again. A Weibull fitted to the old batch, the field's first form, runs +67 to +74 per cent.
- **Election polling, the swing scale (the redraw's lead; political-science-public-policy, election-polling-forecasting; seats_sim.py).** A seat projection under a filed national scenario (600 seats, six past elections, a third party C rising 15 to 20 per cent, the governing party falling 36 to 33) was to turn on the scale of the change across seats, uniform swing being the default. It died on stumping 1.3's library test, measured: under a logit truth the back-test of uniform, proportional and logit swing on the five past pairs picked logit in 4 of 4 seeds and landed within 0 to 5 seats of the truth's 64 to 72 C seats, proportional swing alone within 0 to 3, while uniform swing missed by 17 to 22 seats; under a uniform truth the back-test picked uniform in 3 of 3. The scale is a debate between textbook routes that a careful reader back-tests both sides of.
- **Election polling, a realignment that keeps moving (seats_sim.py, truth realign).** Each seat's lean drifting along a factor recovered from the history of seat-level changes (step 0.10 to 0.50 logits per election, transient noise 0.10 to 0.18) was meant to be the judgment beyond the swing scale. It died on lever: the logit swing the back-test picks lands within 0 to 6 seats of the truth's 83 to 101 C seats at every setting, because the last result already carries five steps of the realignment and one more adds under 6 per cent; the per-seat trend, factor, pooled AR and last-plus-mean-change routes all land inside the same few seats.
- **Election polling, tactical switching when a seat's configuration changes (tactical_sim.py).** The third party's voters moving to the close challenger where the governing party leads (rate 0.25 to 0.60, window 12 to 20 points), so seats entering that configuration gain beyond the swing. Truth 58 to 79 C seats; uniform swing 32 to 48 per cent under, but the logit swing the back-test picks only 5 to 13 seats (9 to 17 per cent) under, a swing stratified by the last result's winner and runner-up no closer, and the true model's own hard count up to 8 seats from its expected count, so the estimand's hard-or-expected choice forks by as much as the lever and the tactical form (window, decay, who switches) is a free specification.
- **Election polling, paper screens across the cell.** Poll-based vote shares and margins fail on arithmetic (a share cannot move 30 per cent; a margin's sampling sigma is about a point on 10,000 to 100,000 respondents). Turnout after a surge election: the comparable-election reflex lands, and with surge registrants it is composition, out this round. Election-day turnout from the remaining pool after early voting: the timing-against-turnout split rests on an assumption the data cannot force. The late count completed stream by stream: a few hundredths of a point on the margin, and task181's driver. Mail-ballot returns by time since each ballot was mailed: the mailing delay is a stated break, the realigned curve is the subset route, and the driver is task134 v2's and this slot's own screenA death. Expected seats of a party near a threshold: card 1's simulation lands. Phantom swing as a hold: a margin's sigma. Notional results on new boundaries from ward local results: a single-purpose file and the textbook allocation. The local-election swing pattern carried into a general election: a fitted regression on the obvious covariate. Ballot cure deadlines (task172), a holiday in the count's development (task162-like, small), a ranking cap in ranked-choice counts (task168-like), signature-sample duplicates and betting longshot bias (the swap test fails), seat quantile calibration (a variance lever on a few cycles).
- **Scaling laws, the critical batch (general-statistics-data-science, scaling-laws; cbs_sim.py).** A planned 1.5B run forced to an 8M-token batch by a new pod, graded on the tokens to first reach a target validation loss, the judgment beyond the three cards being that tokens stop being the exposure once the batch passes the critical batch, which grows as the loss falls (the steps-against-tokens tradeoff, the critical batch read from the batch sweeps). Truth 383B tokens; the golden (critical batch a power law in the loss) -4 to +4 per cent; the cards' pooled fit +27 to +43, the standard-batch grid -19 to -45, a batch covariate +36 to +41, one pooled critical batch +13 to +17. It died on determinism: the critical batch as a power law in the reducible loss fits the sweeps as well (residual sd 0.046 to 0.070 against 0.039 to 0.066) and lands +73 to +99 per cent (+99 to +230 in a fixed-recipe variant with the plan near its own critical batch, where the cards miss by -42 to -53), and as a power law in data size it runs wild; with the target inside the sweeps' losses the batch factor at the target is a filter and a divide on the largest sweep. The single dial is the target's distance below the sweeps.
- **Scaling laws, card 3's holdout direction against an overtrained plan (dir_sim.py).** A 1B model trained to about 250 tokens per parameter, the judgment being that the form is validated along the plan's tokens-per-parameter axis rather than on the largest compute. It died twice: where the forms differ enough to matter (a coupled truth against the additive form, RMSE 3.6 against 39 to 62 thousandths of a nat) every holdout and the in-sample fit pick the right form, so the card lands; and a token budget near the size's own loss limit swings -22 to +96 per cent across seeds under the true form itself.
- **Scaling laws, paper screens.** Repeated data (the value of an epoch at the plan's count is measured by small multi-epoch runs, a filter and a divide, unless its dependence on model size is extrapolated, which spreads); learning-rate drift with scale (the same dilemma); downstream accuracy read through the loss (the external models nearest the predicted loss are the forecast); continued pretraining from a cooled checkpoint (matched continuation pairs measure the penalty); interval calibration by back-test distance (a handful of origins); best-of-attempts selection at the largest scale (a lever of a few thousandths of a nat); compute accounting from configs, rolled-back tokens and eval-set drift (rule application or Layer 1).
- **Rebuild 2026-10-23, the discrete-choice cell, paper screens before any harness.** The client's three cards (willingness to pay as a ratio, IIA against nesting, scale across samples) are the default path, and each judgment drawn beyond them died on paper: congestion feedback when a toll moves trips onto a crossing that slows with its own volume (task253's and task228's fixed point); a randomised savings-plan invitation whose comparison arm is reached through co-workers (task131 architecture 1's household interference read where a group drew one arm); diversion after a product is withdrawn read from each buyer's browse log (the set a buyer would consider once the product is gone is not the viewed set less the product, and with stockout episodes the diversion is a filter and a divide); logit curvature at each unit's own propensity (task165's own-baseline gain); attenuation from skimmed travel times corrected on a GPS sub-study (skims are zone averages, so the error is Berkson and barely attenuates, and the sub-study sees only the chosen mode's time); a nesting dimension no category names (a likelihood back-test picks it, the election cell's death); choice-based sampling (calibrating constants to counts is the reflex); crop rotation after a price spike (the lagged crop is the obvious covariate); travel-time reliability (mean delay proxies its spread across routes and hours); a customer switching away from a plan whose provider fails (task169's two routes, one closed).
- **Rebuild 2026-10-23, departure-time choice under a 2027 peak surcharge (scratch `b171n/proto/dt1.py`).** A bridge's commuters choosing 15-minute slots under a scheduling-model truth (preferred arrival times, early and late penalties, a lateness step), with an early-bird discount and planned roadworks in the record to calibrate on. Over 18 settings the peak window lost 24 to 46 per cent of its share; a multinomial logit with slot constants and its toll and time coefficients calibrated on the early bird and the roadworks overstated the drop by -1 to +40 per cent (median about +20), and the early bird's slot shifts scaled to the surcharge understated it by 28 to 72. It died three ways: the textbook route sits 15 to 25 per cent of the drop off in most settings, under the 30 per cent lever the held builds carried, and straddles zero in one; the golden is a structural scheduling model over a latent preferred-arrival distribution, so its outsider family is a set of specifications (preferred time from habit or fitted, linear or stepped lateness) rather than one construction; and a peak surcharge names peak spreading, so the adjacent-slot step is the question's own reflex.

- **Rebuild 2026-10-23, measured inside architecture 3 before the pack was frozen.** (1) A take-up truth with one decision and a fixed launch-response curve put the textbook discrete-time hazard 10 to 15 per cent under the 12-month logit on the shortfall, so the truth is the monthly logit hazard the field writes, and the 12-month logit, probit and saving bins sit within 4.8 per cent of it on services. (2) With the overnight rate's customer charge above R-1's, the overnight savings sat left of the evening rate's and every form extrapolated in the lower tail; equal customer charges and the overnight rate's top savers kept inside the evening rate's range removed it. (3) A forecast population with part-year services forked on annualising their saving (2,298 services and $206,671 against 2,216 and $201,673); the paper now files the population as the services billed in all twelve test-year months, and annualising the cohort's part-year savings is rejected by 235 log-likelihood units. (4) Ask B by district and month left 3 to 7 of 15 cells unmoved by the first-service keying, so it is graded by district, with the two-service members' homes in town and their farm dwellings out of town. (5) A re-issue of every R-TOU row at one date put every tenure cell at zero under the in-effect row's start, a loud failure; the re-writes now follow account maintenance after the June 2025 upgrade (42 per cent of spells). (6) Districts named Coldwater and Velma were renamed (Brisco Bend, Tamsey) for real places with utilities, and Arden Flats (Sedge Flats) for reading as a person's name.
- **Architecture 3 (optional-rate take-up, Sablewood Electric Cooperative) spent at Gate F on ce04ed65, 2026-10-23.** Scored reader B filed 2,250 services and $200,000 and all 20 ask figures. Its path: "Cohort = R-1 services at launch, billed 12 months pre-launch, open through 2025-02-28; outcome = on R-TOU 12 months after launch. Logistic on annual dollar saving (R-1 minus R-TOU, 2024 rates, pre-launch use) fits best"; for the asks, "consecutive R-TOU rows (1-day gap) merged into spells ... after dropping the EST row of each EST/ACT duplicate" and "CRM times UTC converted to local ... 'Closed - duplicate' rows dropped". A careful reader calibrating take-up on a launch cohort reads the cohort's pre-launch covariates by default, because that is the textbook way to set up a launch cohort, so the decisive step was the default; and every ask device (spell gaps, estimate and actual duplicates, UTC, duplicate-closed rows) was visible hygiene the battery executes.
- **Rebuild 2026-10-23, after architecture 3: a regional hospital emergency department's low-acuity walk-ins deterred by its posted wait, a 2027 fast-track holding that wait at 45 minutes (healthcare-delivery utilization-access-demand-forecasting; scratch `b171n/proto2/ed2.py`, `screen3.py`, `screen4.py`).** A slotted priority-queue ED with a queue-based hourly posted wait, deterrence exp(-beta x posted) on CTAS 4 and 5 walk-ins, unfilled physician shifts as the exogenous shifter. The lever is 15 to 25 per cent of the CTAS 4 and 5 count, and the naive Poisson with hour-of-week effects is biased by the shared demand shocks (beta 0.05 to 0.10 against 0.13 to 0.18). It died on the family: with the truth at beta 0.18 the deterrence-aware estimators split, Poisson with day effects 0.205 to 0.214, day-demeaned log OLS 0.123 to 0.174, the Wald ratio on the shortfall 0.135 to 0.151, 2SLS on logs 0.152 to 0.182, the control function 0.150 to 0.166, forecasts about 6 per cent either side, so no rounding holds the golden; and the decisive insight (patients answer the posted wait) is the one a reader reaches from the feed the plan's own target names.
- **Rebuild 2026-10-23, paper and arithmetic screens beside it.** An index provider's 2027 watch list making every addition anticipated, the event desk's capture read on the rule-mandated additions (quantitative-finance strategy-backtesting-evaluation): a hedged five-day capture carries about 4.5 per cent of noise against a mean near 0.7, so 600 anticipated additions give a standard error of 27 per cent of the figure and 2 per cent would need about 37,000 events; the short-notice variant (off-cycle additions already at a one-day notice) is the very subset the rule change names. Cross-border fuel excise after a unilateral rate rise (time-series-macro): the neighbour's price survey on the textbook path names the mechanism and the one tax holiday in the record sizes it from a single episode. A kindergarten entry cut-off moved from 31 December to 1 September, delayed entry by relative age read from a second board already on 1 September (sociology population projection, spent by task176 besides): relative-age redshirting is common knowledge and the second board's pattern is the analogue a reader takes. A five-year mortgage reset's defaults on its payment shock (credit-scoring-pd): the payment shock is the covariate every reader fits. Bunching at a tax kink moved forward: the counterfactual density is a polynomial knob. Forestalling before a tax rise and a toll bridge's commuters were not taken further (the second is this note's dt1 world).
- **Architecture 4 at design, 2026-10-23: agency settlements as Ask B's device, replaced before the pack was frozen.** A violation account settled at 65 per cent in one payment with no invoice number, its invoices listed in the reference and applied oldest first, toll before fees: the unmatched join the hygiene battery runs surfaces the payment and a policy sentence then hands the allocation over (a filed rule adjudicating the device), so the device became the violation agency's whole-account remittance named on the oldest invoice.
- **Architecture 4 (the Marrowfield Turnpike's toll-by-mail collection, matured on each in-state plate's registration renewal) spent at Gate F on 9451b6bd, 2026-10-23.** Blind reader B landed $13.75 million: "used toll-by-mail (closed booth) invoices, not violation invoices, as the comparison group. Out-of-state: ultimate toll-weighted collection of matured cohorts issued Apr-Oct 2025 (agency window closed) = 0.600. In-state: share paid before DMV referral 0.610, DMV holds 0.378 (converting at 0.862 at renewal, measured on holds whose registration expiry has passed, right-censoring handled) ... In-state ultimate about 0.938." Lessons: a collection channel the policy states (the hold paid at renewal, 4.1 and 4.2) with its clock on file (reg_expires) is measured on sight, the law that killed task177 v3; both ask devices held, 0 of 22 (the classifier-split phantoms found only by same-lane sub-second timing against the commercial postings, and the whole-account agency remittance named on the oldest invoice), so neither sat on the reader's path; and "the in-state and out-of-state shares behind it" forked, read as the collected toll's composition (81 and 19 per cent) rather than the collection rates (94 and 60), so a share in a prompt names its numerator and denominator.
- **Rebuild 2026-10-23, fifth cell (chosen shape first): biomedical-clinical-research / dose-response-pk-pd-modeling, a phase 3's week-12 target-lesion response read lesion by lesion (scratch `b171s/proto/l1.py`, `l1b.py`, `l2.py`).** The structure looked right: the response is a threshold on the size-weighted sum of a patient's target-lesion changes, the lesions share a patient effect and vary within it, and a forward population whose sums are dominated by one large lesion averages less than a record of evenly sized metastases, so the record's patient-level rate does not transfer; the concentration (the effective number of lesions) is built from lesion rows and named nowhere, and the count and baseline-sum reflexes move the wrong way. It died on lever and on sigma, measured: over sixteen settings (median lesion ratio 0.70 to 0.90, within-patient correlation 0.10 to 0.50) the forward rate sits only +1.7 to +18.7 per cent from the record's at correlations of 0.23 to 0.50, the published range for lesion response, and reaches +22 to +29 only at a correlation of 0.10 with median shrinkage of 10 to 16 per cent; on 640 patients at the dose the lesion-level mixed model's own figure moves 0.239 to 0.278 across seeds on a truth of 0.265, about 6 per cent, because a trial's patient count cannot carry a sigma near 1 per cent; and the shared patient effect with members summed is task143's insight one step removed. The cell's other structures are named by the field (dose intensity and reductions, cumulative-dose toxicity, schedule, tolerance, the PK-PD index, hysteresis, exposure confounded by clearance) or sit in population PK, which died for task178 and task179.
- **Fifth cell, the paper half: physical-environmental-sciences / hydrology-flood-frequency, screened beside it (scratch `b171s/proto/h1.py`).** Flood frequency is one weather-driven system per site, so no forward quantity rests on enough events: on a 45-year record the mean annual count of flood-stage days carries a 15 per cent sigma, the 10-year flood about 9 per cent and the 100-year flood about 22 (16th to 84th percentile over 400 records), against the 1 per cent the holds this round had. Every structural break the cell offers is a channel its standard names (regulation and naturalised flows, mixed rain and snowmelt populations, historical floods and perception thresholds, low outliers, urbanisation, non-contributing area, permeable-catchment growth curves, rating extrapolation, compound river and surge flooding), and a hindcast of a forward scheme over the recorded flows is a filed operating rule replayed on the record. A many-unit version (culverts, crossings) reads its catchment property off a map layer, a column.
- **Fifth cell, while choosing, the grey cells on paper (each died in another number's note this round, so not drawn):** a land-retirement programme's 2017 contracts expiring together, read on the share of each owner's holding enrolled (built from a contract file and an ownership file with no shared key), holds the street-grain shape but is `composition_mix`, banned by task179 in the window, and sits in task175's own task type; lease banks rationed per solar developer read through project-company names is builder absorption in another field (task175's world) and fails the swap test; patients with one or more admissions under a therapy that halves each person's rate is a fitted nonlinearity whose lever is its own sensitivity; habit, default, inertia and reference-point choice structures are named in decision-making (task170 v4's ground); media reach, reserving, ratemaking and model diagnostics carry task174's findings.
- **Architecture 5 at the draw, 2026-10-26: exposure-response confounded by baseline clearance.** The sickest patients
  clear the antibody fastest, so low exposure and poor response travel together inside the one dose arm and only the
  randomised dose groups carry the dose's effect. Set aside before the card: it is the client library's card 3 for
  this task type, its remedy (adjust for the clearance determinants) is the careful analyst's reflex, and task179 and
  task170 screened it as the cell's own card. Drawn instead as the feedback from the outcome to the exposure after
  baseline, which that adjustment does not cure (`generator/paper/cands.json`; `guard.py nearest` 0.07 for the
  confounding driver and 0.10 for the feedback driver, both against older builds).
- **Architecture 5, the first paper world (`generator/paper/sim_er.py`).** The true dose effect an Emax on
  first-interval exposure with EC50 4 against first-interval concentrations near 30, candidates 300, 450 and 600 mg
  under a 2-point rule: on seeds 141, 1 and 2 the day-14 and week-4 members' slopes ran from minus 0.19 to 0.51 and
  filed 300, 450 or 600 mg, so the clean family itself forked the call, the true curve still rising between 300 and
  600 mg and albumin (0.045 a g/L) sitting in both clearance and prognosis. The true effect was put on its plateau
  (EC50 1 ug/mL, far under every candidate's induction-average concentration) and albumin's prognostic weight cut to
  0.02 a g/L.
- **Architecture 5, a day-14 sample or the first-interval AUC as the clean exposure (`sim_er2.py`, `sim_er3.py`,
  `sweep3.py`).** Both vary little across patients (log SD about 0.5 for the day-14 sample against about 1.0 for the
  week-4 trough on the five paper worlds), so their exposure-response slope is noisy: in `sim_er2.py`'s 40-world sweep
  the day-14 member filed 300 mg in 16 to 20 worlds and the highest dose in 16 to 21, and over `sweep3.py`'s 40 worlds
  the first-interval AUC's 300 mg gap ran from about minus 3 points (its tenth percentile) to plus 15, forking the call
  inside the standing family. The main schedule keeps only the pre-dose troughs and week 12, so the clean exposure is
  the week-4 trough.
- **Architecture 5, clearance moving from a median of day 11 or day 19 (`sim_er3.py`, `sweep3.py`).** The week-4
  trough then carried part of the response (remitter to non-remitter geometric-mean ratio 1.30 on seed 141 at day 19)
  and sat between the families: with the change at day 11 its 300 mg gap ran at a median of about 4 points (at most
  7.1) and no world of 40 held the families apart, and at day 19 only 9 of 40 did. The change was moved to a median of
  day 26 with a tight spread (`sim_er4.py`), so the week-4 trough is drawn before almost all of it.
- **Architecture 5, the change at a median of day 36 (`sweep3.py`).** The week-8 trough's 300 mg gap fell to a median
  of about 4.5 points over 40 worlds, on the rule's margin, so a week-8 reader could land 300 mg by chance. The burden
  term was raised to 38 per cent with non-responders' clearance rising 10 per cent (`sim_er4.py`), which puts the
  closest late member's gap at 11.5 points or more over 40 worlds (`fam5_sweep.py`).
- **Architecture 5, albumin as the only carrier of the clearance change (`sim_er4.py`'s first run, whose parameters
  were not kept).** Adjusting the week-12 trough for the week-12 albumin flattened it and landed 300 mg through a
  post-baseline adjustment with no insight. The change now runs mainly through an unmeasured inflammatory burden with
  albumin rising 2 g/L in remitters, and the week-12 albumin adjustment files 900 mg on four of the five paper worlds
  and 600 mg on the fifth (300 mg 8 to 14 points under 600 mg).
- **Architecture 5, a two-dose call (300 against 600 mg).** The steady-state route and the do-nothing route both filed
  600 mg; the third candidate, 900 mg, gives the default path its own answer (it escalates) and leaves 600 mg as the
  lazy answer, three distinct stops.
- **Architecture 5, a forecast remission rate as a critical component at whole percent.** The standing family's 300 mg
  forecasts spread 1.7 to 4.8 points inside one world on the five paper worlds, so a whole-percent forecast is not
  determinate (`stumping` 1.2a); the call is graded and the components come from records the data fix, set at stage 2.
- **Architecture 5, a population pharmacokinetic report with each patient's post-hoc clearance.** A time-invariant
  fit's individual exposures are a shipped record whose standard use files 900 mg (every post-hoc member on the five
  paper worlds), which reads as a certified record built to bless the wrong method; no popPK report ships, and the
  investigator's brochure gives phase 1's linearity and covariates only.

## Retired

task171 retired on 2026-10-19 under the author's rule for this round (a number that dies in its second new cell retires);
no card was ever registered. The seed's receiving-desk architecture died at the draw, and the redraw round's two cells
died on code: political-science-public-policy / election-polling-forecasting (e27c16f: the swing scale is settled by a
back-test a careful reader runs, and the realignment and tactical layers sit under the bar or fork on hard against
expected seats) and general-statistics-data-science / scaling-laws (96b18ed: every judgment beyond the three client
cards is a common exposure the sweeps either measure, so a filter and a divide lands it, or cannot pin, so the family
spreads past any rival). The lesson: in a field whose standard is a back-tested model choice, the back-test is the
textbook route and it lands.

## Rebuild (2026-10-23)

Reopened under the author's rule that no number stays retired; rebuilt from scratch in economics-econometrics / discrete-choice-limited-dependent-variable-modeling as architecture 3 (`## Draw`), the receiving-desk seed and both redraw cells left spent.

Architecture 3 was spent at Gate F at stage 4 the same day (the scored reader calibrated take-up on the launch cohort's pre-launch use by default); the coordinator left the next cell to this build, the healthcare utilization cell died on code, and architecture 4 was drawn in economics-econometrics / forecasting-forecast-evaluation: the Marrowfield Turnpike Authority's first all-electronic tolling year (`## Draw`). Stage 3 went green the same day and the build is parked at stage 4 for the readers and the judge.

Architecture 4 was spent at Gate F at stage 4 the same day (a blind reader measured the renewal-hold channel the policy states); the number is PAUSED for the main session's next cell.

The fifth rebuild cell was left to this build, shape first: biomedical-clinical-research / dose-response-pk-pd-modeling was taken to code (the lesion-level response, dead on lever and sigma) and physical-environmental-sciences / hydrology-flood-frequency screened beside it (dead on sigma and named channels), with the grey cells read on paper (`## Tried and rejected`, the three fifth-cell lines). No card registered past v4, which stays the card's identity marked spent; PAUSED at stage 1 for the main session's next cell. The number is never retired.

Architecture 5 came from outside this number on 2026-10-26: the dovikizumab induction dose, drawn in the task141 rework,
which task141 did not take because its own session had already re-rooted it to architecture 2. The author parked it
here. Its card waits on `ban.strategy` (`## Draw`, Guard); no card is registered past v4 until then.
