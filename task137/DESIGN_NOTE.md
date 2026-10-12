# task137: Kaimai Building Society, the agent-hours to book with Harbourline for the January to March 2027 term deposit maturity calls (architecture 1)

Private, never ships. A new build (wave 2), numbered from seed FC08: the seed's world, decision and quantity are kept (a
deposit-taker's maturity calls made by an outsourced contact centre booked in agent-hours, take-or-pay, a quarter ahead,
on a list fixed at the booking deadline); its architecture (dialling rules withheld from the contract and recovered from
the vendor's acknowledgements, with the callable-number count as the decisive unit) is not used. The dialling rules are
filed and the callable-number wash is depth; the pitfall is re-found from how the deposits on the list reprice.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task137.json`, architecture v1, registered 2026-10-12; `guard.py check` WARN on one finding (`repeat.gate_g`, answered below); `guard.py validate` clean |
| Domain / task type | banking-credit-financial-risk / deposit-liquidity-behaviour (a client domain): how term deposit holders behave at maturity when their deposit reprices onto the posted card is the deciding quantity |
| Objective | Forecasting & Predictive Modeling: the agent-hours the January to March 2027 list will use, a campaign not yet begun, forecast from the seven closed campaigns |
| Shape | other: the call and its components (the hours, the hours for each maturity month), the note's opening and chart, and two asks on rows the call never reads (14 and 6 figures); about 30 criteria, arithmetic in `## Ask sheet` |
| Decision | `quantity_figure`, answer unit `count` (agent-hours, to the nearest 250) |
| Mechanism | gap time (decisive: the evidence is about past repricings on past cards, the bet is on a list repricing onto a much lower card), then population; pattern E (a conditioned yield, no column naming the conditioning quantity); generators G14 (the share of conversations that go to the retention offer, conditioned on the drop from the locked rate to the card) then G6 (the coming list's mix on that drop sits far from every past list's within each term: its four-year deposits meet a 2.50-point drop, every past four-year deposit met a negative or small one); Gate G `forecasting`; strategy `composition_mix` |
| Layer 2 family / pattern | `field_method` (deposit behaviour's repricing-gap retention model); `own:repricing-gap-conditioned-retention-at-maturity` (banking has no library patterns; the family is the client's "the field's own method done right") |
| Furniture | forum `line_manager_or_team` (the head of deposits signs the block order), forcing event `purchase_order_or_contract` (the quarterly take-or-pay block order is due on Friday 20 November 2026), organisation family `cooperative_or_member_body` (a building society), role family `product_manager` (the term deposits product manager owns the campaign budget), context artifact `planning_thread` (Harbourline's request for the block order and the society's reply), calibration `none` (the past campaigns are the history the yields are estimated from, not an organ), opening `question-first`, question form `how-many` |
| Spine | `harbourline_dial_log_2025q1-2026q3.csv`, the contact centre's dial records: one row per dial on a released case, December 2024 to September 2026 (264,592 rows); constructed |
| Deliverables | `td_booking_q1_2027.xlsx` (the booking by maturity month with its basis, the two asks, a notes sheet), `td_booking_note_q1_2027.docx` (a one-page note for the head of deposits opening with the block and charting it by maturity month) |
| People | drawn with `guard.py names --geo "New Zealand" --seed 137 --n 30`, keeping only names the guard clears: Hazel Johnstone (term deposits product manager, the requester), Stuart Waller (head of deposits, signs the block order), Suzanne Wallis (Harbourline account manager), Joseph Herd (customer data steward, keeps the do-not-call register), Sienna Stewart (treasury pricing analyst, prepares the quarterly card for ALCO), Ashton Findlay (Harbourline workforce planner); none appears in the prompt |

**Guard.** `guard.py check` on the scratch card: WARN, one finding. `repeat.gate_g` (`forecasting` in one of the last two
builds, task130): the key is honest, because the decisive step is how the forward share of long conversations is
forecast, conditioned on each deposit's repricing gap, and task130's mechanism (a claims-made window costed by report
lag) shares nothing with it. Bans run against the last three builds and the builds live beside this one (task128,
task136): a first draft blocked on `ban.org_family` (`financial_institution`, task128) and `ban.artifact`
(`operations_log`, task128; then `register`, task130), so the world moved to a building society and the context
artifact to the planning thread that frames the booking. A first gap draft (population, E) blocked on `test.same_driver`
against task124's lineage and on `test.same_puzzle_older`; gap time is the honest decisive gap (the stumping skill's
"a lapsing term": the quantity moves with where on the rate path each deposit locked and where it matures), and the
four older carriers of time, E and a quantity are differentiated on the card.

**Same-puzzle and same-driver tests.** Gap time, pattern E, decision `quantity_figure`, Gate G `forecasting`: no build in
the last twelve carries the four (task125 carries gap time with a composition mix on a G6 pattern; task130 gap time with
pattern none). Older carriers: task117 (draw caps of another entity through a dated join, follow-on operations re-timed
behind the one ahead), task37 v2 (a coupling to a linked entity's authorisation recovered from a closed roll), task44 v2
(a pilot's pooled gain mixing opposite effects split by a moderator), task97 v5 (the cumulative history of the place a
unit occupies). None conditions a share on the unit's own price change at a repricing; the card carries the four lines.

**Abstraction test.** Stripped of nouns, the driver is: a unit's chance of needing the long, costly form of a service at
a one-off repricing is set by the gap between the price it locked in and the schedule it rolls onto; the share is
stable across past rounds only per unit of that gap, and the coming round's dominant cohort meets a gap no past unit of
its own class met. The three nearest drivers (`guard.py nearest`: task97 v5 0.06, the place's cumulative history;
task254 v2 0.05, a cut of a time-to-event distribution seen only through events already happened; task98 v3 0.05, a
per-unit threshold on groups formed by chaining) share no latent structure, default path or correction with it.
task136, drawn beside this one, carries a campaign's yield to new sites per member still able to respond (a
denominator); here the population is fixed and nobody's eligibility moves, the share of the conversations that go
long is conditioned on a price change, and no denominator is rebuilt.

**Data-native sentence.** The society's term deposits reprice only at maturity, onto the posted card for their term,
so each holder Harbourline reaches meets in one step the whole gap between the rate they locked in and the card they
will roll onto, and that gap decides whether the conversation goes to the 22-minute retention offer; the seven past
campaigns met their gaps as the rate cycle turned (four-year deposits locked in the 2021 and 2022 lows met higher or
similar cards), while January to March 2027 brings 10,735 four-year deposits locked at the 2023 special's 5.65 per cent
onto a 3.15 per cent four-year card, a 2.50-point drop.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting` (47 builds): hazards by time since entry
(134), selection on the outcome (124), the maturity of a claims window (130), a recycling term and a deadline-driven
draw (501), corpus-recovered conversion rates (27, 29, 30, 78), censored delays (31, 99), a slowest sub-unit (52), a
two-class mix recovered by differencing dated events (95), a campaign's yield carried per untapped member (136): none
conditions a behavioural share on the unit's own repricing gap. `stumping/references/client/two-layer-task-design.md`:
banking has no library patterns, so the pitfall comes from the `field_method` family (the field's own method done
right), here deposit behaviour's retention-at-maturity model on the repricing gap. `stumping/references/client/
measured-drivers.md`: the held tasks are a construction outside the solver's hypothesis space, upstream of every graded
figure; the drop is built across two files (the list's locked rate and the card in each quarter's campaign brief) that
no reflex joins. `guide-to-prompt/references/exemplars.md`: the 0.20 to 0.40 band misses on a window, a lag or a base;
this build's miss is the base the share is carried on. The seed's header (FC08) for the world only.

**World.** Kaimai Building Society is a mutual deposit-taker headquartered in Tauranga, most of its funding on term
deposit (one- to five-year terms). At maturity a term deposit reinvests for the same term at the posted rate in force on
its maturity date unless the holder has given other instructions (the Term Deposit Terms, clause 9.2, cited in
procedure 5.1). The society's Asset and Liability Committee sets the posted card each quarter, effective on the first
day of the quarter, and runs short new-money specials beside it (the four-year special at 5.65 per cent in January to
March 2023, the three-year special at 5.95 per cent in July to September 2023, the two-year special at 6.20 per cent in
October to December 2023, the one-year special at 6.35 per cent in April to June 2024); no shipped file names the
specials, which are visible only as locked rates on the lists. Since January 2025 Harbourline Contact Services, a
Palmerston North contact centre, has made the society's maturity calls under a statement of work (HCS-KBS-2025-01):
each quarter the society lists the term deposits of NZ$25,000 or more maturing in it with no maturity instruction on
file at the list cut, releases each to Harbourline 21 days before its maturity date unless the holder has instructed in
the meantime, and Harbourline works the case under the SOW's dialling rules until a conversation with the holder,
exhaustion of every callable number, withdrawal or maturity. Harbourline bills agent time at fixed minutes per event
(1.5 for each dial that does not reach the holder, 8 for each conversation, 22 for each conversation that goes to the
retention offer because the holder says they mean to withdraw or move the funds) against a quarterly take-or-pay block
the society books, in multiples of 250 hours, by the 20th of the second month before the quarter; hours beyond the
block are billed at the block rate plus 35 per cent. The retention procedure (version 4) books the hours the quarter's
list is forecast to need, to the nearest 250, drawing on every campaign closed under the SOW.

As-of dates: the January to March 2027 list was cut on 2 November 2026 (18,400 term deposits, 10,735 of them four-year
deposits at 5.65 per cent); ALCO approved the January to March 2027 card (four years 3.15 per cent) and it sits in the
draft campaign brief issued 3 November 2026; Harbourline's last close-out (July to September 2026) arrived on
21 October 2026; the request is made on 4 November 2026; the block order is due on Friday 20 November 2026.

## Default path

1. Read the SOW (the minutes billed per event, the dialling rules, the take-or-pay block in multiples of 250) and the
   retention procedure (the list, the release 21 days before maturity unless the holder has instructed, no release
   without a callable number, the booking of the hours the list is forecast to need from every closed campaign).
2. Take the 18,400 deposits on the January to March 2027 list, normalise their holders' phone numbers and wash them
   against the do-not-call register: each case's callable numbers by type (mobile, home, work), and the 460 cases left
   with none.
3. From the seven closed campaigns (the release log, the dial log and the close-outs), price dialling per mix of
   callable number types: the dials that do not reach the holder and the chance of a conversation per released case,
   and the 95.5 per cent of listed deposits with a callable number that reach release.
4. Take the share of the past conversations that went to the retention offer (pooled over the seven campaigns, 33 per
   cent; the latest campaign's, 35; or each term's own, four per cent for four-year deposits) and price each expected
   conversation at 8 minutes plus 14 times that share.
5. Sum over the list and round to the nearest 250.

Ends on: about 4,500 agent-hours (4,611.1 with the pooled share; 4,000 by term, 4,750 with the latest campaign's share;
5,000 with the share read off each deposit's own locked rate; 4,750 with the latest campaign's hours per listed
deposit).
Golden: 5,500 agent-hours (5,568.0: the share of conversations that go to the retention offer conditioned on each
deposit's drop from its locked rate to the January to March 2027 card for its term).

## Stump sentence

A competent solver washes the numbers against the do-not-call register, prices dialling per mix of callable numbers
from the seven closed campaigns, carries the past share of conversations that went to the retention offer (pooled, the
latest campaign's or each term's) and books about 4,500 agent-hours (Ends on); the step that lands it there is not
conditioning that share on each deposit's drop from its locked rate to the card it reinvests at, which leaves the
10,735 four-year deposits locked at 5.65 per cent, meeting a 2.50-point drop where 92 per cent of past conversations
went to the retention offer, at the share of deposits that met smaller drops: the golden is 5,500.

## Three rules

- **Domain test:** the deciding quantity is the share of maturing term deposits whose holders, once reached, will want
  to move their money, which deposit-behaviour analysis models on the repricing gap between each deposit's locked rate
  and the posted rate it reinvests at on maturity; with another field's nouns there is no fixed-term repricing, posted
  card, rate cycle or locked rate for the share to hang on, so the task stops making sense.
- **Analyst test:** a strong analyst who reads the SOW's billing and dialling rules and the procedure right, washes
  every number against the do-not-call register, prices dialling per mix of callable numbers and scales by the
  released share still carries the past campaigns' retention-offer share (pooled, the latest campaign's, trended, by
  term, by term from the latest campaign or by the deposit's locked rate) and books 4,000 to 5,000 agent-hours, 10 to
  28 per cent short.
- **Layer 1:** realistic mess across the pack, none of it deciding the call: past lists in two extract layouts (rate in
  per cent with dashed account numbers and comma-grouped principal through 2025, a decimal rate and unpunctuated
  account numbers after the January 2026 core banking upgrade); the dial log in UTC with the contact centre's own
  disposition codes and case reference format; release files listing each case's callable numbers by type; phone
  numbers in mixed New Zealand formats normalised before the do-not-call wash; a register with recorded and withdrawn
  dates; the posted card inside each quarter's campaign brief (PDF tables whose layout changes in 2026); the ask paths'
  own mess (an account event extract where a change of term at maturity opens a new account funded by transfer, a core
  holdings view listing joint deposits under each holder beside a frozen legacy certificate register and its migration
  batches).
- **Layer 2:** the field's method for retention at maturity: the shortcut a capable analyst takes is the share of
  conversations that went to the retention offer carried pooled, from the latest campaign, trended or by term; an
  expert in deposit behaviour rejects it because the share is a function of the repricing gap, which the coming list
  carries far from every past list's mix within each term; conditioning on the gap is the only method consistent with
  all seven closed campaigns (the share rises with the drop inside every campaign and every term, asserted).
- **Stump class:** analytical. The decisive step is choosing what the forward share is conditioned on; no plant, no
  field read and no filed rule decides, and every rule in the pack (the billing minutes, the dialling rules, the
  release, the do-not-call wash, the reinvestment default, the booking) is executed the same way on the default path
  and the golden.

## Readability screen

Rungs as climbed (Ladder). The six tests: 1 a filed sentence names the decisive quantity or sends the solver looking;
2 a column, key or marker makes it a predicate or a header-found join; 3 an opponent reflex; 4 a control or corpus
scores the bases or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or half of a
reported figure.

| Rung (the step that refuses the rung below) | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R1: price dialling per mix of callable numbers from the release log and dial log, with the release share (refuses rung 0's hours per listed deposit of the latest campaign) | the SOW's dialling rules name callable numbers and the six-dial limit | the release log lists each case's callable numbers and types | stratifying by a visible attribute is a reflex | none | no | a group-by and a weighted sum | readable |
| R2: the retention-offer share by term, from the latest campaign (whole or by term), trended, or read off each deposit's own locked rate (refuses the pooled share) | no | term and rate are columns of every list | a reflex (pool, recency, trend, visible strata) | none | no | a group-by | readable |
| R3 (decisive): the share conditioned on each deposit's drop from its locked rate to the card for its term in force on its maturity date, the coming list's drops read against the January to March 2027 card | no sentence names the drop, the card as a driver of anything but the reinvestment rate, or a link between rates and the retention offer; the Terms say what a deposit reinvests at, the same on both paths, and the SOW defines the retention conversation by what the holder says | no column holds a drop: the locked rate is on each list, the card is a table inside each quarter's campaign brief (a PDF), joined by term and maturity quarter | not an opponent default (its reflexes pool, take the latest, trend, stratify by term or use the deposit's own rate, and each lands 10 to 28 per cent short) | no control scores the bases: no published share by drop, the treasury outlook's rollover assumption is on balances and flat, and the close-outs tie under every basis | the battery never touches it | a conditioned share across a covariate built from two files, not one ratio | silent |

The screen holds on R3 because the only sentences about rates are what a deposit reinvests at (procedure 5.1, read the
same on every path) and what the agent quotes; the pitfall is the field's own: deposit behaviour models run-off at
maturity on the repricing gap, and a generalist carries the observed share.

## Semantic fork table

One row per term in the main ask and per convention the main computation needs. The stump (what the share is
conditioned on) is not a reading and has no row: every route computes the same literal estimand, the hours the list
will use under the SOW, and only the data's structure separates them (Literal reader). Every row is asserted in
`generator/checks.py`.

| SF | Term or convention | Golden reading | Alternative and the call under it | Ruled out by |
|---|---|---|---|---|
| SF1 | agent-hours | the minutes the SOW bills per event, over 60 | logged agent time on shift | SOW schedule 2.1 (agent time is billed per event at the stated minutes); no shift or roster data ships |
| SF2 | book | the hours the quarter's list is forecast to need (the expected hours), to the nearest 250 | a smaller block that minimises expected cost under take-or-pay with the 35 per cent overage | procedure 6.1 (the society books the hours the list is forecast to need, rounded to the nearest 250 hours); SOW 2.2 (multiples of 250) |
| SF3 | the 18,400 deposits on the list | each listed deposit a case, one per holder | a holder's other deposits as extra cases | procedure 3.3 (one deposit per member, the others covered in the same conversation); asserted that no holder has two listed deposits |
| SF4 | deposits maturing in each of the three months | the calendar month of the contractual maturity date | the month in which the dialling falls | the prompt's own words; every deposit's hours go to its maturity month |
| SF5 | callable number | a number held at the cut and not on the do-not-call register at the cut | a number registered after the cut | both extracts are dated the cut and no register entry, withdrawal or contact point is dated after it (C1, asserted) |
| SF6 | the rate a deposit reinvests at | the card for its term in force on its maturity date, as the quarter's campaign brief carries it | the card in force at release | procedure 5.1 and the brief's section 3 (rates for deposits maturing this quarter); every listed deposit matures in January to March 2027, so one card applies (C1, asserted) |
| SF7 | which closed campaigns | all seven | the latest four, 2025 only or 2026 only | procedure 6.1 (the forecast draws on every campaign closed under the statement of work); each subset files the same bins anyway (C3, asserted) |
| SF8 | the share's estimator | the share of past conversations in the same 0.25-point band of drop | bands of 0.2, 0.25 or 0.5 points at any offset, a band by term, a logistic fit in the drop with or without term, an isotonic fit | C3, asserted: every member files the same booking and months; a linear probability fit is refused (its fitted share falls below zero at the past's negative drops, where 9,000-odd conversations ran at 0.1 per cent, and misses the 2.5-point band by more than 20 points) |
| SF9 | dialling estimator | per mix of callable number types | per ordered configuration, per count only, or a per-number fit of the dialling rules with withdrawals | C3, asserted |
| SF10 | a deposit with no callable number | not released, no hours | released and closed at once | procedure 4.3; the same zero |
| SF11 | deposits instructed before release | the past share of listed deposits with a callable number kept from release by the holder's instruction | every deposit with a callable number released | procedure 4.2 (no release once the holder has instructed); the release log's reasons; released without it, the hours land a bin high (asserted) |
| SF12 | withdrawals and maturity in the dialling window | inside the per-mix yields (past cases closed by withdrawal) | modelled apart | the per-number model with a withdrawal rate files the same bins (C3, asserted) |
| SF13 | rounding | the unrounded total once to the nearest 250; each month from its own unrounded hours | months rounded and summed | the prompt and procedure 6.1; the rounded months add to the rounded booking, and every graded figure sits at least 25 hours from an edge (asserted) |
| SF14 | the retention conversation | dispositions RTK and RTW, billed at 22 minutes | any conversation that mentions rates | SOW schedule 3 (codes) and schedule 2 (minutes) |
| SF15 | a dial that does not reach the holder | NOA, BSY, VML, DIS and WNG, at 1.5 minutes | wrong party as a conversation | SOW schedule 2 and 3 |
| SF16 | the dialling calendar | no listed deposit has fewer dialling days between release and maturity than the six dials per number need | maturity truncating dials | C1, asserted over every maturity date with Harbourline's close-down and public holidays |
| SF17 | a deposit's term | the list's term | term from the start and maturity dates | the same on every row (C1, asserted) |

## Ladder

Measured on the built pack (`generator/checks.py` asserts every rung and rival at least 8 per cent under the golden and
off every graded bin).

| Rung | Construction | Hours | Off the golden | Booked |
|---|---|---|---|---|
| R0 | the latest campaign's billed minutes per listed deposit times 18,400 | 4,674.3 | minus 16 per cent | 4,750 |
| R1 | dialling per mix of callable numbers and the release share, the pooled retention share (33 per cent) | 4,611.1 | minus 17 per cent | 4,500 (months 1,250, 1,750, 1,750) |
| R2a | R1 with the latest campaign's share (35 per cent) | 4,693.7 | minus 16 per cent | 4,750 |
| R2b | R1 with each term's own share (four years: 4 per cent) | 3,996.9 | minus 28 per cent | 4,000 |
| R2b' | R1 with each term's share from the latest campaign, or each term's trend | 4,240.1, 4,165.3 | minus 24, minus 25 per cent | 4,250 |
| R2c | R1 with the share read off each deposit's locked rate (0.25-point bands; 5.50 to 5.75 ran at 69 per cent on a mean drop of 1.97) | 4,987.3 | minus 10 per cent | 5,000 (months 1,250, 1,750, 1,750) |
| R2c' | R1 with the share by locked rate within term | 4,528.9 | minus 19 per cent | 4,500 |
| R2d | R1 with the campaigns' trend in the share | 4,856.4 | minus 13 per cent | 4,750 |
| R3 (golden) | R1 with the share conditioned on the drop | 5,568.0 (months 1,479.5, 2,044.1, 2,044.4) | | 5,500 (months 1,500, 2,000, 2,000) |

- **Rung 0 (default):** the latest campaign's hours per listed deposit. Dies to the release log: the coming list's
  holders carry another mix of callable numbers and the deposits' terms and rates differ, so neither the dialling nor
  the share transfers.
- **Rung 1 (the obvious correction):** dialling priced per mix of callable numbers with the release share, the pooled
  share of conversations that went to the retention offer. Dies to the seven campaigns: their shares run from 18 to 37
  per cent and no visible stratum makes them agree.
- **Rung 2 (the sophisticated wrong ones):** the share per term (four-year deposits ran at 4 per cent, every one locked
  in the 2021 and 2022 lows and rolling onto a higher or similar card), the latest campaign's, a trend, or the share read
  off each deposit's locked rate (past deposits locked at 5.50 to 5.75 were mostly two-year deposits meeting a drop near
  two points, 69 per cent). Each dies to the drop: within every term and every locked-rate band, the past shares sort
  by the gap to the card the deposit met.
- **Rung 3 (decisive):** the share conditioned on the drop, read against the January to March 2027 card: the four-year
  deposits' 2.50-point drop gives 92 per cent of their conversations to the retention offer.
- **Margins and flip:** the nearest wrong rung (R2c) sits 10.4 per cent under the golden and a bin below on the
  booking and on every month; the others 13 to 28 per cent. The golden would fall a bin only if the four-year deposits'
  share were under 0.82 (against 0.92), a level past conversations met at a drop near 2.2 points.
- **Position and dominance:** every rung below R3 lands under the golden; over R1's pooled 33 per cent, R2a to R2d
  move the list's forward share by at most 12 points (R2c to 44 per cent; R2b lowers it to 14), R3 by 29 (to 62); no
  correction short of R3 reaches the golden's bins, and no two of them combine to it: the nearest, the locked-rate
  share, carries the four-year deposits at 69 per cent against the drop's 92.
- **Grid:** dialling estimator (4) by share basis (pooled, latest, term, latest by term, term trend, locked rate,
  locked by term, trend, drop) by release share (with, without): every cell without the drop lands at least 10 per cent
  under the golden; every drop cell with the release share lands in the golden's bins (32 members, C3); the drop without
  the release share lands 4.8 per cent over and a bin high (a second error, refused by procedure 4.2).
- **Worth, on the graded figures:** the booking and all three monthly figures move with R3 (each month carries
  four-year deposits at 5.65 per cent); no rung below it files any of the four.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the 18,400 deposits on the January to March 2027 list as cut on 2 November 2026; no deposit joins after the cut | procedure 3.1 and 3.3; the list file |
| 2 | Unit of account | one case per listed deposit, one per holder; hours are billed minutes over 60 | SF1, SF3 |
| 3 | Attribution window | every dial on a listed deposit belongs to the list, whatever month it falls in | SF4 |
| 4 | As-of dating | list, contact points and register at 2 November 2026; the card for January to March 2027 maturities in the draft brief | the extract names, the brief |
| 5 | Version basis | one close-out per closed campaign; one register edition; one brief per quarter | one edition ships of each |
| 6 | Denominator | the retention share is per conversation, not per case or per dial | SOW schedule 2 bills per conversation |
| 7 | Weighting | yields weighted by the coming list's mixes; the share applied deposit by deposit | SF8, SF9 |
| 8 | Window length | the seven closed campaigns | SF7 (procedure 6.1, and C3) |
| 9 | Boundary inclusivity | drop bands; the NZ$25,000 listing threshold is the society's, already applied | SF8 (C3); procedure 3.1 |
| 10 | Rounding path | once, at the end, for the booking and each month, to the nearest 250 | SF13, asserted |
| 11 | Tie-break | none arises | a sum |
| 12 | Maturity and censoring | only closed campaigns: every released case carries a close-out | asserted |
| 13 | Order of operations | wash, mix, release share, yields, share, sum | each step commutes with the others except the wash, which precedes the mix |
| 14 | Row order | no step depends on it | sums and group-bys |
| 15 | Duplicate resolution | one release-log row per listed deposit, one close-out per released case, one row per dial | asserted in checks |
| 16 | Identity normalisation | account numbers dashed in 2025, unpunctuated from 2026; phone numbers in local and E.164 forms | the extract notes; normalised joins asserted complete |
| 17 | Netting against gross | none | does not arise |
| 18 | Dimensional units | rates in per cent on the 2025 lists, decimals from 2026; minutes against hours | the list headers and extract notes; SOW schedule 2 |
| 19 | Code and status semantics | disposition codes; release-log reasons | SOW schedule 3; the extract notes |
| 20 | Integerisation | none (expected hours) | does not arise |
| 21 | Clause scope | one SOW and one billing schedule for every campaign since January 2025 | SOW clause 1.1 |
| 22 | Forward window contents | the coming list, its holders' numbers, the register and the card are all filed; no dial on it exists yet | the extracts and the brief |

## Literal reader

Executed word for word on the built pack: the prompt asks how many agent-hours to book for the 18,400 deposits on the
January to March 2027 list; the procedure books the hours the list is forecast to need, to the nearest 250, drawing on
every campaign closed under the SOW (6.1), releases each deposit 21 days before maturity unless the holder has
instructed or no number is callable (4.2, 4.3), and the SOW bills each dial and conversation at fixed minutes
(schedules 2 and 3) under the dialling rules (schedule 1). The forecast needs, per deposit, the expected dials that do
not reach the holder, the chance of a conversation and the chance that a conversation goes to the retention offer; the
first two come from the closed campaigns per mix of callable numbers, the third from the closed campaigns'
conversations. Every reading of every term is a row of the fork table and lands on the golden or is refused by a quoted
sentence; every estimator in the corridor files 5,500 (1,500, 2,000, 2,000). The default's figure is the same estimand
computed with the share carried unconditioned (or by term, or by locked rate), which the seven campaigns contradict
(their shares sort by the drop within every campaign and term), so it is the easy method on the same literal estimand,
not another reading of it.

## Oracles

- The campaign briefs: each quarter's card for reinvestment and the retention offer's limits; inputs every route reads
  the same way; no share, no hours.
- The close-outs and the dial log: the past campaigns' events; every basis reproduces them (they are what happened), so
  none ties only under the golden.
- The treasury funding outlook (distractor): term funding balances by month, member deposits and certificates with
  wholesale term deposits, and one flat 82 per cent rollover assumption; no conversation share, no hours, and no figure
  any ask's path reproduces.
- Harbourline's 2027 staffing proposal (distractor): team sizes, shift patterns, the hourly rate and a capacity well
  above any route's hours; no forecast of the society's hours.
- No published share by drop, no past forecast, no booking memo and no rule of thumb for the block ships, so nothing
  ties only under the golden or only under the default.

## Ask sheet

The main call's declared row population: every row of the January to March 2027 list, the 2025 and 2026 lists, the
release log, the dial log, the close-outs, the contact points, the do-not-call register, the eight campaign briefs, the
SOW and the procedure. Device and hazard rows in it: 0 (asserted: the call's figures are unchanged with every ask file
deleted, and the asks read no file the call reads except the lists, device-free). The asks read the account event
extract, the member transfers extract, the term holdings view, the legacy certificate register, the migration batches
and the extract notes; Ask A reads the past lists for its population and Ask B the coming list for its last column.
Each ask is a measure the campaigns or the book carry that the call does not turn on; neither is keyed to the call, its
construction or its figures; the two share no primary device and no primary file. No sentence in the pack adjudicates a
device: the extract notes describe each file's fields and scope only.

**Ask A. For each campaign from January to March 2025 to July to September 2026, how many of the deposits on its list,
and how much of their principal, were still on term deposit with the society 30 days after maturity** (7 counts, 7
amounts to the nearest NZ$1,000; 14 figures).
- H18 home: the audit trail of what the calls the block pays for have kept on term (a measure every closed campaign
  carries that the booking, which forecasts hours, does not turn on); use: the head of deposits reads the block beside
  what the calls have kept.
- Golden: 6,520 (NZ$486,794,000), 7,007 (NZ$526,875,000), 6,902 (NZ$504,704,000), 6,917 (NZ$500,989,000), 6,860
  (NZ$503,624,000), 6,933 (NZ$512,433,000), 7,001 (NZ$521,207,000).
- Construction: per listed deposit, a REINVEST on its own account at that maturity and no BREAK or CLOSE in the 30 days
  after; otherwise the maturity proceeds transferred that day to term deposits opened that day and still open at 30
  days, at the amount transferred; counted once per deposit.
- Primary device (D7, the true key elsewhere, a prior-id chain): a holder who changes term or amount at maturity does not
  reinvest on the old account; the core pays the old account out, closes it and opens a new term deposit funded by an
  internal transfer. The old account's events read exactly like a payout; only the transfer extract's from and to
  accounts link them. Read on the deposit's own account, every such change counts as money gone. The one coherent
  reading: the ask is whether the principal stayed on term deposit with the society, which a change of term does.
- Over-cleaning half: counting any term deposit the same holder opened within 30 days of maturity brings in new money
  from other banks (the events extract covers the holders' new term deposits, the new-money ones among them).
- Hazards: partial changes (part to a new term deposit, part paid to savings) and new money added to the new deposit
  (amounts); reinvested deposits broken within 30 days (counts and amounts); accounts listed again a year later (an
  unanchored REINVEST counts a later year's renewal); account numbers dashed on the 2025 lists and unpunctuated in the
  extracts (seen, repaired right).
- C1 (asserted): no kept deposit is broken or closed between day 25 and day 35 after maturity; no savings account pays
  into a new term deposit; every listed deposit has a MATURE event at its maturity date; no deposit both reinvests and
  pays out at one maturity.
- Span (5 files, 11 columns): the 2025 and 2026 lists (account, principal, maturity date), the account events (account,
  event type, event date), the member transfers (from account, to account, amount, value date), the extract notes.
- Stops (measured): own account only (the cracker), every count 20 to 22 per cent low and every amount 17 to 21 per cent
  low; same-holder matching, every count 34 to 59 high and every amount about 4 per cent high; transfers followed at the
  new deposit's whole principal, every amount 1.1 to 1.3 per cent high (counts land); no 30-day survival check, every
  count 117 to 139 high; a REINVEST found anywhere on the account, every 2026 figure high (2025 lands). Every golden
  amount sits at least NZ$117 from a rounding edge.
- Realism: a core system that books a change of term as a closed deposit and a new one funded by transfer is ordinary.

**Ask B. How much principal on term deposits and investment certificates together matures across the society in each
month of January to March 2027, and how much of it is not on the list** (6 amounts to the nearest NZ$1,000).
- H18 home: a qualifier of the call (how much of the maturing book the booked hours work on), from the maturity book
  the list was cut from, on rows outside the list; use: the note's line on what the campaign covers.
- Golden: January NZ$467,102,000 (not on the list NZ$60,860,000), February NZ$633,665,000 (NZ$74,665,000), March
  NZ$633,034,000 (NZ$80,661,000).
- Construction: the core holdings view's deposits and certificates maturing in the month, counted once per account,
  plus the legacy register's certificates maturing in the month that no migration batch moved; the list's principal by
  month taken off.
- Primary device (D1, the same records under two sources): the legacy platform's register (30 June 2026) still lists
  every certificate; the July to October batches moved most of them to the core under new account numbers, where they
  sit in the holdings view as KIC. The overlap shows only by joining the batches' core accounts to the holdings view;
  adding the register whole double counts the moved certificates, and the core alone drops those still on the
  platform. Re-batched certificates (deferred in one batch, moved in a later one) punish a rule keyed on DEFERRED.
- Second device (D6, a quantity on every line it covers, grain unstated): the holdings view lists each account under
  each holder, the account's whole principal on each row; about one deposit in six has two holders.
- Hazards: the list's principal by month (one row per deposit, no joint repeats); certificates listed only as DEFERRED
  (still on the platform, counted from the register).
- Span (5 files, 10 columns): the holdings view (account, customer number, product, principal, maturity date), the
  legacy register (certificate number, principal, maturity date), the migration batches (certificate number, core
  account, status), the coming list (principal, maturity date), the extract notes.
- Stops (measured): rows summed and both sources added (the natural read), every total 16 to 18 per cent high and the
  part off the list more than doubled; once per account with the register added whole, 1.1 to 1.7 per cent high and 8
  to 13 per cent on the part off the list; once per account, core only, 0.2 per cent low and 1.3 to 1.8 per cent on the
  part off the list; rows summed, core only, high; the register's DEFERRED and unbatched certificates added, every
  figure high. Every golden figure sits at least NZ$170 from a rounding edge (an unlisted, sole-held deposit's principal
  is shifted by a multiple of NZ$50 in the generator when a month would sit within NZ$150 of one).
- Realism: a customer-centric holdings view repeats an account under each holder, and a migration in batches leaves a
  frozen legacy register beside the new core.

**Hazard table.**

| Hazard | Asks moved | Per-ask movement (measured) |
|---|---|---|
| Account number formats (dashed, unpunctuated) | A | none once normalised; an unnormalised join drops every 2025 deposit |
| Partial changes and new money in the new deposit | A | every amount, 1.1 to 1.3 per cent |
| Breaks within 30 days | A | every count and amount |
| Accounts listed again a year later | A | every 2026 figure |
| Joint holders in the holdings view | B | every figure |
| Re-batched and deferred certificates | B | every month |

**Referee.** None needed: no designed disagreement between two systems is arbitrated by a third file.

**The cracker sheet.** The cracker filed the golden hours and months, ran the hygiene battery (keys unique, no exact
duplicates, every join matched, no fan-out) and executed every filed rule:

| Ask figures | The cracker's path | What keeps it wrong | Cracker result |
|---|---|---|---|
| Ask A, 7 counts and 7 amounts | each listed deposit's own account: reinvested and open at 30 days, or gone | a change of term at maturity reinvests through a new account funded by transfer | miss |
| Ask B, 6 amounts | the holdings view once per account after the key check, the certificate register added for certificates | the moved certificates sit in both sources, joined only through the batches' core accounts | miss |
| Note's chart and opening (recommendation block) | the booking and the monthly hours | carried by the main call, scored with it | outside |

The mirror sheet (the same response stopped at R1) differs from the cracker sheet only on the recommendation criteria,
so no ask is coupled to the call. Ask B is the weaker device: a response that reads the batches against the holdings
view and dedups the holder rows lands it, 6 of the 20 ask figures.

Mirror leakage: 8 per cent of the ask weight (method credit on the ask paths, no figure).

**Pair arithmetic.** Planning weights 36 recommendation (the booking, the three months, the note's opening), 9
instruction following (the two files, the chart's named parts), 55 asks over 20 figures. With r = 4 (the chart's
structure and the note a wrong call keeps) and each top response keeping about 8 per cent of the ask weight: C = 36 + 9
+ 4.4 = 49.4 for the cracker, S = 4 + 9 + 4.4 = 17.4 for the mirror. If both also land Ask B (16.5 of the ask weight),
the pair rises to 45.9.

Pair ceiling: 33.4

## Prompt

`prompt.txt` (voice-check.py exit 0, 847 characters): how many agent-hours to book for the 18,400 deposits on the
January to March 2027 list; td_booking_q1_2027.xlsx with the hours for the deposits maturing in each month, Ask A for
the seven campaigns and Ask B for the quarter's maturities; td_booking_note_q1_2027.docx opening with the booking and
charting the hours by maturity month; hours to the nearest 250, deposits whole and dollars to the nearest thousand, in
the last sentence. It names no method, convention, input file, standard or person, and nothing about rates, drops or
the retention offer.

## Build record

- Generator: `task137/generator/build.py` (world, sim, book, pack, docs, postprocess, calc, asks, golden, writeup,
  checks, verify). Seeded per purpose (`world.rng`), fixed mtimes, office containers and PDFs normalised to the
  fiction's owners and stamps.
- Pack: 27 files in 6 formats (csv, pdf, docx, eml, txt, xlsx); the dial log 264,592 rows; target.zip 9.9 MB.
- Checks: every SF row, every rung and rival off every graded bin, the 32-member corridor, the domain claims the note
  and write-up make, both asks' goldens, stops and C1 conditions, separation and distractor deletion, the realism sweep
  and the goldens against figures.json, all green; `verify.py` (csv, pypdf, openpyxl; no generator import) green from
  the bundle alone.
- Two consecutive builds byte-identical: target, golden, metadata.json, figures.json and target.zip.
- `figures_check.py task137`: every figure in blocks 1 to 4 is in figures.json.
- `guard.py surface task137`: exit 0. The people the pack names are the card's (an email sign-off that set a first name
  before the full name read as two personas and was reworked). Four pairs promoted on card axes only (task117, task37,
  task97, task44: the same gap, pattern, Gate G and decision type), each differentiated on the card, surface overlap
  0.075 to 0.089. `guard.py heart task137`: WARN (`repeat.gate_g` against task130, answered in `## Draw`).
- `leak.py --asof 2026-11-04`: the one LEAK (Harbourline's proposal gave a minimum block of 1,500 hours, the golden's
  January figure) fixed in the generator (750). REVIEW lines, each harmless: 3.15 in two briefs is a posted rate the
  call reads, not an answer; the briefs, SOW and extract notes share the call's domain nouns (agent-hours, Harbourline,
  term deposits, maturity, list), not its figure or its step; the briefs, SOW, notes, procedure and proposal carry 5 to
  7 of the stump paragraph's generic words (release, retention, callable, account, quarter) and none names the drop or
  any conditioning of the share; the dates after 4 November 2026 are maturity dates of deposits and certificates still
  running, forward-looking by nature.

## Tried and rejected

- The seed's architecture (FC08): the vendor's standard dialling rules withheld from the contract and recovered from its
  acknowledgements, with the callable-number count behind two number-level joins as the decisive unit. Rejected at the
  draw: a rule recovered from settled records is banned as the decisive step, and with the rules filed the callable
  count is rule application; the wash stays as depth on the default path.
- A first card in the seed's world as a bank (`financial_institution`, context artifact `operations_log`): blocked by
  the guard against task128, live beside this build (a Canadian bank's collections centres); the deposit-taker became a
  New Zealand building society and the context artifact the block-order thread.
- The coming list's special as the 2024 three-year special (5.65 per cent onto a 3.00 per cent card): the latest
  campaign's share by term and the share by locked rate within term landed 2 to 3 per cent under the golden, because the
  2026 campaigns' three-year deposits, opened at the 2023 peak, met the same drop. Moved to a 2023 four-year special,
  whose past four-year peers all locked in the 2021 and 2022 lows; every term-based rival now lands 19 to 28 per cent
  short.
- Hours to the nearest 100: with the list's drops on thin past support (0.25, 0.55, 1.50 points) the estimator corridor
  (bands of 0.2 to 0.5 at offsets, logistic, isotonic) spread 110 to 230 hours. The 2027 card was set so the list's
  drops sit on dense past drops (0.45, 1.35, 2.00, 2.30, 2.50), and the block moved to multiples of 250 (SOW 2.2,
  procedure 6.1).
- Hours to the nearest 500: the locked-rate and trend rivals landed all three months, and rounding each month to 500
  stopped the months adding to the block.
- Extract notes that said the certificates in the holdings view were moved to the core and what MIGRATED means: they
  narrated Ask B's overlap; the notes now describe the files' fields only.
