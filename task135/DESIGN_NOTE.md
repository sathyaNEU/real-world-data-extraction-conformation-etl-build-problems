# task135: The Wrexford Trust, the 2027 growth share under the investment policy's volatility cap

The only reasoning record for this build. State lives in `pipeline.json`. Architecture 2 of 3, re-rooted on 2026-10-11; architecture 1 (the forebay sediment build) is spent, and its record is in `## Tried and rejected`.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task135.json`, architecture v2, registered 2026-10-11 (commit 1ceb52a), with architecture 1 moved into `lineage` with its fate. `guard.py check` returns WARN only, on `repeat.gate_g` (method_or_model_selection repeats task134 v2). The answer: task134 v2's method selection is a conversion hazard by months since admission, which is about how a pool's ages generate a flow. This build's is the covariance estimator that asynchronously struck prices entitle, which is about how co-movement is measured across striking times. The gap, the data structure and the field all differ; only the label is shared. `guard.py validate`: 138 cards, 0 invalid.
- **Domain:** Quantitative Finance (`quantitative-finance`), task type volatility forecasting (`volatility-derivatives-pricing`; nothing is priced).
- **Objective:** Forecasting & Predictive Modeling. The committed figure is the growth share for calendar 2027. It is set against the portfolio's expected volatility, the standard deviation of a twelve-month return the window has not produced, estimated from two years of the holdings' returns.
- **Shape:** 04, setting one dial. The dial is the growth share in the policy's ten-point steps from 20 to 100. The second axis is what each step yields and what each draws.
- **Criteria arithmetic.**
  - The call: 1.
  - 2027 income at each of nine steps: 9.
  - The capital release at each step: 9.
  - The 2027 grant payments: 1.
  - The chart's income bars, grant line, grants-plus-running-costs line and title: 4.
  - The two files named and the rounding: 3.
  - Total: 27.
- **Decision:** `dial_setting`, answer unit `rate_or_share`, question form `what`.
- **Mechanism.**
  - Gap: time (decisive: when each price is struck). Pattern: none.
  - Generators: G7 decisive (the operating window of each price, from the valuation points in the operations documents); G2 (the return interval as the grain of co-movement); G17 (the margin across the synchronous estimators, asserted).
  - Gate G: method_or_model_selection.
  - Stump strategy: `other`, nonsynchronous pricing.
  - Layer 2: `estimation_fit`, `own:nonsynchronous-unit-prices-in-a-portfolio-volatility`.
- **Furniture.**
  - Forum `trustees_or_governors`: the December meeting sets the share.
  - Forcing `vote_or_meeting`.
  - Organisation `foundation_or_funder`: an endowed grant-making charity.
  - Role family `portfolio_manager`: the finance director runs the annual investment review, and the prompt names no one.
  - Context artifact `monitoring_export`: the custodian's daily valuation export.
  - Calibration `none`; scoring `other`.
- **World.** England, GBP. The Wrexford Trust, an endowed grant-making charity, invests its permanent and expendable endowments as one portfolio:
  - a segregated UK equity mandate managed by Fernside Partners and held by Brackenfold Custody;
  - five Kestwick Charity Funds (North American, European and Japan equity, gilts, sterling corporate bonds), also held through Brackenfold.
- **People**, drawn with `guard.py names --geo "United Kingdom, England" --seed 1352` and on the card:
  - Harriet Clarke, finance director (owns the budget procedure);
  - Lawrence Barnes, chair of the investment committee (signs the policy);
  - Samantha Morton, grants manager (the grants exports' notes);
  - Connor Wells, Fernside's portfolio manager (the quarterly report).
  Every invented name is on the card.
- **As-of.**
  - The custodian's daily valuation runs to Monday 30 November 2026, the last month-end before the trustees' meeting of 10 December 2026, and was exported on 2 December.
  - The grants exports are at 30 November 2026.
  - The budget workbook is the draft of 24 November 2026.
  - The 2026 growth share is 80 per cent, set on 9 December 2025 (policy annex). Volatility rose through 2025 and 2026, which is why the review binds this year.
- **Data-native sentence.** Same-dated prices in this pack are struck at different times of day. The segregated UK shares are priced at the London close. Every Kestwick fund is priced at its noon valuation point from each market's last available price, so the North American fund's price on a date carries the previous evening's New York close. A daily covariance of same-dated returns therefore misses the co-movement that lands a day apart. That makes the trap native to a charity portfolio mixing a segregated mandate with noon-priced pooled funds; on any dataset whose prices share one clock it does not exist.
- **Sources read, one line each.**
  - `two-layer-task-design.md`: the three rules and the pre-ship check. They are answered below, and every Layer 1 device is kept off the call's decisive step.
  - `layer2-rigor-patterns.md`: carries no Quantitative Finance patterns. The nearest are the lagged-effect and autocorrelation patterns (psychology, urban), which teach that a same-period correlation misstates a relation running across periods. This build's version is a cross-holding lag made by pricing clocks, so it is filed as its own pattern.
  - `traps/_measured.md`: #7 (uses the ready-made measure; daily volatility times the square root of 252 is the market's ready-made annualisation) and #2 (counts file rows instead of the real unit, which is the income ask's lot lines).
  - Exemplars:
    - Nonprofit "Capital Grant Drawdown Forecasting" (0.34) teaches that a schedule's dates are not the payment dates. This build spends that idea only as an ask device (project instalments released after the report), never on the call, and files no withheld rule.
    - Economics "Treasury Cash Flow Forecasting" (0.41) is a forecast built from the record's own timing, taken for depth only.
  - `proven-in-production.md`:
    - Part 1: L7 (the naive basis is excellent on the closed record: every single-fund volatility agrees at any frequency) and L8 (no reconciliation can see the decisive move).
    - Part 4: the default construction here is not the golden, the decisive step is not a reflex, and no control or filed sentence names it.
- **Lane note.** task132 to task134 are survival and caseload builds. This one carries no time-to-event estimator, no conditioned yield and no retransformation.

## Default path

This is the pipeline the measured opponent builds unsteered, from the prompt's words and the files' grain. It was measured on the prototype in scratch (`t135-arch2/protoA6` to `protoA10`): an hourly shock model with the six holdings struck at their own points, run over a long run of 300 years and over a two-year sample (seed 2036) that meets every condition in `## Ladder`. The build (world seed 11480) measures it again from `target/`; the figures below are the build's, with the prototype's long run kept for reference.

1. Read the investment policy:
   - growth assets: the Fernside mandate 40, North American 30, European 15 and Japan 15 per cent of growth;
   - defensive assets: gilts 55 and corporate bonds 45 per cent of defensive;
   - the steps from 20 to 100;
   - the cap: expected volatility not more than 10 per cent;
   - the definition in paragraphs 4.1 to 4.4.
2. Build each holding's daily total return over the two years to 30 November 2026 (505 UK business days).
   - The mandate: the time-weighted return from the custodian's daily lot values with its cash and accrued income, external flows stripped from the capital movements report, and corporate actions carried through.
   - Each fund: the return from its dealing prices, with the distributions added back on their ex-dividend dates (from the published histories, which the custodian's fund prices agree with).
3. Put every holding on UK business days. On the noon after its own market's holiday, the North American or Japan fund's price carries that market's last close, moved only by the exchange rate; keep those days as they are. Estimate the covariance of daily returns: 505 periods, each weighted equally, well over 100.
4. For each step, combine the holdings at the policy weights, take the portfolio's daily standard deviation and scale it by the square root of 252. That gives 8.25 at 60, 9.41 at 70 and 10.63 per cent at 80 on the build (8.20, 9.34 and 10.53 on the prototype's long run).
5. Cross-check, then file:
   - each holding's daily volatility agrees with its factsheet's and with its own monthly volatility;
   - the volatility rises smoothly step by step;
   - the largest step at or under 10.0 is 70 per cent.

**Ends on:** 70 per cent growth (9.41 per cent expected volatility at 70 on the build; 80 breaches at 10.63).

**Golden:** 60 per cent growth. Co-movement is measured where the prices are struck together: weekly returns on any anchor, or daily covariances with their one-day lead and lag.
- On the build, across the golden family's 26 members: 8.96 to 9.72 per cent at 60, and 10.33 to 11.11 at 70.
- Long run: the true twelve-month volatility is 9.81 at 60 and 11.32 at 70.

**Other natural variants**, each a complete pipeline:

| Variant | Files | Why it is out |
|---|---|---|
| Exponentially weighted daily estimate (0.94) | 80 | it weights the calm last months |
| The benchmark indices | 70 | not the holdings' own prices |
| A Ledoit-Wolf shrunk daily covariance | 70 | intensity 0.031 |
| Monthly returns | 60 | 24 periods, which the policy's 100 refuses |
| Partial synchronisation (two-, three- or four-day returns on any anchor, or lead and lag on the UK and North American pair only) | 60 | lands the call |

## Stump sentence

A competent solver builds each holding's daily total return from the prices it is valued at, estimates the two-year covariance of daily returns, scales the portfolio's daily standard deviation by the square root of 252 at each step and sets the 2027 growth share at 70 per cent against 60; the step that lands it there is treating same-dated prices as same-moment prices, when the Kestwick funds are struck at noon from each market's last available price, so the North American fund's price carries the previous evening's New York close that the London-close UK shares have already priced, and the daily covariance misses the co-movement that arrives a day apart.

## Three rules

**Domain test:** the deciding quantity is the portfolio's twelve-month volatility at each growth step. Investment risk practice estimates it from returns over which the holdings' prices are contemporaneous, because a pooled fund's dealing price is struck at its valuation point from each market's last available price while listed shares are struck at their exchange's close. Put another field's nouns in and there is no valuation point, no previous evening's close inside a noon price and no twelve-month variance assembled from daily covariances, so the task stops reading the same.

**Analyst test:** take a strong analyst who strips the mandate's flows, adds back the funds' distributions, carries the corporate actions, aligns the calendars, and reads the policy's definition and the valuation points correctly.
- The easy way: they still estimate co-movement from same-dated daily returns, scale by the square root of 252 and set growth at 70 per cent (9.41 at 70 and 10.63 at 80 on the build), above what the cap allows.
- The right way: measuring co-movement over periods that align the noon dealing prices with the London close (weekly returns, any anchor), or adding the one-day lead and lag covariances, sets it at 60 (8.96 to 9.72 at 60, and 10.33 to 11.11 at 70).
The easy way gets it wrong after every field and rule has been read correctly, so the stump is analytical.

**Layer 1:** what these systems produce. None of it decides the call.
- For the call:
  - a custodian's daily valuation export at tax-lot grain across two endowment sub-accounts, with accrued income beside market value and the mandate's cash on its own lines;
  - the mandate's corporate actions in a separate events file: a 1-for-8 consolidation, a demerger whose new shares arrive the day after, a rights issue taken up, and a cash takeover;
  - external flows into and out of the mandate (a legacy added to the permanent endowment, the quarterly rebalancing transfers, and the expendable endowment's share of the capital the trustees release each quarter) in a capital movements report that a time-weighted return has to strip;
  - UK, US and Japanese calendars that differ, so on the noon after its own market's holiday an overseas fund carries that market's last close, moved only by the exchange rate; and UK and US daylight saving changes on different dates;
  - two price sources for the funds (the custodian's valuation and Kestwick's published history, which agree);
  - income units whose distributions drop out of the price on ex-dividend dates, beside accumulation units.
- For the asks:
  - an income entitlements report by tax lot that runs thirteen months and carries the position's entitlement on every lot line;
  - REIT distributions paid in two components on one ex-dividend date;
  - a grants register and an instalment schedule from the grants system (UK date format), beside a payment ledger from the finance system;
  - euro grants whose currency sits only on the register;
  - withdrawn grants whose open instalments stay Scheduled.

**Layer 2:**
- The tempting shortcut is the square-root-of-time rule on daily returns. The policy's two years give 505 daily periods, every holding's daily volatility agrees with its factsheet, and the covariance matrix looks complete.
- An expert refuses it. The variance of a twelve-month return is the sum of every lagged covariance across the year, and same-dated prices struck hours apart put a large share of the co-movement into the one-day cross-lags. The North American fund's noon price carries the New York session that the London close priced the day before.
- The rigorous method measures co-movement where the prices are contemporaneous, over periods long enough to align them or with the lead and lag terms added. The data's own cross-lag correlation demands it: 0.49 between the UK mandate and the next day's North American return, against 0.20 on the same day (the build).

**Gate G.**
- **Litmus.** No reported figure is overturned. Every price, distribution, flow and document in the pack is correct, and no shipped artifact computes a portfolio volatility.
- **Mechanism.** method_or_model_selection (the covariance estimator the data entitles), with forecasting support. surface_read_dependency: no. sole_data_defect: no.
- **Clean-data test.** There is no defect to repair: same-dated prices struck at different times are what the valuation points produce. Repairing every Layer 1 device in the generator leaves the default at 70 and the golden at 60 (asserted).
- **Deletion test.** Delete every distractor and every Layer 1 device and the call still turns on the estimator.
- **Lens swap.** The default and the golden read the same returns, for the same estimand, over the same window. They differ in how a twelve-month variance is estimated from daily data whose co-movement lands a day apart, not in which population or moment they look at.
- **Identity test.** The twelve-month variance is the sum of every lagged covariance across the year's days. No shipped figure closes that identity: there is no portfolio volatility and no run of annual returns.
- **Corpus direction.** Every published figure (the factsheets' single-fund volatilities, the mandate report's own volatility) reproduces under daily and weekly returns alike, so nothing refutes the naive read and nothing files it as policy.

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 battery | 6 linear | Verdict |
|---|---|---|---|---|---|---|---|
| Total returns: the income units' distributions added back, the mandate's flows stripped (time-weighted), corporate actions carried | fires: policy 4.1 and 4.2 (total return, time-weighted) | fires: the movements report's type codes, the price history's distribution column | no | no | fires: flow days are double-digit one-day outliers | no | readable |
| The policy's estimand executed: two years to the 30 November valuation, the step's policy weights in every period, at least 100 equal periods each weighted equally (an exponentially weighted estimate and monthly returns out) | fires: policy 4.2 and 4.3 | no | no | no | no | no | readable |
| The holdings' own prices, not the benchmark indices | fires: policy 4.2 ("the holding's own prices") | fires: the index levels are a separate, named file | no | no | no | no | readable |
| One calendar: UK business days, keeping each overseas fund's price on the noon after its own market's holiday (the last close, moved only by the exchange rate) | no | fires: the calendars file | no | no | fires: small fund returns, the exchange rate alone, on the noon after a US or Japanese holiday | no | readable |
| (decisive) Co-movement measured on returns whose prices are struck together: periods long enough to align the noon dealing prices with the London close (weekly on any anchor), or daily covariances with their one-day lead and lag | no. The policy defines the twelve-month standard deviation and its periods and names no period length. The fund documents state the valuation point as every fund document does. No sentence names a lag, a stale price, a time zone, synchronicity, autocorrelation, a lead-lag or an aggregation | no. The price files carry dates, never times; no column marks a valuation time, and the custodian's price date equals the valuation date on every line | no. The reflexes (an exponentially weighted estimate, shrinkage, a benchmark proxy, more history) leave it in place, and checking each series for autocorrelation comes back clean: the cross-lags show only on the portfolio's series or between holdings | no. The factsheets' single-fund volatilities and the mandate report's own volatility reproduce under daily and weekly returns alike, and no portfolio-level figure ships | no. Every holding prices on every UK business day, every join resolves on the date, and there is no duplicate, gap or fan-out | no. The gap is a sum of lagged cross-covariances across six holdings at each step's weights | silent |

The decisive rung's quantity is named by no sentence and no column. It is not a reflex, no control can see it, the battery comes back clean on the wrong path, and it is not linear in anything reported. Of the two shapes the record says hold, it is the first: a quantity the solver believes needs no construction. The daily covariance looks complete, and nothing in it shows that a large part of the co-movement sits a day off its diagonal.

## Semantic fork table

One row per term of the main ask and per convention the main computation rests on. Paragraph numbers are those of the investment policy (`## Build record` carries the text). The calls under each alternative are measured on the build; `checks.py` computes and asserts each one.

| Id | Term or convention | Golden reading | Alternative reading | Call under the alternative | Ruled out by |
|---|---|---|---|---|---|
| SF1 | growth share | the policy's growth assets (the mandate and the three overseas equity funds) at 40, 30, 15 and 15 per cent of growth, defensive at 55 and 45 | equities at today's drifted split | same call (asserted) | policy 2.1 and 2.2 |
| SF2 | the investment policy's ten-point steps | 20, 30 and so on to 100 | a continuous share (62.9 per cent on the build) | not a step | the prompt ("in the investment policy's ten-point steps") and policy 3.1 |
| SF3 | the largest step that keeps it inside the cap | the highest step whose own volatility is inside the cap | every step up to it inside the cap | same call: the volatility rises with the growth share at every step under every estimator (asserted) | same call |
| SF4 | inside the cap | not more than 10 per cent | strictly under 10 per cent | same call: no golden-family value within 0.15 of 10.0 at any step (asserted) | policy 3.4 ("not more than 10 per cent") |
| SF5 | the comparison with the cap | the estimate before any rounding | each step's volatility rounded to a whole per cent first | 70 for some members (five-day blocks from the fifth day, 10.43, and calendar weeks to Friday, 10.34, round to 10) | policy 4.4 ("before any rounding") |
| SF6 | expected volatility | the standard deviation of the twelve-month total return, estimated as policy 4.2 and 4.3 say | a forward forecast weighting recent periods (exponentially weighted, GARCH) | 80 on the build (90 on the prototype's long run) | policy 4.3 ("every period is weighted equally") |
| SF7 | the two years | the two years to the 30 November 2026 valuation (returns from 2 December 2024) | to 31 October 2026, or the calendar years 2025 and 2026 | same call on the October window (asserted); the calendar years are not in the pack | policy 4.2 ("the last month-end valuation before the review") |
| SF8 | the prices | each holding's own prices: the mandate's closing prices, the funds' dealing prices | the benchmark indices | 70 | policy 4.2 ("the holding's own prices") |
| SF9 | total return | the price change plus the dividends and distributions, time-weighted for the mandate | the income units' price return, distributions left out | same call (asserted) | policy 4.1 and 4.2 |
| SF10 | the weights | the step's policy weights in every period | weights drifting from the window's start | same call (asserted) | policy 4.2 ("in every period") |
| SF11 | the return periods | equal periods that divide the two years, at least 100 of them | overlapping twelve-month returns | 60 on the build (9.43 at 60) and 90 on the prototype sample, refused either way | policy 4.3 ("divided into return periods of equal length") |
| SF12 | the portfolio | both endowments' holdings as one portfolio, the mandate with its cash | one endowment's holdings, or the mandate without its cash | same call for either endowment alone (asserted); without its cash the mandate's purchase and sale days become one-day outliers of up to 43 per cent and the call falls to 40, a gross slip | policy 1.1 and 2.3 |
| SF13 | twelve months from the periods | the variance scaled by the periods in a year (252 daily, 52 weekly) or by the window's own count | 250 or 260 trading days a year | same call (asserted at 250, 252, 253 and 260) | same call |
| SF14 | for 2027 | the share the December 2026 meeting sets for calendar 2027 | the trust's financial year, or the 2026 setting | same call: the trust's year is the calendar year and the estimate uses the same window | policy 3.2 |

The stump is none of these readings. The default and the golden read every term the same way and differ only in how co-movement is measured from asynchronously struck prices.

## Ladder (measured on the build)

The volatility at 60, 70 and 80 per cent growth and the call. "Long run" is 300 years under the prototype's parameters (`protoA10`), kept for reference. "Build" is the shipped pack (world seed 11480, `## Build record`, As built), computed by `checks.py` from `target/` and recomputed by `verify.py`.

| Rung | Construction | Long run 60 / 70 / 80 | Call | Build 60 / 70 / 80 | Call | Killed by |
|---|---|---|---|---|---|---|
| R0 (default) | daily covariance, the square root of 252 | 8.20 / 9.34 / 10.53 | 70 | 8.25 / 9.41 / 10.63 | 70 | same-dated prices struck hours apart; the co-movement a day off the diagonal |
| R1 | exponentially weighted daily (0.94) | 7.02 / 7.94 / 8.91 | 90 | 7.32 / 8.35 / 9.44 | 80 | policy 4.3, every period weighted equally |
| R2 | the benchmark indices, daily | 8.70 / 9.93 / 11.20 | 70 | 8.63 / 9.84 / 11.10 | 70 | policy 4.2, the holdings' own prices (the indices close at their own markets, so they are still asynchronous) |
| R3 | daily, Ledoit-Wolf shrinkage to constant correlation | 8.20 / 9.34 / 10.53 | 70 | 8.24 / 9.39 / 10.60 | 70 | the shrinkage lift (intensity 0.031) is a fraction of the gap |
| R4 | monthly returns | 9.59 / 10.99 / 12.43 | 60 | 9.53 / 10.82 / 12.15 | 60 | policy 4.3, at least 100 periods (24) |
| Partial | two-, three- and four-day returns on every anchor; lead and lag on the UK and North American pair only | 9.02 to 9.30 / 10.30 to 10.64 | 60 | 8.90 to 9.46 / 10.18 to 10.84 | 60 | lands the call (C1); kept at 60 |
| Golden | 26 members: five-day periods on each of five anchors and calendar weeks to each weekday, each from the holdings' period returns and from the daily portfolio compounded; daily with one or two lead-lag terms (the portfolio series and the covariance matrix); Newey-West at four or five lags; daily volatilities with five-day correlations | 9.46 to 9.80 / 10.82 to 11.22 | 60 | 8.96 to 9.72 / 10.33 to 11.11 | 60 | |

**Margins on the build.**
- The golden family's highest value at 60 is 9.72 (five-day periods from the window's first day), 0.28 inside the cap.
- Its lowest value at 70 is 10.33 (calendar weeks to Friday from the daily portfolio), 0.33 over.
- The default sits 0.59 inside at 70 and 0.63 over at 80.
- The thinnest rung margin is R2's: 9.84 at 70, 0.16 inside the cap at its own boundary step.

**Forcing evidence on the build.**
- The portfolio's lag-1 autocorrelation at 60 per cent is 0.177 (t 3.97).
- The same-day correlation of the UK mandate with the North American fund is 0.20, against 0.49 with the next day's fund return and 0.59 between their five-day returns.
- The variance of five-day sums at 60 per cent is 1.35 times five daily variances.
- Every single holding's daily, five-day and monthly volatilities agree within 12 per cent (UK mandate 15.06, 15.94 and 15.46), so no single-series check sees anything.

**Feasibility.**
- `protoA7`: two-year samples meeting every call condition at a 0.10 margin, 27 of 400; at 0.15, 13 of 400, on a smaller golden family.
- The build's scan (`tune.py scan`: every target below on the book at its base size, plus the lot lines' inflation and the mandate's yield in range) passed 3 of the 8,500 seeds from 10000 to 18499: 11480, 14684 and 16914. The golden family's spread is the binding condition: its members sit within 10 per cent of each other on about one sample in five, and the targets leave them about 10 per cent of room at 60 (from about 8.9, where 70 is 10.15, to 9.85).
- `protoA8`: across the golden family the samples spread by a median of 0.88 points at 70 per cent (up to 1.28). That is why no volatility figure is graded (`## Tried and rejected`).

**The builder's targets** (asserted on the built pack by `checks.py`; every one met):
- Every golden-family member at or under 9.85 at 60, and at or over 10.15 at 70: 9.72 and 10.33.
- The default at or under 9.85 at 70, and at or over 10.15 at 80: 9.41 and 10.63.
- The partials at 60: all ten.
- R1, R2 and R3 calling a step other than 60, each at least 0.15 from the cap at its own boundary steps: R1 80 (9.44 and 10.57), R2 70 (9.84 and 11.10), R3 70 (9.39 and 10.60).
- The portfolio's lag-1 autocorrelation at 60 per cent between 0.17 and 0.26, with t at least 3.5: 0.177, t 3.97.
- The same-day UK-to-North-American correlation between 0.20 and 0.35, the next-day correlation at least 0.40, and the weekly at least 0.45: 0.20, 0.49 and 0.59.
- Single holdings' daily, weekly and monthly volatilities within 12 per cent of each other: all six.

**The grid and the Layer 1 slips.** Priced by the builder on the build; none is a rung. Each is computed under the default and under every golden-family member (default call; golden-family calls):
- the mandate's flows left in: 40; 40 (one-day returns of up to 41 per cent; gross);
- the distributions left out: 70; 60;
- the holdings' prices inner-joined with the benchmark index file: no date dropped, so 70 (9.41 at 70); 60. The file carries the custodian's valuation dates, with each index's last close shown on a date it is not calculated (asserted in `checks.py` and `verify.py`);
- the stale-day filter, accepted as a lower rung that policy 4.3 refuses and recorded rather than held off 60 (`## Build record`, As built). Every holding prices on every UK business day, so these are filters a solver chooses from the calendars, not gaps a join leaves:
  - the 46 days on which the North American or Japan fund carries no new close of its market, merged into the next day (420 one-day, 34 two-day, 3 three-day and 2 four-day periods): 60 (10.31 at 70); 50 and 60 at 252 periods a year, and 70 (9.84); 50 and 60 at the merged series' own 229.5 a year;
  - only the calendars' days on which London, New York and Tokyo are all open kept (46 days: Tokyo's 33 as above, and the 13 US holidays themselves in place of the days after them): 60 (10.27); 50 and 60 at 252, and 70 (9.80); 50 and 60 at 229.5;
  - either set of days deleted instead of merged, leaving 459 one-day periods that no longer divide the two years: 70 (9.53 and 9.47); 60 and 70;
  - by market, merged at 252: Tokyo's 33 days alone 60 (10.02), New York's 13 alone 70 (9.69);
- one endowment's sub-account only, either: 70; 60;
- the mandate's cash left out: 40; 30 and 40 (purchase and sale days become one-day outliers of up to 43 per cent; gross);
- the accrued income left out: 70; 60;
- the custodian's fund prices instead of Kestwick's: identical (C1, asserted);
- the demerger uncarried at stock level: 70; 60;
- the accumulation units instead of the income units: 70; 60;
- 250 or 260 periods a year: 70; 60.

None may land the default on 60, and none may move the golden off 60. Two exceptions are allowed. The gross slips land at 50 or below, with outliers a solver sees. The stale-day filter lands the default on 60 at 252 periods a year and splits the golden family. Policy 4.3 refuses it in every form: merged, its periods are not of equal length; deleted, its periods no longer divide the two years. No world holds it off 60 (`## Tried and rejected`).

## Closure table

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | the policy's six holdings across both endowments: the Fernside mandate (its shares and its cash) and the five Kestwick funds; nothing else the trust holds | filed (policy 1.1, 2.1, 2.3); SF12 asserted; C1: the export carries no other account |
| 2 | Unit of account | one return per holding per period; the mandate is one holding (both sub-accounts combined) | filed (policy 2.1); C3: the sub-accounts' mandate returns separately or combined land every golden-family member on 60 (asserted) |
| 3 | Attribution window | a period's return belongs to the period ending on its price date | C1 |
| 4 | As-of dating | the 30 November 2026 valuation, the last month-end before the December meeting | filed (policy 4.2); SF7 |
| 5 | Version basis | the funds' dealing prices as published (no restatement in the window); the custodian's export as run on 2 December 2026 | C1: the custodian's fund prices equal Kestwick's history on every day (asserted) |
| 6 | Divisor and denominator | the sample variance on n minus 1; periods a year from the period length | C3: n or n minus 1, and 250 to 260 days a year, land every member on 60 (asserted) |
| 7 | Weighting | every period equally; the step's policy weights in every period | filed (policy 4.2, 4.3); SF6 and SF10; R1 prices the exponentially weighted estimate |
| 8 | Measurement window length | two years to the valuation | filed (policy 4.2); SF7 |
| 9 | Boundary inclusivity | the cap is met at or under 10.0 | filed (policy 3.4); C4: no step within 0.15 of 10.0 under the default or any golden-family member (asserted) |
| 10 | Rounding path | the estimate compared with the cap before any rounding; pounds rounded once at the end | filed (policy 4.4); the prompt for the pounds |
| 11 | Tie-break | none: the call is the largest step inside the cap | not applicable |
| 12 | Maturity and censoring | every holding is priced on every UK business day of the window, and none is bought into or sold out of within it | C1 (asserted: 505 returns per holding) |
| 13 | Order of operations | the holdings' returns, then the step's portfolio return, then the estimator, then the comparison | C1: combining the returns first and combining the covariances agree (asserted) |
| 14 | Row order | every estimator is order-free | C1 |
| 15 | Duplicate resolution | one price per holding per date; the mandate's lot rows summed to the position | C1: unique keys asserted on the export |
| 16 | Identity normalisation | the custodian's security code, linked to Kestwick's ISINs through the static data file; the demerged and consolidated shares carried through the events file | C1, asserted |
| 17 | Netting against gross | the mandate's external flows stripped (time-weighted); dividends received, trades and the rights subscription are internal movements, not flows | filed (policy 4.2); flows left in is a gross Layer 1 slip |
| 18 | Dimensional units | pounds and per cent throughout; the overseas funds are sterling share classes | C1 |
| 19 | Code and status semantics | the movements report's type codes, the events file's action codes, the price history's unit types (income, accumulation) | filed in the export notes and the workbook's notes; asserted |
| 20 | Integerisation | none | not applicable |
| 21 | Scope of a stated clause | the cap and its definition apply to every step | C1 |
| 22 | Forward window contents | the call sets the growth share for calendar 2027; the estimate uses the two years to 30 November 2026 | filed (policy 3.2, 4.2); SF14 |
| + | Period length | any equal division of the two years into at least 100 periods: daily, two-, three- and four-day, weekly | this is the method, never pinned. Daily alone is R0; every other admissible length converges on 60 (asserted) |
| + | Estimator form | weekly on each anchor; daily plus one or two lead-lag terms; Newey-West at four or five lags; daily volatilities with weekly correlations | C3: every member on 60 with a 0.15 margin (asserted) |
| + | Ask: income basis | ex-dividend dates from 1 December 2025 to 30 November 2026. The mandate is one holding, over its market value with cash in and accrued income out. Each fund is taken per unit over its 30 November price | filed (procedure 7.2, 7.3); a pay-date basis is refused by 7.2's "ex-dividend date" |
| + | Ask: the entitlement's grain | one amount per sub-account, security and event reference | the ask's primary device, never a reading the prompt allows. Forced by the lot quantities (C4): the line-sum reading credits a 600-share lot and a 14,000-share lot of one security with the same dividend |
| + | Ask: grant payments | open instalments of grants awarded by 30 November 2026 and not withdrawn, at the date the trust expects to pay them; euro at 1.1460 | filed (procedure 7.4, 7.5). C3: every lag the 2023 to 2026 project payments show (35 to 70 days, whether median, mean, minimum, maximum or by programme) puts every instalment in the same year. The corridor guarantees it: no project later-instalment falls due between 23 October and 26 November of 2026 or of 2027, and every one due before 23 October 2026 is paid by 30 November (asserted) |
| + | Ask: running costs | the budget workbook's running costs total; fees charged to capital are not running costs | filed (procedure 7.6; policy 5.1) |
| + | Ask: release and title | grant payments plus running costs less each step's income, positive at every step. The title is the highest step whose income is at or above the grant payments | C1: positive at every step on the golden and on every stop, so no floor reading arises. Income falls with the step, and the golden title has at least 2.5 per cent of income on each side (asserted) |

## Literal reader

The prompt and the policy, executed word for word, fix the estimand:
- the population: the policy's six holdings across both endowments, at the policy weights for each step in every period;
- the outcome: the standard deviation of the portfolio's twelve-month total return;
- the window: the two years to the 30 November 2026 valuation;
- the comparison: not more than 10 per cent, before rounding;
- the periods: equal periods dividing the window, at least 100, each weighted equally;
- the steps and the year the share applies to.

No filed sentence names a period length or an estimator. Every literal reading of those terms selects the same returns (C1). The literal text admits daily periods, and daily periods give the default's 70 only through the square-root-of-time scaling, a method the data refutes. The portfolio's daily returns carry a lag-1 autocorrelation of 0.177 at 60 per cent (t 3.97), and the variance of five-day sums is 1.35 times five daily variances at 60 per cent on the build. So the twelve-month standard deviation, which is the filed estimand, is not the daily one times the square root of 252. The design forces the method (`determinism-check` §1, form 1), and the default's 70 comes from a method, not from a reading.

The asks read literally as follows:
- income per procedure 7.2 and 7.3;
- grant payments as the instalments the trust expects to pay in 2027 (7.4), with euro at 7.5's rate;
- running costs as the workbook's total (7.6);
- the release as grant payments plus running costs less income.

Two things are devices the records expose, never readings the prompt allows: the entitlement report's lot lines repeating the position's amount, and the project instalments' due dates being report dates.

## Oracles

- **What ships no figure.** No shipped file states a portfolio volatility at any mix, a covariance or correlation of the holdings, a twelve-month return series, an income figure or yield for the mandate, or a 2027 grant payments total. Nothing ranks or scores the steps.
- **Kestwick's factsheets** (distractor). They carry each fund's own three-year volatility from monthly returns. These are single-fund figures that daily, weekly and monthly returns all reproduce within noise (L7). They rank nothing on the decision.
- **Fernside's quarterly report** (distractor). It carries the mandate's performance and its own volatility against the FTSE All-Share. It is one holding, and it shows no income and no yield.
- **The benchmark index levels** (declared wrong-basis distractor). They file 70 (R2). Policy 4.2 refuses them, and they are themselves struck at different closes. The custodian's report carries them on its valuation dates (London business days). Where an index is not calculated on one of those dates, its last available level is shown, so joining the indices to the holdings drops no date.
- **The 2026 setting** (80 per cent, policy annex). It was last year's decision on a window the pack does not carry, and nothing reproduces it.
- **The operations documents.** Kestwick's key facts and Brackenfold's valuation methodology state the valuation points and the pricing sources, as every fund and custody document does, and draw no consequence for co-movement. `checks.py` sweeps every document for lag, stale, synchron, autocorrel, Dimson, Scholes, Newey, weekly, square root, annualis, time zone and fair value.
- **The asks' one referee: the finance system's grant payment ledger.** It holds the dates and amounts of past payments and no 2027 figure. The spine's lot quantities corroborate the entitlement report's grain and carry no income.
- **The budget workbook.** It leaves the investment income and grants lines to be completed after the December decision and carries only the running costs total.

## Ask sheet

**The main call's declared population.**
- What the call reads:
  - the spine's mandate lots (both sub-accounts) and the mandate's cash lines, every day;
  - the capital movements report;
  - the corporate events file;
  - Kestwick's price and distribution history (and the spine's fund prices, which agree);
  - the calendars;
  - the policy, the fund key facts and the valuation methodology.
- Where the ask devices and hazards live, all outside that population:
  - the income entitlements report (D6, H1, H2);
  - the grants register, the instalment schedule and the payment ledger (D8, H3, H4);
  - the budget workbook and procedure 7.
- Device cells inside the call's population: 0. Hazard cells inside it: 0.
- The asks also read the spine's 30 November rows, for the portfolio's value and the lot quantities, and change none of them.
- `checks.py` asserts the separation by scrambling every ask-only file and column and recomputing the call's figures unchanged at full precision.
- No ask figure moves between the cracker and mirror sheets.

### Ask A: the 2027 investment income at each step (the workbook, and the chart's bars)

| Field | Entry |
|---|---|
| What it asks | For each step from 20 to 100, the income the portfolio would produce in 2027 under procedure 7.2 and 7.3: nine figures, to the nearest thousand pounds |
| Named use | The finance director sets the 2027 income line at the step the trustees choose and shows them what each step gives up in income. H18 home: the other measure the workbook carries for every candidate step (income beside the volatility), computed from rows and columns the call never reads |
| Primary device | D6, grain. The custodian's income entitlements report by tax lot repeats each mandate position's entitlement (sub-account, security, event) on every one of the position's lot lines. There is no allocation, no lot quantity and no rate on the line. Purchases over the years (the legacy money of May 2025 among them) leave 35 of the mandate's 158 dividend events in the twelve months on two lot lines each, so summing the lines puts the mandate's trailing income 43 per cent high: an apparent yield of 5.3 per cent against 3.70, inside the range a UK equity income mandate shows, so no sanity check fires. Fund positions are not lot-tracked and carry one line per sub-account. Silent under the battery: keys are unique on lot and event reference, there are no exact duplicates and no unmatched joins, and no count has to tie. It is visible only at a cross-file cut nothing invites: the spine's lot quantities on the ex-date, where a lot of 5,906 shares and a lot of 23,625 shares in one holding carry the same £2,829.07. The export notes say "one line per tax lot" and "entitlement_gbp: the income entitlement in pounds"; nothing says whose |
| Hazards | H1 (D5, scope): the report runs thirteen months, from 1 November 2025, and procedure 7.2's twelve months drop November 2025's ex-dates. H2 (D1, genuine repeats): the two REITs pay a property income distribution and an ordinary dividend on one ex-date under two event references, and a dedup on sub-account, security and ex-date drops one |
| Stops (measured on the build, pounds against the golden; `figures.json` stops) | s1, the cracker: the lot lines summed, twelve months, the funds per unit; every step high by the lot lines' inflation on the mandate's weight (+42,307 at 20 to +211,535 at 100). s2, lazy: the whole thirteen-month report summed, the funds from their lines too; +409,069 at 20 to +310,286 at 100. o1, over-cleaner: dedup on sub-account, security and ex-date keeping the first line; low by the REITs' ordinary dividend components (-2,723 at 20 to -13,614 at 100), and by their property income distributions keeping the last (-10,775 to -53,873). o2, over-cleaner: dedup on security and event ignoring the sub-account; low by the second endowment's lines (-64,972 to -324,861). s3: the funds' income from their report lines over today's units instead of per unit; -5,506 at 20 to -3,101 at 100, because units changed at the quarterly rebalancings and with the expendable endowment's releases |
| Golden | The mandate: one amount per sub-account, security and event reference, ex-dates from 1 December 2025 to 30 November 2026, over the mandate's market value at 30 November (cash in, accrued income out). Each fund: the distributions per unit over the twelve months, over its 30 November price. Each yield is applied to the step's policy weight of the portfolio's market value (£1,442,000 at 20 falling to £854,000 at 100, on £32,908,401) |
| Span (7 files, 13 columns, causal) | income entitlements report (sub-account, security, event reference, event type, ex-date, entitlement); valuation export (30 November rows: sub-account, security, market value, accrued income, lot quantity for the tell); Kestwick price and distribution history (distribution per unit, ex-date, price); static data (security code, ISIN); the policy (2.1 to 2.3); procedure 7.2 and 7.3; the export notes (which sub-account is which endowment, and which lines are fund positions). That is one file under the span floor of eight. The build adds no eighth: no other file sits on this path without an organ the ask does not need, which would be padding, and the nine releases carry every income figure again through Ask B's eleven |
| Necessity matrix (target, then measured on the build) | One file misread, the rest right. Entitlements summed by line: 9 of 9 (9). The thirteenth month kept: 9 (9). Accrued income in the value: 9 (4: the accrued income at 30 November is £29,574, 0.27 per cent of the mandate, so it moves each income by £249 to £1,035 and five stay in their bins; recorded, not sized, since only a planted accrual would size it). Kestwick's history unread, so the funds are taken from their report lines over today's units: 9 (9). The static file unread, so the funds' ISINs do not link to Kestwick's sheets: 9 (not separate: the custodian's security names carry each fund's name). The policy weights misread: 9 (9). The export notes unread, so a fund's line is taken for a lot line: at least 7 (not separate: fund lines carry no lot) |
| Realism | A custodian's tax-lot income report is built by joining each position's entitlement to the position's tax lots for book-cost reporting. The template carries the position's amount on every lot line, with the lot quantity and the rate in other reports. No one designed it to mislead; a finance team downloads it because it is the one report that lists every dividend |

### Ask B: the capital release at each step, and the 2027 grant payments (the workbook, and the chart's lines)

| Field | Entry |
|---|---|
| What it asks | The 2027 grant payments (one figure), and for each step from 20 to 100 those payments plus the running costs less the step's income (nine figures), to the nearest thousand pounds |
| Named use | The trustees authorise the year's release from the expendable endowment at the step they choose (policy 6.1), and the finance director plans the sales. H18 home: the other measure for every candidate (the capital each step draws), with the grant payments as its audited input |
| Primary device | D8, clock. The grants system schedules a project grant's later instalments on the progress report's due date. The trust pays each one once the grants committee has accepted the report: 35 to 70 days after the due date in every payment from 2023 to 2026. First instalments and core grants' instalments are paid on their due date, and the schedule's due date never moves. So the project instalments falling due from 27 November to 31 December 2026 are paid in January and February 2027, and those falling due in the same weeks of 2027 are paid in 2028 (on the build the due-date year is £38,000 high: £1,298,071 against £1,260,071, more project instalments falling due in late 2027 than in December 2026). Silent: the schedule is complete and carries no condition flag, and the release process is described nowhere in the pack. It is visible only at the cross-file cut of the payment ledger's dates against the schedule's due dates by grant type, which nothing invites, because every payment being forecast is in the future |
| Hazards | H3 (D3, units): the euro grants' instalments carry euro amounts with no currency column; the currency sits on the register and the rate in procedure 7.5 (+£6,179 when taken as pounds). H4 (D2, a stored label before a silent switch): withdrawn grants keep their open instalments as Scheduled, and the withdrawal sits on the register's status (+£43,250). The ask also crosses D6, H1 and H2 through each step's income |
| Stops (measured on the build, pounds) | s1, the cracker: due dates in 2027, the register joined (euro converted, withdrawn out); grant payments £1,298,071 against £1,260,071, and every release off by the £38,000 less the income error, so its releases run from £142,951 at 20 to £561,726 at 100 against the golden's £147,258 to £735,262. s2, lazy: due dates, no register; £1,347,500, and every release off. o3, over-cleaner: the lag applied to every instalment; +£90,000, the core and first instalments falling due in December 2026 counted in 2027. s4: the clock handled but withdrawn grants left in; +£43,250 |
| Golden | The open instalments of grants not withdrawn. Core and first instalments are taken on their due date. Project later instalments are taken on the due date plus any lag the 2023 to 2026 history shows (35 to 70 days; every lag gives the same year, by the corridor). Euro is converted at 1.1460. Add the budget workbook's running costs total, £328,949, then subtract each step's income (£147,000 at 20 to £735,000 at 100, on grant payments of £1,260,000) |
| Span (11 files, 25 columns, causal) | instalment schedule (grant, instalment, due date, amount, status); grants register (grant, programme, type, currency, status, status date); payment ledger (grant, instalment, payment date); budget workbook (running costs total); procedure 7.4 to 7.6; policy 5.1 and 6.1; and Ask A's seven files for the income |
| Necessity matrix (target, then measured on the build) | Payment ledger unread (due dates as payment dates): 10 of 10 (10). Register unread: 10 (10). Procedure 7.5 unread (euro as pounds): 10 (10). The budget workbook's fee lines counted as running costs: 9 (9). Every Ask A file misread: the 9 releases (9 for each, 4 for the accrued income) |
| Realism | A grants system schedules a project grant's later payments on the date its progress report is due, because that is the date in the award letter; the money follows once the committee accepts the report. A withdrawal is recorded on the grant, not on its instalments. A finance system's payment ledger records what was paid and when. Every trust running two systems has this shape |
| Referee | the finance system's payment ledger: dates and amounts of past payments, no 2027 level |

### The chart (`income_cost_by_step_2027.svg`)

- **Graded parts.** One bar per step for its 2027 income (Ask A's figures), a line at the 2027 grant payments, a line at the grant payments plus running costs, and a title naming the highest step whose income still covers the grant payments.
- **Order and title.** The order is the dial's own (20 to 100) and the title is on the ask's own quantity (income against grant payments), never on the volatility.
- **Titles (measured on the build).**
  - Golden: 40 (income at 40 clears the grant payments by £34,690; income at 50 falls £38,810 short).
  - s1: 50.
  - s2: 70.
  - D6 alone: 60.
  - D8 alone: 30 (the due-date reading is high on this grants world), as are o3 and s4.
- **The over-cleaner keeps the title.** o1 shifts income by at most £13,614 and lands on 40, so the title alone does not separate o1. o1 still misses all nine bars and all nine releases.

**Hazard table** (deltas in pounds against the golden, measured on the build and asserted):

| Hazard | Ask A income (nine) | Ask B grant payments | Ask B release (nine) | Chart |
|---|---|---|---|---|
| D6 lot lines summed | +42,307 to +211,535 | 0 | -42,307 to -211,535 | bars; title 60 |
| H1 thirteen months | +8,163 to +40,816 (the mandate's November 2025 dividends) | 0 | -8,163 to -40,816 | bars |
| H2 / o1 REIT pair | -2,723 to -13,614 | 0 | +2,723 to +13,614 | bars |
| D8 due dates | 0 | +38,000 | +38,000 | both lines; title 30 |
| H3 euro as pounds | 0 | +6,179 | +6,179 | both lines |
| H4 withdrawn kept | 0 | +43,250 | +43,250 | both lines; title 30 |
| o3 lag on every instalment | 0 | +90,000 | +90,000 | both lines; title 30 |

**Composed mishandlings.** Every subset of {D6, D8, H1, o1, H3, H4, o3} is computed on both fund routes (D6 and o1 are two handlings of the lot lines, D8 and o3 two clocks), with o1 keeping the last line, o2 and the fee lines alone: 146 combinations (`asks.stop_combos()`). The toy found one inside the bin: H1 with H3 landed the 70 per cent release £463 from the golden. The build re-sized the hazards with `tune_asks.py` (the November 2025 dividends' level, the REITs' distribution split, the mandate's dividend scale, the grants world, the portfolio's size and the running costs total): every combination that moves a figure lands at least £759 from the stated golden (the 90 per cent release, under the thirteen-month report read for the funds too with the lag on every instalment and withdrawn grants kept), asserted at £600.

**Cracker sheet.** The cracker lands the call. It runs the hygiene battery (key uniqueness, duplicates, unmatched joins, fan-out, counts that tie) and executes every filed sentence: procedure 7.2's twelve months (H1 handled), 7.3's market value, 7.5's euro rate (the register joined for currency, so withdrawn grants out, H4 handled) and 7.6's running costs. On the asks it sums the entitlement lines and takes the instalments' due dates: stop s1.

| Ask row | The cracker's computation | What moves it | Cracker verdict |
|---|---|---|---|
| Income, steps 20 to 100 (nine figures) | the mandate's lot lines summed | D6 | miss |
| Release, steps 20 to 100 (nine figures) | s1 income, s1 grant payments | D6 and D8 | miss |
| 2027 grant payments | due dates in 2027 | D8 | miss |
| Chart: the income bars | s1's nine incomes | D6 | miss |
| Chart: the grant payments line | £1,298,071 against £1,260,071 | D8 | miss |
| Chart: the grants plus running costs line | s1's grant payments plus running costs | D8 | miss |
| Chart: the title step | 50 against 40 | D6 and D8, each alone moving it (60 and 30) | miss |

**Mirror sheet.** The same response at R0, the default path, is identical on every ask row (the asks are decoupled), so the two sheets differ only in the call's criterion.

Mirror leakage: 4.4 per cent of the ask weight (at most the one structural chart criterion, 2.4 of 55); the mirror misses every ask figure the cracker misses.

**Pair ceiling:** 34. The arithmetic, at the planning weights 38 / 7 / 55 over 27 criteria (the call; the files and the rounding; 23 ask criteria at about 2.4 each):
- The cracker keeps the call and instruction following (45.0), plus at most a structural chart criterion if the rubric grades one (one bar per step, 2.4): 47.4.
- The mirror keeps instruction following and the same 2.4: 9.4.
- The pair is 28.4.
- At a tenth of the ask weight each (5.5), with 5 of the recommendation surviving on the mirror, it is (50.5 + 17.5) / 2 = 34.0.
- A response that missed the call keeps about 4 to 10 per cent of the ask weight, under the 35 per cent gate, and cracks no ask item.

**What the pass rests on.**
- **The call** holds while no top response sees that a noon dealing price and a London close on the same date are struck hours apart, and so measures co-movement across them. The fund documents state the valuation point (Gate B needs them to), so a reader who connects "last available price at noon" to the previous evening's New York close lands 60. The data's cross-lag correlation is there for anyone who looks between holdings.
- **The asks** hold while no top response checks the lot lines against the lot quantities, or the instalments' due dates against the payment ledger. A response that does both lands all 19 figures and the chart.

## Prompt

`prompt.txt`, 700 characters, one paragraph, question first ("What is", the call in the first sentence), two files named, and the rounding stated once at the close. `voice-check.py task135` passes on every rule.
- It names no person, title, meeting or reader, no input file, no method and no trap word.
- Its only forcing facts are the year and the policy's steps.
- The chart is on the ask's own quantity, never on the call's.
- The volatility figure at the step above the call and the cost-by-step ask were dropped at design (`## Tried and rejected`).

## Build record

**The builder's brief.** A builder (Opus, medium) executes this design from this commit. It cuts the data, writes the generator and the goldens, and returns to a designer if a target below cannot be met without changing the ladder. Architecture 1's build products were removed from the folder at the re-root and stay in git history: `generator/`, `golden/`, `target/`, `target.zip`, `submission.md`, `metadata.json`, `leak_check_report.md`. The generator is written fresh.

**What the generator builds** (`task135/generator/`).
- `world.py`:
  - the dates: prices from 29 November 2024 to 30 November 2026; UK, US and Japanese calendars and holidays; the UK and US daylight-saving dates; the valuation of 30 November 2026; the export run of 2 December 2026; the meeting of 10 December 2026;
  - the mandate: about 32 UK shares across the two endowments' sub-accounts, two of them REITs;
  - the five Kestwick funds, each with charity income and accumulation units;
  - the policy's weights, steps and the 2026 setting (80 per cent);
  - the corporate events;
  - the mandate's external flows: a legacy added to the permanent endowment in 2025, and the quarterly rebalancing transfers;
  - the grants world: about 140 grants in two programmes, core and project, a few in euro, a few withdrawn in 2025 and 2026;
  - the budget's running costs (a total near 344,000 pounds, not round);
  - the seeds.
- `sim.py`: the hourly shock model of `protoA6`.
  - Shocks: a global factor with an intraday news profile heavier in US hours, regional factors on their own hours, rates and credit, and a sterling exchange-rate factor that enters the overseas funds' prices at the noon rate.
  - Each holding is struck at its own point:
    - the mandate's shares at the London close (16:30);
    - every Kestwick fund at 12:00 noon from each market's last available price (the North American fund at the previous New York close, Europe live, Japan at the same day's Tokyo close, gilts and credit live).
  - The mandate also gets:
    - stock-level prices with idiosyncratic moves around the UK factor;
    - dividends with ex and pay dates, including the two REITs' paired components.
  - The funds' distributions: quarterly for the bond funds, half-yearly for the equity funds.
- `tune.py` and `tune_asks.py`: the seed scan (`tune.py scan`) and a light polish to `## Ladder`'s targets (each market's month-on-month moves re-scaled so every holding's monthly volatility sits between its daily and five-day ones), then the asks' targets: the title margins, the hazard sizes and the corridor (`tune_asks.py`).
- `observe.py`: what the systems hold.
  - The custodian's daily lot-level valuation export (both sub-accounts; lot open dates and quantities; closing or dealing price; market value; accrued income; the mandate's cash lines).
  - The capital movements report and the corporate events file.
  - The income entitlements report by tax lot (thirteen months, the position's entitlement on every mandate lot line, fund positions one line per sub-account).
  - The static data file, Kestwick's price and distribution history workbook, and the calendars.
  - The grants register and instalment schedule at 30 November 2026 (UK date format, as the grants system writes it).
  - The finance system's payment ledger from January 2023.
  - The budget workbook.
- `docs.py` and `files.py`: the documents and the pack.
- `golden.py`: the two deliverables.
- `checks.py`; `verify.py` (independent, reading only `target/`); `figures.json`.

**The pack (planned: 18 files, 5 formats, 3 distractors).**

| File | Role | Key columns or content |
|---|---|---|
| `brackenfold_valuation_lots_2024-11_2026-11.csv` | the spine: the custodian's daily valuation at tax-lot grain, about 70,000 rows (call; asks read 30 November) | valuation_date, sub_account, security_code, security_name, lot_id, lot_open_date, quantity, price, market_value_gbp, accrued_income_gbp, asset_class |
| `brackenfold_capital_movements_2024-12_2026-11.csv` | the mandate's external flows (call) | date, sub_account, movement_type, amount_gbp, narrative |
| `brackenfold_corporate_events_2024-12_2026-11.csv` | consolidation, demerger, rights issue, takeover (call) | event_ref, security_code, action_type, ex_date, effective_date, terms, new_security_code |
| `brackenfold_income_entitlements_by_lot_2025-11_2026-11.csv` | the income report (Ask A) | sub_account, security_code, event_ref, event_type, ex_date, pay_date, lot_id, lot_open_date, entitlement_gbp |
| `brackenfold_static_data_2026-12-02.csv` | security codes, ISINs, names, asset class (call, asks) | security_code, isin, name, asset_class, listing |
| `brackenfold_export_notes_2026-12-02.txt` | the cover note: field descriptions, codes, the valuation methodology's pricing sources | the sentences below |
| `kestwick_charity_funds_prices_2024-11_2026-11.xlsx` | Kestwick's dealing prices and distributions, one sheet per fund (call, Ask A, the referee for the funds) | date, income unit price, accumulation unit price, ex-dividend flag, distribution per income unit |
| `kestwick_charity_funds_key_facts_2026.pdf` | the five funds' key facts: objective, units, charges, dealing and valuation | the valuation sentences below |
| `market_calendars_2024-2027.csv` | UK, US and Japanese business days and holidays | date, market, is_business_day, holiday_name |
| `wrexford_investment_policy_2025-12.pdf` | the estimand, at authority | the paragraphs below |
| `wrexford_finance_procedure_07_budget_2026-10.docx` | the asks' estimand | the paragraphs below |
| `wrexford_budget_2027_draft_2026-11-24.xlsx` | the budget: running costs, lines to complete (Ask B) | sheets Summary and Running costs |
| `wrexford_grants_register_2026-11-30.csv` | the grant header (Ask B) | grant_ref, grantee, programme, grant_type, award_date, currency, award_amount, status, status_date |
| `wrexford_grant_instalments_2026-11-30.csv` | the schedule (Ask B) | grant_ref, instalment_no, due_date, amount, status |
| `wrexford_grant_payments_2023-01_2026-11.csv` | the finance system's ledger (Ask B, the referee) | payment_ref, payment_date, grant_ref, instalment_no, currency, amount, amount_gbp |
| `benchmark_index_levels_2024-11_2026-11.csv` | distractor, declared wrong basis: Brackenfold's performance-measurement report | a header block (closing levels at each valuation date, London business days, with the last available level where an index is not calculated), then date, index_name, close |
| `kestwick_factsheets_2026-10.pdf` and `fernside_quarterly_report_2026-q3.pdf` | distractors | single-fund three-year volatility from monthly returns, top holdings; the mandate's performance and own risk statistics, no income or yield |

**The documents' load-bearing sentences** (verbatim in the documents; `checks.py` asserts each SF row's quoted text is present).

Investment policy (approved 9 December 2025):
- 1.1 The trust invests its permanent and expendable endowments as one portfolio under this policy.
- 2.1 Growth assets are the segregated UK equity portfolio managed by Fernside Partners (the mandate) and the Kestwick North American, European and Japan Equity Funds for Charities; defensive assets are the Kestwick Gilt Fund for Charities and the Kestwick Sterling Corporate Bond Fund for Charities.
- 2.2 Within growth assets the weights are 40 per cent the mandate, 30 per cent North American, 15 per cent European and 15 per cent Japan; within defensive assets, 55 per cent gilts and 45 per cent corporate bonds.
- 2.3 The mandate includes the cash its manager holds in it.
- 3.1 The trustees set the growth share in ten-point steps from 20 to 100 per cent.
- 3.2 At their December meeting the trustees set the growth share for the following calendar year.
- 3.3 The portfolio is rebalanced to the policy weights at each quarter end.
- 3.4 The portfolio's expected volatility at the growth share set must be not more than 10 per cent.
- 4.1 Expected volatility is the standard deviation of the portfolio's total return over twelve months.
- 4.2 It is estimated from the time-weighted total returns of the policy's holdings, each measured from the holding's own prices and the income it pays, over the two years to the last month-end valuation before the review, combined in every period at the policy weights for the growth share under review.
- 4.3 The two years are divided into return periods of equal length, at least 100 of them, and every period is weighted equally.
- 4.4 The estimate is compared with the cap before any rounding.
- 5.1 Investment management and custody fees are charged to the capital of the endowments.
- 6.1 The trustees may release capital from the expendable endowment to meet grant payments and running costs that income does not cover.
- Annex: the growth share for 2026 is 80 per cent.

Finance procedure 7 (revised October 2026):
- 7.1 The budget year is the calendar year.
- 7.2 Investment income for the budget year is estimated from the last month-end valuation before the trustees' December meeting. For the Fernside mandate, it is the mandate's dividends and distributions with an ex-dividend date in the twelve months to the valuation date, as a share of the mandate's market value at that date. For each Kestwick fund, it is the distributions per unit with an ex-dividend date in those twelve months, as a share of the fund's price at that date. Each share is applied to the value that the policy weights for the growth share under review place in the holding, the portfolio taken at its market value at the valuation date.
- 7.3 Market value excludes income accrued but not yet received.
- 7.4 Grant payments for the budget year are the instalments of grants awarded by the date of the budget that the trust expects to pay in the year; grants awarded during the year are budgeted under the new awards line.
- 7.5 Grant payments in euro are budgeted at 1.1460 euro to the pound.
- 7.6 Running costs are the budget workbook's running costs total; investment management and custody fees are charged to capital (investment policy 5.1) and are not running costs.

Kestwick key facts, each fund: "Dealing: daily at 12 noon UK time, the fund's valuation point. Investments are valued at their latest available prices at the valuation point." Brackenfold's export notes: "Listed securities are valued at the official closing price of their primary exchange. Units in collective investment schemes are valued at the latest dealing price published by the manager." The notes' field line for the income report reads "One line per tax lot. entitlement_gbp: the income entitlement in pounds." No document says how a figure is estimated, what a lot line's amount covers, or when a grant instalment is paid.

**What `checks.py` asserts.**
- Every semantic fork row, SF1 to SF14: the alternative is computed from the shipped files and its call recorded, and it is either the golden call or refused by the quoted sentence, which is present in the named document.
- The ladder:
  - R0 at 70 with its margins;
  - every golden-family member at 60 with its margins;
  - the partials at 60;
  - R1, R2 and R3 calling a step other than 60 with margins;
  - R4 refused (24 periods);
  - every target in `## Ladder`, including the forcing statistics and the single-holding agreement.
- The Layer 1 grid: every slip on the default and on every golden-family member, with none landing the default on 60, and none moving the golden off 60 except the gross slips (at 40 or below, with outliers).
  - The stale-day filter is the accepted exception (As built), in both forms: the post-holiday days merged, and only the calendars' common days kept. Asserted instead: its refusal by policy 4.3 (merged, periods of unequal length; deleted, periods that no longer divide the two years) and the default's 70 at the merged series' own count of periods a year.
  - An inner join of the holdings' prices with the benchmark index file keeps all 506 dates and gives the default's 70, asserted again in `verify.py`.
- The clean-data test, the lens-swap test and the separation count (zero device and hazard cells in the call's population; scrambling the ask-only files leaves the call's figures unchanged at full precision).
- The asks:
  - every stop in the ask sheet, its value and its distance from the golden bin;
  - every hazard delta, and every composed subset outside 600 pounds of the golden;
  - the title under each stop;
  - the corridor: no project later-instalment due in the two corridors, and every lag from 35 to 70 days gives the same year for every instalment;
  - the necessity matrix;
  - the cracker and mirror sheets;
  - every golden figure at least 100 pounds inside its bin, and every release rounding the same way from rounded parts (measured: at most 262 pounds from its stated thousand);
  - the release positive at every step;
  - the title margins at least 2.5 per cent of income on each side.
- The documents:
  - none carries lag, stale, synchron, asynchron, autocorrel, Dimson, Scholes, Newey, weekly, square root, annualis, time zone or fair value;
  - no file carries a portfolio volatility, a correlation of the holdings, a mandate income or yield, or a 2027 grant payments total.
- The input gates (18 files, 5 formats, the spine at 25,000 rows or more, three distractors in `metadata.json`) and two consecutive builds byte-identical.

**What `figures.json` carries.**
- The call.
- Each step's volatility under R0 to R4, the partials and every golden-family member, and the forcing statistics.
- The portfolio's value at 30 November and each holding's twelve-month yield.
- The nine incomes and nine releases, unrounded and as stated.
- The grant payments with their parts (core and first instalments; project later instalments by year of payment; euro; withdrawn excluded).
- The running costs and the title step.
- Every stop value in the ask sheet.

**The realism sweep.**
- No identical counts across periods.
- No round headline totals: the portfolio value, the grant payments, the running costs and the incomes.
- No constant monthly streams, and no reused free-text narratives on movements or grants.
- Names from `guard.py names`.
- Every container carries the fiction's authors, dates and the software that made it: Brackenfold's report generator, Kestwick's website export, the trust's Word and Excel.
- The custodian's export keeps its own column naming. The grants system writes UK dates and the finance system ISO dates, each said in its export's notes.
- Fernside's report and the factsheets read as their genre: a fund factsheet's layout, and a manager's quarterly letter with a performance table.

**Seeds and records.** The prototype (scratch `t135-arch2/`, never shipped) used seed 5 for the long run and seeds 2036 and 2038 for two-year samples. Seed 2038 fails the builder's targets (R1 and R2 land on 60), which is why R1 to R3 are in the conditions. The builder picks its world seed and records it here with the measured ladder, which replaces the prototype figures in `## Default path`, `## Stump sentence` and `## Ladder`. The build's world is market seed 11480 (As built, below); the figures in `## Default path`, `## Three rules`, `## Semantic fork table`, `## Ladder` and `## Ask sheet` are the build's.

**Stopping rule.**
- A round in which the solver lands 60 by synchronising (any member of the golden family) sends the build back to the designer, with a brief naming the step that saw the asynchrony. This is loop 1 of 3 for this architecture.
- A round in which it misses the call and keeps 35 per cent or more of the ask weight sends the build to the ask layer.
- Three loops landed on the call re-root to architecture 3.

### As built (stage 3, 2026-10-12)

The builder, stopped mid-stage 3, left a generator whose world (seed 2109) missed the golden family's margins and the exponentially weighted rung's, with the ask layer untuned (`## Tried and rejected`). This session finished the stage on that generator without changing the ladder, the stump, the prompt or the asks.

**The world.** Market seed 11480 (the scan's first full pass); book seed 1352. The book at a base value of £30,553,605.90 at the window's start (the legacy scaled with it), so the portfolio is worth £32,908,401 at 30 November 2026. Book knobs for the asks, the call's targets checked again on the book they make: the November 2025 dividends' level 0.9899, the REITs' property income share shifted by 0.0185, the mandate's dividend scale 0.74 (a 3.70 per cent yield). Grants world 2477 at scale 1.2. Running costs £328,949 (the draft's staff salaries line carries the adjustment). `world.py` records all of it.

**The generator** (`task135/generator/`): `world.py` (calendars, holdings, policy, the mandate's shares, corporate events, the legacy, the expendable endowment's quarterly releases, the grants world's names, the budget lines, the chosen world); `sim.py` (the half-hourly market and the funds' prices and distributions); `book.py` (the custodian's book); `tune.py` (the polish, the call's conditions and the seed scan); `tune_asks.py` (the ask layer's solve and its exact check); `grants.py`; `observe.py`, `files.py`, `docs.py`, `officex.py` and `postprocess.py` (the extracts, the documents and their containers); `estimators.py`, `callcalc.py`, `ladder.py`, `asks.py` and `load.py` (the computations on the shipped files); `build.py`, `golden.py`, `checks.py` and `verify.py`. A build takes about eight seconds and `checks.py` about ten.

**The pack.** 18 files in five formats (csv, docx, pdf, txt, xlsx); the spine `brackenfold_valuation_lots_2024-11_2026-11.csv` at 42,894 rows; three distractors in `metadata.json` (the benchmark index levels, the declared wrong basis; Kestwick's factsheets; Fernside's quarterly report).

**Free gates, on the final build.**
- `checks.py`: 281 assertions, 0 failed (every SF row with its quoted sentence present once, the ladder, the golden family's 26 members and the ten partials, the grid with the stale-day filter's refusal and the index-file join, the clean-data, lens-swap, separation and distractor-deletion tests, the asks' bins, title, corridor, the 146 composed mishandlings, the cracker sheet and necessity matrix, the cited clauses, the documents' vocabulary and the realism sweep).
- `verify.py` (reads only `target/`, imports nothing from the generator): the 505 returns per holding, the default's 70 and R0 at every step, the one-day lead-lag, Newey-West, Friday-week and five-day members' 60 with their values at 60 and 70, the portfolio's value, the running costs, the grant payments with the payment ledger's median lag, the nine incomes, the nine releases, the chart's title step, and the inner join of every price file with the index file (506 of 506 dates, the default's 70): 0 failed.
- Two consecutive builds byte-identical, file by file and `target.zip` (sha256 550f976258b084f0e1d055571c322cee3bcf25160c8ba482df7a3364a9f67330); `golden.py` twice gives byte-identical goldens, unchanged by the holiday repair.
- `figures_check.py`: 92 figures in blocks 1 to 4, 0 absent.
- `scrub_producer_metadata.py` audit: `target/` and `golden/` clean.
- `leak.py --asof 2026-12-02`: REVIEW, no LEAK; every line answered below.
- `guard.py surface`: exit 0, no pair promoted; the personas in the pack (Connor Wells, Harriet Clarke, Lawrence Barnes) are on the card.
- `guard.py heart`: WARN on repeat.gate_g against task134 v2 (answered in `## Draw`); nearest driver 0.06 (task128), nearest stump 0.05 (task111).
- `guard.py validate`: 145 cards, 0 invalid. `precut.py`: exit 0, 38 checks, 0 FAIL, 0 WARN; `voice-check.py` PASS.

**The holiday slips, resolved at stage 3 (2026-10-12).** `## Ladder`'s grid wants no Layer 1 slip to land the default on 60, and the post-holiday slip did at 252 periods a year.
- **What the pack already did.** Every holding already priced on every UK business day: the Kestwick funds deal daily at noon, and on a US or Japanese holiday the fund carries that market's last close. So an inner join of the holdings' prices drops nothing.
- **The two routes that landed 60:**
  - an inner join with the benchmark index file. Its S&P 500 (501 dates) and TOPIX (485) ran on their own markets' days, so the join dropped 46 dates: 10.27 at 70 at 252 periods a year, 9.80 at the series' own 229.5;
  - the stale-day filter, a solver's own choice from the calendars (the grid's figures).
- **The index file, changed.** It now carries the custodian's valuation dates, with the last available level shown where an index is not calculated, and its header block says so.
  - Against the previous build: 2,990 levels unchanged, 46 carried levels added (13 S&P 500, 33 TOPIX), and 20 levels on UK holidays gone.
  - R2 is unchanged to the last digit, because the ladder already read the indices forward-filled onto UK dates, and every other file is byte-identical.
  - The inner join now keeps all 506 dates and gives the default's 70, asserted in `checks.py` and `verify.py`.
- **The stale-day filter, accepted** as a lower rung that policy 4.3 refuses, with its figures in the grid.
  - It is off the default path, whose step 3 keeps those days.
  - No world holds it off 60 (`## Tried and rejected`). Of the scan's 202 samples whose golden family met its margins, it landed the default on 60 on 144. It held on 4 (10451, 11091, 11572 and 17062), none of which meets the other targets, and it fails on all 6 samples meeting every call target.
  - `market_calendars_2024-2027.csv` stays as Layer 1.

**Other measured departures from the design's figures.**
- The lot lines inflate the mandate's twelve-month income by 43 per cent (design: about 36): an apparent yield of 5.3 per cent against 3.70.
- The due-date reading of the grant payments is high on the chosen grants world (+£38,000) where the design's toy had it low; the device works either way (s1 and D8 alone miss the grant payments, every release and the title).
- The accrued income moves 4 of the 9 incomes past their bins (target 9); 7.3's sentence stays and no accrual is planted to size it.
- Ask A's span stays at seven files (`## Ask sheet`).
- SF11's overlapping twelve-month returns call 60 on the build (90 on the prototype); policy 4.3 refuses them either way.

**Layer 1 added at the build** (no graded figure depends on it): the trustees' quarterly releases of capital from the expendable endowment (0.87 to 1.31 per cent of its value each quarter from March 2025), drawn across its holdings at the quarter-end rebalancing, so the expendable endowment's fund units fall between distribution dates and its mandate withdrawals carry its share; new money spread so that no purchase is much over 4 per cent of the designation's mandate; the Fernside report's benchmark as a total return, and its letter's account of the takeover cash read from the book; at the holiday repair, the benchmark index levels on the custodian's valuation dates, under its performance-measurement report's header block.

**Leak review lines** (`leak.py`, each harmless):
- the policy's paragraph number 4.3 matches a figure the write-up cites (a clause, not an answer);
- the policy carries 7 of 11 words of the committed call: the decision's own vocabulary (growth share, the policy's steps, expected volatility, the cap);
- the export notes (design, valuation, market, holding), Fernside's report (returns, report, holding), the key facts (returns, prices, valuation), procedure 7 (mandate, valuation, market, holding) and the policy (design, returns, prices, measured, mandate, valuation) carry generic stump-paragraph words; none names a period length, a lag or an estimator;
- dates after 2 December 2026: the income report's pay dates for dividends that went ex by 30 November, and the market calendars through 2027, forward-looking by nature.

## Tried and rejected

- Seed FC06 kept in substance (four scheduled lock closures; grain the river terminals cannot store goes by rail, the per-terminal storage floor summed): rejected at the draw.
  - The guard blocked it on `test.same_puzzle`: population gap, pattern D and a quantity decision are spent in 14 builds.
  - Its decisive move, a sum of per-site shortfalls each floored at zero because surpluses cannot transfer, is task16's driver.
  - Moving the stump onto which pools a closure cuts off, or onto the back-to-back closure spell, would leave a lesser device carrying it.
- A sediment-removal plan for an existing reservoir after a dam safety inspection: rejected at the draw. An existing forebay or reservoir carries its own deposition history (earlier cleanout quantities, earlier surveys), which is a control a solver could calibrate on instead of estimating the load. A new forebay at design has none.
- A Newton step on the lab values against every constraint at once: diverged, because the seasonal variants are nearly collinear and the big-sample subset ill-conditioned; replaced by coefficient constraints solved continuously on the full sample, then floor and ceiling flips with pair moves.
- Polishing lab values in absolute mg/L with sequential rounding: moved small results by up to 1,150 per cent; the polish now works in relative (log) terms.
- Constraining only the alternative specifications' effect on the total: class-level effects of 3.8 tons survived; the polish constrains the coefficients, with tolerances derived from each figure's lever.
- Sample seeds 101 and 32: Elk Draw's MVUE total sat 35.0 tons off the smearing total, half a rounding unit, so no placement could centre both; a seed scan found 325 and 76.
- Placement by single greedy moves: stalled at objective 0.314 after 342 moves; replaced by planned targets per class, an achieve step and a short greedy finish.
- Elk Draw bypass at 8.0 cfs: the Class V day counts needed 629 placement moves; 8.5 cfs needs few.
- Requiring R7 (grabs and replicates kept) on its own forebay figure: no trapping efficiency and density met it, because the rung is mess-neutral by design; it is exempt from the distinct-bin assertion.
- "Trap efficiency" as the design report's term: `leak.py` reads "trap" as author vocabulary; the pack says "trapping efficiency" throughout.
- Leaving the rounding path to the reader: at tens and one decimal the concentrations from the rounded loads (5,820.9 and 296.3) against the unrounded (5,823.1 and 296.5) were a fork; guidance section 6 now says to carry full precision.
- The memo with a full-size chart: the class table spilled to page 2; the chart is 6.1 inches wide and the table compact, so the chart, table, source line and footnote sit on page 1.
- Colorado PE licence numbers in the design report's and the geotechnical memo's signature blocks: dropped, because an invented number in the live range can belong to a real licensee.
- No constraint on a time trend: Bitterbrush's trend term came out at t 1.47 (Elk Draw −1.14), enough for an AIC model search to keep it, and a 2011 to 2026 trend carried back to 1951 moves the creek's load by a fifth; the polish now holds |t| under 0.4. That re-tune moved the figures of the day (Elk Draw 4,460 to 4,340 tons, density 73 to 72 pcf) and left the forebay at 28,000.
- Leaving same-day samples unpinned: collapsing a storm day's samples to one value moves the forebay to 28,538.1 (29,000); the notes now say a second set counts as a sample of its own.
- Checking the invented gauge number and case number against the real registers: the proxy refused the lookup, so 06756890 and 18CW3192 are unverified against the live USGS and court indexes.
- Tons to the nearest ten and concentrations to one decimal: the MVUE ran 0.5 per cent under smearing on Elk Draw (20 tons, two rounding units), so six figures rounded apart whatever the placement; the prompt now asks for two significant figures and all five corrections agree.
- Re-centring at two significant figures by flow placement alone: with a creek's diverted volume fixed, its concentration is its load over a constant, so Bitterbrush's tons and concentration bins could not both be met near the old load; the level stage now moves each rating's level and slope first.
- Level targets in the polish with only the largest results free after its first round: Bitterbrush's residual variance rose from 0.14 to 0.88 and its smearing factor to 1.55; every value now stays free in every round.
- The first polish freeing only the largest results in its later rounds: it turned the Elk Draw rating about the high flows (slope 1.449 to 1.485, the load up by a fifth); the polish now holds the intercept and slope where the samples put them.
- Trapping efficiency 0.73 with density 70 pcf: the volume sat at 29,099, high in its 29,000 bin, and the box coefficient applied twice (+1.5 per cent) moved it to 30,000; the design step now aims the total so the smearing volume sits in the lower 55 per cent of its bin (27,903 at 73 pcf).
- Architecture 1, the rating curve's retransformation as the decisive step: spent on paper at the precut retrofit (2026-10-11), before any precut repair, because the honest default path ends on the golden.
  - The default path the measured opponent builds unsteered: (1) guidance 2.1 to 2.5 executed as written, the design load the long-term average annual load, day by day over the full record, each day's concentration estimated from samples paired with the day's mean discharge; (2) the samples kept by the notes' rule, every N sample by EWI or PUMP (238 Elk Draw, 218 Bitterbrush); (3) a rating per creek, least squares of ln SSC on ln Q (slopes 1.416 and 1.315, residual standard deviation 0.769 and 0.380); (4) the field's retransformation correction, because the design load is an average and the exponentiated fit is the median (Duan's smearing 1.344 and 1.075, or Ferguson's exp(s²/2), the same factors); (5) the rating on every day's creek flow, times the decree's diversion, times 0.0027, over 76 water years (Elk Draw 4,412.5 tons, Bitterbrush 3,121.4), times 0.73, five years, 73 pcf: 27,903.3 cubic yards. Ends on 28,000, the golden.
  - Why step 4 is the default and not an extra correction: it is the textbook construction of a load from a log-log rating (Ferguson 1986, Duan 1983, Cohn et al. 1989, Helsel and Hirsch; USGS LOADEST corrects by default and the USGS surrogate-regression guidance reports Duan's factor with every sediment model), and this note's own Three rules line called it "the field's own practice". The opponent does the default construction well and corrects by reflex (`stumping` Part 0, traits 3 and 7; task134 loop 0 and task130 v3 landed that way). No round measured it, and none is owed: a rung that bites only a solver who omits the field's standard step is not on the default path (Part 1.5).
  - Measured from `target/` alone with a scratch script independent of the generator: no correction 22,919.7 (23,000); smearing 27,903.3; lognormal on n − 2 27,903.3; lognormal on n 27,855.1; MVUE 27,818.1 (the generator's series; an independent series gives 27,794.4); a log10 fit with Ferguson's matching factor exp(2.651 s²) 27,903.3. All five file 28,000. Only two slips land elsewhere: the log10 unit slip, exp(s²/2) on the log10 variance, 23,763.8 (24,000), and a ratio-of-means factor from the samples (1.678 and 1.103) 32,277.9 (32,000).
  - Readability screen on the decisive rung (no correction, 23,000): filed sentence no (no shipped text names a log, a median or a factor); schema no; reflex correction YES (retransforming a log-scale regression summed to a mean is a textbook reflex, in sediment work above all); control bench YES (the samples are the only calibration data and the opponent back-tests the rating on them: the uncorrected line has 52.1 and 50.0 per cent of the samples above it and its mean on the sample days is 1/1.678 of the observed mean on Elk Draw and 1/1.103 on Bitterbrush, so the shortfall accumulates and the samples refute the naive read, failing the corpus-direction test); hygiene battery no; linear arithmetic no (one computed scalar per creek). Verdict: readable.
  - Analyst test: the class is analytical, since a strong analyst who cleaned the samples and read every rule can still file 23,000 by exponentiating the fit; but here the easy way is not the strong analyst's way, because the correction is the field's default, so 23,000 is a slip and not the default path.
  - No hardening inside the architecture saves it. The estimand has to be filed literally as an average (`determinism-check` §1), and the filed average is the cue for the correction; deleting it opens a median-against-mean fork on the main call (`stumping` Part 2.2). A flow-dependent residual spread, so that one smearing factor misses, keeps the same driver and is surfaced by the re-screen-the-residual reflex (residuals plotted against flow). The decisive generator was G17, which the mechanism table now marks supporting only.
- The ask layer as built (26 graded figures) fails today's ask gate on its own, whatever happens to the call: the 15 tonnage, concentration and tons-kept figures are splits of the call's own corrected construction (`supplemental-stumping` Part 1.2, ban 4), so the cracker sheet hits all 26; the ten day counts are the decree executed on the record, which every response hits, so the response at the uncorrected stop keeps 10 of the 24 ask criteria (the class tons, class days, concentrations and the two memo items), about 42 per cent of the ask weight and over the 35 per cent gate, and cracks those items (`grade.py` exit 3). One-cracker pair at the planning weights: C = 38 + 7 + 55 = 100, S about 5 + 7 + 55 × 0.42 = 35, pair about 67 against the ceiling of 40. The re-root designs its asks against the cracker sheet from the start.
- Architecture 2's draw, candidate A: every holding a noon-priced pooled fund, the North American fund at the previous New York close, no London-close mandate. Set aside at the draw.
  - Measured (`protoA_async.py`): the daily estimate was about 11 per cent low (9.53 against a true 10.70 at 70 per cent growth).
  - The portfolio's lag-1 autocorrelation was only 0.09, t of about 2 on two years. That is too weak to force the method on the data's own evidence, and too thin to keep every synchronous estimator on one ten-point step.
  - Adding the London-close segregated mandate (`protoA5` onward) widened the striking-time spread to 16:30 against the previous evening's 21:00 and lifted the autocorrelation past 0.17.
- Candidate S: blocked simulator practice lifting in-training grades and lowering retention at a later checkride, with failures forecast for a cohort trained entirely under block booking. Rejected at the draw.
  - Its decisive step is a conditioned yield (G14 with G9), which the guard bans against task134 and task133. Recoding it under another label to dodge the ban would be a card written to pass.
  - Measured (`protoS_spacing.py`): the grade-only model expects 24.6 failures in the 128-trainee cohort, the model with the practice schedule 80.2, against a simulated 70.
- An average-wait forecast from bus headways (the inspection paradox): set aside on paper. The length-biased correction is a textbook step a strong analyst applies by reflex, which is architecture 1's death in another costume.
- Initial stock from a fishery's declining catch per unit effort (Leslie depletion): set aside on paper. The field's textbook regression is the default construction and the golden, and any wrong step would need a planted change in catchability.
- A moving Easter in a monthly demand forecast: set aside on paper. The calendar regressor is a reflex in official-statistics practice, and the decisive step would read as calendar semantics.
- Repeated screening rounds (prevalent against incident yield): set aside on paper as task446's move, method selection over a round's yield.
- A pooled rate hiding a matching or herd effect: set aside on paper. Holding the pool to a visible attribute is the reflex correction that task230 landed on twice.
- A time-on-task fatigue forecast, and an experience-curve cost forecast: set aside on paper.
  - The time-on-task covariate is a reflex control.
  - The experience curve's log-log fit is the default and the golden, and any wrong step in it is a retransformation (architecture 1) or a field reading.
- This architecture's card with G13 decisive (the horizon) or G16 decisive (method selection): blocked by `guard.py check` on `test.same_driver_older`, against task229 v2 and task446 v2 respectively. The decisive generator is G7 (when each price is struck), with G2 and G17 supporting, which is also what the step is.
- A graded volatility figure (the expected volatility at the step above the call, to the nearest whole per cent): dropped at design.
  - Across the golden family (lead-lag, Newey-West at four or five lags, weekly on each anchor, daily volatilities with weekly correlations), two-year samples spread by a median of 0.88 points at 70 per cent, and up to 1.28 (`protoA8`).
  - The figure pinned in one bin with margin on 6 of 1,000 seeds, so it would have been a fork.
  - Only the call is graded on the volatility.
- A cost-by-step ask: dropped at design. It covered the manager's tiered fee, the pooled funds' charges net of a charity-class rebate paid in units, and a superseded fee schedule beside the invoices.
  - Each cost device is adjudicated by a document the cost work reads anyway (the fee letter or the invoices, the rebate receipts' own labels), so the cracker sheet hits it.
  - The rebate's booking, as a cost reduction or as income, is an ask-level fork that only a sentence naming the rebate could close.
  - The card's layer1 lines for the rebate and the superseded schedule drop at the final card update.
- 2027 grant payments by programme and quarter as an ask: dropped at design.
  - It is a cash plan a person could act on with the call unmade (H18), and the quarter edges would multiply the clock corridors.
  - The year's total is graded as the release's input instead, and the policy's steps from 20 to 100 supply the criteria.
- The funds' lines repeated per lot in the income report, as well as the mandate's: dropped at design. With the funds repeated, the gilt fund's apparent yield reads near 8.7 per cent, which any analyst questions, so the device would announce itself. The repetition stays on the mandate's lots, whose apparent yield (about 4.9 per cent) sits inside a UK equity income mandate's range.
- A two-year sample whose exponentially weighted or benchmark-index rung lands on 60 by chance: seed 2038 met every call condition and still had R1 and R2 on 60. The builder's seed conditions now hold R1, R2 and R3 off 60 with margin.
- The stopped builder's world (market seed 2109 on the book as it stood): the golden family's lead-lag and five-day members sat at 9.88 to 9.93 at 60 and the exponentially weighted rung 0.13 from the cap, and the asks were untuned (title 100, releases negative); a fresh seed scan replaced it.
- The legacy cut to £2.43 million to hold the lot lines' inflation under 0.48: the flows-left-in slip stopped being gross (a 17 per cent day) and landed the default on 60; the legacy keeps its size and scales with the portfolio.
- New money bought into one or two holdings: positions of up to 12 per cent of a designation and lot inflation of 0.6 to 0.8; purchases are now capped near 4 per cent of the designation's mandate and positions start the window in one lot.
- Sales capped at 60 per cent of a holding's largest lot with no carry of the shortfall: a designation's cash went negative at a quarter end on some seeds; the shortfall now moves to the next holding.
- The market polish run on the book at each tuned size and knob: the market moved with the ask tuning and the scan's margins no longer held; the polish now runs on the base book, so the market is the seed's alone.
- The ask tuner's size solve with a fixed legacy: the built portfolio missed the solved value by 1.3 per cent and the asks' bins with it; with the legacy scaled to the portfolio the book is scale-free and the solve exact to a few pounds.
- Composing every line handling and the fee lines with every hazard (480 combinations): no portfolio size and running costs total held every figure £600 clear on the seeds tried; the composed set is the ask sheet's seven hazards on both fund routes, with o1 keeping the last line, o2 and the fee lines alone (146).
- A portfolio size whose income fell £75,0xx a step: every stated income and release stepped by exactly 75,000 and read made up; the tuner keeps the fall at least £200 from a whole thousand.
- The mandate's dividends at scale 0.82: a 4.1 per cent yield whose summed lot lines read 5.9 per cent, high for a UK equity income mandate and an invitation to check; scale 0.74 gives 3.70 and 5.3.
- Holding the post-holiday-days slip to the grid's target by scanning further: seeds 10000 to 18499 gave 3 worlds meeting every other target and the slip failed on all of them, as on every sample meeting the call's targets (As built); recorded as the one target not met.
- Fernside's letter as drafted said the takeover cash bought two holdings at the September rebalancing, where the book shows sales and a transfer to the trust; the letter now reads the book.
- The budget workbook's totals written as text, and its summary pointing at a blank row: Excel would show the formula and a nil running costs line; the formulas now carry Excel's cached values and point at the total.
- A Kestwick factsheet sector weight of 9.7 echoed a golden figure in `leak.py`'s sweep; 9.9.
- Removing the holiday-gap slip in the world by having the Kestwick funds deal and price on every UK business day from each market's last close: they already did (506 prices per fund), so the change moved no figure, and the routes that landed 60 were an inner join with the benchmark index file and the stale-day filter (As built). No world holds that filter off 60 at 252 periods a year. Merging its 46 days lifts the daily estimate by about 6.6 per cent in expectation: 4.9 from the period count and 1.6 from co-movement inside the merged periods (9.6 on this world). That leaves the default room only between about 9.24 and 9.38 at 70, and the golden family cannot stay on 60 under it in any world, since its members spread about 8 per cent at 60.
