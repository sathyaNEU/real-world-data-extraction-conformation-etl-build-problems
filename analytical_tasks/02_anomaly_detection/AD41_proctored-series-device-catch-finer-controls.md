# AD41 — Which prize series gets proctored mode next season, when proctoring catches assisted players on desktop and almost never on the app

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Product Analytics · online game integrity |
| Mirrors | Integrity teams deciding where a costly protection goes when it works on one channel and not another (anti-cheat drivers that run on PC but not on consoles at Riot and Valve, invalid-traffic filters that see browser signals but not in-app traffic at Google, proctoring vendors whose screen share covers desktop sessions only) |
| Decision shape | Which of N gets one scarce thing: the season's single proctored-mode deployment (webcam, screen share and live move-time review on prize sessions) goes to one of five prize series |
| Committed call | The series that gets proctored mode, and the prize money it protects from assisted play over the season |
| Gap · Pattern | Gap 2 (population: where proctoring can act) over Gap 4 (rule) · finer controls separate constructions (the pilot's overall catch is met by a constant rate and by a platform split; only the split meets each account's outcome), with a mixed segment split through the entry table (prize divisions) and a quiet depth contamination below it |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #12 stops at the first control that passes · #11 beats the headline trap, misses the quiet one · #6 treats a mixed segment all one way |
| Calibration form | Pilot log: last season's proctored-mode pilot on series B and D, with every flagged account, the device of each prize session, the proctors' live outcome and the fair-play committee's filed decision |
| Driving force | Proctored mode protects prizes only where it can see the play. On desktop it watches the screen and the move times and caught 0.90 of the pilot's confirmed assisted accounts live; on the mobile app its screen share cannot see a second device, and it caught 0.15. The pilot's overall rate, 0.82, is met by a constant and by the platform split alike, and only the split reproduces each confirmed account's outcome. Once the two 960 series' depth-12 analysis is corrected, the 960 Series carries the most assisted prize money, but 95% of its prize sessions are played on the app, so proctoring there would protect $15k; the 960 Masters, played on desktop, would protect $44k. |

## 1. Situation

An online chess platform runs five prize series, from a titled arena to two 960 series, with $2.1 million in prizes next season. Its
fair-play team can run proctored mode (webcam, screen share and live review of move times) on the prize sessions of one series, which the
pilot showed catches most assisted players before prizes are paid. The fair-play plan sends it where it protects the most prize money from
assisted play, valued on this season's results. The team holds every analysed game with per-move evaluations, the analysis job log (engine,
depth and host for each game), the entry table with each entrant's prize division, the session log (the device of every prize session), the
account register, the series terms and the pilot log. The community manager is sure the titled arena is the problem.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the evaluations at the depth each game was analysed, the residual screen, the entries, the session
  devices, the committee's decisions and the pilot's live outcomes. The fair-play lead is right that proctoring caught most assisted players
  in the pilot. Nothing is overturned; the difficulty is where proctoring can catch them.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the community manager's view and the best-five list. A per-depth residual screen with division-correct prize
  money at the pilot's overall catch rate still names E.
* **Instrument repair.** Suspect files: the 960 games' evaluations, made at depth 12 (a narrower measurement of move quality), and the account
  register's sign-up device (a narrower record of the device a prize session is played on). Repaired at depth 20 and with every session's
  device, rung 0 still names A, rung 1 B, rung 2 now names E (80 against D's 56) as rung 3 does, and the device-conditioned catch is still
  needed: proctoring cannot see 95% of the 960 Series' prize sessions.
* **Lens swap.** The naive protection is assisted prize money at one catch rate; the answer's is assisted prize money on the devices
  proctoring can see, a different set of prize sessions and a different series.

## 3. The driving force

A strong solver rejects raw and best-five accuracy, builds expected move loss by rating band, time control and colour, splits prizes by
division through the entry table, and finds the quiet trap: the prize queue's engine build has no 960 support, so every game in both 960
series was analysed client-side at depth 12, which inflates and squeezes the 960 residuals. Rebuilt per depth, the 960 Series carries $80k of
assisted prize money and the 960 Masters $56k, and at the pilot's catch rate of 0.82 the 960 Series wins. Every step is correct, and the catch
rate is a mix. Read account by account, the pilot log shows proctoring caught 148 of 164 assisted desktop accounts live and 3 of 20 on the
mobile app, whose screen share cannot see a second device. The pilot ran on two desktop-heavy series, so its overall rate hides the split.
The session log puts 95% of the 960 Series' prize sessions on the app and 85% of the 960 Masters' on desktop: proctoring would protect $15k
in the first and $44k in the second.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Accounts on the best-five accuracy screen × their prize winnings ($k): A 74, B 61, C 52, D 45, E 38 | A, the titled arena | The current screen and the obvious place to look | The expectation table: accuracy rises steeply with rating, and A's flagged accounts score as expected for their band |
| 1 | Residuals against rating, time control and colour on a pooled expectation, aggregated per account; prize money won by accounts over the review line, series pool treated as one: B 96, C 52, E 34, D 25, A 19 | B | The loud trap beaten with a proper expectation | The entry table and series terms: B's prizes split into an Open division ($360k) and an under-2000 division ($140k), and B's high scorers sit in the under-2000 division |
| 2 | The same with prize money assigned by division: C 50, E 36, B 28, D 25, A 18 | C | Expectation-adjusted and division-correct | The analysis job log: every prize game in both 960 series was analysed client-side at depth 12 |
| 3 | Expectation built per analysis depth, prizes by division: E 80, D 56, C 50, B 28, A 18 | E, the 960 Series | The quiet trap beaten, and the pilot's 0.82 applies to every series alike | The pilot log's live outcomes by device: proctoring caught 148 of 164 assisted desktop accounts and 3 of 20 on the app, and 95% of the 960 Series' prize sessions are played on the app |
| 4 | **Decisive:** rung 3's assisted prize money × the live catch for each series' mix of prize-session devices (desktop 0.90, app 0.15): D 44.1, C 30.0, B 22.1, E 15.0, A 14.9 | **D, the 960 Masters** (4th of 5 on rung 0) | — | — |

* **Position table.** D ranks 4th on rungs 0, 1 and 2 and 2nd on rung 3 (E leads it by 1.43×), and leads only rung 4. Rung leaders beat
  their runners-up by 1.21×, 1.85×, 1.39×, 1.43× and 1.47×.
* **Discriminator dominance.** E carries a 1.43× advantage into rung 4 (80 against 56), so the required edge is 1.2 × 1.43 = 1.71×. D's
  device mix gives a catch of 0.79 against E's 0.19 (4.2×), 2.45× the requirement, and the net is 4.2 / 1.43 = 2.9×.
* **Partial correction priced (L3).** A solver who applies the pilot's overall 0.82 to every series keeps rung 3's order and names E, 65.6
  against D's 45.9 (1.43×). A solver who conditions on the account register's sign-up device, where 70% of E's accounts signed up on desktop
  before playing their prize sessions on the app, puts E's catch at 0.68 and names E again, 54 against D's 44 (1.22×). Both land on the
  rung-3 leader.
* **Grid.** Expectation (best-five, pooled, per depth) × prize assignment (one pool or by division) × catch (pilot overall or by device) =
  12 cells. Best-five cells name A; pooled cells name B in one pool and C by division under either catch; per-depth cells name B in one pool,
  E by division at the overall catch, and D only by division with the device catch.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The pilot report gives one live catch rate; no document says proctoring sees less on the app, and the session log is
   filed as a support record.
2. **Finer controls pin a construction, not a menu.** The pilot's overall live catch, 151 of 184 confirmed accounts (0.82), is the salient
   control, and a constant rate and the device split both meet it. The finer controls, each confirmed account's live outcome with its
   session device, are met only by the split (148 of 164 desktop, 3 of 20 app); the constant misses 17 of the 20 app accounts. The split is
   a join from each prize session to the session log, not a parameter.
3. **No arithmetic symptom.** Every game has evaluations on every move, residuals reproduce from them, the pilot's outcomes sum to its 0.82,
   and session devices tie to the session log.
4. **Not a row predicate.** Each series' protection needs its assisted prize money per depth and division, each prize session's device, and
   the device rates from the pilot's account-level outcomes.
5. **The enumeration is arithmetic.** Protected prize money is computed; no column carries a catch probability.
6. **No cutover date.** The app's screen share has never shown a second device; nothing steps.
7. **Survives deletion.** Remove both voices and the best-five list, and the per-depth screen at the pilot's overall rate is still the
   natural build.

## 6. The calibration corpus

* **Form.** The pilot log: last season's proctored-mode pilot on series B and D, every account the proctors flagged, each prize session's
  device, the proctors' live outcome and the fair-play committee's filed decision (confirmed assisted or cleared).
* **What it pins.** The review line (every confirmed account scores 3.0 or more on the per-depth screen and every cleared account under 2.4)
  and the live catch by device (above). It also pins the depth construction: the pooled screen flags 9 of the 23 confirmed D accounts and
  the per-depth screen all 23.
* **Twin pair.** Pilot finals F-09 and F-14 in series B are identical on every screen column: 14 flagged accounts each, the same residual
  distribution and the same prize pool. The committee confirmed 12 assisted accounts in each; proctors had caught 10 live in F-09 and 5 in
  F-14, 2.0× apart, because two thirds of F-14's confirmed accounts played their prize sessions on the app. Only the session device separates
  them.
* **Resemblance points at the decoy.** On every residual column the 960 Series resembles the pilot's best-protected finals.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The fair-play plan: proctored mode runs on one series' prize sessions and goes where it protects the most prize money from
  assisted play, valued on this season's results. The series terms with each division's prizes. The analysis job log and the session log as
  records. One sentence each.
* **Empirical pins.** The review line, the depth construction and the device catch rates, from the pilot.
* **Voices.** The community manager: "The titled arena is where the money and the cheaters are." The fair-play lead: "Proctoring catches
  eight in ten; put it where the most cheating is."
* **Licensed wrong basis.** The plan records that the sponsor's integrity auditor measures each series by flagged accounts on the best-five
  screen and will review the decision on that basis.

## 8. Determinism by construction

* **Expectation cells.** Every rating band × time control × colour × depth cell holds at least 2,000 games, so no cell is thin.
* **Review line.** The pilot's gap from 2.4 to 3.0 is empty this season too, so any line in it flags the same accounts.
* **Devices.** Each prize session records one device, and no series' app share moves by more than two points between counting sessions and
  counting accounts by their last prize session.
* **Rounding.** Protected prize money is given to the nearest $1,000: D's $56k assisted × 0.7875 = $44.1k.

## 9. Prompt sketch and deliverables

> We can run proctored mode on one prize series next season and five are asking for it. Our community manager is sure the titled arena is
> the problem. Tell me which series gets it and how much prize money it should keep away from assisted players over the season, to the
> nearest $1,000, in a line for the sponsor. Send `proctoring_case.xlsx`, a chart `catch_by_device.png`, and a one-page `series_memo.pdf`.

* `proctoring_case.xlsx` — the five series under each rung's basis (ask C), the entrant sheet (ask A) and the payout sheet (ask B).
* `catch_by_device.png` — the pilot's live catch for desktop and app accounts as two labelled bars with their counts, each series' app share
  of prize sessions as a strip, assisted and protected prize money per series as paired bars, and the chosen series highlighted.
* `series_memo.pdf` — the committed series and figure, and why each other series falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each series, unique entrants this season and their median and 90th-percentile rating. *Device:*
  the entry table stores the username at entry, and the account register maps renamed usernames to one account ID; counting usernames
  double-counts renamed accounts in four series. The decision uses account IDs from the results table, never the entry usernames.
* **Ask B (device-carried).** For each series, prize money paid this season in cash and in store credit. *Device:* the payment ledger books
  store credit at face value, and the finance guide states it at a cash equivalent of 0.6; adding face values overstates three series. The
  decision values prizes from the series terms, never the ledger.
* **Ask C (validity).** Each series' figure under each of the five rung bases.
* **Decoupling.** Clearing the device split, the depth stratification and the division split changes no figure in asks A or B.

## 11. Rubric arithmetic

5 series × 3 (ask A) + 5 × 2 (ask B) + 5 × 5 bases (ask C) + the committed series, its protected prize money, the runner-up and the margin +
5 named chart parts + 3 files ≈ 62 criteria.

## 12. World-building constraints

* Rung figures as in the ladder; D is 4th, 4th, 4th, 2nd (1.43× behind E) and 1st (1.47× ahead of C). The overall-rate build names E at
  65.6 against D's 45.9; the sign-up-device build E at 54 against D's 44.
* App share of prize sessions: A 10%, B 15%, C 40%, D 15%, E 95%; 70% of E's accounts signed up on desktop.
* Pilot on series B and D: 184 confirmed accounts (B 161, D 23); live catch 148 of 164 on desktop and 3 of 20 on the app; 0.82 overall.
* Both 960 series' prize games are analysed at depth 12; every other game, casual 960 included, at depth 20; depth-12 move losses run 1.8×
  depth-20 losses in the 2,000-game side sample shipped with the job log.
* Prize pools: $2.1 million; B's Open division $360k and its under-2000 division $140k.
* F-09 and F-14 are identical on every screen column.
* Entry usernames and payment ledger rows never touch the results table, evaluations, the job log or the session log.
