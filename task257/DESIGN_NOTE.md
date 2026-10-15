# task257 design note

Architecture 1, drawn 2026-10-15 (wave 2 of sathay3012, Descriptive lane). The seed DA07 gave the number only.

## Draw

- **Card:** `cards/task257.json`, registered 2026-10-15. Psychology & Behavioral Science, task type
  psychometric-measurement-scale-validation (how many dimensions an engagement survey's items measure), objective
  Descriptive & Distribution Analysis; shape 07 (a grid: the 30 items against the sub-scales they report under);
  decision structural_verdict (the 2027 dashboard's sub-scales and their items); gap objective (what a sub-scale has
  to be: a distinct dimension of employees' views, not a cluster of item scores); pattern none, G2 then G16; Gate G
  method_or_model_selection; strategy grain_or_unit (a five-point answer is an ordered category, not a score).
- **World:** Brackenmere Markets, a fictional grocery chain in Ontario, Quebec and New Brunswick (about 21,600
  employees in 148 stores, three distribution centres and a head office), runs a yearly engagement survey through
  Kestrava Listening, a fictional survey vendor, in English and French. The 2026 survey ran 14 to 27 September with 30
  agreement items on a five-point scale. From February 2027 a dashboard gives every store and department manager
  their team's sub-scale scores, and each sub-scale below the company line asks the manager for an action plan, so
  every sub-scale the dashboard carries is work for about 1,400 managers. The executive team settles the 2027
  structure before the dashboard is built (forum executive_team, forcing event launch_or_rollout); the people
  analytics team's survey reporting standard defines a sub-scale as a distinct dimension of employees' views that the
  items measure, each item reporting under one.
- **People** (guard.py names --geo Canada --seed 257; Christine Huffman skipped for a first name used in an older
  build): Alexander Copeland, head of employee listening (role family programme_officer); Maria Murray, people
  analytics lead, who wrote the reporting standard; Melissa Vang, Kestrava's account manager, who keeps the export and
  codebook.
- **Data-native sentence:** Brackenmere's tools items describe what nearly every employee has (a scanner that works,
  the schedule posted two weeks ahead) and are answered agree or strongly agree by more than nine in ten, while its
  growth items describe what few store employees have (a written development plan, a path to promotion) and are
  answered disagree by most; a five-point answer is a coarse reading of a continuous view, so items that share a
  lopsided distribution correlate with each other through the shared ceiling or floor of their categories as well as
  through what they measure, and only correlations estimated for the underlying views (polychoric) separate the two.
- **Guard:** WARN three_rules.strategy_risk (grain_or_unit), answered by the analyst test: every code, key and rule
  read correctly still leaves the item scores as numbers from 1 to 5, and the easy route (correlate the scores, keep
  the dimensions that beat random data) files five sub-scales. WARN repeat.gate_g and overuse.gate_g
  (method_or_model_selection, 8 of the last 12): how many dimensions a scale measures is settled by the estimator the
  responses' level of measurement requires, a method choice by nature; the driver shares nothing with task456 (three
  imperfect records) or task457 (a forward remuneration estimate), nearest driver 0.05.
- **Pairing and shape:** the field's own analysis decides (scale validation counts a scale's dimensions on the
  correlation structure its items' level of measurement calls for), the objective is how the employees' views are
  composed (Descriptive), and the call is a grid of 30 items against their sub-scales (shape 07). Criteria: the count,
  30 item placements, the chart's parts, and the asks' unit-level figures.
- **Sources, one line each.** `guard.py mechanisms --objective descriptive-distribution`: task253 spent a latent
  level seen through noisy averages (shrinkage) and task256 a reference survey's conditional distribution carried to a
  roster; neither counts dimensions or touches the measurement level of rating items. task450 (test equating through
  anchor items) and task459 (emissions at a fixed output) spend other measurement problems. The client's
  psychometric pattern 2 (Likert items need polychorics) gives the family; this build's own version is the
  dimensionality count, where the lopsided items manufacture two sub-scales rather than biasing a loading.
- **Seed:** DA07 (a parcel carrier's van tiers by duty-cycle fuel economy) gave the lane's number only: its world's
  natural step, the duty-cycle mix, reads as the target's own definition once the estimand is filed, so the step
  would be semantics; the world is redrawn, as task255 and task256 redrew theirs.
- **Forward facing:** the call fixes the 2027 dashboard's structure, a window not yet open; the deciding quantity is
  the dimensionality of the 2026 responses, the survey the 2027 instrument repeats unchanged.

## Default path

1. Map the French questionnaire's item codes to the 30 master items through the codebook, keep the last submission
   under each invitation token and drop Kestrava's test tokens.
2. Reverse-score the four negatively worded items and set "does not apply to me" and blanks to missing.
3. Correlate the 30 item scores (Pearson), take the eigenvalues and keep the dimensions that stand above what random
   answers of the same size give (parallel analysis; Kaiser's eigenvalue-above-one rule and the scree agree).
4. Rotate the solution with that many factors and place each item under the factor it loads on most.

Ends on: five sub-scales (workload, tools, leadership, belonging, growth), the tools items and the growth items each split from the dimension they measure
Golden: three sub-scales (resources: the workload and tools items; leadership: the manager and recognition items; connection: the belonging and growth items)

## Stump sentence

The default path correlates the 30 five-point item scores as numbers and keeps five dimensions, splitting the tools
items and the growth items into sub-scales of their own; the step that lands it there is treating answers that pile
up at the top of the scale (tools) and at the bottom (growth) as interval scores, whose correlations carry the items'
shared lopsidedness as a dimension of its own, so only correlating the responses as ordered categories of the
employees' underlying views (polychoric correlations) shows the three dimensions the items measure.

## Three rules

Task type: psychometric-measurement-scale-validation (Psychology & Behavioral Science), which serves Descriptive & Distribution Analysis in the client taxonomy.
Domain test: The deciding quantity is the number of latent dimensions a psychological scale measures, counted on the correlation structure the items' ordinal level of measurement requires, which is scale validation's own work.
Swap: "How many distinct groups do the 30 product lines form, and which lines belong to each?" keeps a count and a grid but loses the rating item, the category threshold and the latent view behind an answer, so the polychoric step has nothing to act on and the task no longer reads the same.
Layer 1: A vendor export in long form with a header block, French and English versions in different item orders joined through the codebook's crosswalk, negatively worded items to reverse-score, a does-not-apply code, resubmissions under one invitation token, the vendor's test tokens, store and department codes renamed in a July reorganisation, an effective-dated HR roster and UTC timestamps against the stores' survey window; each is what these systems produce and none is placed to be caught.
Layer 2: estimation_fit, estimation that fits the data: five-point answers are coarse readings of continuous views, and with items piled at opposite ends of the scale the correlation estimator decides how many dimensions the items show.
Decisive step: Correlating the 30 items as ordered categories of underlying continuous views (polychoric correlations) before counting the dimensions that stand above random data, because Pearson correlations of the lopsided tools and growth items carry their shared ceiling and floor as two extra dimensions.
Not semantics: Every code, key and crosswalk read correctly leaves each answer a number from 1 to 5, the five-point scale is exactly what it says, and correlating those numbers still keeps five dimensions; no field, code or definition says how the items are to be correlated.
Not rule application: The reporting standard defines a sub-scale as a distinct dimension of employees' views and places each item under one, and leaves the analysis to the analyst; no filed rule names an estimator or a retention test, so executing every stated rule still leaves the count to the correlations an analyst chooses.
Analyst test: A strong analyst who cleans the export and reads every item and rule correctly correlates the item scores, keeps the dimensions that beat random data, and reports five sub-scales (tools and growth split off as their own), the default path's answer (executed on the generator's clean responses in checks.py).
Estimand: The number of distinct dimensions of employees' views that the 30 items of the 2026 survey measure among the employees who answered it, each item placed under the one dimension it measures most (survey_reporting_standard_2025.pdf, sections 2 and 3).
No decoy: Nothing is planted: no earlier dashboard, vendor scoring guide, theme tag or memo states a number of sub-scales, the questionnaire shows the items in one order without headings, and no record is copied, withheld or written to carry the wrong answer.
No certified replay: No certified or published structure exists for a method to reproduce; the count is forced by the responses' own distribution, where every retention test run on latent correlations keeps three.
Lesson: Rating items whose answers pile up at one end correlate through their shared lopsidedness, so a dimension count on Pearson correlations finds difficulty factors (Bernstein and Teng's spurious multidimensionality); the analyst estimates the latent correlations first, and no build on file teaches the level of measurement of rating items.

## Tried and rejected

- DA07's world (van tiers by duty-cycle fuel economy): the duty-cycle mix either contradicts a literal "fuel economy over the year" estimand or, filed as "on the duty cycle", becomes the reading of a definition; dropped before any ladder.
- A disease registry that enrolled its prevalent cases at launch (survival from diagnosis with delayed entry): the same insight as task133's left truncation (units seen only if they survived to the takeover); dropped at the draw.
- Competing deaths in a cumulative incidence (Aalen-Johansen against 1 - KM): spent by task134's first architecture.
- A random follow-up of non-respondents weighted as a second phase, and a two-stage household survey whose fresh listing breaks self-weighting: both weight each unit by its own inclusion probability, task452's insight drawn the day before; dropped.
- Hospital mortality adjusted only for conditions present on admission: the onset flag is a column, so the decisive step is a one-line filter (schema-readable); dropped.
- Usual intake below a requirement from one or two recall days: task253's latent level seen through noisy averages; dropped.
- Informative dropout in weekly symptom scores (completers against a mixed model): multiple imputation lands on the golden without the insight, and missing-at-random against not-at-random stays open; dropped.
- Cross-country satisfaction corrected with anchoring vignettes, and the Double Jeopardy benchmark for brand loyalty: the vignette items and the "for its size" estimand each hand over the method; dropped.
- Factor retention alone (parallel analysis against eigenvalue above one on a clean scale): the scree's elbow and parallel analysis both reach the golden by reflex; kept only as the retention step after the decisive one.
