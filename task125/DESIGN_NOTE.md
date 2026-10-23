# task125 design note (architecture 2, ladder re-rooted at stage 2)

Architecture 1 (Wealdmoor County Council's digit filter) was solved in-house twice and sent back by the determinism
judge; architecture 2 drew Merrowland Statistics' Household Labour Survey. Architecture 2's first ladder shipped, was
measured by a blind reader holding only a fresh unzip of `target.zip`, `prompt.txt` and the figure names, and failed
Gate F: the reader took 2 of 2 call figures and 38 of 53 ask figures, and quoted the methods note's section 5 as what
told it the decisive step ("the effect of a change is measured by applying the change to the last full quarter
collected before it and re-running the estimation as in section 4"). The pack stated the method, so executing it was
rule application. This ladder is re-rooted at stage 2 on the same draw: section 5's procedure sentence is gone, the
base quarter is settled by the records rather than by a sentence, and the cap now runs long enough that the decisive
step carries the call itself rather than only the forward path.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task125.json` (v2), registered 2026-10-12, re-read at this re-root.
  `guard.py check`: WARN repeat.gate_g (forecasting in task124) and repeat.deliverables (docx and xlsx in task120).
  Answers: the forward figure here is pinned by the panel's own rotation once the recruitment selection is measured,
  with no trend or driver to extrapolate, so it is a different FINE-numbers shape from task124's pre-cool hours; a
  methods note with a chart and a quarter-by-quarter workbook is what a statistics office's methods division hands its
  head, so the format set stays. Strategy `composition_mix`, forum the head's line manager (the Government
  Statistician), forcing event the statutory July to September release. test.same_driver_older against task132 is
  differentiated on the card. Labels at stage 3: decisive gap time, G6 then G13, context artifact filed_standard.
- **Pairing:** Survey Research & Official Statistics (client domain), task type `anomaly-detection`, objective Anomaly
  Detection & Diagnostics. The anomaly is the July to September 2026 rise in the Household Labour Survey's published
  unemployment rate; the diagnosis is how much of it, and of every published quarter to September 2027, is the
  first-interview visit cap rather than the labour market.
- **World:** a fictional English-speaking country (Merrowland), its national statistics office (Merrowland Statistics)
  and the Household Labour Survey (HLS): quarterly, a five-wave rotating panel of addresses, wave 1 face to face,
  waves 2 to 5 by telephone, person weights raked to population controls. For the 2026/27 field year (1 April 2026 to
  31 March 2027) a field budget cut stops first interviews after three visits (six before and after). People
  (guard.py names, en_NZ, seed 125): Raewyn Bailey, Jane Phillips, Aaron Tucker, Dylan Fletcher.
- **Stakeholder and forum:** the head of labour market statistics (role `statistical_office_head`) must say in the
  July to September release (13 November 2026, forcing event `statutory_or_regulatory_filing`) whether the rise is
  real, and put to the Government Statistician (forum `line_manager_or_team`) what the cap does to the published rates
  through September 2027 once six visits return in April.
- **Shape 02 (forecast across periods):** the cap's distortion of the published rate in each quarter from July to
  September 2026 to July to September 2027, for the unemployment rate and the employment rate, with the April to June
  to July to September change decomposed; arithmetic fixed at design.
- **Strategy and gate:** `composition_mix`, gate G `forecasting`, gap population then time, generators G6 then G13,
  pattern none, layer 2 `estimand_identification` (own:recruitment-selection-accumulating-through-a-rotating-panel).
- **Data-native sentence:** a household that needs a fourth visit to be found at home is one whose adults are out by
  day, mostly at work, and this panel keeps every household it recruits for five quarters, so a cap on recruitment
  visits removes the employed-heavy households from the sample for five quarters per intake and its effect on the
  published rate compounds for as long as the cap is issued, which is why the quarter-on-quarter change it causes is
  nothing like the gap it causes.
- **Same-puzzle test:** task132 (population, none, forecasting) differentiated on the card; no build in the last
  twelve shares gap, pattern and decision type with a recruitment-protocol selection compounding through a panel.
  Nearest drivers 0.08 (task500 v2) and under.
- **Sources (one line each):** `stumping/references/strategies.md` F5 (the mix moves under a correct pooled rate; here
  the property is rebuilt from the contact log joined to the panel, never a person-file column) and F1's current form
  (a clock already in the data: each intake's position in its five-quarter run); the client's
  continuum-of-resistance and fieldwork-effort literature teaches that late contacts differ, and this build differs by
  making the selected households persist through a rotating panel so the effect accumulates across overlapping
  intakes and outlasts the change.

## Default path

1. Read FI-2026/04: first interviews are capped at three visits for addresses issued from 1 April 2026, and telephone
   interviews at waves 2 to 5 are unchanged.
2. Take the interview visit of each address from the call records (the visit number of its interview call) and join it
   to the person file on the serial: the households a three-visit cap would not have recruited are those interviewed
   at a fourth, fifth or sixth visit.
3. Take the last quarter collected before the cap, January to March 2026, drop those households from its wave-1
   intake, re-rake the rest to the population controls and read the change in each rate.
4. A fieldwork change changes that quarter's fieldwork, so the gap applies to wave 1 in each quarter whose intake is
   issued under the cap and is zero once six visits return.
5. April to June and July to September 2026 therefore carry the same wave-1 gap, so the cap contributes nothing to the
   change between them and the whole published rise is the labour market.

Ends on: the unemployment rate 0.21 point above the six-visit rate in each quarter whose intake is capped and 0.00 from April to June 2027 (the employment rate 0.79 below, then 0.00), and none of the 0.27-point July to September rise the cap, so the rise is real.
Golden: the unemployment rate 0.39, 0.53, 0.62, 0.47 and 0.28 point above the six-visit rate from July to September 2026 to July to September 2027 (the employment rate 1.42, 1.97, 2.44, 1.88 and 1.19 below), 0.18 of the 0.27-point July to September rise the cap and 0.09 the labour market.

## Stump sentence

A competent solver finds the cap in the field instruction, measures how much dropping the households first interviewed
at a fourth to sixth visit moves a wave-1 intake, and files that one wave-1 gap (0.21 point) for every quarter the cap
is issued and 0.00 from April to June 2027, with none of the 0.27-point July to September rise the cap, so the rise is
real; the step that lands it there is taking the unit the change acts on to be the quarter's fieldwork, when it is the
intake, which the panel keeps for five quarters, so each published quarter is a mix of capped and uncapped intakes, the
gap compounds to 0.62 point by January to March 2027 and the change between two quarters that are both capped is the
change in the mix, not zero.

## Three rules

- **Task type:** anomaly-detection in Survey Research & Official Statistics (a break in a published series diagnosed
  against the survey's own design), which serves Anomaly Detection & Diagnostics in the client's taxonomy.
- **Domain test:** the quantity that decides the call is the survey methodologist's: what a calibrated estimator built
  on a rotating panel reports when a recruitment protocol selects which households enter each intake, how long the
  panel keeps them, and how their selected outcomes regress over the later waves. It is estimated the way a statistics
  office estimates the effect of a fieldwork change, by rebuilding the published estimator on the sample the change
  would have left, intake by intake and wave by wave.
- **Swap:** "how much of the July to September rise in the unemployment rate is the labour market, and how far will the
  three-visit cap on first interviews hold the published rates off the six-visit rates to September 2027" with another
  field's nouns becomes "how much of the rise in the defect rate is the process" and stops making sense at once: there
  is no first-interview visit protocol selecting which units enter, no five-quarter rotation keeping each intake, no
  overlapping intakes making one period's estimate a mix of two fieldwork regimes, and no raking to population
  controls for the removal to move through.
- **Layer 1:** wave-1 call records one row per visit with the call-record app's re-sends among the non-interview calls;
  household serials that gained a check digit at the July to September 2026 processing run; person numbers re-ordered
  between waves when a roster changes; telephone interviews recording hours as hours and minutes while face-to-face
  interviews record decimal hours; population controls rebased once in the period; a superseded field instruction
  beside the current one; the call-record application replacing paper call sheets at the January to March 2025 intake;
  a fiscal field year against calendar quarters; a release table rounded to one decimal. Each is what these systems
  produce, and none decides the call.
- **Layer 2:** the shortcut is to treat a change to first-interview fieldwork as a property of the quarter's
  fieldwork; the expert treats it as a property of the intake, follows each capped intake through the five quarters
  the panel keeps it, measures how the selected households' outcomes persist and decay across the telephone waves,
  re-runs the calibrated estimator on each quarter's own mix of capped and uncapped intakes, and reads the
  quarter-on-quarter change off the change in that mix.
- **Decisive step:** the unit of analysis is the intake, not the quarter, so the counterfactual is rebuilt for each
  target quarter on the waves that quarter's capped intakes hold, and the cap's share of a change between two quarters
  is the change in the gap rather than the gap.
- **Not semantics:** every field, code, unit and definition read correctly leaves the easy route on 0.21 point in each
  capped quarter and 0.00 after, and on none of the rise. No column, code or definition marks a later-wave record as
  one recruited under the cap; the visit number sits in the call records of the intake quarter and reaches waves 2 to 5
  only through the serial, and the one quarter the counterfactual can be rebuilt on is identified by what the records
  cover, not by what any field says. Reading `wave`, `intake`, `ilo_status` and the h.mm hours perfectly changes no
  graded figure of the call.
- **Not rule application:** no shipped sentence says how the effect of a fieldwork change is measured, which quarter
  to rebuild it on, or that a recruitment change reaches past wave 1. The methods note files the design, the
  definitions, the raking and the sampling error, and the field instruction files the cap and says telephone
  interviews at waves 2 to 5 are unchanged, which is true and pulls the other way. Executing every filed rule gives
  the default path's answer. **Said plainly: this line is the one that is argued rather than measured.** The decisive
  step is a choice of the unit of analysis, which `CLAUDE.md` rule 3 counts as analysis, but once that choice is made
  the construction is exact arithmetic on recorded fields rather than an estimation, because a cap is a subsetting of
  a sample and the pre-cap quarter observes the subset it removes. The architecture therefore has no estimated
  quantity in the deciding position and no open estimator family (measured: 3e-06 point of spread on the unemployment
  gap across six licensed variants); its defence against rule application rests entirely on the unit-of-analysis
  carve-out and on the pack no longer stating the construction.
- **Analyst test:** a strong analyst who reads the field instruction and the methods note correctly, takes ILO status
  as derived and the final weights as published, identifies the capped-out households exactly and rebuilds the
  estimator properly, but treats the cap as a wave-1 effect, files the unemployment rate 0.21 point above the
  six-visit rate in each quarter whose intake is capped and 0.00 from April to June 2027 (the employment rate 0.79
  below, then 0.00), and none of the 0.27-point July to September rise the cap, so the rise is real.
- **Estimand:** for each quarter, the HLS published estimator's rate less the rate the same estimator would give had
  first interviews had six visits throughout, for persons aged 15 and over in the responding households of the
  quarter's five intakes, in percentage points on the published rates; the population, the definitions, the raking and
  the unit sit in the methods note's sections 1, 3, 4 and 5 and the prompt's own wording ("what six visits all along
  would give"), and the window and the comparison quarters sit in the prompt.
- **No decoy:** nothing is planted to be caught. There is no memo, draft, briefing or stakeholder figure arguing the
  wrong answer, no copied block, no withheld rule. The sentence the default path leans on (telephone interviews at
  waves 2 to 5 are unchanged) is a true operational fact about the telephone protocol, shipped because a real
  instruction says it; the easy route misreads it as a fact about the sample, which is an inference the pack never
  makes.
- **No certified replay:** the method is not hidden and recovered by reproducing a published figure. The release table
  reproduces under every rung and every basis (asserted); the claimant series is blind to the cap; nothing in the pack
  ties only under the golden construction.
- **Lesson:** a protocol change at the point of recruitment acts on the intake, not on the period, so in a rotating
  panel its effect on a published series compounds while it is issued and decays after it stops, and the change
  between two periods inside its run is the change in the mix of regimes rather than the effect itself. No build on
  file teaches it: the nearest, task132, moves a population property under a correct pooled rate within one period.

## Readability screen

Each rung is the move a solver makes to leave the rung below; the decisive rung has to be silent on all six tests.

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0, the wave-1 gap in each capped quarter | yes, the instruction names first interviews and three visits and says waves 2 to 5 are unchanged | yes, the call records carry the visit number | yes | no | no | yes, one difference scaled by a share | readable |
| 1, that gap carried unchanged into every later wave of each capped intake | no | no | yes, once the rotation is in view | no | no | yes, the same gap times wave shares | readable |
| 2, the intake as the unit: per-wave removal on each quarter's own mix (decisive) | no: the instruction speaks of first interviews only, the methods note of design, definitions, estimation and sampling error, nothing of a recruitment change's reach into later waves or of how a change is measured | no: no column marks a later-wave record as recruited under the cap; the visit sits in the call records of the intake quarter and reaches waves 2 to 5 through the serial over up to four quarters, and no field says which quarter the counterfactual can be rebuilt on | no: the reflexes all land elsewhere, measured (no adjustment, wave-1 simulation, a constant carried gap, the rotation-group difference in differences, the matched-panel change, year on year) | no: the release table and the claimant series tie under every basis | no: every key unique, every join matched once the check digit is handled | no: each quarter's gap is a re-estimate on a different mix of intakes at different waves, and the cap's share of a change is a difference of two such re-estimates | silent |
| 3, the calibrated estimator re-run on each reduced sample | yes, the methods note says every published estimate uses the raked weights | no | partly, reweighting is a reflex but re-raking a counterfactual sample is not | no | no | no | readable |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternatives | Call under each | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the six-visit rate | the rate the published estimator gives with six visits all along | the published rate before April 2026 carried forward | the default's ending, not a reading | the prompt's own wording ("what six visits all along would give") |
| SF2 | unemployment rate | ILO unemployed over the labour force, person weights, ages 15 and over | ages 15 to 64; unweighted | same call | the methods note's definition (asserted within 0.01 on the gap) |
| SF3 | employment rate | employed over population 15 and over | 15 to 64 | same call | the methods note's definition |
| SF4 | the quarter the counterfactual is rebuilt on | January to March 2026 | an earlier quarter (October to December 2025 and back) or a later one (April to June 2026, July to September 2026) | an earlier quarter cannot be split at every wave the capped intakes hold and moves the figures by up to 0.085 point; a later quarter is itself capped, so the households to remove are already absent | the records: January to March 2026 is the only quarter with no capped intake at any wave whose five intakes all carry visit histories (the call-record app replaced the paper call sheets at the 2025Q1 intake); every earlier uncapped quarter has 15 per cent or more of its sample with no visit history and every later quarter has a capped intake, both asserted in checks.py, and no document says which quarter to use |
| SF5 | a household the cap would not have recruited | interviewed at wave 1 at a fourth, fifth or sixth visit | refusals; every non-contact | same call | the instruction's cap counts visits to an address; asserted |
| SF6 | re-estimation | re-rake to the population controls after dropping those households | keep the base quarter's final weights; unweighted | rung 3 below, not a reading | the methods note: every estimate the office publishes uses the raked weights |
| SF7 | the six-visit restoration | first interviews issued from 1 April 2027, so the capped intakes are April to June 2026 to January to March 2027 | from the July to September 2027 intake | same call | the prompt's date and the instruction's field year; asserted |
| SF8 | the cap's share of the published change | the change in the gap between April to June and July to September 2026 | the July to September gap itself; a year-on-year change | the July to September gap alone files 0.39 of a 0.27-point rise and a negative labour market, which no reading of "how much of the rise is the labour market" supports once both quarters are capped | the prompt asks what the rates would differ from six visits all along in each quarter and how much of the rise between two named quarters is the labour market, so the market's share is the change in the six-visit series; asserted |
| SF9 | rounding | hundredths of a point, from unrounded estimates | rounding each rate first | same call | the prompt; the methods note's section 7; asserted |

## Ladder

Built values (asserted in checks.py by name, printed by the build). Gap = published rate less the six-visit rate,
points; unemployment rate first, employment rate below it. The last column is the cap's share of the April to June to
July to September change in the unemployment rate, which is the call's headline.

| Rung | Construction | Jul-Sep 26 | Oct-Dec 26 | Jan-Mar 27 | Apr-Jun 27 | Jul-Sep 27 | cap share of the rise |
|---|---|---|---|---|---|---|---|
| 0, default | the wave-1 gap in each capped quarter, zero after | 0.21 / -0.79 | 0.21 / -0.79 | 0.21 / -0.79 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 (the whole 0.27 the market) |
| 1 | the wave-1 gap carried unchanged at each later wave of each capped intake | 0.60 / -2.26 | 0.85 / -3.15 | 1.07 / -3.93 | 0.95 / -3.16 | 0.67 / -2.02 | 0.28 (the market -0.01) |
| 2 | per-wave removal on January to March 2026, final weights kept | 0.45 / -2.26 | 0.61 / -3.15 | 0.72 / -3.93 | 0.57 / -3.16 | 0.34 / -2.02 | 0.21 (the market 0.06) |
| 3, golden | per-wave removal on January to March 2026, re-raked | 0.39 / -1.42 | 0.53 / -1.97 | 0.62 / -2.44 | 0.47 / -1.88 | 0.28 / -1.19 | 0.18 (the market 0.09) |

- **Position:** rung 0 gives one figure for three quarters and zero for the last two, and files no cap at all in the
  change; the golden rises to 0.62 and falls to 0.28, and files 0.18 of 0.27.
- **Margins (measured, tolerance 0.05 on the unemployment gap and 0.15 on the employment gap):** rung 0 off the golden
  by at least 0.18 point on the unemployment gap in every quarter (0.18, 0.32, 0.41, 0.47, 0.28) and by at least 0.63
  on the employment gap; rung 1 by at least 0.21 and 0.83; rung 2 by at least 0.06 on the unemployment gap and 0.83 on
  the employment gap. On the headline, rung 0 is 0.18 out, rung 1 0.10 out and rung 2 0.03 out, and all three print a
  different cap share and a different labour market share from the golden's 0.18 and 0.09.
- **Dominance:** the decisive move (the intake as the unit) is the only one that makes the gap change from quarter to
  quarter at all, so it alone can put anything but zero in the headline; re-raking then brings the carried gap down to
  the golden and carries every employment cell.
- **Grid:** wave-1 only, carried constant, carried by the panel; final weights or re-raked: six paths, each asserted.
- **Worth:** the decisive move carries the headline (the cap's and the market's share of the rise, four graded
  figures) and all ten gap cells; re-raking carries every employment cell and three of the unemployment cells.
- **Direction, asserted in every quarter:** rung 0 understates the gap and rung 1 overstates it, so the golden is
  bracketed rather than extreme.
- **The sign flip:** the published employment rate fell 0.34 point while the six-visit employment rate rose 0.29, so
  the two routes disagree on the direction of the employment call and not only on its size.
- **The simulation's own truth (information):** the generator also builds the six-visit counterfactual of the capped
  intakes that were actually fielded; its July to September gap is 0.35 point against the estimate's 0.39 (asserted
  within 0.12), which is what the base-quarter estimator costs in sampling noise.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | persons 15 and over in the responding households of the quarter's five intakes | filed in the methods note; C1 |
| 2 | Unit of account | the person for rates, the address for the cap | filed: the instruction counts visits to an address |
| 3 | Attribution window | survey quarter | filed in the methods note |
| 4 | As-of dating | microdata to July to September 2026 as locked 20 October 2026 | filed in the extract notes |
| 5 | Version basis | final weights; population controls as rebased | C1: the rebasing predates the base quarter (asserted) |
| 6 | Denominator | the labour force (unemployment rate), population 15 and over (employment rate) | filed definitions |
| 7 | Weighting | raked person weights | filed in the methods note; SF6 |
| 8 | Window length | the base quarter the counterfactual is rebuilt on | SF4, closed by what the records cover rather than by a sentence |
| 9 | Boundary inclusivity | fourth visit and later | SF5 |
| 10 | Rounding path | hundredths of a point from unrounded estimates | the methods note section 7 (changes computed from unrounded estimates, rounded independently); SF9 |
| 11 | Tie-break | none | no decision turns on a tie; the gap's largest quarter clears the next by 0.09 point (asserted) |
| 12 | Maturity and censoring | the July to September 2026 file complete at lock; the October to December 2026 intake not yet fielded | filed in the extract notes |
| 13 | Order of operations | drop households, re-rake, estimate | asserted |
| 14 | Row order | none | C1 over permutations |
| 15 | Duplicate resolution | the call-record app's re-sends are non-interview rows; the visit of interview is unique per address | asserted |
| 16 | Identity normalisation | address serial across files, check digit dropped from the July to September 2026 run | asserted |
| 17 | Netting | the cap's share of a change is the change in the gap | SF8; asserted |
| 18 | Dimensional units | percentage points; hours | dictionary |
| 19 | Code semantics | ILO status codes, call outcome codes | dictionary; never the stump |
| 20 | Integerisation | counts integers | C1 |
| 21 | Clause scope | the cap binds first interviews issued from 1 April 2026 to 31 March 2027, so the intakes April to June 2026 to January to March 2027 | filed in the instruction and the prompt; asserted |
| 22 | Forward window contents | intakes, waves and controls to September 2027 | the base quarter's structure; controls held at their latest vintage |

## Literal reader

Executing the prompt and the shipped documents word for word: the gap in a quarter is the published estimator's rate
less the rate it would give had first interviews had six visits all along; the cap removes, from every intake issued
from 1 April 2026 to 31 March 2027, the households first interviewed at a fourth to sixth visit; the panel keeps each
intake for five quarters, so a quarter's sample holds each capped intake at the wave its issue date puts it; the
estimator rakes every sample to the population controls. Nothing in the pack says how to measure the effect of a
fieldwork change or on which quarter, and only January to March 2026 can carry the construction at every wave the
capped intakes hold, so each quarter's gap is January to March 2026 re-estimated without those households in those
waves, and the cap's share of the April to June to July to September change is the difference of two such gaps. Every
reading in SF1 to SF9 returns the golden path; the default path comes from the same estimand by taking the quarter
rather than the intake as the unit the cap acts on.

## Oracles

- The release table to April to June 2026: the published rates the microdata reproduces; ties under every basis.
- The administrative claimant count: a different concept on a benefit rule changed in 2025; moves with the labour
  market, blind to the cap; ties under every basis (a distractor).
- The July to September 2026 microdata: its wave-1 and wave-2 intakes are both capped, so it shows the cap's presence
  and nothing about which quarter to rebuild the counterfactual on or how far the cap reaches.
- The field staffing list: interviewers by region, never read by the solution (a distractor).
- None ties only under the golden.

## Ask sheet

The main call's declared row population: the person file's January to March 2026 records (columns serial, wave,
quarter, ILO status, age group, sex, region, final weight) and the April to June and July to September 2026 published
rates, the call records' interview rows for the intakes of January to March 2025 to January to March 2026, the
population controls and the methods note. Person numbers, hours and every non-interview call row are outside it. Each
ask is a measure the quarterly fieldwork and quality report carries for every region beside the headline (H18 home: an
audit trail of the call's inputs, the intake's visits, the panel's flows and the employed's hours), on which the call
does not turn; none is keyed to the call or its construction, and the three share no primary family and no file path.
No sentence in the pack adjudicates a device.

**Ask 1. First-interview visits made to the July to September 2026 intake, each region (6 whole numbers).**
- Use: the field budget the cap was meant to save, read beside the call.
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
- Ladder (asserted): rows counted (the cracker, every region high); de-duplicated on serial and date (every region
  low); golden. The July to September 2026 intake is outside the base quarter's five intakes, so no ask device sits in
  the call's own population.

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
- Ladder (asserted): joined on serial and person number (the cracker, every region off); joined on serial alone
  (fan-out, every region off); golden, serial, sex and date of birth (one match each).

**Ask 3. Total weekly hours actually worked by the employed in July to September 2026, each region (6 figures,
thousands of hours to one decimal, final weights).**
- Use: the hours the release carries, read for intensity beside the rate.
- Primary device (D3, units set per source): telephone interviews store hours and minutes as h.mm (37.30 for 37 hours
  30 minutes) while face-to-face interviews store decimal hours; summed as decimals every region is low by about 0.3
  per cent (asserted). Only the telephone values' fractions never exceeding .59, against the face-to-face quarter
  hours, show it.
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

Measured by: generator/pair.py, run on the cut pack (0 of 18 ask figures graded right on the cracker's path and 0 of
18 on the over-correction).

Mirror leakage: 8.0 per cent of the ask weight (method credit on the ask paths, no figure).

**Pair arithmetic.** Planning weights 38 recommendation, 7 instruction following, 55 asks over 18 ask figures. With
each top response keeping about 8 per cent of the ask weight: C = 38 + 7 + 4.4 = 49.4 for the cracker, S = 6 + 7 + 4.4
= 17.4 for the mirror.

Pair ceiling: 33.4

## Pins

- The design, the definitions, the raking to region and age-sex controls and the sampling error: the methods note
  (sections 1, 3, 4 and 5), once. Nothing in it says how the effect of a fieldwork change is measured or on which
  quarter.
- The cap (three visits, first interviews, the 2026/27 field year, the 2027/28 pattern set with that year's budget):
  FI-2026/04, once; the return to six visits from 1 April 2027 is the prompt's scenario.
- Ask readings: none filed; each ask's wording fixes its quantity. No sentence adjudicates a device.

## Stopping rule

Two portal solves of the gap path or the headline by different routes re-root the decisive step; a determinism finding
that the base quarter is open is closed by what the records cover, never by filing the method; a solve landing the path
from a filed sentence sends that sentence out of the pack and the build back to design. One more measured Gate F
failure on this ladder retires the architecture rather than hardening it, because the only remaining lever would be a
plant.

## Build record

- Realisation: the sampling noise is fixed by world.SALT = 14, chosen from 40 scanned on the joint criterion that the
  cap be the larger share of the rise (0.18 of 0.27), the labour market's share be a clean positive figure (0.09), the
  published employment change flip sign on a six-visit basis (-0.34 against +0.29), every rung sit outside the
  tolerance, and every graded figure sit mid-bin. Measured on the chosen realisation: the tightest graded rate figure
  is the July to September 2027 unemployment gap at 0.00106 point from its printed cell's edge (the raking converges
  to 1e-12, so that is about 1e9 times the numerical noise), and the tightest ask figure is Pellard's total hours at
  0.00041 of a thousand hours from its edge (a float sum whose worst-case accumulation error is 2.5e-05, so about 16
  times the noise even without pairwise summation).
- The cap's timeline was moved from one quarter before the released quarter to the 2026/27 field year so that the
  released quarter and its comparison quarter are both capped. That is what makes the decisive step carry the
  headline: with only one capped quarter, the wave-1 route and the golden agree on the cap's share of the change.
- Licensed-family spread, measured on the clean truth over six variants (base-quarter controls against each target
  quarter's own, raking from unit weights against the base quarter's final weights, 60, 200 and 1000 iterations):
  3e-06 point on the unemployment gap and 2.5e-05 on the employment gap, against a printed unit of 0.01 and a lever of
  0.18 to 0.47 point. The family is closed; the reason it is closed is also the reason the construction is arithmetic
  rather than estimation (see the Not rule application line).
- Reflex sweep, measured on the clean truth: 0 of 6 textbook routes reach the golden's headline (no adjustment 0.00,
  the wave-1 route 0.00, the carried gap 0.28, the weights-kept route 0.21, a rotation-group difference in differences
  0.34, the matched-panel change 0.58, against the golden's 0.18); the wave-1 cross-section and the year-on-year
  change answer other questions and the claimant series is blind to the cap.
- Gates (stage 3): 300 checks, the independent verifier, two byte-identical builds, figures_check 155 figures,
  precut 51 of 51 with no WARN, leak.py REVIEW (sweep 4's design-note vocabulary only, all eleven other sweeps clean,
  including answer figures in the pack, announcements, ranking artifacts and dates), voice-check PASS at 997
  characters, guard.py validate 0 invalid, guard.py surface exit 0 with no vocabulary, file-name or persona overlap.
- **guard.py heart is BLOCK, and the three findings are the draw's, not this ladder's.** The card was registered on
  2026-10-12 and the corpus moved under it: `ban.artifact` (context artifact filed_standard) against task501 v4 and
  `ban.strategy` (composition_mix) against task448, both cards delivered since, and `test.same_driver` (gap time,
  pattern G6, Gate G forecasting) inside the batch against task501 v3. The fourth,
  `test.same_driver_older` against task150, carried guard's own prescribed fix and is now a NOTE with a
  differentiation line on the card. The remaining three each ask for a card axis to be redrawn, which is a stage-1
  action, and relabelling an axis to clear a ban is the move `stumping` Part 6 names as banned, so they are left for
  the author. Nearest driver 0.07 (task467), well under the 0.12 warn line, so the driver text itself is clear.

## Judge record

- Pass 1 and pass 2 (2026-10-12) were on architecture 2's first ladder and are **void**: the determinism judge's
  APPROVE is scoped to the pack it saw (`determinism-check`, Running the judge), and this re-root moves every graded
  figure, the base quarter, the cap's timeline and the methods note. Pass 2's own Gate H line already read the
  decisive step as "borderline rule application through section 5", which the blind reader then measured. The reports
  are kept as evidence of the architecture's history; the judge owes this pack a fresh run at stage 4.
- Carried forward from pass 1, and kept in this pack: the methods note's sections 2, 6 and 7 (visit identity, flows,
  rounding from unrounded estimates) and the release table's total actual weekly hours as the hours referee. A
  dictionary line naming the h.mm encoding was declined as narrating the device.

## Pre-ship check

- Call: most of the July to September rise is the cap (0.18 of 0.27, the labour market 0.09); the published
  unemployment rate sits 0.39, 0.53, 0.62, 0.47 and 0.28 point above the six-visit rate from July to September 2026 to
  July to September 2027, the employment rate 1.42, 1.97, 2.44, 1.88 and 1.19 below, and the rates are back on a
  six-visit basis from April to June 2028.
- Default path: the wave-1 gap in each capped quarter and nothing after (0.21, 0.21, 0.21, 0.00, 0.00), with none of
  the rise the cap.
- Gates: as the Build record lists them. **Stage 4 is owed:** the leak reader and the determinism judge have not seen
  this pack, so the build is not ready to ship.
- Deliverables: hls_visit_limit_note_2026q3.docx (two pages, chart and table), hls_visit_limit_path_2027.xlsx (gap
  path, the April to June to July to September split, regions, notes).
- Card: the stump, driver and answer brought up to this ladder.

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

- Architecture 2's first ladder (2026-10-20, at this re-root): the methods note's section 5 stated the procedure the
  decisive step executes ("applying the change to the last full quarter collected before it and re-running the
  estimation as in section 4"), so a blind Sonnet reader at medium effort, holding only a fresh unzip of target.zip,
  the prompt and the figure names, took 2 of 2 call figures and 38 of 53 ask figures and quoted that sentence as what
  told it the step. Under rule 3 that is rule application, not analysis. Not repairable by deleting the sentence
  alone, because the base quarter it pinned would then be an open knob (measured: up to 0.085 point of movement on a
  figure printed to 0.01); the re-root deletes the sentence, lets the call-record app's coverage settle the base
  quarter, and moves the cap's timeline so the decisive step carries the headline.
- Keeping the cap on one intake and removing section 5 only (2026-10-20, at the re-root, measured): with the cap
  issued for a single quarter before the released one, the wave-1 route and the golden give the same cap share of the
  April to June to July to September change, because only one of the two quarters has a capped wave 1. The decisive
  step then carries no graded figure of the headline, only the forward path, which is exactly the half the measured
  reader took last. Rejected for the field-year timeline, which puts a capped intake in both compared quarters and
  makes the wave-1 route file 0.00 of the 0.27-point rise.
- Grading the non-contact bias of the published rate instead of the six-visit counterfactual (2026-10-20, at the
  re-root): the level of the bias is genuinely unobserved (measured at +0.78 to +0.84 point of unemployment in every
  pre-cap quarter against the eligible population, and +0.99 under the cap), which would put an estimated quantity in
  the deciding position. Rejected on the determinacy screen: it needs the never-contacted households, whose outcomes
  are reached only by extrapolating a level-of-effort gradient past the sixth visit, and the geometric contact process
  behind the pack is a three-class mixture whose tail mass is identified only to within a wide band, so the estimator
  family would be open on a figure printed to 0.01.
- Making the wave structure something the solver infers from the sample's own composition rather than from the methods
  note's section 1 (2026-10-20, at the re-root): a methods note that does not document a rotating panel's rotation is
  not a methods note, and the person file carries a `wave` column besides, so the rotation is schema-visible whatever
  the documents say. Readability test 2 fires. The re-root leaves the rotation filed and moves the decisive step to
  the unit the change acts on instead.
- Identifying the capped-out households from the capped intakes rather than from a pre-cap quarter, so that the
  counterfactual is estimated rather than subset (2026-10-20, at the re-root): with the pre-cap call records removed
  the forward path is unidentified, because nothing then measures how the selected households' outcomes persist
  across the telephone waves; with them shipped the counterfactual is exactly recoverable by subsetting and the step
  is arithmetic. Same dial, both ends. Recorded as the architecture's structural ceiling: no stage-2 move puts an
  estimated quantity in the deciding position on this draw, and a third measured Gate F failure retires the number
  rather than hardening it.

## Pre-ship check, architecture 2 (2026-10-23)

**The free gates, all re-run on the final pack.** Generator checks 300 assertions passed; `verify` OK with
18 regional figures recomputed independently; two builds byte-identical at sha256 `052a1c1b078e0b29`;
`target.zip` cut from that build at sha256 `5314b654417ae84b`, 12 files each identical to `target/`;
`figures_check.py` PASS at 155 figures in blocks 1 to 4 with none absent from `figures.json`;
`voice-check.py` PASS with the prompt at 998 characters; `leak.py --asof 2026-10-20` REVIEW, not LEAK, with
sweeps 1 to 3 and 5 to 11 clean; `guard.py surface` clean on the hard-tell screen.

**The 10/10 rules re-read against the built pack.** The decisive step is still the unit of analysis, the
intake rather than the quarter, which is analysis and not a reading or a procedure; the mess is still
Layer 1 only (the serial gaining a tenth check-digit character in the 2026Q3 run, local-time call stamps,
the 2025-based control rebase); nothing is planted to be caught. The isolated stage-4 reader independently
answered the rule-3 question as **(a) an analytical choice** and found no sentence that announces the
decisive step, which is the external confirmation Gate H wants.

**The stage-4 reader's six answers.** Question 1, nothing announces the decisive step; the nearest pointers
are the methods note's section 4 ("Every quarter's sample is therefore made of five intakes, one at each
wave") and section 6, which "tell you to re-rake and to use matched people, but they do not say a visit cap
shifts who responds". Question 2, no file ranks or scores the candidates; the release tables stop at April
to June 2026 and carry no six-visit counterfactual. Question 3, no file exists only to help the analyst.
Question 4, no figure reads as the answer. Question 5, the filed sentences fix the rate definitions, the
raked weights, the unweighted matched-pair flow base and the unrounded-then-rounded convention, and the
reader's own summary is that they "fix the definitions and the population, but not the counterfactual
method", which is exactly the WHAT filed and the HOW left open. Question 6, an analytical choice.

**Its two realism findings, one fixed at source and one ruled harmless.**
- **Fixed.** `population_controls_2023q1_2027q4.xlsx`, sheet "Age and sex": `25-34 male` and `25-34 female`
  were byte-identical in all 20 rows, which no real control table would be. The cause was `FEMALE[1] = 0.500`
  in `generator/models.py`, where every other band sits off 0.5 (ratios 1.04082, 0.9802, 0.96078, 0.94175,
  0.90476, 0.73913). Corrected to 0.497, which keeps the array monotone in age, and rebuilt. Exactly one of
  33 figure keys moved, the ask figure `total_weekly_hours_thousand`, and `submission.md` block 4 item 5 was
  updated to its six new values. Every main-recommendation and critical-component figure is unchanged: the
  gap path 0.39/0.53/0.62/0.47/0.28, rung 0 0.21/0.21/0.21/0.00/0.00, rung 1 0.60/0.85/1.07/0.95/0.67, and
  the cap's share of the rise 0.180 against rung 0 0.000, rung 1 0.282 and rung 2 0.208.
- **Harmless, no change.** The reader judged the methods note to read "partly as teaching a method", naming
  sections 4, 5 and 6. Declined on `leak-check`'s own test, would the sentence exist without the trap: a
  rotating panel's wave structure, raking by iterative proportional fitting to region and age-by-sex
  controls, the quarter-on-quarter caveat that consecutive samples share four intakes, and the matched-pair
  unweighted flow base are all standard content of a real labour-force methods note, and the asks need the
  flow and hours definitions to be determinate at all, so trimming them would cost Gate B and make the
  document less realistic, not more. The reader itself found no announcement of the decisive step.
- `leak.py`'s REVIEW is sweep 4 alone, five documents sharing generic survey vocabulary (change, population,
  intakes, statistics, records, controls, instruction, telephone, weights, quarters). Ordinary domain words.

**The guard's state at ship, and the author's override.** One BLOCK remains, `ban.strategy` on
`composition_mix` against task446 (v3), carried on the author's explicit `--force` with the reason on the
card. The measured case: driver similarity is 0.07 against a 0.12 WARN line and a 0.30 BLOCK line, the
nearest of 280 cards; `heart` found nothing above 0.07 against any driver, lineage driver, stump or ledger
row; and task446 sits on banking-credit-financial-risk/credit-scoring-pd-modeling under forecasting, so
only the coarse label collides. Two BLOCKs that registration surfaced after the author's decision were NOT
forced and were corrected on accuracy instead: `forcing_event` from `statutory_or_regulatory_filing` to
`budget_or_appropriation`, because nothing here is filed to a regulator and the pack's own field instruction
says the cap exists to bring fieldwork within the field budget; and a truthful differentiation line against
task179 (v3), which `test.same_puzzle_older` raised on three coarse labels alone.
**The three WARNs answered:** `people.first` and `people.last`, the persona Aaron Tucker shares a first name
and a surname with task267, one older build, which the rule scores as WARN rather than BLOCK and which is
not worth a pack churn that would void the reader's pass; `repeat.gate_g`, `decomposition_attribution`
repeats task252 (v2), and the Gate G mechanism is the one axis this build cannot rotate without changing
the decisive step itself, which the 10/10 rules fix.

