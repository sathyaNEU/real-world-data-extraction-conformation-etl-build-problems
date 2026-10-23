# task170 design note: the employer match Vindeholm County Hospitals will pay in FY2027 on its first auto-enrolled intake

Architecture 4, a from-scratch rebuild of a reopened number (Forecasting lane, sathya8571), in a cell this session
chose under the main session's conditions (`## Rebuild`): psychology-behavioral-science /
decision-making-computational-behavioral-modeling. Architecture 3 (the repellent net campaign) is summarised under
`## Architecture 3 record`, architecture 1 (the paediatric ARV order) under `## Architecture 1 record`; architecture 2's
cells and the expected-credit-loss cell died before any card (`## Tried and rejected`). The setting is fictional
throughout, country included: Tarnland, Vindeholm County, Vindeholm County Hospitals and its six hospitals, the VCH
Supplementary Savings Plan, Ledstrand Pension Administration and Tarnmark Mutual are invented, and no record is a real
employer's, administrator's or insurer's.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task170.json`, architecture v4, v3 moved into `lineage` with its fate
   beside v1. `guard.py check` WARN (answered in item 9); nearest drivers 0.05 (task129 v1 lineage, task230 v1
   lineage), none flagged.
2. Pairing: Psychology & Behavioral Science (client domain) / `decision-making-computational-behavioral-modeling` /
   Forecasting & Predictive Modeling (the taxonomy lists the task type under F only; no card on file in the pairing).
   The deciding analysis is a choice model of a default: each hire holds a preference and a moment of active choice,
   the default holds until that moment, and the forward default's take-up is rebuilt from the two, the way
   behavioural models of defaults and procrastination separate preference from inertia.
3. Niche: a county council's hospital group (about 9,000 staff in six hospitals) whose supplementary savings plan has
   been opt-in since 2012 enrols every new hire automatically at 3 per cent from 1 January 2027; the reward and pensions
   manager forecasts the employer's match on the 2027 intake for the FY2027 budget.
4. Call and shape: the employer match on the 2027 intake over the January to December 2027 payrolls, a currency figure
   (`quantity_figure`, how much). Shape `other`: the group figure with each hospital's (which inherit the decisive
   step), the intake contributing on the December 2027 payroll, the two critical components (the share of hires who
   join when joining is their own choice, the share who have made a choice by the twelfth payroll), and asks on rows
   the call never reads (the 2026 payroll's match lines, the register's members from before 2019). Shapes 14 and 01
   are banned by the last two builds; criteria are counted in `## Ask sheet`.
5. Mechanism keys: gap time (when each hire makes a choice against the payroll months of 2027), then population (the
   opt-in record shows only the hires who chose to join); pattern none; generators G7 (the default holds only until
   the hire's own moment of choice) and G14 (the record's take-up does not carry to the opposite default); Gate G
   `forecasting`; strategy `other` (a choice model of a default; the card's notes say why and that
   `population_selection`, in the ban window against task274, also describes the plateau step); Layer 2 family
   `field_method`, pattern `own:the-default-holds-until-each-hire-makes-an-active-choice-on-the-clock-the-opt-in-record-shows`.
6. Default path's answer against the golden: carrying the income protection cover's cancellations by month of service
   (the group's one record of hires leaving a default) as the plan's opt-outs files TNK 14.5 million (14,409,662);
   reading the opt-in join curve as the share who have chosen files 14.0 million; the 43 per cent who join contributing
   from the first payroll files 8.5 million; the golden, the hires not yet chosen at 3 per cent plus the joiners at
   their own rates, files TNK 11.5 million (11,439,212 unrounded).
7. **Data-native sentence.** Vindeholm's hires join an opt-in plan at a pace (a third at induction, the rest over the
   following year) that the register shows only for the 43 per cent who join, while the 57 per cent who never join
   leave no trace, and the one record of hires leaving a default (a cheap income protection cover) is set by a
   preference only 16 per cent hold; so the clock on which every hire makes a choice is the join curve over its own
   plateau, and under a 3 per cent default the hires who will opt out are the plateau's complement leaving on that
   clock.
8. Sources, one line each. `guide-to-prompt` domains README (the task type serves F); the behavioural literature on
   defaults (Madrian and Shea 2001; Choi, Laibson, Madrian and Metrick 2004; Carroll, Choi, Laibson, Madrian and
   Metrick 2009) for the structure only: preference against a cost of acting, take-up under opt-in and opt-out
   converging on the same long-run share. No card or seed is used; the pitfall is re-found from the record's own
   structure (only joiners are visible; the cover's level is a different preference). task136 (a scheduled
   intervention enrolling units that were about to take up on their own) and task137 (a behavioural share at a
   repricing) were read for their drivers and differ (card `differentiation`).
9. WARN answers. `overuse.objective`, `overuse.gate_g` and `repeat.gate_g` (forecasting in 6 of 12, beside task178):
   the objective is the lane's; the mechanism is not any recent build's. `repeat.decision` (quantity_figure beside
   task274): the call is a budget line, the decision's own unit. `people.first` cleared by drawing replacements.
10. People (`guard.py names --locale sv_SE --seed 170`; the country is fictional, so the locale is passed and named):
    Caroline Hagman (reward and pensions manager), Erik Palm (director of finance), Alfred Sundberg (payroll services
    lead). None appears in the prompt.
11. Furniture: forum `committee_or_panel` (the county council's employment committee, which approved the enrolment
    and signs off the FY2027 pay budget), forcing event `budget_or_appropriation`, organisation family
    `hospital_or_health_provider`, role family `other` (HR's reward and pensions manager, a role the vocabulary does
    not name), context artifact `other` (the plan amendment's committee paper), calibration form `other` (the income
    protection cover, auto-enrolled with opt-out since 2019). The first draw sent the forecast through the director of
    finance to the executive team (`finance_controller`, `executive_team`); the window moved under the registration
    lock (task175 holds both), so the world was redrawn to the committee and the prompt's note goes to it.
12. Cell choice (the main session's conditions, 2026-10-23). The forward window changes the process in a way not on
    file: no Vindeholm plan has ever defaulted anyone in, so no record shows a hire under a plan default. The record is
    not replayable (no opt-out pension history exists to copy), not one group-by (the take-up needs a censored join
    curve, its plateau, the clock as their ratio and the recombination under the opposite default), and not a
    field-standard correction (no textbook adjustment turns an opt-in record into an opt-out forecast; the field's
    habit is a benchmark opt-out rate). The materials of the decisive step sit in three files from three systems (HR's
    spells, Ledstrand's register, the plan rules), and the one document that names the change (the committee paper)
    states only the estimand. Excluded as spent: every cell in this note and in the siblings' `## Rebuild` sections as they stood when the
    cell was chosen. task173 chose the same cell the same day and recorded it dead under its `## Rebuild` (commit
    1d4ac1b9, landed while this draw was being measured) on a different mechanism: a reference-dependent courier
    stopping rule whose lever is bounded by the size of a pay change. Nothing here turns on a pay change or a
    stopping rule, no card of task173's sits in the pairing, and the overlap is reported to the main session.

## Default path

The route a competent analyst takes from the prompt and the pack, every field read and every filed rule applied:

1. Take the intake from the amendment's section 4: the approved requisitions of vch_hiring_plan_2027.xlsx (3,025),
   each paid at the 2027 scale for its grade and FTE from its planned start month.
2. Build how many of the group's hires since 2019 are still on the payroll by month of service from the HR history,
   leavers dropping out at their month.
3. Enrolment at 3 per cent means everyone contributes unless they opt out. The group already defaults every hire into
   one benefit, the income protection cover, and Tarnmark's bordereau shows when hires cancel it: carry the cover's
   cancellation share by month of service as the plan's opt-outs, everyone else at 3 per cent.
4. The match on 3 per cent is 3 per cent of basic pay (rules, section 4); sum over each requisition's 2027 payrolls.

Ends on: TNK 14.5 million (14,409,662 unrounded).
Golden: TNK 11.5 million (11,439,212 unrounded).

## Stump sentence

A competent analyst carries the income protection cover's cancellations, the group's one record of hires leaving a
default, as the share of the 2027 intake that will opt out and files TNK 14.5 million against 11.5 million; the step
that lands it there is reading a cancellation curve set by the 16 per cent of hires who want to drop a 0.4 per cent
cover as the opt-outs of a plan 57 per cent of hires never join, when the opt-in record holds both what hires prefer
(43 per cent join within five years) and how fast every hire makes a choice (the join curve over that plateau: 35 per
cent by the first payroll, 90 per cent by the twelfth), so the intake's match is the not-yet-chosen at 3 per cent plus
the joiners at their own rates.

## Three rules

- Task type: psychology-behavioral-science / decision-making-computational-behavioral-modeling, which serves
  Forecasting in the taxonomy: the match a default will produce over a fiscal year not yet open.
- Domain test: the deciding quantity is a choice model of a default, a preference and a moment of active choice per
  hire, the default holding until that moment, recovered from a record that shows only one preference and carried to
  the opposite default; with clinical or school nouns there is no default to sit in and no moment of choice to wait
  for, because it is inertia against preference.
- Swap: "how many patients will keep their follow-up appointment once clinics book one by default" keeps the
  arithmetic of a share times a count and loses what decides here only if nothing in the record separates who wants
  the appointment from when they act; with a record of opt-in bookings it is the same model, a behavioural default,
  which is the domain's task type, not a backdrop.
- Layer 1: HR's two employee-number schemes across the February 2026 cutover (the register and the bordereau keep the
  number a membership or policy was opened under); LRC codes before the July 2024 merger; rehires as new spells under
  the same number and new memberships under the same member number; Tarnmark's old policy numbers before its July
  2022 system change; rate changes at April pay awards; a payroll
  that writes a person's match on each assignment's line and a reversed and re-run payroll. Each is what the system
  writes; none is placed to be caught, and none moves the call (`generator/checks.py` R2 rows).
- Layer 2: family `field_method`. The choice that flips the call is reading the opt-in record as a preference and a
  clock (the join curve's plateau and the curve over it) and rebuilding the take-up under the opposite default, rather
  than carrying any observed take-up or opt-out level.
- Decisive step: the share of hires who have made a choice by each month of service is the opt-in join curve divided
  by its own five-year plateau; under automatic enrolment the not-yet-chosen sit at 3 per cent and the chosen
  contribute at their own rates or not at all.
- Not semantics: every term is read correctly on the default path (the intake, FY2027, the default rate, the match,
  the pay scale, the cover's cancellations), and it still files 14.5 million, because no field, code or definition
  says that the cover's cancellations measure a different preference or that the register shows only joiners; the
  employee numbers, hospital codes and rehire spells converge under every reading (R2 rows).
- Not rule application: no filed rule or procedure computes the take-up under the new default, so executing every
  stated rule (the amendment's intake, enrolment and opt-out; the rules' match and timing; the scale) leaves the
  opt-out pace to the analyst. The enumerated family of take-up constructions (the cover's cancellations as opt-outs,
  with or without joiners at their rates, the join curve as the share who have chosen, nobody leaving, preference from
  the first payroll at own rates or at 3, the opt-in record replayed) spreads 5.0 to 16.0 million; the standing family
  (the join curve over its plateau read at three to seven years or at its end, Kaplan-Meier or complete cohorts for the
  join curve and for staying on the payroll, the clock read from the cover's cancellations over their own plateau,
  first spells only, joiners' rates at join or current, pay-weighted) spreads 11.40 to 11.50 million (0.85 per cent),
  and what rules the rest out is the record itself: the cover's cancellation curve over its own plateau runs on the
  join curve's clock (90.2 against 89.9 per cent by the twelfth payroll) at a level a third of the plan's non-joiners.
- Analyst test: a strong analyst who cleans the HR history, the member register and the payroll lines, reads the plan
  rules and the amendment correctly, and carries the cover's cancellations as the plan's opt-outs files TNK 14.5
  million (14.0 million if it reads the join curve as the share who have chosen, 8.5 million if the 43 per cent who join
  contribute from the first payroll and nobody else does), against the golden TNK 11.5 million.
- Estimand: the amendment (vch_savings_plan_amendment_2027.docx, section 4) files the population (the approved
  requisitions of the 2027 hiring plan, each filled at its planned start; nobody hired before 2027), the window (the
  January to December 2027 payrolls), the pay (the 2027 scale for the grade and FTE), the comparison basis (the
  group's hires since January 2019, all six hospitals taken together) and the outcome (the employer's match, rules
  section 4); section 3 files the default and the opt-out; the prompt fixes the unit and the rounding.
- No decoy: nothing is planted. The cover's bordereau is Tarnmark's ordinary record of a benefit the group has
  defaulted hires into since 2019, needed for the clock's corroboration; no document applies it to the plan or argues
  for it, no memo, draft or stakeholder figure carries a take-up, an opt-out rate or a match forecast, and no file is
  copied or backfilled.
- No certified replay: no certified or published figure is reproduced to recover a method; the cover's cancellations
  are outcomes of hires' own choices under a default, read forward, and nothing in the pack certifies a take-up or a
  match forecast.
- Lesson: a record kept under one default shows only the people whose preference differs from it, and only once they
  have acted, so its take-up level carries to nothing and its curve is a selected view of the pace of acting; the
  forward default's take-up is the not-yet-acted plus the acted who prefer it. No build on file teaches a default read
  through a preference and a clock (task136 enrols units about to take up on their own; task137 reads a behavioural
  share at a repricing).

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the cover's cancellations as the plan's opt-outs | no sentence links the cover to the plan's opt-outs | the bordereau's cancellation dates | the in-house opt-out analogue | none | no | one curve times pay | readable |
| R2 the join curve as the share who have chosen | no | register join dates against HR starts | the opt-in record as the choice record | none | no | one curve | readable |
| R4 the joiners from the first payroll | no | the register's join share | preferences are stable, defaults change nothing | none | no | one share | readable |
| R3 nobody opts out | no | none | inertia is total | none | no | a constant | readable |
| R7 decisive: the not-yet-chosen at 3 per cent on the join curve over its plateau | no sentence names a clock, a plateau, a preference or the division | no column holds a choice date for non-joiners or a take-up; the curve needs HR spells against register joins across two number schemes with leavers censored | the textbook carries a benchmark opt-out rate | the cover's curve over its own plateau corroborates the clock only once both curves are built | no | a ratio of two curves recombined under the opposite default | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "the staff it hires in 2027" | the approved requisitions, each filled at its planned start | a hiring trend from the record; requisitions left unfilled at a vacancy rate | other | amendment section 4: "the approved requisitions in the 2027 hiring plan, each filled at its planned start date" |
| SF2 | FY2027 | the January to December 2027 payrolls | an April to March year | other | amendment section 4: "(the January to December 2027 payrolls)" |
| SF3 | pay in 2027 | the 2027 scale for the grade times FTE | the 2026 scale, an April award | other | scale extract: "The 2027 scale applies to every payroll from January to December 2027." |
| SF4 | the default | 3 per cent from the first payroll | from the second payroll | larger | amendment section 3: "at a contribution of 3 per cent of basic pay from the first payroll" |
| SF5 | the match | 100 per cent to 3, 50 per cent from 3 to 6 | the whole contribution matched | other | rules section 4 |
| SF6 | whose experience | all six hospitals together | each hospital from its own hires | hospital figures move | amendment section 4: "all six hospitals taken together" |
| SF7 | the month of a choice | the payroll it applies to (the 10th cut-off) | calendar months from the start date | same call | rules section 3; joins dated by first contribution; asserted under SF10 |
| SF8 | the join curve's plateau | its level at five years | three, four, six or seven years, or the curve's end | same call (11,429,909 to 11,447,798) | asserted |
| SF9 | the estimator | Kaplan-Meier, leavers censored | complete cohorts for the join curve, for staying, or both | same call (11,400,683 to 11,497,776) | asserted |
| SF10 | the clock's source | the plan's own join curve | the cover's cancellations over their own plateau | same call (11,470,958; 90.2 per cent by the twelfth payroll) | asserted |
| SF11 | a joiner's rate | the rate at join | the current rate; pay-weighted | same call | asserted |
| SF12 | rehires | each spell a hire (amendment section 2 counts rehires as new hires) | first spells only | same call (11,443,595) | asserted |
| SF13 | "contributing on the December 2027 payroll" | a contribution deducted on that payroll, at the default or a chosen rate | members including those who opted out | other | the prompt's word "contributing"; asserted |
| SF14 | who is in the line | the 2027 intake only | the whole workforce | larger | amendment section 4: "counts nobody hired before 2027" |

## Ladder

| Rung | Construction | FY2027 match, TNK | Rounded | Clearance from the golden's bin |
|---|---|---|---|---|
| R0 | the cover's cancellations as the plan's opt-outs, everyone else at 3 | 14,409,662 | 14,500,000 | 5.6 bins |
| R1 | the same, the opt-in joiners at their own rates | 15,311,542 | 15,500,000 | 7.4 bins |
| R2 | the join curve read as the share who have chosen | 14,064,941 | 14,000,000 | 4.9 bins |
| R3 | nobody opts out | 16,025,948 | 16,000,000 | 8.8 bins |
| R4 | the 43 per cent who join, from the first payroll, at their own rates | 8,359,207 | 8,500,000 | 5.8 bins |
| R5 | the same at 3 per cent | 6,851,712 | 7,000,000 | 8.8 bins |
| R6 | the opt-in record replayed | 5,001,013 | 5,000,000 | 12.5 bins |
| golden | the not-yet-chosen at 3, the joiners at their own rates, on the join curve over its plateau | 11,439,212 | 11,500,000 | edge 189,212 |

Position: the default path and the near rungs sit above the golden (R0 to R3), the preference rungs below (R4 to R6);
the golden is bracketed and every rung lands in its own bin. Worth: the decisive step moves the call 21 per cent off
R0 and 27 per cent off R4. The hospital figures inherit the step (each rung moves every hospital by the same share);
each hospital's golden sits 22,244 to 41,343 from its 100,000 bin's edge against a family spread of 0.85 per cent.
The plan's monthly multipliers (1.06 in January, August and September, 0.98 otherwise) were chosen so that every
standing-family member lands in the golden's bins on every graded figure.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the approved 2027 requisitions | SF1, SF14 |
| 2 | Unit of account | TNK of employer match | the prompt and rules section 4 |
| 3 | Attribution window | the January to December 2027 payrolls | SF2 |
| 4 | As-of dating | the pull of 9 November 2026, the October 2026 payroll the last | dictionary header; manifest |
| 5 | Version basis | plan rules of February 2024, the committee paper as approved, the tracker of 4 November 2026 | one version ships of each |
| 6 | Denominator | the December contributors over nobody: a count | the prompt |
| 7 | Weighting | each hire equally in the curves; pay weights only in the match sum | SF11 asserted |
| 8 | Window length | hires January 2019 to October 2026 | amendment section 4 ("since January 2019") |
| 9 | Boundary inclusivity | a choice received by the 10th applies that month | rules section 3 (SF7) |
| 10 | Rounding path | unrounded by requisition and month, rounded once per figure | the prompt's rounding sentence |
| 11 | Tie-break | none needed | no figure on a bin edge |
| 12 | Maturity and censoring | open spells and recent hires censored at the October 2026 payroll | SF9 asserted |
| 13 | Order of operations | staying times pay times the expected match rate, summed | sums of products |
| 14 | Row order | none | sums |
| 15 | Duplicate resolution | rehires as spells, memberships placed on their spell | SF12 asserted |
| 16 | Identity normalisation | V and E numbers through HR's crosswalk; LRC as Lidmark | dictionary; R2 rows |
| 17 | Netting against gross | none on the call | not applicable |
| 18 | Dimensional units | monthly basic pay, per cent rates | rules section 2; scale extract |
| 19 | Code and status semantics | the register's Active and Deferred (asks only); the tracker holds approved rows only | the dictionary; the tracker's Notes sheet |
| 20 | Integerisation | none on the call | not applicable |
| 21 | Clause scope | amendment section 4 governs the budget line; section 2 who is enrolled | amendment |
| 22 | Forward window contents | every requisition's start month and grade for 2027 | the tracker ships all twelve months |

## Literal reader

Executed word for word, the prompt and the amendment fix the intake, the window, the pay, the default, the opt-out,
the match and the comparison basis; the literal reading that carries the cover's cancellations, or any observed
take-up, is the default path's easy method on the same literal estimand (14.5 million), not another reading of a term,
and every term's alternatives converge or are ruled out by a quoted sentence (SF1 to SF14). Pass.

## Oracles

None ties only under the golden. The register's join dates, HR's spells and the bordereau are inputs on every path; no
published take-up, opt-out rate or match forecast ships. The cover's curve over its own plateau corroborates the
clock only after both curves are built, which is the decisive step itself.

## Ask sheet

Asks, each on rows the call never reads (separation asserted in `checks.py`: the call's code reads no deduction line,
and no membership opened before 2019 sits on a 2019 to 2026 hire).

- Ask A, the employer match paid on the January to October 2026 payrolls by hospital (6 figures, nearest TNK 1,000).
  H18 home: the 2026 run-rate the budget line sits beside. Path: payroll_deductions_2025-11_2026-10.csv (10 columns),
  the plan rules' section 2 (pensionable pay across every post), the dictionary's assignment field. Primary device (D6,
  an event's quantity on every line it covers, silent): payroll computes the match on the person's pensionable pay
  across assignments and writes it on each assignment's ERM line, so the 440 or so staff holding a bank post in a month carry
  their match twice; nothing marks it, the bank post's ERM line equals its main post's exactly, and only a match
  recomputed from each line's basic pay and rate shows it. Hazards: Rendholm's April 2026 payroll ran on the 2025 scale, was reversed
  and run again (MAIN, REVERSAL and RERUN lines, all netting); V-numbers before the February 2026 cutover. Stops: every
  ERM line summed (each hospital 6.1 to 8.3 per cent high); the reversal lines dropped (Rendholm 9.7 per cent high);
  the first run only (Rendholm 0.3 per cent low); golden, each person's ERM once per payroll and run.
- Ask B, members whose membership began before 2019 and who were still active on 1 November 2026, by the hospital that
  paid them in October 2026 (6 figures, whole numbers). H18 home: the long-standing membership the plan's match
  already carries. Path: ledstrand_member_register_2026-10.xlsx (9 columns), hr_employment_history_2019_2026.csv, the
  October 2026 deduction lines, the dictionary. Primary device (D2, the record is the latest accepted, not the latest
  delivered, silent): Ledstrand's register is the snapshot after the October contribution file and before the month-end
  leavers file, so long-standing members whose employment ended on 31 October 2026 (6 to 11 a hospital, its
  October retirements among them) still read Active; only HR's contract end shows it. Hazards: register references in V-numbers; hospital_at_join in LRC; rehired members'
  later memberships under the same member number (anchoring on the member number's first membership counts them).
  Stops: the register's Active rows by the hospital at join (every hospital 6 to 11 high); anchored on the first
  membership (every hospital 1 to 4 high); golden.

Measured by: generator/ceiling.py

| Ask | Cracker (lands the call, runs the battery, applies the rules, nets the re-run, maps both numbers) | Figures kept | Verdict |
|---|---|---|---|
| A match paid 2026 by hospital | sums every ERM line of every run, exact duplicates removed (none) | 0 of 6 | miss |
| B long-standing active members by hospital | the register's Active memberships opened before 2019, LRC read as Lidmark | 0 of 6 | miss |
| call construction (hospitals and December contributors) | on the call | 7 of 7 | yes |

Mirror leakage: 0.0 per cent of ask weight (the mirror stops at R0 and takes both asks on their natural reads).
Pair ceiling: 38.6 ((65.3 + 12.0) / 2 on 38, 7 and 55), 47.3 if the cracker also cracks one ask's device.

## Leak review

`leak.py --asof 2026-11-09`: REVIEW, no LEAK. Each line answered:
- vch_savings_plan_amendment_2027.docx shares the call's words (budget, match, intake, FY2027, hospitals): the
  committee paper files the estimand (section 4) in the organisation's words; it carries no figure, rate, curve or
  method.
- The dictionary, the amendment and the rules carry three or four of the note's stump terms each (record, register,
  change, member; default, choice): ordinary words of a payroll dictionary, a plan's rules and an enrolment paper;
  none names a clock, a plateau, a take-up or an opt-out rate (`checks.py` R1 and R3c rows).
- staff_benefits_survey_2025.xlsx names the six hospitals beside its survey shares: a distractor (awareness of the
  match, satisfaction with reward), which ranks nothing on the FY2027 line.
- The export manifest's "from 2027-01-01" and the tracker's planned start dates run past the pull: the forward plan's
  own dates, which the estimand needs.

## Duplicate check

`guard.py heart task170` (2026-10-23, after the registration pull): WARN, the WARNs answered in `## Draw` item 9;
nearest text 0.05 (task133 v2, task255 v1). `guard.py surface task170`: eight pairs promoted, every one on the card
axes (gap time, pattern none with G7 among the generators, quantity_figure), none on text or a shared name. task169
and task171 (the neighbouring numbers): task169 closes one exit route for released people and task171 prices an
optional plan's take-up by each unit's own saving; neither has a default, a choice clock or a record that shows one
preference. task172 (a deadline's bite moving with a step), task132 (a replacement restarting a wear curve), task229
(a convex conversion of a daily mean), task161 (a pre-built stock drawn down at its usual share), task87 (an
exclusivity capping a delivered count) and task259 (a level carried to a reference date) share only the broad
labels; the card's `differentiation` carries one line for each the guard named. The surface tool still reads this
number's ledger row as architecture 1's retirement.

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Neutral |
|---|---|---|---|---|
| V-numbers and E-numbers | the HR and payroll cutover of February 2026 | HR, register, bordereau, deductions | joining on E-numbers alone (loses most joins, loud) | R2 asserted |
| LRC before the merger | the old org structure | HR, register, bordereau | a seventh hospital | pooled; not in the 2027 plan |
| rehires as new spells | HR | HR, register | first spells only | same call (SF12) |
| old policy numbers | Tarnmark's 2022 system change | bordereau | none on a count of cancellations | not read by the call |
| rate changes at April awards | Ledstrand | register | current rate for a joiner | same call (SF11) |
| the person's match on every assignment line | payroll | deductions | ask A device | ask only |
| reversed and re-run payroll | payroll | deductions | ask A hazard | ask only |
| the register before the month-end leavers file | Ledstrand | register | ask B device | ask only |

## Architecture 3 record (spent 2026-10-23)

Architecture 3, epidemiology-public-health / health-burden-impact-modeling (Forecasting), the main session's cell of
2026-10-23: an implementing non-profit's forecast, for its donor, of the Ombeni fever cases the March 2027 county-wide
distribution of LulaNet R repellent sleeping nets in Ruvari County (a fictional county in Kenya) would avert among the
people sleeping under them from April to December 2027. The golden carried the KINGA-5 trial's per-bite protection
(0.80, the five sites' efficacies over their own in-bed shares of exposure) through the county's in-bed share (0.36):
11,000 cases averted against the default path's 22,000 (the pooled efficacy, 56.7 per cent, carried unchanged). Built
to stage 3 (72676b37), judged DETERMINISTIC / APPROVE on zip 74728781, and spent at Gate F (the last line of
`## Tried and rejected`). The full architecture 3 note is in git at cc9ca581.

## Architecture 1 record (spent 2026-10-18)

Architecture 1, wave 7 (new), Forecasting lane (sathya8571), numbered from seed FC41. The seed (a national Central
Medical Stores filing its order of the adult first-line pack, tenofovir, lamivudine and dolutegravir in one tablet
(TLD), for the January to June cycle C7 at the quantification review, while the children of a paediatric scale-up five
years ago grow into it) was read at its header and Situation only. Its world, decision and quantity are kept. Its
mechanism (a certified cohort model and a register read off one field) is not used: no document vouches for any
model, the paediatric register ships as honest data, and the SOP's stock-out wording is replaced by a filed maximum
stock level so no distribution-against-mean step can decide the call. The pitfall is re-found from how a child moves
onto TLD: at the first clinic weighing that reads 30 kg or more, while a single clinic weighing scatters more than a
kilogram either side of the child's own growth line and the line rises about a fifth of a kilogram a month.

The country is fictional and never named in the pack: a southern African ministry of health whose Central Medical
Stores (CMS) buys antiretrovirals for a national programme of about 310,000 adults on TLD and 12,000 children on treatment,
in US dollars, every product on a six-month cycle (C7 is January to June 2027). The TLD order has two lines (SOP QP-04
4.3): line 1 for the patients of the programme's projection, net of the stock and the lots on order, and line 2,
funded by the paediatric grant, for the children under 15 at the count in the paediatric and adolescent ART register.
The register holds every child's clinic visits, weighings and regimens since January 2023: children diagnosed in
infancy (born 2005 to 2026, fewer each year as PMTCT improved) and the 2021-22 catch-up campaign's children (born 2011
to 2018, diagnosed at three to ten, the more stunted and the slower growing the older they were found). The 2026
edition of the national guidelines, effective 1 March 2026, lowered the weight from which a child takes TLD from 35 kg
to 30 kg and gave children who are well two or three months of medicines at a visit; by the 31 August count most
stable children were on two or three months.


The full architecture 1 note (default path, ladder, closure, asks and the stage 4 repair) is in git at f7ff3fb2.

## Tried and rejected
- A national adult forecast left to the solver (consumption trend or the cohort model of the seed): the adult projection's own spread swamps the children's wave, so no estimator family agrees to a step of the order; the adult part is filed as the programme projection.
- The children's growth on reference centile curves (CDC-shaped weight-for-age) as the truth: per-child functional forms fitted to scattered weighings disagreed by more than a step; growth is straight in kg from age six in this world, and the pooled weighings show it.
- A transient dolutegravir supply constraint as the driver: a dated cause whose effect is a step in the switch series, read off the date.
- An adult nowcast of undetected exits filled by multi-month dispensing: the driver of task231 again, and the adult trend is immune to it.
- A report-back device on the call's own rows: banned by the separation line.
- The wave's peak inside the window (the 2015-16 cohort born half a year earlier): every estimator agreed, but the trailing switch count and its linear trend landed inside the golden's step; the cohort was set later so the window holds the rise.
- Twelve-month per-child growth fits as the golden family's member: on scattered weighings their slopes carry so much error that the first passage is overstated by about a sixth in the forecast and by 30 to 50 per cent on every closed window; the family is the fits on each child's whole register history, which the closed windows validate within five per cent.
- A chart of the national months of deliveries and dispensing labelled at its peak: the peak month was a figure the cracker landed; the chart carries the table's 24 figures by region.
- Reissued codes closing in December 2025: the cracker's region route cancelled across the two cycles and kept Capital C5 and Central C5; the closures moved to March 2026 with larger, varied sites.
- A rival list that included the pooled-velocity and shrinkage constructions as members of the golden's family: after the infants' scatter fix they spread the family over 4,700 bottles, the 29.95 kg member four bottles inside the step's edge; each under-forecasts every closed window by 9 to 24 per cent while the register measures the slopes' spread between children, so they are reported as decisive-step routes, not members, and the step is centred on the per-child family.
- The empirical Bayes member with the between-child variance from unweighted moments: on this register it comes out at zero and shrinks every child to one mean slope; the DerSimonian and Laird estimate stands beside it, and both fail out of sample.
- The same scatter for an infant's weighing as for a 25 kg child's: readings under 3 kg and one below zero; a reading's scatter and clothing allowance shrink below 15 kg (an infant scale), which moved no switch and lowered the pooled scatter from 1.31 to 1.28 kg.
- New sites' customer accounts opened after their first delivery, and opening stock signed for before the registry's opening date: accounts now open two to six weeks before a site opens and its opening stock arrives on the day it opens.
- Other products' eLMIS lines with a loss larger than the stock on hand: the balance identity broke on 12 lines; the loss is capped at the stock.
- "Bottles it allows for patients aged 15 and over" as one figure: a reader could leave the maximum stock out of it; consumption and maximum stock are asked apart.
- Back-test percentages for every rival in the write-up: the band and trailing-count constructions vary with the bin and window a reader picks; the write-up bounds only the golden and the growth line.
- A delivery picked from two batches split on two different draws: its two lines summed to more or less than the quantity the facility received, so CMS's deliveries and the facility's eLMIS receipts disagreed on every such delivery; the split now shares one draw (the stream of later draws kept), which moved the asks' delivery figures and nothing the call reads.
- A family placed on its single choices' midpoint: two upward choices made together (the 29.95 kg threshold with 24-month lines) then sat 58 bottles inside the step's edge; the step is now centred on the span of the members and of the two compound choices that push the need furthest up and down.
- The whole C7 order at the nearest 5,000 bottles as the call (stage 4, round 1): the judge found the step unforced (the textbook per-visit prediction variance crossed its edge by 380 bottles, 24-month lines with it and the shrunk slopes by more), and the audit found the children's part 0.93 per cent of the order; the call moved to line 2, the children's part as its own line, in whole pallets.
- The repaired register with paediatric multi-month dispensing from July 2024 (most stable children on three months for two years): the lever between the growth line and the golden fell to 4,000 to 5,000 bottles while the family, with the prediction-variance and shrinkage routes in it, spread over 3,300, and the register's band rates, band chain and trailing counts sat inside any rounding wide enough to hold the family; the rollout moved to March to August 2026, with the guidelines.
- A stationary register with TLD at 30 kg throughout: every history-based route (band rates, the band chain, the trailing counts) measured the same flow the golden forecasts and landed in its pallet; the 2026 edition's change from 35 kg follows the WHO update of 2021 that many programmes adopted late, and it makes every rate measured on the register's history a rate of a band no longer in force.
- Line 2 rounded to 5,000 bottles with every prediction-variance construction in the family: the per-visit prediction variance on 24-month lines sits 2,271 bottles above the golden and the shrunk 24-month plug-in 813 below, so no 5,000-bottle step holds both a quarter step and one sigma from its edges; the order is placed in pallets of 84 cartons of 96 bottles, and a pallet holds them.
- The paediatric line the moving children leave (ABC/3TC with DTG 50 mg, 20 to 29.9 kg) as the call: its inflow at 20 kg is dosed visit by visit, so the noisy first passage moves only its outflow, the lever is the same number of child-months as on the children's TLD line, and the line carries two transitions to forecast.
- The children who move onto TLD in the window as the line alone (about 16,000 bottles): a pallet is half the line, so the call would be two pallets against one.
- A season of 0.2 kg peaking in May, and a velocity ramp from 2 to 6 years: windows opening at the season's peak under-forecast by a fifth on every route, and the all-weighings lines of 9- and 10-year-olds under-projected their June weight by 0.3 kg; the season is 0.08 kg peaking in September and growth is the child's own line from five and a half.
- The campaign's size changed by redrawing the world: every child's draws moved with the size and the family's centre jumped; every child of the campaign's largest size is drawn and the first 7,040 kept, the size set so the family's centre sits at the pallet's.
- The scatter of a 10 to 15 kg child's weighing shrunk like an infant's: the pooled scatter fell below the near-band children's by 0.07 kg and the MAD member drifted; infant scales stop at 10 kg.
- A crossing-age rule left out of the asserted misses: 11 of its 24 binnings, those that move every child already past the crossing age at the next visit, land in the pallet; they are reported, and the binnings that wait for each child's age are asserted to miss.
- The whole C7 TLD order as the call: the children's switch timing moved it by under 1 per cent (the default 25,000 bottles short on 2.69 million), so the 5,000-bottle step was finer than the estimator family could hold and the lever was immaterial to the order.
- Line 2 in whole pallets (8,064 bottles) as the call: the lever between the default and the golden is 1.03 pallets, so the default misses by one pallet and P(both) is about 0.2, twice the bar; routes that land the pallet without the decisive step include a chosen lead of 3 to 6 months, a margin of 0.75 to 1.25 kg, the last weight at 28 kg, age 12 with the backlog and a weighing every month; architecture 1 is spent on strength and the number needs a re-root.
- Architecture 2 in pharmacology-pharmacoepidemiology-safety / population-pharmacokinetics-exposure-response (2026-10-19, never carded): twenty in-cell candidates screened before any card, every one in one of four graves (a filed pharmacokinetic formula executed: renal scaling, accumulation, Michaelis-Menten, weight-band edges, design and sample-size calls; a fit whose estimator family forks the graded figure: covariates inside the NLME, effective half-life on sparse troughs, a ceiling-censored Emax, variance components; the field's textbook route as the golden: actual dosing histories, within-patient trajectories, dialysis calendars, covariate-vector resampling, per-patient rates for an extended interval; or a reading or a rejected shipped number: unbound fraction, eta-shrinkage off a shipped post-hoc table, BLQ hiding the bottom), with the confounded exposure-response card blocked as `causal_design` by the window and the dose-level IOV call at 11 to 25 per cent against a 30 per cent bar. It is the verdict task171's own screen recorded for this cell (`task171/DESIGN_NOTE.md` line 42); the full table is in the build's scratch `r170/STATE.md`. The cell is spent for this slot.
- Architecture 2 in banking-credit-financial-risk / deposit-liquidity-behaviour (2026-10-19, never carded): composition is the deposit field's native mechanism and `composition_mix` is out this round (task137 and task166 drew it; three of the four banking forecasting builds on file carry it), so every heterogeneity candidate died on the ban (surge layers, hot against core money, primary relationships, dormant accounts, holder age, product migration, a relationship-tenure clock, burnout of rate-sensitive savers, the last two `population_selection` besides). The cards' own methods are the textbook route the readers take (cumulative and asymmetric betas, with level dependence in card 2's own note and the error-correction lag in card 1's "lagged repricing"; cohort decay; first cumulative breach; behavioural maturity), and the bank's own pricing reaction recovered from its history (funding need, a swap ceiling) is a withheld rule.
- Deposit cell, the rest: floors, notice periods, payment limits, insured-limit aggregation, early-repayment schedules and product terms are rule application or a reading, and the unconstrained periods hand over the floor-free beta; net against gross runoff is task89, a left-truncated cohort after a migration task133, loan-linked and refinance-ability exits task166, maturity retention task137, in-flight transfers by provider route task181, shared collateral across funding sources task106 and a rival-level crossing task115; lumpy repricing moves about 5 per cent of the expense and a hold on the core share fails the variance-only screen.
- Deposit cell, the three drafts scored with `guard.py nearest` (0.06 to 0.07, none flagged by text): re-timing the outflow on each saver's own notice for a cut notified to everyone on one day is task162's insight (a forward trigger alignment no recorded instance had, so the record's weekly profile understates the peak); a leaving hazard set by the interest given up (balance times gap) against a fixed bother of moving reads the same as any switching-cost churn, and its forward cell is either in the record (one balance-by-gap table lands it) or empty only by a selection that is composition; topping up to a raised deposit guarantee limit from the bunching at the old one is the public-finance bunching estimator (the swap test reads it as tax kinks) and its response rests on one past limit change.
- Rebuild of 2026-10-23 in banking-credit-financial-risk / expected-credit-loss-provisioning (never carded), the one candidate taken to code: a credit union's CECL allowance on its auto loans after a used-vehicle price surge, each defaulting loan's recovery forecast as its own vehicle's market value at its sale against a balance sized at its own purchase market, so the record's severities (vehicles bought at or below the market they sold at) carry nothing to the vehicles bought at the top. On the clean truth (40,655 open loans, 7,947 closed sales, three seeds) the golden family (five fits of resale over purchase price on the index at sale against the index at purchase, the ratio's coefficient free or fixed at one, point, smeared and residual-integrated) sat within 1.1 per cent of the truth and the rivals missed by a third or more (pre-surge severity 33 to 34 per cent low, the latest year's recovery rate scaled by the forecast index change 39 to 44, pooled severity 47, a valuation on the purchase price without the purchase market 64). It died on the shipped-proxy screen: the practitioner's macro-linked severity, the recovery rate regressed on the index's change over a holding horizon, filed 4.6 per cent high on a 12-month change where the fall sits in the forecast and 7 per cent low on a 24-month change where the fall comes before the report, because for loans that default 12 to 24 months after purchase the index's change over that horizon is the purchase-to-sale ratio; the horizon is a free knob whose range spans the golden, so some member lands in any world. A hedonic valuation on the vehicle's segment and age with no price information also landed (2 to 8 per cent high), and with the fall before the report the surge vintages' own realised severity shows the effect.
- Expected-credit-loss cell, the rest on paper: rate resets and interest-only, promotional and grace-period expiries (task166's due units, task177's exposure end, task46's and task157's cohort crossing a step); a collections, extension, repossession or court-order change that closes one route for distressed loans, and negative equity routing distressed borrowers into default instead of a sale (task169's driver both times); drawdown before default capped by the limit (task168's cap completion); cure, re-ageing and delinquency momentum (conditioning on the account's own history is a stratification, the opponent's first group-by, `stumping` Part 6); guarantees, first-loss covers, forward-flow debt sales, deficiency and repossession statutes, the CECL collateral-dependent expedient and line-freeze policies (each a filed rule executed); indexed mortgage loan-to-value (the field's own indexation is the textbook route); a distributed lag from a county panel (the field's lag reflex, task160's readers landed a lag, and it moves only a 12-month window under staging rules); a cut in the state's unemployment-benefit duration turning more job losses into defaults (task172's cap moving into the bulk of a duration distribution, the exceedance share read straight off the record's spells); sector-linked defaults at a select-employee credit union and a sponsor's plant closure (composition, the metro or sector forecast a proxy or a signpost, the closure a dated cause); dealer price packing, electric-vehicle depreciation and force-placed insurance (each a column to stratify on); a retained first-loss tranche (its expected loss turns on the spread of ten vintages' losses). The cell's core estimation mechanics (survival to date, competing exits, the remaining-life base) are task133's.
- Architecture 3 (epidemiology-public-health / health-burden-impact-modeling, the LulaNet R campaign's cases averted through the in-bed share of exposure) spent at Gate F at stage 4 on zip 74728781: the judge returned DETERMINISTIC / APPROVE with no fix, and blind reader A took the decisive step in its own words ("net protection only works while the person is in bed, so for each KINGA-5 site I computed the share of person-exposure to An. ruvariensis bites that falls in bed (survey in-bed/indoors by half hour x hourly indoor/outdoor landing rates). Trial protective efficacy divided by 0.97 net use, regressed through the origin on that share gave per-user efficacy = 0.824 x share in bed"), filing 12,000 against 11,000 and 22 against 21 per cent with 6 of 7 sub-counties landed (score_reader FAIL as landed), and took ask B ("outreach clinics' Jan-Mar 2026 rows dropped because parent hospitals' Jan-Mar returns already include outreach OPD"), 7 of 14 ask figures. Why: the trial report shipped each site's hourly biting and sleeping tables beside its widely varying efficacies, which laid the transport model out on one page, and a behaviour-time overlap is the field's standard entomological reasoning for nets, so it fails the library test at medium effort; an in-row comment is no silent device.
- Cell choice after architecture 3 (2026-10-23, on paper, before the card): the console merger of two control-room operators' alarm streams (misses rise with concurrent load) replays the two journals onto one clock, so the record is replayable; a 12-hour shift roster's errors from a time-on-duty curve beyond eight hours rests on selected overtime and the field's fatigue index is the textbook route; a voting-age or compulsory-voting change carries a transport of turnout from a pilot province, architecture 3's shape; a party's withdrawal under an electoral pact is a transfer rule executed; a deductible cut extrapolates a truncated severity below its truncation point (the parametric family forks) and a deductible rise is the limited expected value, field-standard; a tempo-adjusted birth forecast is the Bongaarts-Feeney correction; select mortality wearing off after a scheme closes is task107's intake moving to the experienced rate; mortality displacement after an excess-death year is a dated cause read off the record; a removed second check is task169's route closure; a staggered decision-aid rollout is a difference-in-differences the rollout log lays out; flat dosing on an Emax curve is the popPK cell's grave.
- The 2027 tracker with its cancelled and re-issued requisitions kept beside the approved rows: counting every row moved
  the call by about 8 per cent on a status reading, mess on the call's path that is not neutral; the tracker exports the
  approved plan only.
- Automatic enrolment with a common clock and no corroborating default on file (prototype `proto3/ae.py`): the golden's assumption that hires who prefer not to join choose on the joiners' clock rested on no record, so a judge could read it as an unfiled method; the income protection cover, auto-enrolled since 2019, was added as the clock's corroboration, its own cancellations drawn on the same law and independently of the plan's choice, so no hire's two choices share a date a reader could join on.
- The FY2027 line to the nearest TNK 100,000 with hospitals to the nearest 10,000 (prototype `proto3/ae3.py`, `family.py`): complete-cohort estimators of the join curve sat 1.4 per cent from Kaplan-Meier on a 2,600-hire five-year cohort, outside both bins; the group grew to about 11,400 staff with longer tenures (the five-year cohort to 3,964), the family narrowed to 0.85 per cent, and the line is rounded to TNK 500,000 with hospitals to 100,000, the plan's monthly multipliers set so every member lands in every bin.
- The share who have chosen by the sixth payroll as a critical component: the cover's clock read 71.4 against the join curve's 72.1 per cent, across a whole per cent; the twelfth payroll (89.8, 90.2, 89.8 and 89.9 across the family) holds.
- Architecture 4 (psychology-behavioral-science / decision-making-computational-behavioral-modeling, Vindeholm County Hospitals' FY2027 match on its first auto-enrolled intake) spent at stage 4 on zip 0c216157: the determinism judge returned NOT_DETERMINISTIC (underspecified_objective), SEND_BACK. The pack holds no record of auto-enrolled savers, so the golden's premise that every hire chooses on the voluntary join clock and settles at the 43 per cent join level is a behavioural assumption the files never state, while the one default-with-opt-out record shipped (Tarnmark's Auto basis, a 16.7 per cent five-year cancellation level) carried as the opt-out clock gives TNK 14.3 million and about 2,300 contributors, and nothing shipped rules it out; the 2026 match ask left the bank pool (cost centre 950) unfiled. Blind reader C took that route exactly: a Kaplan-Meier on hires since 2019, all hospitals pooled, the stop event the IPC auto-cover cancellation or leaving, everyone at 3 per cent, filing 14.5 million and 2,300 against 11.5 million and 1,600; it summed every ERM line (ask A 0 of 6) and took ask B 6 of 6 on a leaver filter and the main-post cost centre, ordinary hygiene. The miss was a fork, not a stump: an unidentified behavioural response, whose method forks, and shipping a peer scheme's auto-enrolled record would only turn the stump into a transfer of that record's level.
- Fifth-cell search after architecture 4 (2026-10-23, the main session's rule: the lever from a structural estimand choice, never from a behavioural response the data cannot identify; the cells other rebuilds hold excluded). One candidate on code, `proto5/ip.py`: a group income protection policy whose deferred period falls from 13 weeks to 4 in 2027 (actuarial claims-frequency-severity), the expected benefit days per new claim stitched from the employer's absence spells to day 91 and the insurer's claims beyond it; the lever was 65 per cent either side (HR spells alone 66 per cent low with the transfers at day 91 read as returns, the insurer's claim durations on the new claims 64 per cent high) with the stitch unique, but HR closes each absence at day 91 by its transfer to the claim and a careful reader joins the two or multiplies the share reaching day 91 by the claims' durations, which is the golden: dead on the careful-path screen.
- Fifth-cell paper screens, each dead before code: a delivery fleet's claims read on delivery stops rather than kilometres (claims-frequency; the lever is capped by the parcel growth at 11 to 19 per cent, and a split by the circumstance code is a careful reader's group-by); a per-occurrence deductible replacing a per-claim one (the treaty term is read, so the step is semantics, and grouping by an hours clause is rule application); amount-weighted against lives-weighted mortality for a pension scheme (mortality-longevity; under 1 per cent on a year's payments, 3 to 6 per cent on the liability, inside the amount-weighted estimator's own noise); cohort against period annuity values and Lee-Carter fitting choices (the card's textbook route, and the fits fork); the carry-over of a late-2026 price step into 2027's annual-average inflation (time-series-macro; a monthly path forecast and averaged carries it, the natural route); Easter moving into March 2027 (seasonal adjustment; a month's lever of 5 to 6 per cent and the Easter window forks); a budget quantile from archived forecast errors (forecast evaluation, drawn three times; a filed back-test organ, and archive errors over model intervals is the careful route); an excavation's summer exposure to extreme rain (climate-weather-extremes; seasonal maxima are read directly and a GEV on thirty maxima forks); peak-week claims from storm clustering (a few events a year leave the event rate's estimator open); an aggregate stop-loss on a compound sum (the stop-loss premium by simulation is the card's pin); batch compounding in a hospital pharmacy cutting error events (human reliability; the batch task's error probability was never observed, a transport of behaviour); a sick-pay limit extended over absences recorded as certificates (linking contiguous certificates is hygiene a careful reader runs, and the longer pay changes behaviour); a notifiable disease's case definition widened to probable cases (reading the definition is semantics, counting the tracing log rule application); journey injuries made compensable under workers' compensation (lodging of excluded claims is suppressed by behaviour, and the road-injury scheme's commute flag is a field read).

## Retired

task170 retired on 2026-10-19 under the author's rule for this round (a number that dies in its second new cell retires),
every card kept. Architecture 1 (the C7 order's line 2, children switched to TLD on the first passage of noisy
clinic weighings over 30 kg) was spent on strength at stage 4 on 2026-10-18: with the call in whole pallets the
first-passage lead was 1.03 pallets and routes with a chosen lead landed it. The redraw's first cell,
pharmacology-pharmacoepidemiology-safety / population-pharmacokinetics-exposure-response, died on paper (twenty
candidates, each a filed formula executed, a tail count or a textbook route); the second, banking-credit-financial-risk /
deposit-liquidity-behaviour, died before any card (efced35). The lesson the cells share: where the field's native
mechanism is composition or a filed formula, the judgment beyond the card is either a reading or a rule, and nothing
the data settle is left to carry the call.

## Rebuild (2026-10-23)

Reopened by the author for a from-scratch rebuild under the rule that no number stays retired, in
banking-credit-financial-risk / expected-credit-loss-provisioning. No draw was carded: the one candidate taken to code
(auto-loan recoveries forecast on each vehicle's purchase market) died on the shipped-proxy screen, and the rest died on
paper (`## Tried and rejected`, last two lines). The number is paused at stage 1 for another cell; the v1 card is
unchanged and no lineage was moved, since no new draw was registered.

The main session then assigned epidemiology-public-health / health-burden-impact-modeling the same day, and
architecture 3 (`## Draw`) was carded there: the repellent net campaign's cases averted, the trial efficacy carried
through the county's in-bed share of exposure.

The architecture 3 death was recorded the same day (cc9ca581), and the main session left the next cell to this
session under four conditions: the forward window changes the process in a way not on file; the record is not
replayable, not one group-by and not a field-standard correction; the materials of the decisive step do not sit side
by side in one shipped report; and no cell in this note or the siblings' `## Rebuild` sections. Architecture 4 was
carded in psychology-behavioral-science / decision-making-computational-behavioral-modeling (`## Draw`, item 12 for
why): Vindeholm County Hospitals' FY2027 employer match on its first auto-enrolled intake, the opt-in record read as a
preference and a clock.

Architecture 4 was spent at stage 4 the same day (the judge's NOT_DETERMINISTIC, `## Tried and rejected`), and the
main session left a fifth cell to this session with the lever to come from a structural estimand choice. No candidate
held: one measured dead on code and fourteen more on paper (`## Tried and rejected`, last lines). No card registered
past v4, which stays the card's identity marked spent; PAUSED at stage 1 for the main session to assign another cell.
The number is never retired.
