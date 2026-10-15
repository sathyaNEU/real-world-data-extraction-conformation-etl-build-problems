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
  analytics lead, who wrote the reporting standard; Melissa Vang, Kestrava's account manager, who keeps the export and
  codebook.
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
  30 item placements, the chart's parts, and the asks' 24 district figures.
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

## Default path

1. Map the French questionnaire's item codes to the 30 items through the codebook, keep the last submission under
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
Layer 1: Kestrava's export in long form under a header block, French and English questionnaires in different item orders joined through the codebook, negatively worded statements, a does-not-apply code, resubmissions under one token, Kestrava's test tokens, kiosk sessions logged under the July store numbering with employee numbers as typed, an effective-dated HR history renumbered in the July reorganisation, and UTC timestamps against each site's local close; each is what these systems produce and none is placed to be caught.
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
| SF5 | "does not apply" | not scored, missing to the correlations | scored as an extra category | same call (asserted) | the standard, 3.3, and the codebook |
| SF6 | negatively worded statements | reverse-scored | left as answered | same call: reversing an item changes the sign of its correlations, never the eigenvalues or the placements (asserted) | the codebook's reversed flag |
| SF7 | yes and no codes | yes 1, no 2 as exported, or recoded 1 and 0 | either | same call: a linear recode moves no correlation (asserted) | the codebook |
| SF8 | the two language versions | pooled through the codebook's French codes | English only | same call (asserted) | the codebook |
| SF9 | a repeated submission under one token | the last one | the first, or both | same call (asserted) | Kestrava's export notes |
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
| 4 | As-of dating | answers as given; the count does not depend on when they were recorded | C1 (SF4) |
| 5 | Version basis | the last submission under a token | filed (export notes); C1 (SF9) |
| 6 | Denominator | none: a count of dimensions | not applicable |
| 7 | Weighting | every respondent once | filed (standard 3.2); C1 (SF11) |
| 8 | Window length | one survey | filed |
| 9 | Boundary inclusivity | an answer at 23:59 local on 27 September is in | C1 for the call (SF4); the asks' rule in the standard, 3.1 |
| 10 | Rounding path | counts only; nothing rounds | by construction |
| 11 | Tie-break | an item placed under the dimension it loads on most | filed (standard 2.2); no item within 0.25 of a second loading (asserted) |
| 12 | Maturity and censoring | every answer is in when the export runs | export date after the last keyed form |
| 13 | Order of operations | clean, reverse, correlate, count, rotate, place | method-level; reversing commutes with the count (SF6) |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | the last submission per token; kiosk sessions joined per employee | export notes; C1 for the call (SF9, SF10) |
| 16 | Identity normalisation | French item codes to the 30 items through the codebook | filed (codebook) |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | answer codes (1 to 5; yes 1, no 2; 6 does not apply) | filed (codebook) |
| 19 | Code and status semantics | the answer codes, the reversed flag, the submission status | filed codebook and export notes; never the stump |
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
| A, for each of the 12 store districts, how many employees answered at least one item before the survey closed | 12 | the trail of the respondents the dimension count stands on, from the collection records to the district | the dashboard's coverage line for each district | D8: a printed form's answers are recorded when Kestrava keys the form, and the store's second envelope, sealed on 26 or 27 September, is keyed in October; only the paper returns log's sealed date places those answers inside the survey, while first-envelope forms keyed during the survey look the same | D1 a kiosk session that times out and the employee's next session (two tokens, one person); D1 repeat submissions; D2 the distribution list's site (31 August) against the site held on the opening day; D8 UTC dates against each site's local close; D7 kiosk employee numbers without leading zeros and kiosk store numbers from before the July renumbering | responses (token, answered_at), submissions (token, channel, status), paper returns (site, sealed, keyed), kiosk sessions (session, store, employee), distribution list (token, employee, site), HR history (employee, site, effective dates), site directory (site, legacy number, district, time zone), the standard (3.1, 3.3); 8 files, 16 columns | answered_at against the close: every district off; tokens counted: districts with kiosk time-outs off; the distribution list's site: districts with September transfers off; UTC dates: every district off; the answer | paper forms in small stores, kiosk time-outs in large ones and transfers in the weeks before the survey are what a survey administrator's records hold |
| B, for each of the 12 store districts, how many of them answered all 30 items | 12 | the completeness of the answers the correlations rest on | the coverage line's second figure | D1: a kiosk session that sits idle for twenty minutes closes and keeps its answers, and the employee's next session starts at the first unanswered item, so neither token holds 30 answers and only the kiosk log's employee number joins them | D8 second-envelope forms keyed after the close; D1 repeat submissions; D2 the opening-day district; D5 does-not-apply is an answer (standard 3.3), not a gap | as A, with the codebook's code list; 8 files, 17 columns | each token's answers counted alone, or one session per employee: districts with kiosk time-outs off; second-envelope forms dropped: every district off; does-not-apply counted as missing: every district off; the answer | the same records |
| C, the chart | its parts | the construction | the call's own exhibit | none | none | the golden's eigenvalues | R0 to R3 values | the analyst's own exhibit |

- **Main population zero-counts.** No ask device moves the call (asserted: three dimensions and the same placements
  with second-envelope forms dropped, kiosk sessions taken one per token, repeat submissions both kept, late answers
  kept and test tokens kept); the paper returns log, the kiosk log, the distribution list, the HR history and the
  site directory are read by no step of the call; deleting every ask file leaves the call and Ask C unchanged.
- **Hazard table.** D8 paper (A primary, B hazard) moves every district in both (15 to 96 respondents a district);
  D1 kiosk (B primary, A hazard) moves every district in B (5 to 36 completes) and, for a token count, in A (5 to 42);
  D2 the opening-day site moves 7 districts by 1 to 4; D8 UTC dates move every district (2 to 29); does-not-apply
  counted as missing moves every district in B (84 to 286).
- **Referee.** None for the primaries; the export notes define each column (answered_at is the time Kestrava recorded
  the answer), the WHAT only; no filed sentence says when paper answers were given, that a kiosk time-out splits an
  employee's answers, or how to join them.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A respondents per district (12) | employees counted through the distribution list and the kiosk log, test tokens dropped, the last submission per token, answers before each site's local close by answered_at, the opening-day site from the HR history | second-envelope forms keyed in October dropped: every district off (asserted, 12 of 12 cells) | miss |
| B complete respondents per district (12) | the same, an employee complete when one of their tokens holds 30 answers | second-envelope forms dropped and kiosk time-outs never complete: every district off (asserted, 12 of 12 cells) | miss |
| C the chart | the golden's eigenvalues | right | outside |

Mirror leakage: 5 per cent of the ask weight on the most attractive wrong rung (the Pearson count of five): it misses
every Ask A and Ask B cell as the cracker does, and of the chart keeps only its axes and one value per dimension, its
marked dimensions being five on the wrong correlations.
Pair ceiling: 36 (the cracker about 54 with the call, its placements and the chart; the five-dimension mirror about
18 with the belonging and recognition placements).

## Build record

- **Generator** (`task257/generator/`): `common.py` (calendar, districts, the 30 items and their two questionnaire orders),
  `world.py` (sites, 21,375 employees on the opening day, the HR history with the July renumbering, transfers and
  leavers, the distribution list, the latent views behind every answer, web, kiosk and paper collection, time-outs,
  envelopes, test tokens), `records.py` and `docs.py` (the 12 files), `psy.py` (bivariate normal, tetrachoric and
  polychoric correlations, retention tests, three extractions, four rotations), `load.py` and `deliver.py` (the golden
  from the bundle alone), `checks.py` (170 assertions), `verify.py` (an independent route: scipy's bivariate normal,
  its own random data, principal-axis with varimax), `build.py` (two builds byte-identical, `target.zip` cut last).
  World seed 2570944, chosen among seeds screened for distinct district counts, live devices in every district and
  MAP agreeing with parallel analysis on the Pearson route.
- **Pack:** 12 files in four formats (CSV, XLSX, PDF, JSONL); the spine `kestrava_brackenmere_2026_responses.csv` has
  417,221 answer rows from 14,255 submissions; distractors `pulse_survey_2026_q2_site_results.csv` and
  `kestrava_retail_benchmark_2026.xlsx` (the golden and both asks unchanged with each deleted, asserted).
- **Measured:** Pearson eigenvalues 5.59, 3.93, 2.15, 1.49, 1.34, 0.84 (parallel analysis, Kaiser and MAP keep five; the
  revised MAP three, with placements off the golden under all 12 extraction and rotation pairs); latent eigenvalues
  9.75, 6.01, 2.21, 0.78 (every test keeps three; the same 30 placements under all 12 pairs; each item's largest
  loading at least 0.48 above its second); sparsest tools-by-growth cell 6; the 0.5 correction moves no latent
  correlation by more than 0.007.
- **Asks:** respondents 12,245 and complete 10,055 across the 12 store districts; the cracker misses all 24 cells
  (second-envelope forms 15 to 96 a district, kiosk-joined completes 5 to 36); no handling with the paper forms
  dropped or the kiosk sessions apart lands on any cell (asserted over 16 and 88 handlings).
- **Gates:** `precut.py` exit 0; `figures_check.py` 68 of 68; `leak.py --asof 2026-10-20` REVIEW, no LEAK, each line
  harmless (the standard holds the estimand's words, "distinct dimension of employees' views", and no count, grouping
  or method; the prompt sentence asks for the coverage counts and a scree chart of "the items' correlations" without
  an estimator; the counts are whole numbers and need no rounding words); `guard.py surface` clean, personas the three
  drawn; `guard.py heart` WARN, nearest 0.05.
- **Stage 4, loop 0:** the leak reader (Sonnet, medium) quoted nothing for questions 1 to 4, found the count left to
  the analysis (question 5) and the deciding step analytical (question 6), and flagged three realism tells, all fixed
  in the generator in one pass: the benchmark's quartiles ran past 0 and 100 (now a logit spread), a client programme
  sat in Kestrava's cross-client library (generic library wording for four items), and the French codes were the
  English ones swapped in adjacent pairs (the French version now has its own item order). The judge thread (Sonnet,
  medium, isolated) returned DETERMINISTIC, APPROVE: every figure reproduced from the bundle; Gate G
  method_or_model_selection, analytical_non_defect, no surface read, no sole data defect; Gate H domain, layers and
  decisive step pass; its two hygiene nits were the benchmark tells above. The fix moved the first two latent
  eigenvalues by 0.01 (9.75, 6.01) and the lowest tools yes share to 93.7 per cent; every gate re-ran green and no
  district figure moved.

## Pre-ship check

- **Rule 1, the domain:** the deciding quantity is the number of latent dimensions a psychological scale measures,
  counted on the correlations its items' level of measurement calls for; with another field's nouns there is no
  survey item, no category threshold and no view behind an answer for the latent correlation to estimate.
- **Rule 2, two layers:** every Layer 1 item (the long export under a header block, two questionnaire orders,
  negatively worded statements, does-not-apply, resubmissions, test tokens, kiosk sessions under the old store numbers
  with employee numbers as typed, the HR history's July renumbering, UTC against local closes) is produced by
  Kestrava's, the kiosk app's or HR's own systems and is asserted neutral to the call; the decisive layer is the
  correlation estimator the answers' level of measurement requires.
- **Rule 3, the decisive step:** analytical (which correlations measure the views the items share), executed in
  checks.py: the easy route on the clean truth files five with tools and growth split off, the latent route alone
  files the golden, the continuous views before they are cut keep three on any route, and no plant ships. Reading
  every field and executing every filed sentence still leaves the estimator open; nothing in the pack names one.

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
