# task179 design note

**Status: PAUSED 2026-10-23 at stage 1 (reopened from RETIRED 2026-10-21; see `## Retired` and `## Rebuild (2026-10-23)`). Architecture v2, re-sited 2026-10-21 into a fictional setting inside the round's second new cell,
Epidemiology & Public Health, `infectious-disease-transmission-modeling`, Forecasting.** The first cell (the
ambulance surge pool, never carded) and the redraw cell in Economics & Econometrics (never carded) are spent; their
records sit under `## First-cell record` and in `## Tried and rejected`. Re-screen nothing there.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task179.json`, architecture v2, first registered 2026-10-21 and
   re-registered at the re-site. `guard.py check` WARN only: `repeat.gate_g` against task178 (answered in item 5);
   `test.same_puzzle_older` and `test.same_driver_older` against task133, task196 and task180 (G12) and earlier
   task126, task138 and task82 (G3), differentiated on the card (left truncation of loan exposure, capture-recapture
   of uncounted events, events masked by instrument noise; none reads a delay distribution from linked pairs).
   Nearest drivers 0.07 (task251 v4) and 0.06 (task192 v1).
2. Pairing: Epidemiology & Public Health (client domain) / `infectious-disease-transmission-modeling` /
   Forecasting & Predictive Modeling. The one build on file in this task type is task501 (a next-generation matrix
   built from contact diaries of the season's regime); nothing here touches a contact matrix or an eigenvalue.
3. Niche: Larrowmede Medical Relief, a medical humanitarian organisation running two treatment centres in the
   fictional Dunmarrow Province of the fictional Republic of Orvanthe, projecting the cases its centres must plan
   for in epidemiological weeks 49 to 52 (30 November to 27 December 2026) of an outbreak of Tamberlow virus disease
   (a fictional haemorrhagic fever first described in this outbreak) under the provincial response plan's central
   scenario, from the province's line list and the response's transmission links.
4. Call and shape: the number of new cases (confirmed and probable, by date of symptom onset) in weeks 49 to 52
   under the central scenario, to the nearest thousand (`quantity_figure`, `count`, question form how-many), with the
   reproduction number and the mean serial interval as components. Shape `single-figure`.
5. Mechanism keys: gap population (the transmission links are not the population of transmission intervals, they
   are the subset whose case has already fallen ill) then time; generators G12 (absence of a record against a record
   of absence: the long intervals are missing because their later event has not happened, not because they do not
   exist), G3 (the record's interval against the process's), G13 (each pair observed only inside its source's
   horizon to the extract). G13 led the first draft and G3 the second; task178 and task484 took them into the window
   in turn, and G12 reads the step as honestly. Gate G `forecasting` (a forecast the correctly read past does not
   pin); the WARN `repeat.gate_g` against task178 is answered by the honest key, since no validation or standard pins
   a method here. Strategy `maturity_censoring` (right truncation of a delay at the extract).
6. Layer 2: `estimation_fit` (censoring and truncation), pattern
   `epidemiology-public-health/infectious-disease-transmission-modeling/1` (Rt needs onset timing and the
   generation interval). The default path is that card's method; the stump is the judgment it takes for granted,
   that the serial interval read from the outbreak's own pairs is the interval the renewal equation needs.
7. Furniture: forum `operations_desk` (the organisation's emergency desk orders beds and staff on the planning
   lead's figure); forcing event `incident_or_complaint` (the outbreak, with the response plan's phase 3 starting 2
   November); organisation family `hospital_or_health_provider` (a non-governmental operator whose role here is
   running treatment centres); role family `capacity_planner`; context artifact `capacity_report` (the centres'
   weekly bed and roster file); calibration `none`.
8. Spine: the provincial line list as extracted on Sunday 18 October 2026 (one row per notified suspected,
   probable or confirmed case); the 25,000-row file is the contact registry (one row per listing of a person).
9. Deliverables: `tvd_projection_w49-w52.xlsx` (the projection, its components and the ask tables) and
   `tvd_projection_curve.svg` (observed and projected weekly cases with phase 3's start marked).
10. World, fictional throughout: the Republic of Orvanthe and its Dunmarrow Province (provincial capital
    Kettlebank), seven districts with cases (Tamberlow, Quillmarsh, Threlmarren, Wendlecombe, Brindlecourt, Kettlebank
    North, Kettlebank South), the Dunmarrow Provincial Health Directorate, the Kettlebank public health laboratory
    and the Tamberlow field laboratory, Larrowmede Medical Relief and its two centres, and Tamberlow virus disease
    with its own provincial case definition. No real administrative geography, agency, product or report voice is
    used; `metadata.json` states that the setting is fictional and the data synthetic. The epidemiology is kept
    real: a growing outbreak (doubling about every 18 days), onset to notification to laboratory to outcome links,
    contact tracing. Personas from `guard.py names --geo "Republic of Orvanthe" --seed 179`: Jacqueline Arnold
    (response epidemiologist, owner of the planning note), Tanner Molina (emergency coordinator), Kristin Sampson
    (treatment-centre medical lead).
11. As-of: the line list and the transmission links extracted Sunday 18 October 2026 at 23:59 (Orvanthe Standard
    Time, UTC+1); notification closes within four days of onset, so onsets to Sunday 11 October are complete; the
    laboratories' exports were pulled at 08:00 on Monday 19 October.
12. Sources read for the domain (stumping 1.3): the cell's two library cards (renewal-equation Rt with onset timing
    and the generation interval; the next-generation matrix's eigenvalue); task501 (a contact matrix pooled over two
    regimes); task232 (a transmission rate per exposure from closed episodes whose outcomes surface after a delay
    window; here the delay itself is the estimated quantity); task181's lineage (counts read before their records
    finish arriving; here the counts are complete and the intervals between linked records are what the cut-off
    bends); task133 (left truncation; here truncation is on the right and by the later event).
13. Data-native sentence: a source-to-case link is entered in the tracing system only when the infected contact
    falls ill and is notified, and the outbreak doubles about every 18 days, so at the extract most sources are
    recent and appear only with the cases they infected within the few weeks they have had, which bends the links'
    intervals short in exactly the cohort the renewal equation's growth window reads.

## Screens (stumping 1.2, as code)

Prototypes in the session scratchpad, b179e/screen (`a1.py` to `a4.py`, `e1.py`; seeds fixed before outcomes,
the outbreaks that died out before 2,500 cases skipped). The world screened is a discrete-day onset process,
offspring negative binomial (R 1.7, k 0.4), serial interval a discretised gamma (mean 12.6, sd 7.4 days), 62 per
cent of cases linked to a source, extract at day 165; eight outbreaks of 6,979 to 18,354 cases with 4,364 to
11,356 pairs. Figures are the projected cases in a four-week window starting five weeks after a 40 per cent cut,
each route against the golden (truncated maximum likelihood, gamma) on the same pack.

- The default family lands about a quarter low and tightly: every pair fitted (empirical or gamma) -27.2 per cent
  (sd 0.8), the same with the renewal-ratio R -27.0 (2.5), dropping pairs whose case fell ill in the last 21 or 42
  days (the hygiene reflex, on the case's clock) -27.9 and -26.9.
- The golden family converges where the data close it: truncated gamma 0.0, truncated Weibull +0.5 (0.1), the
  reverse-time nonparametric estimator 0.0, sources whose onset is 50 or 70 days before the cut-off (the
  complete-cohort subset, on the source's clock) +0.9 (3.0) and +0.3 (4.9). The lognormal reads +4.0 and the data
  reject it (negative log-likelihood 64 to 183 units worse than the gamma on every pack).
- The open residue is the current reproduction number's window and estimator: from the growth rate over 42 days
  it is the golden, over 28 days -0.1 with sd 7.4, the renewal ratio over the same 42 days +0.6 with sd 3.0. That
  is a knob, not the stump, so the window is filed (the six weeks to 11 October, weeks 36 to 41) and the spread of
  the two estimators on that window is measured on the cut pack before the rounding is set.
- Dispersion: the decisive quantity is a delay distribution's location; the parametric forms the data do not
  reject agree within 0.5 per cent and the nonparametric estimator within 0.1.
- Variance-only: the step moves the point (a quarter of the figure), it does not widen an interval.
- Common-exposure subset: the subset already complete, sources old enough that every case they caused has fallen
  ill, lands within its own sampling noise; choosing it means filtering on the source's onset, which is the
  decisive step itself. On the case's clock (the reflex) it lands the default.
- Truncation direction: the cut-off hides the top of the interval distribution (the long intervals), which is the
  case the screen keeps alive.
- Literature reflex: none applies in the re-sited world, since the virus is described only in this outbreak and the
  planning note says no parameter comes from elsewhere; in the screened world an outside interval (15.3 days, sd 9.3)
  landed +30 per cent, outside the golden's bin either way.
- `guard.py slots --driver`: vocabulary hits only (task194, task190, task253, task117, task501); no slot records
  a truncated delay distribution or a serial interval dying.

## Default path

1. Daily onsets of confirmed and probable cases from the line list (people found not to be cases and suspected cases
   left out, a case notified twice under two numbers kept once by its sample), complete to 11 October.
2. The serial interval from every source-to-case pair in the transmission links: onset of case less onset of source,
   2,449 pairs, a gamma fitted or the pairs' own distribution (mean 11 days).
3. The reproduction number implied by the exponential growth rate of daily onsets over weeks 36 to 41 (0.038 a day)
   through that interval (1.5).
4. The renewal equation forward from 12 October, the reproduction number halved for every source with onset from
   2 November, cases summed over weeks 49 to 52 (3,564).

Ends on: 4,000 cases
Golden: 5,000 cases

## Stump sentence

A competent analyst fits the serial interval to every source-to-case pair in the transmission links (11 days), takes
the reproduction number implied by the growth of onsets over weeks 36 to 41 (1.5), halves it from 2 November and
projects about 4,000 cases for weeks 49 to 52 instead of about 5,000, because the tracing system holds a link only
once its case has fallen ill, so September's and October's sources appear only with the cases they infected quickly;
read against the time each source had to 11 October, the links give the 13-day interval the chains run on, a
reproduction number of 1.6 and a December that holds a quarter higher.

## Three rules

Task type: infectious-disease-transmission-modeling (Epidemiology & Public Health): the outbreak's line list and transmission links turned into a serial interval, a reproduction number and a renewal-equation projection of cases under the response plan's central scenario, a projection serving Forecasting & Predictive Modeling.

Domain test: the deciding quantity is the serial interval distribution the renewal equation runs on, estimated from the outbreak's own transmission pairs the way a transmission modeller estimates a delay during a growing epidemic: each pair read against the longest interval its source could show at the cut-off (right truncation), then the reproduction number from the growth rate through that interval (Wallinga and Lipsitch) and the renewal equation forward under the scenario's halving.

Swap: "how many referrals a sales network brings in December, from referrer-to-referee links" keeps a link between two dated events and loses the step's ground: no renewal equation turning a growth rate into a reproduction number through the generation interval, no scenario that halves transmission by the source's onset, no epidemic whose growth makes the recent sources the numerous ones.

Layer 1: a case notified a second time from a neighbouring district under a new number with the same laboratory sample, people found not to be cases and suspected cases awaiting a result in the line list, rows fed from the field laboratory's forms carrying ISO dates beside day-first ones, links graded by certainty and links whose case was later discarded; each is how a surveillance line list and a tracing system write, nothing is placed to be caught, and checks.py asserts the call holds under each (SF1, SF6, L1, L2).

Layer 2: estimation_fit, the data's real structure: the serial interval is read from pairs that exist only once the later case has fallen ill, so the sample is right truncated at the extract, and during growth the truncation falls on the recent sources that are most of the pairs.

Decisive step: estimating the serial interval with each pair conditioned on its interval being no longer than 11 October less its source's onset (or any estimator that reads the pairs against their sources' horizon), which moves the mean from 11 to 13 days, the reproduction number from 1.5 to 1.6 and weeks 49 to 52 from 3,564 to 5,049 cases.

Not semantics: every field, code and definition read correctly (the classifications, the duplicate case numbers, the two date formats, the links' source and target, the dictionary's note that a link is entered when the target case is notified) still leaves the easy route fitting the pairs as they stand, because no field says the pairs are a truncated sample of the outbreak's intervals; the step is the inference that a growing outbreak cut off at an extract holds only the quick intervals of its recent sources, which the data show (the mean interval of the pairs falls from 13.5 days for sources ill in August to 11.0 for September's and 5.2 for October's) and no sentence says.

Not rule application: the planning note files the population, outcome, window, unit, scenario and the reproduction number's basis, and no rule says how the serial interval is read from the links; executing every filed rule with the pairs fitted as they stand files 4,000 cases.

Analyst test: a strong analyst who cleans the line list and reads every rule, fitting the serial interval to every pair in the links, files 4,000 cases (the default path's Ends on); one who drops the pairs whose case fell ill in the last fortnight (the hygiene reflex, on the case's clock) files 4,000 too; only reading each pair against its source's time to 11 October files 5,000; checks.py runs the three on the generator's clean truth (R3a, R3b, R3c).

Estimand: the planning note (planning_note_phase3_2026-10-19.pdf, sections 1 to 3): the population (new cases of Tamberlow virus disease, confirmed and probable under the provincial case definition, in the seven districts with cases), the outcome and unit (cases by date of symptom onset), the window (ISO weeks 49 to 52, 30 November to 27 December 2026), the scenario (every case with onset on or after 2 November causes half as many new cases as cases did over weeks 36 to 41, whose reproduction number is the one implied by the exponential growth rate of their daily onsets), the records (the line list and the transmission links as extracted on 18 October, onsets complete to 11 October, no outside parameter).

No decoy: nothing is planted: the line list, links, contact registry, laboratory exports, capacity report and situation report are the producing systems' records, the planning note states the scenario without a method, and no serial interval, reproduction number, projection or published parameter ships anywhere in the pack.

No certified replay: no certified or published serial interval, reproduction number or projection ships; the planning note says the virus is described only in this outbreak, so the method is not recovered by reproducing any figure.

Lesson: a delay read from linked records that exist only once the later event has happened is truncated at the extract, and while the process grows that truncation sits on the recent sources, which are most of the record; no build on file estimates a delay distribution from linked pairs read against each pair's own horizon.

## Readability screen

Each rung, the sentence or file a reader would have to read to take it, and whether any shipped text hands it over.

| Rung | What takes the reader there | Verdict |
|---|---|---|
| Layer 1: the duplicate case numbers, non-cases and suspects, two date formats | the dictionary and the line list | readable |
| R0 growth of onsets over weeks 36 to 41 | the planning note, section 2 | readable |
| R1 (default path) the serial interval from every pair as it stands | the transmission links and the dictionary | readable |
| R1b the pairs whose case fell ill in the last fortnight dropped | the hygiene reflex on the links' dates | readable |
| R2 (decisive) each pair read against its source's time to 11 October | nothing: no sentence names truncation, the interval's bias, a cohort of complete sources or an estimator; the dictionary says when a link is entered and nothing about what that does to the intervals | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a case | Confirmed and Probable, a person notified twice under two numbers counted once by sample | both numbers kept; Not a case kept | same call (5,206; 4,898) | planning note section 3; checks.py SF1 |
| SF2 | completeness | onsets to 11 October complete, pairs whose case fell ill by 11 October | pairs and onsets to the 18 October extract | same call (4,739) | planning note section 3; SF2 |
| SF3 | the growth rate | log-linear least squares on daily onsets, 31 August to 11 October | Poisson regression on daily onsets; weekly counts | same call (5,005; 5,004) | SF3 |
| SF4 | the reproduction number's basis | the one implied by the exponential growth rate through the serial interval | the renewal ratio over the same six weeks (5,508) | not the filed estimand | planning note section 2, "implied by the exponential growth rate of their daily onsets" |
| SF5 | the halving | every source with onset on or after 2 November transmits at half | cases whose own onset falls on or after 2 November halved (2,525) | not the filed scenario | planning note section 2, "every case with symptom onset on or after 2 November causes half as many new cases" |
| SF6 | the links' certainty | every link | Low certainty dropped | same call (4,992) | SF6 |
| SF7 | the interval's family | discretised gamma | Weibull; the reverse-time nonparametric estimator; lognormal | same call (5,062; 5,047; 5,406, the lognormal 36 log-likelihood units worse) | SF7 |
| SF8 | the window | ISO weeks 49 to 52 by onset, 30 November to 27 December | none | filed | planning note section 1 |
| SF9 | rounding | the unrounded projection to the nearest thousand | none | prompt | prompt.txt |
| SF10 | the projection's start | the renewal equation from 12 October on onsets to 11 October | the onsets of 12 to 18 October read as complete (4,241) | not the filed record | planning note section 3, "onsets to Sunday 11 October are complete in the extract"; SF10 |

## Ladder

Built values from the cut pack (generator/checks.py R1 to R3c, SF1 to SF10), cases in weeks 49 to 52.

| Rung | Route | Serial interval (days) | R | Cases | Call |
|---|---|---|---|---|---|
| R1 (default path) | every pair as it stands, gamma or empirical | 11.13 | 1.484 | 3,564 | 4,000 |
| R1b | pairs whose case fell ill in the last 14 days dropped | 11.09 | 1.483 | 3,549 | 4,000 |
| Golden | truncated gamma, each pair conditioned on its source's time to 11 October | 13.16 | 1.586 | 5,049 | 5,000 |
| Golden family | truncated Weibull; reverse-time nonparametric; sources 50 or 60 days old only | 13.04; 13.14; 13.15; 12.83 | 1.585; 1.586; 1.589; 1.573 | 5,062; 5,047; 5,092; 4,857 | 5,000 |

- Dominance: every member of the golden family sits in [4,500, 5,500), the nearest 7.4 per cent from an edge (the
  complete-cohort subset at 60 days, 4,857), the golden 8.9 per cent; a bootstrap of the pairs (60 draws) puts the
  golden's sd at 3.0 per cent and every draw in the bin (B1); the default family sits in [3,500, 4,500).
- The data separates the readings: the mean interval of the pairs by the month their source fell ill falls from 13.5
  days (August, 519 pairs) to 11.0 (September, 1,486) and 5.2 (October, 215), which an interval that does not change
  cannot do unless the record is cut off; read against each source's horizon, the truncated fit's interval holds
  (sources 50 days old or more, whose cases have all fallen ill, give 13.15 days).

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | new cases, confirmed and probable, in the seven districts with cases | filed (planning note 1, 3) |
| 2 | Unit of account | a case by date of symptom onset | filed (planning note 1) |
| 3 | Attribution window | ISO weeks 49 to 52, 30 November to 27 December 2026 | filed (SF8) |
| 4 | As-of dating | the extract of 18 October 23:59, onsets complete to 11 October | planning note 3; manifest (SF2) |
| 5 | Version basis | one line list and one links export, no earlier release | the manifest |
| 6 | Denominator | none (a count) | commutes |
| 7 | Weighting | each pair once, each day's onsets as counted | SF3, SF7 |
| 8 | Window length | the growth window weeks 36 to 41 | filed (planning note 2) |
| 9 | Boundary inclusivity | onset on or after 2 November halved; 30 November and 27 December inside | filed (SF5, SF8) |
| 10 | Rounding path | the unrounded projection to the nearest thousand | prompt (SF9) |
| 11 | Tie-break | none | the golden family 3.0 per cent or more inside its bin |
| 12 | Maturity and censoring | the pairs right truncated at 11 October; onsets complete to 11 October | the decisive step; SF2 |
| 13 | Order of operations | clean, pair, fit, grow, project from complete onsets, sum | SF10 |
| 14 | Row order | none | commutes |
| 15 | Duplicate resolution | a case notified twice counted once by its sample | SF1 |
| 16 | Identity normalisation | case numbers across the line list and the links, duplicates mapped to the first | SF1 |
| 17 | Netting against gross | not a case and suspected rows out | filed (planning note 3, SF1) |
| 18 | Dimensional units | days, cases | the dictionary |
| 19 | Code and status semantics | classifications, certainty grades | the dictionary (SF6); never the stump |
| 20 | Integerisation | none before the rounding | commutes |
| 21 | Clause scope | the halving applies to every source in every district from 2 November | filed (SF5) |
| 22 | Forward window contents | cases not yet ill, the scenario's halving the only change | filed (planning note 2) |

## Literal reader

The planning note executed word for word asks for the cases with onset in weeks 49 to 52 under a scenario whose base
is the reproduction number the growth of weeks 36 to 41 implies through the outbreak's serial interval; the literal
question is the interval the chains run on, which the links show only in part, since a link exists once its case has
fallen ill. A literal reader who fits the links as they stand has assumed the extract holds every interval its
sources will produce, which the falling mean interval by source month contradicts; every other reading converges or
violates a quoted sentence (fork table). Re-run on the finished pack.

## Oracles

- No shipped file carries a serial interval, a reproduction number, a projection or a published parameter for the
  virus; the planning note says none comes from elsewhere.
- The Kettlebank public health laboratory's results, the centres' admissions and the safe burials log are
  distractors (metadata.json); none ranks a projection.
- The situation report counts cases by week of notification as notified at 13 October; it projects nothing.
- No control ties only under the golden on the asks.

## Ask sheet

- **Ask A, contacts first listed in weeks 37 to 39 in Tamberlow, Quillmarsh, Kettlebank North and Brindlecourt:
  different people and the percentage who completed follow-up (eight figures, whole numbers and one decimal).**
  Home: the planning note's section 4 (the follow-up the scenario leans on). Path: the contact registry. Primary
  device: the same records under two key schemes: in the four districts the directorate's paper listings are
  entered at the district office beside the organisation's tablet listings of the same contacts, and the paper form
  carries an estimated age one to three years off the tablet's, so the exact person key counts those people twice;
  only source case, household, initials and sex, listed within a day, tie them. Hazards: a person exposed to two
  cases is listed once for each; completion is the person's last listing, not each listing's.
- **Ask B, the Tamberlow field laboratory's diagnostic samples by ISO week of collection, weeks 38 to 41: average
  hours from collection to final result and the percentage resulted within 24 hours (eight figures, one decimal).**
  Home: the planning note's section 4 (the laboratory turnaround). Path: the field laboratory's workbook. Primary
  device: a clock basis: the analyser writes its result time on UTC while collection and reception are keyed on
  local time (UTC+1); the evidence is in the data, results less than the 92-minute cartridge run after reception and
  positives a day before the line list's lab_result_date. Hazards: the final result is the re-run after
  Indeterminate; discharge-control samples are out.
- **The construction layer:** the call, its two components and the chart; the cracker has them.
- **Main population zero-counts (asserted):** the call reads the line list and the links only; the registry and the
  laboratory workbook are read by the asks only (X1).
- **Hazard table (asserted):** A1 to A3, B1 to B3 in checks.py; none moves the call.
- **Referee:** none.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, people and completion by district | the exact person key, the last listing's status; keeps 0 of 8 | miss |
| B, turnaround by week | the final result on the clock the file shows; keeps 0 of 8 | miss |

- Mirror leakage: 0.0 per cent of ask weight on the cut pack (0 of 16).
- Pair ceiling: 28.5 on the cut pack (weights 38 / 7 / 55: the cracker keeps the call and instructions, 45.0; the
  mirror at the default path misses the call and keeps no ask figure, 12.0). Re-measured by the stage 4 readers.
- Measured by: generator/ceiling.py on the cut pack.

## First-cell record

**First cell (2026-10-18).** New, Forecasting, seed FC50. The world was
moved honestly off `local_government`: a private ambulance company holds a city's 911 ambulance contract (the city
stays as the contract's counterparty) and decides its own summer surge pool, ten medic units for the weekend
20:00 to 24:00 block from June to August, any it does not need offered to the county's mutual-aid roster for the
summer; the contract's deployment standard staffs so that on nine weekend evenings in ten the units can answer every
call in the block at 1.2 unit-hours a call, and from June dispatch sends any unit in a district to any call in it,
North (planning areas 1 and 2), Central (3 and 4) and South (5). The world, the decision and the quantity were kept.
The seed's own mechanisms (a filed staffing formula executed literally, the public dataset's suppression of one-
and two-call cells, a sentence telling the solver to pool the areas) were never candidates. Two decisive steps were
screened on code, each one of the brief's ideas in its strongest form, over three seeds each plus sweeps, and
neither held. No architecture is live. This note holds the screen record only; it carries none of the `precut.py`
sections, because no design exists. The prototypes stay in the session scratchpad (b179/screen:
`c1_pool.py`, `c1_summary.py`, `c1_station.py`, `c1_total.py`, `c2_level.py`, `c2_sigma.py` and `screen179.py`,
whose output `screen179.out` is byte-identical with `screen179_run2.out` over two runs).

**The structural sentence, and the first thing to read.** The quantity cannot carry a graded whole-unit call under
the bar, whatever the decisive step. A district's units at the 9-in-10 standard are the ceiling of 0.3 times the
90th percentile of its block calls over one summer's 39 or 40 Friday, Saturday and Sunday evenings, and the record that
estimates that percentile is at most nine or ten summers of those evenings: the golden's own bootstrap sigma is
0.40 to 0.91 units in every realistic world measured (1.51 at twice the size), against the 0.25 units a whole-unit
bin leaves once its quarter-bin margin is taken, and on one pack the defensible estimators of that percentile
spread 0.44 to 1.19 units; only small Poisson-dominated districts reach 0.24 and 0.22, where every lever on file
(pooling, co-movement, a trend, a break, a one-off) moves the call by at most one unit and the cheap routes land.
The total of the three districts is worse: its sigma is 1.09 to 1.19 units at the base world (`c1_total.py`).
And the one forward change this world really carries, district dispatch, is the estimand's unit: once the standard
names the district's block as what its units must answer, the district's own evening totals in the record,
filtered, summed and quantiled with a trend, are the golden family, which is the first thing a strong analyst
builds. A draw on this quantity needs a graded figure resting on many more events than one evening's percentile (a
season's unit-hours, say, which changes the seed's quantity), or another world.

**The registration finding.** Nothing was registered and no axis of the window was spent. The window moved during
the screen: at fa74407 it was task201, task247 and task165; at 2689b12 it is task165 (`council_or_assembly`,
`purchase_order_or_contract`, `local_government`, `operations_director`, `register`, `single-figure`,
`composition_mix`), task268 (`board_of_directors`, `launch_or_rollout`, `retailer_or_ecommerce`,
`operations_director`, `operations_log`, `14`, `composition_mix`) and task248 (`line_manager_or_team`,
`cutover_or_migration`, `government_agency`, `capacity_planner`, `monitoring_export`, `03`, `other`). The keys this
world offers honestly outside it, had a design held: organisation `hospital_or_health_provider` (a licensed
ambulance service), forum `customer_or_counterparty` (the city's EMS contract office receives the summer deployment
plan), forcing event `other` (the county's mutual-aid roster closing in May), context artifact `filed_standard`
(the contract's deployment standard), calibration `prior_period_close_out` (the summers' close-outs), shape `05`
(ten units across three districts, the rest released). The honest role is `capacity_planner` (the contractor's
deployment planner), which task248 now holds, and the honest strategies are `grain_or_unit` for candidate 1's
pooling reading and `forecast_method_backtest` for candidate 2, both free.

**The taxonomy finding.** The honest home is Healthcare Delivery & Health Economics,
`utilization-access-demand-forecasting` (ambulance demand forecasting; the client library's pattern 4 there, plan
capacity to an overdispersed quantile against a mean plus a Poisson margin, is this quantity exactly), or
`patient-flow-beds-workforce-optimization` (staffing to the standard). The urban-regional municipal-service cell is
held by task165's subdomain in the window.

**The repeat screen.** `guard.py recent`, `coverage`, `mechanisms --objective forecasting` and `slots` ran before
any card, `slots` on the pooled-percentile driver, the level driver and the terms pooling, percentile, surge,
ambulance, medic and dispatch: no slot or card spent a pooled-percentile or a surge-pool level mechanism. The binding
matches are by the abstraction test: candidate 1's co-movement reading is task143's driver (a joint tail of a few
members whose error is mostly a component they share, the members treated as independent misstating it, the shared
component carried into the joint quantity), and its percentile-of-a-total reading sits beside task142 (an upper
percentile of a period's total built from the units that generate it). The brief's near drivers were read in full
on their cards: task148 (Erlang A with reneging in a 911 queue), task159 (platform backlog behind full trains),
task160 (regional waves timed by their lag) and task162 (version uptake set by the monthly restart burst); neither
candidate touches them.

## Tried and rejected
- **Architecture v2 (the serial interval read from transmission links right truncated at the extract), spent at stage 4 Gate F on target.zip 9e1843f8:** scored reader B landed 5,000 cases, R 1.6 and 13 days on its own first route, "Serial interval: onset differences on transmission links where both ends are cases; sources with early onset (right-truncation), mean about 13 days, gamma (shape 2.86, scale 4.6). R from r via gamma moment generating function: 1.59", then the renewal projection with the halving from 2 November; it kept 0 of 16 ask figures. The correction is a reflex at medium effort in this field (the textbook nowcasting caution), so it was the default path, not the stump; the judge and reader A were stopped.
- **Architecture v2's first world (a named real disease in a named real province):** declined on the real-places records concern, since its pack would be fabricated public-health records of a real outbreak; the mechanism was re-sited unchanged into the fictional Republic of Orvanthe.

- **Candidate 1: the district's requirement read from the areas' joint evenings, against the closed summers'
  area-by-area staffing, the areas treated as independent, a square-root pooling law and a pooling discount** (the
  brief's first and second ideas; `c1_pool.py`, `c1_summary.py`, `c1_station.py`, `c1_total.py`, seeds 1, 2 and 3
  fixed before outcomes).
  Killed at stage 1 on measurement and on the estimand screen.
  - The world: five planning areas whose block calls are Poisson around a lognormal intensity carrying a city-wide
    evening factor (weather, events), a district factor and an area factor, Friday 0.95, Saturday 1.15 and Sunday
    0.88, 3 per cent a year; 2026 means 14, 12, 18, 10 and 15 calls a block; summers 2021 to 2026 (236 evenings),
    the truth simulated on 200,000 evenings of 2027.
  - The golden family on one pack (the district's evening totals rescaled to 2027 by their own log-linear trend and
    quantiled: type 7, type 1, Harrell-Davis, last three summers, area trends summed, additive rescaling, a negative
    binomial by weekday mixed): at the base world (city factor 0.15, district 0.05, area 0.10) North 10.92 to 11.22
    continuous units, Central 11.43 to 13.37, South 6.40 to 7.03 for the type 7 member, the family spanning two
    whole numbers in 6 of 9 district-seeds, a bootstrap sigma of 0.47 to 0.58 (North), 0.53 to 0.69 (Central) and
    0.38 to 0.44 (South).
  - The sweep, North and Central over three seeds (sigma, family spread on one pack, the area-by-area default's
    units above the golden, and how often independence and the square-root law land the golden's whole number):

    | World | Sigma | Family spread | Area-by-area | Independence lands | Square-root law lands |
    |---|---|---|---|---|---|
    | city factor 0.05 | 0.43 | 0.44 | +1.50 | 6 of 6 | 6 of 6 |
    | city factor 0.15 (base) | 0.58 | 0.62 | +1.17 | 3 of 6 | 4 of 6 |
    | city factor 0.25 | 0.71 | 0.88 | +1.33 | 5 of 6 | 5 of 6 |
    | city factor 0.35, area 0.15 | 0.91 | 1.02 | +1.00 | 0 of 6 | 0 of 6 |
    | nine summers (2017 to 2026 less 2020) | 0.40 | 0.61 | +1.50 | 5 of 6 | 5 of 6 |
    | twice the size | 1.51 | 1.19 | +1.67 | 0 of 6 | 0 of 6 |
    | small Poisson districts (means 4 to 6 an area) | 0.24 | 0.22 | +1.00 | 6 of 6 | 6 of 6 |

  - The lever at the truth: area-by-area staffing needs one unit more than the district in North and Central (13
    against 12, 8 per cent of the units a district needs), one or two at twice the size, none in South, against the
    brief's 30 per cent. Staffing station by station in the closed summers (three station areas a planning area)
    raises it to 29 to 33 per cent (16 against 12, 9 against 7) and changes nothing else below.
  - One dial: the independence and square-root routes miss only where the city factor is strong enough to make the
    golden's own sigma 0.91 units or more and the family spread a unit; where sigma falls toward 0.24 they land in
    every district-seed. No world puts both rivals a bin away while the golden holds a quarter-bin and one sigma.
  - The eda6c8c screens, as code (`screen179.py`): dispersion fires (the co-movement is estimated, and on one pack
    the family spreads 0.49 to 0.78 units); variance-only passes (area-by-area +0 to +2, independence -1 to +0, the
    point moves); the common-exposure subset fires in 6 of 6 district-seeds, since the district's own evening totals
    filtered, summed and quantiled are the golden, a filter and a sum with no model; truncation direction: blanking
    station cells of one or two calls (13 to 21 per cent of evenings carry one) leaves every district's units
    unchanged at an imputation of 0, 1, 1.5 or 2, so the suppression hides the bottom and is Layer 1 at most.
  - Why it is dead whatever the tuning: pooling is the estimand's unit (the district's block, which the standard
    has to file), so filing it makes the computation follow and the strong analyst's first build, the district's
    own totals, is the golden (rule 3, rule application); the co-movement reading is task143's driver; and the
    sigma floor above holds at every size.
- **Candidate 2: next summer's level against the record's, a trend, an accelerating district, a break and a
  one-off, each route priced in whole units and the route chosen on the 2025 and 2026 summers held out** (the
  brief's third and fourth ideas; `c2_level.py`, `c2_sigma.py`, seeds 1, 2 and 3 fixed before outcomes, then 101
  to 120 for the routes' own sigma). Killed at stage 1 on measurement. Built on small Poisson districts (2026 means
  North 16, Central 20 and South 11 calls a block, city factor 0.06) so that the percentile's noise is the smallest
  the world allows; summers 2018, 2019 and 2021 to 2026, spring weekends through April 2027.
  - The routes: the last summer flat; the last summer times the record's trend; every summer detrended; the last
    three summers on their own trend; the last summer times spring 2027 over spring 2026; a quadratic trend; the
    plain mean of the summers.
  - A, 3 per cent a year everywhere: Central's truth 9 units (8.10 continuous); the routes' means over 20 seeds
    7.36 to 8.42, their own sigma 0.19 to 0.45; on seeds 1 to 3, 5, 3 and 5 of the 7 routes land the truth's whole
    number; the back-test lands the truth in 13 of 20 and picks six different routes across them (every summer
    detrended 9 times, the last summer flat 4, the last three 4).
  - B, North's growth accelerating from 4 to 9 per cent a year from 2022: truth 8 (7.20); routes 5.40 to 8.31 on
    seeds 1 to 3, 2, 1 and 3 of them landing; the back-test right in 1 of 3.
  - C, Central 18 per cent lower from January 2025 (a diversion programme): truth 7 (6.90); routes' means 5.95 to
    7.17, sigma 0.15 to 0.48; on seeds 1 to 3, 4, 3 and 7 of 7 routes land; the back-test lands the truth in 17 of
    20, picking the plain mean of the summers in 8 of them (and on seeds 1 to 3 every time), which lands by
    cancellation (the break against the trend, mean 6.94).
  - D, South 20 per cent higher in summer 2026 only: truth 5 (4.80); only the plain mean lands (4.49, sigma 0.10),
    the flat hold once; the back-test lands the truth in 2 of 20 and never picks the plain mean.
  - The eda6c8c screens, as code: dispersion and truncation direction do not apply (a level, no suppressing
    threshold on the path); variance-only passes (on seeds 1 to 3 each scenario's routes spread 0.58 to 2.91
    continuous units); the common-exposure subset fires, since the summers already at the coming level, filtered
    and quantiled (the last summer, the last three on their own trend), land the truth in 8 of 12 scenario-seeds
    (all three of A and C, one of B and of D).
  - Why it is dead: the levers a trend, an 18 per cent break, a 20 per cent one-off and an accelerating district
    can buy are a unit or less on districts this small, against routes whose own sigma is 0.10 to 0.48 units (0.26
    to 0.48 for every route that carries a trend), so the flat hold, the plain mean and the last summer land, two
    wrong steps cancel (scenario C), and two held-out summers of 39 or 40 evenings cannot select the route (it lands the
    truth in 2 to 17 of 20 depending on the scenario). On larger districts the levers grow with the noise, as
    candidate 1's sweep shows.
- **Paper screens, not coded.**
  - Heat normalised over a long weather record: the lever is the record's weather sample against climatology,
    whose sign the draw sets, and the recent summers are the better guide to a warming climate, so the reading is
    contested.
  - A new venue's or team's weekend evenings on a filed event calendar: `composition_mix` (held by task165 and
    task268), the coming window's cells unfilled, and the venue's own event evenings filtered and divided hand it
    over.
  - A new development's occupancy: its occupied dwellings' rate times the forward occupancy is two filters and a
    divide.
  - An alternative-response or sobering-centre pilot going city-wide: a filed forward condition, the pilot
    district's own post-period evenings at the coming exposure, and a lever of a few per cent of block calls.
  - A frequent-caller programme and its regression to the mean: a lever of a few per cent.
  - Calls passed to county mutual aid or held when an area's units were all committed (capacity-censored demand):
    task168's driver, and a mutual-aid log that records every overflow call makes it a join.
  - The county's own units cut, so more of its calls overflow to the contractor (a loss model): task156's driver
    (work reaches a second tier only when the first falls short).
  - Hospital offload delays or cross-area travel lengthening each call under district dispatch: the 1.2 unit-hours
    a call is part of the filed estimand, and leaving it open makes the quantity a duration times a count,
    task142's driver.
  - Peak concurrency inside the block: task142's and task148's drivers, and the filed unit-hour standard does not
    ask for it.
  - Summing the block's hourly 90th fractiles (the demand-pattern reflex) or the stations' requirements: the
    estimand's unit again, which a strong analyst reads off the standard.
  - The predictive spread widened by next summer's own level shock: variance-only, the golden always above the
    plug-in, so a padding reflex lands it.
  - A summer-specific growth against all-year growth: a lever of a few per cent a year.
  - One 9-in-10 condition across the three districts jointly: the estimand again, and once filed the joint
    record's evenings answer it by a count.

- **Redraw cell, 2026-10-19: Economics & Econometrics, `time-series-macro-econometrics`, Forecasting.** The cell's
  three library cards (cointegration critical values, the Johansen rank's deterministic terms, shock identification)
  were read first; `guard.py recent`, `coverage`, `mechanisms --objective forecasting` and `slots` (pass-through,
  asymmetric, invoicing, indexation, cointegration, error correction, recovery, seasonal, mortgage, lock-in, rent,
  catch-up, settlement, Phillips, kink, capacity utilisation) ran before any candidate. No build on file sits in this
  task type. The live window at a932f79 is task249, task177 and task270 (strategies `causal_design`,
  `forecast_method_backtest`, `population_selection`; patterns G14, G16, G12; task269 is spent and skipped). Prototypes
  in the session scratchpad, b179r/screen: `s1_cp.py`, `lm1.py`, `d1.py`, `w1.py`, `w2.py`, and `screen179r.py`, whose
  output `screen179r.out` is byte-identical with `screen179r_run2.out` (as `lm1.out` is with `lm1_run2.out`). Seeds
  were fixed before outcomes. No card was drafted, because nothing passed the measurement.
  - **Measured: a business survey's up, same and down shares against the quarter's mean output move** (the balance
    bridge against a quantification that scales the shares by the firms' spread, Carlson-Parkin; `s1_cp.py`, 20
    world draws a scenario, 1,500 firms a quarter, 127 quarters, t(5) firm growth). At ordinary spread the balance
    bridge lands (truth -1.0: balance -0.86, golden -0.98); only a deep fall at an unprecedented spread separates it
    (truth -3.0 at spread 12: balance -1.80, the up-and-down two-share regression -2.55, golden -2.89 with a sd of
    0.35, 12 per cent of the figure). The nearest reflex sits about one golden sigma away, the golden's own sigma is
    an order above the bar, and the separating world needs a recession no record has seen.
  - **Measured: long memory, a fractionally integrated series against the AR chosen by AIC and the KPSS-chosen unit
    root** (`lm1.py`, 40 draws, d 0.4, 480 months, the mean of months 25 to 36). The AR by AIC, the AR(1) and the
    estimated-d forecast agree (mean absolute errors 0.605, 0.593 and 0.599 sd units, the random walk 0.936), and all
    three miss the truth through the sample mean's own long-memory error (correlation -0.89 to -0.93 with it). No
    lever between the textbook route and the golden: the residue is the mean, not the method.
  - **Measured: national excess unemployment twelve months on when the shock sits in the slowest regions** (bottom-up
    regional persistence against the national AR; `d1.py`, 30 seeds, eight regions at monthly persistence 0.90 to
    0.985). The national AR understates the remaining excess by 0.108 (24 per cent of 0.459); the bottom-up AR(1)
    overshoots by 0.087 with a sd of 0.085, so the golden's own error is the size of the lever, because forty years
    of monthly data pin a near-unit-root persistence too loosely. By abstraction it is also composition weights that
    moved (task95, task446).
  - **Measured: new collective agreements' annualised increase once a long pre-surge wave expires** (the catch-up of
    real pay lost since each agreement's own last settlement; `w1.py`, `w2.py`, seeds 1 to 5, about 13,600
    agreements over 2000 to 2027). On the 2027 approvals the trailing-inflation regression lands within 0.15 to 0.50
    points (2.50 against truths of 2.64 to 3.00, 5 to 17 per cent); the symmetric catch-up regression misses as
    badly (2.20 to 2.57) and only an asymmetric catch-up lands (2.61 to 2.95), so the decisive step became the
    asymmetry, a 0.4-point split inside the golden family against the lever. Catch-up since the last settlement is
    also the first thing a labour economist checks after a surge, a cousin of task165's gain conditioned on each
    unit's own baseline, and the settlement regression is panel estimation rather than this task type.
  - Paper: invoicing-currency (dominant-currency) pass-through into import prices is task145's driver (units differ
    in which currency they hold fixed), and task153 rejected its pass-through cousins.
  - Paper: asymmetric error correction in a retail price (rockets and feathers) is the adjustment-speed cousin
    task153 rejected.
  - Paper: phase-asymmetric unemployment (steep rises, recoveries at a steady log pace) against a linear AR: a gap
    closing at a fixed pace rather than in proportion is task161's driver (own-use burn against a half-life), its
    honest strategy `forecast_method_backtest` (a regime) is in the window (task177), and the pace of past
    recoveries, the natural analogue, is the golden.
  - Paper: a rent index under a cap on sitting-tenant increases with vacancy decontrol (a backlog drawn down at the
    cap, a nonlinear error correction): fixed-rate drawdown is task161's driver and the saturation task79's, and once
    the cap is filed the sitting tenancies' path executes it.
  - Paper: a convex price response to capacity utilisation read from an industry panel is task79's kink (task149
    rejected the same).
  - Paper: mortgage-rate lock-in holding down housing transactions and transfer-tax receipts is task166's driver
    (units whose own rate the terms beat).
  - Paper: a moving lunar holiday (Ramadan and Eid) in a monthly flow or in banknote demand is task162's
    calendar-locked alignment, and a strong reader models it.
  - Paper: a reset-month step in a price index sized by trailing inflation (state-dependent seasonality from annual
    indexation), and year-end appropriation spending sized by the unspent balance: both task146's driver (a step at a
    calendar turn is not a fixed seasonal share).
  - Paper: downward nominal wage rigidity bending aggregate wage growth: at plausible desired growth for 2027 (1 to 3
    per cent, a worker sd of 3) the floor moves aggregate growth 0.09 points from a linear extrapolation, and
    aggregation over a per-unit floor is task16's driver.
  - Paper: cointegration and error correction against a VAR in differences or ARIMA, including the partner that
    reveals a shock's permanence and a trend in the cointegrating relation: the cell's own cards 1 and 2 applied as
    stated, which the library test says a blind reader lands; where the golden is no reversion, ARIMA lands it; and
    `coint` applies MacKinnon's critical values by default.
  - Paper: signal extraction from a sampled series: IMA(1,1) is the optimal filter for a random walk plus noise and
    lands, and autocorrelated sampling error needs the filed design variance (rule application).
  - Paper: a minimum wage's effect through its bite is task165's untreated part; the shadow rate at the lower bound
    is markets and lending ground, with a rule fitted on off-floor quarters both the default and the golden; an
    uncertainty hold on a trend-growth revision (HAC against iid) fails the variance-only screen; inventory payback,
    the accelerator and the carry-over are accounting a strong reader states; tariff diversion to untariffed origins
    is a product-panel elasticity outside this task type and close to task88's displacement.
  - The cell finding: the field's textbook routes (ARIMA, VAR, VECM, bridge, X-13) are routes a blind reader takes,
    and every structural judgment beyond them that this search found is either a driver on file by abstraction
    (fixed-pace drawdown, a kink, a calendar turn's step, a conditioned gain, a moved mix, a lock-in, pass-through)
    or, where it is new, carries a golden whose own sigma (12 per cent, 18 per cent of the figure) or family split
    is the size of its lever, because macro aggregates rest on too few independent events. Micro registers give the
    precision and move the work out of this task type.

- **Rebuild screen, 2026-10-23: product-analytics / `feature-adoption-diffusion-modeling`, Forecasting** (the number
  reopened under the author's rule; worktree `b_179n`). The cell's three library cards (novelty against durable use,
  the eligible denominator in a staged rollout, censored non-adopters) and the field's textbook routes (a Bass curve
  fitted to the adoption series, analogue launches, a logistic on account features) were taken as the default path;
  task144's spotlight cascade through follower feeds and task162's calendar-locked restart burst were read as spent.
  `guard.py recent` at a544497 put task173, task178 and task482 in the window. Three candidates measured on code
  (scratchpad b179n/screen: `a1.py`, `a2.py`, `b1.py`, `c1.py`; `screen179n.out` byte-identical with
  `screen179n_run2.out`; seeds fixed before outcomes) and sixteen on the structural screens; no card was drafted.
  - **Measured: contagion local to each customer account against the Bass curve's global mixing** (each non-adopter's
    weekly hazard p plus q times the adopted share of the user's own account; 3,000 accounts, lognormal sizes median 6,
    the feature live 39 weeks). Over a 13-week window the recent pace lands (+1.4 and +4.5 per cent on two seeds)
    because account ignitions are a steady flow. Over 52 weeks the nearest textbook route is the Bass curve with the
    whole base as its potential (-14.6 to -15.5 per cent), the recent pace +20.5 to +26.4 and the pooled hazard -31 to
    -33, while the golden family splits: the account-share hazard by likelihood lands the truth, the count form is
    rejected by about 5,000 log-likelihood units, but a two-stage account construction (ignition by size band, the
    completion curve by weeks since ignition, held flat past the 39 observed weeks) files -51 to -53 per cent. Lever
    about 15 per cent against a family that forks on the extrapolation: dead.
  - **Measured: adoption on the session clock (a constant chance per session, heterogeneous session rates)** (30,000
    users, lognormal rates sd 1.2, 52-week window). The per-session golden lands within 1 per cent (plug-in and
    gamma-Poisson empirical Bayes agree), but the eligible-denominator card's own route (the hazard per active
    non-adopter week times each non-adopter's active-week share) files +10.5 to +13.1 per cent and the pooled hazard
    with a log-linear decay -7.5 to -15.6 (-0.1 at a tighter spread): the card is the golden to a tenth and a half,
    and the golden is one divide and one group-by. Dead.
  - **Measured: substitution inside the account (one adopter serves the team, teammates' hazard falling to a tenth
    after the first adoption)** (4,000 accounts, median 8, 52-week window). The recent pace and the pooled hazard miss
    by +31 to +60 per cent, but the pooled hazard's decay extrapolation lands in some seeds (-3.9, -5.4) and swings to
    +90 in others, and the decisive fact is on the surface (two in three accounts adopted with about 1.2 adopters each),
    so the golden is one group-by of ignitions per account-week by size band. Dead.
  - Paper: a staged rollout's last wave or a long-term holdout released in the window is the eligible-denominator card
    applied to a filed date, the first wave's early weeks the attaining subset.
  - Paper: a growing in-app prompt read by the Bass curve as imitation (marketing effort against contagion): bucketed
    prompts are the eligibility card, session-level prompts one divide per impression, and the recent pace lands once
    the prompt is at its full share.
  - Paper: a past device or plan purchase surge ageing into replacement in the window, and self-hosted instances
    synchronised by a security upgrade wave: task46's cohort crossing a step and task162's burst by abstraction.
  - Paper: adoption at each account's renewal, quarterly business review or payroll run: task177 v2's days to the next
    bill by abstraction.
  - Paper: a need pool (the users who can use the feature) pinned by a finer file: the class with zero adoption is the
    attaining subset, one group-by.
  - Paper: cross-market lead-lag spillover between staggered country launches: a handful of markets carry the
    spillover coefficient, and the latest launch is the attaining analogue.
  - Paper: a second generation substituting for the first (Norton-Bass): the first generation's base is a group-by.
  - Paper: influence from current rather than cumulative users after disadoption: the definition of current is a free
    window, and the recent pace lands once current users plateau.
  - Paper: hard-deleted churned accounts inflating the analogue curves: a retention policy read (semantics) or a
    reconciliation (Layer 1).
  - Paper: churn as a competing exit against Kaplan-Meier: the textbook competing-risks correction.
  - Paper: later adopters' lighter durable use for a usage-volume forecast: the cohort chain ladder carries each
    cohort's level, and future cohorts' level is an extrapolation that forks.
  - Paper: late-arriving telemetry from offline devices: the right-truncation reflex this number already spent.
  - Paper: two-sided adoption through a counterparty graph, and contagion through feature-made artifacts: task144's
    per-view rate through a graph by abstraction.
  - Paper: a waitlist throttling admissions: task168's capacity-censored demand.
  - Paper: beta testers' adoption transported to general availability: selection on observables is the logistic
    route, on unobservables unidentified.
  - Paper: interference in a user-randomised test of a collaborative feature, the full rollout at a team-treated share
    of one: the network-interference card, small fully treated teams the attaining subset, and task177 v2's exposure
    end by abstraction.
  - The cell finding: an adoption forecast from a user or account event log is landed by one of three reflexes
    whenever the process is stationary over the window (the recent pace on a short window, the eligible-denominator
    hazard or a depletion-aware curve on a long one), so a lever of 30 to 50 per cent needs the window to change the
    process; every predictable change this search found is a filed date (rollout, holdout, sunset, price), a cohort or
    calendar alignment already on file (task46, task162, task177 v2), a cap or a pipeline in flight (task172, task77),
    or a network cascade (task144). Where the structure is new (local contagion, substitution in the team), the
    golden is either a group-by visible on the surface or an extrapolation past the observed weeks on which the
    golden family forks.

- **Second rebuild cell, 2026-10-23, chosen by this build: pharmacology-pharmacoepidemiology-safety /
  `population-pharmacokinetics-exposure-response`, Forecasting** (no card on file in the task type; the domain is
  outside the guard window of task178, task482 and task274). Why its window changes the process: a monoclonal
  antibody's move from 300 mg every three weeks to 600 mg every six puts each patient's trough twice as far from the
  dose, into the low concentrations where target-mediated elimination bends the decline and which the three-weekly
  record reaches only during treatment holds; no patient in the record has run the six-weekly schedule, so it cannot
  be replayed. The cell's four library cards (covariates inside the mixed model, allometric centring, exposure-response
  confounded by clearance, below-quantification samples as censored) and the field's textbook route (a population
  model fitted to the monitoring levels, each patient's own levels read by maximum a posteriori, the new schedule
  simulated) were taken as the default path. One candidate measured on code (scratchpad b179n/screen2: `pk1.py`,
  `pk1fit.py`; `pk_screen.out` byte-identical with `pk_screen_run2.out`) and eleven on paper; nothing holds.
  - **Measured: target-mediated (Michaelis-Menten) elimination against the linear one-compartment model** (600
    patients, clearance CV 35 per cent, troughs before half the infusions, a tenth of infusions with a peak, 5 to 15 per
    cent of patients with a hold of 5 to 12 weeks sampled one to three times; graded figure the share of patients whose
    six-weekly steady-state trough falls under 8 mg/L). With Km 2 mg/L the truth is 21.7 and 21.5 per cent on two
    seeds; carrying the linear clearance alone would file 11.5 and 12.3, but the textbook per-patient linear fit files
    21.2 and 21.0 (19.0 and 19.3 with the hold samples dropped), because each patient's own levels absorb the bend at
    that patient's concentrations. With Km 6 mg/L and holds in 5 per cent of patients the truth is 33.5 and the linear
    fit 28.8 (a lever of 14 per cent of the figure), and where the bend is strong enough for a 30 per cent lever the
    hold samples show it on a log plot. Dead: the field's own precision-dosing route reads each unit at its own level,
    and the only records of the forward region are the holds, an attaining subset.
  - Paper: two-compartment kinetics against one compartment for the longer interval: the standard structural choice for
    an antibody, tested by any population modeller, and three-weekly troughs already sit in the terminal phase.
  - Paper: each patient's half-life from the loading-phase accumulation (first trough over steady trough): an identity
    per patient, and the per-patient fit takes it anyway.
  - Paper: time-varying clearance falling with time on treatment: each patient's latest levels carry it.
  - Paper: anti-drug antibodies induced by lower troughs feeding faster clearance: the response is identified only by
    the patients already at low troughs (an attaining subset), with reverse causation as an open fork.
  - Paper: exposure-response confounded by clearance carried to the higher-exposure regimen: the cell's own card 3.
  - Paper, dose-response-pk-pd-modeling: the same per-patient absorption, and the cell's cards (relative ED50, AUC to
    infinity, hysteresis) are the textbook.
  - Paper, election-polling-forecasting (the other untouched Forecasting cell): a move from plurality to instant
    runoff (the upper house's ballot-level preferences are the obvious and only flow data), an election moved
    on-cycle (the national electorate in the voter file is the attaining subset), compulsory voting (the
    registered-voter sample is the cell's card 3), a party's withdrawal (districts it never contested are the
    attaining subset), a lowered voting age or a new party (unidentified).
  - Paper, banking deposit-liquidity-behaviour and credit-scoring-pd-modeling: a lower deposit-guarantee limit (the
    balances already above the old limit), branch closures (earlier closures), a payroll client leaving (customers
    who lost a salary credit), reject inference for a widened approval policy (rejects' bureau performance elsewhere),
    a payment holiday ending (pre-holiday performance), forbearance withdrawn (task169's removed route by
    abstraction).
  - The cell finding: in exposure modelling the field's own forecast already conditions on each patient's levels, so a
    forward schedule that stays near the record's concentrations is landed by the per-patient fit, and one that moves
    far from them is informed only by the minority of records already there (holds, delays), which a filter reads.

## Retired

Retired on 2026-10-21 under the author's rule for this round (a number that dies in its second new cell is
retired). Three worlds were worked. The first cell, the seed's own world (a private ambulance contractor's summer
surge pool), died at stage 1 on code: the golden's own sigma was wider than a whole-unit bin under every pooling and
level lever. The redraw cell in Economics & Econometrics (time-series macro-econometrics) died on code and paper
before any card: every structural judgment beyond the textbook routes was a driver on file or carried a golden whose
own error matched its lever. The second new cell, Epidemiology & Public Health
(infectious-disease-transmission-modeling), carried architecture v2: the serial interval read from transmission
links that exist only once the later case has fallen ill, right truncated at the extract while the outbreak grows.
Its first world, a named real disease in a named real province, was declined on the real-place records concern; it
was re-sited into a fictional setting (the Republic of Orvanthe, Dunmarrow Province, Tamberlow virus disease),
built to stage 3 green (44 checks, the independent verifier, two byte-identical builds, precut.py exit 0, pair
ceiling 28.5) and spent at Gate F when scored reader B landed the call and both components.

The lesson: a correction the field teaches as standard is the default path, not the stump. Right truncation of a
delay read from linked records is the textbook caution of outbreak analytics (nowcasting, serial and generation
interval estimation), so a strong reader applies it on the first pass; the screen that measured the uncorrected
fit as the competent route measured a route this field's analysts do not take. A delay-truncation stump needs a
setting where the truncation is not the field's own named hazard, or a judgment beyond the correction.

The card stays filed with `architecture_spent` set. The two ask devices held (the reader kept 0 of 16) and are kept
here as reusable records:

- **Device record, the paper register's handover join.** During a handover between two field teams, the outgoing
  team's paper listings were keyed at the district office beside the incoming team's tablet listings of the same
  people, the paper form carrying an estimated age one to three years off and the listing closed as lost when the
  visits stopped. The exact person key counts those people twice and drags completion down; only source case,
  household, initials and sex, listed within a day, with the age inside the paper form's estimate, tie them. The
  filed definition (the follow-up that ends last, completed by either team) keeps the completion share determinate.
  Measured: the exact key, the key without age, the listing id and per-listing completion each missed every
  district's count and percentage.
- **Device record, the UTC result clock inferred from an internal inconsistency.** A laboratory analyser writes its
  result time on UTC while collection and reception are keyed on local time (UTC+1); nothing labels the clock. The
  evidence sits in the data: about 2.6 per cent of results land less than the dictionary's 92-minute cartridge run
  after reception, and positives fall on the day before the line list's result date, both vanishing once an hour is
  added. Measured: the clock read as local missed every week's mean and within-24-hour share; the re-run after an
  indeterminate result is the hazard beside it.

## Rebuild (2026-10-23)

Reopened under the author's rule that no number stays retired, for a from-scratch rebuild in product-analytics /
feature-adoption-diffusion-modeling (Forecasting), worktree `b_179n`. No candidate held at stage 1: three measured dead on
code (local contagion, the session clock, substitution inside the account) and sixteen directions dead on paper, all in
`## Tried and rejected` with the cell finding. No card registered, so architecture v2 stays the card's current identity
and nothing moved into `lineage`; nothing cut. PAUSED at stage 1 for the coordinator to assign another cell.

The coordinator then left the next cell to this build's choice: pharmacology-pharmacoepidemiology-safety /
population-pharmacokinetics-exposure-response (Forecasting). One candidate measured dead on code (target-mediated
elimination under a six-weekly schedule) and eleven directions on paper, with the election-polling and banking cells
screened on paper beside it (`## Tried and rejected`). No card registered; PAUSED at stage 1 again.

## Resume

PAUSED 2026-10-23 at stage 1 after the product-analytics / feature-adoption-diffusion-modeling and the
population-pharmacokinetics-exposure-response rebuild screens found no draw that holds; resume at stage 1 in the next cell the coordinator assigns, reading `## Tried and rejected` first.
(RETIRED 2026-10-21 before the reopening: architecture v2 spent at stage 4 Gate F.)
