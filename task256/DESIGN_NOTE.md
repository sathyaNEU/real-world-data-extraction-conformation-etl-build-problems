# task256 design note

## Draw

- **Card:** `cards/task256.json`, registered 2026-10-13. Human Factors & Ergonomics, task type
  anthropometric-design-fit, objective Descriptive & Distribution Analysis; shape 01 (each configuration in or out
  against the 95 per cent line, the cheapest in); decision pick_one_of_n; gap population; G14 then G6; Gate G
  method_or_model_selection; strategy composition_mix (the reference survey's accommodation does not fit this
  workforce, whose build differs on the two measurements its own records hold).
- **World:** Tamarack Valley Regional Transit Authority, a US regional transit authority running its buses from three
  divisions with 2,110 bus operators. Its 2027 order of battery-electric buses from Halvard Coach Works carries
  one operator workstation configuration, chosen from the eight Halvard's fit report quotes (A to H), each with a
  fit envelope on five body dimensions and a price per bus. The Authority's operator workstation standard specifies
  the lowest-priced configuration that fits at least 95 per cent of its bus operators. The Authority knows its
  operators' bodies only through the stature and weight recorded at their DOT medical examinations, kept by two
  occupational health providers either side of a 2021 changeover; the five dimensions are described by a reference
  survey of working adults (Brennard Institute for Workplace Design, 2012) through within-sex means, standard
  deviations, percentiles and correlations. The board adopts the FY2027 capital budget, the order and its
  configuration included, on 19 November 2026 (forcing event budget_or_appropriation); the Authority's Bus Specification
  Committee approves the configuration the standard specifies at its meeting of 29 October 2026 (forum
  committee_or_panel).
- **People** (guard.py names --geo us --seed 256; Amy Hawkins skipped for a first name used in task130): Tracy
  Reynolds, vehicle procurement manager in Fleet Engineering (role family procurement_lead); William Roberts,
  Halvard's application engineer; Kelsey Sanchez, occupational health coordinator; Donald Mcguire, chief operating
  officer.
- **Data-native sentence:** the Authority knows its operators' bodies only through the stature and weight its DOT
  medical examinations record, and its operators are heavier and more varied in stature than the workers the
  reference survey measured; the five dimensions a workstation must fit are known only through the survey's
  within-sex correlations with stature and weight, so each operator's chance of fitting has to be carried from the
  survey through both measurements, the spread around the prediction kept, and averaged over the roster.
- **Guard:** PASS with WARNs. overuse.shape (01 in three of the last twelve): the decision is a pick against a line,
  each configuration in or out, so the criteria come from the configurations. repeat.gate_g and overuse.gate_g
  (method_or_model_selection after task255 and task501): the mechanism is the carry of a reference distribution to a
  target population through conditional relationships, against task255's truncated and censored likelihood and
  task501's transmission model; the vocabulary's nearest honest key. repeat.question_form (which, task501): a pick
  of one of eight configurations asks which. test.same_driver_older against task54 is differentiated on the card.
  At the heart screen task187 (drawn earlier the same day in another session) held utility_or_infrastructure,
  board_of_directors and operations_director, and task501 executive_team: the card now carries government_agency (a
  regional transit authority is a public agency; overuse WARN answered here), committee_or_panel and procurement_lead,
  each honest for this world; heart WARN only.
- **Pairing and shape:** the field's own analysis decides (multivariate accommodation of a user population, the
  reference survey carried to the users), the objective is the share of a distribution inside a box, and the call
  is a pick against the standard's line (shape 01). Criteria: eight configurations, each with its accommodation
  share (8) and its 2027 order cost (8); the call, the runner-up below the line and its gap (3); the chart's named
  parts (5); two files (2); the asks (sheet below). 26 before the asks.
- **Sources, one line each.** `guard.py mechanisms --objective descriptive-distribution` (27 builds): none carries a
  reference distribution to a target population through conditional relationships; task253 counts units whose noisy
  sample averages fall below a line and shrinks them, whose mirror (a share counted from predicted values) is only a
  rung here, never the decisive move; task255 fits a size curve through truncation and censoring; task114 and
  task126 rebuild units from records. `layer2-rigor-patterns.md` has no Human Factors patterns (the domain README
  says so), so the family comes from `two-layer-task-design.md` ("the right comparison group", "the data's real
  structure"): estimand identification, the users' own distribution in place of the reference's. The seed DA06 gave
  the number only.
- **Forward facing:** the call is the configuration of buses built for 2027, a window not yet open; the deciding
  quantity is the accommodation of the operators on the roster the day the configuration is chosen, because the
  standard measures it there (the workforce that will drive the 2027 buses is that workforce plus hires the
  standard does not ask the Authority to predict).

## Default path

1. Read the standard (a configuration fits an operator when all five fit dimensions lie within its envelope;
   accommodation is the share of the bus operators on the roster of 30 September 2026 it fits, each as measured at
   the latest DOT physical; the lowest-priced configuration at 95 per cent or more) and the fit report's eight envelopes and prices per bus.
2. Count the bus operators on the roster by sex (full-time and part-time, every duty status).
3. Take the five fit dimensions' within-sex means, standard deviations and correlations from the survey report: one
   multivariate normal per sex.
4. Each configuration's accommodation: the probability that all five dimensions lie in its envelope, by sex,
   weighted to the roster's sex mix.
5. Specify the lowest-priced configuration at or above 95 per cent.

Ends on: Configuration B
Golden: Configuration G

## Stump sentence

The default path computes each configuration's joint accommodation for the survey's own workers at the roster's sex
mix and ends on Configuration B (95.6 per cent on that basis), because the Authority's operators, heavier and more
varied in stature than the survey's workers, never enter the model; carrying the survey to the operators through
stature alone ends on Configuration E (95.1 per cent on that basis), and counting each operator by their predicted
dimensions on Configuration C (95.2); only each operator's conditional distribution of the five dimensions given
stature and weight, averaged over the roster, files Configuration G (96.4 per cent; E 93.2 and F 92.9, the two
nearest cheaper configurations).

## Three rules

- **Task type:** anthropometric-design-fit in Human Factors & Ergonomics, serving Descriptive & Distribution
  Analysis: the call reads the share of a user population's joint body-dimension distribution that lies inside each
  configuration's fit envelope.
- **Domain test:** the deciding quantity is multivariate accommodation, the share of the Authority's operators whose
  five correlated fit dimensions all lie within a configuration's envelope, estimated the way the field does it for
  users measured only on stature and weight: the reference survey's within-sex joint distribution carried to each
  user through its conditional relationships, the spread around the prediction kept, averaged over the users.
- **Swap:** with an electricity network's nouns ("which transformer configuration serves 95 per cent of our feeders,
  from a reference survey of load shapes and the two readings each feeder's meter records") there is no within-sex
  body-dimension structure, no stature and weight from a medical examination and no fit envelope on five correlated
  dimensions to carry them into; the estimator and the decision stop making sense.
- **Layer 1:** two occupational health providers' exports either side of 1 July 2021 (one encounter per row with
  drug and alcohol tests among the physicals, heights as feet-and-inches text or decimal inches, weights in pounds,
  dates in two formats), employee numbers formatted differently in the roster and each export, several examinations
  per person and examinations of mechanics, supervisors and former staff, the survey and the fit report as PDF tables
  in millimetres and kilograms; for the ask, a work-order export that prints each job's labour on every part line, a
  fleet roster of the buses in service whose fleet numbers were reused from retired series, a disposals list and a
  retrofit campaign log. Nothing is placed to be caught; every main-path item leaves the call where it is when
  mishandled (asserted).
- **Layer 2:** estimand_identification: the accommodation of the Authority's own operators, the survey's joint
  distribution carried to each operator through its within-sex conditional distribution given the operator's stature
  and weight, in place of the survey's own workers; it moves the call from B (or C or E) to G.
- **Decisive step:** carrying the reference survey's joint distribution of the five fit dimensions to each operator
  through its within-sex conditional distribution given the operator's recorded stature and weight, the residual
  spread kept, and averaging each operator's probability of fitting over the roster.
- **Not semantics:** every field and definition reads plainly (the standard's fit and accommodation, the envelopes,
  the survey's dimensions, heights in inches and weights in pounds), and an analyst who reads them all still files B
  by modelling the survey's workers, E by carrying the operators through stature alone or C through their predicted
  dimensions: no field, code or definition says how the survey's description reaches the operators.
- **Not rule application:** the standard files the population, the fit, the line and the price rule and no model of
  the operators' bodies; executing every filed rule with the survey's tables files B, and carrying the survey to the
  operators through their stature and weight is the step no rule performs.
- **Analyst test:** a strong analyst who cleans both exports, takes each operator's latest stature and weight, reads
  the standard and the fit report correctly and computes each configuration's joint accommodation from the survey's
  within-sex normal model files Configuration B for the survey's workers at the roster's sex mix (the default path's
  Ends on: Configuration B), Configuration E when the operators are carried through stature alone, or Configuration C
  when each is counted by their predicted dimensions; none of A to F fits 95 per cent of the Authority's operators.
- **Estimand:** the standard (tvrta_standard_ES-12_operator_workstation.pdf) fixes accommodation as the share of the
  Authority's bus operators a configuration fits (all five fit dimensions within its envelope), the bus operators
  being every employee in the Bus Operator job classification, full-time or part-time, on the roster of 30 September
  2026 whatever their duty status, each as measured at the latest DOT physical examination, and the specification as the lowest-priced configuration in the fit report whose
  accommodation is 95 per cent or more.
- **No decoy:** nothing is planted: no memo, draft, briefing or stakeholder figure states an accommodation or ranks
  the configurations; the survey's tables describe its own workers truly and the fit report states envelopes and
  prices only.
- **No certified replay:** no certified or published figure is reproduced by the method: no accommodation figure,
  fit trial result or measured operator dimension ships.
- **Lesson:** an anthropometric reference describes its own sample; a workforce known only by stature and weight has
  its accommodation carried through the reference's within-sex conditional relationships, operator by operator, or
  the reference's share stands in for a different population. No build on file carries a reference distribution to
  a target population through conditional relationships.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, each dimension on its own (A) or the female 5th to male 95th percentile (B) | the standard's fit clause says all five together | no | the textbook design range | none | no | no | readable |
| R1, the survey's workers at the roster's sex mix (B) | the standard names the Authority's operators, no model | the roster's sex column | the opponent's default: reweight to the visible mix | none | no | no | readable |
| R2 and R3, carried through stature alone (E) or counted by predicted dimensions (C) | no sentence names stature, weight or a carry | heights and weights are ordinary exam columns | a solver who carries uses stature, the anthropometric scaling variable, or plugs in a regression | none | no | no | silent |
| G (decisive), each operator's conditional distribution given stature and weight, averaged (G) | no sentence names a conditional distribution, a residual or the operators' build | no flag or marker; weight never appears in the fit envelope | every reflex lands elsewhere: the sex mix files B, stature alone E, a plug-in C, the visible heavy build (the column and the deep track) E | nothing scores a fit: no accommodation figure, fit trial or measured operator ships | the battery sees nothing | a joint normal integral per operator, no ratio or subtraction | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | bus operators | every Bus Operator employee, full-time or part-time, on the 30 September 2026 roster, whatever the duty status | operators on active duty only | same call | same call; and standard 3.2: whatever their duty status |
| SF2 | fits | all five fit dimensions within the envelope together | each dimension at 95 per cent on its own | Configuration A | standard 3.1: every one of the five within the envelope |
| SF3 | envelope limits | inclusive, an open side unlimited | exclusive | same call | same call: continuous dimensions; standard 2.3 for the open side |
| SF4 | an operator's stature and weight | the latest DOT physical on or before 30 September 2026 | the mean or the earliest of the operator's physicals | same call; the shares move (G 96.7 or 96.9) | standard 3.2: each operator as measured at the operator's latest DOT physical examination on or before that date (filed after the judge's first pass) |
| SF5 | fit dimensions | as the survey defines and measures them, unclothed | shod or clothed | none stated | standard 2.2 and the fit report's envelope note: the survey's dimensions |
| SF6 | price | the price per bus in the fit report | an order total | same order | standard 3.3: price per bus in the fit report |
| SF7 | at least 95 per cent | 95.0 per cent or more, unrounded | rounded first | same call | same call: no configuration within half a point of 95.0 (asserted) |
| SF8 | the roster date | 30 September 2026 | the date the order is placed | not in the pack | standard 3.2: 30 September of the year before the order's model year |
| SF9 | sex | the roster's sex | the providers' sex field | same call | same call: the two agree for every operator (asserted) |
| SF10 | the survey's distributions | normal within sex with the tabulated means and standard deviations | the empirical percentiles | same call | the survey report: its percentiles are computed from the normal distribution with the mean and standard deviation shown |
| SF11 | heights and weights | inches times 25.4 to millimetres, pounds times 0.45359237 to kilograms | none | same call | the exports' column headings and the survey's units |
| SF12 | accommodation of an operator whose dimensions are unmeasured | the operator's probability of fitting, averaged | counting operators whose probability passes one half | Configuration C | the standard counts a share of operators; counting operators above one half is the predicted-dimension rung's error (asserted) |
| SF13 | the survey's correlations | within sex as tabulated | pooled across the sexes | not tabulated | the survey report tabulates within-sex correlations only |
| SF14 | numerical integration | any method to four decimals | Monte Carlo with 200,000 draws | same call | same call (asserted within 0.1 point) |
| SF15 | stature at the physical | measured without shoes, as the survey's | a shoe allowance taken off | not licensed | the HR readme: both providers measure height without shoes |
| SF16 | weight at the physical | as weighed, light clothing | an allowance taken off for clothing | same call; the shares move | standard 3.2: each operator as measured at the latest DOT physical examination |
| SF17 | the latest DOT physical examination | the latest physical (DOTPE, DOT PHYSICAL), the visit that measures height and weight | a recertification (DOTRC, DOT PHYSICAL - RECERT), the latest DOT visit of nine operators, read as the latest examination | same call, every share unchanged at one decimal | standard 3.2 names the DOT physical examination, and the HR readme lists recertifications apart from DOT physical examinations; C1: no recertification carries a height or weight, and leaving the nine out moves no share (asserted) |

## Ladder

| Rung | Model of the operators' fit dimensions | A | B | C | E | F | G | Call |
|---|---|---|---|---|---|---|---|---|
| R0a | each dimension on its own, the survey's sex-mixed marginals at 95 per cent | 97.3 | 97.5 | 97.3 | 97.3 | 98.4 | 99.6 | A (its weakest dimension) |
| R0b | the survey's female 5th to male 95th percentile on every dimension | short | covers | short | short | covers | covers | B |
| R1 | the survey's workers, joint, at the roster's sex mix | 92.6 | 95.6 | 95.3 | 96.3 | 98.0 | 99.2 | B |
| Rind | the survey's marginals multiplied as if independent | 91.3 | 95.2 | 94.5 | 95.7 | 97.8 | 99.1 | B |
| R2 | each operator carried through stature alone | 90.8 | 94.2 | 93.5 | 95.1 | 96.5 | 98.4 | E |
| R3 | each operator's predicted dimensions given stature and weight | 86.1 | 86.5 | 95.2 | 97.2 | 95.6 | 97.8 | C |
| G | each operator's conditional distribution given stature and weight | 79.4 | 82.3 | 90.1 | 93.2 | 92.9 | 96.4 | G |

- **Position:** the golden is the seventh of eight configurations by price; rung 1 takes the second. Every
  correction walks one way (up the price list) and only the decisive move reaches G.
- **Margins:** G at 96.4 per cent (1.4 points over the line); E 93.2 and F 92.9, the two nearest cheaper
  configurations, 1.8 and 2.1 points under; D 82.6 (D's value the generator's, figures.json).
- **Worth:** the decisive move (R1 to G) takes B from 95.6 to 82.3 per cent and moves the call five configurations up
  the price list; R2 and R3 move it one or two.
- **Grid:** each single-error cell files a quoted configuration cheaper than G: A, B, B, B, E, C, and the qualitative
  reading of the heavy build (the column and the deep track) files E.
- **Convergence asserted:** the latest physical against the mean of each operator's physicals; operators on active
  duty only; operators whose latest physical is within two years only; weights less a kilogram of clothing; Monte Carlo
  with 200,000 draws per sex against the quasi-Monte Carlo integral; and a bivariate normal fitted to the operators'
  statures and weights (the Pearson and Lawley carry), which files G with E at 94.2 and F at 93.4, half a point or
  more short.
- **Flip:** G would fail only if its accommodation fell 1.4 points; E would pass only if it rose 1.8.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every Bus Operator employee on the 30 September 2026 roster, any duty status; no member unobserved | filed literally, standard 3.2; C1 on duty status (SF1) |
| 2 | Unit of account | the operator | the standard's share of operators |
| 3 | Attribution window | the roster date | standard 3.2 |
| 4 | As-of dating | each operator's latest DOT physical examination on or before 30 September 2026 | standard 3.2 (SF4); C1 against recertifications (SF17) |
| 5 | Version basis | the roster as exported on 30 September 2026 | one export |
| 6 | Denominator | all counted operators | standard 3.2 |
| 7 | Weighting | one weight per operator | the share of operators |
| 8 | Window length | none for the call; the ask's work orders 2021 to 2025 | filed in the ask |
| 9 | Boundary inclusivity | 95 per cent inclusive; envelope limits inclusive | C1: no configuration within half a point of the line, every share 0.02 points or more from a rounding edge; continuous dimensions (SF3, SF7) |
| 10 | Rounding path | accommodation unrounded until compared, shown to one decimal | SF7 |
| 11 | Tie-break | none: one lowest-priced passing configuration | prices distinct |
| 12 | Maturity and censoring | none | a roster at one date |
| 13 | Order of operations | units converted before conditioning | C1: conversion is linear |
| 14 | Row order | none | C1 asserted over shuffled operators |
| 15 | Duplicate resolution | an operator's physicals in both exports at the changeover are one examination | C1: duplicates carry identical stature and weight (asserted) |
| 16 | Identity normalisation | employee numbers across the roster and the two exports | the exports readme; every counted operator matched (asserted) |
| 17 | Netting against gross | none | none |
| 18 | Dimensional units | millimetres and kilograms from inches and pounds | SF11 |
| 19 | Code and status semantics | job classification and encounter type | the roster's classification; only DOT physical examinations carry stature and weight, recertifications C1 (SF17) |
| 20 | Integerisation | none | none |
| 21 | Clause scope | standard 3.1 for fit, 3.2 for the population, 3.3 for the pick | filed per clause |
| 22 | Forward window contents | the 2027 buses carry the configuration; the population is the roster the standard names | standard 3.2 |

## Literal reader

Executed word for word, the standard fixes accommodation as the share of the Authority's bus operators (the Bus
Operator employees on the 30 September 2026 roster, any duty status, each as measured at the latest DOT physical
examination) whose five fit dimensions all lie within a configuration's envelope, and the pick as the lowest-priced
configuration at 95 per cent or more; the operators' fit dimensions are unmeasured, the survey report is the only
description of them, and the exports record each operator's stature and weight, so the literal estimate of that share
is each operator's probability of fitting under the survey's within-sex joint normal given the operator's stature and
weight, averaged over the roster: Configuration G at 96.4 per cent. Every row of the fork table violates a quoted
sentence or converges on G; the easy answers (B, C) come from an easier model of the same operators' share, not from
another reading.

## Oracles

- The survey's percentiles and correlations: inputs of every rung; they tie to nothing.
- The fit report's envelopes and prices: inputs; no accommodation figure ships.
- The operator comfort survey (distractor): operators' ratings of today's workstations by bus series; it scores no
  configuration and no envelope.
- The workers' compensation claims (distractor): operators' claims by body part; no fit figure.
- The ask layer: no maintenance key performance figure, no labour summary and no fleet-size total ships, so nothing
  ties under one handling of the work orders only.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops (lazy delta) | Realism |
|---|---|---|---|---|---|---|---|---|
| A, each option's 2021 to 2025 maintenance cost, bus-years and cost per bus-year | 15 | a measure every candidate carries that the call does not turn on (its parts) | the board weighs what each option costs to keep up beside its price | D6: the export prints the job's labour hours and cost on every part line of a work order | D7 (fleet numbers of the retired 2011 and 2012 series reused for the 2024 and 2025 series, so every work order joins); D5 (the retired buses' months in the disposals list only); D2 (the 2024 pedal retrofit campaign: the fleet roster shows today's options); D8 (closing month, filed) | work orders (number, bus, component, closed date, bill to, part cost, labour hours, labour cost), fleet roster (number, accepted, options), disposals (number, series, accepted, disposed, options), retrofit campaigns (bus, option, completed), maintenance notes; 5 files, 15 columns | labour summed over lines: every option's cost and rate high; current roster only: pedal and riser bus-years low, their rates high; today's options for every month: pedal bus-years high; the answer | a fleet system flattening work-order labour onto part lines; a transit authority reusing a retired series' fleet numbers |
| B, each configuration's twelve-year cost per bus | 8 | a measure every candidate carries that the call does not turn on | the board sees each configuration's price beside its upkeep | inherits A's devices | as A | A's path and the fit report's prices | any error in A moves every configuration but A | the authority's own life-cycle line |
| C, each configuration's accommodation and the chart | 8 and 5 chart parts | the construction | the call's own table | none | none | the golden model | R1 to R3 values | the fit report's layout |

- **Main population zero-counts:** no row of the work orders, fleet roster, disposals or retrofit log sits in the
  roster, the exports, the survey, the standard or the fit report's envelopes the call reads; the call and every
  component are unchanged with the ask files deleted (asserted).
- **Hazard table:** D6 moves every option's cost and rate (A) and every configuration but A (B); D7 and D5 move the
  pedal and riser bus-years and rates (A) and every configuration with them (B); D2 moves the pedal bus-years and rate
  (A) and B, D, F, G and H (B).
- **Referee:** none; the maintenance notes define bus-years and the closing month and adjudicate no device.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A option costs (5) | labour summed over the part lines | high for every option | miss |
| A bus-years (5) | the fleet roster's buses with today's options | pedal and riser wrong; column, deep track and header right | miss |
| A cost per bus-year (5) | the two above | high for every option | miss |
| B twelve-year costs (8) | price plus twelve of A's rates | high for every configuration but A | miss |
| C accommodation and chart | the golden's construction | right | outside |

Mirror leakage: about 17 per cent of the ask weight (the three column, track and header bus-years and configuration
A's zero twelve-year cost, 4 of 23 ask figures; the mirror's accommodation values are R1's).
Pair ceiling: 38 (the cracker at about 54 with the call, its accommodation table and four ask figures, the mirror at
about 22).

## Build record

- Generator: `world.py`, `analysis.py`, `records.py`, `docs.py`, `golden.py`, `checks.py`, `verify.py`, `build.py`,
  `postprocess.py`; `python3 task256/generator/build.py` builds the pack, the goldens, `metadata.json` and
  `generator/figures.json`, runs the checks and the independent verifier, rebuilds into scratch for the byte
  comparison and cuts `target.zip`.
- Pack: 14 files in 4 formats (pdf, xlsx, csv, md): the standard, Halvard's fit report, the survey's summary tables,
  Human Resources' roster (2,437 staff, 2,110 bus operators), Ostrander's encounters (19,073 rows) and Fernhill's
  visits (17,398 rows, Ostrander's first half of 2021 among them), the fleet roster (460 buses), disposals (134),
  retrofit campaigns (87), the operator-area work orders (28,746 lines), two exports readmes; distractors the 2023
  comfort survey (715 responses) and the workers' compensation claims (602).
- Numbers: the per-operator conditional normal is integrated by quasi-Monte Carlo on one fixed Sobol set (2^15
  points, within 0.0004 points of 2^18); the verifier integrates each operator by Genz's algorithm from its own
  parse of the PDFs and exports and agrees to 0.01 point; every share is 0.02 points or more from a rounding edge;
  the fit trials' readings trim five envelope limits by a millimetre (A, C, F and G eye height, H knee clearance).
- Gates: 176 assertions (the three-rules analyst test on clean truth, SF1 to SF17, the convergences, the ask's
  devices, the goldens); the verifier from target/ alone; two builds byte-identical with BLAS pinned to one thread;
  figures_check 70 figures; precut 49 checks; voice-check PASS; scrub audit clean on target and golden; leak.py
  REVIEW, no LEAK (the quoted prices are stated inputs, the certificate expiries forward dated by nature); guard
  surface 2 pairs promoted for adjudication (not run: author-triggered), heart WARN (org family, shape and Gate G
  overuse, answered in the Draw).

## Judge record

- Pass 1 (stage 4): DETERMINISTIC, FIX_NOW (optional). The isolated thread recomputed the 2,110 operators (1,522 men,
  588 women), all eight shares (G 96.41, E 93.21, F 92.91), the five options' costs and bus-years and the eight
  twelve-year costs from the bundle alone; the plug-in files C and the survey's workers B, the intended easy routes;
  the call held under active-only, full-time-only, earliest physical, mean of physicals and a 4 lb clothing
  allowance. The finding: no shipped sentence said "latest", so the graded one-decimal shares moved (G 96.3 to 96.9)
  under those conventions, which SF4's "same call" did not close for the shares. Gate G statistical_rigor,
  analytical_non_defect, no surface read, no sole data defect; Gate H domain pass, layers pass, decisive step
  analytical.
- The fix, in the generator and at authority, not in the prompt: standard 3.2 now takes each operator as measured at
  the operator's latest DOT physical examination on or before the roster date, which closes earliest and mean of
  physicals (SF4) and a clothing allowance (SF16); "physical examination" rather than "medical examination" keeps
  the nine operators whose latest DOT visit is a recertification (no height or weight) on their latest physical, and
  leaving them out moves no share at one decimal (SF17, asserted). Every graded figure is the judged one to the last
  digit. The clause points a reader at the operators' own measurements, which thins the survey's-workers rung (B)
  for a careful reader; the plug-in (C) and the stature carry (E) are untouched, and the decisive step is unchanged.
- Pass 2 (the one re-judge, on the rebuilt pack): DETERMINISTIC, APPROVE (determinism_check_report_pass2.md). The
  thread took each operator's latest DOT physical (DOTPE or DOT PHYSICAL only) from 3.2 and recomputed every share,
  the operators, the five options' costs and bus-years and the twelve-year costs; B 95.6 and C 95.2 reproduced as the
  rivals. Gate G method_or_model_selection, analytical_non_defect, no surface read, no sole data defect; Gate H
  domain pass, layers pass, decisive step analytical; no mismatch with the note or the card. Two optional notes. No
  sentence says to average each operator's probability of fitting: that is the decisive step, left to the analysis
  (filing it would make the step rule application). The bus-month rule's first day: a disposal or a fitting dated on
  a 1st moved the pedal set's and the riser's bus-years by 0.1 to 0.3 under another reading of "on the first day".
- After pass 2: no acceptance, disposal or fitting in the fleet files falls on a 1st any more (one recorded on a 1st
  is recorded on the last day of the month before, which the rule counts the same way), so every reading of the first
  day gives the same bus-months (asserted under four readings). Only the three fleet files changed; figures.json and
  the goldens are the judged ones byte for byte. No re-judge: the disposition was APPROVE, the change is data on the
  ask's path only, and no estimand, rule or sentence the call reads changed.

## Leak record

- leak.py REVIEW, no LEAK: the option names are the configurations' own; the documents carry ordinary domain words,
  none naming a carry, a conditional distribution or the operators' build (asserted in checks.py); Fernhill's later
  dates are certificate expiries.
- Reader (fresh copy of prompt.txt and target/): no decisive-step sentence, no ranking file, no answer-like figure;
  question 5 read the standard's population and fit clauses to the golden's estimand and could not say the
  configuration without solving; question 6 analytical; every REVIEW line harmless; one mild realism note on the
  comfort survey (a distractor), left as it is.
- Reader 2 (after standard 3.2 took each operator as measured at the latest DOT physical examination): no
  decisive-step sentence (the nearest, 3.2, leaves open how two measurements become five dimensions), no ranking
  file, no answer-like figure; question 5 read 3.2 to the golden's estimand; question 6 analytical; every REVIEW line
  harmless; the standard's revision history and the fit report's table read slightly tidy but plausible, left as
  they are (no note added to a document the call reads).

## Pre-ship check

- Call: specify Configuration G ($4,450 per bus), 96.4 per cent of the 2,110 bus operators on the 30 September 2026
  roster (1,522 men, 588 women); E 93.2 and F 92.9, the nearest cheaper configurations.
- Default path: the survey's workers at the roster's sex mix file B (95.6); a carry through stature alone E (95.1);
  each operator counted by predicted dimensions C (95.2); a bivariate normal fitted to the operators' statures and
  weights G (convergent).
- Gates: 176 assertions with the three-rules block and SF1 to SF17; the independent verifier from target/ alone; two
  builds byte-identical; figures_check 70 figures; precut 49 checks; voice-check PASS; scrub clean on target and
  golden; leak.py REVIEW, no LEAK; guard surface 2 pairs promoted (author-triggered, not run); heart WARN (org family,
  shape and Gate G overuse, answered in the Draw).
- Deliverables: workstation_configurations_2027.xlsx (the eight configurations with price, share and the line, the
  five options' maintenance, the twelve-year costs, notes) and operator_accommodation_2027.svg; target.zip from the
  final rebuild, 14 files.
- Leak: two isolated reads, no decisive-step sentence, no ranking file, question 6 analytical.
- Judge: pass 1 DETERMINISTIC, FIX_NOW (the measurement record, filed in standard 3.2); pass 2 DETERMINISTIC, APPROVE.
- Card current: answer, spine rows, stump and driver at the built values.

## Tried and rejected

- DA06 seed world (a mapping foundation's grant baseline, volunteer stickiness net of organised editors from
  published tables): the decisive step reduced to subtracting one published table from another, a population
  filter the 10/10 rules ban as the decisive step; redrawn at the draw, never registered.
- First anthropometric draft with the decisive rung on predicted values (counting operators whose regression-predicted
  dimensions fall inside the envelope against each operator's conditional distribution): the insight is task253's
  mirror (a share from per-unit point estimates whose spread is not the population's), so it stays one rung and the
  decisive move is the carry through stature and weight.
- First guard check: ban.artifact (filed_standard after task501), ban.forcing_event (purchase_order_or_contract after
  task450) and test.same_driver_older (task54) blocked; context artifact none, forcing event budget_or_appropriation,
  task54 differentiated.
- First envelope set (the standard workstation's popliteal range from 365 mm): the per-operator carry filed G, but a
  bivariate normal fitted to the operators' statures and weights (the Pearson and Lawley carry, a defensible way to
  move a survey to a new population) put E at 95.1 per cent, because the operators' weights are skewed and the normal
  fit thins the heavy tail the abdominal limit meets; the range now starts at 371 mm, so both carries file G and every
  cheaper configuration sits half a point or more short under both (asserted).
- A single readme for both export families: the fleet maintenance measures sat in a file the call reads; split into an
  HR and occupational health readme and a fleet maintenance readme, so no document the call reads carries the ask.

