# task235 design note

Architecture 1, wave 2, seed DQ08 (which reporting areas get a completeness alert, when recent weeks are still filling
in): the seed's decision and quantity only, the pitfall re-found from the data under the 10/10 rules. Product
Analytics, metric definition and measurement science, Data Quality Monitoring & Alerting. Ardnagh Games, a Dublin
studio, sells coin packs, boosters and a monthly pass in its match-3 game Kittiwake Cove on iOS and Android. Every
Monday its data quality lead runs the tracking-quality check: each production build's tracking loss, the share of its
store-verified purchases whose `purchase_completed` event from the game's analytics SDK never reaches the warehouse,
and an alert on every build above 2 per cent, which takes the build's purchase events out of the experiment readouts
and the revenue funnels, opens a P1 bug for the SDK team and holds a staged rollout where it stands.

## Draw

Card `cards/task235.json` (architecture 1, registered 2026-10-17). Guard verdict WARN, one line: `repeat.question_form`
against task234 (which) is the decision's own form, a set of builds. `test.same_puzzle_older` (task445) and
`test.same_driver_older` (task445, task459) are cleared by the card's differentiation lines: neither completes a missing
amount from a class change or reads a rate at a committed level; this build decides item by item whether a missing record
is due yet.

- **Pairing.** Product Analytics / metric-definition-measurement-science, serving Data Quality Monitoring & Alerting
  (the domain index lists this task type under DD and DQ). The seed sits in Epidemiology & Public Health; that pairing
  is banned against task234 (the last three builds), and the seed's quantity, what has arrived against what should
  have by now while recent periods fill in, is native to product telemetry, where the late item is a client event
  queued on a phone and the record of what should have arrived is the store's server-side purchase.
- **Niche.** The game's analytics SDK logs `purchase_completed` on the phone and uploads its queue in batches; a player
  who leaves the game in the seconds after buying leaves the event queued on the phone. The studio's purchase service
  verifies every purchase with the store as it happens, and its session service records every time a phone opens the
  game. The check runs on Monday 9 November 2026 over purchases made from Monday 12 October to Sunday 8 November
  (Irish dates), so the last days' events are still arriving.
- **The call.** For each of the twelve production builds (iOS 7.38.2, 7.39.1, 7.40.0, 7.41.0, 7.41.1 and 7.42.0;
  Android 7.38.1, 7.39.0, 7.40.2, 7.41.0, 7.41.3 and 7.42.0), alert or not. The 7.42.0 builds moved to a new major SDK
  version and have been in a staged rollout since Wednesday 4 November; players who switch off automatic updates stay
  on the 7.38 and 7.39 builds and come back to the game about weekly.
- **Shape.** 10, a scorecard against a threshold: every build's tracking loss against the 2 per cent line, each check
  graded. Decision designation_set, answer set_of_items, question form which.
- **Strategy.** maturity_censoring with G12 decisive (a missing event is a non-answer until the phone that made the
  purchase has opened the game again), G14 supporting (the loss rate conditioned on that chance, pattern E's form) and
  G2 (the chance belongs to the phone, not the account); Gate G method_or_model_selection (which way of telling a lost
  event from a late one the data support); calibration none; context artifact register (the metrics catalogue); layer
  2 family estimation_fit, pattern own:loss-conditioned-on-the-delivery-chance.
- **Forum, event, organisation.** line_manager_or_team (the data quality lead raises the alerts in the analytics team's
  Monday run; no committee; redrawn from operations_desk after the pull brought task154's redrawn forum),
  launch_or_rollout (7.42.0's staged rollout goes to 100 per cent on Wednesday 11 November unless held),
  software_or_platform (a game studio).
- **People** (`guard.py names --geo "Ireland" --seed 235`): Amelia Seery, data quality lead, who runs the check and
  raises the alerts; Padraic Cormick, SDK lead; Darragh Boylan, release manager.
- **Deliverables.** `tracking_loss_alerts_2026-11-09.csv` (one row per build with its tracking loss and alert) and
  `tracking_loss_by_build_2026-11-09.png` (each build's loss against the 2 per cent line).
- **Data-native sentence.** A purchase event leaves the phone only while the game is open and online: sent within
  seconds if the player stays, otherwise kept in the phone's queue until that phone next opens the game, which for the
  weekly players on the old builds can be a week or two; the session service records every opening the moment it
  happens, so whether a missing event is late or lost is known purchase by purchase, while a settle window charges the
  weekly players' waiting events as losses and cannot judge a build too new to settle.

Sources, one line each (what it teaches; how this build differs):
- Client pattern metric-definition-measurement-science/2 (ratio of sums against mean of ratios: the metric follows its
  stated unit): here the unit is the purchase whose delivery chance has come; a pooled settled share is the wrong unit.
- Client pattern retention-cohort-lifetime-value-modeling/1 (young cohorts are censored, not churned): the same
  censoring logic turned item by item; the censoring time is each phone's next session, read from another system.
- Seed DQ08: the decision and the quantity only; its decoy-era design is not read.
- Client-server event reconciliation as analytics teams run it (server-side purchases as the record of truth, client
  events matched by transaction id); mobile analytics SDKs that persist a queue and upload in batches.
- Spent on this objective (`guard.py mechanisms`): task228 (a ratio metric's variance at the randomised unit), task229
  (a daily mean through a convex rating), task230 (net coding bias of a late channel), task231 (the closed share of
  silent units from rounds the register caught up with), task232 (transmission from delayed, mixed outcomes), task233
  (a missing-not-at-random departure on the odds scale), task234 (a source's output read from a share a loss cannot
  move). None judges a missing record by its own sender's next contact.

## Default path

1. Read the metrics catalogue's tracking-quality entry: a build's tracking loss is the share of its store-verified
   purchases made in the game from 12 October to 8 November (Irish dates) whose `purchase_completed` event never
   reaches the warehouse, purchases whose event can still arrive included; alert above 2 per cent.
2. Take the purchase service's verified purchases, drop the pass renewals the store makes without the game and the
   sandbox and licence-tester purchases, and match each to its event by store transaction id, the SDK's duplicate
   uploads collapsed.
3. Events arrive late, so count a purchase as lost only when its event is still missing seven days after the purchase;
   each build's loss is its unmatched purchases over its purchases at least seven days old.
4. Alert every build above 2 per cent.

Ends on: four builds alerted (Android 7.41.0 and three old builds whose weekly players have not opened the game again,
iOS 7.38.2, Android 7.38.1 and Android 7.39.0) and the two 7.42.0 builds left without a loss (no purchase seven days
old) and not alerted, so iOS 7.42.0, which loses events, is missed: 4 of the 12 builds wrong.

Golden: alert iOS 7.42.0 and Android 7.41.0, and no other build.

## Stump sentence

A competent solver counts a purchase as lost when its event is still missing seven days later and files 4 of the 12
builds wrong (Ends on: four builds alerted, three of them old builds whose weekly players have not opened the game
again, and iOS 7.42.0 missed); the step that lands it there is treating a missing event as lost before the phone that
made the purchase has opened the game again, the only moment the event can leave it.

## Three rules

- **Task type:** product-analytics / metric-definition-measurement-science, which serves Data Quality Monitoring &
  Alerting; the measurement here is a build's purchase tracking, the client-side instrumentation reconciled against the
  store's server-side purchases.
- **Domain test:** the quantity that decides is each build's purchase-tracking loss, measured over purchases whose
  phone has opened the game since, the reconciliation product analysts run on SDK telemetry against server-side truth;
  it rests on how a mobile analytics SDK delivers (a persisted on-device queue sent only while the game is open) and on
  the backend's session handshake.
- **Swap:** "which wards get a charting-loss alert, judged on the share of admissions whose nursing note never reaches
  the record" has no queue on a phone that empties only when the game is next opened, no session service and no store
  receipt; the analysis that decides here has nothing to act on.
- **Layer 1:** pass renewals the store makes without the game and sandbox and licence-tester purchases among the
  verified purchases (the purchase service records them all); duplicate SDK uploads and restored transactions (the
  SDK retries and the game re-logs a restored purchase); device clocks skewed against the warehouse's receipt time;
  build numbers in the purchase service against version names in the SDK (two systems); Irish dates against UTC
  timestamps with the end of Irish Summer Time inside the window; accounts that play on more than one device. Nothing
  is placed to be caught.
- **Layer 2:** estimation_fit, censoring: a missing event is censored until its phone's next session, so the loss rate
  is read among purchases whose chance has come; a settle window, a pooled arrival curve or the account's next session
  each mismeasure it.
- **Decisive step:** judging each missing event against the next session of the phone that made the purchase, read from
  the session service, and measuring each build's loss over the purchases whose phone has opened the game since.
- **Not semantics:** the default path reads every field, code and status right (renewals and sandbox out, duplicates
  collapsed, versions crosswalked, the window in Irish dates) and still files 4 wrong builds; what it gets wrong is when
  a missing event becomes a loss, which no field states.
- **Not rule application:** the catalogue files the loss as the share of purchases whose event never reaches the
  warehouse, purchases whose event can still arrive included, and the 2 per cent line; no rule says how to tell a lost
  event from a late one, and executing every stated rule still leaves that choice.
- **Analyst test:** a strong analyst who cleans the data and reads every rule, then counts a purchase as lost when its
  event is still missing seven days later, files 4 of the 12 builds wrong (Ends on: four builds alerted, three of them
  old builds whose weekly players have not opened the game again, and iOS 7.42.0 missed); joining the session log by
  account instead of by phone still files a false alert on iOS 7.41.1.
- **Estimand:** the metrics catalogue's tracking-quality entry (in the pack) fixes the population (each production
  build's store-verified purchases made in the game from 12 October to 8 November 2026, Irish dates), the outcome (the
  purchase's event never reaches the warehouse, purchases whose event can still arrive included), the unit (the
  purchase), the window and the comparison (above 2 per cent).
- **No decoy:** nothing is planted: no memo, dashboard export, draft list or stakeholder figure states a loss or an
  alert; the two faulty builds lose events through their own code paths, recorded only as missing events; the SDK notes
  describe delivery as SDK documentation does.
- **No certified replay:** no certified or published loss exists for a method to reproduce.
- **Lesson:** a record missing from a feed is a non-answer until its sender has had its next chance to send it, and that
  chance can sit in another system's log, item by item; no build on file judges a missing record by its own sender's
  next contact.

## Tried and rejected

- The seed's world (notifiable disease reports by area, nowcast against the delay distribution): Epidemiology & Public
  Health x Data Quality is banned against task234, and in that domain the completeness alert's analysis is the
  expected count, which task234 spent; the decision and the quantity move to purchase tracking.
