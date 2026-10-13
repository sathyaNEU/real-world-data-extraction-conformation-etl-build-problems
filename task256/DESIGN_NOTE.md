# task256 design note

## Draw

- **Card:** `cards/task256.json`, registered 2026-10-13. Human Factors & Ergonomics, task type
  anthropometric-design-fit, objective Descriptive & Distribution Analysis; shape 01 (each configuration in or out
  against the 95 per cent line, the cheapest in); decision pick_one_of_n; gap population; G14 then G6; Gate G
  method_or_model_selection; strategy composition_mix (the reference survey's accommodation does not fit this
  workforce, whose build differs on the two measurements its own records hold).
- **World:** Tamarack Valley Regional Transit Authority, a US regional transit authority running its buses from three
  divisions with about 2,100 bus operators. Its 2027 order of battery-electric buses from Halvard Coach Works carries
  one operator workstation configuration, chosen from the eight Halvard's fit report quotes (A to H), each with a
  fit envelope on five body dimensions and a price per bus. The Authority's operator workstation standard specifies
  the lowest-priced configuration that fits at least 95 per cent of its bus operators. The Authority knows its
  operators' bodies only through the stature and weight recorded at their DOT medical examinations, kept by two
  occupational health providers either side of a 2021 changeover; the five dimensions are described by a reference
  survey of working adults (Brennard Institute for Workplace Design, 2012) through within-sex means, standard
  deviations, percentiles and correlations. The board adopts the FY2027 capital budget, the order and its
  configuration included, on 19 November 2026 (forcing event budget_or_appropriation).
- **People** (guard.py names --geo us --seed 256; Amy Hawkins skipped for a first name used in task130): Tracy
  Reynolds, manager of fleet engineering; William Roberts, Halvard's application engineer; Kelsey Sanchez,
  occupational health coordinator; Donald Mcguire, chief operating officer.
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
