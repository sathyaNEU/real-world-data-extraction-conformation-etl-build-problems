# task161 design note

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task161.json`, registered 2026-10-18T01:20:40Z, guard WARN (no BLOCK).
- **Pairing:** Supply Chain & Logistics (house domain `supply-chain-logistics`, task type fulfillment and warehousing), client domain Urban & Regional Science, task type `forecasting`. Objective Forecasting & Predictive Modeling.
- **Seed:** FC32. Kept: the world (an import 3PL beside the San Pedro Bay ports, 40,000 rack positions in its own buildings), the decision (how many of six 4,000-position overflow blocks to take for January to June) and the quantity (the half-year's positions above the 3PL's own racks). Not kept: the seed's error-band mechanism, its leasing test on a lower edge, its option date and its booking notices for the half-year.
- **Shape:** 02, forecast across many periods (each month of January to June 2027 against the racks), the call read off the monthly path by the space policy's block test. Criteria: the call and its components, the port ask (ten months, two figures each), the chart (five parts), the two files: 28 or more.
- **Strategy:** `other` (a stock balance: bought-ahead pallets netted per account against that account's own shipments). Gap time, then population. Decisive generator G7 (when can the excess physically leave: only as its owner ships), then G13 (the burn runs through months no earlier burn ran through for the seasonal accounts) and G2 (the unit of netting is the account's own stock, not the book).
- **Data-native sentence:** each account's bought-ahead pallets leave the buildings only as that account ships, and in every earlier rush an account's excess fell by a steady share of its own shipments until its own excess was gone; this rush's excess sits mostly with five seasonal accounts that bought for their whole 2027 season, whose own shipments run at their first-half low through June, so it outlasts anything the earlier rushes' fade suggests; the one earlier rush in their low season (April 2025) shows it.
- **Furniture:** forum executive_team; forcing event season_or_peak (the half-year after the rush; the park lets its six blocks for the January to June term to whoever commits first, with no option or exercise date in this world); organisation logistics_or_3pl; role capacity_planner; context artifact filed_standard (the 3PL's space policy filing the forecast basis and the block test, and the park's block offer); calibration existing_book_actuals (the book's own 2019 and 2025 rushes).
- **Personas** (guard.py names --geo 'United States' --seed 161): Mariah Norman (VP Operations, owns the space policy), Jerome Lam (WMS systems lead, owns the export dictionary), Frederick James (customer service manager, keeps the booking-notice tracker; drawn at stage 4, when the first name drawn at the draw fell under the guard's first-name ban against a recent build), Brandon Page (leasing manager at the park's landlord). Karen Haynes was drawn and dropped (first name on an older build).
- **WARN answers.** overuse.gate_g: method_or_model_selection is the honest mechanism (a fade, a book-level burn and a per-account burn all fit the small earlier rushes on the book total; only the rushes of different season and the accounts' own paths separate them), and the strategy and generator differ from every one of the five. repeat.decision and repeat.question_form against task160: the call is a count of blocks, so it asks how many; task160's is a count of nurse shifts in another domain, mechanism and furniture. Deliverables are pdf plus xlsx, clearing repeat.deliverables.
- **Same puzzle and same driver** (older): differentiated on the card against task259, task87, task135, task451, task460; none nets a stock against its owners' own use.
- **Sources read at the draw** (one line each):
  - `guard.py mechanisms --objective forecasting`: the stock and queue drivers on file (task138's store rebuilt through a balance, task148's queue with reneging, task156's volunteer backlog, task159's platform backlog) each build a quantity from inflow against a service rate; none nets a stock bought ahead of a price step against its owners' later demand, and none turns on whose stock it is against whose shipments a fade was measured on.
  - task152 (a forward sale at P50 with its sigma) and task151 (a stepped payout from a predictive distribution): the commitment here is read off the forecast path's level, never off a tail or an interval.
  - task157 (a returning wave sized from its leading edge): members come back on a calendar; here nothing comes back, a held stock leaves at its owners' pace.
  - task153 (a yard's draw capped per segment at a tankful): a min() per segment of a vehicle's need; here the min() is each account's excess against its own cumulative burn.
  - task154 and task160 (forecast_method_backtest, G16): nothing here files a back-test or a selection criterion; the method is the balance, and the earlier rushes are the record a planner reads.
  - Urban & Regional Science forecasting pattern 1 (back-test from the forecast origin): each rival is checked against the earlier rushes from its own origin, which is how a planner checks a fade against a burn.

## Default path

1. Stack the legacy WMS on-hand export (to 30 September 2022) and the new WMS nightly snapshot (from 12 September 2022, sites summed, run stamps converted to the Pacific close), map the accounts through the register, and average the book's pallets on hand by calendar month.
2. Take the book's normal stock from its clean months as a cover on shipments (pallets held against the mean of this and next month's shipments), and measure the book's excess over it after each earlier duty step (1 September 2019, 5 April 2025, 7 August 2025, dates from the broker's advisories).
3. Fit the fade of that excess: a half-life of 0.87 months on the three rushes (the median of 0.72, 1.30 and 0.87), the excess back to normal within two months.
4. Project the close of 31 December from the close of 6 December plus the December booking notices less the rest of December's forecast shipments, take its excess over the normal stock, and fade it at the fitted half-life through January to June 2027.
5. Add the faded excess to the 2027 normal stock, take each month's overflow above the 40,000 rack positions and run the space policy's block test: the first block is used 14 per cent of its position-months.

Ends on: 0 blocks (none)

Golden: 2 blocks

## Stump sentence

The default path fades this rush's excess at the 0.87-month half-life the earlier rushes showed, leaves overflow only in January and takes 0 blocks (none); the step that lands it there is treating the excess as a proportional decay of the book's total, when it is stock each account burns at a steady share of its own shipments, and most of it belongs to five seasonal accounts that bought for their whole 2027 season and ship at their first-half low through June, so the first two blocks stay full through June.

## Three rules

- **Task type:** urban-regional-science/forecasting (the house domain Supply Chain & Logistics, fulfillment and warehousing): a forecast of the book's monthly pallet positions for a closed future window, each candidate model checked out of sample on the book's earlier rushes.
- **Domain test:** the deciding quantity is the burn-down of bought-ahead stock, the warehouse planner's projected on-hand netted per owner against that owner's own forecast shipments (inventory netting, weeks of supply burned at sales pace); the estimator is each account's burn share from its own earlier rushes applied to its own seasonal shipment forecast until its excess is gone.
- **Swap:** "how many overflow wards should a hospital lease for January to June after an admissions surge" no longer reads: patients are not stock their owners bought ahead of a price step and draw down at their own sales pace, so there is no owner whose season sets the burn and no later intake netted against stock already held.
- **Layer 1:** the legacy WMS1 export (MM/DD/YYYY business dates, rows Monday to Saturday only, mnemonic client codes, Rosales on two codes until the migration); the new WMS nightly run (UTC stamps at 07:00Z or 08:00Z holding the previous Pacific close, balances by site, the Dominguez sublease a fifth site while let); the parallel run of 12 to 30 September 2022 in both exports; two former accounts in the history; the booking-notice tracker, three accounts' notices in boxes only; the receipts export with UTC confirmation stamps, ISO size-type codes and 53ft trailers; the two ports' monthly releases in their own layouts. Each is written by the system named and each natural mishandling leaves the call at 2 (asserted R2.1 to R2.6c); the sublease is not a mess item but part of the estimand (space policy 3.1 counts every pallet held with us).
- **Layer 2:** field_method; the choice that flips the call is projecting each account's stock as a balance in which its bought-ahead pallets burn at the share of its own shipments its earlier rushes show, against fading the book's excess at the earlier rushes' half-life or burning the book's total at the book's share.
- **Decisive step:** net each account's bought-ahead stock against its own forecast shipments at the burn share its own earlier rushes show, until that account's excess is gone, so the seasonal accounts' stock, bought for their 2027 season, stays until summer.
- **Not semantics:** every field, code, unit and date can be read correctly (the run stamps converted, the accounts mapped, the notices converted, the sites summed) and a solver who then fades the book's excess at the earlier rushes' half-life still files no block; no field, code or definition says how fast bought-ahead stock leaves or whose it is.
- **Not rule application:** the space policy files only the forecast basis (the accounts under contract, every pallet they hold in our racks or outside them, the mean of each day's close, the 40,000 rack positions), an account's normal stock (3.4: its cover times the mean of its shipments in the month and the month after) and the block test; no filed rule or procedure says how the stock above normal leaves or how to forecast it, so executing every stated rule on a fade of the excess files no block, and on a burn of the book's total files no block.
- **Analyst test:** a strong analyst who stacks both WMS exports, maps the accounts, projects December from the notices and reads the block test correctly, then fades the book's excess over its normal stock at the 0.87-month half-life the 2019 and 2025 rushes showed, files 0 blocks (none); burning each account's excess at the share of its own shipments those rushes show files 2.
- **Estimand:** the space policy, section 3: a space forecast covers the accounts under contract on the day it is made and counts every pallet they will hold with us, in our racks or outside them, as the mean of each day's closing stock in the month, overflow being that figure above the 40,000 rack positions of the four buildings, and (3.4) an account's normal stock its cover times the mean of its shipments in the month and the month after; section 4's block test; the window (January to June 2027) and the unit (whole blocks of 4,000 positions) from the prompt and the park's offer.
- **No decoy:** nothing is planted: no copied block, withheld rule, memo, draft, briefing or stakeholder figure argues a number of blocks; the earlier rushes are the book's own history, and no shipped file computes a forecast, a burn share or a block count.
- **No certified replay:** no certified or published figure is reproduced to recover a method; the earlier rushes are ordinary days in the WMS exports, and the burn is read from how each account's stock behaved after each step, not fitted to a printed total.
- **Lesson:** bought-ahead stock is a balance its owner burns at its own sales pace, so a fade measured on small pull-forwards that burned in their owners' busy season understates how long a large pull-forward bought for next season stays; no build on file nets a stock bought ahead of a price step against its owners' own seasonal demand.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 Fade the book's excess at the earlier rushes' half-life | no | no | yes, the first model of a temporary excess | no | no | no | readable |
| 1 Burn the book's excess at the book's share of shipments | no | no | yes, once the excess is seen falling in a line | no | no | yes, one share times shipments | readable |
| 2 Each account's excess falls by its own earlier fall per month | no | no | yes, by account is the next cut | no | no | yes, one rate per account | readable |
| 3 (decisive) Each account's excess burns at the share of its own forecast shipments its own earlier rushes show, until it is gone | no sentence names a burn, a share or an excess | no column holds an excess, a share or a season | no: the reflexes are the fade, the book total and the calendar rate | no control, corpus or published figure scores it | no sweep finds it | no: a per-account minimum over a seasonal path | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "take" a block | commit to the block for the whole January to June term | take a block for part of the term | none: no part-term block is offered | the offer: "Blocks are let whole and for the whole term"; space policy 4.1 |
| SF2 | overflow | pallets held above the 40,000 rack positions | above the racks' practical fill (39,740) | 2 | space policy 3.2 names the 40,000 rack positions; same call (asserted) |
| SF3 | the book's population | the 14 accounts under contract at the as-of | every account in the history | 2 | space policy 3.1; the two former accounts hold nothing at the close (same call, asserted) |
| SF4 | a month's need | the mean of each day's closing stock | the month-end close; the peak day | 2; 2 | space policy 3.1; same call (asserted) |
| SF5 | the block test | each block's own use, blocks counted in order | the average use of the blocks taken together | 2 | space policy 4.2; same call (asserted) |
| SF6 | in our racks or outside them | every pallet on hand, sublease and yard included | racked pallets only | 0 | space policy 3.1: "in our racks or outside them" |
| SF7 | the close of 6 December | the run of 7 December at 08:00Z | the run stamped 6 December (the close of 5 December) | 2 | the dictionary's run line; the close of Sunday 6 December equals Saturday's (same call, asserted) |
| SF8 | the rest of December | the tracker's notices in, forecast shipments out | December at last year's net flow | 1 | the tracker's header files the notices as the arrivals due after the close |
| SF9 | a notice in boxes only | boxes at the account's own pallets per box over the last 90 days | the book's pallets per box; the account's pallets per receipt row; no pallets | 2; 2; 2 | the tracker's planning basis; same call (asserted) |
| SF10 | the duty step | the date the duties apply from (1 September 2019, 5 April 2025, 7 August 2025; 1 January 2027 ahead) | the date of the advisory announcing it | 2 | the advisories' "on or after" lines; same call (asserted) |
| SF11 | the earlier rushes | the three steps in the advisories with the book's own stock in the record | any surge, the 2022 congestion unwind taken as a fourth | 2 | the advisories date three steps; same call (asserted) |
| SF12 | a block's position-months | 4,000 positions for each of the six months | 4,000 positions times days | 2 | space policy 4.2; same call (asserted) |
| SF13 | an account's normal stock | its cover times the mean of its shipments in the month and the month after, the cover its median over its ordinary months | the cover held against the same month's shipments; a centred three months; the next month; a flat median stock; a daily forward window of 21 to 30 days | 1; 1; 3; 1; 1 (block 2 at 0.73, the round 2 judge's measure) | space policy 3.4: "its cover times the mean of its shipments in that month and the month after" (SF13 asserts the policy line and measures the first four) |

## Ladder

Each rung is a full pipeline from the raw files. Figures are each block's use over the term (share of its 24,000 position-months), the call by the block test, all measured on the cut pack (checks.py L1 to L10, B1 to B4).

| Rung | Construction | Call | Block uses (1, 2, 3, 4) | Dies to |
|---|---|---|---|---|
| 0 (default) | book excess faded at the earlier rushes' half-life (0.87 months) | 0 | 0.14, 0, 0, 0 | the earlier rushes left out in turn (L8) and the owners' shipments (L9): the fade takes 10,926 pallets of excess out in January, more than the 1,095 held outside the five seasonal accounts plus the five's own January shipments of 5,749 |
| 1 | book excess burned at the book's share of book shipments (0.128 on the slope, 0.109 on totals) | 0 or 1 (2 in the round 2 judge's construction, per-episode shares 0.125 to 0.147) | 0.70, 0.33 (slope); 0.88, 0.44 (totals) | the book's share mixes accounts that hold none of this rush's excess with the five that hold most of it |
| 2 | each account's excess falls by its own earlier fall per month | 1 | 1.00, 0.65, 0.01 (median rate; mean 0.70, latest 0.48) | the April 2025 step: the seasonal accounts' excess fell in step with their own low spring shipments, not at their autumn rate |
| 3 (decisive) | each account's excess burned at the share of its own forecast shipments its earlier rushes show, until it is gone | 2 | 1.00, 1.00, 0.18, 0 | the golden |
| other side | today's stock held flat (the close of 6 December, November's mean, December to date) | 3 | 1.00, 1.00, 1.00, 0.05 to 0.48 | every earlier rush: the excess left |
| other side | no payback (the rush's stock held through June) | 3 | 1.00, 1.00, 0.85, 0.38 | every earlier rush: the excess left |
| other side | Holt-Winters on the book's monthly positions through the rush; the autumn trend | 5; 6 | | the record after every earlier step |
| other side | last year's January to June scaled by November against November | 0 | 0.67, 0.29 | the 2027 stock is this rush's excess, not a scaled 2026 |
| hedge | halfway between the fade and no payback | 1 | 1.00, 0.27 | neither half survives the earlier rushes |

- **Winners and margins:** the golden takes block 2 at 1.00 against the 0.75 line (flip: block 2 under 0.75 needs every account's share 52 per cent higher) and refuses block 3 at 0.18 (flip: block 3 at 0.75 needs every share 68 per cent lower). The nearest wrong rung on each side: rung 2 at block 2 = 0.65 (0.70 at the mean rate), no payback at block 3 = 0.85.
- **Position and dominance:** the golden is the only construction the earlier rushes do not reject that files 2; the corrections below it walk up (0, then 0 or 1, then 1) and the decisive move is the only one reaching 2; the other side's routes file 3 or more, or 0.
- **Out of sample on the earlier rushes (L8, V13):** each rush left out in turn and predicted from the other two, the mean absolute error of each account's excess path over the 90 days after the step, summed over accounts: burn share 2,421, fade 4,536 (47 per cent under), calendar rate 3,299; by rush (burn, fade): 2019 611 and 913, April 2025 1,047 and 2,546, August 2025 763 and 1,078. The burn is ahead of the fade on all three rushes, so 2019 is no longer a reason to prefer the fade; the April 2025 rush, the one earlier rush in the seasonal accounts' low season, separates them most.
- **Grid:** burn share per account (episodes weighted by shipments, unweighted mean, median, latest episode, pooled, times 0.85 and 1.15) by normal cover (median of clean months, mean since 2024) by shipment forecast (same month grown, two-year mean grown, no growth): all 42 cells file 2 (block 2 between 0.96 and 1.00, block 3 between 0.05 and 0.35); each earlier rush alone files 2; the fade at each rush's own half-life (0.72, 1.30, 0.87 months) files 0 (L6, L7, B4).
- **Worth:** rung 0 to rung 3 moves the call by two blocks; rung 2 to rung 3 by one.
- **Accidental landings, measured:** last year's January to June scaled by the projected close of 31 December against December 2025 files 2 (block 2 at 0.77, block 3 at 0.42), and by the close of 6 December against December 2025 also 2 (0.85, 0.52); the same carry by November against November, the latest full month, files 0. No natural change moves the December carries off 2 without moving the golden, so they are counted below.
- **Stump estimate:** a strong response reaches the per-account burn with probability about 0.10; the December carries add about 0.04 (a single December ratio on last year's first half is a rare route for a strong solver, and the November ratio a solver reaches first files 0); the flat hold (3) and the hedge (1) no longer land. P(one of the top two on the call) about 0.15, P(both) about 0.03; round 2's recheck, with the book-level burn able to land 2 in some constructions, put P(both) at about 0.045.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the 14 accounts under contract at the as-of | space policy 3.1; former accounts hold nothing at the as-of, C1 asserted |
| 2 | Unit of account | a pallet holds one position; blocks of 4,000 positions | space policy 3.2 and 4.1; the park's offer |
| 3 | Attribution window | calendar months January to June 2027 | the prompt and the offer's term |
| 4 | As-of dating | the close of 6 December 2026, notices for the rest of December | the dictionary's run-stamp line; the tracker's header |
| 5 | Version basis | the new WMS from its 1 October 2022 cutover | the parallel run's days are identical in both exports, C1 asserted |
| 6 | Denominator | a block's 24,000 position-months | space policy 4.2 |
| 7 | Weighting | each account's own episodes, weighted by their shipments | C3: unweighted, median and pooled shares give 2, asserted |
| 8 | Window length | all three earlier rushes | C3: each rush alone gives 2, asserted |
| 9 | Boundary inclusivity | at least three quarters | uses sit at 1.00 and 0.18, C1 |
| 10 | Rounding path | block uses unrounded; ask figures rounded once at the end | the prompt's last sentence; checks.py |
| 11 | Tie-break | none; blocks fill in order | space policy 4.2 |
| 12 | Maturity and censoring | nothing censored: the window is forecast, December completed by the notices | the tracker's header |
| 13 | Order of operations | the burn by day, then the month's mean | C1: a monthly burn gives 2, asserted |
| 14 | Row order | sums only | C1 |
| 15 | Duplicate resolution | the parallel-run days kept once | identical values, C1 asserted; A2's repeated box numbers are an ask device |
| 16 | Identity normalisation | legacy mnemonics to account ids through the register | the register; Rosales's two codes sum to one account |
| 17 | Netting against gross | each account's excess over its normal stock netted only against its own shipments | the normal stock in space policy 3.4 (SF13 asserted); the netting is the decisive step, nothing filed |
| 18 | Dimensional units | pallets throughout; notices in boxes converted | the tracker's planning-basis line; SF9 asserted |
| 19 | Code and status semantics | location types, ISO size-type codes, site codes | the dictionary; never the stump |
| 20 | Integerisation | whole blocks | space policy 4.1 |
| 21 | Clause scope | section 3 governs the forecast, section 4 the blocks | space policy |
| 22 | Forward window contents | the window's shipments forecast from each account's own record; the December notices | no plan file ships; the forecast is the analyst's, every grid cell gives 2 |

## Literal reader

Executed word for word, the prompt, space policy sections 3 and 4, the park's offer, the tracker's header, the advisories and the dictionary fix the population, the measure, the normal stock (3.4), the window, the unit and the test, and leave only the forecast method open; every method the earlier rushes do not reject files 2 blocks (the grid above), and every method that files another count (the fade, the book-level burn, the per-account monthly fall, no payback, the scaled and seasonal carries) is rejected by the earlier rushes' own record, asserted in checks.py under R3.

## Oracles

none: no shipped file states a forecast, a burn share, an excess or a block count; the capacity report (a distractor) reports past fiscal periods' rack utilisation only; the pallet extract (a distractor) lists the warehouse locations at the close and states no total; the earlier rushes are history in the same exports, not a control that ties under the golden or the wrong path.

## Ask sheet

**A2. For each month of January to October 2026, the TEU of the import containers whose freight reached us from the two ports (whole TEU) and that TEU as a share of the two ports' loaded import TEU (per cent, three decimals)** (twenty figures; the chart's bars and labels carry them).
- H18: an input reconciled to another system's total: the book's receipts against the ports' published imports.
- Use: how much of the ports' front-loading the book absorbed.
- Primary devices: (a) about one box in twenty is devanned across two shifts and confirmed as two receipts, and two accounts ship part of their freight in their own boxes, which come back every few months, so one box number is one visit when its receipts fall within days and two when months apart (the dictionary files that a container received in several pieces is counted once, in the month of its first receipt; it is silent on the same number coming back with new freight); counting rows overstates every month by 2 to 6 per cent and collapsing every repeated number understates it by 3 to 7; (b) five accounts receive part of their freight from the transload partner in 53ft trailers, each carrying one or two port boxes listed only in the partner's delivery manifest; counting no 53ft trailer understates every month by 2 to 5 per cent, counting each at 53/20 TEU overstates it.
- Hazards: confirmation stamps are UTC (a late-shift receipt on the last day of a month carries the next month's UTC date); a 45ft box is 2.25 TEU (the dictionary's TEU line); the two ports report in different layouts (Loaded Imports, Inbound Loaded).
- Files and columns on the path: the receipts export (received_at_utc, equipment_id, equipment_type, pallets), the transload manifest (trailer_no, container_no, iso_type), the two port releases, the dictionary.
- Stops, measured on the pack (TEU hits, share hits of ten, A2c): rows without trailers 0, 0; box numbers collapsed without trailers 0, 0; collapsed with the manifest 0, 0; rows with the manifest 0, 0; visits without trailers 0, 0; visits with trailers at 53/20 TEU 0, 0; visits and manifest on UTC months 0, 2; visits and manifest with 45ft at 2 TEU 0, 0; the golden 10, 10.
- Bins: every TEU 0.25 from its whole-TEU edge; every share at least 0.00026 from its three-decimal edge (a quarter cell; A2a, V9).
- Realism: split devanning and shipper-owned boxes on a rotation are how a receiving dock and two of its importers really work; a transload partner's manifest is the only record of which port boxes fed a trailer.

- Closures (the reader's and the judge's readings): the dictionary names the two ports ("Ocean containers reach us by dray from the container terminals of the Port of Los Angeles and the Port of Long Beach"), Avila's manifest carries each container's port beside its pickup terminal and says what it lists (containers devanned at Avila and delivered to us in 53' trailers), and every Avila trailer's delivery date is its WMS receipt's Pacific date, so a container counted through the manifest or through the trailer's receipt falls in the same month (A6, A7); the dictionary counts a container received in several pieces once, in the month of its first receipt (WMS) or delivery (Avila), which is how the golden dates each visit (A8; dated at its last piece instead, 7 of the 10 months' TEU move, by 1 to 9).

**The main population's zero-counts:** the port ask reads TEU and equipment; the call reads pallets, unchanged by the split receipts' re-dating (the pallets move between two adjacent days, asserted on every split), the box numbers and the trailers.

**Hazard table:** the UTC stamps (the month boundary), the 45ft TEU line, the two ports' layouts.

**Referee:** the partner's manifest is the only record of the trailers' boxes.

| Ask | Cracker (C1) | Verdict |
|---|---|---|
| Port TEU, ten months | battery dedup of repeated box numbers, no 53ft trailer counted: 0 of 10 | miss |
| Port shares, ten months | from those TEU: 0 of 10 | miss |
| Chart bars and labels | from those figures: 0 of 2 | miss |

A thorough solver beyond the cracker (C2: reads the manifest, collapsing repeated numbers) misses all twenty figures as well, keeping the chart's three structural points (12.0 per cent of the ask weight).

Pair ceiling: 35.1 (C1 or C2 with the mirror)

Mirror leakage: 12.0 (the mirror stops on rung 2, one block, and handles the ask as C1)

Measured by: generator/cracker.py

## Leak sweep

`leak.py task161 --asof 2026-12-07`: REVIEW, no LEAK (the rack capacity 40,000, the block size 4,000 and the price $1,100,000 are filed inputs, listed under `stated_inputs`).
- The block offer carries the call's words and four stump terms ("accounts" in its copy line, positions, pallets): it is the offer the call answers (six blocks, the term, the price), with no number to take. Harmless.
- The space policy carries eight stump terms (account, shipments, forecast, policy, positions, months): it files the estimand, an account's normal stock (3.4) and the block test and names no method for the stock above normal (P2 asserts no sentence names a fade, a burn, a half-life or a netting). Harmless.
- The advisories carry three (earlier, shipments, months): "bring shipments forward" and dates. Harmless.
- Dates after the as-of: the December booking tracker (arrivals due 7 to 31 December), the export manifest (the tracker's coverage) and the site list (the sublease ends 31 December): forward-looking records known at the as-of, the allow-list S13 asserts.

## Surface screen

`guard.py surface task161` promotes eleven pairs for adjudication; none carries a hard tell. Four (task267, task448, task266, task194) on surface similarity 0.102, the corpus top percentile, share only `export_manifest.csv`, a corpus habit in 55 builds, and no column, prompt phrase or decision; five (task451, task135, task460, task87, task259) on the card signature differentiated at registration; and task160, the build before this one, on two of three mechanism axes (gap time and decision type quantity_figure): its decisive pattern (G16 against G7), strategy (forecast_method_backtest against other), Gate G mechanism (forecasting against method_or_model_selection), domain, world and decision all differ, so it is the same-puzzle test's near miss, left for the author's adjudicated clone-check; task162, the build after this one (registered seventeen minutes later), is promoted on the same two axes (gap time and decision type quantity_figure), its strategy (time_semantics against other), Gate G mechanism (forecasting against method_or_model_selection), domain, world and decision all differing, and is left for the same read. The people read finds "Jan Feb" (two month labels in adjacent cells) and "Vance Customs" (the broker's firm name), not personas. `guard.py heart task161`: WARN (overuse.gate_g, repeat.decision and repeat.question_form against task160, answered in the Draw), nearest drivers 0.06; its people.first BLOCK on the customer service manager's first name, used by a build registered earlier the same night, was cleared by drawing Frederick James from `guard.py names`.

## Tried and rejected

- Block test on the January peak alone (the seed's peak-month framing): January's need is mostly the end-December stock plus one month's burn, so the no-payback and seasonal-carry routes land within half a block of the burn; the test moved to each block's use over the whole term.
- Block test as each block's average use with a path that falls through the term: a declining path leaves one block's use near the 75 per cent line under a 15 per cent change in the burn rate; the world is tuned so the burn path plateaus inside one block band from March (the spring stock build offsets the burn).
- forecast_method_backtest as the strategy key: the decisive move is a constructed balance with nothing filed to select it among fitted methods, so the card keys `other`, as task138 and task148 keyed their balance and queue constructions.
- The excess spread evenly across the book with a large rush for every account: the book-level burn and the per-account burn then agree and a burn at the book's share lands the call; the current excess was moved onto five seasonal accounts that bought for their whole 2027 season.
- Earlier rushes of uneven size by account: the book's share measured over the whole of each earlier decline averaged in the long tails and fell to the current mix's pace, landing the call by coincidence; the earlier rushes were made similar in size across accounts (about two months of affected lines each).
- Noisy shares from a lagging replenishment and a regression through the origin: the share came out at two thirds of its value; the replenishment now tracks its target within days, and each episode's share is a slope with an intercept, cut at the next announcement.
- A1 with trailers placed by the yard they were set up in against the yard check's current spot: either a fork (which site is a trailer's) or a documented device the cracker executes; dropped for the warehouse-location scope of the pallet export.
- A1 by location type per building with bulk floor lanes carried as one row with a pallet quantity: the units column shows two values and the hygiene battery's unit check resolves it.
- A third ask on fiscal-period rack utilisation with a rack re-typing: its device touched only the periods before the change, so the cracker kept the rest.

- Box-only booking notices on a seasonal account (KDT Mobile Accessories): read as no pallets they moved the call to one block, so the box-only notices went to three accounts outside the five (Ashby Linens, Bramwell Pet Supply, Garza Auto Parts), where every handling files 2.
- Port shares graded to two decimals: three months shared 0.29 and a constant response would hit three of ten, and the first placement left five shares on one fourth decimal; graded to three decimals with each month's placement drawn.
- The ports' own 2026 releases as a real public spine: the network proxy refuses both ports' websites, so the two releases are constructed in each port's layout and declared in metadata.json.
- Three client names within an edit or a word of real firms (Kenwick against Kenswick, Paloma against Paloma Wool, Ritter against Ritter's): renamed Quillan, Ostrander and Bramwell before the pack was cut.
- The run stamp as an A1 hazard: the as-of close is a Sunday, so the run stamped 6 December holds the same balances; kept as Layer 1 texture and not counted against A1.
- A projection Saturday weight of 0.42 from the generator's calendar: the book's own Saturday shipments run 0.40 of a weekday in 2025 and 2026, so the golden uses 0.40 and S11 asserts it.

- The off-rack ask (pallets outside the racks at each building): the reader and the judge read it two ways (floor and staging rows only, or the nightly balance less racked pallets) because the pallet extract's coverage was unfiled; filing it (warehouse locations only, yard trailers in the yard system) closed the reading but handed the device to the cracker, which executes filed coverage, leaving the ask no silent primary; retired, and the pallet extract kept as a distractor with its coverage filed.
- Today's stock held flat landed 2 (overflow 10,449 to 10,870 inside the 7,000 to 11,000 band that files 2): bought-ahead arrivals now spread evenly over each build window instead of ramping into December, so the close of 6 December holds more of the build (52,180 pallets) and every flat hold files 3, while the 31 December stock and the golden are unchanged in kind.
- The fade passed the earlier rushes' back-test (13.5 per cent behind the burn, ahead in 2019): the April 2025 rush now has the five seasonal accounts buying through the end of July (3.8 months), facing the steepest of that spring's expected rates, the one earlier rush in their low season; the burn is 47 per cent under the fade and ahead on all three rushes.
- An April 2025 pull-forward through October (6.9 months): its stock ran into the August 2025 episode and each account's own monthly fall landed 2; through July keeps the two episodes apart.
- Stock from an earlier rush frozen through a later build (the generator held the burn during build days): it now keeps burning through the later build at its owner's share.
- Each account's own monthly fall at 0.77 of block 2 (landing 2) with the milder seasonal categories shipping their holiday quarter at only 1.6 to 1.8 times their first-half pace: housewares, mobile accessories and small appliances now run at about twice, as their categories do; the monthly fall files 1 at the median, mean or latest rate.
- A sailing-shaped build (arrivals climbing over five weeks and tailing off over four): it put the 2019 and August 2025 rushes on the fade's side of the back-test; the even spread kept.
- Write-up figures that rest on the episode-fit conventions (the 30 June excess, block 3's use, the monthly overflow line, block 2's 96.7 per cent): the judge's conventions gave 11,571, 28.7 per cent, a flat line and 100 per cent; the write-up now states only the close's stock, the five's January 2026 shipments, the call and what every construction shares.
- A sublease shown holding 556 pallets at the close of its last day: emptied over its last ten days.
- Every document dated with the export: each file now carries its own date (exports at their pull, documents at their saving), and the capacity report's workbook is dated December 2026.
- Two shares that read round at three decimals (0.300, 0.280) and a month of exactly 1,800 TEU: the port placement moves a share ending in zero to the next cell, and four of that month's 40ft high cubes are re-typed as 45ft boxes.
- Normal stock left to the analyst's convention (the golden's cover against the mean of this and next month's shipments): the round 2 judge's same-month and centred three-month covers and a flat median stock filed 1, the next month's cover 3, and a daily forward window of 21 to 30 days left block 2 at 0.73; space policy 3.4 now defines an account's normal stock as its cover times the mean of its shipments in the month and the month after (SF13), and how the stock above it leaves stays unfiled.
- A container devanned in pieces with its month unfiled: dated at its last piece, 7 of the 10 months' TEU move by 1 to 9; the dictionary now counts it once, in the month of its first receipt (WMS) or delivery (Avila), as the golden does (A8).
- The write-up's line that a burn at the book's share of its shipments files one block or none: the round 2 judge's per-episode book shares (0.125 to 0.147) filed 2, against 0 or 1 in the generator's construction; the clause is dropped from the recommendation.
