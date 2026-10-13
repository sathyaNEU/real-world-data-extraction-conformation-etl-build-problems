# task259 design note

## Draw

- **Card:** `cards/task259.json`, registered 2026-10-13. Survey Research & Official Statistics, task type
  nonresponse-calibration-measurement-error-adjustment (a salary survey's measurement adjustment), objective
  Descriptive & Distribution Analysis; shape 07 (a grid: four Data Engineer levels against the band's three cuts of
  market base pay); decision quantity_figure (the Data Engineer III midpoint); gap time then population; pattern none,
  G7 then G16; Gate G decomposition_attribution; strategy grain_or_unit (a person's pay growth is not the level's).
- **World:** Tarnwick Systems, a fictional US software company, refreshes its engineering pay bands each year. Its
  compensation policy sets each band's 25th percentile, midpoint and 75th percentile at the market's 25th
  percentile, median and 75th percentile of base pay for the job and level, read from the matched respondents of the
  licensed extract of Tallyband, a fictional salary-sharing platform, as in effect on the benchmark date of
  1 October 2026. The bands take effect on 1 April 2027, when the pay-transparency posting system switches to them
  (forcing event launch_or_rollout); the executive team approves the refresh (forum executive_team).
- **People** (guard.py names --geo "United States" --seed 259; Diana Young skipped for a first name used in an older
  build): Patty Carroll, head of total rewards (role family other); Cole Gillespie, compensation analytics lead;
  Wanda Kane, people data and systems lead, who keeps the HRIS and posting exports.
- **Data-native sentence:** Tallyband keeps each respondent's latest report with the date it was filed, and some
  respondents carry their previous report too, so the extract spreads one level's pay over three years of filing
  dates; carrying a report to the benchmark date by what that respondent's own pay did between two reports adds the
  merit and promotion each person earns inside and between levels, while the market rate at a fixed level, which is
  what the band prices, moves only by how much the level's pay rises across filing dates; and because the platform's
  reach widened through the window to employers that pay less at every level (128 of the 247 matched employers are
  first seen after its first six months, 43 per cent of the last half-year's reports), the level's pay rises across
  the pooled reports by much less than it rises inside any one employer, so the movement is read within employers.
- **Loop 1 (2026-10-13, the author's request for a second layer of stumping):** the shipped decisive step (the level's
  movement read across filing dates, 1.7 per cent, $168,000) becomes a rung. The world now carries each employer's
  arrival on the platform and its pay at a fixed level: the employers whose engineers were filing when the window
  opened, and those that arrived from July 2024, the later arrivals paying less. Pay at a fixed level rises 2.7 per
  cent a year inside every employer; across the pooled reports it rises 1.1 per cent. The golden carries each report
  at the movement within employers: $170,000. The re-reporters' growth stays the default path (4.7 per cent,
  $175,000). The second layer is the survey field's own fixed-composition reading of change (the Employment Cost Index
  holds jobs and establishments fixed; salary surveys measure market movement on matched employers), not a new organ:
  no file, column or sentence was added for it. The card keeps grain_or_unit as the strategy of the first decisive
  move (whose movement carries a report) and names the second in its notes (composition_mix, the employer mix of
  the pooled reports); task256's composition step (a survey's within-sex conditional transfer to a roster) shares no
  mechanism with it.
- **Guard:** WARN three_rules.strategy_risk (grain_or_unit), answered by the analyst test: every field and rule read
  correctly still leaves the ageing rule open, and the easy routes (no ageing, or the re-reporters' own growth) are
  analysis, not readings. test.same_puzzle_older against task87 and the near driver task445 carry differentiation
  lines on the card. repeat.deliverables (an xlsx and an svg, as task256): a band table and the chart of the bands are
  the compensation genre's own pair, and the asks and their devices share nothing with task256's. task257 (DA07) waits
  for a later draw day: its world's natural step is the duty-cycle mix (composition_mix), barred against task256 in
  the draw window.
- **Client domain:** Economics carries no Descriptive task type, so the build sits in Survey Research & Official
  Statistics: a salary-sharing platform is a non-probability salary survey, and carrying each report from its filing
  date to the reference date is that survey's measurement adjustment.
- **Pairing and shape:** the field's own analysis decides (compensation practice ages every survey report to a
  common effective date by the market's structure movement at a fixed level, never by individuals' raises), the
  objective is where a pay distribution's cuts sit at a date, and the grid is four levels by three cuts (shape 07).
  Criteria: twelve cells, the call, each level's matched respondents (4), and the asks' figures.
- **Sources, one line each.** `guard.py mechanisms --objective descriptive-distribution`: task445 (completing a
  period for reporters not yet in) and task451 (arrival delays) spend the late report; here every report is in hand
  and the question is how far each must be carried. task253 v1 (nonresponse within class, retired as a template)
  spent calibration to population margins; the OEWS margins here are a distractor and the policy names the matched
  respondents as the population. task258 spent an effect's functional form carried to new units; here the carried
  quantity is a rate of movement, and the trap is whose movement. The seed DA09 gave the world, the decision and the
  quantity; its own step (the platform's family mixing machine-learning data engineers) stays a lower rung.
- **Forward facing:** the bands govern pay and postings from 1 April 2027, a window not yet open; the deciding
  quantity is the market as in effect on the benchmark date the policy names.

## Default path

The pipeline a strong analyst builds from the prompt's words, the policy and the files' grain; every figure is the
generator's, asserted in `generator/checks.py`.

1. Read the question and the policy: each Data Engineer band's midpoint is the median of market base pay for the job
   and level among Tallyband's matched respondents, as in effect on 1 October 2026, filed to the nearest $1,000.
2. Match the extract: respondents in the United States working full time whose primary focus (the profile table) is
   data pipelines and platforms, each employer level code mapped to Tarnwick's levels through the level crosswalk
   (788, 1,234, 1,366 and 844 respondents at I to IV).
3. See that reports were filed from October 2023 to September 2026, so each report's pay has to be carried to the
   benchmark date.
4. Measure pay growth where the extract measures it directly: the re-reporters' own change between their previous and
   current reports at the same level, 4.7 per cent a year over 848 pairs (7.3 with the reports that crossed a level).
5. Carry each matched report to 1 October 2026 at that growth and take each level's median: Data Engineer III
   175,000 (181,000 on every pair), Data Engineer I 122,000, II 149,000, IV 209,000.

Ends on: Data Engineer III midpoint $175,000
Golden: Data Engineer III midpoint $170,000

## Stump sentence

A strong analyst matches Tallyband's respondents to Tarnwick's levels, sees the reports were filed over three years,
carries each one to the benchmark date at the re-reporters' own pay growth between their two reports at the same level
(4.7 per cent a year) and files the Data Engineer III midpoint at $175,000; the step that lands it there is ageing by a
person's growth, which adds the merit each person earns inside the level as they progress through it, when the band
prices the level itself; the analyst who corrects that and reads the level's movement across the pooled reports (1.1
per cent a year) files $166,000, because the platform's later filings come more and more from employers that pay less
at every level; read within employers the level's pay rises 2.7 per cent a year, and the matched reports carried by
that movement give $170,000; the analyst who leaves the reports as filed files $164,000.

## Three rules

- Task type: nonresponse-calibration-measurement-error-adjustment (Survey Research & Official Statistics): a salary
  survey's reports filed at different dates adjusted to one reference date before its percentiles are read, the
  adjustment read on a fixed composition of employers.
- Domain test: the deciding quantity is the market median base pay for a job and level as in effect on a benchmark
  date, which compensation practice reads from survey reports aged to that date by the market's structure movement
  at a fixed level, never by individuals' raises, which also carry merit and in-level progression; and the field
  measures that movement on matched employers (the Employment Cost Index holds jobs and establishments fixed for the
  same reason), never across a respondent pool whose employer mix shifts between dates.
- Swap: "a hospital's median nurse wage at a reference date from staffing reports" or "a utility's median meter read
  cost" loses what decides here: there is no pay band whose market rate moves slower than the people inside it
  progress, no salary survey whose re-reporters carry their own merit and promotions, and no platform whose reach
  widens to employers paying less at the same level, so neither gap stands for anything.
- Layer 1: Tallyband's own family and normalised level, which mix roles and levels the company separates (the
  platform writes them); employer level codes mapped through an effective-dated crosswalk after one employer's
  re-levelling (the compensation team keeps it); employer names in the respondents' own spellings (free text); a few
  respondents outside the United States or not full time (the platform's open sign-up); OEWS wages by state beside
  the platform; Tallyband's offers extract beside its current-pay extract; and, on the ask paths only, an HRIS job
  history whose rows carry the pay zone recorded when each was written (Tarnwick re-zoned five cities on 1 July
  2026), future-dated job changes, leaves and contingent workers, and an ATS export listing each requisition once per
  posting city with its status as of the export and a hire's close date only.
- Layer 2: estimand identification and composition: the reference-date market rate for a level is carried from each
  report by the level's own movement, a property of the job and level, not of the people reporting, and that movement
  is read within employers because the employers reporting at each date are not the same.
- Decisive step: reading the market's movement at a fixed level within employers (an intercept for each employer),
  rather than across the pooled reports, whose later dates hold more of the lower-paying employers the platform
  reached later, or from the re-reporters' own growth, which carries merit and in-level progression, then ageing each
  matched report by it.
- Not semantics: every field is read correctly on every route: the filing date is the date the pay applied, the
  previous report is the same person's earlier pay, the crosswalk maps levels, the employer is the employer; no field,
  code, unit or definition says which movement carries a report or that the platform's employers changed over time.
- Not rule application: the policy files what the market is (the matched respondents) and when it is read (the
  benchmark date) and nothing on how a report is carried there; executing every filed sentence leaves the movement
  open, and only the data separate the level's movement inside employers from the pooled drift and the people's
  growth.
- Analyst test: a strong analyst who matches every respondent correctly and ages each report by the re-reporters'
  own growth between their two reports at the same level files the Data Engineer III midpoint at $175,000 (the
  default path's Ends on); one who corrects that by reading the level's movement across the pooled reports files
  $166,000; leaving the reports unaged files $164,000; all miss $170,000.
- Estimand: the compensation policy (`tarnwick_compensation_policy_2026.pdf`, 4.1 to 4.4): each band's midpoint is
  the median of market base pay for the job and level, the market being every matched respondent of the licensed
  extract counted once, read as in effect on 1 October 2026 and filed to the nearest $1,000.
- No decoy: nothing is planted: no memo, prior band, published index or stakeholder figure states a growth rate or a
  midpoint; the previous reports are the platform's ordinary record of respondents who updated, and the employers'
  arrival through the window is the platform's ordinary growth, named in no file.
- No certified replay: no file publishes a market movement, an aged median or last year's bands, so no rule is chosen
  by reproducing a certified figure.
- Lesson: a rate read from people who move through a scale is not the rate at which the scale moves, and a rate read
  across a pool whose members change between dates is not the rate at which any member moves; to carry a survey
  report to a reference date, read the movement at a fixed grade inside the same reporting units.

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene battery | 6 linear arithmetic | Verdict |
|---|---|---|---|---|---|---|---|
| R0 Tallyband's own family and normalised level, as reported | the policy names matched respondents through the focus and the crosswalk | the family and level columns | yes | none | clean | a median | readable |
| R1 matched respondents, base pay as reported | policy 4.2 | the profile table and the crosswalk | yes | none | clean | a median | readable |
| R2 (default) each report aged by the re-reporters' own growth | policy 4.3 says the market is read as the pay a job and level commands on the benchmark date | previous_base_usd and previous_reported_on name a growth | yes: a paired, same-person growth reads as the careful measure | none | clean | one rate, then a median | readable |
| R3 each report aged by the level's movement across the pooled reports | no sentence names a movement | no column carries one | the careful analyst's correction once the people's growth is refused: a trend at a fixed level | none | clean | a trend fit, then every report re-aged | readable |
| R4 (decisive) each report aged by the level's movement read within employers | no sentence names a movement, an employer mix, the platform's reach or a fixed panel | no column marks an employer's arrival or its pay; the employer column is the respondent's own text | not a reflex: the reflexes leave the reports as filed, use the people's growth or fit the pooled trend | no published index, prior band or matched-employer series to confirm it | clean | no: an intercept for each employer, then every report re-aged before the percentiles | silent |

## Semantic fork table

| Id | Term or convention in the main ask or the main computation | Golden reading | Alternative reading | Call under the alternative | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "base pay" | the base salary each respondent reports, annual US dollars | total pay with bonus and equity | another figure | policy 4.1 (base pay); the extract's base column |
| SF2 | "the market" | every matched respondent counted once | respondents weighted to OEWS state employment | another figure | policy 4.2: every matched respondent counts once |
| SF3 | "Data Engineer III" | Tarnwick's level III through the level crosswalk | Tallyband's normalised level (L4) | another figure (166,000 carried) | policy 4.2 maps employer levels through the crosswalk |
| SF4 | a matched respondent's job | primary focus data pipelines and platforms in the profile table | Tallyband's data engineering family | another figure (172,000 carried) | policy 4.2 and the job architecture's survey match |
| SF5 | "as in effect on 1 October 2026" | every matched report carried to the benchmark date | only reports filed in the last twelve months, as filed | another figure | policy 4.2: every matched respondent counts once |
| SF6 | the crosswalk in force | the mapping in effect on each report's filing date | the current mapping for every report | same figure (asserted) | C1; the crosswalk's effective dates |
| SF7 | percentile definition | linear interpolation between order statistics | nearest rank, or the median of even counts as the lower middle | same figures to $1,000 (asserted) | C1 |
| SF8 | rounding | half up to the nearest $1,000 once, from unrounded percentiles | rounding the aged pay first | same figures (asserted) | C1 |
| SF9 | the movement's estimator within employers | the slope of log base pay on filing date with an intercept for each employer and each level | an intercept for each employer and level pair; each level's own slope within employers; the pooled slope over the employers seen in the window's first year, or in all three years | same figures to $1,000 (asserted) | C1 |
| SF10 | the ageing form | pay times e to the movement times the years to the benchmark date | compound annual, or linear | same figures (asserted) | C1 |
| SF11 | years to the benchmark date | days over 365.25 | whole months over 12 | same figures (asserted) | C1 |
| SF12 | "United States" | respondents located in the United States | respondents of US employers located abroad | same figure (asserted) | policy 4.2 (located in the United States); C1 |
| SF13 | the employer a report belongs to | the employer name tidied to the crosswalk's | the name as the respondent typed it | same figures (asserted) | C1 |
| SF14 | the reports the movement is read from | the matched reports | every family's US full-time reports, or the offers extract, each within employers | same call (asserted: 2.67 and 2.75 per cent) | C1 |

## Ladder

Generator figures (the Data Engineer III midpoint, dollars), asserted in `checks.py`.

| Rung | Construction | DE III midpoint | Killed by (one fact) |
|---|---|---|---|
| R0 | Tallyband's data engineering family at its normalised level L4, as reported | 162,000 | policy 4.2: matched through the survey match's focus and the crosswalk |
| R1 | matched respondents, as reported | 164,000 | policy 4.3: read as in effect on the benchmark date |
| R2 (default) | each matched report aged by the re-reporters' growth at the same level (4.7 per cent a year) | 175,000 (181,000 on every pair, 7.3 per cent) | the level's pay rises across filing dates far slower; the pairs add each person's merit inside the level |
| R3 | each matched report aged by the level's movement across the pooled reports (1.1 per cent a year; 1.8 without an intercept for each level, 168,000) | 166,000 | inside every employer the level's pay rises 2.7 per cent a year; the pooled reports' later dates hold more of the employers that arrived later and pay less |
| R4 (decisive) | each matched report aged by the level's movement within employers (2.7 per cent a year) | 170,000 | |

- **Why each rung is a place to stop:** R0 is the platform's own dashboard; R1 is the median every survey reader
  quotes; R2 is the most careful-looking measure of growth in the file (the same people, twice); R3 is the careful
  analyst's correction of R2 (a trend at a fixed level across every report), and it reconciles: every level's pooled
  trend agrees, every estimator of it agrees (per level, quarterly or annual medians, median regression: 166,000 or
  167,000).
- **Sign and worth:** R1 and R3 sit below the golden and R2 above it, so neither single correction from R2 or R1
  lands: the refusal of the people's growth walks down to R3 and only the within-employer reading reverses it back up
  four rounding steps; the gaps to the golden are 6, 4, 2 (R3 without level intercepts) and 5 steps.
- **Every level:** the same construction moves every level's midpoint the same way (I: 114,000, 116,000, 119,000,
  122,000; II: 140,000, 142,000, 145,000, 149,000; IV: 197,000, 200,000, 204,000, 209,000 on R1, R3, R4, R2), asserted
  per level; R1, R3, R3 without level intercepts and R2 each miss every Ask C figure.
- **Every shortcut:** the family or the focus, the crosswalk or Tallyband's L4, each as reported, carried at the
  pooled, within-employer or paired rate: 160,000 to 177,000, none on 170,000 (asserted). Within employers but
  without an intercept for each level reads 3.3 per cent and files 172,000 (asserted). Every cross-section estimator
  of the movement files 166,000 to 168,000 (asserted).
- **Bins:** every graded point keeps a margin of $234 or more to its bin edge under every defensible estimator
  (SF9 to SF11, SF13, every percentile definition, rounding first); the call sits $447 inside its bin.

## Closure table

| # | Axis | Reading chosen | Closure move |
|---|---|---|---|
| 1 | Population | matched respondents: US, full time, focus data pipelines, level through the crosswalk | pinned (policy 4.2); C1 (SF12) |
| 2 | Unit of account | one respondent | pinned (policy 4.2: counts once) |
| 3 | Attribution window | the extract as taken on the benchmark date | pinned (policy 4.2) |
| 4 | As-of dating | 1 October 2026 | pinned (policy 4.3) |
| 5 | Version basis | the crosswalk row in effect on each report's filing date | C1 (SF6) |
| 6 | Denominator | none: percentiles of a distribution | C1 |
| 7 | Weighting | none: every matched respondent once | pinned (policy 4.2); SF2 |
| 8 | Window length | the three years of filing dates the extract keeps | pinned (the platform's methodology) |
| 9 | Boundary inclusivity | percentiles by linear interpolation | C1 (SF7) |
| 10 | Rounding path | unrounded percentiles rounded once, half up, to $1,000 | C1 (SF8) |
| 11 | Tie-break | none needed | C1 |
| 12 | Maturity and censoring | every report in hand at the extract | C1 |
| 13 | Order of operations | match, age, then take percentiles | C1 (SF8) |
| 14 | Row order | not order-dependent | C1 |
| 15 | Duplicate resolution | one row per respondent | C1: respondent ids unique (asserted) |
| 16 | Identity normalisation | employer names to crosswalk employers by their canonical name | C1: the mess neutral to the figures (asserted) |
| 17 | Netting against gross | none | C1 |
| 18 | Dimensional units | annual US dollars | C1: one unit in the base columns |
| 19 | Code and status semantics | employment type and focus codes from the methodology page | pinned (methodology); never the stump |
| 20 | Integerisation | none | C1 |
| 21 | Scope of a stated clause | "market pay" is base pay of matched respondents | pinned (policy 4.1, 4.2) |
| 22 | Forward window contents | the bands from 1 April 2027, set on the benchmark-date market | pinned (policy 4.3, 4.5) |

## Literal reader

Filed estimand, from the prompt and the policy: for each Data Engineer level, the 25th percentile, median and 75th
percentile of the base pay of every matched respondent (US, full time, focus data pipelines and platforms, level
through the crosswalk), counted once, as in effect on 1 October 2026 (the base pay a job and level commands on that
date), filed to the nearest $1,000. Criterion: none filed; the design forces the method (determinism-check §1, form
1): the policy reads the market at the benchmark date and the reports were filed over three years, so each must be
carried there, and the extract shows how: inside every employer, at every level, pay rises across filing dates by
the same 2.7 per cent a year (each level's own slope within employers, and an intercept for each employer and level
pair, give the same rate); across the pooled reports it rises 1.1 per cent, because the employers first seen after
the window's first six months (43 per cent of the last half-year's reports) pay 7.2 per cent less at a fixed level;
and the re-reporters' own growth at the same level, 4.7 per cent, would have every level's pay rise far faster than
any employer's reports filed at each date show. Every literal reading of the policy's terms lands on the golden once
the reports are carried by the level's movement within employers (the fork table, SF1 to SF14); the easy answers come
only from easier models of the same carry (none, the people's growth, the pooled drift), never from another reading.

## Oracles

- OEWS wages by state: another population (every industry, no levels), no figure about Tarnwick's levels; ties
  nothing on either path, declared a distractor.
- Tallyband's offers extract: what new hires were offered, not what respondents are paid; read within employers its
  movement is the golden's (2.75 per cent, the same call), read across the pooled offers it drifts like the pooled
  reports (1.7 per cent); it ties nothing only under the golden, declared a distractor.
- Every family's reports: within employers 2.67 per cent (the same call), pooled 1.2 per cent; the same insight on
  more rows, never a referee.
- The re-reporters' previous reports: evidence, not a control; they measure people's growth, which the golden does
  not use.
- Nothing ties only under the golden for the main call.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops (lazy delta) | Realism |
|---|---|---|---|---|---|---|---|---|
| A, how many Data Engineers Tarnwick employed at each level in each pay zone on 1 October 2026 | 12 | a measure every level carries that the call does not turn on (the population each band governs, policy 5.1) | the head of total rewards submits each band with the population it governs | D2: each HRIS job record carries the pay zone recorded when it was written; Tarnwick moved Los Angeles, Washington and Denver into zone 1, Atlanta and Raleigh into zone 2 and Portland into zone 3 on 1 July 2026, so the records written before carry the old zone; only pay_zones_2026.csv, with both maps and their dates, places a worker in the zone of their location that day | D8 (job changes entered ahead to 16 November 2026); D4 (employees on leave remain employees; an active-only filter drops them); D5 (contingent workers in the same export); D6 (a job history, one row per change, read as a roster) | hris_job_history_2026-10-14.csv (employee_id, effective_date, job_code, work_location, pay_zone, status, worker_type), pay_zones_2026.csv (work_location, pay_zone, effective_from, effective_to), people_data_exports_readme.md; 3 files, 11 columns | every row counted: 592 rows for 159 employees; the latest record, changes entered ahead read as current: 10 of 12 cells off; active only: 9 off; contingent kept: 8 off; the zone on the record: every cell off ([10, 13, 7], [17, 21, 13], [19, 18, 18], [7, 9, 7]); the answer: [19, 6, 5], [29, 12, 10], [27, 14, 14], [14, 6, 3] | an HRIS that stamps a derived attribute on the job record and refreshes it only when the next job event writes a record |
| B, how many open requisitions Tarnwick held at each level on 1 October 2026 | 4 | a measure every level carries that the call does not turn on (the postings policy 4.5 reprices) | the head of total rewards counts the postings the new ranges replace | D4: closed_on holds a hire's close only; a cancelled requisition has none, and its cancellation is dated only by status_date, the date its status as of the export took effect | D6 (each requisition once per posting city); D2 (status as of the export, 14 October: fills and cancellations after 1 October, openings after it) | ats_requisitions_2026-10-14.csv (requisition_id, job_code, opened_on, closed_on, status, status_date), people_data_exports_readme.md; 2 files, 6 columns | posting rows: 12, 23, 28, 6; status open as exported: 3, 6, 9, 4 (three levels off); closed_on as the end: 4, 15, 12, 4 (every level off); the answer: 3, 5, 8, 3 | an ATS that dates a requisition's close by its hire and keeps a cancellation as a status change |
| C, the midpoints of Data Engineer I, II and IV and Data Engineer III's 25th and 75th percentiles, and the chart | 5 and the chart's parts | the construction | the band table's own cells | none | none | the golden model | R1, R3 and R2 values (I 114,000, 116,000 and 122,000; II 140,000, 142,000 and 149,000; IV 197,000, 200,000 and 209,000; III quartiles 153,000 to 176,000, 155,000 to 179,000 and 162,000 to 188,000) | the policy's own reference points |

- **Main population zero-counts:** no row of the HRIS export, the zones table, the ATS export or the people data
  notes is read by the call; the Tallyband extract, the profile table, the crosswalk, the methodology page, the job
  architecture and the policy carry no ask device (asserted: the call's documents name no requisition, leave,
  contingent worker or zone change); the call computed from the call files alone equals the golden (asserted).
- **Hazard table:** D2 (A) moves every cell (the five re-zoned cities' workers whose last record predates July);
  D8 moves ten cells; D4 nine; D5 eight; D6 every cell (592 rows); D4 (B) moves every level (cancellations before
  1 October counted open); D6 (B) every level; D2 (B) three levels.
- **Referee:** none; the notes say what each column holds (pay_zone "the pay zone on the job record"; status_date "the
  date that status took effect"), and no filed sentence says how to count an employee or a requisition on a date or
  which record's zone to read.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A headcount (12) | each employee's record in force on 1 October (dated on or before it), employees only, leave counted, the pay zone on that record | every cell off: [10, 13, 7], [17, 21, 13], [19, 18, 18], [7, 9, 7] | miss |
| B requisitions (4) | distinct requisitions opened on or before 1 October and not closed by then (closed_on blank or later) | every level off: 4, 15, 12, 4 | miss |
| C midpoints and quartiles (5) and the chart | the golden's construction | right | outside |

Mirror leakage: 0 per cent of the ask weight (the mirror, on R1, R2 or R3, misses every Ask C figure and does the asks
as the cracker does).
Pair ceiling: 38 (the cracker at about 63 with the call, Ask C and the chart; the mirror at about 12).

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Outcome (asserted) |
|---|---|---|---|---|
| Employer names as respondents typed them (one report in twenty) | Tallyband (free text) | tallyband_extract_2026-10-01.csv | joined to the crosswalk as typed, the unmatched dropped | the same call (169,994 unrounded); the counts move |
| Respondents outside the United States or not full time (under one per cent) | Tallyband's open sign-up | tallyband_extract_2026-10-01.csv | kept | the same call (169,916) |
| Quarry Systems' re-levelling on 3 March 2025 | Tarnwick's compensation team | level_crosswalk_2026.csv | today's crosswalk row for every report | the same call (170,225) |
| Salaries typed to the thousand (a quarter of reports) | respondents | tallyband_extract_2026-10-01.csv | none needed | every estimator in the same bins (asserted) |
| Previous reports for about a quarter of respondents, a fifth across a promotion | Tallyband (updates) | tallyband_extract_2026-10-01.csv | read as extra respondents | ruled out by policy 4.2 (counts once); the default path's raw material, never mess |
| Employer names as typed when reading the movement within employers | Tallyband (free text) | tallyband_extract_2026-10-01.csv | each spelling its own employer | the same figures (SF13, asserted) |
| OEWS wages and the offers extract beside the platform | the OEWS layout; Tallyband | the two distractors | read for the call | never read by the golden (asserted) |
| The HRIS's recorded zone, entered-ahead changes, leaves and contingent workers; the ATS's posting grain, status as of the export and hire-only close dates | the HRIS and the ATS | the ask files | as in the ask sheet | the call never reads them (asserted) |

## Build record

- Stage 3: `python3 task259/generator/build.py` writes the pack (12 files, 4 formats; the Tallyband extract 35,851
  rows), the goldens, figures.json and metadata.json; 87 checks green (the three-rules block R1 to R3c on the clean
  truth, SF1 to SF12, the bins under every defensible estimator, the ladder and every shortcut, both device asks'
  truths, crackers and stops, the separation line, the realism sweep, the goldens against figures.json); the
  independent verifier agrees on the six band points, the four matched counts, the twelve headcount cells, the four
  requisition counts and the chart's labels; two builds byte-identical; target.zip cut from the final build. precut
  exit 0 (49 checks); figures_check exit 0 (33 figures); container audit clean on target/ and golden/; guard heart
  WARN (answered in the Draw), validate clean; guard surface promotes task258 (surface 0.100, back to back, the same
  decisive gap) and task87 (gap, pattern and decision family): author-triggered adjudication, not run; against
  task258 the drivers differ (a part of a page's paint settling at a level carried to new pages, against a survey
  report carried to a reference date by its level's movement) and so do the strategies (method_or_model_selection
  against grain_or_unit); task87 is differentiated on the card.
- leak.py REVIEW, no LEAK: the policy carries the call's words (Data Engineer, midpoint, bands, 1 April 2027) as the
  estimand's own authority, never the figure; the methodology page and the policy share the stump paragraph's
  ordinary vocabulary (report, respondent, extract, market, crosswalk) and name no movement, ageing or growth rule;
  the ATS names the four levels beside requisition ids and dates, never a ranking; the HRIS's 34 dates after the
  export are changes entered ahead, as its readme says.
- Generator choices that keep every reading on one answer: matched pay built per level and filing quarter on the
  market's path with a quarter-to-quarter wobble carrying no trend, a quarter of salaries typed to the thousand, no
  $5,000 heaps; the tuned market levels give every graded point a margin of $215 or more under every estimator; no
  HRIS or ATS record falls on the benchmark day.
- Stage 4 (2026-10-13), pass 1. Determinism judge (isolated thread on the r1 brief): DETERMINISTIC, APPROVE; every
  figure reproduced (matched 788, 1,234, 1,366, 844; slope 1.73 per cent; midpoints and quartiles; headcount 159;
  requisitions 3, 5, 8, 3); Gate G decomposition_attribution, analytical_non_defect, no surface read, no sole data
  defect; Gate H domain, layers and decisive step pass; residual risk named: the re-reporters' growth contested as a
  carry by a strict literal reader. Leak reader: no decisive-step sentence, no ranking or answer-bearing file; it
  read policy 4.3 ("as in effect on the benchmark date") as leaving open whether to take each latest report as filed;
  realism tells: round counts (36,000 respondents, 5,200 offers), employer names in sibling sets, a crosswalk of
  exactly four rows an employer, the readme describing the requisitions' posting grain. Fixed in the generator in one
  pass: 4.3 now files the WHAT ("the base pay a job and level commands on that date"), which closes both the as-filed
  reading and the person-against-position reading without naming a carry; 3.2 no longer ties zones to the work
  location (an ask organ in a call document), and the readme instead says what the HRIS column holds ("the pay zone
  recorded on the job record when it was written"); the readme no longer narrates the posting grain; Tallyband
  withdrew 149 identifying reports outside data engineering (35,851 rows); 5,163 offers; employers trade under 260
  distinct names; the crosswalk lists out-of-scope codes for some employers (1,214 rows). No graded figure moved
  (checks and verifier unchanged); leak.py REVIEW on the same harmless lines; the reader and one judge pass re-run on
  the final pack because documents changed.

- Stage 4, pass 2 (on the final pack, because documents changed). Leak reader: no decisive-step sentence, no ranking
  or helper file; 4.3 now read as requiring every report restated to 1 October 2026 with the method open; remaining
  realism notes (word-plus-trade employer names in bulk, every crosswalk row dated 2019-01-01) fixed as data only
  (varied employer names, mapping dates per employer from 2019 to 2021); no document, prompt or graded figure moved.
  Determinism judge (r2): DETERMINISTIC, APPROVE; every figure reproduced; Gate G method_or_model_selection,
  analytical_non_defect, no surface read, no sole data defect; Gate H domain, layers and decisive step pass. Its
  optional fix (file "movement in pay at a fixed level across filing dates" in 4.3) is declined: it files the method,
  and the decisive step would become rule application. Its minor semantics (the HRIS's recorded zone differs from the
  dated table for 65 of 159 employees; leave employed; contingent workers out) are each closed by a shipped file.

- Loop 1 (2026-10-13, the author's request for a second layer). Stage 3: the world gives each employer its arrival
  on the platform and its pay at a fixed level (127 employers filing when the window opened, 133 arriving from July
  2024 with 60-day ramps, the later paying less); each person's place about their employer carries no movement of its
  own inside any employer (projected off every within-employer date contrast), and the other families' and the
  offers' noise likewise; movement 2.7 per cent within employers, merit 2.0; the market medians and Data Engineer
  III's spread and lean tuned so every graded point keeps $234 or more under every estimator. 101 checks green (the
  analyst test now runs both easy routes on the clean truth: the pairs file 175,000, the pooled movement 166,000, the
  movement within employers the golden); the verifier recomputes the slope with an intercept for every employer;
  two builds byte-identical; figures_check 36 figures; precut 49 checks; leak.py REVIEW on the same harmless lines
  (clause 1.1 read as the pooled 1.1; the policy's call words; ordinary vocabulary; ATS levels; HRIS dates ahead);
  guard heart WARN (loop 0 differentiated on the card), surface promotes task258 and task87 as before.
- Loop 1, stage 4. Leak reader (fresh copies): no decisive-step sentence, no ranking or helper file, nothing names
  the employers' arrival; it read 4.3 as vague on restating old reports (its literal executor files R1), ruled as in
  loop 0: 4.3 names the pay on 1 October 2026. Determinism judge (one isolated thread on the judge agent's brief):
  DETERMINISTIC, APPROVE; every figure reproduced (slope 2.70 per cent, the same by level and with an intercept for
  each employer and level pair; midpoints, quartiles, matched counts, headcount, requisitions); the alternatives
  (no carry 164,000, the pooled slopes 166,000 and 168,000, the pairs 175,000) all miss; Gate G
  method_or_model_selection, analytical_non_defect, no surface read, no sole data defect; Gate H domain, layers and
  decisive step pass. Its optional point (close "employed" for workers on leave in Ask A) is declined as in loop 0:
  the leave rows are the ask's designed device and the readme files leave as a job state.

## Pre-ship check

- **Rule 1, the domain:** the deciding quantity is a salary survey's market median for a job and level at a
  reference date, read from reports filed over three years; the field carries each report to the reference date by
  the level's own movement (the survey's reference-period adjustment), never by the reporters' raises, because people
  climb through a level that the band holds still, and it reads that movement on matched employers, the way the
  Employment Cost Index holds establishments fixed, because the platform's employers changed across the window.
  Swapped into a hospital census or a meter file, there is no level people move through, no re-reporter whose own
  growth carries merit and no platform whose reach widened to employers paying less, so the gaps between the three
  rates stand for nothing.
- **Rule 2, two layers:** Layer 1 is the platform's free-text employers, its own families and normalised levels, the
  effective-dated crosswalk, its non-US and part-time respondents, typed-to-the-thousand salaries and, on the ask
  paths, the HRIS's recorded zone, entered-ahead changes, leaves and contingent workers and the ATS's posting grain
  and dates; each mishandled leaves the call at $170,000 (asserted). Layer 2 is the carry and the composition the
  carry is read on: the paired growth files $175,000, the pooled movement $166,000, no carry $164,000, the movement
  within employers $170,000, executed on the clean truth.
- **Rule 3, the decisive step:** an analytical choice of whose movement carries a report and on which composition it
  is read (the level's inside employers, against the pooled reports' drift and the people's growth between their two
  reports); no field, code, unit or definition says it, no filed rule performs it, and no file names the employers'
  arrival; nothing is planted (no memo, prior band, index or stakeholder figure).
- **Gate G:** no shipped artifact ranks or states a midpoint; deleting every wrong number leaves the difficulty
  intact, since the wrong answers come from methods, not from figures in the pack.
- **Determinism:** the estimand is filed in the policy (who, counted once, when, which points, rounding); every
  defensible estimator of the movement within employers, carrying form, time convention, employer spelling and
  percentile definition lands in the same bins, and the movement read within employers from every family or from the
  offers lands on the same call (asserted); the asks' WHAT is in the people data readme (what each row and column
  holds).

## Tried and rejected

- DA09's own decisive step (the platform's data engineering family mixing machine-learning data engineers, removed
  through the profile table's primary focus): a filter on a field, data semantics under the 10/10 rules; kept as a
  lower rung.
- Calibration of the platform's respondents to OEWS state employment margins as the decisive step: the driver of
  task253 v1 (nonresponse within class), retired as a template; OEWS ships as a distractor and the policy names the
  matched respondents as the population.
- Salaries heaped to $5,000 for a twelfth of reports: medians stuck to the heaps, the quarterly and annual medians'
  slopes fell to 1.3 to 1.6 per cent, and the graded points split across bins by estimator; heaping kept to the
  thousand for a quarter of reports.
- Tallyband's normalised scale aligned to the crosswalk but for two schemes: the profile focus with Tallyband's L4, as
  reported, filed $168,000 by offsetting errors (IV codes in L4 against unaged pay); the scale now sets one employer
  scheme a level higher, and no shortcut lands.
- The requisition ask's device as a re-levelled or reopened requisition: the level or the open spell on 1 October is
  not recoverable from an export that keeps no history, and it touches one or two requisitions; the cancellation dated
  only by status_date kept.
- An acting-assignment row in the HRIS carrying the acting job: "employed at each level" reads two ways, a semantic
  fork on the ask; dropped.
- Employee job codes reissued in a mid-year architecture refresh: a real refresh converts every record, so stale codes
  would read as planted; the recorded pay zone, which no job event refreshes, kept.
- Coined employer names from syllable pairs: one came out as a drug brand (Valium), others matched real companies
  (Calyx, Doryx), and shared syllables still formed sibling sets; replaced by one distinct place or nature word an
  employer, with the words of real companies (Lattice, Starling, Mistral, Wolfram and others) left out.
- The shipped design (loop 0) as the final rung: the level's movement read across filing dates over the pooled
  reports (1.7 per cent, $168,000) was the decisive step; at the author's request for a second layer it is now R3,
  and the world's employers arrive through the window paying less, so the pooled movement understates the market's.
- A record check (a verified subsample of reports against pay statements) as the second layer: a verification column
  or file announces the correction by its schema, and a check sample selected on the reported pay either needs its
  selection filed (rule application) or left unstated (a hidden rule); the employer mix, which no column or sentence
  names, kept.
- A fixed panel of employers with 180-day arrival ramps and arrivals from January 2024: the panel's pooled slope fell
  to 2.66 per cent and its band points left the golden's bins; ramps cut to 60 days and arrivals from July 2024.
- Movement at 3.0 per cent a year within employers: whole months and linear carrying spread Data Engineer III's
  quartiles over $480 and no common window held all three points; movement set to 2.7 per cent and III's spread given
  a slight lean.
