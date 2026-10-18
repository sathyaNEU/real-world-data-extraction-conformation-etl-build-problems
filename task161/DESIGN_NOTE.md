# task161 design note

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task161.json`, registered 2026-10-18T01:20:40Z, guard WARN (no BLOCK).
- **Pairing:** Supply Chain & Logistics (house domain `supply-chain-logistics`, task type fulfillment and warehousing), client domain Urban & Regional Science, task type `forecasting`. Objective Forecasting & Predictive Modeling.
- **Seed:** FC32. Kept: the world (an import 3PL beside the San Pedro Bay ports, 40,000 rack positions in its own buildings), the decision (how many of six 4,000-position overflow blocks to take for January to June) and the quantity (the half-year's positions above the 3PL's own racks). Not kept: the seed's error-band mechanism, its leasing-test-on-a-lower-edge and its option date.
- **Shape:** 02, forecast across many periods (each month of January to June 2027), with the block test read off the monthly path.
- **Strategy:** `other` (a stock balance: bought-ahead pallets netted per customer against that customer's own shipments). Gap time, then population. Decisive generator G7 (when can the excess physically leave: only as its owner ships), then G13 (the burn runs through a season no earlier burn ran through) and G2 (the unit of netting is the owner's own stock, not the book).
- **Data-native sentence:** customers' bought-ahead pallets leave the buildings only as each customer ships them, and in every earlier rush a customer's receipts ran short of its shipments by a steady share of those shipments until its own excess was gone, so the excess left by this rush, several times any earlier one per customer and burning through the January and February trough, outlasts anything the earlier rushes' fade suggests.
- **Furniture:** forum executive_team; forcing event season_or_peak (the half-year after the rush; the park lets its six blocks for the January to June term to whoever commits before it starts, with no option or exercise date in this world); organisation logistics_or_3pl; role capacity_planner; context artifact filed_standard (the 3PL's space policy filing the block test, and the park's block terms); calibration existing_book_actuals (the book's own 2019 and 2025 rushes).
- **Personas** (guard.py names --geo 'United States' --seed 161): Jerome Lam, Nicole Freeman, Brandon Page, Mariah Norman. Karen Haynes was drawn and dropped (first name on an older build).
- **WARN answers.** overuse.gate_g: method_or_model_selection is the honest mechanism (the half-life and the burn both fit the small earlier rushes; only the rushes of different size and season separate them), and the strategy and generator differ from every one of the five. repeat.decision and repeat.question_form against task160: the call is a count of blocks, so it asks how many; task160's is a count of nurse shifts in another domain, objective furniture and mechanism. Deliverables moved from png plus xlsx to pdf plus xlsx to clear repeat.deliverables.
- **Same puzzle and same driver** (older): differentiated on the card against task259, task87, task135, task451, task460; none nets a stock against its owners' own use.
- **Sources read at the draw** (one line each):
  - `guard.py mechanisms --objective forecasting`: the stock and queue drivers on file (task138's store rebuilt through a balance, task148's queue with reneging, task156's volunteer backlog, task159's platform backlog) each build a quantity from inflow against a service rate; none nets a stock bought ahead of a price step against its owners' later demand, and none turns on the size of the excess against a fade measured on smaller ones.
  - task152 (a forward sale at P50 with its sigma) and task151 (a stepped payout from a predictive distribution): the commitment here is read off the forecast path's level, never off a tail or an interval.
  - task157 (a returning wave sized from its leading edge): a wave of members coming back on a calendar; here nothing comes back, a held stock leaves at its owners' pace.
  - task153 (a yard's draw capped per segment at a tankful): a min() per segment of a vehicle's need; here the min() is each owner's excess against its own cumulative burn.
  - task154 and task160 (forecast_method_backtest, G16): nothing here files a back-test or a selection criterion; the method is the balance, and the earlier rushes are the evidence a planner reads, not a filed test.
  - Urban & Regional Science forecasting pattern 1 (back-test from the forecast origin): the rivals are rejected on the earlier rushes, each fitted from its own origin, which is how a planner checks a fade against a burn.

## Default path

1. Read the WMS daily on-hand history into one series of positions held per day (old and new layouts stacked, overflow location classes included), and average it by calendar month.
2. Take the seasonal normal from the years without a rush and measure the book's excess over it at the end of each earlier rush (summer 2019, the first quarter of 2025, summer 2025) and month by month afterwards.
3. Fit the fade of that excess (a half-life of about a month across the three rushes, the excess back to normal within two to three months).
4. Project end-December 2026 from end-November plus the December booking notices less December's normal shipments, take its excess over the seasonal normal, and fade it at the fitted half-life through January to June 2027.
5. Add the faded excess to the seasonal normal for 2027, take the overflow above 40,000 rack positions month by month, and run the space policy's block test.

Ends on: 0 blocks (none)

Golden: 2 blocks

## Stump sentence

The default path fades this rush's excess at the half-life the earlier rushes showed, clears it by March and takes 0 blocks (none); the step that lands it there is treating the excess as a proportional decay, when it is stock each customer burns at a steady share of its own shipments, so a rush several times larger than any earlier one, burning through the January and February trough, keeps two blocks full through June.

## Tried and rejected

- Block test on the January peak alone (the seed's peak-month framing): January's need is mostly the end-December stock plus one month's burn, so the no-payback and seasonal-carry routes land within half a block of the burn; the test moved to each block's use over the whole term.
- Block test as each block's average use with a path that falls through the term: a declining path leaves one block's use near the 75 per cent line under a 15 per cent change in the burn rate; the world is tuned so the burn path plateaus inside one block band from March (the spring stock build offsets the burn).
- forecast_method_backtest as the strategy key: the decisive move is a constructed balance with nothing filed to select it among fitted methods, so the card keys `other`, as task138 and task148 keyed their balance and queue constructions.
