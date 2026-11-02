# task183 design note

Architecture 4, a re-root (2026-11-02). Architecture 1 (Tamsin Valley Electric's underground cable program) is spent on
measurement and stays delivered on the portal as it shipped; architecture 2 (a city electric department's Feeder 14
patrol) is spent at the judge on Gate G, its shipped DMS fault-location log having carried the stump; architecture 3 (a
train operating company's SPAD review) is spent at the judge, its default path having applied the brake sheet's filed
level-track rate, a reading the judge licensed. All three identities sit in the card's lineage with their fates. The
objective and the number are kept; the client domain, the world, the dataset, the generator, the shell and the decisive
step are new.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task183.json`, architecture v4, checked on the draft and registered
  2026-11-02, then checked again on the filed card. v3 moved into `lineage` with its fate beside v1 and v2, and its shell
  into `lineage_shells`.
- **Pairing:** Banking, Credit & Financial Risk, task type `fraud-aml-detection` (serves AD), objective Anomaly
  Detection & Diagnostics: cash put through a front business separated from a business whose own customers simply pay
  cash. Shape `01` (every reviewed customer carries the figure, those over the line referred); decision
  `designation_set`, answer the set of customers referred. Question form `who`. Not energy, physical or environmental
  sciences, biomedical and clinical research, actuarial science, human factors, survey research or general statistics
  (the main thread's exclusions); not a domain the lineage used (energy twice, human factors once).
- **World:** Lough Ree Bank, a fictional Irish regional bank with branches in Connacht and the midlands (real counties
  and towns: Athlone, Roscommon, Longford, Mullingar, Ballinasloe, Tuam, Castlebar, Carrick-on-Shannon). Its business
  current accounts in the cash-intensive segment (cafes, takeaways, barbers, nail and beauty salons, car washes and
  valeting, convenience stores, launderettes) take card payments through the bank's own merchant services. Financial
  Crime Operations reviews the segment each year under the Business Cash Review Standard (BCR-3): for the review year
  1 October 2025 to 30 September 2026, every customer whose lodged cash beyond what its own trading took exceeds
  EUR 40,000 is referred to Financial Crime Investigations at the Financial Crime Risk Committee in January 2027, which
  restricts the accounts and opens the case. As-of Friday 6 November 2026.
- **Mechanism:** gap `objective` (cash intensity against the trade's peers is a correct figure and is not what the
  referral is scored on, the cash the customer's own trade did not take), pattern `D` (the account totals and the
  lodgement-level detail are both correct, and the decision lives only at the lodgement grain), generators G2 decisive
  (each lodgement read against the card trade of the trading days it carries), G14 (the peer ratio does not apply to
  this customer), G3 (the lodgement record against the trading operation). Gate G `decomposition_attribution` (each
  customer's lodged cash split between its trade and an outside source); strategy `decomposition_attribution`;
  calibration `settled_transaction_ledger` (the merchant services daily file of settled card trade, the forcing file at
  a finer grain than the account export).
- **Validation where the golden applies (lesson 12):** the golden imputes each customer's trading cash as its own card
  trade at its own ratio with no fixed part. Customers on the bank's own till service (EPOS) carry a daily till record
  of cash and card sales, which observes trading cash directly; BCR-3 files that till figure as the measure for those
  customers (its independent use), and the till customers sit in every trade, the car wash and nail bar trades
  included. `checks.py` back-tests the golden's lodgement-window estimator on every till customer as if its till were
  unknown and asserts it reproduces the till's cash, proportional with no fixed part and each lodgement equal to the till
  cash of the trading days since the one before (which also closes the window convention), while the peer ratio misses
  individual till customers by tens of per cent. Neither front nor either of the default's referrals runs the till
  service, so the till record arbitrates nobody's figure on the decision.
- **Furniture:** forum `committee_or_panel` (the Financial Crime Risk Committee), forcing event `audit_or_inspection`
  (the annual review of the cash-intensive segment under BCR-3), organisation `financial_institution`, role
  `operations_director` (the Head of Financial Crime Operations runs the investigations desk and decides the referrals),
  context artifact `operations_log` (the account and merchant services records the review works from), opening
  `question-first`. Personas drawn with `guard.py names --geo Ireland --seed 183` (en_IE): Malachy Crohan (Head of
  Financial Crime Operations), Helen Culhane (Money Laundering Reporting Officer, owner of BCR-3), Conall Mulgrew (cash
  operations), Dearbhail Cashman (merchant services); none a v1 to v3 persona; the prompt carries none.
- **Axes redrawn and why the labels are the honest ones:** the window at the draw (task163, task458, task454) bans
  `compliance_or_audit`, `programme_officer` and `policy_adviser`, `government_agency` and `local_government`, and the
  context artifacts `register`, `monitoring_export` and `filed_standard`. The Head of Financial Crime Operations runs a
  first-line operations desk (case intake, investigations queue, account restrictions) rather than the second-line
  compliance function, which the MLRO holds, so `operations_director` is the role as the bank organises it; the review
  works from the account and merchant services records, an `operations_log`, while BCR-3 is the governing document the
  WHAT is filed in.
- **Guard result:** `check` on the draft PASS after one differentiation (below); nearest driver on file 0.08 (task196
  v2), then task125 v3, task470 v1, task482 and task238, all under the 0.12 warn band. `test.same_driver_older`
  against task69's never-built PA draw (gap objective, pattern D, Gate G decomposition) is differentiated on the card:
  task69 rebuilt experiment effects in the joint cells of two concurrent randomisations; this build randomises nothing.
  Differentiation also filed against task201's v1a (an intercept of a cross-variant regression read as a statistic's
  inflation, killed at its draw) and task180 v5 (a volume-linked shortfall split by the meters' drift on litres since
  calibration): neither decomposes a unit's own payments against its own activity interval by interval.
- **`guard.py slots`, mechanism and setting, before the first harness:** on the mechanism (co-mingling, cash
  deposits, card takings, cash-intensive, takeaway, merchant services, the driver sentence) nothing on file but task183's
  own rejected heaping of deposits under a threshold, task268's card takings at a counter (a ticket-tying device) and
  task454's rejected merchant-side ask; on the setting (trade-based laundering, sanctions, AIS, vessel) nothing. The
  candidates that died at this draw are in `## Tried and rejected`.
- **Data-native sentence:** a cash business's takings come from the same customers on the same days whichever way they
  pay, so its cash moves with its card trade from one lodgement to the next at a ratio its own customers set (a market
  town cafe's regulars pay cash, a car wash's drivers tap their cards); the outside cash the car wash and the nail bar
  put through is handed over by the week and lodged in fixed sums beside the takings, so it lifts their cash share only
  to their trades' ordinary level, while the cafe and the barber whose own customers pay cash sit far above their peers.
- **Abstraction sentence (written to test it):** "an inflow that should move with a unit's own activity carries a part
  that does not, and a ratio of the unit's channel totals against its peers' reads that part as an ordinary channel mix
  while flagging units whose own mix is simply heavy; the part shows only when each payment is read against the activity
  of its own interval." No approved build carries it: task180 splits a throughput-linked shortfall by the instrument
  drift's true clock, task196 counts what two capture channels miss, task191 reads an outcome share over undecided
  cases, task182 a length-biased snapshot; none reads a unit's own payments against its own activity interval by
  interval.
- **The 10/10 rules first (`CLAUDE.md`):** the deciding quantity, each customer's lodged cash that its own trading did
  not take, is the AML question for a cash-intensive business (rule 1); the mess is settlement lags, post office
  counter dates carried only in the credit reference, cent and euro units, a re-sent quarter export, several terminals
  to a customer and bank holidays, none of which moves the call (rule 2, Layer 1); the decisive step is decomposing each
  customer's lodgements against its own card trade lodgement window by lodgement window rather than against its trade's
  peer ratio, with every record correct and no shipped artifact stating any ratio, rating, benchmark or estimate of any
  customer's unexplained cash (rule 3; lessons 9 and 11). The WHAT (cash lodged beyond what the customer's own trading
  took) names the quantity and never the card trade, the lodgement window or the co-movement the step recognises
  (lesson 10's test, run here: the sentence that would close a peer-ratio reading is the data's own refutation of it,
  every legitimate customer's cash tracking its own card trade at its own ratio in every lodgement, not a filing).
- **Ask layer, as built (screened as code at stage 2, `generator/ceiling.py`):** two blocks on records the main call
  never reads, their devices on customers outside the review population.
  - Ask A, the post office channel: An Post's export of every business lodgement its counters took for the Bank and
    Schedule 2 of the agency agreement; the mechanic is An Post's move from its older counter platform to the newer one
    office by office through the year, the older platform writing the whole cash tendered into the export's notes field
    beside the coin declaration (family D3, a per-row convention; the draw's card re-pointing was dropped at stage 2,
    its population needed a filed pin that named it).
  - Ask B, the till service: the service's central Z-report log for every till customer and the merchant services
    file; the mechanic is the mobile tills (market stalls, a food truck, a caterer) that hold their Z-reports and send
    them in a batch when they next connect, so the log's received time stands for several trading days (family D8, an
    upload date for the event date; the draw's dispute cycles were dropped at stage 2, the cycle count was a fork only a
    pin naming the device closed).
- **Sources read, one line each:**
  - `CLAUDE.md` and the build brief (lessons 1 to 11): the default path is the analyst's own model on correct records,
    no shipped figure of the decision quantity, the WHAT names nothing the step recognises, two ask families.
  - `stumping/SKILL.md` 1.1b and 1.4: the field's AML screen (cash intensity against peers) at rung 0 files the wrong
    customers; the decisive step is the recognition that a customer's own trade, read lodgement by lodgement, is the
    reference the peer ratio stands in for.
  - `stumping/references/client/layer2-rigor-patterns.md`, fraud-aml-transaction-monitoring: no card carries the
    decomposition; the card's peer and threshold habits supply the default path.
  - task180 v5 (approved today): the template of a decomposition the field's method gets wrong and the population's own
    records settle; here the field's method is a peer ratio, the outside part does not move with the trade at all, and
    no instrument or drift law is involved.
  - `supplemental-stumping/SKILL.md` Parts 0 to 3: asks on rows outside the main population, two primary families on
    disjoint blocks, measured by `generator/ceiling.py`.
- **Harness at the draw (`scratchpad/task183_a4/harness/h2.py`, three seeds, clean truth):** the peer screen
  (median, mean or pooled ratio) refers the cafe and the barber with two or three others and leaves the car wash and the
  nail bar at EUR 6,000 to 14,000 over their peers; every lodgement-window decomposition (least squares with an
  intercept, weighted by window length, Huber, a per-day term) refers exactly the car wash and the nail bar (EUR 94,000
  to 100,000 and 49,000 to 51,000) with every legitimate customer inside EUR 10,000 of nought; the own ratio through
  the origin refers no one; calendar-week and calendar-month versions and windows dated by the credit day refer dozens
  of legitimate customers, so the window alignment is part of the step. One convention forked in the sketch (whether a
  lodgement carries its own day's trade: one legitimate customer reached EUR 41,000 under the wrong one), to be closed
  by the lodgement times the records carry and asserted.

## Default path

The pipeline a competent AML analyst builds from the prompt and BCR-3, with the field's screen in it.

1. Read BCR-3: every customer in the segment is reviewed on the review year 1 October 2025 to 30 September 2026, and
   one whose lodged cash beyond what its own trading took exceeds EUR 40,000 is referred.
2. Build each customer's cash lodged in the review year from the account export (branch counter and post office cash
   lodgements, the re-sent quarter de-duplicated); for a customer on the bank's till service take its trading cash from
   the till, as BCR-3 files it.
3. Build each customer's card takings for the year from the merchant services daily file (its terminals mapped through
   the merchant register, gross, refunds netted, cent read as euro cent).
4. For every other customer, compute its cash intensity, cash against card takings, and its trade's peer median across
   the segment, the AML screen for a cash-intensive business.
5. Take the cash its trading took as its card takings at the peer ratio, the excess as lodged cash less that, and refer
   every customer whose excess is over EUR 40,000.

Ends on: the cafe and the barber, EUR 118,551 and 51,301 over the peer ratio (EUR 120,000 and 50,000 at the bin), with
the car wash and the nail bar under the line.
Golden: the car wash and the nail bar, EUR 99,899 and 49,952 lodged beyond their own trade (EUR 100,000 and 50,000).

## Stump sentence

A competent analyst reads each customer's lodged cash against its card takings at its trade's peer ratio and refers
the cafe and the barber, whose cash runs EUR 118,551 and 51,301 above it; the step that lands it there is judging a
customer's cash against its peers' ratio instead of against its own card trade lodgement by lodgement, which shows the
cafe's and the barber's cash moving with their trade at their own ratio in every lodgement and the car wash and the nail
bar carrying a fixed sum in every lodgement, EUR 99,899 and 49,952 over the year, that their trade never moved.

## Three rules

Task type: `fraud-aml-detection` (Banking, Credit & Financial Risk), serving Anomaly Detection & Diagnostics: cash put
through a front business told apart from a business whose own customers pay cash, judged against a referral line.
Domain test: the deciding quantity is each customer's cash lodged in the review year beyond what its own trading took,
the AML question for a cash-intensive business, and the field's screen for it is cash intensity against the trade's
peers; the golden estimates it by decomposing each customer's lodgements into the part that moves with its own card
trade from one lodgement to the next and the part that does not.
Swap: "which of our hospitals drew more than 40,000 litres of oxygen their own beds did not use" keeps the arithmetic
and loses the call: there is no outside cash supply co-mingled with takings, no lodgement cycle carrying several trading
days, no card channel recording the same customers' spend day by day and no front whose outside sum rides in every
lodgement, so the split that decides does not exist.
Layer 1: the account export (card settlements a working day or more after trading, Friday to Sunday settled on Monday,
net of charges; post office counter lodgements credited the next working day with the counter date only in the
reference; one quarter delivered twice; dates day-first); the merchant services daily file (cent, ISO dates, several
terminals to a customer through the merchant register, refunds as negative lines); bank holidays and the Christmas
closure. Each is what the producing system writes; none is placed to be caught, and none moves the call.
Layer 2: `estimation_fit`, a decomposition: the choice that flips the call is the reference a customer's cash is read
against, its own card trade lodgement window by lodgement window with a part that does not move allowed (golden),
against the trade's peer ratio (refers the cafe and the barber) or its own ratio through the origin (refers no one).
Decisive step: reading each lodgement against the card trade of the trading days since the customer's previous
lodgement, estimating the cash that moves with that trade at the customer's own ratio and the part that does not, and
taking the part that does not as the cash its trading did not take.
Not semantics: reading every field and code right (the counter date in the post office reference, the trading day
against the settlement day, cent against euro, the re-sent quarter, each terminal's customer) and running the field's
screen still refers the cafe and the barber, because their cash sits far above their peers' ratio while the fronts'
outside sums lift them only to their trades' ordinary share; no field, code, unit or definition carries the outside
part, which is a property of how each customer's cash moves against its own trade.
Not rule application: BCR-3 files the estimand (cash lodged in the review year beyond what the customer's own trading
took, the till's cash sales where the customer runs the bank's till service, more than EUR 40,000 referred) and no
method for a customer without a till; executed with the field's screen it refers the cafe and the barber. Enumerated
family (harness h2.py, three seeds): peer median, mean and pooled ratio (the cafe and the barber with two or three
others), own ratio through the origin (no one), calendar-week and calendar-month regressions (dozens), windows dated by
the credit day (dozens), lodgement-window decompositions by least squares, length-weighted least squares, Huber and with
a per-day term (the car wash and the nail bar, EUR 98,487 to 99,899 and 49,410 to 50,466 on the cut pack). Standing
family once the records are read right: the lodgement-window decompositions, spread EUR 1,412 on the car wash and 1,056
on the nail bar, one set and both bins held (checks F1 to F3). What rules out the rest is loud: every legitimate customer's fixed part sits within EUR 10,000 of
nought against the fronts' 49,000 and more, the peer ratio misses individual till customers' observed cash by tens of
per cent, and the till back-test reproduces every till customer's cash with no fixed part (figures fixed at stage 3).
Analyst test: a strong analyst who cleans both exports, reads every field correctly and runs the field's AML screen,
cash intensity against the trade's peer median, refers the cafe and the barber, EUR 118,551 and 51,301 over the peer ratio (EUR 120,000 and 50,000 at the bin), with
the car wash and the nail bar under the line (the default path's Ends on): their cash shares sit inside their trades'
ranges.
Estimand: BCR-3 sections 3 and 4 in `business_cash_review_standard_BCR-3.pdf`: population every customer in the
cash-intensive segment reviewed for the year; outcome the cash lodged to its accounts in the review year beyond what its
own trading took, the till's cash sales being that measure for a customer on the bank's till service; window
1 October 2025 to 30 September 2026; unit the customer; comparison more than EUR 40,000, referred.
No decoy: nothing is planted to be caught: no memo, draft, prior review, alert list, risk score, peer benchmark or
stakeholder figure states or argues an answer; every customer in the segment is rated high risk by the segment's own
rule, so no rating ranks them; the till service records are the bank's own product data, carried for BCR-3's till rule.
No certified replay: no certified or published figure is reproduced to recover a method; no published cash shares ship,
and every ratio is read off the bank's own records.
Lesson: a business's own takings move with its own trade from one lodgement to the next, so cash beside them that
does not move with that trade is outside cash however ordinary the business's cash share looks, and a peer ratio both
hides a front at its trade's median and refers a business whose own customers pay cash. No build on file decomposes a
unit's payments against its own activity interval by interval.

## Survivor anatomy

Actor: each customer has rows (lodgements in the account export, terminal days in the merchant services file); the
property that decides, a fixed sum riding in every lodgement that its own trade never moves, has no column anywhere: it
is a relation between each lodgement and the card trade of the trading days that lodgement carried.
Link: nothing keys a lodgement to its days; the comparison is each lodgement's amount against the card trade, by trading
date through the merchant register, of the days since the customer's previous lodgement, across two files, a join the
field's screen never asks for because it compares a customer's year totals with its trade's peers.
Reflex: the field's AML screen for a cash-intensive business, cash intensity against the trade's peer median (mean and
pooled ratio alike), sits at rung 0 and refers the cafe and the barber at EUR 118,551 and 51,301 (`Ends on:`).
Back-test: the screen validates where an analyst checks it: the median, mean and pooled peer ratios refer the same two,
the cafe's and the barber's cash ratios are the highest in their trades, and the next model a careful analyst tries,
each customer's own ratio through the origin, fits every legitimate customer closely and refers no one.
Second use: the account export is the lodgement record, the merchant services file the card takings the screen itself
reads (and ask B's terminal days), the merchant register the terminal map, the till file BCR-3 4.2's measure and the
lesson 12 back-test, the review list the population; with the decisive step deleted every file still carries the
default path.
Shock: the fronts are no extreme of any shipped statistic: the car wash's cash-to-card share (0.427) is its trade's
median and the nail bar's (0.365) sits inside its trade's 0.274 to 0.424, they rank 23rd and 42nd of 48 by cash lodged,
and both lodge twice a week like most of the segment (checks SH1, SH2).
Pins: BCR-3 files the WHAT in the bank's own standard (population 2.1, year 2.2, lodgement and its date 3.1 and 3.2,
unexplained cash 4.1, the till measure for till customers only 4.2, the line 4.3); no sentence names the lodgement
window, the fit, the fixed part or a peer comparison, and no peer table, ratio or screen ships (lessons 10 and 11).

## Readability screen

| Rung | Route | What it needs from the pack | Verdict |
|---|---|---|---|
| 0 | peer median screen | the review list's Trade, the year's lodgements and card takings | readable |
| 0b | peer mean or pooled ratio | the same totals | readable |
| 1 | own ratio through the origin | each customer's own year totals or lodgement windows | readable |
| 2 | calendar week or month regressions | weekly or monthly lodgements against card takings | readable |
| 3 (decisive) | the lodgement-window decomposition with a part that does not move | each lodgement against the card trade of the days it carried, a relation no column holds | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | lodgements to which accounts | all of a customer's accounts | the current account only | same call (no lodgement reaches a second account) | BCR-3 3.2, and same call |
| SF2 | a lodgement's date | the day handed in (the post office counter date in the reference) | the posting date | a different call | BCR-3 3.2 |
| SF3 | the review year | 1 October 2025 to 30 September 2026 | none in the files | same call | BCR-3 2.2 and the prompt |
| SF4 | the trading days a lodgement carries | the days from the previous lodgement to the day before | the lodgement's own day included | five referred | every lodgement handed in before 13:00, and the till back-test: the own-day window misses the tills' cash on nearly every lodgement |
| SF4d | the window's edges, the judge's residual | the previous lodgement's day to the day before | the previous lodgement's day to the lodgement's own day | same call, the car wash at EUR 94,183 (the 95,000 bin) and the nail bar at 49,601; the day after the previous one to the own day moves the nail bar to 54,583, and to the day before gives 105,036 and 53,808 | the till back-test: only the day-before window reproduces every till customer's lodgement to the cent, each other edge missing nearly all of them (SF4d, SF4e) |
| SF5 | the day of the card trade | trading_date | settlement_date | dozens referred | the merchant services file's own trading_date |
| SF6 | refunds | net | gross | same call | same call |
| SF7 | the quarter delivered twice | each Transaction Ref once | both copies | a different call | the repeated Transaction Ref |
| SF8 | till customers | BCR-3 4.2, the till's cash sales | the card model | same call | BCR-3 4.2, and same call |
| SF9 | more than EUR 40,000 | strictly over | at or over | same call | both referrals clear the line by EUR 9,400 and more under every member |
| SF10 | post office lodgements handed in on the last days of September and credited in October | in the year, not in the account export | read from An Post's export | same call (both referrals lodge at branch counters) | asserted |
| SF11 | rounding | the nearest five thousand euro | none | bins 100,000 and 50,000 across the standing family | the prompt |
| SF12 | ask A: a fee falling on an exact half cent | rounded up | half to even, or the float the arithmetic leaves | ask figures only: half to even moves 10 of the 12 monthly fees, float all 12 (the call untouched) | Schedule 2 clause 1.2, "a half cent rounding up" |

## Ladder

| Rung | Method | Referred | Car wash | Nail bar |
|---|---|---|---|---|
| 0 | peer median ratio (mean and pooled the same) | the cafe and the barber | under the line | under the line |
| 1 | own ratio through the origin | no one | EUR 13,625 | EUR 1,892 |
| 2 | windows dated by settlement, or by posting, or with the own day | dozens, a dozen, five | off | off |
| 3 | lodgement-window decomposition, least squares (golden) | the car wash and the nail bar | EUR 99,899 | EUR 49,952 |

Margins: the fronts clear the line by EUR 59,899 and 9,952 at the golden and by 58,487 and 9,410 at the family's lowest;
every other customer sits at EUR 1,346 or less; the family's spread (EUR 1,412 and 1,056) stays inside both bins. The
rung-1 fit is refuted on the fronts' own records (intercept t 61 and 32, through-origin RSS 38 and 11 times the
decomposition's, residuals against card correlated -0.985 and -0.953), and on no legitimate customer (median |t| under
1.5).

## Closure table

| Axis | Reading here | Closure |
|---|---|---|
| 1 Population | every customer on the review list | BCR-3 2.1; the list ships |
| 2 Unit of account | the customer, all its accounts | BCR-3 3.2; SF1 same call |
| 3 Attribution window | a lodgement in the year by the day handed in | BCR-3 3.2; SF2, SF10 |
| 4 As-of dating | records pulled after the year closes | BCR-3 5.1; C1 |
| 5 Version basis | the export as delivered, the repeated quarter once | SF7 |
| 6 Denominator | none: an amount, not a rate | not applicable, C1 |
| 7 Weighting | each lodgement once in the fit | C4: WLS and Huber in the standing family, same bins |
| 8 Window length | the review year's lodgements | C1: fitting on all history gives the same bins |
| 9 Boundary inclusivity | strictly over EUR 40,000 | SF9, C1 |
| 10 Rounding path | each figure once to the nearest five thousand | SF11 |
| 11 Tie-break | none needed | C1: no figure near a bin edge (nearest 987) |
| 12 Maturity and censoring | none: the year is closed | C1 |
| 13 Order of operations | de-duplicate, date, window, fit | C1 |
| 14 Row order | none | C1, the fit is order-free |
| 15 Duplicate resolution | one copy per Transaction Ref | SF7 |
| 16 Identity normalisation | terminals to customers through the merchant register | the register's own keys, C1 |
| 17 Netting against gross | refunds net | SF6 same call |
| 18 Dimensional units | cent in the merchant file, euro elsewhere | the column names, C1 |
| 19 Code and status semantics | LDG lodgements, AN POST LODGEMENT references | BCR-3 3.1, the export's own labels |
| 20 Integerisation | none | not applicable |
| 21 Clause scope | 4.2 for till customers only | BCR-3 4.2's own words |
| 22 Forward window contents | none: a closed year | not applicable |

## Literal reader

Executing BCR-3 and the prompt word for word: the population is the review list (2.1), the year 1 October 2025 to 30
September 2026 (2.2), a lodgement is cash handed in at a branch counter or a post office counter (3.1) dated by the day
handed in, totalled over all the customer's accounts (3.2); unexplained cash is the year's lodgements beyond what its own
trading took (4.1), the till's cash sales for a till customer (4.2), referred when more than EUR 40,000 (4.3). For a card
customer the text leaves the estimate of what its trading took to the analyst and ships no rate, ratio or peer table to
apply, so no literal reading files a number; every model the records leave standing (the lodgement-window
decompositions) files the car wash and the nail bar in the same bins, and every model they refute (the peer ratios, the
own ratio through the origin) is refuted by records a grader can rerun (checks D1, D2, B1 to B3). The asks: Schedule 2
1.1 to 1.3 file the cash (notes and coin together), the fee and the counter's month; the till ask files the trading day
in its own words. Every fork row above is asserted in `generator/checks.py`.

## Oracles

No control ties only under the golden or only on the wrong read. BCR-3 carries no figure; the till file is a measure for
till customers only and validates the golden's model without stating it (lesson 12); An Post's export carries no
totals, and Schedule 2 only rates; the till log has no daily or monthly summary. The merchant services file is the trade
record under every reading; it arbitrates ask B's batched Z-reports by amount and hands over no ask figure.

## Ask sheet

Ask A, An Post (24 figures: each month's cash lodged at post office counters and the agency fee due).
- H18 home: the audit trail of an input the call consumes (the reviewed customers' post office lodgements are part of
  what An Post took) through rows the call never reads (the other business customers') to the agency's own terms.
- Use: Financial Crime Operations shows the committee the post office channel the reviewed cash came through, and cash
  operations settles An Post's invoices against Schedule 2.
- Primary device (D3, a per-row convention): An Post moved its counters from the older platform to the newer one office
  by office (six offices, the last still on the older one at year end); the older platform writes the whole cash
  tendered into notes_eur beside the coin declaration, so notes plus coin counts the coin twice. Forced row by row:
  banknotes come in fives, and on exactly those rows notes_eur is off a whole five while notes_eur less coin_eur is on
  one (K1, K2). Over-cleaning half: notes_eur alone for every row drops the newer platform's coin (K5).
- Hazard: 21 January 2026 sent twice under the same ap_ref (K6).
- File: an_post_business_lodgements_2025-10_2026-09.csv, 9 columns; Schedule 2 PDF.
- Stops: plain notes plus coin misses every figure (cash high by EUR 8,880 to 79,572 a month, fees by EUR 5.74 to
  51.76); notes only misses every figure (cash low by EUR 66,998 to 137,900); the golden.
- Realism: a counter platform migrated office by office, its export field carrying what that platform recorded.
- Pin test: the asking sentence and Schedule 2 file cash, fee, month and the half-cent rounding (1.2, added at the
  judge's FIX_NOW: 46 lodgements carry an exact half-cent fee); no pin names a field or a platform.

Ask B, the till service (24 figures: each month's cash sales and paid-outs the tills recorded on its trading days).
- H18 home: the audit trail of BCR-3 4.2's own input, the till service's records, across the service's customers.
- Use: the committee sees the till service's cash month by month, the measure 4.2 rests on.
- Primary device (D8, an upload date for the event date): the mobile tills (market stalls, a food truck, a caterer)
  hold their Z-reports and send them in a morning batch, so received_at stands for several trading days; some of their
  trading days run on the portable terminal alone with no Z-report. Forced: one Z-report closes one trading day, and
  each Z-report's card sales equal its terminal's trade on exactly one day after the till's previous Z (T1 to T4).
  Over-cleaning half: laying a batch on the terminal's last days by count misses (T6).
- Hazard: the late bars' Z-reports sent after midnight (the hour profile repairs them). The log carries no repeated
  row: a retried upload was drafted and is not in the cut.
- File: till_service_z_report_log_2025-10_2026-10.csv, 9 columns; merchant services file; merchant register.
- Stops: received dates miss every figure; the careful reconstruction (morning batches filled back one a day) misses
  every figure (cash sales off by EUR 296 to 4,073 a month); laying batches on the terminal's last days misses 18 of
  24; the golden.
- Realism: mobile EPOS that store and forward when they next have a connection.
- Pin test: "on that month's trading days" files the date the figure is cut by; nothing names a batch or a terminal.

Main population zero-counts: no reviewed customer's An Post row is a device row (K3) and every reviewed till sends each
Z-report the evening it closes (T5); the devices sit in ask-only files the call never reads.

| Response (the cracker sheet) | Ask A device | Ask B device | Verdict |
|---|---|---|---|
| cracker: battery, plain fields, Schedule 2 executed | reads notes_eur as notes | fills each batch back one a day | miss |
| mirror at the peer screen, same asks | same | same | miss |
| lazy: received dates, plain notes | same | received dates | miss |
| over-corrected: notes only | drops the newer platform's coin | fills back one a day | miss |

Pair ceiling: 28.5 (cracker 45.0 on the call, mirror 12.0 off it), measured on the cut pack.
Mirror leakage: 0.0 per cent of the ask weight.
Single-device exposure: a response that repairs one device and not the other keeps half the ask weight, 72.5;
the full includer (both repaired) reproduces figures.json, as the script requires.
Measured by: generator/ceiling.py.

## Leak review

`leak.py task183 --asof 2026-11-06`: REVIEW, no LEAK; each line ruled.
- Sweep 3, "golden figures" 10896, 10731, 10643 and 10444 in the review list, the merchant register and the merchant
  services file: they are the customer numbers of BC-10896, BC-10731, BC-10643 and BC-10444, the keys every file joins
  on, and once a coincidental cent figure (10643 cents of trade, a balance of 10,731.65); no referral figure appears.
- Sweep 3, BCR-3 carries 11 of 16 words of the call: its referral clause 4.3 (Financial Crime Investigations, the
  January committee, EUR 40,000), the WHAT the call executes; it names no customer and no method.
- Sweep 4, six stump-paragraph words in BCR-3 (lodgement, record, population, operations, refers): the standard's own
  vocabulary for population, lodgement and referral; it names no window, fit, fixed part or peer comparison.
- Sweep 6, the review list and the merchant register name candidates beside numbers: account numbers, MCCs, opening
  dates and statuses, nothing ranked on the decision question (Gate G).

## Pre-ship check

- **The 10/10 rules, re-read against the built pack.** Rule 1: the deciding quantity is each customer's cash lodged
  beyond what its own trading took, the AML question for a cash-intensive business, worked from the bank's own
  lodgement and card records; the swap to oxygen and beds loses the outside cash riding in every lodgement. Rule 2:
  Layer 1 is the systems' own mess (the repeated quarter, counter dates in references, settlement against trading days,
  refunds, lodgements credited after 30 September), none of it deciding (SF2, SF5, SF6, SF7, SF10); Layer 2 is the
  decomposition of each lodgement against the card trade of the days it carried. Rule 3: nothing planted, no field read
  decides, and no filed rule performs the step: BCR-3 files the WHAT and ships no rate, ratio or peer table.
- **The decisive step is still analytical, on the built pack.** A strong analyst who de-duplicates the export, dates
  each lodgement by its counter day and runs the field's peer screen files the cafe and the barber at EUR 118,551 and
  51,301 (L1 to L3); the own ratio through the origin files no one (L4); only the lodgement-window decomposition with a
  part that does not move files the car wash and the nail bar, every standing member in the same bins (F1 to F3), the
  through-origin fit refuted on the fronts' own records (D1) and on no legitimate customer (D2, A2).
- **Determinacy on the built pack.** The standing family spans EUR 98,487 to 99,899 and 49,410 to 50,466, inside both
  bins; the judge's window residual (previous lodgement's day to the own day) gives 94,183 and 49,601, the same call,
  and is closed by the till back-test, which only the day-before window passes (SF4d, SF4e, B1); every other customer
  stays under EUR 4,000 under every reading (G5); the asks' fee rounding is pinned in Schedule 2 clause 1.2 (SF12).
- **Gate G.** No shipped artifact ranks the customers on the decision question: the review list rates every customer
  High and the merchant register lists terminals. The judge read Gate G as method_or_model_selection,
  analytical_non_defect, with no surface-read dependency.
- **Stage 4.** The leak reader on a490e8dc was clean (Q1 no announcement; Q2 to Q4 none; Q5 the estimand fixed and the
  method open for card customers; Q6 analytical) and its re-read on b8730f43 was clean, the half-cent pin read as a fee
  rule only. The judge's pass 2 returned DETERMINISTIC with FIX_NOW (Schedule 2's half-cent rounding, pinned in clause
  1.2; submission step 4 reworded to the card trade of the windows the year's lodgements carry), and pass 3 on b8730f43
  returned DETERMINISTIC, step 7's wording fixed in the write-up (the Z log carries no repeated row, so the step has no
  de-duplication clause) with no pack change.
- **The ask layer.** The cracker misses 48 of 48 ask figures (pair 28.5, mirror leakage 0.0); a response that repairs
  one device and not the other keeps half the asks, 72.5.
- **Every gate on the final cut.** checks 83 run, 0 failed; verify 0 differences; two builds byte-identical; target.zip
  md5 b8730f43987be07f5090d1ce8004c29a; freeze.py determinism PASS; precut exit 0; voice-check PASS; figures_check 67
  of 67; leak.py REVIEW with no LEAK, every line ruled above; guard.py surface exit 0; heart PASS.
- **House fixes run.** H1: producer metadata clean in target/ and golden/; H4: the archive's members are target/'s,
  flat; H8: every cited clause resolves (BCR-3 2.2, 3.1, 3.2, 4.1 to 4.4; Schedule 2 1.1 to 1.3); H9: no file describes
  the pack; H13: transaction references scrambled, no constant step; H16: no date past the extract of 14 October 2026.

## Tried and rejected

- Portal determinism review (2026-10-12), `competing_defensible_answer`: Sutter Park 5 under its 2025 count, two- and
  three-year averages and a recent cohort Poisson model, because the Kessler Avenue loop's overload (scheduled 2024 to
  2026) had no end anywhere in the pack and its SCADA peaks still reached 119 per cent in July 2026; the write-up's
  clause that Sutter Park 5 leads only on insulation and age was also wrong against the record. A filed back-test
  criterion was measured and rejected: on the shipped record a three-year cohort rate predicts each closed year 2019
  to 2025 best (absolute error 302 against the failure-count model's 418), so it would select Sutter Park 5. Closed
  instead by filing the overload's end (the loop's second feed, energised 15 September 2026, after its last failure on
  4 September) in the 2025 report (6.3) and the extract notes, with the write-up's clause corrected (SF9); no record
  any graded figure reads moved.

- Seed AD06 as written (a surge trigger rebuilt from a settled activation ledger): the decisive step is a rule left out of the method note and recovered from settled figures, which the guard blocks and the client caps, and under literal determinism the undefined term is a fork, not a stump.
- Drinking-water non-detects (left-censored lab results; substitution against a censored-data estimator for the 95th percentile): the decisive move is method selection (G16, banned against the last three builds), and a laboratory reporting full values is a better instrument that dissolves it.
- Heaping of cash deposits under a reporting threshold: the decisive move is a statistical test (G16 or G17), and the swap test fails because any threshold-gaming setting reads the same.
- An ICU 96-hour readmission rhythm: comparisons in 24-hour bands cancel the rhythm, so the naive read lands on the right unit by accident.
- A Farrington-type seasonal baseline behind an outbreak trigger: method selection on a seasonal baseline, and too near the background-rate driver drawn for task181 at the time.
- Capture-recapture for under-ascertained incidents: fails the instrument repair (complete ascertainment dissolves it) and sits next to task181's surveillance build.
- Funnel limits with overdispersion for an outlier hospital: the choice of overdispersion model (multiplicative or additive) flips the flag, a fork, and the decisive step is statistical rigour (G17).
- An empirical null for many hospitals' z-scores: G17 decisive, and a reflex correction for a strong solver.
- Technical against non-technical distribution losses: decomposition_attribution is banned against the last three, and it is task180's first world.
- Card cohort seasoning behind an early-default alarm: adjacent to task133 and to a task181 architecture.
- A post-campaign immunity rebound behind a measles trigger: needs a back-tested forecast method, a banned strategy for this slot.
- Service-time inflation behind an emergency department boarding alarm: a queueing decomposition, a banned strategy for this slot.
- Interviewer interpenetration behind a survey anomaly: causal_design, banned for this slot.
- Constant-risk standardisation, retrospective (emergency laparotomy; a community hospital good on the low-risk cases its catchment brings and poor on the high-risk ones; card drafted, guard PASS with no WARN, never registered): once the estimand is filed literally (the death rate the system's patients would have had at each hospital) the careful first move is direct standardisation and it lands right; the only deeper variant, risk bands too coarse, is a fork (in the sketch three bands named another hospital, five bands gave 1.14x, six bands 1.20x, per-hospital logistic curves 1.19x).
- Frailty as the unmeasured modifier in the same world: the target hospital was not worst under the frailty strata across seeds, and the strata were fragile.
- Left truncation in a joint-replacement registry (a hospital that joined late loaded its earlier primaries from its surveillance list, alive and unrevised, so the time before loading is immortal; delayed-entry Kaplan-Meier names it, Kaplan-Meier from the operation names another): it survives the literal test but fails the clean-data and instrument repair, because a registry that captured every primary at its operation makes the naive estimate right; also every partial correction (drop the loaded records, a rate from loading, a clock from loading) lands right, and a late-rising hazard put the target first on counts and crude shares.
- Constant-risk forecast (a closing hospital's emergency laparotomies moved to a neighbour in 2027; each hospital's 2027 ratio of observed to predicted deaths): it passes Gate G (a different population at a different date, both limbs filed), but the method stays open between a carried ratio and each hospital's own curve, and every filed criterion that separates them either names the step (calibration at each level of risk) or needs a back-test across a mix change (a dated event, and a banned strategy here); the per-hospital 2027 ratios also differ by estimator in the second decimal, so they cannot be graded.
- Composition designs in general (standardisation to a common population, each unit's own curve applied to a known forward mix): applying stratum-specific rates to a mix is the "reweight" reflex on the readability screen, so the decisive rung is readable however the bands are drawn.
- Device records against faults on an outage export (one fault opens several protective devices, the default counts rows): the client's Layer 1 library lists collapsing staged restorations into events as mess, so the stump would rest on Layer 1.
- Wastewater signal per person contributing to the sewer (students and visitors against census residents): the literal estimand has to name the denominator, and the fecal-strength ratio is one ratio a solver reads off a column (tests 2 and 6).
- Locus effect with masking variants in a genome-wide scan: filing the estimand literally ("the locus's variants together") names the joint model, and any selection rule for the joint set is a fork.
- Tuberculosis contacts progressing to disease in 2027: the same "a quiet unit about to surge" insight as task181's nowcast, a clone risk in the same task type.
- Learning curve of new structural heart programs: the rate-in-cumulative-experience family of task46 and task132.
- Intensive care blocking by queueing scale: no anomaly-detection task type hosts it, and the empirical past blocking is the right forecast while the load is stationary.
- This draw's first card (gap population, pattern E, gate method_or_model_selection): guard BLOCK on same_puzzle_older and same_driver_older (task28, 30, 31, 32, 53, 57, 69, 76, 228); redrawn as gap time with G14 decisive and gate forecasting before registration.
- Cable recurrence world, first tuning: with recurrence only from the third failure, the trailing in-service average already named the target (it never replaced, so its repeat failures sat in the default window); fixed by moving the recurrence threshold to the second failure, flattening the target's yearly counts, and giving the other feeders replacement at the second failure since 2019.
- Builder's first tuning (WIP before the restart): the section-year split credited the rest of each piece after a failure to the count before it, which inflated the rates after two and three failures; fixed in `models.py`, and on correct exposures the WIP world's R3 lead fell to 1.24x and the Poisson model with attributes to 1.03x.
- The WIP world itself (paper cable spliced in place, episodes on every count, Mill Lane 7 still at three times baseline in 2026): a pooled rate after one failure of 6 to 7 per cent (paper cable and the State Route 443 run) lifted every feeder's forecast, a feeder-effect Poisson model named Mill Lane 7 (1.13x) and passing history to replacements named Harrow Road 12 (1.85x), a fork on SF7; replaced by paper cable replaced at its first fault, first-failure episodes, and Mill Lane 7's episode easing out.
- A fourth rung above the failure count, 2026-10-15 (the author asked for a second decisive layer). Two were
  built and measured, and both died on this world's own structure:
  - the repeat hazard as a function of time since the last failure, with a second spliced-in-place run (a duct
    bank under a rail viaduct) carrying a recent cohort of second failures: the process self-regulates, because a
    section with a high hazard fails often and its time since the last failure stays short, so the built cohorts
    came out with the same time since (medians 1.2 and 1.8 years) and the layer had nothing to separate;
  - the repeat hazard conditioned on the water the section's structures stand in, with the viaduct run drying out
    when the deck was relaid: the water is the cause of the failure count here, so the two are collinear by
    construction and the conditioning added nothing the count had not already given; worse, the inspection
    file's Water Level column makes it a header-found join, which fails the readability screen's schema test, and
    a readable decisive rung is dead.
  The deeper reason is that in this world any model conditioned on the section's failure count already ranks
  Quarry Hill 21 first by a wide margin (its stock is 14 sections at three failures or more), so a decoy cannot
  outrank it on a count-conditioned basis without a failure volume that would also make it lead the default
  five-year average, which collapses the ladder. A fourth rung therefore needs a re-rooted world with different
  volumes, not a hardening of this one, and the shipped build was left exactly as it is (rebuilt byte-identical
  after the experiment).

- Removing the filed adjudication, the cheap repair the rework was opened on, 2026-10-22: dead on measurement,
  and it was priced clause by clause before anything was edited (harness
  `scratchpad/t183rw/s4.py`, run twice byte-identical). Two of the four clauses the wave 8 reader quoted are
  redundant and could go (report 6.2 on Harrow Road 12's paper replacement, because the register's own status,
  retired_date, insulation and install_date columns already refute a per-feeder rate there, 21.79 expected
  against the attribute model's 2.08, a ratio of 10.5; report 6.4 on Harrow Road 14's elbow batch, because no
  standing member of the estimator family names Harrow Road 14 at all, 0 of 9). One cannot go: the prompt's
  "sections in service at the end of September 2026" is the estimand's population, one of the five parts
  `determinism-check` section 1 requires filed. And one is load-bearing: SF9, the Kessler Avenue loop's
  overload and its relief in report 6.3 and the extract notes, is the clause the portal's own determinism
  return of 2026-10-12 required, and removing it reinstates `competing_defensible_answer` exactly, Sutter Park
  5 under the last twelve months (1.083x), a two-year average (1.043x), a three-year average (1.088x), a
  straight line on the yearly counts (1.076x) and an exponentially weighted count (1.025x), with Quarry Hill 21
  second in all five. So the dial has both ends on the same end: the convergence Gate C rests on here is the
  reach Gate F pays, which is the condition `stumping` 1.1 names, and it holds because the easy route (a
  trailing average) is itself a member of the family the portal licenses.

- Resuming this architecture at all, 2026-10-22: dead, because the stump does not need the clauses. The
  decisive content of the call is 17 in-service sections at two or more failures on Quarry Hill 21 against 0 on
  every other feeder, and five one-group-by routes on `section_id`, a key the default path already holds, reach
  the call from the files alone with no filed sentence: sections at two or more failures (infinite lead),
  sections at three or more (infinite), most failures on any one in-service section (9.000x), repeat-failure
  events inside the default path's own five-year window (4.000x) and sections spliced in place twice or more off
  `repair_code` (1.889x). The designed forecast is exactly linear in the stock counts and a regression on the
  twice-failed count alone reproduces it at R-squared 0.8180 with the same top bar, maximum difference 2.222
  expected failures. Screens failed, by name: `stumping` Part 3 step three (the correcting quantity is one per
  CLASS, four pooled rates, not one per case, and it is forced from the same file at the same grain as the main
  file rather than by a second file at a finer grain); the proxy screen in its structural form (the forcing file
  is the work order history and its plainest column, the per-section failure count, IS the correction); the
  monotone-functional screen (the graded object is a sum over a per-class rate vector, which a one-pass count
  reaches); and the designation determinacy screen (the standing family returns 2 distinct names, Quarry Hill 21
  in 12 of 16 and Harrow Road 12 in 4, and only one of those four groupings is asserted refuted in
  `checks.py`). The recorded resume line of 2026-10-20 was necessary and not sufficient: inferring the retired
  causes from the data's own structure rather than from a filing leaves every one of those five routes standing.

- Retuning this world's dial, 2026-10-22: dead, and the cells were counted jointly rather than marginally
  (harness `scratchpad/t183rw/s3.py` against a copy of the generator with the replacement year parameterised,
  run twice byte-identical). 300 settings swept over four dials, the highway run at 12, 20, 33, 48 and 70
  sections, the rate after two failures at 0.12, 0.20, 0.33 and 0.50, the rate after three or more at 0.33,
  0.50, 0.70 and 0.90, and the replacement-at-the-second-failure policy starting 2014, 2019, 2023 or never.
  The requirements were listed before the sweep: the licensed family unanimous on one printed call, the golden's
  lead at or above 1.15x, each of the three wrong rungs naming another feeder and clearing its own second place
  by 1.15x, no cheap count form naming the golden, and the golden in another printed cell. Marginally the dial
  looks open (the golden's separation holds in 181 of 300, rung 0's floor in 288, the golden in another cell in
  228). Jointly it is shut: **0 of 300**. The family is unanimous in only 32 settings, and a cheap count form
  lands the call in all 32 of them; the count of twice-failed in-service sections lands it in **300 of 300**,
  the count at three or more in 300 of 300, the most failures on any one section in 300 of 300 and the
  repeat-failure events in 288 of 300. The reason is algebra and not tuning: the decisive construction is
  `n2 + rho n3` with `rho = r3 / r2`, so `rho = 1` IS the twice-or-more count and `rho` large IS the
  three-or-more count, and the designed forecast sits between the two cheap routes by construction. Searching
  integer stocks to 60 sections and `rho` from 1.05 to 12, the largest lead an intermediate `rho` can take while
  both cheap routes name someone else is 1.2732x, so a cell exists in the geometry and no realistic replacement
  policy reaches it, which is why the sweep found none. Also measured at the shipped setting: the licensed
  family is NOT unanimous (Harrow Road 12 under the per-feeder and per-substation groupings), and rung 2's own
  lead is 1.165x on the built pack but 1.122x when the lateral is read off the register rather than moved, so
  the rung floor sits on the attribution of one lateral.
- **(2026-10-25, measured) A blind reader landed the call and took 97.7 per cent of the ask figures.** One isolated Sonnet reader at medium effort, holding only the pack, the prompt and the emitted key list, filed **Quarry Hill 21** against the golden QH21 and hit **43 of 44 ask figures**, every feeder's SAIFI, SAIDI, four-plus count and customers served among them, both major event days and the 13.72 minute beta threshold. It reached the call by the section-level reasoning this architecture rests on: it counted only insulation, splice and termination failures on sections still in service at 30 September 2026, found the 17 twice-failed sections at the State Route 443 duct bank with the crew note about standing water, set aside HR12's 322 failures because only 5 are on cable still in service, and named Sutter Park 5 as the answer a raw or trailing-twelve-month ranking gives, which is the default path. Readability test 3 and test 6 together: retiring out-of-service plant before projecting failures is what a reliability engineer does first.

- **Architecture 1 (2026-10-11 to 2026-11-02), spent on measurement and re-rooted, not on a portal result.** Tamsin
  Valley Electric's underground cable program (which of eight feeders fails most in 2027) stays delivered on the portal
  as it shipped on 2026-10-12. Its decisive quantity, the in-service sections at two or more failures, was a count of
  work-order rows by section_id, forced from the same file at the same grain as the main record, so one group-by named
  the call in 300 of 300 swept settings. Architecture 2 moves to a new world, dataset and shell (one architecture per
  world) and puts the decisive step on a per-trip quantity forced by a second file at a finer grain.
- 2026-11-02, the re-root draw, candidates screened on paper and set aside before the card was filed:
  - a cooperative's own direct load control releases blowing tap fuses minutes after each event, read as line faults
    until each outage is timed against the release log: the correcting factor is 1 for the feeder the call would
    designate (dropping the loud feeder and ranking the rest lands it, `evidence.md` Part 3 benchmark screen), the
    rebound after a control window is task131's driver, and the abstraction (an external process's events traced case
    by case and removed) is task303's and task181 v6's;
  - a feeder's insulation judged against the induced voltage of each nearby lightning stroke (IEEE 1410): the count
    form (flashovers per nearby stroke) equals the per-stroke physics in expectation whenever the stroke mix is
    stationary, so it bites only through a contrived quiet period; filed, the physics is rule application or, beside a
    density procedure, an official decoy; estimated from the feeders' own record, it is indirect standardisation by
    stress, the reweight reflex;
  - members with four or more interruptions in 2027 replayed through each member's protection path: under stationarity
    the trailing per-member count and the path replay estimate one quantity, so the gap is noise, and a protection
    change that makes it systematic is a dated step an event study finds or a forward condition (validated decoy);
  - a failing primary connection read off AMI voltages against a load flow: the calculated-against-measured voltage
    drop is the field's own method (golden at the top), and a degrading connection shows as a per-meter voltage trend at
    matched load, a cheaper route;
  - a cooperative's or a gas utility's balance separation (a loss proportional to throughput against one proportional
    to time): task180 v5 drew it on retail fuel tanks the same morning, and a gas or water balance has no
    anomaly-detection task type in this domain;
  - card-scheme dispute ratios carried into Q1 2027 through each dispute's lag: the maturity family, spent on this
    objective (task191, task194, task201).
  - The guard then moved under this draw: task180 v5 (filed 07:51 UTC) took shape 01, `line_manager_or_team`,
    `cooperative_or_member_body` and G3 into the window, and the gap population with G2 or G3 is a spent structural
    signature (same_puzzle and same_driver in the last twelve). The organisation was redrawn to a city-owned electric
    department (local government, the honest family for a municipal utility), the forum to the department's operations
    desk, the decisive generator to G2 under gap rule (no filed sentence says how a fault is located).
- 2026-11-02, stage 2 and 3 measurements of this architecture, set aside before data was final:
  - a recloser control's own reactance-based locator (voltage and current): on these conductors 1/0 ACSR's reactance
    per mile is within 10 per cent of 336.4's, so the overshoot past mile 3.6 is about 0.3 mile and no section
    changes; the locator is the DMS's current-magnitude model, the recloser senses current only;
  - a study table of fault duty at every tap: hands the position over by lookup, so the study tabulates 14B and R1407
    only; a line-end duty figure lets a 1/I interpolation from R1407 land the golden, so none is tabulated;
  - recorded currents carrying the prefault load: the DMS cluster moves to mile 8.4, the edge of sections 8 and 9,
    so the history's currents are the fault currents and no load or voltage series ships (A1 to A3);
  - ask A with the meters served per lateral as a column and ask B with the end poles per section: 42 lookups a
    cracker keeps, cut from the goldens;
  - the sections table's repair cost sentence naming "repair orders and trouble calls alike": it hands ask B's
    device over; it now files the WHAT as "everything charged for repair work on the section's poles".
- 2026-11-02, ask B's first device, spent before stage 4: one F14 job per crew per day, so a cracker that included
  the blanket (the sections table files "everything charged for repair work on the section's poles") and linked each
  line by crew and date kept 13 or 14 of 14, and two careful on-call responses sat near 72.5. Replaced by call-list
  days where crew and date match two or three jobs and only each line's hours or item places it. The radio retrofit
  was widened from L16 to L18 to L14 to L18 in the same pass, so a careful route that rebuilds only the never-heard
  meters keeps 9 of 14 laterals rather than 11.
- 2026-11-02, stage 4 (architecture 2 spent): the judge (determinism_check_report.md, cut a11364ba) returned DETERMINISTIC but SEND_BACK on Gate G. Every golden figure reproduced and no competing answer survived, but the main call's wrong route was the DMS fault-location log, a shipped artifact that locates each of the 24 trips in section 9 on a model carrying one conductor's impedance over the whole main line. The stump was catching that the system's own estimate of the decision quantity is wrong and flipping away from it (planted_defect_flip, surface_read_rejection, sole_data_defect yes; on clean data the log would give section 7 directly). The design note's argument that the log is the system's own record and ranks nothing did not hold: a per-trip location is the decision question's own answer. Dropping or correcting the log would leave the decisive step a textbook relocation, and a SEND_BACK spends the architecture; re-rooted at stage 1 into another world and dataset.
- 2026-11-02, the architecture 3 draw (outside energy, physical and environmental sciences, biomedical and clinical
  research), candidates screened on paper and with `guard.py slots` before the card was filed, one line each:
  - pharmacovigilance lot attribution by replaying each pharmacy's first-in-first-out stock: the swap test fails (a
    food lot traced through shop stock reads the same), and assigning lots is linkage, Layer 1;
  - seroprevalence corrected for antibody waning through each district's epidemic timing, and satellite burn scars
    fading by time since the burning: both are task242's shipped driver (a detector whose chance of registering an
    event fades with time since it happened);
  - signal detection theory's sensitivity against criterion for screeners: spent twice (task194 architecture 8,
    task230 architecture 2, task177);
  - pseudohyperkalaemia from samples left unspun in cold transport: task46's driver, and a scale per source pinned by
    paired samples is this batch's banned ask family;
  - colonisation pressure on a ward (acquisitions per exposure to unisolated carriers): task181 v4's crossings driver
    told in patients, and the field's own transmission reasoning;
  - household secondary attack rates net of community infection: the estimand ("infected by the index case") names
    the step on test 1;
  - over-adjustment of a provider comparison by coding the provider controls: dead on the WHAT screen (task194's
    record), and coding intensity is task458's;
  - circular flows in money laundering: task190 M3 measured dead (one divide names the round-tripper 30 of 30);
  - a SPAD world judged on wheel-measured OTMR speed that under-reads while the wheels slide: the record would be
    wrong exactly where the call turns, so the stump would be catching a recorder's error (architecture 2's Gate G
    death in another instrument); replaced by correct records and a level-track rating applied where the approach is
    not level;
  - rail SPADs per red-aspect approach: task191 architecture 3's exposure insight (warnings whose trigger was real),
    so no exposure ships for the call;
  - sun glare on east-west junction approaches: the estimand would have to name glare (test 1) or leave the junction's
    real problem open (a fork); traffic camera or STATS19-style records also carry a dazzling-sun factor (semantics).
- 2026-11-02, stage 2 and 3 of architecture 3, ask designs set aside before the cut, one line each:
  - each depot's train miles from the running record and the diagram book: every candidate device (part
    cancellations, diversions, crew reliefs, empty stock, a depot's diagrams moved at a timetable change) is either a
    labelled column the careful solver reads or a reconstruction the records do not force;
  - approaches at danger counted per signal with both units of a formation recording the stand: a two-minute window
    per signal merges exactly the pairs, since no second train can stand at the same signal inside the headway;
  - an OTMR recorder fitted to another unit and reporting its old number: the per-depot mass nets out at random and a
    one-unit-two-places check finds it;
  - drivers per depot with staff numbers reissued to new drivers: the reissue is this batch's banned family (client
    ids re-issued with a counter carrying on);
  - hours on duty corrected to the later of the record and the arrival plus ten minutes on every turn: a booking off
    a few minutes after a slightly late arrival is possible, so the literal record stands there and the max rule is a
    second reading; the repair moves only bookings off before the arrival, and the generator's telephone truth was
    set to match;
  - the first ask B layout with one weekday closing time: the evening-only partial repair kept five of nine figures
    and the mirror reached 50 per cent; weekend and midday telephone bookings (the offices' real hours) took it to two.
- 2026-11-02, stage 4 (architecture 3 spent): the judge (cut 2d063320) returned NOT_DETERMINISTIC, SEND_BACK. Every golden figure reproduced (CJ58 6 against SK112 3, stable from p25 to p95 of each approach's own stands), but SP-07 3.5 says only "a full-service application in normal rail conditions" and never says whose deceleration tests it. The only filed rate, the Class 162 sheet's 0.88 m/s2, read literally files SK112 (3) with CJ58 on 0, and the judge licensed that reading; the golden's rate from each approach's own routine stands (CJ58 0.667) is directed by no sentence. The sentence that would close the fork (the rate full service gives on that approach) names what the decisive step works out, so the fork is the stump and no pin saves it. A default path resting on a figure a shipped document states is a literal reading the judge licenses. The asks forked as well: TPWS events on speed-restriction and buffer-stop loops filed under signal_ref, and turns extended to the last arrival plus ten minutes by no filed sentence. Re-rooted at stage 1 into another world and dataset.
- 2026-11-02, the architecture 4 draw (outside energy, physical and environmental sciences, biomedical and clinical
  research, actuarial science, human factors, survey research and general statistics), candidates screened on paper and
  with `guard.py slots` before the card was filed, one line each:
  - testing yield (positives grow more slowly than tests as testing widens to people less likely to be infected):
    task236's driver (a testing change moves who is tested, so positivity moves with the change) and task304's
    screening-yield family;
  - a water-borne outbreak attributed to treatment works through each supply zone's daily blend: task263's driver (a
    source's level measured only in mixtures whose proportions change), killed again in task190 and task200;
  - regression dilution in a risk-adjustment covariate: task262 (the reliability ratio), task166 (regression dilution
    with replicate readings is the probe's reflex) and task174;
  - saturable (Michaelis-Menten) elimination in a drug-monitoring register: measured dead in task179, noted in task154;
  - Legionnaires' source attribution by plume and incubation: root cause, not anomaly detection (task188's note);
  - a self-controlled case series biased by event-dependent exposure (a contraindication deferring later doses):
    measured and rejected on its arithmetic in task180's architecture 3 hardening;
  - HIV infections dated by CD4 at diagnosis against an opt-out testing drive's backlog: the field's own
    back-calculation is the golden (the library test) and CD4 or recent-negative-test thresholds are cheap routes;
  - a product's reporting life cycle across markets (the Weber effect): disproportionality is blind to a reporting curve
    common to every reaction, so only a rise in every reaction type separates, and reports do not identify incidence;
  - trade invoices against a lot-size price curve (trade-based laundering): the lot size is a column (the schema test
    fires), the expected price at a lot size is a stratification, and the swap test is weak;
  - a cash business's cash against its ticket size or its purchases at a markup: a size covariate on a column
    (composition, readable) and a named forensic method (the markup method) as the golden;
  - AIS silence on financed voyages read through each gap's kinematics: the WHAT (a call at a sanctioned port) is not
    determinable without filing the inference standard, which names the step;
  - an ATM's demand displaced from its neighbours' outages against a cloned-card cash-out: cash-outs are caught at the
    transaction level by card and BIN patterns, so a volume model is not the field's analysis;
  - a seasonal baseline against a multi-year epidemic cycle, and seasons aligned on their own timing: the cycle is
    visible in any plot (a reflex), and a WHAT built on alignment names the step.
- 2026-11-02, the architecture 4 harness at the draw (`h1.py`): outside cash added once per calendar week rather than
  in each lodgement is misspecified against a per-lodgement fixed part, and the decomposition missed the nail bar
  (EUR -10,000); calendar-week and calendar-month regressions and windows dated by the credit day gave every legitimate
  customer spurious fixed parts (dozens referred). The design adds the outside sum to each of a front's lodgements and
  the golden reads each lodgement against the trading days it carries (`h2.py`).
- 2026-11-02, stage 2 ask screen: the draw's ask A (business lodgement cards re-pointed to a new account, the register
  holding only the current one) needed its population filed as the card's account at the counter date, a pin naming the
  device; replaced by An Post's notes field on the older counter platform.
- 2026-11-02, stage 2 ask screen: the draw's ask B (dispute cycles logged as fresh cases) forked on whether a second
  chargeback is a chargeback received; only a pin counting each sale once closed it, and that pin names the device;
  replaced by the till service's batched Z-reports.
- 2026-11-02, stage 2 ask screen: ask B's trading-day count per month landed for the careful reader by cancellation in
  one to three months on five upload seeds; replaced by the paid-outs, a cent figure no cancellation reaches. Card sales
  were left out of the ask so it does not point at the till-to-terminal identity the repair rides on.

