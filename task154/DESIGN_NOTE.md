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
| Mechanism | gap time (decisive: a book value is priced at the weeks its goods were bought in, the volume the estimate needs is priced at 2025's average prices and measured at the quarter end); pattern none; generators G1 (the stock's unit of value is cost at purchase, not the period's prices), G13, G16; Gate G `decomposition_attribution`; strategy `decomposition_attribution` (the nominal stock movement split into volume and price, the price basis deciding the split) |
| Layer 2 family / pattern | `field_method` (the turnover method behind the national accounts' inventory valuation adjustment: book values revalued at the prices of the weeks the stock was bought in, over each industry's stockholding period, at both ends of the quarter); `own:book-value-stocks-revalued-over-each-industry-turnover-period-at-both-ends` |
| Calibration | `pilot_log`: the desk's sixteen-quarter pilot of its tracker (June quarter 2022 to March quarter 2026), each filed line beside the advance estimate's line; it validates the method out of sample and refutes nothing by itself |
| Furniture | forum `customer_or_counterparty` (the desk's clients receive the call at 18:00), forcing event `other` (the office's scheduled advance release, Thursday 30 July 2026, 10:45), organisation family `financial_institution`, role family `research_desk`, context artifact `monitoring_export` (the desk's GDP tracker as at 08:00 on Tuesday 28 July, before the bulletin), opening `question-first`, question form `what` |
| Spine | Trade and Business Statistics' bulk download of merchandise trade by partner country and SITC division, January 2023 to May 2026 (constructed; row counts at stage 3) |
| Deliverables | `gdp_preview_2026q2.pdf` (the one-page client preview, the call first, with one chart) and `gdp_preview_2026q2_tables.xlsx` (the two ask tables); the format pair is answered under Guard |
| People | drawn with `guard.py names --locale en_GB --seed 154`, the names the check left clear: Nicola Jones (senior economist, Tarbert Bank Economics, the preview's author; not in the prompt), Garry Greenwood (Tarbert's chief economist), Jodie Ford (Tarbert's economics data analyst, who keeps the tracker and the pilot log), Yvonne Mitchell (the Statistics Office's national accounts release contact), Bryan O'Brien (Trade and Business Statistics, the bulletin's contact), Josh Dean (the economists' poll's compiler). Gavin, Rachel, Anthony, Christopher, Ruth and Sheila from the same draw each sit on one older build and were left out |

**Guard.** At the draw: PASS. The first draw led with G13 (horizon mismatch) and met two older signatures, gap time, G13
and `quantity_figure` (task102, task130's lineage, task134's lineage) and gap time, G13 and `decomposition_attribution`
(task122's lineage); G1 leads instead because the decisive fact is the stock's unit of value, cost at purchase, against
the period's prices the volume needs, and the redrawn signature (time, G1) matches no card. The format pair (pdf and
xlsx) repeats task152's in this lane; a bank's client preview goes out as a PDF note with its data appendix in Excel,
and task152 shares no other axis with this build. Same world type as task146 (a bank desk previewing an official
release): different release, different driver, line on the card.

**Same-puzzle and same-driver tests.** Gap time, decisive G1, decision `quantity_figure`, Gate G
`decomposition_attribution`: no card on file carries either triple, lineage included (the guard's structural tests are
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
  named target release): the call is struck against the advance estimate itself, and the pilot validates out of sample
  on the desk's own real-time filings; the decisive step is not a vintage choice (`## Tried and rejected`).
- task152's design note (the lane's last ship): its corridor discipline (every defensible construction of the golden in
  the bin, every rival a set distance out) is the model for this ladder.

**World.** A fictional English-speaking country of about 7 million with its own floating dollar; a coal, LNG and dairy
exporter that imports most of its machinery, vehicles and consumer durables. The Statistics Office publishes quarterly
GDP in three estimates (the advance about 30 days after the quarter, the second about 60, the third about 90), volumes
at the average prices of the previous calendar year (2025 for the quarters of 2026) and the headline as the change on
the previous quarter at a compound annual rate; it also publishes the producer and trade price indexes. Trade and
Business Statistics (TBS), a unit of the Department of Industry, publishes the monthly bulletin "Merchandise trade and
business stocks": goods exports and imports from customs entries, and wholesalers', retailers' and manufacturers' sales
and stocks from its monthly business survey. On 13 July 2026 a failed storage migration took TBS's processing system and
data portal down; the June bulletin, due on Wednesday 22 July, came out on Tuesday 28 July as a PDF with its tables,
the portal still down. On Friday 24 July the Office announced that the advance estimate would be published as scheduled
on Thursday 30 July and would incorporate the June results. The dollar fell in two legs, in late February after the
Reserve Bank's surprise rate cut and the fall in the coal price, and in the first days of June after the sovereign
rating downgrade; import prices rose in March and again in June. Tarbert Bank (fictional) is a commercial bank whose
economics desk sends clients a GDP preview at 18:00 the evening before each advance estimate; from the June quarter of
2022 to the March quarter of 2026 it ran its line-by-line tracker as a pilot and logged each quarter's filed lines beside
the advance estimate's.

## Default path

Target figures at the draw; the built figures replace them at stage 3 (`generator/checks.py`).

1. Read the Office's user guide and notice: the advance estimate is the change in GDP volume on the March quarter at a
   compound annual rate, the June bulletin is in it, volumes are at 2025 prices, contributions are each component's
   change as a share of March-quarter GDP.
2. Take the desk tracker's June-quarter contributions for every line the bulletin does not feed (household consumption,
   government, dwellings, business investment, farm and other stocks, services trade).
3. Build goods exports and imports from the bulletin's June figures and its revised April and May, deflated section by
   section with the export and import price indexes rebased to 2025, and extend the March quarter's published volumes by
   the quarter's change.
4. Build business stocks: each industry's end-March and end-June book value from the bulletin, each divided by that
   month's industry price index rebased to 2025, the change in volume, less the March quarter's published change in
   business inventories, as a share of March-quarter GDP.
5. Sum the contributions and compound to an annual rate.

Ends on: 1.1 per cent (target; built figure at stage 3).

Golden: 1.6 per cent (target): the same lines, with each industry's end-March and end-June book value divided by the
average of its price index over the months its stock-to-sales ratio covers at that date.

## Stump sentence

Taking the desk's track for every line the late bulletin does not feed, building goods trade from the bulletin and
deflating each industry's end-March and end-June book-value stocks by that month's price index, the textbook removal of
holding gains, files 1.1 per cent against the golden 1.6; the step that lands it there is reading a book value as if its
goods had been bought at the quarter end's prices, when each industry's stock was bought over its own turnover period,
partly before the March and June legs of the import price rise, so the June volume comes out too low and the March one
too high.

## Three rules

- **Task type:** economics-econometrics, forecasting-forecast-evaluation (serves Forecasting): a bottom-up forecast of the
  statistical office's first release of June-quarter GDP growth, built from the release's own source data the evening
  before and validated against the office's advance estimates over the desk's sixteen-quarter pilot.
- **Domain test:** the quantity that decides the call is the volume of business inventory investment the advance estimate
  will carry, which national accountants measure by revaluing businesses' book-value stocks at the prices of the weeks
  the goods were bought in, over each industry's stockholding period, before taking the change, and which a GDP desk
  replicates from the trade and stocks bulletin and the producer price indexes the office deflates with.
- **Swap:** "what growth a hospital's patient-day index will show next quarter" keeps a call on an index and a monthly
  source, but book values carried at cost, a stockholding period read from a stock-to-sales ratio, producer prices
  rising in two legs and an expenditure aggregate summed from contributions at 2025 prices have no counterpart, so what
  decides the figure stops making sense.
- **Layer 1:** the June bulletin delayed by TBS's outage and published as a PDF with tables while the portal was down
  (TBS's processing system); the bulletin's revised April and May figures overlapping the portal download's earlier
  vintage (TBS's monthly revision cycle); price indexes on a 2019 base against volumes at 2025 prices (the Office's
  price statistics and national accounts bases); values in thousands of dollars in the bulk download and in millions
  in the bulletin and the Office's tables (TBS's portal and publication formats); seasonally adjusted stocks and sales
  beside unadjusted price indexes (the survey's adjustment and the price statistics' practice); the tracker's own line
  labels against the Office's component names and the pilot log's layout change when the desk split business investment
  in 2024 (the desk's own workbooks); contributions in points of the previous quarter's GDP beside a headline at a
  compound annual rate (the Office's presentation). None is placed to be caught, and each is asserted neutral (R2).
- **Layer 2:** `field_method`: the turnover method behind the inventory valuation adjustment, the national accounts'
  own way of taking a volume change out of book values; the methodological choice that flips the call is the price a
  book value is divided by: each industry's own prices over the months its stock covers, at both quarter ends, against
  the quarter end's price (the textbook removal of holding gains) or the quarter's average price.
- **Decisive step:** revalue each industry's end-March and end-June book-value stock at the average of its price index
  over the months its stock-to-sales ratio covers at that date, so that the stock is read at the prices it was bought
  at, then take the change in volume at 2025 prices.
- **Not semantics:** every field (book value, sales, stock-to-sales ratio, the price indexes and their base, exports
  and imports by SITC section) and every filed definition (the advance estimate's headline, volumes at 2025 prices,
  contributions, the change in inventories as a change in volume) is read the same way by the easy routes; no field,
  code or definition says when the goods in a month-end stock were bought or at what price, and the default path reads
  them all correctly and still files 1.1.
- **Not rule application:** no shipped sentence says how a book value becomes a volume; the user guide defines the change
  in inventories as a change in volume at 2025 prices and lists its sources, and executing every filed sentence word for
  word gives the month-end deflation, 1.1 (asserted in `checks.py` as R3c); no filed rule or procedure performs the
  revaluation over each industry's turnover period.
- **Analyst test:** a strong analyst who takes the desk's track for every line the late bulletin does not feed, builds
  goods trade from the bulletin section by section and deflates each industry's end-March and end-June stocks by that
  month's price index files 1.1 per cent; deflating at each quarter's average price files about 2.0; revaluing only the
  June end files about 2.0 as well; only each stock revalued over its own turnover period at both ends files 1.6
  (executed on the clean truth at stage 3, R3a and R3b).
- **Estimand:** the prompt and the Office's user guide: the percentage change in GDP volume (2025 prices) from the March
  quarter to the June quarter of 2026 at a compound annual rate, as the advance estimate published on 30 July 2026 will
  show it, rounded to one decimal; the population (the June quarter's expenditure on GDP), outcome, window, unit,
  comparison and rounding are filed, the method is not.
- **No decoy:** no memo, draft, briefing, client note or stakeholder figure states or argues a June-quarter call, an
  inventory volume or a revaluation; the desk's tracker carries no total and leaves the bulletin's three lines blank
  until the bulletin; the economists' poll (a distractor) states forecasters' views collected before the bulletin and is
  never the stump.
- **No certified replay:** no published figure the golden reproduces ships for the June quarter; the pilot's advance
  estimates are realised outcomes with the office's own noise, used to compare methods out of sample, and no method is
  recovered from them; no table states a volume of stocks, a replacement cost or an inventory valuation adjustment.
- **Lesson:** a stock reported at what its holder paid is priced at the weeks the goods were bought in, so its volume must
  be read at those weeks' prices, industry by industry over each one's own turnover period and at both ends of the
  period; the quarter end's price misreads a price rise inside the turnover period as a fall in volume. No build on file
  teaches the revaluation of a book-value stock.

## Readability screen

Stage 2.

## Semantic fork table

Stage 2.

## Ladder

Stage 2.

## Closure table

Stage 2.

## Literal reader

Stage 2.

## Oracles

Stage 2.

## Ask sheet

Stage 2.

## Tried and rejected

- The seed's research memo filing the desk's tracking (each line rebuilt from the handbook's source at its latest
  values, consumer services extrapolated with total private hours): shipping it files how the nowcast is computed,
  rule application; not shipped.
- The seed's premise that the agency froze its inputs on an unpublished cut-off, so the late report's lines carry the
  agency's own projections: withheld, it is a hidden rule; stated, the call is rule application; inferred from past late
  sources in the pilot, it is a cut-off recovered from published figures on small counts. The Office's notice states the
  June bulletin is in the estimate.
- A real-time-vintage calibration as the decisive step (the desk's bias measured on tracks rebuilt from the sources'
  latest vintage against the advance estimates): the pilot log carries the desk's real-time inputs, so the natural
  calibration is already real-time, and any sixteen-quarter calibration in the golden moves the call a bin under one
  standard error; kept out of the golden.
- A stale consensus updated by the bulletin's news as the golden: the decisive step would be reading the poll's closing
  date, a field reading; the poll ships as a distractor.
- The agency's month-three projections for missing sources recovered from its published assumption tables: a hidden rule
  recovered from published figures.
- A pay-timing effect in the government's cash outturn as the decisive step: visible in the monthly series and fixed by
  counting paydays, a rule; kept for the ask layer if needed.
