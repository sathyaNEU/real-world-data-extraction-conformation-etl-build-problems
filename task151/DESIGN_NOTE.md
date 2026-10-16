# task151: the plate-appearance bonus accrual for five free-agent hitters, booked at signing (architecture 1)

Private, never ships. A new build (wave 4), numbered from seed FC22. The seed (a club accruing, at signing, the
plate-appearance escalators of five free-agent hitters, $500,000 at 475, 550 and 625 plate appearances, with three
regulars who can bat only at first base or DH) was read at its header and Situation only. Its world, decision and
quantity are kept. Its mechanism is not: the seed files the projection method (playing time from the last two seasons
regressed toward a part-time baseline), which makes the decisive step rule application, and its shared first-base and
DH ceiling is a shared-pool driver already spent (task106's return legs, task140's residual tier, task16's per-cell
floors). The ceiling stays as texture, fixed by the club's depth chart. The pitfall is re-found from how a hitter's
season of plate appearances comes to exist: a planned everyday regular starts nearly every game or loses one long block
of the schedule to the injured list (some of it before opening day), and each start is worth the plate appearances his
lineup slot comes up, about 4.3 batting fourth and 3.8 batting ninth.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task151.json`, architecture v1, registered 2026-10-16; `guard.py check` WARN (overuse.objective, repeat.gate_g), answered below; nearest drivers 0.05 (task132, task105 v1 lineage) and under |
| Domain / task type | `general-statistics-data-science` (client domain), task type `resampling-simulation-monte-carlo-methods` (serves Forecasting): the bonus accrual is the expectation of a stepped payout, worked by resampling comparable seasons, and the step is which unit is resampled (a whole season of a regular planned in the winter, injured-list blocks included) and at what rate its starts are read (the new lineup slot's). Economics is not the owner (the call is a club's accrual, corporate finance, and the economics task types are macro, choice and causal designs); the seed's Economics label is a house domain that maps to Economics & Econometrics |
| Objective | Forecasting & Predictive Modeling: the expected bonus payments for the 2027 regular season, a season not begun at the decision (the contracts were signed between November 23 and December 11, 2026, and the accrual is booked in the December close) |
| Shape | `other`: one committed figure (the accrual) built from five players' accruals, each the sum of its bonuses' chances, plus two ask tables and a memo (arithmetic in `## Ask sheet`) |
| Decision | `quantity_figure`, answer unit `currency` (US dollars) |
| Mechanism | gap population (decisive: the comparison seasons are whole seasons of every regular planned in the winter, read at the new slot's rate, not the player's own seasons, not the regulars who opened or completed the season) with time (the accrual is assessed at signing, so the injured-list blocks before opening day are in the window); pattern none; generators G1 (the payout is on steps of a bounded total, so its value is the chances of clearing each step, not the steps a projection reaches), G9 (the regulars who opened the season or qualified are the survivors of the blocks), G13 (the window runs from signing, not from opening day); Gate G `forecasting`; strategy `other` |
| Layer 2 family / pattern | `forecast_uncertainty`; `own:stepped-bonus-chances-from-winter-planned-regular-seasons-at-the-new-slot-rate`. The library line nearest it is the task type's first (resample the independent unit, not rows); here the unit is a planned regular's whole season and the reading rate is the slot's, so the line is a frame, not the step |
| Furniture | forum `other` (the controller books it; no committee), forcing event `period_close` (the December close books the accrual at signing), organisation family `other` (a professional baseball club), role family `finance_controller` (the club's controller), context artifact `register` (the club's player contract register and term sheets), calibration `none`, opening `question-first`, question form `how-much` |
| Spine | the league statistics feed's box-score batting lines, one row per player per championship-season game with his lineup slot and position, 2021 to 2026 in two layouts across the league's 2025 platform change (constructed, about 370,000 rows) |
| Deliverables | `escalator_accrual_2027.xlsx` (the accrual by player and in total, the two ask tables), `escalator_accrual_memo_2027.docx` (one page for the audit file) |
| People | drawn with `guard.py names --geo "United States" --seed 151` (first names checked clean): Harry Barnes (controller, the requester; not in the prompt), Steven Armstrong (assistant general manager, baseball operations, who owns the depth chart), Gregory Melton (director of baseball analytics), Karl Rojas (head athletic trainer), Matthew Wallace (payroll manager) |

**Guard.** `guard.py check` on the registered card: WARN `overuse.objective` (Forecasting in 7 of the last 12: this is
the Forecasting lane) and `repeat.gate_g` (forecasting beside task150, a cohort-component school projection that shares no
other axis: gap time there, population here; G6 there, G1 here; a demographer's flows there, a stepped payout here). The
first draft (gap objective, decisive G1) blocked on `test.same_puzzle_older` against task140; the objective gap in
`stumping` 1.4 is the binding-constraint gap, which this build is not, so the honest reading is gap population with
time second, and nothing in the last twelve or older carries population, G1 and `quantity_figure` (task184 is
population, G1, a ranked slate). Banned against the last three (task149, task148, task150) and avoided: the strategies
forecast_method_backtest and population_selection, generators G14, G16 and G6, shapes 02 and 05, forums executive_team,
board_of_directors and trustees_or_governors, forcing events purchase_order_or_contract, budget_or_appropriation and
vote_or_meeting, the capacity_report, published_series and filed_standard artifacts.

**Same-puzzle and same-driver tests.** Decisive gap population, decisive G1, decision `quantity_figure`, Gate G
`forecasting`: no build in the last twelve (task262 to task150) or older carries the triple (gap, pattern, decision) or
(gap, pattern, Gate G).

**Abstraction test.** Stripped of nouns: a stepped payout on one unit's season total is the sum of its chances of
clearing each step; the total is a rate fixed by the position the unit is given times the appearances it makes; units
planned to play every day either make nearly all of them or lose one long block, some before the season; so the chances
come from the appearances of every unit planned the same way at the same point before the season, read at the new
position's rate. Read by mechanism rather than score, the nearest are: task142 (an upper percentile of a quarter's visits
compounded from admissions and stays, the shortcut an independent count: there arrivals compound, here one unit's
bounded total is read at a new rate and no arrivals are compounded); task143 (a shared group effect in the chance the
weakest member falls below a line: here nothing is shared between the five); task97 (a unit's chance set by the
cumulative history of the place it occupies: here the slot fixes only a rate per start and the chance comes from other
units' seasons); task106 and task140 (a shared finite pool, a residual after reservations: here the crowding at first
base and DH is texture the depth chart fixes); task132 (a replacement restarting a wear curve: no replacement here). None
shares the latent structure, the default path and the correction. Differentiation lines for task142, task143, task106
and task97 are on the card.

**Data-native sentence.** A league's box scores record a hitter's season as the games he started, each worth the plate
appearances his lineup slot came up (the order turns over, so the leadoff man bats about 4.7 times a start and the ninth
man about 3.8), and the season's lost games as gaps: a planned everyday regular who stays healthy starts 150 to 158 of
162, one who is hurt loses a block of weeks, and about one in eight of the regulars the clubs planned in the winter was
on the injured list on opening day; so a signing's chance of reaching a plate-appearance line is the share of planned
regulars' seasons whose starts clear the line at his new slot's rate, and his own record (earned at the top of a weaker
club's order, its injured seasons a few draws from that same block process) says little about it.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting` (62 builds): no driver on file prices a
stepped payout from the season distribution of a bounded total read at a new rate (the nearest structures are a
compound percentile, task142; a shared-error threshold, task143; a place's history, task97). `layer2-rigor-patterns.md`:
general statistics, resampling line 1 (resample the independent unit) is the frame for the whole-season unit; Bayesian
line 2 (predict with the predictive, not the mean) is the shortcut the default takes; regression diagnostics line 2
(misfit where the variance moves with the level) is why a normal band fails at the top step.
`two-layer-task-design.md`: "the data's real structure" and "the evidence judged with its uncertainty".
`strategies.md` F7 (who is in the denominator: survivors) and F1 (the window the decision bets on: from signing) are the
family record for the two lower rungs; `measured-drivers.md` (held tasks are compound: a conjunction whose partial
fixes score no better) is why the decisive step is the distribution and the slot together. The seed's header and
Situation (FC22) for the world, decision and quantity only.

**World.** A fictional major league of 30 clubs in mid-sized North American metros (every club, player, vendor and
person fictional). The club, a contender that finished 2026 with an offense near the league's average, signed five
free-agent hitters between November 23 and December 11, 2026, each contract carrying plate-appearance bonuses for the
2027 season (the terms differ by contract). The club's accounting policy accrues a playing-time bonus at signing at its
expected amount for the season it covers. Baseball operations' December 2026 depth chart bats the five fourth, fifth,
sixth, seventh and ninth; four of them batted higher for their old clubs (two led off). Two of the five are first
basemen; the club's incumbent first baseman, under contract for 2027, moves to the bench, and the depth chart plays one
newcomer at first and the other at DH. The controller's files: the contracts, the policy, the depth chart, the league
statistics feed (box scores from 2021), the projection vendor's winter depth charts and its 2027 hitter projections,
the league transactions feed, and the club's payroll export. As-of: Friday December 11, 2026.

## Default path

1. Read the five contracts' plate-appearance bonuses (each bonus's amount and threshold) from the term sheets.
2. Take each signing's projected 2027 plate appearances from the projection vendor's file (or from his own last three
   seasons in the box scores, two layouts stitched through the crosswalk).
3. Take the projection's error from its past misses (the vendor's earlier projections against the box-score totals of
   the regulars they covered) as a normal band around each projection.
4. Accrue each bonus at its amount times the band's chance of clearing the threshold, and add the five.

Ends on: about $4.4 million (prototype; fixed at the build).
Golden: about $3.85 million (prototype; fixed at the build).

## Stump sentence

Pricing each signing's bonuses off his projected 2027 plate appearances with a normal band from the projection's past
misses accrues about $4.4 million (Ends on); the step that lands it there is reading each player off his own record,
earned higher in his old club's batting order and spread symmetrically around a mean, when his 2027 total is his new
lineup slot's rate per start times the starts a regular the clubs planned in the winter makes, a near-full season or
one long injured-list block (opening day's included), which accrues about $3.85 million.

## Tried and rejected

- The seed's mechanism (a filed projection method, playing time from the last two seasons regressed toward a part-time
  baseline): rejected at the draw, a filed method makes the decisive step rule application.
- The seed's shared first-base and DH ceiling as the driver (three hitters' plate appearances drawn from two lineup
  spots): rejected at the draw, a shared finite pool is task106's and task140's driver; kept as texture, the depth chart
  fixing who plays where.
- The step payout alone (the expected value of the bonuses needs the distribution, not the projection reaching the
  line): rejected as the decisive step at the draw, one enumerable insight (Jensen) is the coin-flip signature in
  `measured-drivers.md`; it is the frame, and the decisive construction is the season distribution of planned regulars
  read at the new slot's rate.
- A per-game independent availability model as the default path: rejected at the draw, an independent count against
  blocks is task142's shortcut; it stays a lower rival only.
- A prototype with an age effect on injured-list time and rest (prototype 1): the age-matched comparison sets moved the
  accrual by $170,000 to $360,000 against the pooled set, because the top bonus line sits on the steep part of the starts
  distribution; redrawn with no age effect inside the signings' 30 to 34 (the history shows none), a narrow healthy peak
  (rest and day-to-day absences light), and slots chosen so most lines fall off the peak.
- A prototype where the five kept their old slots or moved both ways (prototypes 2 and 3): the point projection at the
  new slot and the player's own three-year mean with a normal band each landed inside the golden's bin by cancelling
  errors; redrawn so four of the five bat lower for the club than for their old clubs (one change, never uniform: fourth
  to fourth, second to fifth, third to sixth, first to seventh, first to ninth).
- Spring-training injured-list placements at 5 to 9 per cent of winter-planned regulars: the opening-day comparison set
  sat 0.6 to 0.9 of a $250,000 bin from the golden; set at about 13 per cent with a median of about 25 games lost, the
  rung sits clear of the bin.
