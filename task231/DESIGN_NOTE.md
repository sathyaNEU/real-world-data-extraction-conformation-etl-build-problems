# task231 design note

The Brevland Central Bank's quarterly Business Conditions Survey (BCS), a panel of firms in twelve regions (doubled in
March 2024; 8,604 firms invited to the September 2026 round). The September 2026 round's main fieldwork closes at 17:00 on Friday 25 September 2026. The
BCS fieldwork quality standard sets each region's alert level on the round's response rate over the panel firms that
were still trading on the round's frame date, 1 September 2026: under 55 per cent the region goes into the two-week
reminder-call extension (28 September to 9 October), 55 to under 58 per cent it gets one extra email reminder, 58 per
cent or more it needs neither.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task231.json`, architecture v1, drawn 2026-10-13. Survey Research &
  Official Statistics (client domain), task type `nonresponse-calibration-measurement-error-adjustment`, objective
  Data Quality Monitoring & Alerting. Shape 10 (each region's response rate checked against the 55 and 58 per cent
  lines), decision `designation_set`, question form which. Gap time then population; no A to E pattern, decisive
  generator G12 (absence of a closure record is not a record of trading), then G11 (eligibility precondition). Gate G
  `forecasting`: the decisive figure is the share of this round's non-returners that the register will eventually
  show had already closed. Strategy `maturity_censoring`. Calibration `realised_outcome_roster` (the register's
  settled closures for earlier rounds). Stakeholder: the head of the business survey unit (`statistical_office_head`),
  deciding with her team (`line_manager_or_team`) at the close of main fieldwork (`period_close`).
- **Seed:** DQ04 (network-total shortfall alert with imputed missing reads), kept as an idea seed only: a network of
  reporting zones, a shortfall alert for the round being closed, a quantity completed for the units whose state is
  missing. The seed's Rubin's-rules pitfall is a reflex once implicates ship, and its GSD framing reads as a backdrop,
  so the pitfall is re-found in survey nonresponse: the missing state is whether a silent firm is still in scope.
- **Data-native sentence:** the business register learns of a closure only when the firm, its liquidator or the tax
  office notifies it, a year or more after trading stops for strike-offs and liquidations, and the contact centre can
  confirm a closure only if someone still answers for the firm, so the round's non-returners hide closures that only
  the settled records of earlier rounds can count.
- **Guard:** `guard.py check` WARN only. `repeat.gate_g` (forecasting, against task229): the label repeats, the
  mechanism does not (task229 carries a convex rating curve's bias into 2027 months; task231 nowcasts the register's
  eventual closures among current non-returners). `repeat.question_form` (which, against task188): the call picks
  regions, so which is the form the decision takes. `test.same_puzzle_older` against task445 v1 is differentiated on
  the card (task445 completes amounts held by late reporters; task231 estimates membership of the denominator).
- **Sources, one line each.**
  - Client Layer 2 patterns for the task type (cells before calibration, raking to convergence, sensitivity and
    specificity of a classification): none is this build's step; it is the unresolved-eligibility estimate that
    AAPOR leaves to "the best available scientific information".
  - Client measured drivers: the held tasks built an unfamiliar unit upstream of every graded figure; here the unit is
    the in-scope firm, and the construction is its scope at the frame date, not a replay of certified figures.
  - Family record: the maturity attack held where the graded object crystallised after the extract and the tail sat in
    a registry the natural pipeline never joins (73 world seven); task451 completes payments from the development in
    force and task255 truncates and censors a size distribution; neither estimates whether a unit belongs to the
    denominator.
- **Shape arithmetic (10, threshold checks per segment):** twelve regions' alert levels (12), the call's three lists
  (extension, email, neither: 3), the slide's named parts (a bar per region, the 55 and 58 per cent lines, the title
  naming the extension regions: 4), the two files (2): 21 on the main side, before the asks' 66 figures.

## Default path

1. Read the September 2026 invitation list (`bcs_invitations_2026_09.csv`, the panel firms invited, by region) and the
   returns received by 17:00 on 25 September (`bcs_returns_2026_09.csv`), keeping one return per firm where a firm
   answered by web and by phone.
2. Join the invited firms to the business register's closure extract (`brevland_business_register_closures.csv`) on
   company number and drop the firms whose recorded cessation date is on or before 1 September 2026 (24 firms).
3. Take each region's response rate as its returns over the invited firms that remain.
4. Set the alert level from the standard's lines: under 55 per cent the extension, 55 to under 58 the email.

Ends on: five regions into the extension (Capital, Harbour, Islands, Border and Western Uplands) and seven onto the email.
Golden: Capital and Harbour into the extension, Islands and Western Uplands onto the email, the other eight neither.

## Stump sentence

The default path counts every non-returning firm without a business-register closure as still trading and sends five
regions into the extension (Capital, Harbour, Islands, Border and Western Uplands) and seven onto the email; the register
records a strike-off or liquidation a year or more after trading stops, so most firms that closed before 1 September are
not yet on it, and the closure share of the round's non-returners read from rounds old enough for the register to have
recorded their closures leaves only Capital and Harbour for the extension and Islands and Western Uplands for the email.

## Three rules

- Task type: `nonresponse-calibration-measurement-error-adjustment` (Survey Research & Official Statistics), which
  serves Data Quality Monitoring & Alerting.
- Domain test: the decisive quantity is each region's response rate over the panel firms still trading on 1 September
  2026, with the eligibility of the unresolved non-returners estimated (AAPOR's e for unknown-eligibility cases), the
  field's own estimator, here from the register's settled closures for earlier rounds.
- Swap: "which regions' meter read rate among connected meters falls below 98 per cent, with disconnections recorded
  late" keeps the arithmetic but loses the survey quantity: there is no in-scope population fixed by trading status at
  a frame date, no nonresponse follow-up whose success depends on the outcome, and no unresolved eligibility to
  estimate; the task stops being a survey-nonresponse question.
- Layer 1: the register's two dates per closure (its own procedure); the contact centre's two teams with their own code
  schemes and keys (the contractor's records carry its own copy of company numbers, some in the six-digit form, and the
  bank's pre-2023 region codes); calls placed and calls received in one log, dialler retries the same day, transfers to a
  supervisor; returns by web, phone and post, a few firms returning twice; paper returns keyed by an outside bureau since
  2023 and telephone returns loaded overnight since April 2024; timestamps in UTC against a 17:00 local close; round labels
  in three forms (2026-09, 2026Q3, frame dates); a 2023 regional review that renamed two regions and recoded all twelve;
  panel IDs freed in the 2024 expansion block issued again; NACE Rev. 2.1 sections for recruits from 2025. Each comes from
  the systems that make the files; none is placed to be caught, and none sits on the decisive path (the main files carry
  one company-number form, the settled rounds hold true reach times and one holder per panel ID).
- Layer 2: `maturity_censoring` in the field-method family; the estimate of how many of this round's non-returners
  were still trading on 1 September decides each region's alert level.
- Decisive step: estimating the eligibility of the unresolved non-respondents from the settled outcomes of comparable
  earlier non-respondents (rounds old enough for the register to have recorded their closures), instead of treating
  the register as it stands as complete or carrying the call centre's resolved mix onto the unresolved.
- Not semantics: reading every field right (the two closure dates, both company-number forms, the outcome codes)
  still leaves the September non-returners' closures unrecorded; the register is read correctly and is simply not yet
  complete, so no reading fixes the denominator.
- Not rule application: the quality standard defines the response rate over firms trading on the frame date and
  leaves open how the trading status of a silent firm is established; no filed rule or procedure estimates it, so
  executing every stated rule still files the register-as-it-stands answer.
- Analyst test: a strong analyst who deduplicates the returns, drops the firms the register shows closed by 1 September
  and divides each region's returns by the rest sends five regions into the extension (the default path's Ends on:
  Capital, Harbour, Islands, Border and Western Uplands) and seven onto the email; one who gives the unresolved
  non-returners the eligibility of the call centre's resolved cases, or reads the closure share from every earlier round
  or the last two years, still sends four (Capital, Harbour, Islands and Western Uplands), where only Capital and Harbour
  fall under 55 per cent.
- Estimand: the BCS fieldwork quality standard (`BCS_fieldwork_quality_standard_v3.pdf`, sections 4 and 5) defines the
  round's response rate as the panel firms that return the questionnaire by the main close over the panel firms invited
  to the round that were trading on the round's frame date, says that a firm whose business ceased on or before the
  frame date is out of scope whether or not the register yet shows it, and sets the three alert levels; the frame date
  for September 2026 is 1 September 2026 (`BCS_round_calendar.xlsx`).
- No decoy: nothing is planted; the register's lag, the contact centre's selective confirmations and the panel's
  history are the systems' own behaviour, no memo, draft or dashboard carries a region list, and no artifact ranks the
  regions.
- No certified replay: no published or certified figure is reproduced to recover the method; the settled rounds are
  evidence for an estimate, not controls the method must match.
- Lesson: a response rate's denominator is a population fixed at a date, and when the register that defines it lags,
  the eligibility of silent units has to be estimated from cases whose fate has since become known, not taken from the
  record as it stands or from follow-up that reaches only the units still there; no build on file teaches the
  eligibility of non-respondents.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R1 register closures recorded by 25 September dropped (the default) | the standard's scope sentence sends the solver to the register | the closure extract joins on company number | yes, the first move | none | the join is the battery's own work | one subtraction | readable |
| R2 AAPOR proportional e from the contact centre's resolved outcomes | none, but AAPOR is the textbook for unknown eligibility | the call log carries outcome codes per firm | yes, the survey statistician's default | none | no | one ratio | readable |
| R3 closure share from the last two years of rounds | none | the register's two dates show the lag | the most recent rounds look the most relevant | none | no | one ratio over a join | readable |
| R4 closure share from every earlier round | none | as R3 | pooling all history is a reflex | none | no | one ratio over a join | readable |
| R5 (decisive) closure share from rounds old enough to be settled (frame dates at least four years before the extract) | none: no sentence names settled rounds, a share or a window; the register's notes say only that closures are recorded when notified | no column marks a round as settled or a firm's status at a frame date | every reflex above lands elsewhere | no control or corpus scores the routes | the records are complete as recorded; the battery finds nothing | built from 23 rounds' non-returners joined to the register with each round's own frame and close | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | region | the region on the September 2026 invitation list (regions as reviewed in 2023) | the region at recruitment | same call | C1: the invitation list carries the current region for every invited firm; no main-population firm changed region since recruitment |
| SF2 | panel firms invited to the round | the firms on `bcs_invitations_2026_09.csv` | every firm the panel register shows active | same call | C1: the active panel and the invitation list hold the same firms (asserted) |
| SF3 | returned by the main close | received by the bank by 17:00 Brevland time on 25 September 2026 | received by 17:00 UTC | same call | standard section 4 (17:00 Brevland time) and C1: no September return is received between 15:00 and 17:00 UTC on 25 September |
| SF4 | trading on the frame date | no cessation on or before 1 September 2026 | no cessation before 1 September | same call | standard section 4 ("ceased on or before the frame date") and C1: no main-population cessation falls on 1 September |
| SF5 | frame date | 1 September 2026 | the invitation date or the close | same call | `BCS_round_calendar.xlsx` (frame date column) |
| SF6 | response rate | returns by the close over invited firms in scope | returns over all invited firms | the default's call and worse | standard section 4 (the scope sentence) |
| SF7 | alert levels | red under 55, amber 55 to under 58, green 58 or over | strict or inclusive at either line | same call | standard section 5 and C1: every settled-round estimate sits at least 0.5 points from both lines |
| SF8 | a settled round's non-returners | firms not returned by that round's main close | firms not returned by the round's end (after any extension) | same call | standard section 4 (the round's status is set at the main close) and C1: the round-end variant lands the same level in every region |
| SF9 | settled window | frame dates at least 48 months before the extract | 36 to 72 months | same call | C3: every window from 36 to 72 months lands the same level in every region (asserted) |
| SF10 | comparable earlier non-returners | all settled non-returners pooled | by region, by rounds silent, by size band, by region and rounds silent, by call outcome (2022 rounds) | same call | C3: every comparability class lands the same level in every region (asserted) |
| SF11 | duplicate returns | one return per firm | every row | same call | standard section 4 counts firms, and C1: every September cross-mode duplicate is received before the close |
| SF12 | company number | the register's current form | the six-digit core | same call | C1: the invitation list, the panel register's invited and settled-round holders and the closure extract all carry the check-digit form, and an exact join and a core join select the same firms (asserted) |
| SF13 | the extension and the email | red regions get the extension; amber get one email | both for red | same call | standard section 5 |

## Ladder

Rungs in climbing order; each is a complete pipeline a strong analyst can stop at. Rates are per cent of the in-scope
firms, recomputed from the shipped files by `generator/verify.py`; bands R (extension), A (email), G (neither). The settled
corridor is every estimator in the closure table's axes 8, 12 and SF8 to SF10; truth is the simulation's own count.

| Region | R1 register as it stands | R2 call-centre e | R3 last two years | Unobtainable as closed | R4 all earlier rounds | Golden (settled) | Settled corridor | Truth |
|---|---|---|---|---|---|---|---|---|
| Capital | 44.6 R | 45.4 R | 46.6 R | 46.5 R | 47.8 R | 48.7 R | 47.8 to 49.7 | 48.5 R |
| Harbour | 48.6 R | 49.3 R | 50.6 R | 50.7 R | 51.8 R | 52.7 R | 52.2 to 53.7 | 52.7 R |
| North Coast | 56.5 A | 57.2 A | 58.5 G | 58.6 G | 59.7 G | 60.6 G | 60.3 to 61.3 | 62.0 G |
| Islands | 51.4 R | 53.0 R | 53.4 R | 54.3 R | 54.6 R | 55.5 A | 55.4 to 56.4 | 56.5 A |
| Border | 54.6 R | 56.3 A | 56.6 A | 57.1 A | 57.8 A | 58.7 G | 58.5 to 59.5 | 59.3 G |
| Western Uplands | 51.3 R | 52.8 R | 53.3 R | 54.3 R | 54.5 R | 55.4 A | 55.3 to 56.2 | 55.8 A |
| Northern Forests | 56.5 A | 57.6 A | 58.5 G | 58.7 G | 59.7 G | 60.6 G | 60.3 to 61.3 | 61.8 G |
| South Coast | 57.2 A | 58.5 G | 59.2 G | 59.9 G | 60.3 G | 61.2 G | 61.1 to 62.1 | 61.7 G |
| Eastern Lakes | 56.8 A | 57.4 A | 58.7 G | 59.1 G | 59.9 G | 60.8 G | 60.6 to 61.6 | 61.8 G |
| Midlands | 56.3 A | 57.3 A | 58.3 G | 58.7 G | 59.5 G | 60.4 G | 60.2 to 61.2 | 60.4 G |
| River Valley | 57.4 A | 59.0 G | 59.3 G | 60.4 G | 60.5 G | 61.4 G | 61.2 to 62.2 | 63.4 G |
| Southern Plains | 56.8 A | 57.5 A | 58.8 G | 59.3 G | 59.9 G | 60.8 G | 60.6 to 61.6 | 61.8 G |

- **R1, the register as it stands (the default):** five extension, seven email, none neither; ten regions on the wrong
  level. Dies to the standard's scope sentence (section 4.2) and the register's notes (a company appears only once its
  closure is registered).
- **R2, AAPOR's proportional e from the contact centre:** of the September non-returners still out at the close, the call
  records resolve trading firms (refusals, promises) far more often than closed ones, because a ceased report needs
  someone to answer for the firm, so e is close to 1 and the correction small: Capital, Harbour, Islands and Western
  Uplands into the extension, Border and five more onto the email; eight regions wrong. The same levels with staff answers
  counted as trading or with outbound records only (asserted). Dies to the codebook (a ceased report needs an answer) and
  to the settled rounds, whose register-settled share is far above the call outcomes' closed share.
- **R3, the last two years of rounds (share 7.8 per cent):** Capital, Harbour, Islands and Western Uplands into the
  extension, Border onto the email; three wrong. Dies to the register's lag: those rounds' closures are still arriving.
- **Unobtainable as closed:** a heuristic some reach from the codebook; the same levels as R3. Dies to the codebook (an
  unobtainable number is not a ceased report).
- **R4, every earlier round pooled (share 12.1 per cent):** the same levels as R3; three wrong. Dies to the same lag: the
  doubled panel puts the unsettled rounds at close to half the history. The same levels with telephone returns timed at
  the database load (asserted).
- **Golden, the settled rounds (share 15.3 per cent, 7,494 of 48,978 non-returners in 23 rounds):** Capital and Harbour
  extension, Islands and Western Uplands email, the other eight neither.
- **Over-correction (every unresolved non-returner closed):** all twelve green; four regions wrong.
- **Position and dominance:** the default is the most distant answer (ten wrong); every correction walks the rates up and
  every route short of the settled share still sends Islands and Western Uplands into the extension and Border onto the
  email. The decisive move is the last and largest of the history moves (share 12.1 to 15.3 per cent). Separation:
  Islands and Western Uplands sit 0.5 and 0.4 points above 55 under the golden (corridor floor 55.4 and 55.3) and 0.4 and
  0.5 points below under R4; Border sits 0.7 points above 58 under the golden and 0.2 below under R4.
- **Grid:** two binary moves (use history; use only settled rounds) and the call-centre branch give five cells, each a
  named wrong answer above except the golden; partial applications (history without settling, settling without history)
  land R4 and R1 respectively.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | the firms on the September invitation list trading on 1 September; non-returners whose closure the register does not yet show are members whose status is unobserved | filed: standard section 4 (scope sentence, unobserved members stated) |
| 2 Unit of account | the firm (panel ID) | filed: standard section 4 counts firms; C1 for duplicates |
| 3 Attribution window | the September 2026 round's returns received by the main close | filed: standard section 4 and the round calendar |
| 4 As-of dating | the extract at 17:00 on 25 September 2026 | filed: `export_manifest.csv` and the register notes (extract date) |
| 5 Version basis | the register as at the extract for every round | C1: the extract is the only register vintage shipped |
| 6 Denominator | invited firms in scope | filed: standard section 4 |
| 7 Weighting | unweighted firm counts | filed: standard section 4 (a share of firms) |
| 8 Window length | settled rounds, frame dates at least 48 months before the extract | C3: windows from 36 to 72 months land the same levels (asserted) |
| 9 Boundary inclusivity | under 55, 55 to under 58, 58 or over | filed: standard section 5; C1, no region within 0.5 of a line under any settled estimate |
| 10 Rounding path | levels from unrounded rates | C1: no rate within 0.5 of a line |
| 11 Tie-break | none needed | C1: no two regions or estimates tie at a line |
| 12 Maturity and censoring | only rounds the register has settled inform the closure share | the decisive step (HOW); the register notes state that closures are recorded when notified; C3 across settled windows |
| 13 Order of operations | deduplicate, drop recorded closures, estimate the rest, divide | C1: the steps commute on the shipped records; a closure registered on a settled round's close date counts the same either side of the close (asserted) |
| 14 Row order | none | C1: no result depends on file order (asserted over a permutation) |
| 15 Duplicate resolution | one return per firm, the first received | C1: every September cross-mode duplicate is received before the close |
| 16 Identity normalisation | company numbers in the register's current form | C1: every main file carries the check-digit form, and an exact join and a core join select the same firms (asserted); the contractor's six-digit numbers sit only in the call records |
| 17 Netting against gross | not applicable (counts only) | C1 |
| 18 Dimensional units | counts and per cent | C1 |
| 19 Code and status semantics | outcome codes and register routes, read by the dictionary and the codebook | dictionary semantics; never the stump |
| 20 Integerisation | not applicable | C1 |
| 21 Clause scope | the alert levels apply to each region's response rate for the round | filed: standard section 5 |
| 22 Forward window contents | the extension window holds no data; the call is which regions enter it | C1: nothing in the forward window is graded |

## Literal reader

Executed word for word, the prompt and the standard ask for each region's returns by 17:00 on 25 September over the
invited firms trading on 1 September; the register notes say a closure is recorded when it is notified, so the register
as it stands does not settle the status of every non-returner, and the only shipped evidence for the rest is the earlier
rounds whose non-returners the register has since resolved. Every settled-round reading (pooled or by region, rounds
silent, size band or call outcome; windows of 36 to 72 months; status at the main close or at the round's end) lands the same level in
every region, asserted; the routes that land elsewhere each break a quotable sentence (the scope sentence for the register
as it stands, the codebook's ceased and unobtainable definitions for the call-centre e and the unobtainable heuristic) or
the register's own lag for the unsettled rounds. Golden: Capital and Harbour into the extension, Islands and Western
Uplands onto the email, the other eight neither.

## Oracles

None. No control, published figure or reconciliation column ties only under the golden: the published regional
balances (a distractor) carry balances, not response counts; the manifest's row counts tie under every route; no shipped
artifact states a response rate, a closure share or an alert level for the round.

Leak sweep (`leak.py --asof 2026-09-25`, REVIEW, no LEAK), one line per REVIEW:
- Sweep 4, the standard (register, rounds, closure, standard, trading, records): the estimand's own words in sections 2 to
  4; no sentence names settled rounds, a closure share, a lag or a window.
- Sweep 4, the register's notes (register, closure, trading, records, extract): the register's own process, stating that
  an unregistered closure is not in the extract (`determinism-check` section 1) and never how many or which.
- Sweep 6, the published June balances (a distractor) and the invitation list name the regions beside numbers: net
  balances and panel attributes, neither a response rate nor an alert level; no file ranks the regions on the call.
- Sweep 9, the round calendar's dates after 25 September (the extension window, the cut-off and publication dates, the
  December round marked planned): a forward calendar, the allow-listed file in `checks.py` RS4.

Duplicate guard: `guard.py heart` WARN (Gate G label against task229, question form which against task188, both
answered at the draw; task445 differentiated on the card); `guard.py surface` promotes task230 (back to back: the time
and population gap and the designation-set decision) and task447 (both file a standard). Neither shares the decisive
move: task230's detection rate falls as targets grow rarer in a shared pool, task447's redirection share resets with
payer terms, task231's register records exits late so the closed share of silent firms comes from settled rounds; clean,
shares components by design.

## Ask sheet

Three asks, 66 figures, each decoupled from the call (none uses the eligibility estimate, the settled rounds or the
alert lines) and each moved by silent primaries on rows outside the main population. Stops and misses are recomputed
from the shipped files by `generator/verify.py` and asserted in `generator/checks.py`.

**Main population (zero device rows, asserted):** the September 2026 invitation list, its receipts file (true reach times;
the 17 firms that returned twice did so before the close), the register's closure records for those firms (check-digit
form), and the outcome rows of the settled rounds (March 2017 to September 2022: true reach times, recorded at receipt,
one holder per panel ID) with their firms' closure records.

| Ask | Figures | H18 home | Use | Primary devices (family) | Hazards | Path (files, columns) | Stops (natural read, half-handled, over-corrected, answer) |
|---|---|---|---|---|---|---|---|
| A: the contact centre in the September round, by region | firms reached so far (12), calls placed (12) | a qualifier of the call: the extension's calls are the contact centre's, and what it has already done per region | sizing the extension's call lists | D1: the contractor's records for 22 September were loaded a second time on 23 September under fresh record numbers, every other field identical, beside genuine same-day retries by the dialler; D5: calls firms make to the bank's inbound desk sit in the same log (direction in), so calls placed counts outbound calls only while a firm reached on its own callback counts as reached | transfers to a supervisor (code 71, the call continues in the supervisor's record); the contractor's numeric codes; the contractor's company numbers in two forms and its pre-2023 region codes; staff answers count as reached | call records (team, direction, panel ID, company number, region, agent, start, duration, outcome), outcome codes (two schemes, reached), invitation list, region review, dictionary: 5 files, 14 columns | calls: every record 12/12 high, every outbound record 12/12 high, reload dropped but legs kept 10/12 high, one call per firm a day 12/12 low; reached: outbound records only 12/12 low, respondent codes only 12/12 low, the bank's own records only 12/12 low; the answer |
| B: the June 2026 round's late returns, by region | returns that reached the bank after the June main close (12), their share of the region's June returns to one decimal (12) | a qualifier: what arrives after the close without an extension | judging the extension against the late returns a round gets anyway | D8: since 9 April 2024 the survey database loads telephone returns in an overnight transfer, so an interview finished on the close day carries a load time after the close; the interview end is in the call records (COMP, 10) | `recorded_at` (bureau keying since February 2023) one word from `received_at`; UTC timestamps against the 17:00 local close | round outcomes (round, panel ID, region, mode, received_at, recorded_at), call records (direction, panel ID, company number, start, duration, outcome), calendar (June close), standard section 4.3, dictionary: 5 files, 12 columns | received_at as loaded 12/12 high; recorded_at 12/12 high; the answer |
| C: the March 2026 refreshment, by industry group | firms recruited (9), of them firms that have returned at least once (9) | an audit trail of the invited population the call is computed on | checking the refreshment's take-up | D7: panel IDs freed in the 2024 expansion block were issued again to March 2026 recruits, so the outcomes file holds the earlier holder's rounds under the same ID; D1: the contractor signed some firms up twice, and the second record kept a six-digit company number and was cancelled as a withdrawal before the first round, beside genuine withdrawals before the first round; D4: September's returns sit in the receipts file, not the outcomes file | NACE Rev. 2.1 sections on recruits from 2025 (crosswalk in the dictionary) | panel register (ID, company number, NACE section, recruited, wave, left), dictionary crosswalk, round outcomes (round, panel ID, mode), September receipts, calendar: 5 files, 11 columns | recruited: register rows 5/9 high, dropping every early withdrawal 8/9 low, invitation lists 8/9 low, Rev. 2.1 letters read as groups 6/9; returned: any return under the ID 8/9 high, outcomes file only 9/9 low; the answer |

- **Span:** ten files and 37 column uses across the asks (the per-ask lists above); no two asks share a primary device or
  a path.
- **Shared hazards:** company-number forms move A (the contractor's records) and C (the duplicate recruitment records);
  the region review moves A only; UTC against the local close is texture on B and A.
- **Realism:** each device is a record the bank's systems make (a contractor re-sending a day after a fault, a database
  stamping overnight loads, an identifier allocator recycling numbers, a recruitment form keyed twice); none needs a task
  to exist.
- **Referee:** none needed; no ask turns on a designed disagreement.

| Ask figure | Where the cracker's path goes | Mirror (stops at R2) | Cracker (lands the call, runs the battery) |
|---|---|---|---|
| A firms reached (12) | filters the round's outbound calls for calls placed and counts reached firms on the same records, missing firms reached only on their own callback | misses the same way | miss |
| A calls placed (12) | the exact-duplicate check passes the reloaded records (fresh record numbers) | misses the same way | miss |
| B late returns (12) | takes `received_at` for telephone returns, the overnight load | misses the same way | miss |
| B late share (12) | follows the late count | misses the same way | miss |
| C recruited (9) | counts the register's 2026 refreshment rows, or drops every withdrawal before the first round | misses the same way | miss |
| C returned at least once (9) | counts any return under the recruit's panel ID, the earlier holder's included | misses the same way | miss |

- **Cracker keeps:** about 0.15 of the ask weight (a cracker that catches the reload, the callbacks or the reissued IDs
  keeps those cells; no single habit keeps a whole ask).
- Mirror leakage: 15 per cent of ask weight (the mirror's ask path is the cracker's; the asks do not touch the call's
  construction).
- Pair ceiling: 36.8 (C = 38 + 7 + 55 x 0.15 = 53.3; S = 5 + 7 + 55 x 0.15 = 20.3; mean 36.8).

## Pre-ship check

1. Domain: survey nonresponse's estimate of the eligibility of unresolved non-respondents (AAPOR's e for
   unknown-eligibility cases), taken from the register's settled closures because follow-up resolves closed firms far
   less often than trading ones; with a meter fleet's read rate in its place there is no in-scope population fixed by
   trading status at a frame date and no e to estimate.
2. Real work, nothing planted: the register's late recording, the contact centre's two teams and the contractor's
   reload, the inbound desk, overnight loads and bureau keying, reissued identifiers, a recruitment record keyed twice,
   NACE Rev. 2.1; each is a record the bank's or the register's systems produce, and none sits on the call's rows.
3. The step that flips the call is methodological: the closure share of this round's silent firms read from rounds the
   register has caught up with, not from the register as it stands, the call outcomes, or rounds still settling.
4. Analyst test: the default path (deduplicate, drop recorded closures, divide) files five extension regions and seven
   email regions; the call-centre e, every earlier round and the last two years each file four extension regions
   (asserted on the clean truth, `checks.py` R3a and R3b).
5. Standard section 4 defines the estimand (firms invited and trading on the frame date, whether or not the register yet
   records a closure); the design forces the method, and every settled estimator lands the same levels (corridor
   asserted, tightest margin 0.29 points).
6. No decoy: no memo, dashboard or prior list carries a region set; the published June balances rank nothing on the call.
7. Nothing is recovered from certified figures: the settled rounds are evidence for an estimate, not controls to match.
8. The lesson (a response rate's denominator is fixed at a date, so the eligibility of silent units comes from cases whose
   fate has since become known) is on no other card: nearest drivers 0.08.

## Tried and rejected

- Seed pitfall kept (Rubin's rules over shipped implicates): a reflex for any strong solver once the implicates ship;
  rejected at the draw.
- GSD missing-data framing (meter reads imputed in a utility network): the deciding quantity reads the same in any
  field, the backdrop the author keeps getting returned; rejected at the draw.
- Product analytics SRM alert, psychometric reliability under a population change, consensual observer drift, SSI
  post-discharge ascertainment, AMR cascade testing, airport noise-monitor capture: each either read as a reflex (ramp
  SRM, a pilot alpha), split into competing defensible methods (CTT against IRT, drift indices), sat in a pairing the
  wave's epidemiology seeds need, or turned on a fleet mix (composition, banned in the window); rejected at the draw.
- Silence run as the decisive rung (closure share by rounds since the last return): prototype 2026-10-13 put the
  pooled and run-based estimates within 0.3 points of each other; the run is a corridor variant, not a rung.
- An insolvency wave to make the run decisive: the settled history stops transporting to the wave regions (the
  estimate misses the truth by about 5 points there); rejected.
- Per-region response rates as graded figures: the reasonable settled-round estimators (pooled, by region, by rounds
  silent, by size) differ by up to 1.4 points in a region because a region's closure share among non-returners falls as
  its response rate falls; graded at whole per cent they would split rigorous solvers. The graded figure became the
  standard's alert level, which every settled estimator lands identically (2026-10-13).
- Register lags of 900 days and a five-year settled window, to make pooling all history a rung on the call: the
  settled-estimator corridor widened to 1.8 points (Islands) without moving the all-history route off the extension list;
  reverted to the 780-day liquidation route and a four-year window (2026-10-13).
- Reminder calls on the simulation's calendar days 15 to 20, weekends included: moved to working days from day 15 to the
  close, which reshuffles every region's draws; propensities recentred and stream offsets re-searched (2026-10-13).
- An all-history route one region off the call (Border only): the re-search found offsets where every route short of the
  settled share also sends Islands and Western Uplands into the extension; adopted (2026-10-13).
- Enterprise-group calls logged once under the group's lead firm, as the firms-reached device: the group's firms carry
  independent call outcomes in every other round, so the convention contradicts the history; replaced by calls firms make
  to the inbound desk (2026-10-13).
- The codebook's definition of reached as the only device on firms reached: a careful solver executes it; the inbound
  desk's callbacks added (2026-10-13).
- Panel IDs reissued from any freed identifier: earlier holders sit in the settled rounds, so a join through the register
  would mislink the main population; reissue limited to the 2024 expansion block, freed before July 2025 (2026-10-13).
- Contractor-style six-digit company numbers in the main files: an exact join would miss those firms' closures silently
  and move the call; the main files carry the check-digit form only, the six-digit form stays in the contractor's call
  records and the cancelled duplicate recruitment records (2026-10-13).
- A main close on Christmas Day 2020 and 2026 and on Christmas Eve 2021 (the Friday on or before the 25th taken
  literally), found by the leak reader: the December close moves to 23 December when that Friday is the 24th or 25th, and
  the post room keeps the Christmas and New Year holidays; the settled share moves from 15.32 to 15.30 per cent and no
  level or margin moves (2026-10-13).
