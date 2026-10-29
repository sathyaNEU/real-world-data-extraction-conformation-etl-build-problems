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

**Stage 4 loop 2: record fixes on the same world.** The re-judge returned DETERMINISTIC, APPROVE at $4,250,000 and the
leak reader found no leak. The rule 3 re-audit returned AT_RISK on realism: the record carries no persistence (the
vendor's projection correlates 0.005 with realised plate appearances, last season's plate appearances -0.04), and the
seed search that kept 1539 is noise-picking. The loop tried honest persistence under a seed rule written first (next
section). On the rule's seed the look-back's winner became a credibility blend on the player's own starts, and bases
tying it within z 0.5 filed $5,250,000 and $5,500,000 with different player figures, so the total was not determinate
and the loop stopped (the coordinator's stop rule). The 5a71a64 world ships unchanged, seed 1539 as searched, with the
record fixes: step 4 of the write-up prices each look-back hitter from his own group's seasons (the judge scored 0.1972
the other way); the prompt asks for the bonuses paid to date (SF15); the league is renamed from wider pools (945
surnames; Lusk, Brock and Meeks unique, Rivas and Medina three times each, one Rivas the designed namesake pitcher); and
FIN-14 4.4 keeps the principle while close-file working paper CF-14.4 holds the look-back's hitters, thresholds and
score.

## World seed rule (loop 2, stopped)

Written at stage 4 loop 2, before any look-back or accrual was run on a world with persistence. The record gets honest
persistence: a per-player durability drawn once for his career on its own stream (lognormal, sigma 0.8, on his chances
of a spring placement, an in-season stint and a day-to-day absence), and a lost job more likely for a weaker regular (the
6 per cent scaled by exp(-0.8 x (talent - 0.5))). Sigma was set on W1 alone, over seeds 1601 to 1606 (0.7 gave a mean
plate-appearance correlation of 0.22, 0.8 gave 0.25, about what a regular's playing time carries year to year). The
world seed is the first integer from 1601 upward whose world passes W1 to W4, read on league-wide tables only (never the
five, the look-back's ranking or any accrual):
- W1 persistence: over 4.4's non-catcher hitters (2023 to 2026, a depth chart's starting lineup, 100 plate appearances
  in each of the two seasons before), a season's plate appearances correlate with the season before's between 0.15 and
  0.40, and so do its starts;
- W2 projection skill: the vendor's preseason projection correlates with those hitters' realised plate appearances
  between 0.15 and 0.45;
- W3 injured-list volume: hitters' placements average 8 to 18 a club-season, and 10 to 22 per cent of winter-planned
  regulars miss the club's first game;
- W4 integrity: 162 games a club-season, one line per player per game (a traded player leaves his old club's bench
  and its injured-list cover on the trade's date, a generator fix made while calibrating), nine starters a club per
  game, no club booked twice on one make-up date.

The seed is kept whatever the look-back and the accrual then show. If no basis wins 4.4 cleanly, if the bases tying the
winner file different rounded figures, or if the vendor's band or the player's own seasons land, the loop stops and the
5a71a64 world ships with the record fixes (coordinator, loop 2).

Outcome: stopped (measured with scratch scripts on the reverted generator, so not reproducible from the shipped one).
Seed 1601 is the first from 1601 to pass W1 to W4 (W1 0.30 for plate appearances and 0.29 for starts,
W2 0.31, W3 10.2 placements a club-season and 16.8 per cent missing game one, W4 clean). Its look-back ranks the
player's own starts blended in at 30 per cent first (0.16837, $5,250,000; players $600,000, $1,400,000, $600,000,
$1,500,000, $1,200,000). The regulars matched on last season's starts within 10 to 25 tie it (z 0.10 to 0.38 by hitter
pairs) and file $5,500,000, as does the blend at 40 per cent (z 0.53); on 2024 to 2026 or 2023 to 2025 alone the
matched set wins. This build's golden basis scores 6.7 per cent above the winner there; the vendor's band ($6,250,000)
and the players' own seasons ($7,750,000) miss. Seeds 1602 and 1604, drawn after the stop only to see whether the shape
was structural, gave the same at $5,000,000, with the 20 and 40 per cent blends a bin either side within z 1.5. A blend
weight is continuous; the look-back pins it to about 0.1, and 0.1 of weight is about a bin. The generator's persistence
was reverted, with the trade fix made while calibrating (the 1539 world has no line for a traded player's old club
after his trade, checked).

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task151.json`, architecture v1, registered 2026-10-16, updated at the stage 4 repair; `guard.py check` and `heart` WARN (overuse.objective, repeat.gate_g), answered below; nearest drivers 0.06 (task105 v1 lineage), 0.05 (task132) and under |
| Domain / task type | `general-statistics-data-science` (client domain), task type `resampling-simulation-monte-carlo-methods` (serves Forecasting): the bonus accrual is the expectation of a stepped payout, worked by resampling comparable seasons, and the step is which unit is resampled (a whole season of a regular planned in the winter, injured-list blocks included) and at what rate its starts are read (the new lineup slot's). Economics is not the owner (the call is a club's accrual, corporate finance, and the economics task types are macro, choice and causal designs); the seed's Economics label is a house domain that maps to Economics & Econometrics |
| Objective | Forecasting & Predictive Modeling: the expected bonus payments for the 2027 regular season, a season not begun at the decision (the contracts were signed between November 24 and December 10, 2026, and the accrual is booked in the December close) |
| Shape | `other`: one committed figure (the accrual) built from five players' accruals, each the sum of its bonuses' chances, plus one ask table (the other playing-time bonuses paid, 21 figures) and a memo (arithmetic in `## Ask sheet`) |
| Decision | `quantity_figure`, answer unit `currency` (US dollars) |
| Mechanism | gap population (decisive: the comparison seasons are whole seasons of every non-catcher regular planned in the winter, read at the new slot's rate, not the player's own seasons, not the starting nines taken whole, not the regulars who opened or completed the season) with time (the accrual is assessed at signing, so the injured-list blocks before opening day are in the window); pattern none; generators G1 (the payout is on steps of a bounded total, so its value is the chances of clearing each step), G9 (the regulars who opened the season or qualified are the survivors of the blocks), G13 (the window runs from signing, not from opening day); Gate G `forecasting`; strategy `other`. Selection organ: the filed look-back of FIN-14 4.4 (a selection criterion in general terms), card note |
| Layer 2 family / pattern | `forecast_uncertainty`; `own:stepped-bonus-chances-from-winter-planned-regular-seasons-at-the-new-slot-rate`. The library line nearest it is the task type's first (resample the independent unit, not rows); here the unit is a planned regular's whole season and the reading rate is the slot's, so the line is a frame, not the step |
| Furniture | forum `other` (the controller books it; no committee), forcing event `period_close` (the December close books the accrual at signing), organisation family `other` (a professional baseball club), role family `finance_controller` (the club's controller), context artifact `register` (the club's player contract register and term sheets), calibration `none`, opening `question-first`, question form `how-much` |
| Spine | the League Statistics Feed's box-score batting lines, one row per player per championship-season game with his lineup slot and position, 2021 to 2026 in two layouts across the League's 2025 platform change: `lsf_batting_2021_2024.txt` (184,271 rows) and `lsf_batting_2025_2026.csv` (92,107 rows), 276,378 in all (constructed) |
| Deliverables | `pa_bonus_accrual_2027.xlsx` (the accrual by line, player and in total, the look-back, the ask table, notes), `pa_bonus_accrual_memo_2027.docx` (one page for the audit file) |
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
for the probabilities by a look-back (4.4, added November 2026, its test set in close-file working paper CF-14.4) and
rounds totals from unrounded amounts (6). Baseball
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
  with DH, batting order, bench rows); the term sheets and the policy as PDFs; the transaction wire and the weekly
  injured-list report beside the Article 22 excerpt (distractors); on the ask side, the payroll export across the
  January 2026 HRIS migration (legacy numbers, names and codes on legacy history, a reissued legacy number, a void and
  reissue, the season-end line after a contract's last season settling the salary it deferred), the earning codes and
  the contract register (Ask sheet). Each is what these systems write; none moves the
  call or a player figure (R2: legacy
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
- **Analyst test:** a strong analyst who reads the five term sheets, FIN-14 (4.4 included), CF-14.4 and the depth chart
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
  (population, window, thresholds and score filed in working paper CF-14.4); in
  `target/FIN-14_player_compensation_accounting_policy.pdf` and `target/CF-14.4_look-back_working_paper.pdf`.
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
| SF11 | CF-14.4's "four championship seasons before the contract is signed" | 2023 to 2026 (the 2026 season ended September 27, before the first signing) | 2024 to 2026, 2023 to 2025, or 2022 to 2025 (no 2022 hitter has two earlier seasons in the box scores, so it adds none) | same call (a construction of the golden ranks first every way, asserted) | working paper CF-14.4 (FIN-14 4.4) |
| SF12 | CF-14.4's "every hitter in a starting lineup" | the lineup rows of each January 31 depth chart, catchers in | the non-catchers only | same call (asserted) | CF-14.4; the depth charts' legend |
| SF13 | CF-14.4's "100 plate appearances in each of the two seasons before" | as the League counts them, every club | with the planning club only | same call (asserted) | CF-14.4 ("counting his plate appearances for every club") |
| SF14 | CF-14.4's "reached the threshold" | plate appearances at or above it | above it only | same call (asserted) | CF-14.4; the term sheets ("when the Player reaches its threshold") |
| SF15 | the ask's "playing-time bonuses other than plate-appearance bonuses" | FIN-14 4.1's class less plate appearances: the innings, starts, relief-appearance and Active List terms in the register's "Other playing-time bonuses" column, the pitchers' | award bonuses counted in, or hitters' games-started bonuses | the award reading adds $75,000 to 2024 and the All-Star amounts (AK5 'e45_all'); no hitter carries other terms | FIN-14 4.1 and 5; the register's column (asserted, SF15) |
| SF16 | the ask's "paid for each of the 2023, 2024 and 2025 seasons" | the season the bonus was earned: an October payment to its season, a January payment to the season before | the year paid | the pay-year reading files $35,000, $135,000 and $390,000 (asserted) | every January payment falls before that year's Opening Day (SF16) |
| SF17 | the ask's "paid" | paid through the December 11 pull, voids netted | earned, or gross of the void | same figures: every payment for 2023 to 2025 is made by January 15, 2026; gross adds $875,000 to 2025 (AK8) | the payroll register; SF17 |
| SF18 | an award bonus inside a playing-time payment | not a playing-time bonus | counted in | +$50,000, +$40,000, +$50,000 on three rows (AK7) | FIN-14 5 (asserted, SF18) |
| SF19 | "player by player" | the player paid, by the name each legacy line carries | the legacy number through the HRIS map, or to the register's ID | moves Benítez 2023 or Pietersz 2025 (AK5, AK6) | the payroll's own name on each line |
| SF20 | the excess in the season-end line after a contract's last season | salary the contract deferred to its end, not a bonus: out of the row | a playing-time bonus paid, counted in | +$255,000, +$430,000, +$350,000, +$690,000, +$620,000 on five rows (DF2) | FIN-14 3.2 (deferred salary) apart from 4.1's class; each line less the deferral is a bonus his terms allow and the whole line is above the largest (asserted, SF20, DF1) |
| SF21 | a contract's last season, paid in one season-end line | the whole season paid | a first half with the second unpaid | same figures: paid is paid, and the row is what the line carries less the deferral (asserted, SF21) | the payroll register (no later payment to those players for those seasons) |
| SF22 | the register's salary for a season | the contract's salary, gross of the deferral | the salary paid, net of it | the net reading leaves no deferral to take out: the full includer's figures (DF2) | every other contract's salary lines add to its register salary to the cent, and the five fall short by their deferral exactly (asserted, SF22, DF7) |

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
| R2e | the slot's rate with its substitutes' plate appearances, per start (the round 3 judge's near rival) | $4,500,000 | +1.11 | +0.38% | a substitute's plate appearances are not the starter's; the look-back on every reading, 0.30 to 0.61 per cent (LB9) |
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
  The rule 3 re-audit's outside read is higher and is the one to plan on: the basin is wide (any model form on the slot
  and catching over the depth-chart regulars files $4,250,000), so P(one lands) about 0.2 to 0.25 and P(both) about
  0.07 to 0.11, borderline at 0.1. Loop 2 kept the world, so the estimate stands; the margin to a basis filing another
  total is 0.2 to 0.6 per cent of the score (hitter-paired z 2.1 to 2.7).
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
that chooses the basis (4.4's look-back, its population, window, thresholds and score set in working paper CF-14.4)
and the arithmetic from the probabilities to the rounded totals; it leaves only which basis to build, and every reading
of every term converges on the golden or violates a quoted line (SF1 to SF14 for the call, SF15 to SF22 for the ask). The literal executor of 4.4 and CF-14.4
still has to bring bases to rank; the one basis the paper's words suggest (its own hitters' seasons) files $4,500,000. The easy answers come from easy bases
ranked by the same look-back, never from another reading.

## Oracles

- The vendor's 2027 projections and its past projections: a mean playing-time forecast per hitter; the look-back scores
  the bases built on them 25 to 104 per cent worse than the basis used; they confirm only that the five project to 578
  to 697 plate appearances; deleting the file leaves the golden and the ask (D1; a declared distractor, though the
  look-back reads it to score the vendor's bases).
- The box scores and the winter depth charts themselves: the history every basis fits and the look-back scores; nothing
  in them ties only under the golden.
- The 2027 schedule: 162 games a club under every method (a declared distractor).
- Nothing ties only under the golden: no 2027 projection of starts, no control total and no certified figure ships.

## Ask sheet

**Revision, 2026-10-28, the portal's third rubric return: a third device.** The portal scored the build at 72 per cent: both top responses missed the call (rows 1 to 6) and kept every other row, all 21 ask figures among them, so both earlier devices were handled in full (the catch-all's halves paired October to January, the contract-end lines reconciled against the register's salary). The third device is a catch-up transfer (D8, a settlement date for the event date): the legacy January run missed the half it owed Max White for 2023 and Joe Livingston for 2024, and the next season-end run settled it on the catch-all line with that season's half, one line a code a run. Read season by run, as both responses did, White files $60,000 for 2023 and $180,000 for 2024 and Livingston $50,000 for 2024 (his line's All-Star bonus taken out) and $150,000 for 2025, each a full bonus his terms allow, so no check against the register fails (CU2); what finds it is a contract season with no January half and the next season-end line exceeding the January half after it by exactly that season's October half, to the dollar (CU1), with no code, description or status marking the merged lines (CU3). Every ask golden is unchanged (the bonuses as earned), so `freeze.py check --mode rubric` passes with 0 ask figures moved: the device moved where the evidence sits, not what it sums to (H30); the payroll export lost the two January lines and the close-file index its row count, and no other file moved. The path both responses took now misses the three totals and four rows, 19 of the ask's 44 points on the portal's weights, so each sits near 53.

**Revision, 2026-10-28, the author's hardening: a second device.** The re-sited ask shipped at f4bcf386 with one
primary, the legacy catch-all carrying the pitchers' season-end halves. `ceiling.py` priced the careful path at 0 of 21,
but a solver who reads each pitcher's payments and adds the catch-all lines with every hazard handled kept 21 of 21
(pair 67.0 on Part 0's weights with both off the call, 82.0 on the portal's calibration), and so did the other full
handling, twice each January half, measured at this repair on the f4bcf386 pack at 21 of 21; the stage 4 leak reader
paired the two lines unprompted. The author asked for a second device from another family, so that a full handling of
the first still misses a block of figures, with the ask's wording kept. It is the contract-end settlement below. The
prompt, the call, every file the call reads (SEP4 against e93c6561) and the ask's shape (18 rows, 3 totals, whole
dollars) are unchanged. Seven ask figures moved: four rows whose last-season outcomes were re-drawn so each golden sits
below the largest bonus its terms allow (Benítez 2023, Ruiz 2024, White 2025, Reed 2025, all inside the settlement
device), and the three totals; `freeze.py check --mode rubric` passes with no key allowed.

**Revision, 2026-10-28, the author's re-site.** The shipped asks (the five's injured-list stints since 2024; the club's
plate-appearance bonuses paid for 2024 to 2026) were landed by both top responses at the portal, which missed the call
and still scored 84 and 79, because the frozen batting lines and Article 22 pinned every one of their figures
(`## Tried and rejected`, the 10-27 and 10-28 lines). The author re-sited the ask layer onto quantities no main-call file
pins and waived every ask figure, unit and rounding. The prompt's ask sentence now asks for the playing-time bonuses
other than plate-appearance bonuses the club paid for each of the 2023, 2024 and 2025 seasons, player by player and in
total: 18 player rows and 3 totals, whole dollars. No new file ships. Every file the call reads is byte-identical to
e93c6561 (SEP4, twelve files hashed); the payroll export, the HRIS map, the earning codes, the contract register (now
covering 2023 to 2026, its Notes sheet gone) and the close-file index moved; the transaction wire, the weekly report and
the Article 22 excerpt ship unchanged as distractors. `freeze.py check --mode rubric` passes with `--allow
deliverables.paid.1.total,deliverables.paid.2.season`: two ask keys whose old values ($900,000 and 2026) happened to
equal numbers in blocks 1 and 2, both ask figures the author waived. `--mode determinism` fails on the 48 moved ask
items, as a re-site must, and is recorded only.

**Main call's declared row population:** the two box-score files (every row and column the golden reads: player, game,
date, club, lineup slot, starter, plate appearances or their components), the crosswalk, the club directory, the
vendor's winter depth charts, the five term sheets, the 2027 depth chart, FIN-14, CF-14.4, the feed notes and the
calendar (the look-back also reads the vendor's projections to score the vendor's bases). Device and hazard rows in it:
0, asserted: the call computed from those files alone is the golden (SEP1); the ask is unchanged with every distractor
deleted (SEP2, D1); no main-call document carries a payroll code, a payment run, an employee number or the legacy
payroll (SEP3); every file the call reads hashes as shipped at e93c6561 (SEP4); the ask reads none of them (SEP5). The
ask is not keyed to the call, its construction or its figures: it reads pitchers' payments, and pitchers do not bat.

**The ask. The playing-time bonuses other than plate-appearance bonuses the club paid for each of the 2023, 2024 and
2025 seasons, player by player and in total** (18 rows and 3 totals, 21 figures).
- H18 home: the club's own record on the other playing-time bonuses FIN-14 section 4 accrues, the same liability's other
  measures, kept in the controller's file beside the plate-appearance accrual for the auditors: rows the call never
  reads, and nothing estimated, decided or booked from them, so a component of the accrual file and not a second
  decision.
- The unit, filed: FIN-14 4.1 names the playing-time bonuses (plate appearances, games played, games started, innings
  pitched, relief appearances and days on the Active List) and FIN-14 5 sets award bonuses apart; the register's "Other
  playing-time bonuses (each season)" column carries each pitcher's terms and no hitter's (SF15); salary a contract
  defers is salary under FIN-14 3.2, not a bonus (SF20); a bonus paid for a season is the season it was earned, every
  January payment falling before that year's Opening Day (SF16); paid means paid by the pull, every payment for 2023 to
  2025 made by January 15, 2026 (SF17).
- Primary device (D2, a label stored before a silent switch): until the January 2026 HRIS cutover the legacy payroll
  paid the pitchers' season-end payments (October 15) on its catch-all E45 OTHER BONUS, which the earning-code table
  migrates as BOT Other bonus, and their January halves on E40 PERF BONUS, which it migrates as BPA Playing-time bonus;
  the hitters' plate-appearance bonuses ran in full on E40 in October, so E40 and BPA read as the playing-time code
  (AK3, AK3c). The careful path executes the table and reads each line for what it says: it files every season it
  carries at exactly half, and a contract's last season, which no January half follows, not at all (AK4). The wrong
  reading is complete: every amount it carries is itself a full bonus the pitcher's own terms allow, and the seven
  seasons it carries nothing for read as seasons with no line reached (AK3d), so no check against the register fails,
  and nothing ties only under the golden. What finds it: a pitcher's OTHER BONUS line on October 15 equal to his PERF
  BONUS line the next January 15, in every legacy season but a contract's last, with no filed sentence, column name or
  battery sweep pointing at it. Work left after noticing: the All-Star bonus inside three season-end lines, the
  reissued legacy number, the void, each payment to its season, and the second device (Fair: the golden equals the
  season as it happened, every row, AK2).
- Second device (a grain device; its item deferred salary, its remedy a salary reconciliation): after the last season of
  a contract the legacy season-end run settled what the contract still owed, one line a code a run: the season's
  playing-time bonus in full, no January half following, and on five pitchers' contracts the salary the contract had
  deferred to its end, which the legacy payroll, having no deferred-compensation code, paid on the same catch-all. The
  family, stated plainly: the collision still lands on E45 and inherits the legacy's one-line-a-code-a-run from HZ1 (a
  shared cause, law 9), and it adds no new code label; what is new is the grain (one season-end line settling two
  obligations at a contract's end) and the remedy, which the full handling of the catch-all never reads. That
  handling ('settle_whole' in `calc.py`, `full` in `ceiling.py`) takes each of the five lines as the season's bonus
  and keeps the deferral (DF2): Yordy Benítez 2023 (line $310,000, deferral $255,000), Carlos Lara 2023 ($570,000,
  $430,000), Santiago Ruiz 2024 ($575,000, $350,000), Max White 2025 ($870,000, $690,000) and Tyler Reed 2025 ($875,000,
  voided and reissued, $620,000), and with them every season total. Twice the January half misses all seven of a
  contract's last seasons (DF4); cutting a line to the largest bonus his terms allow misses all five, each golden
  sitting below its maximum (DF3); splitting a line into a bonus his terms allow and the roundest remainder, a guess
  at a round non-bonus payment, misses all five too, each line's roundest split being a wrong bonus (DF8). The forcing figure (DF1, DF7, SF22): each of the five lines less any award is above
  the largest bonus the pitcher's terms allow, and the excess equals, to the dollar, the register's salary less the E01
  salary lines paid over the contract (Benítez $255,000 of 2023; Lara $430,000 of 2023; Ruiz $175,000 of each of 2023
  and 2024; White $230,000 of each of 2023 to 2025; Reed $310,000 of each of 2024 and 2025); every other contract's
  salary lines add to its register salary to the cent but two hitters' (their own deferrals) and the one assigned
  mid-season. Work left after noticing: the terms check says only that a line is too big; what it carries is rebuilt
  from the salary lines, season by season over the contract, against the register's salary columns (Lara's first
  contract reaches back to 2022, which the export does not hold, so his deferral is a 2023-only term, asserted). Silent
  (DF5): no shipped file states a club contract's deferral; FIN-14 3.2 states the policy and the term sheets the 2027
  signing's own deferral, payable 2033 to 2037. Benign twins (DF6): the same catch-all carries the deferred salary of two
  hitters whose contracts ended in 2024 (Herron's line alone, Cedeno's with his All-Star bonus), which the ask does not
  count.
- Hazards: HZ1 an All-Star bonus inside the legacy season-end line (Ruiz 2023, $50,000; Livingston 2024, $40,000;
  Pietersz 2025, $50,000; the line taken whole adds it, AK7); HZ2 a Cy Young bonus on the same catch-all in November
  (White 2024, $75,000; every catch-all line taken adds it); HZ3 legacy number 01661 reissued (Yordy Benítez's lines in
  2023, Gilmar Pietersz's from 2025: the HRIS map gives it to Pietersz and the register to Benítez, so either join moves a
  row, and the name on each line settles it, AK6); HZ4 a season-end payment voided and reissued (Reed's contract-end line,
  October 2025: summing gross adds $875,000, AK8); HZ5 the 2022 season's second half paid January 15, 2023 (Lara: the
  pay-year reading moves it into 2023, AK9); HZ6 benign twins (award bonuses and deferred salary to hitters on E45; the
  hitters' plate-appearance bonuses on E40, outside the ask by its words).
- Stops (measured, AK4, AK5, DF2 to DF4, DF8 and `ceiling.py`): the earning-code table's playing-time codes by season,
  every row it carries at half and a contract's last season absent ($135,000, $390,000, $280,000); the same codes by the
  year paid ($35,000, $135,000, $390,000); the catch-all lines taken whole (8 rows and every total: $950,000,
  $1,395,000, $2,445,000); every catch-all line in any month (9 rows, 2024 at $1,470,000); the full handling of the
  catch-all with every hazard (5 rows and every total: $1,210,000, $1,355,000, $2,395,000); twice the January half (7
  rows: $270,000, $780,000, $560,000); each row cut to his terms (5 rows: $650,000, $1,080,000, $1,230,000); each line
  his terms cannot hold split at its roundest remainder (5 rows: $510,000, $855,000, $770,000); every legacy number
  through the HRIS map (Benítez's 2023 row to Pietersz, 2023 at $470,000); every legacy number to the register's own ID
  (Pietersz's 2025 row to Benítez, 2025 at $1,025,000); the void's reversal left out (2025 at $1,960,000); the golden
  ($525,000, $1,005,000, $1,085,000). No stop total equals a figure of the call.
- Span: the payroll export (bonus and salary lines), the HRIS map, the earning codes and the contract register (its
  terms, awards, seasons and salary columns): 4 files, 18 columns on the golden's path; FIN-14 3.2, 4.1 and 5 for the
  class.
- Realism: a legacy payroll with few earning codes, its catch-all carrying what its clause types did not cover (award
  bonuses, the pitchers' season-end payments, deferred salary); a club settling everything a contract still owes in the
  season-end run after its last season; salary deferred to a contract's end in larger contracts, as the club's 2027
  signing also defers (term sheets); an HRIS migration mapping legacy codes one to one, keeping legacy history under
  legacy numbers and names, and migrating only the employees paid in its last year; a legacy system reissuing a
  departed employee's number; one payroll line a code a run; a void and reissue after changed bank details. None was
  placed to be caught: each pays what the contract owed.

**Hazard table**

| Hazard | Root cause | Moves | Delta |
|---|---|---|---|
| D2 the season-end payments on the catch-all code | the legacy payroll's clause types | every row and total | each row it carries at half, a contract's last season at nothing, on the careful path |
| D3 the contract-end line carrying deferred salary | the contract-end settlement, one line a code a run | 5 rows, every total | +$255,000, +$430,000, +$350,000, +$690,000, +$620,000 if the line is read as the bonus |
| HZ1 an All-Star bonus inside the season-end line | one legacy line a code a run | 3 rows, every total | +$50,000, +$40,000, +$50,000 if taken whole |
| HZ2 a Cy Young bonus on the catch-all | award bonuses on the catch-all | White 2024, 2024 total | +$75,000 if every catch-all line is taken |
| HZ3 a reissued legacy number | the legacy system's number reuse | Benítez 2023 or Pietersz 2025, a total | -$55,000 from 2023 or -$60,000 from 2025 |
| HZ4 a void and reissue | changed bank details | Reed 2025, 2025 total | +$875,000 if summed gross |
| HZ5 a 2022 half paid in January 2023 | the January run | 2023 on the pay-year reading | +$35,000 |

**Referee.** The register's terms (every amount the careful path carries is a full bonus, so they arbitrate nothing; on
the full includer's path they only say that five lines are too big, not by how much) and each season-end line's
January twin (equal except where an award sits inside, absent after a contract's last season). The salary lines tie the
deferral only on the golden's path, a reconciliation the ask never asks for. No file ties only under the golden.

| Ask figures | Cracker's path (`ceiling.py`, measured) | Cracker's value | Verdict |
|---|---|---|---|
| 2023 player rows (5) | the earning-code table's playing-time codes (E40, BPA), each legacy line by its name, voids netted, each payment to its season | Ruiz and White at half; Benítez, Casilla and Lara (a contract's last season) absent | miss |
| 2023 total (1) | the same | $135,000 against $525,000 | miss |
| 2024 player rows (6) | the same | five rows at half; Ruiz (a contract's last season) absent | miss |
| 2024 total (1) | the same | $390,000 against $1,005,000 | miss |
| 2025 player rows (7) | the same | Blair, Lara, Livingston and Pietersz at half; Reed, Robertson and White (a contract's last season) absent | miss |
| 2025 total (1) | the same | $280,000 against $1,085,000 | miss |

The includers, the risk the cracker sheet does not price (`ceiling.py`, both off the call; on the portal's calibration
in brackets): the catch-all lines taken whole keep 10 of 21 (38.2; 53.2); every catch-all line in any month, 9 (35.6;
50.6); the full handling of the first device and every one of its hazards, 13 (46.0; 61.0), the author's target case,
at or under 60 and about 65; twice the January half, 11 (40.8; 55.8); the full handling with each row cut to his terms,
13 (46.0; 61.0); the full handling with each oversized line split at its roundest remainder, 12 (43.4; 58.4); the full
handling of both devices, the salary reconciliation included, 21 (67.0; 82.0), the fair handling. With one response on the call and both on the full handling of the first device the pair is 62.5 (70.0 on the
portal's calibration): a call-lander and a second full includer together still reach the bar.
Mirror leakage: 0.0 per cent of the ask weight (the mirror stops at the same codes by the year paid, 0 of 21).
Pair ceiling: 53.0 (the portal's own weights from its 10-28 rubric, both responses off the call on the path both took there, every earlier device handled: rows 1 to 6 missed, rows 7, 8, 30 and 31 and the five instruction rows kept, and of the ask's 44 points the three season totals and the four catch-up rows, 19, lost; Part 0's weights give 28.5 for the cracker on the call and the mirror off it).
Measured by: `generator/ceiling.py`, on the cut target.zip (sha256 64554e72), 10-28 (its 'full2' includer keeps 14 of 21).

## Residual

What the shipped build still carries, each item measured and none moving a committed figure.
- **The thin rival.** The round 3 judge's near tie: the slot's rate read with its substitutes' plate appearances, per
  start (0.17367 on this build's construction, 0.17359 on the judge's, against 0.17301), files $4,500,000 (+1.11 bins;
  Rivas, Medina and Meeks a step higher). It loses the look-back on every reading, by 0.30 to 0.61 per cent
  (hitter-paired z 1.17 to 2.19), asserted in `checks.py` (LB9, LB3, L5) and in `verify.py`; it counts a substitute's
  plate appearances against the starter's start.
- **The candidate set is not enumerated** (4.4 and CF-14.4 name no basis; the round 2 judge's fork 1): a pooled
  at-slot basis without catchers apart files $3,750,000 and the look-back separates it (0.1940 against 0.1730). The
  exact-position variant sits $16,000 inside the $4,125,000 boundary and still rounds to $4,250,000.
- **Realism.** Player records carry little signal in this world: among the look-back's non-catcher hitters the
  vendor's projection correlates 0.005 with realised plate appearances and last season's plate appearances -0.04. Honest
  persistence was tried at loop 2 under a seed rule written first and made the total indeterminate (World seed rule,
  Outcome); the world keeps seed 1539, which a search over seeds chose.
- **Strength.** P(one strong solver lands) about 0.2 to 0.25 and P(both of two land) about 0.07 to 0.11 (the rule 3
  re-audit's outside read, Ladder).
- **The ask's open risks.** The cracker sheet prices the careful path, which files every row it carries at half; the
  full handling of the first device (each pitcher's October line beside his January line, every hazard handled) now
  keeps 13 of 21 (`ceiling.py`), because five contract-end lines carry the salary the contract deferred. What is left:
  (1) a solver who reconciles each pitcher's salary lines against the register's salary, and pairs the shortfall with
  the oversized contract-end line, lands both devices, 21 of 21 (67.0 both off the call on Part 0's weights, 82.0 on
  the portal's calibration); the terms check tells it five lines are too big and not by how much, and whether the top
  responses go on to the reconciliation only the portal measures; (2) one response on the call with two full includers
  of the first device puts the pair at 62.5 on Part 0's weights and 70.0 on the portal's calibration (a guess at a
  round non-bonus remainder no longer helps: 12 of 21, DF8); (3) the realism
  trade, made deliberately: the register extract carries no deferral column or note though FIN-14 3.2 names deferred
  salary and the club's 2027 signing defers, because a documented deferral is a work order the full includer would
  execute; a judge may read the extract as incomplete.
- **The heart BLOCK is a later builds' artifact (H27).** `guard.py heart` exits 1 on one rule, people.last: the surname
  of the register's payroll contact, Matthew Wallace (drawn for this build on 10-16), was drawn again by task179 and
  task174, both on 2026-10-28, after this card. Recorded with the dates; every other heart line is the WARN or NOTE of
  the last ship.

## Pre-ship check

- **The 10/10 rules against the built pack.** The decisive step is still analytical: FIN-14 4.2 to 4.4 and CF-14.4
  file the estimand and the look-back and name no basis, distribution, comparison set, rate per start, slot or catcher
  (R3s, asserted over both texts); 4.4 run on the bases at hand files $4,500,000 and its own hitters' seasons
  $4,500,000 (R3a, LB7); only the planned non-catcher regulars' starts at the new slot's rate win the look-back on every
  reading (LB1, SF11 to SF14, LB9). Layer 1 (two layouts and the crosswalk, catcher's interference, substitute lines,
  doubleheaders, suspended games, accents, traded regulars) is neutral: every mishandled reading leaves the call (R2).
- **Free gates on the final rebuild (the hardening, 10-28).** `checks.py` 289 assertions, 0 failed (the ask's AK1 to
  AK12, DF1 to DF8 and SF15 to SF22; SEP4 hashes the twelve files the call reads against e93c6561); `verify.py` agrees on
  its own path for the call and the 21 ask figures, the deferral taken from the register's salary less the salary lines
  paid; two builds byte-identical, target.zip sha256 3ded6ddd; `figures_check.py` 82 figures, 0 absent; `precut.py` exit
  0 (53 checks); `voice-check.py` PASS (609 characters, the prompt unchanged); container audit clean on the pack and the
  goldens; `leak.py` REVIEW, no LEAK (answered in the Build record); `guard.py validate` clean, `surface` the four
  promoted pairs of the last ship, `heart` BLOCK on people.last alone (Residual, H27); `freeze.py check --mode rubric`
  PASS with no key allowed (the main call, the stump, the card's stump and driver, the ladder, the default path and the
  call sentence unchanged; seven ask figures and the workbook moved).
- **The 10/10 rules after the repair.** The call's decisive step and every file it reads are untouched (SEP4), so the
  three rules read as at ship. The ask's first device turns on reading a legacy code against its substance and the
  second on reconciling the salary lines to the register's salary, both licensed for an ask by 2.1 of
  `supplemental-stumping`; nothing in either is planted (each payment is real, its amount the contract's, its code the
  legacy system's, and the deferral a term of the contract paid when the contract said).
- **Stage 4 (the hardening, 10-28).** Determinism judge pass 3 DETERMINISTIC, APPROVE
  (`determinism_check_report_pass3.md`, on target.zip 44480c2b): every figure of the call and every row of the table
  reproduced, the deferred salary in the contract-end line among them, no competing answer surviving; Gate G
  method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no; Gate H domain pass,
  layers pass, decisive step analytical. Leak reader CLEAN on the same pack (no sentence names a step for the table, no
  file ranks, nothing reads as planted, the payroll, register, HRIS map and code table read as one club's records; it
  did not surface the deferral). After both, the five deferral amounts were re-aimed (`## Tried and rejected`, the
  roundest split): no graded figure, clause, document or prompt moved, so the APPROVE stands for the shipped pack
  3ded6ddd under `determinism-check` (an APPROVE is voided only by a change to a graded figure or a clause a gate turned
  on) and the reader is not re-run (only a record file changed); `leak.py` and every free gate re-run on it.
- **Personas in the pack.** Harry Barnes, Steven Armstrong and Matthew Wallace (drawn with `guard.py names`); the
  players from the generator's ranked pools, the designed names on the card.

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
- Honest persistence (loop 2): a career durability (lognormal, sigma 0.8) on each player's injured-list and day-to-day
  chances and a lost job likelier for a weaker regular, the seed by the rule written first (1601). The look-back's winner
  became a credibility blend on the player's own starts and the bases tying it filed $5,250,000 and $5,500,000 with
  different player figures (seeds 1602 and 1604 the same shape a bin lower): a continuous weight the look-back pins to
  about 0.1, each 0.1 about a bin. Stopped under the coordinator's rule and reverted (World seed rule, Outcome).
- FIN-14 4.4 carrying the look-back's hitters, thresholds and score in the policy itself: it read as a filed procedure
  (coordinator, loop 2); the policy keeps the principle and close-file working paper CF-14.4, in the controller's voice,
  holds the test.
- League names from about 330 US and 95 Hispanic surnames (408 in all): the signings' surnames recurred 5 to 18 times
  and near-duplicates crossed them (an Ángel Rivas beside Ángel Medina and Andres Rivas); renamed once every player exists, from
  ranked pools of 879 US and 254 Hispanic surnames on its own stream, the designed players and the namesake pitcher kept.
- Ask B's "bonuses we paid" for 2026 open to the season's bonus as earned, both halves (the judge's fork 3, $825,000
  against $412,500): the prompt says "paid to date" (SF15).
- The club's 2027 pitching staff drawn new: the 2027 depth chart asked for it before the 2023 to 2026 staffs existed, so
  no 2026 pitcher was on it; every staff now exists before the league is named, and 2027's carries over from 2026.
- Ask A as shipped (portal return of 10-27): the date a stint took effect is forced as the weekly report's first date of
  reinstatement less the 22.2 minimum (the round 2 judge's own words), so a reader who executes 22.1, 22.2, 22.7 and
  22.9 on the wire, the report and the calendar files every row; `generator/ceiling.py` on the shipped pack, 18 of 18,
  and both top responses landed all nine rows. The prose cracker row ("the move's date as the date it took effect")
  was the mirror's path.
- Ask B as shipped (same return): the register's Notes file the population, the season, the reissue and the legacy
  code, and the batting lines, which are the call's own pristine files, pin each payment's plate-appearance part, the
  payroll amounts tying exactly; `ceiling.py`, 10 of 10, and both top responses landed every figure. The prose cracker
  row (the payroll lines at face value) was the mirror's path too.
- Re-siting either ask (rubric repair, 10-27): every quantity the ask-only files yield is executable, because the
  wire, the weekly report, Article 22, the calendar, the register, the payroll and the HRIS map agree with one another
  and are documented, and the batting lines any of them would be checked against are pristine; a filed sentence that
  makes an ask determinate names the quantity's source, and withholding it opens a fork. Screened on paper against the
  count test (a cross-file count tying under one reading only, no filed sentence adjudicating, every figure moved, work
  left after the discovery): the wire dating each placement by the date it takes effect, with the ask on the date he
  left the Active List (22.9 names the report's transaction date, so a sentence adjudicates and noticing is the
  remedy); days on the Active List (a determinate count needs a pin naming the transaction date, the same sentence, and
  a relief pitcher's games-finished and Active-List split inherits it); a reissued legacy employee number shown under
  the later holder's name (passes the count, the 2024 installments summing to the earlier holder's register salary,
  but moves two of 28 figures); a month-grain injured-list days statement in place of the report's eligibility column
  (a reader matches its days and recovers the date); an official plate-appearance certification departing from the
  feed (a reconciliation break whose discovery is its remedy). None holds every row, so no pack was cut and the ask
  side waits on the author: a new ask-only source the author approves, or a re-root.
- Ask A held as worded with a new League source (rubric repair, 10-28, the author's new ask-only source): the weekly
  report's first date of reinstatement withdrawn and a League service-time ledger by player, club and month (days on
  the active list, on an injured list, on other lists) added, so each date had to be rebuilt from a month's days. The
  frozen batting lines pin every date with no report at all: the day after the player's last batting line before the
  move, never more than three days back, lands 18 of 18 figures (`ceiling.py`), and Medina's first 2024 stint is
  forced outright (last line May 18, activated May 29, 10-day list: May 19 only, by 22.2). No League-side source can
  hold a row; designations moved off the day after the last game would also leave Medina's row where it is.
- Ask B held as worded with a new club source (10-28): an off-cycle bonus register outside the player earnings export,
  a treasury or accounts-payable channel to a departed player, a contract-amendment log behind the register's terms,
  and the register's terms withdrawn with each installment row carrying the season's award. The cracker's route reads
  no payment amount and the club paid to the contracts (11 of 12 lines to the dollar, the twelfth by Cedeno's filed
  All-Star term, `ceiling.py`, as B3c asserts), so a primary moving every row needs off-contract payments on every
  player-season, a plant; a channel moves only its own player, and withdrawing the terms leaves two readings of an
  installment row that only a control settles, which the cracker matches.
- Re-wording either ask with every figure kept (10-28): every date-and-days quantity about a batter (the date a stint
  took effect, its transaction, its reinstatement, the days it covered, its days on the 60-day list) is fixed by the
  batting lines and Article 22 or read off the wire, and every plate-appearance payment by the register and the
  batting lines, so a wording that keeps the figures keeps the pin. Holding the asks needs a re-site that changes
  their figure shapes onto quantities the main files do not pin (the club's own cash where no box-score formula
  reaches it), the author's decision; nothing was cut.

- Ask A replaced (the author's re-site, 10-28): what the responses did to it is in the 10-27 and 10-28 lines above (the
  report's first date of reinstatement less the 22.2 minimum, and the batting lines alone, file all 18 figures). Every
  quantity about the five's injuries is fixed by the frozen batting lines or read off the wire, so no device moves it;
  the wire, the weekly report and the Article 22 excerpt now ship unchanged as distractors.
- Ask B replaced (10-28): both top responses filed every figure, the club having paid its hitters exactly to contract on
  batting lines the call freezes (11 of 12 lines to the dollar). Re-sited onto the pitchers' playing-time bonuses, which
  no batting line can pin because pitchers do not bat; the hitters' plate-appearance bonuses stay in the payroll as the
  lines that make E40 read as the playing-time code, outside the ask by its words.
- Screened for the re-site on paper before anything was cut (10-28), each landed by the careful path: the pitchers'
  bonuses earned from a League pitching file (a formula over clean innings and appearances, and its layout could only
  go in the frozen feed notes, H9); days on the Active List (whether a backdated placement leaves the Active List from
  the date it takes effect or from the transaction needs a pin that hands the device over); the 2027 pitching staff's
  injured-list stints (the report and 22.2 file every date, and the injury record of players outside the five is not
  behind the call); a ledger roll-forward of the accrued bonuses (every figure a journal line read or summed); award and
  escalator bonuses (FIN-14 5 sets awards outside the accrual, and each is an announcement read against a term);
  pitchers' 2027 bonuses as expected amounts (a second forecast, and CF-14.4 sets a look-back for plate-appearance
  bonuses only); the five's signing-bonus and deferral entries (pinned by the frozen term sheets, and outside the
  bonus accrual).
- The first draft of the re-site (10-28) left a tell on the careful path: 9 of its 18 January halves were not a full
  bonus any combination of the pitcher's own terms gives (White's $52,500 against $60,000 and $45,000 lines), and the
  hitters' bonuses ran in two halves beside the pitchers' one, so a check of payments against the register pointed at
  the missing season-end halves. Each pitcher-season now reaches an even count of equal lines, so every half is itself a
  full bonus (AK3d), and the hitters' plate-appearance bonuses run in full in October. The same pass moved two outcomes
  whose 2024 half equalled the 2025 total (Lara, Livingston), which had let the pay-year reading hit two rows.

- The re-sited ask with its one device (f4bcf386), measured at the hardening (10-28): besides the full includer of the
  catch-all lines (21 of 21), twice each January half lands all 21 figures, a second full handling of the first device,
  so any device that leaves a January half clean and loads only the October line hands the row to the doubler.
- Second devices screened for the hardening and rejected (10-28), each against the full includer's invariant (a
  pitcher-season is his October line plus his January line, less an award its twin shows), with no pitching statistics
  in the pack to force anything a payment does not show:
  a bonus split across two clubs after a trade is invisible under "paid" (the payroll holds what we paid either way), and
  its offseason-assignment variants give a row the cracker lands (a January half we paid on E40 for a season with
  another club) or one the full includer lands; a later check, or an installment or deferral schedule on the bonus
  itself, is placed by the twin check and the month paid, and a delay long enough to fool it (past the next July) is
  forced only by a filed schedule, which the includer executes, or by pitching statistics, which would make it a fork;
  record identity at block scale (legacy history attached to each number's latest holder, several numbers reissued)
  moves at most six figures, its rows turn up as orphans an unmatched join sees, and the totals move only if the
  includer drops the stray lines; what the HRIS migrated (departed players' legacy history only in the legacy year-end
  registers at calendar-year grain, the departed pitchers' 2025 second halves in a December 2025 final run) misses 8 on a
  natural annual reading, but the twin pairing that found the first device splits the year's E40 total by equal halves
  at once, discovery and remedy one act; deferred salary paid with a season-end half while a January twin follows makes
  the October line exceed its twin, and twice the January half lands the row; an award paid in halves inside both twins
  is HZ1's family and the terms check finds every pair that is not a valid combination; a currency or tax-year basis has
  no record in this world beyond the pay year, already the mirror's stop. The device that holds sits on a contract's last
  season, which no January payment follows, and is resolved only from the salary lines.
- Contract-end outcomes at their terms' maximum (Benítez 2023, Ruiz 2024, White 2025 and Reed 2025 as first drawn):
  cutting an oversized line to the largest bonus his terms allow would have landed each; re-drawn below the maximum
  (Benítez one innings line of two, Ruiz three lines of four, White three of four, Reed three of four), the ask's
  figures waived by the author.
- The first-drawn deferral amounts (Benítez $300,000; Lara $450,000; White $250,000 and Reed $325,000 a season), found
  after stage 4: four of the five oversized lines split at their roundest remainder into the true bonus, so a solver who
  guessed a round non-bonus payment instead of reconciling the salary kept 19 of 21 (`ceiling.py` 'round'). Re-aimed to
  amounts whose roundest split is a wrong bonus (Benítez $255,000; Lara $430,000; White $230,000 and Reed $310,000 a
  season; Ruiz's $175,000 a season already split wrong): the guess keeps 12 (DF8), and no graded figure moved.

## Build record

Stage 3, built 2026-10-16 (world seed 1511), PAUSED at 5e385a0. Stage 4 repair, built 2026-10-16 (world seed 1539),
PAUSED at 5a71a64. Stage 4 loop 2, built 2026-10-17 from `task151/generator/build.py` on the same world (seed 1539; the
platform batting file byte-identical to 5a71a64's, every other change a name, CF-14.4, FIN-14 4.4's wording or the
club's pitching staffs).

Ship, 2026-10-17: judge round 3 DETERMINISTIC, APPROVE; the write-up and the record only (step 4's grouping stated,
rival scores dropped from blocks 1 and 3 and from the memo, LB9 and the 2022 to 2025 window asserted, the residual
recorded); the pack unchanged (target.zip 83bf068f).

- Pack: 21 files, 5 formats (csv, json, pdf, txt, xlsx); the spine 276,378 batting lines (`lsf_batting_2021_2024.txt`
  184,271 rows, `lsf_batting_2025_2026.csv` 92,107); distractors `hvbd_hitter_projections_2022_2027.csv` and
  `league_schedule_2027.csv` (metadata.json); the close-file index `ral_close_file_index_2026-12-11.csv` (was
  export_manifest); the working paper `CF-14.4_look-back_working_paper.pdf` (loop 2).
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
- Loop 2 items: step 4 of the write-up and the look-back sheet price each tested hitter from his own group's seasons
  (catchers from the catcher regulars'); the prompt's "paid to date" (SF15, the earned reading $825,000 for 2026
  asserted, B2); the league renamed (945 surnames, the commonest twelve times; the signings' surnames as in the
  header); FIN-14 4.4 cut to the principle with CF-14.4 holding the test (R3s reads both); the memo's line on the
  record now states the look-back's finding (the regulars' seasons at the new slot forecast better than each hitter's
  own recent seasons) instead of saying a regular's next season does not follow his last ones; the 2027 pitching staff
  carried over from 2026.
- Gates: `checks.py` 278 assertions, 0 failed; `verify.py` agrees on its own pandas and pdftotext path (the accrual, the
  five player figures, the vendor's band, the at-hand pick, the step figures, the look-back for four bases, the nine
  stints and the bonuses paid); two byte-identical builds (target, goldens, metadata.json, submission.md, figures.json,
  target.zip 83bf068f); container audit clean on the pack and the goldens; `figures_check.py` 87 figures, 0 absent;
  `precut.py` exit 0 (49 checks); `voice-check.py` PASS (779 characters); `leak.py` REVIEW, no LEAK (answered below);
  `guard.py validate` clean, `heart` WARN (answered under Draw), `surface` promotes nothing.
- `leak.py` REVIEW lines, each harmless: FIN-14's and CF-14.4's "4.4" is the section the write-up cites and the paper
  serves; the register's "$125,000
  each" and "$225,000 each" beside the $125,000 and $225,000 the club paid two veterans (each reached one line with the
  club; the register's term is the input); the term sheets carry the call's words (they are the contracts the call
  accrues for); FIN-14 and CF-14.4 carry five of the stump paragraph's terms each (FIN-14: appearances, look-back,
  planned, contract, record; CF-14.4: appearances, look-back, starting, contract, lineup): 4.3 names the planned role
  and CF-14.4 the hitters a basis is tested on, and neither names a basis, a slot, a rate per start or catchers; the feed notes carry five (appearances, catchers in "catcher's interference",
  lineup, batting, position), field definitions naming no method; the projections, the depth charts, the wire and the
  term sheets name the five beside numbers (projected plate appearances, ages, transaction IDs, contract terms), none an
  accrual or a ranking on it; the calendar's and the 2027 schedule's dates after December 11, 2026 are the 2027 season's
  (forward-looking by nature). A first cut carried a $1,000,000 signing bonus and salaries ending in 500,000 beside the
  $1,000,000 and $500,000 player accruals (LEAK); the signing bonuses and salaries moved ($1,250,000, $1,750,000,
  $9,750,000, $15,750,000, $9,250,000).

Rubric repair, 2026-10-28 (the author's re-site): the ask layer re-sited onto the playing-time bonuses other than
plate-appearance bonuses the club paid for 2023 to 2025 (21 figures), the main side frozen. Generator: `records.py`
(the pitchers' contracts and their lines reached each season, the hitters' games-started terms dropped, the HRIS cutover
moved to January 1, 2026, the legacy catch-all E45 for the pitchers' season-end halves, the reissued number, the void
and reissue, the register to 2023 to 2026 with no Notes sheet), `calc.py` (the ask and its stops), `checks.py` (AK1 to
AK11, SF15 to SF19, SEP4 and SEP5 against e93c6561, H6, H9b, B8, GD3), `verify.py` (its own pandas path for the ask),
`deliver.py` (the ask sheet, step 8 and block 4), `metadata.py` and `docs.py` (distractors, coverage), `ceiling.py`
rewritten. Gates: `checks.py` 274 assertions, 0 failed; `verify.py` agrees; two builds byte-identical (target.zip
f4bcf386); `figures_check.py` 82 of 82; `voice-check.py` PASS (609 characters); `precut.py` exit 0 (53 checks);
`leak.py` REVIEW, no LEAK (answered below); container audit clean; `guard.py validate` clean, `heart` WARN (no BLOCK),
`surface` four promoted pairs (answered below); `freeze.py check --mode rubric` PASS with the two waived ask keys
allowed.
- `leak.py` REVIEW lines new at this repair: the register's "$140,000 each" (a hitter's plate-appearance term) and
  "$60,000 each" (a pitcher's relief-appearance term) beside ask figures of $140,000 (Lara 2023, Blair 2025) and $60,000
  (Casilla 2023): the register is the ask's input, and each figure is two lines of another amount. Every other REVIEW
  line is the shipped build's, answered above. A first cut put Reed's 2025 row at $320,000, which the frozen term
  sheets carry as one signing's line amount (LEAK); his line amount moved to $85,000 and AK12 now asserts no ask figure
  stands in a shipped document.
- `guard.py surface` promotes task155 and task472 at 0.101 and task184 and task158 on card structure. The shipped pack
  scores the same against the first two (0.1007, computed from the e93c6561 zip with the same weights): the layout and
  format axes alone, no shared file name, wording or entity, both builds delivered after task151's last surface read
  (H31). The structural pair is the call's own card, differentiated against both (heart's notes), and untouched here.
- Stage 4 (10-28): determinism judge DETERMINISTIC, APPROVE (`determinism_check_report_pass2.md`): every ask figure
  reproduced and no competing answer survived (the 01661 reuse closed by the name on each line, the three All-Star
  amounts by the register's award column, White's November line apart, the void netted); Gate G method_or_model_selection,
  analytical_non_defect, surface_read_dependency no; Gate H domain pass, layers pass, decisive step analytical. Its
  thread had step 8 in hand and recomputed player by player, so the pass shows the ask forced, not how strong it is.
  Its two notes: the transaction wire, the weekly report and the Article 22 excerpt stay as distractors because they
  carry the five's own injury record, which a solver weighing FIN-14 4.3's health clause or the players' own seasons
  (rung R0b) reads, and deleting each leaves the call and the ask (D1); the rubric's criteria come from the prompt's
  shape: the total and five player accruals (6), 18 player rows and 3 season totals (21), the memo (1), 28 before the
  instruction-following lines.
- Stage 4 (10-28): leak reader CLEAN (`leak_check_report.md`, Solver's-eye read): no sentence names either step, no
  file ranks, every REVIEW line harmless. Two of its notes are the open risk stated in Residual: it read the pay year
  against the season earned as two readings (the judge, who recomputed, found the season earned forced), and, reading
  player by player, it paired a pitcher's October OTHER BONUS line with his January PERF BONUS line unprompted, which
  is the full includer's route. Its other notes sit in frozen main-call files (the vendor's December 1 projection after
  two signings, which the golden basis does not read; the five's signing order equalling their lineup order).

Rubric hardening, 2026-10-28 (the author's second device): the ask's wording, the call and every file the call reads
unchanged. Generator: `records.py` (the salary each of five pitchers' contracts and two hitters' defers to its end, the
salary lines paid net of it; the season-end run after a contract's last season settling the season's whole bonus and
the deferral in one catch-all line; four last-season outcomes re-drawn below their terms' maximum; the deferral amounts
re-aimed after stage 4), `calc.py` (the golden takes the deferral out, found as the register's salary less the salary
lines paid over the contract; stops `settle_whole`, `double`, `cap`, `roundest`), `checks.py` (DF1 to DF8, SF20 to SF22;
AK1, AK3, AK3b, AK3d, AK4 and AK5 restated for the contract-end seasons; GD3 reads the workbook's new column),
`verify.py` (the deferral on its own pandas path), `deliver.py` (the workbook's deferred-salary column and notes, a blank
January cell where none was paid, step 8), `ceiling.py` rewritten with the includer paths `full`, `double`, `cap`,
`round` and `full2`. Gates as in the Pre-ship check; `ceiling.py` on target.zip 3ded6ddd: the cracker 0 of 21, the
mirror 0, the full handling of the first device 13 (46.0 both off the call on Part 0's weights, 61.0 on the portal's
calibration), twice the January half 11, cut to the terms 13, split at the roundest remainder 12, both devices handled
21.
- `leak.py` REVIEW lines new at this repair: the register's "$55,000 each" (Benítez's innings term) beside his 2023 row
  of $55,000 (one line reached), and "$225,000 each" (Nunez's plate-appearance term, a hitter's) beside Ruiz's 2024 row
  of $225,000 (three of his $75,000 lines): the register is the ask's input, and each figure is the pitcher's own lines
  or another player's term. The stump-term sweep now draws "contract" from this note and so reads the term sheets
  (season, appearances, contract), FIN-14 and CF-14.4 as before: the term sheets are the contracts the call accrues for,
  FIN-14 and CF-14.4 the frozen policy and paper answered above. Every other REVIEW line is the last ship's.
- Stage 4: the judge (pass 3) and the leak reader as in the Pre-ship check. The judge's one informational note, that the
  card's `analyst_test` opens on $4,500,000 beside a list without it, misreads the sentence: $4,500,000 is the default
  path's figure (the look-back run on the bases at hand), named first, and the list after it is the other rungs; the
  card is left as it is. The reader read FIN-14 4.4 as naming the decisive step (choosing the basis by a back-test) and
  its question 6 as an analytical choice: 4.4 is the filed selection criterion that names no basis, unchanged since the
  round 1 repair and judged so in every round. Its question 3 names the League's feed notes and the close-file index, both
  frozen main-call files carried since e93c6561.
- The ask's two earlier devices, after the portal's third rubric return on 2026-10-28 (72 per cent, both responses off the call and holding all 21 ask figures): the catch-all's season-end halves were paired with the January halves after them, and the contract-end settlements were reconciled against the register's salary, by both responses in full. Kept as they stand, with a third device of another family beside them (the catch-up transfer, the ask sheet).
