# task167 design note

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task167.json`, registered 2026-10-18T06:59:01Z, guard WARN (no BLOCK).
  WARNs answered: driver.near 0.12 against task501 v3 (its catch-up is driven by a deadline, what a fund must still
  place before its investment period ends; here it is a class of schedule shape that each fund's own first-year
  notices reveal, and no deadline enters); overuse.objective and overuse.gate_g (Forecasting is the lane's most
  wanted objective, and two schedules pinned by the funds that have passed the forward ages is the honest Gate G);
  repeat.decision against task168 (the call is an amount, the reserve). The older same-puzzle and same-driver
  matches (population, E) carry one differentiation line each on the card. The card's shape moved from 02 to
  `other` at the PAUSED commit (`## Tried and rejected`: the quarterly path is not determinate; the criteria come from
  one reserve, its four strategy components and two decoupled ask tables, arithmetic in the ask sheet).
- **Pairing:** Nonprofit & Grant-making (house domain `nonprofit-grant-making`, task type endowment management, card
  subdomain `other`), client domain General Statistics & Data Science, task type regression classification model
  diagnostics (the pacing model's out-of-sample diagnostic). Objective Forecasting & Predictive Modeling: the reserve
  is next year's expected capital calls on commitments already made, a value the supplied fund history pins, for a
  window (calendar 2027) not yet run.
- **Seed:** FC38, re-rooted by the coordinator on 2026-10-18 after the measurement in `## Tried and rejected` (v1).
  Kept from the re-root: the world (a grant-making foundation's private-markets programme), the decision (the call
  reserve the liquidity policy requires for the coming year) and the quantity (next year's capital calls on existing
  unfunded commitments). Generator seed 167 (the task number), fixed before any outcome was seen.
- **World:** the Brandvold Foundation, Saint Paul (invented; no foundation of that name found). 186 fund commitments
  since 2006 through 194 vehicles (eight funds hold a main and a parallel vehicle), 172 of them from the 2006 to 2022
  vintages and 14 from the 2026 re-entry programme ($1,164.3 million at the year-end rate, three of the fourteen in
  euros), whose first closes fell between 12 January and 30 March 2026 after the board suspended new commitments for
  2023 to 2025 while the private allocation sat above its range. 146 funds are active at 31 December 2026.
- **Strategy:** `forecast_method_backtest`, pattern E (G14's form) with G16 as the frame. The natural fit, a call
  schedule by fund age pooled over every fund (Takahashi-Alexander rates on the undrawn balance, or shares of
  commitment by age), is wrong out of sample for the funds that bridge their first deals on a subscription line:
  they call fees and one small first investment in their first year, under 8 per cent of commitment in all, and the
  deals the line carried in their second, while fifteen ordinary funds that started slowly called 11 to 18 per cent in
  theirs. No field names the class; the shape of each fund's first-year notices shows it, with a clean break between
  7.6 and 11.1 per cent. The programme spends 2027 in its second year, and twelve of its fourteen funds called less than
  8 per cent of commitment in 2026.
- **Furniture (honest alternatives where the first choice was banned at the draw):** forum `board_of_directors` (the
  foundation is a Minnesota nonprofit corporation; its board confirms the call reserve at its January meeting);
  forcing event `vote_or_meeting` (that meeting, 21 January 2027); organisation `foundation_or_funder`; role
  `compliance_or_audit` (the investment office's director of investment risk, Troy Stein, who certifies the reserve;
  the treasurer, `finance_controller`, was banned against task198); context artifact `close_out_summary` (the
  administrator's year-end capital account summary; `filed_standard` banned against task168); calibration `none`
  (the back-test runs on the spine's own record, no separate organ ships).
- **As-of:** notices and positions to 31 December 2026; the board set was assembled on 14 January 2027 for the
  meeting of 21 January (`leak.py --asof 2027-01-14`).
- **Personas** (`guard.py names --geo 'United States' --seed 167`): Troy Stein, Kristin Brown, Brian Erickson,
  Adriana Mitchell (the grants office's budget memo). Lisa Stone and Sara Salazar were passed over (first names on
  task118 and task265); none appears in the prompt.
- **Sources read for the domain (stumping 1.3):** task501's pacing architectures (a deadline catch-up, a filed
  walk-forward, a recycling term; this build has none of the three), task132 (renewal of replaced modules: a wear
  curve restarted, here two curves never mixed), task166 (balloon refinance by cover: a conditioned share read at due
  dates, here a conditioned schedule read at ages). The data-native sentence: the class lives in the timing of each
  fund's own notices, which no column records, because a subscription line moves the call date and not the deal date.

## Default path

The pipeline a competent analyst builds from the prompt and the files, with every field and filed rule read correctly:

1. Read `fund_commitments_register.xlsx` (one row per vehicle: commitment, currency, first close, strategy) and join
   `investor_capital_activity_2016-04_2026-12.csv` on the administrator code and
   `legacy_administrator_notices_2006-2016.xlsx` on the former administrator's name, counting the second quarter of
   2016 once (the export manifest says the current administrator re-keyed it), dropping cancelled notices and
   reading calls gross of any distribution set against them (policy 2.3).
2. Build each fund's calls by month of age from its first close (policy 2.4), fees, expenses and offsets included.
3. Fit the call schedule by age over every fund, as Takahashi-Alexander rates on the undrawn balance (the field's
   standard pacing model), checking it against shares of commitment by age and by strategy.
4. Apply it to each active fund's 2027 ages and undrawn balance, euro funds at the 31 December 2026 reference rate
   (policy 2.5), sum and round up to the next $50 million (policy 2.2).

- **Ends on:** a reserve of $350 million (expected 2027 calls $344.5 million on the pooled rates on the undrawn
  balance; $298.2 million and a $300 million reserve on pooled shares of commitment).
- **Golden:** a reserve of $450 million (expected 2027 calls $425.3 million).

## Stump sentence

Fitting one call schedule by fund age over every fund the foundation has backed and applying it to each fund's 2027
age and undrawn balance files a reserve of $350 million, because twelve of the fourteen 2026 programme funds belong to
the line-bridged class their own light first year shows (fees and a first investment, under 8 per cent of commitment),
whose second year calls 37 per cent of commitment against the pooled schedule's 21, so the 2027 calls are $425.3
million and the reserve $450 million.

## Three rules

- **Task type:** General Statistics & Data Science, regression classification model diagnostics: the pacing model is
  chosen on its out-of-sample error on the funds that have passed the ages the forecast needs.
- **Domain test:** the deciding quantity is next year's capital calls on existing fund commitments, the pacing
  forecast an endowment's investment office builds from its funds' contribution schedules by age (Takahashi-Alexander
  rates fitted to its own history), with the schedule of the funds that bridge their first deals on a subscription
  line found from their light first years and validated on the funds that have passed those ages.
- **Swap:** "how large a reserve must we hold for 2027's capital calls" with a hospital's capital projects for funds
  stops making sense: no limited partnership calls an allotment on a schedule its general partner sets, no credit
  line defers the first calls, no light first year marks a schedule shape.
- **Layer 1:** two administrators' notice files in different layouts with the 2016 handover quarter in both (the
  administrator change); euro funds in euros (the general partners' currency); distributions set against calls on one
  notice late in a fund's life and fee offsets on buyout and growth notices (the general partners' notices); twelve
  cancelled and reissued notices (the administrator's processing); names keyed differently across the administrators
  (two systems); none placed to be caught, each neutral for the call (R2, asserted).
- **Layer 2:** forecast_uncertainty: the model choice on out-of-sample error, a schedule conditioned on each fund's
  own first-year class against one pooled schedule, which the funds that have passed their second year decide.
- **Decisive step:** condition each fund's call schedule on its financing class, read from its own first-year notices
  (fees and a first investment, 5.2 to 7.6 per cent of commitment, annualised for the programme's younger funds,
  against 11.1 per cent or more for every other fund, fifteen slow-starting ordinary funds among them at 11.1 to 17.8),
  and read the programme's line-bridged funds at the line-bridged funds' schedule; the out-of-sample record chooses the
  break at the gap over a round threshold past it or two clusters.
- **Not semantics:** every field, code, currency, status and date read correctly, and every filed rule applied, still
  leaves the pooled schedule on $350 million; no column, code or document names the class, and line types only say
  what each amount was for.
- **Not rule application:** policy 2.2 to 2.5 file what is forecast (the population, the outcome, the window, the unit,
  the clock), not how; no filed rule splits the schedule, and executing every rule with the pooled schedule files $350
  million.
- **Analyst test:** a strong analyst who stitches both administrators' files, counts the handover quarter once, drops
  cancelled notices, reads calls gross, ages funds from first close and converts euros at the year-end rate, then fits
  Takahashi-Alexander rates by age over all 172 funds, files a reserve of $350 million where the line-bridged funds'
  own schedule gives $450 million.
- **Estimand:** policy 2.2 to 2.5 (`liquidity_and_reserve_policy_2025.pdf`): the capital calls the Foundation expects
  to pay in calendar 2027 on the commitments made before 1 January 2027, fees, partnership and organisational
  expenses included, before any distribution set against a call, euros at the 31 December 2026 reference rate,
  rounded up to the next $50 million; 2027's new commitments are outside it.
- **No decoy:** nothing is planted to be caught: no memo, draft, briefing or stakeholder figure argues a schedule, no
  block is copied, no rule is withheld; the pooled schedule arrives only as the analyst's own reflex.
- **No certified replay:** no certified or published figure is reproduced to recover the method; the out-of-sample
  record is the funds' own calls, and no document scores a schedule.
- **Lesson:** a pacing curve is a property of how a fund finances its deals as well as of its age; a model learns to
  look for the class a fund's own early record reveals before pooling, and to validate on the units that have passed
  the forecast's ages. No build on file conditions a schedule on a class read from each unit's first period.

## Readability screen

Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a row
predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds it, 6
one subtraction, ratio or half of a figure). Figures from `generator/ladder.py` on the cut pack, asserted in
`generator/checks.py` (LADDER, REFLEX, R3a, R3b).

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 2026's calls carried ($198.0 million, reserve $200 million) or 2026's rate on the undrawn balance ($165.3 million) | policy 2.2 asks for calls expected in the year | the activity file's 2026 lines | yes, the trailing year | the funds' own ages: the programme was in its first year in 2026 | no | yes | readable |
| R1 one schedule by age pooled over every fund ($344.5 million on rates, $298.2 million on shares; reserve $350 or $300 million) | policy 2.4 files the clock | the first close and every call by month | yes, the default (Takahashi-Alexander) | the analyst's own back-test: left out a vintage at a time, the pooled schedule misses the line funds' second years low in every one of twelve vintages, by $177.7 million in all | no | no | readable |
| R1b the schedule by strategy or by recent vintages or calls since 2019 ($349.0, $359.9, $358.9 million; reserve $350 or $400 million) | no | the register's strategy and vintage | yes, stratify on what is visible | the same back-test: the class runs across every strategy and vintage | no | no | readable |
| R1c the programme's own first-year pace carried ($147.6 million; reserve $150 million) | no | the programme's 2026 lines | yes, credibility on the young book | the history: the funds whose first year called under 8 per cent called 37 per cent of commitment in their second | no | yes, one ratio | readable |
| R1f the class misplaced: a round 15 or 20 per cent threshold, or two clusters of first-year share ($391.1, $376.2, $374.3 million; reserve $400 million) | no | the first-year shares | yes, a round cut or a clustering | the out-of-sample record: the slow-starting ordinary funds call an ordinary second year, so those classes miss $209.3 to $239.4 million against the gap's $160.6 million | no | no | readable |
| R2 (decisive) each fund's schedule read from the funds whose first year looked like its own: the 36 line-bridged funds' schedule for the programme's twelve, the other 136's for the rest ($425.3 million; reserve $450 million) | no sentence names a line, a facility, a class, a light year or a schedule by kind; the policy files what is forecast and the clock | no column marks the class: the register has no financing field and line types say what an amount was for | no: the reflexes are the trailing year, the pooled curve, strategy, vintage, recent windows and the young book's own pace, each measured wrong | none ships: no document scores a schedule; the closed record is read alike by every method | no: nothing is duplicated, missing or mis-keyed that points at it | no: a class read from each fund's first year, two schedules by month of age, applied fund by fund | silent |

## Semantic fork table

Every term in the main ask and every convention the main computation needs. Every id is asserted in
`generator/checks.py`.

| Id | Term or convention | Golden reading | Alternative and its call | Ruled out by |
|---|---|---|---|---|
| SF1 | "call reserve ... for 2027" | policy 2.2: the capital calls expected in calendar 2027 on commitments made before 1 January 2027, rounded up to the next $50 million | a reserve net of expected distributions; a stressed or upper-quantile figure | policy 2.2 ("the capital calls the Foundation expects to pay") and 2.3 ("before any distribution a fund sets against a call") |
| SF2 | "capital calls" | every amount called: investments, management fees net of the offsets on the notice, partnership and organisational expenses | investments only ($380.2 million, $400 million); fee offsets ignored ($425.8 million, same call) | policy 2.3 names fees and expenses; the dictionary ("A Management fee offset reduces the management fees called on the same notice"); offsets: same call (asserted), and Ask A's total 1411.6 against 1411.2 when ignored |
| SF3 | "2027" | calendar 2027 by the date paid, January to December | a fiscal year; notice dates ($435.3 million, same call) | policy 2.2 ("that calendar year"); notice dates: same call asserted |
| SF4 | "commitments made before the year began" | every vehicle with a first close on or before 31 December 2026, realised funds contributing nothing | 2027's new commitments added; realised funds projected too ($425.3 million, same call) | policy 2.3 (they "are not part of the call reserve") |
| SF5 | "expects" | the mean of the year's calls | a percentile | policy 2.2 |
| SF6 | the age clock | months from the fund's first close | calendar years from the vintage ($338.8 million, $350 million) | policy 2.4 ("a fund's age is counted in months from its first close") |
| SF7 | euro conversion | the custodian's reference rate for 31 December 2026 (1.1326) | the 2026 average ($426.3 million, same call); notice-date rates (not applicable to a forecast) | policy 2.5; same call asserted |
| SF8 | rounding | up to the next $50 million | to the nearest $50 million (450 at the golden's 425.3, 400 for any construction under 425); to the nearest $25 million (425) | policy 2.2 ("rounded up to the next $50 million"); the prompt ("as the policy does") |
| SF9 | parallel vehicles | a parallel vehicle's commitment and calls are the foundation's | each vehicle as its own fund ($425.3 million, same call) | policy 1.1 ("directly or through a parallel vehicle"); same call asserted |
| SF10 | cancelled notices | dropped | counted ($424.2 million, same call) | the dictionary ("Cancelled for a notice the general partner withdrew"); same call asserted |
| SF11 | distributions set against calls | calls read gross | the net amount ($409.1 million, same call) | policy 2.3; same call asserted |
| SF12 | the 2016 handover quarter | counted once, from the current file | counted twice ($431.1 million, same call) | the export manifest (the administrator "re-keyed the former administrator's notices from 1 April 2016"); same call asserted |
| SF13 | "from each of the four strategies" | the register's strategy of each fund, expected calls in millions to the nearest 25 | the general partner's own label | the register's Strategy column is the only strategy field |
| SF14 | Ask A: "net asset value at 31 December 2026" | policy 4.1: each fund's latest reported value rolled forward for the contributions paid and distributions received after its date (the value date, the dictionary's "date the amount was paid or received") to 31 December, euros at 1.1326, each fund once | the reported values unrolled; euros at the reporting date; the roll-forward cut on notice dates | policy 4.1 ("contributions paid and distributions received after the date of that value") and the dictionary's value_date |
| SF15 | Ask A: "euro and dollar funds", "vintages" | the register's currency and vintage (the year of first close) | the summary's currency label | the register; the summary's header ("Amounts in each fund's currency") |
| SF16 | Ask B: "qualifying assets", "face value ... maturing in each quarter" | policy 3.1: Treasury bills maturing in 2027, the Schedule 1 fund and the reserve account's cash, at market value on a settled basis; bills by calendar quarter of maturity at face value | trade-date positions; agency discount notes; the operating account | policy 3.1, 3.2 and Schedule 1; the dictionary on the positions report ("on trade date and include purchases not yet settled; the cash line is the account's settled balance") |

## Ladder

Built figures from `generator/ladder.py` on the cut pack, every row asserted in `generator/checks.py` (LADDER, R3a,
R3b, REFLEX) and recomputed from the bundle by `generator/verify.py`. Expected 2027 calls in $ million, the reserve
rounded up to the next $50 million.

| Rung | Construction | Expected calls | Reserve | Dies to |
|---|---|---|---|---|
| R0 | 2026's calls carried | 198.0 | 200 | the programme's funds were in their first year in 2026 |
| R0b | 2026's rate on the undrawn balance | 165.3 | 200 | the same, and most of the older funds' undrawn balance is never called |
| R1 default | one schedule by age over every fund, rates on the undrawn balance (monthly, quarterly, annual ages: 344.5, 343.8, 350.2) | 344.5 | 350 | the out-of-sample record: the pooled schedule puts every vintage's line funds' second year low (by $177.7 million over 36 funds) |
| R1a | the same on shares of commitment | 298.2 | 300 | the same |
| R1b | the schedule by strategy (rates; shares 300.5) | 349.0 | 350 | the class runs across strategies: 11 of 58 buyout, 10 of 47 growth, 12 of 51 venture, 3 of 16 credit funds |
| R1c | the schedule of the 2014 to 2022 vintages (rates; 2017 on 354.4, 2019 on 351.3) | 359.9 | 400 | one fund in four of those vintages bridges its first year; the programme is twelve in fourteen |
| R1d | rates on calls since 2019 (since 2022: 354.2) | 358.9 | 400 | the same mix |
| R1e | the pooled schedule at the programme's own first-year pace | 147.6 | 150 | the funds whose first year called under 8 per cent called 37 per cent of commitment in their second |
| R1f | the class misplaced: a 15 per cent threshold (20 per cent 376.2, two clusters cut at 21.4 per cent 374.3) | 391.1 | 400 | the slow-starting ordinary funds call an ordinary second year: out of sample those classes miss $209.3, $235.3 and $239.4 million of second-year calls against the gap's $160.6 million |
| R2 decisive | the line-bridged funds' schedule for the twelve programme funds whose first year called under 8 per cent (fees and a first investment), the other funds' for the rest | 425.3 | 450 | golden |

**Position and margins.** Every rung files below the golden; the nearest, R1c at 359.9, sits $40.1 million under the
golden cell's $400 million floor, and the default's 344.5 a full bin below it. The golden sits $25.3 million above the
cell's floor and $24.7 million under its ceiling.

**Convergence (C1, asserted, FAMILY).** Thirty-six constructions of the class-conditioned schedule file 414.3 to
432.1, all a $450 million reserve and all in the 425 cell of expected calls: monthly, quarterly and annual ages on
shares of commitment and on rates on the undrawn balance, commitment-weighted or equally weighted (422.9 to 432.1);
first-year thresholds of 8, 9, 10 and 11 per cent (all 425.3: the first-year shares break at 7.6 against 11.1 per cent,
nothing between); the line funds of the 2012, 2014, 2016 and 2018 vintages on (421.9 to 427.0); the programme by class
with the older funds pooled (425.7); the class schedules fitted within each strategy, on shares or rates (427.6,
426.3); each fund's 5, 7, 10, 15, 20 or 30 nearest earlier funds in first-year share, annualised or as observed (414.3
to 429.8). The strategy components at the nearest 25: buyout 174.9 to 182.7 (175), growth 94.0 to 101.5 (100),
venture 74.8 to 83.8 (75), credit 66.0 to 69.7 (75), every construction in its cell.

**Back-test (the out-of-sample record, asserted, BACKTEST).** Left out one vintage at a time, the pooled schedule
fitted on the others puts the vintage's line funds' second-year calls low in all twelve vintages that have them, by
$177.7 million in all (actual $407.5 million); the line funds' own schedule, fitted the same way, misses by $0.9 million
in all. The 36 line funds called 37.3 per cent of commitment in their second year, the 136 others 16.5, the pooled
schedule 21.2. Over every earlier fund's second year, the class at the gap misses $160.6 million out of sample, a 15
per cent threshold $209.3 million, a 20 per cent threshold $235.3 million, two clusters $239.4 million and the pooled
schedule $376.7 million.

**Routes the rule-3 audit named (asserted, ROUTE).** The regression of second-year on first-year share files $391.0 to
$398.2 million ($400 million) across its four forms; the catch-up of the programme to the pooled cumulative schedule
files $470.8 million ($500 million). Two routes skip the class and still land every graded calls figure, the reserve,
the 425 total and all four strategy cells, because cells of $25 million cannot tell their strategy splits from the
golden's: 35 per cent of the programme's undrawn balance with the earlier funds on a pooled schedule ($418.4 to $421.2
million; buyout 173.6 to 174.0, growth 96.5 to 98.1, venture 83.0 to 83.1, credit 65.3 to 66.1), and an uplift of 19.7
to 24.9 per cent (19.73 to 24.85) on the pooled rates. Others land the reserve alone: the rest of the 16.1 to 30.6 per
cent uplift band; one third of the programme's commitment ($438.5 to $441.3 million, total cell 450, venture cell 100)
or of its undrawn balance ($400.9 to $403.7 million, total cell 400); the average of the pooled rates and that catch-up
($407.7 million, total cell 400). 35 and 40 per cent of commitment and 40 per cent of the undrawn balance land $500 or
$550 million.

**Strength.** P(one strong solver lands) about 0.19 (the stage 4 recheck's figure on the repaired pack): it must read
each fund's class from the shape of its first-year notices, a light year of fees and one first investment that the
fifteen slow-starting ordinary funds do not share, place the break at the gap rather than at a round threshold or a
clustering (both file $400 million), and read the programme's twelve light funds at their own schedule. P(both land)
about 0.06, most of it the two class-free routes above that land every graded calls figure; the class counts in the
critical components (36 of 172 earlier and 12 of 14 programme funds under 8 per cent in their first year) are the one
figure none of those routes produces.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every vehicle with a first close on or before 31 December 2026, active at that date | filed (policy 2.2, 2.3, 1.1); SF4, SF9 |
| 2 | Unit of account | US dollars of capital calls in the year | filed (policy 2.2, 2.5); SF1 |
| 3 | Attribution window | calendar 2027 by month of payment | filed (policy 2.2); SF3 |
| 4 | As-of dating | notices with value dates to 31 December 2026 | filed (the export manifest) |
| 5 | Version basis | settled notices; cancelled ones dropped | the dictionary; SF10 same call asserted |
| 6 | Denominator | the share of commitment or of the undrawn balance | C1: both bases inside the cell (FAMILY asserted) |
| 7 | Weighting | commitment-weighted or equal by fund | C1: 425.3 and 425.7 (asserted) |
| 8 | Window length | which vintages the class schedule is read from | C1: all, 2012 on, 2014 on, 2016 on, 2018 on (asserted) |
| 9 | Boundary inclusivity | the first-year class threshold | C1: no fund between 7.6 and 11.1 per cent (asserted); a cut past the gap is a different class, chosen against by the out-of-sample record (C2 on the funds' own second years, asserted) |
| 10 | Rounding path | the unrounded total rounded up once | filed (policy 2.2); SF8 |
| 11 | Tie-break | none | n/a |
| 12 | Maturity and censoring | the schedule at each age from the funds observed through it | C1: every construction reads the observed funds only; the programme's first year is observed for nine to twelve months, its class read from them (asserted) |
| 13 | Order of operations | each fund forecast, converted, summed, rounded | C1 (asserted) |
| 14 | Row order | sums | C1 |
| 15 | Duplicate resolution | the 2016 handover quarter | filed (the manifest); SF12 same call asserted |
| 16 | Identity normalisation | administrator codes and the former administrator's names to the register | the register's two key columns; C1: every line joins (asserted) |
| 17 | Netting against gross | distributions set against calls | filed (policy 2.3); SF11 same call asserted |
| 18 | Dimensional units | euro funds | filed (policy 2.5); SF7 same call asserted |
| 19 | Code and status semantics | line types, status | the dictionary; SF2, SF10 |
| 20 | Integerisation | none before the total | the golden mid-cell (asserted) |
| 21 | Clause scope | the 2025 policy governs the 2027 reserve | filed (policy 5.1, adopted 12 June 2025) |
| 22 | Forward window contents | each active fund's 2027 calls | forecast from the records (the decisive step); no file covers the window |

## Literal reader

Executing the prompt and policy 2.2 to 2.5 word for word gives the capital calls the Foundation expects to pay in
calendar 2027 on the fund commitments made before 1 January 2027, fees and expenses included, gross of distributions
set against calls, each fund's age counted in months from its first close, euros at the 31 December 2026
reference rate, rounded up to the next $50 million; no shipped sentence says which schedule a fund follows, so a
literal reader must estimate it from the records; the easy method on the same literal estimand (one pooled schedule)
files $350 million, and the fork table leaves no reading under which any rung is the golden.

## Oracles

- The funds' own call history: every method reads it alike; on the wrong path it supplies the pooled schedule, and
  the analyst's own back-test on it rejects that schedule. No closed window holds a 2027 figure.
- The capital account summary: contributions and distributions to date, unfunded and reported values at each fund's
  statement date; it states no 2027 figure and ranks no schedule. Its main-vehicle rows tie to both vehicles' notices
  (the Ask A device), on every reading of the call.
- The legacy file's net amounts: calls less distributions on each notice, true on every reading.
- The custodian's account totals: the sum of the positions report's rows, true in its own scope (the Ask B device).
- No control ties only under the golden.

## Ask sheet

**Main call's declared row population:** every call line (investments, management fees and offsets, partnership and
organisational expenses) in both administrators' files, the register's rows, the reference rate for 31 December 2026,
and policy sections 1.1 and 2. Device and hazard rows in it: 0 (asserted, SEPARATION: the call computed with the
capital account summary, both custody files, every distribution line, the performance file and the grants budget
deleted is unchanged to the dollar; no ask reads a call line except Ask A's roll-forward, which reads the call lines
after each statement date and carries no device on them).

**Ask A. The private-markets net asset value at 31 December 2026 for each of the four strategies, for euro and dollar
funds, for the 2015 to 2018 and 2019 to 2022 vintages and in total** (9 figures, $ million to one decimal).
- H18 home: policy 4.1, the board's liquidity report, carries the private funds at their rolled-forward value beside
  the call reserve it certifies; the reserve is read against the book it stands behind.
- Use: the workbook's NAV table, the figures the liquidity report prints.
- Basis (filed): policy 4.1 (each fund at its most recent reported value, adjusted for the contributions paid and
  distributions received after its date; euros at the rate in 2.5).
- Primary A1 (D9 and D1, a rollup above its own parts): for each of the eight funds held through two vehicles, the
  summary's main-vehicle row is the general partner's combined statement for both interests (commitment,
  contributions, distributions, unfunded and value), and the parallel vehicle has its own row too. Summing the rows
  counts every parallel interest twice: $36.0 million in all, $13.0 buyout, $9.6 growth, $7.8 venture, $5.7
  credit. Fair: the register lists each vehicle's own commitment and the main row's commitment and contributions to
  date equal both vehicles' (asserted). Silent: every code joins, no row repeats another, the main row's name is the
  main vehicle's, and no sentence says the statement is combined.
- Primary A2 (D3, a missing currency read as the house's): the administrator's fund master defaults the currency of
  vehicles set up on its platform from 2021 to US dollars, so eleven euro vehicles carry a USD label over euro values.
  Taken at the label, the euro funds' value falls $152.5 million and the dollar funds' rises $134.6 million; buyout,
  growth, credit, the 2019 to 2022 vintages and the total move too. Fair: the register's Currency column and the
  summary's header ("Amounts in each fund's currency"); the main rows' commitments equal the register's euro amounts.
  Silent: no blank, the label is a valid code.
- Hazards: the roll-forward from each statement date (30 June for venture, 30 November for credit, 30 September for
  the rest; unrolled, the total moves $152.1 million); euros at the statement date's rate (total $0.7 million).
- Stops (built and asserted): S1 the cracker (rows summed, labels taken, the rule executed): all 9 miss; S1a A1 cracked
  alone: 7 of 9 still miss (venture and the 2015 to 2018 vintages kept); S1b A2 cracked alone: all 9 miss; S2 both: the
  golden.
- Span: the summary, the register, both administrators' activity files (the roll-forward), the reference rates, the
  policy, the dictionary (7 files).
- Realism: general partners send a combined statement for an investor's interests across parallel vehicles; an
  administrator's fund master that defaults a currency field is ordinary data debt.

**Ask B. The reserve account's qualifying assets at 31 December 2026, the Treasury bills among them and the face
value of those bills maturing in each quarter of 2027** (6 figures, $ million to one decimal).
- H18 home: policy 5.1, the certification itself: the director certifies the call reserve and the qualifying assets
  together, and the shortfall is the transfer the board authorises.
- Use: the workbook's reserve assets table and the transfer.
- Basis (filed): policy 3.1 and 3.2 and Schedule 1.
- Primary B1 (D8, a trade date for the settled position): the custodian's positions report carries the 2027 bill
  ladder bought on 31 December for settlement on 4 January 2027 ($140 million face) beside the settled cash that will
  pay for it; the settled activity report has no purchase for those four bills. Taken as reported, qualifying assets
  rise $137.1 million and each quarter's face value $40, $40, $30 and $30 million. Fair: the dictionary says the
  report is on trade date, includes purchases not yet settled and carries the settled cash balance; the opening
  position and the settled activity rebuild the settled holdings exactly (asserted); policy 3.1 says settled. Silent:
  the report's account total ties to its rows, and no row or column marks which purchases are unsettled.
- Primary B2 (D5, a category crossed by its label): the custodian's "Government Bill" class holds four agency discount
  notes beside the Treasury bills ($39 million face, one maturing in each quarter). Taken by class, qualifying assets
  rise $38.2 million and each quarter's face value $10, $8, $12 and $9 million. Fair: each row's description names its
  issuer. Silent: the class column is the one built for the question.
- Hazards: the 2028 Treasury note, the prime money market fund (not in Schedule 1), the operating account's bill and
  cash (policy 3.2).
- Stops: S1 the cracker: all 6 miss; S1a B1 cracked alone: all 6 miss (the agency notes); S1b B2 cracked alone: all 6
  miss (the unsettled ladder); S2 both: the golden.
- Span: both custody files, the policy, the dictionary (4 files).
- Realism: custodians report positions by trade date and cash by settlement; a custodian's security master groups
  agency discount notes with bills.

**Hazard table.**

| Hazard | Asks moved | Per-ask delta read the easy way |
|---|---|---|
| A1 combined statements | A | every figure, $36.0 million in all |
| A2 defaulted currency | A | euro funds $152.5 million low, dollar funds $134.6 million high, total $17.8 million low |
| B1 the unsettled ladder | B | qualifying assets $137.1 million high, each quarter $30 to $40 million |
| B2 agency notes as bills | B | qualifying assets $38.2 million high, each quarter $8 to $12 million |
| roll-forward | A | total $152.1 million high when skipped |
| the operating account and the non-qualifying holdings | B | qualifying assets $42.8 million high when counted |

**Referee.** None: the policy files every basis and nothing shipped totals a graded figure on the golden path.

**Cracker sheet** (the cracker landed the call, ran the hygiene battery, executed every filed rule and took each
file's columns as they stand):

| Ask figures | The cracker's route | Device that holds | Verdict |
|---|---|---|---|
| A, value by strategy (4) | summary rows rolled forward, euros by the summary's label | A1 at all four, A2 at three | miss |
| A, euro and dollar funds (2) | the same | A1 and A2 at both | miss |
| A, the 2015 to 2018 and 2019 to 2022 vintages (2) | the same | A1 at both, A2 at 2019 to 2022 | miss |
| A, total (1) | the same | A1 and A2 | miss |
| B, qualifying assets and bills (2) | the positions report as reported, bills by class | B1 and B2 at both | miss |
| B, face value maturing in each quarter (4) | the same | B1 and B2 at every quarter | miss |

**Single cracks.** With A1 cracked alone the cracker keeps 2 of 15 (venture and the 2015 to 2018 vintages); A2, B1 or
B2 cracked alone, none. Each pair is at most 32.2.

**Mirror sheet.** The mirror stops at the pooled schedule ($350 million); the asks are decoupled from the call, so its
ask route is the cracker's and it keeps no ask figure.

Measured by: `generator/cracker.py` (run on the cut pack by `checks.py` on every build).

Mirror leakage: 0.0 per cent of ask weight (15 ask criteria; the chart is an instruction-following point).

Pair ceiling: 28.5 (the cracker at 38 + 7 + 55 x 0/15 = 45.0, the mirror at 5 + 7 + 0 = 12.0); both top responses on
the call: 45.0; with A1 cracked alone 32.2, with any other device alone 28.5. Criteria supplied: the reserve, the
expected 2027 calls in total and by strategy (6), Ask A's 9 and Ask B's 6 figures, the workbook, the memo, the chart
with the reserve drawn across it and the rounding (4): 25.

## Leak review

`leak.py --asof 2027-01-14`: REVIEW, no LEAK. Each line:
- Sweep 3, the policy carries four of the call's five distinctive words: it defines the call reserve (2.1 to 2.5) and
  states no figure; harmless.
- Sweep 4, the grants budget memo (schedule, million, programme, second, twelve): grant programmes, the grant
  agreements' payment schedules, the second quarter and twelve quarters of endowment value; it names no fund, call or
  schedule of calls; harmless (a declared distractor).
- Sweep 4, the policy (schedule, million, commitment, commitments, investment, January): Schedule 1 is the approved
  money market fund, 2.2 to 2.3 file the estimand and 5.1 names the director of investment risk and the board's January
  meeting; it names no schedule of calls, no first investment and no financing class; harmless.
- Sweep 9, fifteen dates after 14 January 2027 in the positions report: the maturity dates of the bills, the agency
  notes and the 2028 note, forward by nature; harmless.

## Pre-ship check

The 10/10 rules read again against the shipped pack (target.zip ff9df788):
- Rule 1, the domain: the deciding quantity is next year's capital calls on commitments already made, the pacing
  forecast an endowment's investment office builds from its funds' schedules by age (Takahashi-Alexander rates or
  shares of commitment), conditioned on the financing class each fund's first-year notices show and validated out of
  sample on the funds that have passed their second year; the swap test holds (the judge's Gate H: pass, both rounds).
- Rule 2, two layers: Layer 1 is the two administrators' files with the 2016 handover quarter in both, euro funds in
  euros, distributions netted on notices late in a fund's life, fee offsets on buyout and growth notices, twelve
  cancelled notices and two naming systems, each asserted neutral on the call (R2); Layer 2 decides: the class read
  from the shape of each fund's first year, chosen over one pooled schedule, a round threshold or two clusters by the
  out-of-sample record.
- Rule 3: nothing planted, no filed method, no field marks the class. The rule 3 audit on 8abffa03 read AT_RISK,
  narrowly (P(one) about 0.25, P(both) about 0.08: the class readable as a first year with no Investments line, policy
  2.4 quotable as a HOW); repaired in one rebuild, and the recheck on 2d75d4ac read PASS at P(one) about 0.19 and
  P(both) about 0.06. The easy route on the clean truth files $350 million (R3a). Counted in P(both): two class-free
  routes land every graded calls figure, 35 per cent of the programme's undrawn balance with the earlier funds pooled
  ($418.4 to $421.2 million) and an uplift of 19.7 to 24.9 per cent on the pooled rates; the class counts in block 2
  (36 of the 172 earlier funds and 12 of the 14 programme funds under 8 per cent in their first year) are the one
  graded figure neither produces.
- Determinism: judge round 1 on 8abffa03 DETERMINISTIC, APPROVE. Judge round 2 on 2d75d4ac DETERMINISTIC, FIX_NOW
  (optional, small): calls of 425.8 and the $450 million reserve reproduced, the class-aware variants at 425 to 428,
  the pooled routes failing, the leave-one-vintage-out holding, every NAV reproduced exactly, Gates G and H pass. Its
  two pins are filed as dictionary facts (the positions report on trade date with purchases not yet settled and the
  settled cash; a management fee offset reduces the fees called on its notice), the devices left as detection work;
  figures.json and block 4 byte-identical across the fix (freeze.py: only this note's ladder section moved).
- Readers: round 1 and round 2 no leak; the targeted re-read of ff9df788 clean (Q1 and Q2 none, Q6 an analytical
  choice; both dictionary lines read as plain conventions naming no class or method; the as_of line's slight steer
  toward the settled basis reads as a custodian's field note, left).
- Duplicates: guard heart WARN (the objective's and the Gate G mechanism's use, the decision type against task168,
  answered at the draw); guard surface pairs this build with task166, back to back on pattern E, sent to the author for
  an optional clone-check, with a differentiation line on the card.
- Gates at ship: checks 127, verify 51 on its own pandas path, two byte-identical builds, figures_check 59, precut 51
  checks with no FAIL, voice-check PASS, leak.py REVIEW answered, container audit clean; target.zip from the final
  rebuild.

## Tried and rejected

- v1, the tail test on appraisal-smoothed marks (2026-10-18, on paper, never registered): the largest one-off
  outflow the endowment could take while the tenth percentile of its value ten years on stayed above a share of
  today's, with the private sleeve's marks de-smoothed before the tail is read. Died on resampling noise: on a
  148-quarter record (37 years) the ten-year tenth percentile moves by a standard deviation of about $281 million
  between independent and block-of-eight bootstrap draws on the same record (24 replicate worlds, 8,000 paths each),
  the de-smoothing variants (Geltner first-order, Getmansky-Lo-Makarov with two and three lags) move it by more, and
  back-filling the shorter private history against the longer public one scatters it by about $160 million. No
  realistic draw step is deterministic, and filing the resampling scheme to close it turns the de-smoothing step into
  a literal fork the judge executes.
- v2 draft, a call schedule broken by vintage date (2026-10-18, on paper, never registered): every fund from the
  2018 vintage on called little in year one and most in years two and three. Died at the reflex sweep on paper: any
  recent calendar window holds only post-break funds at young ages, so a plain recency choice reaches the golden,
  while a softer break leaves the cut year a knob; and abstractly it repeats task501 v4's pooled regimes (the
  forward window's regime selected from a pool of two). Replaced by the class read from each fund's own first-year
  notices, spread across vintages and strategies so no date cut, window or visible attribute isolates it.
- Line-bridged share rising with the vintage (prototype, 2026-10-18): a class growing from 10 to 55 per cent put the
  recent-vintage and recent-window rates within one bin of the golden; the share is now flat at about a quarter from
  2014 (5 per cent before), and the recency rivals sit $45.9 million under the golden's cell.
- A programme spread across the year, or closing late in 2025 (prototype): either the catch-up falls half in 2026, so
  2026's calls carried come near the golden, or calendar-year ages and monthly ages part by a bin; the first closes are
  now 12 January to 30 March 2026 and the clock is filed (policy 2.4).
- The quarterly 2027 path as graded periods (shape 02, measured on the cut pack): the first quarter ran 90.7 to 124.8
  across monthly, quarterly and annual ages, so no quarter is determinate at any useful precision; the call is graded
  on the year, the card's shape becomes `single-figure`.
- The expected calls by currency as components: dollars 327.3 to 339.2 and euros 87.0 to 91.6 straddle the $25 million
  edges; dropped.
- Distributions set against calls at 35 per cent of eligible months: read net, the reserve fell to $400 million; netting
  is now one month in ten after a fund's fifth year and never on loan income (net reading 410.0, same call).
- Parallel vehicles drawn at random from 2011 to 2021: three of the eight had less than $1 million of value left, so
  the combined-statement device moved credit and the euro funds by $0.1 million; they are now picked by rule, two per
  strategy from the 2015 to 2018 and 2019 to 2022 bands, the latest and largest.
- A single device per ask: with only A1 and B1 a single crack kept 9 or 6 of 15 figures (pair 45.7 and 39.9); A2 and
  B2 now hold every figure the other device in the ask holds but two.
- A custody wires ask (2026's capital-call payments by quarter): every candidate device was a reading (net wires,
  returned duplicates, the euro legs), so it was not built.
- `single-figure` for the card's shape once the quarterly path died (2026-10-18, at the PAUSED commit): the call carries
  a repeated unit (the four strategies' expected calls) and the asks carry the NAV and reserve-asset cuts, so the card
  takes `other`, its 25 criteria counted in the ask sheet.
- A fees-only first year for the line-bridged class (stage 4 round 1, 2026-10-18): judge APPROVE and reader clean,
  but the rule-3 audit read the class as a zero (twelve of fourteen programme funds with no Investments line in their
  first year) and found policy 2.4's "projected from its age" quotable as a HOW. Replaced by a small first investment
  call for the line-bridged funds and slow first years for some ordinary funds, 2.4 reworded to file only the clock.
  Repositioning rule, written before the redesigned world was measured: only the programme's size (PROG_TOTAL_USD,
  $0.9 to $1.3 billion in $50 million steps) and then the common first-year deal share (DEAL_YEARS[0], 0.32 to 0.38 in
  0.02 steps) may move, smallest move first; take the first setting where (a) the class-aware golden sits $12.5 million
  or more inside its bin, (b) the pooled-rate and pooled-share routes sit two or more bins below, (c) the linear
  regression of second-year on first-year share sits one or more bins below, and (d) none of one third, 35 or 40 per
  cent of commitment or of the undrawn balance, each plus the earlier funds' calls on either pooled schedule, lands in
  the golden's bin; if none qualifies, keep the setting that fails fewest of (a) to (d) and report every lander.
- Slow-starting ordinary funds at 9 to 15 per cent of commitment in their first year (stage 4 round 1, measured): a
  second break opened at 15 to 18 per cent, the widest among first years under a quarter, and a class read there took
  the slow starters in and filed $350 million; their first years now run to 17.8 per cent, so the class's break at 7.6
  to 11.1 is the only clean one.
- Slow starters making up half or all of their first-year shortfall in year two (measured): the regression of
  second-year on first-year share then sat in the golden's bin ($376 to $382 million with half made up, $395 to $399
  million with all of it, against a golden of $394 million at that size); they now make none of it up and read as
  ordinary funds in their second year.
- Twelve deals a year and an 8 per cent spread in each fund's pace (measured at a $1,050 million programme and a 0.34
  first-year deal share, the repositioning rule's first pick): the nearest-neighbour constructions ran $399 to $459
  million across k and annualising, three reserves. The structure was fixed first (twenty-four investment calls a year,
  add-ons included; a 5 per cent pace spread; first investment calls of 3.5 to 5 per cent), and the rule re-run from the
  start on it, with every class-aware construction required in one reserve bin and one cell of expected calls.
- The repositioning rule's outcome on the fixed structure (36 settings): no setting cleared (d). The first that failed
  only (d), every class-aware construction in one bin and one cell, was the 0.32 first-year deal share and a $1,150
  million programme, kept. Landing in its bin: one third of the programme's commitment or of its undrawn balance and 35
  per cent of its undrawn balance, each with the earlier funds on a pooled schedule; the average of the pooled rates
  and the pooled catch-up ($407.7 million); an uplift of 16.1 to 30.6 per cent on the pooled rates. Off it: 35 and 40
  per cent of commitment, 40 per cent of the undrawn balance, the regression ($391.0 to $398.2 million) and the class
  misplaced at 15 or 20 per cent or by two clusters ($374.3 to $391.1 million).
