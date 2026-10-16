# task151: the plate-appearance bonus accrual for five free-agent hitters, booked at signing (architecture 1)

Private, never ships. A new build (wave 4), numbered from seed FC22. The seed (a club accruing, at signing, the
plate-appearance escalators of five free-agent hitters, with three regulars who can bat only at first base or DH) was
read at its header and Situation only. Its world, decision and quantity are kept. Its mechanism is not: the seed files
the projection method (playing time from the last two seasons regressed toward a part-time baseline), which makes the
decisive step rule application, and its shared first-base and DH ceiling is a shared-pool driver already spent
(task106's return legs, task140's residual tier, task16's per-cell floors). The ceiling stays as texture, fixed by the
club's depth chart. The pitfall is re-found from how a hitter's season of plate appearances comes to exist: a planned
everyday regular starts nearly every game or loses one long block of the schedule to the injured list (some of it
before opening day), and each start is worth the plate appearances his lineup slot comes up, about 4.7 batting first
and 3.8 batting ninth.

**Stage 4 repair, inside architecture 1 (not a re-root).** The determinism judge (round 1,
`determinism_check_report_round1.md`) returned NOT_DETERMINISTIC on the main call: FIN-14 filed the estimand and
nothing filed preferred the golden's basis, so the vendor's projection with a band, the vendor with its residuals and
each player's own seasons stood as defensible. The repair files the adjudication, not the method: FIN-14 4.4 (revised
November 2026, after the auditors' review of the 2025 close, in the controller's voice) chooses the basis by a
look-back: every basis considered is applied to each of the four seasons before the signing with what was published
before it, to the depth charts' starting-lineup hitters with two earlier seasons of 100 plate appearances, and scored
by the average squared difference between its probabilities of 450 to 650 plate appearances and the outcomes. It names
no slot, no starts, no catchers and no modelling step. The decisive step is unchanged (the planned regulars' starts read
at the new slot's rate, catchers apart); only its adjudication is filed, a selection criterion the determinism skill
allows (`determinism-check` 1: a filed selection criterion in general terms that never names the method, never in
consecutive builds; task150 and task148 file none). The same pass took the rule 3 audit's strength finding (the
starting nines' raw seasons landed the call by cancelling errors; now 1.53 to 1.77 bins away on every window) and the
coordinator's five closures (FIN-14 4.3 restated, Ask B's population and attribution filed, one rounding path, Ask A's
effective date filed, the close-file index renamed). The world was redrawn under those constraints (seed 1539, the
signings batting fifth to ninth) and the golden re-derived: $4,250,000.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task151.json`, architecture v1, registered 2026-10-16, updated at the stage 4 repair; `guard.py check` and `heart` WARN (overuse.objective, repeat.gate_g), answered below; nearest drivers 0.06 (task105 v1 lineage), 0.05 (task132) and under |
| Domain / task type | `general-statistics-data-science` (client domain), task type `resampling-simulation-monte-carlo-methods` (serves Forecasting): the bonus accrual is the expectation of a stepped payout, worked by resampling comparable seasons, and the step is which unit is resampled (a whole season of a regular planned in the winter, injured-list blocks included) and at what rate its starts are read (the new lineup slot's). Economics is not the owner (the call is a club's accrual, corporate finance, and the economics task types are macro, choice and causal designs); the seed's Economics label is a house domain that maps to Economics & Econometrics |
| Objective | Forecasting & Predictive Modeling: the expected bonus payments for the 2027 regular season, a season not begun at the decision (the contracts were signed between November 24 and December 10, 2026, and the accrual is booked in the December close) |
| Shape | `other`: one committed figure (the accrual) built from five players' accruals, each the sum of its bonuses' chances, plus two ask tables and a memo (arithmetic in `## Ask sheet`) |
| Decision | `quantity_figure`, answer unit `currency` (US dollars) |
| Mechanism | gap population (decisive: the comparison seasons are whole seasons of every non-catcher regular planned in the winter, read at the new slot's rate, not the player's own seasons, not the starting nines taken whole, not the regulars who opened or completed the season) with time (the accrual is assessed at signing, so the injured-list blocks before opening day are in the window); pattern none; generators G1 (the payout is on steps of a bounded total, so its value is the chances of clearing each step), G9 (the regulars who opened the season or qualified are the survivors of the blocks), G13 (the window runs from signing, not from opening day); Gate G `forecasting`; strategy `other`. Selection organ: the filed look-back of FIN-14 4.4 (a selection criterion in general terms), card note |
| Layer 2 family / pattern | `forecast_uncertainty`; `own:stepped-bonus-chances-from-winter-planned-regular-seasons-at-the-new-slot-rate`. The library line nearest it is the task type's first (resample the independent unit, not rows); here the unit is a planned regular's whole season and the reading rate is the slot's, so the line is a frame, not the step |
| Furniture | forum `other` (the controller books it; no committee), forcing event `period_close` (the December close books the accrual at signing), organisation family `other` (a professional baseball club), role family `finance_controller` (the club's controller), context artifact `register` (the club's player contract register and term sheets), calibration `none`, opening `question-first`, question form `how-much` |
| Spine | the League Statistics Feed's box-score batting lines, one row per player per championship-season game with his lineup slot and position, 2021 to 2026 in two layouts across the League's 2025 platform change: `lsf_batting_2021_2024.txt` (184,271 rows) and `lsf_batting_2025_2026.csv` (92,107 rows), 276,378 in all (constructed) |
| Deliverables | `pa_bonus_accrual_2027.xlsx` (the accrual by line, player and in total, the look-back, the two ask tables, notes), `pa_bonus_accrual_memo_2027.docx` (one page for the audit file) |
| People | drawn with `guard.py names --geo "United States" --seed 151` (first names checked clean): Harry Barnes (controller, author of FIN-14 and of the golden memo; not in the prompt), Steven Armstrong (assistant general manager, baseball operations, who updated the depth chart), Matthew Wallace (payroll contact in the contract register). The players' names come from the generator's origin-weighted pools and are on the card (`guard.py surface`) |

**Guard.** `guard.py check` and `heart` on the card: WARN `overuse.objective` (Forecasting in 7 of the last 12: this is
the Forecasting lane) and `repeat.gate_g` (forecasting beside task150, a cohort-component school projection that shares no
other axis: gap time there, population here; G6 there, G1 here; a demographer's flows there, a stepped payout here). The
first draft (gap objective, decisive G1) blocked on `test.same_puzzle_older` against task140; the objective gap in
`stumping` 1.4 is the binding-constraint gap, which this build is not, so the honest reading is gap population with
time second, and nothing in the last twelve or older carries population, G1 and `quantity_figure`. Banned against the
last three (task149, task148, task150) and avoided: the strategies forecast_method_backtest (task149's tag; the card
keeps `other`, the decisive move being the predictive distribution, and the filed look-back is the selection organ,
which neither task150 nor task148 carries) and population_selection, generators G14, G16 and G6, shapes 02 and 05,
forums executive_team, board_of_directors and trustees_or_governors, forcing events purchase_order_or_contract,
budget_or_appropriation and vote_or_meeting, the capacity_report, published_series and filed_standard artifacts.
`guard.py surface` promotes nothing (nearest task38, task147 and task32 at surface 0.100, no shared gap); its people
screen WARNs that one veteran's first name and surname (Jonathan Vasquez) appear in older builds (task130, task85): a
player's name in a different world, harmless; "Raleigh Oaks", read by the screen as a name, is the club (on the card's
invented names).

**Same-puzzle and same-driver tests.** Decisive gap population, decisive G1, decision `quantity_figure`, Gate G
`forecasting`: no build in the last twelve or older carries the triple (gap, pattern, decision) or (gap, pattern, Gate
G).

**Abstraction test.** Stripped of nouns: a stepped payout on one unit's season total is the sum of its chances of
clearing each step; the total is a rate fixed by the position the unit is given times the appearances it makes; units
planned to play every day either make nearly all of them or lose one long block, some before the season; so the chances
come from the appearances of every unit planned the same way at the same point before the season, read at the new
position's rate, and a filed scoring of candidate bases on past seasons picks that basis without naming it. Read by
mechanism rather than score, the nearest are: task142 (an upper percentile of a quarter's visits compounded from
admissions and stays: there arrivals compound, here one unit's bounded total is read at a new rate); task143 (a shared
group effect in the chance the weakest member falls below a line: here nothing is shared between the five); task97 (a
unit's chance set by the cumulative history of the place it occupies: here the slot fixes only a rate per start and the
chance comes from other units' seasons); task106 and task140 (a shared finite pool: here the crowding at first base and
DH is texture the depth chart fixes); task132 (a replacement restarting a wear curve: no replacement here). None shares
the latent structure, the default path and the correction. Differentiation lines are on the card.

**Data-native sentence.** A league's box scores record a hitter's season as the games he started, each worth the plate
appearances his lineup slot came up (the order turns over, so the leadoff man bats about 4.7 times a start and the ninth
man about 3.8), and the season's lost games as gaps: a planned everyday regular who stays healthy starts 150 to 160 of
162, one who is hurt loses a block of weeks, and about one in six of the regulars the clubs planned in the winter
missed his club's first game; so a signing's chance of reaching a plate-appearance line is the share of planned
regulars' seasons whose starts clear the line at his new slot's rate, and his own record (earned higher in another
club's order, its injured seasons a few draws from that same block process) says little about it, which the policy's
look-back over the last four seasons shows.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting` (62 builds): no driver on file prices a
stepped payout from the season distribution of a bounded total read at a new rate. `layer2-rigor-patterns.md`:
general statistics, resampling line 1 (resample the independent unit) is the frame for the whole-season unit; Bayesian
line 2 (predict with the predictive, not the mean) is the shortcut the band takes. `two-layer-task-design.md`: "the
data's real structure" and "the evidence judged with its uncertainty". `determinism-check` 1 and
`references/forcing-the-answer.md` Part 5 for the filed selection criterion. `strategies.md` F7 (survivors in the
denominator) and F1 (the window from signing) for two lower rungs; `measured-drivers.md` (held tasks are compound: a
conjunction whose partial fixes score no better) is why the decisive step is the population, the slot and the shape
together. The seed's header and Situation (FC22) for the world, decision and quantity only.

**World.** A fictional league of 30 clubs in mid-sized North American metros (every club, player, vendor and person
fictional). The Raleigh Oaks signed five free-agent hitters between November 24 and December 10, 2026, each contract
carrying plate-appearance bonuses for the 2027 season (amounts and lines differ by contract). The club's accounting
policy FIN-14 accrues a playing-time bonus at signing at its expected amount for the season it covers, chooses the basis
for the probabilities by a look-back (4.4, added November 2026) and rounds totals from unrounded amounts (6). Baseball
Operations' depth chart of December 10, 2026 bats the club's own four first (Néstor Cabrera, Gilberto Polanco, Josh
Atwell and the bat-first catcher Parker Burkett) and the five fifth to ninth: Sawyer Lusk fifth (fourth for his old club
in 2026), Andres Rivas sixth (second), Drew Brock seventh (third), Ángel Medina eighth (first) and Mike Meeks ninth
(first). Two of the five are first basemen; the club's incumbent first baseman, under contract for 2027, moves to the
bench, and the depth chart plays one newcomer at first and the other at DH. The controller's files: the term sheets, the
policy, the depth chart, the League Statistics Feed (box scores from 2021, the player ID crosswalk, the club directory,
the calendar, the transaction wire), the League office's weekly injured-list report, rules excerpt and 2027 schedule,
the projection vendor's winter depth charts and hitter projections, the club's contract register, payroll export, HRIS
employee map and earning codes, and the finance close-file index. As-of: Friday December 11, 2026.

## Default path

1. Read the five contracts' plate-appearance bonuses (each bonus's amount and threshold) from the term sheets.
2. Score the bases at hand on FIN-14 4.4's look-back (748 hitter-seasons, 2023 to 2026): the vendor's projection with a
   normal band from its past misses (0.2254), each player's own last three seasons (0.2698), and the depth charts'
   starting nines' seasons taken whole, each season's own plate appearances (0.2182).
3. Keep the lowest (the starting nines' seasons, 2021 to 2026, as the draws) and accrue each bonus at its amount times the
   share of those seasons reaching its threshold; add the five.

Ends on: $4,500,000 ($4,621,364 before rounding).
Golden: $4,250,000 ($4,221,715 before rounding).

## Stump sentence

Running FIN-14 4.4's look-back on the bases at hand (the vendor's projection with a band from its past misses, the
players' own seasons, the depth charts' starting nines' seasons taken whole) keeps the starting nines' seasons and
accrues $4,500,000 (Ends on); the step that lands it there is reading each signing off seasons that keep the catchers in
and ignore where each hitter bats, when his 2027 total is his new lineup slot's plate appearances per start times the
starts a winter-planned non-catcher regular makes, a near-full season or one long injured-list block (opening day's
included): the basis that scores lowest in the same look-back and accrues $4,250,000.

## Three rules

- **Task type:** general-statistics-data-science, resampling-simulation-monte-carlo-methods (serves Forecasting): the
  accrual is the expectation of a stepped payout over each signing's 2027 plate appearances, taken by resampling
  comparable seasons; the unit resampled is a whole season of a non-catcher regular the clubs planned in the winter (the
  starts he lost before opening day and in long injured-list blocks included), and each resampled season's starts are
  read at the plate appearances per start of the lineup slot the club gives the signing; the filed look-back scores the
  candidate bases on out-of-sample seasons.
- **Domain test:** the deciding quantity is each signing's predictive distribution of 2027 plate appearances at his
  bonus lines, which a resampling of comparable seasons gets only when the unit resampled is a winter-planned
  non-catcher regular's whole season and its starts are read at the new slot's rate per start; the generic summary of
  the player's record (a projection and its error as a normal band) moves the accrual from $4,250,000 to $6,250,000 and
  the starting nines taken whole to $4,500,000, and with another field's nouns there is no batting order fixing a rate
  per start, no position whose holders rest a third of the schedule and no 162-game schedule that planned regulars play
  out or lose in blocks.
- **Swap:** "how much should we accrue for the quota bonuses of our five new account executives" keeps a stepped
  bonus, but a rep has no batting order that fixes how many chances a working day brings, no catcher's position that
  caps a season's starts, no 162-game schedule that a planned everyday player either plays out or loses in one long
  block, and no winter plan whose members can be followed through a season, so the quantity that decides here (the share
  of planned non-catcher regulars' seasons whose starts clear a line at the new slot's rate) has nothing to attach to;
  and in the method swap, the projection with a normal band files $6,250,000 against $4,250,000.
- **Layer 1:** the box scores in two layouts across the League's 2025 platform change (2021-2024 pipe-delimited with
  CRLF ends, legacy player and club codes, numeric positions, US dates and the plate-appearance components AB, BB, HBP,
  SH, SF and CI with no PA field; 2025-2026 comma-separated with league player IDs, platform team IDs, ISO dates, a PA
  field, batting-order codes of slot times 100 plus entry and a substitute flag), joined through the League's crosswalk
  (names without accents); doubleheaders as two games on one date; suspended games carried under the date they began
  with a completion date; postponed games played on make-up dates; players traded mid-season appearing for two clubs;
  the vendor's winter depth-chart archive (one sheet per season, its own club abbreviations for seven clubs, positions
  with DH, batting order, bench rows); the term sheets and the policy as PDFs; on the ask side, the transaction wire, the
  weekly injured-list report, the payroll export across the January 2025 HRIS migration, the earning codes and the
  contract register (Ask sheet). Each is what these systems write; none moves the call or a player figure (R2: legacy
  PA without CI, doubleheaders merged to one start a date, accented names dropped, traded regulars cut to the planning
  club, each asserted).
- **Layer 2:** `forecast_uncertainty`, the expectation of a stepped payout from the right predictive distribution: each
  signing's 2027 plate appearances are his new slot's rate per start times the starts a winter-planned non-catcher
  regular makes, the starts taken whole from the 1,440 seasons of the 2021-2026 winter-planned non-catcher regulars (391
  of them 155 starts or more, 178 under 100, 16.5 per cent missing his club's first game); FIN-14 4.4's look-back over 748
  hitter-seasons ranks that basis first and every rival below it by a visible margin (the vendor's band 30.3 per cent
  worse, the players' own seasons 56.0, the starting nines taken whole 26.1, the catchers kept in 12.1, the regulars at
  any slot 6.7, the opening-day starters 2.1).
- **Decisive step:** pricing each bonus line at the share of the winter-planned non-catcher regulars' whole seasons
  whose starts, read at the signing's new lineup slot's plate appearances per start, clear the line: the season
  distribution, not a projection or a band around one; the new slot's rate, not the player's old rate and not every
  slot pooled; the non-catchers, not the starting nine with its catchers; the regulars the clubs planned in the winter,
  not the ones who opened or finished the season whole.
- **Not semantics:** no field, code, unit or definition says how plate appearances follow from starts and slots, which
  seasons are comparable, or that catchers differ; the contracts' plate-appearance definition, the policy's expected
  amount and look-back, the depth chart's slots and every feed field are read correctly on the easy route too, and an
  analyst who reads every one of them correctly and runs the look-back on the bases at hand files $4,500,000.
- **Not rule application:** the strict rule 3 test on every shipped sentence that bears on how the figure is computed:
  the prompt; FIN-14 4.1 to 4.5 and 6 (scope; each bonus at its amount times the probability, assessed at signing; the
  contract standing all season, the player in his planned role, his health and playing time in the probability; the
  look-back that chooses the basis; quarter-end remeasurement; totals from unrounded amounts); the term sheets' bonus
  clauses and their plate-appearance definition; the depth chart's legend; the feed notes; the vendor charts' header
  line. Executed word for word they fix the target and a way to rank bases, and construct none: no sentence names a
  distribution, a comparison set, a rate per start, a catcher or how starts are lost (R3s); 4.4 read as a basis itself
  (its own hitters' seasons) files $4,500,000 (LB7), and the one literal combination with the field's ready projection
  (each bonus counted if the vendor's projection reaches it) files $8,000,000. The basis that wins the look-back is the
  analyst's construction from the data (slot rates, catchers apart, whole seasons of the winter plan).
- **Analyst test:** a strong analyst who reads the five term sheets, FIN-14 (4.4 included) and the depth chart
  correctly and runs the look-back on the bases at hand files $4,500,000 (Ends on); the vendor's projection with its
  band files $6,250,000, the players' own seasons $7,750,000, the non-catcher regulars at any slot $5,250,000, every
  regular at the slot with the catchers kept in $3,750,000, the new slot's rate with a normal band $3,500,000, the
  opening-day starters $4,000,000, the regulars who opened the season $4,750,000 and the hitters with 400 plate
  appearances $4,500,000; only the winter-planned non-catcher regulars' whole seasons read at the new slot's rate file
  $4,250,000 and score lowest (executed in `checks.py` on the clean truth and on the pack, R3a, R3b, LB1 to LB8).
- **Estimand:** FIN-14 4.2, 4.3 and 6 with the prompt: for each of the five contracts, each plate-appearance bonus's
  amount times the probability, assessed at the date the contract was signed, that the player reaches its threshold in
  the 2027 championship season, plate appearances as the term sheets define them, the contract standing as signed all
  season with the player in the role the Club plans for him and his health and playing time inside the probability,
  added by player and over the five, the total from the unrounded amounts; the basis chosen by 4.4's look-back
  (population, window, thresholds and score filed); in `target/FIN-14_player_compensation_accounting_policy.pdf`.
  Population, outcome, window, unit, comparison and the selection criterion are filed; the basis is not.
- **No decoy:** no memo, earlier accrual, consultant estimate, agent's figure or stakeholder number states or argues an
  accrual or a probability; 4.4 is a scoring rule that ranks every basis an analyst brings and names none, and its one
  misreading (its own hitters as the basis) files another figure, asserted, so it blesses no wrong method; the vendor's
  projections are a mean playing-time forecast that answers no bonus question (a declared distractor); the depth chart
  gives roles and slots; the 2027 schedule ranks nothing.
- **No certified replay:** nothing certified or published is reproduced to recover a method; the season distribution,
  the slot rates and the look-back's scores are computed from the raw box scores, the vendor's winter depth charts and
  its projections.
- **Lesson:** a stepped payout on a capped season total is worth the chances of clearing each step, and those chances
  belong to the distribution of whole seasons of comparable planned units read at the unit's new rate; a filed look-back
  can choose that basis without naming it, so the difficulty is building the basis that wins, and the bases at hand
  (the projection and its band, the player's record, the starting nines taken whole) each lose; no build on file prices
  a stepped payout from a bounded total's season distribution at a new rate.

## Readability screen

Six tests per rung (`stumping` 2.1): 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the vendor's projected plate appearances, a bonus counted if the projection reaches its line | no | yes: the projection column | yes: the point forecast | no | no | yes | readable |
| R0a the vendor's projection with a normal band from its past misses | no | yes | yes: the band | no | no | yes | readable |
| R0b each player's own last seasons (his seasons as the draws, or their mean with a band) | no | yes: the box scores | yes: the player's record | no | no | yes | readable |
| R0c (the default path) the depth charts' starting nines' seasons taken whole, the look-back's pick among the bases at hand | no: 4.4 names the starting lineups as the hitters a basis is tested on, not as the basis | yes: the depth charts' lineup rows | yes: the reference class at hand | no | no | yes | readable |
| R1 the non-catcher regulars' seasons, any slot | no | yes: the position column | yes: comparables by position | no | no | yes | readable |
| R1b every lineup regular at the new slot's rate, catchers kept in | no | yes: the lineup slot field | yes: the slot allocation | no | no | yes | readable |
| R1c the new slot's rate with a normal band, or at the mean or median starts | no | yes | yes: the band | no | no | yes | readable |
| R1d the vendor's projection rescaled to the new slot, or calibrated by regression, with a band | no | yes | yes: the calibration | no | no | yes | readable |
| R1e the regulars' seasons moved toward the player's record or the vendor's projection (a weight) | no | yes | yes: credibility | no | no | yes | readable |
| R2a the regulars who qualified (502 plate appearances), had 400, or started 100 games | no | yes: a filter | yes: "regulars" by playing time | no | no | no | readable |
| R2b the opening-day starters, or the planned regulars who opened the season | no | yes: the first game's lineup | yes: opening day as the plan | no | no | no | readable |
| R3 (decisive) the winter-planned non-catcher regulars' whole seasons, read at the new slot's plate appearances per start | no: no sentence names a distribution, a comparison set, a rate per start, catchers or how starts are lost; 4.4 ranks bases and names none | no: no column holds a season's starts or a planned role's outcome; the seasons come from joining the vendor's winter depth charts to six seasons of box scores in two layouts through the crosswalk | no: the reflexes are the projection, the band, the player's own record, the reference class taken whole and regulars by playing time | no: no projection of 2027 starts, control total or certified figure ships | no: nothing in the files is wrong | no: a season-by-season starts table, a slot rate table, catchers apart, then each line's share, scored season by season out of sample | silent |

## Semantic fork table

Every row is asserted in `generator/checks.py` under its id.

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "accrue at signing" | the expected amount assessed at each contract's signing date | an accrual struck at the December 11 close | same call (nothing bearing on the five arrives between the signings and December 11: no batting line after the 2026 season, no move for the five after the November 3 reinstatement, the depth chart of December 10) | FIN-14 4.2 ("assessed at the date the contract is signed") |
| SF2 | "the plate-appearance bonuses in our five free-agent hitters' 2027 contracts" | the fifteen plate-appearance bonus lines in the five term sheets | other bonuses (awards, innings) | not in the five term sheets | the prompt; the term sheets' bonus rows |
| SF3 | "plate appearances" | championship-season plate appearances for the Club, as the League's official statistics count them | with postseason or rehabilitation plate appearances | not the contract's measure | each term sheet's plate-appearance definition; the feed carries championship-season games only |
| SF4 | the season | the 2027 championship season | later seasons of the multi-year contracts | none to accrue (no plate-appearance bonuses in later seasons) | the four multi-year term sheets ("No plate-appearance bonuses in later seasons") |
| SF5 | "expected amount" | each bonus times the probability its line is reached | the bonus counted if the expected plate appearances reach the line | $3,250,000 or $5,000,000 (mean or median starts), not the policy's measure | FIN-14 4.2 ("the amount of the bonus multiplied by the probability that the player reaches its threshold") |
| SF6 | what 4.3 holds fixed | the contract (no trade, release or renegotiation) and the planned role; health and playing time inside the probability | the player taken as healthy all season | $8,500,000 (every game started) or $7,250,000 (the seasons with no injured-list stint), asserted | FIN-14 4.3 ("His own health and playing time are not assumed") |
| SF7 | the role | as the Club's December 10, 2026 depth chart plans it (fifth to ninth) | another plan, a platoon or a role contest | not the Club's plan | FIN-14 4.3 ("in the role the Club plans for him at the date of signing"); the depth chart |
| SF8 | rounding path | each player's unrounded expected amount; the total from the unrounded amounts, rounded once | the total as the sum of the rounded player figures | $4,200,000 against $4,250,000, ruled out | FIN-14 6 ("a total is the sum of the unrounded amounts, rounded only where it is reported") |
| SF9 | the memo's figures | the accrual and each player's amount as in the workbook | other figures | same figures (asserted) | the prompt |
| SF10 | the as-of | December 11, 2026, every file pulled that day | a later pull | same call | the close-file index; every file stamped with the pull |
| SF11 | 4.4's "four championship seasons before the contract is signed" | 2023 to 2026 (the 2026 season ended September 27, before the first signing) | 2024 to 2026, or 2023 to 2025 | same call (a construction of the golden ranks first either way, asserted) | FIN-14 4.4 |
| SF12 | 4.4's "every hitter in a starting lineup" | the lineup rows of each January 31 depth chart, catchers in | the non-catchers only | same call (asserted) | FIN-14 4.4; the depth charts' legend |
| SF13 | 4.4's "100 plate appearances in each of the two seasons before" | as the League counts them, every club | with the planning club only | same call (asserted) | FIN-14 4.4 ("counting his plate appearances for every club") |
| SF14 | 4.4's "reached the threshold" | plate appearances at or above it | above it only | same call (asserted) | FIN-14 4.4; the term sheets ("when the Player reaches its threshold") |

## Ladder

Built figures (from `generator/calc.py` on the shipped files, asserted in `generator/checks.py`); every figure is the
accrual in US dollars for the five signings' 2027 plate-appearance bonuses, rounded to $250,000, with its distance from
the golden in $250,000 bins, and its FIN-14 4.4 look-back score above the basis used (the golden basis scores 0.1730 on
748 hitter-seasons). The five, as the depth chart bats them: Lusk fifth (fourth for his old club), Rivas sixth (second),
Brock seventh (third), Medina eighth (first), Meeks ninth (first).

| Rung | Construction | Accrual | Bins | Look-back | Dies to |
|---|---|---|---|---|---|
| R0 | the vendor's projection, a bonus counted if it reaches its line | $8,000,000 | +14.71 | +104.3% | FIN-14 4.2 (a probability, not a projection reaching a line); the look-back |
| R0a | the vendor's projection with a normal band from its misses | $6,250,000 | +7.71 | +30.3% | the look-back; the projection carries the old slot's rate and the five's full recent seasons |
| R0b | each player's own 2024-2026 seasons as the draws; their mean with a band; their starts at the new slot; his 2021-2026 seasons | $7,750,000; $6,500,000; $6,500,000; $6,750,000 | +14.29; +8.90; +8.95; +10.27 | +56.0%; +35.1%; +50.6%; +53.3% | a planned regular's starts in one season say nothing about the next (correlation -0.055 over 934 pairs) |
| R0c (default path) | the starting nines' seasons taken whole (the look-back's pick among the bases at hand); 2022-2026 and 2024-2026 windows; 4.4's own hitters' seasons | $4,500,000; $4,750,000; $4,500,000; $4,500,000 | +1.60; +1.77; +1.53; +1.39 | +26.1% | catchers rest a third of the schedule and every slot's rate is pooled |
| R1 | the non-catcher regulars' own plate appearances, any slot | $5,250,000 | +3.73 | +6.7% | the slot fixes the rate: 4.72 batting first to 3.83 batting ninth, every season |
| R1b | every lineup regular at the new slot's rate, catchers kept in; the full nine at the slot | $3,750,000; $3,500,000 | -1.73; -3.04 | +12.1%; +9.3% | a catcher's starts are capped by the position; none of the five catches |
| R1c | the new slot's rate with a normal band; at the mean or median starts; starts drawn game by game | $3,500,000; $3,250,000 or $5,000,000; $3,000,000 | -2.72; -4.17 or +3.03; -5.04 | +3.7%; +62.0% or +50.1%; +38.0% | the starts are a near-full season or a long block, not a symmetric spread or a point |
| R1d | the vendor rescaled to the new slot with its band; calibrated by regression with a band or its residuals | $4,750,000; $4,750,000 or $5,250,000 | +1.91; +2.11 or +4.51 | +28.2%; +8.7% or +7.0% | the look-back |
| R1e | the regulars' seasons moved 5 or 10 per cent toward the player's record or the vendor's projection; 10 per cent of the record blended in | $4,500,000 to $4,750,000 | +1.36 to +2.46 | +0.4% to +1.6% | the look-back (every weight scores worse than none, more weight worse) |
| R1f | the regulars at the old slot's rate; with a band | $6,000,000; $5,500,000 | +7.29; +4.95 | +7.5%; +9.4% | the role is the 2027 plan |
| R2a | hitters with 502 or 400 plate appearances, or 100 starts | $5,500,000; $4,500,000; $4,750,000 | +5.43; +1.37; +1.99 | +28.0%; +3.6%; +5.2% | selects on the outcome: the injured seasons fail the filter |
| R2b | the opening-day starters; the planned regulars who opened the season | $4,000,000; $4,750,000 | -1.22; +1.65 | +2.1%; +1.2% | drops the regulars hurt in spring training and keeps the fill-ins (16.5 per cent of planned regulars missed the first game) |
| R2c | the club's own regulars only | $4,000,000 | -1.22 | +7.3% | thirty-odd seasons, the look-back |
| R2d | appearances read as starts (substitute lines counted) | $3,500,000 | -3.10 | +3.2% | a substitute's line is not a start |
| near | a regression on the projection, the slot and catching, or on the slot and catching; a 2 per cent weight on the record or the projection; 5 per cent of the record blended in | $4,250,000 to $4,500,000 | +0.13 to +0.71 | +0.20% to +1.07% | they lose the look-back (LB6); four of the five file the golden's figure anyway |
| golden (R3) | the winter-planned non-catcher regulars' whole seasons at the new slot's rate per start | $4,250,000 | 0 | 0 | (the golden; the last three seasons alone tie it, 0.00 per cent, and the plate appearances rescaled to the slot, 0.08) |

- **Every construction of the golden** (C1, asserted, L4): the seasons from 2022, 2023, 2024 or 2025 (+80,852, +49,150,
  +15,827, -11,819 against the unrounded golden); slot rates from 2024-2026 or 2025-2026 (0, +35,375); ages within two
  or three years of each signing, or 30 to 34 (-75,084, -55,468, -70,065); each comparable season's own or starting plate
  appearances rescaled to the new slot (+6,959); the planned regulars who batted at the new slot, their own plate
  appearances (+63,249); the club's own plate appearances per start (-51,937); the player with the most starts at each
  club's position (+70,688) or the eight non-catchers with most starts per club (+70,118); the same position only
  (-80,548); the regulars with two earlier seasons of 100 plate appearances (+40,623): one rounded accrual and the same
  five player figures every time. Two loose regular sets also round alike: hitters with 81 or more starts (+137,651) and
  with 300 or more plate appearances (-56,099). The look-back scores the constructions within 0.35 per cent of the basis
  used.
- **One sigma.** Bootstrap of the comparison seasons (300 draws): standard deviation $86,384 against the golden's
  -$28,285 from its bin's centre, so a one-sigma move keeps $4,250,000; each player's figure (standard deviation $9,776
  to $24,845; 513,778; 1,010,938; 587,583; 1,198,417; 911,000) keeps its rounding at one sigma (L3).
- **The look-back ranks the bases** (LB0 to LB8): 748 hitter-seasons, every one with the vendor's projection; the basis
  used scores lowest; every rival and near route scores worse (LB3), the vendor's band by 30.3 per cent, the players' own
  seasons by 56.0, the starting nines taken whole by 26.1, the catchers kept in by 12.1, the non-catchers at any slot by
  6.7, the opening-day starters by 2.1 and the regulars who opened by 1.2 (LB4 floors); weight on the record or the
  projection only worsens the score (LB5); each of 4.4's own terms read the other way still ranks a construction of the
  golden first (SF11 to SF14). The out-of-sample checks behind it (BT1 to BT7) hold: the season distribution at the slot
  predicts the 2024-2026 shares within 2 standard errors, the normal band misses by more than 3 at 550 and 600, the
  vendor's band by more than 5 at every line, the rate per start falls down the order every season, starts do not
  persist, 16.5 per cent of planned regulars missed the first game.
- **Position and dominance.** The decisive construction moves every player's figure; the nearest rivals sit 1.22 bins
  below (the opening-day starters, the club's own regulars) and 1.36 bins above (a 5 per cent weight on the record or the
  projection), every other one further, on both sides (L5, L6); the audit's route (the starting nines' own plate
  appearances) sits 1.60, 1.77 and 1.53 bins above on the 2021-2026, 2022-2026 and 2024-2026 windows (LB8).
- **Strength, re-estimated.** A strong solver who runs 4.4 is pushed off the vendor and the players' records (both lose
  by 30 per cent or more) toward a reference class of regulars, and the clause's population puts the starting nines in
  front of him: that route files $4,500,000. The golden needs three moves the clause does not name, each rewarded by the
  look-back but each alone a wrong figure: catchers apart ($5,250,000 without the slot), the new slot's rate ($3,750,000
  with the catchers kept), and the planned regulars' whole seasons rather than the opening day's or the qualified
  ($4,000,000 to $5,500,000). Estimated P(a strong solver implements the look-back) 0.6 to 0.7, P(it then builds the
  population, the slot and the catchers together) 0.25 to 0.3, plus about 0.02 landing through a near or same-slot
  route: P(one lands) about 0.15 to 0.2; P(both of two land), the two correlated (rho about 0.3), about 0.05 to 0.08.
- **Worth.** Graded: the total accrual, each player's accrual, the slot rates and the look-back's ranking; never an
  intermediate a valid method could skip.

## Closure table

Each row's assertion is in `checks.py` (C1 to C22).

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the fifteen plate-appearance bonus lines of the five 2027 term sheets | filed (prompt, term sheets); SF2 |
| 2 | Unit of account | US dollars, one bonus line at a time | filed (term sheets, FIN-14 4.2) |
| 3 | Attribution window | the 2027 championship season | filed (term sheets, FIN-14 4.2); SF4 |
| 4 | As-of dating | assessed at each signing date; files pulled December 11, 2026 | FIN-14 4.2; the close-file index; SF1 |
| 5 | Version basis | one term sheet a contract; one depth chart; FIN-14 as revised November 2026 | asserted (no superseded version ships) |
| 6 | Denominator | the probability's base: the comparable seasons | FIN-14 4.4 chooses the basis; every construction rounds alike (L4, LB2) |
| 7 | Weighting | each comparable season once | C1 asserted (age-matched variants); weights toward the record lose the look-back (LB5) |
| 8 | Window length | the history 2021-2026; the look-back's four seasons | C1 across windows; SF11 |
| 9 | Boundary inclusivity | a line reached at exactly its threshold | filed (term sheets: "reaches its threshold"); strict and inclusive readings round alike (C9); SF14 |
| 10 | Rounding path | unrounded amounts, the total rounded once from their sum | FIN-14 6; SF8 |
| 11 | Tie-break | none arises | not applicable, asserted (no two of the five share a slot; the look-back's lowest is unique) |
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
the contract standing all season with the player in his planned role and his health inside the probability), the rule
that chooses the basis (4.4's look-back, its population, window, thresholds and score) and the arithmetic from the
probabilities to the rounded totals; it leaves only which basis to build, and every reading of every term converges on
the golden or violates a quoted line (SF1 to SF14). The literal executor of 4.4 still has to bring bases to rank; the
one basis the clause's words suggest (its own hitters' seasons) files $4,500,000. The easy answers come from easy bases
ranked by the same look-back, never from another reading.

## Oracles

- The vendor's 2027 projections and its past projections: a mean playing-time forecast per hitter; the look-back scores
  the bases built on them 25 to 104 per cent worse than the basis used; they confirm only that the five project to 578
  to 697 plate appearances; deleting the file leaves the golden and both asks (D1; a declared distractor, though the
  look-back reads it to score the vendor's bases).
- The box scores and the winter depth charts themselves: the history every basis fits and the look-back scores; nothing
  in them ties only under the golden.
- The 2027 schedule: 162 games a club under every method (a declared distractor).
- Nothing ties only under the golden: no 2027 projection of starts, no control total and no certified figure ships.

## Ask sheet

**Main call's declared row population:** the two box-score files (every row and column the golden reads: player, game,
date, club, lineup slot, starter, plate appearances or their components), the crosswalk, the club directory, the
vendor's winter depth charts, the five term sheets, the 2027 depth chart, FIN-14 and the feed notes (the look-back also
reads the vendor's projections to score the vendor's bases). Device and hazard rows in it: 0 (asserted, SEP1 to SEP3:
the call computed from those files alone is the golden; the transaction wire, the weekly report, the rules excerpt, the
calendar, the payroll export, the HRIS map, the earning codes and the contract register are read only by the asks; no
main-call document carries an ask's organ). Neither ask is keyed to the call, its construction or its figures; they
share no primary device.

**Ask A. Every injured-list stint the five have had since the start of the 2024 season: the date it took effect and the
regular-season days it covered** (nine stints, 18 figures).
- H18 home: the injury record behind the accrual, in the audit file beside it: a measure every signing carries that
  the call does not turn on (the golden reads other players' seasons, never the five's injuries).
- The unit, filed once in the League's rules excerpt (Article 22), in the League's voice: a placement takes effect on the
  date the club designates, up to three days before the transaction (22.1); the minimum periods run from the date the
  placement takes effect (22.2); a transfer, a rehabilitation assignment or an assignment of the contract does not end
  the placement (22.3 to 22.5); reinstatement ends it (22.6); days counted from the date it takes effect through the day
  before reinstatement (22.7); the paternity and bereavement lists not injured lists (22.8); the weekly report's
  contents, the transaction date and the first date of reinstatement (22.9); the championship season from Opening Day
  through the last scheduled day (the feed notes and the calendar).
- Primary device A1 (D7, the true key in another field, split evidence): the transaction wire dates each move on the
  day the club made it, and the weekly report's "placed" column carries the same transaction date; every one of the
  five's placements took effect one to three days earlier (22.1 allows it), a date only the report's first date of
  reinstatement less the list's minimum period (22.2) gives. The natural path and the cracker's (the move's date as the
  date it took effect) miss every date and every day count (A3b, CR1). Fair: for all 7,389 report rows the derived date
  is the true date the stint took effect (A4). The internal inconsistency that finds it: a 10-day placement whose first
  date of reinstatement is eight or nine days after it.
- Hazards: HA1 a spring placement (took effect March 25, 2025, two days before Opening Day; days from Opening Day);
  HA2 a stint open at the 2026 season's end, reinstated November 3 (days through the last scheduled day); HA3
  rehabilitation assignments inside two stints; HA4 a paternity-list move (not an injured list); HA5 the 7-day concussion
  list (an injured list); HA6 a trade while on the list (one stint); HA7 a 10-day to 60-day transfer written on the wire
  as a fresh placement (splitting it adds rows); HA8 two stints five days apart (merging them drops one); HA9 a pitcher
  who shares one signing's name (found by name, his stints join the table).
- Stops (measured): the move dates (9 rows, every figure off); every placement a stint (11 rows); stints a week apart
  merged (8 rows); the moves found by name (11 rows); the golden.
- Span: the transaction wire, the weekly report, the rules excerpt, the calendar, the vendor charts (the five's League
  IDs), the term sheets (the five's names) (6 files); about 12 columns.
- Realism: a transaction wire records the day a club makes a move; an injured-list placement can be backdated; the
  League office's report lists the transaction and the first date of eligibility; a legacy roster system logged a list
  change as a new placement.

**Ask B. The plate-appearance bonuses the club paid for each of the 2024, 2025 and 2026 seasons, player by player and in
total** (seven player rows and three totals, 10 figures).
- H18 home: the club's own record on the bonuses it accrues, an audit trail of the same liability, rows the call never
  reads; in payroll's words.
- The unit, filed in the contract register's notes, in the system owner's voice: plate-appearance and games-started
  bonuses are earned in the championship season and paid half in the first payroll after the season ends and half on
  the following January 15, both halves the bonus of the season earned; every plate-appearance bonus the club paid for
  2024 to 2026 went to a player under a contract in the register with plate-appearance terms (the population: the club's
  own players, not the five); a voided and reissued payment is one payment; until the January 2025 migration every
  performance and award bonus went on the legacy code E40, one line able to carry more than one bonus; pitchers'
  playing-time bonuses in full after the season.
- Primary device B1 (D5, a category crossed by label): the payroll pays a player's playing-time bonuses for a season
  in one line (the HRIS playing-time code, and before the migration the legacy performance-bonus line), so every
  payment carries the season's plate-appearance and games-started bonuses together; the plate-appearance part is half
  the plate-appearance lines the player reached for the Club, which only the register's terms against the box scores
  separate. The payroll lines at face value miss all ten figures (CR2). Fair: every 2024-2026 playing-time line equals
  half the season's plate-appearance and games-started lines reached for the Club, the legacy October 2024 line to one
  player also carrying his All-Star bonus (B3c, 12 lines).
- Second device B2 (D2, a label stored before a silent switch): before the January 2025 HRIS migration every
  performance bonus went on one legacy code, migrated as "other bonus"; the October 2024 first halves sit there, one of
  them with the season's All-Star bonus in it, a veteran's November Silver Slugger bonus on the same code.
- Hazards: HB1 a void and reissue in October 2026 (net once); HB2 legacy employee numbers mapped through the HRIS map;
  HB3 the playing-time code also carries two pitchers' games and innings bonuses; HB4 a contract assigned at the 2025
  deadline (the register's lines against the season's plate appearances give $675,000 for a player the club paid
  $225,000); HB5 the 2026 second halves are payable January 15, 2027 (not paid at December 11); HB6 the January 2024
  halves of the 2023 season (a pay-year grouping moves them into 2024).
- Stops (measured): the lines at face value ($420,000, $1,025,000, $445,000); the playing-time code by pay year (none for
  2024, $772,500, $1,157,500); the playing-time code by season ($185,000, $1,100,000, $645,000); the register's terms
  against plate appearances ($325,000, $1,350,000, $825,000); face value with the void reversal ignored ($420,000,
  $1,025,000, $610,000); each half under the year it was paid ($372,500, $612,500, $862,500); the five signings only
  (nothing); the golden ($325,000, $900,000, $412,500).
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
| HA8 two stints five days apart | a re-aggravated hamstring | Ask A, one player | merging drops a row |
| HA9 a namesake pitcher | a common name | Ask A, one player | extra rows if matched by name |
| HB1 a void and reissue | changed bank details | Ask B, 2026 | +$165,000 if summed gross |
| HB3 pitchers on the playing-time code | one code for all playing-time bonuses | Ask B, 2025 and 2026 totals | +$75,000 and +$200,000 |
| HB4 an assigned contract | the 2025 deadline trade | Ask B, 2025 | +$450,000 on the register path |
| HB5 the 2026 second halves | January payment | Ask B, 2026 | doubles each row on the register path |

**Referee.** For Ask A, the weekly report's first dates of reinstatement and the rules' minimum periods; for Ask B, the
register's terms and the box scores' plate appearances and starts by club. Each is a field the golden reads, not a
control: no file ties only under the golden.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A stints: date taken effect and regular-season days (18) | the filed stint definition executed on the transaction wire (placement to reinstatement, transfers, rehab and trades inside, lists filtered, season caps applied), the date taken effect read as the placement's date on the wire and the report | every date one to three days late, every day count short by as much or more: all 18 off | miss |
| B 2024 player rows and total (3) | the payroll's playing-time and legacy season-end lines at face value, each half to its season, voids netted, pitchers dropped | $250,000, $170,000, $420,000 | miss |
| B 2025 player rows and total (4) | the same path | $420,000, $330,000, $275,000, $1,025,000 | miss |
| B 2026 player rows and total (3) | the same path | $280,000, $165,000, $445,000 | miss |

Mirror leakage: about 10 per cent of the ask weight (the mirror runs the natural ask paths, the move dates and the
playing-time code by season, and keeps only the workbook's and the memo's structural criteria; no ask figure).
Pair ceiling: 34 (on a rubric of about 35 for the call, the five player accruals and the look-back's ranking, 7 for
instructions and 58 for the asks: the cracker lands the call, 35 plus 7 plus about 5 of structure, 47; the mirror keeps
about 5 of the recommendation's weight plus 7 and 9 of structure, 21; neither keeps an ask figure).

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
  accrual by $170,000 to $360,000 against the pooled set; redrawn with no age effect inside the signings' 30 to 34.
- A prototype where the five kept their old slots or moved both ways (prototypes 2 and 3): the point projection at the
  new slot and the player's own three-year mean with a normal band each landed inside the golden's bin by cancelling
  errors; redrawn so the five bat lower for the club than for their old clubs.
- Spring-training injured-list placements at 5 to 13 per cent of winter-planned regulars, with the bench's best player
  filling every absence: the opening-day lineups sat 0.5 to 0.6 of a bin from the golden; set at 16 per cent with a
  club's answer to a long stint (a bench player at the position about a quarter of the time, else a recall), the rung
  sits clear.
- Injured-list stints shorter than the list's minimum period: every stint now runs at least its list's minimum from the
  date it took effect, and a transfer to the 60-day list only for a stint of sixty days or more.
- Trades left out of the next season's rosters: the offseason now starts from the rosters as the season ended.
- World seed 151: the history windows and age-matched sets spread about $190,000 around the golden; seed 1511 was
  searched with the contract terms (superseded at stage 4, below).
- The weekly report carrying an "on list since" date (the date taken effect, stated): the cracker reads it; the report
  now carries the transaction date and the first date of eligibility, the true date only through 22.2.
- Ask B with the payroll's plate-appearance halves on their own lines (the first design): the cracker's face-value path
  matched every 2025 and 2026 figure; the payroll now pays a season's playing-time bonuses on one line.
- A platform layout whose only starter marker was the batting-order code: reading every platform line as a start moved
  the call half a bin; the platform layout now carries its substitute flag.
- Contract amounts equal to answer figures: `leak.py` read them as the answer in the term sheets; amounts are searched
  so no bonus line, or two or three of them, equals an answer figure.
- Club nicknames shared with real teams: renamed. Three Australian names among the club's designed players: designed
  names are drawn apart.
- The unfiled back-test (stage 3): the out-of-sample comparison lived only in `checks.py`, so nothing the judge could treat
  as deciding preferred the golden's basis; the judge reproduced the golden and stood the vendor's band ($4.67M then),
  the vendor's residuals and each player's own seasons beside it as defensible (round 1, NOT_DETERMINISTIC). Filing the
  population and slot method (the judge's own suggested fix) was refused: it files the HOW. FIN-14 4.4 now files the
  selection criterion only.
- Stage 3's lineup (the five fourth to seventh and ninth, the club's catcher eighth): the starting nines' own plate
  appearances, catchers in and no slot, landed $3,500,000 by cancelling errors (catchers about -1.5 bins, pooled slots
  about +1.5) on every window; batting the catcher fourth or fifth alone moved the golden 0.8 to 0.9 bins. The five now
  bat fifth to ninth with contract lines searched toward the steep part of the starts distribution, and the route sits
  1.53 to 1.77 bins away.
- The world with an age effect on rest and injuries over 34, and a lost job's slot passing to a bench catcher at DH: the
  player's own record carried a little signal (credibility weights of 2 to 10 per cent beat the golden basis in the
  look-back and moved the accrual more than a bin); redrawn with no age effect and catchers kept to catching jobs, so a
  regular's record carries nothing beyond his slot and position.
- Seeds 1512 to 1538 and 1540 to 1592 under the redrawn world: in most, a small weight on the record, or 5 per cent of it
  blended in, scored level with or below the golden basis (season-level noise over four seasons); seed 1539 is one where
  every weight scores worse and more weight worse, the regressions and the opened regulars lose by 0.75 per cent or more,
  and the contract search leaves every rival 1.22 bins away or more.
- Rainouts at 1.2 per cent of games (about 1.7 doubleheaders a club a season) with the $4.25M golden: merging a
  doubleheader to one start a date moved the call 0.74 of a bin (a Layer 1 slip deciding the call); rainouts now 0.5 per
  cent, and a postponed series-ending game is made up on the next off day neither club already plays (two clubs had been
  booked twice on one make-up date).
- A FIN-14 4.4 dated in the 2024 policy: a December 2024 policy cannot name the 2023 to 2026 seasons; 4.4 says "the four
  championship seasons before the contract is signed" and the policy is revised November 12, 2026, after the auditors'
  review of the 2025 close.

## Build record

Stage 3, built 2026-10-16 (world seed 1511), PAUSED at 5e385a0. Stage 4 repair, built 2026-10-16 from
`task151/generator/build.py` (world seed 1539).

- Pack: 20 files, 5 formats (csv, json, pdf, txt, xlsx); the spine 276,378 batting lines (`lsf_batting_2021_2024.txt`
  184,271 rows, `lsf_batting_2025_2026.csv` 92,107); distractors `hvbd_hitter_projections_2022_2027.csv` and
  `league_schedule_2027.csv` (metadata.json); the close-file index `ral_close_file_index_2026-12-11.csv` (was
  export_manifest).
- Main call from the shipped files: $4,250,000 ($4,221,715), players $500,000, $1,000,000, $600,000, $1,200,000, $900,000
  (513,778; 1,010,938; 587,583; 1,198,417; 911,000; adding to $4,200,000); the vendor's band $6,250,000 on the pack and
  the clean truth alike; the look-back's pick among the bases at hand $4,500,000; every construction one rounded figure
  and the same five player figures (L4, LB2); one bootstrap sigma $86,384; the look-back (748 hitter-seasons) ranks the
  golden basis first.
- Repair items: FIN-14 4.3 restated (the contract standing, health and playing time in the probability; the healthy
  readings file $8,500,000 and $7,250,000, SF6); 4.4 the look-back; 6 one rounding path (SF8); the rules' 22.1
  backdating sentence (HA7, the placed-date reading misses all 18 figures); the register's four notes (population,
  season earned, one payment for a reissue, E40 carrying more than one bonus; the pay-year and five-only readings
  asserted, B1b, B2); the index renamed (H9); world: no age effect, catchers kept to catching jobs, the club's catcher a
  bat-first hitter batting fourth, rainouts 0.5 per cent with clean make-up dates, one veteran's games-started line at
  110.
- Gates: `checks.py` 276 assertions, 0 failed; `verify.py` agrees on its own pandas and pdftotext path (the accrual, the
  five player figures, the vendor's band, the at-hand pick, the step figures, the look-back for four bases, the nine
  stints and the bonuses paid); two byte-identical builds (target, goldens, metadata.json, submission.md, figures.json,
  target.zip b6ee5326); container audit clean on the pack and the goldens; `figures_check.py` 87 figures, 0 absent;
  `precut.py` exit 0; `voice-check.py` PASS (766 characters, the prompt unchanged); `leak.py` REVIEW, no LEAK (answered
  below); `guard.py validate` clean, `heart` WARN (answered under Draw), `surface` promotes nothing.
- `leak.py` REVIEW lines, each harmless: FIN-14's "4.4" is the section the write-up cites; the register's "$125,000
  each" and "$225,000 each" beside the $125,000 and $225,000 the club paid two veterans (each reached one line with the
  club; the register's term is the input); the term sheets carry the call's words (they are the contracts the call
  accrues for); FIN-14 carries seven of the stump paragraph's terms (appearances, look-back, planned, starting,
  contract, lineup): 4.3 names the planned role and 4.4 the hitters a basis is tested on, and neither names a basis, a
  slot, a rate per start or catchers; the feed notes carry five (appearances, catchers in "catcher's interference",
  lineup, batting, position), field definitions naming no method; the projections, the depth charts, the wire and the
  term sheets name the five beside numbers (projected plate appearances, ages, transaction IDs, contract terms), none an
  accrual or a ranking on it; the calendar's and the 2027 schedule's dates after December 11, 2026 are the 2027 season's
  (forward-looking by nature). A first cut carried a $1,000,000 signing bonus and salaries ending in 500,000 beside the
  $1,000,000 and $500,000 player accruals (LEAK); the signing bonuses and salaries moved ($1,250,000, $1,750,000,
  $9,750,000, $15,750,000, $9,250,000).
