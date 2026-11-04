# task403 design note

Architecture 1, drawn 2026-11-04 (wave 7, Root-Cause lane), numbered from seed RC09 (a university estates department's
air-handler repair programme). The seed's world could not carry an honest unbanned draw on this objective, measured with
`guard.py check` on probe cards before anything else (`## Tried and rejected`, first lines), so the build moves to
another client domain, world and dataset under the same objective and number (`CLAUDE.md`, A stuck build is unblocked).
Kept from the seed: the decision kind (one programme of a short list, or none, funded from one budget) and the quantity
kind (what each programme would win back, in the outcome's natural unit). The kernel is new.

Ellesmere Media, an invented Canadian subscription streaming service (head office Toronto, English and French
catalogues, subscribers in every province), sells a monthly plan after a seven-day free trial. Trialists who signed up
between November 2025 and January 2026 converted to paid at about 43 per cent, against about 56 per cent for the same
months a year earlier. The growth team's review runs in early March 2026, once the January trials' first charges and
retries have matured, and the subscriber growth budget funds one programme against the fall, or none, to be in place
before the November 2026 sign-up peak: (A) a first-month price hold for trialists, (B) first-charge payment recovery
(retries and a card updater), (C) a winter release slate that keeps a weekly original airing through the holidays and
licenses a weekly series for December and January, (D) moving paid acquisition from social to search. The call faces
forward (the 2026-27 winter); each programme is valued on what its cause cost the 2025-26 winter's trials, the measured
window the programme sheet names.

What nothing in the pack says: a trialist decides at the day-7 charge, and what holds them is a show they were watching
whose season still has episodes to come after their trial ends. From November 2024 to October 2025 a weekly season was
airing every week; the two autumn 2025 seasons ended on 30 and 31 October, the winter's weekly original slipped to April
2026, and the winter's two originals arrived as full-season drops. The price for new subscribers rose from CAD 9.99 to
11.99 on first charges from 1 November 2025, the same night. At equal runway the price cost about a point.

## Draw

- Card: `.claude/skills/fingerprint/cards/task403.json`, architecture v1, drawn and registered 2026-11-04 (the
  registered stamp and the last `check` are in `pipeline.json`). `guard.py validate` clean.
- Pairing: Product Analytics, task type funnel-journey-analysis (DD, RC in the taxonomy), objective Root-Cause
  Analysis. The fall is located and explained on the trial journey (sign-up, first play, viewing days, trial end, first
  charge) and the call is which cause the plan fixes. Probed with `guard.py check` before the draw: legal for root-cause,
  no axis ban against task400, task402 or task401 (the last three live cards).
- Shape 09, funnel of stages for a fall: each stage of the trial journey with its volume and rate for the two winters
  and the conversions lost at it, each programme with the paid conversions its cause cost, the call, runner-up, gap and
  flip, a chart with its named parts, two files. The sum is drafted in `## Ask sheet` at stage 2 (at or above 25).
- Strategy composition_mix (F5), pattern E (conditioned yield), generators G14 then G6; Gate G
  decomposition_attribution; gap objective then population (the within-group fall after 1 November is correct and is
  not the price effect the decision is scored on); Layer 2 family estimand_identification (Simpson's reversal across a
  constructed stratum: the library-title control is contaminated by the same runway shift).
- Decision pick_one_of_n with a licensed non-pick (or none), answer unit named_option; forum executive_team, forcing
  event season_or_peak (the November 2026 sign-up peak the funded programme must be in place for), org family
  media_or_publishing, role product_manager (the head of subscriber growth), context artifact planning_thread (the
  growth team's programme sheet, which lists the four programmes and their costs and ranks nothing). The forcing event
  was first drafted as budget_or_appropriation; at registration task401's card had gone architecture_spent, the live
  window became task399, task400 and task402, and task399 holds that value (`ban.forcing_event`). The winter peak is the
  truer label (the review runs in March 2026 to put one programme in place for the peak), not merely the passing one.
- People from `guard.py names --geo Canada --seed 403`: Kristen Hurst, Julie Jacobson, Tamara Delgado (Thomas Mcneil
  was drawn and replaced: `people.first` WARN against task126).
- Data-native sentence: a trialist decides at the day-7 charge, and what holds them is a show whose season still has
  episodes to come, so the share of trialists who can stay is set by the release calendar, a file the content team
  keeps for scheduling, and that share fell on the same night the price rose because the autumn finales and the price
  notice both closed October.
- Abstraction sentence (written to test it, not writable against any approved build): a fall in a rate is booked to a
  dated change that coincides with it, because the fall holds in every visible group, in the units drawn in by things
  no other change touched and in the stated reasons, but each unit decides at the end of a fixed window on whether
  something it follows still has more to come, a state set by its own activity against a second calendar, and the
  share of units in that state fell in the same week. Against the approved builds (111, 119, 124, 128, 132, 135, 141,
  151, 162, 169, 175, 179, 182, 196, 236, 253, 258, 275, 303, 309 and 100 to 126): none is a coincident dated change
  taking the blame for a shift in a calendar-set state; 162 (a valve acts only in the hours its inlet runs above the
  setting) prices a fix by its operating hours and 124 (a share holds only within the kind of main) conditions a rate
  on a physical class, neither on a decision window against a release calendar.
- Same-puzzle and same-driver tests: `test.same_puzzle_older` (objective, E, pick_one_of_n) against task306 v4 and
  `test.same_driver_older` (objective, E, decomposition_attribution) against task271 v5 are older builds, each answered
  on the card's differentiation (a strategy's trading cost at scale; market impact inside an actor's sequences). Nothing
  in the last twelve shares either triple.
- WARNs answered: `overuse.objective` (root-cause in 6 of 12) is the lane: task403 is a root-cause number;
  `repeat.gate_g` and `overuse.gate_g` (decomposition_attribution): the honest mechanism is booking a correctly measured
  fall to its driver, and no forecast, binding limit or method selection carries the call here (the brief's preference
  for another FINE-numbers mechanism was screened: a forward runway forecast would add a fork and no stump);
  `repeat.question_form` (which): the pick asks which; the shell is drawn at stage 2 against `voice-check.py` quotas;
  `repeat.decision` (pick_one_of_n against task402): the decision kind is the seed's (one programme from a filed list,
  or none), kept on purpose; task402's pick is among filed changes ranked by cost, this one among programmes with a
  licensed non-pick, and the shape differs (09 against 01).
- Sources, every one synthetic and generated by `generator/` (no real dataset): the trial register, the first-charge
  billing export, the trial viewing log (the spine, about 450,000 trial-episode rows), the release calendar, the price
  notice, the conversion standard, the cancellation survey, the programme sheet, the paid acquisition report; modelled
  on Canadian SVOD practice (monthly plans after a seven-day trial, provincial sales taxes, English and French titles,
  weekly and full-season releases).

### Mechanisms on the objective, one line each (`guard.py mechanisms --objective root-cause`), and whether the decisive step is any of them in other nouns

- task13: re-attributes outcomes by physical evidence against an exceptions-only log. No: nothing is re-labelled here.
- task11: a threshold rebate accretive at zero volume on a rebuilt ledger. No.
- task36: an excluded largest candidate plus a counterfactual conditioned on a cancelling property. No filed exclusion.
- task50: exposure inside a funded window by a projected issue order. No window projection.
- task72: booking to the owner whose agreement covered each piece across transfers. No transfer or owner.
- task84: identical concurrent copies raise their own price. No competing copies.
- task111: the closed window's leading cause is generated by an arrangement the forward window replaces. No: the call
  here is the winter's own decomposition; the slate is the cause in the window measured, not a forward replacement.
- task500: changes measured by a matched-reference method; v2 a spillover through a link to touched units. No.
- task129: a rise outside the zone maintenance touches, scaling with each unit's surroundings; v1 two causes separated
  by groups that each received one. No group here received one cause alone (the price reached every first charge from
  1 November); the separation is each trialist's own state.
- task121: each event's exposure to rest rebuilt from consecutive worked periods. Nearest in kind (a hidden per-event
  state rebuilt from the organisation's schedule while a coincident change takes the blame); the state, the schedule
  and the reconstruction differ (rest between shifts on a rota against content still to come on a release calendar),
  answered on the card.
- task202: an inflow's depth set by its density against the lake's layering. No.
- task398: removing a component's loss re-runs a path-dependent rule. No rule or path.
- task399: whether the advocate was in the room when the case was called. No shared actor.
- task400: alerts read against speed inside a rollout window with the same crews on both versions. No rollout or
  within-window comparison.
- task402: second failures filed under the cause their aftermath resembles. No re-labelled events.
- task401: failures inside the recovery days after a small contributor's excursions. No excursion or recovery.
- Seed RC09's own insight (a past repair priced on units whose operating regime let it pay) is task162's and task83's;
  it is not used.

## Default path

The field's method at rung 0 and 1: trial cohorts by start date, matured to the first charge, compared year on year,
cut by every visible segment, with a content-neutral control and an event study on the price date.

1. Read the conversion standard: trials counted by start date in Toronto time; a trial converts when its first monthly
   charge, due at the end of the seven-day trial, is collected within the retry window.
2. Join the trial register to the first-charge billing export; build the November to January cohorts of both winters.
3. Conversion falls from about 56 to about 43 per cent, about 13 points, about 3,700 paid conversions on the winter's
   about 27,600 trials.
4. Cut by plan, device, acquisition channel and province: the fall holds in every cell, 11 to 15 points; the
   acquisition mix barely moved, so (D) is worth little.
5. Content control: trialists who signed up on library titles, which no slate change touched, fell about 10 points.
6. Event study by trial-start day: the step lands on the trials whose first charge fell on or after 1 November, the
   date the price notice moved new subscribers to CAD 11.99.
7. First-charge declines and their recovery are flat, so (B) is worth little; the cancellation survey's price reason
   climbs after 1 November.
8. Book the fall to the price and fund (A) the first-month price hold, sized at the year-on-year fall.

Ends on: (A) the first-month price hold, about 3,700 paid conversions
Golden: (C) the winter release slate, about 3,400 paid conversions, with (A) at about 300

## Stump sentence

A competent solver compares the November to January trials with a year earlier, finds conversion down about 13 points
in every plan, device, channel and province and about 10 points among the library-title trialists no slate change
touched, sees the step arrive with the 1 November first charges at the new price, and funds (A) the first-month price
hold on about 3,700 lost conversions; the step that lands it there is never setting each trialist's viewing against the
release calendar to ask whether a show they were watching still had episodes to come after day 7, which puts about
3,400 of the loss on the winter slate (C) and leaves the price about 300.

## Three rules

- Task type: product-analytics / funnel-journey-analysis, which serves root-cause in the taxonomy; the fall is located
  on the trial journey and explained by what decides the day-7 charge.
- Domain test: the deciding quantity is the paid conversions each cause cost the November 2025 to January 2026 trials
  against a year earlier, read through each trialist's content runway at the day-7 charge (a show they were watching
  with episodes released after their trial ended), worked as streaming trial-journey analysis against the release
  calendar.
- Swap: "fund the winter release slate, because trialists whose show had ended cancelled at day 7" in a hospital's
  nouns ("fund the ward schedule, because patients whose ward round had ended...") stops making sense: weekly drops,
  full-season releases, a season finale and a holiday slate have no counterpart, and the coincidence that decides the
  easy route is a subscription price notice meeting a broadcast season's last night.
- Layer 1: viewing heartbeats logged in UTC against trial clocks in each subscriber's local time across the 2 November
  2025 clock change, with Saskatchewan on standard time all year (the viewing platform); new content identifiers from
  the June 2025 content management migration, with a crosswalk (the CMS); English and French records of one series
  (the catalogue); billing exports in cents with GST, HST and QST by province (the billing system); duplicate heartbeat
  summaries written on app reconnects (the player). Nothing is placed to be caught; none of it decides the call.
- Layer 2: estimand_identification, Simpson's reversal across a constructed stratum; conditioning the year-on-year fall
  on each trialist's runway state separates the within-state change (about a point, the price) from the shift in the
  share of trialists with episodes still to come (about 12 points), and the library-title control the easy route trusts
  is contaminated by that shift.
- Decisive step: reading each trialist's day-7 charge against whether a show they watched during the trial still had
  episodes to be released after the trial ended, rebuilt from the viewing log against the release calendar, and
  splitting the winter's loss into that state's mix and the change within it.
- Not semantics: every field read correctly (the price notice's effective date, the trial clock, the conversion
  standard, the calendar's release times, the billing codes) still leaves the year-on-year fall, the segment cuts, the
  library control and the event study on the price; runway is no field, flag or code in any file.
- Not rule application: no filed rule names runway, a stratification or a decomposition; executing the conversion
  standard and the price notice files the year-on-year fall and the step at 1 November. The estimator family the rules
  leave open (runway by acquisition title or by any title watched, by any play or a full episode, trial end at the
  exact hour or the local day; the decomposition weighted by either winter's mix or their mean) is measured at stage 2
  and asserted in `checks.py`, enumerated and standing spreads both, with the loudness of the ruling-out.
- Analyst test: a strong analyst who cleans every file and reads every rule correctly finds the fall in every segment,
  in the library-title control and at the price date, and funds (A) the first-month price hold on about 3,700 lost
  conversions, the default path's `Ends on:`.
- Estimand: the conversion standard (the growth team's filed measurement standard) fixes the trials (by start date in
  Toronto time), the outcome (the first monthly charge collected), the windows (November to January, each winter) and the
  comparison (the same months a year earlier); the programme sheet states that each programme is valued at the paid
  conversions the winter's trials lost to the cause it addresses.
- No decoy: nothing is planted; the price rise is real and costs about a point, the cancellation survey records what
  trialists ticked, the programme sheet ranks nothing and no memo, draft or briefing argues for any programme.
- No certified replay: no certified or published figure is reproduced to recover a method; the KPI pack shows the
  conversion series and nothing that ranks the causes.
- Lesson: before booking a conversion fall to a coincident price change, read each decision against the state it was
  made in (content still to come at the day-7 charge), rebuilt from viewing against the release calendar; no build on
  file teaches release cadence or content runway.

## Survivor anatomy

- Actor: the deciding property, whether a show the trialist was watching still had episodes to come when the trial
  ended, has no column in any file; the trialist has rows (a trial, a charge, viewing rows) and the property is a
  relation between the viewing rows and the release calendar's later episodes.
- Link: the signal is read through a comparison no key offers and no sentence invites: each trialist's trial end set
  against the next release date of every season they played, across the viewing log and the release calendar, which
  the conversion standard and the programme sheet never mention together.
- Reflex: the field's method (year-on-year cohorts, segment cuts, a content-neutral control, an event study on the
  price date) sits at rungs 0 and 1 and files (A) at about 3,700.
- Back-test: the textbook route validates: the library-title control falls about 10 points, the step lands on the price
  date, the survey's price reason climbs, and first-charge declines are flat; nothing in the pack refutes the price.
- Second use: the release calendar is the content team's schedule and carries its own ask (each original's first-week
  sign-ups); the viewing log carries the funnel's activation and engagement stages; neither drops out if the decisive
  step is deleted.
- Shock: the moved share is spread across every trial, every province and every acquisition title; no unit, title or
  week is the pack's largest anomaly, and the November to January cohorts are not an interval of any one shipped sort.
- Pins: the WHAT sits in the conversion standard and the programme sheet in the growth team's own genre (trials by start
  date, the first charge collected, the same months a year earlier, each programme valued on its cause's lost
  conversions); no filed sentence names runway, the release calendar, the trial's end against a season, or a
  decomposition.

## Tried and rejected

- 2026-11-04, the seed's world (a university estates department's air-handling units, a winter heating and
  ventilation energy rise, one repair programme or none): measured undrawable on root-cause with probe cards.
  energy-systems-utilities x root-cause is `ban.pairing`-blocked by task402; its one root-cause task type
  (grid-reliability-outage-analysis) is `ban.subdomain`-blocked; efficiency-savings-verification, the natural home of
  measurement and verification, serves experiment-causal only (`three_rules.task_type`); asset-condition-maintenance
  serves forecasting and opportunity sizing only; the policy-education house domain's only root-cause task type is
  multilevel-classroom-school-research, which the world would use as a backdrop. Moved world.
- 2026-11-04, the seed's own insight (the book of past repairs priced the fan-drive repair on units whose fans could
  slow, and this year's faulty units run a regime in which it cannot): spent in other nouns as task162 (approved: each
  valve lowers pressure only in the hours its inlet runs above the setting) and task83 (a measured effect conditioned
  on a history-rebuilt property to transport it to a new pool), also task170 (a protection acts only on the exposure
  that arrives while the protected state holds). Not carried into the new world.
- 2026-11-04, an online grocer's checkout funnel where payment failures in zone-days whose delivery slots filled are
  re-placed by other customers' bookings: the driver is task472's (a job already waiting for its window saves nothing),
  task79's (conversion falls once a downstream capacity binds) and task106's (sizing each candidate against the whole
  shared pool overstates) in other nouns. Not drawn.
- 2026-11-04, the cells left after the bans, screened on paper: customer-satisfaction-driver-analysis (two deaths in
  the last ten days, both linking each response to the conditions it was made under), health-equity-disparity-
  decomposition (two stage-2 deaths on honest magnitudes, one on care-home composition), mediation and panel-data
  estimation (deciding quantities are fitted estimators whose families do not close), multilevel-classroom-school-
  research (every decisive step found was a grouping choice, which 1.1c kills), interpretability (no world where the
  attribution is both the field's object and determinate), factor-return-attribution and sentencing-bail (task398 and
  task399, two days old). Product Analytics' funnel-journey-analysis is the one cell with no recent death.
- 2026-11-04, within the streaming world, a runway counted on a horizon (an episode within 7, 14 or 28 days of the
  trial's end) and a calendar with mid-season hiatuses and gaps between seasons: measured on the harness, the runway
  leaks through every hiatus, January recovers under the new price, and the 15-month history dips whenever nothing
  airs, each a refutation of the price on the easy route's own chart. Replaced by season-based runway (a watched
  season still has an episode to come) and a calendar that keeps a weekly season airing from November 2024 to October
  2025.
- 2026-11-04, stage 2, full-season drops in the 2025-26 winter only (the draw's calendar): the coordinator's first-look
  reader (outcome by week, every candidate's dated record beside it, a before-and-after on each date, the reflex
  segmentations including the release type of the most-watched show and of any show watched) would read "full-season
  drop trialists convert less and their share rose in November" and land the slate without the runway. Replaced by an
  originals-only service whose every season is released weekly in both winters (harness h7, h8).
- 2026-11-04, stage 2, a catalogue with licensed boxsets and library titles beside weekly originals (harness h5, h6):
  the trialists who watched no weekly-released show had no runway in either winter, so their fall was the price alone
  (1.4 to 5.3 points against 17 to 22 for weekly watchers), a contrast a first-look reader reads even at 2 per cent of
  the winter's trials. Any group whose runway never moves reveals the price's true size, so the world has no such group:
  every title is an Ellesmere original released weekly.
- 2026-11-04, stage 2, the first-look reader's composition arithmetic counted titles present in one winter only (a 165
  per cent "mix" share for acquisition title); corrected to common support, the title mix explains 3 per cent and the
  new-release-against-catalogue mix about 30 per cent, both inside the price story.
