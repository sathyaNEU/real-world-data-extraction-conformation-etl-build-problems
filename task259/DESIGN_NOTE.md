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
  what the band prices, moves only by how much the whole level's pay rises across filing dates.
- **Guard:** WARN three_rules.strategy_risk (grain_or_unit), answered by the analyst test: every field and rule read
  correctly still leaves the ageing rule open, and the easy routes (no ageing, or the re-reporters' own growth) are
  analysis, not readings. test.same_puzzle_older against task87 and the near driver task445 carry differentiation
  lines on the card. task257 (DA07) waits for a later draw day: its world's natural step is the duty-cycle mix
  (composition_mix), barred against task256 in the draw window.
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

## Tried and rejected

- DA09's own decisive step (the platform's data engineering family mixing machine-learning data engineers, removed
  through the profile table's primary focus): a filter on a field, data semantics under the 10/10 rules; kept as a
  lower rung.
- Calibration of the platform's respondents to OEWS state employment margins as the decisive step: the driver of
  task253 v1 (nonresponse within class), retired as a template; OEWS ships as a distractor and the policy names the
  matched respondents as the population.
