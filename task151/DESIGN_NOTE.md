# task151: the plate-appearance bonus accrual for five free-agent hitters, booked at signing (architecture 1)

Private, never ships. A new build (wave 4), numbered from seed FC22. The seed (a club accruing, at signing, the
plate-appearance escalators of five free-agent hitters, with three regulars who can bat only at first base or DH) was
read at its header and Situation only. Its world, decision and quantity are kept. Its mechanism is not: the seed files
the projection method (playing time from the last two seasons regressed toward a part-time baseline), which makes the
decisive step rule application, and its shared first-base and DH ceiling is a shared-pool driver already spent
(task106's return legs, task140's residual tier, task16's per-cell floors). The ceiling stays as texture, fixed by the
club's depth chart. The pitfall is re-found from how a hitter's season of plate appearances comes to exist: a planned
everyday regular starts nearly every game or loses one long block of the schedule to the injured list (some of it
before opening day), and each start is worth the plate appearances his lineup slot comes up, about 4.4 batting fourth
and 3.8 batting ninth.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task151.json`, architecture v1, registered 2026-10-16, updated at the build; `guard.py check` and `heart` WARN (overuse.objective, repeat.gate_g), answered below; nearest drivers 0.06 (task105 v1 lineage), 0.05 (task132) and under |
| Domain / task type | `general-statistics-data-science` (client domain), task type `resampling-simulation-monte-carlo-methods` (serves Forecasting): the bonus accrual is the expectation of a stepped payout, worked by resampling comparable seasons, and the step is which unit is resampled (a whole season of a regular planned in the winter, injured-list blocks included) and at what rate its starts are read (the new lineup slot's). Economics is not the owner (the call is a club's accrual, corporate finance, and the economics task types are macro, choice and causal designs); the seed's Economics label is a house domain that maps to Economics & Econometrics |
| Objective | Forecasting & Predictive Modeling: the expected bonus payments for the 2027 regular season, a season not begun at the decision (the contracts were signed between November 24 and December 10, 2026, and the accrual is booked in the December close) |
| Shape | `other`: one committed figure (the accrual) built from five players' accruals, each the sum of its bonuses' chances, plus two ask tables and a memo (arithmetic in `## Ask sheet`) |
| Decision | `quantity_figure`, answer unit `currency` (US dollars) |
| Mechanism | gap population (decisive: the comparison seasons are whole seasons of every regular planned in the winter, read at the new slot's rate, not the player's own seasons, not the regulars who opened or completed the season) with time (the accrual is assessed at signing, so the injured-list blocks before opening day are in the window); pattern none; generators G1 (the payout is on steps of a bounded total, so its value is the chances of clearing each step, not the steps a projection reaches), G9 (the regulars who opened the season or qualified are the survivors of the blocks), G13 (the window runs from signing, not from opening day); Gate G `forecasting`; strategy `other` |
| Layer 2 family / pattern | `forecast_uncertainty`; `own:stepped-bonus-chances-from-winter-planned-regular-seasons-at-the-new-slot-rate`. The library line nearest it is the task type's first (resample the independent unit, not rows); here the unit is a planned regular's whole season and the reading rate is the slot's, so the line is a frame, not the step |
| Furniture | forum `other` (the controller books it; no committee), forcing event `period_close` (the December close books the accrual at signing), organisation family `other` (a professional baseball club), role family `finance_controller` (the club's controller), context artifact `register` (the club's player contract register and term sheets), calibration `none`, opening `question-first`, question form `how-much` |
| Spine | the League Statistics Feed's box-score batting lines, one row per player per championship-season game with his lineup slot and position, 2021 to 2026 in two layouts across the League's 2025 platform change: `lsf_batting_2021_2024.txt` (184,137 rows) and `lsf_batting_2025_2026.csv` (92,038 rows), 276,175 in all (constructed) |
| Deliverables | `pa_bonus_accrual_2027.xlsx` (the accrual by line, player and in total, the two ask tables, notes), `pa_bonus_accrual_memo_2027.docx` (one page for the audit file) |
| People | drawn with `guard.py names --geo "United States" --seed 151` (first names checked clean): Harry Barnes (controller, author of the golden memo; not in the prompt or the pack), Steven Armstrong (assistant general manager, baseball operations, who updated the depth chart), Matthew Wallace (payroll contact in the contract register). The players' names come from the generator's origin-weighted pools and are on the card (`guard.py surface`) |

**Guard.** `guard.py check` and `heart` on the card: WARN `overuse.objective` (Forecasting in 7 of the last 12: this is
the Forecasting lane) and `repeat.gate_g` (forecasting beside task150, a cohort-component school projection that shares no
other axis: gap time there, population here; G6 there, G1 here; a demographer's flows there, a stepped payout here). The
first draft (gap objective, decisive G1) blocked on `test.same_puzzle_older` against task140; the objective gap in
`stumping` 1.4 is the binding-constraint gap, which this build is not, so the honest reading is gap population with
time second, and nothing in the last twelve or older carries population, G1 and `quantity_figure` (task184 is
population, G1, a ranked slate). Banned against the last three (task149, task148, task150) and avoided: the strategies
forecast_method_backtest and population_selection, generators G14, G16 and G6, shapes 02 and 05, forums executive_team,
board_of_directors and trustees_or_governors, forcing events purchase_order_or_contract, budget_or_appropriation and
vote_or_meeting, the capacity_report, published_series and filed_standard artifacts. `guard.py surface` promotes
nothing (nearest task38, task32 and task147 at surface 0.100, no shared gap or pattern); its people screen WARNs that
the first name Kevin (Kevin Weeks, a signing) appears in one older build (task73): a player's name in a different
world, harmless; "Raleigh Oaks", read by the screen as a name, is the club (on the card's invented names).

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
man about 3.8), and the season's lost games as gaps: a planned everyday regular who stays healthy starts 150 to 160 of
162, one who is hurt loses a block of weeks, and about one in six of the regulars the clubs planned in the winter
missed his club's first game; so a signing's chance of reaching a plate-appearance line is the share of planned
regulars' seasons whose starts clear the line at his new slot's rate, and his own record (earned at the top of another
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

**World.** A fictional league of 30 clubs in mid-sized North American metros (every club, player, vendor and person
fictional). The Raleigh Oaks signed five free-agent hitters between November 24 and December 10, 2026, each contract
carrying plate-appearance bonuses for the 2027 season (amounts and lines differ by contract). The club's accounting
policy FIN-14 accrues a playing-time bonus at signing at its expected amount for the season it covers. Baseball
Operations' depth chart of December 10, 2026 bats the five fourth, fifth, sixth, seventh and ninth; four of them batted
higher for their old clubs in 2026 (two led off). Two of the five are first basemen; the club's incumbent first baseman,
under contract for 2027, moves to the bench, and the depth chart plays one newcomer at first and the other at DH. The
controller's files: the term sheets, the policy, the depth chart, the League Statistics Feed (box scores from 2021, the
player ID crosswalk, the club directory, the calendar, the transaction wire), the League office's weekly injured-list
report, rules excerpt and 2027 schedule, the projection vendor's winter depth charts and hitter projections, and the
club's contract register, payroll export, HRIS employee map and earning codes. As-of: Friday December 11, 2026.

## Default path

1. Read the five contracts' plate-appearance bonuses (each bonus's amount and threshold) from the term sheets.
2. Take each signing's projected 2027 plate appearances from the projection vendor's file (or from his own last three
   seasons in the box scores, two layouts stitched through the crosswalk).
3. Take the projection's error from its past misses (the vendor's 2022 to 2026 projections against the box-score totals
   of the regulars in its winter depth charts) as a normal band around each projection.
4. Accrue each bonus at its amount times the band's chance of clearing the threshold, and add the five.

Ends on: $4,750,000 ($4,660,655 before rounding).
Golden: $3,500,000 ($3,495,938 before rounding).

## Stump sentence

Pricing each signing's bonuses off the vendor's projected 2027 plate appearances with a normal band from the
projection's past misses accrues $4,750,000 (Ends on); the step that lands it there is reading each player off his own
record, earned higher in his old club's batting order and spread symmetrically around a mean, when his 2027 total is his
new lineup slot's plate appearances per start times the starts a regular the clubs planned in the winter makes, a
near-full season or one long injured-list block (opening day's included), which accrues $3,500,000.

## Three rules

- **Task type:** general-statistics-data-science, resampling-simulation-monte-carlo-methods (serves Forecasting): the
  accrual is the expectation of a stepped payout over each signing's 2027 plate appearances, taken by resampling
  comparable seasons; the unit resampled is a whole season of a regular the clubs planned in the winter (the starts he
  lost before opening day and in long injured-list blocks included), and each resampled season's starts are read at the
  plate appearances per start of the lineup slot the club gives the signing.
- **Domain test:** the deciding quantity is each signing's predictive distribution of 2027 plate appearances at his
  bonus lines, which a resampling of comparable seasons gets only when the unit resampled is a winter-planned regular's
  whole season and its starts are read at the new slot's rate per start; replacing it with the generic summary of the
  player's record (a projection and its error as a normal band) moves the accrual from $3,500,000 to $4,750,000, and
  with another field's nouns there is no batting order fixing a rate per start and no 162-game schedule that planned
  regulars play out or lose in blocks.
- **Swap:** "how much should we accrue for the quota bonuses of our five new account executives" keeps a stepped
  bonus, but a rep has no batting order that fixes how many chances a working day brings, no 162-game schedule that a
  planned everyday player either plays out or loses in one long block, and no winter plan whose members can be followed
  through a season, so the quantity that decides here (the share of planned regulars' seasons whose starts clear a line
  at the new slot's rate) has nothing to attach to; and in the method swap, the projection with a normal band files
  $4,750,000 against $3,500,000.
- **Layer 1:** the box scores in two layouts across the League's 2025 platform change (2021-2024 pipe-delimited with
  CRLF ends, legacy player and club codes, numeric positions, US dates and the plate-appearance components AB, BB, HBP,
  SH, SF and CI with no PA field; 2025-2026 comma-separated with league player IDs, platform team IDs, ISO dates, a PA
  field, batting-order codes of slot times 100 plus entry and a substitute flag), joined through the League's crosswalk
  (names without accents); doubleheaders as two games on one date; suspended games carried under the date they began
  with a completion date; postponed games played on make-up dates; players traded mid-season appearing for two clubs;
  the vendor's winter depth-chart archive (one sheet per season, its own club abbreviations for seven clubs, positions
  with DH, batting order, bench rows); the term sheets as a PDF; on the ask side, the transaction wire, the weekly
  injured-list report, the payroll export across the January 2025 HRIS migration, the earning codes and the contract
  register (Ask sheet). Each is what these systems write; none moves the call (R2 assertions in `checks.py`).
- **Layer 2:** `forecast_uncertainty`, the expectation of a stepped payout from the right predictive distribution: each
  signing's 2027 plate appearances are his new slot's rate per start times the starts a winter-planned regular makes,
  the starts taken whole from the 1,440 seasons of the 2021-2026 winter-planned non-catcher regulars (379 of them 155
  starts or more, 242 under 100, about one in six missing his club's first game); the data rejects each rival out of
  sample (the projection's normal band, the player's own seasons, the regulars at the player's old rate, the regulars
  who opened the season or qualified, the catchers kept in).
- **Decisive step:** pricing each bonus line at the share of the winter-planned regulars' whole seasons whose starts,
  read at the signing's new lineup slot's plate appearances per start, clear the line: the season distribution, not a
  projection or a band around one; the new slot's rate, not the player's own rate from his old club; the regulars the
  clubs planned in the winter, not the ones who opened or finished the season whole.
- **Not semantics:** no field, code, unit or definition says how plate appearances follow from starts and slots or which
  seasons are comparable; the contracts' plate-appearance definition, the policy's expected amount, the depth chart's
  slots and every feed field are read correctly on the easy route too, and an analyst who reads every one of them
  correctly and prices the bonuses off each player's projected plate appearances with a normal band files $4,750,000.
- **Not rule application:** the strict rule 3 test on every shipped sentence that bears on how the figure is computed:
  the prompt; FIN-14 4.1 to 4.4 (scope; each bonus at its amount times the probability, assessed at signing, that the
  player reaches its threshold in the championship season; the player taken as staying with the Club for the season in
  the role it plans; quarter-end remeasurement); the term sheets' bonus clauses and their plate-appearance definition;
  the depth chart's legend (lineup, batting order and roles as planned); the feed notes; the vendor charts' header line.
  Executed word for word they fix the target (each bonus's expected amount for 2027 as at signing) and give no
  probability: none names a distribution, a comparison set, a rate per start or how starts are lost (R3s), and the one
  literal combination they admit with the field's ready projection (each bonus counted if the vendor's projection
  reaches it) files $5,750,000. The behaviour the decisive step turns on (a rate per start set by the slot, starts lost
  in whole blocks, some before opening day) is inferred from the data, and the data rejects the rivals by a visible
  margin (Ladder, back-test).
- **Analyst test:** a strong analyst who reads the five term sheets, FIN-14 and the depth chart correctly and prices
  each bonus off each signing's projected 2027 plate appearances with a normal band from the projection's past misses
  files $4,750,000 (Ends on); counting the lines the projection reaches files $5,750,000, the league's regulars' seasons
  at each player's own old-club rate per start $4,500,000, the qualified regulars $4,750,000, the planned regulars who
  opened the season $3,750,000, the opening-day lineups $3,250,000, the catchers kept in $3,250,000 and the new slot's
  rate with a normal band $3,000,000; only the winter-planned non-catcher regulars' whole seasons read at the new slot's
  rate file $3,500,000 (executed in `checks.py` on the clean truth and on the pack, R3a and R3b).
- **Estimand:** FIN-14 4.2 and 4.3 with the prompt: for each of the five contracts, each plate-appearance bonus's amount
  times the probability, assessed at the date the contract was signed, that the player reaches its plate-appearance
  threshold in the 2027 championship season, plate appearances as the term sheets define them and the player taken as
  remaining with the Club for the season in the role it plans for him, added by player and over the five; in
  `target/FIN-14_player_compensation_accounting_policy.pdf`. Population (the five contracts' fifteen bonus lines),
  outcome (each line reached), window (the 2027 championship season, as assessed at signing), unit (US dollars) and
  comparison (the expected amount, not the amount at an expected total) are filed; the method is not.
- **No decoy:** no memo, earlier accrual, consultant estimate, agent's figure or stakeholder number states or argues an
  accrual or a probability; the vendor's projections are a mean playing-time forecast that answers no bonus question (a
  declared distractor); the depth chart gives roles and slots; the 2027 schedule ranks nothing.
- **No certified replay:** nothing certified or published is reproduced to recover a method; the season distribution and
  the slot rates are estimated from the raw box scores and the vendor's winter depth charts, and any back-test is the
  analyst's own on the history.
- **Lesson:** a stepped payout on a capped season total is worth the chances of clearing each step, and those chances
  belong to the distribution of whole seasons of comparable planned units read at the unit's new rate, so the generic
  summary (a projection and its error band) and every own-history or survivor population misplace the steps; no build
  on file prices a stepped payout from a bounded total's season distribution at a new rate (task142's compound
  percentile and task143's shared-error threshold are the nearest, and neither is this).

## Readability screen

Six tests per rung (`stumping` 2.1): 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the vendor's projected plate appearances, a bonus counted if the projection reaches its line | no | yes: the projection column | yes: the point forecast | no | no | yes | readable |
| R0a (the default path) the vendor's projection with a normal band from its past misses | no | yes | yes: the band | no | no | yes | readable |
| R0b each player's own last seasons (his seasons as the draws, or their mean with a band) | no | yes: the box scores | yes: the player's record | no | no | yes | readable |
| R1 the league's regulars' seasons at each player's own old-club plate appearances per start | no | no | yes: a season distribution | no | no | no | readable |
| R1b the new slot's rate with a normal band, or at the mean or median starts | no | yes: the lineup slot field | yes: the slot allocation | no | no | yes | readable |
| R1c the vendor's projection rescaled to the new slot, with a band | no | yes | yes: the slot adjustment | no | no | yes | readable |
| R2a the regulars who qualified (502 plate appearances), had 400, or started 100 games | no | yes: a filter | yes: "regulars" by playing time | no | no | no | readable |
| R2b the opening-day lineups (the fill-ins for injured regulars in, the injured regulars out) | no | yes: the first game's lineup | yes: opening day as the plan | no | no | no | readable |
| R2c the winter depth charts' nine with the catchers kept in | no | yes: the depth chart | no | no | no | no | silent |
| R3 (decisive) the winter-planned non-catcher regulars' whole seasons, read at the new slot's plate appearances per start | no: no sentence names a distribution, a comparison set, a rate per start or how starts are lost | no: no column holds a season's starts or a planned role's outcome; the seasons come from joining the vendor's winter depth charts to six seasons of box scores in two layouts through the crosswalk | no: the reflexes are the projection, the band, the player's own record and regulars by playing time | no: no projection of 2027 starts, control total or certified figure ships | no: nothing in the files is wrong | no: a season-by-season starts table, a slot rate table, then each line's share | silent |

## Semantic fork table

Every row is asserted in `generator/checks.py` under its id.

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "accrue at signing" | the expected amount assessed at each contract's signing date | an accrual struck at the December 11 close | same call (nothing bearing on the five arrives between the signings and December 11: no batting line after the 2026 season, no move for the five after the November 3 reinstatement, the depth chart of December 10) | FIN-14 4.2 ("assessed at the date the contract is signed") |
| SF2 | "the plate-appearance bonuses in our five free-agent hitters' 2027 contracts" | the fifteen plate-appearance bonus lines in the five term sheets | other bonuses (awards, innings) | not in the five term sheets | the prompt; the term sheets' bonus rows |
| SF3 | "plate appearances" | championship-season plate appearances for the Club, as the League's official statistics count them | with postseason or rehabilitation plate appearances | not the contract's measure | each term sheet's plate-appearance definition; the feed carries championship-season games only |
| SF4 | the season | the 2027 championship season | later seasons of the multi-year contracts | none to accrue (no plate-appearance bonuses in later seasons) | the four multi-year term sheets ("No plate-appearance bonuses in later seasons") |
| SF5 | "expected amount" | each bonus times the probability its line is reached | the bonus counted if the expected plate appearances reach the line | $2,500,000 or $4,250,000 (mean or median starts), not the policy's measure | FIN-14 4.2 ("the amount of the bonus multiplied by the probability that the player reaches its threshold") |
| SF6 | trades | the player taken as staying with the Club for the season | a trade probability netted out | not the policy's assumption | FIN-14 4.3 |
| SF7 | the role | as the Club's December 10, 2026 depth chart plans it (fourth, fifth, sixth, seventh, ninth) | another plan, a platoon or a role contest | not the Club's plan | FIN-14 4.3 ("in the role the Club plans for him at the date of signing"); the depth chart |
| SF8 | rounding path | each player's unrounded expected amount, the total from the unrounded amounts, each rounded once | the total of the rounded player figures | same call (both $3,500,000, asserted) | the prompt (each figure's rounding stated) |
| SF9 | the memo's figures | the accrual and each player's amount as in the workbook | other figures | same figures (asserted) | the prompt |
| SF10 | the as-of | December 11, 2026, every file pulled that day | a later pull | same call | the export manifest; every file stamped with the pull |

## Ladder

Built figures (from `generator/calc.py` on the shipped files, asserted in `generator/checks.py`); every figure is the
accrual in US dollars for the five signings' 2027 plate-appearance bonuses, rounded to $250,000, with its distance from
the golden in $250,000 bins. The five, as the depth chart bats them: Calderón fourth (fourth for his old club), Weeks
fifth (second), Figueroa sixth (third), Dobbs seventh (first), Harlow ninth (first).

| Rung | Construction | Accrual | Bins | Dies to |
|---|---|---|---|---|
| R0 | the vendor's projection, a bonus counted if it reaches its line | $5,750,000 | +9.26 | FIN-14 4.2 (a probability, not a projection reaching a line); and the projection is each player's old-club record regressed |
| R0a (default) | the vendor's projection with a normal band from its 2022-2026 misses on the depth-chart regulars | $4,750,000 | +4.66 | out of sample the band misses the share of regulars reaching 500, 550 and 600 by 8 to 15 standard errors; the projection carries the old slot's rate and the five's healthy recent seasons |
| R0b | each player's own 2024-2026 seasons as the draws; their mean with a band; their starts at the new slot | $5,750,000; $5,000,000; $4,750,000 | +9.26; +5.55; +5.12 | three draws of a block process; a planned regular's starts in one season say nothing about the next (correlation -0.039 over 943 pairs) |
| R1 | the regulars' seasons at each player's own old-club rate per start | $4,500,000 | +4.14 | the slot fixes the rate: plate appearances per start fall from 4.73 batting first to 3.84 batting ninth, in every season |
| R1b | the regulars' seasons at the old rate as a normal band | $4,000,000 | +2.22 | two errors; the band and the old rate each die as above |
| R1c | the new slot's rate with a normal band | $3,000,000 | -1.98 | the starts are a near-full season or a long block, not a symmetric spread (the band misses the 550 and 600 shares by 4.4 and 4.3 standard errors out of sample) |
| R1d | the new slot's rate at the mean or the median starts | $2,500,000 or $4,250,000 | -4.14 or +2.94 | a point at the steps (SF5) |
| R1e | the new slot's rate with starts drawn game by game at the regulars' average availability | $2,750,000 | -2.62 | games are lost in blocks, not one at a time |
| R1f | the vendor's projection rescaled to the new slot, with its band | $3,750,000 | +1.29 | the band, as R0a |
| R1g | the planned regulars' own plate appearances, no slot | $4,000,000 | +1.57 | mixes every slot's rate |
| R1h | plate appearances per appearance and appearances for starts (substitute lines counted as starts) | $3,000,000 | -1.76 | a substitute's line is not a start; the per-start rate is the starters' |
| R2a | hitters who qualified (502 plate appearances), had 400, or started 100 games | $4,750,000; $3,750,000; $4,000,000 | +4.81; +1.42; +2.30 | selects on the outcome: the injured seasons fail the filter |
| R2b | the opening-day lineups' non-catchers | $3,250,000 | -1.18 | drops the regulars hurt in spring training and keeps the fill-ins who started in their place |
| R2b' | the planned regulars who opened the season | $3,750,000 | +1.33 | survivors of the spring blocks (17.1 per cent of planned regulars missed the first game) |
| R2c | the winter depth charts' nine, catchers kept in | $3,250,000 | -1.28 | a catcher's starts are capped by the position; none of the five catches |
| golden (R3) | the winter-planned non-catcher regulars' whole seasons at the new slot's rate per start | $3,500,000 | 0 | (the golden) |

- **Every construction of the golden** (C1, asserted, L4): the seasons from 2022, 2023, 2024 or 2025 (+3,112, -52,385,
  -46,757, -29,083 against the unrounded golden); slot rates from 2024-2026 or 2025-2026 (-12,542); ages within two or
  three years of each signing, or 30 to 34 (-27,354, -34,728, +36,633); each comparable season's own plate appearances
  rescaled to the new slot (-8,368), or its starting plate appearances (-9,507); the planned regulars who batted at the
  new slot, their own plate appearances (+43,854); the club's own plate appearances per start (+43,715); the player with
  the most starts at each club's position (+55,014) or the eight non-catchers with most starts per club (+51,410): one
  rounded accrual and the same five player figures every time. Two loose regular sets also round alike, though not
  constructions of the method: hitters with 81 or more starts (+93,043) and with 300 or more plate appearances
  (-109,388).
- **One sigma.** Bootstrap of the comparison seasons (300 draws): standard deviation $67,563 against the golden's
  -$4,062 from its bin's centre, so a one-sigma move keeps $3,500,000; each player's figure (standard deviation $11,579
  to $16,890) sits within $12,000 of its $100,000 centre (698,785; 788,750; 806,597; 603,556; 598,250) and keeps its
  rounding at one sigma (L3).
- **The data rejects the default and every rival** (BT1 to BT7): fitted on 2021-2023 and scored on the 720 planned
  regulars of 2024-2026, the season distribution at each regular's slot predicts the share reaching 500, 550 and 600
  plate appearances within 1.0, 1.3 and 1.2 standard errors, the normal band at the slot misses by -3.4, -4.4 and -4.3,
  and the vendor's projection with its band by -14.5, -11.8 and -8.5; plate appearances per start fall down the order in
  every season; a regular's starts do not persist from one season to the next; 17.1 per cent of the winter-planned
  regulars missed his club's first game.
- **Position and dominance.** The decisive construction moves every player's figure; the nearest rivals sit 1.18 bins
  (the opening-day lineups) and 1.28 bins (catchers kept in) below and 1.29 bins (the rescaled projection) above, every
  other one further, on both sides (L5, L6).
- **Worth.** Graded: the total accrual and each player's accrual; never an intermediate a valid method could skip.

## Closure table

Each row's assertion is in `checks.py` (C1 to C22).

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the fifteen plate-appearance bonus lines of the five 2027 term sheets | filed (prompt, term sheets); SF2 |
| 2 | Unit of account | US dollars, one bonus line at a time | filed (term sheets, FIN-14 4.2) |
| 3 | Attribution window | the 2027 championship season | filed (term sheets, FIN-14 4.2); SF4 |
| 4 | As-of dating | assessed at each signing date; files pulled December 11, 2026 | FIN-14 4.2; export manifest; SF1 |
| 5 | Version basis | one term sheet a contract; one depth chart | asserted (no superseded version of either ships) |
| 6 | Denominator | the probability's base: the comparable seasons | design; every construction rounds alike (L4) |
| 7 | Weighting | each comparable season once | C1 asserted (age-matched variants) |
| 8 | Window length | the history 2021-2026 | C1 across windows |
| 9 | Boundary inclusivity | a line reached at exactly its threshold | filed (term sheets: "reaches its threshold"); strict and inclusive readings round alike |
| 10 | Rounding path | unrounded amounts, each figure rounded once | prompt; SF8 |
| 11 | Tie-break | none arises | not applicable, asserted (no two of the five share a slot) |
| 12 | Maturity and censoring | every history season complete | asserted (162 games for every club in every season) |
| 13 | Order of operations | seasons, slot rates, each line's share, amounts, sums | design; rounding the line amounts first gives the same total |
| 14 | Row order | none matters | asserted (lines read reversed) |
| 15 | Duplicate resolution | one batting line per player per game | asserted in both layouts |
| 16 | Identity normalisation | legacy codes to League IDs through the crosswalk | the crosswalk; asserted complete |
| 17 | Netting against gross | none | asserted (no negative count) |
| 18 | Dimensional units | plate appearances, starts, dollars | the feed notes; platform plate appearances equal their components |
| 19 | Code and status semantics | positions, batting-order codes, starters | the feed notes; nine starters per club per game in both layouts; never the stump |
| 20 | Integerisation | none (dollars to the rounding) | prompt |
| 21 | Clause scope | FIN-14 4.1 covers plate-appearance bonuses | filed |
| 22 | Forward window contents | the 2027 season's 162 games, the depth chart's nine | the 2027 schedule (162 games a club) and the depth chart |

## Literal reader

Executing the prompt, FIN-14, the term sheets, the depth chart and the feed notes word for word fixes the target (each
bonus's amount times the probability, as at signing, that the player reaches its line in the 2027 championship season,
staying with the Club in its planned role) and the arithmetic from the probabilities to the totals; it leaves only how
the probability is estimated, and every reading of every term converges on the golden or violates a quoted line (SF1 to
SF10). The easy answers come from easy methods on the same literal target (a projection and a band, the player's own
record, regulars by playing time or at opening day), never from another reading.

## Oracles

- The vendor's 2027 projections and its past projections: a mean playing-time forecast per hitter; under every method
  they confirm only that the five project to 581 to 700 plate appearances; they tie to nothing the golden computes and
  rank nothing on the accrual (a declared distractor, and deleting it leaves the golden and both asks, D1).
- The box scores and the winter depth charts themselves: the history every method fits; nothing in them ties only under
  the golden.
- The 2027 schedule: 162 games a club under every method (a declared distractor).
- Nothing ties only under the golden: no 2027 projection of starts, no control total and no certified figure ships.

## Ask sheet

**Main call's declared row population:** the two box-score files (every row and column the golden reads: player, game,
date, club, lineup slot, starter, plate appearances or their components), the crosswalk, the club directory, the
vendor's winter depth charts, the five term sheets, the 2027 depth chart, FIN-14 and the feed notes. Device and hazard
rows in it: 0 (asserted, SEP1 to SEP3: the call computed from those files alone is the golden; the transaction wire, the
weekly report, the rules excerpt, the calendar, the payroll export, the HRIS map, the earning codes and the contract
register are read only by the asks; no main-call document carries an ask's organ). Neither ask is keyed to the call,
its construction or its figures; they share no primary device.

**Ask A. Every injured-list stint the five have had since the start of the 2024 season: the date it took effect and the
regular-season days it covered** (nine stints, 18 figures).
- H18 home: the injury record behind the accrual, in the audit file beside it: a measure every signing carries that
  the call does not turn on (the golden reads other players' seasons, never the five's injuries).
- The unit, filed once in the League's rules excerpt (Article 22), in the League's voice: the minimum periods (22.2), a
  transfer, a rehabilitation assignment or an assignment of the contract does not end the placement (22.3 to 22.5),
  reinstatement ends it (22.6), days counted from the date the placement takes effect through the day before
  reinstatement (22.7), the paternity and bereavement lists not injured lists (22.8), the weekly report's contents
  (22.9); the championship season from Opening Day through the last scheduled day (the feed notes and the calendar).
- Primary device A1 (D7, the true key in another field, split evidence): the transaction wire dates each move on the
  day the club made it, and the weekly report's "placed" column carries the same transaction date; every one of the
  five's placements took effect one to three days earlier, a date only the report's first date of reinstatement less
  the list's minimum period (22.2) gives. The natural path and the cracker's (the move's date as the date it took
  effect) miss every date and every day count (A3b, CR1). Fair: for all 7,369 report rows the derived date is the true
  date the stint took effect (A4). The internal inconsistency that finds it: a 10-day placement whose first date of
  reinstatement is eight or nine days after it.
- Hazards: HA1 a spring placement (took effect March 25, 2025, two days before Opening Day; days from Opening Day);
  HA2 a stint open at the 2026 season's end, reinstated November 3 (days through the last scheduled day); HA3
  rehabilitation assignments inside two stints; HA4 a paternity-list move (not an injured list); HA5 the 7-day concussion
  list (an injured list); HA6 a trade while on the list (one stint); HA7 a 10-day to 60-day transfer written on the wire
  as a fresh placement (splitting it adds rows); HA8 two stints six days apart (merging them drops one); HA9 a pitcher
  who shares one signing's name (found by name, his two stints join the table).
- Stops (measured): the move dates (9 rows, every figure off); every placement a stint (11 rows); stints a week apart
  merged (8 rows); the moves found by name (11 rows); the golden.
- Span: the transaction wire, the weekly report, the rules excerpt, the calendar, the vendor charts (the five's League
  IDs), the term sheets (the five's names) (6 files); about 12 columns.
- Realism: a transaction wire records the day a club makes a move; an injured-list placement can take effect before the
  transaction; the League office's report lists the transaction and the first date of eligibility; a legacy roster
  system logged a list change as a new placement.

**Ask B. The plate-appearance bonuses the club paid for each of the 2024, 2025 and 2026 seasons, player by player and in
total** (seven player rows and three totals, 10 figures).
- H18 home: the club's own record on the bonuses it accrues, an audit trail of the same liability, rows the call never
  reads; in payroll's words.
- The unit, filed in the contract register's notes, in the system owner's voice: plate-appearance and games-started
  bonuses are earned in the championship season and paid half in the first payroll after the season ends and half on
  the following January 15; pitchers' playing-time bonuses in full after the season.
- Primary device B1 (D5, a category crossed by label): the payroll pays a player's playing-time bonuses for a season
  in one line (the HRIS playing-time code, and before the migration the legacy performance-bonus line), so every
  payment carries the season's plate-appearance and games-started bonuses together; the plate-appearance part is half
  the plate-appearance lines the player reached for the Club, which only the register's terms against the box scores
  separate. The payroll lines at face value miss all ten figures (CR2). Fair: every 2024-2026 playing-time line equals
  half the season's plate-appearance and games-started lines reached for the Club, the legacy October 2024 line to one
  player also carrying his All-Star bonus (B3c, 11 lines).
- Second device B2 (D2, a label stored before a silent switch): before the January 2025 HRIS migration every
  performance bonus went on one legacy code, migrated as "other bonus"; the October 2024 first halves sit there, one of
  them with the season's All-Star bonus in it, the November Silver Slugger bonus on the same code.
- Hazards: HB1 a void and reissue in October 2026 (net once); HB2 legacy employee numbers mapped through the HRIS map;
  HB3 the playing-time code also carries two pitchers' games and innings bonuses; HB4 a contract assigned at the 2025
  deadline (the later lines were the assignee's to pay: the register's lines against the season's plate appearances
  give $675,000 for a player the club paid $225,000); HB5 the 2026 second halves are payable January 15, 2027 (not paid
  at December 11); HB6 the January 2024 halves of the 2023 season (a pay-year grouping moves them into 2024).
- Stops (measured): the lines at face value ($860,000, $405,000, $480,000); the playing-time code by pay year (none for
  2024, $682,500, $882,500); the playing-time code by season ($405,000, $480,000, $680,000); the register's terms
  against plate appearances ($720,000, $775,000, $850,000); face value with the void reversal ignored; the golden
  ($720,000, $325,000, $425,000).
- Span: the payroll export, the HRIS map, the earning codes, the contract register, the box scores and crosswalk
  (plate appearances and starts by club), the vendor charts (the veterans' League IDs) (8 files); about 14 columns.
- Realism: a club pays a season's playing-time bonuses on one line a payroll; an HRIS migration keeps the legacy earning
  codes on migrated history and maps them to the nearest new code; an assigned contract's later bonuses are the
  assignee's.

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 a spring placement | an injury in spring training | Ask A, one stint | +2 days if counted from the date it took effect |
| HA2 a stint open at season's end | a September injury | Ask A, one stint | +36 days if counted to the November reinstatement |
| HA7 a transfer written as a placement | the legacy roster system | Ask A, two stints | splits each into two rows |
| HA8 two stints six days apart | a re-aggravated hamstring | Ask A, one player | merging drops a row |
| HA9 a namesake pitcher | a common name | Ask A, one player | two extra rows if matched by name |
| HB1 a void and reissue | changed bank details | Ask B, 2026 | +one payment if summed gross |
| HB3 pitchers on the playing-time code | one code for all playing-time bonuses | Ask B, 2025 and 2026 totals | +$75,000 and +$200,000 |
| HB4 an assigned contract | the 2025 deadline trade | Ask B, 2025 | +$450,000 on the register path |
| HB5 the 2026 second halves | January payment | Ask B, 2026 | doubles each row on the register path |

**Referee.** For Ask A, the weekly report's first dates of reinstatement and the rules' minimum periods; for Ask B, the
register's terms and the box scores' plate appearances and starts by club. Each is a field the golden reads, not a
control: no file ties only under the golden.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A stints: date taken effect and regular-season days (18) | the filed stint definition executed on the transaction wire (placement to reinstatement, transfers, rehab and trades inside, lists filtered, season caps applied), the date taken effect read as the placement's date on the wire and the report | every date one to three days late, every day count short by as much or more: all 18 off | miss |
| B 2024 player rows and total (3) | the payroll's playing-time and legacy season-end lines at face value, each half to its season, voids netted, pitchers dropped | $470,000, $390,000, $860,000 | miss |
| B 2025 player rows and total (3) | the same path | $275,000, $130,000, $405,000 | miss |
| B 2026 player rows and total (4) | the same path | $210,000, $165,000, $105,000, $480,000 | miss |

Mirror leakage: about 10 per cent of the ask weight (the mirror runs the natural ask paths, the move dates and the
playing-time code by season, and keeps only the workbook's and the memo's structural criteria; no ask figure).
Pair ceiling: 34 (on a rubric of about 35 for the call and the five player accruals, 7 for instructions and 58 for the
asks: the cracker lands the call, 35 plus 7 plus about 5 of structure, 47; the mirror keeps about 5 of the
recommendation's weight plus 7 and 9 of structure, 21; neither keeps an ask figure).

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
- Spring-training injured-list placements at 5 to 13 per cent of winter-planned regulars, with the bench's best player
  filling every absence: the opening-day lineups sat 0.5 to 0.6 of a bin from the golden (the fill-ins started up to 160
  games); set at 16 per cent with a club's answer to a long stint (a bench player at the position about a quarter of the
  time, else a recall from Triple-A, rarely the same one again), the rung sits 1.18 bins clear.
- Injured-list stints shorter than the list's minimum period (an eight-game 10-day stint): a baseball reader would see a
  10-day placement reinstated in eight days; every stint now runs at least its list's minimum from the date it took
  effect, and a transfer to the 60-day list only for a stint of sixty days or more.
- Trades left out of the next season's rosters (a player traded at the deadline back with his old club the next spring):
  the offseason now starts from the rosters as the season ended.
- World seed 151: the history windows and age-matched sets spread about $190,000 around the golden, too wide for one
  bin with the survivor sets inside it; seed 1511 (searched with the contract terms over eight draws) puts every
  construction within $57,000 of the bin's centre, the golden $4,062 from it.
- The weekly report carrying an "on list since" date (the date taken effect, stated): the cracker reads it; the report
  now carries the transaction date and the first date of eligibility, the true date only through 22.2.
- Ask B with the payroll's plate-appearance halves on their own lines (the first design): the cracker's face-value path
  matched every 2025 and 2026 figure; the payroll now pays a season's playing-time bonuses (plate appearances and games
  started) on one line, as one code covers them.
- A platform layout whose only starter marker was the batting-order code: reading every platform line as a start moved
  the call half a bin (a Layer 1 item deciding nothing must not move it); the platform layout now carries its
  substitute flag, and every appearance read as a start in both layouts is a rival 1.76 bins away.
- Contract amounts equal to answer figures (a $500,000 bonus line beside a $500,000 player accrual, $300,000 and
  $450,000 likewise): `leak.py` read them as the answer in the term sheets; amounts moved ($560,000 and $360,000 lines;
  the veterans' $140,000 and $225,000 lines), every golden figure re-asserted.
- Club nicknames shared with real teams (Monarchs, Suns, Colonials, Barons, Grays and nine others): renamed.
- Three Australian names among the club's designed players (one origin drawn three times): designed names are drawn
  apart, no origin outside the United States twice and no shared first name or surname.

## Build record

Stage 3, built 2026-10-16 from `task151/generator/build.py` (world seed 1511).

- Pack: 20 files, 5 formats (csv, json, pdf, txt, xlsx); the spine 276,175 batting lines (`lsf_batting_2021_2024.txt`
  184,137 rows, `lsf_batting_2025_2026.csv` 92,038); distractors `hvbd_hitter_projections_2022_2027.csv` and
  `league_schedule_2027.csv` (metadata.json).
- Main call from the shipped files: $3,500,000 ($3,495,938), players $700,000, $800,000, $800,000, $600,000, $600,000
  (698,785; 788,750; 806,597; 603,556; 598,250); the default (the vendor's projection with a normal band) $4,750,000 on
  the pack and the clean truth alike; every construction one rounded figure and the same five player figures (L4); one
  bootstrap sigma $67,563.
- Mess variants (R2): legacy plate appearances without catcher's interference, doubleheaders merged into one start a
  date, the vendor's accented names dropped, traded regulars' seasons cut to the planning club: the golden in every case.
- Gates: `checks.py` 173 assertions, 0 failed; `verify.py` agrees on its own pandas and pdftotext path (the accrual, the
  five player figures, the default, the step figures, the nine stints and the bonuses paid); two byte-identical builds
  (target, goldens, metadata.json, submission.md, figures.json, target.zip); container audit clean on the pack and the
  goldens; `figures_check.py` 72 figures, 0 absent; `precut.py` exit 0; `voice-check.py` PASS (766 characters);
  `leak.py` REVIEW, no LEAK (answered below); `guard.py heart` WARN (answered under Draw); `guard.py surface` promotes
  nothing, people WARN answered under Draw.
- `leak.py` REVIEW lines, each harmless: the register's "$225,000 each" beside the $225,000 the club paid one
  veteran (one line reached, the register's term is the input); the term sheets carry the call's words (they are the
  contracts the call accrues for); the feed notes carry five of the stump paragraph's terms (they describe the batting
  lines' fields: appearances, league, opening, lineup, batting) and name no method; the projections, the depth charts,
  the wire and the term sheets name the five beside numbers (projected plate appearances, ages, transaction IDs,
  contract terms), none an accrual or a ranking on it; the calendar's and the 2027 schedule's dates after December 11,
  2026 are the 2027 season's (forward-looking by nature).
- Golden realism and house fixes: the workbook's title states the accrual; number formats per column (currency,
  percentages to a tenth, dates), frozen headers, print setup, a total row from the unrounded line amounts, the
  rounding stated, a notes sheet with the as-of, the policy's estimand, the comparison seasons and the sources; source
  and method lines under the ask tables; the memo in the controller's voice with a source line and a note on the
  contracts' plate-appearance definition; the manifest's names equal the shipped set (H9); every file the goldens and
  the write-up cite ships (H8); no record dated after the pull (H16); the veterans' payments on the register's dates
  (H6).
