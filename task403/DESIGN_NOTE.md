# task403 design note

Architecture 1, drawn 2026-11-04 (wave 7, Root-Cause lane), numbered from seed RC09 (a university estates department's
air-handler repair programme). The seed's world could not carry an honest unbanned draw on this objective, measured with
`guard.py check` on probe cards before anything else (`## Tried and rejected`, first lines), so the build moves to
another client domain, world and dataset under the same objective and number (`CLAUDE.md`, A stuck build is unblocked).
Kept from the seed: the decision kind (one programme of a short list, or none, funded from one budget) and the quantity
kind (what each programme would win back, in the outcome's natural unit). The kernel is new.

Ellesmere Media, an invented Canadian subscription streaming service (head office Toronto, English and French
versions of every title, subscribers in every province), sells a monthly plan after a seven-day free trial and carries
only its own originals, every season released one episode a week on Friday at midnight Toronto time. Trialists who
signed up between November 2025 and January 2026 converted to paid at 37.1 per cent, against 51.7 per cent for the same
months a year earlier: 2,519 paid conversions at this winter's 17,292 trials. The growth team's review runs in March
2026, once the January trials' first charges and retries have matured, and the subscriber growth budget funds one
programme against the fall, or none, to be in place before the November 2026 sign-up peak: (A) a first-month price
hold for trialists, (B) first-charge payment recovery (retries and a card updater), (C) a winter release slate that
keeps a weekly original airing from November to February, (D) moving paid acquisition from social to search. The call
faces forward (the 2026-27 winter); each programme is valued on what its cause cost the 2025-26 winter's trials, the
measured window the programme sheet names.

What nothing in the pack says: a trialist decides at the day-7 charge, and what holds them is a season they were
playing that still has an episode to come after their trial ends. From November 2024 to October 2025 a weekly season
was always airing (last winter, Marrow Creek from 25 October to 14 February). The three autumn 2025 seasons ended on 24
and 31 October, the winter's original (Gravel & Gold) slipped to April 2026, and nothing new aired from 1 November. The
price for new subscribers rose from CAD 9.99 to 11.99 (premium 14.99 to 16.99) on first charges from 1 November 2025,
the same night. At equal runway the price cost about a point.

## Draw

- Card: `.claude/skills/fingerprint/cards/task403.json`, architecture v1, drawn and registered 2026-11-04 (the
  registered stamp and the last `check` are in `pipeline.json`). `guard.py validate` clean.
- Pairing: Product Analytics, task type funnel-journey-analysis (DD, RC in the taxonomy), objective Root-Cause
  Analysis. The fall is located on the trial's stages (sign-up, first play, still subscribed at the trial's end, first
  charge collected) and the call is which cause the plan fixes. Probed with `guard.py check` before the draw: legal for
  root-cause, no axis ban against the live window.
- Shape 09, funnel of stages for a fall: each stage's share for the two winters, each programme with the paid
  conversions its cause cost, the call, runner-up and gap, the months between the winters stage by stage, a waterfall
  with its named parts, two files. The sum is in `## Ask sheet` (38 criteria).
- Strategy composition_mix (F5), pattern E (conditioned yield), generators G14 then G6; Gate G
  decomposition_attribution; gap objective then population (the within-group fall after 1 November is real and is not
  the price effect the decision is scored on); Layer 2 family estimand_identification (Simpson's reversal across a
  constructed stratum: the catalogue sign-up control is contaminated by the same runway shift).
- Decision pick_one_of_n with a licensed non-pick (or none), answer unit named_option; forum executive_team, forcing
  event season_or_peak (the November 2026 sign-up peak the funded programme must be in place for), org family
  media_or_publishing, role product_manager (the head of subscriber growth), context artifact planning_thread (the
  growth team's programme sheet, which lists the four programmes and their costs and ranks nothing). The forcing event
  was first drafted as budget_or_appropriation; task399 holds that value in the live window (`ban.forcing_event`).
- People from `guard.py names --geo Canada --seed 403`: Kristen Hurst, Julie Jacobson, Tamara Delgado (Thomas Mcneil
  was drawn and replaced: `people.first` WARN against task126). The prompt names no one.
- Data-native sentence: a trialist decides at the day-7 charge, and what holds them is a season still releasing
  episodes after their trial ends, so the share of trialists who can stay is set by the release calendar against each
  trialist's own seven days, and that share fell to nothing on the night the price rose because the autumn finales and
  the price notice both closed October.
- Abstraction sentence (written to test it, not writable against any approved build): a fall in a rate is booked to a
  dated change that coincides with it, because the fall holds in every visible group, in the units drawn in by things
  no other change touched and in the stated reasons, but each unit decides at the end of a fixed window on whether
  something it follows still has more to come, a state set by its own activity against a second calendar, and the
  share of units in that state fell in the same week. Against the approved builds (111, 119, 124, 128, 132, 135, 141,
  151, 162, 169, 175, 179, 182, 196, 236, 253, 258, 275, 303, 309 and 100 to 126): none is a coincident dated change
  taking the blame for a shift in a calendar-set state; 162 prices a fix by its operating hours and 124 conditions a
  rate on a physical class, neither on a decision window against a release calendar.
- task401 architecture 3 (in its card lineage, spent at stage 4, never shipped: a new-customer satisfaction fall booked
  to a coincident billing-platform go-live, truly a shift in each customer's quote-against-metered-cost state with
  rates flat within each state): the real difference is that there the state was a static band, one per customer
  fixed when they joined, from two of that customer's own records (the quote against the meter's later use), while here
  the state is a runway measured from each trialist's own decision point (their day 7) against a second calendar that
  every trialist shares, so it moves for everyone at once when the schedule goes dark and no record of the trialist's
  alone holds it. The screens are honest to it: the golden reads each trialist's played seasons against the calendar at
  their own day 7; no band of a register field (plan, device, channel, province, language, sign-up title, its airing
  status or age) reaches it (first-look reader, 20 of 20 on A); and the same relation read at sign-up, during the trial
  or at the end of the last local day is the decisive family read at another instant, asserted to file the same figure
  (2,117 at all four on the build world, 2,077 to 2,145 over 20 redraws), not a static proxy.
- Same-puzzle and same-driver tests: `test.same_puzzle_older` (objective, E, pick_one_of_n) against task306 v4 and
  `test.same_driver_older` (objective, E, decomposition_attribution) against task271 v5 are older builds, each answered
  on the card's differentiation (a strategy's trading cost at scale; market impact inside an actor's sequences).
- WARNs answered: `overuse.objective` (root-cause in 6 of 12) is the lane; `repeat.gate_g` and `overuse.gate_g`
  (decomposition_attribution): the honest mechanism is booking a correctly measured fall to its driver, and no
  forecast, binding limit or method selection carries the call here; `repeat.question_form` (which): the pick asks
  which; `repeat.decision` (pick_one_of_n against task402): the decision kind is the seed's, kept on purpose; task402's
  pick is among filed changes ranked by cost, this one among programmes with a licensed non-pick, shape 09 against 01.
- Sources, every one synthetic and generated by `generator/` (no real dataset): the trial register (73,387 rows), two
  card processors' first-charge exports, the trial viewing log (the spine, 440,424 rows), the release calendar, the
  plan-change log, the content and account crosswalks of the June 2025 platform cut-over, the product release log, the
  conversion standard, the price notice, the programme sheet, the cancellation survey and the paid media report (the
  two distractors); modelled on Canadian SVOD practice (monthly plans after a seven-day trial, provincial sales taxes,
  English and French versions, weekly releases). Fourteen files in four formats (csv, parquet, xlsx, pdf).
- Stage 3 gates (2026-11-04, on the final cut, after merging claude/jolly-hypatia-06c61h at 0570620; no sibling card
  missing from the tree): `guard.py heart` WARN with no BLOCK, nearest driver 0.08 (task500 v2), nearest text 0.06;
  the WARNs are the drawn ones answered above plus `repeat.deliverables` (pdf and xlsx, as task399 v4): the set is
  drawn with this world, a workbook for the figures and a one-page growth note carrying the waterfall, against a court
  list there. `guard.py surface` promotes three structural pairs and no surface tell: task402 (back to back, same gap
  and decision type, pattern E against none), task306 (gap, pattern and decision family) and task271 (gap, pattern
  and Gate G); each carries a differentiation line on the card, and the adjudicated `/clone-check` is the author's call.
  `leak.py --asof 2026-03-09` REVIEW, no LEAK: the standard and the price notice share ordinary words with the stump
  paragraph (charge, standard, change, viewing) and name no runway, calendar or split; `signup_device` is the
  streaming field's own noun, declared under `field_terms`; the calendar's April to June 2026 dates are Gravel &
  Gold's scheduled episodes, a forward schedule.
- Stage 4 round 1 fix pass (2026-11-04, after merging claude/jolly-hypatia-06c61h at 0b1b7fa; no sibling card missing
  from the tree): this pass moved no graded figure (freeze.py PASS in rubric and in determinism mode against the
  snapshot taken before the first edit; figures.json byte-identical). The files that moved are six of fourteen:
  plan_changes.csv (2,348 rows, none starting from a subscription nothing else names), both processor exports (the
  charges on their own random stream), trial_register.csv and account_crosswalk.csv (the 8 copies of web and phone
  sign-ups of 02:00 to 04:00 on 9 June and their copy accounts gone, 73,379 register rows), and
  growth_programmes_2026-27.xlsx (the Funding line); the other eight are byte-identical. The effect, measured: the
  narrow reading of the unlinked charges prints the golden in all nine months (D7i; 24 variants, no trial
  differing), the judge's Toronto-midnight clock prints June at 52.2 (H1), and every free gate is green on the final
  cut (checks.py 70 of 70, verify.py 38 figures, two byte-identical builds, figures_check 67 figures, precut 61
  checks, voice-check PASS, leak.py REVIEW with no LEAK on the same four lines answered above, guard.py heart WARN
  with no BLOCK at a nearest driver of 0.08, surface the same three structural pairs and no tell, ceiling.py pair
  34.8 with the cracker, the full includer, the no-repair reader and the mirror at 0 of 18).

### Mechanisms on the objective, one line each (`guard.py mechanisms --objective root-cause`), and whether the decisive step is any of them in other nouns

- task13: re-attributes outcomes by physical evidence against an exceptions-only log. No: nothing is re-labelled.
- task11: a threshold rebate accretive at zero volume on a rebuilt ledger. No.
- task36: an excluded largest candidate plus a counterfactual conditioned on a cancelling property. No filed exclusion.
- task50: exposure inside a funded window by a projected issue order. No window projection.
- task72: booking to the owner whose agreement covered each piece across transfers. No transfer or owner.
- task84: identical concurrent copies raise their own price. No competing copies.
- task111: the closed window's leading cause is generated by an arrangement the forward window replaces. No: the slate is
  the cause in the window measured, not a forward replacement.
- task500: changes measured by a matched-reference method; v2 a spillover through a link to touched units. No.
- task129: a rise outside the zone maintenance touches, scaling with each unit's surroundings; v1 two causes separated
  by groups that each received one. No group here received one cause alone (the price reached every first charge from
  1 November); the separation is each trialist's own state.
- task121: each event's exposure to rest rebuilt from consecutive worked periods. Nearest in kind (a hidden per-event
  state rebuilt from the organisation's schedule while a coincident change takes the blame); the state, the schedule
  and the reconstruction differ (rest between shifts on a rota against seasons still releasing on a release calendar).
- task202: an inflow's depth set by its density against the lake's layering. No.
- task398: removing a component's loss re-runs a path-dependent rule. No rule or path.
- task399: whether the advocate was in the room when the case was called. No shared actor.
- task400: alerts read against speed inside a rollout window with the same crews on both versions. No rollout or
  within-window comparison.
- task402: second failures filed under the cause their aftermath resembles. No re-labelled events.
- task401: failures inside the recovery days after a small contributor's excursions (architecture 4); architecture 3
  answered above.
- Seed RC09's own insight (a past repair priced on units whose operating regime let it pay) is task162's and task83's;
  it is not used.

### First-look reader (the coordinator's screen, `generator/screens.py`)

Coded and run over 20 redraws on the final world (seeds 1 to 20) and the build world (seed 40326). It tabulates paid
conversion by trial-start week, lays every candidate's own dated record beside it (the price notice, the processor
switch, the paid social campaign, the release calendar's finales and premieres), runs a before-and-after on each date
(build world: price 16.4 points, finales 17.1, campaign 11.7, processor 1.0), and runs the reflex segmentations with a
200-trial readable floor: plan, device, channel, province, language, sign-up title, the sign-up title's airing status
and age at sign-up (28, 56, 91 days), the most-watched title and its age, the release type (weekly for every title) and
the engagement bands (minutes, seasons, viewing days). Its rule books to the slate the largest share of the fall the mix
of any content band explains, to (D) the channel mix, to (B) the recovery change and the rest to (A), after a check that
no content band shows the fall absent in a fifth of this winter's trials. Result on the final world: (A) in 20 of 20
redraws and on the build world; its slate figure 184 to 307 (build 294, by the most-watched title), its price figure
1,998 to 2,148 (build 2,030). It never sets a trialist's played seasons against the calendar's dates around that
trialist's own trial: that relation, at any instant, is the decisive family.

## Default path

The field's method at rungs 0 and 1: trial cohorts by start date, matured to the first charge, compared year on year,
cut by every visible segment, with a content-neutral control and an event study on the price date.

1. Read the conversion standard: trials counted by start date in Toronto time; a trial converts when the first monthly
   charge, due when the seven-day trial ends, is collected within the retry schedule.
2. Join the trial register to both processors' first-charge attempts; build the November to January cohorts of both
   winters (17,965 and 17,292 trials).
3. Conversion falls from 51.7 to 37.1 per cent, 14.6 points: 2,519 paid conversions at this winter's trials.
4. Cut by plan, device, channel and province: the fall holds in every cell, 8 to 20 points; the channel mix barely
   moved, so (D) is worth about 100.
5. Content control: trialists who signed up on a season that had already finished, which no slate change touched,
   fell 11.3 points.
6. Event study by trial-start day: the step lands on the trials whose first charge fell on or after 1 November, the
   date the price notice moved new subscribers to CAD 11.99.
7. First-charge declines are flat and recovery fell under the new processor, so (B) is worth about 100; the
   cancellation survey's price reason climbs after 1 November.
8. Book the fall to the price and fund (A) the first-month price hold, sized at the year-on-year fall.

Ends on: (A) the first-month price hold, about 2,500 paid conversions
Golden: (C) the winter release slate, about 2,100 paid conversions, with (A) at about 200

## Stump sentence

A competent solver compares the November to January trials with a year earlier, finds conversion down about 15 points
in every plan, device, channel and province and 11 points among the trialists who signed up on finished seasons no
slate change touched, sees the step arrive with the 1 November first charges at the new price, and funds (A) the
first-month price hold on about 2,500 lost conversions; the step that lands it there is never setting each trialist's
played seasons against the release calendar to ask whether one still had an episode to come after their day 7, which
puts about 2,100 of the loss on the winter slate (C) and leaves the price about 200.

## Three rules

- Task type: product-analytics / funnel-journey-analysis, which serves root-cause in the taxonomy; the fall is located
  on the trial's stages and explained by what decides the day-7 charge.
- Domain test: the deciding quantity is the paid conversions each cause cost the November 2025 to January 2026 trials
  against a year earlier, read through each trialist's content runway at the day-7 charge (a season they played with
  an episode released after their trial ended), worked as streaming trial-conversion analysis against the release
  calendar.
- Swap: "fund the winter release slate, because trialists whose season had stopped releasing cancelled at day 7" in a
  hospital's nouns ("fund the ward schedule, because patients whose ward round had ended...") stops making sense:
  weekly episode drops, a season finale, a holiday slate and a trial that pays only if a show is still airing have no
  counterpart, and the coincidence that decides the easy route is a subscription price notice meeting a broadcast
  season's last night.
- Layer 1: plays logged in UTC against trials counted in Toronto time across the 2 November 2025 clock change (the
  viewing service); legacy content and account numbers before the June 2025 platform cut-over, with crosswalks (the
  content system and the account service); English and French versions of each episode under their own identifiers
  (the catalogue); one processor in tax-included cents with four attempts to 7 September 2025 and another in pre-tax
  dollars with tax beside it, Toronto time with an offset and three attempts from 8 September (billing); a row written
  twice when an app reconnects (the player); the cut-over's sign-up pause on the night of 8 June and the old platform's
  rows of 9 to 19 June in Toronto time stamped as UTC, its mirror of web and phone sign-ups switched on at 04:00 on 9
  June (the subscription platform); while a plan change opened a new subscription, the subscription managed where it
  was opened, so a trial's changes all reached the plan-change log or none did (the account service). Each ordinary cause is dated in the
  product release log. Nothing is placed to be caught; none of it decides the call.
- Layer 2: estimand_identification, Simpson's reversal across a constructed stratum; conditioning the year-on-year fall
  on each trialist's runway state separates the within-state change (about a point and a half, the price with the
  smaller recovery and channel effects) from the shift in the share of trialists with an episode still to come (70 per
  cent to none), and the catalogue sign-up control the easy route trusts is contaminated by that shift.
- Decisive step: reading each trialist's day-7 charge against whether a season they played during the trial still had
  an episode to be released after the trial ended, rebuilt from the viewing log against the release calendar, and
  splitting the winter's loss into that state's mix and the change within it.
- Not semantics: every field read correctly (the price notice's effective date, the trial clock, the conversion
  standard, the calendar's release times, the billing codes) still leaves the year-on-year fall, the segment cuts, the
  catalogue control and the event study on the price; runway is no field, flag or code in any file.
- Not rule application: no filed rule names runway, a stratification or a decomposition; executing the conversion
  standard and the price notice files the year-on-year fall and the step at 1 November. The enumerated family of
  constructions (state at day 7, at the end of the last local day, at sign-up or at any point of the trial; a play of
  any length, five minutes, 10, 25, 50 or 90 per cent of the runtime; last winter's gap, the only one defined) spreads
  the slate's figure 2,062 to 2,117 on the build world, one hundred-bin, and the standing family is the same set: every
  member names (C) by about tenfold; the ruling-out is loud, since the register-only route (the sign-up season's own
  runway) files 581 and names (A).
- Analyst test: a strong analyst who cleans every file and reads every rule correctly finds the fall in every segment,
  in the catalogue sign-up control and at the price date, and funds (A) the first-month price hold on about 2,500 lost
  conversions, the default path's `Ends on:`.
- Estimand: the conversion standard (the growth team's filed measurement standard) fixes the trials (by start date in
  Toronto time), the outcome (the first monthly charge of the subscription the trial ends on, collected within the retry
  schedule), the windows (November to January, each winter) and the comparison (the same months a year earlier); the
  programme sheet states that each programme is valued at the paid conversions this winter's trials lost to the cause
  it addresses, the four and what none addresses accounting for the fall once.
- No decoy: nothing is planted; the price rise is real and costs about a point and a half, the cancellation survey
  records what trialists ticked, the programme sheet ranks nothing and no memo, draft or briefing argues for any
  programme.
- No certified replay: no certified or published figure is reproduced to recover a method; no KPI pack or prior review
  ships.
- Lesson: before booking a conversion fall to a coincident price change, read each decision against the state it was
  made in (an episode still to come at the day-7 charge), rebuilt from viewing against the release calendar; no build on
  file teaches release cadence or content runway.

## Survivor anatomy

- Actor: the deciding property, whether a season the trialist was playing still had an episode to come when the trial
  ended, has no column in any file; the trialist has rows (a trial, charges, viewing rows) and the property is a
  relation between the viewing rows and the release calendar's later episodes at the trialist's own day 7.
- Link: the signal is read through a comparison no key offers and no sentence invites: each trialist's trial end set
  against the last release of every season they played, across the viewing log (content ids, legacy before June 2025)
  and the release calendar, which the conversion standard and the programme sheet never mention together.
- Reflex: the field's method (year-on-year cohorts, segment cuts, a content-neutral control, an event study on the
  price date) sits at rungs 0 and 1 and files (A) at about 2,500.
- Back-test: the textbook route validates: the catalogue sign-up control falls 11.4 points, the step lands on the price
  date, the survey's price reason climbs, and first-charge declines are flat; nothing in the pack refutes the price.
- Second use: the viewing log carries the first stage of the funnel (played an episode) and the months-between ask; the
  release calendar is the content team's schedule and the slate's own dated record (the candidate comparable to the
  price notice); neither drops out if the decisive step is deleted.
- Shock: the moved share is spread across every trial, every province and every sign-up title; no unit, title or week
  is the pack's largest anomaly, and the November to January cohorts are not an interval of any one shipped sort.
- Pins: the WHAT sits in the conversion standard and the programme sheet in the growth team's own genre (trials by start
  date, the first charge collected, the same months a year earlier, each programme valued on its cause's lost
  conversions); no filed sentence names runway, the release calendar, the trial's end against a season, or a
  decomposition by state.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 year-on-year fall booked to the price (A, 2,519) | the standard files the cohorts | trial and charge columns | the field's method | the catalogue control confirms it | none | one subtraction | none | readable |
| 1 recovery and channel netted out (A, 2,318) | none | the two processors, the channel column | the obvious correction | none | none | two shift-shares | none | readable |
| 2 content band from the register and titles (A, 1,737 to 2,030) | none | sign-up page and titles | new-against-catalogue is a streaming reflex | the catalogue control | none | one group-by | none | readable |
| 3 runway at each trialist's day 7 against the calendar (C, 2,117) (decisive) | silent: no sentence names a runway, a season's last release or the trial's end against it | silent: no column holds the state; it is a relation across the viewing log, the calendar and each trial's clock | silent: every reflex files (A) (first-look reader 20 of 20) | silent: no control refutes the price; the catalogue control falls 11.4 of 14.6 | silent: no battery item touches it | silent: a per-trialist relation and a split, no subtraction of shipped figures | silent: the viewing log and the calendar each carry a second use | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | which trials are in a winter | start date in Toronto time, 1 November to 31 January | start date in UTC | same call (asserted) | the conversion standard's start-date sentence |
| SF2 | converted | the first monthly charge of the subscription the trial ends on, collected within the retry schedule | the register's own subscription only | same call; main windows hold no plan-change subscription (asserted zero) | the standard's plan-change sentence |
| SF3 | the comparison | the same months a year earlier | the months just before (August to October) | the fall would shrink, same call | the standard's comparison sentence |
| SF4 | a season the trialist played | any play of an episode | a floor of five minutes or of 10, 25, 50 or 90 per cent of the runtime | same call, 2,062 to 2,117, one bin (asserted) | same call |
| SF5 | the trial's end | start plus seven days to the second | the end of the trial's last local day | same call, same figure (asserted) | same call |
| SF6 | the instant the state is read | the trial's end | at sign-up, or at any point of the trial | same call, same figure (asserted) | same call |
| SF7 | the gap the runway shift is priced at | last winter's paid-rate gap between the states | this winter's gap | this winter has no trialist with runway, so only one gap exists (asserted) | the data (C1) |
| SF8 | the price's figure | net of the recovery and channel effects (205) | gross of the channel mix (310), or the keep-rate change within the runway state alone (306): the 300 bin and a gap of 1,800 | same call; each gross reading counts (D) twice and the four then exceed the fall by about 100 (asserted) | the programme sheet's sentence that the four and what none addresses account for the fall once |
| SF9 | the price's figure, residual or direct | the within-state fall less recovery and the channel mix (205) | within each state and channel, at this winter's mix (204) | same call; every once-accounting reading (SF9 to SF11 combined, five readings) keeps the price at 204 to 205 and the gap at 1,912 to 1,914, the tightest 36 per cent of a bin from its edge (asserted) | same call |
| SF10 | recovery's figure | the change in the share of declined first charges recovered, on this winter's declines (92) | the change in the collected share of first charges (92) | same call, same bin (asserted) | same call |
| SF11 | the channel mix's figure | last winter's channel shares at this winter's paid rate by channel (105) | at within-state keep rates (105) | same call, same bin (asserted) | same call |
| SF12 | trialists who played nothing | in the no-runway state | left out of the split | same call, slate within its bin (asserted) | same call |
| SF13 | the volume each figure is priced at | this winter's trials | last winter's | same call | the programme sheet's "this winter's trials" |
| SF14 | the waterfall's start | last winter's rate at this winter's trials | last winter's paid conversions | same call | the prompt's chart sentence |
| SF15 | the share still subscribed when the trial ended | of the winter's trials | of the trials that played | same call (asserted, stage shares are the prompt's) | the prompt's "share of each winter's trials" |
| SF16 | an episode's English and French versions | one episode, one season | two | same call (asserted) | the release calendar lists both identifiers on one row |
| SF17 | trials started 25 to 31 October 2025 (first charge in November at the new price) | in neither window | in this winter | same call | the standard's start-date windows |
| SF18 | the ask's average number of episodes | over every trial started in the month, those that played nothing included (4.93 in February) | over the trials that played (5.21) | no effect on the call; the ask figure moves several bins, closed by the ask's own subject (asserted) | the prompt's "for the trials started in each month ... the average number of episodes played during the trial" |
| SF19 | the funding criterion | the one programme with the highest valuation: (C) | paid conversions per dollar of the sheet's Cost column, (D) at 1.24 per CAD 1,000 against (C)'s 0.80; net value on a lifetime value the pack does not hold, none | (D) or none: the call moves, so the reading is ruled out by a filed line | the programme sheet's Funding line, "the one with the highest valuation; none this cycle only if no programme's cause cost the 2025-26 winter's trials paid conversions" (asserted: the line in the shipped sheet, (C) under it, the per-dollar (D) recorded) |

## Ladder

| Rung | Construction | Names | Slate | Price | Recovery | Channel | Dies to |
|---|---|---|---|---|---|---|---|
| 0 | year-on-year fall, segment cuts, catalogue control, event study | (A) | 0 | 2,519 | 0 | 0 | the fall holding within each runway state at about a point and a half |
| 1 | rung 0 with recovery and channel mix netted | (A) | 0 | 2,318 | 92 | 109 | the same |
| 2 | content band from the register and titles (sign-up title, its age, the most-watched title) | (A) | 294 (184 to 307 over redraws) | 2,030 | 92 | 103 | the catalogue control contaminated: last winter's catalogue sign-ups played an airing season |
| 2b | the sign-up season's own runway (register against calendar) | (A) | 581 | 1,737 | 92 | 109 | the same: what a trialist plays, not where they signed up, decides |
| 3 | each trialist's played seasons against the calendar at their day 7 | (C) | 2,117 | 201 | 92 | 109 | golden |

- Position: on rung 0 to 2b the golden (C) is second or fourth; the winner (A) leads by 3.0 times (2b) to 25 times.
- Margin: golden (C) 2,117 against runner-up (A) 201, 10.5 times; gap 1,916.
- Dominance: every rung below 3 names (A); only rung 3 reverses. Every correction walks one way (the price shrinks)
  until the decisive move.
- Pricing sequence: (1) the residue the filed WHAT leaves is the attribution of the fall to causes, a method, not a
  knob; (2) the call must move about 1,900 from (A) to (C), and the runway shift alone can carry 2,117 (70.2 per cent
  of last winter's trials had runway, at a 17-point paid gap); (3) the one-group-by routes on any register column
  explain at most 9 per cent of the fall (sign-up title) and land (A); (4) the slate's standard error from last
  winter's 12,600 and 5,350 trialists in the two states is about 110 conversions and the price's about 150, against a
  1,916 gap; (5) the call is a verdict on one candidate far from its boundary; (6) and (7) do not apply; (8) the reflex
  sweep runs as code (`generator/screens.py`, 20 of 20 redraws on (A)).
- Redraws (20, final world): slate 2,077 to 2,145, price 196 to 234, recovery 89 to 95, channel 92 to 122, fall 2,468
  to 2,563, the register-only route 484 to 667 and (A); the call (C) in 20 of 20.

## Closure table

| Axis | Reading here | Closure |
|---|---|---|
| 1 Population | a winter's trials by start date | filed in the conversion standard (Toronto time, 1 November to 31 January); SF1, SF17 |
| 2 Unit of account | a trial | filed (one account's free week); the register's twin rows of 9 to 19 June lie outside both windows, and wherever a reader starts the old platform's Toronto clock on 9 June one set of 790 copies drops (C1, asserted H1) |
| 3 Attribution window | start date decides the winter | filed; records clear of both boundaries asserted (no trial within a minute of a window edge) |
| 4 As-of dating | the extract of 27 February 2026, every January trial matured | filed in the standard (retries end within seven days of the first attempt); asserted |
| 5 Version basis | the release calendar as released | one version shipped; no preliminary file |
| 6 Denominator | the winter's trials | filed; SF15 |
| 7 Weighting | the split priced at this winter's volume and last winter's gap | SF7, SF13; C1 |
| 8 Window length | seven-day trials | filed in the standard |
| 9 Boundary inclusivity | a release after the trial's end | SF5 asserted at the second and at the local day; no release falls within a minute of a trial end in the windows |
| 10 Rounding path | each figure rounded once at the end | prompt's rounding sentence; mid-bin asserted |
| 11 Tie-break | none needed | gap 1,913 |
| 12 Maturity and censoring | every January trial matured by the extract | asserted (last attempt before the extract) |
| 13 Order of operations | the split before the within-state changes | SF8, SF9; the four and the remainder sum to the fall (asserted) |
| 14 Row order | none | C1, every figure computed by group |
| 15 Duplicate resolution | the player's twice-written rows | exact duplicates; same call either way (asserted) |
| 16 Identity normalisation | legacy content and account numbers before the cut-over; the subscription a plan change opened | the shipped crosswalks map every one (asserted); the first charges no file links to a trial are exactly those on subscriptions no file names, 938, matched alike under every window, order and reuse rule (C1, asserted D7f to D7j) |
| 17 Netting against gross | the price net of the channel mix | SF8 |
| 18 Dimensional units | cents with tax against dollars before tax | the conversion outcome is a count; units move no graded main figure (asserted) |
| 19 Code and status semantics | approved, declined, CAPTURED, REFUSED | each processor's own codes; asserted one reading |
| 20 Integerisation | counts are whole | C1 |
| 21 Clause scope | the standard's sentences apply to every trial | filed |
| 22 Forward window contents | the 2026-27 winter | the call faces forward on the measured winter's causes; the programme sheet names the measured window |

## Literal reader

Executing the prompt, the conversion standard and the programme sheet word for word fixes the trials, the outcome, the
windows, the comparison and that each programme is valued at the paid conversions its cause cost this winter's trials,
the four and what none addresses accounting for the fall once; nothing filed says how to split the fall, so the reader
must choose a construction, and every construction that conditions on whether a played season still had an episode to
come at the trialist's day 7 (any instant, any play floor, SF4 to SF7) files (C) at 2,062 to 2,117 with (A) at 201 to
205, while every construction that skips it books the shift to the price and is refuted by the within-state change the
data show; no filed sentence reads to another answer. The programme sheet's Funding line files the selection, the one
programme with the highest valuation and none only if no programme's cause cost the winter's trials paid conversions,
so the sheet's Cost column ranks nothing (per dollar it would name (D), SF19).

## Oracles

- The catalogue sign-up control (trialists who signed up on a finished season): falls 11.4 of 14.6 points, confirming
  the price on the wrong path; it ties under neither basis because last winter's catalogue sign-ups played an airing
  season. Not an oracle: it confirms the easy route.
- The event study: steps of 16.2 (price date) and 16.8 (finales) points, a day apart; confirms both, separates neither.
- The cancellation survey (a distractor): the price reason climbs after 1 November; confirms the wrong path.
- No control ties only under the golden; no published figure, KPI pack or prior review ships.

## Ask sheet

Rubric sum (39 criteria): the call (1), each programme's paid conversions (4), runner-up (1), gap (1), the stage shares
for the two winters (6), the waterfall's named parts (start, the four cause bars, end: 6), the two files (2), and the
ask (18).

**Ask M: the months between the winters.** For the trials started in each month from February to October 2025, the
share that paid (per cent, one decimal) and the average number of episodes played during the trial (one decimal, over
every trial started): 18 figures. H18 home: a component of the call's case (conversion and viewing held between the
winters, so the fall starts in November), on rows outside the main population (trials started 1 February to 31 October
2025). Use: the growth team's base rate for the plan. Realism: the cut-over year's records as each system wrote them.

- The WHAT, filed in the organisation's voice (conversion standard v3): paid (section 4: the first monthly charge
  collected by the first attempt or a scheduled retry; a charge after the last retry does not convert; a plan change
  during the trial, including one in its last minutes, does not end it, and its first charge is that of the
  subscription and plan the trial ends on); an episode played (section 5: any of it streamed between the trial's start
  and end, whether the viewer started it or the player moved on to it from the episode before, partway or in the
  credits, once a trial in either language). Each handling reproduces one figure exactly; the ask's own subject fixes
  the denominator (SF18).
- Primary 1, D7 (the true key elsewhere), block = the nine paid shares: the plan-change launch (subscription platform
  7.2, 3 February 2025, in the product release log) opened a new subscription on each change until the flow was rebuilt
  (8.4, 14 October 2025); the old platform's changes before the 9 June cut-over never reached the plan-change log, and
  the apps' changes until 14 October did not either. Remedy: match each first charge no file links to a trial to the
  trial without a charge whose end most closely precedes its first attempt, in the provinces its tax rate names (a
  reconstruction across two systems with no shared key). Measured on the cut pack: all 938 unlinked charges matched,
  each to its own trial, the same match within 10 minutes, one hour and six hours, consumed earliest or latest first,
  with or without a trial taken twice. While a change opened a subscription, a trialist's second change went through
  the kind of surface the first did (a subscription opened in an app was managed in the apps), so a trial's changes are
  all logged or none is: every unlinked charge sits on a subscription no file names, and "a first charge no file links
  to a trial" and "a first charge on a subscription no file names" are one set of 938 (checks.py D7f to D7j). Wrong paths: the register's
  subscription only (every month 15 bins low or more); the logged chains followed (7.4 bins low at the least, October).
  Evidence: the processor exports with the register's trial clocks.
- Primary 2, D6 (a row at another grain than its name), block = the nine episode averages: the smart TV app's new
  player with autoplay (3.0, 8 February 2025) wrote one row per autoplay run, the episode named and the run's minutes,
  until its player update (3.4, 27 October 2025). Remedy: expand each such row into the season's following episodes as
  far as the minutes reach on the release calendar's runtimes (a recorded allocation weight); the other apps' rows
  show the same back-to-back runs one row an episode. Measured: the expansion reproduces every trial's episode count
  exactly; one row one episode (or minutes capped at the runtime) misses every month by 3.9 bins at the least
  (February). Evidence: the viewing log.
- Hazards (seen, repaired right by a careful reader): the old platform's twice-written web and phone sign-ups of 9 to
  19 June in Toronto time stamped as UTC, beside TV and tablet sign-ups written only there (June's share and average);
  its mirror of web and phone sign-ups was switched on at 04:00 on 9 June, two hours after the new platform opened, so
  a reader who starts the Toronto clock at the rows' written date, at Toronto midnight or at the first new-platform
  row less four hours drops the same 790 copies and prints every ask figure the golden's (checks.py H1);
  the legacy account and content numbers (the crosswalks); the player's exact duplicate rows; the second processor's
  local time with an offset.
- Pin test: the asking sentence fixes the months (start date), the outcome (paid, the standard's) and the unit (per
  trial started); the standard files the WHAT of paid and of an episode played; the devices sit in which subscription a
  charge belongs to and how many episodes a row covers, which no sentence names.
- Main population zero-counts, asserted by count from the shipped rows (checks.py S1 to S5): unlinked plan-change
  charges on winter trials 0 (938 matched trials, none in a winter); session rows of winter trials 0 (none of the
  20,009); twin rows in either window 0; never-played winter trials hold no viewing row, so the played share is the
  same with the session rows expanded or not; session rows only from the smart TV app between its two releases.
- Referee: none; every route completes and reconciles to its own totals.

| Cracker sheet, on the cut pack (the pack digest heads ceiling.py's output) | Paid shares (D7) | Episode averages (D6) | Kept of 18 | Verdict |
|---|---|---|---|---|
| Cracker: lands the call, runs the battery, follows the logged chains, one episode a row | 0 of 9 | 0 of 9 | 0 | miss |
| Full includer: every file and every stated fact (each retry schedule to the letter, the release log's dates); notices the charges no file links and the smart TV rows longer than their episode, and with no file naming their trials or episodes counts neither | 0 of 9 | 0 of 9 | 0 | miss |
| No-repair: every row as it stands | 0 of 9 | 0 of 9 | 0 | miss |
| Mirror: stops at rung 2 on (A), the cracker's ask route; keeps the six stage shares of the thirteen main criteria | 0 of 9 | 0 of 9 | 0 | miss |

- Measured exposure (ceiling.py's reference rows, never the gate): the strong reader, who also matches every unlinked
  charge to the nearest earlier trial end in its tax group and walks the smart TV rows through the following
  episodes' runtimes, keeps 18 of 18. Two partial handlings reach from stated facts alone: counting each unlinked
  collected charge in the month of its first attempt less the seven-day trial (standard, section 2) keeps 9 of 9 paid
  shares; reading a long smart TV row as its minutes over the named episode's runtime, rounded up, keeps 2 of 9
  averages. The paid block holds only while the unlinked charges go unnoticed (noticing them is most of the remedy);
  the episode block holds against its shortcut. Reported with the hand-off.
- Mirror leakage: 0 per cent of ask weight (measured).
- Pair ceiling: 34.8 (measured: landed call 45.0, best miss 24.5; the full includer keeps 0 per cent).
- Measured by: generator/ceiling.py (shares no code with the generator; scores the cracker, the full includer, the
  no-repair reader and the mirror on the cut pack against figures.json, and prints the strong reader and the two
  partial handlings for reference).

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
- 2026-11-04, stage 2 (resumed session), the coded first-look reader skipped a readable cell through a 3 per cent floor:
  434 of this winter's trials signed up on Northern Lines, the one weekly original airing that winter, and fell under a
  point against 11.6 for the rest. Rewritten with a 200-trial floor, every content band and a decomposition rule; and a
  viewing-against-calendar band at sign-up reproduced the golden (2,026 against 2,005), so that band is the decisive
  family read at another instant, not a runway-free proxy, and the reader does not run it.
- 2026-11-04, stage 2, Northern Lines also forked the split: last winter's and this winter's runway gaps differed (6
  against 19 points among airing sign-ups), so the register-only sign-up-season runway filed (C) at this winter's gap
  (1,178 against a residual price of 1,041) and (A) at last winter's, a weighting fork on a cheap route. Removed: nothing
  new airs from 1 November 2025 to April 2026 (Gravel & Gold slipped), the gap exists only in last winter, and the
  register-only route files 556 and (A).
- 2026-11-04, stage 2, plays of a fixed completion law (beta 4 and 1.6) made a 90-per-cent play floor file 627 and flip
  the call: completion now depends on the season's phase (an airing season's episode watched through 98.5 per cent of the
  time, a catalogue one 72), Harbourlight S2 ends the night last winter's window opens and Marrow Creek runs to 14
  February with Quillon premiering that day, so the state reads the same at sign-up, during the trial and at day 7, and
  the family closes to 2,084 to 2,117.
- 2026-11-04, stage 2, ask devices screened and dropped: web sign-ups sending a series code that the content
  crosswalk maps to the season current at the cut-over (the filed mapping reads to another answer on the ask, an
  official decoy, and the WHAT that closes it, that a series page shows the latest season, spends it); the Android TV
  app's missing plays recovered from the licence server (found by reading that file, which also recovers the smart TV
  session episodes, so two devices shared one evidence file; the licence server is not shipped); a first-week premiere
  ask (only the June twin rows reached it, one season of five); the twin rows themselves are kept as a hazard.
- 2026-11-04, stage 3, the cut-over's register read two ways: an old-format row stamped between 02:00 and 06:00 on 9
  June could be a pre-cut-over trial in true UTC or a post-cut-over sign-up in Toronto time stamped as UTC (the verifier
  re-timed one pre-cut-over trial and left its plan-change charge unmatched). The cut-over now carries its maintenance
  pause (no sign-ups from 22:00 to 02:00 Toronto, 8 to 9 June 2025), so the two clocks cannot overlap.
- 2026-11-04, stage 3, thirty-one graded one-decimal figures re-rolled their bins at every world change (June's paid
  share at 1.6 per cent of a bin, two months on one trial count). A bin guard at the end of the simulation moves the
  fewest records of the months between the winters (a declined first charge recovered or not, one catalogue play more
  or less, one last-minute sign-up into the next ask month) until each monthly figure clears 22 per cent of its bin;
  no winter trial is touched and every figure is computed forward from the records. Its first version oscillated
  across an edge (direction chosen per step); the direction is now fixed per month toward the bin's centre.
- 2026-11-04, stage 3, the session device first moved February's episode average 2 bins, the app release falling a
  week into the month: a run of two or more episodes now goes to the living-room set with probability 0.35, and every
  month moves 3.9 bins or more.
- 2026-11-04, stage 3, autoplay drawn independently of completion put a following episode after a partial play,
  which made a session's minutes ambiguous to expand: autoplay now follows only a complete play (97 to 100 per cent of
  the runtime, the player cutting at the credits), and a season's early plays move as one block after the sign-up
  season's first play, so a run stays contiguous.
- 2026-11-04, stage 3, two invented series titles (North Shore, Quarry) are real television titles (house fix H21):
  renamed Ashby Shore and Cutstone; figures.json byte-identical after the rename.
- 2026-11-04, stage 3, the prompt's "stage by stage" list read two denominators for the share still subscribed (the
  winter's trials or those that played, 52.7 against 53.4 per cent): the prompt now names the winter's trials (SF15).
- 2026-11-04, stage 4 round 1 (the judge's FIX_NOW on the ask's June to October paid shares), plan-change chains that
  mixed an app change the log never received with a logged web change: 46 log rows started from a subscription
  nothing else names (21 of them charged), so "a first charge no file links to a trial" read two ways, every charge no
  register subscription reaches through the log (965) or only those on subscriptions no file names (944), and the
  narrow reading left 21 trials of July to October unpaid. Replaced in the world: while a change opened a
  subscription, the subscription was managed where it was opened, so a trial's changes all reached the log or none
  did; both readings are one set of 938 and print the golden in every month (D7f to D7j). The charges now draw on
  their own random stream, so the log's length moves no attempt.
- 2026-11-04, stage 4 round 1, the same finding's June cell had a cause the chains do not reach: the judge started the
  old platform's Toronto-stamped rows at Toronto midnight (04:00Z as written), kept as trials the 8 web and phone
  copies written between 02:00 and 04:00Z, and printed June at 52.1 (52.087) against 52.2. Closed at the pack: the old
  platform's mirror of web and phone sign-ups starts at 04:00 on 9 June, so the written date, Toronto midnight and the
  first new-platform row less four hours drop the same 790 copies and print every ask figure the golden's (H1); the
  written-date reading still re-times the 26 true-UTC rows of 20:00 to 22:00 on 8 June and prints June at 52.164.
- 2026-11-04, stage 4 round 1, the June closure first tried in the world, an eight-hour cut-over pause (20:00 to 04:00
  Toronto) so that no old-platform row is written between 00:00 and 04:00Z: moving the paused sign-ups re-ordered the
  trials and desynchronised the plays' random stream, and six ask figures moved, four of them in months the fork never
  touched (the February, March, August and September episode averages). Reverted; the mirror's start is a pack-level
  change that moves no draw.
- 2026-11-04, stage 4 round 1 (the judge's Gate E note), the programme sheet's "one programme from the subscriber
  growth budget, or none this cycle" filed no criterion while its Cost column invites paid conversions per dollar,
  under which (D) leads: the Funding line now files the WHAT in the sheet's own voice (the one with the highest
  valuation; none only if no programme's cause cost the winter's trials paid conversions), SF19.

## Pre-ship check

Stage 4 round 2 and ship, 2026-11-04, final cut target.zip 08a813d0 (rebuilt twice on the merged branch, byte-identical):

- The 10/10 rules re-read against the built pack: the decisive step is still setting each trialist's played seasons
  against the release calendar at their own day 7 (a season still to come), analytical, and no field, rule or filed
  sentence performs it; the mess is still Layer 1 only (the 9 June migration and its Toronto-stamped mirror, the
  crosswalks, two processors, the plan-change subscriptions, the autoplay-run rows, the player's duplicates).
- Judge round 1 (order kept): DETERMINISTIC, FIX_NOW on the ask's June to October paid shares; its blind derivation
  filed (A). Closed in the world (no plan-change chain mixes a logged and an unlogged change; the old platform's web and
  phone mirror begins at 04:00 Toronto), no graded figure moved.
- Judge round 2 (order kept): DETERMINISTIC, APPROVE, no fix. Gate F high: its blind derivation again filed (A) (a
  14-day recent-release proxy put about 500 on the slate). Gate G decomposition_attribution, analytical_non_defect, no
  surface-read dependency, no sole data defect. Gate H domain pass, layers pass, decisive step analytical. Every main
  figure, the nine paid shares and the nine episode averages reproduce; both readings of the unlinked charges select one
  set of 938. Its residual note (a gross price near 400, gap 1,700) is SF8, closed by the programme sheet's sentence that
  the valuations account for the fall once, asserted; the call and the slate's figure do not move.
- Leak reader rounds 1 and 2: no decisive-step sentence, no ranking or helper file, nothing reads as the answer, the
  decisive step analytical; round 2 reads the Funding line as settling the choice by valuation and naming no method.
- Coordinator's rulings:
  - Stage 3's flag (one ask, a strong reader keeps 18 of 18): no second ask. Both primaries are reconstructions no
    sentence states, the prompt sits at 913 of 1,000 characters, and no third family survived the filed-WHAT and
    shared-evidence rules.
  - The fix pass's flag 1: the D7 block is weaker than the Ask sheet claimed (a reader who finds the unlinked charges
    and counts each in the month of its first attempt less seven days keeps the nine paid shares without the one-to-one
    match). Accepted: the D6 block holds (minutes over runtime keeps 2 of 9), the pair stays under 70 unless both top
    responses crack both devices, and any change after the one allowed re-judge would move ask figures.
  - The fix pass's flag 2 (SF8's gross readings, price 300 and gap 1,800): closed by the once-only sentence, asserted,
    and read the same way by both judges.
  - The fix pass's flag 3: the frozen ladder's raw values (201, 109, 1,916) differ from the build world's (204.75,
    105.18, 1,912.6) inside the same printed bins; the ladder stays as frozen.
- Gates re-run on the final cut: `checks.py` 70 checks, 0 FAIL; `verify.py` 38 figures; two builds byte-identical
  (08a813d0); `figures_check.py` 67 figures, 0 absent; `precut.py` 61 checks, 0 FAIL, 0 WARN; `voice-check.py` PASS;
  `ceiling.py` cracker, full includer, no-repair and mirror 0 of 18, pair ceiling 34.8; `leak.py --asof 2026-03-09`
  REVIEW, 0 LEAK (the four answered lines); `guard.py heart` WARN, no BLOCK, nearest driver 0.08 (task500 v2);
  `guard.py surface` 3 promoted pairs on card axes (task402 back to back on the gap and decision type, task306 on gap,
  pattern and decision, task271 on gap, pattern and Gate G), each answered on the card's `differentiation`, no surface
  tell.
