# task247 design note

## Draw

Card `cards/task247.json` (architecture 1, registered 2026-10-18). Guard verdict WARN, no BLOCK. The one WARN,
repeat.gate_g (method_or_model_selection after task172), is answered here: task172 selects a forecast method by
back-testing renewals, while here the choice is between correcting a provisional record by its average past error and
refilling its cloud gaps from the observations on both sides once the season has closed, and nothing is back-tested on
a filed criterion. Nearest driver 0.06 (task138 v1 lineage, task458 v1 lineage, task245, task70 v1, task123 v2).

- **Pairing.** Physical & Environmental Sciences / environmental-monitoring-exceedance, a task type serving Anomaly
  Detection and Data Quality Monitoring; drawn for Data Quality Monitoring & Alerting. Not banned against the last three
  builds (task170 healthcare forecasting, task244 survey research data quality, task172 general statistics
  forecasting). The object is the health of the provisional sea surface temperature record the station's bleaching
  alerts were declared on (how far its cloud-filled days moved each reef's heat stress), the call a monitoring
  decision: which reefs' declared alert levels stand on the reprocessed record, and so which reefs the post-bleaching
  survey visits.
- **The seed, re-found.** DQ20 gave the world (alerts raised on provisional monitoring data and scored once the record
  is reprocessed), the decision (each alert kept, changed or withdrawn) and the quantity (the alert scored against the
  reprocessed record on the event it claimed). Its air quality network was left: a rule replayed on its own archive is
  a direct count, the drift and calibration stumps that network could carry belong to the lane's own seeds task249 to
  task252, and the forward versions it allows (analysers ageing, a calibration interval lengthened) teach the
  exposure-clock lesson task46, task132 and task134 v2 already teach. A reef heat-stress watch keeps every element:
  weekly alert levels declared on a near-real-time satellite analysis, a reprocessed record months later, and the alert
  scored on the heat it claimed.
- **Niche.** A public university's reef station on the Caribbean coast of Quintana Roo runs a coral bleaching watch for
  16 reef sites: each week it declares each site's alert level from the degree heating weeks of the near-real-time
  satellite sea surface temperature analysis (HotSpots of a degree or more above the site's maximum monthly mean,
  summed over twelve weeks); the reprocessed analysis, built later with every satellite pass and the in situ records
  that arrive afterwards, is the record of reference and is released the following May. The station's post-bleaching
  survey, sent in November, visits the sites the reference record will put at Alert Level 2.
- **The call.** Which of the 16 sites go on the November 2027 survey list: a site goes when its 2027 season maximum
  degree heating weeks on the reprocessed record reach Alert Level 2 (8 degree-weeks); each site's level declared on the
  near-real-time record is confirmed, raised, lowered or withdrawn accordingly.
- **Shape.** 01, a ranked list under a line: per site the estimated maximum degree heating weeks on the reprocessed
  record, its level and its verdict against the declared level (16 sites by three), the survey list and its count, the
  site nearest the line below it, a chart of each site's declared and estimated heat stress against the alert levels,
  and the asks, well over 25 criteria. Decision renew_replace_lapse, answer set_of_items, question form which.
- **Strategy.** other, named in the card's notes: an imputed-gap structure, the real-time analysis's one-sided fading
  fill of its cloud gaps against the record of reference's later two-sided fill (every 2027 day is present, so neither
  censoring nor late arrival of events; drawn as maturity_censoring, redrawn at stage 3, below). G13 decisive (a filled
  day carries only what was known that day, while the reference record fills it with the observations after it as
  well), G12 (a filled value is the analysis's absence of an observation written as a temperature), G16 (the
  provisional record corrected by its mean error, by flag, by site, or refilled from both sides); gap population (a
  filled day is not an observation of the sea) then time; Gate G method_or_model_selection; calibration
  censored_or_lagged_release (the record of reference arrives the following May, with nine seasons of overlap); context
  artifact operations_log (the weekly alert bulletins); Layer 2 family estimation_fit, pattern
  own:hindsight-refill-of-gaps-a-real-time-analysis-relaxed-to-climatology.
- **Forum, event, organisation.** executive_team (the station's directorate approves the November survey plan),
  vote_or_meeting (its meeting of 10 November, before the Ixchel sails on the 15th), university_or_school (a public
  university's marine station). Role research_desk (the station's head of reef monitoring, a scientist heading the
  monitoring programme, who asks for the list and takes it to the directorate).
- **Stage 3 redraw.** task190 (6), task201 v2 and task202 registered earlier on 2026-10-18 than this card but reached
  this checkout after the draw; against them the guard blocked five context axes (calibration parallel_run_overlap,
  role field_unit_lead, strategy maturity_censoring and forcing event season_or_peak against task201 v2, forum
  line_manager_or_team against task190), each redrawn above to the label the build honestly carries, the request
  rewritten around the directorate's meeting. Heart WARN after the redraw, each answered: repeat.gate_g and
  overuse.gate_g (method_or_model_selection after task202 and task201 v2, six of the last twelve): the stump is the choice
  of how to anticipate a record from its provisional version, not a grain (task202) or a feeder's clock (task201), and
  no other Gate G key is true of it; repeat.deliverables (pdf and xlsx after task202): a survey list note and its
  workbook are the formats a station sends its directorate; repeat.question_form (which after task201 v2): the decision
  is a pick of sites.
- **People** (`guard.py names --geo Mexico --seed 247`, locale es_MX): Fabiola Mireles, the survey coordinator, who
  asks; Alfredo Montero, the station's head of reef monitoring; Rocío Muñiz, the remote sensing analyst who issues the
  bulletins; Hernán Pichardo, the dive team leader. None appears in the prompt.
- **Data-native sentence.** The near-real-time analysis has to say something every day, so on a day cloud hides a reef
  it keeps the last clear-sky anomaly and lets it decay toward climatology; that costs nothing in ordinary weeks and a
  great deal when the cloud is a stalled trough over a hot sea, because then the filled days slide back toward normal
  exactly while the HotSpots should be accumulating, and the reprocessed record, which fills the same days with the
  observations that come after them, will not.
- **As-of.** Wednesday 3 November 2027, before the survey's field trip; the 2027 reprocessed record is due in May 2028.
- **Sources.** The client's two-layer standard (estimation_fit: an estimate that ignores how the data were made) and
  the real coral bleaching heat-stress method (HotSpots above the maximum monthly mean, degree heating weeks over
  twelve weeks, Alert Levels 1 and 2 at 4 and 8 degree-weeks). No build on file uses a satellite analysis, a sea
  surface temperature record or a reef (`guard.py slots` finds no screen on them).

## Default path

1. Read the near-real-time extract: the latest issue of each pixel and day (a later issue replaces the earlier, user
   guide section 3), the observation flag read by each row's version (from 3.2, 2 observed and 1 not; before, 1 and
   0), pixels to sites by the register; 17 June 2027 was never issued.
2. Read the reprocessed record (kelvin less 273.15). The 2027 season is not in it until May 2028, so the 2027 values it
   will hold have to be estimated from the near-real-time record.
3. Correct the near-real-time record toward the reprocessed one by their past differences, 2018 to 2026, the observed
   and the filled days apart, because the guide says the two kinds of day are made differently: +0.060 degrees on
   observed days and -0.007 on filled days, taken out of each 2027 day by its flag.
4. Each site's HotSpots of 1.0 or more above the register's maximum monthly mean, the 84-day sum over 7, the highest
   value on a day from 1 June to 31 October; Alert Level 1 at 4, Alert Level 2 at 8; the verdict against the highest
   level the season's bulletins gave.

Ends on: three sites at Alert Level 2, PB07, PB09 and PB10 (8.8, 9.0 and 11.1 degree-weeks); PB06 lowered to Alert
Level 1 (7.8) and the five southern sites PB11 to PB15 at Alert Level 1 or below (4.2 to 7.1).

Golden: nine sites at Alert Level 2, PB06, PB07, PB09 and PB10 confirmed and PB11 to PB15 raised (expected maxima 9,
11, 10, 12, 13, 10, 12, 9 and 11 degree-weeks), the observed days less the clear-sky difference (0.06) and every other
day refilled by straight-line interpolation of the anomaly between the observed days either side.

## Stump sentence

A competent analyst corrects the 2027 near-real-time record by the past seasons' mean differences from the reprocessed
record, observed and filled days apart (+0.060 and -0.007 degrees), and ends on three sites at Alert Level 2, PB07,
PB09 and PB10; the step that lands it there is treating a filled day's error as a constant to take out, when the
analysis fills a cloudy day by letting the last observed anomaly fade toward the climatology, so its error grows with
the anomaly and the length of the gap (on the 2018 to 2026 hot filled days it reads 0.26 degrees low after the
correction), and during the August trough over the south the filled days ran far below the sea; only refilling each
gap from the observed days on both sides, as the reprocessed analysis will with the passes and in situ records that
reached it later, puts PB06 and the five southern sites PB11 to PB15 at Alert Level 2.

## Three rules

- **Task type:** physical-environmental-sciences / environmental-monitoring-exceedance, which serves Data Quality
  Monitoring & Alerting (the watch's declared alert levels are the monitored data product, and the call is the
  monitoring decision taken on them: which declared levels stand on the record of reference, and so which sites the
  survey visits).
- **Domain test:** the quantity that decides is each site's season maximum degree heating weeks on the reprocessed sea
  surface temperature record, which coral bleaching heat-stress monitoring accumulates from daily HotSpots of a degree
  or more above the maximum monthly mean over twelve weeks; estimating it before the record's release means rebuilding
  the record's daily temperatures from the near-real-time analysis, whose cloud-filled days are the analysis's fading
  persistence of its last observation, and the field's own answer to a gap in a persistent anomaly field is to fill it
  from the observations on both sides.
- **Swap:** "which of our hospitals go on the inspection list, the ones the audited register will put above the line"
  keeps the sentence and loses the task: there is no satellite analysis relaxing toward a climatology under cloud, no
  HotSpot threshold accumulating over twelve weeks, and no record of reference rebuilt later from passes the real-time
  run never saw, so refilling cloud gaps from both sides has nothing to act on.
- **Layer 1:** re-issued days (the later issue replaces the earlier), the observation flag recoded with version 3.2 on
  15 July 2027 (late re-issues of earlier days carry the new codes), the reprocessed record in kelvin, pixel
  identifiers against the register's site codes, a day the centre never issued (17 June 2027), UTC analysis days
  against the bulletins' local Tuesday dates; each produced by the product's re-issue and versioning, the centre's
  units or the station's extract, none placed, and the call is the same under every handling (SF2 to SF13).
- **Layer 2:** estimation_fit, an estimate that ignores how the data were made: a filled day is not an observation with
  a mean error but the analysis's memory of the last clear day fading toward the climatology, so its error depends on
  the anomaly and on how long the cloud has lasted, and the record of reference will fill the same day from the
  observations after it as well.
- **Decisive step:** taking the clear-sky warm difference out of the observed days and refilling every other day by
  straight-line interpolation of the anomaly between the observed days either side, rather than correcting the filled
  days by their past mean error or by a regression on their own decayed value.
- **Not semantics:** reading every field, code, unit and definition right (the latest issue, the flag by version,
  kelvin, the pixels, HotSpots, the 84-day sum, the season, the levels, the declared level) still leaves the
  mean-correction route on three sites: no field or sentence says what a filled day's value is made of beyond that the
  analysis provided one.
- **Not rule application:** the methods note files the estimand (each site's season maximum on the record of
  reference, its level and the verdict against the declared level, sections 3 to 6) and no way of estimating the
  record before its release; executing every stated rule on the near-real-time record files the bulletins' four, and
  on that record corrected by its mean differences the three.
- **Analyst test:** a strong analyst who reads every file right takes the past mean differences of observed and filled
  days out of the 2027 record and ends on three sites at Alert Level 2 (PB07, PB09 and PB10); on the simulator's clean
  truth the same route files the same three and refilling alone gives the nine (R3 in checks.py).
- **Estimand:** the methods note (`reef_heat_stress_watch_methods_v3.pdf`, sections 3 to 6): for each of the 16 sites
  the highest degree heating weeks on a day of 1 June to 31 October 2027 on the record of reference (the reprocessed
  analysis, released May 2028), the level it sets (Alert Level 1 at 4, Alert Level 2 at 8) and whether that confirms,
  raises or lowers the highest level the season's bulletins gave; the survey goes to the Alert Level 2 sites.
- **No decoy:** nothing is planted: no memo, draft, briefing or stakeholder figure argues a list; the request names no
  site; the bulletins are the watch's operational record of the declared levels the call checks, not a ranking on the
  record of reference; the two distractors give no site a heat-stress figure.
- **No certified replay:** no certified or published 2027 figure on the record of reference exists for a method to
  reproduce; the method is found from the data's structure (filled days fading toward the climatology, their past
  error growing with the anomaly) and checked on the 2018 to 2026 overlap.
- **Lesson:** a gap-filled value in a real-time analysis is not a noisy observation but the analysis's fading memory of
  the last one, so its error is conditional on the state and the gap, and an average correction leaves it wrong
  exactly under sustained heat and persistent cloud; a record that will be rebuilt with later data is anticipated by
  rebuilding the gaps from both sides. No build on file spends it (task245 rebuilt hours that were absent from other
  stations' readings and the wind; task241 a sensor's offset at a displaced position; task235 recent weeks still
  filling in).

## Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control or
corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or half of
a reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 the bulletins' declared levels: PB06, PB07, PB09, PB10 | the bulletins workbook | the alert level column | yes, the operational record | none | no | read off | readable |
| 1 (default) the past mean differences of observed and filled days out: PB07, PB09, PB10 | the guide's flag and the release note's record of reference | obs_flag | yes, a bias correction by category | the overlap, which it matches on average by construction | no | a subtraction | readable |
| 2 the regression of filled days' anomalies on the reprocessed record's (slope 1.29): six sites | none | obs_flag | yes, a regression on the overlap | the overlap | no | one regression | readable |
| 3 the refill without the clear-sky difference: the nine, eight figures one degree-week high | none | obs_flag | no | the overlap's observed days show the 0.06 | no | an interpolation | readable |
| 4 (decisive) the observed days less 0.06 and every other day refilled from the observed days either side: the nine | no sentence says what a filled value is made of or names a refill; the guide says the analysis provides a value and the release note that later passes and in situ records reach the record of reference | no column says how a filled value was made | no: the reflex is a bias correction or a regression | the overlap refutes the mean correction only under the decisive lens: the means match by construction, and the failure shows only in the hot filled days' error (-0.26) or the gap structure | no | not linear: an interpolation per gap, then a thresholded 84-day sum and a season maximum | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | season maximum | the highest DHW on a day of 1 June to 31 October | the DHW of the season's last day | same list, other figures at ten sites | methods section 4 "the highest DHW it reaches on a day of the season" (asserted) |
| SF2 | a HotSpot | SST less the MMM when 1.0 or more | strictly above 1.0 | same call | same call and figures (asserted) |
| SF3 | the 84 days | ending on the day, the day included | the 84 days before it | same call | same call and figures (asserted); section 3 "the day included" |
| SF4 | the maximum monthly mean | the register's mmm_c | recomputed from the climatology file | same call | the values are identical (asserted) |
| SF5 | a re-issued day | the later issue | the first issue | same call | same call and figures (asserted); guide section 3 |
| SF6 | 17 June 2027, never issued | a day without an observation, refilled | no HotSpot that day | same call | same call and figures (asserted) |
| SF7 | the declared level | the highest level any season bulletin gave | the last season bulletin's level | same call | the same verdicts (asserted); methods section 5 |
| SF8 | the season's bulletins | those reporting a day of 1 June to 31 October | those issued in June to October | same call | the same declared levels (asserted) |
| SF9 | the day | the UTC day of both satellite records | the station's local date | same call | methods section 2 "the day being the UTC day"; 153 season days (asserted) |
| SF10 | the level for the season | from the unrounded maximum | from the whole number | same call | no maximum lies between 3.5 and 4 or 7.5 and 8 (asserted) |
| SF11 | to the nearest whole number | rounded | truncated | ruled out | the prompt's "to the nearest whole number" |
| SF12 | the observation flag | read by each row's version | read by the day's date | same call | same call and figures (asserted); guide section 4 |
| SF13 | kelvin | less 273.15 | none differs | converge | release note section 3 (asserted) |
| SF14 | the survey list | the sites at Alert Level 2 for the season | none differs | converge | methods section 6 |
| SF15 | confirms, raises or lowers | the level for the season against the declared level | none differs | converge | methods section 6 |
| SF16 | the clear-sky difference | every observed day of 2018 to 2026 | each site's own, the heat seasons' only | same call | same call and figures (asserted, variants) |
| SF17 | the loggers' seasons (an ask) | June to October on the loggers' local clock | in UTC | same figures | the same hours at every site (asserted) |

## Ladder

Four wrong rungs and the golden, each a defensible way to anticipate the record of reference from the near-real-time
record, each dying to one fact of the record (figures on the cut pack, printed by `generator/pair.py --ladder`, asserted
in `checks.py`).

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0 | the bulletins' declared levels (the near-real-time record as issued) | PB06, PB07, PB09, PB10 | the record of reference is the reprocessed analysis (methods 6), and the as-issued record runs 0.06 warm on observed days and low on filled ones |
| 1 (default) | the past mean differences of observed and filled days taken out (+0.060, -0.007) | PB07, PB09, PB10 (PB06 at 7.85) | the overlap: on hot filled days the corrected record still reads 0.26 low, because a filled day's error grows with the anomaly and the gap |
| 2 | the filled days' anomaly regressed on the reprocessed record's (slope 1.29, intercept -0.03), observed days less 0.06 | PB06, PB07, PB09, PB10, PB11, PB15 | the same overlap: the regression restores a day or two after a clear day and not the long gaps (hot filled days still -0.13; PB12 6.5, PB13 7.6, PB14 5.5) |
| 3 | every unobserved day refilled from the observed days either side, the clear-sky difference left in | the nine, with eight figures a degree-week high | the overlap's observed days run 0.06 warm of the reprocessed record |
| 4 (golden) | the observed days less 0.06 and every other day refilled from the observed days either side | PB06, PB07, PB09, PB10, PB11, PB12, PB13, PB14, PB15 | |

- **Margins.** The nine's expected maxima are 8.85 to 13.00 (PB06 the nearest, 0.85 above the line) and the other
  seven 6.96 or less (PB08, 1.04 below); on the Alert Level 1 line PB02 sits 0.95 above and PB01 0.89 below. Every
  variant of the refill (temperature instead of anomaly, a shape-preserving curve, each site's own or the heat seasons'
  clear-sky difference, the last observed anomaly carried, the nearer observed day) prints every site's whole number
  and level, within 0.30 of the whole number (asserted).
- **Position.** The nine are reached by no wrong rung; rung 3 lands the list with eight figures wrong.
- **Dominance.** The decisive move adds PB06 and PB11 to PB15 to the default's three, raises PB02, PB05 and PB16 from no
  alert to Alert Level 1, and changes 15 of the 16 whole-number figures; it moves the northern and central sites by 0.6
  to 2.0 and the southern by 3.8 to 5.9.
- **Grid.** No correction, the pooled mean, the flag means, each site's flag means, the regression, and the refill with
  or without the clear-sky difference: four, three, three, three, six, nine with wrong figures, nine. On the
  simulator's clean truth the default files the three and the refill alone the nine (R3).
- **Worth.** The decisive step is worth six sites on the list (three to nine) and 15 of the 16 figures; no single other
  correction reaches the nine with the golden's figures.
- **Past evidence.** On the 11,857 days of 2018 to 2026 the analysis did not observe, the refill reproduces the
  reprocessed record to 0.065 degrees (root mean square) and -0.001 on the 1,174 hot ones, against 0.142 and -0.263
  for the flag means, 0.129 and -0.133 for the regression, 0.087 and 0.083 for the carried and nearer anomaly; the
  separation forces the refill among the reconstructions that disagree on any figure, and those that agree on every
  figure (asserted) need no forcing.

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the 16 sites of the register, every one graded |
| 2 | Unit of account | one site's season maximum, its level and its verdict |
| 3 | Attribution window | the 2027 heat season, 1 June to 31 October (UTC days), the 84-day sums reaching into March (methods 4) |
| 4 | As-of dating | Wednesday 3 November 2027: the extract to 2 November, the reprocessed record to 31 December 2026, the 2027 record due May 2028 |
| 5 | Version basis | methods note v3; guide v3.2, the flag read by each row's version (SF12); the May 2027 release |
| 6 | Denominator | none: sums and maxima |
| 7 | Weighting | none |
| 8 | Window length | 84 days (methods 3, SF3) |
| 9 | Boundary inclusivity | a HotSpot at 1.0 or more (SF2); levels when the DHW reach 4 and 8; the season's first and last days included |
| 10 | Rounding path | the level from the unrounded maximum (SF10); figures to the nearest whole number (SF11) |
| 11 | Tie-break | none needed |
| 12 | Maturity and censoring | the 2027 record of reference is unreleased, which is the estimand; re-issues arrive within three days and the extract runs to 2 November |
| 13 | Order of operations | latest issues, flags, units, the clear-sky difference, the refill, HotSpots, DHW, the maximum, the level, the verdict |
| 14 | Row order | no step depends on file order |
| 15 | Duplicate resolution | a re-issued day by its later issue (SF5) |
| 16 | Identity normalisation | pixel identifiers to site codes by the register |
| 17 | Netting against gross | none |
| 18 | Dimensional units | degrees Celsius; kelvin less 273.15 (SF13); degree Celsius weeks |
| 19 | Code and status semantics | the observation flag by version (SF12); the alert level names (SF7, SF15) |
| 20 | Integerisation | whole degree-weeks (SF11) |
| 21 | Clause scope | sections 3 to 6 apply to every site; the declared level from the bulletins reporting season days (SF7, SF8) |
| 22 | Forward window contents | the record of reference's 2027 release in May 2028; the survey sails from 15 November |

## Literal reader

Executing the prompt and the methods note word for word: each site's highest DHW on a 2027 season day on the record of
reference, its level and its verdict against the highest declared level. The record of reference for 2027 is not
released, so the literal estimand needs it anticipated from the near-real-time record and the 2018 to 2026 overlap;
every reconstruction that refills the unobserved days from the observed days either side, with the clear-sky
difference out (anomaly or temperature interpolation, a shape-preserving curve, each site's own or the heat seasons'
difference, the last observed anomaly carried, the nearer observed day), files the nine with the same whole numbers,
and every convention row of the fork table files the nine. The easy answer, the three, comes from an easy method (a
mean correction) on the same literal estimand, never from another reading.

## Oracles

None for the call: no 2027 figure on the record of reference, earlier survey list or ranking on it ships; the
bulletins are the declared levels the call checks; the 2018 to 2026 overlap matches the mean correction on average by
construction and shows its failure only conditional on the anomaly; the loggers end with the April 2027 downloads (the
season's readings are still on the reef) and the 2023 survey is another season. For the asks, the protocol's "recorded
once, on the slate line for the metre of tape its centre lies in" and the metre lines referee the repeats, and the
loggers' own step out of the water referees the boats' clocks; neither names a row, a boat or a zone.

## Ask sheet

**Ask A, each site's bleaching prevalence in the 2023 survey (per cent, one decimal) and the colonies it rests on (whole
numbers)** (32 figures). H18: the survey's baseline, a measure every site carries that the call does not turn on (the
request: "which the report compares against"); the call reads no survey row. Use: the November survey report sets each
site's 2027 bleaching against its 2023 prevalence. Primary device D6 (an event's quantity on every line it covers, grain
unstated): two of the 2023 volunteers (KT and DW) wrote a colony of 100 cm or more on the slate line of every metre of
tape it crossed, with its full diameter and condition each time, while the protocol records each colony once, on the
metre its centre lies in; nothing marks a repeat (every line keeps its own line number, so site, transect, sheet and
line stay unique), the hygiene battery's exact-duplicate and key checks pass, and the repeats show only as wide
colonies of one genus, diameter and condition on consecutive metres of one sheet: 153 on KT's and DW's sheets, none on
the four staff observers' (asserted). Hazards: the QA sheets (protocol section 5, 692 lines), PB03's transect 2 laid at
4.2 m (section 2), fire corals (MALC and MCOM, not in the annex, 48 lines), colonies under 10 cm (33 lines). Path: the
slates, the protocol's sections 2, 3, 5 and 6 and its annex, the register's survey depth, the dictionary (4 files, 10
columns: site_code, transect, sheet, observer, depth_m, metre, line, genus, max_diameter_cm, condition). Stops: every
filed rule with every slate line a colony (the cracker): prevalence -0.9 to +4.8 points and colonies +5 to +15, all 32
missed; nothing filtered: colonies +43 to +96, all 32 missed; every identical neighbour collapsed whatever its size:
four sites moved. Realism: volunteers new to a belt transect write a large colony on each metre line it covers, and
slate entry keeps every line as written.

**Ask B, each site's hours at or above its maximum monthly mean at its logger while in the water, June to October 2024
to 2026 (whole numbers)** (16 figures). H18: the reef's recent heat at the corals, a measure every site carries that
the call does not turn on (the request asks for it beside the baseline); the call reads no logger row. Use: the survey
report reads this year's bleaching against each site's recent heat at depth. Primary device D8 (a clock against a
filed cutoff): the log's times are the boat's GPS, which on the Ixchel shows local time and on the Cozumel II showed UTC
until its unit was replaced between the April and August 2026 trips, so on the Cozumel II's August 2025 retrieval trip
and its April 2026 trip every logged time runs five hours ahead of the loggers' local clocks; nothing marks it (the
dictionary gives the times "as noted from the boat's GPS"), and the loggers show it (on those two trips every logger
steps out of the water 4.0 to 4.9 hours before the logged time, on every other trip within two hours after it,
asserted). Read as local time, the August 2025 retrievals keep five readings from the cooler on deck and the lab's
seawater tank, all at or above the MMM. Hazards: the readings before deployment and after retrieval at every trip
(the log's times), the seasons on the loggers' clock (SF17, the same hours either way), the April 2026 trip's shifted
times (outside the seasons). Path: the readings, the log, the register's MMM, the dictionary (4 files, 9 columns:
serial, datetime_local, temperature_c, site_code, deployed, deployed_from, retrieved, retrieved_from, mmm_c). Stops: the log's
times as local (the cracker): +5 hours at every site, all 16 missed; no trimming: +33 to +82, all 16 missed.
Realism: field GPS units default to UTC until someone sets them to local time, and a station with two boats logs what
each screen shows.

Main population zero-counts: the call reads the near-real-time extract, the reprocessed record, the register's pixels
and MMM, the climatology and the bulletins; no slate, log or logger row is among them, no device or hazard row of
either ask sits in those files, and the call computes identically with the survey, logger and distractor files removed
(S1 in checks.py).

| Hazard | Asks moved | Per-ask deltas (largest) |
|---|---|---|
| wide colonies written on every metre crossed (D6, primary) | A | prevalence +4.8, colonies +15 |
| QA sheets, the off-depth transect, fire corals, small colonies kept | A | colonies +96 |
| the Cozumel II's GPS times read as local (D8, primary) | B | +5 hours |
| no trimming to the log's times | B | +82 hours |

Referee: the protocol's "recorded once, on the slate line for the metre of tape its centre lies in" with the metre
lines for Ask A, and the loggers' own step out of the water for Ask B; neither names a row, a boat's clock or a zone.

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed) | Verdict |
|---|---|---|
| Ask A, prevalence, all sixteen sites | S sheets, transects at the survey depth, annex genera of 10 cm or more, each slate line a colony | miss |
| Ask A, colonies, all sixteen sites | the same | miss |
| Ask B, hours, all sixteen sites | each logger's readings between the log's deployed and retrieved times read as local time, June to October 2024 to 2026, at or above the register's MMM | miss |

Measured by: generator/pair.py on the cut pack: the cracker keeps 0 of the 48 ask figures; the lazier paths keep 0
(nothing filtered, no trimming); the mirror (stopped at the regression of filled days' anomalies, six sites) keeps 17.2
of the 38 recommendation points (29 of 48 per-site criteria) and none of the ask figures.

Pair ceiling: 34.6 ((38 + 7 + 55 x 0) and (17.2 + 7 + 55 x 0), averaged)

Mirror leakage: 0.0 per cent of ask weight

## Pre-ship check

1. Domain: the call stands on each site's 2027 season maximum degree heating weeks on the reprocessed record of
   reference, anticipated from the near-real-time analysis by refilling its cloud gaps from the observations on both
   sides, as the reprocessed analysis fills them; with another field's nouns (a hospital's provisional and final case
   counts, a utility's estimated and actual meter reads) there is no clear-sky observation, no relaxation toward
   climatology under cloud and no HotSpot accumulation over twelve weeks, so the task stops making sense.
2. Two layers: Layer 1 (re-issued days, the flag recoded with version 3.2, the day with no analysis, kelvin in the
   reprocessed record, pixel keys, bulletins dated by the station's Tuesday while they report the UTC Monday) is neutral
   on the call (SF1 to SF17). Layer 2 is the reconstruction of the filled days, asserted alone to move the default path
   (the flag-mean correction, three sites) to the golden (nine) on the simulator's clean truth (R3).
3. No banned stump decides: nothing is planted (the bulletins are the declared levels the prompt asks the call to be
   compared against, not a ranking on the reference record); not semantics (every field read right, the flag-mean
   route still files three); not rule application (the methods note files the estimand, and nothing in the pack says
   how to anticipate the reprocessed record).
4. Gate G: no shipped artifact ranks the sites on the reference record; the two distractors (water clarity, the port's
   tide gauge) give no site a heat-stress figure.
5. Determinism: the refill's six variants (the anomaly or the temperature interpolated, a shape-preserving curve, each
   site's own or the heat seasons' clear-sky difference, the last observed anomaly carried, the nearer observed day)
   give the same sixteen whole numbers; 17 fork rows asserted; the verifier recomputes every graded figure by its own
   code (239 checks); two builds byte-identical.
6. Fingerprint: heart WARN (overuse.gate_g, repeat.deliverables, repeat.question_form, answered in the Draw); the
   people screen reads the four card personas and no other. The surface screen promotes five pairs, all in this
   author's wave: task245 on the same pairing two builds apart (legal at the draw, its three newest neighbours being
   task170, task244 and task172; differentiated on the card), and task246, task243, task244 and task242 on the shared
   README name and the population gap (task242 the G13 generator), each a different world and driver. Against task245:
   there the record loses days, the analysers stop on the very days the terminal's plume reaches them, and each lost
   day is rebuilt from that day's wind against the station's own response, interpolation in time being one of the
   wrong routes; here no day is missing (the analysis writes every day), the filled values are a one-sided relaxation
   written as the season ran, and interpolating between the clear days either side is the reconstruction the record of
   reference itself makes.
7. Judge (one isolated thread, Sonnet, medium, the bundle and the graded blocks only): DETERMINISTIC, APPROVE; every
   graded figure reproduced (the sixteen season maxima, levels, verdicts and declared levels, the 32 survey figures,
   the 16 hour counts, the 0.06 and the back-test); Gate G method_or_model_selection, analytical_non_defect; Gate H
   domain, layers and decisive step pass; spec gates pass. Its notes: PB06 the thinnest margin (8.85, every variant keeps
   it on the list); the colony repeats an ask-level reading the protocol's "recorded once" and the two observers'
   pattern pin; and the write-up's regression rival not reproduced because the pack carries no specification for it.
   Fixed: block 1's regression clause and its six sites removed (determinism-check section 5), and the workbook's Basis
   label for that route corrected to the direction fitted (the reprocessed anomaly regressed on the filled days'
   near-real-time anomaly). The two remaining rivals reproduce (four and three sites).

## Leak check

`leak.py --asof 2027-11-03`: REVIEW, no LEAK. Each REVIEW line:
- Sweep 4, the dictionary, README, survey protocol, methods note, user guide and release note: the shared terms are the
  field's nouns (analysis, near-real-time, observation, reference, temperature, station); none names a refill, an
  interpolation or the filled days' conditional error. The user guide's section 6 (differences larger where cloud keeps
  satellites from the sea; the reprocessed analysis for the best estimate of a past period) is the provider's ordinary
  statement of its two products and says nothing of how to anticipate the later one. Harmless.
- Sweep 6, the bulletins: each site's near-real-time DHW and level week by week, the declared basis the prompt asks the
  verdicts against; they rank nothing on the reference record. Harmless (the reader and the judge read them the same
  way).
- Sweep 8, `obs_flag`: the provider's column, documented in its user guide section 4, as satellite products carry
  quality and observation flags. Harmless.

Reader (one isolated agent, Sonnet, medium, the prompt and the pack only), on the first cut: Q1 to Q4 none; Q5 methods
sections 3 to 6 fix the estimand and leave open how the 2027 reprocessed record is anticipated (the design's open
method); Q6 an analytical choice ("building the expected reprocessed value from NRT using the overlap years, on a
method I would have to defend"). Its attempt filed the bulletins' four (PB06, PB07, PB09, PB10), stumped: it found the
filled days running cool by more when the anomaly is large and still corrected by offsets. Asks: it saw no open reading
on the survey and found no repeats; it flagged the boats' GPS times as possibly UTC and did not resolve them. Realism:
the logger models split exactly 64 and 64 and one note repeated on every row of a trip. Fixed in the generator: each
site alternates a pair of loggers of a model (64 serials, numbered by delivery), three MX2203 on trial from August 2024
and three sites keeping a TidbiT until April 2026 (61 TidbiT v2, 67 MX2203), the notes sparse and varied; the readings
are the same draws, so every graded figure held (figures.json unchanged; checks 534, verify 239, two builds
byte-identical, precut 51 with no FAIL, figures_check 76 with none absent, pair ceiling 34.6, mirror leakage 0.0). Its
other realism note (the survey's prevalences spread from 5.9 to 78.4 by site) kept: a 2023 bleaching year's site
prevalences run that wide, in no order of the register. A data-only repair, so leak.py alone after it.

## Tried and rejected

- 2026-10-18, the seed's own air quality network, the alert rule replayed on the archived provisional data against the
  ratified data: a direct count with no analytical step; with the provisional data overwritten, rebuilding them from
  the calibration log executes the network's ratification procedure (rule application).
- 2026-10-18, the alert log as the only record of provisional readings, its over-readings selected by the alarm itself:
  any treatment of the hours that did not alert lands the golden (a coin flip on one insight), the share over all
  hours at the level is read off the filed population (a semantics risk), and the observed misses refute the naive
  error model at once.
- 2026-10-18, verification by reference filters weighed for every alert day and a third of the others: the weighing
  design has to be filed, which makes the weights the obvious move, and a design-weighted estimate is task452's lesson.
- 2026-10-18, analysers' span drift growing with their age (or with the pollutant dose they have measured) and next
  season's analysers older: the exposure-clock lesson of task46, task132 and task134 v2; analyser drift by age swaps
  into any field's instruments unchanged; and the forward allowance reads as a forecast.
- 2026-10-18, a season's calibration-function change as one draw, the rule judged over the draws on record: which
  seasons stand for the coming one is the estimand's population, so filing it hands the step over and leaving it open
  is not determinate.
