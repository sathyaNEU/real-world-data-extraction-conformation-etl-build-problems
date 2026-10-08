# FC22 — The escalator accrual for five free-agent signings, when three of the club's regulars can only bat at first base or designated hitter

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Economics · professional sports labour contracts |
| Mirrors | Accruing performance-contingent pay when the performance draws on a shared, capped resource (sales commissions when reps share a territory, ride-hail driver incentives capped by zone demand, ad-delivery bonuses when campaigns compete for the same inventory, cloud credits shared within a capacity pool) |
| Decision shape | One figure committed at a date: the escalator accrual booked when the five contracts are signed |
| Committed call | Expected plate-appearance escalator payments to the five signings next season, in $ thousands to the nearest 100 |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · S5, a ceiling that does not commute: plate appearances are capped per group of lineup slots a player can fill, a grain no file states, while every pooled check passes; with the player-season built from stint rows below it |
| Gate G mechanism | binding_constraint, with forecasting support |
| Measured traps engaged | #10 notes a binding limit as a risk · #2 counts file rows instead of the real unit · #18 joins only on the visible key |
| Calibration form | Existing-book actuals: the club's ten closed seasons of lineup cards, every plate appearance by player and lineup slot |
| Driving force | Each new contract pays $500,000 at 475, 550 and 625 plate appearances. The club bats 6,200 times a season and the roster's projections need only 5,700, so every pooled check passes. But a player bats only in slots he can fill, and the two new first basemen and the incumbent can each play first base and designated hitter and nothing else: 1,830 projected plate appearances for slots that hold 1,440. Shared as the club has always shared a crowded slot, in proportion to projections, P1 reaches 511 and P2 464. Eligibility is in no roster column; it comes from games started by position. |

## 1. Situation

A club has signed five free-agent hitters, and each contract carries the same escalators: $500,000 when the player reaches 475 plate
appearances, again at 550 and again at 625. The accounting policy accrues each escalator the player's projected plate appearances reach,
and the club's projection memo files the method: playing time from each hitter's last two seasons with regression toward a part-time
baseline. Finance books the accrual when the contracts are signed. P1 and P2 are first basemen by trade; the club already has a regular
first baseman.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the season batting file, the appearances file, the club's lineup cards, the contracts and the
  projection memo. No one's claim about their own numbers is overturned. The difficulty is where a projection meets the slots a player
  can actually fill.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the auditors' basis. The memo's projections, checked against the slot each player's roster
  line names, still accrue $4.5M.
* **Instrument repair.** Suspect: the season batting file, which follows a traded player's stint rows with an all-clubs total row.
  Keep one row per player-season: rung 0 then returns rung 1's $6.0M, and rung 2 still returns $4.5M. The appearances file records every
  start by position and the lineup cards every closed plate appearance; nothing is missing, and the eligibility group is still a
  construction, needed for $4.0M.
* **Lens swap.** The naive read and the answer differ in population: each hitter's playing time on his own, against the plate appearances
  the slots he can fill will actually hold.

## 3. The driving force

A strong solver builds one row per player-season, runs the memo's projections, and checks them against the lineup: the club bats about
6,200 times a season, and the roster's projections need only 5,700. Nothing binds in total. It may then cap each slot by the roster's
listed positions: P1 and the incumbent share first base, and P2 has designated hitter to himself. The appearances file says more. P2 and
the incumbent each started at least 40 games at both first base and designated hitter in each of the last two seasons, and none of the
three has started anywhere else. So all three draw on the same two slots, which have held 700 and 740 plate appearances in every closed
season: 1,440 for 1,830 projected. The lineup cards show how the club shares a crowded slot: every season its catchers split the
catcher's slot in proportion to their projections. On those shares P1 reaches 511 plate appearances and P2 464, and with the other three
signings at their projections the accrual is $4.0M.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The memo's projections on every batting row a player has in a season, each escalator accrued where reached | $6.5M, +63% | The filed method on the league's own batting file | **E02 (the unit not stored):** the file guide: a traded player's season is his stint rows followed by an all-clubs total row, and P5's 2015 is counted twice |
| 1 | The same on one row per player-season | $6.0M, +50% | Clean seasons, and the roster's 5,700 projected plate appearances fit the team's 6,200 | The lineup cards: no slot has held more than 740 plate appearances in ten seasons, and P1 and the incumbent are both listed at first base |
| 2 | Each slot capped at its closed-season plate appearances, players placed by their listed position | $4.5M, +13% | Every slot respected, P1 squeezed at first base and P2 alone at designated hitter | The appearances file: P2 and the incumbent started 40+ games at both first base and designated hitter in each of the last two seasons, and none of the three anywhere else |
| 3 | **Decisive:** eligibility groups from games started; each group's slot plate appearances shared among its regulars in proportion to their projections, capped at each projection | **$4.0M** | — | — |

* **Figure shape.** Every correction lowers the accrual (+63%, +50%, +13%), and the answer is the smallest cell of the grid, so every
  partial application over-accrues.
* **Partial correction priced (L3).** Checking the roster's 5,700 projected plate appearances against the team's 6,200 finds room to
  spare, so nothing binds: rung 1's $6.0M. Grouping by eligibility but on the double-counted P5 accrues $4.5M (+13%).
* **Grid.** Seasons (rows summed, one per player-season) × ceiling (none, listed position, eligibility group) gives 6 cells: $6.5M,
  $5.0M, $4.5M, $6.0M, $4.5M and the answer. The nearest wrong cells sit 13% away, each one omission from the answer.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The memo projects playing time player by player, and the roster lists one position each. No document says a
   player bats only in slots he can fill or that three regulars share two slots.
2. **Corpus blind for a computable reason.** *In every closed season no group of slots outside catcher held more regulars than slots,
   because the club never signed a second regular for a filled position.* Own projections reproduced every non-catcher regular's plate
   appearances within 5%.
3. **No arithmetic symptom.** Plate appearances tie to the lineup cards, seasons to the league's official totals, and the roster's
   projections fit the team's total under every rung.
4. **Not a row predicate.** The ceiling is a sum over a group of slots, the group built from starts by position in another file, and the
   cap falls on the group's combined projections before it reaches any player.
5. **The enumeration is arithmetic.** Which slots a player can fill, and how a crowded group's plate appearances divide, is computed.
   No column says "logjam".
6. **No cutover date.** The signings are this winter's, and no closed series steps; the crowding exists only in the coming season.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The club's lineup cards for ten closed seasons: every plate appearance with its batter and lineup slot.
* **What it certifies.** Slot totals (catcher 600, first base 700, designated hitter 740, the rest 690–700, 6,200 in all), own
  projections at every uncrowded slot within 5%, and backups and call-ups taking the remainder, about 500 a season.
* **Free training instance (O3).** Catchers always share their slot, and in every season they split it in proportion to their
  projections. The pattern is visible every year and harmless, because no catcher has escalators.
* **Twin pair.** Catchers K-11 (2013) and K-19 (2016) are identical on every batting and appearances column: projected at 410 plate
  appearances, the same age and rates. They batted 405 and 205 times (2.0×), because in 2016 a third catcher shared the slot. Own
  projections give both 410; only the shared slot reproduces both.
* **Resemblance points at the decoy.** P1 and P2 resemble the club's past free-agent regulars on every batting column, and every one of
  those reached his projected plate appearances.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The contracts: $500,000 at 475, 550 and 625 plate appearances. The accounting policy: an escalator is accrued when the
  player's projected plate appearances reach it. The projection memo: playing time from the last two seasons, regressed toward a
  part-time baseline. The depth-chart standard: a player may start only at a position he started 20 games at in the last two seasons.
* **Empirical pins.** Slot totals and sharing in proportion to projections, from the lineup cards. Each player's positions, from the
  appearances file.
* **Voices.** The scouting director: "Good hitters find at-bats. It has never been a problem here." The chief financial officer:
  "Accrue what the projections say; that is what the auditors expect."
* **Licensed wrong basis.** The accounting memo records that the club's auditors test escalator accruals against each player's
  plate appearances last season, and will see the accrual on that basis.

## 8. Determinism by construction

* **Thresholds.** Under every rung and grid cell no player's plate appearances fall within 10 of 475, 550 or 625, so rounding of the
  projections cannot move an escalator.
* **Eligibility.** P1, P2 and the incumbent each started more than 40 games at first base or designated hitter, and fewer than 3
  anywhere else, so any start threshold from 5 to 40 gives the same group.
* **Sharing.** Proportional sharing is the only rule the catchers' ten seasons reproduce; equal shares miss every season by more than 60
  plate appearances.
* **Seasons.** The total row equals the sum of a traded player's stints, so taking either gives the same season.
* **Maturity.** The ten closed seasons are complete, and the projections use only finished seasons.

## 9. Prompt sketch and deliverables

> We book the escalator accrual for the five new contracts when they are signed this week, one number in thousands to the nearest
> hundred. Our scouting director says good hitters always find at-bats. Send me `escalator_accrual.xlsx`, a chart `slot_capacity.png`,
> and a one-page `accrual_memo.pdf` that commits to the figure.

* `escalator_accrual.xlsx` — projections, plate appearances and escalators per player under each construction, the on-base sheet (ask
  A) and the call-up sheet (ask B).
* `slot_capacity.png` — each lineup slot's plate appearances as bars, the projected demand of the players eligible for it stacked, the
  first-base and designated-hitter group outlined with its 1,440 ceiling, the escalator thresholds as lines on an inset per signing, and
  the committed accrual labelled.
* `accrual_memo.pdf` — the committed accrual, the two escalators the group ceiling removes, and the auditors' basis.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the five signings, last season's on-base percentage and its rank among regulars.
  *Device:* a sacrifice bunt is a plate appearance but sits outside on-base percentage's denominator, as the scoring rules state.
  Dividing by plate appearances understates two signings' on-base percentage and moves their ranks.
* **Ask B (device-carried).** For each lineup slot, last season's plate appearances by backups and the number of call-ups who batted
  there. *Device:* a player optioned and recalled appears as two roster spells under one ID, and the transactions guide counts call-ups
  as recalls. Counting players undercounts call-ups at four slots. Slot totals come from the lineup cards, not the roster file.
* **Ask C (validity).** The accrual under each of the four rung constructions, with each one's reproduction of the closed seasons'
  regular plate appearances.
* **Decoupling.** Replacing the eligibility group with listed positions changes no figure in asks A or B.

## 11. Rubric arithmetic

5 signings × 2 (ask A) + 9 slots × 2 (ask B) + 4 constructions × 2 (ask C) + the committed accrual, P1's and P2's plate appearances and
the group ceiling + 5 named chart parts + 3 files ≈ 48 criteria.

## 12. World-building constraints

* Projections: P1 650 (1B/DH), P2 590 (1B/DH), P3 600 (CF), P4 640 (SS), P5 600 (LF; 820 with his 2015 counted twice); incumbent 590
  (1B/DH, no escalators).
* Slots: catcher 600, first base 700, designated hitter 740, second 690, third 690, short 690, left 700, centre 690, right 700. The
  roster's projections total 5,700.
* Group sharing: 1,440 / 1,830 = 0.787, giving P1 511, P2 464, incumbent 464. Accruals: $6.5M / $6.0M / $4.5M / $4.0M.
* K-11 and K-19 are identical on every batting and appearances column. Catchers split their slot in proportion every season.
* Sacrifice bunts and optioned spells never touch projections, slot totals or eligibility.
