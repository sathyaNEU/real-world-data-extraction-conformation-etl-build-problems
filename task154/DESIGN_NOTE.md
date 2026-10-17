# task154: Tarbert Bank's call on the June-quarter 2026 advance GDP estimate, the day after the delayed trade and stocks bulletin (architecture 1)

Private, never ships. A new build (wave 5, the first of the wave), numbered from seed FC25. The seed (a bank research
desk's call on a statistics agency's advance real GDP print, sent to clients at 18:00 the business day before, when the
trade and inventories report that feeds three of its lines landed late) was read at its header and Situation only
(`status.py task154`). Its world, decision and quantity are kept. Two of its features are not used: its research memo,
which files how the desk tracks each line, is not shipped (filing the method of the nowcast is rule application), and its
premise that the agency froze its inputs on an unpublished cut-off is replaced by the office's own notice that the
delayed bulletin is incorporated (a withheld cut-off is a hidden rule, a stated one is rule application). The pitfall
is re-found from how the bulletin's stock figures come to exist: a wholesaler, retailer or manufacturer reports the
value of the goods it holds at the end of the month as its accounts carry them, at what it paid for them, and the goods
on hand on any date were bought over the weeks the business takes to turn its stock over.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task154.json`, architecture v1, registered 2026-10-17; `guard.py check` PASS (the first draw, with G13 first, met two older same-puzzle and same-driver signatures, against task102, task130, task134 and task122, and was redrawn with G1 first, the book value's unit of value, see below); nearest drivers 0.08 (task463), 0.07 (task45 lineage, task100 lineage) |
| Domain / task type | `economics-econometrics` (client domain), task type `forecasting-forecast-evaluation` (serves Forecasting): a desk's forecast of a statistical agency's first release, built bottom-up from the release's own source data and evaluated against the release it targets |
| Objective | Forecasting & Predictive Modeling: the June-quarter 2026 advance estimate is released on Thursday 30 July 2026, the day after the call is filed; nothing in the pack contains it |
| Shape | `single-figure`: the call, with two row-set asks in the tables workbook and the note's chart; criteria counted in `## Ask sheet` |
| Decision | `quantity_figure`, answer unit `rate_or_share` (per cent at a compound annual rate, one decimal) |
| Mechanism | gap time (decisive: a book value is priced at the weeks its goods were bought in, the volume the estimate needs is priced at 2025's average prices and measured at the quarter end); pattern none; generators G1 (the stock's unit of value is cost at purchase, not the period's prices), G13, G16; Gate G `method_or_model_selection` (several defensible revaluations of a book value, the right one separated by validation against the Office's past estimates and by the 2008 SNA the user guide cites; relabelled at stage 3 from `decomposition_attribution`); strategy `decomposition_attribution` (the nominal stock movement split into volume and holding gain, each industry's purchase prices over its own holding period deciding the split), banned by `ban.strategy` against task234 v2, see Guard |
| Layer 2 family / pattern | `field_method` (the turnover method behind the national accounts' inventory valuation adjustment: book values revalued at the prices of the weeks the stock was bought in, over each industry's stockholding period, at both ends of the quarter); `own:book-value-stocks-revalued-over-each-industry-turnover-period-at-both-ends` |
| Calibration | `realised_outcome_roster`: the Office's real-time database, every release's estimates of the recent quarters by component; the latest estimate of each past quarter's change in non-farm business inventories (the download's 25 June release, which the 21 July update left as it was) stands as a realised outcome against which a revaluation method, run on TBS's history as the desk pulled it, is compared out of sample; nothing in it states a volume of stocks or a method |
| Furniture | forum `operations_desk` (at 18:00 the call goes to Tarbert's markets floor, whose rates and currency desks position for the release on it, and to clients in the evening preview), forcing event `other` (the office's scheduled advance release, Thursday 30 July 2026, 10:45), organisation family `financial_institution`, role family `research_desk`, context artifact `monitoring_export` (the desk's GDP tracker as at 08:00 on Tuesday 28 July, before the bulletin), opening `question-first`, question form `what` |
| Spine | Trade and Business Statistics' bulk download of merchandise trade by partner country and SITC division, January 2023 to May 2026 (constructed, 72,129 rows); the Office's real-time database (45,576 rows) is the second large file |
| Deliverables | `gdp_preview_2026q2.pdf` (the one-page client preview, the call first, with one chart) and `gdp_preview_2026q2_tables.xlsx` (the two ask tables); the format pair is answered under Guard |
| People | drawn with `guard.py names --locale en_GB --seed 154 --n 20`, the names the check left clear: Nicola Jones (senior economist, Tarbert Bank Economics, the preview's author; not in the prompt), Garry Greenwood (Tarbert's chief economist), Jodie Ford (Tarbert's economics data analyst, who keeps the tracker), Yvonne Mitchell (the Statistics Office's national accounts release contact), Bryan O'Brien (Trade and Business Statistics, the bulletin's contact), Josh Dean (the economists' poll's compiler). Gavin, Rachel, Anthony, Christopher, Ruth and Sheila from the same draw each sit on one older build and were left out |

**Guard.** At the draw: PASS on this worktree; the DRAWN push's pull brought task153's card (registered an hour earlier), which blocked two axes: `ban.calibration` (pilot_log) and `ban.forum` (customer_or_counterparty). Both were redrawn before any design work: the method is validated against the Office's own advance estimates of past quarters (a realised-outcome roster, the real-time database) instead of a desk pilot log, which does not ship, and the call's first user is Tarbert's markets floor (operations_desk), the clients reading the same call in the evening preview. Now WARN `repeat.decision` (task153's quantity_figure), answered: a GDP growth rate is a figure by nature, and task153 shares no other axis. The first draw led with G13 (horizon mismatch) and met two older signatures, gap time, G13
and `quantity_figure` (task102, task130's lineage, task134's lineage) and gap time, G13 and `decomposition_attribution`
(task122's lineage); G1 leads instead because the decisive fact is the stock's unit of value, cost at purchase, against
the period's prices the volume needs, and the redrawn signature (time, G1) matches no card. The format pair (pdf and
xlsx) repeats task152's in this lane; a bank's client preview goes out as a PDF note with its data appendix in Excel,
and task152 shares no other axis with this build. Same world type as task146 (a bank desk previewing an official
release): different release, different driver, line on the card.

At stage 3, `guard.py heart` BLOCKed `ban.strategy`: `decomposition_attribution` repeats task234's v2 card (re-registered
at 02:26, before this card's 03:13) among the last three draws (task464, task153, task234). A relabel to `time_semantics`
cleared it at stage 3 and was reverted at stage 4: it was chosen to pass the guard and named the move in the word the
client bans, which is the card written to pass that the fingerprint skill names. The honest keys are
`decomposition_attribution` for the move as built and `forecast_method_backtest` for the hardened move (the holding period
estimated against the Office's history instead of read off Table 7), and both are banned against the last three draws
(task234 v2 and task464). The build stops here for a different decisive move; it is not relabelled and not forced. Gate G
stays `method_or_model_selection`, the label the rule 3 audit names as honest. `guard.py surface` promotes task152 against
this build (two apart: gap time and `quantity_figure` on both cards), answered on the card's differentiation.

**Same-puzzle and same-driver tests.** Gap time, decisive G1, decision `quantity_figure`, Gate G
`method_or_model_selection`: no card on file carries either triple, lineage included (the guard's structural tests are
clear).

**Abstraction test.** Stripped of nouns: the change over a period in the volume of a stock each holder reports at what
it paid; a holder's stock on any date was bought over its own holding period, so the reported value mixes the prices of
those weeks, and only revaluing each holder's stock at the average price over its own holding period, at both ends of
the period, separates volume from price; the month-end price reads a price step inside the holding period as a fall in
volume and the period's average price reads it the other way. The nearest by mechanism, read for latent structure
rather than score:
- task259 (the brief's nearest) ages pay reports filed at earlier dates to a benchmark date by the market's movement at
  a fixed grade measured within employers; its decisive quantity is which movement carries a report, and its population
  is the reporters. Here nothing is aged to a date and no movement is chosen among reporters: each holder's own reported
  value is split into volume and price, the price being what that holder paid over its own turnover period, and the
  split is taken at both ends of a quarter. The vintage-carry family (a value recorded earlier carried to a later date)
  does not apply: the stock is valued at the date it is reported, the issue is which prices the value is made of.
- task463 links a price index through stock-up periods and drifts; here the price index is given and the stock's
  valuation is the question.
- task445 completes reporters not yet in from their last report; here every reporter is in and the value is complete.
- task133 counts taken-over units only from the takeover; nothing here is censored.
- task68 builds a like-for-like matched panel; the bulletin's industries are fixed and complete.
- task30 carries a gap across from closed parallel cases on a transmission variable; nothing is carried across cases.
None shares the latent structure, the default path and the correction.

**Data-native sentence.** Trade and Business Statistics' monthly survey asks each wholesaler, retailer and manufacturer
for the value of the goods it holds at the end of the month as its accounts carry them, at cost, and the goods on a
machinery importer's floor at the end of June were bought over the two months or so the business takes to sell its
stock, partly before the June leg of the import price rise, while those on a fuel distributor's tank farm were bought in
the last fortnight; so the June book value is a mixture of each industry's prices over its own stockholding period, and
the volume the advance estimate measures comes out right only when each industry's stock, at the end of March and at the
end of June, is divided by its own prices over those weeks.

**Sources read, one line each.**
- `guard.py mechanisms --objective forecasting` (63 builds): the spent ground nearest this build is a level re-dated
  across report dates (task259), completing missing reporters (task445, task146's refiling pool), a rate carried in a
  constructed exposure (task46) and a decline split across an internal boundary (task152); none decomposes a reported
  value into volume and price at the reporter's own purchase prices.
- The kinship cards the brief names: task259 (vintage-carry, differentiated above and on the card), task68 (export
  statistics on a matched panel: here the trade lines are mechanical and the exports-by-market ask carries its own
  devices), task30 (a gap carried across from closed parallel cases: here nothing is carried across), task133 (delayed
  entry: nothing here is censored).
- `two-layer-task-design.md`: "the field's own method done right" and "handling the data's real structure" are the
  client's frames; the turnover method is national accounting's own.
- `layer2-rigor-patterns.md`, economics-econometrics / forecasting-forecast-evaluation (real-time vintages against the
  named target release): the call is struck against the advance estimate itself, and the Office's real-time database
  validates out of sample
  on the desk's own real-time filings; the decisive step is not a vintage choice (`## Tried and rejected`).
- task152's design note (the lane's last ship): its corridor discipline (every defensible construction of the golden in
  the bin, every rival a set distance out) is the model for this ladder.

**World.** A fictional English-speaking country of about 7 million with its own floating dollar; a coal, LNG and dairy
exporter that imports most of its machinery, vehicles and consumer durables. The Statistics Office publishes quarterly
GDP in three estimates (the advance about 30 days after the quarter, the second about 60, the third about 90), volumes
at the average prices of the previous calendar year (2025 for the quarters of 2026) and the headline as the change on
the previous quarter at a compound annual rate; each July its annual national accounts revise the quarterly series of
recent years (this year on Tuesday 21 July, from the June quarter 2023). It also publishes the producer and trade price
indexes (2019 = 100) and a real-time database of every release's estimates by component. Trade and Business Statistics
(TBS), a unit of the Department of Industry, publishes the monthly bulletin "Merchandise trade and business stocks":
goods exports and imports from customs entries, and wholesalers', retailers' and manufacturers' stocks and cost of sales
from its monthly business survey. TBS compiled the statistics on a new processing system from the January 2026 month;
on 13 July 2026 a failed storage migration took that system and the data portal down, and the June bulletin, due on
Wednesday 22 July, came out on Tuesday 28 July as a PDF with its tables, the portal still down. On Friday 24 July the
Office announced that the advance estimate would be published as scheduled on Thursday 30 July and would incorporate
the June results. The dollar fell in two legs, in late February after the Reserve Bank's surprise rate cut and the fall
in the coal price, and in the first days of June after the sovereign rating downgrade; import prices rose in March and
again in June. Floods closed the coal ports for part of February; one of the two LNG projects took a train down for three
weeks of June 2025. Tarbert Bank (fictional) is a commercial bank whose economics desk sends its call at 18:00 the
evening before each advance estimate to the bank's markets floor and, in a one-page GDP preview, to clients; this year
the desk moved the call from a bridge equation on monthly indicators to a line-by-line tracker built on the Office's own
sources, and the tracker workbook carries each line's June-quarter estimate as at 08:00 on Tuesday 28 July, before the
bulletin.

**Pack** (15 files, five formats; stage 3 builds it). The Office's user guide (PDF), its notice of 24 July (text), its
real-time database as the desk downloaded it on 26 June (CSV, every release from the March quarter 2019 advance estimate
to the March quarter 2026 third estimate), its annual national accounts of 21 July (workbook, with the revised quarterly
series), its price indexes for June (workbook: inputs to and outputs of each industry, exports and imports by SITC
section); TBS's June bulletin (PDF), the desk's pull of TBS's monthly series on 24 June (CSV, 2019 to May 2026), TBS's
bulk download of trade by country and SITC division (CSV, January 2023 to May 2026), its country codes and SITC division
list (CSV); the Harbours Board's monthly bulk loadings by port (CSV); the desk's tracker (workbook); the Harbourline
economists' poll of 23 July (JSON, a distractor); the Industry Federation's business conditions survey for June (CSV, a
distractor); and the desk's index of its data folder (CSV, the provenance record).
## Default path

Figures measured on the design world's tables (`generator/calc.py`); stage 3 re-runs every one on the shipped files.

1. Read the Office's user guide and notice: the advance estimate is the percentage change in GDP volume on the March
   quarter at 2025 prices, compounded to an annual rate; a line's contribution is its change over March-quarter GDP; the
   June bulletin is in the estimate; the advance estimate revises no earlier quarter.
2. Take the desk tracker's June-quarter estimates for every line the bulletin does not feed (household and government
   consumption, the four investment lines, farm and other inventories, services exports and imports) and its
   March-quarter base.
3. Build goods exports and imports from the bulletin's seasonally adjusted April, May and June values by SITC section,
   each over its export or import price index rebased from 2019 to the 2025 average, and take the change on the March
   quarter's volumes.
4. Build business inventories: each industry's end-March and end-June book value from the bulletin over that month's
   producer price index of the industry's purchases, rebased to 2025, the change summed over the eight industries, less
   the March quarter's published change, over March-quarter GDP.
5. Sum the contributions and compound to an annual rate.

Ends on: 2.2 per cent.

Golden: 2.8 per cent: the same lines, each industry's end-March and end-June book value divided by the average of its
input price index over the months its stock-to-sales ratio covers at that date (2.793 built, 0.43 of a bin from its
edge; placed by the tracker's household line, `tracker.GOLDEN_TARGET` 2.794, a design parameter set before the asks were
measured). The default path ends on 2.179.

## Stump sentence

Taking the desk's track for every line the late bulletin does not feed, building goods trade from the bulletin section by
section and deflating each industry's end-March and end-June book-value stocks by that month's price index, the textbook
removal of holding gains, files 2.2 per cent against the golden 2.8; the step that lands it there is reading a book value
as if its goods had been bought at the month end's prices, when each industry's stock was bought over its own
stockholding period, partly before the March and June legs of the import price rise, so both quarter ends' volumes come
out low, the June one, with the larger leg inside its window, lower still, and the run-down looks deeper than it was.

## Three rules

- **Task type:** economics-econometrics, forecasting-forecast-evaluation (serves Forecasting): a bottom-up forecast of the
  statistical office's first release of June-quarter GDP growth, built from the release's own source data the evening
  before and validated out of sample against the office's own estimates of past quarters.
- **Domain test:** the quantity that decides the call is the volume of business inventory investment the advance estimate
  will carry, which national accountants measure by revaluing businesses' book-value stocks at the prices of the weeks
  the goods were bought in, over each industry's stockholding period, before taking the change, and which a GDP desk
  replicates from the trade and stocks bulletin and the producer price indexes the office deflates with.
- **Swap:** "what growth a hospital's patient-day index will show next quarter" keeps a call on an index and a monthly
  source, but book values carried at cost, a stockholding period read from a stock-to-sales ratio, producer prices
  rising in two legs and an expenditure aggregate summed from contributions at 2025 prices have no counterpart, so what
  decides the figure stops making sense.
- **Layer 1:** the June bulletin published as a PDF with tables while TBS's portal was down (TBS's processing system);
  its revised April and May overlapping the desk's 24 June portal pull (TBS's monthly revision cycle); price indexes on a
  2019 base against volumes at 2025 prices (the Office's price statistics and national accounts); seasonally adjusted
  bulletin tables beside original-terms market tables (TBS's publication); values in thousands of dollars in the bulk
  download against millions elsewhere (TBS's portal formats); the real-time database's releases each at its own
  reference year's prices, with its 2024 layout change when business investment was split (the Office's database); the
  desk's 26 June download of that database against the 21 July annual update (the desk's refresh routine), neutral on
  the call because the update did not touch goods trade or non-farm inventories; the tracker's line labels against the
  Office's component codes (the desk's workbook); contributions in points of March-quarter GDP beside a compound annual
  headline (the Office's presentation). None is placed to be caught, and each is asserted neutral on the call (R2).
- **Layer 2:** `field_method`: the turnover method behind the inventory valuation adjustment, the national accounts'
  own way of taking a volume change out of book values; the methodological choice that flips the call is the price a
  book value is divided by: each industry's own prices over the months its stock covers, at both quarter ends (2.8),
  against the quarter end's price index (2.2) or the quarter's average (3.3).
- **Decisive step:** revalue each industry's end-March and end-June book-value stock at the average of its price index
  over the months its stock-to-sales ratio covers at that date, so that the stock is read at the prices it was bought
  at, then take the change in volume at 2025 prices.
- **Not semantics:** every field (book value at cost, cost of sales, the stock-to-sales ratio, the price indexes and
  their base, exports and imports by SITC section) and every filed definition (the advance estimate's headline, volumes
  at 2025 prices, contributions, the change in inventories as the change in the volume of goods held) is read the same
  way by the easy routes; no field, code or definition says when the goods in a month-end stock were bought or at what
  price, and the default path reads them all correctly and still files 2.2.
- **Not rule application:** no shipped sentence says how a book value becomes a volume; the user guide files the
  estimand (the change in the volume of goods held, at 2025 prices) and its sources, TBS's notes say book values are at
  cost, and executing every filed sentence word for word leaves the stock's volume uncomputed; the easy execution, the
  book value over the month's index, files 2.2 (R3a in `checks.py`); no filed rule or procedure performs the revaluation
  over each industry's turnover period.
- **Analyst test:** a strong analyst who takes the desk's track for every line the late bulletin does not feed, builds
  goods trade from the bulletin section by section and deflates each industry's end-March and end-June stocks by that
  month's price index files 2.2 per cent; deflating at each quarter's average price files 3.3; revaluing only the June
  end files 3.3; a two-month stockholding period for every industry files 3.1; only each stock revalued over its own
  turnover period at both ends files 2.8 (executed on the clean truth at stage 3, R3a and R3b).
- **Estimand:** the prompt and the Office's user guide: the percentage change in GDP volume (2025 prices) from the March
  quarter to the June quarter of 2026 at a compound annual rate, as the advance estimate published on 30 July 2026 will
  show it, rounded to one decimal; the population (the June quarter's expenditure on GDP), outcome, window, unit,
  comparison and rounding are filed, the method is not.
- **No decoy:** no memo, draft, briefing, client note or stakeholder figure states or argues a June-quarter call, an
  inventory volume or a revaluation; the desk's tracker carries no total and leaves the bulletin's three lines open;
  the economists' poll (a declared distractor, median 2.4, closed before the bulletin) and the business conditions
  survey (a declared distractor) are never the stump; the poll's forecasts are anonymous.
- **No certified replay:** the standard is cited (the user guide compiles the accounts to the 2008 SNA) and the estimand
  filed; the Office's latest estimates of past quarters' non-farm business inventories in the real-time database carry
  its own estimate for businesses outside TBS's survey in every quarter (sd about $10m), so no quarter reproduces
  exactly; they validate the revaluation out of sample (RMSE $9.9m over 28 quarters against $62.5m for month-end
  deflation, $125.9m for the quarter's average, $106.0m for weighted-average cost and $33.6m for the nearest rival,
  ratios rounded down to whole months), and they name no method; no table
  states a volume of stocks, a replacement cost or an inventory valuation adjustment.
- **Lesson:** a stock reported at what its holder paid is priced at the weeks the goods were bought in, so its volume must
  be read at those weeks' prices, industry by industry over each one's own turnover period and at both ends of the
  period; the quarter end's price misreads a price rise inside the turnover period as a fall in volume. No build on file
  teaches the revaluation of a book-value stock.

## Readability screen

Six tests per rung (`stumping` 2.1): 1 a filed sentence names it or sends the solver looking, 2 a column, key or marker
makes it a predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery
finds it, 6 one subtraction, ratio or half of a figure. Design figures.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 (the default path) each industry's stocks over the month-end price index, both ends (2.2) | no | no | yes: the textbook removal of holding gains | no | no | yes: one division a stock | readable |
| R1 each industry's stocks over the quarter's average price index (3.3) | no | no | yes: the change in inventories valued at the period's average prices | no | no | yes: one average | readable |
| R2 a two-month stockholding period for every industry, both ends (3.1) | no | no | yes: a turnover lag of a round number of months | no | no | yes: one average a stock | readable |
| R3 (decisive) each industry's end-March and end-June stocks over the average of its own input prices across the months its stock-to-sales ratio covers at that date (2.8) | no: the user guide files the estimand (the change in the volume of goods held, at 2025 prices) and the sources, TBS's notes define the book value as at cost and the ratio as months of cost of sales; no sentence says when the goods on hand were bought, at what price, or how a book value becomes a volume | no: no column holds a volume of stocks, a replacement cost, a valuation adjustment or a stockholding period; the ratio is a standard bulletin column beside sales | no: the reflexes are the month-end index, the quarter's average and a round lag; only the Office's own estimates of past quarters, rebuilt under each method, show that the month-end and average readings miss (RMSE $62.5m and $125.9m against $9.9m), and a solver must go and build them | no: no forecast, inventory volume, certified figure or past call ships; the database's past estimates carry the Office's coverage term and tie under no method | no: nothing in the files is wrong | no: eight industries, each a window average of its index over a fractional number of months at two dates, against a published change | silent |

## Semantic fork table

Every term in the main ask and every convention the main computation needs. `checks.py` asserts each row.

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | advance estimate | the Office's first estimate of the June quarter, 30 July 2026, 10:45 | the second estimate; the poll | not this release | the prompt and the notice name the advance estimate of 30 July |
| SF2 | real GDP growth | the change in GDP volume on the March quarter | through the year | another quantity | the user guide: the headline is the change on the previous quarter |
| SF3 | annualised rate | compounded four times | the quarter's change times four | 2.77, the same 2.8 | the user guide files compounding; same call (asserted) |
| SF4 | the June quarter | April to June 2026 | none | none | the prompt |
| SF5 | the June bulletin in the estimate | in | May carried into June | -0.6 at the revaluation, -1.1 at month-end | the notice of 24 July |
| SF6 | 2025 prices | each index rebased to its 2025 average | the indexes left at 2019 = 100 | another level | the user guide; the March quarter's goods volumes reproduce only rebased (asserted) |
| SF7 | the March-quarter base | the latest estimates (21 July), the tracker's base | the 25 June release in the database | 2.82, the same 2.8 | same call (asserted): the update moved neither goods trade nor non-farm inventories |
| SF8 | does the advance revise March | no | yes | none | the user guide: the advance estimate revises no earlier quarter |
| SF9 | goods deflation | section by section | total value over a total index | none filed | the user guide: by SITC section with the export and import price indexes |
| SF10 | seasonal adjustment | seasonally adjusted | original terms | another level | the user guide; the bulletin's section tables are seasonally adjusted; original terms miss the March quarter's volumes (asserted) |
| SF11 | business inventories' scope | TBS's eight industries; the Office's term for businesses outside the survey expected at zero | a carried coverage term | 2.79, the same 2.8 | same call (asserted): the term averages $0.3m over 28 quarters and the March quarter's is under $2m |
| SF12 | the price index of a stock | the producer price index of the industry's purchases | of its outputs | 3.0 | the user guide's sources table names the purchases indexes |
| SF13 | sales in the ratio | cost of sales | selling value | none (no margin ships) | TBS's notes: the ratio is stocks over the month's cost of sales |
| SF14 | April and May | the bulletin's revised months | the portal's 24 June pull | 2.82, the same 2.8 | same call (asserted) |
| SF15 | end-March stocks | the bulletin's | the portal's | identical | same call: the June bulletin did not revise March (asserted) |
| SF16 | the bulletin lines' denominator | the tracker's March-quarter GDP | the database's 25 June GDP | 2.82 | same call (asserted) |
| SF17 | rounding | half up to one decimal, the unrounded rate | none | none | the prompt; the golden 0.43 of a bin from its edge |
| SF18 | the lines the bulletin does not feed | the tracker's estimates | another estimate | none ships | converge: the pack carries no other June-quarter estimate of those lines |

## Ladder

Built figures (annualised, per cent), each asserted in `checks.py` (L1 to L6, BT1 to BT3) and the rungs recomputed in
`verify.py` on its own path.

| Rung | Route | Figure | From the golden | Dies to |
|---|---|---|---|---|
| R0 | month-end price indexes at both ends (the default path) | 2.179 | -0.614 | the stock on hand at a month end was bought over its stockholding period; the Office's past estimates (RMSE $62.5m) |
| R1 | the quarter's average price indexes | 3.300 | +0.507 | the same; RMSE $125.9m |
| R2 | a two-month stockholding period for every industry | 3.083 | +0.290 | each industry's own stock-to-sales ratio; RMSE $61.4m |
| R3 | each industry over its own ratio, both ends (golden) | 2.793 | 0 | |

Side cells, each a named wrong answer with its back-test RMSE: the June end revalued with March at its month-end index
3.282 ($62.8m); March revalued with June at its month-end index 1.693 ($68.9m); weighted-average cost 3.441 ($106.0m);
the output price indexes 2.969 ($64.9m); the average stock over each quarter 3.109 ($119.6m); ratios rounded up to whole
months 3.051 ($37.9m) and down 2.473 ($33.6m); ratios plus a month 3.231 ($82.0m); the previous month's index 4.029
($168.0m); the period ending the month before 3.953 ($192.3m); holding gains removed at month-end prices 2.178
($62.8m); the change in book value over the quarter's average index 6.175 ($567.2m); book values undeflated 6.316
($504.6m); month-end with the March quarter rebuilt the same way 2.541; May carried into June -0.6 at the revaluation
and -1.1 at month-end; the poll's median 2.4.

**Corridor** (every construction of R3, inside the bin [2.75, 2.85)): the quarter's average ratio 2.789, the previous
month's ratio 2.793, whole months 2.760, mid-month interpolation 2.836, the index at the period's midpoint 2.774, holding
gains removed at the period's prices 2.800, all industries pooled 2.788, the industries' average ratio for every
industry 2.786, first in first out from the flows 2.782, the March quarter rebuilt the same way 2.797; one sigma (every
ratio 2 per cent longer or shorter) 2.811 and 2.774. The corridor spans -0.033 to +0.043 around the golden (2.760 to
2.836), 0.010 inside the bin's lower edge and 0.014 inside its upper.

**Position and margins.** The golden is bracketed: R0 below by 0.61, R1 above by 0.51. Every rival is at least 0.17
from the golden (the output price indexes, 2.969) and outside the bin. Only the decisive move reverses: R0 to R1 rises,
R2 and R3 come back down to the bracket. Worth on the graded quantity: R3 moves the call 0.61 from R0 and 0.29 from R2.

**Grid.** End treatment (both, June only, March only) by price window (month end, quarter average, two months, own
ratio): every cell but (both, own ratio) is at least 0.1 from the golden (L6). Partial applications (some of the five
industries whose ratio exceeds a month revalued, the rest at month end) walk between R0 and R3, and none of the 31 lands
in the bin (the nearest, all but manufacturing, 2.737; L5). The three industries whose stock turns over in under a month
(food wholesale, fuel wholesale, food retail) value identically under every window.

**Back-test** (the Office's latest non-farm inventories in the 26 June download, 28 quarters 2019Q2 to 2026Q1, TBS's
history as the desk pulled it): RMSE turnover 9.9; its other constructions: the index at the period's midpoint 8.7,
whole months 9.4, the previous month's ratio 9.5, first in first out 9.6 (27 quarters), the quarter's average ratio
9.7, holding gains at the period's prices 10.0, mid-month interpolation 23.9, one average ratio 34.2, all industries
pooled 85.3; the rivals: ratios rounded down 33.6, rounded up 37.9, two months 61.4, month-end 62.5, June end only 62.8,
output indexes 64.9, March end only 68.9, ratios plus a month 82.0, weighted-average cost 106.0, average stock 119.6,
quarter average 125.9 ($m). The March quarter 2026 alone, the one quarter with the March leg inside its window:
month-end misses by $115.0m, turnover by $1.2m.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the June quarter's expenditure on GDP; the business inventories of TBS's eight industries | user guide (filed); SF11 the Office's coverage term at its zero mean (asserted) |
| 2 | Unit of account | the quarter's GDP volume; each industry's month-end stock | the prompt and the user guide name them |
| 3 | Attribution window | April to June 2026 against January to March | the prompt; the bulletin's months are calendar months |
| 4 | As-of dating | the call at 18:00 on 29 July; the March quarter as revised on 21 July | SF7 same call (asserted) |
| 5 | Version basis | the bulletin's revised April and May; the latest March quarter | SF14, SF7 same call (asserted) |
| 6 | Denominator | March-quarter GDP | user guide; SF16 same call (asserted) |
| 7 | Weighting | volumes at 2025 prices, sections and industries summed | user guide (filed) |
| 8 | Window length | each industry's stockholding period from its own ratio | C3 corridor: every construction inside the bin (asserted) |
| 9 | Boundary inclusivity | month m whole, then back to a fraction of the earliest month | C3: mid-month interpolation and whole months inside the bin (asserted) |
| 10 | Rounding path | the unrounded rate, half up to one decimal | the prompt; SF17 |
| 11 | Tie-break | none | no ranking is graded |
| 12 | Maturity and censoring | the June quarter complete in the bulletin | the notice and the bulletin; no partial month |
| 13 | Order of operations | rebase, revalue, difference, sum, compound | C1: linear steps commute except compounding, last (asserted) |
| 14 | Row order | none | sums |
| 15 | Duplicate resolution | the bulletin's months over the portal's | SF14 same call (asserted) |
| 16 | Identity normalisation | the tracker's labels to the Office's components; TBS's industries to the price indexes | one to one, names in both (asserted) |
| 17 | Netting against gross | imports net against exports through the identity | user guide: imports enter with a negative sign |
| 18 | Dimensional units | $m at 2025 prices throughout; the bulk download in $000 is off the call's path | asserted |
| 19 | Code and status semantics | SITC sections and TBS's industry codes | dictionaries; never the stump |
| 20 | Integerisation | none | none |
| 21 | Clause scope | the advance estimate revises no earlier quarter | SF8 user guide |
| 22 | Forward window contents | the June quarter's lines: the tracker for ten, the bulletin for three | SF18 converge; SF5 the notice |

## Literal reader

Executing the prompt, the user guide, the notice, TBS's notes and the tracker word for word fixes the target (the advance
estimate's change in GDP volume at 2025 prices on the March quarter, compounded, one decimal), every line's source and
every convention but the price a book-value stock is divided by, which no sentence states; each other reading converges
on the golden's bin or violates a quoted line (SF1 to SF18), and the easy answers come from easy methods on the same
literal target (the month-end index 2.2, the quarter's average 3.3, a round lag 3.1), never from another reading. The
Office's estimates of past quarters, rebuilt under each method from TBS's history, separate the methods (RMSE $9.9m
against $33.6m and more) without naming one. Re-run on the finished pack at stage 3.

## Oracles

- The Office's real-time database: its latest estimates of past quarters' non-farm business inventories are realised
  outcomes carrying the Office's coverage term in every quarter; the revaluation over each industry's own ratio comes
  within $9.9m RMS and every rival misses by $33.6m or more; the coarser constructions of the same revaluation (all
  industries pooled $85.3m, one average ratio $34.2m, mid-month interpolation $23.9m) back-test worse and land the same
  call; it ties exactly under no method, names none and cannot tell the corridor's members apart. The same
  database's GDP rows are Ask A's source.
- The March quarter's goods volumes: TBS's January to March values over the rebased section indexes reproduce the
  Office's March-quarter exports and imports to the dollar under every inventory method; a reconciliation of the trade
  lines, blind to the decisive step.
- The tracker: the desk's own estimates for ten lines and the March-quarter base, no total, the bulletin's three lines
  open; it ranks nothing and states no call.
- The poll (declared distractor): forecasters' views closed on 23 July, before the bulletin, median 2.4; deleting it leaves
  the call and both asks unchanged (asserted). The business conditions survey (declared distractor): indexes only.
- The desk's data folder index: where each file came from and when; it states no figure, method or device (asserted).
- Nothing ties only under the golden for the June quarter: no published estimate, inventory volume or past call ships.

## Ask sheet

**Main call's declared row population:** the tracker, the bulletin's trade-by-section and stocks tables, the price
indexes, the user guide and the notice, the portal pull's stocks, cost of sales and ratios (the back-test), and the
database's non-farm inventories rows and its March-quarter 2026 goods rows. Device and hazard rows in it: 0 (asserted:
SEP1 the call unchanged with the bulk download, the ports and the database's GDP rows deleted; SEP2 both asks unchanged
with the call's stocks and prices perturbed; R2.3 the database's goods and non-farm inventories rows the same in the 25
June release and the 21 July update; B8 the call's goods months, January to June 2026, carry no lodgement shift). The
asks share no primary device or path, and neither is keyed to the call, its construction or its figures.

**Ask A. The advance estimate's revision record** (5 figures: the three revisions in percentage points to one decimal,
the two means to two decimals): the revision from the advance estimate to the latest estimate of annualised growth for
the September and December quarters of 2025 and the March quarter of 2026, and the mean revision and the mean absolute
revision over the twelve quarters from June 2023.
- H18 home: how far the print the call targets moves once later data arrive, the preview's caveat beside the call; a
  qualifier of the call, not a second decision. Use: the workbook's first table and the preview's chart.
- Construction: each quarter's advance estimate from its advance release in the real-time database (that quarter on the
  one before, in the same release, compounded); the latest estimate from the annual national accounts' quarterly series
  of 21 July; the revision latest minus advance, both growth rates from the unrounded estimates (the user guide: revisions
  are measured between growth rates calculated from the unrounded estimates, not between the rounded headlines).
- Primary device A1 (D5, a silently partial extract): the desk's copy of the database is its download of 26 June, the
  day after the March quarter's third estimate; the annual national accounts of 21 July revised every quarter from June
  2023 and are not in it. The download's last release looks like the latest, and its estimates tie with every release in
  it. Fair: the annual accounts' quarterly series is the latest estimate of every quarter (A5: the update moved GDP in
  all twelve quarters from June 2023 and in none before).
- Hazards: HA1 the releases' reference years (each release's levels at its own year's prices; growth taken within a
  release is unaffected, levels mixed across releases are not); HA2 the 2024 layout change (business investment split
  into three series; GDP unaffected); HA3 compounding against times four (moves the two means, no quarter); HA4 the
  rounded headlines (differencing one-decimal growth rates moves three figures; closed by the user guide's sentence).
- Stops (built, each a complete pipeline): S1 the download's 25 June release as the latest (the cracker), 5 of 5 missed
  (+0.9, +0.4, +0.6; mean +0.08; MAR 0.52); S2 the advance growth taken against the latest level of the quarter before
  (mixing releases), 5 of 5; S3 the annual accounts' current-price table in place of the volumes, 5 of 5; S4 revisions
  signed advance minus latest, 4 of 5; golden +0.5, +0.6, +1.2, mean +0.34, MAR 0.58, every figure at least 0.25 of a
  bin from its edge (A1, A2).
- Span: the database, the annual national accounts, the user guide (3 files); release, release date, estimate, prices,
  quarter, series, value; the annual workbook's quarterly table.
- Realism: a desk refreshes its copy of the real-time database after each quarterly release, and the annual accounts
  are a separate publication.

**Ask B. Coal and LNG shipped to five markets** (12 figures, $m to one decimal): for Japan, China, Korea, India and
Taiwan, the change in the value of coal and of LNG shipped there in the June quarter of 2026 on the June quarter of 2025,
and each commodity's five-market total.
- H18 home: where the June quarter's largest export swing went, the preview's trade paragraph; a measure of the goods
  exports line the call consumes, by market, which the call does not turn on.
- Construction: April and May 2026 from TBS's bulk download (divisions 32 and 34, $000), June 2026 from the bulletin's
  coal and LNG table ($m); the June quarter 2025 from the bulk download, each month the month the cargoes sailed.
- Primary device B1 (D2, a label stored before a silent switch): every coal and LNG export is lodged on a periodic entry
  in the month after the cargoes sail; TBS's old processing system recorded such entries in the month they were lodged,
  and its new system, from the January 2026 month, dates them by their shipments. The download's 2025 months for
  divisions 32 and 34 are therefore lodgement months: its June quarter 2025 is the March to May shipments, and June 2025,
  when LNG loadings at Cape Mallory dropped, falls in July. Every row is valid and every total ties. Evidence, split:
  the Harbours Board's monthly loadings run a month ahead of TBS's 2025 tonnages and level with them from January 2026
  (B4), and December 2025 carries November's and December's cargoes (B5). Fair: every coal and LNG export is on a
  periodic entry, so moving each 2025 month back one reproduces the shipments exactly (B3).
- Hazards: HB1 thousands of dollars in the download against millions in the bulletin; HB2 the download's ISO country
  codes and "Korea, Republic of" against the bulletin's "Korea"; HB3 the bulletin's coal and LNG table in original terms
  beside its seasonally adjusted section tables; HB4 December 2025's double month (outside the window; the tell).
- Stops (built): S1 the download as it stands (the cracker), 11 of 12 missed (Taiwan's LNG unmoved: no cargo sailed for
  Taiwan in March or June 2025); S2 LNG moved back a month, coal left, 6 of 12; S3 coal moved back a month, LNG left, 5
  of 12; S4 both moved back two months, 12 of 12; golden (Japan coal +174.5, LNG +680.7; China +116.9, +262.8; Korea
  -23.5, +91.2; India +72.9, +166.8; Taiwan -15.3, +265.3; totals coal +325.5, LNG +1,466.8), every figure at least 0.15
  of a bin from its edge (B1, B2).
- Span: the bulk download, the bulletin's coal and LNG table and notes, the ports' loadings, the country codes and the
  SITC division list (5 files); month, flow, country, division, value, quantity, unit; port, cargo, tonnes.
- Realism: bulk exporters lodge periodic entries after their cargoes sail, a customs system's replacement changes how it
  dates them without restating history, and the transition month carries both months' cargoes.

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 reference years | each release priced at its own year | Ask A | every figure when levels are mixed across releases |
| HA2 2024 layout | business investment split | Ask A | none at GDP |
| HA3 compounding | the Office's annualising | Ask A | the two means |
| HA4 rounded headlines | releases print one decimal | Ask A | three figures (closed by the user guide) |
| HB1 thousands | the portal's download format | Ask B | every figure by a factor of 1,000 when unread |
| HB2 country names | ISO codes against bulletin names | Ask B | Korea's two figures when unmatched |
| HB3 original terms | market tables are never adjusted | Ask B | none (both years original) |
| HB4 December 2025 | the new system's first month | Ask B | none inside the window |

**Referee.** Ask A: the annual national accounts' quarterly series is the latest estimate, a source the golden reads,
not a control. Ask B: the Harbours Board's loadings show which month TBS's 2025 coal and LNG belong to. Neither hands over
an ask figure, and no filed sentence says the download predates the update or that periodic entries were dated by
lodgement (A6, B6).

**Cracker sheet**

| Ask row | Figures | Cracker's path | Cracker's figures kept | Verdict |
|---|---|---|---|---|
| Ask A, the revision record | 5 | the download's 25 June release as the latest estimate | 0 | miss |
| Ask B, coal and LNG to five markets | 12 | the download's 2025 months as they stand | 1 (Taiwan's LNG) | miss |

Mirror leakage: 5.9 per cent of the ask weight (1 of 17 figures). The mirror is the most attractive wrong rung, R1
(3.3); it runs the same ask paths as the cracker.

Pair ceiling: 31.7 (the cracker C = 38 + 7 + 55 x 1/17 = 48.2; the best miss S = 5 + 7 + 55 x 1/17 = 15.2). With the
cracker also cracking the most obvious device, A1 (the annual accounts sit in the pack): C = 45 + 55 x 6/17 = 64.4 and
the pair 39.8 (PAIR in `checks.py`). With both top responses on the call and neither device cracked: about 48. Rerun
from the generated rubric.

## Tried and rejected

- The seed's research memo filing the desk's tracking (each line rebuilt from the handbook's source at its latest
  values, consumer services extrapolated with total private hours): shipping it files how the nowcast is computed,
  rule application; not shipped.
- The seed's premise that the agency froze its inputs on an unpublished cut-off, so the late report's lines carry the
  agency's own projections: withheld, it is a hidden rule; stated, the call is rule application; inferred from past late
  sources in past quarters, it is a cut-off recovered from published figures on small counts. The Office's notice states the
  June bulletin is in the estimate.
- A real-time-vintage calibration as the decisive step (the desk's bias measured on tracks rebuilt from the sources'
  latest vintage against the advance estimates): a desk keeps its real-time inputs, so the natural calibration is already
  real-time, and any sixteen-quarter calibration in the golden moves the call a bin under one
  standard error; kept out of the golden.
- A stale consensus updated by the bulletin's news as the golden: the decisive step would be reading the poll's closing
  date, a field reading; the poll ships as a distractor.
- The agency's month-three projections for missing sources recovered from its published assumption tables: a hidden rule
  recovered from published figures.
- A pay-timing effect in the government's cash outturn as the decisive step: visible in the monthly series and fixed by
  counting paydays, a rule; kept for the ask layer if needed.
- The desk's own sixteen-quarter pilot log as the calibration organ (each filed line beside the advance estimate's): task153, registered an hour before this card, carries a pilot log, and the guard bans the form in consecutive builds; the validation runs on the Office's real-time database instead, and no desk pilot log ships.
- Exports to the ten largest markets as the trade ask: outside coal and LNG no system-rooted device moves a market's
  year-on-year change, so the cracker keeps every non-energy market; narrowed to coal and LNG, the periodic-entry dating
  carries every figure.
- The revision record graded quarter by quarter for all twelve quarters: five of the twelve revisions sit within a
  tenth of a bin of a rounding edge, and the stale download, the most obvious device, would hand back twelve figures;
  three quarters and the two means are graded, the twelve quarters charted.
- Tarbert's card spending, the poll's own record and the government's pay runs as a third ask: card data's devices are
  not recoverable exactly, the poll's clocks are battery-visible, and the pay runs feed a tracker line (a device there
  would move the call).
- The advance estimate revising the quarter before it (the generator's first vintages): the user guide files that it
  revises no earlier quarter, and a rule the record breaks loses its authority; the vintages were redrawn so every
  advance release leaves earlier quarters as the release before it had them (A7).
- Round March-quarter levels (each component's level, and each industry's end-March book value, placed on a round
  figure): a generator tell in the tracker, the annual accounts and the bulletin; every level moved off round values.
- Port names North Head, Kerrisdale and Barrow Point: real places, and Barrow Island is a real LNG hub; renamed Port
  Ardley, Saltpan Bay and Cape Mallory (H21), and the bulk download's value column named for a real currency renamed.
- Thailand in the coal and LNG table: its coal change sat a hundredth of a bin from a rounding edge; dropped, five markets.
- The two means of the revision record at one decimal: the 26 June download's mean absolute revision rounded to the
  golden's; two decimals, with the rounded-headline reading (three figures moved) closed by the user guide's sentence.
- Relabelling the stump strategy `time_semantics` to clear `ban.strategy` (stage 3): a card written to pass, naming the
  move in the client's banned word (rule 3 audit); reverted to the drawn `decomposition_attribution`, which the guard bans
  against task234 v2, and the build stopped for a different decisive move.
