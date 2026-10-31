# task235 design note

Architecture 2 (re-rooted 2026-10-17 after the determinism judge's SEND_BACK of architecture 1, whose alert list graded
each build's tracking loss at two decimals though nothing shipped said how the purchases still open at the run are
valued, and read paying players off account links no file called incomplete), wave 2, seed DQ08 (which reporting areas
get a completeness alert, when recent weeks are still filling in): the seed's decision and quantity only, the pitfall
re-found from the data under the 10/10 rules. Architecture 2 keeps the world and the decisive step, grades only what the
records force (each build's alert, the losses known outright, iOS 7.42.0's floor), files the outcome for an event still
missing at the run and has the account links say they are not a full register; the asks become each build's paying
players and gross bookings per paying player. Product Analytics, metric definition and measurement science, Data Quality Monitoring & Alerting. Fogbell Games, a Dublin
studio, sells coin packs, boosters and a monthly pass in its match-3 game Kittiwake Cove on iOS and Android. Every
Monday its data quality lead runs the tracking-quality check: each production build's tracking loss, the share of its
store-verified purchases whose `purchase_completed` event from the game's analytics SDK never reaches the warehouse,
and an alert on every build above 2 per cent, which takes the build's purchase events out of the experiment readouts
and the revenue funnels, opens a P1 bug for the SDK team and holds a staged rollout where it stands.

## Draw

Card `cards/task235.json` (architecture 2, registered 2026-10-17, architecture 1 in its lineage with its fate). Guard
verdict WARN, one line: `repeat.question_form` against task234 v2 (which) is the decision's own form, a set of builds.
The slot's own lineage is cleared by the card's `task235` differentiation line (the decisive step unchanged, the graded
figures and the account links' note new). `test.same_puzzle_older` (task445) and
`test.same_driver_older` (task445, task459) are cleared by the card's differentiation lines: neither completes a missing
amount from a class change or reads a rate at a committed level; this build decides item by item whether a missing record
is due yet.

- **Pairing.** Product Analytics / metric-definition-measurement-science, serving Data Quality Monitoring & Alerting
  (the domain index lists this task type under DD and DQ). The seed sits in Epidemiology & Public Health; that pairing
  is banned against task234 (the last three builds), and the seed's quantity, what has arrived against what should
  have by now while recent periods fill in, is native to product telemetry, where the late item is a client event
  queued on a phone and the record of what should have arrived is the store's server-side purchase.
- **Niche.** The game's analytics SDK, Tern, logs `purchase_completed` on the phone into a queue it uploads when the
  game starts and while it is in the foreground; a player who leaves the game in the seconds after buying leaves the
  event on the phone. The studio's purchase service verifies every purchase with the store as it happens, and its
  session service records every time a phone opens the game. The check runs on Monday 9 November 2026 over purchases
  made from Monday 12 October to Sunday 8 November (Irish dates), so the last days' events are still arriving.
- **The call.** For each of the twelve production builds (iOS 7.38.2, 7.39.1, 7.40.0, 7.41.0, 7.41.1 and 7.42.0;
  Android 7.38.1, 7.39.0, 7.40.2, 7.41.0, 7.41.3 and 7.42.0), alert or not. The 7.42.0 builds moved to SDK 5.0.1 and
  have been in a staged rollout since Thursday 5 November (30, 55 and 80 per cent of automatic updates; 100 per cent
  planned for Wednesday 11 November). On iOS, 5.0.1 sends `purchase_completed` the moment StoreKit reports the
  transaction; on Android its uploads run through WorkManager, which holds a batch the game leaves behind. Players who
  switch off automatic updates stay on the 7.38 and 7.39 builds, and older iPads stay on iOS 7.40.0; many come back
  to the game a week or two apart.
- **Shape.** 10, a scorecard against a threshold: every build's tracking loss against the 2 per cent line. Decision
  designation_set, answer set_of_items, question form which.
- **Strategy.** maturity_censoring with G12 decisive (a missing event is a non-answer until the phone that made the
  purchase has opened the game again), G14 supporting (the loss read over the purchases whose chance has come, the
  rest completed at the build's own share of resolved gaps that stayed missing, pattern E's form) and G2 (the chance
  belongs to the phone, not the account); Gate G method_or_model_selection (which way of telling a lost event from a
  late one the data support); calibration none; context artifact register (the metrics catalogue); layer 2 family
  estimation_fit, pattern own:loss-conditioned-on-the-delivery-chance.
- **Forum, event, organisation.** line_manager_or_team (the data quality lead raises the alerts in the analytics team's
  Monday run; no committee; redrawn from operations_desk after the pull brought task154's redrawn forum),
  launch_or_rollout (7.42.0's staged rollout goes to 100 per cent on Wednesday 11 November unless held),
  software_or_platform (a game studio).
- **People** (`guard.py names --geo "Ireland" --seed 235`): Amelia Seery, data quality lead, who runs the check and
  raises the alerts; Padraic Cormick, SDK lead; Darragh Boylan, release manager.
- **Deliverables.** `tracking_loss_alerts_2026-11-09.csv` (one row per build: platform, version, build number, alert,
  paying players, gross bookings per paying player in euro) and `tracking_loss_by_build_2026-11-09.png` (each build's
  loss against the 2 per cent line).
- **Data-native sentence.** A purchase event leaves the phone only when the game starts or is in the foreground: sent
  within seconds if the player stays, otherwise kept in the phone's queue until that phone next opens the game, which
  for the weekly players on the old builds can be a week or two; the session service records every opening the moment
  it happens, so whether a missing event is late or lost is known purchase by purchase, while any reading by age
  charges the weekly players' waiting events as losses, cannot judge a build four days old, and swaps the two 7.42.0
  builds, because the new SDK made events wait less on iOS and more on Android.

Sources, one line each (what it teaches; how this build differs):
- Client pattern metric-definition-measurement-science/2 (ratio of sums against mean of ratios: the metric follows its
  stated unit): here the unit is the purchase whose delivery chance has come; a pooled settled share is the wrong unit.
- Client pattern retention-cohort-lifetime-value-modeling/1 (young cohorts are censored, not churned): the same
  censoring logic turned item by item; the censoring time is each phone's next session, read from another system.
- Seed DQ08: the decision and the quantity only; its decoy-era design is not read.
- Client-server event reconciliation as analytics teams run it (server-side purchases as the record of truth, client
  events matched by transaction id); mobile analytics SDKs that persist a queue and upload in batches; WorkManager's
  deferred uploads on Android against StoreKit's transaction callback on iOS.
- Spent on this objective (`guard.py mechanisms`): task228 (a ratio metric's variance at the randomised unit), task229
  (a daily mean through a convex rating), task230 (net coding bias of a late channel), task231 (the closed share of
  silent units from rounds the register caught up with), task232 (transmission from delayed, mixed outcomes), task233
  (a missing-not-at-random departure on the odds scale), task234 (a source's output read from a share a loss cannot
  move). None judges a missing record by its own sender's next contact.

## Default path

1. Read the metrics catalogue's tracking-quality entry: a build's tracking loss is the share of its store-verified
   purchases made in the game from 12 October to 8 November (Irish dates) whose `purchase_completed` event never
   reaches the warehouse, an event that has not arrived by the run lost only if it never will; alert above 2 per cent.
2. Take the purchase service's validations, keep transaction kind purchase in Production with purchase type standard
   (pass renewals, sandbox and licence-tester purchases out), map each build number through the build register, and
   match each purchase to its event by store transaction id, the SDK's duplicate uploads and restored events
   collapsed.
3. Events arrive late (87 per cent within a minute, 95 per cent within a day, the slowest after 17 days), so count a
   purchase as lost only when its event is still missing seven days after the purchase; each build's loss is its
   unmatched purchases over its purchases at least seven days old (or over all its purchases, the younger ones counted
   not yet lost: the same five builds alerted).
4. Alert every build above 2 per cent.

Ends on: five builds alerted (Android 7.41.0 and four old builds whose weekly players have not opened the game again,
Android 7.38.1 at 3.07, iOS 7.38.2 and 7.39.1 at 2.85, iOS 7.40.0 at 2.77 per cent) and the two 7.42.0 builds left
without a figure (no purchase seven days old) and not alerted, so iOS 7.42.0, which loses events, is missed: 5 of the
12 builds wrong.

Golden: alert Android 7.41.0 (6.34 per cent, none of its purchases still open) and iOS 7.42.0 (at least 3.10 per cent,
8 of its purchases still open), and no other build.

## Stump sentence

A competent solver counts a purchase as lost when its event is still missing seven days later and files 5 of the 12
builds wrong (Ends on: Android 7.41.0 and four old builds alerted, iOS 7.42.0 missed for want of a week-old purchase);
the step that lands it there is judging a missing event by its age instead of by whether the phone that made the
purchase has opened the game since, the only moment the event can leave it.

## Three rules

- **Task type:** product-analytics / metric-definition-measurement-science, which serves Data Quality Monitoring &
  Alerting; the measurement here is a build's purchase tracking, the client-side instrumentation reconciled against the
  store's server-side purchases.
- **Domain test:** the quantity that decides is each build's purchase-tracking loss, settled for the purchases whose
  phone has opened the game since and bounded for the rest by the build's own resolved gaps, the reconciliation
  product analysts run on SDK telemetry against server-side truth; it rests on how a mobile analytics
  SDK delivers (a queue on the phone sent when the game starts and while it is open; StoreKit's callback on iOS 5.0.1,
  WorkManager on Android 5.0.1) and on the backend's session handshake.
- **Swap:** "which wards get a charting-loss alert, judged on the share of admissions whose nursing note never reaches
  the record" has no queue on a phone that empties only when the game is next opened, no session service, no store
  receipt and no SDK whose new version changed the wait in opposite directions on two platforms; the analysis that
  decides here has nothing to act on.
- **Layer 1:** pass renewals the store makes without the game and sandbox and licence-tester purchases among the
  verified purchases (the purchase service records them all); duplicate SDK uploads and restored transactions (the SDK
  retries a batch whose acknowledgement is lost; the game logs a restored pass again); device clocks skewed against
  the warehouse's receipt time; build numbers in the purchase service against version names in the SDK (two systems);
  Irish dates against UTC timestamps with the end of Irish Summer Time inside the window. Nothing is placed to be
  caught.
- **Layer 2:** estimation_fit, censoring: a missing event is censored until its phone's next session, so the loss is
  read over the purchases whose chance has come and the open ones completed at the build's own resolved share; a settle
  window, a pooled arrival curve, an age-matched comparison or the account's next session each mismeasure it.
- **Decisive step:** judging each missing event against the next session of the phone that made the purchase, read from
  the session service, and measuring each build's loss over the purchases whose phone has opened the game since, the
  few still open counted at the build's own share of resolved gaps that stayed missing.
- **Not semantics:** the default path reads every field, code and status right (renewals and testers out, duplicates
  and restores collapsed, build numbers mapped, the window in Irish dates) and still files 5 wrong builds; what it gets
  wrong is when a missing event becomes a loss, which no field states.
- **Not rule application:** the catalogue files the loss as the share of purchases whose event never reaches the
  warehouse, says an event that has not arrived by the run is lost only if it never will, and files the 2 per cent
  line; no rule says how to tell a lost event from a late one, and executing every stated rule still leaves that
  choice.
- **Analyst test:** a strong analyst who cleans the data and reads every rule, then counts a purchase as lost when its
  event is still missing seven days later, files 5 of the 12 builds wrong (Ends on: Android 7.41.0 and four old builds
  alerted, iOS 7.42.0 missed); a fourteen-day window still misses iOS 7.42.0, a pooled arrival curve files 6 wrong, and
  the next session read by account instead of by phone files false alerts on iOS 7.38.2, 7.39.1 and 7.40.0.
- **Estimand:** the metrics catalogue's tracking-quality entry (KC-DQ-04 s.2 to s.5, in the pack) fixes the population
  (each production build's store-verified purchases made in the game from 12 October to 8 November 2026, Irish dates),
  the outcome (the purchase's event never reaches the warehouse; purchases made shortly before the run count like any
  other, and an event that has not arrived by the run is lost only if it never will), the unit (the purchase), the
  window and the comparison (above 2 per cent, unrounded).
- **No decoy:** nothing is planted: no memo, dashboard export, draft list or stakeholder figure states a loss or an
  alert; the two faulty builds lose events through their own code paths, recorded only as missing events; the SDK notes
  describe delivery as SDK release notes do.
- **No certified replay:** no certified or published loss exists for a method to reproduce.
- **Lesson:** a record missing from a feed is a non-answer until its sender has had its next chance to send it, and that
  chance can sit in another system's log, item by item; no build on file judges a missing record by its own sender's
  next contact.

## Survivor anatomy

Actor: the deciding property is whether the phone that made a purchase has opened the game since, a relation between the purchase's device and its later session starts in another service's log; no column in any file holds it.

Link: each missing event is read against its own phone's next session start, joined by device_id from the purchase service's validations to the session service's starts; the catalogue names no session and the SDK changelog says only when the phone's queue uploads, so no sentence invites the join.

Reflex: the field's settle window, a purchase lost when its event is still missing seven days later, is the default path (rung 0) and files five builds wrong, Android 7.38.1 and 7.41.0 and iOS 7.38.2, 7.39.1 and 7.40.0 alerted and the 7.42.0 pair left unjudged.

Back-test: the textbook check passes: the pooled arrival curve flattens within a window of eleven days or more, and a window that long files Android 7.41.0 alone (rung 1), so a window checked against the curve looks safe while the late arrivals it waits for are the phones that have not opened the game.

Second use: every file the decisive step reads has its own use: the session log also carries Ask A's guest sign-ins, the validations are the record of purchases (s.2), the warehouse events the tracked side (s.3), the SDK changelog the developers' release history.

Shock: the correction reads as ordinary delivery delay on every build, and the golden pair is not an interval of any shipped statistic: on the share of purchases whose event is missing at the run Android 7.41.0 is second (6.34) and iOS 7.42.0 fourth (5.57), with Android 7.42.0 first (9.24) and Android 7.38.1 third (5.76) both left out.

Pins: KC-DQ-04 s.2 to s.6 file the WHAT (the purchases, their events, the loss as the share whose event never reaches the warehouse, "lost only if it never will", the 2 per cent line compared unrounded); no filed sentence names a session, a phone's next start or a settle window.

## Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control
or corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or
half of a reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 (default) a purchase lost when its event is still missing seven days later: 5 wrong | s.4 says an event not arrived by the run is lost only if it never will, which invites a maturity window | received_at beside purchased_at gives each event's lag | yes, a maturity window | none | no | one filter and a ratio | readable |
| 1 a longer window (eleven days or more): Android 7.41.0 alone, iOS 7.42.0 missed | as rung 0 | the lag's long tail (17 days) | yes, wait for the tail | none | no | one filter and a ratio | readable |
| 1 a pooled arrival curve completing each build by purchase age: 6 wrong | s.4 as above | the lag by age | yes, chain-ladder completion | none | no | a ratio by age | readable |
| 1 a short window for the 7.42.0 builds beside a long one for the rest, or the 7.42.0 builds against same-age purchases of the platform's other builds: Android 7.42.0 alerted at every window up to 2.5 days, iOS 7.42.0 cleared by the age-matched comparison | none | the register's release dates | yes, judge a young build at the age it has | the other builds' same-age purchases, which refute nothing here | no | a ratio | readable |
| 2 each missing event judged against the account's next session: false alerts on iOS 7.38.2, 7.39.1 and 7.40.0 | none: the SDK notes put the queue on the device | the session log carries account_id | yes, has the player come back | none | no | a join and a ratio | readable |
| 3 (decisive) each missing event judged against the next session of the phone that made the purchase, the loss settled for the purchases whose phone has opened the game since and the open ones bounded by the build's own resolved gaps | no sentence links a missing event to the phone's next session or says how to tell when it becomes a loss; the SDK notes say what release notes say (the queue is kept when the game closes and uploaded when it starts) | no column marks a purchase as due; the session log is the session service's full export of every phone's starts | no: the reflexes judge by age, by platform or by player | no control scores a way of judging a missing event | no | not linear: a per-purchase join to the phone's next start, then a per-build completion | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "production build" | the twelve builds in the register's Builds sheet | builds seen in the purchase service | every purchase's build number is one of the twelve | C1 (asserted) |
| SF2 | "purchase" | a validation of kind purchase, Production, standard; a refunded purchase stays | pass renewals, sandbox and licence-tester purchases in; refunded purchases out | renewals carry no build; testers' events arrive at once; same call | KC-DQ-04 s.2; same call (asserted) |
| SF3 | "a purchase's event" | the purchase_completed event with its store transaction id, a duplicate upload and a restored event the same event | each event row an event | matching is by transaction; same call | KC-DQ-04 s.3; same call (asserted) |
| SF4 | the build a purchase belongs to | the validation's app_build through the register | the event's app_version | every matched event names the validation's build; a missing event names none | KC-DQ-04 s.2; C1 (asserted) |
| SF5 | the period | the Irish date (Europe/Dublin) of purchased_at, 12 October to 8 November | UTC dates; the validation time | same call | KC-DQ-04 s.2; same call (asserted) |
| SF6 | "never reaches the warehouse", an event not arrived by the run lost only if it never will | an event missing once its phone has opened the game since is lost; an open one (its phone has not opened the game since) is lost in the share the build's own resolved gaps show | every missing event lost; every open event delivered; the open ones at the platform's or the pooled resolved share; an open one lost once its phone has been silent longer than its longest earlier gap | every missing event lost: 8 alerted, 6 wrong; every other reading: the golden pair | KC-DQ-04 s.4 ("lost only if it never will" rules out counting every missing event lost); same call for the others (asserted) |
| SF7 | "above 2 per cent, compared unrounded" | strictly above, unrounded | at or above; rounded first | no build sits on the line: the alerted pair at 3.10 or more however their open events end, every other build at 1.68 or less under any rate its resolved gaps give | KC-DQ-04 s.5; same call (asserted) |
| SF8 | the run's data | the exports of 07:00 on 9 November | none | no event of a purchase whose phone opened the game before the run arrives after it | C1 (asserted) |
| SF9 | a purchase validated twice | one purchase | two | no store transaction id repeats among the purchases | C1 (asserted) |
| SF10 | the phone of a purchase | the validation's device_id | the event's device_id | every matched event names the validation's device | C1 (asserted) |
| SF11 | "every build in production in the build register" | the twelve, the staged 7.42.0 builds included | the fully released builds only | the register's status column reads production for all twelve | KC-DQ-04 s.5; register |
| SF12 | each build's tracking loss on the chart | the settled losses plus the open purchases at the build's own resolved share | every open event delivered; the platform's or the pooled resolved share | the same two builds above the line and ten below it; the list grades the alert, never the loss | prompt (the list carries the alert); same call (asserted) |

## Ladder

Four rungs, each a defensible way of telling a lost event from a late one, each dying to one shipped fact (figures
measured on the cut pack, asserted in `checks.py`; losses in per cent).

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0 (default) | a purchase lost when its event is still missing seven days later | Android 7.38.1, 7.41.0, iOS 7.38.2, 7.39.1 and 7.40.0 alerted (3.07, 6.34, 2.85, 2.85, 2.77), the 7.42.0 builds unjudged: 5 wrong | the session log: the old builds' missing events sit on phones that have not opened the game since; the SDK notes: an event leaves only when the game starts or is open |
| 1 | a window of eleven days or more; a pooled arrival curve; a short window or a same-age comparison for the 7.42.0 builds | Android 7.41.0 alone (iOS 7.42.0 missed); 6 alerted, 6 wrong; Android 7.42.0 alerted at every window to 2.5 days (9.24 to 2.27 against iOS's 5.57 to 0.00), and by the same-age comparison (9.24 against 6.92 expected) while iOS 7.42.0 clears (5.57 against 9.76) | the SDK notes: 5.0.1 sends at once on iOS and holds batches on Android, so age says nothing about loss on the new builds |
| 2 | each missing event against its account's next session | Android 7.41.0, iOS 7.38.2, 7.39.1, 7.40.0 and 7.42.0 alerted: 3 wrong | the SDK notes: the queue is the phone's; a player's iPad does not empty when the phone opens the game |
| 3 (golden) | each missing event against its phone's next session; the open ones bounded by the build's own resolved gaps | Android 7.41.0 (157 of 2,477 purchases lost, none open: 6.34) and iOS 7.42.0 (10 lost and 8 open of 323: 3.10 if every open event arrives, 4.75 at its own resolved share, 5.57 if none does); every other build 0.55 or less at its own share | |

- **Margins.** Both alerted builds stay above the line however their open events end: Android 7.41.0 has none open,
  and iOS 7.42.0 reads 3.10 if all 8 arrive and 5.57 if none does. Every other build stays below it unless far more of
  its open events were lost than its resolved gaps show: the nearest, Android 7.42.0, needs 22 per cent of its 34 open
  events lost, where none of its 62 resolved gaps was; on the old builds 33 to 60 per cent, where 2 per cent or fewer
  were (asserted).
- **Corridor (C3).** The rate for the open purchases cannot be recovered and moves no alert: the build's own resolved
  share, its platform's (iOS 3.72, Android 18.16 per cent, Android 7.41.0's losses inside), the pooled 11.29 per cent,
  or an open purchase counted lost once its phone has been silent longer than its longest earlier gap all alert the same
  pair, every other build at 1.68 or less (asserted). No graded figure moves with it.
- **Position and dominance.** Every age-based reading lands on its own wrong set, the old builds' waiting events
  charged as losses or the 7.42.0 pair swapped; only the phone's next session reaches the golden. The default path's
  four false alerts sit 0.77 points or more above the line, and its miss is structural (no week-old purchase).
- **Grid.** The default moves 5 of 12 cells, the rungs 1 to 6.
- **Worth.** Counted on the cells, never on an intermediate.

## Closure table

| # | Axis | Reading in this build | Closure |
|---|---|---|---|
| 1 | Population | each production build's store-verified purchases made in the game, 12 October to 8 November (Irish dates), purchases made shortly before the run counted like any other | KC-DQ-04 s.2, s.4 (SF2, SF6) |
| 2 | Unit of account | the purchase (one store transaction) | KC-DQ-04 s.2, s.4 (SF9) |
| 3 | Attribution window | the Irish date of purchased_at | KC-DQ-04 s.2 (SF5) |
| 4 | As-of dating | the exports of 07:00 on Monday 9 November | the exports' own last timestamps and KC-DQ-04 s.5 (the run at 07:00 on Monday); C1 (SF8) |
| 5 | Version basis | a purchase belongs to the build that made it | KC-DQ-04 s.2 (SF4) |
| 6 | Denominator | every purchase of the build in the period | KC-DQ-04 s.4 |
| 7 | Weighting | none: a share of purchases per build | KC-DQ-04 s.4 |
| 8 | Window length | four weeks to the Sunday before the run | KC-DQ-04 s.5 |
| 9 | Boundary inclusivity | above 2 per cent, unrounded | KC-DQ-04 s.5 (SF7) |
| 10 | Rounding path | the alert on the unrounded share; gross bookings rounded line by line to the cent, then divided by paying players and rounded to the cent | KC-DQ-04 s.5 and s.6 |
| 11 | Tie-break | none: each build on its own | KC-DQ-04 s.5 |
| 12 | Maturity and censoring | an event not arrived by the run is lost only if it never will; a missing event is settled once its phone has opened the game since; the rate for the open ones is a corridor (C3: the build's own, the platform's or the pooled resolved share, or a silence cut-off, all one call) | KC-DQ-04 s.4; the design (the SDK notes and the session log), asserted corridor (SF6) |
| 13 | Order of operations | filter, collapse events, match, judge, divide, compare | KC-DQ-04 s.2 to s.5 |
| 14 | Row order | irrelevant to counts and matches | C1 |
| 15 | Duplicate resolution | duplicate uploads and restored events are the purchase's one event | KC-DQ-04 s.3 (SF3) |
| 16 | Identity normalisation | build numbers to versions through the register; the phone by device_id; a player through the account links and each guest's sign-in on its phone | register; KC-DQ-04 s.6; KC-DQ-04 s.6's note on the account links and the SDK changelog's account line; C1 (SF4, SF10) |
| 17 | Netting against gross | none: a refunded purchase stays a purchase | KC-DQ-04 s.2 |
| 18 | Dimensional units | counts and shares | KC-DQ-04 s.4 |
| 19 | Code and status semantics | transaction kind, environment and purchase type as KC-DQ-04 s.2 names them | KC-DQ-04 s.2 |
| 20 | Integerisation | none | counts are integers |
| 21 | Clause scope | every build in production in the register | KC-DQ-04 s.5 (SF11) |
| 22 | Forward window contents | the events that will still arrive from phones that have not opened the game since | the design: an event leaves only when the game starts or is open (SDK notes), the session log records every start; margins asserted |

## Literal reader

Executed word for word, KC-DQ-04 and the prompt fix the builds (the register's twelve), the purchase (s.2: kind
purchase, Production, standard, refunded purchases kept, the Irish date of purchased_at), the event (s.3: the
purchase_completed event with the store transaction id, the warehouse's several rows for one transaction one event),
the window (12 October to 8 November), the share and its outcome (s.4: the purchases whose event never reaches the
warehouse; purchases made shortly before the run count like any other, and an event not arrived by the run is lost
only if it never will) and the line (s.5: above 2 per cent unrounded). Executed, s.4 leaves one question for the
analysis: which missing events will never arrive. "Lost only if it never will" rules out counting every missing event
as lost (that alerts 8 builds). The SDK notes say how an event moves (queued on the phone, uploaded when the game starts
and while it is in the foreground), and the session service records every start; a missing event of a purchase whose
phone has opened the game since will never arrive, and the build's resolved gaps say how many of the rest will.
Android 7.41.0's share is known outright (157 of 2,477, none open); iOS 7.42.0's lies between 3.10 and 5.57 per cent
whatever its 8 open events do; every other build stays under the line at the build's own, the platform's or the pooled
resolved share, or with an open purchase counted lost once its phone has been silent longer than its longest earlier
gap (asserted). The list grades the alert, not the loss, so no graded figure turns on that rate. s.6 fixes the asks: a
player counted once across accounts (a guest the same player as the account it signs in to, support merges, any chain
of these), which the account links, by their own note not a full register, and each phone's sign-in in the session log
execute; gross bookings per paying player at each currency's minor unit and the ECB rate in force on the Irish date,
rounded line by line, then per player, to the cent. No reading of a term moves the call; the difficulty is the
estimation, not the words.

## Oracles

- No control, published figure or certified loss ships: nothing reports a build's tracking loss, an alert or a lag
  distribution, and no field marks a purchase as due, late or lost.
- The crash reporter's daily crash-free sessions by build, the stores' weekly ratings by version and the push
  campaigns (distractors, named in `metadata.json`): none counts purchases or events; 7.42.0's slightly lower
  crash-free share says nothing about its purchase events.
- The arrival lags (received_at against purchased_at) are data, not a control: they show that events arrive late,
  which every rung uses, and tie under every way of judging a missing event.

## Ask sheet

Two asks, 24 figures, decoupled from the call: the call reads the validations' kind, environment, purchase type,
transaction id, device, build and purchase time, the events' transaction id and receipt time, and the session log's
device and start; the asks read the validations' account, price and currency, the session log's account, the account
links and the ECB rates, columns and files the call never reads.

**Main population (zero device rows, asserted):** no device or hazard of either ask touches the call: the alert set,
each build's settled losses and open purchases are unchanged when every account id is shuffled, every link dropped and
every price and currency scrambled.

| Ask | Figures | H18 home | Use | Primary device (family) | Hazards | Path (files, columns) | Stops |
|---|---|---|---|---|---|---|---|
| A: each build's paying players over the period | 12 | a measure every build carries that the call does not turn on | the alert list tells the funnels' readers how many paying players an alerted build's events carry | D7, the true key elsewhere: a guest who signs in to an account made before keeps that account's history and leaves the guest's behind, so the account service records no link; the phone that bought as the guest goes on as the signed-in account, in the validations and the session log (KC-DQ-04 s.6: a guest account is the same player as the account it signs in to; KC-DQ-04 s.6: the links are not a register of every account a player has used) | link chains (a guest upgraded, then merged by support); testers (s.2); refunded purchases kept (s.2) | validations (account, device, purchase time, kind, environment, purchase type, build), session log (device, account, start), account links (from, to), register (platform, version, build number), KC-DQ-04 s.2 and s.6, the SDK changelog: 6 files, 15 columns | every account a player (every build 8 to 32 high, against 275 to 1,538); the links one hop (every build 6 to 24 high); the links followed to the end of each chain (every build 5 to 20 high); the answer, links joined with each guest's next account on its phone |
| B: each build's gross bookings per paying player, in euro | 12 | a measure every build carries that the call does not turn on | what a paying player of an alerted build spends while its events are left out of the funnels | D3, units set per currency: price_minor is in each currency's minor unit, and the yen and the won have none (ISO 4217 exponent 0), so a Japanese coin pack at 300 yen is 300, not 30,000 | the paying players of A as the divisor (shared); refunds before (s.6); testers (s.2); renewals (no build) | validations (price, currency, purchase time, kind, environment, purchase type, build, account, device), ECB rates (date, currency, units_per_euro), session log (device, account, start), account links (from, to), register (platform, version, build number), KC-DQ-04 s.2 and s.6, the SDK changelog: 7 files, 18 columns | every price divided by 100 (every build 0.78 to 1.31 euro low: 4.80 to 10.42 against 5.58 to 11.73); the links as the record of players (every build 0.06 to 0.21 euro low); every account a player (every build 0.07 to 0.63 euro low); refunds netted (11 builds 0.02 to 0.13 euro low); testers in (6 builds 0.07 to 0.60 euro off); the answer, each price at its currency's exponent, converted at the rate in force and rounded line by line, the total over the paying players of A |

- **Span:** seven files and 33 column uses across the asks. B shares A's player count as a divisor (a hazard moving
  both asks on every build); its own primary is the currencies' minor units, and its rate and rounding hazards cancel
  at a player's cent (the next published rate at weekends and the totals summed before rounding leave every figure
  where it is, asserted).
- **Shared hazards:** the paying players (A's device) move B on all 12 builds; the testers move both asks on the six
  builds they bought on; a refunded purchase dropped moves A and B on 11 builds.
- **Realism:** a guest signing in to an older account that keeps its own progress, with no link because no history
  moved, is how game account services behave; prices stored in each currency's minor unit, with the yen and the won
  carrying none, is how payment systems store them; revenue per paying player is the figure a game studio quotes
  beside its payer counts.
- **Referee:** none.

| Ask figure | Where the cracker's path goes | Mirror (stops at rung 0) | Cracker (lands the call, runs the battery) |
|---|---|---|---|
| A paying players (12) | executes s.6 through the account links, the guest_upgrade rows being the guests' sign-ins and the chains followed to their end; a guest who signed in to an older account has no link and shows only as a phone that changes account, which the battery's accounts-per-device count reads as a phone changing hands, so the player counts twice wherever both accounts bought on the build | misses the same way | miss |
| B gross bookings per paying player (12) | converts every price right but divides by the paying players of A, two accounts for one player wherever the guest's sign-in left no link | misses the same way | miss |

- **Cracker keeps:** 0 of the 24 ask figures (its paying players run 5 to 20 high on every build, so no figure is free
  of them).
- Mirror leakage: 0 per cent of ask weight (the mirror's ask path is the cracker's; the asks do not touch the call's
  construction).
- Pair ceiling: 28.5 (C = 38 + 7 + 55 x 0 = 45.0; S = 5 + 7 + 55 x 0 = 12.0; mean 28.5; 31.3 on paper before it was
  measured).
- Measured by: generator/ceiling.py on the cut pack.

## Pre-ship check

- **2026-10-31 reship under the 10-30 gates (target.zip 526ac9335f1fb56b).** Judge pass 2 DETERMINISTIC, APPROVE
  (Gate G statistical_rigor, analytical_non_defect; Gate H pass; no competing answer survived; every figure
  reproduced); its file-count note fixed and write-up step 7 now states the guest join as the golden computes it.
  Leak reader clean (question 6 analytical, every column read without a dictionary). Free gates on the final cut:
  checks 192, verify, two byte-identical builds, figures_check 109 of 109, precut 0 FAIL 0 WARN, voice-check clean,
  leak.py REVIEW with no LEAK, ceiling.py pair 28.5, guard.py surface exit 0 (seven pairs promoted for the author's
  read) and heart WARN (the task197 similarity answered on the card). The 10/10 rules re-read: the decisive step is
  still the censoring of a missing event until its phone's next session, analytical; the mess is still Layer 1.

1. Domain: the call stands on each build's purchase-tracking loss, the client events reconciled against the
   store-verified purchases with each missing event judged against the next session of the phone that made the purchase
   (the SDK's queue on the phone, uploaded when the game starts). With a seven-day settle window 5 builds change, with
   the account's next session 3, and any reading by age swaps the 7.42.0 pair. With wards or tills for builds there is
   no queue on a phone, no session handshake and no store receipt to read.
2. Two layers: Layer 1 (renewals, sandbox and licence-tester purchases, duplicate uploads and restored events, skewed
   device clocks, build numbers against version names, Irish dates against UTC with the end of Irish Summer Time inside
   the window) is neutral on the call, each item asserted (R2, SF rows); Layer 2 is the censoring of a missing event
   until its phone's next session, asserted alone to move the default path to the golden (R3b), the rate for the open
   purchases a corridor every reading of which alerts the same pair (C3).
3. No banned stump decides: nothing is planted (Android 7.41.0's and iOS 7.42.0's losses are recorded only as missing
   events; no memo, alert, dashboard or draft); not semantics (the default path reads every field and code right and
   files 5 wrong builds on the clean truth, R3a, the younger purchases kept or left out); not rule application (KC-DQ-04
   files the share, the outcome for an event not arrived by the run and the line, and names no way of telling a lost
   event from a late one, asserted on the catalogue's text).
4. Gate G: no shipped artifact estimates, flags or ranks a build; the three distractors count no purchase or event.
5. Determinism: the list grades each build's alert, paying players and gross bookings per paying player, never the
   loss; the alert set is the same under every rate the resolved gaps give the open purchases (the build's own, the
   platform's, the pooled, a silence cut-off, every open event delivered), the nearest other build 0.32 points below
   the line; Android 7.41.0's 6.34 and iOS 7.42.0's floor of 3.10 are known outright; every gross bookings per paying
   player sits 0.077 cent or more from a rounding edge; paying players are integers. Judge (architecture 2, round 1):
   DETERMINISTIC, APPROVE; Gate G statistical_rigor, analytical_non_defect, no surface read; Gate H domain pass,
   layers pass, decisive step analytical; stump power moderate (s.4's outcome sentence and the SDK notes let a strong
   solver reach the censoring, so the asks carry the bar). Its one low note, "resolved gaps" undefined in the write-up,
   is fixed: the write-up names the set (the build's events still on a phone when the game next opened). The judged
   bundle and the shipped one differ in the support merges' times of day, the SDK notes' unrelated entries and the
   distractor ratings; every graded figure, the alert list and the golden list are byte-identical.
6. Asks: A (12 figures) is moved on every build by the guest sign-ins to older accounts (the links alone 5 to 20 high),
   B (12) on every build by the yen and won exponents (0.78 to 1.31 euro low) and by A's players (0.06 to 0.21 euro low
   through the links); the call reads neither (asserted by scrambling accounts, prices and currencies and dropping the
   links and the rates).
7. Input gates: 11 files in four formats (csv, md, pdf, xlsx), the session log at 325,515 rows, three distractors named
   in metadata.json; 193 generator checks with the realism sweep; the verifier (its own merge and union-find, the alert
   set at three rates) green; two builds byte-identical; figures_check 109 of 109; containers clean.
8. Duplicate guard: `guard.py heart` WARN (repeat.gate_g and repeat.decision against task264, drawn since this build's
   first draw; same_puzzle_older and same_driver_older differentiated against task445 and task459; the driver near only
   its own lineage); `guard.py surface` promoted seven pairs for the author's adjudicated read, none a shared mechanism:
   task234 (back to back, a README, the time gap and a designation set: task234 predicts a source's output from a share
   a loss cannot move), task233 (a README and a designation set), task81, task95 and task73 (surface in the corpus top 1
   per cent, other mechanisms), task459 and task445 (the time gap, pattern E and Gate G on the cards, differentiated on
   the card: neither judges a missing item by its own sender's next contact).

## Leak check

Architecture 1: leak.py REVIEW, no LEAK; reader: Q5 read s.4's "may still reach it" as counting every missing event
lost (8 alerts), a main-call fork, and the bookings ask fell whole; with the judge's SEND_BACK, re-rooted.
Architecture 2: leak.py REVIEW, no LEAK (--asof 2026-11-09). Reader pass 1: Q1 none (s.4 "names the issue but not how
to judge it"), Q2 to Q4 none, Q5 s.4 leaves the pending-or-lost judgement to the analysis (counting every unarrived
event lost is the naive option, ruled out by "lost only if it never will"), Q6 an analytical choice; it landed the call
and missed both asks on every build (paying players off the links alone). Realism notes fixed in the generator: support
merges no longer pile up at the desk's opening (a request out of hours is taken up during the next working day, an
older account's request at any point in the weeks, the link set unchanged), the SDK notes read as a changelog (the
queue in 4.6.0, unrelated entries in each release). Reader pass 2 (the changed documents): Q1 to Q4 none, Q6 an
analytical choice; it again landed the call and missed both asks. Its realism notes: the ratings' weekly counts jumped
at random (fixed: each version's count follows its players that week, a data-only change checked by leak.py); the
links file's note reads as a hint (it is the determinism-check §1 sentence a completed source must carry, true of the
792 guests whose phone shows a sign-in the links do not record); the catalogue reads tidy (left: it is a metrics catalogue). Its "links only or links with each phone's
sign-in" is no fork: the links alone leave every guest who signed in to an older account counted twice, against s.6.
REVIEW lines, all harmless: build numbers and version names in the pack are the candidates' own identifiers; the
dictionary carries the call's words as build names; device_id is the SDK's and the services' own column name.

Reship of 2026-10-31: leak.py REVIEW, no LEAK (the README and the data dictionary removed, the SDK notes shipping as
tern_sdk_changelog.md); one reader on the 11-file pack: Q1 to Q4 none, Q6 an analytical choice, every column read
without a dictionary; the catalogue's note on the account links reads a little like a caution, which it is by design
(determinism-check 1); recorded in `leak_check_report.md`.

## Tried and rejected

- The seed's world (notifiable disease reports by area, nowcast against the delay distribution): Epidemiology & Public
  Health x Data Quality is banned against task234, and in that domain the completeness alert's analysis is the
  expected count, which task234 spent; the decision and the quantity move to purchase tracking.
- The loss read over the purchases whose phone has come back only, as the golden: it cannot equal a share the records
  know outright (Android 7.41.0: 157 of 2,477 with none open, 6.34, where the subset gives 6.36) and on a small young
  build it can exceed the share of events missing at the run; replaced by the known losses plus the open ones at the
  build's own resolved share.
- A confirmed-losses rung (the open events counted delivered, or left out of the denominator) to hold solvers who find
  the session log: it misses iOS 7.42.0 only when under half of that build's purchases are due, which no rollout of a
  few days with daily players gives; the session log's own rungs are the account join and the age readings.
- 7.42.0 released on Wednesday 4 November: a long window for the old builds beside a 1.5 to 3.5 day window for the
  7.42.0 pair landed the golden on most seeds, because Android's held events cleared within a day or two; released on
  Thursday 5 November, with WorkManager holding about a third of Android 5.0.1's events, Android 7.42.0 reads above
  iOS 7.42.0 at every window it has data for.
- Paying players on the account links alone as the ask's device (one hop against the whole chain): a cracker that runs
  the battery follows the chains; replaced by the guest sign-ins to older accounts that leave no link.
- "Ardnagh Games" as the studio's name: one letter from Ardagh (a packaging group and several Irish places) and a historical spelling of a Roscommon townland (house fix H21); renamed Fogbell Games before the reader and the judge.
- Architecture 1 (drawn, built and judged 2026-10-17): the alert list graded each build's tracking loss at two decimals,
  the open purchases counted at the build's own share of resolved gaps; the determinism judge returned
  NOT_DETERMINISTIC, SEND_BACK, underspecified_objective, because nothing shipped says how the open purchases are
  valued and the build's own, the platform's and the pooled share or every open event delivered give different
  figures (iOS 7.42.0 4.75, 3.19, 3.38, 3.10), and because paying players reproduced only with each guest's sign-in on
  its phone joined to the links, which no file called incomplete. The alert set was forced and Gate H passed. Spent;
  re-rooted as architecture 2 with the world and the decisive step kept, the loss column off the graded list, s.4
  saying an event not arrived by the run is lost only if it never will (the leak reader had read "may still reach it"
  as counting every missing event lost), and the links file's own note.
- Each build's gross bookings in euro as an ask (architecture 1): the leak reader filed all twelve to the cent (the yen
  and the won without a minor unit, the rate in force at weekends and line-by-line rounding are known moves); replaced
  by gross bookings per paying player, which carries the players' count.
- Filing the rate for the open purchases (the build's own share of resolved gaps) to force the loss figure, as the
  judge offered: it names the decisive construction, and the step becomes rule application; the graded list carries
  the alert instead, which every rate the data supports leaves where it is.
- 2026-10-31, the 10-30 re-check: the README (a pack manifest) and DATA_DICTIONARY.md (41 columns) were describing
  files (leak.py sweeps 1 and 12) and are out. Their facts moved: the time basis is the exports' own Z marks and the
  catalogue's Irish dates; the codes are KC-DQ-04 s.2's; the ECB file's quote direction is its column label
  (units_per_euro); the reading that a phone's account switches from the guest's to the player's at sign-in is a line
  in the SDK changelog's 4.6.0 entry; the links' "not a register of every account a player has used", the sentence
  determinism-check 1 requires of a source the golden completes, is in KC-DQ-04 s.6. The Tern SDK's notes ship as
  tern_sdk_changelog.md, their genre's own name, unchanged but for the account line. The prompt drops its build count
  and asks what; metadata.json's title and subdomain no longer narrate the step. generator/ceiling.py measures the
  pair at 28.5. No graded figure moved (figures.json unchanged).
