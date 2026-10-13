# task122 design note

Architecture v3 on the card (the second architecture built for this slot; v1 was a draft redrawn before
registration), re-rooted 2026-10-13 under the 10/10 rules. v2, a Dutch resale platform choosing which ranking
policy takes its home carousel's test slot, was retired after a Gate G send-back and is FAILED_TO_STUMP in the
author's backlog: its decisive step was a field read under a filed charter and its estimator was pinned by an
archive of certified tests. The slot is redrawn into a new domain, world, decision and quantity. v2's record is
kept at the end of this note; its pack, goldens and reports are removed from the tree and kept in history.

## Draw

| Axis | Value |
|---|---|
| Domain / task type | Biomedical & Clinical Research / longitudinal-outcomes-repeated-measures (serves Experiment & Causal in the client taxonomy; the domain has never been built, in any objective) |
| Objective | Experiment & Causal Analysis: the call is a causal claim read from a randomised trial, how far each dose of the drug moves eGFR against placebo after 36 months' treatment |
| Niche | a Copenhagen-area clinical-stage biotech chooses which of four once-daily doses of its oral aldosterone synthase inhibitor, VMK-4410, goes into the phase 3 kidney trial, from a 52-week multinational phase 2b in albuminuric chronic kidney disease whose protocol held background diuretics, RAS blockers and SGLT2 inhibitors unchanged for the first 12 weeks |
| Shape | 11 before and after with a control: each dose's eGFR difference from placebo after 36 months' treatment, plus the call, the runner-up and the gap, a chart of each dose's difference by month and the asks |
| Decision type / unit | pick one of four doses (named option); the graded figures are mL/min/1.73 m2 of eGFR against placebo |
| Gap / pattern / generators | time (what the 52-week trial measured against the 36 months the decision is scored on); no A to E pattern; G4 decisive (the one-off recovery after background diuretics are eased, at the turn from the acute phase to the chronic phase, attributed to the chronic slope), G13 (the 36-month horizon multiplies a slope read over 40 weeks), G16 (where the chronic phase is fitted from) |
| Gate G mechanism | method_or_model_selection: every laboratory value, visit and protocol rule is read correctly on the wrong route; the decision turns on the window the chronic eGFR slope is fitted over |
| Stump strategy | decomposition_attribution: the eGFR trajectory splits into the acute haemodynamic fall, a one-off recovery once diuretics are eased, and the chronic slope, and only the last is carried for three years |
| Decisive rule filed / decoys | the estimand is filed (the phase 3 synopsis: eGFR at month 36 against placebo, every randomised patient, as if each had stayed on the assigned dose); no official decoy (no filed slope method, knot or acute window anywhere in the pack), no validated decoy, no calibration corpus; the phase 2b's own results report is not shipped |
| Calibration form | none |
| Context artifact | other (the phase 3 synopsis that files the estimand, beside the phase 2b protocol) |
| Stakeholder | the head of clinical development, who recommends the dose to the chief medical officer, who signs it for the end-of-phase-2 meeting package (the prompt names no one) |
| Forum / forcing event / org family | line_manager_or_team / statutory_or_regulatory_filing (the end-of-phase-2 meeting package) / other (a clinical-stage biotech, not yet a manufacturer) |
| World | Varnmark Therapeutics (invented), Copenhagen area, DKK; phase 2b VMK-4410-202 at sites in Denmark, Sweden, Germany, Poland, Spain and the United Kingdom; personas drawn da_DK seed 122: Benedicte Laursen (head of clinical development), Nicolaj Lassen (biostatistics), Kirsten Eriksen (clinical pharmacology), Lene Dam (medical monitor) |
| Deliverables | `VMK-4410_phase3_dose_recommendation.pdf` (the call, each dose's eGFR difference from placebo after 36 months' treatment, a chart of each dose's difference by month); `VMK-4410_phase2b_tables.xlsx` (the asks) |
| Guard | WARN only (answered below); registered 2026-10-13 |

**Data-native sentence.** The protocol held background diuretics steady for the first twelve weeks, so the
patients whose eGFR fell furthest on the higher doses, those already on a loop diuretic when the drug's
natriuresis added to it, had their diuretic eased only from week 12 and recovered part of the fall over the
following weeks; the eGFR record therefore turns from an acute fall to its chronic slope only around week 24, and
a chronic slope started at the field's usual three months carries that one-off recovery forward for three years.

**Mechanisms on file (Experiment & Causal), one line on the insight each spends.**
- task6: a non-randomised pilot read against each arm's own baseline once a hidden record stream is recovered.
- task12: an arm-correlated population captured in a second party's system, recovered by anti-join.
- task15: outcome rows missing for one arm after a client change, recovered from an independent log.
- task43: a pooled effect carried onto a cohort whose moderator mix is reversed, the moderator behind a join.
- task44: a pooled gain that mixes opposite effects split by a moderator in no column.
- task69: a capped set whose members' contributions overlap; an assignment rate that moved across periods.
- task83: an effect conditioned on each unit's own prior treatment history; allocation by single-peaked effect.
- task122 v1 and v2: a library-fill clause; outcomes the log records only before a session closes.
- task131: a randomised tariff's half-hourly effect at design-day heat, read on the maximum of the whole curve.
- None separates a transient from a long-run rate inside one arm's trajectory, and none is in nephrology.

**Sources, one line each.**
- The client's two-layer standard: the field's own method decides; here it is nephrology's acute-plus-chronic
  eGFR slope analysis, worked on where this trial's acute phase really ends, never a stated score or a window rule.
- The client's library (`biomedical-clinical-research/longitudinal-outcomes-repeated-measures`: MMRM over
  completers, baseline-adjusted change): both are lower rungs here; the pattern is our own,
  `own:egfr-chronic-slope-after-diuretic-recovery`.
- The client's measured drivers, held group: the decisive step sits upstream of every graded figure (each dose's
  36-month difference is built on the slope window) and the shortcut is the field's own convention.
- task131 (an effect read at design conditions): there the conditioning was on the weather the decision faces;
  here nothing is conditioned, the trajectory itself has three phases and only one is carried.
- task123 v2 (a total recorded over each unit's own interval, split onto calendar periods; same gap, pattern and
  Gate G): differentiated on the card; no interval allocation here.
- Field practice: GFR slope as a surrogate end point (acute effect over the first months, chronic slope after),
  the haemodynamic eGFR fall on starting a RAS blocker, SGLT2 inhibitor or aldosterone pathway drug, and the
  stable-background period phase 2 kidney protocols write in; the build carries the practice, not any trial's
  figures.

**WARNs answered.**
- repeat.gate_g and overuse.gate_g (method_or_model_selection; task449, task501 in the guard's order): the honest
  name for choosing the window a slope is fitted over; task449 sets a dial and task501 selects an estimator for a
  different quantity, and forecasting or decomposition_attribution would misname a model choice the trial's own
  record forces.
- repeat.decision (pick_one_of_n, task501): a phase 3 takes one dose, so the decision is a pick.
- repeat.question_form (which, task501): a pick asks which.
- The guard orders same-date cards by task number, so its bans read task448, task449 and task501; the card also
  clears the builds registered last on 2026-10-13 (task452, task453, task454) on every banned axis: shape 11
  against 01, 10 and 07; forum against committee_or_panel, minister_or_cabinet and customer_or_counterparty;
  forcing event against budget_or_appropriation, period_close and launch_or_rollout; strategy against other,
  population_selection and composition_mix; decisive pattern G4 against G14, G16 and C.

**Arithmetic on the arm means** (`checks.design_routes`, carried in `generator/figures.json` as
`note.design_coefficients`; visits at weeks 0, 2, 4, 8, 12, 16, 20, 24, 32, 40 and 52; diuretics eased at the
week-12, 16 and 20 visits in 45, 35 and 20 per cent of the patients eased; the fall develops with a time constant of
1.2 weeks and the recovery after easing with 1.5 weeks). Each route's 36-month value is linear in a dose's initial
fall P, the part that comes back after easing R and its chronic benefit C (mL/min/1.73 m2 a year): golden -P + R + 3C;
the two-slope model from week 12, -P + 3.36R + 3C (from week 16, 2.37R; week 20, 1.55R; week 24, 1.05R; week 32, 1.00R);
one slope through every visit, -2.02P + 3.97R + 3C; the week-52 difference, -P + R + C. The draw's values (P, R, C):
5 mg 0.9, 0, 0.30; 10 mg 1.0, 0, 0.667; 20 mg 3.85, 0.15, 2.20; 40 mg 6.9, 1.4, 2.50. The generator calibrates each
arm's level and chronic slope so the measured week-52 difference and the week-24 route land on the draw's targets; the
shipped values are in the Ladder. Month-36 differences by route on the draw's values:

| Route | 5 mg | 10 mg | 20 mg | 40 mg | Files |
|---|---|---|---|---|---|
| golden: the settled level plus the chronic benefit over three years | 0.0 | 1.0 | 2.9 | 2.0 | 20 mg |
| chronic phase from week 24 (week 32) | 0.0 | 1.0 | 2.9 (2.9) | 2.1 (2.0) | 20 mg |
| chronic phase from week 20 | 0.0 | 1.0 | 3.0 | 2.8 | 20 mg, 40 mg's figure a bin out |
| chronic phase from week 16 | 0.0 | 1.0 | 3.1 | 3.9 | 40 mg |
| chronic phase from week 12, the field's month 3 | 0.0 | 1.0 | 3.2 | 5.3 | 40 mg |
| chronic phase from week 4 | 0.0 | 1.0 | 3.2 | 5.8 | 40 mg |
| one slope through every visit | -0.9 | 0.0 | -0.6 | -0.9 | 10 mg |
| the week-52 difference (no projection) | -0.6 | -0.3 | -1.5 | -3.0 | 10 mg |

On the shipped pack the month-3 route reads 40 mg's chronic benefit over placebo as 3.7 mL/min/1.73 m2 a year against
2.5 from week 24; placebo declines about 4 a year, so on the convention 40 mg reads as nearly flat, a strong but
plausible claim for a kidney drug.

**Shape arithmetic (shape 11).** Each dose's eGFR difference from placebo after 36 months' treatment (4), the
call, the runner-up and the gap (3), a chart of each dose's difference by month with four named parts (4) and the
two files (2): 13 before the ask layer; the asks add 5 arms x 4 measures = 20, for 33 in all. The decisive
construction moves 20 and 40 mg's figures and the call; the 12- and 24-month values are drawn on the chart and not
graded, since a chronic benefit that is not a whole number a year cannot keep every year's value mid-bin.

## Default path

1. Read the question: which dose, judged by how much higher eGFR would be than on placebo after 36 months'
   treatment, which the phase 3 synopsis files as the difference at month 36 for every randomised patient as if
   each had stayed on the assigned dose.
2. Take the central laboratory's eGFR (CKD-EPI 2021, reported beside each serum creatinine) at the scheduled
   visits from `lb.csv`, each patient's change from the baseline the protocol defines (the mean of the screening
   and day 1 values), and the mean change by arm and visit.
3. Fit nephrology's standard two-slope model on every randomised patient: an acute effect from baseline to month
   3 (week 12) and a chronic slope from week 12 to week 52, by arm, against placebo.
4. Carry each dose's chronic slope to month 36 from its level at week 12 and take the difference from placebo.
5. File the dose with the largest difference.

Ends on: 40 mg, about 5 mL/min/1.73 m2 above placebo at month 36 (20 mg 3, 10 mg 1, 5 mg 1; on the shipped
pack's arm means 4.81, 3.11, 1.03 and 0.65).

Golden: 20 mg, 3 mL/min/1.73 m2 above placebo at month 36, then 40 mg at 2, 10 mg at 1 and 5 mg at 0 (3.04, 2.04,
1.05 and -0.01 on the shipped pack), with the chronic slope taken from week 24, after the recovery, from the level each
arm settled at.

## Stump sentence

A competent solver fits each dose's eGFR with the field's two-slope model, an acute effect to month 3 and a
chronic slope after it, carries the chronic slope to month 36 and files 40 mg at about 5 mL/min/1.73 m2 above
placebo (the `Ends on:` figure); the step that lands it there is starting the chronic slope at month 3, when the
patients whose eGFR fell most on 20 and 40 mg had their loop diuretics eased only from week 12, at the week-12,
16 and 20 visits, and recovered part of the fall over the following weeks, so a slope from month 3 carries that
one-off recovery forward for three years; taken from week 24, after the recovery, the slope leaves 20 mg furthest
above placebo at month 36 (3) and 40 mg at 2.

## Three rules

Task type: longitudinal-outcomes-repeated-measures in Biomedical & Clinical Research, a task type that serves
Experiment & Causal Analysis in the client taxonomy: repeated eGFR measurements per patient in a randomised trial,
read as each dose's effect against placebo over time.

Domain test: the deciding quantity is each dose's eGFR difference from placebo after 36 months' treatment, and
nephrology estimates it by GFR slope analysis, an acute effect over the first months and a chronic slope after it,
the chronic slope projected; this trial's protocol and its patients' diuretics decide where the chronic phase
starts.

Swap: "Which dose leaves eGFR furthest above placebo after 36 months" with a school's nouns becomes "which tutoring
intensity leaves test scores furthest above the control group after three years"; there is no filtration fall that
a diuretic adds to, no background diuretic held fixed for twelve weeks and then eased, and no recovery of a
volume-related fall, so the step that decides has nothing to act on and the task stops making sense.

Layer 1: an SDTM-style extract from two central laboratory hubs and the sites' local laboratories: unscheduled
potassium rechecks, a repeat sample after a haemolysed one filed under the visit it replaces, potassium not reported
on a haemolysed sample (the condition on the potassium result only), rechecks requested as a renal panel or a full
panel, creatinine in umol/L at one hub and mg/dL at the other, potassium in mmol/L and mEq/L, glucose in mmol/L and
mg/dL, urine albumin-to-creatinine ratios in mg/mmol and mg/g, local laboratories reporting eGFR by CKD-EPI 2009 or
not at all; visits before week 24 taken outside their windows under their scheduled names; drug collected at the site
when a dispensing visit was missed; dosing records running from one dispensing visit to the next; a disposition form
not reopened when a patient restarted; adverse events whose change of severity opens a new record; concomitant
medications in each country's spelling, with free-text doses and changes recorded as new rows; screening failures in
the demographics, visits, laboratory and vital-sign tables. This is the mess a CRO's data management, two central
laboratory hubs and fifty sites produce; none of it is placed to be caught and none of it is on the decisive step.

Layer 2: estimation_fit: fitting the chronic eGFR slope over the stretch where the trajectory is chronic, after
the one-off recovery that easing background diuretics from week 12 produced, then carrying it to month 36 from the
level each arm settled at.

Decisive step: in the field's words, where the acute phase ends: the acute effect of VMK-4410 includes a
volume-related fall that partly recovers once diuretics are eased after week 12, so the chronic slope starts
around week 24, not at the conventional month 3.

Not semantics: every eGFR, creatinine, visit, unit, concomitant medication record and synopsis definition can be
read correctly and the month-3 two-slope route still files 40 mg; the difference between 40 and 20 mg is a choice
of model window, not the meaning of any field.

Not rule application: no filed rule, procedure or formula says where the chronic phase starts or how the slope is
fitted; the synopsis files the estimand only, and the protocol's twelve-week stable-background rule is a fact of
the trial's conduct that no sentence connects to the eGFR record.

Analyst test: with every laboratory value, visit and protocol rule read correctly, a strong analyst fits the
standard acute-plus-chronic eGFR model with the chronic phase from month 3, projects it to month 36 and files 40
mg (the `Ends on:` answer); the week-52 change the phase 2b protocol names as a secondary end point, and one
slope through every visit, file 10 mg instead.

Estimand: the phase 3 synopsis (`VMK-4410-301_synopsis.pdf`) files it: the difference between each dose and
placebo in the change in eGFR (CKD-EPI 2021, central laboratory) from baseline to month 36, in every randomised
patient, as if each had stayed on the assigned dose; the prompt asks which dose and for each dose's difference
after 12, 24 and 36 months' treatment.

No decoy: nothing is planted to be caught; no document states a slope method, a knot, an acute window or a
projected figure, the phase 2b results report is not shipped, and no file ranks the doses on the 36-month
difference; the protocol's primary end point (the week-52 change) is the trial's own question, stated as such.

No certified replay: no certified, published or prior figure has to be reproduced to recover the method; the
method comes from the trial's own record (the shape of each arm's eGFR after week 12 and the diuretic changes
behind it).

Lesson: a model learns that the chronic phase of an eGFR response begins where the trajectory turns linear, which
a trial's conduct (here the background changes its protocol allowed only after twelve weeks) can push well past
the conventional three months, and that a slope fitted over a transient is multiplied by every year it is carried;
no build on file is in nephrology or separates a transient from a long-run rate inside one arm's trajectory.

## Readability screen

Rungs in ladder order; the six tests of `stumping` 2.1 per rung, verdict last.

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 the week-52 change against placebo, unprojected (files 10 mg) | the protocol lists the week-52 change as a secondary end point | the visit column | the trial's own end point is a default | none | none | one difference per arm | readable |
| 0b one slope through every on-treatment visit, the total slope (files 10 mg) | the synopsis's change to month 36 invites a slope | none | a mixed model of every visit is a reflex | none | none | a regression line | readable |
| 1 the field's two-slope model, chronic phase from month 3 (files 40 mg) | none in the pack; field practice puts the acute phase in the first three months | none | the convention is the reflex | none | none | a regression with a knot | readable |
| 2 chronic phase from week 16, after the visible turn at week 12 (files 40 mg) | none | none | moving the knot to the first change seen is a reflex | none | none | a regression with a knot | readable |
| 3 (decisive) chronic phase from week 24, after the recovery that easing diuretics from week 12 produced, carried from the level each arm settled at (files 20 mg) | no sentence says where the chronic phase starts or links any background change to eGFR; the protocol's concomitant-medication clause (doses unchanged to week 12) is one clause among the conduct rules and names no outcome | no column marks the recovery or the eased patients; diuretic changes sit in `cm.csv`, which the eGFR path never opens; the arm curves show a rise after week 12 that reads as the drug's benefit | the convention (month 3) files 40 mg; knotting at the first visible change (week 16) files 40 mg; one slope through everything files 10 mg | no control, corpus or published figure scores the doses | keys, units, duplicates, joins and fan-out see nothing | the window of a fitted slope over a non-linear trajectory, multiplied by three years | silent |

The two reflexes land on different wrong doses (10 mg, 40 mg) and the decisive move reverses the step every
correction above rung 0 takes (towards 40 mg): the held signature.

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | eGFR | the central laboratory's CKD-EPI 2021 eGFR from serum creatinine, reported beside each creatinine | recomputed from the reported creatinine; local-laboratory values added | same call and same figures (asserted: the recomputation is within 1 of the report on every central sample; no local eGFR sits at a scheduled visit) | the synopsis's eGFR definition (central laboratory, CKD-EPI 2021) |
| SF2 | baseline | the mean of the screening and day-1 central values | day 1 only | same call and same figures (asserted) | the protocol's and the synopsis's baseline definition |
| SF3 | how much higher eGFR would be than on placebo | the difference between the dose's and placebo's mean change from baseline | the difference in mean eGFR levels at month 36 | same call and same figures (asserted: every arm's baseline mean is within 0.1 of placebo's; levels read -0.02, 1.07, 3.15, 2.14) | converges; the synopsis files the change from baseline |
| SF4 | after 36 months' treatment | on treatment at the month-36 visit, 156 weeks after randomisation | off treatment, four weeks after the last dose (the phase 2b's week-56 pattern) | 40 mg (the early fall reverses off treatment: 6.5 and 7.1 on 20 and 40 mg, asserted) | the synopsis ("the month-36 visit takes place while patients are taking study drug"); C4 |
| SF5 | every randomised patient, as if each had stayed on the assigned dose | values from samples after a patient's last dose set aside for the patients who stopped study drug for good, read from the dosing record | values after stopping kept (treatment policy); stopping read from the disposition form | treatment policy: same call, 40 mg's figure a bin up (2.70) and 20 mg's at 3.49 (asserted); the disposition form: same call and same figures (asserted) | the synopsis's intercurrent-event strategy (values after a permanent stop set aside); C4 for treatment policy |
| SF6 | each dose | 5, 10, 20 and 40 mg once daily as randomised | as treated | same call (asserted: every patient took the randomised dose on every dosing row) | the synopsis's population (as randomised) |
| SF7 | the visits a slope is fitted on | scheduled on-treatment central visits by nominal week, the first sample of a visit | actual study days; unscheduled central values added | same figures (asserted) | the SAP (values analysed under the scheduled visit; the first sample of a visit) |
| SF8 | the week-56 follow-up visit | off treatment, outside the on-treatment estimand | fitted with the on-treatment visits | 40 mg (asserted) | the synopsis's on-treatment estimand and the protocol (week 56 is four weeks after the last dose); C4 |
| SF9 | the phase 3 the dose goes into | the phase 2b's population, dose, schedule and background rule carried forward | a phase 3 without the 12-week background rule | same call (the settled level and the chronic slope are the same; the recovery comes earlier) | the synopsis's population and background-therapy sections, which repeat the phase 2b's (asserted present) |
| SF10 | 36 months | 156 weeks of treatment from randomisation | 3 x 365.25 days | same figures (asserted) | the synopsis's visit schedule (month 36 = week 156) |
| SF11 | rounding | each difference computed unrounded, rounded once to a whole mL/min/1.73 m2 | arm means rounded to one decimal before the differences; to whole numbers first | one decimal: same call and same figures (asserted); whole numbers first scrambles the figures | the prompt's closing sentence rounds the differences |
| SF12 | placebo | the phase 2b's placebo arm, on the same background therapy | none | same call | the protocol's design |
| SF13 | the dose to take into the phase 3 | the dose with the largest difference from placebo at month 36 | the lowest dose within a margin of the best; a safety screen first | same call (20 mg is the largest and no safety rule in the pack bars it) | the prompt's question; the synopsis's dose-selection sentence names this trial's primary end point, the change in eGFR at month 36 (asserted present) |

## Ladder

Measured on the shipped pack (`generator/checks.py` asserts every row; `generator/figures.json` carries the values
under `note.rungs`, `note.margins` and `note.corridor`). Figures are each dose's month-36 difference from placebo in
mL/min/1.73 m2.

| Rung | Construction | 5 mg | 10 mg | 20 mg | 40 mg | Winner | Margin |
|---|---|---|---|---|---|---|---|
| 0 default variant | the week-52 difference, no projection | -0.60 | -0.34 | -1.39 | -2.99 | 10 mg | 0.26 over 5 mg |
| 0b | one slope through every on-treatment visit, carried to month 36 | -0.15 | 0.18 | -0.38 | -1.02 | 10 mg | 0.33 over 5 mg |
| 1 default path | two-slope, chronic phase from week 12 (month 3) | 0.65 | 1.03 | 3.11 | 4.81 | 40 mg | 1.70 over 20 mg |
| 2 sophisticated | two-slope, chronic phase from week 16, after the visible turn | 0.39 | 1.11 | 3.05 | 3.56 | 40 mg | 0.51 over 20 mg |
| 3 decisive | chronic phase from week 24, after the recovery, from each arm's settled level | -0.01 | 1.05 | 3.04 | 2.04 | 20 mg | 0.99 over 40 mg |

- **Position.** 20 mg is third of four on rung 0 (only 40 mg's larger fall is behind it), second on 0b, second on rungs
  1 and 2, and first only at the decisive rung. Four candidates leave no fifth place; the margins are in
  mL/min/1.73 m2 because the week-52 values are negative.
- **Dominance.** Every correction above the week-52 view moves the call to 40 mg (4.81, then 3.56); only the decisive
  move reverses it, by carrying the recovery as a level rather than a slope: 40 mg's figure falls by 2.8 from rung 1
  (asserted at 2.5 or more), 20 mg's by 0.1.
- **The knot at week 20,** at the last easing visit: 20 mg stays first (3.24 against 2.83) and 40 mg's figure is a bin
  out; the 40 mg difference still rises 0.51 from week 20 to week 24, more than one and a half times its chronic rate
  over four weeks (asserted). A fifth of the easing happens at that visit, so the knot sits inside the recovery.
- **Corridor (C3).** From week 24 every estimator lands the golden figures (asserted within 0.4 of the whole number):
  the knot at week 32 (0.02, 1.10, 2.98, 1.89), the mixed model with a random intercept and slope per patient (-0.07,
  1.24, 3.02, 2.03), each patient's own line averaged (-0.20, 1.14, 3.02, 2.06), the pooled patient-level line on
  actual study days (-0.04, 1.07, 3.08, 2.07) and the week-52 difference plus two years of the chronic slope (0.02,
  1.08, 3.08, 2.00).
- **Worth on the graded quantity.** From rung 1 the decisive move shifts 40 mg by 2.8 and carries the call; from rung 2
  it shifts 40 mg by 1.5. Rungs 0 and 0b file 10 mg with every drug figure one to four whole numbers off.
- **Grid.** Two binary moves (project at all; start the chronic phase after the recovery) and the knot's position:
  no projection, 10 mg; one slope through every visit, 10 mg; knots at weeks 4, 12 and 16, 40 mg; the knot at week
  20, 20 mg with 40 mg's figure a bin out; knots at weeks 24 and 32 and the within-patient estimators, the golden.
  Lower rungs at the golden cell: levels for changes, the disposition form for the dosing record, one-decimal arm
  means, actual days and unscheduled values leave every figure in its bin (asserted); the week-56 visit fitted in or
  an off-treatment reading moves the call to 40 mg (SF4, SF8); treatment policy keeps the call with 40 mg a bin up
  (SF5).
- **Flip condition.** 40 mg overtakes 20 mg at month 36 only if its chronic benefit over placebo exceeded 20 mg's by
  more than 0.7 mL/min/1.73 m2 a year (against 0.3 measured: 2.5 and 2.2 a year).
- **Figures mid-bin.** 3.04, 2.04, 1.05 and -0.01 against whole-number bins, each 0.45 or more from an edge.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every randomised patient, by randomised arm, values after a permanent stop set aside | filed (the synopsis's estimand); SF5, SF6 asserted |
| 2 | Unit of account | a patient's eGFR at a visit; the arm mean of changes from baseline | filed (the synopsis); one central eGFR per patient-visit after duplicates collapse (asserted) |
| 3 | Attribution window | on-treatment visits to week 52; the week-56 follow-up outside | filed; SF8 (C4) |
| 4 | As-of dating | the phase 2b database as locked, every visit final | C1: the extract's last collection date precedes the lock date; no visit after week 56 |
| 5 | Version basis | the central laboratory's final results | C1: no corrected or cancelled eGFR result on the main path (asserted) |
| 6 | Denominator | the arm's patients with a value at each visit | C1: the mixed model, each patient's own line and the pooled patient-level line land the golden figures (asserted) |
| 7 | Weighting | arm means of patients' changes, patients equal within a visit | C1 (asserted across the mixed model, arm means and per-patient lines; the dropout streams were drawn so the incomplete patients do not pull the late visit means) |
| 8 | Window length | where the chronic phase starts | the data's structure: the easing runs from the week-12 visit to the week-20 visit and the recovery to about week 24; knots at weeks 24 and 32 and the within-patient estimators give the golden figures (C3 corridor, asserted); knots at weeks 4, 12 and 16 carry the recovery and file 40 mg; the knot at week 20 keeps 20 mg with 40 mg's figure a bin out, the 40 mg difference still rising from week 20 to 24 (asserted) |
| 9 | Boundary inclusivity | visit windows | C1: from week 24 every visit is inside its window; visits before week 24 taken outside their windows, kept or dropped, leave every figure in its bin (asserted) |
| 10 | Rounding path | once, at the end | filed in the prompt; SF11 asserted |
| 11 | Tie-break | none | C1: the four figures are distinct whole numbers |
| 12 | Maturity and censoring | every patient's 52 weeks complete at the lock | C1 |
| 13 | Order of operations | changes from baseline, then arm means, then the projection | C1: projecting each patient and averaging lands in the same bins (asserted) |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | repeat central samples at a visit (the repeat after a haemolysed sample, filed under its visit) | filed: the SAP's first sample of a visit; averaging the repeats, or dropping the haemolysed sample for its repeat, leaves every figure in its bin (asserted) |
| 16 | Identity normalisation | subject numbers across the laboratory and EDC extracts | C1: the laboratory's subject numbers equal the EDC's for every randomised patient |
| 17 | Netting against gross | none on the main call | C1 |
| 18 | Dimensional units | eGFR in mL/min/1.73 m2; creatinine in umol/L and mg/dL by laboratory | C1 on the main path (eGFR is reported in one unit); creatinine units matter only to a solver recomputing eGFR (SF1) |
| 19 | Code and status semantics | central against local laboratory, scheduled against unscheduled | dictionary semantics; SF1, SF7 |
| 20 | Integerisation | none | C1 |
| 21 | Clause scope | the 12-week background rule covers diuretics, RAS blockers and SGLT2 inhibitors in both studies | filed (the protocol and the synopsis); SF9 |
| 22 | Forward window contents | months 13 to 36 of a phase 3 not yet run | the chronic slope from the phase 2b's weeks 24 to 52 carried forward under the synopsis's identical population and conduct; the estimand is the phase 3's own |

## Literal reader

Executed word for word (the prompt; the synopsis's estimand, eGFR definition, intercurrent-event strategy and
on-treatment month-36 visit; the protocol's design, visit schedule, windows, baseline and conduct sections; the SAP's
visit conventions): each dose's figure is the difference between its mean change in central CKD-EPI 2021 eGFR from
baseline and placebo's at month 36 on treatment, every randomised patient counted as randomised and values after a
permanent stop set aside. The phase 2b records 52 weeks; the literal estimand at week 156 needs a projection, and the
field's projection carries each arm's chronic slope from the level the arm has settled at. The record turns linear
only after week 24 in the 20 and 40 mg arms (the easing visits run from week 12 to week 20 and the recovery follows
them), so the chronic slope from week 24 or 32, by arm means, each patient's own line or a mixed model, returns 20 mg
at 3, 40 mg at 2, 10 mg at 1 and 5 mg at 0; a slope started at month 3 or week 16 is an easier method on the same
literal estimand, never another reading of a filed sentence. The level reading of the prompt's "how much higher eGFR
would be" converges on the same figures (SF3).

## Oracles

- The protocol's planned sample size and the randomisation counts tie under every basis.
- The central laboratory's reported eGFR and its recomputation from creatinine tie within 1 under every basis (SF1).
- No phase 2b results report, published figure, investigator brochure table or corpus ships; nothing states a
  dose's eGFR effect, slope or projection, and no document names a slope, knot or phase window (asserted on the
  protocol, the SAP and the synopsis).
- `vs.csv` (blood pressure, pulse and weight) and `pc.csv` (trough concentrations) are distractors; neither ranks the
  doses on eGFR nor reproduces a figure, and deleting either leaves the golden and every ask unchanged (asserted).
- The asks' tables (potassium, adverse events, exposure, discontinuation) never touch eGFR.

None ties only under the golden.

Leak sweep (`leak.py --asof 2026-10-12`, REVIEW, no LEAK), one line per REVIEW:
- Sweep 3, the protocol and the synopsis carry words of the call (VMK-4410, phase 3, months, treatment, eGFR,
  placebo): the study's own nouns; neither names a dose as the choice or states a figure.
- Sweep 4, the protocol (chronic, change, window, protocol, diuretics, record), the synopsis (chronic, change, window,
  diuretics, clinical, laboratory) and the SAP (change, protocol, laboratory, patient, repeat, second): "chronic" is
  the disease's name, "window" the visit windows, "diuretics" the twelve-week background-therapy clause both studies
  carry; no document names a slope, knot or phase (asserted in `checks.py`).

Duplicate guard: `guard.py heart` WARN (question form "which" against task501); `guard.py surface` promotes task123
on the card axes it shares (time gap, G4, method_or_model_selection), the overlap the card's differentiation line
answers at registration; task123 is retired and failed to stump, and the drivers sit at 0.06.

## Ask sheet

Two asks, 20 figures, in `VMK-4410_phase2b_tables.xlsx`. Each is a component of the dose-selection case the eGFR
call does not turn on (H18: a safety or exposure measure every candidate dose carries), on rows the call never
reads (potassium and adverse events, dosing and disposition).

**Ask A: hyperkalaemia by arm** (10 figures: for placebo and each dose, how many patients had a serum potassium above
5.5 mmol/L on treatment, and how many hyperkalaemia adverse events began on treatment).
- Home: the safety component every dose of an aldosterone synthase inhibitor carries; the call does not turn on it.
- Use: the dose decision's safety table, the first thing the chief medical officer reads after the efficacy figure.
- Primary device, patients (D5, a silently partial extract): potassium measured at local laboratories (an
  unscheduled repeat after a raised central value) sits in the same extract beside the central results, as rows the
  site's own laboratory reported (named in `LBNAM`, no other marker) that also carry creatinine, sodium and glucose,
  most of them normal; the main call's estimand is central only, and a solver who carries that filter over misses the
  patients whose only high potassium was measured locally (2, 2, 2, 5 and 8 by arm, placebo included).
- Primary device, events (D6, a ledger at another grain than its name): the EDC opens a new adverse-event row when an
  event's severity changes and links the rows of one event by a group number (`AEGRPID`, filled on every event, one
  row or several); counting rows counts an event whose severity changed twice or more (1, 1, 1, 2 and 16 extra
  records by arm).
- Hazards: the two preferred terms the SAP's adverse events of special interest list for hyperkalaemia
  (Hyperkalaemia, Blood potassium increased), the SAP's on-treatment period (first dose to last dose, the day-1 sample
  a baseline value) beside its treatment-emergent window, partial onset dates imputed by the SAP's rule, potassium in
  mEq/L at the Spanish sites' local laboratories (equal to mmol/L), and post-treatment values at the week-56 visit.
- Path: `lb.csv`, `ae.csv`, `ex.csv`, `dm.csv`, the SAP (5 files; USUBJID, LBTESTCD, LBSPEC, LBSTRESN, LBSTRESU,
  LBDTC, LBNAM, AEDECOD, AESTDTC, AEGRPID, AESEV, EXSTDTC, EXENDTC, ARM).
- Stops: central only (patients short in every arm); rows counted (events over in every arm); both preferred terms
  missed (events and patients short); the treatment-emergent window ignored (screening events counted); the golden.
- Realism: EDC systems record a change in an event's severity as a new record linked to the first; local potassium
  checks after a dose change are entered on the local-laboratory form of the same extract.

**Ask B: exposure and discontinuation by arm** (10 figures: for placebo and each dose, how many patients stopped study
drug for good before their week-52 visit, and the arm's total years on study drug before that visit, to one decimal).
- Home: the tolerability and exposure components every dose carries; the call does not turn on them.
- Use: how much drug each dose's evidence rests on, and how many patients a dose lost.
- Primary device, stopping (D2, the record is the latest accepted, not the latest delivered): a site records
  "STUDY DRUG DISCONTINUED" in the disposition form when a patient stops, and a few patients restart after a
  temporary stop the site first entered as permanent; the disposition row stays and the dosing record shows tablets
  taken after its date (2, 2, 2, 2 and 1 by arm). Counting disposition rows overstates; only the dosing record says
  who stopped for good.
- Primary device, years (D6 and D9, an interval's quantity on every line it covers): each dosing row runs from one
  dispensing visit to the next with both dates inclusive, so consecutive rows share their boundary day; summing row
  lengths counts each dispensing day twice (every arm, about 1.6 patient-years an arm). Interruptions appear as gaps
  between rows.
- Hazards: the "before their week-52 visit" boundary (the visit day itself excluded); drug collected at the site
  when a dispensing visit was missed (an unscheduled dispensing row); patients who left the study before week 52.
- Path: `ex.csv`, `ds.csv`, `sv.csv` (visit dates), `dm.csv`, the SAP's exposure definition (5 files; USUBJID,
  EXSTDTC, EXENDTC, EXDOSE, DSSCAT, DSDECOD, DSSTDTC, VISIT, SVSTDTC, ARM).
- Stops: disposition rows counted (stopping over); row lengths summed (years over); the visit day included (years
  over by a day a patient); the golden.
- Realism: EDC exposure logs record each dispensing interval visit to visit; disposition forms are not reopened when
  a patient restarts.

**Main population zero-counts (asserted by count).** On the main call's rows (central eGFR at the scheduled visits,
screening to week 52): local-laboratory eGFR rows 0; eGFR results not done, cancelled or corrected 0. Split adverse-event
rows, restarts after a disposition entry and shared-boundary dosing rows are not read by the main call. The patients
who restarted after a disposition entry keep every on-treatment value; reading stopping from the disposition form
instead leaves every figure in its bin (SF5, asserted).

**Device mass on the shipped pack (golden against the device's natural read, placebo, 5, 10, 20, 40 mg).**

| Device | Golden | Natural read | Arms moved |
|---|---|---|---|
| A patients: local potassium (D5) | 2, 4, 10, 29, 68 | central only 0, 2, 8, 24, 60 | all five |
| A events: a new record per change of severity (D6) | 1, 2, 8, 28, 80 | records 2, 3, 9, 30, 96 | all five |
| B stopping: the disposition form not reopened (D2) | 5, 6, 7, 9, 10 | form 7, 8, 9, 11, 11 | all five |
| B years: bottle periods sharing their boundary day (D6, D9) | 147.1, 148.4, 145.7, 146.1, 144.7 | summed periods 148.7, 150.0, 147.3, 147.7, 146.3 | all five |

**Hazard table.**

| Hazard | Asks moved | Per-ask effect on the shipped pack |
|---|---|---|
| the AESI preferred terms | A events | Hyperkalaemia alone: 0, 1, 2, 19, 54 |
| the on-treatment window | A events | three pre-treatment events (placebo, 20 mg, 40 mg) counted if the window is dropped; no event begins in the 30 days after a last dose, so 'on treatment' and treatment-emergent agree (asserted) |
| the day-1 and week-56 samples | A patients | none on this pack: no day-1 value above 5.5 and no patient whose only value above 5.5 is at week 56 (asserted counts 0) |
| local mEq/L units | A patients | none (equal to mmol/L) |
| the week-52 visit day | B years | the visit day included: 149.1, 150.4, 147.7, 148.1, 146.7 |

**Referee.** The adverse-event record of each restart ("drug interrupted") and the trough concentrations at later
visits corroborate the dosing record against the disposition form; no ask needs them to be computed.

| Ask | Figures | Cracker (lands the call, runs the battery, executes every filed rule) |
|---|---|---|
| A patients with potassium above 5.5 (placebo, 5, 10, 20, 40 mg) | 5 | miss |
| A hyperkalaemia adverse events (placebo, 5, 10, 20, 40 mg) | 5 | miss |
| B patients who stopped for good (placebo, 5, 10, 20, 40 mg) | 5 | miss |
| B years on study drug (placebo, 5, 10, 20, 40 mg) | 5 | miss |

The cracker keeps the central filter it built for the call (Ask A patients), counts adverse-event records after
applying the SAP's terms and window (Ask A events), counts the disposition form's discontinuations (Ask B stopping)
and sums dosing-record lengths to the day before the week-52 visit (Ask B years); each device moves every arm
(asserted per arm in `checks.py`).

Mirror leakage: 10 per cent of ask weight at most (the mirror stops at rung 1, files 40 mg and runs the same ask paths
as the cracker; with every device moving every arm it keeps no ask figure on the shipped pack, and the tenth is the
margin for a regrade).

Pair ceiling: 31 (cracker 45 with no ask kept; mirror 5 + 7 + 5.5 = 17.5 at a tenth of the ask weight).

**Stage 4 (2026-10-13).** Leak reader (isolated, medium): nothing names the decisive step, ranks the doses, exists
only to help or reads as the answer; no filed sentence names a method, slope, knot or window for the projection; the
main answer is an analytical choice. Its two notes were fixed in the generator: the synopsis's dose-selection
sentence now names "this trial's primary end point, the change in eGFR from baseline to the month-36 visit" (the
phase 2b's primary is UACR), and recheck requisitions vary between a renal panel and a full panel, so the test counts
differ. Determinism judge (isolated thread from the agent's brief, medium): DETERMINISTIC, APPROVE; Gate G pass
(forecasting mechanism, analytical_non_defect, no surface-read dependency, no sole defect); Gate H domain pass,
layers pass, decisive step analytical; every graded figure reproduced (3.04, 2.04, 1.05, -0.01; the four tables).
Its low findings: the window start (the data identify week 24: residual sums of squares of the 40 mg line 0.593 from
week 12, 0.167 from 16, 0.073 from 20, 0.014 from 24 and 0.013 from 32); the write-up's diuretic counts, which
depended on a counting rule, are cut from `submission.md` and kept in the memo with the rule stated; dropping
haemolysed samples moved 5 mg to the edge, fixed by filing every repeat sample under the visit it replaces and
carrying the haemolysis condition on the potassium result only (the variant now lands 0.24, 1.17, 3.08, 2.40,
asserted). The reader re-ran on the changed documents.

**Pre-ship check, the 10/10 rules re-read against the built pack.** Domain: the deciding quantity is each dose's
eGFR difference from placebo at month 36 on the phase 3 synopsis's estimand, estimated by nephrology's acute and
chronic eGFR slope analysis on a randomised trial's repeated central eGFR; with another field's nouns there is no
haemodynamic fall, no background diuretic held for twelve weeks and then eased, no recovery of a volume-related fall
and no chronic slope to carry, so the swap breaks (judge: domain pass). Two layers: the Layer 1 mess (two laboratory
hubs and local laboratories, units, repeat samples, out-of-window visits before week 24, bottle-period dosing
records, a disposition form not reopened, severity changes as new records, country spellings of medications) is
neutral on the call by assertion (R2: each item mishandled leaves every figure in its bin), and Layer 2, where the
chronic phase starts, decides it (R3a files 40 mg on the clean pre-extract measurements with every filed rule
applied, R3b the decisive step alone files 20 mg). Decisive step analytical: the month-3 two-slope route files 40
mg and the week-52 difference and the total slope file 10 mg with every field read and every rule executed (judge:
decisive_step analytical, analytical_non_defect); nothing planted, no decoy, no certified replay, no filed slope
method.

## Tried and rejected

- First draft (v1, drafted 2026-10-08, never registered): every proposal failed a different launch condition and the test-calendar
  library-fill clause widened the choice to the registered library, where only E cleared all three. Died at checkpoint A because the
  decisive step was a written rule a strong solver follows once no proposal qualifies (measured trap #9 alone scored 0.58 in its
  nearest exemplar, so the stump leaned on lower rungs firing first, and the nearest dead shape is argmax under a stated rule over a
  filed candidate list, task36), and because its honest Gate G, binding_constraint, collided on (objective, G11, binding_constraint)
  with task106 and 13 older builds and passed only after the card relabelled it method_or_model_selection.
- Redraw candidate, 2026-10-09, the leader outside the logger's reach: B's pinned listings fall outside the logger's per-session
  candidate pool on most new-buyer sessions, so its new-buyer guardrails are not identified and B cannot be certified (#13, G15,
  guard PASS). Dropped before registration: it fails Gate G's instrument repair (a logger able to draw B's rankings observes the
  decision's quantity directly and the task collapses, the 89 v6 dead shape), and it carries an arithmetic symptom, B's
  self-normalising weight sum at a fraction of the session count, visible to any solver who prints the normaliser or the
  unnormalised estimate beside the normalised one.
- Other decisive moves screened at the redraw and rejected on paper: carrying a correct pooled lift onto the Q1 traffic mix (the
  transport driver of task43 iteration A, task44 v2 and task83); habituation measured from each buyer's prior exposure count (task83's
  conditioning on each unit's own treatment history); shared unique listings depleted across buyers (task106's shared-pool driver);
  the Q1 control being a retrained incumbent (a dated release-calendar line that asks the question for the solver); and a test-power
  or clustering argument (G2 is banned against task120 and G17 is supporting only).
- Design stage, 2026-10-09, grading the draw's 48 guardrail cells as the shape's grid: rejected on the pair
  arithmetic. The guardrail read is on the main call's path and on the kept basis only B's row moves out of its
  bins, so the response that lands E keeps all 48 and the best response that stops at B keeps about 40; the pair
  sits above 50 on paper. The grid became each policy's fee income by cell, and the guardrail moved to hatching.
- Design stage, 90 per cent lower bounds as graded figures and as the lift condition: rejected. A delta-method bound
  and a bootstrap bound differ in the first decimal, and B's kept bound sat at +0.4 against a zero bar, a knife
  edge on the runner-up. All three conditions became point rules with stated margins.
- Design stage, a fee charged once per checkout and repeated on every order line (D6) as the grid's primary:
  rejected. Splitting a bundle's fixed fee between the carousel order and the other items in the same checkout is an
  allocation fork on every bundled cell.
- Design stage, refunds on cancelled orders as a fee-path device: rejected. Cancellations visible on the ask path
  invite taking cancelled orders out of the main call's lift, a fork on a graded figure.
- Design stage, the offers clock (UTC acceptance against local checkout at a 24-hour expiry) as a hazard: rejected on
  magnitude, about 0.4 per cent on a cell, inside the one-decimal bin.
- Design stage, shipping each archived session's follow-up orders so the archive is blind by construction in the
  pack: rejected. The column names the other outcome and hands route 1 over; the archive ships in-session orders
  only and the blindness is asserted in the generator with the hidden follow-ups.
- Design stage, a first-time-seller ask on a prior-account chain (D7): dropped for this pack. Its construction layer
  is level (B's brought-forward orders rarely go to first-time sellers) and its two files take the pack past 24;
  kept in reserve as an ask device for a hardening loop.
- Design stage, the draw's four-rung sketch (A, C, B, E) carried as the ladder: below the pipeline's five-rung floor,
  because replay and per-render weights both named A, so the two refused estimators were one rung. Split by giving
  the logger's D allocation to the pickup cities (replay over the render rows names D) and A its gain in long
  sessions (render weights name A); every leader is still a different policy.
- Build stage, 2026-10-09, the design's render-weights figures for B (8.31 in-session, 7.70 kept): infeasible.
  With B's session-weighted borrowing at 4.73, the render-weighted borrowing cannot fall below 4.73 x 150,400 /
  404,990 = 1.76 even with every borrowed order in a single-render session, so B's render-weighted kept could
  not exceed 6.55 and the render/eight-cells/kept grid cell would not name B by 1.15x over E. Repaired in the
  data rather than the ladder: B's added new-listing orders rise with session length in the new-buyer cells, so
  B's render-weighted in-session figure is about 9.0 and its render-weighted kept about 7.0 (1.20x over E), and
  A's render-weighted figure rises to about 11.0 to keep rung 1's margin at 1.22x over B.
- Build stage, 2026-10-09, the design's 90 per cent bound check (a bound above zero passes B, D and E and fails F):
  dropped. On the kept basis every policy's per-session outcome includes three weeks of orders, so a delta-method
  bound straddles zero for every policy and the sentence would be false; the charter's conditions are point rules
  and the charter says so, which is the closure, and no assertion claims a variance result.
- Build stage, 2026-10-09, organic watched-listing exposure for the five rankers that do not read saves (the design's
  "plus 0.03 of organic watched exposure" and borrowed 0.06 to 0.30 for A, C, D, E, F): dropped. Route 1 and route 2
  agree to the order and to the cent only if each (cell, ranker) group's in-session watched purchases are a
  multiple of eight with five in eight bought anyway; at an organic purchase rate of 0.1 to 2.3 per 1,000 a group
  of 400 to 3,000 sessions can only hold 0 or 8, so one octet put 3 borrowed orders per 1,000 into a single cell
  (F, web 30-179) and erased F's young-to-old spread that the restatement device needs. Now only the velocity
  boost's build shows a buyer's watched listings (every other ranker, archived ones included, draws from a pool
  that leaves them out, which is also why no archived test could see the borrowing); the other five policies' kept
  and in-session figures are equal, and the decomposition applied to B alone files E at 5.7, a cracker.

- Build stage, 2026-10-09, the design's assertion 13 as written (any segment's anyway rate, applied to every
  session, files the same kept figures): infeasible. B's kept lift moves about 7.5 per 1,000 per unit of the rate, so
  a segment 0.008 off the pooled 62.5 per cent (four-render sessions, 63.3) nets B to 3.25, across its bin edge, and
  no position of B inside its bin survives a spread of 0.01 either way. Replaced by the readings a solver actually
  runs: every segmentation netted stratum by stratum (cell, ranker, cell by ranker, platform, tenure band, renders,
  watch-list size, weekday, ISO week, half) and each natural sub-population's rate (incumbent arm, velocity arm,
  each platform, each half, one-render and up-to-two-render sessions) applied to every session, all filing E 5.7
  and B 3.3; the most extreme single segment applied everywhere is recorded as the thinnest boundary, not asserted.
- Build stage, 2026-10-09, the two halves of the logged window stratified on in-session outcomes only: each
  policy's kept lift differed between the halves by up to 12 per 1,000 (B 9.4 against -2.8), because three weeks of
  background orders per session fell at random between the halves, which hands a solver who checks stability a
  reason to distrust route 1. Equal half sums of in-session and 21-day orders per (cell, ranker) then still left C
  and D 0.4 to 0.5 apart on the kept basis, because a group with an odd session count puts one more session in one
  half and a kept base of about 1.8 orders a session moves that half's mean. Now each group's halves hold the same
  mean of both counts to within one order, the odd orders and sessions placed by a search that matches each
  ranker's half gap to the incumbent's; every policy's halves agree within 0.09 on either basis.
- Build stage, 2026-10-09, placing the fee cells by whole-euro price moves on plain orders alone: could not carry
  the price-paid device out of the bin where the arm's accepted-offer discount per session matched the
  incumbent's (shifts of -0.008 to 0.034 in five cells), and in two cells the January row and the asking price
  cancelled. Replaced by three levers on the cell's own in-session orders, searched together: a plain order's price
  moves the figure and every reading alike, the asking price of an order bought on an accepted offer moves only the
  asking-price readings, and the price of an order paid in person moves only the readings that charge it; every
  one of the seven device combinations and the natural read now clears all 48 cells, the two under EUR 1.00 included.
- Build stage, 2026-10-09, the slot-total placement as first written scored distance from the round hundred, which
  pushed the totals toward the bin edges (A's orders sat 14 from one). Now scored on distance to the edges, 20 to
  45, with every wrong reading of every total at least 5 outside its hundred.
- Build stage, 2026-10-09, the pooled-lift stop on ask 2 (one pooled kept lift times the planned total) against a
  planned Q1 cell mix that matched the logged summer mix: it filed the same hundred as the cell-by-cell total for
  B, C, E and F (4 to 23 orders apart). The weekly table now carries a January new-buyer surge in both years (the
  0-29 band peaks 8 points above its base share in early January, the 30-179 band 4 points), which puts the pooled
  and cell-by-cell totals at least 138 orders apart for every policy before placement.
- Solver round 1 (plain, 2026-10-09), the five-rung build as shipped: LANDED, proxy 89.8, asks 6 of 8. The solver walked every
  rung without friction and executed the decisive one at its step 6 as a work order: "Lift outcome: all orders by the buyer (any
  channel) within 7 days of session start, from orders_enrolled_buyers. The result is identical at 14 days. HC-33 pins watch-list
  listings in tiles 1-2, which cannibalises favourites/alerts orders in the 180+ tenure cells, so its net log-mix lift is 3.30
  against a gross carousel lift of 7.96." The charter's lift definition (orders during the test, every channel) plus a shipped
  all-channel order file keyed by buyer makes the any-channel window the default outcome, so the netting is never a construction.
  It also kept every ask figure (48 fee cells, 12 totals), and it weighted the headline to 5.8 on the slot mix against the
  golden's 5.7 on the logged mix while using the slot mix for the totals, a determinism finding on the headline basis.
- Harden loop 1, diagnosis of round 1 (the borrowed-order netting as the decisive rung; P1 in-person pickups, P2 the R2
  restatement, HZ1 the deferred tariff, HZ2 the price paid and HZ3 the app gating as the ask devices): the decisive quantity
  was the charter's own observable, so the solver never had to think of borrowing at all. Its "Lift outcome: all orders by
  the buyer (any channel) within 7 days of session start, from orders_enrolled_buyers. The result is identical at 14 days"
  is charter 2.2 executed on the one extract that already holds every order by buyer, and the netting of B fell out of it as
  a by-product ("which cannibalises favourites/alerts orders in the 180+ tenure cells"). Every ask device died the same way:
  each organ sits in a file the ask's own path opens with its rule beside it ("recomputed at the 1 Sep 2026 tariff ...
  because KB-2027-01 was deferred", "Pickup orders paid directly carry no fee", "R2 restatement 2026-W01..W12 (it matches the
  account-service tenure), app only from W03 because of the release 27.1 gate"). Dead: a decisive rung whose correct basis
  is the definition's own observable on a shipped extract, and an ask device whose rule is filed in a document the ask path
  reads anyway. What the trace holds fixed without checking is that the logger's in-session columns measure the charter's
  quantities whenever the charter is not about orders over the test (its guardrail is read "from ordered_tiles"), which is
  where loop 1 goes. Harden loop 1 of 3 on this architecture.
- Harden loop 1, the come-back orders credited to the session the tile was in (home_session_id = the logged session): the
  habitual tie between ordered_tiles and the carousel orders credited to each session then failed in 202 sessions, every one
  outside C, an arithmetic symptom on the wrong path that points straight at the device. Now each come-back is credited to
  the session it was placed in, the tie holds in all 150,400 sessions, and the field reference's seven-day rule lets the
  listing alone attribute the order to its tile.
- Harden loop 1, no come-back orders at all under C: one zero in a by-arm count reads as a marker; C now comes back at 0.15
  of the others' rate (3 orders, none in app 0-29).
- Harden loop 1, charter 2.4 as written ("its orders placed from a home carousel tile"): it also admits every carousel order
  by the arm's buyers in a window, a reading under which C passes and is filed; 2.4 now counts the orders placed from the
  carousel tiles the arm served.
- Harden loop 1, the January new-buyer surge at 8 and 4 points (built for the pooled stop on ask 2): it put the slot-mix
  headline at 5.8 against the logged window's 5.7, round 1's determinism finding. Cut to 2 and 1 points, the headline
  converges (5.716 against 5.697) and the pooled totals fall 14 to 41 orders from the cell-by-cell ones for B and E, which
  no placement can carry out of the hundred, so the pooled stop is retired: pooled readings are placed at least 5 from the
  edges on either side and recorded.
- Harden loop 1, every fee reading as a stop on ask 2: B with only P1 mishandled and F on the first release alone sit 25
  and 14 euros from their golden totals, under the 25 a stop needs with the golden 20 from its edges; both are carried as
  either-side readings at least 5 from the edges (both inside) and the placement reached 6.4 of slack.
- Harden loop 1, fee cells placed anywhere from 0.35 to 0.65 of the bin: 7 of 48 landed within 0.003 of the round
  one-decimal value (7.0001, -14.5997 and so on), a receipt; the window now leaves out the middle tenth.
- Harden loop 1, a fresh silent device for the order totals (the logger slice held out of slot arms, a weekly table
  counting home sessions rather than carousel sessions, Easter falling in the slot's last week, staff and monitor
  accounts in the weekly table): each needs a new organ on the traffic path or a rate the pack cannot pin, or reads as
  sabotage; the order half keeps P2 and HZ3 and the pair arithmetic counts it as leaking to both sheets.
- Harden loop 1 as built, graded in the re-run of round 1 (labelled "round 2, plain", 48.7, call missed, 3 of 8 items):
  the tile count held the call (the solver filed C at 9.8 with E as runner-up, its step "Guardrail on the in-session
  carousel order rate: the only breach is HC-31 in web 730+" never sees rung 3), but the ask layer leaked exactly as the
  stated exposure said: "This reconciles exactly to the Finance Q3 sheet (the 6,147 July shipped orders missing from
  payments supply EUR 8,205.17)". Reading the referee settled F1 (VAT out) and F2 (balance purchases charged), so all 48
  fee cells and all twelve totals landed. A referee that ties to the cent only under the golden fee basis is a recipe
  the solver reconciles to, not a silent organ; the fee devices cannot rest on the referee going unread.
- Harden loop 2, diagnosis of round 2 (loop 1's ask layer: F1 fee income net of VAT and F2 balance purchases charged as the
  silent primaries, P1, HZ1 and HZ2 stacked on every fee figure, P2 and HZ3 on the totals, and Finance's Q3 statement as the one
  referee, tying to the cent only under the golden fee basis): the tile count held the call, and every fee figure fell to one
  reconciliation, in the solver's words at its step 7, "Fee income is taken excl. 21% VAT. This reconciles exactly to the Finance
  Q3 sheet (the 6,147 July shipped orders missing from payments supply EUR 8,205.17)". A statement scoped to the extract's own
  buyers that ties to the cent under exactly one fee basis arbitrates all five fee devices at once and hands over the level,
  which is the oracle law 8 bans, not a referee; every device it did not settle was a filed rule the path reads ("KB-2027-01 was
  deferred by the 6 Oct pricing committee", "uncaptured pickups were paid directly and carry no fee", "app uses W03 to W12
  because the first app release on or after 4 Jan 2027 is 27.1"). Dead: a fee device whose correct handling is also the only
  basis on which the logged window's statement ties. Harden loop 2 of 3.
- Harden loop 2 build, the in-person price lever as single-euro moves within plus or minus 30: it moves only the full-cover
  half of a cell, and F app 730+ (23 in-person orders) could then clear its bin by no more than 0.0035; the lever now moves
  up to 3 euros an order over plus or minus 60 units, applied round robin across the cell's orders.
- Harden loop 2 build, traffic readings within 30 of a hundred's edge treated as stops: B's fee total with only the cover
  change mishandled sits 6.3 inside its hundred and no set of traffic factors carried every stop out (the placement score
  stayed negative); the near band is 40 and the readings in it are either-side readings, B's FX-alone total among them
  (recorded as kept by round 2's path).
- Harden loop 2 build, every fee reading at least 0.03 outside its bin: D app 0-29 with only the January row applied can
  sit no further than 0.0246 outside, because the two tariffs differ too little on that cell's orders for the price
  levers to widen it; the floor is 0.02.
- Harden loop 2 build, VAT taken off order by order converging without a lever: on an early placement one B web cell's
  per-order rounding fell 0.0031 outside the golden bin; a pair lever (plus and minus one euro on two plain orders, which
  moves only the per-order rounding) was added, and on the final placement it needed no pairs (0.0227 inside at the
  nearest).
- Harden loop 2 as built, graded in the re-run of round 1 (labelled "round 3, plain", token proxy 51.1, call missed, 4 of 8
  items by token; read-corrected about 23 to 31, because notebook items 1 and 2 and image items 2 to 4 were credited on HC-37,
  5.7, HC-33 and HC-34 named in the solver's screen-out and negation sentences): the tile count held the call for the second
  round running (C filed at 9.8, E runner-up at a gap of 4.1, at the same step, "Condition (b), each cell's carousel order rate
  against HC-24: HC-31 web 730+ is -2.74% and fails. All other policies' cells are within -1.5% (HC-34 app 0-29 -0.96%)"), but
  loop 2's ask layer leaked whole again: all 48 fee cells and all six policies' twelve-week totals landed, at its step 8, "covered
  orders are shipped orders plus pickup orders captured by card or iDEAL, which reproduces Finance's protected orders and fee
  excl. VAT exactly ... Tariff for 2027 stays 0.80 + 5%, because the pricing committee minutes of 6 Oct defer KB-2027-01", and at
  step 9 it read P2, HZ3 and the 1 March cover change straight off the filed notes. Dead: a fee basis that still ties Finance's
  Q3 statement to the cent (the referee survived loop 2 as an oracle under a new cover rule) and traffic and tariff devices whose
  rule sits in a document the ask path opens. Harden loop 3 of 3 on this architecture is the last before a re-root.
- Harden loop 3, diagnosis of round 3 (loop 2's ask layer: FX, the 1 March 2027 checkout change in the capacity note's
  overlaps section, as the fresh primary on all 48 cells and the six fee totals; F1 VAT, F2 balance purchases, HZ1 the
  deferred January row and HZ2 the price paid stacked on every fee figure; P2 the R2 restatement and HZ3 the app release
  gate on the totals; Finance's Q3 statement as the one referee, still tying to the cent on the logged window's cover): the
  call held at the tile count, and the whole ask layer fell to two habits the solver runs by default. It reconciled its fee
  model to the referee, which still ties the logged window under the golden's own per-purchase basis and so settles VAT,
  balance purchases and in-person pickups in one pass, in its words at step 8, "covered orders are shipped orders plus
  pickup orders captured by card or iDEAL, which reproduces Finance's protected orders and fee excl. VAT exactly ... Tariff
  for 2027 stays 0.80 + 5%, because the pricing committee minutes of 6 Oct defer KB-2027-01 even though the tariff register
  lists it"; and it executed every rule filed on the traffic path as a work order, at step 9, "The app arm starts 18 Jan
  2027 (release 27.1 after the code freeze), so app runs W03-W12 and web W01-W12 ... From 1 Mar 2027 (W09-W12) every
  pickup order is paid at checkout and carries the fee", so FX, built to sit off the fee path, was read in the same pass as
  HZ3 because both sit in the capacity note. Dead: a referee whose figure the golden's fee basis reproduces on the logged
  window (whatever changes for the slot, the statement hands over every logged-window device at once), and any device whose
  rule is a dated, named sentence in a document the ask path opens (the minutes, the release log, the capacity note), because
  the solver reads every note on its path and carries out what it says. Harden loop 3 of 3.
- Harden loop 3 build, the either-side band at 40 (a wrong total under 40 from its golden placed on whichever side of the
  edge it falls): infeasible on this pack. E's fee total has two compound readings on the twelve-week app traffic, one 52
  above the golden and one 55 below, and no placement keeps the golden 20 from the edges while carrying both out of a
  hundred-wide bin by 5 (best score -0.03 after refinement). The band is 56, which adds only those two readings.
- Harden loop 3 build, the traffic placement with every first-release total scaled linearly by the placement factors: the
  restatement's moves were counted on the placed table, so a placed cell's first-release sessions were not the factor times
  the unplaced cell's, and B's fee total on the first release with balance purchases uncharged and the logged checkout
  landed 0.21 inside its hundred's edge in the files against at least 5 predicted (the build stopped on
  ask2.every_reading_clear_of_the_edges.B). The moves are now counted on the unplaced table and added to the placed one, so
  a first-release total is the placed table's plus a constant and the placement is exact.
- 2026-10-10, retired: it passed both solver rounds after three hardening loops, but the determinism judge sent it back on Gate G: the answer wins only by reading the charter's outcome definitions in place of the logger's in-session reads (a single conceptual flip), and the shipped planning thread ranks the candidates. Under the author's standing rule a Gate G send-back is retired like a dead build, and DS11 takes the slot in a later wave.
- 2026-10-13, re-root under the 10/10 rules (v2 to v3): v2 is FAILED_TO_STUMP in perssathya's backlog. Its
  decisive step, the logger's in-session order column read against the charter's count of every order placed from
  the tiles an arm served, is a field read under a filed charter condition (data semantics plus rule application),
  and its estimator was pinned by nine certified archived tests (a validated decoy); a redesign inside the world
  would keep the carousel's nouns, and with app or retail nouns the slot question reads the same. The slot moves to
  Biomedical & Clinical Research, a domain never built.
- Re-root candidate, pharmacoepidemiology (new users of inhaled COPD treatments, time in hospital that the
  dispensing record cannot see): dropped on paper. The answer turns on the grace period and how inpatient days
  count against a supply, conventions a filed sentence would have to fix, and once fixed the step is rule
  application.
- Re-root candidate, protopathic bias with a long prodrome (a drug started for the early symptoms of the outcome
  it is then blamed for): dropped. The lag that decides is a convention the field disputes, so determinism rests on
  a pinned lag, and a solver who knows the drug class's literature reaches the answer from priors.
- Re-root candidate, criminology (reporting falls in hot-spot patrol areas): dropped; one obvious move (use calls
  from the public, not officer-initiated records), close to reading a field.
- Re-root candidate, assessment-time bias (progression found sooner in an arm scanned more often): dropped; the
  interval-censored estimate (NPMLE) is not unique and a solver's method choice moves the graded figures.
- Re-root candidate, eGFR off-treatment decomposition (the phase 3 end point read four weeks after the last dose,
  part of the early fall at the top dose not coming back): dropped as the decisive step. The natural construction
  (the week-56 off-treatment difference plus two more years of chronic slope) lands the golden, so it sits inside a
  strong solver's hypothesis space; with monotone dips and slopes, the one-year view and the slope-only view
  bracket the three-year answer, so in a pick of three one simple view always lands the call.
- Re-root candidate, a titration step at week 12 for the top dose (its further fall after the field's month-3
  knot read as a steeper chronic slope): dropped as the decisive step. The step is in the protocol and is a
  4.6 mL/min drop in one arm between two visits, a visible symptom a solver investigates; it also penalises the
  top dose in the same direction as the golden's dip, so the margins the conventional route needs are thin.
- Re-root candidate, slow drug accumulation (a long half-life, the haemodynamic fall deepening for five months):
  dropped. An exponential approach that is half done at month 3 is not finished by month 12, so no clean chronic
  window remains in 52 weeks, and one that finishes by month 6 leaves too little after month 3 to move the call.
- Re-root candidate, anti-drug antibodies (loss of response lagging antibody onset, so a 24-week maintenance read
  overstates week 52): kept in reserve, not drawn. The arm curves do not show the coming loss, which is its
  strength, but the projection rests on the loss distribution after onset estimated from a few early converters,
  and in a pick of three "fewest antibodies" or "the balanced regimen" lands the call by heuristic.
- Re-root candidate, detection bias through organ volume (a drug that shrinks the prostate makes biopsy more
  sensitive): dropped; the setting is the textbook case (the 5-alpha-reductase prevention trials), so a frontier
  solver recalls the resolution, and the adjustment's detection model is a fork.
- Re-root candidate, leaky against all-or-none vaccine protection carried to a high-transmission setting: dropped;
  the invariant-under-base-rate insight is task446's and task230's family, and the mechanism is identified only
  through a model of exposure.
- Re-root candidate, HbA1c lag (a 16-week dose-ranging read before glycation catches up): dropped on the swap
  test; the decisive move, the steady state of a lagged average, reads the same with a trailing business metric.
- Stage 3, 2026-10-13, the arms calibrated to the arm-mean line alone: the mixed model with a random intercept and
  slope per patient, the field's own slope estimator, read 10 mg about 0.4 higher on every measurement draw, because
  the few patients who left or stopped in an arm pulled its later visit means. Fixed in the data: the dropout, stop
  and potassium streams are drawn so the arm-mean line and the within-patient estimators agree, then the measurement
  draw so every estimator from week 24 sits in the golden's bins.
- Stage 3, the claim that a knot anywhere from week 24 to week 32 gives the golden figures on any draw: a slope from
  three visits carried to month 36 multiplies visit noise about sixfold, so the corridor is a property of the
  shipped draw, asserted, never of the design alone.
- Stage 3, treatment policy as a same-figures fork (SF5): values after a permanent stop show the early fall reversed
  and lift the late visit means; on the shipped draw 40 mg's figure moves a bin. SF5 is closed by the synopsis's
  intercurrent-event strategy (C4), the call unchanged.
- Stage 3, a chance baseline imbalance: a 40 mg arm whose baseline sat 0.85 below placebo's moved the level reading
  of the prompt's "how much higher eGFR would be" a bin. The randomisation's block order is drawn so every arm's
  baseline sits within 0.1 of placebo's, and the level and change readings converge (SF3).
- Stage 3, visits outside their windows at any week: dropping the few late ones from weeks 24 to 52 moved 40 mg's
  figure across an edge. Sites keep to the window from week 24 (out-of-window visits fall before it), so the mess
  cannot reach the decisive fit.
- Stage 3, clinic visits on weekends and a missed dispensing visit leaving one bottle for seven months: dates moved to
  the nearest weekday and drug collected at the site on the missed visit's day.

## Architecture v2 record (spent 2026-10-13)

Realised analytical_tasks note DS01 (carousel test slot); registered 2026-10-09 after checkpoint A, built, three
harden loops and five solver rounds, retired 2026-10-10 after a Gate G send-back, never submitted, then put in the
author's backlog as FAILED_TO_STUMP and re-rooted here.

| Axis | Value |
|---|---|
| Domain / subdomain | Product Analytics / experimentation-measurement |
| Objective | Experiment & Causal Analysis |
| Niche | a Dutch peer-to-peer second-hand fashion platform (Vouwlijn) choosing which of six registered ranking policies takes its home carousel's Q1 2027 A/B test slot, every policy scored off-policy on randomised carousel logs |
| Shape | 07 grid of cells |
| Decision type / unit | pick one of six policies (named option) |
| Gap / pattern / generators | time, rule, population; none, B; G13, G9, G16, G2, G11 |
| Gate G mechanism | decomposition_attribution |
| Stump strategy | decomposition_attribution; decisive rule filed, official decoy, validated decoy (nine archived tests pinned the estimator) |
| Calibration form | pilot_log |
| Stakeholder / forum / forcing / org family | head of marketplace science / executive_team / vote_or_meeting / software_or_platform |
| Deliverables | `carousel_slot_q1_2027.ipynb`, `carousel_slot_q1_2027_cells.png` |
| Answer | E, the sequence ranker with the fresh-listing interleave (HC-37), 5.7 extra orders per 1,000 carousel sessions |

Stump (harden loop 1 onward): a solver who scores the six policies with the session-weighted estimator that alone
reproduced the nine archived tests and reads the cell guardrail on the render log's in-session ordered tiles
commits the slot to C, the session-sequence model; the charter counts every order placed from the tiles an arm
served, and buyers under every other ranker come back to order from a tile left on screen after the session
closes, so C fails the guardrail in app 0-29 and E is the largest lift that clears every condition.

Fate: solver rounds 2 to 5 held below 52 after round 1 cracked the draw's rung; the determinism judge sent it back
on Gate G (the answer wins only by reading the charter's outcome definition in place of the logger's in-session
read, a single conceptual flip, and the shipped planning thread ranked the candidates). Under the 10/10 rules the
decisive step is data semantics and rule application, so the architecture is spent.
