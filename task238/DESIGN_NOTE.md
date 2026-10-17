# task238 design note

Architecture 1, wave 3, seed DQ11 (whether a new survey mode's data can be pooled into the tracker): the seed's world
and quantity only, the pitfall re-found from the data under the 10/10 rules. Survey Research & Official Statistics,
nonresponse, calibration and measurement-error adjustment, Data Quality Monitoring & Alerting. The Halvreth Statistics
Office runs the Halvreth Wellbeing Tracker, a quarterly household survey of one adult per sampled address, collected
telephone-first since 2019 (an advance letter, interviewer calls, a web link in the reminder for households the calls
do not reach). From the fourth quarter of 2027 every sampled address gets a web-first letter instead (complete online,
telephone follow-up for households that have not). Before choosing, the office ran a contact strategy test through
the second and third quarters of 2027: each quarter's issued addresses were allocated at random to the web-first
letter (A) or the telephone-first letter (B), to compare response and cost per complete under the two designs. Once
the tracker is web-first, each quarter's indexes pool online and telephone completes, and an index whose answers
differ by mode moves whenever the quarter's share of completes made online moves. The office's continuity standard
for the web-first tracker sets a mode-mix monitor: when a quarter's web share departs from the reference share by
more than the monitor's band, that quarter's indexes are recalibrated to the reference mix before release. The band
is the widest whole-point departure that moves no headline index by more than its continuity tolerance. The head of
survey methodology sets it before the fourth-quarter estimates are processed.

## Draw

Card `cards/task238.json` (architecture 1, registered 2026-10-17). Guard verdict WARN: overuse.objective (the
objective in 4 of the last 12 builds) is this lane's own objective, the backlog wave being Data Quality Monitoring &
Alerting by assignment.

- **Pairing.** Survey Research & Official Statistics / nonresponse-calibration-measurement-error-adjustment, serving
  Data Quality Monitoring & Alerting. Not banned against the last three builds (task237, task155, task464). The object
  is the health of the tracker's published series through a change of collection mode (whether a quarter's mode mix
  has moved its indexes), the call a monitoring setting.
- **Niche.** Mode effects in a mixed-mode household survey: an interviewer's presence moves self-reports (heavy
  drinking and loneliness reported less, volunteering and life satisfaction more), and who completes online is
  self-selected on traits the same questions measure, some of which no field records.
- **The call.** The band, in whole percentage points of the web share, at which the mode-mix monitor runs from the
  fourth quarter of 2027.
- **Shape.** 04, setting one dial: the allowed settings are the whole-point bands, and each headline index's mode
  effect and widest band within tolerance stand behind the setting. Decision dial_setting, answer rate_or_share,
  question form what.
- **Strategy.** causal_design with G14 decisive (the telephone completes' level is not what the web completes would
  have answered by telephone), G16 (the estimator the random letter allocation entitles) and G6 (the two answerer
  groups' mix) supporting; Gate G decomposition_attribution (the web-telephone difference split into the mode's
  measurement effect and who chose the web); calibration none; context artifact close_out_summary (the test's
  close-out); layer 2 family estimand_identification, pattern own:mode-effect-through-a-randomized-contact-strategy.
- **Forum, event, organisation.** line_manager_or_team (the head of survey methodology sets the band under MS-14
  section 5, no formal forum), cutover_or_migration (the tracker's move to web-first collection),
  research_or_statistics_office. Guard WARN repeat.gate_g (decomposition_attribution against task266, a demography
  build): the mechanism there splits a life-course quantity, here a web-telephone difference into the mode's
  measurement and who chose the web; nothing else repeats.
- **People** (`guard.py names --geo en_NZ --seed 238`): Tania Nicholas, head of survey methodology, who sets the band;
  Bernard Johnstone, the tracker's fieldwork manager, who wrote the test's close-out; Leonard McMurray, data
  processing lead, who keeps the exports.
- **Deliverables.** `mwt_mode_mix_band_2027q4.xlsx` (the band, each index's mode effect and widest band within
  tolerance, and the asks' figures) and `mwt_mode_mix_band_2027q4.png` (each index's widest band against the band
  set).
- **As-of.** 2027-10-20: the test's fieldwork closed 30 September 2027, the close-out is dated 15 October 2027, the
  fourth-quarter fieldwork is under way and its estimates are processed in January 2028.
- **Data-native sentence.** Households choose their mode (under letter A they complete online if they get round to
  it before the follow-up calls, under letter B online only if the calls never reach them), and the households that
  end up online are younger and more often away from home, which is also what moves their answers on drinking,
  loneliness and volunteering; the one contrast in this dataset that no choice shapes is the one between the two
  letters, allocated at random by address, and it moved the web share by only about sixty points.

Sources, one line each (what it teaches; how this build differs):
- Survey methodology on mixed-mode designs (selection effects against measurement effects; the interviewer's presence
  and social desirability; recalibrating to a fixed mode mix to keep a series comparable): the field's frame for the
  quantity and the monitor; here the effect must be read through a contact strategy test run for response and cost,
  not a mode experiment built for it.
- Causal inference on encouragement designs (the Wald estimator, two-stage least squares with the assignment as the
  instrument): the method the design entitles; here it is never named in the pack, and the respondent comparison
  adjusted for every recorded characteristic is the reflex it has to beat.
- Seed DQ11: the world (a tracker adding a mode) and the quantity (each index's mode effect) only; its pitfall
  (ordinal items and polychoric invariance testing) belongs to psychometrics, which task237 holds.
- Spent on this objective (`guard.py mechanisms`): task229 (a convex conversion of a daily mean), task231 (a rate over
  active units with late exits), task232 (transmission from delayed mixed outcomes), task230 (a late channel's net
  classification bias), task228 (variance at the randomised unit), task233 (a missing-not-at-random departure on the
  logit scale), task234 (a source's output from a share a loss cannot move), task235 (a missing event censored until
  its device's next contact), task236 (a capture share against an independent fixed-protocol sample), task237 (the
  trait's share of a score with a wording factor). None reads a channel's effect through a randomized nudge's shift
  in uptake.

## Default path

1. Read the continuity standard: each headline index's mode effect (the difference answering online rather than by
   telephone makes to a household's answers), the mode-mix artefact of a departure (the departure times the mode
   effect), each index's tolerance and the band's rule (the widest whole-point departure keeping every index within
   tolerance).
2. Build the test's completes from the interview export under the test plan's rules (one complete per address,
   partials and late returns out) and score the twelve indexes as the codebook defines them.
3. Estimate each index's mode effect by comparing web with telephone completes, adjusted for age, sex, education,
   region, household size, tenure and employment (a regression with a web indicator).
4. Divide each index's tolerance by its mode effect, take the smallest widest band and round it down to whole points.

Ends on: 3 points (safe after dark binding at 3.42, its comparison carrying who chose the web; heavy drinking 3.67 next).

Golden: 4 points (heavy drinking binding at 4.53 points of web share, from each index's difference between the letters
divided by the letters' difference in the share of completes made online; two-stage least squares 4.62).

## Stump sentence

A competent analyst estimates each index's mode effect by comparing web with telephone completes adjusted for every
recorded characteristic and sets the monitor at 3 points (Ends on: 3 points, safe after dark binding); the step that
lands it there is reading the mode effect off households that chose their mode, when the randomly allocated letters
give a contrast that, divided by the letters' difference in web uptake, sets the band at 4.

## Three rules

- **Task type:** survey-research-official-statistics / nonresponse-calibration-measurement-error-adjustment, which
  serves Data Quality Monitoring & Alerting; the object is whether a quarter's mode mix has moved the tracker's
  published indexes, and the call is the monitor's setting.
- **Domain test:** the quantity that decides is each headline index's mode effect, the measurement difference
  between answering online and by telephone for the same households, which survey methodology separates from the
  selection effect of who answers online; here the field reads it from the randomized contact strategy contrast
  through the shift it causes in web uptake.
- **Swap:** with ward admissions or megawatt-hours for answers there is no interviewer whose presence moves a
  self-report, no household choosing its mode, no contact letter allocated at random to read the effect through and
  no mode mix to monitor on a published series; the call stops making sense.
- **Layer 1:** an issued-sample file at address grain and an interview export at record grain, joined by address;
  telephone interviews stamped in local time by the CATI system against web submissions stamped in UTC by the survey
  platform; web submissions after a quarter's fieldwork close kept in the export; households interviewed by telephone
  after they had already submitted online, or the reverse; web break-offs with answers to the early items only; item
  nonresponse codes that differ by mode. Each is how the system that writes it behaves; none is placed to be caught.
- **Layer 2:** estimand_identification: the mode effect identified from the random letter allocation (an
  encouragement design) rather than from the self-selected mode groups, however adjusted.
- **Decisive step:** dividing each index's difference between the two letters' completes by the letters' difference
  in the share of completes made online (the Wald estimator, or two-stage least squares with the letter as the
  instrument), rather than comparing web with telephone completes or taking the letters' difference as the effect.
- **Not semantics:** reading every field, code, timestamp and definition right (completes built under the plan's
  rules, the indexes scored per the codebook, the standard's definition of the mode effect read as written) still
  leaves the analyst comparing web with telephone completes, and that comparison, computed correctly and adjusted for
  every recorded characteristic, files 3 points.
- **Not rule application:** the standard files what the mode effect is, the artefact, the tolerances and the band's
  rule; no rule names an estimator or a comparison group, and executing every stated rule still leaves the
  estimation, where the adjusted comparison files 3 points and the letters' difference 6.
- **Analyst test:** a strong analyst who builds the test's completes under the plan's rules, scores each index as the
  codebook defines it, reads the continuity standard correctly and estimates each mode effect from web against
  telephone completes adjusted for every recorded characteristic files a band of 3 points (Ends on: 3 points, safe
  after dark binding); one who takes the two letters' difference as the mode effect files 6.
- **Estimand:** the continuity standard MS-14 (`mso_ms14_tracker_continuity_standard.pdf`) fixes the population (the contact
  strategy test's completes, both quarters and both letters), the outcome (each headline index as the codebook scores
  it), the window (the second and third quarters of 2027), the unit (index points; the band in whole percentage points
  of the web share) and the comparison (the same households answering online rather than by telephone).
- **No decoy:** nothing is planted: the close-out summary reports fieldwork, response and cost by letter and never a
  mode effect or a band; no memo, draft or briefing argues a band; the published series are the tracker's own
  releases.
- **No certified replay:** no certified or published mode effect or band exists for a method to reproduce.
- **Lesson:** when respondents choose the mode, a contact strategy allocated at random for another purpose is the
  lever: the mode effect is the arms' difference over the arms' difference in uptake, not the comparison of the
  modes' respondents however adjusted, and not the arms' raw difference; no build on file reads an effect through a
  randomized nudge's shift in uptake (task236 reads capture against an independent sentinel sample, task228 the
  variance at the randomised unit).

## Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control
or corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or
half of a reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0a web completes against telephone completes, as they stand: 2 (heavy drinking 2.57) | MS-14's "mode effect" read as the difference between the modes | the mode is a property of every complete | yes, the first comparison anyone runs | none | no | one subtraction per index | readable |
| 0 (default) the same comparison with every recorded characteristic held fixed (a regression with a web indicator): 3 (safe after dark 3.42) | MS-14's definition, the same households online and by telephone, invites holding them alike | age, sex, qualification, employment, tenure, household size and region ship on every complete | yes: adds the controls, reweights | none | no | one regression per index | readable |
| 1 letter A's online completes against letter B's telephone completes: 3 (heavy drinking 3.11) | the plan's two strategies, web-first and telephone-first | the letter joins from the issued sample | partly: a design-minded analyst compares the strategies' typical modes | none | no | one subtraction per index | readable |
| 2 the letters' raw difference (each index under letter A less under letter B): 6 (heavy drinking 6.82) | the plan's random allocation sends a design-minded analyst to the arms | the letter column | yes for an experimenter: compare the randomised arms | none | no | one subtraction per index | readable |
| 3 (decisive) each index's difference between the letters divided by the letters' difference in the share of completes made online (the Wald estimator; two-stage least squares with the letter as the instrument) | no sentence names an estimator, an instrument or uptake; MS-14 files the quantity (every household online against every household by telephone) and the plan files why the letters exist (response and cost) | no column holds a mode effect, an uptake or a band; the mode and the letter are separate facts in separate files | no: the reflexes hold covariates fixed or compare the arms; scaling a contrast by the shift it caused in the mode is neither | no control scores an estimator; the close-out gives uptake only in rounded words | no | not linear: two differences per index from record-level files, then a ratio, then the tolerances | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | mode effect | the index with every household in the measured population answering online, against every one of them by telephone | the difference between the web and the telephone completes | 2 | MS-14 s.3 ("every household in the population it is measured on answered online ... every one of those households answered by telephone") |
| SF2 | web share | the percentage of a quarter's completes made online | the share of issued addresses answering online (uptake per address) | 2 | MS-14 s.3 ("the percentage of a quarter's completes made online"); the effect's population is the completes |
| SF3 | the band | the widest whole-point band within every tolerance | the nearest whole point (5) | 5 breaches heavy drinking's tolerance | MS-14 s.5 ("the widest whole-point band at which ... stays within"); asserted |
| SF4 | the mode effect the band uses | the central estimate | a confidence bound | another band | MS-14 s.5 ("taken at the central estimate of its mode effect") |
| SF5 | the population the effects are measured on | the test's completes, both quarters and both letters | one quarter alone | same call (each quarter alone 4: 4.68 and 4.40) | MS-14 s.5 ("both quarters and under both letters"); same call (asserted) |
| SF6 | a complete | CST-27 s.5: section 6 reached by the close, coded C, an address once at its first-submitted complete, an address's highest result | late returns, partials, both records, the sample system's codes | same call (R2) | CST-27 s.5; same call (asserted) |
| SF7 | each index's score | codebook v9, sheet Indexes | none filed | same call | codebook (asserted) |
| SF8 | an index's base | answers on the scale | don't know, refused and prefer not to say kept in the base | same call | codebook Indexes note; same call (asserted) |
| SF9 | tolerance units | points on the 0 to 10 scores, percentage points on the percentages | none | same call | MS-14 Table 2 |
| SF10 | the artefact | d/100 times the mode effect, d in points of web share | d times the mode effect | a band a hundredth the size | MS-14 s.3 ("d/100 times the index's mode effect") |
| SF11 | controls in the estimator | none (the Wald estimator) | the recorded characteristics (two-stage least squares) | same call (4.53 and 4.62) | same call (asserted) |
| SF12 | the reference share | the fourth quarter's web share | the test's letter A share | the band does not use it | MS-14 s.3, s.5 |
| SF13 | the 9 to 12 August staff-entry returns | telephone interviews | web returns | same call | close-out; same call (asserted) |
| SF14 | a return giving an age under 18 | not the selected adult's: not a complete | a complete | same call | CST-27 s.3 ("aged 18 or over"); same call (asserted) |
| SF15 | the 345 addresses answering twice | one complete each, the first submitted | a within-household comparison of their two answers | 2 | CST-27 s.5 ("An address counts once"); MS-14 s.5 measures the effects on the test's completes, not on 345 households answering a second time |

## Ladder

Four rungs and a floor, each a defensible way to read a mode effect, each dying to one fact of the data (figures on
the cut pack, asserted in `checks.py`; the binding index and its widest band in points of web share).

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0a | web against telephone completes, as they stand | 2 (heavy drinking 2.57; its effect 11.66 points) | the web completes are younger, more educated and more often employed: the recorded characteristics alone move every index |
| 0 (default) | the same with every recorded characteristic held fixed | 3 (safe after dark 3.42, effect 8.77; heavy drinking 3.67 next) | the letters moved web uptake by 66.3 points and moved safe after dark by -0.53: no index can carry a mode effect of 8.77 points and shift half a point the other way when two thirds of households change mode; the comparison carries who chose the web |
| 1 | letter A's online completes against letter B's telephone completes | 3 (heavy drinking 3.11) | the same: each arm's typical mode is still chosen within the arm |
| 2 | the letters' raw difference | 6 (heavy drinking 6.82; its difference 4.40) | the letters changed the mode for 66.3 per cent of completes, not all: the difference carries each effect only for the households a letter moved |
| 3 (golden) | each difference between the letters over the letters' difference in the share made online | 4 (heavy drinking 4.53, effect 6.62; volunteering 6.83 next); two-stage least squares 4 (4.62, 6.49) | |

- **Margins.** Heavy drinking's widest band sits 0.53 inside 4 to 5 under the Wald estimator and 0.38 under two-stage
  least squares; under every Layer 1 mishandling it stays between 4.40 and 4.83 (R2). The rivals sit inside their own
  bins: the adjusted comparison's 3.42, the letters' raw difference 6.82, the raw comparison 2.57.
- **Position and dominance.** Every easy route files 2, 3 or 6; only reading the effect through the letters lands 4,
  and the decisive step alone (the letters' contrast scaled by uptake, nothing else changed) moves the default path
  there on the clean truth (R3b). The generating model's own effects set 4 on heavy drinking.
- **Grid.** The corrections walk 2, 3, 6; only the decisive step reverses (6 to 4), so the golden is bracketed.
- **Worth.** Counted on the band, the one graded call; the binding index changes with the rung (safe after dark on the
  default path), so the default path misses the binding index too.

## Closure table

| # | Axis | Reading in this build | Closure |
|---|---|---|---|
| 1 | Population | the CST-27 completes, both quarters, both letters | MS-14 s.5; CST-27 s.5 (SF5, SF6) |
| 2 | Unit of account | the selected adult's answers; each index in its own units | codebook; MS-14 s.3 |
| 3 | Attribution window | the second and third quarters of 2027, to each quarter's close | CST-27 s.4 |
| 4 | As-of dating | exports of 11 October 2027; the band set before the fourth quarter is processed | dictionary; README; MS-14 s.5 |
| 5 | Version basis | MS-14 issued 8 October 2027; codebook version 9; the plan of 8 March 2027 | headers |
| 6 | Denominator | each index's valid answers; response rates over eligible addresses | codebook; CST-27 s.5 |
| 7 | Weighting | none: no weight ships with the test | data |
| 8 | Window length | two quarters | MS-14 s.5 |
| 9 | Boundary inclusivity | within tolerance means no more than it; the band the widest whole point within | MS-14 s.5 (SF3) |
| 10 | Rounding path | the band from unrounded effects; response rates rounded to one decimal once | MS-14 s.5; prompt |
| 11 | Tie-break | none: the narrowest widest band binds, no tie | asserted |
| 12 | Maturity and censoring | returns after a close do not count; both quarters closed | CST-27 s.5 |
| 13 | Order of operations | completes, letters, scores, effects, widest bands, band | MS-14 s.3, s.5 |
| 14 | Row order | irrelevant | C1 |
| 15 | Duplicate resolution | an address once, its first-submitted complete in Halvreth time | CST-27 s.5 (SF15) |
| 16 | Identity normalisation | web returns to addresses by login code, interviews by address | dictionary |
| 17 | Netting against gross | none | data |
| 18 | Dimensional units | index points; web share and band in percentage points | MS-14 s.3 (SF9, SF10) |
| 19 | Code and status semantics | valid answers per codebook; RESULT C; section 6; outcome codes 4.1 to 4.3 out of eligible | codebook; dictionary (SF8) |
| 20 | Integerisation | the band a whole number of points | MS-14 s.5 |
| 21 | Clause scope | the twelve headline indexes | MS-14 s.2 |
| 22 | Forward window contents | the band governs every release from the fourth quarter of 2027 | MS-14 s.4, s.5 |

## Literal reader

Executed word for word, MS-14 and the prompt fix the candidates (whole-point bands), the population (the CST-27
completes from both quarters and both letters, built under the plan's section 5), the outcome (each headline index as
the codebook scores it), the quantity (each index's mode effect: every one of those households online against every
one by telephone, at its central estimate), the artefact (d/100 times the effect) and the rule (the widest whole-point
band keeping every index within its tolerance). Executed, MS-14 leaves one question to the analysis: how large each
index's mode effect is, which no file states and no household shows, since each answered one way. A comparison of the
web with the telephone completes, however adjusted, answers it with households that chose their mode; the letters
were allocated at random and moved two thirds of completes from telephone to web, so each index's difference between
the letters over that shift is the effect. Every estimator of it (Wald, two-stage least squares, either quarter alone)
sets 4; every reading in the fork table gives 4 or breaks a quoted sentence. The asks execute the plan's section 5
and the codebook; their difficulty is how each system's records come to exist, not the words.

## Oracles

- No control, published figure or certified mode effect ships: nothing states a mode effect, an uptake by index, a
  band or a decision, and no field marks a household's reason for its mode.
- The close-out gives uptake in rounded words (about six in seven online under letter A, one in five under letter B)
  and response in words (much the same); both tie under every handling of every device.
- The published series (a distractor, named in `metadata.json`) is the telephone-first design throughout, its web
  share drifting between 7 and 20 per cent: a regression of an index on that drift is confounded with time and too
  thin to measure an effect, and it ties with no rung.
- The CATI call records (a distractor) carry contact attempts, not answers; their outage gap corroborates the
  close-out and scores nothing.
- The 345 addresses answering twice give a within-household comparison (SF15): 2, ruled out by the plan's one
  complete per address and MS-14's population.

## Ask sheet

Two asks, 28 figures, decoupled from the call: the call reads the letters' contrasts on the completes; the asks read
the issued addresses' outcomes and each index's valid answers by mode, through how each system's records come to
exist.

**Main population:** the call's population is the test's completes; every ask device either sits outside it (late
returns, under-18 returns, the addresses the field team locked, partials, second records) or moves a complete's mode
without moving the band (the outage interviews, the clock on twice-answered addresses). Each stop's handling leaves
the band at 4 with heavy drinking binding (R2): the call is mess-neutral, never pristine.

| Ask | Figures | H18 home | Use | Primary device (family) | Hazards | Path (files, columns) | Stops |
|---|---|---|---|---|---|---|---|
| A: the test's response rate under each letter in each quarter | 4 | the audit trail of the population the call reads: the completes against the addresses issued | MS-14 s.6 files the test's response with the band | D2, the record is the latest accepted, not the latest delivered: the sample system sets 1.1 on any web submission, after the close and from an under-18 respondent alike, but keeps a field team's 4.1 or 4.2 over a household's own later web complete; only a cross-file cut (submission time, age, the address's code) shows each | D8 the close at UTC+13 on 30 September (daylight time from 26 September); the close read on the UTC date; partials; eligibility codes | issued addresses (letter, quarter, final_outcome), web returns (login_code, submitted_utc, last_section, age), CATI interviews (ADDRESS_ID, RESULT, END_TIME), plan s.4 and s.5, dictionary: 5 files, 11 columns | the sample system's 1.1 codes (0.2 to 1.3 high); eligibility on the field codes alone (0.09 low, every cell); completes over field-coded eligibles (0.11 high); under-18 kept (0.07 to 0.38 high); the UTC date (0.04 to 0.30 high); UTC+12 at the third quarter's close (the two third-quarter cells 0.05 to 0.13 high); the answer |
| B: each index's completes with a valid answer, online and by telephone | 24 | a measure every index carries that the call does not turn on | the methods log's evidence table | D1, the same records under two sources: the 9 to 12 August interviews sit in the web platform's export as staff-opened sessions, a column whose other values are help-line link reissues; only the close-out's outage and the dates show they were interviews | D8 the CATI clock in Halvreth time against UTC stamps, decisive on 345 twice-answered addresses (naive 172, UTC+12 all year 51 moved); under-18 returns; late returns; partials; both records kept | web returns (opened_by, submitted_utc, age, Q01 to Q17), CATI interviews (END_TIME, Q01 to Q17), close-out, plan s.5, codebook, dictionary: 6 files, 16 columns | outage as web (every count, 487 to 494 across); CATI clock naive (every count, about 170 across); UTC+12 all year (every count, about 51 across); under-18 kept (online 157 to 164 high); late kept (online 414 to 430 high); the UTC date (online 116 to 120 high); UTC+12 at the close (online 30 to 32 high); both records (online 239 to 250, telephone 91 to 94 high); the answer |

- **Span:** eight files and 20 columns across the asks; the sample system's code device moves all four rates, the
  outage device all 24 counts, the clock device all 24 counts and both third-quarter rates.
- **Shared hazards:** under-18 returns (A every cell, B every online count); the close in Halvreth time (A, B online);
  partials (A none, B online).
- **Realism:** sample management systems overwrite a non-final status on any return and keep a field team's
  ineligibility code; web platforms accept returns past a fieldwork close; push-to-web letters reach whoever opens them;
  a CATI outage sends interviewers to whatever system takes keyed answers; an overnight suppression feed lets a
  household be called the day it completed online.
- **Referee:** none.

| Ask figure | Where the cracker's path goes | Mirror (stops at rung 0) | Cracker (lands the call, runs the battery) |
|---|---|---|---|
| A response rates (4) | builds completes from the exports for the call, then takes eligibility from the sample system's final codes, so the 144 locked addresses leave the denominator with their completes counted or not (every cell 0.09 to 0.11 off); a fixed UTC+12 moves both third-quarter cells; under-18 returns stay unless it screens ages | misses the same way | miss |
| B valid answers (24) | reads the staff-entry returns as the web returns the export calls them (every count off by 487 to 494 across the modes) and orders twice-answered addresses on a fixed offset (about 51 across); under-18 returns stay in its online counts | misses the same way | miss |

- **Cracker keeps:** about a tenth of the ask figures (a cracker handling every device at once). The chart's parts
  sit on the call (the band, the widest bands, the binding index): an eighth of the ask weight if the generated rubric
  files them there.
- Mirror leakage: 13 per cent of ask weight (the chart's frame and band line; the mirror's ask path is the cracker's).
- Pair ceiling: 37.8 (C = 38 + 7 + 55 x 0.21 = 56.7 with the chart's parts kept; S = 5 + 7 + 55 x 0.125 = 18.9; mean
  37.8).

## Pre-ship check

1. Domain: the call stands on each headline index's mode effect, the measurement difference between answering online
   and by telephone for the same households, read through the contact strategy test's random letter allocation (the
   letters' difference over their difference in the share of completes made online); the comparison of web with
   telephone completes, however adjusted, files 3 (safe after dark binding), the letters' raw difference 6. With ward
   admissions or megawatt-hours for answers there is no interviewer whose presence moves a self-report, no household
   choosing its mode and no mode mix on a published series.
2. Two layers: Layer 1 (two systems' exports at different grains and clocks, late returns past each close, under-18
   returns, twice-answered addresses, the outage interviews keyed through the web platform, partials, mode-specific
   item codes, the sample system's own outcome codes) is neutral on the call, each item asserted (R2: the band stays
   4, heavy drinking between 4.40 and 4.83); Layer 2 is the encouragement design, asserted alone to move the default
   path to the golden on the clean truth (R3b).
3. No banned stump decides: nothing is planted (no memo, draft or figure states a mode effect, an uptake by index or a
   band; the close-out's uptake is in rounded words); not semantics (the default path reads every field right and
   files 3 on the clean truth, R3a); not rule application (MS-14 files the quantity, the population, the artefact and
   the band's rule and names no estimator, asserted on its text).
4. Gate G: no shipped artifact ranks the bands or the indexes' mode effects; the two distractors (the call records and
   the published series) carry no answers by mode and letter.
5. Determinism: the list grades the band, the four response rates and the 24 valid-answer counts; the band is 4 under
   the Wald estimator, two-stage least squares, either quarter alone and every Layer 1 mishandling; the components are
   ranges every estimator lands in; every response rate sits 0.022 or more inside its rounding bin; counts are
   integers. Judge pass r1: DETERMINISTIC, FIX_NOW on asks 2 and 3 only (the 18-or-over rule sat in the letters, not
   in plan section 5, and the 164 returns aged 15 to 17 move three rates and the counts); fixed by filing in section 5
   that a return or interview counts only when it comes from the person the letters ask for, and step 1 cites it; Gate
   G method_or_model_selection, analytical_non_defect, no surface read, not a sole data defect; Gate H domain pass,
   layers pass, decisive step analytical; stump power credible (the covariate-adjusted route files 3, the letters' raw
   difference 6). Pass r2 on the fixed pack: DETERMINISTIC, APPROVE, every golden figure reproduced (40,821 completes,
   heavy drinking 6.63 and 4.53, the four rates, all 24 counts); every fork it ran leaves the band at 4 (the close at
   UTC+12 or ignored, staff entries online, CATI start against end time, the age filter after the deduplication); its
   residuals moved no committed answer: the chart's non-binding bars carry no rounding (visual only), two
   twice-answered addresses switch mode on the CATI start time (closed: the dictionary now says END_TIME is when the
   interviewer coded the result), and the 144 field-coded addresses rest on the plan's highest-result rule (filed).
   After r2 the published series' second quarter of 2027 was anchored on the letter B completes it was released from
   (a distractor's values; no graded figure moved).
6. Asks: A is moved in every cell by the sample system's codes (1.1 on any return, a field team's 4.1 or 4.2 kept)
   and the under-18 returns, and in both third-quarter cells by the close at UTC+13; B in every count by the outage
   interviews and by the CATI clock on the twice-answered addresses; no stop moves the band (asserted).
7. Input gates: 12 files in five formats (csv, docx, md, pdf, xlsx), the call records at 204,006 rows and the issued
   addresses at 76,000, two distractors named in metadata.json; 113 generator checks; the verifier (its own completes,
   its own Wald estimate from the PDF's tolerances and the codebook's scoring) green; two builds byte-identical;
   figures_check 58 of 58; containers clean.
8. Duplicate guard: `guard.py heart` WARN (repeat.gate_g against task266, answered in Draw), nearest driver task259 at
   0.10; `guard.py surface` clean; the forum redrawn to line_manager_or_team after task157 (filed earlier the same day)
   reached this checkout.

## Leak check

`leak.py --asof 2027-10-20`: REVIEW, no LEAK (the plan's first file name, `mwt_cst27_test_plan.pdf`, carried the author
word "test" and was renamed `mwt_cst27_plan.pdf`; the web export's `device` became `device_type`). The REVIEW lines:

- MS-14 carries 0.30: heavy drinking's filed tolerance in Table 2, an input every route reads, not an answer.
- MS-14 carries the call's words: it defines the monitor and the band's rule and states no band.
- The dictionary, README, MS-14, close-out and plan carry stump-paragraph words (letters, households, survey, sample,
  close-out, uptake, random): the fiction's own nouns; none names the estimator, an instrument or the uptake ratio.
- `device_type` in the web export: the device the session ran on, a field every web survey platform exports.

Isolated reads (Sonnet, medium, prompt and pack only): pass 1 found no decisive-step sentence, ranking file or answer
figure and judged the call analytical; its one realism finding (the close-out's "For processing" bullets reading as a
list of the cleaning steps) was fixed by retelling the outage as fieldwork history and dropping the bullets the plan
already covers. Pass 2, after the judge's section 5 fix, and pass 3, after the close-out's response and outage lines
were reworded, again found question 1 none and the call analytical; pass 3 read the close-out as "a fieldwork
manager's real, short memo". The outage paragraph stays as the corroborating evidence the staff-entry device needs
(supplemental-stumping law 2); it moves no figure on the call.

## Tried and rejected

- A mode change read across rotation groups (the newest groups moved to web first, a difference in differences
  against time in sample): too close to task453's rotating-panel measurement change and to task236's attribution.
- A parallel run of both modes on split samples: calibration form parallel_run_overlap is banned against task464.
- A censored laboratory panel for the quality alert: the defensible estimators for left-censored data spread across
  the bands, so the call forks.
- A sensor errors-in-variables calibration: the regulator's own method is ordinary least squares, which forks
  against an orthogonal regression.
- A paired-difference standard error for the alert: too close to task228's driver (variance at the randomised unit).
- Each index pooled, flagged or given a new series on the same mode effects: the guard's same-puzzle test blocked it
  inside the batch (task465 v1's gap, pattern and decision type), and a three-way band per member repeats task236's
  and task237's output; the decision is cut as the monitor's band instead.
- The seed's own pitfall (ordinal items, polychoric invariance testing across modes): psychometric invariance is
  task237's pairing, banned against the last three builds, and the estimator choice reads as a convention fork.
