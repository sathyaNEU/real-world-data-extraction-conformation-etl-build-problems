# task458 design note

Architecture 3, drawn 2026-11-02 as a re-root (architecture 2, a city's meter rates from midday occupancy in General Statistics & Data Science, spent at the stage 4 judge; architecture 1, a Medicaid plan's county designation in healthcare delivery, spent on its ask layer: see `## Architecture 2 record`, `## Architecture 1 record` and `## Tried and rejected`). A new world, dataset, generator and shell, on the coordinator's route into the accounting house domain: Ashlund Home Group's FY2026 consolidated stock provision, and whether it takes the borrowing base on the group's revolving facility below what was drawn at the year end.

## Draw

Ten-line summary (sent to the main thread at registration; figures are fixed at build):

1. **Pairing:** house domain Accounting, Audit & Forensic Analytics (`accounting-audit-forensic`, subdomain `general-ledger-close-consolidation`), naming client domain General Statistics & Data Science and its task type `data-integration-record-linkage-entity-resolution`; objective Data Extraction & Conformation (ETL).
2. **Niche:** a UK homewares and hardware importer-distributor group's FY2026 consolidated stock provision under IAS 2, conformed from three trading subsidiaries' stock registers and order books (UK, Ireland, Netherlands; three ERPs, sterling and euro, eaches and cases) and the records of the group's own clearance outlet chain (Valuehall, five stores) and its trade buyers, in the year a lost DIY customer programme and a failed smart-lighting range left far more excess stock than the outlet can clear in 2027; the provision decides whether the audited accounts breach the revolving facility's borrowing base covenant.
3. **Default path against golden:** the default values the GBP 7.2m surplus (excess beyond twelve months' net shipments, with Valuehall's own stock) at the 0.617 Valuehall recovers on what it sells, books GBP 2.8m and finds GBP 1.0m of headroom on the borrowing base (no waiver); the golden caps what Valuehall can sell in 2027 at its stocked trading-day rate (GBP 2.48m), values the other GBP 4.72m at the trade buyers' 0.102, books GBP 5.2m and finds a GBP 0.5m shortfall (seek the bank's waiver before the accounts are delivered).
4. **Stump sentence:** under `## Stump sentence` once the ladder is measured; in one line, the outlet's recovery rate looks proportional to what it is sent only because a store opened each year the excess grew, and its stores' stocked weeks show the cap.
5. **Shape:** 03, a bridge from the group's year-end stock at cost to the provision and the covenant headroom, each reconciling item by subsidiary and division; decision `go_hold_or_stop` with the provision as the call's critical component; question form `whether`.
6. **Deliverables:** `Ashlund_FY2026_stock_provision.xlsx` (the bridge, the excess by company and division, the disposal working, the 2025 shipments and the conformed line-level excess) and `FY2026_stock_provision_note.pdf` (a one-page note to the audit committee).
7. **Nearest driver (`guard.py mechanisms`, `check`):** 0.08 task252 v1 (a channel's mean error), 0.06 task181 draft, 0.06 task301 v1; none values a surplus through a channel capped by its own stocked throughput. NOTE `test.same_driver_older` (gap time, pattern C, Gate G binding_constraint) differentiated on the card against task456; task106 (the approved F3 build) differentiated too.
8. **Guard:** PASS on the registered card (2026-11-02), the NOTE above only.
9. **Ask records:** the 2025 order books, what each division shipped to customers the year before the excess, in units (the Irish company's old-system archive prints case quantities under the each unit it converted to in July 2025) and in invoiced pounds (the UK company's July 2025 price credits, each raised from its order's credit screen on the order's first line whatever lines it corrects); both screened as code against the honest cracker before the pack was cut (`## Ask sheet`; the draw's first two records and a first Ask B device were replaced, `## Tried and rejected`).
10. **Layer 1:** three ERPs (the Dutch subsidiary's own article numbers through its table with superseded group codes, Irish case lines against eaches, euro at the year-end and average rates filed once in the rate table, the Irish company's old system's 2025 archive), Valuehall's weekly store trading summary with shut and thinly stocked weeks, a week cut at the year end and stores opening part-way through 2021 to 2025, order books with transfers to Valuehall, cancellations and returns under each system's own convention.

- **Heart at stage 3 (2026-11-02): WARN, not BLOCK.** Nearest stump text 0.12 task306 v4 (a strategy's backtest alpha net of the turnover cost the desk's own executions show): a trading cost on turnover, not a disposal channel capped by its stocked throughput, nothing shared. `repeat.deliverables` pdf+xlsx against task501 v5: a provision workbook and a committee note are the genre a controller files, the shell's question form and openers differ, and voice-check holds the set under its corpus quota. `test.same_driver_older` against task456 v2 stays differentiated on the card (a fixed solvent capacity behind an oxidizer is a per-candidate engineering limit; here a sales capacity is read off the channel's own stocked periods behind a recovery its growth kept steady).
- **Card:** `.claude/skills/fingerprint/cards/task458.json`, architecture v3, registered 2026-11-02 and `check` re-run on the registered card (PASS, one NOTE). Architecture 2's identity is in the card's lineage with `architecture_spent` and its fate; architecture 1's stays there; both shells sit in `lineage_shells`.
- **Axes redrawn at the draw, each to the honester label:** gap `objective` first BLOCKed `test.same_puzzle_older` and `test.same_driver_older` (the objective-and-C signature is spent in six and ten older builds), and `time` is the honester first gap anyway: the outlet's recovery was measured at volumes its stores could absorb, and the 2027 window holds a volume the record never saw (`objective` kept second). The call is the covenant verdict, `go_hold_or_stop`, with the provision as its critical component; `quantity_figure` with `how-much` also repeated task467, the last build. Forum `committee_or_panel` (the audit committee approves the provision and the covenant position), forcing event `period_close`, organisation `other` (wholesale importer-distributor; the vocabulary's retailer key is the wrong trade and is banned in the window besides), role `finance_controller`, context artifact `register`, calibration form `settled_transaction_ledger` (the outlet's and jobbers' settled sales of past years' excess). Personas Caroline Burns (group financial controller) and Liam Elliott (Valuehall operations) from `guard.py names --geo "United Kingdom" --seed 458`.
- **Why this route:** every ETL cell measured closed for an honest unrepeated driver in this session (seasonal adjustment, census-register, emissions inventory: `## Tried and rejected`); on the coordinator's word the draw takes a house domain whose client domain carries the data-integration task type, in a world no ETL cell has used. The work is data integration (three subsidiaries' registers, order books and transfer records, the outlet's tills and goods-in records and the jobbers' contracts conformed into one group stock valuation); the house domain is the honest label because the decision is a year-end consolidated stock provision and the covenant it tests.
- **The ETL move (guide-to-prompt section 1):** split a total between two causes, here between the two channels that will realise the excess: the forcing file, Valuehall's own till and goods-in records by store and week, pins a structure (the throughput a stocked store sells, and the store count through 2027). Reading every file correctly is not sufficient: the registers, order books and transfer records read right leave the analyst choosing how the excess will be realised, and the outlet's yearly recovery rate on what it was sent reads the same in every year on record.
- **Shape and shell:** shape 03; question form `whether`; deliverable set and openers drawn with the prompt at stage 2 under the corpus quotas, none of architecture 1's (which, put, round, csv+xlsx) or architecture 2's (what, the, occupancy, csv+docx).
- **World:** Ashlund Home Group (fictional), an East Midlands importer-distributor of own-brand homewares and hardware sourced from factories in China, Vietnam and India, selling to retailers, DIY chains and marketplaces through Ashlund Home Ltd (UK, sterling), Ashlund Home Ireland Ltd (Dublin, euro) and Ashlund Home BV (Tilburg, euro), each on its own ERP; five divisions (Kitchen and Dining, Storage and Laundry, Lighting and Electrical, Tools and Hardware, Garden and Outdoor). Valuehall Stores Ltd, a group company, runs five clearance stores in the East Midlands opened one a year from 2021; the subsidiaries transfer their surplus lines to it at cost, and what it cannot take goes to jobbers in mixed pallet lots. The group's revolving credit facility tests consolidated tangible net worth at each audited year-end against a floor. Forum: the audit committee, which approves the FY2026 provision and the covenant position before the auditors sign in February 2027.
- **Data-native sentence:** Valuehall's stores sell what shoppers carry out of five buildings, not what the group sends them: when a store's clearance stock is deep its weekly sales level off at what its floor and footfall move, and the outlet's recovery on what it was sent held steady only because a store opened each year as the group's surplus grew; the surplus the lost DIY programme and the lighting range left at the 2026 year-end is about three times what five stores can sell in 2027.
- **Abstraction sentence (stumping Part 6), and the approved builds it is not:** "a surplus is realised through a channel whose recovery looked proportional to what it was sent only because its capacity grew with the surplus; its own stocked periods show a fixed throughput, and the excess over it goes to a channel that recovers far less." task106 (approved) sizes each candidate against a known shared pool and adds them, a joint-allocation double-booking; no approved build reads a channel's capacity off its own stocked periods behind a rate that the capacity's growth kept steady.
- **Lessons 7, 9, 10, 11, 12 and 13 at the draw:** no shipped document states a recovery rate, a provision rate, a capacity, an outlet budget or a provision for any line or division, and no draft provision or committee paper proposes a figure (9, 11; asserted in `checks.py`); the default path is the analyst's own model (a recovery rate measured on the outlet's history), refuted by the outlet's own stocked store-weeks (11, 12: the back-test is past years' excess and how the outlet and jobbers realised it, including 2023, when three stores were saturated); the filed WHAT (IAS 2's net realisable value, the provision's window and the covenant's definition) names no channel, capacity or rate (10); every assumption the golden makes (no sixth store, a steady store-week throughput, the jobbers' recovery, demand at its 2026 run rate) is asserted on the clean truth (7); every window and rounding the call depends on is filed in the owning document or the asking sentence (13).
- **Sources, one line each:**
  - `stumping/references/client/two-layer-task-design.md`, allocation_constraints (capacity and queueing): the outlet's store-weeks are the binding capacity, `own:excess-stock-realised-through-a-shared-clearance-outlet-at-its-store-week-throughput`.
  - `stumping/references/strategies.md` F3 binding constraint (the metric is correct and is not what the decision is scored on; the limit is shared across candidates): the recovery rate is right on what the outlet took; the realisable value is capped by what it can take.
  - `stumping/references/client/layer2-rigor-patterns.md`, data integration card 1 (propagate integration error into the estimate): the conformation of three ERPs' registers into group lines is Layer 1 here and is asserted neutral on the call.
  - `dataset-generation/references/layer1-messiness.md`: several sources for one picture, imperfect keys, units and currencies, real coverage; none on the decisive step.

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' grain, with the field's own method for
the deciding quantity in it: an excess-and-obsolescence reserve that values the excess at the clearance channel's
historical recovery.

1. Reads FIN-07 2.1 to 2.6 and clauses 1.1 and 21 of the facility extract: excess is stock beyond twelve months' net
   shipments to customers, carried at the net proceeds ex VAT from its disposal in 2027 through Valuehall and trade
   buyers; the borrowing base is 62.5 per cent of inventories at the lower of cost and net realisable value.
2. Conforms the three registers (AHL's bins summed; AHI's case lines at their pack quantity; AHB's semicolon file with
   decimal commas, its articles through its group-code table and superseded codes to their successors), euro at the
   0.8648 year-end rate, and adds Valuehall's stock at its week cut at 31 December: GBP 44.60m at cost.
3. Nets each line's 2026 despatches and returns to customers in its own company (cancelled lines and transfers to
   Valuehall and group companies out, AHI's return receipts subtracted): excess GBP 7.00m (AHL 5.08m, AHI 0.50m, AHB
   1.43m); with Valuehall's GBP 0.20m the surplus to clear in 2027 is GBP 7.20m.
4. Measures the clearance channel the way the reserve does: Valuehall's proceeds ex VAT over its cost of sales, 0.617,
   between 0.615 and 0.622 in every year from 2021 to 2026.
5. Values the surplus at that recovery: proceeds GBP 4.44m, provision GBP 2.76m; inventories after it GBP 41.84m.
6. Borrowing base 62.5 per cent of GBP 41.84m is GBP 26.15m against GBP 25.12m drawn: headroom GBP 1.03m.

Ends on: GBP 2.8m provision, GBP 1.0m headroom, no waiver needed
Golden: GBP 5.2m provision, GBP 0.5m shortfall, seek a waiver

## Stump sentence

The default path books a GBP 2.8m provision and finds GBP 1.0m of headroom, so no waiver, because it values the whole
GBP 7.2m surplus at the 0.617 Valuehall recovers on what it sells, a rate steady every year only because a store opened
each year as the surplus grew; a stocked Valuehall store sells about GBP 1,377 at cost a trading day whatever it holds,
so the five stores' 1,801 trading days in 2027 take GBP 2.48m, the other GBP 4.72m goes to trade buyers at 0.102, and
the provision is GBP 5.2m with a GBP 0.5m shortfall.

## Three rules

- **Task type:** data-integration-record-linkage-entity-resolution in General Statistics & Data Science (house domain accounting-audit-forensic, subdomain general-ledger-close-consolidation), which serves Data Extraction & Conformation: three ERPs' registers and order books, Valuehall's stock system, the lot register and the rate table conformed into one group stock valuation that the provision and the covenant test run on.
- **Domain test:** the deciding quantity is the net realisable value of the group's year-end surplus under IAS 2, the cash its disposal routes will return in 2027; the field values excess stock at its clearance channel's historical recovery, and here what that channel can take in the window decides the value.
- **Swap:** "does the provision against the hospital's waiting list leave its borrowing base above what was drawn" stops making sense: nothing on a waiting list is carried at the lower of cost and net realisable value, no clearance chain sells it, and no bank lends against it.
- **Layer 1:** three ERPs (AHL sterling eaches by bin; AHI's new system in euro with case lines and return receipts, its old system's 2025 archive; AHB's Dutch semicolon export with decimal commas, its own article numbers and a table with superseded group codes), transfers to Valuehall inside the order books, cancelled lines and customer returns, a week cut at the year end in Valuehall's stock system, euro at a year-end and an average rate; each produced by the system that holds it, nothing placed to be caught.
- **Layer 2:** allocation_constraints (capacity and queueing): the surplus is realised through a shared channel whose stocked throughput, not its recovery rate, limits what it takes in the window, and the excess over that limit goes to the channel that recovers far less.
- **Decisive step:** seeing that Valuehall's yearly sales grew with its store count and not with what it was sent, and reading what its five stores can sell in 2027 off their stocked trading days, so the surplus beyond that is valued at trade prices.
- **Not semantics:** every field read right (cases at their pack quantity, AHB's decimal commas and articles, euro at the year-end rate, returns, cancellations and transfers) gives the same GBP 7.20m surplus and the same 0.617 recovery; the easy route values it all at that recovery and files no waiver.
- **Not rule application:** FIN-07 2.4 files the outcome (net proceeds ex VAT), the routes and the window, and no filed rule says how much either route takes; the enumerated family (no limit, the blended recovery on everything Valuehall received, yearly sales fitted on goods in, 2026 sales, every full week, stocked weeks from GBP 20,000 to 60,000, mean or median, January sale in or out, part weeks prorated, each recovery and trade-rate window) spans a provision of GBP 2.76m to 6.47m; the standing family (no limit, the blend and the fit refuted by 2023 and by the stores' flat stocked rate) spans GBP 5.13m to 5.25m over 5,440 members (`## Pre-ship check`), every one filing the waiver and the same four covenant figures at the units the prompt grades them in; the ruling-out is the store weeks' own record, no sentence.
- **Analyst test:** a strong analyst who conforms every file and reads every rule values the GBP 7.2m surplus at Valuehall's 0.617, books a GBP 2.8m provision and finds GBP 1.0m headroom, no waiver needed; the golden books GBP 5.2m and finds a GBP 0.5m shortfall.
- **Estimand:** FIN-07 2.2 to 2.6 (excess beyond twelve months' net shipments to customers in the same company; carried at the net proceeds ex VAT from disposal in the year after the balance sheet date through Valuehall and trade buyers; Valuehall's own stock measured with the excess; assessed on the stock held; euro at the year-end rate) and the facility's clauses 1.1 and 21 (62.5 per cent of the Group's inventories at the lower of cost and net realisable value against the Outstandings at close of business on 31 December).
- **No decoy:** nothing is planted: no draft provision, committee paper, prior-year memo, auditor letter, budget or capacity figure ships; 2023's surplus at the stores and the February 2024 trade lots are an ordinary year in the outlet's record; no document states a recovery, a rate, a provision or an answer (checks.py doc.neutral).
- **No certified replay:** there is no certified figure to reproduce; the golden's limit is estimated from the store weeks and checked on 2023, a year the estimate is never fitted to reproduce.
- **Lesson:** a clearance channel's recovery rate is half of a net realisable value; when the surplus outgrows what the channel can sell in the window, the channel's own stocked periods decide how much goes at the low price, and no build on file values a surplus through a channel capped by its stocked throughput behind a rate the capacity's growth kept steady.

## Survivor anatomy

- **Actor:** Valuehall's 2027 limit has no column: the store weeks hold goods in, sales, trade-outs and closing stock, and the limit is a relation among them (sales level at about GBP 1,377 a trading day once a store holds three weeks of stock, whatever more it holds).
- **Link:** a comparison the reserve never asks for: the surplus against what the chain can sell in the window, read within store weeks (sales against stock held) and across years (sales against store-days, not goods in); no key, no clause.
- **Reflex:** the field's method, an excess-and-obsolescence reserve at the clearance channel's recovery, is rung 0 and files GBP 2.8m and no waiver.
- **Back-test:** the textbook route validates: Valuehall's recovery on what it sells is 0.615 to 0.622 in every year, and its yearly sales tracked what it was sent in four of six years.
- **Second use:** every file the decisive step reads is in the pack for the default path: the store weeks give the recovery and Valuehall's year-end stock, the store plan shows Valuehall trading in 2027 (FIN-07's route exists), the lot register gives the trade rate.
- **Shock:** 2023's full stores and the February 2024 trade lots read as one ordinary clear-out in a six-year record; the stocked rate is flat by store, by year and by promotion; no store, year or line is an outlier on any sort.
- **Pins:** FIN-07, the group's own policy, files the outcome, window, routes and population; no filed sentence names a limit, a throughput, store-days as a limit, or how much either route takes (checks.py doc.neutral on all three documents).

## Readability screen

| Rung | What reads it | Verdict |
|---|---|---|
| 0 the surplus at Valuehall's recovery on cost of sales (default path) | nothing: the recovery is steady in every year | silent |
| 1 the blended recovery on everything Valuehall received, its own trade lots included | nothing: the 2024 trade lots sit in the blend as one ordinary clear-out | silent |
| 2 Valuehall's yearly sales extended in line with what it was sent | nothing: four of six years sold about what they were sent | silent |
| 3 (decisive) Valuehall's 2027 sales capped at its stocked trading-day rate, the rest at trade prices | nothing in any file or sentence names a limit; only sales against stock held within store weeks, and 2023 against its trading days, show it | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | Valuehall's stock at 31 December | close of the stock system's week cut at 31 December (28 to 31 December, 4 trading days) | close of the week to 3 January; Valuehall's stock left out | same call | the file's last week is cut at the year end; same call without it (checks SF1) |
| SF2 | net shipments | despatches less customer returns | despatches only | same call (provision GBP 5.10m) | FIN-07 2.2 "despatches less customer returns" |
| SF3 | a line whose 2026 net shipments are negative | excess is the stock held | excess above the stock held | same call (one line) | FIN-07 2.2 "the quantity of a line held" |
| SF4 | AHI's case lines | quantity times the line's Qty. per Unit of Measure | cases read as eaches | same call | the register's own unit and pack columns |
| SF5 | euro stock | year-end rate 0.8648 | the 2026 average | same call | FIN-07 2.6 and the rate table's note |
| SF6 | cost | each company's landed cost in its register | a group standard cost | same call (none ships) | FIN-07 2.1 |
| SF7 | proceeds | ex VAT | including VAT | waiver either way, figure moves | FIN-07 2.4 "excluding VAT" |
| SF8 | selling costs | not deducted | Valuehall's store costs deducted | not computable from the pack | FIN-07 2.5 |
| SF9 | window | disposal in the year after the balance sheet date | clearance over several years | no waiver (rival) | FIN-07 2.4 "in the year after the balance sheet date" |
| SF10 | Valuehall's own stock | in the surplus with the excess | valued apart at Valuehall's rate | same call (GBP 5.09m) | FIN-07 2.4 "measured with the excess" |
| SF11 | 2027 trading days | the store plan's 1,801 | 365 days a store | same call (GBP 5.18m) | the store plan's table |
| SF12 | trade-buyer rate window | all lots 2021 to 2026 | 2026, 2025 to 2026, 2024 to 2026 | same call | records converge (checks SF12) |
| SF13 | Valuehall recovery window | 2021 to 2026 | 2026, 2025 to 2026 | same call | records converge (checks SF13) |
| SF14 | eligible inventory | the Group's inventories, Valuehall's included | Valuehall's stock left out | same call | clause 1.1 "the inventories of the Group" |
| SF15 | drawn balance | Outstandings at close of business on 31 December, GBP 25.12m | the year's average | same call | clause 1.1 Outstandings and Test Date |
| SF16 | exceed | Outstandings above the base | a tie | same call (GBP 0.49m clear) | clause 21.1 |
| SF17 | the provision's unit | the nearest million, rounded once from the unrounded figure | the nearest 0.1 million, which the defensible family crosses (GBP 5.13m to 5.25m) | same call | the prompt's rounding clause; every member sits in one million bin, GBP 0.25m clear of its edges (checks SF17.provision) |
| SF18 | inventories, base and shortfall | inventories and base to the nearest 0.5 million, the shortfall to the nearest 250,000, each from the unrounded provision | 0.1 million, which the family crosses for the inventories and the base | same call | the prompt's rounding clause; every member sits in one bin of each, GBP 0.07m or more clear (checks SF18.inventories, SF18.bb, SF18.shortfall) |
| SF19 | stock to be assessed | the stock held at 31 December | with surplus arising in 2027 sharing the stores | same call (only raises it) | FIN-07 2.5 "assessed on the stock held at the balance sheet date" |
| SF20 | superseded codes in AHB's table | the successor's line (same division) | the retired code | same call | the master's Superseded By |
| SF21 | an item's division | the master's division | none other ships | same call | one division per code |
| SF22 | 2025 shipments to customers | eaches, returns netted, cancelled lines and transfers out | transfers in | not the call (asks) | the prompt "to customers"; FIN-07 2.2 |
| SF23 | 2025 net value invoiced in pounds | line values net of returns and price credits, euro at the 2025 average 0.8573 | monthly averages, the year-end rate; credits left out | not the call (asks) | the prompt "the net value invoiced for them"; the rate table's note "Income statement items are translated at the year's average rate" |
| SF24 | Lumio's twelve months | its ten months since the March launch, as shipped | annualised | same call (GBP 5.12m) | FIN-07 2.2 "in the twelve months to that date" |
| SF25 | the stores' working stock at the end of 2027 | the whole surplus is disposed of in 2027; the stores' end-2027 stock comes from 2027's own surplus | three weeks of stock per store held back from the trade buyers and valued at Valuehall's rate in 2028 | same call | FIN-07 2.4 "from its disposal in the year after the balance sheet date" and 2.5 "assessed on the stock held at the balance sheet date" |

## Ladder

| Rung | Route | Provision | Borrowing base | Headroom (shortfall) | Call |
|---|---|---|---|---|---|
| 0 | the GBP 7.20m surplus at Valuehall's 0.617 (default path) | GBP 2.76m | GBP 26.15m | 1.03m | no waiver |
| 1 | the blended recovery 0.562 on everything Valuehall received, its trade lots included | GBP 3.16m | GBP 25.90m | 0.78m | no waiver |
| 2 | Valuehall's yearly sales fitted on goods in (slope 0.78) and extended to the surplus | GBP 3.41m | GBP 25.75m | 0.63m | no waiver |
| 3 (golden) | GBP 1,376.5 a trading day in 772 stocked full weeks times 1,801 trading days takes GBP 2.48m at 0.617; GBP 4.72m to trade buyers at 0.102 | GBP 5.19m | GBP 24.63m | (0.49m) | seek a waiver |

The call flips at a provision of GBP 4.41m; the nearest default-side rung sits GBP 1.00m below it and the golden GBP
0.78m above. Pricing: a response on rungs 0 to 2 keeps the excess figures and loses the call, the provision, the
inventories, the base and the shortfall. The rungs that land the call (2026 sales, every full week, GBP 5.18m to 5.24m)
each take the decisive step; checks.py counts no route that leaves Valuehall unlimited landing it. Every trade buyer
route (the whole surplus at 0.102, GBP 6.47m) contradicts FIN-07 2.4's Valuehall route.

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | the three companies' lines held at 31 December 2026 and Valuehall's stock | FIN-07 2.2 and 2.4 filed; C1 |
| 2 Unit of account | a line in a company | FIN-07 2.1 and 2.2 |
| 3 Attribution window | demand in the twelve months to 31 December 2026; disposal in 2027; asks in 2025 | FIN-07 2.2 and 2.4; the prompt |
| 4 As-of dating | the balance sheet date; Valuehall's week cut at the year end | SF1 |
| 5 Version basis | registers and order books as extracted; superseded codes to their successors | SF20, C1 |
| 6 Denominator | recovery over cost of sales; trade price over stock at cost | records converge, SF12, SF13 |
| 7 Weighting | stocked trading days pooled; per store and per year within 2 per cent | C1, checks L7 |
| 8 Window length | recovery and trade-rate windows | C1, SF12, SF13, SF17 |
| 9 Boundary inclusivity | Outstandings exceed the base | SF16, GBP 0.49m clear |
| 10 Rounding path | each sterling figure once from unrounded; units and values once | SF17, SF18 |
| 11 Tie-break | no ranking | not needed |
| 12 Maturity and censoring | Lumio's ten months since launch as shipped | SF24, same call |
| 13 Order of operations | excess line by line, then the surplus split across the routes | uniform rates make the order immaterial, C1 |
| 14 Row order | no step reads file order | C1 |
| 15 Duplicate resolution | no duplicate rows; identical projected lines are separate order lines | full rows unique, C1 |
| 16 Identity normalisation | AHB articles through AHB's table; superseded codes through the master | SF20 |
| 17 Netting against gross | net shipments; a negative net caps the excess at the stock held | SF2, SF3 |
| 18 Dimensional units | eaches and sterling | SF4, SF5 |
| 19 Code and status semantics | Cancelled and Geannuleerd out; RTN, CRN, Return Receipt and Retour are returns; group companies are transfers | the systems' own codes; FIN-07 2.2 |
| 20 Integerisation | none | not needed |
| 21 Clause scope | clause 21.1 on the 31 December 2026 Test Date on the audited accounts | clause 21.2 |
| 22 Forward window contents | Valuehall's 2027 trading days from the store plan; no sixth store; the stock held | SF11, SF19, checks L7.five_stores |

## Literal reader

Executed word for word, FIN-07 2.2 gives GBP 7.00m of excess and 2.4 carries it, with Valuehall's GBP 0.20m, at the
net proceeds ex VAT its disposal returns in 2027 through Valuehall and trade buyers. No sentence says how much each
route takes, so the literal reader must estimate Valuehall's 2027 sales; the records rule out every reading that leaves
it unlimited (in 2023 the stores were sent GBP 2.35m and sold GBP 1.36m, the stocked rate's prediction being GBP
1.36m; stocked sales are flat in the stock held, by store, by year and in the January sale), and every reading that
reads the limit from the stores' own trading days files the same four covenant figures at the prompt's units (SF17, SF18). Every other row of the fork table
is same call or ruled out by a quoted sentence. The asks' readings are each forced row by row (Ask sheet).

## Oracles

- `generator/figures.json`, written by golden.py through calc.py from the cut pack.
- `generator/verify.py`: an independent recompute of 19 graded figures with the standard library and openpyxl only.
- `generator/checks.py`: 95 assertions (input gates, SF1 to SF25, the three-rules block, lesson 7's assumptions, the
  2023 back-test, both devices, the documents).
- `generator/ceiling.py`: the careful-solver cracker, the stops and the pair arithmetic on the cut pack.

## Ask sheet

The asks are the year before the excess, which the committee needs whatever the call: what each division shipped to
customers in 2025, in units and in invoiced pounds, against the 2026 shipments the excess rests on. They read rows the
call never reads (2025 order lines; the AHI archive is 2025 only) and columns it never reads (invoiced value).

- **Ask A, net units each division shipped to customers in 2025 (5 figures, nearest 1,000).** H18 home: the audit
  trail of the demand the excess lost. Files: AHI_legacy_sales_archive_2025.csv (Doc Type, Doc Date, Cust Name, Stock
  Code, Qty, UOM, Line Value), the 2025 rows of AHL's and AHB's order books, the item master (Division, Case Qty), AHB's
  group-code table. Primary device (D2, a label taken across a silent switch by a false-clean join to the item's current
  unit): AHI's old system converted its stock unit from case to each on 7 July 2025, and the archive prints every line
  with the item's current unit, EA, so the lines before the switch carry cases. Forced row by row: on 3,055 pre-switch
  customer lines the invoiced value over the quantity is the case quantity times the same item's later price to the same
  customer (checks dev.forcing.cases), and every later line is a whole number of cases. Over-cleaning half: converting
  every archive line at its case quantity (KD 4.68m units over). Hazards: returns under three conventions, cancelled
  lines, transfers to Valuehall, AHB's articles. Pin test: the sentence pins units, customers, 2025 and net; the device
  sits in which unit a row's quantity carries, a dimension no pin names.

  | Reading | KD | SL | LE | TH | GO |
  |---|---|---|---|---|---|
  | golden (pre-switch lines as cases) | 11,743,000 | 7,603,000 | 7,616,000 | 6,215,000 | 2,874,000 |
  | as labelled (cracker) | 11,329,000 | 7,322,000 | 7,408,000 | 5,997,000 | 2,787,000 |
  | every archive line converted | 16,423,000 | 11,006,000 | 9,906,000 | 8,287,000 | 4,007,000 |

- **Ask B, the net value invoiced for those shipments in pounds by division (5 figures, nearest GBP 1,000).** H18
  home: the same audit trail in the money the committee reads. Files: the 2025 rows of
  AHL_sales_order_lines_2025-2026.csv (Order No, Doc Type, Despatch Date, Customer, Item Code, Qty, Line Value), the AHI
  archive, AHB's order book, the item master (Division), the rate table. Primary device (D6, an amount booked at a grain
  above the line it belongs to, placed by the weights the rows record): AHL's list prices rose by range on 1 April 2025
  (2 to 13 per cent); five key accounts were held at their old prices to 30 June, but the hold was missing on many of
  their lines, which were invoiced at the new price. In July AHL credited each overcharged line. Its system takes a
  price-only credit on the non-stock code NS001 (a stock item on a credit line would book goods back in), so the 754
  credits (Doc Type PRICE, no quantity) sit under their original orders on a code no division carries. As booked, no
  credit has a division (dev.impossible.no_division), and leaving them out is not a net value invoiced. Forced row by
  row: each credit equals, to the penny, the overcharge on exactly one line of its order, the line's quantity times its
  excess over the customer's own price for the item before 1 April, and the 262 credited orders carry exactly 754 such
  lines (dev.forcing.price_identity). Over-cleaning half: spreading each credit over its order's lines by value (the
  battery's header-to-items pairing, the cracker's route), over the customer's 2025 lines, or leaving the credits out,
  each misses every division by GBP 13,000 or more. Pin test: the sentence pins pounds, the net value invoiced and the
  year; the device sits in which line a credit belongs to, a dimension no pin names.

  | Reading | KD | SL | LE | TH | GO |
  |---|---|---|---|---|---|
  | golden (each credit on the line whose overcharge it equals) | 41,162,000 | 33,105,000 | 36,168,000 | 29,568,000 | 25,081,000 |
  | spread over the order's lines by value (cracker) | 41,125,000 | 33,126,000 | 36,183,000 | 29,547,000 | 25,104,000 |
  | spread over the customer's 2025 lines | 41,118,000 | 33,130,000 | 36,187,000 | 29,544,000 | 25,105,000 |
  | credits left out | 41,178,000 | 33,172,000 | 36,237,000 | 29,581,000 | 25,137,000 |

- **Main population zero-counts:** the archive has no 2026 row, and every price credit is dated July 2025 and carries
  no quantity (dev.separation); the call reads 2026 customer quantities, the registers, the store weeks, the lots and
  the rcf file, and deleting both devices leaves every call figure unchanged (freeze.py rubric check).
- **Disjoint blocks:** the cases device moves no value and a price credit carries no quantity (checks dev.disjoint), so
  a response that handles one keeps half the ask weight.

| Ask | Cracker route (lands the call, reads every field plainly, runs the battery) | Cracker |
|---|---|---|
| A, units by division (5) | the archive's quantities in the unit it prints, EA | miss |
| B, net value invoiced by division (5) | each price credit on the orphan code paired to its order's item rows by value | miss |
| A and B, the full includer | both devices handled; reproduces figures.json | yes |

Pair ceiling: 31.6 (cracker 45.0 on the call, mirror 18.1 off it); two careful responses on the call at most 45.0 each; the best single-device handler keeps 27.5 of the 55 ask points, 72.5 on the call and 45.6 off it (two disjoint blocks put a one-device handler on the call at 45 plus half the ask weight)
Mirror leakage: 0.0 per cent of ask weight (the mirror runs the cracker's ask routes)
Measured by: generator/ceiling.py on the cut pack (sha256 printed by the script)


## Leak check

`leak.py task458 --asof 2027-01-22`: REVIEW, no LEAK (18 files, 28 golden figures). Each REVIEW ruled:
- Sweep 3, `FIN-07_Stock_Provisioning_Policy.pdf` carries "2.5": the policy's section number (2.5 Net realisable value), not the GBP 2.5 million Valuehall takes in 2027; harmless.
- Sweep 4, the policy shares seven ordinary nouns with the stump paragraph (Valuehall, surplus, stores, record, records, system, year-end): they name the route FIN-07 2.4 files, its scope, the store costs 2.5 leaves undeducted and the cost each company records in its own system; no sentence names a limit, a throughput or how much either route takes (checks doc.neutral); harmless.
- Sweep 6, `trade_lot_register_2021-2026.xlsx` names the three trading companies beside lot costs and prices: it records lots by seller and ranks nothing on the decision question (the waiver); harmless.

## Pre-ship check

Stage 4, pass 1 (2026-11-02). The leak reader was clean (questions 1 to 4 none; question 6 an analytical choice, how
much each disposal route can take; every sweep line harmless). The judge forced the main call (provision 5.19m,
inventories 39.41m, base 24.63m, shortfall 0.49m, every variant 5.17m to 5.21m, breakeven about 4.41m; asks 1 to 6
reproduced; Gate G binding_constraint, analytical_non_defect; Gate H passes) and returned NOT_DETERMINISTIC on ask 7
only, SEND_BACK, a repair on a sound architecture. One repair pass, for one re-judge:

1. **Ask 7.** The as-booked reading of AHL's July price credits (each netted in the division of the item the credit
   screen defaulted to) was coherent. A pin in the asking sentence would hand the careful cracker the reconstruction,
   so the repair is in the rows: AHL's system books a price-only credit on its non-stock code NS001, one credit per
   corrected line, and no division carries that code. As booked, no credit can be placed in a division, and leaving
   the credits out is not a net value invoiced. Each of the 754 credits equals, to the penny, the overcharge on exactly
   one line of its order (dev.forcing.price_identity). The careful cracker finds the orphan code and pairs each credit to
   its order's item rows by value, which misses every division by GBP 14,000 or more (Ask sheet).
2. **The four covenant figures.** The pass-2 report's member (the non-promotion recovery with 1,390 a day) filed
   5.1 against 5.2. Measured over 5,440 defensible members, the 0.1 million bins were crossed, so the figures moved to
   the units the family holds in, by the prompt's rounding clause alone (no method filed, no world re-centred):

| Members | Provision (GBP m) | Inventories after it | Borrowing base | Shortfall |
|---|---|---|---|---|
| golden | 5.193 | 39.409 | 24.631 | 0.489 |
| every member (5440) | 5.128 to 5.245 | 39.357 to 39.474 | 24.598 to 24.671 | 0.449 to 0.522 |
| recovery: all years | 5.162 to 5.241 | 39.362 to 39.441 | 24.601 to 24.651 | 0.469 to 0.519 |
| recovery: 2025 to 2026 | 5.166 to 5.245 | 39.358 to 39.437 | 24.599 to 24.648 | 0.472 to 0.521 |
| recovery: non-promotion weeks | 5.128 to 5.209 | 39.393 to 39.474 | 24.621 to 24.671 | 0.449 to 0.499 |
| recovery: January sale out | 5.145 to 5.225 | 39.377 to 39.457 | 24.611 to 24.661 | 0.459 to 0.509 |
| recovery: 2021 | 5.147 to 5.227 | 39.376 to 39.455 | 24.610 to 24.660 | 0.460 to 0.510 |
| recovery: 2022 | 5.162 to 5.241 | 39.362 to 39.441 | 24.601 to 24.650 | 0.470 to 0.519 |
| recovery: 2023 | 5.153 to 5.233 | 39.370 to 39.449 | 24.606 to 24.656 | 0.464 to 0.514 |
| recovery: 2024 | 5.159 to 5.239 | 39.364 to 39.443 | 24.602 to 24.652 | 0.468 to 0.518 |
| recovery: 2025 | 5.165 to 5.244 | 39.359 to 39.438 | 24.599 to 24.648 | 0.472 to 0.521 |
| recovery: 2026 | 5.167 to 5.245 | 39.357 to 39.436 | 24.598 to 24.647 | 0.473 to 0.522 |
| daily rate: full stocked weeks, GBP 20,000 to 100,000 | 5.151 to 5.221 | 39.382 to 39.452 | 24.614 to 24.657 | 0.463 to 0.506 |
| daily rate: every week, no stock test | 5.159 to 5.237 | 39.365 to 39.443 | 24.603 to 24.652 | 0.468 to 0.517 |
| daily rate: by year, by promotion, store by store | 5.145 to 5.245 | 39.357 to 39.458 | 24.598 to 24.661 | 0.459 to 0.522 |
| daily rate: probes at 1,390 and 1,400 a day | 5.128 to 5.186 | 39.417 to 39.474 | 24.635 to 24.671 | 0.449 to 0.485 |
| 2027 days: store-days | 5.132 to 5.245 | 39.357 to 39.470 | 24.598 to 24.669 | 0.451 to 0.522 |
| 2027 days: 258 store-weeks | 5.128 to 5.242 | 39.361 to 39.474 | 24.600 to 24.671 | 0.449 to 0.520 |
| trade rate: pooled | 5.135 to 5.245 | 39.357 to 39.468 | 24.598 to 24.667 | 0.453 to 0.522 |
| trade rate: lot by lot | 5.135 to 5.245 | 39.357 to 39.468 | 24.598 to 24.667 | 0.453 to 0.522 |
| trade rate: lots over 150,000 | 5.131 to 5.242 | 39.361 to 39.471 | 24.601 to 24.670 | 0.450 to 0.519 |
| trade rate: 2026 lots | 5.128 to 5.239 | 39.364 to 39.474 | 24.602 to 24.671 | 0.449 to 0.518 |
| graded unit and bin | nearest 1.0: [4.5, 5.5) | nearest 0.5: [39.25, 39.75) | nearest 0.5: [24.25, 24.75) | nearest 0.25: [0.375, 0.625) |
| the 0.1 million bins the family crossed | 5.1 and 5.2 | 39.4 and 39.5 | 24.6 and 24.7 | 0.4 and 0.5 (the 1,400 probe files 0.449) |

3. **The reader's mild tells.** Lot TL144 was dated Christmas Day 2026; a lot dated on a bank holiday now moves to the
   next working day after the draws, so no price moves. The two range clear-out lots are no longer round sums (GBP
   236,412.37 and 318,764.91). The facility balance now moves on most working days in 50,000s, the year-end balance
   unchanged. None moves a graded figure (the trade rate stays 0.102).
4. **The 10/10 rules re-read against the built pack.** The decisive step is still the analytical one: the outlet's
   2027 take from its stocked trading days, checked on 2023. The mess is still Layer 1 only. Both asks still sit on
   rows the call never reads: 2025 rows, credits with no quantity, an ask-only archive.
5. **freeze.py.** The rubric check flags exactly the three figures whose units changed, in figures.json and in
   blocks 1 and 2. With those three keys allowed, only the block 1 and 2 number lists still differ (5.2 to 5, 24.6 to
   24.5, 39.4 to 39.5). Every other frozen item is unchanged: the call, the stump, the shortfall 0.5, the recovery
   0.617, the trade rate 0.102, the daily rate 1,377, the 1,801 days, the rungs and the excess figures. freeze.py was
   not edited; both commands and outputs are in the hand-back.

## Architecture 2 record (spent 2026-11-02)

Kept as history; nothing below binds architecture 3. The sections are demoted one level.

Architecture 2, drawn 2026-11-02 as a re-root (architecture 1, a Medicaid plan's county designation in healthcare delivery, sound on its main call but spent on its ask layer: see `## Architecture 1 record` and `## Tried and rejected`). A new world, dataset, generator and shell in another client domain: the City of Elsworth (Oregon, fictional) Parking Services division's 2027 performance-based meter rates, each metered zone's rate moved by its weekday noon-to-2 p.m. occupancy over the fall 2026 measurement period, which no system records whole.

### Draw

Ten-line summary (sent to the main thread at registration; the lines below are the build as cut):

1. **Pairing:** General Statistics & Data Science, `data-integration-record-linkage-entity-resolution`, objective Data Extraction & Conformation (ETL); client domain general-statistics-data-science (architecture 1 was healthcare delivery).
2. **Niche:** the City of Elsworth (Oregon, fictional) Parking Services division's 2027 performance-based meter rates: each of its meter zones moves its hourly rate by its weekday noon-to-2 p.m. occupancy over the fall 2026 measurement period (8 September to 30 October), counting every parked vehicle, paid or not, which no system records whole.
3. **Default path against golden:** the default adds to the apps' complete paid record the mean count of unpaid vehicles on each zone's enforcement runs (validated on downtown, whose 12:30 run sits inside the window) and raises Alder Row, Cascade Avenue and Hollis Street and holds Fernwood and Irvine Market; the golden adds only the vehicles read unpaid on both the last run before noon and the first after 2 p.m., and holds the three, lowers the two.
4. **Stump sentence:** below.
5. **Shape:** 10, a scorecard against thresholds (each zone's occupancy against 60 and 85 per cent sets its 2027 rate); decision `dial_setting`, question form `what`.
6. **Deliverables:** `elsworth_2027_meter_rates.docx` (the council memo, rate table and a chart of every zone against the two lines) and `fall_2026_curb_occupancy.csv` (the zone figures and the sensor-pilot streets' figures by month).
7. **Nearest driver (`guard.py mechanisms`, `check`):** 0.06 task243 (a register's exit share), 0.05 task250 v3, task274 v1, task130, task265 v0; none moves a window's unrecorded part from members counted on both sides of it.
8. **Guard:** WARN, `overuse.objective` only (the ETL lane); `test.same_driver_older` NOTE, differentiated against task107's v3-etl lineage on the card.
9. **Ask records:** the curb-sensor pilot on four free two-hour streets beside meter zones (its platform's events and heartbeats), a system the call never reads; devices: sensors whose batteries died read as empty spaces, and the magnetometer's four-hourly re-baselining read as departures.
10. **Layer 1:** two app vendors either side of 1 October (StallPay local 12-hour times and zone codes, CurbTrack UTC times and location numbers through a crosswalk), camera misreads of confusable characters, an inventory with a new Eastbank face and a cut Cascade Avenue face, bagged faces, the holiday calendar as an iCalendar file, the sensor platform's UTC export, Saturdays and the days outside the period in every extract.

- **Card:** `.claude/skills/fingerprint/cards/task458.json`, architecture v2, registered 2026-11-02 with `check` run on the registered card (WARN `overuse.objective`, answered: the slot is in the author's ETL lane). Architecture 1's identity is in the card's lineage with `architecture_spent` and its fate, and its shell in `lineage_shells`.
- **Axes redrawn against the window at the draw, each to the honester label:** strategy `composition_mix` (BLOCK against task453) to `population_selection` (the runs count a different unpaid population from the one parked at midday); generators G6 and G13 (BLOCK against task453 and task154) to G12 (the window has no read, and a vehicle with no midday read is not a vehicle absent at midday); forcing event to `launch_or_rollout` (the 2027 schedule rolls out on 1 January); Gate G to `etl_conformance`. Personas Kelsey Solis (Parking Services Manager) and Andrew Ward (enforcement and pilot lead) from `guard.py names --geo "United States" --seed 458`.
- **Why this cell:** ETL is served by six task types; healthcare delivery (architecture 1), physical and environmental sciences, survey research and official statistics were out for this re-root and test equating is spent on file. Data integration remains, and its deciding object here is the integration estimator itself: a complete record of one part of a population joined to periodic counts of all of it.
- **The ETL move (guide-to-prompt section 1):** complete a record the process could not make. The forcing file, the enforcement plate reads, pins an overlap: which unpaid vehicles were read on both sides of the window. Reading every file correctly is not sufficient: the sessions, reads, inventory and rule read right still leave the analyst choosing how the window's unpaid vehicles follow from reads taken outside it.
- **Shape and shell:** shape 10; question form `what`, second sentence opening on the memo, rounding sentence opening on occupancy, deliverable set docx+csv, all under the corpus quotas (`voice-check.py` PASS), none of architecture 1's (which, put, round, csv+xlsx).
- **World:** the City of Elsworth, Department of Transportation, Parking Services. Six downtown zones whose enforcement routes run at about 8:30, 10:30, 12:30, 2:30 and 4:30, and twelve neighbourhood business districts whose routes run once between 8:45 and 10:45 and once between 2:45 and 3:45. Payment is by plate through an app or text, pay as you go, the app ending the session when the car leaves; the vendor changed on 1 October 2026. Parking Administrative Rule 12 (the filed WHAT): the measurement period, the weekday and window, occupancy as the share of in-service metered space-minutes a parked vehicle occupied whether or not it paid, bagged faces out of service, the 85 and 60 per cent lines, the 50-cent step, the floor and ceiling, Schedule A with the 2026 rates. Forum `council_or_assembly`, forcing event `launch_or_rollout`, organisation `local_government`, role `policy_adviser`.
- **Data-native sentence:** the neighbourhood districts' routes run only mid-morning and mid-afternoon, when the vehicles parked without paying include residents' cars left from the night (gone by half past eleven) and parents' school-run stops (from about 2:40), while at midday the only unpaid vehicles are disability placard holders parked all day, a fixed number that neither run's unpaid count describes; downtown, whose routes include a 12:30 run and whose blocks have neither, shows the mean of its runs agreeing with the window.
- **Abstraction sentence (stumping Part 6), and the approved builds it is not:** "a window no count covers is filled from a complete record of one part of a population and counts of all of it taken outside the window, the other part entering only through the members counted on both sides of it." No approved build says it: task275 rebuilds unobserved effort from a catch per hour, task120 subtracts a storage gain, task196 corrects a self-produced overlap, task303 removes simultaneous sibling events; the delivered task473 and architecture 1 complete a count by a capture rate, which this build has none of.
- **Lessons 7, 9, 10 and 11:** no shipped file states an occupancy, a paid-to-total factor, a compliance rate, an unpaid share or an expansion for any zone, and no shipped document reports a figure computed by one (9, 11); the default path is the analyst's own additive model, refuted by the runs' own unpaid mix by time of day; the filed WHAT names occupancy by every parked vehicle over the window and nothing about how unpaid vehicles are known (10; `checks.py` LK2 asserts the rule names no record, system or unpaid group); the golden's assumptions are asserted on the clean truth and through the verifier's readers (7: L7a, L7b, SF6 to SF9).
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, data integration card 1 (propagate integration error into the estimate): this build's own pattern, `own:unrecorded-group-in-a-window-from-its-own-sightings-on-both-sides`.
  - `stumping/references/client/two-layer-task-design.md`, estimation_fit (weighting, ratio estimators): the ratio of all to paid vehicles at the counts is the field's expansion and rung 1 here.
  - `stumping/references/strategies.md` F7 population (the population the decision funds is not the counted one).
  - `dataset-generation/references/layer1-messiness.md`: several sources for one picture, layouts changing at a vendor switch, imperfect keys, real coverage; none on the decisive step.
- **Leak REVIEW rulings:** recorded under `## Leak check` once `leak.py` has run on the final cut.

### Default path

The pipeline a strong analyst builds from the prompt's words and the files' grain, every field read right and Rule 12 executed:

1. Conform the two vendors' sessions: StallPay's 12-hour local times and zone codes; CurbTrack's UTC times converted to Pacific and its location numbers mapped through the crosswalk to block faces and, through the effective-dated inventory, to zones.
2. Take the counted weekdays from Rule 12.03 and the holiday calendar (8 September to 30 October, 12 October out) and each zone's in-service spaces per day from the inventory less the faces bagged that day (Rule 12.04).
3. Paid occupancy minute by minute in the noon-to-2 window from the sessions (pay as you go, so a session is the car's presence).
4. For the vehicles that did not pay, the field's count-based method: take each zone's enforcement runs that day, count the reads with no matching session, and add the mean unpaid count over the day's runs to the window's paid minutes (the ratio of all to paid vehicles at the runs, rung 1, gives districts over 100 per cent and is dropped).
5. Validate on downtown: its 12:30 run sits inside the window, and its unpaid count there equals the mean of its other runs, zone after zone (`checks.py` R3e); the model holds.
6. Apply Rule 12.05 to each zone's occupancy.

- **Ends on:** raise six zones (Courthouse, Union Depot, Eastbank, Alder Row at 95 per cent, Cascade Avenue at 95, Hollis Street at 91, each to its rate plus 50 cents), lower two (Market Hall, Birch Hill), hold ten (Fernwood at 71, Irvine Market at 71 among them).
- **Golden:** raise three (D01 Courthouse to 3.25, D05 Union Depot to 2.50, N05 Eastbank to 2.00), lower four (D04 Market Hall to 2.00, N02 Birch Hill to 1.00, N06 Fernwood to 1.00, N09 Irvine Market to 1.00), hold eleven; Alder Row 79, Cascade Avenue 79, Hollis Street 79, Fernwood 55, Irvine Market 53 per cent.

### Stump sentence

The default path adds each zone's mean unpaid count on its enforcement runs to the complete paid record, a model downtown's in-window 12:30 run confirms, and so raises Alder Row, Cascade Avenue and Hollis Street (95, 95 and 91 per cent) and holds Fernwood and Irvine Market (71 and 71 per cent); but the neighbourhood runs come only mid-morning and mid-afternoon, when the unpaid vehicles include residents' cars left from the night and school-run stops, so only the vehicles read unpaid on both the last run before noon and the first after 2 p.m. were parked through the window, which puts the three at 79 per cent (hold) and the two at 55 and 53 (lower).

### Three rules

- **Task type:** `data-integration-record-linkage-entity-resolution` (General Statistics & Data Science), which serves Data Extraction & Conformation: two vendors' session records and the routes' plate reads are integrated into one conformed table of zone occupancy, and the integration estimator is what decides.
- **Domain test:** the deciding quantity is each zone's window occupancy estimated from a complete record of paid presence plus periodic counts of every vehicle; the field's own estimator is the count-based expansion (the paid record raised by the counts' all-to-paid ratio, or the counts' unpaid stock added), as parking occupancy studies do with survey counts.
- **Swap:** "the share of a ward's beds occupied at noon from the admissions system plus the night porters' bed counts" keeps the arithmetic but loses the call: the call turns on which unpaid parkers stay through a lunchtime window that no route covers, a structure of placard holders, overnight cars and school-run stops the swap does not carry.
- **Layer 1:** the vendor switch on 1 October (StallPay's local 12-hour times and zone codes, CurbTrack's UTC times and location numbers through a crosswalk), confusable characters in camera reads, the effective-dated inventory (a new Eastbank face from 5 October, Cascade Avenue's face 2 cut to three spaces from 21 September), bagged faces under street-use permits, the iCalendar holidays, Saturdays and days outside the period in every extract; each produced by its own system and none carrying the call.
- **Layer 2:** population selection in a stock estimate: the unpaid stock at a count is not the window's unpaid stock when the unpaid population turns over by time of day; the choice that flips the call is to identify the window's unpaid vehicles by their presence across it rather than to transfer a count taken outside it.
- **Decisive step:** reading the unpaid plates on the runs either side of the window as a panel of vehicles, and counting in the window only those parked through it (unpaid on both the last run before noon and the first after 2 p.m.), because the mid-morning unpaid set holds overnight cars and the mid-afternoon set school-run stops that are gone at midday.
- **Not semantics:** every field read by its plain meaning (the payment check, both vendors' clocks, the zone keys, the inventory's dates, the rule's definitions) still leaves the analyst choosing how a count outside the window becomes the window's unpaid stock; the default path reads all of them right and files the wrong schedule (R3a).
- **Not rule application:** Rule 12 files what occupancy is and the lines, never how unpaid vehicles at midday are found; the enumerated family (paid only, the all-to-paid ratio, the mean unpaid count, the morning run, the afternoon run, the smaller of the two counts, the runs' mean, a flat uplift from downtown's in-window share, interpolation of totals) spans Alder Row 45 to 180 per cent and none lands the call (R3b, 0 of 9); the standing family (the plates read unpaid on both runs, by exact or near match, with or without each plate's own session minutes, downtown read at 12:30 or bracketed) spreads 0.0 whole per cents on every zone (SF6 to SF9), and the ruling-out is the runs' own unpaid mix, plate by plate, which nothing announces.
- **Analyst test:** a strong analyst who cleans every file and executes Rule 12 adds the mean unpaid count on each zone's runs to the paid record, sees it confirmed by downtown's 12:30 run, and files Alder Row, Cascade Avenue and Hollis Street raised (95, 95 and 91 per cent) with Fernwood and Irvine Market held (71 and 71 per cent).
- **Estimand:** Rule 12.03 and 12.04 in `Parking_Administrative_Rule_12.pdf`: the in-service metered space-minutes from noon to 2 p.m. on every weekday of 8 September to 30 October 2026 (holidays out), occupied by a parked vehicle whether or not it paid, over all in-service space-minutes in those windows, bagged faces out on their permit days, by zone.
- **No decoy:** nothing is planted: no memo, study, factor, compliance rate, occupancy table or stakeholder figure is shipped; the overnight cars, school-run stops and placard holders are the parking world's own, and the distractors (the garages' monthly summary, the 311 requests) rank no zone.
- **No certified replay:** no certified or published occupancy exists in the pack, so no method is recovered by reproducing one; downtown's 12:30 run is a raw count the default path validates against, not a certified figure.
- **Lesson:** a count of a population taken outside a window describes the population at that time; when the population turns over by time of day, the window's members are the ones present on both sides of it, found plate by plate, and no build on file teaches transferring a stock across a window by its members' presence on both sides.

### Survivor anatomy

- **Actor:** the unpaid vehicle parked through the window has rows (its reads on each run) but no column says it stayed: the property is a relation between a plate's reads on two runs, stored nowhere.
- **Link:** the signal is the same unpaid plate on the morning and the afternoon run of one zone-day, a within-file comparison across runs that no key offers (the read rows carry no vehicle or stay identifier) and no sentence invites.
- **Reflex:** the field's count-based expansion sits at rung 1 (the all-to-paid ratio, over 100 per cent in districts) and the additive count model at rung 2, the default path, which files the wrong schedule (`## Default path`).
- **Back-test:** downtown's 12:30 run inside the window confirms the default path: the mean unpaid count of downtown's other runs matches it in every downtown zone (R3e), because downtown has no overnight cars or school-run stops.
- **Second use:** every file the decisive step reads is in the pack for the paid record or the in-service spaces anyway: the reads give the unpaid count the default path also uses; nothing is shipped only for the step.
- **Shock:** the golden's raise and lower sets are not an interval of any sort on a shipped statistic: by paid occupancy the bottom four hold Linden Square, not Fernwood, and the top three hold Kittredge, not Eastbank (R3d); the five districts the step moves are ordinary lunch and flat-profile zones.
- **Pins:** the WHAT is filed in Rule 12 (the city's administrative rule, its genre) and no filed sentence names a run, a read, a session, an unpaid group or how midday unpaid vehicles are known (LK2); deleting any sentence of 12.03 to 12.05 unforces only what it files.

### Readability screen

| Rung | What reads it | Verdict |
|---|---|---|
| 0 paid only (sessions alone) | Rule 12.04 "whether or not that vehicle paid" rules it out on reading | readable |
| 1 the all-to-paid ratio at the runs | districts at 110 to 180 per cent, impossible on reading the result | readable |
| 2 the mean unpaid count at the runs (default path) | nothing: downtown's 12:30 run confirms it | silent |
| 3 (decisive) the plates read unpaid on both runs either side of the window | nothing in any file or sentence names it; only the runs' plates, compared across runs, show the turnover | silent |

### Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the window's clock | noon to 2 p.m. Pacific; CurbTrack's times are UTC (each carries Z) | CurbTrack read as local | every zone moves | the Z on every CurbTrack time; positive control in checks.py (18 zones move) |
| SF2 | above 85, below 60 | the unrounded share | the whole-per-cent figure | same call | no zone within 4.2 points of a line (R3f) |
| SF3 | weekday | Monday to Friday in the period, not a City holiday | 12 October kept | same call | Rule 12.03's definition and the holiday calendar |
| SF4 | a day without a run on one side | none occurs | fill or skip | same call | every counted zone-day has both runs (asserted) |
| SF5 | in-service space | inventory face on the day, less faces bagged that day | nominal spaces | figures move | Rule 12.04's sentence and the permits' bag dates |
| SF6 | a read's paid status | a session for that plate (or one confusable character off) active at the read | the system's payment check | same figure, every zone | asserted through the verifier's reader |
| SF7 | the same vehicle on two runs | the plate, or one confusable character off | exact plate only | same figure, every zone | asserted |
| SF8 | a both-run unpaid vehicle's window minutes | the window less its own session minutes | the whole window | same figure, every zone | asserted |
| SF9 | downtown's window | bracketed by its 10:30 and 2:30 runs | its 12:30 run read directly | same figure, every zone | asserted |
| SF10 | occupancy | every parked vehicle, paid or not | paid vehicles only | seven zones move | Rule 12.04 "whether or not that vehicle paid" |
| SF11 | the pilot's months | the measurement period's weekdays in September and in October | whole calendar months | figures move | the prompt's "each month of the measurement period" and Rule 12.03 |
| SF12 | a pilot stay's day | the local date the stay began | the UTC date | figures move | the Z on every pilot time; positive control asserted |

### Ladder

| Rung | Construction | Alder Row | Fernwood | Call |
|---|---|---|---|---|
| 0 | paid sessions only | 67 | 47 | lowers eight, raises none |
| 1 | paid record times the all-to-paid ratio at the runs | 180 | 74 | raises N01, N03, N07, N08 and holds N06, N09 |
| 2 (default) | paid record plus the mean unpaid count at the runs | 95 | 71 | raises N01, N03, N08; holds N06, N09 |
| 2b | plus the afternoon run's, the morning run's, the smaller run's or the two runs' mean unpaid count | 90 to 96 | 66 to 73 | the same five flips |
| 3 (golden) | paid record plus the vehicles read unpaid on both runs either side | 79 | 55 | raise D01, D05, N05; lower D04, N02, N06, N09 |

Gate F on the clean truth (R3b): 0 of 9 cheap routes land the call; every count-based route flips exactly the five districts with both overnight and school-run cars (R3c).

### Closure table

| Axis | Reading here | Closure |
|---|---|---|
| 1 Population | every vehicle parked on an in-service metered space in the window, paid or not | filed (Rule 12.04); SF10 |
| 2 Unit of account | space-minutes, summed by zone | filed (12.04) |
| 3 Attribution window | noon to 2 p.m. on the period's weekdays | filed (12.03); SF1, SF3 |
| 4 As-of dating | the inventory on each day, the permits' bag dates | the files' own effective dates; SF5 |
| 5 Version basis | the rule as amended 9 December 2025, the inventory as of 6 October | one version each |
| 6 Denominator | in-service space-minutes | filed (12.04) |
| 7 Weighting | pooled space-minutes over the period's days, by zone | filed ("over the measurement windows of all weekdays") |
| 8 Window length | one measurement period | filed (12.03) |
| 9 Boundary inclusivity | above 85, below 60 | C1: no zone within 4.2 points (SF2) |
| 10 Rounding path | the unrounded share decides; reported in whole per cents | C1 (SF2) |
| 11 Tie-break | none needed | C1 |
| 12 Maturity and censoring | every window closed before the extracts | C1: extracts run to 31 October |
| 13 Order of operations | conform, then occupancy, then the rate step | filed (12.05) |
| 14 Row order | none matters | C1 |
| 15 Duplicate resolution | one session per paid stay; reads per run | C1: no duplicate rows shipped |
| 16 Identity normalisation | CurbTrack locations to faces to zones; plates across runs | the crosswalk and inventory; SF7 |
| 17 Netting against gross | none | not applicable |
| 18 Dimensional units | minutes, spaces, dollars | the files' own columns |
| 19 Code and status semantics | the payment check, StallPay zone codes | SF6; the inventory's zone column |
| 20 Integerisation | whole per cents, cents | filed in the prompt |
| 21 Clause scope | 12.05's floor and ceiling | filed; no zone reaches either |
| 22 Forward window contents | the 2027 rates need no forecast | filed: the rate moves by the 2026 measurement |

### Literal reader

Executed word for word on the cut pack: Rule 12.03 and 12.04 fix the period, the weekdays, the window, the in-service spaces and occupancy by every parked vehicle; the prompt fixes the units and rounding. Silent on how unpaid vehicles are known, and every licensed way of using the plate reads either lands the golden (the standing family, SF6 to SF9, 0.0 whole per cents apart) or is ruled out by the runs' own rows (the turnover of unpaid plates between runs, L7a). The pilot figures follow the prompt's period and weekday words and Rule 12.03; the device readings (silence as vacancy, a four-second blip as a departure) are each contradicted by the feed's own rows (a sensor that stopped heartbeating, a vacancy no car could make), so no literal reading of a field gives them (PA1, PB1, PB2).

### Oracles

None shipped. No document states an occupancy, a factor, a share or a compliance rate; downtown's 12:30 run is a raw count the default path also passes; the golden memo and CSV never ship.

### Ask sheet

Two device families on disjoint figure blocks of the pilot ask, on a system the call never reads (the free streets carry no meter, no session and no route; PS3), so with every pilot file deleted the main files yield no ask figure.

**Ask A, the pilot streets' weekday noon-to-2 occupancy by month (8 figures). Device: a sensor's silence read as an empty space (D4/D9, a state no event records, read from its trace).** Two sensors on each street ran down their batteries in September (at night, while their spaces were empty) and sent nothing after: no events and no heartbeats, their battery readings falling to about 2,600 mV before the last one. Read as recorded, each silent space is empty every weekday for the rest of the period and the street's occupancy falls 2 to 7 points. The rows force one reading: a working sensor heartbeats every hour whatever its space holds, so after the last heartbeat the space is unmeasured, and the occupancy is that of the spaces measured (excluding the space from both sides equals imputing the street's mean). Over-cleaning half: the gateway outages, when a street's heartbeats stop for hours but its occupancy events arrive afterwards with their own times; treating those hours as unmeasured moves figures (PO). Lesson 8: no filed rule or field's plain meaning makes a silent sensor an empty space, since the feed's own heartbeat rows say the sensor stopped; the space's last event is a departure, and the battery trace shows the cause.

| Reading | Ostrander Oct | Wexford Oct | Where the rows put it |
|---|---|---|---|
| silence is an empty space (cracker) | 71 | 46 | contradicted by the heartbeats stopping |
| unmeasured from the last heartbeat (golden) | 77 | 52 | the only reading the rows allow |
| outage hours unmeasured too (over-cleaner) | 78 | 53 | contradicted by the late-delivered events |

**Ask B, the pilot streets' average weekday stay by month (8 figures). Device: the magnetometer's re-baselining read as departures (D1/D6, one stay recorded as several).** Under a long-parked car each sensor re-baselines every four hours from the car's arrival, sending VACANT then OCCUPIED two to five seconds apart. Read as recorded, every overnight resident's car becomes three or four stays and the average stay falls from about 140 to 190 minutes to about 115 to 125. The rows force one reading: no car leaves and another takes the space in five seconds (every real swap in the feed takes twelve seconds or more), and the blips fall at four-hour multiples of the stay's start; any merge threshold from 6 to 11 seconds gives the golden (PB2). Over-cleaning half: merging every gap under a minute joins real quick swaps on busy streets (PO). Lesson 8: no field or rule says a VACANT event is not a departure; the impossibility of the gap and the four-hour rhythm make the literal reading impossible, not merely unlikely. Separation: the blips move no occupancy figure (PS1) and the dead sensors no stay (PS2).

| Reading | Tamarack Oct | Ostrander Oct | Where the rows put it |
|---|---|---|---|
| every VACANT is a departure (cracker) | 117 | 113 | contradicted by the 2 to 5 second gaps at four-hour multiples |
| blips under 6 to 11 seconds merged (golden) | 151 | 139 | the only reading the rows allow |
| gaps under a minute merged (over-cleaner) | 154 | 143 | contradicted by the real swaps of 12 to 60 seconds |

**Cracker sheet** (`generator/ceiling.py` on the cut pack: UTC converted, holidays out, exact duplicates and orphan sensors checked, the OCCUPIED/VACANT alternation checked, spells merged across touching gaps, event time used over received time, heartbeat rows read as status rows):

| Ask figure block | Cracker route | Result |
|---|---|---|
| A, occupancy, 4 streets by 2 months | events as recorded, silent spaces empty | miss |
| B, average stay, 4 streets by 2 months | spells from every OCCUPIED/VACANT transition | miss |

- **Pair ceiling:** 28.5 (cracker on the call 45.0 with 0 of 16 ask figures, mirror off the call 12.0); two careful responses on the call each handling one device, 72.5; the full includer reproduces all 16.
- **Mirror leakage:** 0.0 per cent of ask weight.
- **Measured by:** `generator/ceiling.py` on the cut pack (target/), figures.json as the key.

### Leak check

`leak.py task458 --asof 2026-11-06 --quiet` on the final cut: REVIEW, no LEAK. Each REVIEW ruled:

- Sweep 3, rates in `Parking_Administrative_Rule_12.pdf` (1.00 to 2.75): Schedule A's 2026 rates and 12.05's floor, inputs the memo owes as its 2026 column; no 2027 rate or occupancy appears, and which zones move is not derivable from the rule.
- Sweep 3, 24 of 30 words of the call in the rule: the zone names, "hourly rate", "50 cents" and "1 January" are the rule's own step and schedule; it names no zone that moves.
- Sweep 4, window, downtown and vehicle in the rule: 12.03's window, Schedule A's area column and 12.04's "parked vehicle"; it names no run, read, session or unpaid group (`checks.py` LK2).
- Sweep 6, zones or streets beside numbers in the rule, the inventory, the crosswalk, the sensor list and the 311 requests: 2026 rates and time limits, metered spaces by face, location numbers, sensor space numbers and request ids; none carries an occupancy or ranks a zone on the decision question.
- Heart WARN `repeat.deliverables` (csv+docx against task454 v2, drawn and built 2026-11-02, the same day as this build): a window artifact of two builds in flight; the shells differ (question form `what` and memo opener here). `overuse.objective` answered at the draw.

## Architecture 1 record (spent 2026-11-02)

Kept as history; nothing below binds the current architecture. The sections are demoted one level.

Architecture 1, drawn 2026-10-15 from seed ET15 (behavioral-health workforce designation from NPPES monthly snapshots and weekly deltas). The seed's world, decision and quantity are kept: a Medicaid program designates counties for a behavioral-health prescriber pilot on workforce ratios, with the provider master rebuilt from the NPPES monthly file and its weekly incrementals. Its decoy-era traps (retired clinicians and mail-only addresses in the count) are Layer 1 here, and the pitfall is found in how the ratios' need populations are counted. Pass 2 (stage 4, 15 October): the first design's decisive step (the full-year prevalence standardized by eligibility group) was filed by the isolated leak reader, so the stump was re-centred on the seasonal members' own records; the first design's golden is now the default path.

### Draw

- **Card:** `.claude/skills/fingerprint/cards/task458.json`, architecture v1 (guard WARN only: overuse.objective, answered below; task231 and task445 lineage differentiated on the card for the older same-puzzle signature).
- **Pairing:** Healthcare Delivery & Health Economics / payment-claims-health-plan-analytics / Data Extraction & Conformation (ETL). Sandhollow Health Plan, a nonprofit Medicaid managed care plan serving adults in ten eastern Washington counties, funds a Prescriber Service Award Pilot in 2027: loan repayment for behavioral-health prescribers who commit three years to a designated county. Network Policy NP-31 sets the designation. A county qualifies when it fails at least two of three standards measured over the contract year July 2025 to June 2026: practising behavioral-health prescribers per 1,000 adult members with a serious mental illness, practising prescribers per 1,000 adult members with an opioid use disorder, and the share of adult members with a serious mental illness who saw a behavioral-health prescriber. The plan's network analytics team conforms the NPPES files, the claims and encounter extract and the eligibility spells into one county table. In payment and claims analytics this is case identification against enrollment: a chronic condition is known only through the services billed while a member is enrolled, so its prevalence is measured on members observed long enough for it to show and carried to every member.
- **Why not another task type:** the ETL-serving task types in the census-register and record-linkage families are banned against the last three builds (task457, task456), and the claims are where the deciding quantity lives. Emissions inventories, seasonal adjustment and test equating do not hold this world.
- **Shape:** 10 (scorecard against thresholds: three standards for each of ten counties, each a verdict, the county's designation from the two-of-three test). Arithmetic: the designated set as the call (1), ten counties' practising prescribers (10), twenty need counts to the nearest 10 (20), thirty standard-by-county verdicts (30), the two files (2), then forty quarterly payments and forty group rows of the asks: about 63 criteria before the asks' rows.
- **Strategy:** maturity_censoring (G14 decisive, G12 and G6 behind it). A member's serious mental illness or opioid use disorder appears in the claims only through services billed while they were enrolled, so the claims identify about 1 per cent of expansion adults enrolled one month against 6 per cent of those enrolled all year. NP-31 counts every member who has the condition, identified or not, and leaves the estimate to the analyst. The members enrolled all year are fully observed, but they are not a sample of the membership: disabled adults stay enrolled, and the farmworkers who enrol for a harvest have the conditions about half as often as the members of their group who stay. So the full-year members' prevalence, carried to every member whole or within each eligibility group, overstates the seasonal counties. The estimate that holds counts each identified member over the share of full-year members with the condition that a window of the member's own length identifies (the lookback-window sensitivity), measured on the full-year members' first identifying months.
- **World:** Washington State, ten counties east of the Cascades (Adams, Benton, Chelan, Douglas, Franklin, Grant, Kittitas, Okanogan, Walla Walla, Yakima). Sandhollow Health Plan (fictional), about 120,000 adults enrolled at some point in the contract year, about 150 practising behavioral-health prescribers. The pack carries the NPPES October 2026 monthly file for the plan's state and its three later weekly incremental files and deactivation file, the plan's behavioral-health claims and encounter extract for the contract year (the spine), the eligibility spell file, the policy, the taxonomy and county reference files and distractors. Forcing fact: the board approves the pilot's county list with the 2027 budget at its 19 November 2026 meeting.
- **Forum and forcing event:** board_of_directors (the plan's board approves the pilot's county list), budget_or_appropriation (the 2027 budget carries the pilot). Organisation nonprofit_or_charity (a nonprofit Medicaid plan; the vocabulary has no payer key), role capacity_planner (the plan's director of network development). Personas from `guard.py names --geo "United States" --seed 458`: Cameron Joyce, William Guerrero, Charles Schmidt.
- **Data-native sentence:** the farm counties' expansion adults and parents enrol for one to four months at a harvest, and those farmworkers have a serious mental illness or an opioid use disorder about half as often as the members who stay enrolled; a member's lasting condition reaches the claims only when a service is billed during a spell, so the recorded members fall short of those with the condition where spells are short, while the full-year members who could stand in for them are the ones the seasons never touch.
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, payment-claims-health-plan-analytics pattern 4 (risk-adjusted PMPM is a ratio of totals over member months; members enrol and leave mid-year): the library's pattern weights exposure correctly; this build's pitfall is that the condition itself is recorded through exposure, the count of members with it depends on how long each was observed, and the fully observed members are selected on the condition (`own:condition-count-from-claims-by-lookback-window-sensitivity`).
  - `stumping/references/client/two-layer-task-design.md`, estimation_fit (censoring and truncation): a member's spell truncates the window in which their condition can appear in the claims.
  - `stumping/references/strategies.md` F4 maturity_censoring (open periods are not fully developed and arrival speed differs by unit; the pooled reflex lands in the same place): here the undeveloped unit is a member's short spell, and the reflexes (count recorded members, keep only the continuously enrolled, pool the recorded rate) each land on a named wrong designation.
  - `dataset-generation/references/layer1-messiness.md` (several sources for one picture, vintages and revisions, imperfect keys, documentation to read, genuine overlap, real coverage): the Layer 1 here, none of it on the decisive step.
- **Same-puzzle and abstraction:** gap population, generator G14 behind G12, Gate G etl_conformance, decision designation_set. The guard's older same-puzzle signature (task231, task445 v1 loop 0 in lineage) is differentiated on the card, and so is task448 (a second list's capture by recording route) and this slot's first design (standardizing the full-year members, now the default path). Nearest drivers on file after the re-centre: task73 (0.08), task180 (0.07), task254 (0.06); none counts a lasting trait through each unit's observation window against a reference population selected on the trait.
- **Guard WARN overuse.objective:** the slot is in the author's ETL lane (task445 to task493).

### Default path

1. Build the prescriber master: the October 2026 NPPES file updated record by record by the weekly incremental files through 1 November, behavioral-health primary taxonomies, the practice location's county from the HUD crosswalk's business share, the NPI active on 1 November, and at least one service in the contract year in the claims.
2. Build the adult members: enrollment spans joined into persons by client identifier, each in the county and eligibility group of the span covering the last enrolled day, with the months enrolled.
3. Count each county's adult members with a serious mental illness and with an opioid use disorder as NP-31 2.5 asks, every member who has the condition whether or not a claim identifies it: within each eligibility group (the conformed file's grain, and the full-year members are disproportionately disabled adults), the prevalence among the county's members enrolled all twelve months (fully observed, every claim had time to arrive) times the group's members, summed over the groups.
4. Compute each county's three standards (prescribers per 1,000 members with each condition, the share of members with a serious mental illness seen by a behavioral-health prescriber), compare with NP-31's thresholds and designate the counties failing two or more.

Ends on: Adams, Douglas, Franklin, Grant, Okanogan and Yakima
Golden: Adams, Douglas, Franklin, Grant and Okanogan

### Stump sentence

The default path files six counties, Adams, Douglas, Franklin, Grant, Okanogan and Yakima, because step 3 carries the prevalence the members enrolled all year show, group by group, to members who were enrolled for a season: the farmworkers in Yakima's short spells have the conditions about half as often as the members who stay, so the full-year prevalence puts 2,660 members with a serious mental illness in Yakima where the months-observed count finds 2,320 (15.4 prescribers per 1,000 and a 64 per cent reach instead of 17.7 and 73), and Yakima fails all three standards it meets once each identified member is counted over the share of full-year members a window of its own length identifies.

### Three rules

- Task type: Healthcare Delivery & Health Economics, payment-claims-health-plan-analytics (claims-based case identification against enrollment: the members with a condition estimated from the members a claim identifies, each corrected for how much of the year its enrollment let the claims see, for need-based ratios over a contract year), which serves Data Extraction & Conformation.
- Domain test: the quantity that decides is each county's number of adult members with a serious mental illness and with an opioid use disorder, estimated the way claims-based epidemiology corrects case identification for the length of observation: the sensitivity of a k-month lookback window measured on the members observed all year and applied to each identified member's own window, because continuously enrolled Medicaid members are not a sample of the members who churn; the identified count, the full-year prevalence carried to every member (whole or by eligibility group), an exposure scaling and a capture curve fitted across members of different enrollment lengths each file another county set.
- Swap: with retail nouns (shoppers whose standing preference shows only in purchases during a loyalty spell, seasonal shoppers against year-round members) the window's sensitivity and the seasonal members' lower rate have no institutional source and no standard counts people whose trait no purchase shows; the task needs a lasting condition recorded only through billed services while enrolled, in a program whose continuously enrolled members are sicker than the farmworkers who enrol for a harvest, which is the claims task type's own continuous-enrollment problem.
- Layer 1: the NPPES monthly file superseded record by record by weekly incrementals (a move, a primary taxonomy switch, a reactivation, a deactivation before and one after 1 November, a week after the as-of date), practice against mailing addresses (post office boxes, homes in a neighbouring county), prescriber taxonomies held only as secondary ones, organisations under group and specialty taxonomies, listings with no service, ZIP codes split across counties by business and residential shares, the deactivation report's later dates; the claims' frequency codes (replacements, chains of two, voided duplicates), encounters with no rendering clinician, diagnosis codes in four positions, F11.90 beside the listed opioid codes, lines allowed at the lesser of the charge and the fee schedule; the spans' retroactive rows overlapping a first month, member numbers reissued after a 90-day gap and tied by client identifier, county moves; each produced by the system named and none placed to be caught.
- Layer 2: estimation_fit with the field's case-identification method: the identified members are a capture of those with the condition whose sensitivity depends on the months observed, so the sensitivity is measured on the fully observed members' time to first identification and applied to each identified member's window; the fully observed members cannot stand in for the briefly observed, because who stays enrolled is selected on health.
- Decisive step: counting each identified member as 1 over the share of full-year members with the condition identified within the same number of months, rather than carrying the full-year members' prevalence, whole or within each eligibility group, to the members enrolled for a season.
- Not semantics: every diagnosis code, frequency code, span, eligibility group and NP-31 sentence read correctly still leaves the analyst choosing how to estimate the members no claim identifies; the full-year prevalence within eligibility group is the well-read, standardized estimate, and nothing in a field or a definition says the seasonal members differ: it shows only when their identification is compared with the full-year members' over the same window.
- Not rule application: NP-31 files the conditions, the population (every member who has the condition, identified or not), the window, the county, the ratios and the two-of-three test, and says Network Analytics estimates the members with each condition from each county's own members, never how; executing every filed rule with the full-year prevalence files the six.
- Analyst test: a strong analyst who conforms NPPES, the claims and the spans, reads every field and NP-31 correctly and completes each county's count, as 2.5 requires, with the prevalence its members enrolled all year show within each eligibility group (the stage-4 leak reader's route on the first design) files Adams, Douglas, Franklin, Grant, Okanogan and Yakima (the default path's `Ends on:`); carrying the county's full-year prevalence whole files the same six; counting the identified members files Adams, Douglas and Okanogan.
- Estimand: Network Policy NP-31 (`np31_prescriber_service_area_designation.pdf`), sections 2 and 3: for each county, its practising behavioral-health prescribers per 1,000 of its adult members with a serious mental illness and per 1,000 with an opioid use disorder, every adult member enrolled on a day of the contract year who has the condition counting whether or not a claim or encounter identifies it, and the share of the members with a serious mental illness who had a visit with a behavioral-health prescriber; designated when two of the three fall below 16.5, 23.0 and 68 per cent.
- No decoy: nothing is planted: no memo, prior designation, briefing or stakeholder figure ranks the counties or argues a count; the short spells are the farm counties' seasonal enrollment, the farmworkers' lower rate of serious mental illness and opioid use disorder is who enrols for a harvest, every diagnosis is the claims a member's services produced, and the network adequacy report and the population estimates carry no condition counts.
- No certified replay: no certified or published figure is reproduced to recover a method; NP-31 states what to count and leaves the estimate to the analyst.
- Lesson: a model learns that members observed all year are not a sample of a churning membership, so a condition's count is completed from each member's own record corrected for the window it was observed, the window's sensitivity measured on the fully observed, never by carrying the fully observed members' prevalence, even standardized; no build on file corrects a capture for observation length against a reference population selected on the trait.

### Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 identified members counted | NP-31 2.5's "whether or not a claim identifies it" names the population and sends the solver looking | no column; the count is a group-by | counting identified members is the claims analyst's first reflex | none | none | one count | readable |
| R1 members enrolled all year counted | 2.5's "enrolled on a day of the contract year" rules out the full-year count | months enrolled are derivable from spans | the continuous-enrollment reflex | none | none | one filter | readable |
| R2 each county's full-year prevalence carried whole | none: 2.5 says only that the count is estimated | the full-year flag is derivable | the natural completion once 2.5 is read | none | none | one ratio per county | readable |
| R3 full-year prevalence within each eligibility group carried to the group | none | the eligibility group is a column and the conformed file's grain | standardizing on a visible attribute is the strong analyst's reflex (the first design's leak reader took it) | none | none | a weighted sum over four groups | readable |
| R4 (decisive) each identified member over the full-year members' sensitivity at its own window | none: nothing says the seasonal members differ or names a window's sensitivity | no column marks a seasonal member, a first identifying month or a window; each is built from the spans and the claims | not a reflex: standardizing, reweighting on visible attributes, exposure scaling and a capture curve fitted across enrollment lengths each land six or seven | none: no control ties only under the window weighting | none: the battery finds nothing wrong with the full-year prevalence | a per-member weight from a curve measured on another population | silent |

### Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | adult member | a person (client identifier) | a member number | same call | NP-31 2.2 "a person counts once however many member numbers"; same call (asserted) |
| SF2 | a member's county | the span covering the last enrolled day | the first span's county | same call | NP-31 2.3; same call (asserted) |
| SF3 | a member's county | last enrolled day | the county of most days | same call | NP-31 2.3; same call (asserted) |
| SF4 | identified by a claim | a listed code in any of four positions | the first position only | same call | NP-31 2.4 "in any diagnosis position"; same call (asserted) |
| SF5 | claim versions | final versions | every version | same call | NP-31 2.4; same members and visits under both (asserted) |
| SF6 | NPPES on 1 November | October file updated by the weekly files through 1 November | the October file alone | same call | NP-31 2.6; same call (asserted) |
| SF7 | NPPES on 1 November | weekly files through 1 November | the 2 to 8 November week too | same call | NP-31 2.6 "through that day"; same call (asserted) |
| SF8 | practice location county | larger share of business addresses | residential share | same call | NP-31 2.7; same call (asserted) |
| SF9 | practice location county | business share | all addresses | same call | NP-31 2.7; same call (asserted) |
| SF10 | behavioral-health prescriber | prescriber taxonomy as the primary | any listed taxonomy | same call | NP-31 2.6 "primary taxonomy"; same call (asserted) |
| SF11 | practice location | NPPES business practice location | mailing address | same call | NP-31 2.7 "not the mailing address"; same call (asserted) |
| SF12 | a deactivated NPI's taxonomy | its last record before deactivation | none (no taxonomy) | same call | NP-31 2.6; same call (asserted) |
| SF13 | active on 1 November | the files through 1 November | the November deactivation report applied whatever its date | same call | NP-31 2.7 "active on 1 November 2026"; same call (asserted) |
| SF14 | practising | rendering provider of a contract-year service | listed in NPPES only | no county designated | NP-31 2.7 "rendering provider of at least one claim or encounter" |
| SF15 | visit with a prescriber | wherever the prescriber practises, telehealth included | in-county prescribers only | asserted count of members it drops | NP-31 2.8 "in person or by telehealth, wherever the prescriber practises" |
| SF16 | below the threshold | unrounded values | values rounded to one decimal | same call | NP-31 3.2; same call (asserted) |
| SF17 | members with the condition | every member who has it, identified or not | members a claim identifies | Adams, Douglas and Okanogan | NP-31 2.5 "counts whether or not a claim or encounter in the contract year identifies it" |
| SF18 | measured from its own members | each county's identified members, each weighted by the full-year members' window sensitivity | the sensitivity from each county's own full-year members | same call, same counts to the nearest 10 | NP-31 2.5 "measures each county from its own members"; same call (asserted) |
| SF19 | a full-year member no claim identifies | counted as not having the condition (the window shares end at 1 in the twelfth month) | a constant hazard carried past twelve months, each identified member over 1 - (1 - q)^m | same call; moves several counts by about 1 per cent | NP-31 2.5 "a member enrolled in all twelve months of the contract year whom no claim or encounter identifies is counted as not having the condition"; asserted |

### Ladder

| Rung | Reading | Files | Dies to |
|---|---|---|---|
| 0 | identified members counted | Adams, Douglas, Okanogan (Franklin 15.9 / 24.5 / 83 per cent, Grant 14.3 / 23.6 / 85) | NP-31 2.5's whether-or-not sentence |
| 1 | members enrolled all year counted | Douglas, Okanogan | 2.5's population (every member enrolled on a day) |
| 2 | each county's full-year prevalence carried whole to all its members | the five and Yakima (Yakima 12.7 / 22.0 / 53 per cent) | the full-year members are disproportionately disabled adults, whose serious mental illness rate is three times the expansion adults' |
| 3 | the full-year prevalence within each eligibility group carried to the group's members (default path; the first design's golden) | the five and Yakima (Yakima 15.4 / 21.6 / 64 per cent) | expansion adults enrolled three months are identified at 2.1 per cent against 4.1 per cent of the full-year expansion adults within their first three months, while those enrolled seven to eleven months are identified as the full-year members are over the same months: the seasonal members have the conditions about half as often |
| 4 | each identified member counted as 1 over the share of full-year members with the condition identified within the same number of months (golden) | Adams, Douglas, Franklin, Grant, Okanogan | stands |

- Other reflexes, each landing a named wrong set: the plan's full-year prevalence carried whole or by group (six); identified members per member-month scaled to twelve months (six); a capture curve fitted across members of different enrollment lengths, each identified member weighted by it (seven, Walla Walla added); the plan's pooled under-count factor (seven). The plan-wide identified share by group applied to each county's group counts happens to file the five; it is not a correction of anything (it ignores the county's identified members and their months observed) and NP-31 2.5's "measures each county from its own members" rules it out.
- Winners and margins: the golden's thirty verdicts sit at least 7.2 per cent from their thresholds (closest: Yakima's 17.7 against 16.5); the window sensitivity taken by eligibility group, by county and group, or over days instead of months gives the same thirty verdicts (closest 7.1 per cent) and the same need counts to the nearest 10. Under rung 3 Yakima misses all three standards by 6 to 7 per cent.
- Position and dominance: rung 0 drops two of the five; rungs 2 and 3 keep the five and add Yakima; no standardization, reweighting or curve fit reaches the golden: every correction of rung 0 that leans on the full-year members overshoots, and only the window weighting of each member's own record reverses it.
- Grid: a Layer 1 slip (member numbers, the October file alone, the service requirement dropped, any taxonomy, residential ZIP shares, the first span's county, the mailing address) combined with rungs 0 to 3, the exposure scaling or the pooled factor never files the five (asserted).
- Worth: rung 3 moves the call, Yakima's three verdicts and all twenty need counts with the ratios they feed; rung 0 moves the call and every need count.

### Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | adults enrolled on a day of the contract year, each with the condition counted whether or not a claim identifies it | NP-31 2.2 and 2.5, the unobserved members stated; C1 for the persons (SF1) |
| 2 | Unit of account | a person, by client identifier | NP-31 2.2; same call by member number (SF1) |
| 3 | Attribution window | services and enrollment in the contract year, 1 July 2025 to 30 June 2026 | NP-31 2.1 and the extract's service dates; nothing outside it in the extract |
| 4 | As-of dating | NPPES on 1 November 2026; claims paid through 31 October 2026 | NP-31 2.6, 2.7 and 5.1; SF6, SF7, SF13 converge |
| 5 | Version basis | final claim versions | NP-31 2.4; C1 (SF5) |
| 6 | Denominator | the county's estimated members with each condition | NP-31 3.1; the decisive construction |
| 7 | Weighting | each identified member weighted by 1 over the full-year members' sensitivity at its months enrolled | the decisive construction; the data separates it from every full-year prevalence (rung 3 files six, rung 4 five), and its variants (by group, by county and group, over days) give the same counts to the nearest 10 and the same verdicts (asserted) |
| 8 | Window length | a member's months enrolled, any covered day counting the month; full year as all twelve months | C1: days in place of months give the same need counts to the nearest 10 and the same verdicts (asserted) |
| 9 | Boundary inclusivity | below the threshold fails | NP-31 3.2; nothing within 5 per cent (asserted) |
| 10 | Rounding path | need counts rounded once to the nearest 10 from the unrounded estimate; ratios from the unrounded counts | the prompt's rounding sentence and NP-31 3.2 |
| 11 | Tie-break | none needed | no county on a threshold |
| 12 | Maturity and censoring | short enrollment censors a member's condition; the full-year members are fully observed but selected | the decisive construction; NP-31 2.5 states the unobserved members count and that a full-year member no claim identifies does not (SF19) |
| 13 | Order of operations | conform, identify, weight each identified member, sum by county, divide, compare | C1 (a sum of weights commutes) |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | replacements supersede, voided duplicates drop | NP-31 2.4; C1 for the call (SF5) |
| 16 | Identity normalisation | persons through client identifiers; prescribers through NPI | NP-31 2.2 (the client identifier on the enrollment record identifies the person) and 2.6 (NPPES by NPI); SF1; asserted, 2.2 read back through the verifier's own PDF reader |
| 17 | Netting against gross | net payments: final versions only | the asks' wording; the main call nets nothing |
| 18 | Dimensional units | persons, prescribers, US dollars | the files |
| 19 | Code and status semantics | Appendix A codes, frequency codes, eligibility groups | Appendix A; the producing systems' own codes (the claims system's frequency codes 1, 7 and 8, every 7 and 8 naming the claim it adjusts in orig_icn, under NP-31 2.4's version sentence; the enrollment system's four eligibility-group labels); same call (SF4, SF5); asserted |
| 20 | Integerisation | prescribers and members whole; need estimates fractional, rounded at the end | C1 |
| 21 | Clause scope | NP-31's standards apply to each county separately | NP-31 3.1 and 2.5 "measures each county from its own members" (SF18) |
| 22 | Forward window contents | none: the designation reads a closed contract year and 1 November 2026 | the call is retrospective because NP-31 designates from the closed contract year and the pilot starts in 2027 |

### Literal reader

Executed word for word, NP-31 counts each county's adult members who have each condition, every one of them whether or not a claim or encounter identifies it, estimated by Network Analytics from the county's own members; it names no method. The literal estimand is the number of members with each condition, and the identified count is a reading 2.5 forbids. NP-31 2.5 also counts a member enrolled all twelve months whom no claim identifies as not having the condition, so the share of full-year members identified within twelve months is 1 and no hazard is carried past the year. The pack supports the estimate through each identified member's own record: the full-year members' first identifying months give the share a window of each length identifies, and each identified member counts as 1 over that share at its months enrolled; the share taken by eligibility group, by county and group or over days gives the same counts to the nearest 10 and the same verdicts. The full-year prevalence, whole or within eligibility group, is not another reading of a term: it is an estimate the data refutes, since expansion adults enrolled three months are identified at about half the share of the full-year expansion adults over their first three months while those enrolled seven to eleven months match the full-year members over the same months.

### Oracles

None. No control, published figure or reconciliation column confirms any rung: the network adequacy report scores time and distance, meets its standard in every county and carries no condition counts; the population estimates carry no member counts; the deactivation report confirms deactivations on every rung alike.

### Ask sheet

- **Ask A, the payments, by county and quarter (scorecard) and by county and eligibility group (conformed file):** the plan's net payments on fee-for-service claims for services behavioral-health prescribers rendered to each county's adult members, whole dollars. H18 home: a measure every county carries (what the plan spends on prescriber services where it would fund recruitment), on rows the main call never reads (the paid column). Use: the board's budget line beside the designation. Primary device: D6, an event's quantity on every line it covers, grain unstated: the extract repeats a claim's paid amount on each of its lines (an evaluation and management line with a psychotherapy add-on carries the claim's total on both); no shipped file glosses the column, and the tells sit in the claims file itself (one paid amount on every line of a multi-line claim, add-on lines paid above their own charge), which is the battery's header-to-items check (measured below: spent). Hazards: H1 the frequency codes (replacements, chains of two, voided duplicates); H2 group practices and the telepsychiatry group billing under their own NPIs (the rendering NPI identifies the prescriber); H3 the switch, the reactivation and the deactivated prescriber whose taxonomy comes from the last record; H4 sub-capitated encounters carrying 0.00. Path: claims, spans, NPPES monthly and weekly files, deactivation report, fee schedule, NP-31 (seven files, twelve columns). Stops (built): the answer; every line summed, 12 to 46 per cent over in every one of the forty county-quarter figures; every version, 1 to 10 per cent over in 30 or more of them; both, 19 to 57 per cent over; the billing provider's taxonomy, 49 to 100 per cent under.
- **The conformed file's adult members by county and group:** construction (persons by client identifier, county and group on the last enrolled day); the cracker has it.
- **Main population zero-counts:** the paid column is read by no step of the call; every version and the final versions identify the same members and the same visits (asserted), so the frequency-code hazard is neutral to the call.
- **Hazard table (built):** H1 moves nearly every payment figure (1 to 10 per cent); H2 moves every county's payments (49 to 100 per cent under on the billing taxonomy); H3 moves Grant's, Chelan's and Benton's; H4 moves nothing (texture).
- **Referee:** the fee schedule, which bounds each line and arbitrates the paid amount's grain without handing over a level; nothing ties only under the golden.

| Ask | Cracker (landed the call, ran the battery, executed every filed rule) | Verdict |
|---|---|---|
| A quarterly payments | the header-to-items check finds one paid amount on every line of 3,756 of 3,756 multi-line fee-for-service claims and 4,729 lines paid above their own charge; final versions, the rendering NPI per NP-31 2.6, each claim's paid amount once, the member's county per 2.3, the service date's quarter: 40 of 40 kept | keep |
| A group payments | the same path by the member's eligibility group: 40 of 40 kept | keep |
| Conformed adult members, and the four counties outside the critical components (prescribers and need counts) | the call's own conformance: 52 of 52 kept | keep |

- Ask weight measured: block 4 less blocks 1 and 2, 132 figures (the four counties' 12, the 40 quarterly payments, the conformed file's 40 members and 40 payments), one share of the 55 each.
- Mirror leakage: 34.1 per cent of ask weight (rung 3 off the call, without the battery: the four counties' prescribers and the 40 conformed members; with the battery, the payments being decoupled from the call, 93.9 per cent).
- Pair ceiling: 81.8 (cracker 100.0 with 132 of 132 kept; mirror 63.7 with the battery, 30.8 without it, a pair of 65.4; two careful responses on the call 100.0; the full includer, the cracker's own path, reproduces figures.json, 132 of 132).
- Measured by: generator/ceiling.py, on target.zip md5 3eeae116705fd8fc3e72cd4f9c1b3aad (2 November 2026). The ask layer is spent: /fix-rubric owed (Tried and rejected).

### Pre-ship check

- **Gates:** generator checks 118 of 118 (the leak gate: no file under target/ describes the data, by name, sheet name and header, each with a positive control; closure rows 16 and 19 read back through the verifier's PDF reader and the systems' own codes; the golden against the generator's truth: persons, practising prescribers, the exact allocation of each condition by county, group and kind of member, the first identifying month the generator assigned and its exact F(k) in every county, group and months enrolled; the three-rules block on the clean truth, the reader's route and the default path filing the six and the window weighting alone the five; every route by name; the window weighting by group, by county and group and over days giving the golden's thirty verdicts, margins of at least 7.1 per cent and the same need counts to the nearest 10, every golden count at least 2 from its rounding edge; the reader's route failing Yakima on all three standards by 6 per cent or more; the data's evidence that the seasonal members are identified at about half the full-year share over the same window while those enrolled seven to eleven months match it; SF1 to SF19; the double-error grid; the separation of the payments from the call; the payments against the generator's claims and their stops; the lesser-of tie-out; realism, including spans starting no earlier than the 19th birthday, full diagnosis codes, the adequacy report's June members tied to the spans and lines paid at their charge); the independent verifier on its own pandas path, reading NP-31's thresholds and its 2.2 and 2.4 sentences back from the PDF (the designation, every scorecard row, the forty quarterly and forty group payments); two consecutive builds byte-identical (14 target files, 2 goldens, metadata.json, figures.json); target.zip cut from the final build and equal to target/ file by file; figures_check 206 of 206; voice-check PASS at 735 characters; precut on 2 November: FAIL on the honest ceiling alone (pair ceiling 81.8, the cracker keeps Ask A), the ask layer owed to /fix-rubric.
- **Input gates:** 14 files in three formats (csv, xlsx, pdf), the enrollment spans at 137,838 rows and the claims at 104,860; three distractors named in metadata.json (the network adequacy report, the population estimates and the November weekly NPPES file), none read by the golden.
- **The 10/10 rules re-read against the built pack:** the decisive step is the field's estimate (each identified member corrected for its own window's sensitivity, measured on the fully observed members), executed on the clean truth in checks.py; the mess (NPPES vintages, versions, keys, split ZIP codes, mailing addresses, lesser-of payments) is Layer 1, and no Layer 1 slip alone moves the call except reading away NP-31 2.7's service requirement (SF14).
- **Golden realism:** the scorecard is the board's workbook (finding title, the five rows shaded, verdict cells marked, a notes sheet whose definitions come from NP-31 and the extract, precision by quantity: members whole, ratios to one decimal, the reach in whole per cent); the conformed CSV in the systems' vocabulary, one row per county and group in FIPS order, carrying only what the prompt asks.
- **House fixes:** H1 container clean (target and golden); H9 metadata.json names every shipped file, and no file under target/ describes the data (asserted by name, sheet name and header, each with a positive control); H16 no claim adjudicated after the 31 October run-out and no enrollment end after the 12 November pull (later ends read as open spans); H21 agency, practice and clinic names built from regional landmarks no real agency carries; H23 the asks presuppose nothing about which counties qualify.
- **Guard:** heart WARN (overuse.objective only; the slot's first design differentiated, nearest other driver 0.08); surface promotes task457 (back to back, general surface similarity) and task456 (decisive gap and decision type), both differentiated on the card.

### Leak check

- **leak.py --asof 2026-11-12: REVIEW, no LEAK.** Sweep 3: the golden figures 25.9, 4.1 and 2.1 match the policy's ICD code F25.9 and its section numbers 4.1 and 2.1, and the policy names the ten counties as its service area, not as designations (harmless). Sweep 4: the policy carries ordinary nouns of the stump paragraph (member, enrolled, counts, enrollment); it states the population (members counted whether or not a claim identifies them) and names no method, window or seasonal member; the prompt's deliverable sentence names the need populations it asks for (harmless, the asks' own nouns).
- **Reader pass 1 (first design):** filed the first design's five by standardizing the full-year prevalence by eligibility group; question 6 answered as an analytical choice; tells fixed in the generator (truncated second diagnosis codes, prevalence identical across counties, payments always at the fee, mailing addresses always the practice's, organisations under a prescriber taxonomy, adequacy members not tied to enrollment, two-decimal ZIP ratios, a two-row Appendix C, a three-page policy). The stump was re-centred (Tried and rejected).
- **Reader pass 2 (re-centred):** filed six (Adams, Douglas, Franklin, Grant, Okanogan and Yakima) through the full-year prevalence and an exposure-bin reweighting within eligibility group (Yakima 2,660 with a serious mental illness, 15.4 per 1,000); question 1 none; question 2 none (the adequacy report marks every county Y on time and distance, a declared distractor); question 3 the dictionary, the manifest and the NUCC list (the pack's registers, none touching the decisive step); question 5 NP-31 2.5 fixes the population and leaves the method open; question 6 an analytical choice. Tells: the weekly NPPES files' only deactivation stubs were the plan's own cases (background deactivations added each week); the NUCC and ZIP files holding the codes and ZIPs in use are their dictionary-stated scope, 86 per cent of lines at the fee is how Medicaid pays, and every county meeting time and distance is the usual pattern (harmless). The 2026 NPPES update dates it missed are in the monthly file, and the 117 members with two spans ending on the last day have one county and one group (checked). Payment readings: the last-day county per NP-31 2.3 and the prompt's "its adult members", service-date quarters per "rendered ... in each calendar quarter" (both asserted in the golden, unchanged).
- **Judge r2 (re-centred):** DETERMINISTIC, FIX_NOW: Okanogan's reach sat at 58.5 per cent, 59 on the plan-wide window shares and 58 on the county-and-group shares; and an untruncated constant hazard moved several counts across their nearest-10 bins. Fixed: NP-31 2.5 now counts a full-year member no claim identifies as not having the condition (SF19), the scorecard shows its ratios and reach from the counts as shown with the standards judged unrounded, the write-up states counts, prescribers and verdicts instead of per-county ratios, its evidence figures moved to the two-month window (1.6 and 3.2 per cent, clear of rounding edges), and the November deactivation report no longer lists the NPI reactivated on 20 October. The call, the stump and every count are unchanged.
- **Reader pass 3 (after the r2 fix):** filed the same six (Yakima on all three standards at 21.6 per 1,000 for the opioid ratio) from the full-year members as the benchmark, by county and group; question 1 none (NP-31 2.5 says to estimate and sets the full-year counting convention, not how); question 2 none; question 3 the dictionary, manifest, NUCC, ZIP and deactivation files (registers NP-31 2.6 and 2.7 need) and the fee schedule's lesser-of line (the payments ask's tie-out, needed for its determinism); question 5 2.5 fixes the population, not the estimator; question 6 an analytical choice. Tells: the adequacy report's percentages carried six decimals (now three); the rest are the files' stated scope or the real files' own format (deactivated NPIs as NPI-and-date stubs, a state-selected crosswalk), harmless.
- **Judge r3:** DETERMINISTIC, APPROVE: every golden figure reproduced (members, identified counts, the 131 prescribers, all twenty nearest-10 counts under the window weighting pooled, by group, by county or by county and group, the forty payment cells and the conformed file); stump power strong (the carried full-year prevalence files six, the identified count three); Gate G statistical_rigor, analytical_non_defect; three rules pass. Its optional note (indexing the window by first-to-last span instead of months enrolled moves 8 of 20 counts for members with coverage gaps) is left unfiled: the judge found the data choose months enrolled (gap members' implied prevalence matches their contiguous peers only under it), and a policy clause naming the exposure would point the solver at the decisive step.
- **Re-check 1 November (the new leak gate): LEAK** on `extract_manifest_2026-11-12.csv` and `network_analytics_data_dictionary.xlsx`, files whose names say they describe the data. Both no longer ship (Tried and rejected); no document's text changed. **leak.py --asof 2026-11-12 on the new cut: REVIEW, no LEAK.** Rulings: sweep 3, NP-31's section number 3.2 and its list of the ten counties as the service area (not as designations), harmless as before; sweep 4, NP-31's ordinary nouns (member, enrolled, counts, months, enrollment) state the population and name no method, window or seasonal member, and the prompt's deliverable sentence names the need populations it asks for; sweep 11, the counts the prompt discloses are the call sentence's decision parameters (frozen) and the deliverable sentence's "for each of the ten counties" and "each of the three standards", and the shell quota's "which" is the frozen call sentence while "put" opens the ask sentence the owed rework rewrites. The dictionary's Columns-sheet REVIEW and the metadata subdomain REVIEW (the first design's method in the subdomain) are gone with the repair.

## Tried and rejected


- Over-coverage of the provider master (NPPES records of prescribers who stopped practising) as the decisive step, estimated from a revalidation wave or a recredentialing cohort (design, on paper): the verified half generalises to the unverified with one ratio a strong analyst writes by reflex, and the scheduled version reduces to "status as of the last check", the lesson task457 already teaches; kept as Layer 1 through the policy's own definition of a practising prescriber.
- A two-step floating catchment (prescriber capacity shared among every county within reach) as the decisive step (design, on paper): the estimand either says the capacity is shared, which files the method, or does not, and then the one-step count is a literal reading; a fork either way.
- Prescriber retention by Kaplan-Meier as a third standard (design, on paper): the textbook survival estimate is the reflex (task134 loop 0 died on it), so it carries no stump.
- First scratch simulation (qualifying claims about one every two months, a third of expansion adults in short spells): the recorded count fell only 3 to 6 per cent short in the farm counties, too thin for the thresholds to sit between the readings; rarer qualifying claims and the farm counties' seasonal spells put the shortfall at 13 to 19 per cent, and all three standards now rest on need.
- The identified count as the default path with NP-31 silent on members no claim identifies (design, before data): a literal judge reads the claims as the count (task448's three portal returns on the same shape), so 2.5 states that the count includes members no claim identifies; the default path then completes the count, and the stump moved to how the completion is done.
- Conditions drawn at random per member, then allocated exactly within each cell (generator, 15 October): the golden and the eleven-month cutoff differed by 1 to 3 per cent, splitting nearest-10 bins in seven counties; nested exact allocation by months enrolled, and every member with a condition enrolled ten months or more identified, bring them within half a per cent.
- Six stale listings in Yakima (generator, 15 October): reading away NP-31's service requirement while completing with the unstratified full-year prevalence filed the five by two errors; one stale listing closes the cell.

- The full-year prevalence standardized by eligibility group as the decisive step (first design, built and judged DETERMINISTIC/APPROVE at stage 4, 15 October): the isolated leak reader stratified by group by reflex, prompted by the full-year members' group mix and the conformed file's grain, and filed the five; the stump moved to the seasonal members' own records (they have the conditions about half as often as the members who stay), and the first design's golden became the default path.
- First identifying claims drawn month by month at random (generator, 15 October): the months-observed weighting by plan, by group and by county and group differed by up to 5 per cent in the small counties and split nearest-10 bins; the first identifying month is now allocated exactly within county, group and months enrolled, so the variants agree to under one member.
- Adams at four prescribers on its first need (generator, 15 October): reading the ZIP's residential share or any listed taxonomy added one Adams prescriber and moved Adams off the designation through a Layer 1 slip; Adams's need is raised so that five prescribers still fail both ratios, and Grant's opioid need so one more prescriber still fails it.
- The data dictionary and the export manifest (shipped 15 October; re-check 1 November under the new leak gate): files that describe the data (dataset-generation 3), the dictionary's Columns sheet glossing the very columns the call and the asks join; both no longer ship, provenance stays in metadata.json (whose subdomain no longer narrates the first design's method), closure rows 16 and 19 now cite NP-31 2.2 and 2.4 and the producing systems' own codes, and no sentence was added to any document.
- Ask A's device D6, the claim's paid amount repeated on each of its lines (measured 2 November by generator/ceiling.py's careful-solver cracker on the cut pack): the battery's header-to-items check finds it in the claims file itself (3,756 of 3,756 multi-line fee-for-service claims carry one paid amount on every line, 4,729 lines are paid above their own charge), so the cracker keeps all 132 ask figures and the pair is 81.8; the 15 October sheet's cracker summed the lines, a narrowed cracker. Re-siting is barred because the claims file is read by the call and frozen, and its in-file tells stay; cutting Ask A leaves only the construction figures (52 of 52 kept, two careful responses on the call at 100).
- Full replacement on a pharmacy benefit extract, buprenorphine and antipsychotic prescriptions behavioral-health prescribers wrote, a prescription transferred between pharmacies under a new number (design, 2 November): with the date written shipped the link is a shared value a uniqueness test finds; without it the link is the remaining refills carried to the new number, an exact counter continuation a told reader finds in a few lines (task228's death), and the remedy after noticing is the transfer's defining field; drug fills also put condition evidence beside NP-31 2.5's estimate, a risk to the main call.
- Full replacement on the agencies' sub-capitation remittances or the Health Care Authority's premium remittances, by coverage quarter and rate cell (design, 2 November): a retroactive recoupment and its re-payment, a remittance reconciled to its rate schedule, a member-month paid to two agencies, all battery items; the rate cell's group against the conformed file's group is a fork, and worded it is executed.
- Full replacement on third-party liability recoveries allocated to the claims they recover by the sums they equal (design, 2 November): the arithmetic link holds, but per-member netting lands every county and group figure, so only the forty quarterly figures carry it and the cracker keeps 92 of 132 (two careful responses on the call near 83); hiding the member behind the subscriber's key makes it a record under another holder's key, task147's family.
- Full replacement on an appointment availability survey of the directory's prescriber offices, duplicate and stale listings reaching one scheduler (design, 2 November): the link is the identical offered slot, a shared value, and coincident slots at two offices give it a second explanation; the listing's prescriber checked against NPPES is the battery's finer-key check; offices carry no eligibility group.
- Full replacement on community reinvestment grants against the disbursements that pay them, and on encounter valuation at a fee schedule priced per hour for a code billed in quarter hours (design, 2 November): matching disbursements to installments and pricing units against the schedule are both reconciliations to a filed schedule, battery items; the grants carry no eligibility group, and the valuation reads the call's own encounter rows.
- Architecture 1 as a whole, re-rooted 2026-11-02 (main thread's order): the Medicaid county designation's main call held up, but its ask layer was spent under the careful-solver cracker (132 of 132 kept, pair 81.8) and no re-site, cut or replacement passed; one architecture per world, so the slot moves to a new world, dataset, generator and shell in General Statistics & Data Science (the City of Elsworth's 2027 meter rates). Screened at this draw and set aside before the card, each on file or on the rules: test equating (every mechanism spent in the corpus), length-biased snapshots and rapid guessing (dead on file), a garage's overnight stock as the main call (a storage term, task120's lesson, and a careful reader walks each permit card across midnight), the ski lift's queue from lap times (a strong reader estimates waits from laps by reflex), journeys linked across a hub by passed-up departures (the filed WHAT would name the step, lesson 10), the parcel zone that reveals a shipping node (a reading), and composition_mix, G6, G13, statutory_or_regulatory_filing and period_close (window bans against task453 and task154 at `check`).
- The parking study's expansion (all vehicles over paid vehicles at the passes) as the default path, stated in a shipped study or memo (draw, 2 November; coordinator's lesson 11): a shipped document stating or applying the expansion is a licensed literal method against the golden; no document states one, and the default path is the analyst's own additive count model, refuted by the runs' unpaid mix by time of day.
- The sensor pilot in two downtown meter zones as the back-test (design, 2 November): sensors in meter zones give the judge a direct in-window measurement for those zones and tie any sensor fault to a graded figure; the back-test is downtown's own 12:30 run, and the pilot moved to four free streets, where it carries the asks on a system the call never reads.
- Residential permits in force on the first of each month (a term readable only from a prorated fee), impound storage days from the fee, garages' free spaces at noon (an overnight carry-over), card chargebacks by parking month (design, 2 November): the asks' nouns invite the question each device turns on, or the careful state walk finds it; a permit registry with plates would also have named the residents' overnight cars on the call's own runs.
- First contamination setting (screen, 2 November): school-run stops on an afternoon run starting as late as 4:45, and residents gone by 10:30, left the afternoon run's and the smaller run's unpaid counts on the golden for two of the five districts (two cheap routes landing); the afternoon district run starts by 3:45 and overnight cars leave by 11:30, so every count-based route flips the same five (R3c).
- Missed district runs (screen, 2 November): a day with one run forced a fill convention, and filling with the zone's mean or skipping the day split Delmont's whole-per-cent figure (66 against 67); the routes run every weekday, so no zone-day lacks a run either side.
- Lower-flip districts on an afternoon profile (screen, 2 November): at the 3 p.m. peak the blocks were full, the school-run stops found no space, and the afternoon run's count landed Fernwood and Irvine Market; both now have flat profiles.
- Straddling vehicles recorded on two adjacent sensors as the second pilot device (design, 2 November): a count-once rule the rows do not force (the family the judge sent back as unforced); the re-baselining blip replaces it, whose gap no car can make.
- 2026-11-02, stage 4 (architecture 2 spent): the judge (cut 950254e3) returned NOT_DETERMINISTIC, SEND_BACK. Every golden figure reproduced (all 18 zones, the rates, the pilot streets), but Rule 12.04 counts a vehicle "whether or not that vehicle paid" and no shipped text says how point-in-time enforcement reads become occupied minutes inside a window no neighbourhood run covers. The judge licensed the mean unpaid count on a zone's runs, which moves Alder Row, Cascade Avenue and Hollis Street to raises and Fernwood and Irvine Market to holds, and read the golden's both-runs panel as an unfiled imputation (Gate H3). The design's own validation, downtown's in-window run, supported the mean-count model downtown and nothing inside the window tested the panel in the neighbourhoods, so the golden's imputation was argued, not forced by the data. The pilot-street asks forked too: the flicker merge, the silent sensors and which stays count. Re-rooted at stage 1 into another world and dataset.
- 2026-11-02, architecture 2 as a whole (a city's meter rates from midday occupancy, spent at the stage 4 judge, NOT_DETERMINISTIC SEND_BACK on Gate H3): the golden's imputation of unpaid vehicles over a window no neighbourhood record covered was argued, not validated by the data where it applied, and the mean-count reading was licensed; one architecture per world, so the slot moves to a new world, dataset, generator and shell.
- 2026-11-02, architecture 3 draw, seasonal-adjustment-official-time-series-production screened closed for an honest analytical ETL call (reported to the main thread): benchmarking and the step problem (task123, task482 and task465 on file: the current-year extrapolation is a fork, Denton's end ratio sits within tenths of pro-rata's, the ratio path is assumed; the back-tested ratio trend is the QNA's own bias adjustment, a named refinement; a panel-redraw sawtooth is a visible jump unlinked and a plain trend linked; a ratio varying by season or unit is task474 v1's spent driver), chain-linking overlaps (a convention filed or a fork; chain drift is task463; an overlap window's mix is task481), calendar and trading-day regressors (every calendar composition is task477's opportunity count; moving holidays spent by task162, task467, task135), outlier types at a break (task453 v1, task146, task467; a school-calendar seasonal break is task482 arch 12's reflex), concurrent against revised factors and revisions (task482 arch 12: rule application once vintages ship; Layer 1 by CLAUDE.md; completion spent), the seasonal filter itself (task464 Horn C: 0 of 7 settings), and on paper a collection gap imputed from an uninterrupted series, weather normalisation with a data-forced balance point, card- or registry-driven benchmark ratios, intercensal error-of-closure wedges, staggered VAT quarters and cohort-carried intercensal profiles, each dead on a named record or rule.
- 2026-11-02, architecture 3 draw, census-register-administrative-data-quality and emissions-inventory screened closed on the coordinator's lifted bar (reported to the main thread): every input an inventory figure has and every register-quality quantity has a record (task464's 10-27 enumerations plus task453 v3 and task454 v2 since), and each candidate died on paper: abandoned-mine methane decline (the IPCC hyperbolic is the field's method; a cumulative-gas decline is task180's law; a flooding cut-off needs task154's groundwater world), tuned stack tests (task478 v6), feed-additive dose response (task478's input property), sub-threshold facilities by a truncated size fit, lease fleets at the lessor's address (task454), soil and wastewater N2O pulses (task452 v1), purge-cycle over-coverage (lesson 10, the silence family, task476's phase), stale industry codes by time since check (the classification family, 1.1c), the cancer registry's flow method (task448, task471), own-children birth completeness (task243), threshold bunching (the fit forks), coverage ratios carried from a census (the ratio-forecast fork), attainment completed by cohort (task453 v3).
- 2026-11-02, architecture 3 draw, the house route into data integration screened before this card, each dead before a harness: a convex N2O response to field nitrogen (task229's Jensen gap), unconstrained demand behind stockouts (task18, task108, task168, task137), sticky contract prices passed through at renewals (task179's reset-month screen), appraisal-smoothed private fund marks rolled to the year-end (task308, task167, task128, task135: Geltner and Dimson are taken on sight), distributor returns from each holder's channel stock (task154's 11-02 screen, beside task161), learning curves in a contract's estimate at completion (task46, task132, task170, task174), salmon biomass shortfalls per handling event (task180's usage law in fish), counter coincidence losses and size-biased net sampling (task473's level-dependent catch), feed-implied biomass (task482 v12's load-per-head), first-expiry queues for dated stock (beside task467 v2's leaving order), state transitions over unequal inspection intervals (task301), stockpile density by pile height (a covariate one column away, 1.1c), mirror-trade freight by weight (a rate on the wrong exposure, beside the batch's trade world), stock write-downs by forward cover against age (the excess-and-obsolescence reserve is the textbook and lands the call), and pack-size price benchmarks (the comparison is WHAT).

- 2026-11-02, architecture 3 stage 2, the covenant: a minimum tangible net worth floor (the draw's first wording) moves with the provision net of the tax it saves, and the tax effect is a convention the pack would have to file (a fork on the call); the facility's borrowing base, 62.5 per cent of inventories at the lower of cost and net realisable value, moves with the provision itself, so the call runs on it.
- 2026-11-02, architecture 3 stage 2, the draw's two ask records: the intercompany margin in stock (purchase receipts against a transfer-price list) is the textbook consolidation elimination, which the careful solver performs on sight (the coordinator's flag); the trade buyers' mixed lots sit on the rows the call reads for its trade rate, so an ask device there would sit in the main population. Both replaced by the 2025 order books.
- 2026-11-02, architecture 3 stage 2, ask devices screened on paper and dropped: the item master's 2027 divisions against the 2026 stamps (a vintage pin names the device's dimension, and without it IFRS 8's restated comparatives make the master's divisions a coherent literal reading); the old system's cutover closing open orders as despatched on 31 December 2025 (the duplicate in the new system's January lines leaves the archive's reading coherent, lesson 8); a customer's own article numbers swapped into the item column of its EDI lines (silent only if every customer number collided with an AHB article, which no real numbering does; otherwise the orphans hand it over); price corrections posted as credit and rebill (the battery's rescind handling nets them right); a container's freight posted on a later month's line (the posting month is a coherent literal reading of the cost's period).
- 2026-11-02, architecture 3 stage 2, calibration: the trade buyers' biggest lots (Valuehall's 2024 clear-out) first recovered below the small lots by chance, which a judge could read as a trade rate that falls with volume; two of the subsidiaries' own range clear-outs were added as single large lots and the price noise narrowed, so lots over GBP 150,000 recover 0.102 against the rest's 0.101 with no slope in lot size (checks L7.trade_not_capped). The pool, the drawn balance and the normal lines' cover were set so the standing family of the provision, the inventories after it, the base and the shortfall each sit inside one 0.1 million bin (SF17, SF18).

- 2026-11-02, architecture 3, Ask B's first device (the UK company's euro-invoiced Irish customer under an order report with no currency column, forced by matching euro prices) replaced at the coordinator's order before stage 4: task467 v2 shipped the same family an hour earlier (an Irish site's voucher values in euro with no currency column), and two builds in one batch carrying one device read as templated. Screened for the replacement and dropped: invoiced value booked on despatch against a year-end transit cut-off (it moves units with values, so the blocks stop being disjoint, and its rows sit at the edge of the call's 2026 window); rebates netted on some customers' invoice lines and not others (the net-or-gross reading is a fork the asking sentence would have to pin, and the terms that force it would be a schedule the cracker reconciles to). The price credits on the order's first line replace it.

- 2026-11-02, stage 4 judge (ask 7 only, NOT_DETERMINISTIC, SEND_BACK on a sound architecture): AHL's July price credits sat on the item the credit screen defaults to, the order's first line, and the judge read "net value invoiced by division" as the ledger as booked, a coherent literal reading (KD 40,977,000 against 41,162,000); that 182 credits sat on items charged the customer's own price was an economic impossibility, not a literal one. Route 1, a pin in the asking sentence ("at the prices its customers were due", or "net of the price credits against the lines they corrected"), screened and dropped: the pin tells the careful cracker that credits correct lines and the only way to find them is the overcharge comparison, so the cracker lands the block. Repaired in the rows instead: AHL's system takes a price-only credit on its non-stock code NS001 (a stock item on a credit line books goods back in), one credit per corrected line, so as booked no credit has a division and the as-booked reading cannot be formed; each credit equals one line's overcharge to the penny.
- 2026-11-02, the four covenant figures at 0.1 million: the pass-2 report paired the non-promotion recovery (0.628) with 1,390 a day for a GBP 5.14m provision (5.1 against 5.2, inventories 39.5 against 39.4, base 24.7 against 24.6); measured over 5,440 defensible members (`## Pre-ship check`) the provision runs GBP 5.13m to 5.25m, the inventories 39.36m to 39.47m, the base 24.60m to 24.67m and the shortfall 0.449m to 0.522m, so every 0.1 million bin but the shortfall's was crossed and the shortfall's held only without the 1,400 probe. Moved to the units the family holds in (determinism-check section 3), with no method filed and the world unchanged: the provision to the nearest million, the inventories and the base to the nearest 0.5 million, the headroom or shortfall to the nearest 250,000.
