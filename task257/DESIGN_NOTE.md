# task257 design note

Architecture 1, drawn 2026-10-15 (wave 2 of sathay3012, Descriptive lane). The seed DA07 gave the number only.

## Draw

- **Card:** `cards/task257.json`, registered 2026-10-15. Psychology & Behavioral Science, task type
  psychometric-measurement-scale-validation (how many dimensions an engagement survey's items measure), objective
  Descriptive & Distribution Analysis; shape 07 (a grid: the 30 items against the sub-scales they report under);
  decision structural_verdict (the 2027 dashboard's sub-scales and their items); gap objective (what a sub-scale has
  to be: a distinct dimension of employees' views, not a cluster of item scores); pattern none, G2 then G16; Gate G
  method_or_model_selection; strategy grain_or_unit (an answer is an ordered category of a view, not a score).
- **World:** Brackenmere Markets, a fictional grocery chain in Ontario, Quebec and New Brunswick (about 21,400
  employees in 148 stores in 12 districts, three distribution centres and a head office), runs a yearly engagement
  survey through Kestrava Listening, a fictional survey vendor, in English and French. The 2026 survey ran 14 to 27
  September with 30 items: 14 statements on a five-point agreement scale and 16 yes or no questions about the
  employee's recent experience (the tools questions, the growth questions, and one in each other area). Employees
  answer through a personal link, a store kiosk or, in stores without a kiosk, a printed form. From February 2027 a
  dashboard gives every store and department manager their team's sub-scale scores, and each sub-scale below the
  company line asks the manager for an action plan, so every sub-scale the dashboard carries is work for about 1,400
  managers. The executive team settles the 2027 structure before the dashboard is built (forum executive_team,
  forcing event launch_or_rollout); the people analytics team's survey reporting standard defines a sub-scale as a
  distinct dimension of employees' views that the items measure, each item reporting under one.
- **People** (guard.py names --geo Canada --seed 257; Christine Huffman skipped for a first name used in an older
  build): Alexander Copeland, head of employee listening (role family programme_officer); Maria Murray, people
  analytics lead, who wrote the reporting standard; Melissa Vang, Kestrava's account manager, who keeps the export and the
  questionnaire's fielding copy.
- **Data-native sentence:** Brackenmere's tools questions ask about what nearly every employee has (a working scanner,
  a schedule posted two weeks ahead, correct pay) and are answered yes by about 94 per cent, while its growth questions
  ask about what few employees have (a written development plan, a nomination for a lead role) and are answered yes by
  about 6 per cent; a yes or no answer is a cut through a continuous view, and the Pearson (phi) correlation of two
  cuts is capped by how far apart their splits sit, so questions that share a lopsided split correlate with each other
  far more than with the agreement statements measuring the same view, and only correlations estimated for the
  underlying views (tetrachoric and polychoric) separate the shared split from the shared content.
- **Guard:** WARN three_rules.strategy_risk (grain_or_unit), answered by the analyst test: every code, key and rule
  read correctly still leaves each answer a number (1 to 5, or yes and no as 1 and 0), and the easy route (correlate
  the answers, keep the dimensions that beat random data) files five sub-scales. WARN repeat.gate_g and overuse.gate_g
  (method_or_model_selection, 8 of the last 12): how many dimensions a scale measures is settled by the estimator the
  answers' level of measurement requires, a method choice by nature; the driver shares nothing with task456 (three
  imperfect records) or task457 (a forward remuneration estimate), nearest driver 0.05.
- **Pairing and shape:** the field's own analysis decides (scale validation counts a scale's dimensions on the
  correlation structure its items' level of measurement calls for), the objective is how the employees' views are
  composed (Descriptive), and the call is a grid of 30 items against their sub-scales (shape 07). Criteria: the count,
  30 item placements, the chart's parts, and the department ask's 24 figures.
- **Sources, one line each.** `guard.py mechanisms --objective descriptive-distribution`: task253 spent a latent
  level seen through noisy averages (shrinkage) and task256 a reference survey's conditional distribution carried to a
  roster; neither counts dimensions or touches the measurement level of survey items. task450 (test equating through
  anchor items) and task459 (emissions at a fixed output) spend other measurement problems. The client's
  psychometric pattern 2 (ordinal items need polychorics) gives the family; this build's own version is the
  dimensionality count, where lopsided yes or no items manufacture two sub-scales (Bernstein and Teng's difficulty
  factors) rather than biasing a loading.
- **Seed:** DA07 (a parcel carrier's van tiers by duty-cycle fuel economy) gave the lane's number only: its world's
  natural step, the duty-cycle mix, reads as the target's own definition once the estimand is filed, so the step
  would be semantics; the world is redrawn, as task255 and task256 redrew theirs.
- **Forward facing:** the call fixes the 2027 dashboard's structure, a window not yet open; the deciding quantity is
  the dimensionality of the 2026 answers, the questionnaire the standard fixes for 2026 and 2027.

## Survivor anatomy

Actor: the deciding property, how far each yes or no question's split sits from every other item's and how that caps its correlations, has no column: the export holds one answer per row and the questionnaire each question's wording and type, and the cap is a relation between one item's split and every other item's that no file stores (no yes share, threshold or level of measurement ships).

Link: the signal is read by setting each pair of items' two-way table against the cut through a bivariate normal view it implies, a comparison across items that no key offers and no sentence invites; the standard files what a sub-scale is and names no correlation, and the questionnaire numbers the items without grouping them.

Reflex: the field's named method for counting a scale's dimensions, parallel analysis on the items' Pearson correlations with Kaiser's rule and Velicer's MAP beside it, sits at rung 0 and files five sub-scales with the tools and growth questions split off.

Back-test: what a solver checks the easy route against agrees with it: Kaiser's rule, MAP and random data at the mean and at the 95th percentile all keep five on the Pearson correlations, every extraction and rotation puts the tools and the growth questions on factors of their own with clean loadings, and the scree shows a second elbow at five; no record in the pack scores a Pearson count against a latent one.

Second use: every file the decisive step reads is the call's own (the export, the submissions and the questionnaire); the latent correlations read no file the Pearson count does not, so nothing in the pack exists for the decisive step alone.

Shock: the two extra dimensions read as content facets (tools, growth) that the questionnaire's wording makes look natural, never as an anomaly; the golden's groups are no interval of any shipped sort, since each mixes statements, which carry no yes share, with yes or no questions from opposite ends of the splits.

Pins: the standard files the WHAT (a sub-scale is a distinct dimension of employees' views that the items measure, each item under the dimension it measures most, who a respondent is, the questionnaire fixed for 2026 and 2027); no filed sentence names a correlation, an estimator, a retention test, the level of measurement or the lopsided questions, and deleting 2.1 unforces the count's definition, never the estimator.

## Default path

1. Map the French questionnaire's item codes to the 30 items through the questionnaire's French numbers, keep the last submission under
   each token, drop Kestrava's test tokens, and join the kiosk sessions to the employee who signed in.
2. Reverse-score the four negatively worded statements, code yes as 1 and no as 0, and set "does not apply" to
   missing.
3. Correlate the 30 items (Pearson, pairwise), take the eigenvalues and keep the dimensions that stand above what
   random answers of the same size give (parallel analysis; Kaiser's eigenvalue-above-one rule and Velicer's MAP
   agree).
4. Rotate the solution with that many factors and place each item under the factor it loads on most.

Ends on: five sub-scales (workload, tools, manager, growth, and belonging with recognition), the six tools questions and the six growth questions each split from the dimension they measure
Golden: three sub-scales (resources: the workload statements and the tools questions; manager and growth: the manager statements and the growth questions; connection: the belonging and recognition items)

## Stump sentence

The default path correlates the 30 answers as numbers and keeps five dimensions, five sub-scales (workload, tools,
manager, growth, and belonging with recognition) with the six tools questions and the six growth questions each split
from the dimension they measure; the step that lands it there is correlating yes or no answers that nearly everyone
gives one way (yes to tools, no to growth) as scores, whose correlations are capped by their lopsided splits, so the
shared split stands as a dimension of its own, and only correlating every answer as an ordered category of an
underlying view (tetrachoric and polychoric correlations) shows the three dimensions the items measure.

## Three rules

Task type: psychometric-measurement-scale-validation (Psychology & Behavioral Science), which serves Descriptive & Distribution Analysis in the client taxonomy.
Domain test: The deciding quantity is the number of latent dimensions a psychological scale measures, counted on the correlation structure the items' categorical level of measurement requires (tetrachoric and polychoric correlations, then a retention test), which is scale validation's own work.
Swap: "How many distinct groups do the 30 product lines form, and which lines belong to each?" keeps a count and a grid but loses the survey item, the category threshold and the latent view behind an answer, so the latent-correlation step has nothing to act on and the task no longer reads the same.
Layer 1: Kestrava's export in long form under a header block, French and English questionnaire versions in different item orders joined through the questionnaire's French numbers, negatively worded statements, a does-not-apply code, resubmissions of a personal link, Kestrava's test tokens, kiosk sessions logged under the pre-July store numbers with employee numbers as typed, printed forms recorded when Kestrava keys them, and UTC timestamps against each site's local close; each is what these systems produce and none is placed to be caught.
Layer 2: estimation_fit, estimation that fits the data: yes or no answers and five-point answers are coarse cuts through continuous views, and with questions split far to opposite sides the correlation estimator decides how many dimensions the items show.
Decisive step: Correlating the 30 items as ordered categories of underlying continuous views (tetrachoric and polychoric correlations) before counting the dimensions that stand above random data, because Pearson correlations of the lopsided tools and growth questions carry their shared splits as two extra dimensions.
Not semantics: Every code, key and crosswalk read correctly leaves each answer a number, yes and no are exactly what they say, and correlating those numbers still keeps five dimensions; no field, code or definition says how the items are to be correlated.
Not rule application: The reporting standard defines a sub-scale as a distinct dimension of employees' views and places each item under one, and leaves the analysis to the analyst; no filed rule names an estimator or a retention test, so executing every stated rule still leaves the count to the correlations an analyst chooses.
Analyst test: A strong analyst who cleans the export and reads every item and rule correctly correlates the answers, keeps the dimensions that beat random data, and reports five sub-scales (workload, tools, manager, growth, and belonging with recognition), the default path's answer (executed on the generator's clean answers in checks.py).
Estimand: The number of distinct dimensions of employees' views that the 30 items of the 2026 survey measure among the employees who answered it, each item placed under the one dimension it measures most (survey_reporting_standard_2025.pdf, sections 2 and 3).
No decoy: Nothing is planted: no earlier dashboard, vendor scoring guide, theme tag or memo states a number of sub-scales or groups the items, the questionnaire shows the items in one order without headings, and no record is copied, withheld or written to carry the wrong answer.
No certified replay: No certified or published structure exists for a method to reproduce; the count is forced by the answers' own distribution, where every retention test run on latent correlations keeps three.
Lesson: Yes or no questions that nearly everyone answers the same way correlate through their shared split, so a dimension count on Pearson (phi) correlations finds difficulty factors; the analyst estimates the latent correlations first, and no build on file teaches the level of measurement of survey items.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the answers correlated as numbers (default) | none: the standard defines a sub-scale as a distinct dimension and names no estimator | the answers are codes | yes: every tool's default correlation | none | no | no | readable |
| R1 the questionnaire's six areas | none: no headings, theme tags or earlier sub-scales ship | the item wording | yes: reading the items | none | no | no | readable |
| R2 rank correlations, straight-liners dropped, complete cases, one language | none | no | yes: the opponent's corrections for skewed or careless answers | none | yes: the battery drops straight-liners | no | readable |
| R3 (decisive) the 30 items correlated as ordered categories of underlying views (tetrachoric and polychoric) before the dimensions are counted | none: the standard files the WHAT, and nothing names the level of measurement, an estimator, a retention test or the lopsided questions | yes and no read as yes and no by every analyst; no column marks the lopsided questions or a latent view | no: the extra dimensions read as content facets (tools, growth), so nothing looks wrong on the default path | no prior structure, scoring guide or published sub-scales; the vendor's benchmark carries item favourability only | the battery (duplicates, ranges, straight-liners, missing codes) never measures the correlation estimator | 435 latent correlations, each a maximum-likelihood fit to a two-way table, then the eigenvalues | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "sub-scale" | a distinct dimension of employees' views that the items measure | an area of the questionnaire | six areas | the standard, 2.1; the questionnaire carries no areas or headings |
| SF2 | "the 30 survey items" | the 30 items | with the recommend question | same call: the count and the 30 placements with the recommend question added as a 31st variable (asserted) | the standard, 2.4: the recommend question belongs to no sub-scale |
| SF3 | "belongs to each" | each item under exactly one sub-scale, the dimension it loads on most | an item under two | same call: every item's largest loading exceeds its second by at least 0.25 (asserted) | the standard, 2.2 |
| SF4 | whose answers count | employees who answered at least one item before their site's close | every submission, test tokens and late answers included | same call (asserted) | the standard, 3.1 |
| SF5 | "does not apply" | not scored, missing to the correlations | scored as an extra category | same call (asserted) | the standard, 3.3, and the questionnaire's answer options (6) |
| SF6 | negatively worded statements | reverse-scored | left as answered | same call: reversing an item changes the sign of its correlations, never the eigenvalues or the placements (asserted) | the questionnaire's wording; the four statements run against every other item (asserted) |
| SF7 | yes and no codes | yes 1, no 2 as exported, or recoded 1 and 0 | either | same call: a linear recode moves no correlation (asserted) | the questionnaire's answer options |
| SF8 | the two language versions | pooled through the questionnaire's French numbers | English only | same call (asserted) | the questionnaire |
| SF9 | a repeated submission under one token | the last one | the first, or both | same call (asserted); the figures need it (the first submission moves the first latent eigenvalue to 9.66) | the standard, 3.2 |
| SF10 | kiosk sessions | the employee's sessions joined | each session a respondent | same call (asserted) | the kiosk log; convergent |
| SF11 | weighting | every respondent counts once | weighted to site headcounts | same call (asserted) | the standard, 3.2 |
| SF12 | missing answers | pairwise | complete cases only | same call (asserted) | method-level, convergent |
| SF13 | the retention test on the latent correlations | any (random data at the mean or 95th percentile, eigenvalue above one, MAP, revised MAP, the scree) | none filed | same call: each keeps three (asserted) | convergent (C1) |
| SF14 | empty cells in a two-way table | no correction | psych's 0.5 continuity correction | same call (asserted) | convergent (C1) |
| SF15 | which survey | the 2026 engagement survey | with the quarterly pulse survey | the pulse carries five other items | the standard, 1.2 |
| SF16 | the 2027 instrument | the 2026 questionnaire repeated unchanged | a revised questionnaire | same call | the standard, 1.3 |

## Ladder

| Rung | Construction | Count | Placements | Dies to |
|---|---|---|---|---|
| R0 (default) | Pearson correlations of the 30 answers, dimensions kept above random data (Kaiser's rule and MAP agree) | five | workload, tools, manager, growth, and belonging with recognition | the splits: the tools questions sit at about 94 per cent yes and the growth questions at about 6, and their Pearson correlations carry the shared split; on latent correlations the fourth eigenvalue falls well below the random-data value |
| R1 | the questionnaire's six areas as written | six | one per area | the standard's definition (a distinct dimension the items measure, 2.1) and the latent correlations |
| R2 | rank correlations, straight-liners dropped, complete cases, or one language | five | as R0 | the same splits: ranks of a two-valued answer keep the cap |
| R2b | Pearson correlations with the revised MAP or a scree read at three | three | growth alone, the manager statements with belonging and recognition, workload with tools | the same splits: the growth questions still stand apart, so the placements are wrong |
| R3 (decisive) | tetrachoric and polychoric correlations of every item, then any retention test | three | resources (workload, tools), manager and growth (manager, growth), connection (belonging, recognition) | the golden |

- **Position and margin.** On Pearson correlations (13,717 respondents) the eigenvalues are 5.59, 3.93, 2.15, 1.49,
  1.34 and 0.84, the fourth and fifth 0.43 and 0.28 above the random-data 95th percentile (both at least 0.15,
  asserted); on latent correlations they are 9.75, 6.01, 2.21 and 0.78, the fourth 0.29 below it (at least 0.2,
  asserted). On Pearson correlations the drop after the fifth eigenvalue is 0.77 of the drop after the third (at least
  0.7, asserted), so the scree shows a second elbow at five and a reader of it lands on three or five.
- **Every correction walks one way.** Spearman, complete cases, straight-liners dropped, English or French alone,
  Kaiser, MAP or random data at the mean or 95th percentile, each on Pearson correlations, keeps five; the revised MAP
  or a scree read at three on Pearson correlations keeps three, and every extraction and rotation then places the
  items off the golden (asserted for all 12); only the latent correlations give the golden.
- **Convergence of the decisive rung (C1).** Random data at the mean or 95th percentile, Kaiser, MAP and the revised
  MAP on the latent correlations, with or without the 0.5 correction for empty cells; principal-axis, minres or
  maximum-likelihood extraction with varimax, promax, oblimin or geomin rotation: three dimensions and the same 30
  placements (asserted).
- **Clean truth.** On the generator's own answers (no duplicates, test tokens, late answers or kiosk splits) the
  Pearson route keeps five and the latent route three (asserted); on the continuous views before they are cut into
  answers every route keeps three (asserted), so the five is made by the cuts alone.
- **Grid.** Two moves (latent or Pearson correlations; the retention test): the latent half converges on the golden,
  the Pearson half on five (or three with the growth questions alone), the area reading six.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | employees who answered at least one item of the 2026 survey before their site's close | filed (standard 3.1); C1 on test tokens, late answers and paper forms (SF4) |
| 2 | Unit of account | the item for placements, the dimension for the count | filed (standard 2.1, 2.2) |
| 3 | Attribution window | the 2026 survey, 14 to 27 September | filed (standard 4) |
| 4 | As-of dating | answers as given, a printed form's by its envelope's sealed date (the export records it when keyed) | the paper returns log's header; C1 for the call (SF4) |
| 5 | Version basis | the last submission of a personal link | filed (standard 3.2); C1 for the count (SF9) |
| 6 | Denominator | none: a count of dimensions | not applicable |
| 7 | Weighting | every respondent once | filed (standard 3.2); C1 (SF11) |
| 8 | Window length | one survey | filed |
| 9 | Boundary inclusivity | an answer at 23:59 local on 27 September is in | C1 for the call (SF4); the asks' rule in the standard, 3.1 |
| 10 | Rounding path | counts only; nothing rounds | by construction |
| 11 | Tie-break | an item placed under the dimension it loads on most | filed (standard 2.2); no item within 0.25 of a second loading (asserted) |
| 12 | Maturity and censoring | every answer is in when the export runs | export date after the last keyed form |
| 13 | Order of operations | clean, reverse, correlate, count, rotate, place | method-level; reversing commutes with the count (SF6) |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | the last submission of a personal link; kiosk sessions joined per employee | standard 3.2 and the kiosk log; C1 for the call (SF9, SF10) |
| 16 | Identity normalisation | French item codes to the 30 items through the questionnaire's French numbers | filed (questionnaire) |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | answer codes (1 to 5; yes 1, no 2; 6 does not apply) | filed (the questionnaire's answer options) |
| 19 | Code and status semantics | the answer codes, the negatively worded statements, the submission status | the questionnaire's options and wording, the export's status values; never the stump |
| 20 | Integerisation | counts are whole | by construction |
| 21 | Clause scope | the standard applies to the yearly survey and its dashboard | filed (standard 1.1) |
| 22 | Forward window contents | the 2027 dashboard reports the same 30 items | filed (standard 1.3) |

## Literal reader

Executed word for word, the prompt and the reporting standard fix the estimand (the number of distinct dimensions of
employees' views the 30 items measure among the 2026 respondents, each item under the one it measures most) and name
no estimator or retention test; every literal reading of the terms gives the same population and items (SF1 to SF16),
the method is forced by the answers' own distribution, since every retention test on latent correlations keeps three
with the same placements (asserted, C1), and the five comes from an easy method on the same literal estimand, never
from another reading.

## Oracles

None on the main call: no earlier sub-scales, vendor scoring guide, theme grouping, published structure or
consultant's figure ships. Kestrava's retail benchmark carries each item's favourable share in other retailers'
surveys and no structure, and the pulse survey is another instrument; neither bears on the count on either path.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops (lazy delta) | Realism |
|---|---|---|---|---|---|---|---|---|
| A, for each store department: the respondents, the stores where the dashboard can show its results, and the share of its employees on the opening day who answered | 24 (8 departments by 3) | the managers the call's structure is work for: each department team shown is a department manager who writes an action plan for every sub-scale below the company line, so the stores shown size what each kept sub-scale costs | the rollout's coverage table for the department managers' dashboards | D2 with D7, a label at the wrong vintage on a key whose meaning changed: on 1 October People Services renumbered the store departments for the new labour model (the code set kept, every code passed to another department), and its assignment report names every row's code by the department table as it stood on its 16 October run ("department descriptions as of run date"), so every store row in force on the opening day carries a September code under the name of the department that holds the code now: Grocery's 110 reads Front End and Front End's 160 reads Grocery, and so Produce and Meat and Seafood, Deli and Bakery, Receiving and Store Management. Only the September code read through the 1 October reorganisation rows, where every employee holding a code on 30 September passes to one new code at the same site, places the employees | H1 moves between departments of one store before the opening day (210, the as-of join); H2 the labour model's re-slotting from 16 to 30 September and moves in early October (700), H3 the 5 October moves of assistant department managers into store management (220): each sends the current-department read off; H4 employees assigned on the opening day who left afterwards; H5 the call's own population (test tokens, a personal link's last submission, kiosk sessions per employee, each site's local close, printed forms by the sealed date), which the cracker has | the export, submissions, distribution list, kiosk sessions, paper returns and site directory for the respondents; the HR report (employee_id, site_no, department_code, department, effective_from, effective_to, action) for the departments; the standard (3.1, 3.2, 3.4, 4.1, 4.3); 8 files, 26 columns | the opening-day row as the report names it (the cracker): 24 of 24 off; each employee's latest row (the current department): 23 of 24 off; each employee's own 1 October row: 20 of 24 off; the golden | a renumbered code joined to a report's current dimension table is the commonest way a history is mislabelled, and staff re-slotted before a labour model's go-live and assistant managers created at it are what an HR system records in those weeks |
| B, the chart | its parts | the construction | the call's own exhibit | none | none | the golden's eigenvalues | R0 to R3 values | the analyst's own exhibit |

- **Pin test.** The asking sentence pins the population (employees who answered at least one item before the
  survey closed), the grain (store department), the base (the department's employees on the opening day), the
  showing rule's source (the dashboard, standard 4.1) and the rounding; the standard files the WHAT (3.4 the site
  and department held in HR on the opening day, 4.3 the response rate's base). The device sits in which
  department a September code names, which no pin names and no filed sentence adjudicates: the report's header
  says what its description column is (the run date's), and nothing dates or announces the renumbering.
- **Forcing (asserted on the shipped rows).** Read through the renumbering, each of the eight September store
  codes passes on 1 October to exactly one department, and none of the 19,112 paired store employees changes
  department that day; read by the report's names, every one of them does, Grocery and Front End trading their
  whole staffs. Distribution centre and head office codes keep their names on both sides (the benign twins).
- **Main population zero-counts (asserted).** The call reads no HR row: with the HR report deleted, the
  respondents, every answer row, the eigenvalues and the placements are unchanged, and the close read from each
  token's own site (the list's site, a kiosk's store) keeps the same answer rows as the HR site, since no
  transfer crosses a time zone. No device or hazard row sits in a file the call needs.
- **Hazard table (asserted).** H1 moves the opening-day departments of 210 employees; H2 and H3 send the latest
  row off for 920 employees (the current-department stop misses 23 cells); H4 leaves 40 or more employees in the
  base who are gone by the run date; H5 is the cracker's.
- **Rounding edges (asserted).** Each department's response rate sits 0.01 points or more from its tenth's edge
  (the closest, Grocery's 63.763, 0.013); each rate is an exact ratio of two counts, so the edge moves only with a
  count, which is graded on its own.
- **Referee.** None; the department totals are a permutation under the device (D9: totals invariant), and no
  file carries a department count to tie against.

| Ask figures | Cracker (lands the call, runs the battery, executes every filed rule) | Cracker's value | Verdict |
|---|---|---|---|
| A respondents by department (8) | the opening-day row as the report names it, the standard's 3.1 to 3.4 executed | every department off by 39 or more | miss |
| A response rates by department (8) | the same, with 4.3's base | every department off by 0.4 points or more | miss |
| A stores where results can be shown (8) | the same, with 4.1's line | every department off by 3 or more | miss |
| B the chart | the golden's eigenvalues | right | outside |

Measured by: generator/ceiling.py on the cut pack (target.zip DIGEST): the cracker keeps 0 of the 24 department cells; the mirror on the Pearson rung takes the same ask path and keeps the same.
Mirror leakage: 3.7 per cent of ask weight (the chart's axes, 1 of 27 ask criteria).
Pair ceiling: 32.6 (the cracker 38 + 7 + 55 x 3/27 = 51.1 with the chart's three parts; the mirror 5 + 7 + 55 x 1/27 = 14.0).

- **Stress rows (ceiling.py prints them, not the gate).** Each employee's latest row keeps 1 of 24; each
  employee's own 1 October row keeps 4 of 24; the full includer, who reads every September code through the 1
  October rows, keeps 24 of 24, which with the call landed puts the pair at 81.5. The layer stands on one
  primary, the residual risk recorded here: the includer has to see that the report's names are its run date's
  while the codes in force on the opening day were renumbered before it ran, a judgment the battery does not make.

## Build record

- **Generator** (`task257/generator/`): `common.py` (calendar, districts, the 30 items and their two questionnaire orders,
  the store departments' October codes), `world.py` (sites, 21,375 employees on the opening day, transfers and
  leavers, the distribution list, the latent views behind every answer, web, kiosk and paper collection, time-outs,
  envelopes, test tokens; and `hr_extract`, People Services' assignment report built after the survey from its own
  random stream 16: department moves around the survey, the 1 October renumbering, every row named by the run date's
  table), `records.py` and `docs.py` (the 11 files), `psy.py` (bivariate normal, tetrachoric and polychoric
  correlations, retention tests, three extractions, four rotations), `load.py` and `deliver.py` (the golden from the
  bundle alone, the questionnaire read from its fielding copy, the negatively worded statements from the answers),
  `checks.py`, `verify.py` (an independent route: scipy's bivariate normal, its own random data, principal-axis with
  varimax, pypdf for the questionnaire, the September codes from its own pairing), `ceiling.py` (the cracker and the
  stress rows on the cut zip, no generator code), `build.py` (two builds byte-identical, `target.zip` cut last). World
  seed 2570944 (unchanged: the survey world, every answer and every frozen figure are the shipped version's).
- **Pack:** 11 files in four formats (CSV, XLSX, PDF, JSONL); the spine `kestrava_brackenmere_2026_responses.csv` has
  417,221 answer rows from 14,255 submissions (byte-identical to the shipped version, as are the submissions,
  distribution list, kiosk log, site directory and both distractors); distractors
  `pulse_survey_2026_q2_site_results.csv` and `kestrava_retail_benchmark_2026.xlsx` (the golden and the department
  ask unchanged with each deleted, asserted). No describing file ships: the codebook and the export notes are gone,
  their facts filed where the organisation keeps them (the questionnaire's fielding copy, the standard's 3.2, the
  paper returns log's header).
- **Measured (unchanged):** Pearson eigenvalues 5.59, 3.93, 2.15, 1.49, 1.34, 0.84 (parallel analysis, Kaiser and MAP
  keep five; the revised MAP three, with placements off the golden under all 12 extraction and rotation pairs); latent
  eigenvalues 9.75, 6.01, 2.21, 0.78 (every test keeps three; the same 30 placements under all 12 pairs); sparsest
  tools-by-growth cell 6; the 0.5 correction moves no latent correlation by more than 0.007.
- **The department ask:** 12,245 store respondents; Grocery 3,301 (63.8 per cent, 134 stores), Produce 1,334 (63.4,
  67), Meat and Seafood 1,070 (61.9, 46), Deli 902 (61.8, 24), Bakery 862 (63.5, 21), Front End 3,262 (63.4, 137),
  Receiving 623 (63.6, 2), Store Management 891 (74.4, 24). The cracker misses all 24 cells (39 or more respondents,
  0.4 or more points and 3 or more stores off in every department); the current-department stop misses 23 and the
  own-1-October-row stop 20 (asserted). HR streams 11 to 40 screened for every partner cell apart with margin.
- **Gates:** Gates (11-01, target.zip 132068ce): generator checks 157 of 157; verify.py clean (13,717
  respondents, latent eigenvalues 9.75, 6.01, 2.21, 0.78, three kept, Pearson five, the placements and the 24
  department figures); two builds byte-identical; figures_check.py 63 of 63; precut.py 61 checks, 0 FAIL, 0 WARN;
  voice-check PASS with no warning; ceiling.py pair 32.6 (cracker 0 of 24); leak.py --asof 2026-10-20 REVIEW, no
  LEAK, each line ruled: the questionnaire's "Brackenmere Leaders" and "Brackenmere Markets" beside decision
  vocabulary (an item's wording and the company's name in the recommend question, neither a sub-scale nor a
  figure), the stump-vocabulary lines (the questionnaire's own words; the standard's 2.1 definition of a sub-scale,
  the WHAT, with no count, grouping or method; the prompt's deliverable list, whose scree chart of "the items'
  correlations" names no estimator) and the HR report naming Front End, Store Management and the company beside
  numbers (department names at the ask's grain, ranking no sub-scale); `guard.py surface` exit 0, no pair promoted;
  `guard.py heart` WARN (the draw's three warnings, answered in the Draw), nearest driver 0.06 (task267); the 11-01
  heart BLOCK test.same_driver_older against task269 v2 is an H27 artifact (that card drawn 10-19, after this
  one's 10-15) and the card now carries a differentiation line against it; `freeze.py check task257 --mode rubric`
  exit 1 on the call sentence and the default path only, both recorded in Tried and rejected, every frozen figure,
  the stump, the card's stump and driver and the ladder unchanged.
- **Stage 4, the 11-01 reship cut (target.zip 132068ce):** the leak reader (Sonnet, medium, an isolated copy of the
  prompt and the pack) quoted nothing for questions 1 to 4, found the filed sentences fixing the asks' populations
  (3.1, 3.2, 3.4, 4.1, 4.3, each executing to the golden's basis) and no sub-scale count, and called the deciding
  step an analytical choice; both review items harmless, no realism tell needing a fix. The determinism-judge agent
  could not spawn its thread, so the main session spawned it from the agent's brief (Sonnet, medium, the one scratch
  directory): DETERMINISTIC, APPROVE, every committed figure reproduced, the department table exactly; Gate G
  method_or_model_selection, analytical_non_defect, no surface-read dependency, no sole data defect; Gate H domain,
  layers and decisive step pass, so the reader and the judge agree. Its two advisories need no change: the
  department labels rest on the report's header and the 1 October code pairs, which the judge found the files
  support; and the sub-scale names are not pinned, so block 4 now says the grouping is the answer. The 10-15
  version's stage 4 (one reader, one judge, DETERMINISTIC, APPROVE) is in `determinism_check_report.md`.

## Pre-ship check

- **Rule 1, the domain:** the deciding quantity is the number of latent dimensions a psychological scale measures,
  counted on the correlations its items' level of measurement calls for; with another field's nouns there is no
  survey item, no category threshold and no view behind an answer for the latent correlation to estimate.
- **Rule 2, two layers:** every Layer 1 item of the call (the long export under a header block, two questionnaire
  orders joined through the questionnaire's French numbers, negatively worded statements, does-not-apply,
  resubmissions of a personal link, test tokens, kiosk sessions under the pre-July store numbers with employee numbers
  as typed, printed forms recorded when keyed, UTC against local closes) is produced by Kestrava's or the kiosk app's
  own systems and is asserted neutral to the call; the HR report's renumbered departments sit on the asks' side only
  (the call reads no HR row, asserted); the decisive layer is the correlation estimator the answers' level of
  measurement requires.
- **Rule 3, the decisive step:** analytical (which correlations measure the views the items share), executed in
  checks.py: the easy route on the clean truth files five with tools and growth split off, the latent route alone
  files the golden, the continuous views before they are cut keep three on any route, and no plant ships. Reading
  every field and executing every filed sentence still leaves the estimator open; nothing in the pack names one.
- **The ask layer (rubric scope):** the department ask's device is analysis of HR's own records (a renumbered code
  under a run-date description, read through the renumbering rows), not a plant: the renumbering, the re-slotting
  and the 5 October moves are ordinary HR events, and the call reads no HR row (asserted); every cracker row misses
  on the cut pack (ceiling.py), and the residual risk (the full includer, pair 81.5 with the call landed) is
  recorded in the ask sheet.

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
- All 30 items on the five-point scale with realistic skew: Pearson and polychoric correlations kept the same number of dimensions (five-point answers skewed to agree carry too little of a cap to stand as a dimension); the tools and growth areas became yes or no experience questions, as many engagement surveys ask them.
- Tools questions at 95 to 97.5 per cent yes and growth questions at 2.5 to 6 per cent with the two factors correlated 0.35: four tools-by-growth tables had an empty cell, the uncorrected tetrachoric estimates ran to the boundary and the latent route kept four; the splits moved to about 94 and 6 per cent and the factors' correlation to 0.20, so every tools-by-growth cell holds at least 6 employees (asserted at 5) and the 0.5 correction moves no latent correlation by more than 0.007.
- A weak third dimension (loadings 0.38 to 0.48): the revised MAP kept two on the latent correlations; the belonging and recognition loadings rose to 0.46 to 0.56, where every retention test on the latent correlations keeps three.
- The shipped ask layer (respondents and complete respondents for each of the 12 store districts), re-measured on
  11-01 by an independent cracker on the shipped target.zip (9a983f66): 24 of 24 cells kept, pair 81.5. Both
  devices were executed by the call's own construction (the 13,717 respondents need the kiosk sessions joined per
  employee and the printed forms dated by their envelopes), the export notes filed what each rested on (answered_at
  as Kestrava's recording time, a new token per kiosk session) and the kiosk log marks every time-out; replaced by
  the department ask.
- The codebook and the export notes (describing files, leak.py LEAK): removed. Their facts went where the
  organisation keeps them: the questionnaire's fielding copy (the items, the French numbers, the answer codes with
  does-not-apply 6), the standard's 3.2 (a personal link's last submission) and the paper returns log's header (the
  export records a form's answers when it is keyed). Both conventions stay filed because the frozen figures need
  them: first submissions move the first latent eigenvalue to 9.66 and does-not-apply scored as a category to 7.78.
- A year-on-year ask on Kestrava's 2025 unit results joined to the current hierarchy: it needs a 2025 world, a unit
  code reused across hierarchy loads and a 2025 hierarchy file, which a year-aware solver executes as a crosswalk;
  dropped.
- A recommend-score ask with the score's codes shifted in one channel or keying batch: a range check finds the 11s
  and the batch split is the repair, so noticing and repairing are one act, and an unfiled switch date is not
  determinate; dropped.
- Respondents by district with an HR device: the site numbers are fixed by the call's own files (the list, the kiosk
  log and the site directory), so no code overlap can carry a renumbering, and the opening-day site is 3.4 executed;
  the department, which only the HR report holds, took the device.
- Rehired employees whose open termination row a careful as-of join keeps: the latest-row as-of reading is right for
  rehires and leavers alike, so only a sloppy reading misses; dropped.
- The department moves' first draft (520, none in the last fortnight of September): each employee's latest row kept
  7 of the 24 cells; the labour model's re-slotting from 16 to 30 September and the 5 October moves into store
  management were added, and HR streams 11 to 40 screened (stream 11 tied Grocery and Front End on stores shown, so
  the cracker kept two cells; stream 16 puts every partner cell 39 respondents, 0.4 points and 3 stores apart).
- The prompt's call sentence lost its count ("which of the 30 survey items" is now "which survey items"), as the
  prompt gate's no-count rule requires, and the default path's step 1 now names the questionnaire's French numbers
  for the removed codebook: `freeze.py check task257 --mode rubric` reports both sections moved and `--allow`
  reaches only figures.json keys, so both are recorded here and not cleared; every frozen figure, the stump, the
  card's stump and driver and the ladder are unchanged.
