# task125 design note (architecture 2)

Re-rooted on the author's rule (no retiring). Architecture 1 (Wealdmoor County Council's digit filter, the 2027/28
call-off of routed payments) was solved in-house at rounds 1 and 2 and sent back by the determinism judge on hygiene
(the payments ledger read as generated); its record is the lines of the Tried and rejected section and its files are
gone from the folder. Carried forward: the decisive move must change the graded figure (a step linear in what the
solver already holds is no rung), and the pack must read as an organisation's own systems.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task125.json` (v2), registered 2026-10-12. `guard.py check`: WARN
  repeat.gate_g (forecasting in task124) and repeat.deliverables (docx and xlsx in task120). Answers: the forward
  figure here is pinned by the panel's own rotation once the recruitment selection is measured, with no trend or
  driver to extrapolate, so it is a different FINE-numbers shape from task124's pre-cool hours; a methods note with a
  chart and a quarter-by-quarter workbook is what a statistics office's methods division hands its head, so the
  format set stays. A first card (strategy population_selection, forum executive_team, forcing event
  budget_or_appropriation) was blocked against task124 and task120; the move reads as well as the panel's mix on a
  recruitment property moving under a correct pooled rate, so the strategy is `composition_mix`, the forum the head's
  line manager (the Government Statistician) and the forcing event the statutory July to September release.
  test.same_driver_older against task132 is differentiated on the card. At stage 3 the labels were re-read after
  guard.py surface (Build record): decisive gap time, G6 then G13, context artifact filed_standard.
- **Pairing:** Survey Research & Official Statistics (client domain), task type `anomaly-detection`, objective
  Anomaly Detection & Diagnostics. Never built before on this pairing or this task type. The anomaly is the July to
  September 2026 rise in the Household Labour Survey's unemployment rate; the diagnosis is how much of it, and of
  every published quarter to September 2027, is the first-interview visit limit rather than the labour market.
- **World:** a fictional English-speaking country (Merrowland), its national statistics office (Merrowland
  Statistics) and the Household Labour Survey (HLS): quarterly, a five-wave rotating panel of addresses, wave 1 face
  to face, waves 2 to 5 by telephone, person weights raked to population controls. From 1 July 2026 a field budget
  cut stops first interviews after three visits (six before). People (guard.py names, en_NZ, seed 125): Raewyn
  Bailey, Jane Phillips, Aaron Tucker, Dylan Fletcher; roles fixed at design.
- **Stakeholder and forum:** the head of labour market statistics (role `statistical_office_head`) must say in the
  July to September release (13 November 2026, forcing event `statutory_or_regulatory_filing`) whether the rise is
  real, and put to the Government Statistician (forum `line_manager_or_team`) what the visit limit does to the
  published rate through September 2027 if six visits return in January.
- **Shape 02 (forecast across periods):** the limit's distortion of the published rate in each quarter from July to
  September 2026 to July to September 2027, for the unemployment rate and the employment rate, with the real July to
  September change; arithmetic fixed at design.
- **Strategy and gate:** `composition_mix`, gate G `forecasting`, gap population then time, generators G6 then G13,
  pattern none, layer 2 `estimand_identification` (own:recruitment-selection-riding-a-rotating-panel).
- **Data-native sentence:** a household that needs a fourth visit to be found at home is one whose adults are out by
  day, mostly at work, and the panel keeps every household it recruits for five quarters, so a visit limit at
  recruitment removes the employed-heavy households from the sample for the next five quarters, not one.
- **Same-puzzle test:** task132 (population, none, forecasting) differentiated on the card; no build in the last
  twelve shares gap, pattern and decision type with a recruitment-protocol selection riding a panel. Nearest drivers
  0.08 (task500 v2) and under.
- **Sources (one line each):** `stumping/references/strategies.md` F5 (the mix moves under a correct pooled rate;
  here the property is rebuilt from the contact log joined to the panel, never a person-file column) and F1's
  current form (a clock already in the data: each intake's position in its five-quarter run); the client's
  continuum-of-resistance and fieldwork-effort literature teaches that late contacts differ, and this build differs by
  making the selected households persist through a rotating panel so the effect builds and outlasts the change.

## Default path

1. Read the July 2026 field instruction: first interviews stop after three visits; waves 2 to 5 are unchanged.
2. Take the latest uncapped first-interview intake (April to June 2026, wave 1 of the person file) and the call
   records' visit at which each household was interviewed.
3. Drop the households interviewed at a fourth to sixth visit, re-estimate the wave-1 unemployment and employment
   rates, and scale the change by wave 1's share of the quarter's economically active and of its population.
4. The limit adds that wave-1 gap to every quarter it runs (July to September and October to December 2026); with six
   visits back in January 2027 the published rates are clean again, so the gap is zero from January to September 2027.
5. The real July to September change is the published change less the wave-1 gap.

Ends on: the unemployment rate 0.22 point above the six-visit rate in each of the two capped quarters and 0.00 in each quarter of 2027 (the employment rate 0.74 below, then 0.00), the July to September rise mostly the cap.
Golden: the unemployment rate 0.22, 0.37, 0.25, 0.19 and 0.07 point above the six-visit rate from July to September 2026 to July to September 2027 (the employment rate 0.74, 1.37, 1.11, 0.93 and 0.63 below), 0.22 of the 0.27-point July to September rise the cap and 0.05 the labour market.

## Stump sentence

A competent solver finds the visit limit in the field instruction, measures how much dropping the households first
interviewed at a fourth to sixth visit moves the latest wave-1 intake, carries that wave-1 gap (0.22 point) through the two
capped quarters and files the published rates as clean from January 2027, the gap 0.00 in every quarter of 2027; the step that
lands it there is treating the limit as a first-interview effect, when the households a capped intake fails to recruit
would have stayed in the panel for five quarters, interviewed by telephone in waves 2 to 5 with their lower
unemployment partly persisting, so both capped intakes keep the published unemployment rate above the six-visit rate in
every quarter to September 2027.

## Three rules

- **Domain test:** the decisive analysis is the survey methodologist's: which households a contact protocol recruits,
  how long a rotating panel keeps them, how their selected outcomes regress over later waves, and how the calibrated
  estimator responds once they are gone; with another field's nouns there is no first-interview visit protocol, no
  intake riding five waves and no raked rate, so the task stops making sense.
- **Analyst test:** a strong analyst who reads the field instruction and the methods note correctly, takes ILO status
  as derived and the final weights as published, simulates the limit on the latest uncapped wave-1 intake, carries the
  gap while the limit runs and drops it to zero once six visits return, so the published rates are called clean from
  January 2027 when they still sit off the six-visit rates in every quarter to September 2027.
- **Layer 1:** wave-1 call records one row per visit with tablet re-syncs among the non-interview calls; household
  serials that gained a check digit in the July to September 2026 file; person numbers re-ordered when a roster
  changes; telephone interviews recording hours as hours and minutes while face-to-face interviews record decimal
  hours; population controls revised once in the period; a superseded field instruction beside the current one; a
  release table rounded to one decimal. Each is what these systems produce, and none decides the call.
- **Layer 2:** the shortcut is to treat a first-interview protocol change as a wave-1 effect; the expert follows the
  households the protocol recruits through every wave the panel keeps them, measures how their selected outcomes
  persist, and re-runs the calibrated estimator on each quarter's mix of capped and uncapped intakes.

## Readability screen

Each rung is the move a solver makes to leave the rung below; the decisive rung has to be silent on all six tests.

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0, wave-1 gap while the limit runs | yes, the instruction names first interviews and three visits | yes, the call records carry the visit number | yes | no | no | yes, one difference scaled by a share | readable |
| 1, the wave-1 gap carried into every later wave of each capped intake | no | no | yes, once the rotation is in view | no | no | yes, the same gap times wave shares | readable |
| 2, persistence by wave from the panel (decisive) | no: the instruction speaks of first interviews only, the methods note of rotation and estimation, nothing of a protocol's reach into later waves | no: no column marks a later-wave record as recruited at a fourth visit; the visit sits in the call records of the intake quarter, joined to waves 2 to 5 through the serial over up to four quarters | no: the reflexes (wave-1 simulation, a constant gap, a trend, a seasonal comparison) all land elsewhere | no: the release table and the admin claimant series tie under every basis | no: every key unique, every join matched once the check digit is handled | no: each quarter's gap is a re-estimate on a mix of intakes at different waves, not one figure scaled | silent |
| 3, the calibrated estimator re-run on the reduced sample | yes, the methods note says every estimate is raked to the population controls | no | partly, reweighting is a reflex but re-raking a counterfactual sample is not | no | no | no | readable |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternatives | Call under each | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the labour market rate | the rate the published estimator gives with six visits all along | the published rate before July 2026 carried forward | the default's ending, not a reading | the prompt's own wording ("what six visits all along would have given") |
| SF2 | unemployment rate | ILO unemployed over economically active, person weights, ages 15 and over | ages 15 to 64; unweighted | same call | the methods note's definition (asserted within 0.01 on the gap) |
| SF3 | employment rate | employed over population 15 and over | 15 to 64 | same call | the methods note's definition |
| SF4 | the quarter used to simulate the limit | April to June 2026, the last full quarter before the limit | an earlier quarter (January to March 2026, October to December 2025, July to September 2025) or several pooled | figures move by up to 0.11 point on the unemployment gap, every alternative still positive in every 2027 quarter | the methods note's section 5 ("the last full quarter collected before it"), asserted in checks.py; the build's tolerance (0.05 and 0.15 point) is stated in figures.json |
| SF5 | a household the limit would not have recruited | interviewed at wave 1 at a fourth, fifth or sixth visit | refusals; every non-contact | same call | the instruction's limit counts visits to an address; asserted |
| SF6 | re-estimation | re-rake to the population controls after dropping those households | keep their final weights; unweighted | rung 3 below, not a reading | the methods note: every estimate is raked to the controls |
| SF7 | the six-visit restoration | first interviews from 1 January 2027 | from the April to June 2027 intake | same call | the prompt's date |
| SF8 | the real July to September change | published change less the limit's July to September gap | year-on-year | same call | the prompt asks between April to June and July to September |
| SF9 | rounding | hundredths of a point, from unrounded estimates | rounding each rate first | same call | the prompt; asserted |

## Ladder

Built values (asserted in checks.py by name). Gap = published rate less the six-visit rate, points; unemployment rate
first, employment rate below it.

| Rung | Construction | Jul-Sep 26 | Oct-Dec 26 | Jan-Mar 27 | Apr-Jun 27 | Jul-Sep 27 |
|---|---|---|---|---|---|---|
| 0, default | the wave-1 gap while the cap runs, zero after | 0.22 / -0.74 | 0.22 / -0.74 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 |
| 1 | the wave-1 gap carried unchanged at each later wave of the two capped intakes | 0.32 / -1.23 | 0.60 / -2.32 | 0.54 / -2.11 | 0.49 / -1.94 | 0.42 / -1.71 |
| 2 | per-wave removal on April to June 2026, final weights kept | 0.24 / -1.14 | 0.41 / -2.14 | 0.29 / -1.78 | 0.23 / -1.51 | 0.10 / -1.09 |
| 3, golden | per-wave removal on April to June 2026, re-raked | 0.22 / -0.74 | 0.37 / -1.37 | 0.25 / -1.11 | 0.19 / -0.93 | 0.07 / -0.63 |

- **Position:** rung 0 puts every 2027 cell at zero; the golden puts every one above the tolerance (0.07 the smallest
  unemployment cell against 0.05, -0.63 the smallest employment cell against 0.15).
- **Margins:** rung 0 off the golden by at least 0.07 and 0.63 point in every 2027 quarter and by 0.15 and 0.63 in
  October to December; rung 1 by at least 0.29 and 1.00; rung 2 by at least 0.40 on the employment gap in every
  quarter (its unemployment gaps fall inside the tolerance, so rung 2 costs the employment half only).
- **Dominance:** the decisive move (persistence through the panel) is the only one that moves 2027 off zero; decay and
  re-raking together bring the carried gap down to the golden.
- **Grid:** wave-1 only, carried constant, carried by the panel; final weights or re-raked: six paths, each asserted.
- **Worth:** the decisive move carries the six 2027 cells of the two rates and the October to December pair; re-raking
  carries every employment cell.
- **July to September split:** published unemployment 4.99 to 5.27 per cent (a 0.27-point rise), 0.22 of it the cap,
  0.05 the labour market (5.04 without the cap); employment 60.01 to 59.36, -0.74 the cap, +0.09 the labour market.
  The simulation's own July to September gap (published less the six-visit counterfactual intake) is 0.21, against the
  estimate's 0.22 (information, asserted within 0.12).

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | persons 15 and over in the responding households of the quarter's five intakes | filed in the methods note; C1 |
| 2 | Unit of account | the person for rates, the address for the limit | filed: the instruction counts visits to an address |
| 3 | Attribution window | survey quarter | filed in the methods note |
| 4 | As-of dating | microdata to July to September 2026 as locked 20 October 2026 | filed in the extract notes |
| 5 | Version basis | final weights; population controls as revised | C1: the revision predates the template quarter (asserted) |
| 6 | Denominator | economically active (unemployment rate), population 15+ (employment rate) | filed definitions |
| 7 | Weighting | raked person weights | filed in the methods note; SF6 |
| 8 | Window length | the template quarter | SF4 |
| 9 | Boundary inclusivity | fourth visit and later | SF5 |
| 10 | Rounding path | hundredths of a point from unrounded estimates | the methods note section 7 (changes from unrounded estimates, rounded independently); SF9 |
| 11 | Tie-break | none | no decision turns on a tie |
| 12 | Maturity and censoring | the July to September 2026 file complete at lock | filed in the extract notes |
| 13 | Order of operations | drop households, re-rake, estimate | asserted |
| 14 | Row order | none | C1 over permutations |
| 15 | Duplicate resolution | call records' re-syncs are non-interview rows; the visit of interview is unique per address | asserted |
| 16 | Identity normalisation | address serial across files, check digit dropped in July to September 2026 | asserted |
| 17 | Netting | none | not applicable |
| 18 | Dimensional units | percentage points; hours | dictionary |
| 19 | Code semantics | ILO status codes, call outcome codes | dictionary; never the stump |
| 20 | Integerisation | counts integers | C1 |
| 21 | Clause scope | the limit binds first interviews from 1 July to 31 December 2026 | filed in the instruction and the prompt |
| 22 | Forward window contents | intakes, waves and controls to September 2027 | the template quarter's structure; controls held at their latest vintage |

## Literal reader

Executing the prompt and the shipped documents word for word: the gap in a quarter is the published estimator's rate
less the rate it would give had first interviews had six visits all along; the limit removes, from every intake issued
from 1 July to 31 December 2026, the households first interviewed at a fourth to sixth visit; the panel keeps each
intake five quarters; the methods note assesses a fieldwork change by applying it to the last full quarter before it
and raking every estimate to the population controls. So each quarter's gap is April to June 2026 re-estimated without
those households in the waves the capped intakes will occupy that quarter. Every reading in SF1 to SF9 returns the
golden path; the default path comes from the same estimand by applying the change to wave 1 only.

## Oracles

- The release table to April to June 2026: the published rates the microdata reproduces; ties under every basis.
- The administrative claimant count: a different concept on a benefit rule changed in 2025; moves with the labour
  market, blind to the limit; ties under every basis (a distractor).
- The July to September 2026 microdata: its wave-1 rate jumps with the limit; it shows the wave-1 gap the default
  already takes and nothing about later waves.
- None ties only under the golden.

## Ask sheet

The main call's declared row population: the person file's April to June and July to September 2026 records (columns
serial, wave, quarter, ILO status, age group, sex, region, final weight), the call records' interview rows for the
intakes of April to June 2025 to April to June 2026 (serial, visit number, outcome), the population controls and the
methods note. Person numbers, hours and every non-interview call row are outside it. Each ask is a measure the quarterly
fieldwork and quality report carries for every region beside the headline (H18 home: an audit trail of the call's
inputs, the intake's visits, the panel's flows and the employed's hours), on which the call does not turn; none is keyed
to the call or its construction, and the three share no primary family and no file path. No sentence in the pack
adjudicates a device.

**Ask 1. First-interview visits made to the July to September 2026 intake, each region (6 whole numbers).**
- Use: the field budget the limit was meant to save, read beside the call.
- Primary device (D1, a replay under fresh ids, key kept): the call-record app re-sent part of the non-interview calls
  logged offline after an August update, each re-sent call under a new record id with the same serial, visit number and
  visit time and a later upload time; counted as rows every region is high. Only an internal inconsistency finds it:
  two calls to one address with the same visit number and minute.
- Reading pin (judge pass 1): the methods note's section 2 identifies a visit by the address serial and its visit
  number; it says nothing of uploads.
- Over-cleaning hazard: interviewers call twice on one day (afternoon and evening), so a de-duplication on serial and
  date drops real visits; on serial and visit number it is exact.
- Shared hazard: the serial's check digit in the July to September file (region comes from the address register).
- Span (3 files, 8 columns): call records, address register, field instruction.
- Ladder (asserted): rows counted (the cracker, Velmouth 4,059 against 3,945, every region high); de-duplicated on
  serial and date (every region low, Velmouth 3,790); golden.

**Ask 2. Of the respondents unemployed in April to June 2026, the share employed in July to September 2026, each
region (6 figures, percent to two decimals).**
- Use: the flows the release carries beside the rate, telling a moving labour market from a protocol.
- Primary device (D7, the true key in another field): the telephone system lists a household's members oldest first,
  the face-to-face interview in the order they were entered, and a member who leaves shifts the rest up; a join on
  serial and person number pairs different people in those households, the joined pairs pass every check (one match
  each) and every region moves. Only sex and date of birth disagreeing across a pair shows it.
- Hazard: the check digit (shared with ask 1); wave-1 newcomers in July to September with no April to June record.
- Span (2 files, 9 columns): person file, data dictionary.
- Reading pin (judge pass 1): the methods note's section 6 counts flows on people interviewed in both quarters,
  unweighted; it names no key.
- Ladder (asserted): joined on serial and person number (the cracker, every region off, Velmouth 37.07 against
  30.77); joined on serial alone (fan-out, every region off); golden, serial, sex and date of birth (one match each).

**Ask 3. Total weekly hours actually worked by the employed in July to September 2026, each region (6 figures,
thousands of hours to one decimal, final weights).**
- Use: the hours the release carries, read for intensity beside the rate.
- Primary device (D3, units set per source): telephone interviews store hours and minutes as h.mm (37.30 for 37 hours
  30 minutes) while face-to-face interviews store decimal hours; summed as decimals every region is low by about 0.3
  per cent (Velmouth 26,963.2 against 27,055.5 thousand, asserted). Only the telephone values' fractions never
  exceeding .59, against the face-to-face quarter hours, show it.
- Over-correction hazard: converting every value as h.mm, face-to-face decimals included, puts every region high.
- Referee (judge pass 1): the release table's national total actual weekly hours for each quarter to April to June
  2026, which only the converted telephone hours reproduce (raw sums miss by more than 50 thousand in every quarter,
  asserted); it fixes the level without a sentence naming the encoding.
- Span (2 files, 7 columns): person file, data dictionary.
- Ladder (asserted): raw sum (the cracker); every value converted; golden.

**The cracker sheet.** The cracker landed the call, ran the hygiene battery (keys unique, no exact duplicates, every
join matched) and executed every filed rule:

| Ask figures | The cracker's path | What keeps it wrong | Cracker result |
|---|---|---|---|
| Ask 1, visits (6) | call rows of the July to September intake counted by region | re-sent calls under fresh ids inflate every region | miss |
| Ask 2, flows (6) | April to June and July to September joined on serial and person number | re-ordered person numbers pair different people | miss |
| Ask 3, hours (6) | weighted sum of the hours column for the employed | telephone hours are hours and minutes | miss |
| Chart (rec block, not an ask) | carried by the main call | scored with the recommendation | outside |

The mirror sheet (stopped at rung 0) differs from the cracker sheet only on the recommendation criteria and the chart.

Mirror leakage: 8 per cent of the ask weight (method credit on the ask paths, no figure).

**Pair arithmetic.** Planning weights 38 recommendation, 7 instruction following, 55 asks over 18 ask figures. With
r = 6 (the July to September cells a wrong path keeps) and each top response keeping about 8 per cent of the ask weight:
C = 38 + 7 + 4.4 = 49.4 for the cracker, S = 6 + 7 + 4.4 = 17.4 for the mirror.

Pair ceiling: 33.4

## Pins

- The definitions, the raking to region and age-sex controls, and the rule for assessing a fieldwork change on the last
  full quarter before it: the methods note (sections 3 to 5), once.
- The cap (three visits, first interviews, from 1 July 2026, the 2027 pattern set with the 2027 budget): FI-2026/07,
  once; the six-visit return in January 2027 is the prompt's scenario.
- Ask readings: none filed; each ask's wording fixes its quantity (visits to the intake, the share of the April to June
  unemployed in work, the employed's weighted total hours). No sentence adjudicates a device.

## Stopping rule

Two portal solves of the 2027 path by different routes re-root the decisive step; a determinism finding that the
template quarter is open is closed in the methods note's wording, never by moving the stump; a solve landing the path
from a filed sentence sends that sentence out of the pack and the build back to design.

## Build record

- Realisation: the sampling noise is fixed by world.SALT = 13 (of 24 scanned for a quiet 2025 to 2026 series and a
  July to September rise mostly the cap), and the July to September 2026 labour market multiplier at 1.14 puts the
  labour market's share mid-bin (0.049); the gap path depends on April to June 2026 only and does not move with it.
- Gates (stage 3): 204 checks, the independent verifier, two byte-identical builds, figures_check (120 figures),
  scrub audit clean on the pack and the goldens, precut 38 of 38, leak.py REVIEW (the outcome code 110 matching a
  denominator, and stump vocabulary from architecture 1's lines), guard check WARN (repeat.gate_g, repeat.deliverables)
  and heart WARN.
- guard.py surface promoted card-signature pairs only (task126 back to back on gap and decision type under the first
  labels, task132 and task501 v3 on gap, pattern and Gate G); the labels were re-read at stage 3 (gap time first, G6
  then G13, context artifact filed_standard) and the card carries differentiation lines for task132 and task501 v3.
  No surface (vocabulary, file name, persona) overlap was found; the adjudicated /clone-check is the author's call.

## Judge record

- Pass 1 (2026-10-12): DETERMINISTIC, FIX_NOW. The call, the July to September split and the whole gap path reproduced
  to two decimals; licensed variants (re-raking from the file weights, each quarter's own controls) agree to three
  decimals. Findings on the asks only: the telephone hours encoding, the flow denominator and weighting, rows against
  visits, and the rounding path. Gate G: decomposition_attribution, analytical_non_defect, no surface read, no sole
  defect. Gate H: pass, decisive step analytical (borderline rule application through section 5, which states the
  base quarter and the raking but not the rotation bookkeeping or the persistence). Repairs, one generator pass:
  methods note sections 2, 6 and 7 (visit identity, flows, rounding from unrounded estimates) and the release table's
  total actual weekly hours as a referee; a dictionary line naming the h.mm encoding was declined as narrating the
  device.
- Pass 2 (2026-10-12): DETERMINISTIC, APPROVE, no rerun. Every figure reproduced from target/ alone, the regional asks
  included (visits once the re-uploads go, flows on people interviewed in both quarters, hours converted, which the
  release's April to June total of 85,762.5 thousand confirms against 85,492.6 raw). Alternatives checked: each target
  quarter's own controls (same to four decimals), no re-rake and capping every wave (ruled out by sections 4 and 5 and
  the rotation). Stump power moderate: the direction (cap, not labour market) is easy; the difficulty is the five-quarter
  path, its October to December peak and its tail. Gate G decomposition_attribution with forecasting of the carry-
  through, analytical_non_defect; Gate H pass, decisive step analytical.

## Pre-ship check

- Call: almost none of the July to September rise is the labour market (0.22 of 0.27 the cap, 0.05 the labour market);
  with six visits from January 2027 the unemployment rate sits 0.37, 0.25, 0.19 and 0.07 point above the six-visit rate
  to July to September 2027, the employment rate 1.37, 1.11, 0.93 and 0.63 below.
- Default path: the wave-1 gap while the cap runs and nothing from January 2027 (0.22, 0.22, 0.00, 0.00, 0.00); both
  isolated readers took it or its equivalent.
- Gates: 221 checks, independent verifier, two byte-identical builds, figures_check 120 figures, precut 38 of 38, scrub
  clean, leak.py REVIEW read (no leak), reader twice no leak, judge pass 2 APPROVE, guard heart WARN.
- Deliverables: hls_visit_limit_note_2026q3.docx (two pages, chart and table), hls_visit_limit_path_2027.xlsx (gap
  path, July to September split, regions, notes); target.zip from the final rebuild, 12 files.
- Card current: answer, spine rows 491,673, deliverables, labels as re-read at stage 3.

## Tried and rejected


- The source note's decisive rung (Housing Support's cohort run off on the 2021 intake's 30-instalment term) as the decisive rung: the pilot's plain solver replays records at the finest grain and runs event studies on staggered cohorts, and the 2021 intake's full rise and run-off sits in the same flagged-cell series, so a strong solver constructs it; kept as rung 3.
- Re-pricing Adult Social Care's standing stream at a 2027/28 tariff filed in the council's budget (band 2 from 366 to 399 a week, out of cell 14): honestly labelled (time, A) or (time, G13), which the guard blocks inside the batch (task121 v1 lineage) and as spent in ten older builds, with G13 task122's decisive generator; a relabel to G11 or G6 would not name the move as a reviewer would. It also hangs on a stated rate one multiplication from the digit consequence.
- An upward entrant move with the cohort drop under about a sixth of the closed-year figure: the run-off (down) and the entrants (up) cancel near the closed-year carry-forward, which then lands inside 10 per cent of the answer (L4); the targets keep the drop near 30 per cent.
- Step-down hosts inside the flagged cell, paid the same 1,464 as long-term band 2 hosts and separable only by the turnover pattern in their payment histories (a downward decisive move): its honest label is G3 (record versus operation), task121's decisive generator, and the affected payments sit in the very cell the solver is already examining.
- A guest-level arrangements register in the pack: it turns the carers' composition into a schema-visible join from payee to guests, RC01 v2's death (a two-hop join found from the schema alone) and FC01 loop 2's (a dated attribute of an entity the chain already joins); not shipped.
- Landlord-consolidated remittances in the Tenancy Sustainment scheme (a landlord's monthly payment falling into cell 14 once one household remains): the forward entrants are a few per cent of the answer at any realistic landlord mix, too small for a decisive rung.
- A fourteenth four-weekly cycle in 2027/28 (a 366-day year with a payment date on 1 April 2027) or a 53-Thursday year as a rung: worth 2 to 8 per cent of one stream, a knife-edge hazard; the design picks cycles that add no plan-year date unless it prices the cell.
- A plan-year move from four-weekly to monthly payment, or to fortnightly payment runs: a stated change the solver applies at first order, and its amount consequence sits on the remittance grain a screen rung already validates.
- The filter's own examination holds merging held payments into the next run: a council's digit filter examines after payment, and the merge timing opens forks the judge would read as unpinned.
- The 2025/26 screen close-out as the context artifact (close_out_summary): blocked at registration by ban.artifact against task124, drafted in parallel; the same closed-year figures ship in the filter's 2025/26 run log (operations_log).
- One step-down rate with 70 dual carers on one combined amount (3,044): 910 payments a year land in Adult Social Care cell 30, which then flags itself on the 2025/26 screen (paper ratio about 1.4), so the closure moves payments from one flagged cell to another and the decisive rung is worth zero; three tiers and 60 carers keep every Shared Lives cell under 0.86 of threshold.
- Twins identical on every statement figure (payments tested and MAD as well as the cell-14 count): Housing Support would need about 50,000 payments a year in range, which a county's housing-related support service cannot carry; the twin is held on the run log's 2025/26 line only.
- A second plan-year monthly series for the department that moves most (the draw's criteria arithmetic): a denser split of the committed figure, twelve more criteria the cracker banks free; replaced by the two 2025/26 tables.
- Annotating the plan-year month furthest from the closed-year line: January, February and March 2028 tie at 476 routed payments, an ungradable part; the busiest month (December 2027, 638 by run month) is annotated instead.
- The 2027/28 payment-run calendar on the main path, with "four weeks ending on the run date" as the pin against a 12-run reading: unnecessary, since the 28-day cadence fixes 13 runs and a 12-run reading files the same hundred; kept for the monthly ask only, so the main path carries no file an ask device lives in.
- The spending file from April 2021 with every department's background (build): about 100 MB of CSV; the file starts April 2023 and the 2021 round's histories ship in the Housing Support case extract, which is where the term pin lives anyway.
- Waste & Environment cell 25 as the run log's extra cell (build): a cell-25 count near 500 under 0.86 of its threshold needs a Waste department of more than 22,000 payments a year; cell 11 reaches it with 11,000.
- The rung-1 lever at net cell 20 with Property & Facilities at 7,400 invoices (build): rung 1 landed 8,348, and the net basis with the run-off applied then filed 6,458, inside the answer's hundred; the gross cells 20 to 25 had no room for more bills, so the lever moved to net cell 15 and rung 1 to 8,992.
- Rung 4 (Shared Lives carers' combined amounts decomposed against the weekly rate schedule, step-down placements dropped) as the decisive rung, round 1: the plain solver landed 6,522, filed 6,500, by listing the carer amounts against the rates at its step 4 in its own words, "On each carer pay date, 102 payments are £1,464, and 22 + 20 + 18 more are £1,464 plus a step-down rate (£3,044, £3,272, £3,524). When Home First step-down closes on 31 March 2027 those 60 drop to £1,464". The noisy amount universe did not hide them: the three combined amounts are the only carer amounts equal to 1,464 plus a step-down rate, so the decomposition is one subtraction, not a construction.
- Harden loop 1 (opening line), rung 4 as the decisive rung measured by round 1 plain (proxy 80.2, call landed at path step 4): the solver read every "Shared Lives carer payments" row as one carer's whole fee, summed at the carer grain in its own words, "ASC total: 115 x 12 + 162 x 13 = 3,486", having climbed rungs 2 and 3 and stepped over the side cell by taking the 2025/26 cells; a louder pin, a second decoy or a noisier amount list would only lengthen the same subtraction, so the repair attacks the assumption the sentence holds fixed (one row is one carer's fee) rather than the decomposition itself.
- Rung 5 (joint households' half-fees at the household grain) as the decisive rung, round 2 plain (proxy 85.1, call landed at path step 4, filed 6,700): the solver never constructed the household grain; it decomposed each half against the rate card on its own, read the 2,274, 2,388 and 2,514 halves as two weeks of each rate, dropped the step-down weeks and got 1,484 per vendor, in its own words "2,274/2,388/2,514, which leave 1,484 (16). That gives 178 per run". The halves are linear in the household fee, so halving the rates gives the same result as re-summing the household and halving it again; the grain gap never moves a single vendor's post-closure amount, and the rung cannot change the answer (discriminator dominance failed, not silence).
- Harden loop 2 (opening line), rung 5 as the decisive rung measured by round 2 plain (proxy 85.1 after the --landed yes regrade, call landed at path step 4): the solver treated each joint half as two weeks of each weekly rate, in its own words "2,274/2,388/2,514, which leave 1,484 (16). That gives 178 per run", so a grain step whose arithmetic is linear in the fee (halve, then subtract the halved step-down rate) can never move a vendor's post-closure amount; the repair has to make the household grain change the result, which only a non-linear step at that grain (a household-level threshold, cap or rate that a half cannot see) can do.
- Centring the loop 2 answer at 6,902 by trimming a flat stream by one payment a month (Property & Facilities 81 to 80, or Highways cell 49 66 to 65): the 2025/26 batch returns are drawn per payment, so the trim reshuffled the examined counts and put both unused-volume charges 2 pence off a half-pound edge (1,604.48 and 603.52 or 655.04); loop 1's stream counts were kept, the answer is 6,914 (36 from its upper edge) and asks B1, B2 and C are unchanged.
- The whole build after harden loop 2 (rung 6, the joint-household one-guest payment rule, as the decisive rung; round 3 plain missed at 43.3): the determinism judge returned SEND_BACK on 2026-10-10 with the mechanism matching the note on every field, so the build was retired and not submitted.
- Architecture 1 as a whole (2026-10-12, at the re-root): spent by two in-house solves and a judge SEND_BACK; the
  author's no-retirement rule re-roots the slot to architecture 2 on a new pairing.
- Interviewer falsification in a victimisation survey (2026-10-12, at the draw, never registered): fabricated
  interviews are wrong records, so catching them is a planted defect under the three rules whatever the method.
- A sample boost entering all at wave 1 against rotation-group bias (2026-10-12, at the draw): the first-interview
  bias moves a regional rate by about 0.1 point at any realistic boost, too small to carry a call.
- A staggered web-first rollout read by event time (2026-10-12, at the draw): the arm comparison and the per-wave
  phasing are what a survey-literate solver does first, and every estimator choice opens a numeric fork.
